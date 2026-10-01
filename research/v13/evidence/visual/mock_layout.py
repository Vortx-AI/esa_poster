"""v13 A0 page-composition mock (841 x 1189 mm), drawn 1:1 in mm with real point sizes.

Not the poster: a block diagram with miniatures built from the committed data, to test hierarchy,
grid and figure dominance. Output: v13/mock_layout.png (+ mock_layout_3m.png, a 3 m acuity simulation).
"""
import json
import struct
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon
from PIL import Image, ImageFilter

REPO = Path("/home/user/esa_poster")
DATA = REPO / "research/repro/data"
HERE = Path(__file__).parent
for f in (HERE / "plex/ttf").glob("*.ttf"):
    fm.fontManager.addfont(str(f))
SANS, MONO = "IBM Plex Sans", "IBM Plex Mono"
mpl.rcParams.update({"font.family": SANS, "hatch.linewidth": 0.8})

# ---- palette (v13 semantic tokens; see 06_visual_system.md section 3) ----
INK, INK2, MUTED, RULE = "#222428", "#4A4D55", "#7A7D85", "#D5D6DA"
EMEM, EMEM_T, EMEM_L = "#0F5FA8", "#DCE8F5", "#7FB3E6"
HARM, HARM_T = "#D2481E", "#FADDD2"
INC, OOS = "#E8A317", "#9C9A92"
NAVY = "#203045"
AGA, AGB = "#7A5230", "#3D5566"

W, H = 841, 1189
M, COL, GUT = 20, 58.5, 9.0


def cx(i):
    return M + (i - 1) * (COL + GUT)


def span(i, j):
    return cx(j) + COL - cx(i)


fig = plt.figure(figsize=(W / 25.4, H / 25.4))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")
ax.add_patch(Rectangle((0, 0), W, H, fc="white", ec="none", zorder=-10))


def T(x, y, s, pt, w=400, c=INK, ha="left", va="top", fam=SANS, z=5, **kw):
    return ax.text(x, y, s, fontsize=pt, fontweight=w, color=c, ha=ha, va=va, family=fam, zorder=z, **kw)


def box(x, y, w, h, fc="none", ec=RULE, lw=0.8, z=1, hatch=None, r=0):
    if r:
        p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z, hatch=hatch)
    else:
        p = Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=z, hatch=hatch)
    ax.add_patch(p)
    return p


def panel(x, y, w, h, num, title, tier, note=""):
    ax.plot([x, x + w], [y, y], color=INK, lw=2.2, zorder=3)   # 0.8 mm section rule
    narrow = w < 300
    pt = 34 if narrow else 40
    T(x, y + 2.5, f"{num}", pt, 700, EMEM)
    off = 0 if not num else (12 if len(num) == 1 else 22) * pt / 34
    T(x + off, y + 2.5, title, pt, 600, INK)
    T(x + w, y + h - 1, f"{tier} · {w:.1f} × {h:.0f} mm" + (f" · {note}" if note else ""), 14, 500, MUTED, ha="right", va="bottom")


def grid_bin(name):
    raw = (DATA / f"keylong_{name}.bin").read_bytes()
    w_, h_ = struct.unpack_from("<II", raw, 8)
    return np.frombuffer(raw, dtype="<f4", offset=64).reshape(h_, w_).astype(float)


B2, B3, B4 = (grid_bin(b) for b in ("B02", "B03", "B04"))
rgb = np.dstack([B4, B3, B2]) / 10000.0
lo, hi = np.percentile(rgb, 1.0), np.percentile(rgb, 99.0)
tc = np.clip((rgb - lo) / (hi - lo), 0, 1) ** (1 / 1.35)
R0, C0 = 210, 223

