#!/usr/bin/env python3
"""eight_answers.py: re-derive the eight NDVI answers to one question (brief section C panel 2, figure F3).

Question: NDVI at the Keylong field cell defi.zb572.xoso.zb1ec on 25 Sep 2026 (tslot 20721).
Rule under test (constructed, pre-registered): irrigate iff NDVI <= 0.4705 (read from R1's meta.rule).

Each value is re-derived here, never copied from prose:
  committed  files in this repository (the signed record bytes in the proof bundle, re-hashed with BLAKE3;
             pixel_check.json; cell_products.json; ask_keylong.json; results.json; e84_keylong.json)
  live       read-only public sources: Element84 Earth Search STAC (/v1/search) and Planetary Computer STAC
             (/collections/.../items/<id>, SAS token endpoint), then COG range reads of one pixel with rasterio.
             No emem endpoint is called at all, and nothing is written or minted anywhere.
Every value records its provenance and whether the committed and live derivations agree (to 1e-12).
A value that cannot be re-derived is kept with rederived = false and the reason; the script then exits 2.

Output: research/repro/v13/eight_answers.json        python research/repro/v13/eight_answers.py [--offline]
Needs:  blake3, cbor2, pynacl (via the R1 suite), rasterio, pyproj, requests.
"""
import datetime as dt
import json
import math
import os
import re
import sys
from pathlib import Path

import blake3

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/repro/v11"))
import mutation_suite as R1  # noqa: E402  (committed R1 suite: the signed bundle, the NDVI rule, the rounding mutation)

OUT = Path(__file__).resolve().parent / "eight_answers.json"
D = ROOT / "research/repro/data"
OFFLINE = "--offline" in sys.argv
E84_SEARCH = "https://earth-search.aws.element84.com/v1/search"
MPC_STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
MPC_SAS = "https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-2-l2a"
TOL = 1e-12


def rel(p):
    return str(Path(p).resolve().relative_to(ROOT))


def jload(p):
    return json.loads(Path(p).read_text())


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ndvi_dn(b8, b4, off):
    """NDVI from DNs with an additive DN offset (ESA L2A: BOA_ADD_OFFSET -1000 from baseline 04.00)."""
    return R1.ndvi(float(b8), float(b4), float(off))


def ndvi_refl(b8, b4, scale, offset):
    """NDVI from DNs turned into reflectance with STAC raster:bands scale and offset."""
    r8, r4 = b8 * scale + offset, b4 * scale + offset
    return (r8 - r4) / (r8 + r4)


# ------------------------------------------------------------------ committed inputs
BUNDLE_FACT = R1.FACT                       # the 1,115 signed bytes of oj5cecci, from the committed proof bundle
TOKEN = R1.BUNDLE["token"]
CID = TOKEN.split(":")[3]
assert R1.b32e(blake3.blake3(BUNDLE_FACT).digest()) == CID, "signed record bytes do not re-hash to the token's address"
FACT = R1.FACT_D
ARGS = FACT["derivation"]["args"]
LAT, LNG, SCENE_S2A, EPSG = ARGS[0], ARGS[1], ARGS[2], ARGS[3]
SIGNED_B8, SIGNED_B4 = ARGS[R1.DN_IDX]
SIGNED_OFF = ARGS[R1.OFF_IDX]
RULE = R1.RULE
mm = jload(ROOT / "research/repro/v11/out/mutation_matrix.json")
assert re.search(r"NDVI\s*<=\s*([0-9.]+)", mm["meta"]["rule"]).group(1) == repr(RULE)
TSLOT = R1.QUESTION["tslot"]
QDATE = (dt.date(1970, 1, 1) + dt.timedelta(days=TSLOT)).isoformat()

