# Figures (b) Keylong NDVI series and (c) Rondonia EUDR grid. Reads only data/*.json.
import json, datetime as dt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from matplotlib.colors import ListedColormap, BoundaryNorm

PLAT = {"S2A": ("Sentinel-2A", "#56B4E9", "o"), "S2B": ("Sentinel-2B", "#0072B2", "s"), "S2C": ("Sentinel-2C", "#009E73", "^")}

def draw_ts(base, start="2025-01-01"):
    T = json.load(open("data/case_keylong_ndvi.json"))
    rows = [r for r in T["rows"] if r["date"] >= start and r["verified"]]
    x = np.array([dt.date.fromisoformat(r["date"]) for r in rows]); y = np.array([r["value"] for r in rows])
    fig, ax = plt.subplots(figsize=(16, 6.6))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.83, bottom=0.12)
    ax.plot(x, y, color="#BBBBBB", lw=1.2, zorder=1)
    for k, (lab, col, mk) in PLAT.items():
        sel = [i for i, r in enumerate(rows) if r["platform"] == k]
        ax.scatter(x[sel], y[sel], s=70, marker=mk, color=col, edgecolor="white", linewidth=0.6, zorder=3, label=f"{lab} ({len(sel)})")
    ax.axhline(0, color="#888888", lw=0.8, zorder=0)
    # headline points: season maxima and the poster's R1 record
    for yr in (2025, 2026):
        cand = [r for r in rows if r["date"].startswith(str(yr))]
        m = max(cand, key=lambda r: r["value"])
        xd = dt.date.fromisoformat(m["date"])
        ax.annotate(f"{m['value']:.2f}  {xd.strftime('%-d %b %Y')}\n{m['fact_cid'][:8]}\u2026", (xd, m["value"]), xytext=(0, 18),
                    textcoords="offset points", ha="center", va="bottom", fontsize=14, color="#1a1a1a", family="DejaVu Sans")
    r1 = [r for r in rows if r["fact_cid"].startswith("oj5cecci")]
    if r1:
        r1 = r1[0]; xd = dt.date.fromisoformat(r1["date"])
        ax.scatter([xd], [r1["value"]], s=260, facecolor="none", edgecolor="#D55E00", linewidth=2.2, zorder=4)
        ax.annotate(f"fact traced on the poster {r1['value']:.4f}\n{xd.strftime('%-d %b %Y')}  {r1['fact_cid'][:8]}\u2026", (xd, r1["value"]), xytext=(-28, -70),
                    textcoords="offset points", ha="right", va="top", fontsize=14, color="#D55E00",
                    arrowprops=dict(arrowstyle="-", color="#D55E00", lw=1.2))
    ax.set_ylabel("NDVI (Sentinel-2 L2A)")
    ax.set_ylim(-0.12, 0.98)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_xlim(dt.date(2024, 12, 20), dt.date(2026, 10, 15))
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax.legend(loc="upper left", frameon=False, ncol=1, bbox_to_anchor=(0.50, 1.0), handletextpad=0.3, labelspacing=0.5)
    c = T["cell_centre"]
    fig.text(0.085, 0.955, f"Two growing seasons at one Keylong field cell: {len(rows)} signed NDVI readings from three satellites",
             ha="left", va="top", fontsize=20, color="#111111")
    fig.text(0.085, 0.895, f"cell {T['cell']}   {c['lat']:.4f} N, {c['lng']:.4f} E   every point: fact_cid re-derived, signature and log inclusion checked, NDVI recomputed bit-for-bit",
             ha="left", va="top", fontsize=13, color="#444444")
    fig.savefig(base + ".png", dpi=300); fig.savefig(base + ".svg")
    return fig, rows

CAT = [("forest_2020_no_later_loss", "forest 2020, no later loss", "#1B7837"),
       ("eudr_flag_forest_2020_loss_after_2020", "forest 2020, loss after 2020", "#D55E00"),
       ("loss_after_2020_on_gfc2020_non_forest", "loss after 2020, maps disagree", "#F0A06A"),
       ("cleared_2001_2020", "cleared 2001 to 2020", "#E8C872"),
       ("not_forest_2020_no_hansen_loss", "not forest in 2020", "#D9D9D9")]

