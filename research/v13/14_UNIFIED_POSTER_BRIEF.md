# Reviewed v13 poster and community brief

Keep the complete handoff, token family, Berlin fanout and exact memory formalism restored in v13.7. Recover the dated NDVI history and explain memory operations through EO tasks. Make community entry points usable while preserving the scope of the scientific evidence. See `23_EO_GOLD_AND_USABILITY.md` for the recovery decisions and `22_RECOVERED_DESIGN_AND_FORMALISM.md` for the preceding restoration.

Review of 2 Oct 2026: restore the source-driven eight-value example and complete evidence object, keep the drift decomposition on one line with the implemented score below it, consolidate the checked-reference scope into panel 7, and print the demonstrated SAT-042 execution harness. Remove future-work prose and generic test-count copy from the face.

## C. The complete printed text

Rendered running copy for the reviewed source. Figure labels, equations outside running text, scope metadata and references retain their claim rows.

### Header

> An Earth observation that survives an agent handoff.

> emem gives a sampled or derived observation a reusable reference. The next agent recovers its value, location, acquisition time and processing recipe, then checks the evidence.

> Agent A cites a satellite observation. What can agent B check without trusting A, A’s model, or us?

> emem makes raw satellite observations addressable by place, band and time, each a signed record named by the BLAKE3 hash of its bytes. The exact evidence A cites survives compaction, a change of model and a handoff; B re-hashes it, verifies the log entry and receipt offline, and traces it to the source pixel. Agents cannot write observations, and a changed, rounded or forged value no longer matches its name.

> A compact citation keeps the observation traceable across agents and time. Encode in orbit, decode in AI’s reasoning with emem.

### 1 · Earth to agents

> What survives an agent handoff?

> The same observation, carried through receiver checks.

> Agent A cites a source read. A relay changes the evidence. Agent B acts on it or checks the reference.

> [variant:0of300] In the controlled handoff test, prose led agents to act on 254 of 276 corruptions; a reference with explicit checking instructions, 0 of 300.

> [variant:300of300] In the controlled handoff test, agents with a checked reference and explicit instructions did not act on corrupted evidence in 300 of 300 trials (264 declined, 36 used the genuine record); with prose, 22 of 276.

> Earth data stays on the encoding device in orbit; its reference is downlinked and enters the AI’s reasoning (design; SAT-042 reference harness).

### 2 · One NDVI, eight values

> How does a value change between agents?

> One NDVI, eight values

> At Keylong on 25 Sep 2026, scene, date, pixel and arithmetic choices change the reported NDVI.

> Six cross the constructed irrigation threshold; one exceeds the expected NDVI range. Each calls for a different check.

### 3 · Different drift, different check

> Where did the evidence change?

> A changed value needs a cause

> Between acquisitions, the surface, sensor, location or processing can change.

> Δz: change in readout. Environment · sensor · geolocation · encoder · residual. emem's change attribution links evidence to each term.

> The implemented score measures disagreement with an anchor. SAT-042 applies it to a fixed reference in the execution harness.

### Memory operations

> Use it in an EO workflow

> Compare vegetation observations, retain conflicting estimates and pass their references onward. Single-hop retrieval materialises the requested observation.

### 7 · What checks establish

> What does a checked reference establish?

> Know what was checked

> Record checks establish properties of the cited record. A source re-read adds evidence about the sampled pixel; sensor accuracy remains inherited.

### Full trace

> Token · record · source pixel

> Without emem software, a 698-line script (Python stdlib, blake3, cbor2, pynacl) checked 15 links (17 checks) in 17.9 s, all verified. Grey: what must still be trusted after each check.

### Contribution and prior art

> Checkable observation handoff

> An agent passes a reference to a specific physical observation; the receiver resolves it and checks the evidence.

> Built with standard BLAKE3, Ed25519, CBOR and Merkle logs. STAC, openEO, PROV, C2PA, RAG and temporal storage provide complementary layers.

### 4 · What exactly is handed over

> What exactly is handed over?

> A compact reference to an exact record

> The receiver uses an 84-character reference to fetch the record and its evidence.

> BLAKE3 identifies the 1,115-byte record. Its fields name the source files, sampled point and derivation; a batch signature covers the record address. Source-file hashes are absent from this record.

### 5 · Checks back to the source

> Which changes can the receiver detect?

> Checks can continue back to the source

> Resolve · Re-hash · Bind · Recompute · Re-read

> Deeper checks expose different corruptions. Checked-reference agents made the expected decision on 71 of 72 genuine controls; one was refused (pooled Claude).

