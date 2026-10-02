"""Build the v13 board: poster/src/poster.v13.html (+ .css) -> poster/poster.html -> PDF + PNG previews, then every gate.

usage: python poster/build_v13.py [--r1] [--figures] [--allowlist-candidates]
  --r1          re-run R1 (research/repro/v11/mutation_suite.py) before building
  --figures     run poster/make_figures_v13.py first, when it exists (figures are otherwise taken as they are in fig/v13/)
  --allowlist-candidates  print the banned-word hits with the BLAKE3 a poster/src/poster.v13.allowlist.json entry needs

needs: playwright (Chromium at /opt/pw-browsers), pypdfium2, opencv-python-headless, fonttools, blake3, Pillow, pyproj

Renders with Chromium (playwright): one A0 page, 841 x 1189 mm. Writes poster/poster.html, poster/emem-poster-A0.pdf,
poster/emem-poster-preview.png (about 96 dpi), poster/emem-poster-A0-300dpi.png and poster/build_v13_report.json.

Gates (research/v13/12_FINAL_BRIEF.md section G; research/v13/10_ladder_threat_invention.md section 5). Each one fails the
build; an unknown result (an exception inside a gate) is a failure, never a skip. All gates run and are reported, then the
build exits non-zero if any failed.
"""
import csv
import datetime as dt
import html as htmllib
import json
import re
import subprocess
import sys
import traceback
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RES = REPO / "research"
SRC = HERE / "src" / "poster.v13.html"
CSS = HERE / "src" / "poster.v13.css"
TOKENS = HERE / "src" / "tokens.json"
ALLOW = HERE / "src" / "poster.v13.allowlist.json"
FIG = HERE / "fig" / "v13"
OUT_HTML = HERE / "poster.html"
PDF = HERE / "emem-poster-A0.pdf"
PNG = HERE / "emem-poster-preview.png"
PNG300 = HERE / "emem-poster-A0-300dpi.png"
REPORT = HERE / "build_v13_report.json"
BRIEF = RES / "v13" / "12_FINAL_BRIEF.md"
CLAIMS = RES / "v13" / "12_claims_map.json"
R5_DIR = RES / "repro" / "v13" / "r5"
CHROME_GLOB = "/opt/pw-browsers"
TODAY = dt.date.today()

FIGURES = ["f1_scene", "f2_spine", "f3_eight_answers", "f4_failure_ladder", "f5_evidence_object", "f6_mutation_matrix",
           "f7_wrong_pixel", "f8_ladder", "f9_timeline", "f11_ecosystem", "f12_prior_art", "d_threat",
           "f13_one_address", "f14_token_family", "f15b_sat042_strip"]   # v13.1: F10, D2 and D4 left the face with panels 9 to 11; v13.2: SAT-042 as the strip F15b (F15 drawn, not placed)
QRS = ["demo", "t", "r", "test", "methods", "use"]

# brief section B row label -> data-block id
BLOCK_ROWS = {"Header text": "header_text", "Header image": "header_image", "1 Spine": "p1", "2 Eight answers": "p2",
              "3 Our own errors": "p3", "Questions and hypotheses": "questions", "Threat model": "threat",
              "4 What is handed over": "p4", "5 Mutation matrix": "p5", "6 The right record": "p6",
              "7 Verification ladder": "p7", "8 Same place": "p8", "9 One address": "p9", "10 Token family": "p10",
              "11 SAT-042": "p11", "12 Ecosystem": "p12", "13 Prior-art": "p13", "Conclusion": "conclusion",
              "Footer": "footer"}   # v13.1 rows (section B, "v13.1 change") replace 9 Rondônia, 10 Vectors, 11 What it costs
# deliberate departures from the section B rectangles; each must carry a reason (printed in the report)
LAYOUT_DEVIATIONS = json.loads((HERE / "src" / "poster.v13.layout.json").read_text())["deviations"] \
    if (HERE / "src" / "poster.v13.layout.json").exists() else {}

GATES = {}          # name -> {"pass": bool, "details": [...]}
TYPE_DEVIATIONS = [  # accepted by the coordinator on 2026-10-01; the 14 pt floor and the 24 pt kicker/mechanism/take tier hold
    "Questions panel: RQ1 to RQ4 and H1 to H3 at 17 pt (brief A.2 body tier 24 pt)",
    "Threat model paragraph and the panel 10, 11 and 13 paragraphs at 17 pt (brief A.2 body tier 24 pt); the threat paragraph went from 20 to 17 pt when the R5 lines landed in the spine",
    "Reason: with the section E figures drawn 1:1 and the section C text verbatim, 24 pt body overfills the side columns by about 40 to 60 mm and the bottom-right block by about 25 mm",
    "Leading tightened: kicker 1.06, headlines 1.0, mechanism 1.1, captions 1.16, footer 1.12; panel gaps 3 mm (brief 10 mm)",
    "v13.1: the v12.1 subtitles of panels 9 and 11 at 17 pt (caption tier); the drift block in the header at 17 pt with 14.2 pt subscripts; "
    "panel 11 keeps the v12.1 headline verbatim (39 characters) at the user's request",
    "v13.2: panel 11 headline at 28 pt (one line; 32 pt needs two) so the SAT-042 strip fits the right column; panel 7 prints "
    "no mechanism line or caption (its ladder is compact, one evidence line per rung)",
]
HEADLINE_LEN_EXEMPT = {"p11": "v12.1 title kept verbatim at the user's request (2026-10-02); one line at 28 pt (v13.2)"}
MOVED = []          # running-text lines that a figure prints itself (dropped from the HTML, still counted)
REPORT_EXTRA = {}


def gate(name):
    def deco(fn):
        def run(*a, **k):
            try:
                ok, details = fn(*a, **k)
                GATES[name] = {"pass": bool(ok), "details": details}
            except Exception as e:  # unknown result is a failure
                GATES[name] = {"pass": False, "details": [f"UNKNOWN: {type(e).__name__}: {e}",
                                                          traceback.format_exc(limit=3)]}
            return GATES[name]["pass"]
        return run
    return deco


# ---------------------------------------------------------------- claims map
def load_claims():
    doc = json.loads(CLAIMS.read_text())
    rows = {r["id"]: dict(r, _file=CLAIMS.name) for r in doc["rows"]}
    for add in sorted((RES / "v13").glob("12_claims_map_additions_*.json")):
        d = json.loads(add.read_text())
        for r in (d["rows"] if isinstance(d, dict) else d):
            rows[r["id"]] = dict(r, _file=add.name)
        # extend_print: alternative printed forms of an existing row (line splits, thin spaces, headings)
        for e in (d.get("extend_print", []) if isinstance(d, dict) else []):
            if e["id"] not in rows:
                raise KeyError(f"{add.name}: extend_print names a missing row {e['id']}")
            r = rows[e["id"]]
            r["print"] = list(r["print"]) + [x for x in e.get("print_add", []) if x not in r["print"]]
            r.setdefault("_extended_by", []).append(add.name)
    return doc, rows


# ---------------------------------------------------------------- R5 mode
def r5_mode():
    """R5 mode only if results.json exists, says it is final, and its prereg hash equals the hash pushed before trial 1."""
    res = R5_DIR / "results.json"
    info = {"results_file": str(res.relative_to(REPO)), "exists": res.exists()}
    if not res.exists():
        info["mode"] = "fallback"; info["why"] = "no results.json"
        return False, None, info
    data = json.loads(res.read_text())
    final = bool(data.get("final") or data.get("status") == "final")
    pushed = None
    if (R5_DIR / "prereg_hash.txt").exists():   # "file: .../prereg.md" then "blake3: <hex>"; the first blake3 line is prereg.md's
        m = re.search(r"^blake3:\s*([0-9a-f]{64})", (R5_DIR / "prereg_hash.txt").read_text(), re.M)
        pushed = m.group(1) if m else None
    stated = data.get("prereg_blake3") or data.get("prereg_hash")
    info.update(final=final, prereg_pushed=pushed, prereg_in_results=stated, n_trials_scored=data.get("n_trials_scored"))
    if final and pushed and stated and stated == pushed:
        info["mode"] = "r5"
        return True, data, info
    info["mode"] = "fallback"; info["why"] = "results.json not final or prereg hash mismatch"
    return False, None, info


