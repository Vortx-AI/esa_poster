# Measured evidence we can print, and exactly how to print it

Snapshot: 2026-09-29. Every number keeps its sample size and caveat. Paths are relative to the
emem repo.

**Why this file matters:** at this workshop almost every poster shows an architecture. Very
few will show a **pre-registered negative result about agents**. Our numbers include one.
That is the strongest scientific card we hold.

---

## The headline finding: agreement between agents is not correctness

Source: `docs/paper-section-statistics-and-threats.md:85-89`. The prediction was
pre-registered (`l44rdbk7…`).

| arm | accuracy | cross-model agreement | Fisher (one-sided) |
|---|---|---|---|
| compaction pressure | **0/72** | 3/36 | **p = 0.035** |
| compaction free | 20/72 | 15/36 | p = 0.109 (not established) |
| full-context control | 72/72 | 36/36 | no inversion |

- **Interpretation** (`:150-155`): the error comes from a shared lossy summary, not from
  independent convergence.
- **Caveats to print:**
  - two open models (Gemma-4-12B, Qwen2.5-7B) on one host;
  - six scoring bugs were found and fixed across two scorers (`:163-166`).

**The paraphrase trap** (`docs/collaboration-log.md:9600-9613`, 2026-07-18):

- The input was one real Lahaul NDVI fact, 0.4871541501976284.
- **Token arm:** both models return the value byte-for-byte, and both abstain when asked for a
  band the fact does not contain.
- **Paraphrase arm** ("NDVI around 0.49"): the two models agree *more*, and both take the
  wrong irrigation action (SKIP instead of WATER against a 0.488 threshold).
- **The token arm gets WATER right on both models.**

**Poster line:**

> The paraphrase made two models agree more, and both made the wrong call.
> Agreement is a symptom of a shared lossy summary.

This connects directly to the Manling Li keynote on failure modes in agentic reasoning.

---

## Handoff between agents

`multiagent_v2`, n = 20 per arm (`docs/collaboration-log.md:27332-27336`):

| handoff carries | correct |
|---|---|
| `emem:bundle:` | 20/20 |
| BM25 retrieval | 20/20 (**tie**) |
| dense retrieval | 8/20 |
| **prose** | **2/20** |

The long run: 599 turns, n = 1,624 per arm, 0 call failures (`:27318-27327`). Stopped by a
13-hour deadline, not by completion.

| arm | within 1% | **citable** | median error |
|---|---|---|---|
| emem_bundle | 100% | **100%** | 0.00% |
| context | 100% | 98% | 0.00% |
| BM25 | 35% | **0%** | 22.5% |

- Exclude the `emem_resolve` arm. The log itself labels it "HARNESS DEFECT".
- **Honest framing:** BM25 ties in short handoffs. Over long runs it falls to 35%, and it is
  **never citable**. The claim is *citability and verifiability*, not "we beat retrieval on
  accuracy".

Earlier head-to-head, 5 sites (`docs/how-emem-compares.md:72-109`):

- Dense top-5 retrieval was confidently wrong, with a median location error of **252 m**.
- On retrieval failure, one model abstained 74/96 times. The other gave a confident wrong
  answer 93/96 times.
- The pooled rate of confidently wrong answers: emem 0.000; dense RAG 0.229 (Gemma) and
  0.971 (Qwen); McNemar p = 6e-05 (`docs/collaboration-log.md:14833-14850`).

---

## Cost of verification

Source: `docs/benchmarks.md:148-176`. Production host over loopback, 2026-07-11, n = 200/100.
One node. These predate the redb store, so they are marked SAMPLE.

| operation | p50 | p99 |
|---|---|---|
| offline receipt verification | **0.13 ms** | 0.17 ms |
| token dereference | 1.2 ms | |
| warm recall | 2.5 ms | 9.1 ms |
| sustained throughput | 632 req/s | |
| cold materialisation | 0.5–1.6 s | |

**Signing at the edge** (`docs/roadmap.md:94-97`), on a third-party space-object detector:

- 0.0669 ms per fact, **0.167% of a 40 ms frame**;
- 399/399 facts verified offline.

> Provenance is not what makes a real-time pipeline miss its deadline.

---

## Size of what moves

Source: `docs/how-emem-compares.md:115-146`.

- One `emem:fact:` token is 84 characters, about 51 LLM tokens. That is **9.5× the value it
  replaces.**
  - **Do not claim that tokens save context.** The authors refuted that claim themselves.
- One `emem:bundle:` handle is **38 characters, about 23 LLM tokens, flat for N ≤ 256 facts**,
  against 26,624 characters and 256 round trips unbundled.
- **Poster line:** "The handle is flat. The evidence behind it is not in your context until you
  resolve it."

---

## Real-world audit

Source: `docs/benchmarks.md:283-326`; independent read-side audit, 2026-08-11.

- A clean-room verifier reproduced the golden preimage digest.
- **5/5 tampers were rejected**, including a v1 → v2 downgrade.
- 725 requests at 1–16× concurrency: 0 errors, and 14/14 refusals were typed.
- The auditor filed 11 findings, 8 of them real defects, which were then fixed. Findings and
  fixes are published in `docs/audit-repro-2026-08-02.md`.
- Two remain **open**: P0-5 (`emem_ask` picks the wrong entity) and P0-4 (stripped proofs).
- **The unplanned drift test:** the May token still resolves to 918.0. We re-verified this on
  2026-09-29 (see `../repro/`).

---

## Scale

Re-check these the day before printing; they move.

- 5,440 cells and 90 bands; 118 wired measurements from 46 source schemes.
- **1,728,683** transparency-log entries, and **4** independent witnesses.
- The collaboration log: **216 agents** and 8,427 signed notes (8,381 signed by the caller);
  5,294 of 5,428 cited tokens resolve.
- 114 MCP tools (18 core) and 177 OpenAPI paths.

---

## The authors' own scorecard

Source: `docs/how-emem-compares.md:266-278`. **Print a version of this.** Scientists trust a
team that publishes its refutations.

| claim | verdict |
|---|---|
| A citation survives compaction where a paraphrase does not | **supported (the core claim)** |
| Addressed memory beats plain context when the value fits | refuted |
| Addressed memory beats dense retrieval | supported |
| Addressed memory beats lexical retrieval (BM25) | refuted |
| Model agreement is evidence of correctness | **refuted, p = 0.035** |
| Individual tokens save context | refuted (9.5×) |
| A bundle saves context | supported |
| emem beats peer memory products | **not tested** |

---

## Numbers NOT to print

- **LongMemEval 0.68.** It comes from a 16-item SAMPLE with a lexical fallback, and the
  authors say "never quote" (`docs/benchmarks.md:115-139`).
- **Air-gap custody record "three orders of magnitude smaller".** This was never measured.
- **"94 MCP tools / 124 measurements"** in `huggingface-space/README.md`. These are stale.
- **Any Claude → GPT → Mistral handoff.** No such experiment exists. The cross-model evidence
  is Gemma ↔ Qwen only.
