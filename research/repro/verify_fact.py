"""Independently re-derive an emem fact_cid from the bytes a server returns.

Uses only third-party reference libraries (blake3, cbor2) and no emem code.
    pip install blake3 cbor2
    python verify_fact.py [emem:fact:<cell64>:<fact_cid>]
"""
import base64
import sys
import urllib.request

import blake3
import cbor2

TOKEN = sys.argv[1] if len(sys.argv) > 1 else (
    "emem:fact:defi.zb493.zezo.zcb35:"
    "nflpddk7zsncywguwjzk5koksseqfyx4jnngkuryrnd4aykqlpfq"
)


def cid(b: bytes) -> str:
    return base64.b32encode(blake3.blake3(b).digest()).decode().lower().rstrip("=")


_, _, cell, fact_cid = TOKEN.split(":")
req = urllib.request.Request(
    f"https://emem.dev/v1/facts/{fact_cid}", headers={"accept": "application/cbor"}
)
body = urllib.request.urlopen(req, timeout=30).read()
fact = cbor2.loads(body)

print(f"bytes received : {len(body)}")
print(f"token fact_cid : {fact_cid}")
print(f"re-derived cid : {cid(body)}")
print(f"cid matches    : {cid(body) == fact_cid}")
print(f"cell matches   : {fact['cell'] == cell}  ({fact['cell']})")
print(f"observation    : {fact['band']} = {fact['value']} {fact['unit']} "
      f"(tslot {fact['tslot']}, signed {fact['signed_at']})")

# Change the value by 0.1 and re-encode: the name no longer matches.
fact["value"] = fact["value"] + 0.1
tampered = cbor2.dumps(fact)
print(f"tampered value : {fact['value']} -> cid {cid(tampered)[:16]}... "
      f"matches={cid(tampered) == fact_cid}")
