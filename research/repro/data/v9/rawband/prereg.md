# v9 raw-band change experiment — pre-registration

Written 2026-09-30 before any trial. Pilots (tool listing only, no task prompt) were run first and are recorded
as pilots, not trials: raw/pilot_core.*, raw/pilot_full.*.

## Question prompt (verbatim, unchanged from the brief)

"Using emem, determine whether the surface at Keylong, Lahaul (32.57126 N, 77.03448 E) changed between the Sentinel-2 scenes of 23 Sep 2026 and 25 Sep 2026. Work from the raw band values, not a precomputed index: choose the bands and the method yourself. Cite every number you use by its emem token. End with exactly three lines: CHANGE=<greener|browner|no material change>, METHOD=<one line: bands and formula>, TOKENS=<comma-separated emem tokens you used>."

The pilot showed no tool-naming problem, so the prompt is used verbatim.

## Setup
- Model: claude-sonnet-5-5 via `claude -p` (runner claude_run.py, copied from v8/followup-G2 with two changes:
  selectable MCP config file; optional --disallowedTools list).
- Isolation: emem is the only MCP server (--strict-mcp-config), built-in tools off (--tools ""), allowed tools
  mcp__emem__*, fresh empty temp cwd per run, no setting sources, no session persistence, stream-json parsed.
- Endpoint: https://emem.dev/mcp/full. Reason: the pilot on core https://emem.dev/mcp offered 18 tools and no
  documented raw-band reader (only emem_recall with unverified band keys); /mcp/full offers 116 tools including
  emem_band_raster / emem_band_cube / emem_band_composite (s2.B02..B12) and emem_recall/emem_grid.
- Write-side tools are denied so the experiment stays read-only from our side: emem_memory_create,
  emem_memory_insert, emem_memory_str_replace, emem_memory_rename, emem_memory_delete, emem_memory_supersede,
  emem_derive, emem_entity, emem_entity_link, emem_eudr_dds. (Server-side materialize-on-miss by emem itself,
  e.g. recall/raster minting, cannot be prevented and is not our publishing; any such side effect is logged if seen.)
- n = 10 sequential trials, budget --max-budget-usd 3 per run, timeout 600 s.
- Infra failures (non-zero exit with no model output, MCP server not connected, HTTP 5xx making the run
  impossible, timeout of the runner) are re-run and logged; model behaviour (wrong answer, giving up, budget
  exhaustion) is NOT re-run.

## Reference values (hidden from the agent)
23 Sep S2C: pre-fix neighbour pixel (row 9444) B08 2993 / B04 1972, NDVI(offset −1000) 0.3444, SCL 5, fact
kxjvfwpa7grmfhkxoxufq5xjltq2s5syer2rzdx7odbnrxhnjzkq. Containing pixel (row 9443) B08 3605 / B04 1901, NDVI 0.4860.
25 Sep S2A (post-fix, fact oj5cecci…): containing pixel B08 3502 / B04 1900, NDVI 0.4709, SCL 4.
Equivalent forms counted as the same evidence: raw DN, offset-corrected DN (DN−1000), reflectance (DN−1000)/10000
or DN/10000, and NDVI with or without offset.

## Primary outcome
Per run, the 23 Sep evidence relied on, determined from tool-result text in the transcript:
- (a) pre-fix neighbour: tool results for 23 Sep contain B08 2993 and/or B04 1972 (any equivalent form) or fact kxjvfwpa…
- (b) containing pixel: tool results for 23 Sep contain B08 3605 and/or B04 1901 (any equivalent form) from a post-fix read.
- (c) other/unclear: neither, or 23 Sep values that are something else (e.g. window means, composite, other pixel).
If tool results contain both (a) and (b) values, the class is decided by which 23 Sep values the final answer
uses, and the run is flagged "both_seen". Also recorded: which 25 Sep evidence (containing pixel 3502/1900, other).

## Secondary outcomes
1. Final CHANGE verdict (parsed from the CHANGE= line; missing/malformed recorded as such).
2. Verdict correctness vs ground truth: containing pixel ⇒ "no material change". Rule: |ΔNDVI| < 0.05 ⇒ no
   material change; ΔNDVI ≥ 0.05 greener; ≤ −0.05 browner. Truth = no material change (ΔNDVI ≈ −0.015).
3. Internal consistency: does the verdict follow from the numbers the agent itself cited, under the same rule
   applied to its own method (for non-NDVI methods, the agent's own stated threshold, else judged by hand and noted)?
4. Methods: band set + formula per run (from METHOD=), count distinct methods across runs.
5. Tool sequences (ordered tool names), tool-call count.
6. Numbers-backed: every numeric value in the final answer (excluding numbers copied from the prompt — coordinates,
   dates/years, band names like B04/B08, scene names, and characters inside emem tokens/CIDs) is classified
   directly-backed (appears in tool-result text, allowing rounding to the answer's displayed precision),
   computed-from-backed (reproducible as a−b, a/b, (a−b)/(a+b), a−1000, a/10000 or (a−1000)/10000 from backed
   numbers, at displayed precision), or unbacked. Report directly-backed fraction and (backed+computed) fraction.
7. Flags noticed: whether the answer mentions SCL/scene classification, the −1000 BOA offset, or a pixel
   location/indexing/neighbour issue, and whether it mentions any caveat about the pre-fix record.
8. Cost (total_cost_usd), wall time, tool calls, turns.

## Analysis
Descriptive counts over n=10 (no significance tests). Token integrity: for ≥10 distinct cited fact CIDs,
GET https://emem.dev/v1/facts/<cid> with Accept: application/cbor and check base32-nopad-lower(blake3(bytes)) == cid.
Adverse results reported as-is.
