# 10 · Invention boundary, verification ladder, threat model and claim-status gate

Topic `ladder_threat` for the v13 final A0. Issues #11, #12, #13, #17, #21, #29 (and #7, #14, #20 where they touch
the boundary); MASTER shared state sections 4, 5, 11, 12. Read-only research: only this file was written in the repo.
Scratch artefacts (probe scripts and outputs) are in the session scratchpad
`/tmp/claude-0/-home-user-esa-poster/0db6b3ad-8059-51a6-bd74-2d7a97faf986/scratchpad/v13ladder/` and are named below.

**Code reference.** emem `origin/main` = `18adb67895d33c8b64d3b091a90af1f708315123` (read with
`git -C /home/user/vortx-ai/emem show origin/main:<path>`). The live responder served
`x-emem-commit: 8e9b401cecae7ab9944d403a2d7840952c6586a6` on 2026-10-01T01:02Z. 8e9b401 is 18adb67 plus 7 commits;
`git diff --stat 18adb67 8e9b401 -- crates/emem-fact crates/emem-attest crates/emem-storage/src/lib.rs` is empty, and
`hash: None` / `hash: Some(` in `crates/emem-api-rest/src/lib.rs` count 62 / 0 at both commits. So every code claim
below holds for the deployed binary as far as these files go.

**Labels.** MEASURED (run in this session, command named) · MEASURED (committed) (a committed repo result, re-read
here, file named) · LIVE (fetched from a live service in this session, URL and UTC time) · SPEC (stated by emem code or
docs at 18adb67, file:line) · EXTERNAL (third-party spec or paper, URL, retrieved 2026-10-01) · INFERRED (my reading
or arithmetic) · UNVERIFIED (stated somewhere, not checked).

Live reads in this session (GET only; nothing signed, published or written): `/v1/log/witnesses`,
`/v1/verifier_spec`, `/v1/facts/oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` (CBOR), `/v1/log/sth`,
`/.well-known/agent-card.json`, all at 2026-10-01T01:02:45Z; `https://geo.qa/` at about 01:10Z.

---

## 0. Findings in one screen

1. **The invention is a combination, and it is the handoff unit, not a primitive.** One observation record
   (cell, band, valid time, value, named source, derivation inputs, signer, signing time), named by the BLAKE3 hash of
   its bytes and attested in a log, is what one agent hands another; the receiver checks it at increasing depth.
   BLAKE3, Ed25519, CBOR, content addressing, Merkle logs, STAC, PROV, C2PA, MCP and A2A are used, not claimed
   (section 1). SPEC + INFERRED.
2. **A fact_cid names EMEM's record, not the satellite file.** `fact_cid = base32(BLAKE3-256(ciborium(fact)))`
   (`emem-cache/src/sled_hot.rs:813-820`). The record names its upstream file by scene id and URL but binds none of
   its bytes: `Source.hash` is never filled in the server (62 `hash: None`, 0 `hash: Some(` in
   `emem-api-rest/src/lib.rs`, MEASURED), and 0 of 213 source entries at the Keylong cell carry a hash or cid
   (MEASURED, `research/repro/data/v11/cell_keylong.json`). Defect 25 stands at the deployed commit.
3. **A fact carries no signature of its own.** The operator's key signs
   `PreimageV1("attestation"){batch_root, registry_cid, schema_cid}` over a Merkle root of BLAKE3 hashes of a batch of
   records (`emem-fact/src/attest.rs:93-143`, `emem-attest/src/lib.rs:441-451`). Every hashed field is therefore
   signed transitively; `attested_at`, `attester_key_epoch` and `scope` are not in the signed preimage (SPEC). The
   v12 board's `s = Ed25519(BLAKE3(body))` copies `docs/model.md:25`, which the code contradicts (defect 32).
4. **The ladder has six layers, and R1 measures four of them.** L0 record integrity (hash, attestation, log),
   L1 observation identity, L2 derivation recompute, L3 upstream provenance and source re-read, L4 entity, L5
   physical truth and decision. R1's checks D to I map to L0 (D, F, G), L1 (E), L2 (H), L3 (I); M17 sits at L4 and
   nothing catches it (section 3). MEASURED (committed), re-run here with identical summary.
5. **"0 of 16" is a property of the suite, not of the ladder.** Three signer errors outside R1's 16 pass all six
   checks D to I: an offset recorded as 0 for a baseline-05.13 scene (value 0.2966, the irrigation decision flips), a
   relabelled same-day scene id, and a wrong unit. MEASURED this session with R1's own verifier
   (`scratchpad/v13ladder/r1_t2_extra.py`). They need an L3 metadata re-read (the STAC check in trace link 8), which
   R1 does not run.
6. **"Verified" on the board meant L0 plus L1, and that included wrong-pixel records.** All 780 facts behind
   sections 1 and 3 pass L0 and L1; 266 pass L2; none was re-read at L3. Among the 780 PASS rows is `kxjvfwpa…`
   (Keylong, 23 Sep 2026), signed NDVI 0.3444, whose containing pixel reads 0.4860 (MEASURED (committed),
   `eo_evidence_per_fact_checks.csv`, `pixel_check.json`). This is the clearest demonstration on file that a
   passed check at L0 to L2 is not a measurement check.
