"""F2: complete handoff experiment, 801 x 118 mm at A0 print size.

Recovered from 2686b27: source pixel, sender, five handoff forms, mutation,
receiver checks, measured outcomes and limits. Current final R5 evidence
replaces obsolete statistics; the second outcome is genuine-control
correctness, not corruption rejection. No duplicate QR. The R1 fallback
retains its deterministic-receiver label. Snippets come from experiment code.
"""
import datetime as dt
import json
import math
import os
import re
import struct
import sys
from pathlib import Path

import numpy as np
from matplotlib import patheffects as pe
from matplotlib.collections import PatchCollection
from matplotlib.lines import Line2D
from matplotlib.path import Path as MPath
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as S  # noqa: E402

ROOT = Path(S.ROOT)
DATA = ROOT / "research/repro/data"
R5_DIR = ROOT / "research/repro/v13/r5"
sys.path.insert(0, str(ROOT / "research/repro/v11"))
import mutation_suite as R1  # noqa: E402

C, PT = S.C, S.PT
W, H = 801.0, 118.0
NAME = "f2_spine"
MMPT = 72 / 25.4                  # points per mm (line widths)
THIN = " "
LABELS = []
CLAIMS = {r["id"]: r for r in json.loads((ROOT / "research/v13/12_claims_map.json").read_text())["rows"]}
for ADD in sorted((ROOT / "research/v13").glob("12_claims_map_additions_*.json")):
    CLAIMS.update({r["id"]: r for r in json.loads(ADD.read_text()).get("rows", [])})


def T(ax, x, y, s, claim, **kw):
    assert claim in CLAIMS, f"no claim row {claim} for {s!r}"
    LABELS.append({"text": s, "claim": claim, "x_mm": round(x, 2), "y_mm": round(y, 2), "pt": kw.get("fontsize")})
    return ax.text(x, y, s, **kw)


def text_w(ax, s, **kw):
    """Width of a text in mm at print size."""
    t = ax.text(0, 0, s, **kw)
    r = ax.figure.canvas.get_renderer()
    w = t.get_window_extent(r).width / ax.figure.dpi * 25.4
    t.remove()
    return w


def hatch(ax, x, y, w, h, pitch=1.6, z=1):
    """45 degree hatch (oos on oos_bg), segments clipped analytically to the box (crisp in SVG)."""
    from matplotlib.collections import LineCollection
    ax.add_patch(Rectangle((x, y), w, h, fc=C["oos_bg"], ec="none", zorder=z))
    segs, step, k = [], pitch * math.sqrt(2), -h
    while k < w:
        # line through (x + k, y + h) going up-right at 45 degrees: points (x + k + t, y + h - t), t in [0, h]
        t0, t1 = max(0.0, -k), min(h, w - k)
        if t1 > t0:
            segs.append([(x + k + t0, y + h - t0), (x + k + t1, y + h - t1)])
        k += step
    ax.add_collection(LineCollection(segs, colors=C["oos"], linewidths=0.35 * MMPT, zorder=z + 0.1))


def fmt_frac(k, n):
    return f"{k}{THIN}/{THIN}{n}"


# ------------------------------------------------------------------ data: R1 (always) and R5 (if final)
MM = json.loads((ROOT / "research/repro/v11/out/mutation_matrix.json").read_text())
SUM = MM["summary"]
RULE = float(re.search(r"<=\s*([0-9.]+)", MM["meta"]["rule"]).group(1))
assert RULE == R1.RULE
GEN = R1.genuine()
assert GEN["record"]["value"] == MM["meta"]["genuine_value"]
TOKEN = GEN["token"]
TSLOT = GEN["question"]["tslot"]
DATE = dt.date(1970, 1, 1) + dt.timedelta(days=TSLOT)
N_MUT = len([m for m in MM["meta"]["mutations"] if m["id"] not in ("G0", "M17")])
FAMILIES = "value · cell · time · band · source · derivation · stale state · signature · pixel"


