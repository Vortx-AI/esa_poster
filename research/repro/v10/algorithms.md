# emem core algorithms: formulas, citations, reproduction status

Source: `Vortx-AI/emem` at `origin/main` = `18adb67895d33c8b64d3b091a90af1f708315123`. Citations are `path:line` at that commit.
"Our script" means `/home/user/esa_poster/research/repro/` (no emem code). "Audit" means a check run while writing this file, 2026-09-30, with stock `blake3`/`cbor2`.
Notation: `H(x)` = BLAKE3-256(x). `b32(x)` = base32, RFC 4648 alphabet, no padding, lowercase. `‖` = byte concatenation. `u32le`, `u64be` = fixed-width integers.

---

## 1. Memory unit, canonical bytes, fact_cid, key, recall

**Fact variants** (CBOR map; first key `kind` ∈ {`primary`,`derivative`,`absence`}, then fields in Rust declaration order; `Option` fields omitted when `None`):

- Primary: `kind, cell, band, tslot, value, unit?, confidence, uncertainty?, sources, derivation{fn_key, args?}, privacy_class, schema_cid, signer, signed_at, served_via?`
- Derivative: `kind, cell, band, tslot_window[2], op, parents, value, confidence, derivation, schema_cid, signer, signed_at`
- Absence: `kind, cell, band, tslot, reason_cid, confidence, sources, schema_cid, signer, signed_at`
- Source: `scheme, id, cid?, hash?, captured_at?, url?`

**Encoding (emem-CBOR, as coded):** `bytes = ciborium::into_writer(fact)`. The rules:
- Struct maps use declaration order. They are NOT sorted by RFC 8949 §4.2.1.
- `BTreeMap` maps use plain string order.
- `Value::Map` keeps insertion order.
- Integers use the shortest form.
- Floats use the shortest lossless width: f16, f32 or f64. `confidence` is an f32 and is written as `fa…`.
- Before signing, `canonical_float(f) = NaN→0x7ff8… (f9 7e00); −0.0→+0.0; else f`. It is applied to `value`, `derivation.args` and `uncertainty.params` only.
- `signer` ([u8;32]) is written as a CBOR array of 32 uints, not as a byte string.

**Identity:** `fact_cid = b32(H(bytes))`, which is 52 characters.

**Key:** `(cell, band, tslot)`, stored as `cell ‖ 0x00 ‖ band ‖ 0x00 ‖ u64be(tslot)`.

**Signature:** a fact carries no signature of its own. The attester signs a batch (see §6 and §8).

**Recall for a key:**
- The canonical index is last-write-wins by write order, not by `signed_at` and not by `tslot`. An exact `(cell, band, tslot)` lookup returns that one current cid.
- `bands` given, no `tslot`, no bound: the call returns every tslot's current cid.
- The REST layer re-materialises when the newest fact per band (max `tslot`, tie → later `signed_at`) is older than one tempo slot, or is a superseded read.

Plain: a fact's name is the hash of its exact CBOR bytes, including `signer` and `signed_at`. So re-signing identical values gives a new cid. The address `(cell, band, tslot)` holds only the latest write.

Citations:
- fact.rs:9-18 (tag), 72-112, 151-175, 178-198, 202-223
- cbor.rs:21-27, 43-53, 58-75
- emem-cache/src/sled_hot.rs:813-820 (`fact_cid_of`), 840-844, 850-858 (key bytes)
- emem-storage/src/lib.rs:1822-1833 (last-write-wins)
- emem-api-rest/src/lib.rs:12592-12628 (newest-per-band), 12698-12707 (`primary_answers_latest`)
- Receipt manifest map order: `/v1/verifier_spec` `receipt.manifest_hex_key_order`

Doc vs code:
- docs/model.md:25 says "ed25519 over blake3 of the canonical CBOR body". The code signs the attestation preimage over a batch Merkle root (attest.rs:105-124).
- "canonical CBOR" is not RFC 8949 deterministic encoding for maps.

Reproduced by our script: **yes**.
- `verify_fact.py`, `v8/trace_fact.py` [3]: the CID re-derives, and a 1-ulp change to the value changes the name.
- Audit: key order `kind, cell, band, tslot, value, confidence, sources, derivation, privacy_class, schema_cid, signer, signed_at`; `confidence` = `fa`, `value` = `fb`; `signer` = `98 20 …`.
- Recall "last-write-wins": **not tested directly**.

