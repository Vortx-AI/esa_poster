# Broaden the source of truth before upgrading the EMEM poster

## Purpose

The coding agent must not treat the emem repository alone as the complete source of truth for the scientific poster.

The emem repository is authoritative for implementation behavior and current protocol semantics. It is not sufficient for workshop positioning, related work, competitor overlap, independent evaluation methodology, external scientific evidence, or deciding whether a proposed novelty claim is actually novel.

Before changing the poster, the agent should build a broader evidence graph.

## Source hierarchy

### Tier 0 — live implementation truth
Use:
- Vortx-AI/emem source at the exact cited commit;
- emem protocol/model docs;
- production endpoint behavior;
- reproducibility scripts and captured outputs.

If code and documentation disagree, report the disagreement and follow measured/code behavior for implementation claims.

### Tier 1 — independent external evidence
Use:
- peer-reviewed papers;
- arXiv papers with identified experimental scope;
- official ESA/NASA/JRC documentation;
- workshop programmes and poster abstracts;
- independent benchmark repositories;
- upstream EO data-provider documentation;
- external standards/specifications.

These determine whether a claim is established prior art, a meaningful gap, an untested hypothesis, or a genuine EMEM contribution.

### Tier 2 — ecosystem implementations
Inspect serious external implementations, including:
- NASA-IMPACT GeoGuard;
- Earth-Agent;
- ESA Agentic AI evaluation/benchmarking work;
- EO RAG systems;
- provenance-first geospatial systems;
- openEO / STAC / cloud-native EO data systems;
- MCP/A2A agent infrastructure;
- relevant geospatial foundation-model projects.

Classify each by layer: producer, retriever, validator, provenance system, memory/reference layer, benchmark, foundation model, or orchestration layer.

### Tier 3 — community / ecosystem evidence
Use GitHub, conference material, technical reports and practitioner discussions for discovery. Treat these as discovery evidence, not automatically as scientific proof.

## External evidence already identified

### Berlin workshop

The official programme lists 43 posters across two sessions. EMEM is poster 4 in Session 1. Relevant neighboring topics include:
- Beyond Task Success: Domain-Grounded Evaluation of Earth Observation Agents;
- SENSOR2RAG;
- GeoGuard;
- Agentic Ground Segment;
- Earth Observation Multi-Agent System;
- specialized geospatial foundation models;
- Provenance-First Geospatial Composition;
- agentic irrigation mapping;
- SeismicAgent;
- semantic-search agentic workflows;
- multi-satellite task orchestration.

Source: https://agentic-eo.berlin/programme/posters/

This means the poster must not claim generic novelty in EO agents, RAG, validation, provenance, or agent orchestration.

### GeoGuard

NASA-IMPACT/University of Alabama's GeoGuard is a directly relevant external system. It wraps upstream geospatial AI, decomposes claims, selects verification tools, audits against external authoritative data, and produces verdicts/evidence/confidence.

Its public benchmark reports 50 verified NOAA events and 15 fabricated counterparts; 0 fabricated events were endorsed and 14/15 were explicitly contradicted.

Source: https://github.com/NASA-IMPACT/geoguard

Implication: Do not position EMEM as the generic geospatial validation layer.

Architectural distinction:
- GeoGuard-like system: is this claim supported by external evidence?
- EMEM: which exact evidence object did the previous agent cite, and can another agent independently resolve and verify that reference?

These can be complementary.

### EO-agent reliability literature

Kao et al., Towards LLM Agents for Earth Observation, reports a benchmark of 140 questions across 13 topics and 17 satellite sensors; the reported agent achieved 33% accuracy, with code failing to run in more than 58% of cases.

Source: https://arxiv.org/abs/2504.12110

Implication: EO-agent reliability is already an established research problem. EMEM should demonstrate a specific evidence-integrity/referential failure mode, not merely say EO agents are unreliable.

### Earth-Agent

Earth-Agent is an ICLR 2026 EO-agent system/evaluation framework with public implementation.

Source: https://github.com/opendatalab/Earth-Agent

Implication: compare EMEM's layer to EO-agent producers/evaluation systems rather than claiming the entire EO-agent problem as its novelty.

### ESA Phi-lab evaluation work

ESA's Agentic AI for Earth Observation evaluation project explicitly evaluates general-purpose and EO-specialized LLMs, uses MCP/FastMCP, ADK, vLLM, EO APIs, vector retrieval and graph retrieval.

Source: https://cin.philab.esa.int/databases/projects/agentic-ai-for-earth-observation-evaluation-and-benchmarking-of-llms

