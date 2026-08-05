"""訓練環境與驗收環境。

這兩個類別刻意分開,而且驗收環境用的是更寬的參數範圍加上故障注入 ——
docs/65 的說法是「訓練環境不能當驗證環境,否則只是在測策略記不記得住
訓練集」。分成兩個類別是為了讓這件事在程式碼結構上就成立,不是靠紀律。

驗收用的指標沿用 docs/60-simulation-and-testing/03 那一組:位置誤差 p95、
最大傾角、著陸/終端速度、控制飽和比例。reward 只在訓練裡用,不參與驗收。
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .dynamics import PlanarQuad, Params, State
from .policy import GuardedPolicy
from .randomize import sample


@dataclass
class Episode:
    """一次 rollout 的結果。reward 與 metrics 分開放,避免混用。"""

    reward: float
    crashed: bool
    pos_err_p95_m: float
    pos_err_max_m: float
    max_tilt_deg: float
    terminal_speed_mps: float
    clamp_rate: float
    ood_rate: float


def rollout(
    guarded: GuardedPolicy,
    params: Params,
    *,
    target: np.ndarray,
    start: State,
    dt: float = 0.01,
    horizon: int = 400,
    fault_at: int | None = None,
    fault_thrust_scale: float = 0.75,
) -> Episode:
    """跑一次。fault_at 不為 None 時,在該步注入推力衰減(單顆馬達出力下降的簡化)。"""
    quad = PlanarQuad(params, dt=dt)
    quad.reset(start)
    guarded.reset_counters()

    errs: list[float] = []
    tilts: list[float] = []
    reward = 0.0

    for i in range(horizon):
        if fault_at is not None and i == fault_at:
            quad.p.thrust_scale *= fault_thrust_scale

        obs = quad.observe()
        act = guarded.act(obs, target)
        quad.step(act)

        s = quad.s
        err = math.hypot(target[0] - s.x, target[1] - s.z)
        errs.append(err)
        tilts.append(abs(s.theta))
        # 訓練用的 reward:位置為主,姿態與控制量當正則項
        reward -= err + 0.15 * abs(s.theta) + 0.02 * float(np.sum(np.abs(act)))

        if quad.crashed:
            reward -= 100.0
            break

    e = np.asarray(errs) if errs else np.array([9.9])
    return Episode(
        reward=reward,
        crashed=quad.crashed,
        pos_err_p95_m=float(np.percentile(e, 95)),
        pos_err_max_m=float(e.max()),
        max_tilt_deg=float(np.degrees(max(tilts) if tilts else 0.0)),
        terminal_speed_mps=float(math.hypot(quad.s.vx, quad.s.vz)),
        clamp_rate=guarded.clamp_rate,
        ood_rate=guarded.ood_rate,
    )


@dataclass
class TrainEnv:
    """訓練環境:窄一點的隨機範圍,不注入故障。"""

    seed: int = 0
    dt: float = 0.01
    horizon: int = 400
    rng: np.random.Generator = field(init=False)

    def __post_init__(self) -> None:
        self.rng = np.random.default_rng(self.seed)

    def _episode_setup(self) -> tuple[Params, State, np.ndarray]:
        params = sample(self.rng, evaluation=False)
        # 初始條件的範圍要涵蓋驗收會遇到的操作包絡。第一版把它設得比驗收窄,
        # 結果策略在訓練裡表現正常、驗收 100% 墜毀 —— 那是訓練分布沒蓋到,
        # 不是「驗收比較嚴」。驗收該外推的是系統參數與故障,不是操作包絡。
        start = State(
            x=float(self.rng.uniform(-1.6, 1.6)),
            z=float(self.rng.uniform(1.0, 4.0)),
            theta=float(self.rng.uniform(-0.25, 0.25)),
        )
        target = np.array([0.0, 2.5])
        return params, start, target

    def evaluate(self, guarded: GuardedPolicy, n: int = 4) -> float:
        total = 0.0
        for _ in range(n):
            params, start, target = self._episode_setup()
            total += rollout(guarded, params, target=target, start=start,
                             dt=self.dt, horizon=self.horizon).reward
        return total / n


@dataclass
class EvalEnv:
    """驗收環境:更寬的參數範圍、不同的初始條件、而且會注入故障。

    種子與 TrainEnv 分開,確保驗收看到的不是訓練時抽過的那些參數組合。
    """

    seed: int = 99991
    dt: float = 0.01
    horizon: int = 400
    fault_ratio: float = 0.5          # 一半的回合注入故障
    rng: np.random.Generator = field(init=False)

    def __post_init__(self) -> None:
        self.rng = np.random.default_rng(self.seed)

    def run(self, guarded: GuardedPolicy, n: int = 24) -> list[Episode]:
        out: list[Episode] = []
        for i in range(n):
            params = sample(self.rng, evaluation=True)
            start = State(
                x=float(self.rng.uniform(-1.6, 1.6)),
                z=float(self.rng.uniform(1.0, 4.0)),
                theta=float(self.rng.uniform(-0.25, 0.25)),
            )
            fault_at = int(self.horizon * 0.5) if i < int(n * self.fault_ratio) else None
            out.append(rollout(guarded, params, target=np.array([0.0, 2.5]), start=start,
                               dt=self.dt, horizon=self.horizon, fault_at=fault_at))
        return out


# 驗收門檻。docs/60-simulation-and-testing/03 的做法是「用實測基準定門檻,
# 先寬鬆再逐步收緊」,不是憑感覺挑數字。
#
# 這組值來自退路 PD 控制器在同一組驗收條件下的實測(`--eval-only`):
#   crash_rate 0.000 · pos_err_p95 1.595 · max_tilt 17.6° ·
#   terminal_speed 0.168 · clamp_rate 0.000 · ood_rate 0.000
# 門檻設在基準之上一截,所以「學出來的策略至少不能比退路差」。
# 策略變好之後,這組數字就該往下收。
GATES = {
    "crash_rate":            0.00,
    "pos_err_p95_m":         2.00,
    "max_tilt_deg":          45.0,
    "terminal_speed_mps":    1.00,
    "clamp_rate":            0.30,
    "ood_rate":              0.10,
}


def summarize(episodes: list[Episode]) -> dict[str, float]:
    arr = lambda f: np.array([getattr(e, f) for e in episodes], float)
    return {
        "crash_rate": float(np.mean([e.crashed for e in episodes])),
        "pos_err_p95_m": float(np.percentile(arr("pos_err_p95_m"), 95)),
        "max_tilt_deg": float(arr("max_tilt_deg").max()),
        "terminal_speed_mps": float(np.percentile(arr("terminal_speed_mps"), 95)),
        "clamp_rate": float(arr("clamp_rate").mean()),
        "ood_rate": float(arr("ood_rate").mean()),
    }


def check_gates(metrics: dict[str, float]) -> list[str]:
    """回傳沒過的項目。空清單代表通過。"""
    return [f"{k}: {metrics[k]:.3f} > 門檻 {v}" for k, v in GATES.items() if metrics.get(k, 0.0) > v]