def r5_results():
    """Return the parsed R5 results if final, else None. Accepts {k, n} objects or 'k/n' strings."""
    p = Path(os.environ.get("F2_R5_RESULTS", R5_DIR / "results.json"))   # env override: layout tests only
    if not p.exists():
        return None
    r = json.loads(p.read_text())
    final = r.get("final") is True or str(r.get("status", "")).lower() == "final"
    if not final:
        return None
    ph = R5_DIR / "prereg_hash.txt"
    if r.get("prereg_blake3") and ph.exists():
        if r["prereg_blake3"].strip() not in ph.read_text():
            raise SystemExit("R5 results name a prereg hash that differs from prereg_hash.txt: refusing R5 mode")

    def kn(cond):
        v = r["primary"][cond]["pooled_claude"]["false_accept"]
        if isinstance(v, str):
            k, n = (int(x) for x in v.replace(" ", "").split("/"))
        else:
            k, n = int(v["k"]), int(v["n"])
        planned = r["primary"][cond]["pooled_claude"].get("planned_n")
        return k, n, planned
    models = r.get("models", [])
    dates = r.get("dates", "")
    return {"A": kn("A"), "B": kn("B"), "C": kn("C"), "D": kn("D"), "E0": kn("E0"), "E": kn("E"),
            "Eplus": kn("Eplus") if "Eplus" in r["primary"] else kn("E+"),
            "models": ", ".join(models) if isinstance(models, list) else str(models),
            "dates": " to ".join(dates) if isinstance(dates, list) else str(dates)}


R5 = r5_results()
MODE = "R5" if R5 else "fallback"


def snippets():
    """The handoff text of the genuine record (G0) as each form carries it, rendered by the experiment's code."""
    if MODE == "R5":
        sys.path.insert(0, str(R5_DIR))
        import items as IT  # noqa: E402
        g0 = next(i for i in IT.build_items() if i["id"] == "G0")
        return {"prose": IT.prose(g0), "json": IT.json_handoff(g0), "rag": IT.answer_passage(g0),
                "opaque": f"record ref {IT.OPAQUE_REF}", "emem": TOKEN}
    rec = GEN["record"]
    return {"prose": f"“NDVI {GEN['stated']}, {DATE.day} {DATE:%b %Y}”",
            "json": json.dumps({"band": rec["band"], "value": rec["value"]}),
            "opaque": f"id {TOKEN.split(':')[3]}",
            "emem": TOKEN}


def clip_to(ax, s, width_mm, **kw):
    if text_w(ax, s, **kw) <= width_mm:
        return s
    while s and text_w(ax, s + "…", **kw) > width_mm:
        s = s[:-1]
    return s + "…"


# lanes: (key, name, B does, outcome (k, n), colour, R1 ceiling for the ghost square)
def lanes():
    if MODE == "fallback":
        return [("prose", "prose", "reads the text", (SUM["A"]["false_accepts"], SUM["A"]["applicable"]), None),
                ("json", "JSON", "reads the fields", (SUM["B"]["false_accepts"], SUM["B"]["applicable"]), None),
                ("opaque", "opaque id", "fetches the sender’s record",
                 (SUM["C"]["false_accepts"], SUM["C"]["applicable"]), None),
                ("emem", "EMEM reference", None, (SUM["I"]["false_accepts"], SUM["I"]["applicable"]), None)]
    ceil = {k: (SUM[k]["false_accepts"], SUM[k]["applicable"]) for k in "ABCI"}
    return [("prose", "prose", "reads the text", R5["A"][:2], ceil["A"]),
            ("json", "JSON", "reads the fields", R5["B"][:2], ceil["B"]),
            ("rag", "retrieved text (RAG)", "retrieves a passage", R5["C"][:2], None),
            ("opaque", "opaque id", "fetches the sender’s record", R5["D"][:2], ceil["C"]),
            ("emem", "EMEM reference", None, R5["E"][:2], ceil["I"])]


