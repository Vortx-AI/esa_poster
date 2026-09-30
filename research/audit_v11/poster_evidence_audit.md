# EMEM poster v10: evidence audit for the invention-grade redesign

Poster repo `Vortx-AI/esa_poster` at **50bb8bf** (main). The seal box was filled in at 50bb8bf; the hashed board.jpg is from 5143fac. emem reference implementation: HEAD e226f8b; the poster pins 213e273 and 18adb67. Live responder commit on audit GETs: 9d2c454. Audit run 30 Sep 2026.

**Method.** The poster text and every token were extracted programmatically from `poster/poster.html`. Each printed claim was matched to the repo file that records it. Arithmetic (Fisher p, Wilson intervals, byte fractions, cell pitch, tslot dates, ΔNDVI) was recomputed. The board.jpg sha256 and the v9 pre-registration BLAKE3 were recomputed, and the offline proof bundle was re-run with `verify_bundle.py` (ALL PASS). emem git history was checked for the encoder-retirement dates. Four read-only GETs were made to emem.dev (`/v1/log/witnesses`, `/v1/capabilities`, `/v1/tools.json` → 404, and the published B08 pointer note). Nothing was written, signed or pushed.

**Support codes.** EXACT = the source supports the printed value (rounding checked). PARTIAL = part sourced, or a qualifier is missing. MISMATCH = the source contradicts the wording. UNSOURCED = no file in the repo records it. STALE = superseded by newer data.

**Totals:** 96 claims — EXACT 72, PARTIAL 10, UNSOURCED 6, MISMATCH 6, STALE 2.

## Priority fixes before printing

1. **§ panel 2 · Full trace — A tampered mirror copy was rejected** (UNSOURCED): No mirror/tamper entry in crossruntime_table.json or elsewhere in repo. Commit the run or remove.
2. **§ panel 11 · Integrity elsewhere — Copernicus Data Space SAFE: MD5 + BLAKE3 of whole product, unsigned** (UNSOURCED): No file in repo carries this size or the checksum observation.
3. **§ panel 11 · Integrity elsewhere — NASA Earthdata MCP: granule concept id; older revisions 404** (UNSOURCED): No repo record of the Earthdata MCP call or the 404 on older revisions; commit the query log or remove the row.
4. **§ panel 3 · What the trace found — Pre-fix rule** (MISMATCH): Incomplete: the column was rounded too, so the neighbour is east, south or south-east. State both axes.
5. **§ panel 5 · Handoff — B (Haiku) token arm correct** (MISMATCH): B called resolve; the re-hash and receipt checks were run by the harness, not by B. Say "B resolved 10/10; harness re-hash and receipt 10/10".
6. **§ panel 5 · Handoff — Qwen2.5-3B as B** (UNSOURCED): The pinned results file (§22 evidence pointer, blake3 g2dwdmhw…) has empty Qwen arms and no raw logs are committed. The arithmetic is internally consistent (19+18+5 = 42). Commit the Qwen results before printing. Two-sided Fisher on 0/19 vs 10/18 would be p ≈ 1.3·10⁻⁴ against the token arm.
7. **§ panel 7 · Drift taxonomy — The reader row** (MISMATCH): Must read "a neighbouring pixel"; §3 headline already says so.
8. **§ panel 9 · Since acceptance — TESSERA is frozen on emem.dev** (MISMATCH): The §9 TESSERA vector itself was signed after the documented retirement. Date the freeze (from when?) or explain how the 30 Sep 08:33Z vector was minted.
9. **§ panel 10 · Where emem lost — Single tokens cost 9.5× the LLM tokens** (MISMATCH): Board’s own measurement: 46 cl100k tokens vs 8 for the 16-digit value = 5.75× (15× vs a 3-dp value). Print the own measurement or label 9.5× as the docs figure.
10. **§ panel 12 · Ememify — Local node re-read: bit-identical NDVI, different fact_cid** (UNSOURCED): Strong claim for the federation objection; commit the run.
11. **Footer — Traffic** (UNSOURCED): No repo file. channel_messages.json (29 Sep) has 8,478 messages from 216 attesters but no operator-key list to reproduce 96.2 %.
12. **Footer — Panel numbering** (MISMATCH): Panel numbers collide with §-step numbers ("section 2" vs "§2" = B08 pointer). Use letters for panels.

## A. Claim table

