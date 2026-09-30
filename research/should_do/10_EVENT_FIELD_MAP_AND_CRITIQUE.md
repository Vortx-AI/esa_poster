# ESA Agentic AI for Earth Observation — field research and poster critique
## Research snapshot: 30 September 2026

This review covers the official Berlin workshop programme, all 43 listed posters, the most relevant thematic overlaps, the current EMEM poster source material in this repository, and current EO-agent research directly relevant to EMEM's scientific claim.

The workshop has **43 posters in two sessions**: 23 on 19 October and 20 on 20 October. EMEM is poster 4 in Session 1, alongside work on EO data selection, multimodal RAG, agent evaluation, geo-agents, multi-agent orchestration, datacubes, explainability, change detection, crisis awareness, trustworthy discovery, and geospatial guardrails.

Primary event source: https://agentic-eo.berlin/programme/posters/

# 1. What the room is actually about

| Cluster | Representative Berlin posters | What the room will already understand |
|---|---|---|
| EO agents / assistants | GEODES Assistant; EIS; EOMAS; VISEO; Manteo AI; FlyPix AI | Natural-language interfaces and agent orchestration |
| Agentic data discovery / processing | THEDE; Agentic Ground Segment; Airbus Geo Explore | Agents selecting data, APIs and workflows |
| Agentic decision workflows | Disaster resilience; irrigation; multi-hazard triage; natural-capital risk | End-to-end application agents |
| Trust / validation / evaluation | Beyond Task Success; GeoGuard; CARE/NASA; Provenance-First Composition; SeismicAgent | Reliability is becoming a first-class problem |
| Foundation models / embeddings | Spheer FM; TerraMind/THOR; learned satellite embeddings; Aperture | Representation quality and semantic grounding |
| Multi-agent / operational systems | Ground-segment orchestration; constellation orchestration; space-ground-cloud continuum | Agent-to-agent and agent-to-system coordination |
| EO scientific analysis | canopy height, air quality, soil mapping, hyperspectral compression | Agents attached to serious EO science |

**Implication:** EMEM cannot differentiate by saying 'we make EO agents trustworthy', 'we provide provenance', or 'we provide EO data to agents'. Those ideas are already represented in the room.

The distinctive object should instead be:

> **A machine-verifiable reference to a physical-world observation that can be handed between independent agents without handing over the sender's context or trusting its prose.**

# 2. The strongest overlaps

## GeoGuard / validation

GeoGuard is explicitly an 'Agentic Guardrails and Validation Framework for Geospatial AI'. This creates a direct perceptual collision if EMEM leads with 'verification'.

Do not position EMEM as another guardrail system.

Distinction:
- **Guardrail:** evaluates or controls an agent's behavior.
- **EMEM:** gives the agent an externally resolvable object whose identity and provenance can be checked.
- A guardrail can consume EMEM evidence.
- EMEM does not decide whether an action is permissible.

Recommended line:
'GUARDRAIL = decides whether an action may proceed'
'EMEM = identifies and verifies the evidence the action cites'

## Provenance-First Geospatial Composition

This is the most conceptually dangerous overlap. A provenance-first system can also make geospatial computation traceable and trust-bearing.

If EMEM says only 'we preserve provenance', the novelty becomes difficult to distinguish.

The poster must demonstrate the **inter-agent boundary**:

'Agent A → emem token → Agent B'

rather than merely:

'pipeline → provenance graph → audit trail'

## THEDE

THEDE already addresses LLM-mediated discovery and delivery of heterogeneous EO/environmental data and thematic datacubes.

Therefore 'agents receive EO data as model-readable objects' is not sufficient novelty.

The stronger contrast is:
- **THEDE:** what data should I retrieve?
- **EMEM:** which exact physical-world state did the previous agent cite?

These can be complementary.

## Foundation-model / embedding work

The accepted title says 'over Foundation-Model Embeddings', but the poster must give embeddings a scientific role:

'EO scene → foundation encoder/version → embedding → typed observation → content identity → agent handoff'

Then state exactly what EMEM adds: persistence, identity, provenance, temporal/spatial binding and inter-agent reference.

# 3. Biggest scientific weakness in the current poster

The current board is technically impressive but too much of its evidence is about proving that EMEM itself is internally consistent.

A skeptical ESA researcher can ask:

> 'Fine. The hash verifies. Why does an agent actually become better or safer because of it?'

The poster needs to invert its evidence hierarchy.

**Current emphasis**
1. cryptographic mechanism
2. detailed trace
3. implementation behavior
4. agent experiment

**Better emphasis**
1. failure mode in agent reasoning
2. controlled intervention
3. measured benefit of the token
4. mechanism explaining why
5. cryptographic proof as enabling infrastructure

The cryptography should establish that the object is checkable. The experiment should establish that the object changes agent behavior.

