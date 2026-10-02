"""F15 · How a satellite could prove what it ran (193.5 x 118 mm, right column).

SAT-042 is a scripted pass in emem's test harness, not a spacecraft; run on 30 Sep 2026. Every printed value is
parsed from the captured stdout of that run, or read from the audit beside it (readers in sat042_data.py):
  research/repro/v12/trace/sat042_run_stdout.txt   the verbatim run (emem 04b40c5, 2026-09-30T19:14:15Z)
  research/repro/v12/trace/trace_truth.md          anchor (0.6402, 0.02), tampered segment 2, 'not a spacecraft'
  research/repro/v10/algorithms.md §15             z = |x − anchor| / 3σ, score = z/(1+z); verdict thresholds 0.5, 0.75;
                                                   the gate binds the value digest only (band, cell, tslot unchecked)
  research/v13/00_v11_review_findings.md F08, F09, F12   three refusals; the drift score is scored after admission
(a) the seven steps, (b) the 8-layer trace strip with the rewritten segment, (c) the drift-anchor score strip.
The kicker the board prints is in the labels file: "Extending verification from observations to execution".

    python poster/figs_v13/f15_sat042.py
"""
import json
import os
import re
import sys

from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, MONO, OUT, ROOT, fig_mm, save  # noqa: E402

W, H = 193.5, 118.0
PTMM = 25.4 / 72
NAME = "f15_sat042"

# ------------------------------------------------------------------ parse the run (shared with F15b: sat042_data.py)
from sat042_data import ANCHOR, KICKER, N_CONS, N_CONTRA, SEG, SEQ, SIGMA, V  # noqa: E402

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


def box(x, y, w, h, fc, ec="none", lw=0.0, r=0.8, ls="-", z=3):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw / PTMM, ls=ls, zorder=z)
    ax.add_patch(p)
    return p


short = lambda tok, n=6: tok.rsplit(":", 1)[1][:n] + "…"

# ------------------------------------------------------------------ headline strip (the scope, first)
ax.add_patch(Rectangle((0, 0), W, 11.6, fc=C["oos_bg"], ec="none", zorder=1))
T(1.6, 3.2, "SAT-042 is a scripted pass in emem's test harness,", 14, weight=600, claim="A15.headline")
T(1.6, 8.4, "not a spacecraft; run on 30 Sep 2026.", 14, weight=600, claim="A15.headline")
T(W - 1.6, 3.2, f"emem {V['commit']}, deterministic:", 14, color=C["ink2"], ha="right", claim="A15.headline")
T(W - 1.6, 8.4, "fixed key, clocks, digests, anchor", 14, color=C["ink2"], ha="right", claim="A15.headline")
assert V["run"][:10] == "2026-09-30"

# ------------------------------------------------------------------ (a) seven steps
OK, BAD, AMB = ("emem", "emem_tint"), ("harm_text", "harm_tint"), ("incident_text", "na")
STEPS = [
    ("Enrol", "ENROLLED", OK, f"{V['profile'][0]} enrolled; {V['profile'][1]} layers required"),
    ("Write, no trace", "REFUSED", BAD, "no OS execution trace was presented"),
    ("Capture the pass", "SIGNED", OK, f"{len(V['layers'])} layers chained; {len(V['facts'])} NDVI payload digests bound"),
    ("Smuggle a 4th fact", "REFUSED", BAD, f"digest {V['unbound_digest'][:6]}… is not among the trace's outputs"),
    ("Honest batch", "ADMITTED", OK, f"{len(V['facts'])} facts under 1 trace, {short(V['trace_token'])}, 1 bundle"),
    ("Score vs anchor", "SCORED", AMB, f"{N_CONS} consistent, {N_CONTRA} contradicted; scored after admission"),
    ("Rewrite one log", "CAUGHT", BAD, f"segment {SEG} edited after signing: chain broken at seq {SEQ}"),
]
ay = 14.2
T(0, ay, "a", 17, weight=700)
T(4.6, ay, "one scripted pass: two writes refused, one rewrite caught", 14, color=C["ink2"], claim=None)
XS, XV, XD = 6.4, 49.5, 76.0
VW = 24.5
DW = []
y = ay + 6.0
for i, (what, verdict, (tc, bg), detail) in enumerate(STEPS):
    yy = y + i * 5.1
    ax.add_patch(Circle((2.4, yy), 2.3, fc=C[tc] if tc != "incident_text" else C["incident"], ec="none", zorder=3))
    T(2.4, yy + 0.1, str(i + 1), 14, weight=700, color="white", ha="center", claim="A15.steps")
    T(XS, yy, what, 14, weight=500, claim="A15.steps")
    box(XV, yy - 2.6, VW, 5.2, C[bg], r=1.0)
    T(XV + VW / 2, yy, verdict, 14, weight=700, color=C[tc], ha="center", claim="A15.steps")
    t = T(XD, yy, detail, 14, color=C["ink2"], claim="A15.steps")
    DW.append((detail, round(wmm(t), 1)))
    assert wmm(t) <= W - XD, (detail, wmm(t))
