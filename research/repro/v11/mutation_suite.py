#!/usr/bin/env python3
"""mutation_suite.py: adversarial handoff mutations x verification depth (an ablation), offline.

What it measures
    Agent A hands agent B evidence for a question (cell, band, tslot). Something between A's
    observation and B's decision is wrong: a paraphrase, a relabelled reference, a forged record,
    or an error by the signer itself. For each mutation and each representation / verification
    depth, the suite decides whether B would ACT ON CORRUPTED EVIDENCE (a false acceptance),
    REFUSE it, or be UNAFFECTED (B's decision input never passed through the corrupted channel).

    This is a deterministic study of the VERIFIER, not of a language model. Whether a model runs
    the check is a separate question, measured in poster R3 (research/repro/data/v8/results.json).

Inputs (all committed; no network)
    ../v8/proof_bundle_ndvi.cbor      real signed fact, attestation, STH, witness, upstream refs
    ../data/v8/pixel_windows.json     5x5 DN windows read from the public Sentinel-2 COGs

Threat models
    T1  relay, mirror or forger: controls everything B receives; does NOT hold the pinned key.
    T2  the trusted signer itself errs or equivocates. Simulated with a TEST key derived from a
        public string, which the verifier is told to trust. It is not emem's key.

Output: out/mutation_matrix.json, out/mutation_matrix.csv, out/summary.md
Needs:  blake3, cbor2, pynacl.        python research/repro/v11/mutation_suite.py
"""
import base64
import copy
import csv
import json
import math
import struct
import time
from pathlib import Path

import blake3
import cbor2
from nacl.signing import SigningKey, VerifyKey

HERE = Path(__file__).resolve().parent
REPRO = HERE.parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

H = lambda b: blake3.blake3(b).digest()
b32e = lambda b: base64.b32encode(b).decode().lower().rstrip("=")
seg = lambda t, b: bytes([t]) + struct.pack("<I", len(b)) + b
node = lambda l, r: H(b"\x01" + l + r)


def pre(d):
    d = d.encode()
    return b"emem.preimage.v1\x00" + struct.pack("<I", len(d)) + d


def ed_ok(pk, m, s):
    try:
        VerifyKey(bytes(pk)).verify(m, bytes(s))
        return True
    except Exception:
        return False


# ------------------------------------------------ RFC 6962 inclusion and CBOR slicing (as v8/verify_bundle.py)
def v_incl(idx, size, leaf, path, root):
    if idx >= size:
        return False
    fn, sn, r = idx, size - 1, leaf
    for p in path:
        if sn == 0:
            return False
        if fn & 1 or fn == sn:
            r = node(p, r)
            if not fn & 1:
                while not fn & 1 and fn != 0:
                    fn >>= 1
                    sn >>= 1
        else:
            r = node(r, p)
        fn >>= 1
        sn >>= 1
    return sn == 0 and r == root


def item_end(b, i):
    ib = b[i]
    mt, ai = ib >> 5, ib & 31
    i += 1
    val = ai if ai < 24 else int.from_bytes(b[i:i + (1 << (ai - 24))], "big")
    if 24 <= ai <= 27:
        i += 1 << (ai - 24)
    if mt in (0, 1, 7):
        return i
    if mt in (2, 3):
        return i + val
    if mt == 6:
        return item_end(b, i)
    for _ in range(val if mt == 4 else 2 * val):
        i = item_end(b, i)
    return i


def facts_raw(entry):
    """The fact byte strings exactly as they sit inside the attestation (no re-encoding)."""
    ai = entry[0] & 31
    i = 1 if ai < 24 else 1 + (1 << (ai - 24))
    n = ai if ai < 24 else int.from_bytes(entry[1:i], "big")
    for _ in range(n):
        ke = item_end(entry, i)
        key = cbor2.loads(entry[i:ke])
        ve = item_end(entry, ke)
        if key == "facts":
            arr = entry[ke:ve]
            aj = arr[0] & 31
            j = 1 if aj < 24 else 1 + (1 << (aj - 24))
            m = aj if aj < 24 else int.from_bytes(arr[1:j], "big")
            out = []
            for _ in range(m):
                e = item_end(arr, j)
                out.append(arr[j:e])
                j = e
            return out
        i = ve
    return []


