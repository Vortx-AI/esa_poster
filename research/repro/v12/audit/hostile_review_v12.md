# Hostile review: EMEM A0 poster v12

Target: EMEM board v12 for "Agentic AI for Earth Observation" (ESA Φ-lab and BIFOLD, Berlin), Poster Session 1, 19 Oct 2026, 17:00 to 18:30.
Reviewer stance: senior EO scientist, 90 seconds at the board. Review only; nothing was edited or rebuilt.

## 0. Inputs, method, and where each check comes from

| input | used for |
|---|---|
| `v4fb6b207_emem-poster-A0.pdf` (1 page, 841 x 1189 mm, WeasyPrint 69.0) | rendered at 110 dpi (about 1:1 on a screen) in 10 region crops; 300 dpi grayscale strips for text-size measurement |
| `v520d1ba6_poster.v12.html` | exact board wording, CSS font sizes of live text |
| `vc184ee8a_19_V12_CLAIMS_MAP.md` | every printed number, provenance class per fact, scope notes |
| live `GET https://emem.dev/v1/bands` (30 Sep 2026, HTTP 200, 43 bands, bands_cid `mesoyti3qcs2...`) | product names, versions, units and pitfalls as emem itself serves them |
| GitHub contents API on `Vortx-AI/esa_poster@main` | `research/repro/v12` and `research/should_do/19_V12_CLAIMS_MAP.md` both return 200 (QR payload path exists; QR images were not decoded) |
| project memory from earlier sessions today (labelled **[memory]**) | code findings at emem 04b40c5, Keylong hero-fact quality fields, Zenodo record title; not re-verified here |
| literature | Legge critical print size (0.2 deg x-height); NASA Terra orbit-drift notes |

Figure text on the board is outlined (paths), so its size was measured from the raster: the x-height band of each label strip divided by 0.518 (the x-height/em ratio calibrated on four live-text lines of known size: 0.514 to 0.524). Figure sizes are therefore approximate (about ±0.3 mm).

---

## 1. Reading path, as a visitor walks it

1. **Header.** The first thing read is a struck-through phrase in the title. The explanation ("Why the strike") is in section 1, right column, about 300 mm lower, in 6.8 mm body text. The header raises a question it does not answer. The DOI printed in the header resolves to a Zenodo v0.1.0 record whose title still reads "over Foundation-Model Embeddings" **[memory]**, so a visitor who scans it finds the struck title as the published one.
2. **Header to Problem: the first two claims contradict each other.** Punchline: "When agents disagree, the satellite decides." Next headline: "Agents that agree are not agents that are right." One says disagreement triggers adjudication; the next says agreement is the danger. Read together, agreeing but wrong agents are never checked.
3. **Problem figure.** The bars show agreement and correctness falling together (36/36 to 15/36 to 3/36 pairs agree; 72/72 to 20/72 to 0/72 right). The headline needs "agree and wrong", which the chart does not show directly. It can be derived: under pressure the 3 agreeing pairs must all be wrong, since 0/72 answers are right. The caption names the models but not the task, and nothing in the panel is Earth observation. The link to EO arrives only in "The idea".
4. **Idea to section 1.** This is the cleanest hand-off on the board (cell id, fact_cid, re-read). "0.4709 becomes about 0.47" foreshadows the Keylong record before the visitor has seen it; that is acceptable.
5. **Section 1 holds two unrelated figures.** The Berlin product stack (what a cell holds) sits beside the 43-slot encoding bar (how the cube is laid out, and what was struck). No sentence maps a Berlin row to a slot. The encoding bar's real job is to justify the title strike, so it belongs with the header claim, not with "One address, every satellite". The section title "every satellite" is contradicted inside the figure by "Overture Maps (not EO)", Copernicus CAMS (a model forecast) and ISRIC SoilGrids (a predictive map).
6. **Sections 2 and 3 are in inverted order.** Section 2's subtitle uses "the Keylong NDVI record" before Keylong is shown; section 3's caption then points back ("Circled: the record corrupted in section 2"). The visitor meets the corrupted record before the clean one.
7. **Orphan: "Memory on two clocks" (Bengaluru DEM) in section 2.** It has nothing to do with corruption, introduces a fourth location with no map, and its only other anchor is conclusion 3. It is a stand-alone result placed in section 2 for lack of room.
8. **Section 3 arithmetic does not close on the board.** The subtitle says "All 780 facts behind sections 1 and 3"; the board shows 16 (Berlin) + 141 (Keylong) + 600 (Rondônia) = 757. The claims map explains the difference (Berlin 25, Keylong 155), but the board does not. The Rondônia caption lists Sentinel-2 as a source, but no Sentinel-2 layer appears in either panel. The CCI biomass panel does not enter the flag logic, so it is a second map with no role in the result.
9. **Section 4** has no place, no named anchor product, and no definition of the score (0.05, 0.15, 0.88). Its right column is mostly empty below the take-away line (visual estimate from the crop). The caveat "a trace proves what ran, not that the sensor was right" is the third statement of one idea, after "the value's accuracy: inherited" (table) and "A signature does not make a value true" (Q&A).
10. **Bottom row.** Conclusion 1 restates the idea, 2 restates section 2, and 3 rests only on the orphan Bengaluru panel. Nothing concludes section 3 (EO use) or section 4 (traces). The Q&A answer "No spacecraft is enrolled" corrects the section 4 title, but sits 150 mm below it. The claims map has two addresses: "research/repro/v12" in the bottom box and "research/should_do/19_V12_CLAIMS_MAP.md" in the footer.

