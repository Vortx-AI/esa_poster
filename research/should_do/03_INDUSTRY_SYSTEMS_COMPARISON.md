# Industry / systems comparison — where emem actually differs

Snapshot: 2026-09-30

This is not a competitor scorecard. It is a guardrail against accidental novelty claims and a way to articulate emem's systems contribution precisely.

## STAC

**Established contribution:** a common JSON-based structure for describing, cataloguing and searching spatiotemporal assets.

Source: https://stacspec.org/en/

**Not emem's claim:** asset discovery.

**Useful contrast:** STAC primarily tells a client *what asset exists and where/how to access it*. emem's strongest fact path gives a specific physical observation a content-derived identity and a signed receipt a downstream agent can independently check.

Potential poster relationship:
```text
STAC / source catalogue
        ↓
selected upstream asset
        ↓
materialised observation
        ↓
emem fact_cid + receipt
```

## COG

**Established contribution:** cloud-native raster layout enabling clients to fetch only needed byte ranges.

Source: https://cogeo.org/

**Not emem's claim:** efficient raster transport.

**Useful contrast:** COG optimises access to raster bytes. emem field tokens name a signed derivation / artifact so an agent can carry a compact reference to a field and verify/recompute what it names.

## Google Earth Engine

**Established contribution:** managed, massive-scale geospatial computation; client expressions serialize into a DAG and execution is deferred until a result is requested.

Sources:
- https://developers.google.com/earth-engine/guides/deferred_execution
- https://developers.google.com/earth-engine/reference/rest/v1/Expression

**Not emem's claim:** lazy computation graphs over EO.

**Useful contrast:** Earth Engine's graph is primarily a computation mechanism inside its managed environment. emem's poster thesis should focus on **the externally portable identity of an observation/derived artifact and its use as shared state across agent boundaries**.

Do not say Earth Engine results are "unsigned" or "not reproducible" as a sweeping claim. Avoid unsupported negatives; explain emem by what it positively binds.

## W3C PROV

**Established contribution:** interoperable representation of provenance involving entities, activities, agents, derivation, versioning and reproducibility.

Source: https://www.w3.org/TR/prov-overview/

**Not emem's claim:** provenance itself.

**Useful contrast:** provenance can describe how something came to be. Content-derived observation identity additionally lets the receiver test whether the bytes it got are the bytes named by the reference.

The poster should show:
```text
provenance tells the lineage
content address checks the body identity
receipt checks the signed serving event / bound identifiers
```

## IPFS

**Established contribution:** generic content-addressed data; a CID is based on content and identifies retrievable data independent of storage location.

Source: https://docs.ipfs.tech/concepts/content-addressing/

**Not emem's claim:** generic CIDs.

**Useful contrast:** emem defines a domain object for physical observations with explicit spatial, temporal, semantic, uncertainty and provenance fields, plus agent-facing token semantics. The novelty is not hashing bytes; it is **what is made addressable and why that object is useful to reasoning agents**.

Important nuance: IPFS itself demonstrates that "same content → same address" is not novel. Never use that as the standalone invention claim.

## Nix

**Established contribution:** content-addressed store/build objects, reproducible build ideas, derivations and reusable artifacts.

Source: https://releases.nixos.org/nix/nix-2.34.1/manual/store/store-object/content-address.html

**Not emem's claim:** content-addressed build systems.

**Useful contrast:** the compelling emem analogy is:
> Nix-like durable artifacts, but the object graph is about observations of the physical world and the outputs are meant to survive between independent reasoning agents.

Call it an analogy, not a claim of equivalence.

## Agent-memory systems (Mem0 / LangChain ecosystem)

**Established contribution:** persistent memory outside the context window; retrieval of prior facts/interactions across sessions.

Sources:
- https://mem0.ai/
- https://www.langchain.com/blog/how-to-give-your-agent-memory

**Not emem's claim:** agents remembering after a reset.

**Useful contrast:** most general agent-memory framing is about retaining *context about users/tasks/conversations*. emem's strongest distinctive story is retaining **externally checkable physical-world observations** so the later agent can verify the underlying object rather than trust an extracted/summarised memory.

This distinction must be demonstrated, not asserted.

## The credible invention statement

Do not say:
> emem invented content addressing / provenance / persistent memory / data cubes / EO agents.

Say:
> **emem defines a verifiable memory protocol in which typed physical-world observations and fields become durable addressable state that independent agents can resolve, check and reuse across context, model and organisational boundaries.**

The paper must still establish novelty against literature. The poster's job is to make this mechanism and its utility obvious without claiming ownership of the older primitives it composes.
