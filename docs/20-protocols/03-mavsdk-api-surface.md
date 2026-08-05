# MAVSDK-Python 3.17.2 介面全貌

這份是**產生出來的**,不是手寫的。內容直接來自安裝好的 `mavsdk==3.17.2` 套件,用 `inspect` 讀出來,所以不會有「文件寫的跟套件裡的不一樣」這種問題。

重跑的指令與理由寫在 [`reference-impl/mission-controller/scripts/dump_mavsdk_api.py`](../../reference-impl/mission-controller/scripts/dump_mavsdk_api.py)。換版本就重跑一次,不要手改這個檔。

共 38 個 plugin、359 個方法,其中 100 個是訂閱式串流。

## 出處

| 項目 | 出處 |
|---|---|
| 本文所有簽章與型別 | 安裝於容器內的 `mavsdk==3.17.2`,以 `inspect.signature` / `inspect.getmembers` 讀出 |
| 套件 | <https://pypi.org/project/mavsdk/3.17.2/> |
| 原始碼 | <https://github.com/mavlink/MAVSDK-Python> |
| 底層 C++ 實作 | <https://github.com/mavlink/MAVSDK> |

MAVSDK-Python 沒有官方的方法級 API 參考,這也是這份文件存在的理由。上游若補了官方參考,以官方為準。

## 怎麼讀

- **呼叫**(`await drone.action.arm()`):一次性動作或查詢,回傳單一結果。
- **串流**(`async for p in drone.telemetry.position():`):訂閱式,會一直吐值直到取消。**這是最常踩的地方**——把串流當呼叫 `await`,程式會停在那裡等一個永遠不會結束的東西。
- `*_server` 結尾的 plugin 是**被控端**用的:自己扮演飛控或相機、回應地面站。做模擬器、假飛控或酬載元件時才會用到。
- 失敗以例外拋出,錯誤碼列在每個 plugin 的 Result 清單。

## Plugin 一覽

