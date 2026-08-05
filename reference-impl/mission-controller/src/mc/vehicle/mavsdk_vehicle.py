"""接真的飛控(PX4 SITL 或實機),透過 MAVSDK。

跟 FakeVehicle 實作同一個介面,所以執行器的邏輯完全不用改。
需要額外安裝:`pip install mavsdk`(見 pyproject 的 mavsdk extra)。

幾個刻意的設計:

- 遙測用背景任務持續更新快照,而不是每次呼叫都去訂閱一次。
  MAVSDK 的遙測是 async generator,每次重新訂閱都要等下一筆。
- goto 用絕對高度(AMSL),所以起飛前先記住 home 的 AMSL,
  之後把相對高度換算過去。搞錯這個是很常見的高度偏差來源。
- 拒絕(pre-arm 沒過、模式條件不滿足)一律轉成 VehicleError 往上帶,
  不在這一層重試。原因見 docs/40-mission-control/02-onboard-executor.md。
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from ..clock import Clock, RealClock
from .base import Interrupt, VehicleError, VehicleState


@dataclass
class MavsdkVehicle:
    system_address: str = "udpin://0.0.0.0:14540"
    clock: Clock = field(default_factory=RealClock)
    connect_timeout_s: float = 60.0
    has_camera: bool = False
    has_gimbal: bool = False
    discover_timeout_s: float = 10.0
    photo_timeout_s: float = 20.0

    _drone: object | None = None
    _state: VehicleState = field(default_factory=VehicleState)
    _tasks: list[asyncio.Task] = field(default_factory=list)
    _pending: list[Interrupt] = field(default_factory=list)
    _home_amsl_m: float | None = None
    _last_mode: str = ""
    # 我們自己請求過的模式,用來排除「這個模式變更是我造成的」。
    _requested_modes: set[str] = field(default_factory=set)
    # 雲台與相機的識別碼查一次就好,但要等連上線才查得到,所以不在建構時做。
    _gimbal_id_cache: int | None = None
    _camera_id_cache: int | None = None
    _gimbal_controlled: bool = False

    async def connect(self) -> None:
        from mavsdk import System  # 延遲匯入,沒裝 mavsdk 也能跑假飛控

        self._drone = System()
        await self._drone.connect(system_address=self.system_address)

        deadline = self.clock.now() + self.connect_timeout_s
        async for cstate in self._drone.core.connection_state():
            if cstate.is_connected:
                break
            if self.clock.now() > deadline:
                raise VehicleError(f"連不上 {self.system_address}")

        self._tasks = [
            asyncio.create_task(self._watch_position()),
            asyncio.create_task(self._watch_flight_mode()),
            asyncio.create_task(self._watch_armed()),
            asyncio.create_task(self._watch_in_air()),
            asyncio.create_task(self._watch_battery()),
            asyncio.create_task(self._watch_health()),
            asyncio.create_task(self._watch_status_text()),
        ]
        await self._wait_for_position_fix()

    async def close(self) -> None:
        # 拿了雲台控制權就要還——不還的話下一個接手的元件(例如地面站的
        # 手動雲台操作)會被擋在外面,而且沒有明顯的錯誤訊息。
        if self._gimbal_controlled and self._gimbal_id_cache is not None:
            try:
                await self._drone.gimbal.release_control(self._gimbal_id_cache)
            except Exception:  # noqa: BLE001 - 收尾失敗不該蓋掉原本的關閉流程
                pass
            self._gimbal_controlled = False
        for t in self._tasks:
            t.cancel()
        self._tasks.clear()

    async def state(self) -> VehicleState:
        return self._state

    # --- 動作 -------------------------------------------------------------

    async def arm(self) -> None:
        try:
            await self._drone.action.arm()
        except Exception as err:  # noqa: BLE001 - MAVSDK 的拒絕是例外,要轉成領域錯誤
            raise VehicleError(f"arm rejected: {err}") from err

    async def takeoff(self, altitude_m: float) -> None:
        try:
            await self._drone.action.set_takeoff_altitude(float(altitude_m))
            await self._drone.action.takeoff()
        except Exception as err:  # noqa: BLE001
            raise VehicleError(f"takeoff rejected: {err}") from err

    async def goto(self, lat: float, lon: float, alt_rel_m: float, yaw_deg: float | None = None) -> None:
        if self._home_amsl_m is None:
            raise VehicleError("尚未取得 home 的絕對高度,無法換算目標高度")
        try:
            await self._drone.action.goto_location(
                float(lat), float(lon), self._home_amsl_m + float(alt_rel_m),
                float(yaw_deg) if yaw_deg is not None else float("nan"),
            )
        except Exception as err:  # noqa: BLE001
            raise VehicleError(f"goto rejected: {err}") from err

    async def land(self) -> None:
        self._requested_modes.add("LAND")
        try:
            await self._drone.action.land()
        except Exception as err:  # noqa: BLE001
            raise VehicleError(f"land rejected: {err}") from err

    async def return_to_launch(self) -> None:
        self._requested_modes.add("RETURN_TO_LAUNCH")
        try:
            await self._drone.action.return_to_launch()
        except Exception as err:  # noqa: BLE001
            raise VehicleError(f"rtl rejected: {err}") from err

    async def set_gimbal(self, pitch_deg: float, yaw_deg: float) -> None:
        """指向雲台。簽章對照 MAVSDK 3.17.2,見 docs/20-protocols/03。

        3.x 的雲台介面跟舊版差兩件事:每個呼叫都要帶 gimbal_id(一台機可以
        掛多個雲台),而且下角度之前要先 take_control。少了 take_control,
        指令會被接受但雲台不動——這種「成功但沒作用」最難查。
        """
        if not self.has_gimbal:
            raise VehicleError("這台機沒有設定雲台(has_gimbal=False)")

        from mavsdk.gimbal import ControlMode, GimbalMode, SendMode

        gid = await self._gimbal_id()
        try:
            if not self._gimbal_controlled:
                await self._drone.gimbal.take_control(gid, ControlMode.PRIMARY)
                self._gimbal_controlled = True
            await self._drone.gimbal.set_angles(
                gid,
                0.0,
                float(pitch_deg),
                float(yaw_deg),
                # YAW_FOLLOW:yaw 相對機頭。要相對正北請改 YAW_LOCK——
                # 這兩者搞混會讓繞行拍照的每一張都偏一個航向角。
                GimbalMode.YAW_FOLLOW,
                SendMode.ONCE,
            )
        except Exception as err:  # noqa: BLE001
            raise VehicleError(f"gimbal rejected: {err}") from err

    async def capture_photo(self) -> str:
        """拍一張並等到飛控回報存檔成功,回傳檔案位址。

        介面契約要求回傳的是「已確認存檔」而不是「已送出指令」,所以這裡
        必須等 capture_info。**先訂閱再拍**:反過來的話,回報可能在訂閱
        建立之前就送出,結果等到逾時。

        注意這樣仍不是完全沒有競態——訂閱要一個 gRPC 來回才真的生效。
        沒有相機硬體可測,所以這段只有介面層的測試,見 README 的驗證狀態。
        """
        if not self.has_camera:
            raise VehicleError("這台機沒有設定相機(has_camera=False)")

        from mavsdk.camera import Mode

        cid = await self._camera_id()
        waiter = asyncio.create_task(
            self._first(self._drone.camera.capture_info(), self.photo_timeout_s, "拍照結果")
        )
        try:
            await self._drone.camera.set_mode(cid, Mode.PHOTO)
            await self._drone.camera.take_photo(cid)
        except Exception as err:  # noqa: BLE001
            waiter.cancel()
            raise VehicleError(f"take_photo rejected: {err}") from err

        info = await waiter
        if not info.is_success:
            raise VehicleError("相機回報拍照失敗")
        return str(info.file_url or f"IMG_{info.index}")

    # --- MAVSDK 的查詢都是串流,要包一層 ------------------------------------

    async def _first(self, stream, timeout_s: float, what: str):
        """從訂閱式串流取第一筆。

        MAVSDK 幾乎所有查詢都是 async generator,沒有「查一次」的形式。
        直接 async for 在對方不回話時會永遠掛著,所以一律加逾時。
        """

        async def _take():
            async for item in stream:
                return item
            raise VehicleError(f"{what}:串流結束但沒有資料")

        try:
            return await asyncio.wait_for(_take(), timeout_s)
        except asyncio.TimeoutError as err:
            raise VehicleError(f"{what}:等 {timeout_s:.0f} 秒沒有回應") from err

    async def _gimbal_id(self) -> int:
        if self._gimbal_id_cache is None:
            gl = await self._first(
                self._drone.gimbal.gimbal_list(), self.discover_timeout_s, "雲台清單"
            )
            if not gl.gimbals:
                raise VehicleError("飛控回報沒有任何雲台")
            self._gimbal_id_cache = gl.gimbals[0].gimbal_id
        return self._gimbal_id_cache

    async def _camera_id(self) -> int:
        if self._camera_id_cache is None:
            cl = await self._first(
                self._drone.camera.camera_list(), self.discover_timeout_s, "相機清單"
            )
            if not cl.cameras:
                raise VehicleError("飛控回報沒有任何相機")
            self._camera_id_cache = cl.cameras[0].component_id
        return self._camera_id_cache

    def poll_interrupt(self) -> Interrupt | None:
        return self._pending.pop(0) if self._pending else None

    # --- 遙測背景任務 -----------------------------------------------------

    async def _watch_position(self) -> None:
        async for p in self._drone.telemetry.position():
            self._state.lat = p.latitude_deg
            self._state.lon = p.longitude_deg
            self._state.alt_rel_m = p.relative_altitude_m
            self._state.updated_at = self.clock.now()
            if self._home_amsl_m is None and abs(p.relative_altitude_m) < 1.0:
                self._home_amsl_m = p.absolute_altitude_m - p.relative_altitude_m

    async def _watch_flight_mode(self) -> None:
        """偵測「不是我們要求的」模式變更。

        這裡踩過一次:一開始把任何模式變更都當成中斷,結果 PX4 在
        goto_location 抵達目標後會自然進入 HOLD,任務每次都在第二個航點
        被誤判成 failsafe 中止。

        HOLD 是正常的到點行為,不是中斷。真正該當成中斷的是飛控自己切到
        RETURN_TO_LAUNCH 或 LAND——而且要排除是我們自己下的指令造成的。
        """
        async for m in self._drone.telemetry.flight_mode():
            mode = str(m)
            if (
                self._last_mode
                and mode != self._last_mode
                and mode in ("RETURN_TO_LAUNCH", "LAND")
                and mode not in self._requested_modes
            ):
                self._pending.append(Interrupt("failsafe.mode_changed", f"{self._last_mode} -> {mode}"))
            self._last_mode = mode
            self._state.mode = mode

    async def _watch_status_text(self) -> None:
        """PX4 的 failsafe 會以狀態訊息回報,比模式變更更早也更明確。

        這仍然是字串比對,不是結構化的 failsafe 旗標——真實產品應該直接讀
        飛控的 failsafe_flags(見 docs/10-flight-controller/02),這裡受限於
        MAVSDK 暴露的介面。
        """
        try:
            async for st in self._drone.telemetry.status_text():
                text = getattr(st, "text", "") or ""
                if "failsafe" in text.lower():
                    self._pending.append(Interrupt("failsafe.status_text", text))
        except Exception:  # noqa: BLE001 - 這條遙測不是每個版本都有,缺了不該讓服務掛掉
            return

    async def _watch_armed(self) -> None:
        async for a in self._drone.telemetry.armed():
            self._state.armed = a

    async def _watch_in_air(self) -> None:
        async for v in self._drone.telemetry.in_air():
            self._state.in_air = v

    async def _watch_battery(self) -> None:
        async for b in self._drone.telemetry.battery():
            self._state.battery_remaining = b.remaining_percent

    async def _watch_health(self) -> None:
        async for h in self._drone.telemetry.health():
            self._state.position_ok = bool(
                h.is_global_position_ok and h.is_home_position_ok
            )

    async def _wait_for_position_fix(self) -> None:
        deadline = self.clock.now() + self.connect_timeout_s
        while not self._state.position_ok or self._home_amsl_m is None:
            if self.clock.now() > deadline:
                raise VehicleError("等不到有效的全球定位(GPS fix)")
            await asyncio.sleep(0.5)
