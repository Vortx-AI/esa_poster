"""Task 3 step 1: fetch every emem:fact: token cited in https://emem.dev/channel.json (JSON form, for band triage).
    python harvest_channel.py -> channel_facts.jsonl"""
import json, concurrent.futures as cf
import pa_lib as L
toks = open("channel_tokens.txt").read().split()
def get(t):
    cell, cid = t.split(":")[2], t.split(":")[3]
    try:
        s, h, b = L.http(f"{L.EMEM}/v1/facts/{cid}", tries=3, timeout=40)
        if s != 200: return dict(token=t, status=s)
        f = json.loads(b); return dict(token=t, status=s, band=f.get("band"), fn_key=(f.get("derivation") or {}).get("fn_key"),
                                       signed_at=f.get("signed_at"), cell=f.get("cell"), token_cell=cell, cid=cid, kind=f.get("kind"))
    except Exception as e:
        return dict(token=t, status=f"err {e!r}"[:80])
with cf.ThreadPoolExecutor(24) as ex, open("channel_facts.jsonl", "w") as out:
    for i, r in enumerate(ex.map(get, toks)):
        out.write(json.dumps(r) + "\n")
        if i % 500 == 0: print(i, flush=True)
print("emem bytes", L.BYTES)
