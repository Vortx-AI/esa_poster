"""F14 · The token family (193.5 x 118 mm, right column).

Fourteen data needs, one grammar each, and what the id hashes. Sources, in order of authority:
  research/repro/v10/algorithms.md §6 (raster, cube, rasterset, bundle, tree, track), §9 (absence), §15 (trace),
      §2 (cell64) and §1 (fact_cid = b32(BLAKE3(bytes)), 52 characters), read from emem 18adb67
  research/v13/00_v11_review_findings.md M2 (bundle preimage), M10 to M12 (cube and rasterset hash lists of member
      derivation cids, rasterset appends the purpose), M14 (tree id = BLAKE3(note)[:16], the root is inside the note),
      M15 (state record fields)
  emem docs/model.md at 18adb67 (entity: 16 bytes of a hash over the identity anchor, a label not bytes; cell: an
      address, it names no bytes)
  poster/archive/v11-sealed/poster.html class "fam": the v11 table these rows correct
Every grammar and hash rule is asserted against the text of those files before drawing.

    python poster/figs_v13/f14_token_family.py
"""
import json
import os
import re
import sys

from matplotlib.patches import Polygon, Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, MONO, OUT, ROOT, fig_mm, save  # noqa: E402

W, H = 193.5, 136.0   # v13.10 (4 Oct): rows 8.0 mm apart, from 6.7 (the cut freed the right column)
PTMM = 25.4 / 72
NAME = "f14_token_family"
ALG = open(os.path.join(ROOT, "research/repro/v10/algorithms.md"), encoding="utf-8").read()
FIND = open(os.path.join(ROOT, "research/v13/00_v11_review_findings.md"), encoding="utf-8").read()
V11 = open(os.path.join(ROOT, "poster/archive/v11-sealed/poster.html"), encoding="utf-8").read()


def says(text, *phrases):
    for p in phrases:
        assert p in text, p
    return True


# the rules this table prints, each tied to its source text
says(ALG, "`fact_cid = b32(H(bytes))`, which is 52 characters")
says(ALG, "`reason_cid = b32(H(utf8(reason_text))[0..16])`")
says(ALG, "`aoi_cid = b32(H(cbor{min_lat, min_lng, max_lat, max_lng}))`", "`artifact_cid = b32(H(EMEMGRD1 grid bytes))`",
     "`derivation_cid` = fact_cid of the `band_cube` derivative")
says(ALG, "`cube_cid = b32(H(cbor([member derivation_cid…] in ascending tslot))`")
says(ALG, '`bundle_cid = b32(H(cbor([dcid…, "purpose:"+p])))`')
says(ALG, '`bundle_cid = b32(H("emem.memory_bundle.v1|" ‖ purpose? ‖ "\\n" ‖ Σ(cell‖"|"‖band‖"|"‖dec(tslot)‖"|"‖fact_cid?‖"\\n"))[0..16])`')
says(ALG, "`linkᵢ = cidOf(utf8(linkᵢ₋₁) ‖ utf8(refᵢ))`", "`cidOf(b) = b32(H(b)[0..16])`")
says(ALG, "trace_cid = b32(H(cbor(OsTrace incl. signature)))")
says(ALG, "The first group of every geo cell is `defi`")
says(FIND, "BLAKE3(note)[:16]; note holds Merkle root of chunks", "compute_file_cid = base32(BLAKE3(bytes)[:16])")
says(FIND, "BLAKE3(CBOR{kind, prev, fact_cids, payload, key, …})")
says(FIND, "BLAKE3(p, cell|band|tslot|cid…)[:16]")
says(FIND, "The cube and rasterset hash rules are the same kind of rule: BLAKE3(CBOR(list of member derivation cids)), with rasterset appending the purpose")
says(V11, "emem:cell:&lt;cell64&gt;", "hash of an anchor (e.g. an OSM id): a label, not bytes", "128 / 1024 floats", "attester_only",
     "no hardware admitted yet", "An embedding is one row of fourteen.")

# (data need, grammar after "emem:", what the id hashes, glyph)   glyph: bytes | list | name | none
ROWS = [
    ("a place", "cell:<cell64>", "the quantised lat/lng; no hash", "none"),
    ("one value", "fact:<cell>:<cid>", "BLAKE3(CBOR(fact)), 52 chars", "bytes"),
    ("nothing there", "fact: · kind absence", "same; + BLAKE3(reason)[:16]", "bytes"),
    ("an embedding", "fact: · 128 / 1024 floats", "same; not re-runnable", "bytes"),
    ("a derived value", "fact: · op, parents", "same; pure ops re-runnable", "bytes"),
    ("a raster", "raster:<a>:<b>:<t>:<d>", "fact d names BLAKE3(grid)", "bytes"),
    ("a raster in time", "cube:<a>:<b>:<t0..t1>:<d>", "BLAKE3(CBOR([member d…]))", "list"),
    ("a raster set", "rasterset:<set>:<d>", "BLAKE3(CBOR([d…, purpose]))", "list"),
    ("many facts, one id", "bundle:<cid>", "BLAKE3(p, cell|band|t|cid)[:16]", "list"),
    ("a file, one chunk", "tree:<file>#row=i", "BLAKE3(note)[:16]; root inside", "bytes"),
    ("a reasoning stage", "state:<cid>", "BLAKE3(CBOR(state record))", "list"),
    ("a named object", "entity:<cid>", "BLAKE3(anchor)[:16]: a label", "name"),
    ("a device run", "trace:<cid>", "BLAKE3(CBOR(signed trace))", "bytes"),
    ("an evidence chain", "track.v1 note", "link = BLAKE3(prev, ref)[:16]", "list"),
]
assert len(ROWS) == 14
assert sum(r[3] == "bytes" for r in ROWS) == 7 and sum(r[3] == "list" for r in ROWS) == 5
assert [r[3] for r in ROWS if r[0] == "a named object"] == ["name"] and ROWS[0][3] == "none"

