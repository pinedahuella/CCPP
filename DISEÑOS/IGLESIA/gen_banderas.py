"""
gen_banderas.py  -  Banderas y cortinas de iglesia  32x64 px
Guarda en IGLESIA/ y copia a PNGS/

Banderas (con palo de madera + barra + tela + flecos dorados):
  01 bandera_ihs            - IHS con cruz, tela crema
  02 bandera_sagrado_corazon- Sagrado Corazon, tela blanca
  03 bandera_papal          - Bandera papal bicolor (oro/blanco)
  04 bandera_cuaresma       - Corona de espinas, tela morada
  05 bandera_resurreccion   - Cruz radiante, tela blanca

Cortinas (varilla dorada + tela con pliegues + flecos):
  06 cortina_roja           - Terciopelo rojo, flecos dorados
  07 cortina_morada         - Morada cuaresmal
  08 cortina_blanca         - Blanca de Pascua
  09 cortina_verde          - Verde tiempo ordinario
  10 cortina_negra          - Negra de difuntos, flecos plateados
"""
import sys, math
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
import os, shutil, pathlib

_base    = pathlib.Path(__file__).parent
OUT_DIR  = str(_base)
PNGS_DIR = str(_base.parent / 'PNGS')
os.makedirs(PNGS_DIR, exist_ok=True)

W, H = 32, 64
T    = (0, 0, 0, 0)

# ── Paleta ────────────────────────────────────────────────────────────────────
WDK=(28,12,4,255);   WDD=(55,26,8,255);   WDM=(85,45,16,255);  WDL=(118,68,28,255)
GDK=(110,75,8,255);  GDD=(155,110,15,255); GDM=(205,158,32,255)
GDL=(238,195,58,255);GDH=(255,225,100,255);GDW=(255,248,185,255)
CRM=(245,240,225,255);CRD=(210,202,182,255);CRL=(255,252,242,255)
RDK=(60,5,5,255);    RDM=(145,15,15,255); RDL=(198,32,32,255); RDH=(232,62,62,255)
PUK=(30,6,45,255);   PUM=(68,14,92,255);  PUL=(102,25,142,255);PUH=(142,45,192,255)
GRK=(10,45,10,255);  GRM=(22,88,25,255);  GRL=(42,138,46,255); GRH=(70,180,76,255)
YLK=(150,120,6,255); YLM=(205,168,18,255);YLL=(248,215,50,255);YLH=(255,242,140,255)
WHT=(248,246,238,255);WHS=(215,212,202,255);WHD=(185,182,172,255)
NEK=(16,14,18,255);  NEM=(38,36,42,255);  NEL=(72,70,80,255);  NEH=(112,110,122,255)

# ── Canvas helper ─────────────────────────────────────────────────────────────
def mk_img():
    img = Image.new('RGBA', (W, H), T)
    p   = img.load()
    def px(x, y, c):
        if 0 <= x < W and 0 <= y < H: p[x, y] = c
    def hl(y, x1, x2, c):
        for x in range(x1, x2+1): px(x, y, c)
    def vl(x, y1, y2, c):
        for y in range(y1, y2+1): px(x, y, c)
    def rc(x1, y1, x2, y2, c):
        for yy in range(y1, y2+1):
            for xx in range(x1, x2+1): px(xx, yy, c)
    return img, px, hl, vl, rc

# ── Layout bandera ────────────────────────────────────────────────────────────
# x=0..2  palo de madera
# y=2..5  barra horizontal dorada
# x=3..31, y=6..54  tela (fabric)
# y=55..63  flecos dorados
FX0, FY0, FX1, FY1 = 3, 6, 31, 54
GY0, GY1 = 55, 63

def draw_pole(px):
    for y in range(H):
        px(0, y, WDK); px(1, y, WDD); px(2, y, WDM)
    px(1, 0, WDL); px(2, 1, WDL)   # punta
    for x in range(FX0, W):
        px(x, 2, GDD); px(x, 3, GDL); px(x, 4, GDM); px(x, 5, GDK)
    for y in range(2, 6): px(FX1, y, GDH)  # extremo barra

