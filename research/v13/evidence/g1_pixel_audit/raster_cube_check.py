"""Task 4: the poster's Fig. 2 raster (B04 + B08, 25 Sep) and the 5 cube members (B08), checked against the upstream COG.
For each emem:raster: token: fetch its signed derivation record (a DerivativeFact whose cid is the token's last segment),
re-hash it, read signed_at, scene, asset, dn_offset, grid; re-hash the artifact bytes; read the SAME window from the
COG at the rows/cols the header names; compare every pixel; check the hero pixel; check the anchors' (row, col).
Then search Planetary Computer STAC for every T43SFS scene over the bbox centre (May-Sep 2026) to test the cube's scene choice.
    python raster_cube_check.py -> raster_cube_check.json
"""
import json, math, struct, pathlib, datetime as dt
import numpy as np
import pa_lib as L

DATA = pathlib.Path("/home/user/esa_poster/research/repro/data")
AOI = "zhiz2prbnvds6ex3cmwbwghlzzdhi6b7nro6h42p3xtamezq5voq"
TOKENS = {
    "fig2_B04": ("emem:raster:%s:s2.B04:20721:4wmvv7i6bv4hjqp6lqbja3zjts53xlwlzwttzbpozt4eetukd2oq" % AOI, "keylong_B04.bin"),
    "cube_20614": ("emem:raster:%s:s2.B08:20614:trwmzekmb3mik54gzlz7nsz5564d47evozybaaeslva7w372xjyq" % AOI, "cube_20614.bin"),
    "cube_20634": ("emem:raster:%s:s2.B08:20634:trnlv376gkscbsmgyrxzlznrl23wyup72cfj244ec7cv4kshrosa" % AOI, "cube_20634.bin"),
    "cube_20668": ("emem:raster:%s:s2.B08:20668:3k344xokwvghqe6yhnfpd5pmrph4gjiny72jc45ko4o335tcrokq" % AOI, "cube_20668.bin"),
    "cube_20709": ("emem:raster:%s:s2.B08:20709:bvlsgt4xotztaohigck6lx6zxefmgu4genxacph2qnrjkqob745a" % AOI, "cube_20709.bin"),
    "cube_20721 (= Fig. 2 B08)": ("emem:raster:%s:s2.B08:20721:74n3alcksp4pxpljv4qldxywxykrepezhysblvw5t7ccbiw3yeeq" % AOI, "cube_20721.bin"),
}
CUBE_DCID = "7ath7qdwqbagvs6kojf7pquay5faj2wahytearzkpsrk7e4sufsa"
HERO = dict(cell="defi.zb572.xoso.zb1ec", E=None, N=None)
lat, lng, _, _ = L.cell64_decode(HERO["cell"])
HERO["E"], HERO["N"] = L.utm(lat, lng, 43)
out = {"PIXEL_FIX_AT": L.PIXEL_FIX_AT, "rasters": {}}


def grid(b):
    assert b[:8] == b"EMEMGRD1"
    w, h, epsg = struct.unpack_from("<III", b, 8); lat0, lng0, dlat, dlng = struct.unpack_from("<dddd", b, 24)
    return w, h, epsg, lat0, lng0, dlat, dlng, np.frombuffer(b, "<f4", offset=64).reshape(h, w)


