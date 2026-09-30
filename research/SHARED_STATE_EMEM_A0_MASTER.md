# MASTER SHARED STATE — EMEM A0 POSTER

**Purpose**
This file is the single source of truth for the coding/design agent. The goal is not to make the current poster prettier. The goal is to transform it from a technically impressive protocol board into a **research poster that makes one scientific contribution obvious, experimentally credible, visually memorable, and demonstrably usable across the modern agent ecosystem**.

## 1. What a research poster must do

A poster is not a shrunken paper. It must communicate the research question, method, evidence and main finding to someone walking through a crowded session, at several metres distance, then reward closer inspection. Current poster guidance explicitly emphasizes one research argument, visible takeaway finding, dominant figures, concise text and predictable hierarchy. [CASRAI](https://casrai.org/guides/scientific-poster-design)

This workshop is especially competitive: the programme has **43 posters across two sessions**, and EMEM sits among work on EO-agent evaluation, RAG, agentic architectures, validation/guardrails, provenance, foundation models, orchestration and operational EO systems. Therefore EMEM must NOT compete by saying “agents + EO + provenance” generically. It must own a narrower, testable contribution. [Workshop poster programme](https://agentic-eo.berlin/programme/posters/)

## 2. Current EMEM poster — honest diagnosis

Current v12/v12.1 is:
- technically deep;
- unusually honest about limitations;
- rich in real EO examples;
- strong on content-addressing, signed records, temporal memory and mutation testing;
- visually more sophisticated than earlier versions;
- still too close to a **protocol audit / engineering architecture poster**;
- too many concepts are presented as co-equal: observation memory, embeddings, execution traces, EO evidence, EUDR, MCP, provenance;
- the central agent-to-agent scientific experiment is not yet dominant enough;
- the exact invention boundary is still easy to misunderstand;
- fact CID vs raw source artifact identity is too easy to conflate;
- threat/trust model is underdeveloped;
- baseline definitions are underdeveloped;
- verification depth is present but not presented as a clean ladder;
- source accuracy/entity correctness/decision correctness are correctly acknowledged as out of scope but need a stronger visual boundary;
- cost/overhead is not sufficiently visible;
- independent replication/evidence hierarchy is not sufficiently visible;
- ecosystem integrations are substantially underrepresented;
- ChatGPT, Claude, Dify, A2A, MCP, official MCP Registry, GitHub MCP Registry, GitHub, Glama and developer/framework surfaces must be part of the printed story, not merely QR destinations;
- SAT-042 and embeddings risk looking like equally mature contributions to the EO observation work when they are extensions.

## 3. Target identity

The final A0 should make one sentence unforgettable:

> **Agents hand each other evidence references, not paraphrases.**

Alternative acceptable hero:
> **Make physical-world evidence addressable.**

Do NOT use as the primary scientific claim:
> “When agents disagree, the satellite decides.”

It implies that the satellite establishes truth. It does not.

## 4. Core invention — exact boundary

The central contribution is:

> A physical-world observation can be represented by a stable, signed, content-addressed observation record that an agent can hand to another agent; the receiving agent can independently resolve the reference, verify the record, and—where provenance permits—re-read or recompute the cited observation without trusting the sender's prose.

Not inventions by themselves:
- BLAKE3
- Ed25519
- CBOR
- content addressing
- Merkle structures
- RAG
- STAC
- openEO
- PROV
- C2PA
- MCP
- A2A
- EO orchestration

These are enabling/complementary technologies.

## 5. Critical identity distinction

Never write that the fact CID is simply “the hash of the satellite pixel/bytes.”

Show:

SOURCE ARTIFACT
→ read/derive
→ CANONICAL OBSERVATION RECORD
→ BLAKE3(content address)
→ SIGNED FACT

The CID identifies the canonical EMEM observation record. The record identifies/names the upstream source artifact required for a source re-read.

## 6. Central scientific story

The A0 should read visually as:

**Agent A**
reads EO observation
↓
**Handoff**
prose / JSON / RAG / opaque ID / EMEM reference
↓
**Adversarial corruption**
value / cell / date / band / source / unit / derivation / stale state / etc.
↓
**Agent B**
resolves + verifies + re-reads
↓
**Outcome**
accept / refuse / detect mismatch
↓
**Boundary**
signature/integrity is not measurement truth

The mutation experiment should be the principal quantitative result, not a side panel.

## 7. Research questions

Make these visible:
- RQ1: Can a receiver detect corruption of a cited EO observation without trusting the sender?
- RQ2: Which classes of referential corruption are detectable?
- RQ3: Does address-based handoff preserve evidence better than paraphrased/structured/retrieved context?
- RQ4: What remains unverifiable even when the evidence reference is intact?

## 8. Hypotheses

- H1: EMEM reference handoff rejects mutations that preserve natural-language agreement but change the cited observation.
- H2: Receiver-side source re-read catches source/pixel errors that record integrity alone cannot catch.
- H3: Historical references preserve the state an agent actually cited after newer observations appear.

## 9. Main experiment

Compare:
1. natural-language paraphrase
2. structured JSON
3. ordinary RAG/context
4. opaque identifier
5. EMEM signed observation reference

Mutations should be explicitly enumerated and grouped:
- value
- spatial cell
- time
- band/product
- unit
- source artifact
- derivation
- stale/current state
- signature/CID
- semantic/entity identity

Report:
- denominator;
- mutation classes;
- false acceptance;
- correct refusal/detection;
- downstream decision accuracy where measured;
- verification latency;
- token/storage/network overhead;
- models/runtimes;
- independent vs system-generated components.

## 10. M15 finding must be prominent

Use the phrase:

> **The right record, the wrong pixel.**

Then explain:
> A valid signature can faithfully preserve a wrong measurement if the reader itself selected the wrong source pixel.

The 162/200 production-reader result is important because it demonstrates:
**record integrity ≠ measurement correctness.**

This is one of the strongest scientific findings and should not be buried.

## 11. Verification ladder

Show a compact ladder:

L0 — byte integrity
L1 — observation identity (cell/band/time/value)
L2 — derivation recomputation
L3 — upstream artifact provenance/source re-read
L4 — semantic/entity correctness
L5 — physical truth / downstream decision correctness

Clearly mark each as:
CHECKABLE / RECOMPUTABLE / INHERITED / PARTIAL / OUT OF SCOPE.

Never use “verified” without specifying the layer.

## 12. Trust/threat model

Show:
Attacker can mutate values, cells, dates, sources, records, references, replay stale state and traces.
Attacker cannot forge a valid signature without the signing key or produce the same content address for different canonical bytes.

Explicitly outside scope:
- compromised signer;
- incorrect sensor;
- incorrect upstream product;
- semantic/entity misidentification;
- downstream decision correctness.

Separate:
**cryptographic trust** — exact record signed;
**source trust** — signer/source authority;
**measurement trust** — sensor/product correctness.

## 13. Temporal memory

Make the Bengaluru example a visual timeline:
May: 918.0 m
→ signed observation
→ August newer source: 915.07 m
→ query: “what did the agent know as of 15 Jun?”
→ 918.0 m

Scientific point:
> Memory preserves the exact world-state an agent previously cited; newer observations do not silently rewrite history.

Do not present this merely as generic database versioning.

## 14. Prior-art boundary

Use a compact comparison:

STAC → discovers/describes EO assets
openEO → executes EO computation/workflows
PROV → expresses derivation/provenance
C2PA → signs digital asset provenance
RAG → retrieves context
GeoGuard → validates claims against external evidence
EMEM → gives agents a content-addressed, signed reference to the exact observation they cite, enabling receiver-side resolution/verification

Do not frame these as replacements. EMEM can use them.

Critical answer:
> **A STAC item identifies an asset; EMEM identifies the observation an agent cited and gives the next agent something independently verifiable to resolve.**

## 15. Actual EMEM object

Show one real fact, not only schemas:

cell
band/product
valid time
value
source
CID
signature

The viewer should understand what is handed between agents.

## 16. Ecosystem is mandatory content

The A0 MUST visibly show:

### Agent hosts / applications
- ChatGPT / @emem where verified
- Claude / Claude Code where verified
- Dify Marketplace

### Interoperability
- MCP
- A2A

### Discovery / registries
- Official MCP Registry
- GitHub MCP Registry
- GitHub
- Glama

### Developer surfaces
- VS Code
- Cursor
- Cline
- Gemini CLI
- Python SDK
- TypeScript SDK
- REST/OpenAPI
- Docker/self-hosting

### Framework adapters/examples, only if verified
- LangChain
- LlamaIndex
- CrewAI
- AutoGen
- Mastra
- Agno
- Semantic Kernel

Do NOT create a logo wall. Explain the architecture:

EMEM signed evidence
→ MCP / A2A
→ agent host/client
→ next agent/application

Caption:
> **One evidence protocol, multiple agent runtimes.**

The same observation should ideally be demonstrated resolving through two different agent environments.

## 17. Integration evidence status

Every ecosystem entry must be backed by an integration manifest with:
- platform;
- exact mechanism;
- URL;
- status;
- last verification date;
- actual user capability;
- source evidence.

Allowed status labels:
LIVE / PROTOCOL / REGISTRY / EXAMPLE / EXPERIMENTAL / ROADMAP.

Never imply that a directory listing equals a native integration.

## 18. Cost and performance

The poster should visibly answer:
> What does this buy, and what does it cost?

Where measured, show:
- verification latency;
- source reread cost;
- storage overhead;
- network cost;
- token overhead;
- LLM-token overhead.

Do not hide the known token overhead.

## 19. Embeddings

Embeddings are NOT a co-equal main contribution unless a dedicated experiment proves their scientific role.

If retained:
> **Derived representations are addressable too.**

Bind each representation to encoder/checkpoint/generation metadata and explicitly show that changing the encoder creates a new fact.

Otherwise move detailed embedding material behind QR.

## 20. SAT-042 / execution traces

Treat as an extension:
> **Extending verification to execution**

Explicitly:
> Reference implementation / scripted harness; no spacecraft enrolled.

Do not make it visually compete with the demonstrated EO observation work.

## 21. EO examples

Keep:
- Keylong NDVI
- Bengaluru temporal elevation
- Rondônia / EUDR screen

But every image must answer a scientific question and show:
- cell/location;
- date;
- product/band;
- observation;
- what the image demonstrates;
- scope/limitation.

EUDR screen must visibly say:
> point samples; not parcel polygons; not a regulatory determination.

## 22. Visual hierarchy

Design for:
### 3 m
Problem + invention + principal result

### 1 m
Agent handoff + mutation experiment + guarantee boundary + ecosystem

### 30 cm
Exact record, methods, statistics, citations, QR and reproducibility

No low-level implementation detail should compete with the central invention.

## 23. Prose rules

Prefer active scientific verbs:
**cite, hand off, resolve, re-hash, re-read, recompute, detect, refuse, preserve, recover, inherit, distinguish.**

Examples:
> Agents hand each other evidence references, not paraphrases.

> The receiver resolves the reference, re-hashes the record, and re-reads the source.

> A one-pixel mutation is refused.

> A signature fixes the bytes; it does not make the measurement true.

> The memory preserves what was known at that time.

Use noun-heavy protocol language only where precision requires it.

## 24. Panel rhythm

Each major panel should answer:
1. **Question/problem**
2. **Mechanism**
3. **Measured result + limitation**

Example:
> What survives an agent handoff?
> EMEM hands over an address to the observation, not its paraphrase.
> The verifier rejected X/X in-scope mutations; source accuracy remains separate.

## 25. QR/media

QRs must be action-oriented:
- TRY A TOKEN
- RE-RUN THE TEST
- INSPECT THE RECORD
- VIEW THE DEMO
- READ THE METHODS
- DISCOVER INTEGRATIONS

At least one deterministic <=20-second demo should show:
observation → EMEM reference → mutation → receiver verification → REFUSE.

No cinematic product video as a substitute for scientific reproducibility.

## 26. What the final poster must NOT become

Do not turn it into:
- a generic AI-agent poster;
- a logo wall;
- an EO product brochure;
- a cryptography tutorial;
- an MCP advertisement;
- an EUDR compliance claim;
- a spacecraft-attestation claim;
- an embedding paper;
- a giant API/schema reference;
- a collection of disconnected demos.

## 27. Final target A0 structure

**TOP**
Title + one-sentence contribution + authors/affiliations

**LEFT / PROBLEM**
Agent agreement vs evidence
Referential drift definition
RQ/Hypotheses

**CENTER / INVENTION**
Agent A → evidence → EMEM record → CID/signature → Agent B
Actual fact object
Verification ladder

**CENTER / MAIN RESULT**
Adversarial handoff experiment
Mutation matrix
M15 wrong-pixel finding

**RIGHT / SCIENTIFIC EVIDENCE**
Temporal memory
Keylong / Rondônia examples
Cost/performance
Threat model
Guarantee boundary

**BOTTOM / ECOSYSTEM**
ChatGPT | Claude | Dify
MCP | A2A
MCP Registry | GitHub MCP | GitHub | Glama
VS Code | Cursor | Cline | Gemini CLI
SDK/API/Docker
verified framework adapters

**BOTTOM-RIGHT**
Prior art
Limitations
QR/demo/reproducibility

## 28. Definition of success

A visitor should be able to answer these questions in under 30 seconds:

1. **What problem?**
   Agent handoffs can preserve words while losing the physical-world referent.

2. **What is new?**
   Agents hand off a content-addressed, signed observation reference that the receiver can independently resolve/check.

3. **What evidence?**
   Controlled adversarial mutations + real EO cases + wrong-pixel production finding + temporal/as-of recall.

4. **What does it NOT prove?**
   A signature does not establish sensor accuracy, entity identity or downstream decision correctness.

5. **Why not STAC/RAG/C2PA/GeoGuard?**
   They address adjacent layers; EMEM addresses the identity and receiver-verification of the cited observation during agent handoff.

6. **Can I use it?**
   Yes: show the verified ChatGPT/Claude/Dify/MCP/A2A/registry/GitHub/developer ecosystem surfaces.

7. **Can I reproduce it?**
   Yes: direct QR to token, record, experiment, source and methods.

If a viewer cannot answer those seven questions from the printed A0, the poster is not finished.

## 29. Priority order for implementation

P0:
1. Freeze invention boundary.
2. Make adversarial agent handoff the main experiment.
3. Correct CID/source wording.
4. Build guarantee/verification ladder.
5. Add ecosystem panel.
6. Verify every ecosystem integration.
7. Reduce implementation density.

P1:
8. Add threat/trust model.
9. Add prior-art matrix.
10. Add actual fact object.
11. Promote M15 wrong-pixel result.
12. Make temporal memory visual.
13. Add cost/overhead.
14. Add cross-runtime demonstration.
15. Add 3m/1m/30cm hierarchy.

P2:
16. Refine captions.
17. Add media/demo pack.
18. Polish platform marks.
19. Move detailed embeddings/execution material behind QR unless independently demonstrated.

## 30. Final north-star

The poster should feel like:

**A scientific result first.**
**A protocol second.**
**A working ecosystem third.**
**A product demonstration only where it strengthens the evidence.**

The desired emotional/intellectual sequence is:

> “I understand the failure.”
>
> “I see the exact invention.”
>
> “I can see the experiment.”
>
> “I understand what the experiment proves—and doesn't.”
>
> “I see that it works across real agent ecosystems.”
>
> “I want to try/reproduce it.”

That is the final EMEM poster.