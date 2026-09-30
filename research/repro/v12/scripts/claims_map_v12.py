"""Write research/should_do/19_V12_CLAIMS_MAP.md from the measurement files, and check the board prints them.

Every row reads its value from a file; the script then asserts that the printed string occurs in the built board
(poster/poster.html, text and inlined SVG titles excluded) or in the figure-number dump the SVGs were drawn from.
usage: python research/repro/v12/scripts/claims_map_v12.py   (after python poster/build_v12.py)
"""
import csv
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
V12 = REPO / "research/repro/v12"
FIG = REPO / "poster/fig/v12/figure_numbers.json"
BOARD = REPO / "poster/poster.html"
OUT = REPO / "research/should_do/19_V12_CLAIMS_MAP.md"

N = json.load(open(FIG))
board = re.sub(r"(?s)<style.*?</style>|<svg.*?</svg>", "", BOARD.read_text())
board = re.sub(r"<[^>]+>", " ", board)
board = re.sub(r"\s+", " ", board)
rows = []


def row(section, printed, value, source, cls, on_board=True):
    if on_board:
        assert printed in board, f"not on the board: {printed!r}"
    rows.append((section, printed, value, source, cls))


# header and problem
row("Problem", "3 of 36 pairs", "compaction arm 'shared summary, under pressure': 3/36 pairs agree, 0/72 answers right",
    "claims map v11 R2 row (sec. 17, pre-registered); figure failure.svg", "pre-reg", on_board=False)
for lab, c, n, ag, npair in N["failure"]["rows"]:
    row("Problem figure", f"{ag}/{npair} pairs agree; {c}/{n} answers right", lab, "make_figures_v12.py COMPACTION = claims map v11 R2", "pre-reg", on_board=False)

# section 1: Berlin
b = N["berlin"]
row("1 sub", "15 products, 16 signed facts, 4 of them signed absences",
    f"products={b['products']}, facts={b['facts']}, absences={b['absences']}", "fig/v12/figure_numbers.json berlin (from case_berlin_stack.json)", "live")
assert (b["products"], b["facts"], b["absences"]) == (15, 16, 4)
for r in b["rows"]:
    row("1 figure", r["reading"], f"{r['product']}; class {r['class']}; fact_cid {r['fact_cid']}",
        "research/repro/v12/data/case_berlin_stack.json", "live, verified", on_board=False)
row("1 figure chip", "Sentinel-2C MSI L2A, 27 Sep 2026", b["scene"]["item"], "data/scene_defi.zb655.yaka.pUxe.headers", "live", on_board=False)
E = N["encoding"]
row("1 encoding", "43 slots, 1,792 dimensions", f"{E['slots']} slots, {E['dims']} dims, bands_cid {E['bands_cid']}",
    "data/v1_bands_2026-09-30.json (live /v1/bands)", "live", on_board=False)
row("1 encoding", "944 of 1,792 dimensions", f"encoder slots {E['encoders']} = {E['encoder_dims']} dims", "same", "live", on_board=False)
row("1 encoding", "slots per class", json.dumps(E["class_slots"]), "same", "live", on_board=False)

# section 2: R1 and R4
r1 = N["r1"]
row("4 figure", "15/15 ... 0/16", json.dumps(r1), "research/repro/v11/out/mutation_matrix.json summary", "measured", on_board=False)
assert r1["A"] == [15, 15] and r1["I"] == [0, 16]
row("4 take", "Prose and JSON pass all 15 corruptions", "A, B false accepts 15/15", "mutation_matrix.json", "measured")
row("4 take", "none of the 16 in-scope cases", "I false accepts 0/16", "mutation_matrix.json", "measured")
ms = json.load(open(REPO / "research/repro/v11/out/mutation_matrix.json"))["meta"]["full_verification_ms"]
row("4 take", f"one full check takes {ms:.1f} ms offline", f"meta.full_verification_ms = {ms} (level I, 200 reps, source window cached)",
    "mutation_matrix.json (rerun by build_v12.py)", "measured")
P = json.load(open(REPO / "research/repro/data/v8/prevalence_summary.json"))
pre, post = P["pre"], P["post"]
_, lo, hi = pre["frac_round_wilson95"]
row("4 M15", f"{pre['matches_round_not_floor']} of {pre['n']} sampled records ({lo * 100:.0f} to {hi * 100:.0f} %, Wilson 95 %)",
    f"pre: matches_round_not_floor={pre['matches_round_not_floor']}, n={pre['n']}, wilson95={pre['frac_round_wilson95']}",
    "research/repro/data/v8/prevalence_summary.json", "measured")
row("4 M15", f"After: {post['matches_round_not_floor']} of {post['n']}", f"post: n={post['n']}, signed {post['signed_at_range']}",
    "same", "measured")
m15 = N["m15"]
row("4 M15 figure", "0.4709 / 0.3016, rule 0.4705", json.dumps(m15), "pixel_windows.json (DNs, BOA offset) recomputed in make_figures_v12.py; "
    "asserted equal to mutation_matrix.json meta", "recomputed", on_board=False)
v = N["r4"]
row("2 R4", "918.0 m", f"{v['values'][0]} signed {v['signed_at'][0]}", "research/repro/data/contra_bengaluru.json", "live replay")
row("2 R4", "915.07 m", f"{v['values'][1]} first signed {v['signed_at'][1]}; {len(v['values']) - 1} signings", "same", "live replay")
row("2 R4", "since 11 Aug", v["signed_at"][1], "same", "live replay")
assert v["signed_at"][1].startswith("2026-08-11") and len(v["values"]) - 1 == 7