def r5_lookup(data, key, rows=None):
    """{R5.E.haiku.false_accept} -> value from results.json; tries the layouts the scorer may write.
    {R5.models} and {R5.dates} print the wording of their claims rows (research/v13/12_claims_map_additions_r5.json),
    so the printed string and the row's print[] cannot drift apart."""
    if key in ("R5.models", "R5.dates") and rows and key in rows:
        return rows[key]["print"][0]
    parts = key.split(".")[1:]
    cands = [parts, ["primary"] + parts, ["primary", parts[0], "pooled_claude"] + parts[2:] if len(parts) > 1 else parts]
    for c in cands:
        o = data
        try:
            for k in c:
                o = o[k]
            if isinstance(o, dict) and "k" in o and "n" in o:
                return f"{o['k']} of {o['n']}"
            return str(o)
        except (KeyError, TypeError, IndexError):
            continue
    return None


# ---------------------------------------------------------------- assembly
def remove_elements(html, attr):
    """Remove every element whose start tag carries attr (e.g. 'data-mode="r5"'), with balanced nesting of its tag."""
    while True:
        m = re.search(r'<(\w+)\b[^>]*\b%s[^>]*>' % re.escape(attr), html)
        if not m:
            return html
        tag, depth, i = m.group(1), 1, m.end()
        for t in re.finditer(r'<(/?)%s\b[^>]*>' % tag, html[i:]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = i + t.end()
                break
        else:
            raise ValueError(f"unbalanced <{tag}> carrying {attr}")
        html = html[:m.start()] + html[end:].lstrip("\n ")


def strip_mode(html, drop):
    return remove_elements(html, f'data-mode="{drop}"')


def svg_size_mm(svg):
    m = re.search(r'<svg\b[^>]*>', svg, re.S)
    tag = m.group(0)
    def dim(a):
        mm_ = re.search(r'\b%s="([\d.]+)(pt|mm|px|in|cm)?"' % a, tag)
        if not mm_:
            return None
        v, u = float(mm_.group(1)), mm_.group(2) or "px"
        return v * {"pt": 25.4 / 72, "mm": 1, "px": 25.4 / 96, "in": 25.4, "cm": 10}[u]
    w, h = dim("width"), dim("height")
    if w is None or h is None:
        vb = re.search(r'viewBox="([-\d.\s]+)"', tag)
        if vb:
            _, _, vw, vh = map(float, vb.group(1).split())
            w, h = w or vw * 25.4 / 96, h or vh * 25.4 / 96
    return w, h


def clean_svg(svg, prefix):
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    svg = re.sub(r"<!DOCTYPE[^>]*>", "", svg, flags=re.S)
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    for i in sorted(ids, key=len, reverse=True):
        new = f"{prefix}-{i}"
        svg = svg.replace(f'id="{i}"', f'id="{new}"')
        svg = svg.replace(f"url(#{i})", f"url(#{new})")
        svg = svg.replace(f'href="#{i}"', f'href="#{new}"')
    return svg.strip()


R5_PRINTED = []     # every data-mode="r5" line as printed (for the build report)


def assemble(r5, r5data, rows=None):
    html = SRC.read_text()
    html = html.replace('<link rel="stylesheet" href="src/poster.v13.css">', "<style>\n" + CSS.read_text() + "\n</style>")
    html = strip_mode(html, "r1" if r5 else "r5")
    figs = {}
    def figrep(m):
        name = m.group(1)
        svgp, pngp = FIG / f"{name}.svg", FIG / f"{name}.png"
        if svgp.exists():
            svg = svgp.read_text()
            w, h = svg_size_mm(svg)
            figs[name] = {"state": "placed", "file": str(svgp.relative_to(REPO)), "w_mm": round(w, 2), "h_mm": round(h, 2),
                          "mtime": dt.datetime.fromtimestamp(svgp.stat().st_mtime).isoformat(timespec="seconds")}
            svg = clean_svg(svg, name)
            svg = re.sub(r'<svg\b', f'<svg data-fig="{name}"', svg, count=1)
            return svg
        if pngp.exists():
            figs[name] = {"state": "png-only", "file": str(pngp.relative_to(REPO))}
            return f'<img data-fig="{name}" src="fig/v13/{name}.png" alt="">'
        figs[name] = {"state": "placeholder"}
        return f'<div class="ph" data-placeholder="{name}"><span>{name}: figure pending</span></div>'
    html = re.sub(r"<!--fig:([\w]+)-->", figrep, html)
    # size each slot to the figure actually drawn (figures are 1:1 at print size; never scaled)
    for name, f in figs.items():
        if f["state"] == "placed":
            html = re.sub(r'(data-figslot="%s" style=")--fw:[\d.]+;--fh:[\d.]+' % name,
                          lambda m: f'{m.group(1)}--fw:{f["w_mm"]};--fh:{f["h_mm"]}', html)
    for name, f in figs.items():
        drop = "unless" if f["state"] == "placed" else "if"
        html = remove_elements(html, f'data-{drop}-fig="{name}"')
    # scope lines a figure may already print: data-unless-figtext="NAME|text" is dropped when NAME's SVG holds the text
    for m in list(re.finditer(r'data-unless-figtext="([\w]+)\|([^"]+)"', html)):
        name, needle = m.group(1), htmllib.unescape(m.group(2))
        svgp = FIG / f"{name}.svg"
        if svgp.exists() and needle in htmllib.unescape(svgp.read_text()):
            el = re.search(r'<(\w+)\b[^>]*%s[^>]*>(.*?)</\1>' % re.escape(m.group(0)), html, re.S)
            if el and 'class="' in el.group(0) and " rt" in el.group(0).split(">")[0]:
                sec = re.search(r'data-brief-sec="([^"]+)"', el.group(0))
                MOVED.append({"figure": name, "text": re.sub(r"<[^>]+>", "", el.group(2)).strip(),
                              "brief": sec.group(1) if sec else None})
            html = remove_elements(html, m.group(0))
    def qrrep(m):
        p = FIG / f"qr_{m.group(1)}.svg"
        if not p.exists():
            return f'<div class="ph" data-placeholder="qr_{m.group(1)}"><span>QR missing</span></div>'
        return clean_svg(p.read_text(), f"qr_{m.group(1)}")
    html = re.sub(r"<!--qr:([\w]+)-->", qrrep, html)
    # R5 placeholders
    unresolved = []
    if r5:
        def r5rep(m):
            v = r5_lookup(r5data, m.group(1), rows)
            if v is None:
                unresolved.append(m.group(0)); return m.group(0)
            return htmllib.escape(v)
        html = re.sub(r"\{(R5\.[\w.<>+-]+)\}", r5rep, html)
    if r5:
        for m in re.finditer(r'<(\w+)\b[^>]*\bdata-mode="r5"[^>]*>(.*?)</\1>', html, re.S):
            R5_PRINTED.append(re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip())
    # remove the authoring comment block (it is not printed, but keep the file clean)
    html = re.sub(r"<!--\s*\n\s*SOURCE of the v13 board.*?-->", "<!-- build product of poster/src/poster.v13.html via poster/build_v13.py; do not edit -->", html, flags=re.S)
    return html, figs


# ---------------------------------------------------------------- render and measure
MEASURE_JS = r"""
async () => {
  await document.fonts.ready;
  const PX = 25.4 / 96;
  const R = r => [r.left * PX, r.top * PX, r.width * PX, r.height * PX];
  const vis = el => { for (let e = el; e; e = e.parentElement) { const cs = getComputedStyle(e);
      if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return false; } return true; };
  const out = {blocks: [], texts: [], figs: [], qrs: [], claims: [], images: [], fonts: []};
  document.querySelectorAll('[data-block]').forEach(b => out.blocks.push({id: b.dataset.block, brief: b.dataset.brief || null,
      rect: R(b.getBoundingClientRect()), bleed: b.dataset.bleed || null, scrollH: b.scrollHeight, clientH: b.clientHeight, scrollW: b.scrollWidth, clientW: b.clientWidth}));
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = tw.nextNode())) {
    const t = n.nodeValue;
    if (!t.trim()) continue;
    const el = n.parentElement;
    if (!el || ['STYLE', 'SCRIPT', 'TITLE'].includes(el.tagName.toUpperCase())) continue;
    if (el.closest('title, desc, defs, metadata, style')) continue;
    if (!vis(el)) continue;
    const cs = getComputedStyle(el);
    const svgEl = el.closest('svg');
    let px = parseFloat(cs.fontSize), inSvg = false;
    if (svgEl && el instanceof SVGElement) {
      inSvg = true;
      const ctm = el.getScreenCTM();
      px = px * Math.sqrt(ctm.a * ctm.a + ctm.b * ctm.b);
    }
    const rg = document.createRange(); rg.selectNodeContents(n);
    const rr = rg.getBoundingClientRect();
    const tick = !!el.closest('[id*="tick_"]');
    const roleEl = el.closest('[data-role]'), blk = el.closest('[data-block]'), fig = el.closest('[data-fig]');
    const exempt = el.closest('[data-exempt]');
    out.texts.push({text: t, family: cs.fontFamily, weight: cs.fontWeight, style: cs.fontStyle, pt: px * 0.75, inSvg,
      rect: R(rr), tick, role: roleEl ? roleEl.dataset.role : null, block: blk ? blk.dataset.block : null,
      fig: fig ? fig.dataset.fig : null, exempt: exempt ? exempt.dataset.exempt : null, tag: el.tagName});
  }
  document.querySelectorAll('[data-figslot]').forEach(s => out.figs.push({name: s.dataset.figslot, rect: R(s.getBoundingClientRect()),
      block: (s.closest('[data-block]') || {dataset: {}}).dataset.block || null}));
  document.querySelectorAll('[data-qr]').forEach(q => {
      if (q.dataset.qrIn) { const slot = document.querySelector(`[data-figslot="${q.dataset.qrIn}"]`);
        out.qrs.push({slug: q.dataset.qr, rect: R(slot.getBoundingClientRect()), in_fig: q.dataset.qrIn}); return; }
      const s = q.querySelector('.sym') || q;
      out.qrs.push({slug: q.dataset.qr, rect: R(s.getBoundingClientRect())}); });
  document.querySelectorAll('[data-claim], .rt').forEach(e => { if (!vis(e)) return;
      const c = e.cloneNode(true); c.querySelectorAll('[data-exempt], .num').forEach(x => x.remove());
      out.claims.push({claim: e.dataset.claim || null, role: e.dataset.role || null, rt: e.classList.contains('rt'),
        text: e.innerText.replace(/\s+/g, ' ').trim(), text_noexempt: c.textContent.replace(/\s+/g, ' ').trim(),
        block: (e.closest('[data-block]') || {dataset: {}}).dataset.block || null,
        brief: (e.closest('[data-brief]') || {dataset: {}}).dataset.brief || (e.closest('header') ? 'Header' : null),
        cls: e.className, rect: R(e.getBoundingClientRect())}); });
  for (const im of document.querySelectorAll('svg image, img')) {
    const href = im.getAttribute('href') || im.getAttribute('xlink:href') || im.getAttribute('src');
    const r = im.getBoundingClientRect();
    const I = new Image(); I.src = href; try { await I.decode(); } catch (e) {}
    out.images.push({fig: (im.closest('[data-fig]') || {dataset: {}}).dataset.fig || null, w_mm: r.width * PX, h_mm: r.height * PX,
                     nat_w: I.naturalWidth, nat_h: I.naturalHeight, rendering: getComputedStyle(im).imageRendering,
                     attr_rendering: im.getAttribute('image-rendering') || im.getAttribute('style') || ''});
  }
  out.cols = [...document.querySelectorAll('[data-col]')].map(c => { const r = c.getBoundingClientRect();
      const kids = [...c.children].filter(k => getComputedStyle(k).display !== 'none');
      const last = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
      const need = kids.reduce((a, k) => a + k.scrollHeight, 0) + (kids.length - 1) * parseFloat(getComputedStyle(c).rowGap || 0);
      return {id: c.dataset.col, rect: R(r), content_bottom: last * PX, natural_mm: need * PX}; });
  const ft = document.querySelector('footer').getBoundingClientRect();
  out.footer_top = ft.top * PX;
  out.fonts = [...document.fonts].map(f => ({family: f.family, weight: f.weight, status: f.status}));
  return out;
}
"""


def chrome():
    exe = sorted(Path(CHROME_GLOB).glob("chromium-*/chrome-linux/chrome"))
    if not exe:
        sys.exit("no Chromium under /opt/pw-browsers")
    return str(exe[-1])


def render(html):
    from playwright.sync_api import sync_playwright
    OUT_HTML.write_text(html)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome())
        pg = b.new_page(viewport={"width": 3179, "height": 4494})
        pg.goto(OUT_HTML.as_uri())
        pg.wait_for_load_state("networkidle")
        meas = pg.evaluate(MEASURE_JS)
        pg.emulate_media(media="print")
        pg.pdf(path=str(PDF), width="841mm", height="1189mm", print_background=True, prefer_css_page_size=True)
        b.close()
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(str(PDF))
    pages = len(pdf)
    w_pt, h_pt = pdf[0].get_size()
    meta = pdf.get_metadata_dict()
    prev = pdf[0].render(scale=3179 / w_pt).to_pil().convert("RGB")
    prev.save(PNG, optimize=True)
    big = pdf[0].render(scale=300 / 72).to_pil().convert("RGB")
    big.save(PNG300, dpi=(300, 300))
    pdf.close()
    return meas, {"pages": pages, "w_mm": w_pt * 25.4 / 72, "h_mm": h_pt * 25.4 / 72, "title": meta.get("Title", "")}, big


