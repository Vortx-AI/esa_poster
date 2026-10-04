#!/usr/bin/env python3
"""rtool.py: the receiver's tools for the subagent arm of prereg addendum 2 (Part S). One process per call:

    python3 rtool.py <trial> <tool> '<arguments as one JSON object>'      (key=value pairs are accepted too)

<trial> is an opaque id from plan_s.json naming (item, arm). Arm "E" exposes fetch_evidence and verify_evidence exactly
as tools.call does for condition E. Arm "B+" exposes verify_observation: the matched conventional verifier
(verifier_conv.py) applied to the JSON observation in that trial's handoff, bound to the question the caller passes,
with the same argument parsing as verify_evidence. Every call is appended to calls_s.jsonl. Output: the tool's text,
prefixed "ERROR: " when the tool returns an error.
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

PLAN = HERE / "plan_s.json"
LOG = HERE / "calls_s.jsonl"

VERIFY_OBSERVATION = {
    "name": "verify_observation",
    "description": ("Verify the JSON observation in the handoff you received against a question. Checks: binding of the "
                    "observation to the cell, band and date you pass; optional as_of time (observation must be signed by "
                    "then); recompute of the value from the DNs and offset in the observation; source re-read against the "
                    "committed Sentinel-2 pixel. Returns each check and a verdict."),
    "inputSchema": {"type": "object", "properties": {
        "cell": {"type": "string"},
        "band": {"type": "string", "description": "e.g. indices.ndvi or copdem30m.elevation_mean"},
        "date": {"type": "string", "description": "YYYY-MM-DD scene date (ignored for static bands)"},
        "as_of": {"type": "string", "description": "optional RFC 3339 time"}},
        "required": ["cell", "band"]},
}


def parse_args(rest):
    if not rest:
        return {}
    s = " ".join(rest).strip()
    if s.startswith("{"):
        return json.loads(s)
    out = {}
    for kv in rest:
        k, _, v = kv.partition("=")
        out[k.strip()] = v.strip()
    return out


def bplus(it, args):
    import items as IT
    import tools as T
    import verifier_conv as VC
    q = T._q_from_args(args)
    r = VC.verify(IT.observation_json(it), q)
    out = {"checks": {c: {"result": s, "detail": d} for c, (s, d) in r["results"].items()},
           "verdict": "PASS" if r["accept"] else f"FAIL (first failed check: {r['first_fail']})"}
    if r["accept"]:
        out["value_verbatim"] = repr(r["value"])
    return False, json.dumps(out), {"verdict": r["accept"], "first_fail": r["first_fail"], "bound_q": q}


def main(argv):
    if argv[:1] == ["--selftest"]:
        print("rtool ok")
        return 0
    if len(argv) < 2:
        print("ERROR: usage: rtool.py <trial> <tool> '<arguments as one JSON object>'")
        return 0
    trial, name, rest = argv[0], argv[1], argv[2:]
    plan = {t["trial"]: t for t in json.loads(PLAN.read_text())["trials"]}
    t0 = time.perf_counter()
    meta, args = {}, None
    if trial not in plan:
        err, text = True, f"unknown trial {trial}"
    else:
        import items as IT
        import tools as T
        t = plan[trial]
        it = next(i for i in IT.build_items() if i["id"] == t["item"])
        try:
            args = parse_args(rest)
            if t["arm"] == "B+":
                err, text, meta = bplus(it, args) if name == "verify_observation" else (True, f"unknown tool {name}", {})
            else:
                err, text, meta = T.call(it, "E", name, args)
        except Exception as e:  # malformed arguments are an error the caller sees, never a pass
            err, text = True, f"error: {type(e).__name__}: {e}"
    with open(LOG, "a") as fh:
        fh.write(json.dumps({"t": time.time(), "trial": trial, "tool": name, "argv": rest, "args": args, "is_error": err,
                             "ms": round((time.perf_counter() - t0) * 1000, 3), "meta": meta, "text": text[:2000]},
                            default=str) + "\n")
    print(("ERROR: " if err else "") + text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
