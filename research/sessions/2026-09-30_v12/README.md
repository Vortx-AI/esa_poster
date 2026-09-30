# Session 2026-09-30, v12: an Earth-observation research board

## What changed on the board (poster/src/poster.v12.html, built by poster/build_v12.py)

- Title: "over ~~Foundation-Model Embeddings~~ Satellite Observations and Signed Execution Traces". The strike is a red bar
  across the old phrase; the new phrase follows it on the same line.
- Header punchline: "When agents disagree, the satellite decides." with the sub-line "Every number an agent cites
  resolves to signed bytes, and re-reads to the pixel it came from."
- Reading order follows issue #5: the failure (compaction study), the idea (one invariant, one verification path, the two
  directions of referential drift), then evidence.
- Section 1 "One address, every satellite": one live Berlin cell with 15 products and 16 signed facts (4 signed
  absences) fanned from a real Sentinel-2C L2A chip; beside it the memory encoding (43 slots, 1,792 dims, encoder slots
  struck in the title's red) and the provenance-class ladder (five classes in use, two more defined).
- Section 2: the R1 mutation matrix as focal point, M15 as a production case (162/200), R4 memory on two clocks.
- Section 3: Keylong NDVI through two seasons from Sentinel-2A/2B/2C (141 facts) and a Rondonia EUDR-style grid
  (100 cells, 600 facts).
- Section 4: SAT-042, the reference spacecraft pass, as a seven-step sequence with the eight-layer chain, the tamper
  caught at seq 3 and drift-anchor scores.
- Bottom: guarantees table in issue #7's terms, three objections with answers, three conclusions, a repro QR.
- Removed from the board: the internals hero, the six contribution cards, the tools strip and vignettes, all
  "next step" wording, the commit hash in the header.

## Why the title says what it says

`research/repro/v12/trace/trace_truth.md`: execution traces are implemented and tested in emem (emem-trace, trace_gate,
orbital.satellite.v1 profile) and the trace verifier is live on emem.dev, but no spacecraft is enrolled, every platform
is a candidate and 0 of 43 live bands carry attested_execution. So the title claims satellite observations (live) and
signed execution traces (protocol plus live verifier), and the board states plainly that SAT-042 is a reference pass.
The ungated /v1/attest_cbor path (trace/gate_path_probe.rs) means the board does not claim that every device write
carries a trace.

## Evidence, and the limits that travel with it

- `research/repro/v12/data/`: 780 facts pulled live on 30 Sep 2026, each re-hashed, signature-checked and located in
  the log (eo_evidence_per_fact_checks.csv, all PASS). 266 were also recomputed from signed inputs; raster-read values
  were not re-read from upstream COGs. Sentinel-5P, Dynamic World, OpenET and VIIRS DNB returned band_not_in_registry
  and ERA5 returned upstream_error at the Berlin cell, so they are not on the board. Rondonia is point samples, not plot
  polygons, and not an Annex II statement.
- `research/repro/v12/trace/`: SAT-042 stdout (compiled in a harness crate against emem 04b40c5 because the full
  emem-primitives tree did not fit on disk; `cargo run -p emem-primitives --example satellite_downlink` itself was not
  run), filtered emem-trace and trace-gate tests, live registry state.
- `research/repro/v12/audit/`: the v11.2 section-by-section audit (Hostile EO Reviewer), live checks, issue texts.

## Build and gates

`python poster/build_v12.py` reruns R1, redraws every figure 1:1 at its slot (15 pt floor, clipping and overlap
asserted per figure), renders one A0 page and fails on footer overrun, em dashes, tell words or missing QR payloads.
`python research/repro/v12/scripts/claims_map_v12.py` regenerates `research/should_do/19_V12_CLAIMS_MAP.md` and asserts
the printed strings are on the board.
