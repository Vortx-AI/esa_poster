# 12 · FINAL BRIEF for the v13 A0 board

Written 2026-10-01 by the lead scientific writer and art director. This file is the build specification for the final
board: every printed word, every figure, every number's source and status. The build team implements it as written.
Where the build team finds a conflict with a data file, the data file wins and the build fails until this brief is
corrected; nobody edits a number by hand.

Binding inputs read in full: `research/SHARED_STATE_EMEM_A0_MASTER.md`; reports `research/v13/00` to `11`;
`ecosystem_manifest.json`; `cost_measurements.json`; the issue table in `01_v12_state.md` §4 (#5 to #46);
`poster/src/poster.v12.html`, `poster/build_v12.py`, `poster/make_figures_v12.py`; `AGENTS.md`; the committed evidence in
`research/v13/evidence/`. Every number below was re-read from its file by the generator in Appendix I (which writes
`research/v13/12_claims_map.json`): 212 claim rows, 97 checked automatically against their files today, 0 failures.

Settlements obeyed (report 11): 10 of 10 noticed the date substitution; latencies are `ms_median`; tool-list tokens are
18,709 cl100k as served on 1 Oct; 597 m (WGS-84 geodesic); 14 of 141 / 28 of 155 pre-fix Keylong records (not printed);
receipts on 9 of 11 paths; Dify "community"; Bengaluru ran 10 paths (not printed); emem.dev runs commit 8e9b401; the
hair-salon case is emem commit 0edf574; the witnessed flag is never printed.

---

## A. Narrative and reading paths

### A.1 The narrative in one paragraph

Agents pass Earth-observation evidence to each other as words, and words keep their meaning while losing their
referent: a rounded value, another date, another pixel, another place. EMEM replaces the paraphrase with a reference: a
content-addressed observation record (cell, band, time, value, named source, derivation, signer) that the receiving
agent resolves, re-hashes, binds to its own question, checks against a signature and a public log, recomputes, and,
for open archives, re-reads at the source pixel. In a controlled suite of 16 corruptions of one signed Sentinel-2
record, a receiver handed prose or JSON acted on every corruption it could carry; a receiver that checked the
reference acted on none, and each check stopped a named class. The strongest finding is emem's own: its reader
signed the neighbouring pixel in 162 of 200 sampled records, and every check except the source re-read passed them.
The right record can hold the wrong pixel, the right trace the wrong place, and no reference can tell the entity
meant, the sensor's accuracy or the decision. The same failures sit in any agent pipeline over EO data; the record is
what makes each one checkable at a named layer, across 11 client paths and the agent hosts listed with their evidence.

### A.2 What a viewer gets at each distance (type sizes from report 06 §2.3; fluent at 0.2° x-height)

| distance | what is fluent | what the viewer takes away |
|---|---|---|
| **3 m** (hero 100 pt, spine numerals 64 pt, title 56 pt, sub-hero 32 pt, Keylong scene) | the hero sentence; the title; the spine's five lane names and the outcome numerals "15 / 15 · 15 / 15 · 13 / 16 · 0 / 16"; the real Keylong scene with the two outlined pixels; the vermillion block versus the blue staircase of the matrix; the hatched wall marked "no check reaches" | "Agents hand each other references, not paraphrases; with prose the corruption gets through, with a checked reference it does not; there is a limit." |
| **1 m** (panel headlines 32 to 44 pt, body and take lines 24 pt, labels 20 pt) | every panel's question, claim headline and mechanism line; the spine's check chain; the matrix rows by family and the "only check" rings; M15's two values and the 162 / 200 waffle; the ladder's six status words; the as-of line "15 Jun: 918.0 m"; the eight-answers number line; the failure ladder's rungs; the ecosystem bridge and its four status glyphs; the prior-art lanes | the mechanism, the experiment, the boundary, the failure classes, the ecosystem and the adjacent layers |
| **30 cm** (captions 17 pt, scope lines and references 14 pt) | the record's fields and the full token; scope lines (n, denominators, dates, test key, constructed threshold, sampling frame); the outside sources per failure; latency and token numbers; the R5 per-model strip when it exists; references; commit; QR captions | enough to reproduce or attack any number, and where to scan |

---

## B. Page composition

Sheet 841 × 1189 mm portrait, ISO A0. Bleed 3 mm on the header band only. Grid of report 06 §2.1: margins 20 mm, 12
columns of 58.5 mm with 9 mm gutters; column left edges col1 20.0, col2 87.5, col3 155.0, col4 222.5, col5 290.0,
col6 357.5, col7 425.0, col8 492.5, col9 560.0, col10 627.5, col11 695.0, col12 762.5; right edge 821.0. Three-column
zone 193.5 mm, six-column zone 396.0 mm, four-column zone 261.0 mm, eight-column zone 531.0 mm. Vertical module 3 mm;
panel gaps 10 mm; a 0.8 mm ink rule above every panel. y is measured from the top edge.

| block | cols | x (mm) | y (mm) | w × h (mm) | share of page | answers MASTER §28 question |
|---|---|---|---|---|---|---|
| Header text: title, hero, sub-hero, byline (navy, full bleed left) | 1 to 9 + bleed | −3 | 0 | 630.5 × 188 | 11.9 % | Q2 (what is new), Q4 (sub-hero boundary) |
| Header image: real Keylong scene + VIEW THE DEMO QR | 10 to 12 + bleed | 627.5 | 0 | 216.5 × 188 | 4.1 % | Q7 (reproduce), Q3 (the record followed) |
| 1 Spine: the handoff experiment | 1 to 12 | 20 | 196 | 801 × 190 | 15.2 % | Q1 (problem), Q3 (evidence), Q4 (wall) |
| 2 Eight answers to one question | 1 to 3 | 20 | 396 | 193.5 × 118 | 2.3 % | Q1 |
| 3 Our own errors name the checks (why EMEM) | 1 to 3 | 20 | 524 | 193.5 × 322 | 6.2 % | Q1, Q4 |
| Questions and hypotheses | 1 to 3 | 20 | 856 | 193.5 × 70 | 1.4 % | navigation to all |
| Threat model | 1 to 3 | 20 | 936 | 193.5 × 80 | 1.5 % | Q4 |
| 4 What is handed over (evidence object) | 4 to 9 | 222.5 | 396 | 396 × 156 | 6.2 % | Q2 |
| 5 Mutation matrix (hero quantitative figure) | 4 to 9 | 222.5 | 562 | 396 × 256 | 10.1 % | Q3 |
| 6 The right record, the wrong pixel | 4 to 9 | 222.5 | 828 | 396 × 188 | 7.4 % | Q3, Q4 |
| 7 Verification ladder L0 to L5 | 10 to 12 | 627.5 | 396 | 193.5 × 188 | 3.6 % | Q4 |
| 8 Same place, different time | 10 to 12 | 627.5 | 594 | 193.5 × 126 | 2.4 % | Q3 |
| 9 Rondônia screen | 10 to 12 | 627.5 | 730 | 193.5 × 106 | 2.1 % | Q3, Q4 |
| 10 Vectors are records too (title's embeddings) | 10 to 12 | 627.5 | 846 | 193.5 × 64 | 1.2 % | Q2 |
| 11 What it costs | 10 to 12 | 627.5 | 920 | 193.5 × 96 | 1.9 % | Q6 (cost of use) |
| 12 Ecosystem bridge | 1 to 8 | 20 | 1026 | 531 × 140 | 7.4 % | Q6 |
| 13 Prior-art layers | 9 to 12 | 560 | 1026 | 261 × 82 | 2.1 % | Q5 |
| Conclusion + READ THE METHODS QR | 9 to 12 | 560 | 1116 | 261 × 50 | 1.3 % | all; Q7 |
| Footer: references, commit, extension line | 1 to 12 | 20 | 1172 | 801 × 13 | 1.0 % | Q7 |

Main experiment (spine + matrix + wrong pixel) = 32.8 % of the page (v12.1: 11.0 %). Why-EMEM (panels 2 and 3) =
8.5 %. Implementation detail (formulas, schema bars, token-family table, SAT-042 figure) = 0 %. Content ends at
1166 mm; footer top at 1172 mm (6 mm clearance; gate needs 2 mm). Bottom margin 4 mm (footer only).

Header internals: title y 13 to 57 (two lines, 56 pt SemiBold, white); hero y 62 to 134 (two lines, 100 pt Bold,
white); sub-hero y 138 to 163 (two lines, 32 pt Medium, `emem-light` #7FB3E6); byline y 167 to 183 (two lines,
17 pt, white at 85 %). Header image: the signed-grid true colour, full 443 columns, cropped to 216.5 × 188 with row 212
inside; the cited cell in a white 6 mm box; VIEW THE DEMO QR on a white tile at x 734 to 821, y 13 to 100 (87 mm box =
70 mm symbol + 8.5 mm quiet zone), its label below on the tile to y 118; a 62 % black strip y 160 to 188 carries the
image caption.

Reading sequence (MASTER §30): header → spine (I understand the failure, I see the experiment) → panels 2 and 3 (the
failure is general) → panel 4 (the exact invention) → panels 5 and 6 (the experiment and its strongest finding) →
panel 7 and the threat model (what it proves and does not) → panels 8 to 11 (time, a real screen, vectors, cost) →
panel 12 (it works across runtimes) → panel 13 and the conclusion (where it sits; reproduce it).

### v13.1 change (2026-10-02): panels 9 to 11 replaced by two v12.1 panels; the drift block in the header

At the authors' request the v13 panels 9 (Rondônia screen), 10 (vectors) and 11 (what it costs) leave the face, and
four things from the v12.1 board come back: the drift idea block (header, sub-hero area), panel 9 "One address, every
product" (F13, 193.5 × 128 mm, drawn 1:1), panel 10 "One token family" (F14, 193.5 × 100 mm, drawn 1:1) and the agent-host
sentence in panel 12 (Claude Code plugin, ChatGPT app, each with its manifest status). The SAT-042 panel "How a satellite
could prove what it ran" (F15, 193.5 × 118 mm) was prepared but could not be placed: with its kicker (two lines at 24 pt),
its v12.1 headline (two lines at 32 pt), subtitle and caption it measures 206.9 mm, and the right column (639 mm) already
holds the ladder (202.1), the timeline (128.8) and the two panels above (174.6 and 124.7, total 639.2 with gaps);
the left (635.0) and centre (630.7) columns have no slack, and F13 to F15 set most text at the 14 pt floor, so they
cannot be scaled. Its markup stays in `poster/src/poster.v13.html` inside `<template id="p11-sat042-off">`; its text
is below under section C "v13.1 change". The footer's extension line (K.sat042) remains the face's SAT-042 statement.

Rows that change (everything else as in the table above; the column stacks by content with 3 mm gaps, as before):

| block | cols | x (mm) | y (mm) | w × h (mm) | share of page | answers MASTER §28 question |
|---|---|---|---|---|---|---|
| 9 One address, every product (F13) | 10 to 12 | 627.5 | 714.5 | 193.5 × 174.5 | 3.4 % | Q2, Q3 |
| 10 Token family (F14) | 10 to 12 | 627.5 | 892 | 193.5 × 124.5 | 2.4 % | Q2 |

Header internals in v13.1: title y 9 to 51; hero y 54 to 123; sub-hero y 126 to 151; drift block y 152.5 to 167 (two
lines, 17 pt, white at 92 %, formula in Medium `emem-light`, subscripts 14.2 pt); byline y 171 to 186.

### v13.2 change (2026-10-02): SAT-042 placed as a compact strip; the ladder drawn compact

At the authors' decision the SAT-042 panel goes on the face after all, as panel 11 of the right column, below the token
family: kicker `Extending verification from observations to execution` (24 pt, two lines), the v12.1 headline `How a
satellite could prove what it ran` (28 pt, one line; 32 pt needs two), the subtitle (17 pt, two lines), the strip F15b
(193.5 × 60 mm: the seven harness steps as one row of chips with their verdict words, the 8-layer trace in one row with
the rewritten segment marked, the three drift-anchor scores on a number line) and one 14 pt scope line. The room comes
from panel 7: F8 is drawn compact at 193.5 × 60 mm (`f8_ladder.py --height 60`; six rungs, one evidence line each at
14 pt, the status words and the two-sided hatch kept, the grey "still trusted" lines and the 409 dropped), and the panel's
mechanism line and caption leave (the rungs print the counts; the threat model and the conclusion carry the entity,
sensor and decision scope). The column's arithmetic allowed nothing else: panels 8 to 10 keep 428 mm with their figures,
so panel 7 and panel 11 share 199 mm. The strip is 60 mm, not the 70 first planned, and the ladder 60 mm, not about 110:
the kicker alone needs 18 mm, and every other line of panel 11 sits at its minimum tier. The full F15 stays drawn in
`poster/fig/v13/` for the methods site. Rows (rendered rectangles, 2026-10-02; the column still stacks by content with
3 mm gaps plus 0.5 mm of distributed slack):

| block | cols | x (mm) | y (mm) | w × h (mm) | share of page | answers MASTER §28 question |
|---|---|---|---|---|---|---|
| 7 Verification ladder L0 to L5 (F8 compact) | 10 to 12 | 627.5 | 377.5 | 193.5 × 84.7 | 1.6 % | Q4 |
| 8 Same place, different time | 10 to 12 | 627.5 | 465.7 | 193.5 × 128.8 | 2.5 % | Q3 |
| 9 One address, every product (F13) | 10 to 12 | 627.5 | 598 | 193.5 × 174.2 | 3.4 % | Q2, Q3 |
| 10 Token family (F14) | 10 to 12 | 627.5 | 775.7 | 193.5 × 124.7 | 2.4 % | Q2 |
| 11 SAT-042 strip (F15b) | 10 to 12 | 627.5 | 903.9 | 193.5 × 112.6 | 2.2 % | Q2 (extension to execution) |

---

## C. The complete printed text

Conventions. Lines beginning `>` are running text and count toward the word cap. `[R5]` marks the replacement line
used only when R5 results exist; the fallback line is the default. Figure-internal labels are given in tables or
lists and are figure text (gated like prose, counted separately). Type: Plex Sans (complete 3.005 faces in
`poster/fonts/plex-full/`); tokens and commands in Plex Mono. Minus is U+2212. "15 / 15" with thin spaces in figures,
"15 of 15" in prose. No em dashes; en dashes never (write "to"); no tell words; no "first", "only" (except where the
claims map allowlists it), "truth", "guarantee", "proves", "trustless", "the satellite decides"; "verified" never
without its layer.

Word counts (computed from this section by the counter in Appendix I): running text **823 words** containing a letter
(869 tokens if bare numerals and panel arrows are counted; 807 / 853 before the 1 Oct review fixes 9, 13 and 16), including every kicker, headline, mechanism line, caption,
RQ, hypothesis and the conclusion; cap about 800. Figure, legend, scope and footer text: about 1,740 tokens, all at the
30 cm tier and all gated like prose. The title, the token, QR payloads and references are excluded from the cap.

### Header

Title (56 pt SemiBold, white, two lines; break after "Protocol"):

`EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings`

Hero (100 pt Bold, white, two lines; break after "evidence"):

> Agents hand each other evidence references, not paraphrases.

Sub-hero (32 pt Medium, #7FB3E6):

> The receiver resolves the reference, re-hashes the record, re-reads the source. A signature fixes the record's bytes, not the measurement.

Byline (17 pt, two lines):

`Jaya Kumari · Avijeet Singh · Vortx AI · avijeet@vortx.ai`
`Agentic AI for Earth Observation · BIFOLD and ESA Φ-lab · Berlin · Poster Session 1 · 19 Oct 2026 · emem.dev · github.com/Vortx-AI/emem (Apache-2.0)`

No DOI unless the Zenodo record is corrected first (open item H.6).

Image strip (17 pt / 14 pt, white on 62 % black):

`The record this board follows: NDVI 0.4709 · Sentinel-2A L2A · Keylong, Lahaul, India · 25 Sep 2026`
`true colour B04/B03/B02 from signed 10 m grids; linear 1 to 99 % stretch, γ 1/1.35`

QR tile (white): `VIEW THE DEMO` (28 pt Mono Bold) / `Your phone is Agent B: a paraphrase passes unchecked; three corruptions are refused.` (17 pt)

### 1 · Spine (801 × 190 mm)

Kicker (24 pt, `ink2`):

> What survives an agent handoff?

Headline (44 pt SemiBold):

> Handed prose, B acted on 15 of 15 corruptions; handed a reference it checks, on 0 of 16.

> [R5] Handed prose, agents acted on {R5.A.pooled.false_accept} corruptions; handed a reference they check, on {R5.E.pooled.false_accept}.

Mechanism line (24 pt):

> A relay or a faulty signer corrupts one signed NDVI record in one of 16 ways; Agent B resolves, re-hashes, binds, checks, recomputes and re-reads.

Agent-level strip (24 pt, bottom-left of the spine, x 20 to 400):

> With a model as B and a forged cell, Claude Haiku 4.5 declined 5 of 5; Qwen2.5-3B dropped the cell from all 24 calls and acted 5 of 5: a reference protects only a receiver that keeps it whole and obeys a refusal.

Figure text (see figure F2): lane names `prose` · `JSON` · `retrieved text (RAG)` [R5 only] · `opaque id` · `EMEM reference`;
column heads `Agent A cites` · `handoff` · `relay` · `Agent B` · `B acted on corrupted evidence` · `no check reaches`;
relay bar `relay or faulty signer, one of 16: value · cell · time · band · source · derivation · stale state · signature · pixel`;
Agent A `Agent A reads NDVI 0.4709 and cites it`; Agent B per lane `reads the text` · `reads the fields` ·
`retrieves a passage` [R5] · `fetches the sender's record` · check chain chips `resolve L0 · re-hash L0 · bind L1 · signature L0 · log L0 · recompute L2 · re-read L3`;
wall `the entity meant (M17) · sensor accuracy · the decision`.
Scope line (14 pt, x 410 to 801, bottom): `Deterministic receiver written by us, no model; one record, one band, one run; signer-error rows use a test key; the 0.4705 threshold is set so that rounding flips it. M7, a miscopied token, has no prose form.`
[R5] scope line: `{R5.models}; {R5.dates}; n per lane from the results file; adversary simulated; threshold constructed.`
QR under the wall: `TRY A TOKEN` / `Resolve the Keylong token on emem.dev, then paste your own.`

### 2 · Eight answers; one is right (193.5 × 118 mm)

> What can one NDVI become between agents?

Headline (32 pt SemiBold):

> Eight answers; one is right

> One question, NDVI at the Keylong field on 25 Sep 2026; real records, archive pixels and handling rules give eight values.

Caption (17 pt):

> Six cross the irrigation line, one is impossible, one is right; each wrong value needs a different check.

Figure text (F3): dot labels `0.4709 signed record` · `0.47 rounded in prose` · `0.4370 other satellite, same day` ·
`0.4237 30 Sep record handed as 25 Sep` · `0.3016 neighbour pixel` · `0.2966 offset left out` ·
`0.2824 town point 597 m away (30 Sep)` · `1.1427 offset applied twice`; check chips `resolve L0` · `scene id L1` · `date L1` ·
`re-read pixel L3` · `catalogue offset L3` · `asked coordinates L1` · `range L2`; rule line `test rule: irrigate if NDVI ≤ 0.4705`;
legend `● a signed record or an archive read · ○ the reader rule or arithmetic applied to real pixel values`.

### 3 · Our own errors name the checks (193.5 × 322 mm)

> Why does an agent handoff need a record?

Headline (32 pt SemiBold):

> Our own errors name the checks

> Each error happened inside emem, a system built for evidence, or in our tests; each has a published precedent.

Caption (17 pt):

> Signatures prevented none; the record made each checkable at a named layer, except the top row.

Header strip (14 pt, under the mechanism line): `"errors may propagate silently across steps" (Munir et al. 2026, arXiv 2604.24919)`

Figure text (F4), eight rungs bottom to top, each: what happened · same class elsewhere (14 pt) · consequence (20 pt Bold `harm-text`) · catching check chip · status tag:

| rung | what happened | same class elsewhere | consequence | check | status |
|---|---|---|---|---|---|
| 1 Lost in the handoff | `0.47 for 0.4709` | `Perez et al., ICLR 2025: LLM transmission chains drift` | `5 of 5 receivers irrigated` | `resolve the reference · L0` | `test rule` |
| 2 Wrong date | `asked 23 Sep, served 25 Sep` | `STAC item search defines no default order` | `10 of 10 agents saw one scene twice;` / `3 said no 23 Sep scene existed` (line break after "twice;") | `bind the date · L1` | `open` |
| 3 Wrong place | `coordinates given, town point answered` | `GDAL 3 follows CRS axis order (RFC 73)` | `597 m; NDVI 0.28 for the field's 0.42` | `asked coordinates · L1` | `fix unconfirmed` |
| 4 Wrong version | `918.0 m, then 915.07 m, one band name` | `GFC2020 V3 cut forest cover by more than 20 % in the Cerrado` | `an earlier citation looks wrong` | `source + as-of · L1` | `both kept` |
| 5 Wrong scale or offset | `WorldPop signed per pixel, not per km²: 1.77× low` | `Element84 items say "offset applied" and "apply −0.1"` | `one pixel: 0.4709, 0.2966, 1.1427 under three offset rules` | `recompute · L2 · catalogue · L3` | `fixed` |
| 6 Missing data signed as 0 | `off-tile pixels signed as 0` | `Hansen lossyear 0 means no loss` | `a forest-loss screen passes` | `re-read · L3` | `fixed` |
| 7 Wrong pixel, signed | `the reader rounded the pixel index` | `GDAL RFC 33: half-pixel shift; one-pixel misregistration: error > 50 % of NDVI differences (Townshend 1992)` | `162 of 200 sampled records` | `re-read only · L3` | `fixed 28 Sep 2026` |
| 8 Wrong thing | `"this image" resolved to a hair salon in Ontario` | `toponym ambiguity (Gritta et al. 2018)` | `receipt, Merkle proof and state chain all valid` | `none · L4` (hatched) | `fixed 30 Sep 2026` |

Scope line (14 pt, `ink2`, horizontal, under the caption; review fix 18 moved it here from the rotated side rail of F4): `A check protects only if it runs: emem's resolver once reported a cell match it never tested; one framework adapter returns a refusal as plain text; MAST: no or incomplete verification (FM-3.2).`

### Questions (193.5 × 70 mm)

Headline (32 pt SemiBold):

> We ask four questions

> RQ1 Can a receiver detect corruption without trusting the sender? → 1, 5
> RQ2 Which corruption classes can it detect? → 5
> RQ3 Does a reference beat prose, JSON or an opaque id? → 1
> RQ4 What stays unverifiable with the reference intact? → 6, 7
> H1 A checked reference refuses corruptions that keep the stated value. H2 Only a source re-read catches a signer's wrong pixel. H3 A historical reference keeps the cited state.

> [R5] RQ3 Does a reference beat prose, JSON, retrieval or an opaque id? → 1, 5

Arrows are the panel numbers; set RQ ids in Bold `emem`.

### Threat model (193.5 × 80 mm)

Headline (32 pt SemiBold):

> A relay can rewrite, not sign

> A relay can rewrite what it carries but cannot sign under the pinned key or match an address; a signer's misread pixel is caught only by a re-read. Out of scope: a compromised key, a wrong sensor, the entity meant, the decision.

Figure text (D1): `A` → relay box `rewrites value, cell, date, source, record, reference; replays old records` → `B`; two pins outside the relay `pinned key (DNS TXT, did.json, JWKS)` · `open archive (COG)`; three stripes `cryptographic: the exact record bytes · CHECKABLE` · `source: which file was read · PARTIAL` · `measurement: sensor and product · INHERITED`; 14 pt `All keys today are one operator's.`

### 4 · The address names the record, not the pixel (396 × 156 mm)

> What exactly is handed over?

Headline (40 pt SemiBold):

> The address names the record, not the pixel.

> The receiver gets 84 characters; everything else it fetches and checks.

Caption (17 pt):

> The address is the BLAKE3 hash of the 1,115-byte record, which names its source files and the point it read but holds no hash of them; a batch signature covers such addresses. Re-signing makes a new record: one Bengaluru value has seven.

Figure text (F5): box heads `SOURCE FILES · named, not hashed` · `RECORD · 1,115 B` · `ADDRESS · BLAKE3` · `ATTESTATION + LOG`;
source box `B04 + B08 COGs · Planetary Computer · 277.9 + 281.9 MB · pixel row 9443, col 9098 · DN 1900, 3502`;
arrow `read the containing pixel`; record field list (two columns, Mono 15 pt, actual values, see F5); tags `named` (on source fields) · `recomputable` (on value) · `bound` (on cell, band, tslot);
address `oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` `changes if one bit of the record changes`;
attestation `Ed25519 over a batch root · key 777er3yi… · Merkle log, RFC 6962 style, BLAKE3`;
token line (Mono 18 pt) `emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` with `handed over: 84 characters, 46 tokens (cl100k)`.
QR: `INSPECT THE RECORD` / `The 1,115 bytes behind the main example, decoded.`

### 5 · Each of five checks alone stops a corruption (396 × 256 mm)

> Which check stops which corruption?

Headline (40 pt SemiBold):

> Each of five checks alone stops a corruption.

Caption (17 pt):

> Binding stops cell, time and band swaps; the signature, re-hashed forgeries; the log, a version shown only to B; recomputing, the signer's arithmetic; only the source re-read, the signer's wrong pixel. The entity meant passes every check.

Figure text (F6): column heads `prose` · `JSON` · `RAG` [R5] · `opaque id` · `EMEM, full check` · `first check that refuses` · `flips the decision`;
family labels `value` · `cell` · `time` · `band` · `source` · `derivation` · `stale / current` · `signature / id` · `source pixel` · `entity (out of scope)`;
check legend `D hash L0 · E binding L1 · F signature L0 · G log L0 · H recompute L2 · I re-read L3 · ○ the only check that stops it`;
totals row `B acts on corrupted evidence` `15 / 15 · 15 / 15 · 13 / 16 · 0 / 16`;
control row `nothing altered: accepted everywhere, never refused`;
scope (14 pt): `One signed Keylong NDVI record, one band, one run; deterministic receiver; rows M14 to M16 signed with a test key; the re-read compares with the committed 25 Sep window. Three further signer errors (offset, same-day scene, unit) pass checks D to I; metadata checks catch them.`
[R5] scope: `Bars: agents' false acceptance, k of n per cell (planned 15: 5 runs × 3 Claude models); squares: the deterministic ceiling. {R5.models}, {R5.dates}.`
QR: `RE-RUN THE TEST` / `Data and scripts behind this board's numbers, with one re-run command.`

### 6 · The right record, the wrong pixel (396 × 188 mm)

> Can a valid signature carry a wrong measurement?

Headline (40 pt SemiBold):

> The right record, the wrong pixel.

Claim line (24 pt SemiBold):

> A valid signature can faithfully preserve a wrong measurement when the reader itself selected the wrong source pixel.

Caption (17 pt):

> emem's old reader rounded the pixel index and signed what it read. One such record still resolves: 0.3444 signed, 0.4860 in its own pixel.

Figure text (F7): (a) `Keylong, Lahaul · Sentinel-2A L2A · 25 Sep 2026` `1 km`; (b) per-pixel NDVI values (2 decimals); `named pixel` · `pixel 10 m south`;
(c) `test rule: irrigate if NDVI ≤ 0.4705` · `0.4709 → hold` (30 pt ink) · `0.3016 → irrigate` (30 pt `harm`); chips `hash · binding · signature · log · recompute: pass the wrong value` · `re-read: refuses`;
waffle `162 of 200 sampled pre-fix records carry a neighbour's values (Wilson 95 %: 75 to 86 %)`; `spectral-index error where the rules differ: median 0.027, p90 0.113, max 0.301 (n 121)` (the 121 are the index-band records of the 162; 41 reflectance-band records are excluded);
the real record line (17 pt, Mono id) `kxjvfwpa… · 23 Sep 2026 · signed 0.3444 · its containing pixel 0.4860`;
scope (14 pt): `Sample: 200 pre-fix Sentinel-2 records cited in emem.dev's public channel, one per cell, seeded; 192 Element84, 8 Planetary Computer. After the fix, 0 of 54 (Planetary Computer, two days). On a 100-point Rondônia grid the old rule changed 7 loss years and no EUDR flag. (b) applies the old rule to the 25 Sep scene.`

### 7 · Checks stop at the source (193.5 × 188 mm)

> What does a checked reference establish?

Headline (32 pt SemiBold):

> Checks stop at the source

> Each rung names what it still trusts.

Caption (17 pt):

> Of 780 records pulled on 30 Sep 2026, 780 pass L0 and L1; the 266 with a recipe all recompute at L2; their source files are named, not hashed. No reference establishes the entity, the sensor's accuracy or the decision.

Figure text (F8), rungs bottom to top: `L0 record bytes · CHECKABLE · 780 of 780: hash, signature, log · still trusted: the key is emem.dev's` /
`L1 identity · CHECKABLE · cell and band bound in 780 of 780; a relabelled token returns 409 · still trusted: your own question` /
`L2 derivation · RECOMPUTABLE · 266 of 780 carry a recipe; all 266 recompute · still trusted: the convention the signer chose` /
`L3 source · PARTIAL · named, not hashed: 0 of 215 Keylong sources carry a hash; open archives can be re-read · still trusted: that the archive file is the product` /
`L4 entity · OUT OF SCOPE · M17 passes every check; "this image" became a hair salon` /
`L5 physical truth, decision · INHERITED / OUT OF SCOPE · GFC2020 V3 forest commission error 13.1 %`.

### 8 · Memory keeps what was cited (193.5 × 126 mm)

> What did the agent know on 15 Jun?

Headline (32 pt SemiBold):

> Memory keeps what was cited

Caption (17 pt):

> Asked about 15 Jun, the memory returns 918.0 m; the August record does not overwrite it, and the receiver checks the cited state by its address; at Keylong the newer record would flip the decision.

Figure text (F9): `Bengaluru · one cell · copdem30m.elevation_mean`; record 1 `918.0 m · signed 28 May · 90 m DEM via Open-Meteo`; record 2 `915.07 m · first signed 11 Aug · 30 m DEM · re-signed 7 times`; as-of probes `1 May: none` · `15 Jun: 918.0 m` · `12 Aug: 915.07 m` · `29 Sep: 915.07 m`; emphasised `what did agent A know on 15 Jun? → 918.0 m`;
Keylong strip `cited 25 Sep: 0.4709 → hold` · `30 Sep: 0.4237 → irrigate` · `the cited reference still re-hashes (1 Oct 2026)`; 14 pt `as-of compares signing times (UTC seconds); here the provider changed, not the ground`.

### 9 · An auditor re-runs each input (193.5 × 106 mm)

> Can a screen be re-checked input by input?

Headline (32 pt SemiBold):

> An auditor re-runs each input

Mandatory line (17 pt Bold):

> Point samples, not parcel polygons; not a regulatory determination.

Caption (17 pt):

> 100 point samples 740 m apart, 600 signed records, each re-hashed; TMF agrees on 1 of 3 flags.

Figure text (D2): legend `forest 2020 (GFC2020) + loss after 2020 (Hansen): 3` · `forest, no later loss: 33` · `cleared 2001 to 2020: 20` · `not forest: 43` · `maps disagree: 1`;
cell A card `Hansen loss 2023 · tree cover 2000 100 % · GFC2020 V4 forest · TMF 2023 · CCI 208 t/ha` each with an 8-character address prefix, and `five of its six signed inputs` (NDVI is the sixth, not on the card).

### 10 · Vectors are records too (193.5 × 64 mm)

> Where are the foundation-model embeddings?

Headline (32 pt SemiBold):

> Vectors are records too

> Derived representations are addressable too: this cell's Prithvi-EO-2.0 vector names its checkpoint digest inside the hashed record; the TESSERA vector, only a path and year. Both still resolve; emem.dev lists its encoders as retired.

Figure text (D4): card 1 `prithvi_eo2 · 1,024 values · checkpoint 2ad1775f… (hashed)`; card 2 `geotessera · 128 values · …/npy/v1/2024/… (no checkpoint)`.

### 11 · The source re-read costs most (193.5 × 96 mm)

> What does checking cost?

Headline (32 pt SemiBold):

> The source re-read costs most

> A record check takes 0.33 ms of CPU; a pixel re-read moves 1.18 MB in about 7 s, and only it refuses the wrong pixel. A reference costs 46 tokens, the value 8; a model receiver read 2.1× the tokens prose costs, same decisions.

Figure text (F10): time strip rows `re-hash 1.6 µs` · `all offline checks 0.33 ms` · `offline proof bundle 0.57 ms (4,906 B)` · `resolve 40 ms warm, 154 ms cold` · `source re-read about 7 s, 1.18 MB (0.058 % of the scene)`; token strip `value 8` · `reference 46` · `record as JSON 562` · `18-tool MCP list 18,709 (1 Oct)`; scope (14 pt) `One 2.8 GHz Xeon core; network through our TLS proxy; tokens cl100k; Claude Haiku 4.5 receiver, 10 runs per arm, +1.75 s.`

### 12 · One evidence protocol, multiple agent runtimes (531 × 140 mm)

Headline (40 pt SemiBold):

> One evidence protocol, multiple agent runtimes.

Caption (17 pt):

> One reference resolved to one address and one value through 11 client paths, with receipt signatures checked on 9 (30 Sep 2026). A listing is not an integration. Not run by us: ChatGPT, claude.ai, Dify, VS Code, Cursor.

Figure text (F11): bridge nodes `EMEM signed record · emem:fact:…` → `MCP · A2A` → `agent host or client` → `next agent: resolves, re-hashes, re-reads`;
groups (names in poster type; glyph from the manifest status):
`AGENT HOSTS` ● Claude Code ● Claude Code plugin ○ Claude.ai custom connector ● Dify Marketplace plugin (community)
`INTEROPERABILITY` ○ Model Context Protocol (MCP) · emem.dev/mcp ○ Agent2Agent (A2A) · signed agent card
`DISCOVERY` ▢ Official MCP Registry · io.github.Vortx-AI/emem ▢ GitHub MCP Registry ● github.com/Vortx-AI/emem ▢ Glama
`DEVELOPER` ● Gemini CLI ○ Visual Studio Code ○ Cursor ● pip install ememdev ● npm i @vortxai/emem ○ REST / OpenAPI 3.1 ● ghcr.io/vortx-ai/emem
`FRAMEWORKS` △ LlamaIndex △ AutoGen △ CrewAI △ Mastra (+ △ LangChain (MCP adapters), △ Agno only if their conditions in the claims map are met; + ● ChatGPT (@emem) only with the screenshot)
legend `● LIVE: connected or published · ○ PROTOCOL: open surface, client not run by us · ▢ REGISTRY: a listing · △ EXAMPLE: repo code, tool list checked · checked 30 Sep 2026`;
dot plot rows (median ms, 30 Sep 2026) `official MCP Python SDK 56.3` · `official MCP TypeScript SDK 58.3` · `TypeScript SDK 58.6` · `Python SDK 207.7` · `raw REST 223.5` · `raw MCP 223.7` · `A2A message/send 226.3` · `independent BLAKE3 + CBOR reader 235.6` · `LlamaIndex 300.8` · `LangChain MCP adapters 1,176.8`; axis `ms, log scale; one address, one value on every path`.
QR: `DISCOVER INTEGRATIONS` / `Where EMEM runs today, each surface labelled by evidence.`

### 13 · EMEM relies on these layers (261 × 82 mm)

Headline (32 pt SemiBold):

> EMEM relies on these layers

> A STAC item identifies a file; EMEM identifies the observation an agent cited, for the next agent to re-check. GeoGuard judges the claim; EMEM fixes the evidence it cites.

Figure text (F12): lanes top to bottom `JUDGE · GeoGuard · a claim in text` · `CARRY · MCP, A2A · a tool call, an agent card` · `RETRIEVE · RAG · a text chunk` · `SIGN FILES · C2PA, CDSE Traceability · a file` · `RECORD LINEAGE · W3C PROV · entity, activity, agent` · `RUN · openEO · a process graph` · `FIND · STAC · an asset (file)`; thread label `EMEM: is this the observation the sender cited?`; footnote (14 pt) `Same pattern in software supply chains: Sigstore, RFC 9162, SCITT (RFC 9943). Closest agent memory: ARC (arXiv 2607.25066).`

### Conclusion (261 × 50 mm; issue #38)

> A signed observation reference left the receiver acting on none of the 16 corruptions in our suite; a source re-read exposes a wrong pixel emem signed in production; entity, sensor and decision stay beyond its checks.

> [R5] … in our suite, and agents with a checked reference acted on {R5.E.pooled.false_accept}; entity, sensor and decision stay beyond its checks.

QR: `READ THE METHODS` / `Definitions, denominators, models, and what our own tools generated.` Under the QR (14 pt Mono): `vortx-ai.github.io/esa_poster`.

### Footer (14 pt, two lines, `ink2`)

Line 1 (method): `Mechanisms read from emem's code; where its docs differ, the code is printed. emem.dev at commit 8e9b401; measurements 29 Sep to 1 Oct 2026. Extending verification to execution: reference harness, no spacecraft enrolled.`
Line 2 (references): `Sentinel-2 Products Specification (ESA) · Copernicus DEM GLO-30/90 · Hansen et al. 2013, GFC v1.13 · JRC GFC2020 V3/V4, TMF · ESA CCI Biomass v7 · Reg. (EU) 2023/1115 · BLAKE3 · RFC 8032 · RFC 6962/9162 · STAC 1.1 · openEO 1.3 · W3C PROV-DM · C2PA 2.4 · MCP 2025-11-25 · A2A 1.0 · Perez et al., ICLR 2025 · Munir et al. 2026 (2604.24919) · Cemri et al. 2025, MAST (2503.13657) · Dang et al. 2026, ARC (2607.25066) · Townshend et al. 1992 · GeoGuard (NASA-IMPACT) · Prithvi-EO-2.0 · TESSERA (2506.20380)`

Not on the face (move to `/methods/`): the token-family table, the formulas, SAT-042's figure, the Berlin stack, the
encoding bar, the compaction study, version history, defect numbers, scorecards, traffic counts, the witnessed flag,
star and install counts, the 209-record count at the Keylong address.

### v13.1 change (2026-10-02)

The sections below replace "9 · An auditor re-runs each input", "10 · Vectors are records too", "11 · The source
re-read costs most" and the panel 12 caption; the header gains the drift block. Counted by the Appendix I counter like
every other section.

### Drift (v13.1)

Header, sub-hero area (17 pt, two lines, white at 92 %; "Names move" and "Values move" in SemiBold; the formula in Medium
`emem-light` with 14.2 pt subscripts):

> Names move: “the north field” drifts; a 64-bit cell id of about 10 m does not. Values move: 0.4709 becomes “about 0.47”; a fact_cid breaks if one bit changes.
> Δz = Δenv + Δsensor + Δgeo + Δencoder + ε: world, instrument, misregistration, model, noise; change at one pinned address.

### 9 · One address, every product (193.5 × 174.5 mm)

> Which products does one address reach?

Headline (32 pt SemiBold; "every" allowlisted against BE.stack):

> One address, every product

Subtitle (17 pt, the v12.1 subtitle verbatim):

> One 10 m cell in central Berlin, read live on 30 Sep 2026 from each product's native grid (10 m to about 11 km): 15 products, 16 signed facts, 4 of them signed absences.

Figure text (F13): see `research/v13/12_claims_map_additions_F13-15.json` (rows A13.*).

### 10 · One token family (193.5 × 124.5 mm)

> What else can a token name?

Headline (32 pt SemiBold):

> One token family

Figure text (F14): rows A14.* of the same file.

### 12 · One evidence protocol, multiple agent runtimes (v13.1)

Headline unchanged. Caption (17 pt; the agent-host sentence is new, each host with its manifest status):

> One evidence protocol, multiple agent runtimes.

> One reference resolved to one address and one value through 11 client paths, with receipt signatures checked on 9 (30 Sep 2026). Agent hosts: emem is a Claude Code plugin (marketplace emem@emem 2.4.2, 19 skills, 3,672 tokens a session: LIVE, installed by us) and a ChatGPT app (@emem: listed by its publisher, not re-checked by us). A listing is not an integration. Not run by us: ChatGPT, claude.ai, Dify, VS Code, Cursor.

### 11 · How a satellite could prove what it ran (prepared, not placed; not counted)

Kicker `Extending verification from observations to execution`; headline `How a satellite could prove what it ran`;
subtitle `SAT-042 is a scripted pass in emem's test harness, not a spacecraft; run on 30 Sep 2026.`; figure F15;
caption `A write with no trace and a fact the trace did not emit are refused; 3 facts are admitted under one trace; a
rewritten segment is named. Reference harness, no spacecraft enrolled; the gate binds the value digest only.`
Allowlist it needs if placed: kicker (verif-without-layer, K.sat042), headline (prove, SAT.run), caption (only, SAT.gate).

### v13.2 change (2026-10-02)

The two sections below replace "7 · Checks stop at the source" and place "11 · How a satellite could prove what it ran";
everything else stands. Counted by the Appendix I counter like every other section.

### 7 · Checks stop at the source (v13.2) (193.5 × 84.7 mm)

> What does a checked reference establish?

Headline (32 pt SemiBold):

> Checks stop at the source

No mechanism line and no caption (v13.2): the compact F8 prints the counts, the threat model and the conclusion carry the
entity, sensor and decision scope. Figure text (F8 compact, 193.5 × 60 mm), rungs bottom to top: `L0 record bytes
CHECKABLE · 780 of 780: hash, signature, log` / `L1 identity CHECKABLE · cell and band bound in 780 of 780` /
`L2 derivation RECOMPUTABLE · 266 of 780 recompute from a recipe` / `L3 source PARTIAL · named, not hashed: 0 of 215
hashed` / `L4 entity OUT OF SCOPE · M17 passes every check; "this image" became a hair salon` / `L5 physical truth,
decision · INHERITED / OUT OF SCOPE · GFC2020 V3 forest commission error 13.1 %`.

### 11 · How a satellite could prove what it ran (v13.2) (193.5 × 112.6 mm)

Kicker (24 pt, two lines; "verification" allowlisted against K.sat042):

> Extending verification from observations to execution

Headline (28 pt SemiBold, one line; "prove" allowlisted against SAT.run):

> How a satellite could prove what it ran

Subtitle (17 pt):

> SAT-042 is a scripted pass in emem's test harness, not a spacecraft; run on 30 Sep 2026.

Figure F15b (193.5 × 60 mm): chips `Enrol ENROLLED` · `Write, no trace REFUSED` · `Capture the pass SIGNED` · `Smuggle a
4th fact REFUSED` · `Honest batch ADMITTED` · `Score vs anchor SCORED` · `Rewrite one log CAUGHT`; trace row `8 trace
layers, each log digest chained;` · `seq 2 rewritten after signing: broken at seq 3` · `syscall seq 0` to `storage seq 7`;
number line `drift anchor 0.6402 ± 0.02 (1σ): scored after admission, not a gate` · bands `consistent` `0.5` `tension`
`0.75` `contradicted` · `0.6431 → 0.05` · `0.6512 → 0.15` · `0.2103 → 0.88` (rows A15.* of
`research/v13/12_claims_map_additions_F13-15.json`).

Scope (14 pt, one line; "only" allowlisted against SAT.gate):

> Reference harness, no spacecraft enrolled; the gate binds the value digest only.

---

## D. Claims map

Machine-readable twin: `research/v13/12_claims_map.json` (212 rows; schema in its header). Generator: Appendix I (save as
`research/repro/v13/claims/claims.py` at build; it rewrites the JSON and re-checks every row). Status vocabulary: SPEC, LIVE,
MEASURED, PRE-REGISTERED, INFERRED, EXTERNAL, OUT-OF-SCOPE. "check" = pass means the generator read the value from the
file today; "manual" means the source is a quote, a spec, a report section or a pending R5 file. R5 rows have date
`pending` and print only in R5 mode. Rows whose note begins `CONDITIONAL` print only when the condition holds. Per-model
R5 rows (haiku, sonnet, opus, fable, qwen7b × 7 conditions) are in the JSON and omitted from this table.

Rows that the build team must still materialise as a committed file before print (gate fails otherwise):
`E8.s2b` (0.4370 needs `research/repro/v13/eight_answers.json` from a committed rasterio re-read of
`S2B_43SFS_20260925_0_L2A` at row 9443, col 9098; report 05 §4.2 gives the expected DNs 1014/2588), `E8.double` (same
file, E84 DNs 900/2502), `F.date` (commit an erratum to `research/repro/data/v9/rawband/results.md`: 10 of 10 noticed),
`TM.still` and `V.resolve` (re-fetch within 7 days of print and save the response).

| id | block | printed | status | layer | source (file · key/line) | date | check |
|---|---|---|---|---|---|---|---|
| H.title | header | EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings | LIVE | n/a | file: research/v13/evidence/industry/prog_posters.txt · line: 42 · url: https://agentic-eo.berlin/programme/posters/ | 2026-10-01 | pass |
| H.session | header | Poster Session 1 / 19 Oct 2026 | LIVE | n/a | file: research/v13/evidence/industry/prog_posters.txt · url: https://agentic-eo.berlin/programme/posters/ | 2026-10-01 | manual |
| H.hero | header | Agents hand each other evidence references, not paraphrases. | SPEC | n/a | file: research/v13/10_ladder_threat_invention.md · section: 1.1 invention statement | 2026-10-01 | manual |
| H.sub.mechanism | header | The receiver resolves the reference, re-hashes the record, re-reads the source. | MEASURED | L0-L3 | file: research/repro/v11/out/summary.md · pointer: levels C, D, I | 2026-09-30 | manual |
| H.sub.boundary | header | A signature fixes the record's bytes, not the measurement. | OUT-OF-SCOPE | L5 | file: repro/data/v8/pixel_check.json · example: M15: signed 0.3444 vs containing pixel 0.4860 (kxjvfwpa) | 2026-10-01 | manual |
| H.img.record | header | NDVI 0.4709 / Sentinel-2A L2A / Keylong, Lahaul, India / 25 Sep 2026 | MEASURED | L1 | file: repro/data/v8/pixel_check.json · pointer: ['S2A 2026-09-25 (now, fact oj5cecci, signed 2026-09-28T09:06Z = post-fix)', 'ndvi_floor_pixel'] | 2026-09-25 | pass |
| H.img.grid | header | signed 10 m grids / B04/B03/B02 / linear 1 to 99 % stretch, γ 1/1.35 | MEASURED | L3 | file: research/repro/data/keylong_B0{2,3,4}.bin · note: EMEMGRD1 443 x 453 px, EPSG:32643, values DN-1000; window equality asserted in research/v13/evidence/visual/proto_m15.py | 2026-09-25 | manual |
| S.R1.A | P1 spine + P5 matrix | 15 / 15 | MEASURED | n/a | file: repro/v11/out/mutation_matrix.json · pointer: ['summary', 'A', 'false_accepts'] · denominator: ['summary', 'A', 'applicable'] | 2026-09-30 | pass |
| S.R1.B | P1 spine + P5 matrix | 15 / 15 | MEASURED | n/a | file: repro/v11/out/mutation_matrix.json · pointer: ['summary', 'B', 'false_accepts'] · denominator: ['summary', 'B', 'applicable'] | 2026-09-30 | pass |
| S.R1.C | P1 spine + P5 matrix | 13 / 16 | MEASURED | L0 | file: repro/v11/out/mutation_matrix.json · pointer: ['summary', 'C', 'false_accepts'] · denominator: ['summary', 'C', 'applicable'] | 2026-09-30 | pass |
| S.R1.I | P1 spine + P5 matrix | 0 / 16 | MEASURED | L0-L3 | file: repro/v11/out/mutation_matrix.json · pointer: ['summary', 'I', 'false_accepts'] · denominator: ['summary', 'I', 'applicable'] | 2026-09-30 | pass |
| S.headline | P1 spine | Handed prose, B acted on 15 of 15 corruptions; handed a reference it checks, on 0 of 16. | MEASURED | L0-L3 | file: repro/v11/out/mutation_matrix.json · pointer: summary.A, summary.I | 2026-09-30 | manual |
| S.16 | P1 spine | 16 ways / 16 corruptions | MEASURED | n/a | file: repro/v11/out/mutation_matrix.json · pointer: meta.mutations minus G0 and M17 | 2026-09-30 | pass |
| S.threshold | P1 spine + P2 + P6 | 0.4705 / irrigate if NDVI ≤ 0.4705 | PRE-REGISTERED | n/a | file: repro/v11/out/mutation_matrix.json · pointer: ['meta', 'rule'] · prereg: research/repro/data/v8/prereg.md (constructed boundary test) | 2026-09-30 | pass |
| S.G2.haiku.F | P1 spine | Claude Haiku 4.5 declined 5 of 5 | PRE-REGISTERED | L1 | file: repro/data/v8/results.json · pointer: ['b', 'claude-haiku-4-5', 'arms', 'F', 'decisions', 'DECLINE'] · prereg: research/repro/data/v8/prereg.md blake3 67631a79... | 2026-09-30 | pass |
| S.G2.qwen.F | P1 spine | Qwen2.5-3B / acted 5 of 5 | PRE-REGISTERED | L1 | file: v13/evidence/g2_handoff/qwen_trials.jsonl · pointer: count(arm=F, decision=IRRIGATE) · prereg: research/v13/evidence/g2_handoff/prereg_addendum2.md | 2026-09-30 | pass |
| S.G2.qwen.bare | P1 spine | dropped the cell from all 24 calls | PRE-REGISTERED | L1 | file: v13/evidence/g2_handoff/qwen_trials.jsonl · pointer: count(tool_calls[].token_form == 'bare_cid') over arms T and F | 2026-09-30 | pass |
| S.G2.boundary | P1 spine | a reference protects only a receiver that keeps it whole and obeys a refusal | INFERRED | L1 | inputs: ['S.G2.haiku.F', 'S.G2.qwen.F', 'S.G2.qwen.bare'] | 2026-10-01 | manual |
| S.scope | P1 spine | one record, one band, one run / test key | MEASURED | n/a | file: research/repro/v11/out/summary.md · pointer: Notes | 2026-09-30 | manual |
| S.boundary_wall | P1 spine | the entity meant (M17) / sensor accuracy / the decision | OUT-OF-SCOPE | L4-L5 | file: repro/v11/out/mutation_matrix.json · pointer: ['summary', 'I', 'entity_case_accepted'] | 2026-09-30 | pass |
| R5.A.pooled | P1 spine + P5 matrix | {R5.A.pooled.false_accept} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) · pointer: primary.A.pooled_claude.false_accept · prereg: research/repro/v13/r5/prereg.md (BLAKE3 pushed before trial 1) | pending | manual |
| R5.B.pooled | P1 spine + P5 matrix | {R5.B.pooled.false_accept} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) · pointer: primary.B.pooled_claude.false_accept · prereg: research/repro/v13/r5/prereg.md (BLAKE3 pushed before trial 1) | pending | manual |
| R5.C.pooled | P1 spine + P5 matrix | {R5.C.pooled.false_accept} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) · pointer: primary.C.pooled_claude.false_accept · prereg: research/repro/v13/r5/prereg.md (BLAKE3 pushed before trial 1) | pending | manual |
| R5.D.pooled | P1 spine + P5 matrix | {R5.D.pooled.false_accept} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) · pointer: primary.D.pooled_claude.false_accept · prereg: research/repro/v13/r5/prereg.md (BLAKE3 pushed before trial 1) | pending | manual |
| R5.E0.pooled | P1 spine + P5 matrix | {R5.E0.pooled.false_accept} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) · pointer: primary.E0.pooled_claude.false_accept · prereg: research/repro/v13/r5/prereg.md (BLAKE3 pushed before trial 1) | pending | manual |
| R5.E.pooled | P1 spine + P5 matrix | {R5.E.pooled.false_accept} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) · pointer: primary.E.pooled_claude.false_accept · prereg: research/repro/v13/r5/prereg.md (BLAKE3 pushed before trial 1) | pending | manual |
| R5.Eplus.pooled | P1 spine + P5 matrix | {R5.Eplus.pooled.false_accept} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) · pointer: primary.Eplus.pooled_claude.false_accept · prereg: research/repro/v13/r5/prereg.md (BLAKE3 pushed before trial 1) | pending | manual |
| R5.cell.cond.item.false_accept | P1/P5 (R5 mode only) | {R5.cell.<cond>.<item>.false_accept} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) | pending | manual |
| R5.G0.cond.pooled.false_refusal | P1/P5 (R5 mode only) | {R5.G0.<cond>.pooled.false_refusal} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) | pending | manual |
| R5.E0.pooled.verify_called | P1/P5 (R5 mode only) | {R5.E0.pooled.verify_called} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) | pending | manual |
| R5.M15r.Eplugin.false_accept | P1/P5 (R5 mode only) | {R5.M15r.Eplugin.false_accept} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) | pending | manual |
| R5.M15r.EpluginV.false_accept | P1/P5 (R5 mode only) | {R5.M15r.EpluginV.false_accept} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) | pending | manual |
| R5.M20.E.pooled.false_accept | P1/P5 (R5 mode only) | {R5.M20.E.pooled.false_accept} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) | pending | manual |
| R5.models | P1/P5 (R5 mode only) | {R5.models} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) | pending | manual |
| R5.dates | P1/P5 (R5 mode only) | {R5.dates} | PRE-REGISTERED | L0-L3 | file: research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build) | pending | manual |
| E8.right | P2 eight answers | 0.4709 signed record | MEASURED | L0 | file: repro/data/v8/pixel_check.json · pointer: S2A ... ndvi_floor_pixel | 2026-10-01 | pass |
| E8.rounded | P2 eight answers | 0.47 rounded in prose | PRE-REGISTERED | L0 | file: repro/data/v8/results.json · pointer: b.claude-haiku-4-5.arms.R.decisions.IRRIGATE = 5 (exploratory addendum) | 2026-10-01 | pass |
| E8.s2b | P2 eight answers | 0.4370 other satellite, same day | MEASURED | L1 | file: research/repro/v13/eight_answers.json (to create; values from report 05 sec. 4.2, rasterio 1.4.4, 2026-10-01) | 2026-10-01 | manual |
| E8.newer | P2 eight answers | 0.4237 30 Sep record handed as 25 Sep | LIVE | L1 | file: repro/data/v11/cell_products.json · pointer: band=indices.ndvi value | 2026-10-01 | pass |
| E8.neighbour | P2 eight answers | 0.3016 neighbour pixel | MEASURED | L3 | file: repro/data/v8/pixel_check.json · pointer: S2A ... ndvi_round_pixel | 2026-10-01 | pass |
| E8.offset0 | P2 eight answers | 0.2966 offset left out | INFERRED | L3 | inputs: pixel_check.json DNs · formula: (3502-1900)/(3502+1900) | 2026-10-01 | pass |
| E8.place | P2 eight answers | 0.2824 town point 597 m away (30 Sep) | MEASURED | L1 | file: repro/data/v11/ask_keylong.json · pointer: answer fact p6ewjnlq value 0.28244274809160314 | 2026-10-01 | pass |
| E8.double | P2 eight answers | 1.1427 offset applied twice | INFERRED | L2 | inputs: E84 DNs 900/2502 (report 05 sec. 4.2) + raster:bands offset -0.1 (research/v13/evidence/failure_modes/e84_keylong.json) · formula: (0.2502-0.1 - (0.0900-0.1))/(0.2502-0.1 + 0.0900-0.1) | 2026-10-01 | pass |
| E8.summary | P2 eight answers | Six cross the irrigation line, one is impossible, one is right | INFERRED | n/a | inputs: ['E8.right', 'E8.rounded', 'E8.s2b', 'E8.newer', 'E8.neighbour', 'E8.offset0', 'E8.place', 'E8.double'] | 2026-10-01 | manual |
| E8.place_m | P2 + P3 | 597 m | MEASURED | L1 | file: repro/data/v11/ask_keylong.json · pointer: located stage (32.5717891, 77.0281479) vs asked (32.57126, 77.03448) · method: pyproj Geod WGS84 inv: 597.49 m | 2026-10-01 | pass |
| F.lost | P3 | 0.47 for 0.4709 / 5 of 5 receivers irrigated | PRE-REGISTERED | L0 | file: repro/data/v8/results.json · pointer: b.claude-haiku-4-5.arms.R.decisions.IRRIGATE | 2026-09-30 | pass |
| F.lost.out | P3 | Perez et al., ICLR 2025: LLM transmission chains drift | EXTERNAL | n/a | url: https://arxiv.org/abs/2407.04503 | 2026-10-01 | manual |
| F.date | P3 | asked 23 Sep, served 25 Sep / 10 of 10 agents saw one scene twice / 3 said no 23 Sep scene existed | PRE-REGISTERED | L1 | file: repro/data/v9/rawband/trials.jsonl · pointer: result_text of all 10 trials (critic C1 recount); results.md:14 says 9 and needs an erratum · prereg: research/repro/data/v9/rawband/prereg.md blake3 30d8a1a1 | 2026-09-30 | manual |
| F.date.out | P3 | STAC item search defines no default order | EXTERNAL | n/a | file: research/v13/evidence/failure_modes/item-search_README.md | 2026-10-01 | manual |
| F.place | P3 | coordinates given, town point answered / 597 m / NDVI 0.28 for the field's 0.42 | MEASURED | L1 | file: repro/data/v11/ask_keylong.json · pointer: located stage; answer value 0.28244 · field: repro/data/v11/cell_products.json indices.ndvi 0.4237 (same 30 Sep scene) | 2026-09-30 | manual |
| F.place.out | P3 | GDAL 3 follows CRS axis order (RFC 73) | EXTERNAL | n/a | url: https://gdal.org/development/rfc/rfc73_proj6_wkt2_srsbarn.html | 2026-10-01 | manual |
| F.version | P3 + P8 | 918.0 m / 915.07 m / one band name | MEASURED | L1 | file: repro/data/contra_bengaluru.json · pointer: contradictions[0].attestations values | 2026-09-29 | pass |
| F.version.out | P3 | GFC2020 V3 cut forest cover by more than 20 % in the Cerrado | EXTERNAL | n/a | file: research/v13/evidence/failure_modes/jrc146622.txt · line: 1492 · doi: 10.2760/9982436 | 2026-10-01 | pass |
| F.worldpop | P3 | WorldPop signed per pixel, not per km²: 1.77× low | SPEC | L2 | file: v13/evidence/failure_modes/CHANGELOG_18adb67.md · line: 61 · repo: emem 18adb67 CHANGELOG [2.4.2] | 2026-09-29 | pass |
| F.scale | P3 | one pixel: 0.4709, 0.2966, 1.1427 under three offset rules | INFERRED | L2-L3 | inputs: ['E8.right', 'E8.offset0', 'E8.double'] | 2026-10-01 | manual |
| F.scale.out | P3 | Element84 items say "offset applied" and "apply −0.1" | LIVE | n/a | file: research/v13/evidence/failure_modes/e84_keylong.json · pointer: features[*].properties earthsearch:boa_offset_applied + assets.red raster:bands offset | 2026-10-01 | pass |
| F.missing | P3 | off-tile pixels signed as 0 / a forest-loss screen passes | SPEC | L3 | file: v13/evidence/failure_modes/CHANGELOG_18adb67.md · line: 53 · repo: emem 18adb67 CHANGELOG [2.4.2] | 2026-09-29 | pass |
| F.missing.out | P3 | Hansen lossyear 0 means no loss | EXTERNAL | n/a | url: https://storage.googleapis.com/earthenginepartners-hansen/GFC-2025-v1.13/download.html | 2026-10-01 | manual |
| F.pixel | P3 + P6 | 162 of 200 / fixed 28 Sep 2026 | MEASURED | L3 | file: repro/data/v8/prevalence_summary.json · pointer: ['pre', 'matches_round_not_floor'] · fix: v13/evidence/failure_modes/CHANGELOG_18adb67.md:47 (2026-09-28T04:09:26Z) | 2026-09-30 | pass |
| F.pixel.out | P3 | GDAL RFC 33: half-pixel shift / one-pixel misregistration: error > 50 % of NDVI differences (Townshend 1992) | EXTERNAL | n/a | url: ['https://gdal.org/en/stable/development/rfc/rfc33_gtiff_pixelispoint.html', 'doi:10.1109/36.175340'] | 2026-10-01 | manual |
| F.thing | P3 | "this image" resolved to a hair salon in Ontario / receipt, Merkle proof and state chain all valid / fixed 30 Sep 2026 | SPEC | L4 | repo: Vortx-AI/emem · commit: 0edf574 · quote: Every part of the verification machinery worked on an answer about a hair salon in Canada. | 2026-09-30 | manual |
| F.thing.out | P3 | toponym ambiguity (Gritta et al. 2018) | EXTERNAL | n/a | doi: 10.1007/s10579-017-9385-8 | 2026-10-01 | manual |
| F.rail.cellmatch | P3 side rail | emem's resolver once reported a cell match it never tested | SPEC | L1 | repo: emem 18adb67 · file: crates/emem-api-rest/src/lib.rs:37800-37818 (line numbers move at 8e9b401) | 2026-08-11 | manual |
| F.rail.langchain | P3 side rail | one framework adapter returns a refusal as plain text | MEASURED | L1 | file: research/v13/evidence/crossruntime/refusal_matrix.json · pointer: ['wrong_cell', 'langchain_mcp'] | 2026-09-30 | pass |
| F.rail.mast | P3 side rail | MAST: no or incomplete verification (FM-3.2) | EXTERNAL | n/a | url: https://arxiv.org/abs/2503.13657 | 2026-10-01 | manual |
| F.caption | P3 | Signatures prevented none | INFERRED | n/a | file: research/v13/02_experiment_design.md · section: 18 (honest boundary) | 2026-10-01 | manual |
| T.can | threat | A relay can rewrite what it carries but cannot sign under the pinned key or match an address | SPEC | L0 | file: research/v13/10_ladder_threat_invention.md · section: 4.2-4.3 · external: RFC 8032 l.160; BLAKE3 spec 128-bit | 2026-10-01 | manual |
| T.pinned | threat | pinned key / DNS TXT / did.json / JWKS | LIVE | L0 | file: research/repro/v8/trace_fact_output.txt · pointer: link 15 | 2026-09-30 | manual |
| T.oneop | threat | All keys today are one operator's | LIVE | L0 | file: research/v13/evidence/ladder/witnesses.json · pointer: ['independent_operator_count'] | 2026-10-01 | pass |
| O.84 | P4 | 84 characters / 46 tokens (cl100k) | MEASURED | n/a | file: repro/data/v8/token_counts.json · pointer: ['fact_token_ndvi'] | 2026-09-30 | pass |
| O.46 | P4 + P11 | 46 tokens | MEASURED | n/a | file: v13/cost_measurements.json · pointer: ['m5_tokens', 'items', 'fact_token', 'cl100k'] | 2026-10-01 | pass |
| O.1115 | P4 | 1,115 B | LIVE | L0 | file: repro/data/v8/token_counts.json · pointer: ['fact_cbor_bytes', 'bytes'] · live: GET /v1/facts/oj5cecci... re-hashed 2026-10-01T01:42Z (critic) | 2026-10-01 | pass |
| O.cid | P4 | oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa | LIVE | L0 | file: research/repro/v8/proof_bundle_ndvi.cbor · pointer: token | 2026-10-01 | pass |
| O.cogs | P4 | 277.9 + 281.9 MB / B04 + B08 COGs / Planetary Computer | MEASURED | L3 | file: research/repro/data/v8/cog_pixel_bytes.json · pointer: B04 277897303 B, B08 281898500 B | 2026-09-30 | pass |
| O.pixel | P4 | row 9443, col 9098 / DN 1900, 3502 | MEASURED | L3 | file: repro/data/v8/pixel_check.json · pointer: S2A ... B08.floor(r,c), floor_DN | 2026-09-30 | pass |
| O.key | P4 | 777er3yi… | LIVE | L0 | file: repro/data/v8/crossruntime_table.json · pointer: responder key | 2026-10-01 | pass |
| O.nohash | P4 + P7 | named, not hashed / 0 of 215 Keylong sources carry a hash | MEASURED | L3 | file: repro/data/v11/cell_keylong.json · pointer: count(sources[] with hash or cid) | 2026-09-30 | pass |
| O.sevenaddr | P4 | one Bengaluru value has seven | MEASURED | L0 | file: repro/data/contra_bengaluru.json · pointer: 7 attestations with value 915.0712280273438, 7 fact_cids | 2026-09-29 | pass |
| O.batch | P4 | a batch signature covers such addresses | SPEC | L0 | repo: emem 18adb67 · file: crates/emem-fact/src/attest.rs:93-143 | 2026-10-01 | manual |
| O.log | P4 | Merkle log, RFC 6962 style, BLAKE3 | SPEC | L0 | repo: emem · file: crates/emem-attest/src/translog.rs; docs/federation.md 9c | 2026-10-01 | manual |
| X.loo | P5 | Each of five checks alone stops a corruption. | MEASURED | L0-L3 | file: repro/v11/out/mutation_matrix.json · pointer: ['leave_one_out'] | 2026-09-30 | pass |
| X.only | P5 + H2 | only the source re-read, the signer's wrong pixel / Only a source re-read catches a signer's wrong pixel / caught only by a re-read / only it refuses the wrong pixel | MEASURED | L3 | file: repro/v11/out/mutation_matrix.json · pointer: ['leave_one_out', 'I'] | 2026-09-30 | pass |
| X.flips | P5 | flips the decision | MEASURED | n/a | file: repro/v11/out/mutation_matrix.json · pointer: ['summary', 'A', 'decision_flips'] | 2026-09-30 | pass |
| X.p123 | P5 scope | Three further signer errors (offset, same-day scene, unit) pass checks D to I; metadata checks catch them. | MEASURED | L3 | file: research/v13/evidence/ladder/r1_t2_extra_out.json · pointer: T2_offset_zero, T2_scene_relabel_same_day, T2_unit_mislabel .refused_at_level_I == false | 2026-10-01 | pass |
| X.entity | P5 | The entity meant passes every check | OUT-OF-SCOPE | L4 | file: repro/v11/out/mutation_matrix.json · pointer: M17 outcome at every level | 2026-09-30 | manual |
| W.vals | P6 | 0.4709 → hold / 0.3016 → irrigate | MEASURED | L3 | file: repro/data/v8/pixel_check.json · pointer: S2A ... ndvi_floor_pixel / ndvi_round_pixel | 2026-09-30 | pass |
| W.prev | P6 | 162 of 200 sampled pre-fix records / Wilson 95 %: 75 to 86 % | MEASURED | L3 | file: repro/data/v8/prevalence_summary.json · pointer: ['pre', 'frac_round_wilson95'] · script: research/v13/evidence/g1_pixel_audit/prevalence.py (seed 20261019) | 2026-09-30 | pass |
| W.err | P6 | median 0.027 / p90 0.113 / max 0.301 / n 121 | MEASURED | L3 | file: repro/data/v8/prevalence_summary.json · pointer: ['pre', 'abs_err_index_where_differ'] | 2026-09-30 | pass |
| W.kx | P6 | signed 0.3444 / 0.4860 / 23 Sep 2026 | LIVE | L3 | file: repro/data/v8/pixel_check.json · pointer: S2C 2026-09-23 ... ndvi_round_pixel / ndvi_floor_pixel · live: research/v13/evidence/critic/kx.json (GET 2026-10-01T01:41Z, no warning in body) | 2026-10-01 | pass |
| W.frame | P6 scope | 200 pre-fix Sentinel-2 records cited in emem.dev's public channel, one per cell, seeded / 192 Element84, 8 Planetary Computer | MEASURED | n/a | file: repro/data/v8/prevalence_summary.json · pointer: ['pre', 'providers'] · script: research/v13/evidence/g1_pixel_audit/prevalence.py:1-20 | 2026-09-30 | pass |
| W.post | P6 scope | 0 of 54 / Planetary Computer, two days | MEASURED | L3 | file: repro/data/v8/prevalence_summary.json · pointer: ['post', 'matches_round_not_floor'] | 2026-09-30 | pass |
| W.rondonia | P6 scope | changed 7 loss years and no EUDR flag / 100-point Rondônia grid | MEASURED | L3 | file: research/v13/evidence/failure_modes/rondonia_floor_round_v2.json · pointer: count(lossyear floor != round) = 7; flags floor 3 / round 3 | 2026-10-01 | pass |
| W.south | P6 | pixel 10 m south / 10 m south | MEASURED | L3 | file: repro/data/v8/pixel_check.json · pointer: round(r,c) = floor row + 1, same col | 2026-09-30 | manual |
| L.780 | P7 | 780 of 780 / 780 records pulled on 30 Sep 2026 / cell and band bound in 780 of 780 | MEASURED | L0-L1 | file: repro/v12/data/eo_evidence_per_fact_checks.csv · pointer: count(verified == PASS) | 2026-09-30 | pass |
| L.266 | P7 | 266 of 780 | MEASURED | L2 | file: repro/v12/data/eo_evidence_per_fact_checks.csv · pointer: count(recompute == pass) | 2026-09-30 | pass |
| L.reread0 | P7 | their source files are named, not hashed | SPEC | L3 | repo: emem 18adb67 and 8e9b401 · file: crates/emem-api-rest/src/lib.rs: 62 x 'hash: None', 0 x 'hash: Some(' (report 10 sec. 0 item 2) · measured: 0 of 215 Keylong source entries (O.nohash) | 2026-10-01 | manual |
| L.409 | P7 | a relabelled token returns 409 | MEASURED | L1 | file: research/v13/evidence/crossruntime/refusal_matrix.json · pointer: ['wrong_cell', 'rest'] | 2026-09-30 | pass |
| L.gfc | P7 | GFC2020 V3 forest commission error 13.1 % | EXTERNAL | L5 | file: research/v13/evidence/failure_modes/jrc146622.txt · line: 236 | 2026-10-01 | pass |
| L.status | P7 | CHECKABLE / RECOMPUTABLE / PARTIAL / INHERITED / OUT OF SCOPE | SPEC | L0-L5 | file: research/v13/10_ladder_threat_invention.md · section: 3.1-3.2 | 2026-10-01 | manual |
| TM.918 | P8 | 918.0 m / signed 28 May / 90 m DEM via Open-Meteo | MEASURED | L1 | file: repro/data/contra_bengaluru.json · pointer: attestation yqbolgeo signed_at 2026-05-28T19:54:32Z; fn_key open_meteo_copdem90m@1 | 2026-09-29 | pass |
| TM.915 | P8 | 915.07 m / first signed 11 Aug / re-signed 7 times | MEASURED | L1 | file: repro/data/contra_bengaluru.json · pointer: 7 attestations value 915.0712280273438, first 2026-08-11T09:39:36Z | 2026-09-29 | pass |
| TM.asof | P8 | 1 May: none / 15 Jun: 918.0 m / 12 Aug: 915.07 m / 29 Sep: 915.07 m | MEASURED | L1 | file: repro/data/contra_bengaluru.json · recompute: poster/make_figures_v12.py:506-510 asserts these as-of answers from the attestations | 2026-09-29 | manual |
| TM.keylong | P8 | cited 25 Sep: 0.4709 → hold / 30 Sep: 0.4237 → irrigate | LIVE | L1 | file: repro/data/v11/cell_products.json · pointer: indices.ndvi 3yyaxn5d 0.4237 signed 2026-09-30T22:20:02Z | 2026-09-30 | pass |
| TM.still | P8 | the cited reference still re-hashes (1 Oct 2026) | LIVE | L0 | file: research/v13/11_research_gaps.md · pointer: P1-8: oj5cecci 1,115 B re-hash equal at 01:42Z | 2026-10-01 | manual |
| TM.asof_rule | P8 scope | as-of compares signing times (UTC seconds) | SPEC | L1 | repo: emem · file: crates/emem-primitives/src/recall.rs:282-391; defect 35 (string compare) | 2026-10-01 | manual |
| RO.grid | P9 | 100 point samples / 740 m apart / 600 signed records | MEASURED | L0 | file: repro/v12/data/case_rondonia_eudr.json · pointer: ['grid'] | 2026-09-30 | pass |
| RO.cats | P9 | forest 2020 (GFC2020) + loss after 2020 (Hansen): 3 / forest, no later loss: 33 / cleared 2001 to 2020: 20 / not forest: 43 / maps disagree: 1 | MEASURED | n/a | file: repro/v12/data/case_rondonia_eudr.json · pointer: ['category_counts'] | 2026-09-30 | pass |
| RO.tmf | P9 | TMF agrees on 1 of 3 flags | MEASURED | n/a | file: repro/v12/data/case_rondonia_eudr.json · pointer: rows with eudr flag: jrc_tmf.deforestation_year 2023, 0, 0 | 2026-09-30 | manual |
| RO.cardA | P9 | Hansen loss 2023 / tree cover 2000 100 % / GFC2020 V4 forest / TMF 2023 / CCI 208 t/ha | MEASURED | n/a | file: repro/v12/data/case_rondonia_eudr.json · pointer: row cell defi.zb391.taza.zcc31 | 2026-09-30 | manual |
| RO.must | P9 | Point samples, not parcel polygons; not a regulatory determination. | OUT-OF-SCOPE | L5 | file: research/SHARED_STATE_EMEM_A0_MASTER.md · section: 21 | 2026-10-01 | manual |
| V.prithvi | P10 | Prithvi-EO-2.0 / 1,024 values / checkpoint 2ad1775f… | LIVE | L2 | file: v13/evidence/critic/cell.json · pointer: facts[band=prithvi_eo2].served_via.model_blake2b_hex == derivation.args.args[4] | 2026-10-01 | pass |
| V.tessera | P10 | TESSERA / 128 values / only a path and year / …/npy/v1/2024/… | LIVE | L3 | file: v13/evidence/critic/cell.json · pointer: facts[band=geotessera].sources[0].id = .../npy/v1/2024/..., args [lat, lng, 2024] | 2026-10-01 | pass |
| V.retired | P10 | emem.dev lists its encoders as retired | SPEC | n/a | file: research/repro/v12/data/v1_bands_2026-09-30.json · pointer: bands[*].materializer.kind == retired for geotessera, clay_v1, prithvi_eo2, galileo | 2026-09-30 | pass |
| V.resolve | P10 | Both still resolve | LIVE | L0 | file: v13/evidence/critic/cell.json · pointer: GET /v1/cells/defi.zb572.xoso.zb1ec 2026-10-01T01:42Z | 2026-10-01 | manual |
| C.cpu | P11 | 0.33 ms of CPU / One 2.8 GHz Xeon core | MEASURED | L0-L3 | file: v13/cost_measurements.json · pointer: ['m2_offline_verification', 'mutation_suite_ms_per_decision_by_level', 'I', 'median'] · host: one 2.8 GHz Xeon core | 2026-10-01 | pass |
| C.reread | P11 | 1.18 MB / about 7 s | MEASURED | L3 | file: v13/cost_measurements.json · pointer: m3_trace_read_only.keylong_ndvi.links 8+9+9b: 6,945 ms, 1,180,728 B | 2026-10-01 | pass |
| C.scene | P11 | 0.058 % of the scene | MEASURED | L3 | file: research/repro/data/v8/scene_sizes.json + cog_pixel_bytes.json · pointer: 1,165,033 / 2,023,818,762 | 2026-09-30 | pass |
| C.tok | P11 | 46 tokens / the value 8 | MEASURED | n/a | file: v13/cost_measurements.json · pointer: ['m5_tokens', 'items', 'value_16_digits', 'cl100k'] | 2026-10-01 | pass |
| C.tools | P11 | 18-tool MCP list 18,709 (1 Oct) | MEASURED | n/a | file: v13/cost_measurements.json · pointer: ['m5_tokens', 'items', 'mcp_tools_list_core18_response', 'cl100k'] | 2026-10-01 | pass |
| C.json | P11 | record as JSON 562 | MEASURED | n/a | file: v13/cost_measurements.json · pointer: ['m5_tokens', 'items', 'fact_json_as_served', 'cl100k'] | 2026-10-01 | pass |
| C.g2tok | P11 | 2.1× the tokens prose costs / same decisions | PRE-REGISTERED | n/a | file: repro/data/v8/results.json · pointer: b.claude-haiku-4-5.arms.{T,P}.input_tokens_mean; decision_correct 10/10 both | 2026-09-30 | pass |
| C.g2wall | P11 scope | +1.75 s | PRE-REGISTERED | n/a | file: repro/data/v8/results.json · pointer: wall_s_mean T 8.85 - P 7.10 | 2026-09-30 | pass |
| C.resolve | P11 | 40 ms warm / 154 ms cold | MEASURED | L0 | file: v13/cost_measurements.json · pointer: m1_resolve_fact_https.{warm_cbor_reused_connection_ms,cold_cbor_new_connection_ms}.median | 2026-10-01 | pass |
| C.bundle | P11 | 4,906 B / offline proof bundle 0.57 ms | MEASURED | L0-L2 | file: v13/cost_measurements.json · pointer: ['m2_offline_verification', 'in_process_precompiled_exec_ms', 'median'] | 2026-10-01 | pass |
| C.hash | P11 | 1.6 µs | MEASURED | L0 | file: v13/cost_measurements.json · pointer: ['m2_offline_verification', 'primitives_us', 'blake3_fact_1115B', 'median'] | 2026-10-01 | pass |
| EC.11 | P12 | 11 client paths / one address and one value | MEASURED | L0 | file: repro/data/v8/crossruntime_table.json · pointer: ['summary', 'ndvi_keylong', 'paths_ok'] | 2026-09-30 | pass |
| EC.9of11 | P12 | with receipt signatures checked on 9 | MEASURED | L0 | file: repro/data/v8/crossruntime_table.json · pointer: ['summary', 'ndvi_keylong', 'receipt_verified_paths'] | 2026-09-30 | pass |
| EC.ms | P12 dot plot | 56.3 / 58.3 / 58.6 / 207.7 / 223.5 / 223.7 / 226.3 / 235.6 / 300.8 / 1,176.8 | MEASURED | L0 | file: repro/data/v8/crossruntime_table.json · pointer: rows.ndvi_keylong[*].ms_median (never .ms, which is the last repetition) | 2026-09-30 | pass |
| EC.notrun | P12 | Not run by us: ChatGPT, claude.ai, Dify, VS Code, Cursor | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: rows chatgpt, claude-ai-custom-connector, dify-marketplace, vscode, cursor: evidence_level | 2026-10-01 | manual |
| EC.row.claude-code-mcp | P12 band | Claude Code | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: id=claude-code-mcp: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.claude-code-plugin | P12 band | Claude Code plugin | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: id=claude-code-plugin: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.claude-ai-custom-connector | P12 band | Claude.ai custom connector | SPEC | n/a | file: v13/ecosystem_manifest.json · pointer: id=claude-ai-custom-connector: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.dify-marketplace | P12 band | Dify Marketplace plugin (community) | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: id=dify-marketplace: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.mcp-core | P12 band | Model Context Protocol (MCP) | SPEC | n/a | file: v13/ecosystem_manifest.json · pointer: id=mcp-core: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.a2a | P12 band | Agent2Agent (A2A) | SPEC | n/a | file: v13/ecosystem_manifest.json · pointer: id=a2a: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.official-mcp-registry | P12 band | Official MCP Registry | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: id=official-mcp-registry: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.github-mcp-registry | P12 band | GitHub MCP Registry | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: id=github-mcp-registry: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.github-repo | P12 band | github.com/Vortx-AI/emem | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: id=github-repo: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.glama | P12 band | Glama | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: id=glama: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.gemini-cli | P12 band | Gemini CLI | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: id=gemini-cli: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.vscode | P12 band | Visual Studio Code | SPEC | n/a | file: v13/ecosystem_manifest.json · pointer: id=vscode: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.cursor | P12 band | Cursor | SPEC | n/a | file: v13/ecosystem_manifest.json · pointer: id=cursor: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.python-sdk | P12 band | pip install ememdev | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: id=python-sdk: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.ts-sdk | P12 band | npm i @vortxai/emem | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: id=ts-sdk: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.rest-openapi | P12 band | REST / OpenAPI 3.1 | SPEC | n/a | file: v13/ecosystem_manifest.json · pointer: id=rest-openapi: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.docker | P12 band | ghcr.io/vortx-ai/emem | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: id=docker: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.llamaindex | P12 band | LlamaIndex | MEASURED | n/a | file: v13/ecosystem_manifest.json · pointer: id=llamaindex: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.autogen | P12 band | AutoGen | MEASURED | n/a | file: v13/ecosystem_manifest.json · pointer: id=autogen: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.crewai | P12 band | CrewAI | MEASURED | n/a | file: v13/ecosystem_manifest.json · pointer: id=crewai: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.mastra | P12 band | Mastra | MEASURED | n/a | file: v13/ecosystem_manifest.json · pointer: id=mastra: status, print.allowed, verified_utc | 2026-10-01 | pass |
| EC.row.chatgpt | P12 band (conditional) | ChatGPT (@emem) | OUT-OF-SCOPE | n/a | file: v13/ecosystem_manifest.json · pointer: id=chatgpt | 2026-10-01 | manual |
| EC.row.langchain | P12 band (conditional) | LangChain (MCP adapters) | MEASURED | n/a | file: v13/ecosystem_manifest.json · pointer: id=langchain | 2026-10-01 | manual |
| EC.row.agno | P12 band (conditional) | Agno | MEASURED | n/a | file: v13/ecosystem_manifest.json · pointer: id=agno | 2026-10-01 | manual |
| EC.statusdate | P12 legend | checked 30 Sep 2026 | LIVE | n/a | file: v13/ecosystem_manifest.json · pointer: verified_utc of every printed row | 2026-10-01 | manual |
| PA.stac | P13 | FIND · STAC · an asset (file) | EXTERNAL | n/a | url: https://stacspec.org (STAC 1.1.0) · report: research/v13/04_prior_art_and_field.md sec. 1-2 | 2026-10-01 | manual |
| PA.openeo | P13 | RUN · openEO · a process graph | EXTERNAL | n/a | url: openEO API 1.3.0 · report: research/v13/04_prior_art_and_field.md sec. 1-2 | 2026-10-01 | manual |
| PA.prov | P13 | RECORD LINEAGE · W3C PROV · entity, activity, agent | EXTERNAL | n/a | url: https://www.w3.org/TR/prov-dm/ · report: research/v13/04_prior_art_and_field.md sec. 1-2 | 2026-10-01 | manual |
| PA.c2pa | P13 | SIGN FILES · C2PA, CDSE Traceability · a file | EXTERNAL | n/a | url: C2PA 2.4; documentation.dataspace.copernicus.eu/APIs/Traceability.html · report: research/v13/04_prior_art_and_field.md sec. 1-2 | 2026-10-01 | manual |
| PA.rag | P13 | RETRIEVE · RAG · a text chunk | EXTERNAL | n/a | url: arXiv 2005.11401 · report: research/v13/04_prior_art_and_field.md sec. 1-2 | 2026-10-01 | manual |
| PA.carry | P13 | CARRY · MCP, A2A · a tool call, an agent card | EXTERNAL | n/a | url: MCP 2025-11-25; A2A 1.0 · report: research/v13/04_prior_art_and_field.md sec. 1-2 | 2026-10-01 | manual |
| PA.geoguard | P13 | JUDGE · GeoGuard · a claim in text | EXTERNAL | n/a | url: https://github.com/NASA-IMPACT/geoguard · report: research/v13/04_prior_art_and_field.md sec. 1-2 | 2026-10-01 | manual |
| PA.credit | P13 | Sigstore, RFC 9162, SCITT (RFC 9943) / ARC (arXiv 2607.25066) | EXTERNAL | n/a | url: report 04 sec. 2.8-2.14 · report: research/v13/04_prior_art_and_field.md sec. 1-2 | 2026-10-01 | manual |
| PA.critical | P13 | A STAC item identifies a file; EMEM identifies the observation an agent cited | SPEC | L1 | file: research/v13/04_prior_art_and_field.md · section: 2.1, 8 | 2026-10-01 | manual |
| PA.munir | P3 header strip | errors may propagate silently across steps / Munir et al. 2026, arXiv 2604.24919 | EXTERNAL | n/a | url: https://arxiv.org/abs/2604.24919 · report: research/v13/04_prior_art_and_field.md sec. 0 item 9, 2.15 | 2026-10-01 | manual |
| PA.geoguard_line | P13 | GeoGuard judges the claim; EMEM fixes the evidence it cites. | EXTERNAL | n/a | file: research/v13/04_prior_art_and_field.md · section: 2.7 | 2026-10-01 | manual |
| H.byline | header | Jaya Kumari / Avijeet Singh / Vortx AI / emem.dev / github.com/Vortx-AI/emem (Apache-2.0) / BIFOLD and ESA Φ-lab / Berlin | LIVE | n/a | file: research/v13/evidence/industry/prog_posters.txt · repo_licence: research/v13/03_ecosystem_manifest.md row GitHub (Apache-2.0) | 2026-10-01 | manual |
| REF.footer | footer | Sentinel-2 Products Specification (ESA) / Copernicus DEM GLO-30/90 / Hansen et al. 2013, GFC v1.13 / JRC GFC2020 V3/V4, TMF / ESA CCI Biomass v7 / Reg. (EU) 2023/1115 / BLAKE3 / RFC 8032 / RFC 6962/9162 / STAC 1.1 / openEO 1.3 / W3C PROV-DM / C2PA 2.4 / MCP 2025-11-25 / A2A 1.0 / Perez et al., ICLR 2025 / Munir et al. 2026 (2604.24919) / Cemri et al. 2025, MAST (2503.13657) / Dang et al. 2026, ARC (2607.25066) / Townshend et al. 1992 / GeoGuard (NASA-IMPACT) / Prithvi-EO-2.0 / TESSERA (2506.20380) | EXTERNAL | n/a | report: research/v13/04_prior_art_and_field.md sec. 6 (arXiv ids verified via the arXiv API); 00_v11_review_findings.md EXT-3 (ESA document title) | 2026-10-01 | manual |
| K.concl | conclusion | none of the 16 corruptions in our suite / a wrong pixel emem signed in production | MEASURED | L0-L3 | inputs: ['S.R1.I', 'F.pixel'] | 2026-09-30 | manual |
| K.commit | footer | emem.dev at commit 8e9b401 | LIVE | n/a | header: x-emem-commit 8e9b401cecae7ab9944d403a2d7840952c6586a6 · file: v13/cost_measurements.json · pointer: ['environment', 'emem_server_commit_header'] | 2026-10-01 | pass |
| K.dates | footer | measurements 29 Sep to 1 Oct 2026 | MEASURED | n/a | inputs: dates of every row above | 2026-10-01 | manual |
| K.sat042 | footer | Extending verification to execution: reference harness, no spacecraft enrolled. | SPEC | n/a | file: research/repro/v12/trace/sat042_run_stdout.txt | 2026-09-30 | manual |
| Q.view_demo | QR | VIEW THE DEMO | SPEC | n/a | payload: https://vortx-ai.github.io/esa_poster/demo/ · file: research/v13/evidence/visual/qr/qr_table.json | 2026-10-01 | manual |
| Q.try_token | QR | TRY A TOKEN | SPEC | n/a | payload: https://vortx-ai.github.io/esa_poster/t/ · file: research/v13/evidence/visual/qr/qr_table.json | 2026-10-01 | manual |
| Q.inspect_record | QR | INSPECT THE RECORD | SPEC | n/a | payload: https://vortx-ai.github.io/esa_poster/r/ · file: research/v13/evidence/visual/qr/qr_table.json | 2026-10-01 | manual |
| Q.re-run_test | QR | RE-RUN THE TEST | SPEC | n/a | payload: https://vortx-ai.github.io/esa_poster/test/ · file: research/v13/evidence/visual/qr/qr_table.json | 2026-10-01 | manual |
| Q.read_methods | QR | READ THE METHODS | SPEC | n/a | payload: https://vortx-ai.github.io/esa_poster/methods/ · file: research/v13/evidence/visual/qr/qr_table.json | 2026-10-01 | manual |
| Q.discover_integrations | QR | DISCOVER INTEGRATIONS | SPEC | n/a | payload: https://vortx-ai.github.io/esa_poster/use/ · file: research/v13/evidence/visual/qr/qr_table.json | 2026-10-01 | manual |

