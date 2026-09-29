"""Replay one EO key at several transaction times (as_of_signed_at) and re-hash each answer.

Key: Bengaluru cell defi.zb493.xuqA.zcb5f, band copdem30m.elevation_mean, tslot 0.
    pip install blake3 ; python verify_bitemporal.py
"""
import base64, json, urllib.request
import blake3

def post(path, body):
    r = urllib.request.Request("https://emem.dev" + path, json.dumps(body).encode(),
                               {"content-type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=60))

def rehash(cid):
    r = urllib.request.Request(f"https://emem.dev/v1/facts/{cid}", headers={"accept": "application/cbor"})
    b = urllib.request.urlopen(r, timeout=60).read()
    return base64.b32encode(blake3.blake3(b).digest()).decode().lower().rstrip("=") == cid

for t in ["2026-05-01", "2026-06-15", "2026-08-12", "2026-09-29"]:
    out = post("/v1/recall", {"cell64": "defi.zb493.xuqA.zcb5f", "bands": ["copdem30m.elevation_mean"],
                              "tslot": 0, "as_of_signed_at": f"{t}T00:00:00Z"})
    facts = out.get("facts") or []
    if not facts:
        print(f"as known on {t}: no fact yet"); continue
    f = facts[0]
    print(f"as known on {t}: {f['value']} m  signed {f['signed_at']}  "
          f"source {f['sources'][0]['scheme']}  cid {f['fact_cid'][:8]}…  re-hash {rehash(f['fact_cid'])}")
