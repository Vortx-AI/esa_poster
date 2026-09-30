---
emem: pointer.v1
source: https://raw.githubusercontent.com/Vortx-AI/emem/213e2738d508a4e084cd0beef329598950f01bf0/docs/how-emem-compares.md
bytes: 15505
etag: not exposed
kind: text (line ranges)
chunks: 2 of 278 lines hashed
root: gc5ddjoxnyrnb3lapcloh2sqmjdb347w7bnz7g3subeto5rxvp6a
hash: blake3-256 of each chunk's bytes
order: as cited
---

# how-emem-compares.md at Vortx-AI/emem 213e273

> token and bundle sizes, and the authors' scorecard. The file stays on GitHub at a pinned commit; each row below names exact bytes of it, which anyone can range-read and hash. Cited by the EMEM poster at Agentic AI for Earth Observation, Berlin, 19 Oct 2026.

### lines 115–120

> / axis / individual tokens / **bundled** / context / winner /
> /---/---/---/---/---/
> / citation size / 84 chars / 51 LLM tokens / 38 chars / 23 LLM tokens, any N / grows with values / **bundle** /
> / context, N facts / 51·N LLM tokens / **23 LLM tokens flat** / ~5.4·N LLM tokens / **bundle** /
> / round trips / N / **1** (to 256) / 1 / bundle / context /
> / wall clock / 69 up to 1,255 ms / **20 to 54 ms flat** / ~0.9 s total / **bundle** /
### lines 266–278

> ## Scorecard, honestly
> 
> / claim / verdict /
> /---/---/
> / A citation survives compaction where a paraphrase does not / **supported**, and it is the core claim /
> / Addressed memory beats plain context when the value fits / **refuted by our own re-scoring** /
> / Addressed memory beats *dense* retrieval on these corpora / **supported**, and it is a claim about embeddings /
> / Addressed memory beats *lexical* retrieval on these corpora / **refuted.** BM25 scores 16/16 /
> / Model agreement is evidence of correctness / **refuted**, p = 0.035 /
> / Addressed memory is O(1) / **only when bundled.** See below /
> / Individual tokens save context / **refuted, and by more than we used to claim.** A token is 84 chars / 51 LLM tokens, the value it replaces averages 10.9 chars / 5.4 LLM tokens, so N tokens cost 7.7x the characters and **9.5x the LLM tokens** of the plain numbers, and hit the context wall SOONER /
> / A bundle saves context / **supported.** 38 chars and one round trip at every N up to 256, against 26,624 chars and 256 trips /
> / emem outperforms peer memory products / **not tested. No evidence either way** /

## Chunks

| what | url (· is the source) | offset | length | blake3 | stats |
|---|---|---|---|---|---|
| lines 115–120 · token vs bundle size | · | 6128 | 441 | b4gpkpizhgjwbee6xe2czwe6756xgj4wzekenkukqj3zqtz7okmq |  |
| lines 266–278 · scorecard: what is supported, refuted, not tested | · | 14389 | 1116 | hclnh3dcwhdjsgls2ixzemzmjckcokrpdckveirtdsbfxxfms5qa |  |
