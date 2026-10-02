#!/usr/bin/env python3
"""relay_server.py: minimal stdio MCP server (newline-delimited JSON-RPC 2.0, stdlib only) exposing ONLY the current
condition's tools for one trial. Item and condition come from the environment (R5_ITEM, R5_COND); every call is
appended to R5_CALLLOG as one JSON line."""
import json, os, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import items as IT  # noqa: E402
import tools as T  # noqa: E402

ITEM = next(i for i in IT.build_items() if i["id"] == os.environ["R5_ITEM"])
COND = os.environ["R5_COND"]
LOG = os.environ.get("R5_CALLLOG")


def send(o):
    sys.stdout.write(json.dumps(o) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            m = json.loads(line)
        except Exception:
            continue
        mid, meth = m.get("id"), m.get("method")
        if meth == "initialize":
            pv = (m.get("params") or {}).get("protocolVersion", "2025-06-18")
            send({"jsonrpc": "2.0", "id": mid, "result": {"protocolVersion": pv, "capabilities": {"tools": {}},
                                                          "serverInfo": {"name": "evidence", "version": "r5"}}})
        elif meth == "tools/list":
            send({"jsonrpc": "2.0", "id": mid, "result": {"tools": T.TOOLS[COND]}})
        elif meth == "tools/call":
            p = m.get("params") or {}
            t0 = time.perf_counter()
            try:
                err, text, meta = T.call(ITEM, COND, p.get("name"), p.get("arguments") or {})
            except Exception as e:
                err, text, meta = True, f"error: {type(e).__name__}", {}
            ms = (time.perf_counter() - t0) * 1000
            if LOG:
                with open(LOG, "a") as fh:
                    fh.write(json.dumps({"t": time.time(), "name": p.get("name"), "args": p.get("arguments"), "is_error": err,
                                         "ms": round(ms, 3), "meta": meta, "text": text[:2000]}, default=str) + "\n")
            send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": text}], "isError": err}})
        elif meth == "ping":
            send({"jsonrpc": "2.0", "id": mid, "result": {}})
        elif mid is not None and meth not in (None,) and not meth.startswith("notifications/"):
            send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "method not found"}})


if __name__ == "__main__":
    main()
