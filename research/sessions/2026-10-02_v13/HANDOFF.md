# Handoff: v13 EMEM A0 poster (2 Oct 2026)

Branch `claude/tender-planck-clvh1p`. Everything below is pushed. Start with `AGENTS.md`, then this file.

## State
- **Board:** `poster/src/poster.v13.html` (+ .css, .layout.json, allowlist, tokens.json), built by `python3 poster/build_v13.py`
  (17 gates; all passed at `efcc4b5`). Outputs `poster/emem-poster-A0.pdf`, `emem-poster-preview.png`, `emem-poster-A0-300dpi.png`,
  `poster/build_v13_report.json`. Running text 815 words (cap 830).
- **Composition (v13.1):** header (title, hero, sub-hero, drift block, byline, F1 scene + VIEW THE DEMO QR); spine p1 (F2, R5 numbers);
  left: p2 eight answers (F3), p3 failure ladder (F4), Questions, Threat (d_threat); centre: p4 evidence object (F5), p5 mutation matrix (F6),
  p6 wrong pixel (F7); right: p7 ladder (F8), p8 timeline (F9), p9 One address (F13), p10 Token family (F14); bottom: p12 ecosystem (F11),
  p13 prior art (F12), conclusion. Panels 9 Rondônia, 10 vectors, 11 cost were removed on the user's request (figures still in `poster/fig/v13/`).
- **IN FLIGHT when this was written:** an agent is adding a COMPACT SAT-042 STRIP (user's choice) as p11 in the right column:
  `poster/figs_v13/f15b_sat042_strip.py` (193.5 x 70 mm) + a `height_mm` parameter on `f8_ladder.py` (ladder shortened to about 110 mm)
  + live p11 markup replacing `<template id="p11-sat042-off">` in the HTML (kicker "Extending verification from observations to execution",
  subtitle "SAT-042 is a scripted pass in emem's test harness, not a spacecraft; run on 30 Sep 2026.", scope "Reference harness, no spacecraft
  enrolled; the gate binds the value digest only."). If those files are absent, redo that step; the full F15 figure and its claims rows
  (`research/v13/12_claims_map_additions_F13-15.json`, `..._board2.json` SAT.*) already exist.
- **R5 (main result):** `research/repro/v13/r5/` final (2,794 trials; `results.json` final: true; `results.md`). The build prints R5 lines
  automatically from results.json.
- **Reviews:** `research/v13/13_review_fixes.md` (23 confirmed findings, all applied at `99b10aa`). Research reports: `research/v13/01..11`.
- **Site for the QR codes:** `docs/` (built by `python3 poster/build_site.py`); live only after GitHub Pages (main, /docs) is enabled and
  this branch is merged to main.
- **Seal of the previous print (v13.0, commit e66c3ba):** pointer note `7jr4zw2tq7slvbsyzbyxxzwwii`, 21-step track
  `hepwyxdhiwckwi7qahkuvya2b4` (21 of 21 in ememdemo, log entry 2,591,968), linked from `docs/r/` and `poster/README.md`.
  **The v13.1/v13.2 print is NOT yet re-sealed.**

## To finish (in order)
1. Confirm the SAT-042 strip landed and `python3 poster/build_v13.py` passes all 17 gates; look at the right column crops.
2. Re-seal: `research/repro/v13/track/make_track_v13.py` composes the track; add the Berlin cell step `emem:cell:defi.zb655.yaka.pUxe`
   and (optionally) its 16 facts; publish a pointer note over the new `poster/emem-poster-A0.pdf` at its commit (`research/repro/v8/publish_note.py`
   with the poster key; see `poster/README.md` v11 and the v13 seal commit `fa5de75` for the exact commands: probe the raw PDF URL with the
   ememdemo cutter, verify chunk hashes, publish with `--flat --go`, run `make_track_v13.py <board_note_cid>`, dry-stamp and rehearse in
   ememdemo via `scratchpad/ememify/publish/js/render.mjs`, publish, verify live), then update the BOARD TRACK block in `tools/site/site.mjs`,
   rebuild the site, update `poster/README.md`, commit, push.
   The poster key lives only in the session scratchpad (`scratchpad/poster-key/agent_identity.json`, pubkey njedkglt…); if the scratchpad is
   gone, a new key means a new namespace: regenerate and re-publish the pointer notes the track cites, or skip the seal.
3. Author items: enable GitHub Pages, merge to main, print proof at 100 %, organiser board size, ChatGPT listing screenshot,
   and the emem-side fixes the board states as open (date substitution, /v1/ask coordinates, README witnesses wording, broken install routes).

## Rules that must hold
No em dashes; en dashes only in numeric ranges; no banned words without a BLAKE3-bound allowlist entry; every number on the face needs a
claims-map row (`research/v13/12_claims_map*.json`); nothing under 14 pt; numbers from data files only; no model identifiers on the face,
on the site or in commit messages; never commit keys.
