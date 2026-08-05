"""機載任務執行器。

對應 docs/40-mission-control/02-onboard-executor.md 的執行迴圈。
三個設計重點:

1. 每次狀態變更「先存檔再發事件」。反過來的話,發完事件就當機,
   雲端會以為某個動作完成了,而機上重啟後不知道。
2. 中斷監看與動作執行「同時進行」,不是在動作之間檢查。一個 goto
   可能跑三分鐘,只在邊界檢查等於那三分鐘對 failsafe 沒有反應。
3. 恢復時「先確認飛機實際狀態」再決定續行,不能假設它還在中斷時的位置。
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from .actions import Action, Context, build
from .clock import Clock
from .models import (
    Execution,
    ExecutionEvent,
    ExecutionState,
    MissionDefinition,
    MissionPlan,
    ResumePolicy,
)
from .store import Store
from .vehicle.base import Interrupt, Vehicle, VehicleError


class Interrupted(Exception):
    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(f"{reason}: {detail}" if detail else reason)
        self.reason = reason
        self.detail = detail


# 哪些中斷可以在條件恢復後續飛,哪些直接結束。
_RESUMABLE = {"operator_takeover"}


@dataclass
class Executor:
    vehicle: Vehicle
    clock: Clock
    store: Store
    poll_interval_s: float = 0.2

    # 中斷之後何時可以續飛,是應用層的決定(等操作者交還控制、等電量回復、
    # 等雲端核准…),所以做成可注入的判斷式。預設立即續行。
    resume_predicate: Callable[[], Awaitable[bool]] | None = None
    resume_timeout_s: float = 120.0

    async def _wait_for_resume(self) -> bool:
        if self.resume_predicate is None:
            return True
        deadline = self.clock.now() + self.resume_timeout_s
        while not await self.resume_predicate():
            if self.clock.now() > deadline:
                return False
            await self.clock.sleep(self.poll_interval_s)
        return True

    async def run(
        self,
        plan: MissionPlan,
        definition: MissionDefinition,
        execution: Execution | None = None,
    ) -> Execution:
        ex = execution or self.store.load_execution_for(plan) or Execution(
            plan_id=plan.id,
            plan_version=plan.version,
            definition_id=definition.id,
            definition_version=definition.version,
            vehicle_id=plan.vehicle_id,
        )
        ctx = Context(vehicle=self.vehicle, clock=self.clock, emit=lambda e, d: self._emit(ex, e, d))

        if ex.state in (ExecutionState.COMPLETED, ExecutionState.ABORTED, ExecutionState.REJECTED):
            return ex

        if ex.state is ExecutionState.RECEIVED:
            ex.started_at = self.clock.now()
            self._transition(ex, ExecutionState.PREPARING, "execution_started", {})

        # 從中斷恢復時,先問飛機現在到底在哪、是什麼狀態,再決定怎麼續。
        st = await self.vehicle.state()
        self._emit(ex, "vehicle_state_checked", {"in_air": st.in_air, "mode": st.mode,
                                                 "alt_rel_m": round(st.alt_rel_m, 2)})

        self._transition(ex, ExecutionState.RUNNING, "execution_running", {})

        while ex.action_index < len(definition.actions):
            spec = definition.actions[ex.action_index]
            action = build(spec)

            check = action.preconditions(ctx)
            if not check.ok:
                await self._abort(ex, action, ctx, "precondition_failed", check.reason)
                return ex

            self._emit(ex, "action_started", {"action": action.name, "index": ex.action_index})

            try:
                await self._run_action_with_watchdog(action, ctx)
            except Interrupted as itr:
                await self._safe_abort_hook(action, ctx, itr.reason)
                self._transition(ex, ExecutionState.PAUSED, "execution_paused",
                                 {"reason": itr.reason, "detail": itr.detail})
                if itr.reason not in _RESUMABLE or not await self._wait_for_resume():
                    self._finish(ex, ExecutionState.ABORTED, itr.reason)
                    return ex
                self._apply_resume_policy(ex, action)
                self._transition(ex, ExecutionState.RUNNING, "execution_resumed",
                                 {"policy": action.resume_policy.value})
                continue
            except VehicleError as err:
                await self._safe_abort_hook(action, ctx, "vehicle_error")
                self._emit(ex, "vehicle_rejected", {"action": action.name, "error": str(err)})
                self._finish(ex, ExecutionState.ABORTED, f"vehicle_error: {err}")
                return ex

            self._emit(ex, "action_completed", {"action": action.name, "index": ex.action_index})
            ex.action_index += 1
            self.store.save_execution(ex)

        self._finish(ex, ExecutionState.COMPLETED, None)
        return ex

    # --- 內部 -------------------------------------------------------------

    async def _run_action_with_watchdog(self, action: Action, ctx: Context) -> None:
        """執行動作,同時持續監看中斷與逾時。"""
        deadline = self.clock.now() + action.timeout_s
        task = asyncio.ensure_future(action.execute(ctx))
        try:
            while True:
                itr = self.vehicle.poll_interrupt()
                if itr is not None:
                    raise Interrupted(_reason_of(itr), itr.detail)
                if task.done():
                    task.result()          # 讓動作內部的例外浮上來
                    break
                if self.clock.now() > deadline:
                    raise Interrupted("timeout", f"{action.name} 超過 {action.timeout_s}s")
                await self.clock.sleep(self.poll_interval_s)

            # 完成判定看實際狀態,不看「execute 有沒有回來」。
            while not await action.is_complete(ctx):
                if self.clock.now() > deadline:
                    raise Interrupted("timeout", f"{action.name} 完成判定逾時")
                await self.clock.sleep(self.poll_interval_s)
        finally:
            if not task.done():
                task.cancel()
                try:
                    await task
                except (asyncio.CancelledError, Exception):
                    pass

    async def _safe_abort_hook(self, action: Action, ctx: Context, reason: str) -> None:
        """on_abort 不能讓收尾流程再爆一次。"""
        try:
            await action.on_abort(ctx, reason)
        except Exception as err:  # noqa: BLE001 - 收尾路徑刻意吞掉例外並記錄
            ctx.emit("abort_hook_failed", {"action": action.name, "error": str(err)})

    async def _abort(self, ex: Execution, action: Action, ctx: Context, reason: str, detail: str) -> None:
        await self._safe_abort_hook(action, ctx, reason)
        self._emit(ex, "action_rejected", {"action": action.name, "reason": reason, "detail": detail})
        self._finish(ex, ExecutionState.ABORTED, f"{reason}: {detail}")

    def _apply_resume_policy(self, ex: Execution, action: Action) -> None:
        if action.resume_policy is ResumePolicy.SKIP:
            ex.action_index += 1
        # RESTART 與 CONTINUE 都停在同一個 index:差別在動作自己的內部狀態,
        # 而 build() 每次都會產生新的實例,所以 RESTART 天然成立。
        self.store.save_execution(ex)

    def _transition(self, ex: Execution, state: ExecutionState, event: str, data: dict) -> None:
        ex.state = state
        self.store.save_execution(ex)      # 先存檔
        self._emit(ex, event, data)        # 再發事件

    def _finish(self, ex: Execution, state: ExecutionState, reason: str | None) -> None:
        ex.state = state
        ex.reason = reason
        ex.ended_at = self.clock.now()
        self.store.save_execution(ex)
        self._emit(ex, "execution_finished", {"state": state.value, "reason": reason})

    def _emit(self, ex: Execution, event: str, data: dict) -> None:
        evt = ExecutionEvent(execution_id=ex.id, seq=ex.next_seq(), event=event,
                             at=self.clock.now(), data=data)
        self.store.save_execution(ex)      # seq 要跟狀態一起持久化,重啟後不歸零
        self.store.append_event(evt)


def _reason_of(itr: Interrupt) -> str:
    if itr.kind.startswith("failsafe."):
        return "failsafe"
    if itr.kind == "operator_takeover":
        return "operator_takeover"
    if itr.kind == "operator_cancel":
        return "operator_cancel"
    return itr.kind
