# v13 evidence (copied from the session scratchpad on 1 Oct 2026, so it outlives the session)

| folder | what | cited by |
|---|---|---|
| `g2_handoff/` | the two-LLM pre-registered handoff (Claude Sonnet 5.5 as A; Claude Haiku 4.5 and the local Qwen2.5-3B as B): prereg + addenda, runners, `agent_a.jsonl`, `claude_b_trials.jsonl`, **`qwen_trials.jsonl` (52 rows; the adverse Qwen arm never committed before)**, raw transcripts. Models and venv omitted. | reports 02, 07, critic |
| `g1_pixel_audit/` | the M15 prevalence sample: **`prevalence.py` (seeded 20261019, one record per cell from emem.dev/channel.json)**, `prevalence.csv/json`, the channel snapshot, census, footprint, raster/cube checks | reports 01, 05, 10, critic |
| `failure_modes/` | Rondônia floor-vs-round re-reads (Hansen v1.13, GFC2020 V4), Element84 Keylong items, the pre-fix fact, OSM 1411107, CHANGELOG at 18adb67 | report 05 |
| `ladder/` | extra R1 signer-error probes (`r1_t2_extra.py`, out), claim-gate prototype, witnesses and STH snapshots, A2A card | report 10 |
| `ecosystem/` | integration probes (MCP initialize/tools/list, registry/PyPI/npm/GHCR JSON, framework tool lists), `build_manifest.py` | report 03 |
| `crossruntime/` | refusal matrix (LangChain returns a refusal as text), untrusted mirror (+0.1 value passes the receipt, fails the re-hash) | reports 02, 07 |
| `critic/` | live checks used to settle conflicts between reports | report 11 |
| `demo_site/` | the static receiver demo (verdicts, live source re-read) and its build scripts (node_modules omitted) | report 09 |
| `visual/` | M15 prototype from real Keylong grids, page mock and 3 m simulation, palette checks, QR set | report 06 |
| `industry/` | integrity probes of Planetary Computer / CDSE / NASA CMR from the v8 round | v8 board |

Complete IBM Plex Sans/Mono TTFs (OFL) are in `poster/fonts/plex-full/` (the board's subsets lack arrows, ≤ ≥ ≠, Greek and ≈).
