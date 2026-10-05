# v13.10 review: section read-through, emem scan, audience fit (4 Oct 2026)

Reviewer: the agent that built v13.10, reading the rendered board (poster/emem-poster-A0.pdf) after every gate passed.
Treat it as a self-review, not an independent one.

## 1. Changes in this round

- **Superseded, see section 9.** Panel 1 outcome flipped from "B acted on corrupted evidence" (0/300 for emem) to
  "B declined to act on corrupted evidence" (300/300 for emem; prose 22/276, JSON 112/276, RAG 56/276, opaque id 134/288). Each declined count is
  the complement of the pre-registered false-accept count on the same trials (rows `R5.*.declined`, checked as
  n - k against `research/repro/v13/r5/results.json`). The take line keeps the harm figure in brackets ("they acted
  on 254"), so the original measurement is still printed.
  Why: at walking distance, higher-is-better reads faster. A visitor sees 300/300 next to 22/276 without decoding
  "0 is good". Panel 5 keeps the per-mutation "B acts on corrupted evidence" view, which is the analysis grain.
- Panel 5 follows panel 1: agent bars and totals now show corruptions declined (n - acted on), in emem blue, so the
  same quantity reads the same way in both panels (22/276 ... 300/300; R1 0/15 ... 16/16). The per-cell R1 squares
  keep their outcome colours; the legend's blue reads "declined". Rows `R5.cell.*.declined` and `S.R1.*.declined`
  are re-checked as n - k against the result files.
- Panel 6 is not flipped. Its numbers (162 of 200 pre-fix records) describe a defect in emem's own reader, and the
  figure already reads as "which check catches it": five checks pass the wrong value, the source re-read refuses it.
  Turning that into "38 of 200 read the right pixel" would soften a finding the board should state plainly.
- Arrow glyphs (→) removed from the face. Step sequences print as boxes: the header trace line, the full-trace
  headline, panel 5's Resolve / Re-hash / Bind / Recompute / Re-read, the header strip (2.02 GB scene | 84 characters)
  and the workflow strip (boxes without arrows). Inline uses became words or colons: "0.4709: hold",
  "as of 15 Jun: 918.0 m", "Tests pin 3σ at 0.50", "NaN as f9 7e00", "0.6431 (s 0.05)", "bytes, name".
- The Qwen scope line now names its direction ("acted on corruptions ... 22 of 23"), so it no longer reads as the
  same metric as the flipped column.
- The subhero uses the product's spelling, "emem", to match the lead, the code box, panel 12 and the emem repo.
  The title keeps "EMEM" because it is the programme title.

## 2. AI-tell scan, section by section

Checked against the build's tell list plus the patterns it does not catch: slogan pairs ("not X but Y"), triads,
hedging stacks, colon-heavy headlines, "seamless/robust"-class adjectives and unearned superlatives.

| Section | Finding | Action |
|---|---|---|
| Header lead | Plain declaratives. "Agents cannot write observations" is a strong claim; it holds by default (fact plane closed to agents; emem README "Only machines write facts"). | Kept; allowlisted with that evidence. |
| Header bridge | "Encode in orbit, decode in AI's reasoning with emem." is a tagline. emem's own diagrams use the same pairing ("Encoders in orbit, decoders on the ground"; "What travels between machines is a handle, not a payload"). | Kept as the one tagline; panel 1 and panel 11 print the harness scope. |
| Panel 1 | "The same observation, carried through receiver checks." Fine. | None. |
| Panels 2, 3, 7 | Short, measured, no tells. | None. |
| Full trace | Grey residuals are concrete, not hedges. | None. |
| Panel 9 | "Conceptual tuple" caption is dense but exact. | None. |
| Panel 10 | New line uses a colon list; it is a definition, not a slogan. | Kept. |
| Panel 12 | "Use emem. Carry the evidence forward." is the board's only imperative headline. | Kept (call to action). |

No em or en dashes and no listed tell words (build gate). No sentence was found that needed rewording for tone.

## 3. What the emem repo (Vortx-AI/emem @ 320a1d5, 3 Oct 2026) has that the board does not

| emem material | On the board? | Recommendation |
|---|---|---|
| Absence facts ("when the world has no answer, emem signs that too") | Token family row "nothing there" only | Strong for EO agents (cloud, no coverage). Worth a line if space opens. |
| Cross-vendor decoding: one token, same fact_cid in Claude, Gemma 3 (Bedrock) and Qwen 2.5 (local) | Panel 12 prints 11 client paths, not the vendor spread | Supports "decode in AI's reasoning". Needs a committed run here before it can be printed. |
| emem-guard: refuses a sentence whose number disagrees with the fact it cites | No | Directly relevant to the GeoGuard poster in the same session. Talking point; add if a measured run is committed. |
| Clean-room third-party verifier (dxrfmreb: 725 requests, 11 findings) | No | Credibility point; source is emem's README, not this repo. Talking point only. |
| "Satellites for AI." (emem's own one-line pitch) | No | Fits the AGENTS.md convention ("emem is AI infrastructure; satellites are the input"). Candidate for the header strip in a later round. |
| Notes plane: agents write signed notes, never facts | Implied by the lead | Fine as is. |

## 4. Will the session 1 room understand, like and use emem?

Poster Session 1 (19 Oct, 23 posters) is mostly EO agent systems: data discovery and orchestration (Telespazio, GMV,
Thales GEODES, Sistema THEDE, Development Seed NASA discovery agent), disaster and flood agents (CloudFerro x2,
VITO, RSS-Hydro), evaluation (CERTH "Beyond Task Success"), guardrails (GeoGuard, UAH), onboard constellation
orchestration (LLM-based onboard simulation study) and RAG over sensors (SENSOR2RAG).

- **Understand.** The 3 m read is now: hero ("survives an agent handoff"), the seven-step strip with "Hand off"
  highlighted, and 300/300 against 22/276. At 1 m the lead paragraph answers the question every one of these teams
  has. Risk: the centre code box and the full trace are 30 cm material; they are dense by design.
- **Like.** Builders of multi-agent pipelines (CloudFerro, Telespazio, GMV, isardSAT) all hand intermediate EO results
  between agents; panel 1 is their failure mode measured. The onboard-orchestration poster is the natural audience
  for the orbit line. Evaluation and guardrail posters will value panel 7 and the trace's "still trusted" column.
- **Use.** Panel 12 answers "where can I use it today" without a QR (ChatGPT, Claude, VS Code, Dify, MuleSoft,
  SDKs, frameworks). The weak point is visual: text cards rather than the real listings (issue #58).

## 5. Self-rating

8 / 10 for this audience. Strong: one measured headline, honest scope lines, every number traceable, a usable
integration band. Held back by: density in the centre and left columns (issue #18 tension, now an author decision),
text-only listing cards (#58), and two measured-elsewhere results (cross-vendor decode, emem-guard) that are not yet
committed here and so cannot be printed.

## 6. Issue triage

| Issue | State after this round | Reason |
|---|---|---|
| #5 rebuild around handoff | close | Board leads with the handoff experiment; integrity is not truth, upstream and entity limits stay explicit (panel 7, trace residuals). The 15-link trace returned to the face at the author's request (v13.10). |
| #6 handoff benchmark | close | R5: pre-registered, 2,794 scored trials, five conditions, 23 items, three Claude models plus Qwen2.5-7B, Wilson intervals. Deviation: two model families, not 4 to 6. |
| #16 handoff as primary result | close | Panel 1 prints conditions, denominators, models, false acceptance (as its complement) and the controls' decision accuracy (panel 5). |
| #17 guarantee ladder | close | Panel 7 table, L0 to L3 chips in panels 1 and 5, trace residuals per link. |
| #18 reduce density | close, not planned | Superseded by the author's v13.10 request to keep the coded memory and full trace on the face. |
| #27 matrix as hero figure | close | Panel 5 is the largest figure (396 x 196 mm) with n, scope and the check that stops each mutation. |
| #40 ecosystem map | close | Panel 12, manifest-backed; the build fails if a required integration is missing or stale. |
| #43 same evidence, different agent | close | Panel 12: same record and value through 11 client paths, receipts on 9 (30 Sep). |
| #7 bind upstream identity | open | Protocol work in emem; the board states "Source-file hashes are absent from this record". |
| #33 walk-by hierarchy | open | Improved (3 m read above) but not designed as a full three-distance pass. |
| #39 media pack | open | Not started. |
| #44 discovery destinations | open | Connect QR lands on /use/; acceptance needs a phone test. |
| #46 platform marks | open | Depends on #58 assets and brand guidance. |
| #58 real listing images | close | Five listings (ChatGPT, Claude directory, Dify, GitHub MCP Registry, ClawHub) printed as screenshot tiles in panel 12; sources in `research/v13/evidence/listings/`. |
| #46 platform marks | close | The listing tiles carry each platform's own page; no separate logo assets. |

## 7. Final print review (4 Oct 2026)

Every section was read at print resolution (20 crops of the 300 dpi render) and the printed text was scanned for
arrows, dashes, slogan pairs, hedges and tell words. Fixed in this pass: panel 5's bar note (it still described
false acceptance after the flip), the attribution sentence in panel 3, two unclear phrases in panel 10, trace link
labels, line breaks inside SAT-042 and inside the acceptance rule, chain rules between boxed steps, product spelling
in two figure labels, the GitHub card's repeated "Registry", and a missing space in panel 6. Kept on purpose: the
panel 10 headline "Beyond a single observation" (authors' wording) and the programme title (authors' decision).
Result: 18 of 18 gates, 0 text overlaps, all three QR codes decode to their pages.

## 8. Listings, the Vortx site and the emem changelog (4 Oct 2026)

- **Listing images removed from the print.** Screenshot text set at about 5 pt at A0, tile widths varied, and the
  crops showed "No ratings yet", like and install counts, "New" and "updated 2 days ago". Each card now quotes the
  listing's own words (verbatim) at 17 pt; the screenshots stay as evidence in `research/v13/evidence/listings/`.
- **Paper citation added and corrected.** The board printed no DOI. The vortx.ai agent card names the whitepaper with
  the board's exact title as 10.5281/zenodo.20706317 and the companion study as 10.5281/zenodo.20706893; the byline now
  prints both. emem's CITATION.cff lists 20706893 as its preferred citation, which the site calls the study: worth
  aligning in the emem repo.
- **Vortx site framing (vortxwebsite @ e625106) against the board.** Same core story: "Encode on device. Decode with
  @emem."; "Send the token. Keep the pixels."; "Signed on the ground today, in orbit next" (payload in design, ground
  segment next), which matches the board's orbit line and its harness scope. Not on the board, as talking points
  (no committed measurement here): the 24-hop relay between two model families (words round, the token arrives exact);
  the live draft check that catches a rounded number (`/v1/echo_verify`, emem-guard); non-EO observers (telescopes,
  drones, robots, cameras); the accelerator programmes (Seraphim Space Mission 15, NVIDIA Inception, AWS Space
  Accelerator); the products built on emem (geo.qa, eudr.dev, propcheck.dev).
- **emem since the measurements (CHANGELOG to 320a1d5).** Nothing contradicts the board. Overture facts now carry
  `sources[0].hash`; COG facts such as the board's record still do not (panel 4 says so for this record). Pre-fix
  facts no longer answer "latest" and are re-read; nothing signed is rewritten (panel 6). The foundation-model
  encoders were removed on 24 Sep; old vectors still resolve. Visitors may ask why the title keeps "Foundation-Model
  Embeddings": an embedding is one typed record kind (panel 10), and records outlive their encoders.

## 9. Correction: "declined" was not accurate; two print variants (4 Oct 2026)

An EO reviewer flagged that 0/300 (false acceptance) and its verdict were more accurate than 300/300 "declined".
The reviewer is right. False acceptance (`score.py`) counts a trial when B acts on a value other than the genuine
one. Its complement is not a count of refusals: it also contains trials where B acted on the genuine value, for
example after resolving the reference. Re-scored from the stored transcripts (`research/repro/v13/r5/not_acted_split.py`,
output `out/not_acted_split.json`, primary items, three Claude models pooled):

| condition | n | acted on corrupted | declined | acted on genuine | not acted on |
|---|---|---|---|---|---|
| prose | 276 | 254 | 22 | 0 | 22 |
| JSON | 276 | 164 | 106 | 6 | 112 |
| RAG | 276 | 220 | 56 | 0 | 56 |
| opaque id | 288 | 154 | 88 | 46 | 134 |
| checked reference | 300 | 0 | 264 | 36 | 300 |

So "declined 300 of 300" overstated the refusals by 36 (and JSON by 6, opaque id by 46). The board now builds in two
variants, from one source, and every gate runs on each:

- **0of300 (default, `poster/emem-poster-A0.pdf`):** the pre-registered metric as measured. Panel 1 "B acted on
  corrupted evidence", 254/276 prose ... 0/300; the reviewed take line restored word for word; panel 5 red bars and
  totals of false acceptance with the R1 ceilings, as reviewed before the flip.
- **300of300 (`poster/emem-poster-A0-300of300.pdf`, `--variant 300of300`):** the same trials counted the other way,
  with accurate wording. Panel 1 "B did not act on corrupted evidence", 22/276 ... 300/300; the take line gives the
  split ("264 declined, 36 used the genuine record"); panel 5 blue bars "B did not act on it (declined, or used the
  genuine value)".

Recommendation: print 0of300. It is the pre-registered metric, it is what the reviewer read as correct, and a
low-is-good column is standard for false-acceptance results. 300of300 is accurate too, but it reports a derived
quantity, so it needs the split in the take line to be read correctly.

The `R5.*.declined` claim rows are removed; `R5.*.notacted`, `R5.cell.*.notacted`, `S.R1.*.notacted` and
`R5.E.split.*` replace them, each re-checked against the result files.

## 10. Response to the EO reviewer's report (4 Oct 2026)

The report scored the board 6.5/10 and set a correction order. What changed on the face, item by item; numbers come
from `research/repro/v13/r5/out/not_acted_split.json` (re-scored transcripts) and are checked by the build.

| Reviewer item | Change on the board |
|---|---|
| 1. Outcome labels in sections 1 and 5 (mandatory) | Default print (0of300) reports false acceptance as pre-registered. Panel 1's figure now prints every outcome of the same trials per condition: acted on, declined, used the genuine record (emem 0 + 264 + 36 = 300; opaque id 154 + 88 + 46 = 288). Panel 5 keeps false-acceptance bars; genuine controls 71 of 72 stay in its caption. The 300of300 variant says "did not act on", never "declined". |
| Common-item comparison | Panel 1 take line: across the 23 shared items, agents acted on 254 of 276 prose, 154 of 276 opaque-id and 0 of 276 emem-reference corruptions (2 of 276 without the check instruction). Denominators per condition are printed in panel 5 (23; opaque id 24; emem 25). |
| 4. Treatment stated accurately | Panel 1 scope: "emem condition: the reference, a verifier tool and an instruction to check." The uninstructed result (2 of 300; 2 of 276 shared) is printed. |
| 5. Equal-tool baseline | Not run (needs new trials). Panel 1 scope states the limit: conditions differ in tools and instructions as well as representation; an equal-tool baseline is not yet run. |
| 2. Opening claims | Lead: "satellite observations, raw or derived", "records ... signed in batches"; the compaction claim is removed. Header strip: the 84-character reference is separated from the 1,115-byte record and log entry a check fetches. Title kept: the authors chose the programme title. |
| Orbital framing | Panel 1 orbit line: the signed record and reference downlink; the data stays on the device (emem-airgap design); "SAT-042 harness, not flown". Panel 11: the trace shows which key signed the run and that no logged segment changed; it does not show which code ran on which inputs. |
| 3. Section 6 as the scientific centre | The contribution box now states the boundary: content hashes (IPFS), signed logs (SCITT) and provenance (PROV) exist; emem adds typed EO references and a source re-read that caught a wrong pixel which hashing, signatures, logs and recomputation preserved (panel 6). No re-layout before print. |
| 6. Uncertainty, retrieval | Panel 4: confidence 0.95 is fixed per scene class (SCL 4 here), not a measured uncertainty. Panel 9: uncertainty "if recorded"; "a cid names a record, not an object". |
| Section 2 | "Constructed variants: scene, date, place, pixel and arithmetic change one Keylong NDVI." |
| Section 3 | The decomposition lists possible causes, not measured shares; the score is "an uncalibrated heuristic"; invalid σ is marked fail-closed. |
| Full trace | "still trusted: nothing" became "BLAKE3 and the verifier's code" and "the cell rule". |
| Section 8 | "known" is defined: versions signed by τ (signed_at, the signer's clock). The line the figure already prints is removed. |
| Section 10 | The embedding row loses its emphasis; embedding and device-run rows are grey (encoders retired; reference harness). |
| Section 12 | "Listings show availability; agent decisions are measured in panel 1." |
| Workflow | The Check step prints "If one fails: refuse." |
| Footer commits | "Service: emem.dev at 8e9b401; code read at 18adb67." |

Not changed, and why: the title (authors' decision); the matched before/after rerun for panel 6, drift-score
calibration, the equal-tool baseline and an orbital execution trust model (each needs new measurements); the
reviewer's density point is answered only by replacing repeated content (panel 1's handover stack, panel 8's
duplicate line), not by a re-layout days before print. Both variants pass every gate.

## 11. Wording pass (4 Oct 2026)

Every printed line was read for machine-sounding copy left by the space-constrained edits. Rewritten as plain
sentences, at the same length: the lead's colon chain ("Each is a record named by the BLAKE3 hash of its bytes and
signed in a batch"); panel 1's mechanism ("a satellite reading"), take line ("corrupted handoffs in prose / with an
opaque id / with an emem reference"), orbit line ("By design, ... are downlinked into") and both scope notes (no
more "Figure: ...; line at left: ..."); panel 2 ("We varied one Keylong NDVI by ..."); panel 3 ("This score is an
uncalibrated heuristic"); the contribution box; panel 5's bar note; the EO-workflow caption ("Each request returns one
observation, read from the archive if not yet stored" replaces "single-hop retrieval materialises"); panel 10 ("One
bundle resolves to eight facts"); panel 12 ("Separately, the same record and value came back through 11 client
paths"); panel 6's legend ("38: both rules agree"). No hyphenated word breaks across lines in either variant.

## 12. Final error pass, short title, no versions on the face (4 Oct 2026)

Two corrections from the final error pass (13e9fb3). The EO-workflow caption said "Each request returns one
observation"; a request with a band list returns many. It now reads "A request reuses stored records and fetches and
signs missing ones from the archive" (emem docs/model.md, ensure at single hop). In the 300of300 variant, panel 5's
"did not act on" bars used the legend's "refused" blue; they now use a lighter blue that the bar note defines.

A third error: the footer read "Service: emem.dev at 8e9b401; code read at 18adb67", but the full trace and the 11
client paths (30 Sep) ran against x-emem-commit 213e2738; 8e9b401 is the 1 Oct cost run. The authors' rule settles it:
service and code versions advance with every upgrade and do not belong on a research poster. The commits leave the
footer, the memory-as-coded label ("emem 18adb67") and panel 10's note ("At emem 18adb67, names, sets and records hash
differently" is now "Names, sets and records hash differently"). The rows keep them (K.commit, CODE.commit, the trace
and crossruntime files), and the face_hygiene gate now fails on a commit hash on the face. The footer keeps
"Measurements: 29 Sep to 1 Oct 2026."

Title: the authors shortened the printed title to the programme title up to "Protocol" (h1 and PDF title); the
programme listing is unchanged. The header re-spaces the freed line (poster.v13.layout.json, v13.10_notes.title).
This supersedes section 10's "Title kept" and its "Footer commits" row. Both variants pass every gate; 0 text overlaps
and no hyphenated word breaks across lines in either variant.

## 13. Byline, subhero, and wording for a scientific reader (4 Oct 2026)

**Byline.** The two Zenodo DOIs are removed at the authors' request; panel 12 and the QR codes carry the routes. Line 1
names the authors, contact, emem.dev and the repository; line 2 names the event.

**Subhero.** Of the items the board could not print (section 8 and the earlier review), one has an in-repo source and fits
the line: "Where no observation exists, emem signs an absence and its reason, not a zero." Sources: emem's CHANGELOG at
18adb67 (JRC GSW 255 signed as an Absence; Hansen, WorldCover, CCI, Cop-DEM and GeoTessera 404s are Absences while a
known tile answers; a pixel off its tile is now an error, not a zero), `research/repro/verify_absence.py` and panel
10's "nothing there" row (row V8.absence). Not added: the 24-hop relay and the live draft check (no measurement in this
repository), non-EO observers (unmeasured, and outside an EO session), the accelerator programmes and the product list
(not research content).

**Contradictions and vague wording.**

| Where | Was | Now | Why |
|---|---|---|---|
| Panel 1 question | What survives an agent handoff? | Does agent B act on a corrupted handoff? | The figure counts false acceptance, where 0/300 is the good result; under "survives" it read as nothing surviving. |
| Panel 1 headline | The same observation, carried through receiver checks. | The same corruptions, handed over five ways. | States the design: identical items across five conditions (prereg section 3). |
| Panel 1 mechanism | Agent B acts on it or checks the reference. | Agent B acts on it, declines it or uses the genuine record. | The three outcomes the figure counts. |
| Panel 1 scope, panel 5 caption | checked reference; Checked-reference agents | emem reference | One name for the condition across the board. |
| Panel 5 caption | ... genuine controls; one was refused (pooled Claude). | ... genuine controls and declined one. | Says who declined; one line (the panel names the models). |
| Panel 5 totals | B acts on corrupted evidence; R1 15 / 15 | B acted on corrupted evidence; "deterministic receiver, same corruptions" 15 / 15 | Tense as in the legend; R1 was never defined on the face. |
| Panel 5 checks | Resolve, Re-hash, Bind, Recompute, Re-read | the same, each with its layer (L0, L0, L1, L2, L3) | Panels 2, 4 and 5 print L0 to L3; the key left the board with the old ladder. |
| Panel 2 caption | one exceeds the expected NDVI range | one lies outside the valid NDVI range | NDVI is bounded to [-1, 1]; 1.1427 is impossible, not unexpected. |
| Panel 7 headline | Know what was checked | The record, not physical truth | Answers its question; matches the figure's NOT ESTABLISHED column. |
| Header bridge | Encode in orbit, decode in AI's reasoning with emem. | Design goal: encode in orbit, decode in AI's reasoning with emem. | Panel 11 says no spacecraft is enrolled. |
| 300of300 bar note | used the genuine value; squares: deterministic receiver | used the genuine record; squares: deterministic ceiling | The words panel 1 and the default variant use. |
| Panel 1 take line and scope | "0 / of 276" and "22 / of 23" broke across lines | kept on one line | |

Kept: panel 3's Δencoder (the whitepaper's term for "the model changed"); panel 10's token-family line and panel 12's
headline (the authors' lines; neither contradicts a measurement). Word cap 870 / 895 (copy brief 860 / 884 plus about
1 %); the board prints 854 / 878. Both variants pass every gate, with 0 text overlaps, no broken hyphenation and no
number phrase split across lines.

