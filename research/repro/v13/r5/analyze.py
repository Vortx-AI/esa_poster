#!/usr/bin/env python3
"""analyze.py: R5 analysis per prereg §7 (+ addendum 1). Re-scores every trial from its stored transcript with score.py,
then writes results.json, results_tables.md (generated tables) and fa_matrix.csv (figure-ready)."""
import csv, json, math, random
from collections import defaultdict
from pathlib import Path

from scipy.stats import fisher_exact

import items as IT
import score as S

HERE = Path(__file__).resolve().parent
ITEMS = {i["id"]: i for i in IT.build_items()}
CONDS = IT.ALL_C
LIVE = ["L0", "L1", "L2"]
CLAUDE = ["claude-haiku-4-5-20251001", "claude-sonnet-5-5", "claude-opus-5-5"]
SHORT = {"claude-haiku-4-5-20251001": "haiku", "claude-sonnet-5-5": "sonnet", "claude-opus-5-5": "opus"}
DESIGN_SET = {f"M{i}" for i in range(1, 17)} | {"M5b", "M2-B", "M18", "M20"}


def wilson(k, n, z=1.959964):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0, c - h), 4), round(min(1, c + h), 4)]


def rate(rows, key):
    xs = [r[key] for r in rows if r[key] is not None]
    k, n = sum(bool(x) for x in xs), len(xs)
    return {"k": k, "n": n, "rate": round(k / n, 4) if n else None, "wilson95": wilson(k, n)}


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, m, run = [None] * len(ps), len(ps), 0
    for r, i in enumerate(order):
        run = max(run, min(1, (m - r) * ps[i]))
        adj[i] = run
    return adj


def load():
    rows = [json.loads(l) for l in open(HERE / "trials.jsonl") if l.strip()]
    out = []
    for r in rows:
        if r["block"] == "P" or r.get("excluded"):
            continue
        it = ITEMS[r["item"]]
        cond = r["cond"] if r["block"] == "1" else "E"
        txt = r.get("final_text") or ""
        new = S.score(it, cond, txt, seen_served=r.get("seen_served"), verified_pass=r.get("verified_pass"))
        orig = S.score(it, cond, txt, seen_served=r.get("seen_served"), verified_pass=r.get("verified_pass"), original_rule=True)
        r.update({k: new[k] for k in ("decision", "value_str", "actionable", "acted_value", "acted_channel", "fa",
                                      "correct_refusal", "false_refusal", "correct", "harm", "parsed")})
        r["fa_original_rule"] = orig["fa"]
        r["fa_missing_as_accept"] = (new["fa"] or (not new["parsed"])) if new["fa"] is not None else None
        r["in_primary"] = it["primary"] and r["item"] not in ("G0", "G0-B")
        r["in_design_set"] = r["item"] in DESIGN_SET
        r["obeyed_refusal"] = (not r["actionable"]) if (r.get("refusals_seen") or 0) > 0 else None
        out.append(r)
    excluded = [r for r in rows if r["block"] != "P" and r.get("excluded")]
    return out, excluded, rows


def bootstrap(rows, B=10000, seed=7):
    by = defaultdict(list)
    for r in rows:
        by[r["item"]].append(bool(r["fa"]))
    its = sorted(by)
    if not its:
        return [None, None]
    rnd = random.Random(seed)
    vals = []
    for _ in range(B):
        s = [rnd.choice(its) for _ in its]
        k = sum(sum(by[i]) for i in s)
        n = sum(len(by[i]) for i in s)
        vals.append(k / n)
    vals.sort()
    return [round(vals[int(0.025 * B)], 4), round(vals[int(0.975 * B) - 1], 4)]