---

## E. Figure specifications

Shared rules for every figure (report 06 §3, §4): drawn 1:1 at print size in mm with `fig_mm`/`mm_axes` from
`poster/make_figures_v12.py` (copy into `poster/make_figures_v13.py`); text stays text (`svg.fonttype: "none"`) and every
label is also dumped to `fig/v13/<name>.labels.json` with its claim id; floor 14 pt, `check_text` extended to text
versus lines; colour encodes evidence state only: `emem` #0F5FA8 (reference, refusal, checked), `harm` #D2481E (B acts on
corrupted evidence, the adversary, the wrong pixel; text below 24 pt uses `harm-text` #B5401A), `incident` #E8A317 (seen
in production; rings and 3 mm bars only, always with a word), `oos` #9C9A92 with 45° hatch on #F1F0EC (out of scope;
never text on hatch), `ink` #222428, `ink2` #4A4D55, `navy` #203045, agents neutral (A umber #7A5230 outline, B slate
#3D5566 fill, told apart by letter and shape); depth ramp L0 #8FB5E0, L1 #5B8FCB, L2 #0F5FA8, L3 #0B4A86. Imagery:
nearest-neighbour integer upscaling only, ≥ 300 ppi; true colour B04/B03/B02 = grid / 10 000, one linear 1 to 99 %
stretch over all three bands, γ 1/1.35, identical everywhere; marks 1.4 mm stroke over a 2.4 mm white halo, the wrong
pixel also dashed 2.2/1.2 mm. Every caption is generated from the data file it cites.

