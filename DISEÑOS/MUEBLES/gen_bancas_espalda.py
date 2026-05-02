"""
gen_bancas_espalda.py  -  Bancas de iglesia vistas de espalda  48x48 px
Perspectiva RPG 3/4: la camara mira hacia el altar (norte).
El jugador ve la cara posterior del respaldo de cada banca.

Items:
  01 banca_espalda_simple    - Panel liso, tres railes horizontales
  02 banca_espalda_misalero  - Con portamisales en la parte alta y libros
  03 banca_espalda_cruz      - Con cruz tallada en el panel central
  04 banca_espalda_antigua   - Remate curvo, talla ornamental
  05 banca_espalda_brazo     - Vista desde el extremo lateral (brazo visible)
  06 banca_espalda_larga     - Panel mas ancho, 4 secciones
"""
from PIL import Image, ImageDraw
import os, shutil, pathlib, math

_base    = pathlib.Path(__file__).parent
OUT_DIR  = str(_base)
PNGS_DIR = str(_base.parent / 'PNGS')
os.makedirs(PNGS_DIR, exist_ok=True)

S = 48
T   = (  0,   0,   0,   0)
SHC = (  0,   0,   0,  45)

# Madera oscura de iglesia
WDK = ( 28,  12,   4, 255)
WDD = ( 55,  26,   8, 255)
WDM = ( 85,  45,  16, 255)
WDL = (118,  68,  28, 255)
WDH = (155,  95,  45, 255)
WDB = ( 18,   7,   2, 255)   # muy oscuro (sombra profunda)

# Dorado
GDK = (110,  75,   8, 255)
GDD = (155, 110,  15, 255)
GDM = (205, 158,  32, 255)
GDL = (238, 195,  58, 255)

# Libros / misales
BK1 = ( 88,  12,  12, 255)   # rojo oscuro
BK2 = ( 12,  38,  88, 255)   # azul oscuro
BK3 = ( 12,  65,  18, 255)   # verde oscuro
BKP = (238, 220, 185, 255)   # paginas crema

# ── Canvas helper ─────────────────────────────────────────────────────────────
def cv():
    img = Image.new('RGBA', (S, S), T)
    p   = img.load()
    dr  = ImageDraw.Draw(img)
    def px(x, y, c):
        if 0 <= x < S and 0 <= y < S: p[x, y] = c
    def hl(y, x1, x2, c):
        for x in range(x1, x2+1): px(x, y, c)
    def vl(x, y1, y2, c):
        for y in range(y1, y2+1): px(x, y, c)
    def rc(x1, y1, x2, y2, c):
        for yy in range(y1, y2+1):
            for xx in range(x1, x2+1): px(xx, yy, c)
    return img, dr, p, px, hl, vl, rc

# ── Piezas reutilizables ──────────────────────────────────────────────────────

def draw_legs(px):
    """Patas y travesano visibles debajo del respaldo."""
    for y in range(35, 44):
        px( 9, y, WDK); px(10, y, WDD); px(11, y, WDM); px(12, y, WDL)
        px(35, y, WDL); px(36, y, WDM); px(37, y, WDD); px(38, y, WDK)
    for x in range(11, 37):
        px(x, 40, WDK); px(x, 41, WDD); px(x, 42, WDM)

def draw_legs_wide(px):
    """Patas para banca larga."""
    for y in range(35, 44):
        px( 7, y, WDK); px( 8, y, WDD); px( 9, y, WDM)
        px(38, y, WDL); px(39, y, WDM); px(40, y, WDD); px(41, y, WDK)
    # Pata central
    for y in range(38, 44):
        px(22, y, WDK); px(23, y, WDD); px(24, y, WDM)
    for x in range(9, 40):
        px(x, 41, WDK); px(x, 42, WDD)

def draw_side_caps(px, x0=5, x1=43):
    """Costados del respaldo (vista 3/4)."""
    # Costado izquierdo (cara visible del extremo)
    for y in range(10, 35):
        px(x0,   y, WDH); px(x0+1, y, WDL)
        px(x0+2, y, WDM); px(x0+3, y, WDD)
    for x in range(x0, x0+4): px(x, 10, WDH); px(x, 34, WDK)
    # Costado derecho (borde en sombra)
    for y in range(10, 35):
        px(x1-3, y, WDD); px(x1-2, y, WDM)
        px(x1-1, y, WDL); px(x1,   y, WDK)
    for x in range(x1-3, x1+1): px(x, 10, WDH); px(x, 34, WDK)