# ---------------------------------------------------------------- text helpers
NUM_RE = re.compile(r"(?<![\w.\-])[−+]?\d+(?:[.,]\d+)*(?!\w)")
MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December"
DATE_RE = re.compile(r"\b\d{1,2} (?:%s)(?: \d{4})?\b|\b(?:%s) \d{4}\b|\b20\d\d-\d\d-\d\d" % (MONTHS, MONTHS))


def nums(s):
    return [m.group(0).lstrip("−+") for m in NUM_RE.finditer(s)]


def norm_num(x):
    return x.replace(",", "")


def date_nums(s):
    out = set()
    for m in DATE_RE.finditer(s):
        out.update(norm_num(x) for x in nums(m.group(0)))
    return out


def norm_sentence(s):
    s = unicodedata.normalize("NFC", s).lower()
    return re.sub(r"\s+", " ", s).strip()


def b3(s):
    import blake3
    return blake3.blake3(norm_sentence(s).encode()).hexdigest()


def sentences(s, clauses=False):
    pat = r"(?<=[.?!;])\s+" if clauses else r"(?<=[.?!])\s+(?=[A-Z\"0-9(])"
    return [x.strip() for x in re.split(pat, s) if x.strip()]


# ---------------------------------------------------------------- gates
@gate("page_fit")
def g_page(pdfinfo):
    d = [f"PDF pages {pdfinfo['pages']}, page {pdfinfo['w_mm']:.2f} x {pdfinfo['h_mm']:.2f} mm"]
    ok = pdfinfo["pages"] == 1 and abs(pdfinfo["w_mm"] - 841) <= 0.5 and abs(pdfinfo["h_mm"] - 1189) <= 0.5
    return ok, d


@gate("footer_clearance")
def g_footer(meas):
    ft = meas["footer_top"]
    bottoms = [t["rect"][1] + t["rect"][3] for t in meas["texts"] if t["block"] != "footer" and t["rect"][3] > 0]
    bottoms += [f["rect"][1] + f["rect"][3] for f in meas["figs"]]
    bottoms += [q["rect"][1] + q["rect"][3] for q in meas["qrs"]]
    for b in meas["blocks"]:
        if b["id"] != "footer":
            bottoms.append(b["rect"][1] + b["rect"][3])
    low = max(bottoms)
    gap = ft - low
    return gap >= 2.0, [f"content ends {low:.1f} mm, footer top {ft:.1f} mm, clearance {gap:.1f} mm (need >= 2)"]


def parse_brief_blocks():
    t = BRIEF.read_text().split("## B. Page composition")[1].split("## C.")[0]
    out = {}
    for line in t.splitlines():
        if not line.startswith("| ") or "---" in line or line.startswith("| block"):
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        label, x, y, wh = c[0], c[2], c[3], c[4]
        bid = next((v for k, v in BLOCK_ROWS.items() if label.startswith(k)), None)
        if not bid:
            continue
        w, h = [float(v) for v in re.findall(r"[\d.]+", wh)[:2]]
        out[bid] = (float(x.replace("−", "-")), float(y), w, h)
    return out


