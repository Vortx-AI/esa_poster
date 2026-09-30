"""Figures for the v12 board. Every SVG is drawn at its print size (1:1 placement), so font sizes are print points.

Data (no number is typed by hand; each is read from these files):
  research/repro/v11/out/mutation_matrix.json             R1 mutation matrix (deterministic, offline)
  research/repro/data/contra_bengaluru.json               R4 memory through time
  research/repro/v12/data/case_berlin_stack.json          one Berlin cell, live emem.dev, 30 Sep 2026
  research/repro/v12/data/case_keylong_ndvi.json          Keylong NDVI series, live emem.dev, 30 Sep 2026
  research/repro/v12/data/case_rondonia_eudr.json         Rondonia 10 x 10 grid, live emem.dev, 30 Sep 2026
  research/repro/v12/data/v1_bands_2026-09-30.json        the live band ontology (43 slots, 1792 dims)
  research/repro/v12/data/scene_<cell>.png + .headers     Sentinel-2 L2A chips served by emem.dev
  research/repro/v12/trace/sat042_run_stdout.txt          SAT-042 reference run (emem 04b40c5)
The compaction study numbers (R2) are the pre-registered counts printed on v10/v11 (claims map section 17).

usage: python poster/make_figures_v12.py
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Patch, Polygon, Rectangle

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
V12 = REPO / "research" / "repro" / "v12"
OUT = HERE / "fig" / "v12"
OUT.mkdir(parents=True, exist_ok=True)
for ttf in (HERE / "fonts" / "ttf").glob("*.ttf"):
    fm.fontManager.addfont(str(ttf))

INK, INK2, MUTED, RULE = "#141414", "#46463F", "#85857E", "#D3D3CC"
BLUE, BLUES, AMB, AMBS, BAD, BADS = "#1F4FD8", "#E7ECFA", "#A86B00", "#FBF1DE", "#B3261E", "#F8E3E1"
SANS, MONO = "IBM Plex Sans", "IBM Plex Mono"
# provenance classes (emem-core bands.rs ProvenanceClass); one colour per class across the whole board
CLS = {"direct_sensor": "#1F4FD8", "deterministic_index": "#0B8A6B", "model_output": "#C98A00",
       "human_curated": "#A8468A", "unclassified": "#9A9A93"}
CLS_LABEL = {"direct_sensor": "direct sensor", "deterministic_index": "deterministic index",
             "model_output": "model output", "human_curated": "human curated", "unclassified": "unclassified"}
L, S, XS = 19, 17, 15          # print points: label, secondary, floor
MM = 1 / 25.4

mpl.rcParams.update({
    "font.family": SANS, "font.size": L, "axes.labelsize": S, "xtick.labelsize": S, "ytick.labelsize": S,
    "axes.edgecolor": INK2, "axes.linewidth": 1.0, "xtick.color": INK2, "ytick.color": INK2,
    "svg.fonttype": "path", "mathtext.fontset": "custom", "mathtext.rm": SANS, "mathtext.it": SANS + ":italic",
    "axes.spines.top": False, "axes.spines.right": False, "hatch.linewidth": 1.2,
})
NUMBERS = {}   # every number a figure prints, written to fig/v12/figure_numbers.json for the claims map


def fig_mm(w, h):
    return plt.figure(figsize=(w * MM, h * MM))


def mm_axes(fig, w, h):
    """One axes over the whole figure, in millimetres, y growing downwards."""
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return ax


def check_text(fig, name, allow_overlap=()):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    tx = [(t, t.get_window_extent(r)) for t in fig.findobj(mpl.text.Text) if t.get_text().strip() and t.get_visible()]
    small = [t.get_text() for t, _ in tx if t.get_fontsize() < XS - 0.01]
    fb = fig.bbox
    out = [t.get_text() for t, b in tx if b.x0 < fb.x0 - 1 or b.x1 > fb.x1 + 1 or b.y0 < fb.y0 - 1 or b.y1 > fb.y1 + 1]
    def core(b):   # matplotlib boxes include line leading; test the glyph core (70 % of the box height)
        pad = 0.15 * b.height
        return mpl.transforms.Bbox([[b.x0, b.y0 + pad], [b.x1, b.y1 - pad]])
    cores = [(t, core(b)) for t, b in tx]
    bad = [(a.get_text(), c.get_text()) for i, (a, ba) in enumerate(cores) for c, bc in cores[i + 1:]
           if ba.overlaps(bc) and not any(k in a.get_text() or k in c.get_text() for k in allow_overlap)]
    assert not small, f"{name}: text below {XS} pt: {small[:5]}"
    assert not out, f"{name}: clipped labels: {out[:5]}"
    assert not bad, f"{name}: overlapping labels: {bad[:5]}"


def save(fig, name):
    fig.savefig(OUT / f"{name}.svg", transparent=True)
    fig.savefig(OUT / f"{name}.png", dpi=200, transparent=False, facecolor="white")
    plt.close(fig)


# ---- 1. the failure: agreement is not evidence (pre-registered compaction study, claims map section 17) ----
COMPACTION = [("full context (control)", 72, 72, 36, 36),
              ("shared summary, no pressure", 20, 72, 15, 36),
              ("shared summary, under pressure", 0, 72, 3, 36)]


def fig_failure(w=372, h=84):
    fig = fig_mm(w, h)
    a = fig.add_axes([0.345, 0.2, 0.64, 0.78])
    hh = 0.36
    for i, (lab, c, n, ag, npair) in enumerate(COMPACTION):
        a.barh(i - hh / 2, ag / npair, hh, color="#C98A00")
        a.barh(i + hh / 2, max(c / n, 0.005), hh, color=INK)
        a.text(ag / npair + 0.015, i - hh / 2, f"{ag}/{npair} pairs agree", va="center", fontsize=S, color=AMB)
        a.text(max(c / n, 0.005) + 0.015, i + hh / 2, f"{c}/{n} answers right", va="center", fontsize=S,
               color=BAD if c == 0 else INK, fontweight=700 if c == 0 else 400)
    a.set_yticks(range(3), [r[0] for r in COMPACTION], fontsize=S)
    a.set_xlim(0, 1.4)
    a.set_xticks([0, .5, 1], ["0", "50 %", "100 %"])
    a.spines["bottom"].set_bounds(0, 1)
    a.invert_yaxis()
    a.tick_params(axis="y", length=0)
    NUMBERS["failure"] = {"rows": COMPACTION}
    check_text(fig, "failure")
    save(fig, "failure")


# ---- 3. R1: 17 mutations x 9 verification depths ----
def fig_mutation(w=468, h=214):
    d = json.load(open(REPO / "research/repro/v11/out/mutation_matrix.json"))
    muts = d["meta"]["mutations"]
    by = {(r["mutation"], r["level"]): r for r in d["rows"]}
    cols = [("A", "prose"), ("B", "JSON"), ("C", "opaque id"), ("D", "hash"), ("E", "binding"),
            ("F", "signature"), ("G", "log"), ("H", "recompute"), ("I", "re-read")]
    short = {
        "G0": "control: nothing altered", "M1": "stated value +1 ULP", "M2": "stated value rounded to 0.47",
        "M3": "1 ULP changed in served bytes", "M4": "record cited for another cell",
        "M5": "older record passed as current", "M6": "record for another band", "M7": "token miscopied by 1 char",
        "M8": "value forged to 0.45, re-hashed", "M9": "cell forged, re-hashed", "M10": "date forged, re-hashed",
        "M11": "source scene forged, re-hashed", "M12": "offset forged, value recomputed",
        "M13": "forged, signed by own key", "M14": "signer: value disagrees with DNs",
        "M15": "signer: DNs of the pixel 10 m south", "M16": "signer: second version, not logged",
        "M17": "same bytes, a different entity"}
    groups = [("G0",), ("M1", "M2", "M3"), ("M4", "M5", "M6", "M7"), ("M8", "M9", "M10", "M11", "M12", "M13"),
              ("M14", "M15", "M16"), ("M17",)]
    gnames = ["", "paraphrase, relay", "misbinding", "forgery without the key", "the trusted signer errs",
              "out of scope"]
    real = {m["id"] for m in muts if m["real_case"]}
    RED, PALE, GREYC = "#B3261E", "#CFDBF6", "#E4E4DE"
    rowh, gap = 1.0, 1.15
    ys, y, gy = {}, 0.0, []
    for gi, g in enumerate(groups):
        if gi:
            y += gap
        gy.append(y)
        for m in g:
            ys[m] = y
            y += rowh
    ymax = y
    fig = fig_mm(w, h)
    ax = fig.add_axes([0, 0.075, 1, 0.925])
    LX = -0.25
    for m in ys:
        for j, (lv, _) in enumerate(cols):
            o = by[(m, lv)]["outcome"]
            fc = {"acted on corrupted evidence": RED, "refused": BLUE, "unaffected": PALE,
                  "acted correctly": GREYC, "n/a": "#FFFFFF"}[o]
            ax.add_patch(Rectangle((j + 0.05, ys[m] + 0.08), 0.9, rowh - 0.16, fc=fc, ec="none"))
            if o == "refused":
                ax.text(j + 0.5, ys[m] + rowh / 2, by[(m, lv)]["failed_check"], ha="center", va="center",
                        fontsize=XS, color="#FFFFFF", fontweight=600)
            if o == "n/a":
                ax.text(j + 0.5, ys[m] + rowh / 2, "n/a", ha="center", va="center", fontsize=XS, color=MUTED)
        ax.text(LX, ys[m] + rowh / 2, short[m], ha="right", va="center", fontsize=15.5, color=INK if m != "G0" else INK2)
        ax.text(-6.9, ys[m] + rowh / 2, m, ha="left", va="center", fontsize=15.5, fontweight=600,
                color=AMB if m in real else MUTED)
    for gi, name in enumerate(gnames):
        if name:
            ax.text(-6.9, gy[gi] - 0.12, name.upper(), ha="left", va="bottom", fontsize=XS, color=MUTED, fontweight=600)
    for j, (lv, name) in enumerate(cols):
        ax.text(j + 0.5, -0.55, name, ha="center", va="bottom", fontsize=XS, color=BLUE if lv == "I" else INK2,
                fontweight=600 if lv == "I" else 400)
        ax.text(j + 0.5, -1.55, lv, ha="center", va="bottom", fontsize=L + 3, fontweight=700,
                color=BLUE if lv == "I" else INK)
    sm = d["summary"]
    ax.text(LX, ymax + 0.95, "B acts on corrupted evidence", ha="right", va="center", fontsize=S, color=RED, fontweight=700)
    for j, (lv, _) in enumerate(cols):
        fa, ap = sm[lv]["false_accepts"], sm[lv]["applicable"]
        ax.text(j + 0.5, ymax + 0.95, f"{fa}/{ap}", ha="center", va="center", fontsize=S + 1,
                color=RED if fa else BLUE, fontweight=700)
    ax.annotate("", xy=(9.0, -2.95), xytext=(3.0, -2.95), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.4),
                annotation_clip=False)
    ax.text(3.0, -3.15, "emem's checks, one more per column", ha="left", va="bottom", fontsize=XS, color=INK2)
    ax.set_xlim(-7.0, 9.05)
    ax.set_ylim(ymax + 1.6, -4.75)
    ax.axis("off")
    hs = [Patch(fc=RED, label="B acts on corrupted evidence"), Patch(fc=BLUE, label="refused; letter = the check"),
          Patch(fc=PALE, label="unaffected"), Patch(fc="#FFFFFF", ec=AMB, lw=2, label="amber id: seen in production")]
    fig.legend(handles=hs, loc="lower left", ncol=4, frameon=False, fontsize=XS, bbox_to_anchor=(0.0, 0.0),
               handlelength=1.1, columnspacing=1.4)
    NUMBERS["r1"] = {lv: [sm[lv]["false_accepts"], sm[lv]["applicable"]] for lv, _ in cols}
    check_text(fig, "r1_mutation")
    save(fig, "r1_mutation")


# ---- 4. one Berlin cell, every product ----
def scene_meta(cell):
    hdr = (V12 / "data" / f"scene_{cell}.headers").read_text()
    get = lambda k: re.search(rf"(?im)^{k}:\s*(.+?)\s*$", hdr).group(1)
    return {"item": get("x-emem-scene-item-id"), "datetime": get("x-emem-scene-datetime"),
            "bbox": [float(v) for v in get("x-emem-scene-bbox-crs").split(",")]}


def fmt_date(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")[:19]).strftime("%-d %b %Y")


def fig_berlin(w=436, h=252):
    b = json.load(open(V12 / "data/case_berlin_stack.json"))
    rows = b["rows"]
    pick = lambda inst, qty, date=None: next(r for r in rows if inst in r["instrument"] and qty in r["quantity"]
                                              and (date is None or (r["observed_at"] or "").startswith(date)))
    meta = scene_meta(b["cell"])
    s2 = "Sentinel-" + meta["item"][1:3] + " MSI L2A"          # S2C_MSIL2A_20260927... -> Sentinel-2C MSI L2A
    sel = [  # (product label, row, reading)
        (s2, pick("Sentinel-2", "B08", "2026-09-27"), lambda r: f"NIR reflectance {r['value']:.4f}"),
        (s2, pick("Sentinel-2", "NDVI", "2026-09-27"), lambda r: f"NDVI {r['value']:.3f}"),
        ("Sentinel-1 C-SAR GRD, RTC", pick("Sentinel-1", "VV", "2026-09-28"), lambda r: f"VV backscatter {r['value']:.2f} dB".replace("-", "\u2212")),
        ("Copernicus DEM GLO-30", pick("Copernicus DEM", "elevation"), lambda r: f"elevation {r['value']:.1f} m"),
        ("Terra MODIS MOD11A2", pick("MOD11A2", "temperature"), lambda r: f"day surface temp. {r['value']:.1f} K"),
        ("ESA WorldCover 2021 v200", pick("WorldCover", "class"), lambda r: f"class {int(r['value'])}: built-up"),
        ("ESA CCI Biomass v7", pick("CCI Biomass", "biomass"), lambda r: f"biomass {r['value']:.0f} t/ha"),
        ("JRC Global Surface Water", pick("Surface Water", "occurrence"), lambda r: f"water occurrence {r['value']:.0f} %"),
        ("Hansen Forest Change v1.13", pick("Hansen", "tree cover"), lambda r: f"tree cover 2000: {r['value']:.0f} %"),
        ("JRC Forest Cover 2020", pick("Forest Cover 2020", "forest"), lambda r: "not forest (EUDR baseline)" if r["value"] == 0 else "forest (EUDR baseline)"),
        ("Copernicus CAMS", pick("Copernicus Atmosphere", "NO2", "2026-09-30"), lambda r: f"surface NO$_2$ {r['value']:.1f} \u00b5g/m\u00b3"),
        ("Overture Maps (not EO)", pick("Overture", "building"), lambda r: f"{int(r['value'])} building footprints"),
        ("ISRIC SoilGrids v2", pick("SoilGrids", "organic carbon"), lambda r: "no data at this cell"),
        ("CHIRPS v2.0", pick("CHIRPS", "precip"), lambda r: "outside the \u00b150\u00b0 product"),
        ("JRC Tropical Moist Forest", pick("Tropical Moist", "deforestation"), lambda r: "outside the tropical belt"),
        ("NASA FIRMS, VIIRS + MODIS", pick("FIRMS", "fire"), lambda r: "no active fire in 24 h"),
    ]
    def when(label, r):
        if r["kind"] == "absence":
            return "signed absence"
        o = r["observed_at"] or ""
        if "WorldCover" in label: return "2021"
        if "CCI" in label: return "2022"
        if "Surface Water" in label: return "1984 to 2021"
        if "Hansen" in label: return "2000"
        if "Forest Cover 2020" in label: return "2020"
        if "DEM" in label: return "GLO-30 release"
        if "Overture" in label: return o[:10] + " release"
        if "CAMS" in label: return fmt_date(o) + ", 18 UTC" if o.endswith("18:00:00Z") or "T18:00" in o else fmt_date(o)
        if "MOD11A2" in label: return fmt_date(o + "T00:00:00") + ", 8-day"
        return fmt_date(o)
    fig = fig_mm(w, h)
    ax = mm_axes(fig, w, h)
    # the chip: a real Sentinel-2 L2A crop served by emem for this cell, 256 px of 10 m
    img = plt.imread(V12 / "data" / f"scene_{b['cell']}.png")
    cx0, cy0, cs = 0, 44, 82
    ax.imshow(img, extent=(cx0, cx0 + cs, cy0 + cs, cy0), zorder=1, interpolation="lanczos")
    mx, my = cx0 + cs / 2, cy0 + cs / 2
    ax.add_patch(Rectangle((mx - 2.4, my - 2.4), 4.8, 4.8, fill=False, ec="#FFD400", lw=2.4, zorder=3))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ax.plot([mx + dx * 4.5, mx + dx * 11], [my + dy * 4.5, my + dy * 11], color="#FFD400", lw=2.0, zorder=3)
    ax.plot([mx + 11, cx0 + cs + 1], [my, my], color="#FFD400", lw=2.0, zorder=3)
    km = (meta["bbox"][2] - meta["bbox"][0]) / 1000
    ax.text(cx0, cy0 + cs + 6, f"{s2}, {fmt_date(meta['datetime'])}", fontsize=XS, color=INK2, va="top")
    ax.text(cx0, cy0 + cs + 13, f"{km:.2f} km across; the cell is", fontsize=XS, color=INK2, va="top")
    ax.text(cx0, cy0 + cs + 20, "the 10 m pixel at the centre", fontsize=XS, color=INK2, va="top")
    ax.text(cx0, cy0 - 9.5, "one address", fontsize=L, color=INK, fontweight=600, va="bottom")
    ax.text(cx0, cy0 - 1.5, b["cell"], fontsize=XS, color=BLUE, family=MONO, va="bottom")
    # rows
    X_SW, X_P, X_R, X_T, X_C = 112, 127, 250, 348, w
    top, rh = 20, (h - 20 - 26) / len(sel)
    for x, lab in ((X_P, "product"), (X_R, "signed reading"), (X_T, "valid time")):
        ax.text(x, top - 3, lab, fontsize=XS, color=MUTED, va="bottom")
    ax.text(X_C, top - 3, "fact_cid", fontsize=XS, color=MUTED, va="bottom", ha="right")
    ax.plot([X_P, w], [top - 1, top - 1], color=RULE, lw=1)
    shown = []
    for i, (lab, r, reading) in enumerate(sel):
        yc = top + rh * (i + 0.5)
        cls = r["provenance_class"]
        col = CLS[cls]
        absent = r["kind"] == "absence"
        ax.plot([cx0 + cs + 1, X_SW - 1], [my, yc], color=col, lw=1.3, alpha=0.9, zorder=2)
        par = Polygon([(X_SW, yc + 4), (X_SW + 3.5, yc - 4), (X_SW + 12, yc - 4), (X_SW + 8.5, yc + 4)], closed=True,
                      fc="white" if absent else col, ec=col, lw=1.6, hatch="////" if absent else None)
        ax.add_patch(par)
        ax.text(X_P, yc, lab, fontsize=S, fontweight=600, color=INK, va="center")
        ax.text(X_R, yc, reading(r), fontsize=S, color=INK2 if absent else INK, va="center",
                style="italic" if absent else "normal")
        ax.text(X_T, yc, when(lab, r), fontsize=XS, color=MUTED, va="center")
        ax.text(X_C, yc, r["fact_cid"][:8] + "\u2026", fontsize=XS, color=MUTED, va="center", ha="right", family=MONO)
        shown.append({"product": lab, "reading": reading(r), "fact_cid": r["fact_cid"], "class": cls, "kind": r["kind"]})
    # legend
    ly = h - 7
    x = X_SW
    ax.text(x - 2, ly, "provenance class", fontsize=XS, color=MUTED, va="center", ha="right")
    for c in ("direct_sensor", "deterministic_index", "model_output", "human_curated", "unclassified"):
        ax.add_patch(Rectangle((x, ly - 3), 6, 6, fc=CLS[c], ec="none"))
        t = ax.text(x + 8, ly, CLS_LABEL[c], fontsize=XS, color=INK2, va="center")
        x += 8 + len(CLS_LABEL[c]) * 2.95 + 6
    ax.add_patch(Rectangle((x, ly - 3), 6, 6, fc="white", ec=INK2, hatch="////", lw=1))
    ax.text(x + 8, ly, "signed absence", fontsize=XS, color=INK2, va="center")
    products = {s["product"] for s in shown}
    NUMBERS["berlin"] = {"cell": b["cell"], "facts": len(shown), "products": len(products),
                         "absences": sum(s["kind"] == "absence" for s in shown), "scene": meta, "rows": shown}
    check_text(fig, "eo_berlin")
    save(fig, "eo_berlin")


# ---- 4b. how emem encodes memory: 43 slots, 1792 dims, provenance classes ----
def fig_encoding(w=345, h=150):
    d = json.load(open(V12 / "data/v1_bands_2026-09-30.json"))
    bands = sorted(d["bands"], key=lambda x: x["offset"])
    total = d["total_dims"]
    assert sum(x["dims"] for x in bands) == total == 1792
    fig = fig_mm(w, h)
    ax = mm_axes(fig, w, h)
    x0, x1, y0, bh = 2, w - 2, 12, 16
    sc = (x1 - x0) / total
    enc = [x for x in bands if x["family"] == "foundation" and x["provenance_class"] == "model_output"]
    enc_dims = sum(x["dims"] for x in enc)
    for x in bands:
        c = CLS[x["provenance_class"]]
        is_enc = x in enc
        ax.add_patch(Rectangle((x0 + x["offset"] * sc, y0), x["dims"] * sc, bh, fc=c, ec="white", lw=0.6,
                               hatch="////" if is_enc else None, alpha=0.55 if is_enc else 1.0))
    for x in enc:   # the strike: the same red line as the title
        ax.plot([x0 + x["offset"] * sc - 0.5, x0 + (x["offset"] + x["dims"]) * sc + 0.5], [y0 + bh / 2] * 2,
                color="#E5484D", lw=3.2, solid_capstyle="butt")
    ax.text(x0, y0 - 2.5, f"one cell = {len(bands)} slots, {total:,} dimensions (live ontology, bands_cid {d['bands_cid'][:8]}\u2026)",
            fontsize=S, color=INK, va="bottom")
    ax.text(x0, y0 + bh + 3, f"foundation-model encoder slots: {enc_dims:,} of {total:,} dimensions, struck", fontsize=XS,
            color="#C0282D", va="top")
    # the ladder
    counts = {}
    for x in bands:
        counts[x["provenance_class"]] = counts.get(x["provenance_class"], 0) + 1
    ladder = [("direct_sensor", "the sensor product itself: re-read the source"),
              ("deterministic_index", "a fixed formula: recompute it bit for bit"),
              ("model_output", "a signed model checkpoint"),
              ("human_curated", "the attester who drew it"),
              ("unclassified", "nothing: it fails closed, lowest rank")]
    ty, rh = 50, 12.9
    ax.text(x0, ty - 3, "class", fontsize=XS, color=MUTED, va="bottom")
    ax.text(x0 + 88, ty - 3, "slots", fontsize=XS, color=MUTED, va="bottom")
    ax.text(x0 + 142, ty - 3, "what a verifier leans on", fontsize=XS, color=MUTED, va="bottom")
    ax.plot([x0, x1], [ty - 1.5, ty - 1.5], color=RULE, lw=1)
    for i, (c, lean) in enumerate(ladder):
        yc = ty + rh * (i + 0.5)
        ax.add_patch(Rectangle((x0, yc - 3.5), 7, 7, fc=CLS[c], ec="none"))
        ax.text(x0 + 10, yc, CLS_LABEL[c], fontsize=S, fontweight=600, color=INK, va="center")
        n = counts.get(c, 0)
        ax.add_patch(Rectangle((x0 + 88, yc - 3), n * 1.6, 6, fc=CLS[c], ec="none", alpha=0.85))
        ax.text(x0 + 88 + n * 1.6 + 2, yc, str(n), fontsize=S, color=INK, va="center", fontweight=600)
        ax.text(x0 + 142, yc, lean, fontsize=S, color=INK2, va="center")
    ax.text(x0, ty + rh * 5 + 5, "Two more classes are defined for fits and devices: estimator (re-run from signed inputs)",
            fontsize=XS, color=INK2, va="center")
    ax.text(x0, ty + rh * 5 + 12, "and attested execution (a reading bound inside a verified device trace).",
            fontsize=XS, color=INK2, va="center")
    NUMBERS["encoding"] = {"slots": len(bands), "dims": total, "bands_cid": d["bands_cid"], "class_slots": counts,
                           "encoder_dims": enc_dims, "encoders": [x["key"] for x in enc]}
    check_text(fig, "encoding")
    save(fig, "encoding")


# ---- 5a. Keylong: two seasons, three satellites ----
def fig_keylong(w=392, h=124):
    k = json.load(open(V12 / "data/case_keylong_ndvi.json"))
    rows = [r for r in k["rows"] if r["observed_at"] >= "2025-01-01"]
    sat = lambda r: r["platform"][-1]          # S2A / S2B / S2C, from the scene id of each signed fact
    ts = lambda r: datetime.fromisoformat(r["observed_at"].replace("Z", "+00:00"))
    rows.sort(key=ts)
    fig = fig_mm(w, h)
    ax = fig.add_axes([0.075, 0.15, 0.915, 0.70])
    ax.plot([ts(r) for r in rows], [r["value"] for r in rows], color="#B9B9B2", lw=1.2, zorder=1)
    style = {"A": ("o", "#56B4E9"), "B": ("s", BLUE), "C": ("^", "#0B8A6B")}
    counts = {}
    for s_, (mk, col) in style.items():
        pts = [r for r in rows if sat(r) == s_]
        counts[s_] = len(pts)
        ax.scatter([ts(r) for r in pts], [r["value"] for r in pts], marker=mk, s=70, color=col, ec="white", lw=0.8,
                   zorder=3, label=f"Sentinel-2{s_} ({len(pts)})")
    assert sum(counts.values()) == len(rows), (counts, len(rows))
    peaks = []
    for yr in ("2025", "2026"):
        pk = max((r for r in rows if r["observed_at"].startswith(yr)), key=lambda r: r["value"])
        peaks.append(pk)
        ax.annotate(f"{pk['value']:.2f}  {fmt_date(pk['observed_at'])}", (ts(pk), pk["value"]),
                    xytext=(0, 12), textcoords="offset points", ha="center", fontsize=XS, color=INK)
    rec = next(r for r in rows if r["fact_cid"].startswith("oj5cecci"))
    ax.scatter([ts(rec)], [rec["value"]], s=380, facecolor="none", ec=AMB, lw=2.6, zorder=4)
    ax.annotate(f"the record in section 2: {rec['value']:.4f}, {fmt_date(rec['observed_at'])}", (ts(rec), rec["value"]),
                xytext=(-12, -58), textcoords="offset points", ha="right", fontsize=XS, color=AMB,
                arrowprops=dict(arrowstyle="-", color=AMB, lw=1.4))
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_ylabel("NDVI, Sentinel-2 L2A", fontsize=S)
    ax.set_ylim(-0.12, 1.02)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax.set_xlim(datetime(2024, 11, 20, tzinfo=timezone.utc), datetime(2026, 10, 25, tzinfo=timezone.utc))
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 0.995), frameon=False, fontsize=XS, ncol=3, handletextpad=0.3,
              columnspacing=1.2)
    # chip inset: the scene behind the R1 record, served by emem for this cell
    meta = scene_meta(k["cell"])
    ia = fig.add_axes([0.083, 0.50, 0.095, 0.30])
    ia.imshow(plt.imread(V12 / "data" / f"scene_{k['cell']}.png"), interpolation="lanczos")
    ia.plot([128], [128], marker="s", ms=7, mfc="none", mec="#FFD400", mew=2)
    ia.set_xticks([]); ia.set_yticks([])
    for sp in ia.spines.values():
        sp.set_color(INK2)
    NUMBERS["keylong"] = {"cell": k["cell"], "n_2025_2026": len(rows), "by_satellite": counts, "n_all": len(k["rows"]),
                          "peaks": [(p["value"], p["observed_at"], p["fact_cid"][:8]) for p in peaks],
                          "record": (rec["value"], rec["observed_at"], rec["fact_cid"]), "chip": meta}
    check_text(fig, "eo_keylong")
    save(fig, "eo_keylong")


# ---- 5b. Rondonia: EUDR check on a 10 x 10 grid ----
def fig_rondonia(w=392, h=124):
    r = json.load(open(V12 / "data/case_rondonia_eudr.json"))
    G = np.full((10, 10), "", dtype=object)
    bio = np.full((10, 10), np.nan)
    ly = np.zeros((10, 10), dtype=int)
    for c in r["rows"]:
        G[c["row"], c["col"]] = c["eudr_category"]
        bio[c["row"], c["col"]] = c["esa_cci_biomass.agb_t_per_ha_2022"]
        ly[c["row"], c["col"]] = c["hansen.loss_year"]
    cats = sorted(set(G.ravel()))
    colmap = {"forest_2020_no_later_loss": "#1B7A3A", "eudr_flag_forest_2020_loss_after_2020": "#D95F02", "cleared_2001_2020": "#E8C77A",
              "not_forest_2020_no_hansen_loss": "#DADAD4"}
    colmap["loss_after_2020_on_gfc2020_non_forest"] = "#F2A774"
    other = ["loss_after_2020_on_gfc2020_non_forest"]
    assert set(cats) <= set(colmap), cats
    labels = {"forest_2020_no_later_loss": "forest in 2020, no later loss", "eudr_flag_forest_2020_loss_after_2020": "forest in 2020, loss after 2020",
              "cleared_2001_2020": "cleared 2001 to 2020", "not_forest_2020_no_hansen_loss": "not forest in 2020"}
    labels["loss_after_2020_on_gfc2020_non_forest"] = "loss after 2020, maps disagree"
    fig = fig_mm(w, h)
    cell = 6.5
    gx0, gy0 = 4, 16
    ax = mm_axes(fig, w, h)
    ax.text(gx0, gy0 - 4, "EUDR check per cell", fontsize=S, color=INK, fontweight=600, va="bottom")
    gx1 = gx0 + 10 * cell + 16
    ax.text(gx1, gy0 - 4, "ESA CCI biomass 2022, t/ha", fontsize=S, color=INK, fontweight=600, va="bottom")
    cmap = plt.get_cmap("YlGn")
    flagged = [(i, j) for i in range(10) for j in range(10) if G[i, j] == "eudr_flag_forest_2020_loss_after_2020"]
    for i in range(10):
        for j in range(10):
            ax.add_patch(Rectangle((gx0 + j * cell, gy0 + i * cell), cell - 0.6, cell - 0.6, fc=colmap[G[i, j]], ec="none"))
            if G[i, j] in ("eudr_flag_forest_2020_loss_after_2020",) or G[i, j] in other:
                ax.text(gx0 + j * cell + cell / 2 - 0.3, gy0 + i * cell + cell / 2 - 0.3, f"{ly[i, j] % 100:02d}",
                        ha="center", va="center", fontsize=XS, color="white", fontweight=700)
            v = bio[i, j]
            ax.add_patch(Rectangle((gx1 + j * cell, gy0 + i * cell), cell - 0.6, cell - 0.6,
                                   fc=cmap(min(v, 300) / 300) if v == v else "#EEE", ec="none"))
    for i, j in flagged:
        ax.add_patch(Rectangle((gx1 + j * cell - 0.4, gy0 + i * cell - 0.4), cell + 0.2, cell + 0.2, fill=False,
                               ec="#D95F02", lw=2.6))
    # colour bar for biomass
    cb_y = gy0 + 10 * cell + 5
    for t in range(60):
        ax.add_patch(Rectangle((gx1 + t * 10 * cell / 60, cb_y), 10 * cell / 60 + 0.05, 3.5, fc=cmap(t / 59), ec="none"))
    for v in (0, 150, 300):
        ax.text(gx1 + v / 300 * 10 * cell, cb_y + 5.5, str(v), fontsize=XS, color=INK2, ha="center", va="top")
    # legend column
    lx, lyy = gx1 + 10 * cell + 14, gy0 + 4
    order = ["eudr_flag_forest_2020_loss_after_2020"] + other + ["forest_2020_no_later_loss", "cleared_2001_2020", "not_forest_2020_no_hansen_loss"]
    cnt = {c: int((G == c).sum()) for c in order}
    for c in order:
        ax.add_patch(Rectangle((lx, lyy - 3), 6.5, 6.5, fc=colmap[c], ec="none"))
        ax.text(lx + 9, lyy + 0.2, f"{labels[c]}: {cnt[c]}", fontsize=XS, color=INK, va="center")
        lyy += 11
    ax.text(lx, lyy + 3, "digits: Hansen loss year, 20xx", fontsize=XS, color=MUTED, va="center")
    ax.text(lx, lyy + 11, "outline: flagged cell", fontsize=XS, color="#D95F02", va="center")
    NUMBERS["rondonia"] = {"counts": cnt, "flagged_loss_years": sorted(int(ly[i, j]) for i, j in flagged),
                           "n_cells": 100, "facts": r.get("n_facts") or len(r["rows"]) * 6, "grid": r["grid"]}
    check_text(fig, "eo_rondonia")
    save(fig, "eo_rondonia")


# ---- 5c. R4: memory through time ----
def fig_bitemporal(w=260, h=124):
    import matplotlib.dates as mdates
    import matplotlib.transforms as mtrans
    d = json.load(open(REPO / "research/repro/data/contra_bengaluru.json"))
    c = d["contradictions"][0]
    at = sorted(c["attestations"], key=lambda a: a["signed_at"])
    prov = [p["fn_key"] for p in c["providers"]]
    ts = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))

    def as_of(t):
        k = [a for a in at if ts(a["signed_at"]) <= t]
        return k[-1] if k else None

    queries = [("2026-05-01", None), ("2026-06-15", 918.0), ("2026-08-12", 915.0712280273438),
               ("2026-09-29", 915.0712280273438)]
    for q, want in queries:
        got = as_of(datetime.fromisoformat(q + "T00:00:00+00:00"))
        assert (got["value"] if got else None) == want, (q, got)
    fig = fig_mm(w, h)
    ax = fig.add_axes([0.12, 0.17, 0.86, 0.6])
    t0, t1 = datetime(2026, 4, 20, tzinfo=timezone.utc), datetime(2026, 10, 15, tzinfo=timezone.utc)
    bt = mtrans.blended_transform_factory(ax.transData, ax.transAxes)
    xs = [ts(at[0]["signed_at"])] + [ts(a["signed_at"]) for a in at[1:]] + [t1]
    ys = [a["value"] for a in at] + [at[-1]["value"]]
    ax.step(xs, ys, where="post", color=BLUE, lw=2.6, zorder=2)
    for a, pk in zip(at, prov):
        old = pk.startswith("open_meteo")
        ax.plot(ts(a["signed_at"]), a["value"], "o", ms=9, color="#A3A39C" if old else BLUE, mec="white", mew=1.2, zorder=3)
    ax.text(ts(at[0]["signed_at"]), 918.0 + 0.35, "918.0 m  GLO-90, via Open-Meteo", fontsize=XS, color=INK2, va="bottom")
    ax.text(datetime(2026, 6, 20, tzinfo=timezone.utc), 915.07 - 0.35, f"915.07 m  GLO-30 COG, signed {len(at) - 1} times",
            fontsize=XS, color=BLUE, va="top")
    for q, want in queries:
        x = datetime.fromisoformat(q + "T00:00:00+00:00")
        ax.axvline(x, color=MUTED, lw=1.0, ls=(0, (2, 2)), zorder=1)
        lab = "nothing" if want is None else (f"{want:.1f}" if want == round(want, 1) else f"{want:.2f}")
        ax.text(x, 1.2, f"as of {x:%-d %b}", transform=bt, fontsize=XS, color=INK, ha="center", va="bottom", fontweight=600)
        ax.text(x, 1.03, lab, transform=bt, fontsize=XS, color=MUTED if want is None else BLUE, ha="center", va="bottom")
    ax.set_xlim(t0, t1)
    ax.set_ylim(914.0, 919.4)
    ax.set_yticks([915, 917, 919])
    ax.spines["left"].set_bounds(915, 919)
    ax.set_ylabel("elevation, m", fontsize=XS)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(5, 7, 9)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlabel("record time, 2026", fontsize=XS)
    NUMBERS["r4"] = {"values": [a["value"] for a in at], "signed_at": [a["signed_at"] for a in at], "queries": queries}
    check_text(fig, "r4_bitemporal")
    save(fig, "r4_bitemporal")


# ---- 6. SAT-042: satellites that prove what they ran ----
def parse_sat042():
    t = (V12 / "trace/sat042_run_stdout.txt").read_text()
    body = t.split("satellite_downlink stdout (verbatim)")[1].split("end satellite_downlink stdout")[0]
    V = {"key": re.search(r"enrolled spacecraft key (\w+)", body).group(1),
         "profile": re.search(r"profile (\S+) requires (\d+) trace layers", body).groups(),
         "layers": re.search(r"\[([^\]]+)\]", body).group(1).replace(" ", "").split(","),
         "unbound_digest": re.search(r"payload digest (\w+) that is not bound", body).group(1),
         "facts": re.findall(r"(emem:fact:\S+)", body), "trace_token": re.search(r"(emem:trace:\S+)", body).group(1),
         "bundle_token": re.search(r"(emem:bundle:\S+)", body).group(1),
         "drift": [{"cell": m[0], "device": float(m[1]), "anchor": float(m[2]), "score": float(m[3]), "verdict": m[4]}
                   for m in re.findall(r"(defi\.\S+)\s+device ([\d.]+) vs anchor ([\d.]+)\s+score ([\d.]+)\s+(\w+)", body)],
         "tamper": re.search(r"tampered segment (\d+) after signing.*?reject: chain broken at seq (\d+)", body, re.S).groups(),
         "commit": re.search(r"emem commit: (\w+)", t).group(1)[:7],
         "run": re.search(r"run window \(UTC\): (\S+)", t).group(1)}
    assert len(V["facts"]) == 3 and len(V["drift"]) == 3 and len(V["layers"]) == int(V["profile"][1])
    return V


def fig_sat042(w=440, h=136):
    V = parse_sat042()
    n_layers = int(V["profile"][1])
    seg, seq = int(V["tamper"][0]), int(V["tamper"][1])
    anchor = V["drift"][0]["anchor"]
    n_cons = sum(d["verdict"] == "Consistent" for d in V["drift"])
    n_contra = sum(d["verdict"] == "Contradicted" for d in V["drift"])
    short = lambda tok: tok.rsplit(":", 1)[0] + ":" + tok.rsplit(":", 1)[1][:6] + "\u2026"
    fig = fig_mm(w, h)
    ax = mm_axes(fig, w, h)
    steps = [("Enrol", "ENROLLED", BLUE, V["profile"][0], f"{n_layers} layers required"),
             ("Write, no trace", "REFUSED", BAD, "no execution trace", "presented"),
             ("Capture the pass", "SIGNED", BLUE, f"{n_layers} layers chained", f"{len(V['facts'])} NDVI payloads bound"),
             ("Smuggle a 4th fact", "REFUSED", BAD, "digest " + V["unbound_digest"][:6] + "\u2026", "not in the trace"),
             ("Honest batch", "ADMITTED", BLUE, f"{len(V['facts'])} facts, 1 trace", short(V["trace_token"])),
             ("Score vs anchor", "SCORED", AMB, f"{n_cons} consistent", f"{n_contra} contradicted"),
             ("Rewrite one log", "CAUGHT", BAD, f"segment {seg} edited", f"chain broken at seq {seq}")]
    sw = (w - 72) / 6
    ax.plot([36, w - 36], [9, 9], color=RULE, lw=4, zorder=0, solid_capstyle="round")
    for i, (what, verdict, col, l1, l2) in enumerate(steps):
        x = 36 + sw * i
        ax.add_patch(plt.Circle((x, 9), 6.2, color=col, zorder=2))
        ax.text(x, 9.2, str(i + 1), ha="center", va="center", color="white", fontsize=L, fontweight=700, zorder=3)
        ax.text(x, 21, what, ha="center", va="center", color=INK, fontsize=L - 1, fontweight=600)
        fc = {BLUE: BLUES, BAD: BADS, AMB: AMBS}[col]
        ax.add_patch(FancyBboxPatch((x - 24, 26.5), 48, 8.5, boxstyle="round,pad=0,rounding_size=1.5", fc=fc, ec=col, lw=1.8))
        ax.text(x, 30.9, verdict, ha="center", va="center", color=col, fontsize=XS + 1, fontweight=700)
        for j, line in enumerate((l1, l2)):
            mono = line.startswith(("orbital", "emem:", "digest"))
            ax.text(x, 41.5 + j * 7, line, ha="center", va="center", color=INK2, fontsize=XS, family=MONO if mono else SANS)
    # b: the chain of captured layers, one segment rewritten
    by0 = 64
    ax.text(0, by0 - 3, f"The trace chains {n_layers} captured layers and signs each payload digest", fontsize=S, color=INK,
            va="bottom", fontweight=600)
    bw, bh, bg = 29, 15, 3.4
    names = {"SensorBus": "sensor bus"}
    for k_, lay in enumerate(V["layers"]):
        x = k_ * (bw + bg)
        bad = k_ == seg
        ax.add_patch(FancyBboxPatch((x, by0 + 5), bw, bh, boxstyle="round,pad=0,rounding_size=1.2",
                                    fc=BADS if bad else BLUES, ec=BAD if bad else BLUE, lw=2.2 if bad else 1.3))
        ax.text(x + bw / 2, by0 + 10.5, names.get(lay, lay.lower()), ha="center", va="center", fontsize=XS, color=INK)
        ax.text(x + bw / 2, by0 + 16.5, f"seq {k_}", ha="center", va="center", fontsize=XS, color=BAD if bad else INK2, family=MONO)
        if k_ < len(V["layers"]) - 1:
            broken = k_ + 1 == seq
            ax.annotate("", xy=(x + bw + bg, by0 + 5 + bh / 2), xytext=(x + bw, by0 + 5 + bh / 2),
                        arrowprops=dict(arrowstyle="-|>", color=BAD if broken else INK2, lw=2 if broken else 1.1,
                                        mutation_scale=10))
    xb = seg * (bw + bg)
    ax.text(xb, by0 + 27, f"rewritten after signing; the verifier reports: chain broken at seq {seq}", ha="left",
            va="center", fontsize=XS, color=BAD, fontweight=600)
    oy = by0 + 36
    for k_, d_ in enumerate(V["drift"]):
        x = k_ * 64
        ax.add_patch(FancyBboxPatch((x, oy), 60, 10, boxstyle="round,pad=0,rounding_size=1.2", fc="white", ec=BLUE, lw=1.3))
        ax.text(x + 30, oy + 5, f"NDVI {d_['device']:.4f}", ha="center", va="center", fontsize=XS, color=INK, family=MONO)
    ax.add_patch(FancyBboxPatch((3 * 64, oy), 60, 10, boxstyle="round,pad=0,rounding_size=1.2", fc=BADS, ec=BAD, lw=1.3, ls="--"))
    ax.text(3 * 64 + 30, oy + 5, "4th fact: unbound", ha="center", va="center", fontsize=XS, color=BAD)
    ax.text(0, oy + 17, "signed payload digests, bound in the trace", fontsize=XS, color=INK2, va="center")
    # c: drift anchor
    cx0, cx1 = 300, w - 4
    ax.text(cx0 - 40, by0, "An open-archive anchor scores each claim", fontsize=S, color=INK, va="bottom", fontweight=600)
    zy0, zy1 = by0 + 12, by0 + 52
    X = lambda v: cx0 + v * (cx1 - cx0)
    for a_, b_, fc, lab, col in ((0, .5, BLUES, "consistent", BLUE), (.5, .75, AMBS, "tension", AMB), (.75, 1, BADS, "contradicted", BAD)):
        ax.add_patch(Rectangle((X(a_), zy0), X(b_) - X(a_), zy1 - zy0, fc=fc, ec="none"))
        ax.text((X(a_) + X(b_)) / 2, zy0 - 1.5, lab, ha="center", va="bottom", fontsize=XS, color=col)
    for i, d_ in enumerate(V["drift"]):
        yy = zy0 + 7 + i * 13
        col = BAD if d_["verdict"] == "Contradicted" else BLUE
        ax.plot([X(0), X(d_["score"])], [yy, yy], color=col, lw=2.4)
        ax.plot([X(d_["score"])], [yy], "o", ms=10, color=col)
        ax.text(X(0) - 2, yy, f"{d_['device']:.4f}", ha="right", va="center", fontsize=XS, color=INK, family=MONO)
        ax.text(X(d_["score"]) + (2.5 if d_["score"] < 0.8 else -2.5), yy - 4.5, f"{d_['score']:.2f}",
                ha="left" if d_["score"] < 0.8 else "right", va="center", fontsize=XS, color=col, fontweight=700)
    ax.text(cx0 - 40, zy1 + 6, f"device NDVI vs anchor {anchor:.4f} \u00b1 0.02", fontsize=XS, color=INK2, va="center")
    NUMBERS["sat042"] = V
    check_text(fig, "sat042")
    save(fig, "sat042")


def qr_codes():
    """QR payloads live in fig/v12/qr_*.txt; the SVGs are regenerated from them."""
    import qrcode
    import qrcode.image.svg
    payloads = {"qr_try": "https://emem.dev/verify",
                "qr_repro": "https://github.com/Vortx-AI/esa_poster/tree/main/research/repro/v12"}
    for name, url in payloads.items():
        (OUT / f"{name}.txt").write_text(url + "\n")
        img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, border=0,
                          error_correction=qrcode.constants.ERROR_CORRECT_M)
        img.save(str(OUT / f"{name}.svg"))


if __name__ == "__main__":
    # sizes are the board slots in mm (width, height); poster.v12.html places each SVG 1:1
    fig_failure(372, 70)
    fig_mutation(468, 182)
    fig_berlin(436, 210)
    fig_encoding(349, 140)
    fig_keylong(392, 102)
    fig_rondonia(392, 102)
    fig_bitemporal(317, 112)
    fig_sat042(440, 130)
    qr_codes()
    json.dump(NUMBERS, open(OUT / "figure_numbers.json", "w"), indent=1, default=str)
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
