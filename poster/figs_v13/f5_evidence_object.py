"""F5 · What is handed over: the evidence object, exploded (396 x 98 mm, brief §E F5).

The record is the real one: the fact bytes inside research/repro/v8/proof_bundle_ndvi.cbor (entry.facts[0], cut out
of the attestation without re-encoding by mutation_suite.facts_raw), decoded with cbor2. Asserted before drawing:
1,115 bytes; base32(BLAKE3(bytes)) equals the token's cid; the record has no signature field and its source has no
hash or cid; sizes and DNs equal cog_pixel_bytes.json / pixel_check.json; 84 characters and 46 cl100k tokens equal
token_counts.json.

    python poster/figs_v13/f5_evidence_object.py
"""
import base64
import json
import os
import struct
import sys
from datetime import datetime, timezone

import blake3
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from style import C, MONO, OUT, ROOT, fig_mm, save  # noqa: E402

sys.path.insert(0, os.path.join(ROOT, "research/repro/v11"))
import mutation_suite as MS  # noqa: E402  (reads the committed bundle; runs nothing on import)

W, H = 396.0, 98.0
PTMM = 25.4 / 72
NAME = "f5_evidence_object"
D = os.path.join(ROOT, "research/repro/data")

# ------------------------------------------------------------------ the real record
FACT, REC, TOKEN = MS.FACT, MS.FACT_D, MS.BUNDLE["token"]
_, _, TCELL, TCID = TOKEN.split(":")
CID = base64.b32encode(blake3.blake3(FACT).digest()).decode().lower().rstrip("=")
TC = json.load(open(os.path.join(D, "v8/token_counts.json")))
assert len(FACT) == TC["fact_cbor_bytes"]["bytes"] == 1115
assert CID == TCID == "oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa"
assert len(TOKEN) == TC["fact_token_ndvi"]["chars"] == 84 and TC["fact_token_ndvi"]["cl100k"] == 46
assert not any("signature" in k or k == "sig" for k in REC), "the record carries no signature of its own"
assert set(REC) == {"kind", "cell", "band", "tslot", "value", "confidence", "sources", "derivation", "privacy_class",
                    "schema_cid", "signer", "signed_at"}, sorted(REC)
SRC = REC["sources"][0]
assert len(REC["sources"]) == 1 and "hash" not in SRC and "cid" not in SRC, "source named, not hashed"
ARGS = REC["derivation"]["args"]
SIGNER = base64.b32encode(bytes(REC["signer"])).decode().lower().rstrip("=")
assert SIGNER.startswith("777er3yi") and bytes(REC["signer"]) == MS.EMEM_KEY
day = datetime.fromtimestamp(REC["tslot"] * 86400, tz=timezone.utc)
assert day.strftime("%Y-%m-%d") == "2026-09-25"
urls = SRC["id"].split(" ; ")
tails = [u.rsplit("_", 2)[-2] for u in urls]
assert tails == ["B08", "B04"]
COG = json.load(open(os.path.join(D, "v8/cog_pixel_bytes.json")))["bands"]
PC = json.load(open(os.path.join(D, "v8/pixel_check.json")))
now = next(v for k, v in PC.items() if "oj5cecci" in k)
assert ARGS[5] == [now["B08"]["floor_DN"], now["B04"]["floor_DN"]] == [3502, 1900]
assert now["B04"]["floor(r,c)"] == [9443, 9098] and COG["B04"]["pixel"] == [9098, 9443]
mb = lambda b: f"{COG[b]['cog_bytes'] / 1e6:.1f}"
assert (mb("B04"), mb("B08")) == ("277.9", "281.9")
assert ARGS[3] == 32643 and ARGS[12] == -1000.0 and ARGS[2].startswith("S2A_MSIL2A_20260925T054251_R005_T43SFS")
assert abs(REC["value"] - (3502 - 1900) / ((3502 - 1000) + (1900 - 1000))) == 0.0, "value recomputes bit for bit"


