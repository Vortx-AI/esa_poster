# 06 · The visual system for the v13 A0: grid, type, colour, glyphs, every figure, page composition

Written 2026-10-01 (UTC) for the final A0 (841 × 1189 mm portrait). Topic: `visual`. Read-only research: nothing on the
board, in `poster/`, in emem or on emem.dev was changed. The only live calls were two read-only `GET /v1/facts/<cid>`.

Labels on every item:

- **MEASURED**: computed in this session from committed files, images or fonts (command, file or script named).
- **LIVE**: fetched from a live service this session (URL, time).
- **SPEC**: what emem's code or docs say, or what an external standard or guide says (URL, retrieved 2026-10-01).
- **INFERRED**: my design reasoning or arithmetic from the above.
- **UNVERIFIED**: stated by a committed file or another report, not re-checked here.

Inputs read in full: `research/SHARED_STATE_EMEM_A0_MASTER.md` (558 lines), the 39 open issues of Vortx-AI/esa_poster
(GitHub MCP `list_issues`, 39 returned, #5 to #7 and #11 to #46), `research/v13/01_v12_state.md`, `02_experiment_design.md`,
`03_ecosystem_manifest.md`, `04_prior_art_and_field.md` (sibling reports; their MEASURED/LIVE items are reused with their
labels), `poster/make_figures_v12.py`, `poster/src/poster.v12.html` (CSS), `poster/make_hero_v11.py`, `poster/make_figures.py`
(F1), the v12 preview and the sealed v11 preview. Data opened: `research/repro/data/keylong_B0{2,3,4,8}.bin`,
`research/repro/data/v8/{pixel_windows,pixel_check,prevalence_summary,token_counts,crossruntime_table,cog_pixel_bytes,scene_sizes,results}.json`,
`research/repro/data/v9/rawband/results.md`, `research/repro/data/v11/cell_products.json`,
`research/repro/data/contra_bengaluru.json`, `research/repro/v12/data/{case_keylong_ndvi,case_rondonia_eudr,v1_bands_2026-09-30}.json`,
`research/repro/v12/data/scene_*.png/.headers`, `research/repro/v11/out/{mutation_matrix.json,summary.md}`. emem source at
`origin/main` 18adb67 (`crates/emem-fact/src/attest.rs`, `CHANGELOG.md`).

Artifacts made for this report (scratchpad, **ephemeral**: copy into the repo before the session ends; see section 11):

| file (under `/tmp/claude-0/-home-user-esa-poster/0db6b3ad-8059-51a6-bd74-2d7a97faf986/scratchpad/v13/`) | what it is |
|---|---|
| `mock_layout.png` (+ `mock_layout.py`) | **the page-composition mock**, drawn 1:1 in mm with real point sizes and miniatures built from the committed data |
| `mock_layout_3m.png` | the same mock reduced to the acuity limit at 3 m (1 arcmin = 0.873 mm per pixel) and blurred: what survives at 3 m |
| `proto_m15.png` (+ `proto_m15.py`) | buildable prototype of "the right record, the wrong pixel" from the **real signed Sentinel-2 grids at native 10 m** |
| `palette_check.py`, `palette_final.py`, `palette_check.txt` | CVD simulation (Machado 2009, severity 100) and FOGRA39 round trip of every colour token |
| `plex/ttf/IBMPlex{Sans,Mono}-*.ttf` | the **complete** IBM Plex fonts (npm `@ibm/plex-sans` 1.1.0, `@ibm/plex-mono` 2.5.0, OFL-1.1), converted from WOFF |
| `icc/Adobe ICC Profiles (end-user)/CMYK/CoatedFOGRA39.icc` | the FOGRA39 profile used for the gamut check (Adobe end-user profile bundle) |

---

## 0. Findings in one screen

1. **The board can follow one real record from the satellite pixel to the decision, at native resolution, with no
   new data.** The committed signed grids `keylong_B0{2,3,4,8}.bin` (EMEMGRD1, 443 × 453 px, 10 m, EPSG:32643, S2A L2A
   25 Sep 2026) contain the hero record's 5 × 5 window exactly: rows 210 to 214, cols 223 to 227 equal the committed COG
   DNs minus the BOA offset 1000, for B04 and B08, every pixel (MEASURED, `np.array_equal`). The header's first-pixel
   centre (688735 E, 3607705 N) puts the pixel corner on the tile's 10 m lattice, so grid pixel (212, 225) is COG pixel
   (row 9443, col 9098), the pixel the record names, and (213, 225) is the pixel 10 m south that the old reader took
   (MEASURED + `CHANGELOG.md:59, :68` SPEC). True colour from B04/B03/B02 of the same grids gives a real, beautiful
   4.4 km scene and a real 50 m window (`proto_m15.png`). The emem scene chip for the same cell also sits on the native
   grid (R-channel window vs B04 DN: Pearson r = 0.993 at zero offset, MEASURED).
2. **The v12 accent blue does not survive offset print.** `#1F4FD8` round-trips through FOGRA39 with ΔE00 7.49 (prints
   as about `#3856A1`); IBM Blue 60 `#0F62FE` 9.59. The proposed EMEM blue `#0F5FA8` 0.61 (MEASURED, littleCMS 2.19,
   Adobe CoatedFOGRA39, relative colorimetric).
3. **A purple "agent A" would collide with the EMEM blue for colour-blind readers**: ΔE00 2.2 under protanopia and 5.5
   under deuteranopia (MEASURED). Colour therefore encodes evidence state only; agents are neutral glyphs (umber
   `#7A5230` and slate `#3D5566`, distinguished by letter and shape). The four state colours (EMEM blue, vermillion
   `#D2481E`, amber `#E8A317`, warm grey `#9C9A92`) keep ΔE00 ≥ 17.0 for every pair under normal, protan, deutan and
   tritan simulation (MEASURED), and blue vs vermillion passes the dataviz validator (CVD ΔE 21.3, normal 32.2, contrast ≥ 3:1).
4. **The board's fonts are Latin subsets that lack → ≤ ≥ ≠ Δ σ Φ γ ≈ ⁰** (270 glyphs; MEASURED with fontTools on
   `poster/fonts/ttf/*`). v12 prints "Φ-lab", arrows and "≤" in HTML, so the browser falls back to another face. The
   complete IBM Plex Sans 3.005 (895 code points) has all of them; it lacks ● ■ ▲ ○ (MEASURED), so status glyphs must be
   drawn as shapes, never typed.
5. **Nothing on v12 is fluent at 3 m** (01 §2.5). Using Legge & Bigelow's 0.2° critical print size and Plex's measured
   x-height (0.516 to 0.525 em), fluent reading needs ≥ 57.5 pt at 3 m, ≥ 19.2 pt at 1 m, ≥ 5.8 pt at 30 cm. The proposed
   scale puts the hero at 100 pt (fluent to 5.3 m), the title at 56 pt (2.95 m), the principal-result numerals at 64 pt
   (3.4 m), body at 24 pt (1.25 m) and the floor at 14 pt (0.73 m) (MEASURED arithmetic, section 2.3).
6. **Composition**: full-bleed header with the real Keylong scene; a full-width handoff spine (panel 1); three columns
   (problem / invention + result / evidence and boundary); a bottom band (ecosystem bridge, prior-art layers, conclusion).
   The main experiment (spine + matrix + wrong-pixel figure) takes **32.6 % of the page**, against 11.0 % on v12 (R1 7.96 % +
   M15 3.04 %); SAT-042, the schema bar and the formulas leave the face (INFERRED design, MEASURED areas).
7. **The "catastrophe ladder" is buildable from sourced failures**: seven failures found in emem, ordered by the depth of
   check that catches them (L1 binding → L2 recompute → L3 source re-read); five are fixed in emem's CHANGELOG and none was
   prevented by a signature. It is the poster's answer to "why is this needed" (section 6.12).
8. **The mock (`mock_layout.png`) works and exposed four rules** the build must gate: 3-column panel titles ≤ 27
   characters at 34 pt; two-digit panel numbers need a 22 mm title offset; never set text on hatch; one dot per row in log
   cost charts (labels on a shared axis collide).

---

## 1. Research basis (what each source decides on this board)

