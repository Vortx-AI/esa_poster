# Session log: v10 to v11.2, 30 Sep 2026

What was built in one working session, how, why, and what is unfinished. Written for the developer agent that
takes the board further. Read in this order:

1. `AGENTS.md` (repository root): how to build and the rules the build enforces.
2. This file: the story of the session, the decisions and the dead ends.
3. `NEXT_STEPS.md` (this folder): work in progress, in priority order, with how to do each item.
4. `STATE.json` (this folder): the machine-readable state (branch, commits, numbers on the board, open items).
5. `research/should_do/15_` to `18_`: claims map, critique and decisions, response to the field map, handoff.

## 1. The brief

The authors' requests, in order (verbatim, typos kept):

1. "be critic, find out where we missed, messed, standarize, neaten, wow up the invention truly in the paper, emem is
   actually much more than what we have here, plus refutations on paper , is it wise, you are the best scientist,
   upgrade us, push your upgrades to github, you have the free hand to drastically improve and upgrade us to be in
   standard."
2. "pull the latest updated code as well"
3. "the coding agent delivered it like a project work plan, we need to enhance it to be an invention grade research
   poster, emem is truly amazing just the indexing is partial on this poster making it look lame."
4. "push everything including our findings, outputs, reasoning, processes etc such that the coding agent can evolve,
   also see another agent has added their view, how to truly enhance."
5. "is it needed to show the record recorded emem's own error, is it wise, do posters gave these sections, are we
   being harsh on emem, hiding what truly is underneath. see sections where we are doing refutations, just showing
   counts etc, scientists wont like that"
6. "push everything we worked on, spent tokens on, final results, reasonings, work in progress etc such that the
   developer agent is aware of what we built, how we built for them to take further."

Standing conventions carried from earlier sessions: emem is AI infrastructure (satellites are the input, not the
identity); prose has short sentences, no em or en dashes outside numeric ranges, no tell words.

## 2. Inputs read

- `esa_poster` at `main` 50bb8bf (v10 board, sealed track `7n7qogvn…`), later 24c5d6f (two field-map documents by
  another agent, `research/should_do/10_EVENT_FIELD_MAP_AND_CRITIQUE.md` and `11_BROAD_SOURCE_OF_TRUTH_FOR_CODING_AGENT.md`).
- `emem` at HEAD e226f8b (Rust, Apache-2.0), README in full, plus code pointers through the inventory below.
- agentic-eo.berlin: EMEM is in Poster Session 1, 19 Oct 2026, 17:00 to 18:30, B. von Langenbeck, 23 posters.
  Same session: GeoGuard (guardrails), Beyond Task Success (evaluation), THEDE, a trustworthy NASA discovery agent.
  Session 2 holds Provenance-First Geospatial Composition.

## 3. What was built, in order

| step | output | where |
|---|---|---|
| v10 critique | five reasons it read as an audit log: a fifth of emem indexed, no architecture figure, self-refutation in the best space, internal vocabulary, density (about 3,200 words) | `research/should_do/16_V11_CRITIQUE_AND_DECISIONS.md` §1 |
| two parallel audits (sub-agents, fresh contexts, told not to push or write to emem.dev) | capability index of all of emem with code pointers and live counts; audit of all 96 claims printed on v10 | `research/audit_v11/`; briefs verbatim in `subagent_briefs.py` |
| renderer | WeasyPrint build with fail-loud gates | `poster/build_v11.py` |
| hero figure | the whole protocol around one real Sentinel-2 record, badges C1 to C6 | `poster/make_hero_v11.py` |
| v11 board | thesis, hero, six contributions, what agents do, results, objections, scope | commit aff0c21 |
| v11.1 | R1 mutation test (17 corruptions × 9 verification depths, leave-one-out), identity table, response to the field map, handoff doc | commit c53480c; `research/repro/v11/` |
| reviewer fix | witness keys: 111 keys, 2 organisation-vouched, one other operator domain (two metrics had been merged) | commit 415bcf7 |
| v11.2 | a research poster, not an audit: R4 memory through time; Discussion and Conclusion; guarantees table; counts and defect lists off the board | commit d47a412; `16_` §3c |
| this log | session record and next steps | this folder |