---

## 2. Title and punchline verdict

**Title replacement, "Satellite Observations and Signed Execution Traces", checked against the scope on the board: it overclaims on both halves.**

- *Satellite Observations.* In the flagship Berlin cell, by the classes the claims map records, 3 of 16 facts are `direct_sensor`, 1 is `deterministic_index`, 9 are `model_output`, 1 is `human_curated` and 2 are `unclassified`. The live registry has 23 of 43 slots as `model_output` (claims map, and live /v1/bands). CAMS is served "via the Open-Meteo Air Quality API. Hourly forecasts at ~11 km" (live /v1/bands). Overture is labelled "not EO" on the board itself. So most of what the board serves are satellite-derived or model products, not observations.
- *The strike's own logic.* "Why the strike" says an embedding "is a model output: only its checkpoint vouches for it". The same sentence applies to WorldCover, CCI Biomass, Hansen, GFC2020 and CAMS, all kept and all `model_output`. The defensible distinction is that those products publish an accuracy assessment and an embedding has no ground truth to validate against. The board does not say that.
- *Audience risk.* ESA Φ-lab co-hosts the event, and EO foundation models are a Φ-lab research line. A struck "Foundation-Model Embeddings" in the title is the first thing Φ-lab staff will read. The encoding figure still shows 944 of 1,792 dimensions as encoder slots.
- *Signed Execution Traces.* This is a protocol shown in a harness run. The claims map scope note says "SAT-042 is a deterministic reference run compiled in a harness crate ... not a live spacecraft"; live /v1/devices lists one generic host; `orbital.satellite.v1` is a candidate. Per **[memory]**, 0 of 43 live bands carry attested execution, and the earlier traces verdict recommended the wording "with Signed Execution Traces", not "over ... Signed Execution Traces". Putting "over" in front of traces claims the protocol operates over trace data it does not yet hold.
- Proposed replacement (no em dashes): **"... for AI Agents over ~~Foundation-Model Embeddings~~ Earth-Observation Products, with Signed Execution Traces"**.

**Punchline, "When agents disagree, the satellite decides.": it contradicts the board. Change it.**

- The condition is wrong. The problem panel argues agreement is not evidence, and the verifier in section 2 runs on every handoff whatever the agents say. "When agents disagree" makes the check conditional, which is exactly the failure the problem panel warns about.
- The subject is wrong for most of the stack. The satellite cannot decide for a CAMS forecast, an Overture count, a SoilGrids prediction or a signed absence. In section 4 the "satellite" is the thing being scored, by an open-archive anchor. And the guarantees table says accuracy is "inherited".
- Proposed: **"Agreement is not evidence. Re-read the pixel."** This keeps the board's own verb (re-read, column I, M15) and holds for every case the board demonstrates.
- The sub-line "Every number an agent cites resolves to signed bytes, and re-reads to the pixel it came from." also overclaims. The claims map says only 266 of the 780 facts were recomputed from signed inputs, and "the rest ... were not re-read from the upstream COGs" (780 minus 266 = 514). Signed absences and the CAMS/Overture rows have no pixel. Proposed: **"Every number an agent cites resolves to signed bytes and names the file it came from; open-archive pixels can be re-read."**

---

## 3. EO correctness: Berlin figure, row by row

Sources for each verdict: **CM** = claims map, **LB** = live /v1/bands (30 Sep 2026), **M** = project memory, **K** = domain knowledge.

