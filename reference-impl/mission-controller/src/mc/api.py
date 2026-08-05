"""雲端任務服務的最小 API。

只做三件跟一般 CRUD 不同的事,其餘刻意留白:
1. 派工是冪等的(計畫 ID + 版本當鍵),重送不會飛兩趟
2. 下發的是意圖,執行器有權拒絕,拒絕帶原因
3. 狀態由 append-only 的事件投影而來,查詢一律附「這份資料是什麼時候的」
"""

from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .actions import REGISTRY
from .clock import RealClock
from .executor import Executor
from .models import ActionSpec, Execution, MissionDefinition, MissionPlan
from .store import Store
from .vehicle.base import Vehicle
from .vehicle.fake import FakeVehicle


class DefinitionIn(BaseModel):
    name: str
    actions: list[ActionSpec]
    version: int = 1


class PlanIn(BaseModel):
    definition_id: str
    definition_version: int = 1
    vehicle_id: str = "sim-01"
    version: int = 1
    id: str | None = None
    constraints: dict[str, Any] = {}


def build_vehicle() -> Vehicle:
    """依環境變數決定接哪個後端。

    預設是假飛控,所以這個服務不需要 PX4 就能起來並跑完整條流程。
    設 MC_VEHICLE=mavsdk 才會去連真的 SITL 或實機。
    """
    backend = os.environ.get("MC_VEHICLE", "fake")
    if backend == "mavsdk":
        from .vehicle.mavsdk_vehicle import MavsdkVehicle

        return MavsdkVehicle(
            system_address=os.environ.get("MC_MAVSDK_ADDRESS", "udpin://0.0.0.0:14540"),
            clock=RealClock(),
            # SITL 開機到取得定位可能要一分鐘以上,連線等待要給得夠寬。
            connect_timeout_s=float(os.environ.get("MC_CONNECT_TIMEOUT", "300")),
        )
    vehicle = FakeVehicle(clock=RealClock(), speed_mps=float(os.environ.get("MC_FAKE_SPEED", "20")))
    # 預設起始點對齊 PX4 SITL 的預設 home,這樣同一份情境檔在假飛控與
    # 真 SITL 兩種後端下都是合理的距離。
    vehicle._state.lat = float(os.environ.get("MC_FAKE_HOME_LAT", "47.397742"))
    vehicle._state.lon = float(os.environ.get("MC_FAKE_HOME_LON", "8.545594"))
    return vehicle


def create_app(store: Store | None = None, vehicle: Vehicle | None = None) -> FastAPI:
    state: dict[str, Any] = {}

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        state["store"] = store or Store(os.environ.get("MC_DB", "/data/mc.sqlite3"))
        state["vehicle"] = vehicle or build_vehicle()
        await state["vehicle"].connect()
        state["tasks"] = set()
        yield
        for t in state["tasks"]:
            t.cancel()
        await state["vehicle"].close()

    app = FastAPI(title="mission-controller", version="0.1.0", lifespan=lifespan)

    @app.get("/health")
    async def health() -> dict:
        return {"ok": True, "actions": sorted(REGISTRY)}

    @app.post("/definitions", status_code=201)
    async def create_definition(body: DefinitionIn) -> MissionDefinition:
        for a in body.actions:
            if a.type not in REGISTRY:
                raise HTTPException(400, f"未知的動作型別: {a.type}")
        d = MissionDefinition(name=body.name, actions=body.actions, version=body.version)
        state["store"].save_definition(d)
        return d

    @app.post("/plans", status_code=202)
    async def dispatch(body: PlanIn) -> dict:
        st: Store = state["store"]
        definition = st.get_definition(body.definition_id, body.definition_version)
        if definition is None:
            raise HTTPException(404, "找不到該版本的任務定義")

        plan = MissionPlan(
            **({"id": body.id} if body.id else {}),
            version=body.version,
            definition_id=body.definition_id,
            definition_version=body.definition_version,
            vehicle_id=body.vehicle_id,
            constraints=body.constraints,
        )
        accepted = st.save_plan(plan)
        if not accepted:
            existing = st.load_execution_for(plan)
            return {"accepted": False, "why": "duplicate_dispatch",
                    "plan_id": plan.id, "version": plan.version,
                    "execution_id": existing.id if existing else None}

        execution = Execution(
            plan_id=plan.id, plan_version=plan.version,
            definition_id=definition.id, definition_version=definition.version,
            vehicle_id=plan.vehicle_id,
        )
        st.save_execution(execution)

        executor = Executor(vehicle=state["vehicle"], clock=RealClock(), store=st)
        task = asyncio.create_task(executor.run(plan, definition, execution))
        state["tasks"].add(task)
        task.add_done_callback(state["tasks"].discard)

        return {"accepted": True, "plan_id": plan.id, "version": plan.version,
                "execution_id": execution.id}

    @app.get("/executions/{execution_id}")
    async def get_execution(execution_id: str) -> dict:
        ex = state["store"].get_execution(execution_id)
        if ex is None:
            raise HTTPException(404, "找不到該執行")
        return {"execution": ex.model_dump(),
                "as_of_seq": ex.seq,
                "note": "飛行期間權威在機上,這份是投影出來的副本"}

    @app.get("/executions/{execution_id}/events")
    async def get_events(execution_id: str) -> dict:
        events = state["store"].events(execution_id)
        return {"count": len(events), "events": [e.model_dump() for e in events]}

    return app


app = create_app()
