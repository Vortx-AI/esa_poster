"""F7 · The right record, the wrong pixel (396 x 128 mm, brief §E F7).

Real Sentinel-2A L2A pixels at native 10 m from the signed grids; nothing interpolated, nothing typed:
  research/repro/data/keylong_B0{2,3,4,8}.bin     signed EMEMGRD1 grids, 443 x 453 px, EPSG:32643, values DN - 1000
  research/repro/data/v8/pixel_windows.json      committed 5 x 5 COG windows (B04/B08 DN) of the hero record
  research/repro/data/v8/pixel_check.json        floor (containing) vs round (old reader) pixel, both records
  research/repro/data/v8/prevalence_summary.json 162 / 200 pre-fix, Wilson interval, post-fix 0 / 54, index error
  research/v13/evidence/g1_pixel_audit/prevalence.json   the 121 index errors behind the strip plot
  research/v13/evidence/critic/kx.json            the real pre-fix record (fetched 2026-10-01)
  research/v13/evidence/failure_modes/rondonia_floor_round_v2.json   Rondonia scope line
Asserts before drawing: window == grids - 1000 (B04, B08); NDVI per pixel recomputed from DNs; named / south pixel
from pixel_check.json; 162 + 38 == 200; the 121 errors reproduce median, p90 and max.

    python poster/figs_v13/f7_wrong_pixel.py
"""
import json
import math
import os
import statistics
import struct
import sys

import numpy as np
from matplotlib.patches import ConnectionPatch, Rectangle, FancyBboxPatch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, MONO, OUT, ROOT, fig_mm, save  # noqa: E402

W, H = 396.0, 128.0
PTMM = 25.4 / 72
NAME = "f7_wrong_pixel"
D = os.path.join(ROOT, "research/repro/data")
G1 = os.path.join(ROOT, "research/v13/evidence/g1_pixel_audit")


# ------------------------------------------------------------------ data
def grid(b):
    raw = open(os.path.join(D, f"keylong_{b}.bin"), "rb").read()
    assert raw[:8] == b"EMEMGRD1"
    w, h, epsg = struct.unpack_from("<IIi", raw, 8)
    n0, e0, dy, dx = struct.unpack_from("<dddd", raw, 24)
    assert (w, h, epsg, dx, dy) == (443, 453, 32643, 10.0, -10.0)
    assert (e0, n0) == (688735.0, 3607705.0)
    return np.frombuffer(raw, dtype="<f4", offset=64).reshape(h, w).astype(float)


B2, B3, B4, B8 = (grid(b) for b in ("B02", "B03", "B04", "B08"))
PX = 10.0                                   # m per pixel, asserted from the header
PW = json.load(open(os.path.join(D, "v8/pixel_windows.json")))
key = next(k for k in PW if k.startswith("oj5cecci"))
WIN = PW[key]
oc, orr = WIN["window_origin_col_row"]
R0, C0 = 210, 223                           # window origin inside the signed grids (report 06 §0.1)
assert (oc - C0, orr - R0) == (9096 - 223, 9441 - 210)
b4w, b8w = np.array(WIN["B04"], float), np.array(WIN["B08"], float)
assert np.array_equal(B4[R0:R0 + 5, C0:C0 + 5], b4w - 1000)
assert np.array_equal(B8[R0:R0 + 5, C0:C0 + 5], b8w - 1000)
off = WIN["offset"]
NDVI = (b8w - b4w) / ((b8w + off) + (b4w + off))
assert np.allclose(NDVI, np.array(WIN["ndvi_5x5"]), atol=1e-12, rtol=0)

PC = json.load(open(os.path.join(D, "v8/pixel_check.json")))
now = next(v for k, v in PC.items() if "oj5cecci" in k)
prev_k = next(k for k in PC if "kxjvfwpa" in k)
prev = PC[prev_k]
cc, cr = WIN["centre_col_row"]
fr, fc = math.floor(cr) - orr, math.floor(cc) - oc          # containing pixel in the window
rr, rc = round(cr) - orr, round(cc) - oc                    # the old reader's rounded index
assert (fr, fc) == tuple(WIN["containing_pixel_in_window"]) == (2, 2)
assert (rr, rc) == (3, 2), "rounding moved one row: the pixel 10 m south"
assert list(now["B08"]["floor(r,c)"]) == [orr + fr, oc + fc] and list(now["B08"]["round(r,c)"]) == [orr + rr, oc + rc]
V_NAMED, V_SOUTH = now["ndvi_floor_pixel"], now["ndvi_round_pixel"]
assert abs(NDVI[fr, fc] - V_NAMED) < 1e-12 and abs(NDVI[rr, rc] - V_SOUTH) < 1e-12

