# SAT-042 poster figure. Every value is parsed from work/sat_run1.out (the captured
# stdout of the satellite_downlink reference run) or read from the example source /
# emem-trace code where noted. Expects V (parsed run values) in the kernel.
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

NAVY, INK, INK2, MUTED, RULE = "#0E1A2B", "#141414", "#46463F", "#85857E", "#D3D3CC"
ACC, ACCS, AMB, AMBS, BAD, BADS = "#1F4FD8", "#E7ECFA", "#A86B00", "#FBF1DE", "#B3261E", "#F8E3E1"
SANS, MONO = "IBM Plex Sans", "IBM Plex Mono"
FS_BASE, FS_ANN, FS_TICK = 22, 18, 16   # three-size ladder, poster scale

apply_figure_style(frame="none", font=SANS, sizes=(FS_BASE, FS_ANN, FS_TICK))
mpl.rcParams["svg.fonttype"] = "path"   # glyphs as paths: renders identically without Plex installed

def short(tok, keep=8):
    head, cid = tok.rsplit(":", 1)
    return f"{head}:{cid[:keep]}…"

key8 = V["key"][:8] + "…"
n_layers = int(V["profile"][1])
drift = V["drift"]
n_cons = sum(d["verdict"] == "Consistent" for d in drift)
n_contra = sum(d["verdict"] == "Contradicted" for d in drift)
tamper_seq = int(V["tamper"][0].rsplit(" ", 1)[1])      # "chain broken at seq 3"
tampered_seg = 2                                          # satellite_downlink.rs:215 tampered.segments[2]
anchor, sigma = drift[0]["anchor"], 0.02                  # satellite_downlink.rs:198 anchor = (0.6402, 0.02)

fig = plt.figure(figsize=(20, 11.2))
fig.patch.set_facecolor("white")

# ---------------- panel a: the pass as a sequence ----------------
axA = fig.add_axes([0.02, 0.50, 0.96, 0.44]); axA.set_xlim(0, 7); axA.set_ylim(0, 1); axA.axis("off")
steps = [
    ("Enrol", "ENROLLED", ACC, f"key {key8}", f"{V['profile'][0]}", f"{n_layers} layers required"),
    ("Write, no trace", "REFUSED", BAD, "no OS execution", "trace presented", ""),
    ("Capture the pass", "SIGNED", ACC, f"{n_layers} layers chained", f"{V['n_admitted']} NDVI payloads", "bound in trace"),
    ("Smuggle a 4th fact", "REFUSED", BAD, "payload digest", V["unbound_digest"][:8] + "…", "not bound"),
    ("Honest batch", "ADMITTED", ACC, f"{V['n_admitted']} facts, 1 trace", short(V["trace_token"]), short(V["bundle_token"])),
    ("Score vs anchor", "SCORED", AMB, f"{n_cons} consistent", f"{n_contra} contradicted", f"anchor {anchor:.4f}"),
    ("Rewrite one log", "CAUGHT", BAD, f"segment {tampered_seg} edited", f"chain broken", f"at seq {tamper_seq}"),
]
axA.plot([0.5, 6.5], [0.80, 0.80], color=RULE, lw=4, zorder=0, solid_capstyle="round")
for i, (what, verdict, col, l1, l2, l3) in enumerate(steps):
    x = i + 0.5
    axA.plot([x], [0.80], "o", ms=52, color=col, zorder=2)
    axA.text(x, 0.80, str(i + 1), ha="center", va="center", color="white", fontsize=FS_BASE, fontweight="bold", zorder=3)
    axA.text(x, 0.66, what, ha="center", va="center", color=INK, fontsize=FS_BASE, fontweight="semibold")
    chip_fc = {ACC: ACCS, BAD: BADS, AMB: AMBS}[col]
    axA.add_patch(FancyBboxPatch((x - 0.40, 0.49), 0.80, 0.10, boxstyle="round,pad=0.0,rounding_size=0.03",
                                 fc=chip_fc, ec=col, lw=2))
    axA.text(x, 0.54, verdict, ha="center", va="center", color=col, fontsize=FS_ANN, fontweight="bold")
    for j, line in enumerate([l1, l2, l3]):
        mono = ("…" in line) or line.startswith(("orbital", "emem:"))
        axA.text(x, 0.36 - j * 0.115, line, ha="center", va="center", color=INK2,
                 fontsize=FS_TICK, family=MONO if mono else SANS)
axA.text(0.0, 1.0, "One pass of SAT-042 over Nile Delta cropland: two writes refused, one tamper caught",
         transform=axA.transAxes, ha="left", va="top", fontsize=FS_BASE, color=INK)
axA.text(-0.005, 1.0, "a", transform=axA.transAxes, ha="right", va="top", fontsize=FS_BASE + 4, fontweight="bold")

# ---------------- panel b: the signed trace and the tamper ----------------
axB = fig.add_axes([0.02, 0.08, 0.56, 0.36]); axB.set_xlim(0, 8.5); axB.set_ylim(0, 1); axB.axis("off")
axB.text(0.0, 1.0, f"The trace chains {n_layers} captured layers and binds each payload",
         transform=axB.transAxes, ha="left", va="top", fontsize=FS_BASE, color=INK)
