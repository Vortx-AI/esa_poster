#!/usr/bin/env python3
"""freeze_inputs.py: GET-only freeze of the real records R5 uses (no emem code, no signing, no minting).

For each record: GET /v1/facts/<cid> (CBOR), BLAKE3 re-hash == cid, locate its attestation in the public log by
bisection on attested_at (as research/repro/v8/trace_fact.py), fetch the inclusion proof under one signed tree head,
and write frozen/<cid8>.cbor (an R1-style bundle: token, bytes, entry, leaf_index, sth) plus frozen/inputs.json.
The hero record keeps its committed bundle (research/repro/v8/proof_bundle_ndvi.cbor).
"""
import base64, datetime as dt, json, sys, time, urllib.request
from pathlib import Path
import blake3, cbor2

HERE = Path(__file__).resolve().parent
OUT = HERE / "frozen"
OUT.mkdir(exist_ok=True)
EMEM = "https://emem.dev"
RECORDS = {
    "3yyaxn5dvvutqukhtycog2y6ab2hfnzlcnf56qlevgnnare3nnsa": "Keylong NDVI 30 Sep S2C (M5b; M5 truth)",
    "ezs2hn7psaynfitpzcov4my5vtyxy44re2egie4hmwsupf43mk7q": "Keylong NBR 25 Sep (M6)",
    "kxjvfwpa7grmfhkxoxufq5xjltq2s5syer2rzdx7odbnrxhnjzkq": "Keylong NDVI 23 Sep pre-fix wrong pixel (M15r)",
    "yqbolgeoycqkvj3zkxukb4bjw4odhpwvfzqo3fbgwf4spk45zala": "Bengaluru elevation 918.0 m, May (G0-B)",
    "jzxzmvomshs6di3bkgponk6p3rgfk5nyvklekj6caegx6dwcuo5q": "Bengaluru elevation 915.07 m, Sep (M20)",
    "p6ewjnlqo5npzooyrlak7gwtia23s2vlnb435xbxz3ycusv7auta": "/v1/ask town-point answer 0.2824, 30 Sep (M24)",
}
H = lambda b: blake3.blake3(b).digest()
b32e = lambda b: base64.b32encode(b).decode().lower().rstrip("=")
b32d = lambda s: base64.b32decode(s.upper() + "=" * ((8 - len(s) % 8) % 8))
LOG = []


def get(path, accept="application/json"):
    for k in range(6):
        try:
            req = urllib.request.Request(EMEM + path, headers={"accept": accept})
            with urllib.request.urlopen(req, timeout=90) as r:
                b = r.read()
                LOG.append({"GET": path, "status": r.status, "bytes": len(b)})
                return b
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 * (k + 1)); continue
            raise
        except Exception:
            time.sleep(2 * (k + 1))
    raise RuntimeError(path)


def cbor_end(b, i):
    ib = b[i]; mt, ai = ib >> 5, ib & 31; i += 1
    val = ai if ai < 24 else int.from_bytes(b[i:i + (1 << (ai - 24))], "big")
    if 24 <= ai <= 27: i += 1 << (ai - 24)
    if mt in (0, 1, 7): return i
    if mt in (2, 3): return i + val
    if mt == 6: return cbor_end(b, i)
    for _ in range(val if mt == 4 else 2 * val): i = cbor_end(b, i)
    return i


def facts_raw(entry):
    ai = entry[0] & 31
    i = 1 if ai < 24 else 1 + (1 << (ai - 24))
    n = ai if ai < 24 else int.from_bytes(entry[1:i], "big")
    for _ in range(n):
        ke = cbor_end(entry, i); key = cbor2.loads(entry[i:ke]); ve = cbor_end(entry, ke)
        if key == "facts":
            arr = entry[ke:ve]; aj = arr[0] & 31
            j = 1 if aj < 24 else 1 + (1 << (aj - 24))
            m = aj if aj < 24 else int.from_bytes(arr[1:j], "big")
            out = []
            for _ in range(m):
                e = cbor_end(arr, j); out.append(arr[j:e]); j = e
            return out
        i = ve
    return []