def draw_top_face(px, x0=6, x1=42, y0=7, y1=10):
    """Cara superior del respaldo (tira 3/4 perspectiva)."""
    for yy in range(y0, y1+1):
        for xx in range(x0, x1+1):
            if yy == y0:              px(xx, yy, WDH)
            elif yy == y1:            px(xx, yy, WDM)
            elif xx == x0:            px(xx, yy, WDH)
            elif xx == x1:            px(xx, yy, WDD)
            else:                     px(xx, yy, WDL)

def draw_back_panel(px, x0=6, y0=10, x1=42, y1=34):
    """Panel trasero del respaldo (cara que mira al jugador)."""
    for yy in range(y0, y1+1):
        for xx in range(x0, x1+1):
            if xx == x0 or xx == x1:  px(xx, yy, WDK)
            elif xx == x0+1:           px(xx, yy, WDD)
            elif xx == x1-1:           px(xx, yy, WDD)
            elif yy == y0:             px(xx, yy, WDK)
            elif yy == y1:             px(xx, yy, WDK)
            else:                      px(xx, yy, WDM)

def draw_rails(px, x0=8, x1=40, ys=(13, 21, 31)):
    """Railes horizontales en el panel trasero."""
    for yr in ys:
        for xx in range(x0, x1+1):
            px(xx, yr, WDK); px(xx, yr+1, WDB)

def draw_panel_recesses(px, panels):
    """Paneles hundidos: lista de (x0,y0,x1,y1)."""
    for (px0, py0, px1, py1) in panels:
        for yy in range(py0, py1+1):
            for xx in range(px0, px1+1):
                if xx == px0 or yy == py0:   p_c = WDK
                elif xx == px1 or yy == py1: p_c = WDL
                else:                        p_c = WDD
                # Solo aplicar si la funcion px esta disponible
        # dibujo manual
        for yy in range(py0, py1+1):
            for xx in range(px0, px1+1):
                if   xx == px0 or yy == py0: px(xx, yy, WDK)
                elif xx == px1 or yy == py1: px(xx, yy, WDL)
                else:                         px(xx, yy, WDD)


# =============================================================================
# 01  BANCA DE ESPALDA SIMPLE
# =============================================================================
def mk_banca_espalda_simple():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(7, 42): px(x, 47, SHC)

    draw_legs(px)
    draw_side_caps(px)
    draw_top_face(px)
    draw_back_panel(px)

    # Tres railes horizontales
    draw_rails(px, ys=(13, 21, 31))

    # Seis paneles hundidos (2 filas x 3 columnas)
    draw_panel_recesses(px, [
        ( 9, 15, 18, 20), (20, 15, 28, 20), (30, 15, 40, 20),
        ( 9, 23, 18, 30), (20, 23, 28, 30), (30, 23, 40, 30),
    ])

    # Divisores verticales
    for y in range(14, 32):
        px(19, y, WDK); px(20, y, WDD)
        px(29, y, WDK); px(30, y, WDD)

    return img


# =============================================================================
# 02  BANCA DE ESPALDA CON MISALERO (porta-misales)
# =============================================================================
def mk_banca_espalda_misalero():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(7, 42): px(x, 47, SHC)

    draw_legs(px)
    draw_side_caps(px)

    # Cara superior del respaldo (sube un poco menos para el misalero)
    draw_top_face(px, y0=8, y1=11)

    # Misalero: repisa en la parte superior del panel trasero
    # (el portamisales de la banca de adelante, visible para los de atras)
    rc(7, 11, 41, 14, WDL)
    for x in range(7, 42): px(x, 11, WDH); px(x, 14, WDK)
    for y in range(11, 15): px(7, y, WDH); px(41, y, WDD)

    # Libros/misales en la repisa
    libros = [
        ( 9, 12, 11, 13, BK1),
        (12, 12, 14, 13, BK2),
        (15, 11, 17, 13, BK3),
        (18, 12, 20, 13, BK1),
        (22, 12, 24, 13, BK2),
        (26, 11, 28, 13, BK3),
        (30, 12, 32, 13, BK1),
        (34, 12, 36, 13, BK2),
        (37, 11, 39, 13, BK3),
    ]
    for (lx0, ly0, lx1, ly1, lc) in libros:
        rc(lx0, ly0, lx1, ly1, lc)
        for x in range(lx0, lx1+1): px(x, ly0, BKP)  # canto/paginas

    # Panel trasero (debajo del misalero)
    draw_back_panel(px, y0=14, y1=34)
    draw_rails(px, ys=(18, 26), x0=8, x1=40)
    draw_panel_recesses(px, [
        ( 9, 20, 20, 25), (21, 20, 31, 25), (32, 20, 40, 25),
        ( 9, 27, 20, 33), (21, 27, 31, 33), (32, 27, 40, 33),
    ])
    for y in range(19, 34):
        px(21, y, WDK); px(22, y, WDD)
        px(31, y, WDK); px(32, y, WDD)

    return img


