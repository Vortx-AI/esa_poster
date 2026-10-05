# 03. Ecosystem integration manifest: where emem can be used today, and on what evidence

Written 2026-10-01 (CEST) for the v13 final A0. Topic: `ecosystem`. Issues #40, #41, #42, #44, #45, #46 (and #43 where
the evidence overlaps); `research/SHARED_STATE_EMEM_A0_MASTER.md` sections 16 and 17. Read-only research: nothing in
emem, on the board or in any registry was changed. Nothing was signed or published. No emem write endpoint and no
`tools/call` was used.

Machine-readable twin: `research/v13/ecosystem_manifest.json` (a JSON array of 38 rows; each row has `id`,
`poster_group`, `platform`, `mechanism`, `url`, `status`, `evidence_level`, `evidence[]`, `user_can`, `verified_utc`,
`caveats[]`, `print`, `brand`). Generator (scratch, not committed):
`/tmp/claude-0/-home-user-esa-poster/0db6b3ad-8059-51a6-bd74-2d7a97faf986/scratchpad/eco/build_manifest.py`.

Verification window: 2026-09-30T23:10Z to 23:40Z (2026-10-01 01:10 to 01:40 CEST). emem source read at
`origin/main` 18adb67; the live server reports `x-emem-commit: 8e9b401c` (GitHub `main` head, 7 commits later; between
them the only ecosystem file that changed is `integrations/chatgpt/tools.md`, `git diff --stat 18adb67 8e9b401c`).

Labels on every item:

- **MEASURED**: run in this session (command and output given).
- **LIVE**: fetched from a live public service in this session (URL, HTTP status, field).
- **SPEC**: what emem's files or a platform's docs say, not exercised here (file:line or URL).
- **INFERRED**: my reading of the above.
- **UNVERIFIED**: claimed by a source I could not check.

Status vocabulary (closed set, SHARED_STATE §17 plus two the task adds):

| status | meaning on the poster |
|---|---|
| LIVE | a person can do this today; confirmed end to end or at connection level, or by the platform's own API |
| PROTOCOL | an open protocol surface emem serves; any compliant client can use it; the client itself was not run here |
| REGISTRY | a listing in a third-party directory or registry. A listing is not an integration |
| EXAMPLE | example code in the emem repo, checked against live emem at connection level (tool list) |
| EXPERIMENTAL | in the repo or documented, but unpublished, or not working as documented |
| ROADMAP | planned only |
| NOT FOUND | requested or claimed, absent where it would have to be |

---

## 0. Findings in one screen

1. **The protocol surfaces hold up under independent checks.** MCP `initialize` + `tools/list` at `https://emem.dev/mcp`
   returned 18 annotated tools in one page (77,038 bytes, `nextCursor: null`, no session id); `/mcp/full` pages
   114 tools over 8 pages (335,788 bytes). The A2A agent card's detached JWS verified under my own RFC 8785
   canonicalizer and Ed25519 check, and a one-field tamper was rejected. A fact fetched by CID re-hashed to its own CID.
   All MEASURED.
2. **Four client routes were run here and connected:** Claude Code 2.1.286 (`claude mcp list`: "√ Connected"), the
   Claude Code plugin (marketplace add + install: 19 skills, 1 MCP server, about 3,672 always-on tokens per session),
   Gemini CLI 0.62.0 (`gemini mcp list`: "✓ ... Connected"), and six of seven framework clients at tool-list level
   (18 tools each). As written, four examples list tools cleanly (LlamaIndex, AutoGen, CrewAI, Mastra via its
   package.json); Agno needs `fastmcp`, which its README omits; LangChain needs a one-line API fix. MEASURED.
3. **Three documented routes fail as written.** (a) emem's Gemini command `gemini extensions install
   https://emem.dev/gemini-extension.json` fails: "Failed to clone Git repository". (b) The Semantic Kernel example
   fails to load the plugin: one tool (`emem_echo_verify.claimed_value`, JSON-Schema type `["string","number"]`) breaks
   SK 1.44.1's parameter model. (c) The LangChain example uses an API removed in langchain-mcp-adapters 0.1.0.
   MEASURED. A fourth, Cline, is INFERRED to fail: the shipped config omits `type`, Cline then defaults to SSE, and
   emem answers SSE with 405.
4. **ChatGPT cannot be confirmed from outside.** The directory URL
   `https://chatgpt.com/plugins/plugin_asdk_app_6a6a0832a59081918b19aec0ddf9ec77` returns 403 (a JavaScript
   challenge) to curl and WebFetch, as does `chatgpt.com/apps`. The only evidence is emem's own site. It needs a
   logged-in phone screenshot before print. UNVERIFIED.
5. **Claude has no directory listing.** emem is not in Anthropic's official plugin directory (0 of 315 entries in
   `anthropics/claude-plugins-official`) nor in the Claude connectors directory (the submission form was deprecated,
   `docs/registries/anthropic-claude-connectors-submission.md:3-4`). The Claude routes are emem's own plugin
   marketplace, `claude mcp add`, and a custom connector. LIVE + SPEC.
   *Update, 5 Oct 2026.* The authors' listing screenshot of 4 Oct (issue #58,
   `evidence/listings/claude.png`) shows the plugin in the Claude apps' Anthropic Directory: "emem · from Anthropic
   Directory · 2.4.2 · 19 skills", with the emem connector. Claude Code's catalogue,
   `anthropics/claude-plugins-official`, still lists 315 plugins and none is emem (re-fetched 2026-10-05T05:53Z,
   `evidence/ecosystem/cpo_market_2026-10-05.json`). The manifest row `claude-connectors-directory` now records the
   directory listing (REGISTRY); points 4 and 5 above are as of 1 Oct. The ChatGPT listing of point 4 was confirmed
   by the authors' screenshot of 4 Oct (`evidence/listings/chatgpt.png`).