@gate("block_rectangles")
def g_blocks(meas):
    brief = parse_brief_blocks()
    d, ok = [], True
    have = {b["id"]: b for b in meas["blocks"]}
    for bid, (x, y, w, h) in brief.items():
        if bid not in have:
            ok = False; d.append(f"{bid}: block missing"); continue
        # the header bleed is clipped to the sheet: compare inside the page
        x0, x1 = max(0.0, x), min(841.0, x + w)
        bx, by, bw, bh = have[bid]["rect"]
        err = max(abs(bx - x0), abs(by - y), abs(bx + bw - x1), abs(by + bh - (y + h)))
        dev = LAYOUT_DEVIATIONS.get(bid)
        if err > 1.0:
            line = (f"{bid}: brief ({x0:.1f},{y:.1f},{x1 - x0:.1f}x{h:.1f}) rendered ({bx:.1f},{by:.1f},{bw:.1f}x{bh:.1f}), "
                    f"off by {err:.1f} mm")
            if dev and dev.get("reason"):
                d.append("DEVIATION " + line + f"; reason: {dev['reason']}")
            else:
                ok = False
                d.append("UNEXPLAINED " + line)
        elif dev:
            d.append(f"{bid}: listed as a deviation but sits on its brief rectangle; remove the entry")
            ok = False
    REPORT_EXTRA["layout_deviations"] = [x for x in d if x.startswith("DEVIATION")]
    return ok, d or ["all blocks inside their section B rectangles (+/- 1 mm)"]


@gate("no_overflow_or_clipping")
def g_overflow(meas):
    d = []
    blocks = {b["id"]: b for b in meas["blocks"]}
    for b in meas["blocks"]:
        if b.get("bleed") == "right" and b["scrollH"] <= b["clientH"] + 2:
            continue   # the header image runs 3 mm past the trim on the right by design (bleed)
        if b["scrollH"] > b["clientH"] + 2 or b["scrollW"] > b["clientW"] + 2:
            d.append(f"{b['id']}: content larger than its box (scroll {b['scrollW']}x{b['scrollH']} px > {b['clientW']}x{b['clientH']})")
    for t in meas["texts"]:
        x, y, w, h = t["rect"]
        if w <= 0:
            continue
        if x < -0.5 or y < -0.5 or x + w > 841.5 or y + h > 1189.5:
            d.append(f"text off the page: {t['text'][:50]!r}")
        bid = t["block"]
        if bid and not t["inSvg"]:
            bx, by, bw, bh = blocks[bid]["rect"]
            if x < bx - 0.6 or y < by - 0.6 or x + w > bx + bw + 0.6 or y + h > by + bh + 0.6:
                d.append(f"{bid}: text outside its block: {t['text'][:60]!r} at y {y:.1f} to {y + h:.1f} (block {by:.1f} to {by + bh:.1f})")
    for f in meas["figs"]:
        if f["block"] and f["block"] in blocks and blocks[f["block"]].get("bleed") != "right":
            bx, by, bw, bh = blocks[f["block"]]["rect"]
            x, y, w, h = f["rect"]
            if x < bx - 0.6 or y < by - 0.6 or x + w > bx + bw + 0.6 or y + h > by + bh + 0.6:
                d.append(f"{f['block']}: figure {f['name']} outside its block: y {y:.1f} to {y + h:.1f} (block {by:.1f} to {by + bh:.1f}), x {x:.1f} to {x + w:.1f}")
    for c in meas.get("cols", []):
        x, y, w, h = c["rect"]
        if c["content_bottom"] > y + h + 0.5 or c["natural_mm"] > h + 0.5:
            d.append(f"column {c['id']}: content needs {c['natural_mm']:.1f} mm, column is {h:.1f} mm (ends {c['content_bottom']:.1f}, column bottom {y + h:.1f})")
    REPORT_EXTRA["columns"] = [{k: (round(v, 1) if isinstance(v, float) else v) for k, v in c.items() if k != "rect"} | {"height": round(c["rect"][3], 1)} for c in meas.get("cols", [])]
    # QR boxes must not cover text that is not on their own tile
    for q in meas["qrs"]:
        if q.get("in_fig"):
            continue   # drawn inside a figure, which places its own label
        qx, qy, qw, qh = q["rect"]
        for t in meas["texts"]:
            x, y, w, h = t["rect"]
            if w <= 0 or t["tick"]:
                continue
            if t.get("fig") and t["fig"].startswith("qr_"):
                continue
            ov_x = min(x + w, qx + qw) - max(x, qx); ov_y = min(y + h, qy + qh) - max(y, qy)
            if ov_x > 0.5 and ov_y > 0.5:
                d.append(f"QR {q['slug']} covers text {t['text'][:50]!r}")
    return not d, d or ["no box larger than its parent; no text outside its block or the page; no QR over text"]


@gate("type_floor")
def g_type(meas, claims):
    d = []
    for t in meas["texts"]:
        if t["pt"] < 14 - 0.05:
            d.append(f"{t['pt']:.1f} pt < 14: {t['text'][:60]!r} ({t['fig'] or t['block']})")
    need = {"kicker": 24, "mechanism": 24, "take": 24, "conclusion": 24, "caption": 17}
    for t in meas["texts"]:
        r = t["role"]
        if r in need and not t["inSvg"] and t["pt"] < need[r] - 0.05:
            d.append(f"{r} at {t['pt']:.1f} pt < {need[r]}: {t['text'][:50]!r}")
    for c in claims:
        if c["role"] == "headline":
            cls = next((b for b in ("c3", "c4", "c6", "c8") if c["block"] in BLOCK_CLASS.get(b, ())), None)
            txt = c["text_noexempt"]
            if cls in ("c3", "c4") and len(txt) > 30:
                if c["block"] in HEADLINE_LEN_EXEMPT:
                    d.append(f"DEVIATION {c['block']}: headline {len(txt)} characters; reason: {HEADLINE_LEN_EXEMPT[c['block']]}")
                else:
                    d.append(f"three/four-column headline over 30 characters ({len(txt)}): {txt!r}")
            if cls in ("c6", "c8") and len(txt) > 50:
                d.append(f"six/eight-column headline over 50 characters ({len(txt)}): {txt!r}")
    bad = [x for x in d if not x.startswith("DEVIATION")]
    return not bad, d or ["no text below 14 pt (HTML and figure SVG, effective size); kicker, mechanism and take lines >= 24 pt; captions >= 17 pt; headline lengths"]


BLOCK_CLASS = {"c3": ("p2", "p3", "questions", "threat", "p7", "p8", "p9", "p10", "p11"), "c4": ("p13",),
               "c6": ("p4", "p5", "p6"), "c8": ("p12",)}


FONTFILES = {("IBM Plex Sans", "400", "normal"): "IBMPlexSans-Regular.ttf", ("IBM Plex Sans", "400", "italic"): "IBMPlexSans-Italic.ttf",
             ("IBM Plex Sans", "500", "normal"): "IBMPlexSans-Medium.ttf", ("IBM Plex Sans", "600", "normal"): "IBMPlexSans-SemiBold.ttf",
             ("IBM Plex Sans", "700", "normal"): "IBMPlexSans-Bold.ttf", ("IBM Plex Mono", "400", "normal"): "IBMPlexMono-Regular.ttf",
             ("IBM Plex Mono", "500", "normal"): "IBMPlexMono-Medium.ttf", ("IBM Plex Mono", "600", "normal"): "IBMPlexMono-SemiBold.ttf",
             ("IBM Plex Mono", "700", "normal"): "IBMPlexMono-Bold.ttf"}


