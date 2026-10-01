"""F9 · Memory keeps what was cited: a branching transaction-time memory (193.5 x 82 mm, brief §E F9).

Top: one Bengaluru cell and band; record 1 (918.0 m) from 28 May runs to the right edge (it still resolves), record 2
(915.07 m) branches off on 11 Aug with one tick per signing; four as-of probes, each answered by recomputing the
as-of rule from the attestations. Bottom: Keylong valid time; the 2025-26 NDVI records drawn hollow when they were
signed before the reader's pixel fix (review finding F01), and a zoom on the cited 25 Sep record versus the newer
30 Sep one under the constructed test rule.
Every number is read from a file; every printed string with a digit is checked against the claims map."""
import json, os, re, sys
from datetime import datetime, timezone, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, PT, MONO, ROOT, fig_mm, save  # noqa: E402
import matplotlib.text  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, PathPatch, Rectangle  # noqa: E402
from matplotlib.path import Path  # noqa: E402

W, H = 193.5, 82.0
J = lambda p: json.load(open(os.path.join(ROOT, p)))
ts = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))

# ---------------- data ----------------
CB = J("research/repro/data/contra_bengaluru.json")["contradictions"][0]
AT = sorted(CB["attestations"], key=lambda a: a["signed_at"])
PROV = [p["fn_key"] for p in CB["providers"]]
r1 = [a for a in AT if a["value"] == AT[0]["value"]]
r2 = [a for a in AT if a["value"] != AT[0]["value"]]
assert len(r1) == 1 and len({a["value"] for a in r2}) == 1
assert PROV[0].startswith("open_meteo_copdem90m") and all(p.startswith("copernicus_dem_30m") for p in PROV[1:])
V1, V2 = r1[0]["value"], r2[0]["value"]


def as_of(t):
    k = [a for a in AT if ts(a["signed_at"]) <= t]
    return k[-1] if k else None


PROBES = [("2026-05-01", None), ("2026-06-15", 918.0), ("2026-08-12", 915.07), ("2026-09-29", 915.07)]
for q, want in PROBES:     # the printed as-of answers equal the recomputation (make_figures_v12.py:506-510)
    got = as_of(ts(q + "T00:00:00Z"))
    assert (None if got is None else round(got["value"], 2)) == want, (q, got)

KL = J("research/repro/v12/data/case_keylong_ndvi.json")["rows"]
src = open(os.path.join(ROOT, "research/repro/v8/trace_fact.py")).read()
FIX = re.search(r"PIXEL_FIX_AT (\d{4}-\d\d-\d\dT[\d:]+Z)", src).group(1)       # emem lib.rs:12650, as cited there
KS = [r for r in KL if r["date"] >= "2025-01-01" and r["value"] is not None]
PRE = [r for r in KS if r["signed_at"] < FIX]
assert (len(KS), len(PRE)) == (141, 14), (len(KS), len(PRE))     # 11_research_gaps C5: 14 of the 141 plotted
CITED = next(r for r in KL if r["fact_cid"].startswith("oj5cecci"))
assert CITED["signed_at"] >= FIX
NEW = next(p for p in J("research/repro/data/v11/cell_products.json") if p["band"] == "indices.ndvi")
NEW_DATE = (datetime(1970, 1, 1) + timedelta(days=NEW["tslot"])).date()          # tslot = days since epoch
assert str(NEW_DATE) == "2026-09-30" and CITED["tslot"] == 20721
RULE = float(re.search(r"<= ([\d.]+)", J("research/repro/v11/out/mutation_matrix.json")["meta"]["rule"]).group(1))
dec = lambda v: "irrigate" if v <= RULE else "hold"
assert dec(CITED["value"]) == "hold" and dec(NEW["value"]) == "irrigate"

# ---------------- claims gate ----------------
IDS = ["TM.918", "TM.915", "TM.asof", "TM.keylong", "TM.still", "TM.asof_rule", "S.threshold",
       "A9.signed7", "A9.ground", "A9.axis", "A9.prefix", "A9.kaxis"]


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


# ---------------- drawing ----------------
fig = fig_mm(W, H)
fig.set_dpi(300)                      # measure text at the dpi it is rendered at
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
F, S, L = PT["floor"], 15, PT["caption"]
PTMM = 0.3528                                                       # 1 pt in mm
KO = dict(boxstyle="square,pad=0.1", fc="white", ec="none")         # knock-out plate: no line crosses a label


def T(x, y, s, size=F, color=C["ink"], ha="left", va="center", weight="normal", ko=True, family=None, z=6):
    kw = dict(fontsize=size, color=color, ha=ha, va=va, fontweight=weight, zorder=z)
    if family:
        kw["family"] = family
    if ko:
        kw["bbox"] = KO
    return ax.text(x, y, s, **kw)


def right_of(t, gap=0.0):
    fig.canvas.draw()
    e = t.get_window_extent()
    return ax.transData.inverted().transform((e.x1, e.y0))[0] + gap


def line(xs, ys, w_mm, col, **kw):
    ax.plot(xs, ys, color=col, lw=w_mm / PTMM, solid_capstyle="butt", **kw)