# ================================================================ HEADER 0-172 (full bleed)
HB = 180
box(-3, -3, W + 6, HB + 3, fc=NAVY, ec="none", z=0)
img_x = cx(10)
ax.imshow(tc[0:453, 0:443], extent=(img_x, W + 3, HB, -3), interpolation="nearest", zorder=1, aspect="auto")
r_, c_ = R0 + 2, C0 + 2
px = img_x + (c_ / 443) * (W + 3 - img_x)
py = -3 + (r_ / 453) * (HB + 3)
box(px - 3, py - 3, 6, 6, ec="white", lw=1.6, z=3)
box(img_x, HB - 20, W + 3 - img_x, 20, fc="#000000", ec="none", z=2).set_alpha(0.62)
T(img_x + 4, HB - 17, "The record this board follows: NDVI 0.4709", 17, 600, "white", z=4)
T(img_x + 4, HB - 9.5, "10 m cell · Sentinel-2A L2A · Keylong · 25 Sep 2026", 14, 400, "#E6ECF3", z=4)
# QR tile
box(img_x + 6, 8, 44, 52, fc="white", ec="none", z=4)
box(img_x + 9, 11, 38, 38, fc="none", ec=INK, lw=1.0, z=5, hatch="....")
T(img_x + 28, 51.5, "TRY THIS TOKEN", 14, 700, INK, ha="center", z=6)
T(M, 13, "EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol\nfor AI Agents over Foundation-Model Embeddings", 56, 600, "#F3F6FA", z=4, linespacing=1.05)
T(M, 62, "Agents hand each other evidence\nreferences, not paraphrases.", 100, 700, "white", z=4, linespacing=0.96)
T(M, 139, "The receiver resolves, re-hashes, re-reads. A signature fixes the bytes, not the measurement.", 32, 500, EMEM_L, z=4)
T(M, 160, "Jaya Kumari · Avijeet Singh · Vortx AI   ·   Agentic AI for Earth Observation · ESA Φ-lab and BIFOLD · Berlin · Poster Session 1 · 19 Oct 2026", 20, 400, "#C9D3E0", z=4)
T(W - 4, HB - 1, "3 m tier: title 56 pt · hero 100 pt · boundary 32 pt", 14, 500, "#C9D3E0", ha="right", va="bottom", z=6)

# ================================================================ SPINE 180-372
SY, SH = 188, 190
panel(M, SY, span(1, 12), SH, "1", "What survives an agent handoff?", "3 m / 1 m", "the visual grammar of the board")
T(cx(7), SY + 5, "Agent B resolves the reference, re-hashes the record and re-reads the source.", 24, 500, INK2)
lanes = [("prose", "“NDVI was about 0.47 on 25 Sep”", "reads the text", "15 / 15", HARM),
         ("JSON", '{"ndvi": 0.4709, "date": "2026-09-25"}', "reads the fields", "15 / 15", HARM),
         ("retrieved text (RAG)", "“…field log: Keylong NDVI 0.47…”", "retrieves a passage", "R5", OOS),
         ("opaque id", "obs-7d1c44", "fetches the sender's record", "13 / 16", HARM),
         ("EMEM reference", "emem:fact:defi.zb572.xoso.zb1ec:oj5cecci…", "resolve · re-hash · bind · verify · log · recompute · re-read", "0 / 16", EMEM)]
ly0, lh, lg = SY + 26, 25.5, 4.0
# source + agent A block
box(M, ly0, 104, 5 * lh + 4 * lg, fc="#F4F5F7", ec="none", z=1)
ax.imshow(tc[R0:R0 + 5, C0:C0 + 5], extent=(M + 6, M + 56, ly0 + 56, ly0 + 6), interpolation="nearest", zorder=2)
box(M + 26, ly0 + 26, 10, 10, ec=EMEM, lw=2.4, z=3)
T(M + 6, ly0 + 60, "Sentinel-2A pixel,\n25 Sep 2026", 17, 500, INK2, linespacing=1.15)
box(M + 64, ly0 + 10, 30, 30, fc="white", ec=AGA, lw=2.4, z=2, r=6)
T(M + 79, ly0 + 25, "A", 40, 700, AGA, ha="center", va="center")
T(M + 6, ly0 + 82, "Agent A reads\nNDVI 0.4709\nand cites it", 24, 600, INK, linespacing=1.1)
xs = M + 112
for k, (name, snip, bdoes, out, oc) in enumerate(lanes):
    y = ly0 + k * (lh + lg)
    emem = name.startswith("EMEM")
    box(xs, y, 690 - 0, lh, fc=(EMEM_T if emem else "#F4F5F7"), ec="none", z=1)
    T(xs + 3, y + 3, name, 22, 700, EMEM if emem else INK)
    T(xs + 3, y + 14.5, snip, 15, 400, INK2, fam=MONO)
    T(xs + 300, y + lh / 2, bdoes, 17 if emem else 20, 500, EMEM if emem else INK2, va="center")
    T(xs + 600, y + lh / 2, out, 64, 700, oc, ha="right", va="center")