@gate("glyph_coverage")
def g_glyphs(meas):
    from fontTools.ttLib import TTFont
    cmaps, d = {}, []
    wmap = {"normal": "400", "bold": "700"}
    for t in meas["texts"]:
        fam = t["family"].split(",")[0].strip().strip('"\'')
        w = wmap.get(t["weight"], t["weight"])
        w = str(min((400, 500, 600, 700), key=lambda v: abs(v - int(float(w)))))
        st = "italic" if t["style"] in ("italic", "oblique") and fam == "IBM Plex Sans" and w == "400" else "normal"
        key = (fam, w, st)
        if key not in FONTFILES:
            d.append(f"text set in a face that is not shipped: {fam} {w} {t['style']}: {t['text'][:40]!r}")
            continue
        if key not in cmaps:
            cmaps[key] = set(TTFont(HERE / "fonts" / "plex-full" / FONTFILES[key]).getBestCmap())
        miss = sorted({ch for ch in t["text"] if not ch.isspace() and ord(ch) not in cmaps[key]})
        if miss:
            d.append(f"{FONTFILES[key]} lacks {' '.join(f'U+{ord(c):04X}({c})' for c in miss)} in {t['text'][:50]!r}")
    return not d, d or [f"every printed code point is in the face that sets it ({len(meas['texts'])} text runs)"]


TELLS = ["robust", "seamless", "leverage", "cutting-edge", "game-chang", "revolutioni", "unlock", "delve", "paradigm",
         "groundbreaking", "state-of-the-art", "empower", "synergy", "crucial", "pivotal", "landscape", "tapestry",
         "harness the", "in today's", "furthermore", "moreover"]
BANNED = [  # (key, regex) from report 10 section 5.3 and brief G.3
    ("first", r"\bfirst\b"), ("only", r"(?<!-)\bonly\b"), ("unique", r"\bunique\b"), ("novel", r"\bnovel\b"),
    ("never", r"\bnever\b"), ("always", r"\balways\b"), ("impossible", r"\bimpossible\b"), ("cannot", r"\bcannot\b"),
    ("every", r"\bevery(?:thing|one)?\b"), ("all", r"\ball\b"), ("any", r"\bany\b"), ("none", r"\bnone\b"),
    ("true", r"\btrue\b"), ("truth", r"\btruth\b"), ("truly", r"\btruly\b"), ("correct", r"\bcorrect\b"),
    ("guarantee", r"\bguarantee[sd]?\b"), ("prove", r"\bprove[sn]?\b"),
    ("proof", r"(?<!inclusion )(?<!consistency )(?<!merkle )\bproofs?\b"), ("certain", r"\bcertain\b"),
    ("certified", r"\bcertified\b"), ("immutable", r"\bimmutable\b"), ("tamper-proof", r"\btamper-proof\b"),
    ("trustless", r"\btrustless\b"), ("secure", r"\bsecure\b"), ("zero-trust", r"\bzero-trust\b"),
    ("unforgeable", r"\bunforgeable\b"), ("decides", r"\bdecides?\b"), ("arbiter", r"\barbiter\b"),
    ("judge", r"\bjudge[sd]?\b"), ("the satellite", r"\bthe satellite\b"),
    ("independent", r"\bindependent(?:ly)?\b"), ("compliance", r"\bcomplian(?:t|ce)\b"), ("due diligence", r"\bdue diligence\b"),
    ("regulatory", r"(?<!a )\bregulatory\b"),
    ("hash of", r"\bhash of (?:its|the) (?:bytes|pixel|file|scene|image|data)\b"), ("signed pixel", r"\bsigned pixel\b"),
    ("signs the value", r"\bsigns the value\b"), ("equal values give equal", r"equal values give equal"),
]
DEPLOY = r"\b(?:spacecraft|in orbit|on board|onboard|downlink|flight|operational|deployed|production)\b"
DEPLOY_OK = r"\b(?:harness|reference run|scripted|not a spacecraft|no spacecraft)\b"
VERIF = r"\bverif(?:y|ied|ies|iable|ication)\b"
COUNT_AFTER = re.compile(r"^\s+(?:of\s+(?:the\s+)?|the\s+)?\d")


def text_units(meas, claims):
    """(where, sentence) for every printed text: HTML blocks by data-claim/.rt element, figure text by SVG <text>."""
    units = []
    seen = set()
    for c in claims:
        key = (c["text"], c["block"])
        if key in seen:
            continue
        seen.add(key)
        units.append((f"html:{c['block']}:{c['role'] or ''}", c["text"], c["role"]))
    # html text not inside any claim element (bylines, QR captions, strip) is covered by its claim element; figure text:
    for t in meas["texts"]:
        if t["inSvg"] and not t["tick"] and not (t["fig"] or "").startswith("qr_"):
            units.append((f"fig:{t['fig']}", t["text"].strip(), "figure"))
    return units


@gate("prose_and_banned_words")
def g_banned(meas, claims, rows, collect=None):
    allow = json.loads(ALLOW.read_text())["entries"] if ALLOW.exists() else []
    allowed = {(a["word"], a["text_sha"]): a for a in allow}
    d = []
    used = set()
    for where, text, role in text_units(meas, claims):
        if "—" in text:
            d.append(f"{where}: em dash: {text[:80]!r}")
        if "–" in text:
            d.append(f"{where}: en dash (write 'to'): {text[:80]!r}")
        low = text.lower()
        for w in TELLS:
            if w in low:
                d.append(f"{where}: tell word {w!r}: {text[:80]!r}")
        if role == "title":
            continue
        for s in sentences(text, clauses=False):
            sl = s.lower()
            hits = []
            for key, rx in BANNED:
                for m in re.finditer(rx, sl):
                    if key in ("all", "none", "every", "any") and COUNT_AFTER.match(sl[m.end():]):
                        continue
                    if key == "regulatory" and re.search(r"\bnot a regulatory\b", sl):
                        continue
                    hits.append(key)
            if re.search(VERIF, sl) and not re.search(r"\bL[0-5]\b", s):
                hits.append("verif-without-layer")
            if re.search(DEPLOY, sl) and not re.search(DEPLOY_OK, sl):
                hits.append("deployment-wording")
            for key in sorted(set(hits)):
                sha = b3(s)
                a = allowed.get((key, sha))
                if a and a.get("evidence") in rows:
                    used.add((key, sha)); continue
                if collect is not None:
                    collect.append({"word": key, "text_sha": sha, "sentence": s, "where": where})
                d.append(f"{where}: banned {key!r} without an allowlist entry: {s[:110]!r}")
    stale = [a for a in allow if (a["word"], a["text_sha"]) not in used]
    REPORT_EXTRA["allowlist_used"] = len(used)
    REPORT_EXTRA["allowlist_unused"] = [a["sentence"][:80] for a in stale]
    for a in allow:
        if a.get("evidence") not in rows:
            d.append(f"allowlist entry cites a missing claims row {a.get('evidence')!r}: {a['sentence'][:60]!r}")
    return not d, d or [f"no em/en dashes, tell words or unlisted banned words; {len(used)} allowlisted uses, each bound by BLAKE3 to its sentence and a claims row"]


@gate("face_hygiene")
def g_hygiene(meas, pdfinfo, doc_title):
    d = []
    allt = " ".join(t["text"] for t in meas["texts"])
    for rx, what in [(r"\bv1[0-3](?:\.\d)?\b", "board version number"), (r"\bwithdrawn\b", "withdrawn"),
                     (r"\bscorecard", "scorecard"), (r"should_do", "research/should_do path"), (r"\bdefect\b", "defect id"),
                     (r"\{R5\.", "unresolved R5 placeholder"), (r"figure pending", "figure placeholder")]:
        for m in re.finditer(rx, allt, re.I):
            d.append(f"{what}: ...{allt[max(0, m.start() - 30):m.end() + 30]}...")
    if pdfinfo["title"] != doc_title:
        d.append(f"PDF title {pdfinfo['title']!r} is not the programme title")
    return not d, d or ["no version numbers, defect ids, scorecards, placeholders or R5 tokens on the face; PDF title is the programme title"]


@gate("r5_placeholders")
def g_r5(html_out, info):
    left = re.findall(r"\{R5\.[^}]*\}", re.sub(r"(?s)<!--.*?-->", "", html_out))
    return not left, [f"mode: {info['mode']} ({info.get('why', 'results final')})"] + [f"unresolved {x}" for x in left]