# transaction-time axis, 1 May to 30 Sep 2026
t0, t1 = datetime(2026, 5, 1, tzinfo=timezone.utc), datetime(2026, 9, 30, tzinfo=timezone.utc)
X0, X1 = 21.0, W - 3.0
xt = lambda t: X0 + (t - t0).total_seconds() / (t1 - t0).total_seconds() * (X1 - X0)
YA, YB = 8.6, 14.2                      # probe label tiers
Y1, Y2, YAX = 24.4, 31.8, 41.2          # record 1 lane, record 2 lane, axis

h = T(0, 2.6, "Bengaluru · one cell · ", F, C["ink2"], ko=False)
T(right_of(h, 0.4), 2.6, "copdem30m.elevation_mean", F, C["ink2"], ko=False, family=MONO)

# the address node and its branches
NX, NY = 5.2, (Y1 + Y2) / 2
for yl, recs in ((Y1, r1), (Y2, r2)):
    xs = xt(ts(recs[0]["signed_at"]))
    v = [(NX, NY), (NX + 6, NY), (NX + 4, yl), (NX + 11, yl), (xs, yl)]
    ax.add_patch(PathPatch(Path(v, [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.LINETO]),
                           fc="none", ec=C["muted"], lw=0.35 / PTMM, ls=(0, (2, 2)), zorder=2))
ax.add_patch(Circle((NX, NY), 2.6, fc=C["emem"], ec="white", lw=1.2, zorder=4))
T(0.0, NY + 5.6, "address", F, C["emem"], ko=False)

# records: from first signing to the right edge (a record does not end; it still resolves)
for yl, recs in ((Y1, r1), (Y2, r2)):
    xa = xt(ts(recs[0]["signed_at"]))
    line([xa, X1 + 0.6], [yl, yl], 1.5, C["ink2"], zorder=3)
    ax.add_patch(PathPatch(Path([(X1 + 0.6, yl - 1.5), (X1 + 2.9, yl), (X1 + 0.6, yl + 1.5)]), fc=C["ink2"], ec="none", zorder=3))
    for a in recs:                                        # one tick per signing
        x = xt(ts(a["signed_at"]))
        line([x, x], [yl - 2.2, yl + 2.2], 0.55, C["ink"], zorder=4)
d1, d2 = ts(r1[0]["signed_at"]), ts(r2[0]["signed_at"])
T(xt(d1) - 0.3, Y1 - 4.4, f"{V1:.1f} m · signed {d1:%-d %b} · 90 m DEM via Open-Meteo", F, C["ink"], weight="medium")
T(X1, Y2 + 4.4, f"{V2:.2f} m · first signed {d2:%-d %b} · 30 m DEM · signed {len(r2)} times", F, C["ink"],
  weight="medium", ha="right")

# as-of probes
for q, want in PROBES:
    t = ts(q + "T00:00:00Z"); x = xt(t)
    hot = q == "2026-06-15"
    lab = f"{t:%-d %b}: " + ("none" if want is None else (f"{want:.1f} m" if want == 918.0 else f"{want:.2f} m"))
    a = as_of(t)
    if want is None:
        T(x - 1.2, YA, lab, S, C["ink2"])
        ytop, yend = YA + 2.7, YAX
    else:
        T(x - (2.9 if hot else 0.9), YB, lab, S, C["harm_text"] if hot else C["ink"], ha="right",
          weight="semibold" if hot else "normal")           # the 15 Jun label sits 2 mm clear of its dashed rule
        ytop, yend = (YA - 2.6 if hot else YB - 2.6), (Y1 if a in r1 else Y2)
    col, w = (C["harm"], 0.9) if hot else (C["muted"], 0.5)
    ax.plot([x, x], [ytop, yend], color=col, lw=w / PTMM, ls=(0, (2.2 / w, 1.2 / w)) if hot else (0, (3, 3)), zorder=1)
    line([x, x], [YAX - 1.3, YAX], 0.5, C["ink2"], zorder=2)
    if a is not None:
        yy = Y1 if a in r1 else Y2
        ax.add_patch(Circle((x, yy), 1.8, fc="white", ec=C["emem"], lw=0.8 / PTMM, zorder=5))
        ax.add_patch(Circle((x, yy), 0.8, fc=C["emem"], ec="none", zorder=5))
    else:
        ax.add_patch(Circle((x, YAX), 0.9, fc="white", ec=C["ink2"], lw=1.2, zorder=5))
xq = xt(ts("2026-06-15T00:00:00Z"))
T(xq + 1.4, YA, "what did agent A know on 15 Jun? → 918.0 m", S, C["harm_text"], weight="semibold")

# axis
line([X0, X1], [YAX, YAX], 0.5, C["ink2"], zorder=2)
for m in range(5, 10):
    x = xt(datetime(2026, m, 1, tzinfo=timezone.utc))
    line([x, x], [YAX, YAX + 1.3], 0.5, C["ink2"], zorder=2)
    xm = xt(datetime(2026, m, 15, tzinfo=timezone.utc))
    T(xm, YAX + 3.3, datetime(2026, m, 1).strftime("%b"), F, C["ink2"], ha="center", ko=False)
