import sys, os, math
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

OUT = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\CASAS\IGLESIA"
os.makedirs(OUT, exist_ok=True)
W = H = 54

# ── Paleta ────────────────────────────────────────────────────────────────────
T  = (0,0,0,0)
# Muro estuco crema
WL = (248,244,232,255); WM = (226,216,192,255); WD = (196,182,156,255)
WS = (158,146,120,255); WO = (58, 48, 32, 255)
# Piedra (fundación, molduras)
PL = (190,174,144,255); PM = (158,142,112,255); PD = (120,106, 82,255)
PS = (84, 72, 54, 255); PO = (40, 34, 24, 255)
# Techo pizarra gris-azul
RL = (142,160,175,255); RM = (100,120,140,255); RD = (66, 88,110,255)
RS = (40, 60, 82, 255); RE = (18, 32, 50, 255)
# Cruz dorada
GL = (255,228, 78,255); GM = (218,170, 26,255); GD = (152,116,  8,255)
GE = (80, 58,  4,255)
# Puerta madera oscura
DK = (20,  9,  3,255); DB = (42, 22,  8,255); DM = (76, 46, 18,255)
DL = (108,70, 28,255); DH = (148,100,44,255); DG = (195,152,68,255)
# Vidrio iglesia (azul gótico)
GS = (16,  8,  3,255); GNM= (220,213,196,255)
GGA= (135,190,228,255); GGB= (78,136,192,255); GGC= (46, 92,154,255)
GGR= (216,236,255,255)
# Campana
BL = (200,170, 80,255); BM = (158,126, 46,255); BD = (96, 74, 20,255)

# ── Utilidades ────────────────────────────────────────────────────────────────
def new_frame():
    return Image.new('RGBA',(W,H),T)

def save(img, name):
    img.save(os.path.join(OUT,name))
    print(f'OK  {name}')

def p(img,x,y,c):
    if 0<=x<W and 0<=y<H: img.putpixel((x,y),c)

def wall_px(x,y):
    ly=y%10
    if ly==0: return WD
    t=(x*13+y*7)%31
    if t<3: return WD
    if t<5: return WL
    return WM

def stone_px(x,y):
    row=y//5; loc_y=y%5
    off=(row%2)*5; loc_x=(x+off)%10
    if loc_y==0 or loc_x==0: return PO
    if loc_y==1: return PL
    if loc_y==4: return PD
    t=(x*7+y*11+row*5)%19
    if t<2: return PD
    if t<4: return PL
    return PM

def roof_px(x,y):
    row=y//4; off=(row%2)*3; lx=(x+off)%6; ly=y%4
    if lx==0: return RE
    if ly==0: return RS
    if ly==1: return RL
    if ly==2: return RM
    return RD

# ── Bloques constructivos ──────────────────────────────────────────────────────

def fill_wall(img,x0,y0,x1,y1):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if x==x0 or x==x1 or y==y0 or y==y1: p(img,x,y,WO)
            else: p(img,x,y,wall_px(x,y))

def fill_stone(img,x0,y0,x1,y1):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if x==x0 or x==x1 or y==y0 or y==y1: p(img,x,y,PO)
            else: p(img,x,y,stone_px(x-x0,y-y0))

def cornice(img,y,x0=0,x1=W-1):
    """Cornisa horizontal con dentículos."""
    for x in range(x0,x1+1):
        p(img,x,y,WO); p(img,x,y+1,WL); p(img,x,y+2,WD)
    for x in range(x0+3,x1-2,6):
        p(img,x,y-1,WD); p(img,x+1,y-1,WD)
        p(img,x,y-2,WM); p(img,x+1,y-2,WM)

def pilaster(img,x,y0,y1):
    """Pilastra de 3px."""
    for y in range(y0,y1+1):
        p(img,x,y,WO); p(img,x+1,y,WL); p(img,x+2,y,WD)
    for dx in range(-1,4): p(img,x+dx,y0,WO); p(img,x+dx,y0+1,WL)
    for dx in range(-1,4): p(img,x+dx,y1,WO); p(img,x+dx,y1-1,WL)

def glass_color(tx,ty):
    t=tx*0.4+ty*0.6
    if t<0.1: return GGR
    if t<0.4: return GGA
    if t<0.7: return GGB
    return GGC