| Plugin | 類別 | 呼叫 | 串流 | 用途 |
|---|---|---|---|---|
| [`action`](#action) | `Action` | 23 | 0 | 控制端 |
| [`action_server`](#action-server) | `ActionServer` | 8 | 7 | 被控端 |
| [`arm_authorizer_server`](#arm-authorizer-server) | `ArmAuthorizerServer` | 2 | 1 | 被控端 |
| [`calibration`](#calibration) | `Calibration` | 1 | 5 | 控制端 |
| [`camera`](#camera) | `Camera` | 29 | 7 | 控制端 |
| [`camera_server`](#camera-server) | `CameraServer` | 22 | 17 | 被控端 |
| [`component_metadata`](#component-metadata) | `ComponentMetadata` | 3 | 1 | 控制端 |
| [`component_metadata_server`](#component-metadata-server) | `ComponentMetadataServer` | 1 | 0 | 被控端 |
| [`core`](#core) | `Core` | 1 | 1 | 控制端 |
| [`events`](#events) | `Events` | 1 | 2 | 控制端 |
| [`failure`](#failure) | `Failure` | 1 | 0 | 控制端 |
| [`follow_me`](#follow-me) | `FollowMe` | 7 | 0 | 控制端 |
| [`ftp`](#ftp) | `Ftp` | 7 | 2 | 控制端 |
| [`ftp_server`](#ftp-server) | `FtpServer` | 1 | 0 | 被控端 |
| [`geofence`](#geofence) | `Geofence` | 3 | 0 | 控制端 |
| [`gimbal`](#gimbal) | `Gimbal` | 7 | 3 | 控制端 |
| [`gripper`](#gripper) | `Gripper` | 2 | 0 | 控制端 |
| [`info`](#info) | `Info` | 5 | 1 | 控制端 |
| [`log_files`](#log-files) | `LogFiles` | 2 | 1 | 控制端 |
| [`log_streaming`](#log-streaming) | `LogStreaming` | 2 | 1 | 控制端 |
| [`manual_control`](#manual-control) | `ManualControl` | 3 | 0 | 控制端 |
| [`mavlink_direct`](#mavlink-direct) | `MavlinkDirect` | 2 | 1 | 控制端 |
| [`mission`](#mission) | `Mission` | 11 | 3 | 控制端 |
| [`mission_raw`](#mission-raw) | `MissionRaw` | 17 | 2 | 控制端 |
| [`mission_raw_server`](#mission-raw-server) | `MissionRawServer` | 1 | 3 | 被控端 |
| [`mocap`](#mocap) | `Mocap` | 4 | 0 | 控制端 |
| [`offboard`](#offboard) | `Offboard` | 13 | 0 | 控制端 |
| [`param`](#param) | `Param` | 8 | 0 | 控制端 |
| [`param_server`](#param-server) | `ParamServer` | 8 | 3 | 被控端 |
| [`rtk`](#rtk) | `Rtk` | 1 | 0 | 控制端 |
| [`server_utility`](#server-utility) | `ServerUtility` | 1 | 0 | 被控端 |
| [`shell`](#shell) | `Shell` | 1 | 1 | 控制端 |
| [`telemetry`](#telemetry) | `Telemetry` | 26 | 33 | 控制端 |
| [`telemetry_server`](#telemetry-server) | `TelemetryServer` | 17 | 0 | 被控端 |
| [`tracking_server`](#tracking-server) | `TrackingServer` | 6 | 3 | 被控端 |
| [`transponder`](#transponder) | `Transponder` | 1 | 1 | 控制端 |
| [`tune`](#tune) | `Tune` | 1 | 0 | 控制端 |
| [`winch`](#winch) | `Winch` | 10 | 1 | 控制端 |

---

## action

類別 `mavsdk.action.Action`,存取路徑 `drone.action`。

| 方法 | 型態 |
|---|---|
| `arm()` | 呼叫 |
| `arm_force()` | 呼叫 |
| `disarm()` | 呼叫 |
| `do_orbit(radius_m, velocity_ms, yaw_behavior, latitude_deg, longitude_deg, absolute_altitude_m)` | 呼叫 |
| `get_return_to_launch_altitude()` | 呼叫 |
| `get_takeoff_altitude()` | 呼叫 |
| `goto_location(latitude_deg, longitude_deg, absolute_altitude_m, yaw_deg)` | 呼叫 |
| `hold()` | 呼叫 |
| `kill()` | 呼叫 |
| `land()` | 呼叫 |
| `reboot()` | 呼叫 |
| `return_to_launch()` | 呼叫 |
| `set_actuator(index, value)` | 呼叫 |
| `set_current_speed(speed_m_s)` | 呼叫 |
| `set_gps_global_origin(latitude_deg, longitude_deg, absolute_altitude_m)` | 呼叫 |
| `set_relay(index, setting)` | 呼叫 |
| `set_return_to_launch_altitude(relative_altitude_m)` | 呼叫 |
| `set_takeoff_altitude(altitude)` | 呼叫 |
| `shutdown()` | 呼叫 |
| `takeoff()` | 呼叫 |
| `terminate()` | 呼叫 |
| `transition_to_fixedwing()` | 呼叫 |
| `transition_to_multicopter()` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`BUSY`、`COMMAND_DENIED`、`COMMAND_DENIED_LANDED_STATE_UNKNOWN`、`COMMAND_DENIED_NOT_LANDED`、`TIMEOUT`、`VTOL_TRANSITION_SUPPORT_UNKNOWN`、`NO_VTOL_TRANSITION_SUPPORT`、`PARAMETER_ERROR`、`UNSUPPORTED`、`FAILED`、`INVALID_ARGUMENT`

| 型別 | 內容 |
|---|---|
| `ActionError` | 欄位 `(result, origin, *params)` |
| `OrbitYawBehavior` | 列舉:`HOLD_FRONT_TO_CIRCLE_CENTER`、`HOLD_INITIAL_HEADING`、`UNCONTROLLED`、`HOLD_FRONT_TANGENT_TO_CIRCLE`、`RC_CONTROLLED` |
| `RelayCommand` | 列舉:`ON`、`OFF` |

## action_server

類別 `mavsdk.action_server.ActionServer`,存取路徑 `drone.action_server`。

| 方法 | 型態 |
|---|---|
| `get_allowable_flight_modes()` | 呼叫 |
| `set_allow_takeoff(allow_takeoff)` | 呼叫 |
| `set_allowable_flight_modes(flight_modes)` | 呼叫 |
| `set_armable(armable, force_armable)` | 呼叫 |
| `set_armed_state(is_armed)` | 呼叫 |
| `set_disarmable(disarmable, force_disarmable)` | 呼叫 |
| `set_flight_mode(flight_mode)` | 呼叫 |
| `set_flight_mode_internal(flight_mode)` | 呼叫 |
| `arm_disarm()` | 串流 |
| `flight_mode_change()` | 串流 |
| `land()` | 串流 |
| `reboot()` | 串流 |
| `shutdown()` | 串流 |
| `takeoff()` | 串流 |
| `terminate()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`BUSY`、`COMMAND_DENIED`、`COMMAND_DENIED_LANDED_STATE_UNKNOWN`、`COMMAND_DENIED_NOT_LANDED`、`TIMEOUT`、`VTOL_TRANSITION_SUPPORT_UNKNOWN`、`NO_VTOL_TRANSITION_SUPPORT`、`PARAMETER_ERROR`、`NEXT`

| 型別 | 內容 |
|---|---|
| `ActionServerError` | 欄位 `(result, origin, *params)` |
| `AllowableFlightModes` | 欄位 `(can_auto_mode, can_guided_mode, can_stabilize_mode, can_auto_rtl_mode, can_auto_takeoff_mode, can_auto_land_mode, can_auto_loiter_mode)` |
| `ArmDisarm` | 欄位 `(arm, force)` |
| `FlightMode` | 列舉:`UNKNOWN`、`READY`、`TAKEOFF`、`HOLD`、`MISSION`、`RETURN_TO_LAUNCH`、`LAND`、`OFFBOARD`、`FOLLOW_ME`、`MANUAL`、`ALTCTL`、`POSCTL`、`ACRO`、`STABILIZED` |

## arm_authorizer_server

類別 `mavsdk.arm_authorizer_server.ArmAuthorizerServer`,存取路徑 `drone.arm_authorizer_server`。

| 方法 | 型態 |
|---|---|
| `accept_arm_authorization(valid_time_s)` | 呼叫 |
| `reject_arm_authorization(temporarily, reason, extra_info)` | 呼叫 |
| `arm_authorization()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`FAILED`

| 型別 | 內容 |
|---|---|
| `ArmAuthorizerServerError` | 欄位 `(result, origin, *params)` |
| `RejectionReason` | 列舉:`GENERIC`、`NONE`、`INVALID_WAYPOINT`、`TIMEOUT`、`AIRSPACE_IN_USE`、`BAD_WEATHER` |

## calibration

類別 `mavsdk.calibration.Calibration`,存取路徑 `drone.calibration`。

| 方法 | 型態 |
|---|---|
| `cancel()` | 呼叫 |
| `calibrate_accelerometer()` | 串流 |
| `calibrate_gimbal_accelerometer()` | 串流 |
| `calibrate_gyro()` | 串流 |
| `calibrate_level_horizon()` | 串流 |
| `calibrate_magnetometer()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NEXT`、`FAILED`、`NO_SYSTEM`、`CONNECTION_ERROR`、`BUSY`、`COMMAND_DENIED`、`TIMEOUT`、`CANCELLED`、`FAILED_ARMED`、`UNSUPPORTED`

| 型別 | 內容 |
|---|---|
| `CalibrationError` | 欄位 `(result, origin, *params)` |
| `ProgressData` | 欄位 `(has_progress, progress, has_status_text, status_text)` |

## camera

類別 `mavsdk.camera.Camera`,存取路徑 `drone.camera`。

| 方法 | 型態 |
|---|---|
| `focus_in_start(component_id)` | 呼叫 |
| `focus_out_start(component_id)` | 呼叫 |
| `focus_range(component_id, range)` | 呼叫 |
| `focus_stop(component_id)` | 呼叫 |
| `format_storage(component_id, storage_id)` | 呼叫 |
| `get_current_settings(component_id)` | 呼叫 |
| `get_mode(component_id)` | 呼叫 |
| `get_possible_setting_options(component_id)` | 呼叫 |
| `get_setting(component_id, setting)` | 呼叫 |
| `get_storage(component_id)` | 呼叫 |
| `get_video_stream_info(component_id)` | 呼叫 |
| `list_photos(component_id, photos_range)` | 呼叫 |
| `reset_settings(component_id)` | 呼叫 |
| `set_mode(component_id, mode)` | 呼叫 |
| `set_setting(component_id, setting)` | 呼叫 |
| `start_photo_interval(component_id, interval_s)` | 呼叫 |
| `start_video(component_id)` | 呼叫 |
| `start_video_streaming(component_id, stream_id)` | 呼叫 |
| `stop_photo_interval(component_id)` | 呼叫 |
| `stop_video(component_id)` | 呼叫 |
| `stop_video_streaming(component_id, stream_id)` | 呼叫 |
| `take_photo(component_id)` | 呼叫 |
| `track_point(component_id, point_x, point_y, radius)` | 呼叫 |
| `track_rectangle(component_id, top_left_x, top_left_y, bottom_right_x, bottom_right_y)` | 呼叫 |
| `track_stop(component_id)` | 呼叫 |
| `zoom_in_start(component_id)` | 呼叫 |
| `zoom_out_start(component_id)` | 呼叫 |
| `zoom_range(component_id, range)` | 呼叫 |
| `zoom_stop(component_id)` | 呼叫 |
| `camera_list()` | 串流 |
| `capture_info()` | 串流 |
| `current_settings()` | 串流 |
| `mode()` | 串流 |
| `possible_setting_options()` | 串流 |
| `storage()` | 串流 |
| `video_stream_info()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`IN_PROGRESS`、`BUSY`、`DENIED`、`ERROR`、`TIMEOUT`、`WRONG_ARGUMENT`、`NO_SYSTEM`、`PROTOCOL_UNSUPPORTED`、`UNAVAILABLE`、`CAMERA_ID_INVALID`、`ACTION_UNSUPPORTED`

| 型別 | 內容 |
|---|---|
| `CameraError` | 欄位 `(result, origin, *params)` |
| `CameraList` | 欄位 `(cameras)` |
| `CaptureInfo` | 欄位 `(component_id, position, attitude_quaternion, attitude_euler_angle, time_utc_us, is_success, index, file_url)` |
| `CurrentSettingsUpdate` | 欄位 `(component_id, current_settings)` |
| `EulerAngle` | 欄位 `(roll_deg, pitch_deg, yaw_deg)` |
| `Information` | 欄位 `(component_id, vendor_name, model_name, focal_length_mm, horizontal_sensor_size_mm, vertical_sensor_size_mm, horizontal_resolution_px, vertical_resolution_px)` |
| `Mode` | 列舉:`UNKNOWN`、`PHOTO`、`VIDEO` |
| `ModeUpdate` | 欄位 `(component_id, mode)` |
| `Option` | 欄位 `(option_id, option_description)` |
| `PhotosRange` | 列舉:`ALL`、`SINCE_CONNECTION` |
| `Position` | 欄位 `(latitude_deg, longitude_deg, absolute_altitude_m, relative_altitude_m)` |
| `PossibleSettingOptionsUpdate` | 欄位 `(component_id, setting_options)` |
| `Quaternion` | 欄位 `(w, x, y, z)` |
| `Setting` | 欄位 `(setting_id, setting_description, option, is_range)` |
| `SettingOptions` | 欄位 `(component_id, setting_id, setting_description, options, is_range)` |
| `Storage` | 欄位 `(component_id, video_on, photo_interval_on, used_storage_mib, available_storage_mib, total_storage_mib, recording_time_s, media_folder_name, storage_status, storage_id, storage_type)` |
| `StorageUpdate` | 欄位 `(component_id, storage)` |
| `VideoStreamInfo` | 欄位 `(stream_id, settings, status, spectrum)` |
| `VideoStreamSettings` | 欄位 `(frame_rate_hz, horizontal_resolution_pix, vertical_resolution_pix, bit_rate_b_s, rotation_deg, uri, horizontal_fov_deg)` |
| `VideoStreamUpdate` | 欄位 `(component_id, video_stream_info)` |

## camera_server

類別 `mavsdk.camera_server.CameraServer`,存取路徑 `drone.camera_server`。

| 方法 | 型態 |
|---|---|
| `respond_capture_status(capture_status_feedback, capture_status)` | 呼叫 |
| `respond_format_storage(format_storage_feedback)` | 呼叫 |
| `respond_reset_settings(reset_settings_feedback)` | 呼叫 |
| `respond_set_mode(set_mode_feedback)` | 呼叫 |
| `respond_start_video(start_video_feedback)` | 呼叫 |
| `respond_start_video_streaming(start_video_streaming_feedback)` | 呼叫 |
| `respond_stop_video(stop_video_feedback)` | 呼叫 |
| `respond_stop_video_streaming(stop_video_streaming_feedback)` | 呼叫 |
| `respond_storage_information(storage_information_feedback, storage_information)` | 呼叫 |
| `respond_take_photo(take_photo_feedback, capture_info)` | 呼叫 |
| `respond_tracking_off_command(stop_video_feedback)` | 呼叫 |
| `respond_tracking_point_command(stop_video_feedback)` | 呼叫 |
| `respond_tracking_rectangle_command(stop_video_feedback)` | 呼叫 |
| `respond_zoom_in_start(zoom_in_start_feedback)` | 呼叫 |
| `respond_zoom_out_start(zoom_out_start_feedback)` | 呼叫 |
| `respond_zoom_range(zoom_range_feedback)` | 呼叫 |
| `respond_zoom_stop(zoom_stop_feedback)` | 呼叫 |
| `set_in_progress(in_progress)` | 呼叫 |
| `set_information(information)` | 呼叫 |
| `set_tracking_off_status()` | 呼叫 |
| `set_tracking_rectangle_status(tracked_rectangle)` | 呼叫 |
| `set_video_streaming(video_streaming)` | 呼叫 |
| `capture_status()` | 串流 |
| `format_storage()` | 串流 |
| `reset_settings()` | 串流 |
| `set_mode()` | 串流 |
| `start_video()` | 串流 |
| `start_video_streaming()` | 串流 |
| `stop_video()` | 串流 |
| `stop_video_streaming()` | 串流 |
| `storage_information()` | 串流 |
| `take_photo()` | 串流 |
| `tracking_off_command()` | 串流 |
| `tracking_point_command()` | 串流 |
| `tracking_rectangle_command()` | 串流 |
| `zoom_in_start()` | 串流 |
| `zoom_out_start()` | 串流 |
| `zoom_range()` | 串流 |
| `zoom_stop()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`IN_PROGRESS`、`BUSY`、`DENIED`、`ERROR`、`TIMEOUT`、`WRONG_ARGUMENT`、`NO_SYSTEM`

| 型別 | 內容 |
|---|---|
| `CameraFeedback` | 列舉:`UNKNOWN`、`OK`、`BUSY`、`FAILED` |
| `CameraServerError` | 欄位 `(result, origin, *params)` |
| `CaptureInfo` | 欄位 `(position, attitude_quaternion, time_utc_us, is_success, index, file_url)` |
| `CaptureStatus` | 欄位 `(image_interval_s, recording_time_s, available_capacity_mib, image_status, video_status, image_count)` |
| `Information` | 欄位 `(vendor_name, model_name, firmware_version, focal_length_mm, horizontal_sensor_size_mm, vertical_sensor_size_mm, horizontal_resolution_px, vertical_resolution_px, lens_id, definition_file_version, definition_file_uri, image_in_video_mode_supported, video_in_image_mode_supported)` |
| `Mode` | 列舉:`UNKNOWN`、`PHOTO`、`VIDEO` |
| `Position` | 欄位 `(latitude_deg, longitude_deg, absolute_altitude_m, relative_altitude_m)` |
| `Quaternion` | 欄位 `(w, x, y, z)` |
| `StorageInformation` | 欄位 `(used_storage_mib, available_storage_mib, total_storage_mib, storage_status, storage_id, storage_type, read_speed_mib_s, write_speed_mib_s)` |
| `TrackPoint` | 欄位 `(point_x, point_y, radius)` |
| `TrackRectangle` | 欄位 `(top_left_corner_x, top_left_corner_y, bottom_right_corner_x, bottom_right_corner_y)` |
| `VideoStreaming` | 欄位 `(has_rtsp_server, rtsp_uri)` |

## component_metadata

類別 `mavsdk.component_metadata.ComponentMetadata`,存取路徑 `drone.component_metadata`。

| 方法 | 型態 |
|---|---|
| `get_metadata(compid, metadata_type)` | 呼叫 |
| `request_autopilot_component()` | 呼叫 |
| `request_component(compid)` | 呼叫 |
| `metadata_available()` | 串流 |

錯誤碼:`SUCCESS`、`NOT_AVAILABLE`、`CONNECTION_ERROR`、`UNSUPPORTED`、`DENIED`、`FAILED`、`TIMEOUT`、`NO_SYSTEM`、`NOT_REQUESTED`

| 型別 | 內容 |
|---|---|
| `ComponentMetadataError` | 欄位 `(result, origin, *params)` |
| `MetadataData` | 欄位 `(json_metadata)` |
| `MetadataType` | 列舉:`ALL_COMPLETED`、`PARAMETER`、`EVENTS`、`ACTUATORS` |
| `MetadataUpdate` | 欄位 `(compid, type, json_metadata)` |

## component_metadata_server

類別 `mavsdk.component_metadata_server.ComponentMetadataServer`,存取路徑 `drone.component_metadata_server`。

| 方法 | 型態 |
|---|---|
| `set_metadata(metadata)` | 呼叫 |

| 型別 | 內容 |
|---|---|
| `Metadata` | 欄位 `(type, json_metadata)` |
| `MetadataType` | 列舉:`PARAMETER`、`EVENTS`、`ACTUATORS` |

## core

類別 `mavsdk.core.Core`,存取路徑 `drone.core`。

| 方法 | 型態 |
|---|---|
| `set_mavlink_timeout(timeout_s)` | 呼叫 |
| `connection_state()` | 串流 |

| 型別 | 內容 |
|---|---|
| `ConnectionState` | 欄位 `(is_connected)` |

## events

類別 `mavsdk.events.Events`,存取路徑 `drone.events`。

| 方法 | 型態 |
|---|---|
| `get_health_and_arming_checks_report()` | 呼叫 |
| `events()` | 串流 |
| `health_and_arming_checks()` | 串流 |

錯誤碼:`SUCCESS`、`NOT_AVAILABLE`、`CONNECTION_ERROR`、`UNSUPPORTED`、`DENIED`、`FAILED`、`TIMEOUT`、`NO_SYSTEM`、`UNKNOWN`

| 型別 | 內容 |
|---|---|
| `Event` | 欄位 `(compid, message, description, log_level, event_namespace, event_name)` |
| `EventsError` | 欄位 `(result, origin, *params)` |
| `HealthAndArmingCheckMode` | 欄位 `(mode_name, can_arm_or_run, problems)` |
| `HealthAndArmingCheckProblem` | 欄位 `(message, description, log_level, health_component)` |
| `HealthAndArmingCheckReport` | 欄位 `(current_mode_intention, health_components, all_problems)` |
| `HealthComponentReport` | 欄位 `(name, label, is_present, has_error, has_warning)` |
| `LogLevel` | 列舉:`EMERGENCY`、`ALERT`、`CRITICAL`、`ERROR`、`WARNING`、`NOTICE`、`INFO`、`DEBUG` |

## failure

類別 `mavsdk.failure.Failure`,存取路徑 `drone.failure`。

| 方法 | 型態 |
|---|---|
| `inject(failure_unit, failure_type, instance)` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`UNSUPPORTED`、`DENIED`、`DISABLED`、`TIMEOUT`

| 型別 | 內容 |
|---|---|
| `FailureError` | 欄位 `(result, origin, *params)` |
| `FailureType` | 列舉:`OK`、`OFF`、`STUCK`、`GARBAGE`、`WRONG`、`SLOW`、`DELAYED`、`INTERMITTENT` |
| `FailureUnit` | 列舉:`SENSOR_GYRO`、`SENSOR_ACCEL`、`SENSOR_MAG`、`SENSOR_BARO`、`SENSOR_GPS`、`SENSOR_OPTICAL_FLOW`、`SENSOR_VIO`、`SENSOR_DISTANCE_SENSOR`、`SENSOR_AIRSPEED`、`SYSTEM_BATTERY`、`SYSTEM_MOTOR`、`SYSTEM_SERVO`、`SYSTEM_AVOIDANCE`、`SYSTEM_RC_SIGNAL`、`SYSTEM_MAVLINK_SIGNAL` |

## follow_me

類別 `mavsdk.follow_me.FollowMe`,存取路徑 `drone.follow_me`。

| 方法 | 型態 |
|---|---|
| `get_config()` | 呼叫 |
| `get_last_location()` | 呼叫 |
| `is_active()` | 呼叫 |
| `set_config(config)` | 呼叫 |
| `set_target_location(location)` | 呼叫 |
| `start()` | 呼叫 |
| `stop()` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`BUSY`、`COMMAND_DENIED`、`TIMEOUT`、`NOT_ACTIVE`、`SET_CONFIG_FAILED`

| 型別 | 內容 |
|---|---|
| `Config` | 欄位 `(follow_height_m, follow_distance_m, responsiveness, altitude_mode, max_tangential_vel_m_s, follow_angle_deg)` |
| `FollowMeError` | 欄位 `(result, origin, *params)` |
| `TargetLocation` | 欄位 `(latitude_deg, longitude_deg, absolute_altitude_m, velocity_x_m_s, velocity_y_m_s, velocity_z_m_s)` |

## ftp

類別 `mavsdk.ftp.Ftp`,存取路徑 `drone.ftp`。

| 方法 | 型態 |
|---|---|
| `are_files_identical(local_file_path, remote_file_path)` | 呼叫 |
| `create_directory(remote_dir)` | 呼叫 |
| `list_directory(remote_dir)` | 呼叫 |
| `remove_directory(remote_dir)` | 呼叫 |
| `remove_file(remote_file_path)` | 呼叫 |
| `rename(remote_from_path, remote_to_path)` | 呼叫 |
| `set_target_compid(compid)` | 呼叫 |
| `download(remote_file_path, local_dir, use_burst)` | 串流 |
| `upload(local_file_path, remote_dir)` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NEXT`、`TIMEOUT`、`BUSY`、`FILE_IO_ERROR`、`FILE_EXISTS`、`FILE_DOES_NOT_EXIST`、`FILE_PROTECTED`、`INVALID_PARAMETER`、`UNSUPPORTED`、`PROTOCOL_ERROR`、`NO_SYSTEM`

| 型別 | 內容 |
|---|---|
| `FtpError` | 欄位 `(result, origin, *params)` |
| `ListDirectoryData` | 欄位 `(dirs, files)` |
| `ProgressData` | 欄位 `(bytes_transferred, total_bytes)` |

## ftp_server

類別 `mavsdk.ftp_server.FtpServer`,存取路徑 `drone.ftp_server`。

| 方法 | 型態 |
|---|---|
| `set_root_dir(path)` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`DOES_NOT_EXIST`、`BUSY`

| 型別 | 內容 |
|---|---|
| `FtpServerError` | 欄位 `(result, origin, *params)` |

## geofence

類別 `mavsdk.geofence.Geofence`,存取路徑 `drone.geofence`。

| 方法 | 型態 |
|---|---|
| `clear_geofence()` | 呼叫 |
| `download_geofence()` | 呼叫 |
| `upload_geofence(geofence_data)` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`ERROR`、`TOO_MANY_GEOFENCE_ITEMS`、`BUSY`、`TIMEOUT`、`INVALID_ARGUMENT`、`NO_SYSTEM`

| 型別 | 內容 |
|---|---|
| `Circle` | 欄位 `(point, radius, fence_type)` |
| `FenceType` | 列舉:`INCLUSION`、`EXCLUSION` |
| `GeofenceData` | 欄位 `(polygons, circles)` |
| `GeofenceError` | 欄位 `(result, origin, *params)` |
| `Point` | 欄位 `(latitude_deg, longitude_deg)` |
| `Polygon` | 欄位 `(points, fence_type)` |

## gimbal

類別 `mavsdk.gimbal.Gimbal`,存取路徑 `drone.gimbal`。

| 方法 | 型態 |
|---|---|
| `get_attitude(gimbal_id)` | 呼叫 |
| `get_control_status(gimbal_id)` | 呼叫 |
| `release_control(gimbal_id)` | 呼叫 |
| `set_angles(gimbal_id, roll_deg, pitch_deg, yaw_deg, gimbal_mode, send_mode)` | 呼叫 |
| `set_angular_rates(gimbal_id, roll_rate_deg_s, pitch_rate_deg_s, yaw_rate_deg_s, gimbal_mode, send_mode)` | 呼叫 |
| `set_roi_location(gimbal_id, latitude_deg, longitude_deg, altitude_m)` | 呼叫 |
| `take_control(gimbal_id, control_mode)` | 呼叫 |
| `attitude()` | 串流 |
| `control_status()` | 串流 |
| `gimbal_list()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`ERROR`、`TIMEOUT`、`UNSUPPORTED`、`NO_SYSTEM`、`INVALID_ARGUMENT`

| 型別 | 內容 |
|---|---|
| `AngularVelocityBody` | 欄位 `(roll_rad_s, pitch_rad_s, yaw_rad_s)` |
| `Attitude` | 欄位 `(gimbal_id, euler_angle_forward, quaternion_forward, euler_angle_north, quaternion_north, angular_velocity, timestamp_us)` |
| `ControlMode` | 列舉:`NONE`、`PRIMARY`、`SECONDARY` |
| `ControlStatus` | 欄位 `(gimbal_id, control_mode, sysid_primary_control, compid_primary_control, sysid_secondary_control, compid_secondary_control)` |
| `EulerAngle` | 欄位 `(roll_deg, pitch_deg, yaw_deg)` |
| `GimbalError` | 欄位 `(result, origin, *params)` |
| `GimbalItem` | 欄位 `(gimbal_id, vendor_name, model_name, custom_name, gimbal_manager_component_id, gimbal_device_id)` |
| `GimbalList` | 欄位 `(gimbals)` |
| `GimbalMode` | 列舉:`YAW_FOLLOW`、`YAW_LOCK` |
| `Quaternion` | 欄位 `(w, x, y, z)` |
| `SendMode` | 列舉:`ONCE`、`STREAM` |

## gripper

類別 `mavsdk.gripper.Gripper`,存取路徑 `drone.gripper`。

| 方法 | 型態 |
|---|---|
| `grab(instance)` | 呼叫 |
| `release(instance)` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`BUSY`、`TIMEOUT`、`UNSUPPORTED`、`FAILED`

| 型別 | 內容 |
|---|---|
| `GripperAction` | 列舉:`RELEASE`、`GRAB` |
| `GripperError` | 欄位 `(result, origin, *params)` |

## info

類別 `mavsdk.info.Info`,存取路徑 `drone.info`。

| 方法 | 型態 |
|---|---|
| `get_flight_information()` | 呼叫 |
| `get_identification()` | 呼叫 |
| `get_product()` | 呼叫 |
| `get_speed_factor()` | 呼叫 |
| `get_version()` | 呼叫 |
| `flight_information()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`INFORMATION_NOT_RECEIVED_YET`、`NO_SYSTEM`

| 型別 | 內容 |
|---|---|
| `FlightInfo` | 欄位 `(time_boot_ms, flight_uid, duration_since_arming_ms, duration_since_takeoff_ms)` |
| `Identification` | 欄位 `(hardware_uid, legacy_uid)` |
| `InfoError` | 欄位 `(result, origin, *params)` |
| `Product` | 欄位 `(vendor_id, vendor_name, product_id, product_name)` |
| `Version` | 欄位 `(flight_sw_major, flight_sw_minor, flight_sw_patch, flight_sw_vendor_major, flight_sw_vendor_minor, flight_sw_vendor_patch, os_sw_major, os_sw_minor, os_sw_patch, flight_sw_git_hash, os_sw_git_hash, flight_sw_version_type)` |

## log_files

類別 `mavsdk.log_files.LogFiles`,存取路徑 `drone.log_files`。

| 方法 | 型態 |
|---|---|
| `erase_all_log_files()` | 呼叫 |
| `get_entries()` | 呼叫 |
| `download_log_file(entry, path)` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NEXT`、`NO_LOGFILES`、`TIMEOUT`、`INVALID_ARGUMENT`、`FILE_OPEN_FAILED`、`NO_SYSTEM`

| 型別 | 內容 |
|---|---|
| `Entry` | 欄位 `(id, date, size_bytes)` |
| `LogFilesError` | 欄位 `(result, origin, *params)` |
| `ProgressData` | 欄位 `(progress)` |

## log_streaming

類別 `mavsdk.log_streaming.LogStreaming`,存取路徑 `drone.log_streaming`。

| 方法 | 型態 |
|---|---|
| `start_log_streaming()` | 呼叫 |
| `stop_log_streaming()` | 呼叫 |
| `log_streaming_raw()` | 串流 |

錯誤碼:`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`BUSY`、`COMMAND_DENIED`、`TIMEOUT`、`UNSUPPORTED`、`UNKNOWN`

| 型別 | 內容 |
|---|---|
| `LogStreamingError` | 欄位 `(result, origin, *params)` |
| `LogStreamingRaw` | 欄位 `(data_base64)` |

## manual_control

類別 `mavsdk.manual_control.ManualControl`,存取路徑 `drone.manual_control`。

| 方法 | 型態 |
|---|---|
| `set_manual_control_input(x, y, z, r)` | 呼叫 |
| `start_altitude_control()` | 呼叫 |
| `start_position_control()` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`BUSY`、`COMMAND_DENIED`、`TIMEOUT`、`INPUT_OUT_OF_RANGE`、`INPUT_NOT_SET`

| 型別 | 內容 |
|---|---|
| `ManualControlError` | 欄位 `(result, origin, *params)` |

## mavlink_direct

類別 `mavsdk.mavlink_direct.MavlinkDirect`,存取路徑 `drone.mavlink_direct`。

| 方法 | 型態 |
|---|---|
| `load_custom_xml(xml_content)` | 呼叫 |
| `send_message(message)` | 呼叫 |
| `message(message_name)` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`ERROR`、`INVALID_MESSAGE`、`INVALID_FIELD`、`CONNECTION_ERROR`、`NO_SYSTEM`、`TIMEOUT`

| 型別 | 內容 |
|---|---|
| `MavlinkDirectError` | 欄位 `(result, origin, *params)` |
| `MavlinkMessage` | 欄位 `(message_name, system_id, component_id, target_system_id, target_component_id, fields_json)` |

## mission

類別 `mavsdk.mission.Mission`,存取路徑 `drone.mission`。

| 方法 | 型態 |
|---|---|
| `cancel_mission_download()` | 呼叫 |
| `cancel_mission_upload()` | 呼叫 |
| `clear_mission()` | 呼叫 |
| `download_mission()` | 呼叫 |
| `get_return_to_launch_after_mission()` | 呼叫 |
| `is_mission_finished()` | 呼叫 |
| `pause_mission()` | 呼叫 |
| `set_current_mission_item(index)` | 呼叫 |
| `set_return_to_launch_after_mission(enable)` | 呼叫 |
| `start_mission()` | 呼叫 |
| `upload_mission(mission_plan)` | 呼叫 |
| `download_mission_with_progress()` | 串流 |
| `mission_progress()` | 串流 |
| `upload_mission_with_progress(mission_plan)` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`ERROR`、`TOO_MANY_MISSION_ITEMS`、`BUSY`、`TIMEOUT`、`INVALID_ARGUMENT`、`UNSUPPORTED`、`NO_MISSION_AVAILABLE`、`UNSUPPORTED_MISSION_CMD`、`TRANSFER_CANCELLED`、`NO_SYSTEM`、`NEXT`、`DENIED`、`PROTOCOL_ERROR`、`INT_MESSAGES_NOT_SUPPORTED`

| 型別 | 內容 |
|---|---|
| `MissionError` | 欄位 `(result, origin, *params)` |
| `MissionItem` | 欄位 `(latitude_deg, longitude_deg, relative_altitude_m, speed_m_s, is_fly_through, gimbal_pitch_deg, gimbal_yaw_deg, camera_action, loiter_time_s, camera_photo_interval_s, acceptance_radius_m, yaw_deg, camera_photo_distance_m, vehicle_action)` |
| `MissionPlan` | 欄位 `(mission_items)` |
| `MissionProgress` | 欄位 `(current, total)` |
| `ProgressData` | 欄位 `(progress)` |
| `ProgressDataOrMission` | 欄位 `(has_progress, progress, has_mission, mission_plan)` |

## mission_raw

類別 `mavsdk.mission_raw.MissionRaw`,存取路徑 `drone.mission_raw`。

| 方法 | 型態 |
|---|---|
| `cancel_mission_download()` | 呼叫 |
| `cancel_mission_upload()` | 呼叫 |
| `clear_mission()` | 呼叫 |
| `download_geofence()` | 呼叫 |
| `download_mission()` | 呼叫 |
| `download_rallypoints()` | 呼叫 |
| `import_mission_planner_mission(mission_planner_path)` | 呼叫 |
| `import_mission_planner_mission_from_string(mission_planner_mission)` | 呼叫 |
| `import_qgroundcontrol_mission(qgc_plan_path)` | 呼叫 |
| `import_qgroundcontrol_mission_from_string(qgc_plan)` | 呼叫 |
| `is_mission_finished()` | 呼叫 |
| `pause_mission()` | 呼叫 |
| `set_current_mission_item(index)` | 呼叫 |
| `start_mission()` | 呼叫 |
| `upload_geofence(mission_items)` | 呼叫 |
| `upload_mission(mission_items)` | 呼叫 |
| `upload_rally_points(mission_items)` | 呼叫 |
| `mission_changed()` | 串流 |
| `mission_progress()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`ERROR`、`TOO_MANY_MISSION_ITEMS`、`BUSY`、`TIMEOUT`、`INVALID_ARGUMENT`、`UNSUPPORTED`、`NO_MISSION_AVAILABLE`、`TRANSFER_CANCELLED`、`FAILED_TO_OPEN_QGC_PLAN`、`FAILED_TO_PARSE_QGC_PLAN`、`NO_SYSTEM`、`DENIED`、`MISSION_TYPE_NOT_CONSISTENT`、`INVALID_SEQUENCE`、`CURRENT_INVALID`、`PROTOCOL_ERROR`、`INT_MESSAGES_NOT_SUPPORTED`、`FAILED_TO_OPEN_MISSION_PLANNER_PLAN`、`FAILED_TO_PARSE_MISSION_PLANNER_PLAN`

| 型別 | 內容 |
|---|---|
| `MissionImportData` | 欄位 `(mission_items, geofence_items, rally_items)` |
| `MissionItem` | 欄位 `(seq, frame, command, current, autocontinue, param1, param2, param3, param4, x, y, z, mission_type)` |
| `MissionProgress` | 欄位 `(current, total)` |
| `MissionRawError` | 欄位 `(result, origin, *params)` |

## mission_raw_server

類別 `mavsdk.mission_raw_server.MissionRawServer`,存取路徑 `drone.mission_raw_server`。

| 方法 | 型態 |
|---|---|
| `set_current_item_complete()` | 呼叫 |
| `clear_all()` | 串流 |
| `current_item_changed()` | 串流 |
| `incoming_mission()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`ERROR`、`TOO_MANY_MISSION_ITEMS`、`BUSY`、`TIMEOUT`、`INVALID_ARGUMENT`、`UNSUPPORTED`、`NO_MISSION_AVAILABLE`、`UNSUPPORTED_MISSION_CMD`、`TRANSFER_CANCELLED`、`NO_SYSTEM`、`NEXT`

| 型別 | 內容 |
|---|---|
| `MissionItem` | 欄位 `(seq, frame, command, current, autocontinue, param1, param2, param3, param4, x, y, z, mission_type)` |
| `MissionPlan` | 欄位 `(mission_items)` |
| `MissionProgress` | 欄位 `(current, total)` |
| `MissionRawServerError` | 欄位 `(result, origin, *params)` |

## mocap

類別 `mavsdk.mocap.Mocap`,存取路徑 `drone.mocap`。

| 方法 | 型態 |
|---|---|
| `set_attitude_position_mocap(attitude_position_mocap)` | 呼叫 |
| `set_odometry(odometry)` | 呼叫 |
| `set_vision_position_estimate(vision_position_estimate)` | 呼叫 |
| `set_vision_speed_estimate(vision_speed_estimate)` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`INVALID_REQUEST_DATA`、`UNSUPPORTED`

| 型別 | 內容 |
|---|---|
| `AngleBody` | 欄位 `(roll_rad, pitch_rad, yaw_rad)` |
| `AngularVelocityBody` | 欄位 `(roll_rad_s, pitch_rad_s, yaw_rad_s)` |
| `AttitudePositionMocap` | 欄位 `(time_usec, q, position_body, pose_covariance)` |
| `Covariance` | 欄位 `(covariance_matrix)` |
| `MocapError` | 欄位 `(result, origin, *params)` |
| `Odometry` | 欄位 `(time_usec, frame_id, position_body, q, speed_body, angular_velocity_body, pose_covariance, velocity_covariance, reset_counter, estimator_type, quality_percent)` |
| `PositionBody` | 欄位 `(x_m, y_m, z_m)` |
| `Quaternion` | 欄位 `(w, x, y, z)` |
| `SpeedBody` | 欄位 `(x_m_s, y_m_s, z_m_s)` |
| `SpeedNed` | 欄位 `(north_m_s, east_m_s, down_m_s)` |
| `VisionPositionEstimate` | 欄位 `(time_usec, position_body, angle_body, pose_covariance, reset_counter)` |
| `VisionSpeedEstimate` | 欄位 `(time_usec, speed_ned, speed_covariance, reset_counter)` |

## offboard

類別 `mavsdk.offboard.Offboard`,存取路徑 `drone.offboard`。

| 方法 | 型態 |
|---|---|
| `is_active()` | 呼叫 |
| `set_acceleration_ned(acceleration_ned)` | 呼叫 |
| `set_actuator_control(actuator_control)` | 呼叫 |
| `set_attitude(attitude)` | 呼叫 |
| `set_attitude_rate(attitude_rate)` | 呼叫 |
| `set_position_global(position_global_yaw)` | 呼叫 |
| `set_position_ned(position_ned_yaw)` | 呼叫 |
| `set_position_velocity_acceleration_ned(position_ned_yaw, velocity_ned_yaw, acceleration_ned)` | 呼叫 |
| `set_position_velocity_ned(position_ned_yaw, velocity_ned_yaw)` | 呼叫 |
| `set_velocity_body(velocity_body_yawspeed)` | 呼叫 |
| `set_velocity_ned(velocity_ned_yaw)` | 呼叫 |
| `start()` | 呼叫 |
| `stop()` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`BUSY`、`COMMAND_DENIED`、`TIMEOUT`、`NO_SETPOINT_SET`、`FAILED`

| 型別 | 內容 |
|---|---|
| `AccelerationNed` | 欄位 `(north_m_s2, east_m_s2, down_m_s2)` |
| `ActuatorControl` | 欄位 `(groups)` |
| `ActuatorControlGroup` | 欄位 `(controls)` |
| `Attitude` | 欄位 `(roll_deg, pitch_deg, yaw_deg, thrust_value)` |
| `AttitudeRate` | 欄位 `(roll_deg_s, pitch_deg_s, yaw_deg_s, thrust_value)` |
| `OffboardError` | 欄位 `(result, origin, *params)` |
| `PositionGlobalYaw` | 欄位 `(lat_deg, lon_deg, alt_m, yaw_deg, altitude_type)` |
| `PositionNedYaw` | 欄位 `(north_m, east_m, down_m, yaw_deg)` |
| `VelocityBodyYawspeed` | 欄位 `(forward_m_s, right_m_s, down_m_s, yawspeed_deg_s)` |
| `VelocityNedYaw` | 欄位 `(north_m_s, east_m_s, down_m_s, yaw_deg)` |

## param

類別 `mavsdk.param.Param`,存取路徑 `drone.param`。

| 方法 | 型態 |
|---|---|
| `get_all_params()` | 呼叫 |
| `get_param_custom(name)` | 呼叫 |
| `get_param_float(name)` | 呼叫 |
| `get_param_int(name)` | 呼叫 |
| `select_component(component_id, protocol_version)` | 呼叫 |
| `set_param_custom(name, value)` | 呼叫 |
| `set_param_float(name, value)` | 呼叫 |
| `set_param_int(name, value)` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`TIMEOUT`、`CONNECTION_ERROR`、`WRONG_TYPE`、`PARAM_NAME_TOO_LONG`、`NO_SYSTEM`、`PARAM_VALUE_TOO_LONG`、`FAILED`、`DOES_NOT_EXIST`、`VALUE_OUT_OF_RANGE`、`PERMISSION_DENIED`、`COMPONENT_NOT_FOUND`、`READ_ONLY`、`TYPE_UNSUPPORTED`、`TYPE_MISMATCH`、`READ_FAIL`

| 型別 | 內容 |
|---|---|
| `AllParams` | 欄位 `(int_params, float_params, custom_params)` |
| `CustomParam` | 欄位 `(name, value)` |
| `FloatParam` | 欄位 `(name, value)` |
| `IntParam` | 欄位 `(name, value)` |
| `ParamError` | 欄位 `(result, origin, *params)` |
| `ProtocolVersion` | 列舉:`V1`、`EXT` |

## param_server

類別 `mavsdk.param_server.ParamServer`,存取路徑 `drone.param_server`。

| 方法 | 型態 |
|---|---|
| `provide_param_custom(name, value)` | 呼叫 |
| `provide_param_float(name, value)` | 呼叫 |
| `provide_param_int(name, value)` | 呼叫 |
| `retrieve_all_params()` | 呼叫 |
| `retrieve_param_custom(name)` | 呼叫 |
| `retrieve_param_float(name)` | 呼叫 |
| `retrieve_param_int(name)` | 呼叫 |
| `set_protocol(extended_protocol)` | 呼叫 |
| `changed_param_custom()` | 串流 |
| `changed_param_float()` | 串流 |
| `changed_param_int()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NOT_FOUND`、`WRONG_TYPE`、`PARAM_NAME_TOO_LONG`、`NO_SYSTEM`、`PARAM_VALUE_TOO_LONG`、`PARAM_PROVIDED_TOO_LATE`

| 型別 | 內容 |
|---|---|
| `AllParams` | 欄位 `(int_params, float_params, custom_params)` |
| `CustomParam` | 欄位 `(name, value)` |
| `FloatParam` | 欄位 `(name, value)` |
| `IntParam` | 欄位 `(name, value)` |
| `ParamServerError` | 欄位 `(result, origin, *params)` |

## rtk

類別 `mavsdk.rtk.Rtk`,存取路徑 `drone.rtk`。

| 方法 | 型態 |
|---|---|
| `send_rtcm_data(rtcm_data)` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`TOO_LONG`、`NO_SYSTEM`、`CONNECTION_ERROR`

| 型別 | 內容 |
|---|---|
| `RtcmData` | 欄位 `(data_base64)` |
| `RtkError` | 欄位 `(result, origin, *params)` |

## server_utility

類別 `mavsdk.server_utility.ServerUtility`,存取路徑 `drone.server_utility`。

| 方法 | 型態 |
|---|---|
| `send_status_text(type, text)` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`INVALID_ARGUMENT`

| 型別 | 內容 |
|---|---|
| `ServerUtilityError` | 欄位 `(result, origin, *params)` |
| `StatusTextType` | 列舉:`DEBUG`、`INFO`、`NOTICE`、`WARNING`、`ERROR`、`CRITICAL`、`ALERT`、`EMERGENCY` |

## shell

類別 `mavsdk.shell.Shell`,存取路徑 `drone.shell`。

| 方法 | 型態 |
|---|---|
| `send(command)` | 呼叫 |
| `receive()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`NO_RESPONSE`、`BUSY`

| 型別 | 內容 |
|---|---|
| `ShellError` | 欄位 `(result, origin, *params)` |

## telemetry

類別 `mavsdk.telemetry.Telemetry`,存取路徑 `drone.telemetry`。

| 方法 | 型態 |
|---|---|
| `get_gps_global_origin()` | 呼叫 |
| `set_rate_actuator_control_target(rate_hz)` | 呼叫 |
| `set_rate_actuator_output_status(rate_hz)` | 呼叫 |
| `set_rate_altitude(rate_hz)` | 呼叫 |
| `set_rate_attitude_euler(rate_hz)` | 呼叫 |
| `set_rate_attitude_quaternion(rate_hz)` | 呼叫 |
| `set_rate_battery(rate_hz)` | 呼叫 |
| `set_rate_distance_sensor(rate_hz)` | 呼叫 |
| `set_rate_fixedwing_metrics(rate_hz)` | 呼叫 |
| `set_rate_gps_info(rate_hz)` | 呼叫 |
| `set_rate_ground_truth(rate_hz)` | 呼叫 |
| `set_rate_health(rate_hz)` | 呼叫 |
| `set_rate_home(rate_hz)` | 呼叫 |
| `set_rate_imu(rate_hz)` | 呼叫 |
| `set_rate_in_air(rate_hz)` | 呼叫 |
| `set_rate_landed_state(rate_hz)` | 呼叫 |
| `set_rate_odometry(rate_hz)` | 呼叫 |
| `set_rate_position(rate_hz)` | 呼叫 |
| `set_rate_position_velocity_ned(rate_hz)` | 呼叫 |
| `set_rate_raw_gps(rate_hz)` | 呼叫 |
| `set_rate_raw_imu(rate_hz)` | 呼叫 |
| `set_rate_rc_status(rate_hz)` | 呼叫 |
| `set_rate_scaled_imu(rate_hz)` | 呼叫 |
| `set_rate_unix_epoch_time(rate_hz)` | 呼叫 |
| `set_rate_velocity_ned(rate_hz)` | 呼叫 |
| `set_rate_vtol_state(rate_hz)` | 呼叫 |
| `actuator_control_target()` | 串流 |
| `actuator_output_status()` | 串流 |
| `altitude()` | 串流 |
| `armed()` | 串流 |
| `attitude_angular_velocity_body()` | 串流 |
| `attitude_euler()` | 串流 |
| `attitude_quaternion()` | 串流 |
| `battery()` | 串流 |
| `distance_sensor()` | 串流 |
| `fixedwing_metrics()` | 串流 |
| `flight_mode()` | 串流 |
| `gps_info()` | 串流 |
| `ground_truth()` | 串流 |
| `heading()` | 串流 |
| `health()` | 串流 |
| `health_all_ok()` | 串流 |
| `home()` | 串流 |
| `imu()` | 串流 |
| `in_air()` | 串流 |
| `landed_state()` | 串流 |
| `odometry()` | 串流 |
| `position()` | 串流 |
| `position_velocity_ned()` | 串流 |
| `raw_gps()` | 串流 |
| `raw_imu()` | 串流 |
| `rc_status()` | 串流 |
| `scaled_imu()` | 串流 |
| `scaled_pressure()` | 串流 |
| `status_text()` | 串流 |
| `unix_epoch_time()` | 串流 |
| `velocity_ned()` | 串流 |
| `vtol_state()` | 串流 |
| `wind()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`BUSY`、`COMMAND_DENIED`、`TIMEOUT`、`UNSUPPORTED`

| 型別 | 內容 |
|---|---|
| `AccelerationFrd` | 欄位 `(forward_m_s2, right_m_s2, down_m_s2)` |
| `ActuatorControlTarget` | 欄位 `(group, controls)` |
| `ActuatorOutputStatus` | 欄位 `(active, actuator)` |
| `Altitude` | 欄位 `(altitude_monotonic_m, altitude_amsl_m, altitude_local_m, altitude_relative_m, altitude_terrain_m, bottom_clearance_m, timestamp_us)` |
| `AngularVelocityBody` | 欄位 `(roll_rad_s, pitch_rad_s, yaw_rad_s)` |
| `AngularVelocityFrd` | 欄位 `(forward_rad_s, right_rad_s, down_rad_s)` |
| `Battery` | 欄位 `(id, temperature_degc, voltage_v, current_battery_a, capacity_consumed_ah, remaining_percent, time_remaining_s, battery_function)` |
| `BatteryFunction` | 列舉:`UNKNOWN`、`ALL`、`PROPULSION`、`AVIONICS`、`PAYLOAD` |
| `Covariance` | 欄位 `(covariance_matrix)` |
| `DistanceSensor` | 欄位 `(minimum_distance_m, maximum_distance_m, current_distance_m, orientation)` |
| `EulerAngle` | 欄位 `(roll_deg, pitch_deg, yaw_deg, timestamp_us)` |
| `FixType` | 列舉:`NO_GPS`、`NO_FIX`、`FIX_2D`、`FIX_3D`、`FIX_DGPS`、`RTK_FLOAT`、`RTK_FIXED` |
| `FixedwingMetrics` | 欄位 `(airspeed_m_s, throttle_percentage, climb_rate_m_s, groundspeed_m_s, heading_deg, absolute_altitude_m)` |
| `FlightMode` | 列舉:`UNKNOWN`、`READY`、`TAKEOFF`、`HOLD`、`MISSION`、`RETURN_TO_LAUNCH`、`LAND`、`OFFBOARD`、`FOLLOW_ME`、`MANUAL`、`ALTCTL`、`POSCTL`、`ACRO`、`STABILIZED`、`RATTITUDE` |
| `GpsGlobalOrigin` | 欄位 `(latitude_deg, longitude_deg, altitude_m)` |
| `GpsInfo` | 欄位 `(num_satellites, fix_type)` |
| `GroundTruth` | 欄位 `(latitude_deg, longitude_deg, absolute_altitude_m, timestamp_us)` |
| `Heading` | 欄位 `(heading_deg)` |
| `Health` | 欄位 `(is_gyrometer_calibration_ok, is_accelerometer_calibration_ok, is_magnetometer_calibration_ok, is_local_position_ok, is_global_position_ok, is_home_position_ok, is_armable)` |
| `Imu` | 欄位 `(acceleration_frd, angular_velocity_frd, magnetic_field_frd, temperature_degc, timestamp_us)` |
| `LandedState` | 列舉:`UNKNOWN`、`ON_GROUND`、`IN_AIR`、`TAKING_OFF`、`LANDING` |
| `MagneticFieldFrd` | 欄位 `(forward_gauss, right_gauss, down_gauss)` |
| `Odometry` | 欄位 `(time_usec, frame_id, child_frame_id, position_body, q, velocity_body, angular_velocity_body, pose_covariance, velocity_covariance)` |
| `Position` | 欄位 `(latitude_deg, longitude_deg, absolute_altitude_m, relative_altitude_m)` |
| `PositionBody` | 欄位 `(x_m, y_m, z_m)` |
| `PositionNed` | 欄位 `(north_m, east_m, down_m)` |
| `PositionVelocityNed` | 欄位 `(position, velocity)` |
| `Quaternion` | 欄位 `(w, x, y, z, timestamp_us)` |
| `RawGps` | 欄位 `(timestamp_us, latitude_deg, longitude_deg, absolute_altitude_m, hdop, vdop, velocity_m_s, cog_deg, altitude_ellipsoid_m, horizontal_uncertainty_m, vertical_uncertainty_m, velocity_uncertainty_m_s, heading_uncertainty_deg, yaw_deg)` |
| `RcStatus` | 欄位 `(was_available_once, is_available, signal_strength_percent)` |
| `ScaledPressure` | 欄位 `(timestamp_us, absolute_pressure_hpa, differential_pressure_hpa, temperature_deg, differential_pressure_temperature_deg)` |
| `StatusText` | 欄位 `(type, text)` |
| `StatusTextType` | 列舉:`DEBUG`、`INFO`、`NOTICE`、`WARNING`、`ERROR`、`CRITICAL`、`ALERT`、`EMERGENCY` |
| `TelemetryError` | 欄位 `(result, origin, *params)` |
| `VelocityBody` | 欄位 `(x_m_s, y_m_s, z_m_s)` |
| `VelocityNed` | 欄位 `(north_m_s, east_m_s, down_m_s)` |
| `VtolState` | 列舉:`UNDEFINED`、`TRANSITION_TO_FW`、`TRANSITION_TO_MC`、`MC`、`FW` |
| `Wind` | 欄位 `(wind_x_ned_m_s, wind_y_ned_m_s, wind_z_ned_m_s, horizontal_variability_stddev_m_s, vertical_variability_stddev_m_s, wind_altitude_msl_m, horizontal_wind_speed_accuracy_m_s, vertical_wind_speed_accuracy_m_s)` |

## telemetry_server

類別 `mavsdk.telemetry_server.TelemetryServer`,存取路徑 `drone.telemetry_server`。

| 方法 | 型態 |
|---|---|
| `publish_attitude(angle, angular_velocity)` | 呼叫 |
| `publish_battery(battery)` | 呼叫 |
| `publish_distance_sensor(distance_sensor)` | 呼叫 |
| `publish_extended_sys_state(vtol_state, landed_state)` | 呼叫 |
| `publish_ground_truth(ground_truth)` | 呼叫 |
| `publish_home(home)` | 呼叫 |
| `publish_imu(imu)` | 呼叫 |
| `publish_odometry(odometry)` | 呼叫 |
| `publish_position(position, velocity_ned, heading)` | 呼叫 |
| `publish_position_velocity_ned(position_velocity_ned)` | 呼叫 |
| `publish_raw_gps(raw_gps, gps_info)` | 呼叫 |
| `publish_raw_imu(imu)` | 呼叫 |
| `publish_scaled_imu(imu)` | 呼叫 |
| `publish_status_text(status_text)` | 呼叫 |
| `publish_sys_status(battery, rc_receiver_status, gyro_status, accel_status, mag_status, gps_status)` | 呼叫 |
| `publish_unix_epoch_time(time_us)` | 呼叫 |
| `publish_visual_flight_rules_hud(fixed_wing_metrics)` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`BUSY`、`COMMAND_DENIED`、`TIMEOUT`、`UNSUPPORTED`

| 型別 | 內容 |
|---|---|
| `AccelerationFrd` | 欄位 `(forward_m_s2, right_m_s2, down_m_s2)` |
| `ActuatorControlTarget` | 欄位 `(group, controls)` |
| `ActuatorOutputStatus` | 欄位 `(active, actuator)` |
| `AngularVelocityBody` | 欄位 `(roll_rad_s, pitch_rad_s, yaw_rad_s)` |
| `AngularVelocityFrd` | 欄位 `(forward_rad_s, right_rad_s, down_rad_s)` |
| `Battery` | 欄位 `(voltage_v, remaining_percent)` |
| `Covariance` | 欄位 `(covariance_matrix)` |
| `DistanceSensor` | 欄位 `(minimum_distance_m, maximum_distance_m, current_distance_m)` |
| `EulerAngle` | 欄位 `(roll_deg, pitch_deg, yaw_deg, timestamp_us)` |
| `FixType` | 列舉:`NO_GPS`、`NO_FIX`、`FIX_2D`、`FIX_3D`、`FIX_DGPS`、`RTK_FLOAT`、`RTK_FIXED` |
| `FixedwingMetrics` | 欄位 `(airspeed_m_s, throttle_percentage, climb_rate_m_s, groundspeed_m_s, heading_deg, absolute_altitude_m)` |
| `GpsInfo` | 欄位 `(num_satellites, fix_type)` |
| `GroundTruth` | 欄位 `(latitude_deg, longitude_deg, absolute_altitude_m, timestamp_us)` |
| `Heading` | 欄位 `(heading_deg)` |
| `Imu` | 欄位 `(acceleration_frd, angular_velocity_frd, magnetic_field_frd, temperature_degc, timestamp_us)` |
| `LandedState` | 列舉:`UNKNOWN`、`ON_GROUND`、`IN_AIR`、`TAKING_OFF`、`LANDING` |
| `MagneticFieldFrd` | 欄位 `(forward_gauss, right_gauss, down_gauss)` |
| `Odometry` | 欄位 `(time_usec, frame_id, child_frame_id, position_body, q, velocity_body, angular_velocity_body, pose_covariance, velocity_covariance)` |
| `Position` | 欄位 `(latitude_deg, longitude_deg, absolute_altitude_m, relative_altitude_m)` |
| `PositionBody` | 欄位 `(x_m, y_m, z_m)` |
| `PositionNed` | 欄位 `(north_m, east_m, down_m)` |
| `PositionVelocityNed` | 欄位 `(position, velocity)` |
| `Quaternion` | 欄位 `(w, x, y, z, timestamp_us)` |
| `RawGps` | 欄位 `(timestamp_us, latitude_deg, longitude_deg, absolute_altitude_m, hdop, vdop, velocity_m_s, cog_deg, altitude_ellipsoid_m, horizontal_uncertainty_m, vertical_uncertainty_m, velocity_uncertainty_m_s, heading_uncertainty_deg, yaw_deg)` |
| `RcStatus` | 欄位 `(was_available_once, is_available, signal_strength_percent)` |
| `ScaledPressure` | 欄位 `(timestamp_us, absolute_pressure_hpa, differential_pressure_hpa, temperature_deg, differential_pressure_temperature_deg)` |
| `StatusText` | 欄位 `(type, text)` |
| `StatusTextType` | 列舉:`DEBUG`、`INFO`、`NOTICE`、`WARNING`、`ERROR`、`CRITICAL`、`ALERT`、`EMERGENCY` |
| `TelemetryServerError` | 欄位 `(result, origin, *params)` |
| `VelocityBody` | 欄位 `(x_m_s, y_m_s, z_m_s)` |
| `VelocityNed` | 欄位 `(north_m_s, east_m_s, down_m_s)` |
| `VtolState` | 列舉:`UNDEFINED`、`TRANSITION_TO_FW`、`TRANSITION_TO_MC`、`MC`、`FW` |

## tracking_server

類別 `mavsdk.tracking_server.TrackingServer`,存取路徑 `drone.tracking_server`。

| 方法 | 型態 |
|---|---|
| `respond_tracking_off_command(command_answer)` | 呼叫 |
| `respond_tracking_point_command(command_answer)` | 呼叫 |
| `respond_tracking_rectangle_command(command_answer)` | 呼叫 |
| `set_tracking_off_status()` | 呼叫 |
| `set_tracking_point_status(tracked_point)` | 呼叫 |
| `set_tracking_rectangle_status(tracked_rectangle)` | 呼叫 |
| `tracking_off_command()` | 串流 |
| `tracking_point_command()` | 串流 |
| `tracking_rectangle_command()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`

| 型別 | 內容 |
|---|---|
| `CommandAnswer` | 列舉:`ACCEPTED`、`TEMPORARILY_REJECTED`、`DENIED`、`UNSUPPORTED`、`FAILED` |
| `TrackPoint` | 欄位 `(point_x, point_y, radius)` |
| `TrackRectangle` | 欄位 `(top_left_corner_x, top_left_corner_y, bottom_right_corner_x, bottom_right_corner_y)` |
| `TrackingServerError` | 欄位 `(result, origin, *params)` |

## transponder

類別 `mavsdk.transponder.Transponder`,存取路徑 `drone.transponder`。

| 方法 | 型態 |
|---|---|
| `set_rate_transponder(rate_hz)` | 呼叫 |
| `transponder()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`CONNECTION_ERROR`、`BUSY`、`COMMAND_DENIED`、`TIMEOUT`

| 型別 | 內容 |
|---|---|
| `AdsbAltitudeType` | 列舉:`PRESSURE_QNH`、`GEOMETRIC` |
| `AdsbEmitterType` | 列舉:`NO_INFO`、`LIGHT`、`SMALL`、`LARGE`、`HIGH_VORTEX_LARGE`、`HEAVY`、`HIGHLY_MANUV`、`ROTOCRAFT`、`UNASSIGNED`、`GLIDER`、`LIGHTER_AIR`、`PARACHUTE`、`ULTRA_LIGHT`、`UNASSIGNED2`、`UAV`、`SPACE`、`UNASSGINED3`、`EMERGENCY_SURFACE`、`SERVICE_SURFACE`、`POINT_OBSTACLE` |
| `AdsbVehicle` | 欄位 `(icao_address, latitude_deg, longitude_deg, altitude_type, absolute_altitude_m, heading_deg, horizontal_velocity_m_s, vertical_velocity_m_s, callsign, emitter_type, squawk, tslc_s)` |
| `TransponderError` | 欄位 `(result, origin, *params)` |

## tune

類別 `mavsdk.tune.Tune`,存取路徑 `drone.tune`。

| 方法 | 型態 |
|---|---|
| `play_tune(tune_description)` | 呼叫 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`INVALID_TEMPO`、`TUNE_TOO_LONG`、`ERROR`、`NO_SYSTEM`

| 型別 | 內容 |
|---|---|
| `SongElement` | 列舉:`STYLE_LEGATO`、`STYLE_NORMAL`、`STYLE_STACCATO`、`DURATION_1`、`DURATION_2`、`DURATION_4`、`DURATION_8`、`DURATION_16`、`DURATION_32`、`NOTE_A`、`NOTE_B`、`NOTE_C`、`NOTE_D`、`NOTE_E`、`NOTE_F`、`NOTE_G`、`NOTE_PAUSE`、`SHARP`、`FLAT`、`OCTAVE_UP`、`OCTAVE_DOWN` |
| `TuneDescription` | 欄位 `(song_elements, tempo)` |
| `TuneError` | 欄位 `(result, origin, *params)` |

## winch

類別 `mavsdk.winch.Winch`,存取路徑 `drone.winch`。

| 方法 | 型態 |
|---|---|
| `abandon_line(instance)` | 呼叫 |
| `deliver(instance)` | 呼叫 |
| `hold(instance)` | 呼叫 |
| `load_line(instance)` | 呼叫 |
| `load_payload(instance)` | 呼叫 |
| `lock(instance)` | 呼叫 |
| `rate_control(instance, rate_m_s)` | 呼叫 |
| `relative_length_control(instance, length_m, rate_m_s)` | 呼叫 |
| `relax(instance)` | 呼叫 |
| `retract(instance)` | 呼叫 |
| `status()` | 串流 |

錯誤碼:`UNKNOWN`、`SUCCESS`、`NO_SYSTEM`、`BUSY`、`TIMEOUT`、`UNSUPPORTED`、`FAILED`

| 型別 | 內容 |
|---|---|
| `Status` | 欄位 `(time_usec, line_length_m, speed_m_s, tension_kg, voltage_v, current_a, temperature_c, status_flags)` |
| `StatusFlags` | 欄位 `(healthy, fully_retracted, moving, clutch_engaged, locked, dropping, arresting, ground_sense, retracting, redeliver, abandon_line, locking, load_line, load_payload)` |
| `WinchAction` | 列舉:`RELAXED`、`RELATIVE_LENGTH_CONTROL`、`RATE_CONTROL`、`LOCK`、`DELIVER`、`HOLD`、`RETRACT`、`LOAD_LINE`、`ABANDON_LINE`、`LOAD_PAYLOAD` |
| `WinchError` | 欄位 `(result, origin, *params)` |

---

→ 回 [20 章索引](README.md)
