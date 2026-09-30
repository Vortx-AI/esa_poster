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

## Live strip

| printed | value | source | class | note |
|---|---|---|---|---|
| MCP tools | 114, core 18 | /v1/agent_card `.tools.count`, `.tools.core`; 114 `ToolDescriptor` entries in `crates/emem-mcp/src/lib.rs` | live + code | the claims audit saw 116 in one listing; agent card and code agree on 114 |
| published algorithms | 168 | /v1/algorithms `pagination.total` | live | 39 of 168 need retired encoder bands and cannot produce new values |
| wired measurements | 118 | /v1/agent_card `band_taxonomy.materializer_wired.count` | live | **provisional**: /v1/materializers reports 116; cause not isolated |
| source schemes | 46 | /v1/manifests `covers.sources` | live | |
| log entries | 2.57 M | /v1/log/sth tree_size 2,568,372 at 16:53Z | live | hero prints 2,568,005, the size stamped when the track was sealed |
| REST paths | 177 | /openapi.json paths under /v1 | live | 188 paths in all, 206 operations |
| client paths, one fact_cid | 10 | `research/repro/data/v8/crossruntime_table.json` (reps = 3) | measured | |

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
| R1a | 72/72 and 36/36; 20/72 and 15/36; 0/72 and 3/36; one-sided Fisher p = 0.035 | §17 (emem docs row); recomputed 0.0350 by the claims audit | pre-reg | pairs and answers share trials, so the test is read as descriptive; two open models on one host |
| R1b | prose 2/20, dense 8/20, BM25 20/20, bundle 20/20 | §18 | measured | single-token arm (16/20) excluded for a window bug; emem-authored benchmark |
| R2 | 162/200 (81 %, Wilson 75 to 86 %); after the fix 49/49 read the containing pixel where rules differ | §7, §8; `research/repro/data/v8/prevalence_summary.json`, `pixel_windows.json` | measured | the neighbour is east, south or south-east (both axes were rounded); the pictured case is south |
| R3 | token 10/10, prose 10/10, rounded 0/5, forged 5/5 declined | §22; `research/repro/data/v8/results.json` | pre-reg (rounded arm exploratory) | the re-hash and receipt were done by the harness, not by model B. The Qwen2.5-3B arm is withheld until its raw logs are committed |
| R4 | seven drifts, six located by one field | v10 drift taxonomy; §4, §6, §7, §13, §21 | measured + track | the referent drift (Maasvlakte) is not caught; entity tokens are labels |

## Objections

| objection | numbers | source |
|---|---|---|
| token cost | 46 vs 8 tokenizer tokens (about 6×) | token_counts.json (cl100k). The 9.5× in emem's docs is a different measurement and is no longer printed |
| BM25 | 16/16; dense 4/142 exact, up to 138 confidently wrong, median 252 m | §25 |
| encoders | Clay, Prithvi-EO-2.0, Galileo, JEPA removed §23; old vectors resolve §24 | track (doc rows). Pre-retirement vector recall was not exercised end-to-end by the inventory |
| operator | 111 witness keys; one domain-vouched, geo.qa, also Vortx AI | /v1/log/witnesses (live) |

## Removed from v10 because no source is committed

- the tampered-mirror claim (panel 2)
- the Copernicus Data Space and NASA Earthdata rows (panel 11)
- the local-node re-read (panel 12)
- the footer traffic figures (96,728 MCP calls, PyPI 314, npm 304, 96.2 %)
- the Qwen2.5-3B numbers (arm kept as a sentence, numbers withheld)
- "logged as entry 2,568,005" for the seal (no leaf index is recorded)

Each can come back once its run is committed.
