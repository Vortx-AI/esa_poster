"""pa_lib.py - independent helpers for the emem pixel audit (no emem code imported).

Dependencies: stdlib, blake3, cbor2 (pyproj only as a cross-check).
 - fetch_fact(cid): GET https://emem.dev/v1/facts/<cid> as CBOR, re-hash with BLAKE3-256,
   base32-nopad-lower, compare to the cid, decode.
 - utm(lat, lng, zone): WGS84 -> UTM north (Krueger n^4 series).
 - COG(url).window(r0, c0, h, w): range-read only the tiles (and only the
   deflate prefix of each tile) that cover the window; own TIFF 6.0 / GeoTIFF parser,
   Predictor 2 undone per row.
 - BYTES: running count of every HTTP body byte read from upstream COG hosts.
"""
import base64, json, math, struct, threading, time, urllib.request, urllib.error, zlib
import blake3, cbor2

EMEM = "https://emem.dev"
PC_SAS = "https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-2-l2a"
PIXEL_FIX_AT = "2026-09-28T04:09:26Z"          # crates/emem-api-rest/src/lib.rs:12651
BYTES = {"cog": 0, "cog_requests": 0, "emem": 0}
_lock = threading.Lock()


def http(url, data=None, headers=None, rng=None, tries=4, timeout=90, kind="emem"):
    h = dict(headers or {})
    if rng: h["Range"] = f"bytes={rng[0]}-{rng[1]}"
    if data is not None and not isinstance(data, bytes):
        data = json.dumps(data).encode(); h.setdefault("content-type", "application/json")
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                with _lock:
                    BYTES[kind] += len(body)
                    if kind == "cog": BYTES["cog_requests"] += 1
                return r.status, dict(r.headers), body
        except urllib.error.HTTPError as e:
            body = e.read()
            if e.code in (403, 404, 409, 400) and k >= 1: return e.code, dict(e.headers), body
            last = e
        except Exception as e:
            last = e
        time.sleep(1.5 * (k + 1))
    raise RuntimeError(f"{url[:120]}: {last!r}")


def b32(d): return base64.b32encode(d).decode().lower().rstrip("=")


def fetch_fact(cid):
    s, h, b = http(f"{EMEM}/v1/facts/{cid}", headers={"Accept": "application/cbor"})
    if s != 200: return None, b, False
    ok = b32(blake3.blake3(b).digest()) == cid
    return cbor2.loads(b), b, ok


# ---------------------------------------------------------------- cell64 (emem grid, docs/protocol + emem-codec geo.rs semantics)
CONS, VOWS = "bcdfghjklmnpqrstvwxyz", "aeiouAEIOU"
_ALPHA = [c1 + v1 + c2 + v2 for c1 in CONS for v1 in VOWS for c2 in CONS for v2 in VOWS]
while len(_ALPHA) < 65536: _ALPHA.append("z%04x" % len(_ALPHA))
_IDX = {w: k for k, w in enumerate(_ALPHA)}
LATM, LNGM = (1 << 21) - 1, (1 << 22) - 1


def cell64_decode(s):
    """-> (lat_centre, lng_centre, half_dlat_deg, half_dlng_deg). The encoder rounds
    (lat+90)/180*LATM to an integer, so a cell is the +-0.5 quantum around its centre."""
    raw = 0
    for k, sym in enumerate(s.split(".")): raw |= _IDX[sym] << (48 - 16 * k)
    prefix = (1 << 60) | (21 << 52) | (0xAB << 44)
    assert raw & 0xFFFFF00000000000 == prefix, "not a geo cell"
    lat_q = (raw >> 22) & LATM; lng_q = raw & LNGM
    return lat_q / LATM * 180.0 - 90.0, lng_q / LNGM * 360.0 - 180.0, 90.0 / LATM, 180.0 / LNGM


# ---------------------------------------------------------------- WGS84 -> UTM north
def utm(lat, lng, zone):
    a, f = 6378137.0, 1 / 298.257223563; k0 = 0.9996; n = f / (2 - f)
    A = a / (1 + n) * (1 + n**2 / 4 + n**4 / 64)
    al = [None, n/2 - 2*n**2/3 + 5*n**3/16 + 41*n**4/180, 13*n**2/48 - 3*n**3/5 + 557*n**4/1440,
          61*n**3/240 - 103*n**4/140, 49561*n**4/161280]
    phi, lam = math.radians(lat), math.radians(lng - (zone * 6 - 183))
    c = 2 * math.sqrt(n) / (1 + n)
    t = math.sinh(math.atanh(math.sin(phi)) - c * math.atanh(c * math.sin(phi)))
    xi = math.atan2(t, math.cos(lam)); eta = math.atanh(math.sin(lam) / math.sqrt(1 + t * t))
    E = 500000 + k0 * A * (eta + sum(al[j] * math.cos(2*j*xi) * math.sinh(2*j*eta) for j in range(1, 5)))
    N = k0 * A * (xi + sum(al[j] * math.sin(2*j*xi) * math.cosh(2*j*eta) for j in range(1, 5)))
    return E, N


# ---------------------------------------------------------------- PC SAS token
_sas = {"tok": None, "t": 0}


def pc_token(force=False):
    if force or _sas["tok"] is None or time.time() - _sas["t"] > 1800:
        s, h, b = http(PC_SAS)
        _sas["tok"] = json.loads(b)["token"]; _sas["t"] = time.time()
    return _sas["tok"]


def signed_url(u):
    if "blob.core.windows.net" in u: return u + "?" + pc_token()
    return u


