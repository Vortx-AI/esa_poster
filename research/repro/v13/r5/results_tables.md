# R5 generated tables

Primary false acceptance (in-scope items; k/n, Wilson 95 %)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 4/4 (100 %, 51-100) | 4/5 (80 %, 38-96) | 6/6 (100 %, 61-100) | 9/11 (82 %, 52-95) | 0/8 (0 %, 0-32) | 0/8 (0 %, 0-32) | 0/7 (0 %, 0-35) |
| sonnet | 9/10 (90 %, 60-98) | 4/10 (40 %, 17-69) | 5/8 (62 %, 31-86) | 2/7 (29 %, 8-64) | 0/9 (0 %, 0-30) | 0/10 (0 %, 0-28) | 0/11 (0 %, 0-26) |
| opus | 3/3 (100 %, 44-100) | 0/2 (0 %, 0-66) | - | 0/4 (0 %, 0-49) | 0/4 (0 %, 0-49) | 0/1 (0 %, 0-79) | 0/1 (0 %, 0-79) |
| qwen2.5-7b-instruct-q4_k_m | - | 1/1 (100 %, 21-100) | - | - | - | 0/2 (0 %, 0-66) | 1/2 (50 %, 9-91) |
| pooled Claude | 16/17 (94.1 %, 73.0-99.0) | 8/17 (47.1 %, 26.2-69.0) | 11/14 (78.6 %, 52.4-92.4) | 11/22 (50.0 %, 30.7-69.3) | 0/21 (0.0 %, 0.0-15.5) | 0/19 (0.0 %, 0.0-16.8) | 0/19 (0.0 %, 0.0-16.8) |
| deterministic ceiling | 23/23 | 23/23 | 23/23 | 20/24 | 0/25 | 0/25 | 0/25 |

Decision accuracy, all items incl. controls (k/n)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 1/5 | 3/7 | 2/7 | 4/13 | 10/10 | 10/10 | 9/10 |
| sonnet | 4/13 | 9/13 | 5/10 | 6/9 | 10/10 | 10/10 | 13/13 |
| opus | 2/5 | 2/2 | 2/2 | 5/6 | 6/6 | 2/2 | 1/1 |
| qwen2.5-7b-instruct-q4_k_m | - | 0/1 | - | - | - | 2/2 | 2/3 |

False refusal on controls G0, G0-B (k/n)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 0/1 | 0/2 | 0/1 | 0/2 | 0/2 | 0/2 | 0/2 |
| sonnet | 0/3 | 0/3 | 0/2 | 0/2 | 0/1 | 0/0 | 0/1 |
| opus | 0/2 | 0/0 | 0/2 | 0/2 | 0/2 | 0/0 | 0/0 |
| qwen2.5-7b-instruct-q4_k_m | - | 0/0 | - | - | - | 0/0 | 0/0 |

Tests (Claude, per model)

```
{
 "claude-haiku-4-5-20251001": {
  "E<A": {
   "p_one_sided": 0.00202,
   "p_holm": 0.00404
  },
  "E<B": {
   "p_one_sided": 0.00699,
   "p_holm": 0.00699
  },
  "E<C": {
   "p_one_sided": 0.000333,
   "p_holm": 0.00133
  },
  "E<D": {
   "p_one_sided": 0.000595,
   "p_holm": 0.00179
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
   "p_one_sided": 5.95e-05,
   "p_holm": 0.000238
  },
  "E<B": {
   "p_one_sided": 0.0433,
   "p_holm": 0.0867
  },
  "E<C": {
   "p_one_sided": 0.00654,
   "p_holm": 0.0196
  },
  "E<D": {
   "p_one_sided": 0.154,
   "p_holm": 0.154
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
   "p_one_sided": 0.25,
   "p_holm": 0.75
  },
  "E<B": {
   "p_one_sided": 1.0,
   "p_holm": 1.0
  },
  "E<D": {
   "p_one_sided": 1.0,
   "p_holm": 1.0
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
