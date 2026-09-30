# Work in progress and next steps (priority order)

Status legend: **P0** before printing (print deadline for 19 Oct), **P1** strengthens the science, **P2** upstream emem.

## P0

1. **Merge `v11-invention-board` into `main`.** The "Try it" QR opens `…/tree/main/research/repro/v11` and 404s until
   the merge. Then re-scan all three QRs on a print proof (header: emem.dev/verify; try box: the R1 folder;
   evidence box: the v10 track).
2. **Hostile read.** Run the adversarial reviewer over `poster/emem-poster-A0.pdf` against `15_V11_CLAIMS_MAP.md`.
   Any number without a row there comes off the board.
3. **Reseal v11 (optional but recommended).** Render `board.jpg` from the v11 PDF; publish a board pointer note at the
   v11 commit, as in `research/repro/v8/pub/b_v10/note.md`; append it as step 29 of a new track; check it in ememdemo;
   regenerate `poster/fig/v11/qr_seal.svg` from the new track URL (snippet in `18_` §4). Needs the poster signing key.
4. **Print proof at 100 %.** The smallest hero labels are about 4 mm cap height. Check R1's matrix labels and the R4
   axis labels from 1 m. If the print shop wants a Chromium PDF, `poster/render.mjs` renders `poster/poster.html`.
5. **Commit or keep off.** The Qwen2.5-3B arm of §22 and the derive response behind §11 have no committed raw logs.
   Neither is printed now; commit them before anyone re-adds them.
6. **Zenodo v0.2.** The header DOI is paper v0.1.0 while the method line says whitepaper v3.

## P1

7. **Models in the loop** (spec in `18_` §5): the same 17 mutations, 4 to 6 vendors, two runtimes, metrics false
   acceptance, false refusal, verification completion, obedience after refusal; pre-register and hash first.
8. **Extend R1** to the three uncovered mutation classes: changed unit, altered model checkpoint, altered embedding
   (for embeddings the honest outcome is "re-readable, not recomputable").
9. **Second record in R1.** One record and one band are exercised today; add a DEM record and a raster token.
10. **Deterministic outputs.** `mutation_matrix.json` stores a wall-clock timing, so every build rewrites it. Move
    timing to a separate file or round it, so diffs show only real changes.

## P2 (upstream emem)

11. Bind a provider-issued upstream identity (signed STAC item or checksum) into derived facts; the board prints that
    edge as "named" until then.
12. Version the verification policy; fix `docs/protocol.md` §3 (fact_cid is 32 bytes); fix the agent card listing
    geotessera as live; fix CHANGELOG 2.4.2 counts; reconcile 118 vs 116 wired measurements.
13. Independent operators for the log (the only other operator domain today, geo.qa, is also Vortx AI).