7. **Trust is one organisation deep.** emem.dev and geo.qa are both Vortx AI (geo.qa's own page names "Vortx AI
   Private Limited" as creator and publisher, LIVE); `/v1/log/witnesses` reports `independent_operator_count: 1`
   (geo.qa), `head_is_independently_witnessed: false`, and 109 `key_only` keys, which "proves someone holds the key
   and nothing more" (LIVE 01:02Z). emem's README:246 still says the head "is co-signed by independent witnesses …
   so a split view is detectable" (SPEC; contradicted by the live endpoint and by `docs/whitepaper.md` §8.3, §8.5).
8. **emem's own resolved bugs are each a failure class of one ladder layer** (section 3.7): wrong pixel (L3),
   wrong offset convention (L2/L3), asked-date vs served-date (L1), provider substitution under one band name (L1/L3),
   stale state as current (L1), place name over coordinates (L4), copies counted as corroboration (trust model). A
   pipeline that hands values between agents without a record has no field at which to detect any of them.
9. **The current build gate cannot see the boundary.** `poster/build_v12.py:42-58` checks dashes and 13 tell words,
   and strips `<svg>` and comments first, so figure text is never checked. A lexical prototype of the claim gate
   (section 5.6) flags 36 items on the v12.1 board, 7 of them in figure text the present gate never reads. MEASURED.
10. **Section 6 lists 46 boundary violations on the v12.1 board with corrected text** (36 in the HTML, 10 in figure
    text); 16 are high (they change what a reader would believe EMEM establishes): the CID wording (L132), the guarantees table (L220-228), the hero line
    (L112), the "truth is tested by re-reading" answer (L234), "emem signs the one value" (L236), the model figure's
    signature and "equal values give equal names", and the "Every number" sub-line (L113).

---

## 1. Invention boundary (issue #11; MASTER §4)

### 1.1 The invention statement

**Poster form (31 words, 3 m / 1 m line).**

> An agent hands the next agent a reference to a signed observation record, not a paraphrase; the receiver resolves it,
> checks the record and, for open archives, re-reads the pixel it names.

**Canonical form (one sentence, for the claims map and the 30 cm text).**

> EMEM represents an Earth-observation reading as a canonical observation record (cell, band, valid time, value, named
> upstream source, derivation inputs, signer, signing time), names the record by the BLAKE3 hash of its encoded bytes,
> and has the operator's key attest it in an append-only log, so that one agent can hand another this reference
> instead of a paraphrase and the receiver can check, without trusting the sender, that the bytes are the attested
> ones (L0), that they describe the cell, band and time it asked about (L1), that the value follows from the recorded
> inputs (L2) and, for open archives, that those inputs match the named source pixel (L3).

**Boundary sentence (must sit next to it).**

> It does not establish that the sensor or product is accurate, that the cell is the thing the sender meant, or that
> a decision taken on the value is right (L4, L5).

Status of each clause: record fields SPEC (`emem-fact/src/fact.rs:72-112`); name SPEC (`sled_hot.rs:813-820`) and
MEASURED (live re-hash of `oj5cecci…` at 01:02Z equals its cid); attestation and log SPEC (`attest.rs:93-143`,
`emem-storage/src/lib.rs:2128-2191`, `emem-attest/src/translog.rs`); receiver checks L0 to L3 MEASURED (R1; trace
links 1 to 15, `research/repro/v8/trace_fact_output.txt`).

### 1.2 What is claimed: the combination, element by element

| element | why it is part of the contribution | evidence |
|---|---|---|
| the unit of handoff is one observation record at `(cell, band, tslot)`, not a file, scene or asset | the receiver can bind the reference to its own question (L1) | SPEC `fact.rs:72-112`; storage key `cell ‖ 0x00 ‖ band ‖ 0x00 ‖ u64be(tslot)` (`sled_hot.rs:850-858`) |
| the record carries what a recompute and a re-read need (scene id, EPSG, DNs, BOA offset, catalogue, SCL class, cell node lat/lng) | it turns L2 and L3 from trust into checks | SPEC args order `lib.rs:53033-53051` (per `research/repro/v10/algorithms.md` §5); MEASURED trace links 6-9 |
| the reference is checkable by the receiver with stock libraries and no emem code | the handoff does not depend on the sender or the server | MEASURED R1 (`blake3`, `cbor2`, `pynacl`); `verify_lib.py` (780 facts); 10 client paths (01_v12_state §6.2) |
| history is kept: a newer observation is a new record; as-of recall returns the one valid then | an agent's earlier citation keeps resolving | SPEC `emem-primitives/src/recall.rs:282-391`; MEASURED (committed) Bengaluru 918.0 vs 915.07, `research/repro/data/contra_bengaluru.json` |
| the same reference travels through agent runtimes (MCP tool, A2A, REST) | the check is runtime-independent | LIVE MCP/A2A surfaces (report 03); G2 run (`research/repro/data/v8/results.json`) |

The defensible novelty is this combination applied to physical-world observations exchanged between agents, with a
receiver-side source re-read path (04_prior_art_and_field.md, finding 5). INFERRED. The boundary text must not claim
that any element alone is new.

### 1.3 Not claimed: enabling and complementary technologies

| technology | role in EMEM | where | prior art / spec (EXTERNAL unless noted) |
|---|---|---|---|
| BLAKE3 | record hash, Merkle leaves and nodes, preimage digest | `cbor.rs:77-83`, `emem-attest/src/lib.rs:740-751` | BLAKE3 spec: "targets 128-bit security for all of its security goals" (github.com/BLAKE3-team/BLAKE3-specs, blake3.pdf) |
| Ed25519 (`verify_strict`) | attestation, receipt, STH, witness signatures | `emem-storage/src/lib.rs:2188`, `server.rs:711` | RFC 8032 ("around the 128-bit security level", l.160) |
| CBOR | record encoding (ciborium, declaration order, not RFC 8949 §4.2.1 key sort) | `cbor.rs:15-27`; defect 33 | RFC 8949 |
| content addressing | the name of the record | `sled_hot.rs:813-820` | IPFS/IPLD, git; trusty URIs and nanopublications (04 §5) |
| Merkle trees, transparency logs | batch root, RFC 6962/9162 log, STH, consistency | `translog.rs:28-267` | RFC 6962, RFC 9162; Certificate Transparency; Sigstore/Rekor; SCITT (04 §5) |
| signed statements about digests | the attestation and receipt pattern | `attest.rs`, `receipt.rs` | in-toto, SLSA, COSE receipts (04 §5) |
| did:web, JWKS, DNS TXT | publishing the key | trace link 15 | W3C DID, RFC 7517 |
| STAC | finding the scene and its asset URLs | args[11] catalogue | STAC 1.0 (identifies assets) |
| openEO | executing EO workflows | not used | openEO API |
| W3C PROV | expressing derivation | `derivation{fn_key,args}` is a minimal analogue | PROV-O |
| C2PA, CDSE Traceability | signing a file's provenance | not used | C2PA 2.x (04 §2) |
| RAG, agent memory | retrieving and keeping context | `recall` is retrieval by address | MemGPT/Letta, LangMem; ARC arXiv 2607.25066 (closest, 04 §6) |
| MCP, A2A | carrying the reference between runtimes | `/mcp`, agent card | MCP 2026-07-28; A2A 1.0 (04 §2.12) |
| discrete global grids | the cell64 lattice | `emem-codec/src/geo.rs:137-172` | H3, S2 geometry, geohash |
| bi-temporal data | valid time `tslot` and transaction time `signed_at` | `recall.rs:282-391` | Snodgrass, SQL:2011 temporal |
| EO foundation-model embeddings | vectors as model-output records (all four encoders retired on emem.dev) | `fact.rs:102-148` | TESSERA, Clay, Prithvi, Galileo |
| claim checking against EO data | an adjacent layer | not used | GeoGuard (NASA-IMPACT, 04 finding 4) |
| remote attestation of execution | the SAT-042 trace profile (extension, harness only) | `emem-trace/src/verify.rs` | TPM/TEE attestation |

### 1.4 What the boundary forbids on the board

No sentence may imply that EMEM invented any row of 1.3, that a fact_cid hashes the satellite file or pixel, that a
signature or a re-read establishes truth, that the satellite decides, or that SAT-042 is a spacecraft capability.
Section 5 turns this into gate rules; section 6 applies it to the v12.1 text.

---

## 2. Fact CID vs source artifact (issue #12; MASTER §5)

### 2.1 Exact wording

- **3 m:** "The address names the record, not the pixel."
- **1 m (caption under the source to record to CID diagram):** "A fact_cid is the BLAKE3 hash of EMEM's observation
  record. The record names the upstream file (scene id and URL) and carries the values read from it; it does not carry
  a hash of that file."
- **30 cm (method text):** "fact_cid = base32(BLAKE3-256(emem-CBOR(record))), 52 characters. The record holds cell,
  band, tslot, value, confidence, sources (scheme, id or URL, capture time), derivation (function key and arguments:
  scene id, EPSG, DNs, BOA offset, catalogue), privacy class, schema cid, signer and signing time. The operator's key
  signs a Merkle root over the hashes of a batch of records, not each record. No field binds the bytes of the upstream
  file, so the source is identified by name, and a receiver checks it by re-reading it."
- **Forbidden phrasings:** "hash of its bytes" (about an observation), "hash of the pixel / scene / satellite data",
  "signed pixel", "emem signs the value", "the observation is signed", "cid(O) with s inside O",
  "equal values give equal names".

### 2.2 The path, with the code that implements each arrow

```
SOURCE ARTIFACT  S2A_MSIL2A_20260925T054251_R005_T43SFS (COGs B08, B04 on Planetary Computer; SCL)
   | read at the cell node: TM projection (proj.rs:79-147), floor pixel rule (cog.rs:137-169), DN, offset rule
   v
CANONICAL OBSERVATION RECORD  Fact::Primary {cell, band, tslot, value, confidence, sources[], derivation, ...}
   | canonical_float (cbor.rs:43-75), ciborium::into_writer (sled_hot.rs:840-844)
   v
BLAKE3-256  ->  fact_cid oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa  (sled_hot.rs:813-820)
   | leaf = BLAKE3(record bytes); sort; reject duplicates; merkle_root_v1 (attest.rs:105-118)
   v
SIGNED BATCH ATTESTATION  Ed25519(PreimageV1("attestation"){batch_root, registry_cid, schema_cid})  (attest.rs:119-124)
   | entry = BLAKE3(ciborium(Attestation)); leaf = BLAKE3(0x00 || entry)  (translog.rs; algorithms.md §8)
   v
TRANSPARENCY LOG  leaf 2457078 under STH tree_size 2556451  (trace links 12-13)
   v
TOKEN handed between agents  emem:fact:defi.zb572.xoso.zb1ec:oj5cecci...  (cell in the token is re-checked, lib.rs:38231-38235)
```

### 2.3 The real record, field by field (Keylong NDVI, `oj5cecci…`, 1,115 B, re-hashed LIVE 01:02Z)

"Hashed" = inside the bytes the fact_cid names. "Signed" = covered by the attestation signature, which is always
transitive (the leaf is the record's hash); no record field is in the signature preimage directly. "Names upstream"
= identifies an artifact outside EMEM. "Binds upstream bytes" = would let a receiver detect a different upstream file
without re-reading it.

| field | value in this record | hashed | signed (via batch root) | names upstream | binds upstream bytes | serves layer |
|---|---|---|---|---|---|---|
| `kind` | `primary` | yes | yes | no | no | L0 |
| `cell` | `defi.zb572.xoso.zb1ec` (node 32.57125977, 77.03447748) | yes | yes | no | no | L1 |
| `band` | `indices.ndvi` | yes | yes | no | no | L1 |
| `tslot` | 20721 (UTC day 2026-09-25) | yes | yes | no | no | L1 |
| `value` | 0.4708994708994709 (`fb` f64) | yes | yes | no | no | L0/L2 |
| `unit` | absent (Option, omitted) | n/a | n/a | no | no | L1 (gap) |
| `confidence` | 0.95 as f32 (`fa`) | yes | yes | no | no | L2 (SCL rule) |
| `uncertainty` | absent | n/a | n/a | no | no | none |
| `sources[0].scheme` | `sentinel_s2_l2a` | yes | yes | product family | no | L3 |
| `sources[0].id` | two Planetary Computer COG URLs joined by " ; " (path carries `N0513`) | yes | yes | **yes (by URL)** | **no** | L3 |
| `sources[0].captured_at` | `2026-09-25T05:42:51.024000Z` | yes | yes | yes (acquisition time) | no | L1/L3 |
| `sources[0].cid` | absent | n/a | n/a | would | would (for IPLD sources) | L3 (gap) |
| `sources[0].hash` | **absent; never filled by the server** | n/a | n/a | would | **would** | L3 (gap, defect 25) |
| `sources[0].url` | absent here (9 of 213 Keylong sources carry one) | n/a | n/a | would | no | L3 |
| `derivation.fn_key` | `sentinel2_l2a_indices_ndvi@1` | yes | yes | no (EMEM function) | no | L2 |
| `args[0..1]` lat, lng | 32.57125977099409, 77.03447748052537 | yes | yes | no | no | L1/L3 |
| `args[2]` scene id | `S2A_MSIL2A_20260925T054251_R005_T43SFS_20260925T090015` | yes | yes | **yes (product id)** | no | L3 |
| `args[3]` EPSG | 32643 | yes | yes | yes (CRS of the asset) | no | L3 |
| `args[4]` formula note | "NDVI = (B08 − B04) / (B08 + B04) …" | yes | yes | no | no | L2 |
| `args[5]` DNs | [3502, 1900] | yes | yes | values read from upstream | no (values, not bytes) | L2/L3 |
| `args[6..10]` cloud 10.840102, max 40, lookback 30 d, SCL 4, scenes tried 1 | | yes | yes | metadata | no | L3 |
| `args[11]` catalogue | `https://planetarycomputer.microsoft.com/api/stac/v1/search` | yes | yes | yes (catalogue) | no | L3 |
| `args[12]` BOA offset | −1000.0 | yes | yes | convention from baseline | no | L2/L3 |
| reader stamp `reader=cog-pixel-floor@2` | **absent** (signed 09:06Z on 28 Sep, after the fix at 04:09Z, before the stamp commit 128ac75) | n/a | n/a | no | no | L3 (gap) |
| `privacy_class` | `public` | yes | yes | no | no | none |
| `schema_cid` | `d24rgwlq…` | yes | yes | no | no | L0 |
| `signer` | `777er3yi…` as an array of 32 uints | yes | yes | no | no | L0 |
| `signed_at` | `2026-09-28T09:06:56Z` | yes | yes | no | no | L1 (as-of), L3 (fix cut) |
| `served_via` | absent (set for model outputs; carries `model_blake2b_hex` for Clay) | when present | when present | names a checkpoint | **binds a checkpoint digest** (digest rule not in code at 18adb67, algorithms.md §14) | L3 |
| provenance class | **not in the record**: declared per band in the bands manifest, bound to receipts through `bands_cid` (`emem-core/src/bands.rs:55-63`; whitepaper §7.2) | no | no | no | no | L2 (declaration) |
| request (`observed_on`, question text) | **not stored** (algorithms.md §13) | no | no | no | no | L1 (gap, defect 27) |

Sources: decoded from `research/repro/v8/proof_bundle_ndvi.cbor` with `cbor2` (MEASURED); field definitions SPEC
`fact.rs:72-233`; args order SPEC `lib.rs:53033-53051`; reader stamp SPEC `lib.rs:57113` and trace link 9.

### 2.4 Attestation and receipt fields

| object | signed (in the preimage) | carried but not signed | source |
|---|---|---|---|
| attestation | `batch_root` (over BLAKE3 of each record, plus edges), `registry_cid`, `schema_cid`; key is the verifying key | `attested_at`, `attester_key_epoch`, `scope` ("deliberately NOT folded into batch_root or the signature preimage"), `preimage_version` (selects the rule; a flip makes verification fail) | SPEC `attest.rs:11-64`, `emem-attest/src/lib.rs:441-451`; the log entry hash covers the whole attestation, so log inclusion does bind `attested_at` (INFERRED from `algorithms.md` §8) |
| receipt (v2) | request id, served_at, scope/as-of/edges digests, source manifest (`bands_cid`, `registry_cid`, `schema_cid`, `sources_cid`), primitive, cells, fact_cids, field binding, merkle binding | **no value** (the value is bound only through fact_cid) | SPEC `algorithms.md` §7; trace link 10 |

The receipt signature ("this responder served these cids at this time") and the attestation signature ("this
attester signed this batch") are different statements under the same key on emem.dev (trace link 15:
`fact.signer == receipt.responder: True`). emem.dev/verify checks the receipt and re-hashes the record; it does not
check the attestation or the log for a fact token (SPEC `web/verify.html:550-575`).

### 2.5 Consequences a reader must not miss

- **One observation, many names.** `signer` and `signed_at` are hashed, so re-signing identical values gives a new
  cid. Bengaluru elevation 915.0712280273438 m was signed 7 times by one key under 7 cids (MEASURED (committed),
  `contra_bengaluru.json`); emem's own note measured three responders, one reading, three cids (SPEC,
  `.well-known/agent-notes/AGENT_NOTE_fact_cid_is_not_portable.md`). A fact_cid identifies an attestation of an
  observation by one responder, not the observation.
- **One name, unbound upstream bytes.** The same Planetary Computer URL could serve different bytes later (mutable
  path, reprocessing) and the record would not show it; the STAC item carries no `file:checksum` (trace link 8:
  "STAC asset file:checksum present: False"). The only binding available today is a separate signed byte-range
  witness, `POST /v1/range_hash`, which the fact does not reference (trace link 9c; SPEC `range_hash.rs:1-28`).
- **The field doc and the one filler disagree.** `fact.rs:210-212` says `hash` is "SHA-256 of source bytes"; the
  only code that fills it, the `emem-realdemo` binary, stores BLAKE3 of a byte range (`emem-realdemo.rs:152-158`).
  A future filler must fix the algorithm in the schema. SPEC.
- **Parent links are bound, upstream links are not.** Derived facts set `Source.cid` to their parent fact cids
  (`lib.rs:56731`, `:56739`), so EMEM-to-EMEM lineage is hash-bound while EMEM-to-archive lineage is name-only. SPEC.

### 2.6 Upgrade path (issue #7; INFERRED recommendations, not current behaviour)

Fill `Source.hash` from the catalogue where one exists (Earth Search C1 and CDSE publish per-asset checksums, 04
finding 3), or from a `/v1/range_hash` read of the exact tile, and reference that receipt from the record; fix the
hash algorithm in the field name; stamp the reader version on every raster read; store the requested date beside the
served one; mark records with no upstream binding as "upstream identity: by name only". Until then the poster must
say "names", never "binds", for the upstream file.

---

## 3. The verification ladder (issues #17, #29; MASTER §11)

### 3.1 Status vocabulary

- **CHECKABLE**: the receiver decides it offline, with stock libraries, from what it was handed plus its own question.
- **RECOMPUTABLE**: the receiver can re-execute the declared derivation (L2) or re-read the named open source (L3)
  and compare bits.
- **INHERITED**: it rests on the signer or the upstream producer; the record gives the receiver nothing to recompute.
- **PARTIAL**: checkable or recomputable for some sources or classes and inherited for others.
- **OUT OF SCOPE**: no reference protocol can establish it.

"Verified" is never used alone: write "re-hashed (L0)", "signature-checked (L0)", "in the log (L0)", "bound to the
question (L1)", "recomputed (L2)", "re-read (L3)".

### 3.2 The ladder

| layer | question | check (R1 letter) | status | R1 first refusal | measured evidence | cost (08_cost_overhead.md) | what stays trusted |
|---|---|---|---|---|---|---|---|
| **L0 record integrity** | are these the exact bytes the pinned key attested and logged? | resolve (C), re-hash (D), attestation signature and batch root (F), log inclusion and consistency (G) | CHECKABLE | C: M1, M2, M7; D: M3; F: M8-M13; G: M16 | R1; 780/780 facts (`eo_evidence_per_fact_checks.csv`); 30/30 rawband cids; 207/207 through a TLS-intercepting proxy (08) | hash 1.57 µs; Ed25519 67.7 µs; resolve 40 ms warm; locating the log entry 4.9 s and 1.97 MB online, 0 with the 4.8 KB bundle | the key-to-operator binding (Web PKI, DNS without DNSSEC); a head others also see |
| **L1 observation identity** | does the record describe the cell, band, time (and scene) I asked about? | binding of record fields to token and question (E) | CHECKABLE (declared fields) | M4, M5, M6 | trace links 4-5; 409 on a relabelled token (`lib.rs:38231-38235`), G2 forged arm 5/5 declined; Bengaluru as-of | +0.010 ms | the receiver's own question; responder selection of "latest" |
| **L2 derivation** | does the value follow from the recorded inputs by the named function? | recompute (H) | RECOMPUTABLE where inputs are in the record (266 of 780), else INHERITED | M14 | trace link 7, bit-identical `0x3fde233788cde233`; 266/780 bit-identical | below noise | the function's meaning; the convention (offset) the signer chose |
| **L3 upstream provenance and source re-read** | do the recorded inputs equal the named upstream artifact at the named pixel? | re-read the pixel (I) + catalogue metadata (trace link 8) + byte-range witness (9c) | PARTIAL | M15 (only I catches it) | trace links 8, 9, 9b, 9c; 162/200 pre-fix records; `kxjvfwpa` | 6.9 s and 1.18 MB cold per pixel | that the archive's file is the product (no checksum); the pixel rule; mutable or non-file sources |
| **L4 semantic / entity** | is this cell the thing the sender meant? | none | OUT OF SCOPE | M17 accepted at every level | defect 21 (Maasvlakte); defect 37 (town point 597 m away) | n/a | everything |
| **L5 physical truth / decision** | is the value right about the world, and is acting on it right? | none | OUT OF SCOPE (decision); INHERITED (product accuracy) | n/a | GFC2020 commission error 13 to 18 % (05, EXTERNAL); constructed R3 rule | n/a | the product's validation; the user's rule |

### 3.3 Each layer in detail

**L0 record integrity (CHECKABLE).**
- *Checks.* (a) Resolve the token and fetch the record bytes (`GET /v1/facts/<cid>`, `Accept: application/cbor`);
  (b) `base32(BLAKE3(bytes)) == fact_cid`; (c) the bytes sit in an attestation whose recomputed batch root and Ed25519
  signature verify under the pinned key; (d) the attestation entry is included under a signed tree head, and that head
  is consistent with one pinned earlier or co-signed by a witness.
- *R1.* Resolving (C) protects B from M1, M2 and M7 because B uses the record's value, not A's text; D refuses M3; F
  refuses M8 to M13, the forgeries that re-hash consistently; G refuses M16. Leave-one-out: without D nothing gets
  through, because F recomputes the batch root from the record hashes (MEASURED (committed),
  `research/repro/v11/out/summary.md`; re-run here, summary identical).
- *Measured.* Live re-hash of `oj5cecci…` at 01:02Z: equal (MEASURED). 780/780 facts pass every L0 check, including
  log inclusion with a flipped-leaf negative control (MEASURED (committed)). 30/30 cited cids in the v9 run re-hash
  (MEASURED (committed), `research/repro/data/v9/rawband/results.md`).
- *Limits.* The receipt does not chain to the log, and there is no `fact_cid -> leaf_index` index, so (d) needs a scan:
  21 bisection probes plus 256 entries (trace link 12; whitepaper §8.4, `docs/protocol.md:1462-1463`, SPEC). G's
  catch of M16 assumes B's head is one others see; a first-contact client "cannot detect a split view" (trace link 13;
  whitepaper §8.3). emem's head was not independently witnessed at 01:02Z (LIVE).

