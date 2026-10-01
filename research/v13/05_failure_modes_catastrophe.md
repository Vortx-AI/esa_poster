# 05. Failure modes: each error emem found in itself is a failure class of any multi-agent EO pipeline

Written 2026-10-01 (UTC) for the v13 final A0. Topic: `failure_modes`. Read-only research: nothing on the board, in the
figures, in emem or on emem.dev was changed. No emem read tool that signs or stores was called (no `/v1/recall`,
`/v1/ask`, `/v1/band_raster`, `/v1/backfill`); emem was touched only with `GET /v1/facts/<cid>` (105 GETs).

Labels on every item:

- **MEASURED**: computed or counted in this session from committed files, from public rasters re-read here, or from
  code at emem `origin/main` 18adb67 (command, file:line given).
- **LIVE**: fetched from a live service in this session (2026-09-30/10-01 UTC).
- **SPEC**: what a document, changelog or code comment states; not exercised here.
- **INFERRED**: my arithmetic or reading from the above; not a measurement.
- **UNVERIFIED**: stated by a source I could not open or re-check.

Inputs read in full: `research/SHARED_STATE_EMEM_A0_MASTER.md` (558 lines), `research/do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md`
(defects 1 to 37), `research/repro/v11/{README.md,out/summary.md}` (R1), `research/repro/v12/CLAIMS_MAP.md`,
`research/repro/data/v9/rawband/results.md`, `research/repro/data/v8/{prevalence_summary.json,pixel_check.json,results.json}`,
`research/repro/data/contra_bengaluru.json`, `research/repro/data/v11/ask_keylong.json`,
`research/repro/v12/data/case_rondonia_eudr.json`, `research/v13/01_v12_state.md` and `02_experiment_design.md` (for
alignment of mutation ids), GitHub issues #7, #13, #26 of Vortx-AI/esa_poster (the other 36 titles read via `list_issues`),
emem `CHANGELOG.md` at 18adb67 (all release blocks from [Unreleased] to [1.4.0]), `docs/paper-section-statistics-and-threats.md`,
`crates/emem-fetch/src/{cog.rs,stac.rs}`, `crates/emem-api-rest/src/{lib.rs,band_raster.rs}`.

Mutation ids (M1 to M17, M18, M20) are those of R1 (`research/repro/v11/mutation_suite.py`) and of the v13 experiment design
(`research/v13/02_experiment_design.md:215-243`). Verification levels A to I are R1's: A prose, B JSON, C resolve the
reference, D re-hash, E cell/band/tslot binding, F signature under a pinned key, G log inclusion, H recompute from signed
inputs, I re-read the source pixel. The brief's ladder (MASTER §11): L0 bytes, L1 identity, L2 derivation, L3 source,
L4 entity, L5 physical truth / decision.

---

## 0. Findings in one screen

1. **Seventeen failure classes** come out of emem's own record (defects 1 to 37, the CHANGELOG at 18adb67, R1, the
   compaction and handoff runs, the v9 raw-band run). Every one has a public occurrence outside emem, in GDAL, rasterio,
   STAC catalogues, ESA and NASA product histories, LLM and multi-agent papers, or incident reports (section 2).
2. **The wrong pixel is the strongest case.** Every emem COG reader rounded the fractional pixel index instead of
   flooring it "from the first commit" until 2026-09-28 (SPEC, `CHANGELOG.md:47,68`; the earliest sampled record is
   signed 2026-05-14, so at least 4.5 months, INFERRED); 162 of 200 sampled Sentinel-2 records carry the neighbour's DNs
   (MEASURED, `prevalence_summary.json`). Those records pass hash, signature, log and recompute; only a re-read of the
   pixel exposes them. The same confusion is documented in GDAL (RFC 33: the 1.8 change "will alter the apparent
   georeferencing of all GeoTIFF files with PixelIsPoint set"), in rasterio (discussion #2478 asks why `index()` floors
   instead of rounding), and in the AWS Copernicus DEM mirror, which removed a row and column per tile and moved the
   pixel-centre convention by one pixel. Townshend et al. (1992) measured that a one-pixel misregistration induces an
   error "greater than 50% of the actual differences in the NDVI". ESA specifies Sentinel-2 multi-temporal
   co-registration at 0.3 pixel; the reader rule alone moved emem's reads by up to 1 pixel.
3. **New measurement, LIVE + MEASURED: one pixel, one question, eight answers.** For "NDVI at the Keylong field cell,
   25 Sep 2026", real mechanisms produce 0.4709 (right), 0.47, 0.4370, 0.4237, 0.3016, 0.2966, 0.2824 and 1.1427. Under
   the R3 rule (irrigate iff NDVI ≤ 0.4705) six of the seven wrong values flip the decision and the seventh is outside
   the physical range (section 6). Each wrong value is caught by a different check, or by none.
4. **New, LIVE: Element84's Sentinel-2 metadata contradicts itself.** All five Keylong items of 23 to 30 Sep carry
   `earthsearch:boa_offset_applied: true` and also `raster:bands` `offset: -0.1`. At the Keylong pixel their DNs are
   exactly Planetary Computer's minus 1000 (B04 900 vs 1900, B08 2502 vs 3502), so the offset is already applied. A
   client that follows Element84's README ("If the offset is anything other than 0, then it should be applied") gets
   NDVI 1.143 for the S2A scene and 0.983 for the S2B scene of the same day (INFERRED arithmetic on MEASURED DNs).
5. **New, MEASURED: a date does not identify an observation.** Two Sentinel-2 acquisitions cover the Keylong pixel on
   25 Sep (S2A orbit 005, 10.8 % cloud; S2B orbit 105, 1.6 % cloud): NDVI 0.4709 and 0.4370. They share emem's day slot
   (tslot 20721), so the cell/band/tslot binding cannot tell them apart; the scene id in the record can.
6. **New, MEASURED: the wrong-pixel rule at the Rondônia EUDR grid.** Re-reading Hansen v1.13 and JRC GFC2020 V4 at the
   100 signed cell coordinates: the old rounding rule selects a different pixel at 79 (Hansen) and 82 (GFC2020) points,
   changes the loss year at 7, tree cover 2000 at 21 and the GFC2020 forest class at 1. The EUDR flag count is 3 under
   both rules: **0 flips on this grid.** Errors cluster at class edges; this grid had no flag on an edge. The post-fix
   signed loss-year facts equal the independent floor read at 100 of 100 points.
7. **New, MEASURED: defect 14 resolved.** The 27 Jan 2022 Keylong record (`2dpnuf4e…`) is not an offset error: Element84 v0
   states `sentinel:boa_offset_applied: true` for that item. It is a pre-fix neighbour-pixel record: its signed DNs
   (3034, 3344) are the rounded pixel; the containing pixel reads 5900, 6195 (NDVI −0.0486 signed vs −0.0244).
8. **A processing change in the middle of a series fabricates a trend.** Comparing emem's pre-fix 23 Sep record (0.3444)
   with the post-fix 25 Sep record (0.4709) shows +0.127 "greening"; the containing pixels give −0.015 (MEASURED). The
   same shape outside emem: users report 2022 NDVI "less around 0.1-0.2" after baseline 04.00 (Sinergise forum,
   26 Apr 2024); Terra MODIS C5 degradation produced 17.4 % vs 6.7 % negative NDVI trends against Aqua (Wang et al.
   2012); the Terra C6 look-up table was "incorrect for the period 2012 – 2017", affecting bands 1 and 2 (NASA C6.1
   changes); Hansen GFC: "users will notice inconsistencies".
9. **Detectable is not detected.** emem's own wrong-pixel records verified at every cryptographic level for months and were
   found by an audit that re-read pixels against GDAL (`cog.rs:132-134`). In the v9 run 9 of 10 agents saw that both
   dates were one scene, and 3 of 10 then invented a cause ("probably wasn't imaged that day"). A record that carries
   scene id, DNs, coordinates, reader version and `signed_at` makes each class checkable; a receiver still has to check.
10. **Two classes stay out of reach of any reference protocol**: the entity referent ("Maasvlakte ramp 7" resolves to OSM
    relation 1411107, an admin_level 10 boundary of all of Maasvlakte, LIVE) and product truth (GFC2020 V2 forest
    commission error 18 %, V3 13.1 %, JRC). They define the top of the ladder and the poster's guarantee boundary.

---

## 1. Method

**Where emem's errors come from.** (i) Defects 1 to 37 (`research/do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md`); (ii) the
"Fixed" and descriptive entries of emem `CHANGELOG.md` at 18adb67 (release blocks [Unreleased] lines 8-15, [2.4.2]
2026-09-29 lines 16-78, [2.4.0] 79-132, [2.3.0] 2026-08-26 133-314, [2.2.0] 315-462, [2.0.0] 2026-08-05 659-737,
[1.4.0] 2026-07-31 738-843); (iii) R1 (17 mutations × 9 levels), the pre-registered compaction run, the two-LLM handoff,
the v9 raw-band run; (iv) the live re-reads made for this report (section 4).

**Grouping.** By mechanism, not by component: a class is "a way a value that one agent hands another can stop
describing the observation the first agent meant". Seventeen classes.

**Outside evidence.** Each class needs at least one public source that the same mechanism occurs elsewhere. Quotes are
verbatim from the page as fetched on 2026-10-01; a source that would not open is marked UNVERIFIED and is not used for a
number.

**Consequences.** Only sourced numbers. Where I apply a published relation to emem's numbers (for example a crop
coefficient), the result is INFERRED and says so.

**Detection.** For each class: the first R1 level that stops it, the brief's layer (L0 to L5), and what stays undetected.

**Ranking (the ladder, section 5).** By the depth of check a wrong value survives: the higher the rung, the more checks
it passes and the more confidently it is acted on. Within a rung, by measured consequence. The ranking rule is mine
(INFERRED); every number on a rung is sourced.

---

## 2. Summary table

Status column: state at emem 18adb67 as far as it can be read from code or CHANGELOG; "fixed" is SPEC unless a
measurement is cited.

