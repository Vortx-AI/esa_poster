"""F12 · EMEM relies on these layers (261 x 48 mm, brief §E F12; report 04 §1.2).

Seven quiet lanes, each a verb, the system(s) and the unit it identifies, from the archive (FIND, bottom) to the
judgement of a claim (JUDGE, top). EMEM is not a lane: one blue thread at the right touches FIND and RUN (cite),
CARRY (hand off) and JUDGE (resolve · re-hash · re-read). No ticks or crosses against other systems.
Labels are the claims-map rows PA.* (sourced in research/v13/04_prior_art_and_field.md §2)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, PT, ROOT, fig_mm, save  # noqa: E402
import matplotlib.text  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

W, H = 261.0, 48.0
J = lambda p: json.load(open(os.path.join(ROOT, p)))
MAP = {r["id"]: r for r in J("research/v13/12_claims_map.json")["rows"]}
LANES = []  # (verb, systems, unit) read from the claims rows, top to bottom
for rid in ("PA.geoguard", "PA.carry", "PA.rag", "PA.c2pa", "PA.prov", "PA.openeo", "PA.stac"):
    verb, systems, unit = MAP[rid]["print"][0].split(" · ")
    LANES.append((verb, systems, unit))
assert [l[0] for l in LANES] == ["JUDGE", "CARRY", "RETRIEVE", "SIGN FILES", "RECORD LINEAGE", "RUN", "FIND"]
TOUCH = {"FIND": "cite", "RUN": "cite", "CARRY": "hand off", "JUDGE": "resolve · re-hash · re-read"}
FOOT = "Same pattern in software supply chains: Sigstore, RFC 9162, SCITT (RFC 9943). Closest agent memory: ARC (arXiv 2607.25066)."
assert all(p in FOOT for p in MAP["PA.credit"]["print"])
IDS = ["PA.stac", "PA.openeo", "PA.prov", "PA.c2pa", "PA.rag", "PA.carry", "PA.geoguard", "A12.thread"]


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
F, S, PTMM = PT["floor"], 15, 0.3528


def T(x, y, s, size=F, color=C["ink"], ha="left", va="center", weight="normal", **kw):
    return ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight, zorder=6, **kw)


LH, Y0 = 6.6, 0.6
XV, XS, XU, XE = 2.0, 47.5, 111.0, 172.0     # verb, system, unit columns; lane end
XT = 178.0                                    # the thread
yc = {}
for i, (verb, systems, unit) in enumerate(LANES):
    y = Y0 + i * LH
    yc[verb] = y + LH / 2
    ax.add_patch(Rectangle((0, y + 0.25), XE, LH - 0.5, fc=C["na"] if i % 2 == 0 else C["oos_bg"], ec="none", zorder=1))
    T(XV, y + LH / 2, verb, F, C["ink2"], weight="semibold")
    T(XS, y + LH / 2, systems, S, C["ink"], weight="medium")
    T(XU, y + LH / 2, unit, F, C["ink2"])
# the thread: one blue line from FIND to JUDGE, a node and a stub where it touches a lane
ytop, ybot = yc["JUDGE"], yc["FIND"]
ax.plot([XT, XT], [ytop, ybot], color=C["emem"], lw=1.8 / PTMM, solid_capstyle="round", zorder=3)
for verb, word in TOUCH.items():
    y = yc[verb]
    ax.plot([XE, XT], [y, y], color=C["emem"], lw=0.9 / PTMM, solid_capstyle="butt", zorder=3)
    ax.add_patch(Circle((XT, y), 1.7, fc=C["emem"], ec="white", lw=1.0, zorder=4))
    T(XT + 3.6, y, word, F, C["emem"], weight="semibold")
T(XT + 3.6, (yc["SIGN FILES"] + yc["RECORD LINEAGE"]) / 2 - 0.2, "EMEM: is this the observation\nthe sender cited?", S,
  C["emem"], weight="semibold", linespacing=1.15)
# FOOT (14 pt, 124 characters) needs 2 lines at 261 mm and does not fit under seven lanes in 48 mm: the HTML sets it.

claims_gate(fig, IDS)
save(fig, "f12_prior_art")