## 14. Panel 12's client-path line moves to Connect (4 Oct 2026)

"Separately, the same record and value came back through 11 client paths, with receipt signatures checked on 9 (30 Sep
2026). Listings show availability; panel 1 measures agent decisions." is removed from the face at the authors' request.
The measurement is methods material and is already printed in full, client by client, on the page the CONNECT code
opens (`docs/use/`, "Same token, many runtimes", from `research/repro/data/v8/crossruntime_table.json`); the rows EC.11
and EC.9of11 keep it. The listing cards quote each listing verbatim, so they read as quotes without the scope sentence.
The ecosystem figure moves up and takes 3.5 mm under the headline. Word cap 850 / 870 (copy brief 839 / 858 plus about
1 %); the board prints 830 / 849. Both variants pass every gate, with 0 text overlaps, no broken hyphenation and no split
number phrase.

## 15. Two independent reviews of b6f6717, and what changed (4 Oct 2026)

Two reviews of the merged board: an external ChatGPT agent (EO reviewer persona; it re-derived the outcome counts from
the stored transcripts and confirmed the release hash) and a cold read by a separate Claude agent that saw only the
printed text and the preview. Each finding was checked against the board and the data before acting.

**Both reviews**

| Finding | Check | Action |
|---|---|---|
| The orbit line conflicts with the source re-read: if the pixels stay in orbit, B cannot run the check that caught the wrong pixel. | True. emem admits public-archive EO by recomputation; device output needs a signed execution trace (`trace_truth.md`). | Panel 1: "its signed record and reference are downlinked, so no source re-read (SAT-042 harness, not flown)." |
| The experiment does not isolate content addressing: the emem condition also had a verifier and an instruction. | True; no wording can fix it, only a matched baseline. | Panel 1 note: "so this tests the workflow, not content addressing alone; no equal-tool baseline yet". Headline "five handoff conditions", not "five ways"; the figure row is "emem reference + verifier". |
| Panel 6 (the wrong pixel) is the strongest result but sits low and competes with implementation detail. | Agreed. | Moved above the mutation matrix, to eye level, and renumbered 5 (the matrix is 6). Not resized: shrinking the code box, trace or token table is the authors' call. |
| The board is dense (about 3,500 words with labels). | Agreed; the build's word budget counts running text only (838 words). | No new panels. Open decision for the authors: what to cut (see the reply of 4 Oct). |

