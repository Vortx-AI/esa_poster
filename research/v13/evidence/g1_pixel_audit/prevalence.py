"""Task 3: store-wide prevalence of the pre-fix pixel rule among Sentinel-2 point facts cited in
https://emem.dev/channel.json. One fact per cell (seeded random), all post-fix facts.
    python prevalence.py [n_pre=200] -> prevalence.csv, prevalence.json, prevalence_summary.json
"""
import csv, json, math, random, sys, time, collections, concurrent.futures as cf
import pa_lib as L, pa_audit as A

N_PRE = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 200
FIX = L.PIXEL_FIX_AT
rows = [json.loads(l) for l in open("channel_facts.jsonl")]
s2 = [r for r in rows if r.get("status") == 200 and (r.get("fn_key") or "").startswith("sentinel2_l2a")
      and (r["band"].startswith("indices.") or r["band"].startswith("s2.B"))]
pre = [r for r in s2 if r["signed_at"] < FIX]; post = [r for r in s2 if r["signed_at"] >= FIX]
rng = random.Random(20261019)
bycell = collections.defaultdict(list)
for r in pre: bycell[r["cell"]].append(r)
cells = sorted(bycell); rng.shuffle(cells)
sample_pre = [rng.choice(bycell[c]) for c in cells[:N_PRE]]
sample = sample_pre + post
print(f"S2 point facts in channel: {len(s2)} (pre-fix {len(pre)} over {len(bycell)} cells, post-fix {len(post)}); auditing {len(sample_pre)} pre + {len(post)} post", flush=True)
t0 = time.time()


def one(r):
    try:
        f, raw, ok = L.fetch_fact(r["cid"])
        rec = A.audit(f, want_window=False); rec["cid"] = r["cid"]; rec["cid_ok"] = ok
        return rec
    except Exception as e:
        return dict(cid=r["cid"], error=repr(e)[:200], band=r["band"], signed_at=r["signed_at"], prefix_bool=r["signed_at"] < FIX)


recs = []
if "--retry" in sys.argv:  # re-audit only the records that errored last time
    prev = json.load(open("prevalence.json"))
    keep = [r for r in prev if "error" not in r]; redo = {r["cid"] for r in prev if "error" in r}
    sample = [r for r in sample if r["cid"] in redo]; recs = keep
    print("retrying", len(sample), flush=True)
with cf.ThreadPoolExecutor(10) as ex:
    for i, rec in enumerate(ex.map(one, sample)):
        recs.append(rec)
        if i % 20 == 0: print(i, round(time.time() - t0), L.BYTES, flush=True)
json.dump(recs, open("prevalence.json", "w"), indent=1, default=str)
cols = ["cid", "cell", "band", "tslot", "capture_date", "scene", "provider", "signed_at", "prefix_bool", "signed_value", "floor_value",
        "round_value", "match_class", "scl_signed", "scl_floor", "scl_round", "signed_dns", "floor_dns", "round_dns", "dn_offset",
        "col_frac", "row_frac", "asset_res", "reader_stamp", "cid_ok", "error"]
with open("prevalence.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(cols)
    for r in recs: w.writerow([r.get(c, "") for c in cols])
print("done", round(time.time() - t0), "s", L.BYTES)