for name, (tok, fn) in TOKENS.items():
    dcid = tok.split(":")[-1]
    f, raw, ok = L.fetch_fact(dcid)
    v = f["value"]; src = v["sources"][0]; g = v["artifact"]["grid"]
    b = (DATA / fn).read_bytes(); art_ok = L.b32(L.blake3.blake3(b).digest()) == v["artifact"]["artifact_cid"]
    w, h, epsg, y0, x0, dy, dx, A = grid(b)
    c = L.COG.open(src["asset"])
    col0 = (x0 - c.x0) / c.sx - 0.5; row0 = (c.y0 - y0) / c.sy - 0.5  # header names the FIRST PIXEL CENTRE
    assert col0 == int(col0) and row0 == int(row0)
    col0, row0 = int(col0), int(row0)
    win = np.array(c.window(row0, col0, h, w), dtype=float)
    off = src.get("dn_offset", 0.0)
    exp = np.where(win == 0, np.nan, win + off)  # DN 0 = nodata
    eq = np.sum((A == exp) | (np.isnan(A) & np.isnan(exp)))
    # discriminating power: the same comparison against the window one row south / one col east
    win_s = np.array(c.window(row0 + 1, col0, h, w), dtype=float) + off
    eq_s = int(np.sum(A == win_s))
    # hero pixel
    hc = (HERO["E"] - (x0 - 0.5 * dx)) / dx; hr = ((y0 + 0.5 * abs(dy)) - HERO["N"]) / abs(dy)
    hpx = (math.floor(hr), math.floor(hc))
    # anchors: does the (row, col) each anchor names contain its cell's centre?
    anc = []
    for a in v.get("anchors", []):
        la, ln, _, _ = L.cell64_decode(a["cell"]); E, N = L.utm(la, ln, 43)
        fc = (E - (x0 - 0.5 * dx)) / dx; fr = ((y0 + 0.5 * abs(dy)) - N) / abs(dy)
        anc.append(dict(cell=a["cell"], named=(a["row"], a["col"]), floor=(math.floor(fr), math.floor(fc)), round=(L.math.floor(fr + .5), L.math.floor(fc + .5)),
                        value=a["value"], raster_at_named=float(A[a["row"], a["col"]]), fact_cid=a["fact_cid"]))
    rec = dict(token=tok, derivation_cid_ok=ok, signed_at=f["signed_at"], signed_after_fix=f["signed_at"] >= L.PIXEL_FIX_AT,
               scene=src["id"], asset=src["asset"], captured_at=src["captured_at"], dn_offset=off, artifact_cid=v["artifact"]["artifact_cid"], artifact_rehash_ok=art_ok,
               header=dict(w=w, h=h, epsg=epsg, x0=x0, y0=y0, dx=dx, dy=dy), record_grid=g, cog_rows=[row0, row0 + h - 1], cog_cols=[col0, col0 + w - 1],
               pixels_equal=int(eq), pixels_total=int(w * h), nan_in_artifact=int(np.isnan(A).sum()),
               pixels_equal_if_shifted_1_row_south=eq_s,
               hero_point_raster_frac=(hr, hc), hero_pixel=hpx, hero_value=float(A[hpx]), hero_cog_dn=float(win[hpx]), anchors=anc)
    out["rasters"][name] = rec
    print(f"{name:26s} signed {f['signed_at']} post-fix={rec['signed_after_fix']} scene {src['id'][:44]} art_ok={art_ok} rec_ok={ok} "
          f"COG rows {row0}..{row0+h-1} cols {col0}..{col0+w-1}: equal {eq}/{w*h} (1-row shift: {eq_s}); hero px {hpx} = {A[hpx]:.0f} (COG DN {win[hpx]:.0f}, off {off})", flush=True)
    for a in anc: print("    anchor", a["cell"], "named", a["named"], "floor", a["floor"], "round", a["round"], "value", a["value"], "raster", a["raster_at_named"])

# cube derivation
f, raw, ok = L.fetch_fact(CUBE_DCID)
out["cube"] = dict(derivation_cid=CUBE_DCID, rehash_ok=ok, signed_at=f["signed_at"], members=[(m["tslot"], m["scene_id"], m["requested_dates"], m["requested_date_distance_days"]) for m in f["value"]["members"]])
print("cube derivation", CUBE_DCID[:10], "signed", f["signed_at"], "rehash", ok)

# STAC: every scene over the bbox centre, May..Sep 2026, on Planetary Computer
clat, clng = (32.55 + 32.59) / 2, (77.01 + 77.058) / 2
body = {"collections": ["sentinel-2-l2a"], "intersects": {"type": "Point", "coordinates": [clng, clat]},
        "datetime": "2026-04-10T00:00:00Z/2026-09-30T00:00:00Z", "limit": 200, "sortby": [{"field": "properties.datetime", "direction": "desc"}]}
s, h_, bb = L.http("https://planetarycomputer.microsoft.com/api/stac/v1/search", data=body)
items = json.loads(bb)["features"]
scenes = sorted([(it["properties"]["datetime"][:10], it["id"], it["properties"].get("eo:cloud_cover"), it["properties"].get("s2:mgrs_tile")) for it in items])
out["stac_scenes"] = scenes
print(len(scenes), "PC scenes over the bbox centre:")
for sc in scenes: print("   ", sc)
# the rule the code implements (lib.rs:51452 s2_search_with_fallback -> stac.rs sortby datetime desc, take 1):
# the LATEST scene under 40 % cloud in [target-30 d, min(target+30 d, now)], vs the nearest one the doc (band_raster.rs:1709) states
mint = dt.datetime(2026, 9, 29, 22, 5)
res = []
for req in ["2026-05-15", "2026-06-15", "2026-07-15", "2026-08-15", "2026-09-15"]:
    t = dt.datetime.fromisoformat(req) + dt.timedelta(hours=12)
    lo, hi = t - dt.timedelta(days=30), min(t + dt.timedelta(days=30), mint)
    cand = [sc for sc in scenes if lo <= dt.datetime.fromisoformat(sc[0]) + dt.timedelta(hours=5) <= hi and sc[2] is not None and sc[2] < 40]
    latest = max(cand, key=lambda sc: sc[0]) if cand else None
    nearest = min(cand, key=lambda sc: abs((dt.datetime.fromisoformat(sc[0]) - t.replace(hour=0)).days)) if cand else None
    res.append(dict(requested=req, latest_under40=latest, nearest_under40=nearest))
    print(req, "latest<40%:", latest, "| nearest<40%:", nearest)
out["scene_rule"] = res
json.dump(out, open("raster_cube_check.json", "w"), indent=1, default=str)
print("bytes", L.BYTES)
