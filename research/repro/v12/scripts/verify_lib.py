"""Offline verification of emem facts with stock libraries only (blake3, cbor2, pynacl).

Rules implemented from GET /v1/verifier_spec (emem 2.4.2, fetched 2026-09-30) and RFC 6962/9162:
  fact_cid   = base32-nopad-lower(BLAKE3-256(canonical CBOR bytes of the fact))
  receipt    = ed25519(responder, BLAKE3(PreimageV1("receipt") v2 segment stream))
  batch      = leaves sorted(BLAKE3(fact bytes)); leaf BLAKE3(0x00||L); node BLAKE3(0x01||l||r); odd layer pairs last with itself
  attestation= ed25519(attester, BLAKE3(PreimageV1("attestation"){1:batch_root,2:registry_cid,3:schema_cid}))
  log        = RFC 6962 tree; leaf BLAKE3(0x00||BLAKE3(entry cbor)); STH signed under PreimageV1("emem.translog.sth.v1")
No emem code is imported. Network access is only used to fetch bytes; every check is local.
"""
import base64, struct
import blake3, cbor2
from nacl.signing import VerifyKey

H = lambda b: blake3.blake3(b).digest()
b32e = lambda b: base64.b32encode(b).decode().lower().rstrip("=")
def b32d(s): return base64.b32decode(s.upper() + "=" * ((8 - len(s) % 8) % 8))
seg = lambda t, b: bytes([t]) + struct.pack("<I", len(b)) + b
def seglist(t, items):
    return bytes([t]) + struct.pack("<I", len(items)) + b"".join(struct.pack("<I", len(i.encode())) + i.encode() for i in items)
def pre(d):
    d = d.encode(); return b"emem.preimage.v1\x00" + struct.pack("<I", len(d)) + d
def ed_ok(pk, m, s):
    try: VerifyKey(bytes(pk)).verify(m, bytes(s)); return True
    except Exception: return False
def cid_of(b): return b32e(H(b))

# ------------------------------------------------ published key decoding
def b58d(s):
    A = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"; n = 0
    for ch in s: n = n * 58 + A.index(ch)
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return b"\x00" * (len(s) - len(s.lstrip("1"))) + b
def did_multikey(z):  # z6Mk... -> 0xed01 || key
    raw = b58d(z[1:]); assert raw[:2] == b"\xed\x01"; return raw[2:]
def jwk_x(x): return base64.urlsafe_b64decode(x + "=" * ((4 - len(x) % 4) % 4))

# ------------------------------------------------ receipt preimage v2
def cbor_text(s):
    b = s.encode(); n = len(b)
    return (bytes([0x60 + n]) if n < 24 else bytes([0x78, n]) if n < 256 else bytes([0x79]) + struct.pack(">H", n)) + b
def cbor_str_map(m):  # keys in PLAIN string sort (BTreeMap order), per verifier_spec.manifest_hex_key_order
    ks = sorted(m); return bytes([0xA0 + len(ks)]) + b"".join(cbor_text(k) + cbor_text(m[k]) for k in ks)
def merkle_binding(p):
    s = pre("merkle")
    if p is None: s += seg(5, b"")
    else: s += seg(1, bytes(p["root"])) + seg(2, struct.pack("<I", p["leaf_index"])) + seg(3, b"".join(bytes(x) for x in p["path"])) + seg(4, bytes([p.get("version", 0)]))
    return H(s)
class Unhandled(Exception): pass
def receipt_digest(r, ver=None):
    ver = r.get("preimage_version", 0) if ver is None else ver
    if ver < 1: raise Unhandled("legacy v0 receipt")
    s = pre("receipt") + seg(1, r["request_id"].encode()) + seg(2, r["served_at"].encode())
    for key in ("scope", "as_of", "edges", "field"):
        if r.get(key): raise Unhandled(f"receipt carries {key}")
    if r.get("source_versions"): s += seg(6, blake3.blake3(cbor_str_map(r["source_versions"])).hexdigest().encode())
    s += seg(7, r["primitive"].encode()) + seglist(8, r["cells"]) + seglist(9, r["fact_cids"])
    if ver >= 2: s += seg(0x0B, merkle_binding(r.get("merkle_proof")).hex().encode())
    return H(s)
def receipt_ok(r, pinned):
    if bytes(r["responder"]) != pinned: return False
    try: return ed_ok(pinned, receipt_digest(r), bytes(r["signature"]))
    except Unhandled: return None

# ------------------------------------------------ batch merkle (rule v1; v0 legacy)
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

# ------------------------------------------------ raw CBOR slicing (no re-encoding)
def cbor_end(b, i):
    ib = b[i]; mt, ai = ib >> 5, ib & 31; i += 1
    val = ai if ai < 24 else int.from_bytes(b[i:i + (1 << (ai - 24))], "big")
    if 24 <= ai <= 27: i += 1 << (ai - 24)
    if mt in (0, 1, 7): return i
    if mt in (2, 3): return i + val
    if mt == 6: return cbor_end(b, i)
    for _ in range(val if mt == 4 else 2 * val): i = cbor_end(b, i)
    return i
def cbor_map_raw(b):
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
def entry_facts_raw(entry):
    sp = cbor_map_raw(entry)
    if "facts" not in sp: return []
    a, z = sp["facts"]; return cbor_array_raw(entry[a:z])

# ------------------------------------------------ transparency log (RFC 6962 / 9162)
node = lambda l, r: H(b"\x01" + l + r)
def sth_msg(s):
    return H(pre("emem.translog.sth.v1") + seg(1, struct.pack(">Q", s["tree_size"])) + seg(2, b32d(s["root_b32"]))
             + seg(3, s["signed_at"].encode()) + seg(4, b32d(s["responder_pubkey_b32"])))
def sth_ok(s, pinned):
    return b32d(s["responder_pubkey_b32"]) == pinned and ed_ok(pinned, sth_msg(s), b32d(s["signature_b32"]))
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
def check_attestation_entry(entry, fact_bytes, pinned):
    """All local checks on one log entry that should carry fact_bytes."""
    att = cbor2.loads(entry)
    fr = entry_facts_raw(entry)
    leaves = sorted(H(x) for x in fr)
    pv = att.get("preimage_version", 0)
    edges = att.get("edges") or []
    root_re = merkle_batch_root(leaves, 1 if pv >= 1 else 0) if (leaves and not edges) else None
    return {
        "fact_bytes_in_entry": any(x == fact_bytes for x in fr),
        "batch_root_recomputed": (root_re == bytes(att["batch_root"])) if root_re is not None else None,
        "attester_is_pinned_key": bytes(att["attester"]) == pinned,
        "attestation_sig_valid": ed_ok(pinned, attestation_msg(att), bytes(att["signature"])),
        "preimage_version": pv, "n_facts_in_batch": len(fr), "attested_at": att.get("attested_at"),
        "batch_root_b32": b32e(bytes(att["batch_root"])), "has_edges": bool(edges),
    }
