# v11: how the board was made, and how to evolve it

Written 30 Sep 2026 for the next agent or person who edits this board. Read this first, then
`15_V11_CLAIMS_MAP.md` (every number and its source), `16_V11_CRITIQUE_AND_DECISIONS.md` (why the board changed) and
`17_V11_RESPONSE_TO_FIELD_MAP.md` (what was taken from the field-map critique).

## 1. Files, and which one to edit

| edit | file | notes |
|---|---|---|
| text and layout | `poster/src/poster.v11.html` | the only hand-edited board file; `poster/poster.html` is a build product |
| figure 1 (hero) | `poster/make_hero_v11.py` | writes `fig/v11/hero.svg` in mm at print size; every string is copied from a signed record |
| R1, R2, R4 figures | `poster/make_figures_v11.py` | matplotlib, IBM Plex from `fonts/ttf`, text as paths; each figure asserts no overlapping or clipped labels before it saves |
| R1 data | `research/repro/v11/mutation_suite.py` | deterministic; rerun by the build |
| QR codes | `poster/fig/v11/qr_*.svg` with payload in `qr_*.txt` | regenerate with `qrcode` (snippet in §4) |
| the build | `poster/build_v11.py` | figures, then SVG inlining, gates, PDF, PNG |

Build: `pip install weasyprint pypdfium2 matplotlib qrcode fonttools blake3 cbor2 pynacl`, then
`python poster/build_v11.py` (add `--no-figures` to reuse figures). Output: `poster/emem-poster-A0.pdf` and
`poster/emem-poster-preview.png`.

## 2. Gates, and the rule behind them

The build fails, never warns, when: the PDF is not one 841 × 1189 mm page; `<main>` ends less than 2 mm above the
footer (measured from WeasyPrint's box tree, and "boxes not found" is itself a failure); running text contains an em
dash, an en dash outside a numeric range, or a tell word; a QR file is missing. The figure scripts fail on any
overlapping or clipped label. Rule: **an unknown gate result is a failure.** A gate that prints "could not determine"
and exits 0 enforces nothing.

## 3. Process that produced v11

1. Pulled `main` (v10 merge `50bb8bf`) and emem HEAD `e226f8b`.
2. Two independent audits ran in parallel, each in a fresh context, told not to push or write to emem.dev:
   - an inventory of all of emem at HEAD with code pointers and 10 read-only GETs (`research/audit_v11/emem_capability_index.*`);
   - an audit of all 96 claims printed on v10 against this repository (`research/audit_v11/poster_evidence_audit.*`).
3. The critique (`16_…`) was written from both. Everything unsourced was cut; every mismatch was fixed on the board.
4. The board was rebuilt around one hero figure, six contributions, results and answered objections.
5. After the field-map critique arrived on `main`, v11 was rebased onto it, the mutation suite was built and run, R1
   became the lead result, and the scope box became the seven-row identity table (`17_…`).
6. Each layout change was checked by rendering the PNG and reading region crops, not by trusting the HTML.

## 4. Things that cost time, so the next agent does not repeat them

- **Renderer.** Headless Chrome and Playwright did not launch in the sandbox this was built in; WeasyPrint did.
  WeasyPrint quirks: CSS grid overestimates row heights; a grid nested in flex can crash it; flex items with a zero
  basis that hold images inflate. Use flex with explicit mm widths per column. `render.mjs` (Chromium) still works on
  a normal machine and is kept for print shops that want a Chromium PDF.
- **Fonts in figures.** matplotlib needs TTF, not woff2: `fonts/ttf/` holds converted IBM Plex (fontTools).
- **Checking what is really in a PDF.** Filenames and sizes can look right while the embedded image is stale. Hash
  the decoded pixels of each embedded image (pypdfium2 `page.get_objects()`, type 3, `get_bitmap().to_pil()`) and
  compare with the current PNGs.
- **Numbers.** Copy numbers from the measurement file, never from someone's prose, and put units in count field
  names (`canonical_recordings`, not `stems`). Two past corrections came from exactly this.
- **emem's own tools.** MCP results are capped at about 24 KB and slimmed; read `pagination.total` for counts. Read
  tools can sign new records, so prefer static endpoints for counts (`/v1/agent_card`, `/openapi.json`,
  `/v1/log/sth`, `/v1/algorithms?limit=1`).
- **QR regeneration:**
  ```python
  import qrcode, qrcode.image.svg
  q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0,
                    image_factory=qrcode.image.svg.SvgPathImage)
  q.add_data(url); q.make(fit=True); q.make_image().save("poster/fig/v11/qr_NAME.svg")
  ```

## 5. The next experiment: models in the loop (P1)

R1 answers "does the check stop it?" The open question is "does an agent run the check and obey it?" Specification:

- **Conditions:** A prose; B JSON; C a retrieval tool over a notes corpus; D emem tools (resolve, verify) with the
  same 17 mutations injected at the resolver or in the handoff text.
- **Models:** 4 to 6 from different vendors, two runtimes (MCP client and a plain function-calling loop).
- **Task:** R3's irrigation rule, threshold 0.0004 below the value; A writes the handoff, B decides.
- **Metrics per cell:** false acceptance, false refusal, verification completion (did B call verify), obedience
  (did B act after a refusal), decision accuracy, latency, tokens. Report n and Wilson intervals.
- **Pre-register** the design and hash it before trial 1, as in `research/repro/data/v8/prereg.md`.
- Needs API keys for each vendor; none were available when v11 was built.

## 6. Open before printing

From `16_…` §4, still open:
1. Commit the Qwen2.5-3B arm logs (§22) and the derive response (§11), or keep their numbers off the board.
2. Reseal v11 (the seal QR still opens the v10 track `7n7qogvn…`, which is valid for every § cited).
3. 118 vs 116 wired measurements (agent card vs /v1/materializers).
4. Merge this branch into `main` so the R1 QR (`…/tree/main/research/repro/v11`) resolves; then re-scan all three QRs
   on a print proof.
5. Mint Zenodo v0.2 so the DOI and "whitepaper v3" agree.

Upstream (emem), from the field map P2 and the inventory: bind a provider-issued upstream identity (signed STAC item
or checksum) into derived facts; version the verification policy; fix the agent card still listing geotessera as a
live band; fix the CHANGELOG 2.4.2 counts.

## 7. Conventions

- Prose: short sentences; no em or en dashes except numeric ranges; no tell words (the gate lists them).
- emem is AI infrastructure; satellites are the input, not the identity.
- Every printed number maps to a row in `15_V11_CLAIMS_MAP.md` with its evidence class. No row, no number.
- Refutations stay: as answered objections and the identity table on the board, and in full in `research/`.
