"""F13 · One address, every product (193.5 x 174 mm, right column).

One 10 m cell in central Berlin, read live from emem.dev on 30 Sep 2026, each product on its own native grid.
A common addressing layer, not a co-registered stack: the grid column names each product's native pixel.
  research/repro/v12/data/case_berlin_stack.json            the 25 live facts; 16 drawn (15 products, 4 signed absences)
  research/repro/v12/data/scene_defi.zb655.yaka.pUxe.png    the Sentinel-2C L2A true-colour chip emem served, 256 px of 10 m
  research/repro/v12/data/scene_defi.zb655.yaka.pUxe.headers  scene id, datetime, EPSG, bbox, pixel size, cloud cover
  research/repro/v12/data/v1_bands_2026-09-30.json          native grid sizes stated in the band ontology
With --refresh, every drawn fact is fetched again, GET https://emem.dev/v1/facts/<cid> (Accept application/cbor,
read-only), re-hashed with BLAKE3 to its cid, and checked for cell, band, value and the pinned signer; the result is
written to poster/fig/v13/f13_one_address.verify.json and asserted before drawing. Without network the last verify
file is accepted only if it says 16 of 16.
The "how emem encodes a memory" slot bar of v12 is not drawn: it has no legible room at 14 pt in 193.5 x 174 mm.

    python poster/figs_v13/f13_one_address.py
"""
import base64
import datetime as dt
import json
import os
import re
import ssl
import sys
import urllib.request

import blake3
import cbor2
import numpy as np
from matplotlib.patches import Rectangle, Polygon
import matplotlib.image as mpimg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import C, MONO, OUT, ROOT, fig_mm, save  # noqa: E402

W, H = 193.5, 174.0
PTMM = 25.4 / 72
NAME = "f13_one_address"
D = os.path.join(ROOT, "research/repro/v12/data")
PINNED = "777er3yihgifqmv5hmc2wwmyszgddzderzhsx6rex4yoakwomvka"      # emem.dev responder key (eo_evidence_verification.md)
TODAY = dt.date.today()

# ------------------------------------------------------------------ data
S = json.load(open(os.path.join(D, "case_berlin_stack.json")))
CELL = S["cell"]
assert CELL == "defi.zb655.yaka.pUxe"
LAT, LNG = S["cell_centre"]["lat"], S["cell_centre"]["lng"]
rows = S["rows"]


def pick(inst, qty, date=None):
    return next(r for r in rows if inst in r["instrument"] and qty in r["quantity"]
                and (date is None or (r["observed_at"] or "").startswith(date)))


hdr = open(os.path.join(D, f"scene_{CELL}.headers")).read()
hget = lambda k: re.search(rf"(?im)^{k}:\s*(.+?)\s*$", hdr).group(1)
SCENE = hget("x-emem-scene-item-id")
SCENE_DT = hget("x-emem-scene-datetime")
EPSG = int(hget("x-emem-scene-epsg"))
BBOX = [float(v) for v in hget("x-emem-scene-bbox-crs").split(",")]
PXS = [float(v) for v in hget("x-emem-scene-pixel-size").split(",")]
CLOUD = float(hget("x-emem-scene-cloud-cover"))
assert SCENE.startswith("S2C_MSIL2A_20260927") and EPSG == 32633 and PXS == [10.0, 10.0]
KM = (BBOX[2] - BBOX[0]) / 1000
assert KM == 2.56 and (BBOX[3] - BBOX[1]) / 1000 == 2.56

BANDS = {b["key"]: b for b in json.load(open(os.path.join(D, "v1_bands_2026-09-30.json")))["bands"]}


def band_says(key, phrase):
    b = BANDS[key]
    text = " ".join(x if isinstance(x, str) else json.dumps(x) for x in (b.get("description"), b.get("interpretation"), b.get("pitfalls")) if x)
    assert phrase in text, (key, phrase)
    return True


