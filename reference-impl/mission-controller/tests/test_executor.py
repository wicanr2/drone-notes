"""執行器的行為測試。

這些測試全部用 FakeVehicle + FakeClock,所以一趟「十分鐘」的任務在
毫秒內跑完,而且完全確定性——這就是 docs/40 說的「時間、飛控介面、
中斷、持久化四者可注入 → 確定性可測」。
"""

from __future__ import annotations

import pytest

from mc.clock import FakeClock
from mc.executor import Executor
from mc.models import (
    ActionSpec,
    Execution,
    ExecutionState,
    MissionDefinition,
    MissionPlan,
)
from mc.store import Store
from mc.vehicle.fake import FakeVehicle

LAT, LON = 24.7736, 121.0450


def _simple_mission() -> MissionDefinition:
    return MissionDefinition(
        name="起飛-飛四點-降落",
        actions=[
            ActionSpec(type="takeoff", params={"altitude_m": 10.0}),
            ActionSpec(type="goto", params={"lat": LAT + 0.0005, "lon": LON, "alt_rel_m": 10.0}),
            ActionSpec(type="goto", params={"lat": LAT + 0.0005, "lon": LON + 0.0005, "alt_rel_m": 10.0}),
            ActionSpec(type="land"),
        ],
    )


def _orbit_mission() -> MissionDefinition:
    return MissionDefinition(
        name="環繞拍照",
        actions=[
            ActionSpec(type="takeoff", params={"altitude_m": 15.0}),
            ActionSpec(type="orbit_photo",
                       params={"lat": LAT, "lon": LON, "alt_rel_m": 15.0,
                               "radius_m": 10.0, "shots": 8, "settle_s": 1.0}),
            ActionSpec(type="land"),
        ],
    )


def _setup(mission: MissionDefinition, **veh_kwargs):
    clock = FakeClock()
    vehicle = FakeVehicle(clock=clock, **veh_kwargs)
    vehicle._state.lat, vehicle._state.lon = LAT, LON
    store = Store()
    store.save_definition(mission)
    plan = MissionPlan(definition_id=mission.id, definition_version=mission.version, vehicle_id="sim-01")
    store.save_plan(plan)
    ex = Execution(plan_id=plan.id, plan_version=plan.version, definition_id=mission.id,
                   definition_version=mission.version, vehicle_id="sim-01")
    store.save_execution(ex)
    return clock, vehicle, store, plan, ex


async def test_happy_path_completes_and_emits_expected_events():
    mission = _simple_mission()
    clock, vehicle, store, plan, ex = _setup(mission)

    result = await Executor(vehicle=vehicle, clock=clock, store=store).run(plan, mission, ex)

    assert result.state is ExecutionState.COMPLETED
    names = store.event_names(result.id)
    assert names.count("action_started") == 4
    assert names.count("action_completed") == 4
    assert names[-1] == "execution_finished"
    # 動作順序要對得上,不是只看有沒有跑完
    called = [c[0] for c in vehicle.calls]
    assert called == ["arm", "takeoff", "goto", "goto", "land"]


async def test_seq_is_monotonic_and_events_are_ordered():
    mission = _simple_mission()
    clock, vehicle, store, plan, ex = _setup(mission)
    result = await Executor(vehicle=vehicle, clock=clock, store=store).run(plan, mission, ex)

    seqs = [e.seq for e in store.events(result.id)]
    assert seqs == sorted(seqs) == list(range(1, len(seqs) + 1))


async def test_failsafe_during_action_aborts_and_records_pause():
    mission = _simple_mission()
    clock, vehicle, store, plan, ex = _setup(mission, speed_mps=1.0)
    # 第 5 秒(虛擬時間)注入低電量 failsafe,此時還在第一段航程中
    vehicle.schedule_interrupt(5.0, "failsafe.low_battery", "battery 18%")

    result = await Executor(vehicle=vehicle, clock=clock, store=store).run(plan, mission, ex)

    assert result.state is ExecutionState.ABORTED
    assert result.reason == "failsafe"
    names = store.event_names(result.id)
    assert "execution_paused" in names
    assert "land" not in [c[0] for c in vehicle.calls]   # 沒有繼續往下做


async def test_operator_takeover_is_resumable():
    mission = _simple_mission()
    clock, vehicle, store, plan, ex = _setup(mission, speed_mps=1.0)
    # 第 20 秒:起飛(10 m / 2 m·s⁻¹ = 5 s)早就完成,此時在第一段航程中
    vehicle.schedule_interrupt(20.0, "operator_takeover", "pilot took control")

    result = await Executor(vehicle=vehicle, clock=clock, store=store).run(plan, mission, ex)

    assert result.state is ExecutionState.COMPLETED
    names = store.event_names(result.id)
    assert "execution_paused" in names and "execution_resumed" in names
    # 恢復時起飛不會重做:動作自己看到已經在空中就跳過內部步驟
    assert [c[0] for c in vehicle.calls].count("arm") == 1