RULE = 0.4705
mm_rule = json.load(open(os.path.join(ROOT, "research/repro/v11/out/mutation_matrix.json")))["meta"]["rule"]
assert mm_rule == f"irrigate iff NDVI <= {RULE}"
dec = lambda v: "irrigate" if v <= RULE else "hold"
assert (dec(V_NAMED), dec(V_SOUTH)) == ("hold", "irrigate")

PS = json.load(open(os.path.join(D, "v8/prevalence_summary.json")))
pre, post = PS["pre"], PS["post"]
N, K = pre["n"], pre["matches_round_not_floor"]
SAME = pre["floor_equals_round_pixel"]
assert (N, K, SAME, pre["other"], pre["matches_floor_not_round"]) == (200, 162, 38, 0, 0) and K + SAME == N
_, wlo, whi = pre["frac_round_wilson95"]
E = pre["abs_err_index_where_differ"]
R = [r for r in json.load(open(os.path.join(G1, "prevalence.json"))) if "error" not in r and r["prefix_bool"]]
ERR = sorted(abs(r["signed_value"] - r["floor_value"]) for r in R if r["band"].startswith("indices.")
             and r["floor_value"] is not None and r["match_class"] != "floor=round")


def pctl(v, q):
    k = (len(v) - 1) * q
    f = math.floor(k)
    c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)


assert len(ERR) == E["n"] == 121
assert abs(statistics.median(ERR) - E["median"]) < 1e-15 and abs(pctl(ERR, .9) - E["p90"]) < 1e-15
assert abs(max(ERR) - E["max"]) < 1e-15
assert (post["n"], post["matches_round_not_floor"]) == (54, 0) and set(post["providers"]) == {"PC"}
assert pre["providers"] == {"E84": 192, "PC": 8}

KX = json.load(open(os.path.join(ROOT, "research/v13/evidence/critic/kx.json")))
assert abs(KX["value"] - prev["ndvi_round_pixel"]) < 1e-15 and KX["tslot"] == 20719
assert KX["derivation"]["args"][5] == [prev["B08"]["round_DN"], prev["B04"]["round_DN"]]
KX_ID = prev_k.split("fact ")[1].split(",")[0]
assert KX_ID == "kxjvfwpa"

RO = json.load(open(os.path.join(ROOT, "research/v13/evidence/failure_modes/rondonia_floor_round_v2.json")))

# true colour: R=B04 G=B03 B=B02, reflectance = grid / 10 000; one linear 1 to 99 % stretch, gamma 1/1.35
rgb = np.dstack([B4, B3, B2]) / 10000.0
lo, hi = np.percentile(rgb, 1.0), np.percentile(rgb, 99.0)
TC = np.clip((rgb - lo) / (hi - lo), 0, 1) ** (1 / 1.35)

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


def runs(x, y, parts, va="center"):
    """Set successive text runs on one baseline; parts = [(text, kwargs)]."""
    for s, kw in parts:
        t = T(x, y, s, va=va, **kw)
        x += wmm(t)
    return x


def wrap(s, width, size):
    words, lines, cur = s.split(" "), [], ""
    probe = ax.text(0, 0, "", fontsize=size, family="IBM Plex Sans")
    for w_ in words:
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


def box(x, y, w, h, fc, ec="none", lw=0.0, r=0.6, ls="-", z=3):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw / PTMM,
                       ls=ls, zorder=z)
    ax.add_patch(p)
    return p


def outline(x, y, w, h, color, dashed=False, z=5, stroke=1.4, halo=2.4):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec="white", lw=halo / PTMM, zorder=z, joinstyle="miter"))
    ls = (0, (2.2 / stroke, 1.2 / stroke)) if dashed else "-"
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=color, lw=stroke / PTMM, ls=ls, zorder=z + 0.1,
                           joinstyle="miter"))


