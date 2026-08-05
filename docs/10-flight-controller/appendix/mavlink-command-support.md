# PX4 的 MAVLink 介面 — v1.17.0

> 這份是**產生出來的**,不是手寫的。內容直接解析 PX4 `v1.17.0` 的原始碼,產生器與重跑指令在 [`tools/dump_px4_api.py`](../../../tools/dump_px4_api.py)。換版本重跑,不要手改這個檔。

## 出處

| 項目 | 出處 |
|---|---|
| 原始碼 | <https://github.com/PX4/PX4-Autopilot/tree/v1.17.0>,tarball 為 `archive/refs/tags/v1.17.0.tar.gz` |
| 解析範圍 | `src/modules/mavlink/streams/*.hpp`(發送)與 `mavlink_receiver.cpp` 的 `switch (msg->msgid)`(接收),共 89 個發送串流、51 種接收訊息 |
| 官方參考 | <https://docs.px4.io/>(預設顯示 main 分支,與此處的 `v1.17.0` 可能不同) |

## 這兩張表回答的是不同問題

**發送串流**是 PX4 有能力送出的訊息。實際會不會送、以什麼頻率送,由訊息串流設定與鏈路頻寬決定——[頻寬預算那節](../../20-protocols/02-routing-and-bandwidth.md)算過,57600 bps 的鏈路塞不下全部。

**接收訊息**是 PX4 會處理的入站訊息。**不在這張表裡的訊息會被安靜丟棄**,這是「送出去但沒反應」最常見的原因,而且不會有錯誤訊息。

---

## 發送串流(89)

