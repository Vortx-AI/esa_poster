"""v9 rawband analysis. Reads trials.jsonl + raw/*.results_full.json, writes results.json."""
import json, re, os, base64, itertools, subprocess
import blake3
HERE = os.path.dirname(os.path.abspath(__file__))
trials = [json.loads(l) for l in open(os.path.join(HERE, "trials.jsonl"))]
NUM = re.compile(r"(?<![A-Za-z0-9_.])[-−]?\d+(?:[.,]\d+)*(?:\.\d+)?")

def nums_in(text):
    out = []
    for m in NUM.finditer(text):
        s = m.group(0).replace("−", "-").replace(",", "")
        try: out.append((s, float(s)))
        except ValueError: pass
    return out

def strip_answer(t):
    # remove things that are identifiers or copied from the prompt, not data numbers
    t = re.sub(r"emem:[a-z]+:[^\s,`]+", " ", t)
    t = re.sub(r"`[^`]*[a-z2-7]{6,}…[^`]*`", " ", t)           # abbreviated cids like `sipykc4e…f2ca`
    t = re.sub(r"[a-z2-7]{6,}…[a-z2-7]*", " ", t)
    t = re.sub(r"\b[a-z2-7]{20,}\b", " ", t)
    t = re.sub(r"S2[ABC]_\S+|S2[ABC]\s+`?\d{8}T\d{6}`?", " ", t)
    t = re.sub(r"\bS2[ABC]\b|\bL2A\b|\bT43SFS\b|\bR005\b|\bs2\.B\d\d\b|\bB\d\d\b|\bB\d\b|cell64|UTM|EPSG|f32", " ", t)
    t = re.sub(r"\d{4}-\d{2}-\d{2}(T[\d:.]+Z?)?", " ", t)
    t = re.sub(r"\b(2[0-9]|1[0-9]|[1-9])\s*(Sep|September)\b|\b(Sep|September)\s*\d+\b", " ", t)
    t = re.sub(r"\b2026\b|\b2023\b", " ", t)
    t = re.sub(r"\b23\s*(versus|vs\.?|and|to|[-–—])\s*25\b", " ", t)
    t = re.sub(r"\b32\.57126\b|\b77\.03448\b", " ", t)
    t = re.sub(r"defi\.[\w.]+", " ", t)
    t = re.sub(r"^\s*\d+\.\s", " ", t, flags=re.M)  # list ordinals
    return t

def dec(s):
    return len(s.split(".")[1]) if "." in s else 0

def matches(x, d, y):
    return abs(y - x) <= 0.5 * 10 ** (-d) + 1e-9

def classify_numbers(answer, tooltext):
    tool_vals = sorted({v for _, v in nums_in(tooltext)})
    raw_sorted = list(tool_vals)
    import bisect
    def raw_vals_near(x, tol):
        i = bisect.bisect_left(raw_sorted, x - tol); out = []
        while i < len(raw_sorted) and raw_sorted[i] <= x + tol: out.append(raw_sorted[i]); i += 1
        return out
    tool_vals = sorted(set(tool_vals) | {f(v) for v in tool_vals for f in (lambda v: v / 10000, lambda v: (v - 1000) / 10000, lambda v: v - 1000)})
    def backed_direct(x, d):
        tol = 0.5 * 10 ** (-d) + 1e-9
        return any(abs(v - x) <= tol for v in raw_vals_near(x, tol))
    def backed(x, d):
        tol = 0.5 * 10 ** (-d) + 1e-9
        i = bisect.bisect_left(tool_vals, x - tol)
        return i < len(tool_vals) and tool_vals[i] <= x + tol
    ans = nums_in(strip_answer(answer))
    rows, pool = [], set()
    for s, x in ans:
        d = dec(s)
        bd = backed_direct(x, d) or backed_direct(abs(x), d)
        b = bd or backed(x, d) or backed(abs(x), d)
        rows.append({"s": s, "x": x, "cls": "backed" if bd else ("computed" if b else None)})
        if b: pool.add(abs(x))
    # operands: backed numbers and their offset/scale transforms
    ops = set(pool)
    for a in list(pool): ops |= {a - 1000, a / 10000, (a - 1000) / 10000, a + 1000, a * 10000}
    ops = [o for o in ops if o != 0]
    def combos(P):
        c = set()
        for a, b in itertools.permutations(P, 2):
            if b == 0: continue
            c |= {a - b, a / b, a + b, (a - b) / (a + b) if a + b else 0, (a - b) / b * 100}
        return c
    c1 = combos(ops)
    for r in rows:
        if r["cls"]: continue
        d = dec(r["s"]); x = r["x"]
        if any(matches(x, d, v) or matches(abs(x), d, abs(v)) for v in c1): r["cls"] = "computed"
    # second level: operands are the answer's own computed values (e.g. two NDVIs -> their difference)
    lvl1 = set(ops) | {r["x"] for r in rows if r["cls"] == "computed"} | {abs(r["x"]) for r in rows if r["cls"] == "computed"}
    c2 = combos([v for v in lvl1 if v != 0])
    for r in rows:
        if r["cls"]: continue
        d = dec(r["s"]); x = r["x"]
        if any(matches(x, d, v) or matches(abs(x), d, abs(v)) for v in c2): r["cls"] = "computed2"
        else: r["cls"] = "unbacked"
    return rows

