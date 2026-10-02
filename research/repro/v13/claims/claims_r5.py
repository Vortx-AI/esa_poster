"""Write research/v13/12_claims_map_additions_r5.json: the claims rows for every R5 number the v13 board prints.

    python research/repro/v13/claims/claims_r5.py

Every row's value is read from research/repro/v13/r5/results.json (written by analyze.py) or quoted from results.md;
nothing is typed. Rows override the main map's R5 template rows (same ids) with the printed strings, and add the
per-cell rows F6 prints, the per-model rows the spine's strip prints, and the deviation lines. The board build
(poster/build_v13.py) re-runs each row's check against the file.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
R5 = REPO / "research" / "repro" / "v13" / "r5"
RES_JSON = "research/repro/v13/r5/results.json"
RES_MD = "research/repro/v13/r5/results.md"
OUT = REPO / "research" / "v13" / "12_claims_map_additions_r5.json"
PREREG = "research/repro/v13/r5/prereg.md"

D = json.loads((R5 / "results.json").read_text())
MD = (R5 / "results.md").read_text()
assert D["final"] is True
PRE_HASH = re.search(r"^blake3:\s*([0-9a-f]{64})", (R5 / "prereg_hash.txt").read_text(), re.M).group(1)
assert D["prereg_blake3"] == PRE_HASH, "results.json names a prereg hash other than the one pushed before trial 1"

NAME = {"claude-haiku-4-5-20251001": "Haiku 4.5", "claude-sonnet-5-5": "Sonnet 5.5", "claude-opus-5-5": "Opus 5.5",
        "qwen2.5-7b-instruct-q4_k_m": "Qwen2.5-7B"}
SHORT = {"claude-haiku-4-5-20251001": "haiku", "claude-sonnet-5-5": "sonnet", "claude-opus-5-5": "opus",
         "qwen2.5-7b-instruct-q4_k_m": "qwen7b"}
COND_ID = {"A": "A", "B": "B", "C": "C", "D": "D", "E0": "E0", "E": "E", "E+": "Eplus"}
COND_NAME = {"A": "prose", "B": "JSON", "C": "retrieved text (RAG)", "D": "opaque id",
             "E0": "EMEM token, tool, no instruction", "E": "EMEM token, instructed check", "E+": "EMEM token behind a fail-closed resolver"}
PREREG_SRC = f"{PREREG} (BLAKE3 {PRE_HASH[:8]}…, hashed {D['dates']['prereg_hashed_utc']}, before trial 1)"
DAY = D["dates"]["first_trial_utc"][:10]
MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DATE_TXT = f"{int(DAY[8:10])} {MONTHS[int(DAY[5:7])]} {DAY[:4]}"
assert D["dates"]["last_trial_utc"][:10] == DAY, "trials span one day; the date text assumes so"

rows = []


def row(id, block, prints, status, layer, source, check, note="", tier="30cm", value=None):
    rows.append(dict(id=id, block=block, print=prints if isinstance(prints, list) else [prints], status=status, layer=layer,
                     source=source, date=DAY, value=value, check=check, note=note, tier=tier, fallback=None, r5_key=None,
                     checked=None))


def kn_forms(k, n):
    return [f"{k} of {n}", f"{k} / {n}", f"{k} / {n}"]


def md_grep(s):
    assert s in MD, f"results.md does not contain: {s!r}"
    return {"kind": "grep", "file": RES_MD, "arg": s, "expect": None}


def js(path, exp):
    return {"kind": "json", "file": RES_JSON, "arg": path, "expect": exp}


# ---- pooled primary false acceptance per condition (the spine numerals, F6 totals, the headline, the conclusion)
for cond, cid in COND_ID.items():
    fa = D["primary"][cond]["pooled_claude"]["false_accept"]
    row(f"R5.{cid}.pooled", "P1 spine + P5 matrix", kn_forms(fa["k"], fa["n"]), "PRE-REGISTERED", "L0-L3",
        {"file": RES_JSON, "pointer": f"primary.{cond}.pooled_claude.false_accept", "prereg": PREREG_SRC,
         "wilson95": D["primary"][cond]["pooled_claude"]["wilson95"]},
        js(["primary", cond, "pooled_claude", "false_accept"], fa),
        note=f"condition {cond}: {COND_NAME[cond]}; three Claude models pooled; primary items only", tier="3m",
        value=f"{fa['k']}/{fa['n']}")
    for model, pm in D["primary"][cond]["per_model"].items():
        fa_m = pm["false_accept"]
        row(f"R5.{cid}.{SHORT[model]}", "P1 spine strip", kn_forms(fa_m["k"], fa_m["n"]), "PRE-REGISTERED", "L0-L3",
            {"file": RES_JSON, "pointer": f"primary.{cond}.per_model.{model}.false_accept", "prereg": PREREG_SRC,
             "wilson95": pm["wilson95"]},
            js(["primary", cond, "per_model", model, "false_accept"], fa_m),
            note=f"{NAME[model]} in condition {cond} ({COND_NAME[cond]})" + ("; open weights, one replicate, descriptive only" if model.startswith("qwen") else ""),
            value=f"{fa_m['k']}/{fa_m['n']}")
    ce = D["primary"][cond]["ceiling"]["false_accept"]
    row(f"R5.{cid}.ceiling", "P5 matrix", kn_forms(ce["k"], ce["n"]), "MEASURED", "L0-L3",
        {"file": RES_JSON, "pointer": f"primary.{cond}.ceiling.false_accept"},
        js(["primary", cond, "ceiling", "false_accept"], ce), note="the deterministic verifier on the same items")

# ---- per cell (F6 bars), every condition and item with a false-acceptance count
for cond in D["cells"]:
    for item, v in D["cells"][cond].items():
        fa = v.get("false_accept") if isinstance(v, dict) else None
        if not isinstance(fa, dict):
            continue
        row(f"R5.cell.{cond}.{item}.false_accept", "P5 matrix cell", kn_forms(fa["k"], fa["n"]), "PRE-REGISTERED", "L0-L3",
            {"file": RES_JSON, "pointer": f"cells.{cond}.{item}.false_accept", "per_model": v["per_model"]},
            js(["cells", cond, item, "false_accept"], fa), note=f"family {v['family']}; R1 ceiling false accept: {v['ceiling_fa']}")

# ---- design facts printed in scope lines
reps = D["cells"]["A"]["M1"]["per_model"]
per_cell = sum(v["n"] for v in reps.values())
row("R5.models", "P1 spine scope", "Claude Haiku 4.5, Sonnet 5.5 and Opus 5.5 as B, pooled; Qwen2.5-7B apart", "PRE-REGISTERED", "n/a",
    {"file": RES_JSON, "pointer": "models", "prereg": PREREG_SRC}, js(["models"], D["models"]),
    note="the four receivers; the three Claude models are pooled for the primary endpoint, the open model is reported apart")
row("R5.dates", "P1 spine scope + P5 header", [f"{D['n_trials_scored']:,} scored trials on {DATE_TXT}", DATE_TXT, f"{D['n_trials_scored']:,}"],
    "MEASURED", "n/a", {"file": RES_JSON, "pointer": "n_trials_scored; dates.first_trial_utc, dates.last_trial_utc"},
    js(["n_trials_scored"], D["n_trials_scored"]), note="pilot (84) and infrastructure failures (771) excluded by design")
row("R5.percell", "P5 scope", [f"n {per_cell} per cell", f"{reps['haiku']['n']} Haiku, {reps['sonnet']['n']} Sonnet, {reps['opus']['n']} Opus runs",
                               f"{reps['haiku']['n']} Haiku 4.5, {reps['sonnet']['n']} Sonnet 5.5, {reps['opus']['n']} Opus 5.5 runs"],
    "PRE-REGISTERED", "n/a", {"file": RES_JSON, "pointer": "cells.A.M1.per_model[*].n", "rule": "results.md section 9: the pre-registered cost rule"},
    js(["cells", "A", "M1", "per_model"], reps), note="replicates per Claude model in every primary cell")
n_items_A = D["primary"]["A"]["pooled_claude"]["false_accept"]["n"] // per_cell
row("R5.F6.scope", "P5 figure scope", f"Bars: agents' false acceptance, k of n per cell, n {per_cell} ({reps['haiku']['n']} Haiku 4.5, {reps['sonnet']['n']} Sonnet 5.5, {reps['opus']['n']} Opus 5.5 runs); squares: the deterministic ceiling. Totals pool {n_items_A} items, {DATE_TXT}.",
    "PRE-REGISTERED", "L0-L3", {"file": RES_JSON, "pointer": "cells.A.M1.per_model; primary.A.pooled_claude.false_accept.n / 12 = 23 primary items in A"},
    js(["primary", "A", "pooled_claude", "false_accept", "n"], n_items_A * per_cell),
    note="F6 in R5 mode draws R1's 16 rows; the totals pool the 23 primary items of the results file so they read the same as the spine")
row("R5.M17.notrun", "P5 matrix", "not run", "OUT-OF-SCOPE", "L4", {"file": RES_MD, "section": "10"},
    md_grep("M17 (entity: A meant a different physical place) is outside every condition and was not run with agents"),
    note="R1's result for M17 (never refused) stands")

# ---- deviations and adverse findings the board prints (brief H.1 degrade rules; results.md sections 9 and 10)
row("R5.excluded", "P5 scope", [f"{D['n_excluded']} trial rows with no model output", f"{D['n_excluded']}", "06:31 to 06:40 UTC"],
    "MEASURED", "n/a", {"file": RES_JSON, "pointer": "n_excluded; excluded[*].why", "md": "results.md section 9, first bullet"},
    js(["n_excluded"], D["n_excluded"]), note="a CLI rate limit returned 'session limit' text with exit 0; every affected trial id was re-run after 08:40 UTC")
row("R5.excluded.window", "P5 scope", "06:31 to 06:40 UTC", "MEASURED", "n/a", {"file": RES_MD, "section": "9"},
    md_grep("between 06:31 and 06:40 UTC the Claude Code CLI returned the text \"You've hit your session limit\""))
row("R5.qwen.alone", "P5 scope", "the second model family is Qwen alone", "MEASURED", "n/a", {"file": RES_MD, "section": "9"},
    md_grep("The second model family is therefore Qwen alone."), note="Llama, Gemma and Phi were downloaded but not run (CPU time)")
fb, fd = D["pooled_claude_primary_fa"]["B"], D["pooled_claude_primary_fa"]["D"]
row("R5.baseline.catch", "P5 scope", [f"{fb['n'] - fb['k']} of {fb['n']} and {fd['n'] - fd['k']} of {fd['n']}", "about half"],
    "MEASURED", "n/a", {"file": RES_JSON, "pointer": "pooled_claude_primary_fa.B and .D: n - k", "md": "results.md section 10: 'Baseline B refused or recomputed correctly in 112/276', 'Baseline D ... 134/288'"},
    md_grep(f"Baseline D refused or recomputed correctly in {fd['n'] - fd['k']}/{fd['n']} in-scope trials"),
    note="JSON (B) and the opaque id (D) catch corruptions by reading the fields they carry; these catches are credited to the baseline")
m24 = D["cells"]["E0"]["M24"]["per_model"]["haiku"]
row("R5.E0.haiku.M24", "P5 scope", [f"{m24['k']} of {D['primary']['E0']['per_model']['claude-haiku-4-5-20251001']['false_accept']['n']}", "M24"],
    "PRE-REGISTERED", "L1", {"file": RES_JSON, "pointer": "primary.E0.per_model.claude-haiku-4-5-20251001.false_accept; cells.E0.M24.per_model.haiku"},
    js(["cells", "E0", "M24", "per_model", "haiku"], m24),
    note="both false acceptances in E0 are Haiku on M24: it called the check with the handoff's cell instead of its own question's (results.md section 10)")
b2 = D["block2_pooled"]
row("R5.block2.M15r", "P5 scope", ["4 of 4", "2 of 4", "0 of 4"], "MEASURED", "L3",
    {"file": RES_MD, "section": "5, Block 2 table, row 'M15r false acceptance'", "json": "block2[model][L0|L1|L2].M15r.fa summed over the three Claude models"},
    md_grep("| M15r false acceptance | 4/4 | 2/4 | 0/4 |"),
    note="live emem MCP, real pre-fix record kxjvfwpa: no instruction 4/4, instructed to resolve and bind 2/4, with our source re-read 0/4; one-sided Fisher p = 0.214")
row("R5.block2.pooled", "methods", [f"{b2['L0']['fa_inscope']['k']} of {b2['L0']['fa_inscope']['n']}", f"{b2['L1']['fa_inscope']['k']} of {b2['L1']['fa_inscope']['n']}", f"{b2['L2']['fa_inscope']['k']} of {b2['L2']['fa_inscope']['n']}"],
    "MEASURED", "L0-L3", {"file": RES_JSON, "pointer": "block2_pooled.{L0,L1,L2}.fa_inscope"},
    js(["block2_pooled", "L2", "fa_inscope", "k"], b2["L2"]["fa_inscope"]["k"]), note="site methods page")

# ---- F2's handoff snippets in R5 mode: the genuine record (G0) as each form carries it, rendered by the experiment's items.py
import sys
sys.path.insert(0, str(R5))
import items as IT  # noqa: E402
g0 = next(i for i in IT.build_items() if i["id"] == "G0")
row("F2.snippets", "P1 spine lanes (R5 mode)", [IT.prose(g0), IT.json_handoff(g0), IT.answer_passage(g0), f"record ref {IT.OPAQUE_REF}"],
    "MEASURED", "n/a", {"file": "research/repro/v13/r5/items.py", "pointer": "prose(G0), json_handoff(G0), answer_passage(G0), OPAQUE_REF"},
    {"kind": "grep", "file": "research/repro/v13/r5/items.py", "arg": "def answer_passage", "expect": None},
    note="the handoff text of the genuine record in each lane, as the R5 runner handed it over; F2 clips each to its lane width")

# ---- F2's ghost squares: the R1 ceiling beside each agent numeral (overrides the F1-4 template row "{R1 ceiling k / n}")
R1 = json.loads((REPO / "research/repro/v11/out/mutation_matrix.json").read_text())["summary"]
row("F2.ceiling", "P1 spine (R5 mode)", [f"R1 {R1[l]['false_accepts']} / {R1[l]['applicable']}" for l in "ABCI"] +
    [f"R1 {R1[l]['false_accepts']} / {R1[l]['applicable']}" for l in "ABCI"], "MEASURED", "L0-L3",
    {"file": "research/repro/v11/out/mutation_matrix.json", "pointer": "summary.{A,B,C,I}.false_accepts / applicable"},
    {"kind": "json", "file": "repro/v11/out/mutation_matrix.json", "arg": ["summary", "I", "applicable"], "expect": 16},
    note="the deterministic receiver's result on the same lane, drawn as a 5 mm ghost square beside the agents' k / n")

doc = {"schema": "esa_poster v13 claims map additions (R5: agent receivers), same row schema as 12_claims_map.json",
       "version": 1, "generated": DAY, "generated_by": "research/repro/v13/claims/claims_r5.py",
       "brief": "research/v13/12_FINAL_BRIEF.md", "results": RES_JSON, "prereg_blake3": PRE_HASH,
       "rule": "rows with the same id as a main-map row replace it (the main map holds the pre-registration templates); "
               "every print string is read from results.json or quoted from results.md, and the board build re-runs each check",
       "rows": rows}
OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
print(f"{len(rows)} rows -> {OUT.relative_to(REPO)}")
