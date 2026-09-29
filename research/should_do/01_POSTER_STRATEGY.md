# What we should do

## 1. Lead with the protocol object, not the company

The accepted title already does the right thing:

**EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings**

Under it, explain one invention:

> **Earth observation as durable, externally addressable reasoning state.**

The first 10 seconds should show:
```text
O = (a,b,t,v,u,p,s)
CID(O) = BLAKE3(CanonicalCBOR(O))
emem:fact:<cell64>:<fact_cid>
```

Then show what a second agent can independently do with that address.

## 2. Show the trust-boundary experiment

A strong poster needs one concrete falsifiable handoff:

```text
Agent A
  reads observation
  keeps token
        |
        |  only this crosses
        v
emem:fact:<cell>:<cid>
        |
        v
Agent B
  resolve
  re-hash
  verify signature
  recover exact signed observation
```

The receiver should not need Agent A's prompt, hidden context, summary or model.

This is much stronger than a generic architecture diagram.

## 3. Show long-horizon continuity as a systems consequence

Make the reset visible:

```text
session 1 → context compaction ×
               |
               | tokens + file_cids survive
               v
session 2 → resolve + verify → continue
```

Use the precise phrase:

> **Context can die. The investigation doesn't.**

Explain that emem recommends checkpointing tokens / content ids, not paraphrased numeric summaries.

## 4. Show EO fields, not only scalar facts

For this audience, a world model consuming an actual field is more compelling than another LLM chat example.

Use a real progression:

```text
emem:fact:      one signed observation
emem:raster:    a spatial field over an AOI
emem:cube:      that field through time
emem:rasterset: a bound set of fields
```

Explain that the field token binds a signed derivation containing the AOI, scene, recipe, time and artifact hash. A third party can re-hash the artifact or recompute it from the pinned derivation.

This is where "satellite intelligence directly into model reasoning" becomes technically concrete.

## 5. Show the build-graph interpretation

Use one tiny derivation graph:

```text
Sentinel-2 B04 ─┐
                ├─ NDVI@1 ─→ observation ─→ CID
Sentinel-2 B08 ─┘

May raster  ─┐
June raster ─┼─ cube manifest ─→ CID
July raster ─┘
```

Caption:

> **A content-addressed build graph over the physical world.**

Then make the consequence explicit:

> If valid deterministic state already exists, a later agent resolves and checks it instead of spending tokens re-deriving it.

## 6. Use comparison by object boundary, not by brand attack

A compact scientific comparison can clarify novelty:

| Layer | Primary object |
|---|---|
| STAC | metadata record describing a spatiotemporal asset |
| COG | cloud-readable raster file |
| Earth Engine | expression / computed geospatial object inside a managed compute environment |
| W3C PROV | provenance graph |
| IPFS / Nix | generic content-addressed content/build object |
| agent-memory systems | persistent retrieved context |
| **emem** | **typed physical observation / field with externally checkable identity and receipt** |

Do not say the others lack trust or reproducibility categorically. State only the object each is primarily designed around.

## 7. Make the limits visible

A scientist should see one "BOUNDARY OF CLAIM" box.

### What is checkable
- fact-token co-reference;
- byte integrity;
- spatial binding;
- signer / receipt integrity;
- provenance fields;
- replay of old state;
- append-only log consistency when proofs are pinned.

### What is not proved
- objective truth;
- sensor calibration;
- causal attribution of a change;
- model correctness;
- universal entity co-reference;
- correctness of a prose conclusion.

This honesty is part of the differentiation.

## 8. Use one real token and one real verification trace

Do not fill the poster with fake `emem:abc...` strings.

Before final export:
- mint or select one real `emem:fact:` token;
- show the actual resolved `value_verbatim`, band, source and observed time;
- show re-hash / receipt verification;
- select one real `emem:raster:` or `emem:cube:` token and show its derivation record.

Scientists should be able to scan the QR, reproduce the call, and challenge the claim.

## 9. Make it usable from the poster

The poster should end in a tiny "REPRODUCE THIS" block, not "Book a demo."

Suggested:
```text
1. scan
2. resolve this token
3. recompute its hash
4. verify the receipt offline
5. hand the same token to another model
```

QR targets:
- source repository;
- exact verification example;
- paper DOI.

## 10. Visual language

Aim for:
- a paper figure enlarged to poster scale;
- sparse typography;
- one dominant invariant;
- black/white + one accent;
- actual tokens and byte/hash diagrams;
- no people/robots;
- no stock satellite hero unless it carries information;
- citations adjacent to claims;
- methods over marketing.

The visual should look at home next to a systems paper and an EO methods paper simultaneously.
