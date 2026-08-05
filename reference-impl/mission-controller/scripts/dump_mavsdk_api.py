"""把安裝好的 MAVSDK-Python 整個 introspect 出來,產生 API 全貌文件。

為什麼要有這支腳本:MAVSDK-Python 沒有官方的 API 參考文件,方法簽章又
在版本之間變動過(雲台在 3.x 加了 gimbal_id 與 take_control,相機加了
component_id)。抄一份文件進 repo 只會過期,所以這裡改成**留下產生器**:
真相是安裝好的套件本身,換版本重跑一次就得到那個版本的正確答案。

用法(依 repo 的硬規則,只在 docker 裡跑,不碰系統 Python):

    docker run --rm --cpus=2 -v "$PWD":/w -w /w \\
      ghcr.io/astral-sh/uv:python3.12-bookworm-slim \\
      sh -c 'uv venv -q /venv && VIRTUAL_ENV=/venv uv pip install -q mavsdk==3.17.2 \\
             && /venv/bin/python scripts/dump_mavsdk_api.py > ../../docs/20-protocols/03-mavsdk-api-surface.md'

輸出寫到 stdout,診斷訊息寫到 stderr。
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
import sys

import mavsdk

# gRPC 產生的模組不是給人用的介面,排除。
_SKIP_SUFFIX = ("_pb2", "_pb2_grpc")
_SKIP_NAME = {"bin"}


def _plugin_class(mod):
    """找出模組裡的 plugin 類別:定義在本模組且繼承 AsyncBase。"""
    for _, obj in inspect.getmembers(mod, inspect.isclass):
        if obj.__module__ != mod.__name__:
            continue
        if any(base.__name__ == "AsyncBase" for base in obj.__mro__[1:]):
            return obj
    return None


def _sig(fn) -> str:
    try:
        s = str(inspect.signature(fn))
    except (ValueError, TypeError):
        return "(?)"
    return s.replace("(self, ", "(").replace("(self)", "()")


def collect() -> tuple[str, dict]:
    try:
        from importlib.metadata import version

        ver = version("mavsdk")
    except Exception:  # noqa: BLE001 - 拿不到版本不該讓整份輸出失敗
        ver = "unknown"

    plugins: dict[str, dict] = {}
    for info in sorted(pkgutil.iter_modules(mavsdk.__path__), key=lambda m: m.name):
        name = info.name
        if name.startswith("_") or name in _SKIP_NAME or name.endswith(_SKIP_SUFFIX):
            continue
        try:
            mod = importlib.import_module(f"mavsdk.{name}")
        except Exception as err:  # noqa: BLE001
            print(f"skip {name}: {err}", file=sys.stderr)
            continue
        cls = _plugin_class(mod)
        if cls is None:
            continue

        methods = []
        for mname, fn in inspect.getmembers(cls, predicate=inspect.isfunction):
            if mname.startswith("_"):
                continue
            methods.append(
                {
                    "name": mname,
                    "sig": _sig(fn),
                    # async generator = 訂閱式串流,一般 coroutine = 單次呼叫。
                    # 這個差別決定呼叫端要用 async for 還是 await,是最常踩的地方。
                    "stream": inspect.isasyncgenfunction(fn),
                }
            )

        results: list[str] = []
        types: dict[str, dict] = {}
        for tname, tobj in inspect.getmembers(mod, inspect.isclass):
            if tobj.__module__ != mod.__name__ or tname == cls.__name__:
                continue
            if tname.endswith("Result"):
                res = getattr(tobj, "Result", None)
                if res is not None:
                    results = [k for k in vars(res) if k.isupper()]
                    continue
            enum_vals = [k for k in vars(tobj) if k.isupper()]
            fields = ""
            if not enum_vals:
                fields = _sig(tobj.__init__)
            types[tname] = {"enum": enum_vals, "fields": fields}

        plugins[name] = {
            "class": cls.__name__,
            "doc": (inspect.getdoc(cls) or "").strip().splitlines()[:1],
            "methods": methods,
            "results": results,
            "types": types,
        }
    return ver, plugins


def emit(ver: str, plugins: dict) -> None:
    w = sys.stdout.write
    n_m = sum(len(p["methods"]) for p in plugins.values())
    n_s = sum(sum(1 for m in p["methods"] if m["stream"]) for p in plugins.values())

    w(f"# MAVSDK-Python {ver} 介面全貌\n\n")
    w(
        "這份是**產生出來的**,不是手寫的。內容直接來自安裝好的 "
        f"`mavsdk=={ver}` 套件,用 `inspect` 讀出來,所以不會有「文件寫的跟"
        "套件裡的不一樣」這種問題。\n\n"
    )
    w(
        "重跑的指令與理由寫在 "
        "[`reference-impl/mission-controller/scripts/dump_mavsdk_api.py`]"
        "(../../reference-impl/mission-controller/scripts/dump_mavsdk_api.py)。"
        "換版本就重跑一次,不要手改這個檔。\n\n"
    )
    w(f"共 {len(plugins)} 個 plugin、{n_m} 個方法,其中 {n_s} 個是訂閱式串流。\n\n")

    w("## 出處\n\n")
    w(
        f"| 項目 | 出處 |\n|---|---|\n"
        f"| 本文所有簽章與型別 | 安裝於容器內的 `mavsdk=={ver}`,以 "
        f"`inspect.signature` / `inspect.getmembers` 讀出 |\n"
        f"| 套件 | <https://pypi.org/project/mavsdk/{ver}/> |\n"
        f"| 原始碼 | <https://github.com/mavlink/MAVSDK-Python> |\n"
        f"| 底層 C++ 實作 | <https://github.com/mavlink/MAVSDK> |\n\n"
        "MAVSDK-Python 沒有官方的方法級 API 參考,這也是這份文件存在的理由。"
        "上游若補了官方參考,以官方為準。\n\n"
    )

    w("## 怎麼讀\n\n")
    w(
        "- **呼叫**(`await drone.action.arm()`):一次性動作或查詢,回傳單一結果。\n"
        "- **串流**(`async for p in drone.telemetry.position():`):訂閱式,"
        "會一直吐值直到取消。**這是最常踩的地方**——把串流當呼叫 `await`,"
        "程式會停在那裡等一個永遠不會結束的東西。\n"
        "- `*_server` 結尾的 plugin 是**被控端**用的:自己扮演飛控或相機、"
        "回應地面站。做模擬器、假飛控或酬載元件時才會用到。\n"
        "- 失敗以例外拋出,錯誤碼列在每個 plugin 的 Result 清單。\n\n"
    )

    w("## Plugin 一覽\n\n")
    w("| Plugin | 類別 | 呼叫 | 串流 | 用途 |\n|---|---|---|---|---|\n")
    for name in sorted(plugins):
        p = plugins[name]
        s = sum(1 for m in p["methods"] if m["stream"])
        c = len(p["methods"]) - s
        role = "被控端" if "server" in name else "控制端"
        w(f"| [`{name}`](#{name.replace('_', '-')}) | `{p['class']}` | {c} | {s} | {role} |\n")
    w("\n---\n\n")

    for name in sorted(plugins):
        p = plugins[name]
        w(f"## {name}\n\n")
        w(f"類別 `mavsdk.{name}.{p['class']}`,存取路徑 `drone.{name}`。\n\n")

        if p["methods"]:
            w("| 方法 | 型態 |\n|---|---|\n")
            for m in sorted(p["methods"], key=lambda x: (x["stream"], x["name"])):
                kind = "串流" if m["stream"] else "呼叫"
                w(f"| `{m['name']}{m['sig']}` | {kind} |\n")
            w("\n")

        if p["results"]:
            w("錯誤碼:" + "、".join(f"`{r}`" for r in p["results"]) + "\n\n")

        if p["types"]:
            w("| 型別 | 內容 |\n|---|---|\n")
            for tname in sorted(p["types"]):
                t = p["types"][tname]
                if t["enum"]:
                    body = "列舉:" + "、".join(f"`{e}`" for e in t["enum"])
                else:
                    body = f"欄位 `{t['fields']}`" if t["fields"] else "—"
                w(f"| `{tname}` | {body} |\n")
            w("\n")

    w("---\n\n→ 回 [20 章索引](README.md)\n")


if __name__ == "__main__":
    emit(*collect())
