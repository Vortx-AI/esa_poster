# Verified claims ledger

Snapshot: 2026-09-29. Source: `Vortx-AI/emem` at HEAD `64cfae5`, plus live calls to emem.dev
(see [`../repro/`](../repro/README.md)). Paths are relative to the emem repo.

**Rule: a claim goes on the poster only in the "Poster wording" form below.**

Status key: ✅ verified in code and/or live · 🟡 true with a qualification that must be
printed · ❌ wrong as currently written in `POSTER_CONCEPT.md`

---

## 1. The observation object: 🟡

- **Code:** `PrimaryFact` in `crates/emem-fact/src/fact.rs:73-112`. Fields in declaration
  order, which is also the byte order:
  `kind, cell, band, tslot, value, unit?, confidence, uncertainty?, sources[], derivation{fn_key,args}, privacy_class, schema_cid, signer, signed_at`.
- **Live:** the 541-byte fact we fetched decodes to exactly these keys.
- **Variants:** `Primary`, `Derivative` and `Absence` (`fact.rs:9-18`). Absence is a signed
  fact, not a 404.
- **Correction:** in `O = (a,b,t,v,u,p,s)`, the `s` is **not a signature inside the fact**.
  The fact carries `signer` (a public key) and `signed_at`. The ed25519 signature sits on the
  enclosing attestation, over a Merkle root of fact CIDs (`crates/emem-attest/src/attest.rs:105-124`).
- **Bi-temporal: ✅.**
  - `tslot` is valid time. `signed_at` is transaction time (`fact.rs:100`).
  - Reads take `as_of_tslot` and `as_of_signed_at` (`docs/only-emem.md` §2).
  - Tests: `crates/emem-primitives/tests/bi_temporal.rs:286,314`.

**Poster wording:** `O = (cell, band, tslot, value, uncertainty, provenance, signer, signed_at)`.
Signed by the attester over a Merkle root of fact CIDs. Two time axes: when the world was so
(`tslot`), and when the memory learned it (`signed_at`).

## 2. The content identifier: 🟡

- **Code:** `crates/emem-cache/src/sled_hot.rs:813-819`. The CID is BLAKE3-256, full 32 bytes,
  written as 52 characters of RFC 4648 base32, no padding, lowercase. There is no multihash
  or multibase prefix.
- **Live:** we re-derived three production CIDs with stock `blake3` (see `repro/`). ✅
- **Correction: the encoding is "emem-CBOR", not generic canonical CBOR.**
  - It is deterministic CBOR with **struct-declaration field order**, minimal-length heads,
    absent Options omitted, `confidence` as float32, every NaN folded to `f97e00`, and
    `-0.0` folded to `+0.0` (`crates/emem-fact/src/cbor.rs:43-54`).
  - It is **not** RFC 8949 §4.2.1 key-sorted. `docs/whitepaper.md:623-626` warns that "a
    generic canonical-CBOR encoder that sorts keys computes a different digest".
- **Correction: the CID names one signed attestation.** The signature is outside the hash,
  but `signer` and `signed_at` are inside it. Two responders that measure the same value
  mint different CIDs (`docs/agents.md:444-449`). We saw this live: two CIDs carry the
  identical 915.07 m.

**Poster wording:** `fact_cid = base32(BLAKE3(emem-CBOR(fact)))` where emem-CBOR is
deterministic, declaration-ordered and float-canonical. The bytes hashed are the bytes served
(`GET /v1/facts/<cid>`, `Accept: application/cbor`).

## 3. Token families: 🟡 (the concept lists too few, and one that does not exist)

Shipped grammar (`docs/protocol.md:1696-1707`):

| token | grammar | strength |
|---|---|---|
| `emem:fact:` | `<cell64>:<fact_cid>` (52-char cid) | **byte-identical** |
| `emem:cell:` | `<cell64>` | address only |
| `emem:entity:` | `<entity_cid>` (16 B) | shared *name* anchor, not bytes |
| `emem:bundle:` | `<bundle_cid>` (16 B), up to 256 facts | set anchor; members are full-strength fact CIDs |
| `emem:raster:` | `<aoi_cid>:<band>:<tslot>:<derivation_cid>` | derivation-bound; artifact re-hashes to `artifact_cid` |
| `emem:cube:` | `<aoi_cid>:<band>:<lo>..<hi>:<derivation_cid>` | signed manifest over raster members |
| `emem:rasterset:` | `<bundle_cid>:<derivation_cid>` | 2–64 bound fields |
| `emem:trace:` | `<trace_cid>` | byte-identical signed OS/device trace |
| `emem:attestation:` | `<cid>` | signed platform attestation |
| `emem:state:` | `<cid>` | content address of a reasoning step (unsigned) |
| `emem:tree:` | `<file_cid>#row=<i>` | Merkle row proof over a file |

