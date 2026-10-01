"""verifier.py: R5 receiver-side verifier. Independent code: blake3, cbor2, pynacl, stdlib, and R1's primitives
(research/repro/v11/mutation_suite.py, imported unchanged). No emem code.

Checks, in order (the first failing one is the "refusing check"):
  hash       BLAKE3(served bytes) == the cid in the reference
  binding    record cell == reference cell (if the reference names one) == the QUESTION's cell; band; tslot
             (a bare cid is bound against the question's cell, never the record's own)
  asof       signed_at (parsed RFC 3339) <= the question's as-of time; n/a when no as-of is asked
  signature  the fact bytes sit in an attestation whose batch root recomputes and whose Ed25519 signature verifies
             under the PINNED key (preimage v1 as R1; legacy v0 as research/repro/v8/trace_fact.py)
  log        the attestation's leaf is included under a signed tree head from the pinned key (RFC 6962)
  recompute  the value recomputed bit-for-bit from the signed DNs and offset (NDVI, NBR); other bands n/a
  source     the signed DNs equal the containing pixel of the committed COG window for the record's scene;
             n/a when no window is committed for that scene
Every check returns pass / fail / n/a with a reason; an exception is a fail. Accept iff nothing fails and hash,
binding, signature and log all pass.
"""
import base64, datetime as dt, importlib.util, json, math, struct
from pathlib import Path

import blake3, cbor2

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
_spec = importlib.util.spec_from_file_location("r1", ROOT / "research/repro/v11/mutation_suite.py")
R1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R1)

H = R1.H
b32e = R1.b32e
EMEM_KEY = R1.EMEM_KEY
PW = json.loads((ROOT / "research/repro/data/v8/pixel_windows.json").read_text())
WINDOWS = {  # committed 5x5 COG windows, keyed by the scene id the record names
    "S2A_MSIL2A_20260925T054251_R005_T43SFS_20260925T090015": next(v for k, v in PW.items() if k.startswith("oj5cecci")),
    "S2C_MSIL2A_20260923T053641_R005_T43SFS_20260923T101809": next(v for k, v in PW.items() if k.startswith("kxjvfwpa")),
}
STATIC_BANDS = ("copdem30m.",)
ORDER = ["hash", "binding", "asof", "signature", "log", "recompute", "source"]
REQUIRED = ("hash", "binding", "signature", "log")


def tslot_of(date_str):
    d = dt.date.fromisoformat(date_str[:10])
    return (d - dt.date(1970, 1, 1)).days


def date_of(tslot):
    return (dt.date(1970, 1, 1) + dt.timedelta(days=tslot)).isoformat()


def parse_ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def split_ref(ref):
    """('cell' or None, cid) from 'emem:fact:<cell>:<cid>' or a bare cid."""
    ref = (ref or "").strip()
    parts = ref.split(":")
    if len(parts) == 4 and parts[0] == "emem" and parts[1] == "fact":
        return parts[2], parts[3]
    return None, parts[-1]


# ------------------------------------------------ attestation (v1 = R1; v0 legacy)
def _promote(l, v):
    return H(b"\x00" + l) if v >= 1 else H(l + l)


def _node(l, r, v):
    return H(b"\x01" + l + r) if v >= 1 else H(l + r)


def batch_root(facts, v):
    layer = [_promote(l, v) for l in sorted(H(x) for x in facts)]
    while len(layer) > 1:
        layer = [_node(layer[i], layer[i + 1] if i + 1 < len(layer) else layer[i], v) for i in range(0, len(layer), 2)]
    return layer[0]


def att_msg(att):
    if (att.get("preimage_version") or 0) >= 1:
        return R1.att_msg(att)
    return H(bytes(att["batch_root"]) + att["registry_cid"].encode() + att["schema_cid"].encode())


# ------------------------------------------------ checks
def c_hash(h, q):
    _, cid = split_ref(h["token"])
    ok = b32e(H(h["bytes"])) == cid
    return ("pass" if ok else "fail"), ("BLAKE3 of the served bytes equals the cid" if ok else
                                        "BLAKE3 of the served bytes does not equal the cid in the reference")


def c_binding(h, q):
    r = cbor2.loads(h["bytes"])
    tcell, _ = split_ref(h["token"])
    bad = []
    if tcell is not None and r["cell"] != tcell:
        bad.append(f"record cell {r['cell']} != reference cell {tcell}")
    if r["cell"] != q["cell"]:
        bad.append(f"record cell {r['cell']} != question cell {q['cell']}")
    if r["band"] != q["band"]:
        bad.append(f"record band {r['band']} != question band {q['band']}")
    if r["band"].startswith(STATIC_BANDS):
        if r["tslot"] != 0:
            bad.append("static band with non-zero tslot")
    elif q.get("tslot") is None:
        bad.append("no question date given for a time-varying band")
    elif r["tslot"] != q["tslot"]:
        bad.append(f"record date {date_of(r['tslot'])} != question date {date_of(q['tslot'])}")
    return ("fail", "; ".join(bad)) if bad else ("pass", "cell, band and date match the question")


