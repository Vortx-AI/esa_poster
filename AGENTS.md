# AGENTS.md: working on the EMEM poster

This repository holds the A0 poster "EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol" (the programme lists it
with "for AI Agents over Foundation-Model Embeddings"; Agentic AI for Earth Observation, Berlin, Poster Session 1,
19 Oct 2026), and all the research behind it. The current board is v13.10 (v13.9 plus the recovered v10 lead, memory-as-coded box and full trace, handoff emphasis, the orbit design lines and the emem wordmark; see `poster/src/poster.v13.layout.json` v13.10_notes).

## Start here

1. `research/v13/14_UNIFIED_POSTER_BRIEF.md`: current narrative and printed copy. `research/v13/12_FINAL_BRIEF.md` retains the base grid, original evidence specification and gates.
2. `research/v13/12_claims_map.json` plus `research/v13/12_claims_map_additions_*.json`: every number on the v13 board
   and its source (no row, no number; `extend_print` entries add printed forms of existing rows).
3. `poster/build_v13_report.json`: the last build's gate results, layout deviations from the brief and word counts.
4. v12 history: `research/sessions/2026-09-30_v12/README.md`, `research/should_do/19_V12_CLAIMS_MAP.md`, `research/repro/v12/`
   (live EO evidence, 780 verified facts, the SAT-042 trace run, the v11.2 section audit).
5. v11 history: `research/sessions/2026-09-30_v11/`, `research/should_do/15_V11_CLAIMS_MAP.md`, `18_V11_PROCESS_AND_HANDOFF.md`.

## Build

```
pip install -r poster/requirements.txt   # Chromium is in /opt/pw-browsers
python poster/figs_v13/<figure>.py      # each v13 figure, drawn 1:1 into poster/fig/v13/ (svg, png, labels.json)
python poster/build_v13.py              # board: inlines figures and QRs, renders PDF + PNGs with Chromium, runs every gate
python poster/build_v13.py --r1         # re-runs R1 first; --allowlist-candidates prints banned-word hits with their BLAKE3
python poster/build_v13.py --variant 300of300   # the second print variant (outputs carry -300of300); default is 0of300
python poster/figs_v13/f2_spine.py --variant 300of300   # f2 and f6 also draw <name>.300of300.svg for that variant
python research/repro/v11/mutation_suite.py   # R1 alone, offline
```

Edit `poster/src/poster.v13.html` and `poster/src/poster.v13.css` (never `poster/poster.html`, which is generated).
The printed face uses three QR tasks (Try it, Inspect, Connect & Reproduce); all six web routes remain. Connect opens /use/, which links the methods and tests.
Colours: `poster/src/tokens.json`. The `brand` orange marks the emem identity (the wordmark's dash, the tagline's "decode with AI.") on the navy header only, never data: `harm`, a near hue, means corrupted evidence. The wordmark's dash is drawn in CSS because the face bans the em dash character. Banned-word allowlist (bound to sentences by BLAKE3): `poster/src/poster.v13.allowlist.json`.
Deliberate departures from the brief's block rectangles, each with its reason: `poster/src/poster.v13.layout.json`.
Two print variants of the handoff result (`data-variant="0of300"` / `"300of300"`): 0of300 prints the pre-registered
false acceptance (B acted on corrupted evidence, 0 of 300); 300of300 prints the same trials as "did not act on" with the
declined / genuine split (`research/repro/v13/r5/not_acted_split.py`). Never call the complement "declined": 36 of the
300 used the genuine record.
R5 lines (`data-mode="r5"`, `{R5.*}` placeholders) print only when `research/repro/v13/r5/results.json` is final; the
switch is in the build. The matched baseline (pre-registration addendum 2, results in
`research/repro/v13/r5/results_addendum2.md`, rows `R5.matched.*`) is printed in panel 1's ablation strip and scope;
`research/repro/v13/r5/addendum2/replay.py` re-checks and re-scores its archived agent trials from any checkout path. v12 sources stay in `poster/src/poster.v12.html`, `poster/build_v12.py`, `poster/make_figures_v12.py`;
v11 in `poster/src/poster.v11.html` and `poster/make_figures_v11.py`; the v10 board is in `poster/archive/v10/`.

## Rules the build enforces (it fails, never warns)

- one page, 841 × 1189 mm; content ends at least 2 mm above the footer; no box overflows its block or column;
- no text below 14 pt (computed in the browser, figure SVG included); kicker, mechanism and take lines at 24 pt, captions 17;
- no em or en dashes, no tell words, no banned word (report 10 section 5.3) without an allowlist entry; no board version
  or commit hash on the face;
- every number on the face (HTML and figure text) has a claims-map row; rows with a check re-run against their files;
- every QR decodes (OpenCV, 300 dpi render) to its `.txt` payload; every figure placed; colours are tokens; imagery at 300 ppi;
- an unknown gate result is a failure.

## Conventions

- emem is AI infrastructure; satellites are the input. Short sentences.
- A research poster, not an audit: limitations go in the Discussion and the guarantees table as short scope
  statements. Defect lists, scorecards and withdrawn claims stay in `research/`.
- Numbers are copied from measurement files, never from prose. Counts carry their units and their date.
- No service or code versions on the face (for example "emem.dev at 8e9b401"): they advance with every upgrade. The
  claims rows and `research/` keep them.
- Check depth shows as colour and check names, not as "L0" to "L3": EO readers take those for processing levels.
- Never commit signing keys (`.gitignore` covers the usual names).

The ecosystem figure is generated from `research/v13/ecosystem_manifest.json` by `poster/ecosystem.py`. Dates older than 28 days (LIVE claim rows and ecosystem rows), unqualified statuses and manually added SVG copy fail the build and CI. Run `python -m unittest discover -s poster/tests -v` after changing claim or ecosystem gates.
