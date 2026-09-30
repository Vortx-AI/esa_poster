"""Resolve every emem fact token cited on the v8 poster and re-hash its CBOR with stock blake3.
Writes inventory.json. No emem code.   pip install blake3 cbor2 ; python gate_tokens.py"""
import base64, json, urllib.request, time
import blake3, cbor2
FACTS = {
 "ndvi_keylong":      "emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa",
 "ndvi_prefix_23sep": "emem:fact:defi.zb572.xoso.zb1ec:kxjvfwpa7grmfhkxoxufq5xjltq2s5syer2rzdx7odbnrxhnjzkq",
 "ndvi_trap_17jul":   "emem:fact:defi.zb572.xoso.zb1ec:jwkqm6ehelmzrwupfwyq2oqotiarexr5bdrt4xbl3znuynhurqxq",
 "tessera_keylong":   "emem:fact:defi.zb572.xoso.zb1ec:ga2o2nufuq4s4tmirplgarpj4y5axb4644y7rftpojarlkcbqdrq",
 "clay_v15":          "emem:fact:defi.zb519.faci.modA:jh2kmfiy6pbkzx3hix4qfsmrgz3vnxn64itvu3cegh3pbma73omq",
 "derived_ndvi_delta":"emem:fact:defi.zb572.xoso.zb1ec:jb67zixqk525p7uzjrrhwfkvixusueh7bfklzx4hpq5pfhrq3cxq",
 "elev_may":          "emem:fact:defi.zb493.xuqA.zcb5f:yqbolgeoycqkvj3zkxukb4bjw4odhpwvfzqo3fbgwf4spk45zala",
 "elev_sep":          "emem:fact:defi.zb493.xuqA.zcb5f:jzxzmvomshs6di3bkgponk6p3rgfk5nyvklekj6caegx6dwcuo5q",
 "temp_bengaluru":    "emem:fact:defi.zb493.zezo.zcb35:nflpddk7zsncywguwjzk5koksseqfyx4jnngkuryrnd4aykqlpfq",
 "absence_ocean":     "emem:fact:defi.zb374.toro.dEcO:jvm4xbmbenl7pzshsojtarwbk5pvhpbq62cel7vwfculuswce6xa",
}
def get(url, accept=None):
    r = urllib.request.Request(url, headers={"accept": accept} if accept else {})
    return urllib.request.urlopen(r, timeout=90).read()
out = {}
for k, t in FACTS.items():
    _, _, cell, cid = t.split(":")
    t0 = time.time(); b = get(f"https://emem.dev/v1/facts/{cid}", "application/cbor")
    name = base64.b32encode(blake3.blake3(b).digest()).decode().lower().rstrip("=")
    f = cbor2.loads(b); v = f.get("value")
    out[k] = dict(token=t, bytes=len(b), rehash=name == cid, cell_ok=f.get("cell") == cell, band=f.get("band"),
                  kind=f.get("kind"), tslot=f.get("tslot"), signed_at=f.get("signed_at"),
                  value=(v if not isinstance(v, list) else f"vector[{len(v)}]"), unit=f.get("unit"),
                  fn_key=(f.get("derivation") or {}).get("fn_key"), sources=[s.get("scheme") for s in f.get("sources", [])],
                  ms=round((time.time() - t0) * 1000))
    print(f"{k:20s} rehash={out[k]['rehash']} cell={out[k]['cell_ok']} {out[k]['band']} {str(out[k]['value'])[:22]} {out[k]['signed_at']}")
json.dump(out, open("inventory.json", "w"), indent=1)
