# Real gap study — emem poster vs paper, code, workshop, and adjacent research

Snapshot: 2026-09-30

## Scope

This is not a design critique. It is a scientific/positioning gap analysis against:
- the official Agentic AI for EO programme;
- the current emem repo and skills;
- the accepted/preprint paper framing;
- nearby 2025–26 work in agent memory, EO embeddings, provenance, and geospatial infrastructure;
- the current v7 poster.

## 1. TITLE / SUBMISSION MISMATCH — FIX

The official workshop listing is:

**EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings**

The current poster uses the Zenodo/preprint variant:

**emem: A research on Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings**

Workshop source: https://agentic-eo.berlin/programme/posters/

Recommendation: use the official event-listed title on the board; put the Zenodo title only in the citation/DOI if needed.

## 2. NOVELTY GAP — 'ADDRESSABLE MEMORY' IS NO LONGER ENOUGH

ARC (Addressable Recall Compaction, arXiv:2607.25066) stores tool observations in an append-only ID-addressable log and replaces old context with compact citations that can be recalled later.

Therefore do NOT position emem as novel merely because:
- an ID survives compaction;
- old observations can be recalled by address;
- context can be replaced with pointers.

emem's stronger object boundary is:

**typed physical-world observations and fields whose identity, place/time binding, provenance, and serving receipt can be independently checked across agent runtimes.**

ARC is a direct conceptual competitor for the long-horizon-memory story and should be cited internally.

## 3. FOUNDATION-MODEL EMBEDDING GAP — TITLE PROMISE > POSTER EVIDENCE

The accepted title explicitly says 'over Foundation-Model Embeddings'. The poster currently shows Tessera only as a label.

Nearby work is strong:
- AlphaEarth agentic environmental reasoning uses a FAISS-indexed embedding database and specialized tools (arXiv:2604.18715).
- 'Earth Embeddings as Products' argues for standardized first-class embedding datasets (arXiv:2601.13134).

So 'we feed embeddings to agents' is not distinctive.

What emem needs to show precisely:

`Sentinel-2 -> Tessera encoder -> 128-D vector -> typed model_output fact -> content id -> receipt -> second agent`

Then the contribution:

**the embedding becomes one versioned, place/time-bound, signed observation record that remains citeable after leaving the encoder/runtime that produced it.**

Missing evidence to add before printing:
- one real Tessera fact token;
- its exact cell/time;
- recipe/version/manifests pinned around it;
- a re-resolution in another runtime;
- explicit label that it is `model_output`, not measurement.

## 4. LIVE DISTRIBUTION GAP — STRONG PROOF, BUT CURRENTLY UNDER-VALIDATED

Public evidence confirms:
- ChatGPT has a live emem plugin page;
- Dify has live Referent Lock templates;
- emem.dev documents MCP/A2A/SDK/client integrations.

Sources:
- https://chatgpt.com/plugins/plugin_asdk_app_6a6a0832a59081918b19aec0ddf9ec77/
- https://marketplace.dify.ai/template/emem/6c7b54a5-17f0-4eac-97a2-5d8cb51be381
- https://emem.dev/

Gap: the poster implies the same token is already proven end-to-end across ChatGPT, Claude, Dify, etc. Infrastructure availability is not the same as a controlled cross-runtime experiment.

Before claiming this as evidence, run and record one identical token through at least:
- ChatGPT @emem;
- Dify Referent Lock;
- Claude/MCP if publicly accessible;
- a plain MCP client.

Record:
- input token;
- resolved CID/value;
- whether byte identity/receipt verification was actually checked;
- runtime/model version/date;
- exact output differences.

This could become the strongest conference demo if measured, rather than just listed.

## 5. 'FILES STAY, TOKENS MOVE' GAP — TWO DIFFERENT MECHANISMS ARE BEING MIXED

Vortx's live site demonstrates file tokenisation/pointer notes: the file stays where it is, the model reads a small note / token / Merkle row proof.

The poster's core paper mechanism is different:
- `emem:fact:` for typed observation records;
- `emem:raster:` / `emem:cube:` for signed EO derivations.

Do not blur them into one claim.

Recommended distinction:

**Observation path (paper core):** source scene -> materialised measurement/field -> signed addressable EO record.

**File path (broader protocol):** large file stays at source -> content-addressed note/tree -> agent fetches/verifies only a needed range/chunk.

The second is visually spectacular but belongs in a small 'same primitive scales to files' inset unless the submitted paper explicitly develops it.

## 6. SPATIOTEMPORAL CLAIM GAP — DO NOT SAY EMEM REPLACES IT

emem still uses `(cell64, band, tslot)` as the canonical lookup coordinate.

Best explanation:
- spatiotemporal key answers **where / variable / when**;
- content id answers **exactly which record**;
- token binds both for handoff.

This separation is more novel/defensible than saying 'content addressing instead of spatiotemporal encoding'.

## 7. PROVENANCE GAP — PROVENANCE ITSELF IS OLD

W3C PROV already supports entity/activity/agent provenance, derivation, versioning and reproducibility.

Source: https://www.w3.org/TR/prov-overview/

Related 2026 agent literature now explicitly treats evidence tracing and execution provenance as an active field (arXiv:2606.04990).

So do not headline 'provenance'.

emem's stronger claim:

**the receiver can verify the identity of the evidence body it was handed, not only read a description of its lineage.**

## 8. EARTH-ENGINE / OPENEO GAP — BUILD GRAPHS ARE NOT NOVEL

Earth Engine already serializes computations into expression DAGs and executes lazily/on demand.

Source: https://developers.google.com/earth-engine/guides/deferred_execution

