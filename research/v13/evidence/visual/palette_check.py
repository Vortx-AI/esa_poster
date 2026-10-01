"""Palette check for the v13 board: CVD separation (Machado 2009, severity 100) and FOGRA39 round-trip.

usage: vis_venv/bin/python palette_check.py > palette_check.txt
Needs: colorspacious (CVD + CIELab), Pillow ImageCms (LittleCMS), Adobe CoatedFOGRA39.icc in ./icc/.
"""
import io
import itertools
import math
from pathlib import Path

import numpy as np
from colorspacious import cspace_convert
from PIL import Image, ImageCms

HERE = Path(__file__).parent
FOGRA = HERE / "icc" / "Adobe ICC Profiles (end-user)" / "CMYK" / "CoatedFOGRA39.icc"


def hex2rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float) / 255


def ciede2000(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cm = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cm ** 7 / (Cm ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    dh = h2p - h1p
    if C1p * C2p == 0:
        dh = 0
    elif dh > 180:
        dh -= 360
    elif dh < -180:
        dh += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dh / 2))
    Lpm, Cpm = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hpm = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hpm = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hpm = (h1p + h2p + 360) / 2
    else:
        hpm = (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hpm - 30)) + 0.24 * math.cos(math.radians(2 * hpm))
         + 0.32 * math.cos(math.radians(3 * hpm + 6)) - 0.20 * math.cos(math.radians(4 * hpm - 63)))
    dth = 30 * math.exp(-(((hpm - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cpm ** 7 / (Cpm ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lpm - 50) ** 2 / math.sqrt(20 + (Lpm - 50) ** 2)
    Sc = 1 + 0.045 * Cpm
    Sh = 1 + 0.015 * Cpm * T
    Rt = -math.sin(math.radians(2 * dth)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def lab(rgb01):
    return cspace_convert(np.clip(rgb01, 0, 1), "sRGB1", "CIELab")


def cvd(rgb01, kind):
    if kind == "normal":
        return rgb01
    sp = {"cvd_type": kind, "severity": 100}
    return np.clip(cspace_convert(rgb01, {"name": "sRGB1+CVD", **sp}, "sRGB1"), 0, 1)


def rel_lum(rgb01):
    c = np.where(rgb01 <= 0.04045, rgb01 / 12.92, ((rgb01 + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = rel_lum(a) + 0.05, rel_lum(b) + 0.05
    return max(la, lb) / min(la, lb)


srgb = ImageCms.createProfile("sRGB")
cmyk = ImageCms.getOpenProfile(str(FOGRA))
to_cmyk = ImageCms.buildTransform(srgb, cmyk, "RGB", "CMYK", renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC)
to_rgb = ImageCms.buildTransform(cmyk, srgb, "CMYK", "RGB", renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC)


def fogra_roundtrip(h):
    im = Image.new("RGB", (1, 1), h)
    c = ImageCms.applyTransform(im, to_cmyk)
    back = ImageCms.applyTransform(c, to_rgb).getpixel((0, 0))
    cm = c.getpixel((0, 0))
    de = ciede2000(lab(hex2rgb(h)), lab(np.array(back, float) / 255))
    return tuple(round(v / 2.55) for v in cm), "#%02X%02X%02X" % back, de


PAPER = "#FFFFFF"
CANDIDATES = {
    # role: (hex, note)
    "ink": "#16181D",
    "ink2 (secondary text)": "#4A4D55",
    "muted (labels)": "#7A7D85",
    "rule": "#D5D6DA",
    "EMEM evidence / refused-at-check": "#0F5FA8",
    "EMEM tint (fills)": "#DCE8F5",
    "harm: acted on corrupted evidence": "#D2481E",
    "harm tint": "#FADDD2",
    "real incident (seen in production)": "#E8A317",
    "out of scope / not established": "#9C9A92",
    "agent A (sender)": "#7C4D9E",
    "agent B (receiver)": "#1E8A72",
    "v12 acc #1F4FD8": "#1F4FD8",
    "v12 bad #B3261E": "#B3261E",
    "v12 amb #A86B00": "#A86B00",
    "Okabe-Ito blue": "#0072B2",
    "Okabe-Ito vermillion": "#D55E00",
    "Okabe-Ito orange": "#E69F00",
    "Okabe-Ito bluish green": "#009E73",
    "Okabe-Ito reddish purple": "#CC79A7",
    "IBM blue 60": "#0F62FE",
}
SEMANTIC = ["EMEM evidence / refused-at-check", "harm: acted on corrupted evidence", "real incident (seen in production)",
            "out of scope / not established", "agent A (sender)", "agent B (receiver)", "ink"]

print("== FOGRA39 (Adobe CoatedFOGRA39.icc) round trip, relative colorimetric; dE00 sRGB vs round trip ==")
print(f"{'role':40s} {'hex':8s} {'CMYK %':18s} {'back':8s} dE00  contrast-on-white")
for role, h in CANDIDATES.items():
    cm, back, de = fogra_roundtrip(h)
    print(f"{role:40s} {h:8s} {str(cm):18s} {back:8s} {de:5.2f} {contrast(hex2rgb(h), hex2rgb(PAPER)):5.2f}")

print()
print("== pairwise dE00 between semantic colours, normal and simulated CVD (Machado 2009, severity 100) ==")
kinds = ["normal", "protanomaly", "deuteranomaly", "tritanomaly"]
worst = {k: (1e9, None) for k in kinds}
for a, b in itertools.combinations(SEMANTIC, 2):
    row = []
    for k in kinds:
        ca, cb = cvd(hex2rgb(CANDIDATES[a]), k), cvd(hex2rgb(CANDIDATES[b]), k)
        d = ciede2000(lab(ca), lab(cb))
        row.append(d)
        if d < worst[k][0]:
            worst[k] = (d, (a, b))
    print(f"{a[:28]:28s} vs {b[:28]:28s} " + " ".join(f"{k[:5]} {d:5.1f}" for k, d in zip(kinds, row)))
print()
for k, (d, pair) in worst.items():
    print(f"worst pair under {k}: {d:.1f}  {pair}")

print()
print("== the v12 pair and the proposed pair under CVD (refused vs acted-on) ==")
for name, (x, y) in {"v12 #1F4FD8 vs #B3261E": ("#1F4FD8", "#B3261E"),
                     "v13 #0F5FA8 vs #D2481E": ("#0F5FA8", "#D2481E"),
                     "Okabe-Ito #0072B2 vs #D55E00": ("#0072B2", "#D55E00"),
                     "red vs green #B3261E vs #1E8A72": ("#B3261E", "#1E8A72")}.items():
    print(name, " ".join(f"{k[:5]} {ciede2000(lab(cvd(hex2rgb(x), k)), lab(cvd(hex2rgb(y), k))):5.1f}" for k in kinds))
