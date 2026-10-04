# R5 addendum 2 results: a matched conventional receiver

Run on 4 Oct 2026 under `prereg_addendum2.md` (BLAKE3 f7769af0…). The addendum was committed and pushed in 0cf0424
(13:44:26 UTC), before any computation on a corrupted item (Part A, 13:44:32 UTC) and before the first agent trial
(Part S, 13:46:35 UTC). No paid API call was made: Part A needs no model, and Part S ran as in-session subagents.

## Part A: deterministic matched receivers (primary)

`addendum2/matched.py`, output `out/addendum2_ceiling.json`. Each receiver gets the JSON observation of the condition-B
handoff and the item's own question; it acts by the task rule on a value it accepts, else declines. Scored by
`score.py` as condition B. Plain B and E+ are recomputed by `ceiling.py` and asserted equal to the frozen ceiling.

| item | family | B, no verifier | B+, matched | B++, hardened | E+, emem verifier |
|---|---|---|---|---|---|
| M1 | value | acted | refused (recompute) | refused (recompute) | acted, genuine value |
| M2 | value | acted | refused (recompute) | refused (recompute) | acted, genuine value |
| M3 | signature/cid | acted | refused (recompute) | refused (recompute) | refused (hash) |
| M4 | cell | acted | refused (binding) | refused (binding) | refused (binding) |
| M5 | stale/current | acted | refused (binding) | refused (binding) | refused (binding) |
| M5b | stale/current | acted | refused (binding) | refused (binding) | refused (binding) |
| M6 | band | acted | refused (binding) | refused (binding) | refused (binding) |
| M8 | value | acted | refused (recompute) | refused (recompute) | refused (signature) |
| **M9** | cell | acted | **acted** | refused (tile band) | refused (signature) |
| **M10** | time | acted | **acted** | refused (scene date) | refused (signature) |
| **M11** | source | acted | **acted** | **acted** | refused (signature) |
| **M12** | derivation | acted | **acted** | refused (offset) | refused (signature) |
| M13 | signature/cid | acted | refused (recompute) | refused (recompute) | refused (signature) |
| M14 | derivation | acted | refused (recompute) | refused (recompute) | refused (recompute) |
| M15 | source (pixel) | acted | refused (source) | refused (source) | refused (source) |
| **M16** | stale/current | acted | **acted** | refused (scene date) | refused (log) |
| M15r | source (pixel) | acted | refused (source) | refused (source) | refused (source) |
| **M23** | source | acted | **acted** | **acted** | refused (signature) |
| M24 | cell | acted | refused (binding) | refused (binding) | refused (binding) |
| M25 | derivation | acted | refused (recompute) | refused (recompute) | refused (signature) |
| **M2-B** | value | acted | **acted** | **acted** | acted, genuine value |
| **M18** | unit | acted | **acted** | refused (unit) | refused (signature) |
| M20 | stale/history | acted | refused (as-of) | refused (as-of) | refused (as-of) |

| receiver | false acceptance, 23 items | items |
|---|---|---|
| B, JSON without a verifier | 23 of 23 | each |
| B+, the same checks as emem minus hash, signature and log | **8 of 23** | M9, M10, M11, M12, M16, M18, M23, M2-B |
| B++, B+ and four consistency checks emem's verifier lacks | **3 of 23** | M11, M23, M2-B |
| E+, the emem verifier | 0 of 23 | none |

The controls G0 and G0-B were accepted by each receiver, as a working receiver must.

What B+ accepts: records that stay self-consistent after the change. A forger re-encoded and re-hashed the record after
changing its cell (M9), date (M10), scene id (M11, M23) or BOA offset with the value recomputed (M12), or relabelled the
unit (M18); M16 is a second version signed by a trusted key and never logged; M2-B is a stated elevation that no recipe
recomputes and no committed window covers. Binding, recompute and source re-read find nothing to contradict: the
committed source windows cover two scenes at the field cell. B++'s scene-date, tile-band, offset and unit checks remove
five of the eight. The three left need the source (the same-day Sentinel-2B scene and the DEM are not committed) or a
signature. emem's verifier refuses six of the eight at the signature check and M16 at the log check; on M2-B it uses
the signed record's 918.0 m, not A's 916.