## 2. cell64

**Forward** (geo.rs:137-172):
```
lat' = clamp(lat, −90, 90);   lng' = ((lng+180) mod⁺ 360) − 180
lat_q = round((lat'+90)/180 · (2²¹−1))      (21 bits)
lng_q = round((lng'+180)/360 · (2²²−1))     (22 bits);  lng_q = 0 if lng_q = 2²²−1;  lng_q = 0 if lat_q ∈ {0, 2²¹−1}
raw   = (1≪60) | (21≪52) | (0xAB≪44) | (lat_q≪22) | lng_q       (bit 43 = 0)
```

**String form** (cell64.rs:14-24; alphabet.rs:22-46):
- `cell64 = A[raw≫48] . A[(raw≫32)&0xFFFF] . A[(raw≫16)&0xFFFF] . A[raw&0xFFFF]`.
- `A[i]` for i < 44100 is the CVCV syllable. C ∈ `bcdfghjklmnpqrstvwxyz` (21 letters), V ∈ `aeiouAEIOU` (10 letters), ordered c1,v1,c2,v2.
- `A[i]` for i ≥ 44100 is `"z%04x" % i`.
- The first group of every geo cell is `defi`, which is 0x115A.

**Inverse** (geo.rs:284-305): `lat = lat_q/(2²¹−1)·180 − 90`, `lng = lng_q/(2²²−1)·360 − 180`. This is the grid node itself, and the bbox is ± half a step. Derivations use this node as their lat/lng.

**Geometry:**
- Δφ = 180/(2²¹−1) = 8.5831e-5°, and Δλ = 360/(2²²−1) = 8.5831e-5°.
- At the equator: 9.5546 m, using 111 319.491 m/°. This is `CELL_PITCH_M_EQUATOR`, geo.rs:96.
- At φ = 32.571° (WGS-84 radii), N–S = Δφ·M(φ) = 9.518 m and E–W = Δλ·N(φ)·cos φ = 8.060 m. That is the "≈9.5 × 8.1 m".

Example: `defi.zb572.xoso.zb1ec` → raw 0x115AB57296ADB1EC → (32.57125977099409, 77.03447748052537).

Plain: rounding to the nearest node of a lat/lng lattice. It is not Hilbert-ordered, despite older docs (geo.rs:5-9).

Reproduced by our script: **yes**. `trace_fact.py` [5] decodes the cell independently and it equals the derivation args lat/lng. Audit: the raw value and the prefix check.

## 3. tslot

`tslot = floor(max(unix_s, 0) / slot_seconds(tempo))`. The epoch is 1970-01-01 UTC. `EMEM_EPOCH_UNIX` (2026) is defined but not subtracted.

`slot_seconds`:

| tempo | slot_seconds |
|---|---|
| Static | 0, so tslot ≡ 0 |
| Slow | 365·86400 |
| Composite16Day | 16·86400 |
| Composite8Day | 8·86400 |
| Medium | 30·86400 |
| Fast | 86400 |
| UltraFast | 3600 |

- Sentinel-2 (`sentinel2_raw`, `indices`) is `fast`, so tslot = UTC days since 1970-01-01. `s2.* 20721` = 2026-09-25.
- The S2 point path computes it from `item.datetime`.
- band_raster computes it from the scene's date `YYYY-MM-DD`: `days_from_civil·86400/86400`.
- tslot 0 is used by Static bands (e.g. `copdem30m.elevation_mean`) and by absences that pass 0 explicitly (e.g. GMRT).

Citations:
- emem-core/src/tslot.rs:47, 51-61, 70-76
- bands-v0.json:288-293 (sentinel2_raw fast)
- lib.rs:81021-81038 (`band_tempo_for_key`), 52640-52650 (S2 tslot)
- band_raster.rs:324-328

Reproduced by our script: **yes**. `trace_fact.py` [8]: `floor(unix(item.datetime)/86400) == fact.tslot`.

## 4. Bi-temporal recall