| id | panel | claim | printed value | source | support | note | evidence class |
|---|---|---|---|---|---|---|---|
| A01 | Lead / header | emem version and commits | emem 2.4.2 at 213e273 and 18adb67 | emem Cargo.toml at both commits (version = "2.4.2"); git log | EXACT | Live responder reported x-emem-commit 9d2c454 on 30 Sep audit GETs (between the two pins); emem HEAD is e226f8b. | code-read |
| A02 | Lead / header | Measurement window | 29–30 Sep 2026 | repro/README.md; trace_fact_output.txt (2026-09-30T09:15Z); v9 prereg 13:49Z | EXACT |  | measured (ours) |
| A03 | Lead / header | Agents cannot write observations | — | algorithms.md (derive promotion); track10 step 11 "caller-signed NDVI change" | PARTIAL | True for primary observations only. §12 prints "Register your own result, signed by your key" (a caller-signed derivative, jb67zixq…). Reword: agents cannot write primary observations; caller derivatives are recomputed before promotion to deterministic_index. | code-read |
| A04 | Lead / header | B verifies the log entry and receipt offline | — | v8/verify_bundle.py (re-run 30 Sep: 9/9 PASS) | PARTIAL | The 4,906-byte offline file covers links 1–5 and 12–14 (fact bytes, cell, batch root, attestation sig, STH sig, inclusion, witness, consistency). The serve receipt (link 10) is not in the file. | measured (ours), n=1 bundle |
| A05 | Lead / header | Fact tuple field order | kind, cell, band, tslot, value, unit, confidence, sources, derivation{fn_key,args}, privacy, schema_cid, signer, signed_at | algorithms.md §1 (fact.rs); 04 ledger §1 | EXACT | Board omits optional uncertainty? and served_via? fields; acceptable if footnoted "optional fields omitted". | code-read @18adb67 |
| A06 | Lead / header | Canonical bytes | CBOR in declaration order; NaN→f9 7e00; −0→+0 | algorithms.md §1; defect 33 | EXACT | Not RFC 8949 §4.2.1 key-sorted (defect 33); board wording is correct. | code-read @18adb67 |
| A07 | Lead / header | fact_cid | base32(BLAKE3-256(b)) | verify_fact.py; trace link 3 | EXACT | Lower-case, no padding (algorithms.md notation). | measured (ours) + code-read |
| A08 | Lead / header | cell quantisation and pitch | lat_q = round((lat+90)/180·(2²¹−1)); pitch 8.583·10⁻⁵° = 9.52 × 8.06 m here | algorithms.md §1; recomputed (WGS84 at 32.571°N) | EXACT | Recomputed 9.518 × 8.060 m. Figure caption rounds to 9.5 × 8.1 m (consistent). | derived arithmetic |
| A09 | Lead / header | tslot | ⌊unix/86 400⌋; 20721 = 25 Sep 2026 | recomputed | EXACT | 20719 = 23 Sep; 20651 = 17 Jul (trap value) also check. | derived arithmetic |
| A10 | Lead / header | As-of recall rule | argmax signed_at ≤ t (signed_at, cid) | algorithms.md §1 (recall.rs) | EXACT | Defect 35: as_of_signed_at compared as raw string (fractional seconds / offsets order wrongly; untested). | code-read @18adb67 |
| A11 | Lead / header | Batch attestation | R = Merkle(sorted fact_cids); Ed25519(PreimageV1("attestation"){R, registry, schema}) | algorithms.md; attest.rs:105-124; verify_bundle.py "batch_root recomputed" PASS | EXACT |  | code-read + measured (ours) |
| A12 | Lead / header | Log shape | leaf = BLAKE3(0x00‖BLAKE3(CBOR(att))), node = BLAKE3(0x01‖l‖r), RFC 6962 shape | algorithms.md; verify_log.py; verify_bundle.py inclusion+consistency PASS | EXACT |  | code-read + measured (ours) |
| A13 | Lead / header | Receipt preimage | Ed25519(BLAKE3("emem.preimage.v1\0"‖request_id‖served_at‖primitive‖cells‖fact_cids‖merkle)) | algorithms.md; 04 ledger (Rust/Python/JS agree on preimage digest) | EXACT |  | code-read |
| A14 | Lead figure | Keylong field size and grid bytes | 443 × 453 px at 10 m; 802,780 B per band grid | hero_field.json; token_counts.json raster_artifact_B04_bytes = 802780 (= 443·453·4 + 64) | EXACT |  | measured (ours) |
| A15 | Lead figure | Four band grids re-hash to their names | 4 of 4 | repro/README (data/ re-hashed); hero_field.json | EXACT |  | measured (ours) |
| A16 | § panel 1 · From scene to token | Bytes read vs scene | 1.17 MB of 2.02 GB (0.058 %); 1,165,033 of 2,023,818,762 B | cog_pixel_bytes.json; scene_sizes.json; recomputed 0.0576 % | EXACT | "By our reconstruction of its read path" is the correct qualifier: emem does not log its own range reads. | measured (ours), reconstruction |
| A17 | § panel 1 · From scene to token | What is read | three 64 KiB COG headers + one tile each of B04, B08, SCL | cog_pixel_bytes.json (head_bytes_read 65536 ×3; tiles 468,566 + 477,314 + SCL) | EXACT |  | measured (ours) |
| A18 | § panel 1 · From scene to token | Signed record size | 1,115 B | inventory.json bytes = 1115; trace link 2 | EXACT |  | measured (ours) |
| A19 | § panel 1 · From scene to token | Token length | 84 characters (46 GPT-4 tokenizer tokens) | token_counts.json fact_token_ndvi chars 84, cl100k 46; results.json cl100k_token 46 | EXACT | Conflicts with §10 "9.5×", which uses the docs figure of 51 tokens (see A-§10). | measured (ours) |
| A20 | § panel 1 · From scene to token | Earth Search pointer notes | 292 chunks each (header + 291 tiles); 238.7 MB (B08), 232.9 MB (B04) | pub/b04/note.md bytes 232,853,854; live GET of B08 note 30 Sep: bytes 238,683,874, 292 of 292 hashed | EXACT | B08 note body is not committed to the repo; commit it (pub/b08/) so the claim is repo-checkable. | measured (ours) + live GET |
| A21 | § panel 1 · From scene to token | Tree row of the cell | emem:tree:khiqtqrddb6jponqn4gv72if7e#row=108; 1,586,895 B | live GET of B08 note: 0-based row 108 = level 0 tile 8,9, length 1,586,895 | EXACT | Not in repo (see above). | live GET |
| A22 | § panel 1 · From scene to token | Planetary Computer B08 file | 281.9 MB; offset not pre-subtracted; emem records no hash of it | scene_sizes.json / cog_pixel_bytes.json cog_bytes 281,898,500; defect 25 (Source.hash never filled) | EXACT |  | measured (ours) + code-read |
| A23 | § panel 1 · From scene to token | §4 record contents | band indices.ndvi; day 20721; scene S2A_MSIL2A_20260925T054251_R005_T43SFS; SCL 4; DN B08 3502 / B04 1900; offset −1000; value 0.4708994708994709; signed_at 2026-09-28T09:06:56Z | inventory.json; trace_fact_output.txt link 6; pixel_check.json floor_DN 3502/1900 | EXACT | Hero record carries no reader=cog-pixel-floor@2 stamp (prevalence_summary post.stamp_absent_signed_at includes 09:06:56Z); post-fix status rests on signed_at > PIXEL_FIX_AT 04:09:26Z. | measured (ours) |
| A24 | § panel 1 · From scene to token | NDVI bit-identical from DNs | ((3502−1000)−(1900−1000)) / ((3502−1000)+(1900−1000)) = (2502−900)/(2502+900) = 0.4708994708994709 | verify_ndvi.py; algorithms.md (0x3fde233788cde233) | EXACT |  | measured (ours) |
| A25 | § panel 1 · From scene to token | Earth Search tile values | B08 2502, B04 900; NDVI identical | pub/b04/note.md; live B08 note | EXACT |  | measured (ours) |
| A26 | § panel 2 · Full trace | Trace script | 698-line script (stdlib, blake3, cbor2, pynacl); 15 links, 17 checks, 17.9 s, all verified | trace_fact.py (698 lines); trace_fact_output.txt | EXACT |  | measured (ours), n=1 run |
| A27 | § panel 2 · Full trace | Tamper sensitivity | one flipped mantissa bit gives mu5x2cks… | trace_fact_output.txt link 3 | EXACT |  | measured (ours) |
| A28 | § panel 2 · Full trace | Wrong-cell token refused | HTTP 409 | trace_fact_output.txt link 4 | EXACT | Server-side convenience; offline check is the cell inside the hashed body. | measured (ours) |
| A29 | § panel 2 · Full trace | Pixel re-read | col 9098, row 9443: B08 3502, B04 1900 | trace link 9; pixel_check.json | EXACT |  | measured (ours) |
| A30 | § panel 2 · Full trace | Log inclusion | entry 2,457,078 in 2,556,451-entry log; consistent with root geo.qa co-signed | verify_bundle.py re-run (entry 2457078 under STH 2556451; witness head 2541495) | EXACT |  | measured (ours) |
| A31 | § panel 2 · Full trace | geo.qa is also run by Vortx AI | — | trace residual trust; defect 30; live /v1/log/witnesses: independent_operator_domains = [geo.qa], org_vouched 2 keys, key_only 109 | EXACT |  | live GET + docs |
| A32 | § panel 2 · Full trace | Key → domain | did:web, JWKS, DNS TXT; Web PKI; DNS without DNSSEC | trace link 15 (AD=False) | EXACT |  | measured (ours) |
| A33 | § panel 2 · Full trace | Offline file | 4,906 B; 9 checks with networking disabled (unshare -rn); 1-bit tamper, wrong cell, wrong key fail | proof_bundle_ndvi.cbor = 4906 B; verify_bundle.py prints 9 PASS (re-run by this audit) | PARTIAL | 9 checks and size verified. The unshare -rn run and the three negative cases have no committed log; re-run and commit the output. | measured (ours) |
| A34 | § panel 2 · Full trace | Ten client paths, same fact_cid, 3 reps each | 10 paths × 3/3 | crossruntime_table.json: paths 1–7 (10 entries), distinct_fact_cids = 1, all_rehash_ok | EXACT | Receipt verified on 9 of 11 NDVI paths (not LlamaIndex, not raw CBOR). Same responder for all paths: availability, not replication. Official MCP Python/TS SDK paths (6c, 6d) are not named in the list. | measured (ours), n=10 paths × 3 |
| A35 | § panel 2 · Full trace | A tampered mirror copy was rejected | — | none found | UNSOURCED | No mirror/tamper entry in crossruntime_table.json or elsewhere in repo. Commit the run or remove. | — |
| A36 | § panel 11 · Integrity elsewhere | Planetary Computer: B08 COG URL, opaque ETag, no checksum | 281,898,500 B | scene_sizes.json | PARTIAL | Size sourced; "opaque ETag, no checksum" not logged in repo (pointer notes say "etag: not exposed" for Earth Search). | measured (ours) |
| A37 | § panel 11 · Integrity elsewhere | Copernicus Data Space SAFE: MD5 + BLAKE3 of whole product, unsigned | 1,187,971,637 B | none found | UNSOURCED | No file in repo carries this size or the checksum observation. | — |
| A38 | § panel 11 · Integrity elsewhere | NASA Earthdata MCP: granule concept id; older revisions 404 | — | none found | UNSOURCED | No repo record of the Earthdata MCP call or the 404 on older revisions; commit the query log or remove the row. | — |
| A39 | § panel 11 · Integrity elsewhere | MCP tool results carry no integrity; proposed in issue #3354 | spec 2026-07-28 | external: modelcontextprotocol#3354 (SEP proposal, verifiable tool results) | EXACT | Source is external, not in repo; cite the URL on the handout. | external (web) |
| A40 | § panel 11 · Integrity elsewhere | Source.hash is empty | — | defect 25 (hash: None, 61 sites) | EXACT |  | code-read |
| A41 | § panel 3 · What the trace found | Pre-fix prevalence | 162/200 = 81 % [75–86 %] Wilson 95 % | prevalence_summary.json pre: matches_round_not_floor 162, Wilson (0.750, 0.858) | EXACT |  | measured (ours), n=200 random sample, not pre-registered |
| A42 | § panel 3 · What the trace found | Sample composition | 200 cells, 164 scenes, 19 bands (192 Element84, 8 PC) | prevalence_summary.json | EXACT |  | measured (ours) |
| A43 | § panel 3 · What the trace found | Same pixel under both rules / floor-only matches | 38 / 0 | prevalence_summary.json floor_equals_round_pixel 38, matches_floor_not_round 0 | EXACT |  | measured (ours) |
| A44 | § panel 3 · What the trace found | Pre-fix rule | row = round(j + (Y−N)/sy): the south pixel whenever the fraction ≥ ½ | CHANGELOG line 68 (south-east neighbour); prevalence frac_parts col≥½ 93, row≥½ 100 of 200 | MISMATCH | Incomplete: the column was rounded too, so the neighbour is east, south or south-east. State both axes. | code-read + measured |
| A45 | § panel 3 · What the trace found | 23 Sep record carries pixel 10 m south | 2993/1972, SCL 5, NDVI 0.3444; containing pixel 0.4860 | pixel_check.json; v9 prereg (SCL 5) | EXACT | South is correct for this cell (row fraction .5736, col fraction .3273). | measured (ours) |
| A46 | § panel 3 · What the trace found | ΔNDVI in emem’s signed change record, 23→25 Sep | +0.127 | derived: 0.4708994708994709 − 0.34435075885328836 = 0.12655 | PARTIAL | Arithmetic matches; no signed change record for this pair is in the repo (the only committed change fact is the same-DOY −0.1298). Either cite the change fact or say "difference of the two signed values". | derived arithmetic |
| A47 | § panel 3 · What the trace found | ΔNDVI at containing pixel | −0.015 | 0.47090 − 0.48602 = −0.0151; v9 trial 8 | EXACT |  | measured (ours) |
| A48 | § panel 3 · What the trace found | Fix shipped 28 Sep | PIXEL_FIX_AT 2026-09-28T04:09:26Z | trace_fact_output.txt (lib.rs:12650); CHANGELOG line 68 pointer | EXACT |  | code-read |
| A49 | § panel 3 · What the trace found | Post-fix records read the containing pixel | — | prevalence_summary.json post: n=54, 49/49 floor where rules differ, 0 round (Wilson upper 7.3 %) | EXACT | Print n=54; 3 post-fix records lack the reader stamp. | measured (ours), n=54 |
| A50 | § panel 5 · Handoff | A returned exact token | 10/10; mean 13 s; 3.3 tool calls; one prose misdated 2025 | results.json agent_a: token_equals_hero 10, wall_s_mean 13.28, tool_calls_mean 3.3, prose_year_ok 9 | EXACT | Also: first call errored or used a wrong cell in 3/10 A runs (first_call_error_or_wrong_cell [1,4,5]); not printed. | measured (ours), pre-registered, n=10 |
| A51 | § panel 5 · Handoff | B (Haiku) token arm correct | 10/10; "B checked A’s token: resolve, re-hash, receipt 10/10" | results.json T: resolve_called 10, harness_rehash_ok 10, receipt_valid 10, decision_correct 10 | MISMATCH | B called resolve; the re-hash and receipt checks were run by the harness, not by B. Say "B resolved 10/10; harness re-hash and receipt 10/10". | measured (ours), pre-registered, n=10 |
| A52 | § panel 5 · Handoff | Prose (16 digits) arm | 10/10 | results.json P decision_correct 10 | EXACT |  | measured (ours), pre-registered, n=10 |
| A53 | § panel 5 · Handoff | Rounded prose arm | 0/5; Fisher p = 0.0003 (exploratory) | results.json R: 0/5; T_vs_R p = 0.000333 | EXACT | Correctly labelled exploratory (arm added after A’s runs). | measured (ours), exploratory, n=5 |
| A54 | § panel 5 · Handoff | Forged-cell tokens declined | 5/5 | results.json F decline 5, forged_detected 5 | EXACT | Decline followed a responder refusal (MCP error / REST 409), not B’s own hash check. | measured (ours), pre-registered, n=5 |
| A55 | § panel 5 · Handoff | Primary test tie | 10/10 vs 10/10, p = 1 | results.json T_vs_P_primary p_one_sided 1.0 | EXACT |  | measured (ours), pre-registered |
| A56 | § panel 5 · Handoff | Threshold 0.0004 below value | 0.4705 vs 0.4709 | v8 prereg.md decision rule | EXACT | Constructed boundary; board says so. | pre-registered design |
| A57 | § panel 5 · Handoff | Qwen2.5-3B as B | 42 of 45 trials; token 0/19, prose 10/18; forged 0/5 declined | results.json b.qwen2.5-3b-instruct-q4_k_m = {arms: {}, tests: {}}; RESEARCH_STATE (qualitative only) | UNSOURCED | The pinned results file (§22 evidence pointer, blake3 g2dwdmhw…) has empty Qwen arms and no raw logs are committed. The arithmetic is internally consistent (19+18+5 = 42). Commit the Qwen results before printing. Two-sided Fisher on 0/19 vs 10/18 would be p ≈ 1.3·10⁻⁴ against the token arm. | claimed pre-registered, data not in repo |
| A58 | § panel 6 · Compaction | Agreement ≠ correctness | 0/72 correct, 3/36 agree; Fisher one-sided p = 0.035 | 05_EVIDENCE (paper-section-statistics-and-threats.md:85-89); pointer §17; recomputed p = 0.03497 | EXACT | Test compares 36 pairs with the 72 answers that form them (non-independent units). Defect 28: README prints 27.8 % vs 1.4 %, which does not reproduce p = 0.035. | measured (emem docs), pre-registered, n=72/36 |
| A59 | § panel 6 · Compaction | Control and no-pressure arms | 72/72, 36/36; 20/72, 15/36, p = 0.109 | 05_EVIDENCE; recomputed p = 0.1089 | EXACT |  | measured (emem docs), pre-registered |
| A60 | § panel 6 · Compaction | Handoff n = 20 per arm | prose 2, dense 8, BM25 20, bundle 20 | collaboration-log rows (pointer §18) | PARTIAL | Omits the single-token arm 16/20, excluded for a window bug. Print as "(single-token arm excluded: window bug)". | measured (emem docs), n=20/arm, not pre-registered (as far as the repo shows) |
| A61 | § panel 6 · Compaction | Trap value | 0.4871541501976284, observed 17 Jul (tslot 20651), signed 18 Jul | inventory.json ndvi_trap_17jul | EXACT | "Pre-fix read of the pixel south" is inferred from the hero-cell census (60/66 pre-fix match round), not a direct re-read of the 17 Jul scene. | measured (ours) |
| A62 | § panel 6 · Compaction | Six scoring bugs across two scorers | 6 | paper-section-statistics-and-threats.md:163-166 pointer | EXACT |  | docs |
| A63 | § panel 6 · Compaction | Models and host | Gemma-4-12B + Qwen2.5-7B, one host | 05_EVIDENCE | EXACT |  | docs |
| A64 | § panel 7 · Drift taxonomy | The reader row | 162 of 200 pre-fix S2 records carry the pixel south | prevalence_summary.json frac_parts | MISMATCH | Must read "a neighbouring pixel"; §3 headline already says so. | measured (ours) |
| A65 | § panel 7 · Drift taxonomy | Source drift | Bengaluru elevation 918.0 → 915.07 m; "as known on 15 Jun" returns 918.0 | inventory.json elev_may / elev_sep; repro README Exhibit A; verify_bitemporal.py | EXACT |  | measured (ours) |
| A66 | § panel 7 · Drift taxonomy | Signer drift | 915.07 m signed 7 times: 7 fact_cids | contra_bengaluru.json: 7 of 8 attestations = 915.0712280273438 | EXACT | Severity 1.0, scope same_attester_provider_substitution. | measured (ours) |
| A67 | § panel 7 · Drift taxonomy | Date drift (raster and cube) | 23 Sep → 25 Sep scene; cube member 15 May → 10 Jun | v9 results.md; cubeK_members.json (days 26) | EXACT |  | measured (ours) |
| A68 | § panel 7 · Drift taxonomy | Referent drift | "Maasvlakte ramp 7" resolves to all of Maasvlakte, ≈ 12 × 10 km | defect 21 (OSM relation 1411107); defect 31 entity token | EXACT |  | measured (ours), n=1 |
| A69 | § panel 8 · Raw bands | Scene-selection rule and 23 Sep outcome | window 24 Aug – 30 Sep → 25 Sep (10.8 %); 23 Sep (20 %) cannot win | algorithms.md (band_raster.rs:224-238, stac.rs:405-422); hero_field.json cloud 10.840102; v9 results.md 20.0 % | EXACT |  | code-read + measured |
| A70 | § panel 8 · Raw bands | Run outcomes | 10 chose B04/B08 NDVI; 9 noticed one scene; 1 got 23 Sep values; 5 placeholders; 4 undetermined; 0 greener; 3 wrongly said no 23 Sep scene; 30/30 CIDs re-hash; all values traced | v9 results.md headline + table | EXACT |  | measured (ours), pre-registered, n=10 |
| A71 | § panel 8 · Raw bands | Pre-registration hash | 30d8a1a1… at 13:49Z 30 Sep | prereg_hash.txt; recomputed BLAKE3 of prereg.md matches | EXACT | raw/ transcripts and tools_list_full.json named in results.md are not committed. | measured (ours) |
| A72 | § panel 9 · Since acceptance | Encoders removed from code | Clay v1.5, Prithvi-EO-2.0, Galileo, JEPA-v2 head | emem commit 2335c52 (24 Sep); pointer §23 (CHANGELOG line 77) | EXACT |  | code-read |
| A73 | § panel 9 · Since acceptance | TESSERA is frozen on emem.dev | — | docs/memory.md (fb4795b, 29 Sep); deploy/systemd EMEM_RETIRED_BANDS=geotessera (80641e0, 29 Sep 21:05Z); inventory.json tessera_keylong signed 2026-09-30T08:33:07Z | MISMATCH | The §9 TESSERA vector itself was signed after the documented retirement. Date the freeze (from when?) or explain how the 30 Sep 08:33Z vector was minted. | code-read + measured |
| A74 | § panel 9 · Since acceptance | TESSERA re-read bit-exact | 128 B int8 + 4 B scale, max \|Δ\| = 0, 4 of 4 | fig_tessera_data.json: centre_equals_fact = true (1 fact); 7 neighbour cosines recomputed within 1.1·10⁻⁸ | PARTIAL | "4 of 4" and "max \|Δ\| = 0" not found in any repo file. | measured (ours), n=1 + 7 |
| A75 | § panel 9 · Since acceptance | Clay names its weights by BLAKE2b; code gone | — | algorithms.md Clay pin (served_via.model_blake2b_hex; sidecar removed, CHANGELOG:77) | EXACT | Algorithms.md: digest parameters and the exact file hashed are not determined. | code-read |
| A76 | § panel 9 · Since acceptance | Device gate | 17 reject reasons; admits no real hardware | algorithms.md §device; RESEARCH_STATE | EXACT |  | code-read |
| A77 | § panel 10 · Where emem lost | Scorecard verdicts | 7 rows (supported / refuted / not tested) | how-emem-compares.md pointer §19; 05_EVIDENCE | EXACT |  | docs (authors’ benchmark) |
| A78 | § panel 10 · Where emem lost | BM25 ties | 16/16 | docs_out_v9 how-emem-compares rows (lines 79–96) | EXACT |  | docs |
| A79 | § panel 10 · Where emem lost | Single tokens cost 9.5× the LLM tokens | 9.5× | how-emem-compares (84 chars ≈ 51 tokens) | MISMATCH | Board’s own measurement: 46 cl100k tokens vs 8 for the 16-digit value = 5.75× (15× vs a 3-dp value). Print the own measurement or label 9.5× as the docs figure. | docs vs measured (ours) |
| A80 | § panel 10 · Where emem lost | Bundle | 38 chars for up to 256 facts | 05_EVIDENCE; how-emem-compares | EXACT |  | docs + code-read |
| A81 | § panel 10 · Where emem lost | Dereferenced citations | 99.2 % exact, 0 confidently wrong (84.4 % before four fixes); dense 4/142, up to 138 confidently wrong, median 252 m; 74/96 abstain vs 93/96 confident wrong | docs_out_v9 how-emem-compares rows (lines 79–96, 102–109) | EXACT |  | docs (SAMPLE, 5 sites) |
| A82 | § panel 10 · Where emem lost | Nineteen withdrawn claims | 19 | whitepaper-v3 lines 241–246 pointer §20 | EXACT |  | docs |
| A83 | § panel 12 · Ememify | MCP tool counts | 18 core, 114 in all | 05_EVIDENCE (snapshot 64cfae5); crossruntime tools_list_count_/mcp 18; v9 results.md: 116 tools at /mcp/full | STALE | Core 18 confirmed; "114 in all" is stale (116 on 30 Sep). | docs + measured |
| A84 | § panel 12 · Ememify | Claude skill research-grade-citation | — | emem plugins/emem/skills/emem-research-grade-citation/SKILL.md at HEAD | EXACT | Skill name has the emem- prefix; print the exact name. | code-read |
| A85 | § panel 12 · Ememify | Caller-signed NDVI change, emem recomputed bit-identical | −0.1298 (25 Sep 2025 → 2026) | inventory.json derived_ndvi_delta −0.12976424591468844 (derivative, same_doy_ndvi_delta@1) | PARTIAL | Value sourced; the derive response (ulp_gap = 0, promotion) is not in the repo. | measured (ours) |
| A86 | § panel 12 · Ememify | Local node re-read: bit-identical NDVI, different fact_cid | — | none found | UNSOURCED | Strong claim for the federation objection; commit the run. | — |
| A87 | § panel 12 · Ememify | A2A card signed | emem.dev/.well-known/agent-card.json | crossruntime path 3 (A2A message/send works) | PARTIAL | Signature on the card not logged in repo. | — |
| A88 | § panel 13 · Not established | Draft-check rule | allows ⇔ ∃ a: round(a·10^d)/10^d = s; "≈ 0.49" passes for 0.4871 | algorithms.md guard section; 04 ledger (35 °C vs 28.0 denied) | EXACT |  | code-read |
| A89 | § panel 13 · Not established | Witness keys | only domain-vouched co-signer geo.qa (Vortx); 109 other keys unvouched | live /v1/log/witnesses 30 Sep: key_only 109, org_vouched 2 keys, 1 domain | EXACT | Moves over time; re-check before print. | live GET |
| A90 | § panel 13 · Not established | Re-minting a raster gives a new token | signed_at is hashed | 14_REAL_GAP_STUDY; algorithms.md | EXACT |  | code-read |
| A91 | § panel 14 · Seal | Track, head, steps | 7n7qogvn2ib3er5nreorzmfnbu; head q62y7frkthtivnqrynwt6iradm; 28 of 28 | pub/track10/note.md; publish_log.json | EXACT |  | measured (ours) |
| A92 | § panel 14 · Seal | board.jpg sha256 | 96fed23a…701c | recomputed on poster/board.jpg at 5143fac and 50bb8bf | EXACT |  | measured (this audit) |
| A93 | § panel 14 · Seal | Written after log size 2,568,005; logged as entry 2,568,005 | 2,568,005 | publish_log.json sth.tree_size 2568005 (read before writing) | PARTIAL | "Written after" is recorded. "Logged as entry 2,568,005" is not recorded (no leaf index in publish_log); concurrent writes can interleave. Fetch the inclusion proof and print the actual index. | measured (ours) |
| A94 | Footer | Traffic | 96,728 MCP tool calls; PyPI 314; npm 304 last month; 96.2 % of signed agent notes from operator keys | none found | UNSOURCED | No repo file. channel_messages.json (29 Sep) has 8,478 messages from 216 attesters but no operator-key list to reproduce 96.2 %. | — |
| A95 | Footer | Panel numbering | panels 1, 2, 11, 3, 5–10, 12–14; no panel 4 | poster.html | MISMATCH | Panel numbers collide with §-step numbers ("section 2" vs "§2" = B08 pointer). Use letters for panels. | — |
| A96 | HTML metadata | <title> | EMEM poster A0 (v8, ememified) | poster.html | STALE | Cosmetic; appears in PDF metadata. | — |

