# R1: the mutation test (17 cases × 9 verification depths)

```
pip install blake3 cbor2 pynacl
python research/repro/v11/mutation_suite.py      # offline, well under a second
```

Writes `out/mutation_matrix.json` (every cell, the summary, leave-one-out, input hashes), `out/mutation_matrix.csv`
(one row per mutation) and `out/summary.md`. The poster figure `poster/fig/v11/r1_mutation.svg` is drawn from the JSON
by `poster/make_figures_v11.py`, and `poster/build_v11.py` re-runs this suite first, so the board cannot drift from it.

## Design

- **Evidence:** the real Keylong NDVI record (`emem:fact:defi.zb572.xoso.zb1ec:oj5cecci…`, §4), its attestation, the
  signed tree head, inclusion path and witness, all in `../v8/proof_bundle_ndvi.cbor`; and the 5 × 5 DN windows
  re-read from the public Sentinel-2 COGs, `../data/v8/pixel_windows.json`.
- **Question:** NDVI at cell `defi.zb572.xoso.zb1ec`, tslot 20721. **Rule:** irrigate iff NDVI ≤ 0.4705 (R3's rule).
- **Outcome per cell:** *refused* (and which check refused), *acted on corrupted evidence*, *unaffected* (B's input
  never passed through the corrupted channel), or *acted correctly* (control). "Decision flipped" marks cases where
  the corruption also changes the irrigation decision.
- **Depths:** A prose, B JSON record, C opaque id resolved by B, D + re-hash to the cid, E + cell/band/tslot binding,
  F + Ed25519 attestation under the pinned key (batch root recomputed), G + RFC 6962 inclusion under the signed tree
  head, H + NDVI recomputed from the signed DNs, I + DNs equal the COG pixel that contains the point.
- **Threats:** T1, a relay or forger without the pinned key. T2, the trusted signer errs; simulated with a TEST key
  derived from a public string that the verifier is told to trust. Nothing is signed with emem's key.

## Result (committed run)

| depth | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| acted on corrupted evidence | 15/15 | 15/15 | 13/16 | 12/16 | 9/16 | 3/16 | 2/16 | 1/16 | 0/16 |

The control is never refused. The entity case (M17) is accepted at every depth and is out of scope by design.
Leave-one-out: without binding M4 to M6 get through; without the signature M9 to M12; without the log M16; without
recompute M14; without the re-read M15. Without the hash nothing gets through, because the signature recomputes the
batch root from the fact hashes.

## Limits, stated where the numbers are used

- The verifier is tested, not a model. Whether an agent runs the check and obeys a refusal is R3.
- The re-read compares against the committed 25 Sep window. It does not follow a forged scene id to another scene,
  so M11 is caught by the signature, not by the re-read.
- Not covered: units, model checkpoints, embeddings.
- One record, one band. The mechanisms are generic, but only this record is exercised.
