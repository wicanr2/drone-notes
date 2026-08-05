"""可注入的時鐘。

不要直接呼叫 time.time() 與 asyncio.sleep():測試要能把一個十分鐘的任務
在幾秒內跑完,而且要能精確控制「第 60 秒注入低電量」這種事件。
理由見 docs/40-mission-control/02-onboard-executor.md 的「怎麼讓它可測試」。
"""

from __future__ import annotations

import asyncio
import time
from typing import Protocol


class Clock(Protocol):
    def now(self) -> float: ...
    async def sleep(self, seconds: float) -> None: ...


class RealClock:
    def now(self) -> float:
        return time.monotonic()

    async def sleep(self, seconds: float) -> None:
        await asyncio.sleep(seconds)


class FakeClock:
    """虛擬時間。sleep 不真的等待,只把時間往前推。

    每次推進都讓出一次事件迴圈,好讓其他協程有機會反應
    (例如注入器在虛擬時間到達某點時觸發中斷)。
    """

    def __init__(self, start: float = 0.0, step_yield: bool = True) -> None:
        self._t = start
        self._step_yield = step_yield

    def now(self) -> float:
        return self._t

    async def sleep(self, seconds: float) -> None:
        self._t += seconds
        if self._step_yield:
            await asyncio.sleep(0)

    def advance(self, seconds: float) -> None:
        self._t += seconds