def batch_root(fact_bytes_list):
    L = [H(b"\x00" + l) for l in sorted(H(x) for x in fact_bytes_list)]
    while len(L) > 1:
        L = [H(b"\x01" + L[i] + (L[i + 1] if i + 1 < len(L) else L[i])) for i in range(0, len(L), 2)]
    return L[0]


def att_msg(att):
    return H(pre("attestation") + seg(1, bytes(att["batch_root"])) + seg(2, att["registry_cid"].encode())
             + seg(3, att["schema_cid"].encode()))


def sth_msg(S):
    return H(pre("emem.translog.sth.v1") + seg(1, struct.pack(">Q", S["tree_size"])) + seg(2, S["root"])
             + seg(3, S["signed_at"].encode()) + seg(4, S["pubkey"]))


# ------------------------------------------------ real inputs
BUNDLE_PATH = REPRO / "v8" / "proof_bundle_ndvi.cbor"
BUNDLE = cbor2.loads(BUNDLE_PATH.read_bytes())
EMEM_KEY = base64.b32decode("777er3yihgifqmv5hmc2wwmyszgddzderzhsx6rex4yoakwomvka".upper() + "====")
ENTRY = BUNDLE["entry"]
FACT = facts_raw(ENTRY)[0]
FACT_D = cbor2.loads(FACT)
_, _, TOKEN_CELL, TOKEN_CID = BUNDLE["token"].split(":")
PW = json.loads((REPRO / "data" / "v8" / "pixel_windows.json").read_text())
WIN = next(v for k, v in PW.items() if k.startswith("oj5cecci"))   # 25 Sep window around this fact
OTHER_CELL = "defi.zb493.xuqA.zcb5f"                              # Bengaluru, a real cell on the board
QUESTION = {"cell": TOKEN_CELL, "band": "indices.ndvi", "tslot": 20721}
RULE = 0.4705                                                      # R3's rule: irrigate iff NDVI <= 0.4705
DN_IDX, OFF_IDX, SCENE_IDX = 5, 12, 2                              # positions in derivation.args
GENUINE = FACT_D["value"]


def ndvi(b8, b4, off):
    return (b8 - b4) / ((b8 + off) + (b4 + off))


def window_pixel(win, drow=0):
    cc, rr = win["centre_col_row"]
    oc, orr = win["window_origin_col_row"]
    c, r = math.floor(cc) - oc, math.floor(rr) - orr + drow
    return float(win["B08"][r][c]), float(win["B04"][r][c])


# ------------------------------------------------ handoffs
def genuine():
    return {
        "stated": repr(GENUINE),                     # A's text, all 16 significant digits
        "record": copy.deepcopy(FACT_D),             # a structured copy of the record (levels A, B)
        "token": BUNDLE["token"],
        "bytes": FACT,                               # the bytes the resolver returns
        "entry": ENTRY, "sth": BUNDLE["sth"], "leaf_index": BUNDLE["leaf_index"],
        "pinned_key": EMEM_KEY, "question": dict(QUESTION), "cog": WIN,
    }


def forge(h, mutate, signer=None, logged=True):
    """Re-encode a mutated record and make its token consistent; optionally sign and log it."""
    d = copy.deepcopy(FACT_D)
    mutate(d)
    b = cbor2.dumps(d)
    h.update(record=cbor2.loads(b), bytes=b, token=f"emem:fact:{d['cell']}:{b32e(H(b))}", stated=repr(d["value"]))
    if signer is None:                                # T1: no key, so the genuine attestation and log stay
        return h
    sk = signer
    pk = bytes(sk.verify_key)
    base = cbor2.loads(ENTRY)
    att = {"facts": [cbor2.loads(b)], "batch_root": list(batch_root([b])), "attester": list(pk),
           "attester_key_epoch": 0, "registry_cid": base["registry_cid"], "schema_cid": base["schema_cid"],
           "attested_at": d["signed_at"], "preimage_version": 1}
    att["signature"] = list(sk.sign(att_msg(att)).signature)
    entry = cbor2.dumps(att)
    assert facts_raw(entry)[0] == b, "fact bytes inside the new entry differ from the forged bytes"
    leaf = H(b"\x00" + H(entry))
    x, y = H(b"\x00" + H(b"another entry")), H(b"\x00" + H(b"a third entry"))
    if logged:
        S = {"tree_size": 2, "root": node(leaf, x), "signed_at": d["signed_at"], "pubkey": pk, "inclusion_path": [x]}
    else:                                             # equivocation: the public log does not hold this entry
        S = {"tree_size": 2, "root": node(x, y), "signed_at": d["signed_at"], "pubkey": pk, "inclusion_path": [y]}
    S["sig"] = sk.sign(sth_msg(S)).signature
    h.update(entry=entry, sth=S, leaf_index=0)
    return h


