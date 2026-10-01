# 11 · Research gaps: what the v13 research phase still lacks before design and print

Completeness critic for the research phase. Written 2026-10-01 (UTC, about 01:20Z to 02:00Z). Inputs read in full:
`research/SHARED_STATE_EMEM_A0_MASTER.md` (558 lines), the 39 open issues of Vortx-AI/esa_poster (#5 to #7, #11 to #46;
GitHub MCP `list_issues`, 0 closed issues exist), and every file under `research/v13/` (00 to 10, `ecosystem_manifest.json`,
`cost_measurements.json`). Only this file was written. Nothing was signed or published. emem.dev received GETs only
(`/v1/facts/{kxjvfwpa…,oj5cecci…}`, `/v1/cells/defi.zb572.xoso.zb1ec`, `/v1/log/witnesses`) plus one JSON-RPC
`tools/list` on `/mcp`. Critic scratch files: `/tmp/claude-0/-home-user-esa-poster/0db6b3ad-8059-51a6-bd74-2d7a97faf986/scratchpad/critic/`.

Labels: **MEASURED** (computed here; command or file named) · **LIVE** (fetched here, UTC time) · **SPEC** (emem code, docs
or commit message; commit and path given) · **INFERRED** (my reasoning) · **UNVERIFIED** (stated elsewhere, not checked).

---

## 0. Summary

1. **The principal result the brief asks for does not exist yet.** MASTER §6 and §9 and issues #6 and #16 ask for an
   agent-to-agent adversarial handoff with prose, JSON, RAG, opaque-id and EMEM conditions across 4 to 6 models. That
   experiment (R5, report 02) is designed and smoke-tested but has not run. Every agent-level number on file comes from
   n = 5 to 19 per arm, two model families, and a constructed threshold. One of those arms runs against the token:
   Qwen2.5-3B was 0/19 correct with the token and 10/18 with prose. MEASURED (critic recount of the uncommitted
   `qwen_trials.jsonl`).
2. **The evidence behind the strongest findings exists only in an ephemeral scratchpad.** That includes the Qwen arm, the
   refusal matrix, the M15 prevalence sampling script with its per-record CSV, the eight-answers data, the Rondônia
   floor/round re-read, the P1 to P3 probes, the demo site and the visual prototypes. Reports 05 to 10 and
   `cost_measurements.json` are themselves untracked (`git status`). MEASURED.
3. **The reports disagree on about a dozen printable facts.** I checked each conflict myself (section 2). Six of them would
   put a wrong number or word on the board if copied: "9 of 10 agents noticed" (it was 10 of 10), last-rep latencies
   printed as medians, a tool-list token count whose value depends on how the JSON is serialized, 596 m vs 597 m,
   14 vs 28 pre-fix Keylong records, and Dify "verified" vs "community".
4. **The research read emem at 18adb67, but emem.dev runs 8e9b401, seven commits later.** One of those commits records a
   resolved error that makes the user's "catastrophe" point better than anything in reports 01 to 10. The words
   "this image" were geocoded to a hair salon in Ontario, and "Every part of the verification machinery worked on an
   answer about a hair salon in Canada" (SPEC, emem commit 0edf574 message). Section 3.
5. **Three of MASTER §28's seven questions cannot be answered truthfully from evidence today:** Q1 (the problem rests on a
   constructed rounding), Q5 (no measured RAG arm) and Q7 (every reproducibility QR target is 404 or unpublished).
   Q6 is partly answerable (ChatGPT unverified). Section 4.

---

## 1. Prioritized gaps and the action for each

P0 means the board cannot print truthfully, or cannot meet a binding brief section, without it. P1 means a workshop
reviewer would attack it or a brief item stays only partly met. P2 is polish or a low-risk residual.

### P0

