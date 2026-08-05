#!/usr/bin/env python3
"""情境執行器:讀一份宣告式的情境檔,派工,等結果,斷言。

對應 docs/60-simulation-and-testing/03-ci-and-regression.md 的「情境即程式碼」。

已實作:events(含次數)與 final_state 的斷言。
未實作:metrics 斷言與 inject(故障注入)——那兩項需要解析 SITL 的飛行紀錄
與一個注入介面,不在這個骨架的範圍內。文件裡有完整格式,這裡不假裝支援。

用法:
    python scripts/run_scenario.py scenarios/01-basic-mission.yaml
    python scripts/run_scenario.py scenarios/*.yaml --base-url http://localhost:8000
"""

from __future__ import annotations

import argparse
import glob
import sys
import time
from pathlib import Path

import httpx
import yaml

UNSUPPORTED_KEYS = {"inject", "metrics"}


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def run_one(scenario: dict, base_url: str, name: str) -> tuple[bool, list[str]]:
    problems: list[str] = []

    for key in UNSUPPORTED_KEYS & set(scenario) | UNSUPPORTED_KEYS & set(scenario.get("expect", {})):
        print(f"  [略過] 這個骨架尚未實作 `{key}`,該段不會被驗證")

    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        d = client.post("/definitions", json=scenario["mission"])
        d.raise_for_status()
        definition = d.json()

        p = client.post("/plans", json={
            "definition_id": definition["id"],
            "definition_version": definition["version"],
            "vehicle_id": scenario.get("vehicle_id", "sim-01"),
        })
        p.raise_for_status()
        dispatch = p.json()
        if not dispatch.get("accepted"):
            return False, [f"派工被拒: {dispatch}"]

        execution_id = dispatch["execution_id"]
        deadline = time.monotonic() + float(scenario.get("timeout_s", 180))
        state = "unknown"
        while time.monotonic() < deadline:
            got = client.get(f"/executions/{execution_id}").json()
            state = got["execution"]["state"]
            if state in ("completed", "aborted", "rejected"):
                break
            time.sleep(1.0)
        else:
            problems.append(f"逾時:{scenario.get('timeout_s', 180)} 秒後仍停在 {state}")

        events = client.get(f"/executions/{execution_id}/events").json()["events"]

    expect = scenario.get("expect", {})
    want_state = expect.get("final_state")
    if want_state and state != want_state:
        problems.append(f"最終狀態:期望 {want_state},實際 {state}")

    names = [e["event"] for e in events]
    for rule in expect.get("events", []):
        want = rule["event"]
        count = names.count(want)
        if "count" in rule:
            if count != rule["count"]:
                problems.append(f"事件 {want}:期望 {rule['count']} 次,實際 {count} 次")
        elif count == 0:
            problems.append(f"事件 {want}:一次都沒出現")

    print(f"  執行 {execution_id} → {state},事件 {len(events)} 筆")
    if problems:
        print("  最後 10 筆事件:", ", ".join(names[-10:]))
    return not problems, problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("patterns", nargs="+")
    ap.add_argument("--base-url", default="http://localhost:8000")
    args = ap.parse_args()

    paths = sorted({Path(p) for pat in args.patterns for p in glob.glob(pat)})
    if not paths:
        print("找不到任何情境檔", file=sys.stderr)
        return 2

    failed = 0
    for path in paths:
        scenario = load(path)
        name = scenario.get("name", path.stem)
        print(f"[情境] {name} ({path})")
        ok, problems = run_one(scenario, args.base_url, name)
        if ok:
            print("  通過\n")
        else:
            failed += 1
            for p in problems:
                print(f"  失敗:{p}")
            print()

    total = len(paths)
    print(f"{total - failed}/{total} 個情境通過")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
