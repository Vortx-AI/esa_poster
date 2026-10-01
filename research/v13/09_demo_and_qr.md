# 09 · The QR, demo and media layer: what a visitor's phone does with the poster

Written 2026-10-01 (UTC) for the v13 final A0. Topic: `demo`. Issues #34, #35, #39, #43, #44;
`research/SHARED_STATE_EMEM_A0_MASTER.md` §25 (QR/media), with §5, §11, §15 and §28 (questions 6 and 7) where they constrain it.

This is read-only research. In this repo, only this file was written. Nothing was signed or published. No key file was
touched. Every live call is listed in §11. All builds, screenshots and videos are in the scratchpad (paths in Appendix C).

Labels on every item:

- **MEASURED**: run in this session; the command, file or output is named.
- **LIVE**: read from a live public service in this session (URL and time).
- **SPEC**: what emem's code or docs say at `origin/main 18adb67` (file:line), or what a standard says.
- **INFERRED**: my reasoning from the above.
- **UNVERIFIED**: stated somewhere and not checked here.

Test rig (MEASURED): headless Chromium 1194 (`/opt/pw-browsers/chromium-1194`) through playwright-core 1.63.0. Viewport
390 × 844 CSS px, DPR 2, touch, Android Chrome user agent, locale en-GB, time zone Europe/Berlin. Requests went through
the container's HTTPS proxy. Harness: `scratchpad/v13/mobile/mobile.mjs`. One safety rule applied to every page:
GETs pass. POSTs to emem.dev pass only for resolve endpoints, MCP `initialize`/`tools/list` and A2A
`emem_memory_view`/`emem_memory_list*`. **Every other POST to emem.dev is aborted and logged.** This rule blocked
`/v1/recall` three times (§1). Times come from a container network, so a phone on conference Wi-Fi will differ. One run
added a throttled profile (4 Mbit/s down, 150 ms RTT). WebKit/Safari was not tested; no WebKit build is installed.

---

## 0. Findings in one screen

1. **No current QR destination shows the scientific claim on a phone.** MEASURED, at 390 × 844:
   - `emem.dev/verify` (the v12 "Check any token" QR) opens an empty composer. Its example chips mint new records by
     `POST /v1/recall` and `/v1/ask` when tapped (SPEC `web/verify.html:941-948`).
   - The ememdemo token view never shows the value, the date or the source. Its headline reads "Tokenise huge files for
     agents to use."
   - On the v12 repro QR's GitHub tree, a phone cannot run anything.