def draw_border(px, c=GDM):
    for y in range(FY0, FY1+1): px(FX0, y, c); px(FX1, y, c)
    for x in range(FX0, FX1+1): px(x, FY0, c); px(x, FY1, c)

def draw_fringe(px, c1=GDM, c2=GDL, c3=GDH):
    for x in range(FX0, W):
        ph = (x - FX0) % 4
        if ph == 0:
            for y in range(GY0, GY1+1): px(x, y, c1)
        elif ph == 1:
            for y in range(GY0, GY0+6): px(x, y, c3)
        elif ph == 2:
            for y in range(GY0, GY1):   px(x, y, c2)
        # ph==3: transparente

def fill_fabric(px, col, dark=None, light=None, folds=3.5):
    if dark  is None: dark  = col
    if light is None: light = col
    for y in range(FY0+1, FY1):
        for x in range(FX0+1, FX1):
            t = (x - FX0 - 1) / (FX1 - FX0 - 2)
            f = math.sin(t * math.pi * folds)
            if   f >  0.38: px(x, y, light)
            elif f < -0.38: px(x, y, dark)
            else:            px(x, y, col)

# ── Pixel letters (para simbolos IHS, INRI) ───────────────────────────────────
def draw_I(px, x0, y0, c, ch, w=4, h=12):
    for y in range(y0, y0+h):
        px(x0, y, c); px(x0+w-1, y, c)
        for xi in range(x0+1, x0+w-1): px(xi, y, ch)
    for x in range(x0-1, x0+w+1):
        px(x, y0, c); px(x, y0+h-1, c)

def draw_H(px, x0, y0, c, ch, w=6, h=12):
    for y in range(y0, y0+h):
        px(x0, y, c); px(x0+1, y, ch)
        px(x0+w-2, y, c); px(x0+w-1, y, ch)
    mid = y0 + h//2 - 1
    for x in range(x0, x0+w): px(x, mid, c); px(x, mid+1, ch)

def draw_S(px, x0, y0, c, ch, w=5, h=12):
    mid = y0 + h//2
    for x in range(x0+1, x0+w):   px(x, y0, c)         # arco top
    for y in range(y0+1, y0+4):   px(x0, y, ch)          # left top
    px(x0+w-1, y0+1, c)
    for x in range(x0, x0+w):     px(x, mid-1, c); px(x, mid, ch)  # medio
    for y in range(mid+1, mid+4):  px(x0+w-1, y, ch)    # right bot
    px(x0, mid+1, c)
    for x in range(x0, x0+w-1):   px(x, y0+h-1, c)      # arco bot
    px(x0+w-1, y0+h-2, c)

# =============================================================================
# 01  BANDERA IHS
# =============================================================================
def mk_bandera_ihs():
    img, px, hl, vl, rc = mk_img()
    fill_fabric(px, CRM, CRD, CRL)
    draw_border(px, GDM)
    draw_pole(px)

    # Cruz sobre la I (x=10..14, y=9..17)
    for y in range(9, 19): px(11, y, GDM); px(12, y, GDH)
    for x in range(8, 17): px(x, 12, GDM); px(x, 13, GDH)
    px(11, 12, GDW); px(12, 12, GDW)

    # Letras IHS (y=19..30, altura=12)
    draw_I(px, 5,  19, GDM, GDH, w=4, h=12)
    draw_H(px, 11, 19, GDM, GDH, w=7, h=12)
    draw_S(px, 20, 19, GDM, GDH, w=5, h=12)

    # Cruz ornamental inferior
    for y in range(34, 42): px(17, y, GDM); px(18, y, GDH)
    for x in range(13, 23): px(x, 37, GDM); px(x, 38, GDH)
    px(17, 37, GDW); px(18, 37, GDW)

    # Puntitos decorativos
    for xi in (9, 17, 25):
        px(xi, 44, GDD); px(xi, 46, GDD)

    draw_fringe(px)
    return img


