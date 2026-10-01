# Addendum 1 to the pre-registration (written after agent A finished and before any agent-B trial)

Written: 2026-09-30T10:51Z (UTC; the first version, BLAKE3 db0ac6d9…, was logged at 10:51:38Z. This line alone was corrected at 10:58Z because it had a wrong time). The primary analysis in prereg.md is unchanged.

## What we already knew when this was written
Agent A has finished (n=10). In all 10 runs, A's HANDOFF_TOKEN equals the hero token. In all 10 runs, A's HANDOFF_PROSE contains the full value
`0.4708994708994709`, which is 16 significant digits. So the pre-registered P arm gives B the full value, and the stated expectation
("P will score as well as T, the primary test will be null") is the likely outcome. We keep and report the primary test as registered.

## Added EXPLORATORY arm (not pre-registered, labelled as such everywhere)
- **R (rounded-prose positive control)**: A's prose for the paired run, with the value string replaced by `0.47`. This mimics the 2-decimal
  paraphrase that the earlier drift experiment observed. Its purpose is to show that the harness and the rule can detect a precision loss
  when one exists. It is **not** evidence about how often natural prose rounds. For this model, natural prose did not round in 10/10 runs.
  n = 10 for B-open and n = 5 for B-claude. The same template, seeds scheme and scoring are used.
- Also recorded, as an exploratory observation: whether the non-value fields of A's prose (date, tile) match the signed record. Run a03 wrote "25 September **2025**",
  but the signed scene is 2026-09-25.

## Seeds (B-open)
T trial i uses seed 1000+i, P trial i uses 2000+i, F trial i uses 3000+i, R trial i uses 4000+i. For tool turn k, the seed is increased by k.
