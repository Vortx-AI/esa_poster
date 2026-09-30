> **v9 (2026-09-30):** the board track is now `njedkglt/d7aoricjy4rnm4g5ykil6a4zre.md`, with 28 of 28 steps checked. The board adds:
> - a drift taxonomy;
> - a pre-registered raw-band run, in which emem's raster tool substituted dates (defect 27);
> - "since acceptance": emem retired its foundation-model encoders;
> - "where emem lost".
>
> Do not claim "no memory poisoning". emem's own reader wrote 162 of 200 wrong-pixel records, and entity referents are not bound by bytes. Do not claim OS traces are live: the device gate admits no real hardware.

> **v8 (2026-09-30):** the poster is an emem track (22 steps, 22/22 in ememdemo): `emem.dev/memories/by_attester/njedkglt/qw5zd3de2lyo532g66kva5t5oe.md`, head `zvy3kzpm4a4nkhrnb3h5gtkf7i`. See `poster/README.md` (v8). The v8 findings are:
> - The pixel-rounding audit: 162 of 200 pre-fix S2 records carry a neighbouring pixel's DNs.
> - The two-LLM pre-registered handoff. Claude Haiku as B declined 5 of 5 forged tokens. The Qwen2.5-3B arm misapplied the rule and did not decline forged tokens.
> - A 15-link trace, 17 checks, run with no emem code.
> - New emem defects 23–26 are in `do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md`. The one that matters for the demo: rasterset resolve returns no receipt.

# Research state

> **v3 (2026-09-29, later):** four audits produced [`should_do/09_INVENTION_REGISTER.md`](should_do/09_INVENTION_REGISTER.md), which supersedes the "poster spine" below. The poster is rebuilt on its eight contributions (A1–A8) and three findings (B1–B3). Correction: geo.qa is run by Vortx AI, so it is not an independent witness.

Snapshot: 2026-09-29 (v2). This supersedes the 2026-09-30-dated v1 snapshot.

## What changed in v2

- Every mechanism claim was checked against the emem source at HEAD `64cfae5`.
  Results: [`should_do/04_VERIFIED_CLAIMS_LEDGER.md`](should_do/04_VERIFIED_CLAIMS_LEDGER.md).
- **16 errors in the earlier concept** were found and corrected:
  [`do_not_use/03_CORRECTIONS_TO_CURRENT_CONCEPT.md`](do_not_use/03_CORRECTIONS_TO_CURRENT_CONCEPT.md).
- The core invariant was **reproduced independently** against production with stock `blake3`,
  using no emem code: [`repro/`](repro/README.md).
- The measured results were mined, with their caveats:
  [`should_do/05_EVIDENCE_AND_NUMBERS.md`](should_do/05_EVIDENCE_AND_NUMBERS.md).
- The device/agent story was separated into shipped vs simulated vs roadmap:
  [`should_do/06_HOW_DEVICES_AND_AGENTS_CONNECT.md`](should_do/06_HOW_DEVICES_AND_AGENTS_CONNECT.md).
- The event facts are confirmed: no official format; the people in the room; the hackathon.
  See [`should_do/07_EVENT_FORMAT_PEOPLE_AND_ACTIONS.md`](should_do/07_EVENT_FORMAT_PEOPLE_AND_ACTIONS.md).
- Related work from 2025–26: [`should_do/08_RELATED_WORK_2025_2026.md`](should_do/08_RELATED_WORK_2025_2026.md).

## What the invention is, in its sharpest defensible form

> **Agents hand each other the *address* of a signed physical observation instead of a
> sentence about it. Any receiver can fetch the exact bytes, re-hash them to the address,
> and check the signature offline, without trusting the sender, the server's honesty,
> or the model that wrote the sentence.**

The content address is the mechanism. The invention is **the unit being exchanged between
agents**: a typed, place- and time-keyed, signed observation, with a family of token types
that extends it to fields (`raster`), fields through time (`cube`) and sets of fields
(`rasterset`).

