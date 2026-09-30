# Missing systems view — architecture, workflow, comparison, and facts

Snapshot: 2026-09-30

## Core diagnosis

The current v5 poster explains several mechanisms but still leaves four scientific questions unanswered at a glance:

1. Where does emem sit in an EO/agent stack?
2. What does an agent actually do, step by step?
3. What object crosses the boundary between agents?
4. How is that object different from the primary objects in STAC/COG, openEO/Earth Engine, and agent-memory/RAG systems?

These are higher-value uses of poster space than session/date/licence metadata or vague slogans.

## Remove or demote

- Poster session number/date/location: the board is already inside the event.
- Apache-2.0 from the top metadata line: keep source/licence at the bottom or emem.dev.
- 'portable world-state' when not immediately defined.
- 'cited world-state is not temporary' style language unless paired with the exact object: signed observation record / raster derivation / cube manifest.
- API names as section titles. Show observable behaviour first; API names can sit in small type.
- repeated claims that the receiver 'does not trust' the server. State exactly what is checked and what trust remains.

## Add 1 — architecture: WHERE EMEM SITS

One horizontal scientific architecture, no product logos:

EO SOURCES
Sentinel-2 · DEM · weather · documents · device traces
        |
        v
EMEM NODE
LOCATE -> MATERIALISE -> CANONICALISE -> HASH -> ATTEST -> LOG
                             |
                     fact / raster / cube
                             |
                RESOLVE <- VERIFY <- GUARD
        |
        v
AGENT INTERFACES
MCP · REST · A2A
        |
        v
REASONERS
Agent A · Agent B · later session · other model

Key architectural fact: emem is not the foundation model and not the EO source. It is the address/verification layer between physical-world observations and transient reasoners.

Large caption:
**SOURCES PRODUCE EVIDENCE. EMEM GIVES THE EVIDENCE AN ADDRESS. AGENTS REASON FROM THE ADDRESS.**

## Add 2 — workflow: WHAT AN AGENT ACTUALLY DOES

Use verbs and one real example:

ASK
'Has vegetation changed here?'
  -> LOCATE
place -> cell64
  -> READ
fact / raster / cube
  -> REASON
model analyses the resolved field
  -> CHECK
guard compares stated values with cited records
  -> HAND OFF
token / bundle / checkpoint crosses to next agent or session
  -> CONTINUE
next reasoner resolves and verifies before using it

This should be executable against the 19 shipped skills / MCP surface, not a conceptual workflow.

## Add 3 — comparison: PRIMARY OBJECT BOUNDARY

Keep it to four rows. Do not score competitors.

| system family | primary object | primary job |
|---|---|---|
| STAC / COG | EO asset / raster file | discover and read EO data |
| openEO / Earth Engine | process / computed geospatial object | execute EO analysis |
| agent memory / RAG | retrieved text / task context | restore useful context |
| **emem** | **signed, typed observation / field address** | **let another agent resolve and check the cited physical-world state** |

Optional fifth row only if space remains:
W3C PROV | provenance graph | describe lineage.

Caption:
**The novelty is not hashing, provenance, or memory alone. It is the object being handed between reasoners.**

## Add 4 — missing facts worth surfacing

These are strong because they explain actual usage rather than breadth:

### A. Two clocks
Every EO value has valid time (when the world was observed) and transaction time (when the memory learned it). This explains why an old citation can remain reproducible after the upstream changes.

Use the 918.0 m -> 915.07 m Bengaluru example as a small inset, not a full panel.

### B. Signed absence
'Looked and found no tile' is different from 'could not look'. This is a subtle, scientist-friendly consequence of treating absence as a typed observation state.

Keep as a small badge/inset, not a headline.

### C. Fields are first-class
Do not let raster/cube look like another visualisation feature. State that the address binds a derivation and artifact hash, so the same field can be re-resolved or rebuilt.

### D. Long-run continuity
The 599-turn result is more relevant than generic 'memory' language: bundle arm 100% citable vs BM25 0% citable in that run. Keep the caveat and do not imply universal superiority.

### E. Guard is pre-publication checking
Value-level checking of a model's prose against the signed value it cites is unusually concrete. Visualise the mismatch, not the endpoint.

## Lost opportunities

### 1. The 918.0 -> 915.07 production drift exhibit
This is an excellent demonstration of why immutable citations matter even when the upstream changes. It is real, unplanned, and both values still verify. It should appear as a small 'WHY HISTORY MATTERS' inset.

### 2. The context-reset image
The skills explicitly support long-horizon memory, but the poster still does not show a context window dying and a later session reconstructing the evidence. This is probably the most memorable agent-specific visual available.

### 3. One complete real token
Print one complete emem:fact token at readable size. A poster about addressable evidence should let a scientist literally copy the address.

### 4. One complete observation record
Show the fields behind that token at least once. Otherwise 'content-addressed observation' remains abstract.

### 5. 'Why not just RAG?'
Do not answer this with prose. The comparison table plus drift experiment answers it: retrieval can recover useful context, while the emem handoff preserves a directly checkable citation object.

### 6. Architecture boundary
Without the architecture figure, visitors can mistake emem for an EO model, database, STAC catalogue, or RAG memory product. This is a preventable failure.

## Poster hierarchy after the upgrade

3 m:
- research question
- DRIFT experiment
- architecture / object boundary
- ADDRESS mechanism
- FIELD story
- conclusion

1.5 m:
- workflow
- handoff/context reset
- comparison
- verify-before-publish
- two-clock inset

0.5 m:
- exact token
- exact observation fields
- scene ids
- p-value and n
- caveats
- one QR

## Suggested top scientific question

**Can two independent agents still refer to the same Earth observation after their contexts diverge?**

Suggested answer at the bottom:

**Yes — if they hand over the address of the cited observation record rather than a sentence about it.**

Important qualification:
Same cited record does not mean same reasoning, same conclusion, or objective truth.