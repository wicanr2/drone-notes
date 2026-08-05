"""飛控介面。

抽成介面的用意是讓執行器能在兩種後端上跑同一套邏輯:
- FakeVehicle:單元測試用,確定性、可注入中斷、跑得飛快
- MavsdkVehicle:接真的 PX4 SITL 或實機

介面刻意只暴露「高階意圖」(起飛、飛到、拍照),不暴露 setpoint 層級的細節。
需要即時控制時由實作內部處理 Offboard 的進出,見
docs/40-mission-control/02-onboard-executor.md「Offboard 的正確用法」。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass
class VehicleState:
    """飛控回報的狀態快照。

    每個欄位都帶 stale_s 的概念:呼叫端要能判斷這份資料多舊。
    介面層只回傳快照,新鮮度判斷留給呼叫端(見 docs/50 的載具模型層)。
    """

    armed: bool = False
    mode: str = "HOLD"
    in_air: bool = False
    lat: float = 0.0
    lon: float = 0.0
    alt_rel_m: float = 0.0
    yaw_deg: float = 0.0
    battery_remaining: float = 1.0
    position_ok: bool = True
    updated_at: float = 0.0


@dataclass
class Interrupt:
    """飛控端發生、會打斷任務的事件。"""

    kind: str          # failsafe.low_battery / failsafe.rc_loss / operator_takeover ...
    detail: str = ""
    data: dict = field(default_factory=dict)


class VehicleError(RuntimeError):
    """飛控拒絕了某個請求。原因要往上帶,不要吞掉重試。"""


@runtime_checkable
class Vehicle(Protocol):
    async def connect(self) -> None: ...
    async def close(self) -> None: ...

    async def state(self) -> VehicleState: ...

    async def arm(self) -> None: ...
    async def takeoff(self, altitude_m: float) -> None: ...
    async def goto(self, lat: float, lon: float, alt_rel_m: float, yaw_deg: float | None = None) -> None: ...
    async def land(self) -> None: ...
    async def return_to_launch(self) -> None: ...

    async def set_gimbal(self, pitch_deg: float, yaw_deg: float) -> None: ...
    async def capture_photo(self) -> str:
        """回傳照片識別碼。

        注意這裡的語意是「已確認存檔」,不是「已送出拍照指令」——
        完成判定看實際狀態是這個領域反覆出現的原則。
        """
        ...

    def poll_interrupt(self) -> Interrupt | None:
        """取出待處理的中斷。執行器在動作執行期間持續輪詢它。"""
        ...