The bound is `B = (Tv = as_of_tslot, Tt = as_of_signed_at)`. `passes(f) ⇔ (Tv=∅ ∨ t(f) ≤ Tv) ∧ (Tt=∅ ∨ signed_at(f) ≤ Tt)`. Here `t(f)` is `tslot`, or `tslot_window[1]` for a derivative. `≤` on `signed_at` is a **byte-lexicographic string compare**.

```
per key k: if Tt set → cid*(k) = argmax_{c ∈ history(k) ∪ {current(k)}, passes(c)} (signed_at, cid)      [derivatives skipped]
per band:  if no exact tslot and B ≠ ∅ → keep argmax_{k : tslot(k) ≤ Tv} (tslot, cid)                    [latest_per_band]
```

- With an exact `tslot`, the lookup is `(cell, band, tslot)` and the transaction-time filter applies. `tslot > as_of_tslot` → 400 `invalid_temporal_bound`.
- With an unbounded recall, `latest_per_band` is not applied.

Plain: first choose, per key, the newest signature not after `as_of_signed_at`. Then, per band, the highest tslot not after `as_of_tslot`.

Citations:
- emem-primitives/src/recall.rs:102-128, 282-391 (collapse 357-361, 386-388), 619-628, 636-655
- emem-storage/src/lib.rs:235-258 (`fact_passes`), 1833-1880 (history walk), 1177-1199

Code note (from reading, not tested):
- `as_of_signed_at` is validated (`cbor_ops.rs:128`, which accepts `.fff` and `±HH:MM`) but not normalised before the string compare.
- So `…56.5Z` sorts before `…56Z`, and `+05:30` offsets compare as raw text.
- The receipt's as_of digest does normalise (receipt.rs:259).

Reproduced by our script: **partly**. `verify_bitemporal.py` replays one key at four `as_of_signed_at` values and re-hashes each answer. It checks the behaviour, not the tie-break.

## 5. Sentinel-2 point read (after the 28 Sep fix)

**Reprojection:** `(E, N) = TM_WGS84(lat, lng; zone from the item's proj:epsg)`.
- It uses a forced zone and Snyder's series with k0 = 0.9996, FE = 500 000, and FN = 10⁷ for 327xx.
- lat/lng are the cell node (§2).
- Citations: proj.rs:79-93, 97-147; lib.rs:52631-52633.

**Pixel** (cog.rs:137-169). Tiepoint `(i, j, X, Y)`, scale `(sx, sy)`:
```
col_f = i + (E − X)/sx ;  row_f = j + (Y − N)/sy
PixelIsArea: (col,row) = (⌊col_f + 1e−6⌋, ⌊row_f + 1e−6⌋)      PixelIsPoint: (round col_f, round row_f)
```

**Pre-fix rule:** `round` for all rasters.
- Facts from `.tif` sources with `signed_at < PIXEL_FIX_AT = 2026-09-28T04:09:26Z` no longer answer "latest" (lib.rs:12651, 12676-12696).
- New GeoTIFF reads append `reader=cog-pixel-floor@2` to the args (lib.rs:57113-57138).
- CHANGELOG.md:68.

**Reflectance** (lib.rs:51726-51748, 52747-52748; stac.rs:161-196): `ρ = (DN + o)·10⁻⁴`, where `o` is:

| catalogue | condition | o |
|---|---|---|
| Element84 (harmonised) | always | 0 |
| Planetary Computer | `s2:processing_baseline ≥ "04.00"` (string compare) | −1000 |
| Planetary Computer | baseline < "04.00" | 0 |
| Planetary Computer | baseline absent | refused (error) |
| any other catalogue | always | refused |

`DN = 0` → error "nodata" (raw bands).

**NDVI** (lib.rs:52771-52778): `NDVI = (ρ₈ − ρ₄)/(ρ₈ + ρ₄)` with `ρ₈ = r(DN_B08)`, `ρ₄ = r(DN_B04)`. The result is an error if `ρ₈ + ρ₄ < 1e−6`.

**SCL** (lib.rs:51620-51635, 52010-52040, 52703-52735, 52984-52995):
- The SCL pixel at the same point is probed per candidate scene.
- Hard reject: {0, 1, 8, 9, 10}. On a hard reject the picker tries the next (older) candidate.
- If every candidate is rejected, the result is a signed Absence `s2_scl_pixel_unusable`.
- Confidence depends on the SCL class:

