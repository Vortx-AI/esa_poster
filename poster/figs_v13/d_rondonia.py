"""D2 · Rondônia point lattice and the auditor card for cell A (193.5 x 56 mm, brief §C panel 9, §E small diagrams).

The 10 x 10 lattice of case_rondonia_eudr.json drawn as point symbols (north up, 740 m apart), coded by shape and
colour: EUDR-rule flag (forest 2020 in JRC GFC2020 and Hansen loss after 2020) a vermillion disc; forest with no
later loss a blue disc; cleared 2001 to 2020 an ink triangle; not forest a grey dot; maps disagree an amber diamond.
Card: cell A's five inputs, each with the first 8 characters of its signed record's address.
Mandatory line: point samples, not parcel polygons; not a regulatory determination."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, PT, MONO, ROOT, fig_mm, save  # noqa: E402
import matplotlib.text  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Polygon  # noqa: E402

W, H = 193.5, 56.0
J = lambda p: json.load(open(os.path.join(ROOT, p)))
D = J("research/repro/v12/data/case_rondonia_eudr.json")
ROWS, G = D["rows"], D["grid"]
assert len(ROWS) == G["rows"] * G["cols"] == 100
FLAG, DIS = "eudr_flag_forest_2020_loss_after_2020", "loss_after_2020_on_gfc2020_non_forest"
FOR, CLR, NOT = "forest_2020_no_later_loss", "cleared_2001_2020", "not_forest_2020_no_hansen_loss"
cnt = {k: sum(r["eudr_category"] == k for r in ROWS) for k in (FLAG, FOR, CLR, NOT, DIS)}
assert cnt == {FLAG: D["category_counts"][FLAG], FOR: D["category_counts"][FOR], CLR: D["category_counts"][CLR],
               NOT: D["category_counts"][NOT], DIS: D["category_counts"][DIS]}
assert all(r["all_verified"] for r in ROWS)
n_rec = sum(1 for r in ROWS for k in r if k.endswith("|fact_cid") and r[k])
assert n_rec == 600
for r in ROWS:   # the rule, re-applied to the signed values
    flag = r["jrc_gfc2020.forest_2020"] == 1 and r["hansen.loss_year"] > 2020
    assert flag == (r["eudr_category"] == FLAG), r["cell"]
A = sorted([r for r in ROWS if r["eudr_category"] == FLAG], key=lambda r: (r["row"], r["col"]))[0]
assert A["cell"] == "defi.zb391.taza.zcc31"
flags = [r for r in ROWS if r["eudr_category"] == FLAG]
tmf_agree = sum(1 for r in flags if r["jrc_tmf.deforestation_year"] > 2020)
assert (tmf_agree, len(flags)) == (1, 3)                       # RO.tmf: TMF agrees on 1 of 3 flags
SPACING_M = 740                                                # grid.note: nodes are about 740 m apart
assert "740 m" in G["note"]
IDS = ["RO.grid", "RO.cats", "RO.cardA", "RO.must", "A14.card"]


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


def T(x, y, s, color=C["ink"], ha="left", weight="normal", size=F, family=None):
    kw = dict(fontsize=size, color=color, ha=ha, va="center", fontweight=weight, zorder=6)
    if family:
        kw["family"] = family
    return ax.text(x, y, s, **kw)


def ext(t):
    fig.canvas.draw(); e = t.get_window_extent()
    return ax.transData.inverted().transform((e.x1, e.y0))[0]


def sym(kind, x, y, scale=1.0):
    if kind == FLAG:
        ax.add_patch(Circle((x, y), 2.25 * scale, fc=C["harm"], ec="white", lw=0.8, zorder=5))
    elif kind == FOR:
        ax.add_patch(Circle((x, y), 1.45 * scale, fc=C["emem"], ec="none", zorder=4))
    elif kind == CLR:
        h = 2.9 * scale
        ax.add_patch(Polygon([(x - h / 1.73, y + h / 3), (x + h / 1.73, y + h / 3), (x, y - 2 * h / 3)], closed=True,
                             fc=C["ink"], ec="none", zorder=4))
    elif kind == NOT:
        ax.add_patch(Circle((x, y), 0.75 * scale, fc=C["oos"], ec="none", zorder=4))
    elif kind == DIS:
        d = 2.1 * scale
        ax.add_patch(Polygon([(x, y - d), (x + d, y), (x, y + d), (x - d, y)], closed=True, fc=C["incident"],
                             ec=C["incident_text"], lw=0.5, zorder=5))


# lattice: north up, west left
P, X0, Y0 = 4.5, 3.0, 2.9
gx = lambda c: X0 + c * P
gy = lambda r: Y0 + r * P
for r in ROWS:
    sym(r["eudr_category"], gx(r["col"]), gy(r["row"]))
T(gx(A["col"]), gy(A["row"]) + 0.1, "A", "white", ha="center", weight="bold")
# spacing bracket under the lattice
yb = gy(9) + 3.6
for c in (8, 9):
    ax.plot([gx(c), gx(c)], [yb - 0.7, yb + 0.7], color=C["ink2"], lw=0.35 / PTMM, zorder=3)
ax.plot([gx(8), gx(9)], [yb, yb], color=C["ink2"], lw=0.35 / PTMM, zorder=3)
T(gx(8) - 1.2, yb, f"{SPACING_M} m", C["ink2"], ha="right")
# north tick
ax.plot([gx(0), gx(0)], [yb + 1.9, yb - 1.9], color=C["ink2"], lw=0.35 / PTMM, zorder=3)
ax.plot([gx(0) - 1.0, gx(0), gx(0) + 1.0], [yb - 0.6, yb - 1.9, yb - 0.6], color=C["ink2"], lw=0.35 / PTMM, zorder=3)
T(gx(0) + 1.6, yb, "N", C["ink2"])

# legend
LX = 56.0
order = [(FLAG, f"forest 2020 (GFC2020) + loss after 2020 (Hansen): {cnt[FLAG]}", C["harm_text"], "semibold"),
         (FOR, f"forest, no later loss: {cnt[FOR]}", C["ink"], "normal"),
         (CLR, f"cleared 2001 to 2020: {cnt[CLR]}", C["ink"], "normal"),
         (NOT, f"not forest: {cnt[NOT]}", C["ink"], "normal"),
         (DIS, f"maps disagree: {cnt[DIS]}", C["incident_text"], "normal")]
for i, (k, lab, col, wt) in enumerate(order):
    y = 2.9 + i * 5.0
    sym(k, LX + 2.3, y, 0.85 if k == FLAG else 1.0)
    T(LX + 6.0, y, lab, col, weight=wt)

# auditor card for cell A
CX, CY, CW, CH = LX, 26.4, W - LX - 0.4, 23.0
ax.add_patch(FancyBboxPatch((CX, CY), CW, CH, boxstyle="round,pad=0,rounding_size=1.6", fc="white", ec=C["harm"],
                            lw=0.55 / PTMM, zorder=2))
sym(FLAG, CX + 4.2, CY + 4.2, 0.85)
T(CX + 4.2, CY + 4.3, "A", "white", ha="center", weight="bold")
t = T(CX + 8.0, CY + 4.2, "cell A", C["ink"], weight="semibold")
T(ext(t) + 2.0, CY + 4.2, A["cell"], C["emem"], family=MONO)
card = [(f"Hansen loss {A['hansen.loss_year']}", "hansen.loss_year"),
        (f"tree cover 2000 {A['hansen.tree_cover_2000']} %", "hansen.tree_cover_2000"),
        ("GFC2020 V4 forest" if A["jrc_gfc2020.forest_2020"] == 1 else "GFC2020 V4 not forest", "jrc_gfc2020.forest_2020"),
        (f"TMF {A['jrc_tmf.deforestation_year']}", "jrc_tmf.deforestation_year"),
        (f"CCI {A['esa_cci_biomass.agb_t_per_ha_2022']:.0f} t/ha", "esa_cci_biomass.agb_t_per_ha_2022")]
cols = [(CX + 2.4, [0, 1, 2]), (CX + 81.6, [3, 4])]
for x, idx in cols:
    for j, i in enumerate(idx):
        y = CY + 9.6 + j * 5.0
        lab, key = card[i]
        t = T(x, y, lab, C["ink"])
        T(ext(t) + 1.8, y, A[key + "|fact_cid"][:8], C["muted"], family=MONO)
T(CX + 81.6, CY + 19.6, "each a signed record", C["ink2"])
# the mandatory scope line
T(0, H - 2.7, "Point samples, not parcel polygons; not a regulatory determination.", C["ink"], weight="bold")

claims_gate(fig, IDS)
save(fig, "d_rondonia")
