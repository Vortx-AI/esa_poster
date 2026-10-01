"""STEP 3: tables, Fisher tests, cost/latency/tokens, A prose precision, transcripts."""
import json, os, re, statistics as st, sys
from scipy.stats import fisher_exact
import tiktoken
import common

HERE = os.path.dirname(os.path.abspath(__file__))
enc = tiktoken.get_encoding("cl100k_base")
A = [json.loads(l) for l in open(os.path.join(HERE, "agent_a.jsonl"))]
files = {"qwen2.5-3b-instruct-q4_k_m": "qwen_trials.jsonl", "claude-haiku-4-5": "claude_b_trials.jsonl",
         "qwen2.5-7b-instruct-q4_k_m": "qwen7b_trials.jsonl"}
out = {"agent_a": {}, "b": {}}

# ---- agent A
signed = 0.4708994708994709
nums = [re.findall(r"\d+\.\d+", a["handoff_prose"] or "") for a in A]
prec = []
for a, ns in zip(A, nums):
    ndvi_like = [n for n in ns if 0 < float(n) < 1]
    s = ndvi_like[0] if ndvi_like else None
    prec.append({"i": a["i"], "stated": s, "sig_digits": common.sig_digits(s), "decimals": len(s.split(".")[1]) if s else 0,
                 "agrees": common.exact_quote(s, signed) if s else False,
                 "year_ok": ("2026" in a["handoff_prose"]) and ("2025" not in a["handoff_prose"]),
                 "tile_ok": ("43SFS" in a["handoff_prose"])})
out["agent_a"] = {
    "n": len(A), "models": sorted({m for a in A for m in a["models_used"]}),
    "token_equals_hero": sum(a["token_equals_hero"] for a in A),
    "prose_ge4_sigdig_and_agrees": sum(p["sig_digits"] >= 4 and p["agrees"] for p in prec),
    "prose_sig_digits_distribution": {str(k): sum(p["sig_digits"] == k for p in prec) for k in sorted({p["sig_digits"] for p in prec})},
    "prose_year_ok": sum(p["year_ok"] for p in prec), "prose_tile_mentions_43SFS": sum(p["tile_ok"] for p in prec),
    "cost_usd_total": round(sum(a["cost_usd"] for a in A), 4), "cost_usd_mean": round(st.mean(a["cost_usd"] for a in A), 4),
    "wall_s_mean": round(st.mean(a["wall_s"] for a in A), 2), "wall_s_range": [min(a["wall_s"] for a in A), max(a["wall_s"] for a in A)],
    "tool_calls_mean": round(st.mean(len(a["calls"]) for a in A), 2),
    "tool_sequences": [[c["name"].replace("mcp__emem__", "") for c in a["calls"]] for a in A],
    "first_call_error_or_wrong_cell": [a["i"] for a in A if a["results"] and a["results"][0]["is_error"]],
    "cl100k_token": len(enc.encode(A[0]["handoff_token"])), "cl100k_prose_mean": round(st.mean(len(enc.encode(a["handoff_prose"])) for a in A), 1),
    "prose_detail": prec,
}


def pct(k, n):
    return f"{k}/{n} ({100*k/n:.0f}%)" if n else "0/0"


