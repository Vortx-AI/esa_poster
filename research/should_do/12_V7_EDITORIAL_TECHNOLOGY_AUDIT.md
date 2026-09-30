# v7 editorial / technology audit

Snapshot: 2026-09-30

## Principle
Every element on the wall must do one of three jobs: DEFINE the invention, PROVE it, or LET A SCIENTIST REPRODUCE it. Everything else belongs in the repo or at emem.dev.

## AI-tell cleanup

Replace slogan-like abstractions with observed transformations.

REMOVE / AVOID:
- 'portable world-state'
- 'the agent is temporary, the world-state is not'
- 'emem changes the handoff unit'
- generic ASK / REASON workflow verbs
- repeated 'trust' language without naming the exact check
- feature-list prose inside boxes

PREFER:
- '0.487154 became ≈0.49. The decision flipped.'
- 'Agent B resolves the token to the bytes Agent A cited.'
- 'BLAKE3(bytes) = fact_cid.'
- 'wrong cell -> 409.'
- '35.0 != signed 28.0 -> DENY.'

## Technology triage

### SHOW LARGE
1. **fact_cid / emem:fact** — the core content-addressed signed observation record.
2. **raster / cube** — the EO-specific extension: spatial fields and fields-through-time as signed derivations.
3. **referential-drift experiment** — why this matters to multi-agent reasoning.
4. **long-horizon handoff / bundle** — how agents continue after context loss.
5. **claim guard** — observable value-level check before publication.

### SHOW SMALL BUT VISIBLE
6. **Tessera 128-D foundation embedding** — because the accepted title says 'over Foundation-Model Embeddings'. Show that an embedding is just another typed fact value, labelled `model_output`, with place/time/source/recipe around it.
7. **bundle** — <=256 facts under one 38-character handle (~23 LLM tokens). This is the concrete mechanism behind compact handoff. Also state that individual fact tokens do NOT save context (they cost ~9.5x the bare value).
8. **CIDv1** — the same BLAKE3 digest is also emitted as CIDv1 so generic IPFS/Filecoin/ATProto tooling can address the fact without rehashing. This is interoperability, not the invention.
9. **two clocks** — valid time vs transaction time. Use only the real 918.0 -> 915.07 m inset.

### KEEP OFF THE MAIN WALL
10. transparency log internals — rigour, not invention; keep one small 'append-only audit' phrase.
11. signed absence — excellent but secondary.
12. ULP derivation rules — excellent methods detail; repo / discussion material.
13. DID/federation — useful systems infrastructure, but it will drag the conversation toward identity/federation instead of the paper.
14. emem:tree — impressive chunk proof, but not central to the submitted title.
15. airgap/orbit — supporting future/edge story only; nothing is deployed in orbit.
16. EUDR / ground perception / cameras — product/application scope, not this poster's invention.

## Missing title alignment
The poster must visibly answer 'over Foundation-Model Embeddings'. Add one small strip:

Sentinel-2 -> Tessera encoder -> 128-D vector -> `model_output` fact -> fact_cid

Caption:
**THE EMBEDDING IS A VALUE. THE MEMORY IS THE ADDRESSABLE RECORD AROUND IT.**

Do not claim AlphaEarth integration; the slot is reserved/unused. Tessera is the live encoder.

## Missing long-horizon mechanism
Use the actual compact handoff object:

256 cited facts -> emem:bundle:<38 chars> -> context reset X -> next session resolves members

Badge:
`<=256 facts · 38 characters · ~23 LLM tokens`

Small honesty line:
`one fact token is ~51 LLM tokens; bundling, not individual tokens, is the compression mechanism.`

## Better workflow
Replace ASK -> LOCATE -> READ -> REASON -> CHECK -> HAND OFF -> CONTINUE with protocol/object operations:

`LOCATE -> MATERIALISE -> ADDRESS -> RESOLVE -> VERIFY -> GUARD -> HAND OFF`

Object transitions:
`place -> cell64 -> fact/raster/cube -> token -> exact bytes -> receipt/verdict -> token/bundle`

This is specific to emem and does not resemble a generic AI agent diagram.

## Better opening
Research question:
**If Agent A cites an Earth observation, can Agent B recover exactly what was cited after the context is gone?**

First visual line:
**0.4871541501976284 -> '≈ 0.49' -> decision flipped.**

Label it simply: `REFERENTIAL DRIFT`.

Then the answer:
**Hand over the address of the signed observation record.**

## Better section names
- `01 CONTENT ID` instead of `ADDRESS · the observation record names itself`
- `02 HANDOFF` instead of `HAND OFF · carry the address, not the paraphrase`
- `03 FIELD / CUBE` instead of `FIELD · give the model pixels...`
- `04 CLAIM CHECK` instead of `VERIFY · check the sentence...`

These sound like technical sections, not generated slogans.

## One-line comparison
Do not overbuild a competitor matrix. Four object boundaries are enough:
- STAC/COG -> asset/file
- openEO/Earth Engine -> process/computed object
- RAG/agent memory -> retrieved context
- emem -> signed observation/field address

## Final 3-metre reading order
1. Exact paper title
2. Research question
3. Drift split (exact value vs paraphrase)
4. One architecture line
5. CONTENT ID mechanism
6. FIELD/CUBE image
7. one conclusion

Everything else is 1.5 m / 0.5 m detail.

## Final conclusion
**Reasoning can change. The cited observation does not have to.**

Qualification in small type:
`Same cited record != same conclusion and != objective truth.`