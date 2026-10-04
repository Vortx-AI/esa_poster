#!/usr/bin/env python3
"""replay.py: re-check and re-score the archived Part S trials from any checkout location (prereg addendum 2).

The archived commands name the rtool.py of the run (/home/user/esa_poster/research/repro/v13/r5/addendum2/rtool.py).
score_s.py, which the addendum binds by its BLAKE3 and which stays unchanged, builds its allowed command from the current
checkout, so in a clone at another path every archived call fails its pattern and the scores do not reproduce. This
wrapper reads the execution root of the run from the trial prompts (prompts_s/<trial>.txt, each bound by its BLAKE3 in
plan_s.json; the 53 prompts name one rtool.py) and then:
  1. checks each archived tool call, failed attempts included, with the strict rule of audit_strict.py against that
     root: one line, the recorded rtool.py, the trial's own id, the arm's own tool, single-quoted JSON or key=value;
  2. replays each call in-process with rtool.py's own functions (no call log written) and compares the output with the
     archived tool result;
  3. re-scores with score_s.score_all(), its pattern rebuilt around the recorded root and otherwise unchanged, compares
     the result with out/addendum2_s.json byte for byte, and restores the committed file.

    python3 research/repro/v13/r5/addendum2/replay.py
"""
import contextlib
import io
import json
import re
import shlex
import sys
from pathlib import Path

import blake3

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
PLAN = json.loads((HERE / "plan_s.json").read_text())
ARM_TOOLS = {"B+": {"verify_observation"}, "E": {"fetch_evidence", "verify_evidence"}}
CALL_LINE = re.compile(r"^python3 (\S+/rtool\.py) (t[0-9a-f]{5}) <tool name> ", re.M)


def recorded_rtool():
    """The rtool.py path the run used, from the hash-bound prompts; each prompt must name it once, with its own id."""
    paths = set()
    for t in PLAN["trials"]:
        p = (HERE / "prompts_s" / f"{t['trial']}.txt").read_bytes()
        assert blake3.blake3(p).hexdigest() == t["prompt_blake3"], f"prompt {t['trial']} does not match plan_s.json"
        m = CALL_LINE.findall(p.decode())
        assert len(m) == 1 and m[0][1] == t["trial"], f"prompt {t['trial']}: call line {m}"
        paths.add(m[0][0])
    assert len(paths) == 1, paths
    return paths.pop()


def strict(rtool):
    return re.compile(r"^python3 " + re.escape(rtool) + r" (t[0-9a-f]{5}) (fetch_evidence|verify_evidence|verify_observation)"
                      r"( '[^'$`\n]*'| [A-Za-z_]+=[^\s'\"$`;|&<>*?#\n]+)*$")


def archived_calls():
    for f in sorted((HERE / "raw_s").glob("*.json")):
        d = json.loads(f.read_text())
        for a in d["attempts"]:
            for c in a["calls"]:
                if c["name"] != "SubagentHandback":
                    yield d["trial"], c


def check_and_replay(rtool):
    import items as IT
    import rtool as RT
    import tools as T
    plan = {t["trial"]: t for t in PLAN["trials"]}
    items = {it["id"]: it for it in IT.build_items()}
    rx = strict(rtool)
    n = bad = same = 0
    for trial, c in archived_calls():
        n += 1
        cmd = (c["input"] or {}).get("command", "") if c["name"] == "Bash" else ""
        m = rx.match(cmd)
        arm = plan[trial]["arm"]
        if not m or m.group(1) != trial or m.group(2) not in ARM_TOOLS[arm]:
            bad += 1
            print("fails the strict rule:", trial, repr(cmd[:160]))
            continue
        argv = shlex.split(cmd)
        name, rest = argv[3], argv[4:]
        it = items[plan[trial]["item"]]
        try:
            args = RT.parse_args(rest)
            if arm == "B+":
                err, text, _ = RT.bplus(it, args) if name == "verify_observation" else (True, f"unknown tool {name}", {})
            else:
                err, text, _ = T.call(it, "E", name, args)
        except Exception as e:  # the same handling as rtool.main
            err, text = True, f"error: {type(e).__name__}: {e}"
        out = ("ERROR: " if err else "") + text
        if out.strip() == (c["result"].get("text") or "").strip():
            same += 1
        else:
            print("replayed output differs:", trial, name)
    return n, bad, same


def rescore(rtool):
    import score_s as SS
    old = re.escape(SS.RTOOL)
    assert old in SS.ALLOWED.pattern
    SS.RTOOL = rtool
    SS.ALLOWED = re.compile(SS.ALLOWED.pattern.replace(old, re.escape(rtool), 1), SS.ALLOWED.flags)
    out = HERE.parent / "out" / "addendum2_s.json"
    committed = out.read_bytes()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            SS.score_all()
        fresh = out.read_bytes()
    finally:
        out.write_bytes(committed)
    return fresh == committed, json.loads(fresh)["summary"]


def main():
    rtool = recorded_rtool()
    here = str(HERE / "rtool.py")
    print(f"recorded rtool.py: {rtool}" + ("" if rtool == here else f" (this checkout: {here})"))
    n, bad, same = check_and_replay(rtool)
    print(f"{n} archived tool calls: {n - bad} pass the strict rule, {same} replay to the archived output")
    ok, summ = rescore(rtool)
    print("re-score:", "identical to out/addendum2_s.json" if ok else "DIFFERS from out/addendum2_s.json",
          f"(B+ {summ['B+']['fa']} of {summ['B+']['n_primary']}, E {summ['E']['fa']} of {summ['E']['n_primary']})")
    return 0 if (bad == 0 and same == n and ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
