"""F11 · One evidence protocol, multiple agent runtimes: bridge, status-labelled surfaces, same-token dot plot
(531 x 100 mm, brief §E F11).

(1) Bridge: signed record -> MCP · A2A -> agent host or client -> next agent.
(2) Five groups of named surfaces, names in poster type; each glyph is drawn from the row's `status` in
    research/v13/ecosystem_manifest.json (LIVE filled circle, PROTOCOL open circle, REGISTRY open square, EXAMPLE open
    triangle). A name prints only if its manifest row allows it and was verified within 14 days; conditional rows
    (ChatGPT, LangChain, Agno) print only when their condition file exists. One mark: GitHub's black Invertocat
    (octicons mark-github, unmodified) beside the repo name. No Dify mono asset is committed, so Dify is text.
(3) Same-token dot plot: rows.ndvi_keylong[*].ms_median from crossruntime_table.json (never .ms); every dot is the
    same `emem` blue because every path returned the same address and value; the A-to-B process row is one run, hollow.
The top-right corner (x > 468 mm, y < 17 mm) stays empty for the DISCOVER INTEGRATIONS QR (brief §F)."""
import glob, json, math, os, re, sys
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, PT, MONO, ROOT, fig_mm, save  # noqa: E402
import matplotlib.text  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, PathPatch, Polygon, Rectangle  # noqa: E402
from matplotlib.path import Path  # noqa: E402
from matplotlib.transforms import Affine2D  # noqa: E402

W, H = 531.0, 100.0
J = lambda p: json.load(open(os.path.join(ROOT, p)))
TODAY = datetime.now(timezone.utc)

# ---------------- manifest ----------------
MAN = {r["id"]: r for r in J("research/v13/ecosystem_manifest.json")}
COND = {   # conditional rows (claims map notes): the condition is a committed file
    "chatgpt": glob.glob(os.path.join(ROOT, "research/v13/*chatgpt*screenshot*.*")),
    "langchain": glob.glob(os.path.join(ROOT, "research/v13/evidence/ecosystem/*langchain*fixed*")),
    "agno": glob.glob(os.path.join(ROOT, "research/v13/evidence/ecosystem/*agno*fixed*")),
}
GROUPS = [  # (header, [(manifest id, printed name, mono?)])
    ("AGENT HOSTS", [("claude-code-mcp", "Claude Code", False), ("claude-code-plugin", "Claude Code plugin", False),
                     ("claude-ai-custom-connector", "Claude.ai custom connector", False),
                     ("dify-marketplace", "Dify Marketplace plugin\n(community)", False),
                     ("chatgpt", "ChatGPT (@emem)", False)]),
    ("INTEROPERABILITY", [("mcp-core", "Model Context Protocol (MCP)\nemem.dev/mcp", False),
                          ("a2a", "Agent2Agent (A2A)\nsigned agent card", False)]),
    ("DISCOVERY", [("official-mcp-registry", "Official MCP Registry\nio.github.Vortx-AI/emem", False),
                   ("github-mcp-registry", "GitHub MCP Registry", False),
                   ("github-repo", "github.com/Vortx-AI/emem", True), ("glama", "Glama", False)]),
    ("DEVELOPER", [("gemini-cli", "Gemini CLI", False), ("vscode", "Visual Studio Code", False), ("cursor", "Cursor", False),
                   ("python-sdk", "pip install ememdev", True), ("ts-sdk", "npm i @vortxai/emem", True),
                   ("rest-openapi", "REST / OpenAPI 3.1", False), ("docker", "ghcr.io/vortx-ai/emem", True)]),
    ("FRAMEWORKS", [("llamaindex", "LlamaIndex", False), ("autogen", "AutoGen", False), ("crewai", "CrewAI", False),
                    ("mastra", "Mastra", False), ("langchain", "LangChain (MCP adapters)", False), ("agno", "Agno", False)]),
]
GLYPH = {"LIVE": "disc", "PROTOCOL": "ring", "REGISTRY": "square", "EXAMPLE": "triangle"}
SHOWN, HELD = [], []
for g, items in GROUPS:
    keep = []
    for mid, name, mono in items:
        r = MAN[mid]
        allowed = r["print"]["allowed"]
        if mid in COND:
            allowed = bool(COND[mid])
        if allowed is not True:
            HELD.append(mid)
            continue
        assert r["status"] in GLYPH, (mid, r["status"])
        vt = datetime.fromisoformat(r["verified_utc"][:17].replace("Z", "+00:00"))
        assert (TODAY - vt).days <= 14, f"{mid}: manifest row older than 14 days ({r['verified_utc']})"
        keep.append((mid, name, mono, r["status"]))
    items[:] = keep
    SHOWN += [k[0] for k in keep]
