# v13.7 unified poster and community brief

Recover the complete handoff experiment, full token table and Berlin fanout from the two requested historical commits. Complete the formalism from pinned implementation sources. Preserve the current results, community routes and fail-closed A0 gates. See `22_RECOVERED_DESIGN_AND_FORMALISM.md` for the restoration and scientific review.

## C. The complete printed text

### Header

> An Earth observation thatsurvives an agent handoff.
> EMEM gives an observation a lookup identity and a content-addressed record. Agent A passes the reference. Agent B resolves the same record and checks it before continuing.
> Earth data stays in the data layer. Its reference enters the reasoning layer.

### 1 · Earth to agents

> What survives an agent handoff?
> The same observation, carried through receiver checks.
> Agent A cites a source read. A relay changes the evidence. Agent B acts on it or checks the reference.
> In the controlled handoff test, prose led agents to act on 254 of 276 corruptions; a reference with explicit checking instructions, 0 of 300.

### 2 · One question, different records

> What can change between agents?
> One question, several records
> Scene, pixel, offset, rounding and stale state can change the value passed on.
> The same Keylong question yields eight values under these choices. Keeping the cited record makes the differences inspectable.

### 3 · Different drift, different check

> Where did the evidence change?
> A changed value needs a cause
> References can drift during a handoff; readouts can change between visits. Keep both questions separate.
> World, instrument, alignment, model and noise. Δz is the later readout minus the earlier one. The attribution ledger links evidence to each term; the numeric split remains open.
> The implemented anchor score measures disagreement, not its cause. SAT-042 exercises it in a reference harness; live device-to-anchor wiring remains next work.

### Memory operations

> Compute over the memory
> Typed memory operations retain the evidence behind an answer. Single-hop materialisation is implemented; multi-hop planning remains open.
> 20 upstream offline SDK / encoding tests passed.

### Concrete handoff

> Model outputs are records too
> Satellite input → encoder → vector record → content address
> Archived vectors: Prithvi names a checkpoint digest; TESSERA names a product year. These encoders are retired on the deployment; stored records remain addressable.

### Contribution and prior art

> Checkable observation handoff
> An agent passes a reference to a specific physical observation; the receiver resolves it and checks the evidence.
> Built with standard BLAKE3, Ed25519, CBOR and Merkle logs. STAC, openEO, PROV, C2PA, RAG and temporal storage provide complementary layers.

### Berlin source-to-record fanout

> What does one Berlin location reveal?
> One cell, many source records
> One lookup joins the evidence; each product keeps its own time, provenance and native grid.
> Absence is citable too: CHIRPS reports outside its latitude range. A common cell does not make these products co-registered.

### 5 · Checks back to the source

> Which changes can the receiver detect?
> Checks can continue back to the source
> Resolve → Re-hash → Bind → Recompute → Re-read
> Deeper checks expose different corruptions. Checked-reference agents made the expected decision on 71 of 72 genuine controls; one was refused (pooled Claude).

### 6 · Source re-read

> A valid record can preserve a wrong source read
> NDVI = (DN8 − DN4) / (DN8 + DN4 + 2o), o = −1000 (product offset)

### 7 · What checks establish

> What has the receiver established?
> Know what was checked
> Checks establish properties of the cited record. A source re-read adds evidence; sensor accuracy remains inherited.

### 8 · Memory keeps what was cited

> Can a later agent recover the earlier state?
> Memory keeps what was cited
> Latest-as-of mode: take the versions known by signing time τ, then the latest valid time ≤ t*. No candidate gives an empty result; CID order breaks ties.
> As of 15 Jun → 918.0 m. The later 915.07 m is a provider change. Temporal storage is established; the handoff adds a portable citation to the exact earlier record.

### Complete observation and memory model

> What does the memory contain?
> Observations + temporal edges
> a: cell · b: band · t: valid time · v: valueu: uncertainty · p: provenance, recipe, signing times: attestation associated with the observation
> Conceptual tuple: a batch attestation covers the fact address; a signed read receipt binds the response.
> Append observations and supersedes / disagrees_with edges; keep earlier records.

### 10 · Token family

> What else can an agent carry?
> Beyond a single observation
> Eight facts resolve through one bundle; four checkpoint hashes reproduce. These object checks do not validate an agent's reasoning.

### Execution extension

> Measure each cause of change
> Control scene, pixel and encoder changes to test numeric attribution. Connect device outputs to separately recalled anchors. Repeat handoffs across separately operated hosts.

### 11 · Community routes

> Use emem. Carry the evidence forward.
> Connect a plugin, a workflow or your own code. Public emem reads need no API key; the source is open.
> Measured separately: the same record and value through 11 client paths; receipt signatures checked on 9 (30 Sep 2026).The routes below are plugins, connectors, packages and listings. One evidence protocol, multiple agent runtimes. Setup and compatibility notes are behind CONNECT.

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


## v13.5 recovery and community

See `18_RECOVERED_CONTRIBUTIONS_AND_COMMUNITY.md` for the history audit. `12_claims_map_additions_community.json` adds typed absence, bundle and reasoning-state examples plus community availability. The community figure is 801 × 91 mm with 28 pt platform names. CONNECT opens /use/, linking methods, tests, setup and the restored EO gallery. Related-work context moves to the left column; the central experiments retain their original space.


## v13.7 restoration

The current placement, complete model and claim taxonomy supersede the earlier layout decisions above. Berlin now occupies the central source-record panel, the full model is on the right, and the full token table and experimental flow are restored. Duplicate prose made room; print sizes were not reduced.