## Why this is more than a mechanism: the scientific finding

emem's own experiments produced a result that matters beyond emem:

> **When agents pass paraphrases, they can agree *more* and be *more wrong*.**
> Under compaction: accuracy 0/72, with the inversion supported at Fisher p = 0.035
> (pre-registered). In the paraphrase trap, "NDVI ≈ 0.49" raised agreement between Gemma
> and Qwen, and both took the wrong irrigation action. The token arm got it right.
> In handoff, prose was correct 2/20 times; the bundle 20/20.

That makes cross-agent agreement an unsafe signal of correctness. It is a failure-mode result
(the Manling Li keynote) and a collective-intelligence result (the James Zou keynote). **emem
is the fix we measured.**

## The real-world exhibit (re-verified today)

One Bengaluru cell, one band, and two answers, **both still verifiable**:

- `emem:fact:defi.zb493.xuqA.zcb5f:yqbolgeo…` resolves to **918.0 m**. Signed 2026-05-28;
  source: Copernicus DEM 90 m via Open-Meteo.
- `emem:fact:defi.zb493.xuqA.zcb5f:jzxzmvom…` resolves to **915.07 m**. Signed 2026-09-28;
  source: a Copernicus DEM 30 m COG.

The upstream changed. An agent holding the May token still knows exactly what it cited and
where that value came from. **Nobody staged this.** An external auditor found it in production.

## Honesty that is part of the pitch

- The authors' published scorecard **refutes two headline claims**: "beats plain context" and
  "beats BM25".
- A single token costs 9.5× the LLM tokens of the value it names. Only the bundle handle is flat.
- Hardware attestation and anything in orbit are **not shipped**.
- The comparison against peer memory products is **untested**.

Printing a compact "what holds / what doesn't" panel will earn more trust from this audience
than any adjective.

## Recommended poster spine (A0 portrait; confirm with the organisers)

1. **Title band.** The exact accepted title; both authors; Vortx AI; DOI; the emem commit hash.
2. **The claim.** One sentence: "Hand over the address of the evidence, not a sentence about it."
3. **Mechanism, with real bytes.**
   - The 541-byte fact → BLAKE3 → the 52-character CID → the token.
   - Resolve, re-hash, 409 on a wrong cell, receipt verified offline.
   - Stock `blake3`, 3 lines.
4. **Hero exhibit.** One place, two answers: the 918.0 / 915.07 drift.
5. **The experiment.**
   - Agreement ≠ correctness (0/72, p = 0.035).
   - The paraphrase trap.
   - Handoff: prose 2/20, BM25 20/20, bundle 20/20.
   - Long run: citable 100% vs 0%.
6. **From point facts to fields.**
   - The ladder `fact → raster → cube → rasterset`, with strength labels.
   - Embeddings (Tessera, 128-D) signed as `model_output` facts.
7. **What holds / what does not / open work.** Include the edge story here, labelled
   *simulated*: 0.167% of a frame; the forged fact refused.
8. **Reproduce this.**
   - A QR code to `research/repro`.
   - The `curl` + `blake3` recipe.
   - `claude mcp add … emem.dev/mcp`.

## Decisions pending from the authors

- Headline wording: "Hand over the address, not the sentence" vs "The satellite observation
  can outlive the agent". v2 recommends the first: it is the one the data supports directly.
- Whether to mint Zenodo v0.2 aligned with whitepaper v3 before 19 Oct.
- Which live field token to print (the raster endpoints returned 504 on 2026-09-29).
- Whether to join the 22 Oct EVE MCP hackathon.

## The test for every poster element (unchanged)

Keep an element only if a scientist can answer one of these after seeing it:

1. What object did emem introduce?
2. What invariant does it enforce?
3. What mechanism makes the invariant checkable?
4. What can a second agent do that it could not safely do with prose alone?
5. What does the protocol explicitly not prove?
