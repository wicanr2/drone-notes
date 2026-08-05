# PX4 參數全集 — v1.17.0

> 這份是**產生出來的**,不是手寫的。內容直接解析 PX4 `v1.17.0` 的原始碼,產生器與重跑指令在 [`tools/dump_px4_api.py`](../../../tools/dump_px4_api.py)。換版本重跑,不要手改這個檔。

## 出處

| 項目 | 出處 |
|---|---|
| 原始碼 | <https://github.com/PX4/PX4-Autopilot/tree/v1.17.0>,tarball 為 `archive/refs/tags/v1.17.0.tar.gz` |
| 解析範圍 | `src/**/module.yaml` 的 `parameters` 區塊 + `src/**/*.c` 的 `PARAM_DEFINE_*` 巨集,共 2059 個參數、100 個群組 |
| 官方參考 | <https://docs.px4.io/>(預設顯示 main 分支,與此處的 `v1.17.0` 可能不同) |

## 怎麼用這份東西

**不要從頭讀。** 參數是查詢用的,不是閱讀用的。實際會用到的方式有三種:在地面站裡搜名字、在文件裡確認單位與範圍、看某個功能牽動哪些參數(用群組)。

有幾個地方值得先知道:

- **參數名有 16 字元上限**,所以縮寫很兇。`MC_ROLLRATE_P` 是多旋翼滾轉角速率的比例增益,不是別的。
- **改參數會即時生效,但不是每個都安全**。控制增益在飛行中改會直接影響穩定性。
- **預設值是「某台參考機」的值**,不是你的機。特別是慣量、推力、增益這幾類,照抄預設等於假設你的機跟參考機一樣。

其中 **19 個參數在原始碼裡沒有說明**(`TEST_MIN`、`TEST_MAX`、`TEST_TRIM`、`TEST_HP`、`TEST_LP`、`TEST_P`、`TEST_I`、`TEST_I_MAX`…),這裡照實留白,不代為推測用途。

---

## 群組