# ------------------------------------------------------------------ canvas
fig = fig_mm(W, H)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
LABELS = []


def T(x, y, s, size=14, claim="V7.token_labels", weight=400, color=None, family=None, ha="left", va="center", z=6, **kw):
    t = ax.text(x, y, s, fontsize=size, fontweight=weight, color=color or C["ink"], ha=ha, va=va,
                family=family or "IBM Plex Sans", zorder=z, **kw)
    LABELS.append({"text": s, "pt": size, "claim": claim})
    return t


def wmm(t):
    return t.get_window_extent(fig.canvas.get_renderer()).width / fig.dpi * 25.4


def glyph(x, y, kind, s=3.6):
    """bytes: a filled square (the id hashes the observed bytes); list: three stacked bars (it hashes a list of ids);
    name: an open diamond (it hashes a name, not bytes)."""
    if kind == "bytes":
        ax.add_patch(Rectangle((x, y - s / 2), s, s, fc=C["emem"], ec="none", zorder=4))
    elif kind == "list":
        for k in range(3):
            ax.add_patch(Rectangle((x, y - s / 2 + k * s / 3 + 0.25), s, s / 3 - 0.5, fc=C["navy"], ec="none", zorder=4))
    elif kind == "name":
        ax.add_patch(Polygon([(x + s / 2, y - s / 2 - 0.3), (x + s + 0.3, y), (x + s / 2, y + s / 2 + 0.3), (x - 0.3, y)],
                             closed=True, fill=False, ec=C["agentA"], lw=0.9 / PTMM, zorder=4))


# columns
XN, XG, XH, XY = 0.0, 43.0, 119.5, W
hy = 2.8
T(XN, hy, "data need", 14, color=C["muted"])
T(XG, hy, "grammar, after emem:", 14, color=C["muted"])
T(XH, hy, "what its id hashes", 14, color=C["muted"])
ax.plot([0, W], [hy + 2.7, hy + 2.7], color=C["rule"], lw=0.5 / PTMM, zorder=2)
PITCH = 8.0
ty = hy + 2.7 + PITCH / 2 + 0.2
COLW = {"need": 0, "grammar": 0, "hash": 0}
for i, (need, gram, rule, kind) in enumerate(ROWS):
    yy = ty + i * PITCH
    if i % 2 == 1:
        ax.add_patch(Rectangle((0, yy - PITCH / 2), W, PITCH, fc=C["oos_bg"], ec="none", zorder=1.5))
    legacy = need in ("an embedding", "a device run")   # archived embeddings (no encoder runs); device runs in a reference harness
    ink = C["muted"] if legacy else C["ink"]
    COLW["need"] = max(COLW["need"], wmm(T(XN, yy, need, 14, color=ink, claim="A14.need")))
    COLW["grammar"] = max(COLW["grammar"], wmm(T(XG, yy, gram, 14, family=MONO, color=ink, claim="A14.grammar")))
    COLW["hash"] = max(COLW["hash"], wmm(T(XH, yy, rule, 14, color=C["muted"] if legacy else C["ink2"], claim="A14.hash")))
    # Hash semantics are given explicitly in the third column.
ybot = ty + 13 * PITCH + PITCH / 2
ax.plot([0, W], [ybot, ybot], color=C["rule"], lw=0.5 / PTMM, zorder=2)
print("column widths", {k: round(v, 1) for k, v in COLW.items()}, "starts", (XN, XG, XH, XY))
assert COLW["need"] <= XG - XN - 1.5 and COLW["grammar"] <= XH - XG - 1.5 and COLW["hash"] <= XY - XH - 1.5, COLW

# Full table, scoped to its inspected implementation; current object checks below it.
fy = ybot + 4.2
T(0, fy, "14 data needs; embedding and absence share the fact grammar.", 14, color=C["emem"], claim="V7.token_labels")
T(0, fy+5.2, "Names, sets and records hash differently.", 14, color=C["ink2"], claim="V7.token_labels")
T(0, fy+10.4, "Grey: archived embeddings; device runs in a reference harness.", 14, color=C["ink2"], claim="V7.token_labels")

# ------------------------------------------------------------------ labels must be covered by claims rows
CM = json.load(open(os.path.join(ROOT, "research/v13/12_claims_map_additions_F13-15.json")))
CROWS = {r["id"]: r for r in CM["rows"]}
for add in __import__("pathlib").Path(ROOT, "research/v13").glob("12_claims_map_additions_*.json"):
    CROWS.update({r["id"]:r for r in json.loads(add.read_text()).get("rows",[])})
NUM_RE = re.compile(r"(?<![\w.\-])[−+]?\d+(?:[.,]\d+)*(?!\w)")
nums = lambda s_: [m.group(0).lstrip("−+") for m in NUM_RE.finditer(s_)]
for L in LABELS:
    if not nums(L["text"]):
        continue
    assert L["claim"] in CROWS, f"label without a claims row: {L['text']!r}"
    own = {x for p in CROWS[L["claim"]]["print"] for x in nums(p)}
    missing = [x for x in nums(L["text"]) if x not in own]
    assert not missing, f"{L['claim']}: numbers {missing} of {L['text']!r} not in its print strings"

save(fig, NAME)
json.dump({"figure": NAME, "size_mm": [W, H], "labels": LABELS},
          open(os.path.join(OUT, f"{NAME}.labels.json"), "w"), indent=1, ensure_ascii=False)
