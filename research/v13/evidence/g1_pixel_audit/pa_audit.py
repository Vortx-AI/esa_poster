"""pa_audit.py - audit one signed emem Sentinel-2 point fact against the upstream COG pixels.

For each asset the fact read (sources[0].id, ' ; '-joined), project the fact's own
(lat, lng) (derivation.args[0:2]) to the scene's UTM zone (args[3]), and read:
  floor pixel  (floor(col_f), floor(row_f))  = the pixel that CONTAINS the point (PixelIsArea)
  round pixel  (round(col_f), round(row_f))  = emem's pre-fix rule (cog.rs:130-135, "every point
               sampler here did that from the first commit until 2026-09-28")
  a 5x5 window centred on the floor pixel.
Compare the signed DNs (args[5]) and signed SCL (args[9]) with both. No emem code is used.
"""
import math
import pa_lib as L

FIX = L.PIXEL_FIX_AT


def rnd(x): return math.floor(x + 0.5)  # Rust f64::round (half away from zero) for x > 0


def refl(dn, off): return (dn + off) * 1e-4


def nd(a, b): return (a - b) / (a + b) if abs(a + b) > 1e-12 else float("nan")


def value_from(band, dns, off):
    r = [refl(d, off) for d in dns]
    if band == "s2.scl": return float(dns[0])
    if band.startswith("s2.B"): return r[0]
    if band in ("indices.ndvi", "indices.ndwi", "indices.mndwi", "indices.nbr", "indices.ndmi", "indices.ndbi",
                "indices.ndti", "indices.gndvi", "indices.ndre", "indices.ndsi"): return nd(r[0], r[1])
    if band == "indices.savi": return 1.5 * (r[0] - r[1]) / (r[0] + r[1] + 0.5)
    if band == "indices.savi_l1": return 2.0 * (r[0] - r[1]) / (r[0] + r[1] + 1.0)
    if band == "indices.evi": return 2.5 * (r[0] - r[1]) / (r[0] + 6 * r[1] - 7.5 * r[2] + 1.0)
    if band == "indices.afri1600": return (r[0] - 0.66 * r[1]) / (r[0] + 0.66 * r[1])
    if band == "indices.bsi": return ((r[0] + r[1]) - (r[2] + r[3])) / ((r[0] + r[1]) + (r[2] + r[3]))
    if band == "indices.surface_dryness": return 1.0 - max(0.0, min(1.0, nd(r[0], r[1])))
    if band == "indices.fai": return r[0] - (r[1] + (842.0 - 665.0) / (1610.0 - 665.0) * (r[2] - r[1]))
    if band == "indices.tss": return max(0.0, 14.464 * (r[0] / r[1]) + 16.336)
    if band in ("indices.urban_canopy", "indices.urban_canopy_index"): return nd(r[0], r[1]) * (1.0 - nd(r[2], r[0]))
    return None


def scl_href(asset_url):
    u = asset_url
    if "sentinel-cogs" in u:  # Element84: .../<item>/B04.tif -> .../<item>/SCL.tif
        return u.rsplit("/", 1)[0] + "/SCL.tif"
    if "blob.core.windows.net" in u:  # PC SAFE layout: IMG_DATA/R10m/T.._B04_10m.tif -> IMG_DATA/R20m/T.._SCL_20m.tif
        head, fn = u.split("/IMG_DATA/")
        stem = fn.split("/", 1)[1]
        stem = "_".join(stem.split("_")[:2])
        return f"{head}/IMG_DATA/R20m/{stem}_SCL_20m.tif"
    return None


def provider(u):
    return "PC" if "blob.core.windows.net" in u else ("E84" if "sentinel-cogs" in u else "other")


def audit(f, want_window=True):
    a = f["derivation"]["args"]
    band = f["band"]
    lat, lng, scene, epsg = a[0], a[1], a[2], a[3]
    dns = [float(x) for x in a[5]]
    scl_signed = a[9] if len(a) > 9 else None
    off = a[12] if len(a) > 12 and isinstance(a[12], float) else 0.0
    stamp = [x for x in a if isinstance(x, str) and x.startswith("reader=")]
    urls = f["sources"][0]["id"].split(" ; ")
    zone = epsg % 100
    assert epsg // 100 in (326, 327), f"epsg {epsg} is not WGS84 UTM"
    E, N = L.utm(lat, lng, zone)
    if epsg // 100 == 327: N += 10_000_000.0  # UTM south false northing
    per = []
    for u in urls:
        c = L.COG.open(u)
        cf, rf = c.frac(E, N)
        fc, fr = math.floor(cf), math.floor(rf)
        rc, rr = rnd(cf), rnd(rf)
        w = c.window(fr - 2, fc - 2, 5, 5)
        per.append(dict(url=u, cf=cf, rf=rf, floor=(fr, fc), round=(rr, rc), win=w, res=c.sx,
                        v_floor=w[2][2], v_round=w[2 + rr - fr][2 + rc - fc], rt=c.raster_type))
    floor_dns = [p["v_floor"] for p in per]
    round_dns = [p["v_round"] for p in per]
    same_px = all(p["floor"] == p["round"] for p in per)
    m_floor = [float(x) for x in floor_dns] == dns
    m_round = [float(x) for x in round_dns] == dns
    other = []
    if not (m_floor or m_round):
        for i in range(5):
            for j in range(5):
                if [float(p["win"][i][j]) for p in per] == dns: other.append((i - 2, j - 2))
    if same_px and m_floor: cls = "floor=round"  # both rules pick the same pixel
    elif m_floor and m_round: cls = "both(equal DNs)"
    elif m_floor: cls = "matches-floor"
    elif m_round: cls = "matches-round"
    elif other: cls = "matches-other"
    else: cls = "no-match"
    # SCL at floor/round (20 m grid)
    scl_floor = scl_round = None
    try:
        su = scl_href(urls[0]) if band != "s2.scl" else urls[0]
        if su:
            sc = L.COG.open(su); cf, rf = sc.frac(E, N)
            fr, fc, rr, rc = math.floor(rf), math.floor(cf), rnd(rf), rnd(cf)
            sw = sc.window(fr, fc, 2, 2)
            scl_floor = sw[0][0]; scl_round = sw[rr - fr][rc - fc]
    except Exception as e:
        scl_floor = f"err:{e!r}"[:60]
    rec = dict(
        cid=None, band=band, tslot=f["tslot"], cell=f["cell"],
        capture_date=(f["sources"][0].get("captured_at") or "")[:10], scene=scene, provider=provider(urls[0]),
        signed_at=f["signed_at"], prefix_bool=f["signed_at"] < FIX,
        signed_value=f["value"], signed_dns=dns, floor_dns=floor_dns, round_dns=round_dns,
        dn_offset=off, recomputed_signed=value_from(band, dns, off),
        floor_value=value_from(band, floor_dns, off), round_value=value_from(band, round_dns, off),
        match_class=cls, other_offsets=other, scl_signed=scl_signed, scl_floor=scl_floor, scl_round=scl_round,
        col_frac=per[0]["cf"] % 1, row_frac=per[0]["rf"] % 1, E=E, N=N,
        floor_px=per[0]["floor"], round_px=per[0]["round"], reader_stamp=stamp[0] if stamp else "",
        fn_key=f["derivation"]["fn_key"], n_assets=len(urls), asset_res=[p["res"] for p in per],
        raster_type=per[0]["rt"], lat=lat, lng=lng, urls=urls,
    )
    if want_window: rec["windows"] = {u.rsplit("/", 1)[-1]: p["win"] for u, p in zip(urls, per)}
    return rec
