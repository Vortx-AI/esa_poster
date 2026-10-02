"""Statistics over prevalence.json (and census.json): Wilson CIs, the geometric prediction, value error sizes."""
import json, math, collections, statistics
R = [r for r in json.load(open("prevalence.json")) if "error" not in r]

def wilson(k, n, z=1.959963984540054):
    if n == 0: return (float("nan"),) * 3
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, c - h, c + h

def grid(r):
    res = set(r["asset_res"]); return "10m" if res == {10.0} else ("20m" if res == {20.0} else "mixed10/20m")

def pctl(v, q):
    v = sorted(v); k = (len(v) - 1) * q; f = math.floor(k); c = min(f + 1, len(v) - 1); return v[f] + (v[c] - v[f]) * (k - f)

out = {}
for label, sel in (("pre", True), ("post", False)):
    S = [r for r in R if r["prefix_bool"] == sel]
    n = len(S); k_round = sum(r["match_class"] == "matches-round" for r in S)
    k_floor = sum(r["match_class"] == "matches-floor" for r in S)
    k_same = sum(r["match_class"] == "floor=round" for r in S)
    k_other = sum(r["match_class"] in ("matches-other", "no-match", "both(equal DNs)") for r in S)
    diff = [r for r in S if r["match_class"] != "floor=round"]
    o = dict(n=n, cells=len({r["cell"] for r in S}), scenes=len({r["scene"] for r in S}), bands=dict(collections.Counter(r["band"] for r in S)),
             providers=dict(collections.Counter(r["provider"] for r in S)),
             signed_at_range=[min(r["signed_at"] for r in S), max(r["signed_at"] for r in S)],
             matches_round_not_floor=k_round, matches_floor_not_round=k_floor, floor_equals_round_pixel=k_same, other=k_other,
             frac_round_wilson95=wilson(k_round, n), frac_floor_wilson95=wilson(k_floor, n),
             of_facts_where_rules_differ=dict(n=len(diff), round=sum(r["match_class"] == "matches-round" for r in diff),
                                              floor=sum(r["match_class"] == "matches-floor" for r in diff),
                                              frac_round_wilson95=wilson(sum(r["match_class"] == "matches-round" for r in diff), len(diff))))
    # geometric prediction by asset grid mix; uniform sub-pixel positions -> 0.75 for one grid, 1-(1/4)^2=0.9375 for 10 m + 20 m
    pred = {"10m": 0.75, "20m": 0.75, "mixed10/20m": 1 - 0.0625}
    g = collections.defaultdict(lambda: [0, 0])
    for r in S: g[grid(r)][0] += 1; g[grid(r)][1] += r["match_class"] != "floor=round"
    o["rules_differ_by_grid"] = {k: dict(n=v[0], differ=v[1], frac_wilson95=wilson(v[1], v[0]), predicted=pred[k]) for k, v in g.items()}
    o["predicted_differ_fraction_for_this_band_mix"] = sum(pred[grid(r)] for r in S) / n
    # uniformity of the 10 m-grid fractional parts (first asset)
    cf = [r["col_frac"] for r in S]; rf = [r["row_frac"] for r in S]
    o["frac_parts"] = dict(col_ge_half=sum(x >= .5 for x in cf), row_ge_half=sum(x >= .5 for x in rf),
                           either_ge_half=sum(a >= .5 or b >= .5 for a, b in zip(cf, rf)), n=n,
                           ks_col=max(max(abs((i + 1) / n - x), abs(i / n - x)) for i, x in enumerate(sorted(cf))),
                           ks_row=max(max(abs((i + 1) / n - x), abs(i / n - x)) for i, x in enumerate(sorted(rf))),
                           ks_crit_95=1.358 / math.sqrt(n))
    # value error: |signed - containing pixel|
    idx = [abs(r["signed_value"] - r["floor_value"]) for r in S if r["band"].startswith("indices.") and r["floor_value"] is not None and r["match_class"] != "floor=round"]
    ref = [abs(r["signed_value"] - r["floor_value"]) for r in S if r["band"].startswith("s2.B") and r["match_class"] != "floor=round"]
    idx_all = [abs(r["signed_value"] - r["floor_value"]) for r in S if r["band"].startswith("indices.") and r["floor_value"] is not None]
    ref_all = [abs(r["signed_value"] - r["floor_value"]) for r in S if r["band"].startswith("s2.B")]
    for name, v in (("abs_err_index_where_differ", idx), ("abs_err_reflectance_where_differ", ref), ("abs_err_index_all", idx_all), ("abs_err_reflectance_all", ref_all)):
        if v: o[name] = dict(n=len(v), median=statistics.median(v), p90=pctl(v, .9), max=max(v), frac_gt_0p05=sum(x > .05 for x in v) / len(v), frac_gt_0p1=sum(x > .1 for x in v) / len(v))
    nd = [r for r in S if r["band"] == "indices.ndvi" and r["match_class"] != "floor=round"]
    if nd: o["ndvi_abs_err_where_differ"] = dict(n=len(nd), median=statistics.median([abs(r["signed_value"] - r["floor_value"]) for r in nd]), max=max(abs(r["signed_value"] - r["floor_value"]) for r in nd))
    # SCL: which pixel did the signed SCL class come from?
    sc = [r for r in S if isinstance(r["scl_signed"], int) and r["scl_signed"] >= 0 and isinstance(r["scl_floor"], int)]
    o["scl"] = dict(n=len(sc), signed_eq_round=sum(r["scl_signed"] == r["scl_round"] for r in sc), signed_eq_floor=sum(r["scl_signed"] == r["scl_floor"] for r in sc),
                    round_ne_floor=sum(r["scl_round"] != r["scl_floor"] for r in sc),
                    signed_eq_round_ne_floor=sum(r["scl_signed"] == r["scl_round"] != r["scl_floor"] for r in sc),
                    signed_eq_floor_ne_round=sum(r["scl_signed"] == r["scl_floor"] != r["scl_round"] for r in sc),
                    class_changes=dict(collections.Counter(f"{r['scl_floor']}->{r['scl_signed']}" for r in sc if r["scl_signed"] != r["scl_floor"])))
    o["reader_stamp"] = dict(collections.Counter(r["reader_stamp"] or "(none)" for r in S))
    o["stamp_absent_signed_at"] = sorted(r["signed_at"] for r in S if not r["reader_stamp"])[-5:] if not sel else None
    o["value_recomputes_from_signed_dns"] = sum(r["recomputed_signed"] is not None and abs(r["recomputed_signed"] - r["signed_value"]) < 1e-9 for r in S)
    o["value_recomputable_bands"] = sum(r["recomputed_signed"] is not None for r in S)
    o["cid_ok"] = sum(bool(r["cid_ok"]) for r in S)
    out[label] = o
# the hero census for comparison
C = json.load(open("census.json"))
out["hero_census"] = dict(n=len(C), by=dict(collections.Counter(f"{'pre' if r['prefix_bool'] else 'post'}:{r['match_class']}" for r in C)),
                          scl_pre_signed_eq_round_ne_floor=sum(r["prefix_bool"] and r["scl_signed"] == r["scl_round"] != r["scl_floor"] for r in C),
                          scl_pre_round_ne_floor=sum(r["prefix_bool"] and r["scl_round"] != r["scl_floor"] for r in C))
json.dump(out, open("prevalence_summary.json", "w"), indent=1)
print(json.dumps(out, indent=1))
