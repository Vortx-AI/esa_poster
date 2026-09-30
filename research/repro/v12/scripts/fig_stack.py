# Figure (a): one Berlin cell, many instruments, every line a signed fact.
# Reads only data/case_berlin_stack.json. Run after apply_figure_style().
import json, datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

T = json.load(open("data/case_berlin_stack.json"))
rows = {(r["band"], r["tslot"]): r for r in T["rows"]}
def latest(band):
    c = [r for r in T["rows"] if r["band"] == band]
    return max(c, key=lambda r: r["tslot"])

CLASS_COL = {"direct_sensor": "#0072B2", "deterministic_index": "#009E73", "model_output": "#E69F00",
             "human_curated": "#CC79A7", "unclassified": "#8C8C8C"}
CLASS_LBL = {"direct_sensor": "direct sensor", "deterministic_index": "deterministic index",
             "model_output": "model output", "human_curated": "human curated", "unclassified": "unclassified"}

def d(s):  # ISO -> '27 Sep 2026'
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).strftime("%-d %b %Y")

# (label, band, reading formatter, when)
SPEC = [
    ("Sentinel-2C MSI, L2A", "s2.B08", lambda r: f"NIR reflectance {r['value']:.4f}", lambda r: d(r["observed_at"])),
    ("Sentinel-2C MSI, L2A", "indices.ndvi", lambda r: f"NDVI {r['value']:.3f}", lambda r: d(r["observed_at"])),
    ("Sentinel-1C C-SAR, RTC", "sentinel1_raw", lambda r: f"VV backscatter {r['value']:.2f} dB".replace("-", "\u2212"), lambda r: d(r["observed_at"])),
    ("Copernicus DEM GLO-30", "copdem30m.elevation_mean", lambda r: f"elevation {r['value']:.1f} m", lambda r: "static"),
    ("ESA WorldCover 2021", "esa_worldcover.lc_2021", lambda r: f"class {r['value']}: built-up", lambda r: "2021"),
    ("ESA CCI Biomass v7", "esa_cci_biomass.agb_t_per_ha_2022", lambda r: f"biomass {r['value']:.0f} t/ha", lambda r: "2022"),
    ("JRC Global Surface Water", "surface_water.occurrence", lambda r: f"water occurrence {r['value']:.0f} %", lambda r: "1984 to 2021"),
    ("Hansen Forest Change v1.13", "hansen.tree_cover_2000", lambda r: f"tree cover {r['value']} %", lambda r: "2000"),
    ("JRC Forest Cover 2020", "jrc_gfc2020.forest_2020", lambda r: "not forest (EUDR baseline)" if r["value"] == 0 else "forest (EUDR baseline)", lambda r: "2020"),
    ("Copernicus CAMS", "cams.no2", lambda r: f"NO\u2082 {r['value']:.1f} \u00b5g/m\u00b3", lambda r: d(r["observed_at"]) + ", 18 UTC"),
    ("Terra MODIS MOD11A2", "modis.lst_day_8day", lambda r: f"day surface temp. {r['value']:.1f} K", lambda r: d(r["observed_at"]) + ", 8-day"),
    ("DMSP-OLS F18", "nightlights.dmsp_ols_avg_dn", lambda r: f"night lights {r['value']} DN", lambda r: "2013"),
    ("Overture Maps (not EO)", "overture.buildings.count", lambda r: f"{r['value']} building footprints", lambda r: "2026-08 release"),
    ("ISRIC SoilGrids v2", "soilgrids.soc_0_30cm", lambda r: "no data: ISRIC returned null", None),
    ("CHIRPS v2.0", "chirps.precip_daily_mm", lambda r: "outside the \u00b150\u00b0 product", None),
    ("JRC Tropical Moist Forest", "jrc_tmf.deforestation_year", lambda r: "outside the \u00b130\u00b0 belt", None),
    ("NASA FIRMS, VIIRS + MODIS", "firms.active_fires", lambda r: "no active fire, 24 h", None),
]

