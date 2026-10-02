"""Prototype of the v13 M15 figure 'The right record, the wrong pixel', drawn 1:1 at 396 x 200 mm.

Real data only (no number typed by hand except the rule threshold and the published prevalence counts,
which are read from prevalence_summary.json):
  research/repro/data/keylong_B0{2,3,4,8}.bin  signed EMEMGRD1 grids, S2A L2A 25 Sep 2026, 443 x 453 px, 10 m, EPSG:32643
  research/repro/data/v8/pixel_windows.json   committed COG 5x5 windows (B04/B08 DN) for the hero record oj5cecci
  research/repro/data/v8/prevalence_summary.json   162/200 pre-fix, 0/54 post-fix, error magnitudes
Checks asserted below: the 5x5 window equals the signed grids at rows 210:215, cols 223:228 minus the BOA offset 1000.
"""
import json
import struct
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
from matplotlib.patches import ConnectionPatch, Rectangle

REPO = Path("/home/user/esa_poster")
DATA = REPO / "research/repro/data"
HERE = Path(__file__).parent
for f in (HERE / "plex/ttf").glob("*.ttf"):
    fm.fontManager.addfont(str(f))
SANS = "IBM Plex Sans"
MM = 1 / 25.4
INK, INK2, MUTED, RULE = "#222428", "#4A4D55", "#7A7D85", "#D5D6DA"
EMEM, EMEM_T, HARM, HARM_T, INC = "#0F5FA8", "#DCE8F5", "#D2481E", "#FADDD2", "#E8A317"
mpl.rcParams.update({"font.family": SANS, "svg.fonttype": "path"})


def grid(name):
    raw = (DATA / f"keylong_{name}.bin").read_bytes()
    assert raw[:8] == b"EMEMGRD1"
    w, h = struct.unpack_from("<II", raw, 8)
    return np.frombuffer(raw, dtype="<f4", offset=64).reshape(h, w).astype(float)


B2, B3, B4, B8 = (grid(b) for b in ("B02", "B03", "B04", "B08"))
pw = json.load(open(DATA / "v8/pixel_windows.json"))
key = next(k for k in pw if k.startswith("oj5cecci"))
win = pw[key]
R0, C0 = 210, 223                      # window origin inside the signed grids (MEASURED: exact match)
assert np.array_equal(B4[R0:R0 + 5, C0:C0 + 5], np.array(win["B04"]) - 1000)
assert np.array_equal(B8[R0:R0 + 5, C0:C0 + 5], np.array(win["B08"]) - 1000)
ndvi = np.array(win["ndvi_5x5"])
prev = json.load(open(DATA / "v8/prevalence_summary.json"))
pre, post = prev["pre"], prev["post"]

# true colour: R=B04 G=B03 B=B02, reflectance = grid / 10000 (grid already carries the -1000 BOA offset)
rgb = np.dstack([B4, B3, B2]) / 10000.0
lo, hi = np.percentile(rgb, 1.0), np.percentile(rgb, 99.0)
tc = np.clip((rgb - lo) / (hi - lo), 0, 1) ** (1 / 1.35)

W, H = 396, 200
fig = plt.figure(figsize=(W * MM, H * MM))


def ax_mm(x, y, w, h):
    return fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H])


# (a) the scene: 4.43 x 4.53 km at native 10 m
sw = 118
sh = sw * tc.shape[0] / tc.shape[1]
axs = ax_mm(0, 22, sw, sh)
axs.imshow(tc, interpolation="nearest")
axs.set_axis_off()
r, c = R0 + 2, C0 + 2
axs.add_patch(Rectangle((c - 12.5, r - 12.5), 25, 25, fill=False, ec="white", lw=1.6))
axs.plot([20, 120], [tc.shape[0] - 22] * 2, color="white", lw=2.2)   # 1 km = 100 px
axs.text(70, tc.shape[0] - 30, "1 km", color="white", ha="center", va="bottom", fontsize=15, fontweight=600)
fig.text(0, 1 - 6 / H, "a  Where", fontsize=22, fontweight=700, color=INK, va="top")
fig.text(0, 1 - 14 / H, "Keylong, Lahaul · Sentinel-2A L2A · 25 Sep 2026", fontsize=15, color=INK2, va="top")
fig.text(0, 1 - (22 + sh + 3) / H, "true colour from the signed B02/B03/B04 grids, 10 m;\nwhite box: 250 m around the cited cell",
         fontsize=15, color=INK2, va="top", linespacing=1.25)

# (b) the 5 x 5 window, one square per 10 m pixel
x0, wb = 134, 112
axw = ax_mm(x0, 22, wb, wb)
axw.imshow(tc[R0:R0 + 5, C0:C0 + 5], interpolation="nearest")
axw.set_xlim(-0.5, 4.5); axw.set_ylim(4.5, -0.5); axw.set_axis_off()
for i in range(5):
    for j in range(5):
        v = ndvi[i, j]
        lum = tc[R0 + i, C0 + j].mean()
        axw.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=17, fontweight=500,
                 color="white" if lum < 0.55 else INK)