| source (retrieved 2026-10-01) | what it says (SPEC) | what it decides here (INFERRED) |
|---|---|---|
| CASRAI, *Scientific poster design* — https://casrai.org/guides/scientific-poster-design (cited by MASTER §1) | title readable at 15–20 ft, "commonly 85-120pt"; headings 36–44 pt; body 24–32 pt, "anything meaningfully smaller forces readers to lean in"; "understood from about ten feet away in ten seconds"; the takeaway "should be the largest, boldest text block"; "size and weight — not color alone"; colour-blind-safe palette; "generous white space" | the hero sentence, not the title, is the largest text; body 24 pt; size/weight carry hierarchy, colour carries state |
| Morrison, #betterposter (2019) — https://www.npr.org/sections/health-shots/2019/06/11/729314248/ ; https://www.insidehighered.com/news/2019/06/24/theres-movement-better-scientific-posters-are-they-really-better ; how-to: https://med-fom-dcd14.sites.olt.ubc.ca/files/2021/07/Morrison_Method_How_To_Guide.pdf | main finding in big plain-language type; an "ammo bar" of detail for the presenter; "silent presenter" bullets | header = plain-language finding at billboard size; the 30 cm tier (record fields, stats, references) is the ammo bar |
| Legge & Bigelow 2011, *Does print size matter for reading?*, J. Vision 11(5):8 — https://jov.arvojournals.org/article.aspx?articleid=2191906 | critical print size for normal readers ≈ 0.2° x-height; fastest reading at 0.21° | the distance tiers are computed, not guessed (section 2.3) |
| Rougier, Droettboom, Bourne 2014, *Ten Simple Rules for Better Figures*, PLoS Comput Biol 10(9):e1003833 — https://pmc.ncbi.nlm.nih.gov/articles/PMC4161295/ | rules incl. "Identify Your Message", "Captions Are Not Optional", "Do Not Trust the Defaults", "Use Color Effectively" ("If you don't know the answer, just keep it black"), "Avoid 'Chartjunk'", "Message Trumps Beauty" | every figure states one finding; matplotlib defaults are replaced by tokens; ink is the default colour |
| Tufte, *The Visual Display of Quantitative Information* (1983/2001) — https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/ ; Few, *Show Me the Numbers* (2004/2012) | maximise data-ink, erase non-data ink; small multiples; table design for lookup | no frames or drop shadows; cost chart as aligned small multiples; matrix as a table-graphic with direct labels |
| Wong 2011, *Points of view: Color blindness*, Nat. Methods 8:441, doi:10.1038/nmeth.1618 — https://www.semanticscholar.org/paper/Points-of-view:-Color-blindness-Wong/522240b091edc812134b0ba259c78f8bf30f61b1 ; Okabe & Ito, *Color Universal Design* (2002, rev. 2008) — https://jfly.uni-koeln.de/color/ | the 8-colour CUD palette; "Use not only different colors but also a combination of different shapes, positions, line types and coloring patterns" | blue/vermillion pair from the CUD family; every state also coded by shape, line pattern or hatch |
| Crameri, Shephard, Heron 2020, *The misuse of colour in science communication*, Nat. Commun. 11:5444 — https://www.nature.com/articles/s41467-020-19160-7 | rainbow and red–green maps distort data and exclude CVD readers; use scientifically derived maps | no rainbow; no red/green pairs (the NDVI greens never meet a red mark without a white halo and a dash pattern) |
| Nuñez, Anderton, Renslow 2018, *cividis*, PLoS ONE 13(7):e0199239 — https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199239 | a CVD-optimised, perceptually uniform, linear-lightness map | `cividis` for any continuous non-NDVI raster (e.g. a biomass inset) |
| Machado, Oliveira, Fernandes 2009, IEEE TVCG 15(6):1291–1298 — https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html | physiologically based CVD simulation | the model used for every CVD number in section 3 (via `colorspacious` 1.1.2) |
| FOGRA39 / ISO Coated v2 — https://www.color.org/chardata/fogra.xalter ; TAC 330 % (e.g. https://grafistore.com/en/support/iso-coated-v2-versus-fogra39) ; rich black — https://en.wikipedia.org/wiki/Rich_black | the European offset reference condition; total area coverage limit 330 %; ~240 % is a safe rule for rich blacks | every token checked against FOGRA39; text in K-only; large dark fills ≤ 300 % TAC |
| QR sizing, "10:1 rule" — https://scanova.io/blog/minimum-qr-code-size/ ; https://www.uniqode.com/blog/qr-code-best-practices/how-to-perfectly-size-your-qr-codes | code width ≥ scan distance / 10; 2 cm minimum | header QR 60 mm (scan from 0.6 m); panel QRs 40 mm (0.4 m) |
| Sentinel-2 L2A PB 04.00 offset — https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-2-msi/level-2a-algorithms-products ; https://forum.step.esa.int/t/info-introduction-of-additional-radiometric-offset-in-pb04-00-products/35431 | SR = (DN + BOA_ADD_OFFSET) / 10000, offset −1000 since 25 Jan 2022 | image annotations print "reflectance = (DN − 1000) / 10 000"; the signed grids already carry the offset (MEASURED, section 5) |
| Sentinel Hub true-colour scripts — https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/l2a_optimized/ ; https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/highlight_optimized_natural_color/ | gamma or root compression of the true-colour bands for natural appearance | one stated linear stretch + one gamma, identical for all bands, printed on the figure |

---

## 2. Page, grid and type

### 2.1 Sheet, margins, grid (INFERRED design; dimensions are ISO 216 A0)

| item | value |
|---|---|
| sheet | 841 × 1189 mm portrait; bleed 3 mm on the header band only (full-bleed dark band and image) |
| side margins | 20 mm (live width 801 mm); top content inset 13 mm inside the header; bottom margin 13 mm |
| columns | 12 × 58.5 mm, gutters 9.0 mm. Zones: left = cols 1–3 (193.5 mm), centre = cols 4–9 (396.0 mm), right = cols 10–12 (193.5 mm); bottom band splits cols 1–8 (531.0 mm) and 9–12 (261.0 mm) |
| column x positions (left edge, mm) | col 1: 20.0 · col 4: 222.5 · col 7: 425.0 · col 9: 560.0 · col 10: 627.5 · col 12 right edge: 821.0 |
| vertical module | 3 mm; panel gaps 10 mm; section rule 0.8 mm ink above every panel |
| panel rhythm (issue #25) | question as title → one active-verb mechanism line → figure → caption = finding + scope |

### 2.2 Fonts (MEASURED)

- Faces: IBM Plex Sans (text, figures) and IBM Plex Mono (tokens, CIDs, commands), OFL-1.1 (`poster/fonts/OFL-IBM-Plex.txt`).
- **Replace the subsets.** `poster/fonts/ttf/ibm-plex-*-latin-*.ttf` have 270 (Sans) / 280 (Mono) glyphs and miss → ← ≤ ≥ ≠ Δ σ
  Φ γ ≈ ⁰ ✓ (fontTools `getBestCmap`). The complete IBM Plex Sans 3.005 (npm `@ibm/plex-sans` 1.1.0, 895 code points) has every
  one of them; complete Plex Mono 2.005 (`@ibm/plex-mono` 2.5.0, 1,049) lacks Greek, so Greek is set in Sans. Neither has
  ● ■ ▲ ○: draw status glyphs as SVG shapes. Metrics: unitsPerEm 1000; x-height 516 (Regular), 520 (Medium), 522 (SemiBold),
  525 (Bold); cap height 698.
- Numerals: tabular figures in tables and the matrix (`font-feature-settings: "tnum"`); U+2212 minus; "1,115" thousands commas;
  "15 / 15" with thin spaces in figures, "15 of 15" in prose.
- Figure text stays **text** in SVG (`svg.fonttype: "none"` + the same @font-face), or every string is dumped to JSON, so the
  prose and claim-status gates can read figure labels (v12 outlined them: `make_figures_v12.py:50`, 01 §1.1 gate 2 gap).

### 2.3 Type scale by viewing distance (MEASURED arithmetic: x-height = em × Plex ratio; fluent if x-height ≥ 0.2°, Legge & Bigelow)

Thresholds: x-height 10.47 mm at 3 m (Plex Regular 57.5 pt), 3.49 mm at 1 m (19.2 pt), 1.05 mm at 30 cm (5.8 pt).
Acuity limit (1 arcmin): 0.87 mm at 3 m, 0.29 mm at 1 m, so 3 m marks need strokes ≥ 1 mm.

| tier | role | face | pt | em mm | x-height mm | fluent to | width check (MEASURED with matplotlib) |
|---|---|---|---|---|---|---|---|
| 3 m | hero sentence | Sans Bold | 100 | 35.3 | 18.5 | 5.3 m | "Agents hand each other evidence" 549.5 mm / "references, not paraphrases." 476.4 mm, both < 598.5 mm (9 cols) |
| 3 m | principal-result numerals (spine outcomes, matrix totals in the spine) | Sans Bold | 64 | 22.6 | 11.9 | 3.4 m | "15 / 15" 74.9 mm |
| 3 m | title (programme title, exact) | Sans SemiBold | 56 | 19.8 | 10.3 | 2.95 m | line 1 "EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol" 582.6 mm; line 2 "for AI Agents over Foundation-Model Embeddings" 457.8 mm |
| 1 m (read at 2 m) | spine question; 6-col panel titles | Sans SemiBold | 44 / 40 | 15.5 / 14.1 | 8.1 / 7.4 | 2.3 / 2.1 m | "What survives an agent handoff?" 234.2 mm; "Which check stops which corruption" 238.4 mm |
| 1 m | boundary sub-hero (header) | Sans Medium | 32–36 | 11.3–12.7 | 5.9–6.6 | 1.7–1.9 m | "A signature fixes the bytes, not the measurement." 289.7 mm at 36 pt |
| 1 m | 3-col and 4-col panel titles | Sans SemiBold | 34 | 12.0 | 6.3 | 1.8 m | ≤ 27 characters: "Seven failures, one pattern" 148.6 mm (+ 12 mm number) < 193.5 |
| 1 m | figure values that carry the result (M15 values, matrix totals) | Sans Bold | 30 | 10.6 | 5.6 | 1.6 m | |
| 1 m | take line (measured result sentence); body | Sans SemiBold / Regular | 24 | 8.5 | 4.4 | 1.25 m | CASRAI body 24–32 pt |
| 1 m | figure labels, lane names | Sans Medium | 20 | 7.1 | 3.7 | 1.05 m | |
| 30 cm | captions, annotations, snippets | Sans Regular / Mono | 17 | 6.0 | 3.1 | 0.89 m | token in Mono 18 pt: 320.0 mm |
| 30 cm | floor: references, CIDs, footnotes, tier notes | Sans / Mono Regular | **14 (minimum anywhere)** | 4.9 | 2.5 | 0.73 m | v12 footer was 4.2 mm em = 11.9 pt: below this floor |

Leading: 0.96–1.0 hero, 1.05–1.1 titles, 1.3 body, 1.25 captions. Weights: 400 body, 500 labels, 600 titles and take lines,
700 hero, numerals and lane names. No italics for emphasis (weight only). No all-caps above 3 words except the six QR verbs and
the status words of the ladder (CHECKABLE …), set at +8 % tracking.

**Word budget** (INFERRED; v12.1 had 1,029 live words, 01 §2.4): ≤ 800 printed words outside references, figure ticks and QR
labels. Per panel: header 40 · spine 70 · paraphrase 45 · failures 110 · questions 55 · threat 50 · handed-over 55 · matrix 60 ·
wrong pixel 70 · checks 60 · time 45 · Rondônia 40 · cost 35 · ecosystem 70 · layers 45 · conclusion 35. The build counts
words per panel and fails above budget.

---

## 3. Colour

### 3.1 Semantic tokens (MEASURED: CMYK and ΔE00 from sRGB → FOGRA39 → sRGB, relative colorimetric, Adobe CoatedFOGRA39.icc,
littleCMS 2.19; contrast = WCAG ratio on white `#FFFFFF`; script `palette_check.py`)

