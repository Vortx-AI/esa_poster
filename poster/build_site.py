#!/usr/bin/env python3
"""Build docs/, the GitHub Pages site the EMEM poster's QR codes open, and the six QR codes.

    npm ci --prefix tools/site          # once: the pure-JS @noble libraries, esbuild, playwright-core
    python poster/build_site.py         # pages, transcript, fonts, QR codes, gates
    python poster/build_site.py --test  # plus the headless phone test (390 x 844) and screenshots

Steps:
  1. node tools/site/build.mjs   -> docs/demo/index.html, transcript.txt, expected.json (fails on any changed verdict)
  2. node tools/site/site.mjs    -> docs/index.html, t/, r/, test/, methods/, use/, .nojekyll
  3. shared CSS and IBM Plex (SIL OFL 1.1), subset to the characters the pages use, as WOFF2 in docs/assets/fonts/
  4. six QR codes (ECC Q, 4-module quiet zone) -> poster/fig/v13/qr_<name>.svg + qr_<name>.txt; each SVG is
     rasterised at its print size and must decode (OpenCV) to its exact payload
  5. gates (they fail, never warn): no em dash, no en dash outside a numeric range, no tell word, no model
     identifier, every relative link resolves, no page script names a POST to emem.dev
  6. --test: node tools/site/test_site.mjs serves docs/ with python -m http.server and drives Chromium
"""
import html as htmllib, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS, TOOLS = ROOT / "docs", ROOT / "tools" / "site"
QR_DIR = ROOT / "poster" / "fig" / "v13"
FONT_SRC = ROOT / "poster" / "fonts" / "plex-full"
BASE = "https://vortx-ai.github.io/esa_poster/"
# (slug, call to action, path, printed symbol size in mm without the quiet zone; research/v13/09_demo_and_qr.md section 2.2)
QRS = [("demo", "TRY IT", "demo/", 70), ("t", "TRY A TOKEN", "t/", 40), ("r", "INSPECT", "r/", 40),
       ("test", "RE-RUN THE TEST", "test/", 40), ("methods", "REPRODUCE", "methods/", 40),
       ("use", "CONNECT", "use/", 40)]
FONTS = [("IBMPlexSans-Regular", "IBMPlexSans-Regular"), ("IBMPlexSans-SemiBold", "IBMPlexSans-SemiBold"),
         ("IBMPlexSans-Bold", "IBMPlexSans-Bold"), ("IBMPlexMono-Regular", "IBMPlexMono-Regular"),
         ("IBMPlexMono-SemiBold", "IBMPlexMono-SemiBold"), ("IBMPlexMono-Bold", "IBMPlexMono-Bold")]
TELLS = ["robust", "seamless", "leverage", "cutting-edge", "game-chang", "revolutioni", "unlock", "delve",
         "paradigm", "groundbreaking", "state-of-the-art", "empower", "synergy"]
MODEL_ID = re.compile(r"claude-(opus|sonnet|haiku|fable)|\b(opus|sonnet|haiku|fable)[ -]\d|gpt-\d|qwen\d|llama-?\d|gemma-?\d", re.I)


def fail(msg):
    sys.exit("SITE GATE FAIL: " + msg)


def run(cmd):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stdout + r.stderr)
        fail(f"{cmd[0]} {cmd[1]} exited {r.returncode}")
    print(r.stdout.strip()[-1200:])
    return r.stdout


def visible_text(page: str) -> str:
    body = re.sub(r"(?s)<script.*?</script>|<style.*?</style>|<svg.*?</svg>|<!--.*?-->", " ", page)
    return htmllib.unescape(re.sub(r"<[^>]+>", " ", body))


def prose_gate(name: str, text: str):
    bad = []
    for m in re.finditer("—", text):
        bad.append("em dash: " + text[max(0, m.start() - 40):m.end() + 40].strip())
    for m in re.finditer("–", text):
        a, b = text[m.start() - 1:m.start()], text[m.end():m.end() + 1]
        if not (a.isdigit() and (b.isdigit() or b == "")):
            bad.append("en dash outside a numeric range: " + text[max(0, m.start() - 30):m.end() + 30].strip())
    low = text.lower()
    bad += [f"tell word: {w}" for w in TELLS if w in low]
    bad += [f"model identifier: {m.group(0)}" for m in MODEL_ID.finditer(text)]
    if bad:
        fail(f"{name}:\n  " + "\n  ".join(bad))


def link_gate(path: Path, page: str):
    for href in re.findall(r'(?:href|src)="([^"#?:]+)(?:[#?][^"]*)?"', page):
        if href.startswith(("data", "//")) or not href:
            continue
        t = (path.parent / href).resolve()
        if t.is_dir():
            t = t / "index.html"
        if not t.exists():
            fail(f"{path.relative_to(ROOT)}: broken relative link {href}")


def post_gate(path: Path, page: str):
    for s in re.findall(r"(?s)<script[^>]*>(.*?)</script>", page):
        if re.search(r"""method\s*:\s*['"]POST|['"]POST['"]""", s, re.I):
            fail(f"{path.relative_to(ROOT)}: a page script names a POST")
        if re.search(r"/v1/(recall|ask|memory_token\b|memory_bundle|grid|locate|band_raster|range_hash|attest)", s):
            fail(f"{path.relative_to(ROOT)}: a page script names an emem write or minting endpoint")


