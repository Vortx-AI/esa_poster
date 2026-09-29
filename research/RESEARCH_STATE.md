# Research state

Snapshot: 2026-09-30

Purpose: shared research memory for the Agentic AI for Earth Observation poster. Update this file when a new comparison materially changes the poster thesis.

## Current conclusion

The strongest defensible positioning is **not** that emem invented content addressing, provenance, agent memory, EO data access, or multi-agent orchestration individually.

The distinctive systems thesis is their composition around a new unit of shared state:

> **A physical-world observation becomes an externally addressable, typed, signed object that can survive the agent, context window, model, vendor and session that first used it.**

This is what the poster should make experimentally and mechanically obvious.

## Why this matters at this event

The published poster programme contains 43 posters. Many titles cluster around:
- multi-agent frameworks and orchestration;
- RAG / assistants / semantic search;
- EO datacubes and data dissemination;
- end-to-end analysis agents;
- guardrails, validation and trust;
- provenance-first workflows;
- foundation models and embeddings;
- onboard / space-ground-cloud agent systems.

Source: https://agentic-eo.berlin/programme/posters/

Therefore, a generic "agents + EO + provenance" poster will disappear into the room.

## Neighbouring systems we must acknowledge mentally

| System / standard | What it already does | Why emem must not claim this alone |
|---|---|---|
| STAC | standard language to describe and discover spatiotemporal assets | discovery/cataloguing of EO assets is established |
| COG | efficient cloud-native partial access to GeoTIFF imagery | moving fewer bytes / range access is established |
| Google Earth Engine | deferred execution over a computation DAG at massive scale | lazy EO computation graphs are established |
| W3C PROV | interoperable model for entities, activities, derivation and provenance | provenance vocabularies and derivation models are established |
| IPFS | generic content-addressed data with CIDs | content-derived names are established |
| Nix | content-addressed store/build artefacts and reproducible derivations | content-addressed build systems are established |
| Mem0 / agent-memory systems | persistence across agent sessions and contexts | long-term agent memory is established as a category |

Sources:
- https://stacspec.org/en/
- https://cogeo.org/
- https://developers.google.com/earth-engine/guides/deferred_execution
- https://www.w3.org/TR/prov-overview/
- https://docs.ipfs.tech/concepts/content-addressing/
- https://releases.nixos.org/nix/nix-2.34.1/manual/store/store-object/content-address.html
- https://mem0.ai/

## emem's credible whitespace

emem can credibly show a different object boundary:

1. **The atom is a physical observation**, not a chat memory or a file.
2. **Its identity is content-derived** from canonical bytes.
3. **Its spatial/temporal semantics are explicit**, not merely metadata around a blob.
4. **Its receipt is independently verifiable**, including by a downstream agent.
5. **Its address is designed to cross model/session/agent boundaries.**
6. **Fields and fields-through-time are first-class addressable derivations**, not only scalar facts.
7. **The same mechanism underpins long-horizon state, multi-agent handoff, drift checking and publish-time verification.**

The poster should demonstrate these as one architecture, not as a feature list.

## Event-level opportunity

Several keynote titles sharpen the relevance:
- "Why Mature Agents Require a Paradigm Shift in Tooling" — Google DeepMind
- "FAME - Traditional and Agentic AI in Space" — NASA JPL
- "Failure Mode in Agentic Reasoning" — Northwestern / Amazon
- "Harnessing the Collective Intelligence of AI Agents for Discoveries" — Stanford

Source: https://agentic-eo.berlin/programme/keynote-speakers/

emem can sit underneath all four conversations: persistent world-state, agent handoff, failure containment, and collective reuse of verified evidence.

## Working test for every poster element

Keep it only if a scientist can answer at least one of these after seeing it:

1. **What object did emem introduce?**
2. **What invariant does it enforce?**
3. **What mechanism makes that invariant checkable?**
4. **What can a second agent do that it could not safely do with prose alone?**
5. **What does the protocol explicitly not prove?**

If an element answers none of these, remove it.
