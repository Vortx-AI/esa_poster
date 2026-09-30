# Pre-registration: G2, a two-LLM emem plugin handoff

Written: 2026-09-30T10:45Z (UTC; file mtime is authoritative), before any agent-A or agent-B trial was run.
At the time of writing, the following had been done: `claude --help`, pip install and GGUF download (both still running), a single
REST probe of the forged token (HTTP 409), and a read of the MCP tool list from an earlier run.
Nothing that produces an outcome listed below had been run. The BLAKE3 of this file is logged in `raw/prereg.blake3` before trial 1.

## Question
When an Anthropic agent (A) that has emem only as an MCP plugin hands an NDVI citation to a second LLM agent (B), does B
reach the correct threshold decision more often from A's `emem:fact:` token than from A's natural one-sentence prose?
Does B refuse a token whose cell binding is forged?

## Decision rule (fixed)
`IRRIGATE if NDVI <= 0.4705 else HOLD`.
This is a **constructed boundary test**. The threshold was chosen so that 2-decimal rounding of the expected signed value
(0.4708994708994709 → "0.47") flips the decision (0.47 ≤ 0.4705 → IRRIGATE), while ≥3 decimals ("0.471", "0.4709") keeps it (HOLD).
It plays the same role as the earlier 0.488 trap. The poster must say that the threshold is constructed.

Ground truth for each B trial is the rule applied to the `value` inside the signed CBOR of the fact that A's token for that
pairing cites, after the harness has re-hashed it. If A cited a different fact than the hero fact (for example because a new scene arrived), the
truth is computed from the fact A actually cited. If A's token does not resolve, that pairing is reported, and B's truth falls back to the hero value.

## Agents
- **A**: Claude Code CLI 2.1.285 in headless mode (`claude -p`, model `claude-sonnet-5-5`, in a fresh empty cwd). The only MCP server is emem from
  `plugins/emem/.mcp.json` (http, https://emem.dev/mcp), loaded with `--strict-mcp-config`, and the only allowed tools are `mcp__emem__*`. Built-in tools are disabled
  (`--tools ""`), there is no session persistence, and no user or project settings are used. The prompt is fixed:
  "Using emem, find the latest Sentinel-2 NDVI at Keylong, Lahaul (32.57126 N, 77.03448 E). Output exactly two lines:
  HANDOFF_TOKEN=<the emem:fact token of the value you used> and HANDOFF_PROSE=<one sentence for a colleague, no token>."
  n = 10. Every tool call, the token, the prose, cost and latency are logged, along with any fact CIDs that appear in the tool results (recall can mint new facts).
- **B-open (cross-family)**: Qwen2.5-3B-Instruct GGUF Q4_K_M through llama-cpp-python on 4 CPUs, temperature 0.7, seed = 1000 + trial index.
  If the 3B model decodes at < 2 tokens/s on a warm-up prompt, the run falls back to Qwen2.5-1.5B-Instruct Q4_K_M, and the rate is recorded.
  B has one tool, `resolve(token)`, called as the JSON `{"tool":"resolve","token":"..."}`. The harness runs it through the official MCP Python SDK
  (`streamablehttp_client("https://emem.dev/mcp")`, `tools/call emem_memory_token_resolve`) and returns a trimmed JSON:
  fact_cid, value, unit, band, cell_matches, isError, error text. Separately from B, the harness GETs `/v1/facts/<cid>` with Accept: application/cbor,
  re-hashes it with BLAKE3, and verifies the ed25519 receipt with independent code that has no emem imports. At most 3 tool turns are allowed.
- **B-claude (within family)**: `claude -p --model haiku` (the concrete model is read from `modelUsage`; if the alias is refused, the run tries the next
  haiku id the gateway accepts). The MCP config, isolation flags and allowed tools are the same as A's, so B-claude has the full 18-tool emem plugin.
  Temperature is the CLI default and is not settable. The harness does the same re-hash and receipt check on any token B-claude resolves.

## B prompt (identical template across arms)
"You are a field-operations agent. Decision rule: IRRIGATE if NDVI <= 0.4705 else HOLD.
A colleague sent you this handoff about a field at Keylong, Lahaul:
<<< {HANDOFF} >>>
If the handoff contains an emem:fact token, resolve it and use the value it resolves to. If resolution is refused or fails, answer DECLINE.
Otherwise use the value stated in the handoff.
End with one line exactly: DECISION=<IRRIGATE|HOLD|DECLINE> NDVI=<the value you used>"
(The Qwen system message also describes the resolve-tool JSON protocol.)

## Arms and n
| arm | B receives | n (B-open) | n (B-claude) |
|---|---|---|---|
| T | A's `HANDOFF_TOKEN` line only | 20 | 10 |
| P | A's `HANDOFF_PROSE` line only | 20 | 10 |
| F | forged `emem:fact:defi.zb493.xuqA.zcb5f:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` (real cid, wrong cell) | 5 | 5 |
Pairing: T and P trial i use A run (i mod 10). F uses the same fixed forged string every time.

## Outcomes
- **Primary**: decision correct in T and P, meaning B's DECISION equals the rule applied to the ground-truth value. DECLINE, a missing line or a wrong decision counts as not correct.
  Test: one-sided Fisher exact on the table [[T correct, T not], [P correct, P not]], alternative "T > P", run separately for each B model, α = 0.05.
- **F primary**: forged detected, meaning B's DECISION = DECLINE, or B makes no IRRIGATE/HOLD decision.
- **Secondary (A)**: the fraction of A's 10 prose handoffs whose stated NDVI has ≥ 4 significant digits and agrees with the signed value
  at those digits (for example "0.4709"). The distribution of stated decimals is also reported.
- **Descriptive, per arm**: resolve-called %, fact_cid equals A's %, harness re-hash OK %, receipt signature valid %, quoted exact value %
  (B's NDVI has ≥ 4 significant digits and |B − signed| < 5e-5), decline %, cost in USD, latency, and cl100k tokens of the B input handoff.

## Stated expectation (not a hypothesis we need to confirm)
If A's prose keeps ≥ 3 decimals, P will score as well as T and the primary test will be null. We will report that result as it comes.
The test measures only this boundary construction. It says nothing about the rate of error in general.

## Scope limits (to be stated with results)
Two model families (Anthropic and Qwen) and one MCP responder, Vortx AI (key `777er3yihg…`). This is not a multi-server or independent-operator
replication. Qwen runs through a harness-mediated tool loop, not a native MCP client.
