# EMEM poster v11.2: section-by-section standards audit

Board: `Vortx-AI/esa_poster` main `643451a` (v11.2), `poster/emem-poster-A0.pdf` rendered and read, `poster/src/poster.v11.html` read. emem code: `Vortx-AI/emem` main `04b40c5` (the board cites `18adb67`, two commits earlier). ememdemo `bc06197`. Live emem.dev read-only GETs on 30 Sep 2026, 18:55 to 19:05 UTC. Review only: nothing on the board was edited or rebuilt.

Overall verdict rule: fail if the truth check fails or two or more of EO, poster, visual and issues fail; pass only if all five pass; otherwise weak.

Standards applied per section: (a) EO science (CEOS-ARD / CARD4L per-pixel quality, cal/val and uncertainty, W3C PROV / STAC provenance, sensor and processing-level naming); (b) poster communication (legible from 1.5 m, one message per panel, figure carries the message, jargon load); (c) truth against `research/should_do/15_V11_CLAIMS_MAP.md`, emem code and the live service; (d) esa_poster issues #5, #6, #7; (e) visual clarity; plus work-in-progress framing.

## Ranked objection table

| # | section | objection | who asks | severity | where it bites | spoken answer | fix needed |
|---|---|---|---|---|---|---|---|
| 1 | Header / title block | Your title says 'over foundation-model embeddings'. Where are the embeddings? | ESA Phi-lab reviewer; any visitor reading the title first | High | y 0-94 mm, full width | They were the first thing we signed. We retired the encoders in September, and every vector signed before still verifies. What stays is the layer underneath: satellite observations, each signed and checkable. | yes |
| 2 | The Problem | Is this an Earth-observation problem or a generic LLM memory problem? Show me an EO agent that failed. | EO agent builder (the room's majority) | High | x 22-390, y 95-162 mm | One Sentinel-2 field, two agents. After one summary the NDVI arrived as 0.47 instead of 0.4709, and the irrigation decision flipped. R2 and R3 measure exactly that. | yes |
| 3 | Hero figure: world writes / fact plane / agents read | Sixteen digits of NDVI and no uncertainty. Was the pixel cloud-free, and what is the reflectance uncertainty? | CEOS cal/val scientist; poster judge at 1.5 m | High | x 22-819, y 162-392 mm (about 18 % of board area) | The signed bytes carry the pixel's scene class, vegetation, and the scene's 10.8 % cloud cover. Sixteen digits is identity, not accuracy. Accuracy is the L2A product's own validation, and the record points to the exact file. | yes |
| 4 | C5 Verification that needs no trust | Who checks the checker? Your verifier spec is written by you. | Security reviewer; CEOS cal/val scientist | High | x 290-560, y 500-597 mm | An unaffiliated agent built its own verifier from the published spec and rejected all five tampered receipts. The spec is generated from the signer's own constants. | yes |
| 5 | What agents do with it: tools strip and scale line | Forty-six sources. How many are satellites, and at what processing level? Can I get a TROPOMI NO2 value now? | EO agent builder; sceptical reviewer | High | x 22-819, y 597-660 mm | Sentinel-1 as radiometrically terrain-corrected VV, Sentinel-2 at L2A, Copernicus DEM, plus ESA, JRC and Hansen products. TROPOMI is declared in the registry but not read today, so we do not claim it. | yes |
| 6 | The Invention | Two nodes read the same pixel. Do they get the same name? | Protocol or STAC engineer | High | x 400-819, y 95-162 mm | No. The name is of one signed reading. The observation's key is place, band and time; the name proves which reading you received. | yes |
| 7 | R1 The mutation test | This is a unit test of your own verifier on one record. Where are the agents and the error bars? And 'one error' hit most of your Sentinel-2 records for four months. | ML evaluation reviewer; statistician | High | x 22-290, y 703-968 mm; matrix about 275 x 160 mm (about 4 % of board area) | R1 isolates what each check stops, with no model to blame. R2 and R3 put models in the loop. M15 is one error class, a pixel-rounding rule, and the source re-read is how we found it. | yes |
| 8 | What a verified token guarantees (table) | 'The value's truth: tested.' Re-reading the archive tests you, not the Earth. | Cal/val scientist; provenance (W3C PROV) person | High | x 518-819, y 968-1062 mm | Agreed. The re-read tests fidelity to the archive. Accuracy is the product's own validation; emem makes the value traceable to it. | yes |
| 9 | C4 One token algebra, pixel to archive | openEO already records the process graph. What does a cube token add? | openEO / STAC engineer | Medium | x 22-290, y 500-597 mm | A process graph names the recipe. The cube token names the exact scenes and pixels it ran on, signed, so a second party rebuilds the same array. | yes |
| 10 | C1 An address for every observation | Your cell is not my pixel. Which Sentinel-2 pixel does a 9.5 m cell take? | Sentinel-2 L2A user | Medium | x 22-290, y 410-500 mm | The pixel that contains the cell's point, in the tile's own UTM grid. The record signs the point and the EPSG code, so anyone can re-read that pixel. | yes |
| 11 | C2 A memory on two clocks | A DEM has no valid time. Show me two clocks on a time series. | Time-series / change-detection scientist | Medium | x 290-560, y 410-500 mm | Any band works. Ask for NDVI as it was on 25 September, as known on 26 September. Both bounds are signed into the receipt. | yes |
| 12 | C3 Machines write facts; agents write claims | What stops your own reader from writing a wrong fact? | Data-quality lead; guardrail researcher | Medium | x 560-819, y 410-500 mm | Only the re-read, which is why every record names its public source pixel. R1's M15 is our own reader's error, found exactly that way. | yes |
| 13 | C6 Computation others can recompute | A year-on-year NDVI drop of 0.13 from two dates. Is that change, or phenology and illumination? | Change-detection scientist | Medium | x 560-819, y 500-597 mm | C6 proves the arithmetic over two signed readings, same date a year apart. Whether it is change is the analyst's call, and both pixels can be re-read. | yes |
| 14 | What agents do with it: four vignettes | Which of these did you measure? | EUDR / policy visitor; sceptic who reads the claims map | Medium | x 22-819, y 660-703 mm | None of these four; they are field reports from emem's README. The four results below are ours, with scripts. | yes |
| 15 | R2 Agreement is not evidence | BM25 ties you at 20 of 20. Why do I need emem? | LLM-agents researcher; statistician | Medium | x 307-570, y 725-862 mm | BM25 finds the string when it is in the corpus. It cannot tell the receiver that the string is the signed one. R1 shows what that costs. | yes |
| 16 | R4 Memory through time | That is GLO-90 against GLO-30, not a provider change. Why did a 30 m band ever hold a 90 m value? | DEM / geodesy specialist | Medium | x 576-819, y 725-968 mm | It should not have. The record says which product it read, so the substitution is visible and dated. That is the point of keeping both. | yes |
| 17 | Discussion | Your 'independent' second node is also you. | Cal/val scientist; independence sceptic | Medium | x 22-510, y 968-1112 mm | Yes. The checks need no operator: stock libraries and a published key. The binary is Apache-2.0, so anyone can run a node. | yes |
| 18 | Conclusion | Under 2 ms including fetching the COG pixel? | Anyone who reads only the conclusion | Medium | x 22-510, y 1112-1162 mm | No. Under 2 ms for hash, signature, log and arithmetic. Re-reading the pixel is one range request to the public archive. | yes |
| 19 | R3 A token helps only when checked | n of 5 and 10, one vendor. Token and prose tie. What did the token buy? | LLM-agents researcher | Low | x 307-570, y 862-968 mm | Refusal. Prose cannot be refused. A forged token was refused five times out of five, by the resolver, not by the model. | yes |
| 20 | Try it / evidence boxes | Three QR codes. Which one do I scan? | Visitor with a phone | Low | x 518-819, y 1062-1160 mm | The top one. Paste any token and your browser re-checks it. | yes |
| 21 | References / footer | Your DOI is a June paper with a different design. | ESA programme reviewer | Low | x 22-819, y 1162-1189 mm | It is the first version. This board is whitepaper v3, in the repository. The DOI's title is the one struck through above. | yes |

## Verdict grid

| section | EO | poster | truth | issues #5-#7 | visual | WIP on board |
|---|---|---|---|---|---|---|
| Header / title block | weak | weak | fail | fail (#5) | weak | Not WIP wording, but reads as in flux: 'method: whitepaper v3, emem @18adb67' puts a commit hash in the title block; 'paper doi' (Zenodo v0.1.0, 15 Jun 2026) and 'whitepaper v3' are two different documents on one line. |
| The Problem | fail | weak | pass | fail (#5 step 1) | weak | none |
| The Invention | weak | pass | weak | pass (#5 thesis) / weak (#6) | pass | none |
| Hero figure: world writes / fact plane / agents read | weak | fail | weak | fail (#5), partial (#7) | fail | 'enrolled devices (next)' chip under OTHER WRITERS. |
| C1 An address for every observation | weak | weak | pass | pass (#5 invariant) | weak | none |
| C2 A memory on two clocks | weak | weak | pass | fail (#5 formula load) | weak | none |
| C3 Machines write facts; agents write claims | weak | weak | pass | pass (#7 separation) | weak | none |
| C4 One token algebra, pixel to archive | weak | fail | pass | fail (#5 internals) | fail | none |
| C5 Verification that needs no trust | weak | fail | weak | partial (#5 path) | fail | none |
| C6 Computation others can recompute | weak | weak | weak | pass (#7 derivation integrity) | weak | none |
| What agents do with it: tools strip and scale line | weak | fail | weak | fail (#5) | fail | none |
| What agents do with it: four vignettes | weak | weak | weak | fail (#6 evidence standard) | weak | none |
| R1 The mutation test | weak | pass | weak | pass (#5 focal) / partial (#6) | weak | none |
| R2 Agreement is not evidence | fail | pass | pass | pass (#5 failure) / partial (#6) | pass | none |
| R3 A token helps only when checked | fail | weak | weak | partial (#6) | weak | 'rounded arm exploratory' is a method note, acceptable. |
| R4 Memory through time | weak | pass | pass | pass (#7 source change visible) | pass | none |
| Discussion | weak | weak | weak | pass on content (#5 must-remain-explicit) / fail on form | fail | Heading 'Independent operation is the next step.' and 'Next: independent operators, provider-signed upstream identity and a multi-vendor agent study.' |
| What a verified token guarantees (table) | weak | pass | weak | partial (#7) | weak | 'COG and pixel recorded; provider signature next'. |
| Try it / evidence boxes | weak | weak | pass | pass (#5: traces behind QR) | weak | none |
| Conclusion | weak | weak | weak | partial (#5) | weak | none |
| References / footer | weak | weak | pass | n/a | weak | 'Paper v0.1.0; this board describes whitepaper v3.' |

## The three objections most likely to lose the room

1. **Your title says 'over foundation-model embeddings'. Where are they?** Asked by: ESA Phi-lab reviewer. Bites: Title vs Discussion ('left the code') vs R1 ('embeddings are not covered'). Say: "They were the first thing we signed. We retired the encoders in September, and every vector signed before still verifies. What stays is the layer underneath: satellite observations, each signed and checkable."
2. **Sixteen-digit NDVI, no uncertainty, and 'the value's truth: tested'. Re-reading the archive is not validation.** Asked by: CEOS cal/val scientist. Bites: Hero record, guarantees table row 5, Discussion item 1. Say: "Agreed. The re-read tests fidelity to the archive. The bytes carry the pixel's scene class and the scene's cloud cover; accuracy is the L2A product's own validation, and the record points to the exact file."
3. **'One observation, one signed record'? Your R4 shows one DEM cell signed seven times under seven names, and two nodes reading one pixel get two names.** Asked by: Protocol / STAC engineer. Bites: Invention headline vs R4 caption vs per-replica identity in emem's protocol. Say: "The name is of one signed reading. The observation's key is place, band and time. Join on the key, cite the name."

## Three weakest sections

1. Header / title block: the title's EO noun ('Foundation-Model Embeddings') is retired in code and on emem.dev, the board's own Discussion says so, the DOI is the June v0.1.0 paper, the word 'satellite' appears nowhere, and a 485.5 x 34.5 mm band next to the title is empty.
2. Hero figure: 417 words at a 12.8 pt median (100 % of characters under 18 pt), an internals diagram that duplicates C1 to C6, prints 16-digit NDVI without the scene class and processing baseline that are in the signed bytes, lists retired 'Earth embeddings' as a writer and carries '(next)'.
3. What agents do with it (tools strip and vignettes): an API catalogue in monospace between mechanism and results; '168 recipes' and '46 source schemes' include retired encoders; the four vignettes are README claims not re-measured; the board's EO breadth (Sentinel-1 VV, JRC, Hansen, MODIS, ERA5, SoilGrids) should live here and does not.

## Title and header

Fail on truth, weak on communication. 'over Foundation-Model Embeddings' is inherited from the Zenodo record 20706893 (v0.1.0, 15 Jun 2026, the only version). At emem 04b40c5 Clay v1.5, Prithvi-EO-2.0, Galileo and the JEPA head are removed from code; GeoTESSERA is retired on emem.dev by configuration; live /v1/capabilities reports no models loaded; 39 of 168 recipes cannot run (provisional, band-prefix match); 944 of 1,792 cube dims are retired encoder slots. The board itself says the encoders 'left the code'. emem's README headline is now 'Satellites for AI.' A red strike-through is defensible only as a deliberate continuity device (the DOI title stays citable) and only if the header also carries the replacement and a one-line reason, and the board explains referential drift, the memory encoding and the provenance classes. Without the punchline the strike reads as a correction the authors forgot to finish. Header free space: 485.5 x 34.5 mm (x 279.5-765.0 mm, y 44.2-78.8 mm) right of title line 2, plus 336.0 x 49.8 mm (x 429-765, y 44.2-94.0 mm) right of the metadata line. With 4 to 6 mm gutters that fits about one line of roughly 50 characters at about 45 pt, or two lines of roughly 80 characters at about 28 pt (estimate from IBM Plex Sans average advance width, not a render).

Header free space (measured on the PDF): 485.5 x 34.5 mm (x 279.5-765.0 mm, y 44.2-78.8 mm from the top edge), bounded by title line 2, the QR panel, line-1 descenders and the metadata line; plus 336.0 x 49.8 mm (x 429-765, y 44.2-94.0 mm) right of the metadata line. Method: page rendered at 4 px/mm; any pixel more than 40 RGB units from the navy band counted as ink; largest empty axis-aligned rectangle inside x 22-819 mm.

## Workflow cohesion

1. The reading path breaks at the first line: the title promises embeddings; the Problem, Invention, hero, C1 to C6 and R1 to R4 never use one, and the Discussion reports their retirement. Conclusion 3 then claims a result 'across retired encoders' that no panel measures.
2. Mechanism is shown twice before any evidence. The hero carries C1 to C6 badges and the six cards restate it; together they fill y 162-597 mm (about 37 % of the board height). The first result starts at y 725 mm, 61 % of the way down.
3. 'What agents do with it' sits between mechanism and results. It is the lowest-evidence panel on the board (README claims per the claims map) and interrupts the mechanism-to-evidence step.
4. Forward references force the eye down and back: the Problem cites R2, the Invention cites R1, C2 cites R4. Issue #5's order (failure, intervention, measured detection, mechanism) is R2, R3, R1, then C1. The board runs mechanism, R1, R2, R3, R4.
5. Repeats: 918.0 to 915.07 m four times in text plus the R4 figure; the six receiver checks in the hero, C5 formula, R1 columns, guarantees table and Conclusion 2; the 256-fact bundle five times; the guard (9 mentions) in hero, C6, tools strip and Discussion; '84 characters' three times; 're-read' seven times. Discussion item 1 and guarantees rows 4 and 5 say the same thing.
6. No EO arc. The only satellite image is top-left. After the hero the Earth content is one DEM cell, a road in Venice, a road in Doha and a 28 degC weather value. 'Satellite' 0 mentions, 'Sentinel-2' 1, 'uncertainty', 'validation', 'calibration', 'CEOS' 0 each.
7. Visual weight is inverted relative to issue #5: the internals hero is about 18 % of board area; the R1 matrix, which issue #5 wants as the focal point, is about 4 %.
8. Legibility at 1.5 m: outside the title block and footer, every region has a median of 12.8-17.6 pt and 69-100 % of its characters under 18 pt; common A0 guidance is 24 pt or more for body text. Section heads are 27.2 pt, the title 51.6 pt.
9. Work-in-progress framing on the board, four places: 'enrolled devices (next)' (hero), 'provider signature next' (guarantees table), 'Independent operation is the next step' and 'Next: ...' (Discussion), 'Paper v0.1.0; this board describes whitepaper v3' (footer).
10. If 'Foundation-Model Embeddings' stays struck through, three things the founder requires are missing: 'referential drift' (0 mentions); the memory encoding (43 cube slots, 1,792 dims, cell64, canonical CBOR, BLAKE3; only the last three appear, in formulas); the provenance classes (present only as the unlabelled depth ladder in C5). Measured caveat for that panel: in bands-v0.json, 944 of 1,792 dims (52.7 %) are the four retired encoder slots and 162 dims are reserved or unclassified; model_output is 23 of 43 slots.

## Section detail

### Header / title block

Location: y 0-94 mm, full width. Verdict: **fail (EO weak; poster weak; truth fail; issues fail (#5); visual weak)**. Severity: High.

- **Evidence.** Title 51.6 pt, 16 words, two lines. The word 'satellite' appears 0 times on the whole board; 'Sentinel-2' once (hero caption). Zenodo record 20706893 is v0.1.0 of 15 Jun 2026 and is the only version; its title is the poster title. emem 2.4.2 removed Clay, Prithvi-EO-2.0, Galileo and the JEPA head from code (CHANGELOG, 29 Sep); GeoTESSERA is retired on emem.dev by configuration; live /v1/capabilities on 30 Sep: models_loaded [], cuda_available false. Header free space: 485.5 x 34.5 mm right of title line 2 (x 279.5-765.0, y 44.2-78.8 mm), plus 336.0 x 49.8 mm right of the metadata line (x 429-765, y 44.2-94.0 mm).
- **Undersells.** emem's own README now opens with 'Satellites for AI.' and 'the machine-maintained, external memory of our physical world'. The header names no mission, although emem reads Sentinel-1 RTC, Sentinel-2 L2A, Copernicus DEM, ESA WorldCover, JRC GSW, Hansen GFC, MODIS, CAMS and ERA5 live. The event's own framing is 'beyond foundation models' and the onboard segment; emem has an operator-satellite profile (orbital.satellite.v1) that fits it and is not mentioned.
- **Objection** (ESA Phi-lab reviewer; any visitor reading the title first). Your title says 'over foundation-model embeddings'. Where are the embeddings?
- **Spoken answer.** They were the first thing we signed. We retired the encoders in September, and every vector signed before still verifies. What stays is the layer underneath: satellite observations, each signed and checkable.
- **Fix.** Strike 'Foundation-Model Embeddings' and put the replacement noun (for example 'Satellite Observations') plus a one-line punchline in the 485 x 34 mm band. Drop the commit hash from the header. Either mint Zenodo v0.2 before print or show only the DOI, not 'whitepaper v3'. If the struck phrase stays, the board must also carry referential drift, the memory encoding and the provenance classes (see cohesion).
- **WIP framing.** Not WIP wording, but reads as in flux: 'method: whitepaper v3, emem @18adb67' puts a commit hash in the title block; 'paper doi' (Zenodo v0.1.0, 15 Jun 2026) and 'whitepaper v3' are two different documents on one line.

### The Problem

Location: x 22-390, y 95-162 mm. Verdict: **fail (EO fail; poster weak; truth pass; issues fail (#5 step 1); visual weak)**. Severity: High.

- **Evidence.** 54 words, median 17.6 pt, no figure, no mission, no place, no value. It cites R2 but shows none of it.
- **Undersells.** The board already holds a concrete EO failure: the Keylong Sentinel-2 NDVI 0.4709 against the rule 'irrigate iff NDVI <= 0.4705'; rounded to 0.47 the decision flips (R1 M2, R3 'prose rounded' 0/5). emem names this failure 'referential drift' with two sides, words move and values move (plugins/emem/skills/emem-referential-drift/SKILL.md); the term never appears on the board.
- **Objection** (EO agent builder (the room's majority)). Is this an Earth-observation problem or a generic LLM memory problem? Show me an EO agent that failed.
- **Spoken answer.** One Sentinel-2 field, two agents. After one summary the NDVI arrived as 0.47 instead of 0.4709, and the irrigation decision flipped. R2 and R3 measure exactly that.
- **Fix.** Lead with the Keylong failure in one sentence and one small graphic (value, threshold, flipped decision). Name it: referential drift, values move. Put the R2 bar chart here (issue #5: concrete failure first).
- **WIP framing.** none

### The Invention

Location: x 400-819, y 95-162 mm. Verdict: **weak (EO weak; poster pass; truth weak; issues pass (#5 thesis) / weak (#6); visual pass)**. Severity: High.

- **Evidence.** Headline 32.3 pt, the strongest text on the board. 'One observation, one signed record' conflicts with emem's per-replica identity: signed_at is inside the hashed body, so each re-signing and each node mints a new fact_cid (capability index 'Per-replica fact identity'; R4 on this board: 915.07 m 'signed 7 times', 'Each re-signing mints a new fact_cid'). 'prose passed all 15 corruptions' uses 'passed' to mean 'let through'. 'On real bytes' is one record and one band.
- **Undersells.** 'Written by machines' is stronger than stated. The hero record's signed bytes (live GET /v1/facts/oj5ceccile...) carry the Sentinel-2 processing baseline N0513 and granule A058804 in the source path, EPSG 32643, scene cloud cover 10.84 %, the pixel's scene-classification class 4 (vegetation, clear), and the BOA offset -1000. That is an EO reader that screens clouds per pixel, not a scraper.
- **Objection** (Protocol or STAC engineer). Two nodes read the same pixel. Do they get the same name?
- **Spoken answer.** No. The name is of one signed reading. The observation's key is place, band and time; the name proves which reading you received.
- **Fix.** Change to 'One place, one address. One reading, one signed name.' Replace 'passed' with 'let through'. Keep the blue sentence: it is issue #5's thesis in the author's words.
- **WIP framing.** none

### Hero figure: world writes / fact plane / agents read

Location: x 22-819, y 162-392 mm (about 18 % of board area). Verdict: **fail (EO weak; poster fail; truth weak; issues fail (#5), partial (#7); visual fail)**. Severity: High.

- **Evidence.** 115 text lines, 417 words, median 12.8 pt, minimum 9.9 pt, 100 % of characters below 18 pt; 24 monospace lines. Seven sub-boxes, six receiver checks, seven token families and a five-bullet note plane, badged C1 to C6, so it is a second copy of the six contributions. NDVI printed to 16 digits with no uncertainty or confidence; the live fact carries confidence 0.95 (an SCL-derived heuristic in code) and no uncertainty object. Source id shown as S2A_MSIL2A_20260925T054251_R005_T43SFS; the signed bytes have the full product path with N0513. 'OTHER WRITERS' lists 'Earth embeddings', retired. '2,568,005 entries on 30 Sep' is the tree size read at 15:56:14Z (research/repro/v8/pub/track10/publish_log.json) while the scale line prints 2.57 M from 2,568,372 at 16:53Z; the claims map lists 2,568,005 only under 'removed'. Live /v1/devices lists one operator-endorsed generic.linux-host with one accepted trace and no platform-attested device.
- **Undersells.** EO breadth and fusion. Live /v1/sources lists 46 schemes; live /v1/materializers wires 116 bands including Sentinel-1 RTC VV (sentinel1_rtc_vv_db@1), 19 Sentinel-2 indices and 13 S2 bands plus SCL, Copernicus DEM, GMRT, ESA WorldCover 2021, JRC GSW (4 bands), JRC TMF, Hansen GFC, MODIS (7), FIRMS active fires, CAMS (7), ERA5 (7), SoilGrids (6). One cell can hold all of them at once (ememdemo 'world: <place>' stacks every layer and cross-checks Copernicus DEM against GMRT and stored NDVI against NDVI recomputed from bands and against MODIS). /v1/worlds serves four signed 1,024-cell scenes, e.g. Rondonia: ESA CCI biomass 2022 with its standard error, Hansen loss year and tree cover 2000, 3,733 facts. The EO-native signed absence is 's2_scl_pixel_unusable': every candidate scene in the window was cloudy at this pixel.
- **Objection** (CEOS cal/val scientist; poster judge at 1.5 m). Sixteen digits of NDVI and no uncertainty. Was the pixel cloud-free, and what is the reflectance uncertainty?
- **Spoken answer.** The signed bytes carry the pixel's scene class, vegetation, and the scene's 10.8 % cloud cover. Sixteen digits is identity, not accuracy. Accuracy is the L2A product's own validation, and the record points to the exact file.
- **Fix.** Cut to one path: Sentinel-2 pixel, bytes, BLAKE3, name, receiver re-hash (issue #5 invariant and path). Show the scene class and processing baseline in the record. Replace the writer chips with a multi-sensor cell stack (S1 VV, S2 NDVI, DEM, WorldCover, JRC water, ERA5). Remove 'Earth embeddings' and '(next)'. Move token families, Merkle batch, log and note plane behind the QR.
- **WIP framing.** 'enrolled devices (next)' chip under OTHER WRITERS.

### C1 An address for every observation

Location: x 22-290, y 410-500 mm. Verdict: **weak (EO weak; poster weak; truth pass; issues pass (#5 invariant); visual weak)**. Severity: Medium.

- **Evidence.** 67 words, median 16.4 pt, 50 % monospace, three formula lines. The cell is a lat/lng grid of about 9.5 x 8.1 m at Keylong; the Sentinel-2 pixel is 10 m in UTM. The card does not say which pixel a cell takes, which is the relation M15 broke in production.
- **Undersells.** cell64 is a global grid of about 9.55 m with a pronounceable text form; tslot is quantised by seven tempo classes from 1 h to static; the record signs the query point and EPSG code, so anyone re-reads the same pixel.
- **Objection** (Sentinel-2 L2A user). Your cell is not my pixel. Which Sentinel-2 pixel does a 9.5 m cell take?
- **Spoken answer.** The pixel that contains the cell's point, in the tile's own UTM grid. The record signs the point and the EPSG code, so anyone can re-read that pixel.
- **Fix.** Keep C1 as the board's single invariant (bytes, BLAKE3, CID). Add one line on cell to pixel. Remove '84 characters' here or in the hero, not both.
- **WIP framing.** none

### C2 A memory on two clocks

Location: x 290-560, y 410-500 mm. Verdict: **weak (EO weak; poster weak; truth pass; issues fail (#5 formula load); visual weak)**. Severity: Medium.

- **Evidence.** Three formula lines; the third (log leaf) belongs to the log, not the clocks. The only demonstration is a DEM (tempo static, tslot 0), so the valid-time clock is never exercised; 918.0 to 915.07 m appears four times in the text layer plus in the R4 figure.
- **Undersells.** Every read primitive (recall, recall_polygon, trajectory, query_region, find_similar, state, memory_bundle) accepts as_of_tslot and as_of_signed_at, and the bound is signed into the receipt. A past as_of_signed_at never materialises on a miss, so the memory cannot invent what it did not know then. That is an audit property EO reviewers value (reprocessed archives, late scenes).
- **Objection** (Time-series / change-detection scientist). A DEM has no valid time. Show me two clocks on a time series.
- **Spoken answer.** Any band works. Ask for NDVI as it was on 25 September, as known on 26 September. Both bounds are signed into the receipt.
- **Fix.** Drop the log-leaf formula. State the rule once in words and point to R4. If R4 stays a DEM, add one dynamic example (NDVI trajectory) or say plainly that the demo exercises record time only.
- **WIP framing.** none

### C3 Machines write facts; agents write claims

Location: x 560-819, y 410-500 mm. Verdict: **weak (EO weak; poster weak; truth pass; issues pass (#7 separation); visual weak)**. Severity: Medium.

- **Evidence.** Two ideas in one card (write access, signed absence). Venice absence verified live: /v1/facts/exhq6lps... kind absence, band overture.transportation.road_bearing_deg, Overture release 2026-09-23.1. The example is a vector map, not EO.
- **Undersells.** The EO absence: 's2_scl_pixel_unusable', signed when every candidate Sentinel-2 scene in the window is cloudy at the pixel, with the SCL class and scene named. Hansen, WorldCover and CCI 404s are signed as absences only while a known tile of the pinned release still answers. 'Could not look' is a separate unsigned skip note, so an unknown never poses as a confirmed absence. The fact plane admits three writer classes: the responder, operator-listed keys and trace-enrolled devices.
- **Objection** (Data-quality lead; guardrail researcher). What stops your own reader from writing a wrong fact?
- **Spoken answer.** Only the re-read, which is why every record names its public source pixel. R1's M15 is our own reader's error, found exactly that way.
- **Fix.** Use a cloud absence as the example (EO-native), or pair Venice with it. Drop the 'HTTP 409' formula line.
- **WIP framing.** none

### C4 One token algebra, pixel to archive

Location: x 22-290, y 500-597 mm. Verdict: **fail (EO weak; poster fail; truth pass; issues fail (#5 internals); visual fail)**. Severity: Medium.

- **Evidence.** 106 words, the longest card; 59 % monospace; four separate numbers; seven families already drawn in the hero. No image of the raster or cube it describes.
- **Undersells.** band_composite: a cloud-masked multi-scene Sentinel-2 median (default rejects SCL 0, 1, 3, 8, 9, 10 and keeps snow) minted as an emem:raster token that anyone rebuilds pixel for pixel. A cube token names the exact scenes used. That is the CEOS-ARD-style per-pixel masking made reproducible, and the card never says so.
- **Objection** (openEO / STAC engineer). openEO already records the process graph. What does a cube token add?
- **Spoken answer.** A process graph names the recipe. The cube token names the exact scenes and pixels it ran on, signed, so a second party rebuilds the same array.
- **Fix.** Replace the list with one picture: the cloud-masked composite or the B04 field, with its token under it. Move tree and bundle to the repo.
- **WIP framing.** none

### C5 Verification that needs no trust

Location: x 290-560, y 500-597 mm. Verdict: **fail (EO weak; poster fail; truth weak; issues partial (#5 path); visual fail)**. Severity: High.

- **Evidence.** 69 % monospace; a six-conjunct logical formula at 14 pt; '15 links, 17 checks, 17.9 s' is the detail issue #5 says to put behind the QR. '725 requests, zero errors' is sourced (emem README line 65: 725 requests with zero errors), but the same sentence reports eleven findings, eight of them real defects since fixed; the board keeps only the first half. The depth ladder (recomputable to attester-only) is the provenance-class mapping, but the words 'provenance class' never appear.
- **Undersells.** Seven provenance classes (direct_sensor, deterministic_index, estimator, attested_execution, model_output, human_curated, unclassified) map to five tamper-evidence levels, ride into every receipt through bands_cid, and are downgraded per fact when a checkpoint hash is missing. Receipt v2 binds the inclusion proof or a signed ABSENT marker, so proof stripping is detectable. Caveat an EO reviewer will raise: in bands-v0.json, ESA WorldCover, ESA CCI biomass, Hansen, JRC GSW and CHIRPS sit in model_output slots, and fetched facts without a checkpoint hash are served as attester_only, although their pixels are as re-readable as Sentinel-2's.
- **Objection** (Security reviewer; CEOS cal/val scientist). Who checks the checker? Your verifier spec is written by you.
- **Spoken answer.** An unaffiliated agent built its own verifier from the published spec and rejected all five tampered receipts. The spec is generated from the signer's own constants.
- **Fix.** Show one path: resolve, re-hash, compare, re-read the pixel. Put the formula and the 15-link trace behind the QR. Print the whole sentence: 'zero errors in 725 requests; eight defects found and fixed'. It reads as strength. Label the ladder 'provenance class' if the embeddings strike-through stays.
- **WIP framing.** none

### C6 Computation others can recompute

Location: x 560-819, y 500-597 mm. Verdict: **weak (EO weak; poster weak; truth weak; issues pass (#7 derivation integrity); visual weak)**. Severity: Medium.

- **Evidence.** Two ideas (derive, guard). The -0.1298 NDVI change is two single dates a year apart, no phenology or cloud context. Claims map: 'The derive response itself (ulp_gap = 0) is not committed; commit it.' The guard example (28.0 degC) is weather.temperature_2m, not EO.
- **Undersells.** change_attribution names the terms behind a moved reading (NDVI, NBR, NDWI pairs) with their fact cids; the 168-recipe registry is content-addressed by algorithms_cid and 74 recipes carry an executable expression tree; parametric temporal_diff bands; the guard runs at nine hook checkpoints.
- **Objection** (Change-detection scientist). A year-on-year NDVI drop of 0.13 from two dates. Is that change, or phenology and illumination?
- **Spoken answer.** C6 proves the arithmetic over two signed readings, same date a year apart. Whether it is change is the analyst's call, and both pixels can be re-read.
- **Fix.** Commit the derive response before print. Keep the guard in one place on the board (it appears in four).
- **WIP framing.** none

### What agents do with it: tools strip and scale line

Location: x 22-819, y 597-660 mm. Verdict: **fail (EO weak; poster fail; truth weak; issues fail (#5); visual fail)**. Severity: High.

- **Evidence.** Eight equal tiles, each a tool name in 12.5-14.7 pt monospace and one line of use: an API catalogue, no focal point. '168 recipes': 39 of 168 take a retired encoder band and cannot run on emem.dev (capability index, band-prefix match, provisional). '46 source schemes' (live /v1/sources, 30 Sep) counts five encoder schemes that mint nothing (geotessera.v1, geotessera, model.prithvi_eo2_300m_tl, model.clay_v1_5, model.galileo_v1) and counts Sentinel-2 and Sentinel-1 more than once. Live log head was 2,570,200 at 18:58Z, consistent with '2.57 M'.
- **Undersells.** The EO breadth itself belongs here as a mission strip: live-wired Sentinel-1 RTC VV, Sentinel-2 L2A (13 bands, 19 indices, SCL), Copernicus DEM, GMRT, ESA WorldCover, JRC GSW and TMF, Hansen GFC, MODIS, FIRMS, CAMS, ERA5, SoilGrids; and EO algorithms such as sar_forest_disturbance (VV drop of at least 3 dB, Reiche et al. 2018), flood_extent_sar_threshold, burn_severity_from_dnbr, bathymetry_stumpf_log_ratio. Guard for v12: TROPOMI CH4 and NO2, Dynamic World and OpenET are declared schemes with no reader in code (the only references are algorithm inputs in algorithms.rs), and the wired nightlights band is DMSP-OLS, not VIIRS DNB. Do not print them as live.
- **Objection** (EO agent builder; sceptical reviewer). Forty-six sources. How many are satellites, and at what processing level? Can I get a TROPOMI NO2 value now?
- **Spoken answer.** Sentinel-1 as radiometrically terrain-corrected VV, Sentinel-2 at L2A, Copernicus DEM, plus ESA, JRC and Hansen products. TROPOMI is declared in the registry but not read today, so we do not claim it.
- **Fix.** Replace the eight tool tiles with a mission-by-band strip of what is wired live, one icon row, 20 pt minimum. Print the number of recipes that run today (about 129 if the provisional 39 holds) or drop the count. Tool names go to the repo.
- **WIP framing.** none

### What agents do with it: four vignettes

Location: x 22-819, y 660-703 mm. Verdict: **weak (EO weak; poster weak; truth weak; issues fail (#6 evidence standard); visual weak)**. Severity: Medium.

- **Evidence.** 149 words at 15.3 pt. The claims map classes all four as README claims, not re-measured. 'Gemma 3 on Amazon Bedrock' and the Doha 9.8 m vs 5.4 m dispute rest on emem's README; the EUDR vignette names no measurement.
- **Undersells.** The EUDR vignette hides the strongest multi-sensor EO chain emem has: Sentinel-1 VV backscatter drop (signed VV facts) confirmed against JRC GFC2020 and Hansen loss year through /v1/eudr_dds and /v1/deforestation_alert, with the Rondonia world as the visual.
- **Objection** (EUDR / policy visitor; sceptic who reads the claims map). Which of these did you measure?
- **Spoken answer.** None of these four; they are field reports from emem's README. The four results below are ours, with scripts.
- **Fix.** Keep one vignette, the EUDR deforestation check, and show it as an EO figure (S1 VV drop plus Hansen loss year on one cell) with a token. Cut the other three or mark them as field reports.
- **WIP framing.** none

### R1 The mutation test

Location: x 22-290, y 703-968 mm; matrix about 275 x 160 mm (about 4 % of board area). Verdict: **weak (EO weak; poster pass; truth weak; issues pass (#5 focal) / partial (#6); visual weak)**. Severity: High.

- **Evidence.** Best figure on the board: red/blue pattern reads at 1.5 m. Labels are small at print size (make_figures_v11.py TICK 14 pt: row labels 12 pt, column names and group names 9 pt, legend 10 pt). One record, one band. By our mapping it covers 10 of issue #6's 12 mutation types (missing: changed unit, changed checkpoint or embedding); issue #6's other asks (4 to 6 models, false-acceptance and false-rejection rates with intervals) are not met. Deterministic verifier, no model in the loop; genuine record accepted (false rejection 0 of 1 control). 'M15 is the one error emem's own reader made': research/repro/data/v8/prevalence_summary.json shows 162 of 200 sampled pre-fix records (81 %, Wilson 95 % 75-86 %) matched the neighbouring-pixel rule, across 19 bands and 164 scenes signed 14 May to 27 Sep.
- **Undersells.** It is an EO decision test: the neighbour pixel 10 m south reads NDVI 0.3016 against the genuine 0.4709, so a geolocation-class error flips an irrigation decision. That sentence would make R1 legible to the room.
- **Objection** (ML evaluation reviewer; statistician). This is a unit test of your own verifier on one record. Where are the agents and the error bars? And 'one error' hit most of your Sentinel-2 records for four months.
- **Spoken answer.** R1 isolates what each check stops, with no model to blame. R2 and R3 put models in the loop. M15 is one error class, a pixel-rounding rule, and the source re-read is how we found it.
- **Fix.** Make R1 the focal point (issue #5): larger, higher, column labels at 18 pt or more. Say 'one error class in emem's reader' instead of 'the one error'. Add a one-line EO reading of M15. Print the control acceptance.
- **WIP framing.** none

### R2 Agreement is not evidence

Location: x 307-570, y 725-862 mm. Verdict: **weak (EO fail; poster pass; truth pass; issues pass (#5 failure) / partial (#6); visual pass)**. Severity: Medium.

- **Evidence.** Clean bar chart, one message. Nothing says what quantity the agents were carrying. Prints Fisher p = 0.035 and calls the result descriptive in the same sentence. No confidence intervals. Two open models on one host (claims map caveat).
- **Undersells.** The handoff arm (prose 2/20, dense 8/20, BM25 20/20, emem bundle 20/20) is issue #5's 'controlled intervention', buried in the caption.
- **Objection** (LLM-agents researcher; statistician). BM25 ties you at 20 of 20. Why do I need emem?
- **Spoken answer.** BM25 finds the string when it is in the corpus. It cannot tell the receiver that the string is the signed one. R1 shows what that costs.
- **Fix.** Move R2 up as the Problem's figure. Name the carried quantity. Add Wilson intervals; keep either the p-value or 'descriptive', not both.
- **WIP framing.** none

### R3 A token helps only when checked

Location: x 307-570, y 862-968 mm. Verdict: **weak (EO fail; poster weak; truth weak; issues partial (#6); visual weak)**. Severity: Low.

- **Evidence.** n = 10 and 5, one vendor family. Token and full prose tie (10/10 each, p = 1). The re-hash and receipt check were done by the harness, not by model B (claims map); the table cell says so in small type. The carried value is the Keylong NDVI but the table does not say so.
- **Undersells.** The refusal is protocol-level: MCP returns a typed error and REST returns 409, so any client gets it without prompting.
- **Objection** (LLM-agents researcher). n of 5 and 10, one vendor. Token and prose tie. What did the token buy?
- **Spoken answer.** Refusal. Prose cannot be refused. A forged token was refused five times out of five, by the resolver, not by the model.
- **Fix.** Merge into R2 as its intervention arm. Say 'NDVI 0.4709'. Print intervals.
- **WIP framing.** 'rounded arm exploratory' is a method note, acceptable.

### R4 Memory through time

Location: x 576-819, y 725-968 mm. Verdict: **weak (EO weak; poster pass; truth pass; issues pass (#7 source change visible); visual pass)**. Severity: Medium.

- **Evidence.** Step chart with four as-of queries, clear. The May value came from the 90 m Copernicus DEM via Open-Meteo, inside a band named copdem30m.elevation_mean; from 11 Aug the 30 m COG pixel. That is a product and resolution change (GLO-90 to GLO-30), not only a provider change; a 2.93 m difference on terrain is expected, and neither value is wrong. Only record time varies (static band). 'Signed 7 times' means seven fact_cids for one value, which contradicts 'one observation, one signed record' in the Invention.
- **Undersells.** The contradiction detector scores severity per band kind and flags one attester answering from two upstreams; agents can record disagreement as signed disagrees_with edges without overwriting. A dynamic band would show both clocks.
- **Objection** (DEM / geodesy specialist). That is GLO-90 against GLO-30, not a provider change. Why did a 30 m band ever hold a 90 m value?
- **Spoken answer.** It should not have. The record says which product it read, so the substitution is visible and dated. That is the point of keeping both.
- **Fix.** Name the two products (Copernicus DEM GLO-90, GLO-30) and say the band-name mismatch was found this way. Keep the chart; it is the board's cleanest figure after R1.
- **WIP framing.** none

### Discussion

Location: x 22-510, y 968-1112 mm. Verdict: **weak (EO weak; poster weak; truth weak; issues pass on content (#5 must-remain-explicit) / fail on form; visual fail)**. Severity: Medium.

- **Evidence.** Six headed paragraphs, 325 words at 16 pt (1,939 characters): readable at arm's length only. 'Truth is re-read' equates fidelity to the archive with truth. 'The one such error in production' (see R1: one error class, 162 of 200 sampled). 'Every vector signed before still resolves and verifies §24' rests on a documentation row; the claims map says pre-retirement vector recall was not exercised end to end.
- **Undersells.** emem already states per record how far it can be checked (provenance class to tamper-evidence level). That is the confident form of 'where emem stops'.
- **Objection** (Cal/val scientist; independence sceptic). Your 'independent' second node is also you.
- **Spoken answer.** Yes. The checks need no operator: stock libraries and a published key. The binary is Apache-2.0, so anyone can run a node.
- **Fix.** Cut to three items of 25 words or fewer. Rewrite the 'next step' item as scope: 'One operator and one attester today; the checks need neither.' Replace 'truth is re-read' with 'fidelity is re-read; accuracy is the product's validation'.
- **WIP framing.** Heading 'Independent operation is the next step.' and 'Next: independent operators, provider-signed upstream identity and a multi-vendor agent study.'

### What a verified token guarantees (table)

Location: x 518-819, y 968-1062 mm. Verdict: **weak (EO weak; poster pass; truth weak; issues partial (#7); visual weak)**. Severity: High.

- **Evidence.** Seven rows, colour-coded, the most visitor-friendly format on the board, but 14.2 pt median. 'The place and time: guaranteed' means the claimed cell and tslot are bound, not that the pixel is geolocated correctly (M15 was a pixel error). 'The value's truth: tested, by re-reading the source' calls archive fidelity truth. No row for accuracy or uncertainty. The claims map says the upstream row is printed as 'upstream identity unverified'; the board prints 'named', so map and board disagree.
- **Undersells.** Issue #7's five-way split (source integrity, derivation integrity, observation identity, entity identity, semantic correctness) is already almost here. emem's substrate profile earth.satellite.v0 declares the lineage an EO reviewer expects (SAFE manifest, s2:processing_baseline, s2:datastrip_id, s1:orbit_source, sat:absolute_orbit, cdse.traceability.blake3), but only as a declaration: no code records it per fact.
- **Objection** (Cal/val scientist; provenance (W3C PROV) person). 'The value's truth: tested.' Re-reading the archive tests you, not the Earth.
- **Spoken answer.** Agreed. The re-read tests fidelity to the archive. Accuracy is the product's own validation; emem makes the value traceable to it.
- **Fix.** Rename rows to issue #7's five terms. 'Upstream file: named by URL and product id, not by a provider checksum.' Add 'accuracy: inherited from the product's validation'. Drop 'next'. Sync the claims map row.
- **WIP framing.** 'COG and pixel recorded; provider signature next'.

### Try it / evidence boxes

Location: x 518-819, y 1062-1160 mm. Verdict: **weak (EO weak; poster weak; truth pass; issues pass (#5: traces behind QR); visual weak)**. Severity: Low.

- **Evidence.** 13.5 pt text; install strings for five channels; three QR codes on the board (header to /verify, try box to the R1 folder, evidence box to the v10 track) and no cue which to scan. 'Under a second' holds: suite_seconds 0.0536 in mutation_matrix.json.
- **Undersells.** The live EO path a visitor can run in 30 seconds: emem.dev's 'Cite a real place, live' box (Uluru, Mount Fuji, Lake Erie, Rondonia) and ememdemo's 'world: <place>', which returns every layer at one cell with cross-checks.
- **Objection** (Visitor with a phone). Three QR codes. Which one do I scan?
- **Spoken answer.** The top one. Paste any token and your browser re-checks it.
- **Fix.** One visitor QR (cite a place, see every layer, check it) and one reviewer QR (repro). Install strings to the repo.
- **WIP framing.** none

### Conclusion

Location: x 22-510, y 1112-1162 mm. Verdict: **weak (EO weak; poster weak; truth weak; issues partial (#5); visual weak)**. Severity: Medium.

- **Evidence.** Three boxes at 16.4 pt in the lowest 50 mm of the board. (1) 'Checks it offline in under 2 ms': meta.full_verification_ms 1.207 includes the source re-read against a committed pixel window; a real receiver's re-read is a range request to the archive, so the offline claim holds for bytes, binding, signature, log and arithmetic only. (3) 'across ... retired encoders': no result tests encoders (R1 excludes embeddings).
- **Undersells.** No EO sentence. The board never concludes anything about Sentinel data.
- **Objection** (Anyone who reads only the conclusion). Under 2 ms including fetching the COG pixel?
- **Spoken answer.** No. Under 2 ms for hash, signature, log and arithmetic. Re-reading the pixel is one range request to the public archive.
- **Fix.** (1) 'checks the bytes, signature and log offline in under 2 ms'. (3) cite only R4. Add one EO sentence: every Sentinel number an agent cites traces to its pixel.
- **WIP framing.** none

### References / footer

Location: x 22-819, y 1162-1189 mm. Verdict: **weak (EO weak; poster weak; truth pass; issues n/a; visual weak)**. Severity: Low.

- **Evidence.** 156 words at 11.9 pt. 37 '§' citations on the board need the 'Track steps' legend to decode. References cite STAC, COG, openEO, PROV-O, C2PA, TESSERA and Earth Embeddings as Products; no CEOS-ARD / CARD4L, no Sentinel-2 L2A or Copernicus DEM product reference, although the board's only data are those two products.
- **Undersells.** n/a
- **Objection** (ESA programme reviewer). Your DOI is a June paper with a different design.
- **Spoken answer.** It is the first version. This board is whitepaper v3, in the repository. The DOI's title is the one struck through above.
- **Fix.** Add the Sentinel-2 L2A product specification and CEOS-ARD Surface Reflectance references if SCL or accuracy lines are added. Mint Zenodo v0.2 or drop 'Paper v0.1.0'. Drop the embeddings references if the embeddings leave the board.
- **WIP framing.** 'Paper v0.1.0; this board describes whitepaper v3.'

## EO breadth: declared versus wired (guard for any v12 claim)

| item | value |
|---|---|
| declared_source_schemes_live | 46 |
| encoder_schemes_minting_nothing | geotessera.v1, geotessera, model.prithvi_eo2_300m_tl, model.clay_v1_5, model.galileo_v1 |
| declared_but_no_reader_in_code | tropomi.s5p.ch4, tropomi.s5p.no2, dynamic_world.v1, openet.30m.daily |
| declared_but_wired_differently | {"viirs.dnb.monthly": "wired nightlights band is DMSP-OLS (nightlights.dmsp_ols_avg_dn); the fetcher documents why VIIRS DNB v22 was not used"} |
| wired_materializers_live | 116 |
| wired_families_live | cams 7, copdem30m 1, era5 7, esa_worldcover 1, firms 1, forest_change 3, gmrt 1, hansen 3, indices 19, jrc_gfc2020 1, jrc_tmf 4, koppen 1, marine 5, modis 7, nightlights 3, overture 4, population 1, power 7, protected 2, s2 13, sentinel1_raw 1, soilgrids 6, surface_water 4, temporal_diff 3, terraclimate 3, weather 8 |
| served_outside_auto_materializer | esa_cci_biomass (Rondonia world, with standard error), chirps (code references in emem-api-rest), ftw (emem-fetch/src/ftw.rs) |
| multi_sensor_per_cell | ememdemo 'world: <place>' stacks S2 reflectance and NDVI, S1 VV, Copernicus DEM and GMRT, met.no, ERA5, MODIS LST, CAMS PM2.5, Overture, an SCL-masked 120-day composite and every applicable algorithm, with cross-checks; /v1/worlds serves 4 signed 1,024-cell scenes (canyon 1,024 facts; carbon 3,733; interlaken 3,026; semantic 1,893, the last uses retired GeoTESSERA) |
| os_trace_protocol | 18 substrate profiles (earth.satellite.v0 active and the only drift anchor; 17 candidate incl. orbital.satellite.v1, admission os_trace_required, 8 required trace layers: syscall, scheduler, memory, sensor_bus, signal, energy, thermal, storage); 17 device platforms all candidate; 8 trace encodings incl. zephyr.ctf.v1; 4 conformance vectors; drift rule z = |d| / (3 sigma), score z/(1+z), consistent below 3 sigma, contradicted above 9 sigma (crates/emem-trace/src/drift.rs), 'wiring it to a recall of the anchor band ... is ingest-side work'; SAT-042 downlink example runs offline in Rust. Live /v1/devices: 1 operator-endorsed generic.linux-host (host.counters.v1), 1 trace, no platform-attested device. |

## Typography by region (from the PDF text layer)

| region | words | median pt | min pt | % chars < 18 pt | % monospace |
|---|---|---|---|---|---|
| Header | 64 | 15.3 | 12.8 | 64 | 30 |
| Problem | 54 | 17.6 | 13.9 | 87 | 0 |
| Invention | 72 | 17.6 | 13.9 | 69 | 0 |
| Hero figure | 417 | 12.8 | 9.9 | 100 | 14 |
| C1 | 67 | 16.4 | 14.0 | 91 | 50 |
| C2 | 76 | 16.4 | 14.0 | 95 | 49 |
| C3 | 83 | 17.4 | 14.0 | 92 | 31 |
| C4 | 106 | 16.4 | 14.0 | 93 | 59 |
| C5 | 90 | 16.4 | 14.0 | 94 | 69 |
| C6 | 88 | 16.4 | 14.0 | 93 | 40 |
| What agents do: tools strip | 164 | 14.7 | 12.5 | 98 | 13 |
| What agents do: four vignettes | 149 | 15.3 | 15.3 | 100 | 0 |
| R1 | 154 | 15.6 | 13.9 | 78 | 36 |
| R2 | 73 | 15.6 | 13.9 | 83 | 46 |
| R3 | 89 | 14.7 | 12.8 | 80 | 23 |
| R4 | 117 | 15.6 | 13.9 | 80 | 26 |
| Discussion | 325 | 16.0 | 16.0 | 99 | 14 |
| Conclusion | 72 | 16.4 | 16.4 | 98 | 0 |
| Guarantees table | 128 | 14.2 | 12.8 | 96 | 21 |
| Try it / evidence boxes | 42 | 13.5 | 13.5 | 100 | 50 |
| Footer | 156 | 11.9 | 11.9 | 100 | 0 |

Figures embedded as SVG images (R1, R2, R4) are not in the text layer; their label sizes come from `poster/make_figures_v11.py` (TICK 14 pt; R1 row labels 12 pt, column and group names 9 pt) at 1:1 placement.

## Memory encoding and provenance classes (needed if the embeddings strike-through stays)

bands-v0.json: 43 cube slots, 1792 dims. Slots by provenance class: {'model_output': 23, 'human_curated': 5, 'unclassified': 2, 'direct_sensor': 6, 'deterministic_index': 7}. Dims by class: {'model_output': 1110, 'human_curated': 130, 'unclassified': 162, 'direct_sensor': 35, 'deterministic_index': 355}. The four retired encoder slots (geotessera 128, clay_v1 384, prithvi_eo2 384, galileo 48) hold 944 of 1792 dims. attested_execution and estimator are defined in crates/emem-core/src/bands.rs but have no slot in bands-v0.json; attested_execution is the class of the device substrates (orbital.satellite.v1 and others). Tamper-evidence mapping (bands.rs tamper_evidence): direct_sensor and deterministic_index to recomputable_from_source; estimator to rerunnable_from_signed_inputs; attested_execution to verified_execution_trace; model_output to signed_model_checkpoint, downgraded per fact to attester_only when no checkpoint hash is bound; human_curated and unclassified to attester_only.

## Live checks made for this audit

| GET | UTC | status |
|---|---|---|
| /v1/facts/oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa | 2026-09-30T18:55:32Z | 200 |
| /v1/manifests | 2026-09-30T18:58:23Z | 200 |
| /v1/log/sth | 2026-09-30T18:58:23Z | 200 |
| /v1/capabilities | 2026-09-30T18:58:23Z | 200 |
| /v1/facts/exhq6lpsjbimxru33wbhvx2rrz72jeecnugpynsber2dxwgrfuea | 2026-09-30T18:58:23Z | 200 |
| /openapi.json | 2026-09-30T18:58:24Z | 200 |
| /v1/sources | 2026-09-30T18:58:36Z | 200 |
| /v1/substrates | 2026-09-30T18:58:47Z | 200 |
| /v1/devices | 2026-09-30T18:58:37Z | 200 |
| /v1/worlds | 2026-09-30T18:58:46Z | 200 |
| /v1/materializers?limit=200 | 2026-09-30T19:05:11Z | 200 |
| /v1/materializers?page=2&page_size=20 | 2026-09-30T19:05:22Z | 200 |
| /v1/materializers?page=3&page_size=20 | 2026-09-30T19:05:22Z | 200 |
| /v1/materializers?page=4&page_size=20 | 2026-09-30T19:05:22Z | 200 |
| /v1/materializers?page=5&page_size=20 | 2026-09-30T19:05:23Z | 200 |
| /v1/materializers?page=6&page_size=20 | 2026-09-30T19:05:23Z | 200 |

Key live values: hero fact `oj5ceccile...` resolves with confidence 0.95, no uncertainty, sources = two Azure COG paths under `S2A_MSIL2A_20260925T054251_N0513_R005_T43SFS_20260925T090015.SAFE`, derivation args including EPSG 32643, scene cloud 10.840102 %, SCL class 4, scenes tried 1, offset -1000. Venice absence `exhq6lps...` resolves as kind absence on Overture 2026-09-23.1. Manifests: 168 algorithms, 43 bands, 46 sources, 18 substrates, 17 device platforms, 8 trace encodings. Log tree size 2,570,200 at 18:58:23Z. /v1/capabilities: no extensions, no CUDA, no models loaded. /v1/devices: one operator-endorsed generic.linux-host, one trace. /v1/materializers: 116 wired bands. Zenodo 20706893: v0.1.0, 15 Jun 2026, only version.

## Scope and limits of this audit

- No POST calls were made to emem.dev (recall, trajectory and derive can materialise new facts); multi-sensor and as-of behaviour is verified from code, the live registries and ememdemo, not by a fresh live query.
- The count of recipes blocked by retired encoders (39) is the capability index figure from a band-prefix match and is provisional.
- Text sizes are from the PDF text layer; SVG figures placed as images were sized from their generator script, not measured on the render.
- Characters-per-line estimates for the header punchline assume an average advance of 0.55 em for IBM Plex Sans; they were not rendered.