def arch_window(img,x0,y0,x1,y1):
    """Ventana lanceta con arco y vidrio azul."""
    r=(x1-x0)//2; cx=(x0+x1)//2; acy=y0+r
    # --- moldura exterior ---
    for y in range(acy,y1+2):
        p(img,x0-1,y,GNM); p(img,x0-2,y,WO)
        p(img,x1+1,y,GNM); p(img,x1+2,y,WO)
    for x in range(x0-2,x1+3):
        p(img,x,y1+1,GNM); p(img,x,y1+2,WO)
    for dy in range(-r-3,1):
        for dx in range(-r-3,r+4):
            dist=math.sqrt(dx*dx+dy*dy)
            px2,py2=cx+dx,acy+dy
            if not(0<=px2<W and 0<=py2<H) or dy>0: continue
            if r+0.5<dist<=r+2: p(img,px2,py2,GNM)
            elif r+2<dist<=r+3: p(img,px2,py2,WO)
    # --- arco vidrio ---
    for dy in range(-r,1):
        for dx in range(-r,r+1):
            dist=math.sqrt(dx*dx+dy*dy)
            px2,py2=cx+dx,acy+dy
            if not(0<=px2<W and 0<=py2<H) or dy>0 or py2>=acy: continue
            if dist<=r-0.5:
                p(img,px2,py2,glass_color((dx/max(r,1)+1)/2,(dy/max(r,1)+1)/2))
            elif dist<=r+0.5:
                p(img,px2,py2,GS)
    # --- cuerpo rectangular ---
    for y in range(acy,y1+1):
        for x in range(x0,x1+1):
            if x==x0 or x==x1 or y==y1: p(img,x,y,GS)
            else:
                tx=(x-x0-1)/max(x1-x0-2,1); ty=(y-acy)/max(y1-acy,1)
                p(img,x,y,glass_color(tx,ty))
    # --- travesaño central (x) y montante (y) ---
    for y in range(acy,y1): p(img,cx,y,GS)
    mid_y=(acy+y1)//2
    for x in range(x0,x1+1): p(img,x,mid_y,GS)

def rose_window(img,cx,cy,r):
    """Rosetón circular con 8 divisiones."""
    for dy in range(-r-3,r+4):
        for dx in range(-r-3,r+4):
            dist=math.sqrt(dx*dx+dy*dy)
            px2,py2=cx+dx,cy+dy
            if not(0<=px2<W and 0<=py2<H) or dist>r+3: continue
            if dist>r+2: c=WO
            elif dist>r+1: c=GNM
            elif dist>r-0.5: c=GS
            elif dist<2: c=GS
            else:
                ang=math.atan2(dy,dx)
                sec=int((ang+math.pi)/(math.pi/4))%8
                on_spoke=(((ang+math.pi)%(math.pi/4))<0.2)
                t=dist/r
                if on_spoke: c=GS
                elif sec%2==0: c=GGR if t<0.4 else GGA if t<0.75 else GGB
                else: c=GGA if t<0.4 else GGB if t<0.75 else GGC
            p(img,px2,py2,c)

def church_door(img,x0,y0,x1,y1):
    """Puerta doble con arco, paneles y escalones."""
    r=(x1-x0)//2; cx=(x0+x1)//2; acy=y0+r
    # moldura exterior piedra
    for y in range(acy,y1+1):
        p(img,x0-2,y,PM); p(img,x0-3,y,PO)
        p(img,x1+2,y,PM); p(img,x1+3,y,PO)
    for x in range(x0-3,x1+4):
        p(img,x,y1+1,PM); p(img,x,y1+2,PO)
    for dy in range(-r-5,1):
        for dx in range(-r-5,r+6):
            dist=math.sqrt(dx*dx+dy*dy)
            px2,py2=cx+dx,acy+dy
            if not(0<=px2<W and 0<=py2<H) or dy>0: continue
            if r+2<dist<=r+5: p(img,px2,py2,PM)
            elif r+5<dist<=r+6: p(img,px2,py2,PO)
    # vidrio arco
    for dy in range(-r,1):
        for dx in range(-r,r+1):
            dist=math.sqrt(dx*dx+dy*dy)
            px2,py2=cx+dx,acy+dy
            if not(0<=px2<W and 0<=py2<H) or dy>0 or py2>=acy: continue
            if dist<=r-0.5:
                ang=math.atan2(dy,dx)
                c=GGR if (ang+math.pi)<0.5 else GGA if (ang+math.pi)<1.5 else GGB
                p(img,px2,py2,c)
            elif dist<=r+0.5: p(img,px2,py2,DK)
    # cuerpo puerta
    for y in range(acy,y1+1):
        for x in range(x0,x1+1):
            if x==x0 or x==x1 or y==y1: c=DK
            elif x==cx: c=DK
            else:
                mid=cx; ly2=y-acy; ph=7; pr=ly2//ph; pl=ly2%ph
                if x<mid:
                    lx2=x-x0-1; ww=mid-x0-2
                    if lx2==0 or lx2==ww: c=DK
                    elif pl==0: c=DB
                    elif pl==1 or lx2==1 or lx2==ww-1: c=DH
                    else: c=DL if pr%2==0 else DM
                else:
                    lx2=x1-x-1; ww=x1-mid-2
                    if lx2==0 or lx2==ww: c=DK
                    elif pl==0: c=DB
                    elif pl==1 or lx2==1 or lx2==ww-1: c=DH
                    else: c=DL if pr%2==0 else DM
            p(img,x,y,c)
    # manijas
    hy=(acy+y1)//2
    p(img,cx-3,hy,DG); p(img,cx-3,hy+1,DG)
    p(img,cx+4,hy,DG); p(img,cx+4,hy+1,DG)
    # escalones
    for step in range(3):
        sx0=max(0,x0-step*2-2); sx1=min(W-1,x1+step*2+2); sy=y1+step+1
        if sy<H:
            for sx in range(sx0,sx1+1):
                c=PO if sx==sx0 or sx==sx1 else PL if step==0 else PM
                p(img,sx,sy,c)