### F1 · Header scene: the record this board follows (216.5 × 188 mm incl. bleed)

- Claim: the board follows one real, signed observation at native resolution.
- Data: `research/repro/data/keylong_B0{2,3,4}.bin` (EMEMGRD1, 443 × 453 px, EPSG:32643, first-pixel centre 688735 E /
  3607705 N, values DN − 1000); grid pixel (212, 225) = COG pixel (9443, 9098) (report 06 §0.1).
- Encoding: all 443 columns, rows chosen so row 212 sits at 60 % of the height; ×n nearest-neighbour; cited cell in a
  white 6 mm box with a thin leader to the strip; VIEW THE DEMO tile top-right.
- Stunning: the Lahaul valley at true 10 m, the river and the terraces sharp as squares; nothing interpolated; the same
  pixel reappears in F2, F5 and F7 so the eye travels with it.
- Reuse: `research/v13/evidence/visual/proto_m15.py` (window-equality assert), `mock_layout.py` crop.

### F2 · The handoff spine (801 × 118 mm figure inside the 801 × 190 mm panel)

- Claim: only the reference gives B something to resolve; each check refuses a named class; nothing reaches the entity.
- Data: `research/repro/v11/out/mutation_matrix.json` `summary.{A,B,C,I}.{false_accepts,applicable}`, `meta.rule`,
  `meta.genuine_value`; snippets rendered by `mutation_suite.py`'s own A/B/C renderers for G0 (never typed);
  G2 strip from `research/repro/data/v8/results.json` and `research/v13/evidence/g2_handoff/qwen_trials.jsonl`;
  R5 mode: the R5 results file in `research/repro/v13/r5/` (keys `R5.<cond>.pooled.false_accept`).
