#!/usr/bin/env python3
"""run_claude.py: R5 trial runner for Claude models (Blocks P, 1, 2). Resumable; appends one row per trial to
trials.jsonl and keeps a cost ledger (ledger.jsonl). Stops before a trial that would cross the cap.

  python run_claude.py --block P --model claude-haiku-4-5-20251001
  python run_claude.py --block 1 --model claude-haiku-4-5-20251001 --reps 5
  python run_claude.py --block 2 --model claude-sonnet-5-5 --reps 1
"""
import argparse, fcntl, json, os, random, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import claude_run  # noqa: E402
import items as IT  # noqa: E402
import score as S  # noqa: E402

TRIALS = HERE / "trials.jsonl"
LEDGER = HERE / "ledger.jsonl"
RAW = HERE / "raw"
RAW.mkdir(exist_ok=True)
HARD_CAP = 40.0
SOFT_CAP = 38.0
SEED = 20261019
EFFORT = {"claude-haiku-4-5-20251001": None, "claude-sonnet-5-5": "medium", "claude-opus-5-5": "medium"}
PILOT_ITEMS = ["G0", "M4", "M8", "M15"]
LIVE_ITEMS = ["G0", "M2", "M4", "M5", "M5b", "M6", "M7", "M15r", "M19", "G0-B", "M20"]
LIVE_CONDS = ["L0", "L1", "L2"]   # E0-plugin, E-plugin (instructed), E-plugin + our verifier (re-read)
CONTROLS = ("G0", "G0-B")
EMEM_DISALLOW = ["emem_entity", "emem_locate", "emem_recall", "emem_memory_token", "emem_memory_contradictions",
                 "emem_guard_verdict", "emem_tools", "emem_ask", "search", "fetch", "emem_echo_verify", "emem_memory_bundle",
                 "emem_entity_resolve", "emem_entity_link", "emem_find_similar", "emem_intent"]
L1_K = ("Before you use an emem token, resolve it with emem_memory_token_resolve and check that the resolved record's cell, band "
        "and date match YOUR question, not the handoff's. Use a value only if they match and the resolve succeeds; otherwise DECLINE.")
L1_B = ("Before you use an emem token, resolve it with emem_memory_token_resolve and check that the resolved record's cell and band "
        "match YOUR question and that it was signed by the as-of time. Use a value only if all of this holds; otherwise DECLINE.")
L2_K = ("Before you use an emem token, resolve it with emem_memory_token_resolve, and also call verify_evidence with the cell, band "
        "and date of YOUR question, not the handoff's. Use a value only if the resolve succeeds and every check passes; otherwise DECLINE.")
L2_B = ("Before you use an emem token, resolve it with emem_memory_token_resolve, and also call verify_evidence with the cell, band "
        "and as_of time of YOUR question, not the handoff's. Use a value only if the resolve succeeds and every check passes; otherwise DECLINE.")


def ledger_total():
    if not LEDGER.exists():
        return 0.0
    return sum(json.loads(l).get("cost_usd") or 0.0 for l in LEDGER.read_text().splitlines() if l.strip())


def append(path, row):
    with open(path, "a") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.write(json.dumps(row, default=str) + "\n")
        fcntl.flock(fh, fcntl.LOCK_UN)


def done_ids():
    if not TRIALS.exists():
        return set()
    rows = [json.loads(l) for l in TRIALS.read_text().splitlines() if l.strip()]
    return {r["trial_id"] for r in rows if not r.get("excluded")}


def plan(block, model, reps, items):
    rows = []
    by = {i["id"]: i for i in items}
    for r in range(1, reps + 1):
        cells = []
        if block == "P":
            cells = [(iid, c) for iid in PILOT_ITEMS for c in IT.ALL_C if c in by[iid]["conds"]]
        elif block == "1":
            for it in items:
                for c in IT.ALL_C:
                    if c in it["conds"]:
                        cells += [(it["id"], c)] * (3 if it["id"] in CONTROLS else 1)
        elif block == "2":
            cells = [(iid, c) for iid in LIVE_ITEMS for c in LIVE_CONDS]
        rnd = random.Random(f"{SEED}-{block}-{model}-{r}")
        rnd.shuffle(cells)
        seen = {}
        for iid, c in cells:
            k = seen[(iid, c)] = seen.get((iid, c), 0) + 1
            rows.append({"trial_id": f"B{block}-{model}-{iid}-{c}-r{r}-{k}", "block": block, "model": model, "item": iid,
                         "cond": c, "rep": r, "k": k})
    return rows