# corruption bar
cxb = xs + 205
box(cxb, ly0 - 3, 82, 5 * lh + 4 * lg + 6, fc=HARM_T, ec=HARM, lw=1.6, z=2)
T(cxb + 41, ly0 + 2, "adversary", 20, 700, HARM, ha="center")
T(cxb + 41, ly0 + 14, "one of 16 corruptions:\nvalue · cell · time\nband · unit · source\nderivation · stale\nsignature · pixel", 15, 400, INK, ha="center", linespacing=1.25)
box(xs + 285, ly0 - 3, 10, 5 * lh + 4 * lg + 6, fc="none", ec="none")
T(xs + 300, ly0 - 8, "Agent B", 20, 700, AGB)
T(xs + 600, ly0 - 8, "acted on corrupted evidence", 17, 600, INK2, ha="right")
# boundary
bx = xs + 610
box(bx, ly0 - 3, W - M - bx, 5 * lh + 4 * lg + 6, fc="#F1F0EC", ec=OOS, lw=1.2, z=2, hatch="//")
T(bx + 4, ly0 + 2, "no check\nreaches:", 20, 700, INK, linespacing=1.05, z=6)
T(bx + 4, ly0 + 30, "the entity\nmeant (M17)\n\nsensor\naccuracy\n\nthe decision", 17, 500, INK, linespacing=1.12, z=6)

# ================================================================ COLUMNS 382-1004
Y0 = 390
# ---- LEFT
x, w = cx(1), span(1, 3)
panel(x, Y0, w, 108, "2", "What a paraphrase loses", "1 m")
chain = ["0.4708994708994709", "“0.4709”", "“about 0.47”"]
for k, s in enumerate(chain):
    box(x + k * 64, Y0 + 22, 60, 16, fc="#F4F5F7", ec="none", r=3)
    T(x + k * 64 + 30, Y0 + 30, s, 15 if k == 0 else 20, 500, INK, ha="center", va="center", fam=MONO if k == 0 else SANS)
T(x, Y0 + 44, "Rounded to “0.47”, 5 of 5 receivers irrigated;\nhanded the reference, 10 of 10 held.", 24, 600, INK, linespacing=1.15)
T(x, Y0 + 72, "rule constructed so rounding flips it: irrigate if NDVI ≤ 0.4705;\nexploratory arm, one model pair (claude-haiku-4-5 as B)", 14, 400, INK2, linespacing=1.25)

panel(x, Y0 + 118, w, 284, "3", "Seven failures, one pattern", "1 m", "failure ladder")
rungs = [("signer read the pixel 10 m south", "162 / 200 records", "re-read", 3),
         ("tile edge read as 0: an EUDR pass", "every edge plot", "re-read", 3),
         ("people per pixel, not per km²", "1.77× low", "recompute", 2),
         ("newer record replaces the cited one", "0.4709 → 0.4237", "as-of", 1),
         ("place name moved the cell 597 m", "1 query", "bind cell", 1),
         ("asked 23 Sep, served 25 Sep", "9 / 10 agents", "bind time", 1),
         ("0.4709 retold as “0.47”", "5 / 5 flipped", "use value", 1)]
ry = Y0 + 140
for k, (what, n, chk, lvl) in enumerate(rungs):
    yy = ry + k * 36
    box(x, yy, w, 31, fc="#F7F7F5", ec="none")
    box(x, yy, 3, 31, fc=INC if k in (0, 1, 5, 4) else INK2, ec="none")
    T(x + 6, yy + 3, what, 17, 600, INK)
    T(x + 6, yy + 16, n, 20, 700, HARM)
    tint = {1: EMEM_T, 2: "#A9C7E8", 3: EMEM}[lvl]
    box(x + w - 58, yy + 15, 56, 12, fc=tint, ec="none", r=2)
    T(x + w - 30, yy + 21, f"L{lvl} {chk}", 14, 700, "white" if lvl == 3 else EMEM, ha="center", va="center")
