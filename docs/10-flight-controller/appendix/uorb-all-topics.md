# PX4 uORB 訊息全集 — v1.17.0

> 這份是**產生出來的**,不是手寫的。內容直接解析 PX4 `v1.17.0` 的原始碼,產生器與重跑指令在 [`tools/dump_px4_api.py`](../../../tools/dump_px4_api.py)。換版本重跑,不要手改這個檔。

## 出處

| 項目 | 出處 |
|---|---|
| 原始碼 | <https://github.com/PX4/PX4-Autopilot/tree/v1.17.0>,tarball 為 `archive/refs/tags/v1.17.0.tar.gz` |
| 解析範圍 | `msg/**/*.msg`,共 244 則(對外契約 34 則、內部 210 則) |
| 官方參考 | <https://docs.px4.io/>(預設顯示 main 分支,與此處的 `v1.17.0` 可能不同) |

## 先看這件事:兩區的差別

`msg/versioned/` 底下的 **34 則是刻意穩定下來的對外契約**,其餘 210 則是內部實作細節。

差別不在技術上——兩者都是一樣的 uORB 主題,伴隨電腦都訂閱得到。差別在**承諾**:versioned 的那批改動會顧及相容性,內部的那批可能在任何一個版本改掉欄位而不另行通知。**寫伴隨電腦程式時依賴內部訊息,是把自己綁在特定韌體版本上。**

---

## 對外契約(`msg/versioned/`)