# ---------------------------------------------------------------- minimal COG reader
class COG:
    TYPES = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 7: 1, 11: 4, 12: 8, 16: 8}
    FMT = {1: "B", 3: "H", 4: "I", 12: "d", 16: "Q", 11: "f", 7: "B"}
    _cache = {}

    _olock = threading.Lock()
    _ulocks = {}

    @classmethod
    def open(cls, url):
        with cls._olock:
            lk = cls._ulocks.setdefault(url, threading.Lock())
        with lk:
            if url not in cls._cache: cls._cache[url] = cls(url)
            return cls._cache[url]

    def __init__(self, url):
        self.url = url; self.tiles = {}
        self.head = self.read(0, 32767)
        self.e = "<" if self.head[:2] == b"II" else ">"
        self.big = struct.unpack(self.e + "H", self.head[2:4])[0] == 43
        off = struct.unpack(self.e + ("Q" if self.big else "I"), self.head[8:16] if self.big else self.head[4:8])[0]
        t = self.tags = self.ifd(off)
        self.W, self.H = t[256][0], t[257][0]; self.bps = t[258][0]; self.comp = t[259][0]
        self.pred = t.get(317, [1])[0]; self.tw, self.th = t[322][0], t[323][0]
        self.sx, self.sy = t[33550][0], t[33550][1]; tp = t[33922]
        self.i0, self.j0, self.x0, self.y0 = tp[0], tp[1], tp[3], tp[4]
        gk = t.get(34735, []); self.raster_type = 1
        for k in range(4, len(gk), 4):
            if gk[k] == 1025: self.raster_type = gk[k + 3]
        self.tcols = (self.W + self.tw - 1) // self.tw

    def read(self, a, b):
        u = signed_url(self.url)
        s, h, body = http(u, rng=(a, b), kind="cog")
        if s == 403 and "blob.core" in self.url:
            pc_token(force=True); s, h, body = http(signed_url(self.url), rng=(a, b), kind="cog")
        assert s == 206, f"range read status {s} {self.url[:100]}"
        return body

    def bytes_at(self, off, n):
        if off + n <= len(self.head): return self.head[off:off + n]
        return self.read(off, off + n - 1)

    def ifd(self, off):
        e = self.e
        if self.big: cnt = struct.unpack(e + "Q", self.bytes_at(off, 8))[0]; esz, base = 20, off + 8
        else: cnt = struct.unpack(e + "H", self.bytes_at(off, 2))[0]; esz, base = 12, off + 2
        raw = self.bytes_at(base, cnt * esz); tags = {}
        for k in range(cnt):
            ent = raw[k * esz:(k + 1) * esz]
            if self.big: tag, typ, n = struct.unpack(e + "HHQ", ent[:12]); vb = ent[12:20]; inl = 8
            else: tag, typ, n = struct.unpack(e + "HHI", ent[:8]); vb = ent[8:12]; inl = 4
            size = self.TYPES.get(typ, 1) * n
            data = vb[:size] if size <= inl else self.bytes_at(struct.unpack(e + ("Q" if self.big else "I"), vb)[0], size)
            if typ == 2: tags[tag] = data.rstrip(b"\x00").decode(errors="replace")
            elif typ == 5: tags[tag] = [a / b for a, b in zip(*[iter(struct.unpack(e + "I" * 2 * n, data))] * 2)]
            else: tags[tag] = list(struct.unpack(e + self.FMT.get(typ, "B") * n, data))
        return tags

    def frac(self, E, N):
        """fractional (col, row) of a world point; pixel k spans [k, k+1) on a PixelIsArea raster"""
        return self.i0 + (E - self.x0) / self.sx, self.j0 + (self.y0 - N) / self.sy

    def _tile_rows(self, ti, need_rows):
        """decoded rows [0, need_rows) of tile ti, reading only the deflate prefix needed"""
        have = self.tiles.get(ti)
        if have is not None and len(have) >= need_rows: return have
        off, cnt = self.tags[324][ti], self.tags[325][ti]
        assert self.comp in (8, 32946), f"compression {self.comp}"
        rb = (self.tw * self.bps + 7) // 8
        want = need_rows * rb
        d = zlib.decompressobj(); out = b""; pos = 0
        chunk = max(65536, int(cnt * min(1.0, (need_rows + 8) / self.th)) + 16384)
        while len(out) < want and pos < cnt:
            n = min(chunk, cnt - pos)
            out += d.decompress(self.read(off + pos, off + pos + n - 1)); pos += n
            chunk = 131072
        rows = []
        for r in range(min(need_rows, len(out) // rb)):
            rowb = out[r * rb:(r + 1) * rb]
            if self.bps == 16: v = list(struct.unpack(self.e + "H" * self.tw, rowb))
            elif self.bps == 8: v = list(rowb)
            else:
                big = int.from_bytes(rowb, "big"); tot = rb * 8; m = (1 << self.bps) - 1
                v = [(big >> (tot - (c + 1) * self.bps)) & m for c in range(self.tw)]
            if self.pred == 2:
                acc, m = 0, (1 << self.bps) - 1
                for c in range(self.tw): acc = (acc + v[c]) & m; v[c] = acc
            rows.append(v)
        self.tiles[ti] = rows
        return rows

    def window(self, r0, c0, h, w):
        """h x w grid of raw DNs with top-left image pixel (r0, c0); None outside the image"""
        g = [[None] * w for _ in range(h)]
        for rr in range(h):
            r = r0 + rr
            if not 0 <= r < self.H: continue
            for cc in range(w):
                c = c0 + cc
                if not 0 <= c < self.W: continue
                ti = (r // self.th) * self.tcols + (c // self.tw)
                rows = self._tile_rows(ti, (max(r0 + h - 1, r) % self.th if (r0 + h - 1) // self.th == r // self.th else self.th - 1) + 1)
                g[rr][cc] = rows[r % self.th][c % self.tw]
        return g