6. **Registries list emem; most are behind the server.** Official MCP Registry and GitHub MCP Registry: 2.4.2,
   `isLatest: true`. Dify: 2.4.0 with 16 tools. Glama: graded A on a 16-tool scan of 2026-09-09. Smithery: 16 tools,
   behind a gateway that needs a Smithery token. npm SDK: 2.4.0. Hugging Face Space: runs emem 1.1.0. One server,
   four advertised versions, three tool counts. LIVE.
7. **That drift is the poster's own argument, seen in the ecosystem.** Every directory entry is a copy of what the
   server said when the copy was taken, and each copy went stale on its own (section 4). emem's own history has
   the same bug, fixed and then recurring: `ai-plugin.json`, the SDK version constants, the PR-status table
   (4 of 7 rows wrong) and the Dify version lag. INFERRED from MEASURED and SPEC items.
8. **Brand rules push toward names in type, not logos.** Only GitHub (black or white required) and Dify (mono
   "when layout demands") clearly allow monochrome marks. VS Code, LF Projects (MCP, A2A), Anthropic and Google do
   not allow colour changes, or need permission for this use. OpenAI's page was unreadable (403). Section 6.
9. **Name collisions to avoid in print:** PyPI `emem` and npm `emem` are unrelated projects. Print
   `pip install ememdev` and `npm i @vortxai/emem`. LIVE.

---

## 1. The manifest (38 rows; full evidence in the JSON)

Grouped as issue #40 asks. "Print" gives the text the poster can carry. Where a row says "no", the surface should stay
off the board.

### 1.1 LIVE CLIENT INTEGRATIONS (agent hosts and editors)

| platform | exact mechanism | most specific URL | status | evidence (label) | caveat | print |
|---|---|---|---|---|---|---|
| **ChatGPT** (@emem) | ChatGPT Directory plugin over `https://emem.dev/mcp`; 18 core tools (`integrations/chatgpt/README.md`) | https://chatgpt.com/plugins/plugin_asdk_app_6a6a0832a59081918b19aec0ddf9ec77 | LIVE (claimed) | UNVERIFIED: 403 "Enable JavaScript" to curl and WebFetch; generic `chatgpt.com/apps` also 403. SPEC: emem `README.md:127,135`, `web/index.html:1009` (`"listed": "2026-09-27"`); vortx.ai: "Listed in ChatGPT". LIVE: same URL pattern belongs to other directory apps (search results: ElevenLabs, Quizlet) | Needs a logged-in human check before print. OpenAI plugin guidelines forbid "a generic executor to enable operations not individually exposed for review", and emem's `initialize` says `tools/call` runs any of 114 tools. Never print "114 tools in ChatGPT" | yes, after the manual check: "ChatGPT: @emem (ChatGPT Directory)" |
| **Claude Code** (MCP) | `claude mcp add --transport http emem https://emem.dev/mcp` | https://github.com/Vortx-AI/emem#quickstart | LIVE | MEASURED: Claude Code 2.1.286, isolated HOME: "Added HTTP MCP server emem"; `claude mcp list` → "emem: https://emem.dev/mcp (HTTP) - √ Connected" | connection only; no model turn | yes |
| **Claude Code plugin** | `/plugin marketplace add Vortx-AI/emem`, then `/plugin install emem@emem` (`.claude-plugin/marketplace.json`, `plugins/emem/`) | https://github.com/Vortx-AI/emem/tree/main/plugins/emem | LIVE | MEASURED: marketplace cloned + validated; `emem@emem` 2.4.2 installed, enabled; `claude plugin details`: Skills (19), MCP servers (1), always-on ~3,672 tokens | emem's own marketplace, not Anthropic's directory (0 of 315). Print the token cost if printed at all | yes: "Claude Code plugin: /plugin marketplace add Vortx-AI/emem" |
| **Claude.ai / Claude Desktop** | custom connector URL `https://emem.dev/mcp`; `examples/claude-desktop.json` | https://emem.dev/mcp | PROTOCOL | SPEC: `docs/mcp-directory.md` (Add custom connector); LIVE: endpoint passes initialize + tools/list | not run in claude.ai; enterprise orgs may block non-directory connectors | yes: "Claude.ai: add https://emem.dev/mcp as a custom connector" |
| Claude connectors directory | directory submission (Team/Enterprise admin portal) | https://claude.ai/admin-settings/directory/submissions/new | NOT FOUND | SPEC: previous form "deprecated ... now closed" (`anthropic-claude-connectors-submission.md:3-4`) | | no |
| **Dify Marketplace** | tool plugin `vortx-ai/emem`, Dify ≥ 1.9.0 | https://marketplace.dify.ai/plugin/vortx-ai/emem | LIVE | LIVE: page 200 "emem - Dify Marketplace"; API `status: active`, `latest_version: 2.4.0` (2026-09-13), `authorized_category: community`, `install_count: 32`, 16 tools; template "emem Referent Lock Lite" 200 | not run inside Dify; 2.4.0 / 16 tools vs live 2.4.2 / 18; "community" is not a Dify endorsement; plugin source is outside the emem repo | yes: "Dify: Marketplace plugin vortx-ai/emem" |
| **Gemini CLI** | `gemini mcp add --transport http emem https://emem.dev/mcp` | https://emem.dev/mcp | LIVE | MEASURED: Gemini CLI 0.62.0: "MCP server "emem" added ... (http)"; `gemini mcp list` → "✓ emem: https://emem.dev/mcp (http) - Connected". MEASURED: emem's documented `gemini extensions install https://emem.dev/gemini-extension.json` → "Failed to clone Git repository ... fatal: repository ... not found" | print only the `mcp add` form. `examples/gemini-extension.json` says 1.1.0 and "113 MCP tools"; the served copy says 2.4.2 and 114 | yes: `gemini mcp add --transport http emem https://emem.dev/mcp` |
| **Visual Studio Code** | install link → `vscode:mcp/install?{...}`; `code --add-mcp`; `.vscode/mcp.json` key `servers`; `@mcp` gallery (backed by the GitHub MCP Registry) | https://insiders.vscode.dev/redirect/mcp/install?name=emem&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Femem.dev%2Fmcp%22%7D | PROTOCOL | LIVE: link → 302 `vscode:mcp/install?{"type":"http","url":"https://emem.dev/mcp","name":"emem"}`; SPEC: VS Code docs (`@mcp`, `--add-mcp`, `servers`) | no VS Code here; no icon (brand rules) | yes: "Visual Studio Code: @mcp emem" |
| **Cursor** | deeplink `cursor://anysphere.cursor-deeplink/mcp/install?name=emem&config=eyJ1cmwiOiJodHRwczovL2VtZW0uZGV2L21jcCJ9`; web form `cursor.com/install-mcp` | https://cursor.com/install-mcp?name=emem&config=eyJ1cmwiOiJodHRwczovL2VtZW0uZGV2L21jcCJ9 | PROTOCOL | MEASURED: config decodes to `{"url":"https://emem.dev/mcp"}` (Cursor's documented format); LIVE: `/en/install-mcp` → 308 to `/install-mcp` | not run; use the https link in a QR, not `cursor://` | yes |
| **Cline** | MCP settings JSON; working form needs `"type": "streamableHttp"` | https://github.com/Vortx-AI/emem/blob/main/examples/cline.mcp.json | EXPERIMENTAL | SPEC: example has no `type`, and `autoApprove` names like `emem.recall` that are not tool names. LIVE: Cline docs: "Omitting it defaults to the legacy sse transport". MEASURED: SSE GET on `/mcp` → 405. LIVE: Cline marketplace API 199 entries, 0 emem; `cline/mcp-marketplace#1605` open since 2026-05-18, 0 comments | INFERRED failure; fix the example first | only with corrected config |

