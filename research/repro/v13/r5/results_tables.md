# R5 generated tables

Primary false acceptance (in-scope items; k/n, Wilson 95 %)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 80/80 (100 %, 95-100) | 61/79 (77 %, 67-85) | 74/74 (100 %, 95-100) | 67/82 (82 %, 72-89) | 1/94 (1 %, 0-6) | 0/88 (0 %, 0-4) | 0/82 (0 %, 0-4) |
| sonnet | 84/101 (83 %, 75-89) | 46/104 (44 %, 35-54) | 61/101 (60 %, 51-69) | 28/105 (27 %, 19-36) | 0/112 (0 %, 0-3) | 0/113 (0 %, 0-3) | 0/111 (0 %, 0-3) |
| opus | 19/23 (83 %, 63-93) | 8/23 (35 %, 19-55) | 12/23 (52 %, 33-71) | 6/24 (25 %, 12-45) | 0/25 (0 %, 0-13) | 0/25 (0 %, 0-13) | 0/25 (0 %, 0-13) |
| qwen2.5-7b-instruct-q4_k_m | 9/9 (100 %, 70-100) | 8/8 (100 %, 68-100) | - | - | - | 2/13 (15 %, 4-42) | 7/15 (47 %, 25-70) |
| pooled Claude | 183/204 (89.7 %, 84.8-93.2) | 115/206 (55.8 %, 49.0-62.4) | 147/198 (74.2 %, 67.7-79.8) | 101/211 (47.9 %, 41.2-54.6) | 1/231 (0.4 %, 0.1-2.4) | 0/226 (0.0 %, 0.0-1.7) | 0/218 (0.0 %, 0.0-1.7) |
| deterministic ceiling | 23/23 | 23/23 | 23/23 | 20/24 | 0/25 | 0/25 | 0/25 |

Decision accuracy, all items incl. controls (k/n)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 24/101 | 44/101 | 25/95 | 36/103 | 114/118 | 114/114 | 100/103 |
| sonnet | 45/129 | 86/128 | 73/129 | 99/133 | 142/142 | 145/145 | 142/142 |
| opus | 9/29 | 20/29 | 16/29 | 19/30 | 31/32 | 31/32 | 32/32 |
| qwen2.5-7b-instruct-q4_k_m | 0/10 | 0/9 | - | - | - | 11/15 | 8/17 |

False refusal on controls G0, G0-B (k/n)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 0/21 | 0/22 | 0/21 | 0/21 | 0/20 | 0/23 | 0/18 |
| sonnet | 0/28 | 0/24 | 0/28 | 0/28 | 0/25 | 0/28 | 0/27 |
| opus | 1/6 | 2/6 | 0/6 | 0/6 | 0/6 | 1/6 | 0/6 |
| qwen2.5-7b-instruct-q4_k_m | 0/1 | 0/1 | - | - | - | 1/1 | 0/1 |

Tests (Claude, per model)

```
{
 "claude-haiku-4-5-20251001": {
  "E<A": {
   "p_one_sided": 5.26e-50,
   "p_holm": 2.1e-49
  },
  "E<B": {
   "p_one_sided": 1.07e-29,
   "p_holm": 1.07e-29
  },
  "E<C": {
   "p_one_sided": 4.99e-48,
   "p_holm": 1.5e-47
  },
  "E<D": {
   "p_one_sided": 4.96e-33,
   "p_holm": 9.92e-33
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
   "p_one_sided": 7.94e-43,
   "p_holm": 3.18e-42
  },
  "E<B": {
   "p_one_sided": 2.5e-18,
   "p_holm": 5e-18
  },
  "E<C": {
   "p_one_sided": 1.07e-26,
   "p_holm": 3.22e-26
  },
  "E<D": {
   "p_one_sided": 1.52e-10,
   "p_holm": 1.52e-10
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
   "p_one_sided": 7.67e-10,
   "p_holm": 3.07e-09
  },
  "E<B": {
   "p_one_sided": 0.0013,
   "p_holm": 0.0026
  },
  "E<C": {
   "p_one_sided": 1.94e-05,
   "p_holm": 5.82e-05
  },
  "E<D": {
   "p_one_sided": 0.00963,
   "p_holm": 0.00963
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