| SCL class | confidence |
|---|---|
| 4, 5, 6, 11 | 0.95 |
| 7 | 0.75 |
| 2, 3 | 0.65 |
| SCL unavailable | clamp(1 − cloud/100, 0.30, 0.95) |

**Args order:** `[lat, lng, scene_id, epsg, formula_note, [DN…], scene_cloud, max_cloud, lookback_days, scl, scenes_tried, catalogue, offset]` (lib.rs:53033-53051).

Reproduced by our script: **yes**. `v8/trace_fact.py` [7]-[9b] on `oj5ceccile…`:
- Own TIFF decoder and TM projection; pyproj agrees within dE = 2e-10 m.
- floor gives (col, row) = (9098, 9443) and DN 3502/1900, equal to the signed DNs.
- NDVI is bit-identical (0x3fde233788cde233).
- The pre-fix `round` gives row 9444 (NDVI 0.3016).
- SCL = 4 → 0.95.
- `verify_ndvi.py`: the offset rule.

## 6. Field tokens, bundles, tree, track chain

**Raster** `emem:raster:{aoi_cid}:{band}:{tslot}:{derivation_cid}` (band_raster.rs:183-189, 318, 381-419, 420-436, 490):
- `aoi_cid = b32(H(cbor{min_lat, min_lng, max_lat, max_lng}))`: struct order, shortest floats.
- `artifact_cid = b32(H(EMEMGRD1 grid bytes))`: grid.rs, with a 64-byte header, then f32 LE row-major values of `harmonise(DN, o) = DN=0 ? 0 : DN+o`.
- `derivation_cid = fact_cid(Derivative{cell = centre cell, band "field.derivation", tslot_window [t,t], op "band_raster", parents = anchor cids that already exist, value = record JSON (keys sorted), confidence 1.0, fn_key "band_raster@1", …, signed_at})`.
- Because `signed_at` is hashed, a re-mint gives a new token.

**Cube** `emem:cube:{aoi_cid}:{band}:{lo}..{hi}:{derivation_cid}` (band_raster.rs:1717-1724, 1914, 2000):
- `cube_cid = b32(H(cbor([member derivation_cid…] in ascending tslot))`.
- `derivation_cid` = fact_cid of the `band_cube` derivative.

**Rasterset** `emem:rasterset:{bundle_cid}:{derivation_cid}`: `bundle_cid = b32(H(cbor([dcid…, "purpose:"+p])))` (band_raster.rs:1045-1053, 1185).

**Memory bundle** `emem:bundle:{bundle_cid}`: `bundle_cid = b32(H("emem.memory_bundle.v1|" ‖ purpose? ‖ "\n" ‖ Σ(cell‖"|"‖band‖"|"‖dec(tslot)‖"|"‖fact_cid?‖"\n"))[0..16])` (memory_bundle.rs:159-182).
- It is 26 characters.
- The module doc (memory_bundle.rs:7) says `canonical_cbor`; the code uses the pipe preimage.

**Tree / pointer.v1** (tree.rs:65-99, 110-143; `emem:tree:{file_cid}#row=i`, tree.rs:409):
```
leaf = H(url ‖ u64be(offset) ‖ u64be(length) ‖ hash32)       (url "" for "·"; hash 0³² if absent)
node = H(l ‖ r);  odd node promoted unchanged;  no 0x00/0x01 domain separation
directory.v1 row: hash = H(path "\n" size "\n" publisher_hash), leaf over (url, 0, size, hash)
```

**Track chain** (ememdemo client code, recorded in docs/collaboration-log.md:448146-448147; not in emem crates):
- `link₀ = cidOf("")`, `linkᵢ = cidOf(utf8(linkᵢ₋₁) ‖ utf8(refᵢ))`, `head = link_n`.
- `cidOf(b) = b32(H(b)[0..16])` (collaboration-log.md:485704).

Reproduced by our script:
- artifact_cid **yes**: `data/v9/rawband/analyze.py:170-174`.
- pointer.v1 **yes**: `v8/doc_pointer_v9.py:8-15` and `evidence_pointer.py` build roots with the same rule, and the track shows them ✓.
- track chain **yes**: `v8/make_track.py:40-42`.
- aoi_cid, cube_cid and derivation_cid-as-fact_cid: **yes (audit, not in repro/)**.
  - A hand-rolled CBOR of bbox {32.55, 77.01, 32.59, 77.058} gives `zhiz2prb…5voq`.
  - The 5 member dcids of `cubeK_members.json` give `k5on7ska…eeka`, which equals `/v1/cube/resolve`.
  - `/v1/facts/{4wmvv7i6…, 7ath7qdw…}` bytes re-hash to their names.
