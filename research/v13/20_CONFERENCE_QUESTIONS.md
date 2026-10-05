# Conference questions: EMEM

Evidence checked 5 October 2026. Short answers for the A0 poster, with scope and sources attached.

## What is the contribution?

An observation-sized handoff unit: a lookup identity finds a record, a content address fixes the cited bytes, and the receiver can check binding, attestation and declared computation, then re-read the source pixel the record names. EMEM combines established primitives for agent evidence handoffs. The poster makes no priority claim for hashing, signatures, memory or EO data.

Status: SPEC / MEASURED.

Evidence: [Invention boundary and primitive taxonomy](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/10_ladder_threat_invention.md) · [Controlled handoff results](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v13/r5/results.json).

## Why not STAC?

STAC catalogues spatiotemporal assets. EMEM names the particular observation read from an asset and carries that record between agents. A source asset can still be discovered through STAC. Binding its checksum into the EMEM record is a separate, unfinished improvement.

Status: EXTERNAL / SPEC.

Evidence: [STAC specification](https://stacspec.org/en/about/stac-spec/) · [Record fields and missing upstream hash](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/10_ladder_threat_invention.md).

## Why not openEO or PROV-O?

openEO describes and executes EO processing; PROV-O represents entities, activities and agents in provenance. EMEM adds the addressable observation a receiving agent can recover and check. A process graph or provenance description can supply the derivation context; a complete mapping is not demonstrated here.

Status: EXTERNAL / INFERRED.

Evidence: [openEO API](https://api.openeo.org/) · [W3C PROV-O](https://www.w3.org/TR/prov-o/) · [Layer comparison](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/04_prior_art_and_field.md).

## Why not ordinary RAG?

RAG retrieves context for generation. A retrieved passage can still be paraphrased or used without checking the cited record. EMEM references can be returned by retrieval and then resolved and checked. The poster compares one BM25-based RAG baseline (top 3 of nine passages); it does not claim to outperform every RAG design.

Status: EXTERNAL / MEASURED.

Evidence: [Original RAG paper](https://arxiv.org/abs/2005.11401) · [R5 preregistration and protocol](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v13/r5/prereg.md) · [Results by arm](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v13/r5/results.json).

## Why not C2PA?

C2PA binds provenance assertions to media assets. EMEM addresses an observation record used in an agent handoff and exposes checks on that record. Both depend on trust in signers and source processes. A C2PA manifest linking a rendered map to EMEM facts is a possible composition, not a shipped result.

Status: EXTERNAL / INFERRED.

Evidence: [C2PA technical specification](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) · [Prior-art boundary](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/04_prior_art_and_field.md).

## What does a signature establish?

A successful signature check binds an attestation to the expected public key and signed bytes. In this example the batch attestation covers the record address. The key must be selected by the receiver's trust policy; accepting any key supplied by a sender would not establish the intended source.

Status: SPEC / MEASURED.

Evidence: [Ed25519 specification](https://www.rfc-editor.org/rfc/rfc8032) · [Independent bundle verifier](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v8/verify_bundle.py) · [Offline verification](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/evidence/community/recovery_checks.json).

## What do the checks leave unestablished?

Record identity, declared cell/band/time, attestation, derivation and retained history are checkable at their respective depths. Sensor accuracy, entity identity, physical truth and downstream decision correctness do not follow from those checks. The source re-read can reveal a faithful record of a wrong pixel.

Status: MEASURED / OUT-OF-SCOPE.

Evidence: [Canonical verification ladder](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/10_ladder_threat_invention.md) · [Mutation matrix including wrong-pixel and entity cases](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v11/out/mutation_matrix.json).

## Is the upstream source trusted?

Product quality is inherited from the data provider. The cited NDVI record names source files and read coordinates but does not bind an upstream file hash. Re-reading adds a check against the source available then. A retained witness helps reproducibility; it does not independently validate the sensor.

Status: SPEC / MEASURED.

Evidence: [Source audit and guarantee layers](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/10_ladder_threat_invention.md) · [Saved source windows](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/data/v8/pixel_windows.json).

## Is entity identity solved?

No. A valid observation for one cell can be cited as evidence about the wrong field or entity. The deterministic entity-swap case survives the record checks. The application must establish that the declared cell and time answer the intended real-world question.

Status: OUT-OF-SCOPE / MEASURED.

Evidence: [M17 and the verification boundary](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v11/out/mutation_matrix.json).

## Is this running on a spacecraft?

SAT-042 is a scripted reference harness. Its recorded execution and output checks were exercised; it is not a spacecraft deployment. Hardware enrolment and live device-to-anchor wiring remain future work.

Status: MEASURED / OUT-OF-SCOPE.

Evidence: [Trace truth and scope](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v12/trace/trace_truth.md) · [Code and test audit](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/16_FORMALISM_AND_TEST_AUDIT.md).

## How large is the benchmark, and what does zero mean?

R5 contains 2,794 scored trials. In the primary pooled Claude comparison, prose falsely accepted 254/276 corruptions and the instructed reference accepted 0/300. The latter had one false refusal among 72 genuine controls. Zero observed false accepts is a result in this constructed task; its Wilson upper bound is 1.26%, not universal reliability.

Status: MEASURED.

Evidence: [Counts, exclusions, intervals and decision metrics](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v13/r5/results.json) · [Analysis implementation](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v13/r5/analyze.py).

## How many independent models and operators?

Three Claude variants and one locally run quantized Qwen model were tested. These are four model configurations across two families, not four independent operators. The poster team ran the experiment. Qwen falsely accepted 2/25 corruptions with the instructed reference. Separately operated host-to-host replication remains open.

Status: MEASURED / OUT-OF-SCOPE.

Evidence: [Exact model IDs, repetitions and results](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v13/r5/results.json) · [Client-path study, distinct from host-to-host testing](https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/data/v8/crossruntime_table.json).

## What happens with foundation-model embeddings?

Embeddings are stored as observations with model provenance. The archived Prithvi vector names a checkpoint digest; the TESSERA example names a product year. Those deployed encoders are retired, while their saved records remain addressable. The poster does not demonstrate new embedding generation or numerical separation of all drift causes.

Status: SPEC / MEASURED.

Evidence: [Embedding and drift audit](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/16_FORMALISM_AND_TEST_AUDIT.md) · [Formalism claims and source pointers](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/12_claims_map_additions_formalism.json).

## What if source data changes or becomes unavailable?

Append a new observation and keep the cited record. Recall can bound both observation time and signing time: the Bengaluru example recovers 918.0 m as of 15 June, before a provider later returned 915.07 m. Identity is not availability. Retain bytes, receipts and proofs; source disappearance can prevent a fresh re-read.

Status: SPEC / MEASURED.

Evidence: [Two-clock memory example and tests](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/16_FORMALISM_AND_TEST_AUDIT.md) · [Temporal-memory study](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/16_FORMALISM_AND_TEST_AUDIT.md).

## Can a small drift score explain what changed?

The implemented anchor score normalises disagreement against an anchor and uncertainty: r = |x - a| / (3σ), s = r / (1 + r). It is not a causal attribution or probability. The decomposition into environment, sensor, geolocation and encoder terms (poster panel 3) motivates controlled interventions; fitting that split remains future work.

Status: SPEC / MEASURED / INFERRED.

Evidence: [Implementation and pinned test audit](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/16_FORMALISM_AND_TEST_AUDIT.md) · [Equation claims and source pointers](https://github.com/Vortx-AI/esa_poster/blob/main/research/v13/12_claims_map_additions_formalism.json).
