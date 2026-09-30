# Event facts: format, people, and the actions to take before 19 Oct

Snapshot: 2026-09-29. Sources: every page on agentic-eo.berlin, the schedule PDF, the site's
public source repo (`github.com/rsim-tu-berlin/agentic-eo.berlin`, commit `78b044b`, 27 Sep),
and the Zenodo API.

## Poster format

**Verified: the organisers publish no poster size, orientation, template or deadline.**

- The site repo was grepped for A0, portrait, landscape and board: no matches.
- `/faq`, `/information` and `/programme/poster-guidelines/` all return 404.
- The only official text: *"Presenters stand by their boards for the full session."*
  (`/programme/posters/`).
- No board numbers have been assigned yet (`_data/schedule.yml` has an optional
  `board: "P01"` field, unused).
- The lightning-talks page exists but says "To be defined", and no pitch slot is scheduled.
- **Our slot:** Poster Session 1, Mon 19 Oct, 17:00–18:30, Langenbeck-Virchow-Haus, room
  B. von Langenbeck (1st floor). We are 4th of 23 in the list.
- **The nearest precedent is unverified.** ESA's Living Planet Symposium 2025 reportedly used
  boards of at most 120 × 150 cm, bring-your-own prints and push pins. We could not fetch the
  page, so treat this as unconfirmed.

**Decision until the organisers answer: design for A0 portrait (841 × 1189 mm).** It fits every
common ESA board.

- Keep 20 mm safe margins.
- Do not laminate or use rigid board (push pins).
- Bring an A4 handout carrying the QR code and the repro commands.

**Action:** email `paper@agentic-eo.berlin` (or `contact@`) to ask for the board size,
orientation, fixing method, and whether a digital copy or lightning slot is expected.

## Title and author consistency: fix before printing

| where | title | authors |
|---|---|---|
| Programme | "**EMEM:** A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents over Foundation-Model Embeddings" | Jaya Kumari (Vortx AI) |
| Zenodo 10.5281/zenodo.20706893, v0.1.0, 2026-06-15 | "**emem: A research on** Content-Addressed, Verifiable Earth-Memory Protocol…" | Jaya Kumari; "Avijeet Singh Singh" (the surname is entered twice) |

- **Recommendation:** print the accepted programme title exactly. List both authors on the
  poster.
- Fix the doubled surname on Zenodo. A new version can correct the metadata.
- If possible, ask the organisers to add the co-author to the listing.

**The DOI caveat.** The DOI version (whitepaper v1) contains claims the repo has since
withdrawn; `docs/whitepaper.md:1733-1790` lists them one by one, and v3 records 19
withdrawals. The poster should cite the DOI *and* name the current version, for example
"claims as of whitepaper v3 / repo `64cfae5`". Better still, mint a Zenodo v0.2 before
19 Oct.

## Who is in the room: build the poster to start these conversations

| person / slot | when | the hook |
|---|---|---|
| **Christopher F. Brown**, Google DeepMind: *"Why Mature Agents Require a Paradigm Shift in Tooling"* | Day 3, 09:45 | first author of AlphaEarth Foundations. Our story is **what happens after the embedding**: identity, receipts, cross-agent continuity. (The AlphaEarth slot in emem is reserved but unused. Do not claim integration.) |
| **Davide Crapis**, Ethereum Foundation: *"Building Robust Economic Capabilities in AI Agents"* | Day 3, 09:00 | co-author of **ERC-8004 "Trustless Agents"**, which provides agent identity, reputation and validation registries. emem receipts are a natural *payload* such validators could check. emem needs no chain. |
| **Manling Li**, Northwestern/Amazon: *"Failure Mode in Agentic Reasoning"* | Day 2, 14:00 | our pre-registered **agreement ≠ correctness** result (0/72, p = 0.035) and the paraphrase trap are failure-mode evidence |
| **James Zou**, Stanford: *"Collective Intelligence of AI Agents"* | Day 2, 17:15 | 216 agents and 8,427 signed notes in a public collaboration log; shared evidence without shared context |
| **Steve Chien**, JPL: *"FAME: Traditional and Agentic AI in Space"* | Day 2, 09:30 | signing overhead at the edge (0.167% of a frame). Say clearly that orbit is simulated. |
| Oral: *"Agentic Orchestration of EO Foundation Models via MCP"* | Day 1, 15:36 | the same MCP surface; we add signed, addressable results |
| Oral: *"EVE's Community-driven MCP Registry"* (Pi School / ESA Φ-lab) | Day 2, 15:33 | register emem in EVE's MCP registry |
| **Hackathon: EO MCP tools on EVE's registry** | Thu 22 Oct | asks for "provenance", a "full audit trail" and optional A2A. **Enter with emem, or offer it as a tool.** |
| Demo 13: *Reproducible openEO Workflows on CDSE* (VITO); Demo 9: *Verified Pipelines*; Demo 14: *Artifact-Grounded Geospatial Intelligence* | various | our closest "verifiable" peers. Visit them and compare object boundaries. |
| Nicolas Longépé (ESA Φ-lab, organiser); D'Ercole (Φ-lab, onboard VLMs poster; co-moderates "Subway Takes") | | the organisers' own interest: onboard and space–ground |

## Neighbouring posters most likely to be compared with ours

No abstracts are public; these are inferred from titles.

**Session 1 (the same room and time as us):**

- *GeoGuard*, agentic guardrails and validation (UAH);
- *THEDE*, thematic datacubes on demand (Sistema, an ESA project);
- *Trustworthy NASA Earth Science Discovery Agent using CARE* (Development Seed);
- *Hierarchical System with Agentic Refinement for EO Archives* (GMV);
- *LLM-based Onboard Orchestration for EO Constellations*;
- *SENSOR2RAG*;
- *Fitness for Purpose as an Agentic Task* (Aniterra).

**Session 2:**

- *Provenance-First Geospatial Composition* (Earthward/TUM), plus their Demo 1. This is the
  **most direct "provenance" competitor**; they use human-in-the-loop scaffolding.
- *Agentic AI as an Auditable Co-Scientist* (DRI);
- *Learned Satellite Embeddings as Covariates* (ISRIC);
- *Airbus Geo Explore semantic search*;
- *Multi-Satellite Task Orchestration with On-Board VLMs* (ESA Φ-lab).

**How we differ:** GeoGuard and CARE make *trust* a design or validation step. Earthward makes
provenance a *workflow*. emem makes each piece of evidence carry **its own content-derived
identity and signature**, so trust survives *after* it leaves the system that produced it.

## Checklist before 19 Oct

- [x] Poster drafted: `poster/emem-poster-A0.pdf` (A0 portrait)
- [ ] Merge to `main` before printing (the repro QR points to main)
- [ ] Email the organisers about board size, orientation, pins and a digital copy.
- [ ] Freeze the claims at one emem commit, and print that commit hash on the poster.
- [ ] Zenodo: fix the doubled author surname; mint v0.2 aligned with whitepaper v3.
- [ ] Mint or pick the final printed tokens, and re-verify them within 24 h of printing and
      on the morning of 19 Oct (`research/repro/verify_fact.py`).
- [ ] Pre-warm the raster and cube examples (both returned 504 today), and record fallbacks.
- [ ] Prepare an A4 handout with the QR code and the three repro commands.
- [ ] Prepare a laptop demo: the drift exhibit, `echo_verify` catching a wrong number, and a
      cross-model handoff that passes one bundle handle.
- [ ] Register emem with EVE's MCP registry before the hackathon.
- [ ] Walk the room with the 7 questions in `02_EVENT_LANDSCAPE.md` and log the answers.
