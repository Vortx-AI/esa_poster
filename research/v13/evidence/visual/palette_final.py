import itertools
from palette_check import hex2rgb, lab, cvd, ciede2000, fogra_roundtrip, contrast
kinds = ["normal", "protanomaly", "deuteranomaly", "tritanomaly"]
for name, S in {
 "final (agents neutral-warm/neutral-cool)": {"EMEM": "#0F5FA8", "harm": "#D2481E", "incident": "#E8A317", "out-of-scope": "#9C9A92", "ink": "#16181D", "agentA": "#7A5230", "agentB": "#3D5566"},
 "no agents": {"EMEM": "#0F5FA8", "harm": "#D2481E", "incident": "#E8A317", "out-of-scope": "#9C9A92", "ink": "#16181D"},
}.items():
    m = (1e9, None); rows=[]
    for (na, a), (nb, b) in itertools.combinations(S.items(), 2):
        ds = [ciede2000(lab(cvd(hex2rgb(a), k)), lab(cvd(hex2rgb(b), k))) for k in kinds]
        rows.append((min(ds), na, nb, ds))
        for k, d in zip(kinds, ds):
            if d < m[0]: m = (d, (na, nb, k))
    print(name, "min dE00 %.1f" % m[0], m[1])
    for r in sorted(rows)[:6]: print("   %-12s %-12s " % (r[1], r[2]) + " ".join("%5.1f" % d for d in r[3]))
    for n, h in S.items():
        cm, back, de = fogra_roundtrip(h); print("   %-12s %s CMYK%s dE00(FOGRA39) %.2f  contrast %.1f" % (n, h, cm, de, contrast(hex2rgb(h), hex2rgb('#FFFFFF'))))
