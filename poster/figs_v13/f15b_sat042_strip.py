"""F15b · How a satellite could prove what it ran, as a compact strip (193.5 x 60 mm, right column panel 11, v13.2).

The full F15 (193.5 x 118 mm) did not fit the right column; this strip prints the same run in three rows:
  (a) the seven harness steps in one row of chips, each with its verdict word;
  (b) the 8-layer trace in one row, the rewritten segment marked and the broken link crossed;
  (c) the three drift-anchor scores on a tiny number line with the 0.5 / 0.75 verdict bands.
Data readers and asserts: sat042_data.py (shared with F15). Claim ids: rows A15.* of
research/v13/12_claims_map_additions_F13-15.json; the script asserts that every printed number is in its row.

    python poster/figs_v13/f15b_sat042_strip.py [--height 60]
"""
import json
import os
import re
import sys

from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, MONO, OUT, ROOT, fig_mm, save  # noqa: E402
from sat042_data import ANCHOR, KICKER, N_CONS, N_CONTRA, SEG, SEQ, SIGMA, V  # noqa: E402

W = 193.5
H = float(sys.argv[sys.argv.index("--height") + 1]) if "--height" in sys.argv else 60.0
PTMM = 25.4 / 72
NAME = "f15b_sat042_strip"

# ------------------------------------------------------------------ canvas
fig = fig_mm(W, H)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
LABELS = []


def T(x, y, s, size=14, claim=None, weight=400, color=None, family=None, ha="left", va="center", z=6, **kw):
    t = ax.text(x, y, s, fontsize=size, fontweight=weight, color=color or C["ink"], ha=ha, va=va,
                family=family or "IBM Plex Sans", zorder=z, **kw)
    LABELS.append({"text": s, "pt": size, "claim": claim})
    return t


def wmm(t):
    return t.get_window_extent(fig.canvas.get_renderer()).width / fig.dpi * 25.4


def box(x, y, w, h, fc, ec="none", lw=0.0, r=0.8, z=3):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw / PTMM, zorder=z)
    ax.add_patch(p)
    return p


# ------------------------------------------------------------------ (a) seven steps as chips
OK, BAD, AMB = ("emem", "emem_tint"), ("harm_text", "harm_tint"), ("incident_text", "na")
STEPS = [(["Enrol"], "ENROLLED", OK), (["Write,", "no trace"], "REFUSED", BAD), (["Capture", "the pass"], "SIGNED", OK),
         (["Unbound", "fact"], "REFUSED", BAD), (["Bound", "batch"], "ADMITTED", OK),
         (["Score vs", "anchor"], "SCORED", AMB), (["Rewrite", "one log"], "REFUSED", BAD)]
assert sum(v == "REFUSED" for _, v, _ in STEPS) == 3 and len(STEPS) == 7
G = 1.4
CW = (W - 6 * G) / 7
NH, VH = 11.0, 5.8                      # name plate, verdict band
ay = 0.0
for i, (name, verdict, (tc, bg)) in enumerate(STEPS):
    x = i * (CW + G)
    box(x, ay, CW, NH + VH, C["paper"], ec=C["rule"], lw=0.35, r=1.0, z=2)
    box(x, ay + NH, CW, VH, C[bg], r=1.0, z=3)
    ax.add_patch(Rectangle((x, ay + NH), CW, 1.2, fc=C[bg], ec="none", zorder=3.1))   # square the band's top edge
    for k, s in enumerate(name):
        yy = ay + NH / 2 + (k - (len(name) - 1) / 2) * 5.0
        t = T(x + CW / 2, yy, s, 14, weight=500, ha="center", claim="A15.steps")
        assert wmm(t) <= CW - 1.0, (s, wmm(t))
    t = T(x + CW / 2, ay + NH + VH / 2 + 0.1, verdict, 14, weight=700, color=C[tc], ha="center", claim="A15.steps")
    assert wmm(t) <= CW - 0.8, (verdict, wmm(t))
a_end = ay + NH + VH

# ------------------------------------------------------------------ (b) the trace strip
by = a_end + 4.9
t = T(0, by, f"{len(V['layers'])} trace layers, each log digest chained;", 14, color=C["ink2"], claim="A15.layers")
t2 = T(W, by, f"seq {SEG} rewritten after signing: broken at seq {SEQ}", 14, weight=500, color=C["harm_text"], ha="right", claim="A15.layers")
assert wmm(t) + wmm(t2) <= W - 3.0, (wmm(t), wmm(t2))
GAP = 1.2
BW = (W - 7 * GAP) / 8
BH = 11.0
by0 = by + 3.6
names = {"SensorBus": "sensor bus"}
for k, lay in enumerate(V["layers"]):
    x = k * (BW + GAP)
    bad = k == SEG
    box(x, by0, BW, BH, C["harm_tint"] if bad else C["emem_tint"], ec=C["harm"] if bad else "none", lw=1.2 if bad else 0, r=1.0)
    T(x + BW / 2, by0 + 2.9, names.get(lay, lay.lower()), 14, ha="center", color=C["harm_text"] if bad else C["ink"], claim="A15.layers")
    T(x + BW / 2, by0 + 8.2, f"seq {k}", 14, ha="center", family=MONO, color=C["harm_text"] if bad else C["ink2"], claim="A15.layers")
    if k < 7:
        broken = k + 1 == SEQ
        xa, xb = x + BW, x + BW + GAP
        ax.plot([xa, xb], [by0 + BH / 2] * 2, color=C["harm"] if broken else C["ink2"], lw=(1.4 if broken else 0.8) / PTMM, zorder=4)
        if broken:
            ax.add_patch(Circle(((xa + xb) / 2, by0 + 8.2), 2.2, fc="white", ec=C["harm"], lw=0.9 / PTMM, zorder=5))
            T((xa + xb) / 2, by0 + 8.3, "×", 14, weight=700, color=C["harm"], ha="center", claim="A15.layers", z=6)