| # | class | emem incident (label, source) | outside emem (source, §10 ref) | consequence (label) | first check that stops it | stays undetected | status at 18adb67 |
|---|---|---|---|---|---|---|---|
| F1 | **wrong pixel** (round vs floor, half-pixel corner/centre) | 162/200 pre-fix S2 records carry neighbour DNs; NDVI 0.4709 → 0.3016 at Keylong (MEASURED); all COG bands "from the first commit" (SPEC, `CHANGELOG.md:68`); raster headers half a pixel off, SCL one pixel off at cloud edges (`:59`) | GDAL RFC 33 [S1]; rasterio #2478, #2205 [S2, S3]; AWS Cop-DEM mirror grid [S4]; Townshend 1992 [S5]; S2 co-registration spec 0.3 px [S6] | decision flip at the R3 threshold (MEASURED); spurious +0.127 change (MEASURED); 1 px → error > 50 % of NDVI differences (SPEC, [S5]) | I (source re-read), only | old records stay signed; a receiver who skips I accepts them | fixed 2026-09-28T04:09:26Z (`:47`, code `cog.rs:137-143`, MEASURED) |
| F2 | **radiometric convention** (BOA_ADD_OFFSET −1000; per catalogue; per item) | per-catalogue offset, unknown baseline refused (SPEC, `lib.rs:51714-51747`); one Keylong pixel: 0.4709 / 0.2966 omitted / 1.1427 double (MEASURED) | ESA PB 04.00 notice [S7]; GEE HARMONIZED [S8]; STEP forum users [S9]; Sinergise forum 2024 [S10]; S2Mosaic PR #9 and surtgis PR #146, both merged 30 Sep 2026 [S11, S12]; Element84 contradiction (LIVE) [S13] | NDVI pulled "toward zero by roughly a third" (SPEC, `stac.rs:176-182`); time-series step (SPEC [S10]) | H (recompute with the recorded offset); I (re-read, baseline from scene id `N0513`) | a signer that records the wrong offset passes F; only H/I catch it | handled per catalogue; E84 per-item flag not read (MEASURED: `git grep boa_offset_applied` empty) |
| F3 | **date or scene substitution** (asked 23 Sep, got 25 Sep; newest, not nearest; two scenes one day) | `band_raster observed_on=23 Sep` returned the byte-identical 25 Sep raster, 9/10 agents never got 23 Sep values, 3/10 invented a cause (MEASURED, rawband) ; code takes the first item of a newest-first search in ±30 d (MEASURED, `lib.rs:51499-51543`, `stac.rs:419`); recall default gave a 2022 scene (defect 15) | STAC item search defines no default order (MEASURED, spec text) [S14]; GEE `mosaic()` "from last to first" [S15]; E84: two 25 Sep acquisitions 0.4709 vs 0.4370 (MEASURED) | 0.4370 flips the threshold (INFERRED); a change test across "two dates" that is one scene reports no change (MEASURED, 6/10 "no material change", 5 self-declared placeholders) | E (tslot) for a different day; C (B resolves A's own reference) for a same-day scene; scene id in record | a same-day other scene passes E (same tslot) | **open** in code (newest-first, `max_scenes=1`) |
| F4 | **silent source substitution and reprocessing** | Bengaluru elevation 918.0 m (Open-Meteo GLO-90) → 915.07 m (Cop-DEM GLO-30 AWS), same band key (MEASURED, `contra_bengaluru.json`); Hansen v1.12 → v1.13, GFC2020 V3 → V4 (SPEC, `CHANGELOG.md:13,54,55,71-72`); `Source.hash` never filled (defect 25) | MODIS C6 Terra LUT error 2012-2017 bands 1-2 [S16]; Terra C5 trends 17.4 % vs 6.7 % [S17]; Hansen "users will notice inconsistencies" [S18]; GFC2020 V2 → V3 forest cover −20 % in Caatinga and Cerrado [S19]; Cop-DEM 9 releases [S20]; S2 Collection-1 reprocessing [S21]; E84 vs MPC: two processing runs of one 2022 acquisition (MEASURED) | EUDR forest baseline can change class between versions (INFERRED from [S19]) | C/E (the record names source scheme, version, fn_key, product id); as-of recall keeps what was cited | which upstream bytes were read rests on the signer (defect 25); upstream correctness is inherited (L3 partial) | versions named in facts (SPEC); `Source.hash` still None in S2 path (defect 25, UNVERIFIED today) |
| F5 | **stale state presented as current; history rewritten** | "Asked what is happening in London right now, this responder answers partly from bands 87 days old" (SPEC, `CHANGELOG.md:188-191`); `source_freshness_s` was literal 0 for an April 2021 tile (`:691-694`); 918.0 m cited in June vs 915.07 m now (MEASURED) | Google Maps routed a driver over a bridge collapsed since 2013; fatal, Sep 2022; lawsuit 2023 [S22] (analog, not EO) | an agent blamed for a value that did not exist yet (M20, INFERRED) | E (tslot) + as-of recall (E′) + log (G) for a version shown only to B (M16) | as-of compare is a raw string (defect 35); `as_of_signed_at` without tslot timed out (defect 2) | age carried per reading (SPEC) |
| F6 | **paraphrase and rounding at a threshold** | prose "0.47" for 0.4709: 5/5 wrong decisions vs token 10/10 right (MEASURED, `v8/results.json`); emem's draft check lets "≈ 0.49" pass for 0.4871 (SPEC, audit A88) | quantity hallucination in summaries (Zhao et al. 2020) [S23]; iterated LLM transmission amplifies small biases (Perez et al.) [S24] | decision flip (MEASURED, R arm) | C (resolve the reference instead of reading the prose) | none once the reference is resolved | by design |
| F7 | **compaction and shared lossy memory** | shared summary under pressure: 0/72 answers right while 3/36 pairs agreed; control 72/72 (MEASURED in emem docs, pre-registered, `paper-section-statistics-and-threats.md:87-89`) | Claude docs: "when the default summary drops something a later turn needs" [S25]; 39 % average drop in multi-turn (Laban et al. 2025) [S26]; Lost in the Middle [S27]; MAST FM-1.4 "loss of conversation history" [S28] | agreement without correctness (MEASURED) | C (the token survives compaction) | the compaction itself is not detected; only its effect on the cited value | by design |
| F8 | **wrong place** (name over coordinates; exonyms; axis order) | `/v1/ask` with explicit coordinates answered from the town point 596 m away, NDVI 0.2824 vs 0.4237 at the field cell, same 30 Sep scene (MEASURED, LIVE `p6ewjnlq`); Piccadilly Circus → a locality in the ACT; Milan → Colombia; Seoul → a village in Côte d'Ivoire (SPEC, `CHANGELOG.md:241-252`); `[12.96, 77.58, …]` read as a box of 64° latitude (`:699-703`) | MaxMind default point: more than 600 million IPs mapped to one Kansas farm [S29]; GDAL 3 axis order (RFC 73) [S30]; WikToR ambiguity (Lima, Peru / Ohio / Oklahoma) [S31] | 596 m is 8.4 × the 71 m spacing emem says cannot miss a 0.5 ha clearance (INFERRED from `CHANGELOG.md:56`) | E (cell binding) | a wrong geocode signed as the entity's cell passes everything (→ F16) | geocoder fixes shipped (SPEC); `/v1/ask` coordinates: open as of 30 Sep 22:44Z (MEASURED file) |
| F9 | **missing data signed as a measurement** | EUDR plot across a 3° or 10° tile line "signed the far side's out-of-image pixels as 0: a forest-2020 of 0 or a loss year of 0, a pass" (SPEC, `CHANGELOG.md:53`); Overpass HTTP 200 + `remark` signed "not protected"; FIRMS searched a 1972 window and a 20 m box; NASA POWER −999 (`:11,60`); MCD64A1 −2 read as a burn day (`:62`) | Hansen `lossyear` 0 = "no loss" [S18]; Overpass returns HTTP 200 on out-of-memory (overpass-turbo #176) [S32]; NASA POWER fill −999 [S33]; FIRMS "data do not provide any information on cloud cover or missing data" [S34] | false EUDR pass (SPEC mechanism; prevalence UNVERIFIED); "no fire" from a malformed query (SPEC) | I (re-read shows off-tile); signed Absence with a reason | upstream-error paths unsigned (defect 8); `reason_cid` hashes prose (defect 9) | fixed per connector (SPEC) |
| F10 | **units and scale** | WorldPop signed people per pixel, "1.77x low at Paris"; SoilGrids clay/sand labelled g/kg, nitrogen cg/kg (SPEC, `CHANGELOG.md:61`) | Mars Climate Orbiter lost: "failure to use metric units in the coding of a ground software file" [S35]; SoilGrids mapped units need a conversion factor [S36] | 1.77 × population error (SPEC) | H (recompute from signed inputs); `valid_range` refused at signing (`:47`) | a wrong unit inside a trusted signer's derivation passes F | fixed (SPEC) |
| F11 | **unstable identity** (same data, different name) | polygon mean order-dependent, "an unstable mean means an unstable `fact_cid`" (`CHANGELOG.md:728-730`); re-minting gives a new `derivation_cid` for identical pixels (defect 18); read tools sign and store (defect 29) | floating-point "associative laws of algebra do not necessarily hold" (Goldberg) [S37]; GEE `bestEffort` silently uses a larger scale [S38] | two agents hold different tokens for one field; false disagreement (SPEC) | D (different cid is visible) | the cause (order, scale) is not | partly fixed (SPEC) |
| F12 | **truncated result read as complete** | `memory_view` of 135 notes returned 3 (`CHANGELOG.md:803-807`); whitepaper 93,945 bytes "through a transport that truncates silently" (`:723-724`); cursor bug read 322 entries of 150 notes (`:26`) | Claude Code caps MCP output at 25,000 tokens by default [S39]; MAST FM-2.4 "information withholding" [S28] | an agent concludes "only 3 notes" (SPEC) | C (resolving one reference is not truncated); `_kept`/`_len` | an agent that does not read `_len` | fixed (SPEC) |
| F13 | **copies counted as corroboration** | 7 identical re-signings counted as 7 attestations (defect 5; MEASURED: `contra_bengaluru.json` "8 disagreeing attestation(s)" from one key); "independent witnesses" = one Vortx-run domain + 109 key-only keys (defects 1, 30) | LLM conformity in multi-agent settings (Weng et al., ICLR 2025) [S40]; emem's own reading: "correlated error, not independent convergence" (`paper-section-statistics-and-threats.md:150-155`) | 3/36 agreeing pairs with 0/72 right (MEASURED) | F/G expose keys; a receiver can count distinct keys and operators | independence of keys is not provable from keys | open (defects 1, 5, 30) |
| F14 | **a verifier that passes what it did not check** | `/verify` "showed a green pass for a CID whose signature was never checked, and its CDN fallback asked the signer to vouch for itself" (`CHANGELOG.md:735-736`); guard with `text` instead of `texts` returns `allow` (defect 13); rasterset step never checks (defect 23); recall receipt Merkle proof covers only `fact_cids[0]` (defect 19; MEASURED: 8 cids, `path: []`) | Apple CVE-2014-1266 "does not check the signature" [S41]; Windows CVE-2020-0601 ECC validation [S42]; MAST FM-3.2/3.3 verification failures "appear frequently even in successful runs" [S28] | every rung above is void if the verifier lies (INFERRED) | receiver-side re-hash with stock libraries (10 client paths, `01_v12_state.md` §6.2) | a verifier bug in the receiver's own code | partly fixed (SPEC) |
| F15 | **data read as instructions** | agent-authored memory is "untrusted third-party text inside a trusted channel"; `_content_is_data_not_instructions` added (`CHANGELOG.md:713-716`); MCP `initialize` text said nothing on it (`:237-239`) | indirect prompt injection (Greshake et al. 2023) [S43]; MCP spec: "clients MUST consider tool annotations to be untrusted unless they come from trusted servers" [S44] | an agent acts on a note's instruction (SPEC) | F (who wrote it) | whether the text is true or benign | marked (SPEC) |
| F16 | **entity referent** (the right record of the wrong thing) | "Maasvlakte ramp 7" → OSM relation 1411107 (LIVE: `boundary=administrative`, `admin_level=10`, `name=Maasvlakte`), about 12 × 10 km (defect 21); three entities for Mount Fuji in Colfax, Wisconsin carried the Japanese volcano's bbox (`CHANGELOG.md:36`); road bands counted footways (`:28`) | toponym ambiguity (Gritta et al. 2018) [S31]; EUDR asks for polygons above 4 ha, at least six decimals [S45] | the measurement is right and about the wrong place (INFERRED) | none (R1 M17 accepted at every level) | always | out of scope by design |
| F17 | **product truth and model domain** | `agb_ndvi_powerlaw@1` (pan-tropical) applied at 3,900 m in the Himalaya (defect 16); a 92-95 % triple-consensus accuracy with no evaluation (defect 17) | GFC2020 V2: forest user accuracy 82 % (commission 18 %) [S46]; V3 commission 13.1 % [S19]; JRC: the maps are "non-mandatory, non-exclusive, and non-legally binding" [S19] | a signed, re-readable, wrong product value (INFERRED) | none | always | out of scope by design |

---

## 3. The classes in detail

Each class: (a) mechanism, (b) outside emem, (c) consequence, (d) what detects it and what does not.

### F1. The wrong pixel: the right record, the wrong pixel

**(a) Mechanism.** A raster point read converts (lat, lng) to a fractional pixel position and must pick the pixel that
contains it. On a PixelIsArea raster pixel k spans [k, k+1), so the containing pixel is the floor. emem's
`cog::world_to_pixel` rounded, "so any point in the right or lower half of a pixel read its south-east neighbour; GDAL
takes the floor. Every COG-backed band (Hansen, JRC GFC2020 and TMF, WorldCover, Cop-DEM, CCI biomass, Sentinel scenes,
and the hand-rolled DMSP-OLS and Köppen readers) did this from the first commit" (SPEC, `CHANGELOG.md:68`). Current code
floors with an epsilon for PixelIsArea and rounds for PixelIsPoint (MEASURED, `crates/emem-fetch/src/cog.rs:128-143`). A
second, related bug: Sentinel-2 raster headers "named its corner, half a pixel off", and the SCL cloud mask "was a pixel
off at cloud edges" (SPEC, `CHANGELOG.md:59`). The signer signed exactly what it read, so hash, signature, log and even
recompute from the signed DNs all pass.

emem incident, MEASURED:
- 162 of 200 sampled pre-fix records (200 cells, 164 scenes, 19 bands, signed 2026-05-14 to 2026-09-27) match the
  rounded pixel and 0 the floor; in the other 38 both rules pick the same pixel. Wilson 95 %: 75.0 to 85.8 %. Post-fix:
  0 of 54 (`research/repro/data/v8/prevalence_summary.json`). The post-fix sample is all Planetary Computer and two days
  wide, so provider and fix are confounded (`01_v12_state.md` §6.1).
- Error where the rules differ: index median 0.027, p90 0.113, max 0.301 (n 121); reflectance median 0.0097, max 0.120
  (n 41); SCL class changed in 4 of 198 records (same file).
- Keylong 25 Sep: containing pixel NDVI 0.4709 (DN B08 3502, B04 1900), rounded pixel 0.3016 (2720, 1923)
  (`pixel_check.json`).
- The pre-fix 23 Sep record, LIVE today: `GET /v1/facts/kxjvfwpa7grmfhkxoxufq5xjltq2s5syer2rzdx7odbnrxhnjzkq` returns
  value 0.34435, DNs [2993, 1972], offset −1000, `signed_at` 2026-09-25T19:35:27Z, source = the S2C 23 Sep B08/B04 COG
  URLs. The containing pixel reads 3605/1901, NDVI 0.4860.
- Spurious change: pre-fix 23 Sep (0.3444) to post-fix 25 Sep (0.4709) = +0.127; containing pixels 0.4860 to 0.4709 =
  −0.015 (MEASURED arithmetic on the DNs above).
- The 27 Jan 2022 record `2dpnuf4e…` (signed 2026-07-16) carries DNs 3034/3344; re-read today, those are the rounded
  pixel of `S2A_43SFS_20220127_1_L2A`; the containing pixel is 5900/6195. NDVI −0.0486 signed vs −0.0244 (MEASURED,
  section 4.4).
- Rondônia EUDR grid (section 4.3): different pixel at 79/100 (Hansen) and 82/100 (GFC2020), loss year changed at 7,
  tree cover at 21 (median |Δ| 8 points, max 97), GFC2020 class at 1, EUDR flag count 3 → 3.

**(b) Outside emem.**
- GDAL RFC 33 (fixing PixelIsPoint interpretation): GDAL had "treated this flag as having no relevance to the
  georeferencing"; after the fix "Interpretation of the raster space from the GeoTIFF tie points will be offset by half a
  pixel in the PixelIsPoint case"; "This change will alter the apparent georeferencing of all GeoTIFF files with
  PixelIsPoint set", and files written earlier "will now be interpreted differently and the values will be off by half a
  pixel". `GTIFF_POINT_GEO_IGNORE` restores the old behaviour [S1]. SPEC.
- rasterio discussion #2478 (10 Jun 2022, unanswered): a user asks why `index()`/`rowcol()` default to `math.floor`
  rather than rounding, arguing `index()` should invert `xy()` [S2]. The rounding intuition emem's reader followed is
  the intuition this user brings. SPEC.
- rasterio issue #2205 "Merge is prone to off-by-one pixel errors" (opened 11 Jun 2021 by the maintainer, closed) [S3].
  SPEC.
- Copernicus DEM on AWS: "Original tiles share one row or column with neighboring tiles … We removed these shared rows
  and columns on east and south edges"; "In original files, this is the northing of the center of the bottom-most
  pixels, while in our files … the center of the new bottom-most pixels is one pixel-length (resolution) away to north"
  [S4]. One product, two distributors, two grids. SPEC. emem's own fix list includes "Cop-DEM's ~15 m tile-edge strips
  now read the neighbouring tile" (`CHANGELOG.md:60`).
- Townshend et al. 1992, IEEE TGRS 30(5):1054-1060: misregistration of one pixel induced an error "greater than 50% of
  the actual differences in the NDVI" over densely vegetated areas; a registration accuracy better than one-fifth of a
  pixel was needed for change-detection error below 10 % [S5]. SPEC (abstract as indexed; DOI 10.1109/36.175340
  confirmed via Crossref).
- Sentinel-2: multi-temporal registration of refined products is specified at 0.3 pixel (2σ); a Global Reference Image
  refinement is used since 2021 [S6]. SPEC. INFERRED: the reader rule moved emem's reads by 0 or 1 pixel, more than three
  times the mission's co-registration budget.

**(c) Consequence.**
- Irrigation (synthetic R3 rule, irrigate iff NDVI ≤ 0.4705): 0.4709 "hold" becomes 0.3016 "irrigate" (MEASURED values;
  the rule is the experiment's, not an agronomic standard). Applying Kamble et al. 2013 (Kc = 1.457 NDVI − 0.1725,
  calibrated on MODIS and AmeriFlux crops) [S47]: Kc 0.514 vs 0.267, a 48 % lower crop water estimate (INFERRED; the
  relation is not calibrated for Keylong or Sentinel-2 and is shown only for scale).
- Change detection (EUDR, disaster mapping, MRV all difference two dates): a reader fix between two dates produced a
  +0.127 NDVI step where the ground changed by −0.015 (MEASURED).
- EUDR: at Rondônia the rule changed 7 loss years and 1 forest class among 100 points and no flag (MEASURED). INFERRED:
  points near forest edges and plots straddling class boundaries are where a one-pixel error changes a verdict; this
  grid is not a prevalence estimate for EUDR plots.

**(d) Detection.** Only level I (re-read the containing pixel from the named COG) stops it; leave-one-out "without I:
M15" (`research/repro/v11/out/summary.md`). What makes I possible is in the record: scene id, COG URLs, the point,
the DNs, and since 2026-09-28T12:23:14Z the reader stamp `reader=cog-pixel-floor@2`; pre-fix records are identified by
`signed_at` before 2026-09-28T04:09:26Z (SPEC, `CHANGELOG.md:47`). Old records are not rewritten; they stop answering
"latest" (`:54`). Undetected: a receiver that stops at H; a pre-fix token already handed to a third agent.

### F2. Radiometric convention: the same pixel on three scales

**(a) Mechanism.** From processing baseline 04.00 (25 Jan 2022) ESA L2A reflectance is
`(L2A_DN + BOA_ADD_OFFSET) / QUANTIFICATION_VALUE` with BOA_ADD_OFFSET −1000 (SentiWiki S2 Products [S7]). Catalogues
differ: Planetary Computer serves ESA DNs; Element84 subtracts 1000 before publishing and flags the item; GEE offers a
HARMONIZED collection. Because NDVI cancels a shared scale but not a shared offset, a 1000 DN error on both bands moves
NDVI. emem's code says so: "A +1000 DN offset on both bands biases NDVI toward zero by roughly a third at typical canopy
reflectance. The bias is smooth, plausible-looking, and invisible without a reference" (SPEC,
`crates/emem-fetch/src/stac.rs:176-182`); the value path now applies 0 for Element84, −1000 for MPC from baseline 04.00,
and refuses an MPC item with no stated baseline (MEASURED code, `crates/emem-api-rest/src/lib.rs:51714-51747`).

emem incident: defect 14 asked whether a 2022 Element84 v0 record was offset-correct. Answered today (section 4.4): the
v0 item states `sentinel:boa_offset_applied: true`, so offset 0 was right; the record's error is F1, not F2. Residual
(MEASURED): emem treats every Element84 v1 item as harmonised (`s2_dn_is_harmonised`, `stac.rs:186`) and does not read
the per-item flag (`git grep -i boa_offset_applied origin/main` returns nothing), while Element84's README says the
offset "has been applied to some of the Items" [S13a].

**(b) Outside emem.**
- ESA STEP forum, 25 Mar 2022: PB 04.00 L1C and L2A "now contain an Offset in the metadata … At L2A, RADIO_ADD_OFFSET
  = -1000" [S9a]. Users, Jun to Aug 2022: values "approximately 0.1 higher"; a B2 of 1069 (2022) vs 234 (2021) "making
  direct comparison problematic"; Aug 2024: NDVI "still lower than before years" after correcting [S9]. SPEC.
- Sinergise / Planet community, 26 Apr 2024: "NDVI range for 2022 is less around 0.1-0.2 compare to the previous years
  (2019-2021)" across Brazil and USA [S10]. SPEC.
- GEE: "After 2022-01-25, Sentinel-2 scenes with PROCESSING_BASELINE '04.00' or above have their DN (value) range shifted
  by 1000. The HARMONIZED collection shifts data in newer scenes to be in the same range as in older scenes" [S8].
  SPEC (fetched).
- DPIRD-DMA/S2Mosaic PR #9, merged 30 Sep 2026: "MPC serves those DNs unchanged, and S2Mosaic passed them through";
  mosaics across Jan 2022 mixed scales, means and medians "pulled up by up to 1000 DN" [S11]. SPEC.
- franciscoparrao/surtgis PR #146, merged 30 Sep 2026: Planetary Computer DNs made composites "read 1000 DN too high"
  [S12]. SPEC.
- Element84 earth-search discussion #26: for the Collection-1 preview "we have decided not to apply scale or offset"
  (8 Dec 2023) [S13b]. One provider, two collections, two conventions. SPEC.
- **Element84 metadata, LIVE today** (`/v1/search`, Keylong point, 20 to 30 Sep 2026, 5 items): every item has
  `earthsearch:boa_offset_applied: true` and red `raster:bands` `{"scale": 0.0001, "offset": -0.1}`. DNs at the Keylong
  pixel equal MPC minus 1000 (section 4.2). The flag and the band metadata disagree; the DNs follow the flag.
- UNVERIFIED (search index only, page 404 today): Khadra-AI/thuraya-experience PR #109 "stop subtracting the Sentinel-2
  BOA offset twice" and issue #110 "Rebake the Hajar ground maps with the corrected Sentinel-2 offset".

**(c) Consequence.** At one Keylong pixel on 25 Sep (MEASURED DNs, INFERRED arithmetic): 0.4709 correct; 0.2966 if MPC
DNs are read without the offset (decision flips); 1.1427 if Element84 DNs are read with Element84's declared −0.1
(impossible; a range check catches it); for the S2B scene of the same day, 0.9825 (inside [−1, 1], no range check
catches it). A series that mixes conventions shows a step at 25 Jan 2022 (SPEC, [S10], [S11]).

**(d) Detection.** H: recompute NDVI from the signed DNs with the signed offset (emem records catalogue and offset in
`derivation.args`, e.g. `oj5cecci…` ends `["https://planetarycomputer.microsoft.com/api/stac/v1/search", -1000.0]`,
LIVE). I: re-read the pixel and take the baseline from the product id (`N0513` in the source URL). Forged offset with
re-hash: F (M12). Undetected: a trusted signer that records a wrong offset and a wrong value consistently passes F and G;
only H against an independent rule, or I, catches it.

### F3. Date or scene substitution: asked 23 Sep, got 25 Sep

**(a) Mechanism.** A tool asked for a date returns a scene from another date, or another scene from the same date,
without saying so. emem `band_raster` with `observed_on` builds a window of target ± 30 days capped at now and returns
the first item of a STAC search sorted `properties.datetime desc`, with `max_scenes = 1` (MEASURED code:
`band_raster.rs:221-238`, `lib.rs:51499-51543`, `lib.rs:52247-52290`, `stac.rs:405-419`). That is the newest scene under
the cloud tier, not the nearest; the `BandCubeReq` docs say "nearest scene" (defect 34). Recall without a date returned
a 2022 scene rather than the 2026 one (defect 15).

emem incident, MEASURED (`research/repro/data/v9/rawband/results.md`, pre-registered, n = 10, claude-sonnet-5-5):
`observed_on` 2026-09-23 (also 09-22, 09-21) returned the byte-identical 25 Sep S2A raster with no warning; the 23 Sep
S2C scene exists (20 % cloud). 9 of 10 runs had no 23 Sep band values; 9 of 10 noticed both dates were one scene; 3 of 10
wrongly suggested or claimed no 23 Sep acquisition existed; 6 of 10 wrote "no material change", 5 of them self-declared
placeholders. Only trial 8 (via recall and backfill) measured ΔNDVI −0.015.

New, MEASURED today (section 4.2): two acquisitions cover the pixel on 25 Sep, S2A relative orbit 005 (10.8 % cloud) and
S2B relative orbit 105 (1.6 % cloud): NDVI 0.4709 and 0.4370. Both fall in tslot 20721 (`floor(unix/86400)`).

**(b) Outside emem.**
- STAC API item search: the specification text contains no default ordering; ordering is an extension (`sortby`)
  (MEASURED: `grep -n -i "sort\|order"` on `stac-api-spec/item-search/README.md` finds only the extension mention, line 257)
  [S14]. A client taking `items[0]` gets whatever the server's order gives.
- GEE `ImageCollection.mosaic()` "prioritizes the order of images from last to first in the collection" [S15]. SPEC.
- Sentinel-2 now flies three units (A, B, C), so one site can have two acquisitions on one day from different relative
  orbits, as here (MEASURED, E84 items).

**(c) Consequence.** A two-date change test that silently reads one scene twice reports "no change" (MEASURED, v9). The
same-day S2B value 0.4370 crosses the 0.4705 rule (INFERRED decision). For pre/post-event disaster mapping a
substituted pre-event scene reports no flood or no burn (INFERRED; no incident sourced).

**(d) Detection.** E (tslot binding) stops a different day (M5, M10). A same-day other scene passes E; it is stopped at C
only if B resolves the reference A cited (a different scene has a different fact CID), and by inspecting the scene id in
the record. The v9 run shows the limit: the records exposed the substitution to 9 of 10 agents; none could recover the
23 Sep values with the raster tool, and 3 invented an explanation. Status: open in code at 18adb67.

### F4. Silent source substitution and reprocessing: same name, other bytes

**(a) Mechanism.** The band name stays the same while the upstream product, version or processing run changes.

emem incidents:
- Bengaluru elevation, cell `defi.zb493.xuqA.zcb5f`, band `copdem30m.elevation_mean`: 918.0 m signed 2026-05-28 from
  `open_meteo_copdem90m@1` (Open-Meteo, Copernicus DEM GLO-90), then 915.0712 m from `copernicus_dem_30m_aws_pixel@1`,
  first signed 2026-08-11, re-signed 7 times; the contradiction scanner labels it `same_attester_provider_substitution`
  (MEASURED, `research/repro/data/contra_bengaluru.json`, served 2026-09-29T22:05:30Z). Δ 2.93 m.
- Hansen v1.12 → v1.13 and GFC2020 V3 → V4: superseded facts "no longer answer 'latest' … Nothing signed is rewritten"
  (SPEC, `CHANGELOG.md:54-55`); the registry text said V3 while the connector read V4 (`:13`); facts now name the version
  in `sources[0].scheme`, e.g. `jrc.gfc2020.v4` (`:71-72`; LIVE on `ncupl5pt…`, whose `fn_key` is still
  `jrc_gfc2020_v3_pixel@1` with arg `v4` and URL path `/GFC2020/LATEST/`).
- `Source.hash` (hash of upstream bytes) is never filled on the Sentinel path (defect 25), so "which bytes" rests on the
  signer unless the pixel is re-read.
- New, MEASURED (section 4.4): the 27 Jan 2022 acquisition exists as two processing runs: Element84
  `…N0400_R005_T43SFS_20220127T083110` and Planetary Computer `…N0400_R005_T43SFS_20220212T103433`. At the containing
  pixel, DNs differ by 1300/1313 (about 0.03 reflectance beyond the offset); NDVI −0.0244 vs −0.0242.

**(b) Outside emem.**
- Open-Meteo elevation: "Data is based on the Copernicus DEM 2021 release GLO-90 with 90 meters resolution" [S48] (SPEC,
  fetched): the 918.0 m source is a 90 m product behind a band named for 30 m.
- Copernicus DEM: nine releases 2019_1 to 2024_1, including "2021_1 Jul-2021 Corrective Maintenance (Negative values
  correction)" and "Edge Error: Correction of inconsistencies within the overlapping posts of two neighbouring geocells";
  absolute vertical accuracy "< 4m (90% linear error)" [S20]. SPEC. INFERRED: Bengaluru's 2.93 m is within the stated
  accuracy; neither value is shown wrong; what matters is which one an agent cited.