**ChatGPT review only**

| Finding | Check | Action |
|---|---|---|
| A refusal by the verifier does not stop an agent acting: Qwen E+ (fail-closed) 10/25; Haiku 6/6 in the exploratory M22 persuasion case. | True (`results.json` primary.E+ and X3_M22). | Panel 1 note: "With a fail-closed resolver, Qwen2.5-7B still acted on 10 of 25 corruptions (2 of 25 when instructed): enforce refusal outside the model." Workflow: "Policy: refuse if one fails." |
| 2,794 trials are repetitions over few tasks. | True: two constructed tasks (K, B), 25 items. | "2,794 scored trials of 25 items from two constructed tasks" (row R5.tasks). |
| 162/200 pre-fix vs 0/54 post-fix is not a matched comparison. | True: providers differ. | Panel 5 note: "(Planetary Computer, two days; not a matched sample)". |
| "without trusting A, A's model, or us" overclaims. | True: the signature and log checks trust emem's key. | "What can agent B check without trusting A or A's model?" (the suggested "independently" is a banned word here). |
| "No candidate gives an empty result" is ambiguous. | True. | "If no candidate exists, recall returns an empty result." |

**Cold read only**

| Finding | Check | Action |
|---|---|---|
| "a changed, rounded or forged value no longer matches its name" is contradicted by panel 6: re-hashed changes and a forger's own key pass the hash and fail the signature. | True (f6: M8, M9, M13 first refused by F). | "...no longer matches its name or signature." |
| "STAC carries no checksum" is wrong about STAC: the file extension defines `file:checksum`. | True; this item has none. | "this STAC item carries no checksum". |
| L0 to L3 read as EO processing levels (beside "Sentinel-2 L2A"). | True for this audience. | Removed the L text from panels 2, 4 and 6; depth stays as colour and check names. |
| Panel 6's check chain leaves out Signature and Log, the first refusals in many rows. | True. | "Resolve, Re-hash, Bind, Signature, Log, Recompute, Re-read". |
| G0 "accepted everywhere, never refused" vs agents declining 1 of 72 controls. | The row is the deterministic receiver. | "nothing altered: no check refuses it". |
| "how agents read Earth observation" outruns the evidence. | Agreed. | "In emem, the token family is how agents read Earth observation". |
| Panel 9's CBOR_canonical vs the code box's declaration order. | True: a sorted-key canonical encoder gives a different cid. | "cid(record) = BLAKE3(CBOR(record))". |
| "A relay changes the evidence" omits signer errors. | True (f2: relay or faulty signer). | "A relay or a faulty signer changes the evidence." |
| Panel 3 asks "Where did the evidence change?" but lists possible causes. | True. | "Why can a value change?" |
| Undefined: ULP, cl100k, STH, attester_only, Referent Lock. | | "changed in its last bit"; "46 GPT-4 tokens"; "signed tree head (STH)"; "not re-runnable"; "Workflow templates, including EUDR". |