# the 16 drawn facts: (product, row, reading, valid time, native grid, grid source)
s2 = "Sentinel-" + SCENE[1:3] + " L2A"
NOT_STATED = "n/s"
SEL = [
    (s2, pick("Sentinel-2", "B08", "2026-09-27"), lambda r: f"NIR {r['value']:.4f}", "date", "10 m", "derivation arg 'B08 10m'"),
    (s2, pick("Sentinel-2", "NDVI", "2026-09-27"), lambda r: f"NDVI {r['value']:.3f}", "date", "10 m", "derivation reads B08/B04 10m"),
    ("Sentinel-1C RTC", pick("Sentinel-1", "VV", "2026-09-28"), lambda r: f"VV {r['value']:.2f} dB".replace("-", "−"), "date", NOT_STATED, None),
    ("GLO-30 DEM", pick("Copernicus DEM", "elevation"), lambda r: f"{r['value']:.1f} m DSM", "year", "30 m", "band copdem30m; COG copernicus-dem-30m"),
    ("MODIS MOD11A2", pick("MOD11A2", "temperature"), lambda r: f"{r['value']:.1f} K day LST", "date", "1 km", "source band LST_Day_1km"),
    ("ESA WorldCover", pick("WorldCover", "class"), lambda r: f"built-up ({int(r['value'])})", "2021", "10 m", "v1_bands landcover 'at 10 m'"),
    ("ESA CCI Biomass", pick("CCI Biomass", "biomass"), lambda r: f"{r['value']:.0f} t/ha", "2022", "100 m", "v1_bands esa_cci_biomass 'at 100 m'"),
    ("JRC GSW v1.4", pick("Surface Water", "occurrence"), lambda r: f"{r['value']:.0f} % water", "1984 to 2021", "30 m", "v1_bands surface_water 'at 30 m'"),
    ("Hansen v1.13", pick("Hansen", "tree cover"), lambda r: f"{r['value']:.0f} % tree cover", "2000", NOT_STATED, None),
    ("JRC GFC2020 V4", pick("Forest Cover 2020", "forest"), lambda r: "not forest" if r["value"] == 0 else "forest", "2020", "10 m", "v1_bands jrc_gfc2020 '10 m native'"),
    ("Copernicus CAMS", pick("Copernicus Atmosphere", "NO2", "2026-09-30"), lambda r: f"NO₂ {r['value']:.1f} µg/m³", "date", "~11 km", "v1_bands air_quality '~11 km'"),
    ("Overture, not EO", pick("Overture", "building"), lambda r: f"{int(r['value'])} buildings", "release", "vector", "source s3 theme=buildings (no raster)"),
    ("ISRIC SoilGrids", pick("SoilGrids", "organic carbon"), lambda r: "no data, null", "signed", "250 m", "v1_bands soilgrids '250 m native'"),
    ("CHIRPS v2.0", pick("CHIRPS", "precip"), lambda r: "outside ±50°", "signed", "0.05°", "v1_bands chirps '0.05°'; source cog p05"),
    ("JRC TMF", pick("Tropical Moist", "deforestation"), lambda r: "outside ±30°", "signed", "30 m", "v1_bands jrc_tmf '30 m primary product'"),
    ("NASA FIRMS", pick("FIRMS", "fire"), lambda r: "no fire in 24 h", "signed", "points", "absence reason: detections within the cell bbox"),
]
assert len(SEL) == 16 and len({s[0] for s in SEL}) == 15
assert sum(s[1]["kind"] == "absence" for s in SEL) == 4
assert all(s[1]["verified"] is True for s in SEL)
# the stated grids are read from the files they are attributed to
band_says("landcover", "at 10 m"); band_says("esa_cci_biomass", "at 100 m"); band_says("surface_water", "at 30 m")
band_says("jrc_gfc2020", "10 m native"); band_says("air_quality", "~11 km"); band_says("soilgrids", "250 m native")
band_says("chirps.precip_daily_mm", "0.05°"); band_says("jrc_tmf", "30 m primary")
assert "within cell bbox" in SEL[15][1]["absence_reason"]
assert "±50°" in SEL[13][1]["absence_reason"] and "±30°" in SEL[14][1]["absence_reason"]
assert SEL[2][1]["value"] == -2.8157914266581785 and SEL[4][1]["instrument"].endswith("(1 km, 8-day)")

# ------------------------------------------------------------------ re-verification (live, read-only)
VERIFY = os.path.join(OUT, f"{NAME}.verify.json")
b32 = lambda b: base64.b32encode(b).decode().lower().rstrip("=")