- **❌ There is no `log:`, `proof:` or `file:` token.** Log proofs are REST routes (`/v1/log/*`).
- The guard classifies only fact, bundle and field tokens as "resolves_to_bytes"
  (`crates/emem-guard/src/tokens.rs:37-72`).

**Poster wording:** show fact → raster → cube → rasterset as the EO ladder. Mark entity and
bundle as anchors with a *different strength*. Never imply that every family means "same
bytes".

## 4. Spatial binding and re-hash: ✅, with who-does-what fixed

- **Spatial binding is fail-closed.** A token whose `cell64` differs from the cell inside the
  signed fact returns **HTTP 409** (`crates/emem-api-rest/src/lib.rs:38166-38193`). The
  descriptor form also binds band and date.
- **Who re-hashes: the client, not the resolver.** The server serves the exact preimage
  bytes, and anyone checks them in three lines (`lib.rs:23249-23274`; `web/verify.html:564-573`).
- **Poster wording:** "Resolve returns the exact bytes; *you* re-hash them. A token cited
  under the wrong place fails with 409."

## 5. Signed receipts: ✅

- **Signature:** ed25519 (`verify_strict`) over the BLAKE3 digest of a domain-separated,
  length-prefixed preimage (`crates/emem-attest/src/lib.rs:163-213`).
- **Receipt preimage v2 binds:** `REQUEST_ID`, `SERVED_AT`, `SCOPE?`, `AS_OF?`, `EDGES?`,
  `MANIFEST?`, `PRIMITIVE`, `CELLS`, `FACT_CIDS`, `FIELD?`, `MERKLE`.
- **Proof stripping is detectable.** `MERKLE` is always present, either as a proof or as an
  explicit ABSENT marker (`lib.rs:283-313`).
- **Not bound:** the full query parameters and intent. Do not say "binds the query".
- **Offline verifiers:** Rust CLI `emem verify`; Python `ememdev.verify.verify_receipt_offline`;
  browser JS at `/verify`. The Python test pins the same digest as the browser verifier
  (`sdks/emem-py/tests/test_verify_offline.py:48-63`).
- **Live:** `signature_valid: true`, `merkle_proof_valid: true` on a Bengaluru recall today.
  A real fact CID cited under another cell returned **HTTP 409** today.

## 6. cell64: 🟡

- **Code:** `crates/emem-codec/src/geo.rs:15-49,96`. The shipped grid is a quantized lat/lng
  grid (21-bit lat × 22-bit lng), **about 9.55 m at the equator**, not equal-area, at a
  single active resolution.
- String form: 4 dotted bigrams, e.g. `defi.zb493.xuqA.zcb5f`.
- An H3-like hierarchical grid is specified (`crates/emem-core/src/cell.rs`), but it is a
  migration target, **not live**.
- **Do not say** "hierarchical", "S2" or "H3". Say "a deterministic 64-bit cell, about 9.55 m".

## 7. Field tokens: ✅

- **Grid encoding:** `application/x.emem-grid-f32.v1` (`crates/emem-codec/src/grid.rs`).
  - A 64-byte header with magic `EMEMGRD1`, then little-endian f32, row-major, north row first.
  - NaN is canonicalized to `0x7fc00000`; `-0.0` becomes `0.0`.
  - GeoTIFF is a "lossy VIEW… never the signed thing".
- **Derivation record** `emem.field_derivation.v1` (`band_raster.rs:380-416`) holds:
  `aoi_cid`, `band`, `tslot`, `fn_key`, the source Sentinel-2 scene with its angles and cloud
  cover, the artifact CID, and sampled anchor cells. It is signed as a `DerivativeFact`.
- **Cube:** a signed manifest over independently resolvable raster members. Each member
  records which requested date mapped to which scene, and how many days away it was.
- Heavy artifacts can be evicted; the signed record is the rebuild recipe.
- **Live today: ⚠ `band_raster` and `raster/resolve` returned 504.** See `repro/README.md`.

## 8. Pinned semantics: 🟡

- Manifest CIDs are published for bands (43 slots), algorithms (168 recipes), sources and
  schema (`crates/emem-core/data/`).
- The receipt `MANIFEST` segment binds `bands_cid`, `registry_cid`, `schema_cid` and
  `sources_cid`.
