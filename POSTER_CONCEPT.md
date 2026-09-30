# Poster concept — emem at Agentic AI for Earth Observation

> **⚠ Checked against emem source on 2026-09-29.** Several statements below were imprecise or wrong (signature placement, CBOR profile, token families, orbit, encoders). The corrected wording lives in [research/should_do/04_VERIFIED_CLAIMS_LEDGER.md](research/should_do/04_VERIFIED_CLAIMS_LEDGER.md); the list of fixes is in [research/do_not_use/03_CORRECTIONS_TO_CURRENT_CONCEPT.md](research/do_not_use/03_CORRECTIONS_TO_CURRENT_CONCEPT.md). Inline fixes are marked **[v2]**.

## Respect the paper title

**emem: A research on Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings**

The poster should not rename the work into a startup slogan. The title remains the title. The visual story beneath it explains the invention.

---

## One-line research claim

> **emem turns Earth observation into durable reasoning state that survives the model doing the reasoning.**

Alternative large visual line:

> **The satellite observation can outlive the agent.**

Supporting line:

> Pixels become addressable evidence. Evidence becomes persistent world state. Agents come and go; the state remains.

---

## 1. The new object

The unit of memory is one observation:

```text
O = (a, b, t, v, u, p, s)
```

Where:

- `a` — canonical spatial address (`cell64`)
- `b` — semantic band/type
- `t` — valid time (plus transaction time in provenance)
- `v` — scalar, vector, embedding, or derived value
- `u` — uncertainty/confidence
- `p` — provenance, source ids, derivation rule, encoder/version
- `s` — signer public key + `signed_at` **[v2]** (the ed25519 signature is on the enclosing attestation, over a Merkle root of fact CIDs)

The atom is the observation, not the model output and not the file.

---

## 2. The load-bearing invariant

```text
canonical bytes
      ↓
BLAKE3(bytes)
      ↓
fact_cid
```

```text
fact_cid = base32(BLAKE3(emem-CBOR(O)))   [v2: declaration-ordered, float-canonical; not RFC 8949 key-sorted]
```

For `emem:fact:`:

- the bytes that are hashed are the bytes that are stored;
- equal canonical bytes independently produce the same name; **[v2]** because `signer` and `signed_at` are hashed, a CID names one *signed attestation* — two attesters of the same value mint different CIDs;
- any changed byte produces a different name;
- the client can re-hash the body and detect substitution (the resolver itself checks the cell and fails with 409; **the client** re-hashes).

This is the scientific core.

### The line to print large

> **The reference is no longer a sentence describing the evidence. The reference is a cryptographic function of the evidence.**

---

## 3. The token is an address, not the payload

```text
emem:fact:<cell64>:<fact_cid>
```

A receiving agent can:

```text
TOKEN
  ↓
RESOLVE
  ↓
CANONICAL BYTES
  ↓
RE-HASH
  ↓
CID MATCH?
  ↓
VERIFY RECEIPT
```

The receiving model does not have to trust the previous agent's prose.

Important precision: this strong byte-identity claim applies to `emem:fact:`. Other token families have different semantics and should not be presented as equivalent.

---

## 4. Why this matters for agents

### Conventional pipeline

```text
EO → model → prose → summary → compaction → handoff → paraphrase
```

At every textual hop, the referent can drift.

### emem pipeline

```text
EO → observation O → CID/token ─────────────┐
                                            ├→ Agent A
                                            ├→ Agent B
                                            ├→ later session
                                            └→ different model
```

Each party can resolve back to the same observation bytes.

### Poster line

> **Share the evidence. Not the context.**

---

## 5. Long-horizon agent continuity

The skills make the research consequence concrete.

### Before reset

```text
SESSION 01
research + tools + reasoning
context fills
↓
checkpoint tokens + file_cids
```

### After reset / model swap

```text
SESSION 02
resolve tokens
verify signed notes
continue from checkable state
```

Large line:

> **Context can die. The investigation doesn't.**

The checkpoint should contain tokens and content ids, not paraphrased numbers.

---

## 6. Multi-agent handoff as a trust boundary

Agent A's private context does not need to cross.

```text
Agent A                               Agent B
private prompt     ┌────────────┐     different model
hidden reasoning   │ TRUST      │     no shared database
tool history       │ BOUNDARY   │     no reason to trust A
                   └─────┬──────┘
                         │
                 emem:fact:...
                         │
                         ▼
                   resolve + verify
```

The receiver cannot replay Agent A's thought process. It can check the evidence object that Agent A cited.

---

## 7. Foundation-model embeddings become observations, not authority