| id | gap | evidence (label) | concrete action | owner / by |
|---|---|---|---|---|
| P0-1 | **Evidence at risk of loss.** The Qwen trials (52 rows, BLAKE3 `cb6e6369…318f`), G2 scripts, `refusal_matrix.json`, `refusal_ts.json`, `untrusted_mirror.json`, M15 sampling (`prevalence.py`, `prevalence.csv`, `prevalence.json`, `channel_facts.jsonl`), eight-answers data (`fm/e84_keylong.json`), Rondônia floor/round (`fm/rondonia_floor_round_v2.json`), P1 to P3 probes (`v13ladder/r1_t2_extra*.{py,json}`), claim-gate prototype, demo build and site, `proto_m15.*`, `mock_layout.*`, `palette_*`, `eco/build_manifest.py` and the cost scripts all sit only in the session scratchpad. Reports 05 to 10 and `cost_measurements.json` are untracked. | MEASURED: every file listed exists under `scratchpad/` (stat, 01:45Z); `git status` lists 05 to 10 as `??`; committed `results.json` has `"qwen2.5-3b-instruct-q4_k_m": {"arms": {}}` (report 07 §6) | Copy everything into `research/repro/v13/{g2_archive,prevalence,failure_modes,ladder,demo,visual,eco,cost}/` with a `MANIFEST.blake3`. Recompute the Qwen arm of `results.json` from `qwen_trials.jsonl` and label it "52 of 55 pre-registered trials". Commit reports 05 to 11. | next agent, today (the scratchpad dies with the session) |
| P0-2 | **R5 has not run, and its inputs are not frozen.** It is the only route to MASTER §9's RAG condition, decision accuracy, models/runtimes, and #6's 4 to 6 model families. Without it, the board's hero figure is the deterministic R1 matrix, which compares by construction: prose has nothing to verify. | SPEC: report 02 §8 to §16; MEASURED: R1 levels A and B "acted on corrupted evidence" 15/15, but the decision flips in only 6 of the 15 (`mutation_matrix.json` `summary.A.decision_flips` = M2, M8, M12, M13, M14, M15) | (a) Ask the user to decide on Fable 5.1 (about $85), the Tier-3 open models, and the AWS/GCP credentials (needs explicit permission). (b) Freeze R1-v13 first. Add P1 to P3. Replace M11's fictitious scene id (P0-4j). Add M5b, M6-NBR, M18, M20 and the as-of check. (c) Run Blocks P, 1, 2 and **Block 0 (natural corruption)**. (d) Print decision flips beside every false-accept rate. | experiment agent; run by about 6 Oct so design can freeze before the print deadline (06 §11 asks the print shop by 10 Oct) |
| P0-3 | **No canonical ladder or failure ladder.** 05 §5, 06 §6.5 and §6.12, 08 §2 and 10 §3.2 use different rung sets, orders and row labels. Defect 37 (the wrong place) is L1 in 05 and 06, L4 in 10, and "the right trace, the wrong place" in 07. | SPEC/MEASURED in each report. 07 §3.3 and 00 M13 show that the token check passes on defect 37 (`cell(b) = cell(token)`). Only a check of the answered cell against the cell of the asked coordinates catches it, and R1 does not implement that check. | Adopt 10 §3.2 as the only layer vocabulary (08's "cryptographic trust" rows fold into L0, per 10 §3.8). Put defect 37 at **L1, caught only by binding to the receiver's own coordinates (not implemented in R1; implemented in the R5 verifier, 02 §11)**. Its name-only form ("Keylong" with no coordinates) is L4. Build one failure ladder from 06 §6.12, with rung order and statuses taken from section 3 below. | design agent, before figure work |
| P0-4 | **Cross-report contradictions that would print wrong values.** | All MEASURED by the critic; details in section 2 | Fix at the source before any caption is generated: (a) v9 "9 of 10 noticed" becomes **10 of 10** (the committed `rawband/results.md` needs an erratum line; 05 copies the error). (b) Latencies use `ms_median`, not `ms` (01 copied the last repetition). (c) The tool-list count is printed with its serialization and tokenizer. (d) Distance: print 597 m (WGS-84 geodesic). (e) Pre-fix Keylong records: 14 of the 141 plotted, 28 of all 155. (f) Offline check: one host-stated figure. (g) Bengaluru: 10 paths, not 11. (h) Receipts verify on 9 of 11 paths. (i) Dify: print "community", never "verified". (j) M11's scene id `S2B_MSIL2A_20260927T054239_R005_T43SFS_20260927T081707` does not exist (PC STAC 404), so the mutation is weaker than it looks. (k) Report 02 §0 says about $80 / $200, its §13 says $75 / $190; use §13. | whoever writes the claims registry (10 §5.2) |
| P0-5 | **Cited emem commit.** The reports cite 18adb67, v12.1 cites 04b40c5, emem.dev serves 8e9b401. Report 01 said 04b40c5 was not in the clone; it is there now. | MEASURED: `git merge-base --is-ancestor` shows 18adb67 → e226f8b → **04b40c5** → ab5af22 → 0edf574 → 29a655b → 5c7787b → **8e9b401** (one line). `x-emem-commit: 8e9b401cecae…` (LIVE 01:41Z). `lib.rs` changed between 18adb67 and 8e9b401, so its line numbers shift. | Print **8e9b401** (deployed) once in the footer. Re-run every `file:line` citation the board prints against 8e9b401, especially the `lib.rs` lines (51499-51543, 38229, 38451, 12645-12696, 37800-37818). Add the new resolved errors from section 3 to the failure ladder. | claims-registry owner |
| P0-6 | **Every reproducibility QR would land on a 404 today** (MASTER §25, §28 Q7; #34, #44). | MEASURED (09 §0.6): Pages off (`has_pages:false`); `research/repro/v13` missing on `main`; repo has no LICENSE; the branch is not merged | Authors: enable Pages (`main /docs`), add a LICENSE (code Apache-2.0, poster and media CC BY 4.0 per 09 §9), merge to `main`. Build agent: `research/repro/v13/README.md` (one re-run command) and `METHODS.md`. Then decode and phone-test all six QRs (09 §8 gates 1 and 2). | authors + build agent, before QRs are drawn |
| P0-7 | **Board size and orientation are unconfirmed.** The whole layout assumes A0 portrait 841 × 1189 mm. | LIVE: no page on agentic-eo.berlin states a poster size (checked `/`, `/calls/call-for-abstract/`, `/attend/venue/`, `/dates/`, `/attend/registration/`, 01:50Z). `research/should_do/07_EVENT_FORMAT_PEOPLE_AND_ACTIONS.md:98` "Email the organisers about board size, orientation, pins" is still unchecked. | Authors email `paper@agentic-eo.berlin` today: board size and orientation, mounting, whether a screen or Wi-Fi is available for the demo, and the digital-copy policy. | authors, today |
| P0-8 | **ChatGPT is mandatory content "where verified" (MASTER §16) but cannot be verified from outside.** | UNVERIFIED (03 §1.1: 403 JS challenge). The manifest row has `status: "LIVE"` while its evidence is UNVERIFIED (MEASURED, `ecosystem_manifest.json` row `chatgpt`) | A logged-in author takes a dated phone screenshot (title, developer, status) into `research/v13/`; until then the row is `UNVERIFIED` and is not printed. Fix the row's status field. | authors |
| P0-9 | **The M15 headline (162/200) cannot be reproduced from committed files, and its sampling frame is not stated.** | MEASURED: only `prevalence_summary.json` is committed. The script (scratchpad `followup-G1-pixel-audit-before-after/prevalence.py:1-20`) samples "Sentinel-2 point facts cited in https://emem.dev/channel.json. One fact per cell (seeded random)", seed 20261019, compares `signed_at` strings with `PIXEL_FIX_AT`, and takes all post-fix facts (0/54, all Planetary Computer, two days). | Commit the script, `prevalence.csv` and the `channel_facts.jsonl` snapshot (or its BLAKE3). Print the frame at 30 cm: "200 pre-fix Sentinel-2 records cited in emem.dev's public channel, one per cell, seeded random". Either re-sample post-fix records over the days since 28 Sep (GET only), or print "post-fix sample: one provider, two days". | next agent |

### P1

| id | gap | evidence | concrete action |
|---|---|---|---|
| P1-1 | **Embeddings are in the official title (MASTER §19) but no report covers them.** A Φ-lab reviewer will ask. | LIVE (critic, `GET /v1/cells/defi.zb572.xoso.zb1ec` 01:42Z). The Keylong `prithvi_eo2` record (1,024 floats, signed 2026-07-18) carries `served_via.model_blake2b_hex 2ad1775f…62cc`, and the same digest is in its hashed `derivation.args`. The `geotessera` record (128 floats) names `…/tessera/npy/v1/2024/...`, a truncated path, with no checkpoint. All four encoders are retired (10 §1.3, SPEC). This also settles 02 §7's UNVERIFIED "64-hex field": it is the model digest. | Print one 1 m line, "Derived representations are addressable too: this cell's Prithvi vector names its checkpoint digest inside the hashed record; the TESSERA vector names only a product year", with a 30 cm note on retirement. Add M21/M21b to R1-v13. Decide whether the title stays verbatim (06 and 10 say yes). |
| P1-2 | **The problem panel (Q1) rests on injected rounding.** The team's own agent A kept all 16 digits 10/10. | MEASURED (committed): G2 A arm 10/10 carried 16 digits; 1/10 wrote the wrong year (`results.json`); R arm "0.47" was exploratory and constructed (`prereg.md`) | Run R5 Block 0 (natural A corruption, 02 §8). Cite emem's benchmark-arm 21.7 % retype rate only as emem-authored (SPEC) and the literature (Laban 2505.06120, 04 §6). Say on the board that the threshold is constructed. |
| P1-3 | **Adverse agent-level results must be on the face.** Report 07 says so; 06's panel 2 omits them. | MEASURED (critic recount): Qwen2.5-3B T 0/19 (19 × IRRIGATE), P 10/18, R 2/10 (+4 DECLINE), F 5/5 acted. Qwen sent the bare cid in 24 of 24 resolve calls. Haiku T and P tied 10/10 at 2.1× input tokens (08 §2). | Print 07 §3.6's sentence ("a reference protects only a receiver that keeps it whole and obeys a refusal") and the Haiku tie with its cost. In R5, add "receiver strips the cell" and "adapter returns refusal as text" as conditions (02 E+ already covers part of this). |
| P1-4 | **#43 "same evidence, different agent" is shown only at the protocol level.** | MEASURED (committed): 11 client paths, 1 cid (30 Sep, server 213e273). G2 has 2 model runtimes. The 5-lane run (02 §15, under $1) has not run; no host pair has a model in the loop. | Run 02 §15 lanes 1 to 5 against 8e9b401. Print "11 client paths; 2 model runtimes; ChatGPT and Dify not run" until host legs exist. |
| P1-5 | **"Catastrophe" needs measured consequence sizes.** Most wrong-pixel errors are small. | MEASURED (critic, from scratchpad `prevalence.csv`): of 91 pre-fix index records where the rules differ, 4 cross a conventional class boundary (NBR 0.1; NDMI 0; NDBI 0). The thresholds are my illustrative choice (INFERRED). Index error median 0.027, max 0.301 (committed). Rondônia: 0 of 3 EUDR flags change (05 §4.3). Large single cases exist: `jwkqm6eh` 0.4872 signed vs 0.7669 containing pixel (00 F01). | Pre-register per-index thresholds and report "crosses a class boundary in k of n" for the 162. Print measured consequences, never the word "catastrophe" (05 §7). Lead with the cases where every check passes. |
| P1-6 | **No independent replication.** | SPEC (02 §4): "Nobody outside the team has run any part" | Ask one person outside Vortx to run RE-RUN THE TEST (R1 plus `verify_bundle.py`) on their machine and record date, OS and output hash. Print "replicated by <name>, <date>", or state that no outside run exists. |
| P1-7 | **QR destinations conflict across 06, 07 and 09.** | 06 §6.16 (header TRY THIS TOKEN → `emem.dev/verify`; INSPECT → raw JSON); 07 §3.1 (ememdemo track and token pair); 09 §2 (Pages site). MEASURED (09): the ememdemo track fires `POST /v1/recall` and shows "29 of 30" in red when that call is blocked; `emem.dev/verify` shows the result about 825 px down and says "verified in this tab" (SPEC `verify.html:489` at 8e9b401). | Adopt 09's six-QR Pages set. Put ememdemo in a 30 cm text link only, unless the track is rebuilt without the recall step (author signature needed). |
| P1-8 | **Temporal claim (#19, MASTER §13) is not falsified and not distinguished from bitemporal databases.** | 04 §2.11 covers RDA WGDC with UNVERIFIED wording; no comparison with SQL:2011 or Snodgrass bitemporal models (10 §1.3 only lists them). M20 has not run. LIVE (critic 01:42Z): `oj5cecci…` still resolves (1,115 B, re-hash equal) while `current_by_band["indices.ndvi"]` is `3yyaxn5d…` (30 Sep). That is a natural H3 instance. | Print the H3 instance as measured. Read the RDA WGDC PDF (doi:10.15497/RDA00016) for R6 and R9 verbatim. Add one 30 cm sentence on what EMEM adds beyond a bitemporal table: the receiver holds the address of the cited state and checks it without the database. Run M20 in R5. |
| P1-9 | **EUDR text is only partly verified.** | LIVE: EUR-Lex returns HTTP 202 with an empty body (critic, 01:48Z). The EC trade portal (trade.ec.europa.eu, retrieved 2026-10-01) gives 30 Dec 2026 and 30 Jun 2027 under Reg. (EU) 2025/2650. Art. 25 (4 % fines) and Art. 2(28) remain secondary sources (05 §8.6). | Print no article numbers unless an author reads them on EUR-Lex from a browser. Keep MASTER §21's line. |
| P1-10 | **emem's own docs contradict its code on points the board touches.** A visitor who reads them finds the contradiction. | SPEC at 8e9b401: `docs/model.md` row `s` says "ed25519 over blake3 of the canonical CBOR body" and row `p` lists "content hash" in `sources[]`; `README.md:246` says "co-signed by independent witnesses … so a split view is detectable"; the README architecture alt text says the same. LIVE: `independent_operator_count 1` (geo.qa, Vortx), `head_is_independently_witnessed false` (01:42Z). | The board follows the code (10 §2). Ask emem's maintainers to fix model.md and README:246 before 19 Oct. If not fixed, add a 30 cm "where emem's docs and code differ, this board prints the code". |
| P1-11 | **"Stable" in MASTER §4 overstates.** One value has many addresses. | MEASURED (committed): 915.0712 m signed 7 times under 7 cids (`contra_bengaluru.json`); `signer` and `signed_at` are hashed (10 §2.5) | Wording: "the record's address never changes; the same observation signed again gets a new record". Never "stable identity of the observation". |
| P1-12 | **Ecosystem manifest is internally inconsistent.** | MEASURED: `chatgpt` status LIVE while its evidence is UNVERIFIED; `langchain` `print.allowed: true` while 03 §7 says "after the fix"; `official-mcp-registry` url 404s in Chromium (09 d19); four routes broken (Gemini extension, Cline, LangChain, Semantic Kernel; 03 §0.3) | Fix the three rows. Decide whether emem fixes the four routes before print or the band omits them. Gate on `verified_utc` within 14 days (03 §8). |
| P1-13 | **The #22 attack-question file is not assembled.** | 04 §7 answers 12 questions. Missing from #22's list: "What exactly is novel?", "Is the source trusted?", "Is entity identity solved?", "Is this live on a spacecraft?", "How large is the benchmark?", "How many independent models/operators?", "What happens with embeddings?", "What happens when source data changes?" | One file, `research/v13/12_attack_questions.md`, with 20 answers of 50 words or fewer, each linking a committed source. Answers exist in 10 §1/§4, 02 §17, P1-1, P1-8 and section 5 below. |
| P1-14 | **Accepted abstract and DOI metadata are unchecked.** | The accepted 300 to 500 word abstract is not in the repo (MEASURED, `git ls-files`). LIVE (01 §2.2): the Zenodo v0.1.0 title reads "emem: A research on …" and the creator reads "Singh, Avijeet Singh". | Commit the submitted abstract and check the board against it (the title promises embeddings). Re-mint or correct the Zenodo record, or drop the DOI from the board. |
| P1-15 | **The claim-status gate (#21) is specified but not built.** The current gate cannot read figure text. | MEASURED (10 §5.6): the prototype finds 36 items on v12.1; the existing `prose_gate` finds 0 (`build_v12.py:43` strips `<svg>`) | Build agent implements 10 §5.2 to §5.5 with the registry populated from section 2's resolved values. |
| P1-16 | **Network and latency figures are path-specific.** | MEASURED (08): every timing went through a TLS-re-terminating proxy over HTTP/1.1; B08 tile at about 0.46 MB/s | Re-measure resolve (cold, warm) and source re-read from an author laptop on an ordinary network, or print "on our test path, through a proxy". |
| P1-17 | **Only OpenAI BPE token counts exist.** The board's models are Claude. | MEASURED (08): cl100k/o200k only. MEASURED (committed G2, 02 §2): the emem plugin raised Claude Code (Haiku) per-call input from 4,125 to 21,555 tokens. | Print the in-host Claude figure (+17,430 input tokens per call with the 18-tool plugin) beside the cl100k counts, each labelled by tokenizer. Or measure Claude counts through the CLI's `usage` for value, token and prose strings. |
| P1-18 | **Print colour condition unknown.** | SPEC (06 §3.4, §11.2) | Authors ask the print shop (sRGB inkjet vs PDF/X-4 FOGRA39/51). |

### P2

| id | gap | action |
|---|---|---|
| P2-1 | Rondônia has no imagery; the wrong-pixel figure uses 25 Sep, not `kxjvfwpa`'s own 23 Sep scene (06 §11.4, §11.5) | Fetch both from Planetary Computer (public STAC + COG range reads, no emem read tool). |
| P2-2 | Safari/iOS untested for the demo (09 §3.7) | One iPhone (iOS 16.4+) and one Android test, dated in the media manifest. |
| P2-3 | Hostile objection 4 (ungated `POST /v1/attest_cbor`) | Resolved in code, SPEC at 8e9b401: `post_attest_cbor` calls `put_attestation`, which refuses a key that is neither enrolled nor operator-listed ("fact_plane_closed … LevelTooLow", `crates/emem-storage/src/lib.rs:1005-1038`). Not tested live (it is a write). Matters only if the SAT-042 line stays. |
| P2-4 | Fix status of defect 15 (recall default 2022 scene) and defect 18 (re-mint gives new cid) not checked | Read the recall and derivation code at 8e9b401; print nothing about them unless checked. |
| P2-5 | Why the six MCP signing proposals were closed; OWASP ASI06/ASI07 wording; GeoGuard commit hash; CDSE trace signature not cryptographically checked; pixel equality of the three B04 files (04 §9) | Close each, or leave it off the board (04 already forbids printing the unverified ones). |
| P2-6 | Workshop dates: home page "19-20 October 2026", `/dates/` and schedule "19–21 October 2026" (LIVE 01:50Z) | Print only "Poster Session 1 · 19 Oct 2026". |
| P2-7 | Moving counts: the Keylong cell holds 207 (22:43Z), then 208 (07), then 209 facts (LIVE 01:42Z); `current_by_band` lists 12 bands while the facts span 14; the log head's "independently witnessed" flag read false (00:33Z), true (00:48Z), false (01:02Z, 01:42Z) | Never print these snapshots. Print "one address, many products" with a dated count only in the 30 cm tier, and "all keys today are one operator's". |
| P2-8 | Cell size: "about 9.55 m" holds N-S. E-W is about 8.0 m at Keylong and 5.8 m at Berlin (00 F19; INFERRED cos-latitude arithmetic) | State "a lattice node; about 9.5 m by 8 m here". |
| P2-9 | Logo permissions (03 §6) | Typographic band; GitHub (black) and Dify (mono) marks at most. |

---

## 2. Conflicts between reports, and between reports and the data (each checked here)

| # | conflict | what the data says (critic check) | label | resolution |
|---|---|---|---|---|
| C1 | v9 raw-band: 05 §2 F3 and the committed `results.md` say "9/10 noticed both dates were one scene"; 07 §3.7 and 00 F8 say 10/10 | Every one of the 10 final answers states the same-scene fact (trial 8: "kept returning the 25 Sep scene"; trial 3: "byte-identical across dates") | MEASURED (`trials.jsonl` `result_text`) | **10 of 10 noticed; 9 of 10 never got 23 Sep values; 3 of 10 then wrote that no 23 Sep scene existed.** Add an erratum to `rawband/results.md`. |
| C2 | Cross-runtime latencies: 01 §6.2 gives A2A 214.0, TS SDK 79.3, LlamaIndex 334.3, LangChain 1,201.1, official MCP Py 58.3, TS 57.6; 06, 07 and 08 give 226.3, 58.6, 300.8, 1,176.8, 56.3, 58.3 | `crossruntime_table.json` holds two fields: `ms` is the last of three repetitions, `ms_median` the median. 01 read `ms`. | MEASURED | Use `ms_median`. Also: Bengaluru ran 10 paths, not 11 (03 §3); `receipt_verified_paths 9` of 11 (01 says all rehash, which is true of re-hash only). |
| C3 | MCP 18-tool list: 20,838 cl100k (02, "LIVE"), 18,709 (08), 18,659 (committed `token_counts.json`) | Same response today: raw body 77,014 chars = **18,709** cl100k (19,125 o200k); the tools array re-serialized by `json.dumps` with default separators = 20,800; compact = 18,538; indent 2 = 23,722 | MEASURED (critic `tools/list` 01:4xZ, `x-emem-commit 8e9b401c`) | 02 counted a re-serialized form. Print "18.7 k cl100k tokens as served (1 Oct)" or the in-host Claude Code figure (P1-17), never both unlabelled. |
| C4 | `/v1/ask` place error: 596 m (05, 00 M13 haversine) vs 597 m (01, 06, 07, 10) | Haversine 596.3 m; WGS-84 geodesic 597.5 m from the asked point, 597.3 m from the cell node | MEASURED (pyproj) | Print 597 m (geodesic). |
| C5 | Pre-fix Keylong records: 10 §6 rows 26 and 27 say 14 | `case_keylong_ndvi.json`: 14 of the 141 plotted 2025–26 rows; 28 of all 155 rows signed before `2026-09-28T04:09:26Z` | MEASURED | Say "14 of the 141 plotted" or "28 of 155", with the denominator. |
| C6 | Offline full check: 1.187 ms (01, 06 caption "1.2 ms", 09) vs 0.357 ms (08) and 0.359 ms (10) | Same code; host-dependent (08 §M2) | MEASURED (committed vs this host) | Print one host-stated value ("about 1 ms on one laptop core") and keep the range in the claims map. The browser demo's 11.7 ms (09) is a different implementation and must say "in a phone browser". |
| C7 | Network resolve: 06 uses 223.6 ms "median of 10 timed paths"; 08 measured 154 ms cold and 40 ms warm | The path medians include a signing `POST /v1/memory_token/resolve` plus a CBOR GET (`crossruntime_table.json` `call` field); 08 measured GET only | MEASURED | Cost panel: GET cold/warm from 08; path medians only in the ecosystem dot plot. |
| C8 | Dify: 03 "authorized_category community"; 09 page text "Verified by Dify" | Marketplace API: `verification.authorized_category "community"`, `badges []`, `latest_version 2.4.0`, `install_count 32` | LIVE (01:4xZ) | Print "community". The page string is not a badge on this plugin. |
| C9 | Head witnessed: 07 false (00:33Z), 08 true (00:48Z), 10 false (01:02Z) | `head_is_independently_witnessed false`, `independent_operator_count 1` (geo.qa), tree size 2,575,060 | LIVE (01:42Z) | The flag oscillates. Never print it; print "one operator". |
| C10 | Emem commit: 01 "04b40c5 not in the local clone" | 04b40c5 is present and lies between 18adb67 and 8e9b401 | MEASURED | See P0-5. |
| C11 | QR targets: 06 vs 07 vs 09 | See P1-7 | MEASURED (09) | Adopt 09. |
| C12 | Ladder vocabularies and the place error's layer: 05 vs 06 vs 08 vs 10 | See P0-3 | SPEC/MEASURED | Adopt 10 §3.2. |
| C13 | Agent-card JWS: 04 §2.13 "not verified here"; 03 §2 verified it under RFC 8785 + Ed25519 and rejected a tamper | Both true of their own session | MEASURED (03) | Cite 03. |
| C14 | Report 02's "64-hex field in prithvi_eo2 args, UNVERIFIED" | It equals `served_via.model_blake2b_hex` | LIVE (critic) | Resolved (P1-1). |
| C15 | Report 02 open item 6: is R1's M11 scene id real? | `GET …/items/S2B_MSIL2A_20260927T054239_R005_T43SFS_20260927T081707` → 404 NotFoundError; the real scenes for 20 to 30 Sep are S2C 20 Sep, S2C 23 Sep, S2A 25 Sep, S2B 25 Sep (R105, 1.59 % cloud), S2B 28 Sep, S2C 30 Sep | LIVE (Planetary Computer STAC, 01:5xZ) | M11 tests a fictitious id that any STAC lookup refuses. R1-v13 should relabel to the real S2B 25 Sep scene (10's P2). |

Spot checks that **agreed** with the reports (MEASURED or LIVE by the critic). R1 summary A 15/15 … I 0/16 and the
leave-one-out (`mutation_matrix.json`). The 780 facts all PASS, `recompute` pass 266 / n/a 514, and `kxjvfwpa` is a
PASS row (`eo_evidence_per_fact_checks.csv:180`). `kxjvfwpa` LIVE: value 0.34435075885328836, DNs [2993, 1972],
signed 2026-09-25T19:35:27Z, scene `S2C_MSIL2A_20260923T053641_…`, no flag in the body. `oj5cecci` re-hashes to its cid
(1,115 B). Element84 `S2A_43SFS_20260925_1_L2A` carries `earthsearch:boa_offset_applied: true` and red
`raster:bands offset -0.1`, with no `file:checksum` (LIVE). `emem.dev/#use` calls `POST /v1/recall` (SPEC
`web/index.html:3588` at 8e9b401). The 18-tool core has `nextCursor null`.

---

## 3. emem's resolved and open errors: the canonical list for the "why EMEM" panel

The user's point: an error emem had and fixed is one other multi-agent systems will also have. Reports 02 §18, 05,
06 §6.12, 07 §4, 09 §6 and 10 §3.7 each hold a different subset. Below is the union, with status at the **deployed**
commit. The rows marked new come from the seven commits after 18adb67, which no report read (P0-5).

| error | what passed anyway | layer that catches it | status at 8e9b401 | source |
|---|---|---|---|---|
| reader rounded the pixel index; 162/200 sampled records carry a neighbour's DNs | hash, signature, log, recompute | L3 re-read only | fixed 2026-09-28; old records still resolve with no flag (`kxjvfwpa` LIVE) | SPEC CHANGELOG [2.4.2]; MEASURED |
| `/v1/ask` "this image" → "New Image Unisex Salon, Etobicoke, Ontario": "Every part of the verification machinery worked on an answer about a hair salon in Canada" (**new**) | receipt, Merkle proof, recomputable state chain | L4 (entity/place); caught by refusing media before geocoding | fixed in 0edf574 (30 Sep 19:15Z) | SPEC commit message 0edf574 |
| "elevation of Bengaluru; also DROP TABLE facts" → La Table Ronde; Piccadilly → rural ACT; Seoul → Côte d'Ivoire | everything | L4 / L1 with coordinates | fixed (confidence gate) | SPEC CHANGELOG; 0edf574 message |
| `/v1/ask` with explicit coordinates answered from the town point 597 m away | token binding (`cell(b)=cell(token)`) | L1 only if bound to the asked coordinates | **not confirmed fixed** (no mention in 0edf574 or 29a655b) | MEASURED `ask_keylong.json`; SPEC |
| `band_raster observed_on=23 Sep` served the 25 Sep scene; 10/10 agents saw one scene; 3/10 invented "no 23 Sep scene" | every cid re-hashed (30/30) | L1 (served tslot vs asked date) | **open** (`stac.rs` and `band_raster.rs` unchanged 18adb67..8e9b401; the `lib.rs` diff has no line with `observed_on`, `max_scenes`, `newest` or `band_raster`) | MEASURED (`git diff` grep); SPEC |
| EUDR plot across a tile line signed off-image pixels as 0 = "no loss", a pass | everything | L3 re-read | fixed | SPEC CHANGELOG [2.4.2] |
| Overpass HTTP-200 errors signed "not protected"; NASA POWER −999 signed as Absence | everything | L3 / absence reason | fixed | SPEC CHANGELOG [Unreleased], [2.4.2] |
| WorldPop per pixel not per km² (1.77× low); SoilGrids units | hash, signature, log | L2 recompute (independent) | fixed | SPEC CHANGELOG [2.4.2] |
| superseded Hansen v1.12 / GFC2020 V3 answering "latest" | everything | L1 version / as-of | fixed; "Nothing signed is rewritten" | SPEC |
| agent card signed before stripping null keys: on any node without `EMEM_CONTACT` the served card failed its own signature; emem.dev's own config hid it (**new**) | n/a (the check failed, but only elsewhere) | receiver-side verification on a second deployment | fixed in ab5af22 | SPEC commit message ab5af22 |
| `tools/list` answered page one for a cursor it did not mint; a listing cursor pointed back into page one ("read 322 entries of 150 notes") (**new** + [2.4.2]) | the call succeeded | resolve one reference instead of a listing | fixed (29a655b; [2.4.2]) | SPEC |
| CI checked each commit against the old production server, so the contract gates judged the wrong binary (**new**) | CI green | independent verifier of the right artefact | fixed in 04b40c5 | SPEC commit message 04b40c5 |
| `robots.txt` told agents the MCP core was 16 tools when it was 18; directories show 16 (**new**; 03 §4) | n/a | address the catalogue (`capability_manifest_cid`) | fixed in 8e9b401; directories still stale | SPEC; LIVE (03) |
| `cell_matches` hard-coded `true` on every 200; then Qwen ignored the corrected `false` 5/5 | the receiver's check | fail-closed resolver (E+) | server fixed; receiver failure measured | SPEC `lib.rs:37800-37818` at 18adb67 (line numbers move at 8e9b401); MEASURED |
| `/verify` showed a green pass without checking a signature | the verifier | independent receiver code | fixed | SPEC CHANGELOG [2.0.0] |

Reading for the board (INFERRED): the hair-salon case is the clearest instance of MASTER §28 Q4. Every check above L3
passed, and the error was at L4, which no reference protocol can check. Pair it with M15, where every check below L3
passed and only the re-read caught it. Together they show the two edges of the guarantee boundary with real incidents.

---

## 4. MASTER §28: can a visitor answer the seven questions from evidence today?

| question | evidence on file | status | what closes it |
|---|---|---|---|
| 1 What problem? | R1 by construction; G2 rounded-prose arm 5/5 wrong (exploratory, constructed threshold); literature (04 §6); v9 date substitution 10/10 noticed, 3/10 invented a cause | **PARTLY**: no measured natural corruption rate | P1-2 (Block 0) |
| 2 What is new? | 10 §1 invention sentence; 04 §2 prior art incl. ARC, Sigstore, SCITT, nanopublications | **YES**, with credit lines | keep 04 §8's pattern-credit line |
| 3 What evidence? | R1 (one record, deterministic); M15 162/200; 780-fact L0/L1; Bengaluru as-of; G2 and Qwen | **PARTLY**: no R5; M15 frame unstated | P0-2, P0-9 |
| 4 What does it NOT prove? | 10 §3, §4; M17; hair salon; GFC2020 commission error | **YES** | P0-3 for one figure |
| 5 Why not STAC/RAG/C2PA/GeoGuard? | 04 §1, §7 (SPEC); 04 §3 three-archives figure (LIVE) | **PARTLY**: "Why not RAG" has no measured arm; emem's own BM25 tie 16/16 (SPEC) | R5 condition C |
| 6 Can I use it? | 03 manifest: Claude Code and Gemini CLI connect (MEASURED); 11 client paths; registries LIVE | **PARTLY**: ChatGPT unverified; 4 broken routes; no host-pair handoff | P0-8, P1-4, P1-12 |
| 7 Can I reproduce it? | prototypes only | **NO** today | P0-1, P0-6 |

---

## 5. Brief sections and issues still lacking research

Sections with no remaining research gap: §1, §2, §5, §12, §14, §15, §22, §23, §24, §26, §27 (reports 01, 04, 06, 10).
Sections with a gap: §3/§28 Q1 (P1-2); §4 "stable" (P1-11); §6, §7, §8, §9 (P0-2; H3 has one live instance, P1-8);
§10 (P0-9, P1-5); §11 (P0-3); §13 (P1-8); §16 and §17 (P0-8, P1-4, P1-12); §18 (P1-16, P1-17); **§19 (P1-1, no report
covered it)**; §20 (P2-3, low because SAT-042 leaves the face); §21 (P1-9, P2-1); §25 (P0-6).

Issues: research is sufficient for #11, #12, #13, #14, #15, #17, #23, #24, #25, #26, #27, #28, #29, #30, #32, #33, #36,
#37, #38, #42, #45 and #46 (design and build remain). Research gaps remain for #6 and #16 (P0-2), #7 (an emem change, not
a poster claim: 10 §2.6), #18 (06 cuts words by 22 %; the 40 % mechanism-copy test needs a count at build), #19 (P1-8),
#20 (native supports of met.no and GeoTessera unsourced, 06 §11.6), #21 (P1-15), #22 (P1-13), #31 (P2-1), #34, #35 and
#44 (P0-6, P1-7, P2-2), #39 (the media pack is specified; only the demo exists, in the scratchpad), #40 and #41 (P0-8,
P1-12) and #43 (P1-4). Note on #5: its "Keep one invariant: bytes → BLAKE3 → CID" must read **record bytes** → BLAKE3 →
CID, to agree with #12 and MASTER §5.

---

## 6. Numbers that need a fresh measurement or a decision before print

| number | current values | action at build (≤ 7 days before print unless noted) |
|---|---|---|
| R1 denominators and outcomes | 15/15, 15/15, 13/16 … 0/16 | change when R1-v13 adds P1 to P3 and others; regenerate from JSON; always "of N in this suite" |
| agent-level false acceptance | none (R5) | from R5 `results.json` only (02 §19 templates) |
| M15 post-fix | 0/54 (one provider, 2 days) | re-sample by GET over more days, or state the confound |
| decision impact of M15 | 4/91 cross illustrative thresholds (critic) | pre-register thresholds; recompute from committed CSV |
| offline check time | 0.357 to 1.187 ms | one host-stated value |
| resolve latency, source re-read | 40/154 ms; 6.9 s, 1.18 MB (through proxy) | re-measure on an ordinary network (P1-16) |
| MCP tool-list tokens | 18,709 (raw, cl100k); 20,800 (re-serialized); +17,430 in-host Claude Code | one value, labelled; re-measure |
| token ratio | 5.75× (hero), 6.4× (205 facts), 9.5× (emem docs) | one value with its sample |
| cross-runtime table | 11 paths, server 213e273, 30 Sep | re-run at 8e9b401 (resolve signs a receipt and stores nothing: 09 §1.3, SPEC) |
| ecosystem versions and tool counts | 2.4.2; Dify 2.4.0/16; npm 2.4.0; Glama 16; HF 1.1.0 | re-check by API; gate 14 days (03 §8) |
| `kxjvfwpa` resolves with no warning | LIVE 30 Sep (02), 1 Oct GET (critic) | re-check: emem may add a superseded flag |
| H3 natural instance | `oj5cecci` resolves; latest NDVI `3yyaxn5d` | re-check both at build |
| programme title, session, date | LIVE 1 Oct | re-check the week of print |
| demo timing | 9.8 s (headless Chromium) | real phones (P2-2) |

---

## 7. What an adversarial workshop reviewer would still attack (ranked), and the current answer

| # | attack | current answer | weakness left | gap id |
|---|---|---|---|---|
| A1 | "Your verifier catches the mutations you designed it to catch." | R1 leave-one-out; P1 to P3 show the suite is bounded | one record, one band, self-authored, no outside run; M11 uses a non-existent scene | P0-2, P0-4j, P1-6 |
| A2 | "Your own agent kept 16 digits; you injected the rounding and set the threshold 0.0004 below." | constructed threshold disclosed | no natural rate | P1-2 |
| A3 | "With a small open model the token did worse than prose and the forged cell was acted on." | 07 §3.6 sentence | not on 06's plan | P1-3 |
| A4 | "Every trust root is your company; DNS has no DNSSEC; your README claims independent witnesses." | 10 §4.6 | README still claims it | P1-10 |
| A5 | "'Verifiable' is in your title, but the record links to ESA data by URL only." | L3 PARTIAL, "named, not hashed" | Source.hash never filled (62 `hash: None`, 0 `Some`; 10) | (emem change) |
| A6 | "Signatures prevented none of your own bugs, and the wrong records still resolve with no warning." | "the record carried what the re-read needed" (05 §8) | no superseded flag on the record or its resolve | P1-5 |
| A7 | "Your wrong-pixel bug changed no EUDR flag and most errors are 0.03." | none yet | consequence size unmeasured | P1-5 |
| A8 | "Is 162/200 a random sample of what?" | Wilson CI | frame unstated; script uncommitted | P0-9 |
| A9 | "Where are the embeddings in your title?" | none on the face | no report | P1-1 |
| A10 | "This is Sigstore / SCITT / nanopublications / ARC for EO." | 04 §7 answers | must be printed as credit | (design) |
| A11 | "18.7 k tokens of tool list, 2.1× input, same accuracy; your own docs say don't use it for one value." | 08 cost panel | number conflict (C3) | P0-4c |
| A12 | "Your raster tool still substitutes dates, and ask still prefers a place name over coordinates." | 05 F3, 07 | statuses must print as open | section 3 |
| A13 | "Is ChatGPT real? Half your documented routes fail." | manifest | unverified row; stale directories | P0-8, P1-12 |
| A14 | "Your QR makes the server sign records on every scan." | 09 site avoids it | site not hosted | P0-6 |
| A15 | "Pre-registered by whom? The prereg note came after the trials." | 07 §6 discloses | R5 must push its prereg before trial 1 | P0-2 |
| A16 | "I cannot reuse your code: no licence; your repro link is 404." | none | | P0-6 |
| A17 | "Does the poster match your accepted abstract and DOI?" | none | abstract not in repo; DOI metadata wrong | P1-14 |
| A18 | "A content address that changes when you re-sign is not a stable name for the observation." | 10 §2.5 | MASTER §4 says "stable" | P1-11 |

---

## 8. Order of work (INFERRED from the dependencies above)

1. Today: P0-1 (archive), P0-7 (email organisers), P0-8 (ChatGPT screenshot), P0-6 author steps (Pages, LICENSE, merge plan).
2. 1 to 2 Oct: claims registry with section 2's resolutions (P0-4, P0-5); R1-v13 frozen (P0-2b); user decisions on models and
   credentials (P0-2a).
3. 2 to 6 Oct: R5 Blocks P, 1, 2, 0 and the #43 lanes (P0-2, P1-4); P1-1, P1-5, P1-8 measurements (GET-only or offline).
4. 6 to 10 Oct: figures from committed data only; gates (P1-15, 09 §8); phone tests; print-shop proof (P1-18).

## 9. Sources used by the critic (retrieved 2026-10-01)

emem.dev: `GET /v1/facts/kxjvfwpa7grmfhkxoxufq5xjltq2s5syer2rzdx7odbnrxhnjzkq` (01:41:40Z),
`GET /v1/facts/oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` (CBOR, 1,115 B), `GET /v1/cells/defi.zb572.xoso.zb1ec`
(294,966 B, 209 facts), `GET /v1/log/witnesses` (01:42:20Z), `POST /mcp tools/list` (77,042 B). Planetary Computer STAC item
and search for the Keylong point (20 to 30 Sep 2026). Earth Search v1 item `S2A_43SFS_20260925_1_L2A`. Dify Marketplace
API `plugins/vortx-ai/emem`. agentic-eo.berlin `/`, `/dates/`, `/programme/posters/`, `/programme/schedule/`,
`/calls/call-for-abstract/`. EC trade portal, "Delay until December 2026 and other developments in the implementation of the
EUDR Regulation", https://trade.ec.europa.eu/access-to-markets/en/news/delay-until-december-2026-and-other-developments-implementation-eudr-regulation .
EUR-Lex (`eli/reg/2023/1115/oj/eng`, `CELEX:32025R2650`): HTTP 202, empty body. emem git: commit messages of 04b40c5,
ab5af22, 0edf574, 29a655b, 5c7787b, 8e9b401; `8e9b401:{CHANGELOG.md,README.md,docs/model.md,web/index.html,web/verify.html,
crates/emem-storage/src/lib.rs,crates/emem-api-rest/src/lib.rs}`. Repo files: `research/repro/data/v8/{crossruntime_table,
prevalence_summary}.json`, `research/repro/data/v9/rawband/{results.md,trials.jsonl}`, `research/repro/v11/out/mutation_matrix.json`,
`research/repro/v12/data/{eo_evidence_per_fact_checks.csv,case_keylong_ndvi.json}`, `research/v13/ecosystem_manifest.json`;
scratchpad `v8/followup-G2-two-llm-plugin-handoff/qwen_trials.jsonl`, `v8/followup-G1-pixel-audit-before-after/{prevalence.py,prevalence.csv}`.
