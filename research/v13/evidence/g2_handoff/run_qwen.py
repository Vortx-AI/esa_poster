"""Run B-open (Qwen) arms T, P, F (+ exploratory R) against agent A's logged handoffs."""
import json, os, sys, time
import common, qwen_b

HERE = os.path.dirname(os.path.abspath(__file__))
A = [json.loads(l) for l in open(os.path.join(HERE, "agent_a.jsonl"))]
model_path = sys.argv[1]
out_path = sys.argv[2]
plan = sys.argv[3] if len(sys.argv) > 3 else "T20,P20,F5,R10"
counts = {x[0]: int(x[1:]) for x in plan.split(",")}
SEED0 = {"T": 1000, "P": 2000, "F": 3000, "R": 4000}


def handoff(arm, i):
    a = A[i % len(A)]
    if arm == "T":
        return a["handoff_token"], a["i"]
    if arm == "P":
        return a["handoff_prose"], a["i"]
    if arm == "R":
        return a["handoff_prose"].replace("0.4708994708994709", "0.47"), a["i"]
    if arm == "F":
        return common.FORGED, None


# ground truth: re-hash A's token's fact once per distinct token (independent code)
gt = {}
for a in A:
    if a["handoff_token"] not in gt:
        gt[a["handoff_token"]] = common.harness_verify(a["handoff_token"])
json.dump(gt, open(os.path.join(HERE, "raw", "ground_truth.json"), "w"), indent=1)

llm = qwen_b.load(model_path)
order = []
for i in range(max(counts.values())):
    for arm in ("T", "P", "R", "F"):
        if i < counts.get(arm, 0):
            order.append((arm, i))
with open(out_path, "a") as fo:
    for arm, i in order:
        h, a_i = handoff(arm, i)
        seed = SEED0[arm] + i
        t0 = time.time()
        tr = qwen_b.trial(llm, h, seed)
        dec, nd = common.parse_final(tr["final"])
        a_tok = A[a_i]["handoff_token"] if a_i is not None else common.HERO
        g = gt.get(a_tok) or common.harness_verify(a_tok)
        signed = g["signed_value"]
        rec = {"model": os.path.basename(model_path), "arm": arm, "i": i, "a_run": a_i, "seed": seed, "handoff": h,
               "decision": dec, "ndvi_str": nd, "truth": common.truth(signed), "signed_value": signed,
               "wall_s": round(time.time() - t0, 2), **{k: tr[k] for k in ("tool_calls", "final", "gen_tokens", "prompt_tokens", "llm_s", "messages")}}
        rec["correct"] = dec == rec["truth"]
        rec["exact_quote"] = common.exact_quote(nd, signed)
        rec["resolve_called"] = len(tr["tool_calls"]) > 0
        rec["cid_equals_A"] = any(tc["trimmed"].get("fact_cid") == a_tok.split(":")[-1] for tc in tr["tool_calls"])
        rec["harness_rehash_ok"] = any(tc.get("harness", {}).get("rehash_ok") for tc in tr["tool_calls"] if not tc["trimmed"].get("isError"))
        rec["receipt_ok"] = any(tc.get("harness", {}).get("receipt_sig_ok") and tc["harness"].get("receipt_binds") for tc in tr["tool_calls"])
        rec["tool_isError"] = [tc["trimmed"].get("isError") for tc in tr["tool_calls"]]
        rec["forged_detected"] = (arm == "F") and dec not in ("IRRIGATE", "HOLD")
        fo.write(json.dumps(rec) + "\n"); fo.flush()
        print(arm, i, seed, dec, nd, rec["truth"], rec["correct"], "calls", len(tr["tool_calls"]), rec["tool_isError"], rec["wall_s"], flush=True)
