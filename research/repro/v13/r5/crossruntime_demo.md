# #43 cross-runtime demonstration (R5 Block 3)

Token T = `emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa`; forged T' = the same cid under the Bengaluru cell (M4). Run 2026-10-01T05:32:33Z to 2026-10-01T09:43:25Z.
Read-only on emem (resolve, GET /v1/facts, A2A resolve skill). Agent A was given T by its operator; minting tools were disallowed.

| lane | runtime / model | transport | token | fact_cid | value_verbatim | receipt sig | decision / outcome |
|---|---|---|---|---|---|---|---|
| 1 Claude as A | Claude Code CLI 2.1.286 claude-sonnet-5-5 | MCP over HTTP | T | oj5cecci | 0.4708994708994709 | True | emitted T unchanged: True |
| 2 Claude as B | Claude Code CLI 2.1.286 claude-haiku-4-5-20251001 | MCP over HTTP | T | oj5cecci | 0.4708994708994709 | True | DECLINE |
| 2 Claude as B | Claude Code CLI 2.1.286 claude-haiku-4-5-20251001 | MCP over HTTP | T' | - | - | None | DECLINE |
| 4 A2A message/send | Python urllib, JSON-RPC  | A2A | T | oj5cecci | 0.4708994708994709 | None | accepted |
| 4 A2A message/send | Python urllib, JSON-RPC  | A2A | T' | - | - | None | refused -32602 |
| 5 independent verifier | Python, blake3 + cbor2 + pynacl  | GET /v1/facts/<cid> (CBOR) + frozen attestation and log proof + committed COG window | T | oj5cecci | 0.4708994708994709 | None | accepted |
| 5 independent verifier | Python, blake3 + cbor2 + pynacl  | GET /v1/facts/<cid> (CBOR) + frozen attestation and log proof + committed COG window | T' | oj5cecci | 0.4708994708994709 | None | refused binding |
| 2 Claude as B | Claude Code CLI 2.1.286 claude-haiku-4-5-20251001 | MCP over HTTP | T | oj5cecci | 0.4708994708994709 | True | DECLINE |
| 2 Claude as B | Claude Code CLI 2.1.286 claude-haiku-4-5-20251001 | MCP over HTTP | T' | - | - | None | DECLINE |
| 2 Claude as B | Claude Code CLI 2.1.286 claude-haiku-4-5-20251001 | MCP over HTTP | T | oj5cecci | 0.4708994708994709 | True | DECLINE |
| 2 Claude as B | Claude Code CLI 2.1.286 claude-haiku-4-5-20251001 | MCP over HTTP | T' | - | - | None | DECLINE |
| 3 Qwen as B | llama-cpp-python 0.3.35, CPU Qwen2.5-7B-Instruct Q4_K_M | harness tool loop; call via official MCP Python SDK 2.2.0 (streamable HTTP) | T | oj5cecci | 0.4708994708994709 | True | IRRIGATE |
| 3 Qwen as B | llama-cpp-python 0.3.35, CPU Qwen2.5-7B-Instruct Q4_K_M | harness tool loop; call via official MCP Python SDK 2.2.0 (streamable HTTP) | T' | oj5cecci | 0.4708994708994709 | True | IRRIGATE |

Distinct cids for T across lanes: ['oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa']; distinct values: ['0.4708994708994709'].
Forged T' refused by lane: {'2 Claude as B': True, '4 A2A message/send': True, '5 independent verifier': True, '3 Qwen as B': False}.
Total CLI-reported cost: $0.12576.

- Lane 2 (haiku, instructed to resolve and bind cell, band and date): the genuine token T resolved to the right cid and value in 3/3 runs but B answered DECLINE in 3/3, because the live resolve body carries the signing time and no scene date, so B could not confirm the 25 Sep date it was told to check. T' was refused by the server (isError) and B declined in 3/3 runs.
- Lane 3 (Qwen2.5-7B) T: sent `emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` (intact: True); server isError False; resolved cid oj5cecci, value 0.4708994708994709; decision IRRIGATE (wrong: 0.4709 > 0.4705 is HOLD).
- Lane 3 (Qwen2.5-7B) T': sent `defi.zb493.xuqA.zcb5f:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` (intact: False); server isError False; resolved cid oj5cecci, value 0.4708994708994709; decision IRRIGATE (the relabelled reference was NOT refused: Qwen dropped the emem:fact: prefix, the server resolved the remainder without error, and Qwen acted on it for the wrong field).

Not demonstrated: ChatGPT and Dify (need interactive accounts). Lane 5's source check uses the committed 25 Sep COG
window (research/repro/data/v8/pixel_windows.json), not a fresh COG read.
