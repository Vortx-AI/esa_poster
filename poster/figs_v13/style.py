"""Shared style for every v13 figure (palette and type from research/v13/06_visual_system.md §3, brief §E).
Every figure is drawn 1:1 at its board size in mm; text sizes are true points on the printed A0."""
import os, matplotlib
matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FONTS = os.path.join(ROOT, "poster", "fonts", "plex-full")
OUT = os.path.join(ROOT, "poster", "fig", "v13")
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(FONTS):
    if f.endswith(".ttf"):
        font_manager.fontManager.addfont(os.path.join(FONTS, f))

C = dict(
    emem="#0F5FA8", emem_tint="#DCE8F5", emem_light="#7FB3E6",
    harm="#D2481E", harm_text="#B5401A", harm_tint="#FADDD2",
    incident="#E8A317", incident_text="#8A5A00",
    oos="#9C9A92", oos_bg="#F1F0EC",
    agentA="#7A5230", agentB="#3D5566",
    ink="#222428", ink2="#4A4D55", muted="#7A7D85", rule="#D5D6DA",
    navy="#203045", paper="#FFFFFF",
    unaffected="#EEF3FA", na="#F2F2F0",
    L0="#8FB5E0", L1="#5B8FCB", L2="#0F5FA8", L3="#0B4A86",
)
# type scale in pt (brief §A.2): never below FLOOR
PT = dict(hero=100, numeral=64, title=56, headline=44, headline_s=32, body=24, label=20, caption=17, floor=14)
FLOOR = 14
MM = 1 / 25.4

plt.rcParams.update({
    "font.family": "IBM Plex Sans", "font.size": PT["label"], "text.color": C["ink"],
    "axes.edgecolor": C["ink2"], "axes.labelcolor": C["ink"], "xtick.color": C["ink2"], "ytick.color": C["ink2"],
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 1.0,
    "svg.fonttype": "none", "pdf.fonttype": 42, "figure.facecolor": C["paper"], "savefig.facecolor": C["paper"],
})
MONO = "IBM Plex Mono"


def fig_mm(w_mm, h_mm):
    """A figure exactly w x h mm."""
    return plt.figure(figsize=(w_mm * MM, h_mm * MM))


def check_text(fig, floor=FLOOR):
    """Fail on any text below the floor, clipped outside the canvas, or overlapping another text."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer(); W, H = fig.canvas.get_width_height()
    boxes = []
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not t.get_text().strip():
            continue
        if t.get_fontsize() < floor - 1e-6:
            raise AssertionError(f"text below {floor} pt: {t.get_text()!r} {t.get_fontsize()}")
        bb = t.get_window_extent(r)
        if bb.x0 < -1 or bb.y0 < -1 or bb.x1 > W + 1 or bb.y1 > H + 1:
            raise AssertionError(f"text clipped: {t.get_text()!r}")
        boxes.append((t.get_text(), bb))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i][1], boxes[j][1]
            if a.overlaps(b) and a.width > 0 and b.width > 0:
                ov = (min(a.x1, b.x1) - max(a.x0, b.x0)) * (min(a.y1, b.y1) - max(a.y0, b.y0))
                if ov > 4:   # px^2 tolerance
                    raise AssertionError(f"overlapping labels: {boxes[i][0]!r} / {boxes[j][0]!r}")


def save(fig, name):
    check_text(fig)
    for ext in ("svg", "png"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=300)   # 300 also for SVG so embedded rasters are not resampled to 72 ppi
    plt.close(fig)
    print("wrote", name)
