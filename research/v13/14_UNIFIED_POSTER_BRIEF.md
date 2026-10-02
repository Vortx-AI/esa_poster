# v13.9 unified poster and community brief

Keep the complete handoff, token family, Berlin fanout and exact memory formalism restored in v13.7. Recover the dated NDVI history and explain memory operations through EO tasks. Make community entry points usable while preserving the scope of the scientific evidence. See `23_EO_GOLD_AND_USABILITY.md` for the recovery decisions and `22_RECOVERED_DESIGN_AND_FORMALISM.md` for the preceding restoration.

## C. The complete printed text

### Header

> An Earth observation thatsurvives an agent handoff.
> EMEM gives a sampled or derived observation a reusable reference. The next agent recovers its value, location, acquisition time and processing recipe, then checks the evidence.
> A compact citation keeps the observation traceable across agents and time.

### 1 · Earth to agents

> What survives an agent handoff?
> The same observation, carried through receiver checks.
> Agent A cites a source read. A relay changes the evidence. Agent B acts on it or checks the reference.
> In the controlled handoff test, prose led agents to act on 254 of 276 corruptions; a reference with explicit checking instructions, 0 of 300.

### 2 · Traceable observation history

> Can a time series retain its evidence?
> NDVI history, with citations
> Each value retains its dated record.
> Cloud/snow screening and processing harmonisation were not applied; physical interpretation needs both.

### 3 · Different drift, different check

> Where did the evidence change?
> A changed value needs a cause
> A cited value can change during a handoff. Between acquisitions, the surface, sensor or processing may also change.
> Surface change, instrument, registration, encoder and residual. Δz is the later value minus the earlier one. The attribution ledger links evidence to each term; the numeric split remains open.
> The implemented anchor score measures disagreement, not its cause. SAT-042 exercises it in a reference harness; live device-to-anchor wiring remains next work.

### Memory operations

> Use it in an EO workflow
> Compare vegetation observations, keep conflicting product estimates and pass the cited evidence onward. Single-hop retrieval is implemented; multi-hop planning remains open.
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
> An EMEM cell indexes a location. Products retain their native pixels; CHIRPS records an out-of-coverage absence.

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

### 8 · Revisit the earlier evidence

> Can a later agent recover the earlier state?
> Revisit the earlier evidence
> Latest-as-of mode: take the versions known by signing time τ, then the latest valid time ≤ t*. No candidate gives an empty result; CID order breaks ties.
> As of 15 Jun → 918.0 m. The later 915.07 m is a provider change. Temporal storage is established; the handoff adds a portable citation to the exact earlier record.

### Complete observation and memory model

> What does the memory contain?
> Observations + temporal edges
> a: location cell · b: variable · t: valid time · v: valueu: uncertainty · p: provenance, recipe, signing times: attestation associated with the observation
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
> Measured separately: same record and value through 11 client paths; receipt signatures checked on 9 (30 Sep 2026).

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


## v13.9 workflow and community layout

A seven-step diagram now precedes section 1: Observe → Locate → Record → Hand off → Resolve → Check → Continue. Locate states location/product/time lookup; Record names the canonical record CID and batch attestation. Checks name hash, binding and signature, with source re-reading as a further step. The full controlled handoff experiment follows immediately.

Section 11 removes repeated explanatory prose and its redundant four-stage bridge. It retains the measured client-path result, five platform cards, all 33 remaining community labels at their existing sizes, and a dedicated 50 mm Connect QR. The community band is 91.5 mm high rather than 147.5 mm, releasing 56 mm. The handoff and all three columns move down by 56 mm; all 11 existing scientific figures retain their dimensions and content. No scientific evidence, measurements, claim status or integration evidence changes. The companion site's existing download link picks up the new PDF when main is updated.
