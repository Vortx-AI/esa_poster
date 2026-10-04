#!/usr/bin/env python3
"""matched.py: Part A of prereg addendum 2, the deterministic matched receivers. No model, no network.

For every item whose conditions include B (23 primary items and the controls G0, G0-B): the receiver gets the JSON
observation of the condition-B handoff and the item's question (bound by the harness, as for E+), accepts or refuses,
and acts by the task rule on the value it accepted. Scored by score.py as condition B. Receivers: B+ (verifier_conv,
the matched ablation) and B++ (verifier_hard, the hardened sensitivity), beside plain B (no verifier) and E+ (the emem
verifier) recomputed by ceiling.py and checked against the frozen out/ceiling_v13.json. Writes out/addendum2_ceiling.json.

    python3 research/repro/v13/r5/addendum2/matched.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import ceiling as CE  # noqa: E402
import items as IT  # noqa: E402
import score as S  # noqa: E402
import verifier_conv as VC  # noqa: E402
import verifier_hard as VH  # noqa: E402

OUT = HERE.parent / "out"
FROZEN = json.loads((OUT / "ceiling_v13.json").read_text())


def act(it, rv):
    if rv["accept"]:
        v = rv["value"]
        return f"DECISION={S.rule(it['task'], v)} VALUE={v!r}"
    return "DECISION=DECLINE VALUE=NA"


def main():
    rows = []
    for it in IT.build_items():
        if "B" not in it["conds"]:
            continue
        ob = IT.observation_json(it)
        row = {"item": it["id"], "family": it["family"], "threat": it["threat"], "primary": it["primary"], "desc": it["desc"]}
        for arm, mod in (("B+", VC), ("B++", VH)):
            rv = mod.verify(ob, it["q"])
            sc = S.score(it, "B", act(it, rv))
            row[arm] = {"accept": rv["accept"], "first_fail": rv["first_fail"],
                        "checks": {k: v[0] for k, v in rv["results"].items()},
                        "detail": {k: v[1] for k, v in rv["results"].items()},
                        "decision": sc["decision"], "acted_value": sc["acted_value"], "fa": sc["fa"], "correct": sc["correct"]}
        for cond in ("B", "E+"):
            c = CE.ceiling(it, cond)
            fz = next(r for r in FROZEN["cells"] if r["item"] == it["id"] and r["cond"] == cond)
            assert (c["fa"], c["decision"]) == (fz["fa"], fz["decision"]), (it["id"], cond, c, fz)
            row[cond] = {"accept": not c["refused"], "first_fail": c["check"], "decision": c["decision"], "fa": c["fa"],
                         "correct": c["correct"]}
        rows.append(row)
    prim = [r for r in rows if r["primary"]]
    ctrl = [r for r in rows if not r["primary"]]
    summary = {}
    for arm in ("B", "B+", "B++", "E+"):
        fa = [r["item"] for r in prim if r[arm]["fa"]]
        summary[arm] = {"fa": len(fa), "n": len(prim), "fa_items": fa,
                        "controls_accepted": sum(r[arm]["accept"] for r in ctrl), "n_controls": len(ctrl),
                        "correct_primary": sum(bool(r[arm]["correct"]) for r in prim)}
    out = {"generated_by": "research/repro/v13/r5/addendum2/matched.py", "prereg": "research/repro/v13/r5/prereg_addendum2.md",
           "items": len(rows), "primary": len(prim), "controls": [r["item"] for r in ctrl], "summary": summary, "rows": rows}
    (OUT / "addendum2_ceiling.json").write_text(json.dumps(out, indent=1, default=str))
    print(f"{'item':6}{'family':16}{'B':>4}{'B+':>16}{'B++':>18}{'E+':>14}")
    for r in rows:
        cell = lambda a: (("FA " if r[a]["fa"] else "") + ("acc" if r[a]["accept"] else f"ref:{r[a]['first_fail']}"))
        print(f"{r['item']:6}{r['family']:16}{cell('B'):>8}{cell('B+'):>16}{cell('B++'):>18}{cell('E+'):>14}")
    for a, s in summary.items():
        print(a, f"FA {s['fa']}/{s['n']}", s["fa_items"], f"controls accepted {s['controls_accepted']}/{s['n_controls']}")


if __name__ == "__main__":
    main()
