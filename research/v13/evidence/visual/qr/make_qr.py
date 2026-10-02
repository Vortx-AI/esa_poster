# Proposed QR set: ECC Q, 4-module quiet zone inside the symbol, one SVG + one 300-dpi PNG each; decode-gate every PNG.
import qrcode, qrcode.image.svg, numpy as np, cv2, json, hashlib
from PIL import Image
SET = [('VIEW THE DEMO','demo','https://vortx-ai.github.io/esa_poster/demo/',70),
       ('TRY A TOKEN','t','https://vortx-ai.github.io/esa_poster/t/',40),
       ('INSPECT THE RECORD','r','https://vortx-ai.github.io/esa_poster/r/',40),
       ('RE-RUN THE TEST','test','https://vortx-ai.github.io/esa_poster/test/',40),
       ('READ THE METHODS','methods','https://vortx-ai.github.io/esa_poster/methods/',40),
       ('DISCOVER INTEGRATIONS','use','https://vortx-ai.github.io/esa_poster/use/',40)]
det = cv2.QRCodeDetector(); out=[]
for cta, slug, url, mm in SET:
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=4, box_size=10); q.add_data(url); q.make(fit=True)
    q.make_image(image_factory=qrcode.image.svg.SvgPathImage).save(f'qr_{slug}.svg')
    total_modules = q.modules_count + 8; px = round(mm / 25.4 * 300)  # symbol + quiet zone printed at mm
    img = q.make_image(fill_color='black', back_color='white').convert('L').resize((px, px), Image.NEAREST); img.save(f'qr_{slug}_300dpi.png')
    s, _, _ = det.detectAndDecode(np.array(img))
    out.append(dict(cta=cta, url=url, version=q.version, modules=q.modules_count, printed_mm_incl_quiet_zone=mm, module_mm=round(mm/total_modules,2), decoded_equals_payload=(s==url), svg_sha256=hashlib.sha256(open(f'qr_{slug}.svg','rb').read()).hexdigest()[:16]))
print(json.dumps(out, indent=0))
