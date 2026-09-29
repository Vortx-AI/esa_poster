# Claims to keep off the poster: refuted, unmeasured, or not shipped

Snapshot: 2026-09-29. If a visitor asks about any of these, answer honestly; the answer is
in the right-hand column.

## Refuted by emem's own experiments

Source: `docs/how-emem-compares.md:266-278`.

| do not claim | what the data says |
|---|---|
| "emem beats plain context" | a tie when the value fits (284/284 vs 284/284) |
| "emem beats retrieval" | it beats **dense** retrieval; **BM25 ties** (16/16; 20/20 in handoff) |
| "tokens save context" | a single token is **9.5×** the LLM tokens of its value; only bundles save context |
| "multi-model agreement shows it works" | **refuted, p = 0.035**; agreement can rise while correctness falls |
| "emem outperforms Mem0 / Zep / Letta / LangMem" | **not tested** |

## Measured badly, or not measured

- **LongMemEval 0.68.** A 16-item sample with a lexical fallback. The authors say "never quote".
- **Air-gap "three orders of magnitude smaller".** Never measured.
- **Grid token efficiency.** cell64 is 12.5 BPE tokens, against 8.5 for H3 and about 8 for
  geohash/S2 (`docs/roadmap.md:260-272`). Do not claim cell64 is LLM-efficient.
- **Aggregates verify "exactly".** They do not. Sums show ULP gaps at N = 16, 32 and 64, so
  the bound is 4 ULP.

## Roadmap, not shipped

- Hardware-attested device enrolment (TPM, Jetson, TDX, SEV-SNP): every enrolment is refused today.
- Anything executing in orbit.
- Read federation, write sharding, quorum reads.
- 17 of 18 substrate profiles (only `earth.satellite.v0` is active).
- General multi-hop `prove(goal)` planning.
- Causal decomposition of observed change.
- Machine-checked protocol proofs; full conformance test vectors (cell64, CBOR, CID, signature).
- A ROS 2 client.
- Sleep-time refiner writes on a default responder.
- Traces in the transparency log.

## Known open defects

Source: `docs/audit-repro-2026-08-02.md`.

- **P0-5:** `emem_ask` can pick the wrong entity.
- **P0-4:** stripped-proof handling, still OPEN in that document. Check the current status
  before any stripping claim beyond "receipt v2 signs an ABSENT marker".
- **The guard does not match band to sentence.** "Rainfall 28.0 mm" citing a temperature fact
  was allowed.

## Stale numbers in emem's own public material

- `huggingface-space/README.md`: "94 MCP tools, 124 measurements". Current: 114 tools, 118
  measurements.
- `server.json` gives MCP sizes of 64/290 KB; `README.md` gives 75/324 KB.
- The verifier's reject count appears as both "sixteen" and "seventeen".
- `spec/test_vectors/README.md` lists 9 vector kinds; 1 exists.

Fix these in emem before the event. A careful visitor will find them.
