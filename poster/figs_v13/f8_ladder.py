"""F8 · Checks stop at the source: the two-sided ladder L0 to L5 (193.5 x 138 mm, brief §E F8; the v13.2 board draws it
compact at 193.5 x 60 mm with --height 60: one evidence line per rung at 14 pt, the status words and the hatch kept).

Counts are read from their files and asserted:
  research/repro/v12/data/eo_evidence_per_fact_checks.csv   780 records: verified, cell/band bound, recompute
  research/v13/evidence/critic/cell.json                    215 Keylong source entries (1 Oct), none with a hash or cid
  research/v13/evidence/crossruntime/refusal_matrix.json    a relabelled (wrong-cell) token: HTTP 409 on REST
  research/repro/v11/out/mutation_matrix.json               M17 accepted at every level A to I
  research/v13/evidence/failure_modes/jrc146622.txt:236     GFC2020 V3 forest commission error 13.1 %
Status words: report 10 §3.1 vocabulary (claims row L.status).

    python poster/figs_v13/f8_ladder.py [--height 138]     # < 120 mm selects the compact layout (v13.2 board: 60)
"""
import csv
import json
import os
import re
import sys

from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, OUT, ROOT, fig_mm, save  # noqa: E402

W = 193.5
H = float(sys.argv[sys.argv.index("--height") + 1]) if "--height" in sys.argv else 138.0   # default: the brief's F8
COMPACT = H < 120.0
PTMM = 25.4 / 72
NAME = "f8_ladder"

# ------------------------------------------------------------------ data
CSV = list(csv.DictReader(open(os.path.join(ROOT, "research/repro/v12/data/eo_evidence_per_fact_checks.csv"))))
N = len(CSV)
L0_OK = sum(r["verified"] == "PASS" and r["cid_recomputed"] == "pass" and r["attestation_sig_valid"] == "pass"
            and r["log_inclusion_valid"] == "pass" for r in CSV)
L1_OK = sum(r["cell_bound"] == "pass" and r["band_bound"] == "pass" for r in CSV)
L2_OK = sum(r["recompute"] == "pass" for r in CSV)
assert (N, L0_OK, L1_OK, L2_OK) == (780, 780, 780, 266)
KEY = json.load(open(os.path.join(ROOT, "research/v13/evidence/critic/cell.json")))      # 209 facts, 2026-10-01T01:41Z
SRC = [s for f in KEY["facts"] for s in f.get("sources", [])]
N_SRC, N_HASH = len(SRC), sum(1 for s in SRC if s.get("hash") or s.get("cid"))
assert (N_SRC, N_HASH) == (215, 0)
RM = json.load(open(os.path.join(ROOT, "research/v13/evidence/crossruntime/refusal_matrix.json")))
CODE = re.search(r"HTTP (\d{3})", RM["wrong_cell"]["rest"]).group(1)
assert CODE == "409"
MM = json.load(open(os.path.join(ROOT, "research/repro/v11/out/mutation_matrix.json")))
assert all(r["outcome"] == "acted on corrupted evidence" for r in MM["rows"] if r["mutation"] == "M17")
assert MM["summary"]["I"]["entity_case_accepted"]
JRC = open(os.path.join(ROOT, "research/v13/evidence/failure_modes/jrc146622.txt"), encoding="utf-8").read().splitlines()
GFC = re.search(r"commission error of (\d+\.\d)%", JRC[235]).group(1)
assert GFC == "13.1"

