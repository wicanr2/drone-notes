# reference-impl

兩套可跑的骨架:

| 目錄 | 對應章節 | 內容 |
|---|---|---|
| [`mission-controller/`](mission-controller/) | [40 任務控制](../docs/40-mission-control/) | 雲端任務服務 + 機載任務執行器,可接假飛控或真 PX4 SITL |
| [`policy-lab/`](policy-lab/) | [65 Physical AI 模擬環境](../docs/65-physical-ai-sim/) | 飛行策略訓練骨架:訓練與驗收環境分離、安全外殼、指標驗收 |

---

# mission-controller:三層任務控制的最小骨架

這裡是[文件](../docs/40-mission-control/)講的東西的實際程式碼。目標不是做一個完整產品,而是讓「機載任務執行器怎麼寫、雲端任務服務怎麼設計、怎麼把它接上真的飛控並自動驗證」這幾件事有一份可以跑、可以改的起點。

架構刻意做成兩種後端共用同一套邏輯:

```
                       ┌──────────────────────────────┐
   HTTP API ─────────► │  雲端任務服務(定義 / 派工)   │
                       └──────────────┬───────────────┘
                                      │  冪等派工
                       ┌──────────────▼───────────────┐
                       │  機載任務執行器(狀態機)      │
                       └──────────────┬───────────────┘
                                      │  Vehicle 介面
                        ┌─────────────┴─────────────┐
                        ▼                           ▼
                 FakeVehicle                 MavsdkVehicle
              (虛擬時間 · 可注入中斷)        (真的 PX4 SITL / 實機)
```

同一份情境檔在兩種後端下都能跑,這是能建 CI 的前提。

---

## 快速開始

### 只跑任務服務(不需要 PX4)

```bash
docker compose up -d
curl -s localhost:8000/health
```

建立任務定義並派工:

```bash
DEF=$(curl -s -X POST localhost:8000/definitions \
      -H 'content-type: application/json' \
      -d @mission-controller/examples/survey-mission.json | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')

curl -s -X POST localhost:8000/plans -H 'content-type: application/json' \
     -d "{\"definition_id\":\"$DEF\",\"definition_version\":1,\"vehicle_id\":\"sim-01\"}"
```

跑情境測試:

```bash
docker compose exec mission-controller python scripts/run_scenario.py "scenarios/*.yaml"
```

### 接真的 PX4 SITL

```bash
MC_VEHICLE=mavsdk docker compose --profile sitl up -d
# PX4 開機到取得定位大約要一分鐘;服務會等它
until curl -s localhost:8000/health >/dev/null; do sleep 5; done
docker compose exec mission-controller python scripts/run_scenario.py scenarios/01-basic-mission.yaml
```

### 單元測試

```bash
cd mission-controller
docker run --rm -v "$PWD":/w -w /w ghcr.io/astral-sh/uv:python3.12-bookworm-slim \
  sh -c "uv venv -q && uv pip install -q -e '.[dev]' && .venv/bin/pytest -q"
```

---

## 驗證狀態

老實說明哪些跑過、哪些沒有:

| 項目 | 狀態 |
|---|---|
| 單元測試(執行器狀態機、恢復、冪等)20 項 | **通過** |
| 情境測試 × 2,假飛控後端 | **通過** |
| 情境測試 01,真 PX4 SITL v1.17 + Gazebo(無頭)+ MAVSDK | **通過**(起飛 → 三個航點 → 降落) |
| 情境的 `metrics` 斷言 | **未實作**——需要解析 ULog |
| 情境的 `inject` 故障注入 | **未實作**——需要注入介面 |
| 雲台與相機(`orbit_photo` 動作) | 只在假飛控後端可用;預設的 `gz_x500` 模型沒有相機,MAVSDK 的雲台/相機介面在不同版本間有變動,這裡不猜 |
| HITL / 實機 | **未驗證** |

文件裡[情境檔的完整格式](../docs/60-simulation-and-testing/03-ci-and-regression.md)包含 `metrics` 與 `inject`,那是目標形狀;這個骨架只實作了 events 與 final_state 的斷言,遇到未實作的欄位會印出「略過」而不是假裝驗過。

---

## 目錄

```
docker-compose.yml              兩個服務:任務服務 + (選用) PX4 SITL
mission-controller/
  src/mc/
    models.py                   定義 / 計畫 / 執行 / 事件 四種實體
    store.py                    SQLite;事件表 append-only,(execution_id, seq) 唯一
    actions.py                  動作與註冊表:takeoff / goto / orbit_photo / land / rtl
    executor.py                 執行迴圈:先存檔再發事件、中斷監看、恢復政策
    clock.py                    可注入時鐘(虛擬時間讓測試跑得飛快)
    api.py                      FastAPI:冪等派工、事件查詢
    vehicle/
      base.py                   Vehicle 介面
      fake.py                   假飛控:虛擬時間 + 可排程的中斷注入
      mavsdk_vehicle.py         接 PX4 SITL / 實機
  tests/                        20 項單元測試
  scenarios/                    宣告式情境檔
  scripts/run_scenario.py       情境執行器
```

---

## 三個踩過的坑

這些是實際跑出來才發現的,程式碼與文件都已經照修正後的版本更新:

**恢復政策不能假設中斷發生在動作完成後。** 起飛原本設成「中斷後跳過」(SKIP),理由是「已經在空中就不用再起飛」。但中斷可能打在起飛途中,這時飛機還在地面,跳過之後下一個 `goto` 就在錯誤前提下執行,被飛控拒絕。改成重跑該動作,由動作自己檢查實際狀態——**把冪等性放進動作,而不是靠恢復政策去猜。**

**「模式變了就是 failsafe」是錯的。** 接上真 SITL 之後,任務每次都在第二個航點被判定為中斷。原因是 PX4 執行完 `goto_location` 抵達目標後會自然進入 HOLD,而我把任何模式變更都當成 failsafe。正確的判斷要排除自己造成的模式變更,而且 HOLD 是正常的到點行為。

**PX4 容器在啟動當下就把目標主機名解析成 IP。** 之後只要任務服務容器被重建拿到新 IP,PX4 就繼續送到舊位址,現象是「連得上但永遠等不到遙測」。compose 因此改用固定 IP。

---

## 這個骨架刻意沒做的事

- **沒有認證授權**。真實系統的派工要綁操作者身分與權限。
- **沒有多機**。資料模型支援(每個計畫綁一台機),但沒有排程器。
- **沒有離線緩衝與補送**。事件直接寫本地 SQLite,沒有往上游同步的機制。
- **沒有 ULog 解析**。指標斷言要靠它。
- **雲端與機上是同一個行程**。真實部署要拆開,而且拆開之後才會遇到[文件裡講的那些一致性問題](../docs/40-mission-control/03-cloud-mission-service.md)。

這些留白是刻意的:骨架要小到能一次讀完,而上面每一項都足以撐起自己的一章。