T(0, YAX + 3.3, "2026", F, C["ink2"], ko=False)
T(0, YAX + 8.3, "as-of compares signing times (UTC seconds); here the provider changed, not the ground", F, C["ink2"], ko=False)

# ---------------- Keylong valid-time strip ----------------
line([0, W], [53.2, 53.2], 0.35, C["rule"], zorder=1)
YH, YR1, PY0, PY1, YR2 = 57.0, 62.2, 65.2, 74.6, 78.9
h = T(0, YH, "Keylong field · NDVI", S, C["ink"], weight="semibold", ko=False)
lx = right_of(h, 5.0)
ax.add_patch(Circle((lx + 0.9, YH), 0.9, fc="white", ec=C["ink"], lw=0.8, zorder=4))
T(lx + 2.8, YH, f"signed before the reader's pixel fix ({ts(FIX):%-d %b %Y})", F, C["ink2"], ko=False)
ax.add_patch(Circle((lx + 0.9 + 0, YH), 0.0, fc="none"))
vlo, vhi = -0.1, 0.8
yv = lambda v: PY1 - (v - vlo) / (vhi - vlo) * (PY1 - PY0)
# two segments on one value scale: Jan 2025 to 12 Sep 2026, and 13 Sep to 1 Oct 2026 stretched
A0, A1, B0, B1 = 9.5, 118.0, 124.0, W - 1.5
s0, sb, s1 = datetime(2025, 1, 1), datetime(2026, 9, 13), datetime(2026, 10, 1)
def xk(d):
    if d < sb:
        return A0 + (d - s0).total_seconds() / (sb - s0).total_seconds() * (A1 - A0)
    return B0 + (d - sb).total_seconds() / (s1 - sb).total_seconds() * (B1 - B0)
for xa, xb in ((A0, A1), (B0, B1)):
    line([xa, xb], [PY1 + 0.9, PY1 + 0.9], 0.5, C["ink2"], zorder=2)
for xb in (A1, B0):                                   # the axis break
    line([xb - 0.9, xb + 0.9], [PY1 + 2.1, PY1 - 0.3], 0.5, C["ink2"], zorder=2)
for r in KS:
    if r is CITED:
        continue
    d = datetime.fromisoformat(r["date"]); x, y = xk(d), yv(r["value"])
    rad = 0.72 if d < sb else 0.95
    if r["signed_at"] < FIX:
        ax.add_patch(Circle((x, y), rad, fc="white", ec=C["ink"], lw=0.8, zorder=4))
    else:
        ax.add_patch(Circle((x, y), rad * 0.8, fc=C["ink2"], ec="none", zorder=3))
for v in (0.0, 0.5):
    line([A0 - 1.2, A0 - 0.2], [yv(v)] * 2, 0.5, C["ink2"], zorder=2)
    T(A0 - 1.8, yv(v), "0" if v == 0 else "0.5", F, C["ink2"], ha="right", ko=False)
for yr in (2025, 2026):
    x = xk(datetime(yr, 1, 1))
    line([x, x], [PY1 + 0.9, PY1 - 0.4], 0.5, C["ink2"], zorder=2)
    T(x + 0.5, YR1, str(yr), F, C["ink2"], ko=False)
for d in (datetime(2026, 9, 15), datetime(2026, 9, 20), datetime(2026, 9, 25), datetime(2026, 9, 30)):
    x = xk(d); line([x, x], [PY1 + 0.9, PY1 - 0.4], 0.5, C["ink2"], zorder=2)
cd = datetime.fromisoformat(CITED["date"])
xc, yc = xk(cd), yv(CITED["value"])
ax.add_patch(Circle((xc, yc), 1.9, fc="white", ec=C["emem"], lw=0.8 / PTMM, zorder=5))
ax.add_patch(Circle((xc, yc), 0.9, fc=C["emem"], ec="none", zorder=5))
nd = datetime(NEW_DATE.year, NEW_DATE.month, NEW_DATE.day)
xn, yn = xk(nd), yv(NEW["value"])
ax.add_patch(Circle((xn, yn), 1.3, fc=C["oos"], ec="white", lw=0.8, zorder=5))
T(xc + 2.2, YR1, f"cited {cd:%-d %b}: {CITED['value']:.4f} → {dec(CITED['value'])}", S, C["emem"], ha="right", weight="semibold")
T(B1 + 1.0, YR2, f"{NEW_DATE:%-d %b}: {NEW['value']:.4f} → {dec(NEW['value'])}", S, C["ink2"], ha="right", weight="medium")
T(0, YR2, "the cited reference still re-hashes (1 Oct 2026)", F, C["emem"], ko=False, weight="medium")
for (x, y0), y1 in (((xc, yc - 2.0), YR1 + 2.4), ((xn, yn + 1.4), YR2 - 2.4)):
    line([x, x], [y0, y1], 0.35, C["ink2"], zorder=7)

claims_gate(fig, IDS)
save(fig, "f9_timeline")