The paper title explicitly says "over Foundation-Model Embeddings."

Show:

```text
EO input x
   ↓
foundation encoder @ checkpoint
   ↓
embedding z
   ↓
O = (place, time, embedding, uncertainty, provenance, signature)
   ↓
CID(O)
```

The embedding is the representation layer. emem adds continuity, identity, provenance and verification around it.

Poster line:

> **The embedding is not memory. The addressable observation around it is.**

---

## 8. From point facts to fields

A world model needs spatial fields, not only scalar point facts.

Use a precise progression:

```text
emem:fact:      one observation
emem:raster:    one spatial field over an AOI
emem:cube:      that field through time
emem:rasterset: a bound set of fields
```

For field tokens, the receipt binds the derivation record: AOI, source scene, recipe, time, and artifact hash. The artifact can be re-hashed or recomputed from the pinned derivation.

This is how satellite intelligence can arrive directly as a model-readable reasoning object rather than as a human-authored paragraph.

---

## 9. The deeper systems thesis

### A content-addressed build graph over the physical world

```text
Sentinel-2 B04 ─┐
                ├─ NDVI@1 ─→ signed observation ─→ CID
Sentinel-2 B08 ─┘

May raster  ─┐
June raster ─┼─ cube manifest ─→ CID
July raster ─┘

EO scene ─→ encoder@checkpoint ─→ embedding ─→ observation ─→ CID
```

If a deterministic artifact already exists and remains valid, another agent should not spend tokens re-deriving it. It resolves it by name and checks it.

That is the "wow" for multi-agent scale: shared, reusable computational state about the physical world.

---

## 10. One continuous investigation

Recommended lower-third visual:

```text
EARTH
  │
OBSERVATION
  │
canonicalise + sign
  │
CONTENT ID
  │
  ├── Agent A: research
  ├── Agent B: inspect
  ├── Agent C: continue after handoff
  ├── Agent D: resume after context reset
  │
verify-before-publish
  │
ACTION
```

Large caption:

> **One observation. Many reasoners. One continuous investigation.**

---

## 11. Why it works

Use six compact scientific mechanisms, not marketing feature boxes:

1. **Canonical encoding** — same observation serializes to the same bytes.
2. **Content-derived identity** — changed content changes the CID.
3. **Spatial binding** — a valid fact cannot silently be relabelled under another cell.
4. **Signed receipt** — request id, time, primitive, cells, fact ids, as-of, manifest and Merkle proof (or signed ABSENT marker) are bound to a responder key. **[v2]** Full query parameters are not bound.
5. **Immutable evolution** — corrections become new observations; old state remains replayable.
6. **Pinned semantics** — bands, sources, schema and function registry are content-addressed and bound into receipts. **[v2]** `algorithms_cid` is published but not in the receipt preimage.

---

## 12. What this enables

These should appear as consequences of the mechanism, not as product tiles:

- long-horizon agents that resume from verified state;
- multi-agent handoff across vendors/models;
- context compaction without losing the underlying referent;
- direct delivery of EO facts/fields/cubes into agent reasoning;
- research-grade citations with reproducible estimands;
- contradiction detection without averaging disagreement away;
- verify-before-publish gates over measurable claims;
- append-only transparency history;
- reusable EO computation instead of repeated reasoning.

---

## 13. What it does NOT prove

Scientists will trust the poster more if this is explicit.

**Proves / makes checkable**

- co-reference for strongly bound fact tokens;
- byte integrity;
- provenance binding;
- signer identity;
- replayability;
- append-only history when log proofs are pinned.

**Does not prove**

- objective truth of a measurement;
- model correctness;
- perfect entity co-reference;
- that a signed model output is accurate;
- a numeric causal split of observed change.

---

## Suggested composition

### Top 20%
Exact paper title + one-line thesis.

### Middle 45%
One large mechanism:
`O → canonical bytes → CID → token → resolve → verify`

Beside it, the comparison:
`prose handoff` vs `address handoff`.

### Lower-middle 20%
Long-horizon and multi-agent continuity diagram.

### Bottom 15%
Field/cube extension + "content-addressed build graph over the physical world" + honest limits + QR/source.

---

## Visual rules

- Scientific poster, not product launch.
- No cute robots.
- No glowing "AI brain" imagery.
- No generic startup five-step feature row.
- No claim that signatures imply truth.
- Very little prose.
- Equations and invariants large enough to read from a distance.
- One real `emem:fact:` token example.
- One real raster/cube token example.
- Minimal emem/Vortx branding.
- Let the paper title carry authority; let the mechanism carry novelty.