### 1.2 PROTOCOL / DISCOVERY SURFACES

| platform | mechanism | URL | status | evidence (label) | caveat | print |
|---|---|---|---|---|---|---|
| **MCP** `/mcp` | Streamable HTTP, JSON-RPC over POST, stateless, no key | https://emem.dev/mcp | PROTOCOL | MEASURED: initialize 200, `protocolVersion 2025-11-25`, `serverInfo emem 2.4.2`, no `mcp-session-id`; `notifications/initialized` 202; `tools/list` 18 tools, `nextCursor null`, 77,038 B, annotations on all (readOnlyHint 9 true / 9 false, destructiveHint false on 18); SSE GET 405 | `server.json` says "about 64 KB"; measured 77,038 B | yes |
| MCP `/mcp/full` | same, paged | https://emem.dev/mcp/full | PROTOCOL | MEASURED: 8 pages (13,17,14,12,14,25,11,8) = 114 distinct, 335,788 B | `server.json` says 7 pages, ~290 KB | 30 cm only |
| **A2A** | agent card, A2A `protocolVersion 1.0`, JSON-RPC at `/a2a/tasks`; detached JWS (EdDSA, JCS) | https://emem.dev/.well-known/agent-card.json | PROTOCOL | LIVE: 200, 15,165 B, version 2.4.2, 18 skills, 8 additionalInterfaces. MEASURED: JWS valid under my RFC 8785 + Ed25519 check against `/.well-known/jwks.json`; tampered card rejected; kid = JWK x = card pubkey = `/.well-known/emem.json` pubkey = first `did:web:emem.dev` key. MEASURED earlier (`research/repro/data/v8/crossruntime_table.json`, 2026-09-30T08:40Z): `message/send` resolved the Keylong token 3/3 | message/send not re-run (it writes a signed task artifact). Card signing as served dates from ab5af22, after 18adb67. Key agreement is self-consistency (cryptographic trust), not third-party operator attestation (source trust) | yes |
| **Official MCP Registry** | `server.json` under `io.github.Vortx-AI/emem` | https://registry.modelcontextprotocol.io/v0.1/servers/io.github.Vortx-AI%2Femem/versions/latest | REGISTRY | LIVE: 16 versions, 0.0.2 (2026-04-28T13:30:52Z) to 2.4.2 (2026-09-29T18:47:27Z, `status: active`, `isLatest: true`); remote `streamable-http https://emem.dev/mcp`; package `oci ghcr.io/vortx-ai/emem:latest` | no human page; the API URL is the most specific | yes: "Official MCP Registry: io.github.Vortx-AI/emem" |
| **GitHub MCP Registry** | GitHub's registry; backs VS Code `@mcp` | https://github.com/mcp/Vortx-AI/emem | REGISTRY | LIVE: `api.mcp.github.com/v0.1/servers/io.github.Vortx-AI%2Femem/versions/latest` 200, version 2.4.2, `isLatest: true`, `stargazerCount: 63` | HTML page not reachable from this session (proxy); URL from `/.well-known/mcp.json` `registries[0]` | yes |
| **GitHub** | Apache-2.0 source | https://github.com/Vortx-AI/emem | LIVE | LIVE (GitHub MCP): created 2026-04-24, pushed 2026-09-30T21:11:14Z, 63 stars, 9 forks, 0 open issues; linguist language "HTML" | do not quote the linguist label; stars only with timestamp | yes |
| **Glama** | directory listing claimed via `glama.json` | https://glama.ai/mcp/servers/Vortx-AI/emem | REGISTRY | LIVE: 200 "emem by Vortx-AI \| Glama"; "Knowledge & Memory", "Location Services", "Remote"; badge title "emem – MCP server rated A on Glama"; payload `scoredAt 2026-09-09T18:51:25Z`, `scoredToolCount 16` | grade predates 2.4.2 | yes: "Glama: listed" |
| Smithery | listing + Smithery gateway `emem--vortxai.run.tools` | https://smithery.ai/servers/vortxai/emem | REGISTRY | LIVE: 200; registry API `remote: true`, 16 tools. MEASURED: gateway POST → 401 "Missing Authorization header" | Smithery route needs a Smithery token; the direct route needs none | optional, no |
| Hugging Face Space | Docker Space | https://huggingface.co/spaces/vortx-ai/emem | REGISTRY | MEASURED: `initialize` on `vortx-ai-emem.hf.space/mcp` → `serverInfo 1.1.0`; API `RUNNING`, lastModified 2026-07-17 | stale mirror | no |
| Context7 | docs index `/vortx-ai/emem` | https://context7.com/vortx-ai/emem | REGISTRY | LIVE: 200 "emem (vortx-ai/emem) \| Context7" | | no |
| MuleSoft Exchange | asset "Vortx AI MCP Server" | https://anypoint.mulesoft.com/exchange/68e53915-e89b-4e82-b794-12d37982db4c/vortxAi-asset/ | REGISTRY | LIVE: 200, title "Vortx AI MCP Server"; SPEC (emem site): "mcp 2.0.0" | contents not inspected | no |
| awesome-mcp-servers | README entry | https://github.com/punkpeye/awesome-mcp-servers | REGISTRY | LIVE: raw README line 2961 lists Vortx-AI/emem | | no |
| emem integration landing | homepage section `#use` (surfaces JSON, `web/index.html:1009`) | https://emem.dev/#use | LIVE | LIVE: homepage 200 with `id="use"` and `id="surfaces"`; `/integrations` returns text/markdown; `/docs/integrations.html` mentions ChatGPT 0 and A2A 0 times | not mobile-tested; labels in the surfaces JSON are stale ("pypi 2.4.0") | QR target (section 7) |

