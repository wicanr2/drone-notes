# 開源生態地圖:現在有什麼可以直接用

這個領域的開源成熟度比多數人想像的高。從飛控韌體、通訊協定、地面站、模擬器到空域管理,每一層都有活躍的專案,而且不少是產業界真的拿去出貨的東西。所以進場的難處不在「找不到輪子」,而在兩件事:**授權踩雷**,以及**把停更的專案當成現役的用**。

下面這張表是 2026-08-05 用 GitHub API 直接查的授權與最後推送時間,不是憑印象寫的。表後面按層說明各自的取捨。

---

## 1. 總表

| 層 | 專案 | 授權 | 最後推送 | Stars | 一句話 |
|---|---|---|---|---|---|
| 飛控韌體 | [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot) | BSD-3-Clause | 2026-08-05 | 12.3k | 模組化、ROS 2 整合最深,商用可閉源 |
| 飛控韌體 | [ArduPilot](https://github.com/ArduPilot/ardupilot) | GPL-3.0 | 2026-08-05 | 15.6k | 機型與周邊支援最廣,韌體衍生作品須開源 |
| 協定庫 | [pymavlink](https://github.com/ArduPilot/pymavlink) | (L)GPLv3 + 產生碼例外 | 2026-08-03 | 717 | 學協定與寫工具的首選 |
| 協定庫 | [MAVSDK](https://github.com/mavlink/MAVSDK) | BSD-3-Clause | 2026-08-04 | 917 | C++20 核心 + gRPC,多語言 client |
| 協定庫 | [rust-mavlink](https://github.com/mavlink/rust-mavlink) | Apache-2.0 | 2026-08-03 | 284 | Rust 官方綁定,async 與 blocking 都有 |
| 協定庫 | [gomavlib](https://github.com/bluenviron/gomavlib) | MIT | 2026-08-04 | 194 | Go 的完整 MAVLink 實作,含簽章與擴充欄位 |
| 路由 | [mavlink-router](https://github.com/mavlink-router/mavlink-router) | Apache-2.0 | 2026-07-13 | 604 | C 寫的經典路由器,機上常駐 |
| 路由 | [mavp2p](https://github.com/bluenviron/mavp2p) | MIT | 2026-08-04 | 235 | 單一執行檔,設定簡單,基於 gomavlib |
| ROS 2 | [px4_msgs](https://github.com/PX4/px4_msgs) | BSD-3-Clause | 2026-07-30 | 155 | PX4 uORB 訊息的 ROS 2 定義 |
| ROS 2 | [px4-ros2-interface-lib](https://github.com/Auterion/px4-ros2-interface-lib) | BSD-3-Clause | 2026-08-03 | 181 | 用 ROS 2 寫飛行模式並註冊回 PX4 |
| ROS 2 | [MAVROS](https://github.com/mavlink/mavros) | BSD / GPLv3 / LGPLv3 三授權 | 2026-08-04 | 1.2k | MAVLink ↔ ROS 橋接,ArduPilot 生態主力 |
| ROS 2 | [Aerostack2](https://github.com/aerostack2/aerostack2) | BSD-3-Clause | 2026-07-30 | 367 | 平台無關的多機空中自主框架 |
| ROS 2 | [AirStack](https://github.com/castacks/AirStack) | MIT | 2026-08-05 | 84 | CMU AirLab 的模組化自主堆疊,重視 sim→real |
| 中介層 | [Zenoh](https://github.com/eclipse-zenoh/zenoh) | Apache-2.0 OR EPL-2.0 | 2026-08-05 | 3.0k | pub/sub + 查詢,對高延遲與跨網段友善 |
| 中介層 | [rmw_zenoh](https://github.com/ros2/rmw_zenoh) | Apache-2.0 | 2026-08-04 | 493 | ROS 2 的 Zenoh middleware,Kilted 起 Tier 1 |
| 地面站 | [QGroundControl](https://github.com/mavlink/qgroundcontrol) | Apache-2.0 | 2026-08-03 | 4.8k | 跨平台桌面 / 行動 GCS,PX4 官方推薦 |
| 地面站 | [ADOS Mission Control](https://github.com/altnautica/ADOSMissionControl) | GPL-3.0 | 2026-08-04 | 222 | Web 版 GCS,含多機與 MQTT 遙測轉發 |
| 模擬 | [Gazebo (gz-sim)](https://github.com/gazebosim/gz-sim) | Apache-2.0 | 2026-08-04 | 1.4k | PX4 官方對齊的模擬器 |
| 模擬 | [Isaac Sim](https://github.com/isaac-sim/IsaacSim) | Apache-2.0(**依賴另有 NVIDIA 授權**) | 2026-07-02 | 3.8k | 光線追蹤等級的感測器模擬與 RL 環境 |
| 模擬 | [Pegasus Simulator](https://github.com/PegasusSimulator/PegasusSimulator) | BSD-3-Clause | 2026-07-24 | 858 | 在 Isaac Sim 上跑 PX4 多旋翼的框架 |
| 合規 | [opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) | Apache-2.0 | 2026-08-01 | 356 | 廣播式 Remote ID 的編碼實作 |
| 合規 | [InterUSS DSS](https://github.com/interuss/dss) | Apache-2.0 | 2026-08-04 | 157 | UTM 的探索與同步服務,Linux Foundation 專案 |
| 後處理 | [Flight Review](https://github.com/PX4/flight_review) | BSD-3-Clause | 2026-06-24 | 267 | 上傳 ULog 產生分析報告 |
| 後處理 | [OpenDroneMap](https://github.com/OpenDroneMap/ODM) | AGPL-3.0 | 2026-08-04 | 6.4k | 空拍影像轉正射影像與點雲 |

查證方式:`gh api repos/<owner>/<repo>` 取 `license.spdx_id`、`pushed_at`、`archived`。授權欄位顯示為非標準的專案(pymavlink、MAVROS、Zenoh、Isaac Sim、ADOS)另外讀了 repo 內的授權檔確認。上表所有專案的 `archived` 都是 false。

---

## 2. 授權:這一層踩雷最貴

無人機專案的授權問題比一般後端專案嚴重,因為你要交付的是**含韌體的實體產品**,而不是自己機房裡跑的服務。幾個必須先搞清楚的點:

### PX4 的 BSD-3 與 ArduPilot 的 GPLv3

這是產業界最常見的選型分水嶺。ArduPilot 是 GPLv3:**你改了韌體、把它裝進要賣的機器裡,就構成分發,必須提供對應的原始碼**,包含你的修改。PX4 是 BSD-3,改完可以閉源出貨。

但這條線常被過度解讀,要講清楚它**不管什麼**:GPL 約束的是韌體本身的衍生作品。你的地面站、雲端服務、機載 Python 程式透過 MAVLink 跟 ArduPilot 通訊,那是行程間的協定往來,不會讓你的程式變成 ArduPilot 的衍生作品。所以「用 ArduPilot 就得把整套系統開源」是錯的,「改了 ArduPilot 韌體出貨卻不給原始碼」才是違規。

實務上的建議:如果你完全不打算改韌體,兩者的授權差異對你影響不大,選型應該看別的條件。如果你確定要動韌體核心並且要閉源,那 PX4 是唯一選項。

### pymavlink 的例外條款

pymavlink 的產生器本身是 (L)GPLv3,但授權檔裡有一條明確的例外:**產生出來的訊息程式碼可以嵌進你自己的專案,不因此觸發 GPL 的傳染性。** 這是刻意設計的,否則整個 MAVLink 生態都沒辦法商用。很多人看到 GPL 就直接排除 pymavlink,那是誤讀。

### Isaac Sim 的兩層授權

Isaac Sim 的 repo 本身是 Apache-2.0,但授權檔第一段就寫明:**建置或使用它需要另外的元件,包含 Omniverse Kit SDK 與 3D 模型貼圖,那些是 NVIDIA 自有授權。** 所以「Isaac Sim 是開源的」這句話只對了一半。實務上這代表:你可以自由讀改 Isaac Sim 的程式碼,但不能把整包重新散布成一個不受 NVIDIA 條款約束的產品,而且執行環境綁 NVIDIA GPU。

### AGPL 的網路服務條款

OpenDroneMap 是 AGPL-3.0。AGPL 比 GPL 更進一步:**把它包成網路服務讓別人用,也算分發**,必須提供原始碼。如果你打算做一個「上傳空拍照片、線上出正射影像」的 SaaS,直接把 ODM 包進去會觸發這一條。ODM 官方有商用授權管道,走那條路。

### MAVROS 的三授權

MAVROS 同時以 BSD、GPLv3、LGPLv3 三種授權提供,使用者可以挑一種來遵守。這在開源專案裡少見,對商用是好消息。

---

## 3. 按層評述

### 飛控韌體

除了授權,PX4 與 ArduPilot 的實質差異在**設計哲學**。PX4 的模組邊界切得比較乾淨(每個模組是獨立的任務,透過 uORB 通訊),對想改核心的人友善,ROS 2 整合是官方主線。ArduPilot 的機型與周邊支援廣度是無可取代的——潛水艇、天線追蹤器、各種奇怪的載具都有現成支援,而且參數調校的社群知識累積最厚。

Betaflight 與 INAV 是另一個世界:為競速與航模設計,不做自動任務、沒有伴隨電腦整合的概念。如果你的需求含「自動飛一條航線」,它們不在候選名單裡。

### 協定與語言綁定

值得注意的是**後端工程師慣用語言在這裡都有第一方或高品質的實作**:Go 有 gomavlib、Rust 有官方的 rust-mavlink、Python 有 pymavlink、C++ 有 MAVSDK。這代表你不需要為了接無人機而換語言。

選擇的邏輯:
- 要**理解協定**、寫一次性工具、做逆向分析 → pymavlink,它幾乎不做抽象,你看到的就是協定本身。
- 要寫**產品級的地面應用**,不想處理 MAVLink 的狀態機細節 → MAVSDK。它把「起飛」「上傳任務」「等待到達」包成 async 呼叫,並且用 gRPC 讓其他語言接得上。
- 要寫**高吞吐的服務端**(同時接幾十台機、要做路由與轉發)→ gomavlib / rust-mavlink,型別安全、無 GIL、部署成單一執行檔。

MAVLink 路由器(mavlink-router 或 mavp2p)幾乎是機上必備:飛控只有一個序列埠,但要同時餵給地面遙測、伴隨電腦、記錄器。路由器把一路分成多路,順便做協定版本轉換與過濾。mavp2p 因為是單一 Go 執行檔、設定簡單,近年常被拿來取代 mavlink-router。

### ROS 2 整合

這一層最近幾年變化最大,選錯會做白工:

- **px4_msgs + uXRCE-DDS** 是 PX4 的原生路線,直接把 uORB 主題暴露成 ROS 2 主題,延遲最低、資訊最完整。
- **px4-ros2-interface-lib** 是更上層的東西,而且是這幾年最值得注意的變化:**你可以用 ROS 2 寫一個飛行模式,把它動態註冊進 PX4**,地面站看到的是一個像原生模式的選項,而且模式失效時 PX4 會自動 fallback 回內建模式。這改變了「客製飛行行為必須改韌體」的老規則——現在可以在伴隨電腦上用 C++ 寫,不必動韌體、不必重新驗證整份韌體。代價是它對 PX4 與 px4_msgs 的版本一致性要求嚴格,註冊時會做相容性檢查。
- **MAVROS** 是 MAVLink 到 ROS 的橋,對 ArduPilot 使用者仍是主力。在 PX4 上它是舊路線,新專案沒有理由選它,除非你需要同時支援兩種韌體。

框架層有 Aerostack2 與 AirStack。它們解決的是「每個實驗室都在重寫同一套任務行為、狀態機、平台抽象」的問題。Aerostack2 的賣點是平台無關(PX4、DJI、Crazyflie 都能接)加上 behavior 為單位的任務組合;AirStack 偏向研究到部署的流程完整性。兩者都不是「拿來就能出貨的產品」,而是省掉你重造基礎設施的起點。

### 地面站

QGroundControl 是預設答案:跨平台、支援 PX4 與 ArduPilot、參數校正與韌體燒錄都完整,Apache-2.0 讓你可以改了拿去用。它的問題是 Qt/QML 的架構對只寫過 web 的團隊來說學習成本不低,而且它是**單機工具**,不是多機隊管理平台。

ADOS Mission Control 代表另一條路線:web 版 GCS,含多機與 MQTT 遙測轉發。GPL-3.0,222 stars 屬於小專案,拿來當產品基礎要自己評估維護風險,但拿來當「web GCS 該怎麼設計」的參考實作很有價值。

商用的 Auterion Mission Control 不是開源的,雖然 Auterion 的底層是 PX4。這是這個生態常見的模式:核心開源、產品層閉源。

### 模擬

Gazebo 與 Isaac Sim 不是競爭關係,是不同工具。[60 模擬與測試](../60-simulation-and-testing/)會展開,這裡先給結論:**要跑 CI、要驗證控制與任務邏輯,用 Gazebo;要驗證視覺演算法、要生訓練資料、要光學保真度,用 Isaac Sim。** Pegasus Simulator 是把 PX4 接到 Isaac Sim 的橋,目前對應 Isaac Sim 5.1,**在已經 GA 的 Isaac Sim 6.0 上載入失敗**([issue #131](https://github.com/PegasusSimulator/PegasusSimulator/issues/131),查證日 2026-08-05 未關閉)。

已經退場的要知道:jMAVSim 已被 PX4 淘汰,微軟的 AirSim 已封存(社群 fork Cosys-AirSim 仍在動)。看到教學文章用這兩個,先確認發文日期。

### 合規

Remote ID 與 UTM 這塊,開源的成熟度出乎意料地高。廣播式 Remote ID 有 opendroneid-core-c 可以直接用,網路式 Remote ID 與空域協調有 InterUSS 的 DSS——那是 Linux Foundation 底下的專案,而且真的有服務商在跑。

對軟體團隊來說重點是:**這些是標準的實作,不是某家公司的產品**。你要做的是接上去,不是重新發明。

### 資料後處理

Flight Review 是 PX4 官方的 ULog 分析服務,可以自架。它的價值不只是畫圖:它內建了一批**異常判讀規則**(震動過大、推力不足、EKF 異常),等於把資深工程師的除錯經驗編碼成自動檢查。做飛行後自動品管的話,這是最省力的起點。

---

## 4. 判斷一個無人機開源專案能不能用

除了看 star 數,這幾項更能預測你半年後會不會後悔:

- **最後推送時間**。無人機專案跟著 PX4 / ROS 2 的版本走,超過一年沒動的,大概率跟現行版本接不上。
- **它綁定哪個上游版本**。README 寫「支援 PX4 v1.13」的專案,在 v1.17 上多半要改。ROS 2 的 distro 也同理。
- **授權檔要自己開來看**,不要只信 GitHub 側欄的標示。上表裡有五個專案的標示是「非標準」,實際內容差很多。
- **有沒有 CI**。無人機專案的整合面很寬,沒有自動化測試的專案,合併新韌體版本時通常就爛掉了。
- **是誰在維護**。基金會專案(Dronecode、Linux Foundation、Open Robotics)與公司主導的專案,風險型態不一樣;學術專案要看主要作者畢業了沒——Pegasus Simulator 的作者就明確寫過維護預期跟他的博士班時程綁在一起。

→ 下一篇把這些選項收斂成幾條決策線:[02 選型決策](02-selection.md)