| 訊息 | 欄位數 | 常數 | 說明 |
|---|---|---|---|
| [`ActuatorMotors`](#actuatormotors) | 4 | 3 | Motor control message Normalised thrust setpoint for up to 12 motors. … |
| [`ActuatorServos`](#actuatorservos) | 3 | 2 | Servo control message Normalised output setpoint for up to 8 servos. P… |
| [`AirspeedValidated`](#airspeedvalidated) | 10 | 7 | Validated airspeed Provides information about airspeed (indicated, tru… |
| [`ArmingCheckReply`](#armingcheckreply) | 21 | 3 | Arming check reply This is a response to an ArmingCheckRequest message… |
| [`ArmingCheckRequest`](#armingcheckrequest) | 3 | 1 | Arming check request Broadcast message to request arming checks be rep… |
| [`BatteryStatus`](#batterystatus) | 38 | 24 | Battery status Battery status information for up to 4 battery instance… |
| [`ConfigOverrides`](#configoverrides) | 6 | 4 | Configurable overrides by (external) modes or mode executors |
| [`Event`](#event) | 5 | 2 | Events interface |
| [`FixedWingLateralSetpoint`](#fixedwinglateralsetpoint) | 4 | 1 | Fixed Wing Lateral Setpoint message Used by the fw_lateral_longitudina… |
| [`FixedWingLongitudinalSetpoint`](#fixedwinglongitudinalsetpoint) | 6 | 1 | Fixed Wing Longitudinal Setpoint message Used by the fw_lateral_longit… |
| [`GotoSetpoint`](#gotosetpoint) | 10 | 1 | Position and (optional) heading setpoints with corresponding speed con… |
| [`HomePosition`](#homeposition) | 15 | 1 | GPS home position in WGS84 coordinates. |
| [`LateralControlConfiguration`](#lateralcontrolconfiguration) | 2 | 1 | Fixed Wing Lateral Control Configuration message Used by the fw_latera… |
| [`LongitudinalControlConfiguration`](#longitudinalcontrolconfiguration) | 10 | 1 | Fixed Wing Longitudinal Control Configuration message Used by the fw_l… |
| [`ManualControlSetpoint`](#manualcontrolsetpoint) | 17 | 9 |  |
| [`ModeCompleted`](#modecompleted) | 3 | 3 | Mode completion result, published by an active mode. The possible valu… |
| [`RegisterExtComponentReply`](#registerextcomponentreply) | 8 | 2 |  |
| [`RegisterExtComponentRequest`](#registerextcomponentrequest) | 10 | 3 | Request to register an external component |
| [`TrajectorySetpoint`](#trajectorysetpoint) | 7 | 1 | Trajectory setpoint in NED frame Input to PID position controller. Nee… |
| [`UnregisterExtComponent`](#unregisterextcomponent) | 5 | 1 |  |
| [`VehicleAngularVelocity`](#vehicleangularvelocity) | 4 | 1 |  |
| [`VehicleAttitude`](#vehicleattitude) | 5 | 1 | This is similar to the mavlink message ATTITUDE_QUATERNION, but for on… |
| [`VehicleAttitudeSetpoint`](#vehicleattitudesetpoint) | 4 | 1 |  |
| [`VehicleCommand`](#vehiclecommand) | 15 | 158 | Vehicle Command uORB message. Used for commanding a mission / action /… |
| [`VehicleCommandAck`](#vehiclecommandack) | 8 | 15 | Vehicle Command Ackonwledgement uORB message. Used for acknowledging t… |
| [`VehicleControlMode`](#vehiclecontrolmode) | 16 | 1 |  |
| [`VehicleGlobalPosition`](#vehicleglobalposition) | 18 | 1 | Fused global position in WGS84. This struct contains global position e… |
| [`VehicleLandDetected`](#vehiclelanddetected) | 13 | 1 |  |
| [`VehicleLocalPosition`](#vehiclelocalposition) | 53 | 4 | Fused local position in NED. The coordinate system origin is the vehic… |
| [`VehicleOdometry`](#vehicleodometry) | 13 | 8 | Vehicle odometry data Fits ROS REP 147 for aerial vehicles |
| [`VehicleRatesSetpoint`](#vehicleratessetpoint) | 6 | 1 |  |
| [`VehicleStatus`](#vehiclestatus) | 39 | 67 | Encodes the system state of the vehicle published by commander |
| [`VtolVehicleStatus`](#vtolvehiclestatus) | 3 | 6 | VEHICLE_VTOL_STATE, should match 1:1 MAVLinks's MAV_VTOL_STATE |
| [`Wind`](#wind) | 10 | 1 | Wind estimate (from EKF2) Contains the system-wide estimate of horizon… |

## 內部訊息(`msg/`)

| 訊息 | 欄位數 | 常數 | 說明 |
|---|---|---|---|
| [`ActionRequest`](#actionrequest) | 4 | 13 | Action request for the vehicle's main state Message represents actions… |
| [`ActuatorArmed`](#actuatorarmed) | 8 | 0 |  |
| [`ActuatorControlsStatus`](#actuatorcontrolsstatus) | 2 | 0 |  |
| [`ActuatorOutputs`](#actuatoroutputs) | 3 | 2 |  |
| [`ActuatorServosTrim`](#actuatorservostrim) | 2 | 1 | Servo trims, added as offset to servo outputs |
| [`ActuatorTest`](#actuatortest) | 5 | 7 |  |
| [`AdcReport`](#adcreport) | 6 | 0 |  |
| [`Airspeed`](#airspeed) | 5 | 0 | Airspeed data from sensors This is published by airspeed sensor driver… |
| [`AirspeedValidatedV0`](#airspeedvalidatedv0) | 11 | 1 |  |
| [`AirspeedWind`](#airspeedwind) | 14 | 4 | Wind estimate (from airspeed_selector) Contains wind estimation and ai… |
| [`ArmingCheckReplyV0`](#armingcheckreplyv0) | 20 | 3 |  |
| [`ArmingCheckRequestV0`](#armingcheckrequestv0) | 2 | 1 | Arming check request. Broadcast message to request arming checks be re… |
| [`AutotuneAttitudeControlStatus`](#autotuneattitudecontrolstatus) | 15 | 17 | Autotune attitude control status This message is published by the fw_a… |
| [`BatteryInfo`](#batteryinfo) | 3 | 0 | Battery information Static or near-invariant battery information. Shou… |
| [`BatteryStatusV0`](#batterystatusv0) | 39 | 24 | Battery status Battery status information for up to 4 battery instance… |
| [`ButtonEvent`](#buttonevent) | 2 | 1 |  |
| [`CameraCapture`](#cameracapture) | 9 | 0 |  |
| [`CameraStatus`](#camerastatus) | 3 | 0 |  |
| [`CameraTrigger`](#cameratrigger) | 4 | 1 |  |
| [`CanInterfaceStatus`](#caninterfacestatus) | 5 | 0 |  |
| [`CellularStatus`](#cellularstatus) | 8 | 22 | Cellular status This is currently used only for logging cell status fr… |
| [`CollisionConstraints`](#collisionconstraints) | 3 | 0 | Local setpoint constraints in NED frame setting something to NaN means… |
| [`ControlAllocatorStatus`](#controlallocatorstatus) | 8 | 5 |  |
| [`Cpuload`](#cpuload) | 3 | 0 |  |
| [`DatamanRequest`](#datamanrequest) | 7 | 0 |  |
| [`DatamanResponse`](#datamanresponse) | 7 | 6 |  |
| [`DebugArray`](#debugarray) | 4 | 1 |  |
| [`DebugKeyValue`](#debugkeyvalue) | 3 | 0 |  |
| [`DebugValue`](#debugvalue) | 3 | 0 |  |
| [`DebugVect`](#debugvect) | 5 | 0 |  |
| [`DifferentialPressure`](#differentialpressure) | 6 | 0 |  |
| [`DistanceSensor`](#distancesensor) | 13 | 22 | DISTANCE_SENSOR message data |
| [`DistanceSensorModeChangeRequest`](#distancesensormodechangerequest) | 2 | 2 |  |
| [`DronecanNodeStatus`](#dronecannodestatus) | 7 | 9 |  |
| [`Ekf2Timestamps`](#ekf2timestamps) | 8 | 1 | this message contains the (relative) timestamps of the sensor inputs u… |
| [`EscReport`](#escreport) | 12 | 11 |  |
| [`EscStatus`](#escstatus) | 7 | 7 |  |
| [`EstimatorAidSource1d`](#estimatoraidsource1d) | 14 | 0 |  |
| [`EstimatorAidSource2d`](#estimatoraidsource2d) | 14 | 0 |  |
| [`EstimatorAidSource3d`](#estimatoraidsource3d) | 14 | 0 |  |
| [`EstimatorBias`](#estimatorbias) | 8 | 0 |  |
| [`EstimatorBias3d`](#estimatorbias3d) | 8 | 0 |  |
| [`EstimatorEventFlags`](#estimatoreventflags) | 20 | 0 |  |
| [`EstimatorGpsStatus`](#estimatorgpsstatus) | 17 | 0 |  |
| [`EstimatorInnovations`](#estimatorinnovations) | 22 | 0 |  |
| [`EstimatorSelectorStatus`](#estimatorselectorstatus) | 16 | 0 |  |
| [`EstimatorSensorBias`](#estimatorsensorbias) | 20 | 0 | Sensor readings and in-run biases in SI-unit form. Sensor readings are… |
| [`EstimatorStates`](#estimatorstates) | 5 | 0 |  |
| [`EstimatorStatus`](#estimatorstatus) | 38 | 43 |  |
| [`EstimatorStatusFlags`](#estimatorstatusflags) | 74 | 0 |  |
| [`EventV0`](#eventv0) | 5 | 2 | this message is required here in the msg_old folder because other msg … |
| [`FailsafeFlags`](#failsafeflags) | 42 | 0 | Input flags for the failsafe state machine set by the arming & health … |
| [`FailureDetectorStatus`](#failuredetectorstatus) | 12 | 0 |  |
| [`FigureEightStatus`](#figureeightstatus) | 8 | 0 |  |
| [`FixedWingLateralGuidanceStatus`](#fixedwinglateralguidancestatus) | 9 | 0 | Fixed Wing Lateral Guidance Status message Published by fw_pos_control… |
| [`FixedWingLateralStatus`](#fixedwinglateralstatus) | 3 | 0 | Fixed Wing Lateral Status message Published by the fw_lateral_longitud… |
| [`FixedWingRunwayControl`](#fixedwingrunwaycontrol) | 3 | 0 | Auxiliary control fields for fixed-wing runway takeoff/landing Passes … |
| [`FlightPhaseEstimation`](#flightphaseestimation) | 2 | 4 |  |
| [`FollowTarget`](#followtarget) | 8 | 0 |  |
| [`FollowTargetEstimator`](#followtargetestimator) | 12 | 0 |  |
| [`FollowTargetStatus`](#followtargetstatus) | 8 | 0 |  |
| [`FuelTankStatus`](#fueltankstatus) | 9 | 3 |  |
| [`GeneratorStatus`](#generatorstatus) | 12 | 23 |  |
| [`GeofenceResult`](#geofenceresult) | 5 | 6 |  |
| [`GeofenceStatus`](#geofencestatus) | 3 | 2 |  |
| [`GimbalControls`](#gimbalcontrols) | 3 | 3 |  |
| [`GimbalDeviceAttitudeStatus`](#gimbaldeviceattitudestatus) | 13 | 7 |  |
| [`GimbalDeviceInformation`](#gimbaldeviceinformation) | 16 | 12 |  |
| [`GimbalDeviceSetAttitude`](#gimbaldevicesetattitude) | 8 | 5 |  |
| [`GimbalManagerInformation`](#gimbalmanagerinformation) | 9 | 14 |  |
| [`GimbalManagerSetAttitude`](#gimbalmanagersetattitude) | 11 | 6 |  |
| [`GimbalManagerSetManualControl`](#gimbalmanagersetmanualcontrol) | 11 | 5 |  |
| [`GimbalManagerStatus`](#gimbalmanagerstatus) | 7 | 0 |  |
| [`GpioConfig`](#gpioconfig) | 5 | 11 | GPIO configuration |
| [`GpioIn`](#gpioin) | 3 | 0 | GPIO mask and state |
| [`GpioOut`](#gpioout) | 4 | 0 | GPIO mask and state |
| [`GpioRequest`](#gpiorequest) | 2 | 0 | Request GPIO mask to be read |
| [`GpsDump`](#gpsdump) | 4 | 1 | This message is used to dump the raw gps communication to the log. |
| [`GpsInjectData`](#gpsinjectdata) | 5 | 2 |  |
| [`Gripper`](#gripper) | 2 | 2 | Used to command an actuation in the gripper, which is mapped to a spec… |
| [`HealthReport`](#healthreport) | 8 | 0 |  |
| [`HeaterStatus`](#heaterstatus) | 12 | 2 |  |
| [`HomePositionV0`](#homepositionv0) | 13 | 1 | GPS home position in WGS84 coordinates. |
| [`HoverThrustEstimate`](#hoverthrustestimate) | 9 | 0 |  |
| [`InputRc`](#inputrc) | 13 | 18 |  |
| [`InternalCombustionEngineControl`](#internalcombustionenginecontrol) | 6 | 0 |  |
| [`InternalCombustionEngineStatus`](#internalcombustionenginestatus) | 23 | 28 |  |
| [`IridiumsbdStatus`](#iridiumsbdstatus) | 15 | 0 |  |
| [`IrlockReport`](#irlockreport) | 6 | 0 | IRLOCK_REPORT message data |
| [`LandingGear`](#landinggear) | 2 | 3 |  |
| [`LandingGearWheel`](#landinggearwheel) | 2 | 0 |  |
| [`LandingTargetInnovations`](#landingtargetinnovations) | 5 | 0 |  |
| [`LandingTargetPose`](#landingtargetpose) | 17 | 0 | Relative position of precision land target in navigation (body fixed, … |
| [`LaunchDetectionStatus`](#launchdetectionstatus) | 2 | 3 | Status of the launch detection state machine (fixed-wing only) |
| [`LedControl`](#ledcontrol) | 6 | 19 | LED control: control a single or multiple LED's. These are the externa… |
| [`LogMessage`](#logmessage) | 3 | 1 | A logging message, output with PX4_WARN, PX4_ERR, PX4_INFO |
| [`LoggerStatus`](#loggerstatus) | 11 | 5 |  |
| [`MagWorkerData`](#magworkerdata) | 10 | 1 |  |
| [`MagnetometerBiasEstimate`](#magnetometerbiasestimate) | 6 | 0 |  |
| [`ManualControlSwitches`](#manualcontrolswitches) | 16 | 12 |  |
| [`MavlinkLog`](#mavlinklog) | 3 | 1 |  |
| [`MavlinkTunnel`](#mavlinktunnel) | 6 | 11 | MAV_TUNNEL_PAYLOAD_TYPE enum |
| [`MessageFormatRequest`](#messageformatrequest) | 3 | 1 |  |
| [`MessageFormatResponse`](#messageformatresponse) | 5 | 0 |  |
| [`Mission`](#mission) | 11 | 0 |  |
| [`MissionResult`](#missionresult) | 15 | 0 |  |
| [`MountOrientation`](#mountorientation) | 2 | 0 |  |
| [`NavigatorMissionItem`](#navigatormissionitem) | 17 | 0 |  |
| [`NavigatorStatus`](#navigatorstatus) | 3 | 2 | Current status of a Navigator mode The possible values of nav_state ar… |
| [`NeuralControl`](#neuralcontrol) | 5 | 0 | Neural control Debugging topic for the Neural controller, logs the inp… |
| [`NormalizedUnsignedSetpoint`](#normalizedunsignedsetpoint) | 2 | 0 |  |
| [`ObstacleDistance`](#obstacledistance) | 8 | 7 | Obstacle distances in front of the sensor. |
| [`OffboardControlMode`](#offboardcontrolmode) | 8 | 0 | Off-board control mode |
| [`OnboardComputerStatus`](#onboardcomputerstatus) | 20 | 0 | ONBOARD_COMPUTER_STATUS message data |
| [`OpenDroneIdArmStatus`](#opendroneidarmstatus) | 3 | 0 |  |
| [`OpenDroneIdOperatorId`](#opendroneidoperatorid) | 4 | 0 |  |
| [`OpenDroneIdSelfId`](#opendroneidselfid) | 4 | 0 |  |
| [`OpenDroneIdSystem`](#opendroneidsystem) | 13 | 0 |  |
| [`OrbTest`](#orbtest) | 2 | 0 |  |
| [`OrbTestLarge`](#orbtestlarge) | 3 | 0 |  |
| [`OrbTestMedium`](#orbtestmedium) | 3 | 1 |  |
| [`OrbitStatus`](#orbitstatus) | 7 | 6 | ORBIT_YAW_BEHAVIOUR |
| [`ParameterResetRequest`](#parameterresetrequest) | 3 | 1 | ParameterResetRequest : Used by the primary to reset one or all parame… |
| [`ParameterSetUsedRequest`](#parametersetusedrequest) | 2 | 1 | ParameterSetUsedRequest : Used by a remote to update the used flag for… |
| [`ParameterSetValueRequest`](#parametersetvaluerequest) | 4 | 1 | ParameterSetValueRequest : Used by a remote or primary to update the v… |
| [`ParameterSetValueResponse`](#parametersetvalueresponse) | 3 | 1 | ParameterSetValueResponse : Response to a set value request by either … |
| [`ParameterUpdate`](#parameterupdate) | 9 | 0 | This message is used to notify the system about one or more parameter … |
| [`Ping`](#ping) | 7 | 0 |  |
| [`PositionControllerLandingStatus`](#positioncontrollerlandingstatus) | 4 | 5 |  |
| [`PositionControllerStatus`](#positioncontrollerstatus) | 9 | 0 |  |
| [`PositionSetpoint`](#positionsetpoint) | 20 | 8 | this file is only used in the position_setpoint triple as a dependency |
| [`PositionSetpointTriplet`](#positionsetpointtriplet) | 4 | 0 | Global position setpoint triplet in WGS84 coordinates. This are the th… |
| [`PowerButtonState`](#powerbuttonstate) | 2 | 4 | power button state notification message |
| [`PowerMonitor`](#powermonitor) | 12 | 0 | power monitor message |
| [`PpsCapture`](#ppscapture) | 3 | 0 |  |
| [`PurePursuitStatus`](#purepursuitstatus) | 6 | 0 | Pure pursuit status |
| [`PwmInput`](#pwminput) | 4 | 0 |  |
| [`Px4ioStatus`](#px4iostatus) | 32 | 0 |  |
| [`QshellReq`](#qshellreq) | 4 | 1 |  |
| [`QshellRetval`](#qshellretval) | 3 | 0 |  |
| [`RadioStatus`](#radiostatus) | 8 | 0 |  |
| [`RateCtrlStatus`](#ratectrlstatus) | 4 | 0 |  |
| [`RcChannels`](#rcchannels) | 8 | 31 |  |
| [`RcParameterMap`](#rcparametermap) | 8 | 2 |  |
| [`RoverAttitudeSetpoint`](#roverattitudesetpoint) | 2 | 0 | Rover Attitude Setpoint |
| [`RoverAttitudeStatus`](#roverattitudestatus) | 3 | 0 | Rover Attitude Status |
| [`RoverPositionSetpoint`](#roverpositionsetpoint) | 6 | 0 | Rover Position Setpoint |
| [`RoverRateSetpoint`](#roverratesetpoint) | 2 | 0 | Rover Rate setpoint |
| [`RoverRateStatus`](#roverratestatus) | 4 | 0 | Rover Rate Status |
| [`RoverSpeedSetpoint`](#roverspeedsetpoint) | 3 | 0 | Rover Speed Setpoint |
| [`RoverSpeedStatus`](#roverspeedstatus) | 7 | 0 | Rover Velocity Status |
| [`RoverSteeringSetpoint`](#roversteeringsetpoint) | 2 | 0 | Rover Steering setpoint |
| [`RoverThrottleSetpoint`](#roverthrottlesetpoint) | 3 | 0 | Rover Throttle setpoint |
| [`Rpm`](#rpm) | 3 | 0 |  |
| [`RtlStatus`](#rtlstatus) | 6 | 5 |  |
| [`RtlTimeEstimate`](#rtltimeestimate) | 4 | 0 |  |
| [`SatelliteInfo`](#satelliteinfo) | 8 | 1 |  |
| [`SensorAccel`](#sensoraccel) | 10 | 1 |  |
| [`SensorAccelFifo`](#sensoraccelfifo) | 9 | 0 |  |
| [`SensorAirflow`](#sensorairflow) | 5 | 0 |  |
| [`SensorBaro`](#sensorbaro) | 6 | 1 |  |
| [`SensorCombined`](#sensorcombined) | 10 | 4 | Sensor readings in SI-unit form. These fields are scaled and offset-co… |
| [`SensorCorrection`](#sensorcorrection) | 25 | 0 | Sensor corrections in SI-unit form for the voted sensor |
| [`SensorGnssRelative`](#sensorgnssrelative) | 21 | 0 | GNSS relative positioning information in NED frame. The NED frame is d… |
| [`SensorGnssStatus`](#sensorgnssstatus) | 7 | 0 | Gnss quality indicators |
| [`SensorGps`](#sensorgps) | 37 | 31 | GPS position in WGS84 coordinates. the field 'timestamp' is for the po… |
| [`SensorGyro`](#sensorgyro) | 10 | 1 |  |
| [`SensorGyroFft`](#sensorgyrofft) | 11 | 0 |  |
| [`SensorGyroFifo`](#sensorgyrofifo) | 9 | 1 |  |
| [`SensorHygrometer`](#sensorhygrometer) | 5 | 0 |  |
| [`SensorMag`](#sensormag) | 8 | 1 |  |
| [`SensorOpticalFlow`](#sensoropticalflow) | 15 | 4 |  |
| [`SensorPreflightMag`](#sensorpreflightmag) | 2 | 0 | Pre-flight sensor check metrics. The topic will not be updated when th… |
| [`SensorSelection`](#sensorselection) | 3 | 0 | Sensor ID's for the voted sensors output on the sensor_combined topic.… |
| [`SensorUwb`](#sensoruwb) | 21 | 0 | UWB distance contains the distance information measured by an ultra-wi… |
| [`SensorsStatus`](#sensorsstatus) | 8 | 0 | Sensor check metrics. This will be zero for a sensor that's primary or… |
| [`SensorsStatusImu`](#sensorsstatusimu) | 11 | 0 | Sensor check metrics. This will be zero for a sensor that's primary or… |
| [`SystemPower`](#systempower) | 14 | 8 |  |
| [`TakeoffStatus`](#takeoffstatus) | 3 | 6 | Status of the takeoff state machine currently just available for multi… |
| [`TaskStackInfo`](#taskstackinfo) | 3 | 1 | stack information for a single running process |
| [`TecsStatus`](#tecsstatus) | 25 | 0 |  |
| [`TelemetryStatus`](#telemetrystatus) | 38 | 6 |  |
| [`TiltrotorExtraControls`](#tiltrotorextracontrols) | 3 | 0 |  |
| [`TimesyncStatus`](#timesyncstatus) | 6 | 3 |  |
| [`TrajectorySetpoint6dof`](#trajectorysetpoint6dof) | 7 | 0 | Trajectory setpoint in NED frame Input to position controller. |
| [`TransponderReport`](#transponderreport) | 15 | 29 |  |
| [`TuneControl`](#tunecontrol) | 7 | 25 | This message is used to control the tunes, when the tune_id is set to … |
| [`UavcanParameterRequest`](#uavcanparameterrequest) | 8 | 8 | UAVCAN-MAVLink parameter bridge request type |
| [`UavcanParameterValue`](#uavcanparametervalue) | 8 | 0 | UAVCAN-MAVLink parameter bridge response type |
| [`UlogStream`](#ulogstream) | 6 | 2 | Message to stream ULog data from the logger. Corresponds to the LOGGIN… |
| [`UlogStreamAck`](#ulogstreamack) | 2 | 2 | Ack a previously sent ulog_stream message that had the NEED_ACK flag s… |
| [`VehicleAcceleration`](#vehicleacceleration) | 3 | 0 |  |
| [`VehicleAirData`](#vehicleairdata) | 9 | 0 | Vehicle air data Data from the currently selected barometer (plus ambi… |
| [`VehicleAngularAccelerationSetpoint`](#vehicleangularaccelerationsetpoint) | 3 | 0 |  |
| [`VehicleAttitudeSetpointV0`](#vehicleattitudesetpointv0) | 6 | 1 |  |
| [`VehicleConstraints`](#vehicleconstraints) | 4 | 0 | Local setpoint constraints in NED frame setting something to NaN means… |
| [`VehicleImu`](#vehicleimu) | 12 | 3 | IMU readings in SI-unit form. |
| [`VehicleImuStatus`](#vehicleimustatus) | 20 | 0 |  |
| [`VehicleLocalPositionSetpoint`](#vehiclelocalpositionsetpoint) | 11 | 0 | Local position setpoint in NED frame Telemetry of PID position control… |
| [`VehicleLocalPositionV0`](#vehiclelocalpositionv0) | 52 | 4 | Fused local position in NED. The coordinate system origin is the vehic… |
| [`VehicleMagnetometer`](#vehiclemagnetometer) | 5 | 0 |  |
| [`VehicleOpticalFlow`](#vehicleopticalflow) | 11 | 0 | Optical flow in XYZ body frame in SI units. |
| [`VehicleOpticalFlowVel`](#vehicleopticalflowvel) | 11 | 0 |  |
| [`VehicleRoi`](#vehicleroi) | 8 | 6 | Vehicle Region Of Interest (ROI) |
| [`VehicleStatusV0`](#vehiclestatusv0) | 41 | 68 | Encodes the system state of the vehicle published by commander |
| [`VehicleThrustSetpoint`](#vehiclethrustsetpoint) | 3 | 0 |  |
| [`VehicleTorqueSetpoint`](#vehicletorquesetpoint) | 3 | 0 |  |
| [`VelocityLimits`](#velocitylimits) | 4 | 0 | Velocity and yaw rate limits for a multicopter position slow mode only |
| [`WheelEncoders`](#wheelencoders) | 3 | 0 |  |
| [`YawEstimatorStatus`](#yawestimatorstatus) | 9 | 0 |  |

---

# 逐則定義

## ActuatorMotors

對外契約 · 主題名 `actuator_motors`

Motor control message Normalised thrust setpoint for up to 12 motors. Published by the vehicle's allocation and consumed by the ESC protocol drivers e.g. PWM, DSHOT, UAVCAN.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `timestamp_sample` | `uint64` | [us] Sampling timestamp of the data this control response is based on |
| `reversible_flags` | `uint16` | [-] Bitset indicating which motors are configured to be reversible |
| `control` | `float32[12]` | [@range -1, 1] Normalized thrust. where 1 means maximum positive thrust, -1 maximum negative (if not supported by the output, <0 maps to NaN). NaN maps to disarmed (stop the motors) |

常數:`MESSAGE_VERSION=0`、`ACTUATOR_FUNCTION_MOTOR1=101`、`NUM_CONTROLS=12`

## ActuatorServos

對外契約 · 主題名 `actuator_servos`

Servo control message Normalised output setpoint for up to 8 servos. Published by the vehicle's allocation and consumed by the actuator output drivers.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `timestamp_sample` | `uint64` | [us] Sampling timestamp of the data this control response is based on |
| `control` | `float32[8]` | [-] [@range -1, 1] Normalized output. 1 means maximum positive position. -1 maximum negative position (if not supported by the output, <0 maps to NaN). NaN maps to disarmed. |

常數:`MESSAGE_VERSION=0`、`NUM_CONTROLS=8`

## AirspeedValidated

對外契約 · 主題名 `airspeed_validated`

Validated airspeed Provides information about airspeed (indicated, true, calibrated) and the source of the data. Used by controllers, estimators and for airspeed reporting to operator.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `indicated_airspeed_m_s` | `float32` | [m/s] [@invalid NaN] Indicated airspeed (IAS) |
| `calibrated_airspeed_m_s` | `float32` | [m/s] [@invalid NaN] Calibrated airspeed (CAS) |
| `true_airspeed_m_s` | `float32` | [m/s] [@invalid NaN] True airspeed (TAS) |
| `airspeed_source` | `int8` | [@enum SOURCE] Source of currently published airspeed values |
| `calibrated_ground_minus_wind_m_s` | `float32` | [m/s] [@invalid NaN] CAS calculated from groundspeed - windspeed, where windspeed is estimated based on a zero-sideslip assumption |
| `calibraded_airspeed_synth_m_s` | `float32` | [m/s] [@invalid NaN] Synthetic airspeed |
| `airspeed_derivative_filtered` | `float32` | [m/s^2] Filtered indicated airspeed derivative |
| `throttle_filtered` | `float32` | [-] Filtered fixed-wing throttle |
| `pitch_filtered` | `float32` | [rad] Filtered pitch |

常數:`MESSAGE_VERSION=1`、`SOURCE_DISABLED=-1`、`SOURCE_GROUND_MINUS_WIND=0`、`SOURCE_SENSOR_1=1`、`SOURCE_SENSOR_2=2`、`SOURCE_SENSOR_3=3`、`SOURCE_SYNTHETIC=4`

## ArmingCheckReply

對外契約 · 主題名 `arming_check_reply`

Arming check reply This is a response to an ArmingCheckRequest message sent by the FMU to an external component, such as a ROS 2 navigation mode. The response contains the current set of external mode requirements, and a queue of events indicating recent failures to set the mode (which the FMU may then forward to a ground station). The request is sent regularly to all registered ROS modes, even while armed, so that the FMU always knows and can forward the current state. Note that the external component is identified by its registration_id, which is allocated to the component during registration (arming_check_id in RegisterExtComponentReply). The message is not used by internal/FMU components, as their mode requirements are known at compile time.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start. |
| `request_id` | `uint8` | [-] Id of ArmingCheckRequest for which this is a response |
| `registration_id` | `uint8` | [-] Id of external component emitting this response |
| `health_component_index` | `uint8` | [@enum HEALTH_COMPONENT_INDEX] |
| `health_component_is_present` | `bool` | Unused. Intended for use with health events interface (health_component_t in events.json) |
| `health_component_warning` | `bool` | Unused. Intended for use with health events interface (health_component_t in events.json) |
| `health_component_error` | `bool` | Unused. Intended for use with health events interface (health_component_t in events.json) |
| `can_arm_and_run` | `bool` | True if the component can arm. For navigation mode components, true if the component can arm in the mode or switch to the mode when already armed |
| `num_events` | `uint8` | Number of queued failure messages (Event) in the events field |
| `events` | `Event[5]` | Arming failure reasons (Queue of events to report to GCS) |
| `mode_req_angular_velocity` | `bool` | Requires angular velocity estimate (e.g. from gyroscope) |
| `mode_req_attitude` | `bool` | Requires an attitude estimate |
| `mode_req_local_alt` | `bool` | Requires a local altitude estimate |
| `mode_req_local_position` | `bool` | Requires a local position estimate |
| `mode_req_local_position_relaxed` | `bool` | Requires a more relaxed global position estimate |
| `mode_req_global_position` | `bool` | Requires a global position estimate |
| `mode_req_global_position_relaxed` | `bool` | Requires a relaxed global position estimate |
| `mode_req_mission` | `bool` | Requires an uploaded mission |
| `mode_req_home_position` | `bool` | Requires a home position (such as RTL/Return mode) |
| `mode_req_prevent_arming` | `bool` | Prevent arming (such as in Land mode) |
| `mode_req_manual_control` | `bool` | Requires a manual controller |

常數:`MESSAGE_VERSION=1`、`HEALTH_COMPONENT_INDEX_NONE=0`、`ORB_QUEUE_LENGTH=4`

## ArmingCheckRequest

對外契約 · 主題名 `arming_check_request`

Arming check request Broadcast message to request arming checks be reported by all registered components, such as external ROS 2 navigation modes. All registered components should respond with an ArmingCheckReply message that indicates their current mode requirements, and any arming failure information. The request is sent regularly, even while armed, so that the FMU always knows the current arming state for external modes, and can forward it to ground stations. The reply will include the published request_id, allowing correlation of all arming check information for a particular request. The reply will also include the registration_id for each external component, provided to it during the registration process (RegisterExtComponentReply).

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `request_id` | `uint8` | [-] Id of this request. Allows correlation with associated ArmingCheckReply messages. |
| `valid_registrations_mask` | `uint32` | [-] Bitmask of valid registration ID's (the bit is also cleared if flagged as unresponsive) |

常數:`MESSAGE_VERSION=1`

## BatteryStatus

對外契約 · 主題名 `battery_status`

Battery status Battery status information for up to 4 battery instances. These are populated from power module and smart battery device drivers, and one battery updated from MAVLink. Battery instance information is also logged and streamed in MAVLink telemetry.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `connected` | `bool` | Whether or not a battery is connected. For power modules this is based on a voltage threshold. |
| `voltage_v` | `float32` | [V] [@invalid 0] Battery voltage |
| `current_a` | `float32` | [A] [@invalid -1] Battery current |
| `current_average_a` | `float32` | [A] [@invalid -1] Battery current average (for FW average in level flight) |
| `discharged_mah` | `float32` | [mAh] [@invalid -1] Discharged amount |
| `remaining` | `float32` | [@range 0,1] [@invalid -1] Remaining capacity |
| `scale` | `float32` | [-] [@range 1,] [@invalid -1] Scaling factor to compensate for lower actuation power caused by voltage sag |
| `time_remaining_s` | `float32` | [s] [@invalid NaN] Predicted time remaining until battery is empty under previous averaged load |
| `temperature` | `float32` | [°C] [@invalid NaN] Temperature of the battery |
| `cell_count` | `uint8` | [-] [@invalid 0] Number of cells |
| `source` | `uint8` | [@enum SOURCE] Battery source |
| `priority` | `uint8` | [-] Zero based priority is the connection on the Power Controller V1..Vn AKA BrickN-1 |
| `capacity` | `uint16` | [mAh] Capacity of the battery when fully charged |
| `cycle_count` | `uint16` | [-] Number of discharge cycles the battery has experienced |
| `average_time_to_empty` | `uint16` | [minutes] Predicted remaining battery capacity based on the average rate of discharge |
| `manufacture_date` | `uint16` | [-] Manufacture date, part of serial number of the battery pack. Formatted as: Day + Month×32 + (Year–1980)×512 |
| `state_of_health` | `uint16` | [%] [@range 0, 100] State of health. FullChargeCapacity/DesignCapacity |
| `max_error` | `uint16` | [%] [@range 1, 100] Max error, expected margin of error in the state-of-charge calculation |
| `id` | `uint8` | [-] ID number of a battery. Should be unique and consistent for the lifetime of a vehicle. 1-indexed |
| `interface_error` | `uint16` | [-] Interface error counter |
| `voltage_cell_v` | `float32[14]` | [V] [@invalid 0] Battery individual cell voltages |
| `max_cell_voltage_delta` | `float32` | [V] Max difference between individual cell voltages |
| `is_powering_off` | `bool` | Power off event imminent indication, false if unknown |
| `is_required` | `bool` | Set if the battery is explicitly required before arming |
| `warning` | `uint8` | [@enum WARNING STATE] Current battery warning |
| `faults` | `uint16` | [@enum FAULT] Smart battery supply status/fault flags (bitmask) for health indication |
| `full_charge_capacity_wh` | `float32` | [Wh] Compensated battery capacity |
| `remaining_capacity_wh` | `float32` | [Wh] Compensated battery capacity remaining |
| `over_discharge_count` | `uint16` | [-] Number of battery overdischarge |
| `nominal_voltage` | `float32` | [V] Nominal voltage of the battery pack |
| `internal_resistance_estimate` | `float32` | [Ohm] Internal resistance per cell estimate |
| `ocv_estimate` | `float32` | [V] Open circuit voltage estimate |
| `ocv_estimate_filtered` | `float32` | [V] Filtered open circuit voltage estimate |
| `volt_based_soc_estimate` | `float32` | [-] [@range 0, 1] Normalized volt based state of charge estimate |
| `voltage_prediction` | `float32` | [V] Predicted voltage |
| `prediction_error` | `float32` | [V] Prediction error |
| `estimation_covariance_norm` | `float32` | [-] Norm of the covariance matrix |

常數:`MESSAGE_VERSION=1`、`MAX_INSTANCES=3`、`SOURCE_POWER_MODULE=0`、`SOURCE_EXTERNAL=1`、`SOURCE_ESCS=2`、`WARNING_NONE=0`、`WARNING_LOW=1`、`WARNING_CRITICAL=2`、`WARNING_EMERGENCY=3`、`WARNING_FAILED=4`、`STATE_UNHEALTHY=6`、`STATE_CHARGING=7`、`FAULT_DEEP_DISCHARGE=0`、`FAULT_SPIKES=1`、`FAULT_CELL_FAIL=2`、`FAULT_OVER_CURRENT=3`、`FAULT_OVER_TEMPERATURE=4`、`FAULT_UNDER_TEMPERATURE=5`、`FAULT_INCOMPATIBLE_VOLTAGE=6`、`FAULT_INCOMPATIBLE_FIRMWARE=7`、`FAULT_INCOMPATIBLE_MODEL=8`、`FAULT_HARDWARE_FAILURE=9`、`FAULT_FAILED_TO_ARM=10`、`FAULT_COUNT=11`

## ConfigOverrides

對外契約 · 主題名 `config_overrides`、`config_overrides_request`

Configurable overrides by (external) modes or mode executors

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `disable_auto_disarm` | `bool` | Prevent the drone from automatically disarming after landing (if configured) |
| `defer_failsafes` | `bool` | Defer all failsafes that can be deferred (until the flag is cleared) |
| `defer_failsafes_timeout_s` | `int16` | Maximum time a failsafe can be deferred. 0 = system default, -1 = no timeout |
| `source_type` | `int8` |  |
| `source_id` | `uint8` | ID depending on source_type |

常數:`MESSAGE_VERSION=0`、`SOURCE_TYPE_MODE=0`、`SOURCE_TYPE_MODE_EXECUTOR=1`、`ORB_QUEUE_LENGTH=4`

## Event

對外契約 · 主題名 `event`

Events interface

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `id` | `uint32` | Event ID |
| `event_sequence` | `uint16` | Event sequence number |
| `arguments` | `uint8[25]` | (optional) arguments, depend on event id |
| `log_levels` | `uint8` | Log levels: 4 bits MSB: internal, 4 bits LSB: external |

常數:`MESSAGE_VERSION=1`、`ORB_QUEUE_LENGTH=16`

## FixedWingLateralSetpoint

對外契約 · 主題名 `fixed_wing_lateral_setpoint`

Fixed Wing Lateral Setpoint message Used by the fw_lateral_longitudinal_control module At least one of course, airspeed_direction, or lateral_acceleration must be finite.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `course` | `float32` | [rad] [@range -pi, pi] Desired direction of travel over ground w.r.t (true) North. NAN if not controlled directly. |
| `airspeed_direction` | `float32` | [rad] [@range -pi, pi] Desired horizontal angle of airspeed vector w.r.t. (true) North. Same as vehicle heading if in the absence of sideslip. NAN if not controlled directly, takes precedence over course if finite. |
| `lateral_acceleration` | `float32` | [m/s^2] [FRD] Lateral acceleration setpoint. NAN if not controlled directly, used as feedforward if either course setpoint or airspeed_direction is finite. |

常數:`MESSAGE_VERSION=0`

## FixedWingLongitudinalSetpoint

對外契約 · 主題名 `fixed_wing_longitudinal_setpoint`

Fixed Wing Longitudinal Setpoint message Used by the fw_lateral_longitudinal_control module If pitch_direct and throttle_direct are not both finite, then the controller relies on altitude/height_rate and equivalent_airspeed to control vertical motion. If both altitude and height_rate are NAN, the controller maintains the current altitude.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `altitude` | `float32` | [m] Altitude setpoint AMSL, not controlled directly if NAN or if height_rate is finite |
| `height_rate` | `float32` | [m/s] [ENU] Scalar height rate setpoint. NAN if not controlled directly |
| `equivalent_airspeed` | `float32` | [m/s] [@range 0, inf] Scalar equivalent airspeed setpoint. NAN if system default should be used |
| `pitch_direct` | `float32` | [rad] [@range -pi, pi] [FRD] NAN if not controlled, overrides total energy controller |
| `throttle_direct` | `float32` | [norm] [@range 0,1] NAN if not controlled, overrides total energy controller |

常數:`MESSAGE_VERSION=0`

## GotoSetpoint

對外契約 · 主題名 `goto_setpoint`

Position and (optional) heading setpoints with corresponding speed constraints Setpoints are intended as inputs to position and heading smoothers, respectively Setpoints do not need to be kinematically consistent Optional heading setpoints may be specified as controlled by the respective flag Unset optional setpoints are not controlled Unset optional constraints default to vehicle specifications

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `position` | `float32[3]` | [m] NED local world frame |
| `flag_control_heading` | `bool` | true if heading is to be controlled |
| `heading` | `float32` | (optional) [rad] [-pi,pi] from North |
| `flag_set_max_horizontal_speed` | `bool` | true if setting a non-default horizontal speed limit |
| `max_horizontal_speed` | `float32` | (optional) [m/s] maximum speed (absolute) in the NE-plane |
| `flag_set_max_vertical_speed` | `bool` | true if setting a non-default vertical speed limit |
| `max_vertical_speed` | `float32` | (optional) [m/s] maximum speed (absolute) in the D-axis |
| `flag_set_max_heading_rate` | `bool` | true if setting a non-default heading rate limit |
| `max_heading_rate` | `float32` | (optional) [rad/s] maximum heading rate (absolute) |

常數:`MESSAGE_VERSION=0`

## HomePosition

對外契約 · 主題名 `home_position`

GPS home position in WGS84 coordinates.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `lat` | `float64` | Latitude in degrees |
| `lon` | `float64` | Longitude in degrees |
| `alt` | `float32` | Altitude in meters (AMSL) |
| `x` | `float32` | X coordinate in meters |
| `y` | `float32` | Y coordinate in meters |
| `z` | `float32` | Z coordinate in meters |
| `roll` | `float32` | Pitch angle in radians |
| `pitch` | `float32` | Roll angle in radians |
| `yaw` | `float32` | Yaw angle in radians |
| `valid_alt` | `bool` | true when the altitude has been set |
| `valid_hpos` | `bool` | true when the latitude and longitude have been set |
| `valid_lpos` | `bool` | true when the local position (xyz) has been set |
| `manual_home` | `bool` | true when home position was set manually |
| `update_count` | `uint32` | update counter of the home position |

常數:`MESSAGE_VERSION=1`

## LateralControlConfiguration

對外契約 · 主題名 `lateral_control_configuration`

Fixed Wing Lateral Control Configuration message Used by the fw_lateral_longitudinal_control module to constrain FixedWingLateralSetpoint messages.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `lateral_accel_max` | `float32` | [m/s^2] currently maps to a maximum roll angle, accel_max = tan(roll_max) * GRAVITY |

常數:`MESSAGE_VERSION=0`

## LongitudinalControlConfiguration

對外契約 · 主題名 `longitudinal_control_configuration`

Fixed Wing Longitudinal Control Configuration message Used by the fw_lateral_longitudinal_control module and TECS to constrain FixedWingLongitudinalSetpoint messages and configure the resultant setpoints.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `pitch_min` | `float32` | [rad][@range -pi, pi] defaults to FW_P_LIM_MIN if NAN. |
| `pitch_max` | `float32` | [rad][@range -pi, pi] defaults to FW_P_LIM_MAX if NAN. |
| `throttle_min` | `float32` | [norm] [@range 0,1] deaults to FW_THR_MIN if NAN. |
| `throttle_max` | `float32` | [norm] [@range 0,1] defaults to FW_THR_MAX if NAN. |
| `climb_rate_target` | `float32` | [m/s] target climbrate to change altitude. Defaults to FW_T_CLIMB_MAX if NAN. Not used if height_rate is directly set in FixedWingLongitudinalSetpoint. |
| `sink_rate_target` | `float32` | [m/s] target sinkrate to change altitude. Defaults to FW_T_SINK_MAX if NAN. Not used if height_rate is directly set in FixedWingLongitudinalSetpoint. |
| `speed_weight` | `float32` | [@range 0,2], 0=pitch controls altitude only, 2=pitch controls airspeed only |
| `enforce_low_height_condition` | `bool` | [boolean] if true, the altitude controller is configured with an alternative timeconstant for tighter altitude tracking |
| `disable_underspeed_protection` | `bool` | [boolean] if true, underspeed handling is disabled in the altitude controller |

常數:`MESSAGE_VERSION=0`

## ManualControlSetpoint

對外契約 · 主題名 `manual_control_setpoint`、`manual_control_input`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `valid` | `bool` |  |
| `data_source` | `uint8` |  |
| `roll` | `float32` | move right,   positive roll rotation,  right side down |
| `pitch` | `float32` | move forward, negative pitch rotation, nose down |
| `yaw` | `float32` | positive yaw rotation,   clockwise when seen top down |
| `throttle` | `float32` | move up,      positive thrust,         -1 is minimum available 0% or -100% +1 is 100% thrust |
| `flaps` | `float32` | position of flaps switch/knob/lever [-1, 1] |
| `aux1` | `float32` |  |
| `aux2` | `float32` |  |
| `aux3` | `float32` |  |
| `aux4` | `float32` |  |
| `aux5` | `float32` |  |
| `aux6` | `float32` |  |
| `sticks_moving` | `bool` |  |
| `buttons` | `uint16` | From uint16 buttons field of Mavlink manual_control message |

常數:`MESSAGE_VERSION=0`、`SOURCE_UNKNOWN=0`、`SOURCE_RC=1`、`SOURCE_MAVLINK_0=2`、`SOURCE_MAVLINK_1=3`、`SOURCE_MAVLINK_2=4`、`SOURCE_MAVLINK_3=5`、`SOURCE_MAVLINK_4=6`、`SOURCE_MAVLINK_5=7`

## ModeCompleted

對外契約 · 主題名 `mode_completed`

Mode completion result, published by an active mode. The possible values of nav_state are defined in the VehicleStatus msg. Note that this is not always published (e.g. when a user switches modes or on failsafe activation)

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `result` | `uint8` | One of RESULT_* |
| `nav_state` | `uint8` | Source mode (values in VehicleStatus) |

常數:`MESSAGE_VERSION=0`、`RESULT_SUCCESS=0`、`RESULT_FAILURE_OTHER=100`

## RegisterExtComponentReply

對外契約 · 主題名 `register_ext_component_reply`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `request_id` | `uint64` | ID from the request |
| `name` | `char[25]` | name from the request |
| `px4_ros2_api_version` | `uint16` |  |
| `success` | `bool` |  |
| `arming_check_id` | `int8` | arming check registration ID (-1 if invalid) |
| `mode_id` | `int8` | assigned mode ID (-1 if invalid) |
| `mode_executor_id` | `int8` | assigned mode executor ID (-1 if invalid) |

常數:`MESSAGE_VERSION=0`、`ORB_QUEUE_LENGTH=2`

## RegisterExtComponentRequest

對外契約 · 主題名 `register_ext_component_request`

Request to register an external component

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `request_id` | `uint64` | ID, set this to a random value |
| `name` | `char[25]` | either the requested mode name, or component name |
| `px4_ros2_api_version` | `uint16` | Set to LATEST_PX4_ROS2_API_VERSION |
| `register_arming_check` | `bool` |  |
| `register_mode` | `bool` | registering a mode also requires arming_check to be set |
| `register_mode_executor` | `bool` | registering an executor also requires a mode to be registered (which is the owned mode by the executor) |
| `enable_replace_internal_mode` | `bool` | set to true if an internal mode should be replaced |
| `replace_internal_mode` | `uint8` | vehicle_status::NAVIGATION_STATE_* |
| `activate_mode_immediately` | `bool` | switch to the registered mode (can only be set in combination with an executor) |

常數:`MESSAGE_VERSION=0`、`LATEST_PX4_ROS2_API_VERSION=1`、`ORB_QUEUE_LENGTH=2`

## TrajectorySetpoint

對外契約 · 主題名 `trajectory_setpoint`

Trajectory setpoint in NED frame Input to PID position controller. Needs to be kinematically consistent and feasible for smooth flight. setting a value to NaN means the state should not be controlled

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `position` | `float32[3]` | in meters |
| `velocity` | `float32[3]` | in meters/second |
| `acceleration` | `float32[3]` | in meters/second^2 |
| `jerk` | `float32[3]` | in meters/second^3 (for logging only) |
| `yaw` | `float32` | euler angle of desired attitude in radians -PI..+PI |
| `yawspeed` | `float32` | angular velocity around NED frame z-axis in radians/second |

常數:`MESSAGE_VERSION=0`

## UnregisterExtComponent

對外契約 · 主題名 `unregister_ext_component`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `name` | `char[25]` | either the mode name, or component name |
| `arming_check_id` | `int8` | arming check registration ID (-1 if not registered) |
| `mode_id` | `int8` | assigned mode ID (-1 if not registered) |
| `mode_executor_id` | `int8` | assigned mode executor ID (-1 if not registered) |

常數:`MESSAGE_VERSION=0`

## VehicleAngularVelocity

對外契約 · 主題名 `vehicle_angular_velocity`、`vehicle_angular_velocity_groundtruth`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | timestamp of the data sample on which this message is based (microseconds) |
| `xyz` | `float32[3]` | Bias corrected angular velocity about the FRD body frame XYZ-axis in rad/s |
| `xyz_derivative` | `float32[3]` | angular acceleration about the FRD body frame XYZ-axis in rad/s^2 |

常數:`MESSAGE_VERSION=0`

## VehicleAttitude

對外契約 · 主題名 `vehicle_attitude`、`vehicle_attitude_groundtruth`、`external_ins_attitude`、`estimator_attitude`

This is similar to the mavlink message ATTITUDE_QUATERNION, but for onboard use The quaternion uses the Hamilton convention, and the order is q(w, x, y, z)

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `q` | `float32[4]` | Quaternion rotation from the FRD body frame to the NED earth frame |
| `delta_q_reset` | `float32[4]` | Amount by which quaternion has changed during last reset |
| `quat_reset_counter` | `uint8` | Quaternion reset counter |

常數:`MESSAGE_VERSION=0`

## VehicleAttitudeSetpoint

對外契約 · 主題名 `vehicle_attitude_setpoint`、`mc_virtual_attitude_setpoint`、`fw_virtual_attitude_setpoint`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `yaw_sp_move_rate` | `float32` | rad/s (commanded by user) |
| `q_d` | `float32[4]` | Desired quaternion for quaternion control |
| `thrust_body` | `float32[3]` | Normalized thrust command in body FRD frame [-1,1] |

常數:`MESSAGE_VERSION=1`

## VehicleCommand

對外契約 · 主題名 `vehicle_command`、`gimbal_v1_command`、`vehicle_command_mode_executor`

Vehicle Command uORB message. Used for commanding a mission / action / etc. Follows the MAVLink COMMAND_INT / COMMAND_LONG definition

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start. |
| `param1` | `float32` | Parameter 1, as defined by MAVLink uint16 VEHICLE_CMD enum. |
| `param2` | `float32` | Parameter 2, as defined by MAVLink uint16 VEHICLE_CMD enum. |
| `param3` | `float32` | Parameter 3, as defined by MAVLink uint16 VEHICLE_CMD enum. |
| `param4` | `float32` | Parameter 4, as defined by MAVLink uint16 VEHICLE_CMD enum. |
| `param5` | `float64` | Parameter 5, as defined by MAVLink uint16 VEHICLE_CMD enum. |
| `param6` | `float64` | Parameter 6, as defined by MAVLink uint16 VEHICLE_CMD enum. |
| `param7` | `float32` | Parameter 7, as defined by MAVLink uint16 VEHICLE_CMD enum. |
| `command` | `uint32` | Command ID. |
| `target_system` | `uint8` | System which should execute the command. |
| `target_component` | `uint8` | Component which should execute the command, 0 for all components. |
| `source_system` | `uint8` | System sending the command. |
| `source_component` | `uint16` | Component / mode executor sending the command. |
| `confirmation` | `uint8` | 0: First transmission of this command. 1-255: Confirmation transmissions (e.g. for kill command). |
| `from_external` | `bool` |  |

常數:`MESSAGE_VERSION=0`、`VEHICLE_CMD_CUSTOM_0=0`、`VEHICLE_CMD_CUSTOM_1=1`、`VEHICLE_CMD_CUSTOM_2=2`、`VEHICLE_CMD_NAV_WAYPOINT=16`、`VEHICLE_CMD_NAV_LOITER_UNLIM=17`、`VEHICLE_CMD_NAV_LOITER_TURNS=18`、`VEHICLE_CMD_NAV_LOITER_TIME=19`、`VEHICLE_CMD_NAV_RETURN_TO_LAUNCH=20`、`VEHICLE_CMD_NAV_LAND=21`、`VEHICLE_CMD_NAV_TAKEOFF=22`、`VEHICLE_CMD_NAV_PRECLAND=23`、`VEHICLE_CMD_DO_ORBIT=34`、`VEHICLE_CMD_DO_FIGUREEIGHT=35`、`VEHICLE_CMD_NAV_ROI=80`、`VEHICLE_CMD_NAV_PATHPLANNING=81`、`VEHICLE_CMD_NAV_VTOL_TAKEOFF=84`、`VEHICLE_CMD_NAV_VTOL_LAND=85`、`VEHICLE_CMD_NAV_GUIDED_LIMITS=90`、`VEHICLE_CMD_NAV_GUIDED_MASTER=91`、`VEHICLE_CMD_NAV_DELAY=93`、`VEHICLE_CMD_NAV_LAST=95`、`VEHICLE_CMD_CONDITION_DELAY=112`、`VEHICLE_CMD_CONDITION_CHANGE_ALT=113`、`VEHICLE_CMD_CONDITION_DISTANCE=114`、`VEHICLE_CMD_CONDITION_YAW=115`、`VEHICLE_CMD_CONDITION_LAST=159`、`VEHICLE_CMD_CONDITION_GATE=4501`、`VEHICLE_CMD_DO_SET_MODE=176`、`VEHICLE_CMD_DO_JUMP=177`、`VEHICLE_CMD_DO_CHANGE_SPEED=178`、`VEHICLE_CMD_DO_SET_HOME=179`、`VEHICLE_CMD_DO_SET_PARAMETER=180`、`VEHICLE_CMD_DO_SET_RELAY=181`、`VEHICLE_CMD_DO_REPEAT_RELAY=182`、`VEHICLE_CMD_DO_REPEAT_SERVO=184`、`VEHICLE_CMD_DO_FLIGHTTERMINATION=185`、`VEHICLE_CMD_DO_CHANGE_ALTITUDE=186`、`VEHICLE_CMD_DO_SET_ACTUATOR=187`、`VEHICLE_CMD_DO_LAND_START=189`、`VEHICLE_CMD_DO_GO_AROUND=191`、`VEHICLE_CMD_DO_REPOSITION=192`、`VEHICLE_CMD_DO_PAUSE_CONTINUE=193`、`VEHICLE_CMD_DO_SET_ROI_LOCATION=195`、`VEHICLE_CMD_DO_SET_ROI_WPNEXT_OFFSET=196`、`VEHICLE_CMD_DO_SET_ROI_NONE=197`、`VEHICLE_CMD_DO_CONTROL_VIDEO=200`、`VEHICLE_CMD_DO_SET_ROI=201`、`VEHICLE_CMD_DO_DIGICAM_CONTROL=203`、`VEHICLE_CMD_DO_MOUNT_CONFIGURE=204`、`VEHICLE_CMD_DO_MOUNT_CONTROL=205`、`VEHICLE_CMD_DO_SET_CAM_TRIGG_DIST=206`、`VEHICLE_CMD_DO_FENCE_ENABLE=207`、`VEHICLE_CMD_DO_PARACHUTE=208`、`VEHICLE_CMD_DO_MOTOR_TEST=209`、`VEHICLE_CMD_DO_INVERTED_FLIGHT=210`、`VEHICLE_CMD_DO_GRIPPER=211`、`VEHICLE_CMD_DO_SET_CAM_TRIGG_INTERVAL=214`、`VEHICLE_CMD_DO_MOUNT_CONTROL_QUAT=220`、`VEHICLE_CMD_DO_GUIDED_MASTER=221`、`VEHICLE_CMD_DO_GUIDED_LIMITS=222`、`VEHICLE_CMD_DO_LAST=240`、`VEHICLE_CMD_PREFLIGHT_CALIBRATION=241`、`PREFLIGHT_CALIBRATION_TEMPERATURE_CALIBRATION=3`、`VEHICLE_CMD_PREFLIGHT_SET_SENSOR_OFFSETS=242`、`VEHICLE_CMD_PREFLIGHT_UAVCAN=243`、`VEHICLE_CMD_PREFLIGHT_STORAGE=245`、`VEHICLE_CMD_PREFLIGHT_REBOOT_SHUTDOWN=246`、`VEHICLE_CMD_OBLIQUE_SURVEY=260`、`VEHICLE_CMD_DO_SET_STANDARD_MODE=262`、`VEHICLE_CMD_GIMBAL_DEVICE_INFORMATION=283`、`VEHICLE_CMD_MISSION_START=300`、`VEHICLE_CMD_ACTUATOR_TEST=310`、`VEHICLE_CMD_CONFIGURE_ACTUATOR=311`、`VEHICLE_CMD_COMPONENT_ARM_DISARM=400`、`VEHICLE_CMD_RUN_PREARM_CHECKS=401`、`VEHICLE_CMD_INJECT_FAILURE=420`、`VEHICLE_CMD_START_RX_PAIR=500`、`VEHICLE_CMD_REQUEST_MESSAGE=512`、`VEHICLE_CMD_REQUEST_CAMERA_INFORMATION=521`、`VEHICLE_CMD_SET_CAMERA_MODE=530`、`VEHICLE_CMD_SET_CAMERA_ZOOM=531`、`VEHICLE_CMD_SET_CAMERA_FOCUS=532`、`VEHICLE_CMD_EXTERNAL_ATTITUDE_ESTIMATE=620`、`VEHICLE_CMD_DO_GIMBAL_MANAGER_PITCHYAW=1000`、`VEHICLE_CMD_DO_GIMBAL_MANAGER_CONFIGURE=1001`、`VEHICLE_CMD_IMAGE_START_CAPTURE=2000`、`VEHICLE_CMD_DO_TRIGGER_CONTROL=2003`、`VEHICLE_CMD_VIDEO_START_CAPTURE=2500`、`VEHICLE_CMD_VIDEO_STOP_CAPTURE=2501`、`VEHICLE_CMD_LOGGING_START=2510`、`VEHICLE_CMD_LOGGING_STOP=2511`、`VEHICLE_CMD_CONTROL_HIGH_LATENCY=2600`、`VEHICLE_CMD_DO_VTOL_TRANSITION=3000`、`VEHICLE_CMD_ARM_AUTHORIZATION_REQUEST=3001`、`VEHICLE_CMD_PAYLOAD_PREPARE_DEPLOY=30001`、`VEHICLE_CMD_PAYLOAD_CONTROL_DEPLOY=30002`、`VEHICLE_CMD_FIXED_MAG_CAL_YAW=42006`、`VEHICLE_CMD_DO_WINCH=42600`、`VEHICLE_CMD_EXTERNAL_POSITION_ESTIMATE=43003`、`VEHICLE_CMD_EXTERNAL_WIND_ESTIMATE=43004`、`VEHICLE_CMD_PX4_INTERNAL_START=65537`、`VEHICLE_CMD_SET_GPS_GLOBAL_ORIGIN=100000`、`VEHICLE_CMD_SET_NAV_STATE=100001`、`VEHICLE_MOUNT_MODE_RETRACT=0`、`VEHICLE_MOUNT_MODE_NEUTRAL=1`、`VEHICLE_MOUNT_MODE_MAVLINK_TARGETING=2`、`VEHICLE_MOUNT_MODE_RC_TARGETING=3`、`VEHICLE_MOUNT_MODE_GPS_POINT=4`、`VEHICLE_MOUNT_MODE_ENUM_END=5`、`VEHICLE_ROI_NONE=0`、`VEHICLE_ROI_WPNEXT=1`、`VEHICLE_ROI_WPINDEX=2`、`VEHICLE_ROI_LOCATION=3`、`VEHICLE_ROI_TARGET=4`、`VEHICLE_ROI_ENUM_END=5`、`PARACHUTE_ACTION_DISABLE=0`、`PARACHUTE_ACTION_ENABLE=1`、`PARACHUTE_ACTION_RELEASE=2`、`FAILURE_UNIT_SENSOR_GYRO=0`、`FAILURE_UNIT_SENSOR_ACCEL=1`、`FAILURE_UNIT_SENSOR_MAG=2`、`FAILURE_UNIT_SENSOR_BARO=3`、`FAILURE_UNIT_SENSOR_GPS=4`、`FAILURE_UNIT_SENSOR_OPTICAL_FLOW=5`、`FAILURE_UNIT_SENSOR_VIO=6`、`FAILURE_UNIT_SENSOR_DISTANCE_SENSOR=7`、`FAILURE_UNIT_SENSOR_AIRSPEED=8`、`FAILURE_UNIT_SYSTEM_BATTERY=100`、`FAILURE_UNIT_SYSTEM_MOTOR=101`、`FAILURE_UNIT_SYSTEM_SERVO=102`、`FAILURE_UNIT_SYSTEM_AVOIDANCE=103`、`FAILURE_UNIT_SYSTEM_RC_SIGNAL=104`、`FAILURE_UNIT_SYSTEM_MAVLINK_SIGNAL=105`、`FAILURE_TYPE_OK=0`、`FAILURE_TYPE_OFF=1`、`FAILURE_TYPE_STUCK=2`、`FAILURE_TYPE_GARBAGE=3`、`FAILURE_TYPE_WRONG=4`、`FAILURE_TYPE_SLOW=5`、`FAILURE_TYPE_DELAYED=6`、`FAILURE_TYPE_INTERMITTENT=7`、`SPEED_TYPE_AIRSPEED=0`、`SPEED_TYPE_GROUNDSPEED=1`、`SPEED_TYPE_CLIMB_SPEED=2`、`SPEED_TYPE_DESCEND_SPEED=3`、`ORBIT_YAW_BEHAVIOUR_HOLD_FRONT_TO_CIRCLE_CENTER=0`、`ORBIT_YAW_BEHAVIOUR_HOLD_INITIAL_HEADING=1`、`ORBIT_YAW_BEHAVIOUR_UNCONTROLLED=2`、`ORBIT_YAW_BEHAVIOUR_HOLD_FRONT_TANGENT_TO_CIRCLE=3`、`ORBIT_YAW_BEHAVIOUR_RC_CONTROLLED=4`、`ORBIT_YAW_BEHAVIOUR_UNCHANGED=5`、`ARMING_ACTION_DISARM=0`、`ARMING_ACTION_ARM=1`、`GRIPPER_ACTION_RELEASE=0`、`GRIPPER_ACTION_GRAB=1`、`ORB_QUEUE_LENGTH=8`、`COMPONENT_MODE_EXECUTOR_START=1000`

## VehicleCommandAck

對外契約 · 主題名 `vehicle_command_ack`

Vehicle Command Ackonwledgement uORB message. Used for acknowledging the vehicle command being received. Follows the MAVLink COMMAND_ACK message definition

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `command` | `uint32` | Command that is being acknowledged |
| `result` | `uint8` | Command result |
| `result_param1` | `uint8` | Also used as progress[%], it can be set with the reason why the command was denied, or the progress percentage when result is MAV_RESULT_IN_PROGRESS |
| `result_param2` | `int32` | Additional parameter of the result, example: which parameter of MAV_CMD_NAV_WAYPOINT caused it to be denied. |
| `target_system` | `uint8` |  |
| `target_component` | `uint16` | Target component / mode executor |
| `from_external` | `bool` | Indicates if the command came from an external source |

常數:`MESSAGE_VERSION=0`、`VEHICLE_CMD_RESULT_ACCEPTED=0`、`VEHICLE_CMD_RESULT_TEMPORARILY_REJECTED=1`、`VEHICLE_CMD_RESULT_DENIED=2`、`VEHICLE_CMD_RESULT_UNSUPPORTED=3`、`VEHICLE_CMD_RESULT_FAILED=4`、`VEHICLE_CMD_RESULT_IN_PROGRESS=5`、`VEHICLE_CMD_RESULT_CANCELLED=6`、`ARM_AUTH_DENIED_REASON_GENERIC=0`、`ARM_AUTH_DENIED_REASON_NONE=1`、`ARM_AUTH_DENIED_REASON_INVALID_WAYPOINT=2`、`ARM_AUTH_DENIED_REASON_TIMEOUT=3`、`ARM_AUTH_DENIED_REASON_AIRSPACE_IN_USE=4`、`ARM_AUTH_DENIED_REASON_BAD_WEATHER=5`、`ORB_QUEUE_LENGTH=4`

## VehicleControlMode

對外契約 · 主題名 `vehicle_control_mode`、`config_control_setpoints`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `flag_armed` | `bool` | synonym for actuator_armed.armed |
| `flag_multicopter_position_control_enabled` | `bool` |  |
| `flag_control_manual_enabled` | `bool` | true if manual input is mixed in |
| `flag_control_auto_enabled` | `bool` | true if onboard autopilot should act |
| `flag_control_offboard_enabled` | `bool` | true if offboard control should be used |
| `flag_control_position_enabled` | `bool` | true if position is controlled |
| `flag_control_velocity_enabled` | `bool` | true if horizontal velocity (implies direction) is controlled |
| `flag_control_altitude_enabled` | `bool` | true if altitude is controlled |
| `flag_control_climb_rate_enabled` | `bool` | true if climb rate is controlled |
| `flag_control_acceleration_enabled` | `bool` | true if acceleration is controlled |
| `flag_control_attitude_enabled` | `bool` | true if attitude stabilization is mixed in |
| `flag_control_rates_enabled` | `bool` | true if rates are stabilized |
| `flag_control_allocation_enabled` | `bool` | true if control allocation is enabled |
| `flag_control_termination_enabled` | `bool` | true if flighttermination is enabled |
| `source_id` | `uint8` | Mode ID (nav_state) |

常數:`MESSAGE_VERSION=0`

## VehicleGlobalPosition

對外契約 · 主題名 `vehicle_global_position`、`vehicle_global_position_groundtruth`、`external_ins_global_position`、`estimator_global_position`、`aux_global_position`

Fused global position in WGS84. This struct contains global position estimation. It is not the raw GPS measurement (@see vehicle_gps_position). This topic is usually published by the position estimator, which will take more sources of information into account than just GPS, e.g. control inputs of the vehicle in a Kalman-filter implementation.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `lat` | `float64` | Latitude, (degrees) |
| `lon` | `float64` | Longitude, (degrees) |
| `alt` | `float32` | Altitude AMSL, (meters) |
| `alt_ellipsoid` | `float32` | Altitude above ellipsoid, (meters) |
| `lat_lon_valid` | `bool` |  |
| `alt_valid` | `bool` |  |
| `delta_alt` | `float32` | Reset delta for altitude |
| `delta_terrain` | `float32` | Reset delta for terrain |
| `lat_lon_reset_counter` | `uint8` | Counter for reset events on horizontal position coordinates |
| `alt_reset_counter` | `uint8` | Counter for reset events on altitude |
| `terrain_reset_counter` | `uint8` | Counter for reset events on terrain |
| `eph` | `float32` | Standard deviation of horizontal position error, (metres) |
| `epv` | `float32` | Standard deviation of vertical position error, (metres) |
| `terrain_alt` | `float32` | Terrain altitude WGS84, (metres) |
| `terrain_alt_valid` | `bool` | Terrain altitude estimate is valid |
| `dead_reckoning` | `bool` | True if this position is estimated through dead-reckoning |

常數:`MESSAGE_VERSION=0`

## VehicleLandDetected

對外契約 · 主題名 `vehicle_land_detected`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `freefall` | `bool` | true if vehicle is currently in free-fall |
| `ground_contact` | `bool` | true if vehicle has ground contact but is not landed (1. stage) |
| `maybe_landed` | `bool` | true if the vehicle might have landed (2. stage) |
| `landed` | `bool` | true if vehicle is currently landed on the ground (3. stage) |
| `in_ground_effect` | `bool` | indicates if from the perspective of the landing detector the vehicle might be in ground effect (baro). This flag will become true if the vehicle is not moving horizontally and is descending (crude assumption that user is landing). |
| `in_descend` | `bool` |  |
| `has_low_throttle` | `bool` |  |
| `vertical_movement` | `bool` |  |
| `horizontal_movement` | `bool` |  |
| `rotational_movement` | `bool` |  |
| `close_to_ground_or_skipped_check` | `bool` |  |
| `at_rest` | `bool` |  |

常數:`MESSAGE_VERSION=0`

## VehicleLocalPosition

對外契約 · 主題名 `vehicle_local_position`、`vehicle_local_position_groundtruth`、`external_ins_local_position`、`estimator_local_position`

Fused local position in NED. The coordinate system origin is the vehicle position at the time when the EKF2-module was started.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `xy_valid` | `bool` | true if x and y are valid |
| `z_valid` | `bool` | true if z is valid |
| `v_xy_valid` | `bool` | true if vx and vy are valid |
| `v_z_valid` | `bool` | true if vz is valid |
| `x` | `float32` | North position in NED earth-fixed frame, (metres) |
| `y` | `float32` | East position in NED earth-fixed frame, (metres) |
| `z` | `float32` | Down position (negative altitude) in NED earth-fixed frame, (metres) |
| `delta_xy` | `float32[2]` | Amount of lateral shift of position estimate in latest reset (in x and y) [m] |
| `xy_reset_counter` | `uint8` | Index of latest lateral position estimate reset |
| `delta_z` | `float32` | Amount of vertical shift of position estimate in latest reset [m] |
| `z_reset_counter` | `uint8` | Index of latest vertical position estimate reset |
| `vx` | `float32` | North velocity in NED earth-fixed frame, (metres/sec) |
| `vy` | `float32` | East velocity in NED earth-fixed frame, (metres/sec) |
| `vz` | `float32` | Down velocity in NED earth-fixed frame, (metres/sec) |
| `z_deriv` | `float32` | Down position time derivative in NED earth-fixed frame, (metres/sec) |
| `delta_vxy` | `float32[2]` | Amount of lateral shift of velocity estimate in latest reset (in x and y) [m/s] |
| `vxy_reset_counter` | `uint8` | Index of latest vertical velocity estimate reset |
| `delta_vz` | `float32` | Amount of vertical shift of velocity estimate in latest reset [m/s] |
| `vz_reset_counter` | `uint8` | Index of latest vertical velocity estimate reset |
| `ax` | `float32` | North velocity derivative in NED earth-fixed frame, (metres/sec^2) |
| `ay` | `float32` | East velocity derivative in NED earth-fixed frame, (metres/sec^2) |
| `az` | `float32` | Down velocity derivative in NED earth-fixed frame, (metres/sec^2) |
| `heading` | `float32` | Euler yaw angle transforming the tangent plane relative to NED earth-fixed frame, -PI..+PI,  (radians) |
| `heading_var` | `float32` |  |
| `unaided_heading` | `float32` | Same as heading but generated by integrating corrected gyro data only |
| `delta_heading` | `float32` | Heading delta caused by latest heading reset [rad] |
| `heading_reset_counter` | `uint8` | Index of latest heading reset |
| `heading_good_for_control` | `bool` |  |
| `tilt_var` | `float32` |  |
| `xy_global` | `bool` | true if position (x, y) has a valid global reference (ref_lat, ref_lon) |
| `z_global` | `bool` | true if z has a valid global reference (ref_alt) |
| `ref_timestamp` | `uint64` | Time when reference position was set since system start, (microseconds) |
| `ref_lat` | `float64` | Reference point latitude, (degrees) |
| `ref_lon` | `float64` | Reference point longitude, (degrees) |
| `ref_alt` | `float32` | Reference altitude AMSL, (metres) |
| `dist_bottom_valid` | `bool` | true if distance to bottom surface is valid |
| `dist_bottom` | `float32` | Distance from from bottom surface to ground, (metres) |
| `dist_bottom_var` | `float32` | terrain estimate variance (m^2) |
| `delta_dist_bottom` | `float32` | Amount of vertical shift of dist bottom estimate in latest reset [m] |
| `dist_bottom_reset_counter` | `uint8` | Index of latest dist bottom estimate reset |
| `dist_bottom_sensor_bitfield` | `uint8` | bitfield indicating what type of sensor is used to estimate dist_bottom |
| `eph` | `float32` | Standard deviation of horizontal position error, (metres) |
| `epv` | `float32` | Standard deviation of vertical position error, (metres) |
| `evh` | `float32` | Standard deviation of horizontal velocity error, (metres/sec) |
| `evv` | `float32` | Standard deviation of vertical velocity error, (metres/sec) |
| `dead_reckoning` | `bool` | True if this position is estimated through dead-reckoning |
| `vxy_max` | `float32` | maximum horizontal speed (meters/sec) |
| `vz_max` | `float32` | maximum vertical speed (meters/sec) |
| `hagl_min` | `float32` | minimum height above ground level (meters) |
| `hagl_max_z` | `float32` | maximum height above ground level for z-control (meters) |
| `hagl_max_xy` | `float32` | maximum height above ground level for xy-control (meters) |

常數:`MESSAGE_VERSION=1`、`DIST_BOTTOM_SENSOR_NONE=0`、`DIST_BOTTOM_SENSOR_RANGE=1`、`DIST_BOTTOM_SENSOR_FLOW=2`

## VehicleOdometry

對外契約 · 主題名 `vehicle_odometry`、`vehicle_mocap_odometry`、`vehicle_visual_odometry`、`estimator_odometry`

Vehicle odometry data Fits ROS REP 147 for aerial vehicles

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `timestamp_sample` | `uint64` | [us] Timestamp sample |
| `pose_frame` | `uint8` | [@enum POSE_FRAME] Position and orientation frame of reference |
| `position` | `float32[3]` | [m] [@frame local frame] [@invalid NaN If invalid/unknown] Position. Origin is position of GC at startup. |
| `q` | `float32[4]` | [-] [@invalid NaN First value if invalid/unknown] Attitude (expressed as a quaternion) relative to pose reference frame at current location. Follows the Hamiltonian convention (w, x, y, z, right-handed, passive rotations from body to world) |
| `velocity_frame` | `uint8` | [@enum VELOCITY_FRAME] Reference frame of the velocity data |
| `velocity` | `float32[3]` | [m/s] [@frame @velocity_frame] [@invalid NaN If invalid/unknown] Velocity. |
| `angular_velocity` | `float32[3]` | [rad/s] [@frame @VELOCITY_FRAME_BODY_FRD] [@invalid NaN If invalid/unknown] Angular velocity in body-fixed frame |
| `position_variance` | `float32[3]` | [m^2] Variance of position error |
| `orientation_variance` | `float32[3]` | [rad^2] Variance of orientation/attitude error (expressed in body frame) |
| `velocity_variance` | `float32[3]` | [m^2/s^2] Variance of velocity error |
| `reset_counter` | `uint8` | [-] Reset counter. Counts reset events on attitude, velocity and position. |
| `quality` | `int8` | [-] [@invalid 0] Quality. Unused. |

常數:`MESSAGE_VERSION=0`、`POSE_FRAME_UNKNOWN=0`、`POSE_FRAME_NED=1`、`POSE_FRAME_FRD=2`、`VELOCITY_FRAME_UNKNOWN=0`、`VELOCITY_FRAME_NED=1`、`VELOCITY_FRAME_FRD=2`、`VELOCITY_FRAME_BODY_FRD=3`

## VehicleRatesSetpoint

對外契約 · 主題名 `vehicle_rates_setpoint`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `roll` | `float32` | [rad/s] roll rate setpoint |
| `pitch` | `float32` | [rad/s] pitch rate setpoint |
| `yaw` | `float32` | [rad/s] yaw rate setpoint |
| `thrust_body` | `float32[3]` | Normalized thrust command in body NED frame [-1,1] |
| `reset_integral` | `bool` | Reset roll/pitch/yaw integrals (navigation logic change) |

常數:`MESSAGE_VERSION=0`

## VehicleStatus

對外契約 · 主題名 `vehicle_status`

Encodes the system state of the vehicle published by commander

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `armed_time` | `uint64` | Arming timestamp (microseconds) |
| `takeoff_time` | `uint64` | Takeoff timestamp (microseconds) |
| `arming_state` | `uint8` |  |
| `latest_arming_reason` | `uint8` |  |
| `latest_disarming_reason` | `uint8` |  |
| `nav_state_timestamp` | `uint64` | time when current nav_state activated |
| `nav_state_user_intention` | `uint8` | Mode that the user selected (might be different from nav_state in a failsafe situation) |
| `nav_state` | `uint8` | Currently active mode |
| `executor_in_charge` | `uint8` | Current mode executor in charge (0=Autopilot) |
| `valid_nav_states_mask` | `uint32` | Bitmask for all valid nav_state values |
| `can_set_nav_states_mask` | `uint32` | Bitmask for all modes that a user can select |
| `failure_detector_status` | `uint16` |  |
| `hil_state` | `uint8` |  |
| `vehicle_type` | `uint8` |  |
| `failsafe` | `bool` | true if system is in failsafe state (e.g.:RTL, Hover, Terminate, ...) |
| `failsafe_and_user_took_over` | `bool` | true if system is in failsafe state but the user took over control |
| `failsafe_defer_state` | `uint8` | one of FAILSAFE_DEFER_STATE_* |
| `gcs_connection_lost` | `bool` | datalink to GCS lost |
| `gcs_connection_lost_counter` | `uint8` | counts unique GCS connection lost events |
| `high_latency_data_link_lost` | `bool` | Set to true if the high latency data link (eg. RockBlock Iridium 9603 telemetry module) is lost |
| `is_vtol` | `bool` | True if the system is VTOL capable |
| `is_vtol_tailsitter` | `bool` | True if the system performs a 90° pitch down rotation during transition from MC to FW |
| `in_transition_mode` | `bool` | True if VTOL is doing a transition |
| `in_transition_to_fw` | `bool` | True if VTOL is doing a transition from MC to FW |
| `system_type` | `uint8` | system type, contains mavlink MAV_TYPE |
| `system_id` | `uint8` | system id, contains MAVLink's system ID field |
| `component_id` | `uint8` | subsystem / component id, contains MAVLink's component ID field |
| `safety_button_available` | `bool` | Set to true if a safety button is connected |
| `safety_off` | `bool` | Set to true if safety is off |
| `power_input_valid` | `bool` | set if input power is valid |
| `usb_connected` | `bool` | set to true (never cleared) once telemetry received from usb link |
| `open_drone_id_system_present` | `bool` |  |
| `open_drone_id_system_healthy` | `bool` |  |
| `parachute_system_present` | `bool` |  |
| `parachute_system_healthy` | `bool` |  |
| `rc_calibration_in_progress` | `bool` |  |
| `calibration_enabled` | `bool` |  |
| `pre_flight_checks_pass` | `bool` | true if all checks necessary to arm pass |

常數:`MESSAGE_VERSION=1`、`ARMING_STATE_DISARMED=1`、`ARMING_STATE_ARMED=2`、`ARM_DISARM_REASON_TRANSITION_TO_STANDBY=0`、`ARM_DISARM_REASON_STICK_GESTURE=1`、`ARM_DISARM_REASON_RC_SWITCH=2`、`ARM_DISARM_REASON_COMMAND_INTERNAL=3`、`ARM_DISARM_REASON_COMMAND_EXTERNAL=4`、`ARM_DISARM_REASON_MISSION_START=5`、`ARM_DISARM_REASON_SAFETY_BUTTON=6`、`ARM_DISARM_REASON_AUTO_DISARM_LAND=7`、`ARM_DISARM_REASON_AUTO_DISARM_PREFLIGHT=8`、`ARM_DISARM_REASON_KILL_SWITCH=9`、`ARM_DISARM_REASON_LOCKDOWN=10`、`ARM_DISARM_REASON_FAILURE_DETECTOR=11`、`ARM_DISARM_REASON_SHUTDOWN=12`、`ARM_DISARM_REASON_UNIT_TEST=13`、`NAVIGATION_STATE_MANUAL=0`、`NAVIGATION_STATE_ALTCTL=1`、`NAVIGATION_STATE_POSCTL=2`、`NAVIGATION_STATE_AUTO_MISSION=3`、`NAVIGATION_STATE_AUTO_LOITER=4`、`NAVIGATION_STATE_AUTO_RTL=5`、`NAVIGATION_STATE_POSITION_SLOW=6`、`NAVIGATION_STATE_FREE5=7`、`NAVIGATION_STATE_ALTITUDE_CRUISE=8`、`NAVIGATION_STATE_FREE3=9`、`NAVIGATION_STATE_ACRO=10`、`NAVIGATION_STATE_FREE2=11`、`NAVIGATION_STATE_DESCEND=12`、`NAVIGATION_STATE_TERMINATION=13`、`NAVIGATION_STATE_OFFBOARD=14`、`NAVIGATION_STATE_STAB=15`、`NAVIGATION_STATE_FREE1=16`、`NAVIGATION_STATE_AUTO_TAKEOFF=17`、`NAVIGATION_STATE_AUTO_LAND=18`、`NAVIGATION_STATE_AUTO_FOLLOW_TARGET=19`、`NAVIGATION_STATE_AUTO_PRECLAND=20`、`NAVIGATION_STATE_ORBIT=21`、`NAVIGATION_STATE_AUTO_VTOL_TAKEOFF=22`、`NAVIGATION_STATE_EXTERNAL1=23`、`NAVIGATION_STATE_EXTERNAL2=24`、`NAVIGATION_STATE_EXTERNAL3=25`、`NAVIGATION_STATE_EXTERNAL4=26`、`NAVIGATION_STATE_EXTERNAL5=27`、`NAVIGATION_STATE_EXTERNAL6=28`、`NAVIGATION_STATE_EXTERNAL7=29`、`NAVIGATION_STATE_EXTERNAL8=30`、`NAVIGATION_STATE_MAX=31`、`FAILURE_NONE=0`、`FAILURE_ROLL=1`、`FAILURE_PITCH=2`、`FAILURE_ALT=4`、`FAILURE_EXT=8`、`FAILURE_ARM_ESC=16`、`FAILURE_BATTERY=32`、`FAILURE_IMBALANCED_PROP=64`、`FAILURE_MOTOR=128`、`HIL_STATE_OFF=0`、`HIL_STATE_ON=1`、`VEHICLE_TYPE_UNSPECIFIED=0`、`VEHICLE_TYPE_ROTARY_WING=1`、`VEHICLE_TYPE_FIXED_WING=2`、`VEHICLE_TYPE_ROVER=3`、`FAILSAFE_DEFER_STATE_DISABLED=0`、`FAILSAFE_DEFER_STATE_ENABLED=1`、`FAILSAFE_DEFER_STATE_WOULD_FAILSAFE=2`

## VtolVehicleStatus

對外契約 · 主題名 `vtol_vehicle_status`

VEHICLE_VTOL_STATE, should match 1:1 MAVLinks's MAV_VTOL_STATE

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `vehicle_vtol_state` | `uint8` | current state of the vtol, see VEHICLE_VTOL_STATE |
| `fixed_wing_system_failure` | `bool` | vehicle in fixed-wing system failure failsafe mode (after quad-chute) |

常數:`MESSAGE_VERSION=0`、`VEHICLE_VTOL_STATE_UNDEFINED=0`、`VEHICLE_VTOL_STATE_TRANSITION_TO_FW=1`、`VEHICLE_VTOL_STATE_TRANSITION_TO_MC=2`、`VEHICLE_VTOL_STATE_MC=3`、`VEHICLE_VTOL_STATE_FW=4`

## Wind

對外契約 · 主題名 `wind`、`estimator_wind`

Wind estimate (from EKF2) Contains the system-wide estimate of horizontal wind velocity and its variance. Published by the navigation filter (EKF2) for use by other flight modules and libraries.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `timestamp_sample` | `uint64` | [us] Timestamp of the raw data |
| `windspeed_north` | `float32` | [m/s] Wind component in north / X direction |
| `windspeed_east` | `float32` | [m/s] Wind component in east / Y direction |
| `variance_north` | `float32` | [(m/s)^2] [@invalid 0 if not estimated] Wind estimate error variance in north / X direction |
| `variance_east` | `float32` | [(m/s)^2] [@invalid 0 if not estimated] Wind estimate error variance in east / Y direction |
| `tas_innov` | `float32` | [m/s] True airspeed innovation |
| `tas_innov_var` | `float32` | [(m/s)^2] True airspeed innovation variance |
| `beta_innov` | `float32` | [rad] Sideslip measurement innovation |
| `beta_innov_var` | `float32` | [rad^2] Sideslip measurement innovation variance |

常數:`MESSAGE_VERSION=0`

## ActionRequest

內部訊息 · 主題名 `action_request`

Action request for the vehicle's main state Message represents actions requested by a PX4 internal component towards the main state machine such as a request to arm or switch mode. It allows mapping triggers from various external interfaces like RC channels or MAVLink to cause an action. Request are published by `manual_control` and subscribed by the `commander` and `vtol_att_control` modules.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `action` | `uint8` | [@enum ACTION] Requested action |
| `source` | `uint8` | [@enum SOURCE] Request trigger type, such as a switch, button or gesture |
| `mode` | `uint8` | Requested mode. Only applies when `action` is `ACTION_SWITCH_MODE`. Values for this field are defined by the `vehicle_status_s::NAVIGATION_STATE_*` enumeration. |

常數:`ACTION_DISARM=0`、`ACTION_ARM=1`、`ACTION_TOGGLE_ARMING=2`、`ACTION_UNKILL=3`、`ACTION_KILL=4`、`ACTION_SWITCH_MODE=5`、`ACTION_VTOL_TRANSITION_TO_MULTICOPTER=6`、`ACTION_VTOL_TRANSITION_TO_FIXEDWING=7`、`ACTION_TERMINATION=8`、`SOURCE_STICK_GESTURE=0`、`SOURCE_RC_SWITCH=1`、`SOURCE_RC_BUTTON=2`、`SOURCE_RC_MODE_SLOT=3`

## ActuatorArmed

內部訊息 · 主題名 `actuator_armed`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `armed` | `bool` | Set to true if system is armed |
| `prearmed` | `bool` | Set to true if the actuator safety is disabled but motors are not armed |
| `ready_to_arm` | `bool` | Set to true if system is ready to be armed |
| `lockdown` | `bool` | Set to true if actuators are forced to being disabled (due to emergency or HIL) |
| `kill` | `bool` | Set to true if manual throttle kill switch is engaged |
| `termination` | `bool` | Send out failsafe (by default same as disarmed) output |
| `in_esc_calibration_mode` | `bool` | IO/FMU should ignore messages from the actuator controls topics |

## ActuatorControlsStatus

內部訊息 · 主題名 `actuator_controls_status_0`、`actuator_controls_status_1`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `control_power` | `float32[3]` |  |

## ActuatorOutputs

內部訊息 · 主題名 `actuator_outputs`、`actuator_outputs_sim`、`actuator_outputs_debug`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `noutputs` | `uint32` | valid outputs |
| `output` | `float32[16]` | output data, in natural output units |

常數:`NUM_ACTUATOR_OUTPUTS=16`、`NUM_ACTUATOR_OUTPUT_GROUPS=4`

## ActuatorServosTrim

內部訊息 · 主題名 `actuator_servos_trim`

Servo trims, added as offset to servo outputs

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `trim` | `float32[8]` | range: [-1, 1] |

常數:`NUM_CONTROLS=8`

## ActuatorTest

內部訊息 · 主題名 `actuator_test`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `action` | `uint8` | one of ACTION_* |
| `function` | `uint16` | actuator output function |
| `value` | `float32` | range: [-1, 1], where 1 means maximum positive output, |
| `timeout_ms` | `uint32` | timeout in ms after which to exit test mode (if 0, do not time out) |

常數:`ACTION_RELEASE_CONTROL=0`、`ACTION_DO_CONTROL=1`、`FUNCTION_MOTOR1=101`、`MAX_NUM_MOTORS=12`、`FUNCTION_SERVO1=201`、`MAX_NUM_SERVOS=8`、`ORB_QUEUE_LENGTH=16`

## AdcReport

內部訊息 · 主題名 `adc_report`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `channel_id` | `int16[12]` | ADC channel IDs, negative for non-existent, TODO: should be kept same as array index |
| `raw_data` | `int32[12]` | ADC channel raw value, accept negative value, valid if channel ID is positive |
| `resolution` | `uint32` | ADC channel resolution |
| `v_ref` | `float32` | ADC channel voltage reference, use to calculate LSB voltage(lsb=scale/resolution) |

## Airspeed

內部訊息 · 主題名 `airspeed`

Airspeed data from sensors This is published by airspeed sensor drivers, CAN airspeed sensors, simulators. It is subscribed by the airspeed selector module, which validates the data from multiple sensors and passes on a single estimation to the EKF, controllers and telemetry providers.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `timestamp_sample` | `uint64` | [us] Timestamp of the raw data |
| `indicated_airspeed_m_s` | `float32` | [m/s] Indicated airspeed |
| `true_airspeed_m_s` | `float32` | [m/s] True airspeed |
| `confidence` | `float32` | [@range 0,1] Confidence value for this sensor |

## AirspeedValidatedV0

內部訊息 · 主題名 `airspeed_validated_v0`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `indicated_airspeed_m_s` | `float32` | indicated airspeed in m/s (IAS), set to NAN if invalid |
| `calibrated_airspeed_m_s` | `float32` | calibrated airspeed in m/s (CAS, accounts for instrumentation errors), set to NAN if invalid |
| `true_airspeed_m_s` | `float32` | true filtered airspeed in m/s (TAS), set to NAN if invalid |
| `calibrated_ground_minus_wind_m_s` | `float32` | CAS calculated from groundspeed - windspeed, where windspeed is estimated based on a zero-sideslip assumption, set to NAN if invalid |
| `true_ground_minus_wind_m_s` | `float32` | TAS calculated from groundspeed - windspeed, where windspeed is estimated based on a zero-sideslip assumption, set to NAN if invalid |
| `airspeed_sensor_measurement_valid` | `bool` | True if data from at least one airspeed sensor is declared valid. |
| `selected_airspeed_index` | `int8` | 1-3: airspeed sensor index, 0: groundspeed-windspeed, -1: airspeed invalid |
| `airspeed_derivative_filtered` | `float32` | filtered indicated airspeed derivative [m/s/s] |
| `throttle_filtered` | `float32` | filtered fixed-wing throttle [-] |
| `pitch_filtered` | `float32` | filtered pitch [rad] |

常數:`MESSAGE_VERSION=0`

## AirspeedWind

內部訊息 · 主題名 `airspeed_wind`

Wind estimate (from airspeed_selector) Contains wind estimation and airspeed innovation information estimated by the WindEstimator in the airspeed selector module. This message is published by the airspeed selector for debugging purposes, and is not subscribed to by any other modules.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `timestamp_sample` | `uint64` | [us] Timestamp of the raw data |
| `windspeed_north` | `float32` | [m/s] Wind component in north / X direction |
| `windspeed_east` | `float32` | [m/s] Wind component in east / Y direction |
| `variance_north` | `float32` | [(m/s)^2] [@invalid 0 if not estimated] Wind estimate error variance in north / X direction |
| `variance_east` | `float32` | [(m/s)^2] [@invalid 0 if not estimated] Wind estimate error variance in east / Y direction |
| `tas_innov` | `float32` | [m/s] True airspeed innovation |
| `tas_innov_var` | `float32` | [m/s] True airspeed innovation variance |
| `tas_scale_raw` | `float32` | Estimated true airspeed scale factor (not validated) |
| `tas_scale_raw_var` | `float32` | True airspeed scale factor variance |
| `tas_scale_validated` | `float32` | Estimated true airspeed scale factor after validation |
| `beta_innov` | `float32` | [rad] Sideslip measurement innovation |
| `beta_innov_var` | `float32` | [rad^2] Sideslip measurement innovation variance |
| `source` | `uint8` | source of wind estimate |

常數:`SOURCE_AS_BETA_ONLY=0`、`SOURCE_AS_SENSOR_1=1`、`SOURCE_AS_SENSOR_2=2`、`SOURCE_AS_SENSOR_3=3`

## ArmingCheckReplyV0

內部訊息 · 主題名 `arming_check_reply_v0`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `request_id` | `uint8` |  |
| `registration_id` | `uint8` |  |
| `health_component_index` | `uint8` | HEALTH_COMPONENT_INDEX_* |
| `health_component_is_present` | `bool` |  |
| `health_component_warning` | `bool` |  |
| `health_component_error` | `bool` |  |
| `can_arm_and_run` | `bool` | whether arming is possible, and if it's a navigation mode, if it can run |
| `num_events` | `uint8` |  |
| `events` | `EventV0[5]` |  |
| `mode_req_angular_velocity` | `bool` |  |
| `mode_req_attitude` | `bool` |  |
| `mode_req_local_alt` | `bool` |  |
| `mode_req_local_position` | `bool` |  |
| `mode_req_local_position_relaxed` | `bool` |  |
| `mode_req_global_position` | `bool` |  |
| `mode_req_mission` | `bool` |  |
| `mode_req_home_position` | `bool` |  |
| `mode_req_prevent_arming` | `bool` |  |
| `mode_req_manual_control` | `bool` |  |

常數:`MESSAGE_VERSION=0`、`HEALTH_COMPONENT_INDEX_NONE=0`、`ORB_QUEUE_LENGTH=4`

## ArmingCheckRequestV0

內部訊息 · 主題名 `arming_check_request_v0`

Arming check request. Broadcast message to request arming checks be reported by all registered components, such as external ROS 2 navigation modes. All registered components should respond with an ArmingCheckReply message that indicates their current mode requirements, and any arming failure information. The request is sent regularly, even while armed, so that the FMU always knows the current arming state for external modes, and can forward it to ground stations. The reply will include the published request_id, allowing correlation of all arming check information for a particular request. The reply will also include the registration_id for each external component, provided to it during the registration process (RegisterExtComponentReply).

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start. |
| `request_id` | `uint8` | Id of this request. Allows correlation with associated ArmingCheckReply messages. |

常數:`MESSAGE_VERSION=0`

## AutotuneAttitudeControlStatus

內部訊息 · 主題名 `autotune_attitude_control_status`

Autotune attitude control status This message is published by the fw_autotune_attitude_control and mc_autotune_attitude_control modules when the user engages autotune, and is subscribed to by the respective attitude controllers to command rate setpoints. The rate_sp field is consumed by the controllers, while the remaining fields (model coefficients, gains, filters, and autotune state) are used for logging and debugging.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `coeff` | `float32[5]` | [-] Coefficients of the identified discrete-time model |
| `coeff_var` | `float32[5]` | [-] Coefficients' variance of the identified discrete-time model |
| `fitness` | `float32` | [-] Fitness of the parameter estimate |
| `innov` | `float32` | [rad/s] Innovation (residual error between model and measured output) |
| `dt_model` | `float32` | [s] Model sample time used for identification |
| `kc` | `float32` | [-] Proportional rate-loop gain (ideal form) |
| `ki` | `float32` | [-] Integral rate-loop gain (ideal form) |
| `kd` | `float32` | [-] Derivative rate-loop gain (ideal form) |
| `kff` | `float32` | [-] Feedforward rate-loop gain |
| `att_p` | `float32` | [-] Proportional attitude gain |
| `rate_sp` | `float32[3]` | [rad/s] Rate setpoint commanded to the attitude controller. |
| `u_filt` | `float32` | [-] Filtered input signal (normalized torque setpoint) used in system identification. |
| `y_filt` | `float32` | [rad/s] Filtered output signal (angular velocity) used in system identification. |
| `state` | `uint8` | [@enum STATE] Current state of the autotune procedure. |

常數:`STATE_IDLE=0`、`STATE_INIT=1`、`STATE_ROLL_AMPLITUDE_DETECTION=2`、`STATE_ROLL=3`、`STATE_ROLL_PAUSE=4`、`STATE_PITCH_AMPLITUDE_DETECTION=5`、`STATE_PITCH=6`、`STATE_PITCH_PAUSE=7`、`STATE_YAW_AMPLITUDE_DETECTION=8`、`STATE_YAW=9`、`STATE_YAW_PAUSE=10`、`STATE_VERIFICATION=11`、`STATE_APPLY=12`、`STATE_TEST=13`、`STATE_COMPLETE=14`、`STATE_FAIL=15`、`STATE_WAIT_FOR_DISARM=16`

## BatteryInfo

內部訊息 · 主題名 `battery_info`

Battery information Static or near-invariant battery information. Should be streamed at low rate.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `id` | `uint8` | Must match the id in the battery_status message for the same battery |
| `serial_number` | `char[32]` | [@invalid 0 All bytes] Serial number of the battery pack in ASCII characters, 0 terminated |

## BatteryStatusV0

內部訊息 · 主題名 `battery_status_v0`

Battery status Battery status information for up to 4 battery instances. These are populated from power module and smart battery device drivers, and one battery updated from MAVLink. Battery instance information is also logged and streamed in MAVLink telemetry.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `connected` | `bool` | Whether or not a battery is connected. For power modules this is based on a voltage threshold. |
| `voltage_v` | `float32` | [V] [@invalid 0] Battery voltage |
| `current_a` | `float32` | [A] [@invalid -1] Battery current |
| `current_average_a` | `float32` | [A] [@invalid -1] Battery current average (for FW average in level flight) |
| `discharged_mah` | `float32` | [mAh] [@invalid -1] Discharged amount |
| `remaining` | `float32` | [@range 0,1] [@invalid -1] Remaining capacity |
| `scale` | `float32` | [@range 1,] [@invalid -1] Scaling factor to compensate for lower actuation power caused by voltage sag |
| `time_remaining_s` | `float32` | [s] [@invalid NaN] Predicted time remaining until battery is empty under previous averaged load |
| `temperature` | `float32` | [°C] [@invalid NaN] Temperature of the battery |
| `cell_count` | `uint8` | [@invalid 0] Number of cells |
| `source` | `uint8` | [@enum SOURCE] Battery source |
| `priority` | `uint8` | Zero based priority is the connection on the Power Controller V1..Vn AKA BrickN-1 |
| `capacity` | `uint16` | [mAh] Capacity of the battery when fully charged |
| `cycle_count` | `uint16` | Number of discharge cycles the battery has experienced |
| `average_time_to_empty` | `uint16` | [minutes] Predicted remaining battery capacity based on the average rate of discharge |
| `serial_number` | `uint16` | Serial number of the battery pack |
| `manufacture_date` | `uint16` | Manufacture date, part of serial number of the battery pack. Formatted as: Day + Month×32 + (Year–1980)×512 |
| `state_of_health` | `uint16` | [%] [@range 0, 100] State of health. FullChargeCapacity/DesignCapacity |
| `max_error` | `uint16` | [%] [@range 1, 100] Max error, expected margin of error in the state-of-charge calculation |
| `id` | `uint8` | ID number of a battery. Should be unique and consistent for the lifetime of a vehicle. 1-indexed |
| `interface_error` | `uint16` | Interface error counter |
| `voltage_cell_v` | `float32[14]` | [V] [@invalid 0] Battery individual cell voltages |
| `max_cell_voltage_delta` | `float32` | Max difference between individual cell voltages |
| `is_powering_off` | `bool` | Power off event imminent indication, false if unknown |
| `is_required` | `bool` | Set if the battery is explicitly required before arming |
| `warning` | `uint8` | [@enum WARNING STATE] Current battery warning |
| `faults` | `uint16` | [@enum FAULT] Smart battery supply status/fault flags (bitmask) for health indication |
| `full_charge_capacity_wh` | `float32` | [Wh] Compensated battery capacity |
| `remaining_capacity_wh` | `float32` | [Wh] Compensated battery capacity remaining |
| `over_discharge_count` | `uint16` | Number of battery overdischarge |
| `nominal_voltage` | `float32` | [V] Nominal voltage of the battery pack |
| `internal_resistance_estimate` | `float32` | [Ohm] Internal resistance per cell estimate |
| `ocv_estimate` | `float32` | [V] Open circuit voltage estimate |
| `ocv_estimate_filtered` | `float32` | [V] Filtered open circuit voltage estimate |
| `volt_based_soc_estimate` | `float32` | [@range 0, 1] Normalized volt based state of charge estimate |
| `voltage_prediction` | `float32` | [V] Predicted voltage |
| `prediction_error` | `float32` | [V] Prediction error |
| `estimation_covariance_norm` | `float32` | Norm of the covariance matrix |

常數:`MESSAGE_VERSION=0`、`MAX_INSTANCES=4`、`SOURCE_POWER_MODULE=0`、`SOURCE_EXTERNAL=1`、`SOURCE_ESCS=2`、`WARNING_NONE=0`、`WARNING_LOW=1`、`WARNING_CRITICAL=2`、`WARNING_EMERGENCY=3`、`WARNING_FAILED=4`、`STATE_UNHEALTHY=6`、`STATE_CHARGING=7`、`FAULT_DEEP_DISCHARGE=0`、`FAULT_SPIKES=1`、`FAULT_CELL_FAIL=2`、`FAULT_OVER_CURRENT=3`、`FAULT_OVER_TEMPERATURE=4`、`FAULT_UNDER_TEMPERATURE=5`、`FAULT_INCOMPATIBLE_VOLTAGE=6`、`FAULT_INCOMPATIBLE_FIRMWARE=7`、`FAULT_INCOMPATIBLE_MODEL=8`、`FAULT_HARDWARE_FAILURE=9`、`FAULT_FAILED_TO_ARM=10`、`FAULT_COUNT=11`

## ButtonEvent

內部訊息 · 主題名 `button_event`、`safety_button`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `triggered` | `bool` | Set to true if the event is triggered |

常數:`ORB_QUEUE_LENGTH=2`

## CameraCapture

內部訊息 · 主題名 `camera_capture`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_utc` | `uint64` | Capture time in UTC / GPS time |
| `seq` | `uint32` | Image sequence number |
| `lat` | `float64` | Latitude in degrees (WGS84) |
| `lon` | `float64` | Longitude in degrees (WGS84) |
| `alt` | `float32` | Altitude (AMSL) |
| `ground_distance` | `float32` | Altitude above ground (meters) |
| `q` | `float32[4]` | Attitude of the camera relative to NED earth-fixed frame when using a gimbal, otherwise vehicle attitude |
| `result` | `int8` | 1 for success, 0 for failure, -1 if camera does not provide feedback |

## CameraStatus

內部訊息 · 主題名 `camera_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `active_sys_id` | `uint8` | mavlink system id of the currently active camera |
| `active_comp_id` | `uint8` | mavlink component id of currently active camera |

## CameraTrigger

內部訊息 · 主題名 `camera_trigger`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_utc` | `uint64` | UTC timestamp |
| `seq` | `uint32` | Image sequence number |
| `feedback` | `bool` | Trigger feedback from camera |

常數:`ORB_QUEUE_LENGTH=2`

## CanInterfaceStatus

內部訊息 · 主題名 `can_interface_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `interface` | `uint8` |  |
| `io_errors` | `uint64` |  |
| `frames_tx` | `uint64` |  |
| `frames_rx` | `uint64` |  |

## CellularStatus

內部訊息 · 主題名 `cellular_status`

Cellular status This is currently used only for logging cell status from MAVLink.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `status` | `uint16` | [@enum STATUS_FLAG] Status bitmap |
| `failure_reason` | `uint8` | [@enum FAILURE_REASON] Failure reason |
| `type` | `uint8` | [@enum CELLULAR_NETWORK_RADIO_TYPE] Cellular network radio type |
| `quality` | `uint8` | [dBm] Cellular network RSSI/RSRP, absolute value |
| `mcc` | `uint16` | [@invalid UINT16_MAX] Mobile country code |
| `mnc` | `uint16` | [@invalid UINT16_MAX] Mobile network code |
| `lac` | `uint16` | [@invalid 0] Location area code |

常數:`STATUS_FLAG_UNKNOWN=1`、`STATUS_FLAG_FAILED=2`、`STATUS_FLAG_INITIALIZING=4`、`STATUS_FLAG_LOCKED=8`、`STATUS_FLAG_DISABLED=16`、`STATUS_FLAG_DISABLING=32`、`STATUS_FLAG_ENABLING=64`、`STATUS_FLAG_ENABLED=128`、`STATUS_FLAG_SEARCHING=256`、`STATUS_FLAG_REGISTERED=512`、`STATUS_FLAG_DISCONNECTING=1024`、`STATUS_FLAG_CONNECTING=2048`、`STATUS_FLAG_CONNECTED=4096`、`FAILURE_REASON_NONE=0`、`FAILURE_REASON_UNKNOWN=1`、`FAILURE_REASON_SIM_MISSING=2`、`FAILURE_REASON_SIM_ERROR=3`、`CELLULAR_NETWORK_RADIO_TYPE_NONE=0`、`CELLULAR_NETWORK_RADIO_TYPE_GSM=1`、`CELLULAR_NETWORK_RADIO_TYPE_CDMA=2`、`CELLULAR_NETWORK_RADIO_TYPE_WCDMA=3`、`CELLULAR_NETWORK_RADIO_TYPE_LTE=4`

## CollisionConstraints

內部訊息 · 主題名 `collision_constraints`

Local setpoint constraints in NED frame setting something to NaN means that no limit is provided

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `original_setpoint` | `float32[2]` | velocities demanded |
| `adapted_setpoint` | `float32[2]` | velocities allowed |

## ControlAllocatorStatus

內部訊息 · 主題名 `control_allocator_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `torque_setpoint_achieved` | `bool` | Boolean indicating whether the 3D torque setpoint was correctly allocated to actuators. 0 if not achieved, 1 if achieved. |
| `unallocated_torque` | `float32[3]` | Unallocated torque. Equal to 0 if the setpoint was achieved. |
| `thrust_setpoint_achieved` | `bool` | Boolean indicating whether the 3D thrust setpoint was correctly allocated to actuators. 0 if not achieved, 1 if achieved. |
| `unallocated_thrust` | `float32[3]` | Unallocated thrust. Equal to 0 if the setpoint was achieved. |
| `actuator_saturation` | `int8[16]` | Indicates actuator saturation status. |
| `handled_motor_failure_mask` | `uint16` | Bitmask of failed motors that were removed from the allocation / effectiveness matrix. Not necessarily identical to the report from FailureDetector |
| `motor_stop_mask` | `uint16` | Bitmaks of motors stopped by failure injection |

常數:`ACTUATOR_SATURATION_OK=0`、`ACTUATOR_SATURATION_UPPER_DYN=1`、`ACTUATOR_SATURATION_UPPER=2`、`ACTUATOR_SATURATION_LOWER_DYN=-1`、`ACTUATOR_SATURATION_LOWER=-2`

## Cpuload

內部訊息 · 主題名 `cpuload`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `load` | `float32` | processor load from 0 to 1 |
| `ram_usage` | `float32` | RAM usage from 0 to 1 |

## DatamanRequest

內部訊息 · 主題名 `dataman_request`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `client_id` | `uint8` |  |
| `request_type` | `uint8` | id/read/write/clear |
| `item` | `uint8` | dm_item_t |
| `index` | `uint32` |  |
| `data` | `uint8[56]` |  |
| `data_length` | `uint32` |  |

## DatamanResponse

內部訊息 · 主題名 `dataman_response`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `client_id` | `uint8` |  |
| `request_type` | `uint8` | id/read/write/clear |
| `item` | `uint8` | dm_item_t |
| `index` | `uint32` |  |
| `data` | `uint8[56]` |  |
| `status` | `uint8` |  |

常數:`STATUS_SUCCESS=0`、`STATUS_FAILURE_ID_ERR=1`、`STATUS_FAILURE_NO_DATA=2`、`STATUS_FAILURE_READ_FAILED=3`、`STATUS_FAILURE_WRITE_FAILED=4`、`STATUS_FAILURE_CLEAR_FAILED=5`

## DebugArray

內部訊息 · 主題名 `debug_array`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `id` | `uint16` | unique ID of debug array, used to discriminate between arrays |
| `name` | `char[10]` | name of the debug array (max. 10 characters) |
| `data` | `float32[58]` | data |

常數:`ARRAY_SIZE=58`

## DebugKeyValue

內部訊息 · 主題名 `debug_key_value`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `key` | `char[10]` | max. 10 characters as key / name |
| `value` | `float32` | the value to send as debug output |

## DebugValue

內部訊息 · 主題名 `debug_value`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `ind` | `int8` | index of debug variable |
| `value` | `float32` | the value to send as debug output |

## DebugVect

內部訊息 · 主題名 `debug_vect`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `name` | `char[10]` | max. 10 characters as key / name |
| `x` | `float32` | x value |
| `y` | `float32` | y value |
| `z` | `float32` | z value |

## DifferentialPressure

內部訊息 · 主題名 `differential_pressure`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `differential_pressure_pa` | `float32` | differential pressure reading in Pascals (may be negative) |
| `temperature` | `float32` | Temperature provided by sensor in degrees Celsius, NAN if unknown |
| `error_count` | `uint32` | Number of errors detected by driver |

## DistanceSensor

內部訊息 · 主題名 `distance_sensor`

DISTANCE_SENSOR message data

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `min_distance` | `float32` | Minimum distance the sensor can measure (in m) |
| `max_distance` | `float32` | Maximum distance the sensor can measure (in m) |
| `current_distance` | `float32` | Current distance reading (in m) |
| `variance` | `float32` | Measurement variance (in m^2), 0 for unknown / invalid readings |
| `signal_quality` | `int8` | Signal quality in percent (0...100%), where 0 = invalid signal, 100 = perfect signal, and -1 = unknown signal quality. |
| `type` | `uint8` | Type from MAV_DISTANCE_SENSOR enum |
| `h_fov` | `float32` | Sensor horizontal field of view (rad) |
| `v_fov` | `float32` | Sensor vertical field of view (rad) |
| `q` | `float32[4]` | Quaterion sensor orientation with respect to the vehicle body frame to specify the orientation ROTATION_CUSTOM |
| `orientation` | `uint8` | Direction the sensor faces from MAV_SENSOR_ORIENTATION enum |
| `mode` | `uint8` |  |

常數:`MAV_DISTANCE_SENSOR_LASER=0`、`MAV_DISTANCE_SENSOR_ULTRASOUND=1`、`MAV_DISTANCE_SENSOR_INFRARED=2`、`MAV_DISTANCE_SENSOR_RADAR=3`、`ROTATION_YAW_0=0`、`ROTATION_YAW_45=1`、`ROTATION_YAW_90=2`、`ROTATION_YAW_135=3`、`ROTATION_YAW_180=4`、`ROTATION_YAW_225=5`、`ROTATION_YAW_270=6`、`ROTATION_YAW_315=7`、`ROTATION_FORWARD_FACING=0`、`ROTATION_RIGHT_FACING=2`、`ROTATION_BACKWARD_FACING=4`、`ROTATION_LEFT_FACING=6`、`ROTATION_UPWARD_FACING=24`、`ROTATION_DOWNWARD_FACING=25`、`ROTATION_CUSTOM=100`、`MODE_UNKNOWN=0`、`MODE_ENABLED=1`、`MODE_DISABLED=2`

## DistanceSensorModeChangeRequest

內部訊息 · 主題名 `distance_sensor_mode_change_request`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `request_on_off` | `uint8` | request to disable/enable the distance sensor |

常數:`REQUEST_OFF=0`、`REQUEST_ON=1`

## DronecanNodeStatus

內部訊息 · 主題名 `dronecan_node_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `node_id` | `uint16` | The node ID which this data comes from |
| `uptime_sec` | `uint32` | Node uptime |
| `health` | `uint8` |  |
| `mode` | `uint8` |  |
| `sub_mode` | `uint8` |  |
| `vendor_specific_status_code` | `uint16` |  |

常數:`HEALTH_OK=0`、`HEALTH_WARNING=1`、`HEALTH_ERROR=2`、`HEALTH_CRITICAL=3`、`MODE_OPERATIONAL=0`、`MODE_INITIALIZATION=1`、`MODE_MAINTENANCE=2`、`MODE_SOFTWARE_UPDATE=3`、`MODE_OFFLINE=7`

## Ekf2Timestamps

內部訊息 · 主題名 `ekf2_timestamps`

this message contains the (relative) timestamps of the sensor inputs used by EKF2. It can be used for reproducible replay. the timestamp field is the ekf2 reference time and matches the timestamp of the sensor_combined topic.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `airspeed_timestamp_rel` | `int16` |  |
| `airspeed_validated_timestamp_rel` | `int16` |  |
| `distance_sensor_timestamp_rel` | `int16` |  |
| `optical_flow_timestamp_rel` | `int16` |  |
| `vehicle_air_data_timestamp_rel` | `int16` |  |
| `vehicle_magnetometer_timestamp_rel` | `int16` |  |
| `visual_odometry_timestamp_rel` | `int16` |  |

常數:`RELATIVE_TIMESTAMP_INVALID=32767`

## EscReport

內部訊息 · 主題名 `esc_report`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `esc_errorcount` | `uint32` | Number of reported errors by ESC - if supported |
| `esc_rpm` | `int32` | Motor RPM, negative for reverse rotation [RPM] - if supported |
| `esc_voltage` | `float32` | Voltage measured from current ESC [V] - if supported |
| `esc_current` | `float32` | Current measured from current ESC [A] - if supported |
| `esc_temperature` | `float32` | Temperature measured from current ESC [degC] - if supported |
| `esc_address` | `uint8` | Address of current ESC (in most cases 1-8 / must be set by driver) |
| `esc_cmdcount` | `uint8` | Counter of number of commands |
| `esc_state` | `uint8` | State of ESC - depend on Vendor |
| `actuator_function` | `uint8` | actuator output function (one of Motor1...MotorN) |
| `failures` | `uint16` | Bitmask to indicate the internal ESC faults |
| `esc_power` | `int8` | Applied power 0-100 in % (negative values reserved) |

常數:`FAILURE_OVER_CURRENT=0`、`FAILURE_OVER_VOLTAGE=1`、`FAILURE_MOTOR_OVER_TEMPERATURE=2`、`FAILURE_OVER_RPM=3`、`FAILURE_INCONSISTENT_CMD=4`、`FAILURE_MOTOR_STUCK=5`、`FAILURE_GENERIC=6`、`FAILURE_MOTOR_WARN_TEMPERATURE=7`、`FAILURE_WARN_ESC_TEMPERATURE=8`、`FAILURE_OVER_ESC_TEMPERATURE=9`、`ESC_FAILURE_COUNT=10`

## EscStatus

內部訊息 · 主題名 `esc_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `counter` | `uint16` | incremented by the writing thread everytime new data is stored |
| `esc_count` | `uint8` | number of connected ESCs |
| `esc_connectiontype` | `uint8` | how ESCs connected to the system |
| `esc_online_flags` | `uint8` | Bitmask indicating which ESC is online/offline |
| `esc_armed_flags` | `uint8` | Bitmask indicating which ESC is armed. For ESC's where the arming state is not known (returned by the ESC), the arming bits should always be set. |
| `esc` | `EscReport[8]` |  |

常數:`CONNECTED_ESC_MAX=8`、`ESC_CONNECTION_TYPE_PPM=0`、`ESC_CONNECTION_TYPE_SERIAL=1`、`ESC_CONNECTION_TYPE_ONESHOT=2`、`ESC_CONNECTION_TYPE_I2C=3`、`ESC_CONNECTION_TYPE_CAN=4`、`ESC_CONNECTION_TYPE_DSHOT=5`

## EstimatorAidSource1d

內部訊息 · 主題名 `estimator_aid_src_baro_hgt`、`estimator_aid_src_ev_hgt`、`estimator_aid_src_gnss_hgt`、`estimator_aid_src_rng_hgt`、`estimator_aid_src_airspeed`、`estimator_aid_src_sideslip`、`estimator_aid_src_fake_hgt`、`estimator_aid_src_gnss_yaw`、`estimator_aid_src_ev_yaw`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `estimator_instance` | `uint8` |  |
| `device_id` | `uint32` |  |
| `time_last_fuse` | `uint64` |  |
| `observation` | `float32` |  |
| `observation_variance` | `float32` |  |
| `innovation` | `float32` |  |
| `innovation_filtered` | `float32` |  |
| `innovation_variance` | `float32` |  |
| `test_ratio` | `float32` | normalized innovation squared |
| `test_ratio_filtered` | `float32` | signed filtered test ratio |
| `innovation_rejected` | `bool` | true if the observation has been rejected |
| `fused` | `bool` | true if the sample was successfully fused |

## EstimatorAidSource2d

內部訊息 · 主題名 `estimator_aid_src_ev_pos`、`estimator_aid_src_fake_pos`、`estimator_aid_src_gnss_pos`、`estimator_aid_src_aux_global_position`、`estimator_aid_src_aux_vel`、`estimator_aid_src_optical_flow`、`estimator_aid_src_drag`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `estimator_instance` | `uint8` |  |
| `device_id` | `uint32` |  |
| `time_last_fuse` | `uint64` |  |
| `observation` | `float64[2]` |  |
| `observation_variance` | `float32[2]` |  |
| `innovation` | `float32[2]` |  |
| `innovation_filtered` | `float32[2]` |  |
| `innovation_variance` | `float32[2]` |  |
| `test_ratio` | `float32[2]` | normalized innovation squared |
| `test_ratio_filtered` | `float32[2]` | signed filtered test ratio |
| `innovation_rejected` | `bool` | true if the observation has been rejected |
| `fused` | `bool` | true if the sample was successfully fused |

## EstimatorAidSource3d

內部訊息 · 主題名 `estimator_aid_src_ev_vel`、`estimator_aid_src_gnss_vel`、`estimator_aid_src_gravity`、`estimator_aid_src_mag`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `estimator_instance` | `uint8` |  |
| `device_id` | `uint32` |  |
| `time_last_fuse` | `uint64` |  |
| `observation` | `float32[3]` |  |
| `observation_variance` | `float32[3]` |  |
| `innovation` | `float32[3]` |  |
| `innovation_filtered` | `float32[3]` |  |
| `innovation_variance` | `float32[3]` |  |
| `test_ratio` | `float32[3]` | normalized innovation squared |
| `test_ratio_filtered` | `float32[3]` | signed filtered test ratio |
| `innovation_rejected` | `bool` | true if the observation has been rejected |
| `fused` | `bool` | true if the sample was successfully fused |

## EstimatorBias

內部訊息 · 主題名 `estimator_baro_bias`、`estimator_gnss_hgt_bias`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `bias` | `float32` | estimated barometric altitude bias (m) |
| `bias_var` | `float32` | estimated barometric altitude bias variance (m^2) |
| `innov` | `float32` | innovation of the last measurement fusion (m) |
| `innov_var` | `float32` | innovation variance of the last measurement fusion (m^2) |
| `innov_test_ratio` | `float32` | normalized innovation squared test ratio |

## EstimatorBias3d

內部訊息 · 主題名 `estimator_bias3d`、`estimator_ev_pos_bias`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `bias` | `float32[3]` | estimated barometric altitude bias (m) |
| `bias_var` | `float32[3]` | estimated barometric altitude bias variance (m^2) |
| `innov` | `float32[3]` | innovation of the last measurement fusion (m) |
| `innov_var` | `float32[3]` | innovation variance of the last measurement fusion (m^2) |
| `innov_test_ratio` | `float32[3]` | normalized innovation squared test ratio |

## EstimatorEventFlags

內部訊息 · 主題名 `estimator_event_flags`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `information_event_changes` | `uint32` | number of information event changes |
| `gps_checks_passed` | `bool` | 0 - true when gps quality checks are passing passed |
| `reset_vel_to_gps` | `bool` | 1 - true when the velocity states are reset to the gps measurement |
| `reset_vel_to_flow` | `bool` | 2 - true when the velocity states are reset using the optical flow measurement |
| `reset_vel_to_vision` | `bool` | 3 - true when the velocity states are reset to the vision system measurement |
| `reset_vel_to_zero` | `bool` | 4 - true when the velocity states are reset to zero |
| `reset_pos_to_last_known` | `bool` | 5 - true when the position states are reset to the last known position |
| `reset_pos_to_gps` | `bool` | 6 - true when the position states are reset to the gps measurement |
| `reset_pos_to_vision` | `bool` | 7 - true when the position states are reset to the vision system measurement |
| `starting_gps_fusion` | `bool` | 8 - true when the filter starts using gps measurements to correct the state estimates |
| `starting_vision_pos_fusion` | `bool` | 9 - true when the filter starts using vision system position measurements to correct the state estimates |
| `starting_vision_vel_fusion` | `bool` | 10 - true when the filter starts using vision system velocity measurements to correct the state estimates |
| `starting_vision_yaw_fusion` | `bool` | 11 - true when the filter starts using vision system yaw  measurements to correct the state estimates |
| `yaw_aligned_to_imu_gps` | `bool` | 12 - true when the filter resets the yaw to an estimate derived from IMU and GPS data |
| `reset_hgt_to_baro` | `bool` | 13 - true when the vertical position state is reset to the baro measurement |
| `reset_hgt_to_gps` | `bool` | 14 - true when the vertical position state is reset to the gps measurement |
| `reset_hgt_to_rng` | `bool` | 15 - true when the vertical position state is reset to the rng measurement |
| `reset_hgt_to_ev` | `bool` | 16 - true when the vertical position state is reset to the ev measurement |

## EstimatorGpsStatus

內部訊息 · 主題名 `estimator_gps_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `checks_passed` | `bool` |  |
| `check_fail_gps_fix` | `bool` | 0 : insufficient fix type (no 3D solution) |
| `check_fail_min_sat_count` | `bool` | 1 : minimum required sat count fail |
| `check_fail_max_pdop` | `bool` | 2 : maximum allowed PDOP fail |
| `check_fail_max_horz_err` | `bool` | 3 : maximum allowed horizontal position error fail |
| `check_fail_max_vert_err` | `bool` | 4 : maximum allowed vertical position error fail |
| `check_fail_max_spd_err` | `bool` | 5 : maximum allowed speed error fail |
| `check_fail_max_horz_drift` | `bool` | 6 : maximum allowed horizontal position drift fail - requires stationary vehicle |
| `check_fail_max_vert_drift` | `bool` | 7 : maximum allowed vertical position drift fail - requires stationary vehicle |
| `check_fail_max_horz_spd_err` | `bool` | 8 : maximum allowed horizontal speed fail - requires stationary vehicle |
| `check_fail_max_vert_spd_err` | `bool` | 9 : maximum allowed vertical velocity discrepancy fail |
| `check_fail_spoofed_gps` | `bool` | 10 : GPS signal is spoofed |
| `position_drift_rate_horizontal_m_s` | `float32` | Horizontal position rate magnitude (m/s) |
| `position_drift_rate_vertical_m_s` | `float32` | Vertical position rate magnitude (m/s) |
| `filtered_horizontal_speed_m_s` | `float32` | Filtered horizontal velocity magnitude (m/s) |

## EstimatorInnovations

內部訊息 · 主題名 `estimator_innovations`、`estimator_innovation_variances`、`estimator_innovation_test_ratios`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `gps_hvel` | `float32[2]` | horizontal GPS velocity innovation (m/sec) and innovation variance ((m/sec)**2) |
| `gps_vvel` | `float32` | vertical GPS velocity innovation (m/sec) and innovation variance ((m/sec)**2) |
| `gps_hpos` | `float32[2]` | horizontal GPS position innovation (m) and innovation variance (m**2) |
| `gps_vpos` | `float32` | vertical GPS position innovation (m) and innovation variance (m**2) |
| `ev_hvel` | `float32[2]` | horizontal external vision velocity innovation (m/sec) and innovation variance ((m/sec)**2) |
| `ev_vvel` | `float32` | vertical external vision velocity innovation (m/sec) and innovation variance ((m/sec)**2) |
| `ev_hpos` | `float32[2]` | horizontal external vision position innovation (m) and innovation variance (m**2) |
| `ev_vpos` | `float32` | vertical external vision position innovation (m) and innovation variance (m**2) |
| `rng_vpos` | `float32` | range sensor height innovation (m) and innovation variance (m**2) |
| `baro_vpos` | `float32` | barometer height innovation (m) and innovation variance (m**2) |
| `aux_hvel` | `float32[2]` | horizontal auxiliary velocity innovation from landing target measurement (m/sec) and innovation variance ((m/sec)**2) |
| `flow` | `float32[2]` | flow innvoation (rad/sec) and innovation variance ((rad/sec)**2) |
| `heading` | `float32` | heading innovation (rad) and innovation variance (rad**2) |
| `mag_field` | `float32[3]` | earth magnetic field innovation (Gauss) and innovation variance (Gauss**2) |
| `gravity` | `float32[3]` | gravity innovation from accelerometerr vector (m/s**2) |
| `drag` | `float32[2]` | drag specific force innovation (m/sec**2) and innovation variance ((m/sec)**2) |
| `airspeed` | `float32` | airspeed innovation (m/sec) and innovation variance ((m/sec)**2) |
| `beta` | `float32` | synthetic sideslip innovation (rad) and innovation variance (rad**2) |
| `hagl` | `float32` | height of ground innovation (m) and innovation variance (m**2) |
| `hagl_rate` | `float32` | height of ground rate innovation (m/s) and innovation variance ((m/s)**2) |

## EstimatorSelectorStatus

內部訊息 · 主題名 `estimator_selector_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `primary_instance` | `uint8` |  |
| `instances_available` | `uint8` |  |
| `instance_changed_count` | `uint32` |  |
| `last_instance_change` | `uint64` |  |
| `accel_device_id` | `uint32` |  |
| `baro_device_id` | `uint32` |  |
| `gyro_device_id` | `uint32` |  |
| `mag_device_id` | `uint32` |  |
| `combined_test_ratio` | `float32[9]` |  |
| `relative_test_ratio` | `float32[9]` |  |
| `healthy` | `bool[9]` |  |
| `accumulated_gyro_error` | `float32[4]` |  |
| `accumulated_accel_error` | `float32[4]` |  |
| `gyro_fault_detected` | `bool` |  |
| `accel_fault_detected` | `bool` |  |

## EstimatorSensorBias

內部訊息 · 主題名 `estimator_sensor_bias`

Sensor readings and in-run biases in SI-unit form. Sensor readings are compensated for static offsets, scale errors, in-run bias and thermal drift (if thermal compensation is enabled and available).

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `gyro_device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `gyro_bias` | `float32[3]` | gyroscope in-run bias in body frame (rad/s) |
| `gyro_bias_limit` | `float32` | magnitude of maximum gyroscope in-run bias in body frame (rad/s) |
| `gyro_bias_variance` | `float32[3]` |  |
| `gyro_bias_valid` | `bool` |  |
| `gyro_bias_stable` | `bool` | true when the gyro bias estimate is stable enough to use for calibration |
| `accel_device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `accel_bias` | `float32[3]` | accelerometer in-run bias in body frame (m/s^2) |
| `accel_bias_limit` | `float32` | magnitude of maximum accelerometer in-run bias in body frame (m/s^2) |
| `accel_bias_variance` | `float32[3]` |  |
| `accel_bias_valid` | `bool` |  |
| `accel_bias_stable` | `bool` | true when the accel bias estimate is stable enough to use for calibration |
| `mag_device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `mag_bias` | `float32[3]` | magnetometer in-run bias in body frame (Gauss) |
| `mag_bias_limit` | `float32` | magnitude of maximum magnetometer in-run bias in body frame (Gauss) |
| `mag_bias_variance` | `float32[3]` |  |
| `mag_bias_valid` | `bool` |  |
| `mag_bias_stable` | `bool` | true when the mag bias estimate is stable enough to use for calibration |

## EstimatorStates

內部訊息 · 主題名 `estimator_states`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `states` | `float32[25]` | Internal filter states |
| `n_states` | `uint8` | Number of states effectively used |
| `covariances` | `float32[24]` | Diagonal Elements of Covariance Matrix |

## EstimatorStatus

內部訊息 · 主題名 `estimator_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `output_tracking_error` | `float32[3]` | return a vector containing the output predictor angular, velocity and position tracking error magnitudes (rad), (m/s), (m) |
| `gps_check_fail_flags` | `uint16` | Bitmask to indicate status of GPS checks - see definition below |
| `control_mode_flags` | `uint64` | Bitmask to indicate EKF logic state |
| `filter_fault_flags` | `uint32` | Bitmask to indicate EKF internal faults |
| `pos_horiz_accuracy` | `float32` | 1-Sigma estimated horizontal position accuracy relative to the estimators origin (m) |
| `pos_vert_accuracy` | `float32` | 1-Sigma estimated vertical position accuracy relative to the estimators origin (m) |
| `hdg_test_ratio` | `float32` | low-pass filtered ratio of the largest heading innovation component to the innovation test limit |
| `vel_test_ratio` | `float32` | low-pass filtered ratio of the largest velocity innovation component to the innovation test limit |
| `pos_test_ratio` | `float32` | low-pass filtered ratio of the largest horizontal position innovation component to the innovation test limit |
| `hgt_test_ratio` | `float32` | low-pass filtered ratio of the vertical position innovation to the innovation test limit |
| `tas_test_ratio` | `float32` | low-pass filtered ratio of the true airspeed innovation to the innovation test limit |
| `hagl_test_ratio` | `float32` | low-pass filtered ratio of the height above ground innovation to the innovation test limit |
| `beta_test_ratio` | `float32` | low-pass filtered ratio of the synthetic sideslip innovation to the innovation test limit |
| `solution_status_flags` | `uint16` | Bitmask indicating which filter kinematic state outputs are valid for flight control use. |
| `reset_count_vel_ne` | `uint8` | number of horizontal position reset events (allow to wrap if count exceeds 255) |
| `reset_count_vel_d` | `uint8` | number of vertical velocity reset events (allow to wrap if count exceeds 255) |
| `reset_count_pos_ne` | `uint8` | number of horizontal position reset events (allow to wrap if count exceeds 255) |
| `reset_count_pod_d` | `uint8` | number of vertical position reset events (allow to wrap if count exceeds 255) |
| `reset_count_quat` | `uint8` | number of quaternion reset events (allow to wrap if count exceeds 255) |
| `time_slip` | `float32` | cumulative amount of time in seconds that the EKF inertial calculation has slipped relative to system time |
| `pre_flt_fail_innov_heading` | `bool` |  |
| `pre_flt_fail_innov_height` | `bool` |  |
| `pre_flt_fail_innov_pos_horiz` | `bool` |  |
| `pre_flt_fail_innov_vel_horiz` | `bool` |  |
| `pre_flt_fail_innov_vel_vert` | `bool` |  |
| `pre_flt_fail_mag_field_disturbed` | `bool` |  |
| `accel_device_id` | `uint32` |  |
| `gyro_device_id` | `uint32` |  |
| `baro_device_id` | `uint32` |  |
| `mag_device_id` | `uint32` |  |
| `health_flags` | `uint8` | Bitmask to indicate sensor health states (vel, pos, hgt) |
| `timeout_flags` | `uint8` | Bitmask to indicate timeout flags (vel, pos, hgt) |
| `mag_inclination_deg` | `float32` |  |
| `mag_inclination_ref_deg` | `float32` |  |
| `mag_strength_gs` | `float32` |  |
| `mag_strength_ref_gs` | `float32` |  |

常數:`GPS_CHECK_FAIL_GPS_FIX=0`、`GPS_CHECK_FAIL_MIN_SAT_COUNT=1`、`GPS_CHECK_FAIL_MAX_PDOP=2`、`GPS_CHECK_FAIL_MAX_HORZ_ERR=3`、`GPS_CHECK_FAIL_MAX_VERT_ERR=4`、`GPS_CHECK_FAIL_MAX_SPD_ERR=5`、`GPS_CHECK_FAIL_MAX_HORZ_DRIFT=6`、`GPS_CHECK_FAIL_MAX_VERT_DRIFT=7`、`GPS_CHECK_FAIL_MAX_HORZ_SPD_ERR=8`、`GPS_CHECK_FAIL_MAX_VERT_SPD_ERR=9`、`GPS_CHECK_FAIL_SPOOFED=10`、`CS_TILT_ALIGN=0`、`CS_YAW_ALIGN=1`、`CS_GNSS_POS=2`、`CS_OPT_FLOW=3`、`CS_MAG_HDG=4`、`CS_MAG_3D=5`、`CS_MAG_DEC=6`、`CS_IN_AIR=7`、`CS_WIND=8`、`CS_BARO_HGT=9`、`CS_RNG_HGT=10`、`CS_GPS_HGT=11`、`CS_EV_POS=12`、`CS_EV_YAW=13`、`CS_EV_HGT=14`、`CS_BETA=15`、`CS_MAG_FIELD=16`、`CS_FIXED_WING=17`、`CS_MAG_FAULT=18`、`CS_ASPD=19`、`CS_GND_EFFECT=20`、`CS_RNG_STUCK=21`、`CS_GPS_YAW=22`、`CS_MAG_ALIGNED=23`、`CS_EV_VEL=24`、`CS_SYNTHETIC_MAG_Z=25`、`CS_VEHICLE_AT_REST=26`、`CS_GPS_YAW_FAULT=27`、`CS_RNG_FAULT=28`、`CS_GNSS_VEL=44`、`CS_GNSS_FAULT=45`、`CS_YAW_MANUAL=46`

## EstimatorStatusFlags

內部訊息 · 主題名 `estimator_status_flags`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `control_status_changes` | `uint32` | number of filter control status (cs) changes |
| `cs_tilt_align` | `bool` | 0 - true if the filter tilt alignment is complete |
| `cs_yaw_align` | `bool` | 1 - true if the filter yaw alignment is complete |
| `cs_gnss_pos` | `bool` | 2 - true if GNSS position measurement fusion is intended |
| `cs_opt_flow` | `bool` | 3 - true if optical flow measurements fusion is intended |
| `cs_mag_hdg` | `bool` | 4 - true if a simple magnetic yaw heading fusion is intended |
| `cs_mag_3d` | `bool` | 5 - true if 3-axis magnetometer measurement fusion is intended |
| `cs_mag_dec` | `bool` | 6 - true if synthetic magnetic declination measurements fusion is intended |
| `cs_in_air` | `bool` | 7 - true when the vehicle is airborne |
| `cs_wind` | `bool` | 8 - true when wind velocity is being estimated |
| `cs_baro_hgt` | `bool` | 9 - true when baro data is being fused |
| `cs_rng_hgt` | `bool` | 10 - true when range finder data is being fused for height aiding |
| `cs_gps_hgt` | `bool` | 11 - true when GPS altitude is being fused |
| `cs_ev_pos` | `bool` | 12 - true when local position data fusion from external vision is intended |
| `cs_ev_yaw` | `bool` | 13 - true when yaw data from external vision measurements fusion is intended |
| `cs_ev_hgt` | `bool` | 14 - true when height data from external vision measurements is being fused |
| `cs_fuse_beta` | `bool` | 15 - true when synthetic sideslip measurements are being fused |
| `cs_mag_field_disturbed` | `bool` | 16 - true when the mag field does not match the expected strength |
| `cs_fixed_wing` | `bool` | 17 - true when the vehicle is operating as a fixed wing vehicle |
| `cs_mag_fault` | `bool` | 18 - true when the magnetometer has been declared faulty and is no longer being used |
| `cs_fuse_aspd` | `bool` | 19 - true when airspeed measurements are being fused |
| `cs_gnd_effect` | `bool` | 20 - true when protection from ground effect induced static pressure rise is active |
| `cs_rng_stuck` | `bool` | 21 - true when rng data wasn't ready for more than 10s and new rng values haven't changed enough |
| `cs_gnss_yaw` | `bool` | 22 - true when yaw (not ground course) data fusion from a GPS receiver is intended |
| `cs_mag_aligned_in_flight` | `bool` | 23 - true when the in-flight mag field alignment has been completed |
| `cs_ev_vel` | `bool` | 24 - true when local frame velocity data fusion from external vision measurements is intended |
| `cs_synthetic_mag_z` | `bool` | 25 - true when we are using a synthesized measurement for the magnetometer Z component |
| `cs_vehicle_at_rest` | `bool` | 26 - true when the vehicle is at rest |
| `cs_gnss_yaw_fault` | `bool` | 27 - true when the GNSS heading has been declared faulty and is no longer being used |
| `cs_rng_fault` | `bool` | 28 - true when the range finder has been declared faulty and is no longer being used |
| `cs_inertial_dead_reckoning` | `bool` | 29 - true if we are no longer fusing measurements that constrain horizontal velocity drift |
| `cs_wind_dead_reckoning` | `bool` | 30 - true if we are navigationg reliant on wind relative measurements |
| `cs_rng_kin_consistent` | `bool` | 31 - true when the range finder kinematic consistency check is passing |
| `cs_fake_pos` | `bool` | 32 - true when fake position measurements are being fused |
| `cs_fake_hgt` | `bool` | 33 - true when fake height measurements are being fused |
| `cs_gravity_vector` | `bool` | 34 - true when gravity vector measurements are being fused |
| `cs_mag` | `bool` | 35 - true if 3-axis magnetometer measurement fusion (mag states only) is intended |
| `cs_ev_yaw_fault` | `bool` | 36 - true when the EV heading has been declared faulty and is no longer being used |
| `cs_mag_heading_consistent` | `bool` | 37 - true when the heading obtained from mag data is declared consistent with the filter |
| `cs_aux_gpos` | `bool` | 38 - true if auxiliary global position measurement fusion is intended |
| `cs_rng_terrain` | `bool` | 39 - true if we are fusing range finder data for terrain |
| `cs_opt_flow_terrain` | `bool` | 40 - true if we are fusing flow data for terrain |
| `cs_valid_fake_pos` | `bool` | 41 - true if a valid constant position is being fused |
| `cs_constant_pos` | `bool` | 42 - true if the vehicle is at a constant position |
| `cs_baro_fault` | `bool` | 43 - true when the current baro has been declared faulty and is no longer being used |
| `cs_gnss_vel` | `bool` | 44 - true if GNSS velocity measurement fusion is intended |
| `cs_gnss_fault` | `bool` | 45 - true if GNSS true if GNSS measurements (lat, lon, vel) have been declared faulty |
| `cs_yaw_manual` | `bool` | 46 - true if yaw has been set manually |
| `cs_gnss_hgt_fault` | `bool` | 47 - true if GNSS true if GNSS measurements (alt) have been declared faulty |
| `fault_status_changes` | `uint32` | number of filter fault status (fs) changes |
| `fs_bad_mag_x` | `bool` | 0 - true if the fusion of the magnetometer X-axis has encountered a numerical error |
| `fs_bad_mag_y` | `bool` | 1 - true if the fusion of the magnetometer Y-axis has encountered a numerical error |
| `fs_bad_mag_z` | `bool` | 2 - true if the fusion of the magnetometer Z-axis has encountered a numerical error |
| `fs_bad_hdg` | `bool` | 3 - true if the fusion of the heading angle has encountered a numerical error |
| `fs_bad_mag_decl` | `bool` | 4 - true if the fusion of the magnetic declination has encountered a numerical error |
| `fs_bad_airspeed` | `bool` | 5 - true if fusion of the airspeed has encountered a numerical error |
| `fs_bad_sideslip` | `bool` | 6 - true if fusion of the synthetic sideslip constraint has encountered a numerical error |
| `fs_bad_optflow_x` | `bool` | 7 - true if fusion of the optical flow X axis has encountered a numerical error |
| `fs_bad_optflow_y` | `bool` | 8 - true if fusion of the optical flow Y axis has encountered a numerical error |
| `fs_bad_acc_vertical` | `bool` | 10 - true if bad vertical accelerometer data has been detected |
| `fs_bad_acc_clipping` | `bool` | 11 - true if delta velocity data contains clipping (asymmetric railing) |
| `innovation_fault_status_changes` | `uint32` | number of innovation fault status (reject) changes |
| `reject_hor_vel` | `bool` | 0 - true if horizontal velocity observations have been rejected |
| `reject_ver_vel` | `bool` | 1 - true if vertical velocity observations have been rejected |
| `reject_hor_pos` | `bool` | 2 - true if horizontal position observations have been rejected |
| `reject_ver_pos` | `bool` | 3 - true if vertical position observations have been rejected |
| `reject_yaw` | `bool` | 7 - true if the yaw observation has been rejected |
| `reject_airspeed` | `bool` | 8 - true if the airspeed observation has been rejected |
| `reject_sideslip` | `bool` | 9 - true if the synthetic sideslip observation has been rejected |
| `reject_hagl` | `bool` | 10 - true if the height above ground observation has been rejected |
| `reject_optflow_x` | `bool` | 11 - true if the X optical flow observation has been rejected |
| `reject_optflow_y` | `bool` | 12 - true if the Y optical flow observation has been rejected |

## EventV0

內部訊息 · 主題名 `event_v0`

this message is required here in the msg_old folder because other msg are depending on it Events interface

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `id` | `uint32` | Event ID |
| `event_sequence` | `uint16` | Event sequence number |
| `arguments` | `uint8[25]` | (optional) arguments, depend on event id |
| `log_levels` | `uint8` | Log levels: 4 bits MSB: internal, 4 bits LSB: external |

常數:`MESSAGE_VERSION=0`、`ORB_QUEUE_LENGTH=16`

## FailsafeFlags

內部訊息 · 主題名 `failsafe_flags`

Input flags for the failsafe state machine set by the arming & health checks. Flags must be named such that false == no failure (e.g. _invalid, _unhealthy, _lost) The flag comments are used as label for the failsafe state machine simulation

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `mode_req_angular_velocity` | `uint32` |  |
| `mode_req_attitude` | `uint32` |  |
| `mode_req_local_alt` | `uint32` |  |
| `mode_req_local_position` | `uint32` |  |
| `mode_req_local_position_relaxed` | `uint32` |  |
| `mode_req_global_position` | `uint32` |  |
| `mode_req_global_position_relaxed` | `uint32` |  |
| `mode_req_mission` | `uint32` |  |
| `mode_req_offboard_signal` | `uint32` |  |
| `mode_req_home_position` | `uint32` |  |
| `mode_req_wind_and_flight_time_compliance` | `uint32` | if set, mode cannot be entered if wind or flight time limit exceeded |
| `mode_req_prevent_arming` | `uint32` | if set, cannot arm while in this mode |
| `mode_req_manual_control` | `uint32` |  |
| `mode_req_other` | `uint32` | other requirements, not covered above (for external modes) |
| `angular_velocity_invalid` | `bool` | Angular velocity invalid |
| `attitude_invalid` | `bool` | Attitude invalid |
| `local_altitude_invalid` | `bool` | Local altitude invalid |
| `local_position_invalid` | `bool` | Local position estimate invalid |
| `local_position_invalid_relaxed` | `bool` | Local position with reduced accuracy requirements invalid (e.g. flying with optical flow) |
| `local_velocity_invalid` | `bool` | Local velocity estimate invalid |
| `global_position_invalid` | `bool` | Global position estimate invalid |
| `global_position_invalid_relaxed` | `bool` | Global position estimate invalid with relaxed accuracy requirements |
| `auto_mission_missing` | `bool` | No mission available |
| `offboard_control_signal_lost` | `bool` | Offboard signal lost |
| `home_position_invalid` | `bool` | No home position available |
| `manual_control_signal_lost` | `bool` | Manual control (RC) signal lost |
| `gcs_connection_lost` | `bool` | GCS connection lost |
| `battery_warning` | `uint8` | Battery warning level (see BatteryStatus.msg) |
| `battery_low_remaining_time` | `bool` | Low battery based on remaining flight time |
| `battery_unhealthy` | `bool` | Battery unhealthy |
| `geofence_breached` | `bool` | Geofence breached (one or multiple) |
| `mission_failure` | `bool` | Mission failure |
| `vtol_fixed_wing_system_failure` | `bool` | vehicle in fixed-wing system failure failsafe mode (after quad-chute) |
| `wind_limit_exceeded` | `bool` | Wind limit exceeded |
| `flight_time_limit_exceeded` | `bool` | Maximum flight time exceeded |
| `position_accuracy_low` | `bool` | Position estimate has dropped below threshold, but is currently still declared valid |
| `navigator_failure` | `bool` | Navigator failed to execute a mode |
| `fd_critical_failure` | `bool` | Critical failure (attitude/altitude limit exceeded, or external ATS) |
| `fd_esc_arming_failure` | `bool` | ESC failed to arm |
| `fd_imbalanced_prop` | `bool` | Imbalanced propeller detected |
| `fd_motor_failure` | `bool` | Motor failure |

## FailureDetectorStatus

內部訊息 · 主題名 `failure_detector_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `fd_roll` | `bool` |  |
| `fd_pitch` | `bool` |  |
| `fd_alt` | `bool` |  |
| `fd_ext` | `bool` |  |
| `fd_arm_escs` | `bool` |  |
| `fd_battery` | `bool` |  |
| `fd_imbalanced_prop` | `bool` |  |
| `fd_motor` | `bool` |  |
| `imbalanced_prop_metric` | `float32` | Metric of the imbalanced propeller check (low-passed) |
| `motor_failure_mask` | `uint16` | Bit-mask with motor indices, indicating critical motor failures |
| `motor_stop_mask` | `uint16` | Bitmaks of motors stopped by failure injection |

## FigureEightStatus

內部訊息 · 主題名 `figure_eight_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `major_radius` | `float32` | Major axis radius of the figure eight [m]. Positive values orbit clockwise, negative values orbit counter-clockwise. |
| `minor_radius` | `float32` | Minor axis radius of the figure eight [m]. |
| `orientation` | `float32` | Orientation of the major axis of the figure eight [rad]. |
| `frame` | `uint8` | The coordinate system of the fields: x, y, z. |
| `x` | `int32` | X coordinate of center point. Coordinate system depends on frame field: local = x position in meters * 1e4, global = latitude in degrees * 1e7. |
| `y` | `int32` | Y coordinate of center point. Coordinate system depends on frame field: local = y position in meters * 1e4, global = latitude in degrees * 1e7. |
| `z` | `float32` | Altitude of center point. Coordinate system depends on frame field. |

## FixedWingLateralGuidanceStatus

內部訊息 · 主題名 `fixed_wing_lateral_guidance_status`

Fixed Wing Lateral Guidance Status message Published by fw_pos_control module to report the resultant lateral setpoints and NPFG debug outputs

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `course_setpoint` | `float32` | [rad] [@range -pi, pi] Desired direction of travel over ground w.r.t (true) North. Set by guidance law |
| `lateral_acceleration_ff` | `float32` | [m/s^2] [FRD] lateral acceleration demand only for maintaining curvature |
| `bearing_feas` | `float32` | [@range 0,1] bearing feasibility |
| `bearing_feas_on_track` | `float32` | [@range 0,1] on-track bearing feasibility |
| `signed_track_error` | `float32` | [m] signed track error |
| `track_error_bound` | `float32` | [m] track error bound |
| `adapted_period` | `float32` | [s] adapted period (if auto-tuning enabled) |
| `wind_est_valid` | `uint8` | [boolean] true = wind estimate is valid and/or being used by controller (also indicates if wind estimate usage is disabled despite being valid) |

## FixedWingLateralStatus

內部訊息 · 主題名 `fixed_wing_lateral_status`

Fixed Wing Lateral Status message Published by the fw_lateral_longitudinal_control module to report the resultant lateral setpoint

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `lateral_acceleration_setpoint` | `float32` | [m/s^2] [FRD] resultant lateral acceleration setpoint |
| `can_run_factor` | `float32` | [norm] [@range 0, 1] estimate of certainty of the correct functionality of the npfg roll setpoint |

## FixedWingRunwayControl

內部訊息 · 主題名 `fixed_wing_runway_control`

Auxiliary control fields for fixed-wing runway takeoff/landing Passes information from the FixedWingModeManager to the FixedWingAttitudeController

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] time since system start |
| `wheel_steering_enabled` | `bool` | Flag that enables the wheel steering. |
| `wheel_steering_nudging_rate` | `float32` | [norm] [@range -1, 1] [FRD] Manual wheel nudging, added to controller output. NAN is interpreted as 0. |

## FlightPhaseEstimation

內部訊息 · 主題名 `flight_phase_estimation`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `flight_phase` | `uint8` | Estimate of current flight phase |

常數:`FLIGHT_PHASE_UNKNOWN=0`、`FLIGHT_PHASE_LEVEL=1`、`FLIGHT_PHASE_DESCEND=2`、`FLIGHT_PHASE_CLIMB=3`

## FollowTarget

內部訊息 · 主題名 `follow_target`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `lat` | `float64` | target position (deg * 1e7) |
| `lon` | `float64` | target position (deg * 1e7) |
| `alt` | `float32` | target position |
| `vy` | `float32` | target vel in y |
| `vx` | `float32` | target vel in x |
| `vz` | `float32` | target vel in z |
| `est_cap` | `uint8` | target reporting capabilities |

## FollowTargetEstimator

內部訊息 · 主題名 `follow_target_estimator`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `last_filter_reset_timestamp` | `uint64` | time of last filter reset (microseconds) |
| `valid` | `bool` | True if estimator states are okay to be used |
| `stale` | `bool` | True if estimator stopped receiving follow_target messages for some time. The estimate can still be valid, though it might be inaccurate. |
| `lat_est` | `float64` | Estimated target latitude |
| `lon_est` | `float64` | Estimated target longitude |
| `alt_est` | `float32` | Estimated target altitude |
| `pos_est` | `float32[3]` | Estimated target NED position (m) |
| `vel_est` | `float32[3]` | Estimated target NED velocity (m/s) |
| `acc_est` | `float32[3]` | Estimated target NED acceleration (m^2/s) |
| `prediction_count` | `uint64` |  |
| `fusion_count` | `uint64` |  |

## FollowTargetStatus

內部訊息 · 主題名 `follow_target_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [microseconds] time since system start |
| `tracked_target_course` | `float32` | [rad] Tracked target course in NED local frame (North is course zero) |
| `follow_angle` | `float32` | [rad] Current follow angle setting |
| `orbit_angle_setpoint` | `float32` | [rad] Current orbit angle setpoint from the smooth trajectory generator |
| `angular_rate_setpoint` | `float32` | [rad/s] Angular rate commanded from Jerk-limited Orbit Angle trajectory for Orbit Angle |
| `desired_position_raw` | `float32[3]` | [m] Raw 'idealistic' desired drone position if a drone could teleport from place to places |
| `in_emergency_ascent` | `bool` | [bool] True when doing emergency ascent (when distance to ground is below safety altitude) |
| `gimbal_pitch` | `float32` | [rad] Gimbal pitch commanded to track target in the center of the frame |

## FuelTankStatus

內部訊息 · 主題名 `fuel_tank_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `maximum_fuel_capacity` | `float32` | maximum fuel capacity. Must always be provided, either from the driver or a parameter |
| `consumed_fuel` | `float32` | consumed fuel, NaN if not measured. Should not be inferred from the max fuel capacity |
| `fuel_consumption_rate` | `float32` | fuel consumption rate, NaN if not measured |
| `percent_remaining` | `uint8` | percentage of remaining fuel, UINT8_MAX if not provided |
| `remaining_fuel` | `float32` | remaining fuel, NaN if not measured. Should not be inferred from the max fuel capacity |
| `fuel_tank_id` | `uint8` | identifier for the fuel tank. Must match ID of other messages for same fuel system. 0 by default when only a single tank exists |
| `fuel_type` | `uint32` | type of fuel based on MAV_FUEL_TYPE enum. Set to MAV_FUEL_TYPE_UNKNOWN if unknown or it does not fit the provided types |
| `temperature` | `float32` | fuel temperature in Kelvin, NaN if not measured |

常數:`MAV_FUEL_TYPE_UNKNOWN=0`、`MAV_FUEL_TYPE_LIQUID=1`、`MAV_FUEL_TYPE_GAS=2`

## GeneratorStatus

內部訊息 · 主題名 `generator_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `status` | `uint64` | Status flags |
| `battery_current` | `float32` | [A] Current into/out of battery. Positive for out. Negative for in. NaN: field not provided. |
| `load_current` | `float32` | [A] Current going to the UAV. If battery current not available this is the DC current from the generator. Positive for out. Negative for in. NaN: field not provided |
| `power_generated` | `float32` | [W] The power being generated. NaN: field not provided |
| `bus_voltage` | `float32` | [V] Voltage of the bus seen at the generator, or battery bus if battery bus is controlled by generator and at a different voltage to main bus. |
| `bat_current_setpoint` | `float32` | [A] The target battery current. Positive for out. Negative for in. NaN: field not provided |
| `runtime` | `uint32` | [s] Seconds this generator has run since it was rebooted. UINT32_MAX: field not provided. |
| `time_until_maintenance` | `int32` | [s] Seconds until this generator requires maintenance.  A negative value indicates maintenance is past-due. INT32_MAX: field not provided. |
| `generator_speed` | `uint16` | [rpm] Speed of electrical generator or alternator. UINT16_MAX: field not provided. |
| `rectifier_temperature` | `int16` | [degC] The temperature of the rectifier or power converter. INT16_MAX: field not provided. |
| `generator_temperature` | `int16` | [degC] The temperature of the mechanical motor, fuel cell core or generator. INT16_MAX: field not provided. |

常數:`STATUS_FLAG_OFF=1`、`STATUS_FLAG_READY=2`、`STATUS_FLAG_GENERATING=4`、`STATUS_FLAG_CHARGING=8`、`STATUS_FLAG_REDUCED_POWER=16`、`STATUS_FLAG_MAXPOWER=32`、`STATUS_FLAG_OVERTEMP_WARNING=64`、`STATUS_FLAG_OVERTEMP_FAULT=128`、`STATUS_FLAG_ELECTRONICS_OVERTEMP_WARNING=256`、`STATUS_FLAG_ELECTRONICS_OVERTEMP_FAULT=512`、`STATUS_FLAG_ELECTRONICS_FAULT=1024`、`STATUS_FLAG_POWERSOURCE_FAULT=2048`、`STATUS_FLAG_COMMUNICATION_WARNING=4096`、`STATUS_FLAG_COOLING_WARNING=8192`、`STATUS_FLAG_POWER_RAIL_FAULT=16384`、`STATUS_FLAG_OVERCURRENT_FAULT=32768`、`STATUS_FLAG_BATTERY_OVERCHARGE_CURRENT_FAULT=65536`、`STATUS_FLAG_OVERVOLTAGE_FAULT=131072`、`STATUS_FLAG_BATTERY_UNDERVOLT_FAULT=262144`、`STATUS_FLAG_START_INHIBITED=524288`、`STATUS_FLAG_MAINTENANCE_REQUIRED=1048576`、`STATUS_FLAG_WARMING_UP=2097152`、`STATUS_FLAG_IDLE=4194304`

## GeofenceResult

內部訊息 · 主題名 `geofence_result`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `geofence_max_dist_triggered` | `bool` | true the check for max distance from Home is triggered |
| `geofence_max_alt_triggered` | `bool` | true the check for max altitude above Home is triggered |
| `geofence_custom_fence_triggered` | `bool` | true the check for custom inclusion/exclusion geofence(s) is triggered |
| `geofence_action` | `uint8` | action to take when the geofence is breached |

常數:`GF_ACTION_NONE=0`、`GF_ACTION_WARN=1`、`GF_ACTION_LOITER=2`、`GF_ACTION_RTL=3`、`GF_ACTION_TERMINATE=4`、`GF_ACTION_LAND=5`

## GeofenceStatus

內部訊息 · 主題名 `geofence_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `geofence_id` | `uint32` | loaded geofence id |
| `status` | `uint8` | Current geofence status |

常數:`GF_STATUS_LOADING=0`、`GF_STATUS_READY=1`

## GimbalControls

內部訊息 · 主題名 `gimbal_controls`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp the data this control response is based on was sampled |
| `control` | `float32[3]` |  |

常數:`INDEX_ROLL=0`、`INDEX_PITCH=1`、`INDEX_YAW=2`

## GimbalDeviceAttitudeStatus

內部訊息 · 主題名 `gimbal_device_attitude_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `target_system` | `uint8` |  |
| `target_component` | `uint8` |  |
| `device_flags` | `uint16` |  |
| `q` | `float32[4]` |  |
| `angular_velocity_x` | `float32` |  |
| `angular_velocity_y` | `float32` |  |
| `angular_velocity_z` | `float32` |  |
| `failure_flags` | `uint32` |  |
| `delta_yaw` | `float32` |  |
| `delta_yaw_velocity` | `float32` |  |
| `gimbal_device_id` | `uint8` |  |
| `received_from_mavlink` | `bool` |  |

常數:`DEVICE_FLAGS_RETRACT=1`、`DEVICE_FLAGS_NEUTRAL=2`、`DEVICE_FLAGS_ROLL_LOCK=4`、`DEVICE_FLAGS_PITCH_LOCK=8`、`DEVICE_FLAGS_YAW_LOCK=16`、`DEVICE_FLAGS_YAW_IN_VEHICLE_FRAME=32`、`DEVICE_FLAGS_YAW_IN_EARTH_FRAME=64`

## GimbalDeviceInformation

內部訊息 · 主題名 `gimbal_device_information`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `vendor_name` | `uint8[32]` |  |
| `model_name` | `uint8[32]` |  |
| `custom_name` | `uint8[32]` |  |
| `firmware_version` | `uint32` |  |
| `hardware_version` | `uint32` |  |
| `uid` | `uint64` |  |
| `cap_flags` | `uint16` |  |
| `custom_cap_flags` | `uint16` |  |
| `roll_min` | `float32` | [rad] |
| `roll_max` | `float32` | [rad] |
| `pitch_min` | `float32` | [rad] |
| `pitch_max` | `float32` | [rad] |
| `yaw_min` | `float32` | [rad] |
| `yaw_max` | `float32` | [rad] |
| `gimbal_device_id` | `uint8` |  |

常數:`GIMBAL_DEVICE_CAP_FLAGS_HAS_RETRACT=1`、`GIMBAL_DEVICE_CAP_FLAGS_HAS_NEUTRAL=2`、`GIMBAL_DEVICE_CAP_FLAGS_HAS_ROLL_AXIS=4`、`GIMBAL_DEVICE_CAP_FLAGS_HAS_ROLL_FOLLOW=8`、`GIMBAL_DEVICE_CAP_FLAGS_HAS_ROLL_LOCK=16`、`GIMBAL_DEVICE_CAP_FLAGS_HAS_PITCH_AXIS=32`、`GIMBAL_DEVICE_CAP_FLAGS_HAS_PITCH_FOLLOW=64`、`GIMBAL_DEVICE_CAP_FLAGS_HAS_PITCH_LOCK=128`、`GIMBAL_DEVICE_CAP_FLAGS_HAS_YAW_AXIS=256`、`GIMBAL_DEVICE_CAP_FLAGS_HAS_YAW_FOLLOW=512`、`GIMBAL_DEVICE_CAP_FLAGS_HAS_YAW_LOCK=1024`、`GIMBAL_DEVICE_CAP_FLAGS_SUPPORTS_INFINITE_YAW=2048`

## GimbalDeviceSetAttitude

內部訊息 · 主題名 `gimbal_device_set_attitude`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `target_system` | `uint8` |  |
| `target_component` | `uint8` |  |
| `flags` | `uint16` |  |
| `q` | `float32[4]` |  |
| `angular_velocity_x` | `float32` |  |
| `angular_velocity_y` | `float32` |  |
| `angular_velocity_z` | `float32` |  |

常數:`GIMBAL_DEVICE_FLAGS_RETRACT=1`、`GIMBAL_DEVICE_FLAGS_NEUTRAL=2`、`GIMBAL_DEVICE_FLAGS_ROLL_LOCK=4`、`GIMBAL_DEVICE_FLAGS_PITCH_LOCK=8`、`GIMBAL_DEVICE_FLAGS_YAW_LOCK=16`

## GimbalManagerInformation

內部訊息 · 主題名 `gimbal_manager_information`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `cap_flags` | `uint32` |  |
| `gimbal_device_id` | `uint8` |  |
| `roll_min` | `float32` | [rad] |
| `roll_max` | `float32` | [rad] |
| `pitch_min` | `float32` | [rad] |
| `pitch_max` | `float32` | [rad] |
| `yaw_min` | `float32` | [rad] |
| `yaw_max` | `float32` | [rad] |

常數:`GIMBAL_MANAGER_CAP_FLAGS_HAS_RETRACT=1`、`GIMBAL_MANAGER_CAP_FLAGS_HAS_NEUTRAL=2`、`GIMBAL_MANAGER_CAP_FLAGS_HAS_ROLL_AXIS=4`、`GIMBAL_MANAGER_CAP_FLAGS_HAS_ROLL_FOLLOW=8`、`GIMBAL_MANAGER_CAP_FLAGS_HAS_ROLL_LOCK=16`、`GIMBAL_MANAGER_CAP_FLAGS_HAS_PITCH_AXIS=32`、`GIMBAL_MANAGER_CAP_FLAGS_HAS_PITCH_FOLLOW=64`、`GIMBAL_MANAGER_CAP_FLAGS_HAS_PITCH_LOCK=128`、`GIMBAL_MANAGER_CAP_FLAGS_HAS_YAW_AXIS=256`、`GIMBAL_MANAGER_CAP_FLAGS_HAS_YAW_FOLLOW=512`、`GIMBAL_MANAGER_CAP_FLAGS_HAS_YAW_LOCK=1024`、`GIMBAL_MANAGER_CAP_FLAGS_SUPPORTS_INFINITE_YAW=2048`、`GIMBAL_MANAGER_CAP_FLAGS_CAN_POINT_LOCATION_LOCAL=65536`、`GIMBAL_MANAGER_CAP_FLAGS_CAN_POINT_LOCATION_GLOBAL=131072`

## GimbalManagerSetAttitude

內部訊息 · 主題名 `gimbal_manager_set_attitude`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `origin_sysid` | `uint8` |  |
| `origin_compid` | `uint8` |  |
| `target_system` | `uint8` |  |
| `target_component` | `uint8` |  |
| `flags` | `uint32` |  |
| `gimbal_device_id` | `uint8` |  |
| `q` | `float32[4]` |  |
| `angular_velocity_x` | `float32` |  |
| `angular_velocity_y` | `float32` |  |
| `angular_velocity_z` | `float32` |  |

常數:`GIMBAL_MANAGER_FLAGS_RETRACT=1`、`GIMBAL_MANAGER_FLAGS_NEUTRAL=2`、`GIMBAL_MANAGER_FLAGS_ROLL_LOCK=4`、`GIMBAL_MANAGER_FLAGS_PITCH_LOCK=8`、`GIMBAL_MANAGER_FLAGS_YAW_LOCK=16`、`ORB_QUEUE_LENGTH=2`

## GimbalManagerSetManualControl

內部訊息 · 主題名 `gimbal_manager_set_manual_control`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `origin_sysid` | `uint8` |  |
| `origin_compid` | `uint8` |  |
| `target_system` | `uint8` |  |
| `target_component` | `uint8` |  |
| `flags` | `uint32` |  |
| `gimbal_device_id` | `uint8` |  |
| `pitch` | `float32` | unitless -1..1, can be NAN |
| `yaw` | `float32` | unitless -1..1, can be NAN |
| `pitch_rate` | `float32` | unitless -1..1, can be NAN |
| `yaw_rate` | `float32` | unitless -1..1, can be NAN |

常數:`GIMBAL_MANAGER_FLAGS_RETRACT=1`、`GIMBAL_MANAGER_FLAGS_NEUTRAL=2`、`GIMBAL_MANAGER_FLAGS_ROLL_LOCK=4`、`GIMBAL_MANAGER_FLAGS_PITCH_LOCK=8`、`GIMBAL_MANAGER_FLAGS_YAW_LOCK=16`

## GimbalManagerStatus

內部訊息 · 主題名 `gimbal_manager_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `flags` | `uint32` |  |
| `gimbal_device_id` | `uint8` |  |
| `primary_control_sysid` | `uint8` |  |
| `primary_control_compid` | `uint8` |  |
| `secondary_control_sysid` | `uint8` |  |
| `secondary_control_compid` | `uint8` |  |

## GpioConfig

內部訊息 · 主題名 `gpio_config`

GPIO configuration

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `device_id` | `uint32` | Device id |
| `mask` | `uint32` | Pin mask |
| `state` | `uint32` | Initial pin output state |
| `config` | `uint32` |  |

常數:`INPUT=0`、`OUTPUT=1`、`PULLUP=16`、`PULLDOWN=32`、`OPENDRAIN=256`、`INPUT_FLOATING=0`、`INPUT_PULLUP=16`、`INPUT_PULLDOWN=32`、`OUTPUT_PUSHPULL=0`、`OUTPUT_OPENDRAIN=256`、`OUTPUT_OPENDRAIN_PULLUP=272`

## GpioIn

內部訊息 · 主題名 `gpio_in`

GPIO mask and state

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `device_id` | `uint32` | Device id |
| `state` | `uint32` | pin state mask |

## GpioOut

內部訊息 · 主題名 `gpio_out`

GPIO mask and state

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `device_id` | `uint32` | Device id |
| `mask` | `uint32` | pin mask |
| `state` | `uint32` | pin state mask |

## GpioRequest

內部訊息 · 主題名 `gpio_request`

Request GPIO mask to be read

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `device_id` | `uint32` | Device id |

## GpsDump

內部訊息 · 主題名 `gps_dump`

This message is used to dump the raw gps communication to the log.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `instance` | `uint8` | Instance of GNSS receiver |
| `len` | `uint8` | length of data, MSB bit set = message to the gps device, |
| `data` | `uint8[79]` | data to write to the log |

常數:`ORB_QUEUE_LENGTH=8`

## GpsInjectData

內部訊息 · 主題名 `gps_inject_data`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `len` | `uint16` | length of data |
| `flags` | `uint8` | LSB: 1=fragmented |
| `data` | `uint8[300]` | data to write to GPS device (RTCM message) |

常數:`ORB_QUEUE_LENGTH=8`、`MAX_INSTANCES=2`

## Gripper

內部訊息 · 主題名 `gripper`

Used to command an actuation in the gripper, which is mapped to a specific output in the control allocation module

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` |  |
| `command` | `int8` | Commanded state for the gripper |

常數:`COMMAND_GRAB=0`、`COMMAND_RELEASE=1`

## HealthReport

內部訊息 · 主題名 `health_report`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `can_arm_mode_flags` | `uint64` | bitfield for each flight mode (NAVIGATION_STATE_*) if arming is possible |
| `can_run_mode_flags` | `uint64` | bitfield for each flight mode if it can run |
| `health_is_present_flags` | `uint64` | flags for each health_component_t |
| `health_warning_flags` | `uint64` |  |
| `health_error_flags` | `uint64` |  |
| `arming_check_warning_flags` | `uint64` |  |
| `arming_check_error_flags` | `uint64` |  |

## HeaterStatus

內部訊息 · 主題名 `heater_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `device_id` | `uint32` |  |
| `heater_on` | `bool` |  |
| `temperature_target_met` | `bool` |  |
| `temperature_sensor` | `float32` |  |
| `temperature_target` | `float32` |  |
| `controller_period_usec` | `uint32` |  |
| `controller_time_on_usec` | `uint32` |  |
| `proportional_value` | `float32` |  |
| `integrator_value` | `float32` |  |
| `feed_forward_value` | `float32` |  |
| `mode` | `uint8` |  |

常數:`MODE_GPIO=1`、`MODE_PX4IO=2`

## HomePositionV0

內部訊息 · 主題名 `home_position_v0`

GPS home position in WGS84 coordinates.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `lat` | `float64` | Latitude in degrees |
| `lon` | `float64` | Longitude in degrees |
| `alt` | `float32` | Altitude in meters (AMSL) |
| `x` | `float32` | X coordinate in meters |
| `y` | `float32` | Y coordinate in meters |
| `z` | `float32` | Z coordinate in meters |
| `yaw` | `float32` | Yaw angle in radians |
| `valid_alt` | `bool` | true when the altitude has been set |
| `valid_hpos` | `bool` | true when the latitude and longitude have been set |
| `valid_lpos` | `bool` | true when the local position (xyz) has been set |
| `manual_home` | `bool` | true when home position was set manually |
| `update_count` | `uint32` | update counter of the home position |

常數:`MESSAGE_VERSION=0`

## HoverThrustEstimate

內部訊息 · 主題名 `hover_thrust_estimate`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | time of corresponding sensor data last used for this estimate |
| `hover_thrust` | `float32` | estimated hover thrust [0.1, 0.9] |
| `hover_thrust_var` | `float32` | estimated hover thrust variance |
| `accel_innov` | `float32` | innovation of the last acceleration fusion |
| `accel_innov_var` | `float32` | innovation variance of the last acceleration fusion |
| `accel_innov_test_ratio` | `float32` | normalized innovation squared test ratio |
| `accel_noise_var` | `float32` | vertical acceleration noise variance estimated form innovation residual |
| `valid` | `bool` |  |

## InputRc

內部訊息 · 主題名 `input_rc`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_last_signal` | `uint64` | last valid reception time |
| `channel_count` | `uint8` | number of channels actually being seen |
| `rssi` | `int32` | receive signal strength indicator (RSSI): < 0: Undefined, 0: no signal, 100: full reception |
| `rc_failsafe` | `bool` | explicit failsafe flag: true on TX failure or TX out of range , false otherwise. Only the true state is reliable, as there are some (PPM) receivers on the market going into failsafe without telling us explicitly. |
| `rc_lost` | `bool` | RC receiver connection status: True,if no frame has arrived in the expected time, false otherwise. True usually means that the receiver has been disconnected, but can also indicate a radio link loss on "stupid" systems. Will remain false, if a RX with failsafe option continues to transmit frames after a link loss. |
| `rc_lost_frame_count` | `uint16` | Number of lost RC frames. Note: intended purpose: observe the radio link quality if RSSI is not available. This value must not be used to trigger any failsafe-alike functionality. |
| `rc_total_frame_count` | `uint16` | Number of total RC frames. Note: intended purpose: observe the radio link quality if RSSI is not available. This value must not be used to trigger any failsafe-alike functionality. |
| `rc_ppm_frame_length` | `uint16` | Length of a single PPM frame. Zero for non-PPM systems |
| `input_source` | `uint8` | Input source |
| `values` | `uint16[18]` | measured pulse widths for each of the supported channels |
| `link_quality` | `int8` | link quality. Percentage 0-100%. -1 = invalid |
| `rssi_dbm` | `float32` | Actual rssi in units of dBm. NaN = invalid |

常數:`RC_INPUT_SOURCE_UNKNOWN=0`、`RC_INPUT_SOURCE_PX4FMU_PPM=1`、`RC_INPUT_SOURCE_PX4IO_PPM=2`、`RC_INPUT_SOURCE_PX4IO_SPEKTRUM=3`、`RC_INPUT_SOURCE_PX4IO_SBUS=4`、`RC_INPUT_SOURCE_PX4IO_ST24=5`、`RC_INPUT_SOURCE_MAVLINK=6`、`RC_INPUT_SOURCE_QURT=7`、`RC_INPUT_SOURCE_PX4FMU_SPEKTRUM=8`、`RC_INPUT_SOURCE_PX4FMU_SBUS=9`、`RC_INPUT_SOURCE_PX4FMU_ST24=10`、`RC_INPUT_SOURCE_PX4FMU_SUMD=11`、`RC_INPUT_SOURCE_PX4FMU_DSM=12`、`RC_INPUT_SOURCE_PX4IO_SUMD=13`、`RC_INPUT_SOURCE_PX4FMU_CRSF=14`、`RC_INPUT_SOURCE_PX4FMU_GHST=15`、`RC_INPUT_MAX_CHANNELS=18`、`RSSI_MAX=100`

## InternalCombustionEngineControl

內部訊息 · 主題名 `internal_combustion_engine_control`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `ignition_on` | `bool` | activate/deactivate ignition (spark plug) |
| `throttle_control` | `float32` | setpoint for throttle actuator, with slew rate if enabled, idles with 0 [norm] [@range 0,1] [@uncontrolled NAN to stop motor] |
| `choke_control` | `float32` | setpoint for choke actuator, 1: fully closed [norm] [@range 0,1] |
| `starter_engine_control` | `float32` | setpoint for (electric) starter motor [norm] [@range 0,1] |
| `user_request` | `uint8` | user intent for the ICE being on/off |

## InternalCombustionEngineStatus

內部訊息 · 主題名 `internal_combustion_engine_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `state` | `uint8` |  |
| `flags` | `uint32` |  |
| `engine_load_percent` | `uint8` | Engine load estimate, percent, [0, 127] |
| `engine_speed_rpm` | `uint32` | Engine speed, revolutions per minute |
| `spark_dwell_time_ms` | `float32` | Spark dwell time, millisecond |
| `atmospheric_pressure_kpa` | `float32` | Atmospheric (barometric) pressure, kilopascal |
| `intake_manifold_pressure_kpa` | `float32` | Engine intake manifold pressure, kilopascal |
| `intake_manifold_temperature` | `float32` | Engine intake manifold temperature, kelvin |
| `coolant_temperature` | `float32` | Engine coolant temperature, kelvin |
| `oil_pressure` | `float32` | Oil pressure, kilopascal |
| `oil_temperature` | `float32` | Oil temperature, kelvin |
| `fuel_pressure` | `float32` | Fuel pressure, kilopascal |
| `fuel_consumption_rate_cm3pm` | `float32` | Instant fuel consumption estimate, (centimeter^3)/minute |
| `estimated_consumed_fuel_volume_cm3` | `float32` | Estimate of the consumed fuel since the start of the engine, centimeter^3 |
| `throttle_position_percent` | `uint8` | Throttle position, percent |
| `ecu_index` | `uint8` | The index of the publishing ECU |
| `spark_plug_usage` | `uint8` | Spark plug activity report. |
| `ignition_timing_deg` | `float32` | Cylinder ignition timing, angular degrees of the crankshaft |
| `injection_time_ms` | `float32` | Fuel injection time, millisecond |
| `cylinder_head_temperature` | `float32` | Cylinder head temperature (CHT), kelvin |
| `exhaust_gas_temperature` | `float32` | Exhaust gas temperature (EGT), kelvin |
| `lambda_coefficient` | `float32` | Estimated lambda coefficient, dimensionless ratio |

常數:`STATE_STOPPED=0`、`STATE_STARTING=1`、`STATE_RUNNING=2`、`STATE_FAULT=3`、`FLAG_GENERAL_ERROR=1`、`FLAG_CRANKSHAFT_SENSOR_ERROR_SUPPORTED=2`、`FLAG_CRANKSHAFT_SENSOR_ERROR=4`、`FLAG_TEMPERATURE_SUPPORTED=8`、`FLAG_TEMPERATURE_BELOW_NOMINAL=16`、`FLAG_TEMPERATURE_ABOVE_NOMINAL=32`、`FLAG_TEMPERATURE_OVERHEATING=64`、`FLAG_TEMPERATURE_EGT_ABOVE_NOMINAL=128`、`FLAG_FUEL_PRESSURE_SUPPORTED=256`、`FLAG_FUEL_PRESSURE_BELOW_NOMINAL=512`、`FLAG_FUEL_PRESSURE_ABOVE_NOMINAL=1024`、`FLAG_DETONATION_SUPPORTED=2048`、`FLAG_DETONATION_OBSERVED=4096`、`FLAG_MISFIRE_SUPPORTED=8192`、`FLAG_MISFIRE_OBSERVED=16384`、`FLAG_OIL_PRESSURE_SUPPORTED=32768`、`FLAG_OIL_PRESSURE_BELOW_NOMINAL=65536`、`FLAG_OIL_PRESSURE_ABOVE_NOMINAL=131072`、`FLAG_DEBRIS_SUPPORTED=262144`、`FLAG_DEBRIS_DETECTED=524288`、`SPARK_PLUG_SINGLE=0`、`SPARK_PLUG_FIRST_ACTIVE=1`、`SPARK_PLUG_SECOND_ACTIVE=2`、`SPARK_PLUG_BOTH_ACTIVE=3`

## IridiumsbdStatus

內部訊息 · 主題名 `iridiumsbd_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `last_at_ok_timestamp` | `uint64` | timestamp of the last "OK" received after the "AT" command |
| `tx_buf_write_index` | `uint16` | current size of the tx buffer |
| `rx_buf_read_index` | `uint16` | the rx buffer is parsed up to that index |
| `rx_buf_end_index` | `uint16` | current size of the rx buffer |
| `failed_sbd_sessions` | `uint16` | number of failed sbd sessions |
| `successful_sbd_sessions` | `uint16` | number of successful sbd sessions |
| `num_tx_buf_reset` | `uint16` | number of times the tx buffer was reset |
| `signal_quality` | `uint8` | current signal quality, 0 is no signal, 5 the best |
| `state` | `uint8` | current state of the driver, see the satcom_state of IridiumSBD.h for the definition |
| `ring_pending` | `bool` | indicates if a ring call is pending |
| `tx_buf_write_pending` | `bool` | indicates if a tx buffer write is pending |
| `tx_session_pending` | `bool` | indicates if a tx session is pending |
| `rx_read_pending` | `bool` | indicates if a rx read is pending |
| `rx_session_pending` | `bool` | indicates if a rx session is pending |

## IrlockReport

內部訊息 · 主題名 `irlock_report`

IRLOCK_REPORT message data

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `signature` | `uint16` |  |
| `pos_x` | `float32` | tan(theta), where theta is the angle between the target and the camera center of projection in camera x-axis |
| `pos_y` | `float32` | tan(theta), where theta is the angle between the target and the camera center of projection in camera y-axis |
| `size_x` | `float32` | /** size of target along camera x-axis in units of tan(theta) **/ |
| `size_y` | `float32` | /** size of target along camera y-axis in units of tan(theta) **/ |

## LandingGear

內部訊息 · 主題名 `landing_gear`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `landing_gear` | `int8` |  |

常數:`GEAR_UP=1`、`GEAR_DOWN=-1`、`GEAR_KEEP=0`

## LandingGearWheel

內部訊息 · 主題名 `landing_gear_wheel`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `normalized_wheel_setpoint` | `float32` | negative is turning left, positive turning right [-1, 1] |

## LandingTargetInnovations

內部訊息 · 主題名 `landing_target_innovations`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `innov_x` | `float32` |  |
| `innov_y` | `float32` |  |
| `innov_cov_x` | `float32` |  |
| `innov_cov_y` | `float32` |  |

## LandingTargetPose

內部訊息 · 主題名 `landing_target_pose`

Relative position of precision land target in navigation (body fixed, north aligned, NED) and inertial (world fixed, north aligned, NED) frames

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `is_static` | `bool` | Flag indicating whether the landing target is static or moving with respect to the ground |
| `rel_pos_valid` | `bool` | Flag showing whether relative position is valid |
| `rel_vel_valid` | `bool` | Flag showing whether relative velocity is valid |
| `x_rel` | `float32` | X/north position of target, relative to vehicle (navigation frame) [meters] |
| `y_rel` | `float32` | Y/east position of target, relative to vehicle (navigation frame) [meters] |
| `z_rel` | `float32` | Z/down position of target, relative to vehicle (navigation frame) [meters] |
| `vx_rel` | `float32` | X/north velocity  of target, relative to vehicle (navigation frame) [meters/second] |
| `vy_rel` | `float32` | Y/east velocity of target, relative to vehicle (navigation frame) [meters/second] |
| `cov_x_rel` | `float32` | X/north position variance [meters^2] |
| `cov_y_rel` | `float32` | Y/east position variance [meters^2] |
| `cov_vx_rel` | `float32` | X/north velocity variance [(meters/second)^2] |
| `cov_vy_rel` | `float32` | Y/east velocity variance [(meters/second)^2] |
| `abs_pos_valid` | `bool` | Flag showing whether absolute position is valid |
| `x_abs` | `float32` | X/north position of target, relative to origin (navigation frame) [meters] |
| `y_abs` | `float32` | Y/east position of target, relative to origin (navigation frame) [meters] |
| `z_abs` | `float32` | Z/down position of target, relative to origin (navigation frame) [meters] |

## LaunchDetectionStatus

內部訊息 · 主題名 `launch_detection_status`

Status of the launch detection state machine (fixed-wing only)

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `launch_detection_state` | `uint8` |  |

常數:`STATE_WAITING_FOR_LAUNCH=0`、`STATE_LAUNCH_DETECTED_DISABLED_MOTOR=1`、`STATE_FLYING=2`

## LedControl

內部訊息 · 主題名 `led_control`

LED control: control a single or multiple LED's. These are the externally visible LED's, not the board LED's

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `led_mask` | `uint8` | bitmask which LED(s) to control, set to 0xff for all |
| `color` | `uint8` | see COLOR_* |
| `mode` | `uint8` | see MODE_* |
| `num_blinks` | `uint8` | how many times to blink (number of on-off cycles if mode is one of MODE_BLINK_*) . Set to 0 for infinite |
| `priority` | `uint8` | priority: higher priority events will override current lower priority events (see MAX_PRIORITY) |

常數:`COLOR_OFF=0`、`COLOR_RED=1`、`COLOR_GREEN=2`、`COLOR_BLUE=3`、`COLOR_YELLOW=4`、`COLOR_PURPLE=5`、`COLOR_AMBER=6`、`COLOR_CYAN=7`、`COLOR_WHITE=8`、`MODE_OFF=0`、`MODE_ON=1`、`MODE_DISABLED=2`、`MODE_BLINK_SLOW=3`、`MODE_BLINK_NORMAL=4`、`MODE_BLINK_FAST=5`、`MODE_BREATHE=6`、`MODE_FLASH=7`、`MAX_PRIORITY=2`、`ORB_QUEUE_LENGTH=8`

## LogMessage

內部訊息 · 主題名 `log_message`

A logging message, output with PX4_WARN, PX4_ERR, PX4_INFO

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `severity` | `uint8` | log level (same as in the linux kernel, starting with 0) |
| `text` | `char[127]` |  |

常數:`ORB_QUEUE_LENGTH=4`

## LoggerStatus

內部訊息 · 主題名 `logger_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `type` | `uint8` |  |
| `backend` | `uint8` |  |
| `is_logging` | `bool` |  |
| `total_written_kb` | `float32` | total written to log in kiloBytes |
| `write_rate_kb_s` | `float32` | write rate in kiloBytes/s |
| `dropouts` | `uint32` | number of failed buffer writes due to buffer overflow |
| `message_gaps` | `uint32` | messages misssed |
| `buffer_used_bytes` | `uint32` | current buffer fill in Bytes |
| `buffer_size_bytes` | `uint32` | total buffer size in Bytes |
| `num_messages` | `uint8` |  |

常數:`LOGGER_TYPE_FULL=0`、`LOGGER_TYPE_MISSION=1`、`BACKEND_FILE=1`、`BACKEND_MAVLINK=2`、`BACKEND_ALL=3`

## MagWorkerData

內部訊息 · 主題名 `mag_worker_data`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `done_count` | `uint32` |  |
| `calibration_points_perside` | `uint32` |  |
| `calibration_interval_perside_us` | `uint64` |  |
| `calibration_counter_total` | `uint32[4]` |  |
| `side_data_collected` | `bool[4]` |  |
| `x` | `float32[4]` |  |
| `y` | `float32[4]` |  |
| `z` | `float32[4]` |  |

常數:`MAX_MAGS=4`

## MagnetometerBiasEstimate

內部訊息 · 主題名 `magnetometer_bias_estimate`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `bias_x` | `float32[4]` | estimated X-bias of all the sensors |
| `bias_y` | `float32[4]` | estimated Y-bias of all the sensors |
| `bias_z` | `float32[4]` | estimated Z-bias of all the sensors |
| `valid` | `bool[4]` | true if the estimator has converged |
| `stable` | `bool[4]` |  |

## ManualControlSwitches

內部訊息 · 主題名 `manual_control_switches`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `mode_slot` | `uint8` | the slot a specific model selector is in |
| `arm_switch` | `uint8` | arm/disarm switch: _DISARMED_, ARMED |
| `return_switch` | `uint8` | return to launch 2 position switch (mandatory): _NORMAL_, RTL |
| `loiter_switch` | `uint8` | loiter 2 position switch (optional): _MISSION_, LOITER |
| `offboard_switch` | `uint8` | offboard 2 position switch (optional): _NORMAL_, OFFBOARD |
| `kill_switch` | `uint8` | throttle kill: _NORMAL_, KILL |
| `termination_switch` | `uint8` | trigger termination which cannot be undone |
| `gear_switch` | `uint8` | landing gear switch: _DOWN_, UP |
| `transition_switch` | `uint8` | VTOL transition switch: _HOVER, FORWARD_FLIGHT |
| `photo_switch` | `uint8` | Photo trigger switch |
| `video_switch` | `uint8` | Photo trigger switch |
| `engage_main_motor_switch` | `uint8` | Engage the main motor (for helicopters) |
| `payload_power_switch` | `uint8` | Payload power switch |
| `switch_changes` | `uint32` | number of switch changes |

常數:`SWITCH_POS_NONE=0`、`SWITCH_POS_ON=1`、`SWITCH_POS_MIDDLE=2`、`SWITCH_POS_OFF=3`、`MODE_SLOT_NONE=0`、`MODE_SLOT_1=1`、`MODE_SLOT_2=2`、`MODE_SLOT_3=3`、`MODE_SLOT_4=4`、`MODE_SLOT_5=5`、`MODE_SLOT_6=6`、`MODE_SLOT_NUM=6`

## MavlinkLog

內部訊息 · 主題名 `mavlink_log`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `text` | `char[127]` |  |
| `severity` | `uint8` | log level (same as in the linux kernel, starting with 0) |

常數:`ORB_QUEUE_LENGTH=8`

## MavlinkTunnel

內部訊息 · 主題名 `mavlink_tunnel`、`esc_serial_passthru`

MAV_TUNNEL_PAYLOAD_TYPE enum

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | Time since system start (microseconds) |
| `payload_type` | `uint16` | A code that identifies the content of the payload (0 for unknown, which is the default). If this code is less than 32768, it is a 'registered' payload type and the corresponding code should be added to the MAV_TUNNEL_PAYLOAD_TYPE enum. Software creators can register blocks of types as needed. Codes greater than 32767 are considered local experiments and should not be checked in to any widely distributed codebase. |
| `target_system` | `uint8` | System ID (can be 0 for broadcast, but this is discouraged) |
| `target_component` | `uint8` | Component ID (can be 0 for broadcast, but this is discouraged) |
| `payload_length` | `uint8` | Length of the data transported in payload |
| `payload` | `uint8[128]` | Data itself |

常數:`MAV_TUNNEL_PAYLOAD_TYPE_UNKNOWN=0`、`MAV_TUNNEL_PAYLOAD_TYPE_STORM32_RESERVED0=200`、`MAV_TUNNEL_PAYLOAD_TYPE_STORM32_RESERVED1=201`、`MAV_TUNNEL_PAYLOAD_TYPE_STORM32_RESERVED2=202`、`MAV_TUNNEL_PAYLOAD_TYPE_STORM32_RESERVED3=203`、`MAV_TUNNEL_PAYLOAD_TYPE_STORM32_RESERVED4=204`、`MAV_TUNNEL_PAYLOAD_TYPE_STORM32_RESERVED5=205`、`MAV_TUNNEL_PAYLOAD_TYPE_STORM32_RESERVED6=206`、`MAV_TUNNEL_PAYLOAD_TYPE_STORM32_RESERVED7=207`、`MAV_TUNNEL_PAYLOAD_TYPE_STORM32_RESERVED8=208`、`MAV_TUNNEL_PAYLOAD_TYPE_STORM32_RESERVED9=209`

## MessageFormatRequest

內部訊息 · 主題名 `message_format_request`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `protocol_version` | `uint16` | Must be set to LATEST_PROTOCOL_VERSION. Do not change this field, it must be the first field after the timestamp |
| `topic_name` | `char[50]` | E.g. /fmu/in/vehicle_command |

常數:`LATEST_PROTOCOL_VERSION=1`

## MessageFormatResponse

內部訊息 · 主題名 `message_format_response`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `protocol_version` | `uint16` | Must be set to LATEST_PROTOCOL_VERSION. Do not change this field, it must be the first field after the timestamp |
| `topic_name` | `char[50]` | E.g. /fmu/in/vehicle_command |
| `success` | `bool` |  |
| `message_hash` | `uint32` | hash over all message fields |

## Mission

內部訊息 · 主題名 `mission`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `mission_dataman_id` | `uint8` | default 0, there are two offboard storage places in the dataman: 0 or 1 |
| `fence_dataman_id` | `uint8` | default 0, there are two offboard storage places in the dataman: 0 or 1 |
| `safepoint_dataman_id` | `uint8` | default 0, there are two offboard storage places in the dataman: 0 or 1 |
| `count` | `uint16` | count of the missions stored in the dataman |
| `current_seq` | `int32` | default -1, start at the one changed latest |
| `land_start_index` | `int32` | Index of the land start marker, if unavailable index of the land item, -1 otherwise |
| `land_index` | `int32` | Index of the land item, -1 otherwise |
| `mission_id` | `uint32` | indicates updates to the mission, reload from dataman if changed |
| `geofence_id` | `uint32` | indicates updates to the geofence, reload from dataman if changed |
| `safe_points_id` | `uint32` | indicates updates to the safe points, reload from dataman if changed |

## MissionResult

內部訊息 · 主題名 `mission_result`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `mission_id` | `uint32` | Id for the mission for which the result was generated |
| `geofence_id` | `uint32` | Id for the corresponding geofence for which the result was generated (used for mission feasibility) |
| `home_position_counter` | `uint32` | Counter of the home position for which the result was generated (used for mission feasibility) |
| `seq_reached` | `int32` | Sequence of the mission item which has been reached, default -1 |
| `seq_current` | `uint16` | Sequence of the current mission item |
| `seq_total` | `uint16` | Total number of mission items |
| `valid` | `bool` | true if mission is valid |
| `warning` | `bool` | true if mission is valid, but has potentially problematic items leading to safety warnings |
| `finished` | `bool` | true if mission has been completed |
| `failure` | `bool` | true if the mission cannot continue or be completed for some reason |
| `item_do_jump_changed` | `bool` | true if the number of do jumps remaining has changed |
| `item_changed_index` | `uint16` | indicate which item has changed |
| `item_do_jump_remaining` | `uint16` | set to the number of do jumps remaining for that item |
| `execution_mode` | `uint8` | indicates the mode in which the mission is executed |

## MountOrientation

內部訊息 · 主題名 `mount_orientation`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `attitude_euler_angle` | `float32[3]` | Attitude/direction of the mount as euler angles in rad |

## NavigatorMissionItem

內部訊息 · 主題名 `navigator_mission_item`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `sequence_current` | `uint16` | Sequence of the current mission item |
| `nav_cmd` | `uint16` |  |
| `latitude` | `float32` |  |
| `longitude` | `float32` |  |
| `time_inside` | `float32` | time that the MAV should stay inside the radius before advancing in seconds |
| `acceptance_radius` | `float32` | default radius in which the mission is accepted as reached in meters |
| `loiter_radius` | `float32` | loiter radius in meters, 0 for a VTOL to hover, negative for counter-clockwise |
| `yaw` | `float32` | in radians NED -PI..+PI, NAN means don't change yaw |
| `altitude` | `float32` | altitude in meters (AMSL) |
| `frame` | `uint8` | mission frame |
| `origin` | `uint8` | mission item origin (onboard or mavlink) |
| `loiter_exit_xtrack` | `bool` | exit xtrack location: 0 for center of loiter wp, 1 for exit location |
| `force_heading` | `bool` | heading needs to be reached |
| `altitude_is_relative` | `bool` | true if altitude is relative from start point |
| `autocontinue` | `bool` | true if next waypoint should follow after this one |
| `vtol_back_transition` | `bool` | part of the vtol back transition sequence |

## NavigatorStatus

內部訊息 · 主題名 `navigator_status`

Current status of a Navigator mode The possible values of nav_state are defined in the VehicleStatus msg.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `nav_state` | `uint8` | Source mode (values in VehicleStatus) |
| `failure` | `uint8` | Navigator failure enum |

常數:`FAILURE_NONE=0`、`FAILURE_HAGL=1`

## NeuralControl

內部訊息 · 主題名 `neural_control`

Neural control Debugging topic for the Neural controller, logs the inputs and output vectors of the neural network, and the time it takes to run Publisher: mc_nn_control Subscriber: logger

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `observation` | `float32[15]` | Observation vector (pos error (3), att (6d), lin vel (3), ang vel (3)) |
| `network_output` | `float32[4]` | Output from neural network |
| `controller_time` | `int32` | [us] Time spent from input to output |
| `inference_time` | `int32` | [us] Time spent for NN inference |

## NormalizedUnsignedSetpoint

內部訊息 · 主題名 `flaps_setpoint`、`spoilers_setpoint`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `normalized_setpoint` | `float32` | [0, 1] |

## ObstacleDistance

內部訊息 · 主題名 `obstacle_distance`、`obstacle_distance_fused`

Obstacle distances in front of the sensor.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `frame` | `uint8` | Coordinate frame of reference for the yaw rotation and offset of the sensor data. Defaults to MAV_FRAME_GLOBAL, which is North aligned. For body-mounted sensors use MAV_FRAME_BODY_FRD, which is vehicle front aligned. |
| `sensor_type` | `uint8` | Type from MAV_DISTANCE_SENSOR enum. |
| `distances` | `uint16[72]` | Distance of obstacles around the UAV with index 0 corresponding to local North. A value of 0 means that the obstacle is right in front of the sensor. A value of max_distance +1 means no obstacle is present. A value of UINT16_MAX for unknown/not used. In a array element, one unit corresponds to 1cm. |
| `increment` | `float32` | Angular width in degrees of each array element. |
| `min_distance` | `uint16` | Minimum distance the sensor can measure in centimeters. |
| `max_distance` | `uint16` | Maximum distance the sensor can measure in centimeters. |
| `angle_offset` | `float32` | Relative angle offset of the 0-index element in the distances array. Value of 0 corresponds to forward. Positive is clockwise direction, negative is counter-clockwise. |

常數:`MAV_FRAME_GLOBAL=0`、`MAV_FRAME_LOCAL_NED=1`、`MAV_FRAME_BODY_FRD=12`、`MAV_DISTANCE_SENSOR_LASER=0`、`MAV_DISTANCE_SENSOR_ULTRASOUND=1`、`MAV_DISTANCE_SENSOR_INFRARED=2`、`MAV_DISTANCE_SENSOR_RADAR=3`

## OffboardControlMode

內部訊息 · 主題名 `offboard_control_mode`

Off-board control mode

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `position` | `bool` |  |
| `velocity` | `bool` |  |
| `acceleration` | `bool` |  |
| `attitude` | `bool` |  |
| `body_rate` | `bool` |  |
| `thrust_and_torque` | `bool` |  |
| `direct_actuator` | `bool` |  |

## OnboardComputerStatus

內部訊息 · 主題名 `onboard_computer_status`

ONBOARD_COMPUTER_STATUS message data

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] time since system start (microseconds) |
| `uptime` | `uint32` | [ms] time since system boot of the companion (milliseconds) |
| `type` | `uint8` | type of onboard computer 0: Mission computer primary, 1: Mission computer backup 1, 2: Mission computer backup 2, 3: Compute node, 4-5: Compute spares, 6-9: Payload computers. |
| `cpu_cores` | `uint8[8]` | CPU usage on the component in percent |
| `cpu_combined` | `uint8[10]` | Combined CPU usage as the last 10 slices of 100 MS |
| `gpu_cores` | `uint8[4]` | GPU usage on the component in percent |
| `gpu_combined` | `uint8[10]` | Combined GPU usage as the last 10 slices of 100 MS |
| `temperature_board` | `int8` | [degC] Temperature of the board |
| `temperature_core` | `int8[8]` | [degC] Temperature of the CPU core |
| `fan_speed` | `int16[4]` | [rpm] Fan speeds |
| `ram_usage` | `uint32` | [MB] Amount of used RAM on the component system |
| `ram_total` | `uint32` | [MB] Total amount of RAM on the component system |
| `storage_type` | `uint32[4]` | Storage type: 0: HDD, 1: SSD, 2: EMMC, 3: SD card (non-removable), 4: SD card (removable) |
| `storage_usage` | `uint32[4]` | [MB] Amount of used storage space on the component system |
| `storage_total` | `uint32[4]` | [MB] Total amount of storage space on the component system |
| `link_type` | `uint32[6]` | [Kb/s] Link type: 0-9: UART, 10-19: Wired network, 20-29: Wifi, 30-39: Point-to-point proprietary, 40-49: Mesh proprietary |
| `link_tx_rate` | `uint32[6]` | [Kb/s] Network traffic from the component system |
| `link_rx_rate` | `uint32[6]` | [Kb/s] Network traffic to the component system |
| `link_tx_max` | `uint32[6]` | [Kb/s] Network capacity from the component system |
| `link_rx_max` | `uint32[6]` | [Kb/s] Network capacity to the component system |

## OpenDroneIdArmStatus

內部訊息 · 主題名 `open_drone_id_arm_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` |  |
| `status` | `uint8` |  |
| `error` | `char[50]` |  |

## OpenDroneIdOperatorId

內部訊息 · 主題名 `open_drone_id_operator_id`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` |  |
| `id_or_mac` | `uint8[20]` |  |
| `operator_id_type` | `uint8` |  |
| `operator_id` | `char[20]` |  |

## OpenDroneIdSelfId

內部訊息 · 主題名 `open_drone_id_self_id`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` |  |
| `id_or_mac` | `uint8[20]` |  |
| `description_type` | `uint8` |  |
| `description` | `char[23]` |  |

## OpenDroneIdSystem

內部訊息 · 主題名 `open_drone_id_system`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` |  |
| `id_or_mac` | `uint8[20]` |  |
| `operator_location_type` | `uint8` |  |
| `classification_type` | `uint8` |  |
| `operator_latitude` | `int32` |  |
| `operator_longitude` | `int32` |  |
| `area_count` | `uint16` |  |
| `area_radius` | `uint16` |  |
| `area_ceiling` | `float32` |  |
| `area_floor` | `float32` |  |
| `category_eu` | `uint8` |  |
| `class_eu` | `uint8` |  |
| `operator_altitude_geo` | `float32` |  |

## OrbTest

內部訊息 · 主題名 `orb_test`、`orb_multitest`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `val` | `int32` |  |

## OrbTestLarge

內部訊息 · 主題名 `orb_test_large`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `val` | `int32` |  |
| `junk` | `uint8[512]` |  |

## OrbTestMedium

內部訊息 · 主題名 `orb_test_medium`、`orb_test_medium_multi`、`orb_test_medium_wrap_around`、`orb_test_medium_queue`、`orb_test_medium_queue_poll`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `val` | `int32` |  |
| `junk` | `uint8[64]` |  |

常數:`ORB_QUEUE_LENGTH=16`

## OrbitStatus

內部訊息 · 主題名 `orbit_status`

ORBIT_YAW_BEHAVIOUR

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `radius` | `float32` | Radius of the orbit circle. Positive values orbit clockwise, negative values orbit counter-clockwise. [m] |
| `frame` | `uint8` | The coordinate system of the fields: x, y, z. |
| `x` | `float64` | X coordinate of center point. Coordinate system depends on frame field: local = x position in meters * 1e4, global = latitude in degrees * 1e7. |
| `y` | `float64` | Y coordinate of center point. Coordinate system depends on frame field: local = y position in meters * 1e4, global = latitude in degrees * 1e7. |
| `z` | `float32` | Altitude of center point. Coordinate system depends on frame field. |
| `yaw_behaviour` | `uint8` |  |

常數:`ORBIT_YAW_BEHAVIOUR_HOLD_FRONT_TO_CIRCLE_CENTER=0`、`ORBIT_YAW_BEHAVIOUR_HOLD_INITIAL_HEADING=1`、`ORBIT_YAW_BEHAVIOUR_UNCONTROLLED=2`、`ORBIT_YAW_BEHAVIOUR_HOLD_FRONT_TANGENT_TO_CIRCLE=3`、`ORBIT_YAW_BEHAVIOUR_RC_CONTROLLED=4`、`ORBIT_YAW_BEHAVIOUR_UNCHANGED=5`

## ParameterResetRequest

內部訊息 · 主題名 `parameter_reset_request`

ParameterResetRequest : Used by the primary to reset one or all parameter value(s) on the remote

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` |  |
| `parameter_index` | `uint16` |  |
| `reset_all` | `bool` | If this is true then ignore parameter_index |

常數:`ORB_QUEUE_LENGTH=4`

## ParameterSetUsedRequest

內部訊息 · 主題名 `parameter_set_used_request`

ParameterSetUsedRequest : Used by a remote to update the used flag for a parameter on the primary

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` |  |
| `parameter_index` | `uint16` |  |

常數:`ORB_QUEUE_LENGTH=64`

## ParameterSetValueRequest

內部訊息 · 主題名 `parameter_set_value_request`、`parameter_remote_set_value_request`、`parameter_primary_set_value_request`

ParameterSetValueRequest : Used by a remote or primary to update the value for a parameter at the other end

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` |  |
| `parameter_index` | `uint16` |  |
| `int_value` | `int32` | Optional value for an integer parameter |
| `float_value` | `float32` | Optional value for a float parameter |

常數:`ORB_QUEUE_LENGTH=32`

## ParameterSetValueResponse

內部訊息 · 主題名 `parameter_set_value_response`、`parameter_remote_set_value_response`、`parameter_primary_set_value_response`

ParameterSetValueResponse : Response to a set value request by either primary or secondary

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` |  |
| `request_timestamp` | `uint64` |  |
| `parameter_index` | `uint16` |  |

常數:`ORB_QUEUE_LENGTH=4`

## ParameterUpdate

內部訊息 · 主題名 `parameter_update`

This message is used to notify the system about one or more parameter changes

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `instance` | `uint32` | Instance count - constantly incrementing |
| `get_count` | `uint32` |  |
| `set_count` | `uint32` |  |
| `find_count` | `uint32` |  |
| `export_count` | `uint32` |  |
| `active` | `uint16` |  |
| `changed` | `uint16` |  |
| `custom_default` | `uint16` |  |

## Ping

內部訊息 · 主題名 `ping`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `ping_time` | `uint64` | Timestamp of the ping packet |
| `ping_sequence` | `uint32` | Sequence number of the ping packet |
| `dropped_packets` | `uint32` | Number of dropped ping packets |
| `rtt_ms` | `float32` | Round trip time (in ms) |
| `system_id` | `uint8` | System ID of the remote system |
| `component_id` | `uint8` | Component ID of the remote system |

## PositionControllerLandingStatus

內部訊息 · 主題名 `position_controller_landing_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] time since system start |
| `lateral_touchdown_offset` | `float32` | [m] lateral touchdown position offset manually commanded during landing |
| `flaring` | `bool` | true if the aircraft is flaring |
| `abort_status` | `uint8` |  |

常數:`NOT_ABORTED=0`、`ABORTED_BY_OPERATOR=1`、`TERRAIN_NOT_FOUND=2`、`TERRAIN_TIMEOUT=3`、`UNKNOWN_ABORT_CRITERION=4`

## PositionControllerStatus

內部訊息 · 主題名 `position_controller_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `nav_roll` | `float32` | Roll setpoint [rad] |
| `nav_pitch` | `float32` | Pitch setpoint [rad] |
| `nav_bearing` | `float32` | Bearing angle[rad] |
| `target_bearing` | `float32` | Bearing angle from aircraft to current target [rad] |
| `xtrack_error` | `float32` | Signed track error [m] |
| `wp_dist` | `float32` | Distance to active (next) waypoint [m] |
| `acceptance_radius` | `float32` | Current horizontal acceptance radius [m] |
| `type` | `uint8` | Current (applied) position setpoint type (see PositionSetpoint.msg) |

## PositionSetpoint

內部訊息 · 主題名 `position_setpoint`

this file is only used in the position_setpoint triple as a dependency

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `valid` | `bool` | true if setpoint is valid |
| `type` | `uint8` | setpoint type to adjust behavior of position controller |
| `vx` | `float32` | local velocity setpoint in m/s in NED |
| `vy` | `float32` | local velocity setpoint in m/s in NED |
| `vz` | `float32` | local velocity setpoint in m/s in NED |
| `lat` | `float64` | latitude, in deg |
| `lon` | `float64` | longitude, in deg |
| `alt` | `float32` | altitude AMSL, in m |
| `yaw` | `float32` | yaw (only in hover), in rad [-PI..PI), NaN = leave to flight task |
| `loiter_radius` | `float32` | [m] [@range 0, INF] loiter major axis radius |
| `loiter_minor_radius` | `float32` | [m] [@range 0, INF] loiter minor axis radius (used for non-circular loiter shapes) |
| `loiter_direction_counter_clockwise` | `bool` | loiter direction is clockwise by default and can be changed using this field |
| `loiter_orientation` | `float32` | [rad] [@range -pi, pi] orientation of the major axis with respect to true north |
| `loiter_pattern` | `uint8` | loitern pattern to follow |
| `acceptance_radius` | `float32` | horizontal acceptance_radius (meters) |
| `alt_acceptance_radius` | `float32` | vertical acceptance radius, only used for fixed wing guidance, NAN = let guidance choose (meters) |
| `cruising_speed` | `float32` | the generally desired cruising speed (not a hard constraint) |
| `gliding_enabled` | `bool` | commands the vehicle to glide if the capability is available (fixed wing only) |
| `cruising_throttle` | `float32` | the generally desired cruising throttle (not a hard constraint), only has an effect for rover |

常數:`SETPOINT_TYPE_POSITION=0`、`SETPOINT_TYPE_VELOCITY=1`、`SETPOINT_TYPE_LOITER=2`、`SETPOINT_TYPE_TAKEOFF=3`、`SETPOINT_TYPE_LAND=4`、`SETPOINT_TYPE_IDLE=5`、`LOITER_TYPE_ORBIT=0`、`LOITER_TYPE_FIGUREEIGHT=1`

## PositionSetpointTriplet

內部訊息 · 主題名 `position_setpoint_triplet`

Global position setpoint triplet in WGS84 coordinates. This are the three next waypoints (or just the next two or one).

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `previous` | `PositionSetpoint` |  |
| `current` | `PositionSetpoint` |  |
| `next` | `PositionSetpoint` |  |

## PowerButtonState

內部訊息 · 主題名 `power_button_state`

power button state notification message

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `event` | `uint8` | one of PWR_BUTTON_STATE_* |

常數:`PWR_BUTTON_STATE_IDEL=0`、`PWR_BUTTON_STATE_DOWN=1`、`PWR_BUTTON_STATE_UP=2`、`PWR_BUTTON_STATE_REQUEST_SHUTDOWN=3`

## PowerMonitor

內部訊息 · 主題名 `power_monitor`

power monitor message

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | Time since system start (microseconds) |
| `voltage_v` | `float32` | Voltage in volts, 0 if unknown |
| `current_a` | `float32` | Current in amperes, -1 if unknown |
| `power_w` | `float32` | power in watts, -1 if unknown |
| `rconf` | `int16` |  |
| `rsv` | `int16` |  |
| `rbv` | `int16` |  |
| `rp` | `int16` |  |
| `rc` | `int16` |  |
| `rcal` | `int16` |  |
| `me` | `int16` |  |
| `al` | `int16` |  |

## PpsCapture

內部訊息 · 主題名 `pps_capture`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) at PPS capture event |
| `rtc_timestamp` | `uint64` | Corrected GPS UTC timestamp at PPS capture event |
| `pps_rate_exceeded_counter` | `uint8` | Increments when PPS dt < 50ms |

## PurePursuitStatus

內部訊息 · 主題名 `pure_pursuit_status`

Pure pursuit status

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `lookahead_distance` | `float32` | [m] [@range 0, inf] Lookahead distance of pure the pursuit controller |
| `target_bearing` | `float32` | [rad] [@range -pi, pi] [@frame NED] Target bearing calculated by the pure pursuit controller |
| `crosstrack_error` | `float32` | [m] [@range -inf (Left of the path), inf (Right of the path)] Shortest distance from the vehicle to the path |
| `distance_to_waypoint` | `float32` | [m] [@range -inf, inf]Distance from the vehicle to the current waypoint |
| `bearing_to_waypoint` | `float32` | [rad] [@range -pi, pi] [@frame NED]Bearing towards current waypoint |

## PwmInput

內部訊息 · 主題名 `pwm_input`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | Time since system start (microseconds) |
| `error_count` | `uint64` | Timer overcapture error flag (AUX5 or MAIN5) |
| `pulse_width` | `uint32` | Pulse width, timer counts (microseconds) |
| `period` | `uint32` | Period, timer counts (microseconds) |

## Px4ioStatus

內部訊息 · 主題名 `px4io_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `free_memory_bytes` | `uint16` |  |
| `voltage_v` | `float32` | Servo rail voltage in volts |
| `rssi_v` | `float32` | RSSI pin voltage in volts |
| `status_arm_sync` | `bool` |  |
| `status_failsafe` | `bool` |  |
| `status_fmu_initialized` | `bool` |  |
| `status_fmu_ok` | `bool` |  |
| `status_init_ok` | `bool` |  |
| `status_outputs_armed` | `bool` |  |
| `status_raw_pwm` | `bool` |  |
| `status_rc_ok` | `bool` |  |
| `status_rc_dsm` | `bool` |  |
| `status_rc_ppm` | `bool` |  |
| `status_rc_sbus` | `bool` |  |
| `status_rc_st24` | `bool` |  |
| `status_rc_sumd` | `bool` |  |
| `status_safety_button_event` | `bool` | px4io safety button was pressed for longer than 1 second |
| `alarm_pwm_error` | `bool` |  |
| `alarm_rc_lost` | `bool` |  |
| `arming_failsafe_custom` | `bool` |  |
| `arming_fmu_armed` | `bool` |  |
| `arming_fmu_prearmed` | `bool` |  |
| `arming_termination` | `bool` |  |
| `arming_io_arm_ok` | `bool` |  |
| `arming_lockdown` | `bool` |  |
| `arming_termination_failsafe` | `bool` |  |
| `pwm` | `uint16[8]` |  |
| `pwm_disarmed` | `uint16[8]` |  |
| `pwm_failsafe` | `uint16[8]` |  |
| `pwm_rate_hz` | `uint16[8]` |  |
| `raw_inputs` | `uint16[18]` |  |

## QshellReq

內部訊息 · 主題名 `qshell_req`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `cmd` | `char[100]` |  |
| `strlen` | `uint32` |  |
| `request_sequence` | `uint32` |  |

常數:`MAX_STRLEN=100`

## QshellRetval

內部訊息 · 主題名 `qshell_retval`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `return_value` | `int32` |  |
| `return_sequence` | `uint32` |  |

## RadioStatus

內部訊息 · 主題名 `radio_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `rssi` | `uint8` | local signal strength |
| `remote_rssi` | `uint8` | remote signal strength |
| `txbuf` | `uint8` | how full the tx buffer is as a percentage |
| `noise` | `uint8` | background noise level |
| `remote_noise` | `uint8` | remote background noise level |
| `rxerrors` | `uint16` | receive errors |
| `fix` | `uint16` | count of error corrected packets |

## RateCtrlStatus

內部訊息 · 主題名 `rate_ctrl_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `rollspeed_integ` | `float32` |  |
| `pitchspeed_integ` | `float32` |  |
| `yawspeed_integ` | `float32` |  |

## RcChannels

內部訊息 · 主題名 `rc_channels`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_last_valid` | `uint64` | Timestamp of last valid RC signal |
| `channels` | `float32[18]` | Scaled to -1..1 (throttle: 0..1) |
| `channel_count` | `uint8` | Number of valid channels |
| `function` | `int8[30]` | Functions mapping |
| `rssi` | `uint8` | Receive signal strength index |
| `signal_lost` | `bool` | Control signal lost, should be checked together with topic timeout |
| `frame_drop_count` | `uint32` | Number of dropped frames |

常數:`FUNCTION_THROTTLE=0`、`FUNCTION_ROLL=1`、`FUNCTION_PITCH=2`、`FUNCTION_YAW=3`、`FUNCTION_RETURN=4`、`FUNCTION_LOITER=5`、`FUNCTION_OFFBOARD=6`、`FUNCTION_FLAPS=7`、`FUNCTION_AUX_1=8`、`FUNCTION_AUX_2=9`、`FUNCTION_AUX_3=10`、`FUNCTION_AUX_4=11`、`FUNCTION_AUX_5=12`、`FUNCTION_AUX_6=13`、`FUNCTION_PARAM_1=14`、`FUNCTION_PARAM_2=15`、`FUNCTION_PARAM_3_5=16`、`FUNCTION_KILLSWITCH=17`、`FUNCTION_TRANSITION=18`、`FUNCTION_GEAR=19`、`FUNCTION_ARMSWITCH=20`、`FUNCTION_FLTBTN_SLOT_1=21`、`FUNCTION_FLTBTN_SLOT_2=22`、`FUNCTION_FLTBTN_SLOT_3=23`、`FUNCTION_FLTBTN_SLOT_4=24`、`FUNCTION_FLTBTN_SLOT_5=25`、`FUNCTION_FLTBTN_SLOT_6=26`、`FUNCTION_ENGAGE_MAIN_MOTOR=27`、`FUNCTION_PAYLOAD_POWER=28`、`FUNCTION_TERMINATION=29`、`FUNCTION_FLTBTN_SLOT_COUNT=6`

## RcParameterMap

內部訊息 · 主題名 `rc_parameter_map`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `valid` | `bool[3]` | true for RC-Param channels which are mapped to a param |
| `param_index` | `int32[3]` | corresponding param index, this field is ignored if set to -1, in this case param_id will be used |
| `param_id` | `char[51]` | MAP_NCHAN * (ID_LEN + 1) chars, corresponding param id, null terminated |
| `scale` | `float32[3]` | scale to map the RC input [-1, 1] to a parameter value |
| `value0` | `float32[3]` | initial value around which the parameter value is changed |
| `value_min` | `float32[3]` | minimal parameter value |
| `value_max` | `float32[3]` | minimal parameter value |

常數:`RC_PARAM_MAP_NCHAN=3`、`PARAM_ID_LEN=16`

## RoverAttitudeSetpoint

內部訊息 · 主題名 `rover_attitude_setpoint`

Rover Attitude Setpoint

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `yaw_setpoint` | `float32` | [rad] [@range -inf, inf] [@frame NED] Yaw setpoint |

## RoverAttitudeStatus

內部訊息 · 主題名 `rover_attitude_status`

Rover Attitude Status

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `measured_yaw` | `float32` | [rad] [@range -pi, pi] [@frame NED]Measured yaw |
| `adjusted_yaw_setpoint` | `float32` | [rad] [@range -pi, pi] [@frame NED] Yaw setpoint that is being tracked (Applied slew rates) |

## RoverPositionSetpoint

內部訊息 · 主題名 `rover_position_setpoint`

Rover Position Setpoint

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `position_ned` | `float32[2]` | [m] [@range -inf, inf] [@frame NED] Target position |
| `start_ned` | `float32[2]` | [m] [@range -inf, inf] [@frame NED] [@invalid NaN Defaults to vehicle position] Start position which specifies a line for the rover to track |
| `cruising_speed` | `float32` | [m/s] [@range 0, inf] [@invalid NaN Defaults to maximum speed] Cruising speed |
| `arrival_speed` | `float32` | [m/s] [@range 0, inf] [@invalid NaN Defaults to 0] Speed the rover should arrive at the target with |
| `yaw` | `float32` | [rad] [@range -pi,pi] [@frame NED] [@invalid NaN Defaults to vehicle yaw] Mecanum only: Specify vehicle yaw during travel |

## RoverRateSetpoint

內部訊息 · 主題名 `rover_rate_setpoint`

Rover Rate setpoint

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `yaw_rate_setpoint` | `float32` | [rad/s] [@range -inf, inf] [@frame NED] Yaw rate setpoint |

## RoverRateStatus

內部訊息 · 主題名 `rover_rate_status`

Rover Rate Status

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `measured_yaw_rate` | `float32` | [rad/s] [@range -inf, inf] [@frame NED] Measured yaw rate |
| `adjusted_yaw_rate_setpoint` | `float32` | [rad/s] [@range -inf, inf] [@frame NED] Yaw rate setpoint that is being tracked (Applied slew rates) |
| `pid_yaw_rate_integral` | `float32` | [-] [@range -1, 1] Integral of the PID for the closed loop yaw rate controller |

## RoverSpeedSetpoint

內部訊息 · 主題名 `rover_speed_setpoint`

Rover Speed Setpoint

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `speed_body_x` | `float32` | [m/s] [@range -inf (Backwards), inf (Forwards)] [@frame Body] Speed setpoint in body x direction |
| `speed_body_y` | `float32` | [m/s] [@range -inf (Left), inf (Right)] [@frame Body] [@invalid NaN If not mecanum] Mecanum only: Speed setpoint in body y direction |

## RoverSpeedStatus

內部訊息 · 主題名 `rover_speed_status`

Rover Velocity Status

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `measured_speed_body_x` | `float32` | [m/s] [@range -inf (Backwards), inf (Forwards)] [@frame Body] Measured speed in body x direction |
| `adjusted_speed_body_x_setpoint` | `float32` | [m/s] [@range -inf (Backwards), inf (Forwards)] [@frame Body] Speed setpoint in body x direction that is being tracked (Applied slew rates) |
| `pid_throttle_body_x_integral` | `float32` | [-] [@range -1, 1] Integral of the PID for the closed loop controller of the speed in body x direction |
| `measured_speed_body_y` | `float32` | [m/s] [@range -inf (Left), inf (Right)] [@frame Body] [@invalid NaN If not mecanum] Mecanum only: Measured speed in body y direction |
| `adjusted_speed_body_y_setpoint` | `float32` | [m/s] [@range -inf (Left), inf (Right)] [@frame Body] [@invalid NaN If not mecanum] Mecanum only: Speed setpoint in body y direction that is being tracked (Applied slew rates) |
| `pid_throttle_body_y_integral` | `float32` | [-] [@range -1, 1] [@invalid NaN If not mecanum] Mecanum only: Integral of the PID for the closed loop controller of the speed in body y direction |

## RoverSteeringSetpoint

內部訊息 · 主題名 `rover_steering_setpoint`

Rover Steering setpoint

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `normalized_steering_setpoint` | `float32` | [-] [@range -1 (Left), 1 (Right)] [@frame Body] Ackermann: Normalized steering angle, Differential/Mecanum: Normalized speed difference between the left and right wheels |

## RoverThrottleSetpoint

內部訊息 · 主題名 `rover_throttle_setpoint`

Rover Throttle setpoint

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `throttle_body_x` | `float32` | [-] [@range -1 (Backwards), 1 (Forwards)] [@frame Body] Throttle setpoint along body X axis |
| `throttle_body_y` | `float32` | [-] [@range -1 (Left), 1 (Right)] [@frame Body] [@invalid NaN If not mecanum] Mecanum only: Throttle setpoint along body Y axis |

## Rpm

內部訊息 · 主題名 `rpm`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `rpm_estimate` | `float32` | filtered revolutions per minute |
| `rpm_raw` | `float32` |  |

## RtlStatus

內部訊息 · 主題名 `rtl_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `safe_points_id` | `uint32` | unique ID of active set of safe_point_items |
| `is_evaluation_pending` | `bool` | flag if the RTL point needs reevaluation (e.g. new safe points available, but need loading). |
| `has_vtol_approach` | `bool` | flag if approaches are defined for current RTL_TYPE parameter setting |
| `rtl_type` | `uint8` | Type of RTL chosen |
| `safe_point_index` | `uint8` | index of the chosen safe point, if in RTL_STATUS_TYPE_DIRECT_SAFE_POINT mode |

常數:`RTL_STATUS_TYPE_NONE=0`、`RTL_STATUS_TYPE_DIRECT_SAFE_POINT=1`、`RTL_STATUS_TYPE_DIRECT_MISSION_LAND=2`、`RTL_STATUS_TYPE_FOLLOW_MISSION=3`、`RTL_STATUS_TYPE_FOLLOW_MISSION_REVERSE=4`

## RtlTimeEstimate

內部訊息 · 主題名 `rtl_time_estimate`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `valid` | `bool` | Flag indicating whether the time estiamtes are valid |
| `time_estimate` | `float32` | [s] Estimated time for RTL |
| `safe_time_estimate` | `float32` | [s] Same as time_estimate, but with safety factor and safety margin included (factor*t + margin) |

## SatelliteInfo

內部訊息 · 主題名 `satellite_info`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `count` | `uint8` | Number of satellites visible to the receiver |
| `svid` | `uint8[40]` | Space vehicle ID [1..255], see scheme below |
| `used` | `uint8[40]` | 0: Satellite not used, 1: used for navigation |
| `elevation` | `uint8[40]` | Elevation (0: right on top of receiver, 90: on the horizon) of satellite |
| `azimuth` | `uint8[40]` | Direction of satellite, 0: 0 deg, 255: 360 deg. |
| `snr` | `uint8[40]` | dBHz, Signal to noise ratio of satellite C/N0, range 0..99, zero when not tracking this satellite. |
| `prn` | `uint8[40]` | Satellite PRN code assignment, (psuedorandom number SBAS, valid codes are 120-144) |

常數:`SAT_INFO_MAX_SATELLITES=40`

## SensorAccel

內部訊息 · 主題名 `sensor_accel`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `x` | `float32` | acceleration in the FRD board frame X-axis in m/s^2 |
| `y` | `float32` | acceleration in the FRD board frame Y-axis in m/s^2 |
| `z` | `float32` | acceleration in the FRD board frame Z-axis in m/s^2 |
| `temperature` | `float32` | temperature in degrees Celsius |
| `error_count` | `uint32` |  |
| `clip_counter` | `uint8[3]` | clip count per axis in the sample period |
| `samples` | `uint8` | number of raw samples that went into this message |

常數:`ORB_QUEUE_LENGTH=8`

## SensorAccelFifo

內部訊息 · 主題名 `sensor_accel_fifo`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `dt` | `float32` | delta time between samples (microseconds) |
| `scale` | `float32` |  |
| `samples` | `uint8` | number of valid samples |
| `x` | `int16[32]` | acceleration in the FRD board frame X-axis in m/s^2 |
| `y` | `int16[32]` | acceleration in the FRD board frame Y-axis in m/s^2 |
| `z` | `int16[32]` | acceleration in the FRD board frame Z-axis in m/s^2 |

## SensorAirflow

內部訊息 · 主題名 `sensor_airflow`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `speed` | `float32` | the speed being reported by the wind / airflow sensor |
| `direction` | `float32` | the direction being reported by the wind / airflow sensor |
| `status` | `uint8` | Status code from the sensor |

## SensorBaro

內部訊息 · 主題名 `sensor_baro`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `pressure` | `float32` | static pressure measurement in Pascals |
| `temperature` | `float32` | temperature in degrees Celsius |
| `error_count` | `uint32` |  |

常數:`ORB_QUEUE_LENGTH=4`

## SensorCombined

內部訊息 · 主題名 `sensor_combined`

Sensor readings in SI-unit form. These fields are scaled and offset-compensated where possible and do not change with board revisions and sensor updates.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `gyro_rad` | `float32[3]` | average angular rate measured in the FRD body frame XYZ-axis in rad/s over the last gyro sampling period |
| `gyro_integral_dt` | `uint32` | gyro measurement sampling period in microseconds |
| `accelerometer_timestamp_relative` | `int32` | timestamp + accelerometer_timestamp_relative = Accelerometer timestamp |
| `accelerometer_m_s2` | `float32[3]` | average value acceleration measured in the FRD body frame XYZ-axis in m/s^2 over the last accelerometer sampling period |
| `accelerometer_integral_dt` | `uint32` | accelerometer measurement sampling period in microseconds |
| `accelerometer_clipping` | `uint8` | bitfield indicating if there was any accelerometer clipping (per axis) during the integration time frame |
| `gyro_clipping` | `uint8` | bitfield indicating if there was any gyro clipping (per axis) during the integration time frame |
| `accel_calibration_count` | `uint8` | Calibration changed counter. Monotonically increases whenever accelermeter calibration changes. |
| `gyro_calibration_count` | `uint8` | Calibration changed counter. Monotonically increases whenever rate gyro calibration changes. |

常數:`RELATIVE_TIMESTAMP_INVALID=2147483647`、`CLIPPING_X=1`、`CLIPPING_Y=2`、`CLIPPING_Z=4`

## SensorCorrection

內部訊息 · 主題名 `sensor_correction`

Sensor corrections in SI-unit form for the voted sensor

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `accel_device_ids` | `uint32[4]` |  |
| `accel_temperature` | `float32[4]` |  |
| `accel_offset_0` | `float32[3]` | accelerometer 0 offsets in the FRD board frame XYZ-axis in m/s^s |
| `accel_offset_1` | `float32[3]` | accelerometer 1 offsets in the FRD board frame XYZ-axis in m/s^s |
| `accel_offset_2` | `float32[3]` | accelerometer 2 offsets in the FRD board frame XYZ-axis in m/s^s |
| `accel_offset_3` | `float32[3]` | accelerometer 3 offsets in the FRD board frame XYZ-axis in m/s^s |
| `gyro_device_ids` | `uint32[4]` |  |
| `gyro_temperature` | `float32[4]` |  |
| `gyro_offset_0` | `float32[3]` | gyro 0 XYZ offsets in the sensor frame in rad/s |
| `gyro_offset_1` | `float32[3]` | gyro 1 XYZ offsets in the sensor frame in rad/s |
| `gyro_offset_2` | `float32[3]` | gyro 2 XYZ offsets in the sensor frame in rad/s |
| `gyro_offset_3` | `float32[3]` | gyro 3 XYZ offsets in the sensor frame in rad/s |
| `mag_device_ids` | `uint32[4]` |  |
| `mag_temperature` | `float32[4]` |  |
| `mag_offset_0` | `float32[3]` | magnetometer 0 offsets in the FRD board frame XYZ-axis in m/s^s |
| `mag_offset_1` | `float32[3]` | magnetometer 1 offsets in the FRD board frame XYZ-axis in m/s^s |
| `mag_offset_2` | `float32[3]` | magnetometer 2 offsets in the FRD board frame XYZ-axis in m/s^s |
| `mag_offset_3` | `float32[3]` | magnetometer 3 offsets in the FRD board frame XYZ-axis in m/s^s |
| `baro_device_ids` | `uint32[4]` |  |
| `baro_temperature` | `float32[4]` |  |
| `baro_offset_0` | `float32` | barometric pressure 0 offsets in the sensor frame in Pascals |
| `baro_offset_1` | `float32` | barometric pressure 1 offsets in the sensor frame in Pascals |
| `baro_offset_2` | `float32` | barometric pressure 2 offsets in the sensor frame in Pascals |
| `baro_offset_3` | `float32` | barometric pressure 3 offsets in the sensor frame in Pascals |

## SensorGnssRelative

內部訊息 · 主題名 `sensor_gnss_relative`

GNSS relative positioning information in NED frame. The NED frame is defined as the local topological system at the reference station.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | time since system start (microseconds) |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `time_utc_usec` | `uint64` | Timestamp (microseconds, UTC), this is the timestamp which comes from the gps module. It might be unavailable right after cold start, indicated by a value of 0 |
| `reference_station_id` | `uint16` | Reference Station ID |
| `position` | `float32[3]` | GPS NED relative position vector (m) |
| `position_accuracy` | `float32[3]` | Accuracy of relative position (m) |
| `heading` | `float32` | Heading of the relative position vector (radians) |
| `heading_accuracy` | `float32` | Accuracy of heading of the relative position vector (radians) |
| `position_length` | `float32` | Length of the position vector (m) |
| `accuracy_length` | `float32` | Accuracy of the position length (m) |
| `gnss_fix_ok` | `bool` | GNSS valid fix (i.e within DOP & accuracy masks) |
| `differential_solution` | `bool` | differential corrections were applied |
| `relative_position_valid` | `bool` |  |
| `carrier_solution_floating` | `bool` | carrier phase range solution with floating ambiguities |
| `carrier_solution_fixed` | `bool` | carrier phase range solution with fixed ambiguities |
| `moving_base_mode` | `bool` | if the receiver is operating in moving base mode |
| `reference_position_miss` | `bool` | extrapolated reference position was used to compute moving base solution this epoch |
| `reference_observations_miss` | `bool` | extrapolated reference observations were used to compute moving base solution this epoch |
| `heading_valid` | `bool` |  |
| `relative_position_normalized` | `bool` | the components of the relative position vector (including the high-precision parts) are normalized |

## SensorGnssStatus

內部訊息 · 主題名 `sensor_gnss_status`

Gnss quality indicators

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `quality_available` | `bool` | Set to true if quality indicators are available |
| `quality_corrections` | `uint8` | Corrections quality from 0 to 10, or 255 if not available |
| `quality_receiver` | `uint8` | Overall receiver operating status from 0 to 10, or 255 if not available |
| `quality_gnss_signals` | `uint8` | Quality of GNSS signals from 0 to 10, or 255 if not available |
| `quality_post_processing` | `uint8` | Expected post processing quality from 0 to 10, or 255 if not available |

## SensorGps

內部訊息 · 主題名 `sensor_gps`、`vehicle_gps_position`

GPS position in WGS84 coordinates. the field 'timestamp' is for the position & velocity (microseconds)

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `latitude_deg` | `float64` | Latitude in degrees, allows centimeter level RTK precision |
| `longitude_deg` | `float64` | Longitude in degrees, allows centimeter level RTK precision |
| `altitude_msl_m` | `float64` | Altitude above MSL, meters |
| `altitude_ellipsoid_m` | `float64` | Altitude above Ellipsoid, meters |
| `s_variance_m_s` | `float32` | GPS speed accuracy estimate, (metres/sec) |
| `c_variance_rad` | `float32` | GPS course accuracy estimate, (radians) |
| `fix_type` | `uint8` | Some applications will not use the value of this field unless it is at least two, so always correctly fill in the fix. |
| `eph` | `float32` | GPS horizontal position accuracy (metres) |
| `epv` | `float32` | GPS vertical position accuracy (metres) |
| `hdop` | `float32` | Horizontal dilution of precision |
| `vdop` | `float32` | Vertical dilution of precision |
| `noise_per_ms` | `int32` | GPS noise per millisecond |
| `automatic_gain_control` | `uint16` | Automatic gain control monitor |
| `jamming_state` | `uint8` | indicates whether jamming has been detected or suspected by the receivers. O: Unknown, 1: OK, 2: Mitigated, 3: Detected |
| `jamming_indicator` | `int32` | indicates jamming is occurring |
| `spoofing_state` | `uint8` | indicates whether spoofing has been detected or suspected by the receivers. O: Unknown, 1: OK, 2: Mitigated, 3: Detected |
| `authentication_state` | `uint8` | GPS signal authentication state |
| `vel_m_s` | `float32` | GPS ground speed, (metres/sec) |
| `vel_n_m_s` | `float32` | GPS North velocity, (metres/sec) |
| `vel_e_m_s` | `float32` | GPS East velocity, (metres/sec) |
| `vel_d_m_s` | `float32` | GPS Down velocity, (metres/sec) |
| `cog_rad` | `float32` | Course over ground (NOT heading, but direction of movement), -PI..PI, (radians) |
| `vel_ned_valid` | `bool` | True if NED velocity is valid |
| `timestamp_time_relative` | `int32` | timestamp + timestamp_time_relative = Time of the UTC timestamp since system start, (microseconds) |
| `time_utc_usec` | `uint64` | Timestamp (microseconds, UTC), this is the timestamp which comes from the gps module. It might be unavailable right after cold start, indicated by a value of 0 |
| `satellites_used` | `uint8` | Number of satellites used |
| `system_error` | `uint32` | General errors with the connected GPS receiver |
| `heading` | `float32` | heading angle of XYZ body frame rel to NED. Set to NaN if not available and updated (used for dual antenna GPS), (rad, [-PI, PI]) |
| `heading_offset` | `float32` | heading offset of dual antenna array in body frame. Set to NaN if not applicable. (rad, [-PI, PI]) |
| `heading_accuracy` | `float32` | heading accuracy (rad, [0, 2PI]) |
| `rtcm_injection_rate` | `float32` | RTCM message injection rate Hz |
| `selected_rtcm_instance` | `uint8` | uorb instance that is being used for RTCM corrections |
| `rtcm_crc_failed` | `bool` | RTCM message CRC failure detected |
| `rtcm_msg_used` | `uint8` | Indicates if the RTCM message was used successfully by the receiver |

常數:`FIX_TYPE_NONE=1`、`FIX_TYPE_2D=2`、`FIX_TYPE_3D=3`、`FIX_TYPE_RTCM_CODE_DIFFERENTIAL=4`、`FIX_TYPE_RTK_FLOAT=5`、`FIX_TYPE_RTK_FIXED=6`、`FIX_TYPE_EXTRAPOLATED=8`、`JAMMING_STATE_UNKNOWN=0`、`JAMMING_STATE_OK=1`、`JAMMING_STATE_MITIGATED=2`、`JAMMING_STATE_DETECTED=3`、`SPOOFING_STATE_UNKNOWN=0`、`SPOOFING_STATE_OK=1`、`SPOOFING_STATE_MITIGATED=2`、`SPOOFING_STATE_DETECTED=3`、`AUTHENTICATION_STATE_UNKNOWN=0`、`AUTHENTICATION_STATE_INITIALIZING=1`、`AUTHENTICATION_STATE_ERROR=2`、`AUTHENTICATION_STATE_OK=3`、`AUTHENTICATION_STATE_DISABLED=4`、`SYSTEM_ERROR_OK=0`、`SYSTEM_ERROR_INCOMING_CORRECTIONS=1`、`SYSTEM_ERROR_CONFIGURATION=2`、`SYSTEM_ERROR_SOFTWARE=4`、`SYSTEM_ERROR_ANTENNA=8`、`SYSTEM_ERROR_EVENT_CONGESTION=16`、`SYSTEM_ERROR_CPU_OVERLOAD=32`、`SYSTEM_ERROR_OUTPUT_CONGESTION=64`、`RTCM_MSG_USED_UNKNOWN=0`、`RTCM_MSG_USED_NOT_USED=1`、`RTCM_MSG_USED_USED=2`

## SensorGyro

內部訊息 · 主題名 `sensor_gyro`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `x` | `float32` | angular velocity in the FRD board frame X-axis in rad/s |
| `y` | `float32` | angular velocity in the FRD board frame Y-axis in rad/s |
| `z` | `float32` | angular velocity in the FRD board frame Z-axis in rad/s |
| `temperature` | `float32` | temperature in degrees Celsius |
| `error_count` | `uint32` |  |
| `clip_counter` | `uint8[3]` | clip count per axis in the sample period |
| `samples` | `uint8` | number of raw samples that went into this message |

常數:`ORB_QUEUE_LENGTH=8`

## SensorGyroFft

內部訊息 · 主題名 `sensor_gyro_fft`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `sensor_sample_rate_hz` | `float32` |  |
| `resolution_hz` | `float32` |  |
| `peak_frequencies_x` | `float32[3]` | x axis peak frequencies |
| `peak_frequencies_y` | `float32[3]` | y axis peak frequencies |
| `peak_frequencies_z` | `float32[3]` | z axis peak frequencies |
| `peak_snr_x` | `float32[3]` | x axis peak SNR |
| `peak_snr_y` | `float32[3]` | y axis peak SNR |
| `peak_snr_z` | `float32[3]` | z axis peak SNR |

## SensorGyroFifo

內部訊息 · 主題名 `sensor_gyro_fifo`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `dt` | `float32` | delta time between samples (microseconds) |
| `scale` | `float32` |  |
| `samples` | `uint8` | number of valid samples |
| `x` | `int16[32]` | angular velocity in the FRD board frame X-axis in rad/s |
| `y` | `int16[32]` | angular velocity in the FRD board frame Y-axis in rad/s |
| `z` | `int16[32]` | angular velocity in the FRD board frame Z-axis in rad/s |

常數:`ORB_QUEUE_LENGTH=4`

## SensorHygrometer

內部訊息 · 主題名 `sensor_hygrometer`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `temperature` | `float32` | Temperature provided by sensor (Celsius) |
| `humidity` | `float32` | Humidity provided by sensor |

## SensorMag

內部訊息 · 主題名 `sensor_mag`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `x` | `float32` | magnetic field in the FRD board frame X-axis in Gauss |
| `y` | `float32` | magnetic field in the FRD board frame Y-axis in Gauss |
| `z` | `float32` | magnetic field in the FRD board frame Z-axis in Gauss |
| `temperature` | `float32` | temperature in degrees Celsius |
| `error_count` | `uint32` |  |

常數:`ORB_QUEUE_LENGTH=4`

## SensorOpticalFlow

內部訊息 · 主題名 `sensor_optical_flow`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `pixel_flow` | `float32[2]` | (radians) optical flow in radians where a positive value is produced by a RH rotation of the sensor about the body axis |
| `delta_angle` | `float32[3]` | (radians) accumulated gyro radians where a positive value is produced by a RH rotation about the body axis. Set to NaN if flow sensor does not have 3-axis gyro data. |
| `delta_angle_available` | `bool` |  |
| `distance_m` | `float32` | (meters) Distance to the center of the flow field |
| `distance_available` | `bool` |  |
| `integration_timespan_us` | `uint32` | (microseconds) accumulation timespan in microseconds |
| `quality` | `uint8` | quality, 0: bad quality, 255: maximum quality |
| `error_count` | `uint32` |  |
| `max_flow_rate` | `float32` | (radians/s) Magnitude of maximum angular which the optical flow sensor can measure reliably |
| `min_ground_distance` | `float32` | (meters) Minimum distance from ground at which the optical flow sensor operates reliably |
| `max_ground_distance` | `float32` | (meters) Maximum distance from ground at which the optical flow sensor operates reliably |
| `mode` | `uint8` |  |

常數:`MODE_UNKNOWN=0`、`MODE_BRIGHT=1`、`MODE_LOWLIGHT=2`、`MODE_SUPER_LOWLIGHT=3`

## SensorPreflightMag

內部訊息 · 主題名 `sensor_preflight_mag`

Pre-flight sensor check metrics. The topic will not be updated when the vehicle is armed

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `mag_inconsistency_angle` | `float32` | maximum angle between magnetometer instance field vectors in radians. |

## SensorSelection

內部訊息 · 主題名 `sensor_selection`

Sensor ID's for the voted sensors output on the sensor_combined topic. Will be updated on startup of the sensor module and when sensor selection changes

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `accel_device_id` | `uint32` | unique device ID for the selected accelerometers |
| `gyro_device_id` | `uint32` | unique device ID for the selected rate gyros |

## SensorUwb

內部訊息 · 主題名 `sensor_uwb`

UWB distance contains the distance information measured by an ultra-wideband positioning system, such as Pozyx or NXP Rddrone.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `sessionid` | `uint32` | UWB SessionID |
| `time_offset` | `uint32` | Time between Ranging Rounds in ms |
| `counter` | `uint32` | Number of Ranges since last Start of Ranging |
| `mac` | `uint16` | MAC adress of Initiator (controller) |
| `mac_dest` | `uint16` | MAC adress of Responder (Controlee) |
| `status` | `uint16` | status feedback # |
| `nlos` | `uint8` | None line of site condition y/n |
| `distance` | `float32` | distance in m to the UWB receiver |
| `aoa_azimuth_dev` | `float32` | Angle of arrival of first incomming RX msg |
| `aoa_elevation_dev` | `float32` | Angle of arrival of first incomming RX msg |
| `aoa_azimuth_resp` | `float32` | Angle of arrival of first incomming RX msg at the responder |
| `aoa_elevation_resp` | `float32` | Angle of arrival of first incomming RX msg at the responder |
| `aoa_azimuth_fom` | `uint8` | AOA Azimuth FOM |
| `aoa_elevation_fom` | `uint8` | AOA Elevation FOM |
| `aoa_dest_azimuth_fom` | `uint8` | AOA Azimuth FOM |
| `aoa_dest_elevation_fom` | `uint8` | AOA Elevation FOM |
| `orientation` | `uint8` | Direction the sensor faces from MAV_SENSOR_ORIENTATION enum |
| `offset_x` | `float32` | UWB initiator offset in X axis (NED drone frame) |
| `offset_y` | `float32` | UWB initiator offset in Y axis (NED drone frame) |
| `offset_z` | `float32` | UWB initiator offset in Z axis (NED drone frame) |

## SensorsStatus

內部訊息 · 主題名 `sensors_status_baro`、`sensors_status_mag`

Sensor check metrics. This will be zero for a sensor that's primary or unpopulated.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `device_id_primary` | `uint32` | current primary device id for reference |
| `device_ids` | `uint32[4]` |  |
| `inconsistency` | `float32[4]` | magnitude of difference between sensor instance and mean |
| `healthy` | `bool[4]` | sensor healthy |
| `priority` | `uint8[4]` |  |
| `enabled` | `bool[4]` |  |
| `external` | `bool[4]` |  |

## SensorsStatusImu

內部訊息 · 主題名 `sensors_status_imu`

Sensor check metrics. This will be zero for a sensor that's primary or unpopulated.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `accel_device_id_primary` | `uint32` | current primary accel device id for reference |
| `accel_device_ids` | `uint32[4]` |  |
| `accel_inconsistency_m_s_s` | `float32[4]` | magnitude of acceleration difference between IMU instance and mean in m/s^2. |
| `accel_healthy` | `bool[4]` |  |
| `accel_priority` | `uint8[4]` |  |
| `gyro_device_id_primary` | `uint32` | current primary gyro device id for reference |
| `gyro_device_ids` | `uint32[4]` |  |
| `gyro_inconsistency_rad_s` | `float32[4]` | magnitude of angular rate difference between IMU instance and mean in (rad/s). |
| `gyro_healthy` | `bool[4]` |  |
| `gyro_priority` | `uint8[4]` |  |

## SystemPower

內部訊息 · 主題名 `system_power`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `voltage5v_v` | `float32` | peripheral 5V rail voltage |
| `voltage_payload_v` | `float32` | payload rail voltage |
| `sensors3v3` | `float32[4]` | Sensors 3V3 rail voltage |
| `sensors3v3_valid` | `uint8` | Sensors 3V3 rail voltage was read (bitfield). |
| `usb_connected` | `uint8` | USB is connected when 1 |
| `brick_valid` | `uint8` | brick bits power is good when bit 1 |
| `usb_valid` | `uint8` | USB is valid when 1 |
| `servo_valid` | `uint8` | servo power is good when 1 |
| `periph_5v_oc` | `uint8` | peripheral overcurrent when 1 |
| `hipower_5v_oc` | `uint8` | high power peripheral overcurrent when 1 |
| `comp_5v_valid` | `uint8` | 5V to companion valid |
| `can1_gps1_5v_valid` | `uint8` | 5V for CAN1/GPS1 valid |
| `payload_v_valid` | `uint8` | payload rail voltage is valid |

常數:`BRICK1_VALID_SHIFTS=0`、`BRICK1_VALID_MASK=1`、`BRICK2_VALID_SHIFTS=1`、`BRICK2_VALID_MASK=2`、`BRICK3_VALID_SHIFTS=2`、`BRICK3_VALID_MASK=4`、`BRICK4_VALID_SHIFTS=3`、`BRICK4_VALID_MASK=8`

## TakeoffStatus

內部訊息 · 主題名 `takeoff_status`

Status of the takeoff state machine currently just available for multicopters

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `takeoff_state` | `uint8` |  |
| `tilt_limit` | `float32` | limited tilt feasibility during takeoff, contains maximum tilt otherwise |

常數:`TAKEOFF_STATE_UNINITIALIZED=0`、`TAKEOFF_STATE_DISARMED=1`、`TAKEOFF_STATE_SPOOLUP=2`、`TAKEOFF_STATE_READY_FOR_TAKEOFF=3`、`TAKEOFF_STATE_RAMPUP=4`、`TAKEOFF_STATE_FLIGHT=5`

## TaskStackInfo

內部訊息 · 主題名 `task_stack_info`

stack information for a single running process

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `stack_free` | `uint16` |  |
| `task_name` | `char[24]` |  |

常數:`ORB_QUEUE_LENGTH=2`

## TecsStatus

內部訊息 · 主題名 `tecs_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `altitude_sp` | `float32` | Altitude setpoint AMSL [m] |
| `altitude_reference` | `float32` | Altitude setpoint reference AMSL [m] |
| `altitude_time_constant` | `float32` | Time constant of the altitude tracker [s] |
| `height_rate_reference` | `float32` | Height rate setpoint reference [m/s] |
| `height_rate_direct` | `float32` | Direct height rate setpoint from velocity reference generator [m/s] |
| `height_rate_setpoint` | `float32` | Height rate setpoint [m/s] |
| `height_rate` | `float32` | Height rate [m/s] |
| `equivalent_airspeed_sp` | `float32` | Equivalent airspeed setpoint [m/s] |
| `true_airspeed_sp` | `float32` | True airspeed setpoint [m/s] |
| `true_airspeed_filtered` | `float32` | True airspeed filtered [m/s] |
| `true_airspeed_derivative_sp` | `float32` | True airspeed derivative setpoint [m/s^2] |
| `true_airspeed_derivative` | `float32` | True airspeed derivative [m/s^2] |
| `true_airspeed_derivative_raw` | `float32` | True airspeed derivative raw [m/s^2] |
| `total_energy_rate_sp` | `float32` | Total energy rate setpoint [m^2/s^3] |
| `total_energy_rate` | `float32` | Total energy rate estimate [m^2/s^3] |
| `total_energy_balance_rate_sp` | `float32` | Energy balance rate setpoint [m^2/s^3] |
| `total_energy_balance_rate` | `float32` | Energy balance rate estimate [m^2/s^3] |
| `throttle_integ` | `float32` | Throttle integrator value [-] |
| `pitch_integ` | `float32` | Pitch integrator value [rad] |
| `throttle_sp` | `float32` | Current throttle setpoint [-] |
| `pitch_sp_rad` | `float32` | Current pitch setpoint [rad] |
| `throttle_trim` | `float32` | estimated throttle value [0,1] required to fly level at equivalent_airspeed_sp in the current atmospheric conditions |
| `underspeed_ratio` | `float32` | 0: no underspeed, 1: maximal underspeed. Controller takes measures to avoid stall proportional to ratio if >0. |
| `fast_descend_ratio` | `float32` | value indicating if fast descend mode is enabled with ramp up and ramp down [0-1] |

## TelemetryStatus

內部訊息 · 主題名 `telemetry_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `type` | `uint8` | type of the radio hardware (LINK_TYPE_*) |
| `mode` | `uint8` |  |
| `flow_control` | `bool` |  |
| `forwarding` | `bool` |  |
| `mavlink_v2` | `bool` |  |
| `ftp` | `bool` |  |
| `streams` | `uint8` |  |
| `data_rate` | `float32` | configured maximum data rate (Bytes/s) |
| `rate_multiplier` | `float32` |  |
| `tx_rate_avg` | `float32` | transmit rate average (Bytes/s) |
| `tx_error_rate_avg` | `float32` | transmit error rate average (Bytes/s) |
| `tx_message_count` | `uint32` | total message sent count |
| `tx_buffer_overruns` | `uint32` | number of TX buffer overruns |
| `rx_rate_avg` | `float32` | transmit rate average (Bytes/s) |
| `rx_message_count` | `uint32` | count of total messages received |
| `rx_message_lost_count` | `uint32` |  |
| `rx_buffer_overruns` | `uint32` | number of RX buffer overruns |
| `rx_parse_errors` | `uint32` | number of parse errors |
| `rx_packet_drop_count` | `uint32` | number of packet drops |
| `rx_message_lost_rate` | `float32` |  |
| `heartbeat_type_antenna_tracker` | `bool` | MAV_TYPE_ANTENNA_TRACKER |
| `heartbeat_type_gcs` | `bool` | MAV_TYPE_GCS |
| `heartbeat_type_onboard_controller` | `bool` | MAV_TYPE_ONBOARD_CONTROLLER |
| `heartbeat_type_gimbal` | `bool` | MAV_TYPE_GIMBAL |
| `heartbeat_type_adsb` | `bool` | MAV_TYPE_ADSB |
| `heartbeat_type_camera` | `bool` | MAV_TYPE_CAMERA |
| `heartbeat_type_parachute` | `bool` | MAV_TYPE_PARACHUTE |
| `heartbeat_type_open_drone_id` | `bool` | MAV_TYPE_ODID |
| `heartbeat_component_telemetry_radio` | `bool` | MAV_COMP_ID_TELEMETRY_RADIO |
| `heartbeat_component_log` | `bool` | MAV_COMP_ID_LOG |
| `heartbeat_component_osd` | `bool` | MAV_COMP_ID_OSD |
| `heartbeat_component_vio` | `bool` | MAV_COMP_ID_VISUAL_INERTIAL_ODOMETRY |
| `heartbeat_component_pairing_manager` | `bool` | MAV_COMP_ID_PAIRING_MANAGER |
| `heartbeat_component_udp_bridge` | `bool` | MAV_COMP_ID_UDP_BRIDGE |
| `heartbeat_component_uart_bridge` | `bool` | MAV_COMP_ID_UART_BRIDGE |
| `open_drone_id_system_healthy` | `bool` |  |
| `parachute_system_healthy` | `bool` |  |

常數:`LINK_TYPE_GENERIC=0`、`LINK_TYPE_UBIQUITY_BULLET=1`、`LINK_TYPE_WIRE=2`、`LINK_TYPE_USB=3`、`LINK_TYPE_IRIDIUM=4`、`HEARTBEAT_TIMEOUT_US=2500000`

## TiltrotorExtraControls

內部訊息 · 主題名 `tiltrotor_extra_controls`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `collective_tilt_normalized_setpoint` | `float32` | Collective tilt angle of motors of tiltrotor, 0: vertical, 1: horizontal [0, 1] |
| `collective_thrust_normalized_setpoint` | `float32` | Collective thrust setpoint [0, 1] |

## TimesyncStatus

內部訊息 · 主題名 `timesync_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `source_protocol` | `uint8` | timesync source |
| `remote_timestamp` | `uint64` | remote system timestamp (microseconds) |
| `observed_offset` | `int64` | raw time offset directly observed from this timesync packet (microseconds) |
| `estimated_offset` | `int64` | smoothed time offset between companion system and PX4 (microseconds) |
| `round_trip_time` | `uint32` | round trip time of this timesync packet (microseconds) |

常數:`SOURCE_PROTOCOL_UNKNOWN=0`、`SOURCE_PROTOCOL_MAVLINK=1`、`SOURCE_PROTOCOL_DDS=2`

## TrajectorySetpoint6dof

內部訊息 · 主題名 `trajectory_setpoint6dof`

Trajectory setpoint in NED frame Input to position controller.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `position` | `float32[3]` | in meters |
| `velocity` | `float32[3]` | in meters/second |
| `acceleration` | `float32[3]` | in meters/second^2 |
| `jerk` | `float32[3]` | in meters/second^3 (for logging only) |
| `quaternion` | `float32[4]` | unit quaternion |
| `angular_velocity` | `float32[3]` | angular velocity in radians/second |

## TransponderReport

內部訊息 · 主題名 `transponder_report`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `icao_address` | `uint32` | ICAO address |
| `lat` | `float64` | Latitude, expressed as degrees |
| `lon` | `float64` | Longitude, expressed as degrees |
| `altitude_type` | `uint8` | Type from ADSB_ALTITUDE_TYPE enum |
| `altitude` | `float32` | Altitude(ASL) in meters |
| `heading` | `float32` | Course over ground in radians, 0 to 2pi, 0 is north |
| `hor_velocity` | `float32` | The horizontal velocity in m/s |
| `ver_velocity` | `float32` | The vertical velocity in m/s, positive is up |
| `callsign` | `char[9]` | The callsign, 8+null |
| `emitter_type` | `uint8` | Type from ADSB_EMITTER_TYPE enum |
| `tslc` | `uint8` | Time since last communication in seconds |
| `flags` | `uint16` | Flags to indicate various statuses including valid data fields |
| `squawk` | `uint16` | Squawk code |
| `uas_id` | `uint8[18]` | Unique UAS ID |

常數:`PX4_ADSB_FLAGS_VALID_COORDS=1`、`PX4_ADSB_FLAGS_VALID_ALTITUDE=2`、`PX4_ADSB_FLAGS_VALID_HEADING=4`、`PX4_ADSB_FLAGS_VALID_VELOCITY=8`、`PX4_ADSB_FLAGS_VALID_CALLSIGN=16`、`PX4_ADSB_FLAGS_VALID_SQUAWK=32`、`PX4_ADSB_FLAGS_RETRANSLATE=256`、`ADSB_EMITTER_TYPE_NO_INFO=0`、`ADSB_EMITTER_TYPE_LIGHT=1`、`ADSB_EMITTER_TYPE_SMALL=2`、`ADSB_EMITTER_TYPE_LARGE=3`、`ADSB_EMITTER_TYPE_HIGH_VORTEX_LARGE=4`、`ADSB_EMITTER_TYPE_HEAVY=5`、`ADSB_EMITTER_TYPE_HIGHLY_MANUV=6`、`ADSB_EMITTER_TYPE_ROTOCRAFT=7`、`ADSB_EMITTER_TYPE_UNASSIGNED=8`、`ADSB_EMITTER_TYPE_GLIDER=9`、`ADSB_EMITTER_TYPE_LIGHTER_AIR=10`、`ADSB_EMITTER_TYPE_PARACHUTE=11`、`ADSB_EMITTER_TYPE_ULTRA_LIGHT=12`、`ADSB_EMITTER_TYPE_UNASSIGNED2=13`、`ADSB_EMITTER_TYPE_UAV=14`、`ADSB_EMITTER_TYPE_SPACE=15`、`ADSB_EMITTER_TYPE_UNASSGINED3=16`、`ADSB_EMITTER_TYPE_EMERGENCY_SURFACE=17`、`ADSB_EMITTER_TYPE_SERVICE_SURFACE=18`、`ADSB_EMITTER_TYPE_POINT_OBSTACLE=19`、`ADSB_EMITTER_TYPE_ENUM_END=20`、`ORB_QUEUE_LENGTH=16`

## TuneControl

內部訊息 · 主題名 `tune_control`

This message is used to control the tunes, when the tune_id is set to CUSTOM then the frequency, duration are used otherwise those values are ignored.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `tune_id` | `uint8` | tune_id corresponding to TuneID::* from the tune_defaults.h in the tunes library |
| `tune_override` | `bool` | if true the tune which is playing will be stopped and the new started |
| `frequency` | `uint16` | in Hz |
| `duration` | `uint32` | in us |
| `silence` | `uint32` | in us |
| `volume` | `uint8` | value between 0-100 if supported by backend |

常數:`TUNE_ID_STOP=0`、`TUNE_ID_STARTUP=1`、`TUNE_ID_ERROR=2`、`TUNE_ID_NOTIFY_POSITIVE=3`、`TUNE_ID_NOTIFY_NEUTRAL=4`、`TUNE_ID_NOTIFY_NEGATIVE=5`、`TUNE_ID_ARMING_WARNING=6`、`TUNE_ID_BATTERY_WARNING_SLOW=7`、`TUNE_ID_BATTERY_WARNING_FAST=8`、`TUNE_ID_GPS_WARNING=9`、`TUNE_ID_ARMING_FAILURE=10`、`TUNE_ID_PARACHUTE_RELEASE=11`、`TUNE_ID_SINGLE_BEEP=12`、`TUNE_ID_HOME_SET=13`、`TUNE_ID_SD_INIT=14`、`TUNE_ID_SD_ERROR=15`、`TUNE_ID_PROG_PX4IO=16`、`TUNE_ID_PROG_PX4IO_OK=17`、`TUNE_ID_PROG_PX4IO_ERR=18`、`TUNE_ID_POWER_OFF=19`、`NUMBER_OF_TUNES=20`、`VOLUME_LEVEL_MIN=0`、`VOLUME_LEVEL_DEFAULT=20`、`VOLUME_LEVEL_MAX=100`、`ORB_QUEUE_LENGTH=4`

## UavcanParameterRequest

內部訊息 · 主題名 `uavcan_parameter_request`

UAVCAN-MAVLink parameter bridge request type

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `message_type` | `uint8` | MAVLink message type: PARAM_REQUEST_READ, PARAM_REQUEST_LIST, PARAM_SET |
| `node_id` | `uint8` | UAVCAN node ID mapped from MAVLink component ID |
| `param_id` | `char[17]` | MAVLink/UAVCAN parameter name |
| `param_index` | `int16` | -1 if the param_id field should be used as identifier |
| `param_type` | `uint8` | MAVLink parameter type |
| `int_value` | `int64` | current value if param_type is int-like |
| `real_value` | `float32` | current value if param_type is float-like |

常數:`MESSAGE_TYPE_PARAM_REQUEST_READ=20`、`MESSAGE_TYPE_PARAM_REQUEST_LIST=21`、`MESSAGE_TYPE_PARAM_SET=23`、`NODE_ID_ALL=0`、`PARAM_TYPE_UINT8=1`、`PARAM_TYPE_INT64=8`、`PARAM_TYPE_REAL32=9`、`ORB_QUEUE_LENGTH=4`

## UavcanParameterValue

內部訊息 · 主題名 `uavcan_parameter_value`

UAVCAN-MAVLink parameter bridge response type

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `node_id` | `uint8` | UAVCAN node ID mapped from MAVLink component ID |
| `param_id` | `char[17]` | MAVLink/UAVCAN parameter name |
| `param_index` | `int16` | parameter index, if known |
| `param_count` | `uint16` | number of parameters exposed by the node |
| `param_type` | `uint8` | MAVLink parameter type |
| `int_value` | `int64` | current value if param_type is int-like |
| `real_value` | `float32` | current value if param_type is float-like |

## UlogStream

內部訊息 · 主題名 `ulog_stream`

Message to stream ULog data from the logger. Corresponds to the LOGGING_DATA mavlink message

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `length` | `uint8` | length of data |
| `first_message_offset` | `uint8` | offset into data where first message starts. This |
| `msg_sequence` | `uint16` | allows determine drops |
| `flags` | `uint8` | see FLAGS_* |
| `data` | `uint8[249]` | ulog data |

常數:`FLAGS_NEED_ACK=1`、`ORB_QUEUE_LENGTH=16`

## UlogStreamAck

內部訊息 · 主題名 `ulog_stream_ack`

Ack a previously sent ulog_stream message that had the NEED_ACK flag set

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `msg_sequence` | `uint16` |  |

常數:`ACK_TIMEOUT=50`、`ACK_MAX_TRIES=50`

## VehicleAcceleration

內部訊息 · 主題名 `vehicle_acceleration`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `xyz` | `float32[3]` | Bias corrected acceleration (including gravity) in the FRD body frame XYZ-axis in m/s^2 |

## VehicleAirData

內部訊息 · 主題名 `vehicle_air_data`

Vehicle air data Data from the currently selected barometer (plus ambient temperature from the source specified in temperature_source). Includes calculated data such as barometric altitude and air density.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | [us] Time since system start |
| `timestamp_sample` | `uint64` | [us] Timestamp of the raw data |
| `baro_device_id` | `uint32` | Unique device ID for the selected barometer |
| `baro_alt_meter` | `float32` | [m] [@frame MSL] Altitude above MSL calculated from temperature compensated baro sensor data using an ISA corrected for sea level pressure SENS_BARO_QNH |
| `baro_pressure_pa` | `float32` | [Pa] Absolute pressure |
| `ambient_temperature` | `float32` | [degC] Ambient temperature |
| `temperature_source` | `uint8` | Source of temperature data: 0: Default Temperature (15°C), 1: External Baro, 2: Airspeed |
| `rho` | `float32` | [kg/m^3] Air density |
| `calibration_count` | `uint8` | Calibration changed counter. Monotonically increases whenever calibration changes. |

## VehicleAngularAccelerationSetpoint

內部訊息 · 主題名 `vehicle_angular_acceleration_setpoint`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | timestamp of the data sample on which this message is based (microseconds) |
| `xyz` | `float32[3]` | angular acceleration about X, Y, Z body axis in rad/s^2 |

## VehicleAttitudeSetpointV0

內部訊息 · 主題名 `vehicle_attitude_setpoint`、`mc_virtual_attitude_setpoint`、`fw_virtual_attitude_setpoint`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `yaw_sp_move_rate` | `float32` | rad/s (commanded by user) |
| `q_d` | `float32[4]` | Desired quaternion for quaternion control |
| `thrust_body` | `float32[3]` | Normalized thrust command in body FRD frame [-1,1] |
| `reset_integral` | `bool` | Reset roll/pitch/yaw integrals (navigation logic change) |
| `fw_control_yaw_wheel` | `bool` | control heading with steering wheel (used for auto takeoff on runway) |

常數:`MESSAGE_VERSION=0`

## VehicleConstraints

內部訊息 · 主題名 `vehicle_constraints`

Local setpoint constraints in NED frame setting something to NaN means that no limit is provided

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `speed_up` | `float32` | in meters/sec |
| `speed_down` | `float32` | in meters/sec |
| `want_takeoff` | `bool` | tell the controller to initiate takeoff when idling (ignored during flight) |

## VehicleImu

內部訊息 · 主題名 `vehicle_imu`

IMU readings in SI-unit form.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `accel_device_id` | `uint32` | Accelerometer unique device ID for the sensor that does not change between power cycles |
| `gyro_device_id` | `uint32` | Gyroscope unique device ID for the sensor that does not change between power cycles |
| `delta_angle` | `float32[3]` | delta angle about the FRD body frame XYZ-axis in rad over the integration time frame (delta_angle_dt) |
| `delta_velocity` | `float32[3]` | delta velocity in the FRD body frame XYZ-axis in m/s over the integration time frame (delta_velocity_dt) |
| `delta_angle_dt` | `uint32` | integration period in microseconds |
| `delta_velocity_dt` | `uint32` | integration period in microseconds |
| `delta_angle_clipping` | `uint8` | bitfield indicating if there was any gyro clipping (per axis) during the integration time frame |
| `delta_velocity_clipping` | `uint8` | bitfield indicating if there was any accelerometer clipping (per axis) during the integration time frame |
| `accel_calibration_count` | `uint8` | Calibration changed counter. Monotonically increases whenever accelermeter calibration changes. |
| `gyro_calibration_count` | `uint8` | Calibration changed counter. Monotonically increases whenever rate gyro calibration changes. |

常數:`CLIPPING_X=1`、`CLIPPING_Y=2`、`CLIPPING_Z=4`

## VehicleImuStatus

內部訊息 · 主題名 `vehicle_imu_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `accel_device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `gyro_device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `accel_clipping` | `uint32[3]` | total clipping per axis |
| `gyro_clipping` | `uint32[3]` | total clipping per axis |
| `accel_error_count` | `uint32` |  |
| `gyro_error_count` | `uint32` |  |
| `accel_rate_hz` | `float32` |  |
| `gyro_rate_hz` | `float32` |  |
| `accel_raw_rate_hz` | `float32` | full raw sensor sample rate (Hz) |
| `gyro_raw_rate_hz` | `float32` | full raw sensor sample rate (Hz) |
| `accel_vibration_metric` | `float32` | high frequency vibration level in the accelerometer data (m/s/s) |
| `gyro_vibration_metric` | `float32` | high frequency vibration level in the gyro data (rad/s) |
| `delta_angle_coning_metric` | `float32` | average IMU delta angle coning correction (rad^2) |
| `mean_accel` | `float32[3]` | average accelerometer readings since last publication |
| `mean_gyro` | `float32[3]` | average gyroscope readings since last publication |
| `var_accel` | `float32[3]` | accelerometer variance since last publication |
| `var_gyro` | `float32[3]` | gyroscope variance since last publication |
| `temperature_accel` | `float32` |  |
| `temperature_gyro` | `float32` |  |

## VehicleLocalPositionSetpoint

內部訊息 · 主題名 `vehicle_local_position_setpoint`

Local position setpoint in NED frame Telemetry of PID position controller to monitor tracking. NaN means the state was not controlled

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `x` | `float32` | in meters NED |
| `y` | `float32` | in meters NED |
| `z` | `float32` | in meters NED |
| `vx` | `float32` | in meters/sec |
| `vy` | `float32` | in meters/sec |
| `vz` | `float32` | in meters/sec |
| `acceleration` | `float32[3]` | in meters/sec^2 |
| `thrust` | `float32[3]` | normalized thrust vector in NED |
| `yaw` | `float32` | in radians NED -PI..+PI |
| `yawspeed` | `float32` | in radians/sec |

## VehicleLocalPositionV0

內部訊息 · 主題名 `vehicle_local_position`、`vehicle_local_position_groundtruth`、`external_ins_local_position`、`estimator_local_position`

Fused local position in NED. The coordinate system origin is the vehicle position at the time when the EKF2-module was started.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `xy_valid` | `bool` | true if x and y are valid |
| `z_valid` | `bool` | true if z is valid |
| `v_xy_valid` | `bool` | true if vx and vy are valid |
| `v_z_valid` | `bool` | true if vz is valid |
| `x` | `float32` | North position in NED earth-fixed frame, (metres) |
| `y` | `float32` | East position in NED earth-fixed frame, (metres) |
| `z` | `float32` | Down position (negative altitude) in NED earth-fixed frame, (metres) |
| `delta_xy` | `float32[2]` | Amount of lateral shift of position estimate in latest reset (in x and y) [m] |
| `xy_reset_counter` | `uint8` | Index of latest lateral position estimate reset |
| `delta_z` | `float32` | Amount of vertical shift of position estimate in latest reset [m] |
| `z_reset_counter` | `uint8` | Index of latest vertical position estimate reset |
| `vx` | `float32` | North velocity in NED earth-fixed frame, (metres/sec) |
| `vy` | `float32` | East velocity in NED earth-fixed frame, (metres/sec) |
| `vz` | `float32` | Down velocity in NED earth-fixed frame, (metres/sec) |
| `z_deriv` | `float32` | Down position time derivative in NED earth-fixed frame, (metres/sec) |
| `delta_vxy` | `float32[2]` | Amount of lateral shift of velocity estimate in latest reset (in x and y) [m/s] |
| `vxy_reset_counter` | `uint8` | Index of latest vertical velocity estimate reset |
| `delta_vz` | `float32` | Amount of vertical shift of velocity estimate in latest reset [m/s] |
| `vz_reset_counter` | `uint8` | Index of latest vertical velocity estimate reset |
| `ax` | `float32` | North velocity derivative in NED earth-fixed frame, (metres/sec^2) |
| `ay` | `float32` | East velocity derivative in NED earth-fixed frame, (metres/sec^2) |
| `az` | `float32` | Down velocity derivative in NED earth-fixed frame, (metres/sec^2) |
| `heading` | `float32` | Euler yaw angle transforming the tangent plane relative to NED earth-fixed frame, -PI..+PI,  (radians) |
| `heading_var` | `float32` |  |
| `unaided_heading` | `float32` | Same as heading but generated by integrating corrected gyro data only |
| `delta_heading` | `float32` | Heading delta caused by latest heading reset [rad] |
| `heading_reset_counter` | `uint8` | Index of latest heading reset |
| `heading_good_for_control` | `bool` |  |
| `tilt_var` | `float32` |  |
| `xy_global` | `bool` | true if position (x, y) has a valid global reference (ref_lat, ref_lon) |
| `z_global` | `bool` | true if z has a valid global reference (ref_alt) |
| `ref_timestamp` | `uint64` | Time when reference position was set since system start, (microseconds) |
| `ref_lat` | `float64` | Reference point latitude, (degrees) |
| `ref_lon` | `float64` | Reference point longitude, (degrees) |
| `ref_alt` | `float32` | Reference altitude AMSL, (metres) |
| `dist_bottom_valid` | `bool` | true if distance to bottom surface is valid |
| `dist_bottom` | `float32` | Distance from from bottom surface to ground, (metres) |
| `dist_bottom_var` | `float32` | terrain estimate variance (m^2) |
| `delta_dist_bottom` | `float32` | Amount of vertical shift of dist bottom estimate in latest reset [m] |
| `dist_bottom_reset_counter` | `uint8` | Index of latest dist bottom estimate reset |
| `dist_bottom_sensor_bitfield` | `uint8` | bitfield indicating what type of sensor is used to estimate dist_bottom |
| `eph` | `float32` | Standard deviation of horizontal position error, (metres) |
| `epv` | `float32` | Standard deviation of vertical position error, (metres) |
| `evh` | `float32` | Standard deviation of horizontal velocity error, (metres/sec) |
| `evv` | `float32` | Standard deviation of vertical velocity error, (metres/sec) |
| `dead_reckoning` | `bool` | True if this position is estimated through dead-reckoning |
| `vxy_max` | `float32` | maximum horizontal speed - set to 0 when limiting not required (meters/sec) |
| `vz_max` | `float32` | maximum vertical speed - set to 0 when limiting not required (meters/sec) |
| `hagl_min` | `float32` | minimum height above ground level - set to 0 when limiting not required (meters) |
| `hagl_max` | `float32` | maximum height above ground level - set to 0 when limiting not required (meters) |

常數:`MESSAGE_VERSION=0`、`DIST_BOTTOM_SENSOR_NONE=0`、`DIST_BOTTOM_SENSOR_RANGE=1`、`DIST_BOTTOM_SENSOR_FLOW=2`

## VehicleMagnetometer

內部訊息 · 主題名 `vehicle_magnetometer`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `device_id` | `uint32` | unique device ID for the selected magnetometer |
| `magnetometer_ga` | `float32[3]` | Magnetic field in the FRD body frame XYZ-axis in Gauss |
| `calibration_count` | `uint8` | Calibration changed counter. Monotonically increases whenever calibration changes. |

## VehicleOpticalFlow

內部訊息 · 主題名 `vehicle_optical_flow`

Optical flow in XYZ body frame in SI units.

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` |  |
| `device_id` | `uint32` | unique device ID for the sensor that does not change between power cycles |
| `pixel_flow` | `float32[2]` | (radians) accumulated optical flow in radians where a positive value is produced by a RH rotation about the body axis |
| `delta_angle` | `float32[3]` | (radians) accumulated gyro radians where a positive value is produced by a RH rotation of the sensor about the body axis. (NAN if unavailable) |
| `distance_m` | `float32` | (meters) Distance to the center of the flow field (NAN if unavailable) |
| `integration_timespan_us` | `uint32` | (microseconds) accumulation timespan in microseconds |
| `quality` | `uint8` | Average of quality of accumulated frames, 0: bad quality, 255: maximum quality |
| `max_flow_rate` | `float32` | (radians/s) Magnitude of maximum angular which the optical flow sensor can measure reliably |
| `min_ground_distance` | `float32` | (meters) Minimum distance from ground at which the optical flow sensor operates reliably |
| `max_ground_distance` | `float32` | (meters) Maximum distance from ground at which the optical flow sensor operates reliably |

## VehicleOpticalFlowVel

內部訊息 · 主題名 `estimator_optical_flow_vel`、`vehicle_optical_flow_vel`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `vel_body` | `float32[2]` | velocity obtained from gyro-compensated and distance-scaled optical flow raw measurements in body frame(m/s) |
| `vel_ne` | `float32[2]` | same as vel_body but in local frame (m/s) |
| `vel_body_filtered` | `float32[2]` | filtered velocity obtained from gyro-compensated and distance-scaled optical flow raw measurements in body frame(m/s) |
| `vel_ne_filtered` | `float32[2]` | filtered same as vel_body_filtered but in local frame (m/s) |
| `flow_rate_uncompensated` | `float32[2]` | integrated optical flow measurement (rad/s) |
| `flow_rate_compensated` | `float32[2]` | integrated optical flow measurement compensated for angular motion (rad/s) |
| `gyro_rate` | `float32[3]` | gyro measurement synchronized with flow measurements (rad/s) |
| `gyro_bias` | `float32[3]` |  |
| `ref_gyro` | `float32[3]` |  |

## VehicleRoi

內部訊息 · 主題名 `vehicle_roi`

Vehicle Region Of Interest (ROI)

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `mode` | `uint8` | ROI mode (see above) |
| `lat` | `float64` | Latitude to point to |
| `lon` | `float64` | Longitude to point to |
| `alt` | `float32` | Altitude to point to |
| `roll_offset` | `float32` | angle offset in rad |
| `pitch_offset` | `float32` | angle offset in rad |
| `yaw_offset` | `float32` | angle offset in rad |

常數:`ROI_NONE=0`、`ROI_WPNEXT=1`、`ROI_WPINDEX=2`、`ROI_LOCATION=3`、`ROI_TARGET=4`、`ROI_ENUM_END=5`

## VehicleStatusV0

內部訊息 · 主題名 `vehicle_status_v0`

Encodes the system state of the vehicle published by commander

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `armed_time` | `uint64` | Arming timestamp (microseconds) |
| `takeoff_time` | `uint64` | Takeoff timestamp (microseconds) |
| `arming_state` | `uint8` |  |
| `latest_arming_reason` | `uint8` |  |
| `latest_disarming_reason` | `uint8` |  |
| `nav_state_timestamp` | `uint64` | time when current nav_state activated |
| `nav_state_user_intention` | `uint8` | Mode that the user selected (might be different from nav_state in a failsafe situation) |
| `nav_state` | `uint8` | Currently active mode |
| `executor_in_charge` | `uint8` | Current mode executor in charge (0=Autopilot) |
| `valid_nav_states_mask` | `uint32` | Bitmask for all valid nav_state values |
| `can_set_nav_states_mask` | `uint32` | Bitmask for all modes that a user can select |
| `failure_detector_status` | `uint16` |  |
| `hil_state` | `uint8` |  |
| `vehicle_type` | `uint8` |  |
| `failsafe` | `bool` | true if system is in failsafe state (e.g.:RTL, Hover, Terminate, ...) |
| `failsafe_and_user_took_over` | `bool` | true if system is in failsafe state but the user took over control |
| `failsafe_defer_state` | `uint8` | one of FAILSAFE_DEFER_STATE_* |
| `gcs_connection_lost` | `bool` | datalink to GCS lost |
| `gcs_connection_lost_counter` | `uint8` | counts unique GCS connection lost events |
| `high_latency_data_link_lost` | `bool` | Set to true if the high latency data link (eg. RockBlock Iridium 9603 telemetry module) is lost |
| `is_vtol` | `bool` | True if the system is VTOL capable |
| `is_vtol_tailsitter` | `bool` | True if the system performs a 90° pitch down rotation during transition from MC to FW |
| `in_transition_mode` | `bool` | True if VTOL is doing a transition |
| `in_transition_to_fw` | `bool` | True if VTOL is doing a transition from MC to FW |
| `system_type` | `uint8` | system type, contains mavlink MAV_TYPE |
| `system_id` | `uint8` | system id, contains MAVLink's system ID field |
| `component_id` | `uint8` | subsystem / component id, contains MAVLink's component ID field |
| `safety_button_available` | `bool` | Set to true if a safety button is connected |
| `safety_off` | `bool` | Set to true if safety is off |
| `power_input_valid` | `bool` | set if input power is valid |
| `usb_connected` | `bool` | set to true (never cleared) once telemetry received from usb link |
| `open_drone_id_system_present` | `bool` |  |
| `open_drone_id_system_healthy` | `bool` |  |
| `parachute_system_present` | `bool` |  |
| `parachute_system_healthy` | `bool` |  |
| `avoidance_system_required` | `bool` | Set to true if avoidance system is enabled via COM_OBS_AVOID parameter |
| `avoidance_system_valid` | `bool` | Status of the obstacle avoidance system |
| `rc_calibration_in_progress` | `bool` |  |
| `calibration_enabled` | `bool` |  |
| `pre_flight_checks_pass` | `bool` | true if all checks necessary to arm pass |

常數:`MESSAGE_VERSION=0`、`ARMING_STATE_DISARMED=1`、`ARMING_STATE_ARMED=2`、`ARM_DISARM_REASON_TRANSITION_TO_STANDBY=0`、`ARM_DISARM_REASON_STICK_GESTURE=1`、`ARM_DISARM_REASON_RC_SWITCH=2`、`ARM_DISARM_REASON_COMMAND_INTERNAL=3`、`ARM_DISARM_REASON_COMMAND_EXTERNAL=4`、`ARM_DISARM_REASON_MISSION_START=5`、`ARM_DISARM_REASON_SAFETY_BUTTON=6`、`ARM_DISARM_REASON_AUTO_DISARM_LAND=7`、`ARM_DISARM_REASON_AUTO_DISARM_PREFLIGHT=8`、`ARM_DISARM_REASON_KILL_SWITCH=9`、`ARM_DISARM_REASON_LOCKDOWN=10`、`ARM_DISARM_REASON_FAILURE_DETECTOR=11`、`ARM_DISARM_REASON_SHUTDOWN=12`、`ARM_DISARM_REASON_UNIT_TEST=13`、`NAVIGATION_STATE_MANUAL=0`、`NAVIGATION_STATE_ALTCTL=1`、`NAVIGATION_STATE_POSCTL=2`、`NAVIGATION_STATE_AUTO_MISSION=3`、`NAVIGATION_STATE_AUTO_LOITER=4`、`NAVIGATION_STATE_AUTO_RTL=5`、`NAVIGATION_STATE_POSITION_SLOW=6`、`NAVIGATION_STATE_FREE5=7`、`NAVIGATION_STATE_FREE4=8`、`NAVIGATION_STATE_FREE3=9`、`NAVIGATION_STATE_ACRO=10`、`NAVIGATION_STATE_FREE2=11`、`NAVIGATION_STATE_DESCEND=12`、`NAVIGATION_STATE_TERMINATION=13`、`NAVIGATION_STATE_OFFBOARD=14`、`NAVIGATION_STATE_STAB=15`、`NAVIGATION_STATE_FREE1=16`、`NAVIGATION_STATE_AUTO_TAKEOFF=17`、`NAVIGATION_STATE_AUTO_LAND=18`、`NAVIGATION_STATE_AUTO_FOLLOW_TARGET=19`、`NAVIGATION_STATE_AUTO_PRECLAND=20`、`NAVIGATION_STATE_ORBIT=21`、`NAVIGATION_STATE_AUTO_VTOL_TAKEOFF=22`、`NAVIGATION_STATE_EXTERNAL1=23`、`NAVIGATION_STATE_EXTERNAL2=24`、`NAVIGATION_STATE_EXTERNAL3=25`、`NAVIGATION_STATE_EXTERNAL4=26`、`NAVIGATION_STATE_EXTERNAL5=27`、`NAVIGATION_STATE_EXTERNAL6=28`、`NAVIGATION_STATE_EXTERNAL7=29`、`NAVIGATION_STATE_EXTERNAL8=30`、`NAVIGATION_STATE_MAX=31`、`FAILURE_NONE=0`、`FAILURE_ROLL=1`、`FAILURE_PITCH=2`、`FAILURE_ALT=4`、`FAILURE_EXT=8`、`FAILURE_ARM_ESC=16`、`FAILURE_BATTERY=32`、`FAILURE_IMBALANCED_PROP=64`、`FAILURE_MOTOR=128`、`HIL_STATE_OFF=0`、`HIL_STATE_ON=1`、`VEHICLE_TYPE_UNKNOWN=0`、`VEHICLE_TYPE_ROTARY_WING=1`、`VEHICLE_TYPE_FIXED_WING=2`、`VEHICLE_TYPE_ROVER=3`、`VEHICLE_TYPE_AIRSHIP=4`、`FAILSAFE_DEFER_STATE_DISABLED=0`、`FAILSAFE_DEFER_STATE_ENABLED=1`、`FAILSAFE_DEFER_STATE_WOULD_FAILSAFE=2`

## VehicleThrustSetpoint

內部訊息 · 主題名 `vehicle_thrust_setpoint`、`vehicle_thrust_setpoint_virtual_fw`、`vehicle_thrust_setpoint_virtual_mc`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | timestamp of the data sample on which this message is based (microseconds) |
| `xyz` | `float32[3]` | thrust setpoint along X, Y, Z body axis [-1, 1] |

## VehicleTorqueSetpoint

內部訊息 · 主題名 `vehicle_torque_setpoint`、`vehicle_torque_setpoint_virtual_fw`、`vehicle_torque_setpoint_virtual_mc`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | timestamp of the data sample on which this message is based (microseconds) |
| `xyz` | `float32[3]` | torque setpoint about X, Y, Z body axis (normalized) |

## VelocityLimits

內部訊息 · 主題名 `velocity_limits`

Velocity and yaw rate limits for a multicopter position slow mode only

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `horizontal_velocity` | `float32` | [m/s] |
| `vertical_velocity` | `float32` | [m/s] |
| `yaw_rate` | `float32` | [rad/s] |

## WheelEncoders

內部訊息 · 主題名 `wheel_encoders`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `wheel_speed` | `float32[2]` | [rad/s] |
| `wheel_angle` | `float32[2]` | [rad] |

## YawEstimatorStatus

內部訊息 · 主題名 `yaw_estimator_status`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `timestamp` | `uint64` | time since system start (microseconds) |
| `timestamp_sample` | `uint64` | the timestamp of the raw data (microseconds) |
| `yaw_composite` | `float32` | composite yaw from GSF (rad) |
| `yaw_variance` | `float32` | composite yaw variance from GSF (rad^2) |
| `yaw_composite_valid` | `bool` |  |
| `yaw` | `float32[5]` | yaw estimate for each model in the filter bank (rad) |
| `innov_vn` | `float32[5]` | North velocity innovation for each model in the filter bank (m/s) |
| `innov_ve` | `float32[5]` | East velocity innovation for each model in the filter bank (m/s) |
| `weight` | `float32[5]` | weighting for each model in the filter bank |

---

→ 回 [附錄索引](README.md)
