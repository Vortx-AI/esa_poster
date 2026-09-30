"""Figures for the v11 board (invention-grade redesign).

Every number drawn here is one printed on the v10 board and traced in
research/should_do/05_EVIDENCE_AND_NUMBERS.md and the §17/§18 pointer notes
(emem docs rows at 213e273). Nothing is recomputed; the figure only draws them.

usage: python poster/make_figures_v11.py   (matplotlib; IBM Plex TTFs in poster/fonts/ttf)
"""
from pathlib import Path
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = Path(__file__).resolve().parent
OUT = HERE / "fig" / "v11"
OUT.mkdir(parents=True, exist_ok=True)
for ttf in (HERE / "fonts" / "ttf").glob("*.ttf"):
    fm.fontManager.addfont(str(ttf))

INK, INK2, MUTED, RULE = "#141414", "#46463F", "#85857E", "#D3D3CC"
BLUE, AMBER, GREY = "#1F4FD8", "#C07A00", "#A3A39C"
BASE, SMALL, TICK = 17, 15, 14  # pt, at print size (the SVG is placed 1:1)

mpl.rcParams.update({
    "font.family": "IBM Plex Sans", "font.size": BASE, "axes.titlesize": BASE,
    "axes.labelsize": SMALL, "xtick.labelsize": TICK, "ytick.labelsize": TICK,
    "axes.edgecolor": INK2, "axes.linewidth": 1.0, "xtick.color": INK2, "ytick.color": INK2,
    "svg.fonttype": "path", "axes.spines.top": False, "axes.spines.right": False,
})

# ---- R1: agreement is not evidence -------------------------------------------------
# compaction study (pre-registered; Gemma-4-12B + Qwen2.5-7B, one host): §17
COMPACTION = [  # label, correct, n_answers, agree, n_pairs
    ("full context\n(control)", 72, 72, 36, 36),
    ("shared summary,\nno pressure", 20, 72, 15, 36),
    ("shared summary,\nunder pressure", 0, 72, 3, 36),
]
# handoff study, n = 20 per arm: §18
HANDOFF = [  # label, exact, n, verifiable_by_receiver
    ("prose handoff", 2, 20, False),
    ("dense retrieval, top-5", 8, 20, False),
    ("BM25 retrieval, top-5", 20, 20, False),
    ("emem token bundle", 20, 20, True),
]


def overlaps(fig):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    tx = [(t, t.get_window_extent(r)) for t in fig.findobj(mpl.text.Text)
          if t.get_text().strip() and t.get_visible()]
    bad = [(a.get_text(), b.get_text()) for i, (a, ba) in enumerate(tx)
           for b, bb in tx[i + 1:] if ba.overlaps(bb)]
    fb = fig.bbox
    out = [t.get_text() for t, b in tx if b.x0 < fb.x0 - 1 or b.x1 > fb.x1 + 1 or b.y0 < fb.y0 - 1 or b.y1 > fb.y1 + 1]
    return bad, out


