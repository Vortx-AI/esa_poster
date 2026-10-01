"""F10 · What it costs: two aligned log strips (193.5 x 50 mm, brief §E F10).

Strip 1: time per check on a log axis 1 µs to 10 s, one row per item, dot and label at the dot; dots take the
verification-depth ramp of the layer they check (L0 re-hash, L0 resolve, L2 offline chain, L3 source re-read).
Strip 2: context tokens (cl100k) on a log axis 1 to 100,000, same width.
Every value is read from research/v13/cost_measurements.json and the committed files it names; printed strings with a
digit are checked against the claims map. The scope line (host, proxy, tokenizer, model receiver) stays in the HTML."""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, PT, ROOT, fig_mm, save  # noqa: E402
import matplotlib.text  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch  # noqa: E402

W, H = 193.5, 50.0
J = lambda p: json.load(open(os.path.join(ROOT, p)))
CM = J("research/v13/cost_measurements.json")
m1, m2, m3, m5 = CM["m1_resolve_fact_https"], CM["m2_offline_verification"], CM["m3_trace_read_only"], CM["m5_tokens"]

rehash_s = m2["primitives_us"]["blake3_fact_1115B"]["median"] * 1e-6
chain_s = (m2["mutation_suite_ms_per_decision_by_level"]["I"]["median"]
           - m2["mutation_suite_genuine_construction_ms"]["median"]) * 1e-3     # per decision less the handoff construction
bundle_s = m2["in_process_precompiled_exec_ms"]["median"] * 1e-3
bundle_B = os.path.getsize(os.path.join(ROOT, "research/repro/v8/proof_bundle_ndvi.cbor"))
assert "4,906 B, 9 checks" in m2["bundle"] and bundle_B == 4906
warm_s = m1["warm_cbor_reused_connection_ms"]["median"] * 1e-3
cold_s = m1["cold_cbor_new_connection_ms"]["median"] * 1e-3
links = m3["keylong_ndvi"]["links"]
reread_ms = sum(links[k]["ms_median"] for k in ("8", "9", "9b"))           # STAC item + COG range reads + SCL
reread_B = sum(min(links[k]["bytes"]) for k in ("8", "9", "9b"))
assert round(reread_ms) == 6945 and reread_B == 1180728, (reread_ms, reread_B)
px = J("research/repro/data/v8/cog_pixel_bytes.json")["ndvi_cold_read_bytes"]["total"]
scene = J("research/repro/data/v8/scene_sizes.json")["total_scene_bytes_all_blob_assets"]
frac = 100 * px / scene
tok = {k: m5["items"][k]["cl100k"] for k in ("value_16_digits", "fact_token", "fact_json_as_served",
                                              "mcp_tools_list_core18_response")}
assert CM["measured_on"].startswith("2026-10-01")
mb = lambda b: f"{b / 1e6:.2f} MB"
TIME_ROWS = [  # label, seconds (one or two), ramp level
    (f"re-hash {rehash_s * 1e6:.1f} µs", [rehash_s], "L0"),
    (f"all offline checks {chain_s * 1e3:.2f} ms", [chain_s], "L2"),
    (f"offline proof bundle {bundle_s * 1e3:.2f} ms ({bundle_B:,} B)", [bundle_s], "L2"),
    (f"resolve {warm_s * 1e3:.0f} ms warm, {cold_s * 1e3:.0f} ms cold", [warm_s, cold_s], "L0"),
    (f"source re-read about {reread_ms / 1e3:.0f} s, {mb(reread_B)} ({frac:.3f} % of the scene)", [reread_ms / 1e3], "L3"),
]
TOK_ROWS = [("value", tok["value_16_digits"]), ("reference", tok["fact_token"]),
            ("record as JSON", tok["fact_json_as_served"]), ("18-tool MCP list", tok["mcp_tools_list_core18_response"])]
IDS = ["C.hash", "C.cpu", "C.bundle", "C.resolve", "C.reread", "C.scene", "C.tok", "C.json", "C.tools", "A10.axes",
       "A10.m15"]


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
X0, X1 = 3.0, W - 3.0


KO = dict(boxstyle="square,pad=0.15", fc="white", ec="none")       # knock-out plate: no gridline crosses a label