T(x, ry + 7 * 36 + 1, "Binding catches the lower four at handoff;\nthe signer's own errors need recompute or re-read.", 17, 500, INK2, linespacing=1.2)

panel(x, Y0 + 412, w, 88, "", "Questions", "1 m / 30 cm")
for k, q in enumerate(["RQ1 Can a receiver detect a corrupted citation alone?  → 1, 5",
                       "RQ2 Which corruptions are detectable?  → 5",
                       "RQ3 Reference vs paraphrase, JSON, RAG?  → 1",
                       "RQ4 What stays unverifiable?  → 7",
                       "H1 rejects word-preserving mutations · H2 re-read · H3 as-of"]):
    T(x, Y0 + 430 + k * 9.5, q, 15, 500 if k < 4 else 400, INK if k < 4 else INK2)

panel(x, Y0 + 510, w, 106, "", "Threat model", "1 m / 30 cm")
box(x, Y0 + 528, 58, 40, fc="#F4F5F7", ec="none")
T(x + 29, Y0 + 542, "A", 30, 700, AGA, ha="center", va="center")
box(x + 68, Y0 + 528, 58, 40, fc=HARM_T, ec=HARM, lw=1.2)
T(x + 97, Y0 + 535, "relay can rewrite\nall it carries", 14, 600, INK, ha="center", linespacing=1.15)
box(x + 136, Y0 + 528, 57.5, 40, fc="#F4F5F7", ec="none")
T(x + 165, Y0 + 542, "B", 30, 700, AGB, ha="center", va="center")
T(x + 136 + 28.75, Y0 + 556, "pinned key ·\npublic COG", 14, 500, EMEM, ha="center", linespacing=1.1)
T(x, Y0 + 573, "cannot: sign under the pinned key; find a second\nrecord with the same address. Outside: a compromised\nkey, a wrong sensor, the entity meant.", 14, 400, INK2, linespacing=1.22)

# ---- CENTRE
x, w = cx(4), span(4, 9)
panel(x, Y0, w, 160, "4", "What is handed over", "1 m / 30 cm", "evidence object, exploded")
steps = [("SOURCE FILES", "B04 + B08 COGs\n277.9 + 281.9 MB\nrow 9443, col 9098", "#F4F5F7", INK, True),
         ("RECORD", "12 fields · 1,115 B\ncell · band · time · value\nsources · derivation", EMEM_T, INK, False),
         ("ADDRESS", "BLAKE3(record)\noj5ceccile62…\n52 characters", EMEM, "white", False),
         ("ATTESTATION", "Ed25519 over a\nbatch root · logged", "#E9EEF5", INK, False)]
for k, (h, b, fc, tc_, dashed) in enumerate(steps):
    bxx = x + k * 101
    p = box(bxx, Y0 + 22, 88, 70, fc=fc, ec=(INK2 if dashed else "none"), lw=1.2, r=3)
    if dashed:
        p.set_linestyle((0, (3, 2)))
    T(bxx + 5, Y0 + 26, h, 17, 700, tc_)
    T(bxx + 5, Y0 + 40, b, 15, 400, tc_, linespacing=1.25)
    if k < 3:
        ax.annotate("", xy=(bxx + 99, Y0 + 57), xytext=(bxx + 89, Y0 + 57), arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.4, mutation_scale=22))
T(x, Y0 + 100, "handed over (84 characters):", 15, 500, MUTED)
T(x, Y0 + 109, "emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa", 20, 500, EMEM, fam=MONO)
T(x, Y0 + 124, "The address names the record, not the satellite file. Dashed: named by URL,\nnot hashed (location-only).", 17, 500, INK2, linespacing=1.2)