| 群組 | 參數數 |
|---|---|
| [Geometry](#geometry) | 250 |
| [Thermal Compensation](#thermal-compensation) | 236 |
| [Sensors](#sensors) | 190 |
| [Sensor Calibration](#sensor-calibration) | 151 |
| [Radio Calibration](#radio-calibration) | 95 |
| [Commander](#commander) | 81 |
| [Multicopter Position Control](#multicopter-position-control) | 67 |
| [Local Position Estimator](#local-position-estimator) | 40 |
| [MAVLink](#mavlink) | 39 |
| [UAVCAN](#uavcan) | 36 |
| [VTOL Attitude Control](#vtol-attitude-control) | 35 |
| [Battery Calibration](#battery-calibration) | 34 |
| [FW Rate Control](#fw-rate-control) | 33 |
| [Spacecraft Rate Control](#spacecraft-rate-control) | 28 |
| [Cyphal](#cyphal) | 25 |
| [System](#system) | 25 |
| [Radio Switches](#radio-switches) | 23 |
| [Vertiq IO](#vertiq-io) | 22 |
| [Mission](#mission) | 21 |
| [Simulation In Hardware](#simulation-in-hardware) | 21 |
| [Spacecraft Position Control](#spacecraft-position-control) | 21 |
| [UUV Attitude Control](#uuv-attitude-control) | 21 |
| [FW Longitudinal Control](#fw-longitudinal-control) | 20 |
| [Multicopter Rate Control](#multicopter-rate-control) | 20 |
| [Airspeed Validator](#airspeed-validator) | 19 |
| [EKF2](#ekf2) | 19 |
| [Mount](#mount) | 19 |
| [VOXL ESC](#voxl-esc) | 19 |
| [Testing](#testing) | 18 |
| [FW Attitude Control](#fw-attitude-control) | 16 |
| [FW Auto Landing](#fw-auto-landing) | 16 |
| [FW General](#fw-general) | 14 |
| [ADSB](#adsb) | 13 |
| [Autotune](#autotune) | 13 |
| [FW Performance](#fw-performance) | 13 |
| [GPS](#gps) | 13 |
| [Land Detector](#land-detector) | 13 |
| [Septentrio](#septentrio) | 13 |
| [Failure Detector](#failure-detector) | 12 |
| [ICE](#ice) | 11 |
| [Landing Target Estimator](#landing-target-estimator) | 11 |
| [Attitude Q estimator](#attitude-q-estimator) | 10 |
| [Multicopter Position Slow Mode](#multicopter-position-slow-mode) | 10 |
| [Rover Rate Control](#rover-rate-control) | 10 |
| [UUV Position Control](#uuv-position-control) | 10 |
| [UXRCE-DDS Client](#uxrce-dds-client) | 10 |
| [Camera trigger](#camera-trigger) | 9 |
| [Multicopter Attitude Control](#multicopter-attitude-control) | 9 |
| [Rover Velocity Control](#rover-velocity-control) | 9 |
| [Return Mode](#return-mode) | 8 |
| [SD Logging](#sd-logging) | 8 |
| [FW Auto Takeoff](#fw-auto-takeoff) | 7 |
| [FW NPFG Control](#fw-npfg-control) | 7 |
| [Multicopter Acro Mode](#multicopter-acro-mode) | 7 |
| [OSD](#osd) | 7 |
| [Runway Takeoff](#runway-takeoff) | 7 |
| [Simulator](#simulator) | 7 |
| [Spacecraft Attitude Control](#spacecraft-attitude-control) | 7 |
| [Circuit Breaker](#circuit-breaker) | 6 |
| [DShot](#dshot) | 6 |
| [Follow target](#follow-target) | 6 |
| [Hover Thrust Estimator](#hover-thrust-estimator) | 6 |
| [Precision Land](#precision-land) | 6 |
| [Simulation](#simulation) | 6 |
| [VOXL2 IO](#voxl2-io) | 6 |
| [未分組](#未分組) | 6 |
| [Geofence](#geofence) | 5 |
| [Neural Control](#neural-control) | 5 |
| [Rover Ackermann](#rover-ackermann) | 5 |
| [Actuator Outputs](#actuator-outputs) | 4 |
| [Rover Differential](#rover-differential) | 4 |
| [UWB](#uwb) | 4 |
| [Camera Control](#camera-control) | 3 |
| [ESC](#esc) | 3 |
| [Iridium SBD](#iridium-sbd) | 3 |
| [Magnetometer](#magnetometer) | 3 |
| [Manual Control](#manual-control) | 3 |
| [Pure Pursuit](#pure-pursuit) | 3 |
| [Return To Land](#return-to-land) | 3 |
| [Rover Mecanum](#rover-mecanum) | 3 |
| [SITL](#sitl) | 3 |
| [Transponder](#transponder) | 3 |
| [CDCACM](#cdcacm) | 2 |
| [Events](#events) | 2 |
| [Flight Task Orbit](#flight-task-orbit) | 2 |
| [Magnetometer Bias Estimator](#magnetometer-bias-estimator) | 2 |
| [PWM Outputs](#pwm-outputs) | 2 |
| [Payload Deliverer](#payload-deliverer) | 2 |
| [RC](#rc) | 2 |
| [Roboclaw Driver](#roboclaw-driver) | 2 |
| [Camera Capture](#camera-capture) | 1 |
| [FW Lateral Control](#fw-lateral-control) | 1 |
| [Mixer Output](#mixer-output) | 1 |
| [ModalAI Custom Configuration](#modalai-custom-configuration) | 1 |
| [RC Input](#rc-input) | 1 |
| [Rover Attitude Control](#rover-attitude-control) | 1 |
| [Serial](#serial) | 1 |
| [Telemetry](#telemetry) | 1 |
| [VTOL Takeoff](#vtol-takeoff) | 1 |
| [Zenoh](#zenoh) | 1 |

---

## Geometry

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `CA_AIRFRAME` | enum | 0 |  |  | Airframe selection |
| `CA_FAILURE_MODE` | enum | 0 |  |  | Motor failure handling mode |
| `CA_HELI_PITCH_C0` | float | -0.05, 0.0725, 0.2, 0.325, 0.45 | -1 ~ 1 |  | Collective pitch curve at position ${i} |
| `CA_HELI_PITCH_C1` | float | -0.05, 0.0725, 0.2, 0.325, 0.45 | -1 ~ 1 |  | Collective pitch curve at position ${i} |
| `CA_HELI_PITCH_C2` | float | -0.05, 0.0725, 0.2, 0.325, 0.45 | -1 ~ 1 |  | Collective pitch curve at position ${i} |
| `CA_HELI_PITCH_C3` | float | -0.05, 0.0725, 0.2, 0.325, 0.45 | -1 ~ 1 |  | Collective pitch curve at position ${i} |
| `CA_HELI_PITCH_C4` | float | -0.05, 0.0725, 0.2, 0.325, 0.45 | -1 ~ 1 |  | Collective pitch curve at position ${i} |
| `CA_HELI_RPM_I` | float | 0.0 | 0 ~ 10 |  | Integral gain for rpm control |
| `CA_HELI_RPM_P` | float | 0.0 | 0 ~ 10 |  | Proportional gain for rpm control |
| `CA_HELI_RPM_SP` | float | 1500 | 100 ~ 10000 |  | Setpoint for main rotor rpm |
| `CA_HELI_THR_C0` | float | 1, 1, 1, 1, 1 | 0 ~ 1 |  | Throttle curve at position ${i} |
| `CA_HELI_THR_C1` | float | 1, 1, 1, 1, 1 | 0 ~ 1 |  | Throttle curve at position ${i} |
| `CA_HELI_THR_C2` | float | 1, 1, 1, 1, 1 | 0 ~ 1 |  | Throttle curve at position ${i} |
| `CA_HELI_THR_C3` | float | 1, 1, 1, 1, 1 | 0 ~ 1 |  | Throttle curve at position ${i} |
| `CA_HELI_THR_C4` | float | 1, 1, 1, 1, 1 | 0 ~ 1 |  | Throttle curve at position ${i} |
| `CA_HELI_YAW_CCW` | boolean | 0 |  |  | Main rotor turns counter-clockwise |
| `CA_HELI_YAW_CP_O` | float | 0.0 | -2 ~ 2 |  | Offset for yaw compensation based on collective pitch |
| `CA_HELI_YAW_CP_S` | float | 0.0 | -2 ~ 2 |  | Scale for yaw compensation based on collective pitch |
| `CA_HELI_YAW_TH_S` | float | 0.0 | -2 ~ 2 |  | Scale for yaw compensation based on throttle |
| `CA_MAX_SVO_THROW` | float | 0.0 | 0 ~ 75 | deg | Throw angle of swashplate servo at maximum commands for linearization |
| `CA_METHOD` | enum | 2 |  |  | Control allocation method |
| `CA_R0_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_R10_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_R11_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_R1_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_R2_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_R3_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_R4_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_R5_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_R6_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_R7_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_R8_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_R9_SLEW` | float | 0.0 | 0 ~ 10 | s | Motor ${i} slew rate limit |
| `CA_ROTOR0_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR0_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR0_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR0_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR0_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR0_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR0_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR0_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR0_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR10_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR10_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR10_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR10_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR10_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR10_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR10_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR10_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR10_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR11_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR11_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR11_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR11_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR11_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR11_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR11_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR11_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR11_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR1_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR1_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR1_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR1_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR1_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR1_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR1_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR1_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR1_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR2_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR2_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR2_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR2_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR2_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR2_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR2_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR2_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR2_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR3_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR3_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR3_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR3_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR3_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR3_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR3_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR3_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR3_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR4_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR4_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR4_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR4_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR4_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR4_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR4_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR4_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR4_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR5_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR5_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR5_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR5_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR5_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR5_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR5_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR5_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR5_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR6_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR6_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR6_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR6_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR6_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR6_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR6_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR6_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR6_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR7_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR7_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR7_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR7_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR7_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR7_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR7_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR7_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR7_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR8_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR8_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR8_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR8_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR8_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR8_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR8_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR8_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR8_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR9_AX` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, X body axis component |
| `CA_ROTOR9_AY` | float | 0.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Y body axis component |
| `CA_ROTOR9_AZ` | float | -1.0 | -100 ~ 100 |  | Axis of rotor ${i} thrust vector, Z body axis component |
| `CA_ROTOR9_CT` | float | 6.5 | 0 ~ 100 |  | Thrust coefficient of rotor ${i} |
| `CA_ROTOR9_KM` | float | 0.05 | -1 ~ 1 |  | Moment coefficient of rotor ${i} |
| `CA_ROTOR9_PX` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along X body axis relative to center of gravity |
| `CA_ROTOR9_PY` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Y body axis relative to center of gravity |
| `CA_ROTOR9_PZ` | float | 0.0 | -100 ~ 100 | m | Position of rotor ${i} along Z body axis relative to center of gravity |
| `CA_ROTOR9_TILT` | enum | 0 |  |  | Rotor ${i} tilt assignment |
| `CA_ROTOR_COUNT` | enum | 0 |  |  | Total number of rotors |
| `CA_R_REV` | bitmask | 0 |  |  | Bidirectional/Reversible motors |
| `CA_SP0_ANG0` | float | 0, 140, 220, 0 | 0 ~ 360 | deg | Angle for swash plate servo ${i} |
| `CA_SP0_ANG1` | float | 0, 140, 220, 0 | 0 ~ 360 | deg | Angle for swash plate servo ${i} |
| `CA_SP0_ANG2` | float | 0, 140, 220, 0 | 0 ~ 360 | deg | Angle for swash plate servo ${i} |
| `CA_SP0_ANG3` | float | 0, 140, 220, 0 | 0 ~ 360 | deg | Angle for swash plate servo ${i} |
| `CA_SP0_ARM_L0` | float | 1.0 | 0 ~ 10 |  | Arm length for swash plate servo ${i} |
| `CA_SP0_ARM_L1` | float | 1.0 | 0 ~ 10 |  | Arm length for swash plate servo ${i} |
| `CA_SP0_ARM_L2` | float | 1.0 | 0 ~ 10 |  | Arm length for swash plate servo ${i} |
| `CA_SP0_ARM_L3` | float | 1.0 | 0 ~ 10 |  | Arm length for swash plate servo ${i} |
| `CA_SP0_COUNT` | enum | 3 |  |  | Number of swash plates servos |
| `CA_SV0_SLEW` | float | 0.0 | 0 ~ 10 | s | Servo ${i} slew rate limit |
| `CA_SV1_SLEW` | float | 0.0 | 0 ~ 10 | s | Servo ${i} slew rate limit |
| `CA_SV2_SLEW` | float | 0.0 | 0 ~ 10 | s | Servo ${i} slew rate limit |
| `CA_SV3_SLEW` | float | 0.0 | 0 ~ 10 | s | Servo ${i} slew rate limit |
| `CA_SV4_SLEW` | float | 0.0 | 0 ~ 10 | s | Servo ${i} slew rate limit |
| `CA_SV5_SLEW` | float | 0.0 | 0 ~ 10 | s | Servo ${i} slew rate limit |
| `CA_SV6_SLEW` | float | 0.0 | 0 ~ 10 | s | Servo ${i} slew rate limit |
| `CA_SV7_SLEW` | float | 0.0 | 0 ~ 10 | s | Servo ${i} slew rate limit |
| `CA_SV_CS0_FLAP` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as flap |
| `CA_SV_CS0_SPOIL` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as spoiler |
| `CA_SV_CS0_TRIM` | float | 0.0 | -1.0 ~ 1.0 |  | Control Surface ${i} trim |
| `CA_SV_CS0_TRQ_P` | float | 0.0 |  |  | Control Surface ${i} pitch torque scaling |
| `CA_SV_CS0_TRQ_R` | float | 0.0 |  |  | Control Surface ${i} roll torque scaling |
| `CA_SV_CS0_TRQ_Y` | float | 0.0 |  |  | Control Surface ${i} yaw torque scaling |
| `CA_SV_CS0_TYPE` | enum | 0 |  |  | Control Surface ${i} type |
| `CA_SV_CS1_FLAP` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as flap |
| `CA_SV_CS1_SPOIL` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as spoiler |
| `CA_SV_CS1_TRIM` | float | 0.0 | -1.0 ~ 1.0 |  | Control Surface ${i} trim |
| `CA_SV_CS1_TRQ_P` | float | 0.0 |  |  | Control Surface ${i} pitch torque scaling |
| `CA_SV_CS1_TRQ_R` | float | 0.0 |  |  | Control Surface ${i} roll torque scaling |
| `CA_SV_CS1_TRQ_Y` | float | 0.0 |  |  | Control Surface ${i} yaw torque scaling |
| `CA_SV_CS1_TYPE` | enum | 0 |  |  | Control Surface ${i} type |
| `CA_SV_CS2_FLAP` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as flap |
| `CA_SV_CS2_SPOIL` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as spoiler |
| `CA_SV_CS2_TRIM` | float | 0.0 | -1.0 ~ 1.0 |  | Control Surface ${i} trim |
| `CA_SV_CS2_TRQ_P` | float | 0.0 |  |  | Control Surface ${i} pitch torque scaling |
| `CA_SV_CS2_TRQ_R` | float | 0.0 |  |  | Control Surface ${i} roll torque scaling |
| `CA_SV_CS2_TRQ_Y` | float | 0.0 |  |  | Control Surface ${i} yaw torque scaling |
| `CA_SV_CS2_TYPE` | enum | 0 |  |  | Control Surface ${i} type |
| `CA_SV_CS3_FLAP` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as flap |
| `CA_SV_CS3_SPOIL` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as spoiler |
| `CA_SV_CS3_TRIM` | float | 0.0 | -1.0 ~ 1.0 |  | Control Surface ${i} trim |
| `CA_SV_CS3_TRQ_P` | float | 0.0 |  |  | Control Surface ${i} pitch torque scaling |
| `CA_SV_CS3_TRQ_R` | float | 0.0 |  |  | Control Surface ${i} roll torque scaling |
| `CA_SV_CS3_TRQ_Y` | float | 0.0 |  |  | Control Surface ${i} yaw torque scaling |
| `CA_SV_CS3_TYPE` | enum | 0 |  |  | Control Surface ${i} type |
| `CA_SV_CS4_FLAP` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as flap |
| `CA_SV_CS4_SPOIL` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as spoiler |
| `CA_SV_CS4_TRIM` | float | 0.0 | -1.0 ~ 1.0 |  | Control Surface ${i} trim |
| `CA_SV_CS4_TRQ_P` | float | 0.0 |  |  | Control Surface ${i} pitch torque scaling |
| `CA_SV_CS4_TRQ_R` | float | 0.0 |  |  | Control Surface ${i} roll torque scaling |
| `CA_SV_CS4_TRQ_Y` | float | 0.0 |  |  | Control Surface ${i} yaw torque scaling |
| `CA_SV_CS4_TYPE` | enum | 0 |  |  | Control Surface ${i} type |
| `CA_SV_CS5_FLAP` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as flap |
| `CA_SV_CS5_SPOIL` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as spoiler |
| `CA_SV_CS5_TRIM` | float | 0.0 | -1.0 ~ 1.0 |  | Control Surface ${i} trim |
| `CA_SV_CS5_TRQ_P` | float | 0.0 |  |  | Control Surface ${i} pitch torque scaling |
| `CA_SV_CS5_TRQ_R` | float | 0.0 |  |  | Control Surface ${i} roll torque scaling |
| `CA_SV_CS5_TRQ_Y` | float | 0.0 |  |  | Control Surface ${i} yaw torque scaling |
| `CA_SV_CS5_TYPE` | enum | 0 |  |  | Control Surface ${i} type |
| `CA_SV_CS6_FLAP` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as flap |
| `CA_SV_CS6_SPOIL` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as spoiler |
| `CA_SV_CS6_TRIM` | float | 0.0 | -1.0 ~ 1.0 |  | Control Surface ${i} trim |
| `CA_SV_CS6_TRQ_P` | float | 0.0 |  |  | Control Surface ${i} pitch torque scaling |
| `CA_SV_CS6_TRQ_R` | float | 0.0 |  |  | Control Surface ${i} roll torque scaling |
| `CA_SV_CS6_TRQ_Y` | float | 0.0 |  |  | Control Surface ${i} yaw torque scaling |
| `CA_SV_CS6_TYPE` | enum | 0 |  |  | Control Surface ${i} type |
| `CA_SV_CS7_FLAP` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as flap |
| `CA_SV_CS7_SPOIL` | float | 0 | -1.0 ~ 1.0 |  | Control Surface ${i} configuration as spoiler |
| `CA_SV_CS7_TRIM` | float | 0.0 | -1.0 ~ 1.0 |  | Control Surface ${i} trim |
| `CA_SV_CS7_TRQ_P` | float | 0.0 |  |  | Control Surface ${i} pitch torque scaling |
| `CA_SV_CS7_TRQ_R` | float | 0.0 |  |  | Control Surface ${i} roll torque scaling |
| `CA_SV_CS7_TRQ_Y` | float | 0.0 |  |  | Control Surface ${i} yaw torque scaling |
| `CA_SV_CS7_TYPE` | enum | 0 |  |  | Control Surface ${i} type |
| `CA_SV_CS_COUNT` | enum | 0 |  |  | Total number of Control Surfaces |
| `CA_SV_TL0_CT` | enum | 1 |  |  | Tilt ${i} is used for control |
| `CA_SV_TL0_MAXA` | float | 90.0 | -90.0 ~ 90.0 | deg | Tilt Servo ${i} Tilt Angle at Maximum |
| `CA_SV_TL0_MINA` | float | 0.0 | -90.0 ~ 90.0 | deg | Tilt Servo ${i} Tilt Angle at Minimum |
| `CA_SV_TL0_TD` | enum | 0 | 0 ~ 359 |  | Tilt Servo ${i} Tilt Direction |
| `CA_SV_TL1_CT` | enum | 1 |  |  | Tilt ${i} is used for control |
| `CA_SV_TL1_MAXA` | float | 90.0 | -90.0 ~ 90.0 | deg | Tilt Servo ${i} Tilt Angle at Maximum |
| `CA_SV_TL1_MINA` | float | 0.0 | -90.0 ~ 90.0 | deg | Tilt Servo ${i} Tilt Angle at Minimum |
| `CA_SV_TL1_TD` | enum | 0 | 0 ~ 359 |  | Tilt Servo ${i} Tilt Direction |
| `CA_SV_TL2_CT` | enum | 1 |  |  | Tilt ${i} is used for control |
| `CA_SV_TL2_MAXA` | float | 90.0 | -90.0 ~ 90.0 | deg | Tilt Servo ${i} Tilt Angle at Maximum |
| `CA_SV_TL2_MINA` | float | 0.0 | -90.0 ~ 90.0 | deg | Tilt Servo ${i} Tilt Angle at Minimum |
| `CA_SV_TL2_TD` | enum | 0 | 0 ~ 359 |  | Tilt Servo ${i} Tilt Direction |
| `CA_SV_TL3_CT` | enum | 1 |  |  | Tilt ${i} is used for control |
| `CA_SV_TL3_MAXA` | float | 90.0 | -90.0 ~ 90.0 | deg | Tilt Servo ${i} Tilt Angle at Maximum |
| `CA_SV_TL3_MINA` | float | 0.0 | -90.0 ~ 90.0 | deg | Tilt Servo ${i} Tilt Angle at Minimum |
| `CA_SV_TL3_TD` | enum | 0 | 0 ~ 359 |  | Tilt Servo ${i} Tilt Direction |
| `CA_SV_TL_COUNT` | enum | 0 |  |  | Total number of Tilt Servos |
| `SIM_GZ_SV_MAXA1` | float | 45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Maximum |
| `SIM_GZ_SV_MAXA2` | float | 45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Maximum |
| `SIM_GZ_SV_MAXA3` | float | 45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Maximum |
| `SIM_GZ_SV_MAXA4` | float | 45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Maximum |
| `SIM_GZ_SV_MAXA5` | float | 45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Maximum |
| `SIM_GZ_SV_MAXA6` | float | 45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Maximum |
| `SIM_GZ_SV_MAXA7` | float | 45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Maximum |
| `SIM_GZ_SV_MAXA8` | float | 45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Maximum |
| `SIM_GZ_SV_MINA1` | float | -45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Minimum |
| `SIM_GZ_SV_MINA2` | float | -45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Minimum |
| `SIM_GZ_SV_MINA3` | float | -45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Minimum |
| `SIM_GZ_SV_MINA4` | float | -45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Minimum |
| `SIM_GZ_SV_MINA5` | float | -45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Minimum |
| `SIM_GZ_SV_MINA6` | float | -45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Minimum |
| `SIM_GZ_SV_MINA7` | float | -45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Minimum |
| `SIM_GZ_SV_MINA8` | float | -45.0 | -180.0 ~ 180.0 | deg | Servo ${i} Angle at Minimum |

## Thermal Compensation

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `TC_A0_ID` | int32 | 0 |  |  | ID of Accelerometer that the calibration is for. |
| `TC_A0_TMAX` | float | 100.0f |  |  | Accelerometer calibration maximum temperature. |
| `TC_A0_TMIN` | float | 0.0f |  |  | Accelerometer calibration minimum temperature. |
| `TC_A0_TREF` | float | 25.0f |  |  | Accelerometer calibration reference temperature. |
| `TC_A0_X0_0` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - X axis. |
| `TC_A0_X0_1` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_A0_X0_2` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_A0_X1_0` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - X axis. |
| `TC_A0_X1_1` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_A0_X1_2` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_A0_X2_0` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - X axis. |
| `TC_A0_X2_1` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_A0_X2_2` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_A0_X3_0` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - X axis. |
| `TC_A0_X3_1` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_A0_X3_2` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_A1_ID` | int32 | 0 |  |  | ID of Accelerometer that the calibration is for. |
| `TC_A1_TMAX` | float | 100.0f |  |  | Accelerometer calibration maximum temperature. |
| `TC_A1_TMIN` | float | 0.0f |  |  | Accelerometer calibration minimum temperature. |
| `TC_A1_TREF` | float | 25.0f |  |  | Accelerometer calibration reference temperature. |
| `TC_A1_X0_0` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - X axis. |
| `TC_A1_X0_1` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_A1_X0_2` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_A1_X1_0` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - X axis. |
| `TC_A1_X1_1` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_A1_X1_2` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_A1_X2_0` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - X axis. |
| `TC_A1_X2_1` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_A1_X2_2` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_A1_X3_0` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - X axis. |
| `TC_A1_X3_1` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_A1_X3_2` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_A2_ID` | int32 | 0 |  |  | ID of Accelerometer that the calibration is for. |
| `TC_A2_TMAX` | float | 100.0f |  |  | Accelerometer calibration maximum temperature. |
| `TC_A2_TMIN` | float | 0.0f |  |  | Accelerometer calibration minimum temperature. |
| `TC_A2_TREF` | float | 25.0f |  |  | Accelerometer calibration reference temperature. |
| `TC_A2_X0_0` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - X axis. |
| `TC_A2_X0_1` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_A2_X0_2` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_A2_X1_0` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - X axis. |
| `TC_A2_X1_1` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_A2_X1_2` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_A2_X2_0` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - X axis. |
| `TC_A2_X2_1` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_A2_X2_2` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_A2_X3_0` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - X axis. |
| `TC_A2_X3_1` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_A2_X3_2` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_A3_ID` | int32 | 0 |  |  | ID of Accelerometer that the calibration is for. |
| `TC_A3_TMAX` | float | 100.0f |  |  | Accelerometer calibration maximum temperature. |
| `TC_A3_TMIN` | float | 0.0f |  |  | Accelerometer calibration minimum temperature. |
| `TC_A3_TREF` | float | 25.0f |  |  | Accelerometer calibration reference temperature. |
| `TC_A3_X0_0` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - X axis. |
| `TC_A3_X0_1` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_A3_X0_2` | float | 0.0f |  |  | Accelerometer offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_A3_X1_0` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - X axis. |
| `TC_A3_X1_1` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_A3_X1_2` | float | 0.0f |  |  | Accelerometer offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_A3_X2_0` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - X axis. |
| `TC_A3_X2_1` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_A3_X2_2` | float | 0.0f |  |  | Accelerometer offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_A3_X3_0` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - X axis. |
| `TC_A3_X3_1` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_A3_X3_2` | float | 0.0f |  |  | Accelerometer offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_A_ENABLE` | int32 | 0 |  |  | Thermal compensation for accelerometer sensors. |
| `TC_B0_ID` | int32 | 0 |  |  | ID of Barometer that the calibration is for. |
| `TC_B0_TMAX` | float | 75.0f |  |  | Barometer calibration maximum temperature. |
| `TC_B0_TMIN` | float | 5.0f |  |  | Barometer calibration minimum temperature. |
| `TC_B0_TREF` | float | 40.0f |  |  | Barometer calibration reference temperature. |
| `TC_B0_X0` | float | 0.0f |  |  | Barometer offset temperature ^0 polynomial coefficient. |
| `TC_B0_X1` | float | 0.0f |  |  | Barometer offset temperature ^1 polynomial coefficients. |
| `TC_B0_X2` | float | 0.0f |  |  | Barometer offset temperature ^2 polynomial coefficient. |
| `TC_B0_X3` | float | 0.0f |  |  | Barometer offset temperature ^3 polynomial coefficient. |
| `TC_B0_X4` | float | 0.0f |  |  | Barometer offset temperature ^4 polynomial coefficient. |
| `TC_B0_X5` | float | 0.0f |  |  | Barometer offset temperature ^5 polynomial coefficient. |
| `TC_B1_ID` | int32 | 0 |  |  | ID of Barometer that the calibration is for. |
| `TC_B1_TMAX` | float | 75.0f |  |  | Barometer calibration maximum temperature. |
| `TC_B1_TMIN` | float | 5.0f |  |  | Barometer calibration minimum temperature. |
| `TC_B1_TREF` | float | 40.0f |  |  | Barometer calibration reference temperature. |
| `TC_B1_X0` | float | 0.0f |  |  | Barometer offset temperature ^0 polynomial coefficient. |
| `TC_B1_X1` | float | 0.0f |  |  | Barometer offset temperature ^1 polynomial coefficients. |
| `TC_B1_X2` | float | 0.0f |  |  | Barometer offset temperature ^2 polynomial coefficient. |
| `TC_B1_X3` | float | 0.0f |  |  | Barometer offset temperature ^3 polynomial coefficient. |
| `TC_B1_X4` | float | 0.0f |  |  | Barometer offset temperature ^4 polynomial coefficient. |
| `TC_B1_X5` | float | 0.0f |  |  | Barometer offset temperature ^5 polynomial coefficient. |
| `TC_B2_ID` | int32 | 0 |  |  | ID of Barometer that the calibration is for. |
| `TC_B2_TMAX` | float | 75.0f |  |  | Barometer calibration maximum temperature. |
| `TC_B2_TMIN` | float | 5.0f |  |  | Barometer calibration minimum temperature. |
| `TC_B2_TREF` | float | 40.0f |  |  | Barometer calibration reference temperature. |
| `TC_B2_X0` | float | 0.0f |  |  | Barometer offset temperature ^0 polynomial coefficient. |
| `TC_B2_X1` | float | 0.0f |  |  | Barometer offset temperature ^1 polynomial coefficients. |
| `TC_B2_X2` | float | 0.0f |  |  | Barometer offset temperature ^2 polynomial coefficient. |
| `TC_B2_X3` | float | 0.0f |  |  | Barometer offset temperature ^3 polynomial coefficient. |
| `TC_B2_X4` | float | 0.0f |  |  | Barometer offset temperature ^4 polynomial coefficient. |
| `TC_B2_X5` | float | 0.0f |  |  | Barometer offset temperature ^5 polynomial coefficient. |
| `TC_B3_ID` | int32 | 0 |  |  | ID of Barometer that the calibration is for. |
| `TC_B3_TMAX` | float | 75.0f |  |  | Barometer calibration maximum temperature. |
| `TC_B3_TMIN` | float | 5.0f |  |  | Barometer calibration minimum temperature. |
| `TC_B3_TREF` | float | 40.0f |  |  | Barometer calibration reference temperature. |
| `TC_B3_X0` | float | 0.0f |  |  | Barometer offset temperature ^0 polynomial coefficient. |
| `TC_B3_X1` | float | 0.0f |  |  | Barometer offset temperature ^1 polynomial coefficients. |
| `TC_B3_X2` | float | 0.0f |  |  | Barometer offset temperature ^2 polynomial coefficient. |
| `TC_B3_X3` | float | 0.0f |  |  | Barometer offset temperature ^3 polynomial coefficient. |
| `TC_B3_X4` | float | 0.0f |  |  | Barometer offset temperature ^4 polynomial coefficient. |
| `TC_B3_X5` | float | 0.0f |  |  | Barometer offset temperature ^5 polynomial coefficient. |
| `TC_B_ENABLE` | int32 | 0 |  |  | Thermal compensation for barometric pressure sensors. |
| `TC_G0_ID` | int32 | 0 |  |  | ID of Gyro that the calibration is for. |
| `TC_G0_TMAX` | float | 100.0f |  |  | Gyro calibration maximum temperature. |
| `TC_G0_TMIN` | float | 0.0f |  |  | Gyro calibration minimum temperature. |
| `TC_G0_TREF` | float | 25.0f |  |  | Gyro calibration reference temperature. |
| `TC_G0_X0_0` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - X axis. |
| `TC_G0_X0_1` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_G0_X0_2` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_G0_X1_0` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - X axis. |
| `TC_G0_X1_1` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_G0_X1_2` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_G0_X2_0` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - X axis. |
| `TC_G0_X2_1` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_G0_X2_2` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_G0_X3_0` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - X axis. |
| `TC_G0_X3_1` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_G0_X3_2` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_G1_ID` | int32 | 0 |  |  | ID of Gyro that the calibration is for. |
| `TC_G1_TMAX` | float | 100.0f |  |  | Gyro calibration maximum temperature. |
| `TC_G1_TMIN` | float | 0.0f |  |  | Gyro calibration minimum temperature. |
| `TC_G1_TREF` | float | 25.0f |  |  | Gyro calibration reference temperature. |
| `TC_G1_X0_0` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - X axis. |
| `TC_G1_X0_1` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_G1_X0_2` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_G1_X1_0` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - X axis. |
| `TC_G1_X1_1` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_G1_X1_2` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_G1_X2_0` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - X axis. |
| `TC_G1_X2_1` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_G1_X2_2` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_G1_X3_0` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - X axis. |
| `TC_G1_X3_1` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_G1_X3_2` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_G2_ID` | int32 | 0 |  |  | ID of Gyro that the calibration is for. |
| `TC_G2_TMAX` | float | 100.0f |  |  | Gyro calibration maximum temperature. |
| `TC_G2_TMIN` | float | 0.0f |  |  | Gyro calibration minimum temperature. |
| `TC_G2_TREF` | float | 25.0f |  |  | Gyro calibration reference temperature. |
| `TC_G2_X0_0` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - X axis. |
| `TC_G2_X0_1` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_G2_X0_2` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_G2_X1_0` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - X axis. |
| `TC_G2_X1_1` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_G2_X1_2` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_G2_X2_0` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - X axis. |
| `TC_G2_X2_1` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_G2_X2_2` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_G2_X3_0` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - X axis. |
| `TC_G2_X3_1` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_G2_X3_2` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_G3_ID` | int32 | 0 |  |  | ID of Gyro that the calibration is for. |
| `TC_G3_TMAX` | float | 100.0f |  |  | Gyro calibration maximum temperature. |
| `TC_G3_TMIN` | float | 0.0f |  |  | Gyro calibration minimum temperature. |
| `TC_G3_TREF` | float | 25.0f |  |  | Gyro calibration reference temperature. |
| `TC_G3_X0_0` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - X axis. |
| `TC_G3_X0_1` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_G3_X0_2` | float | 0.0f |  |  | Gyro rate offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_G3_X1_0` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - X axis. |
| `TC_G3_X1_1` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_G3_X1_2` | float | 0.0f |  |  | Gyro rate offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_G3_X2_0` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - X axis. |
| `TC_G3_X2_1` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_G3_X2_2` | float | 0.0f |  |  | Gyro rate offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_G3_X3_0` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - X axis. |
| `TC_G3_X3_1` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_G3_X3_2` | float | 0.0f |  |  | Gyro rate offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_G_ENABLE` | int32 | 0 |  |  | Thermal compensation for rate gyro sensors. |
| `TC_M0_ID` | int32 | 0 |  |  | ID of Magnetometer that the calibration is for. |
| `TC_M0_TMAX` | float | 100.0f |  |  | Magnetometer calibration maximum temperature. |
| `TC_M0_TMIN` | float | 0.0f |  |  | Magnetometer calibration minimum temperature. |
| `TC_M0_TREF` | float | 25.0f |  |  | Magnetometer calibration reference temperature. |
| `TC_M0_X0_0` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - X axis. |
| `TC_M0_X0_1` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_M0_X0_2` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_M0_X1_0` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - X axis. |
| `TC_M0_X1_1` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_M0_X1_2` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_M0_X2_0` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - X axis. |
| `TC_M0_X2_1` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_M0_X2_2` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_M0_X3_0` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - X axis. |
| `TC_M0_X3_1` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_M0_X3_2` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_M1_ID` | int32 | 0 |  |  | ID of Magnetometer that the calibration is for. |
| `TC_M1_TMAX` | float | 100.0f |  |  | Magnetometer calibration maximum temperature. |
| `TC_M1_TMIN` | float | 0.0f |  |  | Magnetometer calibration minimum temperature. |
| `TC_M1_TREF` | float | 25.0f |  |  | Magnetometer calibration reference temperature. |
| `TC_M1_X0_0` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - X axis. |
| `TC_M1_X0_1` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_M1_X0_2` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_M1_X1_0` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - X axis. |
| `TC_M1_X1_1` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_M1_X1_2` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_M1_X2_0` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - X axis. |
| `TC_M1_X2_1` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_M1_X2_2` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_M1_X3_0` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - X axis. |
| `TC_M1_X3_1` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_M1_X3_2` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_M2_ID` | int32 | 0 |  |  | ID of Magnetometer that the calibration is for. |
| `TC_M2_TMAX` | float | 100.0f |  |  | Magnetometer calibration maximum temperature. |
| `TC_M2_TMIN` | float | 0.0f |  |  | Magnetometer calibration minimum temperature. |
| `TC_M2_TREF` | float | 25.0f |  |  | Magnetometer calibration reference temperature. |
| `TC_M2_X0_0` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - X axis. |
| `TC_M2_X0_1` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_M2_X0_2` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_M2_X1_0` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - X axis. |
| `TC_M2_X1_1` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_M2_X1_2` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_M2_X2_0` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - X axis. |
| `TC_M2_X2_1` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_M2_X2_2` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_M2_X3_0` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - X axis. |
| `TC_M2_X3_1` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_M2_X3_2` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_M3_ID` | int32 | 0 |  |  | ID of Magnetometer that the calibration is for. |
| `TC_M3_TMAX` | float | 100.0f |  |  | Magnetometer calibration maximum temperature. |
| `TC_M3_TMIN` | float | 0.0f |  |  | Magnetometer calibration minimum temperature. |
| `TC_M3_TREF` | float | 25.0f |  |  | Magnetometer calibration reference temperature. |
| `TC_M3_X0_0` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - X axis. |
| `TC_M3_X0_1` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - Y axis. |
| `TC_M3_X0_2` | float | 0.0f |  |  | Magnetometer offset temperature ^0 polynomial coefficient - Z axis. |
| `TC_M3_X1_0` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - X axis. |
| `TC_M3_X1_1` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - Y axis. |
| `TC_M3_X1_2` | float | 0.0f |  |  | Magnetometer offset temperature ^1 polynomial coefficient - Z axis. |
| `TC_M3_X2_0` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - X axis. |
| `TC_M3_X2_1` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - Y axis. |
| `TC_M3_X2_2` | float | 0.0f |  |  | Magnetometer offset temperature ^2 polynomial coefficient - Z axis. |
| `TC_M3_X3_0` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - X axis. |
| `TC_M3_X3_1` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - Y axis. |
| `TC_M3_X3_2` | float | 0.0f |  |  | Magnetometer offset temperature ^3 polynomial coefficient - Z axis. |
| `TC_M_ENABLE` | int32 | 0 |  |  | Thermal compensation for magnetometer sensors. |

## Sensors

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `ADC_ADS1115_EN` | int32 | 0 |  |  | Enable external ADS1115 ADC |
| `BAT1_C_MULT` | float | 1.0f |  |  | Capacity/current multiplier for high-current capable SMBUS battery |
| `BAT1_SMBUS_MODEL` | int32 | 0 | 0 ~ 2 |  | Battery device model |
| `BATMON_ADDR_DFLT` | int32 | 11 |  |  | I2C address for BatMon battery 1 |
| `BATMON_DRIVER_EN` | int32 | 0 | 0 ~ 2 |  | Parameter to enable BatMon module |
| `CAL_AIR_CMODEL` | int32 | 0 |  |  | Airspeed sensor compensation model for the SDP3x |
| `CAL_AIR_TUBED_MM` | float | 1.5f | 1.5 ~ 100 | mm | Airspeed sensor tube diameter. Only used for the Tube Pressure Drop Compensation. |
| `CAL_AIR_TUBELEN` | float | 0.2f | 0.01 ~ 2.00 | m | Airspeed sensor tube length. |
| `CAL_MAG_SIDES` | int32 | 63 |  |  | For legacy QGC support only |
| `ILABS_MODE` | enum | 0 |  |  | InertialLabs INS sensor mode configuration |
| `IMU_ACCEL_CUTOFF` | float | 30.0f | 0 ~ 1000 | Hz | Low pass filter cutoff frequency for accel |
| `IMU_DGYRO_CUTOFF` | float | 20.0f | 0 ~ 1000 | Hz | Cutoff frequency for angular acceleration (D-Term filter) |
| `IMU_GYRO_CAL_EN` | int32 | 1 |  |  | IMU gyro auto calibration enable. |
| `IMU_GYRO_CUTOFF` | float | 40.0f | 0 ~ 1000 | Hz | Low pass filter cutoff frequency for gyro |
| `IMU_GYRO_DNF_BW` | float | 15.f | 5 ~ 30 | Hz | IMU gyro ESC notch filter bandwidth |
| `IMU_GYRO_DNF_EN` | int32 | 0 | 0 ~ 3 |  | IMU gyro dynamic notch filtering |
| `IMU_GYRO_DNF_HMC` | int32 | 3 | 1 ~ 7 |  | IMU gyro dynamic notch filter harmonics |
| `IMU_GYRO_DNF_MIN` | float | 25.f |  | Hz | IMU gyro dynamic notch filter minimum frequency |
| `IMU_GYRO_FFT_EN` | int32 | 0 |  |  | IMU gyro FFT enable. |
| `IMU_GYRO_FFT_LEN` | int32 | 512 |  | Hz | IMU gyro FFT length. |
| `IMU_GYRO_FFT_MAX` | float | 150.f | 1 ~ 1000 | Hz | IMU gyro FFT maximum frequency. |
| `IMU_GYRO_FFT_MIN` | float | 30.f | 1 ~ 1000 | Hz | IMU gyro FFT minimum frequency. |
| `IMU_GYRO_FFT_SNR` | float | 10.f | 1 ~ 30 |  | IMU gyro FFT SNR. |
| `IMU_GYRO_NF0_BW` | float | 20.0f | 0 ~ 100 | Hz | Notch filter bandwidth for gyro |
| `IMU_GYRO_NF0_FRQ` | float | 0.0f | 0 ~ 1000 | Hz | Notch filter frequency for gyro |
| `IMU_GYRO_NF1_BW` | float | 20.0f | 0 ~ 100 | Hz | Notch filter 1 bandwidth for gyro |
| `IMU_GYRO_NF1_FRQ` | float | 0.0f | 0 ~ 1000 | Hz | Notch filter 2 frequency for gyro |
| `IMU_GYRO_RATEMAX` | int32 | 400 | 100 ~ 2000 | Hz | Gyro control data maximum publication rate (inner loop rate) |
| `IMU_INTEG_RATE` | int32 | 200 | 100 ~ 1000 | Hz | IMU integration rate. |
| `INA220_CONFIG` | int32 | 8607 | 0 ~ 65535 |  | INA220 Power Monitor Config |
| `INA220_CUR_BAT` | float | 164.0f | 0.1 ~ 500.0 |  | INA220 Power Monitor Battery Max Current |
| `INA220_CUR_REG` | float | 164.0f | 0.1 ~ 500.0 |  | INA220 Power Monitor Regulator Max Current |
| `INA220_SHUNT_BAT` | float | 0.0005f | 0.000000001 ~ 0.1 |  | INA220 Power Monitor Battery Shunt |
| `INA220_SHUNT_REG` | float | 0.0005f | 0.000000001 ~ 0.1 |  | INA220 Power Monitor Regulator Shunt |
| `INA226_CONFIG` | int32 | 18139 | 0 ~ 65535 |  | INA226 Power Monitor Config |
| `INA226_CURRENT` | float | 164.0f | 0.1 ~ 200.0 |  | INA226 Power Monitor Max Current |
| `INA226_SHUNT` | float | 0.0005f | 0.000000001 ~ 0.1 |  | INA226 Power Monitor Shunt |
| `INA228_CONFIG` | int32 | 63779 | 0 ~ 65535 |  | INA228 Power Monitor Config |
| `INA228_CURRENT` | float | 327.68f | 0.1 ~ 327.68 |  | INA228 Power Monitor Max Current |
| `INA228_SHUNT` | float | 0.0005f | 0.000000001 ~ 0.1 |  | INA228 Power Monitor Shunt |
| `INA238_CURRENT` | float | 327.68f | 0.1 ~ 327.68 |  | INA238 Power Monitor Max Current |
| `INA238_SHUNT` | float | 0.0005f | 0.000000001 ~ 0.1 |  | INA238 Power Monitor Shunt |
| `MS_ACCEL_RANGE` | int32 | -1 |  |  | MicroStrain accelerometer range |
| `MS_ALIGNMENT` | bitmask | 2 | 1 ~ 15 |  | MicroStrain heading alignment type |
| `MS_BARO_RATE_HZ` | int32 | 50 | 0 ~ 1000 |  | MicroStrain barometer data rate |
| `MS_EHEAD_YAW` | float | 0.0 |  |  | MicroStrain External Heading Orientation (Yaw) |
| `MS_EMAG_PTCH` | float | 0.0 |  |  | MicroStrain External Magnetometer Orientation (Pitch) |
| `MS_EMAG_ROLL` | float | 0.0 |  |  | MicroStrain External Magnetometer Orientation (Roll) |
| `MS_EMAG_UNCERT` | float | 0.1 |  |  | MicroStrain external magnetometer uncertainty |
| `MS_EMAG_YAW` | float | 0.0 |  |  | MicroStrain External Magnetometer Orientation (Yaw) |
| `MS_EXT_HEAD_EN` | enum | 0 |  |  | Enable MicroStrain external heading aiding |
| `MS_EXT_MAG_EN` | enum | 0 |  |  | Enable MicroStrain external magnetometer aiding |
| `MS_FILT_RATE_HZ` | int32 | 250 | 0 ~ 1000 |  | MicroStrain EKF data rate |
| `MS_GNSS_AID_SRC` | enum | 1 |  |  | MicroStrain GNSS aiding source control |
| `MS_GNSS_OFF1_X` | float | 0.0 |  |  | MicroStrain GNSS lever arm offset 1 (X) |
| `MS_GNSS_OFF1_Y` | float | 0.0 |  |  | MicroStrain GNSS lever arm offset 1 (Y) |
| `MS_GNSS_OFF1_Z` | float | 0.0 |  |  | MicroStrain GNSS lever arm offset 1 (Z) |
| `MS_GNSS_OFF2_X` | float | 0.0 |  |  | MicroStrain GNSS lever arm offset 2 (X) |
| `MS_GNSS_OFF2_Y` | float | 0.0 |  |  | MicroStrain GNSS lever arm offset 2 (Y) |
| `MS_GNSS_OFF2_Z` | float | 0.0 |  |  | MicroStrain GNSS lever arm offset 2 (Z) |
| `MS_GNSS_RATE_HZ` | int32 | 5 | 0 ~ 5 |  | MicroStrain GNSS data rate |
| `MS_GYRO_RANGE` | int32 | -1 |  |  | MicroStrain gyroscope range |
| `MS_IMU_RATE_HZ` | int32 | 500 | 0 ~ 1000 |  | MicroStrain IMU data rate |
| `MS_INT_HEAD_EN` | enum | 0 |  |  | Enable MicroStrain internal heading aiding |
| `MS_INT_MAG_EN` | enum | 0 |  |  | Enable MicroStrain internal magnetometer |
| `MS_MAG_RATE_HZ` | int32 | 50 | 0 ~ 1000 |  | MicroStrain magnetometer data rate |
| `MS_MODE` | enum | 0 |  |  | MicroStrain device mode |
| `MS_OFLW_OFF_X` | float | 0.0 |  |  | MicroStrain optical flow offset (X) |
| `MS_OFLW_OFF_Y` | float | 0.0 |  |  | MicroStrain optical flow offset (Y) |
| `MS_OFLW_OFF_Z` | float | 0.0 |  |  | MicroStrain optical flow offset (Z) |
| `MS_OFLW_UNCERT` | float | 0.1 |  |  | MicroStrain optical flow uncertainty |
| `MS_OPT_FLOW_EN` | enum | 0 |  |  | Enable MicroStrain optical flow aiding |
| `MS_SENSOR_PTCH` | float | 0.0 |  |  | MicroStrain Sensor to Vehicle Transform (Pitch) |
| `MS_SENSOR_ROLL` | float | 0.0 |  |  | MicroStrain Sensor to vehicle transform (Roll) |
| `MS_SENSOR_YAW` | float | 0.0 |  |  | MicroStrain Sensor to Vehicle Transform (Yaw) |
| `MS_SVT_EN` | enum | 0 |  |  | Enables Microstrain sensor to vehicle transform |
| `PCF8583_MAGNET` | int32 | 2 | 1 ~  |  | PCF8583 rotorfreq (i2c) pulse count |
| `PCF8583_POOL` | int32 | 1000000 |  | us | PCF8583 rotorfreq (i2c) pool interval |
| `PCF8583_RESET` | int32 | 500000 |  |  | PCF8583 rotorfreq (i2c) pulse reset value |
| `SBG_BAUDRATE` | int32 | 921600 | 9600 ~ 921600 |  | sbgECom driver baudrate |
| `SBG_CONFIGURE_EN` | boolean | 0 |  |  | sbgECom driver INS configuration enable |
| `SBG_MODE` | enum | 2 |  |  | sbgECom driver mode |
| `SENS_AFBR_HYSTER` | int32 | 1 | 1 ~ 10 | m | AFBR Rangefinder Short/Long Range Threshold Hysteresis |
| `SENS_AFBR_L_RATE` | int32 | 25 | 1 ~ 100 |  | AFBR Rangefinder Long Range Rate |
| `SENS_AFBR_MODE` | int32 | 0 | 0 ~ 3 |  | AFBR Rangefinder Mode |
| `SENS_AFBR_S_RATE` | int32 | 50 | 1 ~ 100 |  | AFBR Rangefinder Short Range Rate |
| `SENS_AFBR_THRESH` | int32 | 4 | 1 ~ 50 | m | AFBR Rangefinder Short/Long Range Threshold |
| `SENS_BARO_QNH` | float | 1013.25f | 500 ~ 1500 | hPa | QNH for barometer |
| `SENS_BARO_RATE` | float | 20.0f | 1 ~ 200 | Hz | Baro max rate. |
| `SENS_BAR_AUTOCAL` | int32 | 1 |  |  | Barometer auto calibration |
| `SENS_BOARD_ROT` | int32 | 0 | -1 ~ 40 |  | Board rotation |
| `SENS_BOARD_X_OFF` | float | 0.0f | -45.0 ~ 45.0 | deg | Board rotation X (roll) offset |
| `SENS_BOARD_Y_OFF` | float | 0.0f | -45.0 ~ 45.0 | deg | Board rotation Y (pitch) offset |
| `SENS_BOARD_Z_OFF` | float | 0.0f | -45.0 ~ 45.0 | deg | Board rotation Z (yaw) offset |
| `SENS_CM8JL65_R_0` | enum | 25 |  |  | Distance Sensor Rotation |
| `SENS_EN_ADIS164X` | int32 | 0 | 0 ~ 1 |  | Analog Devices ADIS16448 IMU (external SPI) |
| `SENS_EN_ADIS165X` | int32 | 0 |  |  | Analog Devices ADIS16507 IMU (external SPI) |
| `SENS_EN_AGPSIM` | int32 | 0 | 0 ~ 1 |  | Simulate Aux Global Position (AGP) |
| `SENS_EN_ARSPDSIM` | int32 | 0 | 0 ~ 1 |  | Enable simulated airspeed sensor instance |
| `SENS_EN_ASP5033` | int32 | 0 |  |  | ASP5033 differential pressure sensor (external I2C) |
| `SENS_EN_AUAVX` | int32 | 0 |  |  | Amphenol AUAV differential / absolute pressure sensor (external I2C) |
| `SENS_EN_BAROSIM` | int32 | 0 | 0 ~ 1 |  | Enable simulated barometer sensor instance |
| `SENS_EN_BATT` | int32 | 0 |  |  | SMBUS Smart battery driver BQ40Z50 and BQ40Z80 |
| `SENS_EN_ETSASPD` | int32 | 0 |  |  | Eagle Tree airspeed sensor (external I2C) |
| `SENS_EN_GPSSIM` | int32 | 0 | 0 ~ 1 |  | Enable simulated GPS sinstance |
| `SENS_EN_INA220` | int32 | 0 |  |  | Enable INA220 Power Monitor |
| `SENS_EN_INA226` | int32 | 0 |  |  | Enable INA226 Power Monitor |
| `SENS_EN_INA228` | int32 | 0 |  |  | Enable INA228 Power Monitor |
| `SENS_EN_INA238` | int32 | 0 |  |  | Enable INA238 Power Monitor |
| `SENS_EN_IRLOCK` | int32 | 0 |  |  | IR-LOCK Sensor (external I2C) |
| `SENS_EN_LL40LS` | int32 | 0 | 0 ~ 2 |  | Lidar-Lite (LL40LS) |
| `SENS_EN_MAGSIM` | int32 | 0 | 0 ~ 1 |  | Enable simulated magnetometer sensor instance |
| `SENS_EN_MB12XX` | int32 | 0 |  |  | Maxbotix Sonar (mb12xx) |
| `SENS_EN_MPDT` | int32 | 0 | 0 ~ 1 |  | Enable Mappydot rangefinder (i2c) |
| `SENS_EN_MS4515` | int32 | 0 |  |  | TE MS4515 differential pressure sensor (external I2C) |
| `SENS_EN_MS4525DO` | int32 | 0 |  |  | TE MS4525DO differential pressure sensor (external I2C) |
| `SENS_EN_MS5525DS` | int32 | 0 |  |  | TE MS5525DSO differential pressure sensor (external I2C) |
| `SENS_EN_PAA3905` | int32 | 0 |  |  | PAA3905 Optical Flow |
| `SENS_EN_PAW3902` | int32 | 0 |  |  | PAW3902/PAW3903 Optical Flow |
| `SENS_EN_PCF8583` | int32 | 0 | 0 ~ 1 |  | PCF8583 eneable driver |
| `SENS_EN_PGA460` | int32 | 0 |  |  | PGA460 Ultrasonic driver (PGA460) |
| `SENS_EN_PMW3901` | int32 | 0 |  |  | PMW3901 Optical Flow |
| `SENS_EN_PX4FLOW` | int32 | 0 |  |  | PX4 Flow Optical Flow |
| `SENS_EN_SCH16T` | int32 | 0 | 0 ~ 1 |  | Murata SCH16T IMU (external SPI) |
| `SENS_EN_SDP3X` | int32 | 0 |  |  | Sensirion SDP3X differential pressure sensor (external I2C) |
| `SENS_EN_SF0X` | int32 | 1 |  |  | Lightware Laser Rangefinder hardware model (serial) |
| `SENS_EN_SF1XX` | int32 | 0 | 0 ~ 7 |  | Lightware SF1xx/SF20/LW20 laser rangefinder (i2c) |
| `SENS_EN_SHT3X` | int32 | 0 |  |  | SHT3x temperature and hygrometer |
| `SENS_EN_SPA06` | int32 | 0 |  |  | Goertek SPA06 Barometer (external I2C) |
| `SENS_EN_SPL06` | int32 | 0 |  |  | Goertek SPL06 Barometer (external I2C) |
| `SENS_EN_SR05` | int32 | 0 |  |  | HY-SRF05 / HC-SR05 |
| `SENS_EN_TF02PRO` | int32 | 0 |  |  | TF02 Pro Distance Sensor (i2c) |
| `SENS_EN_THERMAL` | int32 | -1 |  |  | Thermal control of sensor temperature |
| `SENS_EN_TRANGER` | int32 | 0 | 0 ~ 3 |  | TeraRanger Rangefinder (i2c) |
| `SENS_EN_VL53L0X` | int32 | 0 |  |  | VL53L0X Distance Sensor |
| `SENS_EN_VL53L1X` | int32 | 0 |  |  | VL53L1X Distance Sensor |
| `SENS_EXT_I2C_PRB` | int32 | 1 |  |  | External I2C probe. |
| `SENS_FLOW_RATE` | float | 70.0f | 1 ~ 200 | Hz | Optical flow max rate. |
| `SENS_FLOW_ROT` | int32 | 0 |  |  | Optical flow rotation |
| `SENS_FLOW_SCALE` | float | 1.f | 0.5 ~ 1.5 |  | Optical flow scale factor |
| `SENS_GPS_MASK` | int32 | 7 | 0 ~ 7 |  | Multi GPS Blending Control Mask. |
| `SENS_GPS_PRIME` | int32 | 0 | -1 ~ 1 |  | Multi GPS primary instance |
| `SENS_GPS_TAU` | float | 10.0f | 1.0 ~ 100.0 | s | Multi GPS Blending Time Constant |
| `SENS_IMU_AUTOCAL` | int32 | 1 |  |  | IMU auto calibration |
| `SENS_IMU_CLPNOTI` | int32 | 1 |  |  | IMU notify clipping |
| `SENS_IMU_MODE` | int32 | 1 |  |  | Sensors hub IMU mode |
| `SENS_IMU_TEMP` | float | 55.0f | 0 ~ 85.0 | celcius | Target IMU temperature. |
| `SENS_IMU_TEMP_FF` | float | 0.05f | 0 ~ 1.0 | % | IMU heater controller feedforward value. |
| `SENS_IMU_TEMP_I` | float | 0.025f | 0 ~ 1.0 | us/C | IMU heater controller integrator gain value. |
| `SENS_IMU_TEMP_P` | float | 1.0f | 0 ~ 2.0 | us/C | IMU heater controller proportional gain value. |
| `SENS_INT_BARO_EN` | int32 | 1 |  |  | Enable internal barometers |
| `SENS_MAG_AUTOCAL` | int32 | 1 |  |  | Magnetometer auto calibration |
| `SENS_MAG_AUTOROT` | int32 | 1 |  |  | Automatically set external rotations. |
| `SENS_MAG_MODE` | int32 | 1 |  |  | Sensors hub mag mode |
| `SENS_MAG_RATE` | float | 15.0f | 1 ~ 200 | Hz | Magnetometer max rate. |
| `SENS_MAG_SIDES` | int32 | 63 | 34 ~ 63 |  | Bitfield selecting mag sides for calibration |
| `SENS_MB12_0_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 0 Rotation |
| `SENS_MB12_10_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 10 Rotation |
| `SENS_MB12_11_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 12 Rotation |
| `SENS_MB12_1_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 1 Rotation |
| `SENS_MB12_2_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 2 Rotation |
| `SENS_MB12_3_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 3 Rotation |
| `SENS_MB12_4_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 4 Rotation |
| `SENS_MB12_5_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 5 Rotation |
| `SENS_MB12_6_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 6 Rotation |
| `SENS_MB12_7_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 7 Rotation |
| `SENS_MB12_8_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 8 Rotation |
| `SENS_MB12_9_ROT` | int32 | 0 | 0 ~ 7 |  | MaxBotix MB12XX Sensor 9 Rotation |
| `SENS_MPDT0_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 0 Rotation |
| `SENS_MPDT10_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 10 Rotation |
| `SENS_MPDT11_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 12 Rotation |
| `SENS_MPDT1_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 1 Rotation |
| `SENS_MPDT2_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 2 Rotation |
| `SENS_MPDT3_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 3 Rotation |
| `SENS_MPDT4_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 4 Rotation |
| `SENS_MPDT5_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 5 Rotation |
| `SENS_MPDT6_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 6 Rotation |
| `SENS_MPDT7_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 7 Rotation |
| `SENS_MPDT8_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 8 Rotation |
| `SENS_MPDT9_ROT` | int32 | 0 | 0 ~ 7 |  | MappyDot Sensor 9 Rotation |
| `SENS_OR_ADIS164X` | int32 | 0 | 0 ~ 101 |  | Analog Devices ADIS16448 IMU Orientation(external SPI) |
| `SENS_TEMP_ID` | int32 | 0 |  |  | Target IMU device ID to regulate temperature. |
| `SENS_TFMINI_HW` | enum | 1 | 1 ~ 3 |  | Hardware Model |
| `SF45_ORIENT_CFG` | enum | 24 |  |  | Orientation upright or facing downward |
| `SF45_UPDATE_CFG` | enum | 5 |  |  | Update rate in Hz |
| `SF45_YAW_CFG` | enum | 0 |  |  | Sensor facing forward or backward |
| `SIM_ARSPD_FAIL` | int32 | 0 | 0 ~ 1 |  | Dynamically simulate failure of airspeed sensor instance |
| `VN_MODE` | enum | 0 |  |  | VectorNav driver mode |
| `VOXLPM_SHUNT_BAT` | float | 0.00063f | 0.000000001 ~ 0.1 |  | VOXL Power Monitor Shunt, Battery |
| `VOXLPM_SHUNT_REG` | float | 0.0056f | 0.000000001 ~ 0.1 |  | VOXL Power Monitor Shunt, Regulator |

## Sensor Calibration

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `CAL_ACC0_ID` | int32 | 0 |  |  | Accelerometer ${i} calibration device ID |
| `CAL_ACC0_PRIO` | enum | -1 |  |  | Accelerometer ${i} priority |
| `CAL_ACC0_ROT` | enum | -1 | -1 ~ 40 |  | Accelerometer ${i} rotation relative to airframe |
| `CAL_ACC0_XOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} X-axis offset |
| `CAL_ACC0_XSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} X-axis scaling factor |
| `CAL_ACC0_YOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} Y-axis offset |
| `CAL_ACC0_YSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} Y-axis scaling factor |
| `CAL_ACC0_ZOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} Z-axis offset |
| `CAL_ACC0_ZSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} Z-axis scaling factor |
| `CAL_ACC1_ID` | int32 | 0 |  |  | Accelerometer ${i} calibration device ID |
| `CAL_ACC1_PRIO` | enum | -1 |  |  | Accelerometer ${i} priority |
| `CAL_ACC1_ROT` | enum | -1 | -1 ~ 40 |  | Accelerometer ${i} rotation relative to airframe |
| `CAL_ACC1_XOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} X-axis offset |
| `CAL_ACC1_XSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} X-axis scaling factor |
| `CAL_ACC1_YOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} Y-axis offset |
| `CAL_ACC1_YSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} Y-axis scaling factor |
| `CAL_ACC1_ZOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} Z-axis offset |
| `CAL_ACC1_ZSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} Z-axis scaling factor |
| `CAL_ACC2_ID` | int32 | 0 |  |  | Accelerometer ${i} calibration device ID |
| `CAL_ACC2_PRIO` | enum | -1 |  |  | Accelerometer ${i} priority |
| `CAL_ACC2_ROT` | enum | -1 | -1 ~ 40 |  | Accelerometer ${i} rotation relative to airframe |
| `CAL_ACC2_XOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} X-axis offset |
| `CAL_ACC2_XSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} X-axis scaling factor |
| `CAL_ACC2_YOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} Y-axis offset |
| `CAL_ACC2_YSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} Y-axis scaling factor |
| `CAL_ACC2_ZOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} Z-axis offset |
| `CAL_ACC2_ZSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} Z-axis scaling factor |
| `CAL_ACC3_ID` | int32 | 0 |  |  | Accelerometer ${i} calibration device ID |
| `CAL_ACC3_PRIO` | enum | -1 |  |  | Accelerometer ${i} priority |
| `CAL_ACC3_ROT` | enum | -1 | -1 ~ 40 |  | Accelerometer ${i} rotation relative to airframe |
| `CAL_ACC3_XOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} X-axis offset |
| `CAL_ACC3_XSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} X-axis scaling factor |
| `CAL_ACC3_YOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} Y-axis offset |
| `CAL_ACC3_YSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} Y-axis scaling factor |
| `CAL_ACC3_ZOFF` | float | 0.0 |  | m/s^2 | Accelerometer ${i} Z-axis offset |
| `CAL_ACC3_ZSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Accelerometer ${i} Z-axis scaling factor |
| `CAL_BARO0_ID` | int32 | 0 |  |  | Barometer ${i} calibration device ID |
| `CAL_BARO0_OFF` | float | 0.0 |  |  | Barometer ${i} offset |
| `CAL_BARO0_PRIO` | enum | -1 |  |  | Barometer ${i} priority |
| `CAL_BARO1_ID` | int32 | 0 |  |  | Barometer ${i} calibration device ID |
| `CAL_BARO1_OFF` | float | 0.0 |  |  | Barometer ${i} offset |
| `CAL_BARO1_PRIO` | enum | -1 |  |  | Barometer ${i} priority |
| `CAL_BARO2_ID` | int32 | 0 |  |  | Barometer ${i} calibration device ID |
| `CAL_BARO2_OFF` | float | 0.0 |  |  | Barometer ${i} offset |
| `CAL_BARO2_PRIO` | enum | -1 |  |  | Barometer ${i} priority |
| `CAL_BARO3_ID` | int32 | 0 |  |  | Barometer ${i} calibration device ID |
| `CAL_BARO3_OFF` | float | 0.0 |  |  | Barometer ${i} offset |
| `CAL_BARO3_PRIO` | enum | -1 |  |  | Barometer ${i} priority |
| `CAL_GYRO0_ID` | int32 | 0 |  |  | Gyroscope ${i} calibration device ID |
| `CAL_GYRO0_PRIO` | enum | -1 |  |  | Gyroscope ${i} priority |
| `CAL_GYRO0_ROT` | enum | -1 | -1 ~ 40 |  | Gyroscope ${i} rotation relative to airframe |
| `CAL_GYRO0_XOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} X-axis offset |
| `CAL_GYRO0_YOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} Y-axis offset |
| `CAL_GYRO0_ZOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} Z-axis offset |
| `CAL_GYRO1_ID` | int32 | 0 |  |  | Gyroscope ${i} calibration device ID |
| `CAL_GYRO1_PRIO` | enum | -1 |  |  | Gyroscope ${i} priority |
| `CAL_GYRO1_ROT` | enum | -1 | -1 ~ 40 |  | Gyroscope ${i} rotation relative to airframe |
| `CAL_GYRO1_XOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} X-axis offset |
| `CAL_GYRO1_YOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} Y-axis offset |
| `CAL_GYRO1_ZOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} Z-axis offset |
| `CAL_GYRO2_ID` | int32 | 0 |  |  | Gyroscope ${i} calibration device ID |
| `CAL_GYRO2_PRIO` | enum | -1 |  |  | Gyroscope ${i} priority |
| `CAL_GYRO2_ROT` | enum | -1 | -1 ~ 40 |  | Gyroscope ${i} rotation relative to airframe |
| `CAL_GYRO2_XOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} X-axis offset |
| `CAL_GYRO2_YOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} Y-axis offset |
| `CAL_GYRO2_ZOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} Z-axis offset |
| `CAL_GYRO3_ID` | int32 | 0 |  |  | Gyroscope ${i} calibration device ID |
| `CAL_GYRO3_PRIO` | enum | -1 |  |  | Gyroscope ${i} priority |
| `CAL_GYRO3_ROT` | enum | -1 | -1 ~ 40 |  | Gyroscope ${i} rotation relative to airframe |
| `CAL_GYRO3_XOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} X-axis offset |
| `CAL_GYRO3_YOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} Y-axis offset |
| `CAL_GYRO3_ZOFF` | float | 0.0 |  | rad/s | Gyroscope ${i} Z-axis offset |
| `CAL_MAG0_ID` | int32 | 0 |  |  | Magnetometer ${i} calibration device ID |
| `CAL_MAG0_PITCH` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Pitch Angle |
| `CAL_MAG0_PRIO` | enum | -1 |  |  | Magnetometer ${i} priority |
| `CAL_MAG0_ROLL` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Roll Angle |
| `CAL_MAG0_ROT` | enum | -1 | -1 ~ 100 |  | Magnetometer ${i} rotation relative to airframe |
| `CAL_MAG0_XCOMP` | float | 0.0 |  |  | Magnetometer ${i} X Axis throttle compensation |
| `CAL_MAG0_XODIAG` | float | 0.0 |  |  | Magnetometer ${i} X-axis off diagonal scale factor |
| `CAL_MAG0_XOFF` | float | 0.0 |  | gauss | Magnetometer ${i} X-axis offset |
| `CAL_MAG0_XSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} X-axis scaling factor |
| `CAL_MAG0_YAW` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Yaw Angle |
| `CAL_MAG0_YCOMP` | float | 0.0 |  |  | Magnetometer ${i} Y Axis throttle compensation |
| `CAL_MAG0_YODIAG` | float | 0.0 |  |  | Magnetometer ${i} Y-axis off diagonal scale factor |
| `CAL_MAG0_YOFF` | float | 0.0 |  | gauss | Magnetometer ${i} Y-axis offset |
| `CAL_MAG0_YSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} Y-axis scaling factor |
| `CAL_MAG0_ZCOMP` | float | 0.0 |  |  | Magnetometer ${i} Z Axis throttle compensation |
| `CAL_MAG0_ZODIAG` | float | 0.0 |  |  | Magnetometer ${i} Z-axis off diagonal scale factor |
| `CAL_MAG0_ZOFF` | float | 0.0 |  | gauss | Magnetometer ${i} Z-axis offset |
| `CAL_MAG0_ZSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} Z-axis scaling factor |
| `CAL_MAG1_ID` | int32 | 0 |  |  | Magnetometer ${i} calibration device ID |
| `CAL_MAG1_PITCH` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Pitch Angle |
| `CAL_MAG1_PRIO` | enum | -1 |  |  | Magnetometer ${i} priority |
| `CAL_MAG1_ROLL` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Roll Angle |
| `CAL_MAG1_ROT` | enum | -1 | -1 ~ 100 |  | Magnetometer ${i} rotation relative to airframe |
| `CAL_MAG1_XCOMP` | float | 0.0 |  |  | Magnetometer ${i} X Axis throttle compensation |
| `CAL_MAG1_XODIAG` | float | 0.0 |  |  | Magnetometer ${i} X-axis off diagonal scale factor |
| `CAL_MAG1_XOFF` | float | 0.0 |  | gauss | Magnetometer ${i} X-axis offset |
| `CAL_MAG1_XSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} X-axis scaling factor |
| `CAL_MAG1_YAW` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Yaw Angle |
| `CAL_MAG1_YCOMP` | float | 0.0 |  |  | Magnetometer ${i} Y Axis throttle compensation |
| `CAL_MAG1_YODIAG` | float | 0.0 |  |  | Magnetometer ${i} Y-axis off diagonal scale factor |
| `CAL_MAG1_YOFF` | float | 0.0 |  | gauss | Magnetometer ${i} Y-axis offset |
| `CAL_MAG1_YSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} Y-axis scaling factor |
| `CAL_MAG1_ZCOMP` | float | 0.0 |  |  | Magnetometer ${i} Z Axis throttle compensation |
| `CAL_MAG1_ZODIAG` | float | 0.0 |  |  | Magnetometer ${i} Z-axis off diagonal scale factor |
| `CAL_MAG1_ZOFF` | float | 0.0 |  | gauss | Magnetometer ${i} Z-axis offset |
| `CAL_MAG1_ZSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} Z-axis scaling factor |
| `CAL_MAG2_ID` | int32 | 0 |  |  | Magnetometer ${i} calibration device ID |
| `CAL_MAG2_PITCH` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Pitch Angle |
| `CAL_MAG2_PRIO` | enum | -1 |  |  | Magnetometer ${i} priority |
| `CAL_MAG2_ROLL` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Roll Angle |
| `CAL_MAG2_ROT` | enum | -1 | -1 ~ 100 |  | Magnetometer ${i} rotation relative to airframe |
| `CAL_MAG2_XCOMP` | float | 0.0 |  |  | Magnetometer ${i} X Axis throttle compensation |
| `CAL_MAG2_XODIAG` | float | 0.0 |  |  | Magnetometer ${i} X-axis off diagonal scale factor |
| `CAL_MAG2_XOFF` | float | 0.0 |  | gauss | Magnetometer ${i} X-axis offset |
| `CAL_MAG2_XSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} X-axis scaling factor |
| `CAL_MAG2_YAW` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Yaw Angle |
| `CAL_MAG2_YCOMP` | float | 0.0 |  |  | Magnetometer ${i} Y Axis throttle compensation |
| `CAL_MAG2_YODIAG` | float | 0.0 |  |  | Magnetometer ${i} Y-axis off diagonal scale factor |
| `CAL_MAG2_YOFF` | float | 0.0 |  | gauss | Magnetometer ${i} Y-axis offset |
| `CAL_MAG2_YSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} Y-axis scaling factor |
| `CAL_MAG2_ZCOMP` | float | 0.0 |  |  | Magnetometer ${i} Z Axis throttle compensation |
| `CAL_MAG2_ZODIAG` | float | 0.0 |  |  | Magnetometer ${i} Z-axis off diagonal scale factor |
| `CAL_MAG2_ZOFF` | float | 0.0 |  | gauss | Magnetometer ${i} Z-axis offset |
| `CAL_MAG2_ZSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} Z-axis scaling factor |
| `CAL_MAG3_ID` | int32 | 0 |  |  | Magnetometer ${i} calibration device ID |
| `CAL_MAG3_PITCH` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Pitch Angle |
| `CAL_MAG3_PRIO` | enum | -1 |  |  | Magnetometer ${i} priority |
| `CAL_MAG3_ROLL` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Roll Angle |
| `CAL_MAG3_ROT` | enum | -1 | -1 ~ 100 |  | Magnetometer ${i} rotation relative to airframe |
| `CAL_MAG3_XCOMP` | float | 0.0 |  |  | Magnetometer ${i} X Axis throttle compensation |
| `CAL_MAG3_XODIAG` | float | 0.0 |  |  | Magnetometer ${i} X-axis off diagonal scale factor |
| `CAL_MAG3_XOFF` | float | 0.0 |  | gauss | Magnetometer ${i} X-axis offset |
| `CAL_MAG3_XSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} X-axis scaling factor |
| `CAL_MAG3_YAW` | float | 0.0 | -180 ~ 180 | deg | Magnetometer ${i} Custom Euler Yaw Angle |
| `CAL_MAG3_YCOMP` | float | 0.0 |  |  | Magnetometer ${i} Y Axis throttle compensation |
| `CAL_MAG3_YODIAG` | float | 0.0 |  |  | Magnetometer ${i} Y-axis off diagonal scale factor |
| `CAL_MAG3_YOFF` | float | 0.0 |  | gauss | Magnetometer ${i} Y-axis offset |
| `CAL_MAG3_YSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} Y-axis scaling factor |
| `CAL_MAG3_ZCOMP` | float | 0.0 |  |  | Magnetometer ${i} Z Axis throttle compensation |
| `CAL_MAG3_ZODIAG` | float | 0.0 |  |  | Magnetometer ${i} Z-axis off diagonal scale factor |
| `CAL_MAG3_ZOFF` | float | 0.0 |  | gauss | Magnetometer ${i} Z-axis offset |
| `CAL_MAG3_ZSCALE` | float | 1.0 | 0.1 ~ 3.0 |  | Magnetometer ${i} Z-axis scaling factor |
| `CAL_MAG_COMP_TYP` | int32 | 0 |  |  | Type of magnetometer compensation |
| `SENS_DPRES_ANSC` | float | 0 |  |  | Differential pressure sensor analog scaling |
| `SENS_DPRES_OFF` | float | 0.0f |  |  | Differential pressure sensor offset |
| `SENS_DPRES_REV` | int32 | 0 |  |  | Reverse differential pressure sensor readings |
| `SENS_FLOW_MAXHGT` | float | 100.f | 1.0 ~ 100.0 | m | Maximum height above ground when reliant on optical flow. |
| `SENS_FLOW_MAXR` | float | 8.f | 1.0 ~  | rad/s | Magnitude of maximum angular flow rate reliably measurable by the optical flow sensor. |
| `SENS_FLOW_MINHGT` | float | 0.08f | 0.0 ~ 1.0 | m | Minimum height above ground when reliant on optical flow. |

## Radio Calibration

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RC10_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 10 maximum |
| `RC10_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 10 minimum |
| `RC10_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 10 reverse |
| `RC10_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 10 trim |
| `RC11_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 11 maximum |
| `RC11_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 11 minimum |
| `RC11_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 11 reverse |
| `RC11_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 11 trim |
| `RC12_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 12 maximum |
| `RC12_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 12 minimum |
| `RC12_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 12 reverse |
| `RC12_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 12 trim |
| `RC13_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 13 maximum |
| `RC13_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 13 minimum |
| `RC13_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 13 reverse |
| `RC13_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 13 trim |
| `RC14_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 14 maximum |
| `RC14_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 14 minimum |
| `RC14_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 14 reverse |
| `RC14_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 14 trim |
| `RC15_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 15 maximum |
| `RC15_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 15 minimum |
| `RC15_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 15 reverse |
| `RC15_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 15 trim |
| `RC16_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 16 maximum |
| `RC16_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 16 minimum |
| `RC16_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 16 reverse |
| `RC16_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 16 trim |
| `RC17_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 17 maximum |
| `RC17_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 17 minimum |
| `RC17_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 17 reverse |
| `RC17_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 17 trim |
| `RC18_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 18 maximum |
| `RC18_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 18 minimum |
| `RC18_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 18 reverse |
| `RC18_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 18 trim |
| `RC1_MAX` | float | 2000.0f | 1500.0 ~ 2200.0 | us | RC channel 1 maximum |
| `RC1_MIN` | float | 1000.0f | 800.0 ~ 1500.0 | us | RC channel 1 minimum |
| `RC1_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 1 reverse |
| `RC1_TRIM` | float | 1500.0f | 800.0 ~ 2200.0 | us | RC channel 1 trim |
| `RC2_MAX` | float | 2000.0f | 1500.0 ~ 2200.0 | us | RC channel 2 maximum |
| `RC2_MIN` | float | 1000.0f | 800.0 ~ 1500.0 | us | RC channel 2 minimum |
| `RC2_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 2 reverse |
| `RC2_TRIM` | float | 1500.0f | 800.0 ~ 2200.0 | us | RC channel 2 trim |
| `RC3_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 3 maximum |
| `RC3_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 3 minimum |
| `RC3_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 3 reverse |
| `RC3_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 3 trim |
| `RC4_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 4 maximum |
| `RC4_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 4 minimum |
| `RC4_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 4 reverse |
| `RC4_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 4 trim |
| `RC5_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 5 maximum |
| `RC5_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 5 minimum |
| `RC5_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 5 reverse |
| `RC5_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 5 trim |
| `RC6_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 6 maximum |
| `RC6_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 6 minimum |
| `RC6_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 6 reverse |
| `RC6_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 6 trim |
| `RC7_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 7 maximum |
| `RC7_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 7 minimum |
| `RC7_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 7 reverse |
| `RC7_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 7 trim |
| `RC8_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 8 maximum |
| `RC8_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 8 minimum |
| `RC8_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 8 reverse |
| `RC8_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 8 trim |
| `RC9_MAX` | float | 2000 | 1500.0 ~ 2200.0 | us | RC channel 9 maximum |
| `RC9_MIN` | float | 1000 | 800.0 ~ 1500.0 | us | RC channel 9 minimum |
| `RC9_REV` | float | 1.0f | -1.0 ~ 1.0 |  | RC channel 9 reverse |
| `RC9_TRIM` | float | 1500 | 800.0 ~ 2200.0 | us | RC channel 9 trim |
| `RC_CHAN_CNT` | int32 | 0 | 0 ~ 18 |  | RC channel count |
| `RC_FAILS_THR` | int32 | 0 | 0 ~ 2200 | us | Failsafe channel PWM threshold. |
| `RC_MAP_AUX1` | int32 | 0 | 0 ~ 18 |  | AUX1 Passthrough RC channel |
| `RC_MAP_AUX2` | int32 | 0 | 0 ~ 18 |  | AUX2 Passthrough RC channel |
| `RC_MAP_AUX3` | int32 | 0 | 0 ~ 18 |  | AUX3 Passthrough RC channel |
| `RC_MAP_AUX4` | int32 | 0 | 0 ~ 18 |  | AUX4 Passthrough RC channel |
| `RC_MAP_AUX5` | int32 | 0 | 0 ~ 18 |  | AUX5 Passthrough RC channel |
| `RC_MAP_AUX6` | int32 | 0 | 0 ~ 18 |  | AUX6 Passthrough RC channel |
| `RC_MAP_ENG_MOT` | int32 | 0 | 0 ~ 18 |  | RC channel to engage the main motor (for helicopters) |
| `RC_MAP_FAILSAFE` | int32 | 0 | 0 ~ 18 |  | Failsafe channel mapping. |
| `RC_MAP_PARAM1` | int32 | 0 | 0 ~ 18 |  | PARAM1 tuning channel |
| `RC_MAP_PARAM2` | int32 | 0 | 0 ~ 18 |  | PARAM2 tuning channel |
| `RC_MAP_PARAM3` | int32 | 0 | 0 ~ 18 |  | PARAM3 tuning channel |
| `RC_MAP_PITCH` | int32 | 0 | 0 ~ 18 |  | Pitch control channel mapping. |
| `RC_MAP_ROLL` | int32 | 0 | 0 ~ 18 |  | Roll control channel mapping. |
| `RC_MAP_THROTTLE` | int32 | 0 | 0 ~ 18 |  | Throttle control channel mapping. |
| `RC_MAP_YAW` | int32 | 0 | 0 ~ 18 |  | Yaw control channel mapping. |
| `RC_RSSI_PWM_CHAN` | int32 | 0 | 0 ~ 18 |  | PWM input channel that provides RSSI. |
| `RC_RSSI_PWM_MAX` | int32 | 2000 | 0 ~ 2000 |  | Max input value for RSSI reading. |
| `RC_RSSI_PWM_MIN` | int32 | 1000 | 0 ~ 2000 |  | Min input value for RSSI reading. |
| `TRIM_PITCH` | float | 0.0f | -0.5 ~ 0.5 |  | Pitch trim |
| `TRIM_ROLL` | float | 0.0f | -0.5 ~ 0.5 |  | Roll trim |
| `TRIM_YAW` | float | 0.0f | -0.5 ~ 0.5 |  | Yaw trim |

## Commander

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `COM_ACT_FAIL_ACT` | int32 | 0 | 0 ~ 3 |  | Set the actuator failure failsafe mode |
| `COM_ARMABLE` | int32 | 1 |  |  | Flag to allow arming |
| `COM_ARM_AUTH_ID` | int32 | 10 |  |  | Arm authorizer system id |
| `COM_ARM_AUTH_MET` | int32 | 0 |  |  | Arm authorization method |
| `COM_ARM_AUTH_REQ` | int32 | 0 |  |  | Require arm authorization to arm |
| `COM_ARM_AUTH_TO` | float | 1 |  | s | Arm authorization timeout |
| `COM_ARM_BAT_MIN` | float | -1.f | -1 ~ 0.9 | norm | Minimum battery level for arming |
| `COM_ARM_CHK_ESCS` | int32 | 0 |  |  | Enable checks on ESCs that report telemetry. |
| `COM_ARM_HFLT_CHK` | int32 | 1 |  |  | Enable FMU SD card hardfault detection check |
| `COM_ARM_IMU_ACC` | float | 0.7f | 0.1 ~ 1.0 | m/s^2 | Maximum accelerometer inconsistency between IMU units that will allow arming |
| `COM_ARM_IMU_GYR` | float | 0.25f | 0.02 ~ 0.3 | rad/s | Maximum rate gyro inconsistency between IMU units that will allow arming |
| `COM_ARM_MAG_ANG` | int32 | 60 | 3 ~ 180 | deg | Maximum magnetic field inconsistency between units that will allow arming |
| `COM_ARM_MAG_STR` | int32 | 2 |  |  | Enable mag strength preflight check |
| `COM_ARM_MIS_REQ` | int32 | 0 |  |  | Require valid mission to arm |
| `COM_ARM_ODID` | int32 | 0 |  |  | Enable Drone ID system detection and health check |
| `COM_ARM_SDCARD` | int32 | 1 |  |  | Enable FMU SD card detection check |
| `COM_ARM_SWISBTN` | int32 | 0 |  |  | Arm switch is a momentary button |
| `COM_ARM_WO_GPS` | int32 | 1 |  |  | GPS preflight check |
| `COM_CPU_MAX` | float | 95.0f | -1 ~ 100 | % | Maximum allowed CPU load to still arm. |
| `COM_DISARM_LAND` | float | 2.0f |  | s | Time-out for auto disarm after landing |
| `COM_DISARM_MAN` | int32 | 1 |  |  | Allow disarming via switch/stick/button on multicopters in manual thrust modes |
| `COM_DISARM_PRFLT` | float | 10.0f |  | s | Time-out for auto disarm if not taking off |
| `COM_DLL_EXCEPT` | int32 | 0 | 0 ~ 7 |  | Datalink loss exceptions |
| `COM_DL_LOSS_T` | int32 | 10 | 5 ~ 300 | s | GCS connection loss time threshold |
| `COM_FAIL_ACT_T` | float | 5.f | 0.0 ~ 25.0 | s | Delay between failsafe condition triggered and failsafe reaction |
| `COM_FLIGHT_UUID` | int32 | 0 | 0 ~  |  | Next flight UUID |
| `COM_FLTMODE1` | enum | -1 |  |  | Mode slot ${i} |
| `COM_FLTMODE2` | enum | -1 |  |  | Mode slot ${i} |
| `COM_FLTMODE3` | enum | -1 |  |  | Mode slot ${i} |
| `COM_FLTMODE4` | enum | -1 |  |  | Mode slot ${i} |
| `COM_FLTMODE5` | enum | -1 |  |  | Mode slot ${i} |
| `COM_FLTMODE6` | enum | -1 |  |  | Mode slot ${i} |
| `COM_FLTT_LOW_ACT` | int32 | 0 |  |  | Remaining flight time low failsafe |
| `COM_FLT_PROFILE` | int32 | 0 |  |  | User Flight Profile |
| `COM_FLT_TIME_MAX` | int32 | -1 | -1 ~  | s | Maximum allowed flight time |
| `COM_FORCE_SAFETY` | int32 | 0 |  |  | Enable force safety |
| `COM_HLDL_LOSS_T` | int32 | 120 | 60 ~ 3600 | s | High Latency Datalink loss time threshold |
| `COM_HLDL_REG_T` | int32 | 0 | 0 ~ 60 | s | High Latency Datalink regain time threshold |
| `COM_HOME_EN` | int32 | 1 |  |  | Home position enabled |
| `COM_HOME_IN_AIR` | int32 | 0 |  |  | Allows setting the home position after takeoff |
| `COM_IMB_PROP_ACT` | int32 | 0 |  |  | Imbalanced propeller failsafe mode |
| `COM_KILL_DISARM` | float | 5.0f | 0.0 ~ 30.0 | s | Timeout value for disarming when kill switch is engaged |
| `COM_LKDOWN_TKO` | float | 3.0f | -1.0 ~ 5.0 | s | Timeout for detecting a failure after takeoff |
| `COM_LOW_BAT_ACT` | int32 | 0 |  |  | Battery failsafe mode |
| `COM_MODE0_HASH` | int32 | 0 |  |  | External mode identifier ${i} |
| `COM_MODE1_HASH` | int32 | 0 |  |  | External mode identifier ${i} |
| `COM_MODE2_HASH` | int32 | 0 |  |  | External mode identifier ${i} |
| `COM_MODE3_HASH` | int32 | 0 |  |  | External mode identifier ${i} |
| `COM_MODE4_HASH` | int32 | 0 |  |  | External mode identifier ${i} |
| `COM_MODE5_HASH` | int32 | 0 |  |  | External mode identifier ${i} |
| `COM_MODE6_HASH` | int32 | 0 |  |  | External mode identifier ${i} |
| `COM_MODE7_HASH` | int32 | 0 |  |  | External mode identifier ${i} |
| `COM_MODE_ARM_CHK` | int32 | 0 |  |  | Allow external mode registration while armed. |
| `COM_MOT_TEST_EN` | int32 | 1 |  |  | Enable Actuator Testing |
| `COM_OBC_LOSS_T` | float | 5.0f | 0 ~ 60 | s | Time-out to wait when onboard computer connection is lost before warning about loss connection. |
| `COM_OBL_RC_ACT` | int32 | 0 |  |  | Set offboard loss failsafe mode |
| `COM_OF_LOSS_T` | float | 1.0f | 0 ~ 60 | s | Time-out to wait when offboard connection is lost before triggering offboard lost action. |
| `COM_PARACHUTE` | int32 | 0 |  |  | Expect and require a healthy MAVLink parachute system |
| `COM_POS_FS_EPH` | float | 5.f | -1 ~ 400 | m | Horizontal position error threshold for hovering systems |
| `COM_POS_LOW_ACT` | int32 | 3 |  |  | Low position accuracy action |
| `COM_POS_LOW_EPH` | float | -1.0f | -1 ~ 1000 | m | Low position accuracy failsafe threshold |
| `COM_POWER_COUNT` | int32 | 1 | 0 ~ 4 |  | Required number of redundant power modules |
| `COM_PREARM_MODE` | int32 | 0 |  |  | Condition to enter prearmed mode |
| `COM_QC_ACT` | int32 | 0 |  |  | Set action after a quadchute |
| `COM_RAM_MAX` | float | 95.0f | -1 ~ 100 | % | Maximum allowed RAM usage to pass checks |
| `COM_RCL_EXCEPT` | int32 | 0 | 0 ~ 31 |  | Manual control loss exceptions |
| `COM_RC_ARM_HYST` | int32 | 1000 | 100 ~ 1500 | ms | Manual control input arm/disarm command duration |
| `COM_RC_IN_MODE` | int32 | 3 | 0 ~ 8 |  | Manual control input source configuration |
| `COM_RC_LOSS_T` | float | 0.5f | 0 ~ 35 | s | Manual control loss timeout |
| `COM_RC_OVERRIDE` | int32 | 1 | 0 ~ 3 |  | Enable manual control stick override |
| `COM_RC_STICK_OV` | float | 30.0f | 5 ~ 80 | % | Stick override threshold |
| `COM_SPOOLUP_TIME` | float | 1.0f | 0 ~ 30 | s | Enforced delay between arming and further navigation |
| `COM_TAKEOFF_ACT` | int32 | 0 |  |  | Action after TAKEOFF has been accepted. |
| `COM_THROW_EN` | int32 | 0 |  |  | Enable throw-start |
| `COM_THROW_SPEED` | float | 5 | 0 ~  | m/s | Minimum speed for the throw start |
| `COM_VEL_FS_EVH` | float | 1.f | 0 ~  | m/s | Horizontal velocity error threshold. |
| `COM_WIND_MAX` | float | -1.f | -1 ~  | m/s | High wind speed failsafe threshold |
| `COM_WIND_MAX_ACT` | int32 | 0 |  |  | High wind failsafe mode |
| `COM_WIND_WARN` | float | -1.f | -1 ~  | m/s | Wind speed warning threshold |
| `NAV_DLL_ACT` | int32 | 0 | 0 ~ 6 |  | Set GCS connection loss failsafe mode |
| `NAV_RCL_ACT` | int32 | 2 | 1 ~ 6 |  | Set manual control loss failsafe mode |

## Multicopter Position Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `CP_DELAY` | float | 0.4f | 0 ~ 1 | s | Average delay of the range sensor message plus the tracking delay of the position controller in seconds |
| `CP_DIST` | float | -1.0f | -1 ~ 15 | m | Minimum distance the vehicle should keep to all obstacles |
| `CP_GO_NO_DATA` | int32 | 0 |  |  | Boolean to allow moving into directions where there is no sensor data (outside FOV) |
| `CP_GUIDE_ANG` | float | 30.f | 0 ~ 90 | deg | Angle left/right from the commanded setpoint by which the collision prevention algorithm can choose to change the setpoint direction |
| `MC_MAN_TILT_TAU` | float | 0.0f | 0.0 ~ 2.0 | s | Manual tilt input filter time constant |
| `MPC_ACC_DECOUPLE` | int32 | 1 |  |  | Acceleration to tilt coupling |
| `MPC_ACC_DOWN_MAX` | float | 3.f | 2 ~ 15 | m/s^2 | Maximum downwards acceleration in climb rate controlled modes |
| `MPC_ACC_HOR` | float | 3.f | 2 ~ 15 | m/s^2 | Acceleration for autonomous and for manual modes |
| `MPC_ACC_HOR_MAX` | float | 5.f | 2 ~ 15 | m/s^2 | Maximum horizontal acceleration |
| `MPC_ACC_UP_MAX` | float | 4.f | 2 ~ 15 | m/s^2 | Maximum upwards acceleration in climb rate controlled modes |
| `MPC_ALT_MODE` | int32 | 2 | 0 ~ 2 |  | Altitude reference mode |
| `MPC_HOLD_MAX_XY` | float | 0.8f | 0 ~ 3 | m/s | Maximum horizontal velocity for which position hold is enabled (use 0 to disable check) |
| `MPC_HOLD_MAX_Z` | float | 0.6f | 0 ~ 3 | m/s | Maximum vertical velocity for which position hold is enabled (use 0 to disable check) |
| `MPC_JERK_AUTO` | float | 4.f | 1 ~ 80 | m/s^3 | Jerk limit in autonomous modes |
| `MPC_JERK_MAX` | float | 8.f | 0.5 ~ 500 | m/s^3 | Maximum horizontal and vertical jerk in Position/Altitude mode |
| `MPC_LAND_ALT1` | float | 10.f | 0 ~ 122 | m | Altitude for 1. step of slow landing (descend) |
| `MPC_LAND_ALT2` | float | 5.f | 0 ~ 122 | m | Altitude for 2. step of slow landing (landing) |
| `MPC_LAND_ALT3` | float | 1.f | 0 ~ 122 | m | Altitude for 3. step of slow landing |
| `MPC_LAND_CRWL` | float | 0.3f | 0.1 ~  | m/s | Land crawl descend rate |
| `MPC_LAND_RADIUS` | float | 1000.f | 0 ~  | m | User assisted landing radius |
| `MPC_LAND_RC_HELP` | int32 | 0 | 0 ~ 1 |  | Enable nudging based on user input during autonomous land routine |
| `MPC_LAND_SPEED` | float | 0.7f | 0.6 ~  | m/s | Landing descend rate |
| `MPC_MANTHR_MIN` | float | 0.08f | 0 ~ 1 | norm | Minimum collective thrust in Stabilized mode |
| `MPC_MAN_TILT_MAX` | float | 35.f | 1 ~ 70 | deg | Maximal tilt angle in Stabilized, Altitude and Altitude Cruise mode |
| `MPC_MAN_Y_MAX` | float | 150.f | 0 ~ 400 | deg/s | Max manual yaw rate for Stabilized, Altitude, Position mode |
| `MPC_MAN_Y_TAU` | float | 0.08f | 0 ~ 5 | s | Manual yaw rate input filter time constant |
| `MPC_POS_MODE` | int32 | 4 |  |  | Position/Altitude mode variant |
| `MPC_THR_CURVE` | int32 | 0 |  |  | Thrust curve mapping in Stabilized Mode |
| `MPC_THR_HOVER` | float | 0.5f | 0.1 ~ 0.8 | norm | Vertical thrust required to hover |
| `MPC_THR_MAX` | float | 1.f | 0 ~ 1 | norm | Maximum collective thrust in climb rate controlled modes |
| `MPC_THR_MIN` | float | 0.12f | 0.05 ~ 0.5 | norm | Minimum collective thrust in climb rate controlled modes |
| `MPC_THR_XY_MARG` | float | 0.3f | 0 ~ 0.5 | norm | Horizontal thrust margin |
| `MPC_TILTMAX_AIR` | float | 45.f | 20 ~ 89 | deg | Maximum tilt angle in air |
| `MPC_TILTMAX_LND` | float | 12.f | 5 ~ 89 | deg | Maximum tilt during inital takeoff ramp |
| `MPC_TKO_RAMP_T` | float | 3.f | 0 ~ 5 | s | Smooth takeoff ramp time constant |
| `MPC_TKO_SPEED` | float | 1.5f | 1 ~ 5 | m/s | Takeoff climb rate |
| `MPC_USE_HTE` | int32 | 1 |  |  | Use hover thrust estimate for altitude control |
| `MPC_VELD_LP` | float | 5.0f | 0 ~ 50 | Hz | Velocity derivative low pass cutoff frequency |
| `MPC_VEL_LP` | float | 0.0f | 0 ~ 50 | Hz | Velocity low pass cutoff frequency |
| `MPC_VEL_MANUAL` | float | 10.f | 3 ~ 20 | m/s | Maximum horizontal velocity setpoint in Position mode |
| `MPC_VEL_MAN_BACK` | float | -1.f | -1 ~ 20 | m/s | Maximum backward velocity in Position mode |
| `MPC_VEL_MAN_SIDE` | float | -1.f | -1 ~ 20 | m/s | Maximum sideways velocity in Position mode |
| `MPC_VEL_NF_BW` | float | 5.0f | 0 ~ 50 | Hz | Velocity notch filter bandwidth |
| `MPC_VEL_NF_FRQ` | float | 0.0f | 0 ~ 50 | Hz | Velocity notch filter frequency |
| `MPC_XY_CRUISE` | float | 5.f | 3 ~ 20 | m/s | Default horizontal velocity in autonomous modes |
| `MPC_XY_ERR_MAX` | float | 2.f | 0.1 ~ 10 |  | Maximum horizontal error allowed by the trajectory generator |
| `MPC_XY_P` | float | 0.95f | 0 ~ 2 |  | Proportional gain for horizontal position error |
| `MPC_XY_TRAJ_P` | float | 0.5f | 0.1 ~ 1 |  | Proportional gain for horizontal trajectory position error |
| `MPC_XY_VEL_ALL` | float | -10.f | -20 ~ 20 |  | Overall Horizontal Velocity Limit |
| `MPC_XY_VEL_D_ACC` | float | 0.2f | 0.1 ~ 2 |  | Differential gain for horizontal velocity error |
| `MPC_XY_VEL_I_ACC` | float | 0.4f | 0 ~ 60 |  | Integral gain for horizontal velocity error |
| `MPC_XY_VEL_MAX` | float | 12.f | 0 ~ 20 | m/s | Maximum horizontal velocity |
| `MPC_XY_VEL_P_ACC` | float | 1.8f | 1.2 ~ 5 |  | Proportional gain for horizontal velocity error |
| `MPC_Z_P` | float | 1.f | 0.1 ~ 1.5 |  | Proportional gain for vertical position error |
| `MPC_Z_VEL_ALL` | float | -3.f | -3 ~ 8 |  | Overall Vertical Velocity Limit |
| `MPC_Z_VEL_D_ACC` | float | 0.f | 0 ~ 2 |  | Differential gain for vertical velocity error |
| `MPC_Z_VEL_I_ACC` | float | 2.f | 0.2 ~ 3 |  | Integral gain for vertical velocity error |
| `MPC_Z_VEL_MAX_DN` | float | 1.5f | 0.5 ~ 4 | m/s | Maximum descent velocity |
| `MPC_Z_VEL_MAX_UP` | float | 3.f | 0.5 ~ 8 | m/s | Maximum ascent velocity |
| `MPC_Z_VEL_P_ACC` | float | 4.f | 2 ~ 15 |  | Proportional gain for vertical velocity error |
| `MPC_Z_V_AUTO_DN` | float | 1.5f | 0.5 ~ 4 | m/s | Descent velocity in autonomous modes |
| `MPC_Z_V_AUTO_UP` | float | 3.f | 0.5 ~ 8 | m/s | Ascent velocity in autonomous modes |
| `SC_MAN_TILT_MAX` | float | 90.f | 0 ~ 90 | deg | Maximal tilt angle in Stabilized or Manual mode |
| `SYS_VEHICLE_RESP` | float | -0.4f | -1 ~ 1 |  | Responsiveness |
| `WV_EN` | int32 | 0 |  |  | Enable weathervane. |
| `WV_ROLL_MIN` | float | 1.0f | 0 ~ 5 | deg | Minimum roll angle setpoint for weathervane controller to demand a yaw-rate. |
| `WV_YRATE_MAX` | float | 90.0f | 0 ~ 120 | deg/s | Maximum yawrate the weathervane controller is allowed to demand. |

## Local Position Estimator

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `LPE_ACC_XY` | float | 0.012f | 0.00001 ~ 2 | m/s^2/sqrt(Hz) | Accelerometer xy noise density |
| `LPE_ACC_Z` | float | 0.02f | 0.00001 ~ 2 | m/s^2/sqrt(Hz) | Accelerometer z noise density |
| `LPE_BAR_Z` | float | 3.0f | 0.01 ~ 100 | m | Barometric presssure altitude z standard deviation. |
| `LPE_EN` | int32 | 0 |  |  | Local position estimator enable (unsupported) |
| `LPE_EPH_MAX` | float | 3.0f | 1.0 ~ 5.0 | m | Max EPH allowed for GPS initialization |
| `LPE_EPV_MAX` | float | 5.0f | 1.0 ~ 5.0 | m | Max EPV allowed for GPS initialization |
| `LPE_FAKE_ORIGIN` | int32 | 0 | 0 ~ 1 |  | Enable publishing of a fake global position (e.g for AUTO missions using Optical Flow) |
| `LPE_FGYRO_HP` | float | 0.001f | 0 ~ 2 | Hz | Flow gyro high pass filter cut off frequency |
| `LPE_FLW_OFF_Z` | float | 0.0f | -1 ~ 1 | m | Optical flow z offset from center |
| `LPE_FLW_QMIN` | int32 | 150 | 0 ~ 255 |  | Optical flow minimum quality threshold |
| `LPE_FLW_R` | float | 7.0f | 0.1 ~ 10.0 | m/s/rad | Optical flow rotation (roll/pitch) noise gain |
| `LPE_FLW_RR` | float | 7.0f | 0.0 ~ 10.0 | m/rad | Optical flow angular velocity noise gain |
| `LPE_FLW_SCALE` | float | 1.3f | 0.1 ~ 10.0 | m | Optical flow scale |
| `LPE_FUSION` | int32 | 145 | 0 ~ 255 |  | Integer bitmask controlling data fusion |
| `LPE_GPS_DELAY` | float | 0.29f | 0 ~ 0.4 | s | GPS delay compensaton |
| `LPE_GPS_VXY` | float | 0.25f | 0.01 ~ 2 | m/s | GPS xy velocity standard deviation. |
| `LPE_GPS_VZ` | float | 0.25f | 0.01 ~ 2 | m/s | GPS z velocity standard deviation. |
| `LPE_GPS_XY` | float | 1.0f | 0.01 ~ 5 | m | Minimum GPS xy standard deviation, uses reported EPH if greater. |
| `LPE_GPS_Z` | float | 3.0f | 0.01 ~ 200 | m | Minimum GPS z standard deviation, uses reported EPV if greater. |
| `LPE_LAND_VXY` | float | 0.05f | 0.01 ~ 10.0 | m/s | Land detector xy velocity standard deviation |
| `LPE_LAND_Z` | float | 0.03f | 0.001 ~ 10.0 | m | Land detector z standard deviation |
| `LPE_LAT` | float | 47.397742f | -90 ~ 90 | deg | Local origin latitude for nav w/o GPS |
| `LPE_LDR_OFF_Z` | float | 0.00f | -1 ~ 1 | m | Lidar z offset from center of vehicle +down |
| `LPE_LDR_Z` | float | 0.03f | 0.01 ~ 1 | m | Lidar z standard deviation. |
| `LPE_LON` | float | 8.545594 | -180 ~ 180 | deg | Local origin longitude for nav w/o GPS |
| `LPE_LT_COV` | float | 0.0001f | 0.0 ~ 10 | m^2 | Minimum landing target standard covariance, uses reported covariance if greater. |
| `LPE_PN_B` | float | 1e-3f | 0 ~ 1 | m/s^3/sqrt(Hz) | Accel bias propagation noise density |
| `LPE_PN_P` | float | 0.1f | 0 ~ 1 | m/s/sqrt(Hz) | Position propagation noise density |
| `LPE_PN_T` | float | 0.001f | 0 ~ 1 | m/s/sqrt(Hz) | Terrain random walk noise density, hilly/outdoor (0.1), flat/Indoor (0.001) |
| `LPE_PN_V` | float | 0.1f | 0 ~ 1 | m/s^2/sqrt(Hz) | Velocity propagation noise density |
| `LPE_SNR_OFF_Z` | float | 0.00f | -1 ~ 1 | m | Sonar z offset from center of vehicle +down |
| `LPE_SNR_Z` | float | 0.05f | 0.01 ~ 1 | m | Sonar z standard deviation. |
| `LPE_T_MAX_GRADE` | float | 1.0f | 0 ~ 100 | % | Terrain maximum percent grade, hilly/outdoor (100 = 45 deg), flat/Indoor (0 = 0 deg) |
| `LPE_VIC_P` | float | 0.001f | 0.0001 ~ 1 | m | Vicon position standard deviation. |
| `LPE_VIS_DELAY` | float | 0.1f | 0 ~ 0.1 | s | Vision delay compensation. |
| `LPE_VIS_XY` | float | 0.1f | 0.01 ~ 1 | m | Vision xy standard deviation. |
| `LPE_VIS_Z` | float | 0.5f | 0.01 ~ 100 | m | Vision z standard deviation. |
| `LPE_VXY_PUB` | float | 0.3f | 0.01 ~ 1.0 | m/s | Required velocity xy standard deviation to publish position |
| `LPE_X_LP` | float | 5.0f | 5 ~ 1000 | Hz | Cut frequency for state publication |
| `LPE_Z_PUB` | float | 1.0f | 0.3 ~ 5.0 | m | Required z standard deviation to publish altitude/ terrain |

## MAVLink

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MAV_0_BROADCAST` | enum | 1, 0, 0 |  |  | Broadcast heartbeats on local network for MAVLink instance ${i} |
| `MAV_0_FLOW_CTRL` | enum | 2, 2, 2 |  |  | Enable serial flow control for instance ${i} |
| `MAV_0_FORWARD` | boolean | True, False, False |  |  | Enable MAVLink Message forwarding for instance ${i} |
| `MAV_0_HL_FREQ` | float | 0.015, 0.015, 0.015 | 0.0 ~ 50.0 | Hz | Configures the frequency of HIGH_LATENCY2 stream for instance ${i} |
| `MAV_0_MODE` | enum | 0, 2, 0 |  |  | MAVLink Mode for instance ${i} |
| `MAV_0_RADIO_CTL` | boolean | True, True, True |  |  | Enable software throttling of mavlink on instance ${i} |
| `MAV_0_RATE` | int32 | 1200, 0, 0 | 0 ~  | B/s | Maximum MAVLink sending rate for instance ${i} |
| `MAV_0_REMOTE_PRT` | int32 | 14550, 0, 0 |  |  | MAVLink Remote Port for instance ${i} |
| `MAV_0_UDP_PRT` | int32 | 14556, 0, 0 |  |  | MAVLink Network Port for instance ${i} |
| `MAV_1_BROADCAST` | enum | 1, 0, 0 |  |  | Broadcast heartbeats on local network for MAVLink instance ${i} |
| `MAV_1_FLOW_CTRL` | enum | 2, 2, 2 |  |  | Enable serial flow control for instance ${i} |
| `MAV_1_FORWARD` | boolean | True, False, False |  |  | Enable MAVLink Message forwarding for instance ${i} |
| `MAV_1_HL_FREQ` | float | 0.015, 0.015, 0.015 | 0.0 ~ 50.0 | Hz | Configures the frequency of HIGH_LATENCY2 stream for instance ${i} |
| `MAV_1_MODE` | enum | 0, 2, 0 |  |  | MAVLink Mode for instance ${i} |
| `MAV_1_RADIO_CTL` | boolean | True, True, True |  |  | Enable software throttling of mavlink on instance ${i} |
| `MAV_1_RATE` | int32 | 1200, 0, 0 | 0 ~  | B/s | Maximum MAVLink sending rate for instance ${i} |
| `MAV_1_REMOTE_PRT` | int32 | 14550, 0, 0 |  |  | MAVLink Remote Port for instance ${i} |
| `MAV_1_UDP_PRT` | int32 | 14556, 0, 0 |  |  | MAVLink Network Port for instance ${i} |
| `MAV_2_BROADCAST` | enum | 1, 0, 0 |  |  | Broadcast heartbeats on local network for MAVLink instance ${i} |
| `MAV_2_FLOW_CTRL` | enum | 2, 2, 2 |  |  | Enable serial flow control for instance ${i} |
| `MAV_2_FORWARD` | boolean | True, False, False |  |  | Enable MAVLink Message forwarding for instance ${i} |
| `MAV_2_HL_FREQ` | float | 0.015, 0.015, 0.015 | 0.0 ~ 50.0 | Hz | Configures the frequency of HIGH_LATENCY2 stream for instance ${i} |
| `MAV_2_MODE` | enum | 0, 2, 0 |  |  | MAVLink Mode for instance ${i} |
| `MAV_2_RADIO_CTL` | boolean | True, True, True |  |  | Enable software throttling of mavlink on instance ${i} |
| `MAV_2_RATE` | int32 | 1200, 0, 0 | 0 ~  | B/s | Maximum MAVLink sending rate for instance ${i} |
| `MAV_2_REMOTE_PRT` | int32 | 14550, 0, 0 |  |  | MAVLink Remote Port for instance ${i} |
| `MAV_2_UDP_PRT` | int32 | 14556, 0, 0 |  |  | MAVLink Network Port for instance ${i} |
| `MAV_COMP_ID` | int32 | 1 | 1 ~ 250 |  | MAVLink component ID |
| `MAV_FWDEXTSP` | int32 | 1 |  |  | Forward external setpoint messages |
| `MAV_HASH_CHK_EN` | int32 | 1 |  |  | Parameter hash check. |
| `MAV_HB_FORW_EN` | int32 | 1 |  |  | Heartbeat message forwarding. |
| `MAV_PROTO_VER` | int32 | 2 |  |  | MAVLink protocol version |
| `MAV_RADIO_TOUT` | int32 | 5 | 1 ~ 250 | s | Timeout in seconds for the RADIO_STATUS reports coming in |
| `MAV_SIK_RADIO_ID` | int32 | 0 | -1 ~ 240 |  | MAVLink SiK Radio ID |
| `MAV_SYS_ID` | int32 | 1 | 1 ~ 250 |  | MAVLink system ID |
| `MAV_S_FORWARD` | boolean | False |  |  | Enable MAVLink forwarding on TELEM2 |
| `MAV_S_MODE` | enum | 11 |  |  | MAVLink Mode for SOM to FMU communication channel |
| `MAV_TYPE` | int32 | 0 | 0 ~ 22 |  | MAVLink airframe type |
| `MAV_USEHILGPS` | int32 | 0 |  |  | Use/Accept HIL GPS message even if not in HIL mode |

## UAVCAN

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `CANNODE_BITRATE` | int32 | 1000000 | 20000 ~ 1000000 |  | UAVCAN CAN bus bitrate. |
| `CANNODE_PUB_IMU` | int32 | 0 |  ~ 1 |  | Enable RawIMU pub |
| `CANNODE_PUB_MBD` | int32 | 0 |  |  | Enable MovingBaselineData publication |
| `CANNODE_SUB_MBD` | int32 | 0 |  ~ 1 |  | Enable MovingBaselineData subscription |
| `CANNODE_SUB_RTCM` | int32 | 0 |  |  | Enable RTCM subscription |
| `CANNODE_TERM` | int32 | 0 |  ~ 1 |  | CAN built-in bus termination |
| `SIM_GZ_EN` | int32 | 0 |  |  | Simulator Gazebo bridge enable |
| `UAVCAN_BITRATE` | int32 | 1000000 | 20000 ~ 1000000 | bit/s | UAVCAN CAN bus bitrate. |
| `UAVCAN_ECU_FUELT` | int32 | 1 | 0 ~ 2 |  | UAVCAN fuel tank fuel type |
| `UAVCAN_ECU_MAXF` | float | 15.0f | 0.0 ~ 100000.0 | liters | UAVCAN fuel tank maximum capacity |
| `UAVCAN_ENABLE` | int32 | 0 | 0 ~ 3 |  | UAVCAN mode |
| `UAVCAN_ESC_IFACE` | bitmask | 255 | 1 ~ 255 |  | Which CAN interfaces to output ESC messages on. |
| `UAVCAN_LGT_ANTCL` | int32 | 2 | 0 ~ 3 |  | UAVCAN ANTI_COLLISION light operating mode |
| `UAVCAN_LGT_LAND` | int32 | 0 | 0 ~ 3 |  | UAVCAN LIGHT_ID_LANDING light operating mode |
| `UAVCAN_LGT_NAV` | int32 | 3 | 0 ~ 3 |  | UAVCAN RIGHT_OF_WAY light operating mode |
| `UAVCAN_LGT_STROB` | int32 | 1 | 0 ~ 3 |  | UAVCAN STROBE light operating mode |
| `UAVCAN_NODE_ID` | int32 | 1 | 1 ~ 125 |  | UAVCAN Node ID. |
| `UAVCAN_PUB_ARM` | int32 | 0 |  |  | publish Arming Status stream |
| `UAVCAN_PUB_MBD` | int32 | 0 |  |  | publish moving baseline data RTCM stream |
| `UAVCAN_PUB_RTCM` | int32 | 0 |  |  | publish RTCM stream |
| `UAVCAN_RNG_MAX` | float | 999.0f |  | m | UAVCAN rangefinder maximum range |
| `UAVCAN_RNG_MIN` | float | 0.0f |  | m | UAVCAN rangefinder minimum range |
| `UAVCAN_SUB_ASPD` | int32 | 0 |  |  | subscription airspeed |
| `UAVCAN_SUB_BARO` | int32 | 0 |  |  | subscription barometer |
| `UAVCAN_SUB_BAT` | int32 | 0 | 0 ~ 2 |  | subscription battery |
| `UAVCAN_SUB_BTN` | int32 | 0 |  |  | subscription button |
| `UAVCAN_SUB_DPRES` | int32 | 0 |  |  | subscription differential pressure |
| `UAVCAN_SUB_FLOW` | int32 | 0 |  |  | subscription flow |
| `UAVCAN_SUB_FUEL` | int32 | 0 |  |  | subscription fuel tank |
| `UAVCAN_SUB_GPS` | int32 | 1 |  |  | subscription GPS |
| `UAVCAN_SUB_GPS_R` | int32 | 1 |  |  | subscription GPS Relative |
| `UAVCAN_SUB_HYGRO` | int32 | 0 |  |  | subscription hygrometer |
| `UAVCAN_SUB_ICE` | int32 | 0 |  |  | subscription ICE |
| `UAVCAN_SUB_IMU` | int32 | 0 |  |  | subscription IMU |
| `UAVCAN_SUB_MAG` | int32 | 1 |  |  | subscription magnetometer |
| `UAVCAN_SUB_RNG` | int32 | 0 |  |  | subscription range finder |

## VTOL Attitude Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `VT_ARSP_BLEND` | float | 8.0f | 0.00 ~ 30.00 | m/s | Transition blending airspeed |
| `VT_ARSP_TRANS` | float | 10.0f | 0.00 ~ 30.00 | m/s | Transition airspeed |
| `VT_BT_TILT_DUR` | float | 1.f | 0.1 ~ 10 | s | Duration motor tilt up in backtransition |
| `VT_B_DEC_I` | float | 0.1f | 0 ~ 0.3 | rad s/m | Backtransition deceleration setpoint to pitch I gain. |
| `VT_B_DEC_MSS` | float | 2.0f | 0.5 ~ 10 | m/s^2 | Approximate deceleration during back transition |
| `VT_B_TRANS_DUR` | float | 10.0f | 0.1 ~ 20.00 | s | Maximum duration of a back transition |
| `VT_B_TRANS_RAMP` | float | 3.0f | 0.0 ~ 20.0 | s | Back transition MC motor ramp up time |
| `VT_ELEV_MC_LOCK` | int32 | 1 |  |  | Lock control surfaces in hover |
| `VT_FWD_THRUST_EN` | int32 | 0 |  |  | Use fixed-wing actuation in hover to accelerate forward |
| `VT_FWD_THRUST_SC` | float | 0.7f | 0.0 ~ 5.0 |  | Fixed-wing actuation thrust scale in hover |
| `VT_FW_DIFTHR_EN` | int32 | 0 | 0 ~ 7 |  | Differential thrust in forwards flight. |
| `VT_FW_DIFTHR_S_P` | float | 1.f | 0.0 ~ 2.0 |  | Pitch differential thrust factor in forward flight |
| `VT_FW_DIFTHR_S_R` | float | 1.f | 0.0 ~ 2.0 |  | Roll differential thrust factor in forward flight |
| `VT_FW_DIFTHR_S_Y` | float | 0.1f | 0.0 ~ 2.0 |  | Yaw differential thrust factor in forward flight |
| `VT_FW_MIN_ALT` | float | 0.0f | 0.0 ~ 200.0 | m | Quad-chute altitude |
| `VT_FW_QC_HMAX` | int32 | 0 | 0 ~  | m | Quad-chute maximum height |
| `VT_FW_QC_P` | int32 | 0 | 0 ~ 180 | deg | Quad-chute max pitch threshold |
| `VT_FW_QC_R` | int32 | 0 | 0 ~ 180 | deg | Quad-chute max roll threshold |
| `VT_F_TRANS_DUR` | float | 5.0f | 0.1 ~ 20.00 | s | Duration of a front transition |
| `VT_F_TRANS_THR` | float | 1.0f | 0.0 ~ 1.0 |  | Target throttle value for the transition to fixed-wing flight. |
| `VT_F_TR_OL_TM` | float | 6.0f | 1.0 ~ 30.0 | s | Airspeed-less front transition time (open loop) |
| `VT_LND_PITCH_MIN` | float | -5.0f | -10.0 ~ 45.0 | deg | Minimum pitch angle during hover landing. |
| `VT_PITCH_MIN` | float | -5.0f | -10.0 ~ 45.0 | deg | Minimum pitch angle during hover. |
| `VT_PSHER_SLEW` | float | 0.33f | 0 ~  | 1/s | Pusher throttle ramp up slew rate |
| `VT_QC_ALT_LOSS` | float | 0.0f | 0.0 ~ 200.0 | m | Quad-chute uncommanded descent threshold |
| `VT_QC_T_ALT_LOSS` | float | 20.0f | 0 ~ 50 | m | Quad-chute transition altitude loss threshold |
| `VT_SPOILER_MC_LD` | float | 0.f | -1 ~ 1 | norm | Spoiler setting while landing (hover) |
| `VT_TILT_FW` | float | 1.0f | 0.0 ~ 1.0 |  | Normalized tilt in FW |
| `VT_TILT_MC` | float | 0.0f | 0.0 ~ 1.0 |  | Normalized tilt in Hover |
| `VT_TILT_TRANS` | float | 0.4f | 0.0 ~ 1.0 |  | Normalized tilt in transition to FW |
| `VT_TRANS_MIN_TM` | float | 2.0f | 0.0 ~ 20.0 | s | Front transition minimum time |
| `VT_TRANS_P2_DUR` | float | 0.5f | 0.1 ~ 5.0 | s | Duration of front transition phase 2 |
| `VT_TRANS_TIMEOUT` | float | 15.0f | 0.1 ~ 30.00 | s | Front transition timeout |
| `VT_TYPE` | int32 | 0 | 0 ~ 2 |  | VTOL Type (Tailsitter=0, Tiltrotor=1, Standard=2) |
| `WV_GAIN` | float | 1.0f | 0.0 ~ 3.0 | Hz | Weather-vane roll angle to yawrate. |

## Battery Calibration

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `BAT1_A_PER_V` | float | -1.0, -1.0 |  |  | Battery ${i} current per volt (A/V) |
| `BAT1_CAPACITY` | float | -1.0, -1.0, -1.0 | -1.0 ~ 100000 | mAh | Battery ${i} capacity. |
| `BAT1_I_CHANNEL` | int32 | -1, -1 |  |  | Battery ${i} Current ADC Channel |
| `BAT1_I_OVERWRITE` | float | 0, 0 |  |  | Battery ${i} idle current overwrite |
| `BAT1_N_CELLS` | enum | 0, 0, 0 |  |  | Number of cells for battery ${i}. |
| `BAT1_R_INTERNAL` | float | -1.0, -1.0, -1.0 | -1.0 ~ 0.2 | Ohm | Explicitly defines the per cell internal resistance for battery ${i} |
| `BAT1_SOURCE` | enum | 0, -1, -1 |  |  | Battery ${i} monitoring source. |
| `BAT1_V_CHANNEL` | int32 | -1, -1 |  |  | Battery ${i} Voltage ADC Channel |
| `BAT1_V_CHARGED` | float | 4.05, 4.05, 4.05 |  | V | Full cell voltage |
| `BAT1_V_DIV` | float | -1.0, -1.0 |  |  | Battery ${i} voltage divider (V divider) |
| `BAT1_V_EMPTY` | float | 3.6, 3.6, 3.6 |  | V | Empty cell voltage |
| `BAT2_A_PER_V` | float | -1.0, -1.0 |  |  | Battery ${i} current per volt (A/V) |
| `BAT2_CAPACITY` | float | -1.0, -1.0, -1.0 | -1.0 ~ 100000 | mAh | Battery ${i} capacity. |
| `BAT2_I_CHANNEL` | int32 | -1, -1 |  |  | Battery ${i} Current ADC Channel |
| `BAT2_I_OVERWRITE` | float | 0, 0 |  |  | Battery ${i} idle current overwrite |
| `BAT2_N_CELLS` | enum | 0, 0, 0 |  |  | Number of cells for battery ${i}. |
| `BAT2_R_INTERNAL` | float | -1.0, -1.0, -1.0 | -1.0 ~ 0.2 | Ohm | Explicitly defines the per cell internal resistance for battery ${i} |
| `BAT2_SOURCE` | enum | 0, -1, -1 |  |  | Battery ${i} monitoring source. |
| `BAT2_V_CHANNEL` | int32 | -1, -1 |  |  | Battery ${i} Voltage ADC Channel |
| `BAT2_V_CHARGED` | float | 4.05, 4.05, 4.05 |  | V | Full cell voltage |
| `BAT2_V_DIV` | float | -1.0, -1.0 |  |  | Battery ${i} voltage divider (V divider) |
| `BAT2_V_EMPTY` | float | 3.6, 3.6, 3.6 |  | V | Empty cell voltage |
| `BAT3_CAPACITY` | float | -1.0, -1.0, -1.0 | -1.0 ~ 100000 | mAh | Battery ${i} capacity. |
| `BAT3_N_CELLS` | enum | 0, 0, 0 |  |  | Number of cells for battery ${i}. |
| `BAT3_R_INTERNAL` | float | -1.0, -1.0, -1.0 | -1.0 ~ 0.2 | Ohm | Explicitly defines the per cell internal resistance for battery ${i} |
| `BAT3_SOURCE` | enum | 0, -1, -1 |  |  | Battery ${i} monitoring source. |
| `BAT3_V_CHARGED` | float | 4.05, 4.05, 4.05 |  | V | Full cell voltage |
| `BAT3_V_EMPTY` | float | 3.6, 3.6, 3.6 |  | V | Empty cell voltage |
| `BAT_ADC_CHANNEL` | int32 | -1 |  |  | This parameter is deprecated. Please use BAT1_I_CHANNEL. |
| `BAT_AVRG_CURRENT` | float | 15 | 0 ~ 500 | A | Expected battery current in flight. |
| `BAT_CRIT_THR` | float | 0.07 | 0.05 ~ 0.5 | norm | Critical threshold. |
| `BAT_EMERGEN_THR` | float | 0.05 | 0.03 ~ 0.5 | norm | Emergency threshold. |
| `BAT_LOW_THR` | float | 0.15 | 0.12 ~ 0.5 | norm | Low threshold. |
| `BAT_V_OFFS_CURR` | float | 0.0 |  |  | Offset in volt as seen by the ADC input of the current sensor. |

## FW Rate Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `FW_ACRO_X_MAX` | float | 90 | 10 ~ 720 | deg | Acro body roll max rate setpoint |
| `FW_ACRO_YAW_EN` | int32 | 0 |  |  | Enable yaw rate controller in Acro |
| `FW_ACRO_Y_MAX` | float | 90 | 10 ~ 720 | deg | Acro body pitch max rate setpoint |
| `FW_ACRO_Z_MAX` | float | 45 | 10 ~ 720 | deg | Acro body yaw max rate setpoint |
| `FW_ARSP_SCALE_EN` | int32 | 1 |  |  | Enable airspeed scaling |
| `FW_BAT_SCALE_EN` | int32 | 0 |  |  | Enable throttle scale by battery level |
| `FW_DTRIM_P_VMAX` | float | 0.0f | -0.5 ~ 0.5 |  | Pitch trim increment at maximum airspeed |
| `FW_DTRIM_P_VMIN` | float | 0.0f | -0.5 ~ 0.5 |  | Pitch trim increment at minimum airspeed |
| `FW_DTRIM_R_VMAX` | float | 0.0f | -0.5 ~ 0.5 |  | Roll trim increment at maximum airspeed |
| `FW_DTRIM_R_VMIN` | float | 0.0f | -0.5 ~ 0.5 |  | Roll trim increment at minimum airspeed |
| `FW_DTRIM_Y_VMAX` | float | 0.0f | -0.5 ~ 0.5 |  | Yaw trim increment at maximum airspeed |
| `FW_DTRIM_Y_VMIN` | float | 0.0f | -0.5 ~ 0.5 |  | Yaw trim increment at minimum airspeed |
| `FW_MAN_P_SC` | float | 1.0f | 0.0 ~  | norm | Manual pitch scale |
| `FW_MAN_R_SC` | float | 1.0f | 0.0 ~ 1.0 | norm | Manual roll scale |
| `FW_MAN_Y_SC` | float | 1.0f | 0.0 ~  | norm | Manual yaw scale |
| `FW_PR_D` | float | 0.f | 0.0 ~ 10 | %/rad/s | Pitch rate derivative gain. |
| `FW_PR_FF` | float | 0.5f | 0.0 ~ 10.0 | %/rad/s | Pitch rate feed forward |
| `FW_PR_I` | float | 0.1f | 0.0 ~ 10 | %/rad | Pitch rate integrator gain. |
| `FW_PR_IMAX` | float | 0.4f | 0.0 ~ 1.0 |  | Pitch rate integrator limit |
| `FW_PR_P` | float | 0.08f | 0.0 ~ 10 | %/rad/s | Pitch rate proportional gain. |
| `FW_RLL_TO_YAW_FF` | float | 0.0f | 0.0 ~  |  | Roll control to yaw control feedforward gain. |
| `FW_RR_D` | float | 0.0f | 0.0 ~ 10 | %/rad/s | Roll rate derivative gain |
| `FW_RR_FF` | float | 0.5f | 0.0 ~ 10.0 | %/rad/s | Roll rate feed forward |
| `FW_RR_I` | float | 0.1f | 0.0 ~ 10 | %/rad | Roll rate integrator gain |
| `FW_RR_IMAX` | float | 0.2f | 0.0 ~ 1.0 |  | Roll integrator limit |
| `FW_RR_P` | float | 0.05f | 0.0 ~ 10 | %/rad/s | Roll rate proportional gain |
| `FW_SPOILERS_MAN` | int32 | 0 |  |  | Spoiler input in manual flight |
| `FW_USE_AIRSPD` | int32 | 1 |  |  | Use airspeed for control |
| `FW_YR_D` | float | 0.0f | 0.0 ~ 10 | %/rad/s | Yaw rate derivative gain |
| `FW_YR_FF` | float | 0.3f | 0.0 ~ 10.0 | %/rad/s | Yaw rate feed forward |
| `FW_YR_I` | float | 0.1f | 0.0 ~ 10 | %/rad | Yaw rate integrator gain |
| `FW_YR_IMAX` | float | 0.2f | 0.0 ~ 1.0 |  | Yaw rate integrator limit |
| `FW_YR_P` | float | 0.05f | 0.0 ~ 10 | %/rad/s | Yaw rate proportional gain |

## Spacecraft Rate Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SC_ACRO_EXPO` | float | 0.69f | 0 ~ 1 |  | Acro mode Expo factor for Roll and Pitch. |
| `SC_ACRO_EXPO_Y` | float | 0.69f | 0 ~ 1 |  | Acro mode Expo factor for Yaw. |
| `SC_ACRO_P_MAX` | float | 720.0f | 0.0 ~ 1800.0 | deg/s | Max acro pitch rate |
| `SC_ACRO_R_MAX` | float | 720.0f | 0.0 ~ 1800.0 | deg/s | Max acro roll rate |
| `SC_ACRO_SUPEXPO` | float | 0.7f | 0 ~ 0.95 |  | Acro mode SuperExpo factor for Roll and Pitch. |
| `SC_ACRO_SUPEXPOY` | float | 0.7f | 0 ~ 0.95 |  | Acro mode SuperExpo factor for Yaw. |
| `SC_ACRO_Y_MAX` | float | 540.0f | 0.0 ~ 1800.0 | deg/s | Max acro yaw rate |
| `SC_BAT_SCALE_EN` | int32 | 0 |  |  | Battery power level scaler |
| `SC_MAN_F_MAX` | float | 1.0f | 0 ~ 1.0 |  | Manual mode maximum force. |
| `SC_MAN_T_MAX` | float | 1.0f | 0 ~ 1.0 |  | Manual mode maximum torque. |
| `SC_PITCHRATE_D` | float | 0.003f | 0.0 ~  |  | Pitch rate D gain |
| `SC_PITCHRATE_FF` | float | 0.0f | 0.0 ~  |  | Pitch rate feedforward |
| `SC_PITCHRATE_I` | float | 0.2f | 0.0 ~  |  | Pitch rate I gain |
| `SC_PITCHRATE_K` | float | 1.0f | 0.01 ~ 5.0 |  | Pitch rate controller gain |
| `SC_PITCHRATE_P` | float | 0.15f | 0.01 ~ 0.6 |  | Pitch rate P gain |
| `SC_PR_INT_LIM` | float | 0.30f | 0.0 ~  |  | Pitch rate integrator limit |
| `SC_ROLLRATE_D` | float | 0.003f | 0.0 ~ 0.01 |  | Roll rate D gain |
| `SC_ROLLRATE_FF` | float | 0.0f | 0.0 ~  |  | Roll rate feedforward |
| `SC_ROLLRATE_I` | float | 0.2f | 0.0 ~  |  | Roll rate I gain |
| `SC_ROLLRATE_K` | float | 1.0f | 0.01 ~ 5.0 |  | Roll rate controller gain |
| `SC_ROLLRATE_P` | float | 0.15f | 0.01 ~ 0.5 |  | Roll rate P gain |
| `SC_RR_INT_LIM` | float | 0.30f | 0.0 ~  |  | Roll rate integrator limit |
| `SC_YAWRATE_D` | float | 0.0f | 0.0 ~  |  | Yaw rate D gain |
| `SC_YAWRATE_FF` | float | 0.0f | 0.0 ~  |  | Yaw rate feedforward |
| `SC_YAWRATE_I` | float | 0.865f | 0.0 ~  |  | Yaw rate I gain |
| `SC_YAWRATE_K` | float | 1.0f | 0.0 ~ 5.0 |  | Yaw rate controller gain |
| `SC_YAWRATE_P` | float | 10.0f | 0.0 ~ 10.0 |  | Yaw rate P gain |
| `SC_YR_INT_LIM` | float | 0.2f | 0.0 ~  |  | Yaw rate integrator limit |

## Cyphal

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `CYPHAL_BAUD` | int32 | 1000000 | 20000 ~ 1000000 | bit/s | UAVCAN/CAN v1 bus bitrate. |
| `CYPHAL_ENABLE` | int32 | 1 |  |  | Cyphal |
| `CYPHAL_ID` | int32 | 1 | -1 ~ 125 |  | Cyphal Node ID. |
| `UCAN1_ACTR_PUB` | int32 | -1 | -1 ~ 6143 |  | actuator_outputs uORB over Cyphal publication port ID. |
| `UCAN1_BMS_BP_SUB` | int32 | -1 | -1 ~ 6143 |  | UDRAL battery parameters subscription  port ID. |
| `UCAN1_BMS_BS_SUB` | int32 | -1 | -1 ~ 6143 |  | UDRAL battery status subscription port ID. |
| `UCAN1_BMS_ES_SUB` | int32 | -1 | -1 ~ 6143 |  | UDRAL battery energy source subscription port ID. |
| `UCAN1_ESC0_SUB` | int32 | -1 | -1 ~ 6143 |  | ESC 0 subscription port ID. |
| `UCAN1_ESC_PUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal ESC publication port ID. |
| `UCAN1_FB0_SUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal ESC 0 zubax feedback port ID. |
| `UCAN1_FB1_SUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal ESC 1 zubax feedback port ID. |
| `UCAN1_FB2_SUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal ESC 2 zubax feedback port ID. |
| `UCAN1_FB3_SUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal ESC 3 zubax feedback port ID. |
| `UCAN1_FB4_SUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal ESC 4 zubax feedback port ID. |
| `UCAN1_FB5_SUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal ESC 5 zubax feedback port ID. |
| `UCAN1_FB6_SUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal ESC 6 zubax feedback port ID. |
| `UCAN1_FB7_SUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal ESC 7 zubax feedback port ID. |
| `UCAN1_GPS0_SUB` | int32 | -1 | -1 ~ 6143 |  | GPS 0 subscription port ID. |
| `UCAN1_GPS1_SUB` | int32 | -1 | -1 ~ 6143 |  | GPS 1 subscription port ID. |
| `UCAN1_GPS_PUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal GPS publication port ID. |
| `UCAN1_LG_BMS_SUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal legacy battery port ID. |
| `UCAN1_READ_PUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal ESC readiness port ID. |
| `UCAN1_SERVO_PUB` | int32 | -1 | -1 ~ 6143 |  | Cyphal Servo publication port ID. |
| `UCAN1_UORB_GPS` | int32 | -1 | -1 ~ 6143 |  | sensor_gps uORB over Cyphal subscription port ID. |
| `UCAN1_UORB_GPS_P` | int32 | -1 | -1 ~ 6143 |  | sensor_gps uORB over Cyphal publication port ID. |

## System

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RPM_CAP_ENABLE` | int32 | 0 |  |  | RPM capture enable |
| `RPM_PULS_PER_REV` | int32 | 1 | 1 ~ 50 |  | Voltage pulses per revolution |
| `SYS_AUTOCONFIG` | int32 | 0 |  |  | Automatically configure default values. |
| `SYS_AUTOSTART` | int32 | 0 | 0 ~ 9999999 |  | Auto-start script index. |
| `SYS_BL_UPDATE` | int32 | 0 |  |  | Bootloader update |
| `SYS_CAL_ACCEL` | int32 | 0 | 0 ~ 1 |  | Enable auto start of accelerometer thermal calibration at the next power up. |
| `SYS_CAL_BARO` | int32 | 0 | 0 ~ 1 |  | Enable auto start of barometer thermal calibration at the next power up. |
| `SYS_CAL_GYRO` | int32 | 0 | 0 ~ 1 |  | Enable auto start of rate gyro thermal calibration at the next power up. |
| `SYS_CAL_TDEL` | int32 | 24 | 10 ~  | celcius | Required temperature rise during thermal calibration |
| `SYS_CAL_TMAX` | int32 | 10 |  | celcius | Maximum starting temperature for thermal calibration |
| `SYS_CAL_TMIN` | int32 | 5 |  | celcius | Minimum starting temperature for thermal calibration |
| `SYS_DM_BACKEND` | int32 | 0 |  |  | Dataman storage backend |
| `SYS_FAC_CAL_MODE` | int32 | 0 |  |  | Enable factory calibration mode |
| `SYS_FAILURE_EN` | int32 | 0 |  |  | Enable failure injection |
| `SYS_HAS_BARO` | int32 | 1 |  |  | Control if the vehicle has a barometer |
| `SYS_HAS_GPS` | int32 | 1 |  |  | Control if the vehicle has a GPS |
| `SYS_HAS_MAG` | int32 | 1 |  |  | Control if and how many magnetometers are expected |
| `SYS_HAS_NUM_ASPD` | int32 | 0 | 0 ~ 1 |  | Control if the vehicle has an airspeed sensor |
| `SYS_HAS_NUM_DIST` | int32 | 0 | 0 ~ 4 |  | Number of distance sensors to check being available |
| `SYS_HAS_NUM_OF` | int32 | 0 | 0 ~ 1 |  | Number of optical flow sensors required to be available |
| `SYS_HF_MAV` | int32 | 1 |  |  | Enable FMU SD card hardfault streaming |
| `SYS_HITL` | int32 | 0 |  |  | Enable HITL/SIH mode on next boot |
| `SYS_PARAM_VER` | int32 | 1 | 0 ~  |  | Parameter version |
| `SYS_RGB_MAXBRT` | float | 1.f |  | % | RGB Led brightness limit |
| `SYS_STCK_EN` | int32 | 1 |  |  | Enable stack checking |

## Radio Switches

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RC_ARMSWITCH_TH` | float | 0.75f | -1 ~ 1 |  | Threshold for the arm switch |
| `RC_ENG_MOT_TH` | float | 0.75f | -1 ~ 1 |  | Threshold for selecting main motor engage |
| `RC_GEAR_TH` | float | 0.75f | -1 ~ 1 |  | Threshold for the landing gear switch |
| `RC_KILLSWITCH_TH` | float | 0.75f | -1 ~ 1 |  | Threshold for the kill switch |
| `RC_LOITER_TH` | float | 0.75f | -1 ~ 1 |  | Threshold for selecting loiter mode |
| `RC_MAP_ARM_SW` | int32 | 0 | 0 ~ 18 |  | Arm switch channel. |
| `RC_MAP_FLAPS` | int32 | 0 | 0 ~ 18 |  | Flaps channel |
| `RC_MAP_FLTMODE` | int32 | 0 | 0 ~ 18 |  | Single channel flight mode selection |
| `RC_MAP_FLTM_BTN` | int32 | 0 | 0 ~ 258048 |  | Button flight mode selection |
| `RC_MAP_GEAR_SW` | int32 | 0 | 0 ~ 18 |  | Landing gear switch channel |
| `RC_MAP_KILL_SW` | int32 | 0 | 0 ~ 18 |  | Emergency Kill switch channel |
| `RC_MAP_LOITER_SW` | int32 | 0 | 0 ~ 18 |  | Loiter switch channel |
| `RC_MAP_MODE_SW` | int32 | 0 | 0 ~ 18 |  | Mode switch channel mapping (deprecated) |
| `RC_MAP_OFFB_SW` | int32 | 0 | 0 ~ 18 |  | Offboard switch channel |
| `RC_MAP_PAY_SW` | int32 | 0 | 0 ~ 18 |  | Payload Power Switch RC channel |
| `RC_MAP_RETURN_SW` | int32 | 0 | 0 ~ 18 |  | Return switch channel |
| `RC_MAP_TERM_SW` | int32 | 0 | 0 ~ 18 |  | Termination switch channel |
| `RC_MAP_TRANS_SW` | int32 | 0 | 0 ~ 18 |  | VTOL transition switch channel mapping |
| `RC_OFFB_TH` | float | 0.75f | -1 ~ 1 |  | Threshold for selecting offboard mode |
| `RC_PAYLOAD_MIDTH` | float | 0.25f | -1 ~ 1 |  | Threshold for mid position of payload power switch |
| `RC_PAYLOAD_TH` | float | 0.75f | -1 ~ 1 |  | Threshold for on position of payload power switch |
| `RC_RETURN_TH` | float | 0.75f | -1 ~ 1 |  | Threshold for selecting return to launch mode |
| `RC_TRANS_TH` | float | 0.75f | -1 ~ 1 |  | Threshold for the VTOL transition switch |

## Vertiq IO

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `VTQ_ARM_BEHAVE` | enum | 0 |  |  | The triggered behavior on PX4 arm |
| `VTQ_BAUD` | int32 | 115200 |  |  | The IQUART driver's baud rate |
| `VTQ_CONTROL_MODE` | enum | 0 |  |  | Module Param - The module's control mechanism |
| `VTQ_DISARM_TRIG` | enum | 0 |  |  | The triggered behavior sent to the motors on PX4 disarm |
| `VTQ_DISARM_VELO` | int32 | 0 | 0 ~ 100 |  | Velocity sent when DISARM_TRIGGER is Set Predefined Velocity Setpoint |
| `VTQ_FC_DIR` | enum | 0 |  |  | Module Param - If the flight controller uses 2D or 3D communication |
| `VTQ_MAX_VELOCITY` | float | 0 |  |  | Module Param - Maximum velocity when CONTROL_MODE is set to Velocity |
| `VTQ_MAX_VOLTS` | float | 0 |  |  | Module Param - Maximum voltage when CONTROL_MODE is set to Voltage |
| `VTQ_MOTOR_DIR` | enum | 0 |  |  | Module Param - The direction that the module should spin |
| `VTQ_NUM_CVS` | int32 | 0 | 0 ~ 16 |  | The number of Vertiq IFCI parameters to use |
| `VTQ_PULSE_V_LIM` | float | 0 |  |  | Module Param - Max pulsing voltage limit when in Voltage Limit Mode |
| `VTQ_PULSE_V_MODE` | enum | 0 |  |  | Module Param - 0 = Supply Voltage Mode, 1 = Voltage Limit Mode |
| `VTQ_REDO_READ` | boolean | 0 |  |  | Reinitialize the target module's values into the PX4 parameters |
| `VTQ_TELEM_IDS_1` | bitmask | 0 |  |  | Module IDs [0, 31] that you would like to request telemetry from |
| `VTQ_TELEM_IDS_2` | bitmask | 0 |  |  | Module IDs [32, 62] that you would like to request telemetry from |
| `VTQ_THROTTLE_CVI` | int32 | 0 | 0 ~ 255 |  | Module Param - The module's Throttle Control Value Index |
| `VTQ_TQUE_OFF_ANG` | float | 0 |  |  | Module Param - Offsets pulse angle to allow for mechanical properties |
| `VTQ_TRGT_MOD_ID` | int32 | 0 |  |  | The Module ID of the module you would like to communicate with |
| `VTQ_VELO_CUTOFF` | float | 0 |  |  | Module Param - The minimum velocity required to allow pulsing |
| `VTQ_X_CVI` | int32 | 0 | 0 ~ 255 |  | Module Param - CVI for the X rectangular coordinate |
| `VTQ_Y_CVI` | int32 | 0 | 0 ~ 255 |  | Module Param - CVI for the Y rectangular coordinate |
| `VTQ_ZERO_ANGLE` | float | 0 |  |  | Module Param - The encoder angle at which theta is zero |

## Mission

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MIS_COMMAND_TOUT` | float | 0.f | 0 ~  | s | Timeout to allow the payload to execute the mission command |
| `MIS_DIST_1WP` | float | 10000 | -1 ~ 100000 | m | Maximal horizontal distance from Home to first waypoint |
| `MIS_LND_ABRT_ALT` | int32 | 30 | 0 ~  | m | Landing abort min altitude |
| `MIS_MNT_YAW_CTL` | int32 | 0 | 0 ~ 1 |  | Enable yaw control of the mount. (Only affects multicopters and ROI mission items) |
| `MIS_TAKEOFF_ALT` | float | 2.5f | 0 ~  | m | Default take-off altitude |
| `MIS_TKO_LAND_REQ` | int32 | 0 |  |  | Mission takeoff/landing required |
| `MIS_YAW_ERR` | float | 12.0f | 0 ~ 90 | deg | Max yaw error in degrees needed for waypoint heading acceptance. |
| `MIS_YAW_TMT` | float | -1.0f | -1 ~ 20 | s | Time in seconds we wait on reaching target heading at a waypoint if it is forced. |
| `MPC_YAW_MODE` | int32 | 0 | 0 ~ 4 |  | Heading behavior in autonomous modes |
| `NAV_ACC_RAD` | float | 10.0f | 0.05 ~ 200.0 | m | Acceptance Radius |
| `NAV_FORCE_VT` | int32 | 1 |  |  | Force VTOL mode takeoff and land |
| `NAV_FW_ALTL_RAD` | float | 5.0f | 0.05 ~ 200.0 | m | FW Altitude Acceptance Radius before a landing |
| `NAV_FW_ALT_RAD` | float | 10.0f | 0.05 ~ 200.0 | m | FW Altitude Acceptance Radius |
| `NAV_LOITER_RAD` | float | 80.0f | -10000 ~ 10000 | m | Loiter radius (FW only) |
| `NAV_MC_ALT_RAD` | float | 0.8f | 0.05 ~ 200.0 | m | MC Altitude Acceptance Radius |
| `NAV_MIN_GND_DIST` | float | -1.f | -1 ~  | m | Minimum height above ground during Mission and RTL |
| `NAV_MIN_LTR_ALT` | float | -1.f | -1 ~  | m | Minimum Loiter altitude |
| `NAV_TRAFF_AVOID` | int32 | 1 |  |  | Set traffic avoidance mode |
| `NAV_TRAFF_A_HOR` | float | 500 | 500 ~  | m | Set NAV TRAFFIC AVOID horizontal distance |
| `NAV_TRAFF_A_VER` | float | 500 | 10 ~ 500 | m | Set NAV TRAFFIC AVOID vertical distance |
| `NAV_TRAFF_COLL_T` | int32 | 60 | 1 ~ 900000000 | s | Estimated time until collision |

## Simulation In Hardware

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SIH_DISTSNSR_MAX` | float | 100.0f | 0.0 ~ 1000.0 | m | distance sensor maximum range |
| `SIH_DISTSNSR_MIN` | float | 0.0f | 0.0 ~ 10.0 | m | distance sensor minimum range |
| `SIH_DISTSNSR_OVR` | float | -1.0f |  | m | if >= 0 the distance sensor measures will be overridden by this value |
| `SIH_IXX` | float | 0.025f | 0.0 ~  | kg m^2 | Vehicle inertia about X axis |
| `SIH_IXY` | float | 0.0f |  | kg m^2 | Vehicle cross term inertia xy |
| `SIH_IXZ` | float | 0.0f |  | kg m^2 | Vehicle cross term inertia xz |
| `SIH_IYY` | float | 0.025f | 0.0 ~  | kg m^2 | Vehicle inertia about Y axis |
| `SIH_IYZ` | float | 0.0f |  | kg m^2 | Vehicle cross term inertia yz |
| `SIH_IZZ` | float | 0.030f | 0.0 ~  | kg m^2 | Vehicle inertia about Z axis |
| `SIH_KDV` | float | 1.0f | 0.0 ~  | N/(m/s) | First order drag coefficient |
| `SIH_KDW` | float | 0.025f | 0.0 ~  | Nm/(rad/s) | First order angular damper coefficient |
| `SIH_LOC_H0` | float | 489.4f | -420.0 ~ 8848.0 | m | Initial AMSL ground altitude |
| `SIH_LOC_LAT0` | float | 47.397742f | -90 ~ 90 | deg | Initial geodetic latitude |
| `SIH_LOC_LON0` | float | 8.545594f | -180 ~ 180 | deg | Initial geodetic longitude |
| `SIH_L_PITCH` | float | 0.2f | 0.0 ~  | m | Pitch arm length |
| `SIH_L_ROLL` | float | 0.2f | 0.0 ~  | m | Roll arm length |
| `SIH_MASS` | float | 1.0f | 0.0 ~  | kg | Vehicle mass |
| `SIH_Q_MAX` | float | 0.1f | 0.0 ~  | Nm | Max propeller torque |
| `SIH_T_MAX` | float | 5.0f | 0.0 ~  | N | Max propeller thrust force |
| `SIH_T_TAU` | float | 0.05f |  | s | thruster time constant tau |
| `SIH_VEHICLE_TYPE` | int32 | 0 |  |  | Vehicle type |

## Spacecraft Position Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SC_MAN_TILT_TAU` | float | 0.0f | 0.0 ~ 2.0 | s | Manual tilt input filter time constant |
| `SC_MAN_Y_SCALE` | float | 150.f | 0 ~ 400 | deg/s | Max manual yaw rate for Stabilized, Altitude, Position mode |
| `SPC_ACC` | float | 3.f | 2 ~ 15 | m/s^2 | Acceleration for autonomous and for manual modes |
| `SPC_ACC_MAX` | float | 5.f | 2 ~ 15 | m/s^2 | Maximum accelaration in autonomous modes |
| `SPC_JERK_AUTO` | float | 4.f | 1 ~ 80 | m/s^3 | Jerk limit in autonomous modes |
| `SPC_JERK_MAX` | float | 8.f | 0.5 ~ 500 | m/s^3 | Maximum jerk in Position/Altitude mode |
| `SPC_MAN_Y_MAX` | float | 150.f | 0 ~ 400 | deg/s | Max manual yaw rate for Stabilized, Altitude, Position mode |
| `SPC_MAN_Y_TAU` | float | 0.08f | 0 ~ 5 | s | Manual yaw rate input filter time constant |
| `SPC_POS_I` | float | 0.f | 0 ~ 15 |  | Integral gain for position error |
| `SPC_POS_I_LIM` | float | 1.f | 0 ~ 5 |  | Integral limit for position error |
| `SPC_POS_P` | float | 0.2f | 0 ~ 2 |  | Proportional gain for position error |
| `SPC_THR_MAX` | float | 1.f | 0 ~ 1 | norm | Maximum collective thrust |
| `SPC_VELD_LP` | float | 5.0f | 0 ~ 10 | Hz | Numerical velocity derivative low pass cutoff frequency |
| `SPC_VEL_ALL` | float | -10.f | -20 ~ 20 |  | Overall Velocity Limit |
| `SPC_VEL_CRUISE` | float | 10.f | 3 ~ 20 | m/s | Cruising elocity setpoint in autonomous modes |
| `SPC_VEL_D` | float | 0.0f | 0.0 ~ 15 |  | Derivative gain for velocity error |
| `SPC_VEL_I` | float | 0.f | 0 ~ 15 |  | Integral gain for velocity error |
| `SPC_VEL_I_LIM` | float | 1.f | 0 ~ 5 |  | Integral limit for velocity error |
| `SPC_VEL_MANUAL` | float | 10.f | 3 ~ 20 | m/s | Maximum velocity setpoint in Position mode |
| `SPC_VEL_MAX` | float | 12.f | 0 ~ 20 | m/s | Maximum velocity |
| `SPC_VEL_P` | float | 6.55f | 0 ~ 15 |  | Proportional gain for velocity error |

## UUV Attitude Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `UUV_MGM_PITCH` | float | 0.05f | 0.0 ~  |  | Pitch gain for manual inputs in manual control mode |
| `UUV_MGM_ROLL` | float | 0.05f | 0.0 ~  |  | Roll gain for manual inputs in manual control mode |
| `UUV_MGM_THRTL` | float | 0.1f | 0.0 ~  |  | Throttle gain for manual inputs in manual control mode |
| `UUV_MGM_YAW` | float | 0.05f | 0.0 ~  |  | Yaw gain for manual inputs in manual control mode |
| `UUV_PITCH_D` | float | 2.0f |  |  | Pitch differential gain |
| `UUV_PITCH_P` | float | 4.0f |  |  | Pitch proportional gain |
| `UUV_RGM_PITCH` | float | 100.0f | 0.0 ~  |  | Pitch gain for manual inputs in rate control mode |
| `UUV_RGM_ROLL` | float | 100.0f | 0.0 ~  |  | Roll gain for manual inputs in rate control mode |
| `UUV_RGM_THRTL` | float | 10.0f | 0.0 ~  |  | Throttle gain for manual inputs in rate control mode |
| `UUV_RGM_YAW` | float | 100.0f | 0.0 ~  |  | Yaw gain for manual inputs in rate control mode |
| `UUV_ROLL_D` | float | 1.5f |  |  | Roll differential gain |
| `UUV_ROLL_P` | float | 4.0f |  |  | Roll proportional gain |
| `UUV_SGM_PITCH` | float | 0.5f | 0.0 ~  |  | Pitch gain for manual inputs in attitude control mode |
| `UUV_SGM_ROLL` | float | 0.5f | 0.0 ~  |  | Roll gain for manual inputs in attitude control mode |
| `UUV_SGM_THRTL` | float | 0.1f | 0.0 ~  |  | Throttle gain for manual inputs in attitude control mode |
| `UUV_SGM_YAW` | float | 0.5f | 0.0 ~  |  | Yaw gain for manual inputs in attitude control mode |
| `UUV_SP_MAX_AGE` | float | 2.0f |  |  | Maximum time (in seconds) before resetting setpoint |
| `UUV_THRUST_SAT` | float | 0.1f | 0.0 ~ 1.0 |  | UUV Thrust setpoint Saturation |
| `UUV_TORQUE_SAT` | float | 0.3f | 0.0 ~ 1.0 |  | UUV Torque setpoint Saturation |
| `UUV_YAW_D` | float | 2.0f |  |  | Yaw differential gain |
| `UUV_YAW_P` | float | 4.0f |  |  | Yawh proportional gain |

## FW Longitudinal Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `FW_GND_SPD_MIN` | float | 5.0f | 0.0 ~ 40 | m/s | Minimum groundspeed |
| `FW_THR_SLEW_MAX` | float | 0.0f | 0.0 ~ 1.0 |  | Throttle max slew rate |
| `FW_T_ALT_TC` | float | 5.0f | 2.0 ~  |  | Altitude error time constant. |
| `FW_T_F_ALT_ERR` | float | -1.0f | -1.0 ~  |  | Fast descend: minimum altitude error |
| `FW_T_HRATE_FF` | float | 0.3f | 0.0 ~ 1.0 |  | Height rate feed forward |
| `FW_T_I_GAIN_PIT` | float | 0.1f | 0.0 ~ 2.0 |  | Integrator gain pitch |
| `FW_T_PTCH_DAMP` | float | 0.1f | 0.0 ~ 2.0 |  | Pitch damping gain |
| `FW_T_RLL2THR` | float | 15.0f | 0.0 ~ 20.0 |  | Roll -> Throttle feedforward |
| `FW_T_SEB_R_FF` | float | 1.0f | 0.5 ~ 3 |  | Specific total energy balance rate feedforward gain. |
| `FW_T_SINK_MAX` | float | 5.0f | 1.0 ~ 15.0 | m/s | Maximum descent rate |
| `FW_T_SPD_DEV_STD` | float | 0.2f | 0.01 ~ 10.0 | m/s^2 | Airspeed rate measurement standard deviation |
| `FW_T_SPD_PRC_STD` | float | 0.2f | 0.01 ~ 10.0 | m/s^2 | Process noise standard deviation for the airspeed rate |
| `FW_T_SPD_STD` | float | 0.07f | 0.01 ~ 10.0 | m/s | Airspeed measurement standard deviation |
| `FW_T_STE_R_TC` | float | 0.4f | 0.0 ~ 2 |  | Specific total energy rate first order filter time constant. |
| `FW_T_TAS_TC` | float | 5.0f | 2.0 ~  |  | True airspeed error time constant. |
| `FW_T_THR_DAMPING` | float | 0.05f | 0.0 ~ 1.0 |  | Throttle damping factor |
| `FW_T_THR_INTEG` | float | 0.02f | 0.0 ~ 1.0 |  | Integrator gain throttle |
| `FW_T_THR_LOW_HGT` | float | -1.f | -1 ~  | m | Low-height threshold for tighter altitude tracking |
| `FW_T_VERT_ACC` | float | 7.0f | 1.0 ~ 10.0 | m/s^2 | Maximum vertical acceleration |
| `FW_WIND_ARSP_SC` | float | 0.f | 0 ~  |  | Wind-based airspeed scaling factor |

## Multicopter Rate Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MC_BAT_SCALE_EN` | int32 | 0 |  |  | Battery power level scaler |
| `MC_PITCHRATE_D` | float | 0.003f | 0.0 ~  |  | Pitch rate D gain |
| `MC_PITCHRATE_FF` | float | 0.0f | 0.0 ~  |  | Pitch rate feedforward |
| `MC_PITCHRATE_I` | float | 0.2f | 0.0 ~  |  | Pitch rate I gain |
| `MC_PITCHRATE_K` | float | 1.0f | 0.01 ~ 5.0 |  | Pitch rate controller gain |
| `MC_PITCHRATE_P` | float | 0.15f | 0.01 ~ 0.6 |  | Pitch rate P gain |
| `MC_PR_INT_LIM` | float | 0.30f | 0.0 ~  |  | Pitch rate integrator limit |
| `MC_ROLLRATE_D` | float | 0.003f | 0.0 ~ 0.01 |  | Roll rate D gain |
| `MC_ROLLRATE_FF` | float | 0.0f | 0.0 ~  |  | Roll rate feedforward |
| `MC_ROLLRATE_I` | float | 0.2f | 0.0 ~  |  | Roll rate I gain |
| `MC_ROLLRATE_K` | float | 1.0f | 0.01 ~ 5.0 |  | Roll rate controller gain |
| `MC_ROLLRATE_P` | float | 0.15f | 0.01 ~ 0.5 |  | Roll rate P gain |
| `MC_RR_INT_LIM` | float | 0.30f | 0.0 ~  |  | Roll rate integrator limit |
| `MC_YAWRATE_D` | float | 0.0f | 0.0 ~  |  | Yaw rate D gain |
| `MC_YAWRATE_FF` | float | 0.0f | 0.0 ~  |  | Yaw rate feedforward |
| `MC_YAWRATE_I` | float | 0.1f | 0.0 ~  |  | Yaw rate I gain |
| `MC_YAWRATE_K` | float | 1.0f | 0.01 ~ 5.0 |  | Yaw rate controller gain |
| `MC_YAWRATE_P` | float | 0.2f | 0.0 ~ 0.6 |  | Yaw rate P gain |
| `MC_YAW_TQ_CUTOFF` | float | 2.f | 0 ~ 10 | Hz | Low pass filter cutoff frequency for yaw torque setpoint |
| `MC_YR_INT_LIM` | float | 0.30f | 0.0 ~  |  | Yaw rate integrator limit |

## Airspeed Validator

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `ASPD_BETA_GATE` | int32 | 1 | 1 ~ 5 | SD | Gate size for sideslip angle fusion |
| `ASPD_BETA_NOISE` | float | 0.15f | 0 ~ 1 | rad | Wind estimator sideslip measurement noise |
| `ASPD_DO_CHECKS` | int32 | 7 | 0 ~ 31 |  | Enable checks on airspeed sensors |
| `ASPD_FALLBACK` | int32 | 0 |  |  | Fallback options |
| `ASPD_FP_T_WINDOW` | float | 2.0f | 0 ~  | s | First principle airspeed check time window |
| `ASPD_FS_INNOV` | float | 5.f | 0.5 ~ 10.0 | m/s | Airspeed failure innovation threshold |
| `ASPD_FS_INTEG` | float | 10.f | 0.0 ~ 50.0 | m | Airspeed failure innovation integral threshold |
| `ASPD_FS_T_START` | float | -1.f | -1.0 ~  | s | Airspeed failsafe start delay |
| `ASPD_FS_T_STOP` | float | 1.f | 0.0 ~  | s | Airspeed failsafe stop delay |
| `ASPD_PRIMARY` | int32 | 1 |  |  | Index or primary airspeed measurement source |
| `ASPD_SCALE_1` | float | 1.0f | 0.5 ~ 2.0 |  | Scale of airspeed sensor 1 |
| `ASPD_SCALE_2` | float | 1.0f | 0.5 ~ 2.0 |  | Scale of airspeed sensor 2 |
| `ASPD_SCALE_3` | float | 1.0f | 0.5 ~ 2.0 |  | Scale of airspeed sensor 3 |
| `ASPD_SCALE_APPLY` | int32 | 2 |  |  | Controls when to apply the new estimated airspeed scale(s) |
| `ASPD_SCALE_NSD` | float | 1.e-4f | 0 ~ 0.1 | 1/s/sqrt(Hz) | Wind estimator true airspeed scale process noise spectral density |
| `ASPD_TAS_GATE` | int32 | 4 | 1 ~ 5 | SD | Gate size for true airspeed fusion |
| `ASPD_TAS_NOISE` | float | 1.4f | 0 ~ 4 | m/s | Wind estimator true airspeed measurement noise |
| `ASPD_WERR_THR` | float | 2.f | 0.01 ~ 5 | m/s | Horizontal wind uncertainty threshold for valid ground-minus-wind |
| `ASPD_WIND_NSD` | float | 1.e-1f | 0 ~ 1 | m/s^2/sqrt(Hz) | Wind estimator wind process noise spectral density |

## EKF2

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `EKF2_ACC_NOISE` | float | 0.35 | 0.01 ~ 1.0 | m/s^2 | Accelerometer noise for covariance prediction |
| `EKF2_ANGERR_INIT` | float | 0.1 | 0.0 ~ 0.5 | rad | 1-sigma tilt angle uncertainty after gravity vector alignment |
| `EKF2_DELAY_MAX` | float | 200 | 0 ~ 1000 | ms | Maximum delay of all the aiding sensors |
| `EKF2_EN` | boolean | 1 |  |  | EKF2 enable |
| `EKF2_GYR_NOISE` | float | 0.015 | 0.0001 ~ 0.1 | rad/s | Rate gyro noise for covariance prediction |
| `EKF2_HDG_GATE` | float | 2.6 | 1.0 ~  | SD | Gate size for heading fusion |
| `EKF2_HEAD_NOISE` | float | 0.3 | 0.01 ~ 1.0 | rad | Measurement noise for magnetic heading fusion |
| `EKF2_HGT_REF` | enum | 1 |  |  | Determines the reference source of height data used by the EKF |
| `EKF2_IMU_CTRL` | bitmask | 7 | 0 ~ 7 |  | IMU control |
| `EKF2_IMU_POS_X` | float | 0.0 |  | m | X position of IMU in body frame |
| `EKF2_IMU_POS_Y` | float | 0.0 |  | m | Y position of IMU in body frame |
| `EKF2_IMU_POS_Z` | float | 0.0 |  | m | Z position of IMU in body frame |
| `EKF2_LOG_VERBOSE` | boolean | 1 |  |  | Verbose logging |
| `EKF2_NOAID_NOISE` | float | 10.0 | 0.5 ~ 50.0 | m | Measurement noise for non-aiding position hold |
| `EKF2_NOAID_TOUT` | int32 | 5000000 | 500000 ~ 10000000 | us | Maximum inertial dead-reckoning time |
| `EKF2_PREDICT_US` | int32 | 10000 | 1000 ~ 20000 | us | EKF prediction period |
| `EKF2_TAU_POS` | float | 0.25 | 0.1 ~ 1.0 | s | Output predictor position time constant |
| `EKF2_TAU_VEL` | float | 0.25 |  ~ 1.0 | s | Time constant of the velocity output prediction and smoothing filter |
| `EKF2_VEL_LIM` | float | 100 |  ~ 299792458 | m/s | Velocity limit |

## Mount

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MNT_DO_STAB` | int32 | 0 | 0 ~ 2 |  | Stabilize the mount |
| `MNT_LND_P_MAX` | float | 90.0f | -90.0 ~ 90.0 | deg | Pitch maximum when landed |
| `MNT_LND_P_MIN` | float | -90.0f | -90.0 ~ 90.0 | deg | Pitch minimum when landed |
| `MNT_MAN_PITCH` | int32 | 0 | 0 ~ 6 |  | Auxiliary channel to control pitch (in AUX input or manual mode). |
| `MNT_MAN_ROLL` | int32 | 0 | 0 ~ 6 |  | Auxiliary channel to control roll (in AUX input or manual mode). |
| `MNT_MAN_YAW` | int32 | 0 | 0 ~ 6 |  | Auxiliary channel to control yaw (in AUX input or manual mode). |
| `MNT_MAV_COMPID` | int32 | 154 |  |  | Mavlink Component ID of the mount |
| `MNT_MAV_SYSID` | int32 | 1 |  |  | Mavlink System ID of the mount |
| `MNT_MODE_IN` | int32 | -1 | -1 ~ 4 |  | Mount input mode |
| `MNT_MODE_OUT` | int32 | 0 | 0 ~ 2 |  | Mount output mode |
| `MNT_OFF_PITCH` | float | 0.0f | -360.0 ~ 360.0 | deg | Offset for pitch channel output in degrees. |
| `MNT_OFF_ROLL` | float | 0.0f | -360.0 ~ 360.0 | deg | Offset for roll channel output in degrees. |
| `MNT_OFF_YAW` | float | 0.0f | -360.0 ~ 360.0 | deg | Offset for yaw channel output in degrees. |
| `MNT_RANGE_PITCH` | float | 90.0f | 1.0 ~ 720.0 | deg | Range of pitch channel output in degrees (only in AUX output mode). |
| `MNT_RANGE_ROLL` | float | 90.0f | 1.0 ~ 720.0 | deg | Range of roll channel output in degrees (only in AUX output mode). |
| `MNT_RANGE_YAW` | float | 360.0f | 1.0 ~ 720.0 | deg | Range of yaw channel output in degrees (only in AUX output mode). |
| `MNT_RATE_PITCH` | float | 30.0f | 1.0 ~ 90.0 | deg/s | Angular pitch rate for manual input in degrees/second. |
| `MNT_RATE_YAW` | float | 30.0f | 1.0 ~ 90.0 | deg/s | Angular yaw rate for manual input in degrees/second. |
| `MNT_RC_IN_MODE` | int32 | 1 | 0 ~ 1 |  | Input mode for RC gimbal input |

## VOXL ESC

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `VOXL_ESC_BAUD` | int32 | 250000 |  | bit/s | UART ESC baud rate |
| `VOXL_ESC_CONFIG` | int32 | 0 | 0 ~ 1 |  | UART ESC configuration |
| `VOXL_ESC_GPIO_CH` | int32 | 0 | 0 ~ 6 |  | GPIO Control Channel |
| `VOXL_ESC_MODE` | int32 | 0 | 0 ~ 2 |  | UART ESC Mode |
| `VOXL_ESC_PUB_BST` | int32 | 1 | 0 ~ 1 |  | UART ESC Enable publishing of battery status |
| `VOXL_ESC_RPM_MAX` | int32 | 15000 |  | rpm | UART ESC RPM Max |
| `VOXL_ESC_RPM_MIN` | int32 | 5500 |  | rpm | UART ESC RPM Min |
| `VOXL_ESC_SDIR1` | int32 | 0 |  |  | UART ESC ID 1 Spin Direction Flag |
| `VOXL_ESC_SDIR2` | int32 | 0 |  |  | UART ESC ID 2 Spin Direction Flag |
| `VOXL_ESC_SDIR3` | int32 | 0 |  |  | UART ESC ID 3 Spin Direction Flag |
| `VOXL_ESC_SDIR4` | int32 | 0 |  |  | UART ESC ID 4 Spin Direction Flag |
| `VOXL_ESC_T_COSP` | float | 0.990 | 0.000 ~ 1.000 |  | UART ESC Turtle Mode Cosphi |
| `VOXL_ESC_T_DEAD` | int32 | 20 | 0 ~ 100 |  | UART ESC Turtle Mode Crash Flip Motor Deadband |
| `VOXL_ESC_T_EXPO` | int32 | 35 | 0 ~ 100 |  | UART ESC Turtle Mode Crash Flip Motor expo |
| `VOXL_ESC_T_MINF` | float | 0.15 | 0.0 ~ 100.0 |  | UART ESC Turtle Mode Crash Flip Motor STICK_MINF |
| `VOXL_ESC_T_OVER` | int32 | 0 | 0 ~ 200 |  | UART ESC Over-Temperature Threshold (Degrees C) |
| `VOXL_ESC_T_PERC` | int32 | 90 | 1 ~ 100 |  | UART ESC Turtle Mode Crash Flip Motor Percent |
| `VOXL_ESC_T_WARN` | int32 | 0 | 0 ~ 200 |  | UART ESC Temperature Warning Threshold (Degrees C) |
| `VOXL_ESC_VLOG` | int32 | 0 | 0 ~ 1 |  | UART ESC verbose logging |

## Testing

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `TEST_1` | int32 | 2 |  |  |  |
| `TEST_2` | int32 | 4 |  |  |  |
| `TEST_3` | float | 5.0f |  |  |  |
| `TEST_D` | float | 0.01f |  |  |  |
| `TEST_DEV` | float | 2.0f |  |  |  |
| `TEST_D_LP` | float | 10.0f |  |  |  |
| `TEST_HP` | float | 10.0f |  |  |  |
| `TEST_I` | float | 0.1f |  |  |  |
| `TEST_I_MAX` | float | 1.0f |  |  |  |
| `TEST_LP` | float | 10.0f |  |  |  |
| `TEST_MAX` | float | 1.0f |  |  |  |
| `TEST_MEAN` | float | 1.0f |  |  |  |
| `TEST_MIN` | float | -1.0f |  |  |  |
| `TEST_P` | float | 0.2f |  |  |  |
| `TEST_PARAMS` | int32 | 12345678 |  |  |  |
| `TEST_RC2_X` | int32 | 16 |  |  |  |
| `TEST_RC_X` | int32 | 8 |  |  |  |
| `TEST_TRIM` | float | 0.5f |  |  |  |

## FW Attitude Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `FW_MAN_P_MAX` | float | 30.0f | 0.0 ~ 90.0 | deg | Maximum manual pitch angle |
| `FW_MAN_R_MAX` | float | 45.0f | 0.0 ~ 90.0 | deg | Maximum manual roll angle |
| `FW_MAN_YR_MAX` | float | 30.f | 0 ~  | deg/s | Maximum manually added yaw rate |
| `FW_PSP_OFF` | float | 0.0f | -90.0 ~ 90.0 | deg | Pitch setpoint offset (pitch at level flight) |
| `FW_P_RMAX_NEG` | float | 60.0f | 0.0 ~ 180 | deg/s | Maximum negative / down pitch rate setpoint |
| `FW_P_RMAX_POS` | float | 60.0f | 0.0 ~ 180 | deg/s | Maximum positive / up pitch rate setpoint |
| `FW_P_TC` | float | 0.4f | 0.2 ~ 1.0 | s | Attitude pitch time constant |
| `FW_R_RMAX` | float | 70.0f | 0.0 ~ 180 | deg/s | Maximum roll rate setpoint |
| `FW_R_TC` | float | 0.4f | 0.2 ~ 1.0 | s | Attitude Roll Time Constant |
| `FW_WR_FF` | float | 0.2f | 0.0 ~ 10 | %/rad/s | Wheel steering rate feed forward |
| `FW_WR_I` | float | 0.1f | 0.0 ~ 10 | %/rad | Wheel steering rate integrator gain |
| `FW_WR_IMAX` | float | 0.4f | 0.0 ~ 1.0 |  | Wheel steering rate integrator limit |
| `FW_WR_P` | float | 0.5f | 0.0 ~ 10 | %/rad/s | Wheel steering rate proportional gain |
| `FW_W_EN` | int32 | 0 |  |  | Enable wheel steering controller |
| `FW_W_RMAX` | float | 30.0f | 0.0 ~ 90.0 | deg/s | Maximum wheel steering rate |
| `FW_Y_RMAX` | float | 50.0f | 0.0 ~ 180 | deg/s | Maximum yaw rate setpoint |

## FW Auto Landing

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `FW_FLAPS_LND_SCL` | float | 1.0f | 0.0 ~ 1.0 | norm | Flaps setting during landing |
| `FW_LND_ABORT` | int32 | 3 | 0 ~ 3 |  | Bit mask to set the automatic landing abort conditions. |
| `FW_LND_AIRSPD` | float | -1.f | -1.0 ~  | m/s | Landing airspeed |
| `FW_LND_ANG` | float | 5.0f | 1.0 ~ 45.0 | deg | Maximum landing slope angle |
| `FW_LND_EARLYCFG` | int32 | 0 |  |  | Early landing configuration deployment |
| `FW_LND_FLALT` | float | 0.5f | 0.0 ~  | m | Landing flare altitude (relative to landing altitude) |
| `FW_LND_FL_PMAX` | float | 15.0f | 0 ~ 45.0 | deg | Flare, maximum pitch |
| `FW_LND_FL_PMIN` | float | 2.5f | -5 ~ 15.0 | deg | Flare, minimum pitch |
| `FW_LND_FL_SINK` | float | 0.25f | 0.0 ~ 2 | m/s | Landing flare sink rate |
| `FW_LND_FL_TIME` | float | 1.0f | 0.1 ~ 5.0 | s | Landing flare time |
| `FW_LND_NUDGE` | int32 | 2 | 0 ~ 2 |  | Landing touchdown nudging option. |
| `FW_LND_TD_OFF` | float | 3.0 | 0.0 ~ 10.0 | m | Maximum lateral position offset for the touchdown point |
| `FW_LND_TD_TIME` | float | -1.0f | -1.0 ~ 5.0 | s | Landing touchdown time (since flare start) |
| `FW_LND_THRTC_SC` | float | 1.0f | 0.2 ~ 1.0 |  | Altitude time constant factor for landing and low-height flight |
| `FW_LND_USETER` | int32 | 1 | 0 ~ 2 |  | Use terrain estimation during landing. |
| `FW_SPOILERS_LND` | float | 0.f | 0.0 ~ 1.0 | norm | Spoiler landing setting |

## FW General

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `FW_GPSF_LT` | int32 | 30 | 0 ~  | s | GPS failure loiter time |
| `FW_GPSF_R` | float | 15.0f | 0.0 ~ 60.0 | deg | GPS failure fixed roll angle |
| `FW_POS_STK_CONF` | int32 | 2 | 0 ~ 3 |  | Custom stick configuration |
| `FW_P_LIM_MAX` | float | 30.0f | 0.0 ~ 80.0 | deg | Maximum pitch angle setpoint |
| `FW_P_LIM_MIN` | float | -30.0f | -60.0 ~ 0.0 | deg | Minimum pitch angle setpoint |
| `FW_R_LIM` | float | 50.0f | 35.0 ~ 75.0 | deg | Maximum roll angle setpoint |
| `FW_THR_IDLE` | float | 0.0f | 0.0 ~ 1.0 | norm | Idle throttle |
| `FW_THR_MAX` | float | 1.0f | 0.0 ~ 1.0 | norm | Throttle limit max |
| `FW_THR_MIN` | float | 0.0f | 0.0 ~ 1.0 | norm | Throttle limit min |
| `FW_T_CLMB_R_SP` | float | 3.0f | 0.1 ~  | m/s | Default target climbrate. |
| `FW_T_SINK_R_SP` | float | 2.0f | 0.1 ~  | m/s | Default target sinkrate. |
| `FW_T_SPDWEIGHT` | float | 1.0f | 0.0 ~ 2.0 |  | Speed <--> Altitude weight |
| `FW_WING_HEIGHT` | float | 0.5 | 0.0 ~  | m | Height (AGL) of the wings when the aircraft is on the ground. |
| `FW_WING_SPAN` | float | 3.0 | 0.1 ~  | m | The aircraft's wing span (length from tip to tip). |

## ADSB

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `ADSB_CALLSIGN_1` | int32 | 0 |  |  | First 4 characters of CALLSIGN |
| `ADSB_CALLSIGN_2` | int32 | 0 |  |  | Second 4 characters of CALLSIGN |
| `ADSB_EMERGC` | int32 | 0 | 0 ~ 6 |  | ADSB-Out Emergency State |
| `ADSB_EMIT_TYPE` | int32 | 14 | 0 ~ 15 |  | ADSB-Out Vehicle Emitter Type |
| `ADSB_GPS_OFF_LAT` | int32 | 0 | 0 ~ 7 |  | ADSB-Out GPS Offset lat |
| `ADSB_GPS_OFF_LON` | int32 | 0 | 0 ~ 1 |  | ADSB-Out GPS Offset lon |
| `ADSB_ICAO_ID` | int32 | 1194684 | -1 ~ 16777215 |  | ADSB-Out ICAO configuration |
| `ADSB_ICAO_SPECL` | int32 | 0 | 0 ~ 16777215 |  | ADSB-In Special ICAO configuration |
| `ADSB_IDENT` | int32 | 0 |  |  | ADSB-Out Ident Configuration |
| `ADSB_LEN_WIDTH` | int32 | 1 | 0 ~ 15 |  | ADSB-Out Vehicle Size Configuration |
| `ADSB_LIST_MAX` | int32 | 25 | 0 ~ 50 |  | ADSB-In Vehicle List Size |
| `ADSB_MAX_SPEED` | int32 | 0 | 0 ~ 6 |  | ADSB-Out Vehicle Max Speed |
| `ADSB_SQUAWK` | int32 | 1200 | 0 ~ 7777 |  | ADSB-Out squawk code configuration |

## Autotune

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `FW_AT_APPLY` | int32 | 2 |  |  | Controls when to apply the new gains |
| `FW_AT_AXES` | int32 | 3 | 1 ~ 7 |  | Tuning axes selection |
| `FW_AT_MAN_AUX` | int32 | 0 | 0 ~ 6 |  | Enable/disable auto tuning using a manual control AUX input |
| `FW_AT_START` | int32 | 0 |  |  | Start the autotuning sequence |
| `FW_AT_SYSID_F0` | float | 1.f | 0.1 ~ 30.0 | Hz | Start frequency of the injected signal |
| `FW_AT_SYSID_F1` | float | 10.f | 0.1 ~ 30.0 | Hz | End frequency of the injected signal |
| `FW_AT_SYSID_TIME` | float | 10.f | 5 ~ 120 | s | Maneuver time for each axis |
| `FW_AT_SYSID_TYPE` | int32 | 1 |  |  | Input signal type |
| `MC_AT_APPLY` | int32 | 1 |  |  | Controls when to apply the new gains |
| `MC_AT_EN` | int32 | 0 |  |  | Multicopter autotune module enable |
| `MC_AT_RISE_TIME` | float | 0.14 | 0.01 ~ 0.5 | s | Desired angular rate closed-loop rise time |
| `MC_AT_START` | int32 | 0 |  |  | Start the autotuning sequence |
| `MC_AT_SYSID_AMP` | float | 0.7 | 0.1 ~ 6.0 |  | Amplitude of the injected signal |

## FW Performance

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `FW_AIRSPD_FLP_SC` | float | 1.f | 0.5 ~ 1 |  | Airspeed scale with full flaps |
| `FW_AIRSPD_MAX` | float | 20.0f | 0.5 ~  | m/s | Maximum Airspeed (CAS) |
| `FW_AIRSPD_MIN` | float | 10.0f | 0.5 ~  | m/s | Minimum Airspeed (CAS) |
| `FW_AIRSPD_STALL` | float | 7.0f | 0.5 ~  | m/s | Stall Airspeed (CAS) |
| `FW_AIRSPD_TRIM` | float | 15.0f | 0.5 ~  | m/s | Trim (Cruise) Airspeed |
| `FW_SERVICE_CEIL` | float | -1.0f | -1.0 ~  | m | Service ceiling |
| `FW_THR_ASPD_MAX` | float | 0.f | 0 ~ 1 |  | Throttle at max airspeed |
| `FW_THR_ASPD_MIN` | float | 0.f | 0 ~ 1 |  | Throttle at min airspeed |
| `FW_THR_TRIM` | float | 0.6f | 0.0 ~ 1.0 | norm | Trim throttle |
| `FW_T_CLMB_MAX` | float | 5.0f | 1.0 ~  | m/s | Maximum climb rate |
| `FW_T_SINK_MIN` | float | 2.0f | 1.0 ~  | m/s | Minimum descent rate |
| `WEIGHT_BASE` | float | -1.0f |  | kg | Vehicle base weight. |
| `WEIGHT_GROSS` | float | -1.0f |  | kg | Vehicle gross weight. |

## GPS

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `GPS_1_GNSS` | int32 | 0 | 0 ~ 63 |  | GNSS Systems for Primary GPS (integer bitmask) |
| `GPS_1_PROTOCOL` | int32 | 1 | 0 ~ 7 |  | Protocol for Main GPS |
| `GPS_2_GNSS` | int32 | 0 | 0 ~ 63 |  | GNSS Systems for Secondary GPS (integer bitmask) |
| `GPS_2_PROTOCOL` | int32 | 1 | 0 ~ 6 |  | Protocol for Secondary GPS |
| `GPS_CFG_WIPE` | int32 | 0 |  |  | Wipes the flash config of UBX modules. |
| `GPS_DUMP_COMM` | int32 | 0 | 0 ~ 2 |  | Log GPS communication data |
| `GPS_SAT_INFO` | int32 | 0 |  |  | Enable sat info (if available) |
| `GPS_UBX_BAUD2` | int32 | 230400 | 0 ~  | B/s | u-blox F9P UART2 Baudrate |
| `GPS_UBX_CFG_INTF` | int32 | 0 | 0 ~ 32 |  | u-blox protocol configuration for interfaces |
| `GPS_UBX_DYNMODEL` | int32 | 7 | 0 ~ 9 |  | u-blox GPS dynamic platform model |
| `GPS_UBX_MODE` | int32 | 0 | 0 ~ 1 |  | u-blox GPS Mode |
| `GPS_YAW_OFFSET` | float | 0.f | 0 ~ 360 | deg | Heading/Yaw offset for dual antenna GPS |
| `PPS_CAP_ENABLE` | int32 | 0 |  |  | PPS capture enable |

## Land Detector

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `LNDFW_AIRSPD_MAX` | float | 6.00f | 2 ~ 30 | m/s | Fixed-wing land detector: Max airspeed |
| `LNDFW_ROT_MAX` | float | 0.5f |  | deg/s | Fixed-wing land detector: max rotational speed |
| `LNDFW_TRIG_TIME` | float | 2.f | 0.1 ~  | s | Fixed-wing land detection trigger time |
| `LNDFW_VEL_XY_MAX` | float | 5.0f | 0.5 ~ 20 | m/s | Fixed-wing land detector: Max horizontal velocity threshold |
| `LNDFW_VEL_Z_MAX` | float | 1.0f | 0.1 ~ 20 | m/s | Fixed-wing land detector: Max vertiacal velocity threshold |
| `LNDFW_XYACC_MAX` | float | 8.0f | 2 ~ 30 | m/s^2 | Fixed-wing land detector: Max horizontal acceleration |
| `LNDMC_ALT_GND` | float | 2.f | -1 ~  | m | Ground effect altitude for multicopters |
| `LNDMC_ROT_MAX` | float | 20.0f |  | deg/s | Multicopter max rotational speed |
| `LNDMC_TRIG_TIME` | float | 1.0f | 0.1 ~ 10.0 | s | Multicopter land detection trigger time |
| `LNDMC_XY_VEL_MAX` | float | 1.5f |  | m/s | Multicopter max horizontal velocity |
| `LNDMC_Z_VEL_MAX` | float | 0.25f | 0 ~  | m/s | Multicopter vertical velocity threshold |
| `LND_FLIGHT_T_HI` | int32 | 0 | 0 ~  |  | Total flight time in microseconds |
| `LND_FLIGHT_T_LO` | int32 | 0 | 0 ~  |  | Total flight time in microseconds |

## Septentrio

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SEP_AUTO_CONFIG` | boolean | True |  |  | Toggle automatic receiver configuration |
| `SEP_CONST_USAGE` | bitmask | 0 | 0 ~ 63 |  | Usage of different constellations |
| `SEP_DUMP_COMM` | enum | 0 | 0 ~ 3 |  | Log GPS communication data |
| `SEP_HARDW_SETUP` | enum | 0 | 0 ~ 1 |  | Setup and expected use of the hardware |
| `SEP_LOG_FORCE` | boolean | False |  |  | Whether to overwrite or add to existing logging |
| `SEP_LOG_HZ` | enum | 0 | 0 ~ 10 |  | Logging frequency for the receiver |
| `SEP_LOG_LEVEL` | enum | 2 | 0 ~ 3 |  | Logging level for the receiver |
| `SEP_OUTP_HZ` | enum | 1 | 0 ~ 3 |  | Output frequency of main SBF blocks |
| `SEP_PITCH_OFFS` | float | 0 | -90 ~ 90 | deg | Pitch offset for dual antenna GPS |
| `SEP_SAT_INFO` | boolean | 0 |  |  | Enable sat info |
| `SEP_STREAM_LOG` | int32 | 2 | 1 ~ 10 |  | Logging stream used during automatic configuration |
| `SEP_STREAM_MAIN` | int32 | 1 | 1 ~ 10 |  | Main stream used during automatic configuration |
| `SEP_YAW_OFFS` | float | 0 | -360 ~ 360 | deg | Heading/Yaw offset for dual antenna GPS |

## Failure Detector

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `FD_ACT_EN` | int32 | 1 |  |  | Enable Actuator Failure check |
| `FD_ACT_MOT_C2T` | float | 2.0f | 0.0 ~ 50.0 | A/% | Motor Failure Current/Throttle Threshold |
| `FD_ACT_MOT_THR` | float | 0.2f | 0.0 ~ 1.0 | norm | Motor Failure Throttle Threshold |
| `FD_ACT_MOT_TOUT` | int32 | 100 | 10 ~ 10000 | ms | Motor Failure Time Threshold |
| `FD_ESCS_EN` | int32 | 1 |  |  | Enable checks on ESCs that report their arming state. |
| `FD_EXT_ATS_EN` | int32 | 0 |  |  | Enable PWM input on for engaging failsafe from an external automatic trigger system (ATS). |
| `FD_EXT_ATS_TRIG` | int32 | 1900 |  | us | The PWM threshold from external automatic trigger system for engaging failsafe. |
| `FD_FAIL_P` | int32 | 60 | 0 ~ 180 | deg | FailureDetector Max Pitch |
| `FD_FAIL_P_TTRI` | float | 0.3 | 0.02 ~ 5 | s | Pitch failure trigger time |
| `FD_FAIL_R` | int32 | 60 | 0 ~ 180 | deg | FailureDetector Max Roll |
| `FD_FAIL_R_TTRI` | float | 0.3 | 0.02 ~ 5 | s | Roll failure trigger time |
| `FD_IMB_PROP_THR` | int32 | 30 | 0 ~ 1000 |  | Imbalanced propeller check threshold |

## ICE

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `ICE_CHOKE_ST_DUR` | float | 5 | 0 ~ 10 | s | Duration of choking during startup |
| `ICE_EN` | boolean | False |  |  | Enable internal combustion engine |
| `ICE_IGN_DELAY` | float | 0 | 0 ~ 10 | s | Cold-start delay after ignition before engaging starter |
| `ICE_MIN_RUN_RPM` | float | 2000 | 0 ~ 10000 | rpm | Minimum RPM for engine to be declared running |
| `ICE_ON_SOURCE` | enum | 0 |  |  | Engine start/stop input source |
| `ICE_RUN_FAULT_D` | boolean | True |  |  | Fault detection if it stops in running state |
| `ICE_STOP_CHOKE` | boolean | True |  |  | Apply choke when stopping engine |
| `ICE_STRT_ATTEMPT` | int32 | 3 | 0 ~ 10 |  | Number attempts for starting the engine |
| `ICE_STRT_DUR` | float | 5 | 0 ~ 10 | s | Duration of single starting attempt (excl. choking) |
| `ICE_STRT_THR` | float | 0.1 | 0 ~ 1 | norm | Throttle value for starting engine |
| `ICE_THR_SLEW` | float | 0.5 | 0 ~ 1 | 1/s | Throttle slew rate |

## Landing Target Estimator

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `LTEST_ACC_UNC` | float | 10.0f | 0.01 ~  | (m/s^2)^2 | Acceleration uncertainty |
| `LTEST_MEAS_UNC` | float | 0.005f |  | tan(rad)^2 | Landing target measurement uncertainty |
| `LTEST_MODE` | int32 | 0 | 0 ~ 1 |  | Landing target mode |
| `LTEST_POS_UNC_IN` | float | 0.1f | 0.001 ~  | m^2 | Initial landing target position uncertainty |
| `LTEST_SCALE_X` | float | 1.0f | 0.01 ~  |  | Scale factor for sensor measurements in sensor x axis |
| `LTEST_SCALE_Y` | float | 1.0f | 0.01 ~  |  | Scale factor for sensor measurements in sensor y axis |
| `LTEST_SENS_POS_X` | float | 0.0f |  | m | X Position of IRLOCK in body frame (forward) |
| `LTEST_SENS_POS_Y` | float | 0.0f |  | m | Y Position of IRLOCK in body frame (right) |
| `LTEST_SENS_POS_Z` | float | 0.0f |  | m | Z Position of IRLOCK in body frame (downward) |
| `LTEST_SENS_ROT` | int32 | 2 | -1 ~ 40 |  | Rotation of IRLOCK sensor relative to airframe |
| `LTEST_VEL_UNC_IN` | float | 0.1f | 0.001 ~  | (m/s)^2 | Initial landing target velocity uncertainty |

## Attitude Q estimator

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `ATT_ACC_COMP` | int32 | 0 |  |  | Acceleration compensation based on GPS velocity. |
| `ATT_BIAS_MAX` | float | 0.05f | 0 ~ 2 | rad/s | Gyro bias limit |
| `ATT_EN` | int32 | 0 |  |  | standalone attitude estimator enable (unsupported) |
| `ATT_EXT_HDG_M` | int32 | 0 | 0 ~ 2 |  | External heading usage mode (from Motion capture/Vision) |
| `ATT_MAG_DECL` | float | 0.0f |  | deg | Magnetic declination, in degrees |
| `ATT_MAG_DECL_A` | int32 | 1 |  |  | Automatic GPS based declination compensation |
| `ATT_W_ACC` | float | 0.2f | 0 ~ 1 |  | Complimentary filter accelerometer weight |
| `ATT_W_EXT_HDG` | float | 0.1f | 0 ~ 1 |  | Complimentary filter external heading weight |
| `ATT_W_GYRO_BIAS` | float | 0.1f | 0 ~ 1 |  | Complimentary filter gyroscope bias weight |
| `ATT_W_MAG` | float | 0.1f | 0 ~ 1 |  | Complimentary filter magnetometer weight |

## Multicopter Position Slow Mode

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MC_SLOW_DEF_HVEL` | float | 3.f | 0.1 ~  | m/s | Default horizontal velocity limit |
| `MC_SLOW_DEF_VVEL` | float | 1.f | 0.1 ~  | m/s | Default vertical velocity limit |
| `MC_SLOW_DEF_YAWR` | float | 45.f | 1 ~  | deg/s | Default yaw rate limit |
| `MC_SLOW_MAP_HVEL` | int32 | 0 |  |  | Manual input mapped to scale horizontal velocity in position slow mode |
| `MC_SLOW_MAP_PTCH` | int32 | 0 |  |  | RC_MAP_AUX{N} to allow for gimbal pitch rate control in position slow mode |
| `MC_SLOW_MAP_VVEL` | int32 | 0 |  |  | Manual input mapped to scale vertical velocity in position slow mode |
| `MC_SLOW_MAP_YAWR` | int32 | 0 |  |  | Manual input mapped to scale yaw rate in position slow mode |
| `MC_SLOW_MIN_HVEL` | float | .3f | 0.1 ~  | m/s | Horizontal velocity lower limit |
| `MC_SLOW_MIN_VVEL` | float | .3f | 0.1 ~  | m/s | Vertical velocity lower limit |
| `MC_SLOW_MIN_YAWR` | float | 3.f | 1 ~  | deg/s | Yaw rate lower limit |

## Rover Rate Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RO_YAW_ACCEL_LIM` | float | -1.f | -1 ~ 10000 | deg/s^2 | Yaw acceleration limit |
| `RO_YAW_DECEL_LIM` | float | -1.f | -1 ~ 10000 | deg/s^2 | Yaw deceleration limit |
| `RO_YAW_EXPO` | float | 0.f | 0 ~ 1 |  | Yaw rate expo factor |
| `RO_YAW_RATE_CORR` | float | 1.f | 0.01 ~ 10000 |  | Yaw rate correction factor |
| `RO_YAW_RATE_I` | float | 0.f | 0 ~ 100 |  | Integral gain for closed loop yaw rate controller |
| `RO_YAW_RATE_LIM` | float | 0.f | 0 ~ 10000 | deg/s | Yaw rate limit |
| `RO_YAW_RATE_P` | float | 0.f | 0 ~ 100 |  | Proportional gain for closed loop yaw rate controller |
| `RO_YAW_RATE_TH` | float | 3.f | 0 ~ 100 | deg/s | Yaw rate measurement threshold |
| `RO_YAW_STICK_DZ` | float | 0.1f | 0 ~ 1 |  | Yaw stick deadzone |
| `RO_YAW_SUPEXPO` | float | 0.f | 0 ~ 0.95 |  | Yaw rate super expo factor |

## UUV Position Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `UUV_GAIN_X_D` | float | 0.2f |  |  | Gain of D controller X |
| `UUV_GAIN_X_P` | float | 1.0f |  |  | Gain of P controller X |
| `UUV_GAIN_Y_D` | float | 0.2f |  |  | Gain of D controller Y |
| `UUV_GAIN_Y_P` | float | 1.0f |  |  | Gain of P controller Y |
| `UUV_GAIN_Z_D` | float | 0.2f |  |  | Gain of D controller Z |
| `UUV_GAIN_Z_P` | float | 1.0f |  |  | Gain of P controller Z |
| `UUV_PGM_VEL` | float | 0.5f |  |  | Gain for position control velocity setpoint update |
| `UUV_POS_MODE` | int32 | 1 |  |  | Stabilization mode(1) or Position Control(0) |
| `UUV_POS_STICK_DB` | float | 0.1f |  |  | Deadband for changing position setpoint |
| `UUV_STAB_MODE` | int32 | 1 |  |  | Stabilization mode(1) or Position Control(0) |

## UXRCE-DDS Client

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `UXRCE_DDS_AG_IP` | int32 | 2130706433 |  |  | uXRCE-DDS Agent IP address |
| `UXRCE_DDS_DOM_ID` | int32 | 0 |  |  | uXRCE-DDS domain ID |
| `UXRCE_DDS_KEY` | int32 | 1 |  |  | uXRCE-DDS session key |
| `UXRCE_DDS_NS_IDX` | int32 | -1 | -1 ~ 9999 |  | Define an index-based message namespace |
| `UXRCE_DDS_PRT` | int32 | 8888 | 0 ~ 65535 |  | uXRCE-DDS UDP port |
| `UXRCE_DDS_PTCFG` | enum | 0 | 0 ~ 2 |  | uXRCE-DDS participant configuration |
| `UXRCE_DDS_RX_TO` | int32 | -1 |  | s | RX rate timeout configuration |
| `UXRCE_DDS_SYNCC` | boolean | 0 |  |  | Enable uXRCE-DDS system clock synchronization |
| `UXRCE_DDS_SYNCT` | boolean | 1 |  |  | Enable uXRCE-DDS timestamp synchronization |
| `UXRCE_DDS_TX_TO` | int32 | 3 |  | s | TX rate timeout configuration |

## Camera trigger

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `TRIG_ACT_TIME` | float | 40.0f | 0.1 ~ 3000 | ms | Camera trigger activation time |
| `TRIG_DISTANCE` | float | 25.0f | 0 ~  | m | Camera trigger distance |
| `TRIG_INTERFACE` | int32 | 4 |  |  | Camera trigger Interface |
| `TRIG_INTERVAL` | float | 40.0f | 4.0 ~ 10000.0 | ms | Camera trigger interval |
| `TRIG_MIN_INTERVA` | float | 1.0f | 1.0 ~ 10000.0 | ms | Minimum camera trigger interval |
| `TRIG_MODE` | int32 | 0 | 0 ~ 4 |  | Camera trigger mode |
| `TRIG_POLARITY` | int32 | 0 | 0 ~ 1 |  | Camera trigger polarity |
| `TRIG_PWM_NEUTRAL` | int32 | 1500 | 1000 ~ 2000 | us | PWM neutral output on trigger pin. |
| `TRIG_PWM_SHOOT` | int32 | 1900 | 1000 ~ 2000 | us | PWM output to trigger shot. |

## Multicopter Attitude Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MC_PITCHRATE_MAX` | float | 220.0f | 0.0 ~ 1800.0 | deg/s | Max pitch rate |
| `MC_PITCH_P` | float | 4.0f | 0.0 ~ 12 |  | Pitch P gain |
| `MC_ROLLRATE_MAX` | float | 220.0f | 0.0 ~ 1800.0 | deg/s | Max roll rate |
| `MC_ROLL_P` | float | 4.0f | 0.0 ~ 12 |  | Roll P gain |
| `MC_YAWRATE_MAX` | float | 200.0f | 0.0 ~ 1800.0 | deg/s | Max yaw rate |
| `MC_YAW_P` | float | 2.8f | 0.0 ~ 5 |  | Yaw P gain |
| `MC_YAW_WEIGHT` | float | 0.4f | 0.0 ~ 1.0 |  | Yaw weight |
| `MPC_YAWRAUTO_ACC` | float | 20.f | 5 ~ 360 | deg/s^2 | Maximum yaw acceleration in autonomous modes |
| `MPC_YAWRAUTO_MAX` | float | 60.f | 5 ~ 360 | deg/s | Maximum yaw rate in autonomous modes |

## Rover Velocity Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RO_ACCEL_LIM` | float | -1.f | -1 ~ 100 | m/s^2 | Acceleration limit |
| `RO_DECEL_LIM` | float | -1.f | -1 ~ 100 | m/s^2 | Deceleration limit |
| `RO_JERK_LIM` | float | -1.f | -1 ~ 100 | m/s^3 | Jerk limit |
| `RO_MAX_THR_SPEED` | float | 0.f | 0 ~ 100 | m/s | Speed the rover drives at maximum throttle |
| `RO_SPEED_I` | float | 0.f | 0 ~ 100 |  | Integral gain for ground speed controller |
| `RO_SPEED_LIM` | float | -1.f | -1 ~ 100 | m/s | Speed limit |
| `RO_SPEED_P` | float | 0.f | 0 ~ 100 |  | Proportional gain for ground speed controller |
| `RO_SPEED_RED` | float | -1.f | -1 ~ 100 |  | Tuning parameter for the speed reduction based on the course error |
| `RO_SPEED_TH` | float | 0.1f | 0 ~ 100 | m/s | Speed measurement threshold |

## Return Mode

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RTL_CONE_ANG` | int32 | 45 | 0 ~ 90 | deg | Half-angle of the return mode altitude cone |
| `RTL_DESCEND_ALT` | float | 30.f | 0 ~  | m | Return mode loiter altitude |
| `RTL_LAND_DELAY` | float | 0.0f | -1 ~  | s | Return mode delay |
| `RTL_LOITER_RAD` | float | 80.0f | 25 ~  | m | Loiter radius for rtl descend |
| `RTL_MIN_DIST` | float | 10.0f | 0.5 ~  | m | Horizontal radius from return point within which special rules for return mode apply. |
| `RTL_PLD_MD` | int32 | 0 |  |  | RTL precision land mode |
| `RTL_RETURN_ALT` | float | 60.f | 0 ~  | m | Return mode return altitude |
| `RTL_TYPE` | int32 | 0 |  |  | Return type |

## SD Logging

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SDLOG_BACKEND` | bitmask | 3 | 0 ~ 3 |  | Logging Backend (integer bitmask) |
| `SDLOG_BOOT_BAT` | boolean | 0 |  |  | Battery-only Logging |
| `SDLOG_DIRS_MAX` | int32 | 0 | 0 ~ 1000 |  | Maximum number of log directories to keep |
| `SDLOG_MISSION` | enum | 0 |  |  | Mission Log |
| `SDLOG_MODE` | enum | 0 |  |  | Logging Mode |
| `SDLOG_PROFILE` | bitmask | 1 | 0 ~ 4095 |  | Logging topic profile (integer bitmask) |
| `SDLOG_UTC_OFFSET` | int32 | 0 | -1000 ~ 1000 | min | UTC offset (unit: min) |
| `SDLOG_UUID` | boolean | 1 |  |  | Log UUID |

## FW Auto Takeoff

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `FW_FLAPS_TO_SCL` | float | 0.0f | 0.0 ~ 1.0 | norm | Flaps setting during take-off |
| `FW_LAUN_AC_T` | float | 0.05f | 0.0 ~ 5.0 | s | Trigger time |
| `FW_LAUN_AC_THLD` | float | 30.0f | 0 ~  | m/s^2 | Trigger acceleration threshold |
| `FW_LAUN_DETCN_ON` | int32 | 0 |  |  | Fixed-wing launch detection |
| `FW_LAUN_MOT_DEL` | float | 0.0f | 0.0 ~ 10.0 | s | Motor delay |
| `FW_TKO_AIRSPD` | float | -1.0f | -1.0 ~  | m/s | Takeoff Airspeed |
| `FW_TKO_PITCH_MIN` | float | 10.0f | -5.0 ~ 80.0 | deg | Minimum pitch during takeoff. |

## FW NPFG Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `NPFG_DAMPING` | float | 0.7f | 0.10 ~ 1.00 |  | NPFG damping ratio |
| `NPFG_LB_PERIOD` | int32 | 1 |  |  | Enable automatic lower bound on the NPFG period |
| `NPFG_PERIOD` | float | 10.0f | 1.0 ~ 100.0 | s | NPFG period |
| `NPFG_PERIOD_SF` | float | 1.5f | 1.0 ~ 10.0 |  | Period safety factor |
| `NPFG_ROLL_TC` | float | 0.5f | 0.00 ~ 2.00 | s | Roll time constant |
| `NPFG_SW_DST_MLT` | float | 0.32f | 0.1 ~ 1.0 |  | NPFG switch distance multiplier |
| `NPFG_UB_PERIOD` | int32 | 1 |  |  | Enable automatic upper bound on the NPFG period |

## Multicopter Acro Mode

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MC_ACRO_EXPO` | float | 0.f | 0 ~ 1 |  | Acro mode roll, pitch expo factor |
| `MC_ACRO_EXPO_Y` | float | 0.f | 0 ~ 1 |  | Acro mode yaw expo factor |
| `MC_ACRO_P_MAX` | float | 100.f | 0.0 ~ 1800.0 | deg/s | Acro mode maximum pitch rate |
| `MC_ACRO_R_MAX` | float | 100.f | 0.0 ~ 1800.0 | deg/s | Acro mode maximum roll rate |
| `MC_ACRO_SUPEXPO` | float | 0.f | 0 ~ 0.95 |  | Acro mode roll, pitch super expo factor |
| `MC_ACRO_SUPEXPOY` | float | 0.f | 0 ~ 0.95 |  | Acro mode yaw super expo factor |
| `MC_ACRO_Y_MAX` | float | 100.f | 0.0 ~ 1800.0 | deg/s | Acro mode maximum yaw rate |

## OSD

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `OSD_ATXXXX_CFG` | int32 | 0 |  |  | Enable/Disable the ATXXX OSD Chip |
| `OSD_CH_HEIGHT` | int32 | 0 | -8 ~ 8 |  | OSD Crosshairs Height |
| `OSD_DWELL_TIME` | int32 | 500 | 100 ~ 10000 |  | OSD Dwell Time (ms) |
| `OSD_LOG_LEVEL` | int32 | 3 |  |  | OSD Warning Level |
| `OSD_RC_STICK` | int32 | 1 | 0 ~ 1 |  | OSD RC Stick commands |
| `OSD_SCROLL_RATE` | int32 | 125 | 100 ~ 1000 |  | OSD Scroll Rate (ms) |
| `OSD_SYMBOLS` | bitmask | 16383 |  |  | OSD Symbol Selection |

## Runway Takeoff

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RWTO_MAX_THR` | float | 1.0 | 0.0 ~ 1.0 | norm | Throttle during runway takeoff. |
| `RWTO_NUDGE` | int32 | 1 |  |  | Enable use of yaw stick for nudging the wheel during runway ground roll |
| `RWTO_PSP` | float | 0.0 | -10.0 ~ 20.0 | deg | Pitch setpoint during taxi / before takeoff rotation airspeed is reached. |
| `RWTO_RAMP_TIME` | float | 2.0f | 1.0 ~ 15.0 | s | Throttle ramp up time for runway takeoff |
| `RWTO_ROT_AIRSPD` | float | -1.0f | -1.0 ~  | m/s | Takeoff rotation airspeed |
| `RWTO_ROT_TIME` | float | 1.0f | 0.1 ~  | s | Takeoff rotation time |
| `RWTO_TKOFF` | int32 | 0 |  |  | Runway takeoff with landing gear |

## Simulator

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SIM_AGP_FAIL` | int32 | 0 | 0 ~ 3 |  | AGP failure mode |
| `SIM_BARO_OFF_P` | float | 0.0f |  |  | simulated barometer pressure offset |
| `SIM_BARO_OFF_T` | float | 0.0f |  | celcius | simulated barometer temperature offset |
| `SIM_GPS_USED` | int32 | 10 | 0 ~ 50 |  | simulated GPS number of satellites used |
| `SIM_MAG_OFFSET_X` | float | 0.0f |  | gauss | simulated magnetometer X offset |
| `SIM_MAG_OFFSET_Y` | float | 0.0f |  | gauss | simulated magnetometer Y offset |
| `SIM_MAG_OFFSET_Z` | float | 0.0f |  | gauss | simulated magnetometer Z offset |

## Spacecraft Attitude Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SC_PITCHRATE_MAX` | float | 220.0f | 0.0 ~ 1800.0 | deg/s | Max pitch rate |
| `SC_PITCH_P` | float | 6.5f | 0.0 ~ 12 |  | Pitch P gain |
| `SC_ROLLRATE_MAX` | float | 220.0f | 0.0 ~ 1800.0 | deg/s | Max roll rate |
| `SC_ROLL_P` | float | 6.5f | 0.0 ~ 12 |  | Roll P gain |
| `SC_YAWRATE_MAX` | float | 200.0f | 0.0 ~ 1800.0 | deg/s | Max yaw rate |
| `SC_YAW_P` | float | 2.8f | 0.0 ~ 5 |  | Yaw P gain |
| `SC_YAW_WEIGHT` | float | 0.4f | 0.0 ~ 1.0 |  | Yaw weight |

## Circuit Breaker

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `CBRK_BUZZER` | int32 | 0 | 0 ~ 782097 |  | Circuit breaker for disabling buzzer |
| `CBRK_FLIGHTTERM` | int32 | 121212 | 0 ~ 121212 |  | Circuit breaker for flight termination |
| `CBRK_IO_SAFETY` | int32 | 22027 | 0 ~ 22027 |  | Circuit breaker for IO safety |
| `CBRK_SUPPLY_CHK` | int32 | 0 | 0 ~ 894281 |  | Circuit breaker for power supply check |
| `CBRK_USB_CHK` | int32 | 197848 | 0 ~ 197848 |  | Circuit breaker for USB link check |
| `CBRK_VTOLARMING` | int32 | 0 | 0 ~ 159753 |  | Circuit breaker for arming in fixed-wing mode check |

## DShot

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `DSHOT_3D_DEAD_H` | int32 | 1000 | 1000 ~ 1999 |  | DSHOT 3D deadband high |
| `DSHOT_3D_DEAD_L` | int32 | 1000 | 0 ~ 1000 |  | DSHOT 3D deadband low |
| `DSHOT_3D_ENABLE` | boolean | 0 |  |  | Allows for 3d mode when using DShot and suitable mixer |
| `DSHOT_BIDIR_EN` | boolean | 0 |  |  | Enable bidirectional DShot |
| `DSHOT_MIN` | float | 0.055 | 0 ~ 1 | norm | Minimum DShot Motor Output |
| `MOT_POLE_COUNT` | int32 | 14 |  |  | Number of magnetic poles of the motors |

## Follow target

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `FLW_TGT_ALT_M` | int32 | 0 |  |  | Altitude control mode |
| `FLW_TGT_DST` | float | 8.0f | 1.0 ~  | m | Distance to follow target from |
| `FLW_TGT_FA` | float | 180.0f | -180.0 ~ 180.0 |  | Follow Angle setting in degrees |
| `FLW_TGT_HT` | float | 8.0f | 8.0 ~  | m | Follow target height |
| `FLW_TGT_MAX_VEL` | float | 5.0f | 0.0 ~ 20.0 |  | Maximum tangential velocity setting for generating the follow orbit trajectory |
| `FLW_TGT_RS` | float | 0.1f | 0.0 ~ 1.0 |  | Responsiveness to target movement in Target Estimator |

## Hover Thrust Estimator

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `HTE_ACC_GATE` | float | 3.0 | 1.0 ~ 10.0 | SD | Gate size for acceleration fusion |
| `HTE_HT_ERR_INIT` | float | 0.1 | 0.0 ~ 1.0 | normalized_thrust | 1-sigma initial hover thrust uncertainty |
| `HTE_HT_NOISE` | float | 0.0036 | 0.0001 ~ 1.0 | normalized_thrust/s | Hover thrust process noise |
| `HTE_THR_RANGE` | float | 0.2 | 0.01 ~ 0.4 | normalized_thrust | Max deviation from MPC_THR_HOVER |
| `HTE_VXY_THR` | float | 10.0 | 1.0 ~ 20.0 | m/s | Horizontal velocity threshold for sensitivity reduction |
| `HTE_VZ_THR` | float | 2.0 | 1.0 ~ 10.0 | m/s | Vertical velocity threshold for sensitivity reduction |

## Precision Land

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `PLD_BTOUT` | float | 5.0f | 0.0 ~ 50 | s | Landing Target Timeout |
| `PLD_FAPPR_ALT` | float | 0.1f | 0.0 ~ 10 | m | Final approach altitude |
| `PLD_HACC_RAD` | float | 0.2f | 0.0 ~ 10 | m | Horizontal acceptance radius |
| `PLD_MAX_SRCH` | int32 | 3 | 0 ~ 100 |  | Maximum number of search attempts |
| `PLD_SRCH_ALT` | float | 10.0f | 0.0 ~ 100 | m | Search altitude |
| `PLD_SRCH_TOUT` | float | 10.0f | 0.0 ~ 100 | s | Search timeout |

## Simulation

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SIM_GZ_EN_ASPD` | int32 | 1 |  |  | Enable airspeed sensor in Gazebo bridge |
| `SIM_GZ_EN_BARO` | int32 | 1 |  |  | Enable barometer/air pressure sensor in Gazebo bridge |
| `SIM_GZ_EN_FLOW` | int32 | 1 |  |  | Enable optical flow sensor in Gazebo bridge |
| `SIM_GZ_EN_GPS` | int32 | 1 |  |  | Enable GPS/NavSat sensor in Gazebo bridge |
| `SIM_GZ_EN_LIDAR` | int32 | 1 |  |  | Enable laser/lidar sensors in Gazebo bridge |
| `SIM_GZ_EN_ODOM` | int32 | 1 |  |  | Enable odometry in Gazebo bridge |

## VOXL2 IO

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `VOXL2_IO_BAUD` | int32 | 921600 |  | bit/s | VOXL2_IO UART baud rate |
| `VOXL2_IO_CMAX` | int32 | 2000 | 0 ~ 2000 | us | VOXL2_IO Calibration Max PWM |
| `VOXL2_IO_CMIN` | int32 | 1050 | 0 ~ 2000 | us | VOXL2_IO Calibration Min PWM |
| `VOXL2_IO_DIS` | int32 | 1000 | 0 ~ 2000 | us | VOXL2_IO Disabled PWM |
| `VOXL2_IO_MAX` | int32 | 2000 | 0 ~ 2000 | us | VOXL2_IO Max PWM |
| `VOXL2_IO_MIN` | int32 | 1100 | 0 ~ 2000 | us | VOXL2_IO Min PWM |

## 未分組

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SCH16T_ACC_FILT` | int32 | 6 |  |  | Accel filter settings |
| `SCH16T_DECIM` | int32 | 4 |  |  | Gyro and Accel decimation settings |
| `SCH16T_GYRO_FILT` | int32 | 2 |  |  | Gyro filter settings |
| `SF1XX_MODE` | int32 | 1 | 0 ~ 2 |  | Lightware SF1xx/SF20/LW20 Operation Mode |
| `SPC_VEHICLE_RESP` | float | 0.5f |  |  |  |
| `ZENOH_DOMAIN_ID` | int32 | 0 | 0 ~ 232 |  | ROS2 RMW_ZENOH_CPP Domain id |

## Geofence

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `GF_ACTION` | int32 | 2 | 0 ~ 5 |  | Geofence violation action. |
| `GF_MAX_HOR_DIST` | float | 0.0f | 0 ~ 10000 | m | Max horizontal distance from Home |
| `GF_MAX_VER_DIST` | float | 0.0f | 0 ~ 10000 | m | Max vertical distance from Home |
| `GF_PREDICT` | int32 | 0 |  |  | [EXPERIMENTAL] Use Pre-emptive geofence triggering |
| `GF_SOURCE` | int32 | 0 | 0 ~ 1 |  | Geofence source |

## Neural Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MC_NN_EN` | int32 | 1 |  |  | If true the neural network control is automatically started on boot. |
| `MC_NN_MANL_CTRL` | int32 | 1 |  |  | Enable or disable setting the trajectory setpoint with manual control. |
| `MC_NN_MAX_RPM` | int32 | 22000 | 0 ~ 80000 |  | The maximum RPM of the motors. Used to normalize the output of the neural network. |
| `MC_NN_MIN_RPM` | int32 | 1000 | 0 ~ 80000 |  | The minimum RPM of the motors. Used to normalize the output of the neural network. |
| `MC_NN_THRST_COEF` | float | 1.2f | 0.0 ~ 5.0 |  | Thrust coefficient of the motors. Used to normalize the output of the neural network. Divided by 100 000 |

## Rover Ackermann

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RA_ACC_RAD_GAIN` | float | 1 | 1 ~ 100 |  | Tuning parameter for corner cutting |
| `RA_ACC_RAD_MAX` | float | -1 | -1 ~ 100 | m | Maximum acceptance radius for the waypoints |
| `RA_MAX_STR_ANG` | float | 0 | 0 ~ 1.5708 | rad | Maximum steering angle |
| `RA_STR_RATE_LIM` | float | -1 | -1 ~ 1000 | deg/s | Steering rate limit |
| `RA_WHEEL_BASE` | float | 0 | 0 ~ 100 | m | Wheel base |

## Actuator Outputs

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `PCA9685_DUTY_EN` | bitmask | 0 |  |  | Put the selected channels into Duty-Cycle output mode |
| `PCA9685_EN_BUS` | int32 | 0 | 0 ~ 10 |  | Enable the PCA9685 output driver |
| `PCA9685_PWM_FREQ` | float | 50.0 | 23.8 ~ 1525.87 |  | PWM cycle frequency |
| `PCA9685_SCHD_HZ` | float | 50.0 | 50.0 ~ 400.0 |  | PWM update rate |

## Rover Differential

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RD_TRANS_DRV_TRN` | float | 0.174533 | 0.001 ~ 3.14159 | rad | Yaw error threshhold to switch from driving to spot turning |
| `RD_TRANS_TRN_DRV` | float | 0.0872665 | 0.001 ~ 3.14159 | rad | Yaw error threshhold to switch from spot turning to driving |
| `RD_WHEEL_TRACK` | float | 0 | 0 ~ 100 | m | Wheel track |
| `RD_YAW_STK_GAIN` | float | 1 | 0.1 ~ 1 |  | Yaw stick gain for Manual mode |

## UWB

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `UWB_INIT_OFF_X` | float | 0.0 |  | m | UWB sensor X offset in body frame |
| `UWB_INIT_OFF_Y` | float | 0.0 |  | m | UWB sensor Y offset in body frame |
| `UWB_INIT_OFF_Z` | float | 0.0 |  | m | UWB sensor Z offset in body frame |
| `UWB_SENS_ROT` | enum | 0 |  |  | UWB sensor orientation |

## Camera Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `CAM_CAP_EDGE` | int32 | 0 |  |  | Camera capture edge |
| `CAM_CAP_FBACK` | int32 | 0 |  |  | Camera capture feedback |
| `CAM_CAP_MODE` | int32 | 0 |  |  | Camera capture timestamping mode |

## ESC

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `ESC_BL_VER` | int32 | 0 | 0 ~ 65535 |  | Required esc bootloader version. |
| `ESC_FW_VER` | int32 | 0 | 0 ~ 65535 |  | Required esc firmware version. |
| `ESC_HW_VER` | int32 | 0 | 0 ~ 65535 |  | Required esc hardware version |

## Iridium SBD

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `ISBD_READ_INT` | int32 | 0 | 0 ~ 5000 | s | Satellite radio read interval. Only required to be nonzero if data is not sent using a ring call. |
| `ISBD_SBD_TIMEOUT` | int32 | 60 | 0 ~ 300 | s | Iridium SBD session timeout |
| `ISBD_STACK_TIME` | int32 | 0 | 0 ~ 500 | ms | Time the Iridium driver will wait for additional mavlink messages to combine them into one SBD message |

## Magnetometer

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `BMM350_AVG` | enum | 1 |  |  | BMM350 data averaging |
| `BMM350_DRIVE` | int32 | 7 | 0 ~ 7 |  | BMM350 pad drive strength setting |
| `BMM350_ODR` | enum | 3 |  |  | BMM350 ODR rate |

## Manual Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MAN_ARM_GESTURE` | int32 | 1 |  |  | Enable arm/disarm stick gesture |
| `MAN_DEADZONE` | float | 0.1f | 0 ~ 1 |  | Deadzone for sticks (only specific use cases) |
| `MAN_KILL_GEST_T` | float | -1.f | -1 ~ 15 | s | Trigger time for kill stick gesture |

## Pure Pursuit

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `PP_LOOKAHD_GAIN` | float | 1.0f | 0.1 ~ 100 |  | Tuning parameter for the pure pursuit controller |
| `PP_LOOKAHD_MAX` | float | 10.0f | 0.1 ~ 100 | m | Maximum lookahead distance for the pure pursuit controller |
| `PP_LOOKAHD_MIN` | float | 1.0f | 0.1 ~ 100 | m | Minimum lookahead distance for the pure pursuit controller |

## Return To Land

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RTL_APPR_FORCE` | int32 | 0 |  |  | RTL force approach landing |
| `RTL_TIME_FACTOR` | float | 1.1f | 1.0 ~ 2.0 |  | RTL time estimate safety margin factor |
| `RTL_TIME_MARGIN` | int32 | 100 | 0 ~ 3600 | s | RTL time estimate safety margin offset |

## Rover Mecanum

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RM_COURSE_CTL_TH` | float | 0.17 | 0 ~ 3.14 | rad | Threshold to update course control in manual position mode |
| `RM_WHEEL_TRACK` | float | 0 | 0 ~ 100 | m | Wheel track |
| `RM_YAW_STK_GAIN` | float | 1 | 0.1 ~ 1 |  | Yaw stick gain for Manual mode |

## SITL

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SIM_BAT_DRAIN` | float | 60 | 1 ~ 86400 | s | Simulator Battery drain interval |
| `SIM_BAT_ENABLE` | int32 | 1 |  |  | Simulator Battery enabled |
| `SIM_BAT_MIN_PCT` | float | 50.0f | 0 ~ 100 | % | Simulator Battery minimal percentage. |

## Transponder

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MXS_EXT_CFG` | int32 | 0 |  |  | Sagetech External Configuration Mode |
| `MXS_OP_MODE` | int32 | 0 | 0 ~ 3 |  | Sagetech MXS mode configuration |
| `MXS_TARG_PORT` | int32 | 1 | 0 ~ 2 |  | Sagetech MXS Participant Configuration |

## CDCACM

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SYS_USB_AUTO` | int32 | 2 |  |  | Enable USB autostart |
| `USB_MAV_MODE` | int32 | 2 |  |  | Specify USB MAVLink mode |

## Events

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `EV_TSK_RC_LOSS` | int32 | 0 |  |  | RC Loss Alarm |
| `EV_TSK_STAT_DIS` | int32 | 0 |  |  | Status Display |

## Flight Task Orbit

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MC_ORBIT_RAD_MAX` | float | 1000.0f | 1.0 ~ 10000.0 | m | Maximum radius of orbit |
| `MC_ORBIT_YAW_MOD` | int32 | 0 |  |  | Yaw behaviour during orbit flight. |

## Magnetometer Bias Estimator

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MBE_ENABLE` | int32 | 1 |  |  | Enable online mag bias calibration |
| `MBE_LEARN_GAIN` | float | 18.f | 0.1 ~ 100 |  | Mag bias estimator learning gain |

## PWM Outputs

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `PWM_SBUS_MODE` | int32 | 0 |  |  | S.BUS out |
| `THR_MDL_FAC` | float | 0.0f | 0.0 ~ 1.0 |  | Thrust to motor control signal model parameter |

## Payload Deliverer

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `PD_GRIPPER_TO` | float | 1 | 0 ~  | s | Timeout for successful gripper actuation acknowledgement |
| `PD_GRIPPER_TYPE` | enum | 0 | -1 ~ 0 |  | Type of Gripper (Servo, etc.) |

## RC

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RC_CRSF_TEL_EN` | boolean | 0 |  |  | Crossfire RC telemetry enable |
| `RC_GHST_TEL_EN` | boolean | 0 |  |  | Ghost RC telemetry enable |

## Roboclaw Driver

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RBCLW_ADDRESS` | enum | 128 | 128 ~ 135 |  | Address of the ESC on the bus |
| `RBCLW_COUNTS_REV` | int32 | 1200 | 1 ~  |  | Number of encoder counts for one wheel revolution |

## Camera Capture

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `CAM_CAP_DELAY` | float | 0.0f | 0.0 ~ 100.0 | ms | Camera strobe delay |

## FW Lateral Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `FW_PN_R_SLEW_MAX` | float | 90.0f | 0 ~  | deg/s | Path navigation roll slew rate limit. |

## Mixer Output

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MC_AIRMODE` | int32 | 0 |  |  | Multicopter air-mode |

## ModalAI Custom Configuration

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `MODALAI_CONFIG` | int32 | 0 |  |  | Custom configuration for ModalAI drones |

## RC Input

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RC_INPUT_PROTO` | enum | -1 | -1 ~ 7 |  | RC input protocol |

## Rover Attitude Control

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `RO_YAW_P` | float | 0.f | 0 ~ 100 |  | Proportional gain for closed loop yaw controller |

## Serial

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `SER_MXS_BAUD` | int32 | 5 | 0 ~ 10 |  | MXS Serial Communication Baud rate |

## Telemetry

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `TEL_BST_EN` | int32 | 0 |  |  | Blacksheep telemetry Enable |

## VTOL Takeoff

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `VTO_LOITER_ALT` | float | 80 | 20 ~ 300 | m | VTOL Takeoff relative loiter altitude. |

## Zenoh

| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |
|---|---|---|---|---|---|
| `ZENOH_ENABLE` | boolean | 0 |  |  | Enable Zenoh |

---

→ 回 [附錄索引](README.md)
