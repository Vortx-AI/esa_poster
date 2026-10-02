"""STEP 1: agent A = Claude Code (claude-sonnet-5-5) with emem as its only plugin/MCP server. n=10."""
import json, os, re, sys
from claude_run import run

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "raw", "agent_a"); os.makedirs(OUT, exist_ok=True)
PROMPT = ("Using emem, find the latest Sentinel-2 NDVI at Keylong, Lahaul (32.57126 N, 77.03448 E). Output exactly two lines: "
          "HANDOFF_TOKEN=<the emem:fact token of the value you used> and HANDOFF_PROSE=<one sentence for a colleague, no token>.")
HERO = "emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa"
n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
with open(os.path.join(HERE, "agent_a.jsonl"), "a") as fo:
    for i in range(start, start + n):
        r = run(PROMPT, "claude-sonnet-5-5", f"a{i:02d}", OUT)
        txt = r["result_text"]
        m1 = re.search(r"HANDOFF_TOKEN=\s*(\S+)", txt); m2 = re.search(r"HANDOFF_PROSE=\s*(.+)", txt)
        r["handoff_token"] = m1.group(1).strip("`<>") if m1 else None
        r["handoff_prose"] = m2.group(1).strip() if m2 else None
        r["token_equals_hero"] = r["handoff_token"] == HERO
        r["prompt"] = PROMPT; r["i"] = i; r.pop("_full_results", None)
        fo.write(json.dumps(r) + "\n"); fo.flush()
        print(i, r["models_used"], r["cost_usd"], r["wall_s"], [c["name"] for c in r["calls"]], r["handoff_token"], "|", r["handoff_prose"], flush=True)