# the real 5 x 5 window of the record, true colour from the signed grids (same processing as F1)
def grid(name):
    raw = (DATA / f"keylong_{name}.bin").read_bytes()
    assert raw[:8] == b"EMEMGRD1"
    w, h = struct.unpack_from("<II", raw, 8)
    return np.frombuffer(raw, dtype="<f4", offset=64).reshape(h, w).astype(float)


B2, B3, B4, B8 = (grid(b) for b in ("B02", "B03", "B04", "B08"))
PW = json.loads((DATA / "v8/pixel_windows.json").read_text())
WIN = next(v for k, v in PW.items() if k.startswith("oj5cecci"))
R0, C0 = 210, 223
assert np.array_equal(B4[R0:R0 + 5, C0:C0 + 5], np.array(WIN["B04"]) - 1000)
assert np.array_equal(B8[R0:R0 + 5, C0:C0 + 5], np.array(WIN["B08"]) - 1000)
RGB = np.dstack([B4, B3, B2]) / 10000.0
LO, HI = np.percentile(RGB, 1.0), np.percentile(RGB, 99.0)
TC = np.clip((RGB - LO) / (HI - LO), 0, 1) ** (1 / 1.35)
WIN_TC = np.repeat(np.repeat(TC[R0:R0 + 5, C0:C0 + 5], 120, 0), 120, 1)   # x120 nearest: 10 mm per pixel, 305 ppi
cc, cr = WIN["centre_col_row"]
oc, orr = WIN["window_origin_col_row"]
NAMED = (int(math.floor(cr)) - orr, int(math.floor(cc)) - oc)
assert NAMED == (2, 2)
VALUE = R1.ndvi(B8[R0 + 2, C0 + 2], B4[R0 + 2, C0 + 2], 0)
assert VALUE == GEN["record"]["value"]


def qr_modules(svg):
    t = Path(svg).read_text()
    n = int(re.search(r'viewBox="0 0 (\d+) \d+"', t).group(1))
    return n, [(int(a), int(b)) for a, b in re.findall(r"M(\d+) (\d+)h1v1h-1z", t)]


# ------------------------------------------------------------------ draw
def chip(ax, x, y, s, layer, claim, h=8.0, size=15, z=5):
    fc = C[layer]
    tc = "white" if layer in ("L2", "L3") else C["ink"]
    w = text_w(ax, s, fontsize=size, fontweight=600) + 5.0
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.6", fc=fc, ec="none", zorder=z))
    T(ax, x + w / 2, y + h / 2 + 0.2, s, claim, fontsize=size, fontweight=600, color=tc, ha="center", va="center",
      zorder=z + 1)
    return w


def glyph(ax, x, y, s, kind, letter_pt=22):
    """Agent glyph: rounded square; A outlined umber, B filled slate. Told apart by letter and fill."""
    if kind == "A":
        ax.add_patch(FancyBboxPatch((x, y), s, s, boxstyle=f"round,pad=0,rounding_size={s * 0.22}", fc="white",
                                    ec=C["agentA"], lw=0.85 * MMPT, zorder=6))
        col = C["agentA"]
    else:
        ax.add_patch(FancyBboxPatch((x, y), s, s, boxstyle=f"round,pad=0,rounding_size={s * 0.22}", fc=C["agentB"],
                                    ec="none", zorder=6))
        col = "white"
    T(ax, x + s / 2, y + s / 2 + 0.3, kind, "F2.agents", fontsize=letter_pt, fontweight=700, color=col, ha="center",
      va="center", zorder=7)