# ------------------------------------------------------------------ rungs, bottom to top
RUNGS = [
    dict(L="L0", name=["record bytes"], status=["CHECKABLE"], fill="L0",
         ev=f"{L0_OK} of {N}: hash, signature, log", trust="still trusted: the key is emem.dev's",
         claims=("L.780", "T.oneop")),
    dict(L="L1", name=["identity"], status=["CHECKABLE"], fill="L1",
         ev=f"cell and band bound in {L1_OK} of {N}; a relabelled token returns {CODE}",
         trust="still trusted: your own question", claims=("L.780", "F8.trust")),
    dict(L="L2", name=["derivation"], status=["RECOMPUTABLE"], fill="L2",
         ev=f"{L2_OK} of {N} carry a recipe; all {L2_OK} recompute", trust="still trusted: the convention the signer chose",
         claims=("L.266", "F8.trust")),
    dict(L="L3", name=["source"], status=["PARTIAL"], fill="half",
         ev=f"named, not hashed: {N_HASH} of {N_SRC} Keylong sources carry a hash; open archives can be re-read",
         trust="still trusted: that the archive file is the product", claims=("O.nohash", "F8.trust")),
    dict(L="L4", name=["entity"], status=["OUT OF SCOPE"], fill="hatch",
         ev="M17 passes every check; “this image” became a hair salon", trust=None,
         claims=("X.entity", None)),
    dict(L="L5", name=["physical truth,", "decision"], status=["INHERITED /", "OUT OF SCOPE"], fill="hatch",
         ev=f"GFC2020 V3 forest commission error {GFC}\u00a0%", trust=None, claims=("L.gfc", None)),
]
HEIGHTS = {"L0": 17.0, "L1": 22.4, "L2": 22.0, "L3": 26.2, "L4": 18.4, "L5": 24.2}
GAP, EDGE = 1.2, 3.0                     # gap between rungs; the wider gap is the claim's edge (L3 | L4)
# compact (v13.2): one evidence line per rung; L4 and L5 take two lines (L5's name and status, L4's two-part evidence)
COMPACT_EV = {"L0": [f"{L0_OK} of {N}: hash, signature, log"],
              "L1": [f"cell and band bound in {L1_OK} of {N}"],
              "L2": [f"{L2_OK} of {N} recompute from a recipe"],
              "L3": [f"named, not hashed: {N_HASH} of {N_SRC} hashed"],
              "L4": ["M17 passes every check; “this image”", "became a hair salon"],
              "L5": ["GFC2020 V3 forest commission", f"error {GFC} %"]}
if COMPACT:
    R1 = (H - 4 * GAP - EDGE - 2 * 5.2) / 6       # single rows; L4 and L5 are one 14 pt line (5.2 mm) taller
    assert R1 >= 6.9, f"height {H} mm is too small for six rungs with 14 pt text (row {R1:.1f} mm)"
    HEIGHTS = {"L0": R1, "L1": R1, "L2": R1, "L3": R1, "L4": R1 + 5.2, "L5": R1 + 5.2}
assert abs(sum(HEIGHTS.values()) + 4 * GAP + EDGE - H) < 1e-6

# ------------------------------------------------------------------ canvas
fig = fig_mm(W, H)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
LABELS = []


def T(x, y, s, size=14, claim=None, weight=400, color=None, ha="left", va="center", z=6, **kw):
    t = ax.text(x, y, s, fontsize=size, fontweight=weight, color=color or C["ink"], ha=ha, va=va,
                family="IBM Plex Sans", zorder=z, **kw)
    LABELS.append({"text": s.replace("\u00a0", " "), "pt": size, "claim": claim})
    return t


def wmm(t):
    return t.get_window_extent(fig.canvas.get_renderer()).width / fig.dpi * 25.4


def wrap(s, width, size, weight=400):
    probe = ax.text(0, 0, "", fontsize=size, fontweight=weight, family="IBM Plex Sans")
    lines, cur = [], ""
    for w_ in s.split(" "):
        cand = (cur + " " + w_).strip()
        probe.set_text(cand)
        if wmm(probe) > width and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = cand
    lines.append(cur)
    probe.remove()
    return lines


def box(x, y, w, h, fc, ec="none", lw=0.0, r=1.0, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec,
                                lw=lw / PTMM, zorder=z))