### Repo-side inconsistencies (not printed on the board)

- research/README.md describes do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md as 22 defects; the file now lists 36 (entries 27–36 added in v9–v10).
- should_do/04_VERIFIED_CLAIMS_LEDGER.md (snapshot 64cfae5) still says TESSERA is the live encoder; poster §9 says it is frozen. Update the ledger snapshot to 18adb67.
- data/v9/rawband/results.md lists raw/ transcripts and tools_list_full.json; neither is committed. data/v8/prereg.md cites raw/prereg.blake3; not committed. The v8 pre-registration timestamp therefore rests on the file mtime claim only.
- poster/README.md says log size 'was 2,537,510 on 29 Sep; the poster says 2.54 M' — v10 no longer prints 2.54 M; the checklist item is stale.

## B. Strongest results for emem as an invention

**1. Any client re-derives the same name from the served bytes.** 10 independent client paths (raw REST, raw MCP JSON-RPC, A2A, Python SDK, TypeScript SDK, LlamaIndex, LangChain MCP adapters, official MCP Python and TypeScript SDKs, stock blake3+cbor2) × 3 repetitions each returned one fact_cid (oj5cecci…) and one value (0.4708994708994709) for the Keylong NDVI record; the Bengaluru elevation record gave the same result on 10 paths. Every path re-hashed; receipts verified on 9/11 (NDVI) and 8/10 (elevation) paths.  
*n:* 10 paths × 3 reps × 2 records; plus 1 isolated A→B process pair · *statistics:* deterministic (all-or-nothing); no test statistic · *source:* `research/repro/data/v8/crossruntime_table.json`  
*Caveat that travels with it:* All paths hit the same responder: this shows client-independent verification, not independent replication or availability.