- Encoding (x in mm inside the figure): Agent A 0 to 100 (the real 5 × 5 true-colour window, 50 mm, named pixel
  `emem` outline; glyph A; label) → lanes 108 to 312, four lanes (five in R5) 22 mm tall with 3 mm gaps, lane name 22 pt
  Bold and Mono snippet 15 to 17 pt; the EMEM lane on `emem-tint` with the token chip → relay 318 to 392, one `harm-tint`
  bar across all lanes with an 8 mm diamond per lane and the family list → Agent B 400 to 600, per lane what B does;
  in the EMEM lane seven depth-ramp chips with layer tags → outcomes 606 to 690, right-aligned 64 pt Bold numerals,
  `harm` for 15 / 15, 15 / 15, 13 / 16 and `emem` for 0 / 16 → wall 698 to 801, hatched, white plate with the three
  unreachable items; TRY A TOKEN QR (40 mm symbol, 50 mm box) below the plate inside the wall column.
- R5 mode: each numeral becomes k / n in 64 pt with a 6 mm ghost square of the R1 ceiling beside it; add the RAG lane;
  the EMEM lane shows E with two small ticks for E0 and E+ (k / n in 17 pt).
- Annotations: the agent-level strip (running text) sits under lanes 1 to 2; the scope line under lanes 4 to 5.
- Stunning: one horizontal sentence of the experiment, readable from 3 m as colour (four vermillion numerals and one
  blue zero ending against a grey wall); the real pixel at the left anchors it in the physical world.
