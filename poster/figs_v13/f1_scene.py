"""F1 · Header scene: the record this board follows (brief §E F1; 216.5 x 188 mm incl. 3 mm right bleed).

Real data only:
  research/repro/data/keylong_B0{2,3,4,8}.bin  signed EMEMGRD1 grids, S2A L2A 25 Sep 2026, 443 x 453 px, 10 m, EPSG:32643
  research/repro/data/v8/pixel_windows.json   committed COG 5 x 5 DN windows of the hero record oj5cecci
  research/repro/v8/proof_bundle_ndvi.cbor   (via the R1 suite) the signed record: value, scene, tslot
  poster/fig/v13/qr_demo.svg                 the committed VIEW THE DEMO symbol (decoded == payload, qr_manifest.json)
Imagery: true colour B04/B03/B02 = grid / 10 000, one linear 1 to 99 % stretch over the three bands, gamma 1/1.35;
integer x6 nearest-neighbour upscaling (no resampling that invents pixels); window equality asserted before drawing.

Deviation from the brief, forced by the data: with all 443 columns across 216.5 mm the cited cell (grid col 225) lands at
x 110 mm, inside the brief's QR tile (x 106.5 to 193.5). The tile therefore sits top-left of the image (x 8 to 95);
row 212 can sit at most at 55 % of the height (the grid has 212 rows above it), not 60 %.
"""
import datetime as dt
import json
import re
import struct
import sys
from pathlib import Path

import numpy as np
from matplotlib import patheffects as pe
from matplotlib.collections import PatchCollection
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as S  # noqa: E402

ROOT = Path(S.ROOT)
DATA = ROOT / "research/repro/data"
sys.path.insert(0, str(ROOT / "research/repro/v11"))
import mutation_suite as R1  # noqa: E402

W, H = 216.5, 188.0
BLEED_R = 3.0
UPSCALE = 6
P_LO, P_HI, GAMMA = 1.0, 99.0, 1.35
NAME = "f1_scene"
LABELS = []
CLAIMS = {r["id"]: r for r in json.loads((ROOT / "research/v13/12_claims_map.json").read_text())["rows"]}
for ADD in sorted((ROOT / "research/v13").glob("12_claims_map_additions_*.json")):
    _d = json.loads(ADD.read_text())
    CLAIMS.update({r["id"]: r for r in (_d["rows"] if isinstance(_d, dict) else _d)})


def claimed(s, cid):
    """Assert the printed substring is one of the claim row's print[] strings (or a ' · ' join of them)."""
    pr = CLAIMS[cid]["print"]
    parts = [p.strip() for p in re.split(r" · |; ", s)]
    assert s in pr or all(any(p in q or q in p for q in pr) for p in parts), f"{s!r} not in claim {cid}: {pr}"
    return s


def T(ax, x, y, s, claim, **kw):
    LABELS.append({"text": s, "claim": claim, "x_mm": round(x, 2), "y_mm": round(y, 2), "pt": kw.get("fontsize")})
    return ax.text(x, y, s, **kw)


# ------------------------------------------------------------------ data
def grid(name):
    raw = (DATA / f"keylong_{name}.bin").read_bytes()
    assert raw[:8] == b"EMEMGRD1"
    w, h = struct.unpack_from("<II", raw, 8)
    return np.frombuffer(raw, dtype="<f4", offset=64).reshape(h, w).astype(float)


