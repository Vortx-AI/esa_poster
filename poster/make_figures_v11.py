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
    """R2: after a shared summary, agreement rises while correctness falls (pre-registered, §17)."""
    fig, a = plt.subplots(figsize=(10.2, 2.4))
    h = 0.4
    for i, (lab, c, n, ag, npair) in enumerate(COMPACTION):
        pc, pa = c / n, ag / npair
        a.barh(i + h / 2, pa, h, color=AMBER)
        a.barh(i - h / 2, max(pc, 0.004), h, color=INK)
        a.text(pa + 0.012, i + h / 2, f"{ag}/{npair} pairs agree", va="center", fontsize=TICK - 2, color=AMBER)
        a.text(max(pc, 0.004) + 0.012, i - h / 2, f"{c}/{n} answers correct", va="center", fontsize=TICK - 2,
               color=INK, fontweight=600 if c == 0 else 400)
    a.set_yticks(range(len(COMPACTION)), [r[0] for r in COMPACTION])
    a.set_xlim(0, 1.42)
    a.set_xticks([0, .5, 1], ["0", "50 %", "100 %"])
    a.spines["bottom"].set_bounds(0, 1)
    a.invert_yaxis()
    a.tick_params(axis="y", length=0)
    fig.subplots_adjust(left=0.2, right=0.985, top=0.985, bottom=0.155)
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
    fig, axs = plt.subplots(1, 2, figsize=(10.2, 4.75))
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


def fig_mutation():
    """R1: 17 mutations x 9 verification depths, from research/repro/v11/out/mutation_matrix.json."""
    import json
    from matplotlib.patches import Rectangle, Circle
    d = json.load(open(HERE.parent / "research/repro/v11/out/mutation_matrix.json"))
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
        "M13": "forged and signed by own key", "M14": "signer: value disagrees with DNs",
        "M15": "signer: DNs of the pixel 10 m south", "M16": "signer: second version, not logged",
        "M17": "same bytes, a different entity"}
    groups = [("G0",), ("M1", "M2", "M3"), ("M4", "M5", "M6", "M7"), ("M8", "M9", "M10", "M11", "M12", "M13"),
              ("M14", "M15", "M16"), ("M17",)]
    gnames = ["", "paraphrase, relay", "misbinding", "forgery, no key", "the trusted signer errs", "out of scope"]
    order = [m for g in groups for m in g]
    real = {m["id"] for m in muts if m["real_case"]}
    RED, PALE, GREY = "#B3261E", "#CFDBF6", "#E4E4DE"
    rowh, gap = 1.0, 1.05
    ys, y, gy = {}, 0.0, []
    for gi, g in enumerate(groups):
        if gi:
            y += gap
        gy.append(y)
        for m in g:
            ys[m] = y
            y += rowh
    ymax = y
    fig, ax = plt.subplots(figsize=(10.83, 5.6))
    LX = -0.3
    for m in order:
        for j, (lv, _) in enumerate(cols):
            r = by[(m, lv)]
            o = r["outcome"]
            fc = {"acted on corrupted evidence": RED, "refused": BLUE, "unaffected": PALE,
                  "acted correctly": GREY, "n/a": "#FFFFFF"}[o]
            ax.add_patch(Rectangle((j + 0.05, ys[m] + 0.07), 0.9, rowh - 0.14, fc=fc, ec="none"))
            if o == "refused":
                ax.text(j + 0.5, ys[m] + rowh / 2, r["failed_check"], ha="center", va="center",
                        fontsize=TICK - 3, color="#FFFFFF", fontweight=600)
            if o == "n/a":
                ax.text(j + 0.5, ys[m] + rowh / 2, "n/a", ha="center", va="center", fontsize=TICK - 5, color=MUTED)
        ax.text(LX, ys[m] + rowh / 2, short[m], ha="right", va="center", fontsize=TICK - 2,
                color=INK if m != "G0" else INK2)
        ax.text(-6.05, ys[m] + rowh / 2, m, ha="left", va="center", fontsize=TICK - 2, fontweight=600,
                color=AMBER if m in real else MUTED)
    for gi, name in enumerate(gnames):
        if name:
            ax.text(-6.05, gy[gi] - 0.06, name.upper(), ha="left", va="bottom", fontsize=TICK - 5, color=MUTED,
                    fontweight=600)
    for j, (lv, name) in enumerate(cols):
        ax.text(j + 0.5, -0.45, lv, ha="center", va="bottom", fontsize=TICK, fontweight=600,
                color=BLUE if lv == "I" else INK)
        ax.text(j + 0.5, -1.35, name, ha="center", va="bottom", fontsize=TICK - 5, color=INK2)
    sm = d["summary"]
    ax.text(LX, ymax + 0.8, "acted on corrupted evidence", ha="right", va="center", fontsize=TICK - 2,
            color=RED, fontweight=600)
    for j, (lv, _) in enumerate(cols):
        ax.text(j + 0.5, ymax + 0.8, f"{sm[lv]['false_accepts']}/{sm[lv]['applicable']}", ha="center",
                va="center", fontsize=TICK - 3, color=RED if sm[lv]["false_accepts"] else BLUE, fontweight=600)
    ax.annotate("", xy=(9.0, -2.55), xytext=(3.05, -2.55), arrowprops=dict(arrowstyle="->", color=INK2, lw=1.0),
                annotation_clip=False)
    ax.text(3.05, -2.75, "emem's checks, one more per column", ha="left", va="bottom", fontsize=TICK - 5, color=INK2)
    ax.set_xlim(-6.1, 9.05)
    ax.set_ylim(ymax + 1.35, -3.75)
    ax.axis("off")
    from matplotlib.patches import Patch
    hs = [Patch(fc=RED, label="B acts on corrupted evidence"), Patch(fc=BLUE, label="refused; letter = the check"),
          Patch(fc=PALE, label="unaffected"), Patch(fc=AMBER, label="amber id: seen in production")]
    fig.legend(handles=hs, loc="lower left", ncol=4, frameon=False, fontsize=TICK - 4, bbox_to_anchor=(0.0, -0.005),
               handlelength=1.0, columnspacing=1.1)
    fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.07)
    bad, out = overlaps(fig)
    assert not out, out
    fig.savefig(OUT / "r1_mutation.svg", transparent=True)
    plt.close(fig)


