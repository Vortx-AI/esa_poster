# 07 · Branch assets: what this line of work holds, and what the final A0 should carry

Written 2026-10-01 for the v13 research phase. Read-only: no record was signed or published, no key file was touched,
no file outside this report was changed. Every item carries one label:
**MEASURED** (computed here or by a committed script, with its output), **LIVE** (read from emem.dev, ememdemo or GitHub
on 2026-10-01 with GET, or by opening a page in a browser), **SPEC** (what emem's code or docs say at `18adb67`),
**INFERRED** (my reasoning from the above), **UNVERIFIED** (stated somewhere, not checked).

Sources: this repo at `dc2463e` (branch `claude/tender-planck-clvh1p`); emem at `origin/main 18adb67`; the live
server reports `x-emem-commit 8e9b401c` (`03_ecosystem_manifest.md`), so live behaviour may differ from `18adb67`.

---

## 0. Findings in one screen

1. **The ememified board works today, from a phone-class browser, in about 9 seconds.** LIVE 2026-10-01T00:33:31Z:
   ememdemo opened the sealed v11 track `qfkcuqcm…`, re-checked **30 of 30** steps, recomputed the chain to head
   `sxmlncauzw…`, and checked the note's inclusion as log entry 2,573,960 ("the log has grown 657 entries since and
   still holds that history"): 8.9 s, 61 requests, no account. Independently, I fetched the note (5,571 B, bytes hash to
   its name), recomputed all 30 chain links with stock blake3 (head matches), and re-hashed 28 of the 30 steps by GET
   (the bundle and the state are checked by other routes). It is the strongest ready-made answer to issue #34
   ("INSPECT THE RECORD") on either line of work. v12.1 has no equivalent: its QRs open `emem.dev/verify` and a GitHub tree.
