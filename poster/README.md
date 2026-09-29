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

## Structure (v2: stand out, then prove, then adopt)

1. **Title band.** The accepted title, both authors, the DOI, the pinned commit, and "Open source · Apache-2.0" in the top-right corner.
2. **Hero (left).** A real Sentinel-2A L2A field over Keylong, Lahaul (25 Sep 2026): 443 × 453 px at 10 m, printed with its `emem:raster:` token.
   - All four band artifacts re-hash as MATCH, and the raster resolves with its spot-check passing.
   - One 9.55 m cell is marked with its signed NDVI fact; that receipt was verified offline with `ememdev`.
   - Provenance: `research/repro/hero_field.json`.
3. **Pitch (right).**
   - Headline: *Hand over the address, not the sentence.*
   - What emem is: Earth memory for AI agents.
   - What an agent gets today.
   - What changes inside the agent loop (the shipped skills).
   - Where emem sits in a GeoAI stack.
   - The open-source strip.
4. **Row A.** The invariant (real 509-byte fact → name; 409 on the wrong cell) · the receiver (resolve, re-hash, bind, verify, log) · the drift exhibit (918.0 → 915.07).
5. **Row B.**
   - The finding: the paraphrase trap, and the pre-registered 0/72 result at p = 0.035.
   - Handoff: 2/20 · 8/20 · 20/20 · 20/20, and the long-run citability result.
   - The boundary of the claim, plus the authors' own scorecard.
6. **Use it tonight.**
   - MCP · Python (`ememdev` 2.4.2) · Docker (`ghcr.io/vortx-ai/emem`) · stock-BLAKE3 check.
   - Each command was run from a clean install on 29 Sep.
   - QR codes: repro · source · paper.

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
