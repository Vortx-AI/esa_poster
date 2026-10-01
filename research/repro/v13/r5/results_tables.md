# R5 generated tables

Primary false acceptance (in-scope items; k/n, Wilson 95 %)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 59/59 (100 %, 94-100) | 45/60 (75 %, 63-84) | 59/59 (100 %, 94-100) | 46/56 (82 %, 70-90) | 0/64 (0 %, 0-6) | 0/63 (0 %, 0-6) | 0/62 (0 %, 0-6) |
| sonnet | 63/75 (84 %, 74-91) | 32/75 (43 %, 32-54) | 46/75 (61 %, 50-72) | 24/81 (30 %, 21-40) | 0/80 (0 %, 0-5) | 0/80 (0 %, 0-5) | 0/81 (0 %, 0-5) |
| opus | 18/21 (86 %, 65-95) | 8/22 (36 %, 20-57) | 12/21 (57 %, 37-76) | 6/23 (26 %, 13-46) | 0/25 (0 %, 0-13) | 0/25 (0 %, 0-13) | 0/24 (0 %, 0-14) |
| qwen2.5-7b-instruct-q4_k_m | 7/7 (100 %, 65-100) | 7/7 (100 %, 65-100) | - | - | - | 1/8 (12 %, 2-47) | 3/9 (33 %, 12-65) |
| pooled Claude | 140/155 (90.3 %, 84.7-94.0) | 85/157 (54.1 %, 46.3-61.7) | 117/155 (75.5 %, 68.2-81.6) | 76/160 (47.5 %, 39.9-55.2) | 0/169 (0.0 %, 0.0-2.2) | 0/168 (0.0 %, 0.0-2.2) | 0/167 (0.0 %, 0.0-2.2) |
| deterministic ceiling | 23/23 | 23/23 | 23/23 | 20/24 | 0/25 | 0/25 | 0/25 |

Decision accuracy, all items incl. controls (k/n)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 18/75 | 33/75 | 19/75 | 26/72 | 79/81 | 79/79 | 77/79 |
| sonnet | 31/94 | 67/95 | 51/94 | 74/102 | 102/102 | 102/102 | 103/103 |
| opus | 9/27 | 19/28 | 14/27 | 18/29 | 31/32 | 31/32 | 30/30 |
| qwen2.5-7b-instruct-q4_k_m | 0/8 | 0/7 | - | - | - | 6/9 | 6/11 |

False refusal on controls G0, G0-B (k/n)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 0/16 | 0/15 | 0/16 | 0/16 | 0/14 | 0/14 | 0/15 |
| sonnet | 0/19 | 0/20 | 0/19 | 0/21 | 0/19 | 0/19 | 0/19 |
| opus | 1/6 | 2/6 | 0/6 | 0/6 | 0/6 | 1/6 | 0/5 |
| qwen2.5-7b-instruct-q4_k_m | 0/1 | 0/0 | - | - | - | 1/1 | 0/1 |

Tests (Claude, per model)

```
{
 "claude-haiku-4-5-20251001": {
  "E<A": {
   "p_one_sided": 2.78e-36,
   "p_holm": 1.11e-35
  },
  "E<B": {
   "p_one_sided": 5.93e-21,
   "p_holm": 5.93e-21
  },
  "E<C": {
   "p_one_sided": 2.78e-36,
   "p_holm": 1.11e-35
  },
  "E<D": {
   "p_one_sided": 1.57e-23,
   "p_holm": 3.14e-23
  },
  "X1_E0_vs_E": {
   "p_two_sided": 1.0,
   "exploratory": true
  },
  "X2_E_vs_E+": {
   "p_two_sided": 1.0,
   "exploratory": true
  }
 },
 "claude-sonnet-5-5": {
  "E<A": {
   "p_one_sided": 1.35e-31,
   "p_holm": 5.38e-31
  },
  "E<B": {
   "p_one_sided": 1.04e-12,
   "p_holm": 2.08e-12
  },
  "E<C": {
   "p_one_sided": 8.46e-20,
   "p_holm": 2.54e-19
  },
  "E<D": {
   "p_one_sided": 9.45e-09,
   "p_holm": 9.45e-09
  },
  "X1_E0_vs_E": {
   "p_two_sided": 1.0,
   "exploratory": true
  },
  "X2_E_vs_E+": {
   "p_two_sided": 1.0,
   "exploratory": true
  }
 },
 "claude-opus-5-5": {
  "E<A": {
   "p_one_sided": 4.72e-10,
   "p_holm": 1.89e-09
  },
  "E<B": {
   "p_one_sided": 0.00102,
   "p_holm": 0.00203
  },
  "E<C": {
   "p_one_sided": 7.55e-06,
   "p_holm": 2.27e-05
  },
  "E<D": {
   "p_one_sided": 0.00823,
   "p_holm": 0.00823
  },
  "X1_E0_vs_E": {
   "p_two_sided": 1.0,
   "exploratory": true
  },
  "X2_E_vs_E+": {
   "p_two_sided": 1.0,
   "exploratory": true
  }
 }
}
```