def c_asof(h, q):
    if not q.get("as_of"):
        return "n/a", "no as-of time asked"
    r = cbor2.loads(h["bytes"])
    ok = parse_ts(r["signed_at"]) <= parse_ts(q["as_of"])
    return ("pass", f"signed {r['signed_at']} <= as-of {q['as_of']}") if ok else \
        ("fail", f"signed {r['signed_at']} is after the as-of time {q['as_of']}")


def c_signature(h, q):
    if not h.get("entry"):
        return "fail", "no attestation served"
    att, fr = cbor2.loads(h["entry"]), R1.facts_raw(h["entry"])
    v = att.get("preimage_version") or 0
    if h["bytes"] not in fr:
        return "fail", "the fact bytes are not in the attestation"
    if batch_root(fr, v) != bytes(att["batch_root"]):
        return "fail", "batch root does not recompute"
    if bytes(att["attester"]) != bytes(h["pinned_key"]):
        return "fail", "attester is not the pinned key"
    if not R1.ed_ok(h["pinned_key"], att_msg(att), att["signature"]):
        return "fail", "Ed25519 signature does not verify under the pinned key"
    return "pass", "Ed25519 attestation verifies under the pinned key"


def c_log(h, q):
    S = h.get("sth")
    if not S:
        return "fail", "no log proof served"
    if bytes(S["pubkey"]) != bytes(h["pinned_key"]) or not R1.ed_ok(S["pubkey"], R1.sth_msg(S), S["sig"]):
        return "fail", "tree head not signed by the pinned key"
    ok = R1.v_incl(h["leaf_index"], S["tree_size"], H(b"\x00" + H(h["entry"])), S["inclusion_path"], S["root"])
    return ("pass", "attestation included under the signed tree head") if ok else \
        ("fail", "inclusion proof does not fold to the signed root")


def recompute_value(r):
    fk = r["derivation"]["fn_key"]
    a = r["derivation"]["args"]
    if fk.startswith(("sentinel2_l2a_indices_ndvi", "sentinel2_l2a_indices_nbr")):
        x, y = a[5]
        off = a[12]
        rx, ry = (x + off) * 1e-4, (y + off) * 1e-4          # emem order: rho = (DN + o) * 1e-4 (research/repro/v10/algorithms.md)
        return {(rx - ry) / (rx + ry), (x - y) / ((x + off) + (y + off))}   # second: R1's algebraically equal order
    return None


def c_recompute(h, q):
    r = cbor2.loads(h["bytes"])
    v = recompute_value(r)
    if v is None:
        return "n/a", f"no recipe for {r['derivation']['fn_key']} (not recomputable)"
    ok = r["value"] in v
    return ("pass", "value recomputes bit-for-bit from the signed DNs") if ok else \
        ("fail", f"signed DNs give {min(v)!r}, record says {r['value']!r}")


def c_source(h, q):
    r = cbor2.loads(h["bytes"])
    if not r["derivation"]["fn_key"].startswith("sentinel2_l2a_indices_ndvi"):
        return "n/a", "no committed source window for this band"
    scene = r["derivation"]["args"][2]
    win = WINDOWS.get(scene)
    if win is None:
        return "n/a", f"no committed COG window for scene {scene}"
    if r["cell"] != "defi.zb572.xoso.zb1ec":
        return "n/a", "committed windows cover the Keylong field cell only"
    px = R1.window_pixel(win)
    ok = tuple(r["derivation"]["args"][5]) == px
    return ("pass", "signed DNs equal the containing pixel of the source COG") if ok else \
        ("fail", f"signed DNs {list(r['derivation']['args'][5])} != containing pixel {list(px)} in the source COG")


CHECKS = {"hash": c_hash, "binding": c_binding, "asof": c_asof, "signature": c_signature, "log": c_log,
          "recompute": c_recompute, "source": c_source}


def verify(h, q, checks=ORDER):
    """Run checks; returns dict(results={check:(status,reason)}, accept, first_fail, value)."""
    res = {}
    for c in checks:
        try:
            res[c] = CHECKS[c](h, q)
        except Exception as e:  # malformed input is a refusal, never a pass
            res[c] = ("fail", f"error: {type(e).__name__}")
    first = next((c for c in checks if res[c][0] == "fail"), None)
    if first is None:
        first = next((c for c in REQUIRED if c in checks and res[c][0] != "pass"), None)
    accept = first is None
    val = None
    if accept:
        val = cbor2.loads(h["bytes"])["value"]
    return {"results": res, "accept": accept, "first_fail": first, "value": val}
