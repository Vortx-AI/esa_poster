#!/usr/bin/env python3
"""Stamp, sign and publish one pointer.v1 body to emem, the way ememdemo's viewer does it.

    publish.py BODY.md OUTDIR [--flat] [--go]

1. fetch GET /v1/log/sth and verify its signature against the pinned responder key
   (ememdemo llms.txt `signer`), then stamp `after: sth <size> <root> <signed_at>` as
   the first front-matter line and add `spec: <pointer.v1 spec cid>` after `emem: pointer.v1`
   (ememdemo time.mjs stamp() and emem.mjs specify()).
2. name it by its bytes: cid = base32(blake3(note)[:16]); path =
   /memories/by_attester/<pk8>/poster-proto/<cid>.md (the filename is a cid, so the
   viewer's getNote() checks the bytes hash to the name).
3. send the create UNSIGNED over MCP and over A2A; both are refused and name the digest.
4. only with --go: sign with sign_write.py (which refuses unless the refusal's digest equals
   the locally computed v2 digest) and send the signed create over A2A.
Nothing secret is printed; the key stays in $EMEM_IDENTITY.
"""
import base64, json, os, subprocess, sys, time, struct, urllib.request
from pathlib import Path
import blake3, nacl.signing

EMEM = "https://emem.dev"
SIGNER = "777er3yihgifqmv5hmc2wwmyszgddzderzhsx6rex4yoakwomvka"   # ememdemo llms.txt `signer`
POINTER_SPEC = "mlxrdcys43hao7cz554s46bp7a"
SIGN = "/home/user/vortx-ai/emem/plugins/emem/skills/emem-sign-and-attest/scripts/sign_write.py"
CA = "/root/.ccr/ca-bundle.crt"

b32 = lambda b: base64.b32encode(b).decode().rstrip("=").lower()
def unb32(s): s = s.upper(); return base64.b32decode(s + "=" * ((8 - len(s) % 8) % 8))

def http(method, url, body=None, headers=None):
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    import ssl; ctx = ssl.create_default_context(cafile=CA)
    t = time.time()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            return r.status, r.read(), time.time() - t
    except urllib.error.HTTPError as e:
        return e.code, e.read(), time.time() - t

def pre_v1(domain: bytes, segs):
    o = b"emem.preimage.v1\0" + struct.pack("<I", len(domain)) + domain
    for tag, b in segs: o += bytes([tag]) + struct.pack("<I", len(b)) + b
    return o

def main():
    body_path, out = sys.argv[1], Path(sys.argv[2]); go = "--go" in sys.argv
    out.mkdir(parents=True, exist_ok=True)
    log = {}
    body = Path(body_path).read_text(encoding="utf-8")
    # 1. stamp with a verified log head
    st, raw, dt = http("GET", EMEM + "/v1/log/sth"); sth = json.loads(raw)["sth"]
    d = blake3.blake3(pre_v1(b"emem.translog.sth.v1", [(1, struct.pack(">Q", sth["tree_size"])), (2, unb32(sth["root_b32"])),
                                                     (3, sth["signed_at"].encode()), (4, unb32(sth["responder_pubkey_b32"]))])).digest()
    nacl.signing.VerifyKey(unb32(sth["responder_pubkey_b32"])).verify(d, unb32(sth["signature_b32"]))  # raises if bad
    assert sth["responder_pubkey_b32"] == SIGNER, "log head not signed by the pinned responder key"
    log["sth"] = {k: sth[k] for k in ("tree_size", "root_b32", "signed_at")} | {"sig_verified": True, "ms": round(dt * 1000)}
    KIND = body.split("\n")[1].split(": ")[1]; SPEC = {"pointer.v1": POINTER_SPEC, "track.v1": "b5lmdatbymxjtttsobn2p7qshy"}[KIND]; assert "\nspec: " not in body.split("\n---\n", 1)[0]
    body = body.replace(f"emem: {KIND}\n", f"emem: {KIND}\nspec: {SPEC}\n", 1)
    body = body.replace("---\n", f"---\nafter: sth {sth['tree_size']} {sth['root_b32']} {sth['signed_at']}\n", 1)
    note = body.encode("utf-8")
    cid = b32(blake3.blake3(note).digest()[:16])
    ident = json.loads(Path(os.environ["EMEM_IDENTITY"]).read_text())
    # --flat: /<pk8>/<cid>.md like ememdemo and the homepage; the viewer's witnesses() reads the author from the
    # path segment before the filename, so a sub-folder (poster-proto/) makes it look up the wrong inbox.
    path = f"/memories/by_attester/{ident['pubkey8']}/{cid}.md" if "--flat" in sys.argv else f"/memories/by_attester/{ident['pubkey8']}/poster-proto/{cid}.md"
    (out / "note.md").write_bytes(note)
    log |= {"cid": cid, "path": path, "note_bytes": len(note), "note_blake3": b32(blake3.blake3(note).digest())}
    args = {"path": path, "file_text": body, "kind": "resource"}
    # 3. unsigned: both surfaces refuse and name the digest
    mcp = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "emem_memory_create", "arguments": args}}
    st, raw, dt = http("POST", EMEM + "/mcp", json.dumps(mcp).encode(), {"content-type": "application/json", "accept": "application/json, text/event-stream"})
    (out / "refusal_mcp.json").write_bytes(raw); log["unsigned_mcp"] = {"http": st, "ms": round(dt * 1000)}
    st, raw, dt = http("POST", EMEM + "/a2a/tasks", json.dumps({"skill": "emem_memory_create", "args": args}).encode(), {"content-type": "application/json"})
    (out / "refusal_a2a.json").write_bytes(raw); log["unsigned_a2a"] = {"http": st, "ms": round(dt * 1000)}
    for k, f in (("mcp", "refusal_mcp.json"), ("a2a", "refusal_a2a.json")):
        doc = json.loads((out / f).read_text())
        text = "".join(c.get("text", "") for c in doc["result"]["content"]) if "result" in doc else doc.get("message", "")
        det = json.loads(text.partition("\ndetails:\n")[2])
        log[f"unsigned_{k}"] |= {"code": det.get("code"), "digest_hex": det["how_to_sign"]["sign_this"]["digest_hex"]}
    local = blake3.blake3(b"emem.memory_write.v2|create|" + path.encode() + b"|" + blake3.blake3(note).digest() + b"|absent").hexdigest()
    log["local_digest_hex"] = local
    log["digests_agree"] = local == log["unsigned_mcp"]["digest_hex"] == log["unsigned_a2a"]["digest_hex"]
    if go and log["digests_agree"]:
        # 4. sign only what we composed; sign_write.py re-checks the refusal's digest against its own
        att = json.loads(subprocess.check_output(["python3", SIGN, "write", "create", path, str(out / "note.md"), "absent", str(out / "refusal_mcp.json")]))
        (out / "attester_public.json").write_text(json.dumps({"pubkey_b32": att["pubkey_b32"], "sig_b32": att["sig_b32"]}))
        st, raw, dt = http("POST", EMEM + "/a2a/tasks", json.dumps({"skill": "emem_memory_create", "args": args | {"attester": att}}).encode(), {"content-type": "application/json"})
        (out / "created_a2a.json").write_bytes(raw); log["signed_a2a"] = {"http": st, "ms": round(dt * 1000)}
    (out / "publish_log.json").write_text(json.dumps(log, indent=1))
    print(json.dumps(log, indent=1))

if __name__ == "__main__":
    main()