# ------------------------------------------------------------------ (a) the scene at native 10 m
SC_W = 443 * 3 / 300 * 25.4                 # x3 integer upscale at 300 dpi = 112.52 mm
ROWS = 386                                  # crop rows (all 443 columns kept); row 212 inside
RA = 33
assert RA <= R0 + 2 < RA + ROWS <= 453
SC_H = ROWS * 3 / 300 * 25.4
UP = 6                                      # integer nearest-neighbour upscale before embedding (SVG keeps squares)
img = np.repeat(np.repeat(TC[RA:RA + ROWS], UP, 0), UP, 1)
ax.imshow(img, extent=(0, SC_W, SC_H, 0), interpolation="none", zorder=1)
s = SC_W / 443                              # mm per pixel
cx, cy = (C0 + 2 + 0.5) * s, (R0 + 2 - RA + 0.5) * s
half = 12.5 * s                             # 25 px = 250 m box
ax.add_patch(Rectangle((cx - half, cy - half), 2 * half, 2 * half, fill=False, ec="white", lw=0.9 / PTMM, zorder=4))
# top strip: place, sensor, date
ax.add_patch(Rectangle((0, 0), SC_W, 13.0, fc="black", alpha=0.62, ec="none", zorder=3))
T(1.6, 3.9, "a", 17, weight=700, color="white", claim="F7.scene")
T(6.0, 3.6, "Keylong, Lahaul", 17, weight=600, color="white", claim="F7.scene")
T(6.0, 9.6, "Sentinel-2A L2A · 25 Sep 2026", 14, color="white", claim="F7.scene")
# bottom strip: scale bar and processing line
ax.add_patch(Rectangle((0, SC_H - 12.4), SC_W, 12.4, fc="black", alpha=0.62, ec="none", zorder=3))
km = 1000 / PX * s
ax.plot([SC_W - 3 - km, SC_W - 3], [8.6, 8.6], color="white", lw=0.9 / PTMM, zorder=4, solid_capstyle="butt")
for xe in (SC_W - 3 - km, SC_W - 3):
    ax.plot([xe, xe], [7.4, 9.8], color="white", lw=0.5 / PTMM, zorder=4)
T(SC_W - 3 - km / 2, 4.2, "1 km", 14, weight=600, color="white", ha="center", claim="F7.scale")
T(1.6, SC_H - 8.6, "true colour B04/B03/B02, signed 10 m grids,", 14, color="white", claim="H.img.grid")
T(1.6, SC_H - 3.4, "linear 1 to 99 % stretch, γ 1/1.35", 14, color="white", claim="H.img.grid")

# ------------------------------------------------------------------ (b) the 5 x 5 window, one square per 10 m pixel
BX, BY, BW = 120.5, 7.0, 95.0
P = BW / 5
T(BX, 3.2, "b", 17, weight=700, claim="F7.window")
T(BX + 4.6, 3.2, "NDVI of each 10 m pixel", 15, color=C["ink2"], claim="F7.window")
for i in range(5):
    for j in range(5):
        col = TC[R0 + i, C0 + j]
        ax.add_patch(Rectangle((BX + j * P, BY + i * P), P, P, fc=col, ec="none", zorder=2))
        lum = 0.2126 * col[0] + 0.7152 * col[1] + 0.0722 * col[2]
        T(BX + (j + 0.5) * P, BY + (i + 0.5) * P, f"{NDVI[i, j]:.2f}", 17, weight=500,
          color="white" if lum < 0.5 else C["ink"], ha="center", claim="F7.window")
inset = 1.0
outline(BX + fc * P + inset, BY + fr * P + inset, P - 2 * inset, P - 2 * inset, C["emem"])
outline(BX + rc * P + inset, BY + rr * P + inset, P - 2 * inset, P - 2 * inset, C["harm"], dashed=True)
for (ya, yb) in ((cy - half, BY), (cy + half, BY + BW)):
    ax.plot([cx + half, BX], [ya, yb], color=C["muted"], lw=0.35 / PTMM, zorder=4)

