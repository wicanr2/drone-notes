"""策略,以及把它放進安全路徑時該有的三層外殼。

對應 docs/65-physical-ai-sim/02-sim-to-real.md 的四條規則:

1. 輸出限幅要在網路外面 —— Policy.act() 之後才夾,而且記次數
2. 要有能一鍵回去的傳統控制器 —— FallbackPD
3. 要監控輸入是否落在訓練分布內 —— OOD 檢查,超出就降級
4. 獎勵不是驗收標準 —— 這裡完全不算 reward,驗收在 envs.py

第 1 與第 3 條產生的計數本身就是健康指標:常截斷、常 OOD,代表策略
正在遇到它不熟的狀況,而這件事要在飛行紀錄裡看得到。
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

OBS_DIM = 6
ACT_DIM = 2

# 觀測完全不可用時的輸出:標稱質量下的懸停油門,零力矩。
# 真實系統應該用飛控的懸停推力估計值,而不是寫死的常數。
SAFE_ACTION = np.array([-0.2, 0.0])

# 注意:LinearPolicy 的輸出經過 tanh,本來就落在 [-1, 1],所以下面那層
# 正規化限幅對它幾乎不會觸發 —— 這是跑測試才看清楚的。真正有意義的限幅
# 要做在**物理量**上(轉速、推力),PX4 的 MC_NN_MAX_RPM / MC_NN_MIN_RPM
# 就是這個形式。這裡保留正規化限幅,是因為它仍然守住兩件事:
# fallback 控制器的輸出沒有 squashing,以及未來換成不做 squashing 的網路。

# 訓練時觀測值出現過的範圍。實務上應該從訓練資料統計出來,
# 這裡寫死是為了讓骨架能單獨跑。
OBS_LIMITS = np.array([
    [-6.0, 6.0],       # x
    [0.0, 12.0],       # z
    [-8.0, 8.0],       # vx
    [-8.0, 8.0],       # vz
    [-1.0, 1.0],       # theta (rad)
    [-8.0, 8.0],       # omega
])


@dataclass
class FallbackPD:
    """傳統控制器。策略失效或觀測落在分布外時接手。

    刻意寫得很笨:能懸停、能大致飛到目標點就好。它的價值不在性能,
    在於「你完全理解它會做什麼」。
    """

    # 增益照「正規化動作空間」算出來,不是憑感覺調的。
    #
    # 姿態迴路的頻寬由**驗收環境的最壞延遲**決定,用 docs/00 那條 φ = ω·τ:
    #   驗收會抽到 delay_steps=6,dt=0.01 → τ = 60 ms
    #   願意付出 30°(0.524 rad)的相位落後 → ω ≤ 0.524 / 0.06 ≈ 8.7 rad/s
    #   取 ω_n = 6 rad/s 留餘裕;滿舵指令約 40 rad/s²
    #   → kp_th = ω_n²/40 = 0.9,kd_th = 2ζω_n/40 = 0.3
    # 位置迴路再慢 5 倍(ω≈1.2 rad/s),避免內外層互打。
    #
    # 第一版沒照這條算,姿態取 ω_n=12 rad/s,在 60 ms 延遲下相位落後 41°,
    # 退路控制器自己會翻 —— 驗收閘門抓到了,而原因就寫在第 00 章。
    kp_z: float = 0.33
    kd_z: float = 0.33
    kp_x: float = 0.147
    kd_x: float = 0.245
    kp_th: float = 0.9
    kd_th: float = 0.3
    hover_cmd: float = -0.2         # 標稱質量下的懸停油門(見 SAFE_ACTION)

    def act(self, obs: np.ndarray, target: np.ndarray) -> np.ndarray:
        x, z, vx, vz, th, om = obs
        tx, tz = target
        thrust = self.hover_cmd + self.kp_z * (tz - z) + self.kd_z * (0.0 - vz)
        theta_ref = -(self.kp_x * (tx - x) + self.kd_x * (0.0 - vx))
        theta_ref = float(np.clip(theta_ref, -0.35, 0.35))
        torque = self.kp_th * (theta_ref - th) + self.kd_th * (0.0 - om)
        return np.array([thrust, torque], float)


@dataclass
class LinearPolicy:
    """學出來的策略本體。

    刻意用最小的形式(線性 + tanh),因為這個骨架要證明的是「外殼與驗收
    怎麼做」,不是「策略能學多難的任務」。換成 MLP 或換成 Isaac Lab 訓出來
    的網路,外面這三層完全不用改。
    """

    weights: np.ndarray = field(default_factory=lambda: np.zeros((ACT_DIM, OBS_DIM + 2)))

    @property
    def n_params(self) -> int:
        return self.weights.size

    @classmethod
    def from_flat(cls, flat: np.ndarray) -> "LinearPolicy":
        return cls(weights=np.asarray(flat, float).reshape(ACT_DIM, OBS_DIM + 2))

    def to_flat(self) -> np.ndarray:
        return self.weights.reshape(-1).copy()

    def act(self, obs: np.ndarray, target: np.ndarray) -> np.ndarray:
        feat = np.concatenate([obs, target - obs[:2]])
        return np.tanh(self.weights @ feat)


@dataclass
class GuardedPolicy:
    """把策略包進三層外殼:OOD 檢查 → 推論或退回 → 輸出限幅。"""

    policy: LinearPolicy
    fallback: FallbackPD = field(default_factory=FallbackPD)
    act_limit: float = 1.0
    ood_margin: float = 1.15          # 允許略微超出訓練範圍再算 OOD
    # 只用退路控制器。這是「策略至少要比這個好」的基準線,
    # 也是驗收閘門本身合不合理的檢查方式。
    force_fallback: bool = False

    clamp_events: int = 0
    ood_events: int = 0
    invalid_obs_events: int = 0
    steps: int = 0

    def is_ood(self, obs: np.ndarray) -> bool:
        lo, hi = OBS_LIMITS[:, 0], OBS_LIMITS[:, 1]
        span = (hi - lo) * 0.5 * self.ood_margin
        mid = (hi + lo) * 0.5
        return bool(np.any(np.abs(obs - mid) > span)) or not np.isfinite(obs).all()

    def act(self, obs: np.ndarray, target: np.ndarray) -> np.ndarray:
        self.steps += 1

        # 觀測本身壞掉(NaN / inf)時,連 fallback 都不能用 —— 把壞數字餵給 PD
        # 只會得到壞輸出。這是寫測試才發現的:「偵測到 OOD 就交給傳統控制器」
        # 這句話漏掉了「傳統控制器也需要有效輸入」。
        if not np.isfinite(obs).all():
            self.ood_events += 1
            self.invalid_obs_events += 1
            return SAFE_ACTION.copy()

        ood = self.is_ood(obs)
        if ood:
            self.ood_events += 1
        if ood or self.force_fallback:
            raw = self.fallback.act(obs, target)      # 降級,不讓網路在沒見過的輸入上輸出
        else:
            raw = self.policy.act(obs, target)

        clipped = np.clip(raw, -self.act_limit, self.act_limit)
        if not np.allclose(clipped, raw):
            self.clamp_events += 1
        return clipped

    def reset_counters(self) -> None:
        self.clamp_events = self.ood_events = self.steps = 0

    @property
    def clamp_rate(self) -> float:
        return self.clamp_events / max(self.steps, 1)

    @property
    def ood_rate(self) -> float:
        return self.ood_events / max(self.steps, 1)