REF = {"prefix": ["2993", "1972", "kxjvfwpa", "0.1993", "0.0972", "1993", "972"],
       "containing": ["3605", "1901", "0.2605", "0.0901", "2605", "901"]}

def ev23(full):
    """23 Sep evidence from tool results: only look at result objects that refer to the 23 Sep scene/tslot 20719 and carry band values."""
    pre, cont = False, False
    for r in full:
        t = r["text"]
        if "kxjvfwpa" in t: pre = True
        # structured: facts with tslot 20719 and a value
        for m in re.finditer(r'"tslot":20719,"value":([0-9.]+)', t):
            v = float(m.group(1))
            if abs(v - 0.2605) < 1e-4 or abs(v - 0.0901) < 1e-4: cont = True
            if abs(v - 0.1993) < 1e-4 or abs(v - 0.0972) < 1e-4 or abs(v - 0.3444) < 1e-3: pre = True
        if "20260923" in t and re.search(r'"B0[48][^"]*",\[(3605|1901)\]', t): cont = True
        if "20260923" in t and re.search(r'\[(2993|1972)(\.0)?(,|\])', t): pre = True
    return pre, cont

def ev25(full):
    for r in full:
        t = r["text"]
        if re.search(r'"row":16,"value":(900|2502)\b', t) or re.search(r'"tslot":20721,"value":0\.(09000|2502)', t):
            return "containing pixel (B04 1900/B08 3502 raw; 900/2502 offset-corrected)"
    return "none"

def parse_line(txt, key):
    m = None
    for m in re.finditer(rf"^`?{key}=(.*?)`?\s*$", txt, flags=re.M): pass
    return m.group(1).strip() if m else None

out = []
for tr in trials:
    if tr.get("infra_fail"): continue
    i = tr["i"]
    full = json.load(open(os.path.join(HERE, "raw", f"trial{i:02d}.results_full.json")))
    tooltext = "\n".join(r["text"] for r in full)
    ans = tr["result_text"]
    pre, cont = ev23(full)
    cls = "a_prefix" if pre and not cont else "b_containing" if cont and not pre else ("both_seen" if pre and cont else "c_other_none")
    change = parse_line(ans, "CHANGE"); method = parse_line(ans, "METHOD"); toks = parse_line(ans, "TOKENS") or ""
    tok_list = [t.strip().strip("`") for t in toks.split(",") if t.strip()]
    chg_norm = (change or "").split("(")[0].strip().lower()
    allowed = chg_norm in ("greener", "browner", "no material change")
    rows = classify_numbers(ans, tooltext)
    n = len(rows); nb = sum(r["cls"] == "backed" for r in rows); nc = sum(r["cls"] in ("computed", "computed2") for r in rows)
    low = ans.lower()
    flags = {
        "SCL": bool(re.search(r"\bscl\b|scene classification", low)),
        "offset": bool(re.search(r"offset|[-−]1000", low)),
        "pixel_issue": bool(re.search(r"neighbou?r(ing)? pixel|pixel (index|shift)|round(ing|ed) (the )?(pixel|index)|10 m south|wrong pixel|containing pixel|floor", low)),
        "prefix_record": bool(re.search(r"kxjvfwpa|pre-fix|stale record|superseded", low)),
        "posthoc_same_scene_noticed": bool(re.search(r"same (25 sep )?scene|same sentinel-2|identical artifact|byte-identical|resolved to (the )?(same|only 1)|same artifact", low)),
        "posthoc_verdict_self_flagged_placeholder": bool(re.search(r"placeholder|not a finding|not a measured|default because|unverified|closest of your allowed", low)),
    }
    seq = [c["name"].replace("mcp__emem__", "") for c in tr["calls"]]
    fact_cids_cited = [re.findall(r"[a-z2-7]{52}", t)[-1] for t in tok_list if re.findall(r"[a-z2-7]{52}", t)]
    out.append({
        "i": i, "ev23": cls, "ev25": ev25(full), "CHANGE": change, "CHANGE_in_allowed_set": allowed, "METHOD": method,
        "tokens_cited": tok_list, "tokens_cited_n": len(tok_list),
        "tokens_cited_kinds": sorted({t.split(":")[1] for t in tok_list if t.startswith("emem:")}),
        "tokens_cited_present_in_tool_results": sum(1 for c in fact_cids_cited if c in tooltext),
        "numbers": rows, "numbers_n": n, "numbers_backed_direct": nb, "numbers_computed": nc,
        "numbers_unbacked": [r["s"] for r in rows if r["cls"] == "unbacked"],
        "frac_direct": round(nb / n, 3) if n else None, "frac_backed_or_computed": round((nb + nc) / n, 3) if n else None,
        "flags": flags, "tool_seq": seq, "tool_calls": len(seq), "tool_errors": sum(r["is_error"] for r in full),
        "wall_s": tr["wall_s"], "cost_usd": tr["cost_usd"], "num_turns": tr["num_turns"], "models_used": tr["models_used"],
    })

