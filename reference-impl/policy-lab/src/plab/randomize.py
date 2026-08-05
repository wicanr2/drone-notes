"""Domain randomization 的範圍定義。

docs/65-physical-ai-sim/02-sim-to-real.md 的原則:隨機範圍要涵蓋真實值
並略微超過,而上下界靠真機參數辨識來定,不是拍腦袋。

所以這裡每一項都寫成「標稱值 ± 比例」,標稱值就是參數辨識的結果。
把 nominal 換成你自己量到的值,範圍會跟著移動。

EVAL_RANGES 刻意比 TRAIN_RANGES 寬:驗收要在訓練沒涵蓋的條件下做,
否則只是在測策略記不記得住訓練集。
"""

from __future__ import annotations

from dataclasses import replace

import numpy as np

from .dynamics import Params

NOMINAL = Params()

# (欄位, 相對標稱值的下界比例, 上界比例)。絕對值型的欄位另外處理。
TRAIN_RANGES: dict[str, tuple[float, float]] = {
    "mass_kg": (0.85, 1.15),
    "inertia": (0.75, 1.25),
    "thrust_scale": (0.90, 1.10),
    "motor_tau_s": (0.60, 1.60),
}
TRAIN_ABS: dict[str, tuple[float, float]] = {
    "delay_steps": (1, 4),
    "theta_bias_rad": (-0.02, 0.02),
    "wind_accel": (-1.0, 1.0),
}

# 驗收用:每一項都比訓練範圍再外推一截
EVAL_RANGES: dict[str, tuple[float, float]] = {
    "mass_kg": (0.80, 1.25),
    "inertia": (0.70, 1.40),
    "thrust_scale": (0.85, 1.15),
    "motor_tau_s": (0.50, 2.00),
}
EVAL_ABS: dict[str, tuple[float, float]] = {
    "delay_steps": (1, 6),
    "theta_bias_rad": (-0.03, 0.03),
    "wind_accel": (-1.6, 1.6),
}


def sample(rng: np.random.Generator, *, evaluation: bool = False) -> Params:
    ranges = EVAL_RANGES if evaluation else TRAIN_RANGES
    absolute = EVAL_ABS if evaluation else TRAIN_ABS

    changes: dict[str, float | int] = {}
    for field, (lo, hi) in ranges.items():
        changes[field] = getattr(NOMINAL, field) * rng.uniform(lo, hi)
    for field, (lo, hi) in absolute.items():
        if field == "delay_steps":
            changes[field] = int(rng.integers(lo, hi + 1))
        else:
            changes[field] = float(rng.uniform(lo, hi))
    return replace(NOMINAL, **changes)


def describe() -> str:
    lines = ["項目                訓練範圍              驗收範圍"]
    for f in TRAIN_RANGES:
        t, e = TRAIN_RANGES[f], EVAL_RANGES[f]
        n = getattr(NOMINAL, f)
        lines.append(f"{f:18s} {n*t[0]:8.4f}~{n*t[1]:<8.4f}  {n*e[0]:8.4f}~{n*e[1]:<8.4f}")
    for f in TRAIN_ABS:
        t, e = TRAIN_ABS[f], EVAL_ABS[f]
        lines.append(f"{f:18s} {t[0]:8.3f}~{t[1]:<8.3f}  {e[0]:8.3f}~{e[1]:<8.3f}")
    return "\n".join(lines)
