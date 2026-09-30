# v11: response to the field map and the source-of-truth brief

Written 30 Sep 2026. It answers `10_EVENT_FIELD_MAP_AND_CRITIQUE.md` and `11_BROAD_SOURCE_OF_TRUTH_FOR_CODING_AGENT.md`,
which were added to `main` while v11 was being built. Both were written against the v10 board. This file records
what v11 adopted, what it adopted in a different form, what it declined and why, and what is still to do.

Note on numbering: those two files reuse the prefixes 10 and 11, which already belong to
`10_EACH_FIGURE_TELLS_A_STORY.md` and `11_ARCHITECTURE_WORKFLOW_COMPARISON_GAPS.md`. They are left in place so that
links do not break; new files continue from 15.

## Verdict

The critique is right on the three points that matter most, and v11 now acts on all three:

1. **The central experiment should be adversarial mutation, scored by false acceptance.** Built and run
   (R1, below). It is now the first result on the board and the headline of the invention paragraph.
2. **Integrity, measurement correctness, upstream identity, entity identity and truth must be kept apart.**
   The Scope box became a seven-row table, "What emem establishes", with yes / checkable / partial / no.
3. **EMEM should not compete as a guardrail, as provenance or as RAG.** An objection now names GeoGuard
   (same session), provenance-first composition (Session 2) and STAC, C2PA and PROV, and places emem under them:
   a guardrail can take emem tokens as its evidence.

## Point by point

| # | the critique asks | v11 | how |
|---|---|---|---|
| 3, 14 | lead with failure, then intervention, result, mechanism | adopted in the text, not in the layout | The problem paragraph states the failure and cites R2; the invention paragraph states the intervention and the R1 result in one sentence. The hero figure stays second: at a poster the mechanism figure is what a passer-by photographs, and it is the part of emem nobody else in the room has. Moving results above it would make the board read as one more evaluation poster in a session that already has two. |
| 4 | show integrity ≠ measurement ≠ upstream ≠ semantic correctness | adopted | "What emem establishes" table. The pixel error (R4) is framed as falsifiability, and R1 row M15 shows exactly which check catches it (the source re-read), and that signature and log do not. |
| 5 | bind immutable upstream identity; else label the edge | adopted as a label; the protocol change is upstream work | The table prints "this upstream file: partial, *upstream identity unverified*". The record names the COG URL and pixel, and the bundle carries a blake3 of the tile bytes read (`v8/proof_bundle_ndvi.cbor`, `upstream[].tile_blake3`), but no provider-issued identity is bound. Binding a signed STAC item or provider checksum is listed for emem (P2 below). |
| 6 | entity identity is unresolved | adopted | Table row "this physical entity: no"; R1 case M17 is accepted at every depth and is printed as out of scope, not hidden. |
| 7 | the agent experiment is too small for a headline | adopted | The headline is now R1, which is deterministic and needs no sample. The model studies (R2, R3) are printed with n, design and "read as descriptive". |
| 8 | eight-level ablation | adopted, nine levels plus leave-one-out | Levels A to I (prose, JSON, opaque id, hash, binding, signature, log, recompute, re-read). Leave-one-out finds five of six checks individually necessary; the hash is subsumed by the signature, which the caption says. |
| 9 | mutation list | 11 of 15 directly, 1 by the same test, 3 not covered; 4 added | Direct: ±1 ULP (M1), rounded (M2), wrong cell (M4, M9), wrong date (M10), stale observation and old token presented as current (M5), swapped band (M6), changed source (M11), altered derivation parameter (M12), same value different entity (M17), modified payload and token (M3, M7). Adjacent cell is caught by the same cell-equality test as wrong cell. Not covered: changed unit, altered checkpoint, altered embedding (TESSERA is retired and a vector is attester-only, so the honest cell there is "not recomputable"). Added: forged and signed under another key (M13), signer arithmetic error (M14), signer pixel error (M15), equivocation (M16). |
| 9 | measure detection, false acceptance, false refusal, latency, token overhead | all but token overhead in R1 | False refusal 0 (G0 accepted at every depth); one full verification about 1.5 ms offline (1.23 ms in the committed run); token overhead is the objection "about 6× for one value". |
| 10 | reframe token overhead | adopted | "A single token buys identity, not compression. The bundle compresses." |
| 11 | a with / without counterfactual | adopted as R1 | Column A (prose) against column I (full emem) is the counterfactual, on the same 17 cases. |
| 12 | central figure: evidence handoff test | adopted as R1's matrix | Placed first among results rather than replacing the hero (see row 3). |
| 13 | cut implementation detail by about 40 % | partly | v10 had about 3,200 words; v11 has about 2,200 (−31 %). One formula block per contribution stays: at this workshop the formulas are what separate a protocol from a product. |
| 15 | thesis "Agents should hand over evidence references, not paraphrases of evidence" | kept ours, same idea | "One place, one address. One observation, one signed record. The record's name, not a paraphrase, is what crosses between agents." It says the same thing and names what the reference is. |
| 18 P1 | multiple models, runtimes, CIs | not done here | R1 is model-free, so a CI would be meaningless (every cell is deterministic). The model question is different: does an agent call the check and obey its refusal? R3 answers it for one pair of models. The harness for the multi-model version is specified in `18_V11_PROCESS_AND_HANDOFF.md` §5; it needs API keys for 4 to 6 vendors. |
| 18 P3 | QR should open a reproducible mutation test | adopted | The "Try it" QR now opens `research/repro/v11/` (resolves once this branch is merged into `main`). |

## What v11 declined

- **Making results visually dominant over the mechanism.** See row 3. The room has at least two evaluation posters;
  emem's distinct contribution is the protocol, and the results are there to show it works.
- **Dropping the formula blocks.** They are short and exact. A reviewer can check each against the code line in
  `research/repro/v10/algorithms.md`.

## What R1 found that the critique did not predict

- **The signer is the weak point, not the relay.** Every relay and forger case (T1) is stopped by signature or
  earlier. Only signer errors (T2) get past the signature; recompute stops an arithmetic error, and only the source
  re-read stops the pixel error that emem actually made in September. That makes the re-read the one check that
  protects against the operator, which is the strongest argument for keeping it cheap (1.17 MB of a 2.02 GB scene).
- **The log earns its place only against equivocation.** Without it, a second signed version shown to one agent
  (M16) gets through. Everything else the log catches is caught earlier.
- **An opaque id is almost worthless.** It stops paraphrase (B resolves the bytes itself) and typos, and nothing
  else: 13 of 16 still get through.