# ------------------------------------------------------------------ (c) what the receiver decides
XC = 228.0
T(XC, 3.2, "c", 17, weight=700, claim="F7.scope")
T(XC + 4.6, 3.2, f"test rule: irrigate if NDVI ≤ {RULE}", 17, color=C["ink2"], claim="S.threshold")
yy = 14.0
box(XC, yy - 3.6, 7.2, 7.2, "none", ec=C["emem"], lw=1.4, r=0.01)
x = runs(XC + 10.6, yy, [(f"{V_NAMED:.4f}: hold", dict(size=30, weight=700, claim="W.vals"))])
T(x + 4.0, yy + 0.6, "named pixel", 17, color=C["ink2"], claim="F7.named")
yy = 27.0
box(XC, yy - 3.6, 7.2, 7.2, "none", ec=C["harm"], lw=1.4, r=0.01, ls=(0, (2.2 / 1.4, 1.2 / 1.4)))
x = runs(XC + 10.6, yy, [(f"{V_SOUTH:.4f}: irrigate", dict(size=30, weight=700, color=C["harm"],
                                                                     claim="W.vals"))])
T(x + 4.0, yy + 0.6, "pixel 10 m south", 17, color=C["ink2"], claim="W.south")

# the receiver's checks on the signed record
yc, hc = 37.4, 7.0
x = XC
chips = [("hash", True), ("binding", True), ("signature", True), ("log", True), ("recompute", True),
         ("re-read", False)]
spans = []
for name, passes in chips:
    t = T(0, 0, name, 15, weight=600, color=C["ink"] if passes else "white", ha="center", claim="F7.chips")
    cw = wmm(t) + 5.0
    box(x, yc, cw, hc, C["harm_tint"] if passes else C["emem"], r=1.2)
    t.set_position((x + cw / 2, yc + hc / 2))
    spans.append((x, x + cw, passes))
    x += cw + 1.6
x_pass_end = max(b for a, b, p in spans if p)
yb_ = yc + hc + 1.6
ax.plot([XC, XC, x_pass_end, x_pass_end], [yb_, yb_ + 1.2, yb_ + 1.2, yb_], color=C["harm_text"], lw=0.5 / PTMM,
        zorder=4)
T(XC, yb_ + 4.6, "pass the wrong value", 15, color=C["harm_text"], claim="F7.chips")
a, b, _ = spans[-1]
T((a + b) / 2, yb_ + 4.6, "refuses", 15, weight=700, color=C["emem"], ha="center", claim="F7.chips")

# waffle: the 200 sampled pre-fix records
WY, PITCH, SQ = 59.0, 4.4, 3.8
for k in range(N):
    i, j = divmod(k, 20)
    ax.add_patch(Rectangle((XC + j * PITCH, WY + i * PITCH), SQ, SQ, fc=C["harm"] if k < K else C["unaffected"],
                           ec="none", zorder=3))
XR = XC + 20 * PITCH + 4.0
T(XR, WY + 3.0, f"{K} of {N}", 30, weight=700, color=C["harm"], claim="W.prev")
T(XR, WY + 11.6, "sampled pre-fix records", 15, color=C["ink"], claim="W.prev")
T(XR, WY + 17.6, "carry a neighbour's values", 15, color=C["ink"], claim="W.prev")
T(XR, WY + 23.4, f"Wilson 95 %: {wlo * 100:.0f} to {whi * 100:.0f} %", 14, color=C["ink2"], claim="W.prev")
ax.add_patch(Rectangle((XR, WY + 31.4 - SQ / 2), SQ, SQ, fc=C["unaffected"], ec=C["rule"], lw=0.3 / PTMM, zorder=3))
T(XR + SQ + 1.8, WY + 31.4, f"{SAME}: both rules agree", 14, color=C["ink2"], claim="F7.same")
assert f"{wlo * 100:.0f} to {whi * 100:.0f}" == "75 to 86"

# ------------------------------------------------------------------ bottom-left: the error distribution (n 121: indices.* records of the 162 where the rules differ)
y0 = SC_H + 3.4
T(0.3, y0, "spectral-index error where the rules differ", 14, color=C["ink2"], claim="W.err")   # the 121 are the index-band records of the 162 (41 reflectance bands excluded)
t = T(SC_W, y0, f"n {E['n']}", 14, color=C["ink2"], ha="right", claim="W.err")
LMIN, LMAX = -5.0, math.log10(0.5)          # log axis: errors span four decades
assert ERR[0] > 10 ** LMIN and ERR[-1] < 10 ** LMAX
sx = lambda v: 1.0 + (math.log10(v) - LMIN) / (LMAX - LMIN) * (SC_W - 2.0)
XMAX = 0.5
ya = y0 + 14.4
ax.plot([sx(10 ** LMIN), sx(XMAX)], [ya, ya], color=C["ink2"], lw=0.5 / PTMM, zorder=3)
# dot strip: one dot per record, stacked where dots would touch (a quantised beeswarm, no jitter noise)
DOT = 1.0
levels = []
for v in ERR:
    xv = sx(v)
    lvl = 0
    while any(abs(xv - x2) < DOT * 1.05 and l2 == lvl for x2, l2 in levels):
        lvl += 1
    levels.append((xv, lvl))
