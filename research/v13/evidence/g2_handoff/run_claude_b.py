"""STEP 2b: agent B within family = claude -p --model haiku with the same emem plugin config and isolation as agent A."""
import json, os, sys
import common
from claude_run import run

HERE = os.path.dirname(os.path.abspath(__file__))
A = [json.loads(l) for l in open(os.path.join(HERE, "agent_a.jsonl"))]
OUTD = os.path.join(HERE, "raw", "agent_b_claude"); os.makedirs(OUTD, exist_ok=True)
model = sys.argv[1]; out_path = sys.argv[2]
plan = sys.argv[3] if len(sys.argv) > 3 else "T10,P10,F5,R5"
counts = {x[0]: int(x[1:]) for x in plan.split(",")}
gt = json.load(open(os.path.join(HERE, "raw", "ground_truth.json")))


def handoff(arm, i):
    a = A[i % len(A)]
    return {"T": (a["handoff_token"], a["i"]), "P": (a["handoff_prose"], a["i"]),
            "R": (a["handoff_prose"].replace("0.4708994708994709", "0.47"), a["i"]), "F": (common.FORGED, None)}[arm]


order = [(arm, i) for i in range(max(counts.values())) for arm in ("T", "P", "R", "F") if i < counts.get(arm, 0)]
with open(out_path, "a") as fo:
    for arm, i in order:
        h, a_i = handoff(arm, i)
        prompt = common.B_TEMPLATE.format(handoff=h)
        r = run(prompt, model, f"b_{arm}{i:02d}", OUTD)
        full = r.pop("_full_results")
        a_tok = A[a_i]["handoff_token"] if a_i is not None else common.HERO
        signed = gt[a_tok]["signed_value"] if a_tok in gt else common.harness_verify(a_tok)["signed_value"]
        dec, nd = common.parse_final(r["result_text"])
        # harness-side independent verification of every resolve call B made
        ver = []
        by_id = {x["tool_use_id"]: x for x in full}
        for c in r["calls"]:
            if c["name"].endswith("emem_memory_token_resolve"):
                res = by_id.get(c["id"], {})
                tok = c["input"].get("token", "")
                rec = None
                try:
                    body = json.loads(res.get("text", ""))
                    rec = body.get("receipt")
                    served_cid = body.get("fact_cid")
                except Exception:
                    served_cid = None
                hv = common.harness_verify(tok, rec) if common.TOK_RE.fullmatch(tok or "") and not res.get("is_error") else {}
                ver.append({"token": tok, "is_error": res.get("is_error"), "served_cid": served_cid, "harness": hv, "text_head": res.get("text", "")[:300]})
        out = {"model_requested": model, "models_used": r["models_used"], "arm": arm, "i": i, "a_run": a_i, "handoff": h,
               "decision": dec, "ndvi_str": nd, "truth": common.truth(signed), "signed_value": signed,
               "calls": r["calls"], "resolve_checks": ver, "result_text": r["result_text"], "cost_usd": r["cost_usd"],
               "wall_s": r["wall_s"], "duration_ms": r["duration_ms"], "num_turns": r["num_turns"], "usage": r["usage"], "raw": r["raw"]}
        out["correct"] = dec == out["truth"]
        out["exact_quote"] = common.exact_quote(nd, signed)
        out["resolve_called"] = len(ver) > 0
        out["any_emem_call"] = len(r["calls"]) > 0
        out["cid_equals_A"] = any(v["served_cid"] == a_tok.split(":")[-1] and not v["is_error"] for v in ver)
        out["harness_rehash_ok"] = any(v["harness"].get("rehash_ok") for v in ver)
        out["receipt_ok"] = any(v["harness"].get("receipt_sig_ok") and v["harness"].get("receipt_binds") for v in ver)
        out["forged_detected"] = (arm == "F") and dec not in ("IRRIGATE", "HOLD")
        fo.write(json.dumps(out) + "\n"); fo.flush()
        print(arm, i, r["models_used"], dec, nd, out["truth"], out["correct"], [c["name"][11:] for c in r["calls"]], r["cost_usd"], r["wall_s"], flush=True)