- MODIS: "Terra forward LUT in C6 are incorrect for the period 2012 – 2017 because of error in generating the LUT at
  MCST, affecting bands 1 and 2" (NASA, MODIS C61 Land changes) [S16]. Bands 1 and 2 are red and NIR. SPEC.
- MODIS C5: "nearly a threefold difference in negative NDVI trends derived from Terra (17.4%) and Aqua (6.7%)",
  2002-2010, North America (Wang et al., RSE 119:55-61, 2012) [S17]. SPEC.
- Hansen GFC v1.13: "The reprocessing of data from 2011 onward in measuring loss … However, the years preceding 2011 have
  not yet been reprocessed in this manner, and users will notice inconsistencies as a result"; "integrated use of
  version 1.0 2000-2012 data and updated version 1.13 2011-2025 data should be performed with caution" [S18]. SPEC.
- JRC GFC2020 V2 → V3 (V3 dated 28 Nov 2025): "a global decrease in forest cover in V3 … In South America, forest cover
  declines by more than 20% in the Caatinga and Cerrado biomes"; "a 5–20% decrease … in boreal regions" (JRC146622,
  2026) [S19]. SPEC.
- Sentinel-2 Collection-1: products reprocessed to baseline 05.00 (2015 to 2021) and 05.10 (2022 to 13 Dec 2023) (CDSE,
  2 Sep 2024) [S21]; Element84 issue #68 (15 May 2025, open): `sentinel-2-c1-l2a` contains baseline 5.09 scenes "which
  ESA defines as not part of collection 1" [S21b]. SPEC.

