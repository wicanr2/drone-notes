# PLAN — 分輪進度

一輪推進一個主題,每輪結束 commit + push。完成的項目留在表上,不刪除,方便回頭追。

## 進度

| 輪次 | 主題 | 產出 | 狀態 |
|---|---|---|---|
| R1 | Repo 骨架 | `README.md` / `CLAUDE.md` / `CONTEXT.md` / `PLAN.md` / `LICENSE` | ✅ |
| R2 | 系統全景 | `docs/00-system-overview/` | ✅ |
| R3 | 開源生態與選型 | `docs/05-open-source-landscape/` | ✅ |
| R4 | 飛控軟體 | `docs/10-flight-controller/` | ✅ |
| R5 | 通訊協定 | `docs/20-protocols/` | ✅ |
| R6 | 機載運算 | `docs/30-companion-compute/` | ✅ |
| R7 | 任務控制三層 | `docs/40-mission-control/` | ✅ |
| R8 | 地面站與雲端 | `docs/50-gcs-and-cloud/` | ✅ |
| R9 | 模擬與測試 | `docs/60-simulation-and-testing/` | ✅ |
| R10 | AI 協作開發 | `docs/70-ai-assisted-development/` | ✅ |
| R11 | 手繪 SVG | `img/` 三張:延遲預算、座標系對照、三層任務控制 | ✅ |
| R12 | 參考實作骨架 | `reference-impl/`,已在 PX4 SITL v1.17 上驗過 | ✅ |
| R13 | 機體參數與飛行包絡 | `docs/15-airframes-and-envelope/` | ✅ |
| R14 | 軍用平台與照片 | `docs/15-.../03-military-classification.md`、`img/photos/` | ✅ |
| R15 | Physical AI 模擬環境 | `docs/65-physical-ai-sim/` | ✅ |
| R16 | 策略訓練骨架 | `reference-impl/policy-lab/`,9 項測試通過 | ✅ |
| R17 | README 改版 | 系統架構圖與爆炸圖(兼作章節導覽) | ✅ |
| R18 | 模擬素材 | `docs/65-physical-ai-sim/03-assets-and-worlds.md`,授權以 `gh api` 逐一查證 | ✅ |
| R19 | MAVSDK 介面與待查證清項 | `docs/20-protocols/03-mavsdk-api-surface.md`(產生器 + 產物)、雲台與相機實作 + 7 項測試、版本表與台灣法規查證 | ✅ |

## 每輪收尾流程

1. 寫完內容,自檢 `CLAUDE.md` 的每篇驗收標準
2. 新術語補進 `CONTEXT.md`
3. 更新 `README.md` 索引與本檔進度
4. `git add -A` → 繁中 commit → push

## 待補與待查證

| 項目 | 狀態 |
|---|---|
| reference-impl 在實體 Pixhawk 上的 HITL 驗證 | 未做,目前只驗過 SITL |
| 情境檔的 `metrics` 斷言(需解析 ULog) | 未實作,格式已在 docs/60 定義 |
| 情境檔的 `inject` 故障注入 | 未實作,假飛控後端已有排程中斷的機制可接 |
| 雲台與相機接真硬體 | 已依 MAVSDK 3.17.2 實作並有介面層測試,但無硬體可驗 |
| 民航局的射頻識別公告(門檻重量與技術規範) | 尚未發布,發布後要回頭補 docs/50 |
| Isaac Lab 3.0 與 Newton 的整合進度 | 仍在 beta(v3.0.0-beta2.patch1,2026-07-02),穩定後要回頭更新 65 章 |
| Pegasus 對 Isaac Sim 6.0 的支援 | 尚未支援(issue #131 未關閉),支援後要改 65-03 的版本建議 |
| Aerial Gym 對 Isaac Lab / Isaac Sim 的支援 | 官方標示開發中,完成後選型建議要改 |
| `mc_nn_control` 各參數的精確語意與實際飛行驗證 | 只確認模組與參數存在,未實跑 |
| RotorS 與 AWS RoboMaker worlds 的實際授權 | repo 根目錄查無授權檔(2026-08-05);未向作者確認,文件已標為風險 |
| Cesium for Omniverse 在無人機高度的細節不足 | 引自社群回報,本機未實測 |
| Isaac Sim 內建資產(Crazyflie / Quadcopter USD)的路徑 | 引自官方文件,未在本機安裝驗證 |

## 後續可擴充

- **獨立的模擬素材 repo**(名稱未定)。這個 repo 只收清單與判斷,不收 3D 檔案——素材授權從 MIT、BSD-3、NVIDIA 資產條款到「查無授權檔」都有,混進 MIT 的文件 repo 會讓整包的授權狀態說不清楚。要收成一包時另開,每一項素材連同自己的授權與出處一起放。判斷依據見 [65-03](docs/65-physical-ai-sim/03-assets-and-worlds.md)。
- 各章的實測數據:鏈路頻寬預算、Offboard 延遲、EKF innovation 正常區間
- 多機模擬與群飛的 CI 範例
- 影像管線(GStreamer / WebRTC)的完整 lab
- 從 ULog 到自動化異常判讀的分析腳本
