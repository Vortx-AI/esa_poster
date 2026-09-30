---
after: sth 2566400 zpmln3ntpmqeb6dcj3s4cndtd53w3yva623dpcjb4qfczgxuqwha 2026-09-30T12:56:23Z
emem: pointer.v1
spec: mlxrdcys43hao7cz554s46bp7a
source: https://raw.githubusercontent.com/Vortx-AI/emem/213e2738d508a4e084cd0beef329598950f01bf0/CHANGELOG.md
bytes: 169723
etag: not exposed
kind: text (line ranges)
chunks: 1 of 2532 lines hashed
root: zxeg52sjy4brrwrbta22kgwjb4hreeiw4xeganlfjpaqckxo3o2q
hash: blake3-256 of each chunk's bytes
order: as cited
---

# CHANGELOG.md at Vortx-AI/emem 213e273

> the pixel-rounding fix. The file stays on GitHub at a pinned commit; each row below names exact bytes of it, which anyone can range-read and hash. Cited by the EMEM poster at Agentic AI for Earth Observation, Berlin, 19 Oct 2026.

### lines 68–68

> - Raster point reads take the pixel that contains the point. `cog::world_to_pixel` rounded the fractional pixel position, so any point in the right or lower half of a pixel read its south-east neighbour; GDAL takes the floor. Every COG-backed band (Hansen, JRC GFC2020 and TMF, WorldCover, Cop-DEM, CCI biomass, Sentinel scenes, and the hand-rolled DMSP-OLS and Köppen readers) did this from the first commit. The fn_keys are unchanged because their registry definition was always "the pixel at (lat, lng)"; facts signed before this release may carry the neighbouring pixel. PixelIsPoint rasters (GTRasterTypeGeoKey 2) still round, which is correct for them.

## Chunks

| what | url (· is the source) | offset | length | blake3 | stats |
|---|---|---|---|---|---|
| line 68 · point reads took the south-east neighbour from the first commit; fixed | · | 15749 | 660 | yycm4omlglprrkpo5wc6qoqv5zgopvb4tfs6x2vdpl26hft74hga |  |