b_end = by0 + BH

# ------------------------------------------------------------------ (c) drift anchor number line
cy = b_end + 4.9
SX0, SX1 = 66.0, W
for k, s in enumerate(("drift anchor", f"{ANCHOR:.4f} \u00b1 {SIGMA} (1\u03c3):", "scored after admission,", "not a gate")):
    t = T(0, cy - 0.8 + k * 5.2, s, 14, color=C["ink2"], claim="A15.formula")
    assert wmm(t) <= SX0 - 4.0, (s, wmm(t))
sy0, sy1 = cy - 2.6, cy + 3.0
X = lambda v: SX0 + v * (SX1 - SX0)   # noqa: E731
for a_, b_, fc, lab, col in ((0, .5, "emem_tint", "consistent", "emem"), (.5, .75, "na", "tension", "incident_text"),
                             (.75, 1, "harm_tint", "contradicted", "harm_text")):
    ax.add_patch(Rectangle((X(a_), sy0), X(b_) - X(a_), sy1 - sy0, fc=C[fc], ec="none", zorder=1.5))
    T((X(a_) + X(b_)) / 2, (sy0 + sy1) / 2 + 0.1, lab, 14, color=C[col], ha="center", claim="A15.formula")
for v in (0.5, 0.75):
    ax.plot([X(v), X(v)], [sy0, sy1 + 1.2], color=C["ink2"], lw=0.5 / PTMM, zorder=2.5)
    T(X(v), sy1 + 3.6, f"{v:g}", 14, color=C["ink2"], ha="center", family=MONO, claim="A15.formula")
ly = sy1 + 8.8                      # the number line
ax.plot([X(0), X(1)], [ly, ly], color=C["rule"], lw=0.8 / PTMM, zorder=2, solid_capstyle="butt")
for i, d in enumerate(sorted(V["drift"], key=lambda d: d["score"])):
    bad = d["verdict"] == "Contradicted"
    col = C["harm"] if bad else C["emem"]
    ax.add_patch(Circle((X(d["score"]), ly), 1.3, fc=col, ec="white", lw=0.4 / PTMM, zorder=4))
    above = i == 0                   # the two consistent scores sit 13 mm apart: label one above, one below the line
    T(X(d["score"]), ly + (-4.2 if above else 4.4), f"{d['device']:.4f} → {d['score']:.2f}", 14, weight=500,
      ha="center" if not bad else "right", color=C["harm_text"] if bad else C["ink"], family=MONO, claim="A15.drift")
assert ly + 4.4 + 2.6 <= H, (ly, H)

# ------------------------------------------------------------------ labels must be covered by claims rows
CM = json.load(open(os.path.join(ROOT, "research/v13/12_claims_map_additions_F13-15.json")))
CROWS = {r["id"]: r for r in CM["rows"]}
for e in CM.get("extend_print", []):
    CROWS[e["id"]]["print"] = list(CROWS[e["id"]]["print"]) + list(e.get("print_add", []))
NUM_RE = re.compile(r"(?<![\w.\-])[−+]?\d+(?:[.,]\d+)*(?!\w)")
nums = lambda s_: [m.group(0).lstrip("−+") for m in NUM_RE.finditer(s_)]   # noqa: E731
for L in LABELS:
    if not nums(L["text"]):
        continue
    assert L["claim"] in CROWS, f"label without a claims row: {L['text']!r}"
    own = {x for p in CROWS[L["claim"]]["print"] for x in nums(p)}
    missing = [x for x in nums(L["text"]) if x not in own]
    assert not missing, f"{L['claim']}: numbers {missing} of {L['text']!r} not in its print strings"

save(fig, NAME)
json.dump({"figure": NAME, "size_mm": [W, H], "kicker": {"text": KICKER, "claim": "A15.kicker", "role": "kicker"},
           "run": V["run"], "commit": V["commit"], "labels": LABELS},
          open(os.path.join(OUT, f"{NAME}.labels.json"), "w"), indent=1, ensure_ascii=False)