async def test_orbit_photo_restarts_from_scratch_after_interrupt():
    """RESTART 政策:中斷後整組重來,最終仍然要有完整的 8 張。"""
    mission = _orbit_mission()
    clock, vehicle, store, plan, ex = _setup(mission, speed_mps=3.0)
    # 第 19 秒:已經拍了兩張,中斷後這兩張作廢,整組重來
    vehicle.schedule_interrupt(19.0, "operator_takeover", "")

    result = await Executor(vehicle=vehicle, clock=clock, store=store).run(plan, mission, ex)

    assert result.state is ExecutionState.COMPLETED
    photo_events = [e for e in store.events(result.id) if e.event == "photo_captured"]
    # 中斷前拍的那幾張作廢,重來後這一輪一定有連續 8 張
    final_round = [e for e in photo_events if e.data["index"] == 7]
    assert len(final_round) == 1
    assert len(photo_events) > 8          # 表示確實重來過
    assert vehicle.calls[-1][0] == "land"


async def test_interrupt_during_takeoff_reruns_it_instead_of_skipping():
    """中斷打在起飛「途中」,飛機還在地上。

    這是把 takeoff 的恢復政策從 SKIP 改成 CONTINUE 的原因:
    盲目跳過會讓後面的動作在「以為已經在空中」的錯誤前提下執行。
    """
    mission = _simple_mission()
    clock, vehicle, store, plan, ex = _setup(mission, climb_mps=0.5, speed_mps=50.0)
    vehicle.schedule_interrupt(3.0, "operator_takeover", "")   # 10 m / 0.5 m·s⁻¹ = 20 s,還沒到頂

    result = await Executor(vehicle=vehicle, clock=clock, store=store).run(plan, mission, ex)

    assert result.state is ExecutionState.COMPLETED
    called = [c[0] for c in vehicle.calls]
    assert called.count("takeoff") == 2      # 重跑了起飛
    assert called[-1] == "land"              # 而且後續動作有正常執行
    st = await vehicle.state()
    assert not st.in_air


async def test_precondition_failure_aborts_before_doing_anything():
    mission = MissionDefinition(
        name="不合理的高度",
        actions=[ActionSpec(type="takeoff", params={"altitude_m": 500.0})],
    )
    clock, vehicle, store, plan, ex = _setup(mission)

    result = await Executor(vehicle=vehicle, clock=clock, store=store).run(plan, mission, ex)

    assert result.state is ExecutionState.ABORTED
    assert "altitude_m" in (result.reason or "")
    assert vehicle.calls == []       # 前置檢查沒過就完全沒有動到飛機


async def test_arm_rejection_is_propagated_not_retried():
    mission = _simple_mission()
    clock, vehicle, store, plan, ex = _setup(mission, reject_arm_reason="preflight: GPS not ready")

    result = await Executor(vehicle=vehicle, clock=clock, store=store).run(plan, mission, ex)

    assert result.state is ExecutionState.ABORTED
    assert "GPS not ready" in (result.reason or "")
    assert [c[0] for c in vehicle.calls].count("arm") == 1     # 沒有重試迴圈


async def test_restart_after_process_death_continues_from_persisted_state():
    """執行器行程被殺掉之後,用同一份持久化狀態重新啟動。

    驗兩件事:進度不從頭來、seq 不歸零。
    """
    mission = _simple_mission()
    clock, vehicle, store, plan, ex = _setup(mission, speed_mps=1.0)
    vehicle.schedule_interrupt(20.0, "failsafe.low_battery", "")
    first = await Executor(vehicle=vehicle, clock=clock, store=store).run(plan, mission, ex)
    assert first.state is ExecutionState.ABORTED
    seq_before = first.seq
    index_before = first.action_index
    assert index_before > 0        # 起飛已經完成

    # 模擬重啟:新的執行器、新的載具連線,但同一個 store
    reborn = store.get_execution(first.id)
    reborn.state = ExecutionState.RUNNING          # 營運上由人或雲端決定要不要續飛
    vehicle2 = FakeVehicle(clock=clock)
    vehicle2._state.in_air = True
    vehicle2._state.armed = True
    vehicle2._state.alt_rel_m = 10.0
    vehicle2._state.lat, vehicle2._state.lon = LAT, LON

    second = await Executor(vehicle=vehicle2, clock=clock, store=store).run(plan, mission, reborn)

    assert second.state is ExecutionState.COMPLETED
    assert second.seq > seq_before                  # 序號延續,不歸零
    # 恢復時第一件事是確認飛機實際狀態
    assert "vehicle_state_checked" in store.event_names(second.id)
    assert [c[0] for c in vehicle2.calls].count("arm") == 0   # 已經在空中,不重新起飛


@pytest.mark.parametrize("action_type", ["takeoff", "goto", "orbit_photo", "land", "rtl"])
def test_every_registered_action_is_buildable(action_type: str):
    from mc.actions import REGISTRY, build

    spec = ActionSpec(type=action_type, params={"lat": LAT, "lon": LON})
    action = build(spec)
    assert action.name in REGISTRY or action.name == action_type
    assert action.timeout_s > 0