So 'content-addressed build graph over Earth' is an analogy, not the novelty claim.

Keep the phrase only if followed by:

**the resulting EO record can leave the compute environment and remain independently identifiable/checkable in another agent runtime.**

## 9. RAG / EMBEDDING-RETRIEVAL GAP — NEED A FAIRER COMPARISON

AlphaEarth agentic reasoning demonstrates strong results from embedding retrieval over FAISS.

Therefore the poster should not visually imply that retrieval itself is unreliable or obsolete.

Better comparison:
- RAG answers: 'which stored item seems relevant?'
- emem token answers: 'which exact evidence object did the previous agent cite?'

Retrieval and addressability solve different stages.

Use the BM25/dense results only as measured task results, not a universal systems verdict.

## 10. PAPER-vs-PRODUCT SCOPE GAP

The latest emem repo is broader than the paper:
- generic agent memory;
- content-addressed files/trees;
- EUDR;
- cameras/perception;
- DID/federation;
- device traces;
- multiple client/plugin surfaces.

These prove the protocol is real, but too many on the poster can dilute the submitted contribution.

Poster rule:

**paper-core technologies large; product-distribution evidence small.**

Large:
- fact content identity;
- spatial/time binding;
- field/cube derivations;
- embedding-as-typed-fact;
- handoff/drift experiment;
- value-level claim check.

Small proof strip:
- ChatGPT / Dify / MCP / A2A / SDK availability.

Off-wall:
- EUDR;
- device/orbit roadmap;
- DID/federation internals;
- cameras;
- memory file CRUD;
- product listings.

## 11. EVIDENCE-FREEZE GAP

The poster is pinned to emem commit `64cfae5`, while current main is later (5acf1f4... on 30 Sep).

This is scientifically acceptable only if explicit:

`Poster experiments frozen at 64cfae5 / 29 Sep 2026; integration availability rechecked 30 Sep 2026.`

Do not mix new code claims into old measured results without re-running the evidence scripts.

Before print choose one:

A. keep the evidence freeze and label it clearly; or
B. re-run every printed check against the final release commit and update the claims ledger.

Option B is stronger if stable before print.

## 12. BENCHMARK GAP — CORE CLAIM IS NOT YET INDEPENDENTLY REPLICATED

The repository itself states the agent benchmark is SAMPLE: small number of sites, two open models on one host, no independent replication.

That honesty should stay.

Biggest scientific opportunity before the event:

**Ask an external lab/person to run the one-token vs paraphrase handoff script unchanged.**

Even one independent reproduction is more valuable than another poster panel.

## 13. CROSS-RUNTIME EXPERIMENT — HIGHEST 'WOW' OPPORTUNITY

Pre-register a tiny live test before the conference:

Question:
`Does the same emem:fact token resolve to the same cited record across independent agent hosts?`

Protocol:
1. choose one real EO token;
2. paste it into ChatGPT @emem, Dify, Claude/MCP, and a bare MCP client;
3. ask each to resolve only, not summarize;
4. record returned CID/value/cell/band/time;
5. verify receipt/body independently;
6. then ask each model to interpret it and show that reasoning can differ while citation identity remains stable.

Expected poster figure:

`same token -> 4 runtimes -> same record / different prose`

This is a direct demonstration of the paper's multi-agent portability claim.

## 14. FOUNDATION-EMBEDDING EXPERIMENT — SECOND HIGHEST OPPORTUNITY

Use one live Tessera embedding fact:

`same 128-D embedding fact -> two models -> different analysis -> same cited vector record`

This directly answers the paper title and differentiates emem from systems that only standardize/retrieve embedding products.

## 15. MISSING SCIENTIFIC BASELINE

The current comparison strip names systems, but the poster needs one sentence clarifying complementarity:

`STAC/COG find/read assets; Earth Engine/openEO compute; RAG retrieves; emem preserves the identity of the cited physical-world record across reasoning boundaries.`

This avoids a straw-man comparison.

## 16. VISUAL GAP — CURRENT POSTER STILL HAS TOO MANY TERMINAL-LIKE BOXES

The scientific message should be image-first:
- one observation card;
- one drift fork;
- one context-reset handoff;
- one field/cube sequence;
- one cross-runtime token fan-out;
- one verify mismatch.

Raw API output belongs at 0.5 m or behind the QR.

## 17. MISSING 'WHAT FAILS' PANEL

Scientists will ask where it breaks.

One tiny boundary box should state:
- content identity does not prove sensor truth;
- entity co-reference is weaker than fact byte identity;
- field derivation tokens can change on re-mint even when pixels match;
- cross-runtime availability != independent replication;
- read federation is not shipped;
- hardware/on-orbit signing is not shipped.

This is stronger than generic 'limitations' prose because it names protocol boundaries.

## 18. TOP 5 UPGRADES, IN ORDER

1. **Use the official workshop title.**
2. **Run the same-token cross-runtime experiment and add the result, not just logos.**
3. **Add one real Tessera embedding fact experiment.**
4. **Make ARC the direct long-horizon prior-art comparator and narrow novelty accordingly.**
5. **Either re-freeze/re-run at final emem commit or clearly label the current evidence freeze.**

## Working novelty statement after research

Do NOT say:
`emem invented content addressing / long-term agent memory / provenance / EO retrieval / embedding access.`

Best defensible statement:

> **emem makes typed physical-world observations and fields externally addressable, place/time-bound and independently checkable, so the exact evidence cited by one reasoner can survive compaction, model/runtime changes and multi-agent handoff.**

That is the claim the poster should prove visually and experimentally.