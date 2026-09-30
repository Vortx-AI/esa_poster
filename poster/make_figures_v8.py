"""v8 figures from data fetched and checked on 2026-09-30 (research/repro/data/v8/).
    python make_figures_v8.py   -> fig/pixel_audit.svg, fig/byte_funnel.svg, fig/tessera_strip.svg"""
import json, pathlib
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
HERE = pathlib.Path(__file__).parent; D = HERE.parent / "research/repro/data/v8"; OUT = HERE / "fig"
INK, INK2, MUTED, RULE, ACC, WRONG = "#141414", "#46463F", "#85857E", "#D3D3CC", "#1F4FD8", "#B3261E"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6, "svg.fonttype": "none"})

# ---- pixel audit: 5x5 NDVI around the cell centre, before and after the fix ----
pw = json.load(open(D / "pixel_windows.json"))
pre = next(v for k, v in pw.items() if k.startswith("kxjvfwpa")); post = next(v for k, v in pw.items() if k.startswith("oj5cecci"))
fig, axs = plt.subplots(1, 2, figsize=(4.6, 2.35), dpi=300)
for ax, w, title, sig in ((axs[0], pre, "S2C 23 Sep · fact kxjvfwpa… (signed 25 Sep, before the fix)", True),
                          (axs[1], post, "S2A 25 Sep · fact oj5cecci… (signed 28 Sep, after the fix)", False)):
    a = np.array(w["ndvi_5x5"]); ax.imshow(a, cmap="Greens", vmin=0.0, vmax=0.8)
    for r in range(5):
        for c in range(5):
            ax.text(c, r, f"{a[r, c]:.3f}", ha="center", va="center", fontsize=4.6, color=INK if a[r, c] < 0.55 else "#FFFFFF")
    cc, rr = w["centre_col_row"]; oc, orr = w["window_origin_col_row"]; x, y = cc - oc - .5, rr - orr - .5
    ax.plot([x], [y], marker="o", ms=2.2, color=INK)
    ax.add_patch(Rectangle((2 - .5, 2 - .5), 1, 1, fill=False, ec=ACC, lw=1.6))
    if sig:
        rr_, cc_ = w["signed_DN_location_in_window"][0]
        ax.add_patch(Rectangle((cc_ - .5, rr_ - .5), 1, 1, fill=False, ec=WRONG, lw=1.6, ls="--"))
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title(title, fontsize=5.4, color=INK, pad=3)
fig.subplots_adjust(.01, .02, .99, .88, wspace=.06); fig.savefig(OUT / "pixel_audit.svg"); plt.close(fig)

# ---- byte funnel: what moves where, log scale ----
rows = [("Sentinel-2 L2A scene, upstream (all assets)", 2_023_818_762, MUTED),
        ("bytes emem range-read for this value (3 COG heads + 3 tiles)", 1_165_033, MUTED),
        ("signed fact, emem-CBOR", 1_115, ACC),
        ("token handed to the next agent (characters)", 84, ACC)]
fig, ax = plt.subplots(figsize=(4.6, 1.45), dpi=300)
for i, (lab, v, c) in enumerate(rows):
    ax.barh(i, v, color=c, height=.42)
    ax.text(v * 1.4, i, f"{v:,}", va="center", fontsize=6.2, color=INK, fontweight="bold")
    ax.text(1.4, i - .26, lab, va="bottom", fontsize=5.4, color=INK2)
ax.set_xscale("log"); ax.set_xlim(1, 3e12); ax.set_ylim(3.5, -0.9); ax.set_yticks([])
ax.set_xlabel("bytes (log scale)", fontsize=5.8, color=INK2); ax.spines["left"].set_visible(False)
fig.subplots_adjust(.02, .24, .98, .99); fig.savefig(OUT / "byte_funnel.svg"); plt.close(fig)

# ---- Tessera: the 128 signed floats, re-derived bit for bit ----
t = json.load(open(D / "fig_tessera_data.json"))
vec = next((s.get("vector") or s.get("v") or s.get("values")) for s in t["strip"] if s["fact_cid"].startswith("ga2o2nuf"))
v = np.array(vec, dtype=float)
fig, ax = plt.subplots(figsize=(4.6, .62), dpi=300)
lim = np.abs(v).max(); ax.imshow(v[None, :], cmap="RdBu_r", vmin=-lim, vmax=lim, aspect="auto")
ax.set_yticks([]); ax.set_xticks([0, 32, 64, 96, 127]); ax.tick_params(labelsize=5)
for s in ax.spines.values(): s.set_visible(False)
fig.subplots_adjust(.01, .3, .99, .98); fig.savefig(OUT / "tessera_strip.svg"); plt.close(fig)
print("ok", len(v))

# ---- drift number line (values as signed; threshold from the logged experiment) ----
fig, ax = plt.subplots(figsize=(4.6, .95), dpi=300)
ax.axhline(0, color=INK, lw=.7); ax.set_xlim(.480, .495); ax.set_ylim(-1, 1.6)
for x in (.480, .485, .490, .495): ax.text(x, -.55, f"{x:.3f}", ha="center", fontsize=5.2, color=MUTED)
ax.axvline(.488, ymin=.1, ymax=.9, color=INK, lw=.7, ls="--"); ax.text(.488, 1.35, "water if NDVI < 0.488", ha="center", fontsize=5.6, fontweight="bold")
ax.plot([.4871541501976284], [0], "o", ms=5, color=ACC); ax.text(.4868, .45, "token: 0.4871541501976284 → both models WATER", ha="right", fontsize=5.2)
ax.plot([.49], [0], "o", ms=5, color=WRONG); ax.text(.4904, .45, "prose “≈ 0.49” → both SKIP", ha="left", fontsize=5.2, color=WRONG)
ax.axis("off"); fig.subplots_adjust(0, 0, 1, 1); fig.savefig(OUT / "drift_line.svg"); plt.close(fig)
