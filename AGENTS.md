# AGENTS.md: working on the EMEM poster

This repository holds the A0 poster for "EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents
over Foundation-Model Embeddings" (Agentic AI for Earth Observation, Berlin, Poster Session 1, 19 Oct 2026), and all
the research behind it.

## Start here

1. `research/sessions/2026-09-30_v11/README.md`: what was built, how, why, dead ends.
2. `research/sessions/2026-09-30_v11/NEXT_STEPS.md`: open work in priority order.
3. `research/should_do/18_V11_PROCESS_AND_HANDOFF.md`: files, build, gates, pitfalls.
4. `research/should_do/15_V11_CLAIMS_MAP.md`: every number on the board and its source. No row, no number.

## Build

```
pip install -r poster/requirements.txt
python poster/build_v11.py              # reruns R1, redraws figures, renders PDF and PNG, runs the gates
python poster/build_v11.py --no-figures # layout only
python research/repro/v11/mutation_suite.py   # R1 alone, offline
```

Edit `poster/src/poster.v11.html` (never `poster/poster.html`, which is generated). Figures: `poster/make_hero_v11.py`,
`poster/make_figures_v11.py`. The v10 board is in `poster/archive/v10/`.

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
