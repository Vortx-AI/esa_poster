#!/usr/bin/env python3
"""genuine_value_source.py: where the genuine value came from when agent B acted on it (added 4 Oct 2026, after a review).

not_acted_split.py splits the complement of false acceptance into "declined" and "acted on the genuine value". This
script asks how B obtained the genuine value in the second group, with score.py's own attribution channel:
  derived  B's own derivation, e.g. NDVI recomputed from the DNs the handoff carries (credited by scoring addendum 1
           when the genuine value differs from every value the relay supplied);
  served   the value the condition's tool returned for the reference: in D the record as the relay serves it
           (fetch_record, no check), in E0, E and E+ the emem record (verified_pass says whether every check passed);
  stated   the value written in the handoff itself, unverified, where the relay left it genuine.
Same trials and scoring as not_acted_split.py (block 1, three Claude models pooled, primary items, controls excluded).
It shows that "used the genuine record" overstated the JSON and opaque-id lanes: no genuine record reaches B in JSON.
    python research/repro/v13/r5/genuine_value_source.py
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
by = {}
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
    if s["fa"] or s["decision"] == "DECLINE" or not s["parsed"]:
        continue
    assert s["acted_value"] == it["genuine"], r["trial_id"]
    d = by.setdefault(r["cond"], {"acted_on_genuine": 0, "by_channel": Counter(), "by_channel_item": {}, "served_verified": 0,
                                 "derived_reasons": []})
    d["acted_on_genuine"] += 1
    d["by_channel"][s["acted_channel"]] += 1
    d["by_channel_item"].setdefault(s["acted_channel"], Counter())[r["item"]] += 1
    if s["acted_channel"] == "derived":   # B's own REASON line, so the kind of derivation can be read, not assumed
        d["derived_reasons"].append({"trial_id": r["trial_id"], "reason": s["reason"]})
    if s["acted_channel"] == "served" and r.get("verified_pass"):
        d["served_verified"] += 1
split = json.loads((HERE / "out" / "not_acted_split.json").read_text())["conditions"]
for cond, d in by.items():
    assert d["acted_on_genuine"] == split[cond]["acted_on_genuine"], cond
res = {"generated_by": "research/repro/v13/r5/genuine_value_source.py",
       "scope": "primary items, three Claude models pooled, block 1 (as out/not_acted_split.json)",
       "channels": {"derived": "B's own derivation (scoring addendum 1)",
                    "served": "the value the condition's tool returned for the reference",
                    "stated": "the value written in the handoff, unverified"},
       "conditions": {c: {"acted_on_genuine": d["acted_on_genuine"], "by_channel": dict(sorted(d["by_channel"].items())),
                          "served_verified": d["served_verified"], "derived_reasons": d["derived_reasons"],
                          "by_channel_item": {k: dict(sorted(v.items())) for k, v in sorted(d["by_channel_item"].items())}}
                      for c, d in sorted(by.items())}}
(HERE / "out" / "genuine_value_source.json").write_text(json.dumps(res, indent=1) + "\n")
for c, d in res["conditions"].items():
    print(c, d["acted_on_genuine"], d["by_channel"], "served and verified:", d["served_verified"])
