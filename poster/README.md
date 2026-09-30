# The poster: A0 portrait, print-ready

| file | what it is |
|---|---|
| `emem-poster-A0.pdf` | print file, 841 × 1189 mm, fonts embedded (IBM Plex, OFL) |
| `emem-poster-preview.png` | 3179 × 4494 px preview |
| `poster.html` | the source; edit this, then re-render |
| `render.mjs` | renders the HTML to the PDF and PNG (needs `playwright-core` and Chromium) |
| `qr-*.svg` | QR codes: the repro folder, emem.dev/verify, the DOI |

Every claim on the poster is traced in `../research/should_do/04_VERIFIED_CLAIMS_LEDGER.md`
and `05_EVIDENCE_AND_NUMBERS.md`. The printed tokens and bytes were re-verified live on
2026-09-29 (`../research/repro/`).

## v9: raw bands, drift taxonomy, since acceptance (30 Sep 2026)

The seal now opens this track:

https://vortx-ai.github.io/ememdemo/?s=https%3A%2F%2Femem.dev%2Fmemories%2Fby_attester%2Fnjedkglt%2Fd7aoricjy4rnm4g5ykil6a4zre.md

- It has 28 steps, and ememdemo checked 28 of 28 at 14:08 UTC on 30 Sep.
- Head: `dr2tllnicvm32wvgziaw6ad57u`.
- It is logged as entry 2,567,387, the next entry after the log size stamped on it.
- board.jpg (seal blank) is at commit `4a516cc`; its sha256 starts `70b4e4bd…`.
- The board pointer is `v2lbozmd…`, and the evidence pointer (§22) is `7o6t4xpu…`.

What changed from v8:

- **Lead.** The claim is restated: raw observations, addressable by place, band and time. The evidence survives a handoff, and agents cannot write observations.
- **Drift taxonomy (7 real cases).** Six are located by one field of the record. The seventh, the referent (the Maasvlakte entity), is not caught.
- **Raw-band run.** It was pre-registered (blake3 `30d8a1a1…`), with n = 10 runs of Claude Sonnet 5.5 and emem's full MCP.
  - The result is reported as it came out. emem's raster tool served the 25 Sep scene when asked for 23 Sep (defect 27).
  - One run reached the containing pixel and got ΔNDVI −0.015. None said "greener".
  - Data: `research/repro/data/v9/rawband/`.
- **Since the paper was accepted.** Clay, Prithvi, Galileo and JEPA-v2 were removed, and TESSERA is frozen. The panel explains why a recomputable raw band read differs from an `attester_only` embedding, and notes that the OS-trace device gate admits no real hardware yet.
- **Where emem lost.** It shows the authors' scorecard (§19) and the README results table (§25), with their scope stated.
- **New steps.** Steps 23–26 are doc rows at emem `18adb67`, and 27–28 are the 23 Sep post-fix B04/B08 facts.
- **Traffic.** It is now one footer line.
- **Defects.** New ones, 27–31, are in `research/do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md`. They cover:
  - 27: the raster date substitution;
  - 28: the README's 27.8 % / 1.4 % does not reproduce p = 0.035;
  - 29: read tools sign new records;
  - 30: the "independent witnesses" wording;
  - 31: entity receipts are v1, which ememdemo rejects.

## v8: the poster is itself an emem track (30 Sep 2026)

Every `§n` on the board is step n of one signed emem track. Scan the seal QR, or open:

https://vortx-ai.github.io/ememdemo/?s=https%3A%2F%2Femem.dev%2Fmemories%2Fby_attester%2Fnjedkglt%2Fqw5zd3de2lyo532g66kva5t5oe.md

ememdemo re-checks all 22 steps in the browser, recomputes the hash chain to its head
`zvy3kzpm4a4nkhrnb3h5gtkf7i`, and checks the note's inclusion in the emem log
(written after log size 2,567,013; logged as entry 2,567,020). Last checked 30 Sep 13:38 UTC: 22 of 22.

| file | what it is |
|---|---|
| `board.jpg`, `board.pdf` | the board with the seal box **blank**: the bytes the §1 pointer note hashes (sha256 `8d4de3b3…69eb2`, commit `624c78b`) |
| `emem-poster-A0.pdf`, `emem-poster-preview.png` | the print: the same board plus the filled seal (QR, track, head, sha256, log position) |
| `fig/seal_qr.png`, `fig/seal_qr.txt` | the seal QR and the URL it encodes (decoded from the render and checked) |
| `make_figures.py`, `make_figures_v8.py` | all figures, from `../research/repro/data/` |

The hash cycle has three steps. First the board is rendered with the seal blank. Then the §1 pointer hashes that board. Then the track is written, and only then is the seal filled. A file cannot contain its own hash, so the seal is the only part of the print outside the hashed bytes.

The §-steps are:

| § | what |
|---|---|
| 1 | this board (`3vqnyosg…`) |
| 2–3 | the Earth Search B08 and B04 COG pointer notes |
| 4 | the NDVI fact |
| 5 | the B04 raster |
| 6 | the cube |
| 7 | the pre-fix record |
| 8 | CHANGELOG line 68 |
| 9 | TESSERA |
| 10 | Clay |
| 11 | the derived value |
| 12–13 | the two elevation records |
| 14 | temperature |
| 15 | the absence record |
| 16 | the bundle of 8 |
| 17–20 | rows of the emem docs at `213e273` |
| 21 | the trap value |
| 22 | our measurements |

The notes are signed by the poster key `njedkglt…`, namespace `/memories/by_attester/njedkglt/`.

