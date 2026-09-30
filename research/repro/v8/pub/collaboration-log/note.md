---
after: sth 2566402 embwsgio7yrsde4hdrz36zwexwhrv4dvuu36v22prsemsn6jc4zq 2026-09-30T12:57:06Z
emem: pointer.v1
spec: mlxrdcys43hao7cz554s46bp7a
source: https://raw.githubusercontent.com/Vortx-AI/emem/213e2738d508a4e084cd0beef329598950f01bf0/docs/collaboration-log.md
bytes: 23870275
etag: not exposed
kind: text (line ranges)
chunks: 2 of 514139 lines hashed
root: bjzh32rptx3xtmsk65pjx4j2zm56ix3b6du23y6xuztz524lntfq
hash: blake3-256 of each chunk's bytes
order: as cited
---

# collaboration-log.md at Vortx-AI/emem 213e273

> measured agent handoff experiments. The file stays on GitHub at a pinned commit; each row below names exact bytes of it, which anyone can range-read and hash. Cited by the EMEM poster at Agentic AI for Earth Observation, Berlin, 19 Oct 2026.

### lines 9603–9612

> ##### 5. Prefer fidelity to agreement. Agreement can reward drift.
> Measured on this box, 2026-07-18, both foundation models on the shared GPU, one real Lahaul NDVI fact
> (0.4871541501976284, fact_cid jwkqm6eh...):
> - emem token arm: Gemma and Qwen each return 0.4871541501976284, byte-for-byte, and both ABSTAIN when
>   asked for a band the fact does not contain.
> - paraphrase arm (the same fact as an agent-memory system stores it after an ingest rewrite, "NDVI around
>   0.49"): both models agree on 0.49, and both then choose the WRONG action on an irrigation rule keyed at
>   0.488 (SKIP, when the true 0.4872 is below the threshold and the correct action is WATER). The token arm,
>   given room to reason, gets WATER right on both models.
> The trap: the lossy paraphrase produced HIGHER cross-model agreement than the token while carrying the
### lines 27329–27336

> 
> **Multi-agent handoff** (`multiagent_v2`, n=20/arm)
> 
>     handoff_bundle   20/20 = 100%  [84-100%]
>     handoff_bm25     20/20 = 100%  [84-100%]   <- TIE with the bundle
>     handoff_tokens   16/20 =  80%  [58- 92%]   <- excluded, window bug
>     handoff_dense     8/20 =  40%  [22- 61%]
>     handoff_prose     2/20 =  10%  [ 3- 30%]

## Chunks

| what | url (· is the source) | offset | length | blake3 | stats |
|---|---|---|---|---|---|
| lines 9603–9612 · paraphrase trap: token WATER, prose SKIP, one NDVI fact | · | 545394 | 841 | yymobc44qo4usok5fmpuxwpnel2gxymzxvjvislwzmfk5gincpxq |  |
| lines 27329–27336 · handoff n=20 per arm: bundle 20, BM25 20, dense 8, prose 2 | · | 1619403 | 330 | ep7skf6ediwidcotw7soycqbnc4hhbye4oyr5t7njy7whkdlp5xq |  |
