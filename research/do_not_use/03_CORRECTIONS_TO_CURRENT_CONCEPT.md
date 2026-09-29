# Errors in the earlier poster concept, found by checking the code

Snapshot: 2026-09-29. Each line below appeared in `POSTER_CONCEPT.md`, `README.md` or the
ChatGPT planning conversation. The code says otherwise. Full evidence is in
`../should_do/04_VERIFIED_CLAIMS_LEDGER.md`.

| # | what we wrote | what is true | fix |
|---|---|---|---|
| 1 | `O = (a,b,t,v,u,p,s)`, where `s` is the signature | the fact has `signer` (a public key) and `signed_at`. The ed25519 signature is on the *attestation*, over a Merkle root of fact CIDs | say "signer + signed_at in the fact; signature on the attestation" |
| 2 | `CID = Base32(BLAKE3(CanonicalCBOR(O)))` | the encoding is **emem-CBOR**: deterministic, *declaration-ordered*, float-canonical, **not RFC 8949 key-sorted**. A generic canonical-CBOR encoder gives a different digest | write `emem-CBOR`, with a footnote |
| 3 | "equal canonical bytes independently produce the same name", read as "two systems observing the same thing agree" | `signer` and `signed_at` are hashed, so **two attesters of one value mint different CIDs**. We saw this live (two CIDs for 915.07 m) | "a CID names one signed attestation; independent observations meet at `(cell, band, tslot)` and their disagreement is scored" |
| 4 | "the resolver re-hashes" | the resolver checks the cell and fails with 409. **The client** re-hashes the served bytes | "resolve returns the exact bytes; you re-hash" |
| 5 | token family includes `LOG / PROOF` (and `FILE`) | no such tokens exist. Logs are REST routes. The real extra families are `trace`, `attestation`, `state`, `tree` | use the table in the ledger, §3 |
| 6 | "the receipt binds the query context" | it binds request id, time, primitive, cells, fact CIDs, as-of, manifest, field and Merkle. **It does not bind the full query parameters** | "binds what was served, not what was asked" |
| 7 | `cell64` shown as hierarchical / H3-like | the live grid is a quantized lat/lng grid of about 9.55 m, at one resolution. The H3-like grid is a migration target | "a deterministic 64-bit cell, about 9.55 m" |
| 8 | "the embedding's encoder/checkpoint is pinned" | there is no per-fact checkpoint hash. The encoder is pinned by `fn_key@version` + the band manifest | "pinned by recipe and band manifest" |
| 9 | Clay / Prithvi / Galileo shown as live encoders | **retired**: old facts verify, no new ones are minted. Tessera is live | show Tessera as live; the others as history |
| 10 | "algorithms are pinned into receipts" | `algorithms_cid` is published but **not in the receipt preimage** | pin claims to: bands, sources, schema, function registry |
| 11 | "encode in orbit, decode at emem" | nothing runs in orbit. There are a simulated satellite-downlink example and a simulated Orin stream. Hardware enrolment refuses everything today. The decoders in diagram 31 are retired | a side panel titled "same primitive at the edge, simulated"; hardware attestation as open work |
| 12 | "tokens move instead of files, so they save context" | a single fact token costs **9.5× the LLM tokens** of the value it names. Only **bundles** (38 characters, flat to 256) save context | "the *bundle* handle is flat" |
| 13 | "multi-agent handoff across vendors (Claude → GPT → Mistral)" | the measured cross-model handoffs are **Gemma ↔ Qwen** only | name the models actually tested |
| 14 | "formal protocol guarantees" | no TLA+, Kani, proptest or fuzzing; conformance vectors exist for `os_trace` only | "open work: machine-checked proofs, full vectors" |
| 15 | "time-travel queries return old state" | as-of reads work, but an auditor found the superseded 918.0 fact was **not returned by an `as_of_signed_at` query**; it is only reachable by CID | re-check before claiming; otherwise say "old tokens still resolve" |
| 16 | Paper title in README: "emem: A research on…" | the programme lists "EMEM: A Content-Addressed…" | print the programme's accepted title |

## What survives intact, and is stronger than we thought

- Spatial binding is fail-closed: 409 on a mismatched cell, band or date.
- The bytes served are the bytes hashed. We verified this with stock BLAKE3 on three
  production facts.
- The receipt signs an explicit ABSENT marker when there is no proof, so stripping the proof
  is detectable.
- The RFC 6962-style transparency log has a live independent witness.
- Bi-temporal fields (`tslot` / `signed_at`) with `as_of` reads.
- Signed absence; contradictions scored, not averaged.