**2. One 84-character token traces to the source pixel with no emem code.** A 698-line script checked 15 links (17 checks) from token to the Sentinel-2 COG pixel in 17.9 s, all VERIFIED; NDVI recomputed bit-identical (0x3fde233788cde233) from DNs 3502/1900 and the −1000 BOA offset inside the signed bytes; a 1-mantissa-bit change renames the record (mu5x2cks…).  
*n:* 1 record, 1 run · *statistics:* deterministic · *source:* `research/repro/v8/trace_fact.py, trace_fact_output.txt; verify_ndvi.py`  
*Caveat that travels with it:* emem stores no hash of the upstream file (Source.hash empty); the upstream link is checked by re-reading the pixel, and the key→domain link rests on Web PKI and DNS without DNSSEC.

**3. A 4,906-byte evidence file verifies offline.** proof_bundle_ndvi.cbor (4,906 B) passes 9 checks with no network: fact bytes inside the logged attestation hash to the token, token cell = signed cell, batch root recomputed, attestation and STH signatures, inclusion of entry 2,457,078 under the 2,556,451-entry STH, witness co-signature at head 2,541,495, and consistency. Re-run by this audit on 30 Sep: ALL PASS.  
*n:* 1 bundle · *statistics:* deterministic · *source:* `research/repro/v8/verify_bundle.py, proof_bundle_ndvi.cbor`  
*Caveat that travels with it:* The only domain-vouched witness (geo.qa) is operated by Vortx AI, so the file does not yet protect against a split view by the operator; the serve receipt is not in the file.

