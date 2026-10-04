#!/usr/bin/env python3
"""audit_strict.py: a stricter re-audit of the Part S transcripts (prereg addendum 2), added after the run.

score_s.py's ALLOWED pattern is looser than the audit rule A2.4 states: it would accept a second command after a
newline, a $(...) or backtick substitution inside double quotes, a glob or a trailing comment. This script re-checks
each recorded tool call, failed attempts included, against a strict form: exactly one line
    python3 <rtool.py> <the trial's own id> <the arm's own tool> ['<json without $ or backticks>' | key=value ...]
and reports any call that is not in that form, names another trial, or uses the other arm's tool.
score_s.py is unchanged (its BLAKE3 is bound by the addendum); this script reads its inputs only.
The rtool.py path it requires is the one the run used, read from the hash-bound prompts (replay.recorded_rtool), so the
check gives the same answer in a checkout at any path; replay.py also replays each call and re-scores the trials.

    python3 research/repro/v13/r5/addendum2/audit_strict.py
"""
import glob
import json
import shlex
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from replay import recorded_rtool, strict  # noqa: E402
ARM_TOOLS = {"B+": {"verify_observation"}, "E": {"fetch_evidence", "verify_evidence"}}


def main():
    STRICT = strict(recorded_rtool())
    arm = {t["trial"]: t["arm"] for t in json.loads((HERE / "plan_s.json").read_text())["trials"]}
    n = loose = other = cross = nonbash = 0
    for f in sorted(glob.glob(str(HERE / "raw_s" / "*.json"))):
        d = json.loads(Path(f).read_text())
        for a in d["attempts"]:
            for c in a["calls"]:
                if c["name"] == "SubagentHandback":
                    continue
                n += 1
                if c["name"] != "Bash":
                    nonbash += 1
                    print("not Bash:", d["trial"], c["name"])
                    continue
                cmd = (c["input"] or {}).get("command", "")
                m = STRICT.match(cmd)
                if not m:
                    loose += 1
                    print("not in the strict form:", d["trial"], repr(cmd[:160]))
                    continue
                if m.group(1) != d["trial"]:
                    other += 1
                    print("names another trial:", d["trial"], m.group(1))
                if shlex.split(cmd)[3] not in ARM_TOOLS[arm[d["trial"]]]:
                    cross += 1
                    print("other arm's tool:", d["trial"], shlex.split(cmd)[3])
    print(f"{n} tool calls in {len(glob.glob(str(HERE / 'raw_s' / '*.json')))} trials (failed attempts included): "
          f"{nonbash} not Bash, {loose} outside the strict form, {other} naming another trial, {cross} with the other arm's tool")
    return 0 if not (nonbash or loose or other or cross) else 1


if __name__ == "__main__":
    raise SystemExit(main())