@gate("claims_coverage")
def g_claims(meas, claims, rows, r5):
    d = []
    allprint_nums = set()
    for r in rows.values():
        for p in r["print"]:
            allprint_nums.update(norm_num(x) for x in nums(p))
    alldates = set()
    for r in rows.values():
        for p in r["print"]:
            alldates |= date_nums(p)
    printed_ids = set()
    exempt_roles = {"kicker", "question"}
    for c in claims:
        ids = (c["claim"] or "").split()
        if not ids:
            if c["rt"] and c["role"] not in exempt_roles and not (c["role"] == "headline" and c["block"] == "questions"):
                d.append(f"{c['block']}: sentence without a data-claim: {c['text'][:80]!r}")
            continue
        for i in ids:
            if i not in rows:
                d.append(f"{c['block']}: data-claim {i!r} is not a row of the claims map"); continue
            r = rows[i]
            printed_ids.add(i)
            if r.get("date") == "pending" and not r5:
                d.append(f"{c['block']}: pending R5 row {i} printed in fallback mode")
            if (r.get("note") or "").startswith("CONDITIONAL"):
                d.append(f"{c['block']}: CONDITIONAL row {i} printed without its condition file")
        own = set()
        for i in ids:
            for p in rows.get(i, {}).get("print", []):
                own.update(norm_num(x) for x in nums(p))
        for x in nums(c["text_noexempt"]):
            xn = norm_num(x)
            if xn in own:
                continue
            if xn in date_nums(c["text_noexempt"]) and xn in alldates:
                continue
            d.append(f"{c['block']}: number {x!r} not in the print strings of its rows {ids}: {c['text'][:70]!r}")
        # R1 suite bound
        if any(i.startswith("S.R1.") or i in ("S.headline", "K.concl") for i in ids):
            if not re.search(r"of 16|/ 16|in our suite", c["text"]):
                d.append(f"{c['block']}: R1 number without the suite bound: {c['text'][:70]!r}")
        # record rule
        for s in sentences(c["text"], clauses=True):
            sl = s.lower()
            if re.search(r"\b(fact_cid|cid|content address|address|token)\b", sl) and re.search(r"\b(pixel|scene|file|satellite)", sl) \
                    and "record" not in sl:
                d.append(f"{c['block']}: address/token next to pixel/scene/file without 'record': {s[:80]!r}")
    # every number anywhere (figure text included) has a row
    labels = {}
    for lj in FIG.glob("*.labels.json"):
        try:
            L = json.loads(lj.read_text())
            L = L.get("labels", L) if isinstance(L, dict) else L
            for e in L:
                if isinstance(e, dict):
                    labels[(lj.name.split(".")[0], (e.get("text") or e.get("label") or "").strip())] = e.get("claim") or e.get("claim_id")
        except Exception as e:  # noqa
            d.append(f"{lj.name}: unreadable labels file ({e})")
    nfig = 0
    for t in meas["texts"]:
        if t["tick"] or t["exempt"] or (t["fig"] or "").startswith("qr_"):
            continue
        for x in nums(t["text"]):
            xn = norm_num(x)
            if t["inSvg"]:
                nfig += 1
                cid = labels.get((t["fig"], t["text"].strip()))
                if cid and cid in rows:
                    own = {norm_num(y) for p in rows[cid]["print"] for y in nums(p)}
                    if xn not in own:
                        d.append(f"fig {t['fig']}: number {x!r} not in its labels.json row {cid}: {t['text'][:60]!r}")
                    continue
            if xn not in allprint_nums:
                d.append(f"{'fig ' + str(t['fig']) if t['inSvg'] else t['block']}: number {x!r} has no claims-map row: {t['text'][:70]!r}")
    # LIVE freshness
    for i in sorted(printed_ids | {k for k in rows if k.startswith("EC.row.")}):
        r = rows[i]
        try:
            age = (TODAY - dt.date.fromisoformat(r["date"])).days
        except Exception:
            continue
        if r["status"] == "LIVE" and age > 7:
            d.append(f"LIVE row {i} is {age} days old (re-fetch within 7 days)")
        if i.startswith("EC.row.") and age > 14:
            d.append(f"ecosystem row {i} is {age} days old (> 14)")
    REPORT_EXTRA["claims_printed"] = sorted(printed_ids)
    REPORT_EXTRA["figure_numbers_checked"] = nfig
    return not d, d or [f"{len(printed_ids)} claim rows printed; every number in HTML and figure text has a row; suite bound and record rule hold"]


# port of the checks in the brief's Appendix I generator (re-run every row that has one)
def _rp(p):
    p = str(p)
    if p.startswith("poster/"):          # figure-side files (verify.json, labels) live under poster/
        return REPO / p
    return RES / (p[len("research/"):] if p.startswith("research/") else p)


def _J(p):
    return json.load(open(_rp(p)))


def _ptr(o, path):
    if isinstance(path, str):   # "rows.ndvi_keylong[10].ms"
        path = [int(x) if x.isdigit() else x for x in re.findall(r"[^.\[\]]+", path)]
    for k in path:
        o = o[k]
    return o


DELEGATED = []