def grid(b):
    raw = open(os.path.join(D, f"keylong_{b}.bin"), "rb").read()
    w, h = struct.unpack_from("<II", raw, 8)
    return np.frombuffer(raw, dtype="<f4", offset=64).reshape(h, w).astype(float)


# ------------------------------------------------------------------ canvas
fig = fig_mm(W, H)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
LABELS = []


def T(x, y, s, size=14, claim=None, weight=400, color=None, family=None, ha="left", va="center", z=6, **kw):
    t = ax.text(x, y, s, fontsize=size, fontweight=weight, color=color or C["ink"], ha=ha, va=va,
                family=family or "IBM Plex Sans", zorder=z, **kw)
    LABELS.append({"text": s, "pt": size, "claim": claim})
    return t


def wmm(t):
    return t.get_window_extent(fig.canvas.get_renderer()).width / fig.dpi * 25.4


def box(x, y, w, h, fc, ec="none", lw=0.0, r=1.0, ls="-", z=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw / PTMM,
                       ls=ls, zorder=z)
    ax.add_patch(p)
    return p


def arrow(x0, x1, y, color=C["ink2"]):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>,head_length=2.4,head_width=1.2",
                                 mutation_scale=1 / PTMM, lw=0.6 / PTMM, color=color, zorder=5,
                                 shrinkA=0, shrinkB=0))


def tag(x, y, s, kind, claim):
    """A field tag: bound (L1), recomputable (L2), named (source, dashed)."""
    t = T(0, 0, s, 14, color="white" if kind == "recomp" else C["ink"], claim=claim, weight=500)
    w = wmm(t) + 3.0
    if kind == "named":
        box(x, y - 2.5, w, 5.0, C["paper"], ec=C["ink2"], lw=0.35, r=1.0, ls=(0, (3, 2)), z=4)
    elif kind == "bound":
        box(x, y - 2.5, w, 5.0, C["L1"], r=1.0, z=4)
    else:
        box(x, y - 2.5, w, 5.0, C["L2"], r=1.0, z=4)
    t.set_position((x + w / 2, y)); t.set_ha("center")
    return x + w


# ------------------------------------------------------------------ boxes
TOP, BOT = 1.0, 76.0
X1, W1 = 0.6, 55.0
X2, W2 = 66.0, 216.0
X3, W3 = 290.0, 54.0
X4, W4 = 352.0, 43.4
HY = 6.4                                   # head line

# (1) source files: dashed, named not hashed
box(X1, TOP, W1, BOT - TOP, C["paper"], ec=C["ink2"], lw=0.5, r=1.6, ls=(0, (5, 3)))
T(X1 + 3, HY, "SOURCE FILES", 15, weight=700, color=C["ink2"], claim="O.nohash")
T(X1 + 3, HY + 5.6, "named, not hashed", 14, color=C["ink2"], claim="O.nohash")
tw, th = 23.4, 23.4 * 453 / 443
for k, b in enumerate(("B08", "B04")):
    g = grid(b)
    lo, hi = np.percentile(g, 1), np.percentile(g, 99)
    tx = X1 + 3 + k * (tw + 2.2)
    ax.imshow(np.clip((g - lo) / (hi - lo), 0, 1), cmap="gray", vmin=0, vmax=1, interpolation="none",
              extent=(tx, tx + tw, 16 + th, 16), zorder=3)
    px, py = tx + (225 + 0.5) / 443 * tw, 16 + (212 + 0.5) / 453 * th
    ax.add_patch(Rectangle((px - 1.1, py - 1.1), 2.2, 2.2, fill=False, ec="white", lw=1.2 / PTMM, zorder=4))
    ax.add_patch(Rectangle((px - 1.1, py - 1.1), 2.2, 2.2, fill=False, ec=C["emem"], lw=0.6 / PTMM, zorder=4.1))
    T(tx + tw / 2, 16 + th + 3.4, b, 14, family=MONO, ha="center", color=C["ink2"], claim="O.cogs")