Colour encodes **evidence state only**. Agents, systems and sections never get a hue of their own.

| token | role | hex | FOGRA39 CMYK % | ΔE00 round trip | contrast on white | usage rule |
|---|---|---|---|---|---|---|
| `emem` | the reference; a refusal by a check; "verified at layer Lx" | `#0F5FA8` | 95 63 2 0 | 0.61 | 6.52 | fills, 1.4 mm outlines, text ≥ 17 pt |
| `emem-tint` | EMEM lane, panel fills | `#DCE8F5` | 16 6 2 0 | 0.46 | 1.24 | background only |
| `emem-light` | blue on the dark header | `#7FB3E6` | 54 20 0 0 | 0.90 | 6.05 on `navy` | header sub-hero only |
| `harm` | B acts on corrupted evidence; the adversary; the wrong pixel | `#D2481E` | 11 85 100 3 | 1.87 | 4.48 | fills; text ≥ 24 pt (use `harm-text` below that) |
| `harm-text` | harm in small text | `#B5401A` | 20 87 100 13 | 3.13 | 5.66 | text 14–20 pt |
| `harm-tint` | adversary zone, "passes a wrong value" chips | `#FADDD2` | 1 18 17 0 | 0.39 | 1.29 | background only |
| `incident` | seen in production (real failure) | `#E8A317` | 7 40 100 1 | 0.24 | 2.17 | rings and 3 mm bars only, always with the word or id; never text |
| `incident-text` | incident labels | `#8A5A00` | 31 58 100 36 | 4.70 | 5.93 | text |
| `oos` | out of scope / not established | `#9C9A92` + 45° hatch | 39 32 38 13 | 1.10 | 2.82 | hatch lines on `#F1F0EC`; never text on hatch |
| `agentA` | sender glyph outline and letter | `#7A5230` | 35 62 87 44 | 0.37 | 6.84 | glyph only |
| `agentB` | receiver glyph outline and letter | `#3D5566` | 80 56 42 33 | 0.57 | 7.79 | glyph only |
| `ink` | text (print as K-only 0 0 0 100) | `#222428` | 88 76 58 85 (as RGB) | 0.78 | 15.54 | all text; K100 previews as `#2B2B2A` in FOGRA39 |
| `ink2` / `muted` / `rule` | secondary text / labels / hairlines | `#4A4D55` / `#7A7D85` / `#D5D6DA` | | 0.58 / 0.55 / 1.02 | 8.45 / 4.12 / 1.45 | `muted` only ≥ 17 pt |
| `navy` | header band | `#203045` | 100 83 46 55 (TAC 284 %) | 1.69 | 13.37 (white on it) | the one dark area; v12's `#0E1A2B` is out of gamut (ΔE00 8.33) |
| `paper` | page | `#FFFFFF` | 0 0 0 0 | 0 | | v12's `#FBFBF8` prints as a 1–2 % tint over 1 m²; use paper white |

Verification-depth ramp (ordinal, one hue, deeper toward the source = darker), used for check chips, the ladder and the
failure stair: L0 `#8FB5E0` · L1 `#5B8FCB` · L2 `#0F5FA8` · L3 `#0B4A86`. The dataviz validator in `--ordinal` mode passes
(monotone lightness, adjacent ΔL ≥ 0.06, light end 2.13:1, hue spread 1°); a first try with `#A9C7E8` failed the light-end
contrast (1.75:1). FOGRA39 ΔE00 0.47 / 0.34 / 0.61 / 1.66 (MEASURED).

### 3.2 Colour-vision safety (MEASURED; Machado 2009, severity 100, `colorspacious`; CIEDE2000)

| pair | normal | protan | deutan | tritan | verdict |
|---|---|---|---|---|---|
| emem vs harm | 47.2 | 48.7 | 56.8 | 64.1 | safe |
| emem vs incident | 60.3 | 60.2 | 67.2 | 60.3 | safe |
| emem vs oos | 37.2 | 33.8 | 38.8 | 30.6 | safe |
| harm vs incident | 31.6 | 25.8 | **17.0** | 20.9 | worst pair of the four state colours; amber always carries a ring + word |
| harm vs oos | 30.8 | 27.9 | 23.2 | 30.3 | safe |
| rejected: emem vs purple agent `#7C4D9E` | 23.0 | **2.2** | **5.5** | 41.1 | collision → agents made neutral |
| rejected: v12 `#B3261E` (red) vs a green `#1E8A72` | 58.7 | 23.1 | 21.9 | 60.4 | red/green avoided anyway (Crameri 2020) |
| final agents: harm vs agentA | 20.2 | 8.8 | 17.1 | 18.9 | agents never touch harm fills; letter + shape carry identity |

The dataviz skill's validator (`validate_palette.js`, OKLab ΔE, Machado 2009): blue/vermillion pair "ALL CHECKS PASS"
(protan ΔE 21.3, normal 32.2). The four-colour state set fails only the chroma floor for `oos` by design (a neutral that means
"no claim") and warns on contrast for amber and grey, which the rules above relieve (labels, rings, hatch) (MEASURED).

### 3.3 Imagery colour maps (INFERRED from section 1 sources)

- True colour: R = B04, G = B03, B = B02 reflectance (= grid / 10 000; the grids already carry the −1000 offset), one linear stretch
  over all three bands at the scene's 1st–99th percentile, then γ = 1/1.35; identical for every image of the board. Printed at
  30 cm under each image: "true colour B04/B03/B02, linear 1–99 % stretch, γ 1/1.35".
- NDVI: ColorBrewer `YlGn` sequential (single-hue family, monotone lightness), fixed range −0.1 to 0.8, or the value printed in
  each pixel over true colour (prototype). Never a diverging or rainbow map for NDVI.
- Other continuous rasters (biomass, elevation): `cividis`.
- Marks on imagery: 1.4 mm coloured stroke over a 2.4 mm white halo; the wrong pixel also dashed (2.2/1.2 mm) so the pair
  differs by pattern as well as hue.

### 3.4 Print

- Ask the print shop which condition it prints to. Large-format inkjet services usually take sRGB PDF; offset or a CMYK RIP takes
  PDF/X-4 with FOGRA39 (or FOGRA51) output intent. Every token above is inside FOGRA39 to ΔE00 < 2 except `harm-text` 3.1 and
  `incident-text` 4.7 (small text; acceptable) (MEASURED).
- Text in K-only black; no rich black in text. Large dark fills ≤ 300 % TAC (navy 284 %). Soft-proof the final PDF through FOGRA39
  and compare the six state colours against this table.
- Raster images at ≥ 300 ppi at final size by integer nearest-neighbour upscaling (keeps 10 m pixels as crisp squares): the
  443 × 453 grid printed 214 mm wide is 52 ppi native → ×6 → 315 ppi. Never resample with interpolation (it invents pixels the
  record does not name).

---

## 4. Lines, marks and the shared glyph grammar (issue #26: "one consistent visual grammar")

| weight (print) | where |
|---|---|
| 0.35 mm | hairline rules, table rules, grid of matrix (minimum printed line; 1 arcmin at 1 m = 0.29 mm) |
| 0.5 mm | axes, connector lines |
| 0.8 mm | section rule above each panel (ink) |
| 0.9 mm | data lines, dot outlines |
| 1.2 mm shaft, 6 mm head | spine arrows (≥ 1 mm to survive 3 m) |
| 1.4 mm + 2.4 mm white halo | named-pixel and wrong-pixel outlines; refusal frames |

Glyphs, identical in every figure (drawn as SVG paths, sizes for the spine / inline):

| meaning | glyph | colour |
|---|---|---|
| agent A (sender) | rounded square 30 / 12 mm, 0.85 mm outline, letter **A** | `agentA` outline, white fill |
| agent B (receiver) | same shape, filled | `agentB` fill, white letter **B** |
| a paraphrase | speech-bubble outline | `ink2` |
| an EMEM reference | tag: rounded rectangle with a notch, Mono text | `emem` fill, white text |
| a corruption | 8 mm diamond with "M" | `harm` |
| the adversary's reach | zone fill | `harm-tint`, 0.55 mm `harm` border |
| a check that passes | rounded chip, check name | depth-ramp tint, ink text |
| a check that refuses | rounded chip, check name or letter D–I | `emem`, white text |
| acted on corrupted evidence | filled square | `harm` |
| unaffected (value still genuine) | filled square | `#EEF3FA` |
| not applicable | light square + en dash | `#F2F2F0` |
| out of scope / not established | 45° hatch, 1.6 mm pitch | `oos` on `#F1F0EC` |
| seen in production | 0.7 mm ring around the id, or 3 mm left bar | `incident` |
| status LIVE / PROTOCOL / REGISTRY / EXAMPLE (ecosystem) | filled circle / open circle / open square / open triangle, 4 mm, drawn | `ink` |

