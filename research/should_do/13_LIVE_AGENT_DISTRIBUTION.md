# Live distribution is part of the scientific proof

Snapshot: 2026-09-30

## Finding

emem is not only a protocol implementation or a standalone EO service. The same responder/protocol is already reachable from multiple agent runtimes:

- ChatGPT app (`@emem`)
- Claude.ai custom connector
- Claude Code / Claude plugin
- Dify marketplace plugin and workflows
- generic MCP clients
- A2A
- Cursor, VS Code, Gemini CLI, Cline
- Python and TypeScript SDKs
- framework examples for LangChain, LlamaIndex, CrewAI, AutoGen, Mastra, Agno and Semantic Kernel

Primary live surface: https://emem.dev/
Source/docs: https://github.com/Vortx-AI/emem
Dify Referent Lock: https://marketplace.dify.ai/template/emem/ad67ca26-e875-494b-b98f-23902c9a2017

## Why this belongs on the poster

This is not a logo-cloud claim. It is evidence for the paper's central systems hypothesis:

> a cited physical-world observation can be represented by a portable address whose meaning does not depend on one model runtime.

The poster should show one token crossing multiple real runtimes, not one architecture box labelled 'agents'.

## Precise spatial/content distinction

Do not say emem replaces spatiotemporal indexing.

`cell64 × band × tslot` = lookup key: where / what variable / when.

`fact_cid = BLAKE3(emem-CBOR(record))` = content identity: exactly which signed record.

`emem:fact:<cell64>:<fact_cid>` = handoff reference: location binding + immutable record identity.

That separation is one of the clearest explanations of why emem is useful to agents.

## Why 'stream satellite intelligence' is defensible

The physical source file does not have to enter an LLM context. emem materialises the needed observation or field, gives the resulting record/artifact an address, and agents carry the address. A later agent resolves only what it needs.

Phrase carefully:

GOOD: **Keep the scene upstream. Move the address into reasoning.**

GOOD: **Satellite data stays a data object; the model receives a citeable observation/field reference.**

AVOID: 'emem replaces spatiotemporal encoding'. It still uses spatial and temporal keys.

AVOID: 'one fact token saves context'. Internal measurements show an individual fact token is ~51 LLM tokens and can be more expensive than a scalar value.

## Where tokenisation really helps

- One `emem:fact:` token preserves exact citation identity across model/context boundaries.
- One `emem:bundle:` handle is 38 characters (~23 LLM tokens) for up to 256 facts; this is the compact multi-fact handoff mechanism.
- `emem:raster:` and `emem:cube:` let an agent refer to spatial fields and fields-through-time without putting a whole source scene into the context window.
- `emem:tree:` can name/check a chunk of a large file by row proof; useful supporting technology, not central to this paper poster.

## Poster visual

Use one horizontal strip:

`emem:fact:<...>`

then branches to:

`ChatGPT @emem | Claude | Dify | MCP client | A2A | SDK/framework agent`

Under every runtime, the same three verbs:

`RESOLVE -> RE-HASH -> REASON`

Caption:

**ONE CITED OBSERVATION. MULTIPLE AGENT RUNTIMES.**

Small qualifier:

`Availability/integration differs by host; all routes above are documented/live surfaces as of 30 Sep 2026.`

## Foundation-model title alignment

The accepted title explicitly says 'over Foundation-Model Embeddings'. Keep one concrete strip:

`Sentinel-2 -> Tessera encoder -> 128-D vector -> model_output fact -> fact_cid -> any agent runtime`

This demonstrates the architectural point: the embedding is not the durable identity; the signed addressable record around it is.

Do not claim AlphaEarth is integrated. The repo documents Tessera as the live encoder and retired older encoders whose old facts remain verifiable.

## Testable conference interaction

One QR to emem.dev.

Prompt beside it:

**Try the same place in the AI you already use. Ask it to return the emem token. Pass that token to another agent and resolve it.**

This is stronger than a demo video because the attendee can test the cross-runtime hypothesis directly.