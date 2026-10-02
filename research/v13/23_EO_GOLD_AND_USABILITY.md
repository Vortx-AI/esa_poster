# v13.8: recovered EO substance and practical use

Reviewed 2 October 2026. This round follows v13.7, which restored the full handoff, token family, Berlin fanout and memory formalism. The aim is to connect those mechanisms to an Earth-observation question without turning archived demonstrations into new scientific validation.

## Recovery decisions

| Source | Useful material | Destination and decision |
|---|---|---|
| v4 `76c61d0`, v5 `f36520b`, v6 `9414dfd`, v7 `aee55fa` | Earth-to-agent lifecycle, field examples, neighbouring infrastructure | Preserve the complete lifecycle. Explain the contribution through a cited observation rather than infrastructure slogans. |
| v11 `aff0c21` and its review | Observation identity, temporal memory, memory operations; implementation caveats | Translate operation names into EO tasks. Keep the exact formalism and its implementation boundary. |
| v12 `57a48a6a350dc61c221f01531c86ca795d82a07a` | Keylong NDVI history, Berlin product stack, Rondônia sampled forest evidence | Restore dated NDVI observations to the A0 face. Add vegetation and forest-product task paths to the community page. Berlin remains the central source-to-record example. |
| v13.2 `2686b27a9947613b72c4690c4dc524839c6fbcd2` | Full handoff and token family; coordinated blue/orange semantics | Retain the v13.7 restorations, their dimensions and colour roles. |
| Earlier eight-answer Keylong diagnostic | Effects of scene, pixel, offset, rounding and record selection | Retain the figure and link it from methods. Give its A0 area to the actual observation history, which supplies the missing EO context. |
| Current emem site and documentation | Observation references, receiver checks, multiple object types and application entry points | Use the task ideas and clearer explanations. Published claims are not substitute measurements. |
| Pinned emem source and existing tests | Exact operation, derivation and temporal behaviour | Keep the implementation boundaries and retained test results; fix the derived-token wording. |
| STAC and openEO primary specifications | Discovery, metadata and interoperable processing | Position EMEM as a complementary record handoff mechanism, without claiming these systems cannot represent observations or provenance. |

## What the restored figure establishes

`poster/figs_v13/f17_ndvi_history.py` reads the committed `research/repro/v12/data/case_keylong_ndvi.json`; it does not query a new time series. It selects 141 distinct records dated in 2025–2026: 87 in 2025 and 54 in 2026; 15 S2A, 61 S2B and 65 S2C. The first retained acquisition is 28 January 2025 and the last is 25 September 2026. The selected record is `oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa`, value `0.4708994708994709`, the same record used in the handoff and source-pixel experiments.

The source was read on 30 September 2026. Original `verified` flags are retained evidence, not a fresh signature-verification run. The chart shows stored observations and time order. Cloud/snow screening, processing harmonisation and a vegetation-trend analysis were not performed. Those limits appear beside the chart and on the linked task page. The data selection, source hash and platform counts are recorded in `evidence/v138/eo_history.json`.

The highlighted observation provides a continuous reading path: an EO history contains a selected value; an agent cites its exact record; a receiver checks the record; source re-reading tests the pixel rule. Record integrity and physical interpretation remain different questions.

## Language and usability

| Protocol term | EO-facing explanation | Boundary retained |
|---|---|---|
| Cell | Location index | It is not the native pixel of all source products. |
| Band | Variable or product field | Typed bands can also contain derived values or model outputs. |
| Fact | Observation record | The name does not establish physical truth. |
| CID | Content address of a specific record | The hash identifies bytes; it does not measure sensor accuracy. |
| Recall / diff | Compare dated observations | State the time bounds and changed provider or processing context. |
| Merge / trace | Assemble evidence | Keep individual citations and lineage. |
| Competing / evolve | Retain conflicting estimates | A shared location does not resolve a scientific disagreement. |
| Ensure / valid | Refresh inputs and inspect validity | Multi-hop planning remains open. |
| Drift | Handoff change, or change between observations | The implemented anchor score measures disagreement, not its physical cause. |

The community page starts with three tasks: vegetation history, forest-product comparison and historical replay. Each links to a short workflow and retained evidence. ChatGPT, Claude, Visual Studio Code, Dify and Salesforce MuleSoft remain the five primary setup cards, with the wider manifest-driven directory below them.

The Rondônia example contains 100 point cells and 600 facts, roughly 740 m between sample nodes. It supports inspection of different products at sampled locations; it is not parcel coverage, an area mean, or a legal-compliance determination. The Bengaluru replay keeps the earlier 918.0 m record distinct from the later 915.07 m provider result; this does not demonstrate ground movement.

## Scientific contribution and the claim boundary

The useful invention to explain is the composition: an agent carries a compact reference to a specific observation, and the next agent can recover that record and apply progressively deeper checks. The paper's controlled handoff experiment and source-pixel tests give this composition evidence. Generic hashing, signatures, temporal storage, lineage and EO workflow execution are established components.

The website's broader statements about regulated deployments, arbitrary real-world guardrails, universal recomputation and very large byte ratios were not promoted to poster measurements. Source-data volume, record size and reference size are different quantities. The website and older documentation also differ on the scope of log proofs and device enrolment; the pinned source and retained test evidence govern this poster.

One concrete wording bug was corrected: the derived-token row previously said “pure ops re-run”. The inspected implementation does not automatically recompute every stored derivation. Verification requires `code_cid` and a supported scalar operation (`delta`, `sum`, `mean`) or a registered algorithm AST. An unverified or failed claim may still be signed/stored without becoming `deterministic_index`. The table now says “pure ops re-runnable”; methods states the conditions. See M5/M6 in `00_v11_review_findings.md` and the pinned implementation.

## Sources and reproducibility

- Pinned source: [Vortx-AI/emem at 8e9b401cecae7ab9944d403a2d7840952c6586a6](https://github.com/Vortx-AI/emem/tree/8e9b401cecae7ab9944d403a2d7840952c6586a6), with retained model excerpts and test results under `evidence/formalism/`.
- [emem homepage](https://emem.dev/), [long version](https://emem.dev/the-long-version), [solutions](https://emem.dev/solutions), [model](https://emem.dev/docs/model.html), [quickstart](https://emem.dev/docs/quickstart.html).
- [STAC specification overview](https://stacspec.org/en/about/stac-spec/), [openEO API](https://api.openeo.org/).
- Retrieval status and content hashes: `evidence/v138/public_source_checks.json`. External pages are mutable; these checks establish retrieval, not experimental validation.
- Figure/claim additions: `12_claims_map_additions_v138.json`.
- Build, interaction checks and publication artifacts: `poster/release_v13.8.json` once built.

This release adds no model trials, new ecological inference, fresh Rust tests or hosted-agent success claims. Existing measurements retain their dates and scopes.

## Issue review

Issue #19 is addressed by the complete latest-as-of formula and its mode limits, the explicit note that temporal storage is established, and the new historical-replay task. The falsifiable handoff implication is recovery of the exact earlier cited record after a provider changes. `research/repro/README.md`, Exhibit A, retains the 29 September replay and re-hash result for the 918.0 m record; `contra_bengaluru.json` retains the attestation history. The current controlled mutation experiment separately includes old/current substitutions (M5 and M16). This release does not label that older replay as a new live experiment.

Other open issues requiring new hosted-agent runs, a broader benchmark, brand assets or an entire media pack remain open. This editorial release does not claim those tasks are complete.