yl = 49.4
for i, (s, cl) in enumerate((("B04 + B08 COGs", "O.cogs"), ("Planetary Computer", "O.cogs"),
                             (f"{mb('B04')} + {mb('B08')} MB", "O.cogs"), ("row 9443, col 9098", "O.pixel"),
                             (f"DN {ARGS[5][1]:.0f}, {ARGS[5][0]:.0f}", "O.pixel"))):
    T(X1 + 3, yl + i * 5.3, s, 14, color=C["ink"], claim=cl)

# (2) the record
box(X2, TOP, W2, BOT - TOP, C["paper"], ec=C["emem"], lw=0.9, r=1.6)
t = T(X2 + 3, HY, f"RECORD · {len(FACT):,} B", 15, weight=700, color=C["emem"], claim="O.1115")
T(X2 + 3 + wmm(t) + 4, HY, f"{len(REC)} fields as decoded; no signature inside", 14, color=C["ink2"],
  claim="F5.fields")
KX, VX, PITCH, Y0 = X2 + 3, X2 + 29, 5.6, 14.0
KX2, VX2 = X2 + 126, X2 + 144.5


def field(kx, vx, y, key, val, claim, tags=()):
    T(kx, y, key, 14, color=C["muted"], claim="F5.fields")
    t = T(vx, y, val, 15, family=MONO, color=C["ink"], claim=claim)
    x = vx + wmm(t) + 2.0
    for s, kind, cl in tags:
        x = tag(x, y, s, kind, cl) + 1.2
    return x


col1 = [("kind", REC["kind"], ()), ("cell", REC["cell"], (("bound L1", "bound", "F5.tags"),)),
        ("band", REC["band"], (("bound L1", "bound", "F5.tags"),)),
        ("tslot", f"{REC['tslot']} ({day.day} {day.strftime('%b')})", (("bound L1", "bound", "F5.tags"),)),
        ("value", repr(REC["value"]), (("recomputable L2", "recomp", "F5.tags"),)),
        ("confidence", f"{REC['confidence']:.2f}", ())]
for i, (k, v, tg) in enumerate(col1):
    xe = field(KX, VX, Y0 + i * PITCH, k, v, "F5.fields", tg)
    assert xe < KX2 - 1 or i >= 4, (k, xe)
col2 = [("privacy", REC["privacy_class"]), ("schema", REC["schema_cid"][:8] + "…"),
        ("signer", SIGNER[:8] + "…"), ("signed", REC["signed_at"])]
for i, (k, v) in enumerate(col2):
    xe = field(KX2, VX2, Y0 + i * PITCH, k, v, "F5.fields")
    assert xe < X2 + W2 - 1, (k, xe)
ys = Y0 + 6 * PITCH + 1.2
ax.plot([X2 + 3, X2 + W2 - 3], [ys - 3.2, ys - 3.2], color=C["rule"], lw=0.35 / PTMM, zorder=3)
cap = SRC["captured_at"]
cap_s = cap[:19] + "Z"
rows = [("sources", f"{SRC['scheme']} · …{tails[0]}_10m.tif ; …{tails[1]}_10m.tif",
         (("named L3", "named", "F5.tags"),)),
        ("", f"captured {cap_s}", ()),
        ("derivation", f"{REC['derivation']['fn_key']} · EPSG {ARGS[3]}", ()),
        ("", f"scene {ARGS[2][:38]}…", (("named L3", "named", "F5.tags"),)),
        ("", f"DNs {ARGS[5][0]:.0f} / {ARGS[5][1]:.0f} · offset −{-ARGS[12]:.0f} · "
             f"+ {len(ARGS) - 4} more args", ())]
for i, (k, v, tg) in enumerate(rows):
    xe = field(KX, VX, ys + i * PITCH, k, v, "F5.fields", tg)
    assert xe < X2 + W2 - 1, (v, xe)
assert ys + 4 * PITCH + 3 < BOT

