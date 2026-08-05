"""從 PX4 原始碼產生 API 參考:uORB 訊息、參數、MAVLink 介面。

為什麼是產生器而不是手抄的文件:PX4 每半年一個大版本,uORB 訊息與參數
都會增刪。手抄的快照一定會過期,而且過期的時候看不出來。這支腳本吃一份
釘死版本的原始碼,產出的東西可以隨時重跑對齊。

真相是原始碼。這裡不從官方文件網站抓任何東西——那是二手的,而且版本
對不上(docs.px4.io 預設顯示 main 分支)。

用法(只在 docker 裡跑):

    # 1. 抓一份釘版本的原始碼
    curl -sL -o px4.tar.gz \\
      https://github.com/PX4/PX4-Autopilot/archive/refs/tags/v1.17.0.tar.gz
    mkdir -p px4 && tar xzf px4.tar.gz -C px4 --strip-components=1

    # 2. 產生
    docker run --rm --cpus=2 -v "$PWD":/w -w /w \\
      ghcr.io/astral-sh/uv:python3.12-bookworm-slim \\
      sh -c 'uv venv -q /venv && VIRTUAL_ENV=/venv uv pip install -q pyyaml \\
             && /venv/bin/python dump_px4_api.py px4 v1.17.0 <輸出目錄>'
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

# --- uORB 訊息 -------------------------------------------------------------

_CONST = re.compile(r"^\s*(\w+(?:\[\d*\])?)\s+([A-Z0-9_]+)\s*=\s*(.+?)\s*(?:#.*)?$")
_FIELD = re.compile(r"^\s*([\w/]+(?:\[\d*\])?)\s+(\w+)\s*(?:#\s*(.*))?$")
_TOPICS = re.compile(r"^#\s*TOPICS\s+(.+)$")


def parse_msg(path: Path) -> dict:
    """解析一個 .msg 檔。

    格式很簡單但有兩個容易漏的東西:大寫的等號行是常數不是欄位,而
    `# TOPICS a b c` 這種註解會宣告出額外的主題名——同一個訊息型別可以
    對應多個主題(例如 VehicleAttitudeSetpoint 之於不同的控制器)。
    """
    name = path.stem
    fields: list[dict] = []
    consts: list[dict] = []
    topics: list[str] = []
    doc: list[str] = []
    seen_field = False

    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        m = _TOPICS.match(line.strip())
        if m:
            # 一個訊息可以有多行 TOPICS(VehicleAttitude 就有兩行),要累加。
            # 覆寫的話會只留下最後一行,把 vehicle_attitude 這個主名弄丟。
            topics.extend(m.group(1).split())
            continue
        if line.lstrip().startswith("#"):
            # 只把出現在第一個欄位之前的註解當成訊息說明,之後的是欄位註解。
            if not seen_field:
                doc.append(line.lstrip("# ").strip())
            continue
        m = _CONST.match(line)
        if m and "=" in line:
            consts.append({"type": m.group(1), "name": m.group(2), "value": m.group(3)})
            continue
        m = _FIELD.match(line)
        if m:
            seen_field = True
            fields.append({"type": m.group(1), "name": m.group(2), "comment": (m.group(3) or "").strip()})

    return {
        "name": name,
        "file": str(path.as_posix()),
        "versioned": "versioned" in path.parts,
        "doc": " ".join(d for d in doc if d),
        "fields": fields,
        "consts": consts,
        # 沒寫 TOPICS 的訊息,主題名就是檔名轉 snake_case。
        "topics": topics or [_snake(name)],
    }


def _snake(camel: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel).lower()


# --- 參數 -----------------------------------------------------------------

# doc 內容不得含 `*/`。用 `.*?` 會從檔頭的授權區塊 `/****…` 開始吃,
# 因為那個區塊自己的 `****/` 後面不是 PARAM_DEFINE,lazy 量詞會一路
# 擴張到真正的說明區塊——結果每個檔案的第一個參數說明都變成 Copyright。
_PARAM_C = re.compile(
    r"/\*\*(?P<doc>(?:[^*]|\*(?!/))*)\*/\s*"
    r"PARAM_DEFINE_(?P<kind>INT32|FLOAT)\s*\(\s*(?P<name>\w+)\s*,\s*(?P<default>[^)]+?)\s*\)",
    re.S,
)
_TAG = re.compile(r"^\s*\*?\s*@(\w+)\s*(.*)$")

# 沒有說明區塊的 PARAM_DEFINE(原始碼裡確實有,例如 SPC_VEHICLE_RESP)。
# `(?!\s*//)` 是必要的:voxl_esc 把四個 PARAM_DEFINE 註解掉留作參考,
# 那些不是真的參數,抓進來會多報。
_PARAM_BARE = re.compile(
    r"^(?!\s*//)\s*PARAM_DEFINE_(?P<kind>INT32|FLOAT)\s*\(\s*(?P<name>\w+)\s*,\s*(?P<default>[^)]+?)\s*\)",
    re.M,
)


def parse_params_c(path: Path) -> list[dict]:
    """解析 PARAM_DEFINE_* 巨集與它前面的 doxygen 註解區塊。

    舊式的參數定義走這條路。註解裡的 @group / @unit / @min / @max 是
    地面站顯示與驗證用的,不是純說明,所以要一起抓出來。
    """
    out: list[dict] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for m in _PARAM_C.finditer(text):
        doc_lines = [ln.strip().lstrip("*").strip() for ln in m.group("doc").splitlines()]
        short, long_, tags = "", [], {}
        for ln in doc_lines:
            t = _TAG.match(ln)
            if t:
                tags.setdefault(t.group(1), t.group(2).strip())
                continue
            if not ln:
                continue
            if not short:
                short = ln
            else:
                long_.append(ln)
        out.append(
            {
                "name": m.group("name"),
                "type": "int32" if m.group("kind") == "INT32" else "float",
                "default": m.group("default").strip(),
                "short": short,
                "long": " ".join(long_),
                "group": tags.get("group", "未分組"),
                "unit": tags.get("unit", ""),
                "min": tags.get("min", ""),
                "max": tags.get("max", ""),
                "source": path.as_posix(),
            }
        )

    # 補上沒有說明區塊的那些,否則它們會安靜消失。
    named = {p["name"] for p in out}
    for m in _PARAM_BARE.finditer(text):
        if m.group("name") in named:
            continue
        out.append(
            {
                "name": m.group("name"),
                "type": "int32" if m.group("kind") == "INT32" else "float",
                "default": m.group("default").strip(),
                "short": "",
                "long": "",
                "group": "未分組",
                "unit": "",
                "min": "",
                "max": "",
                "source": path.as_posix(),
            }
        )
    return out


def parse_params_yaml(path: Path) -> list[dict]:
    """解析 module.yaml 的 parameters 區塊(新式定義)。"""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as err:  # noqa: BLE001 - 個別檔壞掉不該讓整份輸出失敗
        print(f"skip {path}: {err}", file=sys.stderr)
        return []
    if not isinstance(data, dict):
        return []

    out: list[dict] = []
    for group in data.get("parameters", []) or []:
        gname = group.get("group", "未分組")
        for pname, p in (group.get("definitions") or {}).items():
            if not isinstance(p, dict):
                continue
            desc = p.get("description") or {}
            # instance_start 型的參數名字帶 ${i},展開成實際數量。
            names = [pname]
            if "${i}" in pname:
                start = int(p.get("instance_start", 0))
                count = int(p.get("num_instances", 1))
                names = [pname.replace("${i}", str(start + i)) for i in range(count)]
            for n in names:
                out.append(
                    {
                        "name": n,
                        "type": str(p.get("type", "")),
                        "default": _fmt_default(p.get("default")),
                        "short": str(desc.get("short", "")).strip(),
                        "long": " ".join(str(desc.get("long", "")).split()),
                        "group": gname,
                        "unit": str(p.get("unit", "")),
                        "min": _fmt_default(p.get("min")),
                        "max": _fmt_default(p.get("max")),
                        "source": path.as_posix(),
                    }
                )
    return out


def _fmt_default(v) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return str(v)


# --- MAVLink 介面 -----------------------------------------------------------

_STREAM_NAME = re.compile(r'get_name_static\(\)\s*\{\s*return\s*"([A-Z0-9_]+)"')
_MSGID_CASE = re.compile(r"case\s+MAVLINK_MSG_ID_([A-Z0-9_]+)\s*:")


def parse_mavlink(root: Path) -> dict:
    streams: list[dict] = []
    sdir = root / "src/modules/mavlink/streams"
    for f in sorted(sdir.glob("*.hpp")):
        text = f.read_text(encoding="utf-8", errors="replace")
        m = _STREAM_NAME.search(text)
        if m:
            streams.append({"name": m.group(1), "file": f.name})

    inbound: set[str] = set()
    rx = root / "src/modules/mavlink/mavlink_receiver.cpp"
    if rx.exists():
        inbound = set(_MSGID_CASE.findall(rx.read_text(encoding="utf-8", errors="replace")))

    return {"streams": streams, "inbound": sorted(inbound)}


# --- 輸出 -------------------------------------------------------------------

_HEAD = """> 這份是**產生出來的**,不是手寫的。內容直接解析 PX4 `{tag}` 的原始碼,\
產生器與重跑指令在 [`tools/dump_px4_api.py`](../../../tools/dump_px4_api.py)。\
換版本重跑,不要手改這個檔。

