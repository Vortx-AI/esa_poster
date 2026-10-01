"""F3 · Eight answers to one question (brief §E F3): 193.5 x 62 mm, panel 2.

One question (NDVI at the Keylong field, 25 Sep 2026), one constructed decision rule, eight values that real records,
archive pixels and handling rules produce. Every value is read from research/repro/v13/eight_answers.json, which
re-derives it from committed records and read-only public COG range reads (research/repro/v13/eight_answers.py); the
figure re-checks each value against its committed source to 1e-12 before drawing.

Encoding: one number line, same scale on both sides of a break; the rule as a vertical ink line; 6 mm dots, filled for a
signed record or an archive read, hollow for the reader rule or arithmetic applied to real pixel values; dot colour emem
for the right value, harm for the six wrong ones, oos for the impossible one; every wrong value carries the chip of the
check that stops it (depth-ramp tint by layer). Labels sit in three bands; every leader runs clear of other labels.

Deviation from the brief: the left segment ends at 0.50, not 0.55 (nothing lies between 0.48 and 1.10); the scale is the
same on both sides of the break, and the extra 30 mm separate the three answers within 0.02 of each other.
"""
import json
import re
import sys
from pathlib import Path

from matplotlib.patches import Circle, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as S  # noqa: E402

ROOT = Path(S.ROOT)
C, PT = S.C, S.PT
W, H = 193.5, 62.0
NAME = "f3_eight_answers"
MMPT = 72 / 25.4
LABELS = []
CLAIMS = {r["id"]: r for r in json.loads((ROOT / "research/v13/12_claims_map.json").read_text())["rows"]}
ADD = ROOT / "research/v13/12_claims_map_additions_F1-4.json"
if ADD.exists():
    CLAIMS.update({r["id"]: r for r in json.loads(ADD.read_text())["rows"]})


def T(ax, x, y, s, claim, **kw):
    assert claim in CLAIMS, f"no claim row {claim} for {s!r}"
    LABELS.append({"text": s, "claim": claim, "x_mm": round(x, 2), "y_mm": round(y, 2), "pt": kw.get("fontsize")})
    return ax.text(x, y, s, **kw)


def text_w(ax, s, **kw):
    t = ax.text(0, 0, s, **kw)
    w = t.get_window_extent(ax.figure.canvas.get_renderer()).width / ax.figure.dpi * 25.4
    t.remove()
    return w


# ------------------------------------------------------------------ data
EA = json.loads((ROOT / "research/repro/v13/eight_answers.json").read_text())
assert EA["all_rederived"], "eight_answers.json has a value that was not re-derived"
A = {r["key"]: r for r in EA["answers"]}
assert len(A) == 8
RULE = EA["rule"]["threshold"]
MM = json.loads((ROOT / "research/repro/v11/out/mutation_matrix.json").read_text())
assert float(re.search(r"<=\s*([0-9.]+)", MM["meta"]["rule"]).group(1)) == RULE
D = ROOT / "research/repro/data"


def close(a, b):
    return abs(a - b) <= 1e-12


# re-check each value against its committed source (the brief's asserts: recomputed from DNs, equal to 1e-12)
pc = next(v for k, v in json.loads((D / "v8/pixel_check.json").read_text()).items() if "oj5cecci" in k)
assert close(A["right"]["value"], pc["ndvi_floor_pixel"])
assert close(A["neighbour"]["value"], pc["ndvi_round_pixel"])
assert close(A["offset0"]["value"], (pc["B08"]["floor_DN"] - pc["B04"]["floor_DN"]) /
             (pc["B08"]["floor_DN"] + pc["B04"]["floor_DN"]))
cp = next(r for r in json.loads((D / "v11/cell_products.json").read_text()) if r["band"] == "indices.ndvi")
assert close(A["newer"]["value"], cp["value"])
ask = json.loads((D / "v11/ask_keylong.json").read_text())
assert close(A["place"]["value"], next(b for b in ask["band_observations_summary"]["bands"]
                                         if b["band"] == "indices.ndvi")["value"])