B2, B3, B4, B8 = (grid(b) for b in ("B02", "B03", "B04", "B08"))
NR, NC = B4.shape
assert (NC, NR) == (443, 453)
pw = json.loads((DATA / "v8/pixel_windows.json").read_text())
win = next(v for k, v in pw.items() if k.startswith("oj5cecci"))
oc, orr = win["window_origin_col_row"]                 # COG col/row of the window origin
R0, C0 = 210, 223                                      # the same window inside the signed grids
assert np.array_equal(B4[R0:R0 + 5, C0:C0 + 5], np.array(win["B04"]) - 1000)
assert np.array_equal(B8[R0:R0 + 5, C0:C0 + 5], np.array(win["B08"]) - 1000)
cc, cr = win["centre_col_row"]
CELL_R, CELL_C = R0 + int(np.floor(cr)) - orr, C0 + int(np.floor(cc)) - oc   # grid pixel of the record's pixel
assert (CELL_R, CELL_C) == (212, 225)
FACT = R1.FACT_D
VALUE = FACT["value"]
B8s, B4s = FACT["derivation"]["args"][R1.DN_IDX]
assert R1.ndvi(B8[CELL_R, CELL_C], B4[CELL_R, CELL_C], 0) == VALUE      # grid pixel reproduces the signed value
SCENE = FACT["derivation"]["args"][R1.SCENE_IDX]
m = re.match(r"S2([ABC])_MSI(L2A)_(\d{8})", SCENE)
SENSOR = f"Sentinel-2{m.group(1)} {m.group(2)}"
DATE = dt.date(1970, 1, 1) + dt.timedelta(days=FACT["tslot"])
assert DATE.strftime("%Y%m%d") == m.group(3)
DATE_S = f"{DATE.day} {DATE:%b %Y}"

rgb = np.dstack([B4, B3, B2]) / 10000.0
lo, hi = np.percentile(rgb, P_LO), np.percentile(rgb, P_HI)
tc = np.clip((rgb - lo) / (hi - lo), 0, 1) ** (1 / GAMMA)

PX = W / NC                                            # mm per 10 m pixel at print size
ROWS = int(np.ceil(H / PX))                            # rows that fill the height, from the top of the grid
TOP = 0
assert TOP + ROWS <= NR
img = np.repeat(np.repeat(tc[TOP:TOP + ROWS], UPSCALE, 0), UPSCALE, 1)
PPI = NC * UPSCALE / (W / 25.4)
assert PPI >= 300, PPI


def qr_modules(svg):
    """Module squares from a committed QR SVG (paths 'Mx yh1v1h-1z'); returns (size, list of (x, y))."""
    t = Path(svg).read_text()
    n = int(re.search(r'viewBox="0 0 (\d+) \d+"', t).group(1))
    return n, [(int(a), int(b)) for a, b in re.findall(r"M(\d+) (\d+)h1v1h-1z", t)]


QR = ROOT / "poster/fig/v13/qr_demo.svg"
qman = {q["slug"]: q for q in json.loads((ROOT / "poster/fig/v13/qr_manifest.json").read_text())}["demo"]
assert qman["decoded_equals_payload"] and qman["payload"] in QR.read_text()


