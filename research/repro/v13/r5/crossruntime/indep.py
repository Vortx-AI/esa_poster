"""Independent verifier: uses only blake3, cbor2, pynacl, stdlib. No emem code.

cid(b)              base32-nopad-lower(BLAKE3-256(b))
fetch_cbor(cid)     GET https://emem.dev/v1/facts/<cid>  Accept: application/cbor
check_fact(tok)     fetch bytes, re-hash, decode, compare cell
verify_receipt(r)   ed25519 over emem.preimage.v1 domain-separated receipt preimage (v1/v2)
"""
import base64
import json
import struct
import time
import urllib.request

import blake3
import cbor2
from nacl.signing import VerifyKey

BASE = "https://emem.dev"


def cid(b: bytes) -> str:
    return base64.b32encode(blake3.blake3(b).digest()).decode().lower().rstrip("=")


def b32dec(s: str) -> bytes:
    s = s.upper()
    return base64.b32decode(s + "=" * (-len(s) % 8))


def fetch_cbor(fact_cid: str) -> bytes:
    req = urllib.request.Request(f"{BASE}/v1/facts/{fact_cid}", headers={"accept": "application/cbor"})
    return urllib.request.urlopen(req, timeout=60).read()


def check_fact(token: str):
    _, _, cell, fact_cid = token.split(":")
    t0 = time.perf_counter()
    body = fetch_cbor(fact_cid)
    ms = (time.perf_counter() - t0) * 1000
    f = cbor2.loads(body)
    return {
        "bytes": len(body),
        "rehash_cid": cid(body),
        "rehash_ok": cid(body) == fact_cid,
        "cell_ok": f["cell"] == cell,
        "cell": f["cell"], "band": f["band"], "tslot": f["tslot"], "value": f["value"],
        "signed_at": f["signed_at"], "fetch_ms": round(ms, 1),
    }, body


# ---- receipt preimage (independent re-implementation, see research/repro/verify_receipt_tamper.py)
def _seg(t, b):
    return bytes([t]) + struct.pack("<I", len(b)) + b


def _seglist(t, items):
    body = b"".join(struct.pack("<I", len(i.encode())) + i.encode() for i in items)
    return bytes([t]) + struct.pack("<I", len(items)) + body


def _pre(domain):
    d = domain.encode()
    return b"emem.preimage.v1\x00" + struct.pack("<I", len(d)) + d


def _ctext(s):
    b = s.encode()
    return (bytes([0x60 + len(b)]) if len(b) < 24 else bytes([0x78, len(b)])) + b


def _cbor_map(m):
    ks = sorted(m)
    return bytes([0xA0 + len(ks)]) + b"".join(_ctext(k) + _ctext(m[k]) for k in ks)


def _bytes(x):
    if x is None:
        return None
    if isinstance(x, list):
        return bytes(x)
    if isinstance(x, str):
        try:
            return bytes.fromhex(x)
        except ValueError:
            return b32dec(x)
    return bytes(x)


def _merkle_binding(p):
    s = _pre("merkle")
    if p is None:
        s += _seg(5, b"")
    else:
        # serde omits `version` when 0 (legacy unprefixed Merkle rule; emem-fact/src/receipt.rs:246-251).
        # /v1/verifier_spec does not state this default; a literal reading KeyErrors on pre-v1 receipts.
        s += (_seg(1, _bytes(p["root"])) + _seg(2, struct.pack("<I", p.get("leaf_index", 0)))
              + _seg(3, b"".join(_bytes(x) for x in p.get("path", []))) + _seg(4, bytes([p.get("version", 0)])))
    return blake3.blake3(s).digest()


def receipt_digest(r):
    ver = r.get("preimage_version", 0)
    s = _pre("receipt") + _seg(1, r["request_id"].encode()) + _seg(2, r["served_at"].encode())
    if r.get("source_versions"):
        s += _seg(6, blake3.blake3(_cbor_map(r["source_versions"])).hexdigest().encode())
    s += _seg(7, r["primitive"].encode()) + _seglist(8, r["cells"]) + _seglist(9, r["fact_cids"])
    if ver >= 2:
        s += _seg(0x0B, _merkle_binding(r.get("merkle_proof")).hex().encode())
    return blake3.blake3(s).digest()


def verify_receipt(r, expect_cid=None, expect_cell=None):
    """Returns (sig_ok, binds_ok). binds_ok: receipt names the expected (cell, cid)."""
    # prefer the b32 twins: some transports elide byte arrays as "[N floats omitted...]"
    pk = b32dec(r["responder_pubkey_b32"]) if "responder_pubkey_b32" in r else _bytes(r["responder"])
    sig = b32dec(r["signature_b32"]) if "signature_b32" in r else _bytes(r["signature"])
    mp = r.get("merkle_proof")
    if mp is not None and isinstance(mp.get("root"), str) and mp["root"].startswith("["):
        return None, None  # elided: cannot verify offline from this shape
    try:
        VerifyKey(pk).verify(receipt_digest(r), sig)
        ok = True
    except Exception:
        ok = False
    binds = True
    if expect_cid is not None:
        binds = binds and expect_cid in r["fact_cids"]
    if expect_cell is not None:
        binds = binds and expect_cell in r["cells"]
    return ok, binds


def http_json(method, url, body=None, headers=None, timeout=90):
    h = {"content-type": "application/json", "accept": "application/json"}
    h.update(headers or {})
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        hdrs = dict(resp.headers)
    return raw, hdrs, (time.perf_counter() - t0) * 1000