**(c) Consequence.** EUDR uses forest at 31 Dec 2020 as its baseline (SPEC, [S45]); a plot read as forest under GFC2020 V2
can be non-forest under V3 in the Cerrado, which changes whether loss counts as deforestation (INFERRED from [S19]).
MODIS-based trend studies over 2012-2017 inherited a red/NIR calibration error (SPEC [S16]).

**(d) Detection.** The record names scheme, version, `fn_key`, product id and `captured_at`, so C/E show which source a
value came from, and as-of recall returns what was cited before a newer source arrived (Bengaluru: 918.0 m as of 15 Jun).
Undetected: whether the upstream product is right (inherited, L3 partial) and which bytes were read while `Source.hash`
is empty.

### F5. Stale state presented as current; history rewritten

**(a) Mechanism.** "Latest we hold" is read as "now"; or a newer value replaces the one an agent cited, so the earlier
agent looks wrong. emem: "`current_by_band` means 'the newest we hold', never 'fresh', and nothing said so. Asked what is
happening in London right now, this responder answers partly from bands 87 days old" (SPEC, `CHANGELOG.md:188-191`);
`cost.source_freshness_s` "was the literal `0`, so a Copernicus tile captured in April 2021 was served as 0 seconds old"
(`:691-694`).

**(b) Outside emem.** Navigation analog, not EO: the family of Philip Paxson sued Google after he followed Google Maps over
a bridge in Hickory, North Carolina that had partly collapsed in 2013; he died on 30 Sep 2022; the complaint says a
resident reported the bridge via "suggest an edit" in Sep 2020 (Washington Post, CNN, 21 Sep 2023) [S22]. SPEC.

**(c) Consequence.** A value cited in June (918.0 m) and checked in October against the current one (915.07 m) makes the
June agent look wrong unless the check is as-of (M20, INFERRED).

**(d) Detection.** E (tslot) for a stale slot presented as current (M5); G (log inclusion) for a version shown only to B
(M16); as-of recall for "what was known then". Known gaps: `as_of_signed_at` compared as a raw string (defect 35, code
read); `recall` with `as_of_signed_at` and no tslot timed out at 40 s on a busy cell (defect 2).

### F6. Paraphrase and rounding at a threshold

**(a) Mechanism.** The value is retyped, rounded or summarised on its way from A to B. Near a decision threshold, two
digits are enough to flip the decision.

emem incident, MEASURED (`research/repro/data/v8/results.json`, B = claude-haiku-4-5): token arm 10/10 HOLD (correct),
full-precision prose 10/10, prose rounded to "0.47" 0/5 correct (5/5 IRRIGATE; exploratory, Fisher one-sided T vs R
p = 0.00033), forged cell 5/5 DECLINE. emem's own draft checker "judges at the writer's own precision", so "≈ 0.49" passes
for 0.4871 (SPEC, `research/audit_v11/poster_evidence_audit.md` A88, C12).

**(b) Outside emem.** Zhao, Cohen and Webber (Findings of EMNLP 2020) build a verifier because summaries hallucinate
quantities ("dates, numbers, sums of money") [S23]. Perez et al. (2024, revised Jan 2026): in iterated LLM transmission
"small biases, negligible at the single output level, risk being amplified" and content evolves "towards attractor
states" [S24]. SPEC.

**(c) Consequence.** A flipped irrigation decision at a 0.0004 margin (MEASURED in the experiment; rule synthetic).

**(d) Detection.** C: B resolves the reference and reads the 16-digit value; nothing else is needed. Undetected: nothing,
once the reference is resolved. Cost: 46 cl100k tokens for the token vs 8 for the bare value (MEASURED,
`token_counts.json`).

### F7. Compaction and shared lossy memory: agreement without correctness

**(a) Mechanism.** Context is summarised to fit; the summary drops or rounds the number; every agent that reads the same
summary inherits the same error and they agree with each other.