- rasterset and memory bundle: **no**.

## 7. Receipt preimage v2

`PreimageV1(d) = "emem.preimage.v1\0" ‖ u32le(|d|) ‖ d`. Then segments:
- scalar: `tag ‖ u32le(len) ‖ bytes`
- list: `tag ‖ u32le(count) ‖ (u32le(len) ‖ bytes)*`

`msg = H(stream)`, and `sig = Ed25519(sk, msg)`.

```
d = "receipt":
 0x01 request_id (ULID) · 0x02 served_at · [0x03 hex H(cbor scope)] · [0x04 hex H(cbor as_of)] · [0x05 hex H(cbor sorted edge_cids)]
 · [0x06 hex H(cbor source_versions BTreeMap{bands_cid,registry_cid,schema_cid,sources_cid})] · 0x07 primitive
 · 0x08 list(cells) · 0x09 list(fact_cids, served order) · [0x0a hex field_binding] · 0x0b hex merkle_binding
merkle_binding = H(PreimageV1("merkle") ‖ (proof ? 0x01 root · 0x02 u32le leaf_index · 0x03 ‖path‖ · 0x04 [rule_version] : 0x05 ""))
field_binding  = H(PreimageV1("field") ‖ 0x01 aoi_cid ‖ 0x02 derivation_cid)
```

- `[…]` marks a segment present only when non-empty.
- v1 is the same without 0x0b.
- The proof is for `fact_cids[0]` only.
- No value is signed; values are bound through `fact_cid`.

Citations:
- emem-attest/src/lib.rs:167-213, 217-243, 256-261, 269-320, 333-375, 382-422
- emem-storage/src/server.rs:304-375 (proof resolved before signing, 350-352), 510-519
- emem-api-rest/src/lib.rs:21362-21413 (verifier)

Reproduced by our script: **yes**. `verify_receipt_tamper.py`: valid as served; proof-stripped and v1-downgraded variants fail. Also `trace_fact.py` [10].

## 8. Transparency log

```
entry_i  = H(ciborium(Attestation))  (or H(raw cbor) for append_cbor records); record on disk = u32le(len) ‖ cbor ‖ entry_i
leaf     = H(0x00 ‖ entry)      node = H(0x01 ‖ l ‖ r)      MTH(∅) = H("")
MTH(D[n]) = leaf(d₀) if n=1, else node(MTH(D[0:k]), MTH(D[k:n])), k = largest power of 2 < n     (RFC 6962/9162)
STH:     Ed25519 over H(PreimageV1("emem.translog.sth.v1") ‖ 1:u64be tree_size ‖ 2:root ‖ 3:signed_at ‖ 4:responder_pk)
witness: Ed25519_w over H(PreimageV1("emem.translog.witness.v1") ‖ 1:u64be tree_size ‖ 2:root ‖ 3:witness_pk)
```

- Inclusion and consistency proofs follow RFC 9162 §2.1.3/§2.1.4 (translog.rs:88-267).
- A leaf commits to one whole attestation. The attestation holds `facts[]`, `batch_root`, `attester`, `registry_cid`, `schema_cid`, `signature`, `attested_at` and more.
- It does not commit to one fact_cid, and there is no fact_cid→leaf index.

**Batch root inside an attestation** (a different tree from the log):
- `leaves = sort(H(cbor(fact)))`. Duplicates are rejected.
- `merkle_root_v1`: `H(0x00‖leaf)`, then `H(0x01‖l‖r)`, and an **odd node is paired with itself**.
- The attestation signature is over `H(PreimageV1("attestation") ‖ 1:batch_root ‖ 2:registry_cid ‖ 3:schema_cid)`.

Citations:
- translog.rs:28-82, 119-158, 204-267
- emem-storage/src/merkle_log.rs:109-130, 304-321
- lib.rs:21817-21870, 22600-22619
- attest.rs:105-124
- emem-attest/src/lib.rs:441-451, 738-796

