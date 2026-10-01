"""Task 2: before/after figure dataset + PNG for the hero cell (Keylong, defi.zb572.xoso.zb1ec).
Inputs: census.json (census.py), change_attr_live.json (POST /v1/change_attribution), footprint.json (footprint.py).
Outputs: fig_timeseries.csv, fig_timeseries_window.csv, fig_timeseries.png, fig_timeseries.json
"""
import csv, json, math, datetime as dt
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Polygon, Rectangle

INK, INK2, MUTED, RULE, ACC, WRONG = "#141414", "#46463F", "#85857E", "#D3D3CC", "#1F4FD8", "#B3261E"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.linewidth": .6, "xtick.major.width": .6, "ytick.major.width": .6})
C = [r for r in json.load(open("census.json")) if r["band"] == "indices.ndvi"]
C.sort(key=lambda r: (r["capture_date"], r["signed_at"]))
CA = json.load(open("change_attr_live.json")); FP = json.load(open("footprint.json"))
rows = []
for r in C:
    rows.append(dict(cid=r["cid"], capture_date=r["capture_date"], scene=r["scene"], provider=r["provider"], signed_at=r["signed_at"],
                     signed_prefix=r["prefix_bool"], ndvi_signed_served=r["signed_value"], ndvi_containing_pixel=r["floor_value"],
                     ndvi_round_pixel=r["round_value"], error=r["signed_value"] - r["floor_value"], match_class=r["match_class"],
                     scl_signed=r["scl_signed"], scl_containing=r["scl_floor"], signed_dns=r["signed_dns"], containing_dns=r["floor_dns"]))