for mname, fn in files.items():
    path = os.path.join(HERE, fn)
    if not os.path.exists(path):
        continue
    R = [json.loads(l) for l in open(path)]
    arms = {}
    for arm in ("T", "P", "R", "F"):
        rs = [r for r in R if r["arm"] == arm]
        if not rs:
            continue
        n = len(rs)
        own_consistent = 0
        for r in rs:
            try:
                own_consistent += r["decision"] == common.truth(float(r["ndvi_str"]))
            except Exception:
                pass
        row = {"n": n, "resolve_called": sum(r["resolve_called"] for r in rs), "cid_equals_A": sum(r["cid_equals_A"] for r in rs),
               "harness_rehash_ok": sum(bool(r["harness_rehash_ok"]) for r in rs), "receipt_valid": sum(bool(r["receipt_ok"]) for r in rs),
               "exact_quote": sum(r["exact_quote"] for r in rs), "decision_correct": sum(r["correct"] for r in rs),
               "decline": sum(r["decision"] == "DECLINE" for r in rs), "no_decision_line": sum(r["decision"] is None for r in rs),
               "decision_consistent_with_own_stated_value": own_consistent,
               "forged_detected": sum(r["forged_detected"] for r in rs) if arm == "F" else None,
               "decisions": {d: sum(r["decision"] == d for r in rs) for d in ("IRRIGATE", "HOLD", "DECLINE", None)},
               "cl100k_handoff_mean": round(st.mean(len(enc.encode(r["handoff"])) for r in rs), 1)}
        if "cost_usd" in rs[0]:
            row["cost_usd_mean"] = round(st.mean(r["cost_usd"] for r in rs), 5); row["wall_s_mean"] = round(st.mean(r["wall_s"] for r in rs), 2)
            row["any_emem_call"] = sum(r["any_emem_call"] for r in rs)
            row["tools_used"] = sorted({c["name"].replace("mcp__emem__", "") for r in rs for c in r["calls"]})
            row["input_tokens_mean"] = round(st.mean((r["usage"] or {}).get("input_tokens", 0) + (r["usage"] or {}).get("cache_read_input_tokens", 0)
                                                     + (r["usage"] or {}).get("cache_creation_input_tokens", 0) for r in rs), 0)
        else:
            row["cost_usd_mean"] = 0.0; row["wall_s_mean"] = round(st.mean(r["wall_s"] for r in rs), 2)
            row["gen_tokens_mean"] = round(st.mean(r["gen_tokens"] for r in rs), 1); row["prompt_tokens_mean"] = round(st.mean(r["prompt_tokens"] for r in rs), 1)
            row["decode_tok_s"] = round(sum(r["gen_tokens"] for r in rs) / sum(r["llm_s"] for r in rs), 2)
            forms = [tc.get("token_form") for r in rs for tc in r["tool_calls"]]
            row["token_forms_passed"] = {f: forms.count(f) for f in set(forms)}
            row["resolve_isError_any"] = sum(any(r["tool_isError"]) for r in rs)
            row["server_degraded_any"] = sum(any(tc.get("server_degraded") for tc in r["tool_calls"]) for r in rs)
        arms[arm] = row
    tests = {}
    if "T" in arms and "P" in arms:
        t, p = arms["T"], arms["P"]
        tab = [[t["decision_correct"], t["n"] - t["decision_correct"]], [p["decision_correct"], p["n"] - p["decision_correct"]]]
        tests["T_vs_P_primary"] = {"table": tab, "p_one_sided": fisher_exact(tab, alternative="greater")[1]}
    if "T" in arms and "R" in arms:
        t, r = arms["T"], arms["R"]
        tab = [[t["decision_correct"], t["n"] - t["decision_correct"]], [r["decision_correct"], r["n"] - r["decision_correct"]]]
        tests["T_vs_R_exploratory"] = {"table": tab, "p_one_sided": fisher_exact(tab, alternative="greater")[1]}
    out["b"][mname] = {"arms": arms, "tests": tests, "models_used": sorted({m for r in R for m in r.get("models_used", [mname])})}

json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1, default=str)
print(json.dumps({k: v for k, v in out["agent_a"].items() if k not in ("prose_detail", "tool_sequences")}, indent=1))
for m, v in out["b"].items():
    print("\n==", m, v["models_used"])
    cols = ["n", "resolve_called", "cid_equals_A", "harness_rehash_ok", "receipt_valid", "exact_quote", "decision_correct", "decline",
            "decision_consistent_with_own_stated_value", "forged_detected"]
    print("arm | " + " | ".join(cols[1:]))
    for arm, row in v["arms"].items():
        print(arm, "|", " | ".join(pct(row[c], row["n"]) if row[c] is not None else "-" for c in cols[1:]),
              "| cost", row["cost_usd_mean"], "| wall", row["wall_s_mean"], "| cl100k", row["cl100k_handoff_mean"],
              "| extra", {k: row[k] for k in row if k in ("decode_tok_s", "token_forms_passed", "tools_used", "server_degraded_any", "decisions", "input_tokens_mean", "gen_tokens_mean", "prompt_tokens_mean")})
    print("tests", json.dumps(v["tests"]))