def fig_agreement():
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.2, 4.0), gridspec_kw={"width_ratios": [1.0, 1.0], "wspace": 0.74})
    # panel a: per condition, share of answers correct vs share of pairs agreeing
    y = range(len(COMPACTION))
    h = 0.36
    for i, (lab, c, n, ag, npair) in enumerate(COMPACTION):
        pc, pa = c / n, ag / npair
        a.barh(i + h / 2, pa, h, color=AMBER)
        a.barh(i - h / 2, max(pc, 0.004), h, color=INK)
        a.text(pa + 0.02, i + h / 2, f"{ag}/{npair} pairs agree", va="center", fontsize=TICK, color=AMBER)
        a.text(max(pc, 0.004) + 0.02, i - h / 2, f"{c}/{n} correct", va="center", fontsize=TICK,
               color=INK, fontweight=600 if c == 0 else 400)
    a.set_yticks(list(y), [r[0] for r in COMPACTION])
    a.set_xlim(0, 1.62)
    a.set_xticks([0, .5, 1], ["0", "50 %", "100 %"])
    a.invert_yaxis()
    a.set_title("a  After a shared summary", loc="left", fontweight=600)
    a.tick_params(axis="y", length=0)
    # panel b: exact values after a handoff
    for i, (lab, k, n, ver) in enumerate(HANDOFF):
        col = BLUE if ver else GREY
        b.barh(i, k / n, 0.62, color=col)
        note = {0: "", 1: "", 2: "  as text", 3: "  verified bytes"}[i]
        b.text(k / n + 0.02, i, f"{k}/{n}{note}", va="center", fontsize=TICK, color=BLUE if ver else INK2,
               fontweight=600 if ver else 400)
    b.set_yticks(range(len(HANDOFF)), [r[0] for r in HANDOFF])
    for t, r in zip(b.get_yticklabels(), HANDOFF):
        t.set_color(BLUE if r[3] else INK2)
        if r[3]:
            t.set_fontweight(600)
    b.set_xlim(0, 2.3)
    b.set_xticks([0, .5, 1], ["0", "50 %", "100 %"])
    b.invert_yaxis()
    b.tick_params(axis="y", length=0)
    b.set_title("b  Exact value after handoff", loc="left", fontweight=600)
    for ax in (a, b):
        ax.spines["bottom"].set_bounds(0, 1)
    fig.subplots_adjust(left=0.19, right=0.975, top=0.88, bottom=0.14)
    bad, out = overlaps(fig)
    assert not bad and not out, (bad, out)
    fig.savefig(OUT / "r1_agreement.svg", transparent=True)
    plt.close(fig)


def fig_pixel_audit():
    """R2: the 5 x 5 NDVI windows around the query point, as re-read from the COGs named in the records."""
    import json
    import numpy as np
    from matplotlib.patches import Rectangle
    pw = json.load(open(HERE.parent / "research/repro/data/v8/pixel_windows.json"))
    pre = next(v for k, v in pw.items() if k.startswith("kxjvfwpa"))
    post = next(v for k, v in pw.items() if k.startswith("oj5cecci"))
    fig, axs = plt.subplots(1, 2, figsize=(10.2, 5.25))
    for ax, w, title, sig in ((axs[0], pre, "record signed before the fix (23 Sep scene)", True),
                              (axs[1], post, "record signed after the fix (25 Sep scene)", False)):
        a = np.array(w["ndvi_5x5"])
        ax.imshow(a, cmap="Greens", vmin=0.0, vmax=1.15)
        for r in range(5):
            for c in range(5):
                ax.text(c, r + 0.24, f"{a[r, c]:.3f}", ha="center", va="center", fontsize=TICK, color=INK)
        cc, rr = w["centre_col_row"]
        oc, orr = w["window_origin_col_row"]
        ax.plot([cc - oc - .5], [rr - orr - .5], marker="o", ms=7, color=INK, mec="#FFFFFF", mew=1.0)
        ax.add_patch(Rectangle((1.5, 1.5), 1, 1, fill=False, ec=BLUE, lw=3.2))
        if sig:
            r_, c_ = w["signed_DN_location_in_window"][0]
            ax.add_patch(Rectangle((c_ - .5, r_ - .5), 1, 1, fill=False, ec="#B3261E", lw=3.2, ls="--"))
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_title(title, fontsize=SMALL, color=INK, pad=6, loc="left")
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    hs = [Line2D([], [], marker="o", ls="", ms=7, color=INK, mec="#FFFFFF", label="query point"),
          Patch(fill=False, ec=BLUE, lw=3.2, label="the pixel that contains it"),
          Patch(fill=False, ec="#B3261E", lw=3.2, ls="--", label="the pixel whose DNs emem signed")]
    fig.legend(handles=hs, loc="lower left", ncol=3, frameon=False, fontsize=TICK, bbox_to_anchor=(0.0, -0.01),
               handlelength=1.4, columnspacing=1.6)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.08, wspace=0.08)
    bad, out = overlaps(fig)
    bad = [b for b in bad if not (b[0][:1].isdigit() or b[1][:1].isdigit())]
    assert not out, out
    fig.savefig(OUT / "r2_pixel_audit.svg", transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    fig_agreement()
    fig_pixel_audit()
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