- **❌ `algorithms_cid` is not in the receipt preimage.** `docs/model.md` says it is; the code
  does not bind it. Say "bands, sources, schema and function registry are pinned".

## 9. Immutable evolution: ✅

- A changed byte gives a new CID.
- Signed typed edges (`supersedes`, `disagrees_with`, …) are part of attestation leaves
  (`crates/emem-fact/src/edge.rs:39-62`).
- History keeps every CID (`crates/emem-storage/src/lib.rs:615-638`). There is no silent
  `forget()`.
- **Caveat:** superseded facts are reachable when you hold the CID. An auditor found that a
  bi-temporal query could not surface the superseded 918.0 fact (`docs/collaboration-log.md:51903`).
  Check whether this is fixed before claiming "time-travel queries".

## 10. Transparency log: ✅

- RFC 6962 construction with BLAKE3 in place of SHA-256 (`crates/emem-attest/src/translog.rs`).
- Inclusion and consistency proofs are implemented, and forked history is rejected (a test).
- Routes: `/v1/log/sth`, `/v1/log/inclusion`, `/v1/log/consistency`, `/v1/log/entries`,
  `/v1/log/witness(es)`.
- **Live independent witness:** geo.qa co-signs every 15 min (`docs/federation.md:314-345`;
  `docs/security.md:250`).
- 1,728,683 log entries in `docs/whitepaper-v3.md:86-126`. **Live on 2026-09-29: 2,537,510**
  (`/v1/log/witnesses`), with 1 independent operator (geo.qa). The head was 310 entries ahead
  of the freshest witness.
- Traces are not yet in the log.

## 11. Foundation-model embeddings: 🟡 (the claim needs to shrink)

- Embedding slots:
  - `geotessera` (128-D);
  - `clay_v1` (Clay v1.5, 1024-D);
  - `prithvi_eo2` (Prithvi-EO-2.0-300M-TL, 1024-D);
  - `galileo`.
- All are marked `provenance_class: model_output`. The server attaches the caution "a learned
  representation, not a measurement".
- **The Clay, Prithvi and Galileo producers are retired** (`lib.rs:36012`). Old facts still
  verify, but no new ones are minted. **Tessera is the live encoder.** The AlphaEarth slot is
  reserved and unused.
- **❌ No per-fact checkpoint hash.** `ServedVia.model_blake2b_hex` exists but nothing sets it.
  The encoder is pinned by the recipe key (`fn_key@version`) plus sources plus the band manifest.
- **Poster wording:** "Embeddings are signed as ordinary fact values, labelled `model_output`.
  The encoder is pinned by recipe and content-addressed band manifest." Show Tessera as the
  live example. List Clay, Prithvi and Galileo as prior encoders whose facts still verify.

## 12. Formal methods and conformance: 🟡

- **No TLA+, Kani, proptest or fuzzing** in the repo.
- `spec/test_vectors/` has only 4 `os_trace` vectors. The cell64, CBOR, CID and signature
  vectors are "coming soon".
- Cross-language agreement exists for **receipt preimages** (Rust, Python and JS pin the same
  digest). **No non-Rust fact-CID encoder** exists; fact CIDs are checked by hashing the
  served bytes. That is exactly what our `repro/verify_fact.py` does.
- **Poster wording:** "Any client verifies with a stock BLAKE3 in 3 lines. Formal proofs and
  full conformance vectors are open work."

---

## Stronger true claims the concept is missing

1. **Signed absence.** "Nothing here" is a signed `Absence` fact, distinct from an unsigned
   "could not look".
2. **Contradictions kept, not averaged.** `/v1/memory_contradictions` gives a severity score
   per band kind (`docs/only-emem.md` §1).
3. **Provenance classes as hermeticity labels:** `direct_sensor`, `deterministic_index`,
   `attested_execution`, `model_output`, `human_curated`, `estimator`. Recall accepts
   `deterministic: true`.
4. **Resistance to proof stripping and downgrade.** An independent audit caught 5/5 tampers,
   including a v1 → v2 downgrade (`docs/benchmarks.md:283-326`).
5. **Capability-bound memory writes.** The write preimage binds the verb, path, body hash and
   the previous file CID, so a path can be locked to one signer (`docs/only-emem.md` §3).
6. **Notes are served as "data, not instructions"**, a prompt-injection boundary
   (`README.md:478-485`).
7. **Pre-publication guard.** A draft that says 35 °C against a signed 28.0 is denied with
   `PROV_VALUE` (`plugins/emem/skills/emem-verify-before-publish/SKILL.md`). Limit: the guard
   does not yet check that the band matches the sentence.