def fonts(chars: str):
    from fontTools import subset
    from fontTools.ttLib import TTFont
    out = DOCS / "assets" / "fonts"
    out.mkdir(parents=True, exist_ok=True)
    codepoints = sorted({ord(c) for c in chars if ord(c) >= 32} | set(range(0x20, 0x7F)) | set(range(0xA0, 0x100)))
    for src, dst in FONTS:
        f = TTFont(FONT_SRC / f"{src}.ttf")
        opts = subset.Options()
        opts.flavor, opts.layout_features, opts.name_IDs, opts.notdef_outline = "woff2", ["kern", "liga", "tnum", "zero"], ["*"], True
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=codepoints)
        sub.subset(f)
        f.flavor = "woff2"
        f.save(out / f"{dst}.woff2")
    shutil.copy(ROOT / "poster" / "fonts" / "OFL-IBM-Plex.txt", out / "OFL.txt")
    (out / "README.txt").write_text("IBM Plex Sans and IBM Plex Mono, copyright IBM Corp., licensed under the SIL Open Font License 1.1 (OFL.txt).\n"
                                    "Subset to the characters these pages use by poster/build_site.py from poster/fonts/plex-full/.\n"
                                    "The Reserved Font Name 'Plex' is kept; the subsets are not renamed fonts offered on their own.\n")
    return {p.name: p.stat().st_size for p in sorted(out.glob("*.woff2"))}


def qr_svg(matrix, payload, total_mm):
    n = len(matrix)
    d = "".join(f"M{x} {y}h1v1h-1z" for y, row in enumerate(matrix) for x, v in enumerate(row) if v)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" width="{total_mm:.2f}mm" height="{total_mm:.2f}mm" shape-rendering="crispEdges">'
            f"<title>{htmllib.escape(payload)}</title><rect width=\"{n}\" height=\"{n}\" fill=\"#fff\"/><path fill=\"#000\" d=\"{d}\"/></svg>\n")


def svg_raster(svg: str, px: int):
    """Rasterise one of our QR SVGs. cairosvg when installed; otherwise read the module squares back from the file."""
    import numpy as np
    try:
        import cairosvg, io
        from PIL import Image
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=px, output_height=px)
        return np.array(Image.open(io.BytesIO(png)).convert("L")), "cairosvg"
    except ImportError:
        pass
    n = int(re.search(r'viewBox="0 0 (\d+) \1"', svg).group(1))
    grid = np.full((n, n), 255, np.uint8)
    for x, y in re.findall(r"M(\d+) (\d+)h1v1h-1z", svg):
        grid[int(y), int(x)] = 0
    idx = (np.arange(px) * n // px)
    return grid[np.ix_(idx, idx)], "svg module parser"


def qrcodes():
    import qrcode, cv2
    QR_DIR.mkdir(parents=True, exist_ok=True)
    det, rows = cv2.QRCodeDetector(), []
    for slug, cta, p, mm in QRS:
        payload = BASE + p
        q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=4)
        q.add_data(payload)
        q.make(fit=True)
        m = q.get_matrix()  # includes the 4-module quiet zone
        module_mm = mm / q.modules_count
        total_mm = module_mm * len(m)
        svg = qr_svg(m, payload, total_mm)
        (QR_DIR / f"qr_{slug}.svg").write_text(svg)
        (QR_DIR / f"qr_{slug}.txt").write_text(payload + "\n")
        px = round(total_mm / 25.4 * 300)  # 300 dpi at print size, quiet zone included
        img, how = svg_raster((QR_DIR / f"qr_{slug}.svg").read_text(), px)
        got, _, _ = det.detectAndDecode(img)
        if got != payload:
            fail(f"qr_{slug}.svg decodes to {got!r}, not {payload!r}")
        rows.append(dict(slug=slug, cta=cta, payload=payload, ecc="Q", version=q.version, modules=q.modules_count,
                         quiet_zone_modules=4, symbol_mm=mm, with_quiet_zone_mm=round(total_mm, 2), module_mm=round(module_mm, 3), raster_px=px, raster_dpi=300,
                         rasteriser=how, decoded=got, decoded_equals_payload=True))
    (QR_DIR / "qr_manifest.json").write_text(json.dumps(rows, indent=1) + "\n")
    return rows


def main():
    run([sys.executable, str(ROOT / "poster" / "ecosystem.py")])
    if not (TOOLS / "node_modules" / "@noble" / "hashes").exists():
        fail("run `npm ci --prefix tools/site` first")
    run(["node", str(TOOLS / "build.mjs"), str(ROOT), str(DOCS / "demo")])
    run(["node", str(TOOLS / "site.mjs"), str(ROOT), str(DOCS)])
    (DOCS / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy(TOOLS / "site.css", DOCS / "assets" / "site.css")
    (DOCS / ".nojekyll").write_text("")
    pages = sorted(DOCS.rglob("*.html"))
    chars = ""
    for p in pages:
        s = p.read_text()
        t = visible_text(s)
        prose_gate(str(p.relative_to(ROOT)), t)
        link_gate(p, s)
        post_gate(p, s)
        chars += t + "".join(re.findall(r"(?s)<script[^>]*>(.*?)</script>", s))
    tr = (DOCS / "demo" / "transcript.txt").read_text()
    prose_gate("docs/demo/transcript.txt", tr)
    sizes = fonts(chars + tr)
    rows = qrcodes()
    print(json.dumps({"pages": [str(p.relative_to(DOCS)) for p in pages], "fonts_bytes": sizes,
                      "qr": [(r["slug"], r["version"], r["modules"], r["decoded_equals_payload"], r["rasteriser"]) for r in rows]}, indent=1))
    if "--test" in sys.argv:
        run(["node", str(TOOLS / "test_site.mjs"), str(DOCS)])
    print("site build OK")


if __name__ == "__main__":
    main()
