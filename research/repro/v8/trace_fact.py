#!/usr/bin/env python3
"""trace_fact.py - walk one emem fact token to ground truth, link by link.

Independent of emem code. Dependencies: Python stdlib (urllib, zlib, struct, json),
blake3, cbor2, pynacl. pyproj is used only as an optional cross-check of the
projection this script computes itself.

    pip install blake3 cbor2 pynacl
    python trace_fact.py [token] [--no-pixel] [--no-log] [--out DIR]

Every protocol rule used here is written from the emem spec text
(docs/protocol.md, /v1/verifier_spec, the STH `algorithm` block), RFC 9162,
the TIFF 6.0 / GeoTIFF specs and ESA's Sentinel-2 L2A product definition.
Each link prints VERIFIED, FAILED, or NOT VERIFIABLE with the reason.
"""
import base64, datetime as dt, json, math, os, struct, sys, time, urllib.parse, urllib.request, zlib
import blake3, cbor2
from nacl.signing import VerifyKey

TOKEN = "emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa"
EMEM = "https://emem.dev"
PC_STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
PC_SAS = "https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-2-l2a"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
flags = [a for a in sys.argv[1:] if a.startswith("--")]
if args: TOKEN = args[0]
OUT = next((f.split("=", 1)[1] for f in flags if f.startswith("--out=")), os.path.dirname(os.path.abspath(__file__)))
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- helpers
def http(url, data=None, headers=None, rng=None, tries=3, timeout=90):
    h = dict(headers or {})
    if rng: h["Range"] = f"bytes={rng[0]}-{rng[1]}"
    if data is not None and not isinstance(data, bytes):
        data = json.dumps(data).encode(); h.setdefault("content-type", "application/json")
    for k in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, dict(r.headers), r.read()
        except urllib.error.HTTPError as e:
            return e.code, dict(e.headers), e.read()
        except Exception:
            if k == tries - 1: raise
            time.sleep(2 * (k + 1))
def jget(url, **kw):
    for k in range(5):  # retry rate limits / shed load (429, 503) and transient 5xx
        s, h, b = http(url, **kw)
        if s < 500 and s != 429: return s, json.loads(b)
        time.sleep(float(h.get("retry-after") or h.get("Retry-After") or 2 * (k + 1)))
    return s, json.loads(b)
b32e = lambda b: base64.b32encode(b).decode().lower().rstrip("=")
def b32d(s): return base64.b32decode(s.upper() + "=" * ((8 - len(s) % 8) % 8))
H = lambda b: blake3.blake3(b).digest()
def pre(domain):  # PreimageV1 domain header
    d = domain.encode(); return b"emem.preimage.v1\x00" + struct.pack("<I", len(d)) + d
seg = lambda t, b: bytes([t]) + struct.pack("<I", len(b)) + b
def seglist(t, items):
    return bytes([t]) + struct.pack("<I", len(items)) + b"".join(struct.pack("<I", len(i.encode())) + i.encode() for i in items)
def ed_ok(pk, msg, sig):
    try: VerifyKey(pk).verify(msg, sig); return True
    except Exception: return False
fbits = lambda x: struct.pack(">d", x).hex()

CHAIN = []
def link(n, name, check, ok, evidence, residue=""):
    res = "VERIFIED" if ok is True else ("FAILED" if ok is False else "NOT VERIFIABLE")
    CHAIN.append(dict(n=n, link=name, check=check, result=res, evidence=evidence, trust_residue=residue))
    print(f"\n[{n:>2}] {name}\n     check   : {check}\n     result  : {res}" + (f" ({ok})" if isinstance(ok, str) else ""))
    for line in (evidence if isinstance(evidence, list) else [evidence]):
        print(f"     evidence: {line}")
    if residue: print(f"     residual trust: {residue}")
    return ok is True

# ---------------------------------------------------------------- CBOR raw slicing
def cbor_end(b, i):
    """End offset of the CBOR data item starting at b[i] (RFC 8949 s3)."""
    ib = b[i]; mt, ai = ib >> 5, ib & 31; i += 1
    if ai < 24: val = ai
    elif ai in (24, 25, 26, 27):
        n = 1 << (ai - 24); val = int.from_bytes(b[i:i + n], "big"); i += n
    elif ai == 31: val = None
    else: raise ValueError("reserved ai")
    if mt in (0, 1): return i
    if mt == 7: return i if ai != 31 else i
    if mt in (2, 3):
        if val is not None: return i + val
        while b[i] != 0xFF: i = cbor_end(b, i)
        return i + 1
    if mt == 6: return cbor_end(b, i)
    cnt = val if mt == 4 else (None if val is None else 2 * val)
    if cnt is None:
        while b[i] != 0xFF: i = cbor_end(b, i)
        return i + 1
    for _ in range(cnt): i = cbor_end(b, i)
    return i
def cbor_map_raw(b):
    """Top-level CBOR map -> {key: (start, end)} raw byte spans of each value."""
    ib = b[0]; assert ib >> 5 == 5; ai = ib & 31; i = 1
    if ai < 24: n = ai
    else: k = 1 << (ai - 24); n = int.from_bytes(b[1:1 + k], "big"); i += k
    out = {}
    for _ in range(n):
        ke = cbor_end(b, i); key = cbor2.loads(b[i:ke]); ve = cbor_end(b, ke); out[key] = (ke, ve); i = ve
    return out
def cbor_array_raw(b):
    ib = b[0]; assert ib >> 5 == 4; ai = ib & 31; i = 1
    if ai < 24: n = ai
    else: k = 1 << (ai - 24); n = int.from_bytes(b[1:1 + k], "big"); i += k
    items = []
    for _ in range(n):
        e = cbor_end(b, i); items.append(b[i:e]); i = e
    return items

# ---------------------------------------------------------------- cell64 (emem grid), from the spec
CONS, VOWS = "bcdfghjklmnpqrstvwxyz", "aeiouAEIOU"
def cell64_decode(s):
    alpha = [c1 + v1 + c2 + v2 for c1 in CONS for v1 in VOWS for c2 in CONS for v2 in VOWS]
    while len(alpha) < 65536: alpha.append("z%04x" % len(alpha))
    idx = {w: k for k, w in enumerate(alpha)}
    raw = 0
    for k, sym in enumerate(s.split(".")): raw |= idx[sym] << (48 - 16 * k)
    prefix = (1 << 60) | (21 << 52) | (0xAB << 44)
    assert raw & 0xFFFFF00000000000 == prefix, "not a geo cell"
    LATB, LNGB = 21, 22; LATM, LNGM = (1 << LATB) - 1, (1 << LNGB) - 1
    lat_q = (raw >> LNGB) & LATM; lng_q = raw & LNGM
    lat = (lat_q / LATM) * 180.0 - 90.0; lng = (lng_q / LNGM) * 360.0 - 180.0
    return lat, lng, 90.0 / LATM, 180.0 / LNGM