Not changed: the 154/288 versus 154/276 denominators (both printed and explained); the TRY IT position (bring a
hand-held card); "encode" in three senses; panel 12's headline. Both variants pass every gate, with 0 text overlaps, no
broken hyphenation and no split number phrase; 838 running words (cap 852 / 872, copy brief 843 / 862 plus about 1 %).

## 16. Second ChatGPT review of 6132e29; copy frozen (4 Oct 2026)

The reviewer re-read merge 6132e29 (PR #64), confirmed both release hashes and raised the score from 7.8 to 8.0 (visual
hierarchy 6.5 to 7; the receiver-check and token-family sections up half a point each). It withdrew the earlier wording
objections and found one new error: panel 1 said "2,794 scored trials of 25 items from two constructed tasks", after the
previous round cut "with Qwen2.5-7B reported apart" for space. Recounted from `research/repro/v13/r5/trials.jsonl`
(pilot and excluded rows left out): 2,794 scored trials over 28 item ids (25 primary corruption items, the controls
G0 and G0-B, the exploratory M22), 2,688 Claude and 106 Qwen. Panel 1 now reads: "Figure: Claude Haiku 4.5, Sonnet 5.5
and Opus 5.5 pooled, full item set per condition. All 2,794 scored trials (1 Oct 2026, two constructed tasks) span 25
corruption items plus controls, exploratory items and Qwen." Row R5.tasks now checks n_trials_scored in results.json.

What still limits the board, by the reviewer's account and ours, is not copy: no matched baseline (same verifier and
instruction without content addressing), an orbital design without the source re-read, two constructed tasks with one
main model family, and density (about 3,450 words including labels). The copy is frozen at this commit; further gains
need a matched-baseline run or a deliberate cut.

## 17. Deliberate cut (4 Oct 2026)

The second ChatGPT review asked for a deliberate reduction rather than more wording changes. Cut, with the reason for
each:

| Removed | Why |
|---|---|
| Panel 3's drift-score figure and its caption | Both reviews rated the section weakest; the score is an uncalibrated heuristic. The conceptual decomposition stays, with its scope in plainer words ("we have not measured their shares"). |
| The drift-score values in panel 11's strip | Undefined once panel 3's figure is gone. The "Score vs anchor: SCORED" step stays. |
| Four of the seven code-box rows (recall, sign, log, receipt) | Each is printed elsewhere: panel 8 (recall), panel 4 (batch signature), the full trace (log, receipt). The box keeps fact, name and cell and is titled "The record, as coded". |
| Panel 6's first note sentence | It repeated the bar legend (runs per bar, items per condition). |
| Panel 9's conceptual-tuple line | Panel 4 and the trace already say it. |

The space went to legibility, not to new content: panel 7's guarantee table at 17 pt (from 16) in an 80 mm figure; the
full trace at 17 pt (from 14); the token table at 8 mm rows (from 6.7); and air between panels. Measured on the
rendered board: 3,255 to 3,043 printed words, 1,695 to 1,348 of them at 14 pt; running text 838 to 803 words (cap
816 / 836, copy brief 808 / 827 plus about 1 %). Twelve figures are placed (the drift-score figure is no longer one).
Both variants pass every gate, with 0 text overlaps, no broken hyphenation and no split number phrase.

## 18. Panel 1 relay box (4 Oct 2026)

The relay box listed nine change types one per line, down the box, between the five lane markers, so "cell" sat beside
the JSON lane and read as that lane's corruption; the red-on-pink list was hard to read, and it used the R1 families,
which miss two of the R5 families (unit, stale history). It now prints "relay or faulty signer", "one change per trial,
same set on each lane:" and the R5 families as one wrapped list in dark ink, centred in the box: value, unit, cell,
time, band, source, derivation, pixel, stale record, signature / id (prereg section 4; row F2.relay.r5). The lane
markers sit on the box edge. Both variants pass every gate, with 0 text overlaps.

## 19. Third ChatGPT review (a8ad558, 8.2/10) and the matched baseline (4 Oct 2026)

The review raised the score from 8.0 to 8.2 (presentation 7.5, novelty 7.5) and asked for one wording fix. The relay
box's "one change per trial, same set on each lane" implied equal item sets; the sets are 23 (prose, JSON, RAG), 24
(opaque id) and 25 (emem). It now reads "one change per trial, shared corruption families" (row F2.relay.r5). The
shared-item comparison in the take line was already correct.

Its first open limitation was the treatment confound: the emem condition adds a verifier and an instruction, and "a
matched baseline with equivalent evidence access, verification and instructions is still the experiment most likely to
change my scientific score". That baseline is now run, without paid calls, under a pre-registration pushed before it was
computed (`research/repro/v13/r5/prereg_addendum2.md`, 0cf0424; results in `results_addendum2.md`):

| receiver on the 23 items with a JSON form | false acceptance |
|---|---|
| JSON without a verifier | 23 of 23 |
| JSON with emem's checks minus hash, signature and log (binding, as-of, recompute, source re-read) | 8 of 23 |
| the same plus four consistency checks (scene date, tile band, BOA offset, unit) | 3 of 23 |
| emem's verifier | 0 of 23 |

