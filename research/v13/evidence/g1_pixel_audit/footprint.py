"""Settle the cell64 footprint of defi.zb572.xoso.zb1ec: geodesic N-S / E-W extent (WGS84, pyproj.Geod)
and the footprint's corners in the scene's UTM 43N grid (own projection, pyproj cross-check)."""
import json, math, pyproj
import pa_lib as L
cell = "defi.zb572.xoso.zb1ec"
lat, lng, hlat, hlng = L.cell64_decode(cell)
g = pyproj.Geod(ellps="WGS84")
_, _, ns = g.inv(lng, lat - hlat, lng, lat + hlat)
_, _, ew = g.inv(lng - hlng, lat, lng + hlng, lat)
_, _, ew_s = g.inv(lng - hlng, lat - hlat, lng + hlng, lat - hlat)
_, _, ew_n = g.inv(lng - hlng, lat + hlat, lng + hlng, lat + hlat)
tr = pyproj.Transformer.from_crs(4326, 32643, always_xy=True)
corners = [(lat + hlat, lng - hlng), (lat + hlat, lng + hlng), (lat - hlat, lng + hlng), (lat - hlat, lng - hlng)]
utmc = [L.utm(a, b, 43) for a, b in corners]
utmc_p = [tr.transform(b, a) for a, b in corners]
E, N = L.utm(lat, lng, 43)
# grid convergence and point scale factor at the point (pyproj Factors)
fac = pyproj.Proj("EPSG:32643").get_factors(lng, lat)
ns_grid = math.dist(utmc[1], utmc[2]); ew_grid = math.dist(utmc[0], utmc[1])
out = dict(cell=cell, centre_lat=lat, centre_lng=lng, dlat_deg=2 * hlat, dlng_deg=2 * hlng,
           ns_geodesic_m=ns, ew_geodesic_m_centre=ew, ew_geodesic_m_south=ew_s, ew_geodesic_m_north=ew_n,
           area_m2=ns * ew, utm43n_centre=(E, N), utm43n_corners_NW_NE_SE_SW=utmc, utm_pyproj_max_diff_m=max(math.dist(a, b) for a, b in zip(utmc, utmc_p)),
           ns_grid_m=ns_grid, ew_grid_m=ew_grid, meridian_convergence_deg=fac.meridian_convergence, point_scale=fac.meridional_scale,
           centre_col_frac=(E - 600000) / 10, centre_row_frac=(3700020 - N) / 10)
print(json.dumps(out, indent=1)); json.dump(out, open("footprint.json", "w"), indent=1)