---

## 5. Real EO imagery: what is available, verified, and how to use it

| asset | what it is | verification | use |
|---|---|---|---|
| `research/repro/data/keylong_B0{2,3,4,8}.bin` | EMEMGRD1 float32 grids, 443 × 453 px, EPSG:32643, first-pixel centre 688735 E / 3607705 N, 10 m; S2A L2A 25 Sep 2026; values = DN − 1000 | B04 and B08 rows 210–214 × cols 223–227 equal `pixel_windows.json` (oj5cecci) − 1000 exactly (MEASURED); pixel corner 688730 = 600000 + 8873 × 10 sits on the tile lattice, consistent with `CHANGELOG.md:59` "headers name the first pixel's centre" (SPEC) | header scene, spine pixel, wrong-pixel figure (a) and (b) |
| `research/repro/data/v8/pixel_windows.json` | 5 × 5 B04/B08 DNs for oj5cecci (25 Sep), kxjvfwpa (23 Sep, pre-fix) and jwkqm6eh (17 Jul) + NDVI | committed; matches the grids (above) | NDVI per pixel; the real pre-fix record |
| `research/repro/data/v8/pixel_check.json` | floor vs round pixel for both records | 25 Sep: floor (9443, 9098) 3502/1900 → 0.4709; round (9444, 9098) 2720/1923 → 0.3016. 23 Sep: floor 3605/1901 → 0.4860; round 2993/1972 → 0.3444 (MEASURED, file) | M15 values |
| `research/repro/v12/data/scene_defi.zb572.xoso.zb1ec.png` | emem-served chip, 256 × 256 px, bbox 689700–692260 E, 3604310–3606870 N, S2A 25 Sep (headers) | R channel at rows/cols 126–130 vs B04 DN: r = 0.993 at zero offset (MEASURED) → native grid; stretch is emem's (R 1217–2827), not stated | spare; prefer the signed grids (known processing) |
| `poster/img/keylong-s2a-20260925.jpg`, `poster/fig/keylong_truecolor.png` | 1772 × 1812 JPEG / 886 × 906 PNG, resampled (LANCZOS) from the same grids (`make_figures.py:35`) | interpolated: pixels are not 10 m squares | do not use where pixels are claimed; render fresh from the grids |
| `case_keylong_ndvi.json` (155 rows, 141 in 2025–26) + `data/v11/cell_products.json` (13 products, incl. the 30 Sep record `3yyaxn5d…` 0.4237) | the cell's NDVI history and its products | committed (LIVE 30 Sep per their own fields) | time panel, one-address inset |
| `case_rondonia_eudr.json` | 10 × 10 point lattice, 6 bands, categories 43 / 33 / 20 / 3 / 1 | committed | Rondônia panel |
| Rondônia imagery | **none committed** | | optional: fetch the S2 L2A scene named by cell A's NDVI fact (`ndvi_scene` field) from Planetary Computer (public STAC + COG range reads), never from an emem read tool that signs (defect 29) |

Every image carries, at 30 cm under it: place, cell id, sensor and level, date, band(s), processing line, and one sentence of why
it is there (issue #31).

---

## 6. Figure specifications

Each spec: question it answers → slot and size → data (files) → encoding → annotations → **caption-as-claim** (issue #36:
finding + scope) → tier → asserts the figure script must make. Numbers in captions are from the files named, as of their dates;
the build must regenerate them from data, never type them. Where the agent-level experiment R5 (report 02) is not yet run,
the R1 numbers (deterministic verifier) are used and the figure says so.

### 6.1 Hero handoff spine (panel 1; issue #26; MASTER §6) — 801 × 190 mm, full width under the header

- Question: "What survives an agent handoff?" (44 pt). Mechanism line (24 pt): "Agent B resolves the reference, re-hashes the
  record and re-reads the source."
- Data: `research/repro/v11/out/mutation_matrix.json` `summary.{A,B,C,I}.false_accepts / applicable` → 15/15, 15/15, 13/16, 0/16
  (MEASURED); RAG lane from R5 `results.json` when it exists (report 02 §19 templates), else the lane is dropped.
- Encoding, left to right (x in mm inside the figure): **source + Agent A** 0–104 (the real 5 × 5 true-colour window, 50 mm,
  named pixel in `emem`; agent A glyph; "Agent A reads NDVI 0.4709 and cites it" 24 pt) → **handoff** 112–317: five lanes
  25.5 mm tall, 4 mm apart (prose, JSON, retrieved text (RAG), opaque id, EMEM reference), each with its lane name (22 pt Bold)
  and a real snippet in Mono 15–17 pt rendered from the same record (`"NDVI was about 0.47 on 25 Sep"`,
  `{"ndvi": 0.4709, "date": "2026-09-25"}`, a corpus passage, `obs-7d1c44`, `emem:fact:defi.zb572.xoso.zb1ec:oj5cecci…`) →
  **adversary** 317–399: one tall `harm-tint` bar across all lanes, "one of 16 corruptions" + the ten families of MASTER §9 →
  **Agent B** 407–707: per lane what B does ("reads the text"; EMEM lane: the check chain resolve · re-hash · bind · verify ·
  log · recompute · re-read as depth-ramp chips) → **outcome** right-aligned at 712: "15 / 15", "15 / 15", "R5", "13 / 16",
  "**0 / 16**" in 64 pt (harm, harm, oos, harm, emem) under the column head "acted on corrupted evidence" → **boundary**
  722–801: hatched wall, "no check reaches: the entity meant (M17) · sensor accuracy · the decision".
- Caption-as-claim (R1 version, 53 words): "One signed NDVI record handed over in five forms, then corrupted in 16 ways. A receiver
  reading prose or JSON acted on 15 of the 15 corruptions those forms can carry; one that resolved the EMEM reference and ran
  every check acted on none of 16. Deterministic verifier, no model; one record, one band."
- After R5: replace the outcome numerals by the agents' false-acceptance k/n with the R1 ceiling as a small ghost square
  beside each, and add "models, n, dates" to the caption (report 02 §19).
- Tier: lane names and numerals 3 m; check chain 1 m; snippets 30 cm.
- Asserts: lane totals equal `summary` in the JSON; the RAG lane is absent unless R5 rows exist; the snippet strings are rendered
  from the record, not typed.

### 6.2 Mutation matrix, the hero quantitative figure (panel 5; issue #27; MASTER §9) — 396 × 255 mm

- Title: "Which check stops which corruption" (40 pt). Take line: "Removing any one of five checks lets a named corruption through."
- Data: `mutation_matrix.json` rows (162 = 18 mutations × 9 levels; outcomes `acted correctly`, `acted on corrupted evidence`,
  `refused`, `unaffected`, `n/a`), `meta.mutations[].first_protected_level`, `leave_one_out`, `summary[*].decision_flips`
  (MEASURED); R5 cells when available.
- Rows grouped by MASTER §9 family, with the id in the margin (amber ring = seen in production: M2, M4, M5, M15, M17 per R1 meta):
  value (M1, M2, M8) · cell (M4, M9) · time (M10) · band (M6) · unit (M18, only if R1-v13 runs) · source (M11) · derivation
  (M12, M14) · stale / current (M5, M16; M5b, M20 with R1-v13) · signature / id (M3, M7, M13) · source pixel (M15) · then a
  hatched separator · entity, out of scope (M17). Control G0 as a thin top row ("nothing altered: accepted everywhere; 0 false
  refusals"). Row height 8.2 mm, label 15 pt.
- Columns: prose (A) · JSON (B) · RAG (R5 only) · opaque id (C) · **EMEM, full receiver check (I)**, 44 mm wide each, then a
  narrow "first check that refuses" column with the letter D–I in its depth-ramp colour, and a ring on the letter when the
  leave-one-out says that check is the **only** one (E for M4, M5, M6; F for M9–M12; G for M16; H for M14; I for M15), then a
  "flips the decision" tick column (M2, M8, M12, M13, M14, M15 at A/B).
- Cells: glyph squares of section 4. With R5: each cell becomes a horizontal bar whose filled length is the agents' FA rate (k/n
  printed in 14 pt), with the R1 verdict as a 3 mm square at the left edge.
- Bottom row: totals per column in 30 pt (15/15, 15/15, R5, 13/16, 0/16) with "B acts on corrupted evidence" at left.
- Scope line inside the figure (14 pt): "One signed Keylong NDVI record, one band, one run; deterministic verifier, no model;
  signer-error rows (M14–M16) signed with a test key; the re-read compares with the committed 25 Sep COG window and does not
  follow a forged scene id."
- Caption-as-claim (49 words): "Each corruption is stopped by a specific check: binding stops cell, time and band swaps; the signature
  stops forged contents; the log stops an unlogged version; recomputation stops the signer's arithmetic; only a source re-read
  stops the signer's wrong pixel. The entity meant (M17) passes every check."
- Asserts: every printed total equals the JSON; every "only" ring equals `leave_one_out`; RAG column absent without R5.
- The intermediate depths D–H are not columns (they live in the "first check" letters), so the figure stays at the five
  conditions of MASTER §9 while keeping R1's mechanism.

### 6.3 "The right record, the wrong pixel" with real Sentinel-2 at native resolution (panel 6; MASTER §10; issue #31) — 396 × 183 mm

Prototype built: `proto_m15.png` (`proto_m15.py`; asserts the window equality before drawing).

- (a) **Where** (118 × 121 mm): the 4.43 × 4.53 km true-colour scene from the signed grids, nearest-neighbour; white 250 m box
  around the cited cell; 1 km scale bar; label "Keylong, Lahaul · Sentinel-2A L2A · 25 Sep 2026".
- (b) **Which pixel** (112 × 112 mm, each 10 m pixel 22.4 mm): the 5 × 5 window in true colour, NDVI per pixel printed (17 pt,
  2 decimals, ink or white by luminance); named pixel (window 2,2 = COG row 9443, col 9098) `emem` solid outline; the pixel the
  old reader took (window 3,2 = row 9444) `harm` dashed outline; connectors from (a).
- (c) **What the receiver decides**: "rule under test: irrigate if NDVI ≤ 0.4705"; "NDVI 0.4709 → hold" (30 pt ink) and
  "NDVI 0.3016 → irrigate" (30 pt harm); chips hash · bind · signature · log · recompute (harm-tint: "pass the wrong value") and
  re-read (`emem`: refuses); waffle of 200 squares, 162 `harm` (MEASURED `prevalence_summary.json`: pre n 200,
  matches_round_not_floor 162, Wilson 95 % 0.75–0.86; post n 54, 0 round, 49 floor, 5 equal); "index error where the rules
  differ: median 0.027, p90 0.113, max 0.301 (n 121)" (MEASURED).
- 30 cm line, the real production instance: "Record `kxjvfwpa…` (S2C, 23 Sep 2026, signed 25 Sep before the fix) carries the DNs of
  the pixel 10 m south (0.3444; the containing pixel reads 0.4860). It still resolves and verifies." (MEASURED `pixel_check.json`;
  LIVE per report 02 §5).
