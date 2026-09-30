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