for xv, lvl in levels:
    ax.add_patch(matplotlib_circle := __import__("matplotlib").patches.Circle(
        (xv, ya - 1.2 - lvl * DOT * 0.95), DOT / 2, fc=C["harm"], ec="white", lw=0.12 / PTMM, zorder=4))
print("strip max stack", max(l for _, l in levels)); assert max(l for _, l in levels) * DOT * 0.95 < 10.5
for v in (1e-4, 1e-3, 1e-2, 1e-1):
    ax.plot([sx(v), sx(v)], [ya, ya + 1.2], color=C["ink2"], lw=0.4 / PTMM, zorder=3)
for v, lab in ((1e-4, "0.0001"), (1e-3, "0.001"), (1e-2, "0.01"), (1e-1, "0.1")):
    T(sx(v), ya + 4.0, lab, 14, color=C["muted"], ha="center", claim="F7.axis")
for v in (E["median"], E["p90"], E["max"]):
    ax.plot([sx(v), sx(v)], [ya - 10.0, ya + 1.6], color=C["ink"], lw=0.45 / PTMM, zorder=3.5)
T(SC_W, ya + 9.4, f"median {E['median']:.3f} · p90 {E['p90']:.3f} · max {E['max']:.3f}", 14,
  color=C["ink"], ha="right", claim="W.err")

# ------------------------------------------------------------------ bottom-right: the real record and the scope
XS = BX
yr = BY + BW + 5.2
runs(XS, yr, [("the real record ", dict(size=17, color=C["ink2"], claim="W.kx")),
              (f"{KX_ID}…", dict(size=17, family=MONO, color=C["ink"], claim="W.kx")),
              ("\u00a0· 23 Sep 2026 · signed ", dict(size=17, color=C["ink2"], claim="W.kx")),
              (f"{prev['ndvi_round_pixel']:.4f}", dict(size=17, weight=700, color=C["harm_text"], claim="W.kx")),
              ("\u00a0· its containing pixel ", dict(size=17, color=C["ink2"], claim="W.kx")),
              (f"{prev['ndvi_floor_pixel']:.4f}", dict(size=17, weight=700, color=C["emem"], claim="W.kx"))])
n_ro = len(RO["lossyear"])
ly_changed = sum(r["floor"] != r["round"] for r in RO["lossyear"])
flag = lambda rule: {i for i, (l, g) in enumerate(zip(RO["lossyear"], RO["gfc2020"])) if g[rule] == 1 and l[rule] > 20}
assert (n_ro, ly_changed) == (100, 7) and flag("floor") == flag("round"), "no EUDR flag changed"
scope = (f"Sample: {N} pre-fix Sentinel-2 records cited in emem.dev's public channel, one per cell, seeded; "
         f"{pre['providers']['E84']} Element84, {pre['providers']['PC']} Planetary Computer. After the fix, "
         f"{post['matches_round_not_floor']} of {post['n']} (Planetary Computer, two days; not a matched sample). On a {n_ro}-point Rondônia "
         f"grid the old rule changed {ly_changed} loss years and no EUDR flag. (b) applies the old rule to the 25 Sep scene.")
lines = wrap(scope, W - XS - 5.0, 14)
assert len(lines) <= 3, lines
for k, ln in enumerate(lines):
    T(XS, yr + 6.4 + k * 5.4, ln, 14, color=C["ink2"], claim="F7.scope")

save(fig, NAME)
json.dump({"figure": NAME, "size_mm": [W, H], "labels": LABELS},
          open(os.path.join(OUT, f"{NAME}.labels.json"), "w"), indent=1, ensure_ascii=False)