s2b = next(p for p in A["s2b"]["provenance"] if p["kind"] == "live")["DN_B08_B04"]
assert close(A["s2b"]["value"], (s2b[0] - s2b[1]) / (s2b[0] + s2b[1]))
dbl = next(p for p in A["double"]["provenance"] if p["kind"] == "live")
rb = dbl["raster_bands"]
r8, r4 = (v * rb["scale"] + rb["offset"] for v in dbl["DN_B08_B04"])
assert close(A["double"]["value"], (r8 - r4) / (r8 + r4))
res = json.loads((D / "v8/results.json").read_text())["b"]["claude-haiku-4-5"]["arms"]["R"]
assert A["rounded"]["print"] == "0.47" and res["decisions"]["IRRIGATE"] == res["n"]
S_ = EA["summary"]
assert (S_["crosses_rule"], S_["impossible"], S_["right"]) == (6, 1, 1)

# ------------------------------------------------------------------ geometry
X0, SEG1 = 2.0, (0.25, 0.50)
SCALE = 600.0                                   # mm per NDVI unit, both segments
GAP = 4.0
X1 = X0 + (SEG1[1] - SEG1[0]) * SCALE           # end of the left segment
SEG2 = (1.10, 1.15)
X2 = X1 + GAP


def xof(v):
    if v <= SEG1[1]:
        return X0 + (v - SEG1[0]) * SCALE
    assert SEG2[0] <= v <= SEG2[1]
    return X2 + (v - SEG2[0]) * SCALE


assert X2 + (SEG2[1] - SEG2[0]) * SCALE <= W - 2
Y_AX = 31.0
R = 3.0                                          # 6 mm dots
LAYER_OF = {"resolve": "L0", "scene id": "L1", "date": "L1", "re-read pixel": "L3", "catalogue offset": "L3",
            "asked coordinates": "L1", "range": "L2"}
for r in A.values():
    if r["check"]:
        assert LAYER_OF[r["check"]] == r["layer"], r
# label bands: (band, label left x in mm, anchor side). Bands: a above far, b above near, c below.
PLACE = {"place": ("a", 0.0), "s2b": ("a", 91.0), "double": ("a", 148.5),
         "offset0": ("b", 38.0), "right": ("b", 140.0),
         "neighbour": ("c", 0.0), "newer": ("c", 64.0), "rounded": ("c", 142.0)}
BAND_Y = {"a": 0.4, "b": 13.6, "c": 37.4}       # top of each band
CLAIM = {k: r["claim"] for k, r in A.items()}
# two pairs sit closer than one dot (0.47 / 0.4709: 0.0009 apart; 0.2966 / 0.3016: 0.005): each dot keeps its exact x
# and steps 3 mm toward its own label, so its edge still touches the axis
DY = {"right": -R, "rounded": R, "offset0": -R, "neighbour": R}


def colour(r):
    if r["decision"] == "invalid":
        return C["oos"], C["ink2"]
    if r["key"] == "right":
        return C["emem"], C["emem"]
    return C["harm"], C["harm_text"]


def chip(ax, x, y, s, layer, claim, h=5.6, size=S.FLOOR):
    tc = "white" if layer in ("L2", "L3") else C["ink"]
    w = text_w(ax, s, fontsize=size, fontweight=600) + 3.6
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=C[layer], ec="none",
                                zorder=5))
    T(ax, x + w / 2, y + h / 2 + 0.15, s, claim, fontsize=size, fontweight=600, color=tc, ha="center", va="center",
      zorder=6)
    return w