TEST_SIGNER = SigningKey(H(b"emem mutation suite: TEST signer, not emem's key"))
FORGER = SigningKey(H(b"emem mutation suite: forger"))


def set_value(v):
    return lambda d: d.update(value=v)


def m_stated_ulp(h):
    v = math.nextafter(GENUINE, 1.0)
    h["stated"] = repr(v)
    h["record"]["value"] = v
    return h


def m_stated_round(h):
    h["stated"] = "0.47"
    h["record"]["value"] = 0.47
    return h


def m_bytes_ulp(h):
    i = FACT.find(b"\xfb" + struct.pack(">d", GENUINE))
    b = FACT[:i + 1] + struct.pack(">d", math.nextafter(GENUINE, 1.0)) + FACT[i + 9:]
    h.update(bytes=b, record=cbor2.loads(b))
    h["stated"] = repr(h["record"]["value"])
    return h


def m_other_cell(h):
    h["token"] = f"emem:fact:{OTHER_CELL}:{TOKEN_CID}"
    h["question"]["cell"] = OTHER_CELL
    return h


def m_stale(h):
    h["question"]["tslot"] = 20723
    return h


def m_band(h):
    h["question"]["band"] = "indices.ndmi"
    return h


def m_typo(h):
    bad = TOKEN_CID[:-1] + ("a" if TOKEN_CID[-1] != "a" else "b")
    h["token"] = f"emem:fact:{TOKEN_CELL}:{bad}"
    return h


def m_forge_value(h):
    return forge(h, set_value(0.45))


def m_forge_cell(h):
    forge(h, lambda d: d.update(cell=OTHER_CELL))
    h["question"]["cell"] = OTHER_CELL
    return h


def m_forge_tslot(h):
    forge(h, lambda d: d.update(tslot=20723))
    h["question"]["tslot"] = 20723
    return h


def _scene(d):
    d["derivation"]["args"][SCENE_IDX] = "S2B_MSIL2A_20260927T054239_R005_T43SFS_20260927T081707"


def _offset(d):
    d["derivation"]["args"][OFF_IDX] = 0.0
    b8, b4 = d["derivation"]["args"][DN_IDX]
    d["value"] = ndvi(b8, b4, 0.0)


def m_forge_scene(h):
    return forge(h, _scene)


def m_forge_offset(h):
    return forge(h, _offset)


def m_forger_key(h):
    forge(h, set_value(0.45), signer=FORGER)
    h["pinned_key"] = EMEM_KEY                        # B still pins emem's published key
    return h


def m_signer_arith(h):
    forge(h, set_value(0.46), signer=TEST_SIGNER)
    h["pinned_key"] = bytes(TEST_SIGNER.verify_key)
    return h


def _neighbour(d):
    b8, b4 = window_pixel(WIN, drow=1)                # the pixel 10 m south, from the real 25 Sep window
    d["derivation"]["args"][DN_IDX] = [b8, b4]
    d["value"] = ndvi(b8, b4, d["derivation"]["args"][OFF_IDX])


def m_signer_pixel(h):
    forge(h, _neighbour, signer=TEST_SIGNER)
    h["pinned_key"] = bytes(TEST_SIGNER.verify_key)
    return h


