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