# (3) the address
box(X3, TOP, W3, BOT - TOP, C["emem"], r=1.6)
T(X3 + 3, HY, "ADDRESS", 15, weight=700, color="white", claim="O.cid")
T(X3 + 3, HY + 5.6, "BLAKE3 of the record", 14, color="white", claim="O.cid")
for i in range(4):
    T(X3 + W3 / 2, 22.0 + i * 7.0, CID[i * 13:(i + 1) * 13], 17, family=MONO, weight=500, color="white",
      ha="center", claim="O.cid")
for i, s in enumerate(("changes if one bit", "of the record", "changes")):
    T(X3 + 3, 56.6 + i * 5.3, s, 14, color="white", claim="F5.onebit")

# (4) attestation and log
box(X4, TOP, W4, BOT - TOP, C["paper"], ec=C["ink2"], lw=0.5, r=1.6)
T(X4 + 2.6, HY, "ATTESTATION", 15, weight=700, color=C["ink2"], claim="O.batch")
T(X4 + 2.6, HY + 5.6, "+ LOG", 15, weight=700, color=C["ink2"], claim="O.log")
for i, (s, fam, cl) in enumerate((("Ed25519 over", None, "O.batch"), ("a batch root", None, "O.batch"),
                                  (f"key {SIGNER[:8]}…", MONO, "O.key"), ("Merkle log,", None, "O.log"),
                                  ("RFC 6962 style,", None, "O.log"), ("BLAKE3", None, "O.log"))):
    T(X4 + 2.6, 21.4 + i * 5.6, s, 14 if fam else 15, family=fam, color=C["ink"], claim=cl)
for j in range(7):
    ax.add_patch(Rectangle((X4 + 2.6 + j * 5.4, 60.0), 4.4, 4.4, fc=C["emem"] if j == 4 else C["rule"], ec="none",
                           zorder=3))
T(X4 + 2.6, 69.4, "log entries", 14, color=C["ink2"], claim="O.log")

# arrows with their labels, rotated in the gaps
for (xa, xb, lab, cl) in ((X1 + W1, X2, "read the containing pixel", "F5.read"), (X2 + W2, X3, "BLAKE3", "O.cid"),
                          (X3 + W3, X4, "leaf of a batch root", "O.batch")):
    arrow(xa + 0.6, xb - 0.6, HY)
    T((xa + xb) / 2, 44.0, lab, 14, color=C["ink2"], ha="center", rotation=90, claim=cl)

# ------------------------------------------------------------------ the token, as handed over
yt = 87.6
parts = [("emem:fact:", C["muted"], 400), (TCELL, C["ink"], 500), (":", C["muted"], 400), (TCID, C["emem"], 700)]
x = 3.0
texts = []
for s, col, wt in parts:
    t = T(x, yt, s, 18, family=MONO, color=col, weight=wt, claim="O.cid" if s == TCID else "F5.token")
    texts.append((s, x, wmm(t)))
    x += wmm(t)
box(0.6, yt - 5.2, x - 0.6 + 2.4, 10.4, C["emem_tint"], r=1.6, z=1)
cid_x0, cid_w = texts[-1][1], texts[-1][2]
ax.plot([X3 + W3 / 2, X3 + W3 / 2, cid_x0 + cid_w / 2, cid_x0 + cid_w / 2], [BOT, 79.0, 79.0, yt - 5.2],
        color=C["emem"], lw=0.5 / PTMM, zorder=2)
xr = x + 6.0
T(xr, yt - 2.9, f"handed over: {len(TOKEN)} characters,", 14, color=C["ink"], claim="O.84")
T(xr, yt + 2.9, f"{TC['fact_token_ndvi']['cl100k']} tokens (cl100k)", 14, color=C["ink"], claim="O.46")

save(fig, NAME)
json.dump({"figure": NAME, "size_mm": [W, H], "labels": LABELS},
          open(os.path.join(OUT, f"{NAME}.labels.json"), "w"), indent=1, ensure_ascii=False)