# =============================================================================
# 03  BANCA DE ESPALDA CON CRUZ TALLADA
# =============================================================================
def mk_banca_espalda_cruz():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(7, 42): px(x, 47, SHC)

    draw_legs(px)
    draw_side_caps(px)
    draw_top_face(px)
    draw_back_panel(px)
    draw_rails(px, ys=(13, 31))

    # Un solo panel grande central
    draw_panel_recesses(px, [
        ( 9, 15, 18, 30),
        (30, 15, 40, 30),
    ])
    for y in range(14, 32): px(19, y, WDK); px(29, y, WDK)

    # Cruz tallada en el panel central (relieve hundido)
    cx, cy = 24, 22
    # Vertical
    for y in range(15, 31):
        px(cx-1, y, WDK); px(cx, y, WDL); px(cx+1, y, WDM)
    # Horizontal
    for x in range(20, 29):
        px(x, cy-1, WDK); px(x, cy, WDL); px(x, cy+1, WDM)
    # Centro brillante
    px(cx, cy, WDH); px(cx+1, cy, WDL)

    # Pequeños motivos en las esquinas del panel central
    for (mx, my) in [(21,16),(27,16),(21,29),(27,29)]:
        px(mx, my, WDK); px(mx+1, my, WDD)
        px(mx, my+1, WDD)

    return img


# =============================================================================
# 04  BANCA DE ESPALDA ANTIGUA (remate curvo, talla ornamental)
# =============================================================================
def mk_banca_espalda_antigua():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(7, 42): px(x, 47, SHC)

    draw_legs(px)

    # Costados ornamentados (mas gruesos)
    for y in range(5, 35):
        px(4, y, WDH); px(5, y, WDL); px(6, y, WDM); px(7, y, WDD); px(8, y, WDK)
        px(39, y, WDD); px(40, y, WDM); px(41, y, WDL); px(42, y, WDH); px(43, y, WDK)
    for x in range(4, 9):  px(x, 5, WDH); px(x, 34, WDK)
    for x in range(39, 44): px(x, 5, WDH); px(x, 34, WDK)

    # Remate curvo superior (arco en el centro)
    for x in range(9, 39):
        # Curva: mas alto en el centro, baja en los extremos
        dist_center = abs(x - 23)
        top_y = max(4, 7 - int(3 * math.cos(dist_center / 16.0 * math.pi * 0.5)))
        # Cara superior del arco
        for y in range(top_y, top_y+3):
            if   y == top_y:   px(x, y, WDH)
            elif y == top_y+1: px(x, y, WDL)
            else:              px(x, y, WDM)

    # Panel trasero principal
    draw_back_panel(px, x0=8, y0=10, x1=40, y1=34)
    draw_rails(px, x0=10, x1=38, ys=(14, 23, 32))

    # Talla ornamental: floron central
    cx, cy = 24, 18
    # Petalo superior/inferior
    for d in range(1, 5):
        px(cx, cy-d, WDL if d<3 else WDM); px(cx, cy+d, WDL if d<3 else WDM)
        px(cx-d, cy, WDL if d<3 else WDM); px(cx+d, cy, WDL if d<3 else WDM)
    # Diagonales del floron
    for d in range(1, 4):
        px(cx-d, cy-d, WDM); px(cx+d, cy-d, WDM)
        px(cx-d, cy+d, WDM); px(cx+d, cy+d, WDM)
    px(cx, cy, WDH)

    # Paneles inferiores
    draw_panel_recesses(px, [
        (10, 25, 18, 33), (20, 25, 28, 33), (30, 25, 38, 33)
    ])
    for y in range(25, 34): px(19, y, WDK); px(29, y, WDK)

    # Borde tallado en el remate (linea de puntitos)
    for x in range(9, 39, 3): px(x, 11, WDL)

    return img