**4. Signed records audit their own reader.** Re-reading the COG pixel named inside each signed record showed that 162/200 randomly sampled pre-fix Sentinel-2 records (81 %, Wilson 95 % 75–86 %; 200 cells, 164 scenes, 19 bands) carry a neighbouring pixel’s DNs, 0/162 match the containing pixel where the rules differ, and 200/200 values recompute from their signed DNs. After the fix, 0/54 match the rounded pixel and 49/49 match the containing pixel where the rules differ. Old tokens still resolve to exactly what was signed, so the error is dated by signed_at vs PIXEL_FIX_AT (2026-09-28T04:09:26Z).  
*n:* 200 pre-fix + 54 post-fix records · *statistics:* Wilson 95 %: pre 0.750–0.858; post round-match upper bound 0.066 · *source:* `research/repro/data/v8/prevalence_summary.json, pixel_check.json`  
*Caveat that travels with it:* The error was emem’s own; addressing did not prevent it — it made it detectable, datable and non-destructively correctable. Not pre-registered.

**5. Agreement between agents is not correctness (pre-registered).** Under compaction pressure with a shared summary, 0/72 answers were correct while 3/36 model pairs agreed; Fisher one-sided p = 0.035 (recomputed 0.0350). Full-context control 72/72 correct, 36/36 agree; no-pressure arm 20/72 vs 15/36, p = 0.109 (not established).  
*n:* 72 answers / 36 pairs per arm · *statistics:* Fisher exact one-sided p = 0.035 (pre-registered l44rdbk7…) · *source:* `emem docs/paper-section-statistics-and-threats.md:85-89 (pointer §17); should_do/05`  
*Caveat that travels with it:* Two open models (Gemma-4-12B, Qwen2.5-7B) on one host; six scoring bugs fixed across two scorers; the test compares pairs with the answers that form them (non-independent units); emem’s README prints numbers that do not reproduce this p (defect 28).

**6. Addressed handoff keeps the value exact where prose loses it.** Handoff after a context reset, n = 20 per arm: token bundle 20/20, BM25 20/20, dense retrieval 8/20, prose 2/20. Bundle vs prose Fisher one-sided p ≈ 1.7·10⁻⁹ (computed by this audit, not a pre-registered test).  
*n:* 20 per arm · *statistics:* Wilson (from the log): prose 10 % [3–30 %], dense 40 % [22–61 %] · *source:* `emem docs/collaboration-log.md rows (pointer §18)`  
*Caveat that travels with it:* BM25 ties the bundle; a single-token arm (16/20) was excluded for a window bug; one host, emem-authored benchmark.

**7. Dereferenced citations are exact; dense retrieval is confidently wrong.** Citation dereferenced end-to-end: 99.2 % exact with 0 confidently wrong answers; dense top-5 retrieval 4/142 exact with up to 138 confidently wrong, by a median 252 m. On a retrieval miss one model abstained 74/96 and the other gave a real neighbouring-cell value 93/96.  
*n:* 142 items; 96 miss cases; 5 sites · *statistics:* as recorded by the authors (McNemar p = 6·10⁻⁵ for confident-wrong rate, collaboration-log:14833-14850) · *source:* `emem docs/how-emem-compares.md lines 79–109 (pointer §25)`  
*Caveat that travels with it:* Authors’ benchmark labelled SAMPLE; 84.4 % before four fixes the benchmark prompted; BM25 matches (16/16); 2 open 7–12B models, one host.

**8. Bi-temporal memory keeps both answers and exposes the substitution.** Bengaluru cell defi.zb493.xuqA.zcb5f, copdem30m.elevation_mean: 918.0 m (May, open_meteo_copdem90m@1) and 915.07 m (Sep, copernicus_dem_30m_aws_pixel@1) both re-hash today; an as-of-15-Jun read still returns 918.0; /v1/memory_contradictions reports the pair at severity 1.0 as a same-attester provider substitution; the drift is visible as fn_key₁ ≠ fn_key₂ inside the bytes.  
*n:* 1 key, 8 attestations · *statistics:* deterministic · *source:* `research/repro/README.md Exhibit A; data/contra_bengaluru.json; inventory.json; verify_bitemporal.py`  
*Caveat that travels with it:* 915.07 m was signed 7 times as 7 fact_cids: identity is per signed record, not per value; the as-of comparison is a raw string compare (defect 35).

**9. Embeddings are addressable, checkable records that outlive their encoder.** The TESSERA 128-D vector at the Keylong cell (ga2o2nuf…) re-reads from the public source.coop product with centre_equals_fact = true; for 7 neighbouring TESSERA facts the served cosine was recomputed within 1.1·10⁻⁸; the Clay v1.5 1024-D fact (jh2kmfiy…) still resolves and re-hashes after Clay was removed from the code (2335c52, 24 Sep), with its checkpoint pinned by a BLAKE2b field inside the hashed bytes.  
*n:* 1 + 7 TESSERA facts; 1 Clay fact · *statistics:* deterministic · *source:* `research/repro/data/v8/fig_tessera_data.json; inventory.json; algorithms.md (Clay pin)`  
*Caveat that travels with it:* The encoder step is attester_only (not recomputable); TESSERA is frozen for new materialisation but the §9 vector was signed 30 Sep 08:33Z — date the freeze; Clay digest parameters are not determined.

**10. A forged cell binding is refused; the receiver must enforce it.** Pre-registered two-LLM handoff with emem as the only MCP server: A (Claude Sonnet 5.5) returned the exact token 10/10; B (Claude Haiku 4.5) declined 5/5 tokens with a forged cell (responder refusal: MCP error / REST 409); token vs 16-digit prose tied 10/10 vs 10/10 (primary, p = 1); prose rounded to 0.47 gave 0/5 correct (exploratory, p = 0.0003).  
*n:* A 10; B arms 10/10/5/5 · *statistics:* Fisher one-sided: primary p = 1; exploratory p = 0.00033 · *source:* `research/repro/data/v8/results.json, prereg.md`  
*Caveat that travels with it:* The pre-registered Qwen2.5-3B receiver dropped the cell, resolved the bare id and acted (0/5 declined; 0/19 token vs 10/18 prose) — those numbers are not in the committed results.json; one model family for the Claude arms; the re-hash was done by the harness, not by B.

