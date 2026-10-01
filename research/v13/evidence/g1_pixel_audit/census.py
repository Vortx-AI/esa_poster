"""Task 1: hero-cell census. Every Sentinel-2 point fact emem serves at defi.zb572.xoso.zb1ec
(Keylong), each re-hashed and re-read at the upstream COG floor and round pixels.
    python census.py   -> census.csv, census.json, recall_all.json, recall_ndvi.json
"""
import csv, json, sys, time
import pa_lib as L, pa_audit as A

CELL = "defi.zb572.xoso.zb1ec"
t0 = time.time()
_, _, b = L.http(f"{L.EMEM}/v1/recall", data={"cell": CELL, "bands": ["indices.ndvi"]}); open("recall_ndvi.json", "wb").write(b)
_, _, b = L.http(f"{L.EMEM}/v1/recall", data={"cell": CELL}); open("recall_all.json", "wb").write(b)
rall = json.loads(b)
print("recall(no band filter):", len(rall["facts"]), "facts; bands attested:", rall.get("bands_already_attested_at_cell"))
print("recall(indices.ndvi):", len(json.load(open("recall_ndvi.json"))["facts"]), "facts")
recs = []
for fj in sorted(rall["facts"], key=lambda f: (f["band"], f["tslot"], f["signed_at"])):
    if not fj["derivation"]["fn_key"].startswith("sentinel2_l2a"): continue
    cid = fj["fact_cid"]
    f, raw, ok = L.fetch_fact(cid)
    try:
        r = A.audit(f)
    except Exception as e:
        print("ERR", cid, e); continue
    r["cid"] = cid; r["cid_ok"] = ok; r["cbor_bytes"] = len(raw)
    recs.append(r)
    print(f"{cid[:8]} {r['band']:<13} {r['tslot']} {r['capture_date']} {r['provider']:<3} signed {r['signed_at']} pre={int(r['prefix_bool'])} "
          f"dns={r['signed_dns']} floor={r['floor_dns']} round={r['round_dns']} -> {r['match_class']:<14} scl s/f/r={r['scl_signed']}/{r['scl_floor']}/{r['scl_round']} "
          f"cid_ok={ok} {r['reader_stamp']}", flush=True)
cols = ["cid", "band", "tslot", "capture_date", "scene", "provider", "signed_at", "prefix_bool", "signed_value", "floor_value",
        "round_value", "match_class", "scl_signed", "scl_floor", "scl_round", "signed_dns", "floor_dns", "round_dns", "dn_offset",
        "recomputed_signed", "col_frac", "row_frac", "reader_stamp", "cid_ok"]
with open("census.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(cols)
    for r in recs: w.writerow([r[c] for c in cols])
json.dump(recs, open("census.json", "w"), indent=1, default=str)
import collections
print("\nSUMMARY (S2 point facts at hero cell):", len(recs))
print(collections.Counter((r["prefix_bool"], r["match_class"]) for r in recs))
print(collections.Counter((r["band"], r["prefix_bool"], r["match_class"]) for r in recs))
print("all cids verify:", all(r["cid_ok"] for r in recs))
print("value recomputation from signed DNs matches signed value:",
      sum(abs(r["recomputed_signed"] - r["signed_value"]) < 1e-12 for r in recs), "/", len(recs))
print("bytes", L.BYTES, "elapsed", round(time.time() - t0, 1), "s")
