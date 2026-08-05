"""訓練與驗收的進入點。

用 CEM(cross-entropy method)而不是深度 RL,理由很實際:純 numpy、單執行緒、
幾秒鐘跑完、完全確定性。這個骨架要示範的是**外殼與驗收怎麼做**,
不是策略能學多難的任務——換成 Isaac Lab 訓出來的網路,envs.py 與 policy.py
的結構完全不用改。

用法:
    python -m plab.train              # 訓練 + 驗收
    python -m plab.train --eval-only  # 只跑驗收(用 fallback 控制器當基準)
    python -m plab.train --ranges     # 印出隨機化範圍
"""

from __future__ import annotations

import argparse
import time

import numpy as np

from .envs import EvalEnv, GATES, TrainEnv, check_gates, summarize
from .policy import ACT_DIM, OBS_DIM, GuardedPolicy, LinearPolicy
from .randomize import describe

N_PARAMS = ACT_DIM * (OBS_DIM + 2)


def train(iters: int = 25, pop: int = 16, elite: int = 4, rollouts: int = 4,
          seed: int = 0, verbose: bool = True) -> LinearPolicy:
    rng = np.random.default_rng(seed)
    mean = np.zeros(N_PARAMS)
    std = np.ones(N_PARAMS) * 0.6
    best = LinearPolicy.from_flat(mean)

    for it in range(iters):
        samples = rng.normal(mean, std, size=(pop, N_PARAMS))
        scores = np.empty(pop)
        for i, flat in enumerate(samples):
            env = TrainEnv(seed=seed * 1000 + it)      # 同一代用同一批擾動,比較才公平
            scores[i] = env.evaluate(GuardedPolicy(LinearPolicy.from_flat(flat)), n=rollouts)

        idx = np.argsort(scores)[-elite:]
        mean = samples[idx].mean(axis=0)
        std = samples[idx].std(axis=0) + 0.02          # 加一點下限,避免太早收斂
        best = LinearPolicy.from_flat(mean)
        if verbose and (it % 5 == 0 or it == iters - 1):
            print(f"  第 {it:2d} 代  最佳 {scores[idx[-1]]:9.1f}  平均 {scores.mean():9.1f}")
    return best


def evaluate(policy: LinearPolicy | None, n: int = 24) -> tuple[dict, list[str]]:
    """policy 為 None 時跑退路控制器,當作策略必須超越的基準線。"""
    guarded = GuardedPolicy(policy or LinearPolicy(), force_fallback=policy is None)
    episodes = EvalEnv().run(guarded, n=n)
    metrics = summarize(episodes)
    return metrics, check_gates(metrics)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=25)
    ap.add_argument("--pop", type=int, default=16)
    ap.add_argument("--rollouts", type=int, default=4)
    ap.add_argument("--eval-episodes", type=int, default=24)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--eval-only", action="store_true")
    ap.add_argument("--ranges", action="store_true")
    args = ap.parse_args()

    if args.ranges:
        print(describe())
        return 0

    policy = None
    if not args.eval_only:
        steps = args.iters * args.pop * args.rollouts * 400
        print(f"訓練:{args.iters} 代 × {args.pop} 個樣本 × {args.rollouts} 回合 × 400 步 "
              f"≈ {steps/1000:.0f}k 步模擬,單執行緒")
        t0 = time.perf_counter()
        policy = train(iters=args.iters, pop=args.pop, rollouts=args.rollouts, seed=args.seed)
        print(f"訓練耗時 {time.perf_counter()-t0:.1f} 秒\n")

    label = "學出來的策略" if policy is not None else "fallback PD 控制器(基準)"
    print(f"驗收({label}),{args.eval_episodes} 個回合,參數範圍比訓練寬、一半注入推力衰減")
    metrics, failures = evaluate(policy, n=args.eval_episodes)
    for k, v in metrics.items():
        mark = "✗" if any(k in f for f in failures) else "✓"
        print(f"  {mark} {k:20s} {v:8.3f}   門檻 {GATES[k]}")

    if failures:
        print("\n未通過:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\n全部通過")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