# =============================================================================
# 05  BANCA DE ESPALDA VISTA DESDE EL EXTREMO (brazo lateral)
# =============================================================================
def mk_banca_espalda_brazo():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(4, 44): px(x, 47, SHC)

    # Pata visible (solo un extremo)
    for y in range(30, 44):
        px(32, y, WDK); px(33, y, WDD); px(34, y, WDM); px(35, y, WDL)
    for x in range(33, 44): px(x, 41, WDK); px(x, 42, WDD)

    # ── Brazo/apoyabrazos (costado de la banca) ────────────────────────────────
    # Vista lateral del extremo: se ve el costado del respaldo y el asiento

    # Cara exterior del brazo (frente hacia el jugador)
    rc(4, 10, 30, 34, WDD)
    rc(5, 11, 29, 33, WDM)
    for y in range(10, 35): px(4, y, WDH); px(5, y, WDL); px(29, y, WDD); px(30, y, WDK)
    for x in range(4, 31): px(x, 10, WDH); px(x, 34, WDK)

    # Cara superior del brazo
    rc(4, 7, 31, 10, WDL)
    for x in range(4, 32): px(x, 7, WDH); px(x, 10, WDM)
    for y in range(7, 11): px(4, y, WDH); px(31, y, WDD)

    # Remate curvo del extremo del brazo (ornamento tallado)
    for y in range(7, 12):
        for x in range(26, 32):
            dist = math.sqrt((x-26)**2 + (y-12)**2)
            if dist < 5.5:
                if dist > 4.5: px(x, y, WDK)
                else:          px(x, y, WDL)
    px(28, 8, WDH); px(29, 8, WDL)

    # Panel lateral con detalle (lo que se ve en el costado del respaldo)
    draw_rails(px, x0=6, x1=28, ys=(14, 22, 30))
    draw_panel_recesses(px, [
        ( 6, 16, 16, 21), (18, 16, 28, 21),
        ( 6, 24, 16, 29), (18, 24, 28, 29),
    ])
    for y in range(15, 31): px(17, y, WDK); px(18, y, WDD)

    # Cara del respaldo (el panel que mira al altar, en perspectiva)
    # (franja derecha, efecto de profundidad)
    rc(30, 10, 35, 34, WDK)
    for y in range(10, 35):
        px(30, y, WDK); px(31, y, WDD); px(32, y, WDM)
        px(33, y, WDM); px(34, y, WDD); px(35, y, WDK)
    # Cara superior del respaldo (fino)
    rc(30, 7, 36, 10, WDM)
    for x in range(30, 37): px(x, 7, WDL)

    # Asiento (apenas visible debajo del respaldo, en sombra)
    rc(5, 34, 35, 38, WDK)
    for x in range(5, 36): px(x, 34, WDD)

    return img


# =============================================================================
# 06  BANCA DE ESPALDA LARGA (4 secciones de panel)
# =============================================================================
def mk_banca_espalda_larga():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(4, 44): px(x, 47, SHC)

    draw_legs_wide(px)
    draw_side_caps(px, x0=4, x1=43)
    draw_top_face(px, x0=5, x1=43, y0=7, y1=10)
    draw_back_panel(px, x0=5, y0=10, x1=43, y1=34)
    draw_rails(px, x0=7, x1=41, ys=(13, 21, 31))

    # 4 columnas de paneles
    dividers = (15, 23, 31)
    for xd in dividers:
        for y in range(14, 32): px(xd, y, WDK); px(xd+1, y, WDD)

    draw_panel_recesses(px, [
        ( 8, 15, 14, 20), (16, 15, 22, 20), (24, 15, 30, 20), (32, 15, 41, 20),
        ( 8, 23, 14, 30), (16, 23, 22, 30), (24, 23, 30, 30), (32, 23, 41, 30),
    ])

    # Misalero fino (solo una linea con libros, a lo largo)
    for x in range(6, 43): px(x, 11, WDL)
    # Algunos libros
    for lx in range(7, 42, 5):
        col = [BK1, BK2, BK3][lx % 3]
        px(lx, 12, col); px(lx+1, 12, col)
        px(lx, 13, col); px(lx+1, 13, col)
        px(lx, 12, BKP)  # canto

    return img


# ── Generar ───────────────────────────────────────────────────────────────────
ITEMS = [
    ('banca_espalda_simple',   mk_banca_espalda_simple  ),
    ('banca_espalda_misalero', mk_banca_espalda_misalero),
    ('banca_espalda_cruz',     mk_banca_espalda_cruz    ),
    ('banca_espalda_antigua',  mk_banca_espalda_antigua ),
    ('banca_espalda_brazo',    mk_banca_espalda_brazo   ),
    ('banca_espalda_larga',    mk_banca_espalda_larga   ),
]

for nombre, fn in ITEMS:
    img   = fn()
    local = os.path.join(OUT_DIR,  f'{nombre}.png')
    copia = os.path.join(PNGS_DIR, f'{nombre}.png')
    img.save(local)
    shutil.copy2(local, copia)
    print(f'OK  {nombre}.png')

print(f'\n{len(ITEMS)} bancas de espalda -> MUEBLES/ y PNGS/')
