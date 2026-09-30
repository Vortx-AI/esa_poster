"""Build the poster's data figures from emem data fetched on 2026-09-29.

Inputs live in research/repro/data/ (all fetched from emem.dev; every artifact re-hashed with
stock blake3 before use). Outputs are SVG/PNG files in poster/fig/.
    pip install numpy matplotlib networkx pillow ; python make_figures.py
"""
import json, struct, collections, datetime as dt, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import networkx as nx
from PIL import Image

HERE = pathlib.Path(__file__).parent
DATA = HERE.parent / "research" / "repro" / "data"
OUT = HERE / "fig"; OUT.mkdir(exist_ok=True)
INK, INK2, MUTED, RULE, ACC, WRONG, GRAY = "#141414", "#46463F", "#85857E", "#D3D3CC", "#1F4FD8", "#B3261E", "#B9B9B2"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.linewidth": .6, "xtick.major.width": .6, "ytick.major.width": .6, "svg.fonttype": "none"})

def grid(path):
    raw = (DATA / path).read_bytes()
    assert raw[:8] == b"EMEMGRD1"
    w, h = struct.unpack_from("<II", raw, 8)
    return np.frombuffer(raw, dtype="<f4", offset=64).reshape(h, w).astype(float)

# ---------- F1: signed Sentinel-2 bands -> true colour and NDVI ----------
R, G, B, N = (grid(f"keylong_{b}.bin") for b in ("B04", "B03", "B02", "B08"))
rgb = np.dstack([R, G, B]) / 10000.0
lo, hi = np.nanpercentile(rgb, 2), np.nanpercentile(rgb, 98.5)
tc = np.clip((rgb - lo) / (hi - lo), 0, 1) ** (1 / 1.25)
Image.fromarray((np.nan_to_num(tc) * 255).astype("uint8")).resize((886, 906), Image.LANCZOS).save(OUT / "keylong_truecolor.png")
ndvi = (N - R) / (N + R)
cmap = plt.get_cmap("Greens").copy(); cmap.set_under("#E9E6DF")
fig, ax = plt.subplots(figsize=(3.2, 3.27), dpi=300)
im = ax.imshow(ndvi, cmap=cmap, vmin=0.05, vmax=0.8, interpolation="nearest")
ax.set_axis_off()
# the signed NDVI fact oj5cecci (32.57126 N, 77.03448 E) inside bbox 32.55-32.59 N, 77.01-77.058 E
fx, fy = (77.03448 - 77.01) / 0.048 * ndvi.shape[1], (32.59 - 32.57126) / 0.04 * ndvi.shape[0]
ax.add_patch(plt.Rectangle((fx - 6, fy - 6), 12, 12, fill=False, ec=ACC, lw=1.2))
cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=.05, pad=.02, extend="min")
cb.set_label("NDVI from the signed B04/B08 grids", fontsize=6.5); cb.ax.tick_params(labelsize=6)
fig.subplots_adjust(.02, .12, .98, 1); fig.savefig(OUT / "keylong_ndvi.png", dpi=300); plt.close(fig)

# ---------- F2: cube members (B08) with the date each member actually serves ----------
cube = json.load(open(DATA / "cubeK_members.json"))
fig, axs = plt.subplots(1, 5, figsize=(7.2, 1.9), dpi=300)
for ax, m in zip(axs, cube["members"]):
    g = grid(m["file"]); v = g / 10000.0
    ax.imshow(v, cmap="gray", vmin=np.nanpercentile(v, 2), vmax=np.nanpercentile(v, 98)); ax.set_axis_off()
    sd = dt.datetime.strptime(m["scene"].split("_")[2][:8], "%Y%m%d")
    rq = dt.datetime.strptime(m["req"], "%Y-%m-%d")
    ax.set_title(f"{rq:%d %b} → {sd:%d %b}\n(+{m['days']} d)", fontsize=9.5, color=INK, pad=2)
fig.subplots_adjust(.005, .01, .995, .76, wspace=.04); fig.savefig(OUT / "cube_members.png", dpi=300); plt.close(fig)

# ---------- F3: two clocks — one key, every attestation, and the answer as known over time ----------
att = json.load(open(DATA / "contra_bengaluru.json"))["contradictions"][0]["attestations"]
pts = sorted((dt.datetime.fromisoformat(a["signed_at"].replace("Z", "+00:00")), a["value"]) for a in att)
fig, ax = plt.subplots(figsize=(3.6, 1.6), dpi=300)
t_end = dt.datetime(2026, 9, 29, tzinfo=dt.timezone.utc)
xs = [p[0] for p in pts] + [t_end]; ys = [p[1] for p in pts] + [pts[-1][1]]
ax.step(xs, ys, where="post", color=INK2, lw=1)
ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=[26 if p[1] == 918 else 14 for p in pts],
           c=[ACC if p[1] == 918 else INK for p in pts], zorder=3, edgecolors="#FBFBF8", linewidths=.6)
