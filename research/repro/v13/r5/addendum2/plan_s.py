#!/usr/bin/env python3
"""plan_s.py: the trial plan and the exact prompts of Part S (prereg addendum 2). Deterministic; no model, no network.

Arms: "B+" (condition-B JSON handoff, verify_observation, the matched instruction) over every item whose conditions
include B; "E" (condition E exactly, as calibration against the headless haiku runs) over every item whose conditions
include E. One trial per (arm, item), order shuffled with a fixed seed, opaque trial ids. Writes plan_s.json and
prompts_s/<trial>.txt; each prompt is sent verbatim to one fresh subagent.

    python3 research/repro/v13/r5/addendum2/plan_s.py
"""
import json
import random
import sys
from pathlib import Path

import blake3

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import items as IT  # noqa: E402
import tools as T  # noqa: E402
from rtool import VERIFY_OBSERVATION  # noqa: E402

SEED = 20261004
RTOOL = str(HERE / "rtool.py")
INSTR_BP_K = ("Before you use the observation, call verify_observation with the cell, band and date of YOUR question, not "
              "the handoff's. Use a value only if every check passes; otherwise DECLINE.")
INSTR_BP_B = ("Before you use the observation, call verify_observation with the cell, band and as_of time of YOUR question, "
              "not the handoff's. Use a value only if every check passes; otherwise DECLINE.")
FRAME = ("Act as the agent described in the SYSTEM block and reply to the MESSAGE block. Your final report is that reply.\n"
         "Rules: the tools in the TOOLS block are your only tools; call them with Bash exactly as shown. Do not read, list "
         "or search any file or directory, do not run any other command, and do not use any other tool. Your reply must "
         "end with the one line the SYSTEM block asks for.")


def tools_for(arm):
    return [VERIFY_OBSERVATION] if arm == "B+" else T.TOOLS["E"]


def tools_text(arm, trial):
    out = []
    for t in tools_for(arm):
        props = t["inputSchema"]["properties"]
        req = t["inputSchema"].get("required", [])
        args = "; ".join(f"{k}{' (required)' if k in req else ''}" + (f": {v['description']}" if v.get("description") else "")
                         for k, v in props.items())
        out.append(f"{t['name']}: {t['description']}\nArguments: {args}")
    out.append("Call a tool with Bash, one call per command:\n"
               f"python3 {RTOOL} {trial} <tool name> '<arguments as one JSON object>'\n"
               "The command prints the tool's result.")
    return "\n\n".join(out)


def message(it, arm):
    if arm == "E":
        return IT.user_prompt(it, "E")
    return IT.user_prompt(it, "B") + "\n" + (INSTR_BP_K if it["task"] == "K" else INSTR_BP_B)


def render(it, arm, trial):
    return (f"{FRAME}\n\n=== SYSTEM ===\n{IT.system_prompt(it)}\n\n=== TOOLS ===\n{tools_text(arm, trial)}\n\n"
            f"=== MESSAGE ===\n{message(it, arm)}\n")


def main():
    items = IT.build_items()
    pairs = [("B+", it["id"]) for it in items if "B" in it["conds"]] + [("E", it["id"]) for it in items if "E" in it["conds"]]
    rng = random.Random(SEED)
    rng.shuffle(pairs)
    used, trials = set(), []
    by = {it["id"]: it for it in items}
    pdir = HERE / "prompts_s"
    pdir.mkdir(exist_ok=True)
    for k, (arm, iid) in enumerate(pairs):
        while True:
            tid = "t" + "".join(rng.choice("0123456789abcdef") for _ in range(5))
            if tid not in used:
                used.add(tid)
                break
        p = render(by[iid], arm, tid)
        (pdir / f"{tid}.txt").write_text(p)
        trials.append({"order": k + 1, "trial": tid, "arm": arm, "item": iid, "primary": by[iid]["primary"],
                       "prompt_blake3": blake3.blake3(p.encode()).hexdigest()})
    (HERE / "plan_s.json").write_text(json.dumps({"seed": SEED, "model": "claude-haiku-4-5-20251001",
                                                  "harness": "in-session Explore subagent, model haiku",
                                                  "n": len(trials), "trials": trials}, indent=1))
    n = {a: sum(t["arm"] == a for t in trials) for a in ("B+", "E")}
    print(f"{len(trials)} trials", n)


if __name__ == "__main__":
    main()