def hatch(x, y, w, h, pitch=1.6, z=2):
    ax.add_patch(Rectangle((x, y), w, h, fc=C["oos_bg"], ec="none", zorder=z))
    clip = Rectangle((x, y), w, h, transform=ax.transData)
    k = -h
    while k < w:
        ln, = ax.plot([x + k, x + k + h], [y + h, y], color=C["oos"], lw=0.35 / PTMM, zorder=z + 0.1)
        ln.set_clip_path(clip)
        k += pitch


if not COMPACT:
    XL, WL = 0.0, 70.0                       # left plate: layer, name, status
    XR = 72.0                                # right part: depth fill with the evidence on a white plate
    WR = W - XR
    BAR = 8.0                                # visible fill at the plate's left
    PAD = 1.6

    y = H
    for i, r in enumerate(RUNGS):
        h = HEIGHTS[r["L"]]
        y -= h
        oos = r["fill"] == "hatch"
        # left plate
        box(XL, y, WL, h, C["paper"], ec=C["rule"], lw=0.35, r=1.2)
        cy = y + h / 2
        if oos:
            box(XL + 2.2, cy - 6.0, 13.0, 12.0, C["paper"], ec=C["oos"], lw=0.6, r=1.4, z=3)
            T(XL + 8.7, cy, r["L"], 20, weight=700, color=C["ink2"], ha="center", claim="L.status")
        else:
            col = C[r["fill"]] if r["fill"] != "half" else C["L3"]
            box(XL + 2.2, cy - 6.0, 13.0, 12.0, col, r=1.4, z=3)
            T(XL + 8.7, cy, r["L"], 20, weight=700, color=C["ink"] if r["L"] in ("L0", "L1") else "white",
              ha="center", claim="L.status")
        lines = [(s, 18, 600, C["ink"] if not oos else C["ink2"], 6.6 if len(r["name"]) == 1 else 6.5) for s in r["name"]] + \
                [(s, 14, 600, C["emem"] if r["status"][0] in ("CHECKABLE", "RECOMPUTABLE") else C["ink2"], 5.4)
                 for s in r["status"]]
        tot = sum(l[4] for l in lines)
        yy = cy - tot / 2
        for s, size, wt, col, lh in lines:
            t = T(XL + 18.5, yy + lh / 2, s, size, weight=wt, color=col, claim="L.status")
            yy += lh
            assert wmm(t) < WL - 19.5, (s, wmm(t))
        # right part: fill
        if r["fill"] in ("L0", "L1", "L2"):
            box(XR, y, WR, h, C[r["fill"]], r=1.2, z=1)
        elif r["fill"] == "half":
            box(XR, y, WR / 2 + 1.5, h, C["L3"], r=1.2, z=1)
            hatch(XR + WR / 2, y, WR / 2, h, z=1)
        else:
            hatch(XR, y, WR, h, z=1)
        # evidence on a white plate
        px, pw = XR + BAR, WR - BAR - 5.0
        box(px, y + PAD, pw, h - 2 * PAD, C["paper"], r=0.8, z=3)
        ev = wrap(r["ev"], pw - 5.0, 15)
        tr = wrap(r["trust"], pw - 5.0, 14) if r["trust"] else []
        block = len(ev) * 5.6 + len(tr) * 5.0
        assert block <= h - 2 * PAD - 0.4, (r["L"], ev, tr, block, h)
        yy = cy - block / 2
        for s in ev:
            T(px + 2.6, yy + 2.8, s, 15, color=C["ink"], claim=r["claims"][0])
            yy += 5.6
        for s in tr:
            T(px + 2.6, yy + 2.5, s, 14, color=C["muted"], claim=r["claims"][1])
            yy += 5.0
        y -= GAP if r["L"] != "L3" else EDGE
        if r["L"] == "L3":
            ax.plot([0, W], [y + EDGE / 2, y + EDGE / 2], color=C["ink"], lw=0.8 / PTMM, zorder=4,
                    solid_capstyle="butt")
    assert abs(y + GAP) < 1e-6 or abs(y) < 1e-6 or y > -GAP - 1e-6, y

