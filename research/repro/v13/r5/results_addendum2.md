# R5 addendum 2 results: a matched conventional receiver

Run on 4 Oct 2026 under `prereg_addendum2.md` (BLAKE3 f7769af0…). The addendum was committed and pushed in 0cf0424
(13:44:26 UTC), before any computation on a corrupted item (Part A, 13:44:32 UTC) and before the first agent trial
(Part S, 13:46:35 UTC). Neither part made a paid API call: Part A needs no model, and Part S ran as in-session
subagents. The one paid test call made before the addendum carried no item; A2.0 discloses it.

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

The controls G0 and G0-B were accepted by each receiver; A2.3 requires this of B+ and B++.

B+ accepts eight corrupted handoffs that its checks cannot contradict. Six are records a forger re-encoded and
re-hashed after changing the cell (M9), the date (M10), the scene id (M11, M23), the BOA offset with the value
recomputed (M12) or the unit (M18). M16 is a second version that a trusted key signed and the log never received. M2-B
is A's misstated elevation (916 for the signed 918.0 m). Binding passes because each record agrees with the question.
Recompute passes because each value follows from its own DNs and offset, or has no recipe. The source re-read passes
M10, M12 and M16, whose DNs are the genuine S2A pixel, and has no committed window for the other cell (M9), the S2B scene
(M11, M23) or the elevations (M18, M2-B).

B++'s checks refuse five of the eight: M10 and M16 on the scene date, M9 on the tile band, M12 on the offset, M18 on the
unit. Of the three left, a receiver with its own access to the same-day S2B scene would catch M11, whose DNs are the S2A
pixel, and one with the DEM would catch M2-B. M23 carries the S2B scene's own pixel and value, so a re-read passes it;
the signature is what catches it.

emem's verifier refuses seven of the eight: six at the signature check and M16 at the log check. Its hash check refuses
none of them, because a forger re-hashes. On M2-B the reference resolves to the signed record, so the receiver uses
918.0 m, not A's 916. A signed JSON record would also get the six signature refusals; the log and the resolution of the
reference to signed bytes account for the other two.

B+ and E+ share the question binding, the four checks and the source windows. They differ in the content address, the
signature and the log, and over these 23 items that difference is 8 corrupted handoffs accepted against 0 (3 against 0
for the hardened receiver). Part A has no agent in it; Part S adds agents, as an exploratory run.

## Part S: Haiku agents through in-session subagents (exploratory)

53 trials, one per arm and item (25 B+, 28 E), in-session Explore subagents with claude-haiku-4-5-20251001, 4 Oct 2026
13:46 to 16:24 UTC. Output `out/addendum2_s.json`; per-trial transcript facts in `addendum2/raw_s/`; tool calls in
`addendum2/calls_s.jsonl`.

Infra: 12 trials stopped on an account usage limit (HTTP 429, "session limit"), three at 13:51:07 to 13:51:09 UTC and
nine at 13:52:28 UTC. As A2.4 provides,
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

In B+, the agents acted on each of the 8 items the deterministic receiver accepts and declined each of the 15 it
refuses: they followed the verifier's verdict. On M18 the agent
noticed the unit "ft" and converted it (918 ft, about 280 m, INCONSISTENT); that still acts on the relabelled record,
whose pre-registered correct output is DECLINE. The E arm reproduces the headless haiku E result (0 of 25 against 0 of
150, verifier called in each trial), so the subagent harness did not visibly change behaviour on that arm.

## Limits

- One trial per item and one model in Part S; it shows agreement with the deterministic receiver, not a rate.
- Two constructed tasks, 23 items, two committed source windows. With its own access to the same-day S2B scene and the
  DEM, a conventional receiver would also catch M11 and M2-B; M23 would still pass.
- The subagent harness differs from the headless one in four ways (A2.4): the R5 system prompt sits in the task message,
  tools are called through Bash, the subagent had other tools it was told not to use (the audit found none used), and
  the workspace's connector text in its context names emem.dev as a signing service, which bears on the E arm.
- B++'s four checks were fixed in the addendum before the computation; other consistency checks are possible.

## Corrections and notes after the run

1. A2.0 item 1 says the trial tool was called once per arm on the controls' trial ids before the addendum. It was called
   five times: on the ids of B+ G0, E G0 and B+ G0-B, plus two error paths (a wrong tool name on the B+ G0 id and an
   unknown trial id). The call log was deleted before the first trial; no corrupted item was called.
2. A2.4 and A2.5 ask that Part S be labelled exploratory wherever it is reported. The board's first print of it (50ddf41)
   did not say so, and its count lacked a unit; the next print says "in an exploratory run, one trial each" and
   "8 of 23 corruptions".
3. A review of the code after the run found weaknesses that the recorded data never triggered:
   - `score_s.py`'s `ALLOWED` pattern is looser than the audit rule in A2.4: a second command after a newline, a
     substitution inside double quotes, a glob or a trailing comment would match. `addendum2/audit_strict.py` re-checks
     the 57 recorded tool calls, failed attempts included, against a strict one-line form with the trial's own id and
     the arm's own tool: 57 of 57 pass. `score_s.py` is unchanged; its hash is bound by the addendum.
   - `score_s.tool_facts` would count a call that names another trial or uses the other arm's tool; none occurred. The
     audit takes the last assistant text as the report when no handback exists; the 53 scored attempts each ended in
     a handback.
   - `verifier_conv.py` accepts a static-band observation whose tslot is missing or the string "0", which verifier.py
     refuses and A2.2 rules out. `items.observation_json` always writes an integer tslot that agrees with the date.
   - `matched.py` reports the controls accepted and leaves A2.3's broken-receiver rule to the reader; both receivers
     accepted both controls.
   - B++'s tile-band check uses the nominal 8 degree MGRS bands, so a genuine field near a band edge could be refused;
     Keylong lies 0.57 degrees inside band S.

## Files

| file | content |
|---|---|
| `prereg_addendum2.md` | the pre-registration (hash in `prereg_hash.txt`) |
| `addendum2/verifier_conv.py`, `addendum2/verifier_hard.py` | the B+ and B++ receivers |
| `addendum2/matched.py` | Part A; writes `out/addendum2_ceiling.json` |
| `addendum2/plan_s.py`, `addendum2/plan_s.json`, `addendum2/prompts_s/` | Part S plan and the exact prompts |
| `addendum2/rtool.py`, `addendum2/calls_s.jsonl` | the trial tool and its call log |
| `addendum2/score_s.py`, `addendum2/raw_s/`, `out/addendum2_s.json` | collection, audit, scoring and the scored trials |
| `addendum2/audit_strict.py` | the stricter re-audit of the recorded tool calls (added after the run) |