# 4. Upstream correctness is the largest attack surface

The repository reports that **162/200 sampled pre-fix Sentinel-2 records (81%) carried the neighbouring pixel's DN** because of the rounding/floor bug.

Scientifically this is valuable evidence. Presentation-wise it is potentially devastating.

A skeptical reader can interpret it as:

> 'The system claiming to make observations verifiable was itself signing incorrect observations.'

The answer is technically sound: signatures preserve what was signed and make the error reproducible. But the distinction must become visually explicit:

**Cryptographic integrity ≠ measurement correctness ≠ upstream data correctness ≠ semantic/entity correctness.**

Show four failure surfaces:
1. source data
2. extraction / derivation
3. identity / serialization
4. agent interpretation

EMEM directly strengthens #3 and provenance aspects of #2. It does not automatically solve #1 or #4.

# 5. Highest-value protocol upgrade

A derived physical-world claim should bind:

'source artifact identity'
+ 'exact byte/range or pixel reference'
+ 'coordinate transform'
+ 'derivation code/version'
+ 'parameters'
+ 'model/version if applicable'
+ 'output'
+ 'uncertainty'
+ 'attester'

The current demonstration notes that the upstream Planetary Computer file lacks a checksum.

The stronger invariant is:

> **A derived physical-world claim should be traceable not merely to a URL, but to an immutable upstream artifact identity and an exact extraction/derivation recipe.**

If an upstream source cannot provide a cryptographic identity, mark that edge as **location-only / upstream identity unverified** instead of implying full-chain verification.

# 6. Entity identity remains unresolved

The repository correctly notes that the Maasvlakte entity referent is not caught by byte-level drift detection.

A token can preserve a value without proving it refers to the same physical entity.

For EO agents, distinguish:
- byte identity
- spatiotemporal identity
- entity identity
- semantic identity

A research direction should formalize entity identity using geometry, temporal validity, source identifier and an explicit identity policy.

Do not imply full physical-world referential certainty.

# 7. Current agent experiment is too small for the headline

The current experiments are useful controlled demonstrations, but sample sizes such as 10/10 and 5/5 are not broad evidence that EMEM universally improves agent reliability.

Upgrade the experiment matrix:

| Dimension | Recommended levels |
|---|---|
| Models | 4–6 materially different models |
| Agent runtimes | MCP + direct API/tool + one framework |
| Evidence | raw value / prose / RAG / token |
| Tasks | retrieval / comparison / temporal change / threshold decision / citation |
| Perturbations | rounding / stale value / wrong cell / wrong date / wrong entity / altered bytes |
| Outcomes | accuracy / refusal / verification completion / false acceptance |
| Replicates | ≥30 per experimental cell where feasible |

The key metric should be:

> **False acceptance rate of altered or misbound evidence.**

That aligns directly with the protocol's actual promise.

# 8. Add an ablation

The current story bundles content addressing, spatial binding, signatures, receipts, logs, provenance and tokenization.

Run:
1. plain prose
2. opaque ID
3. content hash only
4. content hash + spatial binding
5. signed token
6. signed token + receipt
7. signed token + upstream provenance
8. full EMEM

Then run the same adversarial handoff suite.

This turns the work from a systems demonstration into a mechanism study.

# 9. Make adversarial mutation testing the central experiment

Take valid EO observations and generate controlled mutations:
- value ±1 ULP
- rounded value
- wrong cell
- adjacent cell
- wrong date
- stale observation
- swapped band
- changed unit
- changed source
- altered derivation parameter
- altered model checkpoint
- altered embedding
- same value, different entity
- modified token payload
- valid old token presented as current

Measure:
- detection rate
- false acceptance rate
- false refusal rate
- latency
- token overhead

This is probably the single highest-value experiment before Berlin.

# 10. Reframe token overhead correctly

The repository correctly acknowledges that an individual token can cost more LLM tokens than the value it names.

Do not sell this as compression.

The real benefit is **reference stability**, not payload compression.

Measure:
- token bytes
- tokenizer tokens
- payload bytes
- verification latency
- repeated reuse count

The interesting systems question is whether repeated reuse amortizes the reference cost.

# 11. The poster needs a counterfactual

Make this visually central:

### WITHOUT EMEM
'0.470899 → approximately 0.47 → Agent B → threshold decision'

### WITH EMEM
'0.470899 → emem:fact... → resolve → hash → verify → decision'

Then mutate the value to '0.47' and show that the token path detects the mismatch while prose cannot.

# 12. Recommended central figure

## The evidence handoff test

| | A sends | B receives | B outcome |
|---|---|---|---|
| Prose | 'NDVI ≈ 0.47' | text | cannot detect rounding |
| RAG | retrieved value | retrieved text | depends on retrieval/version |
| Hash | CID | bytes | integrity check |
| **EMEM** | signed spatial-temporal token | exact record + receipt | integrity + binding + provenance checks |

