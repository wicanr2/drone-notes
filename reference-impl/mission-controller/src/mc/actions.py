"""動作:任務執行器的基本單位。

為什麼是動作而不是航點,以及這五個方法各自對應哪一種失敗經驗,
見 docs/40-mission-control/02-onboard-executor.md。
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from .clock import Clock
from .models import ActionSpec, CheckResult, ResumePolicy
from .vehicle.base import Vehicle

_M_PER_DEG_LAT = 111_320.0


@dataclass
class Context:
    vehicle: Vehicle
    clock: Clock
    emit: Callable[[str, dict], None]
    home_lat: float = 0.0
    home_lon: float = 0.0


class Action(Protocol):
    name: str
    resume_policy: ResumePolicy
    timeout_s: float

    def preconditions(self, ctx: Context) -> CheckResult: ...
    async def execute(self, ctx: Context) -> None: ...
    async def is_complete(self, ctx: Context) -> bool: ...
    async def on_abort(self, ctx: Context, reason: str) -> None: ...


@dataclass
class BaseAction:
    params: dict[str, Any] = field(default_factory=dict)
    name: str = "base"
    resume_policy: ResumePolicy = ResumePolicy.CONTINUE
    timeout_s: float = 300.0

    def preconditions(self, ctx: Context) -> CheckResult:
        return CheckResult.passed()

    async def is_complete(self, ctx: Context) -> bool:
        return True

    async def on_abort(self, ctx: Context, reason: str) -> None:
        """預設什麼都不做。

        on_abort 是在已經出事的路徑上跑的,所以裡面只能放冪等、
        不依賴外部條件、不會拋例外的收尾動作。
        """
        return None


@dataclass
class Takeoff(BaseAction):
    """起飛。

    resume_policy 用 CONTINUE 而不是 SKIP,是踩過才改的:
    中斷可能發生在起飛「途中」,這時飛機還在地面。盲目 SKIP 會讓下一個
    goto 在「以為已經在空中」的錯誤前提下執行,直接被飛控拒絕。
    正確做法是重跑這個動作,由 execute 自己去看實際狀態決定要不要起飛——
    也就是把冪等性放在動作裡,而不是靠恢復政策去猜。
    """

    name: str = "takeoff"
    resume_policy: ResumePolicy = ResumePolicy.CONTINUE
    timeout_s: float = 60.0

    def preconditions(self, ctx: Context) -> CheckResult:
        alt = float(self.params.get("altitude_m", 5.0))
        if alt <= 0 or alt > 120:
            return CheckResult.failed(f"altitude_m 超出合理範圍: {alt}")
        return CheckResult.passed()

    async def execute(self, ctx: Context) -> None:
        alt = float(self.params.get("altitude_m", 5.0))
        st = await ctx.vehicle.state()
        if st.in_air:
            ctx.emit("action_skipped", {"action": self.name, "why": "already_in_air"})
            return
        await ctx.vehicle.arm()
        await ctx.vehicle.takeoff(alt)

    async def is_complete(self, ctx: Context) -> bool:
        alt = float(self.params.get("altitude_m", 5.0))
        st = await ctx.vehicle.state()
        return st.in_air and abs(st.alt_rel_m - alt) < 1.0


@dataclass
class Goto(BaseAction):
    name: str = "goto"
    resume_policy: ResumePolicy = ResumePolicy.CONTINUE
    timeout_s: float = 600.0

    def preconditions(self, ctx: Context) -> CheckResult:
        for k in ("lat", "lon"):
            if k not in self.params:
                return CheckResult.failed(f"缺少參數 {k}")
        return CheckResult.passed()

    async def execute(self, ctx: Context) -> None:
        await ctx.vehicle.goto(
            float(self.params["lat"]),
            float(self.params["lon"]),
            float(self.params.get("alt_rel_m", 5.0)),
            self.params.get("yaw_deg"),
        )

    async def is_complete(self, ctx: Context) -> bool:
        st = await ctx.vehicle.state()
        return _distance_m(st.lat, st.lon, float(self.params["lat"]), float(self.params["lon"])) < 1.5


@dataclass
class OrbitPhoto(BaseAction):
    """繞著目標飛一圈,每隔固定角度拍一張。

    resume_policy 是 RESTART:這組照片要拼成一份環景資料,
    少了中間幾張整組就沒用,所以中斷後重來比續拍有意義。
    這種判斷牽涉業務語意,要人決定,不能靠通則。
    """

    name: str = "orbit_photo"
    resume_policy: ResumePolicy = ResumePolicy.RESTART
    timeout_s: float = 600.0
    _captured: list[str] = field(default_factory=list)

    def preconditions(self, ctx: Context) -> CheckResult:
        shots = int(self.params.get("shots", 8))
        radius = float(self.params.get("radius_m", 10.0))
        if shots <= 0 or shots > 72:
            return CheckResult.failed(f"shots 超出合理範圍: {shots}")
        if radius < 2.0 or radius > 200.0:
            return CheckResult.failed(f"radius_m 超出合理範圍: {radius}")
        return CheckResult.passed()

    async def execute(self, ctx: Context) -> None:
        lat0 = float(self.params["lat"])
        lon0 = float(self.params["lon"])
        alt = float(self.params.get("alt_rel_m", 10.0))
        radius = float(self.params.get("radius_m", 10.0))
        shots = int(self.params.get("shots", 8))
        gimbal_pitch = float(self.params.get("gimbal_pitch_deg", -10.0))

        self._captured.clear()
        for i in range(shots):
            bearing = 2 * math.pi * i / shots
            lat, lon = _offset(lat0, lon0, radius, bearing)
            # 機頭與雲台都朝向圓心:繞行方位角加 180 度。
            yaw = (math.degrees(bearing) + 180.0) % 360.0
            await ctx.vehicle.goto(lat, lon, alt, yaw)
            await ctx.vehicle.set_gimbal(gimbal_pitch, 0.0)
            await ctx.clock.sleep(float(self.params.get("settle_s", 1.0)))
            photo_id = await ctx.vehicle.capture_photo()
            self._captured.append(photo_id)
            ctx.emit("photo_captured", {"id": photo_id, "index": i, "of": shots})

    async def is_complete(self, ctx: Context) -> bool:
        # 看實際拍到並確認的張數,不看送出了幾次拍照指令。
        return len(self._captured) == int(self.params.get("shots", 8))

    async def on_abort(self, ctx: Context, reason: str) -> None:
        await ctx.vehicle.set_gimbal(0.0, 0.0)
        ctx.emit("orbit_photo_aborted", {"captured": len(self._captured), "reason": reason})


@dataclass
class Land(BaseAction):
    name: str = "land"
    resume_policy: ResumePolicy = ResumePolicy.CONTINUE
    timeout_s: float = 180.0

    async def execute(self, ctx: Context) -> None:
        await ctx.vehicle.land()

    async def is_complete(self, ctx: Context) -> bool:
        st = await ctx.vehicle.state()
        return not st.in_air


@dataclass
class ReturnToLaunch(BaseAction):
    name: str = "rtl"
    resume_policy: ResumePolicy = ResumePolicy.CONTINUE
    timeout_s: float = 600.0

    async def execute(self, ctx: Context) -> None:
        await ctx.vehicle.return_to_launch()

    async def is_complete(self, ctx: Context) -> bool:
        st = await ctx.vehicle.state()
        return not st.in_air


REGISTRY: dict[str, type[BaseAction]] = {
    "takeoff": Takeoff,
    "goto": Goto,
    "orbit_photo": OrbitPhoto,
    "land": Land,
    "rtl": ReturnToLaunch,
}


def build(spec: ActionSpec) -> BaseAction:
    if spec.type not in REGISTRY:
        raise KeyError(f"未知的動作型別: {spec.type}(已註冊: {sorted(REGISTRY)})")
    return REGISTRY[spec.type](params=dict(spec.params))


def _distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    dlat = (lat2 - lat1) * _M_PER_DEG_LAT
    dlon = (lon2 - lon1) * _M_PER_DEG_LAT * math.cos(math.radians(lat1))
    return math.hypot(dlat, dlon)


def _offset(lat: float, lon: float, distance_m: float, bearing_rad: float) -> tuple[float, float]:
    dlat = distance_m * math.cos(bearing_rad) / _M_PER_DEG_LAT
    dlon = distance_m * math.sin(bearing_rad) / (_M_PER_DEG_LAT * math.cos(math.radians(lat)))
    return lat + dlat, lon + dlon
