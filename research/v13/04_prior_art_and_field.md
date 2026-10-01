# 04 · Prior-art layer map, archive integrity, and the Berlin field map

Topic `prior_art` for the v13 final A0 (issues #15, #22, #30; MASTER §4, §14, §28 Q5). Read-only research: nothing
on the board, in the figures or in emem was changed. Only this file was written.

Retrieval: every URL below was fetched between 2026-09-30T23:30Z and 23:55Z UTC (the brief asks for the retrieval date
to be cited as **2026-10-01**; that is what the poster and QR notes should print). Commands and outputs are summarised
inline; raw downloads sit in the session scratchpad (`…/scratchpad/pa/`), not in the repo.

Labels on every item:

- **LIVE**: fetched from a live service in this session (URL given).
- **SPEC**: what a published specification or paper says (URL, section).
- **MEASURED**: counted or grepped here from a committed file or a fetched document (command given).
- **INFERRED**: my reading or arithmetic, not a measurement.
- **UNVERIFIED**: stated somewhere, not confirmed here.

---

## 0. Findings in one screen

1. **Every adjacent system answers a different question; none identifies "the observation an agent cited".**
   STAC finds and describes files; openEO runs workflows; PROV records lineage; C2PA and the CDSE Traceability
   Service sign files; RAG retrieves context; MCP and A2A carry calls and messages; GeoGuard judges claims.
   EMEM's unit is one observation record (cell, band, valid time, value, source, derivation) that a receiver can
   resolve, re-hash and re-read. SPEC for each (section 2). The unit is new to this room; the mechanism is not (item 5).
2. **The same Sentinel-2 granule comes as three byte streams with three integrity stories** (LIVE, section 3):
   B04 of `S2B … R087 T58MCT 2026-07-15`: CDSE JP2 1,792,843 B with SHA3-256 in STAC; Earth Search COG
   3,790,230 B with SHA2-256 in STAC; Planetary Computer COG 4,711,741 B with **no checksum in STAC** (only an
   unsigned `Content-MD5` HTTP header). A file hash cannot be a cross-archive name for an observation.
3. **EMEM's own Keylong records name their source by URL only.** 207 facts, 213 source entries, 0 with a hash
   (MEASURED, `research/repro/data/v11/cell_keylong.json`); 136 point at Planetary Computer and 66 at the
   Element84 v0 bucket, and both catalogues publish 0 per-asset checksums (LIVE). This is defect 25 made
   concrete, and it is why only the source re-read (level I) caught M15. It is also a cheap upgrade path: Earth
   Search C1 and CDSE publish hashes EMEM could copy into `Source.hash` (issue #7).
4. **GeoGuard is found and read in full**: NASA-IMPACT/geoguard (Apache-2.0), Pantha, Sahoo, Thapa,
   Ramasubramanian (UAH), Ramachandran (NASA MSFC). **No arXiv paper** (arXiv's one "GeoGuard" is an unrelated
   UWB cryptosystem, 2511.14032). It decomposes text into claims, calls authoritative-data tools, and scores a
   verdict: 0/15 fabricated flood events endorsed, 46/50 real events not rejected, GPT-4.1-mini, ~$0.05 and ~35 s
   per event (SPEC, `docs/poster-esa-nasa-workshop-II.md`). Its evidence is an unsigned tool-call trace (MEASURED:
   no hash/signature/provenance terms in `docs/architecture.md`). Complementary, not competing (section 2.7).
5. **The mechanism EMEM uses is established elsewhere and must be credited**: signed statements about a digest
   plus an append-only log (Sigstore/in-toto/SLSA, RFC 6962/9162, SCITT RFC 9943 and COSE Receipts RFC 9942,
   both June 2026); hash-named signed assertions (trusty URIs, nanopublications, 2014/2016); timestamped,
   hash-verified data citation (RDA WGDC R6/R9, 2016); content-addressed agent observation stores (ARC,
   arXiv 2607.25066, July 2026). EMEM's defensible delta is the combination: a physical-world observation as the
   unit, carried **between** agents and organisations, checked by the receiver, with a source re-read path. SPEC.
6. **MCP 2026-07-28 has no result integrity, and moved state into model-carried handles.** "Servers that need
   cross-call state use explicit, server-minted handles passed as ordinary tool arguments (SEP-2567)"; "a handle is
   a name, not a capability". Six community proposals to sign MCP results or tool definitions were found; all
   are closed and none is in the current spec (LIVE, section 2.12). An EMEM token is exactly such a handle, one the
   receiver can verify.
7. **A2A 1.0 signs the Agent Card (JWS, RFC 7515, JCS RFC 8785), not the Artifacts agents exchange** (SPEC).
   EMEM's own card is signed (EdDSA, `kid 777er3yi…`, LIVE).
8. **The room**: 43 posters. Among all 43 poster titles plus every oral, demo and track title, the words
   "memory" and "content-addressed" occur only in EMEM's title (MEASURED, section 4.1). Vocabulary that is
   already taken: validation/guardrails (GeoGuard), trustworthy (CARE/NASA), provenance-first (Earthward),
   traceable, reproducible, verified pipelines, pixel-grounded, artifact-grounded, auditable, evidence-conflict.
9. **The organisers' own framing fits EMEM's slot.** Munir, Sheikh, Shabbir, M. H. Khan, F. Khan, X. X. Zhu,
   **B. Demir** (BIFOLD, workshop organiser) and **S. Khan** (Day-1 keynote), arXiv 2604.24919 (2026): in EO agent
   pipelines "errors may propagate silently across steps"; memory components "track short-term reasoning traces
   rather than … the validity of intermediate geospatial states"; they propose a verifier over "a shared
   structured EO state representation" with provenance as part of the state (SPEC). EMEM is a concrete, checkable
   form of that state for the handoff step. Cite it on the board.
10. **The three older citations are real** (SPEC via arXiv API): Perez et al. ICLR 2025 = arXiv 2407.04503;
    arXiv 2608.11242 = *Lost in Compaction* (Wang, Zhang, Lee, Yang, 2026); arXiv 2607.25066 = *ARC: Addressable
    Recall Compaction* (Dang, Ichikawa, Fatima, Shirahata, 2026). ARC is the closest conceptual competitor and
    must be named, not just cited (section 6).

---

## 1. The layer map (issue #30 figure; MASTER §14)

### 1.1 What the figure must say in under 15 seconds

> Each layer answers a different question. EMEM answers one more: **is this the observation the sender cited?**

### 1.2 Figure specification (for the designer; every label is sourced in section 2)

A single vertical evidence path from sensor to decision, drawn as seven thin horizontal lanes. Each lane has one
verb, the system name(s), and the unit it identifies. EMEM is **not** a lane: it is a thin vertical thread that
touches four lanes, labelled with its three verbs. No ticks or crosses against other systems (issue #30:
"no competitor is caricatured").

```
 lane (verb)        systems                         unit it identifies            question it answers
 ───────────────────────────────────────────────────────────────────────────────────────────────────────
 JUDGE              GeoGuard                        a claim in text               Is the claim supported by outside data?
 CARRY              MCP · A2A                       a tool call · an agent card   How does an agent call / find another?
 RETRIEVE           RAG                             a text chunk                  Which context is relevant?
 SIGN FILES         C2PA · CDSE Traceability        a file (asset, product zip)   Is this file the one its maker signed?
 RECORD LINEAGE     W3C PROV                        entity–activity–agent graph   How was this made, by whom?
 RUN                openEO                          a process graph / job         Compute this on that data.
 FIND               STAC                            an asset (file) + metadata    What data exists, where, how to get it?
 ───────────────────────────────────────────────────────────────────────────────────────────────────────
                    sensor → archive
                                                    ║  EMEM thread (one colour, the board's EMEM colour):
                                                    ║  CITE  → touches FIND (names the STAC asset / CDSE product)
                                                    ║          and RUN (names the recipe: fn_key + args)
                                                    ║  HAND OFF → rides CARRY (token inside an MCP result / A2A part)
                                                    ║  RESOLVE · RE-HASH · RE-READ → supplies JUDGE with evidence
                                                    ║  a third party can check later
```

Caption (finding + scope, issue #36): **"Adjacent systems find files, run workflows, record lineage, sign files,
retrieve context, carry calls and judge claims. EMEM names the one observation an agent cited and lets the next
agent re-check it; it relies on those layers and replaces none."** (40 words)

Footnote line at 30 cm: "Same pattern, other domains: Sigstore/in-toto (software), Certificate Transparency
(RFC 6962/9162), SCITT (RFC 9943). Closest agent-memory work: ARC (arXiv 2607.25066)."

### 1.3 The compact matrix (30 cm, or QR-linked)

| system (version checked) | question it answers | unit it identifies | integrity in the spec | where EMEM sits (complementary) |
|---|---|---|---|---|
| STAC 1.1.0 / STAC API 1.0.0 | What data exists, where? | asset (file) in an Item | `file:checksum` (optional extension, per file); Item JSON unsigned | record names the STAC asset; can copy `file:checksum` into `Source.hash` |
| openEO API 1.3.0 | Compute this on that data | process graph, UDP, batch job | none on results; "signed URLs" are access control | derivation recipe; a process graph can be the recipe EMEM names |
| W3C PROV-O/DM (Rec. 2013) | How was this made? | entity, activity, agent | none (0 hits for "signature"/"integrity" in PROV-DM) | EMEM's derivation fields map to PROV terms |
| C2PA 2.4 (Apr 2026) | Who made/edited this file? | media asset + manifest | hard binding (hash) + COSE claim signature, X.509 trust list | a rendered EMEM map could carry a manifest with the fact CID (planned, not built) |
| CDSE Traceability | Is this product the one ESA published? | product zip | BLAKE3 + RSA-SHA256 signed trace, X.509 | upstream identity EMEM can name for CDSE-read facts (not done today) |
| RAG (Lewis et al. 2020) | Which context is relevant? | text chunk | none by default | retrieval can return EMEM tokens instead of paraphrases |
| MCP 2026-07-28 | How does an agent call a tool? | tool call; handle strings | none on results | EMEM is an MCP server; its token is a verifiable handle |
| A2A 1.0 | Who is this agent? | Agent Card; task Artifact | JWS on the Agent Card (optional); Artifacts unsigned | EMEM tokens travel inside Artifact parts |
| GeoGuard (2026) | Is this claim supported? | atomic claim in text | none on evidence (unsigned tool trace) | GeoGuard tools could return EMEM facts, making the verdict's evidence re-checkable |
| Sigstore / in-toto / SLSA 1.2 | Who built/signed this artifact? | software artifact digest | signed statement over digest + Rekor log | same pattern, applied by EMEM to observations |
| CT RFC 6962/9162; SCITT RFC 9943 + COSE Receipts RFC 9942 | Was this logged, append-only? | log entry / signed statement | Merkle log, inclusion/consistency proofs, receipts | EMEM log is RFC 6962-style but BLAKE3; SCITT receipts proposed, not built |
| IPFS CID / multiformats | Which bytes? | bytes | self-describing multihash | EMEM exposes `cid_v1` (BLAKE3 multihash 0x1e) |
| FAIR, DOI, RDA WGDC | How do I cite data reproducibly? | dataset; query subset | DOI names; R6 result-set hash; R9 timestamped query store | EMEM applies subset citation to one observation, verified by signature |
| ARC (arXiv 2607.25066) | Can an agent recover what it saw? | tool observation, one agent's task | SHA1 id, append-only store, no signature | EMEM crosses agents and organisations; signed; physical referent; re-read |

---

## 2. Per-system entries

Each entry: the one question · what it identifies/signs · where EMEM sits · what EMEM can take from it · source.

### 2.1 STAC (SpatioTemporal Asset Catalog) and STAC API

- **Question.** What spatiotemporal data exists, and where are its files? SPEC: an Item is "an atomic collection
  of inseparable data and metadata", a GeoJSON Feature with asset links (https://stacspec.org/en/about/stac-spec/).
- **Versions.** STAC 1.1.0 (2024-09-10), STAC API 1.0.0 (2023-04-24). SPEC (CHANGELOGs at
  https://github.com/radiantearth/stac-spec and https://github.com/radiantearth/stac-api-spec).
- **Integrity.** The core Item spec defines none: `item-spec/item-spec.md` has 0 matches for
  sign|integrity|checksum|hash (MEASURED, `curl raw…/item-spec/item-spec.md | grep -i`). The **File extension**
  (v2.1.0) adds `file:checksum`: "self-identifying hashes as described in the Multihash specification … hexadecimal"
  (SPEC, https://github.com/stac-extensions/file, README line 32). It is per asset (a whole file), optional, and
  sits inside an unsigned JSON document; its trust is the trust in the HTTPS channel that served the Item (INFERRED).
- **What it identifies.** A file. Not a pixel, not a value, not a query.
- **Where EMEM sits.** Below EMEM: EMEM reads a STAC-described asset and its record names that asset. EMEM does
  not discover or catalogue.
- **Take from it.** Copy `file:checksum` into the fact's `Source.hash` when the catalogue publishes one (today
  `hash: None` in production, defect 25). That turns the source edge from "location-only" into "file identity
  checked" for Earth Search C1 and CDSE reads (section 3). Also: the STAC Processing extension's
  `processing:expression` can hold an openEO process (SPEC, https://github.com/stac-extensions/processing, line 29,
  135), a natural home for EMEM's `fn_key`.
- **Critical answer (MASTER §14, refined).** *A STAC item identifies a file; EMEM identifies the observation an
  agent cited, and names the file it came from.*

### 2.2 openEO

- **Question.** Run this computation on that EO data, on any compliant back-end.
- **Version.** openEO API 1.3.0, 2026-02-02 (SPEC, https://github.com/Open-EO/openeo-api CHANGELOG). 1.3.0 added
  an `OpenEO-Identifier` response header for synchronous requests and batch-job timestamps; nothing on result
  integrity.
- **What it identifies.** Processes, process graphs, user-defined processes (UDPs: "a process graph with a variety
  of additional metadata", openapi.yaml line 244), batch jobs. Results are returned as a STAC Item or Collection
  (openapi.yaml ~3233).
- **Integrity.** None on results. The spec's "signed URLs" are an access-control device: "URL signing is a way to
  protect files from unauthorized access with a key in the URL" (SPEC, openapi.yaml, `list-results`). Do not let a
  reviewer conflate this with signed results.
- **Provenance work.** Omidi et al., *Towards Provenance-Aware Earth Observation Workflows: the openEO Case
  Study*, arXiv 2506.08597 (2025): yProv4WFs integrated into openEO to record lineage (SPEC, abstract).
- **Where EMEM sits.** Beside/after it: openEO computes; EMEM records one cited output with its recipe so another
  agent can recompute it. EMEM does not execute workflows.
- **In the room.** Demo 13 (VITO) "Agent-Based Composition of **Reproducible** openEO Workflows on CDSE"; Demo 15
  (EURAC) "Portable Agentic openEO" (LIVE programme). These people will ask "why not just store the process graph?"
  Answer in section 7.

### 2.3 W3C PROV (PROV-O, PROV-DM)

- **Question.** How did this come to be, and who is responsible? PROV-DM: "An entity is a physical, digital,
  conceptual, or other kind of thing with some fixed aspects"; "A derivation is a transformation of an entity into
  another" (SPEC, https://www.w3.org/TR/prov-dm/, W3C Recommendation 30 April 2013; PROV-O
  https://www.w3.org/TR/prov-o/).
- **Integrity.** None: 0 occurrences of "signature" and "integrity" in the PROV-DM text (MEASURED). PROV describes
  lineage; it does not let a receiver test that the bytes in hand are the ones described.
- **Where EMEM sits.** EMEM's record is a small lineage statement (`sources[]`, `derivation.fn_key`, `args`,
  `signed_at`, signer) plus a content address and a signature. Mapping (INFERRED): fact → `prov:Entity`;
  `fn_key` → `prov:Activity`; `sources[]` → `prov:used`; signer → `prov:Agent`; `wasDerivedFrom` to the source.
  A PROV-JSON export is cheap and would let yProv/openEO lineage tools read EMEM facts. Not built.

### 2.4 C2PA / Content Credentials

- **Question.** Who created or edited this media file, and has it been altered since?
- **Version.** C2PA Technical Specification 2.4 (version history: "2.4 - April 2026"; 2.3 and 2.2 also listed)
  (SPEC, https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html).
- **Mechanism.** Assertions + claim + claim signature bound into a **C2PA Manifest**; a **hard binding** is "one
  or more cryptographic hashes that uniquely identifies either the entire asset or a portion thereof" (§2.3.12);
  a soft binding is a fingerprint or watermark (§2.3.13); trust rests on "the identity of the signer" and the C2PA
  Trust List (§1.3.1, §2.3.15). 2.4 added JSON-LD `crJSON`, a Repository Receipt assertion, and embedding in HTML
  and structured text (§5.3.1).
- **Its own truth boundary (useful to quote).** "C2PA specifications SHOULD NOT provide value judgments about
  whether a given set of provenance data is 'good' or 'bad,' merely whether the assertions included within can be
  validated as associated with the underlying asset, correctly formed, and free from tampering." And: "the signer
  is not responsible for the accuracy of a GPS location appearing in EXIF metadata, even if that metadata is
  covered by the hard binding." (SPEC, §1.2 guiding principles; assertions section). This is the same line EMEM
  draws: a signature fixes bytes, not the measurement.
- **Independent critique.** Golaszewski et al., *Verifying Provenance of Digital Media: Why the C2PA Specifications
  Fall Short*, arXiv 2604.24890 (2026): formal-methods analysis; "the current C2PA specifications fail to achieve
  their claimed security goals" (SPEC, abstract). The older related-work note's claim that credentials "get
  stripped in pipelines" citing this paper is **UNVERIFIED** from the abstract.
- **Where EMEM sits.** C2PA's unit is a file; EMEM's is one observation record and its as-of state. They compose:
  emem's own roadmap proposes a C2PA 2.2 manifest on rendered scene PNGs with the `fact_cid` as an assertion
  (SPEC, emem `docs/federation.md` §9c item 8, "Later"). Not built; do not print as a feature.

### 2.5 Ordinary RAG

- **Question.** Which context should the model see for this query? Lewis et al., *Retrieval-Augmented Generation for
  Knowledge-Intensive NLP Tasks*, NeurIPS 2020, arXiv 2005.11401 (SPEC). Note their own motivation: "providing
  provenance for their decisions and updating their world knowledge remain open research problems".
- **Integrity.** None by default: a retrieved chunk arrives as text. PoisonedRAG (Zou et al., USENIX Security 2025,
  arXiv 2402.07867) and AgentPoison (Chen et al., arXiv 2407.12784) show that corrupting the knowledge base or
  memory steers agents (SPEC, abstracts).
- **Where EMEM sits.** Above RAG or inside it: a retriever can return EMEM tokens (short, resolvable) instead of
  paraphrased values; the receiver then resolves and checks. R1 has no RAG arm (report 01 finding 5); the RAG
  condition is in the R5 design (report 02 §6). Until R5 runs, the poster must not claim a measured RAG result.
- **In the room.** SENSOR2RAG (Session 1, Landbanking Group); Airbus Geo Explore semantic-search APIs (Session 2).

### 2.6 Earth Search, Planetary Computer, CDSE: what integrity metadata the archives actually publish

LIVE on 2026-10-01; full numbers in section 3.

| archive / collection | per-asset hash in STAC | algorithm (multihash code) | product-level | signed? |
|---|---|---|---|---|
| Earth Search `sentinel-2-c1-l2a` | 23 of 23 assets | SHA2-256 (0x12) | – | no (hash inside unsigned JSON) |
| Earth Search `sentinel-2-l2a` (v0 COGs, bucket `sentinel-cogs`) | 0 of 38 assets | – | – | no |
| Planetary Computer `sentinel-2-l2a` | 0 of 23 assets (File extension not declared) | – (blob HTTP `Content-MD5` only) | – | no |
| CDSE STAC `sentinel-2-l2a` | every band asset | SHA3-256 (0x16) | product zip: MD5 (0xd5) | no (in STAC) |
| CDSE OData `Products` | – | – | MD5 and **BLAKE3** per product | no (in OData) |
| CDSE Traceability Service | – | – | **BLAKE3** per product zip | **yes**: RSA-SHA256 over the trace, X.509 cert from the CDSE CA |

Multihash codes confirmed against the multicodec table: sha2-256 0x12, sha3-256 0x16, blake3 0x1e (draft), md5
0xd5 (draft) (SPEC, https://github.com/multiformats/multicodec/blob/master/table.csv).

CDSE Traceability (SPEC, https://documentation.dataspace.copernicus.eu/APIs/Traceability.html): "Digital
signatures on the traces provide users with the ability to verify the authenticity and integrity of the traces
themselves". LIVE trace for `S2B_MSIL2A_20260715T233819_N0512_R087_T58MCT_20260716T005600.SAFE.zip`
(`https://trace.dataspace.copernicus.eu/api/v1/traces/name/<name>`): `hash_algorithm: BLAKE3`,
`product.hash: ac2cd079…1f3f`, `size: 22255506`, `event: COPY`, `signature.algorithm: RSA-SHA256`,
`origin: cdse_csc@dataspace.copernicus.eu`, `timestamp: 2026-07-16T01:11:53Z`; both listed inputs (tile and
datastrip) carry an **empty** hash.

**Where EMEM sits.** CDSE signs the product; EMEM signs the observation an agent cited and can name the CDSE trace
it came from. This is the strongest "complementary" story available in the room: ESA's own data space already signs
at file level with BLAKE3; EMEM continues the chain to the pixel an agent read. Today EMEM does not record the trace
(defect 25). INFERRED + LIVE.

### 2.7 GeoGuard

- **Identity.** "GeoGuard — An Agentic Guardrails & Validation Framework for Geospatial AI". Nishan Pantha, Rohit
  Sahoo, Sanjog Thapa, Muthukumaran Ramasubramanian (The University of Alabama in Huntsville), Rahul Ramachandran
  (NASA Marshall Space Flight Center). Supported by NASA Grant 80MSFC22M004. Code:
  https://github.com/NASA-IMPACT/geoguard (Apache-2.0; `pyproject.toml` `license = "Apache-2.0"`). Poster text:
  `docs/poster-esa-nasa-workshop-II.md` (SPEC, fetched from `raw.githubusercontent.com/NASA-IMPACT/geoguard/main/`).
  Workshop listing: Session 1, presenter "Rohit Sisir Sahoo, The University of Alabama in Huntsville" (LIVE).
- **Venue / arXiv.** None found. arXiv title search `ti:GeoGuard` returns one paper, 2511.14032 "GeoGuard: UWB
  Timing-Encoded Key Reconstruction…" (Mukherjee), unrelated (LIVE, arXiv API). NASA NTRS search "GeoGuard": 0
  results (LIVE). The same group's CARE methodology is on arXiv (2604.28043, Ramachandran, Jha,
  Ramasubramanian; NASA/TM-20260000926).
- **What it validates.** "wraps any upstream system that emits geographically-grounded text … and audits its factual
  claims against authoritative external data sources. It does not modify the upstream model. It decomposes the
  output into atomic claims, picks tools per claim, runs verification with those tools, scores the result with a
  holistic rubric, and emits a structured report with verdicts, evidence, and a confidence score" (README).
  Pipeline: claim extraction (LLM) → per-claim tool selection (LLM) → per-claim verification agent loop → rubric
  (LLM) → report; verdict roll-up "any CONTRADICTS → CONTRADICTS · all SUPPORTS → SUPPORTS · else INCONCLUSIVE".
  Tools: Nominatim geocoding, Open-Meteo (ERA5), NOAA PRISM/MRMS, USGS NWIS, OSM Overpass, NASA VEDA STAC, MODIS/
  VIIRS flood product.
- **Benchmark (SPEC, poster doc §06).** 65 flood events from NOAA Storm Events 2024: 50 verified (41 SUPPORTS,
  4 CONTRADICTS, 5 INCONCLUSIVE) and 15 fabricated by perturbing real events ("wrong date · wrong location ·
  inflated magnitude"): 0 SUPPORTS, 14 CONTRADICTS, 1 INCONCLUSIVE. Headline: "0% of fabricated events endorsed",
  "92% of verified events not rejected". GPT-4.1-mini, ~$0.05 per event, ~35 s per event. Stated limits: "flood /
  storm only · limited tool set · US-only for radar/gauge & streamflow · text claims only". Its own gap table marks
  "Temporal consistency" and "Cross-reference" as future.
- **Integrity of its evidence.** `docs/architecture.md` contains no "hash", "provenance", "sign" (other than
  function signatures), "cache" or "persist" (MEASURED, grep). The report keeps "full tool-call trace (name, args,
  returned data)" (README). So the evidence behind a verdict is an unsigned trace; re-running the tools later may
  return different values if the upstream archive is revised (INFERRED).
- **A shared failure class, stated fairly.** GeoGuard's flood tool, when the requested day is missing, tries "±2 day
  window" offsets (0, +1, −1, +2, −2) and records the offset in its source string, e.g. "LANCE NRT (offset +1d)"
  (MEASURED, `geoguard/tools/satellite.py`, `_download_tile`). EMEM's own `band_raster` substituted 25 Sep for a
  23 Sep request with **no** warning (defect 27; 9 of 10 agents never saw 23 Sep). Date substitution is a generic
  class; GeoGuard labels it in prose, EMEM's fix is to bind `tslot` into the signed record so a receiver can check
  it mechanically. Do not present this as a GeoGuard bug: it is disclosed behaviour.
- **Where EMEM sits.** GeoGuard asks "is this claim true against outside data?" (semantic, the layer EMEM declares
  out of scope). EMEM asks "is the evidence I received exactly what the sender observed?" (identity and integrity).
  If GeoGuard's tools returned EMEM facts, its verdicts would cite evidence a third party could re-check later;
  if an EMEM-citing agent's claim were run through GeoGuard, the claim would be checked against independent data.
  Order in the room: GeoGuard is the last poster of Session 1, EMEM the fourth (LIVE). Worth visiting before 17:00.
- **Room line (10 words).** *GeoGuard judges the claim. EMEM fixes the evidence it cites.*

### 2.8 Sigstore, in-toto, SLSA (supply-chain attestations)

- **Sigstore.** Fulcio issues short-lived certificates bound to an OIDC identity; Rekor is "an immutable,
  append-only ledger" of signing events including artifact digests (SPEC, https://docs.sigstore.dev/about/overview/).
- **in-toto Attestation Framework, Statement v1.** `{"_type": "https://in-toto.io/Statement/v1", "subject":
  [{"name", "digest": {alg: hex}}], "predicateType", "predicate"}`; "Subjects are assumed to be immutable"
  (SPEC, https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md).
- **SLSA.** Current specification v1.2 (SPEC, https://slsa.dev/spec/).
- **Where EMEM sits.** Same pattern (signed statement about a digest-identified subject, logged), different subject:
  a software artifact there, a physical observation here. emem's plans mention an in-toto export of device traces
  (SPEC, `docs/plans/encoder-substrates.md:179-184`); not built. Credit the pattern on the board ("pattern from
  software supply chains"), claim the application.

### 2.9 Transparency logs: RFC 6962, RFC 9162, SCITT (RFC 9943) and COSE Receipts (RFC 9942)

- RFC 6962 *Certificate Transparency*, Experimental, June 2013; RFC 9162 *Certificate Transparency Version 2.0*,
  Experimental, December 2021, **obsoletes 6962** (SPEC, rfc-editor.org headers).
- **RFC 9943** *An Architecture for Trustworthy and Transparent Digital Supply Chains* (SCITT), **Standards Track,
  June 2026**, Birkholz, Delignat-Lavaud, Fournet, Deshpande, Lasker; **RFC 9942** *COSE Receipts*, Standards
  Track, June 2026 (SPEC, https://www.rfc-editor.org/rfc/rfc9943, /rfc9942; datatracker state "RFC Published").
- **EMEM against them (SPEC, emem `docs/federation.md` §9c items 1–2).** emem's log is an RFC 6962-style Merkle
  log hashed with **BLAKE3**, so an off-the-shelf C2SP/RFC 6962 witness "could co-sign our signature and could not
  check our proof"; a SHA-256 shadow tree and a SCITT/COSE receipt adapter are proposed, not built. emem's own
  words: "RFC 9943 (June 2026) is the model emem grew into without the envelope".
- **Poster consequence.** Reference as "Merkle log in the style of RFC 6962/9162 (BLAKE3)". Do not write "RFC 6962
  log" unqualified, and do not imply SCITT conformance. The v11 reference list printed "RFC 6962" and "RFC 8949
  CBOR"; defect 33 says emem-CBOR is not RFC 8949 §4.2.1 deterministic encoding, so "RFC 8949" must not read as a
  conformance claim either.

### 2.10 IPFS / CIDs / multiformats

- CIDv1 = `<multibase><0x01><content-type multicodec><multihash>`; "A CID is a self-describing content-addressed
  identifier" (SPEC, https://github.com/multiformats/cid README lines 42–76).
- emem computes `cid_v1` as `0x01 0x55 0x1e 0x20 ‖ digest`, base32-lower with `b` prefix, "no rehashing"
  (SPEC, emem `crates/emem-api-rest/src/lib.rs:8225-8238` at 18adb67). The public `GET /v1/facts/<cid>` body does not
  include it (LIVE, fact `2dpnuf4e…`, fields: kind, cell, band, tslot, value, confidence, sources, derivation,
  privacy_class, schema_cid, signer, signed_at).
- **Where EMEM sits.** Same addressing format; the difference is the object addressed (a canonical observation
  record with cell/band/time/value/source), not the hashing. "Same content, same address" is not a contribution.

### 2.11 FAIR, DOI, data citation, and earlier hash-named assertions

- **FAIR.** Wilkinson et al., *The FAIR Guiding Principles for scientific data management and stewardship*,
  Scientific Data 3, 2016, doi:10.1038/sdata.2016.18 (SPEC, Crossref). A DOI names a dataset (landing page); it does
  not fix bytes.
- **RDA WGDC** (Rauber, Asmi, van Uytvanck, Pröll), *Data Citation of Evolving Data*, 2016,
  doi:10.15497/RDA00016: 14 recommendations built on timestamped, versioned data and PIDs assigned to queries;
  R6 "Result Set Verification" (compute a fixity hash of the result set), R9 store the query with timestamp and
  checksums (SPEC via search summary of RDA documents; the full text was not fetched: **UNVERIFIED** wording).
  This is prior art for EMEM's as-of recall. EMEM's addition: the unit is one observation and the reader checks a
  signature and log offline instead of querying the data centre's store (INFERRED).
- **Trusty URIs.** Kuhn & Dumontier, *Trusty URIs: Verifiable, Immutable, and Permanent Digital Artifacts for
  Linked Data*, ESWC 2014, LNCS, doi:10.1007/978-3-319-07443-6_27; **nanopublications**: Kuhn et al., *Decentralized
  provenance-aware publishing with nanopublications*, PeerJ CS 2016, doi:10.7717/peerj-cs.78 (SPEC, Crossref).
  Hash-in-identifier signed assertions with provenance, a decade old. Not EO, not agent handoff. Cite at 30 cm.
- **W3C Verifiable Credentials Data Model v2.0**, W3C Recommendation 15 May 2025 (SPEC). Signs claims about a
  subject; emem publishes `did:web:emem.dev` keys so VC/DID verifiers can resolve them (SPEC, `docs/federation.md`
  §9c item 3, "Shipped 2026-09-02"; not re-checked live: UNVERIFIED).

### 2.12 MCP (Model Context Protocol)

- **Current version: 2026-07-28** ("The current protocol version is 2026-07-28") (LIVE,
  https://modelcontextprotocol.io/specification/versioning; `/specification/latest` redirects there).
- **State now lives in model-carried handles (SPEC, changelog and server/tools pages).** "Remove protocol-level
  sessions … Servers that need cross-call state use explicit, server-minted handles passed as ordinary tool arguments
  (SEP-2567)." "The protocol has no concept of a state handle; from the wire's perspective a handle is an ordinary
  string in a tool result and an ordinary argument to subsequent tool calls." "The model is responsible for carrying
  basket_id forward." Security page: "a handle is a name, not a capability." Also: `clientInfo`/`serverInfo` "are
  self-reported … and are not verified by the protocol"; "clients MUST consider tool annotations to be untrusted".
- **Result integrity.** None. Counts of "integrity", "hash", "provenance", "tamper" on the changelog, basic,
  server/tools and security-best-practices pages: 0 each (MEASURED).
- **Open proposals (LIVE, GitHub via WebFetch summaries; all show "Closed"):** SEP-1766 digest-pinned tool
  versioning (opened 2025-11-05); SEP-2787 tool call attestation, JWS over intent/identity/args (opened 2026-05-25,
  closed 2026-09-22); Discussion #2964 "Should MCP tool responses carry verification metadata?" (2026-06-22, closed
  2026-09-25 when Discussions were limited to meeting notes); SEP-3140 signed capability declarations (opened
  2026-07-27, closed 2026-09-22); #3350 Tool Outcome Attestation (2026-09-06); #3354 "verifiable tool results"
  with ZK proofs / TEE attestations (2026-09-10). Why each was closed was not established (UNVERIFIED).
- **Where EMEM sits.** On top of MCP: emem is an MCP server (Streamable HTTP at `https://emem.dev/mcp`; official
  registry `io.github.Vortx-AI/emem`, SPEC `docs/federation.md` §9d, not re-checked here). The emem token is the
  handle the 2026-07-28 spec now asks models to carry, with the property the spec does not give: a receiver can
  resolve and check it without trusting the sender. **Poster line:** "MCP moves the call. The token is the evidence."
- **Research-community signal (INFERRED).** Six proposals in ten months show the gap is felt; none is in the spec.
  EMEM should say "application layer on MCP", never "MCP extension".

### 2.13 A2A (Agent2Agent)

- **Version.** The spec at https://a2a-protocol.org/latest/specification/ is v1.0 ("What's New in v1.0"),
  © 2026 The Linux Foundation, Apache-2.0 (LIVE).
- **Signed Agent Cards.** "Agent Cards MAY be digitally signed using JSON Web Signature (JWS) as defined in RFC
  7515 to ensure authenticity and integrity"; content "MUST be canonicalized using the JSON Canonicalization Scheme
  (JCS) as defined in RFC 8785" (SPEC, §8.4, §8.4.1; `AgentCardSignature` §4.4.7).
- **Artifacts.** `artifactId` ("Unique identifier (e.g. UUID) … unique within a task"), `parts`, `metadata`,
  `extensions`; no content address or signature (SPEC, §4.1.7). "provenance": 0 occurrences in the spec (MEASURED).
- **EMEM live.** `https://emem.dev/.well-known/agent-card.json`: `protocolVersion "1.0"`, `version "2.4.2"`, one
  signature with protected header `{"alg":"EdDSA","jku":"https://emem.dev/.well-known/jwks.json","kid":
  "777er3yihgifqmv5hmc2wwmyszgddzderzhsx6rex4yoakwomvka","typ":"JOSE"}` (LIVE). Signature not verified here.
- **Where EMEM sits.** A2A signs who the agent is; EMEM signs what the agents exchange. An EMEM token rides inside an
  A2A Part. Complementary.

### 2.14 Agent memory, compaction, and multi-agent drift (the phenomenon side)

- **ARC**, *Addressable Recall Compaction for Long Context-Window Control in AI Agents*, Dang, Ichikawa, Fatima,
  Shirahata, arXiv 2607.25066 (2026-07-27). "ARC stores tool observations in an append-only, ID-addressable log and
  replaces older observations with compact citations"; ids are "SHA1 over the action signature, an ASCII
  unit-separator byte, and the observation", first 8 hex characters visible; "content-addressed store"; evaluated on
  Qwen3-8B/32B (SPEC, arXiv HTML). "multi-agent": 0 occurrences; no signatures (MEASURED). **Closest conceptual
  competitor**: content-addressed citations for agent observations already exist. EMEM's delta: across agents and
  organisations, signed and logged, physical referent (cell/band/time/source), receiver re-read.
- Mem0, MemGPT/Letta, A-MEM, CoALA (listed in `research/should_do/08_RELATED_WORK_2025_2026.md`): per-agent,
  rewritable memory; EMEM has not been benchmarked against them (that file says so; keep saying so).

### 2.15 EO agent systems and benchmarks

All SPEC from arXiv abstracts (API, 2026-10-01). None of these abstracts measures whether evidence survives a handoff
between agents or whether a receiver can check it (INFERRED from abstracts only; full texts not read).

| work | arXiv / venue | what it evaluates or builds |
|---|---|---|
| ThinkGeo (Shabbir … F. S. Khan, **S. Khan**) | 2505.23752 | 486 agentic RS tasks, 1,778 expert-verified steps; ReAct; step-wise and final metrics |
| Earth-Agent / Earth-Bench (Feng et al.) | 2509.23141, ICLR 2026 | MCP-based tool ecosystem; 248 tasks, 13,729 images; trajectory + outcome evaluation |
| OpenEarthAgent (Shabbir … X. X. Zhu, **S. Khan**) | 2602.17665, ECCV 2026 | unified executable tool registry, trained on reasoning traces |
| EO-Gym (Ma et al.) | 2605.01250 | Gymnasium-style workspace, 660k files, 35 tools, 9,078 trajectories |
| TerraBench / TerraAgent (Nguyen et al.) | 2606.13148 | ReAct over heterogeneous Earth-system data |
| Towards LLM Agents for EO / UnivEARTH (Kao et al.) | 2504.12110, ICML 2025 TerraBytes WS | 140 yes/no questions; GEE agents 33% accuracy, code fails >58% |
| GeoLLM-Engine (Singh, Fore, Stamoulis) | 2404.15500, EarthVision 2024 | copilot environment with geospatial APIs |
| Evaluating Tool-Augmented Agents in RS Platforms (GeoLLM-QA) | 2405.00709 | (title verified only) |
| GeoBenchX (Krechetova, Kochedykov) | 2503.18129 | 8 LLMs, 23 geospatial functions, includes unsolvable tasks |
| GeoAgent (Chen, Wang, Lobry, Kurtz) | 2410.18792 | code interpreter + static analysis + RAG + MCTS |
| Agentic AI for RS: challenges (Munir … Zhu, **Demir**, **S. Khan**) | 2604.24919 (position) | failure modes; structured geospatial state; verifier-guided execution |
| "GEO-Bench-Agent" | not found | arXiv has GEO-Bench (2306.03831) and GEO-Bench-2 (2511.15658), both foundation-model benchmarks, and unrelated "GEO-Bench" (generative engine optimisation). Treat "GEO-Bench-Agent" as **non-existent** unless someone supplies a link. |

**The position paper matters most** (SPEC, arXiv 2604.24919v3 HTML): generic traces reach "a plausible-looking but
invalid result" through "temporal-window mismatch, incorrect transformation order, coordinate reference system (CRS)
mismatch, and unit-conversion error"; "Multi-step geospatial pipelines accumulate errors … often without explicit
detection mechanisms"; the proposed verifier score includes "provenance consistency"; "Without such domain-grounded
verification loops, multi-agent models may reinforce internally coherent yet scientifically invalid reasoning
chains." Three of their four named failure modes are R1 mutation classes: temporal-window mismatch = M5/M10 (date),
CRS/spatial mismatch = M4/M9 (cell), unit conversion = M14 class (units), and EMEM adds the one they do not name:
M15, the right record with the wrong pixel (INFERRED mapping).

---

## 3. Figure candidate: "Same granule, three archives, three files" (LIVE; issue #31, #12)

A true, specific, visually strong figure that answers "why not just hash the file?" and fixes the CID/source wording
(MASTER §5) at the same time.

Same scene, same band: Sentinel-2B, relative orbit 87, MGRS tile 58MCT, sensing 2026-07-15T23:38Z, processing baseline
05.12, band B04 (10 m).

| archive | item id | file | size (bytes) | hash published in STAC | extra |
|---|---|---|---|---|---|
| CDSE | `S2B_MSIL2A_20260715T233819_N0512_R087_T58MCT_20260716T005600` | `…_B04_10m.jp2` (JPEG 2000) | 1,792,843 | SHA3-256 `1620b8c23a41012a…34f67b` | product zip: MD5 in STAC; BLAKE3 + RSA-signed trace in Traceability |
| Earth Search (C1) | `S2B_T58MCT_20260715T233814_L2A` | `B04.tif` (COG) | 3,790,230 | SHA2-256 `122083cd30e8b9e2…153976` | 23 of 23 assets hashed |
| Planetary Computer | `S2B_MSIL2A_20260715T233819_R087_T58MCT_20260716T005600` | `…_B04_10m.tif` (COG) | 4,711,741 (HTTP Content-Length) | **none** (0 of 23 assets) | blob `Content-MD5: hbvE9XLBI0cUQLOeu03aWQ==` (storage header, unsigned) |

Sources: `https://stac.dataspace.copernicus.eu/v1/collections/sentinel-2-l2a/items?…`,
`https://earth-search.aws.element84.com/v1/search` (`grid:code = MGRS-58MCT`),
`https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-2-l2a/items?…`, HEAD on the PC blob with a
token from `/api/sas/v1/token/sentinel2l2a01/sentinel2-l2`.

Proposed caption (finding + scope): **"One Sentinel-2 band, three archives, three different files and three integrity
stories. An agent cites none of these files; it cites one value at one cell on one date. EMEM names that observation
and the file it was read from."** Scope line: "Pixel values across the three files were not compared here."
(Their equality is plausible for the same baseline but was **not measured**; do not print it.)

Honest companion fact (MEASURED): EMEM's Keylong records (207 facts, 213 source entries) carry **0** source hashes;
136 sources are Planetary Computer and 66 the Element84 v0 bucket, and both catalogues publish 0 per-asset checksums
(LIVE). So for today's records the source edge is location-only, and only a re-read tests it. That is the M15 lesson
and belongs in the guarantee ladder at L3 ("INHERITED / PARTIAL").

---

## 4. Field map of the workshop

Sources: https://agentic-eo.berlin/programme/posters/ (HTTP 200, 43 posters, 23 + 20), https://agentic-eo.berlin/
programme/schedule/ (HTTP 200), /programme/keynote-speakers/ (HTTP 200). `/programme/` itself returns 404 (LIVE).
No abstracts are published on the site; "likely claim" is **INFERRED from the title** unless a source is given.

### 4.1 Vocabulary counts (MEASURED over the 43 poster titles and all oral/demo/track titles)

| word stem | posters (S1/S2) | orals, demos, tracks |
|---|---|---|
| memory | 1/0 (EMEM) | 0 |
| content-address | 1/0 (EMEM) | 0 |
| verif | 1/0 (EMEM) | 2 (Axis Spatial "Verified Pipelines"; Track 2 "Verifiable Scientific Discovery") |
| valid / guardrail | 1/0 (GeoGuard) | 1 ("Scientific Validity", Lobelia) |
| provenance | 0/1 (Earthward) | 0 |
| trust | 1/1 (CARE/NASA; Earthward) | Track 2 "Trustworthy and Scientific Agentic AI" |
| audit | 0/1 (DRI) | 0 |
| evidence | 0/1 (SeismicAgent) | 0 |
| reproduc / traceab | 0/0 | 2 / 2 (VITO openEO; EO Agent Arena / Earthward; CARE) |
| pixel / grounded | 0/0 | TerraScope "Pixel-Grounded"; SAI4EO "Artifact-Grounded"; Aperture "Grounded" |

Reading (INFERRED): EMEM owns "memory" and "content-addressed"; "verification" is shared and "validation",
"trust", "provenance", "traceable", "reproducible" belong to neighbours. Headline verbs should be EMEM's own:
cite, hand off, resolve, re-hash, re-read (MASTER §23).

### 4.2 Poster Session 1 (Day 1, 19 Oct, 17:00–18:30, B. von Langenbeck, 1st floor): all 23

| # | title (short) | presenter, affiliation | likely claim | overlap | EMEM's one-line difference / hook |
|---|---|---|---|---|---|
| 1 | Fitness for Purpose as an Agentic Task: Domain Encoded Reasoning for EO Data Selection in Regulated Environmental Work | N. Alemi Kermani, Aniterra | agents select data fit for a regulatory purpose using encoded domain rules | medium (regulated evidence, like the EUDR screen) | "You choose the data; we record which observation was cited, so an auditor can re-check it." |
| 2 | SENSOR2RAG: Multimodal Sensor-to-RAG for Natural Capital Risk | J. Soldateschi, The Landbanking Group | RAG over in-situ sensor + EO data for site decisions | medium (RAG) | retrieval could return references, not paraphrased readings |
| 3 | Beyond Task Success: Domain-Grounded Evaluation of EO Agents in Environmental Risk Workflows | A. Oikonomidis, CERTH / NTUA | evaluation beyond task completion, domain-grounded metrics | medium (evaluation) | "EMEM gives your evaluator a checkable record of which evidence the agent used." Not the same as arXiv 2604.19818 (Koch & Wellbrock, same main title, different authors). |
| 4 | **EMEM** | J. Kumari, Vortx AI | – | – | – |
| 5 | CLUES: Geospatial Data in Biomedical Research | M. Jentsch, BIH@Charité | workflow linking geodata to health studies | low | exposure linkage needs as-of citation (Bengaluru example) |
| 6 | GEODES Assistant | K. Perriot, THALES | conversational assistant for an EO data portal (INFERRED: CNES GEODES) | low | – |
| 7 | From Isolated Models to Agentic Orchestration: Ground Segment Multi-Agent Framework for Water Resilience | R. Escolà, M. Badenas-Agusti, isardSAT | multi-agent ground-segment orchestration | medium (inter-agent handoff) | "What do your agents pass each other: numbers or references?" |
| 8 | THEDE: Thematic Datacubes On-Demand | E. K. Bellotto, Sistema | LLM maps EO tasks to datacube requests; RAG + prompt engineering; EGU26-5722 abstract does not mention provenance or integrity (SPEC via WebFetch summary) | medium | THEDE: which data to retrieve. EMEM: which observation the last agent cited. |
| 9 | EIS: Open-Source Geo-Agent Framework | M. Mattiuzzi, European Environment Agency | open agent framework for environmental knowledge | medium | EMEM plugs in as an MCP server underneath |
| 10 | AI Agentic Development of xAI for EO: SegExplainer | Y. Grushetskaya, M. Sips, GFZ | agents used to build explainability tools | low | – |
| 11 | Ask, Detect, Explain: End-to-End Agentic Satellite Change Detection | B. Ostrowski et al., CloudFerro | agent does change detection end to end | medium (dates) | date substitution (defect 27) is exactly the change-detection trap |
| 12 | Agentic Interaction between Raster Flood Observations and GIS Features | J. Bosmans, VITO | raster-vector reasoning for crisis awareness | medium (entity identity) | pixel binding is in scope; which feature a pixel belongs to is not (M17) |
| 13 | LATINSIGHT: ReAct Multi-Agent Urban EO Analytics | E. Schettino, P. De Piano, Latitudo 40 | multi-agent urban analytics | medium | inter-agent evidence |
| 14 | ECHOSAT: Physically Consistent Canopy Height Mapping | B. Turan, Zuse Institute Berlin | canopy height as an enabling layer for agents | low–medium | derived products as addressable records |
| 15 | Engineering a Trustworthy NASA Earth Science Discovery Agent Using CARE | L. Thomas, Development Seed | CARE methodology (arXiv 2604.28043): stage-gated artifacts for behaviour, grounding, tools, verification; NASA CMR discovery agent | medium ("trustworthy") | CARE engineers the agent; EMEM is an artifact format for the evidence it cites |
| 16 | Simulation Study of LLM-Based Onboard Orchestration for EO Constellations | C. Castro Traba | simulated onboard LLM orchestration | low | keep SAT-042 labelled as a harness |
| 17 | Agentic Ground Segment: Data Discovery, Processing, Ordering, Operations | F. Bianchini, Telespazio | GenAI redesign of ground-segment workflows | medium | – |
| 18 | Hierarchical System with Agentic Refinement for Large EO Archives | O. Dutta, J. Vitorino, GMV | agentic search over archives | medium (archive identity) | section 3 figure is a conversation starter |
| 19 | AI-Driven ASAP Country Assessments | F. Sabo, JRC | AI-assisted agricultural anomaly country assessments | medium (high-stakes citations) | assessments that cite indicators could cite references |
| 20 | From EO Data to Decision: Agentic Architecture for Disaster Resilience | B. Augustyn, M. Kluczek, CloudFerro | end-to-end decision agent | medium | – |
| 21 | Disaster Resilience through Agentic AI in the EO-PIN Suite | G. Schumann, RSS-Hydro | agent integration in a flood product suite | low–medium | – |
| 22 | EO Agents in Actions: Lessons Learned from Building Products Around Analysis Agents | L. Thomas, D. Patel, Development Seed | practical failure lessons | medium | ask which silent errors they saw; compare with section 5 |
| 23 | GeoGuard: Agentic Guardrails and Validation Framework for Geospatial AI | R. S. Sahoo, UAH (+ Pantha, Thapa, Ramasubramanian, Ramachandran) | post-hoc claim validation against authoritative data (SPEC, section 2.7) | **high vocabulary overlap** | "GeoGuard judges the claim. EMEM fixes the evidence it cites." |

### 4.3 Session 2 neighbours (Day 2, 20 Oct, 17:45–19:00)

| title (short) | presenter | why it matters to EMEM |
|---|---|---|
| Provenance-First Geospatial Composition: A Scaffold-Based Builder as a Trust-Bearing Counterpoint to Agentic Autonomy | S. Chithamanan (Earthward, 33 Blueprints), A. S. Subramanian (TUM, Earthward); also Featured Demo 1 "Earthward: A Human-in-the-Loop Architecture for Traceable, Explainable Agentic EO Workflows" | the conceptually closest title. Their unit (INFERRED) is a provenance-bearing workflow; EMEM's is an observation reference handed between agents. Show the arrow **Agent A → token → Agent B**, not pipeline → audit trail (field-map critique §2). |
| Agentic AI as an Auditable Co-Scientist for Irrigation Mapping and Groundwater Accounting | P. ReVelle, DRI | "auditable" workflows; EMEM records make an audit re-checkable |
| SeismicAgent: Benchmarking Evidence-Conflict Reasoning for Post-Earthquake Damage | F. Elik, Istanbul MM | evidence conflict between sources; EMEM keeps both signed observations (Bengaluru 918.0 vs 915.07) rather than resolving them |
| Learned Satellite Embeddings as Covariates for Soil Mapping | L. Poggio, ISRIC | embeddings; "derived representations are addressable too" |
| Specialized Geospatial FMs for Agentic EO (Spheer FM); TerraMind vs THOR diagnostic | Spheer; Bertelsmann Foundation | encoder version binding |
| Airbus Geo Explore: Semantic Search APIs for LLM Agents | F. Benatia, Airbus DS | retrieval layer |
| Multi-Satellite Task Orchestration with On-Board VLMs | R. D'Ercole, A.-M. Pelin (ESA Φ-lab, TU Delft) | onboard agents: SAT-042 must stay "harness, no spacecraft" |
| Aperture (LiveEO); FlyPix AI; VISEO (THALES); EOMAS; Manteo AI; Space–Ground–Cloud continuum | – | EO agent systems |

### 4.4 Orals, demos, tracks and keynotes that shape the conversation

- **Day 1 13:45 keynote, Salman Khan (MBZUAI)**, "Agentic AI for Earth Observation and Climate Resilience": last
  author of ThinkGeo, OpenEarthAgent and the position paper 2604.24919 (with B. Demir). Three hours later EMEM's
  session opens; the "silent error propagation" framing will be fresh (INFERRED).
- **Day 1 15:36 oral**, "Agentic Orchestration of EO Foundation Models via the Model Context Protocol" (Banerjee,
  Sedona, Jülich); **15:48 oral**, "TerraScope: Pixel-Grounded Visual Reasoning for EO" (Yan Shu, Trento; arXiv
  2603.19039, Shu, Ren, Xiong, **Zhu**). "Pixel-grounded" there means visual grounding; EMEM's "right record, wrong
  pixel" is about which source pixel a reader sampled. Avoid "pixel-grounded" on the board to prevent confusion.
- **Concurrent with Poster Session 1 (17:00–18:40)**: Featured Demos 3–10, including Axis Spatial "From Fragmented
  EO/GIS Projects to **Verified Pipelines**" and GEONOVA "Agentic EO Copilot for Geospatial **Embeddings**"; the
  "Subway Takes" discussion 17:00–17:30 (Lecture Hall). Visitors arrive in waves; the 3 m layer must work in seconds.
- **Day 2 14:00 keynote, Manling Li**, "Failure Mode in Agentic Reasoning"; **Oral Session 3 (14:30–15:45)**,
  "How should EO agents be built, evaluated, validated and trusted?": CARE (Sahoo), Evaluating EVE (Φ-lab), **EO
  Agent Arena** (Axis Spatial, "Reproducible Evaluation"), **ARM behavioural self-monitoring** (Thales Alenia Space),
  "Balancing Accessibility and Scientific Validity" (Lobelia), EVE's community MCP registry (Pi School). These come
  after EMEM's session; attendees of Session 2 will have heard them.
- **Day 3 keynotes**: Davide Crapis (Ethereum Foundation; co-author of ERC-8004 "Trustless Agents", identity,
  reputation and validation registries; SPEC https://eips.ethereum.org/EIPS/eip-8004) and **Christopher F. Brown**
  (Google DeepMind; first author of AlphaEarth Foundations, arXiv 2507.22291), "Why Mature Agents Require a
  Paradigm Shift in Tooling". Both are natural conversations for "evidence as a verifiable tool result".
- **Day 3 Track 2**: "How Do You Know Your Agent Works? Evaluating EO Agents with Existing Benchmarks" (Pi School,
  ESA) and "From Vibe Coding to Verifiable Scientific Discovery" (Jülich, UAH, Pi School).
- **Other demos near EMEM's layer**: VITO "Reproducible openEO Workflows on CDSE"; Planetek SAI4EO
  "Artifact-Grounded Geospatial Intelligence"; EURAC "Portable Agentic openEO"; Pi School "EVE … Open MCP Tool
  Registry"; EOX "Agent-to-UI Streaming".

### 4.5 Whitespace (INFERRED)

The programme has agents that choose data, run workflows, orchestrate, explain, evaluate and validate. No title is
about what one agent hands another as evidence, or whether the receiver can check it. EMEM should occupy exactly that
and borrow the organisers' own words for the problem ("errors may propagate silently across steps", 2604.24919).

---

## 5. Why EMEM's own bugs are the field's bugs (user's point, with outside sources)

Report 02 §18 maps each emem defect to a mutation and the check that catches it. This section adds the outside
evidence that the same classes are documented elsewhere, so the poster can say "these are not our bugs; they are
everyone's, and we measured them in ours".

| class (emem instance) | outside evidence the class is general | who else in the room is exposed (INFERRED) | layer that catches it |
|---|---|---|---|
| wrong source pixel, signed faithfully (M15; 162/200 pre-fix records, `CHANGELOG.md:68`) | position paper 2604.24919: "silent propagation of preprocessing errors", "outputs that appear plausible but violate geospatial or physical validity" | any agent tool doing point reads from COGs (GeoGuard's flood tool, change-detection agents) | L3 source re-read; not signatures |
| date substitution (defect 27; 9/10 agents never saw the requested date) | 2604.24919 "temporal-window mismatch"; GeoGuard's disclosed ±2-day fallback | change detection, crisis agents | L1 binding of `tslot` to the question |
| place resolution overrides coordinates (defect 37; 597 m) | 2604.24919 "spatial or temporal misalignment" | anything that geocodes names (GeoGuard uses Nominatim) | L1 cell binding; entity layer out of scope |
| paraphrase and agreement drift ("0.47"; 0/72 correct under compaction, p = 0.035) | Perez et al. ICLR 2025 (transmission chains drift to attractors); Laban et al. 2505.06120 (multi-turn loss); *Deliberative Illusion* 2606.03032 ("up to 72% of issue-critical facts" erased; "agents can agree more while knowing less") | every multi-agent system | resolve the reference, use the served value verbatim |
| compaction drops what matters | *Lost in Compaction* 2608.11242: compactors retain 17% of session constraints | long-horizon agents | a short resolvable reference survives compaction (ARC makes the same bet within one agent) |
| verification that does not verify (guard answered `allow` on a misspelt field, defect 13; refusal returned as text by an adapter) | MAST (Cemri et al., 2503.13657): 14 failure modes over 1,600+ traces from 7 frameworks, category (iii) "task verification": FM-3.2 "No or incomplete verification", FM-3.3 "Incorrect verification" | every guardrail and verifier, including EMEM's | fail-closed resolver (E+ in report 02) |
| poisoned or stale memory presented as current (M16, M20) | OWASP Top 10 for Agentic Applications 2026, released 9 Dec 2025 (LIVE, genai.owasp.org); per secondary sources ASI06 "Memory & Context Poisoning", ASI07 "Insecure Inter-Agent Communication" (UNVERIFIED against the PDF); PoisonedRAG; AgentPoison; Prompt Infection 2410.07283 | RAG and memory-backed agents | L0 hash + log (M16); as-of binding (M20) |
| handles carried by the model, unchecked | MCP 2026-07-28: "a handle is a name, not a capability"; "The model is responsible for carrying [it] forward" | every stateful MCP server | a content-addressed, signed handle |

**Poster sentence (bounded, 31 words):** "Every error in this table happened inside a system built for evidence. The same classes are documented across
multi-agent systems; what EMEM adds is that each one became checkable at handoff."

Must not say: that EMEM prevents these errors (its signatures prevented none of the T2 rows, report 02 §18), or that
other named systems have these bugs (only GeoGuard's date fallback was read in code, and it is disclosed).

---

## 6. Verification of the related-work citations used on older boards

All via the arXiv API (`export.arxiv.org/api/query?id_list=…`), LIVE, 2026-10-01.

| as printed on v10/v11 | verified identity | relevance (INFERRED) | status |
|---|---|---|---|
| "Perez et al., ICLR 2025" | arXiv **2407.04503**, *When LLMs Play the Telephone Game: Cultural Attractors as Conceptual Tools to Evaluate LLMs in Multi-turn Settings*; J. Perez, G. Kovač, C. Léger, C. Colas, G. Molinaro, M. Derex, P.-Y. Oudeyer, C. Moulin-Frier; comment: "published at … ICLR2025" (iclr.cc poster 28880) | transmission chains of LLMs transform text toward attractors (toxicity, positivity, difficulty, length). Analogy for handoff drift; they study text properties, not numeric evidence | **VERIFIED** |
| "arXiv 2608.11242" | *Lost in Compaction: Evaluating Side-Constraint Loss under Context Compaction*; Zhiqi Wang, Yichi Zhang, Dongwon Lee, Yuchen Yang; submitted 2026-07-31; COMPINT suite; "Current compactors retain only 17% of injected SCs on average" | compaction silently drops constraints; supports "a paraphrase is not a citation" | **VERIFIED** (preprint, no venue) |
| "arXiv 2607.25066" | *Addressable Recall Compaction for Long Context-Window Control in AI Agents* (ARC); Thang Dang, Yuma Ichikawa, Sakina Fatima, Koichi Shirahata; 2026-07-27; 20 pp. | append-only, content-addressed (SHA1) store of one agent's tool observations with citations; closest conceptual competitor | **VERIFIED** (preprint) |
| (invention register) Laban et al., arXiv 2505.06120 | *LLMs Get Lost In Multi-Turn Conversation*; P. Laban, H. Hayashi, Y. Zhou, J. Neville; 2025 | multi-turn degradation | **VERIFIED** |
| (invention register) arXiv 2606.03032 | *The Deliberative Illusion: Diagnosing Factual Attrition and Stance Homogenization in Multi-Agent LLM Deliberation*; H. Wan, J. Wu, M. Luo, F. Li, N. Wang, N. F. Chen, et al.; 2026 | "agents can agree more while knowing less"; up to 72% of issue-critical facts erased | **VERIFIED** |

Recommended 30 cm citation line (fits one line at the board's reference size): "Perez et al., ICLR 2025
(arXiv 2407.04503); Wan et al. 2026 (2606.03032); Wang et al. 2026 (2608.11242); Dang et al. 2026, ARC
(2607.25066); Munir et al. 2026 (2604.24919); Cemri et al. 2025, MAST (2503.13657)."

---

## 7. Twenty-second answers (issue #22; 34 to 53 words each, about 20 s at ~150 wpm)

Each answer: what the other system does, what EMEM does, how they compose, one number where one exists. Sources in
brackets are for the rehearsal sheet, not for reading aloud.

**Why not STAC?** (53 words)
"We use STAC. A STAC item finds a file, and where the archive publishes one, a checksum fixes that file's bytes:
Earth Search yes, CDSE yes, Planetary Computer no. An agent doesn't cite a file. It cites one value at one cell, band
and date. EMEM signs that observation and names its file."
[§2.1, §3; LIVE item counts]

**Why not RAG?** (53 words)
"RAG decides what text the next model sees. It gives the receiver nothing to check that the text still says what
was observed. In our mutation test, prose and JSON handoffs let 15 of 15 applicable corruptions through; the full
receiver check stopped all 16. A retriever can hand over EMEM references instead."
[R1 `research/repro/v11/out/summary.md`; RAG arm pending in R5: say "prose and JSON", never "RAG", until R5 runs]

**Why not C2PA?** (52 words)
"C2PA signs a media file and its edit history, and we'd use it for a rendered map. An agent's evidence is a value
inside a file, at a place and time. EMEM binds that observation. And C2PA says the same thing we do: a valid
signature is not a judgement of truth."
[C2PA 2.4 §1.2 guiding principles; emem federation.md §9c.8 "Later"]

**Why not GeoGuard?** (51 words)
"GeoGuard judges a claim against outside data; on their benchmark no fabricated flood event was endorsed, zero of
fifteen. EMEM does something narrower: it lets the receiver check that the evidence it holds is exactly what the
sender observed. Put EMEM facts under GeoGuard's tools and its verdicts become re-checkable later."
[§2.7; GeoGuard poster doc §06]

**Why not PROV?** (48 words)
"PROV is the vocabulary for lineage: entity, activity, agent. It says how something was made; it doesn't let a
receiver test that the bytes in hand are the ones described. PROV has no signature or hash. EMEM's record carries
both, and its derivation fields map onto PROV terms."
[PROV-DM, W3C Rec. 2013; MEASURED 0 hits]

**Why not openEO?** (51 words)
"openEO runs the computation and returns results as STAC. EMEM doesn't execute anything. It records the one output an
agent cited, with the recipe that produced it, so a second agent can recompute it. An openEO process graph could be
that recipe. openEO's 'signed URLs' control access; they don't sign results."
[openEO API 1.3.0 openapi.yaml, list-results]

Six more the room will ask (same length rule):

**Isn't MCP enough?** (53 words) "MCP moves the call. Since July, state is a server-minted handle the model carries as an
ordinary string, and the spec says a handle is a name, not a capability. Nothing checks it. An EMEM token is a handle
the receiver can verify. Six proposals to sign MCP results or tool definitions are closed." [§2.12]

**A2A signs things already.** (34 words) "A2A signs the Agent Card: who the agent is. The artifacts agents exchange carry an id,
not a hash or a signature. EMEM signs what they exchange. Our own Agent Card is signed too." [§2.13; LIVE card]

**Isn't this Sigstore or SCITT for data?** (48 words) "Yes, the same pattern: sign a statement about a digest, log
it, hand out a proof. Sigstore applies it to software, SCITT to supply chains. We apply it to Earth observations that
agents cite. We don't speak SCITT's receipt format yet, and our log uses BLAKE3, not SHA-256." [§2.8–2.9]

**ARC already content-addresses agent memory.** (45 words) "It does, inside one agent's task, so the agent can recover
what compaction removed. EMEM crosses agents and organisations: the record is signed and logged, names its place,
band, date and source, and a receiver who never saw the sender's context can re-read the pixel." [§2.14]

**Isn't this versioned data citation?** (45 words) "RDA's data-citation recommendations already timestamp data, store
the query and hash the result. EMEM applies that idea to a single observation. The as-of read returns what was known
then, and the reader checks a signature and a public log instead of asking the data centre." [§2.11; RDA wording UNVERIFIED]

**Why not just hash the file (IPFS)?** (44 words) "A CID tells you which bytes, and we use the same format. But one
Sentinel-2 band exists as three different files in three archives. The thing an agent cites is the observation, so
that is what we address, and the record names the file." [§2.10, §3]

---

## 8. Board copy candidates (every word counts; gate words avoided)

- Layer figure title (5 words): **"Seven layers, one question each."**
- Layer figure EMEM label (8 words): **"EMEM: is this the observation the sender cited?"**
- The critical answer (MASTER §14, 22 words): **"A STAC item identifies a file. EMEM identifies the observation an agent
  cited, and gives the next agent something it can re-check."**
- Complementarity line (10 words): **"EMEM relies on these layers. It replaces none of them."**
- Pattern credit (15 words): **"The pattern is from software supply chains: sign a digest, log it, verify the proof."**
- GeoGuard line (10 words): **"GeoGuard judges the claim. EMEM fixes the evidence it cites."**
- MCP line (9 words): **"MCP moves the call. The token is the evidence."**

Do not use on the board: "first", "only", "unique", "replaces", "trustless", "guarantees", "proves", "truth",
"verified" without a layer (issue #21), "pixel-grounded" (collides with TerraScope), "provenance-first" (Earthward),
"guardrail" as a self-description (GeoGuard), "RFC 6962 log" unqualified, "RFC 8949" as a conformance claim.

---

## 9. Open items and caveats

1. GeoGuard facts come from its repository's poster markdown and code at `main` on 2026-10-01; the printed poster
   may differ. Commit hash not recorded (the GitHub API is not reachable for that repo from this session; raw files were).
2. Why the six MCP proposals were closed (rejected, superseded, moved to the extensions process) was not established.
3. RDA WGDC recommendation wording (R6, R9) is from search summaries of RDA documents, not from the full text.
4. The OWASP ASI06/ASI07 names are from secondary sources; only the 9 Dec 2025 release on the OWASP page was seen.
5. Pixel values of the three B04 files in section 3 were not compared; do not claim they are equal.
6. The CDSE trace signature and emem's Agent Card JWS were read, not cryptographically verified here.
7. Session-2 and oral "likely claims" are title-level inferences; no abstracts are published on agentic-eo.berlin.
8. Earthward (Provenance-First) has no public paper found; the collision risk is judged from the title alone.
9. Upgrade for emem maintainers (not a poster claim until built): fill `Source.hash` from STAC `file:checksum`
   (Earth Search C1: SHA2-256; CDSE: SHA3-256) and from the CDSE trace (BLAKE3 + signed trace id) when a fact is read
   from those archives; mark Planetary Computer and Element84 v0 reads as "location-only".