pc = jload(D / "v8/pixel_check.json")
pc_s2a = next(v for k, v in pc.items() if "oj5cecci" in k)
cp = jload(D / "v11/cell_products.json")
cp_ndvi = next(r for r in cp if r["band"] == "indices.ndvi")
ask = jload(D / "v11/ask_keylong.json")
ask_fact = next(b for b in ask["band_observations_summary"]["bands"] if b["band"] == "indices.ndvi")
place = ask["place_resolved"]
q_lat, q_lng = (float(x) for x in re.search(r"\(([0-9.]+) N, ([0-9.]+) E\)", ask["question"]).groups())
res = jload(D / "v8/results.json")
armR = res["b"]["claude-haiku-4-5"]["arms"]["R"]
e84c = jload(ROOT / "research/v13/evidence/failure_modes/e84_keylong.json")
FROZEN = ROOT / "research/repro/v13/r5/frozen"


def frozen_record(name, cid_prefix):
    """A signed record committed with R5's frozen inputs: re-hash its bytes to its token's address."""
    import cbor2
    d = cbor2.loads((FROZEN / f"{name}.cbor").read_bytes())
    cid = R1.b32e(blake3.blake3(d["bytes"]).digest())
    assert d["token"].endswith(":" + cid) and cid.startswith(cid_prefix), f"{name}: bytes do not re-hash to the token"
    return d["token"], cbor2.loads(d["bytes"]), len(d["bytes"])


# ------------------------------------------------------------------ live, read-only
def utm_rowcol(lat, lng, transform):
    from pyproj import Transformer
    x, y = Transformer.from_crs("EPSG:4326", f"EPSG:{EPSG}", always_xy=True).transform(lng, lat)
    col = (x - transform.c) / transform.a
    row = (y - transform.f) / transform.e
    return row, col


def read_pixel(href, lat, lng, which="floor"):
    """One-pixel COG range read. which='floor' = the pixel that contains the point (PixelIsArea);
    'round' = the rule emem's old reader used (round the fractional index)."""
    import rasterio
    from rasterio.windows import Window
    with rasterio.open(href) as ds:
        assert ds.crs.to_epsg() == EPSG and ds.tags().get("AREA_OR_POINT", "Area") == "Area"
        row, col = utm_rowcol(lat, lng, ds.transform)
        r, c = (math.floor(row + 1e-6), math.floor(col + 1e-6)) if which == "floor" else (round(row), round(col))
        v = int(ds.read(1, window=Window(c, r, 1, 1))[0, 0])
        return v, (r, c), (round(row, 4), round(col, 4))


def http_json(url, **kw):
    import requests
    r = requests.get(url, timeout=60, **kw)
    r.raise_for_status()
    return r.json()