def draw(fig_path_base):
    n = len(SPEC)
    fig = plt.figure(figsize=(16, 13))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    top, bot = 0.855, 0.115
    ys = [top - i * (top - bot) / (n - 1) for i in range(n)]
    # the cell
    cx, cy, cs = 0.075, (top + bot) / 2, 0.05
    ax.add_patch(Rectangle((cx - cs / 2, cy - cs / 2 * 16 / 13), cs, cs * 16 / 13, fc="#222222", ec="#222222", zorder=5))
    ax.text(cx, cy - cs * 16 / 13 / 2 - 0.018, "one cell", ha="center", va="top", fontsize=15, color="#222222")
    ax.text(cx, cy - cs * 16 / 13 / 2 - 0.045, "about 10 m", ha="center", va="top", fontsize=13, color="#555555")
    x_slab0, x_slab1 = 0.235, 0.275
    x_ins, x_val, x_when, x_tok = 0.29, 0.545, 0.775, 0.975
    h = (top - bot) / (n - 1) * 0.62
    for (lab, band, fmt, when), y in zip(SPEC, ys):
        r = latest(band)
        col = CLASS_COL[r["provenance_class"]]
        absent = r["kind"] == "absence"
        # converging line from the cell
        ax.plot([cx + cs / 2, x_slab0], [cy, y], color=col, lw=1.6, alpha=0.8, zorder=1, solid_capstyle="round")
        # slab (parallelogram)
        sk = 0.012
        poly = Polygon([(x_slab0, y - h / 2), (x_slab1, y - h / 2), (x_slab1 + sk, y + h / 2), (x_slab0 + sk, y + h / 2)],
                       closed=True, fc="white" if absent else col, ec=col, lw=2.2, hatch="///" if absent else None, zorder=3)
        ax.add_patch(poly)
        ax.text(x_ins, y, lab, ha="left", va="center", fontsize=17, fontweight="bold", color="#1a1a1a")
        ax.text(x_val, y, fmt(r), ha="left", va="center", fontsize=17, color="#1a1a1a",
                fontstyle="italic" if absent else "normal")
        ax.text(x_when, y, "signed absence" if absent else when(r), ha="left", va="center", fontsize=14, color="#444444")
        ax.text(x_tok, y, r["fact_cid"][:8] + "\u2026", ha="right", va="center", fontsize=13, family="monospace", color="#444444")
    # column headers
    hy = top + 0.028
    for x, s, ha in [(x_ins, "instrument or product", "left"), (x_val, "signed reading", "left"), (x_when, "valid time", "left"), (x_tok, "fact_cid", "right")]:
        ax.text(x, hy, s, ha=ha, va="bottom", fontsize=13, color="#666666")
    ax.plot([x_ins, x_tok], [hy - 0.006, hy - 0.006], color="#BBBBBB", lw=0.8)
    # title and address
    n_read = sum(1 for s in SPEC if latest(s[1])["kind"] == "primary")
    n_abs = n - n_read
    n_prod = len({s[0] for s in SPEC})
    ax.text(0.03, 0.975, f"One Berlin cell: {n} signed facts from {n_prod} products, {n_abs} of them signed absences",
            ha="left", va="top", fontsize=22, color="#111111")
    c = T["cell_centre"]
    ax.text(0.03, 0.936, f"cell {T['cell']}   {c['lat']:.4f} N, {c['lng']:.4f} E   each line re-verifies offline",
            ha="left", va="top", fontsize=15, family="monospace", color="#333333")
    # class key
    kx, ky = x_ins, 0.045
    ax.text(0.03, ky, "provenance class", ha="left", va="center", fontsize=14, color="#444444")
    used = []
    for s in SPEC:
        pc = latest(s[1])["provenance_class"]
        if pc not in used: used.append(pc)
    order = [k for k in CLASS_COL if k in used]
    xx = 0.165
    for k in order:
        ax.add_patch(Rectangle((xx, ky - 0.011), 0.022, 0.022, fc=CLASS_COL[k], ec=CLASS_COL[k]))
        t = ax.text(xx + 0.028, ky, CLASS_LBL[k], ha="left", va="center", fontsize=14, color="#222222")
        bb = t.get_window_extent(fig.canvas.get_renderer()).transformed(ax.transData.inverted())
        xx = bb.x1 + 0.022
    ax.add_patch(Rectangle((xx, ky - 0.011), 0.022, 0.022, fc="white", ec="#555555", hatch="///"))
    ax.text(xx + 0.028, ky, "signed absence", ha="left", va="center", fontsize=14, color="#222222")
    fig.savefig(fig_path_base + ".png", dpi=300)
    fig.savefig(fig_path_base + ".svg")
    return fig