2. **A deterministic receiver demo is built, phone-tested and inside budget** (#35). It is one static HTML file of
   86,469 B, with all data inline from committed files and no emem code:
   - It shows one paraphrase **accepted unchecked**, then refuses three corruptions: **M3** one byte changed (refused
     at L0, hash), **M4** cited for another cell (refused at L1, binding), **M8** forged to 0.45 and re-hashed (refused
     at L0, signature).
   - It **accepts the genuine record (G0)**: hash, batch root, Ed25519 under the pinned key, log inclusion, witness
     co-signature and consistency, and NDVI recomputed bit-identically.
   - **It then re-reads the source pixel live from the two Sentinel-2 files.** B08 3502 and B04 1900 give
     0.4708994708994709, equal to the signed value bit for bit. The pixel 10 m south gives 0.3015512674990541 (M15).
   - Timing: done in **9.8 s** paced (unthrottled, throttled 4G or offline) and 3.4 s unpaced. All six verdicts are
     above the fold on a 390 × 844 screen. No sign-in, no key. All MEASURED.
3. **L3 (source re-read) works from a phone with public data only.** It is the check the brief calls PARTIAL, and no
   current page runs it. MEASURED:
   - The Planetary Computer SAS token endpoint answers CORS `*`.
   - Two byte-range reads (tile 413 of each file, 945,880 B together) return 206.
   - The tiles' BLAKE3 values equal the hashes the v8 trace recorded on 30 Sep.
   - The tiles decode in the browser: deflate, 15-bit samples, 512 × 512 tiles, no predictor.
   - The 5 × 5 window equals the committed `pixel_windows.json` window exactly.
4. **The record names its source files but does not hash them.** MEASURED: `sources[0]` has keys `scheme`, `id`,
   `captured_at` only. So L3 is a re-read, not a hash check. The tile hashes the demo compares come from the poster
   team's 30 Sep trace, not from the signer. This is MASTER §5 seen in the bytes, and issue #7.
5. **Three existing viewers write, or would write, on every scan.** MEASURED, with the safety rule above:
   - The emem.dev homepage (`/#use`) fires `POST /v1/recall {"place":"Lusail",…}` on load (SPEC `web/index.html:3588`).
   - The ememdemo track viewer fires `POST /v1/recall` for its cell step. With that call blocked, the sealed v11 track
     shows **"✗ ememified, with a finding · 29 of 30"** in red. With it allowed, the 07 report saw 30/30.
   - `emem.dev/demos/handoff` with an empty token box, and `/demos/signed-answer?run`, call `/v1/recall` (SPEC
     `web/demos-handoff.html:436-445`; `web/demos-signed-answer.html:418-420, 476`).
6. **Hosting:** the demo cannot be served from this repo as it stands.
   - MEASURED: `raw.githubusercontent.com` serves `.html` as `text/plain` with `CSP: sandbox`, and jsDelivr `/gh/`
     serves `text/plain`. Neither renders.
   - GitHub Pages is not enabled on `Vortx-AI/esa_poster` (API `has_pages: false`; `vortx-ai.github.io/esa_poster/` → 404).
   - `research/repro/v13` does not exist on `main` (404). The repo has no LICENSE (API `license: null`).
   - Enabling Pages and merging to `main` are author actions (§9).
7. **Final QR set (§2): six verb-led QRs, all ECC Q, version 4 (33 modules), with short payloads on the poster's own
   Pages site.**
   - **VIEW THE DEMO** is the hero: a 70 mm symbol, which scans from about 0.97 m (INFERRED model, §2.3).
   - The other five are 40 mm symbols (about 0.55 m): TRY A TOKEN, INSPECT THE RECORD, RE-RUN THE TEST, READ THE
     METHODS, DISCOVER INTEGRATIONS.
   - All six were generated and decoded back to their exact payloads (MEASURED, OpenCV 5.0.0).
   - v12's QRs have `border=0`. The white pad of 3.2 mm is about 1.7 modules, below the 4-module quiet zone of
     ISO/IEC 18004 (SPEC `poster/make_figures_v12.py:747-748`, `poster/src/poster.v12.html:43-44`).
8. **`emem.dev/verify?q=<token>` is the best existing TRY A TOKEN target.** MEASURED: 2.0 s to a result that shows the
   value, band, observed date, six check lines and the source. Four limits:
   - On a phone the result starts about 825 CSS px down, below the fold.
   - A refusal's message is cut at 220 characters (SPEC `verify.html:426`), and its red badge overflows the card at 390 px.
   - It checks the resolve receipt, not the fact's original attestation and log entry (SPEC `verify.html:550-575`).
   - It labels the result "✓ verified in this tab", the bare word MASTER §11 forbids on the board.
9. **The cross-runtime claim (#43) is measured at protocol level only.** MEASURED and committed: the same Keylong
   token resolves through 11 code paths (REST, raw MCP, A2A `message/send`, Python and TS SDKs, LlamaIndex, LangChain
   adapters, official MCP Python/TS SDKs, an independent blake3+cbor2 reader). All 3/3, with one CID and one value
   (`research/repro/data/v8/crossruntime_table.json`). No model-in-the-loop handoff between two agent hosts has been
   measured. ChatGPT and Dify were not run (03 report). The media must say so.
10. **The media pack (#39) has eight assets, all fed from one claims map through one manifest** (§7, §8):
    - A0 PDF and 300 dpi PNG;
    - 16:9 slide;
    - 20 s phone video (feasibility shown: 12.9 s, 780 × 1688, H.264, 415,914 B);
    - 60 s narrated video (159-word script, §7.5);
    - landing page;
    - 1200 × 627 social card;
    - A4 technical handout.

    The pages and redirects are built (§4). The video, social card, slide, handout and PDF are specified only.

---

## 1. What exists today, opened on a phone

### 1.1 Destination table (all MEASURED 2026-10-01 00:53–01:20 UTC, 390 × 844, unthrottled)

"Settled" means the page text was unchanged for 3 s (for ememdemo, the verdict line appeared). "Above the fold" means
the first 844 CSS px.

| # | destination | HTTP | settled | requests | what the first screen shows | use as a QR? |
|---|---|---|---|---|---|---|
| d01 | `vortx-ai.github.io/ememdemo/?s=emem:fact:defi.zb572.xoso.zb1ec:oj5cecci…` | 200 | 2.1 s | 31 | "Tokenise huge files for agents to use."; "ememified 610 ms"; "indices.ndvi at defi.zb572.xoso.zb1ec"; "signed record ✓ signed by emem.dev · its bytes hash to its name". **No value, no date, no source anywhere on the page.** Creates a device key ("T1 key … back up now") | no |
| d04 | same, cell swapped to `defi.zb493.xuqA.zcb5f` | 200 | 2.9 s | 30 | "stopped 1.2 s"; "emem.dev said 409: token cell … does not match the signed fact's cell … refusing to dereference a mislabeled handle" | no; the server refuses, the browser only relays it |
| d05 | ememdemo `?s=https://emem.dev/memories/by_attester/njedkglt/qfkcuqcmhvswbe5slcyoxjkwoe.md` (sealed v11 track) | 200 | 9.8 s | 85 | "✗ ememified, with a finding 8.3 s 60 requests"; "steps checked again: 29 of 30" (step blocked: `POST /v1/recall` for the cell); "written by njedkglt · … not named, not affiliated" | only after a v13 rebuild without the recall step (§2.4) |
| d02 | `emem.dev/verify?q=<Keylong token>` | 200 | 2.0 s | 14 | page header and composer. The result ("✓ verified in this tab", 0.4708994708994709, "indices.ndvi · observed 2026-09-25", six ✓ lines, a fields table) starts about 825 CSS px down | **yes: TRY A TOKEN**, through `/t/` |
| d03 | `emem.dev/verify?q=<cell-swapped token>` | 200 | 1.5 s | 12 | the same header. Below the fold: "✗ failed: the resolver refused it (409): token cell …", cut at "`defi.zb493.xu"; the red pill overflows the card | no (a refusal is shown better by the demo) |
| d06 | `emem.dev/verify` (v12 QR) | 200 | 1.4 s | 11 | an empty composer. Its seven example chips mint live records by `/v1/recall`, `/v1/grid`, `/v1/locate`, `/v1/ask` when tapped (SPEC `verify.html:941-948`) | no (an unexplained root page; #34) |
| d07 | `emem.dev/demos/handoff` | 200 | 1.4 s | 11 | "Check what another agent handed you". It runs only on a button press or `?run`. With an empty token box it first calls `POST /v1/recall` for live Bengaluru temperature (SPEC `demos-handoff.html:436-445, 593`). No URL parameter fills the token | no |
| d08 | `emem.dev/demos` | 200 | 1.2 s | 11 | an index of 8 demos | no |
| d09 | `emem.dev/#use` | 200 | 2.6 s | 25 | lands on "Decode it anywhere": 24 tiles (MCP, REST, A2A, Claude Code, Claude plugin, Claude.ai, ChatGPT, Dify, Cursor, VS Code, Gemini CLI, Cline…). Fires `POST /v1/recall {"place":"Lusail","bands":["copdem30m.elevation_mean"]}` on load (blocked). A green dot means "this same-origin endpoint answered just now" (SPEC `index.html:3476-3497`), not that the client was tested | fallback for DISCOVER INTEGRATIONS only |
| d10 | `emem.dev/.well-known/agent-card.json` | 200 | 1.0 s | 1 | raw JSON at a 980 px layout width; unreadable at 390 px | no; link it from `/use/` |
| d11 | `emem.dev/v1/facts/oj5cecci…` | 200 | 0.8 s | 1 | raw JSON at 980 px width | no; link it from `/r/` |
| d12 | `github.com/Vortx-AI/esa_poster/tree/main/research/repro/v12` (v12 QR) | 200 | 3.9 s | 158 | folder list (audit, data, scripts, trace, CLAIMS_MAP.md); no sign-in needed | target behind `/test/`, but use `v13` |
| d13 | `…/tree/main/research/repro/v11` | 200 | 3.9 s | 159 | folder list | same |
| d14 | `…/blob/main/research/repro/v12/CLAIMS_MAP.md` | 200 | 3.8 s | 154 | rendered markdown | target behind `/methods/` (v13 file) |
| d15 | `github.com/mcp/Vortx-AI/emem` (GitHub MCP Registry) | 200 | 3.4 s | 139 | "emem, the verifiable memory protocol for the physical world · By Vortx-AI · 63 · Install MCP server" | linked from `/use/` |
| d16 | `marketplace.dify.ai/plugin/vortx-ai/emem` | 200 | 3.5 s | 74 | a cookie banner covers the lower half. Text includes **"Verified by Dify"**, "No ratings yet", 32 installs, "Install" | linked from `/use/` (the badge is for the ecosystem owner; 03 recorded `authorized_category: community`) |
| d17 | `glama.ai/mcp/servers/Vortx-AI/emem` | 200 | 3.9 s | 102 | "emem by Vortx-AI"; "Remote"; README text | linked from `/use/` |
| d18 | `github.com/Vortx-AI/emem` | 200 | 5.3 s | 216 | repo page; no sign-in needed | linked from `/use/` |
| d19 | `registry.modelcontextprotocol.io/v0.1/servers/io.github.Vortx-AI%2Femem/versions/latest` | **404 in Chromium** (200 with curl; cause not isolated) | 0.8 s | 1 | `{"detail":"Endpoint not found…"}` | **no.** The `?search=` form returns 200 but took 13 s and is raw JSON (s07) |

In every row above that has an HTTP column, the page loaded without sign-in. The GitHub pages show a "Sign in" link,
which is not a wall (MEASURED from screenshots).

### 1.2 ememdemo: how `?s=` works, and why it is not the right front door here

- SPEC (served `src/eio.mjs:799-801`, fetched 2026-10-01; file sha256 `5dcc410d…` per the site seal):
  - `?s=<value>` runs automatically only when the value is a reference: a note URL, a token, a CID or a log head,
    with no whitespace.
  - The code comment says: "a shared link only opens references …; anything that would read a source or write is
    left in the box for you to run". `#k=` and `#g=` fragments carry a key or grant.
- SPEC (`index.html` loader, LIVE): the page runs no file it has not checked. A manifest on emem.dev (sha256
  `1ac68111…`, sealed by `ddzmyzhn…`) names 18 files by sha256. The footer confirms "sealed · 18 of 18 files checked".
- MEASURED (d01):
  - For a fact token, the result block shows the band, the cell, "signed by emem.dev · its bytes hash to its name"
    and a check time. The requests were `POST /v1/memory_token/resolve` and `GET /v1/facts/<cid>`.
  - The value 0.4709 and the date never appear.
  - Each visit created a device key in the browser (`iib5xjyf`, `lt2lf2qz`, `amrqpcmt`). LIVE: all three namespaces
    are empty (`GET /memories/by_attester/<k>/` → `count: 0`), so nothing was published.
- MEASURED (d05), the track viewer:
  - It fetched the note, re-checked the steps, recomputed the chain and checked the inclusion proof: 60 requests in
    8.3 s.
  - One step (the cell) needs `POST /v1/recall {"cell":"defi.zb572.xoso.zb1ec","bands":[…4 bands]}`. Blocked, it fails
    and the header turns red. So every visitor who opens the track asks emem.dev to run a recall. The brief classes
    recall as a write ("emem read tools sign and store records").
- LIVE: `llms.txt` line 2 still says `check base32(blake3(bytes))[0:26]==cid` (defect 24, as in 07 §3.1). An agent
  that follows it rejects the poster's own valid track.

INFERRED verdict: ememdemo is the right home for the *sealed board* idea. It is the wrong front door for "try a token"
and "view the demo", because its first screen is about file tokenisation and it never shows the observation.

### 1.3 emem.dev/verify: the best existing token page

- SPEC: `/verify?q=<input>` and `/verify/<cid>` both auto-run (`web/verify.html:976-977`; routes
  `crates/emem-api-rest/src/lib.rs:774, 785`).
- SPEC: for a fact token, `doFact` (`verify.html:550-575`) runs these steps:
  - `POST /v1/memory_token/resolve`, then shows the value, band and observed date;
  - checks `cell_matches`;
  - fetches the CBOR and re-hashes it;
  - checks the resolve receipt's Ed25519 signature against the key in `/.well-known/emem.json`, and that the receipt
    covers the CID.
- It does **not** fold the fact into its original signed batch or into the transparency log. The receipt it checks
  was signed at request time. The demo in §3 checks the original attestation and the log entry.
- SPEC: a bare CID (`/verify/<cid>`) is read "as the fact at its own cell" (`verify.html:577-580`). That drops the
  place binding, which is the receiver failure the Qwen arm showed (07 §0.3). So use the full token, not the shorter
  CID URL.
- SPEC: the resolve endpoint signs a receipt per request and stores nothing (`lib.rs:38401-38413`; `sign_receipt` at
  `crates/emem-storage/src/server.rs:248` has no storage call). INFERRED: safe to put behind a public QR.

Defects to hand to emem (not fixable by the poster team; INFERRED priority):

1. Scroll the result into view when `?q=` is present (on a phone the verdict is one screen down).
2. Wrap the failure badge, and do not cut the 409 reason at 220 characters (`why()`, `verify.html:426`).
3. Name the layer in the badge ("bytes and responder signature checked", not "verified").

### 1.4 The integration hub (`emem.dev/#use`)

MEASURED (d09):

- The anchor lands on the 24-tile grid in 2.6 s. Seven tiles show a green dot (MCP, REST, A2A, Claude Code, Claude.ai,
  Cursor, VS Code). Five are hollow (Claude plugin, ChatGPT, Dify, Gemini CLI, Cline).
- SPEC (`index.html:3476-3497`): the dot is one probe of the same-origin endpoint: `POST /mcp initialize`, or a GET.
  So "Cursor ●" means emem.dev/mcp answered, not that Cursor ran.
- The Gemini tile says "extension config". 03 measured that the extension route fails.
- INFERRED: DISCOVER INTEGRATIONS should open a page that prints the manifest's status vocabulary (LIVE / PROTOCOL /
  REGISTRY / EXAMPLE), as MASTER §17 requires. That is `/use/` (§4). `emem.dev/#use` stays as a link from it.

---

## 2. The final QR set

### 2.1 Six QRs, one verb-led call to action each

Payloads point at short paths on the poster's own Pages site, `https://vortx-ai.github.io/esa_poster/`. Each path is
either the artifact itself or a one-hop redirect to it. There are three reasons:

- uniform version-4 symbols;
- a target can be corrected after printing without reprinting;
- no dependence on long emem.dev URLs.

| CTA (printed, Plex Mono Bold) | one-line caption (printed) | QR payload | final destination | exists today? | phone path (MEASURED) |
|---|---|---|---|---|---|
| **VIEW THE DEMO** (hero) | Your phone is Agent B: one paraphrase passes unchecked; three corruptions are refused. | `https://vortx-ai.github.io/esa_poster/demo/` | the receiver demo (§3), served by Pages | **build** (prototype done) + enable Pages | 9.8 s to six verdicts; 8 requests; offline 9.8 s, 1 request (s02, d20–d24) |
| **TRY A TOKEN** | Resolve the Keylong token on emem.dev, then paste your own. | `https://vortx-ai.github.io/esa_poster/t/` | `https://emem.dev/verify?q=emem%3Afact%3Adefi.zb572.xoso.zb1ec%3Aoj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` | target LIVE; redirect **build** (done) | redirect + verify: 1.9 s to the result (s05); result one screen down |
| **INSPECT THE RECORD** | The 1,115 bytes behind the main example, field by field. | `https://vortx-ai.github.io/esa_poster/r/` | the record page (§4.2) | **build** (prototype done) | 0.6 s, 1 request (s03) |
| **RE-RUN THE TEST** | Data, scripts and one command for every result on this board. | `https://vortx-ai.github.io/esa_poster/test/` | `https://github.com/Vortx-AI/esa_poster/tree/main/research/repro/v13` | redirect built; **target missing** (404 on `main`) | today lands on GitHub "File not found" (s06) |
| **READ THE METHODS** | Definitions, denominators, models, and what our own tools generated. | `https://vortx-ai.github.io/esa_poster/methods/` | `https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v13/METHODS.md` | redirect built; **target missing** | GitHub blob render measured on v12's CLAIMS_MAP.md: 3.8 s (d14) |
| **DISCOVER INTEGRATIONS** | Where EMEM runs today, each surface labelled by evidence. | `https://vortx-ai.github.io/esa_poster/use/` | the integrations page (§4.3), generated from `research/v13/ecosystem_manifest.json` | **build** (prototype done) | 0.6 s, 1 request (s04) |

Print the short base URL `vortx-ai.github.io/esa_poster` once, in text, beside the QR group. The site root is the
landing page with the same six buttons and the same words (§4.1).

### 2.2 Placement and size (INFERRED; coordinate with 06 §6)

- **VIEW THE DEMO** sits at the right end of the handoff spine, next to the mutation matrix, so it reads as the
  continuation of the main experiment.
  - Symbol: 70 mm, module 2.12 mm, plus an 8.5 mm quiet zone on each side, so the box is about 87 mm.
  - Label: "VIEW THE DEMO" at 28 pt Plex Mono Bold, with the caption at 18 pt.
- The other five sit in one row in the bottom-right "Try · reproduce" strip.
  - Symbol: 40 mm, module 1.21 mm, plus 4.8 mm of quiet zone, so each box is about 50 mm. Five boxes with four 8 mm
    gaps take 282 mm.
  - DISCOVER INTEGRATIONS may move into the ecosystem band instead (issue #44).
- Do not put text or hatch inside the quiet zone (06 §0.8).

### 2.3 Size rule, measured and modelled

| payload | ECC | version | modules | symbol for ≤ 0.5 m | symbol for ≤ 1 m |
|---|---|---|---|---|---|
| the six short payloads above | Q | 4 | 33 | 36 mm | 72 mm |
| `emem.dev/verify?q=<full token>` (110 chars) | M / Q | 7 / 9 | 45 / 53 | 49 / 58 mm | 99 / 116 mm |
| ememdemo `?s=<token>` (129 chars) | M | 8 | 49 | 54 mm | 107 mm |
| v12 `qr_repro` (67 chars, printed at 30 mm) | M | 5 | 37 | 41 mm | 81 mm |

- Model (INFERRED): a scanner preview 1920 px wide over a 70° horizontal field of view, needing at least 3 px per
  module. That gives a symbol width of 3 × 2·d·tan 35° / 1920 × modules.
- Software check of the threshold (MEASURED, `qr/qr_sim.py`, OpenCV 5.0.0, 0.6 px blur, noise σ 6, 10 trials each):

  | px per module | decoded |
  |---|---|
  | ≤ 1.8 | 0/10 |
  | 2.0–2.5 | 7–10/10 |
  | ≥ 3 | 10/10 |

- This agrees with review finding F10: v12's 30 mm repro QR does not decode at 1 m.
- MEASURED (`qr/make_qr.py`): all six proposed symbols were generated with ECC Q and a 4-module border. Each was
  rasterised at 300 dpi at its print size and decoded back to its exact payload by OpenCV (6/6).

### 2.4 Kept and dropped destinations

- **Sealed board track (ememdemo):** KEEP as a 30 cm text link on `/r/` ("the whole board as a signed track"), not as
  a QR, unless the v13 track is rebuilt without the cell/recall step.
  - Reason: as it stands, a scan triggers `POST /v1/recall`, and if that fails the visitor sees a red ✗ on the
    poster's own seal (d05).
  - The track also needs the poster key to re-sign, which only the authors may do (07 §3.1).
- **Dropped:**
  - `emem.dev/verify` bare (an unexplained root page);
  - the agent card and raw `/v1/facts` JSON (unreadable at phone width; linked from `/use/` and `/r/`);
  - the Official MCP Registry API URL (404 in Chromium);
  - `/demos/handoff` (no token parameter; it calls recall).

---

## 3. VIEW THE DEMO: the ≤ 20 s receiver instrument (#35)

### 3.1 Storyboard (MEASURED timings from the built page; pacing constant `STEP = 1500 ms`)

| t (s) | what the screen shows | receiver check | layer | R1 id |
|---|---|---|---|---|
| 0.1 | Headline "Change one field. The receiver refuses." A true-colour Sentinel-2 crop (1.92 km, from the committed 10 m grids) with the ring centred on the cell. "0.4709 · Sentinel-2A L2A, B08 and B04 · 2026-09-25 05:42:51Z · cell defi.zb572.xoso.zb1ec". Agent A's token. "It names 1,115 bytes of CBOR by their BLAKE3-256 hash." | — | — | — |
| ~1 | **prose**: B receives "NDVI is about 0.47 at the Keylong field, late September." | nothing to resolve, re-hash or verify | — | level A |
| | → **ACCEPTED, unchecked** (amber) | | | |
| ~3 | **M3**: byte 82 of the record changes 0x33 → 0x34 (value +1 ULP: 0.4708994708994709 → 0.47089947089947093); the token is kept | the bytes hash to `47o5vzsv…`, not `oj5cecci…` | L0 | M3 (first stopped at D) |
| | → **REFUSED** | | | |
| ~4.5 | **M4**: the same CID cited as `emem:fact:defi.zb493.xuqA.zcb5f:oj5cecci…` (a Bengaluru cell) | L0 passes; "the token says defi.zb493.xuqA.zcb5f; the record says defi.zb572.xoso.zb1ec" | L1 | M4 (E) |
| | → **REFUSED** | | | |
| ~6 | **M8**: value bytes set to 0.45 (`3fdccccccccccccd`) and the token re-named `ylcx42oi…` | L0 hash and L1 pass; "no batch signed by key 777er3yi… contains these bytes" | L0 signature | M8 (F) |
| | → **REFUSED** | | | |
| ~7.5 | **G0**: the genuine token and bytes. Hash ✓; cell ✓; "the bytes sit in a batch of 1; its Merkle root recomputes; Ed25519 accepts the signature of key 777er3yi…" ✓; "log entry 2,457,078 under a signed head of 2,556,451 entries; a second key (quunzdv5…) co-signed head 2,541,495, a prefix of it" ✓; "NDVI recomputes from the signed inputs: B08 3502, B04 1900, offset −1000 → 0.4708994708994709" ✓ | | L0, L1, L2 | G0 |
| | → **ACCEPTED, checked** (blue) | | | |
| ~9 | live line: "GET emem.dev/v1/facts/oj5cecci… → 200, byte-identical to the embedded copy; the forged name ylcx42oi… → 404" | archive confirmation | — | — |
| ~9.5 | **L3** (prefetched from t = 0): "tile 413 of each (945,880 B); their BLAKE3 equals the hashes taken on 30 Sep" ✓; "pixel (col 9098, row 9443): B08 3502, B04 1900; the record signed 3502, 1900" ✓; "NDVI from the re-read pixel: 0.4708994708994709 = the signed value, bit for bit" ✓. A 5 × 5 NDVI grid: named pixel 0.471 outlined in blue, the pixel 10 m south 0.302 outlined dashed in red | source re-read | L3 | I |
| 9.8 | **Boundary**: L4 "Whether this cell is the field Agent A meant. Out of scope." L5 "Whether the sensor was right, and whether a decision taken on 0.4709 is right. Inherited from product validation, or out of scope." "A signature fixes the bytes. It does not make the measurement true." | — | L4, L5 | M17 never |

The verdict board under the token fills as the run proceeds. It has six pills: prose *unchecked*, M3 *refused*,
M4 *refused*, M8 *refused*, G0 *accepted*, L3 pixel *re-read, matches*. All six are above the fold at 390 × 844
(MEASURED screenshot `mobile/out/demo_phone_lastframe.png`). So a visitor sees the result without scrolling, and
everything below is the evidence for it.

### 3.2 Exact data the page needs, all from committed files

| datum | value | source |
|---|---|---|
| proof bundle | 4,906 B CBOR; sha256 `8335118655b3334ca34381cf716b16b642e83989f77dd07965011c0cd4e26d11`; BLAKE3 `4a3f07bb8f60246cffee2d12825389d000d0c2d77058f007675825762051a613`. Keys: `v, token, entry, leaf_index, sth, witness, upstream` | `research/repro/v8/proof_bundle_ndvi.cbor` (MEASURED: `verify_bundle.py` PASS 9/9 today, 0.05 s, offline) |
| token | `emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` | bundle `token` |
| record bytes | 1,115 B (hex in Appendix A); sha256 `0628924d…fc74813`; BLAKE3 base32 = `oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa` | the only element of `entry.facts` (MEASURED) |
| record fields | kind `primary`; cell `defi.zb572.xoso.zb1ec`; band `indices.ndvi`; tslot 20721; value 0.4708994708994709 (f64 `3fde233788cde233` at byte offset 75); confidence 0.95 (f32); source scheme `sentinel_s2_l2a`; two Planetary Computer COG URLs (B08, B04); `captured_at` 2026-09-25T05:42:51.024000Z; derivation `sentinel2_l2a_indices_ndvi@1` with args [lat 32.57125977099409, lng 77.03447748052537, scene `S2A_MSIL2A_20260925T054251_R005_T43SFS_20260925T090015`, EPSG 32643, formula text, DNs [3502.0, 1900.0] as f16, cloud 10.840102, 40.0, 30, 4, 1, STAC URL, offset −1000.0 as f16]; privacy `public`; schema_cid `d24rgwlq…`; signer key = `777er3yi…`; signed_at 2026-09-28T09:06:56Z | decoded (MEASURED) |
| attestation | batch of 1; root `wnljgmqg…`; attester `777er3yi…`; attested 2026-09-28T09:06:56Z; preimage v1; registry_cid `3pbqnyni…` | bundle `entry` |
| log | leaf 2,457,078; STH 2,556,451 signed 2026-09-30T09:15:54Z by `777er3yi…`; witness `quunzdv5qymo…` head 2,541,495 with a consistency proof (21 nodes) | bundle `sth`, `witness` |
| M3 copy | the record with byte 82 `0x33` → `0x34`; CID `47o5vzsvu2krdvijfvtpj2awxdacgwijjkha3tfhlixujqmo7jlq` | computed in the page (MEASURED identical in Python and JS) |
| M4 token | `emem:fact:defi.zb493.xuqA.zcb5f:oj5cecci…` (the cell v12 and 07 used for the relabelled token) | constant |
| M8 copy | bytes 75–82 set to `3fdccccccccccccd` (0.45); CID `ylcx42oiamnly5e2dmqry2lfj2de2wgj5aalgpd5bgb5mr6nh52a`; LIVE `GET /v1/facts/ylcx42oi…` → 404 `cid_not_found` | computed |
| pixel windows | 5 × 5 B08/B04 DNs around col 9098, row 9443, BOA offset −1000 (the offline fallback for L3) | `research/repro/data/v8/pixel_windows.json["oj5cecci S2A 2026-09-25 (signed 2026-09-28T09:06Z, post-fix) offset -1000"]` |
| image | 192 × 192 true colour (B04/B03/B02), rows 116–307, cols 129–320 of the 443 × 453 grids; 1 %–99.5 % stretch, γ 0.85; WebP 16,274 B | `research/repro/data/keylong_B0{2,3,4}.bin` (grid row 212, col 225 = COG pixel (9443, 9098), per 06 §0.1) |
| pinned key | `777er3yihgifqmv5hmc2wwmyszgddzderzhsx6rex4yoakwomvka` | DNS TXT `_emem-node.emem.dev`, `did.json`, `jwks.json` (per `verify_bundle.py` header; 03 §1.2) |

Why the page patches bytes and never re-encodes: MEASURED, `cbor2.dumps(cbor2.loads(fact), canonical=True)` ≠ the
fact bytes, and so does the non-canonical dump. emem's canonical form is not a generic library's. A receiver that
decodes and re-encodes before hashing would refuse every genuine record. That is a false-refusal bug of the same family
as ememdemo's wrong `llms.txt` rule. The page hashes the bytes it received, as the protocol requires.

### 3.3 The receiver algorithm (ported one-to-one from `research/repro/v8/verify_bundle.py`; source in Appendix B)

`receive(handoff)`:

1. Prose: record "a sentence carries no name to resolve, no bytes to re-hash, no signature to check" and return
   ACCEPTED, unchecked.
2. Parse `emem:fact:<cell>:<cid>`.
3. **L0 hash.** If `base32(BLAKE3-256(bytes)) ≠ cid`, REFUSE.
4. **L1 binding.** If `cbor(bytes).cell ≠ token cell`, REFUSE. (The cell form of the token carries no band or date;
   the descriptor form does. SPEC, `lib.rs:33314`.)
5. **L0 signature.** The bytes must equal a raw element of the logged attestation's `facts`. The leaves are sorted
   BLAKE3 values; leaf = H(0x00‖l), node = H(0x01‖l‖r), an odd node pairs with itself. The root must equal
   `batch_root`. Then `Ed25519(attester = pinned, H(PreimageV1("attestation"){1: batch_root, 2: registry_cid,
   3: schema_cid}))`. Otherwise REFUSE.
6. **L0 log.** Leaf = H(0x00‖H(entry)). RFC 6962 inclusion at `leaf_index` under the STH. The STH signature is
   Ed25519 over `H(PreimageV1("emem.translog.sth.v1"){1: u64be size, 2: root, 3: signed_at, 4: pubkey})` by the
   pinned key. The witness signature is over `PreimageV1("emem.translog.witness.v1")`, with inclusion under the
   witnessed head and consistency from the witnessed head to the STH. Otherwise REFUSE.
7. **L2 recompute.** ρ = (DN + o)·10⁻⁴ (SPEC `lib.rs:51726-51748`, `:52771-52778` via `research/repro/v10/algorithms.md`).
   NDVI = (ρ₈ − ρ₄)/(ρ₈ + ρ₄) from `args[5]` and `args[12]` must be `===` the value. Otherwise REFUSE.
8. ACCEPTED, checked (L0, L1, L2).

**L3** `rereadPixel` (live; it never changes a verdict):

1. Get a SAS token from `planetarycomputer.microsoft.com/api/sas/v1/token/sentinel2l2a01/sentinel2-l2`.
2. For each upstream URL: range-read bytes 0–65,535 and parse the classic TIFF IFD (W = 10,980, tile 512, bps 15,
   compression 8).
3. Find tile ⌊row/512⌋·22 + ⌊col/512⌋ = 413, range-read it, and BLAKE3 it.
4. Inflate it with `DecompressionStream('deflate')`.
5. Unpack the 15-bit big-endian samples. Read the DN at (col mod 512, row mod 512) and the 5 × 5 window.
6. Compare the DNs with `args[5]` and the recomputed NDVI with the value.

Negative controls (MEASURED; the attestation case from `negctl2.mjs`, the other two from `negctl.mjs`): each turns G0 into REFUSED.

| control | result |
|---|---|
| one bit flipped in the attestation signature | REFUSED: "the batch signature does not check" |
| one bit flipped in the STH signature | REFUSED: "the log proofs do not check" |
| one node of the inclusion path altered | REFUSED: "the log proofs do not check" |

Self-test: the page refuses to report if `BLAKE3("")` ≠ `af1349b9…3262`. This applies the rule in emem's own verifier
comment: "Telling a user their genuine fact was forged is a worse failure than declining to check it"
(`web/emem-verify-core.js:13-15`).

Cost: the full G0 check takes 11.7 ms per handoff (Node 22, pure-JS @noble, three Ed25519 verifies, two inclusion
proofs and one consistency proof; MEASURED `bench.mjs`). R1's Python/libsodium level-I check is 1.187 ms
(`research/repro/v11/out/summary.md`).

### 3.4 Measured runs of the built page (390 × 844)

| run | done (`window.__RESULT__`) | requests | verdicts | live results |
|---|---|---|---|---|
| live, unthrottled (s02, s08, s09, d20, d24) | 9.79–9.88 s | 8 | prose warn · M3 no · M4 no · M8 no · G0 ok · L3 ok | facts 200 identical; forged 404; B08 3502, B04 1900; both tile BLAKE3 equal |
| throttled 4 Mbit/s, 150 ms RTT (d21) | 9.79 s | 8 | same | same; the last source read started at 3.3 s and finished before the L3 step |
| `?offline` (d22) | 9.78 s | 1 (the page) | same five; L3 shows "committed copy … not re-read on this phone" | none |
| `?fast` (unpaced; d23) | 3.43 s | 8 | same | same |

The source reads start at t = 0 in parallel, so the network is never on the critical path while it takes under about
9 s. A 9 s cut-off then shows the committed window, labelled as such (MEASURED code path; not triggered in these runs).
The only console error is the expected 404 for the forged CID.

### 3.5 Accessibility and the text fallback

- MEASURED (`demo/transcript.txt`, 3,688 B, sha256 `10c42f7d…cbb1103d`): the build runs the same receiver in Node.
  - It asserts the five expected verdicts and fails the build otherwise.
  - It writes a plain-text transcript: every input, every check line, every verdict, the L3 pixel values and the
    boundary.
  - The page links it in the footer and in `<noscript>`.
- Every verdict is a word as well as a colour and a glyph: "REFUSED", "ACCEPTED, unchecked", "ACCEPTED, checked".
  This follows 06's state palette (EMEM blue `#0F5FA8`, vermillion `#D2481E`, amber `#E8A317`, warm grey `#9C9A92`)
  and its CVD check.
- A polite `aria-live` status line announces each verdict.
- `prefers-reduced-motion` and `?fast` remove the pacing. Dark mode is supported.
- Exact input and output are exposed (#35):
  - collapsible "the 1,115 record bytes (hex)";
  - "the record, decoded";
  - every check line names its layer.

### 3.6 Final page copy (every sentence on the page, as built)

> EMEM · receiver demo · Agentic AI for EO, Berlin, 19 Oct 2026
> **Change one field. The receiver refuses.**
> This page is Agent B. Agent A hands it evidence about one 10 m cell near Keylong, India. The page trusts nothing it is
> handed. It re-hashes the record, checks the signature and the public log, recomputes the value, and re-reads the
> source pixel. It uses BLAKE3, Ed25519 and CBOR, and no emem code.
> NDVI of the 10 m cell at the ring's centre · 0.4709 · Sentinel-2A L2A, B08 and B04 · 2026-09-25 05:42:51Z · cell defi.zb572.xoso.zb1ec
> Agent A hands over one reference, not a sentence: [token]. It names 1,115 bytes of CBOR by their BLAKE3-256 hash.
> **Five handoffs, one receiver** — A paraphrase · One byte changed in transit · The right record, cited for another place · Value forged to 0.45 and re-hashed · The genuine handoff
> **L3 · Re-read the named pixel** — The record names its source files and its pixel. The browser fetches the two 512 × 512 tiles from Planetary Computer and decodes them itself. … Solid blue: the pixel the record names. Dashed red: the pixel 10 m south, NDVI 0.3016.
> **The right record, the wrong pixel.** Before 28 Sep 2026 emem's reader rounded the pixel index; for this cell that is the dashed pixel. In a sample of 200 earlier records, 162 carried the rounded pixel's values: signed faithfully, and wrong. Every check above accepts such a record. Only this re-read catches it.
> **What no check here can tell you** — L4 Whether this cell is the field Agent A meant. Out of scope. · L5 Whether the sensor was right, and whether a decision taken on 0.4709 is right. Inherited from product validation, or out of scope.
> A signature fixes the bytes. It does not make the measurement true.

Sources for the M15 sentence:

- SPEC: `CHANGELOG.md:68`: "`cog::world_to_pixel` rounded the fractional pixel position … GDAL takes the floor".
  The fix time is `PIXEL_FIX_AT = 2026-09-28T04:09:26Z` (algorithms.md).
- MEASURED: `research/repro/data/v8/prevalence_summary.json`: `matches_round_not_floor: 162`, `n: 200`, Wilson 95 %
  0.75–0.86, 19 bands, 192 Element84 + 8 PC records, signed 2026-05-14 to 2026-09-27.

### 3.7 What the demo does not show (state it on the methods page)

- It is a scripted harness written by the authors. The receiver is code, not an LLM. The mutations are authored, and
  named as in R1 (`research/repro/v11/mutation_suite.py:332-349`). The genuine record, its signature, its log proofs
  and the source pixels are real.
- It covers one record, one cell and one band. It is not the 16-mutation suite; RE-RUN THE TEST is that.
- M8 is refused because the page holds the signed batch for this observation, from the committed bundle. A real
  receiver would look the forged name up and get 404; the live line shows that. The page does not search the whole log.
- The L3 tile hashes come from the poster team's v8 trace (30 Sep), not from the signer. The record carries no source
  hash (§0.4). L3 shows that the named pixel of the named file gives the signed value today. It does not show the
  upstream product is right (L5).
- It was tested on Chromium only. Safari needs `DecompressionStream` (16.4+) and `color-mix` (16.2+). INFERRED: those
  are within the support ememdemo already requires ("Safari 16.4+", ememdemo loader). Not tested here.
- A receiver that drops the cell (the Qwen arm, 07 §0.3) is not shown. It is optional §7.5 material once
  `qwen_trials.jsonl` is committed.

---

## 4. The rest of the QR site (built as prototypes; MEASURED on the phone rig)

Layout (proposed in-repo location `docs/`, GitHub Pages source "main /docs"; `.nojekyll` included):

```
docs/index.html            landing: the six CTAs, same words as the board                0.6 s, 1 request
docs/demo/index.html       the receiver demo (§3)                                        9.8 s
docs/demo/transcript.txt   text fallback
docs/r/index.html          INSPECT THE RECORD                                            0.6 s, 1 request
docs/use/index.html        DISCOVER INTEGRATIONS, from research/v13/ecosystem_manifest.json   0.6 s, 1 request
docs/t/index.html          redirect → emem.dev/verify?q=<Keylong token>                  1.9 s to the result
docs/test/index.html       redirect → github …/tree/main/research/repro/v13              (target 404 today)
docs/methods/index.html    redirect → github …/blob/main/research/repro/v13/METHODS.md   (target 404 today)
docs/media/                the media pack (§7) + manifest.json (§8)
```

### 4.1 Landing (`/`)

- Hero: "Agents hand each other evidence references, not paraphrases."
- One line naming the programme title, session and date.
- Six CTA cards in the board's order, each with a one-sentence description (MEASURED render, `mobile/out/s01_landing.png`).
- A media link.

### 4.2 Record (`/r/`; MASTER §5 and §15)

The record is shown as a table: token; place (cell + lat/lng + "near Keylong, Lahaul, India"); band/product; valid
time + scene + cloud; value + confidence; signed inputs (DNs, offset, recomputed value); source files ("named, not
hashed … the record carries no hash of these files"); derivation key; name of the record ("= base32(BLAKE3-256(the
1,115 bytes below)). It names this record, not the satellite file."); signed (key, batch root, time); logged (entry,
head, witness).

Then three links (demo, emem.dev/verify, raw bytes at `emem.dev/v1/facts/<cid>`), the 1,115-byte hex, and the boundary
sentence. All fields are generated from the committed bundle (`demo/build/site.mjs`).

### 4.3 Integrations (`/use/`)

- Generated from the 24 manifest rows with `print.allowed === true`. Rows whose condition is "only after the manual
  check" (ChatGPT) or "only with the corrected config" (Cline) are left out, so they stay off until their condition
  is met.
- Grouped by `poster_group`, with a status chip from `status` (LIVE / PROTOCOL / REGISTRY / EXAMPLE), never typed by
  hand. The direct link is the row's `url`.
- Two defects found while generating it, for the ecosystem owner (INFERRED):
  - Row `official-mcp-registry` links an API URL that returns 404 in Chromium (d19). Use the `github-mcp-registry`
    page for humans, and print the registry name as text.
  - Row `langchain` has `print.allowed: true`, while 03 §7 says "LangChain (after the fix)". The two disagree.
- Add a "same token, eleven runtimes" table from `research/repro/data/v8/crossruntime_table.json`: path, 3/3, one
  CID, one value, median ms. Add a refusal row: "wrong-cell token refused on 7 Python paths; LangChain MCP adapters
  return the refusal as ordinary text". The source for that row, `scratchpad/v8/crossruntime/refusal_matrix.json`,
  is not committed; commit it first (02 §1).

---

## 5. "Same evidence, different agent" (#43) in the media layer

| claim | status | evidence | where it appears |
|---|---|---|---|
| the same token resolves to one CID and one value through 11 client paths, 3/3 each | MEASURED (2026-09-30T08:40Z, server `213e2738`) | `research/repro/data/v8/crossruntime_table.json` `summary.ndvi_keylong`: `paths_run 11, paths_ok 11, distinct_fact_cids 1, distinct_values 1` | `/use/` table; 60 s video 0:07–0:15 (on-screen list only) |
| an A2A `message/send` resolves it | MEASURED (same file, path `3_a2a_message_send`, 3/3, 226 ms median) | same | `/use/` |
| Claude Code and Gemini CLI connect to `emem.dev/mcp` | LIVE, connection only, no model turn (03 §0.2) | 03 report | `/use/` status LIVE |
| a model in agent host X hands the token to a model in host Y, which resolves it and refuses a forgery | **not measured** | the R5 design (02) runs Claude models via the Claude Code CLI and Qwen via llama.cpp, not two commercial hosts | must not be implied. If R5 runs it, add one panel: "Claude (MCP) → Qwen (harness): same token, same refusal" |
| ChatGPT (@emem) / Dify resolve the token | UNVERIFIED / not run | 03 §0.4, §1.1 | omit until a dated screenshot exists |

Printed caption (INFERRED, true to the rows above): "One evidence protocol, eleven client paths: one name, one value,
every time. Model-in-the-loop handoffs between hosts are not shown here."

---

## 6. Why the demo is the "why EMEM" argument (the user's catastrophe point)

Each demo step stages a bug class that any multi-agent EO stack can ship. emem shipped several of them, found them and
fixed them, and none was caught by a signature alone.

| demo step | bug class any multi-agent system can have | emem's own instance (status) | what catches it | label |
|---|---|---|---|---|
| prose | evidence is relayed as a sentence; nothing to check | v12 board line 137 "0.4709 becomes 'about 0.47'"; R1 level A acted on 15/15 corrupted handoffs | nothing: accepted, unchecked | MEASURED (R1) |
| M3 | bytes drift in transit (float formatting, re-serialisation) | emem's benchmark arm: value retyped in 21.7 % of resolves (SPEC, 02 §1) | L0 hash | MEASURED (R1 D) |
| M4 | the right record cited for the wrong place | small receiver model (Qwen2.5-3B) dropped the cell from 24/24 tokens and acted on 5/5 forged cells (07 §0.3; uncommitted) | L1 binding, if the receiver keeps the token whole | MEASURED (uncommitted) |
| M8 | a self-consistent forgery (re-hashed) | content addressing alone is forgeable: R1 levels D–E let M8 through | L0 signature + pinned key | MEASURED (R1 F) |
| re-encode-then-hash (§3.2) | the checker disagrees with the producer, so genuine records are refused | ememdemo `llms.txt` rule gives `…kjwof` for a valid `…kjwoe` (defect 24, still LIVE) | self-test vectors; hash the received bytes | LIVE, MEASURED |
| L3 | the right record, the wrong pixel | pixel rounding in every COG reader "from the first commit"; 162/200 sampled records (fixed 2026-09-28, `CHANGELOG.md:68`) | L3 source re-read only | MEASURED + SPEC |
| (not in the demo) | off-tile pixels signed as 0, read as "no forest loss" | EUDR window reads: "a forest-2020 of 0 or a loss year of 0, a pass" (fixed, `CHANGELOG.md:53`) | L3 re-read; now an error | SPEC |

INFERRED framing for the board, for the methods page and for the narration: "These are not EMEM's bugs alone. Any
agent that passes evidence on, or reads pixels itself, can make them. EMEM's record makes each one detectable, except
the last two rows, which need the source re-read."

---

## 7. Media pack (#39): eight assets, one terminology, one claims map

The shared rules for every asset:

- **Terms:** the hero sentence; the ladder names L0 bytes · L1 identity · L2 derivation · L3 source · L4 entity ·
  L5 truth/decision; R1/R5 mutation ids (M1–M17, M5b, M15r…); the status vocabulary LIVE / PROTOCOL / REGISTRY /
  EXAMPLE / EXPERIMENTAL / ROADMAP.
- **Banned:** "verified" without a layer; "the satellite decides"; "spacecraft" outside the SAT-042 extension line.
- **Numbers:** every printed number is read from the claims map at build time (§8).

| id | asset | format and size | content | generator | status |
|---|---|---|---|---|---|
| M-A0 | final A0 | PDF, 841 × 1189 mm (2384 × 3370 pt), fonts embedded (complete IBM Plex, 06 §0.4), QR as vector, images ≥ 150 ppi at print size | the board | `poster/build_v13.py` (to write) | specified |
| M-PNG | print raster | PNG 9933 × 14043 px (300 dpi A0), sRGB; plus a 2480 px-wide preview | rendered from the PDF | same, `pdftoppm -r 300` or Chromium | specified |
| M-SLIDE | 16:9 slide | 1920 × 1080 PNG + PDF | the spine (Agent A umber → token chip → adversary vermillion → Agent B slate → REFUSE); right third: the R5 (or R1) false-acceptance bar by representation; bottom strip: "The right record, the wrong pixel" 0.4709 vs 0.3016; QR VIEW THE DEMO 1 inch at bottom right | same figure code as the board (`make_figures_v13.py`) | specified |
| M-D20 | 20 s demo | the live page (§3) **and** an MP4 recording: 780 × 1688 (phone portrait), H.264, ≤ 20 s, captions as WebVTT from `transcript.txt` | the §3.1 storyboard as it actually runs | `mobile/frames.mjs` + ffmpeg (MEASURED feasible: 42 frames, 12.93 s, 415,914 B, sha256 `db13d8ef…`) | prototype |
| M-D60 | 60 s narrated | MP4 1920 × 1080 (or 1080 × 1920), H.264, burned-in captions + VTT, narration recorded by an author (no synthetic voice claimed as a person) | §7.5 script over: board hero → demo capture → L3 grid → cross-runtime list → boundary | ffmpeg from captured frames + audio | script done; recording owed |
| M-QR | QR landing | the Pages site (§4) | six CTAs | `demo/build/site.mjs` | prototype |
| M-SOC | social preview | PNG 1200 × 627 (LinkedIn), plus a 1200 × 630 og:image for the landing page | hero sentence (Plex Sans Bold); the six-pill verdict row exactly as the demo renders it; the Keylong true-colour crop; footer "Poster Session 1 · Agentic AI for EO · Berlin, 19 Oct 2026 · vortx-ai.github.io/esa_poster" | screenshot of a 1200 × 627 HTML card rendered from the demo's own data | specified |
| M-HAND | technical handout | A4 PDF, one page, two columns | (1) contribution sentence and invention boundary (MASTER §4); (2) the record (§4.2 table, 9 rows); (3) the ladder with status words and counts; (4) R5/R1 result table with denominators; (5) M15 with numbers; (6) threat model (can / cannot / out of scope); (7) prior-art line; (8) cost row (11.7 ms browser check, token overhead from the cost report); (9) six QRs at 22 mm with short URLs; (10) 8 citations | `poster/build_handout_v13.py` | specified |

### 7.5 The 60 s narrated script (159 words, about 160 words per minute; every sentence maps to a claim id in §8)

| time | on screen | narration | claims |
|---|---|---|---|
| 0:00–0:07 | the board hero | "Agents hand each other evidence. A receiver handed prose has nothing to check: in our mutation suite it acted on fifteen of fifteen corrupted handoffs." | `R1.A.false_accept` (replace with `R5.prose.false_accept` when R5 runs) |
| 0:07–0:15 | Keylong crop, the token | "EMEM hands over a reference instead: a signed record of one observation, named by its hash. NDVI 0.4709, one ten-metre cell near Keylong, twenty-fifth of September." | `rec.value`, `rec.captured_at`, `rec.cell_size` |
| 0:15–0:27 | demo cards M3, M4, M8 | "The receiver re-hashes it. One byte changed: refused. Cited for another place: refused. Forged and re-hashed: refused; no signature covers it." | `demo.M3`, `demo.M4`, `demo.M8` |
| 0:27–0:34 | G0 card | "The genuine record passes: hash, signature, public log, and the value recomputed from its own inputs." | `demo.G0` |
| 0:34–0:47 | L3 grid, south pixel dashed | "Then the receiver re-reads the source pixel, the one check a signature cannot make. Until the twenty-eighth of September, emem's own reader took the neighbouring pixel: 162 of 200 sampled records, signed faithfully, and wrong." | `demo.L3`, `M15.prevalence`, `M15.fix_date` |
| 0:47–0:54 | the bug-class table (§6) | "Any reader that computes its own pixel index can make that error. A re-read shows it." | `M15.generic` (INFERRED; `CHANGELOG.md:68` "GDAL takes the floor") |
| 0:54–1:00 | boundary + QR | "A signature fixes the bytes. It does not make the measurement true. Scan the code: your phone is the receiver." | `boundary`, `qr.demo` |

---

## 8. One source-of-truth manifest (proposed `docs/media/manifest.json`; the build fails on any mismatch)

```json
{
  "manifest_version": 1,
  "build": { "repo": "Vortx-AI/esa_poster", "commit": "<filled by build>", "built_utc": "<filled>",
             "claims_map": "research/repro/v13/claims.json", "claims_map_sha256": "<filled>" },
  "terms": {
    "hero": "Agents hand each other evidence references, not paraphrases.",
    "ladder": ["L0 bytes", "L1 identity", "L2 derivation", "L3 source", "L4 entity", "L5 truth, decision"],
    "integration_status": ["LIVE", "PROTOCOL", "REGISTRY", "EXAMPLE", "EXPERIMENTAL", "ROADMAP"],
    "mutation_ids": "research/repro/v11/mutation_suite.py MUTATIONS (+ R5 additions, 02 §0)",
    "banned": ["\\bverified\\b(?! (bytes|signature|log|L[0-5]))", "satellite decides", "spacecraft enrolled"]
  },
  "qr": [
    { "cta": "VIEW THE DEMO",        "payload": "https://vortx-ai.github.io/esa_poster/demo/",    "target": "same",                                                    "ecc": "Q", "version": 4, "symbol_mm": 70 },
    { "cta": "TRY A TOKEN",          "payload": "https://vortx-ai.github.io/esa_poster/t/",       "target": "https://emem.dev/verify?q=emem%3Afact%3Adefi.zb572.xoso.zb1ec%3Aoj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa", "ecc": "Q", "version": 4, "symbol_mm": 40 },
    { "cta": "INSPECT THE RECORD",   "payload": "https://vortx-ai.github.io/esa_poster/r/",       "target": "same",                                                    "ecc": "Q", "version": 4, "symbol_mm": 40 },
    { "cta": "RE-RUN THE TEST",      "payload": "https://vortx-ai.github.io/esa_poster/test/",    "target": "https://github.com/Vortx-AI/esa_poster/tree/main/research/repro/v13", "ecc": "Q", "version": 4, "symbol_mm": 40 },
    { "cta": "READ THE METHODS",     "payload": "https://vortx-ai.github.io/esa_poster/methods/", "target": "https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v13/METHODS.md", "ecc": "Q", "version": 4, "symbol_mm": 40 },
    { "cta": "DISCOVER INTEGRATIONS","payload": "https://vortx-ai.github.io/esa_poster/use/",     "target": "same",                                                    "ecc": "Q", "version": 4, "symbol_mm": 40 }
  ],
  "claims_used": {
    "rec.token":        { "value": "emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa", "source": "research/repro/v8/proof_bundle_ndvi.cbor#token", "label": "MEASURED" },
    "rec.value":        { "value": 0.4708994708994709, "print": "0.4709", "source": "same#entry.facts[0].value", "label": "MEASURED" },
    "rec.captured_at":  { "value": "2026-09-25T05:42:51.024000Z", "source": "same#entry.facts[0].sources[0].captured_at", "label": "MEASURED" },
    "rec.bytes":        { "value": 1115, "source": "same#entry.facts[0]", "label": "MEASURED" },
    "demo.M3":          { "value": "REFUSED at L0 (hash); byte 82 0x33->0x34; cid 47o5vzsv…", "source": "docs/demo/transcript.txt", "label": "MEASURED" },
    "demo.M4":          { "value": "REFUSED at L1 (cell defi.zb493.xuqA.zcb5f)", "source": "docs/demo/transcript.txt", "label": "MEASURED" },
    "demo.M8":          { "value": "REFUSED at L0 (signature); 0.45; cid ylcx42oi…; GET -> 404", "source": "docs/demo/transcript.txt", "label": "MEASURED" },
    "demo.G0":          { "value": "ACCEPTED L0-L2; log entry 2457078 under STH 2556451; witness 2541495", "source": "docs/demo/transcript.txt", "label": "MEASURED" },
    "demo.L3":          { "value": "B08 3502, B04 1900 re-read; NDVI bit-identical; tile 413", "source": "live in the browser; committed window research/repro/data/v8/pixel_windows.json", "label": "MEASURED (live per visit)" },
    "M15.south":        { "value": 0.3015512674990541, "print": "0.3016", "source": "research/repro/data/v8/pixel_windows.json", "label": "MEASURED" },
    "M15.prevalence":   { "value": "162/200", "wilson95": [0.75, 0.86], "source": "research/repro/data/v8/prevalence_summary.json#pre", "label": "MEASURED" },
    "M15.fix_date":     { "value": "2026-09-28T04:09:26Z", "source": "emem CHANGELOG.md:68; algorithms.md PIXEL_FIX_AT", "label": "SPEC" },
    "R1.A.false_accept":{ "value": "15/15", "source": "research/repro/v11/out/summary.md", "label": "MEASURED" },
    "xrt.paths":        { "value": "11/11 paths, 3/3 reps, 1 cid, 1 value", "source": "research/repro/data/v8/crossruntime_table.json#summary", "label": "MEASURED" },
    "verify.ms":        { "value": 11.7, "unit": "ms", "source": "demo/build/bench.mjs (Node 22, @noble)", "label": "MEASURED" }
  },
  "assets": [
    { "id": "M-A0",   "file": "docs/media/emem_a0.pdf",            "generator": "poster/build_v13.py",        "claims": "ALL on-board rows of claims.json", "qr": "all six", "sha256": "<filled>" },
    { "id": "M-PNG",  "file": "docs/media/emem_a0_300dpi.png",     "generator": "poster/build_v13.py",        "claims": "= M-A0", "sha256": "<filled>" },
    { "id": "M-SLIDE","file": "docs/media/emem_slide_16x9.pdf",    "generator": "poster/make_figures_v13.py", "claims": ["R5 or R1 headline", "M15.south", "M15.prevalence", "rec.value"], "qr": ["VIEW THE DEMO"], "sha256": "<filled>" },
    { "id": "M-D20",  "file": "docs/demo/index.html",              "generator": "demo/build/build.mjs",       "claims": ["rec.*", "demo.*", "M15.*"], "text_fallback": "docs/demo/transcript.txt", "sha256": "<filled>" },
    { "id": "M-D20v", "file": "docs/media/emem_demo_20s.mp4",      "generator": "demo/frames.mjs + ffmpeg",   "claims": "= M-D20", "max_seconds": 20, "sha256": "<filled>" },
    { "id": "M-D60",  "file": "docs/media/emem_demo_60s.mp4",      "generator": "ffmpeg (frames + narration)", "claims": ["R1.A.false_accept", "rec.*", "demo.*", "M15.*", "xrt.paths"], "captions": "docs/media/emem_demo_60s.vtt", "sha256": "<filled>" },
    { "id": "M-QR",   "file": "docs/index.html",                   "generator": "demo/build/site.mjs",        "claims": [], "sha256": "<filled>" },
    { "id": "M-SOC",  "file": "docs/media/emem_social_1200x627.png","generator": "card.html screenshot",      "claims": ["rec.value", "demo.*"], "sha256": "<filled>" },
    { "id": "M-HAND", "file": "docs/media/emem_handout_a4.pdf",    "generator": "poster/build_handout_v13.py","claims": "all handout rows", "qr": "all six at 22 mm", "sha256": "<filled>" }
  ]
}
```

Gates. The build refuses when any of these holds (INFERRED design; extends 01 §2's QR-gate gap and 03 §8):

1. A QR SVG does not decode (OpenCV, rasterised at print size) to its manifest `payload`.
2. A `payload`, followed through redirects, does not reach its `target` with HTTP 200, `text/html`, and no
   sign-in page. Test at 390 × 844, with the POST safety rule of this report.
3. A number in any asset's extracted text, or in an SVG `<text>`, is not in `claims_used` or the claims map.
4. A banned pattern appears.
5. `transcript.txt` was not regenerated in the same build as `demo/index.html` (their claim values must agree).
6. The 20 s video is longer than 20 s.
7. A `verified_utc` in the ecosystem manifest is older than 14 days (03 §8).

---

## 9. Build and deploy steps, in order (owner in brackets)

1. **[authors]** Enable GitHub Pages on `Vortx-AI/esa_poster`: Settings → Pages → Deploy from a branch → `main` →
   `/docs`. Add a LICENSE (the repo has none). INFERRED split: CC BY 4.0 for the poster and media, Apache-2.0 for code.
2. **[build agent]** Copy the prototype from `scratchpad/v13/demo/build/` to `poster/demo_src/` (verify.mjs, page.js,
   template.html, build.mjs, site.mjs, test.mjs, negctl*.mjs, bench.mjs, package.json pinning `@noble/hashes@1.5.0`,
   `@noble/curves@1.6.0`, `esbuild@0.24.0`), plus `keylong_tc_192.webp`. Its generator is in this report, §3.2.
3. **[build agent]** `node poster/demo_src/build.mjs . docs/demo && node poster/demo_src/site.mjs . docs`. Commit the
   built `docs/`.
4. **[experiment + methods agents]** Create `research/repro/v13/` (README with the one re-run command and the
   expected output) and `research/repro/v13/METHODS.md`. Until both exist on `main`, two QRs land on "File not found"
   (MEASURED s06).
5. **[authors]** Merge to `main` before printing. Every QR target is a `main` path.
6. **[build agent]** Generate the QR SVGs (`qr/make_qr.py` logic: ECC Q, `border=4`). Run the §8 gates. Re-test all
   six on a real phone (iPhone Safari and Android Chrome) and record the date and device in the manifest.
7. **[authors]** Record the 60 s narration. Add the ChatGPT screenshot (03 §9) before any ChatGPT mention.
8. **[optional, authors]** Rebuild the board track for v13 without the cell/recall step and re-sign it with the poster
   key (07 §3.1). Link it from `/r/`.
9. **[emem team, optional]** The verify-page fixes in §1.3. Correct the `llms.txt` CID rule (defect 24).

---

## 10. Open questions

1. Will Pages be enabled under `vortx-ai.github.io/esa_poster`? The other option is a path on emem.dev, which needs an
   emem change. Every payload depends on this choice and must be fixed before the QRs are drawn.
2. TRY A TOKEN: keep the one-hop redirect to emem.dev/verify (uniform small QRs, fixable after print), or print the
   110-character emem.dev URL directly (version 7, 45 modules, needs 99 mm for 1 m)?
3. Should the demo add a seventh, optional card, "a receiver that drops the cell accepts M4"? It is the Qwen result
   (24/24 cells dropped, 5/5 forged acted on). It is the strongest receiver-side warning, but it is uncommitted and
   makes the run 1.5 s longer.
4. Does the R5 agent experiment change the demo's prose line from the R1 number (15/15) to a model-measured rate? The
   manifest key `R1.A.false_accept` is the switch.
5. Dify shows "Verified by Dify" (LIVE d16), while 03 recorded `authorized_category: community`. Which does the
   ecosystem band print?
6. Safari (WebKit) is untested here. One phone test on iOS 16.4+ is owed before print.

---

## 11. Live calls made in this session (all read-only by the rule above)

- GET:
  - emem.dev pages `/verify`, `/verify?q=…` ×2, `/demos`, `/demos/handoff`, `/#use` ×2, `/.well-known/agent-card.json`;
  - `/v1/facts/{oj5cecci…, ylcx42oi…, 47o5vzsv…}` (200, 404, 404);
  - `/memories/by_attester/{iib5xjyf, lt2lf2qz, amrqpcmt}/` (all `count: 0`);
  - the ememdemo seal and modules;
  - GitHub, Dify, Glama, the MCP registries;
  - the Planetary Computer SAS token, plus range reads of 2 × 64 KiB headers and 2 tiles, several times.
- POST, allowed:
  - `/v1/memory_token/resolve`, issued by ememdemo and emem.dev/verify (about 6 calls; signs a response receipt and
    stores nothing, SPEC §1.3);
  - `/mcp initialize` (homepage probe);
  - A2A `emem_memory_view` and `emem_memory_list_by_kind` (ememdemo).
- POST, **blocked**: `/v1/recall` ×3 (ememdemo track, homepage ×2); `/mcp initialize` ×1 (first homepage run, before
  the rule allowed it); A2A `emem_memory_list_by_kind` ×1 (first ememdemo run).
- Nothing signed or published. No key file touched. The ememdemo device keys live only in the headless profiles.

---

## Appendix A. The 1,115 record bytes (hex; BLAKE3-256 → base32 = `oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa`)

```
ac646b696e64677072696d6172796463656c6c75646566692e7a623537322e786f736f2e7a623165636462616e646c69
6e64696365732e6e6476696574736c6f741950f16576616c7565fb3fde233788cde2336a636f6e666964656e6365fa3f
73333367736f757263657381a366736368656d656f73656e74696e656c5f73325f6c32616269647901d768747470733a
2f2f73656e74696e656c326c326130312e626c6f622e636f72652e77696e646f77732e6e65742f73656e74696e656c32
2d6c322f34332f532f46532f323032362f30392f32352f5332415f4d53494c32415f3230323630393235543035343235
315f4e303531335f523030355f5434335346535f3230323630393235543039303031352e534146452f4752414e554c45
2f4c32415f5434335346535f413035383830345f3230323630393235543035343234352f494d475f444154412f523130
6d2f5434335346535f3230323630393235543035343235315f4230385f31306d2e746966203b2068747470733a2f2f73
656e74696e656c326c326130312e626c6f622e636f72652e77696e646f77732e6e65742f73656e74696e656c322d6c32
2f34332f532f46532f323032362f30392f32352f5332415f4d53494c32415f3230323630393235543035343235315f4e
303531335f523030355f5434335346535f3230323630393235543039303031352e534146452f4752414e554c452f4c32
415f5434335346535f413035383830345f3230323630393235543035343234352f494d475f444154412f5231306d2f54
34335346535f3230323630393235543035343235315f4230345f31306d2e7469666b63617074757265645f6174781b32
3032362d30392d32355430353a34323a35312e3032343030305a6a64657269766174696f6ea266666e5f6b6579781c73
656e74696e656c325f6c32615f696e64696365735f6e647669403164617267738dfb4040491f0a48f854fb40534234e1
08d38478365332415f4d53494c32415f3230323630393235543035343235315f523030355f5434335346535f32303236
3039323554303930303135197f8378394e445649203d202842303820e288922042303429202f2028423038202b204230
34292e2056656765746174696f6e20677265656e6e6573732e82f96ad7f9676cfb4025ae21d96e9bbff95100181e0401
783a68747470733a2f2f706c616e6574617279636f6d70757465722e6d6963726f736f66742e636f6d2f6170692f7374
61632f76312f736561726368f9e3d06d707269766163795f636c617373667075626c69636a736368656d615f63696478
346432347267776c713437613569736d35766b6b626975617633776932766f65777171677934783474746e68646e7a7a
6979666b71667369676e6572982018ff18fe184818ef08183918901858183218bd183b0518ab185918981896184c1831
18e41864188e184f182b18fa182418bf183018e0182a18ce18651854697369676e65645f617474323032362d30392d32
385430393a30363a35365a
```

- Mutation M3: byte 82 (0-based, the last byte of the f64 value at bytes 75–82) `33` → `34`.
- Mutation M8: bytes 75–82 `3fde233788cde233` → `3fdccccccccccccd`.
- Both copies remain valid CBOR of the same length (MEASURED: `cbor2.loads` returns 0.47089947089947093 and 0.45).

## Appendix B. The receiver core, `verify.mjs` (168 lines; sha256 `366f9180…cf85b5`)

The file is at `scratchpad/v13/demo/build/verify.mjs`. It holds:

- base32, hex and byte helpers;
- a minimal CBOR reader with raw item spans (no re-encoding);
- RFC 6962 inclusion and consistency proofs, and the batch Merkle root (rule v1 and the v0 legacy rule);
- `parseToken`, `valueOffset`, `ndvi` and `recompute`;
- `mutations` (M3, M8, the M4 cell);
- `makeReceiver` (§3.3 steps 1–8);
- `rereadPixel` (§3.3, L3).

It is a line-by-line port of the committed `research/repro/v8/verify_bundle.py` and
`research/repro/v12/scripts/verify_lib.py`. It must be copied into the repo with the prototype (§9 step 2).
INFERRED reason it is not reproduced inline: the committed Python already holds every formula and preimage it
implements (§3.3 cites them), and the JS was checked against it: identical verdicts and CIDs for G0, M3, M4 and M8
(MEASURED `test.mjs`), plus the three negative controls.

## Appendix C. Prototype and evidence inventory (scratchpad = `/tmp/claude-0/-home-user-esa-poster/0db6b3ad-8059-51a6-bd74-2d7a97faf986/scratchpad/v13/`; ephemeral, so copy before the session ends)

| path | what | sha256 (prefix) |
|---|---|---|
| `demo/build/verify.mjs` | receiver core | `366f9180a9fb9b28` |
| `demo/build/page.js` | browser UI and timeline | `8b5713d1a91a33bc` |
| `demo/build/template.html` | page HTML/CSS, CSP `connect-src` emem.dev, planetarycomputer.microsoft.com, sentinel2l2a01.blob.core.windows.net | `bdf192d114db5e33` |
| `demo/build/build.mjs` | builds `demo/index.html` + `transcript.txt`, asserts the verdicts | `804f8e81671cce16` |
| `demo/build/site.mjs` | landing, `/r/`, `/use/`, redirects | `5e907878a2a8a3b4` |
| `demo/build/{test,negctl,negctl2,bench}.mjs` | parity test, negative controls, timing (negctl.mjs's first case is void: its byte search missed the CBOR uint-array signature and flipped a fact byte; negctl2.mjs replaces it) | `9b9de429…`, `270fd93f…`, `16daf0a1…`, `f5a745ad…` |
| `demo/keylong_tc_192.webp` | true-colour crop from the committed grids | `7d2f7cfc739ec4ab` |
| `demo/fact_oj5.cbor` | the 1,115 record bytes (= Appendix A) | `0628924d906e1984` |
| `demo/site/` | the built site (`demo/index.html` 86,469 B `a36fb721…`; `demo/transcript.txt` `10c42f7d…`) | |
| `qr/make_qr.py`, `qr/qr_*.svg`, `qr/qr_*_300dpi.png`, `qr/qr_sim.py`, `qr/qr_table.json` | proposed QR set, decode gate, size model | `d48b2db4…`, `2653b538…` |
| `mobile/mobile.mjs`, `mobile/record.mjs`, `mobile/frames.mjs` | phone harness (with the POST safety rule), video capture | `ab773851…`, `a0e58c55…` |
| `mobile/out/*.png`, `*.json` | 71 screenshots and one JSON per destination (d01–d24, s01–s09: status, timings, requests, blocked POSTs, above-the-fold text, page text) | |
| `mobile/out/demo_phone.mp4`, `demo_phone_lastframe.png` | 20 s video feasibility (12.93 s) and its last frame | `db13d8eff4d6c736` |