- Scripts: `../research/repro/v8/`: `make_track.py`, `publish_note.py`, `trace_fact.py`, `verify_bundle.py`.
- Publish logs: `../research/repro/v8/pub/*/publish_log.json`.

Two review passes ran before the seal:
- **Fact check.** Among the fixes, the poster now reports the pre-registered Qwen2.5-3B arm, which went against us. It also labels the rounded-prose p-value as exploratory, and corrects the scale bar, the cell size and the scope of the proof file.
- **Expert language critique.** It removed slogans and jargon, stated the AWS and Planetary Computer file mismatch, and set type to at least about 14 pt.

Any change to the board text now means: re-render → commit → republish §1 → rebuild and republish the track → re-fill the seal.

## v7 distribution + reasoning edit — 30 Sep 2026

This pass moves the poster from “protocol internals” to the broader research claim that emem is already a live **distribution layer for citeable physical-world evidence across agent runtimes**.

- Added the precise split between **lookup identity** and **content identity**:
  - `cell64 × band × tslot` finds where/what/when.
  - `fact_cid = BLAKE3(emem-CBOR(record))` identifies exactly which signed record.
  - `emem:fact:<cell>:<cid>` is the handoff reference.
- Reframed the EO path as **keep the source scene upstream; move the address into reasoning**.
- Added a live-runtime strip: **ChatGPT @emem, Claude.ai / Claude Code, Dify, MCP, A2A, Python/TypeScript and framework agents**.
- Made the accepted-title phrase **“over Foundation-Model Embeddings”** visible through the live **Tessera 128-D → model_output fact → fact_cid** path.
- Added the measured bundle mechanism to long-horizon handoff: up to 256 fact references under a compact handle; explicitly notes that individual fact tokens are not a context-compression claim.
- Renamed the core sections to technical nouns: **CONTENT ID, HANDOFF, FIELD / CUBE / EMBEDDING, CLAIM CHECK**.
- Turned the single QR into a conference experiment: get a token in one agent, paste it into another, resolve/re-hash/verify and compare the cited record.
- The underlying science remains frozen to the 29 Sep evidence set; live integration availability was re-checked on 30 Sep.

The HTML source changed; re-render PDF/PNG before review or print.

## v5 wall edit — 30 Sep 2026

The A0 source was simplified after the research audit without deleting the underlying work.

- **Drift is now the opening problem:** a real 0.487154... NDVI became “≈ 0.49”; two models agreed and crossed the action threshold incorrectly.
- The wall narrative is verb-led: **OBSERVE → ADDRESS → HAND OFF → RESOLVE → VERIFY → CONTINUE**.
- Eight contribution panels were reduced to four core mechanisms: **ADDRESS, HAND OFF, FIELD, VERIFY**.
- Signed absence, disagreement, derivative checking and the transparency log remain as a compact consequences strip and in the research files.
- The agent-correction graph was removed from the wall version; the evidence remains in the repository.
- The token-family table was reduced to the EO ladder: **fact → raster → cube**.
- Only **one QR** remains, pointing to **https://emem.dev**. Source, paper, verify and reproduce should be reachable from there.
- The exact submitted paper title is restored.
- The generated PDF/preview must be re-rendered from `poster.html` after this source change.

## Structure (v4: the complete system, with figures made from real emem data)

1. **Lead.**
   - The problem: agents cannot know they mean the same observation.
   - emem's answer, and the one verification rule.
   - The token family, with each member's strength.
2. **Fig. 1 — the life of one observation.** One real NDVI fact (`oj5cecci…`, Keylong) followed through all seven stages:
   upstream S2 scene → materialised DNs and offset → address (cell64, tslot) → content (1,115 B → BLAKE3)
   → signed batch and RFC 6962 log → served with a receipt over MCP/REST/A2A → passed as a token and checked by the receiver.
   Underneath: the four layers (address, content, object, memory).
3. **Fig. 2 — EO figures from signed data.**
   - 2a: true colour from the signed B04/B03/B02 grids.
   - 2b: NDVI we computed from the signed B08/B04 grids, with the fact's cell marked.
   - 2c: a 5-member `emem:cube:`, each member labelled with the date asked for and the scene actually used. It shows a cloudy member as a stated limit.
4. **A1–A8 contribution panels.** Mechanism, live evidence, prior art, what is new, and the limit. A2 and A8 carry data charts: the two-clocks step chart, and log growth decoded from sampled signed entries.
5. **B1** (agreement ≠ correctness), **B2** (the real agent correspondence graph, 99.1% of cited tokens still resolve) and **Reproduce**.

## Figures

`make_figures.py` rebuilds every figure in `fig/` from `research/repro/data/`. All inputs were fetched from emem.dev on 2026-09-29, and every raster artifact was re-hashed before use.

## Before printing

- [ ] Merge this branch to `main`. The repro QR code points to
      `github.com/Vortx-AI/esa_poster/tree/main/research/repro`.
- [ ] Re-run `python research/repro/verify_fact.py <token>` on both printed tokens.
- [ ] Re-check the log size: `curl -s https://emem.dev/v1/log/witnesses | jq .current_tree_size`.
      It was 2,537,510 on 29 Sep; the poster says 2.54 M.
- [ ] Confirm the board size with the organisers. A0 portrait is assumed. If the board is
      landscape, re-flow rows 1 and 3–4 into three columns.
- [ ] Print matte, unlaminated (push pins). Also print 50 A4 copies of the preview as a
      handout.

## Re-render

```sh
npm i playwright-core
node render.mjs    # writes emem-poster-A0.pdf and emem-poster-preview.png
```