def main():
    fig = S.fig_mm(W, H)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    fig.canvas.draw()
    L = lanes()
    SN = snippets()
    n = len(L)
    top, bot, gap = 19.0, H - 2.0, 3.0
    lh = min(22.0, (bot - top - gap * (n - 1)) / n)
    ys = [top + i * (lh + gap) for i in range(n)]

    # column heads (17 pt SemiBold ink2); the outcome head carries the mode label
    hk = dict(fontsize=PT["caption"], fontweight=600, color=C["ink2"], va="baseline")
    T(ax, 0, 11, "Agent A cites", "F2.heads", **hk)
    T(ax, 112, 11, "handoff", "F2.heads", **hk)
    T(ax, 355, 11, "relay", "F2.heads", ha="center", **hk)
    T(ax, 400, 11, "Agent B", "F2.heads", **hk)
    T(ax, 690, 4.9, "B acted on", "F2.heads", ha="right", **hk)
    T(ax, 690, 11, "corrupted evidence", "F2.heads", ha="right", **hk)
    T(ax, 698 + 103 / 2, 11, "what is handed over?", "O.84", ha="center", **hk)
    mode = "deterministic receiver, no model" if MODE == "fallback" else "agents, pooled Claude"
    T(ax, 690, 16.4, mode, "F2.mode", fontsize=S.FLOOR, color=C["ink2"], ha="right", va="baseline")
    ax.plot([0, 600], [13.6, 13.6], color=C["rule"], lw=0.35 * MMPT, zorder=1)

    # Agent A: the real 50 m window, the named pixel, the glyph and its sentence
    ax.imshow(WIN_TC, extent=(0, 50, top + 50, top), interpolation="none", zorder=2)
    nx, ny = NAMED[1] * 10, top + NAMED[0] * 10
    ax.add_patch(Rectangle((nx, ny), 10, 10, fill=False, ec="white", lw=2.4 * MMPT, zorder=3))
    ax.add_patch(Rectangle((nx, ny), 10, 10, fill=False, ec=C["emem"], lw=1.4 * MMPT, zorder=4))
    glyph(ax, 60, top, 18, "A", letter_pt=28)
    T(ax, 0, top + 57, "Agent A reads", "F2.agentA", fontsize=PT["label"], fontweight=600, color=C["ink"], va="top")
    T(ax, 0, top + 65, f"NDVI {VALUE:.4f} and cites it", "F2.agentA", fontsize=PT["label"], fontweight=600,
      color=C["ink"], va="top")
    T(ax, 0, top + 75, f"Sentinel-2A L2A, {DATE.day} {DATE:%b %Y}", "H.img.record", fontsize=S.FLOOR, color=C["ink2"],
      va="top")
    T(ax, 0, top + 81, "outlined: the 10 m pixel the record names", "F2.agentA.px", fontsize=S.FLOOR, color=C["ink2"],
      va="top")
    T(ax, 0, top + 87, "RGB from recorded grids", "V7.flow", fontsize=S.FLOOR, color=C["ink2"], va="top")
    # fan of handoff arrows from A to every lane
    for y in ys:
        p0, p1 = (79.5, top + 9), (106.5, y + lh / 2)
        bez = MPath([p0, (93, p0[1]), (93, p1[1]), p1], [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4])
        a = FancyArrowPatch(path=bez, arrowstyle="-|>,head_length=2.6,head_width=1.3", mutation_scale=MMPT,
                            lw=0.5 * MMPT, color=C["ink2"], zorder=2)
        ax.add_patch(a)

    # relay bar (harm tint) behind lanes 318 to 392, then lanes
    rx, rw = 318, 74
    for i, (key, name, does, (k, nn), ceil) in enumerate(L):
        y = ys[i]
        em = key == "emem"
        ax.add_patch(Rectangle((108, y), 690 - 108, lh, fc=C["emem_tint"] if em else C["na"], ec="none", zorder=1))
        ax.plot([312, 318 + 9], [y + lh / 2] * 2, color=C["ink2"], lw=0.5 * MMPT, zorder=3)
        ax.add_patch(FancyArrowPatch((392, y + lh / 2), (401, y + lh / 2), arrowstyle="-|>,head_length=2.6,head_width=1.3",
                                     mutation_scale=MMPT, lw=0.5 * MMPT, color=C["ink2"], zorder=3, shrinkA=0, shrinkB=0))
    ax.add_patch(Rectangle((rx, ys[0] - 1.5), rw, ys[-1] + lh - ys[0] + 3, fc=C["harm_tint"], ec=C["harm"],
                           lw=0.55 * MMPT, zorder=2))
    fl = ["relay or faulty", "signer changes:"] + FAMILIES.split(" · ")
    fy0 = ys[0] + 4.5
    step = (ys[-1] + lh - 3 - fy0) / (len(fl) - 1)
    for j, s in enumerate(fl):
        T(ax, rx + 19, fy0 + j * step, s, "F2.relay" if j > 1 else "V7.flow", fontsize=15 if j > 1 else 15,
          fontweight=600 if j < 2 else 400, color=C["harm_text"], va="center", zorder=4)

    for i, (key, name, does, (k, nn), ceil) in enumerate(L):
        y = ys[i]
        cy = y + lh / 2
        em = key == "emem"
        # lane name + snippet
        small = lh < 20
        T(ax, 112, y + (1.6 if small else 3.2), name, "F2.lanes", fontsize=20 if small else 22, fontweight=700, color=C["emem"] if em else C["ink"],
          va="top", zorder=4)
        if em:
            s = clip_to(ax, SN["emem"], 186, family=S.MONO, fontsize=15, fontweight=600)
            tw_ = text_w(ax, s, family=S.MONO, fontsize=15, fontweight=600) + 5
            ax.add_patch(FancyBboxPatch((112, y + lh - (7.8 if small else 9.6)), tw_, 7.2, boxstyle="round,pad=0,rounding_size=1.4",
                                        fc=C["emem"], ec="none", zorder=4))
            T(ax, 114.5, y + lh - (4.2 if small else 6.0), s, "O.cid", family=S.MONO, fontsize=15, fontweight=600, color="white",
              va="center", zorder=5)
        else:
            s = clip_to(ax, SN[key], 196, family=S.MONO, fontsize=15)
            T(ax, 112, y + lh - (4.2 if small else 6.0), s, "F2.snippets", family=S.MONO, fontsize=15, color=C["ink2"], va="center",
              zorder=4)
        # corruption diamond on the lane
        d = 4.0
        ax.add_patch(Polygon([(rx + 9 - d, cy), (rx + 9, cy - d), (rx + 9 + d, cy), (rx + 9, cy + d)], closed=True,
                             fc=C["harm"], ec="white", lw=0.4 * MMPT, zorder=5))
        # Agent B and what it does
        glyph(ax, 402, cy - 5.5, 11, "B", letter_pt=17)
        if em:
            chain = [("resolve", "L0"), ("re-hash", "L0"), ("place / time / band", "L1"), ("signature", "L0"),
                     ("log", "L0"), ("recompute", "L2"), ("source re-read", "L3")]
            x = 418
            ch = min(8.0, (lh - 4.5) / 2)
            row_y = [y + 1.6, y + lh - 1.6 - ch]
            for j, (s, lay) in enumerate(chain):
                if j == 4:
                    x = 418
                x += chip(ax, x, row_y[0 if j < 4 else 1], s, lay, "F2.chips", h=ch, size=15) + 2.2
        else:
            T(ax, 418, cy, does, "F2.actions", fontsize=PT["label"], color=C["ink"], va="center", zorder=4)
        # outcome numeral
        col = C["emem"] if k == 0 else C["harm"]
        r1id = {"prose": "S.R1.A", "json": "S.R1.B", "opaque": "S.R1.C", "emem": "S.R1.I"}
        r5id = {"prose": "R5.A.pooled", "json": "R5.B.pooled", "rag": "R5.C.pooled", "opaque": "R5.D.pooled",
                "emem": "R5.E.pooled"}
        T(ax, 690, cy + 0.6, fmt_frac(k, nn), r1id[key] if MODE == "fallback" else r5id[key],
          fontsize=PT["numeral"] if lh >= 20 else 48, fontweight=700, color=col, ha="right", va="center", zorder=4)
    # The former boundary wall now answers the handoff question directly.
    # It is deliberately compact: the full decoded object is restored as panel 4.
    wx, ww = 698, W - 698
    hatch(ax, wx, ys[0] - 1.5, ww, H - (ys[0] - 1.5), pitch=1.6, z=1)
    px, pw_ = wx + 7, ww - 14

    # What actually crosses the handoff: the address, not a copied pixel or prose blob.
    ay, ah = ys[0] + 1.8, 36.5
    ax.add_patch(FancyBboxPatch((px, ay), pw_, ah, boxstyle="round,pad=0,rounding_size=1.5",
                                fc=C["emem"], ec="none", zorder=3))
    T(ax, px + 5, ay + 6.5, "REFERENCE", "O.84", fontsize=14, fontweight=700, color="white", va="center", zorder=4)
    T(ax, px + 5, ay + 14.0, "84 characters", "O.84", fontsize=22, fontweight=700, color="white", va="center", zorder=4)
    T(ax, px + 5, ay + 21.0, "record CID = BLAKE3(record)", "O.cid", fontsize=15, color="white", va="center", zorder=4)
    cid = TOKEN.split(":")[-1]
    T(ax, px + 5, ay + 27.2, cid[:26], "O.cid", family=S.MONO, fontsize=14, fontweight=600, color="white", va="center", zorder=4)
    T(ax, px + 5, ay + 33.4, cid[26:], "O.cid", family=S.MONO, fontsize=14, fontweight=600, color="white", va="center", zorder=4)

    # Everything below is recovered from that address and independently checked by the receiver.
    items = [
        ("RECORD · 1,115 B", "fetch + re-hash", "O.1115", "L0"),
        ("ATTESTATION + LOG", "signature + inclusion", "O.batch", "L0"),
        ("SOURCE FILES", "named, not hashed", "O.nohash", "L3"),
    ]
    iy = ay + ah + 3.0
    ih = 17.5
    for j, (title, sub, claim, layer) in enumerate(items):
        y = iy + j * (ih + 1.8)
        fc = C["emem_tint"] if j < 2 else C["oos_bg"]
        ec = C["emem"] if j < 2 else C["oos"]
        ax.add_patch(FancyBboxPatch((px, y), pw_, ih, boxstyle="round,pad=0,rounding_size=1.4",
                                    fc=fc, ec=ec, lw=0.35 * MMPT, zorder=3))
        T(ax, px + 5, y + 6.5, title, claim, fontsize=16, fontweight=700,
          color=C["emem"] if j < 2 else C["ink"], va="center", zorder=4)
        T(ax, px + 5, y + 12.6, sub, claim, fontsize=14, color=C["ink2"], va="center", zorder=4)
        if j < len(items) - 1:
            ax.add_patch(FancyArrowPatch((px + pw_/2, y + ih), (px + pw_/2, y + ih + 2.0),
                                         arrowstyle="-|>,head_length=1.8,head_width=1.0", mutation_scale=MMPT,
                                         lw=0.4 * MMPT, color=C["ink2"], zorder=4, shrinkA=0, shrinkB=0))

    S.save(fig, NAME)
    meta = {"figure": NAME, "size_mm": [W, H], "mode": MODE, "lanes": [l[0] for l in L],
            "numerals": {l[0]: list(l[3]) for l in L}, "snippets": SN,
            "r5": {k: v for k, v in (R5 or {}).items()}, "labels": LABELS}
    Path(S.OUT, f"{NAME}.labels.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