else:
    # ------------------------------------------------------------------ compact layout (v13.2): one row per rung
    XL, WL = 0.0, 92.0                   # left plate: badge, name (16 pt) and status word (14 pt) on one line
    XR = 94.0
    WR = W - XR
    BAR, PAD = 6.0, 0.7
    y = H
    for i, r in enumerate(RUNGS):
        h = HEIGHTS[r["L"]]
        y -= h
        oos = r["fill"] == "hatch"
        box(XL, y, WL, h, C["paper"], ec=C["rule"], lw=0.35, r=1.0)
        cy = y + h / 2
        two = len(r["name"]) > 1         # L5: name on the first line, status on the second
        by_ = cy - 2.6 if two else cy
        if oos:
            box(XL + 2.0, by_ - 3.0, 11.5, 6.0, C["paper"], ec=C["oos"], lw=0.6, r=1.0, z=3)
            T(XL + 7.75, by_ + 0.1, r["L"], 16, weight=700, color=C["ink2"], ha="center", claim="L.status")
        else:
            col = C[r["fill"]] if r["fill"] != "half" else C["L3"]
            box(XL + 2.0, by_ - 3.0, 11.5, 6.0, col, r=1.0, z=3)
            T(XL + 7.75, by_ + 0.1, r["L"], 16, weight=700, color=C["ink"] if r["L"] in ("L0", "L1") else "white",
              ha="center", claim="L.status")
        name = " ".join(r["name"])
        tn = T(XL + 16.0, by_, name, 16, weight=600, color=C["ink"] if not oos else C["ink2"], claim="L.status")
        status = " ".join(r["status"])
        scol = C["emem"] if r["status"][0] in ("CHECKABLE", "RECOMPUTABLE") else C["ink2"]
        if two:
            ts = T(XL + 16.0, cy + 2.8, status, 14, weight=600, color=scol, claim="L.status")
            assert wmm(ts) <= WL - 17.5, (status, wmm(ts))
        else:
            ts = T(XL + 16.0 + wmm(tn) + 2.6, cy + 0.1, status, 14, weight=600, color=scol, claim="L.status")
            assert XL + 16.0 + wmm(tn) + 2.6 + wmm(ts) <= WL - 1.5, (name, status, wmm(tn), wmm(ts))
        if r["fill"] in ("L0", "L1", "L2"):
            box(XR, y, WR, h, C[r["fill"]], r=1.0, z=1)
        elif r["fill"] == "half":
            box(XR, y, WR / 2 + 1.5, h, C["L3"], r=1.0, z=1)
            hatch(XR + WR / 2, y, WR / 2, h, z=1)
        else:
            hatch(XR, y, WR, h, z=1)
        px, pw = XR + BAR, WR - BAR - 3.0
        box(px, y + PAD, pw, h - 2 * PAD, C["paper"], r=0.8, z=3)
        ev = COMPACT_EV[r["L"]]
        assert len(ev) * 5.2 <= h - 2 * PAD, (r["L"], ev, h)
        yy = cy - (len(ev) - 1) * 2.6
        for s_ in ev:
            t = T(px + 2.2, yy + 0.1, s_, 14, color=C["ink"], claim=r["claims"][0])
            assert wmm(t) <= pw - 3.6, (s_, wmm(t))
            yy += 5.2
        y -= GAP if r["L"] != "L3" else EDGE
        if r["L"] == "L3":
            ax.plot([0, W], [y + EDGE / 2, y + EDGE / 2], color=C["ink"], lw=0.8 / PTMM, zorder=4,
                    solid_capstyle="butt")
    assert abs(y) < 1e-6 or y > -GAP - 1e-6, y

save(fig, NAME)
json.dump({"figure": NAME, "size_mm": [W, H], "labels": LABELS},
          open(os.path.join(OUT, f"{NAME}.labels.json"), "w"), indent=1, ensure_ascii=False)