2. **A 20-second "mutation → REFUSE" demo already exists, with nothing to publish** (issue #35). LIVE: ememdemo with the
   real Keylong token: "signed record ✓ … its bytes hash to its name", 322 ms, 5 requests. The same cid under the
   Bengaluru cell: "stopped, 1.3 s, 6 requests … emem.dev said 409: token cell … does not match the signed fact's cell …
   refusing to dereference a mislabeled handle." Two QRs, two URLs, no sign-in. Limit: the refusal comes from the server
   (409). The browser itself checks the valid case (re-hash) but only relays the forged case.
3. **The pre-registered Qwen arm is the branch's most important unpublished result. It is the user's "catastrophe"
   point, observed and measured.** MEASURED from `scratchpad/v8/followup-G2-two-llm-plugin-handoff/qwen_trials.jsonl`
   (52 rows; **not committed, not in `results.json`**). Qwen2.5-3B as receiver dropped the cell from **24 of 24** tokens
   it was given (19 genuine, 5 forged), resolved the bare cid, and got HTTP 200 with `cell_matches: false`. On the forged
   cell it **acted 5 of 5** (Claude Haiku 4.5 declined 5 of 5). It also misapplied the threshold: token arm 0 of 19
   correct while quoting 0.4709, prose 10 of 18 (two-sided Fisher p = 1.3 × 10⁻⁴, against the token arm).
   The finding: **a reference protects only a receiver that keeps it whole and obeys a refusal.** That is the
   receiver-side half of the threat model, and the new agent-level experiment (`02`) must test it.
4. **The 15-link independent trace already gives the verification ladder its "what is still trusted" column**
   (MASTER §11, §12; issues #17, #29). MEASURED 2026-09-30, 17 checks, 17.9 s, no emem code. Re-run today offline:
   the 4,906-byte bundle passes 9 of 9 checks with the network unreachable (`unshare -rn`). A one-bit flip in the value
   fails it, and so does a wrong signer key. The v12.1 guarantees table has the rungs, but not the residual trust.
5. **Three production cases share one shape. In each, the record was intact and the referent was wrong, and the record
   located the error.** The pixel (M15, already on v12.1). The date: asked for 23 Sep, the tool served the byte-identical
   25 Sep scene; all 10 agents saw one scene twice, 9 never got 23 Sep values, and 3 then wrote that no 23 Sep acquisition
   existed. The place: `/v1/ask` answered from the town point, 597 m from the coordinates asked, and its `emem:state`
   reasoning stage re-hashes 4 of 4 while recording that wrong stage. This triad is the "wow, why emem" panel: other
   pipelines make these errors silently, and here the bytes say where each error happened.
6. **Ecosystem (#43):** one token resolves to one cid and one value through **11 client paths** (MEASURED, 3 reps), and
   through **two model runtimes** in G2: Claude Code CLI and llama.cpp with the official MCP Python SDK. The adapters do
   not all carry the proof. LlamaIndex's tool spec drops the receipt, A2A at default verbosity elides the receipt bytes,
   and langchain-mcp-adapters returns a refusal as ordinary text. These last results sit only in the scratchpad.
7. **The token-family table should not go on the face.** Seven formula findings in `00_v11_review_findings.md` apply to
   it (M2, M6, M9, M10, M11, M14, M15). The code has 11 `emem:` prefixes (it adds `emem:attestation:`), so "14 kinds"
   counts data needs, not grammars. What survives is a three-tier legend for the evidence object (#28). Only
   `emem:tree` hashes upstream file bytes. A fact cid hashes the canonical record, which names its source but carries
   no hash of it (`Source.hash` is never filled, defect 25). That is MASTER §5 in one line.
8. **Ephemeral evidence must be committed before anything here is printed:** `qwen_trials.jsonl` (blake3 `cb6e6369…`),
   `prereg_addendum*.md`, `crossruntime/refusal_matrix.json`, `refusal_ts.json`, `untrusted_mirror.json`, and the G2 and
   cross-runtime scripts. All of them sit in this session's scratchpad (§6).

---

## 1. What is unique to this branch

MEASURED (git): v8 to v10 of this branch reached `main` through PR #2 to #4 (merge `50bb8bf` took `49f8e6c`, the v10
seal). Their files are on `main`, but the main-line boards (v11 `aff0c21` to v12.1 `1ee1c04`) were rebuilt by another
agent and carry almost none of them. Only two commits were never on `main` before the merge `8a867f4`:

| commit | content |
|---|---|
| `6eb27a9` | v11 board, seal blank: token family (14 rows), Keylong cell with 13 products, reasoning-stage tokens, defect 37; `research/repro/data/v11/*`; `rehearse11/` |
| `9a9933e` | v11 seal: board pointer `xu344qmk…`, evidence pointer `6wmlonyq…`, track `qfkcuqcm…` (30 steps), `pub/b_v11`, `e_v11`, `track11`, `tdry_v11` |

"This branch's line" therefore means the v8 to v11-sealed research. Its files are physically on `main`, apart from the
`data/v11/` and v11 seal files, but its content is not on the v12.1 board.

Note: the local `main` ref (`c5767f6`, "Add editable scientific poster wireframe" and two more) is not `origin/main`
(`4a1567f`). It is 426 files behind the branch. I did not use it.

---

## 2. Inventory

| # | asset | where | what it shows | label | re-checked 2026-10-01 |
|---|---|---|---|---|---|
| A1 | sealed board + signed track.v1 | `poster/archive/v11-sealed/`, `research/repro/v8/make_track.py`, `pub/track11/` | every § on the board is one step of a hash-chained, logged note; the QR opens it in ememdemo | MEASURED + LIVE | yes: 30/30 in ememdemo; chain recomputed; 28/30 re-hashed by GET; board.jpg sha256 `42690cb9…` and 3 chunk hashes match the pointer note |
| A2 | token family (14 rows) | v11-sealed panel "The token family" | data need → token → what its id hashes | SPEC (with errors) | code re-read at `18adb67`; bundle rule recomputed |
| A3 | `emem:state` reasoning stages | `data/v11/ask_keylong.json`, `recompute_state.py`, `verifier_spec.json` | the 4 `/v1/ask` stages are content-addressed and recompute | MEASURED + LIVE | 4/4 recompute; `GET /v1/state/ppfjf5te…` `address_holds: true` |
| A4 | 15-link independent trace | `v8/trace_fact.py` (698 lines), `trace_fact_output.txt` | token → bytes → cell → derivation → STAC → COG pixel → receipt → batch → log → witness → key/domain, each with "residual trust" | MEASURED 2026-09-30T09:15:45Z | offline subset (bundle) 9/9 PASS today; tamper and wrong key fail |
| A5 | cross-runtime table | `data/v8/crossruntime_table.json` | 11 paths × 3 reps, 1 cid, 1 value; receipts verify on 9/11; latency per path | MEASURED 2026-09-30T08:40:43Z | not re-run (resolve signs receipts) |
| A5b | refusal matrix, untrusted mirror | scratchpad `v8/crossruntime/` only | wrong-cell token raises or flags an error on 8 paths; LangChain returns the refusal as text; tampered mirror passes receipt, fails re-hash | MEASURED, **uncommitted** | read from files |
| A6 | two-LLM pre-registered handoff (G2) | `data/v8/results.json`, `prereg.md`; Qwen arm in scratchpad | Claude arms; adverse Qwen arm | MEASURED (Qwen **uncommitted**) | prereg blake3 `67631a79…` matches the hash logged 10:46:12Z |
| A7 | pre-registered raw-band run | `data/v9/rawband/` | the date substitution, from the agent's side | MEASURED | prereg blake3 `30d8a1a1…` recomputed |
| A8 | Keylong cell, 207 facts / 13 products | `data/v11/cell_keylong.json`, `cell_products.json` | one address, many products | MEASURED 22:43:38Z 30 Sep | LIVE now 208 facts, 14 products |
| A9 | drift taxonomy (7 real cases) | v11-sealed panel 7 | each drift ↔ one equality test | MEASURED/SPEC (with errors F2, F3, F13) | mapped to R1 ids below |
| A10 | scene-to-token cost | `data/v8/cog_pixel_bytes.json`, `scene_sizes.json`, `token_counts.json` | 1,165,033 B read of 2,023,818,762 B; 1,115 B record; 84 chars / 46 tokens | MEASURED (read path reconstructed) | arithmetic re-done |
| A11 | source-file pointer notes (`emem:tree`) and `range_hash` | `pub/b04` (B04 note `h6d7xdoc…`); B08 note `khiqtqrd…` has no committed publish log; trace link 9c | the upstream COG can be content-addressed; the fact does not do it | MEASURED | B08 note LIVE: 238,683,874 B, 292 of 292 chunks, re-hashes to its name; the 1,586,895 B tile row is present |
| A12 | algorithms with file:line | `research/repro/v10/algorithms.md` | 15 formulas as coded at `18adb67`; doc-vs-code differences | SPEC | spot-checked: bundle, state, entity, cell_matches |
| A13 | defects 1–37 | `research/do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md` | the raw material for the failure classes | MEASURED/SPEC | 24 and 31 still LIVE |
| A14 | "Where emem lost", "Since acceptance", "Ememify", traffic footer | v11-sealed panels 9–11, footer | authors' scorecard, retired encoders, 5 how-to steps, counts | mixed; several UNSUPPORTED (F4–F7) | — |

---

## 3. Asset by asset

### 3.1 (a) The ememified board: the signed track and the seal QR

**What it is (SPEC/MEASURED).** `make_track.py` builds a `track.v1` note: 30 ordered references: 13 pointer notes (the board, two COG files, two CHANGELOG lines,
doc rows, the measurement files), 12 facts, 1 raster, 1 cube, 1 bundle, 1 cell, 1 state. Each chain link is
`base32(BLAKE3(link_{i−1} ‖ ref_i)[:16])`, with `link₀ = cid("")`. Step 1 is a pointer note that hashes `board.jpg`
rendered with the seal box blank. `publish_note.py` stamps the note with a verified log head, sends it unsigned
(MCP and A2A both refuse and name the same digest; `digests_agree: true` in every `publish_log.json`), then signs
with the poster key `njedkglt…`. A file cannot contain its own hash, so the seal box is the only unhashed area.

**Checks today.**
- LIVE, ememdemo in headless Chromium driven over CDP (`scratchpad/ememdemo/cdp.mjs`): "stored note the track matches
  its name · steps checked again: 30 of 30 · logged as entry 2,573,960 (inclusion proof checked here) … chain recomputed
  and matches its head … the log has grown 657 entries since and still holds that history · checked at 00:33:31Z by
  this browser"; "ememified 8.9 s, 61 requests; fetched 1.4 s; proven 7.5 s". One run, container network, through a proxy.
  The browser trusted only the proxy's own CA key (`--ignore-certificate-errors-spki-list` = SPKI of
  `/root/.ccr/agent-proxy-ca.crt`), because the profile's NSS store predates that CA. The viewer made a local key
  (`kccdabe6`), and its namespace is empty (`GET /memories/by_attester/kccdabe6/` → `total: 0`), so nothing was published.
- MEASURED: `GET …/qfkcuqcmhvswbe5slcyoxjkwoe.md` is 5,571 B, byte-equal to `pub/track11/note.md`, and re-hashes to its
  name. All 30 links recompute, and the head is `sxmlncauzwifezmahgyo7mpkti`.
- MEASURED: steps 1–15, 17–28 re-hash by GET (`/v1/facts/<cid>` CBOR for facts and for the derivation cids of the raster
  and cube; note bytes for pointer notes). Step 29: `GET /v1/cells/…` now lists 208 facts. Step 30: `GET /v1/state/…`
  gives `recomputed_cid == cid`, `address_holds: true`. Step 16 (bundle) is POST-only and was not re-run. Its cid
  recomputes offline from `bundle_mint.json` with the code's preimage (`6x5eoxguweqw46n3gvpaqe3e3a`).
- MEASURED: `git show 6eb27a9:poster/board.jpg` is 2,769,887 B, sha256 `42690cb98dd0…c0f7` as printed on the seal. The
  three chunk BLAKE3s equal the rows of pointer note `xu344qmk…`.

**Is it strong for the final board?** Yes, as the "INSPECT THE RECORD" destination, and it is the only thing either
line has that a visitor can run on the spot. INFERRED reasons:
- It is the poster's own claim applied to the poster. A visitor's browser re-hashes every cited record and checks the
  log position, without trusting the authors' prose. That is MASTER §4 in miniature.
- It meets #34 (one verb-led destination opening the artifact itself; tested path) and #35 (well under 20 s, no account,
  exact input and output on screen; the page has a text form).
- ememdemo verifies its own code before it runs ("sealed · 18 of 18 files checked · signed by ddzmyzhn"), so the
  checker is itself content-addressed.

**What it does not show (state on the board or the landing page).**
- It certifies the *published digital board* (board.jpg), not the paper in front of the visitor (INFERRED).
- The track is signed by an unaffiliated poster key ("T1 keyed · a key that signed its own namespace; not named, not
  affiliated", LIVE ememdemo text). It proves integrity, order and log position, not authorship by the named authors.
- "Verified: 30 of 30" inside the note is the author's assertion. The viewer's re-check is the evidence.
- The track carries no entity or rasterset step, because ememdemo cannot check them: the rasterset resolve returns no
  receipt (defect 23), and the entity receipt is still preimage v1 (defect 31; LIVE 2026-10-01: `preimage_version: 1`,
  `served_at 2026-07-12`). So 30/30 holds over the kinds the viewer can check.
- ememdemo's own `llms.txt` line 2 still states the wrong note-cid rule, `base32(blake3(bytes))[0:26]` (defect 24,
  LIVE 2026-10-01). For this track it gives `…kjwof` instead of `…kjwoe`, so an agent that implements the published
  rule rejects the poster's valid track. That is a live example of checker/producer drift.

**How to keep it without internal-history language (#37).** INFERRED recommendations:
- Drop the "§n" numbering spread across the face. It collided with panel numbers (`16_V11_CRITIQUE_AND_DECISIONS.md` §1.4)
  and reads as build apparatus. Instead, put one small mark (for example "▣ record") on each figure or number that is a
  track step, and one QR box: **"Check this board: your phone re-hashes the records behind every number and checks the
  public log (about 9 s)."**
- Relabel the track's steps in scientific language. A visitor sees these labels in ememdemo. Current labels such as
  "pre-fix record, 23 Sep, pixel south", "sizes and the authors scorecard" and "the record and 19 withdrawals" are
  process language. The labels must stay at most 40 characters with no colon (`make_track.py` assertion).
- Rebuild the track for the v13 board: render → board pointer at the final commit → track → fill the seal. This needs
  the poster key, a signing step that only the authors may take. Re-scan the QR on the print proof; review finding F10
  says a 30 mm QR does not decode at 1 m, so print at 40 mm or more.
- **Add the #35 pair of QRs**, which needs no publishing: "TRY A TOKEN"
  `https://vortx-ai.github.io/ememdemo/?s=emem%3Afact%3Adefi.zb572.xoso.zb1ec%3Aoj5cecci…` and "SEE A REFUSAL", the same cid
  under `defi.zb493.xuqA.zcb5f` (LIVE results in §0.2). Caption the second honestly: "refused by the responder (HTTP 409);
  your browser shows the reason."

**Verdict: KEEP (as one QR box and the #35 pair), REBUILD the track for v13, DROP the § apparatus and the seal prose
from the face.**

### 3.2 (b) The token family

**What the code says (SPEC, `18adb67`).** `git grep -ohE 'emem:[a-z_]+:'` over `crates/` and `docs/` finds 11 real
prefixes: fact (6,777), raster (309), bundle (289), entity (243), cube (193), rasterset (68), cell (67), trace (42),
tree (28), attestation (26), state (25). The others are test strings or old proposals (`emem:v:`, `emem:latest:`,
`emem:derived:`, `emem:banana:`). `track.v1` is an ememdemo note format, not an emem token. The v11 table's 14 rows count
data needs: absence, embedding and derived are rows of `emem:fact:`. It omits `emem:attestation:`.

**What each id hashes** (corrected with `00_v11_review_findings.md` M2, M6, M9–M11, M14, M15; checked in code):

| tier | token | the id is | binds the observed bytes? |
|---|---|---|---|
| record | `emem:fact:<cell>:<cid>` | `b32(BLAKE3-256(emem-CBOR(record)))`, 52 chars; the record holds value, DNs, scene id, COG URLs, offset, signer, signed_at (fact.rs; cbor.rs) | it hashes the **canonical record**, which *names* the source; `Source.hash` is never filled in production (defect 25), so it does not hash the COG |
| record | `emem:raster:<aoi>:<band>:<tslot>:<d>` | `d` = fact_cid of a derivation record that holds `artifact_cid = BLAKE3(EMEMGRD1 grid)` (band_raster.rs:381-436) | yes, through `d`: the emem-harmonised pixel grid, not the COG bytes |
| source file | `emem:tree:<note-cid>#row=i` | the note's own `BLAKE3[:16]`; the note holds a Merkle root over `(url, offset, length, BLAKE3(chunk))` (tree.rs:65-143) | **the only id that hashes upstream file bytes** |
| list | `emem:bundle:<cid>` | `BLAKE3("emem.memory_bundle.v1|" purpose "\n" Σ cell|band|tslot|fact_cid? "\n")[:16]` (memory_bundle.rs:155-182) | no; a list. A citation may leave `fact_cid` empty and point at an address, not a record (SPEC); the poster's bundle pins all 8 (MEASURED) |
| list | `emem:cube:…:<d>` | `d` = fact_cid of the band_cube record holding `BLAKE3(CBOR([member d…]))` (M10) | no; a list of rasters |
| list | `emem:rasterset:<set>:<d>` | `BLAKE3(CBOR([d…, "purpose:p"]))` | no; a list |
| list | `emem:state:<cid>` | `BLAKE3(CBOR{schema, kind, derived_from[prev, facts], payload, class, does_not_cover, responder_pubkey})`, field order, not RFC 8949 sorting (lib.rs:20818-20829) | no; a stage record that cites facts; **unsigned** |
| list | track.v1 head | `BLAKE3(link ‖ ref)[:16]` chain | no; an ordered list |
| name | `emem:entity:<cid>` | `BLAKE3(identity preimage)[:16]`: the external id alone (OSM, GERS, Wikidata) if one is known, else (cell, kind, label) (entity.rs:11-19) | no; a label (M17) |
| name | `emem:cell:<cell64>` | the quantised lat/lng itself, no hash (geo.rs:137-172) | no |
| device | `emem:trace:`, `emem:attestation:` | BLAKE3 of the signed OS trace / platform attestation | the device's own output digests; no hardware enrolled (SAT-042 extension) |

INFERRED threat-model note (MASTER §12): fact ids are 256-bit. Bundle, entity, note, track-link and `reason_cid` ids are
128-bit truncations: second preimage about 2¹²⁸, collision about 2⁶⁴. "Cannot produce the same content address for
different bytes" holds as stated for facts. For the 128-bit ids, the claim should name the length.

**Verdict: DROP the 14-row table from the face** (MASTER §26 "not a giant API/schema reference"; #18).
**MERGE** the three-tier legend (record / list / name) into the evidence-object figure (#28), with the one sentence
MASTER §5 needs: *"The fact id hashes the record. The record names the satellite file. Only a tree token hashes the file
itself."* Keep the full table behind "READ THE METHODS", corrected as above.

### 3.3 (c) `emem:state`: reasoning-stage tokens

**MEASURED.** `python recompute_state.py ask_keylong.json verifier_spec.json` → located ✓ `mps3ysem…`, routed ✓
`l3hg7ydh…`, recalled ✓ `sz4zbhgo…`, scored ✓ `ppfjf5te…`. It uses stock cbor2 + blake3 with the field order from the
published golden vector, and checks that vector's hex first. **LIVE:** `GET /v1/state/ppfjf5te…` returns the record,
`recomputed_cid == cid`, `address_holds: true`.

**Scope (SPEC, lib.rs:20818-20829, 23099-23170).** These are stages of emem's own `/v1/ask` pipeline:
`"class": "deterministic_index: no stage here consults a model"`. A state is **not signed** ("addressed by its content,
and the responder key inside it says whose derivation it was"). No route lets an agent mint its own reasoning state
(`POST /v1/state` is an embedding endpoint). So "verifiable agent reasoning trace" overstates it. The accurate phrase:
**"each stage of the responder's answer pipeline has an address that anyone can recompute."**

**The strong use.** MEASURED (`ask_keylong.json`) plus a WGS-84 geodesic (pyproj): the question was "What is the NDVI at
Keylong, Lahaul (32.57126 N, 77.03448 E)?". The `located` stage payload says `input: "Keylong"`,
`extracted_from_question: true`, and gives the town point (32.5717891, 77.0281479), cell `defi.zb572.xAnI.zb1a2`,
597.3 to 597.5 m from the asked point. The answer was NDVI 0.28, from that cell. The stage chain re-hashes 4 of 4 and
records the wrong step exactly. This is **"the right trace, the wrong place"**, the reasoning-layer twin of M15. The
token check `cell(b) = cell(token)` passes, because the fact really is at the town cell. What exposes it is the answered
cell differing from the cell of the asked coordinates (review M13/F3). Fix status: no CHANGELOG entry at `18adb67`, and
none in the remote `main` CHANGELOG `[Unreleased]` section retrieved 2026-10-01 (INFERRED: unfixed; not re-tested live,
because `/v1/ask` signs records).

**Verdict: MERGE** into the failure triad (§4) as the "wrong place" case, with a single line on the stage address.
**DROP** "reasoning-stage tokens" as a contribution. It is an extension, like SAT-042 (MASTER §20).

### 3.4 (d) The 15-link independent trace: what remains trusted

MEASURED (`trace_fact_output.txt`, run 2026-09-30T09:15:45Z, all 17 checks VERIFIED, 17.9 s). Mapped to the MASTER §11
ladder, with each link's own "residual trust" line, condensed:

| rung (MASTER §11) | links | result on the Keylong record `oj5cecci…` | still trusted after the check |
|---|---|---|---|
| L0 bytes | 1–3 | 1,115 B re-hash to the cid; flipping the value's last mantissa bit gives `mu5x2cks…` | nothing; availability of a copy |
| L1 identity | 4–5 | cell in the bytes = cell in the token (wrong cell → 409); cell decodes to the derivation's lat/lng | nothing |
| L2 derivation | 6–7 | scene id, DNs 3502/1900, offset −1000, catalogue inside the bytes; NDVI recomputed bit-for-bit (`0x3fde233788cde233`) | argument positions are read from emem's code; there is no published per-function schema |
| L3 source | 8–9c | PC STAC item matches 10 fields; own TIFF decoder reads B08 3502 / B04 1900 at (9098, 9443); SCL 4; emem's signed `range_hash` of the tile equals ours | STAC is Microsoft's statement and has no checksum; the floor/PixelIsArea rule is emem's choice; **the fact commits to no COG hash**; nothing binds Microsoft's COG to ESA's product |
| (serving) | 10–11 | receipt Ed25519 valid; proof-stripped and v1-downgraded variants fail; single-fact batch root | proves what emem.dev served, not that it is true; the proof covers `fact_cids[0]` only |
| (log) | 12–14 | entry 2,457,078 in a 2,556,451-entry log; consistency with our earlier head and with geo.qa's co-signed head | no fact_cid→leaf index (21 bisection probes); a first-contact client cannot see a split view; **geo.qa is also Vortx AI** |
| (key) | 15 | key in did:web, JWKS, emem.json, DNS TXT (two resolvers) | Web PKI; DNS without DNSSEC (AD=false) |
| L4 entity, L5 truth | none | not tested by any link | everything |

MEASURED today: `unshare -rn python3 verify_bundle.py proof_bundle_ndvi.cbor` gives 9 PASS with the network unreachable
(a urlopen inside the namespace fails with Errno 101). Flipping one bit of the value, or passing a 52-char wrong key,
gives "SOME CHECKS FAILED". LIVE today: `/v1/log/witnesses` reports `independent_operator_domains: 1`,
`head_is_independently_witnessed: false`, tree size 2,574,653.

Correction to carry (review M8): the v11 acceptance predicate lists only the receipt signature. It must also list the
attester's signature over the batch root, link 12: `… ∧ Ed25519_att(R) ∧ Ed25519_σ ∧ …`.

**Verdict: MERGE as the backbone of the ladder figure (#17, #29).** Each rung: a check, its result on the hero record,
and a grey "still trusted" line. That is exactly how MASTER §11 asks to label "verified". Put the offline 4,906-byte
bundle behind a "RE-RUN THE TEST" QR, with one 30-cm line: "9 checks, no network, 4.9 kB."

### 3.5 (e) Cross-runtime: ten client paths, one cid (issue #43)

**MEASURED** (`crossruntime_table.json`, 2026-09-30T08:40:43Z, server `213e273`, 3 reps per path). The Keylong token
gave cid `oj5cecci…` and value 0.4708994708994709 on all 11 paths, with `rehash_ok` on all. The Bengaluru token gave
918.0 on 10 paths. Median latency per path, in ms: REST 223.5, raw MCP 223.7, A2A `message/send` 226.3,
Python SDK 2.4.2 207.7, TS SDK 2.4.0 58.6, LlamaIndex FunctionTool 300.8, langchain-mcp-adapters 1,176.8,
official MCP Python SDK 56.3, official MCP TS SDK 58.3, independent blake3+cbor2 235.6, A→B isolated processes 772.8.
The receipt verifies on 9 of 11 paths.

**What the table also found (MEASURED; the last three items are in the scratchpad only):**
- LlamaIndex `EmemToolSpec` returns a trimmed dict with **no receipt** ("receipt dropped by the tool spec").
- A2A at default verbosity elides the receipt byte arrays: "inner receipt offline-verifiable: None". It needs
  `verbosity: full`.
- The TS SDK 2.4.0 has no public resolve method.
- `refusal_matrix.json`: a wrong-cell token is refused on REST (409), raw MCP (`isError`), A2A (−32602), the Python SDK,
  LlamaIndex (HTTP 409 raised), the official MCP Python SDK, and the TS SDK and MCP TS SDK (`refusal_ts.json`).
  **langchain-mcp-adapters returns the refusal as ordinary text**, so an LLM receives "tool error (−25): token cell … does
  not match" as content, not as an error.
- `untrusted_mirror.json`: a mirror that changes the value by +0.1 still passes the receipt check (`receipt_sig_ok: true`).
  Only the re-hash fails (`j47f4xb3…` ≠ cid). **The content address catches what the signature does not.**

**Against #43.** The table shows protocol and SDK interoperability, not "two agent environments". G2 adds the model level:
the same token passed from Claude Sonnet 5.5 in Claude Code CLI (A) to Claude Haiku 4.5 in Claude Code CLI and to
Qwen2.5-3B under llama.cpp with the official MCP Python SDK (B). Two runtimes, opposite outcomes on a forged cell (§3.6).
Not demonstrated: ChatGPT, Dify, Gemini CLI or any host pair with a model in the loop (`03` §3: "NOT DONE").

**Verdict: MERGE into the ecosystem band.** Printable line (MEASURED): **"One token, eleven client paths, one cid (30 Sep
2026)."** Add the adapter finding at the 30-cm tier: "the proof survives the protocol, not every adapter: one drops the
receipt, one returns a refusal as text." Commit the scratchpad files first (§6). Leave "resolved in ChatGPT and Claude"
off until `02` runs it.

### 3.6 (f) The two-LLM pre-registered handoff, including the adverse Qwen arm

**Design (MEASURED, `prereg.md`, blake3 `67631a79…`, which equals the value logged at 10:46:12Z in `raw/prereg.blake3`).**
- A: claude-sonnet-5-5 via `claude -p`, emem as the only MCP server, n = 10.
- B: claude-haiku-4-5 (Claude Code CLI, full emem plugin), or Qwen2.5-3B-Instruct Q4_K_M (llama.cpp, harness tool
  `resolve` via the official MCP SDK).
- Constructed rule: IRRIGATE iff NDVI ≤ 0.4705, set 0.0004 below the signed 0.4708994708994709.
- Arms T (token), P (A's prose), F (real cid under a wrong cell). R ("0.47" prose) is an exploratory addendum
  (10:51:38Z, after A, before B).

| B | T token | P prose | R "0.47" (expl.) | F forged cell | source |
|---|---|---|---|---|---|
| Claude Haiku 4.5 | 10/10 correct; resolve 10/10 | 10/10 | 0/5 (5× IRRIGATE) | **5/5 declined** | `results.json` |
| Qwen2.5-3B | **0/19** (19× IRRIGATE; 17 quote 0.4708994708994709, 2 quote 0.4709) | 10/18 | 2/10 (+4 DECLINE) | **0/5 declined: 5/5 acted** | scratchpad `qwen_trials.jsonl`, 52 rows, **uncommitted** |

Tests (MEASURED, scipy): Haiku T vs P one-sided p = 1.0 (a tie, as the prereg expected). Haiku T vs R p = 0.00033
(exploratory). Qwen T vs P two-sided p = 1.26 × 10⁻⁴, **in the direction against the token**.

Mechanism of the Qwen failure (MEASURED from the transcripts). In all 24 resolve calls on a token (T and F), Qwen sent
only the bare cid (`token_form: bare_cid`). The server answered a degraded 200 with `cell_matches: false`,
`isError: false`, and the value. The model saw `"cell_matches": false` in its tool result and decided anyway.
The harness's own re-hash and receipt check passed 19/19 and 5/5, so the evidence was intact and the receiver was not.
Code (SPEC, lib.rs:37800-37818): `cell_matches: false` "means NOT CHECKED … The only way to reach a 200 with false is a
degraded resolve". And: "This used to be hardcoded `true` on every 200 … so on exactly the inputs where no cell was
checked, the field said it had been … Found by a third-party benchmark, 2026-08-11." So emem fixed a verifier that
claimed a check it had not run, and a receiver that ignores the corrected flag still fails. Both are failure classes
of any multi-agent system (F14 in `05`; M19 in `02`).

Cost (MEASURED, `results.json`). A: $0.105 per run, 13.3 s, 3.3 tool calls. Haiku B per decision: token arm $0.0158,
8.85 s, 45,568 input tokens; prose arm $0.0085, 7.1 s, 21,665 tokens. The token itself is 46 cl100k tokens against
64.9 for A's prose. Most of the difference is the MCP tool list (18,659 tokens, `token_counts.json`). So verification
roughly doubled the receiver's input cost in this setup.

Corrections to carry: review F3 (Haiku "checked" nothing; the harness did). "42 of 45 trials" counts the pre-registered
arms only (19 + 18 + 5). With R it is 52 of 55. The Qwen2.5-7B addendum-2 arm never ran. Claude arms are one model family.

**Verdict: KEEP, compact, on the face**, as the agent-level row between R1 (verifier) and the new R5 (`02`), with the Qwen
arm in the same sentence. Suggested wording (every number MEASURED):
**"Same token, two receivers. Claude Haiku refused the forged cell 5 of 5. Qwen2.5-3B dropped the cell from every token,
resolved the bare id and acted 5 of 5. A reference protects only a receiver that keeps it whole and obeys a refusal."**
The constructed threshold is a mechanism test, not a rate. Say so.

### 3.7 The pre-registered raw-band run and its adverse result

MEASURED (`data/v9/rawband/results.md`, `results.json`, `trials.jsonl`; prereg blake3 `30d8a1a1…` recomputed;
claude-sonnet-5-5, n = 10, `/mcp/full`, write tools denied, $2.12 total).
- `emem_band_raster observed_on=2026-09-23` (also 09-22 and 09-21) returned the **byte-identical 25 Sep** raster with no
  warning. The 23 Sep S2C scene exists (20 % cloud).
- Cause (SPEC, algorithms.md §13): the newest scene under the cloud tier in `[t − 30 d, min(t + 30 d, now)]` wins. The
  record does not store `observed_on`. The docs say "nearest" (defect 34).
- 9 of 10 runs never got 23 Sep values. 1 run reached post-fix facts through recall and backfill (ΔNDVI −0.015).
- 0 of 10 said "greener", the answer the pre-fix record would give.
- **All 10** noticed that both dates returned one scene. The board's "9" is a regex miss (review F8); my looser check
  also finds 10.
- **3 of 10 then wrote that no 23 Sep acquisition existed**, which is false.
- 30 of 30 cited cids re-hash.

Disclosed side effect (MEASURED): trial 8's recall and backfill made emem sign four new facts. Two of them (`wbbu4ezm…`,
`4utkk3hy…`, signed 13:53:27Z) are today's "current" B04/B08 at the Keylong cell. Read tools write records (defect 29),
so trials 9 and 10 were not independent.

INFERRED reading for the user's point: an agent that receives a silently substituted input does not just carry it. It
**invents a world fact to explain it** ("probably wasn't imaged that day"). Downstream, that is a false negative about
the satellite record, stated in fluent prose. The signed record named the scene it actually used (tslot 20721), so a
receiver that compares the record's date with its own request catches it. Prose does not.

Fix status: no CHANGELOG entry at `18adb67` or in remote `main` `[Unreleased]` (2026-10-01). Do not call it "resolved".

**Verdict: MERGE into the failure triad (§4) as "the wrong date".** Drop the 10-row run table from the face.

### 3.8 The Keylong cell: 207 facts, 13 products

MEASURED (`cell_keylong.json`, served 2026-09-30T22:43:38Z): 207 facts. By band: NDVI 156, B04 34, S1 VV 5, NDWI 2,
B08 2, and one each of DEM, TESSERA, NBR, DMSP, Prithvi, SCL, JRC, met.no. `cell_products.json`: 13 of 13 current facts
re-hash. LIVE now: 208 facts, 14 products (`cams.pm25` was added minutes after the read; review F6/F11).

Valid times of the 13 "current" facts at one address (MEASURED from `sources[].captured_at`):

| product | valid time |
|---|---|
| DMSP-OLS | 2014-04-01 |
| Copernicus DEM | 2021-04-30 |
| JRC GSW | 2022-01-01 |
| TESSERA | 2024-01-01 |
| Prithvi | 2026-07-17 |
| met.no temperature | 2026-08-10T05:00Z, a 7-week-old forecast printed without a date |
| S2 B04/B08/SCL/NDWI/NBR | 25 Sep (S2A) |
| S1 | 29 Sep |
| NDVI | 30 Sep (S2C) |

INFERRED: "current" NDVI (30 Sep S2C) and "current" B04/B08 (25 Sep S2A) at the same address come from different scenes.
A receiver that combines the current facts mixes dates, and only the per-fact tslot shows it. This is issue #20
("common addressing layer", not one snapshot), measured.

v12.1 already has the stronger version: a Berlin cell, 15 products, 16 facts including 4 signed absences, read from each
product's native grid.

**Verdict: DROP the Keylong product table.** **MERGE two facts** into v12.1 panel 1 or the temporal panel: (i) one address,
valid times from 2014 to 30 Sep 2026, each record dated; (ii) the address grows (207 → 208 in minutes) while every
record stays the same bytes.

### 3.9 The drift taxonomy

MEASURED/SPEC, seven real cases, each with one detecting equality. It maps onto the MASTER §9 mutation classes and the
R1 ids. Corrections: F2/M7 (neighbour pixel: E, S or SE, not always south), F3/M13 (the place row needs
`cell(b) ≠ cell(query)`), F13 (the "words" row is a model behaviour, from §18 not §21).

| drift (real case) | MASTER §9 class | R1 id | detecting test |
|---|---|---|---|
| 0.4871… retold as "≈ 0.49" | value | M2 | stated ≠ signed (only if B dereferences) |
| 162/200 neighbour-pixel reads | source/derivation | M15 | DN(b) ≠ COG[⌊row⌋, ⌊col⌋] |
| Bengaluru 918.0 → 915.07 m, as of 15 Jun → 918.0 | stale/current | M5 | fn_key₁ ≠ fn_key₂; as-of bound |
| raster 23 Sep → 25 Sep scene | time | new (request–record) | date(scene in b) ≠ asked date |
| relabelled cell; ask 597 m | spatial cell | M4; new (query–answer) | cell(b) ≠ cell(token); cell(b) ≠ cell(query) |
| 915.07 m signed 7 times, 7 cids | signer/identity | (none) | k(f₁) = k(f₂), cid(f₁) ≠ cid(f₂) |
| "Maasvlakte ramp 7" → 12 × 10 km | entity | M17 | none |

**Verdict: MERGE as the "seen in production" legend of the mutation matrix.** The two "new" rows (request–record,
query–answer) belong in R5 (`02` has M-ids for them).

### 3.10 Cost numbers (MASTER §18)

MEASURED:

| quantity | value | source |
|---|---|---|
| bytes read to sign one NDVI | 1,165,033 B (3 × 64 KiB heads + 3 tiles) of a 2,023,818,762 B scene = 0.058 %; the read path is reconstructed (INFERRED that emem reads exactly these) | `cog_pixel_bytes.json`, `scene_sizes.json` |
| stored | 1,115 B record | |
| handed to the next agent | 84 chars, 46 cl100k tokens (bare value 18 chars, 8 tokens; 3-decimal value 3) | `token_counts.json` |
| bundle | 38 chars, 22 tokens for 5 facts; a single fact token costs 9.5× the LLM tokens of a bare value (emem's own scorecard) | `token_counts.json` |
| what B pays for verification | about 2× input tokens and about +1.8 s in G2 | §3.6 |
| verification latency | 56–1,177 ms network per path (§3.5); 1.187 ms offline full check (R1, main line) | |

**Verdict: KEEP all of these in the cost panel.** It is the one panel MASTER §18 asks for that neither board has.

### 3.11 Source-file identity: pointer notes and range_hash (MASTER §5, issues #7, #12, #28)

MEASURED: the v8 line hashed the Earth Search (AWS) copies of B08 and B04 into two pointer notes: 292 chunks each,
238.7 MB and 232.9 MB, one Merkle root per file. The tile holding the cell is `emem:tree:khiqtqrddb6jponqn4gv72if7e#row=108`.
These are not the Planetary Computer files the NDVI was read from (B08 281,898,500 B; offset not pre-subtracted). Trace
link 9c: emem's signed `range_hash` of the PC tile equals our BLAKE3, but it is a separate statement and the fact does
not reference it.

INFERRED: this is the exact picture issue #28 asks for. **Source artifact** (a COG, with its own optional
`emem:tree` identity) → **read and derive** → **canonical record** (names the URL and scene) → **BLAKE3** → **signed
fact**, with the edge from record to file drawn dashed: "named, not hashed".

**Verdict: MERGE into the evidence-object figure.** One honest line: "The record names the file. emem can also
content-address the file (we did it for an archive copy), but the record does not bind it today."

### 3.12 `research/repro/v10/algorithms.md`

SPEC: 15 formulas, each with file:line at `18adb67`, a "reproduced by our script: yes / partly / no" line, and the
doc-vs-code differences behind defects 32–36. Spot checks today found the citations accurate: bundle (memory_bundle.rs:155-182),
state (lib.rs:20818), entity (entity.rs:11-19), `cell_matches` (lib.rs:37800-37818).

**Verdict: KEEP behind "READ THE METHODS".** On the face, print only the 3 or 4 formulas a result needs: `fact_cid`, the
acceptance predicate (corrected, §3.4), the pixel floor rule. Where docs and code differ, follow the code. Note that
v12.1 cites `docs/model.md@04b40c5`; one commit must be chosen (`01` §7.2).

### 3.13 Defects 1–37

#37 says to take "defects" off the face; the 05 report turns them into failure classes. Defects this branch found that
are **still LIVE** on 2026-10-01: 24 (ememdemo `llms.txt` cid rule) and 31 (entity receipt v1). Defects with no fix in
any CHANGELOG I could read: 27/34 (date substitution) and 37 (ask place).

**Verdict: DROP from the face; feed §4 and `05`.**

### 3.14 Panels to drop

- **"Where emem lost" / the authors' scorecard / 19 withdrawals** (#37). Keep two facts as baseline and cost inputs:
  BM25 ties the bundle on short handoffs (16/16), and a single token costs 9.5× the tokens of a bare value. The RAG
  baseline in R5 must be fair (`02` §1).
- **"Since the paper was accepted"** (history language). Keep one line for the programme title's "over Foundation-Model
  Embeddings": the TESSERA vector re-reads bit-exact from its public product (**n = 1**; the board's "4 of 4" is
  unsupported, review F4), and it is `attester_only`, because nobody can recompute the encoder step. Prithvi and Clay
  bind their weights (review M9).
- **"Ememify your work".** Two of five steps have no record of being run (review F5/F6). Keep the one-line MCP install
  in the ecosystem band if `03` verifies it.
- **Footer traffic** (96,728 MCP calls, 96.2 % operator keys): unsourced (review F7; #45).

---

## 4. The branch's contribution to "why emem": three intact records, three wrong referents

The user's point is that each error emem had, and found, is one any multi-agent EO pipeline will also have, with real
consequences. This branch holds three measured production cases of one pattern, plus the receiver and adapter failures
that decide whether the pattern is caught:

| case | what happened (MEASURED) | integrity checks | what the record exposes | an ordinary pipeline |
|---|---|---|---|---|
| **the wrong pixel** (M15; on v12.1) | the reader rounded instead of flooring: 162 of 200 pre-fix records carry a neighbour's DNs; at Keylong 23 Sep, NDVI 0.3444 signed where the containing pixel reads 0.4860 | all pass | re-reading the COG at the signed DNs' position | passes silently (INFERRED) |
| **the wrong date** (raster tool) | asked 23 Sep, served the byte-identical 25 Sep scene; 10/10 agents saw one scene twice; 3/10 then wrote that no 23 Sep acquisition existed | all pass | the scene and tslot inside the record ≠ the date asked | the substitution becomes a false claim about the world (INFERRED) |
| **the wrong place** (`/v1/ask`) | "Keylong (32.57126 N, 77.03448 E)" answered from the town point, 597 m away, NDVI 0.28 | the 4 stage addresses recompute 4/4 | the `located` stage payload; answered cell ≠ asked cell | another field's value under this field's name (INFERRED) |
| **the receiver** (G2) | Qwen2.5-3B stripped the cell from 24/24 tokens and acted on a forged cell 5/5; Haiku declined 5/5 | the evidence was intact (harness 24/24) | `cell_matches: false` was in the tool result | nothing to check (INFERRED) |
| **the adapter** (cross-runtime) | LlamaIndex drops the receipt; langchain-mcp-adapters returns a refusal as text; A2A default verbosity elides the receipt bytes | the protocol carried them | — | — |
| **the verifier** (emem 2026-08-11) | `cell_matches` was hardcoded `true` on every 200, including the inputs where no cell was checked; found by a third party, fixed (SPEC lib.rs:37810-37814) | — | — | a check that reports a pass it did not run (F14) |

INFERRED one-line conclusion the board can carry (every term backed above): **"Three times emem signed exactly what it
did, and what it did was wrong. Each time the record said where."** The boundary sentence follows: "A signature fixes the
bytes. Only a receiver that re-checks the referent, and refuses a mismatch, is protected."

This is the bridge to MASTER §10 (M15 prominent) and §6 (handoff, corruption, receiver). It makes M15 the first of a
measured class, not a one-off.

---

## 5. Keep / merge / drop, against v12.1 and the brief

| asset | on v12.1? | brief / issue | verdict | where on the A0 |
|---|---|---|---|---|
| A1 signed track + ememdemo QR | no (QRs: emem.dev/verify, GitHub tree) | §25, #34, #35, #37 | **KEEP**; rebuild for v13; drop § apparatus | QR box, 30-cm tier, "INSPECT THE RECORD" |
| A1b valid / forged token in ememdemo | no | #35 | **ADD** (no publishing) | two QRs, "TRY A TOKEN" / "SEE A REFUSAL" |
| A2 token family | no | §5, §26, #18, #28 | **DROP** the table; **MERGE** the 3-tier legend | evidence-object figure |
| A3 `emem:state` | no | §20 (extension), #18 | **MERGE** as one line in the triad; not a contribution | 30-cm caption |
| A4 15-link trace, residual trust | partly (guarantees table, no residual) | §11, §12, #17, #29 | **MERGE** as the ladder backbone | ladder, 1-m tier |
| A4b offline 4.9 kB bundle | no | §25 "RE-RUN" | **KEEP** | QR + one line |
| A5 11 client paths | no | §16, §17, #43 | **MERGE** | ecosystem band |
| A5b refusal matrix, untrusted mirror | no (uncommitted) | §12, #43 | **MERGE** after committing | ecosystem band 30-cm; threat model |
| A6 G2 incl. Qwen | no | §9, #16 | **KEEP**, compact, Qwen mandatory | main result, agent-level row (R5 pilot) |
| A7 raw-band run | no | §9 time; failure classes | **MERGE** into the triad | triad |
| A8 Keylong 13 products | v12.1 has Berlin 15/16 | #20 | **DROP** the table; **MERGE** the valid-time spread and "address grows" | panel 1 / temporal caption |
| A9 drift taxonomy | partly (R1 amber ids) | §9 | **MERGE** as legend | mutation matrix |
| A10 cost numbers | no | §18 | **KEEP** | cost panel |
| A11 COG pointer notes, range_hash | no | §5, #7, #12, #28 | **MERGE** | evidence-object figure (dashed source edge) |
| A12 algorithms.md | no (cites model.md@04b40c5) | 30-cm / QR | **KEEP** behind QR | "READ THE METHODS" |
| A13 defects list | no | #37 | **DROP** from face | feeds §4 / `05` |
| A14 scorecard, since-acceptance, ememify, traffic | no | #37, #45 | **DROP** (keep the 9.5× and BM25 facts; one TESSERA line) | — |

---

## 6. Must be committed before printing (scratchpad is ephemeral)

All under `/tmp/claude-0/-home-user-esa-poster/0db6b3ad-8059-51a6-bd74-2d7a97faf986/scratchpad/v8/`:
- `followup-G2-two-llm-plugin-handoff/qwen_trials.jsonl` (52 rows, blake3 `cb6e6369c13a…318f`), `raw/run_qwen.log`,
  `raw/prereg.blake3` (the hash log, with times), `prereg_addendum.md`, `prereg_addendum2.md`, `run_qwen.py`,
  `qwen_b.py`, `mcp_resolve.py`, `run_a.py`, `run_claude_b.py`, `analyze.py`, `agent_a.jsonl`, `claude_b_trials.jsonl`.
- `crossruntime/refusal_matrix.json`, `refusal_ts.json`, `untrusted_mirror.json`, `p1…p8_*.py`, `run_all.py`,
  `crossruntime_raw.jsonl`.
- This session: `ememdemo/cdp.mjs`, `track11.txt`, `tok_valid.txt`, `tok_forged.txt` (the LIVE ememdemo outputs above).

Also recompute `results.json` for the Qwen arm from `qwen_trials.jsonl`. The committed file has
`"qwen2.5-3b-instruct-q4_k_m": {"arms": {}}`: it was written at 10:57:56Z, and the Qwen trials ran until 11:16:16Z.

Pre-registration practice (MEASURED): both pre-registrations were hashed locally before trial 1, but first appeared in
a signed note only after their trials: the G2 prereg in the evidence note at 13:10:24Z (trials ended 11:16Z), and the
raw-band prereg in `evidence2` at 14:03:36Z (trials after 13:49Z). So "pre-registered" is self-timestamped.
INFERRED recommendation for R5 (`02`): publish the pre-registration as a signed pointer note *before* trial 1, so emem's
log orders it before the results. Say what that proves: an ordering within an operator-run log, not third-party
timestamping. It also makes the experiment itself an instance of the protocol.

---

## 7. Corrections that must travel with any reused v11 text

From `00_v11_review_findings.md`, confirmed where I could:
- M1/F1: the draft-check rule's roles are swapped.
- M2: bundle preimage.
- M3: receipt preimage framing.
- M4: batch leaves are sorted raw digests.
- M6: derive re-runs only pure ops with a pinned `code_cid`.
- M7/F2: neighbour pixel is E, S or SE.
- M8: the acceptance predicate needs the attester signature.
- M9: `attester_only` is TESSERA only.
- M10/M11/M12: cube is a list hash.
- M13/F3: the place test.
- M14: tree token id.
- M15: state field list.
- F3 (handoff): "B checked".
- F4: TESSERA n = 1.
- F5/F6: local node, citation skill.
- F6/F11: 207 at 22:43Z, one fact per (band, tslot).
- F7: traffic unsourced.
- F8/F9: 10 of 10 noticed.
- Compaction F4/F12: the 0/72 vs 3/36 test had no irrigation rule; 0/72 is the pressure arm only.

---

## 8. Open questions

1. Will the authors re-seal the v13 board with the poster key? It is a signing step that only they can take, and every
   text change after it forces a re-seal.
2. Should the track's QR land on ememdemo, which shows "not named, not affiliated" for the poster key? Or should the poster
   key first be bound to a Vortx-controlled identity (DNS, did:web), so that the page names the authors?
3. Will ememdemo's `llms.txt` cid rule (defect 24) be fixed before 19 Oct? Visitors' agents that read it will reject the
   poster's own track.
4. Should R5 include "receiver strips the cell" and "adapter returns refusal as text" as explicit conditions, so that the
   Qwen and LangChain findings become measured rates rather than anecdotes?
5. Are defects 27 (date substitution) and 37 (place) fixed on the live server (`8e9b401c`)? Re-testing needs
   `/v1/band_raster` and `/v1/ask`, which sign records. That is a decision for the experiment task, not for this report.
6. Can a ChatGPT or Dify host leg be added to the G2-style handoff in time for #43, or is "two model runtimes, eleven
   client paths" the final claim?