| 訊息 | 實作檔 |
|---|---|
| `ACTUATOR_OUTPUT_STATUS` | `streams/ACTUATOR_OUTPUT_STATUS.hpp` |
| `ADSB_VEHICLE` | `streams/ADSB_VEHICLE.hpp` |
| `ALTITUDE` | `streams/ALTITUDE.hpp` |
| `ATTITUDE` | `streams/ATTITUDE.hpp` |
| `ATTITUDE_QUATERNION` | `streams/ATTITUDE_QUATERNION.hpp` |
| `ATTITUDE_TARGET` | `streams/ATTITUDE_TARGET.hpp` |
| `AUTOPILOT_STATE_FOR_GIMBAL_DEVICE` | `streams/AUTOPILOT_STATE_FOR_GIMBAL_DEVICE.hpp` |
| `AUTOPILOT_VERSION` | `streams/AUTOPILOT_VERSION.hpp` |
| `AVAILABLE_MODES` | `streams/AVAILABLE_MODES.hpp` |
| `BATTERY_INFO` | `streams/BATTERY_INFO.hpp` |
| `BATTERY_STATUS` | `streams/BATTERY_STATUS.hpp` |
| `CAMERA_IMAGE_CAPTURED` | `streams/CAMERA_IMAGE_CAPTURED.hpp` |
| `CAMERA_TRIGGER` | `streams/CAMERA_TRIGGER.hpp` |
| `COMMAND_LONG` | `streams/COMMAND_LONG.hpp` |
| `COMPONENT_INFORMATION` | `streams/COMPONENT_INFORMATION.hpp` |
| `COMPONENT_METADATA` | `streams/COMPONENT_METADATA.hpp` |
| `CURRENT_MODE` | `streams/CURRENT_MODE.hpp` |
| `DEBUG` | `streams/DEBUG.hpp` |
| `DEBUG_FLOAT_ARRAY` | `streams/DEBUG_FLOAT_ARRAY.hpp` |
| `DEBUG_VECT` | `streams/DEBUG_VECT.hpp` |
| `DISTANCE_SENSOR` | `streams/DISTANCE_SENSOR.hpp` |
| `EFI_STATUS` | `streams/EFI_STATUS.hpp` |
| `ESC_INFO` | `streams/ESC_INFO.hpp` |
| `ESC_STATUS` | `streams/ESC_STATUS.hpp` |
| `ESTIMATOR_STATUS` | `streams/ESTIMATOR_STATUS.hpp` |
| `EXTENDED_SYS_STATE` | `streams/EXTENDED_SYS_STATE.hpp` |
| `FIGURE_EIGHT_EXECUTION_STATUS` | `streams/FIGURE_EIGHT_EXECUTION_STATUS.hpp` |
| `FLIGHT_INFORMATION` | `streams/FLIGHT_INFORMATION.hpp` |
| `FUEL_STATUS` | `streams/FUEL_STATUS.hpp` |
| `GIMBAL_DEVICE_ATTITUDE_STATUS` | `streams/GIMBAL_DEVICE_ATTITUDE_STATUS.hpp` |
| `GIMBAL_DEVICE_INFORMATION` | `streams/GIMBAL_DEVICE_INFORMATION.hpp` |
| `GIMBAL_DEVICE_SET_ATTITUDE` | `streams/GIMBAL_DEVICE_SET_ATTITUDE.hpp` |
| `GIMBAL_MANAGER_INFORMATION` | `streams/GIMBAL_MANAGER_INFORMATION.hpp` |
| `GIMBAL_MANAGER_STATUS` | `streams/GIMBAL_MANAGER_STATUS.hpp` |
| `GLOBAL_POSITION` | `streams/GLOBAL_POSITION.hpp` |
| `GLOBAL_POSITION_INT` | `streams/GLOBAL_POSITION_INT.hpp` |
| `GNSS_INTEGRITY` | `streams/GNSS_INTEGRITY.hpp` |
| `GPS2_RAW` | `streams/GPS2_RAW.hpp` |
| `GPS_GLOBAL_ORIGIN` | `streams/GPS_GLOBAL_ORIGIN.hpp` |
| `GPS_RAW_INT` | `streams/GPS_RAW_INT.hpp` |
| `GPS_RTCM_DATA` | `streams/GPS_RTCM_DATA.hpp` |
| `GPS_STATUS` | `streams/GPS_STATUS.hpp` |
| `HEARTBEAT` | `streams/HEARTBEAT.hpp` |
| `HIGHRES_IMU` | `streams/HIGHRES_IMU.hpp` |
| `HIGH_LATENCY2` | `streams/HIGH_LATENCY2.hpp` |
| `HIL_ACTUATOR_CONTROLS` | `streams/HIL_ACTUATOR_CONTROLS.hpp` |
| `HIL_STATE_QUATERNION` | `streams/HIL_STATE_QUATERNION.hpp` |
| `HOME_POSITION` | `streams/HOME_POSITION.hpp` |
| `HYGROMETER_SENSOR` | `streams/HYGROMETER_SENSOR.hpp` |
| `LANDING_TARGET` | `streams/LANDING_TARGET.hpp` |
| `LINK_NODE_STATUS` | `streams/LINK_NODE_STATUS.hpp` |
| `LOCAL_POSITION_NED` | `streams/LOCAL_POSITION_NED.hpp` |
| `MAG_CAL_REPORT` | `streams/MAG_CAL_REPORT.hpp` |
| `MANUAL_CONTROL` | `streams/MANUAL_CONTROL.hpp` |
| `MOUNT_ORIENTATION` | `streams/MOUNT_ORIENTATION.hpp` |
| `NAMED_VALUE_FLOAT` | `streams/NAMED_VALUE_FLOAT.hpp` |
| `NAV_CONTROLLER_OUTPUT` | `streams/NAV_CONTROLLER_OUTPUT.hpp` |
| `OBSTACLE_DISTANCE` | `streams/OBSTACLE_DISTANCE.hpp` |
| `ODOMETRY` | `streams/ODOMETRY.hpp` |
| `OPEN_DRONE_ID_ARM_STATUS` | `streams/OPEN_DRONE_ID_ARM_STATUS.hpp` |
| `OPEN_DRONE_ID_BASIC_ID` | `streams/OPEN_DRONE_ID_BASIC_ID.hpp` |
| `OPEN_DRONE_ID_LOCATION` | `streams/OPEN_DRONE_ID_LOCATION.hpp` |
| `OPEN_DRONE_ID_SYSTEM` | `streams/OPEN_DRONE_ID_SYSTEM.hpp` |
| `OPTICAL_FLOW_RAD` | `streams/OPTICAL_FLOW_RAD.hpp` |
| `ORBIT_EXECUTION_STATUS` | `streams/ORBIT_EXECUTION_STATUS.hpp` |
| `PING` | `streams/PING.hpp` |
| `POSITION_TARGET_GLOBAL_INT` | `streams/POSITION_TARGET_GLOBAL_INT.hpp` |
| `POSITION_TARGET_LOCAL_NED` | `streams/POSITION_TARGET_LOCAL_NED.hpp` |
| `PROTOCOL_VERSION` | `streams/PROTOCOL_VERSION.hpp` |
| `RAW_RPM` | `streams/RAW_RPM.hpp` |
| `RC_CHANNELS` | `streams/RC_CHANNELS.hpp` |
| `SCALED_IMU` | `streams/SCALED_IMU.hpp` |
| `SCALED_IMU2` | `streams/SCALED_IMU2.hpp` |
| `SCALED_IMU3` | `streams/SCALED_IMU3.hpp` |
| `SCALED_PRESSURE` | `streams/SCALED_PRESSURE.hpp` |
| `SCALED_PRESSURE2` | `streams/SCALED_PRESSURE2.hpp` |
| `SCALED_PRESSURE3` | `streams/SCALED_PRESSURE3.hpp` |
| `STATUSTEXT` | `streams/STATUSTEXT.hpp` |
| `STORAGE_INFORMATION` | `streams/STORAGE_INFORMATION.hpp` |
| `SYSTEM_TIME` | `streams/SYSTEM_TIME.hpp` |
| `SYS_STATUS` | `streams/SYS_STATUS.hpp` |
| `TIMESYNC` | `streams/TIMESYNC.hpp` |
| `TIME_ESTIMATE_TO_TARGET` | `streams/TIME_ESTIMATE_TO_TARGET.hpp` |
| `UAVIONIX_ADSB_OUT_CFG` | `streams/UAVIONIX_ADSB_OUT_CFG.hpp` |
| `UAVIONIX_ADSB_OUT_DYNAMIC` | `streams/UAVIONIX_ADSB_OUT_DYNAMIC.hpp` |
| `UTM_GLOBAL_POSITION` | `streams/UTM_GLOBAL_POSITION.hpp` |
| `VFR_HUD` | `streams/VFR_HUD.hpp` |
| `VIBRATION` | `streams/VIBRATION.hpp` |
| `WIND_COV` | `streams/WIND_COV.hpp` |

