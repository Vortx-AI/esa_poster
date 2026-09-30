"""Hero figure of the v11 board: the whole of emem on one page, drawn around one real observation.

Every string drawn below is copied from a signed record or a measured number already on the
v10 board (research/should_do/05_EVIDENCE_AND_NUMBERS.md; research/repro/v10/algorithms.md).
Units are millimetres at print size. Output: fig/v11/hero.svg (inlined into poster.html by build_v11.py).
"""
from pathlib import Path
from html import escape

HERE = Path(__file__).resolve().parent
OUT = HERE / "fig" / "v11" / "hero.svg"

W, H = 797, 224
INK, INK2, MUTED, RULE = "#141414", "#46463F", "#85857E", "#D3D3CC"
ACC, ACCS, AMB, AMBS, BAD, PAPER = "#1F4FD8", "#E7ECFA", "#A86B00", "#FBF1DE", "#B3261E", "#FBFBF8"

el = []


def t(x, y, s, size=5.0, w=400, fill=INK, fam="Plex", anchor="start", italic=False):
    st = ' font-style="italic"' if italic else ""
    el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" font-weight="{w}" '
              f'fill="{fill}" text-anchor="{anchor}"{st}>{s}</text>')


def rect(x, y, w, h, fill="none", stroke=INK, sw=0.5, r=2.0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def arrow(x1, y1, x2, y2, col=INK, sw=0.8, head="a", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    el.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="{sw}" fill="none" marker-end="url(#{head})"{d}/>')


def badge(x, y, label, col=ACC):
    el.append(f'<circle cx="{x}" cy="{y}" r="4.6" fill="{col}"/>')
    t(x, y + 1.75, label, 4.6, 700, "#FFFFFF", anchor="middle")


def kicker(x, y, s, col=MUTED):
    t(x, y, s, 4.8, 600, col)


defs = f'''<defs>
<marker id="a" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L7,3.5 L0,7 z" fill="{INK}"/></marker>
<marker id="b" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L7,3.5 L0,7 z" fill="{ACC}"/></marker>
<marker id="d" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L7,3.5 L0,7 z" fill="{BAD}"/></marker>
<marker id="c" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L7,3.5 L0,7 z" fill="{AMB}"/></marker>
<clipPath id="imgclip"><rect x="0" y="12" width="165" height="169" rx="2"/></clipPath>
</defs>'''

# ---------------------------------------------------------------- 1. the world writes
kicker(0, 7, "THE WORLD WRITES")
el.append('<image href="fig/keylong_truecolor.png" x="0" y="12" width="165" height="169" '
          'preserveAspectRatio="xMidYMid slice" clip-path="url(#imgclip)"/>')
# the cell of the NDVI fact: 0.510 of width, 0.4685 of height (make_figures.py, F1)
cx, cy = 0 + 0.510 * 165, 12 + 0.4685 * 169
rect(cx - 3, cy - 3, 6, 6, stroke="#FFFFFF", sw=0.7, r=0.3)
el.append(f'<rect x="0" y="169" width="165" height="12" fill="#141414" fill-opacity="0.72"/>')
t(3, 177, "Keylong, Himalaya · Sentinel-2 L2A · 25 Sep 2026", 4.5, 500, "#FFFFFF")
el.append(f'<line x1="4" y1="16" x2="{4 + 165 / 4.43:.1f}" y2="16" stroke="#FFFFFF" stroke-width="0.8"/>')
t(4, 21, "1 km", 3.6, 500, "#FFFFFF")
t(0, 188.5, "a 2.02 GB scene; the square marks the cell", 4.5, 400, INK2)
t(0, 194.5, "of the NDVI record (drawn 100 m wide)", 4.5, 400, INK2)
kicker(0, 203.5, "OTHER WRITERS")
chips = [("Copernicus DEM", 34, 0, 210.5, False), ("Overture Maps", 32, 37, 210.5, False), ("weather", 21, 72, 210.5, False),
         ("TESSERA (retired)", 44, 96, 210.5, False),
         ("device gate: ships, no hardware enrolled yet", 92, 0, 219.5, True)]
for s_, wbox, x, y, dashed in chips:
    rect(x, y - 4.8, wbox, 7, fill="#FFFFFF", stroke=MUTED if dashed else RULE, sw=0.4, r=1.2, dash="1.2 0.8" if dashed else None)
    t(x + wbox / 2, y, s_, 4.0, 500, MUTED if dashed else INK2, anchor="middle")

# ---------------------------------------------------------------- 2. read
arrow(169, 70, 208, 70, INK, 0.9)
t(189, 64, "read", 4.6, 600, INK, anchor="middle")
t(189, 78, "1.17 MB", 4.3, 500, INK2, anchor="middle")
t(189, 83.5, "0.058 %", 4.3, 500, INK2, anchor="middle")

# ---------------------------------------------------------------- 3. fact plane
FX, FY, FW, FH = 212, 12, 296, 176
rect(FX, FY, FW, FH, fill=ACCS, stroke=ACC, sw=0.8, r=3)
t(FX + 5, FY + 8.8, "FACT PLANE", 6.0, 700, ACC)
t(FX + 42, FY + 8.8, "observations, written only by emem's own readers and listed keys", 4.5, 500, INK2)
badge(FX + FW - 7, FY + 7, "C3")
# the record
RX, RY, RW, RH = FX + 5, FY + 14, FW - 10, 75
rect(RX, RY, RW, RH, fill="#FFFFFF", stroke=INK, sw=0.45, r=1.5)
t(RX + 4, RY + 7.5, "one observation, one record", 5.0, 600, INK)
t(RX + RW - 4, RY + 7.5, "1,115 bytes, deterministic CBOR", 4.5, 500, INK2, anchor="end")
rows = [
    ("cell", "defi.zb572.xoso.zb1ec", "where: a 9.5 × 8.1 m cell"),
    ("band", "indices.ndvi", "what"),
    ("tslot", "20721", "valid time: 25 Sep 2026"),
    ("value", "0.4708994708994709", "(B08 − B04)/(B08 + B04)"),
    ("sources", "S2A_MSIL2A_20260925T054251_R005_T43SFS", ""),
    ("", "DN B08 3502 · B04 1900 · offset −1000", "inputs, re-readable"),
    ("signer", "777er3yi…", ""),
    ("signed_at", "2026-09-28T09:06:56Z", "record time"),
]
for i, (k, v, note) in enumerate(rows):
    y = RY + 15.5 + i * 7.2
    t(RX + 4, y, k, 4.5, 600, ACC, fam="PlexMono")
    t(RX + 31, y, escape(v), 4.5, 400, INK, fam="PlexMono")
    if note:
        t(RX + RW - 4, y, escape(note), 4.2, 400, MUTED, anchor="end", italic=True)
badge(RX - 1, RY + 2, "C1")
# hash
arrow(FX + FW / 2, RY + RH + 1, FX + FW / 2, RY + RH + 9, INK, 0.8)
t(FX + FW / 2 + 5, RY + RH + 6.8, "BLAKE3-256, base32: the name", 4.4, 600, INK)
CY = RY + RH + 10
rect(RX, CY, RW, 11, fill="#FFFFFF", stroke=ACC, sw=0.6, r=1.5)
t(RX + 4, CY + 7.6, "fact_cid", 4.5, 600, ACC, fam="PlexMono")
t(RX + 31, CY + 7.6, "oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa", 4.5, 500, INK, fam="PlexMono")
# attestation, log, absence
BY = CY + 16
bw = (RW - 8) / 3
boxes = [
    ("signed in batches", ["Ed25519 over the Merkle", "root of sorted fact_cids"]),
    ("append-only log", ["RFC 6962 shape,", "2,568,005 entries on 30 Sep"]),
    ("signed absence", ["'looked, found nothing',", "with the bytes it read"]),
]
for i, (h, lines) in enumerate(boxes):
    x = RX + i * (bw + 4)
    rect(x, BY, bw, 25, fill="#FFFFFF", stroke=RULE, sw=0.45, r=1.5)
    t(x + 3.5, BY + 7, h, 4.8, 600, INK)
    for j, s in enumerate(lines):
        t(x + 3.5, BY + 13.8 + j * 5.8, escape(s), 4.3, 400, INK2)


TY2 = BY + 30
rect(RX, TY2, RW, FY + FH - TY2 - 4, fill="#FFFFFF", stroke=RULE, sw=0.45, r=1.5)
badge(RX - 1, TY2 + 2, "C2")
t(RX + 6, TY2 + 7.5, "two clocks", 4.8, 600, INK)
t(RX + 36, TY2 + 7.5, "valid time (tslot) and record time (signed_at) are both in the bytes;", 4.3, 400, INK2)
t(RX + 6, TY2 + 13.8, "recall as of t returns what was signed by t. A correction is a new record; the old token still resolves.", 4.3, 400, INK2)
t(RX + 6, TY2 + 20.1, "Bengaluru elevation: 918.0 m signed in May, 915.07 m after the upstream DEM changed. Both verify.", 4.3, 400, INK)

# ---------------------------------------------------------------- 4. the token crosses
TX = FX + FW + 6  # 514
TKY = 72
rect(TX, TKY, 76, 100, fill="#FFFFFF", stroke=ACC, sw=0.6, r=2)
el.append(f'<line x1="{TX + 38}" y1="64" x2="{TX + 38}" y2="{TKY}" stroke="{ACC}" stroke-width="0.6" stroke-dasharray="1.2 0.9"/>')
badge(TX + 70, TKY + 1, "C4")
t(TX + 4, TKY + 8.5, "the token: 84 characters", 4.7, 600, INK)
t(TX + 4, TKY + 15, escape("emem:fact:<cell>:<fact_cid>"), 4.0, 500, ACC, fam="PlexMono")
t(TX + 4, TKY + 23.5, "one algebra, pixel to archive", 4.5, 600, INK)
fam_rows = [
    ("fact", "one value"),
    ("raster", "a field"),
    ("cube", "field × time"),
    ("rasterset", "fields, bound"),
    ("tree", "any file, in place"),
    ("bundle", "≤ 256 facts"),
    ("entity", "one thing, one name"),
]
for i, (k, v) in enumerate(fam_rows):
    y = TKY + 32 + i * 9.9
    t(TX + 4, y, k, 4.5, 600, ACC if k != "entity" else INK2, fam="PlexMono")
    t(TX + 31, y, escape(v), 4.1, 400, INK2)

# ---------------------------------------------------------------- 5. agents
AX = TX + 82  # 596
AW = W - AX
kicker(AX, 7, "AGENTS READ, CHECK AND CITE")
names = [("agent A", "Claude"), ("agent B", "Gemma"), ("agent C", "Qwen · any model")]
aw = (AW - 8) / 3
for i, (a, m) in enumerate(names):
    x = AX + i * (aw + 4)
    rect(x, 12, aw, 20, fill="#FFFFFF", stroke=INK, sw=0.5, r=2)
    t(x + aw / 2, 20.5, a, 5.0, 600, INK, anchor="middle")
    t(x + aw / 2, 27.2, m, 4.4, 400, INK2, anchor="middle")
t(AX, 39.5, "over MCP, A2A, REST or the Python and TypeScript SDKs", 4.4, 500, INK2)
# verification chain
VY = 45
rect(AX, VY, AW, 76, fill="#FFFFFF", stroke=ACC, sw=0.6, r=2)
t(AX + 4, VY + 8.5, "each receiver checks, trusting no one", 5.0, 600, INK)
badge(AX + AW - 7, VY + 1, "C5")
steps = [
    ("bytes → name", "re-hash to the fact_cid"),
    ("cell", "record's cell = token's cell, else 409"),
    ("arithmetic", "recompute NDVI from the DNs"),
    ("source", "re-read the pixel in the public COG"),
    ("signature", "Ed25519 receipt, offline"),
    ("log", "inclusion in the signed tree head"),
]
for i, (k, v) in enumerate(steps):
    y = VY + 16 + i * 9.6
    el.append(f'<circle cx="{AX + 6}" cy="{y - 1.5}" r="2.5" fill="{ACC}"/>')
    t(AX + 6, y - 0.2, str(i + 1), 3.5, 700, "#FFFFFF", anchor="middle")
    t(AX + 11, y, k, 4.6, 600, INK)
    t(AX + 46, y, escape(v), 4.4, 400, INK2)
# reads flow up from the token to agents
arrow(FX + FW, 64, AX, 64, ACC, 1.2, "b")
t(TX + 38, 60, "only the name crosses", 4.6, 600, ACC, anchor="middle")

# ---------------------------------------------------------------- 6. note plane
NY = 128
rect(AX, NY, AW, 60, fill=AMBS, stroke=AMB, sw=0.8, r=3)
t(AX + 4, NY + 8.8, "NOTE PLANE", 6.0, 700, AMB)
t(AX + 42, NY + 8.8, "claims, written by agents under their own keys", 4.5, 500, INK2)
badge(AX + AW - 7, NY + 7, "C6")
notes = [
    "signed notes, never instructions to the reader",
    "hash-chained tracks (this board's evidence is one)",
    "derivations, re-run by emem before signing",
    "a guard that refuses a wrong number",
    "entities: one shared label for a place or thing",
]
for i, s in enumerate(notes):
    t(AX + 5, NY + 17.5 + i * 8.4, "· " + escape(s), 4.5, 400, INK)
arrow(AX + 14, 121.5, AX + 14, NY - 0.5, AMB, 0.9, "c")
t(AX + 17, 126, "write", 4.3, 600, AMB)
# the wall: agents cannot write observations
WY = 180
el.append(f'<path d="M{AX} {WY} L{FX + FW + 7} {WY}" stroke="{BAD}" stroke-width="0.9" fill="none" stroke-dasharray="2 1.4" marker-end="url(#d)"/>')
el.append(f'<path d="M{TX + 34} {WY - 4} l8 8 M{TX + 42} {WY - 4} l-8 8" stroke="{BAD}" stroke-width="1.2"/>')
t(TX + 38, WY + 10, "agents cannot write observations", 4.6, 700, BAD, anchor="middle")

# ---------------------------------------------------------------- footer line of the figure
t(FX, 199, "Keyed by where, what and when; named by the hash of its bytes.", 4.7, 600, INK)
t(FX, 205.5, "Only the 84-character name travels; the bytes stay where anyone can re-read them.", 4.5, 400, INK2)
t(AX, 199, "Every check runs with stock libraries:", 4.5, 400, INK2)
t(AX, 205.5, "Python stdlib, blake3, cbor2, pynacl.", 4.5, 400, INK2)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
       f'viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm">{defs}' + "\n".join(el) + "</svg>")
OUT.write_text(svg)
print("wrote", OUT, len(svg), "bytes")
