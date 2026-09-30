# emem × Agentic EO — poster working repository

Working material for the Agentic AI for Earth Observation Workshop 2026 poster.

## Accepted paper

**emem: A research on Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings**

Authors: Jaya Kumari, Avijeet Singh  
Preprint: DOI 10.5281/zenodo.20706893

## Poster thesis

> **One place, one address. One observation, one signed record. The record's name, not a paraphrase, is what crosses between agents.**

(v11 headline. Earlier drafts used "The satellite observation can outlive the agent.")

emem is not presented here as another EO tool or another retrieval layer. The poster should show the protocol invention:

**Earth observations become immutable, externally addressable reasoning state. Agents are transient compute over that state.**

Content addressing is the mechanism, not the headline.

## Core scientific story

1. A physical-world observation is represented as a typed object:
   `O = (cell, band, tslot, value, uncertainty, provenance, signer, signed_at)`; the ed25519 signature sits on the enclosing attestation
2. Canonical bytes give the signed observation a deterministic identity:
   `fact_cid = base32(BLAKE3(emem-CBOR(O)))` (deterministic, declaration-ordered, float-canonical CBOR; not RFC 8949 key-sorted)
3. An agent carries a compact token rather than a paraphrased value:
   `emem:fact:<cell64>:<fact_cid>`
4. A second agent resolves the token, gets the byte-identical signed observation, re-hashes it itself, and verifies the receipt offline. A token cited under the wrong cell fails with HTTP 409.
5. Context can be compacted, a session can end, or the model can change; the observation remains addressable.
6. Spatial fields and time-varying fields extend the same idea through `emem:raster:`, `emem:cube:` and `emem:rasterset:`.
7. The result is a content-addressed build graph over physical-world state that multiple agents can reuse instead of re-deriving.

## What the poster should make a scientist understand in 30 seconds

- **What is new:** durable world-state outside the model.
- **Why it works:** canonical encoding + content-derived identity + spatial binding + signed receipts.
- **What it enables:** long-horizon agents, cross-agent handoff, model swaps, referential stability, reusable EO fields, research-grade citations, pre-publication checking, and append-only audit history.
- **What it does not claim:** cryptography does not make an observation true. It makes co-reference, integrity, provenance and replay checkable.

## The poster

**Print-ready A0 poster, v11: [poster/](poster/README.md)** ([PDF](poster/emem-poster-A0.pdf), [preview](poster/emem-poster-preview.png)).

v11 presents emem as an invention: one address per place, one signed record per observation, and the record's
name, not a paraphrase, crossing between agents. Six contributions, four results (led by a 17-case mutation test of the verifier), eight answered objections and a table of what emem does and does not establish.
Every number is traced in [research/should_do/15_V11_CLAIMS_MAP.md](research/should_do/15_V11_CLAIMS_MAP.md);
the reasons for the redesign are in [research/should_do/16_V11_CRITIQUE_AND_DECISIONS.md](research/should_do/16_V11_CRITIQUE_AND_DECISIONS.md).
Independent audits of emem and of the v10 claims are in [research/audit_v11/](research/audit_v11/).
The v10 board is kept in [poster/archive/v10/](poster/archive/v10/).

**To edit or extend the board, start with [AGENTS.md](AGENTS.md), then the [session log](research/sessions/2026-09-30_v11/README.md) and [next steps](research/sessions/2026-09-30_v11/NEXT_STEPS.md).**

## Sample visuals (early exploration, superseded)

These SVGs predate the code check. They still show the old `CanonicalCBOR` formula and `s = signature`, so do not reuse their text.

- [Poster wireframe](assets/poster-wireframe.svg)
- [Why the invariant works](assets/invention-mechanism.svg)
- [Long-horizon / multi-agent continuity](assets/agent-continuity.svg)

See [POSTER_CONCEPT.md](POSTER_CONCEPT.md) for the full narrative and exact copy direction.

**Before using any claim, check [research/](research/README.md)** — especially the [verified claims ledger](research/should_do/04_VERIFIED_CLAIMS_LEDGER.md) and the [corrections to this concept](research/do_not_use/03_CORRECTIONS_TO_CURRENT_CONCEPT.md). The mechanism was independently reproduced against production in [research/repro](research/repro/README.md).

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
