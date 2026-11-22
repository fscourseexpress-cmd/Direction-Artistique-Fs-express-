"""Retouches des photos de la semaine 1 (v2). Lancer depuis assets/v2."""
import cv2, numpy as np
from PIL import Image

def recolor(bgr, region, hue, s_mul, v_mul, hmin, hmax, smin, vmin, blur=5):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    H,S,V = hsv[...,0], hsv[...,1], hsv[...,2]
    sel = ((H>=hmin)&(H<=hmax)&(S>=smin)&(V>=vmin)).astype(np.float32)*(region.astype(np.float32)/255)
    sel = cv2.GaussianBlur(sel,(blur,blur),0)
    new = hsv.copy(); new[...,0]=hue; new[...,1]=np.clip(S*s_mul,0,255); new[...,2]=np.clip(V*v_mul,0,255)
    nb = cv2.cvtColor(new.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    return (bgr.astype(np.float32)*(1-sel[...,None]) + nb*sel[...,None]).clip(0,255).astype(np.uint8)

def cutout(path, out, extra_fg=None):
    bgr = cv2.imread(path); h,w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    S,V = hsv[...,1].astype(int), hsv[...,2].astype(int)
    m = np.full((h,w), cv2.GC_PR_FGD, np.uint8)
    m[(S<28)&(V>190)] = cv2.GC_PR_BGD
    m[:4,:] = cv2.GC_BGD; m[:, :4] = cv2.GC_BGD
    bg, fg = np.zeros((1,65),np.float64), np.zeros((1,65),np.float64)
    cv2.grabCut(bgr, m, None, bg, fg, 6, cv2.GC_INIT_WITH_MASK)
    a = np.where((m==cv2.GC_FGD)|(m==cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    # garder la plus grande zone, adoucir les bords
    n, lab, st, _ = cv2.connectedComponentsWithStats(a)
    if n > 1:
        big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); a = np.where(lab==big, 255, 0).astype(np.uint8)
    a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
    a = cv2.GaussianBlur(a, (3,3), 0)
    rgba = np.dstack([cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB), a])
    Image.fromarray(rgba, 'RGBA').save(out)

# 1. Livreur au sac repas : casque orange -> rouge FS Express, puis détourage
b = cv2.imread('livreur-sac-repas.jpg'); h,w = b.shape[:2]
helmet = np.zeros((h,w),np.uint8); helmet[0:260, 180:560] = 255
b = recolor(b, helmet, 2, 0.95, 0.75, 4, 24, 90, 80)
cv2.imwrite('livreur-sac-repas-fs.jpg', b, [cv2.IMWRITE_JPEG_QUALITY, 95])
cutout('livreur-sac-repas-fs.jpg', 'livreur-sac-repas-detoure.png')

# 2. Livreur sur scooter rouge : détourage
cutout('livreur-scooter-rouge.jpg', 'livreur-scooter-detoure.png')

# 3. Rue de Yaoundé : jaunes (taxis, casques) désaturés
b = cv2.imread('rue-yaounde@2x.jpg'); h,w = b.shape[:2]
hsv = cv2.cvtColor(b, cv2.COLOR_BGR2HSV).astype(np.float32)
sel = ((hsv[...,0]>=15)&(hsv[...,0]<=36)&(hsv[...,1]>=110)&(hsv[...,2]>=110)).astype(np.float32)
sel = cv2.GaussianBlur(sel,(5,5),0)
hsv[...,1] = hsv[...,1]*(1-0.88*sel)
cv2.imwrite('rue-yaounde-fs@2x.jpg', cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR), [cv2.IMWRITE_JPEG_QUALITY, 93])

# 4. Palette de colis : logos générés (mal orthographiés) remplacés par le vrai logo
b = cv2.imread('colis-palette@2x.jpg'); h,w = b.shape[:2]
spots = [(135,385,205,485),(690,470,760,545),(85,580,160,690),(320,655,395,760),(510,640,615,765),(760,595,835,700),(320,190,445,315)]
hsv = cv2.cvtColor(b, cv2.COLOR_BGR2HSV); H,S = hsv[...,0].astype(int), hsv[...,1].astype(int)
ink = (((H>=80)&(H<=140)&(S>=35)) | (((H<=7)|(H>=165))&(S>=80))).astype(np.uint8)*255
rng = np.random.default_rng(3)
for x0,y0,x1,y1 in spots:
    X0,Y0,X1,Y1 = x0-10,y0-10,x1+10,y1+10
    ring = np.concatenate([b[Y0-6:Y0, X0:X1].reshape(-1,3), b[Y1:Y1+6, X0:X1].reshape(-1,3), b[Y0:Y1, X0-6:X0].reshape(-1,3), b[Y0:Y1, X1:X1+6].reshape(-1,3)])
    ink_ring = ring[(np.abs(ring[:,2].astype(int)-ring[:,0].astype(int))>20)]
    col = np.median(ink_ring if len(ink_ring) > 20 else ring, axis=0)
    patch = np.ones((Y1-Y0, X1-X0, 3), np.float32)*col + rng.normal(0, 3.5, (Y1-Y0, X1-X0, 1))
    m = np.zeros((Y1-Y0, X1-X0), np.float32); m[6:-6, 6:-6] = 1; m = cv2.GaussianBlur(m, (11,11), 0)[...,None]
    region = b[Y0:Y1, X0:X1].astype(np.float32)
    b[Y0:Y1, X0:X1] = (region*(1-m) + patch*m).clip(0,255).astype(np.uint8)
