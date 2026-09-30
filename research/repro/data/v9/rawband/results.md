# v9 raw-band change experiment: results

Pre-registration: prereg.md, blake3 30d8a1a1a8cf9646ada5e49b303b9c9c6f0c4ed6d076e797aa1a5fad6e35d50c, hashed 2026-09-30T13:49:13Z, before trial 1.
Setup: claude-sonnet-5-5 (every run reports only that model in modelUsage), n=10, sequential, `--max-budget-usd 3`, endpoint https://emem.dev/mcp/full (116 tools offered, write tools denied).
Pilots: raw/pilot_core.* (18 tools, none of them a documented raw-band reader) and raw/pilot_full.*. No infra failures, no re-runs.

## Headline
- **The primary outcome could not be tested as designed.** 0/10 runs saw or used the pre-fix neighbour-pixel record (kxjvfwpa, 2993/1972). 1/10 (trial 8) used the containing pixel. 9/10 had **no 23 Sep band values at all** (class c).
- **Cause is an emem tool behaviour, not model behaviour.** `emem_band_raster` with `observed_on=2026-09-23` (and 09-22 or 09-21) always returned the **25 Sep** S2A scene (cloud 10.8 %, tslot 20721). The artifacts were byte-identical to the 25 Sep request (B04 `sipykc4e…`, B08 `mg463c6z…`), and no error was raised. The 23 Sep S2C scene does exist (20.0 % cloud). `emem_cell_scene_rgb` found it in 7 runs. `emem_band_cube` refused both dates ("2 requested date(s) resolved to only 1 distinct scene(s)") in 5 runs.
- Only trial 8 got around this. It called `emem_recall`, `emem_backfill` and `emem_trajectory`, which gave post-fix facts (reader=cog-pixel-floor@2): 23 Sep B04 0.0901 / B08 0.2605 (DN 1901/3605, the containing pixel) and 25 Sep 0.0900/0.2502. That makes NDVI 0.486 to 0.471, Δ −0.015, "no material change", which matches the reference.
- **CHANGE lines:** 6 × "no material change" and 4 × "undetermined/indeterminate". The 4 are outside the allowed set, a format violation that is honest. Of the 6, **5 said in their own text that the verdict was a placeholder, not a measurement** (trials 1, 5, 6, 9, 10). Only trial 8's verdict is backed by two-date evidence. Scored on the CHANGE line alone, 6/10 "match" the truth, but only 1/10 is a supported correct verdict. 0/10 said greener, and 0/10 said browner.
- **Methods:** every run stated the same method: B04 and B08, NDVI = (B08−B04)/(B08+B04), date difference, with small variants (single pixel vs window mean, offset handling, one run naming B11 as a cross-check). That is **1 distinct band set/formula**. It was actually computed across two dates in 1 run.
- **Numbers-backed:** 184/193 numbers in the final answers (95.3 %) match tool-result text directly or through a simple computation, by the automated pre-registered matcher. All 193 are covered once the prompt dates it missed are excluded ("23 versus 25", "23–25"). The matcher is permissive: small integers such as 2, 16 and 32 almost always find a match. On manual review every data-bearing value (DNs, reflectances, NDVIs, deltas, cloud %) traces to tool results. The only numbers taken from outside knowledge are a 0.05 threshold (trial 3) and a "~5-day revisit" (trials 5 and 10). Trial 10's prose says reflectance = (value − 1000)/10000, but the values it used are value/10000, which is correct because the anchors were already offset-corrected. The prose formula is wrong; the numbers are not.
- **Flags:** SCL was mentioned by 0/10, the −1000 offset by 6/10, and the pixel-indexing issue by 0/10. None of the runs could have seen the pre-fix record, so this last figure says nothing about whether agents detect it. Post hoc: 9/10 noticed that both dates were the same scene, but 3/10 (trials 5, 7, 10) wrongly suggested or claimed that no 23 Sep acquisition existed ("tile has no acquisition on 23 Sep", "probably wasn't imaged that day").
- **Token integrity:** there were 30 distinct cited CIDs: 4 per-cell `emem:fact` CIDs and 26 raster derivation-record CIDs taken from `emem:raster:` tokens. Each was fetched with GET /v1/facts/<cid> (Accept: application/cbor). **30/30** matched base32-nopad-lower(blake3(bytes)) == cid. The 2 raster artifacts also verified (2/2). Their decoded centre pixel is 900 / 2502, matching the anchors. Every cited token appeared in that run's own tool results.
- **Cost/time:** $2.12 in total (per run $0.11–0.52), median wall time 31.6 s, 4–15 tool calls.