emem incident, MEASURED in emem's docs (pre-registered; Gemma-4-12B and Qwen2.5-7B, one host):
`compaction_pressure` 0/72 correct, 3/36 pairs agree, Fisher one-sided p = 0.035; `compaction_free` 20/72, 15/36,
p = 0.109; control 72/72, 36/36 (`docs/paper-section-statistics-and-threats.md:87-89`). emem's own caveat: "The compaction
result is correlated error, not independent convergence … Gemma wrote every summary, so the writer is a confound"
(`:150-155`). Defect 28: README prints a different pair of numbers that does not reproduce p = 0.035.

**(b) Outside emem.** Anthropic's compaction docs: "Compaction replaces the older turns of a conversation with a summary"
and offer a custom prompt "when the default summary drops something a later turn needs" [S25]. Laban et al. 2025: "an
average drop of 39% across six generation tasks" in multi-turn vs single-turn, 200,000+ simulated conversations [S26].
Liu et al., TACL 12:157-173 (2024): performance "significantly degrades when models must access relevant information in
the middle of long contexts" [S27]. MAST (Cemri et al. 2025, 1600+ traces, 7 frameworks, 14 failure modes, κ = 0.88)
lists FM-1.4 "Loss of conversation history" [S28]. SPEC.

**(c) Consequence.** A reviewer who uses agreement between agents as evidence accepts 3 agreeing pairs when none of 72
answers is right (MEASURED).

**(d) Detection.** C: a reference survives compaction because it is copied, not summarised. Undetected: the compaction
itself; a summary that drops the reference altogether.

### F8. Wrong place: the place name wins over the coordinates

**(a) Mechanism.** A question names a place and gives coordinates; the system geocodes the name and answers for the
geocoder's point. Or a bounding box is read in the wrong axis order.

emem incidents:
- `/v1/ask` with "What is the NDVI at Keylong, Lahaul (32.57126 N, 77.03448 E)?" resolved to the town point
  (32.5717891, 77.0281479), cell `defi.zb572.xAnI.zb1a2`, served 2026-09-30T22:44:27Z (MEASURED,
  `research/repro/data/v11/ask_keylong.json`). Haversine distance 596 m (MEASURED). The answer's fact `p6ewjnlq…` (LIVE):
  NDVI 0.2824, S2C 30 Sep scene, DNs [3688, 2504]. The field cell on the same scene reads 0.4237 (E84 DNs 2505/1014,
  MEASURED).
- Geocoder fixes (SPEC, `CHANGELOG.md`): "Milan answered from Colombia and Calcutta from South Africa; asking about Seoul
  returned a village in Cote d'Ivoire" (`:241-243`); "Piccadilly Circus" resolved "to a locality in the Australian Capital
  Territory: every reading that followed was a correct measurement of rural Australia" (`:249-254`); "how green is the
  area around Nashik right now…" resolved "to an artwork in Georgia" (`:797-801`); `"DROP TABLE facts"` resolved to "La
  Table Ronde, France" (`:707-708`).
- Axis order: `polygon_bbox` `[12.96, 77.58, 12.99, 77.61]` "bound `max_lat = 77.58`: a box spanning 64 degrees of
  latitude. Small mis-orderings returned confident facts about the wrong region" (`:699-703`).

**(b) Outside emem.** MaxMind's default point for US IP addresses without a known location (38°N 97°W) put "more than
600 million IP addresses" on one farm in Potwin, Kansas; reported by Kashmir Hill (Fusion) in April 2016; lawsuit,
settled 2017 [S29]. GDAL 3.0 (RFC 73): coordinates follow the CRS axis order, "latitude first, longitude second for
geographic CRS belonging to the EPSG authority" [S30]. Gritta et al. 2018 (LRE 52:603-623) evaluate toponym resolution on
ambiguous names such as Lima, Peru / Lima, Ohio / Lima, Oklahoma [S31]. SPEC.

**(c) Consequence.** At Keylong the wrong place returned 0.2824 where the field reads 0.4237 on the same scene (MEASURED).
EUDR asks for geolocation with at least six decimal digits and polygons above 4 ha [S45]; 596 m is 8.4 times the 71 m
sample spacing that emem states cannot miss a 0.5 ha clearance (`CHANGELOG.md:56`) (INFERRED).

**(d) Detection.** E: the cell is part of the record; B compares it with the cell it asked about (M4, M9; live 409 on a
relabelled token per `02_experiment_design.md:219`). Undetected: a geocoder error that becomes the entity's identity
(F16). Status of the `/v1/ask` coordinate path after 30 Sep: UNVERIFIED (not called, per the read-only rule).

### F9. Missing data signed as a measurement

**(a) Mechanism.** No data, an error or an off-image read becomes a value (0, "none", "not protected") and is signed.

emem incidents (SPEC, `CHANGELOG.md` [2.4.2] and [Unreleased]):
- "A plot across a 3° (WorldCover) or 10° (Hansen, GFC2020) tile line read only the centre tile and signed the far side's
  out-of-image pixels as 0: a forest-2020 of 0 or a loss year of 0, a pass. A pixel off its tile is now an error, not a
  zero" (`:53`).
- "Overpass's own failures (HTTP 200 with a `remark`) no longer sign 'not protected'; FIRMS searched a 1972 window on
  every call and a 20 m box, now the day and 500 m"; RADD, WRI GDM and OPERA "sign nothing when the connector is not
  built" (`:60`).
- NASA POWER fill −999 inside the publication window was a signed Absence (`:11`); "MCD64A1 Burn_Date -2 (water) is not
  a burn day"; Sentinel-2 northern-zone tiles reaching ~10 km south of the equator "fell off the image" (`:62`).
- Open: upstream-error and "no S2 scene" paths unsigned (defect 8); `reason_cid` hashes prose, not the upstream response
  (defect 9).

**(b) Outside emem.** Hansen GFC: `lossyear` "Encoded as either 0 (no loss) or else a value in the range 1-20 [sic]",
and `datamask` 0 = no data; tiles are 10 × 10 degrees [S18]. A 0 read off the tile is the code for "no loss". Overpass:
an out-of-memory query returned HTTP 200 with empty data (overpass-turbo #176, 3 Jul 2015) [S32]. NASA POWER uses −999
as its fill value [S33]. NASA FIRMS: "the data do not provide any information on cloud cover or missing data"; detection
"beneath the tree canopy is unknown, but likely to be very low" (Earthdata Forum, 13 Feb 2024) [S34]. SPEC.

**(c) Consequence.** EUDR: a false "no loss" on the far side of a tile line is a false pass (SPEC mechanism; how many
plots were affected is UNVERIFIED). INFERRED geography: Rondônia spans about 8° to 13.7° S, so the 10° S Hansen/GFC2020
tile line crosses it. Fire response: "no fire detected" from a 1972 query window says nothing about today (SPEC).

**(d) Detection.** I: a re-read shows the point is off the tile. A signed Absence with an upstream-response hash would make
the reason checkable; defect 9 says the current `reason_cid` hashes prose. Signatures do not help: the wrong 0 was signed.

### F10. Units and scale

**(a) Mechanism.** A value is right in one unit and labelled or used in another.
emem (SPEC, `CHANGELOG.md:61`): "WorldPop signs people per km² (the count over the pixel's own area; it signed people per
pixel, 1.77x low at Paris)"; "SoilGrids clay and sand are %, nitrogen g/kg (they were labelled g/kg and cg/kg)".

**(b) Outside emem.** Mars Climate Orbiter Mishap Investigation Board, Phase I report, 10 Nov 1999: "the root cause for the
loss of the MCO spacecraft was the failure to use metric units in the coding of a ground software file, 'Small Forces',
used in trajectory models"; and "the root cause was not caught by the processes in-place in the MCO project" [S35].
ISRIC SoilGrids: mapped units (e.g. clay g/kg) are converted to conventional units (%) by dividing by a per-property
conversion factor (10 for clay) [S36]. SPEC.

**(c) Consequence.** Population per km² 1.77 × low at Paris (SPEC). Spacecraft lost (SPEC, analog).

**(d) Detection.** H: recompute from signed inputs (M14 in R1 is the WorldPop-shaped case); a published `valid_range` per
band refused at signing (`CHANGELOG.md:47`). M18 (unit relabelled, re-hashed) is caught by F
(`02_experiment_design.md:242`). Undetected: a consistent unit error inside a trusted derivation whose inputs are not
signed.

### F11. Unstable identity: the same data under two names

**(a) Mechanism.** Re-deriving the same data yields a different identifier, so two agents holding the same observation
look as if they disagree. emem: "Polygon aggregates were order-dependent: `JoinSet` yields in completion order, so the
same query signed a slightly different mean each call, and an unstable mean means an unstable `fact_cid`" (SPEC,
`CHANGELOG.md:728-730`); re-minting a raster or cube gives a new `derivation_cid` for identical pixels because
`signed_at` is hashed (defect 18); read tools sign and store, so concurrent agents see different cids for the same values
(defect 29; observed in v9: trials 9 and 10 cited CIDs created by trial 8).

**(b) Outside emem.** Goldberg: "Due to roundoff errors, the associative laws of algebra do not necessarily hold for
floating-point numbers" [S37]. GEE `reduceRegion(bestEffort=true)`: "If the polygon would contain too many pixels at the
given scale, compute and use a larger scale which would allow the operation to succeed" [S38]: the same call can be
computed at a different scale without an error. SPEC.

**(c) Consequence.** False disagreement between agents and non-independent experiments (SPEC, defect 29).

**(d) Detection.** D makes the difference visible (different cid). It does not say why. Status: aggregate order fixed;
defect 18 open.

### F12. A truncated result read as complete

**(a) Mechanism.** A transport or page limit cuts a result; the reader treats the remainder as the whole.
emem (SPEC): `memory_view` on an attester with 135 notes "returned three entries and a caller could not tell that from
'this agent wrote three notes'" (`CHANGELOG.md:803-807`); `whitepaper.md` "was 93,945 bytes against 24,000, through a
transport that truncates silently" (`:723-724`); a cursor that pointed back into page one: "The channel builder read 322
entries of 150 notes and missed others" (`:26`); witness list truncation "nulled fields the tool's own schema requires"
(`:118`).

**(b) Outside emem.** Claude Code: "the default maximum is 25,000 tokens" for MCP tool output; over the limit it saves the
result to a file and replaces it with a message [S39]. MAST FM-2.4 "Information withholding" [S28]. SPEC.

**(c) Consequence.** An agent's census or audit misses records (SPEC).

**(d) Detection.** C: a single reference resolves to one bounded record; responses now carry `_kept`, `_len`,
`_next_offset`. Undetected: a reader that ignores those fields.

### F13. Copies counted as corroboration

**(a) Mechanism.** Several records from one source are counted as independent confirmations.
emem: "7 identical re-signings count as 7 attestations" (defect 5). MEASURED in `contra_bengaluru.json`: the hint reports
"8 disagreeing attestation(s)"; all 8 have one attester key (`777er3yi…`) and 7 carry the same value 915.0712. "Co-signed
by independent witnesses" vs one independent operator domain run by Vortx AI plus 109 key-only keys (defects 1, 30).

**(b) Outside emem.** Weng et al., "Do as We Do, Not as You Think: the Conformity of Large Language Models", ICLR 2025
(BenchForm; conformity rate as a function of majority size) [S40]. emem's own reading of the compaction run:
"correlated error, not independent convergence" (`paper-section-statistics-and-threats.md:150`). SPEC.

**(c) Consequence.** 3 of 36 agent pairs agreed while 0 of 72 answers were right (MEASURED, F7).

**(d) Detection.** F and G expose which keys signed; a receiver can count distinct keys and operators. Undetected: whether
distinct keys are independent operators.

