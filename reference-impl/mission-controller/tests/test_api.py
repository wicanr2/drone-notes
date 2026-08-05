"""雲端任務服務 API 的行為測試。

重點只有一個:派工必須冪等。少了它,一次網路重試就等於飛兩趟。
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from mc.api import create_app
from mc.clock import RealClock
from mc.store import Store
from mc.vehicle.fake import FakeVehicle

LAT, LON = 24.7736, 121.0450

DEFINITION = {
    "name": "巡檢-最小",
    "actions": [
        {"type": "takeoff", "params": {"altitude_m": 10.0}},
        {"type": "goto", "params": {"lat": LAT + 0.0003, "lon": LON, "alt_rel_m": 10.0}},
        {"type": "land", "params": {}},
    ],
}


@pytest.fixture()
def client():
    store = Store()
    vehicle = FakeVehicle(clock=RealClock(), speed_mps=1000.0, photo_delay_s=0.0,
                          climb_mps=1000.0)
    with TestClient(create_app(store=store, vehicle=vehicle)) as c:
        c.store = store
        yield c


def test_health_lists_registered_actions(client):
    body = client.get("/health").json()
    assert body["ok"] is True
    assert {"takeoff", "goto", "land", "orbit_photo", "rtl"} <= set(body["actions"])


def test_unknown_action_type_is_rejected(client):
    bad = {"name": "壞的", "actions": [{"type": "teleport", "params": {}}]}
    assert client.post("/definitions", json=bad).status_code == 400


def test_dispatch_is_idempotent(client):
    d = client.post("/definitions", json=DEFINITION).json()
    plan_body = {"definition_id": d["id"], "definition_version": d["version"],
                 "id": "plan-fixed-001", "version": 1}

    first = client.post("/plans", json=plan_body).json()
    second = client.post("/plans", json=plan_body).json()

    assert first["accepted"] is True
    assert second["accepted"] is False
    assert second["why"] == "duplicate_dispatch"
    assert second["execution_id"] == first["execution_id"]


def test_new_version_creates_a_new_execution(client):
    d = client.post("/definitions", json=DEFINITION).json()
    base = {"definition_id": d["id"], "definition_version": d["version"], "id": "plan-fixed-002"}

    v1 = client.post("/plans", json={**base, "version": 1}).json()
    v2 = client.post("/plans", json={**base, "version": 2}).json()

    assert v1["accepted"] and v2["accepted"]
    assert v1["execution_id"] != v2["execution_id"]


def test_execution_query_reports_as_of_and_events(client):
    d = client.post("/definitions", json=DEFINITION).json()
    r = client.post("/plans", json={"definition_id": d["id"], "definition_version": d["version"]}).json()

    got = client.get(f"/executions/{r['execution_id']}").json()
    assert got["execution"]["plan_id"] == r["plan_id"]
    assert "as_of_seq" in got          # 查詢一律附「這份資料是什麼時候的」

    events = client.get(f"/executions/{r['execution_id']}/events").json()
    assert events["count"] >= 1


def test_dispatch_with_unknown_definition_is_404(client):
    resp = client.post("/plans", json={"definition_id": "def-nope", "definition_version": 1})
    assert resp.status_code == 404
