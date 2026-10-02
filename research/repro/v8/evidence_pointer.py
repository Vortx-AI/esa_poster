"""pointer.v1 over the v8 measurement files at a pinned commit of the public esa_poster repo (one whole-file row each)."""
import sys, struct, base64, urllib.request, blake3
SHA = sys.argv[1]
FILES = [("15-link trace output, 30 Sep", "research/repro/v8/trace_fact_output.txt"),
         ("token gate: 10 facts re-hashed", "research/repro/v8/inventory.json"),
         ("ten client paths, one record", "research/repro/data/v8/crossruntime_table.json"),
         ("two-LLM handoff pre-registration", "research/repro/data/v8/prereg.md"),
         ("two-LLM handoff results", "research/repro/data/v8/results.json"),
         ("pixel-rounding audit, 200 records", "research/repro/data/v8/prevalence_summary.json"),
         ("pixel windows before and after the fix", "research/repro/data/v8/pixel_windows.json"),
         ("raw-band run pre-registration", "research/repro/data/v9/rawband/prereg.md"),
         ("raw-band run results", "research/repro/data/v9/rawband/results.json"),
         ("raw-band run, per-trial records", "research/repro/data/v9/rawband/trials.jsonl"),
         ("defects found in the audit", "research/do_not_use/05_DEFECTS_FOUND_IN_AUDIT.md"),
         ("the algorithms, as coded at emem 18adb67", "research/repro/v10/algorithms.md"),
         ("13 products at the Keylong cell, re-hashed", "research/repro/data/v11/cell_products.json"),
         ("an ask answer with its reasoning stages", "research/repro/data/v11/ask_keylong.json"),
         ("recompute every emem:state address", "research/repro/data/v11/recompute_state.py")]
b32 = lambda b: base64.b32encode(b).decode().lower().rstrip("=")
H = lambda b: blake3.blake3(b).digest()
rows, leaves = [], []
for what, path in FILES:
    url = f"https://raw.githubusercontent.com/Vortx-AI/esa_poster/{SHA}/{path}"
    b = urllib.request.urlopen(url, timeout=60).read(); h = H(b)
    rows.append(f"| {what} | {url} | 0 | {len(b)} | {b32(h)} |  |")
    leaves.append(H(url.encode() + struct.pack(">Q", 0) + struct.pack(">Q", len(b)) + h))
while len(leaves) > 1:
    nx = [H(leaves[i] + leaves[i + 1]) for i in range(0, len(leaves) - 1, 2)]
    if len(leaves) % 2: nx.append(leaves[-1])
    leaves = nx
total = sum(int(r.split("|")[4]) for r in rows)
print("\n".join(["---", "emem: pointer.v1", f"source: https://github.com/Vortx-AI/esa_poster/tree/{SHA}/research/repro", f"bytes: {total}",
    "etag: not exposed", "kind: files (whole-file rows)", f"chunks: {len(rows)} of {len(rows)} hashed", f"root: {b32(leaves[0])}",
    "hash: blake3-256 of each chunk's bytes", "order: as listed", "---", "", "# EMEM poster v8: the measurements behind the board", "",
    f"> The files stay in the public Vortx-AI/esa_poster repository at commit {SHA[:7]}; each row names one whole file by URL, size and BLAKE3. Scripts that produced them sit beside them.", "",
    "## Chunks", "", "| what | url (· is the source) | offset | length | blake3 | stats |", "|---|---|---|---|---|---|", *rows, ""]))