assert "chatgpt" in HELD or COND["chatgpt"]
CHATGPT_EVIDENCE = MAN["chatgpt"]["evidence_level"]
assert CHATGPT_EVIDENCE.startswith("UNVERIFIED")
CHECKED = max(datetime.fromisoformat(MAN[m]["verified_utc"].split("(")[1].split(" ")[0]) for m in SHOWN)

# ---------------- same-token table ----------------
XR = J("research/repro/data/v8/crossruntime_table.json")
SUM = XR["summary"]["ndvi_keylong"]
assert SUM["paths_ok"] == 11 and SUM["receipt_verified_paths"] == 9 and len(SUM["distinct_fact_cids"]) == 1
NAMES = {"6c_official_mcp_python_sdk": "official MCP Python SDK", "6d_official_mcp_typescript_sdk": "official MCP TypeScript SDK",
         "5_typescript_sdk_@vortxai/emem": "TypeScript SDK", "4_python_sdk_ememdev": "Python SDK", "1_raw_rest": "raw REST",
         "2_raw_mcp_jsonrpc": "raw MCP", "3_a2a_message_send": "A2A message/send",
         "7_independent_blake3_cbor2": "independent BLAKE3 + CBOR reader", "6a_llamaindex_FunctionTool": "LlamaIndex",
         "6b_langchain_mcp_adapters": "LangChain MCP adapters", "A->B_isolated_processes": "A to B, two processes"}
ROWS = []
for r in XR["rows"]["ndvi_keylong"]:
    assert r["fact_cid"] == SUM["distinct_fact_cids"][0] and repr(r["value"]) == SUM["distinct_values"][0], r["path"]
    assert r["rehash_ok"] is True
    one = "ms_median" not in r
    ROWS.append(dict(name=NAMES[r["path"]], ms=r["ms"] if one else r["ms_median"], one=one,
                     receipt=bool(r.get("receipt_sig_ok"))))
assert len(ROWS) == 11 and sum(r["receipt"] for r in ROWS) == 9
ROWS.sort(key=lambda r: (r["one"], r["ms"]))
REPS = XR["reps"]; RUN_DATE = datetime.fromisoformat(XR["generated_utc"].replace("Z", "+00:00"))

# GitHub mark-github-24 (@primer/octicons 19.15.0, MIT), unmodified
GH = ("M12.5.75C6.146.75 1 5.896 1 12.25c0 5.089 3.292 9.387 7.863 10.91.575.101.79-.244.79-.546 0-.273-.014-1.178-.014-2.142"
      "-2.889.532-3.636-.704-3.866-1.35-.13-.331-.69-1.352-1.18-1.625-.402-.216-.977-.748-.014-.762.906-.014 1.553.834 1.769"
      " 1.179 1.035 1.74 2.688 1.25 3.349.948.1-.747.402-1.25.733-1.538-2.559-.287-5.232-1.279-5.232-5.678 0-1.25.445-2.285"
      " 1.178-3.09-.115-.288-.517-1.467.115-3.048 0 0 .963-.302 3.163 1.179.92-.259 1.897-.388 2.875-.388.977 0 1.955.13 2.875"
      ".388 2.2-1.495 3.162-1.179 3.162-1.179.633 1.581.23 2.76.115 3.048.733.805 1.179 1.825 1.179 3.09 0 4.413-2.688 5.39"
      "-5.247 5.678.417.36.776 1.05.776 2.128 0 1.538-.014 2.774-.014 3.162 0 .302.216.662.79.547C20.709 21.637 24 17.324 24"
      " 12.25 24 5.896 18.854.75 12.5.75Z")


def svg_path(d):
    toks = re.findall(r"[MmCcLlZz]|-?(?:\d+\.?\d*|\.\d+)", d)
    verts, codes, i, cmd, cur, start = [], [], 0, None, (0, 0), (0, 0)
    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]; i += 1
            if cmd in "Zz":
                verts.append(start); codes.append(Path.CLOSEPOLY); cur = start
                continue
        n = {"M": 2, "m": 2, "L": 2, "l": 2, "C": 6, "c": 6}[cmd]
        v = [float(t) for t in toks[i:i + n]]; i += n
        rel = cmd.islower()
        pts = [(v[k] + (cur[0] if rel else 0), v[k + 1] + (cur[1] if rel else 0)) for k in range(0, n, 2)]
        if cmd in "Mm":
            verts.append(pts[0]); codes.append(Path.MOVETO); start = cur = pts[0]; cmd = "l" if rel else "L"
        elif cmd in "Ll":
            verts.append(pts[0]); codes.append(Path.LINETO); cur = pts[0]
        else:
            verts += pts; codes += [Path.CURVE4] * 3; cur = pts[2]
    return Path(verts, codes)