with open("fig_timeseries.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); [w.writerow(x) for x in rows]

by = {r["cid"][:8]: r for r in C}
k23, k25 = by["kxjvfwpa"], by["oj5cecci"]
served = [e for e in CA["terms"]["env"]["evidence"] if e["band"] == "indices.ndvi"][0]
d_served = served["delta"]; d_true = k25["floor_value"] - k23["floor_value"]
ndwi = [e for e in CA["terms"]["env"]["evidence"] if e["band"] == "indices.ndwi"][0]
cen = {r["cid"]: r for r in json.load(open("census.json"))}
ndwi_now, ndwi_prev = cen[ndwi["fact_cids"][0]], cen[ndwi["fact_cids"][1]]
d_ndwi_true = ndwi_now["floor_value"] - ndwi_prev["floor_value"]

# 5x5 NDVI windows (window[i][j], floor pixel at [2][2]) for the 23 Sep and 25 Sep scenes
def ndvi_win(r):
    k = list(r["windows"]); b8 = np.array(r["windows"][[x for x in k if "B08" in x][0]], float); b4 = np.array(r["windows"][[x for x in k if "B04" in x][0]], float)
    o = r["dn_offset"]; return ((b8 + o) - (b4 + o)) / ((b8 + o) + (b4 + o)), b8, b4
W23, B8_23, B4_23 = ndvi_win(k23); W25, B8_25, B4_25 = ndvi_win(k25)
with open("fig_timeseries_window.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["scene", "cog_row", "cog_col", "B08_DN", "B04_DN", "ndvi", "is_containing_pixel", "is_round_pixel"])
    for name, Wn, b8, b4 in (("S2C 2026-09-23", W23, B8_23, B4_23), ("S2A 2026-09-25", W25, B8_25, B4_25)):
        for i in range(5):
            for j in range(5):
                w.writerow([name, 9443 - 2 + i, 9098 - 2 + j, int(b8[i, j]), int(b4[i, j]), round(float(Wn[i, j]), 6), (i, j) == (2, 2), (i, j) == (3, 2)])

# footprint in window pixel coords (x = col - (9098 - 2) ; y = row - (9443 - 2)), pixel (i,j) spans [j, j+1) x [i, i+1)
c0, r0 = 9098 - 2, 9443 - 2
fpc = [((E - 600000) / 10 - c0, (3700020 - N) / 10 - r0) for E, N in FP["utm43n_corners_NW_NE_SE_SW"]]
pt = (FP["centre_col_frac"] - c0, FP["centre_row_frac"] - r0)

def clip(poly, x0, x1, y0, y1):  # Sutherland-Hodgman against an axis-aligned box
    def cut(P, inside, inter):
        out = []
        for k in range(len(P)):
            a, b = P[k - 1], P[k]
            if inside(b):
                if not inside(a): out.append(inter(a, b))
                out.append(b)
            elif inside(a): out.append(inter(a, b))
        return out
    for ax_, v, keep in ((0, x0, 1), (0, x1, -1), (1, y0, 1), (1, y1, -1)):
        ins = lambda p, ax_=ax_, v=v, keep=keep: (p[ax_] - v) * keep >= 0
        def it(a, b, ax_=ax_, v=v):
            t = (v - a[ax_]) / (b[ax_] - a[ax_]); return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
        poly = cut(poly, ins, it)
        if not poly: return []
    return poly
area = lambda P: abs(sum(P[k - 1][0] * P[k][1] - P[k][0] * P[k - 1][1] for k in range(len(P)))) / 2 if P else 0.0
tot = area(fpc); overlap = {}
for i in range(5):
    for j in range(5):
        a = area(clip(fpc, j, j + 1, i, i + 1)) / tot
        if a > 1e-9: overlap[f"cog(row {r0 + i}, col {c0 + j})"] = a

# ---- figure
fig = plt.figure(figsize=(7.2, 2.75), dpi=300)
axA = fig.add_axes([0.065, 0.17, 0.40, 0.72]); axB = fig.add_axes([0.53, 0.17, 0.25, 0.72]); axI = fig.add_axes([0.80, 0.17, 0.195, 0.72])
def pl(ax, R, lab=True):
    for r in R:
        x = dt.date.fromisoformat(r["capture_date"])
        if abs(r["signed_value"] - r["floor_value"]) > 1e-12:
            ax.plot([x, x], [r["floor_value"], r["signed_value"]], color=MUTED, lw=.6, zorder=1)
    xs = [dt.date.fromisoformat(r["capture_date"]) for r in R]
    ax.scatter(xs, [r["floor_value"] for r in R], s=16, facecolor=ACC, edgecolor="white", lw=.6, zorder=3, label="containing pixel, re-read by us")
    pre = [r for r in R if r["prefix_bool"]]; post = [r for r in R if not r["prefix_bool"]]
    ax.scatter([dt.date.fromisoformat(r["capture_date"]) for r in pre], [r["signed_value"] for r in pre], s=16, marker="o", facecolor="white", edgecolor=WRONG, lw=1.0, zorder=4, label="signed + served, pre-fix read")
    ax.scatter([dt.date.fromisoformat(r["capture_date"]) for r in post], [r["signed_value"] for r in post], s=30, marker="s", facecolor="none", edgecolor=WRONG, lw=1.0, zorder=4, label="signed + served, post-fix read")
pl(axA, C)
axA.set_ylabel("NDVI at Keylong cell"); axA.set_ylim(-0.12, 0.85)
axA.xaxis.set_major_locator(mdates.YearLocator()); axA.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
axA.axhline(0, color=RULE, lw=.5, zorder=0)
axA.set_title(f"a  all {len(C)} NDVI facts at the cell, 2022-2026", loc="left", fontsize=7, color=INK, pad=3)
axA.legend(loc="upper left", fontsize=5.6, frameon=False, handletextpad=.3, borderaxespad=.2)
S = [r for r in C if r["capture_date"] >= "2026-06-01"]
X = list(range(len(S)))
axB.plot(X, [r["floor_value"] for r in S], color=ACC, lw=1.0, zorder=2)
axB.plot(X, [r["signed_value"] for r in S], color=WRONG, lw=1.0, zorder=2, ls=(0, (3, 1.5)))
for x, r in zip(X, S):
    if abs(r["signed_value"] - r["floor_value"]) > 1e-12: axB.plot([x, x], [r["floor_value"], r["signed_value"]], color=MUTED, lw=.6, zorder=1)
    axB.scatter([x], [r["floor_value"]], s=16, facecolor=ACC, edgecolor="white", lw=.6, zorder=3)
    axB.scatter([x], [r["signed_value"]], s=16 if r["prefix_bool"] else 30, marker="o" if r["prefix_bool"] else "s",
                facecolor="white" if r["prefix_bool"] else "none", edgecolor=WRONG, lw=1.0, zorder=4)
axB.set_xticks(X); axB.set_xticklabels([dt.date.fromisoformat(r["capture_date"]).strftime("%d %b") for r in S])
axB.set_xlim(-.4, len(S) - .6); axB.set_ylim(0.30, 0.82)
axB.set_title("b  summer 2026 (one tick per scene)", loc="left", fontsize=7, color=INK, pad=3)
i23, i25 = len(S) - 2, len(S) - 1
axB.text(i25 - .3, 0.395, f"served\n{d_served:+.3f}", fontsize=6, color=WRONG, ha="left", va="top")
axB.text(i25 - .5, 0.505, f"pixel\n{d_true:+.3f}", fontsize=6, color=ACC, ha="center", va="bottom")
for ax in (axA, axB): ax.tick_params(labelsize=6)
# inset: 23 Sep 5x5 NDVI window, containing pixel, the pixel the pre-fix read took, cell64 footprint, point
cm = plt.get_cmap("Greens")
axI.imshow(W23, cmap=cm, vmin=0.0, vmax=0.8, extent=(0, 5, 5, 0), interpolation="nearest")
for i in range(5):
    for j in range(5):
        axI.text(j + .5, i + .5, f"{W23[i, j]:.2f}", ha="center", va="center", fontsize=4.8, color=INK if W23[i, j] < .5 else "white")
axI.add_patch(Rectangle((2, 2), 1, 1, fill=False, ec=ACC, lw=1.3))
axI.add_patch(Rectangle((2, 3), 1, 1, fill=False, ec=WRONG, lw=1.1, ls=(0, (2, 1))))
axI.add_patch(Polygon(fpc, closed=True, fill=False, ec=INK, lw=.6))
axI.plot(*pt, marker="o", ms=2.2, color=INK)
axI.set_xticks([]); axI.set_yticks([])
axI.set_title("c  23 Sep, 10 m pixels", loc="left", fontsize=7, color=INK, pad=3)
axI.text(0, 5.35, "blue: pixel holding the cell centre\nred dashed: pixel the signed fact read\nblack: cell64 footprint %.2f x %.2f m" % (FP["ns_geodesic_m"], FP["ew_geodesic_m_centre"]),
         fontsize=4.9, color=INK2, va="top")
for s in axI.spines.values(): s.set_visible(False)
fig.savefig("fig_timeseries.png", dpi=300); plt.close(fig)

summ = dict(n_ndvi=len(C), n_pre=sum(r["prefix_bool"] for r in C), n_pre_round=sum(r["prefix_bool"] and r["match_class"] == "matches-round" for r in C),
            served_delta_23_25=d_served, containing_delta_23_25=d_true, k23=dict(signed=k23["signed_value"], containing=k23["floor_value"], dns_signed=k23["signed_dns"], dns_containing=k23["floor_dns"]),
            k25=dict(signed=k25["signed_value"], containing=k25["floor_value"]),
            jwkqm6eh=dict(signed=by["jwkqm6eh"]["signed_value"], containing=by["jwkqm6eh"]["floor_value"], dns_containing=by["jwkqm6eh"]["floor_dns"]),
            ndwi_served=dict(delta=ndwi["delta"], now=ndwi["value_now"], prev=ndwi["value_prev"], cids=ndwi["fact_cids"]),
            ndwi_containing=dict(now=ndwi_now["floor_value"], prev=ndwi_prev["floor_value"], delta=d_ndwi_true),
            footprint_overlap_fraction=overlap, point_in_window=pt, footprint_window_coords=fpc,
            summer_2026=[(r["capture_date"], r["signed_value"], r["floor_value"], r["signed_value"] - r["floor_value"]) for r in S],
            mean_abs_err_pre=float(np.mean([abs(r["signed_value"] - r["floor_value"]) for r in C if r["prefix_bool"]])),
            max_abs_err_pre=float(max(abs(r["signed_value"] - r["floor_value"]) for r in C if r["prefix_bool"])))
json.dump(summ, open("fig_timeseries.json", "w"), indent=1)
print(json.dumps(summ, indent=1))