def mcp_for(block, item_id, cond, calllog):
    srv = {"type": "stdio", "command": sys.executable, "args": [str(HERE / "relay_server.py")],
           "env": {"R5_ITEM": item_id, "R5_COND": cond if block != "2" else "E", "R5_CALLLOG": calllog}}
    if block == "2":
        cfg = {"emem": {"type": "http", "url": "https://emem.dev/mcp"}}
        allowed = "mcp__emem__emem_memory_token_resolve,mcp__emem__emem_verify_receipt"
        if cond == "L2":
            cfg["evidence"] = srv
            allowed += ",mcp__evidence__verify_evidence"
        return json.dumps({"mcpServers": cfg}), allowed
    if cond in ("A", "B"):
        return None, None
    return json.dumps({"mcpServers": {"evidence": srv}}), "mcp__evidence__*"


def prompt_for(block, it, cond):
    if block != "2":
        return IT.user_prompt(it, cond)
    base = IT.user_prompt(it, "E0")
    if cond == "L1":
        base += "\n" + (L1_K if it["task"] == "K" else L1_B)
    elif cond == "L2":
        base += "\n" + (L2_K if it["task"] == "K" else L2_B)
    return base


def analyse_transcript(block, it, cond, r, calllog_rows):
    """Tool-use facts for scoring: seen_served, verified_pass, verify calls and their binding, refusals seen."""
    res_by = {x["tool_use_id"]: x for x in r["results"]}
    seen_served = verified_pass = False
    verify_calls, bound_ok, refusals_seen, n_calls = 0, 0, 0, len(r["calls"])
    live_calls = []
    for c in r["calls"]:
        nm = c["name"].split("__")[-1]
        res = res_by.get(c["id"], {})
        txt, err = res.get("text", ""), res.get("is_error", False)
        if nm in ("fetch_evidence", "fetch_record") and not err and "not found" not in txt:
            seen_served = True
        if nm == "search_corpus":
            seen_served = True
        if nm == "verify_evidence":
            verify_calls += 1
            try:
                j = json.loads(txt)
                if j.get("verdict") == "PASS":
                    verified_pass = seen_served = True
                else:
                    refusals_seen += 1
            except Exception:
                refusals_seen += 1
            a = c["input"]
            q = it["q"]
            okb = (a.get("cell", "").strip() == q["cell"] and a.get("band", "").strip() == q["band"])
            if it["task"] == "K":
                okb = okb and a.get("date", "").strip()[:10] == IT.V.date_of(q["tslot"])
            else:
                okb = okb and bool(a.get("as_of"))
            bound_ok += int(okb)
        if nm == "resolve_verified":
            verify_calls += 1
            if err:
                refusals_seen += 1
            else:
                verified_pass = seen_served = True
        if nm == "emem_memory_token_resolve":
            live_calls.append({"tool": nm, "input": c["input"], "is_error": err, "head": txt[:300]})
            if err:
                refusals_seen += 1
            else:
                seen_served = True
        if nm == "emem_verify_receipt":
            live_calls.append({"tool": nm, "input_keys": list((c["input"] or {}).keys()), "is_error": err, "head": txt[:200]})
    return dict(seen_served=seen_served, verified_pass=verified_pass, verify_calls=verify_calls, verify_bound_ok=bound_ok,
                refusals_seen=refusals_seen, n_tool_calls=n_calls, live_calls=live_calls)


def infra_failure(r, needs_mcp):
    if r["exit"] == -9:
        return "timeout"
    if not r["result_text"] and r["exit"] != 0:
        return f"exit {r['exit']} with no output"
    if needs_mcp:
        st = [s.get("status") for s in (r.get("mcp_servers") or [])]
        if not st or any(x != "connected" for x in st):
            return f"mcp not connected {st}"
    if r.get("is_error") and r.get("subtype") not in ("success", "error_max_turns", "error_max_budget_usd"):
        return f"cli error {r.get('subtype')}"
    if r.get("is_error") and "API Error" in (r.get("result_text") or ""):
        return "api error"
    txt = r.get("result_text") or ""
    if ("hit your session limit" in txt or "rate limit" in txt.lower()) and not S.DEC_RE.search(txt):
        return "rate limit: no model output"
    return None