## 會處理的入站訊息(51)

| 訊息 |
|---|
| `ADSB_VEHICLE` |
| `ATT_POS_MOCAP` |
| `BATTERY_STATUS` |
| `CELLULAR_STATUS` |
| `COMMAND_ACK` |
| `COMMAND_INT` |
| `COMMAND_LONG` |
| `DEBUG` |
| `DEBUG_FLOAT_ARRAY` |
| `DEBUG_VECT` |
| `DISTANCE_SENSOR` |
| `FOLLOW_TARGET` |
| `GENERATOR_STATUS` |
| `GIMBAL_DEVICE_ATTITUDE_STATUS` |
| `GIMBAL_DEVICE_INFORMATION` |
| `GIMBAL_MANAGER_SET_ATTITUDE` |
| `GIMBAL_MANAGER_SET_MANUAL_CONTROL` |
| `GPS_RTCM_DATA` |
| `HEARTBEAT` |
| `HIL_GPS` |
| `HIL_OPTICAL_FLOW` |
| `HIL_SENSOR` |
| `HIL_STATE_QUATERNION` |
| `LANDING_TARGET` |
| `LOGGING_ACK` |
| `MANUAL_CONTROL` |
| `NAMED_VALUE_FLOAT` |
| `NAMED_VALUE_INT` |
| `OBSTACLE_DISTANCE` |
| `ODOMETRY` |
| `ONBOARD_COMPUTER_STATUS` |
| `OPEN_DRONE_ID_OPERATOR_ID` |
| `OPEN_DRONE_ID_SELF_ID` |
| `OPEN_DRONE_ID_SYSTEM` |
| `OPTICAL_FLOW_RAD` |
| `PING` |
| `PLAY_TUNE` |
| `PLAY_TUNE_V2` |
| `RADIO_STATUS` |
| `RC_CHANNELS_OVERRIDE` |
| `REQUEST_EVENT` |
| `SERIAL_CONTROL` |
| `SET_ATTITUDE_TARGET` |
| `SET_GPS_GLOBAL_ORIGIN` |
| `SET_MODE` |
| `SET_POSITION_TARGET_GLOBAL_INT` |
| `SET_POSITION_TARGET_LOCAL_NED` |
| `SET_VELOCITY_LIMITS` |
| `STATUSTEXT` |
| `TUNNEL` |
| `VISION_POSITION_ESTIMATE` |

---

→ 回 [附錄索引](README.md)