**L1 observation identity (CHECKABLE, against the receiver's own question).**
- *Checks.* `record.cell == token cell == asked cell`; `record.band == asked band`; `record.tslot == asked day`;
  `record.signed_at <= as-of bound` for a historical question; `args[2]` scene id or product version if the question
  names one; unit against the band registry (not implemented in R1 or the board's verifier).
- *R1.* E refuses M4 (another cell), M5 (an older record as current), M6 (another band). In-record changes that
  re-hash (M9, M10) are refused by F, not E.
- *Measured.* Trace link 4: a wrong-cell token returns HTTP 409 and the cell equality holds offline. G2: a forged
  wrong-cell token was declined 5/5 by Claude Haiku, through the server's 409 (MEASURED (committed),
  `research/repro/data/v8/results.json`). v9: asked for 23 Sep, 9/10 agents were served the 25 Sep scene; each served
  record carried tslot 20721 and `captured_at` 25 Sep, so an L1 comparison with the question detects it, and no agent
  made it (MEASURED (committed), `results.md`). Detectable is not detected.
- *Limits.* tslot is a UTC day: two Sentinel-2 scenes at the Keylong pixel on 25 Sep (S2A R005 0.4709, S2B R105 0.4370)
  share tslot 20721, so only the scene id tells them apart (05 §0 item 5, MEASURED there). "Latest" and "complete"
  are the responder's selection: the log "cannot prove absence, non-omission" (whitepaper §8.3). If the receiver takes
  its question from the sender, E checks nothing (INFERRED from `mutation_suite.py:372-375`).

**L2 derivation (RECOMPUTABLE where the record carries the inputs, otherwise INHERITED).**
- *Check.* Recompute the value from `fn_key` and `args`; compare IEEE-754 bits.
- *R1.* H refuses M14 (the signer's value disagrees with its own DNs).
- *Measured.* Trace link 7 bit-identical. 266 of 780 board facts recomputed bit-identical; 514 (raster reads of DEM,
  WorldCover, CCI, GSW, Hansen, GFC2020, TMF, CAMS, MODIS, Overture) carry no inputs to recompute (MEASURED
  (committed), `eo_evidence_verification.md` step 6).
- *New, MEASURED this session.* A signer that records offset 0 for this baseline-05.13 scene and computes the value
  consistently passes H, and also D to I; B acts on 0.2966 and the decision flips (`r1_t2_extra_out.json`).
  Recompute checks arithmetic, not convention. The offset follows from the scene's processing baseline
  (`s2:processing_baseline >= "04.00"` gives −1000 on Planetary Computer, algorithms.md §5), which only a metadata
  re-read checks (trace link 8: "processing_baseline 05.13 >= 04.00 -> offset -1000.0 == args.dn_offset: True").
- *Limits.* Argument positions are labelled from the emitter source, not a published per-function schema (trace link 6
  residual). The provenance class is "an editorial declaration, not a measurement" (whitepaper §7.2). The server's own
  derive recompute runs only for `delta`, `mean`, `sum` with a pinned `code_cid` (algorithms.md §10).

**L3 upstream provenance and source re-read (PARTIAL).**
- *Checks.* (a) Catalogue metadata: the STAC item for `args[2]` has the same datetime (→ tslot), EPSG, cloud, baseline
  (→ offset) and asset hrefs as the record (trace link 8, all True). (b) Pixel: range-read both COGs at the cell node
  with an independent TIFF decoder and projection, apply the floor rule, compare DNs (trace link 9: DN 3502/1900 equal;
  pyproj agrees to 2.3e-10 m). (c) SCL class (9b). (d) Byte-range witness: emem's signed BLAKE3 of tile #413 equals
  ours (9c).
- *R1.* I refuses M15 and is the only check that does (leave-one-out: without I, M15 gets through).
- *Measured.* Before the reader fix, 162 of 200 sampled Sentinel-2 records carry the neighbour pixel's DNs (Wilson 95 %
  0.750 to 0.858); after, 0 of 54 (provider-confounded, all Planetary Computer, 05 §8 item 8) (MEASURED (committed),
  `research/repro/data/v8/prevalence_summary.json`). `kxjvfwpa…` passes L0 to L2 in the 780 check (`verified=PASS`,
  `recompute=pass`) and its containing pixel gives NDVI 0.4860 against the signed 0.3444 (MEASURED (committed),
  `pixel_check.json`).
- *New, MEASURED this session.* A same-day scene id relabelled by the signer, with the DNs unchanged, passes D to I,
  because R1's I compares against the committed 25 Sep window and does not follow the record's scene id. A re-read that
  follows `args[2]` would fetch the S2B scene and see different DNs (INFERRED; S2B DNs 1014/2588 per 05 §6).
- *Why PARTIAL.* No upstream hash is bound (section 2.3). The archive copy is not bound to ESA's product: "nothing binds
  Microsoft's COG bytes to ESA's product" (trace link 9 residual). Several products name a mutable path, a directory or
  an API query instead of a file (00_v11_review_findings F07: FIRMS, CAMS via Open-Meteo, TESSERA truncated path,
  GFC2020 LATEST). The pixel rule (floor, PixelIsArea) is emem's choice. A fixed reader does not retire old records:
  "The old fact stays in the log and still verifies" (SPEC `lib.rs:12645-12651`); the server stops answering them as
  latest (`superseded_read`, `lib.rs:12676-12696`), but a receiver holding an old token must apply the cut itself,
  and the reader stamp is missing on early post-fix records such as `oj5cecci` (trace link 9).

**L4 semantic / entity correctness (OUT OF SCOPE).**
- M17 (same record, A meant a different physical entity) is accepted at every level A to I (MEASURED (committed)).
- Defect 21: "Maasvlakte ramp 7" resolves to OSM relation 1411107, an administrative boundary of about 12 × 10 km.
  Defect 37: `/v1/ask` with explicit coordinates answered from the town point 597 m away, cell `defi.zb572.xAnI.zb1a2`
  (MEASURED (committed), `research/repro/data/v11/ask_keylong.json`).
- What EMEM adds here is auditability, not detection: the `located` stage of the answer's `emem:state` chain records
  the resolved cell, and all four stage addresses recompute from their published fields (MEASURED this session:
  `python3 recompute_state.py ask_keylong.json verifier_spec.json` → located, routed, recalled, scored: True).
- emem's entity layer ranks candidates by distinct asserting keys (SPEC `docs/security/threat-model.md:21`): a count of
  corroboration, not a correctness check.

**L5 physical truth and decision correctness (OUT OF SCOPE; product accuracy INHERITED).**
- Product accuracy is the producer's validation (GFC2020 V2 forest commission error 18 %, V3 13.1 %, EXTERNAL via 05).
- The R3 rule `IRRIGATE if NDVI <= 0.4705` is "a constructed boundary test" (MEASURED (committed),
  `research/repro/data/v8/prereg.md`).
- G2: B decided correctly 10/10 from the token and 10/10 from prose, because A's prose kept 16 significant digits; the
  handoff method does not change decision correctness when the value survives (MEASURED (committed)).

### 3.4 R1 mutations mapped to layers (all 17, the control, and three new probes)

| id | corruption | threat | first refused at | layer |
|---|---|---|---|---|
| G0 | none | none | never refused (correct) | control |
| M1 | stated value +1 ULP | T1 | C (resolve) | L0 entry |
| M2 | stated value rounded to "0.47" | T1 | C | L0 entry |
| M3 | 1 ULP inside the served bytes | T1 | D | L0 (hash) |
| M4 | record cited for another cell | T1 | E | L1 |
| M5 | older record as the current answer | T1 | E | L1 |
| M6 | record for another band | T1 | E | L1 |
| M7 | token miscopied by one character | T1 | C | L0 entry |
| M8 | value 0.45, re-encoded, re-hashed | T1 | F | L0 (attestation) |
| M9 | cell changed inside the record, re-hashed | T1 | F | L0 protecting L1 |
| M10 | tslot changed, re-hashed | T1 | F | L0 protecting L1 |
| M11 | source scene id changed, re-hashed | T1 | F | L0 protecting L3 |
| M12 | offset changed, value recomputed, re-hashed | T1 | F | L0 protecting L2 |
| M13 | value 0.45 signed and logged under the forger's key | T1 | F | L0 (key pinning) |
| M14 | signer's value disagrees with its DNs | T2 | H | L2 |
| M15 | signer read the pixel 10 m south | T2 | I | L3 |
| M16 | second signed version shown only to B | T2 | G | L0 (log), if B's head is shared |
| M17 | A meant a different entity | T1 | never | L4 |
| P1 (new) | signer records offset 0, value consistent | T2 | **never in D-I** | L3 metadata (trace link 8) |
| P2 (new) | signer relabels a same-day scene id | T2 | **never in D-I** | L3 re-read following the scene id |
| P3 (new) | signer adds a wrong unit | T2 | **never in D-I** | L1 unit check against the band registry |

P1 to P3: MEASURED this session with R1's unmodified verifier from a scratch copy
(`scratchpad/v13ladder/r1_t2_extra.py`, output `r1_t2_extra_out.json`; P1 value 0.29655683080340617, decision
flipped; P2 and P3 value unchanged). Nothing was signed with emem's key; the probes use R1's public-string TEST key.
Recommendation (INFERRED): add P1 to P3 to R1-v13 and add the catalogue-metadata check as level I′; report "0 of N in
this suite" with N stated.

### 3.5 What "verified" meant on the v12.1 board, by layer

| board item | L0 | L1 | L2 | L3 | source |
|---|---|---|---|---|---|
| 780 facts (sections 1, 3) | 780/780 | 780/780 (cell, band) | 266/780 | 0/780 | `eo_evidence_per_fact_checks.csv` (MEASURED (committed)) |
| Keylong series, 155 facts | 155/155 | 155/155 | 155/155 | 0/155; 14 pre-fix, at least 2 proven wrong pixel (F01) | same; `pixel_check.json` |
| hero record `oj5cecci` | all | all | bit-identical | DN, SCL, STAC, byte-range all equal | trace links 1-15 |
| emem.dev/verify ("Check any token") | re-hash + receipt signature | cell reported by the server | no | no | SPEC `web/verify.html:550-575` |
| G2 harness on B's resolves | 10/10 re-hash and receipt | n/a | no | no | `results.json` |
| R1 level I | D, F, G | E | H | I against the committed window | `mutation_matrix.json` |

### 3.6 The two-sided boundary figure (issue #29), with the same vocabulary

| CHECKABLE or RECOMPUTABLE from the reference | NOT ESTABLISHED by the reference |
|---|---|
| L0: the record's bytes, its content address, the attestation under the pinned key, its place in the log | that the key's operator is honest or independent |
| L1: the declared cell, band, valid time, scene and signing time, against your question | that "latest" is the newest that exists |
| L1: the as-of state: which record was signed by a given time | that the history is complete |
| L2: the value, recomputed bit-for-bit from the recorded inputs (deterministic indices) | that the recorded convention (offset, unit) is right |
| L3: the recorded inputs against the named open-archive file and pixel | that the archive file is the producer's product; any upstream hash |
| | L4: that the cell is the field, plot or entity the sender meant |
| | L5: sensor and product accuracy; that a decision taken on the value is right |

Figure data per row: the one measured example in 3.3 (M3 / M4 / Bengaluru / trace link 7 / M15 and `kxjvfwpa` /
M17 and defect 37 / GFC2020 commission error).

### 3.7 emem's own errors are one layer's failure class (why the ladder matters)

Each row: an error emem shipped and fixed or still carries; the layer whose check detects it; what a pipeline without
a record has to check against (INFERRED in the last column). Details and outside occurrences: 05_failure_modes, 02 §18.

| emem error (source) | detected at | without a record |
|---|---|---|
| COG reader rounded the pixel index; 162/200 records carry neighbour DNs (`CHANGELOG.md:68`, prevalence) | L3 only | the DNs and the pixel are gone after the first summary; nothing to re-read |
| BOA offset per catalogue; one pixel gives 0.4709, 0.2966 or 1.1427 (05 F2) | L3 metadata (P1) | the convention is not stated anywhere downstream |
| `band_raster observed_on=23 Sep` served the 25 Sep scene; 9/10 agents (defect 27) | L1 (served tslot vs asked date) | the served date is never stated |
| 918.0 m (GLO-90 via Open-Meteo) and 915.07 m (GLO-30) under one band name (`contra_bengaluru.json`) | L1 (`fn_key`, scheme) + as-of | the earlier value is overwritten; an earlier citation cannot be checked |
| pre-fix and superseded releases still served as "latest" until fixed (`lib.rs:12645-12696`) | L1 (`signed_at` cut) + L3 | staleness is invisible |
| `/v1/ask` took the place name over the coordinates, 597 m (defect 37) | L4: not detected; the state chain records it | the wrong place is reported in good prose |
| 7 identical re-signings counted as 7 attestations (defect 5); one Vortx domain called independent (defects 1, 30) | trust model: count distinct operators, not keys | copies look like corroboration |
| `/verify` once showed a pass without checking a signature (`CHANGELOG.md:735-736`) | receiver-side verification with independent code | there is no verifier to audit |

The poster sentence this supports, at the strength the evidence allows: "Every error we found in emem is one any agent
pipeline over EO data can make; the record is what makes each one checkable at a named layer." The signatures did not
prevent any T2 error (02 §18); what the record bought is that each error was checkable at handoff or auditable after.

### 3.8 Reconciliation with reports 05 and 08

- 08 places "attestation signature" and "log inclusion" in rows labelled *cryptographic trust* between L1 and L2. In
  this canonical ladder they are L0's sub-checks F and G (they protect the L1 fields against re-hashing forgers, M9,
  M10). Same checks, same numbers; only the row label changes.