## C. Objections and answers

**C1. A signature does not make a value true. You have signed a number, not measured the ground.**  
*Kind:* concede + scope · *evidence:* §2 residual-trust column; prevalence_summary.json; 04 ledger (what is not proved)  
Agreed, and the board should say so in one line: the signature proves who served which bytes and when; it does not prove the ground truth. What emem adds is that the value is checkable and datable. Evidence: re-reading the pixel named inside the signed records found emem’s own rounding error in 162/200 pre-fix records (Wilson 75–86 %), and signed_at against PIXEL_FIX_AT dates every affected record. A prose citation would carry neither. Frame it as "a checkable claim, not a true one".

**C2. Your tokens cost more LLM tokens than the value they replace.**  
*Kind:* concede + scope · *evidence:* token_counts.json; results.json; §10 scorecard  
A single fact token is 84 characters = 46 cl100k tokens against 8 for the 16-digit value (5.75×; the emem docs say 9.5× against ~51 tokens). The claim is fidelity, not compression: under compaction the paraphrase gave 0/72 correct and prose rounded to 0.47 gave 0/5, while the token arm stayed exact. Where size matters, one 38-character bundle handle (~23 tokens) covers up to 256 facts. Print the own measurement and drop "saves context" for single tokens.

**C3. BM25 ties you (16/16, 20/20). Why not just keep the corpus and retrieve lexically?**  
*Kind:* concede + scope · *evidence:* how-emem-compares rows 79–109; collaboration-log handoff rows  
On these short corpora BM25 is as accurate as addressing, and the poster should keep that line. BM25 assumes the receiver holds the same corpus and gives no integrity, no place/time binding and no way to detect a substituted or re-minted record. The emem claim is verifiability of the cited value across parties, not retrieval accuracy. Where retrieval is dense (the common agent-memory default), it was exact on 4/142 items and confidently wrong on up to 138 (median 252 m off), against 0 for dereferenced citations.

**C4. The title says "over Foundation-Model Embeddings", but you retired your foundation-model encoders.**  
*Kind:* reframe · *evidence:* emem 2335c52; algorithms.md Clay pin; fig_tessera_data.json; inventory.json  
An embedding in emem is one typed record (model_output) with place, time, source and recipe around it, not the protocol’s identity. The retirement is the test of that design. After Clay, Prithvi, Galileo and the JEPA-v2 head were removed from the code (24 Sep), the vectors signed earlier still resolve and re-hash, and the Clay record still names its checkpoint by BLAKE2b. The TESSERA vector re-reads from its public product. Concede two points: new encoder materialisation is paused, and the encoder step cannot be recomputed (attester_only). Also date the TESSERA freeze, since the §9 vector was signed 30 Sep 08:33Z.

**C5. Your own reader wrote 162 of 200 wrong-pixel records. Why should anyone trust emem’s memory?**  
*Kind:* reframe · *evidence:* prevalence_summary.json; CHANGELOG line 68 pointer (§8); RESEARCH_STATE v9 note  
Content addressing did not prevent the error. It is the reason the error was found by an outside script, dated to the minute, and corrected without rewriting a single signed byte: old tokens still resolve to what was signed, and post-fix records read the containing pixel (49/49 where the rules differ). This is the property an evaluation poster should want. The limits are that emem makes no claim of immunity to memory poisoning, and three post-fix records (including the hero record) carry no reader stamp.

**C6. The log co-signer geo.qa is also Vortx AI. That is not independent witnessing.**  
*Kind:* concede + scope · *evidence:* live /v1/log/witnesses (30 Sep); defect 30; verify_bundle.py  
Correct: the only domain-vouched witness is Vortx-operated, and the other 109 keys are key-only (unvouched), so the log gives no protection against a split view by the operator today. What ships is the machinery: RFC 6962-shaped inclusion and consistency proofs that anyone can check offline, and an open POST /v1/log/witness for co-signatures. Ask for a witness at the session: an ESA, BIFOLD or university key vouched by DNS would change the trust statement.

**C7. Single responder, no federation: if emem.dev disappears, so does your memory.**  
*Kind:* concede + scope · *evidence:* verify_bundle.py; trace link 15; 14_REAL_GAP_STUDY §17  
Integrity checks need no responder: a stock BLAKE3 over the served bytes, and a key published under did:web/JWKS/DNS, work from any copy, and the 4,906-byte file verifies offline. Availability does depend on the responder. Read federation is not shipped. The self-hostable node (docker image) re-signs under its own key, so its fact_cids differ for identical values. That supports the design, but the local-node re-read on the board has no committed log.

**C8. n is small and everything ran on one host. These are anecdotes.**  
*Kind:* concede + scope · *evidence:* 05_EVIDENCE; v8 prereg.md; v9 prereg.md; repro/  
Each number carries its n and design. Compaction: 72/36 per arm, pre-registered, p = 0.035. Handoff: n = 20 per arm. Two-LLM handoff: pre-registered, n = 10/10/5/5, primary test a tie. Raw-band run: pre-registered, n = 10. Mechanism results (re-hash on 10 client paths, the 15-link trace, the offline file) are deterministic and do not need n, only re-runs. There is no independent replication yet. The scripts and pre-registrations are public, and the handout should invite a replication.

**C9. Why not STAC with checksums, C2PA, W3C PROV or IPFS? This is content addressing plus provenance, both old.**  
*Kind:* rebuttal · *evidence:* §11 table; 03_INDUSTRY_SYSTEMS_COMPARISON; do_not_use/01  
The contribution is not the primitive but the object boundary. STAC and COG locate assets (the Planetary Computer B08 COG has an opaque ETag and no checksum). Product checksums cover a whole SAFE, not the value an agent cites. C2PA binds manifests to media assets. PROV is a vocabulary without content identity. IPFS CIDs name bytes but not place, band and valid time, and carry no recomputable derivation. emem composes the four pieces into one citable value: a BLAKE3 name, a (cell, band, tslot) key with as-of recall, a recomputable derivation, and a transparency-logged attestation. Emitting PROV and CIDv1 alongside is compatible, not competing.

**C10. In your own pre-registered handoff, full-precision prose tied the token 10/10 vs 10/10 (p = 1). The token adds nothing.**  
*Kind:* concede + scope · *evidence:* results.json; compaction table  
When the prose carries all 16 digits and nothing compresses it, it ties, and the board reports the tie as the primary result. The token matters at the two points where prose breaks. Rounding to "0.47" flipped every decision (0/5, exploratory). A shared summary under compaction gave 0/72 correct. Only the token lets the receiver check what it got: a forged cell was declined 5/5.

**C11. Your pre-registered open-model receiver (Qwen2.5-3B) did worse with tokens (0/19) than with prose (10/18) and accepted forged tokens.**  
*Kind:* concede + scope · *evidence:* v8 prereg.md; RESEARCH_STATE v8 note; results.json (Qwen arms empty)  
Report it as the result: a token protects only a receiver that dereferences it and enforces the cell binding. The 3B model read 0.4709 and still chose irrigate, and it resolved the bare id after dropping the cell. The design consequence is to move enforcement out of the LLM, into client code (SDK verify, a refusal on the responder) and into the guard. Before printing, commit the Qwen results: the pinned results.json has empty Qwen arms.

**C12. Guardrails and evaluation neighbours: your "verify before publish" check lets "≈ 0.49" pass for 0.4871 and does not check band or unit, and your Fisher test compares pairs with the answers inside them.**  
*Kind:* concede + scope · *evidence:* algorithms.md guard rule; paper-section-statistics-and-threats  
Both points hold. The draft checker judges at the writer’s own precision and does not match band or unit, so it catches 35 °C against a signed 28.0 but not a coarse paraphrase. It complements a guardrail and does not replace one. The compaction test is a pre-registered descriptive inversion (3/36 wrong-but-agreeing pairs while 0/72 answers were correct, against a 72/72 control), and the headline claim should rest on "agreement occurred with zero correct answers" rather than on the p-value alone. Offer a paired or permutation re-analysis in the handout.