def m_equivocate(h):
    """A second signed version, shown only to B: consistent arithmetic and pixels, relabelled as current."""
    forge(h, lambda d: d.update(tslot=20723), signer=TEST_SIGNER, logged=False)
    h["pinned_key"] = bytes(TEST_SIGNER.verify_key)
    h["question"]["tslot"] = 20723
    return h


ALL = ("A", "B", "C", "D", "E", "F", "G", "H", "I")
# id, family, threat, description, builder, harmful-if-accepted-even-with-genuine-value, applies, real case
MUTATIONS = [
    ("G0", "control", "none", "genuine handoff, nothing altered", lambda h: h, False, ALL, None),
    ("M1", "paraphrase", "T1", "stated value moved by 1 ULP", m_stated_ulp, False, ALL, None),
    ("M2", "paraphrase", "T1", 'stated value rounded to "0.47"', m_stated_round, False, ALL, "§21 trap; R3 rounded arm"),
    ("M3", "relay", "T1", "1 ULP changed inside the served bytes; token kept", m_bytes_ulp, False, ALL, None),
    ("M4", "misbinding", "T1", "record cited for another cell", m_other_cell, True, ALL, "§4 relabelled token"),
    ("M5", "misbinding", "T1", "an older record handed over as the current answer", m_stale, True, ALL, "§6 cube member date"),
    ("M6", "misbinding", "T1", "a record for another band handed over", m_band, True, ALL, None),
    ("M7", "reference", "T1", "token miscopied by one character", m_typo, False, ALL[2:], None),
    ("M8", "forgery", "T1", "value changed to 0.45, re-encoded and re-hashed", m_forge_value, False, ALL, None),
    ("M9", "forgery", "T1", "cell changed inside the record, re-hashed", m_forge_cell, True, ALL, None),
    ("M10", "forgery", "T1", "tslot changed to look current, re-hashed", m_forge_tslot, True, ALL, None),
    ("M11", "forgery", "T1", "source scene id changed, re-hashed", m_forge_scene, True, ALL, None),
    ("M12", "forgery", "T1", "derivation offset changed, value recomputed, re-hashed", m_forge_offset, False, ALL, None),
    ("M13", "forgery", "T1", "value 0.45, signed and logged under the forger's own key", m_forger_key, False, ALL, None),
    ("M14", "signer error", "T2", "value (0.46) disagrees with the signed DNs; signed and logged", m_signer_arith, False, ALL, None),
    ("M15", "signer error", "T2", "DNs read from the pixel 10 m south; signed and logged", m_signer_pixel, False, ALL,
     "§7: 162 of 200 pre-fix records"),
    ("M16", "signer error", "T2", "a second signed version shown only to B (not in the log)", m_equivocate, True, ALL, None),
    ("M17", "referent", "T1", "same record; A meant a different physical entity", lambda h: h, True, ALL,
     "R4 Maasvlakte entity"),
]

LEVELS = [
    ("A", "prose", "the value as text"),
    ("B", "structured", "the value in a JSON record"),
    ("C", "opaque id", "an id that B resolves itself"),
    ("D", "content hash", "re-hash the bytes to the cid"),
    ("E", "+ binding", "cell, band and tslot match the question"),
    ("F", "+ signature", "Ed25519 under the pinned key"),
    ("G", "+ log", "inclusion under the signed tree head"),
    ("H", "+ recompute", "NDVI recomputed from the signed DNs"),
    ("I", "+ source re-read", "DNs equal the COG pixel that holds the point"),
]
ORDER = [lv for lv, _, _ in LEVELS]


# ------------------------------------------------ the verifier: one check per level
def check_hash(h):
    return b32e(H(h["bytes"])) == h["token"].split(":")[3]


def check_binding(h):
    cell = h["token"].split(":")[2]
    r, q = cbor2.loads(h["bytes"]), h["question"]
    return r["cell"] == cell == q["cell"] and r["band"] == q["band"] and r["tslot"] == q["tslot"]


def check_signature(h):
    att, fr = cbor2.loads(h["entry"]), facts_raw(h["entry"])
    return (h["bytes"] in fr and batch_root(fr) == bytes(att["batch_root"])
            and bytes(att["attester"]) == bytes(h["pinned_key"])
            and ed_ok(h["pinned_key"], att_msg(att), att["signature"]))