- 05's "catastrophe ladder" ranks failure classes by the deepest check they survive and uses L0 to L5 for "lost in the
  handoff" up to "wrong product". Its rungs map one to one onto these layers (05-L0 → resolve/L0, L1 → L1, L2 → L2,
  L3 → L3, L4 → L4, L5 → L5). Use one vocabulary on the board: this report's layer names, 05's examples.

---

## 4. Threat model (MASTER §12)

### 4.1 Parties and assets

Agent A (sender), agent B (receiver), the channel between them (relay, mirror, RAG store, compaction), the responder
and attester (emem.dev, one key `777er3yi…`), the transparency log and its witnesses, the upstream archive (Planetary
Computer or Element84 copy of the ESA product), the receiver's own verifier code. Asset: B's decision input, the value
B acts on and what it claims to be about.

### 4.2 Attacker and failure classes

| class | capabilities | R1 / probe | detected at |
|---|---|---|---|
| T0 lossy channel (not adversarial) | paraphrase, round, compact, truncate | M1, M2 | L0 entry (resolve) |
| T1 relay, mirror or forger without the pinned key | controls every byte B receives about the evidence: prose, JSON, token, record, attestation, log responses from a mirror; replays old records; relabels tokens; re-encodes and re-hashes; signs with its own key | M1-M13, M17 | L0, L1 (M17: never) |
| T2 the trusted signer errs or equivocates | holds the pinned key; signs wrong arithmetic, a wrong pixel, a wrong convention, a relabelled scene, a second version for one client | M14-M16, P1-P3 | L2, L3, L0 log (if heads are shared); P1-P3 not in R1 |
| T3 compromised signing key | signs anything as emem.dev | none | out of scope; for open data, L2 and L3 still detect false values |
| T4 upstream producer or mirror | wrong calibration, reprocessing under one name, mutable paths, catalogue metadata contradictions | 05 F2, F4 | L3 partially (only against the archive, never against "truth") |
| T5 entity and semantics | right record of the wrong thing | M17 | out of scope |
| T6 receiver failure | a verifier bug, a model that skips the check, a fail-open tool | 05 F14; v9 | outside the protocol; mitigated by independent verifier code and fail-closed tools |

