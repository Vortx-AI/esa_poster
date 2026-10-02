# v13.3 unified poster brief

Issue #48 and its tightening comment supersede the earlier face copy. The original A0 grid, evidence sources and fail-closed build gates remain. This edition uses the final R5 results and three printed QR tasks.

## C. The complete printed text

### Header

> An Earth observation thatsurvives an agent handoff.
> EMEM gives an observation a lookup identity and a content-addressed record. Agent A passes the reference. Agent B resolves the same record and checks it before continuing.
> Earth data stays in the data layer. Its reference enters the reasoning layer.

### 1 · Earth to agents

> How does Earth data enter an agent workflow?
> Keep the source data upstream. Pass its reference.
> Locate an observation, record what was read, and carry its content address into the next agent's reasoning.
> In the controlled handoff test, prose led agents to act on 254 of 276 corruptions; a reference with explicit checking instructions, 0 of 300.

### 2 · One question, different records

> What can change between agents?
> One question, several records
> Scene, pixel, offset, rounding and stale state can change the value passed on.
> The same Keylong question yields eight values under these choices. Keeping the cited record makes the differences inspectable.

### 3 · Different drift, different check

> Where did the evidence change?
> Match the drift to the check
> Compare the fields that identify the observation, then follow its derivation and source.
> These checks address distinct failures seen in the records and handoff tests. The methods link each example to its evidence.

### Two identities

> Two identities, two jobs
> Where · product · observation time
> Find the observation family.
> The exact canonical record
> Recover what the earlier agent cited.
> emem:fact:<cell64>:<fact_cid>
> The token carries the cell and record address. Product and observation time are fields inside the record.

### Concrete handoff

> Carry one reference forward
> ↓ the 84-character reference ↓
> In the recorded two-process handoff, the reference alone crossed the process boundary. The receiving program re-hashed the record, checked its receipt and reproduced its NDVI exactly.

### 4 · Reference to record

> What exactly is handed over?
> A compact reference opens the observation record
> Resolve the value, place, time, derivation and source references from the record's address.
> BLAKE3 identifies the exact 1,115-byte record. A batch attestation covers its address. The record names the source files and read location; source checking continues by re-reading them.

### 5 · Checks back to the source

> Which changes can the receiver detect?
> Checks can continue back to the source
> Resolve → Re-hash → Bind → Recompute → Re-read
> Each step answers a different question. The matrix measures which changes become visible at each depth; signatures and log checks establish attestation and publication history.

### 6 · Source re-read

> What does returning to the source add?
> A valid record can preserve a wrong source read
> Re-reading the named source lets the receiver test the measurement itself.
> A record from the earlier reader still resolves: 0.3444 recorded, 0.4860 at the containing pixel. The source re-read exposes the pixel-selection difference.

### 7 · What checks establish

> What has the receiver established?
> Know what was checked
> Source quality remains inherited. Entity meaning and downstream decisions belong to the application using the evidence.

### 8 · Memory keeps what was cited

> Can a later agent recover the earlier state?
> Memory keeps what was cited
> A later observation does not replace an earlier citation. Asked about 15 Jun, memory returns 918.0 m; the receiver can still resolve and check that record by its content address.

### 9 · Berlin multi-product stack

> What does one Berlin location reveal?
> One place, many observations
> Central Berlin: optical, radar, elevation, temperature, water, forest and biomass. One lookup cell organises 15 products, preserving each record and native grid.

### 10 · Token family

> What else can an agent carry?
> Beyond a single observation
> Choose the reference that preserves what the next agent needs to recover.

### Execution extension

> Bind an output to its run
> SAT-042 records a test execution trace. Its gate checks the output's value digest; code and model identity are recorded in the trace. Full harness and scope in Reproduce.

### 11 · Multiple runtimes

> The same reference can cross agent runtimes
> MCP, A2A, REST and SDKs expose the same reference model. One reference returned the same record and value through 11 client paths; receipt signatures were checked on 9 (30 Sep 2026). Surface status is labelled below.

### 12 · Complementary layers

> EO data into agent reasoning
> STAC describes assets; openEO defines processing; PROV and C2PA carry provenance. EMEM adds the observation reference an agent can pass on and resolve again.

### Conclusion

> An observation stays addressable across a handoff. The next agent can recover the cited record, inspect its provenance, recompute a declared recipe and return to its source.

## D. Claims map

All numeric claims retain their original measured rows. The U.* rows in `12_claims_map_additions_unified.json` map the explanatory synthesis to its mechanism and evidence. Full mutation details, threat model, research questions and execution limits remain in the methods.

## Layout decisions

- Keep the header, mechanism spine, three columns and bottom ecosystem band.
- Replace the questions/threat panels with two identities and a measured two-process handoff.
- Put benchmark results below the mechanism, keeping the complete matrix in the centre.
- Enlarge the Berlin image and give its native-grid table the full column width.
- Move the execution figure and detailed token/verification catalogues behind Reproduce.
- Three printed QR tasks: Try it, Inspect, Reproduce. Existing web routes stay available.

## Scientific boundaries

- The content address identifies the canonical record. A batch attestation covers its address.
- The fact token contains cell and CID; product and observation time are in the record.
- The pooled result describes the recorded Claude runs; Qwen is separate.
- The concrete two-process handoff is a program experiment, not a cross-host ChatGPT/Claude trial.
- ChatGPT remains a publisher listing; it is not relabelled as a runtime tested by this work.
- The archived signed track identifies its earlier PDF, not the revised PDF.