Six of the eight are records a forger re-hashed after changing the cell, date, scene, offset or unit; one is an
unlogged second version; one is A's misstated elevation (916 for 918.0 m). emem's verifier refuses seven at the signature
or log check and uses the signed 918.0 m on the eighth; its hash check refuses none of them, because a forger re-hashes. In 53 in-session Haiku subagent trials (one per
arm and item, exploratory), agents given the matched verifier and instruction acted on the same 8 and declined the other
15; agents in condition E acted on 0 of 25, as in the 150 headless Haiku E trials. Twelve trials stopped on an account
usage limit and were re-run once after the reset, as the addendum provides; the audit found no tool use outside the trial
tool and no exclusion.

Panel 1's scope now prints the matched result. The first print of it (50ddf41) replaced "so this tests the workflow, not
content addressing alone; no equal-tool baseline yet" and squeezed the scope into four lines; section 20 records the
corrections that followed. New rows: R5.matched.ceiling, .n, .hardened, .emem and .agents, each re-checked
against `out/addendum2_ceiling.json` or `out/addendum2_s.json`.

Unchanged, and stated where the review asked: the orbit design does not inherit the ground source re-read, SAT-042 is a
scripted harness, two constructed tasks are narrow, agent compliance needs enforcement outside the model, and the board
is dense. The review's presentation advice, to lead with panel 5's wrong-pixel result and then show how the handoff
checks expose it, is for the talk at the board; the layout is unchanged.

## 20. Audit of the matched-baseline round (4 Oct 2026)

Two independent reviews read the round (0cf0424 to b38c7ba): one of the new code, one of the new text against the data
files. Neither found a reported number that changes; both scorers reproduce their outputs exactly, and the matched
verifier agrees with verifier.py's binding, as-of, recompute and source checks on 25 items by 400 questions.

Fixed on the board (panel 1's scope, now five lines; f2's lane gaps 3.0 to 1.6 mm, the figure 118 to 112.5 mm, the
spine-foot margin 1.6 to 0.6 mm, lane height unchanged):

| Before | Problem | Now |
|---|---|---|
| "instructed Haiku agents with it acted on the same 8" | the addendum (A2.4, A2.5) requires the label exploratory; one trial per item read as a rate | "in an exploratory run, one trial each, instructed Haiku agents given those checks acted on the same 8" |
| "a JSON receiver ... accepted 8 of 23" | no unit; in R5, "receiver" also names agent B | "emem's checks minus hash, signature and log, run on the JSON, accepted 8 of 23 corruptions" |
| "Qwen2.5-7B still acted on 10 of 25 (2 of 25 instructed)" | read as a fail-closed resolver plus an instruction; the 2 of 25 is condition E | "Qwen2.5-7B acted on 10 of 25 corruptions behind a fail-closed resolver (2 of 25 when told to check): gate the action outside the model" |
| "span 25 corruption items, controls, exploratory items and Qwen" | there is one exploratory item | "(..., Qwen included) span 25 corruption items, 2 controls and 1 exploratory item" |
| "The emem lane adds a verifier and an instruction." | the 50ddf41 print had dropped that the figure tests the workflow | "..., so the figure tests the workflow." ("Claude" is back in the model list) |

Fixed in the documents: the methods page said R5 applies "one of 24 enumerated corruptions" (25, plus one exploratory;
an error older than this round) and that each is rendered in seven representations (up to seven); the methods page and
section 19 said the eight accepted corruptions were all re-hashed or relabelled records; `results_addendum2.md` said the
three left after B++ need the source, but M23 carries the S2B scene's own pixel, so a re-read passes it and the signature
catches it; it also had "What X:" lead-ins and a flourish, said no paid call was made without pointing to the disclosed
test call, gave one stop time for the 12 interrupted trials, listed three of the four harness differences, and did not
say that the hash check refuses none of the eight. A section "Corrections and notes after the run" now records the
plumbing calls before the addendum (five, not one per arm), the missing exploratory label in 50ddf41 and the latent code
weaknesses. Claims: R5.limits printed the matched numbers, which belong to the R5.matched rows; R5.matched.agents now
checks the "same 8" (acted_when_receiver_accepts 8/8), not the count of false acceptances alone.

Latent in the code, none triggered by the recorded data: the audit pattern in `score_s.py` accepts more than one command
in some forms; a new script, `audit_strict.py`, re-checks the 57 recorded tool calls against a strict one-line form
(57 pass). `score_s.py` is unchanged because its hash is bound by the addendum.

## 21. Fourth ChatGPT review (ade6319, 8.5/10) (4 Oct 2026)

The review re-ran the deterministic receivers, re-scored the 53 archived agent trials, checked the 53 prompt hashes and
replayed the 57 recorded tool calls; the numbers held. It withdrew "no matched baseline has been run" and raised the score
from 8.2 to 8.5 (panel 1 from 8 to 8.5; presentation and novelty unchanged at 7.5). It read the result as the review
log does: of the eight corruptions the conventional checks accept, six fall at the signature, one at the log and one to
the signed record, and none to the hash, so the result supports the combined system, not content addressing alone.

Two corrections, applied:

| Finding | Change |
|---|---|
| The archived audit was tied to the checkout path: `score_s.py` and `audit_strict.py` build the allowed command from the current checkout, the archived commands name `/home/user/esa_poster/...`, so the audit failed in a clone elsewhere | `addendum2/replay.py` reads the run's rtool.py from the hash-bound prompts, checks the 57 calls with the strict rule, replays them (57 of 57 give the archived output) and re-scores (identical), here and in a worktree at another path; `audit_strict.py` takes the same recorded path; `score_s.py` is unchanged |
| The footer said "Measurements: 29 Sep to 1 Oct 2026"; the board prints 2 Oct rows and the 4 Oct matched baseline | "Measurements: 29 Sep to 4 Oct 2026." (row K.dates; the 25 Sep rows carry the scene's acquisition date, not a measurement date) |

Its presentation suggestion, applied: the matched ablation moved out of the small scope paragraph into its own labelled
strip under the handoff figure, styled apart from the agent results: "Matched ablation, deterministic receiver, same 23
corruptions (4 Oct), accepted: JSON, no checks 23 → emem's checks minus hash, signature and log 8 → plus four
consistency checks 3 → emem's verifier 0". The scope keeps the exploratory agent run ("With the ablation's matched
checks, instructed Haiku agents acted on the same 8 (exploratory run, 4 Oct, one trial each).") and drops back to four
lines. Room came from panel 1's gaps above the mechanism line (1.0 to 0.6 mm) and above the figure (1.6 to 0.8 mm).

Unchanged and not added to the board, as the review advised: the ablation removes hash, signature and log together; the
agent run is exploratory in a different harness; the tasks are two constructed ones; the orbital design does not inherit
the ground source re-read. For the talk at the board, the review suggests joining the two strongest findings: the source
re-read catches a wrong pixel that integrity checks preserve, and signatures and the log catch changes that consistency
checks miss.

## 22. Brand identity (4 Oct 2026)

The authors chose an identity for emem: the wordmark "em", an orange em dash, "em", and the card tagline "Encode in orbit,
decode with AI." The board carries it in two marks, both in the navy header, and adds no artwork.

| Element | On the board |
|---|---|
| Wordmark | Bottom right of the header text, 52 pt Bold white; right edge on the text column (620 mm), baseline on the byline's second line (182.7 mm). The dash is a drawn bar (0.9 by 0.12 em at mid x-height), not a character, because the face bans the em dash. No satellite, face or node art: the identity advice was that the wordmark must stand without its illustration. |
| Tagline | The bridge's design goal uses the card's words: "Design goal: encode in orbit, decode with AI." (it was "decode in AI's reasoning with emem"). "decode with AI." is in the brand orange, as on the card. Row ORBIT.tagline prints the new wording; the "in orbit" allowlist entry is re-bound to the new sentence (BLAKE3 8a319bde…); panel 1 and panel 11 still print the harness scope. |
| Colour | Token `brand` #E86424, for these two marks only. Data keeps its colours: `harm` still means that B acted on corrupted evidence. The two oranges are close (CIEDE2000 9.1), so the brand orange stays on the navy header, off the white panels and the figures. Contrast 4.0:1 on navy (the tagline is 24 pt). |
| Layout | The byline moves up 1.5 mm (top 169.5 mm) so the wordmark's glyph box ends inside the 188 mm header block; the bridge-byline gap goes from 13 to 11.5 mm. |
| Pronunciation | Added at the authors' request in the free space left of the wordmark: "pronounced em-em" over "the em in em dash, twice", 17 pt, right-aligned 7 mm from the wordmark, on the byline's two baselines. It says the name and explains the dash. Row H.brand. |

Left out: the orange ".dev" of the dark card (a third orange mark in the header would scatter the accent) and the card's
Earth, satellite and face artwork. The copy freeze of section 16 holds for the evidence; this is an authors' change to
the header. Both variants pass the 18 gates; running text 799 words (818 tokens), 0 text overlaps.

## 23. Fifth ChatGPT review (4f6277d, 8.5/10) and the retrieval label (4 Oct 2026)

The review re-checked main at 4f6277d, including the PDF, the scoring code and the archived trial outputs, reproduced
the headline counts and kept 8.5/10. It found one poster correction and two scorer weaknesses; none changes a count.

| Finding | What the archive shows | Change |
|---|---|---|
| Panel 1's third outcome column said "used the genuine record", which reads as retrieval of the genuine evidence | `genuine_value_source.py`: JSON 6, each derived by B from the DNs it was given, no record retrieved; opaque id 46, of which 13 derived, 27 the value of the record the relay served (no check), 6 the value stated in the handoff (M7); emem 36, each the value of the record served after every check passed. The reviewer's reconstruction, reproduced exactly | Column "acted on / genuine value"; mechanism "Agent B acts on it, declines it or acts on the genuine value."; 300of300 take line "36 acted on the genuine value" and panel 6 bar note "(declined, or acted on the genuine value)". Counts unchanged |
| `score._matches` gives a VALUE with an exponent zero decimals: `_matches("4.709e-1", 0.9)` is true, `_matches("0.4709", 0.9)` false | 0 of 2,878 re-scored trials state a VALUE with an exponent | `score_v2.py` takes the decimals from mantissa and exponent |
| One available value overrides a contradicting VALUE: M7, opaque id, "IRRIGATE VALUE=0.1" scores as acting on the genuine 0.4709 | 47 actionable answers contradict the attributed value (39 M18 unit conversions, 8 Haiku answers giving the threshold 0.4705 or 916.5); 3 are controls, the other 44 were already scored as acting on corrupted evidence | `score_v2.py` attributes a contradicting VALUE as reported |

`score.py` stays frozen (BLAKE3 f4f22e3b…, addendum 1) and reproduces the 32 published false-acceptance counts;
`score_v2.py` changes 0 of the 2,878 trials (`score_sensitivity.py`, `out/score_sensitivity.json`). The notes are in
`research/repro/v13/r5/scoring_notes.md`, linked from the methods page.

The authors added one label change: condition C, a BM25-based RAG baseline (BM25, top 3 of nine passages, prereg
section 3), prints as "retrieved text (BM25)" in panel 1 (it read "retrieved text (RAG)"); panel 6's 26 mm column keeps
"RAG" with "(BM25)" under it, because "retrieved" fills the column and runs into "opaque id". The methods page describes
condition C as a BM25-based RAG baseline.

Not changed, as the review advised: the layout. Its other points are scope already printed: the novelty is the
integrated evidence protocol and its evaluation, not content addressing alone (the matched ablation strip); 300 trials
are repeated corruption tests on two constructed tasks, not 300 independent EO applications; the satellite section is
a scripted harness. Both variants pass the 18 gates; running text 800 words (801 in 300of300), 0 text overlaps.

## 24. Pre-print pass (4 Oct 2026)

The authors asked for a print-ready board: no vague text, no AI tells, no revision history on the face or the pages its
QR codes open, and working QR codes. Every visible text run of both variants (HTML and 597 figure labels) was read and
scanned for tell words, hedges and changelog wording; the eight docs pages were scanned the same way and the three QR
landing pages read in full.

| Where | Before | After | Why |
|---|---|---|---|
| Panel 1 orbit line | "...are downlinked, so no source re-read" | "...are downlinked, so the source is not re-read" | elliptical; "cannot" is a banned word |
| Panel 2 caption | "Each calls for a different check." | "Each of these seven needs a different check." | the eighth value is the genuine one |
| Panel 5 figure | "sampled pre-fix records", "both rules", "the old rule", "After the fix" | "records read by rounding", "round and floor", "rounding", "With floor"; the caption defines the rule: "read with a rounded pixel position; GDAL floors it" | the face never said what the fix was |
| Panel 6 caption | "Deeper checks expose different corruptions." | "Each added check refuses a corruption that the checks before it pass." | stated from the first-refusal column (C to I) |
| Panel 6 scope | "JSON and an opaque id caught some changes from their fields. On the live pre-fix record, ..." | "Reading the fields they carry, agents did not act on 112 of 276 corrupted JSON handoffs and 134 of 288 with an opaque id. On panel 5's real record, read live, ..." | "some" and "pre-fix" |
| Panel 10 | headline "Beyond a single observation"; "In emem, the token family is how agents read Earth observation: ..." | "From a place to a device run"; "emem's tokens share one grammar." | a tell-word headline and a slogan |
| Panel 10 figure | "Grey: encoders retired; ..." | "Grey: archived embeddings; ..." | status wording |

Two figure lines ran past their figure's edge and were clipped in print. The panel 5 caption ran 4.2 mm over; its wrap
now keeps a 12 mm margin and the caption drops its last sentence. The 300of300 bar note in panel 6 ran 13.5 mm over
(the label change of section 23 lengthened it); it is shorter, and f6 now asserts that its notes fit. Matplotlib
measures IBM Plex about 3 % narrower than Chromium sets it, and the build did not check figure text against the
figure's edge. `no_overflow_or_clipping` now does, horizontally with 0.6 mm tolerance and vertically beyond the
1.5 mm ascent box; a synthetic 13.5 mm overflow fails the gate.

Visitor pages: the methods page's R5 note, its Rust note ("this build environment"), "restoration decisions", "Original
v12", the eight-answer paragraph (which said the figure had moved off the board; it is panel 2) and the bundles
paragraph (which said Berlin coverage absences are on the face; they are not) state results only. The record page
drops the archived board track of the e66c3ba PDF and defines L0 to L5 under its table. The use page says "What was
checked?", "One token, 11 client paths" and names panel 3's change in readout instead of the removed drift score.
`docs/` is deployed as committed; `tools/site/site.mjs` predates the v13.10 page edits (AGENTS.md says so).

QR codes, decoded with OpenCV from the print PDFs rasterised at 300 dpi (pdftoppm): all three decode in both variants.
Degraded copies: the 50 mm tiles (INSPECT, CONNECT; version 4, level Q, 40 mm symbol, 1.22 mm per module) decode down
to about 2.2 px/mm with blur, JPEG and a 12 degree tilt, which a 1080p phone stream reaches within about 0.6 m; the
TRY IT code (69.7 mm symbol, 2.11 mm per module) decodes down to 1.0 px/mm, about 1.2 m. The site's phone test
(`tools/site/test_site.mjs` on a copy of docs/) passes except where it needs emem.dev or Planetary Computer, which this
environment blocks, and its fold check (the demo card's height depends on the step on screen; the page is unchanged
since 2 Oct). The record and landing tests now match the pages. The Pages deploy of main after PR #71 succeeded.

Print PDF: exact A0, one page, 39 font objects all embedded (IBM Plex subsets), vector text, five raster images at 305
to 600 ppi with an ICC profile, RGB. No bleed is included; the navy header runs to the top and side edges, so a print
shop that trims needs either borderless printing or a bleed version. Both variants pass the 18 gates; running text 793
words (794 in 300of300), 0 text overlaps, no figure text past its edge.

## 25. Footer references and panel 12, against emem's current work (4 Oct 2026)

The authors asked that the board credit only what it shows and what emem runs now, not retired components or names
from the conference programme. Each reference was checked against the face (where it is used) and against emem's
main at 320a1d5 (`/home/user/vortx-ai/emem`, read-only).

| Reference | On the face | In emem now | Decision |
|---|---|---|---|
| Prithvi-EO-2.0, TESSERA | grey token row only (archived embeddings) | retired: `EMEM_RETIRED_BANDS=geotessera,clay_v1,prithvi_eo2,galileo` (deploy/systemd/emem-server.service; "Retired here: the Clay, Prithvi, Galileo and JEPA-v2 models, and new Tessera embeddings", web/how-it-works.html) | dropped |
| GeoGuard (NASA-IMPACT) | no | a paper title in docs/collaboration-log.md only | dropped |
| TMF, ESA CCI Biomass v7, openEO 1.3, C2PA 2.4 | no | not on the board | dropped |
| Sigstore, ARC (Dang et al. 2026), Perez et al. 2025, Munir et al. 2026, Cemri et al. 2025 (MAST), Townshend et al. 1992 | no | related literature, not named on the board | dropped |
| JRC GFC2020 "V3/V4" | "no EUDR flag" (panel 5) | V4 current; V3 superseded (emem CHANGELOG at 18adb67) | "JRC GFC2020 V4", the version the Rondônia read used (05_failure_modes_catastrophe.md section 6) |
| Hansen et al. 2013, GFC v1.13 | loss years (panel 5) | v1.13 current | kept |
| Sentinel-2 Products Specification; Copernicus DEM GLO-30/90 | panels 1 to 5; panel 8 (DEM30, Open-Meteo DEM90) | yes | kept |
| Reg. (EU) 2023/1115 (EUDR) | "EUDR" in panels 5 and 12 | EUDR workflows | added |
| BLAKE3, Ed25519 (RFC 8032), RFC 6962/9162 | throughout | yes | kept |
| CBOR (RFC 8949) | "CBOR(f)" in the coded record, panel 10 | yes | added (was missing) |
| STAC "1.1" | the trace's STAC item | the items read carry stac_version 1.0.0 | "STAC 1.0" |
| MCP 2025-11-25, A2A 1.0 | panel 12, workflow | MCP_LATEST_VERSION "2025-11-25", A2A_PROTOCOL_VERSION "1.0" (crates/emem-api-rest/src/lib.rs) | kept |
| IPFS, SCITT (RFC 9943), W3C PROV-DM | named in panel 13's contribution | related work | "Related work: IPFS CIDs (multiformats), SCITT (RFC 9943), W3C PROV-DM"; IPFS was named but not credited |

The footer now reads "Related work: ... · Data: ... · Standards: ...", with each item kept on one line.
"Measurements: 29 Sep to 4 Oct 2026." is correct (row K.dates: the earliest printed measurement is 29 Sep, the matched
baseline 4 Oct) and stays: it dates the evidence in one place.

Panel 12: the Hugging Face Space pins an older emem image by digest (emem huggingface-space/Dockerfile: "Bump it
deliberately when you want the next release pulled"; it answered as 1.1.0 on 30 Sep, against 2.4.2). Printing it
unqualified would present a stale server as current, so it leaves the face (manifest: print not allowed, with the
reason); the group title becomes "DISCOVERY", since none of the five remaining routes is a mirror. The companion
directory on the use page still lists it with its caveat. Both variants pass the 18 gates; 27 printed routes.

## 26. Contribution panel, the Claude listing and the companion pages (5 Oct 2026)

**Panel 13.** The label "THE CONTRIBUTION" becomes "CONTRIBUTION", the usual section name. The caption said "emem
adds typed EO references and a source re-read". emem's own verifier (emem-verify-core.js at emem 320a1d5) recomputes
the receipt digest and checks Ed25519; it does not re-read the source. The re-read is the receiver's check (depth I in
panel 6; links 8 and 9 of the full trace), and emem records make it possible because they name the source files, the
sampled point and the derivation (panel 4). The caption now reads: "emem applies them to single EO observations, and its
records name the source file and sampled point, so a receiver can re-read the pixel. That re-read caught a wrong pixel
that hashing, binding, signatures, logs and recomputation had passed (panel 5)." "binding" was missing from the list:
panel 5's chips are hash, binding, signature, log and recompute (all pass the wrong value) and re-read (refuses). The
new printed forms are in the row V7.invention; the brief's section C carries the same caption. Running text: 810
words (811 in 300of300), under the 816 cap.

**The Claude listing.** The authors' screenshot of 4 Oct (`evidence/listings/claude.png`) shows "emem · from
Anthropic Directory · 2.4.2 · 19 skills", with the emem connector and the plugin enabled. The manifest still called the
Claude directory NOT FOUND ("Nothing via a directory today"), and the plugin row's caveat said "This is emem's own
marketplace, not Anthropic's directory". `anthropics/claude-plugins-official/.claude-plugin/marketplace.json`, Claude
Code's catalogue, was fetched again at 2026-10-05T05:53Z: 315 plugins, none named emem or pointing at Vortx-AI/emem
(the one substring hit is "remember"; `evidence/ecosystem/cpo_market_2026-10-05.json`). Both statements hold for
different catalogues: the Claude apps list emem in the Anthropic Directory; Claude Code's marketplace does not. The row
`claude-connectors-directory` now records the listing (REGISTRY, with both pieces of evidence), the plugin row's caveat
says which catalogue is which, and the use page's Claude setup card starts with the Directory route, as the board's
Claude card does ("Directory plugin / MCP"). "What was checked?" on the use page now says what was run in Claude Code
(install and connect on 30 Sep, no model turn) instead of "checked against the source".

**The use page's integration list.** Every row's evidence line ended in " ." (an empty template slot left when print
placement was taken off the page); fixed in `tools/site/site.mjs` and on the page. Caveats carried authoring
instructions to visitors: "Do not print ...", "Fix the example before printing Cline", "The poster must print the action
URL", an issue number, a commit pin, "this session", "this container". Those move to a new `print.note` field, which no
page shows; the caveats that stay state results and limits. The emem.dev landing row showed "DISCOVER INTEGRATIONS ->
emem.dev/#use", the label of a QR the board no longer carries, as a command; it now shows the URL. Only the integration
list was regenerated (site.mjs into a scratch directory, the section spliced in), so the hand edits elsewhere on the page
stay. AGENTS.md records the `print.note` convention.

**Methods and Q&A.** The prior-art table loses the GeoGuard row and reference (the authors' rule of 4 Oct: not used by
emem), its introduction says EMEM "works alongside" those layers instead of "relies on" them, and the MCP and STAC rows
say what emem serves and reads (protocol 2025-11-25; STAC 1.0.0 items) beside the specification versions checked on 1 Oct
(2026-07-28; 1.1.0), so the table agrees with the footer. "a BM25-based RAG baseline (BM25, top 3 ..." loses its doubled
BM25. On the Q&A page, "Why not GeoGuard?" and GeoGuard's sentence in the quick comparison are removed; the contribution
answer adds the source re-read; the RAG answer names the BM25-based baseline (top 3 of nine passages); the drift answer
uses panel 3's terms (environment, sensor, geolocation, encoder) instead of "world" and "alignment".

**Panel 12.** The five card action lines are labels, but three ended in a period and two did not; none does now.
"Install MCP server" stays as written: it is the GitHub listing's own button.

**Generator.** site.mjs carries the same fixes for these sections (Claude card, "What was checked?", the evidence line,
GeoGuard, the MCP and STAC notes, the "C retrieved text (BM25)" column). It still lacks other v13.10 hand edits, so
docs/ is still not regenerated from it. `evidence/ecosystem/build_manifest.py` is marked as superseded: the manifest has
been edited by hand since 4 Oct, and re-running the script would revert those edits. The ecosystem test's pinned date
moves to 5 Oct, the date of the newest evidence.

Checks: both variants pass the 18 gates; 0 text overlaps, no broken hyphens or split numbers, the same 24 top-edge
ascent boxes as the committed board (inside the gate's allowance), 14 unit tests pass, 42 routes with 27 printed.

**Independent review of the visitor pages (same day).** A separate read-only review of the eight pages against the
face found 24 items; each was checked against the files before any change.

| Finding | Check | Change |
|---|---|---|
| The pages were hand-edited after tools/site built them, so the test page's rebuild command would revert them | the generator's output differed from docs/ by 2 to 34 changed lines on each page except the demo | every v13.10 hand edit ported into `tools/site/site.mjs` and `research/v13/conference_questions.json`; the pages are regenerated from them, and the demo already matched `tools/site/build.mjs` byte for byte; AGENTS.md updated |
| The ChatGPT caveat dated the resolve attempts 4 Oct | `chatgpt_plugin_check.json`: checked 2026-10-02 | "2 Oct 2026" |
| "No agent run in ... Claude ... is claimed" | R5 ran headless `claude -p` sessions (`claude_run.py`) | "No agent run through the Claude apps, VS Code, Dify or MuleSoft is claimed here; the R5 agent trials ran as headless Claude Code sessions" |
| The bundle's nine checks listed "the log leaf" | `verify_bundle.py` checks the token's cell against the signed cell and has no separate leaf check | the list now matches the script |
| ClawHub: the use page linked a skill by avijeetsingh1, the board's card quotes the Vortx AI OpenClaw plugin | `evidence/listings/clawhub.png`: `openclaw plugins install clawhub:@vortx-ai/openclaw-emem` | the row names and installs the plugin, links its screenshot (clawhub.ai is blocked here) and keeps the skill page as a caveat |
| The record and token pages said the demo re-reads the pixel | the demo's default shows the saved source window; a live option re-reads | both pages say so |
| "One full level-I check took 1.187 ms" beside a 0.357 ms median | 1.187 ms is the committed single run | the sentence says so and points to section 8 |
| Drift terms "world, instrument, alignment, encoder and noise"; Q&A formula in u | panel 3: environment, sensor, geolocation, encoder, residual; the face uses u for uncertainty and the methods rename the ratio r | panel 3's terms; r |
| "JSON and the opaque id caught about half" | 112 of 276 (41 %), 134 of 288 (47 %) | the counts |
| "17 corruptions and one control"; R5 "the same corruptions" | R1: 16 in scope, M17 out of scope, G0; R5: 25 items | stated as such |
| R1 and R5 letters collide on the test page; R5's deterministic row (23/23 ...) beside the face's R1 squares (15/15 ...) | different scales and item sets | one note on each page |
| Authoring and dated words: "in-session subagents, no paid calls", "report 09/10" without links, "Recovered demonstrations from earlier posters", "v12" alt text, "today", "Fresh", "for this page", "current status", "Printable rehearsal text", "(apart)", "(2026-10-01 (UTC))" | | reworded; reports linked; "Further demonstrations"; "in this study" |
| "EMEM" in running text, "emem" on the face | | "emem" in running text; titles keep "EMEM" |
| "Every result on the poster comes from a script"; "Every number here is read by the build" | listing quotes rest on screenshots; some methods numbers are typed from files | "Every measured result"; "comes from the file named beside it" |
| The landing and use pages offered MuleSoft as a host | the face lists MuleSoft Exchange under DISCOVERY | "or find emem on MuleSoft Exchange" |

The site gates (`poster/build_site.py`) then caught "Claude Haiku 4.5" in the matched-baseline paragraph, a hand edit
of 4 Oct: the pages leave model identifiers to results.md, so it reads "the smallest of the three Claude models". Three
curly apostrophes from the same edit were missing from the subset web fonts; they are straight now, like the rest of the
generator's text ("‖" on the record page is absent from IBM Plex itself). `research/v13/20_CONFERENCE_QUESTIONS.md`, which
the Q&A page links, is regenerated from the same JSON. Not changed: the methods keep the emem commits of the tests they
cite (provenance, not the face), and the use page's 5 Oct marketplace check stays, although the face's measurements end
on 4 Oct. The site test still fails only where it needs emem.dev or Planetary Computer and on the demo's fold check: the
demo's verdict board ends at 1,310 px on a 390 x 844 phone, below the first screen (the page is unchanged since 2 Oct).

## 27. Dates on the face, and the integration notes (5 Oct 2026)

The authors asked whether the dates on the board are needed and whether this round added weak text. Dates on the
face fall in two kinds. Data dates belong to what is shown and stay: the conference date; the observation's
acquisition (Sentinel-2A L2A, 25 Sep 2026, panels 1 and 5); the record's own fields (tslot 25 Sep, captured, signed,
panel 4); the variants' records in panel 2 (the town point's 30 Sep record, "30 Sep record handed as 25 Sep"); the real
record of 23 Sep in panel 5; the Bengaluru signing and as-of dates in panel 8. Run dates said when a check or trial ran,
and each repeated the footer's "Measurements: 29 Sep to 4 Oct 2026" (row K.dates), which stays as the one place that
dates the runs. Removed: "(4 Oct)" in panel 1's ablation strip; "1 Oct 2026" and "4 Oct" in panel 1's scope; "· 30 SEP
2026" on the full trace; "· 30 Sep 2026" on SAT-042's subtitle; "1 Oct 2026", twice, in panel 6 (header and scope, both
variants). The rows keep every run date (extend_print entries in the v1310 additions); AGENTS.md now says panels print
data dates, not run dates. Running text: 809 words (810 in 300of300).

