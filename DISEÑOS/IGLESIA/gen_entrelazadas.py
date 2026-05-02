"""
gen_entrelazadas.py  -  Cortinas entrelazadas de iglesia  32x64 px
Dos paneles que convergen hacia un amarre con roseta dorada en el centro,
y luego se abren de nuevo hacia abajo.

Variantes de color:
  01 entrelazada_roja
  02 entrelazada_morada
  03 entrelazada_blanca
  04 entrelazada_verde
  05 entrelazada_negra
  06 entrelazada_dorada
  07 entrelazada_azul
  08 entrelazada_bordada_roja   - con motivo bordado en cada panel
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
GDK=(110,75,8,255);  GDD=(155,110,15,255); GDM=(205,158,32,255)
GDL=(238,195,58,255);GDH=(255,225,100,255);GDW=(255,248,185,255)
RDK=(60,5,5,255);    RDM=(145,15,15,255); RDL=(198,32,32,255); RDH=(232,62,62,255)
PUK=(30,6,45,255);   PUM=(68,14,92,255);  PUL=(102,25,142,255);PUH=(142,45,192,255)
GRK=(10,45,10,255);  GRM=(22,88,25,255);  GRL=(42,138,46,255); GRH=(70,180,76,255)
BLK=(8,22,80,255);   BLM=(18,55,148,255); BLL=(42,100,208,255);BLH=(88,150,245,255)
YLK=(120,90,4,255);  YLM=(185,148,14,255);YLL=(235,195,38,255);YLH=(255,228,110,255)
WHT=(248,246,238,255);WHS=(215,212,202,255);CRL=(255,252,242,255)
NEK=(16,14,18,255);  NEM=(38,36,42,255);  NEL=(72,70,80,255);  NEH=(112,110,122,255)
SVR=(178,176,186,255);SVL=(220,218,228,255);SVH=(200,198,212,255)

# ── Canvas ────────────────────────────────────────────────────────────────────
def mk_img():
    img = Image.new('RGBA', (W, H), T)
    p   = img.load()
    def px(x, y, c):
        if 0 <= x < W and 0 <= y < H: p[x, y] = c
    return img, px

# ── Parametros de layout ──────────────────────────────────────────────────────
TIE_Y   = 30    # fila del amarre (centro vertical)
TOP_INN = 15    # anchura de cada panel en el top/bottom (x=0..14 y x=17..31)
TIE_INN = 3     # anchura de cada panel en el amarre (x=0..2 y x=29..31)

def panel_width(y):
    """Anchura del panel (borde interior) para la fila y."""
    if y <= TIE_Y:
        t = (y - 4) / max(1, TIE_Y - 4)       # 0 en el top, 1 en el amarre
    else:
        t = (55 - y) / max(1, 55 - TIE_Y)     # 0 en el bottom, 1 en el amarre
    t = t * t * (3.0 - 2.0 * t)               # smoothstep (curva suave)
    return int(TOP_INN - t * (TOP_INN - TIE_INN))

# ── Componentes comunes ───────────────────────────────────────────────────────
def draw_rod(px):
    """Varilla dorada superior con anillos."""
    for x in range(W):
        px(x,0,GDK); px(x,1,GDM); px(x,2,GDL); px(x,3,GDD)
    for x in range(2, W, 5):
        for y in range(0, 4): px(x, y, GDH)

def draw_fringe(px, c1=GDM, c2=GDL, c3=GDH):
    """Flecos en la parte inferior."""
    for x in range(W):
        ph = x % 4
        if ph == 0:
            for y in range(56, 64): px(x, y, c1)
        elif ph == 1:
            for y in range(56, 62): px(x, y, c3)
        elif ph == 2:
            for y in range(56, 64): px(x, y, c2)

def draw_trim(px, c=GDM):
    """Cenefa dorada arriba y abajo de la tela."""
    for x in range(W):
        px(x, 4, c);   px(x, 5,  GDL)
        px(x, 54, c);  px(x, 55, GDL)

def draw_panels(px, col, dark, light):
    """
    Dos paneles de cortina que convergen desde el top hacia el amarre
    (TIE_Y) y luego se abren de nuevo hacia el bottom.
    Incluye pliegues verticales y ligero oscurecimiento vertical.
    """
    for y in range(4, 56):
        inn = panel_width(y)
        if inn < 1: inn = 1
        vt  = (y - 4) / 51.0
        shd = int(vt * 22)   # oscurecimiento progresivo

        # Panel IZQUIERDO: x = 0 .. inn
        for x in range(0, inn + 1):
            fold_t = x / inn
            f      = math.sin(fold_t * math.pi * 4)   # 2 ciclos → 4 pliegues
            if   f >  0.35: base = light
            elif f < -0.35: base = dark
            else:            base = col
            r, g, b, a = base
            px(x, y, (max(0, r-shd), max(0, g-shd), max(0, b-shd), a))

        # Panel DERECHO: simetrico, x = (W-1-inn) .. W-1
        for x in range(W-1-inn, W):
            fold_t = (W-1-x) / inn
            f      = math.sin(fold_t * math.pi * 4)
            if   f >  0.35: base = light
            elif f < -0.35: base = dark
            else:            base = col
            r, g, b, a = base
            px(x, y, (max(0, r-shd), max(0, g-shd), max(0, b-shd), a))

def draw_tieback(px, fabric_dark):
    """
    Amarre decorativo en el centro (roseta dorada + lazo + borlas).
    fabric_dark: color oscuro de la tela, para el pinzamiento.
    """
    cx = W // 2    # 16
    ty = TIE_Y

    # ── Pinzamiento de los paneles en el punto de amarre ─────────────────────
    for y in range(ty-4, ty+5):
        px(TIE_INN,     y, fabric_dark)
        px(W-1-TIE_INN, y, fabric_dark)
    # Arrugas de pinzamiento
    for dy in range(-3, 4):
        px(TIE_INN+1, ty+dy, fabric_dark)
        px(W-2-TIE_INN, ty+dy, fabric_dark)

    # ── Lazo/cinta horizontal ─────────────────────────────────────────────────
    for x in range(TIE_INN+1, W-TIE_INN-1):
        px(x, ty-1, GDD)
        px(x, ty,   GDM)
        px(x, ty+1, GDD)
    # Grueso en los bordes de la cinta
    for y in range(ty-1, ty+2):
        px(TIE_INN+1, y, GDL)
        px(W-TIE_INN-2, y, GDL)

    # ── Roseta central ────────────────────────────────────────────────────────
    for dy in range(-5, 6):
        for dx in range(-5, 6):
            d2 = dx*dx + dy*dy
            if   d2 <= 4:  px(cx+dx, ty+dy, GDW)   # nucleo brillante
            elif d2 <= 10: px(cx+dx, ty+dy, GDH)   # interior
            elif d2 <= 18: px(cx+dx, ty+dy, GDL)   # anillo medio
            elif d2 <= 25: px(cx+dx, ty+dy, GDM)   # borde externo
    # Petalos de la roseta
    for a in range(0, 360, 45):
        rad = math.radians(a)
        px(int(cx + 5.5*math.cos(rad)), int(ty + 5.5*math.sin(rad)), GDH)
    px(cx, ty, GDW)  # centro absoluto

    # ── Borlas que cuelgan de la roseta ───────────────────────────────────────
    for ox in (-3, 0, 3):
        # Hilo
        for y in range(ty+6, ty+14):
            px(cx+ox, y, GDL if y%2==0 else GDM)
        # Punta de la borla
        for dy in range(0, 3):
            for dx in range(-1, 2):
                if dx*dx + dy*dy <= 2:
                    px(cx+ox+dx, ty+14+dy, GDH)
        px(cx+ox, ty+14, GDW)

def draw_embroidery(px, cx_panel, motif_col):
    """
    Pequeno motivo bordado en el centro de cada panel
    (solo visible en la mitad superior, donde el panel es ancho).
    cx_panel: centro x del panel (aprox 7 para izq, 25 para der).
    """
    cy_mot = 14   # y del motivo (parte alta del panel)
    # Cruz simple bordada
    for y in range(cy_mot-4, cy_mot+5):
        px(cx_panel, y, motif_col)
    for x in range(cx_panel-4, cx_panel+5):
        px(x, cy_mot, motif_col)
    # Floron en las puntas de la cruz
    for ang in (0, 90, 180, 270):
        rad = math.radians(ang)
        tip_x = int(cx_panel + 4*math.cos(rad))
        tip_y = int(cy_mot   + 4*math.sin(rad))
        px(tip_x-1 if ang in (90,270) else tip_x, tip_y-1 if ang in (0,180) else tip_y, motif_col)


# ── Generadores ───────────────────────────────────────────────────────────────
def make(col, dark, light, fringe=(GDM, GDL, GDH), trim=GDM,
         rod=True, embroidery=False, emb_col=GDL):
    img, px = mk_img()
    if rod:
        draw_rod(px)
    draw_panels(px, col, dark, light)
    draw_trim(px, trim)
    draw_tieback(px, dark)
    if embroidery:
        draw_embroidery(px, 7,  emb_col)
        draw_embroidery(px, 24, emb_col)
    draw_fringe(px, *fringe)
    return img

def mk_roja():
    return make(RDL, RDK, RDH)

def mk_morada():
    return make(PUL, PUK, PUH)

def mk_blanca():
    return make(WHT, (185,182,172,255), CRL)

def mk_verde():
    return make(GRL, GRK, GRH)

def mk_negra():
    img, px = mk_img()
    draw_rod(px)
    draw_panels(px, NEM, NEK, NEL)
    for x in range(W): px(x,4,NEL); px(x,5,NEH); px(x,54,NEL); px(x,55,NEH)
    draw_tieback(px, NEK)
    draw_fringe(px, SVR, SVL, SVH)
    return img

def mk_dorada():
    return make(YLL, YLK, YLH, fringe=(GDM, GDL, GDW), trim=GDH)

def mk_azul():
    return make(BLL, BLK, BLH)

def mk_bordada_roja():
    return make(RDL, RDK, RDH, embroidery=True, emb_col=GDL)


# ── Exportar ──────────────────────────────────────────────────────────────────
ITEMS = [
    ('entrelazada_roja',         mk_roja        ),
    ('entrelazada_morada',       mk_morada      ),
    ('entrelazada_blanca',       mk_blanca      ),
    ('entrelazada_verde',        mk_verde       ),
    ('entrelazada_negra',        mk_negra       ),
    ('entrelazada_dorada',       mk_dorada      ),
    ('entrelazada_azul',         mk_azul        ),
    ('entrelazada_bordada_roja', mk_bordada_roja),
]

for nombre, fn in ITEMS:
    img   = fn()
    local = os.path.join(OUT_DIR,  f'{nombre}.png')
    copia = os.path.join(PNGS_DIR, f'{nombre}.png')
    img.save(local)
    shutil.copy2(local, copia)
    print(f'OK  {nombre}.png')

print(f'\n{len(ITEMS)} cortinas entrelazadas -> IGLESIA/ y PNGS/')
