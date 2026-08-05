"""最小平面四旋翼動力學。

刻意保留三個「模擬與真機的落差來源」,因為 docs/65 說策略會學會利用
模擬器的缺陷,而最常被簡化掉的正是這三項:

1. 馬達不是瞬時響應 —— 推力以一階延遲追指令
2. 感測到致動之間有延遲 —— 用一個環形緩衝表示
3. 感測器有偏差 —— 姿態量測帶一個固定偏移

把這三項拿掉,訓出來的策略會在模擬裡表現極好、在真機上抖。
"""

from __future__ import annotations

from dataclasses import dataclass, field

import math

import numpy as np

G = 9.81


@dataclass
class Params:
    """機體與環境參數。

    預設值代表「參數辨識之後得到的標稱值」,訓練時在這組值附近隨機
    (見 randomize.py),而不是隨便挑一個範圍。
    """

    mass_kg: float = 1.2
    inertia: float = 0.015          # 繞 y 軸的轉動慣量
    arm_m: float = 0.25             # 力臂,決定同樣的差動推力能產生多少力矩
    thrust_scale: float = 1.0       # 推力係數誤差(1.0 = 與標稱一致)
    motor_tau_s: float = 0.035      # 馬達一階時間常數
    delay_steps: int = 2            # 感測到致動的延遲(以模擬步數計)
    theta_bias_rad: float = 0.0     # 姿態量測偏差
    wind_accel: float = 0.0         # 側向風造成的等效加速度
    max_thrust_n: float = 2.5 * 1.2 * G   # 推重比約 2.5
    max_torque_nm: float = 0.6


@dataclass
class State:
    x: float = 0.0
    z: float = 0.0
    vx: float = 0.0
    vz: float = 0.0
    theta: float = 0.0              # 正值代表向 +x 方向傾斜
    omega: float = 0.0

    def as_array(self) -> np.ndarray:
        return np.array([self.x, self.z, self.vx, self.vz, self.theta, self.omega], float)


class PlanarQuad:
    """平面(x-z)四旋翼。輸入是正規化的 [推力, 力矩],範圍 [-1, 1]。"""

    def __init__(self, params: Params, dt: float = 0.005) -> None:
        self.p = params
        self.dt = dt
        self.reset()

    def reset(self, state: State | None = None) -> State:
        self.s = state or State()
        self._thrust = self.p.mass_kg * G          # 從懸停推力開始,不從 0
        self._torque = 0.0
        # 延遲以佇列表示:指令要排隊 delay_steps 步才生效
        self._queue: list[tuple[float, float]] = [(0.0, 0.0)] * max(self.p.delay_steps, 0)
        return self.s

    def observe(self) -> np.ndarray:
        """給策略看的觀測。注意姿態帶偏差 —— 策略拿到的不是真值。"""
        o = self.s.as_array()
        o[4] += self.p.theta_bias_rad
        return o

    def step(self, action: np.ndarray) -> State:
        a = np.clip(np.asarray(action, float), -1.0, 1.0)
        thrust_cmd = (a[0] + 1.0) * 0.5 * self.p.max_thrust_n * self.p.thrust_scale
        torque_cmd = a[1] * self.p.max_torque_nm

        # 延遲:現在下的指令排到隊尾,取出隊首才是這一步真正生效的
        self._queue.append((thrust_cmd, torque_cmd))
        thrust_cmd, torque_cmd = self._queue.pop(0) if self._queue else (thrust_cmd, torque_cmd)

        # 馬達一階延遲
        alpha = self.dt / max(self.p.motor_tau_s, 1e-6)
        alpha = min(alpha, 1.0)
        self._thrust += alpha * (thrust_cmd - self._thrust)
        self._torque += alpha * (torque_cmd - self._torque)

        s, dt = self.s, self.dt
        ax = -(self._thrust / self.p.mass_kg) * math.sin(s.theta) + self.p.wind_accel
        az = (self._thrust / self.p.mass_kg) * math.cos(s.theta) - G
        alpha_ang = self._torque / self.p.inertia

        s.vx += ax * dt
        s.vz += az * dt
        s.omega += alpha_ang * dt
        s.x += s.vx * dt
        s.z += s.vz * dt
        s.theta += s.omega * dt

        # 撞地就停住,避免動力學發散成無意義的數字
        if s.z < 0.0:
            s.z, s.vz = 0.0, 0.0
        return s

    @property
    def crashed(self) -> bool:
        return abs(self.s.theta) > np.pi / 2 or not np.isfinite(self.s.as_array()).all()