- Asserts: numerals equal the JSON; the RAG lane is absent unless R5 rows exist; snippets come from the renderer.
- Reuse: `fig_mutation` data loading (`make_figures_v12.py:122`), mock geometry (`mock_layout.py`).

### F3 · Eight answers to one question (193.5 × 62 mm)

- Claim: one pixel and one question yield eight values from real mechanisms; six cross the decision line, one is
  impossible, one is right, and each wrong one needs a different check.
- Data: `pixel_check.json` (0.4709, 0.3016), `cell_products.json` (0.4237), `ask_keylong.json` (0.2824),
  `results.json` arm R (0.47), `research/repro/v13/eight_answers.json` (0.4370, 0.2966, 1.1427; build from a committed
  rasterio script over Element84 and Planetary Computer COGs, values as report 05 §4.2/§6).
- Encoding: one horizontal number line 0.25 to 1.15 (break the axis between 0.55 and 1.10 with a 3 mm gap so the
  impossible value sits at the right edge); the rule as a vertical `ink` line at 0.4705 with "irrigate ←" left of it;
  8 dots, 6 mm, filled for signed records and archive reads, hollow for rule-or-arithmetic values; dot colour `emem`
  for the right value, `harm` for the six wrong ones, `oos` for the impossible one; labels staggered on two baselines
  above and below with leaders; each wrong dot carries its check chip (depth-ramp tint by layer).
- Stunning: a single line that turns "0.47 is close enough" into eight distinct physical stories, with the decision
  boundary cutting through them.
- Asserts: values recomputed from DNs equal the files to 1e-12; the 0.4705 line position from `meta.rule`.

### F4 · Our own errors name the checks: the failure ladder (193.5 × 262 mm)

- Claim: the errors an evidence system made are generic classes; signatures prevented none; each became checkable at a
  named layer, and the top one at none.
- Data: claims rows `F.*` (sources: `results.json`, `rawband/trials.jsonl`, `ask_keylong.json`, `contra_bengaluru.json`,
  `e84_keylong.json`, `CHANGELOG_18adb67.md:53, :47`, `prevalence_summary.json`, emem commit `0edf574`,
  `refusal_matrix.json`, external sources listed in the rows).
- Encoding: eight rungs, 30 mm tall, bottom (rung 1, caught at handoff by resolving) to top (rung 8, caught by
  nothing), so height = depth of check survived; the rung's left 3 mm bar is `incident` amber (every rung is a real
  incident); the check chip on the right uses the depth ramp and climbs in colour with the rung (L0 light to L3 dark);
  rung 8's chip is hatched `oos`; status tags 14 pt `ink2` in a small rounded box; consequence in 20 pt Bold `harm-text`;
  the outside source in 14 pt Regular `ink2` (no italics; weight carries hierarchy); a vertical side rail
  at x 178 to 193 carries the "check protects only if it runs" text rotated 90°.
- Stunning: a ladder that visibly rhymes with F8 (same rung colours), so the viewer sees that the most dangerous
  failures are the ones that pass the most checks; the hair salon at the top is the line people repeat.
- Asserts: every consequence string equals a claims row; status tags from the claims rows' notes; no row without an
  outside source.
- Reuse: report 06 §6.12 spec; report 05 §5 poster table; report 11 §3.

### F5 · What is handed over: the evidence object, exploded (396 × 98 mm)

- Claim: the address names EMEM's record, not the satellite file; the record names the file and pixel without hashing
  them; a batch signature covers such addresses.
- Data: the real record `research/repro/v8/proof_bundle_ndvi.cbor` `entry.facts[0]` (1,115 B; decode with cbor2, never
  re-encode), `research/repro/data/v8/cog_pixel_bytes.json`, `pixel_check.json`, `token_counts.json`.
- Encoding: four boxes left to right with 2.4 mm arrows: (1) SOURCE FILES, dashed outline (named, not hashed), two
  real B08/B04 thumbnails from the grids in grey; (2) RECORD, solid `emem` outline, the 12 fields as a two-column Mono
  list with actual values (`kind primary · cell defi.zb572.xoso.zb1ec · band indices.ndvi · tslot 20721 (25 Sep) ·
  value 0.4708994708994709 · confidence 0.95 · sources sentinel_s2_l2a, two COG URLs, captured 2026-09-25T05:42:51Z ·
  derivation sentinel2_l2a_indices_ndvi@1, scene S2A_MSIL2A_20260925T054251_R005_T43SFS, EPSG 32643, DNs 3502 / 1900,
  offset −1000 · privacy public · schema d24rgwlq… · signer 777er3yi… · signed 2026-09-28T09:06:56Z`), tags beside
  fields; (3) ADDRESS, `emem` fill, the 52-character cid in white Mono 17 pt; (4) ATTESTATION + LOG; under all, the full
  token in Mono 18 pt with its cost.
- Stunning: the dashed edge from file to record is the whole MASTER §5 distinction drawn in one line; real bytes, not a
  schema.
- Asserts: field values decoded from the CBOR; BLAKE3 of the bytes equals the cid; no signature field exists in the
  record (assert absent).
- Reuse: demo build `research/v13/evidence/demo_site/build/site.mjs` (`/r/` page field table) for the field list.

### F6 · Which check stops which corruption: the mutation matrix (396 × 196 mm)

- Claim: each corruption is stopped by a specific check; removing any of E to I lets a named one through; the entity
  passes everything.
- Data: `mutation_matrix.json` `rows`, `meta.mutations[].{family,first_protected_level,real_case}`, `leave_one_out`,
  `summary[*].decision_flips`; probes `research/v13/evidence/ladder/r1_t2_extra_out.json` for the scope line; R5 cells
  `R5.cell.<cond>.<item>.false_accept`.