# =============================================================================
# 02  BANDERA SAGRADO CORAZON
# =============================================================================
def mk_bandera_sagrado_corazon():
    img, px, hl, vl, rc = mk_img()
    fill_fabric(px, WHT, WHS, CRL)
    draw_border(px, GDM)
    draw_pole(px)

    cx, cy = 17, 31

    # Rayos radiales dorados
    for i in range(12):
        ang = math.radians(i * 30)
        col = GDL if i % 2 == 0 else GDM
        for r in range(12, 21):
            rx = int(cx + r * math.cos(ang))
            ry = int(cy + r * math.sin(ang))
            if FY0 < ry < FY1 and FX0 < rx < FX1:
                px(rx, ry, col)

    # Corazon (curva algebraica: (x²+y²-1)³ = x²y³)
    for y in range(cy-10, cy+8):
        for x in range(cx-10, cx+10):
            nx = (x - cx) / 7.0
            ny = -(y - cy) / 7.0
            val = (nx**2 + ny**2 - 1)**3 - nx**2 * ny**3
            if val <= 0:
                edge = abs(val) < 0.08
                if edge:               c = RDK
                elif nx < -0.3 and ny > 0.1: c = RDH
                else:                  c = RDL
                px(x, y, c)

    # Highlight
    px(cx-2, cy-6, RDH); px(cx-1, cy-6, RDH); px(cx-3, cy-5, RDH)

    # Corona de espinas
    for ang in range(0, 360, 18):
        rad = math.radians(ang)
        bx = int(cx + 10 * math.cos(rad)); by = int(cy - 1 + 10 * math.sin(rad))
        if FY0 < by < FY1 and FX0 < bx < FX1: px(bx, by, WDM)
        spx = int(cx + 12 * math.cos(rad)); spy = int(cy - 1 + 12 * math.sin(rad))
        if FY0 < spy < FY1 and FX0 < spx < FX1: px(spx, spy, WDL)

    # Cruz dorada encima del corazon
    for y in range(cy-17, cy-9):
        px(cx, y, GDM); px(cx+1, y, GDH)
    for x in range(cx-3, cx+5):
        px(x, cy-14, GDM); px(x, cy-13, GDH)
    px(cx, cy-14, GDW); px(cx+1, cy-13, GDW)

    # Llamas en la base del corazon
    for fx, fh in [(cx-3, 5), (cx, 7), (cx+3, 5)]:
        for y in range(cy+5, cy+5+fh):
            t = (y - cy - 5) / fh
            if   t < 0.3: px(fx, y, GDH)
            elif t < 0.65: px(fx, y, GDL)
            else:          px(fx, y, GDM)

    draw_fringe(px)
    return img