Reproduced by our script: **yes**. `verify_log.py`, `v8/verify_bundle.py`, `trace_fact.py` [11]-[14]: entry hash, batch root, attestation signature, STH, inclusion (path 20), consistency, witness co-signature.

## 9. Absence

- `reason_cid = b32(H(utf8(reason_text))[0..16])`, which is 26 characters. It hashes the prose reason string, not the upstream response.
- The fact is `Absence{…, confidence 1.0, sources[{scheme, id = upstream url, captured_at = signed_at}]}`. It is signed as a one-fact attestation like any other fact.

When an absence is signed, and when nothing is signed:
- **Signed**: when the materialiser gets a typed "no data here" answer. Examples:
  - a coverage gap or not-implemented area (GMRT);
  - a fill or no-data value;
  - a 404 for a known tile of a pinned release;
  - Cop-DEM 0 m over water;
  - every Sentinel-2 candidate scene cloudy at the pixel (SCL hard reject).
- **Unsigned**: transport or upstream errors. Examples: `"… fetch failed"`, "every catalogue failed", "no scene under X % in ±Nd". These return `Err`, which surfaces as an unsigned `skip_reason` or a `pending` entry.

Citations:
- lib.rs:47809-47818, 57587-57634 (policy doc 57587-57594), 55636-55652 (GMRT: typed → signed, other `Err` → unsigned), 52703-52735 (S2), 51556 / 52042 (no-scene → Err)
- CHANGELOG.md:73 (404 rule)

Reproduced by our script: **yes**. `verify_absence.py` re-derives `reason_cid` from the served reason (ocean, no Cop-DEM tile).

## 10. derive recompute check

Recompute runs only when the caller pins `code_cid` and `op ∈ {delta, mean, sum}` over scalar parents (lib.rs:38842, 39180-39185).

```
delta = v[1] − v[0] (exactly 2 parents);  sum = Σ v (left fold, input order);  mean = (Σ v)/n
r ← canonical_float(recomputed);  gap = ulps(r, claimed) = |bits(r) − bits(claimed)|  (∞ if NaN or signs differ; 0 if equal)
verified ⇔ (op ∈ {mean,sum} ∧ n > 2) ? gap ≤ 4 : r == claimed        → provenance "deterministic_index"
```

- The response states `rule`, `ulp_tolerance` (4 or 0) and `ulp_gap`.
- If no pure op applies, a registered algorithm AST may be evaluated, with exact equality (lib.rs:39208-39222).

Citations: lib.rs:38842, 38862, 38886-38899, 38939-38955, 39226-39306.

Doc vs code: `DERIVE_SIGNATURE_ATTESTS` (lib.rs:38818-38827) says "`mean` is excluded"; the code includes it in `GC1_TIER1_PURE_OPS`.

Reproduced by our script: **no**.

## 11. Guard number verdict

- Scan: for each sentence (tokens masked, same length) citing exactly one byte-resolving token, collect every number with its written decimals `d`. The regex-free scanner allows `,` thousands separators and one `.`. If the citing fragment has no numbers, it also takes the numbers of the preceding sentence, provided that sentence cites nothing.
- Agreement: `agrees(s, d, a) ⇔ round(a·10^min(d,12))/10^min(d,12) == s  ∨  |a − s|/max(|a|,|s|) ≤ 1e−9`.
- Verdict: deny `ProvValue` iff the cited token resolved to a numeric value `a` and **no** stated number in that sentence agrees. So any one agreeing number passes the sentence.
- Signature and byte-mismatch denies are checked first.

Citations: emem-guard/src/claim.rs:1017-1102, 1105-1143, 1151-1160; policy.rs:480-537.

Reproduced by our script: **no**. `echo_verify` (Exhibit B) is a different endpoint.

## 12. Contradiction severity and freshness kernel

**Severity** for n ≥ 2 primaries at one key (memory_contradictions.rs:475-512, 515-535, 555-573, 581-618):

| value shape | severity |
|---|---|
| scalar, all non-negative integers and band ∈ {`esa_worldcover.lc_2021`, `landcover`, `surface_water.transition_class`, `s2.scl`} | `1 − max_class_count/n` |
| other scalar | `clamp((max−min)/R, 0, 1)` |
| vectors | `clamp(1 − mean_{i<j} cos(vᵢ, vⱼ), 0, 1)` |
| text / int / bytes | mode share, as for categorical |
| mixed shapes | 1.0 |

