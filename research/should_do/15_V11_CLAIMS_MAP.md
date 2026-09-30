# v11 claims map: every number on the board, and where it comes from

Board: `poster/src/poster.v11.html` (built to `poster/poster.html`, `emem-poster-A0.pdf`).
Checked on 30 Sep 2026 against two independent audits committed in `research/audit_v11/`:

- `emem_capability_index.md` / `.json`: the whole of emem at HEAD `e226f8b`, with file and line pointers
  and 10 read-only GETs to emem.dev (16:53 to 16:57 UTC). Code was read, not compiled.
- `poster_evidence_audit.md` / `.json`: all 96 printed v10 claims checked against this repository.

Evidence classes: **code** (read in emem's source), **live** (read from emem.dev on 30 Sep),
**track** (a step of the signed evidence track `njedkglt/7n7qogvn2ib3er5nreorzmfnbu.md`, printed as §n),
**measured** (our own run, data in `research/repro/`), **pre-reg** (pre-registered, hash committed),
**README** (emem's README at `e226f8b`, not re-measured by us).

## Scale line (v11.2 replaced the six-number live strip)

Printed once, in the sub-heading of "What agents do with it": 2.57 M signed log entries, 168 versioned algorithms,
46 source schemes (30 Sep 2026).

| printed | value | source | class |
|---|---|---|---|
| log entries | 2.57 M | /v1/log/sth tree_size 2,568,372 at 16:53Z | live |
| published algorithms | 168 | /v1/algorithms `pagination.total` | live; 39 of 168 need retired encoder bands |
| source schemes | 46 | /v1/manifests `covers.sources` | live |

No longer printed: 114 MCP tools, 177 REST paths (product metrics) and 118 wired measurements (provisional: the agent
card says 118, /v1/materializers says 116).

## Hero (figure 1)

| printed | source | class |
|---|---|---|
| the NDVI record: cell `defi.zb572.xoso.zb1ec`, tslot 20721, value 0.4708994708994709, DN B08 3502, B04 1900, offset −1000, signed 2026-09-28T09:06:56Z | §4 | track |
| fact_cid `oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa`, 1,115 bytes | §4; `research/repro/v8/trace_fact_output.txt` | track + measured |
| 2.02 GB scene, 1.17 MB read, 0.058 % | `research/repro/data/v8/scene_sizes.json`, `cog_pixel_bytes.json` | measured |
| cell 9.5 × 8.1 m | cell64 quantisation, `research/repro/v10/algorithms.md` | code |
| batch signing over a Merkle root of sorted fact_cids; RFC 6962-shaped log | `research/repro/v10/algorithms.md` (emem @18adb67) | code |
| signed absence | `/v1/plane/conformance`; README Venice example | code + README |
| Bengaluru 918.0 m and 915.07 m | §12, §13 | track |
| token families and the ≤ 256 bundle limit | capability index §2 | code |
| six receiver checks with stock libraries | `research/repro/v8/trace_fact.py` | measured |
| "agents cannot write observations" | capability index §4; `/v1/plane/conformance` | code + live. Precise form: agents cannot write primary observations; a caller's derived value is kept only after emem recomputes it (C6) |
| device gate ships, no hardware enrolled | §26; capability index (17 device platforms, all `candidate`) | code + live |
| TESSERA retired | capability index §8: production unit sets `EMEM_RETIRED_BANDS=geotessera,clay_v1,prithvi_eo2,galileo` | code |

## Contributions C1 to C6

| card | printed evidence | source | class |
|---|---|---|---|
| C1 | 1,115 bytes, 2.02 GB, 84 characters; ten paths × three runs, one fact_cid | §4; crossruntime_table.json; token_counts.json | track + measured |
| C2 | 918.0 → 915.07 m; as-of recall; receipt binds the as-of bounds; the contradiction detector labels the pair a provider substitution | §12, §13; capability index §1, §4 | track + code |
| C3 | Venice absence `exhq6lps…` in Overture 2026-09-23.1; `/v1/plane/conformance` | emem README lines 40 to 47; capability index §3 | README + live |
| C4 | 443 × 453 px B04 raster §5; 5-scene cube §6; 238.7 MB COG in 292 chunks §2; bundle of 8 behind 38 characters §16 | track steps; token_counts.json (bundle 38 chars) | track + measured |
| C5 | 15 links, 17 checks, 17.9 s §22; clean-room verifier, 725 requests, five tampered receipts rejected, eleven findings of which eight real defects since fixed | §22; emem README line 65 and docs/benchmarks.md | measured + README |
| C5 | verification depth levels | capability index §3 | code |
| C6 | −0.1298 recomputed bit-identical §11; guard refuses "35 °C" against a signed 28.0 °C §14; ULP window 0, 4 for n-ary sum and mean | track; `research/repro/v10/algorithms.md` | track + code. The derive response itself (ulp_gap = 0) is not committed; commit it |

## What agents do with it

The eight job tiles name tools listed in the capability index (§4) and the "What agents do with it" table of
emem's README. The four "in the wild" items are README claims, not re-measured by us:
common decoder across three vendors (README lines 101 to 103), the geo.qa Doha dispute 9.8 m vs 5.4 m
(line 109), eudr.dev (builders section), second node and air-gapped build (lines 246 to 256).

## Results

| result | printed | source | class | caveat that must travel |
|---|---|---|---|---|
| R1 | 17 mutations x 9 depths; acted on corrupted evidence: prose 15/15, JSON 15/15, opaque id 13/16, hash 12/16, binding 9/16, signature 3/16, log 2/16, recompute 1/16, re-read 0/16; decision flips in 6 of 16; leave-one-out shows binding, signature, log, recompute and re-read each necessary; genuine never refused | `research/repro/v11/mutation_suite.py`, `research/repro/v11/out/mutation_matrix.json` (inputs: `v8/proof_bundle_ndvi.cbor`, `data/v8/pixel_windows.json`) | measured, deterministic | tests the verifier, not a model; T2 rows use a TEST key the verifier trusts; the source re-read uses the committed 25 Sep window, so a forged scene id (M11) is caught by the signature, not by the re-read; the hash is subsumed by the signature; units, checkpoints, embeddings not covered |
| R2 | 72/72 and 36/36; 20/72 and 15/36; 0/72 and 3/36; one-sided Fisher p = 0.035; handoff prose 2/20, dense 8/20, BM25 20/20, bundle 20/20 | §17, §18 (emem docs rows); Fisher recomputed 0.0350 by the claims audit | pre-reg | pairs and answers share trials, so read as descriptive; two open models on one host; handoff single-token arm excluded for a window bug; emem-authored benchmark |
| R3 | token 10/10, prose 10/10, rounded 0/5, forged 5/5 declined | §22; `research/repro/data/v8/results.json` | pre-reg (rounded arm exploratory) | re-hash and receipt were done by the harness, not by model B; the Qwen2.5-3B arm is withheld until its raw logs are committed |
| R4 | 918.0 m signed 2026-05-28 (open_meteo_copdem90m@1); 915.07 m signed 7 times from 2026-08-11 (copernicus_dem_30m_aws_pixel@1); as of 1 May nothing, 15 Jun 918.0, 12 Aug 915.07, 29 Sep 915.07; scope same_attester_provider_substitution | `research/repro/data/contra_bengaluru.json`; live replay table in `09_INVENTION_REGISTER.md` (from `research/repro/verify_bitemporal.py`); the figure recomputes the as-of answers with the protocol rule and asserts they equal that table | measured + live | one key, one attester; the as-of compare is a string compare in code (defect 35), which is exact for these UTC second-precision timestamps |
| R1 caption, M15 in production | the reader error before 28 Sep; only the re-read catches it | §7, §8; 162/200 (81 %, Wilson 75 to 86 %) and 49/49 after the fix are in `prevalence_summary.json`, `pixel_windows.json` | measured | the numbers are no longer printed on the board; the pixel-audit figure `fig/v11/r2_pixel_audit.svg` is still generated for handouts |

The v10 drift taxonomy (seven real drifts, six located by one field) is no longer on the board; R1 covers the same
cases as mutations M2, M4, M5, M15 and M17, each marked "seen in production". The taxonomy stays in
`poster/archive/v10/poster.html`.

## What a verified token guarantees (v11.2 wording of the identity table)

| row | value | source |
|---|---|---|
| exact bytes; place and time; derivation | yes, yes, checkable | R1 checks D to I |
| upstream file | partial, printed as "upstream identity unverified" | the record names the COG URL and pixel, but no provider-issued identity (checksum, signed STAC item) is bound; field-map critique `10_EVENT_FIELD_MAP_AND_CRITIQUE.md` |
| physical entity; truth; decision | no | R1 M17; mechanism |

## Objections

| objection | numbers | source |
|---|---|---|
| token cost | 46 vs 8 tokenizer tokens (about 6×) | token_counts.json (cl100k). The 9.5× in emem's docs is a different measurement and is no longer printed |
| BM25 | 16/16; dense 4/142 exact, up to 138 confidently wrong, median 252 m | §25 |
| encoders | Clay, Prithvi-EO-2.0, Galileo, JEPA removed §23; old vectors resolve §24 | track (doc rows). Pre-retirement vector recall was not exercised end-to-end by the inventory |
| guardrail vs provenance vs STAC | positioning, no number | GeoGuard (same session), Provenance-First Geospatial Composition (Session 2), STAC/C2PA/PROV |
| operator | 111 witness keys (109 key-only, 2 organisation-vouched); one independent operator domain, geo.qa, also Vortx AI | /v1/log/witnesses `.witness_keys_by_tier`, `.independent_operator_domains` (live, 30 Sep) |

## Removed from v10 because no source is committed

- the tampered-mirror claim (panel 2)
- the Copernicus Data Space and NASA Earthdata rows (panel 11)
- the local-node re-read (panel 12)
- the footer traffic figures (96,728 MCP calls, PyPI 314, npm 304, 96.2 %)
- the Qwen2.5-3B numbers (arm kept as a sentence, numbers withheld)
- "logged as entry 2,568,005" for the seal (no leaf index is recorded)

Each can come back once its run is committed.

## Conclusion (v11.2)

| printed | source |
|---|---|
| checks offline in under 2 ms | `research/repro/v11/out/mutation_matrix.json` `meta.full_verification_ms` (1.2 to 1.5 ms across runs, Python, one laptop core) |
| five of the six checks each stop a corruption the others miss; together all 16 in-scope cases | R1 leave-one-out and level I |
| records never rewritten; as-of answers across a source change and retired encoders | R4; §23, §24 |
