# v13 board: confirmed review findings and the fixes to apply (1 Oct 2026)

Applied in one pass, then the board is rebuilt and re-gated. Quotes are exact substrings of
`poster/src/poster.v13.html` or figure label strings; replacements are the same length or shorter.

## From the mechanism-vs-code reviewer
1. [medium] "…pass checks D to I and need a catalogue re-read." → "…pass checks D to I; metadata checks catch them." (the unit error is caught by the band registry, not the STAC catalogue). HTML panel 5 scope, f6 script `scope2`, brief §C.
2. [low] "or forge an address;" → "or match an address;" (a relay can mint a valid address for forged bytes; M8-M12 pass D, stop at F).

## From the science / language / legibility reviewer
3. [high] Panel 5 headline "Remove one check, and a named corruption passes." → "Each of five checks alone stops a corruption." (leave_one_out.D is empty; F6 boxes E, F, G, H, I only).
4. F4 rung 5 title "Wrong scale" → "Wrong scale or offset" (consequence line is the BOA-offset case).
5. F4 rung 2 line break: "10 of 10 agents saw one scene twice;" / "3 said no 23 Sep scene existed" (current break makes "3 said no" / "23 Sep scene existed").
6. Spine take line "dropped the cell from all 24 tokens" → "dropped the cell from all 24 calls" (tokens = LLM tokens elsewhere).
7. F10 "offline bundle, 9 checks 0.57 ms (4,906 B)" → "offline proof bundle 0.57 ms (4,906 B)" (nine is a third, undefined count).
8. F9 "15 Jun: 918.0 m" touches the dashed query rule: shift 2 mm left.
9. Panel 7 caption "780 pass L0 and L1 and 266 recompute at L2" → "780 pass L0 and L1; the 266 with a recipe all recompute at L2"; F8 L2 rung "266 of 780 recomputed bit for bit" → "266 of 780 carry a recipe; all 266 recompute" (514 are n/a, not failures).
10. Panel 11 "a model receiver paid 2.1 times the input tokens for the same decisions" → "a model receiver read 2.1× the tokens prose costs, same decisions".
11. Panel 7 mechanism line "Never "verified" without its layer." → "Each rung names what it still trusts."; panel 3 "each class is documented elsewhere" → "each has a published precedent".
12. F7 histogram label "index error where the rules differ" → "NDVI error where the rules differ"; add "(121 with both pixels readable)" only if that is the reason for n 121 (verify in prevalence.py before printing; else leave n 121 as is).
13. Panel 8 caption: add "; at Keylong the newer record would flip the decision." (the Keylong strip is otherwise unclaimed).
14. d_rondonia card: "five of its six" signed inputs (NDVI omitted from the card; the grid has 6 per cell).
15. Panel 4 QR caption "field by field" → "The 1,115 bytes behind the main example, decoded." (avoid "field" = farmland).
16. H1 "word-preserving corruptions" → "corruptions that keep the stated value".
17. Spine scope line: add "M7, a miscopied token, has no prose form" to explain 15 vs 16 denominators.
18. F4 right-hand rotated rail (two 14 pt lines, 262 mm, rotated): move its sentence into the panel 3 caption horizontally, or drop it.

Accepted as is: 17 pt side-panel body (recorded in build report); Dify marked LIVE (published) while "not run by us"; four "X, not Y" contrasts (each substantive); the amber production ring's protan weakness (low, 30 cm detail).

## From the numbers-vs-data reviewer (all low; every other number re-derived and correct)
19. F8 L3 "0 of 213 Keylong sources carry a hash" → "0 of 215 Keylong sources carry a hash", source research/v13/evidence/critic/cell.json (209 facts / 215 sources, 2026-10-01T01:41Z; live GET agrees); update the assert in f8_ladder.py.
20. "A record check takes 0.36 ms of CPU" → "A record check takes 0.33 ms of CPU" and F10 "all offline checks 0.36 ms" → "all offline checks 0.33 ms" (0.3565 ms per decision minus 0.0288 ms handoff construction; cost_measurements.json m2); update claims row C.cpu.
21. F11 "checked 1 Oct 2026" → "checked 30 Sep 2026" (manifest verified_utc is 30 Sep 23:10-23:40Z; the board dates by UTC everywhere else).
