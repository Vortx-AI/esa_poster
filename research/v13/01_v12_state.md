# 01. The v12.1 board as it stands: inventory, gaps against the brief and the 39 issues, assets, hostile review

Written 2026-10-01 (UTC) for the v13 final A0. Topic: `v12_state`. Read-only research; nothing on the board, in the
figures or in emem was changed.

Labels used on every item:

- **MEASURED**: computed or counted in this session from committed files or images (command or file:line given).
- **LIVE**: fetched from a live service in this session (URL and time given; all on 2026-09-30/10-01 UTC).
- **SPEC**: what emem's docs or code say, not exercised here.
- **INFERRED**: my reading or arithmetic from the above, not a measurement.
- **UNVERIFIED**: stated by a committed file, not re-checked here.

Inputs read in full: `research/SHARED_STATE_EMEM_A0_MASTER.md` (558 lines), `poster/src/poster.v12.html` (256 lines),
`poster/build_v12.py` (121), `poster/make_figures_v12.py` (766), `research/repro/v12/CLAIMS_MAP.md` (71, byte-identical
to `research/should_do/19_V12_CLAIMS_MAP.md`, `diff` empty), `research/repro/v12/audit/hostile_review_v12.md` (183),
`research/sessions/2026-09-30_v12/README.md` (76), `research/should_do/10_EVENT_FIELD_MAP_AND_CRITIQUE.md` (419),
`16_V11_CRITIQUE_AND_DECISIONS.md` (120), `17_V11_RESPONSE_TO_FIELD_MAP.md` (59), and the 39 open issues of
Vortx-AI/esa_poster (#5 to #7, #11 to #46; GitHub MCP `list_issues`, all with 0 comments). Supporting reads:
`research/repro/v11/out/{mutation_matrix.json,summary.md}`, `research/repro/data/v8/{prevalence_summary.json,
crossruntime_table.json,token_counts.json,results.json}`, `research/repro/data/v9/rawband/results.md`,
`research/repro/v12/{data,trace,scripts}`, `research/do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md`, emem
`origin/main` 18adb67 (`docs/model.md`, `docs/paper-section-statistics-and-threats.md`, `CHANGELOG.md`,
`crates/emem-fact/src/attest.rs`). Preview crops: `/tmp/claude-0/-home-user-esa-poster/0db6b3ad-8059-51a6-bd74-2d7a97faf986/scratchpad/v13/c01_header.png` to `c12_bottom.png` and `overview.png`.

---

## 0. Findings in one screen

1. **v12.1 predates almost the whole brief.** v12.1 was committed at 2026-09-30T22:19:46Z (`git log`, 1ee1c04).
   Issues #11 to #46 were opened 22:39:52Z to 22:42:59Z and the master shared state was committed at 22:45:43Z
   (4a1567f). v12.1 was designed against issues #5, #6, #7 and the v12 hostile review only
   (`research/repro/v12/audit/intel_notes.md` lines 3 to 9). Most gaps below are therefore expected, not regressions. MEASURED.
2. **Title does not match the programme.** Board: "EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI
   Agents over Earth-Observation Products, Foundation-Model Embeddings and Signed Execution Traces"
   (`poster.v12.html:111`). Programme: "EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over
   Foundation-Model Embeddings", Poster Session 1, poster 4 of 23 (LIVE, https://agentic-eo.berlin/programme/posters/,
   HTTP 200). Four more variants are in circulation (section 3.1).
3. **Three sentences contradict the brief's identity rule (MASTER §5, issue #12).** "Name each satellite observation by
   the hash of its bytes." (`:132`); guarantees row "the source bytes / guaranteed / hash, signature, log" (`:223`);
   formula "s = Ed25519(BLAKE3(body))" (`make_figures_v12.py:718`), which emem's own code does not do: facts carry no
   signature; the attester signs a batch Merkle root (`crates/emem-fact/src/attest.rs:34, 93-133` at 18adb67; defect 32). SPEC + MEASURED.
4. **The main result is not dominant.** R1 sits in section 4 of 5, starting 708 mm down the 1189 mm board; its figure
   is 7.96 % of the page area. The SAT-042 extension occupies a full-width band of 154 mm (13.0 % of the height),
   taller than section 2 (129 mm) and section 3 (144 mm). MEASURED from the preview (section 2.3).
5. **R1 is verifier-level and self-authored.** 17 mutations of one record, one band, one run each, a model-free
   verifier, a TEST signing key for the signer-error rows (`summary.md` notes). No RAG arm, no agent, no decision
   accuracy printed although `decision_flips` is computed (A/B 6 of 15; I 0). MEASURED.
