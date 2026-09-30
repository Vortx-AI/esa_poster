"""Recompute every emem:state address in an /v1/ask answer from its published fields, with stock cbor2 + blake3.
    python recompute_state.py ask_keylong.json verifier_spec.json"""
import json, sys, base64, cbor2, blake3
b32 = lambda b: base64.b32encode(b).decode().rstrip("=").lower()
a = json.load(open(sys.argv[1])); g = json.load(open(sys.argv[2]))["state"]["golden_vector"]
order, C = g["field_order"], g["record"]
enc = lambda rec: cbor2.dumps({k: rec[k] for k in order if k in rec})   # the record's own field order, not RFC 8949 key sorting
assert enc(C).hex() == g["canonical_cbor_hex"], "golden vector"
r = a["receipt"]["responder"]
pk = b32(bytes(r)) if isinstance(r, list) else r   # the responder key in the answer's receipt
prev = None
for st, step in zip(a["reasoning"]["states"], a["reasoning"]["steps"]):
    df = ([{"as": "own_state", "cid": prev}] if prev else []) + [{"as": "fact", "cid": c} for c in step["new_fact_cids"]]
    rec = {"schema": C["schema"], "kind": step["stage"], "derived_from": df, "payload": step["detail"], "class": C["class"],
           "does_not_cover": C["does_not_cover"], "responder_pubkey_b32": pk}
    want = st["state"].split(":")[-1]; got = b32(blake3.blake3(enc(rec)).digest())
    print(step["stage"], got == want, want); prev = want
