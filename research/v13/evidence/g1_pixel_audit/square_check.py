"""Where is the square in poster/fig/keylong_ndvi.png, relative to the pixel that holds the NDVI fact?
Rebuilds the figure's axes exactly as poster/make_figures.py:36-46 does (no file written), maps data coords to PNG
pixels, and locates the drawn square (#1F4FD8) in the shipped PNG."""
import struct, pathlib, json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import pa_lib as L
DATA = pathlib.Path("/home/user/esa_poster/research/repro/data"); PNG = "/home/user/esa_poster/poster/fig/keylong_ndvi.png"
def grid(p):
    raw = (DATA / p).read_bytes(); w, h = struct.unpack_from("<II", raw, 8); return np.frombuffer(raw, "<f4", offset=64).reshape(h, w).astype(float)
R, N = grid("keylong_B04.bin"), grid("keylong_B08.bin")
ndvi = (N - R) / (N + R)
fig, ax = plt.subplots(figsize=(3.2, 3.27), dpi=300)
im = ax.imshow(ndvi, cmap="Greens", vmin=0.05, vmax=0.8, interpolation="nearest"); ax.set_axis_off()
fx, fy = (77.03448 - 77.01) / 0.048 * ndvi.shape[1], (32.59 - 32.57126) / 0.04 * ndvi.shape[0]   # make_figures.py:42
cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=.05, pad=.02, extend="min")
fig.subplots_adjust(.02, .12, .98, 1); fig.canvas.draw()
Hpx = fig.get_size_inches()[1] * fig.dpi
def to_png(x, y):
    X, Y = ax.transData.transform((x, y)); return X, Hpx - Y
lat, lng, _, _ = L.cell64_decode("defi.zb572.xoso.zb1ec"); E, Nn = L.utm(lat, lng, 43)
pt = ((E - 688735.0) / 10.0, (3607705.0 - Nn) / 10.0)      # data coords: pixel (r, c) centre is at (c, r)
hero = (225, 212)
img = np.asarray(Image.open(PNG).convert("RGB")).astype(int)
blue = np.argwhere((abs(img[..., 0] - 0x1F) < 40) & (abs(img[..., 1] - 0x4F) < 40) & (abs(img[..., 2] - 0xD8) < 40))
r0, c0 = blue.min(0); r1, c1 = blue.max(0)
sq_png = ((c0 + c1) / 2, (r0 + r1) / 2)
inv = ax.transData.inverted()
sq_data = inv.transform((sq_png[0], Hpx - sq_png[1]))
px_per_data = to_png(1, 0)[0] - to_png(0, 0)[0]
out = dict(png_size=img.shape[:2], square_png_bbox=[int(c0), int(r0), int(c1), int(r1)], square_png_centre=sq_png, square_centre_in_raster_coords=list(map(float, sq_data)),
           square_centre_intended_by_code=(fx, fy), square_pixel_rc=(int(np.floor(sq_data[1] + .5)), int(np.floor(sq_data[0] + .5))),
           fact_point_raster_coords=pt, fact_pixel_rc=(212, 225), offset_data_px=(float(sq_data[0] - pt[0]), float(sq_data[1] - pt[1])),
           offset_m_east_south=(float(sq_data[0] - pt[0]) * 10, float(sq_data[1] - pt[1]) * 10), png_px_per_raster_px=px_per_data,
           ndvi_at_fact_pixel=float(ndvi[212, 225]), ndvi_at_square_pixel=float(ndvi[int(np.floor(sq_data[1] + .5)), int(np.floor(sq_data[0] + .5))]),
           nodata_pixel_335_401=dict(B04=float(R[335, 401]), B08=float(N[335, 401]), ndvi=float(ndvi[335, 401])))
print(json.dumps(out, indent=1)); json.dump(out, open("square_check.json", "w"), indent=1)
