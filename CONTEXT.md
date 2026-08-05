# CONTEXT — 術語、版本現況與表述決策

這份文件是 repo 的共同語言。文件之間對同一件事的稱呼以這裡為準;版本號與專案狀態也只在這裡維護一份,其他文件引用它。

---

## 1. 版本現況(查證日期:2026-08-05)

寫文件時引用這張表,不要在內文另寫一套版本號。版本會過期,更新時連查證日期一起改。

### 飛控韌體

| 專案 | 狀態 | 備註 |
|---|---|---|
| PX4 | v1.17 stable、v1.18 beta、main 朝 v1.19 | v1.16 起模擬器改用 Gazebo Harmonic、內建 Zenoh middleware、支援 log 加密;v1.17 新增 Altitude Cruise 模式、Zenoh 向 `rmw_zenoh` 相容性成熟 |
| ArduPilot | 4.7.0 stable(2026-07-21) | Copter / Plane / Rover / Sub / Tracker / Periph 同版號釋出 |

### 中介層與 SDK

| 專案 | 狀態 | 備註 |
|---|---|---|
| uXRCE-DDS | PX4 預設,多數 build 內建 | Client 在 PX4、Agent 在伴隨電腦,兩端橋接 uORB ↔ DDS |
| PX4 Zenoh middleware | v1.16 進 in-tree,v1.17 成熟 | CDRv1 序列化對齊 ROS 2、transport lease 60 秒、liveliness 為實驗性;需手動啟用 |
| `rmw_zenoh` | ROS 2 Tier 1(自 Kilted 起) | Zenoh 作為 ROS 2 middleware 的官方實作 |
| MAVSDK (C++) | v3.17.1(2026-04) | C++20;內含 gRPC server,其他語言當 client |
| MAVSDK-Python | 3.15.3(2026-02) | 走 gRPC 連 C++ server |
| px4-ros2-interface-lib | Auterion 維護,活躍 | C++ 函式庫,把 ROS 2 寫的 flight mode 動態註冊進 PX4,GCS 看起來像原生模式,失敗可 fallback 回原模式;版本相容性檢查在註冊時做 |
| pymavlink | MAVLink 官方 Python 綁定 | 低階、無依賴,適合學協定與寫工具 |

### ROS 2

| 版本 | 釋出 | 支援到 | 備註 |
|---|---|---|---|
| Lyrical Luth | 2026-05 | 2031-05 | 最新 LTS |
| Kilted Kaiju | 2025-05 | 2026-11 | 首個把 `rmw_zenoh` 列 Tier 1 的版本 |
| Jazzy Jalisco | 2024-05 | 2029-05 | LTS |
| Humble Hawksbill | 2022-05 | 2027-05 | LTS,現存教材與第三方套件最多 |

### 模擬器

| 專案 | 狀態 | 備註 |
|---|---|---|
| Gazebo Harmonic | LTS,支援到 2028-09 | PX4 官方對齊的版本 |
| Gazebo Ionic | 短期支援,EOL 2026-12 | Harmonic 到 Jetty 之間的過渡版 |
| Gazebo Jetty | LTS(2025-09 起,約 5 年) | 最新 LTS |
| Isaac Sim | 6.0 GA(6.0.1 為最新修訂) | 前一版為 5.1 |
| Pegasus Simulator | v5.1.0 對應 Isaac Sim 5.1 | 支援 PX4,ArduPilot 為實驗性。**是否支援 Isaac Sim 6.0:待查證** |

### Physical AI 訓練堆疊

| 專案 | 狀態 | 備註 |
|---|---|---|
| Newton | 1.0(2026-03 GTC 發布),Apache-2.0 | NVIDIA + Google DeepMind + Disney Research,Linux Foundation 管理;建在 Warp + OpenUSD,MuJoCo Warp 為主要 backend |
| Isaac Lab | 2.3.2(2026-01-30)加入無人機支援;3.0 Beta 整合 Newton(develop 分支) | BSD-3-Clause |
| Aerial Gym Simulator | 活躍,BSD-3-Clause | 仍建在 Isaac Gym Preview;Isaac Lab / Isaac Sim 支援標示為開發中 |
| AirGym | 活躍,BSD-3-Clause | 同樣建在 Isaac Gym |
| gym-pybullet-drones | 活躍,MIT | CPU 可跑 |
| aerial-autonomy-stack | 活躍,MIT | Gazebo + PX4/ArduPilot 多機 + ROS 2 Humble + Jetson 部署 |
| Cosmos Predict | 2.5,Apache-2.0,2B / 14B 兩種規模 | 影片類世界基礎模型需每卡 80 GB VRAM 起 |
| PX4 `mc_nn_control` | 存在於 main 分支 | 位置 setpoint 到控制分配的神經網路控制模組,含啟用開關與輸出限幅參數 |

