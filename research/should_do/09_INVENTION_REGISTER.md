# Invention register: what emem actually contributes

Snapshot: 2026-09-29. Four independent audits of emem at `64cfae5`: memory/time, computation/EO,
trust/protocol, and prior art. Each entry was re-checked live against emem.dev. Scripts are in
[`../repro/`](../repro/README.md).

Rules applied to every entry:

- **Mechanism** is what the code does, cited by file:line in the emem repo.
- **Live** is a demonstration we ran ourselves on 2026-09-29.
- **Prior art** names the closest existing work. **What is new** is stated conservatively and
  always as "to our knowledge".
- **Limits** includes defects found during the audit. They go on the poster in compressed form.

The authors' own framing (whitepaper v3, 2026-09-10): *"shared state for agents that do not
trust each other."* Earth observation is the first and largest corpus. It is not the definition
of the protocol.

---

## Tier A: the contributions to put on the poster

### A1. A self-certifying EO observation

- **Mechanism.** A fact is `(cell, band, tslot, value, uncertainty, sources, derivation, signer,
  signed_at)`. It is encoded as declaration-ordered deterministic CBOR (NaN and −0 canonical) and
  named by `base32(BLAKE3-256(bytes))`. The server serves exactly those bytes. A token cited under
  the wrong cell is refused with HTTP 409.
  - Code: `crates/emem-fact/src/fact.rs:73-112`, `crates/emem-cache/src/sled_hot.rs:813`,
    `crates/emem-api-rest/src/lib.rs:38166`.
- **Live.**
  - Fact `oj5cecci…` (1,115 bytes) re-hashes to its name with stock `blake3`.
  - It records scene `S2A_MSIL2A_20260925T054251_R005_T43SFS`, DNs B08 = 3502 and B04 = 1900,
    the Planetary Computer catalogue, and BOA offset −1000.
  - NDVI recomputed from those DNs is **bit-identical** to the signed value
    (0.4708994708994709, `0x3fde233788cde233`). Script: `verify_ndvi.py`.
- **Prior art.**
  - STAC `file:checksum` and the STAC Merkle extension hash *assets*.
  - RDA Dynamic Data Citation (Rauber et al. 2015/16) cites a subset by a *stored query PID +
    timestamp + result hash*.
  - C2PA and OGC Testbed-20 sign *media/assets*.
- **What is new** (to our knowledge): the identifier names the **individual value itself**,
  not a query or a file. It carries enough of the derivation (scene, DNs, offset, recipe key)
  to be rebuilt offline by anyone.
- **Limits.**
  - `signer` and `signed_at` are inside the hash, so a CID names *one signed attestation*. Two
    attesters of one value mint different CIDs.
  - The encoding is not RFC 8949 key-sorted, and it is "dCBOR-like", not dCBOR.
  - Scenes are pinned by ID and URL, not by content hash.
  - An older fact (2022 scene) records no catalogue or offset in its args. This is an open
    question on the offset convention (see `../do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md`).
  - `recall` without a date can return an old scene. Always pass a `tslot` or date.

### A2. Two clocks on every EO value: when the ground was so, and when the system knew it

- **Mechanism.** `tslot` is valid time; its unit depends on the band's tempo (Fast = days since
  1970, Slow = 365 d, Static = 0). `signed_at` is transaction time. `as_of_signed_at` walks the
  key's full history (D6 fix).
  - Code: `crates/emem-core/src/tslot.rs`, `crates/emem-storage/src/lib.rs:1816-1882`; tests in
    `crates/emem-primitives/tests/bi_temporal.rs` (11 tests).
- **Live** (`verify_bitemporal.py`), key: Bengaluru / `copdem30m.elevation_mean` / tslot 0.
  Every answer re-hashes.

  | as known on | answer |
  |---|---|
  | 2026-05-01 | no fact |
  | 2026-06-15 | **918.0 m**, `open_meteo`, signed 2026-05-28 |
  | 2026-08-12 | **915.07 m**, `copernicus.dem.30m.aws`, signed 2026-08-11 |
  | 2026-09-29 | 915.07 m, signed 2026-09-28 |

- **Prior art.** SQL:2011 bitemporal periods, Snodgrass; XTDB and Datomic as-of; Zep/Graphiti
  bitemporal agent memory (arXiv 2501.13956).
- **What is new** (to our knowledge): **signed** transaction time on EO values served to agents.
  A later agent can replay what an earlier agent was told, and check it.
- **Limits.**
  - The same query **without `tslot` returned 504** on this 280-fact cell. It works on the
    exact-key path.
  - There is no test for the D6 history path.
  - "Slow" is 365 d, not calendar years.

