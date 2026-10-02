#!/usr/bin/env python3
"""ceiling.py: the deterministic ceiling (R1-v13) for every (item, condition) cell, plus unit tests tying the R5 relay
states back to R1's outcomes. Writes out/ceiling_v13.json. No network, no model."""
import json, time
from pathlib import Path

import cbor2

import items as IT
import score as S
import tools as T
import verifier as V

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)
R1LEVEL = {"hash": "D", "binding": "E", "asof": "E'", "signature": "F", "log": "G", "recompute": "H", "source": "I"}


def ceiling(it, cond):
    h = it["h"]
    if cond in ("A", "B", "C"):
        v = float(h["stated"].replace("about", "")) if cond != "B" else h["record"]["value"]
        txt = f"DECISION={S.rule(it['task'], v)} VALUE={v!r}"
        return {"refused": False, "check": None, **S.score(it, cond, txt)}
    if cond == "D":
        if it["id"] == "M7":
            return {"refused": True, "check": "not found", **S.score(it, cond, "DECISION=DECLINE VALUE=NA")}
        v = cbor2.loads(h["bytes"])["value"]
        return {"refused": False, "check": None, **S.score(it, cond, f"DECISION={S.rule(it['task'], v)} VALUE={v!r}", seen_served=True)}
    err, text, meta = T.call(it, "E+", "resolve_verified", {"token": h["token"]})
    if err:
        return {"refused": True, "check": meta.get("first_fail") or "not found", **S.score(it, cond, "DECISION=DECLINE VALUE=NA")}
    v = float(json.loads(text)["value_verbatim"])
    return {"refused": False, "check": None,
            **S.score(it, cond, f"DECISION={S.rule(it['task'], v)} VALUE={v!r}", seen_served=True, verified_pass=True)}


def main():
    t0 = time.perf_counter()
    items = IT.build_items()
    r1 = json.loads((V.ROOT / "research/repro/v11/out/mutation_matrix.json").read_text())
    r1first = {m["id"]: m["first_protected_level"] for m in r1["meta"]["mutations"]}
    rows, tests = [], []
    for it in items:
        full = V.verify(it["h"], it["q"])
        for cond in IT.ALL_C:
            if cond not in it["conds"]:
                continue
            c = ceiling(it, cond)
            rows.append({"item": it["id"], "cond": cond, "refused": c["refused"], "check": c["check"],
                         "check_r1_level": R1LEVEL.get(c["check"]), "fa": c["fa"], "decision": c["decision"],
                         "acted_value": c["acted_value"], "correct": c["correct"]})
        tests.append({"item": it["id"], "first_fail": full["first_fail"], "r1_level": R1LEVEL.get(full["first_fail"]),
                      "r1_first_protected": r1first.get(it["id"]),
                      "checks": {k: v[0] for k, v in full["results"].items()}})
    # unit tests: controls accept; every corrupted item refused at full depth except value-only ones (unaffected)
    fails = []
    for t in tests:
        iid = t["item"]
        if iid in ("G0", "G0-B", "M1", "M2", "M2-B"):
            if t["first_fail"] is not None:
                fails.append(f"{iid} should pass every check: {t}")
        elif t["first_fail"] is None:
            fails.append(f"{iid} should be refused: {t}")
        r1l = t["r1_first_protected"]
        if iid in r1first and r1l not in ("C",) and iid not in ("M1", "M2", "M7", "M17", "G0", "M11") and r1l != t["r1_level"]:
            fails.append(f"{iid}: R5 first check {t['r1_level']} != R1 level {r1l}")
    out = {"generated_by": "research/repro/v13/r5/ceiling.py", "seconds": round(time.perf_counter() - t0, 3),
           "unit_test_failures": fails, "full_depth": tests, "cells": rows}
    (OUT / "ceiling_v13.json").write_text(json.dumps(out, indent=1, default=str))
    for t in tests:
        print(f"{t['item']:5} first_fail={str(t['first_fail']):10} R1={t['r1_first_protected']}  " +
              " ".join(f"{k}:{v}" for k, v in t["checks"].items()))
    print("unit test failures:", fails or "none")
    by = {}
    for r in rows:
        if r["fa"] is not None:
            by.setdefault(r["cond"], []).append(r["fa"])
    print({c: f"{sum(v)}/{len(v)}" for c, v in by.items()})


if __name__ == "__main__":
    main()
