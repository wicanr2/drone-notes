# 素材:模型與世界從哪裡來

要建 Physical AI 模擬環境,第一個實際問題是「機體模型跟場景哪裡找」。這一章給清單,但要先講一件會省下很多時間的事:

**你要的不是 CAD。**

CAD 檔(STEP、IGES、SolidWorks)裡面只有幾何。物理模擬需要的是另外一組東西——質量、慣量張量、關節、致動器模型、碰撞形狀——而那些**不在 CAD 裡**。把一個漂亮的 CAD 匯進 Isaac Sim,你會得到一個外觀完美、像磚頭一樣掉下去的物件。

對無人機更是如此。決定飛行行為的是[第 15 章那組參數](../15-airframes-and-envelope/01-platform-parameters.md):推力係數、馬達時間常數、轉動慣量、槳盤面積。外觀網格只影響渲染與碰撞,對動力學幾乎沒有貢獻。**先找對的動力學模型,視覺網格之後再換。**

所以下面的清單按「含不含動力學」分類,而不是按好不好看。

---

## 1. Isaac Sim 吃什麼格式

原生格式是 OpenUSD,所有東西最後都要轉成 USD。官方提供的匯入路徑:

| 匯入器 | 吃什麼 | 帶得進物理嗎 |
|---|---|---|
| URDF Importer | URDF | **可以**:連桿、關節、慣量、碰撞體 |
| MJCF Importer | MuJoCo XML | **可以** |
| CAD Converter | Catia、SolidWorks、AutoCAD、Creo 等 | 只有視覺網格 |
| Onshape Importer | Onshape 文件 | 視覺為主 |
| Mesh Importer | OBJ、FBX、STL、glTF | 只有網格 |

URDF 與 MJCF 匯入器的原始碼 NVIDIA 已經開源,可以當成寫其他格式匯入器的範例。

判斷很簡單:**走 URDF 或 MJCF 進來的,物理資訊帶得進來;走 CAD 或 mesh 進來的,物理要自己補。**

---

## 2. 現成的無人機模型

授權與活躍度以 `gh api` 於 2026-08-05 查證。