# ---------------------------------------------------------------- WGS84 -> UTM (Krueger series, n^4)
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

# ---------------------------------------------------------------- minimal COG reader (TIFF 6.0 + GeoTIFF)
class COG:
    TYPES = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 7: 1, 11: 4, 12: 8, 16: 8}
    FMT = {1: "B", 3: "H", 4: "I", 5: "II", 12: "d", 16: "Q", 11: "f", 7: "B", 2: "c"}
    def __init__(self, url):
        self.url = url; self.cache = {}
        self.head = self.read(0, 65535)
        bo = self.head[:2]; self.e = "<" if bo == b"II" else ">"
        magic = struct.unpack(self.e + "H", self.head[2:4])[0]
        self.big = magic == 43
        off = struct.unpack(self.e + ("Q" if self.big else "I"), self.head[8:16] if self.big else self.head[4:8])[0]
        self.tags = self.ifd(off)
    def read(self, a, b):
        s, h, body = http(self.url, rng=(a, b))
        assert s == 206, f"range read status {s}"
        return body
    def bytes_at(self, off, n):
        if off + n <= len(self.head): return self.head[off:off + n]
        return self.read(off, off + n - 1)
    def ifd(self, off):
        e = self.e
        if self.big:
            cnt = struct.unpack(e + "Q", self.bytes_at(off, 8))[0]; esz, base = 20, off + 8
        else:
            cnt = struct.unpack(e + "H", self.bytes_at(off, 2))[0]; esz, base = 12, off + 2
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
    def pixel(self, E, N):
        t = self.tags; W, Hh = t[256][0], t[257][0]; bps = t[258][0]; comp = t[259][0]
        pred = t.get(317, [1])[0]; tw, th = t[322][0], t[323][0]
        sx, sy = t[33550][0], t[33550][1]; tp = t[33922]
        gk = t.get(34735, []); raster_type = 1
        for k in range(4, len(gk), 4):
            if gk[k] == 1025: raster_type = gk[k + 3]
        colf = tp[0] + (E - tp[3]) / sx; rowf = tp[1] + (tp[4] - N) / sy
        if raster_type == 2: col, row = round(colf), round(rowf)
        else: col, row = math.floor(colf), math.floor(rowf)
        tcols = (W + tw - 1) // tw; ti = (row // th) * tcols + (col // tw)
        off, cnt = t[324][ti], t[325][ti]
        comp_bytes = self.read(off, off + cnt - 1)
        assert comp in (8, 32946), f"compression {comp} not handled"
        raw = zlib.decompress(comp_bytes)
        ic, ir = col - (col // tw) * tw, row - (row // th) * th
        rows = {}
        rb = (tw * bps + 7) // 8  # TIFF 6.0: rows start on a byte boundary
        for r in (ir - 1, ir, ir + 1):  # Predictor 2 is per row: undo it only on the rows we read
            if not 0 <= r < th: continue
            rowb = raw[r * rb:(r + 1) * rb]
            if pred == 3:  # floating-point predictor (Adobe TIFF TN3): byte-difference, then byte planes MSB first
                assert bps == 32 and t.get(339, [1])[0] == 3
                b = bytearray(rowb)
                for k in range(1, len(b)): b[k] = (b[k] + b[k - 1]) & 0xFF
                rows[r] = [struct.unpack(">f", bytes((b[c], b[tw + c], b[2 * tw + c], b[3 * tw + c])))[0] for c in range(tw)]
                continue
            if bps == 16: v = list(struct.unpack(self.e + "H" * tw, rowb))
            elif bps == 8: v = list(rowb)
            elif bps == 32 and t.get(339, [1])[0] == 3: v = list(struct.unpack(self.e + "f" * tw, rowb))
            else:  # bit-packed unsigned (e.g. NBITS=15), MSB-first within the row
                big = int.from_bytes(rowb, "big"); tot = rb * 8; m = (1 << bps) - 1
                v = [(big >> (tot - (c + 1) * bps)) & m for c in range(tw)]
            if pred == 2:
                acc, m = 0, (1 << bps) - 1
                for c in range(tw): acc = (acc + v[c]) & m; v[c] = acc
            rows[r] = v
        nb = [[rows[ir + dr][ic + dc] if (ir + dr) in rows and 0 <= ic + dc < tw else None for dc in (-1, 0, 1)] for dr in (-1, 0, 1)]
        return dict(value=rows[ir][ic], col=col, row=row, colf=colf, rowf=rowf, W=W, H=Hh, tile=ti, tile_off=off,
                    tile_len=cnt, tile_blake3=b32e(H(comp_bytes)), comp=comp, pred=pred, bps=bps, tw=tw, th=th, raster_type=raster_type,
                    geo=(tp[3], tp[4], sx, sy), neigh=nb)

# ---------------------------------------------------------------- RFC 9162 verifiers (blake3)
node = lambda l, r: H(b"\x01" + l + r)
def v_incl(idx, size, leaf, path, root):
    if idx >= size: return False
    fn, sn, r = idx, size - 1, leaf
    for p in path:
        if sn == 0: return False
        if fn & 1 or fn == sn:
            r = node(p, r)
            if not fn & 1:
                while not fn & 1 and fn != 0: fn >>= 1; sn >>= 1
        else: r = node(r, p)
        fn >>= 1; sn >>= 1
    return sn == 0 and r == root
def v_cons(n1, n2, r1, r2, path):
    if n1 == n2: return r1 == r2 and not path
    if n1 & (n1 - 1) == 0: path = [r1] + path
    fn, sn = n1 - 1, n2 - 1
    while fn & 1: fn >>= 1; sn >>= 1
    fr = sr = path[0]
    for c in path[1:]:
        if sn == 0: return False
        if fn & 1 or fn == sn:
            fr = node(c, fr); sr = node(c, sr)
            if not fn & 1:
                while not fn & 1 and fn != 0: fn >>= 1; sn >>= 1
        else: sr = node(sr, c)
        fn >>= 1; sn >>= 1
    return fr == r1 and sr == r2 and sn == 0
def sth_ok(s):
    m = H(pre("emem.translog.sth.v1") + seg(1, struct.pack(">Q", s["tree_size"])) + seg(2, b32d(s["root_b32"]))
          + seg(3, s["signed_at"].encode()) + seg(4, b32d(s["responder_pubkey_b32"])))
    return ed_ok(b32d(s["responder_pubkey_b32"]), m, b32d(s["signature_b32"]))
def witness_ok(w):
    pk = b32d(w["witness_pubkey_b32"])
    m = H(pre("emem.translog.witness.v1") + seg(1, struct.pack(">Q", w["tree_size"])) + seg(2, b32d(w["root_b32"])) + seg(3, pk))
    return ed_ok(pk, m, b32d(w["signature_b32"]))

# ---------------------------------------------------------------- batch Merkle (emem batch rule v1)
# v1: leaf blake3(0x00||L), node blake3(0x01||l||r); v0 (pre-cutover): leaf blake3(L||L), node blake3(l||r). Odd layer pairs last with itself.
def _promote(l, v): return H(b"\x00" + l) if v >= 1 else H(l + l)
def _node(l, r, v): return H(b"\x01" + l + r) if v >= 1 else H(l + r)
def merkle_batch_root(leaves, v=1):
    layer = [_promote(l, v) for l in leaves]
    while len(layer) > 1:
        layer = [_node(layer[i], layer[i + 1] if i + 1 < len(layer) else layer[i], v) for i in range(0, len(layer), 2)]
    return layer[0]
def batch_path_ok(leaf, idx, path, root, v=1):
    acc = _promote(leaf, v)
    for s in path:
        acc = _node(acc, s, v) if idx % 2 == 0 else _node(s, acc, v); idx //= 2
    return acc == root
def attestation_msg(att):
    if att.get("preimage_version", 0) >= 1:
        return H(pre("attestation") + seg(1, bytes(att["batch_root"])) + seg(2, att["registry_cid"].encode()) + seg(3, att["schema_cid"].encode()))
    return H(bytes(att["batch_root"]) + att["registry_cid"].encode() + att["schema_cid"].encode())

# ---------------------------------------------------------------- receipt preimage v2
def cbor_text(s):
    b = s.encode(); n = len(b)
    return (bytes([0x60 + n]) if n < 24 else bytes([0x78, n]) if n < 256 else bytes([0x79]) + struct.pack(">H", n)) + b
def cbor_str_map(m):
    ks = sorted(m); return bytes([0xA0 + len(ks)]) + b"".join(cbor_text(k) + cbor_text(m[k]) for k in ks)
def merkle_binding(p):
    s = pre("merkle")
    if p is None: s += seg(5, b"")
    else:
        s += seg(1, bytes(p["root"])) + seg(2, struct.pack("<I", p["leaf_index"])) + seg(3, b"".join(bytes(x) for x in p["path"])) + seg(4, bytes([p.get("version", 0)]))
    return H(s)
def receipt_digest(r, ver):
    s = pre("receipt") + seg(1, r["request_id"].encode()) + seg(2, r["served_at"].encode())
    for tag, key in ((3, "scope"), (4, "as_of"), (5, "edges")):
        if r.get(key): raise ValueError(f"receipt carries {key}; not handled by this verifier")
    if r.get("source_versions"): s += seg(6, blake3.blake3(cbor_str_map(r["source_versions"])).hexdigest().encode())
    s += seg(7, r["primitive"].encode()) + seglist(8, r["cells"]) + seglist(9, r["fact_cids"])
    if r.get("field"): raise ValueError("receipt carries field; not handled")
    if ver >= 2: s += seg(0x0B, merkle_binding(r.get("merkle_proof")).hex().encode())
    return H(s)
def receipt_ok(r):
    return ed_ok(bytes(r["responder"]), receipt_digest(r, r.get("preimage_version", 0)), bytes(r["signature"]))

# ---------------------------------------------------------------- base58btc (did:key multikey)
def b58d(s):
    A = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"; n = 0
    for ch in s: n = n * 58 + A.index(ch)
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return b"\x00" * (len(s) - len(s.lstrip("1"))) + b

# ================================================================ THE TRACE
t0 = time.time()
print(f"trace_fact.py  run {dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}\ntoken: {TOKEN}")
res = {}

# 1 token
parts = TOKEN.split(":")
ok = len(parts) == 4 and parts[0] == "emem" and parts[1] == "fact" and len(parts[3]) == 52
cell, cid = parts[2], parts[3]
link(1, "token", "emem:fact:<cell64>:<fact_cid>; fact_cid is 52 base32 chars (32-byte BLAKE3)", ok,
     [f"cell64={cell}", f"fact_cid={cid}", f"cid decodes to {len(b32d(cid))} bytes"])

# 2 resolve
s, hdr, body = http(f"{EMEM}/v1/facts/{cid}", headers={"accept": "application/cbor"})
open(os.path.join(OUT, "fact.cbor"), "wb").write(body)
link(2, "resolve bytes", "GET /v1/facts/<cid> Accept: application/cbor returns the committed bytes", s == 200,
     [f"HTTP {s}, {len(body)} bytes, content-type={hdr.get('content-type')}, etag={hdr.get('etag')}, x-emem-commit={hdr.get('x-emem-commit')}"],
     "none for integrity (link 3 checks the bytes); availability depends on the responder or any mirror")

# 3 content address
got = b32e(H(body))
tam = bytearray(body); vpos = body.find(b"\x65value") + 6
tam[vpos + {0xF9: 2, 0xFA: 4, 0xFB: 8}.get(body[vpos], 0)] ^= 1  # flip the last mantissa bit of the float value (f16/f32/f64)
link(3, "content address", "base32-nopad-lower(BLAKE3-256(bytes)) == fact_cid", got == cid and b32e(H(bytes(tam))) != cid,
     [f"recomputed {got}", f"value with its last mantissa bit flipped ({cbor2.loads(bytes(tam))['value']!r}) -> {b32e(H(bytes(tam)))} (mismatch)"], "none")

# 4 cell binding
f = cbor2.loads(body)
other = "defi.zb572.xoso.zb1ec" if cell != "defi.zb572.xoso.zb1ec" else "defi.zb493.xuqA.zcb5f"
s2, _, b2 = http(f"{EMEM}/v1/memory_token/resolve", data={"token": f"emem:fact:{other}:{cid}"})
link(4, "cell binding", "cell inside the hashed body == cell in the token (and a mislabelled token is refused)",
     f["cell"] == cell, [f"body.cell={f['cell']}", f"wrong-cell token -> HTTP {s2} ({json.loads(b2).get('code')})"],
     "none: the cell is inside the hashed bytes; the 409 is a convenience, the offline check is the equality")

# 5 cell geometry
lat, lng, hlat, hlng = cell64_decode(cell)
a = f["derivation"]["args"]
link(5, "cell geometry", "cell64 decoded independently (grid rule in spec) == lat/lng the derivation used (args[0:2])",
     lat == a[0] and lng == a[1],
     [f"decoded centre lat={lat!r} lng={lng!r}  (half-cell {hlat*111320:.1f} m N-S x {hlng*111320*math.cos(math.radians(lat)):.1f} m E-W)",
      f"args lat={a[0]!r} lng={a[1]!r}"], "none")

FN = f["derivation"]["fn_key"]
if FN == "sentinel2_l2a_indices_ndvi@1":
    # 6 provenance decode
    src = f["sources"][0]; urls = [u.strip() for u in src["id"].split(";")]
    labels = ["lat", "lng", "scene_id", "epsg", "formula", "DN[B08,B04]", "scene_cloud_pct", "max_cloud_pct", "lookback_days",
              "scl_class", "scenes_tried", "catalogue", "dn_offset"]
    lab = {labels[k]: a[k] for k in range(min(len(labels), len(a)))}
    res["args"] = lab
    link(6, "provenance decode", "sources[] and derivation{fn_key,args} are inside the hashed bytes and decode to named inputs",
         True, [f"band={f['band']} tslot={f['tslot']} value={f['value']!r} confidence={f['confidence']!r} signed_at={f['signed_at']}",
                f"fn_key={f['derivation']['fn_key']}", f"source scheme={src['scheme']} captured_at={src['captured_at']}"]
         + [f"COG {k}: {u}" for k, u in enumerate(urls)] + [f"args.{k} = {v!r}" for k, v in lab.items() if k != "formula"],
         "arg positions are labelled from the emitter source (crates/emem-api-rest/src/lib.rs, S2 arm), not from a published per-fn schema")

    # 7 recompute
    dn8, dn4 = a[5]; off = a[12]
    r8, r4 = (dn8 + off) * 1e-4, (dn4 + off) * 1e-4; ndvi = (r8 - r4) / (r8 + r4)
    link(7, "recompute value", "NDVI = (rho8-rho4)/(rho8+rho4), rho=(DN+offset)*1e-4, from the signed args; compare IEEE-754 bits",
         fbits(ndvi) == fbits(f["value"]), [f"recomputed {ndvi!r} 0x{fbits(ndvi)}", f"signed     {f['value']!r} 0x{fbits(f['value'])}",
                                             f"same DNs with offset 0 would give {((dn8-dn4)/(dn8+dn4))!r}"],
         "none for the arithmetic; the DNs themselves are checked in link 9")

    # 8 upstream STAC item
    s, item = jget(f"{PC_STAC}/collections/sentinel-2-l2a/items/{lab['scene_id']}")
    json.dump(item, open(os.path.join(OUT, "stac_item.json"), "w"))
    p = item.get("properties", {})
    strip = lambda u: u.split("?")[0]
    pb = p.get("s2:processing_baseline")
    exp_off = -1000.0 if pb and tuple(map(int, pb.split("."))) >= (4, 0) else 0.0
    checks = {
        "item.id == args.scene_id": item.get("id") == lab["scene_id"],
        "item.datetime == sources.captured_at": p.get("datetime") == src["captured_at"],
        "floor(unix(item.datetime)/86400) == fact.tslot (fast band: days since 1970)":
            int(dt.datetime.fromisoformat(p.get("datetime", "1970-01-01T00:00:00Z").replace("Z", "+00:00")).timestamp() // 86400) == f["tslot"],
        "proj:epsg == args.epsg": p.get("proj:epsg") == lab["epsg"],
        "eo:cloud_cover == args.scene_cloud_pct": p.get("eo:cloud_cover") == lab["scene_cloud_pct"],
        f"processing_baseline {pb} >= 04.00 -> offset {exp_off} == args.dn_offset": exp_off == lab["dn_offset"],
        "assets.B08.href == COG 0": strip(item["assets"]["B08"]["href"]) == urls[0],
        "assets.B04.href == COG 1": strip(item["assets"]["B04"]["href"]) == urls[1],
        "args.catalogue is the PC STAC search endpoint": lab["catalogue"] == PC_STAC + "/search",
        "product_uri baseline tag in COG path": p.get("s2:product_uri", "#") in urls[0],
    }
    link(8, "upstream catalogue (STAC)", "fetch the scene's STAC item from Planetary Computer; every provenance field must match",
         s == 200 and all(checks.values()), [f"{k}: {v}" for k, v in checks.items()] + [
            f"platform={p.get('platform')} product_uri={p.get('s2:product_uri')} granule={p.get('s2:granule_id')}",
            f"STAC asset file:checksum present: {'file:checksum' in item['assets']['B08']}"],
         "the STAC item is Microsoft's statement, served over TLS; it carries no checksum for the COG bytes")

    # 9 upstream pixel
    if "--no-pixel" in flags:
        link(9, "upstream pixel", "range-read the COG pixel", "skipped by --no-pixel", [], "the DNs are emem's reading")
    else:
        try:
            _, sas = jget(PC_SAS); tok = sas["token"]
            E, N = utm(lat, lng, int(str(lab["epsg"])[-2:]))
            cross = ""
            try:
                import pyproj
                E2, N2 = pyproj.Transformer.from_crs(4326, lab["epsg"], always_xy=True).transform(lng, lat)
                cross = f"pyproj cross-check dE={E-E2:+.2e} m dN={N-N2:+.2e} m"
            except Exception: cross = "pyproj not installed (cross-check skipped)"
            pix = {}
            for band, url, want in (("B08", urls[0], dn8), ("B04", urls[1], dn4)):
                cg = COG(url + "?" + tok); pix[band] = (cg.pixel(E, N), want)
            ev = [f"UTM zone {str(lab['epsg'])[-2:]}N: E={E:.3f} N={N:.3f} ({cross})"]
            allok = True
            for band in ("B08", "B04"):
                px, want = pix[band]
                ev.append(f"{band}: tiff tile {px['tw']}x{px['th']} {px['bps']}-bit deflate(comp={px['comp']}) predictor={px['pred']} raster_type={'PixelIsPoint' if px['raster_type']==2 else 'PixelIsArea'} "
                          f"origin=({px['geo'][0]},{px['geo'][1]}) px={px['geo'][2]} m")
                ev.append(f"{band}: col={px['col']} row={px['row']} (frac {px['colf']-px['col']:.3f},{px['rowf']-px['row']:.3f}) tile#{px['tile']} "
                          f"bytes {px['tile_off']}+{px['tile_len']} blake3={px['tile_blake3'][:20]}...  DN={px['value']}  signed DN={want:.0f}  match={px['value']==want}")
                ev.append(f"{band}: 3x3 neighbourhood {px['neigh']}")
                allok &= px["value"] == want
            res["pixel"] = {b: pix[b][0] for b in ("B08", "B04")}
            nd = lambda a8, a4: ((a8 + off) - (a4 + off)) / ((a8 + off) + (a4 + off))
            n8, n4 = pix["B08"][0]["neigh"], pix["B04"][0]["neigh"]
            grid = [[nd(n8[r][c], n4[r][c]) for c in range(3)] for r in range(3)]
            res["ndvi_3x3"] = grid
            ev.append("NDVI over the 3x3 neighbourhood: " + " | ".join(" ".join(f"{v:.3f}" for v in row) for row in grid)
                      + f"  (range {min(map(min, grid)):.3f}..{max(map(max, grid)):.3f})")
            px8 = pix["B08"][0]; rc_, rr_ = round(px8["colf"]), round(px8["rowf"]); dc, dr = rc_ - px8["col"], rr_ - px8["row"]
            ev.append(f"pixel rule: floor -> (col,row)=({px8['col']},{px8['row']}) matches the signed DNs; the pre-fix rounding rule "
                      f"(emem reads signed before PIXEL_FIX_AT 2026-09-28T04:09:26Z, lib.rs:12650) -> ({rc_},{rr_}) "
                      f"DN {n8[1+dr][1+dc]}/{n4[1+dr][1+dc]} NDVI {grid[1+dr][1+dc]:.4f}")
            stamped = any("reader=" in str(x) for x in a)
            ev.append(f"reader stamp in args: {stamped} (fact signed {f['signed_at']}; the stamp reader=cog-pixel-floor@2 exists from lib.rs:57066, commit 128ac75)")
            link(9, "upstream pixel", "range-read both COGs at the cell centre (own TIFF/Deflate/Predictor-2 decoder, own projection); DN must equal args.DN",
                 allok, ev, "none for the DNs if matched; the pixel rule (floor, PixelIsArea) is emem's choice, and nothing binds Microsoft's COG bytes to ESA's product")
        except Exception as e:
            link(9, "upstream pixel", "range-read the COG pixel", f"error: {e!r}", [], "the DNs are emem's reading")

    # 9b SCL (confidence input)
    if "--no-pixel" not in flags:
        try:
            cg = COG(strip(item["assets"]["SCL"]["href"]) + "?" + tok)
            # SCL is uint8 at 20 m; reuse reader with 8-bit path
            t = cg.tags; tw, th = t[322][0], t[323][0]; sx, sy = t[33550][0], t[33550][1]; tp = t[33922]
            col = math.floor(tp[0] + (E - tp[3]) / sx); row = math.floor(tp[1] + (tp[4] - N) / sy)
            ti = (row // th) * ((t[256][0] + tw - 1) // tw) + col // tw
            raw = zlib.decompress(cg.read(t[324][ti], t[324][ti] + t[325][ti] - 1))
            arr = bytearray(raw[:tw * th])
            if t.get(317, [1])[0] == 2:
                for r in range(th):
                    acc = 0
                    for c in range(tw): acc = (acc + arr[r * tw + c]) & 0xFF; arr[r * tw + c] = acc
            v = arr[(row % th) * tw + (col % tw)]
            link("9b", "scene-classification input", "SCL class at the pixel (20 m) == args.scl_class; confidence 0.95 is emitted for SCL 4/5/6/11",
                 v == lab["scl_class"] and abs(f["confidence"] - 0.95) < 1e-6, [f"SCL col={col} row={row} class={v} (4=vegetation); signed scl_class={lab['scl_class']}; confidence={f['confidence']!r}"],
                 "the SCL->confidence mapping is emem's rule (lib.rs S2 arm), not an ESA quantity")
        except Exception as e:
            link("9b", "scene-classification input", "SCL at pixel", f"error: {e!r}", [], "")

    # 9c emem's own signed range_hash of the same tile bytes (optional cross-witness)
    if "--no-pixel" not in flags and "pixel" in res:
        try:
            px = res["pixel"]["B08"]; u = urls[0] + "?" + tok
            s_, rh = jget(f"{EMEM}/v1/range_hash", data={"url": u, "offset": px["tile_off"], "length": px["tile_len"]})
            rc = rh["receipt"]; rpk = b32d(rc["responder_pubkey_b32"])
            m = H(pre("emem.range_hash.v1") + seg(1, rh["url"].encode()) + seg(2, struct.pack(">Q", rh["offset"])) + seg(3, struct.pack(">Q", rh["length"]))
                  + seg(4, b32d(rh["blake3_b32"])) + seg(5, (rh.get("etag") or "absent").encode()) + seg(6, rh["fetched_at"].encode())
                  + seg(7, rpk) + seg(8, rh["fetched_url"].encode()))
            sig = ed_ok(rpk, m, b32d(rc["signature_b32"]))
            link("9c", "byte-range witness", "POST /v1/range_hash on the B08 tile: emem's signed BLAKE3 of those bytes == the BLAKE3 this script computed from its own read",
                 sig and rh["blake3_b32"] == px["tile_blake3"],
                 [f"ours  blake3(tile#{px['tile']} bytes {px['tile_off']}+{px['tile_len']}) = {px['tile_blake3']}",
                  f"emem  blake3_b32 = {rh['blake3_b32']} etag={rh.get('etag')} content_total={rh.get('content_total')} fetched_at={rh['fetched_at']} sig_valid={sig}",
                  "the fact itself carries no such hash: sources[0] has no `hash`/`cid` field, so the NDVI fact does not commit to the COG bytes it read"],
                 "range_hash is a separate signed statement; it is not referenced from the fact")
        except Exception as e:
            link("9c", "byte-range witness", "range_hash cross-witness", f"error: {e!r}", [], "")


elif FN == "copernicus_dem_30m_aws_pixel@1":
    src = f["sources"][0]; url = src.get("url") or src["id"]
    link(6, "provenance decode", "sources[] and derivation{fn_key,args} are inside the hashed bytes and decode to named inputs", True,
         [f"band={f['band']} tslot={f['tslot']} value={f['value']!r} unit={f.get('unit')} signed_at={f['signed_at']}", f"fn_key={FN} args={a!r}",
          f"source scheme={src['scheme']} captured_at={src.get('captured_at')}", f"COG: {url}"],
         "the recipe is 'value = pixel of the COG at (lat,lng)'; its pixel rule is not named in the args")
    link(7, "recompute value", "no arithmetic: the value is the raster sample itself (checked in link 9)", True, [f"value={f['value']!r}"], "")
    s_, hh, _ = http(url, rng=(0, 0))
    link(8, "upstream catalogue", "the source is a bare public COG (no STAC item named in the fact); record what the host states about the object",
         "no catalogue record is named by the fact",
         [f"HTTP {s_} ETag={hh.get('ETag') or hh.get('etag')} Last-Modified={hh.get('Last-Modified') or hh.get('last-modified')} "
          f"Content-Range={hh.get('Content-Range') or hh.get('content-range')}"],
         "the object's identity rests on the S3 URL; the fact records no ETag or byte hash")
    if "--no-pixel" not in flags:
        try:
            cg = COG(url); px = cg.pixel(lng, lat)  # EPSG:4326 raster: world x = lng, y = lat
            okp = px["value"] == f["value"]
            res["pixel"] = {"DEM": px}
            flat = [v for row in px["neigh"] for v in row if v is not None]
            link(9, "upstream pixel", "range-read the COG at (lat,lng) with this script's own TIFF/Deflate/Predictor-3 decoder; sample must equal the signed value bit-for-bit",
                 okp, [f"tiff tile {px['tw']}x{px['th']} {px['bps']}-bit float deflate predictor={px['pred']} raster_type={'PixelIsPoint' if px['raster_type']==2 else 'PixelIsArea'} origin=({px['geo'][0]},{px['geo'][1]}) px={px['geo'][2]:.10f} deg",
                       f"col={px['col']} row={px['row']} (fractional {px['colf']:.3f},{px['rowf']:.3f}) tile#{px['tile']} bytes {px['tile_off']}+{px['tile_len']} blake3={px['tile_blake3']}",
                       f"sample={px['value']!r} signed={f['value']!r} bit-identical={okp}",
                       f"3x3 neighbourhood {[[round(v,2) for v in row] for row in px['neigh']]} (range {min(flat):.2f}..{max(flat):.2f} m)"],
                 "none for the sample if matched; nothing binds the AWS copy to ESA's release")
        except Exception as e:
            link(9, "upstream pixel", "range-read the COG pixel", f"error: {e!r}", [], "the value is emem's reading")
else:
    link(6, "provenance decode", "recipe-specific", f"this verifier has no rule for {FN}", [f"args={a!r}"], "the value is emem's computation")

# 10 receipts
recs = {}
_, rr = jget(f"{EMEM}/v1/recall", data={"cell": cell, "bands": [f["band"]], "tslot": f["tslot"]})
recs["recall"] = rr["receipt"]
_, rt = jget(f"{EMEM}/v1/memory_token/resolve", data={"token": TOKEN})
recs["memory_token_resolve"] = rt["receipt"]
json.dump(recs, open(os.path.join(OUT, "receipts.json"), "w"))
ev, allok = [], True
for name, r in recs.items():
    sigv = receipt_ok(r); cites = r["fact_cids"][0] == cid
    stripped = dict(r); stripped.pop("merkle_proof", None)
    strip_ok = receipt_ok(stripped)
    v1 = ed_ok(bytes(r["responder"]), receipt_digest(stripped, 1), bytes(r["signature"]))
    ev.append(f"{name}: preimage v{r['preimage_version']} request_id={r['request_id']} served_at={r['served_at']} fact_cids[0]==cid:{cites} "
              f"sig_valid={sigv}; proof-stripped sig_valid={strip_ok}; downgraded-to-v1 sig_valid={v1}"
              + ("" if cites else f"  [recall now serves a newer fact at this key: {r['fact_cids'][0]}]"))
    allok &= sigv and not strip_ok and not v1 and (cites or name == "recall")
ev.append("the receipt signs (request_id, served_at, source manifests, primitive, cells, fact_cids, merkle binding); it signs no value: the value is bound through fact_cid (link 3)")
link(10, "serve receipt", "ed25519 over PreimageV1('receipt') v2, verified offline with the responder key; tampered variants must fail",
     allok, ev, "the key is emem.dev's (link 15 binds it to the domain); a receipt proves what this responder served, not that the observation is true")

# 11 receipt Merkle proof -> batch root
mp = recs["memory_token_resolve"]["merkle_proof"]; leaf = b32d(cid)
okm = batch_path_ok(leaf, mp["leaf_index"], [bytes(x) for x in mp["path"]], bytes(mp["root"]), mp.get("version", 0))
batch_root = bytes(mp["root"])
link(11, "batch binding", "receipt.merkle_proof: promoted fact digest folded along path == root (batch rule named by proof.version)", okm,
     [f"rule v{mp.get('version', 0)} leaf_index={mp['leaf_index']} path_len={len(mp['path'])} root={b32e(batch_root)}",
      "single-fact batch: root = blake3(0x00 || blake3(fact bytes))" if mp.get("version", 0) >= 1 else "single-fact batch, legacy v0: root = blake3(d || d), d = blake3(fact bytes)"],
     "the proof is signed by the receipt; it covers fact_cids[0] only")

# 12-14 transparency log
if "--no-log" in flags:
    link(12, "attestation in log", "locate the log entry", "skipped by --no-log", [], "")
else:
    _, sthj = jget(f"{EMEM}/v1/log/sth"); sth = sthj["sth"]; n = sth["tree_size"]
    cache = {}
    def ent(i):
        if i not in cache:
            _, d = jget(f"{EMEM}/v1/log/entries?start={i}&end={i+1}"); e = d["entries"][0]
            b = b32d(e["entry_cbor_b32"]); a_ = cbor2.loads(b)
            cache[i] = (e, b, a_.get("attested_at") or a_.get("signed_at"))
        return cache[i]
    T = f["signed_at"]
    T_lo = (dt.datetime.fromisoformat(T.replace("Z", "+00:00")) - dt.timedelta(seconds=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    lo, hi, probes = 0, n - 1, 0
    while lo < hi:  # first index whose timestamp >= T_lo (log is append-ordered)
        mid = (lo + hi) // 2; probes += 1
        if ent(mid)[2] < T_lo: lo = mid + 1
        else: hi = mid
    found, scanned, i, stop = [], 0, lo, False
    T_hi = (dt.datetime.fromisoformat(T.replace("Z", "+00:00")) + dt.timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
    while not stop and i < n and scanned < 20000:
        _, d = jget(f"{EMEM}/v1/log/entries?start={i}&end={min(i+256, n)}")
        for e in d["entries"]:
            scanned += 1; b = b32d(e["entry_cbor_b32"])
            if e["entry_kind"] != "attestation": continue
            spans = cbor_map_raw(b); a_ = cbor2.loads(b)
            if (a_.get("attested_at") or "") > T_hi: stop = True
            if bytes(a_["batch_root"]) == batch_root or any(H(x) == leaf for x in cbor_array_raw(b[spans["facts"][0]:spans["facts"][1]])):
                found.append((e["leaf_index"], e, b, a_, spans))
        i = d["end_exclusive"]
        if d["returned"] == 0: break
    if not found:
        link(12, "attestation in log", "find the log entry whose attestation carries this fact", False,
             [f"bisected {probes} probes to leaf {lo}; scanned {scanned} entries to {T_hi}; none carries the fact"], "")
    else:
        li, e, b, att, spans = found[0]
        facts_raw = cbor_array_raw(b[spans["facts"][0]:spans["facts"][1]])
        leaves = sorted(H(x) for x in facts_raw)
        edges = att.get("edges") or []
        pv = att.get("preimage_version", 0)
        root_re = merkle_batch_root(leaves, pv) if not edges else None
        msg = attestation_msg(att)
        sig_ok = ed_ok(bytes(att["attester"]), msg, bytes(att["signature"]))
        chk = {
            "blake3(entry_cbor) == entry_hash_b32": b32e(H(b)) == e["entry_hash_b32"],
            "facts[] contains the exact served bytes (raw slice hashes to fact_cid)": any(x == body for x in facts_raw),
            "no duplicate leaves": len(set(leaves)) == len(leaves),
            "batch_root recomputed from facts[] == entry.batch_root": root_re == bytes(att["batch_root"]),
            "entry.batch_root == receipt.merkle_proof.root": bytes(att["batch_root"]) == batch_root,
            (f"attestation sig v{pv}: ed25519(attester, " + ("PreimageV1('attestation'){batch_root,registry_cid,schema_cid})" if pv >= 1 else "blake3(batch_root||registry_cid||schema_cid)) [legacy v0]")): sig_ok,
            "attester == fact.signer": bytes(att["attester"]) == bytes(f["signer"]),
            f"preimage_version = {pv} (" + ("domain-separated v1" if pv >= 1 else "legacy v0: unseparated concatenation, no leaf/node prefixes") + ")": True,
        }
        res["log_entry"] = dict(leaf_index=li, attested_at=att["attested_at"], n_facts=len(facts_raw), entry_hash=e["entry_hash_b32"],
                                other_entries=[x[0] for x in found[1:]])
        link(12, "attestation in log", "locate the attestation by bisection on attested_at (no fact_cid->leaf index exists), then check it",
             all(chk.values()), [f"bisection: {probes} single-entry probes -> leaf {lo}; linear scan {scanned} entries; found at leaf_index={li} "
                                 f"(attested_at={att['attested_at']}, {len(facts_raw)} fact(s), entry {len(b)} bytes); other entries carrying it: {res['log_entry']['other_entries']}"]
             + [f"{k}: {v}" for k, v in chk.items()],
             "finding the entry needs a scan: /v1/log/inclusion takes leaf_index or entry_hash, not fact_cid (docs/protocol.md:1462 lists that index as the next increment)")
        # 13 inclusion under signed STH
        _, inc = jget(f"{EMEM}/v1/log/inclusion?leaf_index={li}&tree_size={n}")
        leafh = H(b"\x00" + H(b)); path = [b32d(x) for x in inc["audit_path_b32"]]
        okinc = v_incl(li, n, leafh, path, b32d(sth["root_b32"]))
        bad = bytearray(leafh); bad[0] ^= 1
        link(13, "inclusion under signed head", "STH ed25519 valid; RFC 9162 audit path folds blake3(0x00||entry_hash) to the STH root",
             sth_ok(sth) and okinc and not v_incl(li, n, bytes(bad), path, b32d(sth["root_b32"])),
             [f"STH tree_size={n} root={sth['root_b32']} signed_at={sth['signed_at']} sig_valid={sth_ok(sth)}",
              f"leaf {li}: path_len={len(path)} inclusion={okinc}; 1-bit-flipped leaf inclusion={v_incl(li, n, bytes(bad), path, b32d(sth['root_b32']))}"],
             "a first-contact client cannot detect a split view; that needs a head pinned earlier or seen by someone else (link 14)")
        json.dump(sth, open(os.path.join(OUT, f"sth_{n}.json"), "w"))
        # 14 consistency with earlier heads
        ev, allok = [], True
        pinned = os.path.join(OUT, "pinned_sth.json")
        heads = []
        if os.path.exists(pinned):
            ps = json.load(open(pinned)); heads.append(("pinned by this script " + ps["signed_at"], ps["tree_size"], ps["root_b32"], sth_ok(ps)))
        _, wl = jget(f"{EMEM}/v1/log/witnesses?limit=200")
        # the OLDEST head co-signed by a second key that still covers our leaf: prove the leaf under it, then prove it grew into today's head
        cands = sorted([w for w in wl["witnesses"] if w.get("tier") == "org_vouched" and w["tree_size"] > li and w["tree_size"] < n], key=lambda w: w["tree_size"])
        wit = cands[0] if cands else None
        if wit: heads.append((f"witness {wit['witness_pubkey_b32'][:12]}... ({wit.get('vouched_by_domain')}) cosigned {wit['cosigned_at']}", wit["tree_size"], wit["root_b32"], witness_ok(wit)))
        for label, size, root, sigok in heads:
            if size > n: ev.append(f"{label}: size {size} > current {n}, skipped"); continue
            _, c = jget(f"{EMEM}/v1/log/consistency?first={size}&second={n}")
            okc = v_cons(size, n, b32d(root), b32d(sth["root_b32"]), [b32d(x) for x in c["consistency_proof_b32"]])
            line = f"{label}: head size={size} sig_valid={sigok}; consistency {size} -> {n}: {okc} (proof len {len(c['consistency_proof_b32'])})"
            if li < size:
                _, inc2 = jget(f"{EMEM}/v1/log/inclusion?leaf_index={li}&tree_size={size}")
                oki = v_incl(li, size, leafh, [b32d(x) for x in inc2["audit_path_b32"]], b32d(root))
                line += f"; leaf {li} included under this head: {oki}"
                allok &= oki
            ev.append(line); allok &= okc and sigok
            if wit and size == wit["tree_size"] and li < size:
                wit_bundle = {"tree_size": size, "root": b32d(root), "pubkey": b32d(wit["witness_pubkey_b32"]), "sig": b32d(wit["signature_b32"]),
                              "inclusion_path": [b32d(x) for x in inc2["audit_path_b32"]], "consistency_to_sth": [b32d(x) for x in c["consistency_proof_b32"]]}
        # a self-contained evidence bundle: everything links 3, 4, 11-14 need, verifiable offline by verify_bundle.py
        bundle = {"v": 1, "token": TOKEN, "entry": b, "leaf_index": li,
                  "sth": {"tree_size": n, "root": b32d(sth["root_b32"]), "signed_at": sth["signed_at"], "pubkey": b32d(sth["responder_pubkey_b32"]),
                          "sig": b32d(sth["signature_b32"]), "inclusion_path": path}}
        if "wit_bundle" in dir(): bundle["witness"] = wit_bundle
        if "pixel" in res and "B08" in res["pixel"]:
            bundle["upstream"] = [{"url": u_, "tile_offset": res["pixel"][k]["tile_off"], "tile_length": res["pixel"][k]["tile_len"],
                                   "tile_blake3": b32d(res["pixel"][k]["tile_blake3"]), "col": res["pixel"][k]["col"], "row": res["pixel"][k]["row"]}
                                  for k, u_ in (("B08", urls[0]), ("B04", urls[1]))]
        bb = cbor2.dumps(bundle); open(os.path.join(OUT, "bundle.cbor"), "wb").write(bb)
        ev.append(f"wrote bundle.cbor: {len(bb)} bytes (entry {len(b)} B incl. the fact bytes, {len(path)}+{len(bundle.get('witness', {}).get('inclusion_path', []))}+{len(bundle.get('witness', {}).get('consistency_to_sth', []))} hashes, STH, witness co-signature"
                  + (", upstream tile refs" if "upstream" in bundle else "") + ")")
        if not os.path.exists(pinned): json.dump(sth, open(pinned, "w")); ev.append(f"pinned this STH ({n}) to {pinned} for the next run")
        if wit and wit.get("vouched_by_domain"):
            try:
                _, wa = jget(f"https://{wit['vouched_by_domain']}/.well-known/emem-agents.json")
                hit = [x.get("nick") for x in wa.get("agents", []) if x.get("key") == wit["witness_pubkey_b32"]]
                ev.append(f"witness key published at https://{wit['vouched_by_domain']}/.well-known/emem-agents.json as {hit}: {bool(hit)}")
                allok &= bool(hit)
            except Exception as e_: ev.append(f"witness key binding check failed: {e_!r}")
        ev.append(f"log witnesses: head_is_independently_witnessed={wl.get('head_is_independently_witnessed')}, independent_operator_domains={wl.get('independent_operator_domains')}, freshest witness {wl.get('freshest_independent_witness_entries_behind')} entries behind")
        link(14, "append-only history", "an earlier signed head (pinned by us, or co-signed by a witness) is a prefix of the current head (RFC 9162 consistency)",
             allok if heads else "no earlier head held", ev,
             "the only co-signing witness domain, geo.qa, is operated by Vortx AI; organisational independence is not established")

# 15 key binding
pk = bytes(f["signer"]); pkb = b32e(pk)
_, did = jget(f"{EMEM}/.well-known/did.json")
vm = next(v for v in did["verificationMethod"] if v["id"].endswith("#responder"))
mk = b58d(vm["publicKeyMultibase"][1:])
_, jw = jget(f"{EMEM}/.well-known/jwks.json")
jx = base64.urlsafe_b64decode(jw["keys"][0]["x"] + "==")
_, wk = jget(f"{EMEM}/.well-known/emem.json")
txt = []
for resolver in ("https://dns.google/resolve?name=_emem-node.emem.dev&type=TXT", "https://cloudflare-dns.com/dns-query?name=_emem-node.emem.dev&type=TXT"):
    try:
        _, d = jget(resolver, headers={"accept": "application/dns-json"})
        txt.append((resolver.split("/")[2], [x["data"].strip('"') for x in d.get("Answer", [])], d.get("AD")))
    except Exception as e: txt.append((resolver, [f"error {e!r}"], None))
chk = {
    "fact.signer == receipt.responder": pk == bytes(recs["recall"]["responder"]),
    "did:web:emem.dev#responder Multikey (0xed01 || key) == signer": mk[:2] == b"\xed\x01" and mk[2:] == pk,
    "JWKS OKP/Ed25519 x == signer (kid == b32)": jx == pk and jw["keys"][0]["kid"] == pkb,
    ".well-known/emem.json responder.pubkey_b32 == signer": wk.get("responder", {}).get("pubkey_b32") == pkb,
}
for host, ans, ad in txt:
    chk[f"DNS TXT _emem-node.emem.dev via {host} names k={pkb[:12]}... (AD={ad})"] = any(f"k={pkb}" in a for a in ans)
link(15, "signer key -> domain", "the signing key is published under emem.dev by three HTTPS documents and one DNS TXT record",
     all(chk.values()), [f"signer b32 = {pkb}"] + [f"{k}: {v}" for k, v in chk.items()],
     "Web PKI (TLS for did.json/jwks/emem.json) and DNS without DNSSEC (AD=false): binds the key to whoever controls emem.dev, not to an independent party")

# summary
print("\n==================== CHAIN OF CUSTODY ====================")
for c in CHAIN: print(f"[{str(c['n']):>2}] {c['result']:<15} {c['link']}")
json.dump(dict(token=TOKEN, run_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), chain=CHAIN, extracted=res),
          open(os.path.join(OUT, "chain.json"), "w"), indent=1, default=str)
print(f"\nwritten {os.path.join(OUT, 'chain.json')}  ({time.time()-t0:.1f} s)")
