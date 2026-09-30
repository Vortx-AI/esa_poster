# Defects and inconsistencies found in the 2026-09-29 audit

These are for the emem maintainers. None goes on the poster as a claim. A visitor may find any of
them, so we should know them first, and ideally fix them before 19 Oct.

| # | area | finding | where |
|---|---|---|---|
| 1 | federation wording | geo.qa is labelled an "independent operator", but it is a second node run by Vortx AI (separate domain and key, same organisation) | `docs/security.md:250`, `/v1/log/witnesses` |
| 2 | bi-temporal | `recall` with `as_of_signed_at` but **no `tslot`** → HTTP 504 after 40 s on a busy cell (280 facts); 4/4 runs | live, `defi.zb493.xuqA.zcb5f` |
| 3 | bi-temporal | there is no test covering the D6 `history_many` path (the mock returns empty history) | `crates/emem-primitives/tests/bi_temporal.rs` |
| 4 | contradictions | severity falls back to `band_range = max(spread, 1.0)` when no registry range exists, so a 2.93 m DEM disagreement scores 1.000; the docstring is also wrong below 1 unit | `memory_contradictions.rs:581-620` |
| 5 | contradictions | 7 identical re-signings count as 7 attestations | live |
| 6 | freshness | the Fast kernel `0.5+0.5cos(2πΔt/5d)` is non-monotonic: 0.0 at 2.5 d, 0.905 at 4.5 d | `lib.rs:80021-80078` |
| 7 | receipts | `was_cached: true` on the call that just materialised the fact | live |
| 8 | absence | D3 still open: upstream-error and "no S2 scene" paths are unsigned | `lib.rs` |
| 9 | absence | `reason_cid` hashes prose, not the upstream response; the struct doc says "CID of evidence" | `fact.rs:186` |
| 10 | memory writes | CAS (`memory_write.v2` with `base`) is required only for delete and rename; create, str_replace and insert accept v1, backed by an in-memory replay set | `memory_acl.rs:163` |
| 11 | namespaces | `/memories/by_attester/<8 base32 chars>` is a 40-bit prefix, and the first writer wins, so it can be squatted | `memory_acl.rs` |
| 12 | derive | the 401 `how_to_sign` text says "mean is excluded"; `GC1_TIER1_PURE_OPS` includes mean | `lib.rs:38795` |
| 13 | guard | a request with `{"text": …}` instead of `texts` returns `allow, citations_found: 0` | live |
| 14 | S2 offset | a 2022-01-27 NDVI fact (Element84 `sentinel-s2-l2a-cogs`, after the PB 04.00 start on 2022-01-25) records no catalogue or offset in its args, and its value matches raw DNs with offset 0. Confirm that the Element84 v0 bucket is harmonised for this scene | fact `2dpnuf4e…`, cell `defi.zb572.xoso.zb1ec` |
| 15 | recall default | `recall` without a date returned the 2022 scene rather than the 2026 one at the same cell | live |
| 16 | registry domain | `agb_ndvi_powerlaw@1` (pan-tropical calibration) applied at about 3,900 m in the Himalaya, with no biome check | live, Rohtang |
| 17 | triple consensus | the registry advertises `/v1/triple_consensus` (404); the 92–95% accuracy figure has no evaluation; the entry calls Tessera 1024-D | `algorithms-v0.json` |
| 18 | field tokens | re-minting a raster or cube gives a new `derivation_cid` for identical pixels (`signed_at` is hashed), so two agents can hold different tokens for the same field | live cube: `l6e2ksxd…` vs `bctf6vw6…` |
| 19 | receipts | the Merkle proof in a recall receipt covers only `fact_cids[0]` | live |
| 20 | preimages | memory-write and entity preimages use `|`-joined strings, not the tagged PreimageV1 the project argues for | `memory_acl.rs`, `entity.rs:251` |
| 21 | entity | "Maasvlakte ramp 7" converges on OSM relation 1411107, which covers all of Maasvlakte (about 12 × 10 km) | live |
| 22 | docs | stale: `federation.md:363` says inclusion ignores `tree_size` (it is honoured now); `emem_tools` prose says "88" tools; the verifier reject count is given as 16 and as 17 | docs |
| 23 | rasterset resolve | `POST /v1/raster_bundle/resolve` returns `verified: true` but **no receipt**, so ememdemo's rasterset check (`receiptOk(j.receipt)`) always fails and a track step citing an `emem:rasterset:` shows as unchecked. The mint call (`POST /v1/raster_bundle`) does return a receipt. Found rehearsing the poster track, 30 Sep 2026. | `emem:rasterset:n3weckag…:vg3ay3pf…` |
| 24 | viewer / docs cid rule | ememdemo llms.txt and spec r1 state the note cid as `base32(blake3(bytes))[0:26]`; the real rule is `base32(blake3(bytes)[:16])`, which differs in the last character for most notes. | llms.txt line 2 |
| 25 | Source.hash | the fact `Source.hash` field (hash of the upstream bytes) is never filled in production (`hash: None` 61 times in emem-api-rest, `hash: Some(` 0 times), so the upstream read rests on the signer unless the pixel is re-read. | crates/emem-api-rest/src/lib.rs |
| 26 | pixel rounding (fixed 28 Sep) | COG point reads before 2.4.x rounded the fractional pixel index, reading the south/east neighbour; 162 of 200 sampled pre-fix Sentinel-2 records carry neighbour DNs. Old records remain as signed. | CHANGELOG.md:68 |
| 27 | band_raster date | `emem_band_raster` with `observed_on` 2026-09-23 (also 09-22, 09-21) at Keylong returned the byte-identical 25 Sep S2A raster with no warning; the 23 Sep S2C scene exists (20 % cloud). 9 of 10 agents in the pre-registered raw-band run never got 23 Sep values. Found 30 Sep 2026. | research/repro/data/v9/rawband/results.md |
| 28 | docs numbers | README and how-emem-compares §5 say "Agreement 27.8% against accuracy 1.4%, Fisher p = 0.035"; the pinned statistics table gives 3/36 agreeing and 0/72 correct, which reproduces p = 0.035; 10/36 vs 1/72 would give p ≈ 5e-5 | docs/how-emem-compares.md:198, README |
| 29 | read side effects | read tools (`band_raster`, `recall`, `backfill`) sign and store new records; concurrent agents then see different fact_cids for the same values, so read-only experiments are not independent | live, 30 Sep |
| 30 | witness wording | README says emem's head is "co-signed by independent witnesses"; `/v1/log/witnesses` lists one independent operator domain, geo.qa (run by Vortx AI), plus 109 key-only (unvouched) keys | README.md, /v1/log/witnesses |
| 31 | entity receipt | `GET /v1/entity/<token>` returns the receipt stored at mint time (preimage v1, July); `/v1/verify_receipt` accepts it, but ememdemo's verifier requires v2, so an entity step in a track never checks | `emem:entity:4itylz3kjtwy3lgr76ku52ffqa` |
