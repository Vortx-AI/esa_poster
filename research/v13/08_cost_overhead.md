# 08. Cost and overhead: what EMEM buys, and what it costs

Written 2026-10-01 (UTC) for the v13 final A0. Topic: `cost` (MASTER §18: "What does this buy, and what does it cost?").
Read-only research. Nothing on the board, in emem or in the repo was changed except this file and
`research/v13/cost_measurements.json` (all raw numbers behind every MEASURED row below).

Labels on every item:

- **MEASURED**: measured in this session on 2026-10-01 (command or script named; raw values in `cost_measurements.json`).
- **MEASURED (committed)**: a number in a committed repo file, re-read here (file:line given), not re-run.
- **LIVE**: fetched from a live service in this session (URL, time).
- **SPEC**: stated by emem's docs or code at `origin/main` 18adb67, not exercised here.
- **INFERRED**: arithmetic or reading from the above.
- **UNVERIFIED**: stated somewhere, not checked.

Environment for every MEASURED row (this matters for the numbers): 4 vCPU container, Intel Xeon @ 2.80 GHz,
Python 3.11.15, curl 8.5.0, blake3 1.0.10, pynacl 1.6.2, cbor2, tiktoken 0.14.0. All HTTPS left the container through a
local agent proxy to a **TLS-re-terminating egress proxy** (`/root/.ccr/README.md`: "TLS is re-terminated there"), HTTP/1.1
only (`curl --http2` still negotiated 1.1). Network latencies are therefore this path's, not a researcher's laptop's and
not emem's loopback figures. emem served `x-emem-commit: 8e9b401cecae7ab9944d403a2d7840952c6586a6` (LIVE, 00:34Z).

Read-only discipline: emem.dev received only GETs (`/v1/facts/<cid>`, `/v1/log/*`, `/v1/memory_bundle/<token>`,
`/.well-known/*`, `/v1/verifier_spec`, `/openapi.json`) plus JSON-RPC `tools/list` on `/mcp` and `/mcp/full`. No
recall, ask, band_raster, backfill, memory_token/resolve, range_hash or any write was sent; nothing was signed or
published; no key file was touched.

---

## 0. Findings in one screen

1. **Checking a handed-over record is cheap; re-reading its source is not.** All offline checks on one Sentinel-2 NDVI
   record (hash, cell/band/date binding, signature, log inclusion, NDVI recompute, cached-pixel compare) take
   **0.36 ms** of CPU per decision (n = 30 batches of 200, IQR 0.35 to 0.37 ms). Re-reading the source pixel cold over
   this network takes **about 6.9 s and 1.18 MB** (STAC item, SAS token, two 64 KiB COG headers, B08 + B04 tiles, SCL),
   about **19,000 times** the time and **1,059 times** the bytes of the 1,115-byte record. MEASURED + INFERRED ratio.
2. **The expensive check is the one that caught emem's own production bug.** Only the source re-read refuses M15 ("the
   right record, the wrong pixel": a validly signed fact whose DNs came from the pixel 10 m south). Before the fix,
   162 of 200 sampled production records (Wilson 95 % 75 to 86 %) had that defect. The cheapest check (binding, about
   0.01 ms more than the hash) is the one that refuses the other real defect class, a record for another date or cell.
   MEASURED (committed, `prevalence_summary.json`, `mutation_matrix.json`) + MEASURED (timings) + INFERRED mapping.
3. **One reference costs 46 LLM tokens; the 16-digit value it names costs 8** (cl100k; o200k 45 vs 8). Over all 205 scalar
   facts at the Keylong cell the token is 48 tokens (median, IQR 47 to 50) against 8 for the value: **6.4x** (ratio of
   means). Against a 3-decimal value it is 15x. emem's docs say 9.5x on a different sample (values averaging 5.4
   tokens). A bundle token is 38 characters and 21 to 23 tokens for up to 256 facts. MEASURED; docs figure SPEC.
