"""雲台與相機的介面層測試。

沒有實體雲台與相機,所以這裡驗的是**呼叫序列與簽章**,不是飛行行為。
stub 的方法簽章逐字照 MAVSDK 3.17.2 抄(見 docs/20-protocols/03),
所以簽章寫錯——少帶 gimbal_id、忘了 component_id——測試會直接爆。

驗不到的部分寫在 README 的驗證狀態,不要把這裡的綠燈當成「接得上實機」。
"""

from __future__ import annotations

import asyncio
import sys
import types

import pytest

from mc.vehicle.base import VehicleError

# --- 假的 mavsdk 子模組 ---------------------------------------------------
# MavsdkVehicle 是在方法內部 from mavsdk.gimbal import ...,所以只要在
# import 之前把假模組塞進 sys.modules 就攔得到,不必真的裝 mavsdk。


class _ControlMode:
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    NONE = "NONE"


class _GimbalMode:
    YAW_FOLLOW = "YAW_FOLLOW"
    YAW_LOCK = "YAW_LOCK"


class _SendMode:
    ONCE = "ONCE"
    STREAM = "STREAM"


class _CameraMode:
    UNKNOWN = "UNKNOWN"
    PHOTO = "PHOTO"
    VIDEO = "VIDEO"


def _install_fake_mavsdk() -> None:
    gimbal = types.ModuleType("mavsdk.gimbal")
    gimbal.ControlMode = _ControlMode
    gimbal.GimbalMode = _GimbalMode
    gimbal.SendMode = _SendMode
    camera = types.ModuleType("mavsdk.camera")
    camera.Mode = _CameraMode
    root = sys.modules.setdefault("mavsdk", types.ModuleType("mavsdk"))
    root.gimbal = gimbal
    root.camera = camera
    sys.modules["mavsdk.gimbal"] = gimbal
    sys.modules["mavsdk.camera"] = camera


_install_fake_mavsdk()

from mc.vehicle.mavsdk_vehicle import MavsdkVehicle  # noqa: E402


# --- 照 MAVSDK 3.17.2 簽章打造的 stub --------------------------------------


class _Item:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class _GimbalStub:
    def __init__(self, calls, gimbals=(3,)):
        self.calls = calls
        self._gimbals = gimbals

    async def gimbal_list(self):  # 串流
        yield _Item(gimbals=[_Item(gimbal_id=g) for g in self._gimbals])

    async def take_control(self, gimbal_id, control_mode):
        self.calls.append(("take_control", gimbal_id, control_mode))

    async def set_angles(self, gimbal_id, roll_deg, pitch_deg, yaw_deg, gimbal_mode, send_mode):
        self.calls.append(("set_angles", gimbal_id, roll_deg, pitch_deg, yaw_deg, gimbal_mode, send_mode))

    async def release_control(self, gimbal_id):
        self.calls.append(("release_control", gimbal_id))


class _CameraStub:
    def __init__(self, calls, cameras=(100,), success=True, emit_info=True):
        self.calls = calls
        self._cameras = cameras
        self._success = success
        self._emit_info = emit_info

    async def camera_list(self):  # 串流
        yield _Item(cameras=[_Item(component_id=c) for c in self._cameras])

    async def capture_info(self):  # 串流
        if not self._emit_info:
            await asyncio.sleep(3600)
        yield _Item(is_success=self._success, index=7, file_url="ftp://cam/IMG_0007.jpg")

    async def set_mode(self, component_id, mode):
        self.calls.append(("set_mode", component_id, mode))

    async def take_photo(self, component_id):
        self.calls.append(("take_photo", component_id))


class _DroneStub:
    def __init__(self, calls, **kw):
        self.gimbal = _GimbalStub(calls, **kw.pop("gimbal", {}))
        self.camera = _CameraStub(calls, **kw.pop("camera", {}))


def _vehicle(calls, **kw):
    v = MavsdkVehicle(has_gimbal=True, has_camera=True, photo_timeout_s=1.0, discover_timeout_s=1.0)
    v._drone = _DroneStub(calls, **kw)
    return v


# --- 測試 -----------------------------------------------------------------


@pytest.mark.asyncio
async def test_gimbal_takes_control_before_setting_angles():
    """少了 take_control,實機會「接受指令但雲台不動」,所以順序要鎖住。"""
    calls: list = []
    v = _vehicle(calls)
    await v.set_gimbal(-30.0, 45.0)

    assert calls[0][0] == "take_control"
    assert calls[1][0] == "set_angles"
    # gimbal_id 來自 gimbal_list,不是寫死的 0
    assert calls[0][1] == 3 and calls[1][1] == 3
    # roll 補 0,pitch/yaw 照傳,模式為相對機頭、單次送出
    assert calls[1][2:] == (0.0, -30.0, 45.0, _GimbalMode.YAW_FOLLOW, _SendMode.ONCE)


@pytest.mark.asyncio
async def test_gimbal_control_taken_once_then_released_on_close():
    calls: list = []
    v = _vehicle(calls)
    await v.set_gimbal(-10.0, 0.0)
    await v.set_gimbal(-20.0, 0.0)
    await v.close()

    assert [c[0] for c in calls].count("take_control") == 1
    assert calls[-1] == ("release_control", 3)


@pytest.mark.asyncio
async def test_capture_photo_returns_file_url_after_confirmation():
    """契約是「已確認存檔」才回傳,所以 take_photo 之後還要等 capture_info。"""
    calls: list = []
    v = _vehicle(calls)
    out = await v.capture_photo()

    assert out == "ftp://cam/IMG_0007.jpg"
    assert [c[0] for c in calls] == ["set_mode", "take_photo"]
    assert calls[0][1] == 100 and calls[1][1] == 100  # component_id 來自 camera_list


@pytest.mark.asyncio
async def test_capture_photo_raises_when_camera_reports_failure():
    v = _vehicle([], camera={"success": False})
    with pytest.raises(VehicleError, match="拍照失敗"):
        await v.capture_photo()


@pytest.mark.asyncio
async def test_capture_photo_times_out_instead_of_hanging():
    """沒有回報時要逾時,不能停在 async for 上等一個不會來的東西。"""
    v = _vehicle([], camera={"emit_info": False})
    with pytest.raises(VehicleError, match="沒有回應"):
        await v.capture_photo()


@pytest.mark.asyncio
async def test_no_gimbal_configured_is_rejected_before_touching_the_link():
    calls: list = []
    v = _vehicle(calls)
    v.has_gimbal = False
    with pytest.raises(VehicleError, match="has_gimbal=False"):
        await v.set_gimbal(0.0, 0.0)
    assert calls == []


@pytest.mark.asyncio
async def test_empty_gimbal_list_is_an_error_not_a_default_id():
    v = _vehicle([], gimbal={"gimbals": ()})
    with pytest.raises(VehicleError, match="沒有任何雲台"):
        await v.set_gimbal(0.0, 0.0)
