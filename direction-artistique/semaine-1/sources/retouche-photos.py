import cv2, numpy as np
from PIL import Image

def poly_mask(shape, polys, blur=5):
    m = np.zeros(shape[:2], np.uint8)
    for p in polys:
        cv2.fillPoly(m, [np.array(p, np.int32)], 255)
    return m

def recolor(bgr, region, hue, s_mul, v_mul, hmin=3, hmax=30, smin=80, vmin=50, blur=5):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    H,S,V = hsv[...,0], hsv[...,1], hsv[...,2]
    sel = ((H>=hmin)&(H<=hmax)&(S>=smin)&(V>=vmin)).astype(np.float32) * (region.astype(np.float32)/255)
    sel = cv2.GaussianBlur(sel, (blur,blur), 0)
    new = hsv.copy()
    new[...,0] = hue; new[...,1] = np.clip(S*s_mul,0,255); new[...,2] = np.clip(V*v_mul,0,255)
    newbgr = cv2.cvtColor(new.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    out = bgr.astype(np.float32)*(1-sel[...,None]) + newbgr*sel[...,None]
    return out.clip(0,255).astype(np.uint8), sel

# ---------- 1. Livreur souriant (détouré) ----------
rgba = np.array(Image.open('livreur-detoure.png').convert('RGBA'))
bgr = cv2.cvtColor(rgba[...,:3], cv2.COLOR_RGB2BGR)
sh = bgr.shape
polo = poly_mask(sh, [
  [(98,485),(100,400),(130,345),(195,315),(205,300),(300,300),(330,310),(400,335),(435,360),(445,420),(448,470),(410,478),(370,490),(330,505),(250,520),(180,505),(140,495),(98,492)],
  [(150,640),(210,615),(300,622),(370,612),(420,605),(445,640),(445,725),(150,725)]])
neck = poly_mask(sh, [[(203,250),(297,250),(297,318),(270,340),(230,340),(203,318)]])
skin = poly_mask(sh, [[(84,516),(152,516),(152,565),(84,565)], [(355,592),(452,592),(452,665),(355,665)]])
band = poly_mask(sh, [[(88,466),(170,472),(250,500),(330,500),(400,478),(448,466),(448,500),(340,512),(300,532),(250,540),(150,540),(88,516)]])
strip = poly_mask(sh, [[(150,530),(255,530),(255,558),(150,558)]])
excl = neck | skin
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
H,S,V = hsv[...,0], hsv[...,1], hsv[...,2]
inr = lambda m: (m>0) & ~(excl>0)
warm = (H<=30)
redw = (H>=168)|(H<=4)
sel = (inr(polo) & ((warm & (S>=70) & (V>=50)) | (redw & (S>=90)))) \
    | (inr(band) & ((warm & (S>=110) & (V>=110)) | (redw & (S>=90) & (V>=90)))) \
    | (inr(strip) & warm & (S>=150) & (V>=170))
selF = cv2.GaussianBlur(sel.astype(np.float32), (3,3), 0)
new = hsv.copy(); new[...,0]=98; new[...,1]=np.clip(S*0.92,0,255); new[...,2]=np.clip(V*0.74,0,255)
nb = cv2.cvtColor(new.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
bgr = (bgr.astype(np.float32)*(1-selF[...,None]) + nb*selF[...,None]).clip(0,255).astype(np.uint8)
helmet = poly_mask(sh, [[(148,165),(150,130),(175,105),(215,90),(270,88),(310,105),(330,135),(336,170),(310,158),(270,150),(220,150),(180,158)]])
lamps = poly_mask(sh, [[(5,850),(80,850),(80,920),(5,920)], [(310,805),(385,805),(385,875),(310,875)]])
bgr,_ = recolor(bgr, helmet, 2, 0.95, 0.72)
bgr,_ = recolor(bgr, lamps, 2, 0.95, 0.85, smin=60)
out = np.dstack([cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB), rgba[...,3]])
Image.fromarray(out, 'RGBA').save('livreur-fs.png')

# ---------- 2. Livreur de dos ----------
bgr = cv2.imread('dos.jpg'); sh = bgr.shape
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
H,S,V = hsv[...,0].astype(int), hsv[...,1].astype(int), hsv[...,2].astype(int)
box = poly_mask(sh, [[(165,538),(495,538),(495,772),(165,772)]])
magenta = (((H>=120)|(H<=3))&(S>=20)).astype(np.uint8)*255
tape = np.zeros(sh[:2], np.uint8); tape[512:562, 292:358] = 255; tape[735:782, 288:340] = 255
tape = cv2.bitwise_and(tape, ((H>=125)&(H<=172)&(S>=25)).astype(np.uint8)*255)
magenta = cv2.bitwise_and(magenta, box)
text = np.zeros(sh[:2], np.uint8); text[625:672, 250:382] = 255
text = cv2.bitwise_and(text, ((V<150)|(S>45)).astype(np.uint8)*255)
labels = np.zeros(sh[:2], np.uint8); labels[556:584, 415:475] = 255; labels[740:770, 415:490] = 255
mask = cv2.dilate(magenta|text|labels, np.ones((5,5),np.uint8), iterations=2)
mask = cv2.bitwise_and(mask, box) | cv2.dilate(tape, np.ones((5,5),np.uint8), iterations=2)
bgr = cv2.inpaint(bgr, mask, 6, cv2.INPAINT_NS)
# lumières orange de la rue -> rouge (hors carton)
notbox = cv2.bitwise_not(cv2.dilate(box, np.ones((9,9),np.uint8)))
bgr,_ = recolor(bgr, notbox, 2, 1.0, 0.95, hmin=4, hmax=26, smin=110, vmin=90, blur=7)
cv2.imwrite('dos-fs.jpg', bgr, [cv2.IMWRITE_JPEG_QUALITY, 95])
cv2.imwrite('dos-mask.png', mask)

# ---------- 3. Remise de commande ----------
bgr = cv2.imread('remise.jpg'); sh = bgr.shape
bag = poly_mask(sh, [[(328,360),(398,292),(505,298),(565,345),(662,436),(660,492),(525,575),(488,615),(468,565),(438,505),(378,445),(332,405)]])
handp = [(452,292),(498,292),(506,330),(500,394),(468,394),(452,350)]
bag = cv2.bitwise_and(bag, cv2.bitwise_not(poly_mask(sh, [handp])))
bgr,_ = recolor(bgr, bag, 99, 0.95, 0.66, hmin=0, hmax=24, smin=70, vmin=70, blur=5)
hsv3 = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV); wr = ((hsv3[...,0]>=168)&(hsv3[...,1]>=70)).astype(np.uint8)*255
bgr,_ = recolor(bgr, cv2.bitwise_and(bag, wr), 99, 0.95, 0.66, hmin=168, hmax=180, smin=70, vmin=60)
handz = cv2.dilate(poly_mask(sh, [handp]), np.ones((7,7),np.uint8))
bgr,_ = recolor(bgr, handz, 99, 0.95, 0.66, hmin=0, hmax=24, smin=150, vmin=160, blur=3)
cv2.imwrite('remise-fs.jpg', bgr, [cv2.IMWRITE_JPEG_QUALITY, 95])
print('ok')