def draw_ron(base):
    T = json.load(open("data/case_rondonia_eudr.json"))
    R = T["rows"]; assert all(r["all_verified"] for r in R)
    n = 10
    def grid(key):
        g = np.full((n, n), np.nan, dtype=object)
        for r in R: g[r["row"], r["col"]] = r[key]
        return g
    cat = grid("eudr_category"); ly = grid("hansen.loss_year"); gfc = grid("jrc_gfc2020.forest_2020")
    flag = [(r["row"], r["col"]) for r in R if r["hansen.loss_year"] > 2020 and r["jrc_gfc2020.forest_2020"] == 1]
    disagree = [(r["row"], r["col"]) for r in R if r["hansen.loss_year"] > 2020 and r["jrc_gfc2020.forest_2020"] == 0]
    fig = plt.figure(figsize=(16, 6.0))
    W, gap, x0 = 0.2, 0.05, 0.03
    axes = [fig.add_axes([x0 + i * (W + gap), 0.19, W, W * 16 / 6.0]) for i in range(4)]
    def frame(ax):
        ax.set_xlim(-0.5, n - 0.5); ax.set_ylim(n - 0.5, -0.5); ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")
        for s in ax.spines.values(): s.set_visible(False)
    def outline(ax):
        for (rr, cc) in flag:
            ax.add_patch(Rectangle((cc - 0.5, rr - 0.5), 1, 1, fill=False, ec="#D55E00", lw=3.0, zorder=5))
    # a: EUDR categories
    ax = axes[0]; frame(ax)
    col = {k: c for k, _, c in CAT}
    for r in R:
        ax.add_patch(Rectangle((r["col"] - 0.47, r["row"] - 0.47), 0.94, 0.94, fc=col[r["eudr_category"]], ec="none"))
        if r["hansen.loss_year"] > 2020:
            ax.text(r["col"], r["row"], str(r["hansen.loss_year"])[2:],
                    ha="center", va="center", fontsize=12, fontweight="bold", color="white")
    ax.set_title(f"EUDR: {len(flag)} of {len(R)} cells flagged", loc="left", fontsize=16)
    # b: tree cover 2000
    specs = [("hansen.tree_cover_2000", "Hansen tree cover 2000 (%)", "Greens", 0, 100),
             ("esa_cci_biomass.agb_t_per_ha_2022", "ESA CCI biomass 2022 (t/ha)", "YlGn", 0, 300),
             ("indices.ndvi", "Sentinel-2 NDVI, Sep 2026", "viridis", 0, 0.9)]
    for ax, (key, title, cmap, lo, hi) in zip(axes[1:], specs):
        frame(ax)
        g = np.array(grid(key), dtype=float)
        im = ax.imshow(g, cmap=cmap, vmin=lo, vmax=hi, interpolation="nearest")
        outline(ax)
        ax.set_title(title, loc="left", fontsize=16)
        cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.05, pad=0.03, aspect=25)
        cb.ax.tick_params(labelsize=12); cb.outline.set_visible(False)
    outline(axes[0])
    # category legend in one row along the bottom
    xx = x0
    for k, lab, c in CAT:
        fig.patches.append(Rectangle((xx, 0.035), 0.012, 0.03, fc=c, ec="none", transform=fig.transFigure, figure=fig))
        t = fig.text(xx + 0.017, 0.05, lab, ha="left", va="center", fontsize=12.5)
        bb = t.get_window_extent(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
        xx = bb.x1 + 0.022
    fig.text(0.03, 0.975, "Rondonia frontier: 100 sampled cells, six signed facts per cell", ha="left", va="top", fontsize=20, color="#111111")
    lat0, lat1 = min(T["grid"]["lat"]), max(T["grid"]["lat"]); lng0, lng1 = min(T["grid"]["lng"]), max(T["grid"]["lng"])
    fig.text(0.03, 0.895, f"{abs(lat1):.3f} to {abs(lat0):.3f} S, {abs(lng1):.3f} to {abs(lng0):.3f} W, nodes about 740 m apart. "
             "Outline = EUDR flag: forest in 2020 (JRC GFC2020) and Hansen loss after 2020. Numbers = loss year, 20xx.",
             ha="left", va="top", fontsize=12, color="#444444")
    fig.savefig(base + ".png", dpi=300); fig.savefig(base + ".svg")
    return fig, flag, disagree