def campanario(img,x0,y0,x1,y1):
    """Torre con arco de campana y pilastras."""
    fill_wall(img,x0,y0,x1,y1)
    # pilastras laterales
    for y in range(y0+1,y1):
        p(img,x0+1,y,WL); p(img,x0+2,y,WD)
        p(img,x1-1,y,WL); p(img,x1-2,y,WD)
    # arco de campana interior
    aw=(x1-x0)-6; acx=(x0+x1)//2; ar=aw//2; acy=y0+ar+3
    for dy in range(-ar,ar+1):
        for dx in range(-ar,ar+1):
            dist=math.sqrt(dx*dx+dy*dy)
            px2,py2=acx+dx,acy+dy
            if not(0<=px2<W and 0<=py2<H): continue
            interior=(acx-ar+1<=px2<=acx+ar-1)
            if dy>0 and interior: p(img,px2,py2,(14,7,2,255))
            elif dy<=0:
                if dist<=ar-0.5: p(img,px2,py2,(14,7,2,255))
                elif dist<=ar+0.5: p(img,px2,py2,WO)
    # campana colgante
    bcx=acx; bcy=acy+ar//2+1
    for dy in range(-2,5):
        bw=max(1,min(4,3-abs(dy-1)))
        for dx in range(-bw,bw+1):
            c=BM if (abs(dx)==bw or dy==-2) else BD if dy==4 else BL
            p(img,bcx+dx,bcy+dy,c)
    p(img,bcx,bcy+4,BD)
    # moldura superior del campanario
    for x in range(x0-1,x1+2):
        p(img,x,y0-1,WO); p(img,x,y0-2,WL)

def cruz(img,cx,cy_top,h=8):
    """Cruz dorada en el pináculo."""
    for y in range(cy_top,cy_top+h):
        p(img,cx-1,y,GM); p(img,cx,y,GL); p(img,cx+1,y,GD)
    arm_y=cy_top+h//3
    for dx in range(-4,5):
        c=GD if abs(dx)==4 else GL if dx==-3 else GM
        p(img,cx+dx,arm_y,c); p(img,cx+dx,arm_y+1,GD)
    # base orbe
    for dx in range(-1,2): p(img,cx+dx,cy_top+h,GE)

# ══════════════════════════════════════════════════════════════════════════════
#  FRAME 1 – FRENTE (fachada principal)
# ══════════════════════════════════════════════════════════════════════════════
f1=new_frame()

# Fundación de piedra
fill_stone(f1,0,46,W-1,H-1)

# Muro principal
fill_wall(f1,0,21,W-1,45)

# Cornisa entre campanario y muro
cornice(f1,20,0,W-1)

# Campanario (x=18..35, y=4..22)
campanario(f1,18,4,35,22)

# Pilastras decorativas en el muro principal
pilaster(f1, 1,21,45)
pilaster(f1,49,21,45)
pilaster(f1,10,21,45)
pilaster(f1,40,21,45)

# Cruz en la cima del campanario
cruz(f1,26,0,4)

# Ventanas laterales con arco
arch_window(f1, 4,25,14,42)
arch_window(f1,39,25,49,42)

# Rosetón central
rose_window(f1,26,29,6)

# Puerta principal con arco
church_door(f1,17,34,36,45)

save(f1,'FRAME1.png')

# ══════════════════════════════════════════════════════════════════════════════
#  FRAME 2 – ATRÁS
# ══════════════════════════════════════════════════════════════════════════════
f2=new_frame()

