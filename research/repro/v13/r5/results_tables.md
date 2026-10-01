# R5 generated tables

Primary false acceptance (in-scope items; k/n, Wilson 95 %)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 32/32 (100 %, 89-100) | 23/31 (74 %, 57-86) | 34/34 (100 %, 90-100) | 27/32 (84 %, 68-93) | 0/32 (0 %, 0-11) | 0/37 (0 %, 0-9) | 0/32 (0 %, 0-11) |
| sonnet | 34/38 (89 %, 76-96) | 18/40 (45 %, 31-60) | 26/42 (62 %, 47-75) | 13/43 (30 %, 19-45) | 0/45 (0 %, 0-8) | 0/47 (0 %, 0-8) | 0/43 (0 %, 0-8) |
| opus | 13/15 (87 %, 62-96) | 5/12 (42 %, 19-68) | 6/11 (55 %, 28-79) | 2/12 (17 %, 5-45) | 0/13 (0 %, 0-23) | 0/12 (0 %, 0-24) | 0/12 (0 %, 0-24) |
| qwen2.5-7b-instruct-q4_k_m | 4/4 (100 %, 51-100) | 6/6 (100 %, 61-100) | - | - | - | 1/3 (33 %, 6-79) | 2/5 (40 %, 12-77) |
| pooled Claude | 79/85 (92.9 %, 85.4-96.7) | 46/83 (55.4 %, 44.7-65.6) | 66/87 (75.9 %, 65.9-83.6) | 42/87 (48.3 %, 38.1-58.6) | 0/90 (0.0 %, 0.0-4.1) | 0/96 (0.0 %, 0.0-3.9) | 0/87 (0.0 %, 0.0-4.2) |
| deterministic ceiling | 23/23 | 23/23 | 23/23 | 20/24 | 0/25 | 0/25 | 0/25 |

Decision accuracy, all items incl. controls (k/n)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 10/41 | 19/41 | 9/42 | 15/42 | 41/41 | 48/48 | 40/41 |
| sonnet | 15/50 | 35/51 | 26/50 | 35/52 | 56/56 | 60/60 | 54/54 |
| opus | 5/19 | 9/14 | 10/16 | 12/17 | 16/17 | 16/17 | 12/12 |
| qwen2.5-7b-instruct-q4_k_m | 0/5 | 0/6 | - | - | - | 2/3 | 3/7 |

False refusal on controls G0, G0-B (k/n)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 0/9 | 0/10 | 0/8 | 0/10 | 0/8 | 0/9 | 0/8 |
| sonnet | 0/12 | 0/11 | 0/8 | 0/9 | 0/9 | 0/12 | 0/9 |
| opus | 1/4 | 0/2 | 0/5 | 0/5 | 0/3 | 1/4 | 0/0 |
| qwen2.5-7b-instruct-q4_k_m | 0/1 | 0/0 | - | - | - | 0/0 | 0/1 |

Tests (Claude, per model)

```
{
 "claude-haiku-4-5-20251001": {
  "E<A": {
   "p_one_sided": 2.12e-20,
   "p_holm": 6.35e-20
  },
  "E<B": {
   "p_one_sided": 9.84e-12,
   "p_holm": 9.84e-12
  },
  "E<C": {
   "p_one_sided": 4.78e-21,
   "p_holm": 1.91e-20
  },
  "E<D": {
   "p_one_sided": 1.8e-14,
   "p_holm": 3.6e-14
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
   "p_one_sided": 1.2e-19,
   "p_holm": 4.8e-19
  },
  "E<B": {
   "p_one_sided": 5.89e-08,
   "p_holm": 1.18e-07
  },
  "E<C": {
   "p_one_sided": 8.06e-12,
   "p_holm": 2.42e-11
  },
  "E<D": {
   "p_one_sided": 2.23e-05,
   "p_holm": 2.23e-05
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
   "p_one_sided": 5.23e-06,
   "p_holm": 2.09e-05
  },
  "E<B": {
   "p_one_sided": 0.0186,
   "p_holm": 0.0373
  },
  "E<C": {
   "p_one_sided": 0.00458,
   "p_holm": 0.0137
  },
  "E<D": {
   "p_one_sided": 0.239,
   "p_holm": 0.239
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
