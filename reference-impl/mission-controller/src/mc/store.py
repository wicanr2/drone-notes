"""持久化。

用 SQLite 而不是記憶體,理由是執行器隨時可能重啟(見 docs/30 的
「假設隨時會重啟」)。事件表是 append-only,(execution_id, seq) 唯一,
所以重送同一筆事件不會產生第二列——這就是雲端去重的機制在機上的對應。
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .models import (
    Execution,
    ExecutionEvent,
    MissionDefinition,
    MissionPlan,
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS definitions (
    id TEXT NOT NULL, version INTEGER NOT NULL, body TEXT NOT NULL,
    PRIMARY KEY (id, version)
);
CREATE TABLE IF NOT EXISTS plans (
    id TEXT NOT NULL, version INTEGER NOT NULL, body TEXT NOT NULL,
    PRIMARY KEY (id, version)
);
CREATE TABLE IF NOT EXISTS executions (
    id TEXT PRIMARY KEY, plan_id TEXT NOT NULL, plan_version INTEGER NOT NULL, body TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    execution_id TEXT NOT NULL, seq INTEGER NOT NULL, body TEXT NOT NULL,
    PRIMARY KEY (execution_id, seq)
);
"""


class Store:
    def __init__(self, path: str | Path = ":memory:") -> None:
        self.conn = sqlite3.connect(str(path), check_same_thread=False)
        self.conn.executescript(_SCHEMA)
        self.conn.commit()

    # --- 定義與計畫 -------------------------------------------------------

    def save_definition(self, d: MissionDefinition) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO definitions (id, version, body) VALUES (?, ?, ?)",
            (d.id, d.version, d.model_dump_json()),
        )
        self.conn.commit()

    def get_definition(self, def_id: str, version: int) -> MissionDefinition | None:
        row = self.conn.execute(
            "SELECT body FROM definitions WHERE id=? AND version=?", (def_id, version)
        ).fetchone()
        return MissionDefinition.model_validate_json(row[0]) if row else None

    def save_plan(self, p: MissionPlan) -> bool:
        """回傳 True 表示這是新的計畫版本,False 表示重複派工。

        派工的冪等鍵是「計畫 ID + 版本」:同一版重送任意次只會被接受一次。
        少了這一條,一次網路重試就等於飛兩趟。
        """
        existing = self.conn.execute(
            "SELECT 1 FROM plans WHERE id=? AND version=?", (p.id, p.version)
        ).fetchone()
        if existing:
            return False
        self.conn.execute(
            "INSERT INTO plans (id, version, body) VALUES (?, ?, ?)",
            (p.id, p.version, p.model_dump_json()),
        )
        self.conn.commit()
        return True

    def get_plan(self, plan_id: str, version: int) -> MissionPlan | None:
        row = self.conn.execute(
            "SELECT body FROM plans WHERE id=? AND version=?", (plan_id, version)
        ).fetchone()
        return MissionPlan.model_validate_json(row[0]) if row else None

    # --- 執行與事件 -------------------------------------------------------

    def save_execution(self, ex: Execution) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO executions (id, plan_id, plan_version, body) VALUES (?, ?, ?, ?)",
            (ex.id, ex.plan_id, ex.plan_version, ex.model_dump_json()),
        )
        self.conn.commit()

    def get_execution(self, execution_id: str) -> Execution | None:
        row = self.conn.execute(
            "SELECT body FROM executions WHERE id=?", (execution_id,)
        ).fetchone()
        return Execution.model_validate_json(row[0]) if row else None

    def load_execution_for(self, plan: MissionPlan) -> Execution | None:
        row = self.conn.execute(
            "SELECT body FROM executions WHERE plan_id=? AND plan_version=?",
            (plan.id, plan.version),
        ).fetchone()
        return Execution.model_validate_json(row[0]) if row else None

    def append_event(self, evt: ExecutionEvent) -> None:
        # 重複的 (execution_id, seq) 直接忽略:去重靠鍵,不靠呼叫端的紀律。
        self.conn.execute(
            "INSERT OR IGNORE INTO events (execution_id, seq, body) VALUES (?, ?, ?)",
            (evt.execution_id, evt.seq, evt.model_dump_json()),
        )
        self.conn.commit()

    def events(self, execution_id: str) -> list[ExecutionEvent]:
        rows = self.conn.execute(
            "SELECT body FROM events WHERE execution_id=? ORDER BY seq", (execution_id,)
        ).fetchall()
        return [ExecutionEvent.model_validate_json(r[0]) for r in rows]

    def event_names(self, execution_id: str) -> list[str]:
        return [e.event for e in self.events(execution_id)]

    def dump_events(self, execution_id: str) -> str:
        return json.dumps([e.model_dump() for e in self.events(execution_id)],
                          ensure_ascii=False, indent=2)