Implication: Benchmarking and MCP-based EO agents are already active at ESA. The EMEM benchmark should be legible as an independent reliability experiment, not another product demo.

## Required research workflow for the coding agent

Before materially changing the poster:

1. Search the official workshop programme and abstracts.
2. Search 2025–2026 literature for agentic EO, geospatial agents, EO RAG, provenance, verifiable computation, content-addressed data, scientific data citation, model/context memory, multi-agent handoff, evidence-grounded agents, hallucination/factuality, and adversarial evidence verification.
3. Inspect the most relevant external implementations.
4. Create a related-work matrix.
5. For every proposed novelty statement, classify it as unique, similar prior art, complementary, untested, or contradicted.
6. Only then modify the poster.

## Required related-work matrix

Maintain:

System/work | Layer | Input | Evidence identity | Provenance | Agent handoff | Independent verification | Adversarial benchmark | EMEM relation
--- | --- | --- | --- | --- | --- | --- | --- | ---
GeoGuard | validator | claims/output | external evidence | yes | indirect | yes | yes | complementary
Earth-Agent | agent/benchmark | EO tasks | task/data dependent | task dependent | yes | task dependent | evaluation | upstream producer
ESA evaluation | benchmark/orchestration | EO questions/tools | retrieval-dependent | tool traces | yes | evaluation-dependent | benchmark | external evaluation
EMEM | evidence/reference layer | physical observations | content-derived reference | signed/provenance-bound | core | core | needs broader benchmark | proposed primitive

Do not populate missing cells by inference. Mark them unknown until independently verified.

## Core scientific distinction

The poster must separate:

1. source integrity — is the upstream artifact what it claims to be?
2. derivation integrity — was the value correctly extracted/computed?
3. observation identity — is this exactly the record that was signed?
4. spatiotemporal identity — does it refer to the intended place/time?
5. entity identity — is it the intended physical entity?
6. semantic correctness — is the interpretation scientifically valid?
7. agent decision correctness — did the downstream agent act correctly?

EMEM currently has strong evidence for observation identity and important mechanisms around spatiotemporal binding, provenance and receipts. It does not automatically establish source correctness, derivation correctness, entity identity, semantic correctness or decision correctness.

Do not collapse these into 'trust'.

## Poster redesign implication

Move from:

protocol internals → long trace → implementation details → agent demo

toward:

failure mode → adversarial mutation → intervention → measured effect → mechanism → limits

The cryptographic mechanism should explain the measured effect, not be the entire scientific result.

## Highest-value experiment

Build a cross-agent evidence-handoff benchmark with:

### Conditions
A. prose
B. structured value
C. ordinary RAG
D. EMEM token

### Mutations
- plus/minus 1 ULP;
- rounding;
- wrong/adjacent cell;
- wrong/stale date;
- swapped band;
- wrong unit;
- changed source;
- altered derivation parameter;
- changed model/checkpoint;
- altered embedding;
- same value but different entity;
- modified token;
- old valid observation presented as current.

### Models
4–6 materially different models where available.

### Metrics
- false acceptance;
- false rejection;
- mutation detection;
- verification completion;
- decision accuracy;
- latency;
- token overhead.

Every headline result must state n, task definition, baseline and uncertainty.

## Protocol upgrade implied by broader research

For derived physical-world claims, bind as much as available:

upstream artifact identity
+ exact byte/pixel/range reference
+ coordinate transform
+ derivation code/version
+ parameters
+ model/checkpoint
+ output
+ uncertainty
+ attester

If the upstream artifact has no cryptographic identity, explicitly label that provenance edge as upstream identity unverified.

## Anti-hallucination rule for the coding agent

Never infer scientific novelty from absence in the emem repository.

Never turn an internal implementation feature into a claim that the field lacks the capability.

Never cite an EMEM experiment as independent evidence.

Never call a mechanism 'truth verification' when it only establishes identity, integrity or provenance.

Never use a benchmark result without reproducing its denominator, population, baseline and task definition.

When external evidence conflicts with an EMEM claim, surface the conflict instead of silently rewriting the claim.

## Deliverables expected from the next research pass

1. research/should_do/ — updated external field map.
2. research/should_do/ — related-work matrix with URLs and dates.
3. research/do_not_use/ — claims ruled out by external evidence.
4. research/repro/ — benchmark scripts and raw result metadata.
5. poster/ — revised wall narrative only after the evidence layer is updated.

The source-of-truth model should therefore be:

EMEM source truth
+
independent external scientific truth
+
event/field truth
+
reproducible experiment truth

—not the emem repository alone.
