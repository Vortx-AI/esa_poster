# Intel notes for v12 (gathered 2026-09-30, emem main 04b40c5, live emem.dev)

## Three esa_poster issues (open, 2026-09-30, avijeetsingh1)
- #5 P0 rebuild around adversarial evidence handoff: failure -> intervention -> FA/FR results -> minimal mechanism; cut internals ~40%;
  one invariant bytes->BLAKE3->CID; one path resolve->re-hash->compare; mutation table = focal point; 15-link traces behind QR.
  Must stay explicit: integrity is not truth; upstream correctness not guaranteed; entity identity not solved; complementary to guardrails/RAG/EO agents.
- #6 P1 adversarial benchmark (A prose, B raw value, C RAG, D emem token; 12 mutation types; 4-6 models; FA/FR/detection/latency/token overhead; n + CIs).
- #7 P1 bind upstream artifact identity; separate source integrity, derivation integrity, observation identity, entity identity, semantic correctness.
  Cites Keylong audit: 162/200 sampled pre-fix records selected the neighbouring pixel.

## Referential drift (whitepaper-v2 §1, §1.1; skill emem-referential-drift)
- "the words survive, the referent does not": each paraphrase/summary/handoff is a lossy re-encoding.
- Two directions: words move (identity: "north field" vs cell64) / values move (copied, rounded, re-summarised).
- World-side drift at a pinned address: Δz = Δ_env + Δ_sensor + Δ_geo + Δ_encoder + ε (world, instrument, misregistration, model, noise).
  Embedding facts carry encoder checkpoint + recipe so Δ_encoder is checkable; bi-temporality separates world change from memory change.
  Numeric split of Δz is NOT computed by the build (open work) -> do not claim attribution numbers.

## Memory encoding
- cell64: 64-bit id per ~9.55 m cell (like a token for text); fact keyed (cell, band, tslot); canonical CBOR -> BLAKE3 -> fact_cid; Ed25519 receipt.
- Band ontology: 43 cube slots summing to exactly 1792 dims (total_dims=1792 in live /v1/bands); 118 wired names ride fixed slots (parametric expansion).

## Tamper-provenance classes (bands.rs ProvenanceClass; whitepaper-v2 §7): seven defined, FIVE populated in the live 43-slot ontology
| class | tamper_evidence | rank | live slots |
| direct_sensor | recomputable_from_source | 5 | 6 (sentinel2_raw, sentinel1_raw, dem, cop_dem, gmrt, nightlights) |
| deterministic_index | recomputable_from_source | 4 | 7 (indices, terrain_derived, phenology, fourier, temporal_diff, multiscale) |
| estimator | rerunnable_from_signed_inputs | 3 | 0 |
| attested_execution | verified_execution_trace | 3 | 0 (device / operator-satellite class) |
| model_output | signed_model_checkpoint | 2 | 23 (geotessera, clay, prithvi, landcover, climate, ghsl, population, air_quality...) |
| human_curated | attester_only | 1 | 5 (overture, topology, protected, ecoregions, admin) |
| unclassified | attester_only (fails closed) | 0 | 2 reserved |
Live check 2026-09-30: /v1/bands -> Counter(model_output 23, deterministic_index 7, direct_sensor 6, human_curated 5, unclassified 2).

## Admission rules (substrates.rs AdmissionRule): ArchiveRecomputable (founding EO archive), OsTraceRequired (devices), CustodialRetention.

## ememdemo (github.com/Vortx-AI/ememdemo, bc06197): "Tokenise huge files for agents to use"
- `world: <place>` = every layer emem measures at one ~10 m cell (S2 optical+NDVI, S1 VV, Cop-DEM + GMRT, met.no/ERA5/MODIS LST, CAMS PM2.5, Overture,
  120-day cloud-masked S2 median composite as emem:raster token rebuildable pixel for pixel, algorithm registry), receipts checked in page, one emem:bundle.
- Cross-checks: Cop-DEM vs GMRT; NDVI recomputed from red/NIR vs stored index vs MODIS; air temp vs reanalysis. "Agreement is evidence; a gap is a finding."
  Marina Beach: recomputed NDVI equals stored index (0.0315).
- `cameras: London`: 12 street cameras, clip hashes, counts labelled as detector readings.

## Visual assets in emem repo: docs/media/world-{grand-canyon,interlaken,interlaken-columns,rondonia,semantic-cairo}.gif;
  docs/media/readme/{01-ask,02-verify,04-guard,10-research,11-two-agents,13-a2a,14-common-decoder,15-a2a-thread}.gif, 20-architecture.svg