| product as printed | reading / valid time as printed | verdict | fix (exact words) |
|---|---|---|---|
| Sentinel-2C MSI L2A | NIR reflectance 0.0475 / 27 Sep 2026 | Plausible for a dark urban pixel. The band is not named: 10 m NIR is B08, and B8A is 20 m. Expect the question "was BOA_ADD_OFFSET applied?" (baseline 04.00 and later). The registry unit text says only "reflectance x 10000 ... divide by 1e4" (LB). For the Keylong hero fact the bytes carry BOA offset -1000 (M); this Berlin fact was not checked. | "NIR reflectance 0.0475" to "NIR (B08) reflectance 0.0475" |
| Sentinel-2C MSI L2A | NDVI 0.195 / 27 Sep 2026 | Consistent with the NIR value (implied red about 0.032, derived). OK. | none |
| Sentinel-1 C-SAR GRD, RTC | VV backscatter −2.82 dB / 28 Sep 2026 | The unit is right: the registry states dB of gamma-naught (LB). The coefficient is unnamed on the board. It is a single pixel, which emem's own pitfall advises against: "Speckle noise is significant ... average a 3x3 cell window" (LB). | "VV backscatter −2.82 dB" to "VV γ⁰ −2.82 dB, one pixel" |
| Copernicus DEM GLO-30 | elevation 36.6 m / GLO-30 release | GLO-30 is a surface model; the registry itself says it "includes building / canopy heights" (LB). In central Berlin that matters. "GLO-30 release" is a publication event, not a valid time (the source acquisitions predate it, K). This undercuts the bitemporal story in section 2. Side note: the same registry pitfall says to "pull GLO-90 for a DTM-like product", but GLO-90 is also a DSM (K). | "elevation 36.6 m" to "surface height 36.6 m (DSM)" |
| Terra MODIS MOD11A2 | day surface temp. 297.4 K / 29 Aug 2026, 8-day | Product, unit (K) and 8-day compositing are consistent. 29 Aug 2026 is day of year 241, a valid MOD11A2 composite start (1 + 8k), derived. Issues: it is a 1 km product read at a 10 m cell; Terra's orbit has drifted (NASA expects sunlight conditions to move from 10:30 to 8:30 local time at the descending node by late 2026), so this day LST comes from an earlier overpass than the heritage record; and emem classes it `unclassified` (CM, M), which the board's own table glosses as "nothing: it fails closed, lowest rank". | "day surface temp. 297.4 K" to "daytime LST 297.4 K (1 km)" |
| ESA WorldCover 2021 v200 | class 50: built-up / 2021 | Correct: class 50 is Built-up, and v200 is the 2021 map. | none |
| ESA CCI Biomass v7 | biomass 0 t/ha / 2022 | **Version conflict.** Live /v1/bands describes this band as "ESA Climate Change Initiative Biomass v6.0", with 2022 as the "most-recent v6.0 epoch". The board (row and footer reference) says v7. Wrong-versioning an ESA CCI product at an ESA event is costly. The unit t/ha equals Mg/ha, matching the registry. | "ESA CCI Biomass v7" to "ESA CCI Biomass v6.0" (row, and "ESA CCI Biomass v7" in References), unless the fact's own source field says v7; the board and registry must agree |
| JRC Global Surface Water | water occurrence 0 % / 1984 to 2021 | Consistent with the GSW occurrence record (K). OK. | none |
| Hansen Forest Change v1.13 | tree cover 2000: 0 % / 2000 | Matches the registry: "Hansen Global Forest Change v1.13 (2000-2025 annual update)" (LB). OK. | none |
| JRC Forest Cover 2020 | not forest (EUDR baseline) / 2020 | The name differs from "JRC GFC2020" used in section 3 and the references. No version is given, while the registry says "V4 since 2026-09 (V3, the 2026-03 release, is withdrawn and its URLs answer 404)" (LB). "EUDR baseline" overstates the map's status; the registry quotes JRC calling it "non-mandatory, non-exclusive and not legally binding" (LB). | "JRC Forest Cover 2020" to "JRC GFC2020 V4" (if the fact was read from V4); "not forest (EUDR baseline)" to "not forest (EUDR reference map)" |
| Copernicus CAMS | surface NO₂ 12.3 µg/m³ / 30 Sep 2026, 18 UTC | The unit is right for surface concentration. But the row names a programme, not a product, and the signed bytes come from a relay: "via the Open-Meteo Air Quality API. Hourly forecasts at ~11 km" (LB). A read "live on 30 Sep" at 18 UTC may be a forecast, not an analysis. | "Copernicus CAMS" to "CAMS forecast via Open-Meteo (about 11 km)" |
| Overture Maps (not EO) | 0 building footprints / 2026-08-19 release | Honestly labelled, but it contradicts the section title "every satellite". Its valid time is again a release date. | fix the section title (objection 18) |
| ISRIC SoilGrids v2 | no data at this cell / signed absence | The registry calls it SoilGrids 2.0, "a predictive map" (LB). It is a model, not a satellite product. OK as an absence. | none |
| CHIRPS v2.0 | outside the ±50° product | Correct: the cell is at 52.52 N (M), outside the 50 S to 50 N domain. | none |
| JRC Tropical Moist Forest | outside the tropical belt | Correct. | none |
| NASA FIRMS, VIIRS + MODIS | no active fire in 24 h | A missing detection is not a missing fire (cloud, overpass timing). Class `unclassified` (M). | "no active fire in 24 h" to "no fire detected in 24 h" |
| chip | Sentinel-2C MSI L2A, 27 Sep 2026, 2.56 km across | Consistent: 256 pixels at 10 m, derived. | none |

