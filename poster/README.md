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

## Structure

The poster reads top to bottom. Each block answers one of the five questions in
`research/RESEARCH_STATE.md`.

0. The accepted programme title, both authors, the DOI, and the emem commit the claims are pinned to.
1. **Claim:** *Hand over the address, not the sentence.*
2. **The object and its invariant.** The real 918.0 m fact, its 509 emem-CBOR bytes,
   BLAKE3 → the 52-character name, and the token. Three rules: same bytes give the same
   name; a changed value gives a different name; a wrong place gives a 409.
3. **The receiver.** Resolve, re-hash, bind the place, verify the receipt offline, check the
   log. What crosses the trust boundary and what does not.
4. **Exhibit.** One place, two answers (918.0 → 915.07 after a real provider change), both
   still verifiable.
5. **The finding.** The paraphrase trap (a number line against the irrigation threshold),
   plus the pre-registered agreement ≠ correctness test (0/72, p = 0.035).
6. **Handoff.** prose 2/20 · dense 8/20 · BM25 20/20 · bundle 20/20; long run citable
   100% vs 0%.
7. **Fields and embeddings.** The token ladder with each family's strength; embeddings signed
   as `model_output`.
8. **Boundary of the claim.** What is checkable, what is not proved, and our own scorecard,
   refutations included.
9. **Reproduce this.** Seven lines of Python with stock `blake3`, the MCP install line, and
   three QR codes.

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