# =============================================================================
# 03  BANDERA PAPAL
# =============================================================================
def mk_bandera_papal():
    img, px, hl, vl, rc = mk_img()

    # Mitad izquierda: oro
    for y in range(FY0+1, FY1):
        for x in range(FX0+1, 17):
            t = (x - FX0 - 1) / 12.0
            f = math.sin(t * math.pi * 3.5)
            if   f >  0.38: px(x, y, YLH)
            elif f < -0.38: px(x, y, YLK)
            else:            px(x, y, YLL)
    # Mitad derecha: blanco
    for y in range(FY0+1, FY1):
        for x in range(17, FX1):
            t = (x - 17) / 13.0
            f = math.sin(t * math.pi * 3.5)
            if   f >  0.38: px(x, y, CRL)
            elif f < -0.38: px(x, y, WHD)
            else:            px(x, y, WHT)

    draw_border(px, GDM)
    # Linea central de separacion
    for y in range(FY0, FY1+1): px(16, y, GDM); px(17, y, GDM)
    draw_pole(px)

    kcx = 17   # centro horizontal

    # ── Tiara papal (triple corona) ───────────────────────────────────────────
    # Base
    rc(10, 14, 23, 16, GDM)
    for x in range(10, 24): px(x, 14, GDL)
    # Corona 1 (inferior)
    rc(11, 11, 22, 14, GDM)
    for x in range(11, 23): px(x, 11, GDL)
    # Corona 2 (media)
    rc(12, 8, 21, 11, GDM)
    for x in range(12, 22): px(x, 8, GDL)
    # Corona 3 (superior)
    rc(13, 6, 20, 8, GDH)
    for x in range(13, 21): px(x, 6, GDW)
    # Cruz en la cuspide
    for y in range(9, 12): px(16, y, GDM); px(17, y, GDH)
    for x in range(14, 20): px(x, 10, GDM)
    px(16, 10, GDW); px(17, 10, GDW)
    # Cintas laterales
    for y in range(16, 20): px(10, y, GDD); px(23, y, GDD)
    px(9, 17, GDD); px(24, 17, GDD)

    # ── Llaves cruzadas (simplificadas) ───────────────────────────────────────
    # Llave 1 (dorada, ang -40 grados)
    a1 = math.radians(-40)
    for r in range(-9, 10):
        kx = int(kcx + r * math.cos(a1)); ky = int(33 + r * math.sin(a1))
        if FY0 < ky < FY1 and FX0 < kx < FX1:
            px(kx, ky, GDM)
            px(kx + int(math.sin(a1)), ky - int(math.cos(a1)), GDL)
    # Anillo llave 1
    for a in range(0, 360, 25):
        rad = math.radians(a)
        ax = int(kcx - 4 + 3 * math.cos(rad)); ay = int(24 + 3 * math.sin(rad))
        if FY0 < ay < FY1 and FX0 < ax < FX1: px(ax, ay, GDM)

    # Llave 2 (plateada/gris, ang +40 grados)
    a2 = math.radians(40)
    SVR = (185, 185, 195, 255); SVL = (225, 225, 235, 255)
    for r in range(-9, 10):
        kx = int(kcx + r * math.cos(a2)); ky = int(33 + r * math.sin(a2))
        if FY0 < ky < FY1 and FX0 < kx < FX1:
            px(kx, ky, SVR)
            px(kx - int(math.sin(a2)), ky + int(math.cos(a2)), SVL)
    # Anillo llave 2
    for a in range(0, 360, 25):
        rad = math.radians(a)
        ax = int(kcx + 4 + 3 * math.cos(rad)); ay = int(24 + 3 * math.sin(rad))
        if FY0 < ay < FY1 and FX0 < ax < FX1: px(ax, ay, SVR)

    # Escudo (ovalo detras de las llaves)
    for dy in range(-6, 7):
        for dx in range(-7, 8):
            d = (dx/7.0)**2 + (dy/5.5)**2
            if 0.9 <= d <= 1.2:
                px(kcx + dx, 33 + dy, GDM)

    draw_fringe(px, GDM, YLL, GDH)
    return img


