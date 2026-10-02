"""SAT-042 run readers shared by F15 (f15_sat042.py) and the F15b strip (f15b_sat042_strip.py).

Every value is parsed from the captured stdout of the run, or read from the audit beside it, and asserted:
  research/repro/v12/trace/sat042_run_stdout.txt   the verbatim run (emem 04b40c5, 2026-09-30T19:14:15Z)
  research/repro/v12/trace/trace_truth.md          anchor (0.6402, 0.02), tampered segment 2, 'not a spacecraft'
  research/repro/v10/algorithms.md §15             z = |x − anchor| / 3σ, score = z/(1+z); verdict thresholds 0.5, 0.75;
                                                   the gate binds the value digest only (band, cell, tslot unchecked)
  research/v13/00_v11_review_findings.md F08, F09, F12   three refusals; the drift score is scored after admission
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TR = os.path.join(ROOT, "research/repro/v12/trace")

t = open(os.path.join(TR, "sat042_run_stdout.txt"), encoding="utf-8").read()
body = t.split("satellite_downlink stdout (verbatim)")[1].split("end satellite_downlink stdout")[0]
V = {"key": re.search(r"enrolled spacecraft key (\w+)", body).group(1),
     "profile": re.search(r"profile (\S+) requires (\d+) trace layers", body).groups(),
     "layers": re.search(r"\[([^\]]+)\]", body).group(1).replace(" ", "").split(","),
     "unbound_digest": re.search(r"payload digest (\w+) that is not bound", body).group(1),
     "facts": re.findall(r"(emem:fact:\S+)", body), "trace_token": re.search(r"(emem:trace:\S+)", body).group(1),
     "bundle_token": re.search(r"(emem:bundle:\S+)", body).group(1),
     "drift": [{"cell": m[0], "device": float(m[1]), "anchor": float(m[2]), "score": float(m[3]), "verdict": m[4]}
               for m in re.findall(r"(defi\.\S+)\s+device ([\d.]+) vs anchor ([\d.]+)\s+score ([\d.]+)\s+(\w+)", body)],
     "tamper": re.search(r"tampered segment (\d+) after signing.*?reject: chain broken at seq (\d+)", body, re.S).groups(),
     "commit": re.search(r"emem commit: (\w+)", t).group(1)[:7],
     "run": re.search(r"run window \(UTC\): (\S+)", t).group(1)}
assert "writes require the device's OS execution trace and none was presented" in body
assert "admitted: 3 facts under one verified trace" in body
assert len(V["facts"]) == 3 and len(V["drift"]) == 3 and len(V["layers"]) == int(V["profile"][1]) == 8
assert V["profile"][0] == "orbital.satellite.v1" and V["run"].startswith("2026-09-30T19:14:15Z") and V["commit"] == "04b40c5"
SEG, SEQ = int(V["tamper"][0]), int(V["tamper"][1])
assert (SEG, SEQ) == (2, 3)
ANCHOR = V["drift"][0]["anchor"]
assert all(d["anchor"] == ANCHOR for d in V["drift"]) and ANCHOR == 0.6402
N_CONS = sum(d["verdict"] == "Consistent" for d in V["drift"])
N_CONTRA = sum(d["verdict"] == "Contradicted" for d in V["drift"])
assert (N_CONS, N_CONTRA) == (2, 1)

truth = open(os.path.join(TR, "trace_truth.md"), encoding="utf-8").read()
assert "The drift anchor is a fixed pair `(0.6402, 0.02)` (line 198)" in truth
assert "The tamper edits `segments[2].log_digest` (line 215)" in truth
assert "No satellite is enrolled." in truth and "It is a deterministic simulation that exercises the real gate and verifier code." in truth
SIGMA = 0.02
alg = open(os.path.join(ROOT, "research/repro/v10/algorithms.md"), encoding="utf-8").read()
assert "`z = |x_dev − x_anchor| / (3σ)`, `score = z/(1+z)`" in alg
assert "Verdict: `<0.5` Consistent (<3σ), `<0.75` Tension (3–9σ), else Contradicted" in alg
assert "fact binding: b32(H(cbor(fact.value))) ∈ { outputⱼ.payload_digest }       (value only; band/cell not checked)" in alg
assert "It is not wired into ingest." in alg
find = open(os.path.join(ROOT, "research/v13/00_v11_review_findings.md"), encoding="utf-8").read()
assert "SAT-042 exercises three refusals: no trace, unbound output digest, and a broken chain." in find
assert "The drift score is not part of ingest." in find


def score(x):
    z = abs(x - ANCHOR) / (3 * SIGMA)
    return z / (1 + z)


for d in V["drift"]:                       # the printed scores reproduce from the formula
    assert round(score(d["device"]), 2) == d["score"], d
    assert d["verdict"] == ("Consistent" if d["score"] < 0.5 else "Tension" if d["score"] < 0.75 else "Contradicted")
assert round(1 / (1 + 1), 2) == 0.5 and round(3 / (1 + 3), 2) == 0.75     # 3σ scores 0.5, 9σ scores 0.75

KICKER = "Extending verification from observations to execution"