### 1.3 SDK / API

| platform | mechanism | URL | status | evidence (label) | caveat | print |
|---|---|---|---|---|---|---|
| **Python SDK** | `pip install ememdev` | https://pypi.org/project/ememdev/ | LIVE | LIVE: PyPI 2.4.2, uploaded 2026-09-29T19:42:00Z, 14 releases, Apache-2.0. MEASURED: clean-venv install, `__version__ 2.4.2`. MEASURED earlier: resolve + offline receipt verify 3/3 | PyPI `emem` is an unrelated project (Automatika Robotics 0.3.0, MIT) | yes: `pip install ememdev` |
| **TypeScript SDK** | `npm i @vortxai/emem` | https://www.npmjs.com/package/@vortxai/emem | LIVE | LIVE: npm latest 2.4.0 (2026-09-09T07:45:11Z), 9 versions. MEASURED: exports Client, EmemError, EmemHTTPError, VERSION "2.4.0" | repo says 2.4.2; npm `emem` is unrelated (2021) | yes |
| **REST / OpenAPI** | `https://emem.dev/v1/*` | https://emem.dev/openapi.json | PROTOCOL | LIVE: 200, OpenAPI 3.1.0, 188 paths / 206 operations, 375,360 B; action subset 38 paths / 39 operations. MEASURED: `GET /v1/facts/oj5ceccile62...` CBOR 1,115 B re-hashes (BLAKE3, base32) to the same CID | | yes |
| Custom GPT Action | import `/openapi.action.json` | https://emem.dev/openapi.action.json | PROTOCOL | LIVE: 200, 121,037 B | `docs/agents.md` Connect table still says `/openapi.json` | fold into REST |
| **Docker** | `docker run -p 5051:5051 ghcr.io/vortx-ai/emem:latest` | https://github.com/Vortx-AI/emem/pkgs/container/emem | LIVE | MEASURED: anonymous GHCR token; `:latest`, `:v2.4.2`, `:2.4.2` OCI index 200; linux/amd64 + linux/arm64; `:latest` built 2026-09-30T21:43:52Z; label `io.modelcontextprotocol.server.name=io.github.Vortx-AI/emem`; ports 443, 5051; amd64 865.0 MB compressed; `emem-encode`, `emem-airgap` images 200 | container not run (no daemon) | yes |
| emem-langmem | LangGraph `BaseStore` | https://pypi.org/project/emem-langmem/ | LIVE | LIVE: PyPI 2.4.2; langchain-ai/docs `integration_external_docs.yaml`: 0 matches for emem | a package, not a LangChain listing | fold into LangChain |
| llama-index-tools-emem | `sdks/llama-index-tools-emem` | https://github.com/Vortx-AI/emem/tree/main/sdks/llama-index-tools-emem | EXPERIMENTAL | LIVE: PyPI 404; not in run-llama/llama_index (404); its README says `pip install llama-index-tools-emem` | unpublished | no |
| n8n node | `integrations/n8n` | https://github.com/Vortx-AI/emem/tree/main/integrations/n8n | EXPERIMENTAL | LIVE: npm `n8n-nodes-emem` 404 | | no |

