#!/usr/bin/env python3
"""not_acted_split.py: what the complement of the pre-registered false-acceptance count contains.

False acceptance (score.py) counts a corrupted trial when agent B acts on a value other than the genuine one. Its
complement therefore mixes outcomes: B declined, B acted on the genuine value (for example after resolving the
reference), or B gave no parsable decision. This script re-scores every primary, pooled-Claude trial with score.py,
exactly as analyze.py does, and writes the split per condition to out/not_acted_split.json. The poster's 300of300
variant prints "did not act on corrupted evidence" and this split; the 0of300 variant prints false acceptance.
    python research/repro/v13/r5/not_acted_split.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import items as IT  # noqa: E402
import score as S  # noqa: E402

ITEMS = {i["id"]: i for i in IT.build_items()}
CLAUDE = ["claude-haiku-4-5-20251001", "claude-sonnet-5-5", "claude-opus-5-5"]
out = {}
for line in open(HERE / "trials.jsonl"):
    if not line.strip():
        continue
    r = json.loads(line)
    if r["block"] != "1" or r.get("excluded") or r["model"] not in CLAUDE:
        continue
    it = ITEMS[r["item"]]
    if not it["primary"] or r["item"] in ("G0", "G0-B"):
        continue
    s = S.score(it, r["cond"], r.get("final_text") or "", seen_served=r.get("seen_served"),
                verified_pass=r.get("verified_pass"))
    c = out.setdefault(r["cond"], Counter())
    c["n"] += 1
    if s["fa"]:
        c["acted_on_corrupted"] += 1
    elif s["decision"] == "DECLINE":
        c["declined"] += 1
    elif not s["parsed"]:
        c["no_parsable_decision"] += 1
    else:
        c["acted_on_genuine"] += 1
res = {"generated_by": "research/repro/v13/r5/not_acted_split.py", "scope": "primary items, three Claude models pooled, block 1",
       "definition": "not acted on = n - acted_on_corrupted = declined + acted_on_genuine + no_parsable_decision",
       "conditions": {}}
for cond in sorted(out):
    c = out[cond]
    d = {k: c.get(k, 0) for k in ("n", "acted_on_corrupted", "declined", "acted_on_genuine", "no_parsable_decision")}
    d["not_acted_on"] = d["n"] - d["acted_on_corrupted"]
    assert d["not_acted_on"] == d["declined"] + d["acted_on_genuine"] + d["no_parsable_decision"]
    res["conditions"][cond] = d
results = json.loads((HERE / "results.json").read_text())
for cond in ("A", "B", "C", "D", "E"):
    fa = results["primary"][cond]["pooled_claude"]["false_accept"]
    assert (fa["k"], fa["n"]) == (res["conditions"][cond]["acted_on_corrupted"], res["conditions"][cond]["n"]), cond
(HERE / "out" / "not_acted_split.json").write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps(res["conditions"], indent=1))