def check_log(h):
    S = h["sth"]
    if bytes(S["pubkey"]) != bytes(h["pinned_key"]) or not ed_ok(S["pubkey"], sth_msg(S), S["sig"]):
        return False
    return v_incl(h["leaf_index"], S["tree_size"], H(b"\x00" + H(h["entry"])), S["inclusion_path"], S["root"])


def check_recompute(h):
    r = cbor2.loads(h["bytes"])
    b8, b4 = r["derivation"]["args"][DN_IDX]
    return ndvi(b8, b4, r["derivation"]["args"][OFF_IDX]) == r["value"]


def check_source(h):
    r = cbor2.loads(h["bytes"])
    return tuple(r["derivation"]["args"][DN_IDX]) == window_pixel(h["cog"])


CHECKS = {"D": check_hash, "E": check_binding, "F": check_signature, "G": check_log,
          "H": check_recompute, "I": check_source}


def decide(level, h):
    """(refused?, failed check, value B acts on)."""
    if level == "A":
        return False, None, float(h["stated"])
    if level == "B":
        return False, None, h["record"]["value"]
    if level == "C":                                  # opaque id over the same untrusted path
        cid = h["token"].split(":")[3]
        if cid not in {TOKEN_CID, b32e(H(h["bytes"]))}:
            return True, "C", None                    # a miscopied id resolves to nothing
        return False, None, cbor2.loads(h["bytes"])["value"]
    for lv in ORDER[3:ORDER.index(level) + 1]:
        try:
            ok = CHECKS[lv](h)
        except Exception:                             # malformed input is a refusal, never a pass
            ok = False
        if not ok:
            return True, lv, None
    return False, None, cbor2.loads(h["bytes"])["value"]


def decide_set(checks, h):
    """Run an arbitrary subset of the checks (leave-one-out ablation)."""
    for lv in ORDER[3:]:
        if lv not in checks:
            continue
        try:
            ok = CHECKS[lv](h)
        except Exception:
            ok = False
        if not ok:
            return True, lv, None
    return False, None, cbor2.loads(h["bytes"])["value"]


def leave_one_out():
    full = set(ORDER[3:])
    res = {}
    for drop in ORDER[3:]:
        through = []
        for mid, fam, threat, desc, build, harm_always, applies, real in MUTATIONS:
            if mid in ("G0", "M17"):
                continue
            refused, _, v = decide_set(full - {drop}, build(genuine()))
            if not refused and (harm_always or v != GENUINE):
                through.append(mid)
        res[drop] = through
    return res


def evaluate():
    rows = []
    for mid, fam, threat, desc, build, harm_always, applies, real in MUTATIONS:
        for lv in ORDER:
            if lv not in applies:
                rows.append({"mutation": mid, "level": lv, "outcome": "n/a"})
                continue
            h = build(genuine())
            refused, failed, v = decide(lv, h)
            if refused:
                out = "refused"
            elif mid == "G0":
                out = "acted correctly"
            elif harm_always or v != GENUINE:
                out = "acted on corrupted evidence"
            else:
                out = "unaffected"
            flips = (not refused) and ((v <= RULE) != (GENUINE <= RULE))
            rows.append({"mutation": mid, "level": lv, "outcome": out, "failed_check": failed,
                         "value_acted_on": v, "decision_flipped": flips})
    return rows