def main():
    sth = json.loads(get("/v1/log/sth"))["sth"]
    n = sth["tree_size"]
    cache = {}

    def ent_ts(i):
        if i not in cache:
            e = json.loads(get(f"/v1/log/entries?start={i}&end={i + 1}"))["entries"][0]
            a = cbor2.loads(b32d(e["entry_cbor_b32"]))
            cache[i] = a.get("attested_at") or a.get("signed_at") or ""
        return cache[i]

    inputs = {"frozen_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "sth": {k: sth[k] for k in ("tree_size", "root_b32", "signed_at", "responder_pubkey_b32", "signature_b32")},
              "records": {}}
    for cid, label in RECORDS.items():
        body = get(f"/v1/facts/{cid}", accept="application/cbor")
        assert b32e(H(body)) == cid, f"re-hash mismatch {cid}"
        f = cbor2.loads(body)
        T = f["signed_at"]
        t0 = dt.datetime.fromisoformat(T.replace("Z", "+00:00"))
        T_lo = (t0 - dt.timedelta(seconds=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
        T_hi = (t0 + dt.timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        lo, hi, probes = 0, n - 1, 0
        while lo < hi:
            mid = (lo + hi) // 2; probes += 1
            if ent_ts(mid) < T_lo: lo = mid + 1
            else: hi = mid
        found, i, scanned, stop = None, lo, 0, False
        while not stop and found is None and i < n and scanned < 20000:
            d = json.loads(get(f"/v1/log/entries?start={i}&end={min(i + 256, n)}"))
            for e in d["entries"]:
                scanned += 1
                if e["entry_kind"] != "attestation": continue
                b = b32d(e["entry_cbor_b32"]); a = cbor2.loads(b)
                if (a.get("attested_at") or "") > T_hi: stop = True
                if any(x == body for x in facts_raw(b)):
                    found = (e["leaf_index"], b, e["entry_hash_b32"]); break
            i = d["end_exclusive"]
            if d["returned"] == 0: break
        rec = {"label": label, "bytes": len(body), "rehash_ok": True, "cell": f["cell"], "band": f["band"],
               "tslot": f["tslot"], "value": f["value"], "unit": f.get("unit"), "signed_at": T,
               "fn_key": f["derivation"]["fn_key"], "probes": probes, "scanned": scanned}
        bundle = {"v": "r5-frozen-1", "token": f"emem:fact:{f['cell']}:{cid}", "bytes": body}
        if found:
            li, entry, eh = found
            inc = json.loads(get(f"/v1/log/inclusion?leaf_index={li}&tree_size={n}"))
            bundle.update(entry=entry, leaf_index=li, sth={
                "tree_size": n, "root": b32d(sth["root_b32"]), "signed_at": sth["signed_at"],
                "pubkey": b32d(sth["responder_pubkey_b32"]), "sig": b32d(sth["signature_b32"]),
                "inclusion_path": [b32d(x) for x in inc["audit_path_b32"]]})
            rec.update(leaf_index=li, entry_hash_b32=eh, entry_bytes=len(entry),
                       preimage_version=cbor2.loads(entry).get("preimage_version", 0))
        else:
            rec["log_entry"] = "not found"
        p = OUT / f"{cid[:8]}.cbor"
        p.write_bytes(cbor2.dumps(bundle))
        rec["file"] = p.name
        rec["file_blake3"] = blake3.blake3(p.read_bytes()).hexdigest()
        inputs["records"][cid] = rec
        print(cid[:8], label, rec.get("leaf_index"), probes, scanned, flush=True)
    inputs["http_log"] = LOG
    (OUT / "inputs.json").write_text(json.dumps(inputs, indent=1))


if __name__ == "__main__":
    main()
