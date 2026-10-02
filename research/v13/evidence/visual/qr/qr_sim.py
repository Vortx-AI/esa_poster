# Software decode test (OpenCV 5.0.0 QRCodeDetector): render a QR at k px per module, blur (sigma 0.6 px, defocus/motion proxy), add noise, decode.
import qrcode, numpy as np, cv2, json
rng=np.random.default_rng(0)
def render(u, ppm, ec=qrcode.constants.ERROR_CORRECT_M):
    q=qrcode.QRCode(error_correction=ec,border=4,box_size=1); q.add_data(u); q.make(fit=True)
    m=np.array(q.get_matrix(),dtype=np.uint8); img=(1-m)*255
    big=cv2.resize(img.astype(np.float32),None,fx=ppm*10,fy=ppm*10,interpolation=cv2.INTER_NEAREST)
    small=cv2.resize(big,None,fx=0.1,fy=0.1,interpolation=cv2.INTER_AREA)
    small=cv2.GaussianBlur(small,(0,0),0.6)+rng.normal(0,6,small.shape)
    canvas=np.full((small.shape[0]+40,small.shape[1]+40),235,np.float32); canvas[20:-20,20:-20]=small
    return np.clip(canvas,0,255).astype(np.uint8), q.version
det=cv2.QRCodeDetector()
out={}
for name,u in [('demo v4','https://vortx-ai.github.io/esa_poster/demo/'),('token v7','https://emem.dev/verify?q=emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa')]:
    res=[]
    for ppm in [1.2,1.5,1.8,2.0,2.5,3.0,4.0]:
        ok=0
        for t in range(10):
            img,v=render(u,ppm); s,_,_=det.detectAndDecode(img); ok+= (s==u)
        res.append((ppm,ok))
    out[name]=res
print(json.dumps(out))
