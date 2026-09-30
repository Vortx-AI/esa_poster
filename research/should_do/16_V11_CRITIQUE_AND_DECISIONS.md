# v11: critique of v10, what changed, and what is still open

Written 30 Sep 2026 for the Agentic AI for Earth Observation workshop, Poster Session 1 (19 Oct, 17:00 to 18:30,
B. von Langenbeck, 23 posters). The v10 board is archived unchanged in `poster/archive/v10/`.

## 1. Verdict on v10

v10 was accurate. Two independent checks reproduced its mechanism claims, and every printed token resolves.
But it read as an audit log, not as an invention, for five reasons.

1. **It indexed about a fifth of emem.** It showed one NDVI fact, one pixel bug and the handoff trials.
   It left out the fact plane and note plane split, signed absence, as-of recall, the token algebra beyond
   fact/raster/cube, entities, change attribution, contradiction detection, the guard, derive with
   recomputation, trees and bundles, the plane conformance endpoint, the clean-room third-party verifier,
   the cross-vendor decoder, the 168 algorithms, the 114 tools and the distribution surfaces.
2. **There was no architecture figure.** A reader walking past could not see what emem is in five seconds.
3. **Self-refutation took the best space.** "emem retired its foundation-model encoders" sat under a title
   that says "over Foundation-Model Embeddings", and a panel titled "Where emem lost" printed red
   "refuted" labels. Honesty is an asset. Presented as defeat, it read as a withdrawn paper.
4. **Internal vocabulary.** "Ememify", "pointer.v1", "since acceptance", "attester_only", fourteen numbered panels
   whose numbers collided with the § step numbers.
5. **Density.** About 3,200 words at roughly 15 pt on A0; no panel could be read from two metres.

The claims audit also found six mismatches, six unsourced numbers, ten partial claims and two stale ones.
They are listed in `research/audit_v11/poster_evidence_audit.md` section A. Every one that survives into
v11 is fixed; the unsourced ones were removed (see `15_V11_CLAIMS_MAP.md`, last section).

## 2. What v11 is

One claim, one figure, six contributions, four results, then the objections and what emem establishes.

| band | content | job |
|---|---|---|
| header | exact accepted title, both authors, DOI, code, commit, QR to /verify | identity |
| thesis | the problem (agents drift apart) and the invention in one sentence | the 5-second read |
| hero | the whole protocol around one real Sentinel-2 observation, every value as signed | the 30-second read |
| live strip | six live counts | scale, not a demo |
| C1 to C6 | address, two clocks, the two planes, the token algebra, trustless verification, recomputable computation; each with its formula and a measurement | the invention register |
| agents | eight jobs and four uses in the wild | "much more than a hash" |
| R1 to R4 | the mutation test (17 cases × 9 depths); agreement is not evidence; a token helps only when checked; the records located emem's own error | science |
| objections | eight, tagged agreed / reframe / rebuttal | peer review in advance |
| identities, try, evidence | what emem establishes and what it does not; one-line install and a QR to R1; the signed track | honesty and a next step |

The prose follows the emem convention: no em or en dashes in running text, no tell words, short sentences.
The build fails if either rule is broken, if the board is not exactly one A0 page, or if content reaches
the footer (`poster/build_v11.py`).

## 3. Is it wise to print refutations? Yes, in a different shape.

The audience is ESA and BIFOLD researchers, with guardrail, evaluation and traceability posters on both sides.
They will ask the hard questions in the first minute. A board that answers them first earns trust, and one that
hides them loses it. But a poster is an argument, not a lab notebook.

- **Keep on the board, reframed:** each refutation that a visitor would raise becomes an objection with an answer.
  "Where emem lost" became three objections (BM25, token cost, small n). "emem retired its encoders" became the
  reframe "the memory outlived its encoders". "What is not established" became the Scope box, and later the table "What emem establishes".
- **Promote to a result:** the pixel error. It is the strongest evidence that the design works: the records
  themselves located and dated emem's own bug. v10 filed it as a defect; v11 prints it as R2.
- **Move to the repository:** the 36-defect list, the authors' scorecard and the nineteen withdrawn claims. The
  footer points there by name, so nothing is hidden.

## 3b. Revision after the field-map critique (same day)

The field map (`10_EVENT_FIELD_MAP_AND_CRITIQUE.md`) asked for an adversarial mutation test scored by false
acceptance, an ablation, and a clear separation of what a signature does and does not establish. All three are now
on the board: R1 (`research/repro/v11/`), the leave-one-out line in its caption, and the "What emem establishes"
table. R1 replaced the drift taxonomy, whose real cases are now R1 rows marked "seen in production". Details and
the points v11 declined: `17_V11_RESPONSE_TO_FIELD_MAP.md`.

## 4. Open before printing (owner: authors)

1. **Commit the missing runs** or keep them off the board: the Qwen2.5-3B arm of §22, the derive response behind
   §11, the tampered-mirror and local-node runs, the Earthdata and Copernicus observations.
2. **Merge and re-scan.** The R1 QR opens `github.com/Vortx-AI/esa_poster/tree/main/research/repro/v11`, which resolves only after this branch is merged into `main`.
2. **Reseal.** The seal QR on v11 still opens the v10 evidence track `7n7qogvn…` (28/28). All § steps cited on v11
   are steps of that track, so the QR is valid. To seal v11 itself: render `board.jpg` from the v11 PDF with the
   seal box as is, publish a board pointer note at the v11 commit (as in `research/repro/v8/pub/b_v10/note.md`),
   append it as step 29 of a new track, re-check it in ememdemo, and regenerate `fig/v11/qr_seal.svg` from the
   new track URL. The build checks every QR file exists; re-scan all three QRs on the print proof.
3. **118 vs 116 wired measurements.** The agent card and /v1/materializers disagree. Either fix upstream or print 116.
4. **Upstream doc defects found by the inventory:** the agent card still lists geotessera as a live embedding band;
   the CHANGELOG 2.4.2 entry says 113 tools and 171 paths. Listed in `research/audit_v11/emem_capability_index.md`.
5. **Print proof.** WeasyPrint builds the board (`python poster/build_v11.py`). Before sending to print, open the PDF at
   100 % and check the hero's smallest labels (about 4 mm cap height, readable at 1 m). `render.mjs` (Chromium) still
   renders `poster.html` if the print shop prefers a Chromium-made PDF.
6. **Zenodo v0.2.** The paper is v0.1.0 and the board describes whitepaper v3. Minting v0.2 before 19 Oct would let
   the header DOI and the method line agree.