# =============================================================================
# 04  BANDERA CUARESMA
# =============================================================================
def mk_bandera_cuaresma():
    img, px, hl, vl, rc = mk_img()
    fill_fabric(px, PUL, PUK, PUH)
    draw_border(px, GDM)
    draw_pole(px)

    cx, cy = 17, 30

    # Cruz central dorada
    for y in range(FY0+2, FY1-1):
        px(cx-1, y, GDK); px(cx, y, GDM); px(cx+1, y, GDH); px(cx+2, y, GDM)
    for x in range(FX0+2, FX1-1):
        px(x, cy-1, GDK); px(x, cy, GDM); px(x, cy+1, GDH); px(x, cy+2, GDM)
    # Centro
    px(cx, cy, GDW); px(cx+1, cy, GDW)

    # Corona de espinas
    for ang in range(0, 360, 14):
        rad = math.radians(ang)
        for r in range(8, 12):
            bx = int(cx + r * math.cos(rad)); by = int(cy + r * math.sin(rad))
            if FY0 < by < FY1 and FX0 < bx < FX1: px(bx, by, WDM)
        spx = int(cx + 13 * math.cos(rad)); spy = int(cy + 13 * math.sin(rad))
        if FY0 < spy < FY1 and FX0 < spx < FX1: px(spx, spy, WDL)

    # INRI encima de la cruz (letras pequeñas crema)
    # I
    for y in range(11, 16): px(9, y, CRM); px(10, y, CRL)
    # N
    for y in range(11, 16): px(12, y, CRM); px(15, y, CRM)
    px(12,11,CRM); px(13,12,CRM); px(13,13,CRM); px(14,14,CRM); px(14,15,CRM)
    # R
    for y in range(11, 16): px(17, y, CRM)
    px(18,11,CRM); px(19,11,CRM); px(19,12,CRM); px(18,13,CRM); px(19,14,CRM); px(19,15,CRM)
    # I
    for y in range(11, 16): px(21, y, CRM); px(22, y, CRL)

    draw_fringe(px, PUM, PUL, PUH)
    return img


# =============================================================================
# 05  BANDERA RESURRECCION
# =============================================================================
def mk_bandera_resurreccion():
    img, px, hl, vl, rc = mk_img()
    fill_fabric(px, WHT, WHS, CRL)
    draw_border(px, GDM)
    draw_pole(px)

    cx, cy = 17, 30

    # Rayos de luz (16 rayos alternados)
    for i in range(16):
        ang = math.radians(i * 22.5)
        col = GDL if i % 2 == 0 else GDM
        for r in range(11, 23):
            rx = int(cx + r * math.cos(ang)); ry = int(cy + r * math.sin(ang))
            if FY0 < ry < FY1 and FX0 < rx < FX1: px(rx, ry, col)

    # Glow central
    for dy in range(-7, 8):
        for dx in range(-7, 8):
            d = math.sqrt(dx**2 + dy**2)
            if   d < 3: px(cx+dx, cy+dy, GDW)
            elif d < 5: px(cx+dx, cy+dy, GDH)
            elif d < 7: px(cx+dx, cy+dy, GDL)

    # Cruz grande con borde dorado
    for y in range(cy-18, cy+18):
        px(cx-2, y, GDM); px(cx-1, y, GDH); px(cx, y, GDW)
        px(cx+1, y, GDH); px(cx+2, y, GDM)
    for x in range(cx-14, cx+14):
        px(x, cy-2, GDM); px(x, cy-1, GDH); px(x, cy, GDW)
        px(x, cy+1, GDH); px(x, cy+2, GDM)

    # Terminales ornamentales (remates de los brazos)
    for d in range(3):
        px(cx+14-d, cy-1+d, GDH)  # der
        px(cx-14+d, cy-1+d, GDH)  # izq
    for d in range(3):
        px(cx-1+d, cy-18+d, GDH)  # sup

    # Aleluya decorativo (puntitos)
    for xi in range(8, 28, 3):
        px(xi, cy+20, GDM); px(xi, cy+21, GDL)

    draw_fringe(px)
    return img


# ── CORTINAS ──────────────────────────────────────────────────────────────────
# Layout:
#   y=0..3  : varilla dorada
#   y=4..55 : tela con pliegues
#   y=56..63: flecos

def cortina_rod(px):
    for x in range(W):
        px(x, 0, GDK); px(x, 1, GDM); px(x, 2, GDL); px(x, 3, GDD)
    # Anillos de la varilla cada 5px
    for x in range(2, W, 5):
        for y in range(0, 4): px(x, y, GDH)