def fetch(cid):
    ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt" if os.path.exists("/root/.ccr/ca-bundle.crt") else None)
    req = urllib.request.Request(f"https://emem.dev/v1/facts/{cid}", headers={"Accept": "application/cbor"})
    return urllib.request.urlopen(req, timeout=40, context=ctx).read()


def reverify():
    out = {"fetched_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "endpoint": "GET https://emem.dev/v1/facts/<cid> (Accept: application/cbor)",
           "pinned_signer": PINNED, "facts": []}
    for prod, r, *_ in SEL:
        b = fetch(r["fact_cid"])
        d = cbor2.loads(b)
        rec = {"product": prod, "band": r["band"], "fact_cid": r["fact_cid"], "bytes": len(b),
               "rehash_equals_cid": b32(blake3.blake3(b).digest()) == r["fact_cid"],
               "cell_bound": d.get("cell") == CELL, "band_bound": d.get("band") == r["band"],
               "signer_pinned": b32(bytes(d["signer"])) == PINNED,
               "value_matches_json": (d.get("value") == r["value"]) if r["kind"] == "primary" else (d.get("kind") == "absence"),
               "grid_arg": None}
        if r["band"] == "s2.B08":
            rec["grid_arg"] = d["derivation"]["args"][4]
        if r["band"] == "modis.lst_day_8day":
            rec["grid_arg"] = d["derivation"]["args"][3]
        if r["band"] == "copdem30m.elevation_mean":
            rec["grid_arg"] = d["sources"][0]["id"].split("/")[2]
        if r["band"] == "chirps.precip_daily_mm":
            rec["grid_arg"] = [p for p in d["sources"][0]["id"].split("/") if p.startswith("p0")][0]
        if r["band"] == "overture.buildings.count":
            rec["grid_arg"] = d["sources"][0]["id"]
        rec["ok"] = all(rec[k] for k in ("rehash_equals_cid", "cell_bound", "band_bound", "signer_pinned", "value_matches_json"))
        out["facts"].append(rec)
    out["n"] = len(out["facts"]); out["n_ok"] = sum(f["ok"] for f in out["facts"])
    return out


try:
    V = reverify() if "--refresh" in sys.argv else json.load(open(VERIFY))
    json.dump(V, open(VERIFY, "w"), indent=1)
    print(f"evidence verification: {V['n_ok']} of {V['n']} ({V['fetched_utc']}); refresh={'--refresh' in sys.argv}")
except (OSError, urllib.error.URLError) as e:   # no network: the last verify file must say 16 of 16
    if not os.path.exists(VERIFY):
        raise SystemExit(f"re-verification impossible: {e}")
    V = json.load(open(VERIFY))
    print(f"offline: using {VERIFY} from {V['fetched_utc']}: {V['n_ok']} of {V['n']}")
assert V["n"] == 16 and V["n_ok"] == 16, V
G = {f["band"]: f["grid_arg"] for f in V["facts"]}
assert G["s2.B08"].startswith("B08 10m") and G["modis.lst_day_8day"] == "LST_Day_1km"
assert G["copdem30m.elevation_mean"] == "copernicus-dem-30m.s3.amazonaws.com" and G["chirps.precip_daily_mm"] == "p05"
assert "theme=buildings" in G["overture.buildings.count"]
VERIFIED_ON = dt.datetime.strptime(V["fetched_utc"][:10], "%Y-%m-%d").date()

# ------------------------------------------------------------------ the chip: the cell's containing pixel
img = mpimg.imread(os.path.join(D, f"scene_{CELL}.png"))
if img.dtype != np.uint8:
    img = (img * 255 + 0.5).astype(np.uint8)
img = img[..., :3]
assert img.shape == (256, 256, 3)
from pyproj import Transformer  # noqa: E402
E, N = Transformer.from_crs(4326, EPSG, always_xy=True).transform(LNG, LAT)
col = int(np.floor((E - BBOX[0]) / PXS[0]))
row = int(np.floor((BBOX[3] - N) / PXS[1]))
assert (col, row) == (128, 128), (col, row)      # the chip is centred on the cell's node: pixel (128, 128) contains it
BOXPX = 9                                        # a 9 x 9 pixel (90 m) box so the marker stays visible at 2 px per 10 m

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


