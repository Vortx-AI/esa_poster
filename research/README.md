# Poster research

This folder is the shared decision memory for the ESA / BIFOLD Agentic AI for Earth Observation poster.

## Shared state

- [RESEARCH_STATE.md](RESEARCH_STATE.md) — current synthesis and the working invention statement.

## What we should do

- [should_do/01_POSTER_STRATEGY.md](should_do/01_POSTER_STRATEGY.md) — mechanism-first poster strategy.
- [should_do/02_EVENT_LANDSCAPE.md](should_do/02_EVENT_LANDSCAPE.md) — title-level scan of all 43 published posters and the visible whitespace.
- [should_do/03_INDUSTRY_SYSTEMS_COMPARISON.md](should_do/03_INDUSTRY_SYSTEMS_COMPARISON.md) — STAC, COG, Earth Engine, W3C PROV, IPFS, Nix and agent-memory comparison.
- [should_do/04_VERIFIED_CLAIMS_LEDGER.md](should_do/04_VERIFIED_CLAIMS_LEDGER.md) — every mechanism claim checked against emem source, with the exact wording allowed on the poster.
- [should_do/05_EVIDENCE_AND_NUMBERS.md](should_do/05_EVIDENCE_AND_NUMBERS.md) — measured results (agreement ≠ correctness, handoff, verify cost) with n and caveats.
- [should_do/06_HOW_DEVICES_AND_AGENTS_CONNECT.md](should_do/06_HOW_DEVICES_AND_AGENTS_CONNECT.md) — how parties that share nothing agree on evidence; shipped vs simulated vs roadmap; the agent skills.
- [should_do/07_EVENT_FORMAT_PEOPLE_AND_ACTIONS.md](should_do/07_EVENT_FORMAT_PEOPLE_AND_ACTIONS.md) — poster format facts, title/author fixes, who is in the room, pre-event checklist.
- [should_do/09_INVENTION_REGISTER.md](should_do/09_INVENTION_REGISTER.md) — **the eight contributions (A1–A8) and three findings (B1–B3)**, each with code evidence, a live check, closest prior art, what is new, and limits. Start here.
- [should_do/08_RELATED_WORK_2025_2026.md](should_do/08_RELATED_WORK_2025_2026.md) — AlphaEarth, TESSERA, C2PA, A2A, ERC-8004, EO MCP servers, agent memory.

## What we should not put in the presentation

- [do_not_use/01_CROWDED_AND_UNSAFE_CLAIMS.md](do_not_use/01_CROWDED_AND_UNSAFE_CLAIMS.md) — crowded claims, novelty traps and overclaims.
- [do_not_use/02_AI_TELLS.md](do_not_use/02_AI_TELLS.md) — visual and language patterns that make the poster look generated or commercial.
- [do_not_use/03_CORRECTIONS_TO_CURRENT_CONCEPT.md](do_not_use/03_CORRECTIONS_TO_CURRENT_CONCEPT.md) — 16 statements in the earlier concept that the code contradicts.
- [do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md](do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md) — 36 defects/inconsistencies for the maintainers (incl. geo.qa is Vortx-operated, not independent).
- [do_not_use/04_REFUTED_UNMEASURED_AND_ROADMAP.md](do_not_use/04_REFUTED_UNMEASURED_AND_ROADMAP.md) — refuted, unmeasured, roadmap-only and stale claims.

## Reproduce

- [repro/](repro/README.md) — `verify_fact.py` re-derives production fact CIDs with stock `blake3`; the 918.0 → 915.07 drift exhibit.

## Research discipline

1. Separate **published facts** from **inference based on titles**.
2. Do not call a primitive novel merely because emem uses it; identify the novel composition/object boundary.
3. Prefer primary sources and official specifications.
4. When another poster's abstract/paper becomes available, update the title-level landscape before making any comparative statement.
5. Treat the emem repo and accepted paper as the source of truth for what ships vs what remains open work.
6. Every final poster claim should be reproducible from a token, endpoint, source file, paper section or live demonstration.

## Current working thesis

> **Agents hand each other the address of a signed physical observation instead of a sentence about it — and any receiver can re-hash and verify it offline.**

The content address is the mechanism. The measured consequence: paraphrase handoffs can raise agreement while lowering correctness (0/72, p = 0.035); addressed handoffs stay exact and citable. See [RESEARCH_STATE.md](RESEARCH_STATE.md).

## v11 (30 Sep 2026)

- [`should_do/15_V11_CLAIMS_MAP.md`](should_do/15_V11_CLAIMS_MAP.md): every number on the v11 board, its source and its evidence class.
- [`should_do/16_V11_CRITIQUE_AND_DECISIONS.md`](should_do/16_V11_CRITIQUE_AND_DECISIONS.md): what was wrong with v10, what v11 does, the refutation policy, and what is open before printing.
- [`audit_v11/`](audit_v11/): two independent audits. `emem_capability_index.*` maps all of emem at HEAD e226f8b with code pointers and live counts; `poster_evidence_audit.*` checks the 96 claims printed on v10.