Keylong (section 3): 141 S2 L2A NDVI facts, and peaks 0.79 (6 Aug 2025) and 0.73 (27 Jul 2026) match the claims map. A cal/val visitor will point at the single-date drops (the Oct 2025 point near 0 between values near 0.5; the Aug 2025 dip) and ask whether the series is SCL-masked. The registry says `indices.ndvi` is "already cloud-gated" (LB), and the hero record's bytes carry SCL class 4, baseline N0513, BOA offset -1000 and scene cloud 10.84 % (M). None of this is on the board. The amber label "the record in section 2 ..." overprints a data marker and the connecting line (verified in a 160 dpi crop).

---

## 4. Rondônia EUDR framing

- **What is printed:** heading "A deforestation check an auditor can re-run"; panel title "EUDR check per cell"; caption "100 cells 740 m apart, 600 facts ... Flag: forest in 2020, loss after the EUDR cut-off"; legend 3 / 1 / 33 / 20 / 43. All counts match the claims map.
- **Tree-cover loss is not deforestation.** Hansen loss year marks stand-replacing tree-cover loss (fire, logging and natural disturbance included). EUDR deforestation means conversion of forest to agricultural use. The flag is a land-cover screen, not a land-use finding.
- **The reference map is non-binding and versioned.** The registry states the JRC map is "non-mandatory, non-exclusive and not legally binding" and that V3 was withdrawn in favour of V4 in Sep 2026 (LB). The board names neither the status nor the version. "An auditor can re-run" fails if the facts point at V3 URLs that now return 404. The registry says "a fact signed from V3 still says V3" (LB).
- **Point lattice, not plots.** The claims map scope note: "point samples, not plot polygons, and is not an Annex II statement". The board omits this. Derived arithmetic, assuming the 10 x 10 lattice drawn: 100 cells of 10 m x 10 m cover 0.01 km² of a lattice spanning about 6.66 km x 6.66 km (about 44 km²), which is about 0.02 % of the area. A clearing between nodes is invisible.
- **Verdict:** the demonstration is good (every input is re-runnable), but the label "check" invites an auditor to say it is not a check. Call it a screen and carry the scope note on the board (objection 8).

---

## 5. SAT-042 panel

- The claims map calls it "a deterministic reference run compiled in a harness crate against emem 04b40c5 ... not a live spacecraft". The board calls it "the reference spacecraft pass in emem's code", under the title "Satellites that prove what they ran". Present tense and plural claim a capability no spacecraft has exercised.
- The board says "its profile demands a signed OS execution trace: eight layers for orbital.satellite.v1". The claims map says `orbital.satellite.v1` "is candidate". The board omits the status.
- The board says "A write with no trace, and a fact the trace never emitted, are refused." Per **[memory]**, at the commit the footer cites (04b40c5), `POST /v1/attest_cbor` calls an ungated `Storage::put_attestation` that "admits an enrolled key without a trace"; that session concluded the poster "must not claim that every device write carries a verified trace" until it is fixed. If it is unfixed, a code reader can falsify this line from the commit the board itself names.
- The Q&A says "The trace verifier is live on emem.dev; SAT-042 exercises every refusal." That reads as if SAT-042 ran against emem.dev. Per the claims map, live /v1/devices lists one generic host, and SAT-042 ran in the harness.
- The anchor is not named ("device NDVI vs anchor 0.6402 ± 0.02"). The claims map shows the same anchor 0.6402 for three different cells (`natI.tUpu`, `nadU.tUra`, `mUgI.tUsE`), which gives away a fixture. The score scale is undefined: 0.6431 scores 0.05 and 0.6512 scores 0.15, both inside ±0.02 of the anchor, and the board does not say why.
- Step 5 "Honest batch ADMITTED 3 facts" includes the 0.2103 value that step 6 then marks "contradicted". This is correct under the board's logic (a trace attests execution, not truth), but a visitor will ask "you admitted a contradicted reading?" Be ready.
- Ground-segment questions the board cannot answer: where the device key lives on board, trace volume against the downlink budget, time source, and relation to CCSDS link security. The empty right column of section 4 has room for one line on this.

