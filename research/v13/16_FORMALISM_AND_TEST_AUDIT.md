# v13.4: restore the formal model without losing the story

Requested 2 October 2026: restore drift and memory formulas, inspect the real GitHub tests, find earlier contributions that disappeared, and make the next poster complete and coherent.

## What returned, and why

| Earlier contribution | v13.3 omission | v13.4 treatment | Evidence and boundary |
|---|---|---|---|
| Drift decomposition | Replaced by a taxonomy of checks | Restored beside a plain-language definition of every term | `docs/whitepaper-v2.md`, pinned below. Conceptual attribution model; no numeric causal split is claimed. |
| Drift-anchor score | Hidden behind the execution extension | Both equations, threshold strip and test-pinned points on the face | `crates/emem-trace/src/drift.rs`; archived passing `pinned_points`, `missing_sigma_is_strict`, `verdict_thresholds`. Disagreement score, not a probability or attribution. |
| Memory model and relations | Reduced to two identity cards | `M = (O*, E*)`, temporal relation tuple, record CID equation | `docs/model.md`; the poster does not copy its obsolete individual-fact signature formula. Actual record and batch attestation retain their separate roles. |
| Two temporal clocks | Dense mixed Bengaluru/Keylong timeline | Explicit recall notation plus one worked signing-time query | `recall.rs`, `bi_temporal.rs`, retained Bengaluru history. The implementation resolves transaction-time versions and then valid-time selection; one unqualified argmax is not an adequate model of every mode. |
| Foundation-model outputs | Title retained, actual vectors removed | Prithvi and TESSERA vector stripes drawn from retained values | Prithvi has 1,024 values and a checkpoint digest; TESSERA 128 values and a product-year path. Encoder deployment is retired. No claim that every model record pins a checkpoint. |
| Source recipe | Described only through the experiment | Explicit NDVI formula with the recorded product offset | `pixel_windows.json`, `mutation_suite.py`, the actual Keylong record. Offset −1000 applies to the cited product; not a universal sensor rule. |
| Real implementation tests | Almost invisible to a reader | Threshold evidence on the face; pinned test sources, raw fresh results and archived results in Reproduce | Fresh Python tests and archived Rust runs have separate dates, commits and scopes. |
| Next work | Generic concluding promise | Controlled attribution experiments and separately operated agent hosts | Specific open questions, not presented as completed capability. Device-to-anchor wiring stays explicitly open beside the score. |

## Tests used as evidence

Source repository: https://github.com/Vortx-AI/emem at `8e9b401cecae7ab9944d403a2d7840952c6586a6`.
Every inspected source file has a SHA-256 and immutable GitHub URL in `evidence/formalism/sources.json`. The original files are copied beneath `evidence/formalism/source/`; no implementation code was changed.

Fresh run, 2 October 2026: **20 passed, 0 failed, 0 skipped**.

```
PYTHONPATH=sdks/emem-py/src:bench GITHUB_ACTIONS=true python -m pytest \
  sdks/emem-py/tests/test_verify_offline.py bench/test_canonical.py -v \
  --junitxml=offline_tests.xml
```

Run from the pinned upstream checkout with its documented Python dependencies and pytest/cbor2 installed. Results: `evidence/formalism/offline_tests.txt`, `.xml`, and `test_results.json`.

The SDK verifier checks agreement with signer vectors, accepts a genuine receipt, rejects six specific forgeries (CID, request id, clock, primitive, Merkle root, stripped proof), and makes refusal unambiguous. The benchmark encoder tests canonical numeric forms, booleans, key order, unsupported types and CID stability/change. These are existing repository tests, not newly invented tests that mirror this poster.

Archived Rust evidence, 30 September 2026, emem `04b40c56c97d1c2809ca05003dc2b7d6de450758`:

- `emem-trace`: 22 passed; one timing test deliberately ignored.
- Filtered storage trace/enrolment tests: 23 passed; 38 unrelated tests excluded.
- Raw retained output: `research/repro/v12/trace/emem_trace_tests.txt`.

Rust is not installed in this workspace. Current drift and bi-temporal test sources were inspected; no fresh Rust execution is claimed. Temporal contracts cover the valid-time bound, signing-time bound, their intersection, empty results, receipt compatibility and candidate filtering.

## Scientific corrections retained

- A fact CID identifies canonical record bytes. It does not by itself establish sensor truth, source-byte integrity or a signature inside the fact.
- The tested record is covered by a batch attestation. The methods explain receipt verification separately.
- In the score, `u` renames the implementation variable `z`, avoiding a collision with the observation `z` in the decomposition. Tension begins at 0.50, contradicted at 0.75. Invalid uncertainty uses exact match.
- The Bengaluru comparison is a provider change under the same lookup cell/band. It is not evidence of ground movement. The signing-time bound selects what memory knew.
- SAT-042 is a reference harness, with no spacecraft enrolled. The gate checks the output value digest; recorded code/model metadata does not become a stronger gate guarantee.
- The main benchmark remains the existing final R5 run, including the Qwen exception and the pre-fix source-read case. No model run or fresh cross-host result was invented for this edition.

## Earlier work deliberately kept in the methods

The full Keylong time series, Rondônia sampling, detailed token grammars, full verification ladder, SAT-042 trace figures, complete mutation matrix evidence, costs, source records and prior-art comparisons remain available. These are supporting depth; copying every chart back onto one A0 sheet would obscure the mechanism. The face now follows a coherent sequence: why values change; what memory stores; what a receiver checks; how the evidence is recovered; what to test next.

The concrete two-process, reference-only handoff remains in the ecosystem evidence and methods. The new vector panel replaces its duplicate diagram in the left column, since the header, spine and ecosystem already explain the handoff.

## Next experiments

1. Introduce controlled scene, pixel and encoder changes; test whether numeric attribution can distinguish their effects.
2. Connect device outputs to independently recalled Earth anchors and evaluate uncertainty calibration, beyond the fixed reference harness.
3. Repeat checked handoffs between separately operated agent hosts, preserving the exact request binding, receipt and source evidence.

These are proposed validations, not promised outcomes. The poster's new Next panel gives the first and third explicitly; the drift caption states the second.
