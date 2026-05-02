from PIL import Image
import os, math

BASE = r'C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\FLORES'
T=(0,0,0,0)
SG=(56,142,60,255); SD=(27,94,32,255); SE=(15,65,15,255); SL=(100,185,72,255)
LG=(80,165,56,255); LD=(44,108,28,255); LH=(118,195,78,255); LE=(28,85,18,255)

def new_img():
    img=Image.new('RGBA',(32,32),T); px=img.load()
    def d(x,y,c):
        if 0<=x<32 and 0<=y<32: px[x,y]=c
    return img,d

# ── Primitivos ────────────────────────────────────────────────────────────────
def petal(d,cx,cy,angle,plen,pw,cm,ch=None,ce=None):
    ca,sa=math.cos(angle),math.sin(angle)
    hl,hw=plen/2.0,pw/2.0; pcx,pcy=cx+hl*ca,cy+hl*sa; R=plen+pw
    for y in range(max(0,int(pcy-R)),min(32,int(pcy+R)+1)):
        for x in range(max(0,int(pcx-R)),min(32,int(pcx+R)+1)):
            dx,dy=x-pcx,y-pcy; lx=dx*ca+dy*sa; ly=-dx*sa+dy*ca
            if hl>0 and hw>0 and (lx/hl)**2+(ly/hw)**2<=1.0:
                f=(lx/hl)**2+(ly/hw)**2
                if f>0.68 and ce: c=ce
                elif lx/hl>0.45 and ch: c=ch
                else: c=cm
                d(x,y,c)

def leaf(d,ax,ay,angle,length,width):
    """Hoja con nervio central oscuro."""
    petal(d,ax,ay,angle,length,width,LG,LH,LD)
    ca,sa=math.cos(angle),math.sin(angle)
    for t in range(1,int(length*0.78)):
        d(int(ax+t*ca),int(ay+t*sa),LD)

def circle(d,cx,cy,r,cf,cc=None,ce=None):
    for y in range(max(0,cy-r-1),min(32,cy+r+2)):
        for x in range(max(0,cx-r-1),min(32,cx+r+2)):
            dist=math.sqrt((x-cx)**2+(y-cy)**2)
            if dist<=r+0.5:
                if ce and dist>r-0.9: c=ce
                elif cc and dist<r*0.4: c=cc
                else: c=cf
                d(x,y,c)

def ring(d,cx,cy,ri,ro,cf,ce=None):
    for y in range(max(0,cy-ro-1),min(32,cy+ro+2)):
        for x in range(max(0,cx-ro-1),min(32,cx+ro+2)):
            dist=math.sqrt((x-cx)**2+(y-cy)**2)
            if ri-0.3<=dist<=ro+0.4:
                c=(ce if ce and (dist>ro-0.8 or dist<ri+0.8) else cf)
                d(x,y,c)

def save(name,flower_fn,sfull,sshort):
    folder=os.path.join(BASE,name); os.makedirs(folder,exist_ok=True)
    for frame,sfn,cy in [(1,sfull,9),(2,sshort,17),(3,None,22)]:
        img,d=new_img()
        if sfn: sfn(d)
        flower_fn(d,15,cy)
        img.save(os.path.join(folder,f'FRAME{frame}.png'))
    print(f'OK  {name}')

# ══════════════════════════════════════════════════════════════════════════════
#  TALLOS PERSONALIZADOS
# ══════════════════════════════════════════════════════════════════════════════

