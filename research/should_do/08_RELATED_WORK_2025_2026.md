# Related work from 2025–26 to position against

Snapshot: 2026-09-29. This extends `03_INDUSTRY_SYSTEMS_COMPARISON.md` (STAC, COG, Earth Engine,
PROV, IPFS, Nix, Mem0).

The rule stays the same: describe **the object each system is built around**. Never make
blanket negatives about other systems. A short line should appear on the poster only where
it sharpens emem's object boundary.

| work | what it does | what emem adds, stated positively |
|---|---|---|
| **AlphaEarth Foundations / Satellite Embedding dataset** (DeepMind; arXiv 2507.22291; also COG + STAC-GeoParquet on Source Cooperative) | global 64-D annual embeddings at 10 m | per-observation content identity + signed receipt + agent tokens *around* an embedding value. (Our AlphaEarth slot is reserved and unused, so do not claim integration.) |
| **TESSERA** (arXiv 2506.20380; v2 2607.03949) | open 128-D annual per-pixel S1/S2 embeddings | **the live encoder in emem.** Tessera values are signed as `model_output` facts |
| **"Earth Embeddings as Products"** (Fang et al., arXiv 2601.13134) | taxonomy + unified access via TorchGeo | the closest "standardised access" peer. Cite it. emem addresses *individual signed values*, not products |
| CNG blog: *"The Technical Debt of Earth Embedding Products"* (2026-02) | versioning and interoperability pain | our motivation: an old citation must not silently change meaning |
| **"Characterizing AlphaEarth Embedding Geometry for Agentic Environmental Reasoning"** (arXiv 2604.18715) | retrieval tools over AlphaEarth beat parametric-only agents | the closest agentic baseline over embeddings. We address what the agent *cites and hands on* |
| **STAC + IPFS** (EASIER Data; IPFS geospatial Zarr docs) | CIDs for whole files and scenes | CIDs for *typed per-cell observations* + responder signatures + bi-temporal reads + agent verbs |
| **openEO provenance** (Omidi et al., arXiv 2506.08597, yProv4WFs) | lineage of workflow processes | lineage says *how*. The CID lets a receiver check *which bytes*. Complementary |
| **C2PA Content Credentials** | signed manifests on media files | signs *files*. emem signs *queryable facts* and *answers*. Credentials also get stripped in pipelines (arXiv 2604.24890), while emem receipts sign an explicit ABSENT marker so stripping is detectable |
| **Geospatial MCP servers** (Earth Engine MCP from FDL; eo-mcp; EVE MCP registry; a survey of 77+ servers by Sparkgeo) | tool wrappers | emem is also an MCP server, but its results are *addressable and signed* |
| **A2A (Agent2Agent)**, Linux Foundation; signed Agent Cards reported for v1.0 (a secondary source) | signs *agent identity/capabilities* | emem signs *the evidence exchanged between agents* |
| **ERC-8004 "Trustless Agents"** (co-authored by keynote speaker D. Crapis) | on-chain agent identity, reputation and validation | emem receipts could be the *payload being validated*; they verify offline with no chain |
| **Agent memory**: MemGPT/Letta (2310.08560), Mem0 (2504.19413), A-MEM (2502.12110), CoALA (2309.02427), Anthropic memory tool | per-agent / per-user text memory, rewritable | emem's memory verbs follow the Anthropic memory-tool / CoALA shape, over **signed, content-addressed, geospatially keyed** notes and facts. **We have not benchmarked against these products; say so.** |

## The positioning sentence that survives scrutiny

> EO work produces **embeddings** (AlphaEarth, TESSERA), serves **files** (STAC, COG,
> Source Cooperative, IPFS), or wraps **tools** (MCP servers, EVE). Agent-trust work signs
> **identities** (A2A, ERC-8004) or **media** (C2PA). emem signs and content-addresses
> **individual physical observations and the answers built from them**, keyed by place, band
> and time, so any agent can re-check them after they have left the system that produced them.

This sentence is **inferred from public abstracts, not from exhaustive reading**. On the
poster, write it as "to our knowledge". Never write "first".