## D. Refutations policy

**Principle.** A workshop poster is read at 1–3 m for about 90 seconds. Self-refutation earns board space when it *bounds a claim the board makes*: a reader who sees the claim should see its limit in the same glance. A refutation of a claim the board does *not* make (an old README number, a retired feature, a maintainer defect) is audit history. It belongs in the handout and the repo, where the reviewers who want it will look. v10 spends roughly four of thirteen panels (§8, §9, §10, §13) and large parts of §3 and §5 on refutation. Visitors then read the board as a post-mortem, and the contribution (a citable, checkable EO value that survives compaction, model change and handoff) is harder to see.

**Rules.**
1. A limit that qualifies a printed number goes in one line next to that number (n, host, pre-registered or exploratory, what was excluded).
2. One compact **trust-boundary box** on the board states what the mechanism proves and what it does not. Neighbours working on guardrails, evaluation and traceability will ask about this first, and a pre-emptive answer is a strength.
3. Pre-registered results that went against the authors stay on the board, compressed. Dropping them would be selective reporting.
4. Anything else goes to the handout or repo, with a QR code and a single pointer line.

**Per panel.**

| v10 panel | what it does now | recommendation | why |
|---|---|---|---|
| §9 "Since the paper was accepted: emem retired its foundation-model encoders" | headline reads as a retraction of the title | **Reframe, keep.** Retitle "Records outlive their encoders". Keep the TESSERA re-read and the Clay pin, plus one line: "new encoder materialisation paused (date)". Move the device-gate formula to the handout. | The retirement is the strongest available test of the design claim that the signed record, not the model, is the identity. It supports the title. Fix the freeze date first (mismatch A-§9). |
| §10 "Where emem lost" (authors' scorecard) | a whole panel of verdicts, 4 of 7 "refuted" | **Compress and move.** Fold three scope lines into the results panel: BM25 ties on short corpora (16/16, 20/20); a single token costs about 5.75× the value's LLM tokens and only bundles are flat; peer memory products not tested. Put the full scorecard, the 99.2 %/84.4 % history and "nineteen withdrawn claims" on the handout. | Each kept line bounds a printed claim (handoff, token cost). The rest refutes claims the v11 board will not make. |
| §13 "What is not established" | 9 statements plus the draft-check formula | **Keep as a box, shortened.** Five lines: a signature says who served it, not that it is true; one responder and one operator, whose witness geo.qa is also Vortx, with 109 other keys unvouched; entity and place tokens are labels, not bytes; the draft check works at the writer's precision and does not check band or unit; no read federation, no hardware attestation, nothing in orbit. Move the draft-check formula and signed-absence caveat to the handout. | This is the section guardrail and evaluation neighbours will probe. Stating it up front turns their objection into agreement. |
| §3 pixel audit | framed as a bug found | **Reframe, keep as a result.** "Records audit their own reader: 162/200 pre-fix records carry a neighbouring pixel (not only south); every error is datable; no signed byte rewritten." | This is the strongest evidence that addressing adds scientific value beyond storage. |
| §5 Qwen2.5-3B arm | one dense paragraph | **Keep one line**, once its data is committed. | It was pre-registered, and it gives a design consequence: enforcement belongs in client code. |
| §8 raw-band run | a full panel on a failed primary test | **Move to the handout.** Keep one row in the drift taxonomy: "date: asked 23 Sep, served 25 Sep; 9/10 agents saw it from the scene id inside the record". | The primary test could not run, so the panel reports a server defect (27), not a result about agents. |
| Defects list (36, do_not_use/05) | not on the board | **Repo only.** One footer line: "36 defects filed to the maintainers, public at research/do_not_use/05". | It shows the process is transparent without using board space. |
| §7 drift taxonomy | a mix of wins and one uncaught case | **Keep.** | "Six of seven drifts are one equality test on a field of the record" is an invention-grade statement. The uncaught referent case is its bound. |

**Net effect.** Refutation drops from about 4 panels to about 1 box plus 6–8 inline scope lines. Every limit that bounds a printed claim stays visible, and none that bounds an unprinted claim takes board space.


## E. Tokens, CIDs, hashes and URLs printed on v10 (verbatim)

Extracted with regular expressions from the unescaped `poster.html`. Every string below was asserted to occur verbatim in the source. Ellipsis-truncated prefixes are printed as they appear, and the full value is given in the verification column where the repo has it.

| kind | string (verbatim) | panel | verification |
|---|---|---|---|
| arxiv | `arXiv 2607.25066` | 6 · Compaction: why a paraphrase is not a citation |  |
| arxiv | `arXiv 2608.11242` | 6 · Compaction: why a paraphrase is not a citation |  |
| b32_26 | `7n7qogvn2ib3er5nreorzmfnbu` | 14 · Seal | track10 publish_log cid; 28 steps, verified 28 of 28 (note header) |
| b32_26 | `khiqtqrddb6jponqn4gv72if7e` | 1 · From scene to token | track10 step 2 (B08 COG pointer note) |
| b32_26 | `q62y7frkthtivnqrynwt6iradm` | 14 · Seal | track10 note head; equals chain value of step 28 |
| b32_52 | `4wmvv7i6bv4hjqp6lqbja3zjts53xlwlzwttzbpozt4eetukd2oq` | header/lead |  |
| b32_52 | `oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` | 1 · From scene to token |  |
| b32_52 | `zhiz2prbnvds6ex3cmwbwghlzzdhi6b7nro6h42p3xtamezq5voq` | header/lead |  |
| band_key | `indices.ndvi` | 1 · From scene to token |  |
| band_key | `s2.B04` | header/lead |  |
| cell64 | `defi.zb572.xoso.zb1ec` | 1 · From scene to token |  |
| cli | `claude mcp add --transport http emem https://emem.dev/mcp` | 12 · Ememify your work |  |
| cli | `npm i @vortxai/emem` | 12 · Ememify your work |  |
| cli | `pip install ememdev` | 12 · Ememify your work |  |
| code_ident | `Source.hash` | 11 · Integrity elsewhere |  |
| code_ident | `attester_only` | 9 · Since the paper was accepted |  |
| code_ident | `emem_band_raster` | 8 · Raw bands, the agent’s own method |  |
| code_ident | `unshare -rn` | 2 · Full trace |  |
| doi | `doi:10.5281/zenodo.20706893` | header/lead | paper DOI (task brief) |
| emem_token | `emem:entity:4itylz3k…` | 7 · A drift taxonomy from real cases | prefix of emem:entity:4itylz3kjtwy3lgr76ku52ffqa (defect 31; rehearse9 step 27) |
| emem_token | `emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` | 1 · From scene to token | re-hash verified (inventory.json, trace_fact_output.txt, verify_bundle.py re-run 30 Sep: ALL PASS) |
| emem_token | `emem:raster:zhiz2prbnvds6ex3cmwbwghlzzdhi6b7nro6h42p3xtamezq5voq:s2.B04:20721:4wmvv7i6bv4hjqp6lqbja3zjts53xlwlzwttzbpozt4eetukd2oq` | header/lead | matches track10 step 5 and hero_field.json |
| emem_token | `emem:tree:khiqtqrddb6jponqn4gv72if7e#row=108` | 1 · From scene to token | row 108 = level-0 tile 8,9, length 1,586,895 B in live B08 pointer note (GET 30 Sep) |
| fn_key | `copernicus_dem_30m_aws_pixel` | 7 · A drift taxonomy from real cases |  |
| fn_key | `open_meteo_copdem90m` | 7 · A drift taxonomy from real cases |  |
| git_commit | `18adb67` | header/lead |  |
| git_commit | `213e273` | header/lead |  |
| hash_prefix_ellipsis | `30d8a1a1…` | 8 · Raw bands, the agent’s own method | prefix of prereg blake3 30d8a1a1a8cf9646ada5e49b303b9c9c6f0c4ed6d076e797aa1a5fad6e35d50c (recomputed) |
| hash_prefix_ellipsis | `4itylz3k…` | 7 · A drift taxonomy from real cases |  |
| hash_prefix_ellipsis | `777er3yi…` | 1 · From scene to token | prefix of responder key 777er3yihgifqmv5hmc2wwmyszgddzderzhsx6rex4yoakwomvka |
| hash_prefix_ellipsis | `mu5x2cks…` | 2 · Full trace | prefix of mu5x2cksmneuujjb7yihfcrfdplv2eu4tmrefyxr2tckyf2q6m4a (tampered-bit CID, trace_fact_output.txt) |
| hash_prefix_ellipsis | `njedkglt…` | 14 · Seal | poster attester key prefix (by_attester path) |
| hash_prefix_ellipsis | `oj5cecci…` | 1 · From scene to token | prefix of the §4 fact_cid |
| issue | `issue #3354` | 11 · Integrity elsewhere | exists: modelcontextprotocol/modelcontextprotocol#3354, SEP proposal for verifiable tool results (web) |
| scene_id | `S2A_MSIL2A_20260925T054251_R005_T43SFS` | 1 · From scene to token |  |
| sha256_hex | `96fed23a289723e50cc7884f0b56d499e7de2b85a02117192a1fa0a22377701c` | 14 · Seal | sha256 of poster/board.jpg at 5143fac and at 50bb8bf (recomputed) |
| url | `emem.dev` | 2 · Full trace |  |
| url | `emem.dev/.well-known/agent-card.json` | 12 · Ememify your work |  |
| url | `emem.dev/memories/by_attester/njedkglt/7n7qogvn2ib3er5nreorzmfnbu.md` | 14 · Seal |  |
| url | `geo.qa` | 2 · Full trace |  |
| url | `ghcr.io/vortx-ai/emem` | 12 · Ememify your work |  |
| url | `github.com/Vortx-AI/esa_poster` | header/lead |  |
| url | `https://emem.dev/mcp` | 12 · Ememify your work |  |
| url | `vortx-ai.github.io/ememdemo/?s=emem.dev/memories/by_attester/njedkglt/7n7qogvn2ib3er5nreorzmfnbu.md` | 14 · Seal |  |
| cli | `docker run ghcr.io/vortx-ai/emem` | 12 · Ememify your work |  |
| repo_path | `research/repro/v8/trace_fact.py` | 2 · Full trace |  |
| repo_path | `verify_bundle.py` | 2 · Full trace |  |
| repo_path | `research/repro/data/v8/prereg.md` | 2 · Full trace |  |
| repo_path | `research/repro/data/v9/rawband` | 2 · Full trace |  |
| repo_path | `research/repro/v8/` | 2 · Full trace |  |
| repo_path | `research/repro/v10/algorithms.md` | 2 · Full trace |  |
| skill | `research-grade-citation` | 12 · Ememify your work |  |
| step_map | `§-steps: 1 board · 2–3 COG pointers · 4 NDVI record · 5 B04 raster · 6 cube · 7 pre-fix record · 8 CHANGELOG line 68 · 9 TESSERA · 10 Clay · 11 your derivation · 12–13 elevation · 14 temperature (draft check) · 15 absence · 16 bundle of 8 · 17–20 doc rows at emem 213e273 · 21 trap value · 22 our measurements · 23–26 doc rows at emem 18adb67 · 27–28 23 Sep B04, B08 (post-fix). Traffic to 30 Sep: 96,728 MCP tool calls; PyPI 314 · npm 304 last month; 96.2 % of signed agent notes are from operator keys` | footer |  |

Full tokens behind §-steps that the board references but does not print (from `research/repro/v8/pub/track10/note.md`), for reuse:

- §1 the board, seal box blank: `https://emem.dev/memories/by_attester/njedkglt/en6hzctku7in4bocyazwtimkou.md`
- §2 Sentinel-2 B08 COG, 292 tiles: `https://emem.dev/memories/by_attester/njedkglt/khiqtqrddb6jponqn4gv72if7e.md`
- §3 Sentinel-2 B04 COG, 292 tiles: `https://emem.dev/memories/by_attester/njedkglt/h6d7xdoc5b2uzood22lowblbc4.md`
- §4 NDVI record, Keylong, 25 Sep 2026: `emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa`
- §5 B04 raster, Keylong, 443 x 453 px: `emem:raster:zhiz2prbnvds6ex3cmwbwghlzzdhi6b7nro6h42p3xtamezq5voq:s2.B04:20721:4wmvv7i6bv4hjqp6lqbja3zjts53xlwlzwttzbpozt4eetukd2oq`
- §6 B08 cube, five scenes: `emem:cube:zhiz2prbnvds6ex3cmwbwghlzzdhi6b7nro6h42p3xtamezq5voq:s2.B08:20614..20721:7ath7qdwqbagvs6kojf7pquay5faj2wahytearzkpsrk7e4sufsa`
- §7 pre-fix record, 23 Sep, pixel south: `emem:fact:defi.zb572.xoso.zb1ec:kxjvfwpa7grmfhkxoxufq5xjltq2s5syer2rzdx7odbnrxhnjzkq`
- §8 CHANGELOG line 68, the pixel fix: `https://emem.dev/memories/by_attester/njedkglt/7zmocvinsgzdayubripuzruy7q.md`
- §9 Tessera 128-D embedding: `emem:fact:defi.zb572.xoso.zb1ec:ga2o2nufuq4s4tmirplgarpj4y5axb4644y7rftpojarlkcbqdrq`
- §10 Clay v1.5 1024-D embedding: `emem:fact:defi.zb519.faci.modA:jh2kmfiy6pbkzx3hix4qfsmrgz3vnxn64itvu3cegh3pbma73omq`
- §11 caller-signed NDVI change: `emem:fact:defi.zb572.xoso.zb1ec:jb67zixqk525p7uzjrrhwfkvixusueh7bfklzx4hpq5pfhrq3cxq`
- §12 elevation 918.0 m, May: `emem:fact:defi.zb493.xuqA.zcb5f:yqbolgeoycqkvj3zkxukb4bjw4odhpwvfzqo3fbgwf4spk45zala`
- §13 elevation 915.07 m, September: `emem:fact:defi.zb493.xuqA.zcb5f:jzxzmvomshs6di3bkgponk6p3rgfk5nyvklekj6caegx6dwcuo5q`
- §14 temperature 28.0 degC, guard test: `emem:fact:defi.zb493.zezo.zcb35:nflpddk7zsncywguwjzk5koksseqfyx4jnngkuryrnd4aykqlpfq`
- §15 signed absence, open ocean: `emem:fact:defi.zb374.toro.dEcO:jvm4xbmbenl7pzshsojtarwbk5pvhpbq62cel7vwfculuswce6xa`
- §16 the 8 stored records, one handle: `emem:bundle:6x5eoxguweqw46n3gvpaqe3e3a`
- §17 statistics rows, 0 of 72, p 0.035: `https://emem.dev/memories/by_attester/njedkglt/k2ww7uxf7umrfsvy33syzafrfq.md`
- §18 handoff and paraphrase-trap rows: `https://emem.dev/memories/by_attester/njedkglt/hyl7r2yl3ybzcegxjhxiplr4ai.md`
- §19 sizes and the authors scorecard: `https://emem.dev/memories/by_attester/njedkglt/eoe5s4arfksqtpd66rczwetviq.md`
- §20 the record and 19 withdrawals: `https://emem.dev/memories/by_attester/njedkglt/izycf6molcl5z53fkolqly57ze.md`
- §21 paraphrase-trap value, 17 Jul: `emem:fact:defi.zb572.xoso.zb1ec:jwkqm6ehelmzrwupfwyq2oqotiarexr5bdrt4xbl3znuynhurqxq`
- §22 the measurements behind the board: `https://emem.dev/memories/by_attester/njedkglt/67alr3czauetbdatbqs36mr6tq.md`
- §23 CHANGELOG line 77, encoders retired: `https://emem.dev/memories/by_attester/njedkglt/jk7pfvdydjfdf5hxs3uozqaita.md`
- §24 memory.md, TESSERA frozen: `https://emem.dev/memories/by_attester/njedkglt/f5hxjofpbmgzdialjilueeartu.md`
- §25 results table and the safety result: `https://emem.dev/memories/by_attester/njedkglt/ay2lfw4pehm52gjzyn7rnu4szq.md`
- §26 README, the device gate: `https://emem.dev/memories/by_attester/njedkglt/74gntpglvsg466a5vgevbvteme.md`
- §27 B04, 23 Sep, containing pixel: `emem:fact:defi.zb572.xoso.zb1ec:aorer7jtgzrjkjospacmula5rd65tev7uyndw3taogg7trmg2a2q`
- §28 B08, 23 Sep, containing pixel: `emem:fact:defi.zb572.xoso.zb1ec:flf5bk4qry32c3exazagp66gs2gzdhafx7heqqsslsuvn43ad5bq`