- Encoding: rows grouped by MASTER §9 family with 2 mm group gaps: value (M1, M2, M8) · cell (M4, M9) · time (M10) · band
  (M6) · source (M11) · derivation (M12, M14) · stale / current (M5, M16) · signature / id (M3, M7, M13) · source pixel
  (M15) · hatched separator · entity (M17); control G0 as a thin top row. Row height 8.2 mm, id label 15 pt Mono with an
  amber ring for production-seen ids (M2, M4, M5, M15, M17 per `meta.mutations[].real_case`). Columns 44 mm: prose · JSON
  · [RAG] · opaque id · EMEM full check; cells are glyph squares (`harm` acted on corrupted evidence; #EEF3FA unaffected;
  `emem` refused; #F2F2F0 with "n/a"); then a 22 mm "first check" column with the letter in its depth-ramp chip and a
  1.4 mm ring when the leave-one-out names it as the only stop (E for M4 to M6, F for M9 to M12, G for M16, H for M14,
  I for M15); then a 16 mm "flips" tick column (M2, M8, M12, M13, M14, M15). Totals row in 30 pt Bold. In R5 mode: each
  cell is a horizontal bar whose length is the agents' rate (k / n printed at 14 pt) with the R1 verdict as a 3 mm
  square at its left edge.
- Stunning: at 3 m it reads as a vermillion block giving way to a blue staircase; at 1 m the rings show exactly which
  check earns its place; it is a table you can read, not a heat map.
- Asserts: totals equal `summary`; rings equal `leave_one_out`; no RAG column without R5; M11's fictitious scene id is
  never printed.
- Reuse: `fig_mutation` (`make_figures_v12.py:122-199`), regrouped.

### F7 · The right record, the wrong pixel (396 × 128 mm)

- Claim: a valid signature preserved a wrong measurement; only the re-read refuses it; the error was common.
- Data: grids `keylong_B0{2,3,4,8}.bin`; `pixel_windows.json` (5 × 5 DNs); `pixel_check.json`; `prevalence_summary.json`
  `pre`, `post`, `abs_err_index_where_differ`; `research/v13/evidence/critic/kx.json` (the real pre-fix record);
  `rondonia_floor_round_v2.json` for the scope line.
- Encoding: (a) 118 × 121 mm the 4.43 km scene, nearest-neighbour, white 250 m box, 1 km bar; (b) 112 × 112 mm the
  5 × 5 window in true colour, each 10 m pixel 22.4 mm, NDVI printed per pixel (17 pt, 2 decimals, ink or white by
  luminance), named pixel solid `emem`, the pixel 10 m south dashed `harm`, connectors from (a); (c) 150 mm wide: the two
  decisions in 30 pt, the chip row (five tinted `harm-tint` chips "pass the wrong value", one `emem` chip "refuses"),
  a 200-square waffle (20 × 10, 4 mm squares, 162 `harm`, 38 #EEF3FA, legend), the error distribution as a single
  strip plot of the 121 index errors with median and p90 ticks, and the real-record line.
- Stunning: real Sentinel-2 pixels at 10 m, two outlines one square apart, and a waffle that shows the scale at a glance;
  a viewer can count the squares.
- Asserts: the window equals the committed DNs minus 1000; floor vs round pixels from `pixel_check.json`; 162 + 38 = 200.
- Reuse: `research/v13/evidence/visual/proto_m15.py` (built and asserted), `fig_m15` labels.

### F8 · Checks stop at the source: the two-sided ladder (193.5 × 138 mm)

- Claim: L0 to L2 are checkable or recomputable, L3 is partial, L4 and L5 are not established by any reference.
- Data: `eo_evidence_per_fact_checks.csv` (`verified`, `recompute`), `cell_keylong.json` (source hashes),
  `refusal_matrix.json` (409), `mutation_matrix.json` (M17), JRC146622 line 236.
- Encoding: six rungs of 22 mm, L0 at the bottom; left plate (white, 70 mm) holds layer, name and status word in caps
  at +8 % tracking; right part is filled with the depth ramp for L0 to L2, half ramp half hatch for L3, hatch for L4 and
  L5; evidence text on a white plate; the grey "still trusted" line under each of L0 to L3 in 14 pt.
- Stunning: the colour drains as the ladder climbs toward the world: the boundary of the claim is a visible edge.
- Asserts: counts from the CSV; status words from the claims vocabulary.
- Reuse: report 10 §3.2 and §3.6; report 07 §3.4 residual-trust column.
- v13.2: the board draws F8 compact, 193.5 × 60 mm (`python poster/figs_v13/f8_ladder.py --height 60`; the default
  stays 138): one row per rung with the badge, name (16 pt) and status word (14 pt) on the left plate and one 14 pt
  evidence line on the right; L4 and L5 take two lines; the "still trusted" lines and the 409 are not printed.
  Running the script without `--height` restores the 138 mm figure and the right column no longer fits.

### F15b · SAT-042 as a compact strip (193.5 × 60 mm; v13.2, panel 11)

- Claim: the harness refuses a write with no trace and a smuggled fact, admits an honest batch, scores it against the
  drift anchor after admission, and names a rewritten log segment.
- Data: `research/repro/v12/trace/sat042_run_stdout.txt` (every value parsed, readers shared with F15 in
  `poster/figs_v13/sat042_data.py`), `trace_truth.md` (anchor, tampered segment), `repro/v10/algorithms.md` §15.
- Encoding: row (a) seven chips, name in 14 pt Medium over a verdict band (emem tint ENROLLED, SIGNED, ADMITTED; harm
  tint REFUSED, CAUGHT; incident SCORED); row (b) the eight layers as boxes with `seq k` in mono, seq 2 in harm tint with
  the 2 to 3 link crossed; row (c) the verdict bands 0 to 0.5 / 0.75 / 1 and the three scores as dots on a number line,
  each labelled `device → score`.
- Asserts: the shared readers' asserts, chip and caption widths, every printed number in its A15.* row.

### F9 · Memory keeps what was cited: branching timeline (193.5 × 82 mm)

- Claim: a newer record does not overwrite the cited one; an as-of question returns what was known then.
- Data: `contra_bengaluru.json` (attestations, `signed_at`, `value`); `cell_products.json` (Keylong 30 Sep record);
  the as-of answers recomputed from the attestations (as `make_figures_v12.py:506-510`).
- Encoding: pictorial first: a single "address" node at the left; a transaction-time axis 1 May to 30 Sep; record 1 as a
  bar from 28 May to the right edge (it never ends), record 2 from 11 Aug with 7 ticks; four vertical as-of probes that
  stop below the labels (fixes review F27), the 15 Jun probe in `harm` dashes with its question; a 20 mm second strip
  for Keylong valid time: 25 Sep (cited, blue) and 30 Sep (newer, grey), with "the cited reference still re-hashes".
- Stunning: the picture of a branching memory, not a table of versions; the viewer sees history persist.
- Asserts: as-of answers equal the recomputation; no label crossed by a probe.
- Reuse: `fig_bitemporal` (`make_figures_v12.py:493`), redrawn.

### F10 · What it costs: two aligned log strips (193.5 × 50 mm)

- Claim: record checks are sub-millisecond; the source re-read is four orders of magnitude dearer and the only check
  that refuses the wrong pixel; the reference is not where the tokens go.
- Data: `research/v13/cost_measurements.json` (`m2…primitives_us.blake3_fact_1115B`, `m2…by_level.I`,
  `m2…in_process_precompiled_exec_ms`, `m1…warm/cold`, `m3…links 8, 9, 9b`, `m5_tokens.items.*`).
- Encoding: strip 1, time per check on a log axis 1 µs to 10 s, one row per item, dot plus label at the dot; the re-read
  row's dot in `emem` dark with "M15" beside it; strip 2, tokens on a log axis 1 to 100 000, value, reference, record as
  JSON, 18-tool MCP list.
- Stunning: one look shows the cheap cluster and the lone expensive dot that matters.
- Asserts: every value from the JSON with its date; tokenizer named.

### F11 · Ecosystem bridge and same-token dot plot (531 × 100 mm)

- Claim: one evidence protocol carries the same reference through many runtimes; each surface is labelled by evidence.
- Data: `research/v13/ecosystem_manifest.json` rows with `print.allowed == true` and status in {LIVE, PROTOCOL, REGISTRY,
  EXAMPLE}; conditional rows per the claims map; `crossruntime_table.json` `rows.ndvi_keylong[*].ms_median`.
- Encoding: (1) bridge, four nodes with 2.4 mm arrows, the first in `emem` fill with the token chip; (2) five groups in
  poster type, each name with a drawn status glyph (4 mm: filled circle, open circle, open square, open triangle);
  at most two marks, GitHub black Invertocat beside the repo name and Dify mono, nothing else; (3) right 165 × 90 mm the
  ten-path dot plot, one row per path, median on a log axis 30 ms to 2 s, every dot `emem` because every path returned
  the same address and value; the A→B process row drawn hollow with "one run".
- Stunning: an architecture, not a logo wall: the eye follows the record from the protocol into named hosts.
- Asserts: no printed name without a manifest row; glyph from `status`; `verified_utc` within 14 days of the build.

### F12 · EMEM relies on these layers (261 × 48 mm)

- Claim: adjacent systems answer other questions; EMEM answers whether this is the observation the sender cited.
- Data: report 04 §1.2 (each label sourced there).
- Encoding: seven 6 mm lanes, verb in caps, system, unit; a 1.8 mm `emem` thread at the right touching FIND, RUN, CARRY
  and JUDGE with three verbs (cite, hand off, resolve · re-hash · re-read); no ticks or crosses.
- Stunning: a quiet stack with one blue thread through it; it says complementary without a word of comparison.

Small typographic diagrams (no data plots): D1 threat channel (193.5 × 30 mm), D2 Rondônia lattice (193.5 × 56 mm; shape
and colour coded points from `case_rondonia_eudr.json`: flag `harm` 7 mm disc, forest `emem` disc, cleared ink triangle,
non-forest grey dot, disagreement amber diamond; reuse `fig_rondonia`), D4 two vector cards (193.5 × 24 mm; from
`research/v13/evidence/critic/cell.json`).

Dropped from v12 (keep in `/methods/` only): `failure.svg`, `eo_berlin.svg`, `eo_keylong.svg` as a panel, `encoding.svg`,
`model.svg`, `drift.svg`, `score.svg`, `sat042.svg`.

---

## F. QR set and the Pages site

All six: ECC Q, version 4 (33 modules), 4-module quiet zone, black on white, vector SVG; payloads short paths on the
poster's own Pages site so a target can be fixed after print (report 09 §2). Generator:
`research/v13/evidence/visual/qr/make_qr.py`.

| CTA (Mono Bold) | printed caption | payload | final target | symbol | placement |
|---|---|---|---|---|---|
| VIEW THE DEMO | Your phone is Agent B: a paraphrase passes unchecked; three corruptions are refused. | `https://vortx-ai.github.io/esa_poster/demo/` | the static receiver demo (report 09 §3) | 70 mm | header image tile, x 734 to 821, y 13 to 100 |
| TRY A TOKEN | Resolve the Keylong token on emem.dev, then paste your own. | `https://vortx-ai.github.io/esa_poster/t/` | `https://emem.dev/verify?q=emem%3Afact%3Adefi.zb572.xoso.zb1ec%3Aoj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` | 40 mm | spine, under the wall plate, x 728 to 778, y 326 to 376 |
| INSPECT THE RECORD | The 1,115 bytes behind the main example, decoded. | `https://vortx-ai.github.io/esa_poster/r/` | the record page; it also links this board's own signed record when the authors seal it | 40 mm | panel 4, right edge, x 568 to 618, y 400 to 450 |
| RE-RUN THE TEST | Data and scripts behind this board's numbers, with one re-run command. | `https://vortx-ai.github.io/esa_poster/test/` | `https://github.com/Vortx-AI/esa_poster/tree/main/research/repro/v13` | 40 mm | panel 5, bottom right, x 568 to 618, y 764 to 814 |
| DISCOVER INTEGRATIONS | Where EMEM runs today, each surface labelled by evidence. | `https://vortx-ai.github.io/esa_poster/use/` | the integrations page generated from the manifest | 40 mm | panel 12, top right, x 497 to 547, y 1030 to 1080 |
| READ THE METHODS | Definitions, denominators, models, and what our own tools generated. | `https://vortx-ai.github.io/esa_poster/methods/` | `https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v13/METHODS.md` | 40 mm | conclusion block, x 768 to 818, y 1116 to 1166 |

"INSPECT THE RECORD" and the board's signed record: the `/r/` page shows the hero record's fields, bytes and checks. If
the authors seal the printed board (render, board pointer, track, sign with the poster key), `/r/` adds one button,
"Check this board's own record: your phone re-hashes the records behind its numbers and checks the public log", opening
the track in ememdemo. The track must be rebuilt without the cell step that calls `POST /v1/recall` (report 09 d05); the
page states what it checks (the published digital board, its order and log position) and does not narrate history.

Pages site map (`docs/`, GitHub Pages source `main` → `/docs`, with `.nojekyll`):

```
docs/index.html            landing: hero sentence, title, session, the six CTAs in the board's words, media link
docs/demo/index.html       receiver demo: prose accepted unchecked; M3, M4, M8 refused; G0 accepted at L0 to L2; live L3 pixel re-read; L4/L5 boundary
docs/demo/transcript.txt   text fallback written by the same build (verdicts asserted)
docs/r/index.html          INSPECT THE RECORD: field table, 1,115-byte hex, checks, "named, not hashed", optional sealed-board button
docs/use/index.html        DISCOVER INTEGRATIONS: manifest rows with print.allowed, status chips, the 11-path table, refusal row
docs/t/index.html          redirect to emem.dev/verify?q=<Keylong token>
docs/test/index.html       redirect to github.com/Vortx-AI/esa_poster/tree/main/research/repro/v13
docs/methods/index.html    redirect to …/blob/main/research/repro/v13/METHODS.md
docs/media/                A0 PDF, 300 dpi PNG, 16:9 slide, 20 s video, social card, A4 handout, manifest.json
```

Source of the built site: `research/v13/evidence/demo_site/` (build scripts in `build/`, built pages in `site/`); copy
the scripts to `poster/demo_src/` and build with `node poster/demo_src/build.mjs . docs/demo && node
poster/demo_src/site.mjs . docs`. Targets that must exist on `main` before the QRs are drawn:
`research/repro/v13/README.md` (one re-run command and its expected output) and `research/repro/v13/METHODS.md`
(definitions, denominators, models, the full token-family table, formulas, SAT-042, the sealed-board explanation).

---

## G. Build checklist and gates

Write `poster/build_v13.py` (from `build_v12.py`), `poster/make_figures_v13.py`, `poster/src/poster.v13.html`. Every gate
fails the build; an unknown result is a failure.

1. **Page fit.** One PDF page, 841 × 1189 mm ± 0.5 mm; every block box inside its section B rectangle ± 1 mm; content
   ends ≥ 2 mm above the footer; no box crosses the page edge except the header bleed; `overflow:hidden` is not
   allowed to hide a box (check each box against its parent).
2. **Type floor.** No text below 14 pt in CSS or SVG; running body ≥ 24 pt for kicker, mechanism and take lines;
   captions ≥ 17 pt; three-column headlines ≤ 30 characters at 32 pt; six-column ≤ 50 at 40 pt; every printed code point
   present in the face that sets it (complete Plex; status glyphs drawn).
3. **Banned words** in HTML and figure text (`labels.json`): em dash; en dash anywhere; the v12 tell words; first, only,
   unique, novel, never, always, every, all, any, none (pass only when followed by a count or allowlisted), truth, true
   (about a value), guarantee*, prove*, proof (except inclusion/consistency/Merkle proof), certain, trustless, secure,
   immutable, tamper-proof, decides, arbiter, "the satellite", verify/verified/verifies/verification without a layer tag
   (title exempt; the ladder line "Never \"verified\" without its layer." allowlisted), spacecraft/onboard/in orbit
   outside the footer extension line, compliant/compliance/due diligence, "hash of (its|the) (bytes|pixel|file|scene)".
   Allowlist entries in the claims map are bound to the sentence by BLAKE3 of the normalised text (report 10 §5.3).
   The allowlist this text needs, each with its evidence row: "only" in the spine strip (S.G2.boundary), the threat
   model, panel 5, H2 and panel 11 (X.only), the panel 3 rail (F.rail.cellmatch, F.rail.langchain); "every" in
   "passes every check" and "every check but the re-read" (X.entity, X.loo); "none" in panel 3 and the conclusion
   (F.caption, S.R1.I); "all" in "all valid" and "all 24" (F.thing, S.G2.qwen.bare); "first" in
   "first check that refuses" and "first signed 11 Aug" (non-novelty uses; X.loo, TM.915); "never" in the control row
   (S.R1.I `genuine_refused` false); "true" in "true colour" (H.img.grid); "unverifiable" in RQ4 and "verified" in the
   ladder line (L.status); "only" in "only a path and year" (V.tessera), "re-read only" (F.pixel), "the only check that
   stops it" (X.only) and "shown only to B" (M16's definition, X.loo); "never" in "never tested" (F.rail.cellmatch);
   "everything else" (O.84); "every path" (EC.11); "All keys" (T.oneop); "all offline checks" (C.cpu); "truth" only as the
   L5 layer name "L5 physical truth, decision" (MASTER §11); "verification" in the MAST quote (F.rail.mast) and the
   mandated extension line (K.sat042); "Verifiable" in the title (H.title).
4. **Claims coverage.** Every number in HTML and figure text, and every sentence in `<main>`/`<header>`, belongs to a
   `data-claim` element whose id is a row of `research/v13/12_claims_map.json`; the printed substring equals one of the
   row's `print[]` strings; each row with a `check` re-runs and passes; LIVE rows older than 7 days are re-fetched or the
   build fails; ecosystem rows older than 14 days fail; rows with date `pending` may print only in R5 mode; rows marked
   CONDITIONAL print only when their condition file exists (ChatGPT screenshot in `research/v13/`, fixed example
   commits). "fact_cid", "address" or "token" within one sentence of pixel, scene, file or satellite requires "record" in
   that sentence. R1 numbers carry the suite bound ("in our suite", "of 16").
5. **QR decode.** Rasterise each QR at print size and 300 dpi, decode with OpenCV, compare with the payload; then follow
   every payload's redirects to HTTP 200 `text/html` without sign-in at 390 × 844 with the POST safety rule of report 09;
   record a real-phone test (one iPhone Safari 16.4+, one Android Chrome) with date and device in
   `docs/media/manifest.json`.
6. **Figure labels.** `check_text` (no text below 14 pt, none clipped, no glyph-core overlap) extended to text versus
   lines and patches (review F27); no text on hatch; every label in `labels.json` maps to a claim id.
7. **Colour.** Every hex comes from `poster/src/tokens.json`; re-run `research/v13/evidence/visual/palette_check.py`
   (CVD Machado 2009 at severity 100 for protan, deutan, tritan; the four state colours keep ΔE00 ≥ 17 pairwise; blue vs
   vermillion passes the validator); FOGRA39 round trip ΔE00 < 2 for fills; text K-only; fills ≤ 300 % TAC; render a
   deuteranopia simulation of the whole board PNG and check the matrix and M15 still read by shape and pattern.
8. **Imagery.** Integer nearest-neighbour upscaling; ≥ 300 ppi at print size; window-equality assert before drawing;
   processing line printed under each image.
9. **Word budget.** Running text ≤ 820 words containing a letter (≤ 870 tokens with numerals; this brief: 807 / 853); per-panel counts of section C ± 10 %; figure text reported in the build log.
10. **Experiment mode.** If the R5 results file in `research/repro/v13/r5/` exists and its prereg BLAKE3 matches the hash pushed
    before trial 1, build R5 mode; otherwise build fallback mode with every R1 line labelled "deterministic receiver,
    no model". A partial R5 file (planned denominators not met) prints achieved n beside planned n.
11. **Media and history.** No version numbers, "v12", defect ids, "withdrawn", scorecards or `research/should_do` paths on
    the face; the PDF `<title>` is the programme title.
12. **Reproducibility.** `research/repro/v13/` exists on `main` with README and METHODS; the claims map, the build log
    and figure label dumps are build products committed with the PDF.

---

## H. Open items only the authors can resolve, and how the brief degrades

| # | item | why only the authors | degrade if unresolved |
|---|---|---|---|
| 1 | R5 is running in `research/repro/v13/r5/` (plan files on 1 Oct: haiku 4.5, sonnet 5.5, opus 5.5 and Qwen2.5-7B). Decide whether to add Fable 5.1 (about $85) or Tier-3 open models; AWS/GCP credentials need explicit permission | spend and credentials | fallback mode: R1 numerals and the G2 strip; RAG lane and RQ3's retrieval clause off; the conclusion keeps "in our suite" |
| 2 | ChatGPT: a logged-in, dated phone screenshot of the @emem directory entry committed to `research/v13/` | needs an account | ChatGPT appears only in "Not run by us"; no glyph in the band |
| 3 | Organisers: board size, orientation, mounting, Wi-Fi/screen (email paper@agentic-eo.berlin) | author correspondence | layout assumes A0 portrait; if landscape or smaller, the brief must be re-composed, not scaled |
| 4 | Print shop colour condition (sRGB inkjet vs PDF/X-4 FOGRA39/51) and deadline (about 10 Oct) | vendor contact | export sRGB PDF plus a FOGRA39 soft-proof |
| 5 | Enable GitHub Pages (`main` → `/docs`), add a LICENSE (code Apache-2.0, poster and media CC BY 4.0), merge to `main` | repository owner | all six QRs fail gate 5; the board cannot print with QRs |
| 6 | Zenodo DOI metadata (title "emem: A research on …", duplicated surname) and the accepted abstract committed to the repo | record owner | no DOI on the board; title check against the programme only |
| 7 | Seal the printed board with the poster key (rebuilt track without the recall step) | signing step | `/r/` shows the hero record only; no sealed-board button |
| 8 | Ask emem's maintainers to fix before 19 Oct: README:246 and `docs/model.md` wording; the date substitution (`band_raster`); the ask coordinates path; the Gemini, Cline, LangChain and Semantic Kernel routes; `llms.txt` cid rule in ememdemo | emem changes | the board prints "open" and "fix unconfirmed" tags as now; LangChain, Agno, Cline stay off the band; footer says the code is printed where docs differ |
| 9 | Record the 60 s narration (no synthetic voice presented as a person) | a person's voice | the media pack ships the 20 s silent demo only |
| 10 | Independent re-run of RE-RUN THE TEST by one person outside Vortx (date, OS, output hash) | needs an outsider | no "replicated by" line; methods states no outside run exists |
| 11 | Confirm keeping the email address on the byline | personal data | byline without the email |

Build-team items (not author decisions, but print-blocking): materialise `eight_answers.json`; the rawband erratum;
re-fetch LIVE rows within 7 days of print; re-verify manifest rows within 14 days; re-measure resolve and re-read from
an ordinary network if time allows (otherwise keep "through our TLS proxy").

---

## Appendix I. Claims-map generator and word counter (as run on 2026-10-01)

Save as `research/repro/v13/claims/claims.py` and `count_words.py`. `python claims.py` rewrites `research/v13/12_claims_map.json` and prints `212 rows; 97 auto-checked pass; 0 fail` today.

```python
"""Generate research/v13/12_claims_map.json and the markdown table for 12_FINAL_BRIEF.md section D.
Every row is checked against its source where the source is a committed machine-readable file.
"""
import csv, json, re, sys
from collections import Counter
from pathlib import Path

REPO = Path("/home/user/esa_poster")
R = REPO / "research"
OUT_JSON = R / "v13" / "12_claims_map.json"
OUT_MD = Path(__file__).with_name("claims_table.md")

def J(p):
    return json.load(open(R / p))

def ptr(obj, path):
    for k in path:
        obj = obj[k]
    return obj

rows = []
def row(id, block, prints, status, layer, source, date, value=None, check=None, note="", tier="1m", fallback=None, r5=None):
    rows.append(dict(id=id, block=block, print=prints if isinstance(prints, list) else [prints], status=status,
                     layer=layer, source=source, date=date, value=value, check=check, note=note, tier=tier,
                     fallback=fallback, r5_key=r5))

MM = "repro/v11/out/mutation_matrix.json"
PX = "repro/data/v8/pixel_check.json"
PV = "repro/data/v8/prevalence_summary.json"
TK = "repro/data/v8/token_counts.json"
XR = "repro/data/v8/crossruntime_table.json"
G2 = "repro/data/v8/results.json"
QW = "v13/evidence/g2_handoff/qwen_trials.jsonl"
CM = "v13/cost_measurements.json"
BG = "repro/data/contra_bengaluru.json"
RO = "repro/v12/data/case_rondonia_eudr.json"
EV = "repro/v12/data/eo_evidence_per_fact_checks.csv"
CK = "research/v13/evidence/critic/cell.json"   # 209 facts, 215 sources, 2026-10-01T01:41Z (was repro/data/v11/cell_keylong.json, 213)
CP = "repro/data/v11/cell_products.json"
AK = "repro/data/v11/ask_keylong.json"
CL = "v13/evidence/failure_modes/CHANGELOG_18adb67.md"
EM = "v13/ecosystem_manifest.json"
CC = "v13/evidence/critic/cell.json"
RB = "repro/data/v9/rawband/trials.jsonl"
D_R1 = "2026-09-30"  # R1 run committed (summary.md); deterministic, re-runnable

# ---------------- header ----------------
row("H.title", "header", "EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings",
    "LIVE", "n/a", {"file": "research/v13/evidence/industry/prog_posters.txt", "line": 42, "url": "https://agentic-eo.berlin/programme/posters/"},
    "2026-10-01", check=("grep", "v13/evidence/industry/prog_posters.txt", "EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings"),
    note="programme title verbatim; re-check the week of print", tier="3m")
row("H.session", "header", ["Poster Session 1", "19 Oct 2026"], "LIVE", "n/a",
    {"file": "research/v13/evidence/industry/prog_posters.txt", "url": "https://agentic-eo.berlin/programme/posters/"}, "2026-10-01",
    note="EMEM is the 4th entry of Session 1 (report 04 sec. 4.2); print only 'Poster Session 1 · 19 Oct 2026' for the date (site gives 19-20 and 19-21 Oct)")
row("H.hero", "header", "Agents hand each other evidence references, not paraphrases.", "SPEC", "n/a",
    {"file": "research/v13/10_ladder_threat_invention.md", "section": "1.1 invention statement"}, "2026-10-01",
    note="mechanism statement; the measured support is S.* and M.* rows", tier="3m")
row("H.sub.mechanism", "header", "The receiver resolves the reference, re-hashes the record, re-reads the source.", "MEASURED", "L0-L3",
    {"file": "research/repro/v11/out/summary.md", "pointer": "levels C, D, I"}, D_R1, tier="3m")
row("H.sub.boundary", "header", "A signature fixes the record's bytes, not the measurement.", "OUT-OF-SCOPE", "L5",
    {"file": PX, "example": "M15: signed 0.3444 vs containing pixel 0.4860 (kxjvfwpa)"}, "2026-10-01", tier="3m")
row("H.img.record", "header", ["NDVI 0.4709", "Sentinel-2A L2A", "Keylong, Lahaul, India", "25 Sep 2026"], "MEASURED", "L1",
    {"file": PX, "pointer": ["S2A 2026-09-25 (now, fact oj5cecci, signed 2026-09-28T09:06Z = post-fix)", "ndvi_floor_pixel"]}, "2026-09-25",
    value=0.4708994708994709, check=("json", PX, ["S2A 2026-09-25 (now, fact oj5cecci, signed 2026-09-28T09:06Z = post-fix)", "ndvi_floor_pixel"], 0.4708994708994709))
row("H.img.grid", "header", ["signed 10 m grids", "B04/B03/B02", "linear 1 to 99 % stretch, γ 1/1.35"], "MEASURED", "L3",
    {"file": "research/repro/data/keylong_B0{2,3,4}.bin", "note": "EMEMGRD1 443 x 453 px, EPSG:32643, values DN-1000; window equality asserted in research/v13/evidence/visual/proto_m15.py"},
    "2026-09-25", tier="30cm")

# ---------------- spine (R1 fallback + G2) ----------------
for lvl, txt, n, k in [("A", "15 / 15", 15, 15), ("B", "15 / 15", 15, 15), ("C", "13 / 16", 16, 13), ("I", "0 / 16", 16, 0)]:
    row(f"S.R1.{lvl}", "P1 spine + P5 matrix", txt, "MEASURED", {"A": "n/a", "B": "n/a", "C": "L0", "I": "L0-L3"}[lvl],
        {"file": MM, "pointer": ["summary", lvl, "false_accepts"], "denominator": ["summary", lvl, "applicable"]}, D_R1,
        value=f"{k}/{n}", check=("json", MM, ["summary", lvl, "false_accepts"], k), tier="3m",
        r5={"A": "R5.A.pooled.false_accept", "B": "R5.B.pooled.false_accept", "C": "R5.D.pooled.false_accept", "I": "R5.E.pooled.false_accept"}[lvl],
        note="R1 opaque id is R5 condition D; R1 level I is the ceiling for R5 condition E/E+")
row("S.headline", "P1 spine", "Handed prose, B acted on 15 of 15 corruptions; handed a reference it checks, on 0 of 16.", "MEASURED", "L0-L3",
    {"file": MM, "pointer": "summary.A, summary.I"}, D_R1, tier="3m",
    r5="R5 template: 'Handed prose, agents acted on {R5.A.pooled.false_accept} corruptions; handed a reference, on {R5.E.pooled.false_accept}.'")
row("S.16", "P1 spine", ["16 ways", "16 corruptions"], "MEASURED", "n/a", {"file": MM, "pointer": "meta.mutations minus G0 and M17"}, D_R1,
    value=16, check=("json", MM, ["summary", "I", "applicable"], 16))
row("S.threshold", "P1 spine + P2 + P6", ["0.4705", "irrigate if NDVI ≤ 0.4705"], "PRE-REGISTERED", "n/a",
    {"file": MM, "pointer": ["meta", "rule"], "prereg": "research/repro/data/v8/prereg.md (constructed boundary test)"}, "2026-09-30",
    check=("json", MM, ["meta", "rule"], "irrigate iff NDVI <= 0.4705"), note="must be labelled a constructed test rule wherever printed")
row("S.G2.haiku.F", "P1 spine", ["Claude Haiku 4.5 declined 5 of 5"], "PRE-REGISTERED", "L1",
    {"file": G2, "pointer": ["b", "claude-haiku-4-5", "arms", "F", "decisions", "DECLINE"], "prereg": "research/repro/data/v8/prereg.md blake3 67631a79..."},
    "2026-09-30", value="5/5", check=("json", G2, ["b", "claude-haiku-4-5", "arms", "F", "decisions", "DECLINE"], 5),
    note="the refusal came through the server's 409; the harness, not the model, re-hashed (review F3)")
row("S.G2.qwen.F", "P1 spine", ["Qwen2.5-3B", "acted 5 of 5"], "PRE-REGISTERED", "L1",
    {"file": QW, "pointer": "count(arm=F, decision=IRRIGATE)", "prereg": "research/v13/evidence/g2_handoff/prereg_addendum2.md"},
    "2026-09-30", value="5/5", check=("qwen", QW, ("F", "IRRIGATE"), 5), note="52 of 55 pre-registered trials ran; label in methods")
row("S.G2.qwen.bare", "P1 spine", "dropped the cell from all 24 calls", "PRE-REGISTERED", "L1",
    {"file": QW, "pointer": "count(tool_calls[].token_form == 'bare_cid') over arms T and F"}, "2026-09-30", value="24/24",
    check=("qwen_bare", QW, None, 24))
row("S.G2.boundary", "P1 spine", "a reference protects only a receiver that keeps it whole and obeys a refusal", "INFERRED", "L1",
    {"inputs": ["S.G2.haiku.F", "S.G2.qwen.F", "S.G2.qwen.bare"]}, "2026-10-01", note="'only' allowlisted with these three rows")
row("S.scope", "P1 spine", ["one record, one band, one run", "test key"], "MEASURED", "n/a", {"file": "research/repro/v11/out/summary.md", "pointer": "Notes"}, D_R1, tier="30cm")
row("S.boundary_wall", "P1 spine", ["the entity meant (M17)", "sensor accuracy", "the decision"], "OUT-OF-SCOPE", "L4-L5",
    {"file": MM, "pointer": ["summary", "I", "entity_case_accepted"]}, D_R1, check=("json", MM, ["summary", "I", "entity_case_accepted"], True))

# R5 placeholders (spine + matrix + caption); planned denominators from report 02 sec. 8-10
PLAN = {"A": 95, "B": 95, "C": 95, "D": 100, "E0": 100, "E": 100, "Eplus": 100}
for cond, n in PLAN.items():
    row(f"R5.{cond}.pooled", "P1 spine + P5 matrix", f"{{R5.{cond}.pooled.false_accept}}", "PRE-REGISTERED", "L0-L3",
        {"file": "research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build)", "pointer": f"primary.{cond}.pooled_claude.false_accept", "prereg": "research/repro/v13/r5/prereg.md (BLAKE3 pushed before trial 1)"},
        "pending", value=f"k/{n*3} planned (3 Claude models x {n}: haiku, sonnet, opus, as in the R5 plan files of 1 Oct); k/{n*4} if Fable 5.1 is added",
        note="print k/n with Wilson 95 % and models, n, dates; absent until results.json exists (fallback: R1 row)", r5=f"R5.{cond}.pooled.false_accept")
    for m in ("haiku", "sonnet", "opus", "fable"):
        row(f"R5.{cond}.{m}", "P5 matrix (30 cm per-model strip)", f"{{R5.{cond}.{m}.false_accept}}", "PRE-REGISTERED", "L0-L3",
            {"file": "research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build)", "pointer": f"primary.{cond}.{m}.false_accept"}, "pending",
            value=f"k/{n} planned", r5=f"R5.{cond}.{m}.false_accept", tier="30cm")
    row(f"R5.{cond}.qwen7b", "P5 matrix (30 cm)", f"{{R5.{cond}.qwen7b.false_accept}}", "PRE-REGISTERED", "L0-L3",
        {"file": "research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build)", "pointer": f"primary.{cond}.qwen7b.false_accept"}, "pending",
        value=f"k/{n // 5} planned (1 replicate; descriptive only)", r5=f"R5.{cond}.qwen7b.false_accept", tier="30cm")
for key, plan, txt in [("R5.cell.<cond>.<item>.false_accept", "k/15 per cell planned (5 reps x 3 Claude models)", "matrix cell bars"),
                       ("R5.G0.<cond>.pooled.false_refusal", "k/45 per condition planned (15 x 3)", "control row"),
                       ("R5.E0.pooled.verify_called", "k/100 per model", "E0 vs E line"),
                       ("R5.M15r.Eplugin.false_accept", "k/15 (5 x 3, Block 2)", "real pre-fix record, no re-read"),
                       ("R5.M15r.EpluginV.false_accept", "k/15 (5 x 3, Block 2)", "real pre-fix record, with re-read"),
                       ("R5.M20.E.pooled.false_accept", "k/15", "as-of case"),
                       ("R5.models", "3 Claude (haiku 4.5, sonnet 5.5, opus 5.5) + Qwen2.5-7B planned", "models line"),
                       ("R5.dates", "run dates", "scope line")]:
    row(key.replace("<", "").replace(">", ""), "P1/P5 (R5 mode only)", f"{{{key}}}", "PRE-REGISTERED", "L0-L3",
        {"file": "research/repro/v13/r5/results.json (name as written by the R5 scorer; bind at build)"}, "pending", value=plan, note=txt, r5=key, tier="30cm")

# ---------------- P2 eight answers ----------------
E8 = [("E8.right", "0.4709", "signed record oj5cecci (containing pixel, S2A R005)", "MEASURED", "L0", {"file": PX, "pointer": "S2A ... ndvi_floor_pixel"}, ("json", PX, ["S2A 2026-09-25 (now, fact oj5cecci, signed 2026-09-28T09:06Z = post-fix)", "ndvi_floor_pixel"], 0.4708994708994709)),
      ("E8.rounded", "0.47", "rounded in prose (G2 arm R: 5 of 5 IRRIGATE)", "PRE-REGISTERED", "L0", {"file": G2, "pointer": "b.claude-haiku-4-5.arms.R.decisions.IRRIGATE = 5 (exploratory addendum)"}, ("json", G2, ["b", "claude-haiku-4-5", "arms", "R", "decisions", "IRRIGATE"], 5)),
      ("E8.s2b", "0.4370", "S2B R105, same day, same tslot; Element84 DNs 1014/2588", "MEASURED", "L1", {"file": "research/repro/v13/eight_answers.json (to create; values from report 05 sec. 4.2, rasterio 1.4.4, 2026-10-01)"}, None),
      ("E8.newer", "0.4237", "30 Sep record 3yyaxn5d handed as 25 Sep", "LIVE", "L1", {"file": CP, "pointer": "band=indices.ndvi value"}, ("cp", CP, "indices.ndvi", 0.42369991474850816)),
      ("E8.neighbour", "0.3016", "old reader rule on this scene (pixel 10 m south)", "MEASURED", "L3", {"file": PX, "pointer": "S2A ... ndvi_round_pixel"}, ("json", PX, ["S2A 2026-09-25 (now, fact oj5cecci, signed 2026-09-28T09:06Z = post-fix)", "ndvi_round_pixel"], 0.3015512674990541)),
      ("E8.offset0", "0.2966", "DNs 3502/1900 read without the -1000 offset", "INFERRED", "L3", {"inputs": "pixel_check.json DNs", "formula": "(3502-1900)/(3502+1900)"}, ("calc", None, (3502 - 1900) / (3502 + 1900), 0.2966)),
      ("E8.place", "0.2824", "town point 597 m from the asked coordinates (30 Sep scene, p6ewjnlq)", "MEASURED", "L1", {"file": AK, "pointer": "answer fact p6ewjnlq value 0.28244274809160314"}, ("grep", AK, "0.28244274809160314")),
      ("E8.double", "1.1427", "Element84 DNs with Element84's declared -0.1 offset", "INFERRED", "L2", {"inputs": "E84 DNs 900/2502 (report 05 sec. 4.2) + raster:bands offset -0.1 (research/v13/evidence/failure_modes/e84_keylong.json)", "formula": "(0.2502-0.1 - (0.0900-0.1))/(0.2502-0.1 + 0.0900-0.1)"}, ("calc", None, ((0.2502 - 0.1) - (0.0900 - 0.1)) / ((0.2502 - 0.1) + (0.0900 - 0.1)), 1.1427))]
LABS = {'E8.right': '0.4709 signed record', 'E8.rounded': '0.47 rounded in prose', 'E8.s2b': '0.4370 other satellite, same day', 'E8.newer': '0.4237 30 Sep record handed as 25 Sep', 'E8.neighbour': '0.3016 neighbour pixel', 'E8.offset0': '0.2966 offset left out', 'E8.place': '0.2824 town point 597 m away (30 Sep)', 'E8.double': '1.1427 offset applied twice'}
for id, v, lab, st, ly, src, chk in E8:
    row(id, "P2 eight answers", [LABS[id]], st, ly, src, "2026-10-01", value=v, check=chk,
        note=lab + ("; hollow dot (rule or arithmetic on real DNs)" if st == "INFERRED" or id in ("E8.rounded", "E8.neighbour") else "; filled dot (a signed record or an archive read)"))
row("E8.summary", "P2 eight answers", "Six cross the irrigation line, one is impossible, one is right", "INFERRED", "n/a", {"inputs": [r[0] for r in E8]}, "2026-10-01")
row("E8.place_m", "P2 + P3", "597 m", "MEASURED", "L1", {"file": AK, "pointer": "located stage (32.5717891, 77.0281479) vs asked (32.57126, 77.03448)", "method": "pyproj Geod WGS84 inv: 597.49 m"}, "2026-10-01",
    check=("geod", None, (77.03448, 32.57126, 77.0281479, 32.5717891), 597))

# ---------------- P3 failures ----------------
row("F.lost", "P3", ["0.47 for 0.4709", "5 of 5 receivers irrigated"], "PRE-REGISTERED", "L0", {"file": G2, "pointer": "b.claude-haiku-4-5.arms.R.decisions.IRRIGATE"}, "2026-09-30",
    check=("json", G2, ["b", "claude-haiku-4-5", "arms", "R", "decisions", "IRRIGATE"], 5), note="exploratory addendum arm; constructed threshold")
row("F.lost.out", "P3", "Perez et al., ICLR 2025: LLM transmission chains drift", "EXTERNAL", "n/a", {"url": "https://arxiv.org/abs/2407.04503"}, "2026-10-01", tier="30cm")
row("F.date", "P3", ["asked 23 Sep, served 25 Sep", "10 of 10 agents saw one scene twice", "3 said no 23 Sep scene existed"], "PRE-REGISTERED", "L1",
    {"file": RB, "pointer": "result_text of all 10 trials (critic C1 recount); results.md:14 says 9 and needs an erratum", "prereg": "research/repro/data/v9/rawband/prereg.md blake3 30d8a1a1"},
    "2026-09-30", note="status at emem 8e9b401: open (no fix in CHANGELOG or code diff)")
row("F.date.out", "P3", "STAC item search defines no default order", "EXTERNAL", "n/a", {"file": "research/v13/evidence/failure_modes/item-search_README.md"}, "2026-10-01", tier="30cm")
row("F.place", "P3", ["coordinates given, town point answered", "597 m", "NDVI 0.28 for the field's 0.42"], "MEASURED", "L1",
    {"file": AK, "pointer": "located stage; answer value 0.28244", "field": CP + " indices.ndvi 0.4237 (same 30 Sep scene)"}, "2026-09-30", note="fix not confirmed at 8e9b401")
row("F.place.out", "P3", "GDAL 3 follows CRS axis order (RFC 73)", "EXTERNAL", "n/a", {"url": "https://gdal.org/development/rfc/rfc73_proj6_wkt2_srsbarn.html"}, "2026-10-01", tier="30cm")
row("F.version", "P3 + P8", ["918.0 m", "915.07 m", "one band name"], "MEASURED", "L1", {"file": BG, "pointer": "contradictions[0].attestations values"}, "2026-09-29",
    check=("bg_values", BG, None, {918.0: 1, 915.0712280273438: 7}))
row("F.version.out", "P3", "GFC2020 V3 cut forest cover by more than 20 % in the Cerrado", "EXTERNAL", "n/a",
    {"file": "research/v13/evidence/failure_modes/jrc146622.txt", "line": 1492, "doi": "10.2760/9982436"}, "2026-10-01",
    check=("grep", "v13/evidence/failure_modes/jrc146622.txt", "more than 20% in the Caatinga and Cerrado"), tier="30cm")
row("F.worldpop", "P3", "WorldPop signed per pixel, not per km²: 1.77× low", "SPEC", "L2", {"file": CL, "line": 61, "repo": "emem 18adb67 CHANGELOG [2.4.2]"}, "2026-09-29",
    check=("grep", CL, "1.77x low at Paris"), note="fixed")
row("F.scale", "P3", ["one pixel: 0.4709, 0.2966, 1.1427 under three offset rules"], "INFERRED", "L2-L3", {"inputs": ["E8.right", "E8.offset0", "E8.double"]}, "2026-10-01")
row("F.scale.out", "P3", "Element84 items say \"offset applied\" and \"apply −0.1\"", "LIVE", "n/a",
    {"file": "research/v13/evidence/failure_modes/e84_keylong.json", "pointer": "features[*].properties earthsearch:boa_offset_applied + assets.red raster:bands offset"}, "2026-10-01",
    check=("grep", "v13/evidence/failure_modes/e84_keylong.json", "boa_offset_applied"), tier="30cm", note="five items at one tile; do not generalise")
row("F.missing", "P3", ["off-tile pixels signed as 0", "a forest-loss screen passes"], "SPEC", "L3", {"file": CL, "line": 53, "repo": "emem 18adb67 CHANGELOG [2.4.2]"}, "2026-09-29",
    check=("grep", CL, "signed the far side's out-of-image pixels as 0"), note="fixed; prevalence not known, print no count")
row("F.missing.out", "P3", "Hansen lossyear 0 means no loss", "EXTERNAL", "n/a", {"url": "https://storage.googleapis.com/earthenginepartners-hansen/GFC-2025-v1.13/download.html"}, "2026-10-01", tier="30cm")
row("F.pixel", "P3 + P6", ["162 of 200", "fixed 28 Sep 2026"], "MEASURED", "L3",
    {"file": PV, "pointer": ["pre", "matches_round_not_floor"], "fix": CL + ":47 (2026-09-28T04:09:26Z)"}, "2026-09-30",
    check=("json", PV, ["pre", "matches_round_not_floor"], 162))
row("F.pixel.out", "P3", ["GDAL RFC 33: half-pixel shift", "one-pixel misregistration: error > 50 % of NDVI differences (Townshend 1992)"], "EXTERNAL", "n/a",
    {"url": ["https://gdal.org/en/stable/development/rfc/rfc33_gtiff_pixelispoint.html", "doi:10.1109/36.175340"]}, "2026-10-01", tier="30cm")
row("F.thing", "P3", ["\"this image\" resolved to a hair salon in Ontario", "receipt, Merkle proof and state chain all valid", "fixed 30 Sep 2026"], "SPEC", "L4",
    {"repo": "Vortx-AI/emem", "commit": "0edf574", "quote": "Every part of the verification machinery worked on an answer about a hair salon in Canada."}, "2026-09-30",
    note="read with git log -1 0edf574 in /home/user/vortx-ai/emem")
row("F.thing.out", "P3", "toponym ambiguity (Gritta et al. 2018)", "EXTERNAL", "n/a", {"doi": "10.1007/s10579-017-9385-8"}, "2026-10-01", tier="30cm")
row("F.rail.cellmatch", "P3 side rail", "emem's resolver once reported a cell match it never tested", "SPEC", "L1",
    {"repo": "emem 18adb67", "file": "crates/emem-api-rest/src/lib.rs:37800-37818 (line numbers move at 8e9b401)"}, "2026-08-11", tier="30cm")
row("F.rail.langchain", "P3 side rail", "one framework adapter returns a refusal as plain text", "MEASURED", "L1",
    {"file": "research/v13/evidence/crossruntime/refusal_matrix.json", "pointer": ["wrong_cell", "langchain_mcp"]}, "2026-09-30",
    check=("json_contains", "v13/evidence/crossruntime/refusal_matrix.json", ["wrong_cell", "langchain_mcp"], "returned [{'type': 'text'"), tier="30cm")
row("F.rail.mast", "P3 side rail", "MAST: no or incomplete verification (FM-3.2)", "EXTERNAL", "n/a", {"url": "https://arxiv.org/abs/2503.13657"}, "2026-10-01", tier="30cm")
row("F.caption", "P3", "Signatures prevented none", "INFERRED", "n/a", {"file": "research/v13/02_experiment_design.md", "section": "18 (honest boundary)"}, "2026-10-01")

# ---------------- threat ----------------
row("T.can", "threat", "A relay can rewrite what it carries but cannot sign under the pinned key or match an address", "SPEC", "L0",
    {"file": "research/v13/10_ladder_threat_invention.md", "section": "4.2-4.3", "external": "RFC 8032 l.160; BLAKE3 spec 128-bit"}, "2026-10-01")
row("T.pinned", "threat", ["pinned key", "DNS TXT", "did.json", "JWKS"], "LIVE", "L0", {"file": "research/repro/v8/trace_fact_output.txt", "pointer": "link 15"}, "2026-09-30", tier="30cm")
row("T.oneop", "threat", "All keys today are one operator's", "LIVE", "L0", {"file": "research/v13/evidence/ladder/witnesses.json", "pointer": ["independent_operator_count"]}, "2026-10-01",
    check=("json", "v13/evidence/ladder/witnesses.json", ["independent_operator_count"], 1), tier="30cm",
    note="the one independent domain (geo.qa) is also Vortx AI; never print the witnessed flag")

# ---------------- P4 evidence object ----------------
row("O.84", "P4", ["84 characters", "46 tokens (cl100k)"], "MEASURED", "n/a", {"file": TK, "pointer": ["fact_token_ndvi"]}, "2026-09-30",
    check=("json", TK, ["fact_token_ndvi", "chars"], 84))
row("O.46", "P4 + P11", "46 tokens", "MEASURED", "n/a", {"file": CM, "pointer": ["m5_tokens", "items", "fact_token", "cl100k"]}, "2026-10-01",
    check=("json", CM, ["m5_tokens", "items", "fact_token", "cl100k"], 46))
row("O.1115", "P4", "1,115 B", "LIVE", "L0", {"file": TK, "pointer": ["fact_cbor_bytes", "bytes"], "live": "GET /v1/facts/oj5cecci... re-hashed 2026-10-01T01:42Z (critic)"}, "2026-10-01",
    check=("json", TK, ["fact_cbor_bytes", "bytes"], 1115))
row("O.cid", "P4", "oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa", "LIVE", "L0", {"file": "research/repro/v8/proof_bundle_ndvi.cbor", "pointer": "token"}, "2026-10-01",
    check=("grep", XR, "oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa"))
row("O.cogs", "P4", ["277.9 + 281.9 MB", "B04 + B08 COGs", "Planetary Computer"], "MEASURED", "L3", {"file": "research/repro/data/v8/cog_pixel_bytes.json", "pointer": "B04 277897303 B, B08 281898500 B"}, "2026-09-30",
    check=("grep", "repro/data/v8/cog_pixel_bytes.json", "281898500"), tier="30cm")
row("O.pixel", "P4", ["row 9443, col 9098", "DN 1900, 3502"], "MEASURED", "L3", {"file": PX, "pointer": "S2A ... B08.floor(r,c), floor_DN"}, "2026-09-30",
    check=("json", PX, ["S2A 2026-09-25 (now, fact oj5cecci, signed 2026-09-28T09:06Z = post-fix)", "B08", "floor_DN"], 3502), tier="30cm")
row("O.key", "P4", "777er3yi…", "LIVE", "L0", {"file": XR, "pointer": "responder key"}, "2026-10-01", check=("grep", QW, "777er3yihgifqmv5hmc2wwmyszgddzderzhsx6rex4yoakwomvka"), tier="30cm")
row("O.nohash", "P4 + P7", ["named, not hashed", "0 of 215 Keylong sources carry a hash"], "MEASURED", "L3", {"file": CK, "pointer": "count(sources[] with hash or cid)"}, "2026-09-30",
    check=("ck_hash", CK, None, (215, 0)))
row("O.sevenaddr", "P4", "one Bengaluru value has seven", "MEASURED", "L0", {"file": BG, "pointer": "7 attestations with value 915.0712280273438, 7 fact_cids"}, "2026-09-29",
    check=("bg_values", BG, None, {918.0: 1, 915.0712280273438: 7}))
row("O.batch", "P4", "a batch signature covers such addresses", "SPEC", "L0", {"repo": "emem 18adb67", "file": "crates/emem-fact/src/attest.rs:93-143"}, "2026-10-01")
row("O.log", "P4", "Merkle log, RFC 6962 style, BLAKE3", "SPEC", "L0", {"repo": "emem", "file": "crates/emem-attest/src/translog.rs; docs/federation.md 9c"}, "2026-10-01", tier="30cm")

# ---------------- P5 matrix ----------------
row("X.loo", "P5", "Each of five checks alone stops a corruption.", "MEASURED", "L0-L3", {"file": MM, "pointer": ["leave_one_out"]}, D_R1,
    check=("json", MM, ["leave_one_out"], {"D": [], "E": ["M4", "M5", "M6"], "F": ["M9", "M10", "M11", "M12"], "G": ["M16"], "H": ["M14"], "I": ["M15"]}))
row("X.only", "P5 + H2", ["only the source re-read, the signer's wrong pixel", "Only a source re-read catches a signer's wrong pixel", "caught only by a re-read", "only it refuses the wrong pixel"], "MEASURED", "L3",
    {"file": MM, "pointer": ["leave_one_out", "I"]}, D_R1, check=("json", MM, ["leave_one_out", "I"], ["M15"]), note="allowlist for 'only' (report 10 sec. 5.3)")
row("X.flips", "P5", "flips the decision", "MEASURED", "n/a", {"file": MM, "pointer": ["summary", "A", "decision_flips"]}, D_R1,
    check=("json", MM, ["summary", "A", "decision_flips"], ["M2", "M8", "M12", "M13", "M14", "M15"]), tier="30cm")
row("X.p123", "P5 scope", "Three further signer errors (offset, same-day scene, unit) pass checks D to I; metadata checks catch them.", "MEASURED", "L3",
    {"file": "research/v13/evidence/ladder/r1_t2_extra_out.json", "pointer": "T2_offset_zero, T2_scene_relabel_same_day, T2_unit_mislabel .refused_at_level_I == false"}, "2026-10-01",
    check=("json", "v13/evidence/ladder/r1_t2_extra_out.json", ["T2_offset_zero", "refused_at_level_I"], False), tier="30cm")
row("X.entity", "P5", "The entity meant passes every check", "OUT-OF-SCOPE", "L4", {"file": MM, "pointer": "M17 outcome at every level"}, D_R1)

# ---------------- P6 wrong pixel ----------------
row("W.vals", "P6", ["0.4709 → hold", "0.3016 → irrigate"], "MEASURED", "L3", {"file": PX, "pointer": "S2A ... ndvi_floor_pixel / ndvi_round_pixel"}, "2026-09-30",
    check=("json", PX, ["S2A 2026-09-25 (now, fact oj5cecci, signed 2026-09-28T09:06Z = post-fix)", "ndvi_round_pixel"], 0.3015512674990541), tier="3m")
row("W.prev", "P6", ["162 of 200 sampled pre-fix records", "Wilson 95 %: 75 to 86 %"], "MEASURED", "L3", {"file": PV, "pointer": ["pre", "frac_round_wilson95"], "script": "research/v13/evidence/g1_pixel_audit/prevalence.py (seed 20261019)"}, "2026-09-30",
    check=("wilson", PV, ["pre", "frac_round_wilson95"], (0.75, 0.86)))
row("W.err", "P6", ["median 0.027", "p90 0.113", "max 0.301", "n 121"], "MEASURED", "L3", {"file": PV, "pointer": ["pre", "abs_err_index_where_differ"]}, "2026-09-30",
    check=("err", PV, ["pre", "abs_err_index_where_differ"], (0.027, 0.113, 0.301, 121)), tier="30cm")
row("W.kx", "P6", ["signed 0.3444", "0.4860", "23 Sep 2026"], "LIVE", "L3", {"file": PX, "pointer": "S2C 2026-09-23 ... ndvi_round_pixel / ndvi_floor_pixel", "live": "research/v13/evidence/critic/kx.json (GET 2026-10-01T01:41Z, no warning in body)"}, "2026-10-01",
    check=("json", PX, ["S2C 2026-09-23 (prev, fact kxjvfwpa, signed 2026-09-25T19:35Z = pre-fix)", "ndvi_floor_pixel"], 0.4860239589275528))
row("W.frame", "P6 scope", ["200 pre-fix Sentinel-2 records cited in emem.dev's public channel, one per cell, seeded", "192 Element84, 8 Planetary Computer"], "MEASURED", "n/a",
    {"file": PV, "pointer": ["pre", "providers"], "script": "research/v13/evidence/g1_pixel_audit/prevalence.py:1-20"}, "2026-09-30",
    check=("json", PV, ["pre", "providers"], {"E84": 192, "PC": 8}), tier="30cm")
row("W.post", "P6 scope", ["0 of 54", "Planetary Computer, two days"], "MEASURED", "L3", {"file": PV, "pointer": ["post", "matches_round_not_floor"]}, "2026-09-30",
    check=("json", PV, ["post", "matches_round_not_floor"], 0), tier="30cm", note="provider and fix confounded; say so")
row("W.rondonia", "P6 scope", ["changed 7 loss years and no EUDR flag", "100-point Rondônia grid"], "MEASURED", "L3",
    {"file": "research/v13/evidence/failure_modes/rondonia_floor_round_v2.json", "pointer": "count(lossyear floor != round) = 7; flags floor 3 / round 3"}, "2026-10-01",
    check=("rond", "v13/evidence/failure_modes/rondonia_floor_round_v2.json", None, (7, 3, 3)), tier="30cm")
row("W.south", "P6", ["pixel 10 m south", "10 m south"], "MEASURED", "L3", {"file": PX, "pointer": "round(r,c) = floor row + 1, same col"}, "2026-09-30",
    note="true of this record only; the 162 carry an east, south or south-east neighbour (review M7)", tier="30cm")

# ---------------- P7 ladder ----------------
row("L.780", "P7", ["780 of 780", "780 records pulled on 30 Sep 2026", "cell and band bound in 780 of 780"], "MEASURED", "L0-L1", {"file": EV, "pointer": "count(verified == PASS)"}, "2026-09-30", check=("csv", EV, ("verified", "PASS"), 780))
row("L.266", "P7", "266 of 780", "MEASURED", "L2", {"file": EV, "pointer": "count(recompute == pass)"}, "2026-09-30", check=("csv", EV, ("recompute", "pass"), 266))
row("L.reread0", "P7", "their source files are named, not hashed", "SPEC", "L3", {"repo": "emem 18adb67 and 8e9b401", "file": "crates/emem-api-rest/src/lib.rs: 62 x 'hash: None', 0 x 'hash: Some(' (report 10 sec. 0 item 2)", "measured": "0 of 215 Keylong source entries (O.nohash)"}, "2026-10-01")
row("L.409", "P7", "a relabelled token returns 409", "MEASURED", "L1", {"file": "research/v13/evidence/crossruntime/refusal_matrix.json", "pointer": ["wrong_cell", "rest"]}, "2026-09-30",
    check=("json_contains", "v13/evidence/crossruntime/refusal_matrix.json", ["wrong_cell", "rest"], "409"), tier="30cm")
row("L.gfc", "P7", "GFC2020 V3 forest commission error 13.1 %", "EXTERNAL", "L5", {"file": "research/v13/evidence/failure_modes/jrc146622.txt", "line": 236}, "2026-10-01",
    check=("grep", "v13/evidence/failure_modes/jrc146622.txt", "commission error of 13.1%"), tier="30cm")
row("L.status", "P7", ["CHECKABLE", "RECOMPUTABLE", "PARTIAL", "INHERITED", "OUT OF SCOPE"], "SPEC", "L0-L5", {"file": "research/v13/10_ladder_threat_invention.md", "section": "3.1-3.2"}, "2026-10-01")

# ---------------- P8 time ----------------
row("TM.918", "P8", ["918.0 m", "signed 28 May", "90 m DEM via Open-Meteo"], "MEASURED", "L1", {"file": BG, "pointer": "attestation yqbolgeo signed_at 2026-05-28T19:54:32Z; fn_key open_meteo_copdem90m@1"}, "2026-09-29",
    check=("grep", BG, "2026-05-28T19:54:32Z"))
row("TM.915", "P8", ["915.07 m", "first signed 11 Aug", "re-signed 7 times"], "MEASURED", "L1", {"file": BG, "pointer": "7 attestations value 915.0712280273438, first 2026-08-11T09:39:36Z"}, "2026-09-29",
    check=("grep", BG, "2026-08-11T09:39:36Z"))
row("TM.asof", "P8", ["1 May: none", "15 Jun: 918.0 m", "12 Aug: 915.07 m", "29 Sep: 915.07 m"], "MEASURED", "L1",
    {"file": BG, "recompute": "poster/make_figures_v12.py:506-510 asserts these as-of answers from the attestations"}, "2026-09-29")
row("TM.keylong", "P8", ["cited 25 Sep: 0.4709 → hold", "30 Sep: 0.4237 → irrigate"], "LIVE", "L1", {"file": CP, "pointer": "indices.ndvi 3yyaxn5d 0.4237 signed 2026-09-30T22:20:02Z"}, "2026-09-30",
    check=("cp", CP, "indices.ndvi", 0.42369991474850816))
row("TM.still", "P8", "the cited reference still re-hashes (1 Oct 2026)", "LIVE", "L0", {"file": "research/v13/11_research_gaps.md", "pointer": "P1-8: oj5cecci 1,115 B re-hash equal at 01:42Z"}, "2026-10-01",
    note="re-fetch within 7 days of print", tier="30cm")
row("TM.asof_rule", "P8 scope", "as-of compares signing times (UTC seconds)", "SPEC", "L1", {"repo": "emem", "file": "crates/emem-primitives/src/recall.rs:282-391; defect 35 (string compare)"}, "2026-10-01", tier="30cm")

# ---------------- P9 Rondonia ----------------
row("RO.grid", "P9", ["100 point samples", "740 m apart", "600 signed records"], "MEASURED", "L0", {"file": RO, "pointer": ["grid"]}, "2026-09-30",
    check=("csv", EV, ("case", "rondonia"), 600))
row("RO.cats", "P9", ["forest 2020 (GFC2020) + loss after 2020 (Hansen): 3", "forest, no later loss: 33", "cleared 2001 to 2020: 20", "not forest: 43", "maps disagree: 1"], "MEASURED", "n/a", {"file": RO, "pointer": ["category_counts"]}, "2026-09-30",
    check=("json", RO, ["category_counts"], {"not_forest_2020_no_hansen_loss": 43, "forest_2020_no_later_loss": 33, "cleared_2001_2020": 20, "eudr_flag_forest_2020_loss_after_2020": 3, "loss_after_2020_on_gfc2020_non_forest": 1}))
row("RO.tmf", "P9", "TMF agrees on 1 of 3 flags", "MEASURED", "n/a", {"file": RO, "pointer": "rows with eudr flag: jrc_tmf.deforestation_year 2023, 0, 0"}, "2026-09-30")
row("RO.cardA", "P9", ["Hansen loss 2023", "tree cover 2000 100 %", "GFC2020 V4 forest", "TMF 2023", "CCI 208 t/ha"], "MEASURED", "n/a",
    {"file": RO, "pointer": "row cell defi.zb391.taza.zcc31"}, "2026-09-30", tier="30cm")
row("RO.must", "P9", "Point samples, not parcel polygons; not a regulatory determination.", "OUT-OF-SCOPE", "L5", {"file": "research/SHARED_STATE_EMEM_A0_MASTER.md", "section": "21"}, "2026-10-01")

# ---------------- P10 vectors ----------------
row("V.prithvi", "P10", ["Prithvi-EO-2.0", "1,024 values", "checkpoint 2ad1775f…"], "LIVE", "L2",
    {"file": CC, "pointer": "facts[band=prithvi_eo2].served_via.model_blake2b_hex == derivation.args.args[4]"}, "2026-10-01",
    check=("prithvi", CC, None, "2ad1775f298264470dd3f0b6e7819b62d7860968665fe308ed93abb766af62cc"))
row("V.tessera", "P10", ["TESSERA", "128 values", "only a path and year", "…/npy/v1/2024/…"], "LIVE", "L3", {"file": CC, "pointer": "facts[band=geotessera].sources[0].id = .../npy/v1/2024/..., args [lat, lng, 2024]"}, "2026-10-01",
    check=("grep", CC, "tessera/npy/v1/2024/..."))
row("V.retired", "P10", "emem.dev lists its encoders as retired", "SPEC", "n/a", {"file": "research/repro/v12/data/v1_bands_2026-09-30.json", "pointer": "bands[*].materializer.kind == retired for geotessera, clay_v1, prithvi_eo2, galileo"}, "2026-09-30",
    check=("grep", "repro/v12/data/v1_bands_2026-09-30.json", "retired on this deployment"), note="do not print a retirement date (the TESSERA record carries signed_at 2026-09-30T08:33Z)")
row("V.resolve", "P10", "Both still resolve", "LIVE", "L0", {"file": CC, "pointer": "GET /v1/cells/defi.zb572.xoso.zb1ec 2026-10-01T01:42Z"}, "2026-10-01", note="re-fetch at build")

# ---------------- P11 cost ----------------
row("C.cpu", "P11", ["0.33 ms of CPU", "One 2.8 GHz Xeon core"], "MEASURED", "L0-L3", {"file": CM, "pointer": ["m2_offline_verification", "mutation_suite_ms_per_decision_by_level", "I", "median", " minus mutation_suite_genuine_construction_ms.median (0.3565 - 0.0288 ms)"], "host": "one 2.8 GHz Xeon core"}, "2026-10-01",
    check=("approx_diff", CM, [["m2_offline_verification", "mutation_suite_ms_per_decision_by_level", "I", "median"], ["m2_offline_verification", "mutation_suite_genuine_construction_ms", "median"]], 0.33), note="committed 1.187 ms on another host; keep the range here, print one host-stated value")
row("C.reread", "P11", ["1.18 MB", "about 7 s"], "MEASURED", "L3", {"file": CM, "pointer": "m3_trace_read_only.keylong_ndvi.links 8+9+9b: 6,945 ms, 1,180,728 B"}, "2026-10-01",
    check=("reread", CM, None, (6945.0, 1180728)), note="through a TLS-re-terminating proxy; print 'on our network path'")
row("C.scene", "P11", ["0.058 % of the scene"], "MEASURED", "L3", {"file": "research/repro/data/v8/scene_sizes.json + cog_pixel_bytes.json", "pointer": "1,165,033 / 2,023,818,762"}, "2026-09-30",
    check=("calc", None, 1165033 / 2023818762 * 100, 0.058), tier="30cm")
row("C.tok", "P11", ["46 tokens", "the value 8"], "MEASURED", "n/a", {"file": CM, "pointer": ["m5_tokens", "items", "value_16_digits", "cl100k"]}, "2026-10-01",
    check=("json", CM, ["m5_tokens", "items", "value_16_digits", "cl100k"], 8))
row("C.tools", "P11", "18-tool MCP list 18,709 (1 Oct)", "MEASURED", "n/a", {"file": CM, "pointer": ["m5_tokens", "items", "mcp_tools_list_core18_response", "cl100k"]}, "2026-10-01",
    check=("json", CM, ["m5_tokens", "items", "mcp_tools_list_core18_response", "cl100k"], 18709), tier="30cm", note="raw body, cl100k; never mix with 20,838 (re-serialised) or 18,659 (30 Sep)")
row("C.json", "P11", "record as JSON 562", "MEASURED", "n/a", {"file": CM, "pointer": ["m5_tokens", "items", "fact_json_as_served", "cl100k"]}, "2026-10-01",
    check=("json", CM, ["m5_tokens", "items", "fact_json_as_served", "cl100k"], 562), tier="30cm")
row("C.g2tok", "P11", ["2.1× the tokens prose costs", "same decisions"], "PRE-REGISTERED", "n/a",
    {"file": G2, "pointer": "b.claude-haiku-4-5.arms.{T,P}.input_tokens_mean; decision_correct 10/10 both"}, "2026-09-30",
    check=("ratio", G2, (["b", "claude-haiku-4-5", "arms", "T", "input_tokens_mean"], ["b", "claude-haiku-4-5", "arms", "P", "input_tokens_mean"]), 2.1))
row("C.g2wall", "P11 scope", "+1.75 s", "PRE-REGISTERED", "n/a", {"file": G2, "pointer": "wall_s_mean T 8.85 - P 7.10"}, "2026-09-30", check=("calc", None, 8.85 - 7.10, 1.75), tier="30cm")
row("C.resolve", "P11", ["40 ms warm", "154 ms cold"], "MEASURED", "L0", {"file": CM, "pointer": "m1_resolve_fact_https.{warm_cbor_reused_connection_ms,cold_cbor_new_connection_ms}.median"}, "2026-10-01",
    check=("approx", CM, ["m1_resolve_fact_https", "cold_cbor_new_connection_ms", "median"], 154.2), tier="30cm")
row("C.bundle", "P11", ["4,906 B", "offline proof bundle 0.57 ms"], "MEASURED", "L0-L2", {"file": CM, "pointer": ["m2_offline_verification", "in_process_precompiled_exec_ms", "median"]}, "2026-10-01",
    check=("approx", CM, ["m2_offline_verification", "in_process_precompiled_exec_ms", "median"], 0.57), tier="30cm")
row("C.hash", "P11", "1.6 µs", "MEASURED", "L0", {"file": CM, "pointer": ["m2_offline_verification", "primitives_us", "blake3_fact_1115B", "median"]}, "2026-10-01",
    check=("approx", CM, ["m2_offline_verification", "primitives_us", "blake3_fact_1115B", "median"], 1.57), tier="30cm")

# ---------------- P12 ecosystem ----------------
row("EC.11", "P12", ["11 client paths", "one address and one value"], "MEASURED", "L0", {"file": XR, "pointer": ["summary", "ndvi_keylong", "paths_ok"]}, "2026-09-30",
    check=("json", XR, ["summary", "ndvi_keylong", "paths_ok"], 11), note="server 213e273, 3 reps")
row("EC.9of11", "P12", "with receipt signatures checked on 9", "MEASURED", "L0", {"file": XR, "pointer": ["summary", "ndvi_keylong", "receipt_verified_paths"]}, "2026-09-30",
    check=("json", XR, ["summary", "ndvi_keylong", "receipt_verified_paths"], 9))
row("EC.ms", "P12 dot plot", ["56.3", "58.3", "58.6", "207.7", "223.5", "223.7", "226.3", "235.6", "300.8", "1,176.8"], "MEASURED", "L0",
    {"file": XR, "pointer": "rows.ndvi_keylong[*].ms_median (never .ms, which is the last repetition)"}, "2026-09-30", check=("xr_med", XR, None, None), tier="30cm")
row("EC.notrun", "P12", "Not run by us: ChatGPT, claude.ai, Dify, VS Code, Cursor", "LIVE", "n/a", {"file": EM, "pointer": "rows chatgpt, claude-ai-custom-connector, dify-marketplace, vscode, cursor: evidence_level"}, "2026-10-01")
for mid, txt in [("claude-code-mcp", "Claude Code"), ("claude-code-plugin", "Claude Code plugin"), ("claude-ai-custom-connector", "Claude.ai custom connector"),
                 ("dify-marketplace", "Dify Marketplace plugin (community)"), ("mcp-core", "Model Context Protocol (MCP)"), ("a2a", "Agent2Agent (A2A)"),
                 ("official-mcp-registry", "Official MCP Registry"), ("github-mcp-registry", "GitHub MCP Registry"), ("github-repo", "github.com/Vortx-AI/emem"),
                 ("glama", "Glama"), ("gemini-cli", "Gemini CLI"), ("vscode", "Visual Studio Code"), ("cursor", "Cursor"), ("python-sdk", "pip install ememdev"),
                 ("ts-sdk", "npm i @vortxai/emem"), ("rest-openapi", "REST / OpenAPI 3.1"), ("docker", "ghcr.io/vortx-ai/emem"),
                 ("llamaindex", "LlamaIndex"), ("autogen", "AutoGen"), ("crewai", "CrewAI"), ("mastra", "Mastra")]:
    row(f"EC.row.{mid}", "P12 band", txt, "LIVE", "n/a", {"file": EM, "pointer": f"id={mid}: status, print.allowed, verified_utc"}, "2026-10-01",
        check=("eco", EM, mid, None), tier="1m", note="glyph drawn from the row's status; re-verify within 14 days of print")
for mid, txt, cond in [("chatgpt", "ChatGPT (@emem)", "only after a dated logged-in screenshot is committed"),
                       ("langchain", "LangChain (MCP adapters)", "only after emem's example is fixed (03 sec. 1.4)"),
                       ("agno", "Agno", "only after emem's README names fastmcp")]:
    row(f"EC.row.{mid}", "P12 band (conditional)", txt, "LIVE", "n/a", {"file": EM, "pointer": f"id={mid}"}, "2026-10-01",
        note="CONDITIONAL: " + cond)
row("EC.statusdate", "P12 legend", "checked 30 Sep 2026", "LIVE", "n/a", {"file": EM, "pointer": "verified_utc of every printed row"}, "2026-10-01", tier="30cm")

# ---------------- P13 prior art ----------------
for k, t, u in [("stac", "FIND · STAC · an asset (file)", "https://stacspec.org (STAC 1.1.0)"), ("openeo", "RUN · openEO · a process graph", "openEO API 1.3.0"),
                ("prov", "RECORD LINEAGE · W3C PROV · entity, activity, agent", "https://www.w3.org/TR/prov-dm/"),
                ("c2pa", "SIGN FILES · C2PA, CDSE Traceability · a file", "C2PA 2.4; documentation.dataspace.copernicus.eu/APIs/Traceability.html"),
                ("rag", "RETRIEVE · RAG · a text chunk", "arXiv 2005.11401"), ("carry", "CARRY · MCP, A2A · a tool call, an agent card", "MCP 2025-11-25; A2A 1.0"),
                ("geoguard", "JUDGE · GeoGuard · a claim in text", "https://github.com/NASA-IMPACT/geoguard"),
                ("credit", ["Sigstore, RFC 9162, SCITT (RFC 9943)", "ARC (arXiv 2607.25066)"], "report 04 sec. 2.8-2.14")]:
    row(f"PA.{k}", "P13", t, "EXTERNAL", "n/a", {"url": u, "report": "research/v13/04_prior_art_and_field.md sec. 1-2"}, "2026-10-01")
row("PA.critical", "P13", "A STAC item identifies a file; EMEM identifies the observation an agent cited", "SPEC", "L1", {"file": "research/v13/04_prior_art_and_field.md", "section": "2.1, 8"}, "2026-10-01")

row("PA.munir", "P3 header strip", ["errors may propagate silently across steps", "Munir et al. 2026, arXiv 2604.24919"], "EXTERNAL", "n/a",
    {"url": "https://arxiv.org/abs/2604.24919", "report": "research/v13/04_prior_art_and_field.md sec. 0 item 9, 2.15"}, "2026-10-01", tier="30cm",
    note="position paper by the workshop organiser B. Demir and keynote S. Khan; quote verbatim from the arXiv HTML")
row("PA.geoguard_line", "P13", "GeoGuard judges the claim; EMEM fixes the evidence it cites.", "EXTERNAL", "n/a", {"file": "research/v13/04_prior_art_and_field.md", "section": "2.7"}, "2026-10-01")
row("H.byline", "header", ["Jaya Kumari", "Avijeet Singh", "Vortx AI", "emem.dev", "github.com/Vortx-AI/emem (Apache-2.0)", "BIFOLD and ESA Φ-lab", "Berlin"], "LIVE", "n/a",
    {"file": "research/v13/evidence/industry/prog_posters.txt", "repo_licence": "research/v13/03_ecosystem_manifest.md row GitHub (Apache-2.0)"}, "2026-10-01", tier="1m")

REFS = ["Sentinel-2 Products Specification (ESA)", "Copernicus DEM GLO-30/90", "Hansen et al. 2013, GFC v1.13", "JRC GFC2020 V3/V4, TMF",
        "ESA CCI Biomass v7", "Reg. (EU) 2023/1115", "BLAKE3", "RFC 8032", "RFC 6962/9162", "STAC 1.1", "openEO 1.3", "W3C PROV-DM", "C2PA 2.4",
        "MCP 2025-11-25", "A2A 1.0", "Perez et al., ICLR 2025", "Munir et al. 2026 (2604.24919)", "Cemri et al. 2025, MAST (2503.13657)",
        "Dang et al. 2026, ARC (2607.25066)", "Townshend et al. 1992", "GeoGuard (NASA-IMPACT)", "Prithvi-EO-2.0", "TESSERA (2506.20380)"]
row("REF.footer", "footer", REFS, "EXTERNAL", "n/a", {"report": "research/v13/04_prior_art_and_field.md sec. 6 (arXiv ids verified via the arXiv API); 00_v11_review_findings.md EXT-3 (ESA document title)"}, "2026-10-01", tier="30cm",
    note="the footer prints exactly these strings joined by ' · '; any other reference needs a row")
# ---------------- conclusion, footer, QR ----------------
row("K.concl", "conclusion", ["none of the 16 corruptions in our suite", "a wrong pixel emem signed in production"], "MEASURED", "L0-L3", {"inputs": ["S.R1.I", "F.pixel"]}, D_R1,
    r5="R5 template appends: 'agents with a checked reference acted on {R5.E.pooled.false_accept}'")
row("K.commit", "footer", "emem.dev at commit 8e9b401", "LIVE", "n/a", {"header": "x-emem-commit 8e9b401cecae7ab9944d403a2d7840952c6586a6", "file": CM, "pointer": ["environment", "emem_server_commit_header"]}, "2026-10-01",
    check=("json_contains", CM, ["environment", "emem_server_commit_header"], "8e9b401"), tier="30cm")
row("K.dates", "footer", "measurements 29 Sep to 1 Oct 2026", "MEASURED", "n/a", {"inputs": "dates of every row above"}, "2026-10-01", tier="30cm")
row("K.sat042", "footer", "Extending verification to execution: reference harness, no spacecraft enrolled.", "SPEC", "n/a", {"file": "research/repro/v12/trace/sat042_run_stdout.txt"}, "2026-09-30", tier="30cm")
for q, p in [("VIEW THE DEMO", "https://vortx-ai.github.io/esa_poster/demo/"), ("TRY A TOKEN", "https://vortx-ai.github.io/esa_poster/t/"),
             ("INSPECT THE RECORD", "https://vortx-ai.github.io/esa_poster/r/"), ("RE-RUN THE TEST", "https://vortx-ai.github.io/esa_poster/test/"),
             ("READ THE METHODS", "https://vortx-ai.github.io/esa_poster/methods/"), ("DISCOVER INTEGRATIONS", "https://vortx-ai.github.io/esa_poster/use/")]:
    row("Q." + q.split()[0].lower() + "_" + q.split()[-1].lower(), "QR", q, "SPEC", "n/a", {"payload": p, "file": "research/v13/evidence/visual/qr/qr_table.json"}, "2026-10-01",
        note="QR gate: decode == payload; follow redirects to HTTP 200 text/html on a 390 x 844 viewport")

# ---------------- checks ----------------
def run(c):
    kind, f, p, exp = (list(c) + [None] * 4)[:4]
    if kind == "json":
        return ptr(J(f), p) == exp
    if kind == "json_contains":
        return exp in str(ptr(J(f), p))
    if kind == "approx":
        return abs(round(ptr(J(f), p), 2) - exp) <= max(0.01, abs(exp) * 0.01)
    if kind == "grep":
        return p in (R / f).read_text()
    if kind == "calc":
        return abs(p - exp) < 0.0006 or round(p, 3) == round(exp, 3)
    if kind == "count_mut":
        return len([m for m in J(f)["meta"]["mutations"] if m["id"] not in ("G0", "M17")]) - 1 == exp or \
               len([m for m in J(f)["meta"]["mutations"] if m["id"] not in ("G0", "M17", "M7")]) == exp - 1 or \
               J(f)["summary"]["I"]["applicable"] == exp
    if kind == "qwen":
        rows_ = [json.loads(l) for l in open(R / f)]
        return sum(1 for r in rows_ if (r["arm"], r["decision"]) == p) == exp
    if kind == "qwen_bare":
        rows_ = [json.loads(l) for l in open(R / f)]
        return sum(1 for r in rows_ for t in (r.get("tool_calls") or []) if t.get("token_form") == "bare_cid") == exp
    if kind == "cp":
        return any(r["band"] == p and r["value"] == exp for r in J(f))
    if kind == "bg_values":
        return dict(Counter(a["value"] for a in J(f)["contradictions"][0]["attestations"])) == exp
    if kind == "ck_hash":
        n = h = 0
        for fa in J(f)["facts"]:
            for s in fa.get("sources", []):
                n += 1; h += 1 if (s.get("hash") or s.get("cid")) else 0
        return (n, h) == exp
    if kind == "wilson":
        w = ptr(J(f), p); return (round(w[1], 2), round(w[2], 2)) == exp
    if kind == "err":
        e = ptr(J(f), p); return (round(e["median"], 3), round(e["p90"], 3), round(e["max"], 3), e["n"]) == exp
    if kind == "csv":
        col, val = p
        return sum(1 for r in csv.DictReader(open(R / f)) if r[col] == val) == exp
    if kind == "geod":
        from pyproj import Geod
        return round(Geod(ellps="WGS84").inv(*p)[2]) == exp
    if kind == "rond":
        d = J(f); ly, g = d["lossyear"], d["gfc2020"]
        ch = sum(1 for r in ly if r["floor"] != r["round"])
        fl = sum(1 for a, b in zip(g, ly) if a["floor"] == 1 and b["floor"] > 20)
        fr = sum(1 for a, b in zip(g, ly) if a["round"] == 1 and b["round"] > 20)
        return (ch, fl, fr) == exp
    if kind == "prithvi":
        for fa in J(f)["facts"]:
            if fa["band"] == "prithvi_eo2":
                return fa["served_via"]["model_blake2b_hex"] == exp and exp in json.dumps(fa["derivation"]) and len(fa["value"]) == 1024
        return False
    if kind == "reread":
        L = ptr(J(f), ["m3_trace_read_only", "keylong_ndvi", "links"])
        return (round(sum(L[k]["ms_median"] for k in ("8", "9", "9b")), 1), sum(L[k]["bytes"][0] for k in ("8", "9", "9b"))) == exp
    if kind == "ratio":
        a, b = ptr(J(f), p[0]), ptr(J(f), p[1]); return round(a / b, 1) == exp
    if kind == "xr_med":
        meds = sorted(r["ms_median"] for r in J(f)["rows"]["ndvi_keylong"] if r.get("ms_median"))
        return meds == [56.3, 58.3, 58.6, 207.7, 223.5, 223.7, 226.3, 235.6, 300.8, 1176.8]
    if kind == "eco":
        m = {r["id"]: r for r in J(f)}[p]
        return m["print"]["allowed"] is True and m["status"] in ("LIVE", "PROTOCOL", "REGISTRY", "EXAMPLE")
    raise ValueError(kind)

bad = 0
for r in rows:
    if r["check"]:
        try:
            ok = run(r["check"])
        except Exception as e:  # noqa
            ok = f"error {e}"
        r["checked"] = ok is True
        if ok is not True:
            bad += 1; print("CHECK FAIL", r["id"], ok, file=sys.stderr)
    else:
        r["checked"] = None
    if r["check"]:
        r["check"] = {"kind": r["check"][0], "file": r["check"][1], "arg": r["check"][2] if len(r["check"]) > 2 else None,
                      "expect": r["check"][3] if len(r["check"]) > 3 else None}
# fix eco rows' status from the manifest itself
man = {m["id"]: m for m in json.load(open(R / EM))}
for r in rows:
    if r["id"].startswith("EC.row."):
        mid = r["id"][7:]
        r["manifest_status"] = man[mid]["status"]
        r["status"] = {"LIVE": "LIVE", "PROTOCOL": "SPEC", "REGISTRY": "LIVE", "EXAMPLE": "MEASURED"}.get(man[mid]["status"], "LIVE")
        if mid == "chatgpt":
            r["status"] = "OUT-OF-SCOPE"; r["note"] += "; manifest says LIVE but evidence is UNVERIFIED (critic P0-8): not printed by default"

doc = {"schema": "esa_poster v13 claims map", "version": 1, "generated": "2026-10-01", "brief": "research/v13/12_FINAL_BRIEF.md",
       "rule": "no row, no print: every number and every claim sentence on the board (HTML and figure text) must match a row's print[] string; rows with status PRE-REGISTERED and date 'pending' print only in R5 mode; rows whose note starts CONDITIONAL print only when the condition is met",
       "statuses": ["SPEC", "LIVE", "MEASURED", "PRE-REGISTERED", "INFERRED", "EXTERNAL", "OUT-OF-SCOPE"],
       "live_max_age_days_at_build": 7, "ecosystem_max_age_days": 14, "rows": rows}
json.dump(doc, open(OUT_JSON, "w"), indent=1, ensure_ascii=False, default=str)

md = ["| id | block | printed | status | layer | source (file · key/line) | date | check |", "|---|---|---|---|---|---|---|---|"]
for r in rows:
    if r["id"].startswith("R5.") and r["id"].count(".") == 2 and r["id"].split(".")[2] in ("haiku", "sonnet", "opus", "fable", "qwen7b"):
        continue
    src = r["source"]
    s = " · ".join(f"{k}: {v}" for k, v in src.items()) if isinstance(src, dict) else str(src)
    s = s.replace("|", "/")
    pr = " / ".join(r["print"]).replace("|", "/")
    chk = {True: "pass", None: "manual", False: "FAIL"}[r["checked"]]
    md.append(f"| {r['id']} | {r['block']} | {pr} | {r['status']} | {r['layer']} | {s} | {r['date']} | {chk} |")
OUT_MD.write_text("\n".join(md) + "\n")
print(len(rows), "rows;", sum(1 for r in rows if r["checked"] is True), "auto-checked pass;", bad, "fail")
```

```python
import re,sys
t=open('/home/user/esa_poster/research/v13/12_FINAL_BRIEF.md').read()
c=t.split('## C. The complete printed text')[1].split('## D. Claims map')[0]
rt=[l[2:] for l in c.splitlines() if l.startswith('> ') and not l.startswith('> [R5]')]
w=sum(len(re.findall(r"[A-Za-z0-9][\w'.,%/:+·-]*",l)) for l in rt)
# figure text: backticked strings outside running lines, excluding title, token and QR payload lines
ft=re.findall(r'`([^`]+)`',c)
skip=('EMEM: A Content','emem:fact:','https://','oj5cecci')
fw=sum(len(x.split()) for x in ft if not x.startswith(skip))
print('running',w,'lines',len(rt),'figure text approx',fw)
for l in rt: print(len(l.split()), l[:70])
```
