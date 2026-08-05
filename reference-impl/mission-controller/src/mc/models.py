"""資料模型。

刻意把「定義 / 計畫 / 執行 / 事件」四種東西分開,理由見
docs/40-mission-control/03-cloud-mission-service.md:

- MissionDefinition 不可變且版本化,稽核時要能回答「當時執行的是哪一版」
- MissionPlan 綁定一台機與一個時窗,同一個定義可以被多個計畫引用
- Execution 是一次實際執行的可變狀態
- ExecutionEvent 是 append-only 的事實,狀態由事件投影而來
"""

from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


def _now() -> float:
    return time.time()


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


class ActionSpec(BaseModel):
    """一個動作的宣告。type 決定用哪個 Action 實作,params 是它的參數。"""

    type: str
    params: dict[str, Any] = Field(default_factory=dict)


class MissionDefinition(BaseModel):
    """任務定義:做什麼。不可變——要改就發新版本。"""

    id: str = Field(default_factory=lambda: _new_id("def"))
    version: int = 1
    name: str
    actions: list[ActionSpec]
    created_at: float = Field(default_factory=_now)

    @property
    def key(self) -> tuple[str, int]:
        """冪等鍵的一半:定義 ID + 版本。"""
        return (self.id, self.version)


class MissionPlan(BaseModel):
    """執行計畫:哪台機、什麼時候、什麼約束。"""

    id: str = Field(default_factory=lambda: _new_id("plan"))
    version: int = 1
    definition_id: str
    definition_version: int
    vehicle_id: str
    constraints: dict[str, Any] = Field(default_factory=dict)
    created_at: float = Field(default_factory=_now)

    @property
    def idempotency_key(self) -> tuple[str, int]:
        """派工的冪等鍵:同一個計畫的同一版重送任意次,只會被接受一次。"""
        return (self.id, self.version)


class ExecutionState(str, Enum):
    RECEIVED = "received"
    PREPARING = "preparing"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABORTED = "aborted"
    REJECTED = "rejected"


class ResumePolicy(str, Enum):
    """中斷後怎麼恢復。屬於動作本身的性質,不是全域設定。"""

    RESTART = "restart"    # 整個動作重來(例如成組的環繞拍照)
    CONTINUE = "continue"  # 重跑這個動作,由動作自己判斷實際狀態(多數情況)
    SKIP = "skip"          # 直接跳過,不再執行。只用於「絕不可重複」的動作,
                           # 例如投放貨物;因為中斷可能發生在動作完成之前,
                           # SKIP 等於賭它已經做完了。


class ExecutionEvent(BaseModel):
    """append-only 的事實。seq 單調遞增,雲端據此去重與排序。"""

    execution_id: str
    seq: int
    event: str
    at: float = Field(default_factory=_now)
    data: dict[str, Any] = Field(default_factory=dict)


class Execution(BaseModel):
    """一次實際執行的狀態。seq 與狀態一起持久化,重啟後不歸零。"""

    id: str = Field(default_factory=lambda: _new_id("exec"))
    plan_id: str
    plan_version: int
    definition_id: str
    definition_version: int
    vehicle_id: str
    state: ExecutionState = ExecutionState.RECEIVED
    action_index: int = 0
    seq: int = 0
    started_at: float | None = None
    ended_at: float | None = None
    reason: str | None = None

    def next_seq(self) -> int:
        self.seq += 1
        return self.seq


class CheckResult(BaseModel):
    """前置檢查的結果。不過就不要開始,而不是開始了再失敗。"""

    ok: bool
    reason: str = ""

    @classmethod
    def passed(cls) -> CheckResult:
        return cls(ok=True)

    @classmethod
    def failed(cls, reason: str) -> CheckResult:
        return cls(ok=False, reason=reason)


AbortReason = Literal[
    "precondition_failed",
    "failsafe",
    "operator_takeover",
    "operator_cancel",
    "timeout",
    "vehicle_error",
]