### 4.3 What the attacker cannot do, and the exact conditions

- **Forge an attestation under the pinned key without the key.** Ed25519 operates "at around the 128-bit security
  level" (RFC 8032 l.160, EXTERNAL). emem verifies with `verify_strict` (`emem-storage/src/lib.rs:2188`,
  `server.rs:711`), which also rejects small-order keys and non-canonical R (ed25519-dalek docs, EXTERNAL); a receiver
  should verify strictly too. Condition: B pins the right key (4.5).
- **Produce different record bytes with the same fact_cid.** BLAKE3 "targets 128-bit security for all of its security
  goals … (second-)preimage, collision" (BLAKE3 spec, EXTERNAL). Condition: the full 32-byte name. fact_cid and
  state_cid are 32 bytes (`cid.rs:35-38`: "Full 32 bytes … because a consumer SKIPS bytes on the strength of it").
  Several other names are 16-byte truncations (`reason_cid`, `bundle_cid`, note cids, the track chain: algorithms.md
  §6, §9; defect 24), whose generic collision bound is about 2^64 (INFERRED). `/memories/by_attester/<8 chars>` is a
  40-bit prefix that the first writer can squat (defect 11).
- **Rewrite logged history unseen by someone who pinned a head.** RFC 9162 consistency proofs; trace link 14 checks
  one. Condition: B or a witness pinned an earlier head; detection of a split view needs comparison between clients
  ("gossip … an active area of research and not defined here", RFC 9162, EXTERNAL).

### 4.4 Explicitly out of scope

Compromised signer (T3); incorrect sensor or product (T4 against truth); upstream substitution where the archive is
not open or not immutable; semantic or entity misidentification (T5, L4); downstream decision correctness (L5);
availability (a responder can refuse to serve); completeness ("does not prove the log is complete", whitepaper §8.3);
privacy of what was asked.

### 4.5 Three kinds of trust

| trust | what B learns | what B must assume | evidence today |
|---|---|---|---|
| **cryptographic** | these exact record bytes were attested by key K and appended to a log under head H (L0) | K is the key B meant: published by did:web, JWKS, `/.well-known/emem.json` and DNS TXT, all controlled by whoever runs emem.dev; DNS answers had AD=false (no DNSSEC) | trace link 15 |
| **source** | the record names scene S, file U, catalogue C; for open archives, the inputs equal U's pixel (L3) | K read U honestly when B does not re-read; U's bytes are the producer's product; the log view is not split | Source.hash never filled; one operator; head not independently witnessed (LIVE) |
| **measurement** | nothing beyond the record | the sensor and product are accurate; the pixel rule and convention are right; the cell is the entity meant | product validation (EXTERNAL); M15, P1, M17 |

