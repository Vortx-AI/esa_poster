"""Run one headless Claude Code session with emem as its only MCP server, and parse the stream-json output.

Used for agent A (sonnet) and agent B-claude (haiku). Each run gets a fresh empty temporary cwd.
"""
import json, os, re, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
MCP = os.path.join(HERE, "emem_mcp.json")  # verbatim copy of emem/plugins/emem/.mcp.json
CID_RE = re.compile(r"\b[a-z2-7]{52}\b")
TOK_RE = re.compile(r"emem:fact:[A-Za-z0-9.]+:[a-z2-7]{52}")


def run(prompt, model, tag, outdir, budget="1"):
    cwd = tempfile.mkdtemp(prefix=f"{tag}_")
    cmd = ["claude", "-p", prompt, "--mcp-config", MCP, "--strict-mcp-config",
           "--allowedTools", "mcp__emem__*", "--tools", "", "--output-format", "stream-json", "--verbose",
           "--model", model, "--no-session-persistence", "--setting-sources", "", "--disable-slash-commands",
           "--permission-prompts", "none", "--max-budget-usd", budget]
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD", "CLAUDE_ADDITIONAL_DIRECTORIES")}
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=600)
    wall = time.time() - t0
    raw_path = os.path.join(outdir, f"{tag}.jsonl")
    open(raw_path, "w").write(p.stdout)
    open(os.path.join(outdir, f"{tag}.err"), "w").write(p.stderr)
    msgs = [json.loads(l) for l in p.stdout.splitlines() if l.strip().startswith("{")]
    calls, results, init, final = [], [], None, None
    for m in msgs:
        if m.get("type") == "system" and m.get("subtype") == "init":
            init = m
        elif m.get("type") == "assistant":
            for c in m["message"].get("content", []):
                if c.get("type") == "tool_use":
                    calls.append({"id": c["id"], "name": c["name"], "input": c["input"]})
        elif m.get("type") == "user":
            cont = m.get("message", {}).get("content", [])
            if isinstance(cont, list):
                for c in cont:
                    if c.get("type") == "tool_result":
                        txt = c.get("content")
                        if isinstance(txt, list):
                            txt = "".join(x.get("text", "") for x in txt if isinstance(x, dict))
                        results.append({"tool_use_id": c["tool_use_id"], "is_error": c.get("is_error", False), "text": txt or ""})
        elif m.get("type") == "result":
            final = m
    res_text = (final or {}).get("result", "") or ""
    tool_cids = sorted({x for r in results for x in CID_RE.findall(r["text"])})
    tool_tokens = sorted({x for r in results for x in TOK_RE.findall(r["text"])})
    mu = (final or {}).get("modelUsage", {})
    return {
        "tag": tag, "model_requested": model, "models_used": list(mu.keys()), "cwd": cwd, "wall_s": round(wall, 2),
        "exit": p.returncode, "tools_offered": (init or {}).get("tools"), "mcp_servers": (init or {}).get("mcp_servers"),
        "calls": calls, "results": [{"tool_use_id": r["tool_use_id"], "is_error": r["is_error"], "len": len(r["text"]),
                                     "head": r["text"][:600]} for r in results],
        "result_text": res_text, "cost_usd": (final or {}).get("total_cost_usd"), "duration_ms": (final or {}).get("duration_ms"),
        "num_turns": (final or {}).get("num_turns"), "is_error": (final or {}).get("is_error"),
        "usage": (final or {}).get("usage"), "modelUsage": mu,
        "tool_result_cids": tool_cids, "tool_result_tokens": tool_tokens, "raw": raw_path,
        "_full_results": results,
    }


if __name__ == "__main__":
    print(json.dumps(run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]), indent=1))