## 4. Key decisions and the reasoning behind them

- **Lead with the mechanism figure, not with results.** Two evaluation posters share the session. emem's distinct
  contribution is the protocol; the results show it works. The opening text states failure and measured effect first.
- **The mutation test is the central experiment.** Proposed by the field map, built here. It is deterministic, so it
  needs no sample and no confidence interval. It tests the verifier; model behaviour is R3 and the P1 experiment.
- **The pixel error is evidence, not a headline.** It is the production instance of mutation M15, the only
  corruption that passes signature, log and recompute. One sentence on the board; the rate and grids in the repo.
- **Refutations are scope, not debate.** Posters carry short limitations in a Discussion. Tags such as
  agreed / reframe / rebuttal, defect counts and withdrawn-claim counts stay in `research/`.
- **Numbers only with a committed source.** Six v10 numbers had none and were removed (list in `15_`, last section).
- **The board follows the code where code and docs differ** (defects 32 to 36 in `research/do_not_use/05_…`).
- **No reseal.** The poster signing key is not available to the agent and publishing to emem.dev was out of scope.
  The seal QR opens the v10 evidence track, whose steps the § marks still cite.

## 5. Things that failed, and what worked instead

| tried | result | instead |
|---|---|---|
| headless Chrome, Playwright (system Chrome and bundled Chromium) | would not launch in the sandbox | WeasyPrint 69 |
| CSS grid in WeasyPrint | row heights overestimated; grid inside flex crashed | flex with explicit mm widths |
| flex items with zero basis holding images | heights inflated | explicit widths |
| matplotlib with woff2 fonts | not loadable | fonts converted to TTF (`poster/fonts/ttf/`) |
| a figure glyph (●) missing in Plex | blank box | a drawn legend |
| push without a credential | refused | git bundle, then a push kit |
| push with the supplied token (fine-grained, `avijeetsingh1`) | 403 on push; 403 on creating a fork, although the account has admin on the repo | a classic token with `repo` scope, or run `push_v11.sh` locally |
| writing a git clone into a granted host folder | `.git` writes refused by the sandbox | plain files: bundle plus script |

## 6. Effort (as recorded by the platform)

| context | input tokens | output tokens |
|---|---|---|
| this session | 58.7 M | 320 k |
| inventory sub-agent | 26.3 M | 93 k |
| claims-audit sub-agent | 19.1 M | 107 k |
| total | 104.2 M | 520 k |

Input counts include cached context re-read on every turn. 182 code cells ran in this session. Most of them were
rendering and fitting the board (each change is checked by rendering the PNG and reading crops), about six rounds
on the hero figure, and three rounds on the results band after R1 and R4 were added.

## 7. Where each result lives

| on the board | data | script | figure |
|---|---|---|---|
| R1 mutation test | `research/repro/v11/out/mutation_matrix.json` | `research/repro/v11/mutation_suite.py` | `poster/fig/v11/r1_mutation.svg` |
| R2 agreement and handoff | §17, §18 doc rows; `research/should_do/05_EVIDENCE_AND_NUMBERS.md` | none (published numbers) | `r1_agreement.svg` (name kept for history) |
| R3 two LLMs | `research/repro/data/v8/results.json` | `research/repro/v8/` | table in HTML |
| R4 memory through time | `research/repro/data/contra_bengaluru.json` | `research/repro/verify_bitemporal.py` (live) | `r4_bitemporal.svg` |
| hero | §4 record; `research/repro/v8/proof_bundle_ndvi.cbor` | `research/repro/v8/verify_bundle.py` | `hero.svg` |
| handout only | `research/repro/data/v8/pixel_windows.json` | | `r2_pixel_audit.svg` |

## 8. Context outside this repository

- A reviewer specialist profile ("Hostile EO Reviewer") exists in the authors' workspace, set up in a separate
  session, for an adversarial read of the board before printing.
- The emem capability index notes upstream doc defects worth fixing before Berlin: `docs/protocol.md` §3 says
  fact_cid is 16 bytes while code uses 32 (52 base32 characters); the agent card still lists geotessera as a live
  band; the CHANGELOG 2.4.2 counts are stale.