fill_stone(f2,0,46,W-1,H-1)
fill_wall(f2,0,0,W-1,45)
cornice(f2,2,0,W-1)

# Pilastras
pilaster(f2, 1,3,45)
pilaster(f2,49,3,45)

# 2 ventanas altas centradas
arch_window(f2, 9,18,19,40)
arch_window(f2,34,18,44,40)

# Puerta trasera (más sencilla, sin escalones ni arco)
for y in range(34,46):
    for x in range(20,34):
        if x==20 or x==33 or y==34 or y==45: c=DK
        elif x==21 or x==32: c=DM
        else:
            ly2=y-35; ph=5; pl=ly2%ph; pr=ly2//ph
            c=DB if pl==0 else DH if pl==1 else DL if pr%2==0 else DM
        p(f2,x,y,c)
# manija
p(f2,26,40,DG); p(f2,27,40,DG)

save(f2,'FRAME2.png')

# ══════════════════════════════════════════════════════════════════════════════
#  FRAME 3 – LADO IZQUIERDO
# ══════════════════════════════════════════════════════════════════════════════
f3=new_frame()

fill_stone(f3,0,46,W-1,H-1)
fill_wall(f3,0,0,W-1,45)
cornice(f3,2,0,W-1)

# 3 ventanas altas uniformemente espaciadas (cada ~16px)
arch_window(f3, 4,18,14,42)
arch_window(f3,21,18,31,42)
arch_window(f3,38,18,48,42)

# Contrafuerte (buttress) entre ventanas — rasgo típico de iglesia
for y in range(4,46):
    for dx,base in [(17,17),(18,18),(32,33),(33,34)]:
        if dx in (17,32):
            p(f3,dx,y,PO if y%8==0 else PD)
        else:
            p(f3,dx,y,PO if y%8==0 else PM)

save(f3,'FRAME3.png')

# ══════════════════════════════════════════════════════════════════════════════
#  FRAME 4 – LADO DERECHO
# ══════════════════════════════════════════════════════════════════════════════
f4=new_frame()

fill_stone(f4,0,46,W-1,H-1)
fill_wall(f4,0,0,W-1,45)
cornice(f4,2,0,W-1)

# Mismas ventanas que lado izquierdo
arch_window(f4, 4,18,14,42)
arch_window(f4,21,18,31,42)
arch_window(f4,38,18,48,42)

# Contrafuertes (espejados)
for y in range(4,46):
    for dx in [17,18,32,33]:
        c=PO if y%8==0 else (PD if dx in(17,32) else PM)
        p(f4,dx,y,c)

save(f4,'FRAME4.png')

# ══════════════════════════════════════════════════════════════════════════════
#  FRAME 5 – TECHO
# ══════════════════════════════════════════════════════════════════════════════
f5=new_frame()

# Textura de techo (pizarra)
for y in range(H):
    for x in range(W):
        p(f5,x,y,roof_px(x,y))

# Borde/canalón perimetral
for x in range(W):
    p(f5,x,0,RE); p(f5,x,1,RS); p(f5,x,H-1,RE); p(f5,x,H-2,RS)
for y in range(H):
    p(f5,0,y,RE); p(f5,1,y,RS); p(f5,W-1,y,RE); p(f5,W-2,y,RS)

# Cumbrera central (ridge horizontal + vertical = forma de cruz del techo)
for x in range(2,W-2): p(f5,x,H//2,RE); p(f5,x,H//2+1,RS)
for y in range(2,H-2): p(f5,W//2,y,RE); p(f5,W//2+1,y,RS)

# Cruz dorada en el centro del techo
cruz(f5,W//2,H//2-4,8)

save(f5,'FRAME5.png')

# ══════════════════════════════════════════════════════════════════════════════
#  FRAME 6 – PARED LATERAL CIEGA (sin ventanas)
# ══════════════════════════════════════════════════════════════════════════════
f6=new_frame()

fill_stone(f6,0,46,W-1,H-1)
fill_wall(f6,0,0,W-1,45)
cornice(f6,2,0,W-1)

# Pilastras en los extremos
pilaster(f6, 1,3,45)
pilaster(f6,49,3,45)

# Contrafuertes decorativos (sin ventanas entre ellos)
for y in range(4,46):
    for dx in [17,18,32,33]:
        c=PO if y%8==0 else (PD if dx in(17,32) else PM)
        p(f6,dx,y,c)

# Pequeña moldura en la parte alta del muro (friso simple)
for x in range(0,W):
    p(f6,x,4,WO)
    p(f6,x,5,WL)

save(f6,'FRAME6.png')

print('\nIglesia 54x54 completada — 6 frames listos!')