---

## 6. Remaining work-in-progress framing

1. The title strike itself reads as an edit mark to anyone who does not reach "Why the strike".
2. "research/should_do/19_V12_CLAIMS_MAP.md" in the footer: a folder called `should_do` reads as a to-do list. The bottom box gives a second location ("research/repro/v12") for the same claims map.
3. "the reference spacecraft pass in emem's code" and "Mechanisms read from emem's code at 04b40c5" are code-internal framing on the board face.
4. The DOI record is v0.1.0 with the old title **[memory]**.
5. PDF metadata title ends "(A0 poster, v12)"; harmless in print, visible if the PDF is shared.
6. The QR payload path `research/repro/v12` exists on `main` (GitHub API 200, checked today), so the "valid once merged" caveat no longer applies.

---

## 7. Legibility at 1.5 m (measured at print scale)

Criterion: fluent reading needs an x-height of at least about 0.2 deg (12 arcmin), the consensus critical print size for normally sighted readers (Legge). At 1.5 m that is an x-height of 5.2 mm, or an em size of about 10.1 mm for IBM Plex Sans (x-height/em = 0.518, measured).

| text class | em (mm) | pt | x-height arcmin at 1.5 m | fluent up to |
|---|---|---|---|---|
| footer references and reproducibility (live) | 4.2 | 11.9 | 5.0 | 0.62 m |
| QR caption "Check any token emem.dev/verify" (live) | 4.6 | 13.0 | 5.5 | 0.68 m |
| guarantees table header (live, caps) | 4.8 | 13.6 | 5.7 | 0.71 m |
| author links, WRITER / RECEIVER (live) | 5.0 | 14.2 | 5.9 | 0.74 m |
| smallest figure labels (SAT-042 sub-labels, matrix legend, Rondônia legend; approx.) | about 5.2 | 14.7 | 6.2 | 0.77 m |
| captions (live) | 5.4 | 15.3 | 6.4 | 0.80 m |
| typical figure labels (matrix rows about 5.6, Berlin readings about 6.0; approx.) | 5.6 to 6.0 | 15.9 to 17.0 | 6.6 to 7.1 | 0.83 to 0.89 m |
| body text and sub-punchline (live) | 6.8 | 19.3 | 8.1 | 1.01 m |
| h3 (live) | 7.6 | 21.5 | 9.0 | 1.13 m |
| section heads (live) | 10.0 to 10.6 | 28.3 to 30.0 | 11.9 to 12.6 | 1.48 to 1.57 m |
| punchline (live) | 12.4 | 35.1 | 14.7 | 1.84 m |
| title (live) | 15.6 | 44.2 | 18.5 | 2.31 m |

At 1.5 m a visitor reads fluently only the title, the punchline and the section heads. Everything else needs a step to 1 m or closer. The call to action ("Check any token emem.dev/verify", 4.6 mm) and the footer (4.2 mm) are the only text near acuity level at 1.5 m. Live text on the board totals 894 words (PDF text layer) before figure labels, which is well beyond a 90-second visit.

---

## 8. Ranked objections

Severity: **LTR** = lose-the-room, **costly** = costs the presenter credibility if unanswered, **minor** = cosmetic or low-probability.