IDS = ["EC.11", "EC.9of11", "EC.ms", "EC.statusdate", "A11.legend", "A11.abrow", "A11.header", "A11.chatgpt",
       "A11.bridge", "A11.axis"] + [f"EC.row.{m}" for m in SHOWN]


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
F, S, L, PTMM = PT["floor"], 15, PT["caption"], 0.3528
KO = dict(boxstyle="square,pad=0.15", fc="white", ec="none")


def T(x, y, s, size=S, color=C["ink"], ha="left", va="center", weight="normal", family=None, ko=False, z=6, **kw):
    d = dict(fontsize=size, color=color, ha=ha, va=va, fontweight=weight, zorder=z, linespacing=1.15, **kw)
    if family:
        d["family"] = family
    if ko:
        d["bbox"] = KO
    return ax.text(x, y, s, **d)


def line(xs, ys, w_mm, col, z=2, **kw):
    ax.plot(xs, ys, color=col, lw=w_mm / PTMM, solid_capstyle="butt", zorder=z, **kw)


def glyph(kind, x, y, r=2.0, col=C["ink"]):
    lw = 0.45 / PTMM
    if kind == "disc":
        ax.add_patch(Circle((x, y), r, fc=col, ec="none", zorder=5))
    elif kind == "ring":
        ax.add_patch(Circle((x, y), r - 0.25, fc="white", ec=col, lw=lw, zorder=5))
    elif kind == "square":
        s = r * 1.62
        ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc="white", ec=col, lw=lw, zorder=5))
    elif kind == "triangle":
        h = r * 1.85
        ax.add_patch(Polygon([(x - h / 1.73 * 1.0, y + h / 3), (x + h / 1.73, y + h / 3), (x, y - 2 * h / 3)],
                             closed=True, fc="white", ec=col, lw=lw, zorder=5, joinstyle="miter"))


def arrow(x0, x1, y, col=C["ink2"]):
    line([x0, x1 - 2.4], [y, y], 0.6, col, z=3)
    ax.add_patch(Polygon([(x1 - 2.6, y - 1.2), (x1, y), (x1 - 2.6, y + 1.2)], closed=True, fc=col, ec="none", zorder=3))


# (1) bridge
LW = 352.0
BY, BH = 1.5, 17.0
nodes = [("EMEM signed record", "emem:fact:…", "emem"), ("MCP · A2A", "transport", "tint"),
         ("agent host or client", "carries the reference", "plain"), ("next agent", "resolves, re-hashes, re-reads", "plain")]
nw, gap = [86, 64, 86, 92], 8.0
x = 0.0; centres = []
for (head, sub, kind), w in zip(nodes, nw):
    fc, ec, tc = {"emem": (C["emem"], C["emem"], "white"), "tint": (C["emem_tint"], C["emem_tint"], C["ink"]),
                  "plain": ("white", C["ink2"], C["ink"])}[kind]
    ax.add_patch(FancyBboxPatch((x, BY), w, BH, boxstyle="round,pad=0,rounding_size=2.0", fc=fc, ec=ec,
                                lw=0.5 / PTMM if kind == "plain" else 0, zorder=4))
    T(x + 4, BY + 5.0, head, L, tc, weight="semibold")
    T(x + 4, BY + 12.0, sub, F, tc if kind != "plain" else C["ink2"], family=MONO if sub.startswith("emem:") else None)
    centres.append(x + w / 2)
    if x + w + gap < LW:
        arrow(x + w + 0.8, x + w + gap - 0.8, BY + BH / 2)
    x += w + gap
assert x - gap <= LW + 0.5, x

# (2) groups
GY, PITCH = 26.5, 6.6
GX, gx = [], 0.0
for g, items in GROUPS:
    GX.append(gx)
    texts = [T(gx, GY, g, F, C["ink2"], weight="semibold")]
    y = GY + 6.6
    for mid, name, mono, st in items:
        glyph(GLYPH[st], gx + 2.0, y)
        lines = name.split("\n")
        tx = gx + 6.0
        if mid == "github-repo":                                       # black Invertocat beside the repo name
            p = svg_path(GH)
            tr = Affine2D().translate(-12.5, -12.0).scale(4.0 / 24).translate(gx + 8.4, y)
            ax.add_patch(PathPatch(tr.transform_path(p), fc="black", ec="none", zorder=5))
            tx = gx + 11.6
        texts.append(T(tx, y, lines[0], F, C["ink"], family=MONO if mono else None))
        for extra in lines[1:]:
            y += 6.0
            texts.append(T(tx, y, extra, F, C["ink2"], family=MONO if "." in extra and " " not in extra else None))
        y += PITCH
    fig.canvas.draw()
    xe = max(ax.transData.inverted().transform((t.get_window_extent().x1, 0))[0] for t in texts)
    line([gx, xe], [GY - 3.8, GY - 3.8], 0.35, C["rule"], z=1)
    gx = xe + 7.0
