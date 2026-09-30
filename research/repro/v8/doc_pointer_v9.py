"""Build pointer.v1 notes whose rows are exact line ranges of public emem docs at a pinned commit.
Each row's bytes can be range-read from raw.githubusercontent.com and hashed with stock blake3.
    python doc_pointer_v9.py OUTDIR      (reads the emem clone; writes one body per doc + rows.json)"""
import subprocess, sys, json, struct, base64, pathlib, urllib.request
import blake3
REPO = "/home/user/vortx-ai/emem"; COMMIT = "18adb67895d33c8b64d3b091a90af1f708315123"
b32 = lambda b: base64.b32encode(b).decode().lower().rstrip("=")
H = lambda b: blake3.blake3(b).digest()
leaf = lambda url, off, ln, h: H(url.encode() + struct.pack(">Q", off) + struct.pack(">Q", ln) + h)
def merkle(ls):
    while len(ls) > 1:
        nx = [H(ls[i] + ls[i + 1]) for i in range(0, len(ls) - 1, 2)]
        if len(ls) % 2: nx.append(ls[-1])
        ls = nx
    return ls[0]
CITES = {
 "CHANGELOG.md": ("the foundation-model encoders retired", [
    ("Clay v1.5, Prithvi-EO-2.0, Galileo, JEPA-v2 removed; old facts still verify", 77, 77)]),
 "docs/memory.md": ("the encoders retired, TESSERA frozen", [
    ("encoders removed from the code; geotessera retired on emem.dev", 43, 48)]),
 "docs/how-emem-compares.md": ("the architecture comparison and the safety result", [
    ("exact vs confidently wrong: citation 99.2 %, dense 4/142, BM25 16/16", 79, 96),
    ("on retrieval failure: abstained 74/96, confident wrong 93/96", 102, 109)]),
 "README.md": ("the substrate rule and the device gate", [
    ("open archives are recomputable; the device gate admits no real hardware yet", 237, 237)]),
}
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); meta = {}
for path, (title, cites) in CITES.items():
    raw = subprocess.run(["git", "-C", REPO, "show", f"{COMMIT}:{path}"], capture_output=True, check=True).stdout
    starts = [0] + [i + 1 for i, c in enumerate(raw) if c == 10]
    url = f"https://raw.githubusercontent.com/Vortx-AI/emem/{COMMIT}/{path}"
    rows, quotes = [], []
    for label, a, b in cites:
        off, end = starts[a - 1], starts[b]
        chunk = raw[off:end]
        live = urllib.request.urlopen(urllib.request.Request(url, headers={"Range": f"bytes={off}-{end-1}"}), timeout=60).read()
        assert H(live) == H(chunk), (path, a, b)
        rows.append((f"lines {a}–{b} · {label}" if a != b else f"line {a} · {label}", off, end - off, b32(H(chunk))))
        q = chunk.decode().replace("|", "/").rstrip("\n").split("\n")
        quotes.append(f"### lines {a}–{b}\n\n" + "\n".join("> " + l for l in q))
    root = b32(merkle([leaf("", o, l, base64.b32decode(h.upper() + "=" * ((8 - len(h) % 8) % 8))) for _, o, l, h in rows]))
    name = path.split("/")[-1]
    body = "\n".join([
        "---", "emem: pointer.v1", f"source: {url}", f"bytes: {len(raw)}", "etag: not exposed",
        "kind: text (line ranges)", f"chunks: {len(rows)} of {len(raw.splitlines())} lines hashed", f"root: {root}",
        "hash: blake3-256 of each chunk's bytes", "order: as cited", "---", "",
        f"# {name} at Vortx-AI/emem {COMMIT[:7]}", "",
        f"> {title}. The file stays on GitHub at a pinned commit; each row below names exact bytes of it, "
        "which anyone can range-read and hash. Cited by the EMEM poster at Agentic AI for Earth Observation, Berlin, 19 Oct 2026.", "",
        *quotes, "", "## Chunks", "",
        "| what | url (· is the source) | offset | length | blake3 | stats |",
        "|---|---|---|---|---|---|",
        *[f"| {w} | · | {o} | {l} | {h} |  |" for w, o, l, h in rows], ""])
    (out / f"{name}.body.md").write_text(body)
    meta[path] = dict(url=url, root=root, rows=[dict(what=w, offset=o, length=l, blake3=h) for w, o, l, h in rows])
    print(path, "rows", len(rows), "root", root[:12])
json.dump(meta, open(out / "rows.json", "w"), indent=1)