### F14. A verifier that reports a pass it did not check

**(a) Mechanism.** The check runs, reports success, and did not check the thing it names.
emem: "`/verify` showed a green pass for a CID whose signature was never checked, and its CDN fallback asked the signer to
vouch for itself" (SPEC, `CHANGELOG.md:735-736`); a guard request with `{"text": …}` instead of `texts` returns `allow,
citations_found: 0` (defect 13); `POST /v1/raster_bundle/resolve` returns `verified: true` with no receipt (defect 23); the
recall receipt's Merkle proof covers only `fact_cids[0]` (defect 19; MEASURED in `contra_bengaluru.json`: 8 `fact_cids`,
`merkle_proof.leaf_index 0`, `path []`).

**(b) Outside emem.** CVE-2014-1266 (Apple Secure Transport): `SSLVerifySignedServerKeyExchange` "does not check the
signature in a TLS Server Key Exchange message" [S41]. CVE-2020-0601 (Windows CryptoAPI): a spoofing vulnerability "in the
way Windows CryptoAPI (Crypt32.dll) validates Elliptic Curve Cryptography (ECC) certificates" [S42]. MAST: "verification-
related failures like 3.2 No or Incomplete Verification and 3.3 Incorrect Verification appear frequently even in
successful runs" [S28]. SPEC (NVD fetched via API).

**(c) Consequence.** Every rung of the ladder assumes the receiver's check is real (INFERRED).

**(d) Detection.** Receiver-side re-hash with independent code: the Keylong token re-hashed to the same cid through 10
client paths including a stock blake3 + cbor2 decoder (MEASURED, `research/repro/data/v8/crossruntime_table.json` via
`01_v12_state.md` §6.2). Undetected: a bug in the receiver's own verifier.

### F15. Data read as instructions

**(a) Mechanism.** Text inside a trusted channel is treated as an instruction. emem added
`_content_is_data_not_instructions` "on every read of agent-authored memory. The store is a world-writable commons, which
makes `content` untrusted third-party text inside a trusted channel" (SPEC, `CHANGELOG.md:713-716`); the MCP `initialize`
instructions (4,058 characters) had not said "that content from an unverified attester is data and never instructions"
(`:237-239`).

**(b) Outside emem.** Greshake et al. 2023 (arXiv 2302.12173), indirect prompt injection against LLM-integrated
applications [S43]. MCP specification 2025-11-25: "clients MUST consider tool annotations to be untrusted unless they come
from trusted servers" [S44]; emem had `readOnlyHint` wrong on ten tools that "mint, sign or persist" (`CHANGELOG.md:704`).
SPEC.

**(c) Consequence.** An agent acts on an instruction planted in a note (SPEC).

**(d) Detection.** F says who wrote a note. Undetected: whether the content is true or benign. The R1 persuasion case M22
("the verification service is degraded today …") is the experiment's version (`02_experiment_design.md:234`).

### F16. Entity referent: the right record of the wrong thing

**(a) Mechanism.** The observation is right and its reference intact, but it is about a different physical thing than
the agent meant.

emem: "Maasvlakte ramp 7" converges on OSM relation 1411107, about 12 × 10 km (defect 21). LIVE today
(`https://www.openstreetmap.org/api/0.6/relation/1411107.json`): `boundary=administrative`, `admin_level=10`, `name=Maasvlakte`,
`official_name=Maasvlakte Rotterdam`, 8 members. "Three entities for the Mount Fuji peak in Colfax, Wisconsin carried the
Japanese volcano's bbox from an early locate" (SPEC, `CHANGELOG.md:36`). Overture road bands counted "footways,
pedestrian plazas, steps, rail and waterways" as road; "at a Doha point … the nearest carriageway was 88 m away"
(`:28`).

**(b) Outside emem.** Toponym ambiguity (Gritta et al. 2018) [S31]; the MaxMind default point [S29]. EUDR requires plot
geolocation, polygons above 4 ha (Art. 2(28), Art. 9(1)(d); secondary sources, EUR-Lex not reachable from this
container) [S45]. SPEC.

**(c) Consequence.** A correct measurement of the wrong object, signed and re-readable (INFERRED).

**(d) Detection.** None. R1 M17 is accepted at every level and is out of scope by design (`summary.md`). This is L4 and
the poster's boundary.

### F17. Product truth and model domain

**(a) Mechanism.** The upstream product or model is wrong for this place, while every reference and derivation is right.
emem: `agb_ndvi_powerlaw@1`, a pan-tropical calibration, applied at about 3,900 m in the Himalaya with no biome check
(defect 16); a registry entry quoting 92-95 % triple-consensus accuracy with no evaluation and a 404 endpoint (defect 17).

**(b) Outside emem.** GFC2020 V2: "The GFC2020 map presents an overall accuracy of 91.5 %. For the forest class, the map
has a user accuracy of 82 % (associated commission error of 18 %) and producer accuracy of 91.8 %" (Bourgoin et al., ESSD
18:1331, 19 Feb 2026) [S46]. V3: overall 92.8 %, omission 10.6 %, commission 13.1 %; the maps are "non-mandatory,
non-exclusive, and non-legally binding sources of information" (JRC146622, 2026) [S19]. Carbon: West et al., Science
381(6660):873-877 (25 Aug 2023): across 26 REDD+ sites "most projects have not significantly reduced deforestation. For
projects that did, reductions were substantially lower than claimed" [S49] (an analog: a baseline error becomes credits;
a rebuttal exists, arXiv 2312.06793). SPEC.

**(c) Consequence.** A screen built on a product with 13 to 18 % forest commission error inherits it (SPEC).

**(d) Detection.** None by a reference protocol (L5). The record says which product and version produced the value, which
is what an accuracy statement can be attached to.

---

## 4. Measurements made for this report

### 4.1 Emem code at 18adb67 (MEASURED, `git -C /home/user/vortx-ai/emem show origin/main:<path>`)

| item | file:line | what it does |
|---|---|---|
| pixel rule | `crates/emem-fetch/src/cog.rs:128-143` | PixelIsArea: `floor(x + 1e-6)`; PixelIsPoint: `round` |
| scene choice for `band_raster` | `crates/emem-api-rest/src/band_raster.rs:221-238` → `lib.rs:51499-51543` | window target ± 30 d (tier 1), capped at now; returns the first item |
| candidate order | `lib.rs:52247-52290`; `crates/emem-fetch/src/stac.rs:405-419` | "newest first", `sortby properties.datetime desc`, `max_scenes = 1` |
| offset | `lib.rs:51714-51747`; `stac.rs:156-195` | E84 → 0; MPC → −1000 if baseline ≥ 04.00, 0 if older, refuse if absent; other catalogues refused |
| E84 per-item flag | `git grep -n -i "boa_offset_applied\|raster:bands" origin/main -- crates/` | no match |

### 4.2 Keylong pixel, all catalogues (MEASURED, rasterio 1.4.4, 2026-10-01)

Point 32.57125977099409 N, 77.03447748052537 E (the args of the signed records); tile 43SFS, EPSG:32643; containing pixel
row 9443, col 9098 (fractional 9443.5736, 9098.3273).

| item (Element84 v1 unless stated) | cloud % | B04 | B08 | NDVI | note |
|---|---|---|---|---|---|
| S2C 23 Sep, R005 (`S2C_43SFS_20260923_0_L2A`) | 20.0 | 901 | 2605 | 0.4860 | MPC: 1901 / 3605 (`pixel_check.json`) |
| S2A 25 Sep, R005 (`S2A_43SFS_20260925_1_L2A`) | 10.8 | 900 | 2502 | 0.4709 | MPC: 1900 / 3502 (LIVE `oj5cecci…`, offset −1000) |
| S2B 25 Sep, R105 (`S2B_43SFS_20260925_0_L2A`) | 1.6 | 1014 | 2588 | 0.4370 | same tslot 20721 |
| S2B 28 Sep (`S2B_43SFS_20260928_0_L2A`) | 97.3 | 7065 | 6938 | −0.0091 | cloud |
| S2C 30 Sep, R105 (`S2C_43SFS_20260930_0_L2A`) | 28.3 | 1014 | 2505 | 0.4237 | M5 "30 Sep truth" |

All five items: `s2:processing_baseline` 05.13, `earthsearch:boa_offset_applied: true`, red `raster:bands`
`{"nodata": 0, "data_type": "uint16", "spatial_resolution": 10, "scale": 0.0001, "offset": -0.1}` (LIVE,
`https://earth-search.aws.element84.com/v1/search?collections=sentinel-2-l2a&intersects=…&datetime=2026-09-20/2026-09-30`).

Derived (INFERRED arithmetic): MPC DNs read without the offset, 25 Sep: (3502 − 1900)/(3502 + 1900) = 0.2966.
Element84 DNs with Element84's declared offset: S2A 25 Sep (0.1502 − (−0.0100))/(0.1502 + (−0.0100)) = 1.1427; S2B
25 Sep 0.9825; S2C 30 Sep 0.9816.

### 4.3 Rondônia: floor vs round at 100 signed points (MEASURED, 2026-10-01)