### 1.4 FRAMEWORKS (examples in the emem repo; each run with its own client class up to the tool list, no LLM)

| framework | client in the example | URL | status | MEASURED result | caveat | print |
|---|---|---|---|---|---|---|
| **LlamaIndex** | `BasicMCPClient` + `McpToolSpec` | https://github.com/Vortx-AI/emem/tree/main/examples/llamaindex | EXAMPLE | llama-index-tools-mcp 0.4.8 → 18 tools | needs an OpenAI key to run the agent | yes |
| **AutoGen** | `McpWorkbench(StreamableHttpServerParams)` | .../examples/autogen | EXAMPLE | autogen-ext 0.7.5 → 18 tools | | yes |
| **Agno** | `MCPTools(url, transport="streamable-http")` | .../examples/agno | EXAMPLE | agno 3.0.11 + fastmcp 4.0.10 + mcp 2.2.0 → 18 tools; with agno + mcp only: ImportError asking for `fastmcp>=4.0.0,<5` | README:10 installs only `agno openai`; following it fails at import | yes, once the README names fastmcp |
| **CrewAI** | `MCPServerAdapter({url, transport})` | .../examples/crewai | EXAMPLE | crewai-tools 1.15.23 → 18 tools; `emem_eudr_dds` absent | the task asks the agent to call `emem_eudr_dds` (extended tier): INFERRED it cannot. Upstream declined (`registry_claude.md:66`) | yes |
| **Mastra** | `@mastra/mcp` `MCPClient` | .../examples/mastra | EXAMPLE | pinned ^0.10.0 (0.10.12) `getTools()` → 18 (prefixed `emem_emem_*`); latest 2.1.1: "mcp.getTools is not a function", `listTools()` → 18 | works via the included package.json; README:10's unpinned `npm install @mastra/core @mastra/mcp ...` resolves to 2.1.1, where the example's call does not exist. Asks for `emem_hunt` (extended tier). Upstream declined (`registry_claude.md:67`) | yes |
| **LangChain** | `langchain_mcp_adapters.MultiServerMCPClient` | .../examples/langchain | EXAMPLE | as written: NotImplementedError "cannot be used as a context manager" (0.3.2); current API → 18 tools. Earlier: both tokens 3/3 (path 6b) | print "LangChain (MCP adapters)" only after the example is fixed, or without pointing at it | after fix |
| Semantic Kernel | `MCPStreamableHttpPlugin` | .../examples/semantic-kernel | EXPERIMENTAL | semantic-kernel 1.44.1 + mcp 1.30.0 (clean venv): ValidationError, `KernelParameterMetadata.type` given `['string','number']`, from `emem_echo_verify.claimed_value` | interop defect; plugin does not load | no |

Package versions used above: `pip list` in the scratch venvs (MEASURED).

---

## 2. The tests, as run (all MEASURED unless marked)

**MCP.** `POST https://emem.dev/mcp` with `{"method":"initialize","params":{"protocolVersion":"2025-11-25",...}}` →
200 in 0.485 s. `result.protocolVersion` = `2025-11-25`, `serverInfo` = `{"name":"emem","version":"2.4.2"}`,
capabilities include `tasks` and extension `io.modelcontextprotocol/ui`, `instructions` 4,709 characters. Response
headers carry `mcp-protocol-version: 2025-11-25` and `x-emem-commit: 8e9b401c...`, no `mcp-session-id`.
`tools/list` → 18 tools, `nextCursor: null`, 77,038 bytes, 0.88 s. `/mcp/full` page cursors `all@13`, `all@30`,
`all@44`, `all@56`, `all@70`, `all@95`, `all@106`, then null.

