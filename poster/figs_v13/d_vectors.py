"""D4 · Vectors are records too: two vector cards (193.5 x 24 mm, brief §C panel 10, §E small diagrams).

Each card draws the signed vector itself as a barcode (one bar per value, grey by value, 2nd to 98th percentile) from
research/v13/evidence/critic/cell.json. Prithvi-EO-2.0 names its checkpoint digest inside the hashed record (the
derivation args carry the same blake2b digest the server reports); the TESSERA record names only a path and a year."""
import json, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, PT, MONO, ROOT, fig_mm, save  # noqa: E402
import matplotlib.text  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

W, H = 193.5, 24.0
J = lambda p: json.load(open(os.path.join(ROOT, p)))
FACTS = {f["band"]: f for f in J("research/v13/evidence/critic/cell.json")["facts"]}
P, G = FACTS["prithvi_eo2"], FACTS["geotessera"]
ck = P["served_via"]["model_blake2b_hex"]
assert ck == P["derivation"]["args"]["args"][4] and len(P["value"]) == 1024
src = G["sources"][0]["id"]
assert "/npy/v1/2024/" in src and len(G["value"]) == 128 and G["derivation"]["args"][2] == 2024
assert not any(re.fullmatch(r"[0-9a-f]{32,}", str(a)) for a in G["derivation"]["args"])   # no checkpoint digest
CARDS = [("prithvi_eo2", P["value"], f"checkpoint {ck[:8]}… (hashed)", C["emem"], "solid"),
         ("geotessera", G["value"], "…/npy/v1/2024/… (no checkpoint)", C["oos"], (0, (3, 2)))]
IDS = ["V.prithvi", "V.tessera", "A15.vec"]


def claims_gate(fig, ids):
    rows = J("research/v13/12_claims_map.json")["rows"] + J("research/v13/12_claims_map_additions_F9-12.json")["rows"]
    rows = {r["id"]: r for r in rows}
    missing = [i for i in ids if i not in rows]
    assert not missing, missing
    allowed = " | ".join(s for i in ids for s in rows[i]["print"])
    num = re.compile(r"\d[\d,]*(?:\.\d+)?")
    ok_tokens = set(num.findall(allowed))
    for t in fig.findobj(matplotlib.text.Text):
        s = t.get_text()
        if not s.strip() or not t.get_visible():
            continue
        assert "\u2014" not in s, f"em dash: {s!r}"
        assert not re.search(r"(?<!\d)\u2013|\u2013(?!\d)", s), f"en dash outside a range: {s!r}"
        for n in num.findall(s):
            assert n in ok_tokens, f"unsourced number {n!r} in {s!r}"


fig = fig_mm(W, H)
fig.set_dpi(300)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
F, PTMM = PT["floor"], 0.3528
GREY = LinearSegmentedColormap.from_list("ink", ["#FFFFFF", C["ink"]])


def T(x, y, s, color=C["ink"], weight="normal", family=None, ha="left"):
    kw = dict(fontsize=F, color=color, ha=ha, va="center", fontweight=weight, zorder=6)
    if family:
        kw["family"] = family
    return ax.text(x, y, s, **kw)


def ext(t):
    fig.canvas.draw(); e = t.get_window_extent()
    return ax.transData.inverted().transform((e.x1, e.y0))[0]


CW, GAP = (W - 5.0) / 2, 5.0
for k, (band, vec, foot, ec, ls) in enumerate(CARDS):
    x0 = k * (CW + GAP)
    ax.add_patch(FancyBboxPatch((x0 + 0.3, 0.3), CW - 0.6, H - 0.6, boxstyle="round,pad=0,rounding_size=1.6",
                                fc="white", ec=ec, lw=0.55 / PTMM, ls=ls, zorder=1))
    t = T(x0 + 3.0, 4.0, band, C["ink"], weight="semibold", family=MONO)
    T(ext(t) + 1.6, 4.0, f"· {len(vec):,} values", C["ink2"])
    v = np.asarray(vec, float)
    lo, hi = np.percentile(v, 2), np.percentile(v, 98)
    z = np.clip((v - lo) / (hi - lo), 0, 1)[None, :]
    # integer nearest-neighbour upscale so the embedded raster is >= 300 ppi at its 187.4 mm width (print gate)
    rep = int(np.ceil(300 * (187.4 / 25.4) / z.shape[1]))
    z = np.repeat(np.repeat(z, max(rep, 1), axis=1), 40, axis=0)
    ax.imshow(z, cmap=GREY, vmin=0, vmax=1, aspect="auto", interpolation="nearest",
              extent=(x0 + 3.0, x0 + CW - 3.0, 14.4, 7.4), zorder=2)
    T(x0 + 3.0, 19.4, foot, ec if k == 0 else C["ink2"], weight="medium" if k == 0 else "normal",
      family=None)
ax.set_xlim(0, W); ax.set_ylim(H, 0)

claims_gate(fig, IDS)
save(fig, "d_vectors")