- Caption-as-claim (58 words): "A valid signature can preserve a wrong measurement. The old reader rounded the pixel position instead of
  flooring it and signed the pixel 10 m south: 0.3016, irrigate, instead of 0.4709, hold. Hash, binding, signature, log and
  recompute all pass; only re-reading the named source pixel refuses it. 162 of 200 sampled pre-fix records read a neighbouring
  pixel."
- Scope (30 cm): "Pre-fix sample 192 Element84 + 8 Planetary Computer records, post-fix 54 Planetary Computer records over 2 days:
  provider and fix are confounded. The neighbour can be east, south or south-east; the bug hit every COG-backed band from the
  first commit (`CHANGELOG.md:68`)." (MEASURED + SPEC; 01 §2.2).
- Honesty note: on 25 Sep the 0.3016 is what the pre-fix reader **would** read from this scene (deterministic, R1's M15, test
  key); the real signed pre-fix record is the 23 Sep one above. Say both, in that order.
- Optional, more exact: fetch the 23 Sep S2C B02/B03 windows from Planetary Computer so panel (b) shows the exact scene of
  `kxjvfwpa`; until then label (b) "25 Sep 2026".

### 6.4 Same place, different time (panel 8; MASTER §13; issues #19, #32) — 193.5 × 140 mm

- Question: "Same place, different time". Mechanism line: "A newer record does not overwrite the one an agent cited."
- Data: `contra_bengaluru.json` (918.0 m `yqbolgeo…` signed 2026-05-28T19:54:32Z, `open_meteo_copdem90m@1`; 915.0712280273438 m
  first signed 2026-08-11T09:39:36Z, `copernicus_dem_30m_aws_pixel@1`, re-signed 7 times as 7 CIDs); as-of answers asserted in
  v12 (`make_figures_v12.py:506-510`); Keylong: `cell_products.json` (30 Sep NDVI `3yyaxn5d…` 0.4237, signed 2026-09-30T22:20:02Z)
  and the cited 25 Sep `oj5cecci…` 0.4709.