### 6 · Source re-read

> A valid record can preserve a wrong source read

> NDVI = (DN8 − DN4) / (DN8 + DN4 + 2o), o = −1000 (product offset)

### 8 · Revisit the earlier evidence

> Can a later agent recover the earlier state?

> Revisit the earlier evidence

> Latest-as-of mode: take the versions known by signing time τ, then the latest valid time ≤ t*. No candidate gives an empty result; CID order breaks ties.

> The later 915.07 m reflects a provider change. The earlier citation still resolves to the earlier estimate.

### Complete observation and memory model

> What does the memory contain?

> Observations + temporal edges

> a: location cell · b: variable · t: valid time · v: value u: uncertainty · p: provenance, recipe, signing time s: attestation associated with the observation

> Conceptual tuple: a batch attestation covers the fact address; a signed read receipt binds the response.

> Append observations and supersedes / disagrees_with edges; keep earlier records.

### 10 · Token family

> What else can an agent carry?

> Beyond a single observation

> The emem token family is how agents read Earth observation: one grammar for a place, a value, a raster, a time series or a device run.

> Eight facts resolve through one bundle; four state addresses re-hash. These object checks do not validate an agent's reasoning.

### 11 · Satellite execution evidence

> Satellite execution evidence

> A signed trace binds the reported run

> SAT-042 scripted pass · reference harness · 30 Sep 2026.

> Reference harness, no spacecraft enrolled. The admission gate binds output value digests; band, cell and time are outside this check.

### 12 · Community routes

> Use emem. Carry the evidence forward.

> Measured separately: same record and value through 11 client paths; receipt signatures checked on 9 (30 Sep 2026).

## D. Claims map

Existing measured rows remain. `12_claims_map_additions_formalism.json` binds the restored equations and examples to pinned upstream source and retained evidence. The attribution decomposition is conceptual; the anchor score is implemented and has archived passing tests. The SDK and benchmark canonical encoder have fresh offline test results. Temporal Rust tests are inspected, not claimed as run here.

## Layout decisions

- Preserve the Earth-to-agent spine and the central verification/source experiments.
- Replace the repeated taxonomy with the drift equations, score thresholds and plain-language meanings.
- Use the left identity panel for the memory model, temporal relations and two-clock recall notation.
- Restore the L0 to L5 verification ladder in the left story flow; remove the archived-vector detour from the face.
- Replace the crowded memory timeline with one worked transaction-time example.
- Show the source NDVI formula and name its product-specific offset.
- Keep the drift decomposition on one line and restore the SAT-042 execution-verification strip instead of a next-experiments prose block.

## Scientific boundaries

Canonical record bytes determine the fact CID; batch attestation covers the address. No individual-fact signature formula is introduced. The conceptual memory tuple is not presented as a full wire schema. Product-year provenance is not called a checkpoint digest. A provider change is not treated as physical ground movement. SAT-042 remains a deterministic reference harness. Archived Rust results and fresh Python results carry different dates and commits. Qwen remains separate from pooled Claude results. The old signed track is not attached to this new PDF.


## v13.5 recovery and community

See `18_RECOVERED_CONTRIBUTIONS_AND_COMMUNITY.md` for the history audit. `12_claims_map_additions_community.json` adds typed absence, bundle and reasoning-state examples plus community availability. The community figure is 801 × 91 mm with 28 pt platform names. CONNECT opens /use/, linking methods, tests, setup and the restored EO gallery. Related-work context moves to the left column; the central experiments retain their original space.


## v13.7 restoration

The current placement, complete model and claim taxonomy supersede the earlier layout decisions above. Berlin now occupies the central source-record panel, the full model is on the right, and the full token table and experimental flow are restored. Duplicate prose made room; print sizes were not reduced.


## v13.9 workflow and community layout

A seven-step diagram now precedes section 1: Observe → Locate → Record → Hand off → Resolve → Check → Continue. Locate states location/product/time lookup; Record names the canonical record CID and batch attestation. Checks name hash, binding and signature, with source re-reading as a further step. The full controlled handoff experiment follows immediately.

Section 11 removes repeated explanatory prose and its redundant four-stage bridge. It retains the measured client-path result, five platform cards, all 33 remaining community labels at their existing sizes, and a dedicated 50 mm Connect QR. The community band is 91.5 mm high rather than 147.5 mm, releasing 56 mm. The handoff and all three columns move down by 56 mm; all 11 existing scientific figures retain their dimensions and content. No scientific evidence, measurements, claim status or integration evidence changes. The companion site's existing download link picks up the new PDF when main is updated.