4. **The token is not the main LLM cost; the extra turn and the tool list are.** In the committed two-LLM run (Claude
   Haiku 4.5 receiver, emem's 18-tool plugin loaded in both arms), resolving the token instead of reading the prose cost
   **2.1x the input tokens (45,568 vs 21,665), 1.86x the USD ($0.0158 vs $0.0085) and +1.75 s** per trial (n = 10 each),
   and it bought **no decision accuracy** there (10/10 vs 10/10, because the prose kept 16 digits). It did buy 5/5
   refusals of a forged token, and the rounded-prose arm got 0/5 decisions right. The 18-tool MCP `tools/list` itself is
   **18,709 cl100k tokens** (77,014 chars); all 114 tools are 81,754. MEASURED (committed) + MEASURED.
5. **A full 15-link trace, read-only, takes 14.9 s and pulls 3.26 MB** (n = 5, IQR 14.5 to 15.0 s, one 27.8 s outlier from
   a single 14.3 s tile read). 60 % of the bytes (1.97 MB) and a third of the time (4.9 s) go to *finding* the log
   entry, because emem has no `fact_cid -> leaf_index` index (SPEC: `docs/protocol.md:1462-1463`, "the next increment").
   The 4.8 to 4.9 KB offline proof bundle replaces that step and verifies in **0.57 ms**. MEASURED.
6. **Integrity did not depend on the transport.** Every fact fetched through a TLS-intercepting proxy we do not control
   re-hashed to its CID: 50/50 + 30/30 for the two hero facts, 207/207 for the whole Keylong cell. The Sentinel-2 tiles
   re-read on 1 Oct hash to the same BLAKE3 as on 30 Sep (30/30 per band), and the decoded DN is the signed 3502. MEASURED.
7. **Storage: about 1.1 KB per fact record, about 1.1 KB per log entry, about 1.2 KB per receipt.** Median fact CBOR
   1,141 B over 207 facts (IQR 787 to 1,141; an 8,246 B embedding vector is the maximum); median log entry 1,102 B over
   1,024 entries at four positions; committed receipts 1,007 to 1,395 B re-encoded as CBOR (1,592 to 1,995 B as served JSON),
   plus about 55 B per extra CID. A float64 value is 8 B: the record is about 140x the value it carries. MEASURED + INFERRED.
8. **The board's "1.2 ms" is a host-dependent number and "under 2 ms" excludes the network.** The committed 1.187 ms
   (`mutation_matrix.json:20`) is one batch of 200 on another machine; here the same code path is 0.36 ms. Neither
   includes a network re-read; the hostile review's question 13 (`hostile_review_v12.md:158`) is answered by finding 1.
9. **One avoidable network cost:** every `/v1/facts` response carries **6,762 B of headers, 5,407 B of them a
   Content-Security-Policy** (an HTML policy, on a CBOR body of 1,115 B). Headers are 6.1x the body. MEASURED.

---

## 1. The cost table (what the poster can print, with n, median, IQR)

Times are wall-clock; "warm" means a reused HTTPS connection; all network rows go through the egress proxy described
above. IQR = Q1 to Q3 (inclusive quartiles).

| # | operation | n | median | IQR | unit | label |
|---|---|---|---|---|---|---|
| **Verify offline (CPU)** | | | | | | |
| 1 | BLAKE3 of the 1,115 B record (re-hash to CID) | 30 batches x 2,000 | 1.57 | 1.57 to 1.58 | µs | MEASURED |
| 2 | CBOR decode of the record (cbor2) | 30 x 2,000 | 7.8 | 7.6 to 8.1 | µs | MEASURED |
| 3 | one Ed25519 verify (pynacl) | 30 x 500 | 67.7 | 66.2 to 69.3 | µs | MEASURED |
| 4 | 20-hash Merkle inclusion fold | 30 x 1,000 | 14.4 | 13.9 to 15.1 | µs | MEASURED |
| 5 | all offline checks, one decision (mutation suite level I: hash, binding, signature, log, recompute, cached pixel) | 30 x 200 | 0.357 | 0.353 to 0.374 | ms | MEASURED |
| 6 | `verify_bundle.py`, 9 checks, in-process (precompiled) | 300 | 0.571 | 0.546 to 0.613 | ms | MEASURED |
| 7 | `verify_bundle.py` as a fresh process, no network namespace (`unshare -rn`) | 50 | 48.2 | 46.6 to 50.4 | ms | MEASURED |
| 7a | of which: Python start + imports alone | 50 | 44.4 | 42.2 to 46.8 | ms | MEASURED |
| **Resolve over HTTPS** | | | | | | |
| 8 | `GET /v1/facts/<cid>` CBOR, new connection | 50 | 154.2 | 150.9 to 166.8 | ms | MEASURED |
| 8a | of which: connect + TLS (to the proxy) | 50 | 101.9 | | ms | MEASURED |
| 9 | same, reused connection | 49 | 40.0 | 38.6 to 43.4 | ms | MEASURED |
| 10 | same, JSON form, new connection | 30 | 152.5 | 147.8 to 158.8 | ms | MEASURED |
| 11 | bytes per resolve: body / headers / request | 50 | 1,115 / 6,762 / 145 | fixed | B | MEASURED |
| **Re-read the source (Keylong pixel, Planetary Computer, Azure blob)** | | | | | | |
| 12 | SAS token GET | 30 | 724 | 691 to 805 | ms | MEASURED |
| 13 | B08 COG header, 64 KiB range | 30 | 943 | 906 to 990 | ms | MEASURED |
| 14 | B08 tile #413, 477,314 B range | 30 | 1,028 | 1,005 to 1,111 | ms | MEASURED |
| 15 | B04 tile #413, 468,566 B range | 30 | 1,235 | 1,195 to 1,335 | ms | MEASURED |
| 16 | decode tile to the DN (zlib + 15-bit unpack, Python) | 30 | 2.5 | | ms | MEASURED |
| 17 | whole source re-read inside the trace (links 8, 9, 9b; 8 requests) | 5 | 6.9 s; 1,180,728 B | | s; B | MEASURED |
| **Full trace** | | | | | | |
| 18 | 15-link trace, read-only (Keylong NDVI) | 5 | 14.9 | 14.5 to 15.0 (max 27.8) | s | MEASURED |
| 18a | requests / bytes in per trace | 5 | 44 / 3.26 MB | 42 to 44 / 3,258,676 to 3,269,942 B | | MEASURED |
| 18b | of which: locating the log entry (link 12, 23 requests) | 5 | 4.9 s; 1.97 MB | 4.8 to 5.0 s | | MEASURED |
| **LLM tokens (cl100k_base; o200k_base in brackets)** | | | | | | |
| 19 | one `emem:fact:` token (84 chars) | 1 | 46 (45) | | tokens | MEASURED |
| 20 | fact tokens at the Keylong cell | 205 | 48 (48) | 47 to 50 | tokens | MEASURED |
| 21 | the values they name (shortest repr) | 205 | 8 (8) | 8 to 8 | tokens | MEASURED |
| 22 | one `emem:bundle:` token (38 chars, up to 256 facts) | 5 tokens | 21 (20) | range 21 to 23 | tokens | MEASURED |
| 23 | a one-sentence prose handoff (constructed) / with the token appended | 1 | 62 / 108 | | tokens | MEASURED |
| 24 | real agent prose handoffs (Sonnet 5.5) | 10 | mean 64.9 | | tokens | MEASURED (committed) |
| 25 | the fact as JSON (`GET /v1/facts` JSON) | 1 | 562 (565) | | tokens | MEASURED |
| 26 | MCP `tools/list`, 18-tool core / all 114 tools | 1 | 18,709 / 81,754 | | tokens | MEASURED |
| **Agent-level (committed run, Haiku 4.5 receiver, 18-tool plugin in both arms)** | | | | | | |
| 27 | input tokens per trial: resolve the token / read the prose | 10 / 10 | mean 45,568 / 21,665 | not committed | tokens | MEASURED (committed) |
| 28 | USD per trial: token / prose | 10 / 10 | mean 0.0158 / 0.0085 | not committed | USD | MEASURED (committed) |
| 29 | wall per trial: token / prose | 10 / 10 | mean 8.85 / 7.10 | not committed | s | MEASURED (committed) |
| **Storage** | | | | | | |
| 30 | fact record (canonical CBOR), all facts at Keylong | 207 | 1,141 | 787 to 1,141 (max 8,246) | B | MEASURED |
| 31 | transparency-log entry (CBOR), 4 positions x 256 | 1,024 | 1,102 | 1,033 to 1,239 (max 35,111) | B | MEASURED |
| 32 | signed receipt, 2 to 8 CIDs (CBOR re-encoded / JSON as served) | 5 | 1,217 / 1,806 | 1,161 to 1,329 / 1,750 to 1,914 | B | MEASURED |
| 33 | offline proof bundle (fact + attestation + STH + witness + proofs + tile refs) | 2 | 4,906 (30 Sep) / 4,770 (1 Oct) | | B | MEASURED |
| 34 | inclusion proof (20 hashes) binary / JSON | 1 | 640 / 2,399 | | B | MEASURED |

Not printed with an IQR: rows 27 to 29 (only means were committed); rows 17, 18b (sums of per-link medians, n = 5).

---

## 2. What each check buys, and what it costs

The ladder rows follow MASTER §11. "Catches" lists the R1 mutations (`research/repro/v11/out/summary.md`, 16 in scope)
that the check is the first to refuse, plus the real defects behind them. Times are from table row 5's per-level
breakdown (marginal cost of adding the level; MEASURED, `cost_measurements.json` `m2...by_level`).

| ladder layer | check | first refuses (R1) | real case it maps to | added CPU per decision | network to run it from a token | label |
|---|---|---|---|---|---|---|
| L0 byte integrity | resolve by CID, re-hash | M1, M2, M7 (by resolving); M3 (1 ULP inside the bytes) | paraphrase and rounding drift (F6 in 05_failure_modes) | 0.02 ms (C); +0.0002 ms (D) | 1 GET: 40 ms warm, 154 ms cold; 1,115 B | MEASURED |
| L1 observation identity | cell, band, date inside the hashed bytes equal the question | M4, M5, M6 | asked 23 Sep, served 25 Sep (`results.md` rawband; token string carries tslot 20721 vs 20719 asked; open in emem's code per 05 F3) | +0.010 ms | none | MEASURED; mapping INFERRED |
| cryptographic trust | attestation signature under the pinned key | M8 to M13 | forged or re-encoded records | +0.18 ms | attestation entry (1,604 B): 4.9 s and 1.97 MB to locate online, or 0 with the offline bundle | MEASURED |
| cryptographic trust | log inclusion and consistency | M16 (a second signed version shown only to B) | split view | +0.11 ms | 0.18 s + 1.35 s, about 96 KB (links 13, 14) | MEASURED |
| L2 derivation | recompute NDVI from the signed DNs | M14 | signer arithmetic error | below noise (H minus G: -0.004 ms) | none | MEASURED |
| L3 source re-read | DNs equal the COG pixel at the cell | **M15, the right record, the wrong pixel** | **162/200 pre-fix production records** (`prevalence_summary.json`); fixed 2026-09-28 (`PIXEL_FIX_AT`, trace link 9) | +0.005 ms with the window cached; 2.5 ms to decode a fetched tile | **6.9 s, 1.18 MB, 8 requests cold** (0.058 % of the 2.02 GB scene) | MEASURED |
| L4 entity | none | M17 (same record, another physical entity) | `emem_ask` picks the wrong entity (P0-5, "open" per `should_do/05_EVIDENCE_AND_NUMBERS.md:127`; status today UNVERIFIED) | no check exists at any cost | | MEASURED (committed) |
| L5 physical truth / decision | none | | sensor and product accuracy | no check exists at any cost | | |

Reading of the table (INFERRED):

- The whole cryptographic and derivation ladder (L0 to L2 plus signature and log) costs 0.36 ms of CPU and 4.8 KB of
  evidence when the evidence travels with the reference. The price of L3 is about four orders of magnitude higher in
  time and three in bytes, and it is the only layer that catches a signer that faithfully signed a wrong pixel.
- emem's own two shipped defects sit at the two ends of this cost axis: the date substitution at the cheapest check
  (binding, about 0.01 ms; open in code per 05 F3), the wrong-pixel reader at the most expensive one (source re-read).
  An agent system that hands over values without a reference cannot run either check, so the same defect classes in
  any multi-agent EO pipeline pass silently. This is the "why EMEM" the user asked for, stated in cost terms.
- A receiver can choose depth by stakes: L0 to L2 always (sub-millisecond), L3 when the decision is near a threshold.
  In R1 the M15 value 0.3016 against the genuine 0.4709 flips the 0.4705 rule (`summary.md`), so L3 paid for itself
  in the one case it exists for.

### What the reference bought in the agent-level run, and what it cost (MEASURED (committed), `results.json:203-287`)

| receiver arm (Haiku 4.5, n) | decisions correct | refused | input tokens (mean) | USD (mean) | wall s (mean) |
|---|---|---|---|---|---|
| T, gets the token, resolves it (10) | 10/10 | 0 | 45,568 | 0.01577 | 8.85 |
| P, gets A's prose, 16 digits (10) | 10/10 | 0 | 21,665 | 0.00849 | 7.10 |
| R, gets rounded prose "0.47" (5) | 0/5 | 0 | 21,658 | 0.00861 | 6.96 |
| F, gets a forged token, real CID wrong cell (5) | n/a | 5/5 DECLINE | 43,964 | 0.01271 | 8.49 |

Honest reading: with faithful 16-digit prose, the reference added cost (+86 % USD, +1.75 s, +23,903 input tokens, i.e.
one more model call carrying the same about 21.7 k context plus the resolved record; INFERRED from the token counts) and
bought nothing in accuracy (Fisher one-sided p = 1.0, `results.json`). It bought refusal of a forged reference (5/5) and
immunity to rounding, which cost the prose receiver every decision (0/5). The threshold 0.4705 is constructed
(`prereg.md`, "The poster must say that the threshold is constructed").

For scale (MEASURED (committed)): agent A (Sonnet 5.5) spent $0.105 mean, 13.3 s and 3.3 tool calls to find the value in
the first place (`results.json:14-17`); the pre-registered raw-band run spent $2.12 for 10 runs (median 31.6 s, 4 to 15
tool calls; `data/v9/rawband/results.md:16`). Different models, so not a like-for-like ratio with the receiver.

---

## 3. Measurements, method and caveats

### M1. Resolve one fact over HTTPS (`GET /v1/facts/<cid>`)

Method: curl `-w` timing, one process per request for "cold" (new TCP + CONNECT + TLS), one process with 50 URLs for
"warm" (first transfer dropped). Accept `application/cbor`; every CBOR body re-hashed with blake3 and compared with the
CID. 2026-10-01 00:37:06Z to 00:37:55Z.

- Keylong NDVI `oj5ceccile62...` (1,115 B): cold 154.2 ms (IQR 150.9 to 166.8, n = 50, 50/50 HTTP 200, 50/50 re-hash OK);
  warm 40.0 ms (38.6 to 43.4, n = 49). Request-to-first-byte inside an open connection (ttfb minus pretransfer) 50.0 ms
  cold. MEASURED.
- JSON form 1,273 B (696 B gzip): 152.5 ms cold (n = 30). MEASURED.
- Bengaluru elevation `yqbolgeo...` (509 B): 154.5 ms cold (148.9 to 159.1, n = 30, 30/30 re-hash OK). Latency does not
  depend on record size at this scale. MEASURED.
- Headers: 6,762 B from emem plus 39 B proxy CONNECT line; `content-security-policy` alone 5,407 B. `cache-control:
  public, max-age=31536000, immutable`, `etag` = the CID. LIVE.
- Comparison (SPEC, `docs/benchmarks.md:163-169`, loopback on the server, 2026-07-11, pre-redb): token dereference p50
  1.2 ms; receipt verification offline p50 0.13 ms; warm recall p50 2.5 ms; 632 req/s. The 40 ms here is network and
  proxy, not server time. Committed cross-runtime table (n = 3 each, 2026-09-30; `crossruntime_table.json:31-342`):
  REST 223.5 ms, MCP 223.7 ms, A2A 226.3 ms, official MCP Python SDK 56.3 ms, LangChain MCP adapters 1,176.8 ms, MCP
  handshake 672.3 ms (these include a signing POST). MEASURED (committed).

### M2. Offline verification (`research/repro/v8/verify_bundle.py` on `proof_bundle_ndvi.cbor`)

Method: (a) 50 fresh processes under `unshare -rn` (no network; verified "Network is unreachable"); (b) 50 processes
that only start Python and import blake3/cbor2/nacl; (c) 300 in-process `runpy` runs, stdout captured; (d) 300 runs of
the precompiled script; (e) primitives with batched `perf_counter`; (f) `mutation_suite.decide(level, genuine())`
imported from the repo with `PYTHONDONTWRITEBYTECODE=1` (no file written; `git status` unchanged), 30 batches of 200 per
level, the same loop shape as the committed `meta.full_verification_ms` (`mutation_suite.py:484-487`).

- Process: 48.2 ms (46.6 to 50.4), 50/50 exit 0, 9/9 PASS; baseline 44.4 ms. Verification adds about 4 ms to a cold
  process, most of it compiling the script (1.53 ms) and reading the bundle. MEASURED + INFERRED.
- In-process: 0.571 ms precompiled (0.546 to 0.613, n = 300); 2.37 ms via runpy (includes compile). MEASURED.
- The 9 checks include three Ed25519 verifies (attestation, STH, witness) at 0.068 ms each, which is about 0.2 ms of
  the 0.57 ms. INFERRED.
- Per level, ms per decision (median, n = 30 batches; each includes building the handoff, 0.029 ms): A 0.028, B 0.028,
  C 0.048, D 0.048, E 0.058, F 0.242, G 0.356, H 0.351, I 0.357. MEASURED.
- Committed 1.187 ms (`research/repro/v11/out/mutation_matrix.json:20`, `summary.md:4`, `CLAIMS_MAP.md:42`) was one
  batch of 200 on another host; `15_V11_CLAIMS_MAP.md:112` records "1.2 to 1.5 ms across runs, Python, one laptop core".
  Same code, 3.3x faster here. Print "under 1.5 ms" or "about 1 ms", not a 4-digit figure. INFERRED.

### M3. The 15-link trace, read-only

`research/repro/v8/trace_fact.py` as committed sends four signing POSTs (link 4 wrong-cell resolve, link 9c
`/v1/range_hash`, link 10 `/v1/recall` and `/v1/memory_token/resolve`). It was therefore **not run as is**. A
scratchpad copy (`make_trace_ro.py` builds `trace_ro.py` by asserted string replacement; the repo file is only read)
refuses any POST to emem.dev, keeps link 4's offline equality, skips 9c, replaces link 10 with an offline signature check
of the committed Keylong recall receipt (`data/v11/cell_keylong.json`; valid) and marks link 11 not run; link 12 uses the
v1 single-fact batch rule found on 30 Sep. It logs every HTTP request (host, bytes, ms, link) and per-link wall time.
Outputs went to the scratchpad (`--out=`), never to `research/repro/v8/`.

Keylong NDVI, n = 5 (00:40Z to 00:46Z): wall 14.9 s median (14.03, 14.51, 14.91, 15.03, 27.79). Run 5's outlier is one
B08 tile range read that took 14.3 s. 15 of 16 links VERIFIED in every run, link 11 NOT VERIFIABLE (not run). MEASURED.

| link | what | median ms (min to max) | bytes in | requests |
|---|---|---|---|---|
| 2 | resolve the record | 177 (174 to 396) | 1,115 | 1 |
| 1, 3 to 7, 10, 11 | token parse, re-hash, binding, cell geometry, provenance, NDVI recompute, receipt check | 45 total | 0 | 0 |
| 8 | STAC item (Planetary Computer) | 558 (480 to 688) | 15,295 | 1 |
| 9 | SAS token, B08 + B04 headers and tiles, decode | 4,861 (4,383 to 17,758) | 1,077,352 | 5 |
| 9b | SCL header and tile | 1,526 (1,461 to 1,594) | 88,081 | 2 |
| 12 | locate the attestation (21 bisection probes + one 256-entry page) | 4,880 (4,781 to 4,999) | 1,971,838 to 1,979,687 | 23 |
| 13 | inclusion under the signed head | 177 (163 to 195) | 2,399 to 2,488 | 1 |
| 14 | consistency with a pinned head and the witness head, witness key | 1,348 (1,234 to 1,548) | 93,461 to 96,921 | 4 to 6 |
| 15 | key to domain (did.json, JWKS, emem.json, two DoH TXT) | 1,026 (960 to 1,425) | about 9,100 | 5 |

- Azure blob bytes were exactly **1,165,033 B in every run**, the committed number (`cog_pixel_bytes.json:223`),
  0.0576 % of the 2,023,818,762 B scene (`scene_sizes.json:162`). MEASURED + MEASURED (committed).
- Bytes by host per run: emem.dev about 2.08 MB (31 to 33 requests), blob 1.165 MB (6), PC API 15.7 KB (2), geo.qa 620 B,
  DoH about 560 B. MEASURED.
- The bundle the trace writes is 4,770 B today against 4,906 B committed (`trace_fact_output.txt:155`): the witness
  consistency proof is 17 hashes instead of 21 (4 x 32 B + CBOR framing = 136 B). MEASURED.
- Committed full trace with the POSTs: 17.9 s (`trace_fact_output.txt:191`, 2026-09-30). Not comparable one-to-one
  (four fewer round trips today). MEASURED (committed).
- Bengaluru elevation (`yqbolgeo...`), n = 3: 7.06 s (7.00 to 7.77), 34 requests, 1.66 MB, of which link 12 is 1.56 MB
  and 4.6 s. Its source is the Open-Meteo elevation API (`open_meteo_copdem90m@1`), for which `trace_fact.py` has no
  re-read rule (link 6 NOT VERIFIABLE). Link 12 reported FAILED only because this harness assumed the v1 batch rule and
  the May entry is preimage v0; the entry hash, the fact bytes inside it, the recomputed batch root and the v0
  attestation signature all passed. A harness limitation, not an emem defect. MEASURED.
- Log growth: tree size 2,556,451 at 2026-09-30T09:15:54Z (`trace_fact_output.txt:146`), 2,574,692 at
  2026-10-01T00:48:00Z: 18,241 entries in 15.5 h, about 1,170 per hour. MEASURED + INFERRED rate.
- On 1 Oct the witness reported `head_is_independently_witnessed=True`, 0 entries behind (30 Sep: False, 943 behind);
  the only witness domain is still geo.qa, operated by Vortx AI. LIVE.

### M4. Source re-read for the Keylong pixel

Method: curl range GETs against the two COGs named inside the fact (`sources[0].id`), n = 30 each, 00:43Z to 00:45Z,
SAS token fetched per iteration. Every tile body hashed with blake3 and compared with `upstream[].tile_blake3` in the
committed bundle; the B08 DN at (col 9098, row 9443) decoded from the fetched tile.

- SAS 724 ms (400 to 404 B); B08 header 943 ms (65,536 B); B08 tile 1,028 ms (477,314 B, about 0.46 MB/s); B04 tile
  1,235 ms (468,566 B, about 0.38 MB/s). 0 failures in the retained run. MEASURED.
- Tile BLAKE3 on 1 Oct equal to 30 Sep for both bands (B08 `xyzcrqucmzeo...`, B04 `nw5nehrmxu55...`, 30/30 each);
  decoded DN 3502 = signed DN 3502. The re-read is reproducible across days. Note: the fact itself does not commit to the
  COG bytes (`trace_fact_output.txt`, link 9c "the NDVI fact does not commit to the COG bytes it read"); the tile hash is
  the verifier's own record. MEASURED.
- Decode cost after fetch: 2.5 ms (n = 30). MEASURED.
- First attempt aborted: one blob connection was closed mid-exchange by the proxy (`ws_closed_mid_exchange`), curl
  reported code 000 and the harness stopped; the rerun from scratch is the one reported. Availability of the source is a
  real cost of L3. MEASURED.
- Throughput of 0.4 to 0.5 MB/s says the path, not the COG, sets the cost; in-region reads would be faster. UNVERIFIED.
- API-sourced fact (Bengaluru): Open-Meteo `elevation` GET, 9/10 OK, 198.5 ms median (181.6 to 283.8), 21 B, returns
  918.0 = the signed value; one TLS failure (30.4 s). Cheap, but the API serves no version or checksum, so agreement
  today does not identify the bytes the signer read. MEASURED + INFERRED.

### M5. Token overhead

Method: tiktoken 0.14.0 `cl100k_base` and `o200k_base` (OpenAI BPEs). No Anthropic, Google or open-model tokenizer was
available offline; Claude token counts are not measured here.

| item | chars | cl100k | o200k |
|---|---|---|---|
| `emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62...` | 84 | 46 | 45 |
| `emem:bundle:` tokens (5 real tokens) | 38 | 21 to 23 | 18 to 23 |
| value, 16 digits `0.4708994708994709` | 18 | 8 | 8 |
| value, 4 dp / 3 dp / 2 dp | 6 / 5 / 4 | 4 / 3 / 3 | 4 / 3 / 3 |
| prose sentence (constructed: place, coordinates, 16-digit value, satellite, date, tile) | 159 | 62 | 63 |
| the same sentence + the fact token | 244 | 108 | 108 |
| fact JSON as served | 1,271 | 562 | 565 |
| fact CBOR as base64 | 1,488 | 1,081 | 1,009 |
| proof bundle 4,906 B as base64 | 6,544 | 4,746 | 4,491 |
| bundle resolve JSON (8 citations + receipt) | 4,930 | 2,446 | 2,414 |
| 15-link trace stdout | 12,148 | 3,931 | 3,908 |
| agent card JSON | 15,165 | 3,780 | 3,796 |
| `/v1/verifier_spec` JSON | 29,969 | 8,454 | 8,512 |
| MCP `tools/list`, 18-tool core response | 77,014 | 18,709 | 19,125 |
| MCP `tools/list`, all 114 tools (8 pages) | 331,302 | 81,754 | 83,655 |

All MEASURED. Ratios (INFERRED): token / 16-digit value 5.75x; / 4 dp 11.5x; / 3 dp 15.3x; bundle / fact token 0.5x;
prose + token / prose 1.74x. Keylong sample (205 scalar facts, values as Python's shortest repr): token median 48
(IQR 47 to 50, range 43 to 58), value median 8 (IQR 8 to 8); ratio of means 6.39x (cl100k), 6.25x (o200k); characters
84 vs 17.0 mean, 4.9x.

The three published ratios measure different things and must be labelled when printed:
- 5.75x: one hero token vs its full-precision value (`token_counts.json:14-18`, 46 vs 8). MEASURED.
- 6.4x: 205 Keylong facts, full-precision values. MEASURED today.
- 9.5x: 131 facts at 12 places across 57 bands, values averaging 10.9 chars / 5.4 tokens, 2026-08-11
  (`docs/how-emem-compares.md:127-135`; `paper-section-statistics-and-threats.md:45`). SPEC. emem's README (`README.md:200`)
  says "about 51 LLM tokens" for a token; today's measurements give 43 to 58 (median 48). SPEC vs MEASURED.

The committed counts agree with today's except the 18-tool list, which grew from 18,659 (`token_counts.json:80-84`) to
18,709 cl100k. MEASURED.

### M6. Storage and wire bytes

- Fact records: all 207 facts at the Keylong cell (CIDs from the committed recall receipt), 207/207 re-hash OK, 207/207
  aligned with the committed band and tslot. Median 1,141 B, IQR 787 to 1,141, min 547, max 8,246; scalar facts mean
  982 B (n = 205); vectors 1,097 B and 8,246 B. Sum 210,615 B for the cell. MEASURED.
- Log entries: 1,024 entries at leaves 0, 1,000,000, 2,457,078 and the head minus 256; 1,024/1,024 entry hashes OK.
  949 attestations (median 1,103 B), 75 `emem.memory_write.v1` (median 530 B). Facts per attestation median 1, mean
  1.36, max 42; 1,212 B of log per attested fact. The log entry contains the fact bytes, so the log roughly doubles the
  stored bytes per fact. MEASURED + INFERRED.
- Whole log, INFERRED: 2.57 M entries x 1,102 to 1,561 B (median to mean) = about 2.8 to 4.0 GB of entry CBOR. The four
  sampled positions differ (mean 1,100 B at 1 M, 2,183 B near Keylong), so this is an order of magnitude only.
- The JSON log API inflates entries by about 4 to 7x (256 entries = 0.95 to 1.83 MB of JSON). MEASURED.
- Receipts (committed files, preimage v2): 2 to 8 CIDs, 1,592 to 1,995 B JSON as served (byte fields duplicated as int
  arrays and base32 twins), 1,007 to 1,395 B re-encoded as CBOR without the twins; the 207-CID recall receipt is 12,873 B
  (about 55 B per additional CID). MEASURED; the CBOR re-encoding is ours, not emem's wire format (INFERRED).
- Proofs: inclusion 20 hashes = 640 B (2,399 B JSON); consistency from 2,556,451 to the head 20 hashes = 640 B; STH
  678 B JSON. MEASURED.
- Ratio, INFERRED: record 1,115 B vs an 8 B float64 = 139x; + its log entry 1,604 B = about 340x. What the bytes carry:
  cell, band, tslot, value, confidence, source URLs, scene id, DNs, offset, cloud cover, catalogue, signer, schema.
- emem's own statement (SPEC, `docs/benchmarks.md:171-172`): "storage bytes per fact under compaction" is not yet
  measured. Server-side index and receipt storage are not visible from outside and were not measured here.

---

## 4. Every committed cost number found in the repo

Search: `grep` over `research/`, `poster/README.md`, `AGENTS.md` for ms, bytes, tokens, latency, cl100k, wall_s,
cost_usd and the listed literals. Status: CONSISTENT (re-measured equal or within noise), SUPERSEDED (re-measured
different), CONFLICT (two committed numbers disagree), SPEC (docs).

| number | where (file:line) | context | status today |
|---|---|---|---|
| 1.187 ms one full verification | `repro/v11/out/mutation_matrix.json:20`; `summary.md:4`; `repro/v12/CLAIMS_MAP.md:42`; `should_do/19_V12_CLAIMS_MAP.md:42` | level I, 200 reps, source window cached | SUPERSEDED: 0.357 ms here (host-dependent) |
| 1.2 to 1.5 ms; 1.23 ms; "about 1.5 ms" | `should_do/15_V11_CLAIMS_MAP.md:112`; `17_V11_RESPONSE_TO_FIELD_MAP.md:34` | earlier runs | same quantity, other host |
| 1.182 / 1.207 ms, "under 2 ms" | `repro/v12/audit/hostile_review_v12.md:158`; `section_audit_v11_2.md:307` | asks whether the COG re-read is included | answered: excluded; re-read cold is about 6.9 s |
| 0.0528 s whole suite | `mutation_matrix.json:19` | 17 mutations x 9 levels | not re-run (would rewrite `out/`) |
| 17.9 s, 15 links, 17 checks | `repro/v8/trace_fact_output.txt:191`; `audit_v11/poster_evidence_audit.md:55` | full trace with POSTs, 30 Sep | read-only trace 14.9 s (n = 5) |
| 1,115 B fact CBOR | `trace_fact_output.txt:14`; `token_counts.json:116`; `crossruntime_table.json` | Keylong NDVI | CONSISTENT |
| 4,906 B offline bundle | `trace_fact_output.txt:155`; `poster_evidence_audit.md:62` | 9 checks offline | CONSISTENT as a file; rebuilt today 4,770 B |
| 1,604 B log entry | `trace_fact_output.txt:132` | the fact's attestation | CONSISTENT |
| 1,165,033 B of 2,023,818,762 B (0.058 %) | `data/v8/cog_pixel_bytes.json:221-226`; `scene_sizes.json:162`; `poster_evidence_audit.md:45` | cold source read | CONSISTENT (5/5 runs) |
| 15,295 B STAC item | `scene_sizes.json:4` | | CONSISTENT |
| 84 chars, 46 cl100k / 45 o200k | `token_counts.json:14-18`; `results.json:82` | fact token | CONSISTENT |
| 38 chars, 22 cl100k (5-fact bundle) | `token_counts.json:38-42` | bundle token | CONSISTENT (21 to 23 over 5 tokens) |
| 562 cl100k fact JSON; 3,064 REST recall; 1,587 MCP recall text; 18,659 tools/list | `token_counts.json` | | 562 CONSISTENT; tools/list now 18,709 |
| 9.5x, 51 tokens, 5.4 per value | `audit_v11/emem_capability_index.md:799`; `should_do/05_EVIDENCE_AND_NUMBERS.md:108`; emem `how-emem-compares.md:117-135` | docs sample | SPEC; CONFLICT with 5.75x flagged in `poster_evidence_audit.md:108` |
| 5.75x (15x vs 3 dp) | `poster_evidence_audit.md:21,108` | board's own measure | CONSISTENT; 6.4x on 205 facts |
| 64.9 cl100k prose mean | `results.json:83` | 10 real handoffs | not re-run |
| $0.1049 mean, 13.28 s (11.61 to 17.27), 3.3 tool calls | `results.json:14-17`; `poster_evidence_audit.md:79` | agent A | not re-run |
| Haiku T/P/R/F cost, wall, input tokens | `results.json:203-287` | receiver arms | not re-run (section 2) |
| $2.12, $0.11 to 0.52/run, 31.6 s median | `data/v9/rawband/results.md:16` | raw-band run | not re-run |
| 207 to 1,177 ms per runtime; 672 ms MCP handshake | `crossruntime_table.json:31-392` | n = 3, with signing POSTs | not re-run (POSTs) |
| 0.13 ms receipt verify, 1.2 ms dereference, 2.5 ms recall, 632 req/s | `should_do/05_EVIDENCE_AND_NUMBERS.md:85-92`; emem `docs/benchmarks.md:163-169` | loopback, 2026-07-11, pre-redb | SPEC |
| 69 to 1,255 ms individual vs 20 to 54 ms bundle | emem `how-emem-compares.md:120` | wall clock | SPEC |
| 0.0669 ms per fact, 0.167 % of a 40 ms frame, 399/399 | `should_do/05_EVIDENCE_AND_NUMBERS.md:97`; emem `docs/roadmap.md:95-96` | edge signing on a third-party detector | SPEC |
| 75 KB core tools, 324 KB all, 13 KB `emem_tools` | emem `README.md:200`; `audit_v11/emem_capability_index.md:669` | MCP context | SPEC; measured 77,014 and 331,302 chars |
| 64 / 290 KB vs 75 / 324 KB | `do_not_use/04_REFUTED_UNMEASURED_AND_ROADMAP.md:54` | `server.json` vs README | CONFLICT (docs vs docs) |
| about 24 KB MCP result cap | `should_do/18_V11_PROCESS_AND_HANDOFF.md:54` | | UNVERIFIED |
| receipt `cost.latency_p50_ms 1, p99 2000` | `data/v11/cell_keylong.json` receipt | server self-report, semantics not documented here | SPEC |
| "about 946 KB for the two 10 m COG tiles" | `research/v13/02_experiment_design.md:313` | S9 plan | CONSISTENT: 945,880 B tiles; 1,165,033 B with headers and SCL |

---

## 5. What is not measured (state it on the board or behind the QR)

1. Claude (Anthropic) token counts: only OpenAI BPEs (cl100k, o200k) were available. A count through Anthropic's
   token-counting API was not possible here.
2. Network cost without this TLS-re-terminating proxy, from other regions, over HTTP/2, or in the same cloud region as
   the COGs.
3. The four signing calls of the original trace (links 4, 9c, 10, 11) today: not run because they sign and store.
4. Bundle resolve latency (`GET /v1/memory_bundle/<token>` fetched once: 4,930 B, 8 citations); MCP handshake today.
5. Server-side storage per fact including redb indexes, receipt persistence, compaction, deduplication (emem lists these as
   open, `benchmarks.md:171-172`).
6. Throughput under concurrency; verification of many facts at once (for example the 780 facts of v12) as a timed batch.
7. Source re-read cost for other products: Copernicus DEM COG on AWS, Sentinel-1, ERA5, the embeddings (vector facts).
   Only Sentinel-2 L2A (COG) and Open-Meteo (API) were measured.
8. Agent-level overhead beyond one model (Haiku 4.5) and one prompt; the Qwen receiver arms in v8 have no data
   (`results.json` "qwen2.5-3b-instruct-q4_k_m": arms empty); cache-read vs uncached split per trial; per-trial spread
   (only means were committed).
9. The cost of *not* checking (a wrong irrigation or EUDR decision) in any unit; energy and hosting cost.
10. Re-read cost when the source is gone or changed: the 30 Sep and 1 Oct tiles were identical; no case of a changed
    upstream object was observed or timed.

---

## 6. For the poster

### Lines that are true and fit (each MEASURED on 2026-10-01 unless labelled)

- "Checking a handed-over record: under 1 ms of CPU. Re-reading its Sentinel-2 pixel: 1.2 MB and about 7 s."
- "The expensive check is the one that caught our own wrong-pixel bug."
- "One reference: 46 LLM tokens. The 16-digit value it names: 8. A bundle of up to 256: 21 to 23."
- "Resolving instead of trusting prose: 2.1x the input tokens, +1.75 s, same accuracy when the prose is faithful,
  5/5 forgeries refused." MEASURED (committed), Haiku 4.5, n = 10/10/5.
- "4.8 KB of evidence lets a receiver check signature and log offline in 0.6 ms."
- "Every record re-hashed to its address after passing through a proxy we do not control (287/287)." (50 + 30 + 207)

Avoid: "tokens save context" (refuted by emem's own docs and by row 19 to 21); "1.187 ms" as a universal figure;
"9.5x" without its sample; "verification in under 2 ms" without "offline, source cached".

### Figure: the cost ladder (data ready in `cost_measurements.json`)

A horizontal log-scale strip, one row per ladder layer (L0, L1, signature, log, L2, L3, L4/L5), x = time per check from
1 µs to 10 s (about 7 decades), marker area = bytes that must move (0 B, 1.1 KB, 4.8 KB, 1.18 MB), right-hand label = what
the row refuses (M-ids and the real case). Data points: hash 1.6 µs / 1,115 B (resolve 40 to 154 ms); binding +0.01 ms /
0 B; signature +0.18 ms / 1,604 B entry (online locate 4.9 s / 1.97 MB, drawn as a ghost bar); log +0.11 ms / 640 B
proof; recompute about 0 / 0 B; source re-read 6.9 s / 1.18 MB (2.5 ms once fetched, drawn as a second tick); L4/L5
"no check exists". The visual point: the top five rows sit within one millimetre of each other at A0 scale; the source
row sits four decades to the right; M15's 162/200 sits on that row.

A second, small panel: token budget bars (cl100k) for value 8, fact token 46, bundle 21 to 23, prose 62, prose + token
108, fact JSON 562, MCP core tool list 18,709 (broken axis), so the viewer sees that the reference is not where the LLM
tokens go.

---

## 7. Reproduction

Scripts (scratchpad of this session, not committed): `m1_resolve.py`, `m2_offline.py`, `make_trace_ro.py` (builds
`trace_ro.py` from `research/repro/v8/trace_fact.py` by asserted replacements), `m4_source.py`, `m5_tokens.py`,
`m6_storage.py`. Each writes JSON; `research/v13/cost_measurements.json` is their merged output (raw per-request times,
per-fact sizes, per-entry sizes, per-link times and bytes per trace run). External URLs used, all retrieved 2026-10-01:
https://emem.dev/v1/facts/oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa ,
https://emem.dev/v1/log/entries , https://emem.dev/mcp , https://emem.dev/mcp/full ,
https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-2-l2a ,
https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-2-l2a/items/S2A_MSIL2A_20260925T054251_R005_T43SFS_20260925T090015 ,
https://sentinel2l2a01.blob.core.windows.net/sentinel2-l2/43/S/FS/2026/09/25/S2A_MSIL2A_20260925T054251_N0513_R005_T43SFS_20260925T090015.SAFE/GRANULE/L2A_T43SFS_A058804_20260925T054245/IMG_DATA/R10m/T43SFS_20260925T054251_B08_10m.tif (and `_B04_10m.tif`),
https://api.open-meteo.com/v1/elevation?latitude=12.971899&longitude=77.593665 .