### A3. Absence is a signed fact, distinct from "could not look"

- **Mechanism.** `Fact::Absence{reason_cid, sources, confidence}` is signed and citable like any
  fact. Timeouts and upstream errors produce an **unsigned** `status: skipped` note instead.
  Absences are rechecked after 6 h.
  - Code: `crates/emem-fact/src/fact.rs:179-198`, `lib.rs:47762`, `:57524`.
- **Live** (`verify_absence.py`).
  - An ocean point (−12.26, −140.15) returns a signed absence: "Cop-DEM GLO-30 publishes no tile
    … URL … returned 404".
  - `reason_cid` re-derives locally, and the receipt is valid.
  - For contrast, an Antarctic NDVI request gives an unsigned `upstream_error` skip.
- **Prior art.** DNSSEC NSEC/NSEC3; sparse-Merkle non-inclusion (CONIKS); authenticated spatial
  range queries (MR-tree).
- **What is new** (to our knowledge): a signed EO distinction between "looked, nothing there"
  and "could not look".
- **Limits.**
  - This is a signed **assertion** of absence, **not authenticated denial of existence**. It is
    not proven against a committed set. Say "signed absence", never "provable absence".
  - `reason_cid` hashes prose, not the upstream HTTP response.
  - Defect D3 is open: some failure paths are still unsigned.

### A4. Disagreement is kept and scored, never fused

- **Mechanism.** Every attestation at a `(cell, band, tslot)` key is kept (`history_many`).
  `/v1/memory_contradictions` scores severity by value shape:
  - scalar: spread / band range;
  - vector: 1 − mean pairwise cosine;
  - categorical: 1 − mode share.

  It also flags a single signer that switched provider or recipe.
  - Code: `crates/emem-primitives/src/memory_contradictions.rs:455-620` (15 tests).
- **Live.** The Bengaluru key is flagged `same_attester_provider_substitution`: providers
  `open_meteo_copdem90m@1` → `copernicus_dem_30m_aws_pixel@1`, 8 attestations.
- **Prior art.** The truth-discovery survey (Li et al. 2016) resolves conflicts. Land-cover
  disagreement maps (Fritz et al. 2011) and Dempster–Shafer conflict mass quantify disagreement
  in order to fuse.
- **What is new** (to our knowledge): disagreement returned **as a query answer, per key, with
  provenance**, rather than fused away. This is a design stance, not a new algorithm.
- **Limits.**
  - **The severity number is miscalibrated** for bands with no registry range: a 2.93 m DEM
    difference scored 1.000. **Do not print the severity value.**
  - There is one responder, so no genuine multi-party disagreement exists yet.
  - A whole-corpus scan is truncated.

### A5. The server recomputes a claimed derivative, and reports the gap in ULPs

- **Mechanism.** `/v1/derive` resolves every parent token and rejects cell-mismatched parents
  (409) and unresolvable ones (404). It recomputes pure ops (`delta`, `mean`, `sum`) or
  registry expression trees, then compares:
  - exactly (canonical f64) for leaves;
  - within **4 ULP** for reductions over more than 2 parents.

  It returns `rule`, `ulp_tolerance` and the measured `ulp_gap`. Only a match is promoted to
  `deterministic_index`; a caller may declare only `model_output`, `human_curated` or
  `estimator`.
  - Code: `lib.rs:38795-39340`; tests at `lib.rs:95490-96290`.
- **Live** (audit run, signed with a throwaway key):

  | submission | ulp_gap | verified |
  |---|---|---|
  | exact delta | 0 | yes |
  | sum +2 ULP | 2 | yes |
  | sum +9 ULP | 9 | no |
  | wrong delta | 7.1 × 10¹¹ | no |

  The unsigned request returns 401 with the exact digest to sign.
- **Why 4 ULP.** Measured on real parents: the gaps for N = 5, 16, 32, 64, 128 were
  0, 1, 2, 2, 0. Strict equality fails non-monotonically (whitepaper v3 §3.5).
- **Prior art.**
  - Nix RFC 62 and Bazel give content-addressed derivations.
  - ESM reproducibility is either bitwise or statistical (ensemble consistency).
  - numpy has `assert_array_max_ulp`.
- **What is new** (to our knowledge): hermeticity classes plus a **declared and measured ULP
  bound returned with the verdict**, for EO-derived values.
- **Limits.**
  - Tier 1 covers scalar `delta`, `mean` and `sum`, plus registry expressions only. Arbitrary
    code is not re-run, and `code_cid` is never fetched.
  - Multi-hop lineage and portable hermetic actions are not built (`docs/model.md` says so).
  - The 401 text says "mean excluded", but the code includes it.