| # | objection | who asks | severity | where it bites | one-line spoken answer | fix: change from | fix: change to |
|---|---|---|---|---|---|---|---|
| 1 | "Satellites that prove what they ran": no satellite has; SAT-042 is a harness run and the orbital profile is a candidate | ESA ground-segment engineer | LTR | §4 title and subtitle; title "Signed Execution Traces"; Q&A | "No spacecraft is enrolled. SAT-042 is a scripted pass in our test harness, orbital.satellite.v1 is a candidate profile, and the live verifier runs on one generic host." | "Satellites that prove what they ran" / "SAT-042, the reference spacecraft pass in emem's code, run on 30 Sep 2026." / "The trace verifier is live on emem.dev; SAT-042 exercises every refusal." | "How a satellite could prove what it ran" / "SAT-042, a scripted pass in emem's test harness, not a spacecraft, run on 30 Sep 2026." / "The trace verifier is live on emem.dev for one generic host; SAT-042 exercises every refusal in the test harness." |
| 2 | The punchline contradicts the problem headline: if agents agree and are wrong, nothing is checked | agent/LLM researcher | LTR | header punchline vs Problem h2 | "The check runs on every handoff, agreed or not; agreement is exactly what we do not trust." | "When agents disagree, the satellite decides." | "Agreement is not evidence. Re-read the pixel." |
| 3 | You struck embeddings as "model output", but 9 of your 16 Berlin facts are model outputs, 944 of 1,792 dimensions are still encoder slots, and Φ-lab co-hosts | EO foundation-model researcher (Φ-lab); provenance person | LTR | title strike; "Why the strike"; encoding figure | "We struck vectors with no validation target, not models. WorldCover or CCI Biomass publish an accuracy assessment; an embedding cannot, and a new encoder moves every vector." | "Satellite Observations and Signed Execution Traces" / "An embedding is a model output: only its checkpoint vouches for it, and a new encoder moves every vector." | "Earth-Observation Products, with Signed Execution Traces" / "An embedding has no ground truth to validate against, and a new encoder moves every vector." |
| 4 | At the commit you cite, POST /v1/attest_cbor admits an enrolled key without a trace [memory] | provenance/standards person reading the code | LTR if unfixed | §4 "A write with no trace ... are refused"; footer "at 04b40c5" | "On the gated write paths, yes. The CBOR attest path was ungated at 04b40c5; it is closed at [commit], or say it is being closed." | "A write with no trace, and a fact the trace never emitted, are refused." | "On the gated write paths, a write with no trace, and a fact the trace never emitted, are refused." (or fix the code and cite the fixing commit) |
| 5 | "Re-reads to the pixel it came from": for CAMS, Overture and the absences there is no pixel, and only 266 of 780 facts were recomputed | EO cal/val scientist | costly | header sub-line | "Every number resolves to signed bytes and names its file; re-reading applies to open-archive pixels, and we recomputed 266 of the 780 for this board." | "Every number an agent cites resolves to signed bytes, and re-reads to the pixel it came from." | "Every number an agent cites resolves to signed bytes and names the file it came from; open-archive pixels can be re-read." |
| 6 | "One 10 m cell" holding a 1 km LST, a 100 m biomass and an 11 km CAMS forecast: what does "at the cell" mean? | EO cal/val scientist | costly | §1 subtitle; Berlin figure | "Each value is read at the cell centre from the product's native grid, and the fact names the source file, so the grid is recoverable." | "One 10 m cell in central Berlin, read live on 30 Sep 2026: 15 products, 16 signed facts, 4 of them signed absences." | "One 10 m cell in central Berlin, read live on 30 Sep 2026 from each product's native grid (10 m to about 11 km): 15 products, 16 signed facts, 4 of them signed absences." |
| 7 | "The observation: guaranteed", yet your own M15 is a signed record with the wrong pixel | EO cal/val scientist | costly | guarantees table, row 2 | "The signature binds cell, band and time to the value; whether the signer read the right pixel is what re-reading checks, as M15 shows." | "the observation / guaranteed / cell, band, time in the bytes" | "the observation / bound / cell, band, time signed; re-read confirms" |
| 8 | This is not an EUDR check: tree-cover loss is not conversion to agriculture, the JRC map is non-binding, and a 740 m point lattice is not plot geolocation | policy/EUDR auditor | costly | §3 right heading, "EUDR check per cell", caption; Berlin row "EUDR baseline" | "It is a screen, not a due-diligence statement: point samples, not polygons. What the auditor can re-run is every input." | "A deforestation check an auditor can re-run" / "Flag: forest in 2020, loss after the EUDR cut-off." | "A deforestation screen an auditor can re-run" / "Flag: forest in 2020, loss after the EUDR cut-off. Point samples, not plot polygons; a screen, not a due-diligence statement." |
| 9 | CCI Biomass "v7" on the board, but emem.dev serves the band as v6.0 | EO cal/val scientist (CCI) | costly | Berlin row; References | "The record names its source file; the board label is wrong and will match the registry." (only if true) | "ESA CCI Biomass v7" | "ESA CCI Biomass v6.0" (unless the fact source says v7; then fix the registry text) |
| 10 | Which JRC GFC2020 version? V3 was withdrawn in Sep 2026 and its URLs return 404, so can an auditor still re-run it? | policy/EUDR auditor; provenance person | costly | §3 caption; Berlin row | "Each fact names the file it read, so a V3 fact still says V3; the 600 Rondônia facts were read from [V3 or V4]." | "JRC GFC2020 and TMF" / "JRC Forest Cover 2020" | "JRC GFC2020 V4 and TMF" / "JRC GFC2020 V4" (only if V4 was read) |
| 11 | Your CAMS bytes are an Open-Meteo API response, not a CAMS file, and possibly a forecast | provenance/standards person | costly | Berlin CAMS row | "Right: that row is a relay of the CAMS forecast at about 11 km, classed model_output, and the fact says so." | "Copernicus CAMS" | "CAMS forecast via Open-Meteo (about 11 km)" |
| 12 | How is this different from STAC, openEO, C2PA, W3C PROV, and the traceable-agent posters in this room? | provenance/standards person | costly | Q&A answer 2 | "STAC names the scene, openEO the process, C2PA the asset; emem signs the one value an agent cites and names the scene and file it came from, so it sits under all three." | "They find files, run processes, sign media. emem names the one observation an agent cites, so each of them can check it." | "STAC names the scene, openEO the process, C2PA the asset. emem signs the one value an agent cites and names the scene and file it came from." |
| 13 | "With every check ... offline, in under 2 ms" includes re-reading a COG? | ESA ground-segment engineer | costly | §2 take-away | "The 1.182 ms covers [state which checks]; re-reading the source is a network read." | "With every check, none of the 16 in-scope cases gets through; offline, in under 2 ms." | "With every check, none of the 16 in-scope cases gets through; checks C to H run offline in under 2 ms." (only if the timing excludes check I) |
| 14 | The SAT-042 anchor is unnamed, is the same value for three different cells, and the score is undefined | EO cal/val scientist | costly | §4 anchor chart | "In the harness the anchor is one fixed value; on a real pass it is the open-archive reading at the same cell and date." | "device NDVI vs anchor 0.6402 ± 0.02" | "device NDVI vs one fixed harness anchor, 0.6402 ± 0.02" (and add one line defining the score) |
| 15 | Your DOI resolves to a record titled "over Foundation-Model Embeddings" [memory] | provenance/standards person | costly | header DOI | "That is v0.1.0 from June; the new version is [DOI]." | "doi:10.5281/zenodo.20706893" | "doi:10.5281/zenodo.20706893 (v0.1.0, June 2026)" (or mint a new version before 19 Oct and print it) |
| 16 | The Keylong series has single-date drops: is it cloud- and snow-masked? | EO cal/val scientist | costly | §3 Keylong chart | "Each fact carries its SCL class and baseline; the circled record is SCL 4, baseline N0513, BOA offset -1000 recorded." [memory; verify before 19 Oct] | "Circled: the record corrupted in section 2." | "Circled: the record corrupted in section 2 (SCL class 4, baseline N0513, in its signed bytes)." |
| 17 | The problem chart shows agreement and accuracy falling together, which is not what the headline says | agent/LLM researcher | costly | Problem figure and caption | "Under pressure, the 3 pairs that still agree are all wrong: 0 of 72 answers are right." | "Pre-registered compaction study, Gemma-4-12B and Qwen2.5-7B on one host." | "Pre-registered compaction study, Gemma-4-12B and Qwen2.5-7B on one host. Under pressure, the 3 pairs that still agree are all wrong." |
| 18 | "Every satellite", but the rows include Overture (not EO), a CAMS forecast and SoilGrids | EO cal/val scientist | minor | §1 title | "Every product: the class column says which are sensors and which are models." | "One address, every satellite" | "One address, every product" |
| 19 | "Each check stops a corruption the others miss": in your matrix, opaque id catches only M7, which hash also catches; your leave-one-out found hash subsumed by signature [memory] | agent/LLM researcher | minor | conclusion 2 | "Binding, signature, log, recompute and re-read are each necessary; id and hash are convenience layers." | "Each check stops a corruption the others miss; together, all 16." | "Binding, signature, log, recompute and re-read each stop a corruption the others miss; together, all 16." |
| 20 | Copernicus DEM is a DSM; in central Berlin 36.6 m includes roofs, and "GLO-30 release" is not a valid time | EO cal/val; provenance person (bitemporal) | minor | Berlin DEM row | "Right, it is surface height, and the valid time should be the acquisition epoch, not the release." | "elevation 36.6 m" | "surface height 36.6 m (DSM)" |
| 21 | MODIS LST: 1 km, a drifted Terra overpass, and classed "unclassified" (by your table, "nothing") | EO cal/val scientist | minor | Berlin MODIS row; encoding table | "It is not yet in the registry, so it fails closed; Terra's overpass has drifted earlier, and the fact carries the acquisition date." | "day surface temp. 297.4 K" | "daytime LST 297.4 K (1 km)" |
| 22 | Single-pixel S1 backscatter, when your own registry says to average 3x3 | SAR scientist | minor | Berlin S1 row | "It is shown to prove the address, not for inference; the registry pitfall travels with the fact." | "VV backscatter −2.82 dB" | "VV γ⁰ −2.82 dB, one pixel" |
| 23 | 780 facts, but I count 16 + 141 + 600 = 757 on the board | any sharp visitor | minor | §3 subtitle | "The other 23 are 9 more Berlin facts and the 14 Keylong points before 2025; all 780 verified." | "All 780 facts behind sections 1 and 3 were re-hashed" | "All 780 facts pulled for sections 1 and 3, including the 757 shown, were re-hashed" |
| 24 | Section 2 uses the Keylong record before section 3 shows it; the Bengaluru clock panel is an orphan | any visitor | minor | §2 subtitle; §2 right column | "Read section 3 first: the circled point is the record we corrupt." | "Agent B receives the Keylong NDVI record after one corruption." | "Agent B receives one Keylong NDVI record (section 3, circled) after one corruption." |
| 25 | "No active fire" from FIRMS is an absence of detection | EO cal/val scientist | minor | Berlin FIRMS row | "Correct: it is a signed absence of detections." | "no active fire in 24 h" | "no fire detected in 24 h" |
| 26 | I cannot read the call to action from 1.5 m | any visitor | minor | header QR caption (4.6 mm); footer (4.2 mm) | none (layout) | "Check any token" at 4.6 mm | "Check any token" at 6.8 mm or larger |
| 27 | Two addresses for the claims map, and one path is "should_do" | provenance person | minor | footer vs bottom box | "Both resolve; the canonical one is research/repro/v12." | "research/should_do/19_V12_CLAIMS_MAP.md at github.com/Vortx-AI/esa_poster" | "research/repro/v12 at github.com/Vortx-AI/esa_poster" (only if the claims map is copied there) |
| 28 | The Keylong annotation overprints the data | any visitor | minor | §3 Keylong chart | none (layout) | label position of "the record in section 2: 0.4709, 25 Sep 2026" | move the label above the series, clear of markers |