panel(x, Y0 + 170, w, 255, "5", "Which check stops which corruption", "3 m / 1 m", "hero quantitative")
mm_ = json.load(open(REPO / "research/repro/v11/out/mutation_matrix.json"))
out = {(r["mutation"], r["level"]): r for r in mm_["rows"]}
fam_rows = [("value", ["M1", "M2", "M8"]), ("cell", ["M4", "M9"]), ("time", ["M10"]), ("band", ["M6"]),
            ("source", ["M11"]), ("derivation", ["M12", "M14"]), ("stale / current", ["M5", "M16"]),
            ("signature / id", ["M3", "M7", "M13"]), ("source pixel", ["M15"]), ("entity (out of scope)", ["M17"])]
cols = [("prose", "A"), ("JSON", "B"), ("RAG", None), ("opaque id", "C"), ("EMEM", "I")]
mx, my, cw, rh = x + 120, Y0 + 210, 44, 8.2
first = {m["id"]: m.get("first_protected_level") for m in mm_["meta"]["mutations"]}
for j, (cn, lv) in enumerate(cols):
    T(mx + j * (cw + 3) + cw / 2, my - 14, cn, 20, 700, EMEM if cn == "EMEM" else INK, ha="center")
T(mx + 5 * (cw + 3) + 16, my - 14, "first\ncheck", 14, 700, MUTED, ha="center", linespacing=1.0)
yy = my
for fam, ids in fam_rows:
    T(x, yy + 1, fam, 15, 700, MUTED)
    for mid in ids:
        T(x + 72, yy + 1, mid, 15, 700, INC if mid in ("M2", "M4", "M5", "M15", "M17") else INK2)
        for j, (cn, lv) in enumerate(cols):
            xx = mx + j * (cw + 3)
            if lv is None:
                box(xx, yy, cw, rh - 1.6, fc="white", ec=RULE, lw=0.6, hatch="..")
                continue
            r = out.get((mid, lv))
            if r is None or r["outcome"] == "n/a":
                box(xx, yy, cw, rh - 1.6, fc="#F2F2F0", ec="none")
                continue
            o = r["outcome"]
            fc = HARM if "corrupted" in o else (EMEM if "refused" in o else ("#EEF3FA" if o in ("unaffected", "acted correctly") else OOS))
            if mid == "M17":
                fc = HARM
            box(xx, yy, cw, rh - 1.6, fc=fc, ec="none")
        fl = first.get(mid)
        T(mx + 5 * (cw + 3) + 16, yy + (rh - 1.6) / 2, fl or "none", 15, 700, EMEM if fl else HARM, ha="center", va="center")
        yy += rh
    yy += 2.2
tot = {"A": "15/15", "B": "15/15", "C": "13/16", "I": "0/16"}
for j, (cn, lv) in enumerate(cols):
    T(mx + j * (cw + 3) + cw / 2, yy + 2, tot.get(lv, "R5"), 30, 700, (EMEM if lv == "I" else (OOS if lv is None else HARM)), ha="center")
T(x, yy + 4, "B acts on\ncorrupted evidence", 17, 700, HARM, linespacing=1.05)
T(x, Y0 + 170 + 255 - 14, "one record · one band · deterministic verifier, no model · T2 rows use a test key · RAG column only if R5 runs", 14, 400, INK2)

panel(x, Y0 + 435, w, 187, "6", "The right record, the wrong pixel", "3 m / 1 m", "real Sentinel-2, native 10 m")
ax.imshow(tc, extent=(x, x + 110, Y0 + 457 + 113, Y0 + 457), interpolation="nearest", zorder=2)
box(x + 110 * (C0 + 2 - 12.5) / 443, Y0 + 457 + 113 * (R0 + 2 - 12.5) / 453, 110 * 25 / 443, 113 * 25 / 453, ec="white", lw=1.4, z=3)
wx = x + 122
ax.imshow(tc[R0:R0 + 5, C0:C0 + 5], extent=(wx, wx + 105, Y0 + 457 + 105, Y0 + 457), interpolation="nearest", zorder=2)
nd = np.array(json.load(open(DATA / "v8/pixel_windows.json"))[next(k for k in json.load(open(DATA / "v8/pixel_windows.json")) if k.startswith("oj5"))]["ndvi_5x5"])
for i in range(5):
    for j in range(5):
        T(wx + 10.5 + j * 21, Y0 + 457 + 10.5 + i * 21, f"{nd[i, j]:.2f}", 15, 500, "white" if tc[R0 + i, C0 + j].mean() < .55 else INK, ha="center", va="center", z=4)