logo = cv2.imread('../logo.jpg').astype(np.float32)
out = b.astype(np.float32)
for x0,y0,x1,y1 in spots:
    sw, sh = x1-x0, y1-y0
    s = min(sw/logo.shape[1], sh/logo.shape[0])
    lg = cv2.resize(logo, (max(1,int(logo.shape[1]*s)), max(1,int(logo.shape[0]*s))), interpolation=cv2.INTER_AREA)
    # opacité = écart au blanc : le fond blanc du logo disparaît, les couleurs restent fidèles
    al = np.clip((255 - lg.min(axis=2)) / 120.0, 0, 1)[..., None] * 0.95
    ox = x0 + (sw-lg.shape[1])//2; oy = y0 + (sh-lg.shape[0])//2
    reg = out[oy:oy+lg.shape[0], ox:ox+lg.shape[1]]
    out[oy:oy+lg.shape[0], ox:ox+lg.shape[1]] = reg*(1-al) + lg*al
cv2.imwrite('colis-palette-fs@2x.jpg', out.clip(0,255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 93])
print('ok')

# 5. Téléphone + carnet : écran vert remplacé par un écran FS Express (Vendu / Encaissé / En attente)
from PIL import ImageDraw, ImageFont
def font(size, bold=True):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
              '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf']:
        try: return ImageFont.truetype(p, size)
        except OSError: pass
    return ImageFont.load_default()
W, H = 360, 740
ui = Image.new('RGB', (W, H), (234, 247, 253)); d = ImageDraw.Draw(ui)
d.rectangle([0, 0, W, 120], fill=(10, 61, 87)); d.text((24, 52), "Mes ventes du jour", font=font(26), fill='white')
rows = [("Vendu", "54 500 F", (10, 61, 87)), ("Encaissé", "33 000 F", (22, 144, 193)), ("En attente", "21 500 F", (147, 36, 30))]
y = 160
for lab, val, col in rows:
    d.rounded_rectangle([18, y, W-18, y+150], 22, fill='white')
    d.text((40, y+22), lab, font=font(24, False), fill=(91, 107, 118)); d.text((40, y+62), val, font=font(44), fill=col)
    y += 172
d.rounded_rectangle([18, y+6, W-18, y+76], 35, fill=(147, 36, 30)); d.text((60, y+26), "Relancer le livreur", font=font(24), fill='white')
src = np.float32([[0,0],[W,0],[W,H],[0,H]])
dst = np.float32([[407,292],[578,302],[500,646],[338,630]])
M = cv2.getPerspectiveTransform(src, dst)
b = cv2.imread('tel-carnet@2x.jpg'); h, w = b.shape[:2]
warp = cv2.warpPerspective(cv2.cvtColor(np.array(ui), cv2.COLOR_RGB2BGR), M, (w, h))
quad = np.zeros((h, w), np.uint8); cv2.fillConvexPoly(quad, dst.astype(np.int32), 255)
hsv = cv2.cvtColor(b, cv2.COLOR_BGR2HSV); Hh, Ss = hsv[...,0].astype(int), hsv[...,1].astype(int)
skin = ((Hh <= 22) & (Ss >= 60)).astype(np.uint8) * 255          # les doigts ne sont pas recouverts
interior = cv2.erode(quad, np.ones((45,45),np.uint8))          # le centre de l'écran est toujours remplacé
m = cv2.bitwise_and(cv2.erode(quad, np.ones((3,3),np.uint8)), cv2.bitwise_not(skin)) | interior
m = cv2.GaussianBlur(m.astype(np.float32)/255, (3,3), 0)[..., None]
b = (b.astype(np.float32)*(1-m) + warp.astype(np.float32)*m).clip(0,255).astype(np.uint8)
cv2.imwrite('tel-carnet-fs@2x.jpg', b, [cv2.IMWRITE_JPEG_QUALITY, 93])
print('écran remplacé')