- `R` is the registry `value_range` width (band, or `family.dimension`).
- If no range is registered, `R = max(max−min, 1.0)`. So any spread ≥ 1 unit scores 1.0.
- Every attestation counts, including identical re-signings.

**Freshness** `Q(Δt)` (lib.rs:80459-80510):
- Δt = |now − tslot_start|. It is measured from the slot start, not from the capture time (lib.rs:80588-80589).
- `stale ⇔ Q < 0.5`.

| tempo | Q(Δt) |
|---|---|
| Static | 1 |
| Slow | max(0, 1 − Δt/365 d) |
| Medium / 8-day / 16-day | exp(−(Δt/σ)²), σ = slot length |
| Fast | Δt > 5 d ? 0 : clamp(0.5 + 0.5·cos(2πΔt/5 d), 0, 1) |
| UltraFast | max(0, 1 − Δt/6 h) |

The Fast kernel is not monotonic: Q = 1 at 0 d, 0 at 2.5 d, 0.905 at 4.5 d, 1.0 at 5 d, 0 at >5 d.

Reproduced by our script: **partly**.
- `data/contra_bengaluru.json` is a live response giving severity 1.000 for a 918.0 vs 915.07 m spread. That fits the `R = max(spread, 1)` fallback.
- The kernel values are recomputed by hand from the formula.

## 13. Scene selection in band_raster / cube, and defect 27

band_raster.rs:224-238 → lib.rs:51499-51556, stac.rs:405-422:

```
t = days_from_civil(observed_on)·86400 + 43200            (noon UTC; now if observed_on absent)
for (c, D) in [(40,30), (60,60), (80,90)]:                 (EMEM_S2_MAX_CLOUD/LOOKBACK_DAYS defaults)
   window = [max(t − D·86400, 0),  max(min(t + D·86400, now), lo + 86400)]
   items  = STAC(intersects = bbox centre, eo:cloud_cover < c, datetime ∈ window, sortby datetime DESC, limit 1)
   if items ≠ ∅: return items[0]                          (first catalogue that answers: Planetary Computer, then Element84 on error)
```

The rule is: the **newest** scene under 40 % cloud in a window reaching up to 30 days after the requested date. It is not the nearest scene, not a scene on or before the date, and not the lowest-cloud scene.

- band_raster does no SCL probe and has no `at_or_before`. The point path has both (`s2_pick_clear_scene`, lib.rs:51892-51944).
- The record does not store `observed_on`, and no warning is emitted.
- The cube calls band_raster per date (band_raster.rs:1774). It dedupes by tslot, keeps `requested_date_distance_days` (1896), and does not warn.
- Doc vs code: the `BandCubeReq` doc (band_raster.rs:1708) says "names the nearest scene"; the code picks the newest.

**Defect 27, precisely.** On 30 Sep, `observed_on = 2026-09-23` gives the window [2026-08-24 12:00, 2026-09-30 now].
- The newest scene under 40 % cloud containing the centre is S2A 2026-09-25 (10.8 %). It wins.
- S2C 2026-09-23 (20 %) is older inside the same window, so it can never be returned.
- Every `observed_on` from about 2026-08-26 to 2026-09-30 yields the same 25 Sep scene, unless a newer scene under 40 % exists.

Reproduced by our script: **yes (observed)**.
- `data/v9/rawband/results.md`: the 23, 22 and 21 Sep requests all gave the byte-identical 25 Sep raster.
- `data/cubeK_members.json`: 05-15→06-10 (+26 d), 06-15→06-30 (+15), 07-15→08-03 (+19), 08-15→09-13 (+29), 09-15→09-25 (+10). Every pick is later than the request, as the newest-in-window rule predicts.

## 14. TESSERA dequantisation; Clay pin