def fig_bitemporal():
    """R4: one Bengaluru key through record time. Data: research/repro/data/contra_bengaluru.json.

    The as-of answers are computed with the protocol's rule (latest signed_at <= t) and must equal the
    live replay recorded in research/should_do/09_INVENTION_REGISTER.md (verify_bitemporal.py).
    """
    import json
    from datetime import datetime, timezone
    import matplotlib.dates as mdates
    d = json.load(open(HERE.parent / "research/repro/data/contra_bengaluru.json"))
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
    fig, ax = plt.subplots(figsize=(9.55, 4.1))
    import matplotlib.transforms as mtrans
    t0, t1 = datetime(2026, 4, 24, tzinfo=timezone.utc), datetime(2026, 10, 12, tzinfo=timezone.utc)
    bt = mtrans.blended_transform_factory(ax.transData, ax.transAxes)
    # the answer "as of t", a step function of record time
    xs = [ts(at[0]["signed_at"])] + [ts(a["signed_at"]) for a in at[1:]] + [t1]
    ys = [a["value"] for a in at] + [at[-1]["value"]]
    ax.step(xs, ys, where="post", color=BLUE, lw=2.4, zorder=2)
    for a, pk in zip(at, prov):
        old = pk.startswith("open_meteo")
        ax.plot(ts(a["signed_at"]), a["value"], "o", ms=9, color=GREY if old else BLUE, mec="#FFFFFF", mew=1.2, zorder=3)
    ax.text(ts(at[0]["signed_at"]), 918.0 + 0.32, "918.0 m  Copernicus DEM 90 m, via Open-Meteo", fontsize=TICK - 1,
            color=INK2, va="bottom")
    ax.text(datetime(2026, 6, 1, tzinfo=timezone.utc), 915.07 - 0.3, f"915.07 m  Copernicus DEM 30 m COG, signed {len(at) - 1} times",
            fontsize=TICK - 1, color=BLUE, va="top")
    for q, want in queries:
        x = datetime.fromisoformat(q + "T00:00:00+00:00")
        ax.axvline(x, color=MUTED, lw=1.0, ls=(0, (2, 2)), zorder=1)
        lab = "nothing yet" if want is None else (f"{want:.1f} m" if want == round(want, 1) else f"{want:.2f} m")
        ax.text(x, 1.10, f"as of {x:%-d %b}", transform=bt, fontsize=TICK - 2, color=INK, ha="center", va="bottom", fontweight=600)
        ax.text(x, 1.01, lab, transform=bt, fontsize=TICK - 2, color=MUTED if want is None else BLUE, ha="center", va="bottom")
    ax.set_xlim(t0, t1)
    ax.set_ylim(914.2, 919.2)
    ax.set_yticks([915, 916, 917, 918, 919])
    ax.spines["left"].set_bounds(915, 919)
    ax.set_ylabel("elevation, m", fontsize=TICK - 1)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlabel("record time (signed_at), 2026", fontsize=TICK - 1)
    fig.subplots_adjust(left=0.085, right=0.985, top=0.83, bottom=0.17)
    bad, out = overlaps(fig)
    assert not bad and not out, (bad, out)
    fig.savefig(OUT / "r4_bitemporal.svg", transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    fig_agreement()
    fig_pixel_audit()
    fig_mutation()
    fig_bitemporal()
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