ax.set_ylim(914, 919.8); ax.set_yticks([915, 916, 917, 918]); ax.set_ylabel("elevation (m)", fontsize=8.5); ax.tick_params(labelsize=8)
ax.xaxis.set_major_locator(mdates.MonthLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.set_xlabel("record time (signed_at), 2026", fontsize=8.5)
ax.annotate("918.0 m · Cop-DEM 90 m via Open-Meteo", (pts[0][0], 918), (6, 4), textcoords="offset points", fontsize=8, va="bottom", color=ACC)
ax.annotate("915.07 m · Cop-DEM 30 m COG\n7 re-signings, same value", (dt.datetime(2026, 5, 30, tzinfo=dt.timezone.utc), 917.55), textcoords="data", fontsize=8, color=INK, ha="left", va="top")
ax.grid(axis="y", color=RULE, lw=.4)
fig.subplots_adjust(.13, .25, .98, .97); fig.savefig(OUT / "two_clocks.svg"); plt.close(fig)

# ---------- F4: transparency-log growth, timestamps decoded from sampled signed entries ----------
lg = [r for r in json.load(open(DATA / "loggrowth.json")) if r[1]]
t = [dt.datetime.fromisoformat(r[1].replace("Z", "+00:00")) for r in lg]; n = [r[0] + 1 for r in lg]
fig, ax = plt.subplots(figsize=(3.6, 1.45), dpi=300)
ax.plot(t, np.array(n) / 1e6, color=ACC, lw=1.4)
ax.set_ylabel("entries (millions)", fontsize=6.5)
ax.xaxis.set_major_locator(mdates.MonthLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.annotate("≈ 2.54 M on 29 Sep", (t[-1], n[-1] / 1e6), (-4, -2), textcoords="offset points", ha="right", va="top", fontsize=6, color=INK)
ax.set_ylim(0, 2.8); ax.grid(axis="y", color=RULE, lw=.4)
fig.subplots_adjust(.16, .2, .97, .95); fig.savefig(OUT / "log_growth.svg"); plt.close(fig)

# ---------- F5: the agent correspondence graph (addressed messages only) ----------
ch = json.load(open(DATA / "channel_messages.json"))
E = collections.Counter(); sent = collections.Counter()
for m in ch["messages"]:
    for to in m["to"]:
        E[(m["attester"], to)] += 1; sent[m["attester"]] += 1
Gr = nx.DiGraph()
for (a, b), w in E.items(): Gr.add_edge(a, b, w=w)
comps = sorted(nx.weakly_connected_components(Gr), key=len, reverse=True)
H = Gr.subgraph(comps[0]).copy()
Eh = {k: v for k, v in E.items() if k[0] in H and k[1] in H}
pos = nx.kamada_kawai_layout(H.to_undirected(), scale=1)
pos = {k: (v[0] * 1.7, v[1]) for k, v in pos.items()}
fig, ax = plt.subplots(figsize=(3.6, 2.0), dpi=300)
for (a, b), w in Eh.items():
    ax.annotate("", pos[b], pos[a], arrowprops=dict(arrowstyle="-|>,head_length=.25,head_width=.12", lw=.25 + .7 * np.log10(w + 1),
                color=GRAY, alpha=.9, shrinkA=2.5, shrinkB=2.5))
own = ch.get("own_attester", "k572x7go")
vol = {nd: sent[nd] + H.in_degree(nd, weight="w") for nd in H.nodes}
for nd in H.nodes:
    ax.scatter(*pos[nd], s=4 + 2.2 * np.sqrt(vol[nd]), c=ACC if nd == own else INK, zorder=3, edgecolors="#FBFBF8", linewidths=.4)
ax.set_axis_off()
json.dump({"nodes": H.number_of_nodes(), "of": Gr.number_of_nodes(), "pairs": len(Eh), "notes": sum(Eh.values())}, open(OUT / "agent_graph.json", "w"))
fig.subplots_adjust(0, 0, 1, 1); fig.savefig(OUT / "agent_graph.svg"); plt.close(fig)
print("figures written to", OUT)