assert gx - 7.0 <= 352.0, gx
# legend and the held ChatGPT row
YL = 86.0
x = 0.0
for kind, word, desc in (("disc", "LIVE", "connected or published"), ("ring", "PROTOCOL", "open surface, client not run by us"),
                         ("square", "REGISTRY", "a listing"), ("triangle", "EXAMPLE", "repo code, tool list checked")):
    glyph(kind, x + 2.0, YL, r=1.8)
    t = T(x + 5.6, YL, word, F, C["ink"], weight="semibold")
    fig.canvas.draw(); e = t.get_window_extent(); xe = ax.transData.inverted().transform((e.x1, e.y0))[0]
    t2 = T(xe + 1.6, YL, desc, F, C["ink2"])
    fig.canvas.draw(); e = t2.get_window_extent(); x = ax.transData.inverted().transform((e.x1, e.y0))[0] + 6.0
T(0.0, YL + 7.0, f"checked {CHECKED.day} {CHECKED:%b %Y}", F, C["ink2"])
if "chatgpt" in HELD:
    T(64.0, YL + 7.0, "ChatGPT (@emem): listed by its publisher, not confirmed by us; held off the band", F, C["ink2"])

# (3) same-token dot plot
PX0 = 362.0
LX = 447.0                     # row labels right-aligned here; receipt column after it
DX0, DX1 = 456.0, 513.0
lo, hi = 30.0, 2000.0
xd = lambda ms: DX0 + math.log10(ms / lo) / math.log10(hi / lo) * (DX1 - DX0)
T(PX0, 4.8, "one address, one value on every path", L, C["emem"], weight="semibold")
T(PX0, 11.6, f"median ms of {REPS} runs, log scale, {RUN_DATE.day} {RUN_DATE:%b %Y}", F, C["ink2"])
RY0, RP = 22.5, 6.55
YAX = RY0 + RP * (len(ROWS) - 1) + 4.6
for v in (30, 100, 300, 1000):
    line([xd(v), xd(v)], [RY0 - 3.0, YAX], 0.35, C["rule"], z=1)
for k, r in enumerate(ROWS):
    y = RY0 + RP * k
    if r["one"]:
        line([PX0, W], [y - 3.0, y - 3.0], 0.35, C["rule"], z=1)
    T(LX, y, r["name"], F, C["ink"], ha="right")
    if r["receipt"]:                                               # receipt signature checked: a drawn tick
        ax.plot([LX + 1.8, LX + 2.9, LX + 5.0], [y + 0.1, y + 1.2, y - 1.4], color=C["emem"], lw=0.55 / PTMM,
                solid_capstyle="round", solid_joinstyle="round", zorder=5)
    else:
        line([LX + 2.0, LX + 4.6], [y, y], 0.45, C["muted"], z=5)
    x = xd(r["ms"])
    line([DX0, x], [y, y], 0.35, C["emem_tint"], z=2)
    if r["one"]:
        ax.add_patch(Circle((x, y), 1.35, fc="white", ec=C["emem"], lw=0.45 / PTMM, zorder=5))
        T(x - 2.4, y, f"{r['ms']:,.1f} · one run", F, C["ink2"], ko=True, ha="right")
    else:
        ax.add_patch(Circle((x, y), 1.45, fc=C["emem"], ec="white", lw=0.6, zorder=5))
        T(x + 2.4, y, f"{r['ms']:,.1f}", F, C["ink"], ko=True)
line([DX0, DX1], [YAX, YAX], 0.5, C["ink2"], z=3)
for v in (30, 100, 300, 1000):
    line([xd(v), xd(v)], [YAX, YAX + 1.2], 0.5, C["ink2"], z=3)
    T(xd(v), YAX + 3.4, f"{v:,}", F, C["ink2"], ha="center")
ax.plot([PX0 + 0.6, PX0 + 1.7, PX0 + 3.8], [YAX + 3.5, YAX + 4.6, YAX + 2.0], color=C["emem"], lw=0.55 / PTMM,
        solid_capstyle="round", solid_joinstyle="round", zorder=5)
T(PX0 + 5.6, YAX + 3.4, f"receipt signature checked on {SUM['receipt_verified_paths']} of {SUM['paths_ok']}", F, C["ink2"])

claims_gate(fig, IDS)
save(fig, "f11_ecosystem")