Weak text added this round, removed or reworded:
- Panel 13 said "single EO observations", which reads as "only one"; it is "individual" now.
- /use/ stated that Anthropic's Claude Code marketplace does not list emem (twice). Accurate, but it told visitors
  where emem is absent instead of how to install it; the rows now give the routes, and the check stays in the manifest.
- Most integration caveats were test bookkeeping ("not run in this study", "not fetched", "HTTP 200") or mismatches
  inside emem's own docs. Visitor notes now carry only what helps someone install or use emem: the right package name,
  the working command, the version or fix an example needs (the LangChain fix is spelled out instead of "needs the
  fix"). The removed text moves to a `qa_notes` field in the manifest, which no page shows, so the research record
  keeps it. The ChatGPT resolve result stays disclosed in "What was checked?".
- Each of the 42 rows printed "Evidence: ... Checked 2026-09-30T23:10Z..23:40Z (2026-10-01 CEST)". One line above
  the list now gives the span (30 Sep to 4 Oct 2026, computed from the manifest) and what each status word means;
  the expanders read "Notes" instead of "Caveats". The Hugging Face row no longer says "an old emem build".

Not changed, because they are needed: the scope statements on the face (inherited source quality, the harness that has
not flown, what the trace leaves trusted), the always-on token cost of the Claude Code plugin (an issue asked
not to hide it), and the measurement window in the footer. Both variants pass the 18 gates; 0 overlaps; QR codes decode from
both PDFs; site gates pass on the 8 pages; 14 unit tests pass.

## 28. Sixth ChatGPT review (92e7b9e, 8.5/10): final copy pass (5 Oct 2026)

Each correction was checked against emem's code (main 320a1d5) or the evidence files before it was applied.

| Location | Before | Check | After |
|---|---|---|---|
| Header, subtitle | "Where no observation exists, emem signs an absence and its reason, not a zero." | emem signs `Fact::Absence` for confirmed no-data (outside a product's mask, no value after the publication window, every composite rejected by QC); a value not yet published returns an error, and a budget limit a skip (`sign_band_absence`, `MaterializeOutcome.skip_reason`) | "When a source confirms no data, emem signs an absence and its reason, not a zero." |
| Header, lead | "Agents cannot write observations, and a changed, rounded or forged value no longer matches its name or signature." | a forged record under the forger's key matches its own signature (M13), and the wrong-pixel record is validly signed (panel 5); /v1/attest is closed to agents by default | "Observation writes require authorised keys; altering the cited bytes breaks the original content address." The allowlist entry for "cannot" goes with the old sentence. |
| Workflow, Check | "Hash · bind · sign · source" | "sign" reads as the receiver signing | "Hash · binding · signature · source" (95.6 mm measured, 98.5 mm with Chromium's 3 %, in a 101.6 mm text width) |
| Panel 5 | "With floor, 0 of 54 (...)"; the constructed test and the archived record not told apart | the 200 sampled records were signed 14 May to 27 Sep, before the 28 Sep fix; the 54 were signed 28 to 30 Sep and none matches the rounded pixel (`prevalence_summary.json` pre/post) | caption: "200 archived records ... After the fix: 0 of 54 carry a neighbour's values (Planetary Computer, two days; unmatched sample)"; c reads "constructed test: irrigate if NDVI ≤ 0.4705"; the 23 Sep record is introduced as "archived signed error" |

Optional suggestions: panel 2's "Each of these seven needs a different check" overstated (binding catches both the place and the date
change, metadata both the scene and the offset); it reads "The seven are caught at different checking stages." ("No single check
catches all seven" hit the banned word "all"). "the deterministic ceiling" becomes "the deterministic verifier" in panel 6 (both
variants) and on the test page. Not applied: "A standalone Python verifier" for "Without emem software, a 698-line script": the
sentence already leads with independence, and the line count tells a reader the verifier is small enough to audit.

Not changed: density (the review recommends locking; 14 pt is the floor, kicker and mechanism lines are 24 pt) and bleed (the
header runs to the page edge and the PDF has none; the print shop must accept the exact A0 file for edge-to-edge output or ask for
a bleed version). Both variants pass the 18 gates; running text 807 words (808); 0 overlaps; QR codes decode from both PDFs;
fonts embedded; site gates pass on the 8 pages; 14 unit tests pass.