axw.add_patch(Rectangle((1.5, 1.5), 1, 1, fill=False, ec="white", lw=7))
axw.add_patch(Rectangle((1.5, 1.5), 1, 1, fill=False, ec=EMEM, lw=4))
axw.add_patch(Rectangle((1.5, 2.5), 1, 1, fill=False, ec="white", lw=7))
axw.add_patch(Rectangle((1.5, 2.5), 1, 1, fill=False, ec=HARM, lw=4, ls=(0, (2.2, 1.2))))
for (xa, ya), (xb, yb) in (((c - 12.5, r - 12.5), (-0.5, -0.5)), ((c - 12.5, r + 12.5), (-0.5, 4.5))):
    fig.add_artist(ConnectionPatch((xa, ya), (xb, yb), "data", "data", axesA=axs, axesB=axw, color=MUTED, lw=0.8))
fig.text(x0 / W, 1 - 6 / H, "b  Which pixel", fontsize=22, fontweight=700, color=INK, va="top")
fig.text(x0 / W, 1 - 14 / H, "the 50 m window; NDVI per 10 m pixel", fontsize=15, color=INK2, va="top")

# (c) the consequence and the checks
xc = 262
fig.text(xc / W, 1 - 6 / H, "c  What the receiver decides", fontsize=22, fontweight=700, color=INK, va="top")
fig.text(xc / W, 1 - 14 / H, "rule under test: irrigate if NDVI ≤ 0.4705", fontsize=15, color=INK2, va="top")
ax = ax_mm(xc, 20, W - xc, H - 20)
ax.set_xlim(0, W - xc); ax.set_ylim(H - 20, 0); ax.set_axis_off()
v_named = ndvi[2, 2]
v_read = ndvi[3, 2]
ax.add_patch(Rectangle((0, 3), 9, 9, fill=False, ec=EMEM, lw=3))
ax.text(13, 6.5, "the pixel the cell names", fontsize=17, color=INK2, va="center")
ax.text(13, 14.5, f"NDVI {v_named:.4f} → hold", fontsize=24, fontweight=700, color=INK, va="center")
ax.add_patch(Rectangle((0, 25), 9, 9, fill=False, ec=HARM, lw=3, ls=(0, (2.2, 1.2))))
ax.text(13, 28.5, "the pixel the old reader took, 10 m S", fontsize=17, color=INK2, va="center")
ax.text(13, 36.5, f"NDVI {v_read:.4f} → irrigate", fontsize=24, fontweight=700, color=HARM, va="center")
# check strip
ax.text(0, 50, "receiver checks on the signed record", fontsize=15, color=MUTED, va="center")
checks = [("hash", True), ("bind", True), ("sig", True), ("log", True), ("recompute", True), ("re-read", False)]
x = 0
for name, passes in checks:
    wbx = 6 + 2.3 * len(name)
    ax.add_patch(Rectangle((x, 54), wbx, 9, fc=(HARM_T if passes else EMEM), ec="none"))
    ax.text(x + wbx / 2, 58.5, name, ha="center", va="center", fontsize=15, fontweight=600,
            color=(INK if passes else "white"))
    x += wbx + 1.6
ax.text(0, 66, "five checks pass the wrong pixel;\nonly the re-read refuses it", fontsize=15, color=INK2, va="top")
# waffle: 200 sampled pre-fix records
ax.text(0, 82, f"pre-fix audit: {pre['matches_round_not_floor']} of {pre['n']} records",
        fontsize=17, fontweight=600, color=INK, va="center")
n_bad = pre["matches_round_not_floor"]
cols, s, g = 25, 4.2, 0.8
for k in range(pre["n"]):
    i, j = divmod(k, cols)
    ax.add_patch(Rectangle((j * (s + g), 86 + i * (s + g)), s, s, fc=(HARM if k < n_bad else RULE), ec="none"))
lo95, hi95 = pre["frac_round_wilson95"][1:]
ax.text(0, 86 + 8 * (s + g) + 4, f"read a neighbouring pixel (Wilson 95 %: {lo95:.0%} to {hi95:.0%});\n"
        f"after the fix {post.get('matches_round_not_floor', 0)} of {post['n']}", fontsize=15, color=INK2, va="top")
e = pre["abs_err_index_where_differ"]
ax.text(0, 86 + 8 * (s + g) + 21, f"index error: median {e['median']:.3f}, p90 {e['p90']:.3f}, max {e['max']:.3f}",
        fontsize=15, color=INK2, va="center")
fig.savefig(HERE / "proto_m15.png", dpi=200, facecolor="white")
print("ok", v_named, v_read, post.keys())
