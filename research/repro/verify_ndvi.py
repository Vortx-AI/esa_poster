"""Rebuild a signed emem NDVI value from the Sentinel-2 DNs carried inside the fact.

Checks, with no emem code:
  1. the served CBOR bytes hash (BLAKE3) to the fact_cid;
  2. NDVI recomputed from the recorded B08/B04 DNs and BOA offset equals the signed value bit-for-bit.
    pip install blake3 cbor2 ; python verify_ndvi.py [fact_cid]
"""
import base64, struct, sys, urllib.request
import blake3, cbor2

CID = sys.argv[1] if len(sys.argv) > 1 else "oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa"
req = urllib.request.Request(f"https://emem.dev/v1/facts/{CID}", headers={"accept": "application/cbor"})
body = urllib.request.urlopen(req, timeout=60).read()
name = base64.b32encode(blake3.blake3(body).digest()).decode().lower().rstrip("=")
f = cbor2.loads(body)
a = f["derivation"]["args"]
scene, (b08, b04), catalogue, offset = a[2], a[5], a[11], a[12]
r8, r4 = (b08 + offset) * 1e-4, (b04 + offset) * 1e-4
ndvi = (r8 - r4) / (r8 + r4)
bits = lambda x: struct.pack(">d", x).hex()
print(f"fact_cid matches bytes : {name == CID}  ({len(body)} bytes)")
print(f"cell / band / tslot    : {f['cell']} / {f['band']} / {f['tslot']}")
print(f"scene                  : {scene}")
print(f"catalogue, BOA offset  : {catalogue}, {offset}")
print(f"DN B08, B04            : {b08}, {b04}")
print(f"signed NDVI            : {f['value']!r}  0x{bits(f['value'])}")
print(f"recomputed NDVI        : {ndvi!r}  0x{bits(ndvi)}")
print(f"bit-identical          : {bits(ndvi) == bits(f['value'])}")