# ------------------------------------------------------------------ draw
def main():
    fig = S.fig_mm(W, H)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    ax.imshow(img, extent=(0, NC * PX, ROWS * PX, 0), interpolation="none", zorder=0)

    # the cited cell: white 6 mm box, the record's own pixel outlined inside it
    cx, cy = (CELL_C - 0 + 0.5) * PX, (CELL_R - TOP + 0.5) * PX
    halo = [pe.Stroke(linewidth=2.2, foreground=(0, 0, 0, 0.45)), pe.Normal()]
    ax.add_patch(Rectangle((cx - 3, cy - 3), 6, 6, fill=False, ec="white", lw=1.6, zorder=3, path_effects=halo))
    ax.add_patch(Rectangle((cx - PX / 2, cy - PX / 2), PX, PX, fill=False, ec="white", lw=0.5, zorder=3))

    # strip: 62 % black, y 160 to 188
    y0 = 160.0
    ax.add_patch(Rectangle((0, y0), W, H - y0, fc=(0, 0, 0, 0.62), ec="none", zorder=4))
    ax.plot([cx, cx], [cy + 3.4, y0], color="white", lw=0.9, zorder=3, path_effects=halo, solid_capstyle="butt")
    ax.plot([cx], [y0], marker="o", ms=3.2, color="white", zorder=5)
    xs = 8.0
    # v13.10: the strip states what the marked pixel becomes; the record itself is identified in panels 1, 2 and 4.
    scene = json.loads((DATA / "v8/scene_sizes.json").read_text())["total_scene_bytes_all_blob_assets"]
    tok = json.loads((DATA / "v8/token_counts.json").read_text())["fact_token_ndvi"]
    assert f"{scene / 1e9:.2f}" == "2.02" and tok["chars"] == 84 and tok["cl100k"] == 46
    T(ax, xs, y0 + 3.0, claimed(f"{scene / 1e9:.2f} GB scene → {tok['chars']} characters", "WOW.scene"), "WOW.scene",
      fontsize=S.PT["body"], fontweight=700, color="white", va="top", zorder=6)
    T(ax, xs, y0 + 12.4, claimed("This pixel’s NDVI record, handed off in one text message.", "WOW.sms"), "WOW.sms",
      fontsize=S.PT["caption"], color="white", va="top", zorder=6)
    T(ax, xs, y0 + 19.8, claimed(f"{tok['chars']} characters, {tok['cl100k']} tokens; one SMS holds 160.", "WOW.sms"),
      "WOW.sms", fontsize=S.FLOOR, color=(1, 1, 1, 0.88), va="top", zorder=6)

    # scale bar: 1 km = 100 pixels of 10 m
    km = 100 * PX
    bx, by = W - BLEED_R - 8 - km, y0 - 6
    ax.add_patch(Rectangle((bx, by), km, 1.1, fc="white", ec="none", zorder=5, path_effects=halo))
    T(ax, bx + km / 2, by - 1.8, "1 km", "F1.scale", fontsize=S.FLOOR, fontweight=600, color="white",
      ha="center", va="bottom", zorder=6, path_effects=[pe.withStroke(linewidth=1.4, foreground=(0, 0, 0, 0.4))])

    # VIEW THE DEMO tile (top-left, see module docstring)
    tx, ty, tw = 8.0, 13.0, 87.0
    n, mods = qr_modules(QR)
    mod = tw / n
    cap = "Your phone becomes Agent B. Resolve the record and run its checks."
    lines = ["Your phone becomes Agent B.", "Resolve the record", "and run its checks."]
    assert " ".join(lines) == cap
    th = tw + 12 + 6.4 * len(lines) + 4
    ax.add_patch(FancyBboxPatch((tx, ty), tw, th, boxstyle="round,pad=0,rounding_size=1.2", fc="white", ec="none",
                                zorder=6))
    ax.add_collection(PatchCollection([Rectangle((tx + a * mod, ty + b * mod), mod, mod) for a, b in mods],
                                      fc="black", ec="none", zorder=7))
    T(ax, tx + tw / 2, ty + tw + 0.5, "TRY IT", "Q.view_demo", fontsize=28, family=S.MONO, fontweight=700,
      color=S.C["ink"], ha="center", va="top", zorder=8)
    for i, ln in enumerate(lines):
        T(ax, tx + tw / 2, ty + tw + 12.5 + 6.4 * i, ln, "Q.view_demo.caption", fontsize=S.PT["caption"],
          color=S.C["ink2"], ha="center", va="top", zorder=8)

    S.save(fig, NAME)
    meta = {"figure": NAME, "size_mm": [W, H], "bleed_right_mm": BLEED_R, "pixel_mm": PX, "upscale": UPSCALE,
            "ppi": round(PPI, 1), "rows_shown": [TOP, TOP + ROWS], "cell_grid_rc": [CELL_R, CELL_C],
            "cell_mm": [round(cx, 2), round(cy, 2)], "cell_height_fraction": round(cy / H, 3),
            "qr_tile_mm": [tx, ty, tw, round(th, 2)], "labels": LABELS}
    Path(S.OUT, f"{NAME}.labels.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
