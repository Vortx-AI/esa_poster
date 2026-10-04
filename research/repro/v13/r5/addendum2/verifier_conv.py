"""verifier_conv.py: the matched conventional receiver of prereg addendum 2.

It runs the checks of verifier.py that need neither a content address nor an attestation, on the JSON observation a
condition-B handoff carries: binding (cell, band, date against the question), as-of (signed_at against the asked time),
recompute (the value from the DNs and offset in the observation, emem's formula) and source re-read (the DNs against
the committed COG window). It cannot run hash, signature or log: plain JSON has no content address and no attestation.
Accept iff no check fails and binding passes, the same rule as verifier.py with REQUIRED reduced to what exists.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import verifier as V  # noqa: E402

ORDER = ["binding", "asof", "recompute", "source"]
REQUIRED = ("binding",)
KEY_CELL = "defi.zb572.xoso.zb1ec"


def _tslot(ob):
    if ob.get("tslot") is not None:
        return int(ob["tslot"])
    return V.tslot_of(ob["date"]) if ob.get("date") else None


def c_binding(ob, q):
    bad = []
    if ob.get("cell") != q["cell"]:
        bad.append(f"observation cell {ob.get('cell')} != question cell {q['cell']}")
    if ob.get("band") != q["band"]:
        bad.append(f"observation band {ob.get('band')} != question band {q['band']}")
    ts = _tslot(ob)
    if str(ob.get("band", "")).startswith(V.STATIC_BANDS):
        if ts not in (0, None):
            bad.append("static band with non-zero tslot")
    elif q.get("tslot") is None:
        bad.append("no question date given for a time-varying band")
    elif ts != q["tslot"]:
        bad.append(f"observation date {V.date_of(ts) if ts else ts} != question date {V.date_of(q['tslot'])}")
    return ("fail", "; ".join(bad)) if bad else ("pass", "cell, band and date match the question")


def c_asof(ob, q):
    if not q.get("as_of"):
        return "n/a", "no as-of time asked"
    ok = V.parse_ts(ob["signed_at"]) <= V.parse_ts(q["as_of"])
    return ("pass", f"signed {ob['signed_at']} <= as-of {q['as_of']}") if ok else \
        ("fail", f"signed {ob['signed_at']} is after the as-of time {q['as_of']}")


def _dns(ob):
    d = ob.get("derivation") or {}
    fk = d.get("fn_key", "")
    if fk.startswith("sentinel2_l2a_indices_ndvi"):
        return fk, (d["B08_DN"], d["B04_DN"]), d["boa_offset"]
    if fk.startswith("sentinel2_l2a_indices_nbr"):
        return fk, (d["B08_DN"], d["B12_DN"]), d["boa_offset"]
    return fk, None, None


def c_recompute(ob, q):
    fk, dn, off = _dns(ob)
    if dn is None:
        return "n/a", f"no recipe for {fk} (not recomputable)"
    x, y = dn
    rx, ry = (x + off) * 1e-4, (y + off) * 1e-4                  # the same two orders as verifier.recompute_value
    v = {(rx - ry) / (rx + ry), (x - y) / ((x + off) + (y + off))}
    ok = ob.get("value") in v
    return ("pass", "value recomputes bit-for-bit from the DNs") if ok else \
        ("fail", f"the DNs give {min(v)!r}, the observation says {ob.get('value')!r}")


def c_source(ob, q):
    fk, dn, _ = _dns(ob)
    if not fk.startswith("sentinel2_l2a_indices_ndvi"):
        return "n/a", "no committed source window for this band"
    win = V.WINDOWS.get(ob.get("source_scene"))
    if win is None:
        return "n/a", f"no committed COG window for scene {ob.get('source_scene')}"
    if ob.get("cell") != KEY_CELL:
        return "n/a", "committed windows cover the Keylong field cell only"
    px = V.R1.window_pixel(win)
    ok = tuple(dn) == px
    return ("pass", "the DNs equal the containing pixel of the source COG") if ok else \
        ("fail", f"the DNs {list(dn)} != containing pixel {list(px)} in the source COG")


CHECKS = {"binding": c_binding, "asof": c_asof, "recompute": c_recompute, "source": c_source}


def verify(ob, q):
    res = {}
    for c in ORDER:
        try:
            res[c] = CHECKS[c](ob, q)
        except Exception as e:  # malformed input is a refusal, never a pass
            res[c] = ("fail", f"error: {type(e).__name__}")
    first = next((c for c in ORDER if res[c][0] == "fail"), None)
    if first is None:
        first = next((c for c in REQUIRED if res[c][0] != "pass"), None)
    accept = first is None
    return {"results": res, "accept": accept, "first_fail": first, "value": ob.get("value") if accept else None}