axB.text(-0.009, 1.0, "b", transform=axB.transAxes, ha="right", va="top", fontsize=FS_BASE + 4, fontweight="bold")
layer_names = {"SensorBus": "sensor bus"}
w, h, y0 = 0.91, 0.22, 0.52
for k, lay in enumerate(V["layers"]):
    x = 0.1 + k * 1.045
    bad = (k == tampered_seg)
    axB.add_patch(FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0.0,rounding_size=0.04",
                                 fc=BADS if bad else ACCS, ec=BAD if bad else ACC, lw=2.5 if bad else 1.5))
    axB.text(x + w / 2, y0 + h * 0.64, layer_names.get(lay, lay.lower()), ha="center", va="center",
             fontsize=FS_TICK, color=INK)
    axB.text(x + w / 2, y0 + h * 0.25, f"seq {k}", ha="center", va="center", fontsize=FS_TICK,
             color=BAD if bad else INK2, family=MONO)
    if k < len(V["layers"]) - 1:
        x1, x2 = x + w, x + 1.045
        broken = (k + 1 == tamper_seq)
        axB.annotate("", xy=(x2, y0 + h / 2), xytext=(x1, y0 + h / 2),
                     arrowprops=dict(arrowstyle="-|>", color=BAD if broken else INK2, lw=2.5 if broken else 1.5))
        if broken:
            axB.text((x1 + x2) / 2, y0 + h + 0.07, "×", ha="center", va="center", color=BAD,
                     fontsize=FS_BASE, fontweight="bold")
axB.text(0.1 + tampered_seg * 1.045 + w / 2, y0 - 0.09, "log rewritten after signing", ha="center", va="center",
         color=BAD, fontsize=FS_TICK)
axB.text(0.1 + tamper_seq * 1.045 + w / 2 + 0.55, y0 + h + 0.07, f"verifier: chain broken at seq {tamper_seq}",
         ha="left", va="center", color=BAD, fontsize=FS_TICK)
# outputs bound into the signed preimage
axB.text(0.1, 0.24, "the signature covers the digest of each emitted payload", ha="left", va="center", fontsize=FS_TICK, color=INK2)
for k, d in enumerate(drift):
    x = 0.1 + k * 2.1
    axB.add_patch(FancyBboxPatch((x, 0.02), 1.95, 0.14, boxstyle="round,pad=0.0,rounding_size=0.04",
                                 fc="white", ec=ACC, lw=1.5))
    axB.text(x + 0.975, 0.09, f"NDVI {d['device']:.4f}", ha="center", va="center", fontsize=FS_TICK, color=INK, family=MONO)
axB.add_patch(FancyBboxPatch((0.1 + 3 * 2.1, 0.02), 1.95, 0.14, boxstyle="round,pad=0.0,rounding_size=0.04",
                             fc=BADS, ec=BAD, lw=1.5, ls="--"))
axB.text(0.1 + 3 * 2.1 + 0.975, 0.09, "4th fact: unbound", ha="center", va="center", fontsize=FS_TICK, color=BAD)

# ---------------- panel c: drift anchor scores ----------------
axC = fig.add_axes([0.66, 0.165, 0.32, 0.235])
axC.text(0.0, 1.42, "The drift anchor flags the outlier claim", transform=axC.transAxes, ha="left", va="top",
         fontsize=FS_BASE, color=INK)
axC.text(-0.035, 1.42, "c", transform=axC.transAxes, ha="right", va="top", fontsize=FS_BASE + 4, fontweight="bold")
axC.axvspan(0, 0.5, color=ACCS, zorder=0); axC.axvspan(0.5, 0.75, color=AMBS, zorder=0); axC.axvspan(0.75, 1.0, color=BADS, zorder=0)
for xz, lab, col in [(0.25, "consistent", ACC), (0.625, "tension", AMB), (0.875, "contradicted", BAD)]:
    axC.text(xz, 1.06, lab, transform=axC.get_xaxis_transform(), ha="center", va="bottom", fontsize=FS_TICK, color=col)
ys = np.arange(len(drift))[::-1]
for y, d in zip(ys, drift):
    col = BAD if d["verdict"] == "Contradicted" else ACC
    axC.plot([0, d["score"]], [y, y], color=col, lw=2.5, zorder=2)
    axC.plot(d["score"], y, "o", ms=14, color=col, zorder=3)
    axC.text(d["score"] + 0.03 if d["score"] < 0.8 else d["score"] - 0.03, y + 0.30, f"{d['score']:.2f}",
             ha="left" if d["score"] < 0.8 else "right", va="center", fontsize=FS_TICK, color=col, fontweight="bold")
axC.set_yticks(ys); axC.set_yticklabels([f"device {d['device']:.4f}" for d in drift], family=MONO)
axC.set_xlim(0, 1.0); axC.set_ylim(-0.6, len(drift) - 0.3)
axC.set_xticks([0, 0.5, 0.75, 1.0]); axC.set_xticklabels(["0", "0.5", "0.75", "1"])
axC.set_xlabel(f"contradiction score vs anchor NDVI {anchor:.4f} ± {sigma}", fontsize=FS_TICK)
for s in ("left", "top", "right"): axC.spines[s].set_visible(False)
axC.spines["bottom"].set_visible(True); axC.tick_params(axis="y", length=0)

fig.text(0.02, 0.012, "emem SAT-042 reference run (satellite_downlink example, emem commit 04b40c5), run 2026-09-30 19:14 UTC. "
         "Deterministic: fixed key, clocks, capture digests and anchor value.",
         ha="left", va="bottom", fontsize=FS_TICK, color=MUTED)
