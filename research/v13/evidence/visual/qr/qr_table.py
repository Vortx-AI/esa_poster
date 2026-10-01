import qrcode, math, json, numpy as np, cv2
from PIL import Image, ImageFilter
P = {
 'VIEW THE DEMO': 'https://vortx-ai.github.io/esa_poster/demo/',
 'TRY A TOKEN': 'https://emem.dev/verify?q=emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa',
 'INSPECT THE RECORD': 'https://vortx-ai.github.io/esa_poster/demo/record.html',
 'RE-RUN THE TEST': 'https://github.com/Vortx-AI/esa_poster/tree/main/research/repro/v13',
 'READ THE METHODS': 'https://github.com/Vortx-AI/esa_poster/blob/main/research/repro/v13/METHODS.md',
 'DISCOVER INTEGRATIONS': 'https://vortx-ai.github.io/esa_poster/use/',
 'v12 qr_try': 'https://emem.dev/verify',
 'v12 qr_repro': 'https://github.com/Vortx-AI/esa_poster/tree/main/research/repro/v12',
 'ememdemo valid token': 'https://vortx-ai.github.io/ememdemo/?s=emem%3Afact%3Adefi.zb572.xoso.zb1ec%3Aoj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa',
 'emem.dev/#use': 'https://emem.dev/#use',
}
# phone model (INFERRED): scanner preview 1920 px across a 70 deg horizontal field of view; decode needs >= 3 px per module
def mm_per_px(d_mm, px=1920, fov=70): return 2*d_mm*math.tan(math.radians(fov/2))/px
rows=[]
for k,u in P.items():
    for ec,nm in [(qrcode.constants.ERROR_CORRECT_M,'M'),(qrcode.constants.ERROR_CORRECT_Q,'Q')]:
        q=qrcode.QRCode(error_correction=ec,border=4); q.add_data(u); q.make(fit=True)
        n=q.modules_count
        need={d: round(3*mm_per_px(d)*n,1) for d in (500,1000)}  # symbol width, quiet zone excluded
        rows.append(dict(cta=k,url=u,chars=len(u),ecc=nm,version=q.version,modules=n,width_mm_for_0_5m=need[500],width_mm_for_1m=need[1000]))
print(json.dumps(rows,indent=0))
