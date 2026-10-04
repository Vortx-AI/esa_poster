"""Write the pointer.v1 note body for a committed print PDF, offline (the first step of ememifying the board).
    python research/repro/v13/track/pointer_body.py <commit> [out.md]
Reproduces the published v13.0 body byte-for-byte for e66c3ba (root z6suryjv...), so the same rule holds for later prints.
Publishing the body and signing it needs emem.dev and the poster key; see poster/README.md."""
import base64, struct, subprocess, sys, pathlib
import blake3
commit = sys.argv[1]
pdf = "poster/emem-poster-A0.pdf"
if "--pdf" in sys.argv:   # a print variant, e.g. --pdf poster/emem-poster-A0-300of300.pdf
    pdf = sys.argv[sys.argv.index("--pdf") + 1]
    del sys.argv[sys.argv.index("--pdf"):sys.argv.index("--pdf") + 2]
tag = pathlib.Path(pdf).stem.replace("emem-poster-A0", "")
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else pathlib.Path(__file__).with_name(f"board_body_{commit[:7]}{tag}.md"))
raw = subprocess.run(["git", "show", f"{commit}:{pdf}"], capture_output=True, check=True).stdout
b32 = lambda b: base64.b32encode(b).decode().lower().rstrip("=")
H = lambda b: blake3.blake3(b).digest()
assert len(raw) <= 4 << 20, "one 4 MiB range expected"
h = H(raw)
root = b32(H(b"" + struct.pack(">Q", 0) + struct.pack(">Q", len(raw)) + h))
mb = f"{len(raw) / 1e6:.1f}"
body = f"""---
emem: pointer.v1
source: https://raw.githubusercontent.com/Vortx-AI/esa_poster/{commit}/{pdf}
bytes: {len(raw)}
etag: not exposed
kind: file
chunks: 1 of 1 hashed
root: {root}
hash: blake3-256 of each chunk's bytes
order: defaults, then by blake3(label without type or shape)
---

# {pathlib.Path(pdf).name}

> file at raw.githubusercontent.com, {mb} MB.

> The printed EMEM poster for Agentic AI for Earth Observation, Berlin, 19 Oct 2026 (A0, PDF as sent to print, emem_poster commit {commit[:7]}). Every record it rests on is a step of the track that cites this note.

- 1 ranges of 4 MiB
- 1 of 1 chunks hashed; more can be hashed later, in a fixed order, without re-reading these

## Chunks

| what | url (· is the source) | offset | length | blake3 |
|---|---|---|---|---|
| bytes 0… | · | 0 | {len(raw)} | {b32(h)} |
"""
out.write_text(body)
print(out, len(raw), root)
