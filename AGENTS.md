# AGENTS.md: working on the EMEM poster

This repository holds the A0 poster for "EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents
over ~~Foundation-Model Embeddings~~ Satellite Observations and Signed Execution Traces" (Agentic AI for Earth
Observation, Berlin, Poster Session 1, 19 Oct 2026), and all the research behind it. The current board is v12.

## Start here

1. `research/sessions/2026-09-30_v12/README.md`: what v12 changed, why, and what stays off the board.
2. `research/should_do/19_V12_CLAIMS_MAP.md`: every number on the v12 board and its source (generated; no row, no number).
3. `research/repro/v12/`: live EO evidence (780 verified facts), the SAT-042 trace run, the v11.2 section audit.
4. v11 history: `research/sessions/2026-09-30_v11/`, `research/should_do/15_V11_CLAIMS_MAP.md`, `18_V11_PROCESS_AND_HANDOFF.md`.

## Build

```
pip install -r poster/requirements.txt
python poster/build_v12.py              # reruns R1, redraws figures, renders PDF and PNG, runs the gates
python poster/build_v12.py --no-figures # layout only
python research/repro/v12/scripts/claims_map_v12.py   # regenerates the claims map and checks the board prints it
python research/repro/v11/mutation_suite.py   # R1 alone, offline
```

Edit `poster/src/poster.v12.html` (never `poster/poster.html`, which is generated). Figures: `poster/make_figures_v12.py`
draws every panel 1:1 at its board size and fails on text under 15 pt, clipped or overlapping labels. v11 sources stay
in `poster/src/poster.v11.html` and `poster/make_figures_v11.py`; the v10 board is in `poster/archive/v10/`.

## Rules the build enforces (it fails, never warns)

- one page, 841 × 1189 mm; content ends at least 2 mm above the footer;
- no em dashes, no en dashes outside numeric ranges, no tell words in running text;
- every QR file present; no overlapping or clipped figure labels;
- an unknown gate result is a failure.

## Conventions

- emem is AI infrastructure; satellites are the input. Short sentences.
- A research poster, not an audit: limitations go in the Discussion and the guarantees table as short scope
  statements. Defect lists, scorecards and withdrawn claims stay in `research/`.
- Numbers are copied from measurement files, never from prose. Counts carry their units and their date.
- Never commit signing keys (`.gitignore` covers the usual names).