box(wx + 42, Y0 + 457 + 42, 21, 21, ec="white", lw=5, z=4)
box(wx + 42, Y0 + 457 + 42, 21, 21, ec=EMEM, lw=3, z=5)
box(wx + 42, Y0 + 457 + 63, 21, 21, ec="white", lw=5, z=4)
pp = box(wx + 42, Y0 + 457 + 63, 21, 21, ec=HARM, lw=3, z=5)
pp.set_linestyle((0, (2, 1)))
tx = wx + 115
T(tx, Y0 + 458, "named pixel", 17, 500, INK2)
T(tx, Y0 + 467, "0.4709 → hold", 30, 700, INK)
T(tx, Y0 + 484, "read pixel, 10 m south", 17, 500, INK2)
T(tx, Y0 + 493, "0.3016 → irrigate", 30, 700, HARM)
T(tx, Y0 + 512, "hash · bind · signature · log ·\nrecompute pass; only the re-read\nrefuses it", 17, 500, INK2, linespacing=1.2)
for k in range(200):
    i, j = divmod(k, 25)
    box(tx + j * 6.4, Y0 + 548 + i * 4.2, 5.4, 3.4, fc=HARM if k < 162 else RULE, ec="none", z=2)
T(tx, Y0 + 573, "162 of 200 sampled pre-fix records", 17, 700, INK)

# ---- RIGHT
x, w = cx(10), span(10, 12)
panel(x, Y0, w, 205, "7", "What the checks establish", "1 m", "ladder L0-L5")
rungs7 = [("L5", "physical truth, the decision", "INHERITED / OUT", OOS),
          ("L4", "the entity meant", "OUT OF SCOPE", OOS),
          ("L3", "the named source pixel", "PARTIAL", "#A9C7E8"),
          ("L2", "derivation recomputes", "RECOMPUTABLE", EMEM_L),
          ("L1", "cell, band, time match", "CHECKABLE", EMEM),
          ("L0", "the bytes that were signed", "CHECKABLE", EMEM)]
for k, (l, what, st, fc) in enumerate(rungs7):
    yy = Y0 + 24 + k * 26
    box(x, yy, w, 22, fc=fc, ec="none", hatch="//" if fc == OOS else None)
    T(x + 3, yy + 3, l, 20, 700, "white" if fc in (EMEM,) else INK, z=6)
    T(x + 22, yy + 3, what, 15, 600, "white" if fc in (EMEM,) else INK, z=6)
    T(x + 22, yy + 12.5, st, 14, 700, "white" if fc in (EMEM,) else INK2, z=6)
T(x, Y0 + 184, "780 / 780 re-hashed and signature-checked;\n266 / 780 recomputed; 0 sources hashed", 14, 500, INK2, linespacing=1.2)

panel(x, Y0 + 215, w, 140, "8", "Same place, different time", "1 m", "as-of memory")
ty = Y0 + 255
ax.plot([x, x + w], [ty + 40, ty + 40], color=INK2, lw=1.4)
for lab_, frac in (("May", 0.05), ("Jun", 0.27), ("Aug", 0.62), ("Sep", 0.9)):
    T(x + frac * w, ty + 43, lab_, 14, 500, MUTED, ha="center")
box(x + 0.08 * w, ty + 4, 0.92 * w, 11, fc=EMEM_T, ec="none")
T(x + 0.08 * w + 2, ty + 5, "918.0 m  signed 28 May", 15, 700, EMEM)
box(x + 0.62 * w, ty + 19, 0.38 * w, 11, fc="#A9C7E8", ec="none")
T(x + 0.62 * w + 2, ty + 20, "915.07 m  11 Aug", 15, 700, INK)
ax.plot([x + 0.3 * w] * 2, [ty - 6, ty + 38], color=HARM, lw=2.0, ls=(0, (3, 2)))
T(x + 0.3 * w + 2, ty - 8, "as of 15 Jun → 918.0 m", 17, 700, INK, va="bottom")
T(x, Y0 + 315, "A newer record does not overwrite\nthe one an agent cited.", 17, 600, INK, linespacing=1.15)