LIVE = {"fetched_utc": None, "e84_items": {}, "mpc_items": {}, "reads": {}, "errors": []}
if not OFFLINE:
    os.environ.update(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", AWS_NO_SIGN_REQUEST="YES",
                      CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif", GDAL_HTTP_MAX_RETRY="3")
    LIVE["fetched_utc"] = now()
    try:
        fc = http_json(E84_SEARCH, params={"collections": "sentinel-2-l2a",
                                           "intersects": json.dumps({"type": "Point", "coordinates": [LNG, LAT]}),
                                           "datetime": "2026-09-20T00:00:00Z/2026-09-30T23:59:59Z", "limit": 20})
        for f in fc["features"]:
            p, red = f["properties"], f["assets"]["red"]
            LIVE["e84_items"][f["id"]] = {
                "red": red["href"], "nir": f["assets"]["nir"]["href"],
                "boa_offset_applied": p.get("earthsearch:boa_offset_applied"),
                "processing_baseline": p.get("s2:processing_baseline"),
                "red_raster_bands": red.get("raster:bands"), "cloud": p.get("eo:cloud_cover"),
                "product_uri": p.get("s2:product_uri")}
    except Exception as e:  # pragma: no cover
        LIVE["errors"].append(f"e84 search: {e!r}")
    try:
        sas = http_json(MPC_SAS)["token"]
        mpc_ids = {"S2A_25Sep": "S2A_MSIL2A_20260925T054251_R005_T43SFS_20260925T090015",
                   "S2C_30Sep": None}
        # the 30 Sep scene id is the one the /v1/ask answer fact names (report 05 sec. 4.5); search it, never type it
        s = http_json(f"{MPC_STAC}/search", params={"collections": "sentinel-2-l2a",
                                                      "intersects": json.dumps({"type": "Point",
                                                                                "coordinates": [LNG, LAT]}),
                                                      "datetime": "2026-09-30T00:00:00Z/2026-09-30T23:59:59Z"})
        s30 = [f["id"] for f in s["features"] if f["id"].startswith("S2C_MSIL2A_20260930") and "T43SFS" in f["id"]]
        mpc_ids["S2C_30Sep"] = s30[0] if s30 else None
        assert mpc_ids["S2A_25Sep"] == SCENE_S2A, "signed scene id differs from the MPC item id"
        for k, iid in mpc_ids.items():
            if not iid:
                LIVE["errors"].append(f"mpc: no item for {k}")
                continue
            it = http_json(f"{MPC_STAC}/collections/sentinel-2-l2a/items/{iid}")
            LIVE["mpc_items"][k] = {"id": iid, "B04": it["assets"]["B04"]["href"], "B08": it["assets"]["B08"]["href"],
                                    "processing_baseline": it["properties"].get("s2:processing_baseline")}
            LIVE["mpc_items"][k]["_sas"] = sas
    except Exception as e:  # pragma: no cover
        LIVE["errors"].append(f"mpc: {e!r}")


def e84(item_id):
    return LIVE["e84_items"].get(item_id)


def live_read(key, href, lat, lng, which="floor", sas=None):
    try:
        v, rc, frac = read_pixel(href + ("?" + sas if sas else ""), lat, lng, which)
        LIVE["reads"][key] = {"href": href, "pixel_row_col": list(rc), "fractional_row_col": list(frac),
                              "rule": which, "DN": v}
        return v
    except Exception as e:  # pragma: no cover
        LIVE["errors"].append(f"read {key}: {e!r}")
        return None


def mpc_read(k, band, lat, lng, which="floor"):
    it = LIVE["mpc_items"].get(k)
    if not it:
        return None
    return live_read(f"mpc.{k}.{band}.{which}", it[band], lat, lng, which, it["_sas"])


def e84_read(item_id, band, lat, lng, which="floor"):
    it = e84(item_id)
    if not it:
        return None
    return live_read(f"e84.{item_id}.{band}.{which}", it["nir" if band == "B08" else "red"], lat, lng, which)


def agree(a, b):
    return a is not None and b is not None and abs(a - b) <= TOL


rows = []


def add(key, claim, label, value, kind, check, layer, decision, provenance, rederived, note=""):
    rows.append({"key": key, "claim": claim, "label": label, "value": value, "print": f"{value:.4f}",
                 "dot": kind, "check": check, "layer": layer, "decision": decision,
                 "provenance": provenance, "rederived": rederived, "note": note})


def decide(v):
    if not -1.0 <= v <= 1.0:
        return "invalid"
    return "irrigate" if v <= RULE else "hold"


# 1. the signed record: re-hash, recompute, re-read at the source (MPC) and at Element84 (harmonised DNs)
v_fact = FACT["value"]
v_recomp = ndvi_dn(SIGNED_B8, SIGNED_B4, SIGNED_OFF)
mb8, mb4 = mpc_read("S2A_25Sep", "B08", LAT, LNG), mpc_read("S2A_25Sep", "B04", LAT, LNG)
E84_S2A = "S2A_43SFS_20260925_1_L2A"
eb8, eb4 = e84_read(E84_S2A, "B08", LAT, LNG), e84_read(E84_S2A, "B04", LAT, LNG)
live_mpc_ok = mb8 == SIGNED_B8 and mb4 == SIGNED_B4
live_e84 = ndvi_dn(eb8, eb4, 0) if eb8 is not None else None
add("right", "E8.right", "signed record", v_fact, "filled", None, None, decide(v_fact), [
    {"kind": "committed", "file": "research/repro/v8/proof_bundle_ndvi.cbor", "pointer": "fact bytes",
     "check": f"BLAKE3 of {len(BUNDLE_FACT)} B = {CID}"},
    {"kind": "committed", "file": "research/repro/v8/proof_bundle_ndvi.cbor", "pointer": "derivation.args DNs + offset",
     "recomputed": v_recomp, "equal": agree(v_recomp, v_fact)},
    {"kind": "committed", "file": rel(D / "v8/pixel_check.json"), "pointer": "S2A ... ndvi_floor_pixel",
     "value": pc_s2a["ndvi_floor_pixel"], "equal": agree(pc_s2a["ndvi_floor_pixel"], v_fact)},
    {"kind": "live", "source": "Planetary Computer COG (the record's own source files)", "DN_B08_B04": [mb8, mb4],
     "equal_signed_DNs": live_mpc_ok},
    {"kind": "live", "source": f"Element84 {E84_S2A} COG (offset already applied)", "DN_B08_B04": [eb8, eb4],
     "ndvi": live_e84, "equal": agree(live_e84, v_fact)}],
    rederived=agree(v_recomp, v_fact) and (OFFLINE or (live_mpc_ok and agree(live_e84, v_fact))))

# 2. rounded in prose: R1's own rounding mutation (M2) and the G2 arm that handed "0.47"
h = R1.m_stated_round(R1.genuine())
v_round = float(h["stated"])
add("rounded", "E8.rounded", "rounded in prose", v_round, "hollow", "resolve", "L0", decide(v_round), [
    {"kind": "committed", "file": "research/repro/v11/mutation_suite.py", "pointer": "m_stated_round(genuine())['stated']",
     "value": h["stated"]},
    {"kind": "committed", "file": rel(D / "v8/results.json"), "pointer": "b.claude-haiku-4-5.arms.R.decisions",
     "value": armR["decisions"], "n": armR["n"]},
    {"kind": "committed", "file": rel(D / "v8/prereg.md"), "pointer": "line 16: 0.4708994708994709 -> \"0.47\""}],
    rederived=h["stated"] == f"{round(v_fact, 2)}" and armR["decisions"]["IRRIGATE"] == armR["n"],
    note="value as handed in prose; formatted to 4 decimals only for the axis; printed as 0.47")
rows[-1]["print"] = h["stated"]

# 3. other satellite, same day: Sentinel-2B, 25 Sep, relative orbit 105 (same tslot)
E84_S2B = "S2B_43SFS_20260925_0_L2A"
b8, b4 = e84_read(E84_S2B, "B08", LAT, LNG), e84_read(E84_S2B, "B04", LAT, LNG)
it = e84(E84_S2B) or {}
off = 0 if it.get("boa_offset_applied") else None
v_s2b = ndvi_dn(b8, b4, off) if (b8 is not None and off is not None) else None
add("s2b", "E8.s2b", "other satellite, same day", v_s2b if v_s2b is not None else float("nan"), "filled", "scene id",
    "L1", decide(v_s2b) if v_s2b is not None else None, [
        {"kind": "live", "source": f"Element84 {E84_S2B} COG", "url": it.get("red"), "DN_B08_B04": [b8, b4],
         "boa_offset_applied": it.get("boa_offset_applied"), "product_uri": it.get("product_uri")},
        {"kind": "reference", "file": "research/v13/05_failure_modes_catastrophe.md", "pointer": "sec. 4.2 (1014/2588)",
         "equal": [b4, b8] == [1014, 2588]}],
    rederived=v_s2b is not None and [b4, b8] == [1014, 2588])

# 4. a later record handed as the 25 Sep answer: the 30 Sep record of the same cell
v_new = cp_ndvi["value"]
tok30, rec30, n30 = frozen_record("3yyaxn5d", cp_ndvi["cid"])
a30 = rec30["derivation"]["args"]
v_new_dn = ndvi_dn(*a30[R1.DN_IDX], a30[R1.OFF_IDX])
E84_S2C30 = "S2C_43SFS_20260930_0_L2A"
c8, c4 = e84_read(E84_S2C30, "B08", a30[0], a30[1]), e84_read(E84_S2C30, "B04", a30[0], a30[1])
v_new_live = ndvi_dn(c8, c4, 0) if c8 is not None else None
add("newer", "E8.newer", "30 Sep record handed as 25 Sep", v_new, "filled", "date", "L1", decide(v_new), [
    {"kind": "committed", "file": rel(D / "v11/cell_products.json"), "pointer": "band=indices.ndvi value",
     "cid": cp_ndvi["cid"], "tslot": cp_ndvi["tslot"], "signed_at": cp_ndvi["signed_at"]},
    {"kind": "committed", "file": rel(FROZEN / "3yyaxn5d.cbor"), "pointer": "bytes (re-hashed to the token)",
     "token": tok30, "bytes": n30, "scene": a30[2], "DN_B08_B04": a30[R1.DN_IDX], "offset": a30[R1.OFF_IDX],
     "recomputed": v_new_dn, "equal": agree(v_new_dn, v_new) and rec30["value"] == v_new},
    {"kind": "live", "source": f"Element84 {E84_S2C30} COG", "DN_B08_B04": [c8, c4], "ndvi": v_new_live,
     "equal": agree(v_new_live, v_new)}],
    rederived=agree(v_new_dn, v_new) and (OFFLINE or agree(v_new_live, v_new)))

# 5. the neighbour pixel: the old reader's rounded index on the same scene, 10 m south
v_nb = pc_s2a["ndvi_round_pixel"]
r8, r4 = mpc_read("S2A_25Sep", "B08", LAT, LNG, "round"), mpc_read("S2A_25Sep", "B04", LAT, LNG, "round")
v_nb_live = ndvi_dn(r8, r4, SIGNED_OFF) if r8 is not None else None
v_nb_dn = ndvi_dn(pc_s2a["B08"]["round_DN"], pc_s2a["B04"]["round_DN"], SIGNED_OFF)
add("neighbour", "E8.neighbour", "neighbour pixel", v_nb, "hollow", "re-read pixel", "L3", decide(v_nb), [
    {"kind": "committed", "file": rel(D / "v8/pixel_check.json"), "pointer": "S2A ... round_DN, ndvi_round_pixel",
     "recomputed": v_nb_dn, "equal": agree(v_nb_dn, v_nb)},
    {"kind": "live", "source": "Planetary Computer COG, round(row, col)", "DN_B08_B04": [r8, r4], "ndvi": v_nb_live,
     "equal": agree(v_nb_live, v_nb)}],
    rederived=agree(v_nb_dn, v_nb) and (OFFLINE or agree(v_nb_live, v_nb)))

# 6. the BOA offset left out: the record's own DNs read with offset 0
v_off0 = ndvi_dn(SIGNED_B8, SIGNED_B4, 0)
add("offset0", "E8.offset0", "offset left out", v_off0, "hollow", "catalogue offset", "L3", decide(v_off0), [
    {"kind": "committed", "file": "research/repro/v8/proof_bundle_ndvi.cbor", "pointer": "derivation.args DNs",
     "DN_B08_B04": [SIGNED_B8, SIGNED_B4], "formula": "(B08 - B04) / (B08 + B04)"},
    {"kind": "live", "source": "Planetary Computer COG", "DN_B08_B04": [mb8, mb4], "equal_signed_DNs": live_mpc_ok}],
    rederived=OFFLINE or live_mpc_ok)

# 7. the place name won over the coordinates: /v1/ask answered from the town point (30 Sep scene)
v_pl = ask_fact["value"]
from pyproj import Geod  # noqa: E402
_, _, dist = Geod(ellps="WGS84").inv(q_lng, q_lat, place["lng"], place["lat"])
tokp, recp, np_ = frozen_record("p6ewjnlq", ask_fact["fact_cid"])
ap = recp["derivation"]["args"]                      # the record's own read point (the town point's cell)
v_pl_dn = ndvi_dn(*ap[R1.DN_IDX], ap[R1.OFF_IDX])
assert (LIVE["mpc_items"].get("S2C_30Sep") or {}).get("id", ap[2]) == ap[2], "30 Sep MPC item differs from the record"
t8, t4 = mpc_read("S2C_30Sep", "B08", ap[0], ap[1]), mpc_read("S2C_30Sep", "B04", ap[0], ap[1])
v_pl_live = ndvi_dn(t8, t4, ap[R1.OFF_IDX]) if t8 is not None else None
add("place", "E8.place", f"town point {round(dist)} m away (30 Sep)", v_pl, "filled", "asked coordinates", "L1",
    decide(v_pl), [
        {"kind": "committed", "file": rel(D / "v11/ask_keylong.json"), "pointer": "band_observations_summary indices.ndvi",
         "fact_cid": ask_fact["fact_cid"]},
        {"kind": "committed", "file": rel(D / "v11/ask_keylong.json"), "pointer": "question vs place_resolved",
         "asked": [q_lat, q_lng], "answered": [place["lat"], place["lng"]], "geodesic_m_wgs84": round(dist, 2)},
        {"kind": "committed", "file": rel(FROZEN / "p6ewjnlq.cbor"), "pointer": "bytes (re-hashed to the token)",
         "token": tokp, "bytes": np_, "read_point": ap[:2], "scene": ap[2], "DN_B08_B04": ap[R1.DN_IDX],
         "offset": ap[R1.OFF_IDX], "recomputed": v_pl_dn, "equal": agree(v_pl_dn, v_pl) and recp["value"] == v_pl},
        {"kind": "live", "source": "Planetary Computer COG, S2C 30 Sep, the record's read point",
         "item": (LIVE["mpc_items"].get("S2C_30Sep") or {}).get("id"), "DN_B08_B04": [t8, t4],
         "ndvi": v_pl_live, "equal": agree(v_pl_live, v_pl)}],
    rederived=agree(v_pl_dn, v_pl) and (OFFLINE or agree(v_pl_live, v_pl)))
rows[-1]["distance_m"] = dist

# 8. the offset applied twice: Element84's harmonised DNs read with Element84's own declared raster:bands offset
it = e84(E84_S2A) or {}
rb = (it.get("red_raster_bands") or [{}])[0]
ccommit = next(f for f in e84c["features"] if f["id"] == E84_S2A)["assets"]["red"]["raster:bands"][0]
v_dbl = ndvi_refl(eb8, eb4, rb["scale"], rb["offset"]) if (eb8 is not None and rb) else \
    ndvi_refl(2502, 900, ccommit["scale"], ccommit["offset"]) if OFFLINE else None
add("double", "E8.double", "offset applied twice", v_dbl if v_dbl is not None else float("nan"), "hollow", "range",
    "L2", decide(v_dbl) if v_dbl is not None else None, [
        {"kind": "live", "source": f"Element84 {E84_S2A} item + COG", "DN_B08_B04": [eb8, eb4],
         "raster_bands": rb, "boa_offset_applied": it.get("boa_offset_applied")},
        {"kind": "committed", "file": "research/v13/evidence/failure_modes/e84_keylong.json",
         "pointer": f"{E84_S2A} assets.red raster:bands", "value": ccommit, "equal_live": ccommit == rb or OFFLINE}],
    rederived=v_dbl is not None and (OFFLINE or ccommit == rb))

ok = all(r["rederived"] for r in rows)
summary = {
    "crosses_rule": sum(1 for r in rows if r["decision"] == "irrigate"),
    "impossible": sum(1 for r in rows if r["decision"] == "invalid"),
    "right": sum(1 for r in rows if r["key"] == "right"),
}
for r in LIVE["mpc_items"].values():
    r.pop("_sas", None)
out = {
    "generated_by": "research/repro/v13/eight_answers.py",
    "generated_utc": now(),
    "mode": "offline" if OFFLINE else "live",
    "question": {"cell": R1.QUESTION["cell"], "band": R1.QUESTION["band"], "tslot": TSLOT, "date": QDATE,
                 "point": [LAT, LNG], "token": TOKEN},
    "rule": {"text": mm["meta"]["rule"], "threshold": RULE, "status": "constructed test rule (pre-registered)"},
    "all_rederived": ok,
    "summary": summary,
    "answers": rows,
    "live": LIVE,
}
OUT.write_text(json.dumps(out, indent=1, default=float) + "\n")
for r in rows:
    print(f"{r['key']:10s} {r['print']:>7s}  {r['decision']:9s} rederived={r['rederived']}  {r['label']}")
print("summary", summary, "errors", LIVE["errors"])
sys.exit(0 if ok else 2)