## 出處

| 項目 | 出處 |
|---|---|
| 原始碼 | <https://github.com/PX4/PX4-Autopilot/tree/{tag}>,tarball 為 `archive/refs/tags/{tag}.tar.gz` |
| 解析範圍 | {scope} |
| 官方參考 | <https://docs.px4.io/>(預設顯示 main 分支,與此處的 `{tag}` 可能不同) |

"""


def emit_msgs(msgs: list[dict], tag: str, out: Path) -> None:
    versioned = [m for m in msgs if m["versioned"]]
    internal = [m for m in msgs if not m["versioned"]]
    w = []
    w.append(f"# PX4 uORB 訊息全集 — {tag}\n\n")
    w.append(
        _HEAD.format(tag=tag, scope="`msg/**/*.msg`,共 %d 則(對外契約 %d 則、內部 %d 則)"
                     % (len(msgs), len(versioned), len(internal)))
    )
    w.append(
        "## 先看這件事:兩區的差別\n\n"
        f"`msg/versioned/` 底下的 **{len(versioned)} 則是刻意穩定下來的對外契約**,"
        f"其餘 {len(internal)} 則是內部實作細節。\n\n"
        "差別不在技術上——兩者都是一樣的 uORB 主題,伴隨電腦都訂閱得到。"
        "差別在**承諾**:versioned 的那批改動會顧及相容性,內部的那批可能在"
        "任何一個版本改掉欄位而不另行通知。**寫伴隨電腦程式時依賴內部訊息,"
        "是把自己綁在特定韌體版本上。**\n\n"
        "---\n\n"
    )

    for title, group in (("對外契約(`msg/versioned/`)", versioned), ("內部訊息(`msg/`)", internal)):
        w.append(f"## {title}\n\n")
        w.append("| 訊息 | 欄位數 | 常數 | 說明 |\n|---|---|---|---|\n")
        for m in sorted(group, key=lambda x: x["name"]):
            anchor = m["name"].lower()
            doc = (m["doc"][:70] + "…") if len(m["doc"]) > 70 else m["doc"]
            w.append(f"| [`{m['name']}`](#{anchor}) | {len(m['fields'])} | {len(m['consts'])} | {doc} |\n")
        w.append("\n")

    w.append("---\n\n# 逐則定義\n\n")
    for m in sorted(msgs, key=lambda x: (not x["versioned"], x["name"])):
        w.append(f"## {m['name']}\n\n")
        badge = "對外契約" if m["versioned"] else "內部訊息"
        w.append(f"{badge} · 主題名 " + "、".join(f"`{t}`" for t in m["topics"]) + "\n\n")
        if m["doc"]:
            w.append(f"{m['doc']}\n\n")
        if m["fields"]:
            w.append("| 欄位 | 型別 | 說明 |\n|---|---|---|\n")
            for f in m["fields"]:
                w.append(f"| `{f['name']}` | `{f['type']}` | {f['comment']} |\n")
            w.append("\n")
        if m["consts"]:
            w.append("常數:" + "、".join(f"`{c['name']}={c['value']}`" for c in m["consts"]) + "\n\n")
    w.append("---\n\n→ 回 [附錄索引](README.md)\n")
    out.write_text("".join(w), encoding="utf-8")


def emit_params(params: list[dict], tag: str, out: Path) -> None:
    groups: dict[str, list[dict]] = {}
    for p in params:
        groups.setdefault(p["group"], []).append(p)

    w = []
    w.append(f"# PX4 參數全集 — {tag}\n\n")
    w.append(
        _HEAD.format(
            tag=tag,
            scope="`src/**/module.yaml` 的 `parameters` 區塊 + `src/**/*.c` 的 "
            f"`PARAM_DEFINE_*` 巨集,共 {len(params)} 個參數、{len(groups)} 個群組",
        )
    )
    w.append(
        "## 怎麼用這份東西\n\n"
        "**不要從頭讀。** 參數是查詢用的,不是閱讀用的。實際會用到的方式有三種:"
        "在地面站裡搜名字、在文件裡確認單位與範圍、看某個功能牽動哪些參數(用群組)。\n\n"
        "有幾個地方值得先知道:\n\n"
        "- **參數名有 16 字元上限**,所以縮寫很兇。`MC_ROLLRATE_P` 是多旋翼滾轉"
        "角速率的比例增益,不是別的。\n"
        "- **改參數會即時生效,但不是每個都安全**。控制增益在飛行中改會直接"
        "影響穩定性。\n"
        "- **預設值是「某台參考機」的值**,不是你的機。特別是慣量、推力、"
        "增益這幾類,照抄預設等於假設你的機跟參考機一樣。\n\n"
    )
    undoc = [p for p in params if not (p["short"] or p["long"])]
    if undoc:
        w.append(
            f"其中 **{len(undoc)} 個參數在原始碼裡沒有說明**"
            + "(" + "、".join(f"`{p['name']}`" for p in undoc[:8])
            + ("…" if len(undoc) > 8 else "")
            + "),這裡照實留白,不代為推測用途。\n\n"
        )
    w.append("---\n\n## 群組\n\n| 群組 | 參數數 |\n|---|---|\n")
    for g in sorted(groups, key=lambda x: (-len(groups[x]), x)):
        w.append(f"| [{g}](#{_anchor(g)}) | {len(groups[g])} |\n")
    w.append("\n---\n\n")

    for g in sorted(groups, key=lambda x: (-len(groups[x]), x)):
        w.append(f"## {g}\n\n")
        w.append("| 參數 | 型別 | 預設 | 範圍 | 單位 | 說明 |\n|---|---|---|---|---|---|\n")
        for p in sorted(groups[g], key=lambda x: x["name"]):
            rng = f"{p['min']} ~ {p['max']}" if (p["min"] or p["max"]) else ""
            desc = p["short"] or p["long"]
            desc = desc.replace("|", "\\|")
            w.append(
                f"| `{p['name']}` | {p['type']} | {p['default']} | {rng} | {p['unit']} | {desc} |\n"
            )
        w.append("\n")
    w.append("---\n\n→ 回 [附錄索引](README.md)\n")
    out.write_text("".join(w), encoding="utf-8")


def _anchor(s: str) -> str:
    return re.sub(r"[^\w一-鿿-]+", "-", s.lower()).strip("-")


def emit_mavlink(mav: dict, tag: str, out: Path) -> None:
    w = []
    w.append(f"# PX4 的 MAVLink 介面 — {tag}\n\n")
    w.append(
        _HEAD.format(
            tag=tag,
            scope="`src/modules/mavlink/streams/*.hpp`(發送)與 "
            f"`mavlink_receiver.cpp` 的 `switch (msg->msgid)`(接收),"
            f"共 {len(mav['streams'])} 個發送串流、{len(mav['inbound'])} 種接收訊息",
        )
    )
    w.append(
        "## 這兩張表回答的是不同問題\n\n"
        "**發送串流**是 PX4 有能力送出的訊息。實際會不會送、以什麼頻率送,"
        "由訊息串流設定與鏈路頻寬決定——[頻寬預算那節](../../20-protocols/02-routing-and-bandwidth.md)"
        "算過,57600 bps 的鏈路塞不下全部。\n\n"
        "**接收訊息**是 PX4 會處理的入站訊息。**不在這張表裡的訊息會被安靜丟棄**,"
        "這是「送出去但沒反應」最常見的原因,而且不會有錯誤訊息。\n\n"
        "---\n\n"
    )
    w.append(f"## 發送串流({len(mav['streams'])})\n\n| 訊息 | 實作檔 |\n|---|---|\n")
    for s in sorted(mav["streams"], key=lambda x: x["name"]):
        w.append(f"| `{s['name']}` | `streams/{s['file']}` |\n")
    w.append(f"\n## 會處理的入站訊息({len(mav['inbound'])})\n\n")
    w.append("| 訊息 |\n|---|\n")
    for n in mav["inbound"]:
        w.append(f"| `{n}` |\n")
    w.append("\n---\n\n→ 回 [附錄索引](README.md)\n")
    out.write_text("".join(w), encoding="utf-8")


def main() -> None:
    root = Path(sys.argv[1])
    tag = sys.argv[2]
    outdir = Path(sys.argv[3])
    outdir.mkdir(parents=True, exist_ok=True)

    msgs = [parse_msg(p) for p in sorted((root / "msg").rglob("*.msg"))]

    params: list[dict] = []
    for p in sorted((root / "src").rglob("module.yaml")):
        params.extend(parse_params_yaml(p))
    for p in sorted((root / "src").rglob("*.c")):
        if "PARAM_DEFINE" in p.read_text(encoding="utf-8", errors="replace"):
            params.extend(parse_params_c(p))
    # 同名以先出現者為準(module.yaml 優先),重複定義是 PX4 遷移期的常態。
    seen: set[str] = set()
    uniq = []
    for p in params:
        if p["name"] in seen:
            continue
        seen.add(p["name"])
        uniq.append(p)

    mav = parse_mavlink(root)

    emit_msgs(msgs, tag, outdir / "uorb-all-topics.md")
    emit_params(uniq, tag, outdir / "parameters-full.md")
    emit_mavlink(mav, tag, outdir / "mavlink-command-support.md")

    print(
        json.dumps(
            {
                "messages": len(msgs),
                "versioned": sum(1 for m in msgs if m["versioned"]),
                "params": len(uniq),
                "param_groups": len({p["group"] for p in uniq}),
                "streams": len(mav["streams"]),
                "inbound": len(mav["inbound"]),
            },
            ensure_ascii=False,
        ),
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