### 地面站

| 專案 | 狀態 |
|---|---|
| QGroundControl | v5.0 stable,v5.1 release candidate |
| Mission Planner | ArduPilot 生態主力,Windows 為主 |

---

## 2. 術語表

### 系統角色

| 術語 | 全名 | 一句話解釋 | 軟體工程師的類比 |
|---|---|---|---|
| UAS | Unmanned Aerial System | 載具 + 地面站 + 通訊鏈路的整個系統 | 整套服務,不只那台機器 |
| UAV | Unmanned Aerial Vehicle | 只指空中載具本身 | 單一節點 |
| FC | Flight Controller | 跑即時控制迴圈的飛控板與韌體 | 硬即時的嵌入式服務,不可被阻塞 |
| Companion Computer | — | 掛在機上的 Linux 電腦,跑視覺、決策、串流 | 邊緣運算節點 |
| GCS | Ground Control Station | 地面操作端,顯示遙測、下命令、規劃任務 | 操作者用的前端 + 本地服務 |
| Payload | — | 相機、紅外、測距等任務酬載 | 業務價值的來源;飛行只是載具 |
| Gimbal | — | 讓相機視角與機體運動解耦的指向機構 | 一個有自己座標系的獨立 component |

### 三層任務控制(本 repo 的命名約定)

「Mission Controller」在業界指涉三種不同的東西,混用會造成責任邊界討論失焦。本 repo 固定用以下稱呼:

| 稱呼 | 跑在哪 | 負責什麼 | 不負責什麼 |
|---|---|---|---|
| **Navigator(FC 內建任務執行)** | 飛控韌體內 | 執行已上傳的航點序列、geofence 判斷、failsafe 介入 | 不懂業務語意,不知道「巡檢第 3 根電線桿」是什麼 |
| **機載任務執行器(on-board mission executor)** | Companion computer | 把業務任務拆成動作序列、驅動 Offboard、處理中斷與恢復、協調感測與 payload | 不做即時姿態控制,不能取代 failsafe |
| **雲端任務服務(mission service)** | 地面或雲端 | 任務資料模型、排程派工、多機協調、生命週期 API、稽核 | 不進即時迴路,不能假設鏈路永遠在 |

### 協定與中介層

| 術語 | 一句話解釋 |
|---|---|
| MAVLink | 為窄頻寬、會掉包的鏈路設計的二進位訊息協定;v2 支援簽章與欄位擴充 |
| sysid / compid | MAVLink 的定址:一台機一個 system id,機上每個元件(飛控、雲台、相機、伴隨電腦)各一個 component id |
| uORB | PX4 韌體內部的發佈訂閱匯流排 |
| DDS | ROS 2 底層的資料分發標準 |
| uXRCE-DDS | 把 uORB 橋到 DDS 的 client/agent 機制 |
| Zenoh | 另一種 pub/sub 與查詢協定,對高延遲、跨網段鏈路較友善;PX4 與 ROS 2 都有實作 |
| Offboard | FC 接受外部高階指令的模式;必須先持續送 setpoint 才能切入 |
| Remote ID | 無人機對外廣播身分與位置的法規要求;有廣播式與網路式兩種 |
| UTM / U-space | 無人機交通管理,處理空域申請、衝突偵測與資訊共享 |

### 機體與飛行包絡