# ── GIRASOL: tallo estándar 2px con hojas grandes ────────────────────────────
def stem_girasol_f(d):
    for y in range(16,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    leaf(d,14,22, math.pi*0.88, 9,4)   # hoja izquierda grande
    leaf(d,17,26, -math.pi*0.12, 9,4)  # hoja derecha grande
def stem_girasol_s(d):
    for y in range(24,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    leaf(d,17,27, -math.pi*0.12, 7,3)

# ── ROSA: tallo medio con ESPINAS y hojas compuestas ────────────────────────
def stem_rosa_f(d):
    for y in range(16,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    d(13,20,SE);d(12,19,SE)   # espina izquierda alta
    d(18,25,SE);d(19,24,SE)   # espina derecha baja
    leaf(d,14,23, math.pi*0.82, 6,2)   # hoja izquierda
    leaf(d,13,22, math.pi*0.72, 4,2)   # hojita extra izq
    leaf(d,17,27, -math.pi*0.18, 6,2)  # hoja derecha
    leaf(d,18,26, -math.pi*0.28, 4,2)  # hojita extra der
def stem_rosa_s(d):
    for y in range(24,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    d(18,25,SE);d(19,24,SE)
    leaf(d,17,27, -math.pi*0.18, 5,2)

# ── MARGARITA: tallo FINO y ligeramente curvo ────────────────────────────────
def stem_margarita_f(d):
    curve=[(15,16),(15,17),(15,18),(16,19),(16,20),(16,21),(15,22),
           (15,23),(15,24),(15,25),(15,26),(15,27),(15,28),(15,29),(15,30)]
    for x,y in curve: d(x,y,SG);d(x+1,y,SD)
    leaf(d,14,21, math.pi*0.9, 5,2)
    leaf(d,17,26, -math.pi*0.08, 5,2)
def stem_margarita_s(d):
    for x,y in [(15,24),(16,25),(16,26),(15,27),(15,28),(15,29),(15,30)]:
        d(x,y,SG);d(x+1,y,SD)
    leaf(d,17,27, -math.pi*0.08, 4,2)

# ── AMAPOLA: tallo MUY FINO con curva y hojas plumosas ──────────────────────
def stem_amapola_f(d):
    path=[(16,16),(16,17),(16,18),(15,19),(15,20),(15,21),(14,22),(14,23),
          (15,24),(15,25),(15,26),(15,27),(15,28),(15,29),(15,30)]
    for x,y in path: d(x,y,SG);d(x+1,y,SD)
    for x,y in [(13,27),(12,26),(11,26),(12,28),(11,28),(10,27)]: d(x,y,LD)
    for x,y in [(12,27),(11,27)]: d(x,y,LG)
    for x,y in [(18,26),(19,25),(20,25),(19,27),(20,27),(21,26)]: d(x,y,LD)
    for x,y in [(18,27),(19,26)]: d(x,y,LG)
def stem_amapola_s(d):
    for x,y in [(15,25),(15,26),(15,27),(15,28),(15,29),(15,30)]:
        d(x,y,SG);d(x+1,y,SD)
    for x,y in [(13,28),(12,28),(18,27),(19,27)]: d(x,y,LD)

# ── LIRIO: tallo estándar con hojas normales ─────────────────────────────────
def stem_lirio_f(d):
    for y in range(16,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    leaf(d,14,22, math.pi*0.88, 8,4)
    leaf(d,17,26, -math.pi*0.12, 8,4)
def stem_lirio_s(d):
    for y in range(24,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    leaf(d,17,27, -math.pi*0.12, 6,3)

# ── NARCISO: tallo estándar con hojas normales ───────────────────────────────
def stem_narciso_f(d):
    for y in range(16,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    leaf(d,14,22, math.pi*0.88, 6,3)
    leaf(d,17,26, -math.pi*0.12, 6,3)
def stem_narciso_s(d):
    for y in range(24,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    leaf(d,17,27, -math.pi*0.12, 5,2)

# ── ORQUÍDEA: tallo medio con hojas OVALADAS gruesas (coriáceas) ─────────────
def stem_orquidea_f(d):
    for y in range(16,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    leaf(d,13,23, math.pi*0.85, 9,5)   # hoja izq grande y ancha
    leaf(d,18,27, -math.pi*0.18, 8,4)  # hoja der
def stem_orquidea_s(d):
    for y in range(24,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    leaf(d,18,28, -math.pi*0.18, 6,3)

# ── CRISANTEMO: tallo medio con hojas PINNATADAS compuestas ─────────────────
def stem_crisantemo_f(d):
    for y in range(16,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    # Hojas compuestas izquierda (3 foliolos)
    for i,(y2,lng) in enumerate([(19,5),(22,4),(25,3)]):
        leaf(d,14,y2, math.pi*(0.85+i*0.04), lng, 2)
    # Hojas compuestas derecha
    for i,(y2,lng) in enumerate([(22,5),(25,4),(27,3)]):
        leaf(d,17,y2, -math.pi*(0.1+i*0.04), lng, 2)
def stem_crisantemo_s(d):
    for y in range(24,31): d(14,y,SD);d(15,y,SG);d(16,y,SG);d(17,y,SD)
    leaf(d,14,26, math.pi*0.85, 4,2)
    leaf(d,17,28, -math.pi*0.1,  4,2)

# ══════════════════════════════════════════════════════════════════════════════
#  FLORES (DISEÑOS MEJORADOS)
# ══════════════════════════════════════════════════════════════════════════════

# ── FLOR3: Girasol ────────────────────────────────────────────────────────────
def girasol(d,cx,cy):
    Y=(255,200,0,255);YH=(255,248,130,255);YD=(212,142,0,255);YE=(168,102,0,255)
    BR=(92,58,28,255);BM=(128,86,36,255);BH=(158,112,50,255);BD=(46,22,3,255)
    for i in range(8): petal(d,cx,cy, math.pi/4*i,     8,4, Y,YH,YD)
    for i in range(8): petal(d,cx,cy, math.pi/4*i+math.pi/8, 6,3, YD,Y,YE)
    circle(d,cx,cy,4,BM,BH,BD)
    for i in range(8):
        a=math.pi/4*i
        for r2 in [1.0,2.2,3.4]:
            d(int(cx+r2*math.cos(a)),int(cy+r2*math.sin(a)),BD)
    d(cx-1,cy-2,BH);d(cx-2,cy-1,BM)

save('FLOR3', girasol, stem_girasol_f, stem_girasol_s)

# ── FLOR4: Rosa ───────────────────────────────────────────────────────────────
def rosa(d,cx,cy):
    R=(195,25,30,255);RL=(238,78,83,255);RD=(118,10,14,255);RO=(62,5,7,255);RH=(255,135,140,255)
    for y in range(max(0,cy-8),min(32,cy+9)):
        for x in range(max(0,cx-8),min(32,cx+9)):
            dist=math.sqrt((x-cx)**2+(y-cy)**2)
            if dist<=7.5:
                ang=math.atan2(y-cy,x-cx)
                seg=((ang+math.pi+dist*0.45)%(2*math.pi/5))/(2*math.pi/5)
                if   dist>6.5:             c=RO
                elif dist>5.5: c=RD if seg<0.45 else R
                elif dist>4.0: c=R  if seg<0.55 else RL
                elif dist>2.0: c=RD if seg<0.35 else RL
                else:          c=RO
                d(x,y,c)
    d(cx-1,cy-2,RH);d(cx,cy-2,RH);d(cx-2,cy-1,RL)
    for i in range(5):
        a=math.pi*2/5*i-math.pi/2
        d(cx+int(7*math.cos(a)),cy+int(7*math.sin(a)),RO)

save('FLOR4', rosa, stem_rosa_f, stem_rosa_s)

# ── FLOR5: Margarita Blanca ───────────────────────────────────────────────────
def margarita_blanca(d,cx,cy):
    W=(248,248,248,255);WH=(255,255,255,255);WS=(192,192,192,255)
    YC=(255,215,0,255);YD=(198,153,0,255);YH=(255,245,112,255)
    for i in range(8): petal(d,cx,cy, math.pi/4*i, 7,4, W,WH,WS)
    circle(d,cx,cy,3,YC,YH,YD)
    for dx2,dy2 in [(-1,0),(1,0),(0,-1),(0,1)]: d(cx+dx2,cy+dy2,YD)

save('FLOR5', margarita_blanca, stem_margarita_f, stem_margarita_s)

# ── FLOR6: Amapola ────────────────────────────────────────────────────────────
def amapola(d,cx,cy):
    RO=(225,55,20,255);ROL=(255,108,44,255);ROD=(152,24,10,255);ROE=(98,8,4,255)
    BK=(10,5,2,255);YS=(250,222,52,255)
    for a in [0,math.pi/2,math.pi,3*math.pi/2]:
        petal(d,cx,cy,a,8,7,RO,ROL,ROD)
    for a in [math.pi/4,3*math.pi/4,5*math.pi/4,7*math.pi/4]:
        petal(d,cx,cy,a,6,5,ROD,RO,ROE)
    circle(d,cx,cy,3,BK,BK,BK)
    for i in range(8):
        a=math.pi/4*i
        d(int(cx+round(3.8*math.cos(a))),int(cy+round(3.8*math.sin(a))),YS)
    for a in [0,math.pi/2,math.pi,3*math.pi/2]:
        d(int(cx+round(3*math.cos(a))),int(cy+round(3*math.sin(a))),BK)

save('FLOR6', amapola, stem_amapola_f, stem_amapola_s)

# ── FLOR7: Lirio ──────────────────────────────────────────────────────────────
def lirio(d,cx,cy):
    OR=(220,122,20,255);ORL=(255,182,62,255);ORD=(148,70,10,255);ORE=(88,38,4,255)
    SPT=(78,26,3,255);WH=(255,242,202,255);GN=(68,178,48,255)
    for i in range(6): petal(d,cx,cy, math.pi/3*i, 8,4, OR,ORL,ORD)
    for i in range(6):
        a=math.pi/3*i
        for r2 in [2.2,3.8,5.4]:
            sx=int(cx+r2*math.cos(a)); sy=int(cy+r2*math.sin(a))
            d(sx,sy,SPT)
            d(sx+int(math.cos(a+math.pi/2)),sy+int(math.sin(a+math.pi/2)),SPT)
    circle(d,cx,cy,2,WH,WH,ORD)
    for i in range(6):
        a=math.pi/3*i+math.pi/6
        d(int(cx+round(3.2*math.cos(a))),int(cy+round(3.2*math.sin(a))),GN)

# ── FLOR7: Narciso ────────────────────────────────────────────────────────────
def narciso(d,cx,cy):
    Y=(255,228,0,255);YH=(255,252,142,255);YD=(198,162,0,255);YE=(152,118,0,255)
    OR=(222,102,20,255);ORL=(255,152,46,255);ORD=(152,56,10,255);ORE=(88,28,4,255)
    for i in range(6): petal(d,cx,cy, math.pi/3*i, 8,4, Y,YH,YD)
    ring(d,cx,cy,2,4,OR,ORD)
    circle(d,cx,cy,2,ORL,ORL,OR)
    d(cx,cy,ORE);d(cx+1,cy,ORE)

save('FLOR7', narciso, stem_narciso_f, stem_narciso_s)

# ── FLOR8: Orquídea ───────────────────────────────────────────────────────────
def orquidea(d,cx,cy):
    PK=(218,78,158,255);PKL=(255,150,212,255);PKD=(148,32,112,255);PKO=(86,10,70,255)
    YC=(255,230,82,255);WH=(255,255,255,255)
    # Pétalos laterales anchos (al fondo, se dibujan primero)
    petal(d,cx,cy, math.pi,   9,6, PKD,PK,PKO)
    petal(d,cx,cy, 0,         9,6, PKD,PK,PKO)
    # 3 sépalos superiores
    petal(d,cx,cy, math.pi*1.5,                6,3, PK,PKL,PKD)
    petal(d,cx,cy, math.pi*1.5-math.pi/5,      5,3, PK,PKL,PKD)
    petal(d,cx,cy, math.pi*1.5+math.pi/5,      5,3, PK,PKL,PKD)
    # Labelo (pétalo inferior distintivo de orquídea)
    for dy2 in range(0,7):
        w=max(1,5-dy2)
        for dx2 in range(-w,w+1):
            if (dx2/max(w,1))**2+((dy2-2)/4.5)**2<=1.05:
                c=PKL if abs(dx2)<w-1 else PK
                d(cx+dx2,cy+dy2,c)
    # Patrón en el labelo
    for dy2 in range(1,5): d(cx,cy+dy2,PKO);d(cx+1,cy+dy2,PKO)
    # Columna central
    circle(d,cx,cy,2,WH,YC,PKD)

save('FLOR8', orquidea, stem_orquidea_f, stem_orquidea_s)

# ── FLOR9: Crisantemo ────────────────────────────────────────────────────────
def crisantemo(d,cx,cy):
    OR=(255,130,0,255);ORL=(255,194,68,255);ORD=(192,78,0,255);ORE=(128,46,0,255)
    OC=(255,230,110,255)
    for i in range(16): petal(d,cx,cy, math.pi/8*i,  7,2, ORD,OR, ORE)
    for i in range(12): petal(d,cx,cy, math.pi/6*i+math.pi/12, 5,2, OR, ORL,ORD)
    for i in range(8):  petal(d,cx,cy, math.pi/4*i+math.pi/8,  3,2, ORL,OC, OR)
    circle(d,cx,cy,2,OC,OC,OR)

save('FLOR10', crisantemo, stem_crisantemo_f, stem_crisantemo_s)

print('\n8 flores con tallos mejorados listas!')
