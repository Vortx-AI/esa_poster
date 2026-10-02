"""D1 · Threat channel (193.5 x 30 mm, brief §C threat model and §E small diagrams).

A -> relay -> B. The relay (harm tint) rewrites what it carries and replays old records; the two anchors B holds sit
outside its reach: the pinned key and the open archive. Below, three trust stripes with their status words, coloured
by the verification-depth ramp and draining to hatch. No numbers are drawn; every string is figure text of the brief."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, PT, ROOT, fig_mm, save  # noqa: E402
import matplotlib.text  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle  # noqa: E402

W, H = 193.5, 30.0
J = lambda p: json.load(open(os.path.join(ROOT, p)))
WIT = J("research/v13/evidence/ladder/witnesses.json")
assert WIT["independent_operator_count"] == 1          # T.oneop: "All keys today are one operator's."
IDS = ["T.can", "T.pinned", "T.oneop", "A13.threat"]


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
fig.set_dpi(300)                      # measure text at the dpi it is rendered at
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
F, PTMM = PT["floor"], 0.3528


def T(x, y, s, color=C["ink"], ha="left", weight="normal", size=F, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, ha=ha, va="center", fontweight=weight, zorder=6, **kw)


def ext(t):
    fig.canvas.draw(); e = t.get_window_extent()
    inv = ax.transData.inverted()
    return inv.transform((e.x0, e.y0))[0], inv.transform((e.x1, e.y0))[0]


def arrow(x0, x1, y, col=C["ink2"]):
    ax.plot([x0, x1 - 2.0], [y, y], color=col, lw=0.6 / PTMM, solid_capstyle="butt", zorder=3)
    ax.add_patch(Polygon([(x1 - 2.2, y - 1.1), (x1, y), (x1 - 2.2, y + 1.1)], closed=True, fc=col, ec="none", zorder=3))


def agent(x, y, letter, filled):
    s = 8.0
    col = C["agentB"] if filled else C["agentA"]
    ax.add_patch(FancyBboxPatch((x, y - s / 2), s, s, boxstyle="round,pad=0,rounding_size=1.8",
                                fc=col if filled else "white", ec=col, lw=0.85 / PTMM, zorder=4))
    T(x + s / 2, y + 0.1, letter, "white" if filled else col, ha="center", weight="bold", size=17)


def hatch(x, y, w, h, z=2):
    ax.add_patch(Rectangle((x, y), w, h, fc=C["oos_bg"], ec="none", zorder=z))
    ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=C["oos"], lw=0, hatch="////", zorder=z))


plt_rc = __import__("matplotlib").rcParams
plt_rc["hatch.color"] = C["oos"]; plt_rc["hatch.linewidth"] = 0.9

YC = 7.6                                      # channel centre line
agent(0.0, YC, "A", False)
RX0 = 12.0
ls = [T(RX0 + 2.4, YC + dy, s, C["harm_text"]) for dy, s in
      ((-4.95, "rewrites value, cell, date,"), (0.0, "source, record, reference;"), (4.95, "replays old records"))]
RX1 = max(ext(t)[1] for t in ls) + 2.4
ax.add_patch(FancyBboxPatch((RX0, YC - 7.45), RX1 - RX0, 14.6, boxstyle="round,pad=0,rounding_size=1.5",
                            fc=C["harm_tint"], ec=C["harm"], lw=0.55 / PTMM, zorder=2))
arrow(8.4, RX0 - 0.4, YC)
BX = RX1 + 3.6
arrow(RX1 + 0.4, BX - 0.4, YC)
agent(BX, YC, "B", True)
# B's two anchors, outside the relay's reach
PX = BX + 12.0
ax.plot([BX + 8.0, PX - 2.4], [YC, YC], color=C["agentB"], lw=0.35 / PTMM, zorder=3)
for y, s in ((YC - 4.95, "pinned key (DNS TXT, did.json, JWKS)"), (YC, "open archive (COG)")):
    ax.plot([PX - 2.4, PX - 2.4, PX - 1.0], [YC, y, y], color=C["agentB"], lw=0.35 / PTMM, zorder=3)
    ax.add_patch(Circle((PX + 0.2, y), 1.1, fc=C["agentB"], ec="none", zorder=4))
    t = T(PX + 2.0, y, s, C["ink"])
    assert ext(t)[1] <= W - 0.3, s
T(PX + 2.0, YC + 4.95, "All keys today are one operator's.", C["ink2"])

# three trust stripes
ys = [17.52, 22.5, 27.48]
SW = 9.0
rows = [("cryptographic: the exact record bytes", "CHECKABLE", C["emem"], "full"),
        ("source: which file was read", "PARTIAL", C["L3"], "half"),
        ("measurement: sensor and product", "INHERITED", C["ink2"], "hatch")]
for y, (lab, word, col, kind) in zip(ys, rows):
    if kind == "full":
        ax.add_patch(Rectangle((0, y - 1.8), SW, 3.6, fc=C["L2"], ec="none", zorder=2))
    elif kind == "half":
        ax.add_patch(Rectangle((0, y - 1.8), SW / 2, 3.6, fc=C["L0"], ec="none", zorder=2))
        hatch(SW / 2, y - 1.8, SW / 2, 3.6)
    else:
        hatch(0, y - 1.8, SW, 3.6)
    t = T(SW + 2.2, y, lab, C["ink"])
    t2 = T(ext(t)[1] + 1.2, y, "·", C["ink"])
    T(ext(t2)[1] + 1.2, y, word, col, weight="semibold")

claims_gate(fig, IDS)
save(fig, "d_threat")