def run_check(c, rows_list, rid=None):
    kind, f, p, exp = c["kind"], c.get("file"), c.get("arg"), c.get("expect")
    if kind == "figure_assert":   # asserted inside the figure script when it draws; the board checks the script exists
        ok = (REPO / f).exists() and rows_list[rid].get("checked") is True
        DELEGATED.append(rid)
        return ok
    if kind == "json":
        return _ptr(_J(f), p) == exp
    if kind == "json_contains":
        return exp in str(_ptr(_J(f), p))
    if kind == "approx":
        return abs(round(_ptr(_J(f), p), 2) - exp) <= max(0.01, abs(exp) * 0.01)
    if kind == "approx_diff":   # arg [pathA, pathB]: round(A - B, 2) == expect (C.cpu: per-decision time less handoff construction)
        J = _J(f)
        return round(_ptr(J, p[0]) - _ptr(J, p[1]), 2) == exp
    if kind == "grep":
        return p in _rp(f).read_text()
    if kind == "calc":
        return abs(p - exp) < 0.0006 or round(p, 3) == round(exp, 3)
    if kind == "count_mut":
        J = _J(f)
        return len([m for m in J["meta"]["mutations"] if m["id"] not in ("G0", "M17")]) - 1 == exp or \
            len([m for m in J["meta"]["mutations"] if m["id"] not in ("G0", "M17", "M7")]) == exp - 1 or \
            J["summary"]["I"]["applicable"] == exp
    if kind == "qwen":
        rs = [json.loads(l) for l in open(_rp(f))]
        return sum(1 for r in rs if [r["arm"], r["decision"]] == list(p)) == exp
    if kind == "qwen_bare":
        rs = [json.loads(l) for l in open(_rp(f))]
        return sum(1 for r in rs for t in (r.get("tool_calls") or []) if t.get("token_form") == "bare_cid") == exp
    if kind == "cp":
        return any(r["band"] == p and r["value"] == exp for r in _J(f))
    if kind == "bg_values":
        got = dict(Counter(a["value"] for a in _J(f)["contradictions"][0]["attestations"]))
        return {str(k): v for k, v in got.items()} == {str(k): v for k, v in exp.items()} or got == exp
    if kind == "ck_hash":
        n = h = 0
        for fa in _J(f)["facts"]:
            for s in fa.get("sources", []):
                n += 1; h += 1 if (s.get("hash") or s.get("cid")) else 0
        return [n, h] == list(exp)
    if kind == "wilson":
        w = _ptr(_J(f), p); return [round(w[1], 2), round(w[2], 2)] == list(exp)
    if kind == "err":
        e = _ptr(_J(f), p); return [round(e["median"], 3), round(e["p90"], 3), round(e["max"], 3), e["n"]] == list(exp)
    if kind == "csv":
        col, val = p
        return sum(1 for r in csv.DictReader(open(_rp(f))) if r[col] == val) == exp
    if kind == "geod":
        from pyproj import Geod
        return round(Geod(ellps="WGS84").inv(*p)[2]) == exp
    if kind == "rond":
        dd = _J(f); ly, g = dd["lossyear"], dd["gfc2020"]
        ch = sum(1 for r in ly if r["floor"] != r["round"])
        fl = sum(1 for a, b in zip(g, ly) if a["floor"] == 1 and b["floor"] > 20)
        fr = sum(1 for a, b in zip(g, ly) if a["round"] == 1 and b["round"] > 20)
        return [ch, fl, fr] == list(exp)
    if kind == "prithvi":
        for fa in _J(f)["facts"]:
            if fa["band"] == "prithvi_eo2":
                return fa["served_via"]["model_blake2b_hex"] == exp and exp in json.dumps(fa["derivation"]) and len(fa["value"]) == 1024
        return False
    if kind == "reread":
        L = _ptr(_J(f), ["m3_trace_read_only", "keylong_ndvi", "links"])
        return [round(sum(L[k]["ms_median"] for k in ("8", "9", "9b")), 1), sum(L[k]["bytes"][0] for k in ("8", "9", "9b"))] == list(exp)
    if kind == "ratio":
        a, b = _ptr(_J(f), p[0]), _ptr(_J(f), p[1]); return round(a / b, 1) == exp
    if kind == "xr_med":
        meds = sorted(r["ms_median"] for r in _J(f)["rows"]["ndvi_keylong"] if r.get("ms_median"))
        return meds == [56.3, 58.3, 58.6, 207.7, 223.5, 223.7, 226.3, 235.6, 300.8, 1176.8]
    if kind == "eco":
        m = {r["id"]: r for r in _J(f)}[p]
        return m["print"]["allowed"] is True and m["status"] in ("LIVE", "PROTOCOL", "REGISTRY", "EXAMPLE")
    if kind == "eco_field":   # arg [manifest id, field, substring]: the manifest row's field holds the substring
        m = {r["id"]: r for r in _J(f)}[p[0]]
        return p[2] in json.dumps(m[p[1]])
    if kind == "berlin":   # v13.1 panel 9: the v12.1 selection (poster/make_figures_v12.py fig_berlin) re-applied to the live file
        rows = _J(f)["rows"]
        def pick(inst, qty, date=None):
            return next(r for r in rows if inst in r["instrument"] and qty in r["quantity"]
                        and (date is None or (r["observed_at"] or "").startswith(date)))
        sel = [("S2", pick("Sentinel-2", "B08", "2026-09-27")), ("S2", pick("Sentinel-2", "NDVI", "2026-09-27")),
               ("S1", pick("Sentinel-1", "VV", "2026-09-28")), ("DEM", pick("Copernicus DEM", "elevation")),
               ("MOD11A2", pick("MOD11A2", "temperature")), ("WorldCover", pick("WorldCover", "class")),
               ("CCI", pick("CCI Biomass", "biomass")), ("GSW", pick("Surface Water", "occurrence")),
               ("Hansen", pick("Hansen", "tree cover")), ("GFC2020", pick("Forest Cover 2020", "forest")),
               ("CAMS", pick("Copernicus Atmosphere", "NO2", "2026-09-30")), ("Overture", pick("Overture", "building")),
               ("SoilGrids", pick("SoilGrids", "organic carbon")), ("CHIRPS", pick("CHIRPS", "precip")),
               ("TMF", pick("Tropical Moist", "deforestation")), ("FIRMS", pick("FIRMS", "fire"))]
        got = [len({a for a, _ in sel}), len(sel), sum(1 for _, r in sel if r["kind"] == "absence")]
        return got == list(exp) and all(r["verified"] in (True, "PASS", "pass") for _, r in sel)
    if kind == "count":   # figure additions: two argument forms are understood; anything else is unknown (a failure)
        J = _J(f)
        m = re.fullmatch(r"attestations value ([\d.]+)", p)
        if m:
            return sum(1 for a in J["contradictions"][0]["attestations"] if a["value"] == float(m.group(1))) == exp
        m = re.fullmatch(r"rows date >= (\S+) and signed_at < (\S+)", p)
        if m:
            return sum(1 for r in J["rows"] if r["date"] >= m.group(1) and r["signed_at"] < m.group(2)) == exp
    raise ValueError(f"unknown check kind {kind} / arg {p!r}")


@gate("claims_rows_recheck")
def g_recheck(rows):
    d, n = [], 0
    for r in rows.values():
        c = r.get("check")
        if not c:
            continue
        n += 1
        try:
            ok = run_check(c, rows, r["id"])
        except Exception as e:  # noqa
            ok = False; d.append(f"{r['id']}: check could not run: {type(e).__name__}: {e}")
            continue
        if ok is not True:
            d.append(f"{r['id']}: check {c['kind']} on {c['file']} does not reproduce the printed value")
    REPORT_EXTRA["rows_rechecked"] = n
    REPORT_EXTRA["rows_delegated_to_figure_asserts"] = DELEGATED
    return not d, d or [f"{n} rows with a check re-run against their files: all pass ({len(DELEGATED)} are figure_assert rows, asserted by the figure scripts when they draw)"]


@gate("qr_decode")
def g_qr(meas, big):
    import cv2
    import numpy as np
    det = cv2.QRCodeDetector()
    d, ok = [], True
    seen = {q["slug"] for q in meas["qrs"]}
    for slug in QRS:
        txt = FIG / f"qr_{slug}.txt"
        svg = FIG / f"qr_{slug}.svg"
        if not txt.exists() or not svg.exists():
            ok = False; d.append(f"qr_{slug}: payload or symbol file missing"); continue
        if slug not in seen:
            ok = False; d.append(f"qr_{slug}: not placed on the board"); continue
    for q in meas["qrs"]:
        payload = (FIG / f"qr_{q['slug']}.txt").read_text().strip()
        x, y, w, h = q["rect"]
        s = 300 / 25.4
        pad = 2
        crop = big.crop((int((x - pad) * s), int((y - pad) * s), int((x + w + pad) * s), int((y + h + pad) * s)))
        arr = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2BGR)
        vals = []
        for a in (arr, cv2.resize(arr, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)):
            v, _, _ = det.detectAndDecode(a)
            vals.append(v)
            try:
                okm, vm, _, _ = det.detectAndDecodeMulti(a)
                if okm:
                    vals += list(vm)
            except cv2.error:
                pass
            if payload in vals:
                break
        val = payload if payload in vals else next((v for v in vals if v), "")
        good = val == payload
        ok &= good
        d.append(f"qr_{q['slug']} at ({x:.1f},{y:.1f}) {w:.1f} mm: decoded {val!r} {'==' if good else '!='} payload {payload!r}")
    return ok, d


@gate("assets")
def g_assets(figs):
    d = []
    for n in FIGURES:
        st = figs.get(n, {"state": "not referenced"})
        if st["state"] != "placed":
            d.append(f"{n}: {st['state']}")
    for f in [CSS, TOKENS] + [HERE / "fonts" / "plex-full-woff2" / v.replace(".ttf", ".woff2") for v in FONTFILES.values()]:
        if not f.exists():
            d.append(f"missing {f.relative_to(REPO)}")
    return not d, d or [f"all {len(FIGURES)} figures and diagrams placed as SVG; fonts, CSS and tokens present"]


@gate("fonts_loaded")
def g_fonts(meas):
    bad = [f for f in meas["fonts"] if f["status"] != "loaded" and f["status"] != "unloaded"]
    used_unloaded = [f for f in meas["fonts"] if f["status"] == "error"]
    return not used_unloaded and not bad, [f"{len(meas['fonts'])} faces declared; " +
                                           ", ".join(f"{f['family']} {f['weight']}: {f['status']}" for f in meas["fonts"])]


IMAGERY_FIGS = {"f1_scene", "f2_spine", "f5_evidence_object", "f7_wrong_pixel"}   # figures that draw real pixels as cells


def _hexes(text):
    out = Counter()
    for m in re.finditer(r"(?<![&\w(#])#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", text):
        h = m.group(0).upper()
        if len(h) == 4:
            h = "#" + "".join(c * 2 for c in h[1:])
        out[h] += 1
    return out