### 4.6 emem-specific trust facts (for the 30 cm text)

- **One operator.** emem.dev, its self-witness `k572x7go…` and geo.qa's witness are Vortx AI. geo.qa's page:
  `<meta name="creator" content="Vortx AI Private Limited"/>`, `publisher` the same, `author` "Vortx AI Team" (LIVE).
  `docs/security.md:250` calls geo.qa "one independent operator" (SPEC; mislabel, defect 1).
- **Witnesses (LIVE 01:02:45Z, tree size 2,574,778).** `witness_keys_by_tier`: key_only 109, org_vouched 2 (geo.qa),
  self_operator 1; `independent_operator_count` 1; `head_is_independently_witnessed` false; freshest independent
  co-signature 40 entries behind. The endpoint's own note: key_only "proves someone holds the key and nothing more;
  keys are free". Whitepaper §8.5: "Witnesses are scaffolding, not a network" (SPEC).
- **Write side.** The fact plane is closed by default: only the responder key, a trace-enrolled device or an
  operator-listed key may write (`docs/security/threat-model.md:19`, SPEC). Read tools still sign and store new records
  (defect 29), so a receiver's own reads can mint new cids for old values.
- **Responder vs client.** "The responder does not recompute the digest on read … The *client* can and should
  recompute it" (whitepaper §3.2, l.433-438, SPEC).
- **Transport.** Integrity held through a TLS-re-terminating proxy: 50/50, 30/30 and 207/207 re-hashes (08 finding 6,
  MEASURED there). L0 does not depend on TLS; key discovery does.
- **Verifier surfaces.** emem.dev/verify gates itself on replayed signer vectors and "verifies via the server" if they
  fail (`web/emem-verify-core.js:10-11, 69`, SPEC): in that fallback the signer vouches for itself, so a poster QR to
  /verify is an L0 convenience, not an independent check.

### 4.7 Poster copy for the threat box (about 70 words)

> **Who can corrupt a handoff, and what stops them.** A relay or forger can change values, cells, dates, sources and
> references, or replay old records: the record's hash, the attestation and the cell, band and time binding refuse
> them. The signer itself can misread a pixel: only a re-read of the open source catches it. No reference can tell a
> wrong sensor, a wrong entity or a wrong decision. All keys today are one operator's.

---

## 5. Claim-status gate (issue #21): specification

Describe-only; `poster/build_v12.py` is not edited.

### 5.1 Statuses and the evidence each requires

| status | meaning | required evidence fields | wording rule |
|---|---|---|---|
| SPEC | stated by emem code or docs | `repo`, `commit`, `path:line` | "emem's code / docs" as subject; never "we found" |
| LIVE | read from a live service | `url`, `utc`, saved response path and its BLAKE3 | date printed; must be re-fetched within 7 days of print (19 Oct) or downgraded to "on <date>" |
| MEASURED | output of a committed script on committed inputs | `script`, `output`, JSON pointer, `n`, denominator | number printed with its denominator; the gate asserts equality with the pointer's value |
| PRE-REGISTERED | measured under a pre-registration hashed before trial 1 | prereg path, prereg BLAKE3, results path, authorship | "pre-registered", and "emem-authored" when it is |
| INFERRED | arithmetic or reading from the above | input claim ids, formula | hedged ("implies", "about") or marked |
| OUT-OF-SCOPE | what EMEM does not establish | ladder layer (L4/L5) and one measured example | phrased as a negation |
| EXTERNAL | third-party fact | URL, retrieval date 2026-10-01, quoted span | never phrased as an EMEM result; analogues labelled "outside EO" |

Every claim also carries `layer` ∈ {L0, L1, L2, L3, L4, L5, n/a}; any claim using check, refuse, accept, resolve or a
`verif*` word must have a layer other than n/a.

### 5.2 Claim registry

One file, `research/v13/claims_registry.json` (proposed path), a list of objects:
`{id, text_sha (BLAKE3 of the normalised sentence), section, status, layer, evidence{...}, value?, pointer?,
denominator?, allow?: [{word, reason, evidence}]}`. In the board source each substantive element carries
`data-claim="<id>"`. Figures carry `data-claim` on the `<!--inline:-->` include or, for matplotlib output, a sidecar
`fig/v13/<name>.claims.json` listing the claim id of each text label, written by `make_figures` from the same data.

### 5.3 Banned words and the allowlist rule

Banned unless the sentence's claim id lists the word in `allow` with an evidence path that exists:

- novelty and absolutes: first, only, unique, novel, never, always, impossible, cannot (as a capability claim),
  every, all, any, none (universal quantifiers pass automatically when followed by a count, "all 15", "none of the 16",
  and the number gate then checks the count);
- truth and guarantee: true, truth, truly, correct (about a value), guarantee(s/d), prove(s/n), proof (except the
  technical terms "inclusion proof", "consistency proof", "Merkle proof"), certain, certified;
- security absolutes: immutable, tamper-proof, tamper-evident (allowed with a layer), trustless, secure, zero-trust,
  unforgeable;
- agency: decides, arbiter, judge (for satellites, signatures or EMEM), "the satellite";
- verification without a layer: verify, verified, verifies, verifiable, verification (title exempt: it is the official
  programme title, and the ladder defines it);
- CID wording: "hash of (its|the) (bytes|pixel|file|scene|image|data)" when the subject is an observation, "signed
  pixel", "signs the value", "the observation is signed", "equal values give equal";