def main():
    rows, excluded, allrows = load()
    models = sorted({r["model"] for r in rows}, key=lambda m: (m not in CLAUDE, CLAUDE.index(m) if m in CLAUDE else 0, m))
    b1 = [r for r in rows if r["block"] == "1"]
    b2 = [r for r in rows if r["block"] == "2"]
    ceil = json.loads((HERE / "out" / "ceiling_v13.json").read_text())
    ceil_by = {(c["item"], c["cond"]): c for c in ceil["cells"]}
    res = {"generated_by": "research/repro/v13/r5/analyze.py", "n_trials_scored": len(rows), "n_excluded": len(excluded),
           "excluded": [{"trial_id": r["trial_id"], "why": r.get("excluded")} for r in excluded],
           "n_pilot": sum(1 for r in allrows if r["block"] == "P"), "models": models}
    # ---- primary FA per model x condition
    prim, tests = {}, {}
    for m in models:
        prim[m] = {}
        for c in CONDS:
            rr = [r for r in b1 if r["model"] == m and r["cond"] == c and r["in_primary"]]
            if rr:
                prim[m][c] = {**rate(rr, "fa"), "fa_original_rule": rate(rr, "fa_original_rule"),
                              "fa_missing_as_accept": rate(rr, "fa_missing_as_accept"),
                              "fa_design_set": rate([r for r in rr if r["in_design_set"]], "fa"),
                              "correct_refusal": rate(rr, "correct_refusal"), "harm": rate(rr, "harm")}
        if m in CLAUDE and "E" in prim[m]:
            ps, labels = [], []
            e = prim[m]["E"]
            for x in ("A", "B", "C", "D"):
                if x in prim[m]:
                    a = prim[m][x]
                    _, p = fisher_exact([[e["k"], e["n"] - e["k"]], [a["k"], a["n"] - a["k"]]], alternative="less")
                    ps.append(p)
                    labels.append(x)
            adj = holm(ps)
            tests[m] = {f"E<{x}": {"p_one_sided": float(f"{p:.3g}"), "p_holm": float(f"{q:.3g}")} for x, p, q in zip(labels, ps, adj)}
            for lab, (a, b) in {"X1_E0_vs_E": ("E0", "E"), "X2_E_vs_E+": ("E", "E+")}.items():
                if a in prim[m] and b in prim[m]:
                    A_, B_ = prim[m][a], prim[m][b]
                    _, p = fisher_exact([[A_["k"], A_["n"] - A_["k"]], [B_["k"], B_["n"] - B_["k"]]])
                    tests[m][lab] = {"p_two_sided": float(f"{p:.3g}"), "exploratory": True}
    res["primary_fa"] = prim
    res["tests"] = tests
    # pooled over Claude models
    pooled = {}
    for c in CONDS:
        rr = [r for r in b1 if r["model"] in CLAUDE and r["cond"] == c and r["in_primary"]]
        if rr:
            pooled[c] = {**rate(rr, "fa"), "cluster_bootstrap95_items": bootstrap(rr), "fa_original_rule": rate(rr, "fa_original_rule")}
    res["pooled_claude_primary_fa"] = pooled
    res["ceiling_primary_fa"] = {c: rate([{"fa": ceil_by[(i, c)]["fa"]} for i in ITEMS if (i, c) in ceil_by and ITEMS[i]["primary"]
                                          and i not in ("G0", "G0-B")], "fa") for c in CONDS}
    # ---- decision accuracy (all items incl. controls) and false refusal
    acc = {}
    for m in models:
        acc[m] = {}
        for c in CONDS:
            rr = [r for r in b1 if r["model"] == m and r["cond"] == c]
            if rr:
                acc[m][c] = {"decision_accuracy_all": rate(rr, "correct"),
                             "decision_accuracy_controls": rate([r for r in rr if r["item"] in ("G0", "G0-B")], "correct"),
                             "false_refusal_controls": rate([r for r in rr if r["item"] in ("G0", "G0-B")], "false_refusal"),
                             "unparsed": sum(1 for r in rr if not r["parsed"])}
    res["decision_accuracy"] = acc
    # ---- S5 verification behaviour, S6 refusal obedience
    beh = {}
    for m in models:
        beh[m] = {}
        for c in ("D", "E0", "E", "E+"):
            rr = [r for r in b1 if r["model"] == m and r["cond"] == c]
            if not rr:
                continue
            v = [r for r in rr if (r.get("verify_calls") or 0) > 0]
            beh[m][c] = {"n": len(rr), "verify_called": len(v), "verify_called_rate": round(len(v) / len(rr), 4),
                         "verify_bound_to_question": (sum(1 for r in v if (r.get("verify_bound_ok") or 0) > 0)
                                                      if c != "E+" else "n/a (harness binds the question)"),
                         "tool_called_any": sum(1 for r in rr if (r.get("n_tool_calls") or 0) > 0),
                         "refusal_seen": sum(1 for r in rr if (r.get("refusals_seen") or 0) > 0),
                         "acted_after_refusal": sum(1 for r in rr if (r.get("refusals_seen") or 0) > 0 and r["actionable"])}
    res["verification_behaviour"] = beh
    # ---- per item x condition x model cells (+ ceiling)
    cells = []
    for m in models:
        for iid, it in ITEMS.items():
            for c in CONDS:
                rr = [r for r in b1 if r["model"] == m and r["cond"] == c and r["item"] == iid]
                if not rr:
                    continue
                key = "fa" if iid not in ("G0", "G0-B") else "correct"
                cells.append({"model": m, "item": iid, "family": it["family"], "cond": c, "metric": "fa" if key == "fa" else "correct",
                              **rate(rr, key), "decisions": dict(sorted({d: sum(1 for r in rr if r["decision"] == d)
                                                                         for d in {r["decision"] for r in rr}}.items(), key=str)),
                              "ceiling_fa": (ceil_by.get((iid, c)) or {}).get("fa")})
    res["cells"] = cells
    # ---- families (pooled Claude)
    fam = defaultdict(dict)
    for c in CONDS:
        for f in sorted({it["family"] for it in ITEMS.values()}):
            rr = [r for r in b1 if r["model"] in CLAUDE and r["cond"] == c and ITEMS[r["item"]]["family"] == f and r["fa"] is not None]
            if rr:
                fam[f][c] = rate(rr, "fa")
    res["families_pooled_claude"] = fam
    # ---- H2, H3, X3
    def sub(items, conds, block=b1, mods=CLAUDE):
        return {c: rate([r for r in block if r["model"] in mods and r["cond"] == c and r["item"] in items], "fa") for c in conds}
    res["H2"] = {"M15_block1": sub({"M15"}, CONDS), "M15r_block1": sub({"M15r"}, CONDS),
                 "M15r_block2": sub({"M15r"}, LIVE, b2)}
    l1 = res["H2"]["M15r_block2"].get("L1", {})
    l2 = res["H2"]["M15r_block2"].get("L2", {})
    if l1.get("n") and l2.get("n"):
        _, p = fisher_exact([[l2["k"], l2["n"] - l2["k"]], [l1["k"], l1["n"] - l1["k"]]], alternative="less")
        res["H2"]["M15r_L2_lt_L1_p_one_sided"] = float(f"{p:.3g}")
    res["H3"] = {"M5b": sub({"M5b"}, CONDS), "M20": sub({"M20"}, CONDS),
                 "G0-B_accuracy": {c: rate([r for r in b1 if r["model"] in CLAUDE and r["cond"] == c and r["item"] == "G0-B"], "correct")
                                   for c in CONDS}}
    res["X3_M22"] = {m: sub({"M22"}, ["E0", "E", "E+"], mods=[m]) for m in models}
    # ---- Block 2
    b2c = {}
    for m in models:
        for c in LIVE:
            for iid in sorted({r["item"] for r in b2}):
                rr = [r for r in b2 if r["model"] == m and r["cond"] == c and r["item"] == iid]
                if rr:
                    b2c.setdefault(m, {}).setdefault(c, {})[iid] = {
                        "n": len(rr), "decisions": {d: sum(1 for r in rr if r["decision"] == d) for d in {r["decision"] for r in rr}},
                        "fa": rate(rr, "fa") if iid not in ("G0", "G0-B") else None, "correct": rate(rr, "correct")}
    res["block2"] = b2c
    res["block2_pooled"] = {c: {"fa_inscope": rate([r for r in b2 if r["cond"] == c and r["item"] not in ("G0", "G0-B")], "fa"),
                                "control_correct": rate([r for r in b2 if r["cond"] == c and r["item"] in ("G0", "G0-B")], "correct"),
                                "live_resolve_calls": sum(sum(1 for x in r.get("live_calls") or [] if x["tool"] == "emem_memory_token_resolve")
                                                          for r in b2 if r["cond"] == c)}
                            for c in LIVE}
    # ---- overheads
    ov = {}
    for m in models:
        for c in CONDS:
            rr = [r for r in b1 if r["model"] == m and r["cond"] == c]
            if not rr:
                continue
            def med(k):
                xs = sorted(r[k] for r in rr if r.get(k) is not None)
                return xs[len(xs) // 2] if xs else None
            ncor = sum(1 for r in rr if r["correct"])
            cost = sum(r.get("cost_usd") or 0 for r in rr)
            ov.setdefault(m, {})[c] = {"median_latency_s": med("latency_s"), "median_tokens_in": med("tokens_in"),
                                       "median_tokens_out": med("tokens_out"), "median_cache_write": med("tokens_cache_write"),
                                       "mean_cost_usd": round(cost / len(rr), 5), "cost_per_correct_decision_usd":
                                       round(cost / ncor, 5) if ncor else None, "n": len(rr)}
    res["overheads"] = ov
    res["total_cost_usd_all_blocks"] = round(sum(json.loads(l)["cost_usd"] or 0 for l in open(HERE / "ledger.jsonl")), 4)
    res["n_by_model_block"] = {f"{m}|B{b}": sum(1 for r in rows if r["model"] == m and r["block"] == b) for m in models for b in ("1", "2")}
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=str))
    # ---- matrix CSV: rows item, columns cond x model; cell = FA rate (controls: decision accuracy, marked)
    with open(HERE / "fa_matrix.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        cols = [(c, m) for c in CONDS for m in models]
        w.writerow(["item", "family", "metric", "ceiling_E"] + [f"{c}|{SHORT.get(m, m)}" for c, m in cols])
        cb = {(x["model"], x["item"], x["cond"]): x for x in cells}
        for iid, it in ITEMS.items():
            metric = "false_accept_rate" if iid not in ("G0", "G0-B") else "decision_accuracy (control)"
            row = [iid, it["family"], metric, (ceil_by.get((iid, "E")) or {}).get("fa")]
            for c, m in cols:
                x = cb.get((m, iid, c))
                row.append("" if not x else f"{x['rate']} ({x['k']}/{x['n']})")
            w.writerow(row)
    # ---- tables md
    L = ["# R5 generated tables", "", "Primary false acceptance (in-scope items; k/n, Wilson 95 %)", "",
         "| model | " + " | ".join(CONDS) + " |", "|---" * (len(CONDS) + 1) + "|"]
    for m in models:
        L.append(f"| {SHORT.get(m, m)} | " + " | ".join(
            (f"{prim[m][c]['k']}/{prim[m][c]['n']} ({100*prim[m][c]['rate']:.0f} %, {100*prim[m][c]['wilson95'][0]:.0f}-{100*prim[m][c]['wilson95'][1]:.0f})"
             if c in prim[m] else "-") for c in CONDS) + " |")
    L.append("| pooled Claude | " + " | ".join(
        (f"{pooled[c]['k']}/{pooled[c]['n']} ({100*pooled[c]['rate']:.1f} %, {100*pooled[c]['wilson95'][0]:.1f}-{100*pooled[c]['wilson95'][1]:.1f})"
         if c in pooled else "-") for c in CONDS) + " |")
    L.append("| deterministic ceiling | " + " | ".join(f"{res['ceiling_primary_fa'][c]['k']}/{res['ceiling_primary_fa'][c]['n']}" for c in CONDS) + " |")
    L += ["", "Decision accuracy, all items incl. controls (k/n)", "", "| model | " + " | ".join(CONDS) + " |", "|---" * (len(CONDS) + 1) + "|"]
    for m in models:
        L.append(f"| {SHORT.get(m, m)} | " + " | ".join(
            (f"{acc[m][c]['decision_accuracy_all']['k']}/{acc[m][c]['decision_accuracy_all']['n']}" if c in acc[m] else "-") for c in CONDS) + " |")
    L += ["", "False refusal on controls G0, G0-B (k/n)", "", "| model | " + " | ".join(CONDS) + " |", "|---" * (len(CONDS) + 1) + "|"]
    for m in models:
        L.append(f"| {SHORT.get(m, m)} | " + " | ".join(
            (f"{acc[m][c]['false_refusal_controls']['k']}/{acc[m][c]['false_refusal_controls']['n']}" if c in acc[m] else "-") for c in CONDS) + " |")
    L += ["", "Tests (Claude, per model)", "", "```", json.dumps(tests, indent=1), "```"]
    (HERE / "results_tables.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