def runs(x, y, parts):
    for s, kw in parts:
        t = T(x, y, s, **kw)
        x += wmm(t)
    return x


CLS = {"direct_sensor": C["emem"], "deterministic_index": C["L1"], "model_output": C["incident"],
       "human_curated": C["agentA"], "unclassified": C["oos"]}
CLS_LABEL = {"direct_sensor": "direct sensor", "deterministic_index": "deterministic index", "model_output": "model output",
             "human_curated": "human curated", "unclassified": "unclassified"}


def glyph(x, y, cls, absent, w=3.2, h=4.6):
    """Provenance class as a filled bar; a signed absence is the same bar, hatched on white."""
    col = CLS[cls]
    if absent:
        ax.add_patch(Rectangle((x, y - h / 2), w, h, fc="white", ec=col, lw=0.9 / PTMM, hatch="////", zorder=4))
    else:
        ax.add_patch(Rectangle((x, y - h / 2), w, h, fc=col, ec="none", zorder=4))


def fmt_date(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")[:19]).strftime("%-d %b %Y")


# ------------------------------------------------------------------ Berlin locator and provenance legend
READ_ON = fmt_date(SEL[0][1]["queried_at_utc"])
assert READ_ON == "30 Sep 2026"
CROP, CS, CX, CY = 224, 50.0, 0.0, 1.0
C0 = (256 - CROP) // 2
big = np.repeat(np.repeat(img[C0:C0+CROP, C0:C0+CROP], 6, 0), 6, 1)
ax.imshow(big, extent=(CX,CX+CS,CY+CS,CY),interpolation="none",zorder=1)
s = CS / CROP
half = BOXPX / 2 * s
mx, my = (col-C0+.5)*s, CY+(row-C0+.5)*s
ax.add_patch(Rectangle((mx-half,my-half),2*half,2*half,fill=False,ec="white",lw=1.5/PTMM,zorder=4))
ax.add_patch(Rectangle((mx-half,my-half),2*half,2*half,fill=False,ec=C["emem"],lw=.6/PTMM,zorder=5))
T(56,5,"BERLIN",22,claim="A13.head",weight=700,color=C["emem"])
T(56,14,CELL,14,claim="A13.head",family=MONO)
T(56,21,f"{LAT:.4f} N, {LNG:.4f} E · one 10 m cell",14,claim="A13.head")
for i,c in enumerate(["direct_sensor","deterministic_index","model_output","human_curated","unclassified"]):
    xx=56 if i<3 else 125
    yy=30+(i if i<3 else i-3)*7
    glyph(xx,yy,c,False)
    T(xx+5,yy,CLS_LABEL[c],14,color=C["ink2"],claim="V6.berlin_labels")
T(0,55,"Sentinel-2C L2A · 27 Sep 2026 · RGB · 2.24 km across; box: 90 m",14,claim="A13.chip",color=C["ink2"])
LEG_END=57

# ------------------------------------------------------------------ the table
X0 = 0.0
XG, XP = X0, X0 + 4.6
XR = 54.0
XT = 98.0
XN = 138.0
XC = W - 1.2
assert XN + 16.4 + 2.0 + 19.8 <= XC, (XN, XC)
hy = 63.0
for xx, lab in ((XP, "product"), (XR, "signed reading"), (XT, "valid time"), (XN, "grid")):
    T(xx, hy, lab, 14, color=C["muted"], claim="V6.berlin_labels")
T(XC, hy, "fact_cid", 14, color=C["muted"], ha="right", family=MONO, claim="V6.berlin_labels")
ax.plot([X0, W], [hy + 2.9, hy + 2.9], color=C["rule"], lw=0.5 / PTMM, zorder=2)
PITCH = 5.5
ty = hy + 2.9 + PITCH / 2 + 0.3
COLW = {}
for i, (prod, r, reading, when, grid, _src) in enumerate(SEL):
    yy = ty + i * PITCH
    absent = r["kind"] == "absence"
    if i % 2 == 1:
        ax.add_patch(Rectangle((X0, yy - PITCH / 2), W - X0, PITCH, fc=C["oos_bg"], ec="none", zorder=1.5))
    glyph(XG, yy, r["provenance_class"], absent)
    COLW["product"] = max(COLW.get("product", 0), wmm(T(XP, yy, prod, 14, weight=400, claim="A13.products")))
    COLW["reading"] = max(COLW.get("reading", 0), wmm(T(XR, yy, reading(r), 14, color=C["ink2"] if absent else C["ink"], style="italic" if absent else "normal", claim="A13.readings")))
    o = r["observed_at"] or ""
    if when == "date":
        tt = fmt_date(o)
    elif when == "year":
        tt = o[:4]
    elif when == "release":
        tt = dt.datetime.strptime(o[:10], "%Y-%m-%d").strftime("%b %Y")
    elif when == "signed":
        tt = fmt_date(r["signed_at"])
    else:
        tt = when
    COLW["time"] = max(COLW.get("time", 0), wmm(T(XT, yy, tt, 14, color=C["ink2"], claim="A13.times")))
    COLW["grid"] = max(COLW.get("grid", 0), wmm(T(XN, yy, grid, 14, color=C["muted"] if grid == NOT_STATED else C["ink2"], claim="A13.grids")))
    COLW["cid"] = max(COLW.get("cid", 0), wmm(T(XC, yy, r["fact_cid"][:6] + "…", 14, family=MONO, color=C["ink2"], ha="right", claim="A13.cids")))
ybot = ty + 15 * PITCH + PITCH / 2
assert COLW["product"] <= XR - XP - 1.0 and COLW["reading"] <= XT - XR - 1.0 and COLW["time"] <= XN - XT - 1.0, COLW
assert COLW["grid"] <= XC - COLW["cid"] - XN - 1.0, COLW
print("column max widths mm", {k: round(v, 1) for k, v in COLW.items()}, "starts", dict(product=XP, reading=XR, time=XT, grid=XN, cid_right=XC))
ax.plot([X0, W], [ybot, ybot], color=C["rule"], lw=0.5 / PTMM, zorder=2)

# ------------------------------------------------------------------ footer: scope (full width, wrapped at 14 pt)
def wrap(text, width, size):
    words, lines, cur = text.split(" "), [], ""
    probe = ax.text(0, 0, "", fontsize=size, family="IBM Plex Sans")
    for w_ in words:
        cand = (cur + " " + w_).strip()
        probe.set_text(cand)
        if wmm(probe) > width and cur:
            lines.append(cur); cur = w_
        else:
            cur = cand
    lines.append(cur); probe.remove()
    return lines


SCOPE = (f"15 products, 16 signed facts, 4 signed absences, 10\u00a0m to about 11\u00a0km; read live {READ_ON}. "
         "Native grids remain distinct; n/s: grid not in source files. "
         f"16 records re-hash under emem.dev's key, {VERIFIED_ON.strftime('%-d %b %Y')}.")
fy = ybot + 3.4
lines = wrap(SCOPE, W - 3.0, 14)
assert len(lines) <= 3, lines
for k, ln in enumerate(lines):
    T(X0, fy + k * 5.2, ln, 14, color=C["ink2"], claim="A13.scope")
assert LEG_END <= H
assert fy + (len(lines) - 1) * 5.2 + 2.6 <= H, fy

# ------------------------------------------------------------------ labels must be covered by claims rows
CM = json.load(open(os.path.join(ROOT, "research/v13/12_claims_map_additions_F13-15.json")))
ROWS = {r["id"]: r for r in CM["rows"]}
NUM_RE = re.compile(r"(?<![\w.\-])[−+]?\d+(?:[.,]\d+)*(?!\w)")
nums = lambda s_: [m.group(0).lstrip("−+") for m in NUM_RE.finditer(s_)]
for L in LABELS:
    if not nums(L["text"]):
        continue
    assert L["claim"] in ROWS, f"label without a claims row: {L['text']!r}"
    own = {x for p in ROWS[L["claim"]]["print"] for x in nums(p)}
    missing = [x for x in nums(L["text"]) if x not in own]
    assert not missing, f"{L['claim']}: numbers {missing} of {L['text']!r} not in its print strings"

save(fig, NAME)
json.dump({"figure": NAME, "size_mm": [W, H], "cell": CELL, "scene": SCENE, "reverified": V["fetched_utc"],
           "labels": LABELS}, open(os.path.join(OUT, f"{NAME}.labels.json"), "w"), indent=1, ensure_ascii=False)
