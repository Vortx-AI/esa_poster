"""Executes agent B's resolve(token) call via the official MCP Python SDK (mcp 2.x, streamable HTTP) against https://emem.dev/mcp.
Returns (trimmed_for_model, full_structured, meta)."""
import asyncio, json, time
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = "https://emem.dev/mcp"


async def _call(token):
    async with streamable_http_client(URL) as streams:
        r, w = streams[0], streams[1]
        async with ClientSession(r, w) as s:
            init = await s.initialize()
            t0 = time.perf_counter()
            res = await s.call_tool("emem_memory_token_resolve", {"token": token})
            ms = (time.perf_counter() - t0) * 1000
            return init, res, ms


def _iserr(res):
    return bool(getattr(res, 'is_error', None) if hasattr(res, 'is_error') else getattr(res, 'isError', False))


def resolve(token):
    init, res, ms = asyncio.run(_call(token))
    text = "".join(getattr(c, "text", "") for c in res.content)
    sc = getattr(res, 'structured_content', None) if hasattr(res, 'structured_content') else getattr(res, 'structuredContent', None)
    if sc is None:
        try:
            sc = json.loads(text)
        except Exception:
            sc = None
    trimmed = {"isError": bool(_iserr(res))}
    if isinstance(sc, dict) and not _iserr(res):
        fact = sc.get("fact", {})
        trimmed.update({"fact_cid": sc.get("fact_cid"), "value": fact.get("value", sc.get("value")), "unit": sc.get("unit"),
                        "band": sc.get("band"), "cell_matches": sc.get("cell_matches")})
    else:
        trimmed["error"] = text[:700]
    meta = {"server": f"{init.server_info.name if hasattr(init,'server_info') else init.serverInfo.name}",
            "protocol": getattr(init, "protocol_version", None) or getattr(init, "protocolVersion", None), "call_ms": round(ms, 1)}
    return trimmed, sc, meta


if __name__ == "__main__":
    import sys
    t, sc, meta = resolve(sys.argv[1])
    print(json.dumps(t)); print(json.dumps(meta))
    if isinstance(sc, dict):
        print(sorted(sc.keys()))
