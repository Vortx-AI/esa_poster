# Each figure must tell a complete story

Snapshot: 2026-09-30

Poster-design research is consistent: viewers decide quickly, figures should carry the result, and posters should revolve around a few memorable findings rather than behave like mini-manuscripts.

Sources:
- NIH OITE poster guidance: https://www.training.nih.gov/creating-a-scientific-poster/
- PMC poster communication review: https://pmc.ncbi.nlm.nih.gov/articles/PMC6715027/
- 2026 poster-design primer: https://pubmed.ncbi.nlm.nih.gov/42178863/
- Systematic review: https://pmc.ncbi.nlm.nih.gov/articles/PMC13233160/
- Nature design principles: https://blogs.nature.com/blog/using-design-principles-to-inform-scientific-posters/
- Figure storytelling review: https://pmc.ncbi.nlm.nih.gov/articles/PMC10651103/

## Rule

Every major visual must answer by itself:
1. What happened?
2. Why does it matter?
3. What exactly can be checked?
4. What is the limit?

## Story 1 — DRIFT

Current evidence: a real Lahaul NDVI of 0.4871541501976284 became the prose approximation ≈0.49. With WATER if NDVI < 0.488, both models changed from WATER to SKIP.

Missing visual: make the rounding itself the event.

Suggested figure:

SATELLITE OBSERVATION 0.4871541501976284
  -> TOKEN -> exact value -> WATER ✓
  -> PROSE ≈0.49 -> 0.49 -> SKIP ✕
                         both models agree

Large caption: AGREEMENT CAN BE A SYMPTOM OF SHARED DRIFT.

The 0/72 and p=0.035 should be a small statistical badge, not the main visual.

## Story 2 — ADDRESS

Current Fig. 1 is correct but seven equal stages make the viewer work too hard.

Make the invention one visible transformation:
PHYSICAL OBSERVATION -> IMMUTABLE RECORD -> CONTENT ADDRESS.

Use one real observation card with CELL / BAND / TIME / VALUE / SOURCE / DERIVATION. Visually compress it into oj5cecci... and then emem:fact:<cell>:<cid>. On the right show the same record reappearing after resolve.

Only three checks: BYTES MATCH, CELL MATCH, ATTESTATION VALID.

Large caption: THE REFERENCE IS A FUNCTION OF THE RECORD IT NAMES.

## Story 3 — HANDOFF / LONG-RUN CONTINUITY

The missing image is the context-death event.

Show Agent A with a nearly full context window. Then a large CONTEXT RESET ×. Nearly everything disappears, but one emem:fact token crosses the break. Agent B / next session / another model resolves it back into the same observation card and continues.

Large caption: THE AGENT IS TEMPORARY. THE INVESTIGATION IS ADDRESSABLE.

## Story 4 — FIELD

The real imagery is strong, but the reasoning-object transition needs to be explicit.

Use the same AOI in three aligned columns:
SEE: true-colour tile
REASON: NDVI grid
CITE: emem:raster token -> artifact hash ✓

Below, turn the five scenes into a time strip under one emem:cube token. Put requested date above each scene and actual scene date below; show +26d, +15d, etc. as visible arrows.

Large caption: THE MODEL GETS THE FIELD — AND THE FIELD GETS AN ADDRESS.

## Story 5 — VERIFY

Do not make this look like terminal output.

Show a sentence under inspection: Bengaluru was 35 °C, cited by token. Beneath it show the resolved signed value 28.0 °C. Then a visible comparison 35.0 ≠ 28.0 -> DENY PROV_VALUE. Beside it show the corrected sentence 28.0 = 28.0 -> ALLOW.

Large caption: CHECK THE CLAIM AGAINST THE EVIDENCE BEFORE THE CLAIM LEAVES THE AGENT.

## Story 6 — HONEST LIMIT

Make the epistemic boundary visual rather than distributing it across prose:

EMEM CAN CHECK:
- same bytes?
- same cited place?
- who attested?
- append-only history?

EMEM CANNOT CHECK:
- sensor is physically correct?
- model understood the band?
- conclusion is true?
- ground truth is accurate?

Large caption: VERIFIABLE ≠ TRUE.

## Story 7 — REPRODUCE

One QR is correct. Turn it into a challenge:

DON'T TRUST THIS POSTER. VERIFY ONE FACT.

1. scan emem.dev
2. paste the printed token
3. resolve
4. re-hash
5. verify receipt

Print one complete real token immediately beside the QR.

## What the v5 poster is still missing

### A. A visual symbol for state surviving context
This is the most important missing image.

### B. A before/after drift story
The current results contain the data, but not yet the visceral 0.487154... -> ≈0.49 -> wrong action transition.

### C. One reusable visual object
Use the same observation card across ADDRESS, HANDOFF, VERIFY and DRIFT. Raster/cube become the larger analogue. This gives emem a visual grammar.

### D. One colour semantics
Black/white = scientific substrate; blue = addressed/verified; red = drift/mismatch; grey = context that may disappear.

### E. One visible scientific question
Can two independent agents refer to the same Earth observation after their contexts diverge?

### F. One visual conclusion
MODEL A / MODEL B / SESSION N / TOOL X -> emem:fact:<...> -> SAME CITED RECORD

Conclusion: REASONING MAY CHANGE. THE CITED OBSERVATION NEED NOT.

## Distance test

At 3 m: only question, DRIFT, ADDRESS, FIELD and one conclusion should dominate.
At 1.5 m: viewer should understand the drift experiment, CID mechanism, handoff continuity, raster/cube meaning and limits.
At 0.5 m: exact tokens, scene ids, p-values, caveats and reproduction details can appear.

The biggest remaining work is the 3 m layer: more story-shaped figures and fewer terminal-like boxes.