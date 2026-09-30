"""Build pointer.v1 notes whose rows are exact line ranges of public emem docs at a pinned commit.
Each row's bytes can be range-read from raw.githubusercontent.com and hashed with stock blake3.
    python doc_pointer.py OUTDIR      (reads the emem clone; writes one body per doc + rows.json)"""
import subprocess, sys, json, struct, base64, pathlib, urllib.request
import blake3
REPO = "/home/user/vortx-ai/emem"; COMMIT = "213e2738d508a4e084cd0beef329598950f01bf0"
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
 "docs/paper-section-statistics-and-threats.md": ("pre-registered agreement vs accuracy test", [
    ("Fisher table: control 72/72, compaction 0/72 with 3/36 agreeing, p = 0.035", 85, 89),
    ("six scoring bugs across two scorers", 163, 166)]),
 "docs/collaboration-log.md": ("measured agent handoff experiments", [
    ("paraphrase trap: token WATER, prose SKIP, one NDVI fact", 9603, 9612),
    ("handoff n=20 per arm: bundle 20, BM25 20, dense 8, prose 2", 27329, 27336)]),
 "CHANGELOG.md": ("the pixel-rounding fix", [
    ("point reads took the south-east neighbour from the first commit; fixed", 68, 68)]),
 "docs/how-emem-compares.md": ("token and bundle sizes, and the authors' scorecard", [
    ("token vs bundle size", 115, 120),
    ("scorecard: what is supported, refuted, not tested", 266, 278)]),
 "docs/whitepaper-v3.md": ("the record and the withdrawals", [
    ("agents on at least five model families", 118, 137),
    ("nineteen withdrawals", 241, 246)]),
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