| 來源 | 格式 | 授權 | 含動力學 | 備註 |
|---|---|---|---|---|
| Isaac Sim 內建資產 | USD | NVIDIA 資產條款 | ✅ | `Robots/Crazyflie/cf2x.usd` 與 `Robots/Quadcopter/quadcopter.usd`;Isaac Lab 有對應的懸停訓練範例 |
| [Pegasus Simulator](https://github.com/PegasusSimulator/PegasusSimulator) | USD | BSD-3-Clause | ✅ | 多旋翼 + PX4 介接,**但只到 Isaac Sim 5.1**,見下方版本說明 |
| [Aerial Gym Simulator](https://github.com/ntnu-arl/aerial_gym_simulator) | 自有格式 | BSD-3-Clause | ✅ | 含幾何控制器與 GPU 光達/相機;目前建在 Isaac Gym 上 |
| [gym-pybullet-drones](https://github.com/utiasDSL/gym-pybullet-drones) | **URDF** | MIT | ✅ | URDF 裡直接寫了慣量與推力係數,是**最好抄的參數來源** |
| [PX4-gazebo-models](https://github.com/PX4/PX4-gazebo-models) | SDF | BSD-3-Clause | ✅ | PX4 官方模擬機型(x500 等),Gazebo 格式,要轉 |
| [RotorS](https://github.com/ethz-asl/rotors_simulator) | URDF / xacro | **無授權檔** | ✅ | Hummingbird / Pelican / Firefly;2024-07 之後沒動、ROS 1,見下方風險 |

### 先確認 Isaac Sim 版本,再決定用哪條路

Pegasus 是 Isaac Sim 上接 PX4 最直接的橋,但**它目前跟不上 Isaac Sim 的版本**。最新的 v5.1.0(2025-10-26)對應 Isaac Sim 5.1;Isaac Sim 6.0 已於 2026-06-04 GA,而 Pegasus 在 6.0 上會載入失敗——擴充相依於 6.0 已經移除的 `omni.isaac.core`([issue #131](https://github.com/PegasusSimulator/PegasusSimulator/issues/131),2026-03-13 開啟,查證日 2026-08-05 仍未關閉)。

這不是死專案,repo 最後 push 是 2026-07-24。但在支援補上之前,選擇只有兩個:**裝 Isaac Sim 5.1 用 Pegasus,或裝 6.0 但自己接 PX4。** 先想清楚要哪一個,再開始裝——裝錯版本重來的成本比查一次高得多。

Pegasus 的維護節奏本來就慢一拍。作者明確寫過維護預期跟他的博士班時程綁在一起,[開源生態那章](../05-open-source-landscape/01-landscape.md)提過這一點。歷史上每個版本都明示「與舊版 Isaac Sim 不相容」,所以版本綁定是常態,不是這一次的意外。

### 最實際的做法

如果目標是「在 Isaac Sim 裡飛一台接 PX4 的多旋翼」,順序是:

1. **先定版本**:要用 Pegasus 就裝 Isaac Sim 5.1。
2. **用 Pegasus 附的模型起步**。它已經處理好 USD、動力學與 PX4 介接,不必自己組。
3. **需要不同機型時,從 gym-pybullet-drones 的 URDF 抄參數。** 它的 URDF 把質量、慣量、推力係數、力矩係數都寫成明碼,是很好的對照組——即使你最後不用 PyBullet。
4. **視覺要好看再換網格。** 這一步放最後,因為它對訓練結果的影響最小(除非你在訓視覺)。

如果非用 Isaac Sim 6.0 不可(例如要用它的 Newton 整合),就要有自己接 PX4 的心理準備,或改用 [Gazebo 走驗證路線](../60-simulation-and-testing/02-gazebo-and-isaac-sim.md)——PX4 官方主線支援的是 Gazebo,不是 Isaac Sim。

---

## 3. 世界模型

| 來源 | 內容 | 授權 | 適合 |
|---|---|---|---|
| Isaac Sim 內建環境 | 倉庫、辦公室等 SimReady 場景 | NVIDIA 資產條款 | 室內任務、倉儲巡檢 |
| [Cesium for Omniverse](https://github.com/CesiumGS/cesium-omniverse) | 真實世界地形與城市 | 擴充本身 Apache-2.0;**內容另有服務條款** | 戶外長距離飛行、地理座標對齊 |
| Gazebo Fuel | 大量社群模型與世界 | **逐一不同**,多為 CC-BY | Gazebo 流程;要轉才能進 Isaac Sim |
| [3DGEMS](https://data.nvision2.eecs.yorku.ca/3DGEMS/) | 270+ 個 Gazebo 模型 | 見該站說明 | 補室內物件 |
| AWS RoboMaker worlds | 醫院、住宅、書店等場景 | **無授權檔,且已封存** | 見下方風險 |

### Cesium 值得單獨說

對無人機來說,Cesium for Omniverse 是少數能把**真實世界的地形與城市**串進 Isaac Sim 的路徑:3D Tiles 串流、Cesium World Terrain、Bing 影像、OSM 建物,以及 Google 的 Photorealistic 3D Tiles。做戶外巡檢、長距離航線、地理座標對齊的模擬,這是目前最直接的選項。

但有一個實測回報的限制要先知道:**在無人機常見的作業高度(約 3~150 公尺)看,Google Photorealistic 3D Tiles 的幾何與貼圖細節不足。** 它是為城市尺度的鳥瞰設計的,拉近到貼近地面的高度就會糊掉甚至變黑。社群也回報過「感測器平台移動時要讓瓦片持續載入」需要額外處理。

所以合理的分工是:**高空航線規劃、長距離轉場用 Cesium 的真實地形;貼近地面的視覺任務用自己建的高細節局部場景。** 兩者混用,不要指望一套素材涵蓋所有高度。

---

## 4. 授權的三個坑

這一節比清單重要,因為素材的授權問題通常在專案後期才爆。

**沒有授權檔 ≠ 可以自由使用。** RotorS 與 AWS RoboMaker 的世界在 repo 根目錄都找不到授權檔(查證日 2026-08-05)。沒有明示授權的作品,預設是「保留所有權利」,不是公有領域。拿來自己實驗風險低,放進要出貨的產品或公開 repo 就要先釐清。AWS 那幾個世界另外還**已經封存**,連問都沒地方問。

**NVIDIA 的資產條款跟 Isaac Sim 的程式碼授權是兩回事。** [前面提過](01-training-stack.md)Isaac Sim 的原始碼是 Apache-2.0,但它依賴的 Omniverse Kit SDK 與 3D 資產另有 NVIDIA 授權。內建的機器人與場景資產屬於後者。

**串流內容的條款跟擴充的條款是兩回事。** Cesium for Omniverse 擴充本身是 Apache-2.0,但你串進來的 Google Photorealistic 3D Tiles、Bing 影像是各自的服務條款,通常限制快取、再散布與衍生用途。拿來訓練模型之前要看清楚——這一項最容易被忽略,因為技術上「它就跑起來了」。

實務建議:**在專案早期就建一份素材清單**,每一項記來源、授權、用途。這跟[開源生態那章](../05-open-source-landscape/01-landscape.md)講的軟體授權盤點是同一件事,只是對象換成 3D 資產。

### 這份筆記為什麼只收清單、不收檔案

上表的素材授權從 MIT、BSD-3、NVIDIA 資產條款一路到「查無授權檔」都有,而這個 repo 的文字與程式碼是 MIT。**把檔案收進來,整包的授權狀態就變成一團說不清楚的混合體**——讀者看到 repo 標 MIT,不會知道其中某個 `.usd` 其實不能商用,某個 `.urdf` 根本沒人授權過。

所以這裡只留清單、授權標註與選型判斷。真要把模型與世界檔案收成一包,該另開一個素材 repo,每一項連同它自己的授權與出處一起放,授權邊界跟文件切乾淨。這件事列在 [PLAN.md](../../PLAN.md) 的後續項目,尚未建立。

---

## 5. 從 CAD 到能飛,缺的是什麼

如果你手上真的只有機構部門給的 CAD,補齊清單如下:

| 要補的東西 | 怎麼來 |
|---|---|
| 質量 | 秤 |
| 轉動慣量 | CAD 軟體可以算(給對材料密度),或用雙線擺實測 |
| 推力係數、力矩係數 | 推力測試台實測,或抄同級槳的公開值 |
| 馬達時間常數 | 階躍響應實測 |
| 碰撞形狀 | 用簡化的凸包,**不要直接拿視覺網格當碰撞體**,physics 會非常慢 |
| 感測器位置與外參 | 從 CAD 量得到,這是 CAD 真正有用的地方 |
| 感測器雜訊與偏差 | 靜置實測 |

看這張表會發現一件事:**大部分項目要實測,而不是從 CAD 導出。** 這也是為什麼[第 15 章](../15-airframes-and-envelope/01-platform-parameters.md)把參數辨識排在建模擬環境之前——你不先量,模型裡的數字就是猜的,而[訓練會放大猜錯的部分](02-sim-to-real.md)。

CAD 唯一不可替代的貢獻是**幾何關係**:相機裝在哪、光達的視角有沒有被機臂擋住、天線離馬達多遠。這些用實測很難補,用 CAD 很直接。

---

## 6. 這一章的結論

1. CAD 只有幾何,沒有質量、慣量、關節與致動器;匯進來會得到一個像磚頭的模型。
2. 走 URDF 或 MJCF 進 Isaac Sim,物理資訊帶得進來;走 CAD 或 mesh 進來的要自己補。
3. 無人機模型的實際起點:Pegasus Simulator 的 USD(BSD-3),參數對照抄 gym-pybullet-drones 的 URDF(MIT)。但 Pegasus 只到 Isaac Sim 5.1,裝之前先定版本。
4. 世界模型:室內用 Isaac Sim 內建場景,戶外用 Cesium,但要知道 Google 3D Tiles 在無人機高度細節不足。
5. 三個授權坑:沒有授權檔不等於可自由使用、NVIDIA 資產條款不等於 Apache-2.0、串流內容條款不等於擴充條款。
6. 素材檔案不進這個 repo,授權太雜;要收就另開一個素材 repo,把授權邊界切乾淨。
7. 從 CAD 到能飛,缺的多半要實測;CAD 真正不可替代的是幾何關係(感測器裝在哪、會不會被擋住)。

→ 回 [65 章索引](README.md)