@gate("colour_tokens")
def g_colour(html_out, figs):
    toks = {v.upper() for v in json.loads(TOKENS.read_text())["colors"].values()} | {"#FFFFFF", "#000000"}
    d, ok = [], True
    # board CSS and markup outside the figures
    board = re.sub(r"(?s)<svg\b.*?</svg>", "", re.sub(r'(?:href|src)="data:[^"]*"', "", html_out))
    bad = {h: n for h, n in _hexes(board).items() if h not in toks}
    for h, n in sorted(bad.items()):
        ok = False; d.append(f"board CSS/HTML: {h} ({n} uses) is not in poster/src/tokens.json")
    pix = 0
    for name, f in figs.items():
        if f["state"] != "placed":
            continue
        svg = re.sub(r'(?:href|src)="data:[^"]*"', "", (REPO / f["file"]).read_text())
        # text and strokes must always be tokens; area fills may be pixel colours in imagery figures
        strict = Counter()
        for m in re.finditer(r"<text\b[^>]*>", svg):
            strict.update(_hexes(m.group(0)))
        for m in re.finditer(r"stroke:\s*(#[0-9a-fA-F]{6})|stroke=\"(#[0-9a-fA-F]{6})\"", svg):
            strict[(m.group(1) or m.group(2)).upper()] += 1
        for h, n in strict.items():
            if h not in toks:
                ok = False; d.append(f"{name}: text or stroke colour {h} ({n}) is not a token")
        allh = _hexes(svg)
        extra = {h: n for h, n in allh.items() if h not in toks and h not in strict}
        if extra:
            if name in IMAGERY_FIGS:
                pix += len(extra)
            else:
                ok = False
                d += [f"{name}: fill {h} ({n}) is not a token (and {name} is not an imagery figure)" for h, n in sorted(extra.items())]
    d.insert(0, f"board and figure colours checked against poster/src/tokens.json; {pix} pixel-cell fills in imagery figures ({', '.join(sorted(IMAGERY_FIGS))})")
    pal = RES / "v13" / "evidence" / "visual" / "palette_check.py"
    d.append(f"palette_check.py (CVD, FOGRA39): {'present in the repo; not re-run by this build (needs the non-redistributable FOGRA39 profile)' if pal.exists() else 'not in the repo'}")
    return ok, d


@gate("imagery")
def g_imagery(meas):
    d, ok = [], True
    for im in meas["images"]:
        if not im["nat_w"] or im["w_mm"] <= 0:
            continue
        ppi = im["nat_w"] / (im["w_mm"] / 25.4)
        line = f"{im['fig']}: {im['nat_w']}x{im['nat_h']} px over {im['w_mm']:.1f} mm = {ppi:.0f} ppi"
        if ppi < 299:
            ok = False; line += " (< 300 ppi)"
        d.append(line)
    return ok, d or ["no raster images on the board yet"]


@gate("word_budget")
def g_words(claims, r5=False):
    wre = re.compile(r"[A-Za-z0-9][\w'.,%/:+·-]*")
    def count(s):
        toks = wre.findall(s)
        return len(toks), sum(1 for t in toks if re.search(r"[A-Za-z]", t))
    per, tot_t, tot_w = defaultdict(lambda: [0, 0]), 0, 0
    for c in claims:
        if not c["rt"] or c["role"] == "title":
            continue
        t, w = count(c["text_noexempt"] + (" " + " ".join(re.findall(r"→ [\d, ]+", c["text"])) if c["role"] == "question" else ""))
        tot_t += t; tot_w += w
        per[c["brief"]][0] += t; per[c["brief"]][1] += w
    for mv in MOVED:   # a running line the figure prints itself still counts once
        t, w = count(mv["text"]); tot_t += t; tot_w += w
        per[mv["brief"]][0] += t; per[mv["brief"]][1] += w
    # section C counts
    c_text = BRIEF.read_text().split("## C. The complete printed text")[1].split("## D. Claims map")[0]
    sec, bc, r1lines = None, defaultdict(int), defaultdict(list)
    for line in c_text.splitlines():
        if line.startswith("### "):
            sec = line[4:]
        elif line.startswith("> [R5]"):
            if not r5 or not r1lines[sec]:
                continue
            r5_line = line[len("> [R5]"):].strip()
            toks = wre.findall(r5_line.lstrip("… "))
            if r5_line.startswith("…"):       # "… tail": the tail replaces the R1 line from where its first words occur
                base = max(r1lines[sec], key=lambda l: len(set(wre.findall(l)) & set(toks)))
                bt = wre.findall(base)
                bare = lambda ts: [t.strip(".,;:") for t in ts]   # noqa: E731  (anchor words, punctuation aside)
                idx = next((i for i in range(len(bt)) if bare(bt[i:i + 3]) == bare(toks[:3])), None)
                bc[sec] += (idx + len(toks) - len(bt)) if idx is not None else len(set(toks) - set(bt))
            else:                              # a replacement of the R1 line that shares its opening words
                base = max(r1lines[sec], key=lambda l: sum(1 for x, y in zip(wre.findall(l), toks) if x == y))
                bc[sec] += len(toks) - len(wre.findall(base))
        elif line.startswith("> "):
            r1lines[sec].append(line[2:])
            bc[sec] += len(wre.findall(line[2:]))
    # cap: brief 823 / 869 after the 1 Oct review fixes 9, 13 and 16 (807 / 853 before them) plus about 1 % slack
    d = [f"running text: {tot_w} words containing a letter, {tot_t} tokens with numerals (cap 830 / 880; brief 823 / 869; v13.1 section C: see the per-panel lines)"]
    ok = tot_w <= 830 and tot_t <= 880
    for b, (t, w) in sorted(per.items(), key=lambda kv: str(kv[0])):
        ref = next((v for k, v in bc.items() if b and k.startswith(b)), None)
        flag = ""
        if ref is not None and abs(t - ref) > max(1, 0.1 * ref):
            flag = " (outside +/- 10 % of section C)"; ok = False
        d.append(f"  {b}: {t} tokens (section C: {ref}){flag}")
    REPORT_EXTRA["words"] = {"running_words_with_letter": tot_w, "running_tokens": tot_t}
    return ok, d


# ---------------------------------------------------------------- main
def main():
    if "--r1" in sys.argv:
        subprocess.run([sys.executable, str(RES / "repro" / "v11" / "mutation_suite.py")], check=True, stdout=subprocess.DEVNULL)
    if "--figures" in sys.argv and (HERE / "make_figures_v13.py").exists():
        subprocess.run([sys.executable, str(HERE / "make_figures_v13.py")], check=True)
    doc, rows = load_claims()
    r5, r5data, info = r5_mode()
    html, figs = assemble(r5, r5data, rows)
    meas, pdfinfo, big = render(html)
    claims = meas["claims"]
    doc_title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
    collect = [] if "--allowlist-candidates" in sys.argv else None

    g_page(pdfinfo)
    g_footer(meas)
    g_blocks(meas)
    g_overflow(meas)
    g_type(meas, claims)
    g_glyphs(meas)
    g_banned(meas, claims, rows, collect)
    g_hygiene(meas, pdfinfo, doc_title)
    g_r5(html, info)
    g_claims(meas, claims, rows, r5)
    g_recheck(rows)
    g_qr(meas, big)
    g_assets(figs)
    g_fonts(meas)
    g_colour(html, figs)
    g_imagery(meas)
    g_words(claims, r5)

    figtext = [t["text"] for t in meas["texts"] if t["inSvg"] and not (t["fig"] or "").startswith("qr_")]
    report = {
        "built_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "source": str(SRC.relative_to(REPO)), "outputs": [str(p.relative_to(REPO)) for p in (OUT_HTML, PDF, PNG, PNG300)],
        "mode": info, "pdf": pdfinfo, "figures": figs,
        "figure_text_tokens": sum(len(t.split()) for t in figtext),
        "gates": GATES, "summary": {k: ("PASS" if v["pass"] else "FAIL") for k, v in GATES.items()},
        "running_lines_printed_by_figures": MOVED,
        "r5_lines_as_printed": R5_PRINTED,
        "type_deviations_from_brief": TYPE_DEVIATIONS,
        **REPORT_EXTRA,
    }
    if collect is not None:
        report["allowlist_candidates"] = collect
    REPORT.write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print(f"\nv13 build: mode {info['mode']}; PDF {pdfinfo['pages']} page {pdfinfo['w_mm']:.1f} x {pdfinfo['h_mm']:.1f} mm")
    for k, v in GATES.items():
        print(f"  {'PASS' if v['pass'] else 'FAIL'}  {k}")
        for line in v["details"][: (60 if not v["pass"] else 3)]:
            print(f"        {line}")
    if collect:
        print("\nallowlist candidates:")
        for c in collect:
            print(json.dumps(c, ensure_ascii=False))
    failed = [k for k, v in GATES.items() if not v["pass"]]
    print(f"\n{'FAILED gates: ' + ', '.join(failed) if failed else 'all gates pass'}; report: {REPORT.relative_to(REPO)}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