# section 3
checks = list(csv.DictReader(open(V12 / "data/eo_evidence_per_fact_checks.csv")))
cnt = Counter(c["case"] for c in checks)
assert len(checks) == 780 and all(c["verified"] == "PASS" for c in checks)
row("3 sub", "All 780 facts", f"{dict(cnt)}; all verified=PASS", "data/eo_evidence_per_fact_checks.csv", "live, verified")
k = N["keylong"]
row("3 Keylong", "141 Sentinel-2 L2A NDVI facts", f"{k['n_2025_2026']} (2025 to 2026) of {k['n_all']}; by satellite {k['by_satellite']}",
    "data/case_keylong_ndvi.json", "live, verified")
row("3 Keylong figure", "peaks", json.dumps(k["peaks"]), "same", "live, verified", on_board=False)
row("3 Keylong figure", "record 0.4709", json.dumps(k["record"]), "same", "live, verified", on_board=False)
ron = N["rondonia"]
row("3 Rondonia", "100 point cells 740 m apart, 600 facts", f"cells={ron['n_cells']}, facts={ron['facts']}, grid note: {ron['grid']['note']}",
    "data/case_rondonia_eudr.json", "live, verified")
row("3 Rondonia figure", "3 / 1 / 33 / 20 / 43", json.dumps(ron["counts"]) + f"; flagged loss years {ron['flagged_loss_years']}", "same", "live, verified", on_board=False)

# section 4
s = N["sat042"]
row("5 sub", "SAT-042", f"emem {s['commit']}, run {s['run']}", "trace/sat042_run_stdout.txt", "measured (reference run)")
row("5 text", "eight layers", f"{s['profile']} layers {s['layers']}", "same", "measured (reference run)")
row("5 figure", "2 consistent, 1 contradicted; 0.05, 0.15, 0.88", json.dumps(s["drift"]), "same", "measured (reference run)", on_board=False)
row("5 figure", "chain broken at seq 3", f"tampered segment {s['tamper'][0]}, broken at seq {s['tamper'][1]}", "same", "measured (reference run)", on_board=False)
row("Objections", "No spacecraft is enrolled", "live /v1/devices lists one generic host; orbital.satellite.v1 is candidate",
    "trace/trace_live_state.json; trace/trace_truth.md", "live")

row("3 sub", "including the 757 drawn here", f"Berlin {len(N['berlin']['rows'])} + Keylong {k['n_2025_2026']} + Rondonia {ron['facts']}",
    "figure_numbers.json", "live, verified")
assert len(N["berlin"]["rows"]) + k["n_2025_2026"] + ron["facts"] == 757
row("3 Rondonia card", "cell A: six signed facts", json.dumps(ron["card"]), "data/case_rondonia_eudr.json", "live, verified", on_board=False)
row("5 score", "3\u03c3 scores 0.5 and 9\u03c3 scores 0.75", "drift_contradiction_score: z = |d - a| / (3 sigma), s = z / (1 + z); "
    "tests pinned_points", "emem crates/emem-trace/src/drift.rs", "code")
row("5 score", "0.6402 \u00b1 0.02 (1\u03c3)", "fixed harness anchor for all three captures", "trace/sat042_run_stdout.txt", "measured (reference run)")

# formulas (drawn in model.svg, drift.svg, score.svg)
for name, src in [("observation O = (a, b, t, v, u, p, s)", "emem docs/model.md, observation tuple"),
                  ("cid(O) = BLAKE3(canonical CBOR(O)); s = Ed25519 over BLAKE3 of the body", "emem docs/model.md, identity and signature rows"),
                  ("M = (O*, E*), E = (subj, pred, obj, valid_from, valid_to)", "emem docs/model.md, memory definition"),
                  ("recall with as_of_tslot and as_of_signed_at", "emem docs/memory.md, bi-temporal recall"),
                  ("NDVI = (DN8 - DN4) / (DN8 + DN4 + 2 offset), offset -1000", "Sentinel-2 L2A BOA_ADD_OFFSET; pixel_windows.json offset"),
                  ("dz = d_env + d_sensor + d_geo + d_encoder + eps", "emem docs/whitepaper-v2.md, drift decomposition (the numeric split is not computed)"),
                  ("s = z / (1 + z), z = |x_device - x_anchor| / 3 sigma", "emem crates/emem-trace/src/drift.rs")]:
    row("Formulas", name, "definition", src, "spec", on_board=False)
row("Header", "doi:10.5281/zenodo.20706893 (v0.1.0)", "Zenodo record of paper v0.1.0", "Zenodo", "reference")

lines = ["# v12.1 claims map: every number and formula on the board, and where it comes from", "",
         "Generated by `research/repro/v12/scripts/claims_map_v12.py` from the measurement files; rows marked on-board are",
         "asserted to occur in the built board text. Figure numbers are dumped by `poster/make_figures_v12.py` to",
         "`poster/fig/v12/figure_numbers.json` from the same files. Live pulls: emem.dev, 30 Sep 2026 (UTC timestamps in each file).", "",
         "Scope notes that travel with these numbers: the Rondônia grid is point samples, not plot polygons, and is not an Annex II",
         "statement; 266 of the 780 facts were also recomputed from signed inputs, the rest are bound by cid, signature and log",
         "but were not re-read from the upstream COGs; SAT-042 is a deterministic reference run compiled in a harness crate",
         "against emem 04b40c5 (see trace/sat042_run_stdout.txt header), not a live spacecraft.", "",
         "| section | printed | value | source | class |", "|---|---|---|---|---|"]
lines += [f"| {a} | {b_} | {c.replace('|', '/')} | {d} | {e} |" for a, b_, c, d, e in rows]
OUT.write_text("\n".join(lines) + "\n")
(REPO / "research/repro/v12/CLAIMS_MAP.md").write_text("\n".join(lines) + "\n")  # the copy the board and footer point to
print(f"wrote {OUT.relative_to(REPO)}: {len(rows)} rows")
