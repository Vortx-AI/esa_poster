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
