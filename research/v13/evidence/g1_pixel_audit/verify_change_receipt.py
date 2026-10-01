"""Verify the signed receipt on the live /v1/change_attribution answer (ed25519 over the domain-separated
receipt preimage v2, rules as in docs/protocol.md; code mirrors scratchpad/v8/fulltrace/trace_fact.py) and re-hash the
stored ledger fact it returns. No emem code."""
import base64, json, struct, blake3
from nacl.signing import VerifyKey
import pa_lib as L
H = lambda b: blake3.blake3(b).digest()
def pre(domain): d = domain.encode(); return b"emem.preimage.v1\x00" + struct.pack("<I", len(d)) + d
seg = lambda t, b: bytes([t]) + struct.pack("<I", len(b)) + b
def seglist(t, items): return bytes([t]) + struct.pack("<I", len(items)) + b"".join(struct.pack("<I", len(i.encode())) + i.encode() for i in items)
def cbor_text(s):
    b = s.encode(); n = len(b)
    return (bytes([0x60 + n]) if n < 24 else bytes([0x78, n]) if n < 256 else bytes([0x79]) + struct.pack(">H", n)) + b
def cbor_str_map(m): ks = sorted(m); return bytes([0xA0 + len(ks)]) + b"".join(cbor_text(k) + cbor_text(m[k]) for k in ks)
def merkle_binding(p):
    s = pre("merkle")
    if p is None: s += seg(5, b"")
    else: s += seg(1, bytes(p["root"])) + seg(2, struct.pack("<I", p["leaf_index"])) + seg(3, b"".join(bytes(x) for x in p["path"])) + seg(4, bytes([p.get("version", 0)]))
    return H(s)
def receipt_digest(r, ver):
    s = pre("receipt") + seg(1, r["request_id"].encode()) + seg(2, r["served_at"].encode())
    for key in ("scope", "as_of", "edges", "field"):
        if r.get(key): raise ValueError(f"receipt carries {key}; not handled")
    if r.get("source_versions"): s += seg(6, blake3.blake3(cbor_str_map(r["source_versions"])).hexdigest().encode())
    s += seg(7, r["primitive"].encode()) + seglist(8, r["cells"]) + seglist(9, r["fact_cids"])
    if ver >= 2: s += seg(0x0B, merkle_binding(r.get("merkle_proof")).hex().encode())
    return H(s)
d = json.load(open("change_attr_live.json")); r = d["receipt"]
try:
    VerifyKey(bytes(r["responder"])).verify(receipt_digest(r, r.get("preimage_version", 0)), bytes(r["signature"])); sig = True
except Exception as e: sig = f"FAIL {e!r}"
print("receipt served_at", r["served_at"], "primitive", r["primitive"], "signature valid:", sig)
print("receipt binds fact_cids:", r["fact_cids"])
lf = d["ledger_fact"]["fact_cid"]; f, raw, ok = L.fetch_fact(lf)
print("ledger fact", lf, "re-hash ok:", ok, "signed_at", f.get("signed_at"), "kind", f.get("kind"), "parents", f.get("parents"))
v = f.get("value"); s = json.dumps(v, default=str)
print("ledger cites kxjvfwpa (pre-fix, round pixel):", "kxjvfwpa7grmfhkxoxufq5xjltq2s5syer2rzdx7odbnrxhnjzkq" in s, "| 6x6af2zx (pre-fix):", "6x6af2zxxkecrvihrwdgipqk2pcfbspgmnl5exk5ipd5thy3cala" in s)
json.dump(dict(signature_valid=sig, served_at=r["served_at"], fact_cids=r["fact_cids"], ledger_cid=lf, ledger_rehash_ok=ok, ledger_signed_at=f.get("signed_at")), open("verify_change_receipt.json", "w"), indent=1)