Below it, inject six adversarial mutations and report acceptance/rejection.

# 13. What to remove or shrink

The current board is too close to a mini-paper.

Shrink:
- full CBOR formalism
- complete Merkle formulas
- all 15-link trace details
- internal commit hashes in the title band
- long source caveats
- multiple operational command examples
- implementation minutiae that do not change the scientific conclusion

Keep one cryptographic invariant:
'bytes → BLAKE3 → CID'

Keep one verification invariant:
'resolve → re-hash → compare'

Everything else belongs behind the QR.

# 14. What to make much larger

Prioritize four things:

### 1. The failure
**Agents can agree on the same paraphrase and still make the same wrong decision.**

### 2. The intervention
**Pass the evidence reference, not the paraphrase.**

### 3. The result
A controlled mutation table showing acceptance/rejection.

### 4. The mechanism
'observation → content identity → spatial/time binding → signed receipt → independent verification'

# 15. Strongest defensible thesis

> **Agents should hand over evidence references, not paraphrases of evidence.**

Supporting line:

> **emem makes a physical-world observation externally addressable, content-identifiable and independently checkable across agent handoffs.**

This avoids implying that signatures establish scientific truth.

# 16. What EMEM should claim at Berlin

### Strong claims supported by the current direction
- Exact byte identity can be checked independently.
- Spatial binding can detect a token/cell mismatch.
- Signed receipts provide cryptographically checkable server responses.
- Historical records remain identifiable after later corrections.
- Agents can exchange references instead of copying the cited value.
- Controlled perturbations can be detected when they violate token binding.
- The mechanism can sit beneath agent frameworks rather than replacing them.

### Claims that should remain explicitly open
- scientific truth of the upstream measurement
- correctness of extraction algorithms
- entity identity
- causal correctness
- model correctness
- universal improvement across agents
- resistance to malicious signing keys
- full upstream provenance where source artifacts are not cryptographically identified

# 17. Recommended Berlin positioning

Do not compete on:
- 'We built an EO agent.'
- 'We built a guardrail.'
- 'We built an EO RAG system.'
- 'We built another geospatial foundation model.'

Instead:

> **'We are proposing a memory/reference primitive underneath all of them.'**

Architecture:

'EO sources'
↓
'EO models / RAG / openEO / agents'
↓
**EMEM evidence layer**
↓
'agents / guardrails / scientific workflows / audit'

This is the most defensible architectural slot from the current evidence.

# 18. Upgrade order

## P0 — before printing
1. Replace the architecture-heavy opening with the evidence-handoff experiment.
2. Make integrity-vs-truth explicit.
3. State upstream provenance limitations.
4. State entity-identity limitations.
5. Reduce implementation detail by roughly 40%.
6. Make measured agent results visually dominant.
7. Give every numerical result an explicit n, task definition and baseline.

## P1 — strongest scientific upgrade
8. Run the adversarial mutation suite.
9. Add ablations.
10. Add multiple models.
11. Add multiple agent runtimes.
12. Report false-acceptance and false-rejection rates.
13. Add confidence intervals.

## P2 — protocol upgrade
14. Bind upstream artifact hashes/ranges wherever available.
15. Add explicit provenance-confidence states.
16. Formalize entity identity.
17. Separate observation integrity, derivation integrity and semantic identity.
18. Version the verification policy.

## P3 — ecosystem positioning
19. Show EMEM underneath RAG, GeoGuard-like validation and EO workflow agents.
20. Demonstrate one cross-runtime handoff live.
21. Make the QR open directly to a reproducible mutation test rather than only the homepage.

# 19. Bottom line

The current repository is unusually rigorous about its own weaknesses, which is a strength. It has also become too much of a forensic audit of implementation details.

Today the poster demonstrates:

> **'We built a sophisticated, inspectable content-addressed evidence system and independently checked many of its invariants.'**

It needs to demonstrate more directly:

> **'When evidence is handed between agents, this representation prevents specific classes of errors that prose, ordinary retrieval and unverified structured data do not prevent.'**

That is the upgrade that most directly turns EMEM from an interesting infrastructure implementation into a research contribution relevant to the workshop's central reliability question.

## Sources consulted

- Official Berlin workshop poster programme: https://agentic-eo.berlin/programme/posters/
- Official Berlin workshop schedule: https://agentic-eo.berlin/programme/schedule/
- TheDe / EGU26 abstract: https://meetingorganizer.copernicus.org/EGU26/EGU26-5722.html
- TheDe project background: https://www.sistema.at/thede-kick-off/
- *Towards LLM Agents for Earth Observation*, arXiv:2504.12110
- Current EMEM poster source and research ledger in this repository