---

## 9. The three objections most likely to lose the room

1. **"Satellites that prove what they ran", with no satellite (objections 1 and 4).** The room is ESA ground-segment and Φ-lab people. The section title, the "reference spacecraft pass" subtitle and "Signed Execution Traces" in the title all claim present capability. The claims map says it is a harness run with a candidate profile, and project memory records an ungated write path at the very commit the footer cites. One engineer asking "which spacecraft?" followed by "which commit closes attest_cbor?" ends the conversation.
2. **The first two lines disagree with each other (objection 2).** "When agents disagree, the satellite decides" is followed immediately by "Agents that agree are not agents that are right." An agent researcher needs no domain knowledge to spot it, and it lands in the first 10 seconds. It also makes the check sound conditional, which the section 2 verifier is not.
3. **The strike, in a Φ-lab room, with a self-defeating reason (objections 3 and 15).** It strikes the host's research line in the title, justifies the strike by "model output" while 9 of 16 kept facts are model outputs, still shows 944 of 1,792 encoder dimensions, and prints a DOI whose title is the struck one. The replacement "Satellite Observations" then overclaims for a stack that includes a relayed CAMS forecast. Reframe the strike as "no validation target", not "model output".

Next tier, likely to cost credibility with specific people rather than the whole room: the EUDR framing (objections 8 and 10) and the CCI Biomass version conflict with emem's own registry (objection 9).