def T(x, y, s, size=F, color=C["ink"], ha="left", va="center", weight="normal", ko=True):
    return ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight, zorder=6,
                   bbox=KO if ko else None)


def line(xs, ys, w_mm, col, z=2, **kw):
    ax.plot(xs, ys, color=col, lw=w_mm / PTMM, solid_capstyle="butt", zorder=z, **kw)


# ---- strip 1: seconds, 1e-6 .. 1e1
xs_ = lambda s: X0 + (math.log10(s) + 6) / 7 * (X1 - X0)
YS = [2.9, 8.7, 8.7, 14.5, 20.3]; YAX = 24.0
for x in [xs_(10 ** e) for e in range(-6, 2)]:
    line([x, x], [0.5, YAX], 0.35, C["rule"], z=1)
for (lab, vals, lev), y in zip(TIME_ROWS, YS):
    xv = [xs_(v) for v in vals]
    if len(xv) == 2:
        line(xv, [y, y], 0.9, C[lev], z=3)
    for x in xv:
        ax.add_patch(Circle((x, y), 1.25 if lev != "L3" else 1.7, fc=C[lev], ec="white", lw=0.8, zorder=4))
    if lev == "L3":                                   # the lone dear dot, the only check that refuses M15
        xr = xv[0] - 3.0
        ax.add_patch(FancyBboxPatch((xr - 10.4, y - 2.1), 10.4, 4.2, boxstyle="round,pad=0,rounding_size=0.9",
                                    fc=C["L3"], ec="none", zorder=4))
        T(xr - 5.2, y + 0.05, "M15", F, "white", ha="center", weight="semibold", ko=False)
        T(xr - 12.0, y, lab, F, C["ink"], ha="right", weight="semibold")
    elif (lev == "L0" and len(xv) == 2) or lab.startswith("all offline"):
        T(xv[0] - 2.4, y, lab, F, C["ink"], ha="right")
    else:
        T(xv[-1] + 2.4, y, lab, F, C["ink"])
line([X0, X1], [YAX, YAX], 0.5, C["ink2"], z=6.5)
for e, lab in zip(range(-6, 2), ["1 µs", "10 µs", "100 µs", "1 ms", "10 ms", "100 ms", "1 s", "10 s"]):
    x = xs_(10 ** e); line([x, x], [YAX, YAX + 1.2], 0.5, C["ink2"])
    T(x, YAX + 3.4, lab, F, C["ink2"], ko=False, ha="left" if e == -6 else ("right" if e == 1 else "center"))

# ---- strip 2: tokens, 1 .. 1e5, same width
xt_ = lambda n: X0 + math.log10(n) / 5 * (X1 - X0)
YHI, YLO, YD, YAX2 = 33.4, 38.4, 42.2, 44.2
for x in [xt_(10 ** e) for e in range(0, 6)]:
    line([x, x], [31.5, YAX2], 0.35, C["rule"], z=1)
place = {"value": (YHI, "center"), "reference": (YLO, "center"), "record as JSON": (YHI, "center"),
         "18-tool MCP list": (YLO, "right")}
for lab, n in TOK_ROWS:
    x = xt_(n); yl, ha = place[lab]
    ref = lab == "reference"
    ax.add_patch(Circle((x, YD), 1.25, fc=C["emem"] if ref else C["ink2"], ec="white", lw=0.8, zorder=7))
    line([x, x], [yl + 2.4, YD - 1.4], 0.35, C["ink2"], z=3)
    s = f"{lab} {n:,}" + (" (1 Oct)" if lab.startswith("18-tool") else "")
    if ha == "right":
        T(W - 0.3, yl, s, F, C["ink"], ha="right")
    else:
        T(x, yl, s, F, C["emem"] if ref else C["ink"], ha="center", weight="semibold" if ref else "normal")
line([X0, X1], [YAX2, YAX2], 0.5, C["ink2"])
for e in range(0, 6):
    x = xt_(10 ** e); line([x, x], [YAX2, YAX2 + 1.2], 0.5, C["ink2"])
    if e == 1:
        continue
    lab = "1 token (cl100k)" if e == 0 else f"{10 ** e:,}"
    T(x, YAX2 + 3.3, lab, F, C["ink2"], ko=False, ha="left" if e == 0 else ("right" if e == 5 else "center"))

claims_gate(fig, IDS)
save(fig, "f10_cost")
