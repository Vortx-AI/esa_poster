"""A signed absence vs an unsigned skip.

Ocean point with no Copernicus DEM GLO-30 tile -> a signed Absence fact whose reason is hash-bound.
    pip install blake3 ; python verify_absence.py
"""
import base64, json, urllib.request
import blake3

def post(path, body):
    r = urllib.request.Request("https://emem.dev" + path, json.dumps(body).encode(),
                               {"content-type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=60))

out = post("/v1/recall", {"lat": -12.26142, "lng": -140.15477, "bands": ["copdem30m.elevation_mean"]})
f = out["facts"][0]
reason = f.get("reason", "")
rc = base64.b32encode(blake3.blake3(reason.encode()).digest()[:16]).decode().lower().rstrip("=")
print("kind            :", f["kind"], "| value:", f.get("value"))
print("reason          :", reason[:140], "…")
print("reason_cid bound:", rc == f.get("reason_cid"), f.get("reason_cid"))
v = post("/v1/verify_receipt", {"receipt": out["receipt"]})
print("receipt valid   :", v.get("valid"), "| token:", f.get("memory_token", "")[:40], "…")
