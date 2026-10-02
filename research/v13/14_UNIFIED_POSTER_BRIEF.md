# v13.4 unified poster and formalism brief

Issue #48 establishes the Earth-to-agent story. The next round restores the formal model, implemented drift score, upstream test evidence and archived model outputs. The original grid and fail-closed gates remain.

## C. The complete printed text

### Header

> An Earth observation thatsurvives an agent handoff.
> EMEM gives an observation a lookup identity and a content-addressed record. Agent A passes the reference. Agent B resolves the same record and checks it before continuing.
> Earth data stays in the data layer. Its reference enters the reasoning layer.

### 1 · Earth to agents

> 1How does Earth data enter an agent workflow?
> Keep the source data upstream. Pass its reference.
> Locate an observation, record what was read, and carry its content address into the next agent's reasoning.
> In the controlled handoff test, prose led agents to act on 254 of 276 corruptions; a reference with explicit checking instructions, 0 of 300.

### 2 · One question, different records

> 2What can change between agents?
> One question, several records
> Scene, pixel, offset, rounding and stale state can change the value passed on.
> The same Keylong question yields eight values under these choices. Keeping the cited record makes the differences inspectable.

### 3 · Different drift, different check

> 3Where did the evidence change?
> A changed value needs a cause
> Keep the scene, pixel, model and time attached so a change can be investigated.
> World, instrument, alignment, model and noise. This is an attribution model; the numeric split remains open work.
> The implemented anchor score measures disagreement, not its cause. SAT-042 exercises it in a reference harness; live device-to-anchor wiring remains next work.

### Two identities

> Memory = observations + edges
> O* stores observations; E* stores typed temporal relations. Append new records and keep earlier ones.
> Relations can say supersedes or disagrees_with, with a validity interval.
> At address a and band b, bound observation time by t* and what memory knew by signing time τ.

### Concrete handoff

> Model outputs are records too
> Satellite input → encoder → vector record → content address
> Archived vectors: Prithvi names a checkpoint digest; TESSERA names a product year. These encoders are retired on the deployment; stored records remain addressable.

### 4 · Reference to record

> 4What exactly is handed over?
> A compact reference opens the observation record
> Resolve the value, place, time, derivation and source references from the record's address.
> BLAKE3 identifies the exact 1,115-byte record. A batch attestation covers its address. The record names the source files and read location; source checking continues by re-reading them.

### 5 · Checks back to the source

> 5Which changes can the receiver detect?
> Checks can continue back to the source
> Resolve → Re-hash → Bind → Recompute → Re-read
> Each step answers a different question. The matrix measures which changes become visible at each depth; signatures and log checks establish attestation and publication history.

### 6 · Source re-read

> 6What does returning to the source add?
> A valid record can preserve a wrong source read
> NDVI = (DN8 − DN4) / (DN8 + DN4 + 2o), o = −1000
> A record from the earlier reader still resolves: 0.3444 recorded, 0.4860 at the containing pixel. The source re-read exposes the pixel-selection difference.

### 7 · What checks establish

> 7What has the receiver established?
> Know what was checked
> Source quality remains inherited. Entity meaning and downstream decisions belong to the application using the evidence.

### 8 · Memory keeps what was cited

> 8Can a later agent recover the earlier state?
> Memory keeps what was cited
> Asked what memory knew on 15 Jun, recall returns 918.0 m. The later 915.07 m record reflects a provider change; it does not establish ground movement.

### 9 · Berlin multi-product stack

> 9What does one Berlin location reveal?
> One place, many observations
> Central Berlin: optical, radar, elevation, temperature, water, forest and biomass. One lookup cell organises 15 products, preserving each record and native grid.

### 10 · Token family

> 10What else can an agent carry?
> Beyond a single observation
> Choose the reference that preserves what the next agent needs to recover.

### Execution extension

> Measure each cause of change
> Validate numeric attribution under controlled scene, pixel and encoder changes. Repeat checked handoffs between separately operated agent hosts.

### 11 · Multiple runtimes

> 11The same reference can cross agent runtimes
> MCP, A2A, REST and SDKs expose the same reference model. One reference returned the same record and value through 11 client paths; receipt signatures were checked on 9 (30 Sep 2026). Surface status is labelled below.

### 12 · Complementary layers

> 12EO data into agent reasoning
> STAC describes assets; openEO defines processing; PROV and C2PA carry provenance. EMEM adds the observation reference an agent can pass on and resolve again.

### Conclusion

> An observation stays addressable across a handoff. The next agent can recover the cited record, inspect its provenance, recompute a declared recipe and return to its source.

## D. Claims map

Existing measured rows remain. `12_claims_map_additions_formalism.json` binds the restored equations and examples to pinned upstream source and retained evidence. The attribution decomposition is conceptual; the anchor score is implemented and has archived passing tests. The SDK and benchmark canonical encoder have fresh offline test results. Temporal Rust tests are inspected, not claimed as run here.

## Layout decisions

- Preserve the Earth-to-agent spine and the central verification/source experiments.
- Replace the repeated taxonomy with the drift equations, score thresholds and plain-language meanings.
- Use the left identity panel for the memory model, temporal relations and two-clock recall notation.
- Restore actual archived foundation-model vectors in place of the duplicate handoff panel.
- Replace the crowded memory timeline with one worked transaction-time example.
- Show the source NDVI formula and name its product-specific offset.
- State concrete next experiments: numeric attribution and independent-host handoffs.

## Scientific boundaries

Canonical record bytes determine the fact CID; batch attestation covers the address. No individual-fact signature formula is introduced. The conceptual memory tuple is not presented as a full wire schema. Product-year provenance is not called a checkpoint digest. A provider change is not treated as physical ground movement. SAT-042 remains a deterministic reference harness. Archived Rust results and fresh Python results carry different dates and commits. Qwen remains separate from pooled Claude results. The old signed track is not attached to this new PDF.
