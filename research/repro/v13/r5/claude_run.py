"""claude_run.py: one headless Claude Code session per trial (adapted from research/v13/evidence/g2_handoff/claude_run.py).

Isolation: fresh empty temp cwd, --strict-mcp-config with only this trial's server (or none), --tools "" (no built-in
tools), --setting-sources "", --no-session-persistence, --disable-slash-commands, --system-prompt (replaces Claude
Code's default prompt). stream-json is parsed for every tool call and tool result.
"""
import json, os, subprocess, sys, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EMPTY_MCP = json.dumps({"mcpServers": {}})


def run(prompt, system, model, mcp_config, allowed, disallowed=None, effort=None, budget="0.50", max_turns=8,
        timeout=420, env_extra=None):
    cwd = tempfile.mkdtemp(prefix="r5_")
    cfg_dir = tempfile.mkdtemp(prefix="r5cfg_")
    cfg = os.path.join(cfg_dir, "mcp.json")
    Path(cfg).write_text(mcp_config or EMPTY_MCP)
    cmd = ["claude", "-p", prompt, "--system-prompt", system, "--mcp-config", cfg, "--strict-mcp-config",
           "--tools", "", "--output-format", "stream-json", "--verbose", "--model", model,
           "--no-session-persistence", "--setting-sources", "", "--disable-slash-commands",
           "--permission-prompts", "none", "--max-budget-usd", budget, "--max-turns", str(max_turns)]
    if allowed:
        cmd += ["--allowedTools", allowed]
    if disallowed:
        cmd += ["--disallowedTools", ",".join(disallowed)]
    if effort:
        cmd += ["--effort", effort]
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD",
                                                           "CLAUDE_ADDITIONAL_DIRECTORIES")}
    env.update(env_extra or {})
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        stdout, stderr, rc = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr, rc = "TIMEOUT", -9
    wall = time.time() - t0
    msgs = []
    for l in stdout.splitlines():
        if l.strip().startswith("{"):
            try:
                msgs.append(json.loads(l))
            except Exception:
                pass
    calls, results, init, final, texts = [], [], None, None, []
    for m in msgs:
        if m.get("type") == "system" and m.get("subtype") == "init":
            init = m
        elif m.get("type") == "assistant":
            for c in m["message"].get("content", []):
                if c.get("type") == "tool_use":
                    calls.append({"id": c["id"], "name": c["name"], "input": c["input"], "t": time.time()})
                elif c.get("type") == "text":
                    texts.append(c.get("text", ""))
        elif m.get("type") == "user":
            cont = m.get("message", {}).get("content", [])
            if isinstance(cont, list):
                for c in cont:
                    if c.get("type") == "tool_result":
                        txt = c.get("content")
                        if isinstance(txt, list):
                            txt = "".join(x.get("text", "") for x in txt if isinstance(x, dict))
                        results.append({"tool_use_id": c["tool_use_id"], "is_error": c.get("is_error", False),
                                        "text": txt or ""})
        elif m.get("type") == "result":
            final = m
    res_text = (final or {}).get("result", "") or ""
    if not res_text and texts:
        res_text = texts[-1]
    return {
        "wall_s": round(wall, 2), "exit": rc, "stderr_tail": stderr[-400:],
        "tools_offered": (init or {}).get("tools"), "mcp_servers": (init or {}).get("mcp_servers"),
        "model_init": (init or {}).get("model"), "cli_version": (init or {}).get("claude_code_version"),
        "calls": calls, "results": results, "result_text": res_text, "all_text": "\n".join(texts),
        "cost_usd": (final or {}).get("total_cost_usd"), "duration_ms": (final or {}).get("duration_ms"),
        "num_turns": (final or {}).get("num_turns"), "is_error": (final or {}).get("is_error"),
        "subtype": (final or {}).get("subtype"), "usage": (final or {}).get("usage"),
        "modelUsage": (final or {}).get("modelUsage"), "n_msgs": len(msgs),
    }


if __name__ == "__main__":
    print(json.dumps(run(sys.argv[1], "Answer briefly.", sys.argv[2], None, None), indent=1)[:3000])