### A6. Fields and fields-through-time as signed derivations, with the date gap stated

- **Mechanism.**
  - A raster is a canonical f32 grid (`EMEMGRD1` header; NaN and −0 canonical) whose artifact
    hash sits in a signed derivation record. That record holds the AOI, band, scene, cloud
    cover, angles and sampled anchor cells.
  - A cube is a signed manifest of raster members. Each member states which requested date it
    serves and **how many days away** its scene is.
  - Code: `crates/emem-codec/src/grid.rs`, `band_raster.rs:380-445,1880-1896`.
- **Live.**
  - Keylong: a 443 × 453 px Sentinel-2A L2A field (25 Sep 2026). All 4 band artifacts
    re-hash, and `raster/resolve` spot-check passes.
  - Cube over the same AOI:

    | requested | scene used | days away |
    |---|---|---|
    | 15 May | 10 Jun | **26** |
    | 15 Jun | 30 Jun | 15 |
    | 15 Jul | 3 Aug | 19 |

- **Prior art.** openEO and Earth Engine datacubes; STAC items; the THEDE datacubes poster at
  this workshop.
- **What is new** (to our knowledge): a cube is a *signed, content-addressed* manifest, and each
  member records its temporal substitution.
- **Limits.**
  - Scene selection uses scene-level cloud cover, relaxed in tiers (40%/30 d → 60%/60 d →
    80%/90 d), with no per-pixel mask in `band_raster`.
  - **Re-minting gives a new derivation id** (`signed_at` is hashed), so the token changes while
    the artifact hash stays the same.
  - The raster endpoints return 504 when cold.

### A7. The agent interface enforces the strength of what is cited

- **Mechanism.**
  - Token families are typed by strength: `resolves_to_bytes` is true only for fact, bundle and
    field tokens; entity is a shared *name*, and cell is only an address
    (`crates/emem-guard/src/tokens.rs:36-73`).
  - `/v1/guard/verdict` checks prose against the facts it cites
    (`crates/emem-guard/src/policy.rs`; 143 tests pass).
  - Refusals are typed (`emem.error.v1`) and carry the fix. A signed write that is refused
    returns the exact 32-byte digest to sign, so the client needs no canonical-CBOR code.
- **Live** (the guard, citing the met.no fact of 28.0 °C):

  | draft | verdict |
  |---|---|
  | "35 °C (token)" | `deny PROV_VALUE` |
  | "28.0 °C" | allow |
  | "28.4 °C" | deny |
  | same CID under the wrong cell | `deny PROV_BYTES` |
  | uncited "35 °C in Bengaluru on 2026-09-28" with claim gating on | `deny CLAIM_UNGROUNDED` |

  Also live: a `memory_create` refusal named digest `95cc9ab7…`, which we recomputed locally.
- **Prior art.** 2025–26 MCP receipt tools (agent-receipts, AGA MCP, Notarized Agents) sign
  *tool calls*. Guardrail frameworks, including GeoGuard at this workshop, validate outputs.
- **What is new** (to our knowledge): **checking a number in an agent's prose against the signed
  value it cites, at the writer's stated precision**, with the citation's strength typed.
- **Limits.**
  - emem.dev is `advisory`; enforcement requires self-hosting.
  - Claim gating is off by default.
  - The guard does not check that the band matches the sentence.
  - A wrongly named request field returns `allow` with 0 citations checked.
  - The memory-write CAS is mandatory only for `delete` and `rename`.

### A8. An append-only public record, checkable offline

- **Mechanism.**
  - An RFC 6962 Merkle log over BLAKE3, with a signed tree head plus inclusion and consistency
    proofs (`crates/emem-attest/src/translog.rs`).
  - Receipt preimage v2 signs either the Merkle proof or an explicit ABSENT marker, so
    stripping the proof or downgrading to v1 breaks the signature.
  - Facts are batch-signed over a sorted Merkle root, and duplicate leaves are refused
    (CVE-2012-2459).
- **Live** (`verify_log.py`, `verify_receipt_tamper.py`, written from RFC 9162):
  - STH valid at **2,538,190 entries**; inclusion of leaf 1,234,567 → true; 1-bit flip → false;
    consistency 1 M → 2.54 M → true.
  - A receipt as served verifies. The same receipt with its proof stripped, or relabelled v1,
    fails.
- **Prior art.** CT (RFC 6962/9162), Trillian, Sigstore Rekor, Go sumdb witnesses, GlassDB.
- **What is new:** nothing cryptographically. It is a careful application to EO facts served to
  agents. Present it as rigour, not invention.