def run_one(t, by, cap):
    it = by[t["item"]]
    calllog = str(RAW / f"{t['trial_id']}.calls.jsonl")
    cfg, allowed = mcp_for(t["block"], it["id"], t["cond"], calllog)
    dis = ["mcp__emem__" + n for n in EMEM_DISALLOW] if t["block"] == "2" else None
    prompt = prompt_for(t["block"], it, t["cond"])
    attempts = []
    for attempt in range(3):
        r = claude_run.run(prompt, IT.system_prompt(it), t["model"], cfg, allowed, disallowed=dis, effort=EFFORT[t["model"]])
        append(LEDGER, {"trial_id": t["trial_id"], "attempt": attempt, "cost_usd": r["cost_usd"] or 0.0, "t": time.time()})
        fail = infra_failure(r, cfg is not None)
        attempts.append(fail)
        if not fail:
            break
        if fail.startswith("rate limit"):
            time.sleep(120)
    calls_rows = [json.loads(l) for l in open(calllog)] if os.path.exists(calllog) else []
    tx = analyse_transcript(t["block"], it, t["cond"], r, calls_rows)
    sc_cond = t["cond"] if t["block"] != "2" else "E"
    sc = S.score(it, sc_cond, r["result_text"], seen_served=tx["seen_served"], verified_pass=tx["verified_pass"])
    mu = r.get("modelUsage") or {}
    u = r.get("usage") or {}
    row = {**t, "task": it["task"], "family": it["family"], "primary": it["primary"], "correct_output": it["correct"],
           "excluded": attempts[-1], "infra_attempts": attempts, **sc, **tx,
           "latency_s": r["wall_s"], "duration_ms": r["duration_ms"], "num_turns": r["num_turns"],
           "cost_usd": r["cost_usd"], "tokens_in": u.get("input_tokens"), "tokens_cache_write": u.get("cache_creation_input_tokens"),
           "tokens_cache_read": u.get("cache_read_input_tokens"), "tokens_out": u.get("output_tokens"),
           "thinking_tokens": (u.get("output_tokens_details") or {}).get("thinking_tokens"),
           "models_used": list(mu.keys()), "tools_offered": r["tools_offered"], "cli_version": r["cli_version"],
           "calls": [{"name": c["name"], "input": c["input"]} for c in r["calls"]],
           "results_head": [{"is_error": x["is_error"], "text": x["text"][:500]} for x in r["results"]],
           "final_text": r["result_text"][-1500:], "subtype": r.get("subtype"), "ts": time.time()}
    append(TRIALS, row)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--block", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--start-rep", type=int, default=1)
    ap.add_argument("--cap", type=float, default=SOFT_CAP)
    ap.add_argument("--shard", default="0/1")
    a = ap.parse_args()
    items = IT.build_items()
    by = {i["id"]: i for i in items}
    rows = [t for t in plan(a.block, a.model, a.reps, items) if t["rep"] >= a.start_rep]
    planfile = HERE / f"plan_B{a.block}_{a.model}.jsonl"
    if not planfile.exists():
        planfile.write_text("".join(json.dumps(t) + "\n" for t in rows))
    si, sn = map(int, a.shard.split("/"))
    rows = [t for n, t in enumerate(rows) if n % sn == si]
    done = done_ids()
    costs = []
    for t in rows:
        if t["trial_id"] in done:
            continue
        spent = ledger_total()
        mean = (sum(costs) / len(costs)) if costs else 0.05
        if spent + 2 * mean > min(a.cap, HARD_CAP):
            print(f"STOP: ledger {spent:.3f} + 2x mean {mean:.4f} would cross cap {a.cap}", flush=True)
            break
        row = run_one(t, by, a.cap)
        costs.append(row["cost_usd"] or 0.0)
        print(f"{t['trial_id']:55} {str(row['decision']):12} fa={row['fa']} vcalls={row['verify_calls']} "
              f"${(row['cost_usd'] or 0):.4f} {row['latency_s']}s excl={row['excluded']} ledger=${ledger_total():.2f}", flush=True)


if __name__ == "__main__":
    main()