6. **No ecosystem, cost, threat model, RQ/hypotheses, invention box, fact object or prior-art matrix is on the board.**
   The words MCP, A2A, ChatGPT, Claude, Dify, registry, RAG and GeoGuard occur 0 times in the live text ("Model Context
   Protocol" appears once, in the references). MEASURED (grep of the rendered text, section 2.4).
7. **Nothing on v12.1 is fluently readable at 3 m** by the hostile review's own criterion (0.2 degree x-height). The title
   reaches 9.3 arcmin at 3 m, the punchline 7.4. INFERRED arithmetic from CSS sizes (section 2.5).
8. **Evidence that answers the brief already exists in the repo but is off the board**: a cross-runtime resolution of
   the same Keylong token through REST, raw MCP, A2A, Python SDK, TypeScript SDK, LlamaIndex, LangChain MCP adapters,
   the official MCP Python and TypeScript SDKs, and an independent blake3+cbor2 decoder (all `rehash_ok`); token cost
   counts; M15 error magnitudes; the date-substitution defect that misled 9 of 10 agents. Section 6.

---

## 1. Build, gates and figure pipeline

### 1.1 `poster/build_v12.py`: every gate it enforces (MEASURED, file:line)

| # | gate | code | what it actually checks | gap |
|---|---|---|---|---|
| 0 | figures rebuilt first | `run_figures()` :25-28 | runs `research/repro/v11/mutation_suite.py` then `make_figures_v12.py` (both `check=True`) | R1 is regenerated on every build, so `full_verification_ms` changes per run, but the printed "1.2 ms" is typed in the HTML (`:194`); only `claims_map_v12.py` (not run by the build) would catch drift |
| 1 | missing inline asset | `inline()` :31-39 | every `<!--inline:...-->` path exists, else `GATE FAIL` | none |
| 2 | prose: em dash | `prose_gate()` :46-47 | any `—` in text outside `<style>`, `<svg>`, comments | figure text is outlined paths (`svg.fonttype: path`, make_figures :50), so figure labels are never prose-checked |
| 3 | prose: en dash | :48-51 | `–` allowed only digit–digit or between uppercase alphanumerics | same |
| 4 | prose: tell words | :52-55 | 13 words: robust, seamless, leverage, cutting-edge, game-chang, revolutioni, unlock, delve, paradigm, groundbreaking, state-of-the-art, empower, synergy | does not include the words issue #21 asks to gate: first, only, truth, guarantees, proves, or spacecraft-deployment words |
| 5 | QR files | `qr_gate()` :61-69 | at least two `fig/v12/qr_*.txt`, each with a sibling `.svg` | docstring (:11) says "every QR payload matches its .txt"; the code does not decode or compare (the `qrcode` import is unused, :62) |
| 6 | one A0 page | `layout_gate()` :75-80 | exactly 1 page, 841 × 1189 mm ± 0.5 mm | none |
| 7 | footer clearance | :81-98 | bottom of `<main>` at least 2.0 mm above the top of `<footer>`; unknown layout fails | checks only `<main>` vs `<footer>`; `.page{overflow:hidden}` (html :26) would hide horizontal overflow; no per-box check |
| 8 | written PDF is one page | :112-114 | after `write_pdf` | none |
| 9 | preview | :115-116 | PNG at 3179 px width | 3179 px / 841 mm = 96 dpi; not a 300 dpi print PNG (issue #39) |

Not enforced by the build: the claims map. `research/repro/v12/scripts/claims_map_v12.py` asserts printed strings
are on the board, but only for rows without `on_board=False`; 16 of its 35 `row(` call sites pass `on_board=False`
(`grep`; the 36th match is the `def row(` line), and the build never calls it. There is no claim-status gate (issue #21). MEASURED.

### 1.2 `poster/make_figures_v12.py`: every figure (MEASURED; sizes from the `__main__` block :754-764 and the SVG headers)

Per-figure checks, all figures: `check_text()` :70-85 asserts no text below 15 pt (XS), no label clipped at the
figure edge, no overlap of glyph cores (70 % of box height). Sizes are print mm and are placed 1:1.

| figure | fn (line) | size mm | slot on board | data read | extra asserts | what it shows | page area |
|---|---|---|---|---|---|---|---|
| failure.svg | `fig_failure` :100 | 372 × 58 | Problem | **hard-coded** `COMPACTION` list :95-97 (72/72, 36/36; 20/72, 15/36; 0/72, 3/36), the only typed numbers in the pipeline | none | agreement and correctness fall together after a shared summary | 2.16 % |
| r1_mutation.svg | `fig_mutation` :122 | 468 × 170 | §4 left | `research/repro/v11/out/mutation_matrix.json` | none | 17 mutations × 9 levels, per-cell outcome and catching check, false-accept row | 7.96 % |
| eo_berlin.svg | `fig_berlin` :211 | 436 × 180 | §1 left | `research/repro/v12/data/case_berlin_stack.json`, `scene_defi.zb655.yaka.pUxe.png` + `.headers` | none | 16 of the 25 Berlin facts from 15 products fanned from a Sentinel-2C chip | 7.85 % |
| encoding.svg | `fig_encoding` :308 | 349 × 124 | §1 right | `research/repro/v12/data/v1_bands_2026-09-30.json` | sum of dims == 1792 (:312) | 43 slots / 1,792 dims, 944 hatched encoder dims, 5 provenance classes with slot counts | 4.33 % |
| eo_keylong.svg | `fig_keylong` :361 | 392 × 90 | §3 left | `case_keylong_ndvi.json`, `scene_defi.zb572.xoso.zb1ec.png` | per-satellite counts sum to rows (:377) | 141 NDVI facts 2025 to 2026 by S2A/B/C, two peaks, the R1 record circled | 3.53 % |
| eo_rondonia.svg | `fig_rondonia` :416 | 392 × 90 | §3 right | `case_rondonia_eudr.json` | categories are a known set (:431) | 10 × 10 point screen, CCI biomass grid, auditor card for cell A | 3.53 % |
| r4_bitemporal.svg | `fig_bitemporal` :493 | 445 × 68 | §2 right | `research/repro/data/contra_bengaluru.json` | as-of answers equal a hard-coded expected list (:506-510) | step plot of one DEM key, four as-of queries | 3.03 % |
| m15.svg | `fig_m15` :543 | 317 × 96 | §4 right | `research/repro/data/v8/pixel_windows.json`, `mutation_matrix.json` meta, `prevalence_summary.json` | round pixel is one row below floor (:554); recomputed NDVI equals R1 meta to 1e-12 (:557) | 5 × 5 NDVI window, named vs read pixel, decisions, checks A to I, 162/200 and 0/54 | 3.04 % |
| model.svg | `formulas()` :715 | 340 × 100 | §2 left | none (typeset strings) | none | six formulas: observation tuple, cid and signature, memory, recall, NDVI recompute, accept conjunction | 3.40 % |
| drift.svg | `formulas()` :729 | 394 × 23 | idea column | none | none | Δz = Δenv + Δsensor + Δgeo + Δencoder + ε | 0.91 % |
| score.svg | `formulas()` :733 | 345 × 24 | §5 right | none | none | s = z/(1+z), z = abs(x_device − x_anchor)/3σ | 0.83 % |
| sat042.svg | `fig_sat042` :618 | 440 × 130 | §5 left | `research/repro/v12/trace/sat042_run_stdout.txt` (regex parse :600-615) | 3 facts, 3 drift rows, layer count == profile (:614) | seven-step harness sequence, eight-layer chain with seq 2 rewritten, drift scores | 5.72 % |
| qr_try.svg | `qr_codes()` :739 | 25 native, drawn at 47.6 | header | payload `https://emem.dev/verify` | txt/svg pair exists | "Check any token" | n/a |
| qr_repro.svg | same | 37 native, drawn at 30 | bottom right | payload `https://github.com/Vortx-AI/esa_poster/tree/main/research/repro/v12` | same | "Re-run every result" | n/a |

Both QR destinations answer HTTP 200 (LIVE, `curl -L`, 2026-10-01). QR images were not decoded (no decoder installed). The
figure-number dump `poster/fig/v12/figure_numbers.json` has keys failure, r1, berlin, encoding, keylong, rondonia, r4,
m15, sat042. Default arguments in several function signatures differ from the called sizes (e.g. `fig_failure(w=372,
h=84)` is called with 58); harmless but confusing for the next editor.

### 1.3 Claims map (`research/repro/v12/CLAIMS_MAP.md`)

58 data rows (MEASURED, `grep`). Classes used: pre-reg, live, live verified, measured, recomputed, live replay,
measured (reference run), code, spec, reference. The scope note at the top of the file is honest (point samples;
266 of 780 recomputed; SAT-042 is a harness run). Printed statements with **no** claims-map row (MEASURED by reading
the board text against the map):

- "Every vector emem signed still resolves." (`:151`). No row. `section_audit_v11_2.md:274` records that
  pre-retirement vector recall was not exercised end to end. UNVERIFIED on the board.
- "SAT-042 exercises every refusal." (`:238`). No row. SAT-042 exercises three refusals (no trace; unbound digest;
  chain broken) out of the verifier's reason set (profile mismatch, missing layer, chain broken, clock non-monotonic,
  output unbound, signature invalid; `trace_truth.md` §3). Overclaim.
- "a 64-bit cell id of about 10 m" (`:136`), "cell64 address (about 9.55 m)" (model.svg), "10 m to about 11 km" (`:145`),
  "2.56 km across" (Berlin chip). No rows (sources exist: `docs/model.md:19`; `/v1/bands` CAMS text; scene bbox).
- "With all nine checks" (`:194`). Levels A to I are nine representations; A (prose), B (JSON) and C (opaque id) are not
  checks. `summary.md` itself speaks of "all six checks" (D to I). Wording error.

---

## 2. The board, panel by panel

### 2.1 Layout geometry (MEASURED from `poster/emem-poster-preview.png`, 3179 × 4495 px, by detecting the 0.8 mm section rules)

| band | from to (mm) | height | share of 1189 mm |
|---|---|---|---|
| header (navy) | 0 to 102.4 | 102.4 | 8.6 % |
| problem + idea | 102.4 to 231.5 | 129.1 | 10.9 % |
| §1 One address, every product | 231.5 to 435.2 | 203.7 | 17.1 % |
| §2 The memory model | 435.2 to 564.3 | 129.1 | 10.9 % |
| §3 Earth observation an agent can cite | 564.3 to 708.2 | 143.9 | 12.1 % |
| §4 Seventeen ways to corrupt one reading | 708.2 to 902.1 | 193.9 | 16.3 % |
| §5 How a satellite could prove what it ran | 902.1 to 1056.1 | 154.0 | 13.0 % |
| bottom row + footer | 1056.1 to 1189 | 132.9 | 11.2 % |

Structure: a vertical stack of five full-width numbered sections, each two columns. Not the brief's left/centre/right
plan (MASTER §27).

### 2.2 Inventory

Text quoted verbatim from `poster/src/poster.v12.html`; line numbers refer to that file.

**Header** (`:108-117`)

- Meta: "Agentic AI for Earth Observation · ESA Φ-lab and BIFOLD · Berlin, 19–21 October 2026" / "Poster Session 1 · 19 Oct · 17:00–18:30".
  LIVE: the schedule page says "19-21 October 2026" with Day 3 on 21 Oct and `/dates/` says "19–21 October 2026"; the home page says
  "19-20 October 2026". The board matches the schedule; the site is internally inconsistent. Session and time match the programme.
- h1 (15.6 mm): the extended title (finding 2).
- Punchline (12.4 mm, yellow): "Agreement is not evidence. The pixel is."
- Sub-line (6.8 mm): "Every number an agent cites resolves to signed bytes and names the file it came from; open-archive pixels can be re-read."
- Byline: "Jaya Kumari · Avijeet Singh · Vortx AI · avijeet@vortx.ai" + "doi:10.5281/zenodo.20706893 (v0.1.0) · github.com/Vortx-AI/emem (Apache-2.0) · emem.dev".
  LIVE (Zenodo API): record title "emem: A research on Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings",
  version 0.1.0, 2026-06-15, creators "Kumari, Jaya" and "Singh, Avijeet Singh" (surname duplicated in the record); `/latest` resolves to the same record.
- QR 1 (47.6 mm): "Check any token emem.dev/verify".
- Proves: identity and a call to action. Does not state the contribution in one sentence (MASTER §3).

**Problem** (`:123-129`, figure failure.svg)

- "Agents that agree are not agents that are right." / "Each summary or handoff re-encodes a reading: the words survive, the referent does not. This is referential drift."
- Numbers: 36/36 pairs agree, 72/72 right (full context); 15/36, 20/72 (shared summary, no pressure); 3/36, 0/72 (under pressure).
  Source: hard-coded `COMPACTION` (make_figures :95-97) = emem `docs/paper-section-statistics-and-threats.md` §2 table at 18adb67
  (Fisher one-sided p = 0.035 for the pressure arm; 0.109 "not established" for the free arm). Same file says "Six scoring bugs were
  found across two independently written scorers" and the free arm "has turned over three times". SPEC (emem-authored study); claims
  map class "pre-reg"; the 15_ claims map notes "pairs and answers share trials, so read as descriptive; two open models on one host;
  emem-authored benchmark".
- Caption: "Pre-registered compaction study, Gemma-4-12B and Qwen2.5-7B on one host. Under pressure, the 3 pairs that still agree are all wrong."
  Models UNVERIFIED here. The task is not named and is not EO (hostile review §1.3 still applies). The free-arm result (p = 0.109) is drawn with
  the same weight as the supported arm.
- Proves: in one emem-authored, two-model study, agreement survived compaction while correctness did not. Does not show EMEM fixing it.

**The idea** (`:130-140`, figure drift.svg)

- "Name each satellite observation by the hash of its bytes. Pass the name, not a sentence about it." (10.6 mm)
- Writer path: "Sentinel-2 pixel → record: cell, band, time, value → BLAKE3 → emem:fact:…"; receiver path: "resolve → re-hash → compare → re-read the pixel".
- "Names move: 'the north field' drifts; a 64-bit cell id of about 10 m does not." / "Values move: 0.4709 becomes 'about 0.47'; a fact_cid breaks if one bit changes."
- drift.svg: Δz = Δenv + Δsensor + Δgeo + Δencoder + ε, gloss "world, instrument, misregistration, model, noise: change at one pinned address".
  SPEC (whitepaper-v2); the claims map says the numeric split is not computed. The formula has no role in any result on the board.
- Proves nothing by itself (mechanism statement). Conflicts: the headline sentence (issue #12, MASTER §5, §4); the record in the writer path
  omits the source reference, which is what makes the source re-read possible.

**§1 One address, every product** (`:144-154`)

- Sub: "One 10 m cell in central Berlin, read live on 30 Sep 2026 from each product's native grid (10 m to about 11 km): 15 products, 16 signed facts, 4 of them signed absences."
- eo_berlin.svg (cell `defi.zb655.yaka.pUxe`; chip S2C_MSIL2A_20260927T101801_R065_T33UUU, 27 Sep 2026, cloud 6.51 %, 2.56 km): 16 rows, every value and fact_cid in
  CLAIMS_MAP rows 19 to 34 from `case_berlin_stack.json` (LIVE on 30 Sep, all 25 Berlin facts PASS in `eo_evidence_per_fact_checks.csv`):
  B08 0.0475; NDVI 0.195; S1 VV γ⁰ −2.82 dB, 1 px; GLO-30 36.6 m (DSM), "2021 release"; MODIS LST 297.4 K (1 km), 29 Aug 2026 8-day; WorldCover class 50;
  CCI biomass 0 t/ha, 2022; GSW 0 %; Hansen tree cover 2000 0 %; GFC2020 V4 not forest; CAMS NO₂ 12.3 µg/m³ 30 Sep 18 UTC; Overture 0 buildings;
  absences for SoilGrids, CHIRPS, TMF, FIRMS. Provenance classes of the 16: direct_sensor 3, deterministic_index 1, model_output 9, human_curated 1, unclassified 2 (claims map).
- Right: "How emem encodes a memory", encoding.svg: 43 slots, 1,792 dims, bands_cid mesoyti3…; 944 of 1,792 hatched encoder dims (geotessera 128, clay_v1 384,
  prithvi_eo2 384, galileo 48, LIVE ontology copy); slots per class model_output 23, deterministic_index 7, direct_sensor 6, human_curated 5, unclassified 2;
  "what a verifier leans on" column; "Defined for fits and devices: estimator ... and attested execution".
- Paragraph: "Each fact carries a provenance class: how far a verifier can check it. Embeddings are memories too. Each vector is a model-output fact bound to its encoder
  checkpoint and recipe, so a new encoder shows up as Δencoder, not as change on the ground. Every vector emem signed still resolves."
- Proves: one address can key many products, each fact resolvable and verifiable (LIVE, 25/25 PASS). Does not prove co-registration across grids (issue #20), and the
  encoding bar is an ontology (schema) figure with no result. The CCI version is dropped; LIVE fact `yc5qjlgh…` (Rondônia) names `esa.cci.biomass.v7`,
  file `...fv7.0.tif`, so "ESA CCI Biomass v7.0" is now the correct fact-level label (the hostile review's v6.0 came from the registry text). "a signed model
  checkpoint" is what a verifier leans on for model_output per the ontology (SPEC), but WorldCover, CCI, Hansen and GFC2020 facts carry no checkpoint (INFERRED from the
  LIVE fact bodies: source scheme and file URL only).

**§2 The memory model** (`:157-166`)

- Sub: "Six definitions from emem's specification; every panel on this board is an instance of them." (SAT-042 is not an instance of these six; INFERRED.)
- model.svg (SPEC, docs/model.md and memory.md): O = (a, b, t, v, u, p, s) "cell64 address (about 9.55 m)...signature"; cid(O) = BLAKE3(CBOR_canonical(O)),
  s = Ed25519(BLAKE3(body)); M = (O*, E*); recall(M, a, b | t*, τ); NDVI = (DN8 − DN4)/(DN8 + DN4 + 2 offset), offset −1000; accept = hash ∧ cell ∧ Ed25519(σ) ∧ leaf ∈ log ∧ f(DN) = v ∧ COG[r,c] = DN.
  - Code disagrees with two of these (SPEC vs code). The signature: `crates/emem-fact/src/attest.rs:34` "v0: ed25519(blake3(batch_root || registry_cid || schema_cid))",
    `build_and_sign_v1` :93-133 builds `merkle_root_v1(&leaves)`. The LIVE fact body (`GET /v1/facts/oj5cecci…`, HTTP 200) has `signer` but no signature field.
    Defect 32. "canonical": defect 33 says emem-CBOR is ciborium in declaration order, not RFC 8949 §4.2.1 sorting, while the footer cites RFC 8949. UNVERIFIED here beyond the defect text.
  - The "accept" row binds "cell" only; level E in R1 checks cell, band and tslot.
- "Memory on two clocks", r4_bitemporal.svg: Bengaluru cell `defi.zb493.xuqA.zcb5f`, band `copdem30m.elevation_mean`, tslot 0. 918.0 m signed 2026-05-28T19:54:32Z
  (`open_meteo_copdem90m@1`); 915.0712280273438 m first signed 2026-08-11T09:39:36Z (`copernicus_dem_30m_aws_pixel@1`), 7 signings; as of 1 May nothing, 15 Jun 918.0,
  12 Aug 915.07, 29 Sep 915.07 (`contra_bengaluru.json`; claims map "live replay"; figure recomputes and asserts).
- Caption: "Bengaluru: 918.0 m from the 90 m Copernicus DEM in May, 915.07 m from the 30 m COG since 11 Aug. Nothing was overwritten. Asked 'as of 15 Jun', emem still answers 918.0, and both answers verify."
- Proves: a later signing does not overwrite an earlier one, and an as-of query on transaction time returns the earlier value. Limits (INFERRED): valid time is constant
  (tslot 0, static DEM), so only one of the "two clocks" moves; the change is a provider substitution (GLO-90 via Open-Meteo to GLO-30 on AWS; emem labels it
  `same_attester_provider_substitution`), not a newer observation of the world; "signed 7 times" is 7 identical re-signings (defect 5); `as_of_signed_at` is a
  string compare in code (defect 35; exact for these UTC second-precision stamps per 15_ claims map). The agent-handoff meaning (what the agent knew when it cited)
  is not stated.

**§3 Earth observation an agent can cite** (`:170-184`)

- Sub: "All 780 facts pulled for sections 1 and 3, including the 757 drawn here, were re-hashed, signature-checked and found in the log on 30 Sep 2026."
  Source `eo_evidence_verification.md` and the per-fact CSV (MEASURED tally this session): 780 facts (berlin 25, keylong 155, rondonia 600), all 20 check columns pass;
  `recompute` pass 266, n/a 514; verifier `verify_lib.py` uses only blake3, cbor2, pynacl and "imports no emem code"; pinned key `777er3yi…` published in four
  well-known places, "No independent party vouches for it". Raster reads (DEM, WorldCover, CCI, GSW, Hansen, GFC2020, TMF, CAMS, MODIS, DMSP, Overture) were not re-read from
  upstream. So on the board's own evidence: byte integrity, binding, receipt, log inclusion 780/780; recompute 266/780; upstream re-read 0/780.
- Keylong (eo_keylong.svg): "Two seasons, three satellites, one field"; 141 NDVI facts in 2025 to 2026 of 155 (S2A 15, S2B 61, S2C 65); peaks 0.79 on 6 Aug 2025 (`rc2mpyys`) and
  0.73 on 27 Jul 2026 (`xbqqfk5r`); circled record 0.4709, 25 Sep 2026 (`oj5cecci…`). The inset chip is the S2A 25 Sep 2026 scene (headers: cloud 10.84 %) and is unlabelled.
  Caption: "Keylong, Lahaul (India): 141 Sentinel-2 L2A NDVI facts at one 10 m cell, Jan 2025 to Sep 2026. Circled: the record that section 4 corrupts."
  Descriptive, not a finding (issue #36 quotes this pattern as the bad example). Single-date drops (about 0 in Oct 2025; 0.27 in Aug 2025, visible in crop c07) are not
  explained; SCL / baseline note not added (session README: "Not changed").
- Rondônia (eo_rondonia.svg): "A deforestation screen an auditor can re-run"; 100 cells × 6 bands = 600 facts; categories 3 / 1 / 33 / 20 / 43; flagged loss years 2023, 2024, 2024;
  auditor card for cell A `defi.zb391.taza.zcc31`: Hansen loss 2023, tree cover 2000 100 %, GFC2020 V4 forest, TMF deforestation 2023, CCI 208 t/ha, NDVI 0.43 (scene 28 Sep, date not printed).
  Caption: "Rondônia (Brazil): 100 point cells 740 m apart, 600 facts. Flag: forest in 2020, tree-cover loss after 31 Dec 2020. A screen, not a due-diligence statement."
  LIVE: cell A's GFC2020 fact names scheme `jrc.gfc2020.v4` and URL `.../GFC2020/LATEST/tiles/JRC_GFC2020_V4_N0_W70.tif` (a mutable "LATEST" path, no content hash; fn_key still
  `jrc_gfc2020_v3_pixel@1` with arg "v4"; reader `cog-pixel-floor@2`); signed 2026-09-30T19:12:40Z, i.e. minted by the pull itself (defect 29).
  Missing vs MASTER §21: "not parcel polygons; not a regulatory determination". No imagery; biomass grid does not enter the flag.
- Proves: every input of a screen resolves to a signed, logged fact an auditor can fetch. Does not prove the screen is right.

**§4 Seventeen ways to corrupt one reading** (`:187-200`)

- Sub: "Agent B receives the Keylong record circled in section 3 after one corruption. A deterministic verifier, with no model in the loop, decides whether B acts."
- r1_mutation.svg (MEASURED, `mutation_matrix.json`): false accepts per level A 15/15, B 15/15, C 13/16, D 12/16, E 9/16, F 3/16, G 2/16, H 1/16, I 0/16.
  Groups: paraphrase/relay (M1 to M3), misbinding (M4 to M7), forgery without the key (M8 to M13), the trusted signer errs (M14 to M16), out of scope (M17). G0 control accepted at
  every level (false refusal 0 of 1, not printed as such). Amber ids = "seen in production": M2 (§21 trap; R3 rounded arm), M4 (§4 relabelled token), M5 (§6 cube member date),
  M15 (162 of 200), M17 (Maasvlakte entity). Only M15's production case is explained on the board.
  Not printed but computed: decision flips A/B 6 (M2, M8, M12, M13, M14, M15), C to E 5, F and G 2, H 1, I 0; leave-one-out (`summary.md`): without E M4, M5, M6; without F
  M9 to M12; without G M16; without H M14; without I M15; without D none (hash subsumed by the signature).
  Scope (MEASURED, `summary.md` notes): one record, one band, one run; "T2 rows use a TEST key the verifier is told to trust"; the re-read (I) compares with a committed
  25 Sep COG window and "does not follow a forged scene id".
- Take line: "Prose and JSON pass all 15 corruptions they can carry. With all nine checks, none of the 16 in-scope cases gets through; one full check takes 1.2 ms offline, with the source window cached."
  1.187 ms, level I, 200 reps (claims map row 42). The network cost of a real re-read is not given (the sealed v11 board had "1.17 MB read from a 2.02 GB scene").
- M15 (m15.svg): "M15 in production: the right record, the wrong pixel"; 5 × 5 NDVI window recomputed from DNs (offset −1000); named pixel (floor, row 2 col 2) 0.4709 "do not irrigate";
  pixel read by the old reader (round, row 3) 0.3016 "irrigate"; rule "irrigate iff NDVI ≤ 0.4705"; "Seen in 162 of 200 sampled records before the fix; 0 of 54 after."
  Caption: "The old reader rounded the pixel centre instead of flooring it, and so read the row below. It signed what it read, so every check up to recompute passes. Before the fix: 162 of 200 sampled records (75 to 86 %, Wilson 95 %). After: 0 of 54."
  Source `prevalence_summary.json`: pre n 200, 200 cells, 164 scenes, 19 bands, providers E84 192 / PC 8, signed 2026-05-14 to 2026-09-27; 162 match round-not-floor, 0 floor-not-round,
  38 where both rules pick the same pixel; post n 54, 44 cells, 36 scenes, providers PC 54, signed 2026-09-28 to 2026-09-30. Where the rules differ, index error median 0.027,
  p90 0.113, max 0.301 (n 121); reflectance error median 0.0097, max 0.120 (n 41) (MEASURED). Caveats not on the board (INFERRED): the post-fix sample is all Planetary Computer and 2 days
  wide, so provider and fix are confounded; the neighbour can be east, south or south-east (`audit_v11/poster_evidence_audit.md` A44, A64), "10 m south" is true of this one record only.
  CHANGELOG.md:68 at 18adb67 (SPEC): the rounding affected "Every COG-backed band (Hansen, JRC GFC2020 and TMF, WorldCover, Cop-DEM, CCI biomass, Sentinel scenes, ...) ... from the first commit",
  so the EUDR bands were exposed too; the board shows only Sentinel-2.
- Proves: at verifier level, each added check stops a named class; only a source re-read stops a signer's wrong-pixel read; the production reader made that error at scale.

**§5 How a satellite could prove what it ran** (`:203-215`)

- Sub: "SAT-042 is a scripted pass in emem's test harness, not a spacecraft; run on 30 Sep 2026."
- sat042.svg (MEASURED from `sat042_run_stdout.txt`, emem 04b40c5, run 2026-09-30T19:14:15Z, two runs byte-identical): Enrol (8 layers, orbital.satellite.v1) / Write, no trace REFUSED /
  Capture 3 NDVI payloads SIGNED / Smuggle a 4th fact REFUSED (digest cyzwak…) / Honest batch ADMITTED (3 facts, 1 trace) / Score vs anchor 2 consistent 1 contradicted (0.05, 0.15, 0.88) /
  Rewrite one log: segment 2 edited, chain broken at seq 3.
- Text: "Open archives enter emem by recomputation. A device cannot be recomputed, so its profile demands a signed OS execution trace: eight layers for orbital.satellite.v1, with every payload digest bound inside."
  "On the gated write paths, a write with no trace is refused, and so is a fact the trace never emitted. Rewrite one log segment and the verifier names the broken link."
  Take: "A trace proves what ran, not that the sensor was right. A drift anchor scores each claim:" + score.svg. Caption: "The harness uses one fixed anchor, 0.6402 ± 0.02 (1σ), for all three captures. 3σ scores 0.5 and 9σ scores 0.75, both pinned by emem-trace's tests."
- Status (MEASURED from `trace_truth.md`): implemented and tested (emem-trace 22 passed, 1 ignored; emem-storage gate subset 23 passed); LIVE on 30 Sep: 1 device (generic Linux host), 17 platforms all
  `candidate`, `orbital.satellite.v1` candidate, 0 of 43 bands `attested_execution`. The example was compiled in a harness crate; `cargo run -p emem-primitives --example satellite_downlink` was not run.
- Conflicts: defect 36 (SPEC): "a fact binds to a device trace by H(cbor(value)) alone; band and cell are not checked; the drift-anchor score is not wired into ingest" vs "with every payload digest bound inside" and
  "A drift anchor scores each claim". The admitted batch includes the 0.2103 value that step 6 calls contradicted.
- Proves: the trace protocol refuses the three scripted forgeries in a harness. Does not prove any spacecraft capability.

**Bottom row** (`:218-248`)

- "What a verified token guarantees" (table): the source bytes / guaranteed / hash, signature, log; the observation / bound / cell, band, time signed; re-read confirms; the derivation / recomputable /
  fixed formula, signed inputs; the upstream file / named / scene id and COG URL; the value's accuracy / inherited / the product's own validation; the entity / out of scope / a shared label (M17).
  Row 1 names the wrong object (the hash and signature fix the record bytes, not the source bytes). No row for decision correctness. "verified" is unqualified.
- "Objections, answered": "A signature does not make a value true." / "Agreed. It fixes which bytes were served. Truth is tested by re-reading the pixel; accuracy comes from the product's own validation."
  / "Why not STAC, openEO or C2PA?" / "STAC names the scene, openEO the process, C2PA the asset. emem signs the one value an agent cites and names the scene and file it came from."
  / "Is a satellite writing to emem today?" / "No spacecraft is enrolled. emem.dev re-checks any signed trace from its one enrolled Linux host; SAT-042 exercises every refusal."
- Conclusions: "1 Agents hand each other a signed observation, not a sentence about it." "2 One address joins every product, so an EO screen can be re-run fact by fact." "3 Only the full chain refuses all 16; M15 needs the pixel re-read."
- Try box: QR 2, "Re-run every result. Data, scripts and claims map: research/repro/v12".

**Footer** (`:251-254`, 4.2 mm)

- References: Sentinel-2 L2A PS; CEOS ARD; Copernicus DEM GLO-30/90; Hansen 2013; JRC GFC2020 V4 and TMF; ESA CCI Biomass; Reg. (EU) 2023/1115; BLAKE3; RFC 6962, 8032, 8949; STAC 1.0; openEO; W3C PROV-O; C2PA 2; Model Context Protocol; TESSERA arXiv:2506.20380; Earth Embeddings as Products arXiv:2601.13134.
- Reproducibility: "Mechanisms and formulas read from emem's code and docs/model.md at 04b40c5; measurements 29 to 30 Sep 2026 on emem.dev. Every number maps to its file and script in research/repro/v12/CLAIMS_MAP.md at github.com/Vortx-AI/esa_poster."
  LIVE/MEASURED: 04b40c5 is not in the local emem clone (73 commits, `origin/main` 18adb67); `git ls-remote` shows remote main at 8e9b401. The commit cannot be checked from this session
  (GitHub API access to Vortx-AI/emem is not enabled). The research brief names 18adb67 as the source of truth; the board and trace files name 04b40c5. Pick one and print it once.

### 2.3 Visual dominance (MEASURED)

| content | share of page area (figure only) | share of height (band) | brief's status |
|---|---|---|---|
| R1 mutation matrix | 7.96 % | §4: 16.3 % (with M15) | main result (MASTER §6, §9) |
| M15 | 3.04 % | inside §4 | strongest finding (MASTER §10) |
| Berlin stack | 7.85 % | §1: 17.1 % (with encoding) | example |
| SAT-042 + score | 6.55 % | §5: 13.0 % | extension, must not compete (MASTER §20) |
| encoding + model formulas | 7.73 % | §1 right + §2 left | implementation detail (MASTER §22, issue #18) |

The largest band on the board is §1 (a product stack and a schema bar). R1 is the fourth band from the top.

### 2.4 Word count and vocabulary (MEASURED, rendered text without `<head>`, `<style>`, comments, SVG)

- 1,029 live words (the hostile review counted 894 on v12 from the PDF text layer; v12.1 added section 2 and more captions).
- Occurrences: "guarantee" 2, "prove(s)" 2 (plus "provenance"), "truth"/"true" 2, "Only" 1, "verified" 1 (unqualified), "decides" 1 (the verifier), "satellite" 5;
  MCP 0, A2A 0, ChatGPT 0, Claude 0, Dify 0, registry 0, RAG 0, GeoGuard 0, overhead/cost/latency 0.

### 2.5 Legibility by viewing distance (INFERRED arithmetic; criterion and x-height/em 0.518 from hostile_review_v12.md §7)

Fluent reading needs an x-height of about 12 arcmin. Required em size: 20.2 mm at 3 m, 6.7 mm at 1 m, 2.0 mm at 30 cm.

| text | em (CSS) | arcmin at 3 m | arcmin at 1 m |
|---|---|---|---|
| title | 15.6 mm | 9.3 | 27.8 |
| punchline | 12.4 mm | 7.4 | 22.1 |
| problem h2 / idea headline | 10.4 / 10.6 mm | 6.2 / 6.3 | 18.5 / 18.9 |
| section heads | 10.0 mm | 5.9 | 17.8 |
| body p | 6.8 mm | 4.0 | 12.1 |
| captions, table | 5.4 / 5.5 mm | 3.2 | 9.6 |
| figure floor (15 pt) | 5.3 mm | 3.1 | 9.4 |
| footer | 4.2 mm | 2.5 | 7.5 |

Nothing reaches the 3 m threshold. At 1 m only body text and larger. Captions, the guarantees table and every figure label need about 0.8 m.

---

## 3. Status against the master shared state (§1 to §30)

Status: SATISFIED / PARTLY / NOT / N/A. "Conflicting text" is verbatim from v12.1.

### 3.1 Title (not a numbered section, but binding)

Five variants exist (MEASURED/LIVE): programme and brief "…for AI Agents over Foundation-Model Embeddings"; v12.1 h1 "…over Earth-Observation Products, Foundation-Model Embeddings and Signed Execution Traces";
v12.1 `<title>` (`:5`) "…over satellite observations and signed execution traces (A0 poster, v12.1)"; `AGENTS.md` line 3 "over ~~Foundation-Model Embeddings~~ Satellite Observations and Signed Execution Traces";
Zenodo "emem: A research on Content-Addressed, …over Foundation-Model Embeddings". The sealed v11 board on this branch uses the programme title exactly. Tension to resolve: the programme title
puts embeddings in the title while MASTER §19 says embeddings are not a co-equal contribution.

| § | topic | status | v12.1 evidence / conflicting text | missing |
|---|---|---|---|---|
| 1 | one argument, visible finding, dominant figures, concise text | PARTLY | five co-equal numbered sections; 1,029 words; take lines exist in §4 and §5 only | one argument; R1 dominant |
| 2 | diagnosis | N/A (describes v12.1) | every bullet confirmed: co-equal concepts (§1 to §5), experiment not dominant (§2.3), CID vs source conflated (`:132`, `:223`), no threat model, no baselines beyond prose/JSON/opaque id, no ladder, no cost, no replication hierarchy, no ecosystem, SAT-042 and embeddings at section/title level | |
| 3 | hero "Agents hand each other evidence references, not paraphrases." | PARTLY | hero is "Agreement is not evidence. The pixel is."; close forms are demoted: "Pass the name, not a sentence about it." (idea), conclusion 1 "Agents hand each other a signed observation, not a sentence about it." (5.9 mm) | the sentence as hero; "The pixel is." makes the pixel the arbiter (same failure as the banned "satellite decides") |
| 4 | invention boundary | NOT | "Name each satellite observation by the hash of its bytes." reads as content addressing being the invention; BLAKE3, Ed25519, CBOR, RFC 6962 appear only as formulas and references | an invention box; enabling-technology list |
| 5 | source artifact → record → BLAKE3 → signed fact | PARTLY | writer path order is right ("Sentinel-2 pixel → record: cell, band, time, value → BLAKE3 → emem:fact:…") but the record omits the source; headline `:132` and table row "the source bytes / guaranteed" contradict it | the four-box diagram with the source reference inside the record |
| 6 | A → handoff formats → corruption → B → outcome → boundary | PARTLY | §4 sub "Agent B receives the Keylong record … after one corruption"; columns A to I | Agent A; RAG format; outcome labels accept/refuse/detect; boundary step; dominance |
| 7 | RQ1 to RQ4 | NOT | none printed | all four |
| 8 | H1 to H3 | NOT | none printed | all three |
| 9 | main experiment (5 conditions, 10 mutation groups, 8 reports) | PARTLY | conditions: prose, JSON, opaque id, EMEM depths D to I; no RAG. Groups: value (M1, M2, M8), cell (M4, M9), time (M5, M10), band (M6), source (M11), derivation (M12), stale (M5), signature/CID (M3, M7, M13), entity (M17); no unit. Reports: denominator yes; false acceptance yes; correct refusal yes (letters); decision accuracy computed not printed; latency 1.2 ms only; token/storage/network none; models/runtimes none ("no model in the loop"); independent vs system-generated not labelled | RAG arm, unit mutation, decision row, overheads, independence labels |
| 10 | M15 prominent, "the right record, the wrong pixel", record integrity ≠ measurement correctness | PARTLY (mostly) | h3 "M15 in production: the right record, the wrong pixel"; caption "It signed what it read, so every check up to recompute passes"; 162 of 200 | prominence (h3 in a right column, 3.04 % area); the explicit "≠" statement; the all-COG-bands scope; error magnitude |
| 11 | ladder L0 to L5 with CHECKABLE/RECOMPUTABLE/INHERITED/PARTIAL/OUT OF SCOPE | PARTLY | six-row table with guaranteed/bound/recomputable/named/inherited/out of scope | vocabulary; L5 decision row; per-layer counts (780/780, 266/780, 0/780 re-read); row 1 fix |
| 12 | threat/trust model | NOT (implicit only) | R1 group names "forgery without the key", "the trusted signer errs" | attacker can/cannot box; out-of-scope list; cryptographic/source/measurement trust split; pinned-key status ("No independent party vouches for it", verification.md) |
| 13 | Bengaluru timeline, "what did the agent know as of 15 Jun" | PARTLY | step plot and caption ("Asked 'as of 15 Jun', emem still answers 918.0") | agent framing; not generic versioning; say it is a source substitution on transaction time |
| 14 | prior-art boundary incl. GeoGuard, RAG, PROV | PARTLY | Q&A: "STAC names the scene, openEO the process, C2PA the asset. emem signs the one value an agent cites and names the scene and file it came from." | PROV, RAG, GeoGuard; matrix form; the "critical answer" sentence |
| 15 | one real fact object | NOT (pieces only) | cid prefixes in Berlin rows and the Rondônia card; tuple formula | the exploded object (cell, band, time, value, source, CID, signature) |
| 16 | ecosystem mandatory | NOT | 0 mentions; "Model Context Protocol" in references only | whole panel |
| 17 | integration manifest | NOT | none | manifest |
| 18 | cost and performance | NOT (1 number) | "one full check takes 1.2 ms offline, with the source window cached" | token overhead, reread cost, storage, network |
| 19 | embeddings as extension ("Derived representations are addressable too.") | PARTLY / CONFLICT | "Embeddings are memories too." paragraph and 944 hatched dims on the board's largest band; "Every vector emem signed still resolves." unsourced | encoder-change-creates-new-fact demonstration, or move behind QR (and reconcile with the programme title) |
| 20 | SAT-042 as "Extending verification to execution", "Reference implementation / scripted harness; no spacecraft enrolled." | PARTLY | "How a satellite could prove what it ran"; "SAT-042 is a scripted pass in emem's test harness, not a spacecraft"; still in h1 ("Signed Execution Traces"); full-width 154 mm band; "SAT-042 exercises every refusal" | size reduction; title; exact status line |
| 21 | Keylong, Bengaluru, Rondônia with cell/date/product/observation/purpose/limit; EUDR "point samples; not parcel polygons; not a regulatory determination" | PARTLY | all three kept; Rondônia "A screen, not a due-diligence statement." | Keylong chip unlabelled; captions descriptive; EUDR phrase incomplete; no image answers a question except M15 |
| 22 | 3 m / 1 m / 30 cm | NOT | §2.5 | typography plan |
| 23 | active verbs | PARTLY | resolve, re-hash, compare, re-read, refuses, signed; section titles are noun phrases ("The memory model", "One address, every product") | verb-led titles and captions |
| 24 | question / mechanism / result + limitation per panel | PARTLY | §4 and §5 have take lines; §1, §2, §3 have no measured result line | rhythm in every panel |
| 25 | action QRs, 20 s demo | PARTLY | 2 QRs: "Check any token", "Re-run every result" | inspect the record, view the demo, read the methods, discover integrations; the demo |
| 26 | must not become … | PARTLY at risk | cryptography tutorial (six formulas incl. Ed25519, Merkle log, COG index), schema reference (43 slots, 1,792 dims, bands_cid), spacecraft claim (h1 + §5), disconnected demos (Berlin, Keylong, Rondônia, Bengaluru, SAT-042 cells: five places) | |
| 27 | target structure | NOT | vertical stack of five sections | column plan with ecosystem band |
| 28 | seven 30-second questions | PARTLY | Q1 yes; Q2 partly (wrong wording); Q3 yes; Q4 yes (table + objection 1); Q5 partly (no RAG/GeoGuard); Q6 no; Q7 yes (QR, claims map) | Q2, Q5, Q6 |
| 29 | P0/P1/P2 | P0: 1 NOT, 2 PARTLY, 3 NOT, 4 PARTLY, 5 NOT, 6 NOT, 7 NOT (density rose). P1: 8 NOT, 9 PARTLY, 10 NOT, 11 PARTLY, 12 PARTLY, 13 NOT, 14 NOT, 15 NOT. P2: 16 PARTLY, 17 NOT, 18 NOT, 19 NOT | | |
| 30 | science first, protocol second, ecosystem third | NOT | protocol and EO examples lead; no ecosystem | |

---

## 4. Status against the 39 open issues

All 39 have 0 comments (GitHub MCP `search_issues`, 2026-10-01). #5 to #7 were open when v12.1 was built; #11 to #46 were opened after it.

| # | ask (short) | status | exact v12.1 text or fact that conflicts / partial evidence |
|---|---|---|---|
| 5 | rebuild around adversarial handoff; cut detail 40 %; mutation table focal; keep bytes → BLAKE3 → CID and resolve → re-hash → compare; state integrity ≠ truth, upstream, entity, complementary to guardrails/RAG | PARTLY | both invariants present (`:133-134`); "A signature does not make a value true." ; "the entity / out of scope"; but R1 is band 4 of 5 (7.96 % area); words rose 894 → 1,029; section 2 adds six formulas; guardrails/RAG never named |
| 6 | benchmark: prose / raw value / RAG / EMEM token; 12 mutation types; 4 to 6 models; FA/FR/detection/latency/token overhead; n and CIs | NOT | verifier-level only ("A deterministic verifier, with no model in the loop"); no RAG; unit, checkpoint and embedding mutations absent; no CIs (deterministic) |
| 7 | bind upstream artifact identity; mark location-only; separate five integrities | PARTLY | "the upstream file / named / scene id and COG URL"; no "upstream identity unverified" label; LIVE facts carry no source hash (defect 25) and GFC2020 points at a mutable `LATEST` URL; no semantic-correctness row |
| 11 | invention boundary box; no ambiguous novelty | NOT | "Name each satellite observation by the hash of its bytes." ; no invention taxonomy in the claims map |
| 12 | correct fact-CID vs source-pixel wording; add source → record → CID diagram | NOT | "Name each satellite observation by the hash of its bytes." (`:132`); "the source bytes / guaranteed / hash, signature, log" (`:223`); "s = Ed25519(BLAKE3(body))" (model.svg) contradicts attest.rs (batch root) |
| 13 | no satellite-as-arbiter; limitation in first screenful | PARTLY | banned line removed, but "Agreement is not evidence. The pixel is." and "Truth is tested by re-reading the pixel" remain; the boundary is at 1056 mm+ |
| 14 | SAT-042 as extension, harness status everywhere | PARTLY | sub says "scripted pass … not a spacecraft"; h1 still "Signed Execution Traces"; section title "How a satellite could prove what it ran"; "SAT-042 exercises every refusal"; 13.0 % of height |
| 15 | prior-art matrix incl. GeoGuard, PROV, RAG | PARTLY | Q&A covers STAC, openEO, C2PA only |
| 16 | agent-to-agent handoff as primary result; verifier-level vs decision-level | PARTLY | honest verifier-level label; no agent run; `decision_flips` not printed; no models/runtimes |
| 17 | guarantee ladder, one layer per claim, no bare "verified" | PARTLY | table present; "What a verified token guarantees", "both answers verify" |
| 18 | reduce mechanism density 40 % | NOT | model.svg accept conjunction, "eight layers for orbital.satellite.v1", "43 slots, 1,792 dimensions (… bands_cid mesoyti3…)", RFC numbers; density up |
| 19 | temporal claim falsifiable; beyond DB versioning; stale/current handoff case | PARTLY | Bengaluru panel; M5 "older record passed as current" is in R1 (caught at E); no DB-versioning distinction; no recovery-of-cited-state result |
| 20 | "one address, every product" precise; common addressing layer; native resolution | PARTLY | sub "from each product's native grid (10 m to about 11 km)"; conclusion 2 "One address joins every product" overstates; per-row resolution only for LST, CCI, S1 |
| 21 | claim-status gate in the build; novelty words; spacecraft words | NOT | §1.1: no status gate; "only", "proves", "guarantees", "truth" pass the prose gate |
| 22 | attack-questions file | PARTLY (off-board) | hostile_review_v12.md §8 (28 objections with spoken answers) and audit_v11 C-questions exist; not the requested file with every listed question |
| 23 | high-information verbs | PARTLY | receiver path is verb-led; section titles are nouns |
| 24 | one memorable hero sentence without jargon | NOT | "Agreement is not evidence. The pixel is." needs EO context; not the handoff sentence |
| 25 | question / mechanism / result per panel | PARTLY | §4 take line only close; §1 to §3 lack result lines |
| 26 | failure → intervention → result visual spine | NOT | five stacked sections; no shared glyphs for agent, evidence, mutation, verification |
| 27 | R1 as hero figure with n, scope, limitation | PARTLY | n row printed ("15/15 … 0/16"); limitation (one record, one band, test key, self-authored) not in figure; not hero-sized |
| 28 | exploded evidence object | NOT | none |
| 29 | two-sided guarantee boundary graphic | PARTLY | one-sided table; "history/as-of", "declared derivation", "physical truth", "decision correctness" absent |
| 30 | prior-art layer diagram | NOT | text Q&A only |
| 31 | every image answers a question, annotated | PARTLY | Berlin chip annotated; M15 window is the one correct/wrong image; Keylong chip unlabelled; Rondônia has no image |
| 32 | "same place, different time" figure | PARTLY | step chart with numbers first |
| 33 | 3 m / 1 m / 30 cm hierarchy | NOT | §2.5 |
| 34 | task-specific QRs, tested mobile path | PARTLY | 2 verb-led QRs, both HTTP 200; no record / methods / demo QRs; mobile path not tested here |
| 35 | 20 s demo | NOT | none |
| 36 | captions as claims | PARTLY | M15, Bengaluru, problem captions state findings; Keylong caption is the issue's "bad" pattern |
| 37 | no internal history on the face | PARTLY | strike gone; remaining: "research/repro/v12" (`:246`), "…/v12/CLAIMS_MAP.md" and "at 04b40c5" (`:253`), "(v0.1.0)" (`:114`), PDF title "(A0 poster, v12.1)" |
| 38 | one-line conclusion: mechanism + evidence + limit | PARTLY | three separate lines; none carries the limit |
| 39 | media asset pack | NOT | PDF and a 96 dpi preview only |
| 40 | ecosystem map on the A0 | NOT | 0 surfaces printed |
| 41 | integration manifest with evidence status | NOT | none |
| 42 | ecosystem as contribution-to-deployment bridge | NOT | none |
| 43 | same evidence, different agent | NOT on board | evidence exists off-board (§6.1) |
| 44 | install / discover destinations | NOT | none |
| 45 | ecosystem numbers only if sourced | N/A | no ecosystem numbers printed |
| 46 | restrained platform marks | NOT | none |

---

## 5. What the hostile review of v12 found, and what v12.1 did with it

Source: `research/repro/v12/audit/hostile_review_v12.md` (review of v12, not v12.1; senior EO scientist stance, 90 s at the board; PDF rendered at 110 dpi and 300 dpi strips).

### 5.1 The review's structural findings (§1, §2, §4, §5, §6, §7)

- Reading path: the header raised a question (the strike) it did not answer; the punchline "When agents disagree, the satellite decides." contradicted the problem headline; the problem
  chart did not show "agree and wrong" directly and was not EO; §1 held two unrelated figures (Berlin stack and encoding bar); §2/§3 inverted; the Bengaluru clock panel was an orphan;
  780 vs 757 did not close; SAT-042 had no place, anchor or score definition; the conclusions did not conclude §3 or §4; two claims-map addresses.
- Title: "Satellite Observations and Signed Execution Traces" overclaimed (9 of 16 Berlin facts model_output; 23 of 43 slots model_output; traces are a harness protocol); striking
  "Foundation-Model Embeddings" in a Φ-lab room was a risk; proposed "…over Earth-Observation Products, with Signed Execution Traces".
- EO correctness table for all 16 Berlin rows (B08 unnamed; S1 coefficient and single pixel; GLO-30 is a DSM; MODIS 1 km and Terra drift; CCI v7 vs registry v6.0; GFC2020 version and
  non-binding status; CAMS is an Open-Meteo relay forecast; Overture not EO; FIRMS absence of detection).
- EUDR: tree-cover loss is not deforestation; JRC map non-binding and versioned (V3 withdrawn, 404); a 740 m lattice covers about 0.02 % of the area it spans.
- SAT-042: plural present tense claimed capability; candidate profile omitted; ungated `POST /v1/attest_cbor` at 04b40c5 [memory]; same anchor for three cells; undefined score; "admitted a contradicted reading?".
- WIP framing: strike, `should_do` path, code-internal phrases, DOI v0.1.0 with the old title.
- Legibility: at 1.5 m only title, punchline and section heads are fluent; 894 words.

### 5.2 The 28 ranked objections and their v12.1 disposition (MEASURED against `poster.v12.html` and `make_figures_v12.py`)

| # | objection (short) | severity | v12.1 |
|---|---|---|---|
| 1 | no satellite has proved what it ran | LTR | applied to §5 title/sub and Q&A; h1 still says "Signed Execution Traces"; "SAT-042 exercises every refusal" (overclaim, new) |
| 2 | punchline contradicts problem | LTR | changed to "Agreement is not evidence. The pixel is." (review proposed "Re-read the pixel"); now conflicts with issues #13, #24 |
| 3 | embeddings struck while 9 of 16 facts are model outputs | LTR | strike removed; embeddings kept in title and §1 |
| 4 | attest_cbor ungated at 04b40c5 | LTR if unfixed | "On the gated write paths" added; fix status not checked here (UNVERIFIED) |
| 5 | "re-reads to the pixel" overclaims | costly | applied verbatim |
| 6 | "at the cell" for 1 km / 11 km products | costly | applied verbatim |
| 7 | "the observation: guaranteed" | costly | "bound … re-read confirms" applied; row 1 "the source bytes / guaranteed" remains wrong (new finding, issue #12) |
| 8 | not an EUDR check | costly | "screen", "A screen, not a due-diligence statement." applied; "point samples, not plot polygons" only as "100 point cells" |
| 9 | CCI v7 vs registry v6.0 | costly | version dropped; LIVE fact says v7.0 (so "v7.0, 2022 epoch" is correct at fact level) |
| 10 | which GFC2020 version | costly | "JRC GFC2020 V4" applied; LIVE cell-A fact confirms scheme v4 (URL is a mutable LATEST path) |
| 11 | CAMS is an Open-Meteo relay | costly | "CAMS forecast, Open-Meteo" applied |
| 12 | why not STAC/openEO/C2PA/PROV | costly | applied verbatim; PROV, RAG, GeoGuard absent |
| 13 | does "under 2 ms" include a COG re-read | costly | "1.2 ms offline, with the source window cached" applied |
| 14 | SAT-042 anchor and score undefined | costly | "one fixed anchor" and score formula applied |
| 15 | DOI title | costly | "(v0.1.0)" label; not re-minted (LIVE: still v0.1.0) |
| 16 | Keylong masking | costly | not applied (session README) |
| 17 | problem chart vs headline | costly | caption sentence applied; task still unnamed |
| 18 | "every satellite" | minor | "every product" applied |
| 19 | conclusion 2 necessity claim | minor | conclusion rewritten |
| 20 | DEM is a DSM; release date as valid time | minor | "(DSM)" applied; "2021 release" kept as valid time |
| 21 | MODIS LST | minor | applied |
| 22 | single-pixel S1 | minor | "γ⁰ … 1 px" applied |
| 23 | 780 vs 757 | minor | applied |
| 24 | section order, orphan clock panel | minor | order fixed; Bengaluru moved into §2 |
| 25 | FIRMS absence | minor | applied |
| 26 | CTA too small | minor | QR caption now 6.2 mm; footer still 4.2 mm |
| 27 | two claims-map addresses, `should_do` | minor | applied (repro/v12 in both places) |
| 28 | Keylong label overprints data | minor | label moved (crop c07 shows it clear) |

The review's "three objections most likely to lose the room" (§9): SAT-042 without a satellite plus the ungated path; the self-contradicting first two lines; the strike in a Φ-lab room.
v12.1 answered all three in part; the title still carries traces (1), and the new punchline carries the arbiter problem (2).

### 5.3 New findings on v12.1 that the review could not see (this session)

1. "the source bytes / guaranteed" (`:223`) and "Name each satellite observation by the hash of its bytes" (`:132`): record bytes conflated with source bytes. MEASURED.
2. Per-fact signature formula vs code (attest.rs:34, :93-133; LIVE fact has no signature field). SPEC + LIVE.
3. "canonical" CBOR vs RFC 8949 §4.2.1 (defect 33). UNVERIFIED beyond the defect text.
4. "SAT-042 exercises every refusal" and "Every vector emem signed still resolves": unsourced overclaims. MEASURED (claims map has no row).
5. "With all nine checks": six checks, three representations. MEASURED.
6. Drift score and digest binding vs defect 36 ("not wired into ingest"; binds by value hash only). SPEC.
7. M15 before/after is provider-confounded (pre E84 192 / PC 8; post PC 54 in 2 days). MEASURED.
8. The pixel bug hit every COG-backed band, including the EUDR layers the board uses (CHANGELOG.md:68). SPEC.
9. Title variants (five). LIVE + MEASURED.
10. Footer commit 04b40c5 not resolvable in the local clone; the brief's source is 18adb67. MEASURED.
11. `AGENTS.md` (line 3, 12) still describes the struck title and "The current board is v12"; `poster/README.md` still describes v11. MEASURED.
12. Build gates have gaps (QR payload not compared, claims map not run, figure text not prose-checked). MEASURED.

---

## 6. Strongest assets to keep

### 6.1 On the v12.1 board

1. **R1 mutation matrix** (`r1_mutation.svg`, `mutation_matrix.json`): deterministic, offline, reproducible in 0.0528 s; each refusal names its check; leave-one-out shows which checks are necessary. Keep; enlarge; add the decision row and the RAG arm when the agent-level run exists.
2. **M15, "the right record, the wrong pixel"** (`m15.svg`): real DNs, recomputed NDVI, a decision that flips (0.4709 vs 0.3016 around 0.4705), a production rate with a Wilson interval, and a clean before/after. It is the single strongest scientific finding; add error magnitude (median 0.027, p90 0.113) and the all-COG-bands scope.
3. **The independent 780-fact verification** (`eo_evidence_verification.md`): 20 checks per fact with a verifier that imports no emem code (blake3, cbor2, pynacl), RFC 6962 inclusion and consistency proofs, bit-flip negative control. It gives the ladder its numbers: L0/L1 780/780, L2 266/780, L3 0/780.
4. **Bengaluru as-of** (`contra_bengaluru.json`): real, committed, asserted in the build; reframe as "what the agent knew".
5. **Keylong series** (141 facts, 3 satellites, peaks, the hero record `oj5cecci…` LIVE-resolvable; fact body carries two COG URLs, DNs [3502, 1900], offset −1000, SCL 4, cloud 10.84, reader stamp).
6. **Rondônia auditor card**: six signed facts for one flagged cell with cid prefixes; the right shape for "inspect the record".
7. **Guarantees table and the "A signature does not make a value true" objection**: the seed of the ladder and boundary.
8. **Build discipline**: 1:1 figures with a 15 pt floor and overlap/clipping asserts; figure numbers dumped to JSON; claims map generated from files.
9. **SAT-042 honesty lines**: "scripted pass in emem's test harness, not a spacecraft"; "No spacecraft is enrolled."

### 6.2 In the repository, not on v12.1, and directly on the brief

1. **Cross-runtime resolution of the same token** (`research/repro/data/v8/crossruntime_table.json`, generated 2026-09-30T08:40:43Z, 3 reps, server commit 213e273): the Keylong token resolved and re-hashed to the same value 0.4708994708994709 through `1_raw_rest` (223.5 ms), `2_raw_mcp_jsonrpc` (223.7), `3_a2a_message_send` (214.0), `4_python_sdk_ememdev` (207.7), `5_typescript_sdk_@vortxai/emem` (79.3), `6a_llamaindex_FunctionTool` (334.3), `6b_langchain_mcp_adapters` (1201.1), `6c_official_mcp_python_sdk` (58.3), `6d_official_mcp_typescript_sdk` (57.6), `7_independent_blake3_cbor2` (235.6), `A->B_isolated_processes` (772.8). MEASURED (file). Answers MASTER §16 "same observation … two different agent environments" at the protocol/SDK level and issue #43; host-level (ChatGPT, Claude, Dify) is not covered by this file.
2. **Token cost** (`research/repro/data/v8/token_counts.json`): fact token 84 chars / 46 cl100k tokens vs bare value 18 chars / 8 tokens (3-decimal value 3 tokens); 5-fact bundle 38 chars / 22 tokens; fact JSON GET 562 tokens; REST recall JSON 3,064; MCP recall content 1,587. emem's own statistics section (18adb67): "50.6 tokens per citation against 5.4 per value: 9.5x (cl100k_base)", bundle "flat at 38 characters and one round trip at every N up to 256", and "A system that reads one value per question should not use addressed memory". MEASURED/SPEC. This is the cost panel MASTER §18 asks for.
3. **The pre-registered two-LLM handoff** (`research/repro/data/v8/results.json`, prereg `prereg.md`): agent A claude-sonnet-5-5 n = 10, token equals hero 10/10, mean wall 13.28 s, mean cost $0.105, 46 cl100k tokens for the token vs 64.9 for the prose. Sealed v11 headline: "the token protects only an agent that refuses a mismatch". Agent-level evidence absent from v12.1 (issue #16).
4. **Resolved emem errors that are multi-agent failure classes** (the user's "catastrophe" point). Only M15 is on v12.1 (M17 appears as out of scope). Off-board, with sources:
   - Date substitution: `emem_band_raster` asked for 23 Sep returned the byte-identical 25 Sep raster with no warning; 9 of 10 agents never got 23 Sep values; 5 of the 6 "no material change" verdicts were self-declared placeholders; 3 of 10 agents then claimed no 23 Sep acquisition existed (`research/repro/data/v9/rawband/results.md`; defect 27, cause defect 34). MEASURED (file). The signed tslot in the token exposes the substitution; prose does not.
   - EUDR tile edge: plots across a tile line "signed the far side's out-of-image pixels as 0: a forest-2020 of 0 or a loss year of 0, a pass" (CHANGELOG.md:53). SPEC (fixed).
   - Superseded releases (Hansen v1.12, GFC2020 V3) stop answering "latest"; "Nothing signed is rewritten." (CHANGELOG.md:54). SPEC.
   - Half-pixel raster headers and a one-pixel SCL mask offset at cloud edges (CHANGELOG.md:59); WorldPop 1.77x low, SoilGrids unit labels (:61); southern UTM reads off-image (:62). SPEC.
   - Place resolution 597 m off the given coordinates (defect 37); recall default returning the 2022 scene (defect 15); re-minting a raster yields a new cid for identical pixels (defect 18); read tools that sign and store records (defect 29). Fix status UNVERIFIED.
   - The amber "seen in production" ids in R1 (M2, M4, M5, M15, M17) already tie five mutation classes to real incidents; v12.1 explains only M15.
5. **Sealed v11 board** (`poster/archive/v11-sealed/poster.html`): uses the programme title exactly; panels "1.17 MB read from a 2.02 GB scene; the agent receives 84 characters", "From one token to the source pixel, without emem software", "Asked for 23 Sep raw bands, emem's raster tool served the 25 Sep scene", "What a signature does not show". Candidate material for cost, source re-read and the catastrophe framing.

---

## 7. Open points for the v13 team (no decisions taken here)

1. Title: print the programme title exactly, or an extension of it, and align `<title>`, AGENTS.md, Zenodo.
2. Which emem commit the board cites (04b40c5 on board and trace files; 18adb67 in the brief; remote main 8e9b401).
3. Whether `POST /v1/attest_cbor` is gated at the cited commit (hostile objection 4); whether defect 36 is fixed.
4. Whether the fact-signature formula is corrected on the board (batch Merkle root under an attestation) or emem's docs are corrected.
5. Whether embeddings stay on the face (programme title) with a demonstration, or move behind a QR (MASTER §19).
6. Workshop dates: 19–21 Oct (schedule, /dates/) vs 19–20 Oct (home page).
7. Whether the M15 before/after should state the provider change (E84 → PC) or be re-sampled within one provider.
