# The poster: A0 portrait, print-ready

| file | what it is |
|---|---|
| `emem-poster-A0.pdf` | print file, 841 × 1189 mm, fonts embedded (IBM Plex, OFL) |
| `emem-poster-preview.png` | 3179 × 4494 px preview |
| `poster.html` | the source; edit this, then re-render |
| `render.mjs` | renders the HTML to the PDF and PNG (needs `playwright-core` and Chromium) |
| `qr-*.svg` | QR codes: the repro folder, emem.dev/verify, the DOI |

Every claim on the poster is traced in `../research/should_do/04_VERIFIED_CLAIMS_LEDGER.md`
and `05_EVIDENCE_AND_NUMBERS.md`. The printed tokens and bytes were re-verified live on
2026-09-29 (`../research/repro/`).

## Structure (v3: methods-paper layout built on the invention register)

The source for every panel is `research/should_do/09_INVENTION_REGISTER.md`.

1. **Title band.** The accepted title, both authors, the DOI, the pinned emem commit, and the date of the live checks.
2. **Lead.**
   - The problem, in the authors' words: agents cannot know they mean the same observation.
   - emem's answer, and the one verification rule.
   - The token family, with the strength of each member ("openly unequal").
3. **Eight contribution panels, A1–A8.** Each panel has a mechanism line, a *live* box with values we obtained on 29 Sep, the closest **prior art**, what is **new** (to our knowledge), and its **limit**.
   - A1: self-certifying fact, with NDVI rebuilt bit-for-bit from signed DNs.
   - A2: two clocks (bitemporal replay 918.0 → 915.07).
   - A3: signed absence vs an unsigned skip.
   - A4: disagreement kept and returned.
   - A5: server recompute with a ULP gap.
   - A6: signed fields and cubes, with date distances (Keylong image).
   - A7: the guard checks the values in an agent's prose.
   - A8: the RFC 6962 log, and receipt tamper checks.
4. **Findings and reproduction.**
   - B1: agreement ≠ correctness (0/72, p = 0.035; paraphrase trap), positioned against the 2025–26 literature.
   - B2: the signed record of agents correcting each other, and the 19 withdrawals.
   - Reproduce: the scripts, MCP/pip/docker, three QR codes, and a "Not claimed" list.
5. **Footer.** Scale numbers, and a pointer to the audit's open issues.

## Before printing

- [ ] Merge this branch to `main`. The repro QR code points to
      `github.com/Vortx-AI/esa_poster/tree/main/research/repro`.
- [ ] Re-run `python research/repro/verify_fact.py <token>` on both printed tokens.
- [ ] Re-check the log size: `curl -s https://emem.dev/v1/log/witnesses | jq .current_tree_size`.
      It was 2,537,510 on 29 Sep; the poster says 2.54 M.
- [ ] Confirm the board size with the organisers. A0 portrait is assumed. If the board is
      landscape, re-flow rows 1 and 3–4 into three columns.
- [ ] Print matte, unlaminated (push pins). Also print 50 A4 copies of the preview as a
      handout.

## Re-render

```sh
npm i playwright-core
node render.mjs    # writes emem-poster-A0.pdf and emem-poster-preview.png
```