a_end = y + 6 * 5.1 + 2.55
print("step details mm", DW)

# ------------------------------------------------------------------ (b) the trace strip
by = a_end + 3.4
T(0, by, "b", 17, weight=700)
T(4.6, by, f"the trace: {len(V['layers'])} layers, each log digest chained to the previous", 14, color=C["ink2"], claim="A15.layers")
GAP = 1.2
BW = (W - 7 * GAP) / 8
BH = 11.0
by0 = by + 3.6
names = {"SensorBus": "sensor bus"}
for k, lay in enumerate(V["layers"]):
    x = k * (BW + GAP)
    bad = k == SEG
    box(x, by0, BW, BH, C["harm_tint"] if bad else C["emem_tint"], ec=C["harm"] if bad else "none", lw=1.2 if bad else 0, r=1.0)
    T(x + BW / 2, by0 + 2.7, names.get(lay, lay.lower()), 14, ha="center", color=C["harm_text"] if bad else C["ink"], claim=None)
    T(x + BW / 2, by0 + 8.3, f"seq {k}", 14, ha="center", family=MONO, color=C["harm_text"] if bad else C["ink2"], claim="A15.layers")
    if k < 7:
        broken = k + 1 == SEQ
        xa, xb = x + BW, x + BW + GAP
        ax.plot([xa, xb], [by0 + BH / 2] * 2, color=C["harm"] if broken else C["ink2"], lw=(1.4 if broken else 0.8) / PTMM, zorder=4)
        if broken:
            ax.add_patch(Circle(((xa + xb) / 2, by0 + 8.3), 2.2, fc="white", ec=C["harm"], lw=0.9 / PTMM, zorder=5))
            T((xa + xb) / 2, by0 + 8.4, "×", 14, weight=700, color=C["harm"], ha="center", claim=None, z=6)
ly = by0 + BH + 3.0
T(SEG * (BW + GAP), ly, f"seq {SEG} rewritten after signing; the verifier: chain broken at seq {SEQ}", 14,
  color=C["harm_text"], claim="A15.layers")
# ------------------------------------------------------------------ (c) drift anchor
cy = ly + 5.2
T(0, cy, "c", 17, weight=700)
T(4.6, cy, f"drift anchor {ANCHOR:.4f} \u00b1 {SIGMA} (1\u03c3): scored after admission, not a gate", 14, color=C["ink2"], claim="A15.formula")
SX0, SX1 = 42.0, W
sy0, sy1 = cy + 3.2, cy + 3.2 + 18.9
X = lambda v: SX0 + v * (SX1 - SX0)
for a_, b_, fc, lab, col in ((0, .5, "emem_tint", "consistent", "emem"), (.5, .75, "na", "tension", "incident_text"),
                             (.75, 1, "harm_tint", "contradicted", "harm_text")):
    ax.add_patch(Rectangle((X(a_), sy0), X(b_) - X(a_), sy1 - sy0, fc=C[fc], ec="none", zorder=1.5))
    T((X(a_) + X(b_)) / 2, sy0 + 2.4, lab, 14, color=C[col], ha="center", claim=None)
for v in (0.5, 0.75):
    ax.plot([X(v), X(v)], [sy0, sy1], color="white", lw=0.6 / PTMM, zorder=2.5)
for i, d in enumerate(V["drift"]):
    yy = sy0 + 6.2 + i * 5.1
    bad = d["verdict"] == "Contradicted"
    col = C["harm"] if bad else C["emem"]
    T(SX0 - 2.0, yy, f"{d['device']:.4f} \u2192 {d['score']:.2f}", 14, weight=500, ha="right",
      color=C["harm_text"] if bad else C["ink"], claim="A15.drift")
    ax.plot([X(0), X(d["score"])], [yy, yy], color=col, lw=1.2 / PTMM, zorder=3, solid_capstyle="butt")
    ax.add_patch(Circle((X(d["score"]), yy), 1.2, fc=col, ec="white", lw=0.4 / PTMM, zorder=4))
fy = sy1 + 3.0
T(0, fy, "s = z/(1+z), z = |x \u2212 anchor| / 3\u03c3; 3\u03c3 scores 0.5, 9\u03c3 scores 0.75 (emem-trace tests)",
  14, color=C["ink2"], claim="A15.formula")
T(0, fy + 5.2, "The gate binds the value digest only; band, cell and tslot are not checked.", 14, color=C["ink2"], claim="A15.scope")
T(0, fy + 10.4, "Three refusals shown; no device is enrolled under orbital.satellite.v1.", 14, color=C["ink2"], claim="A15.scope")
assert fy + 10.4 + 2.6 <= H, fy

# ------------------------------------------------------------------ labels must be covered by claims rows
CM = json.load(open(os.path.join(ROOT, "research/v13/12_claims_map_additions_F13-15.json")))
CROWS = {r["id"]: r for r in CM["rows"]}
NUM_RE = re.compile(r"(?<![\w.\-])[−+]?\d+(?:[.,]\d+)*(?!\w)")
nums = lambda s_: [m.group(0).lstrip("−+") for m in NUM_RE.finditer(s_)]
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
