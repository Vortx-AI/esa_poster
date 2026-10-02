# v13.7: restore the complete handoff, memory model and token family

Requested 2 October 2026. Historical visual sources were inspected as rendered PDFs, and their source scripts were compared with the current board:

- `2686b27a9947613b72c4690c4dc524839c6fbcd2`: full handoff experiment and section 10 token table; blue evidence, orange mutations and neutral hatched limits.
- `57a48a6a350dc61c221f01531c86ca795d82a07a`: section 1 Berlin image-to-products fanout, provenance colours and signed absences.

## What returned, and what made room

| Recovered contribution | New location | Material replaced or condensed |
|---|---|---|
| Actual source pixel, Agent A, five handoff forms, corrupting relay, Agent B's checks, measured outcomes and limit wall | Full-width panel 1 | Generic seven-stage workflow cards; obsolete R1/E0 side statistics stay in methods |
| Berlin cell connected to all 16 selected records from 15 products | Wide central panel 4 | Large wire-record field schematic; exact schema and bytes remain behind INSPECT |
| Full observation tuple, uncertainty, provenance and attestation association | Panel 9 | Small Berlin table, now given the wide column |
| Full 14-row token grammar and hash-preimage table | Panel 10 | Four generic token-family cards; concrete bundle/state checks remain in its caption |
| Complete drift-anchor rule including invalid uncertainty and threshold equality | Panel 3 | Repeated description of where drift occurs |
| Latest-as-of recall with both clock-selection stages and empty-set/tie behaviour | Panel 8 | Unexplained recall shorthand |
| Source-defined memory operations | Left memory panel | Repeated lookup/CID explanation, now beside the full observation tuple |
| Explicit contribution and standard/complementary technology boundary | Left lower panel | Repeated absence prose; the Berlin rows now demonstrate absence directly |

The source-pixel experiment, matrix, two-clock example, actual retained model vectors, 12-second demo, three QR tasks and full community band remain. The centre column's repeated source-pixel caption is removed because the figure already prints the record pair, outcome and sampling scope. Its product-offset equation remains.

## Complete formulas, with their scope

`Δz = Δ_env + Δ_sensor + Δ_geo + Δ_encoder + ε` organises potential causes of a readout change. The `change_attribution@1` ledger returns per-term evidence under a receipt. It does not calculate a numerical causal split: `split` is null. Referential drift during an agent handoff and readout change between visits are different questions.

For the drift-anchor implementation, let `d = |x-a|`. With positive finite uncertainty, `r = d/(3σ)` and `s = r/(1+r)`. Invalid uncertainty (zero, negative or non-finite) yields 0 for exact agreement and 1 otherwise. Consistent means `s < 0.5`; tension means `0.5 <= s < 0.75`; contradicted means `s >= 0.75`. The local variable `r` renames the code's `z`, avoiding collision with the readout in the decomposition. No probability or cause attribution is implied. The shown rule assumes finite output and anchor values.

The conceptual observation is `O = (a,b,t,v,u,p,s)`: address, band, valid time, value, uncertainty, provenance and associated attestation. Memory is `M = (O*,E*)`; temporal edges carry subject, predicate, object and a validity interval. This restores the complete conceptual model without copying an obsolete signature claim from upstream prose. In the tested implementation, canonical **record** bytes determine the fact CID; a batch attestation covers that address; a separate signed receipt binds a read response. Missing uncertainty or source hashes stay missing. The tuple is not a literal fact-wire schema.

For **latest-as-of mode without an exact tslot**, `Cτ = TxAsOf(O*,a,b,τ)` selects transaction-time versions known by τ, per cell/band/valid-time key. `recall = max_(t,cid) {O in Cτ: t <= t*}` then selects the latest valid slot, with deterministic lexicographic CID ties; no candidate yields an empty result. It is not an unqualified argmax over all historical versions, nor a formula for every endpoint mode. Sources are `recall.rs`, `bi_temporal.rs` and the stored Bengaluru observations. The Bengaluru dates illustrate the signing-time axis; its band has a fixed slot. The source change is not evidence of ground movement.

Memory operations are source-defined interfaces: recall, diff, merge, trace, competing, evolve, ensure and valid. Merge creates a citable set rather than a fused estimate. Contradictions are retained rather than averaged away. Ensure currently materialises at a single hop; multi-hop planning and causal-removal recomputation remain open.

## Tests and data, with dates preserved

- Upstream emem implementation remains pinned to `8e9b401cecae7ab9944d403a2d7840952c6586a6`. Formula source files and hashes: `evidence/formalism/sources.json`.
- Existing SDK offline receipt and canonical encoding tests: 20 passed, 0 failed, 0 skipped in the retained 2 October run. This revision does not relabel that as a new run.
- Drift thresholds and invalid uncertainty have archived passing Rust tests from 30 September, at `04b40c5`. Current Rust source was inspected; no fresh Rust run is claimed.
- Final R5 data are unchanged. Pooled Claude corruption outcomes are 254/276 prose, 164/276 JSON, 220/276 retrieved text, 154/288 opaque id and 0/300 checked reference. Genuine controls: 71/72 expected decisions, one false refusal. Qwen remains separate.
- Berlin retains the same selection, source timestamps, native grids and 4 absence records. Existing 2 October verification re-hashes all 16 selected records; record hash equality and signer-field equality are not mislabelled as a fresh signature verification.
- Token hash rules remain explicitly scoped to the inspected `18adb67` implementation and the corrected v11 review. Fourteen rows represent data needs, not fourteen distinct token prefixes. The old glyph key was removed because it incorrectly grouped a hashed state record with list hashes. `track.v1` is a note, and trace evidence is a reference harness.

## Invention taxonomy and issue acceptance

| Category | Included technologies or claim |
|---|---|
| Claimed contribution | A portable, machine-checkable reference to a specific physical observation, handed between agents with receiver-side resolution and checks |
| Standard enablers | Content addressing, BLAKE3, Ed25519, canonical CBOR, Merkle logs and signature verification |
| Complementary layers | STAC asset discovery, openEO processing, PROV/C2PA provenance, RAG, temporal databases/event sourcing, generic agent memory and EO-agent orchestration |
| Open validation | Numerical change attribution, independent device-anchor wiring, separately operated agent-host handoffs |

Acceptance review for this revision:

- **#11:** one explicit contribution box; claims-map taxonomy distinguishes the contribution from standard and complementary technologies. No priority claim, cryptographic invention claim or generic-memory invention claim is introduced.
- **#13:** the first-screen handoff wall explicitly names entity meaning, sensor accuracy and the decision as unestablished. The hero describes an observation handoff; no satellite-as-truth-arbiter framing.
- **#26:** source pixel → sender → alternative handoffs → orange mutation step → receiver action/checks → outcome counts → explicit limits is visible in one figure without needing paragraphs.
- **#31:** header imagery locates the Keylong observation and contrasts the named/south pixel; the handoff chip identifies the cited 10 m pixel and NDVI; the source experiment annotates pixel, band, date, value and changed decision; Berlin's centre marker connects the lookup cell to distinct dated product records. Each image has an evidential purpose.

#19 is strengthened by the full two-clock selection and temporal-storage comparison, but is not closed in this revision: the pinned historical example and stale/current handoff rows are not a fresh end-to-end independently hosted historical-recall experiment. Broader model and external-host issues remain open.
