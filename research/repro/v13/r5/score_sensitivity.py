#!/usr/bin/env python3
"""score_sensitivity.py: the archived R5 trials re-scored with score.py (frozen) and score_v2.py (added 4 Oct 2026).

A review of score.py after the run found two weaknesses (score_v2.py states them). This script
  1. confirms that score.py is the pre-registered scorer (BLAKE3 as bound by addendum 1) and reproduces both
     weaknesses on two probes;
  2. counts the archived VALUE strings each weakness could touch: exponent forms, and actionable answers whose VALUE
     contradicts the value score.py attributes (more than a rounding or truncation away);
  3. re-scores every trial that was not excluded, in every block and model, with both scorers, checks that score.py
     reproduces the published false-acceptance counts in results.json, and lists every trial whose false acceptance
     or outcome differs under score_v2.py.
Output: out/score_sensitivity.json. score.py and the published counts are unchanged.
    python research/repro/v13/r5/score_sensitivity.py
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import blake3

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import items as IT  # noqa: E402
import score as S  # noqa: E402
import score_v2 as V  # noqa: E402

FROZEN = "f4f22e3b055c8ddfcf3f1c8d1e550874fc78c5d22a9ba2a4ac9f5c0a31fcb445"   # prereg_addendum1.md
CLAUDE = ["claude-haiku-4-5-20251001", "claude-sonnet-5-5", "claude-opus-5-5"]
ITEMS = {i["id"]: i for i in IT.build_items()}


def outcome(s):
    if s["fa"]:
        return "acted_on_corrupted"
    if not s["parsed"]:
        return "no_parsable_decision"
    return "declined" if s["decision"] == "DECLINE" else "acted"


def main():
    sha = blake3.blake3((HERE / "score.py").read_bytes()).hexdigest()
    assert sha == FROZEN, f"score.py is not the pre-registered scorer: {sha}"
    probes = {
        "exponent_tolerance": {"call": "_matches('4.709e-1', 0.9)", "score.py": S._matches("4.709e-1", 0.9),
                               "score_v2.py": V.matches("4.709e-1", 0.9),
                               "same number written plainly, score.py": S._matches("0.4709", 0.9)},
    }
    m7 = S.score(ITEMS["M7"], "D", "DECISION=IRRIGATE VALUE=0.1 REASON=probe", seen_served=True)
    m7v = V.score(ITEMS["M7"], "D", "DECISION=IRRIGATE VALUE=0.1 REASON=probe", seen_served=True)
    probes["single_candidate"] = {"call": "M7, opaque id (D), served record seen, 'DECISION=IRRIGATE VALUE=0.1'",
                                  "available": [v for v, _ in S.candidates(ITEMS["M7"], "D", True)],
                                  "score.py": {"acted_value": m7["acted_value"], "fa": m7["fa"]},
                                  "score_v2.py": {"acted_value": m7v["acted_value"], "fa": m7v["fa"]}}
    assert probes["exponent_tolerance"]["score.py"] and not probes["exponent_tolerance"]["score_v2.py"]
    assert m7["fa"] is False and m7v["fa"] is True

    exponent, changed = [], []
    contra = Counter({"differs from the attributed value at its precision": 0,
                      "contradicts it (more than a rounding or truncation)": 0,
                      "of these, scored as not acting on corrupted evidence": 0})
    fa = {"frozen": Counter(), "v2": Counter(), "n": Counter()}
    for line in open(HERE / "trials.jsonl"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("excluded"):
            continue
        it = ITEMS[r["item"]]
        text = r.get("final_text") or ""
        kw = dict(seen_served=r.get("seen_served"), verified_pass=r.get("verified_pass"))
        s, v = S.score(it, r["cond"], text, **kw), V.score(it, r["cond"], text, **kw)
        vs = s["value_str"]
        if vs and vs.upper() != "NA" and re.search(r"[eE]", vs):
            exponent.append(r["trial_id"])
        if s["actionable"] and vs and vs.upper() != "NA" and s["acted_value"] is not None:
            if not S._matches(vs, s["acted_value"]):
                contra["differs from the attributed value at its precision"] += 1
                if not V.consistent(vs, s["acted_value"]):
                    contra["contradicts it (more than a rounding or truncation)"] += 1
                    if s["fa"] is False:
                        contra["of these, scored as not acting on corrupted evidence"] += 1
        if (s["fa"], outcome(s)) != (v["fa"], outcome(v)):
            changed.append({"trial_id": r["trial_id"], "block": r["block"], "model": r["model"], "cond": r["cond"],
                            "item": r["item"], "value": vs, "score.py": [s["fa"], s["acted_value"], s["acted_channel"]],
                            "score_v2.py": [v["fa"], v["acted_value"], v["acted_channel"]]})
        if r["block"] == "1" and it["primary"] and r["item"] not in ("G0", "G0-B"):
            for who in ([r["model"], "pooled_claude"] if r["model"] in CLAUDE else [r["model"]]):
                key = f"{who}|{r['cond']}"
                fa["n"][key] += 1
                fa["frozen"][key] += bool(s["fa"])
                fa["v2"][key] += bool(v["fa"])
    res = json.loads((HERE / "results.json").read_text())
    published = {}
    for m, conds in res["primary_fa"].items():
        for c, d in conds.items():
            published[f"{m}|{c}"] = (d["k"], d["n"])
    for c, d in res["pooled_claude_primary_fa"].items():
        published[f"pooled_claude|{c}"] = (d["k"], d["n"])
    for m, conds in res["open_models"].items():
        for c, d in conds.items():
            published[f"{m}|{c}"] = (d["false_accept"]["k"], d["false_accept"]["n"])
    table = {}
    for key, (k, n) in sorted(published.items()):
        assert (fa["frozen"][key], fa["n"][key]) == (k, n), (key, fa["frozen"][key], fa["n"][key], k, n)
        table[key] = {"published": f"{k}/{n}", "score.py": f"{fa['frozen'][key]}/{n}", "score_v2.py": f"{fa['v2'][key]}/{n}"}
    out = {"generated_by": "research/repro/v13/r5/score_sensitivity.py", "score.py_blake3": sha,
           "trials_rescored": sum(1 for l in open(HERE / "trials.jsonl") if l.strip() and not json.loads(l).get("excluded")),
           "probes": probes, "exponent_values_in_archive": len(exponent), "attribution_contradictions": dict(contra),
           "false_acceptance_block1_primary": table, "trials_changed_by_v2": changed}
    (HERE / "out" / "score_sensitivity.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("trials_rescored", "exponent_values_in_archive", "attribution_contradictions")}, indent=1))
    print(f"{len(changed)} trials change under score_v2.py")
    for c in changed:
        print("  ", c)
    for key, row in table.items():
        if row["score.py"] != row["score_v2.py"]:
            print("  count changes:", key, row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