- **Limits.**
  - **The co-signing witness, geo.qa, is a second node on its own domain and key, operated by
    the same organisation (Vortx AI).** This is not organisational independence.
    `head_is_independently_witnessed` was false during the check (134 entries behind).
  - The receipt's Merkle proof covers only `fact_cids[0]`.
  - Read federation does not exist.

---

## Tier B: findings, not mechanisms

### B1. Agreement between agents is not evidence of correctness

- **Result.** Pre-registered, Fisher one-sided: under compaction, 0/72 correct with 3/36
  agreeing, p = 0.035 (`docs/paper-section-statistics-and-threats.md:85-89`).
- **Paraphrase trap.** "NDVI ≈ 0.49" raised Gemma–Qwen agreement, and both chose SKIP when the
  correct action was WATER.
- **Prior art.**
  - Telephone-game drift: Perez et al., ICLR 2025, arXiv 2407.04503.
  - Lost in multi-turn conversation: Laban et al., arXiv 2505.06120.
  - *The Deliberative Illusion* ("agree more while knowing less"): arXiv 2606.03032.
  - *Lost in Compaction* (17% of constraints retained): arXiv 2608.11242.
  - ARC addressable-recall compaction (pointer-based): arXiv 2607.25066. **This is a direct
    conceptual competitor.**
- **What is new.** A measurement of a known phenomenon on EO values, plus a mechanism that
  detects the drift of cited values. **The phenomenon itself is not new. Cite these papers.**
- **Report with it:** 0/72 has a 95% upper bound of ≈ 4.1% (rule of three); two open models;
  one host.

### B2. A public, signed record of cross-model agents correcting each other and the project

- **The record** (whitepaper v3 §2–3): 69 attesters, 37,020 notes, 4,311 addressed to a peer,
  at least five model families.
- **19 withdrawals**, kept as signed records beside the claims they retract.
- **Examples:**
  - An outside party proved the per-encoder calibration could not work
    (d²S/dc dx = −d(log L)/dx vanishes where the field is flat).
  - A re-score turned a headline 1.000 into 0.989.
  - The opaque identifier was shown to be the wrong thing to hand a model.
- **Why it matters:** a disagreement between agents becomes a durable, addressable object that a
  third party can fetch and check.
- **Caveat:** these are self-reported project records. geo.qa and other Vortx deployments are not
  independent adoption.

### B3. What to hand a model: the descriptor token, not the opaque ID

- **Result** (whitepaper v3 §3.4), measured on 3,583 real `fact_cid`s across two tokenizers:
  - cell64 and base32 IDs cut at identical offsets only 0–4% of the time;
  - the descriptor form (`lat,lng@date@band`, 5 dp) cuts identically 100% of the time, for
    about 3.5 more tokens;
  - at 4 dp, the wrong 10 m neighbour came back 21% of the time.
- **Live:** the descriptor token resolves to its canonical form. (A 4-dp token also resolved
  because the CID disambiguates, so do not claim a refusal.)
- **Related:** cell64 costs 12.5 cl100k tokens against 8.5 for H3 (refuted by the project
  itself; reproduced by us: 11–12 vs 7–9).

---

## Tier C: real, but not poster material

- **Algorithm registry.** 168 recipes in one pinned manifest; every parameter declares a
  `basis`; about 83 run live. *Scientific caveat:* at a Rohtang cell (about 3,900 m),
  `agb_ndvi_powerlaw@1` (a pan-tropical calibration) returned 108.66 Mg/ha with no biome
  domain check.
- **`change_attribution`.** An evidence ledger for Δz = Δenv + Δsensor + Δgeo + Δencoder + ε,
  with `split: null` (it refuses to decompose). Honest, but thin today.
- **Embeddings.** Tessera 128-D facts labelled `model_output` with a caution; the index is frozen
  and the band retired for new materialisation. k-NN works (Hamming then cosine rerank).
- **Triple-encoder change consensus.** **Retired and cannot run**: no route (404), and the
  92–95% figure has no evaluation behind it. **Do not claim it.**
- **`emem:state`** (content-addressed `/v1/ask` stages, recomputable) and **`emem:tree` /
  `range_hash`** (cite exact COG byte ranges; not yet wired into facts).
- **Memory kinds** (CoALA), consolidation (concatenation, off by default), the sleep agent
  (cannot write to production), and typed edges (free-form, empty live).
- **Freshness kernel** (non-monotonic bug), the data-not-instructions marker (a convention), and
  EUDR DDS (an application with no accuracy validation).
- **Device traces.** The verifier and its 4 vectors pass; the drift rule is not wired in; no
  real hardware is admitted.