- Encoding (pictorial before numeric, issue #32): one address node at the left ("one cell, one band"); a transaction-time axis
  May → Sep; record 1 drawn as a bar from 28 May to the right edge (it never ends: it still resolves), record 2 from 11 Aug, with 7
  ticks for its 7 re-signings; four as-of query lines (1 May: nothing; 15 Jun: 918.0; 12 Aug: 915.07; 29 Sep: 915.07), the 15 Jun
  line emphasised in `harm` dashes with "what did agent A know on 15 Jun? → 918.0 m". A thin second strip: Keylong valid time,
  25 Sep (cited, 0.4709 → hold) and 30 Sep (newer, 0.4237 → irrigate): "'latest' moved on 30 Sep; the reference still names 25 Sep."
- Caption-as-claim (52 words): "One address, two signed answers. Asked what was known on 15 Jun, the memory returns the 918.0 m record an
  agent could have cited then; the 915.07 m record signed on 11 Aug does not overwrite it. Here only the signing time moves: a
  static DEM whose provider changed."
- Scope (30 cm): "as-of compares `signed_at` strings (defect 35); exact for these UTC second stamps." Distinguish from database
  versioning in one clause: "the receiver holds the address of the cited state, so the check is its own, not the database's".
- Asserts: as-of answers recomputed from the attestations equal the printed ones.

### 6.5 Verification ladder L0–L5 and the guarantee boundary (panel 7; MASTER §11; issues #17, #29) — 193.5 × 203 mm

- Title: "What the checks establish". Mechanism line: "Never 'verified' without the layer."
- Six rungs, L0 at the bottom (a ladder climbs toward the world), each 22 mm: layer · what it means · status word · this board's
  evidence · the mutations it stops:

| rung | means | status | evidence on this board | stops |
|---|---|---|---|---|
| L0 bytes | the record is the one that was signed and logged | CHECKABLE | 780 of 780 facts re-hashed, signature-checked, found in the log (01 §6.1.3, UNVERIFIED here) | M3, M7, M8–M13, M16 |
| L1 identity | cell, band, time and value match my question | CHECKABLE | binding in R1 level E | M4, M5, M6 (+ as-of for M20) |
| L2 derivation | the value follows from the signed inputs | RECOMPUTABLE (deterministic indices only) | 266 of 780 recomputed | M14 |
| L3 source | the inputs are the named pixel of the named file | PARTIAL | re-read possible for open archives; 0 of 213 Keylong source entries carry a hash (04 §0.3) | M15 |
| L4 entity | the cell is the thing the agent meant | OUT OF SCOPE | M17 accepted at every depth | — |
| L5 truth, decision | the sensor was right; the decision was right | INHERITED (product validation) / OUT OF SCOPE | — | — |

- Two-sided encoding (issue #29): L0–L2 filled with the depth ramp ("the receiver can check"); L3 half ramp, half hatch; L4–L5
  hatched, with the text on a white plate at the left (the mock showed text on hatch is illegible).
- Caption-as-claim (44 words): "For the 780 facts behind this board, bytes, signature and log inclusion checked 780 of 780 and recomputation
  266 of 780. No source file carries a hash, so source identity rests on a re-read. A valid reference never establishes the entity
  meant, the sensor's accuracy or the decision."

### 6.6 Evidence object, exploded (panel 4; MASTER §5, §15; issues #12, #28) — 396 × 158 mm

- Title: "What is handed over". Mechanism line: "The receiver gets 84 characters; everything else it can fetch and check."
- Data (LIVE this session, `GET https://emem.dev/v1/facts/oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa`, 2026-10-01T00:00:37Z,
  JSON 1,273 B, CBOR 1,115 B; BLAKE3 of the CBOR re-hashed here to `oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa`): 12 keys
  `kind, cell, band, tslot, value, confidence, sources, derivation, privacy_class, schema_cid, signer, signed_at`; `sources[0].id` = the
  B08 and B04 COG URLs on `sentinel2l2a01.blob.core.windows.net`, `captured_at` 2026-09-25T05:42:51.024Z; `derivation.fn_key`
  `sentinel2_l2a_indices_ndvi@1` with 13 args incl. lat/lng, scene id `S2A_MSIL2A_20260925T054251_R005_T43SFS_20260925T090015`, EPSG
  32643, a formula description, DNs [3502, 1900], cloud 10.840102, the PC STAC URL and offset −1000 (the meaning of args 40.0, 30, 4, 1
  is not stated in the record; UNVERIFIED); `signed_at` 2026-09-28T09:06:56Z. **No signature
  field in the record**: the attester signs a batch root over fact CIDs (`attest.rs:34`, `build_and_sign_v1` `:93-133`; SPEC).
  COG sizes B04 277,897,303 B, B08 281,898,500 B (MEASURED `cog_pixel_bytes.json`).
- Encoding, four boxes left to right with 2.4 mm arrows:
  1. **source files** (dashed outline = named by URL, not hashed): two COG thumbnails (the real B08 grid in grey), "B04 + B08 COGs,
     277.9 + 281.9 MB, Planetary Computer; pixel row 9443, col 9098; DN 1900, 3502; no checksum published" →
     arrow "read the containing pixel; NDVI = (3502 − 1900) / (3502 + 1900 − 2000)".
  2. **record** (solid `emem` outline = bound by the address): the 12 fields as a two-column list with the actual values, the
     upstream URL fields tagged "named", `value` tagged "recomputable", 1,115 B →
     arrow "BLAKE3".
  3. **address** (`emem` fill): `oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` (Mono 17 pt, 52 characters) "changes if any bit
     of the record changes" →
     arrow "leaf of a batch root".
  4. **attestation + log**: "Ed25519 over the batch root, key `777er3yi…` pinned in DNS, did.json, jwks.json; logged in an append-only
     Merkle log (RFC 6962-style, BLAKE3)".
  Under all four, full width, the token in Mono 18 pt: `emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa`
  (320 mm) with "handed over: 84 characters, 46 tokens".
- Inset (30 cm, 120 × 40 mm), **one address, native supports** (issue #20): squares centred on the 9.55 m cell on a log scale,
  each labelled with its product's native support: S2 B04/B08/NDVI 10 m · S2 SCL 20 m · S1 RTC VV 10 m · Copernicus DEM 30 m · JRC GSW
  30 m · DMSP-OLS 30 arc-seconds (~1 km) · Prithvi-EO-2.0 receptive field 6.72 km · GeoTessera 10 m (13 products at this cell,
  `cell_products.json`; supports from the band ontology text or product docs, SPEC; met.no forecast grid UNVERIFIED, omit if not
  sourced). Line: "The address is a common key, not a co-registration."
- Caption-as-claim (45 words): "The address names the record, not the satellite file. It is BLAKE3 of the 1,115-byte record; the record names
  the two source files and the pixel read; the attester signs a batch root over such addresses. The file link is named, not hashed."
- QR (40 mm): **INSPECT THE RECORD** → `https://emem.dev/v1/facts/oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` (a GET; mobile
  test owed).

### 6.7 Threat model (left column, after the questions; MASTER §12) — 193.5 × 106 mm

- Title: "Threat model". Encoding: a horizontal channel A → relay → B. The relay box (`harm-tint`) lists "can rewrite every byte it
  carries: value, cell, date, source, record, reference; can replay stale records and traces". Two anchors that B holds, drawn as
  pins outside the relay's reach: "pinned signing key (DNS TXT, did.json, jwks.json)" and "public source archive (COG)". Under the
  channel: "cannot sign under the pinned key; cannot find a second record with the same address". Three trust stripes across the
  bottom, left to right: **cryptographic trust** (exact record signed: checkable) · **source trust** (who signed, which file:
  partial) · **measurement trust** (sensor, product: inherited), coloured with the depth ramp → hatch. Out of scope list (14 pt): a
  compromised key; a wrong sensor or product; the entity meant; the decision; an adversary that also controls the archive mirror.
- Data: report 02 §4 (T1 relay, T2 signer errs, real signer error) (SPEC for the experiment design).
- Caption-as-claim (39 words): "The relay can rewrite anything it carries but cannot sign under the pinned key or forge an address. A
  trusted signer that errs is caught only by recompute and re-read. A compromised key and a wrong sensor are outside this model."

### 6.8 Prior-art layers (bottom band, right; MASTER §14; issues #15, #30) — 261 × 96 mm

- Built from report 04 §1.2 (its spec is adopted unchanged; every label sourced there). Seven 8 mm lanes, top to bottom JUDGE
  (GeoGuard) · CARRY (MCP · A2A) · RETRIEVE (RAG) · SIGN FILES (C2PA · CDSE Traceability) · RECORD LINEAGE (W3C PROV) · RUN (openEO) ·
  FIND (STAC), each "verb · system · unit it identifies" (15 pt). EMEM is not a lane: a 1.8 mm `emem` thread at the right that
  touches FIND (names the STAC asset), RUN (names the recipe), CARRY (rides as a handle) and JUDGE (supplies re-checkable
  evidence), labelled "EMEM: is this the observation the sender cited?". No ticks or crosses against other systems.
- Title: "Seven layers, one question each" (04 §8). Caption-as-claim (04 §1.2, 40 words): "Adjacent systems find files, run workflows,
  record lineage, sign files, retrieve context, carry calls and judge claims. EMEM names the one observation an agent cited and lets
  the next agent re-check it; it relies on those layers and replaces none." Footnote (14 pt): "Same pattern in software supply
  chains: Sigstore/in-toto, RFC 6962/9162, SCITT (RFC 9943). Closest agent-memory work: ARC (arXiv 2607.25066)."
- Optional 30 cm companion (if space): "Same granule, three archives, three files" (04 §3: CDSE JP2 1,792,843 B with SHA3-256; Earth Search
  COG 3,790,230 B with SHA2-256; Planetary Computer COG 4,711,741 B with no checksum; LIVE per 04). It is the visual answer to "why not
  hash the file?" and fits as three bars of file size with a hash/no-hash glyph.

### 6.9 Ecosystem bridge (bottom band, left; MASTER §16, §17; issues #40–#46) — 531 × 158 mm

- Title: "One evidence protocol, multiple agent runtimes" (the caption the brief asks for, used as the title).
- Encoding: (1) the path as four nodes with 2.4 mm arrows: **signed observation** (`emem` tag, `emem:fact:…`) → **MCP · A2A**
  (transport) → **agent host / client** → **next agent or application** ("resolves, re-checks"). (2) Under it, four groups, names in
  poster type (brand rules forbid altered marks for most owners; 03 §6), each with its drawn status glyph: LIVE CLIENTS · PROTOCOL /
  DISCOVERY · SDK / API · FRAMEWORKS (examples), populated **only** from `research/v13/ecosystem_manifest.json` rows whose `print`
  is allowed (03 §7: e.g. Claude Code and the Claude Code plugin, Gemini CLI, Dify Marketplace LIVE; MCP, A2A, Claude.ai custom
  connector, VS Code, Cursor PROTOCOL; Official MCP Registry, GitHub MCP Registry, Glama REGISTRY; GitHub, `pip install ememdev`,
  `npm i @vortxai/emem`, Docker LIVE; LlamaIndex, AutoGen, Agno, CrewAI, Mastra EXAMPLE; LangChain only after its example is fixed;
  ChatGPT only after the logged-in check). At most two marks: GitHub (black) and Dify (mono) (03 §6). (3) Right, the
  **same-token dot plot** (165 × 90 mm): 10 timed client paths as rows, median latency on a log axis 30 ms – 2 s (official MCP Python
  56.3, official MCP TS 58.3, TS SDK 58.6, Python SDK 207.7, raw REST 223.5, raw MCP 223.7, A2A 226.3, independent blake3+cbor2 235.6,
  LlamaIndex 300.8, LangChain MCP adapters 1,176.8 ms) plus the A→B isolated-process row; every dot the same `emem` colour because
  every path returned the same CID and value (`crossruntime_table.json`, 2026-09-30T08:40:43Z, 3 reps, server 213e273; MEASURED).
- Caption-as-claim (44 words): "The same Keylong reference resolved to one CID and one value, 0.4708994708994709, through 11 client paths:
  REST, MCP, A2A, two SDKs, four framework or official MCP clients, an independent decoder and an A-to-B process handoff (30 Sep
  2026). Directory listings are not integrations."
- 30 cm footnote (03 §7): "Checked 2026-10-01: MCP/A2A endpoints, registries and packages by API; Claude Code and Gemini CLI connected;
  framework clients listed 18 tools. ChatGPT, claude.ai, Dify, VS Code and Cursor not run by us."
- QR (40 mm): **DISCOVER INTEGRATIONS** → `https://emem.dev/#use` (03 §7).
- Asserts: the build refuses a printed surface without a manifest row (03 §8); latency values from the JSON.

### 6.10 One address, native supports (issue #20)

Specified as the inset of 6.6 (not a panel of its own: the board follows one record, so the one-address claim belongs where the
`cell` field is explained). v12's Berlin stack leaves the face (section 9).

### 6.11 Cost and overhead (panel 10; MASTER §18) — 193.5 × 122 mm

- Title: "What it costs". Mechanism line: "The receiver pays in tokens, bytes and milliseconds."
- Encoding: three aligned log-scale small multiples (Tufte), one dot per row (the mock showed that labels on a shared row collide),
  label at left, value at the dot:
  - context tokens (cl100k): bare value 8 · reference 46 · A's prose, mean of 10 runs 64.9 · record as JSON 562 · 18-tool MCP list
    18,659 (`token_counts.json`, MEASURED) — report 02 measured 20,838 LIVE on 30 Sep: print the value re-measured at build time with
    its date;
  - bytes moved: reference 84 · record (CBOR) 1,115 · proof bundle 4,906 · cold source re-read 1,165,033 (= 0.058 % of the scene) ·
    whole scene ≈ 2.02 GB (`cog_pixel_bytes.json`, `token_counts.json`, MEASURED);
  - milliseconds: offline full check 1.187 (R1 meta, cached window) · resolve over the network 223.6 (median of 10 timed paths) ·
    range 56.3–1,176.8 (`crossruntime_table.json`, MEASURED).
- Caption-as-claim (42 words): "A reference costs 46 tokens where the bare value costs 8, and the 18-tool MCP catalogue costs 18,659 tokens before
  any call. A cold source re-read moves 1.17 MB of a 2.02 GB scene; re-checking a cached record takes 1.2 ms."
- Scope (30 cm): "emem's own guidance: a system that reads one value per question should not use addressed memory" (SPEC,
  `docs/paper-section-statistics-and-threats.md` at 18adb67, per 01 §6.2).

### 6.12 The failure ladder ("catastrophe ladder"; the user's point) (panel 3) — 193.5 × 284 mm

- Title: "Seven failures, one pattern". Mechanism line: "In each, the words survive and the referent does not."
- Seven rungs, 31 mm tall, ordered **bottom to top by the depth of check that catches it** (so the deepest, most dangerous failures sit
  at the top and the figure visually rhymes with the ladder of 6.5). Each rung: what happened (17 pt SemiBold) · the measured scale
  (20 pt Bold `harm-text`) · status (FIXED with the CHANGELOG line, or "fix not confirmed") · the catching check as a depth-ramp chip.
  An amber 3 mm bar marks real incidents.

| rung (top → bottom) | what happened | scale | status | caught by |
|---|---|---|---|---|
| 7 | every COG reader rounded the pixel index "from the first commit"; the signer read the pixel 10 m south | 162 of 200 sampled records | FIXED 2026-09-28 (`CHANGELOG.md:68`, `:47`) | L3 source re-read only |
| 6 | an EUDR plot across a tile line read the far side's out-of-image pixels as 0: "a forest-2020 of 0 or a loss year of 0, a pass" | every plot across a 3° / 10° tile line | FIXED (`CHANGELOG.md:53`) | L3 re-read of the far tile (INFERRED) |
| 5 | an upstream failure signed as a finding: Overpass HTTP-200 errors signed "not protected" | every failed call | FIXED (`CHANGELOG.md:60`) | L3 re-read / absence reason (INFERRED) |
| 4 | WorldPop signed people per pixel, not per km² | 1.77× low (Paris) | FIXED (`CHANGELOG.md:61`) | L2 independent recompute (INFERRED) |
| 3 | superseded releases (Hansen v1.12, GFC2020 V3) still answered "latest" | every pre-fix read | FIXED; "Nothing signed is rewritten." (`CHANGELOG.md:54`) | L1 version / as-of binding |
| 2 | asked for 23 Sep, the raster tool served the 25 Sep scene with no warning | 9 of 10 agents never saw 23 Sep values; 3 of 10 then said no 23 Sep scene existed | found 30 Sep (defect 27); no CHANGELOG entry at 18adb67 (MEASURED grep): fix not confirmed | L1 bind time to the question |
| 1 | "Keylong (32.57126 N, 77.03448 E)" answered from the town cell 597 m away | 1 query, NDVI 0.28 instead of the field's | found (defect 37); fix not confirmed | L1 bind cell |

  A side rail along the ladder (`ink2`): "a refusal returned as text is a refusal ignored: LangChain's MCP adapter returned the
  wrong-cell refusal as ordinary text; emem's SDK now raises (`CHANGELOG.md:32`)" (MEASURED in report 02's refusal matrix; SPEC).
- Caption-as-claim (63 words): "Seven failures found in emem, a system built for evidence. Five are fixed; its signatures prevented none. Each is
  a class any agent pipeline can produce, and a receiver that reads only the words passes all seven. Binding the reference to the
  question catches the lower three at handoff; the signer's own errors need an independent recompute or a source re-read."
- Labels: "passes all seven" is INFERRED from R1 (prose/JSON accept every in-scope class) and must be stated as such in the claims map;
  "prevented none" follows report 02 §18. External generality (MAST FM-3.2/3.3; position paper arXiv 2604.24919; OWASP ASI06/07) goes
  to the 30 cm footnote, worded as report 04 §5 allows: the classes are documented elsewhere; no other system is said to have these
  bugs.
- Why it is the "wow" (INFERRED): it turns emem's own defect list into evidence that the failure is general and silent, and the
  ordering shows that the most dangerous failures are exactly the ones that pass every integrity check.

### 6.13 What a paraphrase loses (panel 2; MASTER §27 left, referential drift) — 193.5 × 108 mm

- Encoding: a relay of three bubbles `0.4708994708994709` → "0.4709" → "about 0.47", then the rule bar at 0.4705 with the decision flip.
- Data: `research/repro/data/v8/results.json` (G2): B = claude-haiku-4-5; arm R (prose "0.47", exploratory) 5 of 5 IRRIGATE, arm T
  (token) 10 of 10 HOLD; Fisher one-sided p = 0.00033 (exploratory); A = claude-sonnet-5-5 prose carried all 16 digits 10 of 10, 1 of
  10 wrote the wrong year (MEASURED).
- Take line (24 pt): "Rounded to '0.47', 5 of 5 receivers irrigated; handed the reference, 10 of 10 held."
- Scope (14 pt): "Threshold constructed so rounding flips it; exploratory arm; one model pair."
- Drop from the face: the compaction chart (emem-authored two-model study; its two published figures disagree, defect 28; 01 §2.2).
  Keep one 30 cm line if wanted, with the defect noted.

### 6.14 A screen an auditor can re-run, Rondônia (panel 9; MASTER §21) — 193.5 × 121 mm

- Data: `case_rondonia_eudr.json`: 10 × 10 lattice, spacing 0.006667° (~740 m), categories not forest 2020 and no Hansen loss 43 ·
  forest 2020, no later loss 33 · cleared 2001–2020 20 · **EUDR flag: forest 2020, loss after 2020 3** · loss after 2020 on GFC2020
  non-forest 1 (MEASURED).
- Encoding: the lattice as point symbols coded by shape and colour (flag: 7 mm `harm` disc; forest: `emem` disc; cleared: ink
  triangle; non-forest: grey dot; disagreement: amber diamond), over a real S2 true colour if fetched (5.5), else over white; the
  auditor card for cell A (`defi.zb391.taza.zcc31`: Hansen loss 2023, tree cover 2000 100 %, GFC2020 V4 forest, TMF 2023, CCI 208 t/ha,
  each with its CID prefix; 01 §2.2).
- Mandatory line, 17 pt Bold (MASTER §21): "Point samples, not parcel polygons; not a regulatory determination."
- Caption-as-claim (34 words): "Every input of this screen is a signed fact an auditor can fetch: 100 point samples 740 m apart, 600 facts.
  Three cells were forest in 2020 and lost tree cover after 31 Dec 2020."

### 6.15 Questions and hypotheses (left column; MASTER §7–8) — 193.5 × 88 mm

Typographic block: RQ1–RQ4 one line each (15 pt, 500) with the panel number that answers it ("→ 1, 5"; "→ 5"; "→ 1"; "→ 7"), then
H1–H3 in one line. This turns the RQs into a navigation device (INFERRED).

### 6.16 Header image and QR set

- Header (full bleed, cols 10–12 + bleed, 216.5 × 183 mm incl. bleed): the signed-grid true colour cropped to aspect 1.18 (all 443
  columns, rows chosen to keep row 212 inside), the cited cell in a white 6 mm box, and a black 62 % strip: "The record this board
  follows: NDVI 0.4709 · 10 m cell · Sentinel-2A L2A · Keylong · 25 Sep 2026" (17/14 pt). It is evidence, not decoration: the same
  pixel appears in panels 1, 4 and 6.
- QRs (verb-led, one destination each, issue #34; destinations from 03 §7 and the brief; each needs the mobile test):

| label | size | where | destination |
|---|---|---|---|
| TRY THIS TOKEN | 60 mm | header, on a white tile over the image | `https://emem.dev/verify` (v12 target, HTTP 200 per 01) or a page pre-filled with the hero token |
| INSPECT THE RECORD | 40 mm | panel 4 | `GET /v1/facts/oj5cecci…` (JSON) |
| RE-RUN THE TEST | 40 mm | panel 5 | the R1/R5 repro folder in Vortx-AI/esa_poster |
| VIEW THE DEMO | 40 mm | panel 1 | the ≤ 20 s demo of issue #35 (only when it exists) |
| DISCOVER INTEGRATIONS | 40 mm | panel 11 | `https://emem.dev/#use` |
| READ THE METHODS | 40 mm | conclusion block | methods + claims map |

---

## 7. Page composition

Mock: **`/tmp/claude-0/-home-user-esa-poster/0db6b3ad-8059-51a6-bd74-2d7a97faf986/scratchpad/v13/mock_layout.png`** (841 × 1189 mm at
60 dpi, real point sizes, faint 12-column overlay; miniatures drawn from `mutation_matrix.json`, the signed grids, `pixel_windows.json`,
`case_rondonia_eudr.json`, `crossruntime_table.json`). 3 m simulation: `mock_layout_3m.png`.

### 7.1 Blocks (y from the top edge, mm; x by column)

| block | cols | x – x (mm) | y – y (mm) | w × h | tier | share of page |
|---|---|---|---|---|---|---|
| header: title, hero, boundary line, authors + venue; real scene; QR | 1–9 text, 10–12 image (bleed) | −3 – 844 | 0 – 180 | 841 × 180 | 3 m | 15.1 % |
| 1 spine: "What survives an agent handoff?" | 1–12 | 20 – 821 | 188 – 378 | 801 × 190 | 3 m / 1 m | 15.2 % |
| 2 What a paraphrase loses | 1–3 | 20 – 213.5 | 390 – 498 | 193.5 × 108 | 1 m | 2.1 % |
| 3 Seven failures, one pattern | 1–3 | 20 – 213.5 | 508 – 792 | 193.5 × 284 | 1 m | 5.5 % |
| Questions | 1–3 | 20 – 213.5 | 802 – 890 | 193.5 × 88 | 1 m / 30 cm | 1.7 % |
| Threat model | 1–3 | 20 – 213.5 | 900 – 1006 | 193.5 × 106 | 1 m / 30 cm | 2.1 % |
| 4 What is handed over | 4–9 | 222.5 – 618.5 | 390 – 548 | 396 × 158 | 1 m / 30 cm | 6.3 % |
| 5 Which check stops which corruption | 4–9 | 222.5 – 618.5 | 558 – 813 | 396 × 255 | 3 m / 1 m | 10.1 % |
| 6 The right record, the wrong pixel | 4–9 | 222.5 – 618.5 | 823 – 1006 | 396 × 183 | 3 m / 1 m | 7.2 % |
| 7 What the checks establish | 10–12 | 627.5 – 821 | 390 – 593 | 193.5 × 203 | 1 m | 3.9 % |
| 8 Same place, different time | 10–12 | 627.5 – 821 | 603 – 743 | 193.5 × 140 | 1 m | 2.7 % |
| 9 A screen an auditor can re-run | 10–12 | 627.5 – 821 | 753 – 874 | 193.5 × 121 | 1 m | 2.3 % |
| 10 What it costs | 10–12 | 627.5 – 821 | 884 – 1006 | 193.5 × 122 | 1 m / 30 cm | 2.4 % |
| 11 One evidence protocol, multiple agent runtimes | 1–8 | 20 – 551 | 1016 – 1174 | 531 × 158 | 1 m | 8.4 % |
| 12 Seven layers, one question each | 9–12 | 560 – 821 | 1016 – 1112 | 261 × 96 | 1 m / 30 cm | 2.5 % |
| conclusion (issue #38) + READ THE METHODS QR | 9–12 | 560 – 821 | 1120 – 1174 | 261 × 54 | 1 m | 1.4 % |
| footer: references (14 pt), commit, retrieval dates | 1–12 | 20 – 821 | 1177 – 1189 | 801 × 12 | 30 cm | 1.0 % |

Main experiment (spine + matrix + wrong pixel) = 32.6 % of the page with these heights; v12: 11.0 %.
Implementation detail (formulas, schema bar, SAT-042) = 0 % of the face (v12: 14.3 %: 7.73 + 6.55; 01 §2.3) (MEASURED areas).

### 7.2 Reading path and the three distances

- **3 m** (what must be readable without stepping closer): the hero sentence (100 pt) → the title (56 pt) → the boundary line
  (32–36 pt, legible from ~1.9 m) → the spine's lane names and the outcome numerals "15 / 15 … 0 / 16" (64 pt) → the real Keylong scene
  and the 5 × 5 window with the two outlined pixels → the matrix as a pattern (vermillion block on the left, blue staircase on the
  right). The simulation `mock_layout_3m.png` confirms these survive and that 14–17 pt text does not.
- **1 m**: panel titles as questions, take lines, the spine's check chain, the matrix rows and totals, M15 values, the ladder's status
  words, the time panel's as-of line, the ecosystem path and groups.
- **30 cm** (the ammo bar): the record's fields and CIDs, scope lines, statistics (Wilson CIs, n, dates), references, commit, retrieval
  dates, QR labels, the native-support inset, the prior-art footnote.
- Sequence (MASTER §30): "I understand the failure" (spine + panel 2–3) → "I see the exact invention" (header + panel 4) → "I can see
  the experiment" (panels 1, 5) → "what it proves and doesn't" (panels 6, 7, threat) → "it works across ecosystems" (11) → "I want to
  try it" (QRs).

### 7.3 The seven 30-second questions (MASTER §28) against the composition

| question | answered at | tier |
|---|---|---|
| What problem? | spine lanes + panel 2 take line | 3 m / 1 m |
| What is new? | hero + panel 4 token | 3 m / 1 m |
| What evidence? | spine numerals, panel 5 totals, panel 6 waffle, panel 8 as-of line | 3 m / 1 m |
| What does it not prove? | header boundary line, spine boundary wall, panel 7 L4–L5 | 2 m / 1 m |
| Why not STAC/RAG/C2PA/GeoGuard? | panel 12 | 1 m |
| Can I use it? | panel 11 path and groups | 1 m |
| Can I reproduce it? | QRs in panels 1, 4, 5, 11 and the conclusion | 30 cm |

### 7.4 What the mock showed (MEASURED by looking at the render)

- The hero at 100 pt and the title at 56 pt fit the 9-column text block in two lines each (widths in 2.3).
- 40 pt titles overflow 3-column panels above ~24 characters → 34 pt and ≤ 27 characters (gate).
- Two-digit panel numbers overlapped titles at a 14 mm offset → 22 mm.
- Text set on the 45° hatch (ladder L4/L5) is illegible → white plate behind text, hatch on the remaining area.
- Labels of several dots on one shared log axis collide → one row per item.
- The matrix reads as a pattern at 3 m; individual letters do not (by design).

---

## 8. Conclusion block (issue #38) and copy rules for figures

Conclusion (35 words, measured scope, report 04 vocabulary): "EMEM lets agents hand off a reference to an observation that the receiver
can re-check. Our mutation tests show which corruptions it catches; sensor accuracy and the entity meant remain separate questions."
After R5, add the agent numbers from the results file.

Figure-copy rules (issues #21, #23): active verbs (cite, hand off, resolve, re-hash, re-read, recompute, refuse, preserve); never
"verified" without its layer; none of first, only (except "only the re-read" where the leave-one-out proves it), unique, truth,
guarantees, proves, trustless; no version or process language (v11, v12, defects) on the face (issue #37).

---

## 9. Existing v12 figures: keep, redraw or drop

| v12 figure (`poster/fig/v12/`) | decision | why / what changes |
|---|---|---|
| `r1_mutation.svg` | **redraw** as 6.2 | regroup rows by MASTER §9 family; five condition columns (+ RAG with R5); "first check" letters with "only" rings from the leave-one-out; flips column; scope line inside; 10.1 % of the page instead of 7.96 % |
| `m15.svg` | **redraw** as 6.3 | real true-colour scene and window from the signed grids; waffle of 162/200; error magnitudes; the real pre-fix record line; "≠" message in the caption |
| `r4_bitemporal.svg` | **redraw** as 6.4 | pictorial bars + as-of lines before numbers; add the Keylong valid-time strip; agent framing |
| `eo_rondonia.svg` | **redraw** compact as 6.14 | shape-coded lattice; the mandatory "point samples, not polygons, not regulatory" line; keep the auditor card |
| `failure.svg` (compaction study) | **drop** from the face | emem-authored, two-model, figures disagree (defect 28); panel 2 uses the team's own G2 measurement instead; at most one 30 cm line |
| `eo_keylong.svg` (141 NDVI facts) | **drop** as a panel; reuse its data | the series appears as the valid-time strip of 6.4; its caption was the issue #36 "bad example" |
| `eo_berlin.svg` | **drop** | the board follows one Keylong record; issue #20 moves to the native-support inset of 6.6; Berlin's 25/25 PASS goes to the methods page |
| `encoding.svg` (43 slots, 1,792 dims) | **drop** | schema figure with no result (MASTER §19, §26); embeddings appear only as two products in the native-support inset, each bound to its encoder fn_key |
| `model.svg` (six formulas) | **drop** | implementation detail (issue #18); its signature formula contradicts `attest.rs:34` (01 finding 3); the one invariant needed (record → BLAKE3 → address) is drawn in 6.6 |
| `drift.svg` (Δz formula), `score.svg` | **drop** | no result on the board depends on them |
| `sat042.svg` | **drop** from the face | an extension (MASTER §20); one 30 cm line in the methods footer: "Extension: the same receiver checks over signed execution traces, in a scripted reference harness; no spacecraft enrolled." |
| `qr_try.svg`, `qr_repro.svg` | **regenerate** | verb-led set of six (6.16); the build decodes each QR and compares it with its payload (01 §1.1 gate 5 gap) |
| `poster/make_figures_v12.py` helpers `fig_mm`, `mm_axes`, `check_text` | **keep** | 1:1 mm drawing and the 15 pt / clipping / overlap asserts are the right discipline; lower the floor to 14 pt and keep text as text |

---

## 10. Build implications (for the build agent; nothing implemented here)

1. Tokens in one file (`poster/src/tokens.json`): every hex of section 3 with role, FOGRA39 CMYK and ΔE00; figures and CSS read it;
   a gate re-runs the CVD and FOGRA39 checks (`palette_check.py`) and fails on any new hex.
2. Fonts: ship the complete Plex Sans/Mono; a gate fails if any printed code point is missing from the face that sets it.
3. Type: a gate fails on text below 14 pt anywhere (CSS and SVG), on a 3-column title above 27 characters at 34 pt, and on a panel above
   its word budget (2.3).
4. Images: integer nearest-neighbour upscaling only; ≥ 300 ppi at print size; the processing line printed under each image; the
   window-equality assert of `proto_m15.py` in the figure script.
5. Text in figures stays selectable (or is dumped), so the prose gate and the claim-status gate (issue #21) cover figure labels.
6. Export: an sRGB PDF and a FOGRA39 soft-proof; text K-only; TAC ≤ 300 % on fills.
7. Each caption is generated from the data file it cites, so a changed number changes the caption (issue #36).

---

## 11. Open items

1. **Copy the scratchpad artifacts into the repo** (`proto_m15.py`, `mock_layout.py`, `palette_check.py`, `palette_final.py`, the
   complete Plex TTFs or the npm versions, and a pointer to the Adobe FOGRA39 profile, which is not redistributable): the scratchpad
   is ephemeral. Suggested location: `research/v13/visual/`.
2. The print shop's condition (sRGB inkjet vs FOGRA39/FOGRA51 CMYK) decides the export; ask before 10 Oct.
3. R5 (report 02) decides whether the RAG column and the agent-level numerals exist; without it the spine and matrix print R1 only,
   labelled "deterministic verifier, no model".
4. The real 23 Sep S2C B02/B03 window for an exact-scene image of `kxjvfwpa` (optional; 6.3).
5. Rondônia imagery (optional; 5.5) via Planetary Computer, not via emem read tools (defect 29).
6. Native support of the met.no forecast and of GeoTessera at this cell: source each from product documentation before printing the
   inset, or omit the row.
7. The MCP tool-list token count moved (18,659 in `token_counts.json`; 20,838 LIVE on 30 Sep per report 02): re-measure at build time
   and print one value with its date.
8. Fix status of defects 27 (date substitution) and 37 (place drift) at the commit the board cites: no CHANGELOG entry found at 18adb67
   (MEASURED grep); print "fix not confirmed" unless a fix is found.
9. The mobile test of every QR (03 §7) and of the INSPECT THE RECORD JSON on a phone.
10. The 780/780 and 266/780 ladder counts come from report 01 (from `eo_evidence_verification.md`); re-derive them in the figure script
    from `eo_evidence_per_fact_checks.csv`.
