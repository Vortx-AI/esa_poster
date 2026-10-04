# R5 scoring notes: two scorer weaknesses and one label, found after the run

Written 4 Oct 2026, after a third-party review of main at 4f6277d that re-ran the scoring code on the archived trials.
The published R5 counts use `score.py`, frozen by pre-registration addendum 1 (BLAKE3 f4f22e3b…). It stays unchanged,
so the published method can be re-run as it was. `score_v2.py` is a corrected scorer for sensitivity analysis and for
future runs; `score_sensitivity.py` re-scores every archived trial with both and writes `out/score_sensitivity.json`.

## 1. A VALUE written with an exponent gets the wrong tolerance

`score._matches` takes the tolerance from the decimals a VALUE states and gives a VALUE with an exponent zero decimals,
a tolerance of ±0.5: `_matches("4.709e-1", 0.9)` is true, while `_matches("0.4709", 0.9)`, the same number, is false.
`score_v2.matches` takes the decimals from the mantissa and the exponent ("4.709e-1" states four, like "0.4709").

No archived answer states its VALUE with an exponent (0 of 2,878 re-scored trials), so no published count rests on this
weakness.

## 2. One available value overrides a contradicting VALUE

When a trial offers B one value, `score.score` attributes that value to an actionable decision whatever VALUE B reports.
Probe: M7 in the opaque-id condition, served record seen, "DECISION=IRRIGATE VALUE=0.1" is scored as acting on the
genuine 0.4709 (no false acceptance). This follows the pre-registered attribution rule (prereg section 6); it is a limit
of that rule, not a change to it. `score_v2.score` attributes a numeric VALUE that contradicts every available value
as reported (channel "other"); a contradiction is a difference of at least one unit in the VALUE's own last place, so a
rounding or a truncation (0.4708 for 0.47089…) still counts as the value it rounds.

In the archive, 59 actionable answers state a VALUE that differs from the attributed value at the VALUE's precision; 47
of them contradict it. 39 of the 47 are M18 answers that converted the relabelled 918 ft to about 280 m; 8 are Haiku
answers that reported the threshold 0.4705 or 916.5. Three are controls; the other 44 were already scored as acting on
corrupted evidence. None of the outcomes behind the published counts rests on a contradicted VALUE.

## 3. Re-score with both scorers

`score.py` reproduces the 32 published false-acceptance counts in `results.json` (each Claude model, the three pooled,
and the open model; block 1, primary items). `score_v2.py` changes no trial's false acceptance or outcome: 0 of 2,878,
across the pilot, block 1 and block 2. The published counts, the 0 of 300 result and the 300of300 split are the same
under both scorers. Future runs should use `score_v2.py` or a successor, pre-registered before the trials.

## 4. "Used the genuine record" on the poster

Panel 1's third outcome column said "used the genuine record". `genuine_value_source.py` splits it by `score.py`'s
attribution channel (`out/genuine_value_source.json`, same trials as `out/not_acted_split.json`):

| condition | acted on the genuine value | how B had the value |
|---|---|---|
| JSON | 6 | 6 derived by B from the DNs the handoff carries (M2); no record reaches B |
| opaque id | 46 | 13 derived by B; 27 the value of the record the relay served (no check); 6 the value stated in the handoff (M7) |
| emem reference, instructed | 36 | 36 the value of the emem record, served after every check passed |

Each derived answer's REASON says that B recomputed NDVI from the band values it was given (the reasons are in
`out/genuine_value_source.json`). Only the emem lane retrieves and verifies the record. The column now reads "acted on genuine value" and panel 1's
mechanism line "acts on the genuine value"; the counts are unchanged.

## Files

| file | content |
|---|---|
| `score.py` | the pre-registered scorer, unchanged |
| `score_v2.py` | the corrected scorer (changes 1 and 2 above) |
| `score_sensitivity.py`, `out/score_sensitivity.json` | the probes, the archive counts and the re-score with both scorers |
| `genuine_value_source.py`, `out/genuine_value_source.json` | how B had the genuine value, per condition and item |
