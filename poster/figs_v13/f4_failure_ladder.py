"""F4 · Our own errors name the checks: the failure ladder (brief §E F4): 193.5 mm wide, panel 3; the height follows
the rungs' content (review fix 18 moved the rotated side rail into the panel's scope line).

Eight rungs, bottom (rung 1, stopped at the handoff by resolving the reference) to top (rung 8, stopped by nothing):
the higher the rung, the more checks the wrong value passes. Each rung: what happened, its consequence (20 pt Bold
harm-text), the same class documented elsewhere (14 pt), the catching check as a depth-ramp chip and a status tag. The
left 3 mm amber bar marks a real incident (in emem or in our tests); the right 3 mm bar repeats the catching layer in the
depth ramp, so the ladder climbs from light to dark like the verification ladder F8, and ends hatched. Rung 2's
consequence breaks after "twice;" (review fix 5); rung 5 is "Wrong scale or offset" (fix 4).

Every consequence and status string is checked against a claims row (research/v13/12_claims_map.json, or the additions
file research/v13/12_claims_map_additions_F1-4.json); every number inside them is read from its data file here.
Deviation from the brief: rungs are 26 to 34 mm (content height), not a uniform 30 mm, so no text wraps into a chip.
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

from matplotlib.collections import LineCollection
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as S  # noqa: E402

ROOT = Path(S.ROOT)
C, PT = S.C, S.PT
W, H = 193.5, 262.0                           # H is trimmed to the rungs' content below (the side rail moved to the panel 3 scope line)
NAME = "f4_failure_ladder"
MMPT = 72 / 25.4
PTMM = 25.4 / 72
LABELS = []
CLAIMS = {r["id"]: r for r in json.loads((ROOT / "research/v13/12_claims_map.json").read_text())["rows"]}
ADD = ROOT / "research/v13/12_claims_map_additions_F1-4.json"
if ADD.exists():
    CLAIMS.update({r["id"]: r for r in json.loads(ADD.read_text())["rows"]})
D = ROOT / "research/repro/data"
EV = ROOT / "research/v13/evidence/failure_modes"


def in_claim(s, cid):
    """The printed string equals a print[] entry of the row, or is a '; ' join of entries."""
    pr = CLAIMS[cid]["print"]
    ok = s in pr or all(p in pr for p in s.split("; "))
    assert ok, f"{s!r} is not a print string of {cid}: {pr}"
    return s


def T(ax, x, y, s, claim, **kw):
    assert claim in CLAIMS, f"no claim row {claim} for {s!r}"
    LABELS.append({"text": s, "claim": claim, "x_mm": round(x, 2), "y_mm": round(y, 2), "pt": kw.get("fontsize")})
    return ax.text(x, y, s, **kw)


def text_w(ax, s, **kw):
    t = ax.text(0, 0, s, **kw)
    w = t.get_window_extent(ax.figure.canvas.get_renderer()).width / ax.figure.dpi * 25.4
    t.remove()
    return w


def wrap(ax, s, width, **kw):
    """Greedy wrap at width; an explicit newline in s forces a break (rung 2 breaks after 'twice;')."""
    lines = []
    for para in s.split("\n"):
        words, cur = para.split(" "), ""
        for w_ in words:
            trial = (cur + " " + w_).strip()
            if text_w(ax, trial, **kw) <= width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w_
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ numbers, each read from its file
res = json.loads((D / "v8/results.json").read_text())["b"]["claude-haiku-4-5"]["arms"]["R"]
EA = {r["key"]: r for r in json.loads((ROOT / "research/repro/v13/eight_answers.json").read_text())["answers"]}
assert all(r["rederived"] for r in EA.values())
bg = json.loads((D / "contra_bengaluru.json").read_text())["contradictions"][0]["attestations"]
bg_vals = sorted({a["value"] for a in bg}, key=lambda v: min(a["signed_at"] for a in bg if a["value"] == v))
assert len(bg_vals) == 2
prev = json.loads((D / "v8/prevalence_summary.json").read_text())["pre"]
chlog = (EV / "CHANGELOG_18adb67.md").read_text().splitlines()
wp = re.search(r"people per pixel, (\d+\.\d+)x low", chlog[60]).group(1)          # CHANGELOG line 61
assert "signed the far side's out-of-image pixels as 0" in chlog[52]                 # line 53
fix_px = re.search(r"before the pixel fix \((\d{4}-\d\d-\d\d)T", "\n".join(chlog)).group(1)
assert fix_px in chlog[46] or fix_px in chlog[53]                                    # lines 47 / 54
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def dmy(iso):
    y, m, d = (int(x) for x in iso[:10].split("-"))
    return f"{d} {MONTHS[m - 1]} {y}"


try:   # hair-salon fix: emem commit 0edf574 (read-only git); fall back to the claims row when the clone is absent
    salon = subprocess.run(["git", "-C", "/home/user/vortx-ai/emem", "log", "-1", "--format=%cI", "0edf574"],
                           capture_output=True, text=True, check=True).stdout.strip()
    fix_salon = dmy(salon)
except Exception:  # pragma: no cover
    fix_salon = next(p for p in CLAIMS["F.thing"]["print"] if p.startswith("fixed "))[6:]

f = lambda v, n: f"{v:.{n}f}"                                                        # noqa: E731
R_ = [  # (n, title, what, elsewhere, consequence, check chips [(text, layer)], status) ; claims per field
    (1, "Lost in the handoff",
     (in_claim(f"{EA['rounded']['print']} for {EA['right']['print']}", "F.lost"), "F.lost"),
     ("F.lost.out", None), (in_claim(f"{res['decisions']['IRRIGATE']} of {res['n']} receivers irrigated", "F.lost"),
                            "F.lost"), [("resolve the reference · L0", "L0")], "test rule"),
    (2, "Wrong date", (in_claim("asked 23 Sep, served 25 Sep", "F.date"), "F.date"), ("F.date.out", None),
     (in_claim("; ".join(CLAIMS["F.date"]["print"][1:3]), "F.date").replace("; ", ";\n"), "F.date"),
     [("bind the date · L1", "L1")],
     "open"),
    (3, "Wrong place", (in_claim("coordinates given, town point answered", "F.place"), "F.place"), ("F.place.out", None),
     (in_claim(f"{round(EA['place']['distance_m'])} m; NDVI {f(EA['place']['value'], 2)} for the field's "
               f"{f(EA['newer']['value'], 2)}", "F.place"), "F.place"), [("asked coordinates · L1", "L1")],
     "fix unconfirmed"),
    (4, "Wrong version", (f"{bg_vals[0]:.1f} m, then {f(bg_vals[1], 2)} m, one band name", "F.version"),
     ("F.version.out", None), ("an earlier citation looks wrong", "F4.version.consequence"),
     [("source + as-of · L1", "L1")], "both kept"),
    (5, "Wrong scale or offset", (in_claim(f"WorldPop signed per pixel, not per km²: {wp}× low", "F.worldpop"),
                        "F.worldpop"), ("F.scale.out", None),
     (in_claim(f"one pixel: {EA['right']['print']}, {EA['offset0']['print']}, {EA['double']['print']} under three "
               "offset rules", "F.scale"), "F.scale"), [("recompute · L2", "L2"), ("catalogue · L3", "L3")],
     "fixed"),
    (6, "Missing data signed as 0", (in_claim("off-tile pixels signed as 0", "F.missing"), "F.missing"),
     ("F.missing.out", None), (in_claim("a forest-loss screen passes", "F.missing"), "F.missing"),
     [("re-read · L3", "L3")], "fixed"),
    (7, "Wrong pixel, signed", ("the reader rounded the pixel index", "F4.pixel.what"), ("F.pixel.out", "; "),
     (f"{prev['matches_round_not_floor']} of {prev['n']} sampled records", "F.pixel"), [("re-read only · L3", "L3")],
     in_claim(f"fixed {dmy(fix_px)}", "F.pixel")),
    (8, "Wrong thing", (in_claim("“this image” resolved to a hair salon in Ontario".replace("“", '"')
                                 .replace("”", '"'), "F.thing"), "F.thing"), ("F.thing.out", None),
     (in_claim("receipt, Merkle proof and state chain all valid", "F.thing"), "F.thing"), [("none · L4", "L4")],
     in_claim(f"fixed {fix_salon}", "F.thing")),
]
assert f"{bg_vals[0]:.1f} m" in CLAIMS["F.version"]["print"] and f"{f(bg_vals[1], 2)} m" in CLAIMS["F.version"]["print"]
assert f"{prev['matches_round_not_floor']} of {prev['n']}" in CLAIMS["F.pixel"]["print"]
for r in R_:
    st = r[6]
    assert st in CLAIMS[f"F4.status.{r[0]}"]["print"], (r[0], st)


# ------------------------------------------------------------------ draw
def hatch(ax, x, y, w, h, pitch=1.6, z=3):
    ax.add_patch(Rectangle((x, y), w, h, fc=C["oos_bg"], ec="none", zorder=z))
    segs, step, k = [], pitch * math.sqrt(2), -h
    while k < w:
        t0, t1 = max(0.0, -k), min(h, w - k)
        if t1 > t0:
            segs.append([(x + k + t0, y + h - t0), (x + k + t1, y + h - t1)])
        k += step
    ax.add_collection(LineCollection(segs, colors=C["oos"], linewidths=0.35 * MMPT, zorder=z + 0.1))


def main():
    global H
    fig = S.fig_mm(W, H)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    fig.canvas.draw()
    X_T, X_R = 6.0, 190.0                          # text left, rung right edge (bar 187 to 190)
    TXT_W = X_R - 4.5 - X_T
    sz = dict(title=PT["caption"], what=15, cons=PT["label"], out=S.FLOOR)
    lead = {k: v * PTMM * 1.05 for k, v in sz.items()}
    PAD_T, PAD_B, GAP = 1.6, 1.2, 1.0

    # layout every rung first (heights from content), then stack bottom (1) to top (8)
    plan = []
    for n, title, (what, wcid), (ocid, ojoin), (cons, ccid), chips, status in R_:
        out = ojoin.join(CLAIMS[ocid]["print"]) if ojoin else CLAIMS[ocid]["print"][0]
        chip_w = [text_w(ax, s, fontsize=S.FLOOR, fontweight=600) + 4.0 for s, _ in chips]
        st_w = text_w(ax, status, fontsize=S.FLOOR) + 3.6
        right = sum(chip_w) + 1.6 * (len(chips) - 1) + 2.0 + st_w
        title_room = TXT_W - right - 3
        assert text_w(ax, title, fontsize=sz["title"], fontweight=600) <= title_room, title
        L_what = wrap(ax, what, TXT_W, fontsize=sz["what"])
        L_cons = wrap(ax, cons, TXT_W, fontsize=sz["cons"], fontweight=700)
        L_out = wrap(ax, out, TXT_W, fontsize=sz["out"])
        h = (PAD_T + lead["title"] + lead["what"] * len(L_what) + lead["cons"] * len(L_cons)
             + lead["out"] * len(L_out) + PAD_B)
        plan.append(dict(n=n, title=title, what=L_what, wcid=wcid, cons=L_cons, ccid=ccid, out=L_out, ocid=ocid,
                         chips=list(zip(chips, chip_w)), status=status, st_w=st_w, h=h))
    HEAD = 6.0
    total = sum(p["h"] for p in plan) + GAP * (len(plan) - 1)
    assert HEAD + total <= H, f"rungs need {HEAD + total:.1f} mm of {H}"
    H = round(HEAD + total + 0.4 * len(plan), 1)    # trim the canvas to the content plus 0.4 mm per rung
    fig.set_size_inches(W * S.MM, H * S.MM)
    ax.set_xlim(0, W); ax.set_ylim(H, 0)
    fig.canvas.draw()
    print("F4 height", H)
    extra = (H - HEAD - total) / len(plan)          # share any spare height evenly
    y = H
    for p in plan:                                   # rung 1 at the bottom
        p["h"] += extra
        y -= p["h"]
        p["y"] = y
        y -= GAP

    # header: what the bars mean and the reading direction
    ax.add_patch(Rectangle((0, 0.2), 3, 4.6, fc=C["incident"], ec="none"))
    T(ax, 5.0, 3.9, "each rung happened, in emem or in our tests", "F4.legend", fontsize=S.FLOOR,
      color=C["incident_text"], va="baseline")
    T(ax, X_R, 3.9, "↑ passes more checks", "F4.order", fontsize=S.FLOOR, color=C["ink2"], ha="right",
      va="baseline")

    for p in plan:
        y0, h = p["y"], p["h"]
        ax.add_patch(Rectangle((0, y0), X_R, h, fc=C["na"], ec="none", zorder=1))
        ax.add_patch(Rectangle((0, y0), 3.0, h, fc=C["incident"], ec="none", zorder=2))
        lay = p["chips"][-1][0][1]
        if lay == "L4":
            hatch(ax, X_R - 3.0, y0, 3.0, h, pitch=1.2, z=2)
        else:
            ax.add_patch(Rectangle((X_R - 3.0, y0), 3.0, h, fc=C[lay], ec="none", zorder=2))
        yy = y0 + PAD_T + lead["title"] * 0.80
        T(ax, X_T, yy, f"{p['n']}", "F4.titles", fontsize=sz["title"], fontweight=700, color=C["ink2"],
          va="baseline", zorder=4)
        T(ax, X_T + 5.6, yy, p["title"], "F4.titles", fontsize=sz["title"], fontweight=600, color=C["ink"],
          va="baseline", zorder=4)
        # chips and status, right-aligned on the title line
        xr = X_R - 4.5
        ch_h, ch_y = 5.6, y0 + PAD_T - 0.6
        bx = xr - p["st_w"]
        ax.add_patch(FancyBboxPatch((bx, ch_y + 0.3), p["st_w"], ch_h - 0.6, boxstyle="round,pad=0,rounding_size=1.0",
                                    fc="white", ec=C["rule"], lw=0.35 * MMPT, zorder=4))
        T(ax, bx + p["st_w"] / 2, ch_y + ch_h / 2 + 0.15, p["status"], f"F4.status.{p['n']}", fontsize=S.FLOOR,
          color=C["ink2"], ha="center", va="center", zorder=5)
        cx = bx - 2.0
        for (s, layer), w in reversed(p["chips"]):
            cx -= w
            if layer == "L4":
                hatch(ax, cx, ch_y, w, ch_h, pitch=1.2, z=4)
                ax.add_patch(FancyBboxPatch((cx + 1.2, ch_y + 1.0), w - 2.4, ch_h - 2.0,
                                            boxstyle="round,pad=0,rounding_size=0.6", fc="white", ec="none", zorder=5))
                tc = C["ink"]
            else:
                ax.add_patch(FancyBboxPatch((cx, ch_y), w, ch_h, boxstyle="round,pad=0,rounding_size=1.2", fc=C[layer],
                                            ec="none", zorder=4))
                tc = "white" if layer in ("L2", "L3") else C["ink"]
            T(ax, cx + w / 2, ch_y + ch_h / 2 + 0.15, s, "F4.chips", fontsize=S.FLOOR, fontweight=600, color=tc,
              ha="center", va="center", zorder=6)
            cx -= 1.6
        yy += lead["title"] * 0.2
        for ln in p["what"]:
            yy += lead["what"]
            T(ax, X_T, yy - lead["what"] * 0.22, ln, p["wcid"], fontsize=sz["what"], color=C["ink"], va="baseline",
              zorder=4)
        for ln in p["cons"]:
            yy += lead["cons"]
            T(ax, X_T, yy - lead["cons"] * 0.2, ln, p["ccid"], fontsize=sz["cons"], fontweight=700,
              color=C["harm_text"], va="baseline", zorder=4)
        for ln in p["out"]:
            yy += lead["out"]
            T(ax, X_T, yy - lead["out"] * 0.22, ln, p["ocid"], fontsize=sz["out"], color=C["ink2"], va="baseline",
              zorder=4)


    S.save(fig, NAME)
    meta = {"figure": NAME, "size_mm": [W, H],
            "rungs": [{k: p[k] for k in ("n", "title", "y", "h", "status")} for p in plan], "labels": LABELS}
    Path(S.OUT, f"{NAME}.labels.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