panel(x, Y0 + 365, w, 125, "9", "A screen an auditor can re-run", "1 m", "Rondônia")
rr = json.load(open(REPO / "research/repro/v12/data/case_rondonia_eudr.json"))
cat_style = {"eudr_flag_forest_2020_loss_after_2020": (HARM, "o", 7), "forest_2020_no_later_loss": (EMEM, "o", 4),
             "cleared_2001_2020": (INK2, "^", 4), "not_forest_2020_no_hansen_loss": (OOS, ".", 4), "loss_after_2020_on_gfc2020_non_forest": (INC, "D", 5)}
cats = [r_.get("eudr_category") for r_ in sorted(rr["rows"], key=lambda q: (q["row"], q["col"]))]
for k, cat in enumerate(cats):
    i, j = divmod(k, 10)
    c_, mk, ms = cat_style.get(cat, (OOS, ".", 3))
    ax.plot(x + 6 + j * 8, Y0 + 388 + i * 8, marker=mk, color=c_, ms=ms, mew=0, zorder=4)
T(x + 90, Y0 + 388, "3 flagged: forest in 2020,\nloss after 2020", 15, 700, HARM, linespacing=1.15)
T(x + 90, Y0 + 412, "100 point samples,\n740 m apart, 600 facts", 15, 500, INK2, linespacing=1.15)
T(x, Y0 + 470, "Point samples, not parcel polygons;\nnot a regulatory determination.", 15, 700, INK, linespacing=1.15)

panel(x, Y0 + 500, w, 122, "10", "What it costs", "1 m / 30 cm", "log scales")
rows10 = [("context tokens (cl100k)", [(8, "bare value"), (46, "reference"), (65, "A's prose (mean)"), (562, "record as JSON"), (18659, "18-tool MCP list")], 3, 30000),
          ("bytes moved", [(84, "reference"), (1115, "record (CBOR)"), (1165033, "cold source re-read"), (2.02e9, "whole scene")], 30, 1e10),
          ("milliseconds", [(1.187, "offline check"), (224, "resolve, median of 11 paths")], 0.5, 3000)]
yy = Y0 + 522
for unit, pts, a, b in rows10:
    T(x, yy, unit, 14, 700, MUTED)
    yy += 6.5
    for v, lab_ in pts:
        fx = x + 70 + (np.log10(v) - np.log10(a)) / (np.log10(b) - np.log10(a)) * (w - 76)
        ax.plot([x + 70, x + w - 6], [yy, yy], color=RULE, lw=0.8, zorder=2)
        ax.plot(fx, yy, "o", color=EMEM if lab_ in ("reference", "offline check", "cold source re-read") else INK2, ms=6, zorder=4)
        T(x, yy, lab_, 14, 500, INK2, va="center")
        yy += 5.6
    yy += 2.5
T(x, Y0 + 612, "46 tokens per reference vs 8 per value", 15, 700, INK)

# ================================================================ BOTTOM 1014-1172
BY = 1014
x, w = cx(1), span(1, 8)
panel(x, BY, w, 158, "11", "One evidence protocol, multiple agent runtimes", "1 m", "ecosystem bridge, typographic")
nodes = [("signed observation", "emem:fact:…", EMEM), ("MCP · A2A", "transport", INK2), ("agent host", "Claude Code · Gemini CLI\nDify · ChatGPT (check)", INK2), ("next agent / app", "resolves, re-checks", AGB)]
for k, (h, b, c_) in enumerate(nodes):
    bxx = x + k * 132
    box(bxx, BY + 22, 116, 34, fc=(EMEM if k == 0 else "#F4F5F7"), ec="none", r=4)
    T(bxx + 5, BY + 25, h, 20, 700, "white" if k == 0 else c_)
    T(bxx + 5, BY + 38, b, 14, 500, "white" if k == 0 else INK2, linespacing=1.15)
    if k < 3:
        ax.annotate("", xy=(bxx + 130, BY + 39), xytext=(bxx + 117, BY + 39), arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.4, mutation_scale=20))