| 術語 | 一句話解釋 |
|---|---|
| MTOW | Maximum Take-Off Weight,最大起飛重量,含機體、電池與酬載 |
| 飛行包絡 | 機體在物理上做得到的操作範圍(速度、高度、傾角、爬升率、抗風)|
| 空速 / 地速 | 相對空氣的速度 / 相對地面的速度;兩者差一個風速,規劃時間要用地速 |
| 巡航速度 | 能量效率最好的持續飛行速度,不是最大速度 |
| 抗風上限 | 機體還控制得住的風速,不等於「這個風速下任務做得完」|
| 最小轉彎半徑 | 固定翼受側傾角限制的轉彎半徑,`R = v²/(g·tanφ)` |
| 槳盤面積 | 螺旋槳掃過的總面積;懸停功率與它的平方根成反比 |
| 渦環狀態 | 多旋翼垂直下降過快時掉進自身下洗氣流、升力驟降的現象 |
| 續航 vs 航程 | 能飛多久 vs 能飛多遠;兩者靠巡航速度換算,但換算會失真 |
| DoD Group 1~5 | 美國國防部按最大起飛重量、慣用高度、速度切的無人機分級;Group 4 與 5 的差別在高度 |
| LOS / BLOS | 視距 / 超視距。BLOS 通常靠衛星鏈路,往返延遲數百毫秒 |
| MALE / HALE | 中空長航時 / 高空長航時,對應 MQ-9 與 RQ-4 這兩類平台 |
| 徘徊彈 | 單程任務的載具,任務狀態機沒有返航分支 |
| 飛行終止系統 | 與主飛控完全分離的獨立通道,最壞情況下強制終止飛行 |

### 座標與估測

| 術語 | 一句話解釋 |
|---|---|
| NED / ENU | 在地座標系。PX4 內部用 NED(z 向下為正),ROS 2 慣例用 ENU(z 向上為正),跨界必轉 |
| Body frame | 機體座標系,原點在重心,隨機體轉動 |
| EKF | 擴展卡爾曼濾波器,把多個不完美的感測器融合成一組狀態估計 |
| Innovation | 量測值與預測值的差;EKF 健康度的第一觀察指標 |
| Setpoint | 控制器要追的目標值 |
| Mixer / Control Allocation | 把力與力矩需求分配成各馬達與舵面輸出 |

### 模擬與測試

| 術語 | 一句話解釋 |
|---|---|
| SITL | Software In The Loop,飛控韌體跑在電腦上,感測器與致動器由模擬器提供 |
| HITL | Hardware In The Loop,真實飛控板接模擬器,驗證韌體在真硬體上的行為 |
| ULog | PX4 的飛行紀錄格式,事後分析用 |
| Flight Review | 上傳 ULog 產生分析報告的開源服務 |
| sim-to-real gap | 模擬與真機的行為落差;策略可能學會利用模擬器的缺陷 |
| Domain randomization | 訓練時隨機化模型參數與環境條件,逼策略不依賴單一設定 |
| 世界基礎模型 | 生成擬真環境影片的大模型,用來產生訓練資料 |
| 分布外輸入(OOD) | 落在訓練時沒見過範圍的觀測;神經網路在此的輸出可能完全無意義 |

### 模擬素材格式

| 術語 | 一句話解釋 |
|---|---|
| OpenUSD | Isaac Sim 的原生場景格式,所有其他格式最後都要轉進來 |
| URDF | ROS 生態的機器人描述格式,**帶得動質量、慣量、關節與碰撞體** |
| SDF | Gazebo 的場景與模型格式,表達力比 URDF 強(可描述世界、感測器、外掛) |
| MJCF | MuJoCo 的模型格式,同樣帶物理資訊 |
| SimReady 資產 | NVIDIA 的說法:除了外觀,還附帶物理屬性與語意標註的 3D 資產 |
| 3D Tiles | 串流大範圍地理場景的開放格式;Cesium for Omniverse 用它把真實地形送進 Isaac Sim |
| 碰撞體 | 給物理引擎算接觸用的簡化形狀;**與視覺網格分開**,直接拿高面數網格當碰撞體會拖垮效能 |

---

## 3. 表述決策

寫作時反覆出現、已經定案的用詞與立場:

- **「飛控」指 FC 這個角色(硬體 + 韌體)**,不特指某塊板子。講到具體硬體寫 Pixhawk / FMUv6X。
- **Delta、Mirle 這類名稱在別的專案是 API 版本,本 repo 不出現**,避免與外部專案術語衝突。
- **不寫「無人機大腦」這類比喻**。飛控是硬即時控制器,伴隨電腦是邊緣運算節點,兩者職責不同,用比喻會讓邊界討論失焦。
- **模擬器不是「玩具版」**。SITL 跑的是真的飛控韌體,只有感測器與致動器被換掉;寫作時要維持這個區分,否則讀者會低估模擬的驗證價值。
- **講「不能放在飛控上」時要給理由**,通常是三者之一:會阻塞即時迴圈、記憶體不夠、失效後沒有安全退路。