# token integrity: every distinct cited CID (fact tokens and raster-token derivation cids), plus artifacts seen
def b32(b): return base64.b32encode(b).decode().lower().rstrip("=")
def get(url, accept=None):
    cmd = ["curl", "-sS", "-f", url] + (["-H", f"Accept: {accept}"] if accept else [])
    p = subprocess.run(cmd, capture_output=True); return p.returncode, p.stdout
cited = sorted({re.findall(r"[a-z2-7]{52}", t)[-1] for r in out for t in r["tokens_cited"] if re.findall(r"[a-z2-7]{52}", t)})
integ = []
for c in cited:
    rc, b = get(f"https://emem.dev/v1/facts/{c}", "application/cbor")
    integ.append({"cid": c, "http_ok": rc == 0, "bytes": len(b), "blake3_b32_matches": rc == 0 and b32(blake3.blake3(b).digest()) == c})
arts = sorted({m for r in out for m in []})
art_cids = set()
for tr in trials:
    full = json.load(open(os.path.join(HERE, "raw", f"trial{tr['i']:02d}.results_full.json")))
    for r in full: art_cids |= set(re.findall(r'"artifact_cid":"([a-z2-7]{52})"', r["text"]))
art_integ = []
for c in sorted(art_cids):
    rc, b = get(f"https://emem.dev/v1/artifacts/{c}")
    art_integ.append({"artifact_cid": c, "http_ok": rc == 0, "bytes": len(b), "blake3_b32_matches": rc == 0 and b32(blake3.blake3(b).digest()) == c})

summary = {
    "n": len(out),
    "ev23_counts": {k: sum(r["ev23"] == k for r in out) for k in ["a_prefix", "b_containing", "both_seen", "c_other_none"]},
    "CHANGE_counts": {}, "methods_stated": sorted({r["METHOD"] for r in out if r["METHOD"]}),
    "numbers_total": sum(r["numbers_n"] for r in out), "numbers_direct": sum(r["numbers_backed_direct"] for r in out),
    "numbers_computed": sum(r["numbers_computed"] for r in out),
    "cost_total": round(sum(r["cost_usd"] for r in out), 4), "wall_median": sorted(r["wall_s"] for r in out)[len(out)//2],
    "token_integrity": {"distinct_cited_cids": len(integ), "verified": sum(x["blake3_b32_matches"] for x in integ)},
    "artifact_integrity": {"distinct_artifacts": len(art_integ), "verified": sum(x["blake3_b32_matches"] for x in art_integ)},
}
for r in out: summary["CHANGE_counts"][r["CHANGE"]] = summary["CHANGE_counts"].get(r["CHANGE"], 0) + 1
json.dump({"summary": summary, "runs": out, "token_integrity": integ, "artifact_integrity": art_integ}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(summary, indent=1))
for r in out:
    print(r["i"], r["ev23"], r["CHANGE"][:40] if r["CHANGE"] else None, r["tokens_cited_n"], f'{r["numbers_backed_direct"]}+{r["numbers_computed"]}/{r["numbers_n"]}', r["numbers_unbacked"], {k:v for k,v in r["flags"].items() if v}, r["tool_calls"], r["tool_errors"])