groups = [("LIVE CLIENTS", "Claude Code · Claude plugin · Gemini CLI · Dify"), ("PROTOCOL / DISCOVERY", "MCP · A2A · MCP Registry · GitHub MCP Registry · GitHub · Glama"),
          ("SDK / API", "pip install ememdev · npm i @vortxai/emem · REST · Docker"), ("FRAMEWORKS (examples)", "LlamaIndex · AutoGen · Agno · CrewAI · Mastra · LangChain")]
for k, (g, s) in enumerate(groups):
    T(x, BY + 64 + k * 11, g, 14, 700, MUTED)
    T(x + 70, BY + 64 + k * 11, s, 15, 500, INK)
# cross-runtime dot plot
cr = json.load(open(DATA / "v8/crossruntime_table.json"))
paths = [(r_["path"], r_["ms_median"]) for r_ in cr["rows"]["ndvi_keylong"] if r_.get("ms_median")]
dpx, dpw = x + 360, 165
T(dpx, BY + 62, "one token, 11 client paths, 1 CID, 1 value", 15, 700, INK)
for k, (pth, ms) in enumerate(sorted(paths, key=lambda t: t[1])):
    yy = BY + 75 + k * 6.6
    fx = dpx + 60 + (np.log10(ms) - 1.5) / (3.2 - 1.5) * (dpw - 60)
    ax.plot([dpx + 60, fx], [yy, yy], color=RULE, lw=1.0)
    ax.plot(fx, yy, "o", color=EMEM, ms=5, zorder=4)
    T(dpx, yy, pth.split("_", 1)[1][:16], 14, 400, INK2, va="center")
T(x, BY + 150, "checked 2026-10-01; directory listings are not integrations; marks as text per brand rules", 14, 400, MUTED, va="bottom")

x, w = cx(9), span(9, 12)
panel(x, BY, w, 96, "12", "Seven layers, one question each", "1 m / 30 cm")
lanes12 = ["JUDGE  GeoGuard", "CARRY  MCP · A2A", "RETRIEVE  RAG", "SIGN FILES  C2PA", "LINEAGE  PROV", "RUN  openEO", "FIND  STAC"]
for k, s in enumerate(lanes12):
    yy = BY + 20 + k * 9.5
    box(x, yy, w, 8, fc="#F4F5F7", ec="none")
    T(x + 3, yy + 4, s, 15, 600, INK, va="center")
ax.plot([x + w - 40] * 2, [BY + 18, BY + 88], color=EMEM, lw=5)
T(x + w - 36, BY + 52, "EMEM:\nthe cited\nobservation", 14, 700, EMEM, va="center", linespacing=1.1)
box(x, BY + 104, w, 68, fc=EMEM_T, ec="none")
T(x + 4, BY + 107, "EMEM lets agents hand off a reference to\nan observation that the receiver can re-check;\nour mutation tests show which corruptions it\ncatches. Sensor accuracy and the entity\nmeant remain separate questions.", 17, 600, INK, linespacing=1.18)

# ================================================================ FOOTER
T(M, 1176.5, "References · methods · claims map: QR READ THE METHODS · every number maps to a file and script · fonts IBM Plex (OFL) · data retrieved 2026-09-29 to 2026-10-01", 14, 400, MUTED)

# grid overlay (columns) for the mock only
for i in range(1, 13):
    ax.add_patch(Rectangle((cx(i), 0), COL, H, fc="#0F5FA8", ec="none", alpha=0.035, zorder=0.5))
fig.savefig(HERE / "mock_layout.png", dpi=60, facecolor="white")

# 3 m acuity simulation: 1 arcmin at 3 m = 0.873 mm -> one pixel per 0.873 mm, then a 1-pixel blur
im = Image.open(HERE / "mock_layout.png").convert("RGB")
px_mm = im.width / W
small = im.resize((int(W / 0.873), int(H / 0.873)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
small.resize(im.size, Image.BICUBIC).save(HERE / "mock_layout_3m.png")
print("ok", im.size)
