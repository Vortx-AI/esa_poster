# emem at Agentic AI for Earth Observation

**An Earth observation that survives an agent handoff.**

EMEM gives an observation a lookup identity and a content-addressed record. An agent passes the reference; the next agent resolves the same record and checks it before continuing. Earth data stays upstream while its reference enters the reasoning.

Jaya Kumari and Avijeet Singh, Vortx AI. Agentic AI for Earth Observation, BIFOLD and ESA Φ-lab, Berlin, 19 October 2026.

## Current poster: v13.8

A dated, 141-record NDVI history now links the EO observation to the handoff experiment. Memory operations have practical EO task names, and the community guide offers vegetation history, forest-product comparison and historical replay. The full handoff, 14-row token table, Berlin fanout, drift and memory formulas remain. [Recovery and scientific scope](research/v13/23_EO_GOLD_AND_USABILITY.md).

- [Print-ready A0 PDF](poster/emem-poster-A0.pdf)
- [Preview](poster/emem-poster-preview.png) and [300 dpi proof](poster/emem-poster-A0-300dpi.png)
- [Try it, inspect, reproduce](https://vortx-ai.github.io/esa_poster/)
- [Publication and validation notes](poster/README.md)

The accepted programme title is **EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings**. The printed scientific title preserves it.

The poster follows one system: observe, locate, record, hand off, resolve, check and continue. The controlled handoff experiment, source-pixel example and temporal memory demonstrate the checks. A Berlin multi-product stack and the token family show the wider scope; the ecosystem panel distinguishes tested paths from protocol, registry and example surfaces.

## Read the mechanism

- The lookup identity is cell, product and observation time.
- The content address is BLAKE3 of the canonical observation record.
- `emem:fact:<cell64>:<fact_cid>` carries the cell and exact record address. Product and time are fields inside the record.
- A batch attestation covers record addresses. The source pointers in the illustrated record name the imagery; a source re-read tests the measurement.
- Source quality, entity meaning and downstream decisions remain separate responsibilities.

## Build and edit

Start with [AGENTS.md](AGENTS.md) and the [current editorial brief](research/v13/14_UNIFIED_POSTER_BRIEF.md). Edit `poster/src/poster.v13.html` and its CSS, then regenerate the affected figures. `poster/poster.html` is generated.

```bash
python -m pip install -r poster/requirements.txt
python -m playwright install chromium
python poster/build_v13.py
npm ci --prefix tools/site
python poster/build_site.py
```

The poster build checks page size, layout, typography, glyphs, claim coverage, evidence rows, colours, images, QR decoding and copy length. [The report](poster/build_v13_report.json) records the results. Measurements are in `research/repro/`; claims are mapped in `research/v13/12_claims_map*.json`.

The detailed verification ladder, token grammars and SAT-042 reference harness remain linked from the methods. Earlier posters and signed tracks identify their own archived files; they do not attest this revised PDF.

The companion pages deploy from committed `/docs` through [the Pages workflow](.github/workflows/pages.yml) on pushes to `main`. Poster artifacts are committed under `poster/`.