## Table
| i | 23-Sep evidence | 25-Sep evidence | CHANGE | method | tokens cited | numbers backed (direct+computed/total) | flags | tool calls (errors) | wall s | cost $ |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | c: none (raster returned 25 Sep) | containing px 900/2502 (offset-corr.) | no material change (self-flagged unverified) | B04/B08 NDVI diff, not computed | 4 raster | 16+1/17 | offset, same-scene | 7 (0) | 35.3 | 0.518 |
| 2 | c: none | containing px | undetermined | B04/B08 NDVI window-mean diff, not computed | 3 raster | 15+1/16 | offset, same-scene | 6 (1) | 31.3 | 0.166 |
| 3 | c: none | containing px | undetermined | B04/B08 NDVI after (DN−1000)/1e4, not computed | 2 raster | 11+5/16 | offset, same-scene | 7 (0) | 32.9 | 0.190 |
| 4 | c: none | containing px | undetermined | B04/B08 NDVI after offset, not computed | 2 raster | 13+1/14 | offset, same-scene | 7 (1) | 31.2 | 0.177 |
| 5 | c: none | containing px | no material change (self-flagged "not a finding") | B04/B08 NDVI per pixel, Δ=0 trivial | 4 raster | 34+8/42 | same-scene; wrongly suggests no 23 Sep scene | 4 (0) | 25.6 | 0.114 |
| 6 | c: none | containing px | no material change (self-flagged placeholder) | B04/B08 NDVI diff, not computed | 2 raster | 7+2/9 | same-scene | 7 (1) | 31.6 | 0.195 |
| 7 | c: none | containing px | indeterminate | B04/B08 NDVI window-mean diff, not computed | 3 raster | 8+1/9 | same-scene; wrongly claims no 23 Sep acquisition | 4 (0) | 25.2 | 0.111 |
| 8 | **b: containing pixel** (0.0901/0.2605, post-fix facts via backfill) | containing px 0.0900/0.2502 | **no material change** (measured ΔNDVI −0.015) | B04/B08 reflectance NDVI at cell | 4 fact | 21+14/35 | none | 15 (0) | 45.8 | 0.343 |
| 9 | c: none | containing px | no material change (self-flagged placeholder) | B04/B08 NDVI (+B11 intended), not computed | 2 raster + 2 fact (25 Sep) | 10+3/13 | offset, same-scene | 6 (1) | 32.7 | 0.164 |
| 10 | c: none | containing px | no material change (self-flagged default) | B04/B08 NDVI, not computed | 4 raster | 12+10/22 | offset, same-scene; wrongly suggests no 23 Sep scene | 5 (1) | 23.8 | 0.137 |

Tool errors are all the expected `emem_band_cube` refusal.

## Side effects and non-independence (disclosed)
We made no writes or signatures ourselves, and write tools were denied. emem's read tools still persist records on the server:
- Every `emem_band_raster` call minted a derivation record, and the 26 cited raster CIDs are those records.
- Trial 8's `emem_recall` and `emem_backfill` caused emem to materialize and sign four new s2.B04/B08 facts, signed 2026-09-30 13:53Z: 23 Sep `aorer7jt…` and `flf5bk4q…`, 25 Sep `wbbu4ezm…` and `4utkk3hy…`.
- In trials 9 and 10 the raster anchors then carried the 25 Sep fact CIDs (`fact_cid` was null in trials 1–7), and trial 9 cited them. The trials are therefore not fully independent. This changes only the citation handles, not the band values.

## Files
prereg.md, prereg_hash.txt, claude_run.py, run_trials.py, pilot.py, analyze.py, trials.jsonl, trials.log, results.json, raw/ (trialNN.jsonl stream-json transcripts, .err, .results_full.json, pilot_*), tools_list_full.json.
