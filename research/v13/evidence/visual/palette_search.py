import itertools, numpy as np
from palette_check import hex2rgb, lab, cvd, ciede2000, fogra_roundtrip, contrast
FIXED = {"emem": "#0F5FA8", "harm": "#D2481E", "incident": "#E8A317", "oos": "#9C9A92", "ink": "#16181D"}
A_C = ["#7C4D9E", "#8C5A2B", "#6E4A2E", "#A0522D", "#5D3A1A", "#B07AA1", "#8E6C8A", "#5E2B5B", "#6A3D9A", "#7F3B08", "#4E3B31", "#9D5B8B", "#2F2F2F"]
B_C = ["#1E8A72", "#117733", "#2E7D32", "#4D9221", "#3B7A57", "#00796B", "#44AA99", "#5AAE61", "#1B7837", "#35978F", "#01665E", "#66A61E"]
kinds = ["normal", "protanomaly", "deuteranomaly", "tritanomaly"]
def mind(cols):
    m = 1e9; arg=None
    for (na, a), (nb, b) in itertools.combinations(cols.items(), 2):
        for k in kinds:
            d = ciede2000(lab(cvd(hex2rgb(a), k)), lab(cvd(hex2rgb(b), k)))
            if d < m: m, arg = d, (na, nb, k)
    return m, arg
res = []
for a in A_C:
    for b in B_C:
        cols = dict(FIXED, A=a, B=b)
        m, arg = mind(cols)
        res.append((m, a, b, arg, fogra_roundtrip(a)[2], fogra_roundtrip(b)[2], contrast(hex2rgb(a), hex2rgb('#FFFFFF')), contrast(hex2rgb(b), hex2rgb('#FFFFFF'))))
res.sort(reverse=True)
for r in res[:10]: print(f"min dE00 {r[0]:5.1f} A {r[1]} B {r[2]} worst {r[3]} fograA {r[4]:.2f} fograB {r[5]:.2f} contrastA {r[6]:.1f} B {r[7]:.1f}")
m, arg = mind(FIXED); print('fixed set alone', round(m,1), arg)
