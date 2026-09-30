---
emem: pointer.v1
source: https://raw.githubusercontent.com/Vortx-AI/emem/18adb67895d33c8b64d3b091a90af1f708315123/docs/how-emem-compares.md
bytes: 15505
etag: not exposed
kind: text (line ranges)
chunks: 2 of 278 lines hashed
root: arbxjsuvjup7wofuxg7lxq3ysxafms2tvexe473wtajpolbx3yia
hash: blake3-256 of each chunk's bytes
order: as cited
---

# how-emem-compares.md at Vortx-AI/emem 18adb67

> the architecture comparison and the safety result. The file stays on GitHub at a pinned commit; each row below names exact bytes of it, which anyone can range-read and hash. Cited by the EMEM poster at Agentic AI for Earth Observation, Berlin, 19 Oct 2026.

### lines 79–96

> / architecture / exact / confidently wrong / what it means /
> /---/---/---/---/
> / citation + value in context / 284/284 / 0 / lossless /
> / plain context (control) / 284/284 / 0 / lossless /
> / citation alone, dereferenced / 99.2% end-to-end / 0 / lossless after the last-mile fix, 84.4% before /
> / dense retrieval, top-5 / 4/142 / up to 138 / fails, and fails *confidently*, by a median 252 m /
> / **BM25 lexical, top-5** / **16/16** / 0 / **matches addressing, without addressing** /
> / summarised memory, tight budget / 1/72 / most of the rest / fails /
> 
> **The first two rows tie, and that matters more than it looks.** Our own
> re-scoring found the citation arm displays a *rounded* value, so it and plain
> context are measuring the same skill: copying a number already in the window.
> **Addressing contributes nothing measurable in that arm.** If your answer needs
> one value and it fits, context is not worse than emem. It is the same, and
> cheaper.
> 
> The dereference row is the one that tests what emem claims, and it only reaches
> 99.2% *after* four fixes prompted by the benchmark finding it at 84.4%.
### lines 102–109

> 
> - one model **abstained** 74/96
> - the other **emitted a confident wrong number** 93/96
> 
> The wrong numbers were real measurements from *neighbouring cells*: plausible,
> correctly formatted, and wrong. That is the failure that survives a sanity check
> and flips a threshold decision. Possession of the exact bytes eliminated
> confident value errors in 280 arm-model observations.

## Chunks

| what | url (· is the source) | offset | length | blake3 | stats |
|---|---|---|---|---|---|
| lines 79–96 · exact vs confidently wrong: citation 99.2 %, dense 4/142, BM25 16/16 | · | 4405 | 1099 | aebrrax6skerfs5z2bs67wlg5er6qptyj7nhwtgznfen2xvs2p4q |  |
| lines 102–109 · on retrieval failure: abstained 74/96, confident wrong 93/96 | · | 5672 | 376 | w544or4afxpdl5alltzawb4c2o7i6ycvm736ciicf7rfv3eg7l2q |  |
