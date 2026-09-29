# emem × Agentic EO — poster working repository

Working material for the Agentic AI for Earth Observation Workshop 2026 poster.

## Accepted paper

**emem: A research on Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings**

Authors: Jaya Kumari, Avijeet Singh  
Preprint: DOI 10.5281/zenodo.20706893

## Poster thesis

> **The satellite observation can outlive the agent.**

emem is not presented here as another EO tool or another retrieval layer. The poster should show the protocol invention:

**Earth observations become immutable, externally addressable reasoning state. Agents are transient compute over that state.**

Content addressing is the mechanism, not the headline.

## Core scientific story

1. A physical-world observation is represented as a typed object:
   `O = (a, b, t, v, u, p, s)`
2. Canonical bytes give the observation a deterministic identity:
   `CID(O) = Base32(BLAKE3(CanonicalCBOR(O)))`
3. An agent carries a compact token rather than a paraphrased value:
   `emem:fact:<cell64>:<fact_cid>`
4. A second agent resolves the token, gets the byte-identical signed observation, re-hashes it, and verifies the receipt independently.
5. Context can be compacted, a session can end, or the model can change; the observation remains addressable.
6. Spatial fields and time-varying fields extend the same idea through `emem:raster:`, `emem:cube:` and `emem:rasterset:`.
7. The result is a content-addressed build graph over physical-world state that multiple agents can reuse instead of re-deriving.

## What the poster should make a scientist understand in 30 seconds

- **What is new:** durable world-state outside the model.
- **Why it works:** canonical encoding + content-derived identity + spatial binding + signed receipts.
- **What it enables:** long-horizon agents, cross-agent handoff, model swaps, referential stability, reusable EO fields, research-grade citations, pre-publication checking, and append-only audit history.
- **What it does not claim:** cryptography does not make an observation true. It makes co-reference, integrity, provenance and replay checkable.

## Sample visuals

- [Poster wireframe](assets/poster-wireframe.svg)
- [Why the invariant works](assets/invention-mechanism.svg)
- [Long-horizon / multi-agent continuity](assets/agent-continuity.svg)

See [POSTER_CONCEPT.md](POSTER_CONCEPT.md) for the full narrative and exact copy direction.

## Source of truth

The poster claims should remain aligned with the live emem repository, especially:

- `docs/model.md`
- `docs/whitepaper.md`
- `plugins/emem/skills/emem-long-horizon-memory/SKILL.md`
- `plugins/emem/skills/emem-multi-agent-handoff/SKILL.md`
- `plugins/emem/skills/emem-referential-drift/SKILL.md`
- `plugins/emem/skills/emem-field-tokens/SKILL.md`
- `plugins/emem/skills/emem-verify-before-publish/SKILL.md`

Source: https://github.com/Vortx-AI/emem
