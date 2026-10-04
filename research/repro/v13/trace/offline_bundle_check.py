"""Re-run the 4,906-byte offline evidence file with networking disabled, plus three negative cases.

Closes the gap the v11 audit recorded (research/audit_v11/poster_evidence_audit.md, A33): the unshare -rn run and the
1-bit tamper, wrong cell and wrong key cases had no committed log. Needs Linux unshare (user + network namespace).
    python research/repro/v13/trace/offline_bundle_check.py   -> writes offline_bundle_log.txt next to this file
"""
import datetime as dt
import subprocess
import sys
import tempfile
from pathlib import Path

import cbor2

HERE = Path(__file__).resolve().parent
V8 = HERE.parents[1] / "v8"
BUNDLE = V8 / "proof_bundle_ndvi.cbor"
VERIFY = V8 / "verify_bundle.py"
WRONG_KEY = "a" * 52   # a well-formed base32 Ed25519 key that is not emem.dev's


def run(bundle, *extra):
    cmd = ["unshare", "-rn", sys.executable, str(VERIFY), str(bundle), *extra]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout


def variant(name, mutate):
    b = cbor2.loads(BUNDLE.read_bytes())
    mutate(b)
    p = Path(tempfile.mkdtemp()) / f"{name}.cbor"
    p.write_bytes(cbor2.dumps(b))
    return p


def flip_bit(b):
    e = bytearray(b["entry"])
    e[len(e) // 2] ^= 0x01          # one bit inside the logged entry that carries the fact bytes
    b["entry"] = bytes(e)


def wrong_cell(b):
    pre, kind, cell, cid = b["token"].split(":")
    b["token"] = ":".join([pre, kind, cell[:-1] + ("d" if cell[-1] != "d" else "e"), cid])


out = [f"offline_bundle_check.py  run {dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}",
       f"bundle {BUNDLE.name}: {BUNDLE.stat().st_size} bytes; every case runs under 'unshare -rn' (no network)", ""]
cases = [("genuine", BUNDLE, (), 0), ("1-bit tamper", variant("tamper", flip_bit), (), 1),
         ("wrong cell", variant("cell", wrong_cell), (), 1), ("wrong key", BUNDLE, (WRONG_KEY,), 1)]
ok = True
for name, path, extra, want in cases:
    rc, so = run(path, *extra)
    passes = sum(1 for l in so.splitlines() if l.startswith("PASS"))
    fails = sum(1 for l in so.splitlines() if l.startswith("FAIL"))
    good = (rc == 0) == (want == 0)
    ok &= good
    out.append(f"[{name}] exit {rc}; {passes} PASS, {fails} FAIL; expected {'accept' if want == 0 else 'reject'}: "
               f"{'as expected' if good else 'UNEXPECTED'}")
    out += ["    " + l for l in so.splitlines() if l.startswith(("PASS", "FAIL"))]
    out.append("")
out.append("RESULT: " + ("all four cases as expected" if ok else "MISMATCH"))
(HERE / "offline_bundle_log.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
sys.exit(0 if ok else 1)
