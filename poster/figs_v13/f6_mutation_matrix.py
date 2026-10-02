"""F6 · Which check stops which corruption: the mutation matrix (396 x 196 mm, brief §E F6).

Every cell, letter, ring, tick and total is read from research/repro/v11/out/mutation_matrix.json (R1). The R5
agent-level mode switches on only when research/repro/v13/r5/results.json exists and says it is final; otherwise
the figure is labelled "deterministic receiver, no model" (brief §G gate 10).

    python poster/figs_v13/f6_mutation_matrix.py
"""
import json
import os
import sys

import matplotlib
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, MONO, OUT, ROOT, fig_mm, save  # noqa: E402

W, H = 396.0, 196.0
PTMM = 25.4 / 72
NAME = "f6_mutation_matrix"

R1 = os.path.join(ROOT, "research/repro/v11/out/mutation_matrix.json")
PROBES = os.path.join(ROOT, "research/v13/evidence/ladder/r1_t2_extra_out.json")
R5 = os.environ.get("F6_R5_RESULTS", os.path.join(ROOT, "research/repro/v13/r5/results.json"))

M = json.load(open(R1))
META = {m["id"]: m for m in M["meta"]["mutations"]}
BY = {(r["mutation"], r["level"]): r for r in M["rows"]}
SUM, LOO = M["summary"], M["leave_one_out"]
PR = json.load(open(PROBES))

# ------------------------------------------------------------------ R5 switch (gate 10)
# figure column -> R5 condition. R1 named its columns A prose, B JSON, C opaque id; R5 names them A prose, B JSON,
# C RAG, D opaque id (research/repro/v13/r5/results.md, design paragraph). The column keys below stay R1's so the
# deterministic verdict squares keep their lookups; the R5 reads are mapped here and nowhere else.
R5_COND = {"A": "A", "B": "B", "RAG": "C", "C": "D"}
R5_MODEL_NAME = {"claude-haiku-4-5-20251001": "Haiku 4.5", "claude-sonnet-5-5": "Sonnet 5.5", "claude-opus-5-5": "Opus 5.5",
                 "qwen2.5-7b-instruct-q4_k_m": "Qwen2.5-7B"}
MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_r5():
    """R5 reads when results.json exists and is final, else None (R1 mode).

    results.json (analyze.py): cells[cond][item] = {"false_accept": {"k","n"} or null for controls, "per_model":
    {"haiku": {"k","n"}, ...}, ...}; primary[cond]["pooled_claude"]["false_accept"] = {"k","n"} over the primary
    items; models[]; dates{first_trial_utc, ...}; n_trials_scored. Items never run with agents (M17) are absent.
    """
    if not os.path.exists(R5):
        return None
    d = json.load(open(R5))
    if not d.get("final"):
        return None
    cells, pooled = {}, {}
    for col, cond in R5_COND.items():
        items = d["cells"][cond]
        cells[col] = {i: (v["false_accept"]["k"], v["false_accept"]["n"]) for i, v in items.items()
                      if isinstance(v, dict) and isinstance(v.get("false_accept"), dict)}
        fa = d["primary"][cond]["pooled_claude"]["false_accept"]
        pooled[col] = (fa["k"], fa["n"])
    fa = d["primary"]["E"]["pooled_claude"]["false_accept"]
    pooled["E"] = (fa["k"], fa["n"])
    # replicates per Claude model in one primary cell (the pre-registered cost rule), e.g. {haiku: 6, sonnet: 5, opus: 1}
    reps = {m: v["n"] for m, v in d["cells"]["A"]["M1"]["per_model"].items()}
    per_cell = sum(reps.values())
    assert all(v[1] == per_cell for c in cells.values() for v in c.values()), "every primary cell has the same n"
    assert all(pooled[col][1] % per_cell == 0 for col in pooled)
    n_items = {col: pooled[col][1] // per_cell for col in pooled}
    day = d["dates"]["first_trial_utc"][:10]
    date_txt = f"{int(day[8:10])} {MONTHS[int(day[5:7])]} {day[:4]}"
    return {"cells": cells, "pooled": pooled, "reps": reps, "per_cell": per_cell, "n_items": n_items,
            "models": d["models"], "date": date_txt, "n_trials": d["n_trials_scored"]}


R5D = load_r5()
MODE = "R5" if R5D else "R1"

# ------------------------------------------------------------------ rows, grouped by family (MASTER §9)
GROUPS = [("value", ["M1", "M2", "M8"]), ("cell", ["M4", "M9"]), ("time", ["M10"]), ("band", ["M6"]),
          ("source", ["M11"]), ("derivation", ["M12", "M14"]), ("stale / current", ["M5", "M16"]),
          ("signature / id", ["M3", "M7", "M13"]), ("source pixel", ["M15"]), ("entity", ["M17"])]
ids_in = [i for _, g in GROUPS for i in g]
assert sorted(ids_in + ["G0"]) == sorted(META), "every R1 mutation appears exactly once"
assert len(ids_in) - 1 == SUM["I"]["applicable"] == 16, "16 in-scope corruptions + the entity case"

# Short descriptions for the 30 cm tier. Each is a shortening of meta.mutations[].desc; every number or quoted
# token it prints must occur in that desc (asserted), so no value is typed that the suite did not use.
SHORT = {
    "M1": "stated value moved by 1 ULP", "M2": "stated value rounded to “0.47”",
    "M8": "value 0.45, re-encoded and re-hashed", "M4": "record cited for another cell",
    "M9": "cell changed inside the record, re-hashed", "M10": "tslot changed to look current, re-hashed",
    "M6": "a record for another band handed over", "M11": "source scene id changed, re-hashed",
    "M12": "offset changed, value recomputed, re-hashed", "M14": "value (0.46) disagrees with the signed DNs",
    "M5": "an older record handed over as current", "M16": "a second signed version shown only to B",
    "M3": "1 ULP changed inside the served bytes", "M7": "token miscopied by one character",
    "M13": "value 0.45 under the forger's own key", "M15": "DNs read from the pixel 10 m south",
    "M17": "same record; A meant another entity (out of scope)",
}
import re  # noqa: E402
for k, s in SHORT.items():
    for num in re.findall(r"\d+(?:\.\d+)?", s):
        assert num in META[k]["desc"], (k, num)

LEVELS = ["A", "B", "C"]                    # representation columns
DEPTH = ["D", "E", "F", "G", "H", "I"]      # the EMEM receiver's checks, cumulative
CHECK = {"C": ("resolve", "L0"), "D": ("hash", "L0"), "E": ("binding", "L1"), "F": ("signature", "L0"),
         "G": ("log", "L0"), "H": ("recompute", "L2"), "I": ("re-read", "L3")}
RAMP = {"L0": C["L0"], "L1": C["L1"], "L2": C["L2"], "L3": C["L3"]}
ONLY = {m: lv for lv, ms in LOO.items() for m in ms}          # the only check that stops it
assert ONLY == {"M4": "E", "M5": "E", "M6": "E", "M9": "F", "M10": "F", "M11": "F", "M12": "F",
                "M16": "G", "M14": "H", "M15": "I"}, "rings as the brief names them"
FLIPS = set(SUM["A"]["decision_flips"])
assert FLIPS == set(SUM["B"]["decision_flips"])
SEEN = {k for k, m in META.items() if m["real_case"]}         # seen in production (amber ring)
FILL = {"acted on corrupted evidence": C["harm"], "unaffected": C["unaffected"], "refused": C["emem"],
        "n/a": C["na"], "acted correctly": C["paper"]}

# ------------------------------------------------------------------ canvas helpers
fig = fig_mm(W, H)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
LABELS = []


def T(x, y, s, size=14, claim=None, weight=400, color=None, family=None, ha="left", va="center", **kw):
    t = ax.text(x, y, s, fontsize=size, fontweight=weight, color=color or C["ink"], ha=ha, va=va,
                family=family or "IBM Plex Sans", **kw)
    LABELS.append({"text": s, "pt": size, "claim": claim})
    return t


def wmm(t):
    r = fig.canvas.get_renderer()
    return t.get_window_extent(r).width / fig.dpi * 25.4


def box(x, y, w, h, fc, ec="none", lw=0.0, r=0.6, ls="-", z=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec,
                       lw=lw / PTMM, ls=ls, zorder=z, mutation_aspect=1)
    ax.add_patch(p)
    return p


def hatch(x, y, w, h, pitch=1.6, z=2):
    ax.add_patch(Rectangle((x, y), w, h, fc=C["oos_bg"], ec="none", zorder=z))
    clip = Rectangle((x, y), w, h, transform=ax.transData)
    k = -h
    while k < w:
        ln, = ax.plot([x + k, x + k + h], [y + h, y], color=C["oos"], lw=0.35 / PTMM, zorder=z + 0.1,
                      solid_capstyle="butt")
        ln.set_clip_path(clip)
        k += pitch


def diamond(cx, cy, s, fc, z=4):
    ax.add_patch(Polygon([(cx, cy - s / 2), (cx + s / 2, cy), (cx, cy + s / 2), (cx - s / 2, cy)],
                         closed=True, fc=fc, ec="none", zorder=z))


# ------------------------------------------------------------------ geometry (mm)
RH, GG, SEP = 6.9, 1.5, 2.6         # row height, group gap, hatched separator height
GAP = 0.8                            # surface gap between tiles
X_ID = 46.0                          # id column left edge (family labels right-aligned before it)
X_DESC = 62.0
cond_cols = LEVELS[:]
if MODE == "R5":
    cond_cols = ["A", "B", "RAG", "C"]
CW = 35.0 if MODE == "R1" else 26.0
X0 = 181.0                           # first condition column
xs = {}
x = X0
for c in cond_cols:
    xs[c] = x
    x += CW + 2.0
X_EM = x + 1.0                       # EMEM depth strip: six cumulative checks D..I
SW = 10.0
X_FC = X_EM + 6 * SW + 3.0           # first check that refuses
FCW = 24.0
X_FL = X_FC + FCW + 2.0              # flips the decision
FLW = W - X_FL
assert X_FL + 12 <= W

# ------------------------------------------------------------------ header
if MODE == "R1":
    T(0.3, 3.6, "deterministic receiver, no model", 17, claim="F6.mode", weight=600, color=C["ink2"], va="center")
else:
    T(0.3, 3.6, f"agents as B: three Claude models pooled, {R5D['date']}", 17, claim="R5.dates", weight=600,
      color=C["ink2"], va="center")
# glyph legend, two rows, drawn patches + words
lx, ly = 0.0, 10.2
for fc, ec, word in ((C["harm"], "none", "B acted on corrupted evidence"), (C["unaffected"], "none", "unaffected"),
                     (C["emem"], "none", "refused"), (C["na"], "none", "not applicable")):
    box(lx, ly - 2.0, 6.0, 4.0, fc, r=0.4)
    t = T(lx + 7.6, ly, word, 14, color=C["ink2"])
    lx += 7.6 + wmm(t) + 5.0
lx, ly = 0.0, 16.0
box(lx, ly - 2.4, 11.0, 4.8, "none", ec=C["incident"], lw=0.7, r=1.2)
T(lx + 5.5, ly, "M2", 14, family=MONO, ha="center", color=C["ink"], claim="F6.ids")
t = T(lx + 13.4, ly, "seen in production", 14, color=C["incident_text"])
lx += 13.4 + wmm(t) + 5.0
box(lx + 0.9, ly - 2.0, 5.2, 4.0, C["L1"], r=0.6)
box(lx, ly - 2.9, 7.0, 5.8, "none", ec=C["ink"], lw=0.6, r=1.4)
t = T(lx + 9.0, ly, "the only check that stops it", 14, claim="X.only", color=C["ink2"])
lx += 9.0 + wmm(t) + 5.0
diamond(lx + 2.2, ly, 4.0, C["harm"])
T(lx + 5.6, ly, "flips the decision", 14, color=C["ink2"])

# column heads
HEAD = {"A": "prose", "B": "JSON", "C": "opaque id", "RAG": "RAG"}
for c in cond_cols:
    T(xs[c] + CW / 2, 6.0, HEAD[c], 18, weight=600, ha="center")
T(X_EM + 3 * SW, 6.0, "EMEM, full check", 18, weight=700, color=C["emem"], ha="center")
for k, lv in enumerate(DEPTH):
    layer = CHECK[lv][1]
    box(X_EM + k * SW + 1.6, 11.6, SW - 3.2, 5.6, RAMP[layer], r=0.6)
    T(X_EM + k * SW + SW / 2, 14.4, lv, 14, weight=700, ha="center",
      color="white" if layer in ("L2", "L3") else C["ink"])
T(X_FC + FCW / 2, 3.2, "first check", 14, ha="center", color=C["ink2"], claim="X.loo")
T(X_FC + FCW / 2, 8.6, "that refuses", 14, ha="center", color=C["ink2"], claim="X.loo")
diamond(X_FL + FLW / 2, 6.0, 4.0, C["harm"])


# ------------------------------------------------------------------ cells
def cell(xc, y, w, h, r, letter=None):
    oc = r["outcome"]
    box(xc, y, w, h, FILL[oc], ec=(C["rule"] if oc == "acted correctly" else "none"),
        lw=(0.35 if oc == "acted correctly" else 0), r=0.5)
    if oc == "n/a":
        T(xc + w / 2, y + h / 2, "n/a", 14, color=C["muted"], ha="center", claim="F6.na")
    if letter:
        T(xc + w / 2, y + h / 2, letter, 14, weight=700, color="white", ha="center")


def r5_cell(xc, y, w, h, cond, mid, r1row):
    """R5 mode: bar of the agents' false-acceptance rate, k / n, with the R1 verdict as a 3 mm square."""
    kn = R5D["cells"][cond].get(mid)
    box(xc, y + h / 2 - 1.5, 3.0, 3.0, FILL[r1row["outcome"]] if r1row else C["na"], r=0.3)
    if kn is None:   # M17 was not run with agents (results.md section 10); M7 has no prose, JSON or RAG form
        if mid == "M17":
            T(xc + 5, y + h / 2, "not run", 14, color=C["muted"], claim="R5.M17.notrun")
        else:
            T(xc + 5, y + h / 2, "n/a", 14, color=C["muted"], claim="F6.na")
        return
    k, n = kn
    bw = (w - 19) * (k / n if n else 0)
    box(xc + 4.5, y + 1.0, max(bw, 0.01), h - 2.0, C["harm"], r=0.4)
    T(xc + w, y + h / 2, f"{k}\u2009/\u2009{n}", 14, ha="right", color=C["ink2"],
      claim=f"R5.cell.{R5_COND[cond]}.{mid}.false_accept")


def row(mid, y, h, first_in_group, fam):
    if first_in_group:
        T(X_ID - 2.4, y + h / 2, fam, 17, weight=600, ha="right", claim="F6.family")
    t = T(X_ID + 0.8, y + h / 2, mid, 15, family=MONO, claim="F6.ids")
    if mid in SEEN:
        tw = wmm(t)
        box(X_ID - 0.6, y + h / 2 - 2.55, tw + 2.8, 5.1, "none", ec=C["incident"], lw=0.7, r=1.2, z=3)
    T(X_DESC, y + h / 2, SHORT.get(mid, ""), 14, color=C["ink2"], claim="F6.desc")
    for c in cond_cols:
        r1 = BY.get((mid, c)) if c != "RAG" else None
        if MODE == "R5":
            r5_cell(xs[c], y + GAP / 2, CW, h - GAP, c, mid, r1)
        else:
            cell(xs[c], y + GAP / 2, CW, h - GAP, r1,
                 letter=(r1.get("failed_check") if r1["outcome"] == "refused" else None))
    prev = None
    for k, lv in enumerate(DEPTH):
        r = BY[(mid, lv)]
        first_ref = r["outcome"] == "refused" and (prev is None or prev["outcome"] != "refused")
        cell(X_EM + k * SW + GAP / 2, y + GAP / 2, SW - GAP, h - GAP, r, letter=(lv if first_ref else None))
        prev = r
    fp = META[mid]["first_protected_level"]
    cy = y + h / 2
    if fp:
        layer = CHECK[fp][1]
        box(X_FC + 2.0, cy - 2.4, 6.6, 4.8, RAMP[layer], r=0.6, z=3)
        T(X_FC + 5.3, cy, fp, 14, weight=700, ha="center",
          color="white" if layer in ("L2", "L3") else C["ink"], claim="F6.first")
        if ONLY.get(mid) == fp:
            box(X_FC + 0.6, cy - 3.25, 9.4, 6.5, "none", ec=C["ink"], lw=0.6, r=1.6, z=3)
        T(X_FC + 11.6, cy, layer, 14, color=C["ink2"], claim="F6.first")
    else:
        hatch(X_FC + 2.0, cy - 2.4, 6.6, 4.8, pitch=1.2, z=3)
        T(X_FC + 11.6, cy, "none", 14, color=C["ink2"], claim="X.entity")
    if mid in FLIPS:
        diamond(X_FL + FLW / 2, cy, 4.0, C["harm"])


# G0 control: a thin top row
y = 21.6
g0h = 4.6
T(X_ID + 0.8, y + g0h / 2, "G0", 15, family=MONO, color=C["ink2"], claim="F6.ids")
T(X_DESC, y + g0h / 2, "nothing altered: accepted everywhere, never refused", 14, color=C["ink2"], claim="S.R1.I")
for c in cond_cols:
    if c in LEVELS:
        assert BY[("G0", c)]["outcome"] == "acted correctly"
        box(xs[c], y + 0.6, CW, g0h - 1.2, C["paper"], ec=C["rule"], lw=0.35, r=0.5)
for k, lv in enumerate(DEPTH):
    assert BY[("G0", lv)]["outcome"] == "acted correctly"
    box(X_EM + k * SW + GAP / 2, y + 0.6, SW - GAP, g0h - 1.2, C["paper"], ec=C["rule"], lw=0.35, r=0.5)
assert not any(SUM[l]["genuine_refused"] for l in SUM)

y = 28.2
row_y = {}
for gi, (fam, ids) in enumerate(GROUPS):
    if fam == "entity":
        y += 0.9
        hatch(X_ID - 2.0, y, W - X_ID + 2.0 - FLW, SEP, pitch=1.6)
        y += SEP + 1.2
    elif gi:
        ax.plot([X_ID - 2.0, W], [y - GG / 2, y - GG / 2], color=C["rule"], lw=0.3 / PTMM, zorder=1)
    for i, mid in enumerate(ids):
        row(mid, y, RH, i == 0, fam if fam != "entity" else "entity")
        row_y[mid] = y
        y += RH
    y += GG
y_end = y - GG

# ------------------------------------------------------------------ totals
yt = y_end + 2.2
ax.plot([0, W], [yt, yt], color=C["ink2"], lw=0.5 / PTMM, zorder=1)
ty = yt + 6.6
T(0.3, ty + 0.6, "B acts on corrupted evidence", 20, weight=600, claim="F6.totals_label")
claim_of = {"A": "S.R1.A", "B": "S.R1.B", "C": "S.R1.C", "I": "S.R1.I"}
R5_POOLED_CLAIM = {"A": "R5.A.pooled", "B": "R5.B.pooled", "RAG": "R5.C.pooled", "C": "R5.D.pooled", "E": "R5.E.pooled"}
R1_CEIL = {"A": ("S.R1.A", SUM["A"]), "B": ("S.R1.B", SUM["B"]), "C": ("S.R1.C", SUM["C"]), "E": ("S.R1.I", SUM["I"])}


def r5_total(xc, cond, color):
    """R5 mode: the agents' pooled false acceptance (primary items, three Claude models) with R1's total beneath
    as the deterministic ceiling, so the same quantity reads the same here and on the spine."""
    k, n = R5D["pooled"][cond]
    T(xc, ty - 1.6, f"{k}\u2009/\u2009{n}", 17, weight=700, color=color(k), ha="center", claim=R5_POOLED_CLAIM[cond])
    if cond in R1_CEIL:
        cid, s_ = R1_CEIL[cond]
        T(xc, ty + 4.2, f"R1 {s_['false_accepts']}\u2009/\u2009{s_['applicable']}", 14, color=C["ink2"], ha="center", claim=cid)


for c in cond_cols:
    if MODE == "R5":
        r5_total(xs[c] + CW / 2, c, lambda k: C["harm"] if k else C["emem"])
        continue
    s = SUM[c]
    T(xs[c] + CW / 2, ty, f"{s['false_accepts']}\u2009/\u2009{s['applicable']}", 30, weight=700,
      color=C["harm"] if s["false_accepts"] else C["emem"], ha="center", claim=claim_of[c])
s = SUM["I"]
if MODE == "R5":
    r5_total(X_EM + 3 * SW, "E", lambda k: C["emem"] if k == 0 else C["harm"])
else:
    T(X_EM + 3 * SW, ty, f"{s['false_accepts']} / {s['applicable']}", 30, weight=700,
      color=C["emem"] if s["false_accepts"] == 0 else C["harm"], ha="center", claim="S.R1.I")
assert [SUM[l]["false_accepts"] for l in "ABCI"] == [15, 15, 13, 0]
assert len(FLIPS) == 6

# ------------------------------------------------------------------ check legend and scope
yl = ty + 9.6
lx = 0.0
for lv in ["C"] + DEPTH:
    name, layer = CHECK[lv]
    box(lx, yl - 2.3, 5.6, 4.6, RAMP[layer], r=0.6)
    T(lx + 2.8, yl, lv, 14, weight=700, ha="center", color="white" if layer in ("L2", "L3") else C["ink"])
    t = T(lx + 7.0, yl, f"{name} {layer}", 14, color=C["ink2"], claim="F6.checks")
    lx += 7.0 + wmm(t) + 4.6
T(lx + 2, yl, "D to I are cumulative: each adds one check", 14, color=C["muted"], claim="F6.cumulative")

probes_pass = all(not v["refused_at_level_I"] for v in PR.values())
assert probes_pass and len(PR) == 3
scope = ("One signed Keylong NDVI record, one band, one run; deterministic receiver; rows M14 to M16 signed with a "
         "test key; the re-read compares with the committed 25 Sep window.")
scope2 = "Three further signer errors (offset, same-day scene, unit) pass checks D to I; metadata checks catch them."
scope_claim = "F6.scope"
if MODE == "R5":
    reps = ", ".join(f"{n} {R5_MODEL_NAME.get(m, m)}" for m, n in R5D["reps"].items())
    reps = reps.replace("haiku", "Haiku 4.5").replace("sonnet", "Sonnet 5.5").replace("opus", "Opus 5.5")
    scope = (f"Bars: agents' false acceptance, k of n per cell, n {R5D['per_cell']} ({reps} runs); "
             f"squares: the deterministic ceiling. Totals pool {R5D['n_items']['A']} items, {R5D['date']}.")
    scope_claim = "R5.F6.scope"
T(0, yl + 5.9, scope, 14, color=C["ink2"], claim=scope_claim)
T(0, yl + 11.2, scope2, 14, color=C["ink2"], claim="X.p123")

assert y_end < 170, y_end
save(fig, NAME)
json.dump({"figure": NAME, "size_mm": [W, H], "mode": MODE, "labels": LABELS,
           "r5": ({k: v for k, v in R5D.items() if k != "cells"} if MODE == "R5" else None)},
          open(os.path.join(OUT, f"{NAME}.labels.json"), "w"), indent=1, ensure_ascii=False)
print("mode", MODE, "rows end", round(y_end, 1), "legend", round(yl, 1))