def cortina_fringe(px, c1=GDM, c2=GDL, c3=GDH):
    for x in range(W):
        ph = x % 4
        if ph == 0:
            for y in range(56, 64): px(x, y, c1)
        elif ph == 1:
            for y in range(56, 62): px(x, y, c3)
        elif ph == 2:
            for y in range(56, 64): px(x, y, c2)
        # ph==3: transparente

def cortina_fabric(px, col, dark, light, num_folds=4):
    """Tela con pliegues verticales y ligero oscurecimiento vertical."""
    for y in range(4, 56):
        vt  = (y - 4) / 51.0
        shd = int(vt * 18)
        for x in range(W):
            t = x / (W - 1)
            f = math.sin(t * math.pi * num_folds * 2)
            if   f >  0.38: base = light
            elif f < -0.38: base = dark
            else:            base = col
            r, g, b, a = base
            px(x, y, (max(0, r-shd), max(0, g-shd), max(0, b-shd), a))
    # Lineas de pliegue (bordes oscuros)
    for fi in range(1, num_folds * 2):
        fx = int(W * fi / (num_folds * 2))
        for y in range(4, 56):
            px(fx, y, dark)

def cortina_trim(px, c=GDM):
    """Cenefa dorada arriba y abajo de la tela."""
    for x in range(W): px(x, 4, c); px(x, 5, GDL); px(x, 54, c); px(x, 55, GDL)


def mk_cortina_roja():
    img, px, hl, vl, rc = mk_img()
    cortina_rod(px)
    cortina_fabric(px, RDL, RDK, RDH)
    cortina_trim(px)
    cortina_fringe(px)
    return img

def mk_cortina_morada():
    img, px, hl, vl, rc = mk_img()
    cortina_rod(px)
    cortina_fabric(px, PUL, PUK, PUH)
    cortina_trim(px)
    cortina_fringe(px, GDM, GDL, GDH)
    return img

def mk_cortina_blanca():
    img, px, hl, vl, rc = mk_img()
    cortina_rod(px)
    cortina_fabric(px, WHT, WHS, CRL)
    cortina_trim(px)
    cortina_fringe(px)
    return img

def mk_cortina_verde():
    img, px, hl, vl, rc = mk_img()
    cortina_rod(px)
    cortina_fabric(px, GRL, GRK, GRH)
    cortina_trim(px)
    cortina_fringe(px)
    return img

def mk_cortina_negra():
    img, px, hl, vl, rc = mk_img()
    cortina_rod(px)
    cortina_fabric(px, NEM, NEK, NEL)
    # Cenefa gris en lugar de dorada
    for x in range(W): px(x, 4, NEL); px(x, 5, NEH); px(x, 54, NEL); px(x, 55, NEH)
    SVR = (180, 178, 188, 255); SVL = (222, 220, 230, 255); SVH = (205, 203, 215, 255)
    cortina_fringe(px, SVR, SVL, SVH)
    return img


# ── Generar todos ─────────────────────────────────────────────────────────────
ITEMS = [
    ('bandera_ihs',             mk_bandera_ihs            ),
    ('bandera_sagrado_corazon', mk_bandera_sagrado_corazon),
    ('bandera_papal',           mk_bandera_papal          ),
    ('bandera_cuaresma',        mk_bandera_cuaresma       ),
    ('bandera_resurreccion',    mk_bandera_resurreccion   ),
    ('cortina_roja',            mk_cortina_roja           ),
    ('cortina_morada',          mk_cortina_morada         ),
    ('cortina_blanca',          mk_cortina_blanca         ),
    ('cortina_verde',           mk_cortina_verde          ),
    ('cortina_negra',           mk_cortina_negra          ),
]

for nombre, fn in ITEMS:
    img   = fn()
    local = os.path.join(OUT_DIR,  f'{nombre}.png')
    copia = os.path.join(PNGS_DIR, f'{nombre}.png')
    img.save(local)
    shutil.copy2(local, copia)
    print(f'OK  {nombre}.png')

print(f'\n{len(ITEMS)} items 32x64 -> IGLESIA/ y PNGS/')