**A2A card.** `GET /.well-known/agent-card.json` → 200 (same bytes at `/.well-known/agent.json`). Protected header:
`{"alg":"EdDSA","jku":"https://emem.dev/.well-known/jwks.json","kid":"777er3yihgifqmv5hmc2wwmyszgddzderzhsx6rex4yoakwomvka","typ":"JOSE"}`;
unprotected header: payload = "this card as served, with `signatures` removed, canonicalized per RFC 8785". I removed
`signatures`, canonicalized with my own JCS function (keys sorted by UTF-16 code units, no whitespace), built
`protected || '.' || b64url(payload)` and verified with `cryptography` 41.0.7 Ed25519: **valid**. Changing `name` to
`emem-tampered`: **rejected**. The A2A v1.0 spec requires exactly this construction
(a2a-protocol.org/latest/specification: "The Agent Card JSON MUST be canonicalized according to RFC 8785 ... The
signatures field itself MUST be excluded"; LIVE).

**Fact by CID.** `GET /v1/facts/oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` with `Accept: application/cbor` →
1,115 bytes; `base32(blake3(bytes))` = the same CID. Record: `indices.ndvi` 0.4708994708994709 at
`defi.zb572.xoso.zb1ec`, tslot 20721, source Sentinel-2A L2A tile T43SFS 2026-09-25 (B08 and B04 URLs),
`fn_key sentinel2_l2a_indices_ndvi@1`. This is the token of the v8 cross-runtime table, still resolving 2 days later.

**Registries and packages.** Commands: `curl` of the registry, PyPI JSON, npm registry, Dify marketplace, Glama,
Smithery and Hugging Face APIs listed per row in the JSON. GHCR: `GET https://ghcr.io/token?scope=repository:vortx-ai/emem:pull`
(anonymous), then `HEAD /v2/vortx-ai/emem/manifests/<tag>` and the amd64 config blob.

**Hosts.** In isolated `HOME` directories under the scratchpad (no real config touched):
`claude mcp add --scope user --transport http emem https://emem.dev/mcp; claude mcp list`;
`claude plugin marketplace add Vortx-AI/emem; claude plugin install emem@emem; claude plugin details emem@emem`;
`npx @google/gemini-cli@0.62.0 extensions install https://emem.dev/gemini-extension.json --consent` (fails) and
`... mcp add --scope user --transport http emem https://emem.dev/mcp; ... mcp list` (connected).

**Frameworks.** One script (`scratchpad/eco/fw/fwtest.py`) and two single-framework scripts reproduce each example's
client construction and stop at the tool list. Mastra via `node` with `@mastra/mcp` 0.10.12 and 2.1.1.

What was not run, on purpose: any `tools/call`, A2A `message/send`, `/v1/recall`, `/v1/ask` (they sign and store),
Docker `run`, and any GUI host (ChatGPT, claude.ai, Dify workspace, VS Code, Cursor, Cline).

---

## 3. Same evidence, different runtimes (issue #43): what exists and what does not

- MEASURED earlier (`research/repro/data/v8/crossruntime_table.json`, generated 2026-09-30T08:40:43Z, server
  213e273, 3 repetitions): the Keylong NDVI token and the Bengaluru elevation token each resolved through 11 paths
  (raw REST, raw MCP JSON-RPC, A2A `message/send`, Python SDK 2.4.2, TypeScript SDK 2.4.0, LlamaIndex FunctionTool,
  langchain-mcp-adapters, official MCP Python and TypeScript SDKs, an independent blake3+cbor2 decoder, and an
  A to B handoff between isolated processes). One CID and one value per token on every path; `rehash_ok` on all.
- MEASURED today: the same endpoint connects from Claude Code and Gemini CLI, and six framework clients list its
  18 tools (Semantic Kernel does not load them). The Keylong CID still re-hashes.
- NOT DONE: a model-in-the-loop run in two named agent hosts (for example Claude Code and Gemini CLI, or Claude and
  Dify) where host A cites the token and host B resolves and re-hashes it. Both CLIs are installable here, so this is
  the cheapest honest #43 demonstration; it needs model credentials and one signed `memory_token_resolve` call per
  host, which is a decision for the experiment task (#9), not for this read-only report.

Poster wording that the evidence supports now: "One token, eleven client paths, one CID (30 Sep 2026)". Wording it
does not support yet: "resolved in ChatGPT and Claude".

---

## 4. Ecosystem drift: the poster's failure mode, in emem's own distribution

The user's point: an error emem has had, and fixed, is one other multi-agent systems will have. The ecosystem
checks above show the same failure the poster is about, one level up. A listing is a copy of what the server said
at copy time. Each copy drifted.

| surface (who copied) | version it shows | tools it shows | as of | label |
|---|---|---|---|---|
| live `/mcp` (`x-emem-commit 8e9b401c`) | 2.4.2 | 18 listed, 114 callable | 2026-09-30T23:12Z | MEASURED |
| A2A card | 2.4.2 | 18 skills (117 on 2026-09-30T08:40Z at 213e273) | same | MEASURED |
| Official MCP Registry, GitHub MCP Registry | 2.4.2 | (none) | published 2026-09-29T18:47Z | LIVE |
| PyPI `ememdev`, `emem-langmem`; GHCR `:v2.4.2`; Claude plugin | 2.4.2 | plugin: 19 skills | 2026-09-29 | LIVE / MEASURED |
| npm `@vortxai/emem` | 2.4.0 | | 2026-09-09 | LIVE |
| Dify Marketplace | 2.4.0 | 16 | 2026-09-13 | LIVE |
| Glama grade | (payload string 2.4.0) | 16 | scanned 2026-09-09 | LIVE |
| Smithery | | 16 | | LIVE |
| MuleSoft Exchange (per emem's own site) | 2.0.0 | | 2026-08-13 | SPEC |
| Hugging Face Space | 1.1.0 | | modified 2026-07-17 | MEASURED |
| `examples/gemini-extension.json` in the repo | 1.1.0 | "113" | origin/main | SPEC |
| `server.json` prose | | "about 64 KB", "7 pages, about 290 KB" (measured 77 KB, 8 pages, 336 KB) | origin/main | SPEC vs MEASURED |

Resolved errors of the same kind in emem's own record (SPEC, file:line at 18adb67):

- `CHANGELOG.md:228-236` (2.3.0): `ai-plugin.json` pointed ChatGPT at the full 350 KB `/openapi.json`; "three surfaces
  disagreed because each was typed by hand". Fixed by generating them from the agent card. The same stale pointer
  survives in `docs/agents.md` (Connect table).
- `sdks/emem-ts/src/version.ts:6-7`: "package.json said 1.0.0, the VERSION export said 0.0.9, and the User-Agent said
  0.0.8. Nothing failed, because nothing compared them." Fixed with a CI check. npm still serves 2.4.0 against a 2.4.2
  repo.
- `registry_claude.md:99-100`: "Seven rows were checked against the actual PR pages. Four were wrong, in both
  directions". The status table was a summary of PR states, and it drifted from the PRs.
- `docs/registries/integration-targets.md:154`: "live on the marketplace at 2.2.0 while every other surface is
  2.4.0". Today Dify is at 2.4.0 while the others are at 2.4.2. The lag moved one release on without closing.
- `server.json:58`: a scanner that takes page one and stops used to get a fragment of the tool list. Fixed with an
  18-tool core page with `nextCursor: null`. Glama, Dify and Smithery still show 16: they copied before the fix.

INFERRED reading for the poster (one line, 30 cm tier at most): **a directory entry is a paraphrase of a server;
every copy here went stale on its own.** emem's own mechanism for this is a content address for the catalogue:
`/.well-known/emem-manifest.json` carries `capability_manifest_cid` (`wlj3x2id...`) with the note "A directory that
polls this and finds `capability_manifest_cid` unchanged can skip re-reading the catalogue" (LIVE). None of the
directories above uses it (INFERRED from their stale counts). It is the protocol's own argument, handoff by
reference instead of by copy, applied to its own listings. Do not overstate it: the CID was not recomputed here.

---

## 5. Numbers (issue #45): what may be printed, with source and timestamp

Printable, if printed at all (each needs a claims-map row with this source and "retrieved 2026-10-01"):

| number | value | source | label |
|---|---|---|---|
| MCP tools listed at /mcp | 18 | `tools/list` at https://emem.dev/mcp | MEASURED |
| MCP tools callable | 114 | `/mcp/full` walk; `/.well-known/emem-manifest.json` `tool_count` | MEASURED + LIVE |
| MCP protocol versions accepted | 4 (2024-11-05 to 2025-11-25) | emem-manifest `protocol_versions_supported` | LIVE |
| client paths resolving one token | 11 paths, 1 CID each | `research/repro/data/v8/crossruntime_table.json` (2026-09-30T08:40Z) | MEASURED earlier |
| Claude plugin skills / always-on tokens | 19 / ~3,672 | `claude plugin details emem@emem` (Claude Code's estimate) | MEASURED |
| framework clients that list emem's tools | 6 of 7 (4 of 7 examples exactly as written) | section 1.4 | MEASURED |
| OpenAPI operations | 206 (38 paths in the Action subset) | https://emem.dev/openapi.json | LIVE |
| Official MCP Registry versions | 16, first 2026-04-28 | registry search API | LIVE |

Do not print (vanity or unstable, #45): GitHub stars (63) and forks (9); Dify installs (32); Glama "A"; Hugging Face
likes. If the design needs one adoption signal, prefer the registry history (16 published versions since 2026-04-28),
which is a fact about the maintainers, not a popularity count.

Numbers found wrong or stale in emem's own prose (do not copy them): "about 64 KB" and "7 pages, about 290 KB"
(`server.json:58`); "113 MCP tools" and version 1.1.0 (`examples/gemini-extension.json`); "the 16 of the core loop
exposed in this app" next to "18 tools" (`integrations/chatgpt/submission.md`, Technical section); "pypi 2.4.0"
(`web/index.html:1009`, while PyPI is 2.4.2).

---

## 6. Platform marks: official guidelines and whether monochrome is allowed (issue #46)

| owner (marks) | guideline URL (retrieved 2026-10-01) | monochrome | rule that decides it | poster use |
|---|---|---|---|---|
| OpenAI (ChatGPT, Blossom) | https://openai.com/brand/ ; https://developers.openai.com/plugins/plugin-guidelines | UNVERIFIED: brand page 403 to curl and WebFetch | search snippets of the brand page: use the logo only for OpenAI services, as provided, unmodified, no implied endorsement (UNVERIFIED). Plugin guidelines (LIVE): "Plugins should not imply that they are made or endorsed by OpenAI." | text "ChatGPT" in poster type |
| Anthropic (Claude, Claude Code) | https://www.anthropic.com/legal/trademark-guidelines (effective 2024-08-01); assets: https://www.anthropic.com/press-kit | a one-color asset exists in the press kit ("Claude logo - One-color.svg", "Claude Code logo - One-color.svg"), but use needs approval | "You may only use our trademarks as specifically permitted by us and only in materials we approve beforehand." "No alterations ... (changes to color, font, proportion, or otherwise)". Contact marketing@anthropic.com | text "Claude", "Claude Code" unless approved |
| Dify | https://dify.ai/brand-guidelines | allowed: "Layout demands mono or reversed options" | appropriate uses include "a group of logos alongside other tools" and "presentations ... referencing Dify technologies"; no implied endorsement or partnership; Dify Design Kit on the page | official mono Dify mark allowed |
| LF Projects (Model Context Protocol, MCP, A2A, Agent2Agent) | https://lfprojects.org/policies/trademark-policy/ (all four names are on its marks list) | not allowed: "A logo should not be displayed with color variations" | "Do not use a LF Projects logo on posters, brochures, signs, websites, or other marketing materials to promote your events, products or services without written permission"; word marks may be used for true factual statements; "Correct: <your product name> compatible with <LF Projects mark>"; trademarks@lfprojects.org | text only: "Model Context Protocol (MCP)", "Agent2Agent (A2A)" |
| GitHub (Invertocat, wordmark) | https://brand.github.com/foundations/logo (github.com/logos → 301) | required: "white, black, or in few cases grey or green" | "Use the Invertocat logo as a social button to link to your GitHub profile or project"; no modification; no implied endorsement | black Invertocat next to the repo URL is allowed |
| Microsoft (Visual Studio Code) | https://code.visualstudio.com/brand | not allowed: blue icon, white only when contrast requires | Not OK: "Using the icon to identify or promote your own product"; "Using our icons to associate your offerings with Microsoft"; OK: "Visual Studio Code" on first instance, "<action> in VS Code" | text only |
| Anysphere (Cursor) | https://cursor.com/brand | not stated; official 2D light and dark variants provided | "Refer to us as Cursor. Not Cursor AI or Cursor Code." | text "Cursor" (safest) |
| Google (Gemini, Gemini CLI) | https://about.google/brand-resource-center/guidance/ | not without a request: product icons are "Ask first" | "You can refer to Google or our products in an informational context in plain text"; "Don't use any Google brand elements on merchandise such as shirts, mugs, posters, etc." | text only: "Gemini CLI" |

INFERRED consequence for #46: a restrained monochrome logo row is not available for most of these marks without
permission. The compliant design is typographic: platform names set in the poster's own face, a small status
glyph per name (section 7), and at most two marks (GitHub black, Dify mono). This also meets #42's "not a logo wall".

---

## 7. What the ecosystem band can say (issues #40, #42, #44), built only from rows above

Spine (issue #42): **emem signed observation → MCP · A2A → agent host → next agent**. Caption:
**One evidence protocol, multiple agent runtimes.**

Legend: ● LIVE (run or confirmed here), ○ PROTOCOL (open surface; client not run here), ▢ REGISTRY (a listing, not an
integration), △ EXAMPLE (repo code; tool list checked 2026-10-01).

- **LIVE CLIENT INTEGRATIONS**: ● Claude Code (`claude mcp add ...` or `/plugin marketplace add Vortx-AI/emem`),
  ● Gemini CLI (`gemini mcp add --transport http emem https://emem.dev/mcp`), ● Dify Marketplace plugin,
  ● ChatGPT @emem (only after the manual check; otherwise omit), ○ Claude.ai custom connector,
  ○ Visual Studio Code, ○ Cursor. Cline only once its example is fixed.
- **PROTOCOL / DISCOVERY**: ○ Model Context Protocol (MCP) `https://emem.dev/mcp`, ○ Agent2Agent (A2A) signed card,
  ▢ Official MCP Registry `io.github.Vortx-AI/emem`, ▢ GitHub MCP Registry, ● GitHub `Vortx-AI/emem`, ▢ Glama.
- **SDK / API**: ● `pip install ememdev`, ● `npm i @vortxai/emem`, ○ REST (OpenAPI 3.1), ● Docker
  `ghcr.io/vortx-ai/emem`.
- **FRAMEWORKS** △ (each through its own MCP client): LlamaIndex, AutoGen, Agno, CrewAI, Mastra, LangChain (after the
  fix). Not Semantic Kernel.
- 30 cm footnote: "Checked 2026-10-01: MCP/A2A endpoints, registries and packages by API; Claude Code and Gemini CLI
  connected; framework clients listed 18 tools. ChatGPT, claude.ai, Dify, VS Code and Cursor not run by us."

QR destinations (issue #44), mobile test still owed by a person:

| QR label | target | why this target |
|---|---|---|
| DISCOVER INTEGRATIONS | https://emem.dev/#use | the one live page that lists every route (homepage surfaces section) |
| INSPECT THE AGENT CARD | https://emem.dev/.well-known/agent-card.json | the signed A2A card (JSON on a phone) |
| FIND IT IN THE REGISTRY | https://github.com/mcp/Vortx-AI/emem | human-readable registry page |
| ADD TO CURSOR | https://cursor.com/install-mcp?name=emem&config=eyJ1cmwiOiJodHRwczovL2VtZW0uZGV2L21jcCJ9 | https form of the deeplink |
| ADD TO VS CODE | the insiders.vscode.dev redirect above | resolves to `vscode:mcp/install` |

Avoid as QR targets: `https://emem.dev/integrations` (serves text/markdown), `https://emem.dev/docs/integrations.html`
(omits ChatGPT and A2A), the Hugging Face Space (1.1.0), the Smithery gateway (needs a token).

---

## 8. CI gate proposal for issue #41 (for the build agent; nothing implemented here)

1. The board's ecosystem band is generated from `research/v13/ecosystem_manifest.json`; the build refuses any
   platform name in the band that has no row, and any row whose `print.allowed` is `false`.
2. A row prints only if its `status` is in {LIVE, PROTOCOL, REGISTRY, EXAMPLE}, and a status glyph is drawn from
   `status`, not typed.
3. `verified_utc` older than 14 days at build time fails the gate (the registries moved within days in section 4).
4. A re-check script (curl + `tools/list` + registry and package APIs, the commands of section 2) rewrites the
   `evidence` fields; a changed version or tool count fails the gate until a person accepts it.
5. Every printed ecosystem number must also appear in the claims map with the source of section 5.
6. The ChatGPT row stays `print.allowed = "only after the manual check"` until a dated screenshot sits in
   `research/v13/`.

---

## 9. Open items before print

1. A logged-in person opens the ChatGPT URL on a phone and records title, developer, status and date (screenshot).
2. Decide whether emem fixes, before print, the four broken routes (Gemini extension command, Cline config,
   LangChain example API, Semantic Kernel union type), or the poster omits them. The poster team cannot edit emem.
3. A person tests every QR target on a phone (#44).
4. If any logo is wanted beyond GitHub and Dify: written permission (LF Projects, Anthropic, Google, Microsoft) or a
   browser read of openai.com/brand.
5. The #43 two-host, model-in-the-loop handoff (section 3) belongs to the experiment task.
6. The Dify plugin (2.4.0, 16 tools, source outside the repo) and npm SDK (2.4.0) lag the server. If the poster says
   "2.4.2", it should say it only of the server and registries.