**TESSERA** (lib.rs:48946-49026; row/col 48698-48740):
- Tile centre = `floor(x·10)/10 + 0.05` for lng and lat.
- Zone comes from the tile-centre lng. `(x, y) = UTM(lat, lng)` in that zone.
- `min_e` and `max_n` come from the 4 projected tile corners.
- `row = clamp(⌊(max_n − y)/10⌋)`, `col = clamp(⌊(x − min_e)/10⌋)`, `idx = row·W + col`.
- `eᵢ = f64( f32(int8 qᵢ) × f32 s )`. `s` is a per-pixel scalar, or per-channel `sᵢ` when the scales `.npy` has 128 per pixel. Scales are f32 LE.
- `emb` is read at `data_off + idx·128`; `scale` at `sc_off + idx·4·k`.
- emem.dev has retired `geotessera` via `EMEM_RETIRED_BANDS` (docs/memory.md:43-48). The code path remains.

**Clay pin**:
- The fact carries `sources[] = {scheme "model.clay_v1_5", id "made-with-clay/Clay@<64 hex>"}`, `derivation.args[4] = <64 hex>`, and `served_via.model_blake2b_hex`. These are inside the hashed bytes.
- `fact.rs:140` names it "blake2b-256 of the model checkpoint".
- The hashing code lived in `python/jepa_v2_sidecar/`, which has been removed (CHANGELOG.md:77). The digest parameters and the exact file hashed are **not determined** at origin/main.
- Observed value: `cccf45f9087c63e8…58697d` (fact `jh2kmfiy…`).
- lib.rs:14250-14262 (binding rule).

Reproduced by our script: **no** for both. The Clay fact bytes re-hash to their cid (audit). The weights were not hashed.

## 15. OS trace gate (`emem.os_trace.v1`)

**Record** (schema.rs:34-166): `OsTrace{schema, device{device_key, key_epoch, substrate_profile, platform, os, kernel, boot_id}, window_start_ns, window_end_ns, segments[{layer, seq, clock_start_ns, clock_end_ns, event_count, log_digest, prev_digest?, encoding}], outputs[{payload_digest, band?, emitted_at_ns, layer}], trace_root, prev_trace_cid?, signature}`.

```
dᵢ = H(cbor(segᵢ)),  segᵢ.prev_digest = b32(dᵢ₋₁), seg₀.prev_digest = ∅
trace_root = merkle_root_v1([d₀…d_{n−1}] in chain order)
sig = Ed25519_dev( H(PreimageV1("os_trace") ‖ 1:schema ‖ 2:H(cbor(device)) ‖ 3:profile ‖ 4:u64le start ‖ u64le end ‖ 5:trace_root
                       ‖ 6:list(b32 H(cbor(outputⱼ))) ‖ [7:prev_trace_cid]) )
trace_cid = b32(H(cbor(OsTrace incl. signature)))
fact binding: b32(H(cbor(fact.value))) ∈ { outputⱼ.payload_digest }       (value only; band/cell not checked)
```

**Admission:**
- Admit ⇔ `reasons = ∅`. The verifier collects all failures from **17** `RejectReason` variants:
  - SchemaMismatch, ProfileMismatch, AdmissionNotTraceBased, WindowEmpty, EmptyTrace, MissingLayer;
  - SeqOutOfOrder, ChainBroken, ClockNonMonotonic, ClockOutsideWindow, DuplicateSegmentDigest, RootMismatch;
  - OutputOutsideWindow, OutputUnbound, PrevTraceMalformed, SignatureInvalid (`verify_strict`), EncodingFailed.
- The write gate adds these checks:
  - trace device key = attester;
  - stream continuity: `prev_trace_cid` = stored head per (device, boot_id);
  - registered encodings that can capture each layer;
  - platform-whitelisted encodings;
  - primary facts only, no edges;
  - every value digest bound in `outputs`.
- The gate applies only to enrolled keys (`None` otherwise).

**Drift anchor** (drift.rs:50-87):
- `z = |x_dev − x_anchor| / (3σ)`, `score = z/(1+z)`.
- If σ ≤ 0 or σ is non-finite: score = 0 if equal, else 1.
- Verdict: `<0.5` Consistent (<3σ), `<0.75` Tension (3–9σ), else Contradicted.
- It is used only in `emem-primitives/examples/satellite_downlink.rs:200`. It is not wired into ingest.

Citations: emem-attest/src/lib.rs:613-677; emem-trace/src/verify.rs:21-119, 164-321; emem-storage/src/trace_gate.rs:392-534; drift.rs:50-87.

Reproduced by our script: **no**. RESEARCH_STATE notes that no real device is admitted.