- SAT-042 and deployment: spacecraft, satellite (as the subject of prove/run/write), in orbit, on board, onboard,
  downlink, flight, operational, deployed, production (allowed for emem.dev's reader with a date); each needs one of
  {harness, reference run, scripted, not a spacecraft, no spacecraft} in the same element or a section marked
  `data-status="EXTENSION"`;
- independence: independent (operator, witness, replication) unless the claim cites an organisation other than Vortx AI;
- compliance: compliant, compliance, due diligence, regulatory (allowed only in a negation: "not a regulatory
  determination").

Allowlist rule: an entry is bound to the sentence by `text_sha`; editing the sentence voids the entry; the evidence must
be a MEASURED, SPEC or EXTERNAL claim id, never INFERRED. Example: "only the re-read stops M15" is allowed with
evidence `mutation_matrix.json#/leave_one_out/I == ["M15"]`.

### 5.4 Structural rules

1. Every text node in `<main>` and `<header>` (after inlining figures) belongs to a `data-claim` element or to an
   exempt class (kicker, section number, axis tick).
2. Every number in prose belongs to a claim whose status is MEASURED, LIVE, PRE-REGISTERED, SPEC or EXTERNAL, and the
   printed string equals the registry value (the v12 claims-map assertion, `claims_map_v12.py:26-29`, made mandatory
   and extended to figure labels).
3. "fact_cid", "CID", "content address" or "token" within one sentence of "pixel", "scene", "file" or "satellite"
   requires the word "record" in the same sentence.
4. A sentence with a `verif*` or check word must carry a layer tag, either printed ("(L0)") or as `data-layer`.
5. R1 results must state the suite bound: "of the 16 in this suite" (or "in R1"), because P1 to P3 exist.
6. LIVE claims older than 7 days at build time fail unless re-fetched.
7. OUT-OF-SCOPE claims must be negations; a positive sentence about L4 or L5 fails.
8. Figure text is gated like prose.

### 5.5 How to extend `poster/build_v12.py` (describe only)

- Add `figure_text(html)` before `prose_gate`: for each `<!--inline:path-->`, read the SVG and collect matplotlib's
  label comments (`re.findall(r"<!-- (.*?) -->", svg)`; matplotlib writes every text as glyph paths preceded by such a
  comment, confirmed in all 12 figures of `poster/fig/v12/`). Today `prose_gate` deletes `<svg>…</svg>` and all
  comments first (`build_v12.py:43`), so no figure word is ever gated.
- Add `claim_gate(html, figtext)` after `prose_gate`: parse with `html.parser`; load the registry; fail on rules 1 to 8
  and on banned words without a matching allowlist entry; print `GATE FAIL (claims): <file:line> <rule> <match>
  <context>` per finding; exit non-zero on any. Unknown status, missing evidence path, or an unreadable pointer is a
  failure, never a skip (the file's own rule, `build_v12.py:6`).
- Call order in `main()`: `run_figures()` → `inline()` → `figure_text()` → `prose_gate()` → `claim_gate()` →
  `qr_gate()` → `layout_gate()`. Write the registry-joined claims map as a build product so the printed map and the
  board cannot drift.
- CI: a workflow on pull requests that runs `python poster/build_v13.py --no-figures` with the gates and uploads the
  findings; the build fails on the first finding.

### 5.6 Prototype run on the v12.1 board (MEASURED this session)

`python3 scratchpad/v13ladder/claim_gate_proto.py` (lexical rules of 5.3 only, with the count exemption) on
`poster/src/poster.v12.html` plus inlined figure text: **36 findings**, 29 in the HTML and 7 in figure text (`claim_gate_proto.txt`,
`claim_gate_proto.out.json`). The figure findings: model.svg, the signature formula, "equal values give equal",
"never" and "only" (the last a false positive on "append-only", which the word rule must exempt); encoding.svg,
"verified device trace"; m15.svg, "Only" and "all" (both allowlistable with the leave-one-out evidence). The present `prose_gate` reports 0 on the same input. Every finding of section 6 that is
lexical is among the 36; the semantic ones (for example "the source bytes / guaranteed" read as a CID claim, or "a fact
the trace never emitted") need rules 3 and 7 or a human reviewer, which is why rule 1 forces every sentence into the
registry.

---

## 6. Every boundary violation on the v12.1 board, with a corrected version

Scope: every text node of `poster/src/poster.v12.html` (line numbers of that file) and the text of the figures it
inlines (`poster/fig/v12/*.svg`, matplotlib label comments). Severity: **H** changes what a reader believes EMEM
establishes; M imprecise; L wording. Earlier review ids (00_v11_review_findings) are cited where they found it first.
Corrected versions avoid em dashes (the board's prose rule).

| # | where | current text | violation | corrected text | sev |
|---|---|---|---|---|---|
| 1 | L111 h1 | "…over Earth-Observation Products, Foundation-Model Embeddings and Signed Execution Traces" | extends the official programme title; puts the SAT-042 extension in the title (#14) | print the programme title verbatim: "EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings", with the contribution line beneath it | M |
| 2 | L112 punch | "Agreement is not evidence. The pixel is." | crowns the pixel as truth (#13, L5); M15 is a signed wrong pixel (F14) | "Agents hand each other evidence references, not paraphrases." | **H** |
| 3 | L113 | "Every number an agent cites resolves to signed bytes and names the file it came from; open-archive pixels can be re-read." | universal; only emem tokens resolve; several facts name no file (F07); bytes are the record's | "An EMEM reference resolves to a signed observation record that names its source; open-archive pixels can be re-read." | **H** |
| 4 | L116 QR | "Check any token" | "any"; /verify checks L0 only and falls back to the server | "INSPECT THE RECORD: re-hash a token and check its receipt (L0)" | M |
| 5 | L125 | "Agents that agree are not agents that are right." | universal; the control arm agrees 36/36 and is right 72/72 (F15) | "Agents sharing a summary can agree and be wrong." | M |
| 6 | L126 | "Each summary or handoff re-encodes a reading: the words survive, the referent does not." | universal "each … does not" | "A summary or handoff re-encodes a reading: the words can survive while the referent is lost." | L |
| 7 | L128 | "Pre-registered compaction study, Gemma-4-12B and Qwen2.5-7B on one host. Under pressure, the 3 pairs that still agree are all wrong." | status incomplete: emem-authored, one writer model (F16) | "emem-authored, pre-registered; Gemma-4-12B wrote every summary that it and Qwen2.5-7B read. Under pressure 3 pairs agree, all wrong." | M |
| 8 | L132 | "Name each satellite observation by the hash of its bytes." | **the CID is not a hash of the observation or the pixel** (#12, SHARED §5) | "Write each observation as a signed record, and name the record by its BLAKE3 hash." | **H** |
| 9 | L133 writer path | "Sentinel-2 pixel → record: cell, band, time, value → BLAKE3 → emem:fact:…" | the record omits source, derivation, signer and time; the signing step is missing | "Sentinel-2 file (scene id, URL) → read → record: cell, band, time, value, source, inputs, signer → BLAKE3 → signed batch → emem:fact:…" | **H** |
| 10 | L134 receiver path | "resolve → re-hash → compare → re-read the pixel" | omits signature, binding, recompute; no layers | "resolve → re-hash, check signature (L0) → match cell, band, time (L1) → recompute (L2) → re-read the pixel (L3)" | M |
| 11 | L136 | "a 64-bit cell id of about 10 m does not [drift]" | the cell is a lattice node, about 9.5 m N-S and 5.8 to 8.1 m E-W here (F19); the place mapped to it can still be wrong (L4, defect 37) | "a 64-bit cell id names one lattice node and does not; which place it is for is still the sender's claim." | M |
| 12 | L137 | "a fact_cid breaks if one bit changes" | of what? the record | "a fact_cid changes if one bit of the record changes." | L |
| 13 | L145 heading | "One address, every product" | "every" (#20, F18) | "One address, fifteen products" | M |
| 14 | L145 sub | "One 10 m cell in central Berlin, read live … from each product's native grid" | cell size (F19); implies co-registration (#20) | "One cell in central Berlin, read on 30 Sep 2026 from each product's own grid (10 m to about 11 km): a common address, not co-registration." | M |
| 15 | L151 | "Each fact carries a provenance class: how far a verifier can check it." | the class is per band, in the manifest, not in the record; it is a declaration (F22, whitepaper §7.2) | "Each band declares a provenance class: how far a receiver can check its facts. It is a declaration, not a measurement." | M |
| 16 | L151 | "Each vector is a model-output fact bound to its encoder checkpoint and recipe … Every vector emem signed still resolves." | false for TESSERA; universal; encoders retired (F05) | "A Clay vector names its checkpoint digest; a TESSERA vector only its product version and year. emem.dev has retired all four encoders; the vectors it signed still resolve." | **H** |
| 17 | L158 | "Six definitions from emem's specification; every panel on this board is an instance of them." | the figure follows docs that the code contradicts; "every panel" (F31) | "Six definitions from emem's code; sections 1 to 4 are instances of them." | M |
| 18 | model.svg | "O = (a, b, t, v, u, p, s) … signature" and "s = Ed25519(BLAKE3(body))" | **a fact carries no signature**; the attester signs a batch root (defect 32, F02) | "O = (a, b, t, v, u, p), with signer and signing time in p; cid(O) = BLAKE3(emem-CBOR(O)); σ = Ed25519 over the batch root of record hashes" | **H** |
| 19 | model.svg | "equal values give equal bytes give equal names; one changed bit is a new cid" | false: signer and signed_at are hashed; 7 cids for one Bengaluru value | "equal records give equal names; re-signing the same value gives a new name; one changed bit is a new cid" | **H** |
| 20 | model.svg | "valid time and transaction time are both inside the signed bytes" | the record is hashed; the batch is signed | "valid time and transaction time are both inside the hashed record, which the batch signature covers" | M |
| 21 | model.svg | "accept: hash ∧ cell ∧ Ed25519(σ) ∧ leaf ∈ log ∧ f(DN) = v ∧ COG[r, c] = DN" | no layers; implies acceptance is complete | label the six terms L0, L1, L0, L0, L2, L3 and add "accept means checked to L3, not true" | M |
| 22 | encoding.svg | "model output: a signed model checkpoint" | checkpoints are not signed; most model_output facts name a product file (F22) | "model output: the producer's file, or a checkpoint digest" | M |
| 23 | encoding.svg | "attested execution (a reading bound inside a verified device trace)" | "verified" without layer; a trace-bound reading is SPEC, no real device enrolled | "attested execution (a reading whose digest is bound in a signed device trace; reference harness only)" | M |
| 24 | eo_berlin.svg | "the cell is the 10 m pixel at the centre" | the cell is a node; the value is the pixel containing it (F19) | "the value is the 10 m pixel holding the cell" | M |
| 25 | L164 | "Asked 'as of 15 Jun', emem still answers 918.0, and both answers verify." | "verify" without layer; 918.0 is a GLO-90 value via Open-Meteo under the 30 m band name | "Asked 'as of 15 Jun', emem returns the May record, 918.0 m (GLO-90 via Open-Meteo); both records re-hash and pass the signature and log checks (L0)." | M |
| 26 | L171 | "All 780 facts … were re-hashed, signature-checked and found in the log on 30 Sep 2026." | correct at L0 but reads as "verified true"; 0 were re-read, and the 780 include wrong-pixel records | "All 780 facts behind sections 1 and 3 pass L0 and L1; 266 were also recomputed (L2); none was re-read (L3), and 14 Keylong records predate the reader fix." | **H** |
| 27 | L176 | "141 Sentinel-2 L2A NDVI facts at one 10 m cell" | plots pre-fix wrong-pixel reads as the cell's NDVI (F01, L3) | "Keylong (India): 141 S2 L2A NDVI facts at one cell; the 14 signed before the reader fix read the row below. Circled: section 4's record." (and draw pre-fix points hollow) | **H** |
| 28 | L181 | "Rondônia (Brazil): 100 point cells 740 m apart … A screen, not a due-diligence statement." | SHARED §21 requires "point samples; not parcel polygons; not a regulatory determination" | "Rondônia (Brazil): 100 point samples 740 m apart, not parcel polygons; 600 facts. Flag: GFC2020 forest, Hansen loss after 2020; TMF agrees on 1 of 3. A screen, not a regulatory determination." | M |
| 29 | eo_rondonia.svg | "cell A: six signed facts an auditor re-runs" | "re-runs" which layer? | "cell A: six signed facts an auditor can re-read (L3)" | L |
| 30 | L194 | "With all nine checks, none of the 16 in-scope cases gets through" | nine representations, six checks (F04); suite-bound (P1 to P3) | "With checks D to I, none of the 16 corruptions in this suite gets through; one offline pass takes 0.4 to 1.2 ms with the source window cached." | **H** |
| 31 | r1_mutation.svg | "emem's checks, one more per column" | columns A to C are not checks; no layers | "representations A to C; checks D to I, one more per column" with the layer under each letter (D L0, E L1, F L0, G L0, H L2, I L3) | M |
| 32 | L197 | "so every check up to recompute passes" | ambiguous; recompute also passes (F29) | "It signed what it read, so every check but the re-read (L3) passes." | M |
| 33 | m15.svg | "the pixel the old reader took, 10 m south" | the drawn record is post-fix; the old reader never read it (F23); production vs simulated | redraw with `kxjvfwpa` (23 Sep, signed 0.3444, containing pixel 0.4860), or label "the pixel the old rule picks (simulated on this record)" | M |
| 34 | L204 | "How a satellite could prove what it ran" | "prove"; satellite as agent (#14) | "Extending checks to execution traces (reference harness)" | **H** |
| 35 | L208 | "its profile demands a signed OS execution trace: eight layers for orbital.satellite.v1, with every payload digest bound inside." | the profile is a candidate (SPEC), harness-only | "emem's candidate orbital.satellite.v1 profile requires a signed OS trace of eight layers, with each payload digest bound inside (reference harness)." | M |
| 36 | L209 | "and so is a fact the trace never emitted" | the gate checks the value digest only; cell and band are not checked (F08, defect 36) | "and so is a value not in the trace." | **H** |
| 37 | L210 | "A trace proves what ran, not that the sensor was right. A drift anchor scores each claim:" | "proves"; a device key signs what the device reports; the score is advisory (F12) | "A signed trace records what the device says it ran, not that the sensor was right. A drift anchor can score a claim:" | M |
| 38 | L220-228 table | "What a verified token guarantees" / "the source bytes · guaranteed · hash, signature, log" / "the observation · bound" / "the upstream file · named" / "the value's accuracy · inherited" / "the entity · out of scope" | "verified" and "guarantees" banned; **row 1 says the source bytes are fixed by hash, signature and log, which is false: they fix the record bytes** (F06); no layers; no decision row | Title "What a checked reference can and cannot tell you". Rows: "the record bytes · CHECKABLE (L0) · hash, signature, log" / "cell, band, time, scene · CHECKABLE (L1) · inside the hashed record, matched to your question" / "the derivation · RECOMPUTABLE (L2) · formula from recorded inputs" / "the upstream file · PARTIAL (L3) · named, no hash bound; open-archive pixels re-readable" / "the entity · OUT OF SCOPE (L4)" / "accuracy and the decision · OUT OF SCOPE (L5) · the product's validation; your rule" | **H** |
| 39 | L234 | "Agreed. It fixes which bytes were served. Truth is tested by re-reading the pixel; accuracy comes from the product's own validation." | a re-read tests fidelity to the file, not truth (F13); the attestation fixes which record bytes were signed, the receipt which were served | "Agreed. It fixes which record bytes were signed. A re-read tests fidelity to the named file (L3); accuracy is the product's own validation (L5)." | **H** |
| 40 | L236 | "emem signs the one value an agent cites and names the scene and file it came from." | no value is signed directly; "file" not always | "A STAC item identifies an asset; an EMEM reference identifies the observation an agent cited, as a signed record that names its source, so the next agent can check it." | **H** |
| 41 | L238 | "emem.dev re-checks any signed trace from its one enrolled Linux host; SAT-042 exercises every refusal." | "any", "every" (F09) | "emem.dev verifies traces; its one enrolled device is a Linux host. SAT-042 shows three of the verifier's 17 refusal reasons." | M |
| 42 | L242 | "Agents hand each other a signed observation, not a sentence about it." | the observation is not signed; the record is | "Agents hand each other a reference to a signed observation record, not a sentence about it." | M |
| 43 | L243 | "One address joins every product, so an EO screen can be re-run fact by fact." | "every", "joins" (F18, #20) | "One address keys 15 products, so an EO screen can be re-run fact by fact." | M |
| 44 | L244 | "Only the full chain refuses all 16; M15 needs the pixel re-read." | leave-one-out shows D is not needed (F03); suite-bound | "Checks E to I refuse all 16 in this suite; only the re-read stops M15, and nothing stops M17." | **H** |
| 45 | L246 | "Re-run every result." | universal; LLM and live results cannot be re-run identically | "RE-RUN THE TEST: data, scripts and claims map, research/repro/v13" | L |
| 46 | L253 | "Mechanisms and formulas read from emem's code and docs/model.md at 04b40c5 … Every number maps to its file and script" | docs contradicted by code (defect 32); universal (F32) | "Mechanisms read from emem's code at 18adb67; where docs differ, the code is printed. Each number maps to its file and script in the claims map." | M |

Counts: 46 rows, 36 on HTML lines and 10 in figure text (rows 18 to 24, 29, 31, 33); 16 rated H. Rows not listed were read and pass the boundary: L110 (meta), L114 (authors), L124, L131, L149, L162,
L174, L179 heading, L188 ("A deterministic verifier … decides whether B acts": a verifier deciding a refusal is
accurate), L195 heading ("the right record, the wrong pixel"), L212, L233 ("A signature does not make a value true":
keep), L237, L252 (references; rename "Sentinel-2 Products Specification" per the review).

---

## 7. Open questions

1. Should L0's attestation (F) and log (G) be printed as separate rungs (L0a, L0b, L0c) or folded? R1 measures them
   separately; the 3 m reader needs six rungs. Proposed: six rungs printed, sub-checks in the 30 cm column.
2. Add P1 to P3 to R1-v13 before printing any R1 denominator? Recommended; otherwise "0 of 16" needs the suite bound
   on every use.
3. Is the S2B 25 Sep scene readable from the committed window set, so P2 can be run as a true re-read that follows the
   scene id? Needs a new committed window (05 §6 has the DNs from Element84).
4. Will emem fill `Source.hash` or reference a `/v1/range_hash` receipt before 19 Oct? If yes, L3 becomes
   "CHECKABLE by hash for sources with a checksum"; the board must then cite the commit.
5. Should the README:246 "independent witnesses … split view is detectable" sentence be fixed in emem before the
   event? A visitor who reads it and then `/v1/log/witnesses` will find the contradiction.
6. The official title contains "Verifiable" and "Foundation-Model Embeddings" while embeddings are retired on
   emem.dev; the board needs one line saying which layers "verifiable" means and that vectors are archival.

---

## 8. Sources

Repository files (this repo, branch claude/tender-planck-clvh1p): `research/SHARED_STATE_EMEM_A0_MASTER.md`;
`research/repro/v11/mutation_suite.py`, `out/summary.md`, `out/mutation_matrix.json`; `research/repro/v8/trace_fact_output.txt`,
`proof_bundle_ndvi.cbor`; `research/repro/data/v8/prevalence_summary.json`, `pixel_check.json`, `results.json`,
`prereg.md`, `pixel_windows.json`; `research/repro/data/v9/rawband/results.md`; `research/repro/data/v11/recompute_state.py`,
`ask_keylong.json`, `verifier_spec.json`, `cell_keylong.json`; `research/repro/data/contra_bengaluru.json`;
`research/repro/v12/data/eo_evidence_per_fact_checks.csv`, `eo_evidence_verification.md`; `research/repro/v12/CLAIMS_MAP.md`,
`scripts/claims_map_v12.py`; `research/repro/v10/algorithms.md`; `research/do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md`;
`poster/src/poster.v12.html`; `poster/build_v12.py`; `poster/fig/v12/*.svg`; `research/v13/00_v11_review_findings.md`,
`02_experiment_design.md`, `04_prior_art_and_field.md`, `05_failure_modes_catastrophe.md`, `08_cost_overhead.md`.

emem at 18adb67: `crates/emem-fact/src/{fact.rs,cid.rs,cbor.rs,attest.rs}`; `crates/emem-attest/src/lib.rs`;
`crates/emem-cache/src/sled_hot.rs`; `crates/emem-storage/src/{lib.rs,server.rs}`; `crates/emem-api-rest/src/{lib.rs,range_hash.rs}`;
`crates/emem-cli/src/bin/emem-realdemo.rs`; `web/verify.html`; `web/emem-verify-core.js`; `docs/whitepaper.md`
(§3.2 l.433, §3.3 l.440, §7.2 l.856, §8.3 l.964, §8.4 l.985, §8.5 l.1005); `docs/model.md:14-27`;
`docs/protocol.md:1455-1463`; `docs/security.md:244-256`; `docs/security/threat-model.md`; `README.md:246`;
`.well-known/agent-notes/AGENT_NOTE_fact_cid_is_not_portable.md`.

Live (2026-10-01): https://emem.dev/v1/log/witnesses, https://emem.dev/v1/verifier_spec,
https://emem.dev/v1/facts/oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa, https://emem.dev/v1/log/sth,
https://emem.dev/.well-known/agent-card.json (01:02:45Z); https://geo.qa/ (about 01:10Z).

External (retrieved 2026-10-01): BLAKE3 specification, https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf
(§ security: "BLAKE3 targets 128-bit security for all of its security goals"); RFC 8032,
https://www.rfc-editor.org/rfc/rfc8032.txt (l.160); RFC 9162, https://www.rfc-editor.org/rfc/rfc9162.txt (gossip
paragraph); ed25519-dalek `VerifyingKey::verify_strict`, https://docs.rs/ed25519-dalek/latest/ed25519_dalek/struct.VerifyingKey.html.

Scratch (this session, not in the repo): `scratchpad/r1run/repro/v11/` (R1 re-run, summary identical to the committed
one; level-I timing 0.359 ms on this host vs 1.187 ms committed); `scratchpad/v13ladder/r1_t2_extra.py` and
`r1_t2_extra_out.json` (P1 to P3); `scratchpad/v13ladder/claim_gate_proto.py`, `.txt`, `.out.json` (36 findings);
`scratchpad/v13ladder/{witnesses.json, vspec.json, fact.cbor, fact.headers, sth.json, card.json, geoqa.html}`.
