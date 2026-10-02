# emem at Agentic AI for Earth Observation

**An Earth observation that survives an agent handoff.**

EMEM gives an observation a lookup identity and a content-addressed record. An agent passes the reference; the next agent resolves the same record and checks it before continuing. Earth data stays upstream while its reference enters the reasoning.

Jaya Kumari and Avijeet Singh, Vortx AI. Agentic AI for Earth Observation, BIFOLD and ESA Φ-lab, Berlin, 19 October 2026.

## Current poster: v13.4

This round restores the drift decomposition, tested drift-anchor score, memory model and two-clock recall, source NDVI formula, and archived foundation-model vectors. The memory example now separates provider change from physical change. [Source and test audit](research/v13/16_FORMALISM_AND_TEST_AUDIT.md).

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
