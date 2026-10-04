#!/usr/bin/env python3
"""Build the two visiting cards from fixed artwork and editable, vector-set copy.

Run from any directory: python cards/build_cards.py
No network or image-generation call is made by this reproducible build.
"""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path

import fitz
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "output"
CFG = json.loads((HERE / "content.json").read_text())
TW, TH = CFG["trim_mm"]
B = CFG["bleed_mm"]
PW, PH = TW + 2 * B, TH + 2 * B
INK = HexColor("#07132B")
FONTS = ROOT / "poster/fonts/plex-full"


def register_fonts():
    for name, file in (
        ("PlexBold", "IBMPlexSans-Bold.ttf"),
        ("PlexMedium", "IBMPlexSans-Medium.ttf"),
        ("PlexRegular", "IBMPlexSans-Regular.ttf"),
    ):
        pdfmetrics.registerFont(TTFont(name, str(FONTS / file)))


def line(c, text, baseline_from_top, size, font="PlexBold", x=8.2):
    """All card copy is real text with embedded fonts, independent of the artwork."""
    c.setFillColor(INK)
    c.setFont(font, size)
    c.drawString(x * mm, (PH - baseline_from_top) * mm, text)


def artwork(c, side):
    path = HERE / "assets" / ("encode-artwork.png" if side == "front" else "decode-artwork.png")
    iw, ih = Image.open(path).size
    if side == "front":
        # Cover the entire media box: the Earth continues through the 3 mm bleed.
        scale = max(PW / iw, PH / ih)
        w, h = iw * scale, ih * scale
        x, y = (PW - w) / 2, (PH - h) / 2
    else:
        # The white reverse has no edge artwork. Keep every instrument inside trim.
        scale = min(TW / iw, TH / ih)
        w, h = iw * scale, ih * scale
        x, y = B + (TW - w) / 2, B + (TH - h) / 2
    c.drawImage(str(path), x * mm, y * mm, width=w * mm, height=h * mm)
    return min(iw / (w / 25.4), ih / (h / 25.4))


def draw_face(c, person, side):
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, PW * mm, PH * mm, fill=1, stroke=0)
    ppi = artwork(c, side)
    for copy, baseline in zip(CFG[side]["headline"], (17.4, 27.1)):
        line(c, copy, baseline, 25.5)
    if side == "front":
        line(c, person["name"], 43.1, 11.5)
        line(c, person["email"], 48.0, 8.5, "PlexMedium")
    else:
        for copy, baseline in zip(CFG["back"]["tagline"], (40.3, 44.7)):
            line(c, copy, baseline, 9.8, "PlexMedium")
        line(c, CFG["back"]["website"], 52.8, 10.5)
    return ppi


def write_pdf(person):
    stream = io.BytesIO()
    c = canvas.Canvas(stream, pagesize=(PW * mm, PH * mm), pageCompression=1, invariant=1)
    c.setTitle(f"{person['name']} | emem visiting card")
    c.setAuthor("Vortx AI")
    c.setSubject("85 x 55 mm duplex visiting card, 3 mm bleed; page 1 front, page 2 reverse")
    ppis = []
    for side in ("front", "back"):
        ppis.append(draw_face(c, person, side))
        c.showPage()
    c.save()
    reader = PdfReader(stream)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    for page in writer.pages:
        page.trimbox = RectangleObject([B * mm, B * mm, (B + TW) * mm, (B + TH) * mm])
        page.bleedbox = RectangleObject([0, 0, PW * mm, PH * mm])
        page.cropbox = RectangleObject([0, 0, PW * mm, PH * mm])
    dest = OUT / f"emem-card-{person['slug']}.pdf"
    with dest.open("wb") as f:
        writer.write(f)
    return dest, ppis


def validate_and_render(path, person, ppis):
    """Preflight the delivered pages and render their trimmed faces for visual QA."""
    reader = PdfReader(path)
    assert len(reader.pages) == 2
    expected = [
        CFG["front"]["headline"] + [person["name"], person["email"]],
        CFG["back"]["headline"] + CFG["back"]["tagline"] + [CFG["back"]["website"]],
    ]
    font_names = set()
    doc = fitz.open(path)
    previews = []
    text_sizes = []
    for i, (page, phrases) in enumerate(zip(reader.pages, expected)):
        assert page.extract_text().splitlines() == phrases
        assert abs(float(page.trimbox.width) / mm - TW) < 0.001
        assert abs(float(page.trimbox.height) / mm - TH) < 0.001
        assert abs(float(page.mediabox.width) / mm - PW) < 0.001
        assert abs(float(page.mediabox.height) / mm - PH) < 0.001
        for ref in page["/Resources"]["/Font"].values():
            f = ref.get_object()
            if "/FontDescriptor" in f:
                desc = f["/FontDescriptor"].get_object()
                assert "/FontFile2" in desc or "/FontFile3" in desc
                font_names.add(str(f["/BaseFont"]))
            # ReportLab's unused base Helvetica resource is not drawn.
        fp = doc[i]
        for block in fp.get_text("dict")["blocks"]:
            for row in block.get("lines", []):
                for span in row["spans"]:
                    if not span["text"].strip():
                        continue
                    text_sizes.append(span["size"])
                    x0, y0, x1, y1 = span["bbox"]
                    safe = (B + 3) * mm
                    assert x0 >= safe and y0 >= safe
                    assert x1 <= (PW - B - 3) * mm and y1 <= (PH - B - 3) * mm
        clip = fitz.Rect(B * mm, B * mm, (B + TW) * mm, (B + TH) * mm)
        pix = fp.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72), clip=clip, alpha=False)
        side = ("front", "back")[i]
        png = OUT / f"emem-card-{person['slug']}-{side}.png"
        pix.save(str(png))
        previews.append(png)
    assert min(text_sizes) >= 8.49
    assert min(ppis) >= 300
    doc.close()
    return {
        "file": path.name,
        "pages": 2,
        "trim_mm": [TW, TH],
        "media_and_bleed_mm": [PW, PH],
        "minimum_copy_pt": round(min(text_sizes), 1),
        "minimum_artwork_ppi": round(min(ppis), 1),
        "fonts_embedded": sorted(font_names),
        "exact_copy_verified": True,
        "copy_safe_margin_mm": 3,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }, previews


def make_preview(rows):
    # A presentation contact sheet; its whitespace is not part of either card.
    cards = [[Image.open(p).convert("RGB") for p in pair] for pair in rows]
    w, h = cards[0][0].size
    pad, gap = 60, 35
    board = Image.new("RGB", (2 * w + 2 * pad + gap, 2 * h + 2 * pad + gap), "#E9EDF1")
    for r, pair in enumerate(cards):
        for col, im in enumerate(pair):
            board.paste(im, (pad + col * (w + gap), pad + r * (h + gap)))
    board.save(OUT / "emem-cards-preview.png", dpi=(300, 300))


def main():
    OUT.mkdir(exist_ok=True)
    register_fonts()
    report, previews = [], []
    for person in CFG["people"]:
        path, ppis = write_pdf(person)
        entry, renders = validate_and_render(path, person, ppis)
        report.append(entry)
        previews.append(renders)
    make_preview(previews)
    result = {"colour": "RGB master; printer-managed conversion", "cards": report}
    (OUT / "preflight.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
