# Addendum 2 (EXPLORATORY): Qwen2.5-7B-Instruct as a second open-weight agent B

Written: 2026-09-30T11:00:58Z. This was written after we saw the first 4 Qwen-3B trials and all 30 haiku trials, and before any 7B trial.

What we saw: in the first trial of each arm (T0, P0, R0, F0), Qwen2.5-3B answered IRRIGATE while itself stating NDVI 0.4709 or 0.4708994708994709.
That is a rule-application (numeric comparison) error, not a transmission error. In F0 it removed the cell from the forged token and resolved
the bare cid. The server answered with a degraded 200, cell_matches=false (by design: emem-api-rest/src/lib.rs:33401,33407), and the model acted on it.

To separate transmission fidelity from rule application, we run Qwen2.5-7B-Instruct Q4_K_M (official Qwen GGUF, split in 2 files) under the identical harness,
template, trimming and seed scheme. Plan: T10, P10, F5, R5. All results are labelled EXPLORATORY and are not part of the pre-registered primary.
The pre-registered primary (Qwen-3B n=20/20/5 and haiku n=10/10/5) is unchanged. We also report, for every B model, the decision-consistency
metric "DECISION equals the rule applied to B's own stated NDVI", labelled EXPLORATORY.
