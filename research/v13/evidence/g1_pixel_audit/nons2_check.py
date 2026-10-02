"""Extra: the non-Sentinel-2 GeoTIFF point facts at the hero cell (Copernicus DEM, JRC GSW), read with GDAL/rasterio
at the containing (floor) and rounded pixel. Cross-check only; rasterio is GDAL, not emem."""
import math, rasterio
lat, lng = 32.57125977099409, 77.03447748052537
for name, u, signed in [("copdem30m.elevation_mean (signed 2026-07-15T19:37:39Z)", "https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N32_00_E077_00_DEM/Copernicus_DSM_COG_10_N32_00_E077_00_DEM.tif", 3105.4443359375),
                        ("surface_water.recurrence (signed 2026-07-15T21:23:04Z)", "https://storage.googleapis.com/global-surface-water/downloads2021/recurrence/recurrence_70E_40Nv1_4_2021.tif", 0.0)]:
    with rasterio.open("/vsicurl/" + u) as ds:
        t = ds.transform; cf = (lng - t.c) / t.a; rf = (lat - t.f) / t.e
        aop = ds.tags().get("AREA_OR_POINT")
        fr, fc = math.floor(rf), math.floor(cf); w = ds.read(1, window=((fr - 1, fr + 2), (fc - 1, fc + 2)))
        rr, rc = math.floor(rf + .5), math.floor(cf + .5)
        print(name, "| AREA_OR_POINT", aop, "| col_f %.4f row_f %.4f" % (cf, rf), "| floor", float(w[1][1]), "| round", float(w[1 + rr - fr][1 + rc - fc]), "| signed", signed)
        print("   3x3", w.tolist())
