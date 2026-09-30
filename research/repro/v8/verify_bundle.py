#!/usr/bin/env python3
"""verify_bundle.py - verify an emem evidence bundle with NO network access.
Needs blake3, cbor2, pynacl. The only input besides the bundle is the signer key you choose to trust
(default: the key emem.dev publishes in DNS TXT _emem-node.emem.dev, did.json and jwks.json).
    python verify_bundle.py bundle.cbor [expected_signer_b32]
"""
import base64, struct, sys, blake3, cbor2
from nacl.signing import VerifyKey
H = lambda b: blake3.blake3(b).digest()
b32e = lambda b: base64.b32encode(b).decode().lower().rstrip("=")
def b32d(s): return base64.b32decode(s.upper() + "=" * ((8 - len(s) % 8) % 8))
def pre(d): d = d.encode(); return b"emem.preimage.v1\x00" + struct.pack("<I", len(d)) + d
seg = lambda t, b: bytes([t]) + struct.pack("<I", len(b)) + b
def ed(pk, m, s):
    try: VerifyKey(pk).verify(m, s); return True
    except Exception: return False
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
def item_end(b, i):  # RFC 8949 item length
    ib = b[i]; mt, ai = ib >> 5, ib & 31; i += 1
    val = ai if ai < 24 else int.from_bytes(b[i:i + (1 << (ai - 24))], "big")
    if 24 <= ai <= 27: i += 1 << (ai - 24)
    if mt in (0, 1, 7): return i
    if mt in (2, 3): return i + val
    if mt == 6: return item_end(b, i)
    for _ in range(val if mt == 4 else 2 * val): i = item_end(b, i)
    return i
def facts_raw(entry):
    ai = entry[0] & 31; i = 1 if ai < 24 else 1 + (1 << (ai - 24)); n = ai if ai < 24 else int.from_bytes(entry[1:i], "big")
    for _ in range(n):
        ke = item_end(entry, i); key = cbor2.loads(entry[i:ke]); ve = item_end(entry, ke)
        if key == "facts":
            arr = entry[ke:ve]; aj = arr[0] & 31; j = 1 if aj < 24 else 1 + (1 << (aj - 24)); m = aj if aj < 24 else int.from_bytes(arr[1:j], "big")
            out = []
            for _ in range(m): e = item_end(arr, j); out.append(arr[j:e]); j = e
            return out
        i = ve
B = cbor2.loads(open(sys.argv[1], "rb").read())
want = b32d(sys.argv[2]) if len(sys.argv) > 2 else b32d("777er3yihgifqmv5hmc2wwmyszgddzderzhsx6rex4yoakwomvka")
_, _, cell, cid = B["token"].split(":")
entry = B["entry"]; att = cbor2.loads(entry); fr = facts_raw(entry)
fact = next((x for x in fr if b32e(H(x)) == cid), None)
ok = {}
ok["fact bytes inside the logged attestation hash to the token's fact_cid"] = fact is not None
f = cbor2.loads(fact) if fact else {}
ok["token cell == signed cell"] = f.get("cell") == cell
pv = att.get("preimage_version", 0)
leaves = sorted(H(x) for x in fr)
def root(ls, v):
    L = [H(b"\x00" + l) if v else H(l + l) for l in ls]
    while len(L) > 1: L = [(H(b"\x01" + L[i] + (L[i + 1] if i + 1 < len(L) else L[i])) if v else H(L[i] + (L[i + 1] if i + 1 < len(L) else L[i]))) for i in range(0, len(L), 2)]
    return L[0]
ok["batch_root recomputed from the facts"] = root(leaves, pv) == bytes(att["batch_root"]) and len(set(leaves)) == len(leaves)
msg = H(pre("attestation") + seg(1, bytes(att["batch_root"])) + seg(2, att["registry_cid"].encode()) + seg(3, att["schema_cid"].encode())) if pv else H(bytes(att["batch_root"]) + att["registry_cid"].encode() + att["schema_cid"].encode())
ok["attestation signed by the expected key"] = bytes(att["attester"]) == want and ed(want, msg, bytes(att["signature"]))
leaf = H(b"\x00" + H(entry)); S = B["sth"]
sthm = H(pre("emem.translog.sth.v1") + seg(1, struct.pack(">Q", S["tree_size"])) + seg(2, S["root"]) + seg(3, S["signed_at"].encode()) + seg(4, S["pubkey"]))
ok["STH signed by the expected key"] = S["pubkey"] == want and ed(want, sthm, S["sig"])
ok[f"entry {B['leaf_index']} included under STH {S['tree_size']}"] = v_incl(B["leaf_index"], S["tree_size"], leaf, S["inclusion_path"], S["root"])
if "witness" in B:
    W = B["witness"]
    wm = H(pre("emem.translog.witness.v1") + seg(1, struct.pack(">Q", W["tree_size"])) + seg(2, W["root"]) + seg(3, W["pubkey"]))
    ok[f"witness {b32e(W['pubkey'])[:12]}... co-signed head {W['tree_size']}"] = ed(W["pubkey"], wm, W["sig"])
    ok["entry included under the witnessed head"] = v_incl(B["leaf_index"], W["tree_size"], leaf, W["inclusion_path"], W["root"])
    ok["witnessed head is a prefix of the STH (consistency)"] = v_cons(W["tree_size"], S["tree_size"], W["root"], S["root"], W["consistency_to_sth"])
for k, v in ok.items(): print(f"{'PASS' if v else 'FAIL'}  {k}")
print(f"\n{B['token']}\n  {f.get('band')} = {f.get('value')!r} at tslot {f.get('tslot')}, signed {f.get('signed_at')}, attested {att.get('attested_at')}")
for u in B.get("upstream", []): print(f"  re-read upstream: {u['url'].rsplit('/',1)[-1]} bytes {u['tile_offset']}+{u['tile_length']} blake3 {b32e(u['tile_blake3'])[:16]}... pixel ({u['col']},{u['row']})")
print("ALL PASS" if all(ok.values()) else "SOME CHECKS FAILED"); sys.exit(0 if all(ok.values()) else 1)
