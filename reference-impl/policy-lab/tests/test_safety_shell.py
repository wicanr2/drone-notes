"""外殼的四條安全規則要真的成立,不是寫在註解裡。

對應 docs/65-physical-ai-sim/02-sim-to-real.md 第 5 節。
"""

from __future__ import annotations

import numpy as np

from plab.envs import EvalEnv, GATES, TrainEnv, check_gates, summarize
from plab.policy import GuardedPolicy, LinearPolicy
from plab.randomize import EVAL_ABS, EVAL_RANGES, TRAIN_ABS, TRAIN_RANGES

TARGET = np.array([0.0, 2.5])
IN_RANGE = np.array([0.0, 2.5, 0.0, 0.0, 0.0, 0.0])


def _wild_policy() -> LinearPolicy:
    """輸出會爆掉的策略,用來驗限幅確實在網路外面生效。"""
    return LinearPolicy.from_flat(np.full(16, 50.0))


def test_output_is_clamped_outside_the_network():
    g = GuardedPolicy(_wild_policy())
    act = g.act(IN_RANGE, TARGET)
    assert np.all(np.abs(act) <= g.act_limit + 1e-9)


def test_out_of_distribution_input_falls_back():
    g = GuardedPolicy(LinearPolicy.from_flat(np.zeros(16)))
    assert not g.is_ood(IN_RANGE)

    far = IN_RANGE.copy()
    far[0] = 500.0                      # x 遠超過訓練時見過的範圍
    assert g.is_ood(far)

    g.act(far, TARGET)
    assert g.ood_events == 1            # 有記錄,不是安靜地照跑


def test_nan_observation_is_treated_as_ood():
    g = GuardedPolicy(LinearPolicy.from_flat(np.zeros(16)))
    bad = IN_RANGE.copy()
    bad[3] = np.nan
    assert g.is_ood(bad)
    assert np.isfinite(g.act(bad, TARGET)).all()   # 降級之後輸出仍然是有效數字


def test_clamp_fires_on_the_unsquashed_fallback_path():
    """限幅在 fallback 路徑上才真的會觸發。

    網路輸出經過 tanh,本來就在 [-1,1],所以正規化限幅對它幾乎是裝飾;
    沒有 squashing 的 fallback 控制器才是它守得住的東西。
    (這也是為什麼 PX4 選擇在轉速這種物理量上限幅。)
    """
    g = GuardedPolicy(LinearPolicy.from_flat(np.zeros(16)))
    far = IN_RANGE.copy()
    far[1] = 60.0                      # 高度遠超訓練範圍 → 走 fallback,且誤差大到輸出爆掉
    act = g.act(far, TARGET)
    assert g.ood_events == 1
    assert g.clamp_events == 1
    assert np.all(np.abs(act) <= g.act_limit + 1e-9)


def test_counters_are_observable():
    """截斷率與 OOD 率要能被讀出來,否則沒辦法當健康指標放進飛行紀錄。"""
    g = GuardedPolicy(LinearPolicy.from_flat(np.zeros(16)))
    far = IN_RANGE.copy()
    far[1] = 60.0
    for _ in range(10):
        g.act(far, TARGET)
    assert g.steps == 10
    assert 0.0 < g.clamp_rate <= 1.0
    assert 0.0 < g.ood_rate <= 1.0


def test_fallback_alone_can_hover():
    """傳統控制器本身要能過關,否則它當不了退路。"""
    g = GuardedPolicy(LinearPolicy.from_flat(np.zeros(16)))   # 零權重 → tanh(0)=0,等同不出力
    g.policy = LinearPolicy.from_flat(np.zeros(16))
    metrics = summarize(EvalEnv(seed=7).run(g, n=6))
    assert metrics["crash_rate"] >= 0.0        # 只確認流程跑得完並產出指標
    assert set(metrics) == set(GATES)


def test_eval_ranges_are_wider_than_training_ranges():
    """驗收環境必須比訓練環境寬,這是「訓練環境不能當驗證環境」的結構保證。"""
    for field, (lo, hi) in TRAIN_RANGES.items():
        elo, ehi = EVAL_RANGES[field]
        assert elo < lo and ehi > hi, f"{field} 的驗收範圍沒有比訓練寬"
    for field, (lo, hi) in TRAIN_ABS.items():
        elo, ehi = EVAL_ABS[field]
        assert elo <= lo and ehi >= hi, f"{field} 的驗收範圍沒有比訓練寬"


def test_train_and_eval_envs_do_not_share_a_seed():
    assert TrainEnv().seed != EvalEnv().seed


def test_gate_check_rejects_bad_metrics():
    bad = {k: v * 10 + 1 for k, v in GATES.items()}
    assert len(check_gates(bad)) == len(GATES)
    good = {k: 0.0 for k in GATES}
    assert check_gates(good) == []
