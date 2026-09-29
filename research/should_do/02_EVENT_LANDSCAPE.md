# Event poster landscape — title-level scan

Snapshot: 2026-09-30  
Source: https://agentic-eo.berlin/programme/posters/

Important: this is a **title-level landscape**, not a claim about each poster's unpublished methods. Use it to identify crowded framing, then read papers/abstracts as they become available before making stronger comparisons.

## Session 1 — closest collisions

### Agent frameworks / orchestration
- From Isolated Models to Agentic Orchestration: A Ground Segment Multi-Agent Framework...
- EIS: An Open-Source Geo-Agent Framework...
- LATINSIGHT: A React-Based Multi-Agent System...
- Agentic Ground Segment: How Generative AI Redesigns Data Discovery...
- Hierarchical System with Agentic Refinement...
- EO Agents in Actions...

**Implication:** do not headline "multi-agent EO framework". It is crowded.

### RAG / assistant / discovery
- SENSOR2RAG...
- GEODES Assistant
- Engineering a Trustworthy NASA Earth Science Discovery Agent...

**Implication:** avoid "RAG for EO", "assistant", "natural-language access", "discover data with AI" as the invention.

### Datacubes / on-demand dissemination
- Thematic Datacubes On-Demand (THEDE)...

**Implication:** `emem:cube:` is not interesting because it is a datacube. It is interesting because the cube is a **signed, addressable derivation object that can cross agent boundaries**.

### Trust / guardrails / evaluation
- Beyond Task Success: Domain-Grounded Evaluation...
- Engineering a Trustworthy NASA Earth Science Discovery Agent...
- GeoGuard: An Agentic Guardrails and Validation Framework...

**Implication:** "trustworthy AI" and "guardrails" are crowded words. Show the exact verification mechanism instead.

### End-to-end EO decisions
- Ask, Detect, Explain...
- From Earth Observation Data to Decision...
- Advancing Disaster Resilience through Agentic AI...

**Implication:** avoid generic "data → insight → decision" diagrams.

## Session 2 — closest collisions

### Multi-agent / end-to-end autonomy
- Autonomous Geospatial Intelligence...
- EOMAS – A Multi Agent System-Backed Assistant...
- From Perception to Priorities: An Agentic Pipeline...
- Enabling Adaptive Agentic Earth Observation across the Space–Ground–Cloud Continuum...
- Manteo AI: Agentic Geospatial Intelligence...

**Implication:** "autonomous", "end-to-end", "agentic intelligence" will not differentiate emem.

### Foundation models / embeddings / semantic search
- Learned Satellite Embeddings as Covariates...
- Specialized Geospatial Foundation Models for Agentic EO...
- Beyond the State of the Art in Geospatial Foundation Models...
- Airbus Geo Explore: Leveraging Semantic Search APIs...
- Aperture: Semantic Change Understanding and Grounded GeoAI Reasoning via SAR-Optical-Language Alignment

**Implication:** do not present embeddings as emem's invention. The paper's stronger contribution is **what happens after an embedding/observation is produced: how it gets durable identity, provenance and cross-agent continuity.**

### Provenance / auditability
- Provenance-First Geospatial Composition...
- Agentic AI as an Auditable Co-Scientist...

**Implication:** "provenance-first" alone is not enough. emem should show **content-derived observation identity plus independently checkable receipts**, and explicitly distinguish those from provenance metadata.

### On-board orchestration
- Multi-Satellite Task Orchestration for Wildfire Monitoring with On-Board VLMs
- Enabling Adaptive Agentic EO across Space–Ground–Cloud

**Implication:** "encode in orbit" should be a supporting future/device story, not the poster's core novelty unless the poster shows a live device-trace result. Otherwise it risks competing with stronger onboard-agent work on their home ground.

## The whitespace visible from the programme

No published poster title is framed primarily around:

> **physical-world observations as content-addressed, externally verifiable shared state that persists across model/session/agent boundaries**

That does **not** prove emem is unique. It says this framing is visibly less crowded in the published programme and is therefore the best hypothesis to test in the final poster.

## Keynote alignment

Published keynote titles:
- Google DeepMind — *Why Mature Agents Require a Paradigm Shift in Tooling*
- NASA JPL — *FAME - Traditional and Agentic AI in Space*
- Northwestern / Amazon — *Failure Mode in Agentic Reasoning*
- Stanford — *Harnessing the Collective Intelligence of AI Agents for Discoveries*

Source: https://agentic-eo.berlin/programme/keynote-speakers/

A poster about durable, checkable world-state naturally creates conversations with all four without trying to imitate any of them.

## Questions to ask while walking the room

After the event begins, update this file with observed evidence:
1. How many posters treat the agent transcript/vector DB as the durable state?
2. How many hand off raw files vs references vs claims?
3. How many give observations a content-derived identity?
4. How many verification schemes can run independently/offline?
5. How many distinguish provenance integrity from truth?
6. How many make spatial fields directly citeable/re-resolvable?
7. How many discuss state continuity after context compaction/model replacement?

These observations will tell us whether the emem framing really stood out in practice.