def main():
    t0 = time.perf_counter()
    rows = evaluate()
    t_suite = time.perf_counter() - t0
    reps, t1 = 200, time.perf_counter()
    for _ in range(reps):
        decide("I", genuine())
    t_full = (time.perf_counter() - t1) / reps
    by = {(r["mutation"], r["level"]): r for r in rows}
    inscope = [m[0] for m in MUTATIONS if m[0] not in ("G0", "M17")]
    summary = {}
    for lv, name, adds in LEVELS:
        app = [m for m in inscope if by[(m, lv)]["outcome"] != "n/a"]
        fa = [m for m in app if by[(m, lv)]["outcome"] == "acted on corrupted evidence"]
        summary[lv] = {"representation": name, "adds": adds, "applicable": len(app), "false_accepts": len(fa),
                       "false_accept_ids": fa,
                       "decision_flips": [m for m in app if by[(m, lv)].get("decision_flipped")],
                       "genuine_refused": by[("G0", lv)]["outcome"] == "refused",
                       "entity_case_accepted": by[("M17", lv)]["outcome"] != "refused"}
    first = {m[0]: next((lv for lv in ORDER if by[(m[0], lv)]["outcome"] in ("refused", "unaffected")), None)
             for m in MUTATIONS}
    loo = leave_one_out()
    meta = {
        "generated_by": "research/repro/v11/mutation_suite.py",
        "inputs": {"bundle": "research/repro/v8/proof_bundle_ndvi.cbor", "bundle_blake3": b32e(H(BUNDLE_PATH.read_bytes())),
                   "pixel_windows": "research/repro/data/v8/pixel_windows.json"},
        "token": BUNDLE["token"], "question": QUESTION, "rule": f"irrigate iff NDVI <= {RULE}",
        "genuine_value": GENUINE, "neighbour_pixel_value": ndvi(*window_pixel(WIN, 1), -1000.0),
        "test_signer_pubkey_b32": b32e(bytes(TEST_SIGNER.verify_key)),
        "suite_seconds": round(t_suite, 4), "full_verification_ms": round(t_full * 1000, 3),
        "levels": [{"id": a, "name": b, "adds": c} for a, b, c in LEVELS],
        "mutations": [{"id": m[0], "family": m[1], "threat": m[2], "desc": m[3], "harmful_even_if_value_genuine": m[5],
                       "applies": list(m[6]), "real_case": m[7], "first_protected_level": first[m[0]]} for m in MUTATIONS],
    }
    (OUT / "mutation_matrix.json").write_text(json.dumps({"meta": meta, "summary": summary, "leave_one_out": loo,
                                                         "rows": rows}, indent=1))
    with open(OUT / "mutation_matrix.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["mutation", "family", "threat", "description"] + [f"{a} {b}" for a, b, _ in LEVELS])
        for m in MUTATIONS:
            cells = []
            for lv in ORDER:
                r = by[(m[0], lv)]
                cells.append(r["outcome"] + (f" [{r['failed_check']}]" if r.get("failed_check") else ""))
            w.writerow([m[0], m[1], m[2], m[3]] + cells)
    lines = ["# Mutation suite: summary", "",
             f"{len(inscope)} in-scope mutations, one control (G0), one out-of-scope case (M17, entity).",
             f"Whole suite {meta['suite_seconds']} s; one full verification (level I) {meta['full_verification_ms']} ms, offline.",
             "", "| level | representation | in-scope applicable | acted on corrupted evidence | decision flipped | genuine refused |",
             "|---|---|---|---|---|---|"]
    for lv, name, _ in LEVELS:
        s = summary[lv]
        lines.append(f"| {lv} | {name} | {s['applicable']} | {s['false_accepts']} ({', '.join(s['false_accept_ids']) or 'none'}) | "
                     f"{', '.join(s['decision_flips']) or 'none'} | {'yes' if s['genuine_refused'] else 'no'} |")
    lines += ["", "First level at which B is protected (refused or unaffected):", ""]
    lines += [f"- {m[0]} ({m[3]}): {first[m[0]] or 'never'}" for m in MUTATIONS if m[0] != "G0"]
    lines += ["", "Leave-one-out (all six checks minus one): mutations that get through", ""]
    names = {lv: n for lv, n, _ in LEVELS}
    lines += [f"- without {lv} ({names[lv].lstrip('+ ')}): {', '.join(v) or 'none'}" for lv, v in loo.items()]
    lines += ["", "Notes", "",
              "- The source check (I) compares the signed DNs with the committed 25 Sep COG window; it does not",
              "  follow a forged scene id to another scene, so M11 is caught here by the signature, not by the re-read.",
              "- The signature check recomputes the batch root from the fact hashes, so it subsumes the content hash.",
              "  The hash earns its place by being checkable alone, offline, without the attestation.",
              "- T2 rows use a TEST key the verifier is told to trust; nothing is signed with emem's key."]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
