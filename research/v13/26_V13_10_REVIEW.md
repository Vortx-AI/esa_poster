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