def main():
    fig = S.fig_mm(W, H)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    fig.canvas.draw()

    # axis: two segments, same scale, a clean break; minor ticks every 0.05
    ax.plot([X0, X1], [Y_AX, Y_AX], color=C["ink2"], lw=0.5 * MMPT, zorder=2, solid_capstyle="butt")
    ax.plot([X2, X2 + (SEG2[1] - SEG2[0]) * SCALE], [Y_AX, Y_AX], color=C["ink2"], lw=0.5 * MMPT, zorder=2,
            solid_capstyle="butt")
    for xb in (X1, X2):
        ax.plot([xb - 0.9, xb + 0.9], [Y_AX + 1.6, Y_AX - 1.6], color=C["ink2"], lw=0.5 * MMPT, zorder=2)
    for v in [0.25 + 0.05 * i for i in range(6)] + [1.10, 1.15]:
        ax.plot([xof(round(v, 2))] * 2, [Y_AX, Y_AX + 1.3], color=C["ink2"], lw=0.35 * MMPT, zorder=2)

    # the rule: vertical ink line through the axis zone, labelled on the irrigate side
    xr = xof(RULE)
    ax.plot([xr, xr], [BAND_Y["b"] + 1.0, BAND_Y["c"] - 0.6], color=C["ink"], lw=0.6 * MMPT, zorder=3)
    T(ax, xr - 1.4, BAND_Y["b"] + 6.6, "irrigate", "F3.rule", fontsize=S.FLOOR, color=C["ink"], ha="right",
      va="baseline", zorder=4)
    ax.annotate("", xy=(xr - 12.0, BAND_Y["b"] + 9.6), xytext=(xr - 0.6, BAND_Y["b"] + 9.6),
                arrowprops=dict(arrowstyle="-|>,head_length=0.36,head_width=0.16", lw=0.5 * MMPT, color=C["ink"],
                                shrinkA=0, shrinkB=0), zorder=4)

    # dots (draw hollow over filled so a ring stays visible on a coincident dot)
    order = sorted(A.values(), key=lambda r: r["dot"] == "hollow")
    for r in order:
        fc_, _ = colour(r)
        x = xof(r["value"])
        y = Y_AX + DY.get(r["key"], 0.0)
        if r["dot"] == "filled":
            ax.add_patch(Circle((x, y), R, fc=fc_, ec="white", lw=0.4 * MMPT, zorder=5))
        else:
            ax.add_patch(Circle((x, y), R - 0.45, fc="white", ec=fc_, lw=0.9 * MMPT, zorder=6))

    # labels: value (17 pt Bold) [+ chip on the same line when it fits], description (14 pt), chip line otherwise
    for key, (band, lx) in PLACE.items():
        r = A[key]
        _, tcol = colour(r)
        ty = BAND_Y[band]
        val = r["print"]
        vw = text_w(ax, val, fontsize=PT["caption"], fontweight=700)
        desc = r["label"]
        dw = text_w(ax, desc, fontsize=S.FLOOR)
        T(ax, lx, ty + 5.0, val, CLAIM[key], fontsize=PT["caption"], fontweight=700, color=tcol, va="baseline",
          zorder=6)
        if r["check"]:
            cs = f"{r['check']} {r['layer']}"
            cw = text_w(ax, cs, fontsize=S.FLOOR, fontweight=600) + 3.6
            chip(ax, lx + vw + 2.0, ty + 0.6, cs, r["layer"], "F3.chips")
        T(ax, lx, ty + 10.6, desc, CLAIM[key], fontsize=S.FLOOR, color=C["ink2"], va="baseline", zorder=6)
        # leader from the dot to the label's anchor
        x = xof(r["value"])
        bw = max(dw, vw + (2 + cw if r["check"] else 0))
        ax_x = min(max(x, lx + 1.0), lx + bw - 1.0)
        yd = Y_AX + DY.get(key, 0.0)
        if band == "c":
            p0, p1 = (x, yd + R + 0.4), (ax_x, ty - 0.4)
        else:
            p0, p1 = (x, yd - R - 0.4), (ax_x, ty + 12.2)
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=C["ink2"], lw=0.35 * MMPT, zorder=1)
        LABELS[-1]["box_mm"] = [round(lx, 1), round(ty, 1), round(bw, 1)]

    # legend + rule, two lines at 14 pt (glyphs drawn as patches)
    ly = 53.8
    T(ax, 0, ly, f"test rule: irrigate if NDVI ≤ {RULE}", "S.threshold", fontsize=S.FLOOR, color=C["ink"],
      va="center")
    lx = text_w(ax, f"test rule: irrigate if NDVI ≤ {RULE}", fontsize=S.FLOOR) + 7
    ax.add_patch(Circle((lx + 1.8, ly), 1.8, fc=C["ink2"], ec="none"))
    T(ax, lx + 5, ly, "a signed record or an archive read", "F3.legend", fontsize=S.FLOOR, color=C["ink2"],
      va="center")
    ly2 = ly + 5.8
    ax.add_patch(Circle((1.8, ly2), 1.45, fc="white", ec=C["ink2"], lw=0.7 * MMPT))
    T(ax, 5, ly2, "the reader rule or arithmetic applied to real pixel values", "F3.legend", fontsize=S.FLOOR,
      color=C["ink2"], va="center")

    S.save(fig, NAME)
    meta = {"figure": NAME, "size_mm": [W, H], "axis": {"segments": [SEG1, SEG2], "mm_per_unit": SCALE},
            "rule": RULE, "values": {k: r["value"] for k, r in A.items()}, "labels": LABELS}
    Path(S.OUT, f"{NAME}.labels.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