Inputs: the 100 cells of `research/repro/v12/data/case_rondonia_eudr.json`; exact coordinates from the signed Hansen
loss-year facts (100 × `GET /v1/facts/<cid>`, all `hansen_gfc_v1_13_pixel@1`, `reader=cog-pixel-floor@2`, signed
2026-09-30T19:12:19Z to 19:13:27Z). Rasters: `Hansen_GFC-2025-v1.13_{lossyear,treecover2000}_00N_070W.tif` (0.00025°,
PixelIsArea) and `JRC_GFC2020_V4_N0_W70.tif` (0.0000833°, PixelIsArea), read by window with rasterio. Rule "floor" =
`floor(x + 1e-6)`, rule "round" = `round(x)`; EUDR flag = GFC2020 forest AND Hansen loss year > 2020 (the case file's rule).

| quantity | count of 100 |
|---|---|
| signed post-fix loss year equals the independent floor read | 100 |
| Hansen: rounding picks a different pixel | 79 |
| GFC2020 V4: rounding picks a different pixel | 82 |
| Hansen loss year changes | 7 (e.g. none → 2022 at `defi.zb391.wuti.zcb96`; 2012 → none at `defi.zb391.yOga.zca5f`) |
| Hansen tree cover 2000 changes | 21 (median abs 8 points, max 97) |
| tree cover crosses 10 % (or 30 %) | 3 (3) |
| GFC2020 forest class changes | 1 (`defi.zb391.bOyE.zcafa`: forest → non-forest) |
| Hansen "loss after 2020" changes | 1 |
| EUDR flags, floor rule / round rule | 3 / 3 (0 flips) |

Scope: one 6 × 6 km grid of point samples, not plots; not a prevalence estimate for EUDR.

### 4.4 The 27 Jan 2022 record (defect 14) (MEASURED + LIVE, 2026-10-01)

`GET /v1/facts/2dpnuf4eqjgmacmwq5hqoofpcslmsmehtui2mnul5x6pbh2ttnwq`: cell `defi.zb572.xoso.zb1ec`, tslot 19019, value
−0.048604578237692105, `signed_at` 2026-07-16T05:40:19Z, source `sentinel-s2-l2a-cogs/43/S/FS/2022/1/S2A_43SFS_20220127_1_L2A/{B08,B04}.tif`,
DNs [3034, 3344], no offset arg.

| source | product id | containing pixel B08 / B04 | rounded pixel B08 / B04 | NDVI containing |
|---|---|---|---|---|
| Element84 v0 and v1 (identical DNs) | `…N0400_R005_T43SFS_20220127T083110`, `sentinel:boa_offset_applied: true` | 5900 / 6195 | **3034 / 3344** (the signed DNs) | −0.0244 |
| Planetary Computer | `…N0400_R005_T43SFS_20220212T103433` (baseline 04.00) | 7200 / 7508 | 4188 / 4512 | −0.0242 (with −1000) |

Reading: the offset was handled right (E84 is harmonised for this item); the record is the rounded neighbour pixel;
two processing runs of one acquisition differ by about 0.03 reflectance beyond the offset at this snow pixel.

### 4.5 Other LIVE reads

- `GET /v1/facts/kxjvfwpa…` (pre-fix 23 Sep) and `oj5cecci…` (post-fix 25 Sep): values, DNs, offsets and sources as quoted
  in F1 and F2.
- `GET /v1/facts/p6ewjnlq…` (the `/v1/ask` answer): cell `defi.zb572.xAnI.zb1a2`, tslot 20726, 0.2824, scene
  `S2C_MSIL2A_20260930T052651_R105_T43SFS_20260930T102304`, DNs [3688, 2504].
- `GET /v1/facts/ncupl5pt…` (GFC2020): scheme `jrc.gfc2020.v4`, URL path `/GFC2020/LATEST/`, `fn_key`
  `jrc_gfc2020_v3_pixel@1`, `captured_at` 2024-04-25.
- OSM relation 1411107 (F16).

---

## 5. The catastrophe ladder

**Rule.** A rung is the deepest check a wrong value survives. The higher the rung, the more checks it passes and the more
confidently it is acted on. The top two rungs are passed by every check a reference protocol can run. Every number
below is sourced in sections 2 to 4; the ordering is my judgement (INFERRED).

| rung | survives up to | stopped by | class | one measured line | outside, one line | stake (sourced) |
|---|---|---|---|---|---|---|
| 9 | everything | nothing | F17 product truth | GFC2020 V2 forest commission 18 %, V3 13.1 % [S46, S19] | JRC: maps "non-legally binding" [S19] | EUDR screen inherits map error |
| 8 | everything | nothing | F16 entity | "Maasvlakte ramp 7" → a 12 × 10 km admin boundary (LIVE) | MaxMind: 600 million IPs on one farm [S29] | right measurement, wrong object |
| 7 | hash, binding, signature, log, recompute | I re-read | F1 wrong pixel | 162/200 records; 0.4709 → 0.3016; +0.127 fake change (MEASURED) | GDAL RFC 33 half pixel [S1]; 1 px → > 50 % of NDVI differences [S5] | decision flip; change detection |
| 6 | hash, signature, log | I re-read, signed Absence | F9 missing as value | off-tile pixel signed 0 = "no loss", a pass (SPEC `CHANGELOG.md:53`) | Hansen `lossyear` 0 = "no loss" [S18]; Overpass HTTP 200 on failure [S32] | EUDR false pass (prevalence UNVERIFIED); Member States must set maximum fines of at least 4 % of EU-wide turnover (Art. 25, secondary source) [S45] |
| 5 | hash, signature, log | H recompute, I re-read | F2 radiometric convention; F10 units | one pixel: 0.4709 / 0.2966 / 1.1427 (MEASURED) ; WorldPop 1.77 × (SPEC) | users: 2022 NDVI 0.1-0.2 lower [S10]; two repos fixed it on 30 Sep 2026 [S11, S12]; MCO lost [S35] | smooth bias, time-series step |
| 4 | hash, binding | C/E naming the version; as-of recall; log | F4 source switch; F5 stale/history | Bengaluru 918.0 → 915.07 m, same band name (MEASURED) | MODIS C6 LUT error bands 1-2, 2012-2017 [S16]; GFC2020 V2 → V3 −20 % Cerrado [S19] | baseline flips; blame for a value not yet known |
| 3 | hash | E binding (C for same-day) | F3 date/scene; F8 place | asked 23 Sep, got 25 Sep, 9/10 agents (MEASURED); 596 m off the given coordinates (MEASURED) | STAC defines no default order [S14]; GDAL 3 axis order [S30] | "no change" from one scene; answer for the wrong place |
| 2 | nothing below C | C resolve the reference | F6 rounding; F7 compaction; F12 truncation | "0.47": 5/5 wrong decisions; compaction 0/72 right, 3/36 agree (MEASURED) | 39 % multi-turn drop [S26]; MAST loss of history [S28] | agreement without correctness |
| side | all rungs | independent receiver code | F14 verifier passes without checking; F13 copies counted; F11 unstable ids; F15 data as instructions | `/verify` green without a signature check (SPEC); 8 "attestations" from one key (MEASURED) | CVE-2014-1266 [S41] | a ladder is only as good as the check that is actually run |

**Poster version (seven rungs, every word sourced).** Top to bottom:

| rung | label | number | check |
|---|---|---|---|
| L5 | Wrong product | GFC2020 forest commission error 13 to 18 % | none |
| L4 | Wrong object | "ramp 7" → all of Maasvlakte, 12 × 10 km | none |
| L3 | Wrong pixel, signed | 162 of 200 records; 0.471 → 0.302 | re-read the source |
| L3 | Missing data signed as 0 | off-tile loss year 0 = "no loss" | re-read the source |
| L2 | Wrong scale | 0.471 / 0.297 / 1.143 at one pixel | recompute |
| L1 | Wrong date, place, version | 23 Sep asked, 25 Sep served; 596 m; 918.0 → 915.07 m | cell / time / source in the record |
| L0 | Lost in the handoff | "0.47": 5 of 5 wrong; compaction 0 of 72 right | resolve the reference |

---

## 6. Figure data: "One pixel, one question, eight answers"

Question: NDVI at cell `defi.zb572.xoso.zb1ec` (Keylong field), 25 Sep 2026. Rule (R3, synthetic): irrigate iff NDVI ≤
0.4705. Suggested form: one horizontal number line from 0.25 to 1.15 with the rule as a vertical line; one dot per answer,
coloured by the check that stops it; dot labels below. All values MEASURED or LIVE except where the row says INFERRED.

| answer | value | mechanism (class) | decision under the rule | first check that stops it | source |
|---|---|---|---|---|---|
| right | 0.4709 | containing pixel, S2A R005, offset −1000 | hold | – | LIVE `oj5cecci…`; E84 900/2502 |
| rounded | 0.47 | prose "0.47" (F6) | irrigate | C | `v8/results.json` R arm 5/5 |
| other scene, same day | 0.4370 | S2B R105, tslot 20721 (F3) | irrigate | C (resolve A's reference) / scene id | E84 1014/2588 |
| other day, as current | 0.4237 | S2C 30 Sep handed as 25 Sep (F3/F5, M5) | irrigate | E tslot | E84 1014/2505 |
| neighbour pixel | 0.3016 | pre-fix rounding reader (F1, M15) | irrigate | I | `pixel_check.json` 2720/1923 |
| offset omitted | 0.2966 | MPC DNs without −1000 (F2, M12) | irrigate | H / I | INFERRED from LIVE DNs 3502/1900 |
| place name, not coordinates | 0.2824 | `/v1/ask` town point, 596 m, 30 Sep (F8, M4) | irrigate | E cell | LIVE `p6ewjnlq…` |
| offset applied twice | 1.1427 | E84 DNs with E84's declared −0.1 (F2) | invalid | range check / H | INFERRED from MEASURED DNs + LIVE metadata |

Caption candidate (claim, not description): "Eight answers to one question, all from real mechanisms. Six cross the
decision line; one is impossible; one is right. Each wrong answer is stopped by a different check, and only a source
re-read stops the signed neighbour pixel."

Second figure candidate, "A fix mid-series makes a trend": two bars per pair, pre-fix 23 Sep 0.344 vs post-fix 25 Sep
0.471 (+0.127) and containing pixels 0.486 vs 0.471 (−0.015). Caption: "Comparing a record signed before the reader fix
with one signed after it shows greening that the ground did not show. `signed_at` tells the two apart."

---

## 7. Poster copy candidates (each tied to a row above)

- "Every error we found in emem is an error any agent pipeline over EO data can make. Here is what each one looked like,
  where else it happens, and which check stops it."
- "The right record, the wrong pixel: 162 of 200 sampled records carried the neighbouring pixel's values. Hash,
  signature, log and recompute all passed. A re-read of the source found it." (F1)
- "A date is not an observation: two Sentinel-2 scenes on 25 Sep give 0.471 and 0.437 at one pixel." (F3)
- "One pixel, three scales: 0.471, 0.297, 1.143. The catalogue's own metadata says both 'offset applied' and 'apply
  −0.1'." (F2)
- "Asked for 23 Sep, served 25 Sep: 9 of 10 agents never got the date they asked for; 3 of 10 explained it away." (F3)
- "Agreement is not evidence: under compaction, 3 of 36 agent pairs agreed and 0 of 72 answers were right." (F7)
- "What no reference can check: whether 'ramp 7' is the whole port, and whether the forest map is right." (F16, F17)

Words to avoid on these panels (MASTER §11, §23; issue #13): "verified" without a layer; "proves"; "truth"; "catastrophe"
as a printed claim (use the measured consequence instead).

---

## 8. Guardrails: what the poster must not say

1. Do not say emem's checks found its own errors in production. The wrong-pixel bug was found by an audit that re-read
   pixels against GDAL (`cog.rs:132-134`); the records verified cryptographically throughout. Say: "the record carries
   what a re-read needs".
2. Do not say the wrong pixel flipped EUDR flags. At Rondônia it flipped 0 of 3 flags in 100 points (section 4.3).
3. Do not give a prevalence for the tile-edge false pass (F9): emem's CHANGELOG states the mechanism, not a count.
4. Do not present the irrigation rule as agronomy; it is R3's synthetic threshold. The Kc figure is INFERRED for scale.
5. Do not present the Google Maps, MaxMind, Mars Climate Orbiter, CVE or REDD+ cases as EO-agent failures; they are
   analogs for a mechanism and must be labelled so.
6. EUDR article text (Art. 25 penalties, Art. 2(28) geolocation, application dates under Regulation (EU) 2025/2650) is
   cited from secondary sources here; EUR-Lex returned HTTP 202 with an empty body from this container. Verify on EUR-Lex
   before printing article numbers.
7. The date-substitution behaviour (F3) is open at 18adb67; do not print it as fixed.
8. The post-fix 0/54 pixel sample is provider-confounded (all Planetary Computer, two days).
9. The Element84 metadata contradiction (F2) is measured on five items at one tile; do not generalise to the collection
   without a wider sample.

---

## 9. Open questions

1. Should emem read `earthsearch:boa_offset_applied` per item instead of treating every Element84 v1 item as harmonised,
   given Element84's README says the offset was applied "to some of the Items"? (Maintainers.)
2. Should `band_raster` with `observed_on` choose the nearest scene (and return the scene date it chose), as the cube
   docs say? Defect 27/34 is open in code.
3. Should a same-day second acquisition be distinguishable by more than the scene id (tslot is day-granular)?
4. Can the v13 experiment add the eight-answers case as mutations (same-day scene; double offset) so the figure is a
   measured matrix row, not a hand-built list?
5. How many pre-fix records were handed out as tokens before 2026-09-28, and can a receiver be told (e.g. a `superseded_by`
   on the record)? Not answerable read-only.
6. Should the Rondônia floor/round check be repeated on plot polygons near forest edges, where a one-pixel error is most
   likely to change a verdict?
7. Is EUR-Lex reachable from the build host, to quote Art. 25 and Art. 2(28) verbatim?

---

## 10. Sources (all retrieved 2026-10-01 unless stated)

| ref | source |
|---|---|
| S1 | GDAL RFC 33, GTiff, fixing PixelIsPoint interpretation. https://gdal.org/en/stable/development/rfc/rfc33_gtiff_pixelispoint.html |
| S2 | rasterio discussion #2478, "Why is op=math.floor the default in index/rowcol?" (10 Jun 2022). https://github.com/rasterio/rasterio/discussions/2478 |
| S3 | rasterio issue #2205, "Merge is prone to off-by-one pixel errors" (11 Jun 2021). https://github.com/rasterio/rasterio/issues/2205 |
| S4 | Copernicus DEM on AWS, readme (data processing; northing of pixel centres). https://copernicus-dem-30m.s3.amazonaws.com/readme.html |
| S5 | Townshend, Justice, Gurney, McManus, "The impact of misregistration on change detection", IEEE TGRS 30(5):1054-1060, 1992, doi:10.1109/36.175340 (abstract via ResearchGate index; DOI via Crossref). https://www.researchgate.net/publication/3201019_The_impact_of_misregistration_on_change_detection |
| S6 | Sentinel-2 L1C Data Quality Reports, SentiWiki (multi-temporal registration ≤ 0.3 SSD at 2σ for refined products). https://sentiwiki.copernicus.eu/__attachments/1673423/OMPC.CS.DQR.001.03-2025%20-%20MSI%20L1C%20DQR%20April%202025%20-%20110.0.pdf (search-indexed text; PDF not opened) |
| S7 | SentiWiki, S2 Products (BOA_ADD_OFFSET formula, fetched). https://sentiwiki.copernicus.eu/web/s2-products |
| S8 | Google Earth Engine, COPERNICUS/S2_SR_HARMONIZED (fetched). https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED |
| S9 | ESA STEP forum, "Changes in band data after 25 Jan 2022" (posts Jun 2022 to Aug 2024). https://forum.step.esa.int/t/changes-in-band-data-after-25-jan-2022-baseline-04-00-harmonizevalues-sentinel-2-l2a-snappy/36270 |
| S9a | ESA STEP forum, "[INFO] Introduction of additional Radiometric Offset in PB04.00 products" (25 Mar 2022, fetched as JSON). https://forum.step.esa.int/t/info-introduction-of-additional-radiometric-offset-in-pb04-00-products/35431 |
| S10 | Planet/Sinergise community, "NDVI values are low after Sentinel-2 processing baseline changes in Jan 2022" (26 Apr 2024). https://community.planet.com/analysis-apis-81/ndvi-values-are-low-after-sentinel-2-processing-baseline-changes-in-jan-2022-5681 |
| S11 | DPIRD-DMA/S2Mosaic PR #9, "Remove the baseline 04.00 BOA offset from MPC spectral bands", merged 30 Sep 2026. https://github.com/DPIRD-DMA/S2Mosaic/pull/9 |
| S12 | franciscoparrao/surtgis PR #146, merged 30 Sep 2026. https://github.com/franciscoparrao/surtgis/pull/146 |
| S13 | Element84 Earth Search v1 STAC API, live items for the Keylong point. https://earth-search.aws.element84.com/v1/search |
| S13a | Element84 earth-search README, "Gain/Offset in Items after Jan 25, 2022". https://github.com/Element84/earth-search (raw README.md) |
| S13b | Element84 earth-search discussion #26, "Options for handling offsets in Sentinel-2 COGs" (decision 8 Dec 2023). https://github.com/Element84/earth-search/discussions/26 |
| S14 | STAC API item search specification (no default ordering text) and sort extension. https://github.com/radiantearth/stac-api-spec/tree/main/item-search ; https://github.com/stac-api-extensions/sort |
| S15 | Google Earth Engine, `ee.ImageCollection.mosaic` (page summary). https://developers.google.com/earth-engine/apidocs/ee-imagecollection-mosaic |
| S16 | NASA Earthdata, "MODIS Land C61 Changes". https://earthdata.nasa.gov/s3fs-public/2022-02/MODIS_C61_Land_Proposed_Changes.docx.pdf |
| S17 | Wang et al., "Impact of sensor degradation on the MODIS NDVI time series", Remote Sensing of Environment 119:55-61, 2012, doi:10.1016/j.rse.2011.12.001 (abstract via NTRS). https://ntrs.nasa.gov/citations/20110015444 |
| S18 | Hansen et al., Global Forest Change 2000-2025 (v1.13) data download and user notes. https://storage.googleapis.com/earthenginepartners-hansen/GFC-2025-v1.13/download.html |
| S19 | Bourgoin et al., "Maps of Global Forest Cover 2020 Version 3 and Global Forest Type 2020 Version 1 Supporting the EU Deforestation Regulation", JRC146622, EUR 40716, 2026, doi:10.2760/9982436. https://publications.jrc.ec.europa.eu/repository/bitstream/JRC146622/JRC146622_01.pdf |
| S20 | Copernicus Data Space Ecosystem, Copernicus DEM collection description (releases; accuracy). https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM |
| S21 | CDSE news, "Sentinel-2 Collection-1 Products Availability" (2 Sep 2024). https://dataspace.copernicus.eu/news/2024-9-2-sentinel-2-collection-1-products-availability |
| S21b | Element84 earth-search issue #68 (15 May 2025). https://github.com/Element84/earth-search/issues/68 |
| S22 | Washington Post, 21 Sep 2023, "North Carolina family sues Google over Snow Creek bridge collapse death"; CNN, 21 Sep 2023. https://www.washingtonpost.com/nation/2023/09/21/north-carolina-hickory-bridge-collapse-google-lawsuit/ ; https://edition.cnn.com/2023/09/21/us/father-death-google-gps-drive-off-bridge-lawsuit-north-carolina (via search index; not opened) |
| S23 | Zhao, Cohen, Webber, "Reducing Quantity Hallucinations in Abstractive Summarization", Findings of EMNLP 2020. https://aclanthology.org/2020.findings-emnlp.203/ |
| S24 | Perez et al., "When LLMs Play the Telephone Game", arXiv 2407.04503 (rev. 29 Jan 2026). https://arxiv.org/abs/2407.04503 |
| S25 | Claude Platform docs, Compaction overview. https://platform.claude.com/docs/en/build-with-claude/compaction |
| S26 | Laban et al., "LLMs Get Lost In Multi-Turn Conversation", arXiv 2505.06120 (9 May 2025). https://arxiv.org/abs/2505.06120 |
| S27 | Liu et al., "Lost in the Middle", TACL 12:157-173, 2024, doi:10.1162/tacl_a_00638. https://arxiv.org/abs/2307.03172 |
| S28 | Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", arXiv 2503.13657 v3 (26 Oct 2025). https://arxiv.org/abs/2503.13657 |
| S29 | MaxMind default location, Potwin, Kansas (Fusion, Apr 2016; lawsuit 2016, settled 2017). https://en.wikipedia.org/wiki/MaxMind ; https://www.arkansasonline.com/news/2016/aug/14/farm-in-kansas-labeled-as-source-of-int/ (via search index) |
| S30 | GDAL RFC 73, PROJ 6 integration, axis order. https://gdal.org/development/rfc/rfc73_proj6_wkt2_srsbarn.html (via search index) |
| S31 | Gritta, Pilehvar, Limsopatham, Collier, "What's missing in geographical parsing?", Language Resources and Evaluation 52(2):603-623, doi:10.1007/s10579-017-9385-8 (Crossref). |
| S32 | overpass-turbo issue #176, "runtime error: Query run out of memory is not returning http error code" (3 Jul 2015). https://github.com/tyrasd/overpass-turbo/issues/176 |
| S33 | NASA POWER API documentation (fill value −999; via search index). https://power.larc.nasa.gov/docs/services/api/ |
| S34 | NASA Earthdata Forum, "What caveats should be considered when using active fire data from FIRMS?" (13 Feb 2024). https://forum.earthdata.nasa.gov/viewtopic.php?t=5188 |
| S35 | Mars Climate Orbiter Mishap Investigation Board, Phase I Report, 10 Nov 1999 (PDF opened). https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf |
| S36 | ISRIC SoilGrids FAQ, mapped units and conversion factors (via search index). https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_01.html |
| S37 | Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic" (Oracle copy, fetched). https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html |
| S38 | Google Earth Engine, `ee.Image.reduceRegion` (`bestEffort`, fetched). https://developers.google.com/earth-engine/apidocs/ee-image-reduceregion |
| S39 | Claude Code docs, MCP output limits (fetched). https://code.claude.com/docs/en/mcp |
| S40 | Weng et al., "Do as We Do, Not as You Think: the Conformity of Large Language Models", ICLR 2025, arXiv 2501.13381. https://arxiv.org/abs/2501.13381 |
| S41 | NVD, CVE-2014-1266 (API). https://nvd.nist.gov/vuln/detail/CVE-2014-1266 |
| S42 | NVD, CVE-2020-0601 (API). https://nvd.nist.gov/vuln/detail/CVE-2020-0601 |
| S43 | Greshake et al., "Not what you've signed up for", arXiv 2302.12173. https://arxiv.org/abs/2302.12173 |
| S44 | Model Context Protocol specification 2025-11-25, Server: Tools (fetched). https://modelcontextprotocol.io/specification/2025-11-25/server/tools |
| S45 | Regulation (EU) 2023/1115 (EUDR), Art. 2, 9, 25; Regulation (EU) 2025/2650 (application dates 30 Dec 2026 / 30 Jun 2027). Primary: https://eur-lex.europa.eu/eli/reg/2023/1115/oj (HTTP 202, empty, from this container). Secondary, fetched: https://www.coolset.com/academy/eudr-penalties-what-non-compliance-actually-costs-fines-bans-criminal-liability ; https://en.wikipedia.org/wiki/EU_Regulation_on_Deforestation-free_products |
| S46 | Bourgoin et al., "GFC2020: a global map of forest land use for year 2020 to support the EU Deforestation Regulation", ESSD 18:1331, 19 Feb 2026. https://essd.copernicus.org/articles/18/1331/2026/ |
| S47 | Kamble, Kilic, Hubbard, "Estimating Crop Coefficients Using Remote Sensing-Based Vegetation Index", Remote Sensing 5(4):1588, 2013 (equation via search index; MDPI returned 403). https://www.mdpi.com/2072-4292/5/4/1588 |
| S48 | Open-Meteo Elevation API docs (fetched). https://open-meteo.com/en/docs/elevation-api |
| S49 | West et al., "Action needed to make carbon offsets from forest conservation work for climate change mitigation", Science 381(6660):873-877, 25 Aug 2023, doi:10.1126/science.ade3535 (abstract via Crossref). Rebuttal: https://arxiv.org/abs/2312.06793 |

Internal sources: emem `origin/main` 18adb67 (`CHANGELOG.md`, `docs/paper-section-statistics-and-threats.md`,
`crates/emem-fetch/src/{cog.rs,stac.rs}`, `crates/emem-api-rest/src/{lib.rs,band_raster.rs}`); emem.dev `GET /v1/facts/<cid>`
(105 reads, 2026-10-01); OpenStreetMap API `relation/1411107.json`; this repository's files named in each row.
Scratch outputs (not committed): `/tmp/claude-0/-home-user-esa-poster/0db6b3ad-8059-51a6-bd74-2d7a97faf986/scratchpad/fm/`
(`e84_keylong.json`, `rondonia_hansen_facts.json`, `rondonia_floor_round_v2.json`, `CHANGELOG_18adb67.md`).
