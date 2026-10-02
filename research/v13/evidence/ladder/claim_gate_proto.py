"""Prototype of the claim-status gate's lexical pass (scratch only; not wired into build_v12.py).
Reads poster/src/poster.v12.html, inlines figure SVG text (matplotlib writes each label as an XML comment), and reports
every banned-word hit with no allowlist entry. Exit code = number of hits (0 = pass)."""
import re, sys, json
from pathlib import Path
POSTER = Path("/home/user/esa_poster/poster")
src = (POSTER / "src/poster.v12.html").read_text()

def fig_text(path):
    s = (POSTER / path).read_text()
    return " | ".join(x.strip() for x in re.findall(r"<!-- (.*?) -->", s, flags=re.S))

units = []   # (where, text)
body = re.sub(r"(?s)<style.*?</style>", "", src)
for m in re.finditer(r"<!--inline:([^>]+?)-->", body):
    units.append((f"fig {m.group(1)}", fig_text(m.group(1))))
body = re.sub(r"(?s)<!--.*?-->", "", body)
for i, line in enumerate(body.split("\n"), 1):
    t = re.sub(r"<[^>]+>", " ", line)
    t = re.sub(r"\s+", " ", t).strip()
    if t:
        units.append((f"html line ~{i}", t))   # line numbers shift by the stripped <style> block; we re-map below

# re-map html lines to source line numbers by searching the text in the source
def srcline(t):
    key = t[:30]
    for n, l in enumerate(src.split("\n"), 1):
        if key and key in re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", l)):
            return n
    return None

BANNED = {
    # novelty and absolutes (issue #21)
    r"\bfirst\b": "novelty", r"\bonly\b": "novelty/absolute", r"\bunique(ly)?\b": "novelty", r"\bnovel\b": "novelty",
    r"\bnever\b": "absolute", r"\balways\b": "absolute", r"\bevery\b": "universal", r"\ball\b": "universal",
    r"\bany\b": "universal",
    # truth and guarantee words (issues #13, #17, #29)
    r"\btrue\b|\btruth\b": "truth", r"\bguarantee[sd]?\b": "guarantee", r"\bprove[sn]?\b|\bproof\b": "proof",
    r"\bimmutable\b|\btamper-?proof\b|\btrustless\b|\bsecure[sd]?\b": "absolute security",
    r"\bdecides?\b|\barbiter\b": "agency",
    # verification without a layer (issue #17)
    r"\bverif(y|ied|ies|iable|ication)\b": "verified-without-layer",
    # CID wording (issue #12)
    r"hash of (its|the) (bytes|pixel|file|scene|image)": "cid-is-not-a-source-hash",
    r"signs? the (one )?value": "facts carry no signature",
    r"Ed25519\}\(\\,\\mathrm\{BLAKE3\}\(\\mathrm\{body\}\)": "facts carry no signature",
    r"equal values give equal": "signer and signed_at are hashed",
    # SAT-042 status (issue #14, #21)
    r"\bsatellite could prove\b|\bspacecraft\b|\bin orbit\b|\bon ?board\b|\bdownlink\b|\boperational\b": "spacecraft status",
    # independence (defects 1, 30)
    r"\bindependent (operator|witness)": "independence",
}
LAYER = re.compile(r"\bL[0-5]\b")
ALLOW = [  # (pattern, sentence substring, reason)
    (r"\bspacecraft\b", "No spacecraft is enrolled", "negation, status statement"),
    (r"\bspacecraft\b", "not a spacecraft", "negation, status statement"),
    (r"\btrue\b|\btruth\b", "does not make a value true", "negation; boundary statement"),
]
hits = []
for where, t in units:
    for pat, why in BANNED.items():
        for m in re.finditer(pat, t, flags=re.I):
            if why == "verified-without-layer" and LAYER.search(t):
                continue
            if why == "universal" and re.match(r"\s+(\d[\d,]*|one|two|three|four|five|six|seven|eight|nine|ten)\b", t[m.end():]):
                continue   # a quantifier with its denominator ("all 15", "all three") is a counted claim, checked by the number gate
            if any(re.search(ap, m.group(0), flags=re.I) and s in t for ap, s, _ in ALLOW):
                continue
            ctx = t[max(0, m.start() - 50): m.end() + 50]
            line = srcline(t) if where.startswith("html") else None
            hits.append({"where": where if line is None else f"poster.v12.html:{line}", "rule": why,
                         "match": m.group(0), "context": ctx})
for h in hits:
    print(f"{h['where']:<34} {h['rule']:<28} [{h['match']}] …{h['context']}…")
print(f"\n{len(hits)} hits", file=sys.stderr)
json.dump(hits, open(Path(__file__).with_suffix(".out.json"), "w"), indent=1)
sys.exit(min(len(hits), 255))