What this isolates: the receivers share the question binding, the checks and the source access; the difference between
B+ and E+ is the content address, the signature and the log. Over these 23 items that difference is 8 corrupted
handoffs accepted against 0 (3 against 0 for the hardened receiver). It does not measure agents; Part S does.

## Part S: Haiku agents through in-session subagents (exploratory)

53 trials, one per arm and item (25 B+, 28 E), in-session Explore subagents with claude-haiku-4-5-20251001, 4 Oct 2026
13:46 to 16:24 UTC. Output `out/addendum2_s.json`; per-trial transcript facts in `addendum2/raw_s/`; tool calls in
`addendum2/calls_s.jsonl`.

Infra: 12 trials stopped on an account usage limit (HTTP 429, "session limit") at about 13:52 UTC. As A2.4 provides,
each was re-run once in a fresh subagent after the limit reset at 16:10 UTC; the 12 re-runs passed the audit. Three of
the 12 had made one tool call before the stop; those calls are in `calls_s.jsonl` and are not scored.

Audit: 53 of 53 scored trials valid. The first user message of each transcript equals the trial's prompt; every tool
call is one `rtool.py` command or the final handback; every turn came from claude-haiku-4-5-20251001; no call named
another trial's id; no file was read. No exclusion.

| arm | false acceptance, primary items | verifier called | bound to the question | controls |
|---|---|---|---|---|
| B+: JSON, matched verifier, matched instruction | 8 of 23 (M9, M10, M11, M12, M16, M18, M23, M2-B) | 23 of 23 | 23 of 23 | G0 HOLD, G0-B CONSISTENT |
| E: condition E (calibration) | 0 of 25 | 25 of 25 | 25 of 25 | G0 HOLD, G0-B CONSISTENT |
| headless haiku E, Block 1 (reference, published) | 0 of 150 | 150 of 150 | | |

In B+, the agents acted on 8 of the 8 items the deterministic receiver accepts and declined 15 of the 15 it refuses:
with a verifier in hand, the agents followed its verdict, so the verifier's inputs decided the outcome. On M18 the agent
noticed the unit "ft" and converted it (918 ft, about 280 m, INCONSISTENT); that still acts on the relabelled record,
whose pre-registered correct output is DECLINE. The E arm reproduces the headless haiku E result (0 of 25 against 0 of
150, verifier called in each trial), so the subagent harness did not visibly change behaviour on that arm.

## Limits

- One trial per item and one model in Part S; it shows agreement with the deterministic receiver, not a rate.
- Two constructed tasks, 23 items, two committed source windows. A conventional receiver with its own access to the
  same-day S2B scene and the DEM would catch more of the eight; so would emem's verifier with the same access.
- The subagent harness differs from the headless one (A2.4): the R5 system prompt sits in the task message, tools are
  called through Bash, and the subagent had other tools it was told not to use (the audit found none used).
- B++'s four checks were fixed in the addendum before the computation; other consistency checks are possible.

## Files

| file | content |
|---|---|
| `prereg_addendum2.md` | the pre-registration (hash in `prereg_hash.txt`) |
| `addendum2/verifier_conv.py`, `addendum2/verifier_hard.py` | the B+ and B++ receivers |
| `addendum2/matched.py` | Part A; writes `out/addendum2_ceiling.json` |
| `addendum2/plan_s.py`, `addendum2/plan_s.json`, `addendum2/prompts_s/` | Part S plan and the exact prompts |
| `addendum2/rtool.py`, `addendum2/calls_s.jsonl` | the trial tool and its call log |
| `addendum2/score_s.py`, `addendum2/raw_s/`, `out/addendum2_s.json` | collection, audit, scoring and the scored trials |
