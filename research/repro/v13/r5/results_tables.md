# R5 generated tables

Primary false acceptance (in-scope items; k/n, Wilson 95 %)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 138/138 (100 %, 97-100) | 106/138 (77 %, 69-83) | 138/138 (100 %, 97-100) | 113/144 (78 %, 71-84) | 2/150 (1 %, 0-5) | 0/150 (0 %, 0-2) | 0/150 (0 %, 0-2) |
| sonnet | 97/115 (84 %, 77-90) | 50/115 (43 %, 35-53) | 70/115 (61 %, 52-69) | 35/120 (29 %, 22-38) | 0/125 (0 %, 0-3) | 0/125 (0 %, 0-3) | 0/125 (0 %, 0-3) |
| opus | 19/23 (83 %, 63-93) | 8/23 (35 %, 19-55) | 12/23 (52 %, 33-71) | 6/24 (25 %, 12-45) | 0/25 (0 %, 0-13) | 0/25 (0 %, 0-13) | 0/25 (0 %, 0-13) |
| qwen2.5-7b-instruct-q4_k_m | 22/23 (96 %, 79-99) | 19/21 (90 %, 71-97) | - | - | - | 2/23 (9 %, 2-27) | 10/25 (40 %, 23-59) |
| pooled Claude | 254/276 (92.0 %, 88.2-94.7) | 164/276 (59.4 %, 53.5-65.0) | 220/276 (79.7 %, 74.6-84.0) | 154/288 (53.5 %, 47.7-59.2) | 2/300 (0.7 %, 0.2-2.4) | 0/300 (0.0 %, 0.0-1.3) | 0/300 (0.0 %, 0.0-1.3) |
| deterministic ceiling | 23/23 | 23/23 | 23/23 | 20/24 | 0/25 | 0/25 | 0/25 |

Decision accuracy, all items incl. controls (k/n)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 42/174 | 74/174 | 42/174 | 67/180 | 185/192 | 192/192 | 186/192 |
| sonnet | 48/145 | 100/145 | 80/145 | 110/150 | 160/160 | 160/160 | 160/160 |
| opus | 9/29 | 20/29 | 16/29 | 19/30 | 31/32 | 31/32 | 32/32 |
| qwen2.5-7b-instruct-q4_k_m | 2/25 | 3/23 | - | - | - | 20/26 | 14/28 |

False refusal on controls G0, G0-B (k/n)

| model | A | B | C | D | E0 | E | E+ |
|---|---|---|---|---|---|---|---|
| haiku | 0/36 | 0/36 | 0/36 | 0/36 | 0/36 | 0/36 | 0/36 |
| sonnet | 0/30 | 0/30 | 0/30 | 0/30 | 0/30 | 0/30 | 0/30 |
| opus | 1/6 | 2/6 | 0/6 | 0/6 | 0/6 | 1/6 | 0/6 |
| qwen2.5-7b-instruct-q4_k_m | 0/2 | 0/2 | - | - | - | 1/2 | 0/2 |

Tests (Claude, per model)

```
{
 "claude-haiku-4-5-20251001": {
  "E<A": {
   "p_one_sided": 5.49e-86,
   "p_holm": 2.2e-85
  },
  "E<B": {
   "p_one_sided": 2.42e-50,
   "p_holm": 2.42e-50
  },
  "E<C": {
   "p_one_sided": 5.49e-86,
   "p_holm": 2.2e-85
  },
  "E<D": {
   "p_one_sided": 5.56e-53,
   "p_holm": 1.11e-52
  },
  "X1_E0_vs_E": {
   "p_two_sided": 0.498,
   "exploratory": true
  },
  "X2_E_vs_E+": {
   "p_two_sided": 1.0,
   "exploratory": true
  }
 },
 "claude-sonnet-5-5": {
  "E<A": {
   "p_one_sided": 4.33e-49,
   "p_holm": 1.73e-48
  },
  "E<B": {
   "p_one_sided": 8.44e-20,
   "p_holm": 1.69e-19
  },
  "E<C": {
   "p_one_sided": 4.36e-30,
   "p_holm": 1.31e-29
  },
  "E<D": {
   "p_one_sided": 7.29e-13,
   "p_holm": 7.29e-13
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
