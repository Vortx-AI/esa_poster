"""tools.py: the receiver's tools, one set per condition. Used in-process by the open-model loop and behind the
stdio MCP server (relay_server.py) for Claude. The relay serves whatever the item's state says; the verifier pins the
item's key and the committed source windows, which the relay cannot change."""
import json, math, re

import cbor2

import items as IT
import verifier as V

TOOLS = {
    "C": [{"name": "search_corpus", "description": "Search the shared field log. Returns the top 3 passages for a text query.",
           "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}],
    "D": [{"name": "fetch_record", "description": "Fetch a referenced record by its record ref (for example obs-xxxxxx).",
           "inputSchema": {"type": "object", "properties": {"ref": {"type": "string"}}, "required": ["ref"]}}],
    "E0": [
        {"name": "fetch_evidence", "description": "Fetch the record an emem evidence token (emem:fact:<cell>:<cid>) points to, as served by the relay.",
         "inputSchema": {"type": "object", "properties": {"token": {"type": "string"}}, "required": ["token"]}},
        {"name": "verify_evidence",
         "description": ("Verify an emem evidence token against a question. Checks: content hash; binding of the record to the cell, band "
                         "and date you pass; optional as_of time (record must be signed by then); Ed25519 signature under the pinned emem "
                         "key; transparency-log inclusion; recompute of the value from the signed inputs; source re-read against the "
                         "committed Sentinel-2 pixel. Returns each check and a verdict."),
         "inputSchema": {"type": "object", "properties": {
             "token": {"type": "string"}, "cell": {"type": "string"},
             "band": {"type": "string", "description": "e.g. indices.ndvi or copdem30m.elevation_mean"},
             "date": {"type": "string", "description": "YYYY-MM-DD scene date (ignored for static bands)"},
             "as_of": {"type": "string", "description": "optional RFC 3339 time"}},
             "required": ["token", "cell", "band"]}}],
    "E+": [{"name": "resolve_verified",
            "description": ("Resolve an emem evidence token through a fail-closed verifier bound to the task's question. Returns the value "
                            "only if every check passes; otherwise returns an error naming the failed check."),
            "inputSchema": {"type": "object", "properties": {"token": {"type": "string"}}, "required": ["token"]}}],
}
TOOLS["E"] = TOOLS["E0"]
TOOLS["A"] = TOOLS["B"] = []

STOP = set("the a an of in for and or to is was at on by from with this that field log".split())


def _tok(s):
    return [w for w in re.findall(r"[a-z0-9.]+", s.lower()) if w not in STOP]


def bm25(query, docs, k1=1.5, b=0.75):
    D = [_tok(d) for d in docs]
    N, avg = len(D), sum(map(len, D)) / len(D)
    q = _tok(query)
    sc = []
    for i, d in enumerate(D):
        s = 0.0
        for t in set(q):
            n = sum(1 for x in D if t in x)
            if n == 0:
                continue
            idf = math.log(1 + (N - n + 0.5) / (n + 0.5))
            f = d.count(t)
            s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(d) / avg))
        sc.append((s, -i))
    order = sorted(range(N), key=lambda i: sc[i], reverse=True)
    return [docs[i] for i in order[:3]]


def _lookup(it, token):
    _, cid = V.split_ref(token)
    _, hcid = V.split_ref(it["h"]["token"])
    return it["h"] if cid == hcid else None


def _q_from_args(a):
    band = (a.get("band") or "").strip()
    date = (a.get("date") or "").strip()
    try:
        ts = V.tslot_of(date) if date else None
    except Exception:
        ts = None
    return {"cell": (a.get("cell") or "").strip(), "band": band, "tslot": ts, "as_of": (a.get("as_of") or "").strip() or None}


def call(it, cond, name, args):
    """Returns (is_error, text, meta)."""
    allowed = {t["name"] for t in TOOLS[cond]}
    if name not in allowed:
        return True, f"unknown tool {name}", {}
    if name == "search_corpus":
        return False, json.dumps({"passages": bm25(args.get("query", ""), IT.corpus(it))}), {}
    if name == "fetch_record":
        ref = (args.get("ref") or "").strip()
        if ref != IT.OPAQUE_REF:
            return True, f"record {ref} not found", {}
        return False, json.dumps(IT.observation_json(dict(it, h=dict(it["h"], record=cbor2.loads(it["h"]["bytes"]))))), {}
    token = (args.get("token") or "").strip()
    h = _lookup(it, token)
    if h is None:
        return True, "not found: no record for this token", {"found": False}
    if name == "fetch_evidence":
        ob = IT.observation_json(dict(it, h=dict(h, record=cbor2.loads(h["bytes"]))))
        ob["fact_cid"] = V.split_ref(token)[1]
        ob["bytes"] = len(h["bytes"])
        return False, json.dumps(ob), {}
    if name == "verify_evidence":
        q = _q_from_args(args)
        r = V.verify(dict(h, token=token), q)
        out = {"checks": {c: {"result": s, "detail": d} for c, (s, d) in r["results"].items()},
               "verdict": "PASS" if r["accept"] else f"FAIL (first failed check: {r['first_fail']})"}
        if r["accept"]:
            out["value_verbatim"] = repr(r["value"])
        return False, json.dumps(out), {"verdict": r["accept"], "first_fail": r["first_fail"], "bound_q": q}
    if name == "resolve_verified":
        r = V.verify(dict(h, token=token), it["q"])
        if not r["accept"]:
            c = r["first_fail"]
            return True, f"refused: {c} check failed: {r['results'][c][1]}", {"verdict": False, "first_fail": c}
        rec = cbor2.loads(h["bytes"])
        out = {"value_verbatim": repr(rec["value"]), "unit": rec.get("unit"), "cell": rec["cell"], "band": rec["band"],
               "date": V.date_of(rec["tslot"]) if rec["tslot"] else None, "signed_at": rec["signed_at"], "verified": True}
        return False, json.dumps(out), {"verdict": True}
    return True, "unsupported", {}
