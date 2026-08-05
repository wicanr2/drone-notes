"""測試用的假飛控。

它做三件真飛控會做、但在單元測試裡很難重現的事:
1. 依虛擬時間移動,所以一趟十分鐘的任務可以在幾毫秒內跑完
2. 在指定的虛擬時刻注入中斷(低電量、遙控器中斷、操作者接管)
3. 記錄所有被呼叫過的動作,讓測試可以斷言「順序對不對」
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from ..clock import Clock
from .base import Interrupt, VehicleError, VehicleState

# 粗略的度/公尺換算,只用於讓假飛控的移動看起來合理。
_M_PER_DEG_LAT = 111_320.0


@dataclass
class ScheduledInterrupt:
    at: float                  # 虛擬時間(秒)
    interrupt: Interrupt
    fired: bool = False


@dataclass
class FakeVehicle:
    clock: Clock
    speed_mps: float = 5.0
    climb_mps: float = 2.0
    photo_delay_s: float = 0.5
    battery_drain_per_s: float = 0.0005
    reject_arm_reason: str | None = None

    _state: VehicleState = field(default_factory=VehicleState)
    calls: list[tuple[str, dict]] = field(default_factory=list)
    photos: list[str] = field(default_factory=list)
    scheduled: list[ScheduledInterrupt] = field(default_factory=list)
    _pending: list[Interrupt] = field(default_factory=list)

    # --- 測試用的注入介面 -------------------------------------------------

    def schedule_interrupt(self, at_s: float, kind: str, detail: str = "") -> None:
        self.scheduled.append(ScheduledInterrupt(at=at_s, interrupt=Interrupt(kind, detail)))

    def _tick(self) -> None:
        now = self.clock.now()
        self._state.updated_at = now
        for s in self.scheduled:
            if not s.fired and now >= s.at:
                s.fired = True
                self._pending.append(s.interrupt)

    def poll_interrupt(self) -> Interrupt | None:
        self._tick()
        return self._pending.pop(0) if self._pending else None

    # --- Vehicle 介面 -----------------------------------------------------

    async def connect(self) -> None:
        self.calls.append(("connect", {}))

    async def close(self) -> None:
        self.calls.append(("close", {}))

    async def state(self) -> VehicleState:
        self._tick()
        return self._state

    async def arm(self) -> None:
        self.calls.append(("arm", {}))
        if self.reject_arm_reason:
            # 真飛控的 pre-arm 拒絕會帶原因,程式要往上帶而不是重試。
            raise VehicleError(f"arm rejected: {self.reject_arm_reason}")
        self._state.armed = True

    async def takeoff(self, altitude_m: float) -> None:
        self.calls.append(("takeoff", {"altitude_m": altitude_m}))
        if not self._state.armed:
            raise VehicleError("takeoff rejected: not armed")
        await self._advance(abs(altitude_m - self._state.alt_rel_m) / self.climb_mps)
        self._state.alt_rel_m = altitude_m
        self._state.in_air = True
        self._state.mode = "TAKEOFF"

    async def goto(self, lat: float, lon: float, alt_rel_m: float, yaw_deg: float | None = None) -> None:
        self.calls.append(("goto", {"lat": lat, "lon": lon, "alt_rel_m": alt_rel_m, "yaw_deg": yaw_deg}))
        if not self._state.in_air:
            raise VehicleError("goto rejected: not in air")
        dist = self._distance_m(lat, lon) + abs(alt_rel_m - self._state.alt_rel_m)
        await self._advance(dist / self.speed_mps)
        self._state.lat, self._state.lon, self._state.alt_rel_m = lat, lon, alt_rel_m
        if yaw_deg is not None:
            self._state.yaw_deg = yaw_deg
        self._state.mode = "OFFBOARD"

    async def land(self) -> None:
        self.calls.append(("land", {}))
        await self._advance(self._state.alt_rel_m / 1.0)
        self._state.alt_rel_m = 0.0
        self._state.in_air = False
        self._state.armed = False
        self._state.mode = "LAND"

    async def return_to_launch(self) -> None:
        self.calls.append(("return_to_launch", {}))
        self._state.mode = "RTL"
        await self._advance(10.0)
        self._state.alt_rel_m = 0.0
        self._state.in_air = False
        self._state.armed = False

    async def set_gimbal(self, pitch_deg: float, yaw_deg: float) -> None:
        self.calls.append(("set_gimbal", {"pitch_deg": pitch_deg, "yaw_deg": yaw_deg}))
        await self._advance(0.2)

    async def capture_photo(self) -> str:
        await self._advance(self.photo_delay_s)
        pid = f"IMG_{len(self.photos):04d}"
        self.photos.append(pid)
        self.calls.append(("capture_photo", {"id": pid}))
        return pid

    # --- 內部 -------------------------------------------------------------

    async def _advance(self, seconds: float) -> None:
        await self.clock.sleep(max(seconds, 0.0))
        self._state.battery_remaining = max(
            0.0, self._state.battery_remaining - seconds * self.battery_drain_per_s
        )
        self._tick()

    def _distance_m(self, lat: float, lon: float) -> float:
        dlat = (lat - self._state.lat) * _M_PER_DEG_LAT
        dlon = (lon - self._state.lon) * _M_PER_DEG_LAT * math.cos(math.radians(self._state.lat))
        return math.hypot(dlat, dlon)
