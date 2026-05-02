"""
gen_iglesia.py  –  Muebles de iglesia  48×48 px  (perspectiva RPG 3/4)
Genera los PNGs en la misma carpeta MUEBLES/ y copia a PNGS/.

Items:
  01 banca_iglesia    - banca larga de madera oscura con respaldo tallado y reclinatorio
  02 altar_mayor      - altar de piedra con mantel rojo, cruz dorada y velas
  03 veladora         - candelero de hierro con velas votivas encendidas
  04 atril            - atril de madera con libro abierto
  05 pila_agua        - pila de agua bendita de mármol
  06 reclinatorio     - reclinatorio individual con apoyalibros
  07 confesionario    - confesionario de madera con cortina morada y celosía
  08 cruz_altar       - crucifijo sobre base de piedra con corpus dorado
  09 incensario       - incensario de metal con cadenas y volutas de humo
  10 organo           - órgano de tubos con caja tallada y tubos dorados
"""

from PIL import Image, ImageDraw
import os, shutil, math
import pathlib

_base    = pathlib.Path(__file__).parent
OUT_DIR  = str(_base)
PNGS_DIR = str(_base.parent / 'PNGS')
os.makedirs(OUT_DIR,  exist_ok=True)
os.makedirs(PNGS_DIR, exist_ok=True)

S = 48

# ── Paleta ───────────────────────────────────────────────────────────────────
T   = (  0,   0,   0,   0)
SHC = (  0,   0,   0,  45)

# Madera oscura de iglesia
WDK = ( 28,  12,   4, 255)
WDD = ( 55,  26,   8, 255)
WDM = ( 85,  45,  16, 255)
WDL = (118,  68,  28, 255)
WDH = (155,  95,  45, 255)

# Piedra / mármol (reutiliza nombres de generador.py)
SD  = ( 88,  82,  76, 255); SM  = (128, 122, 115, 255)
SL  = (172, 166, 158, 255); SHH = (212, 207, 199, 255)
MA  = (238, 232, 220, 255); MB  = (215, 208, 196, 255)
MC  = (188, 180, 168, 255); MDK = (150, 142, 130, 255)

# Metal / hierro
ID  = ( 35,  35,  40, 255); IM  = ( 60,  60,  68, 255)
IL  = ( 92,  92, 102, 255); IH  = (138, 138, 152, 255)
BOM = ( 15,  15,  18, 255)

# Dorado / oro
GDK = (110,  75,   8, 255)
GDD = (155, 110,  15, 255)
GDM = (205, 158,  32, 255)
GDL = (238, 195,  58, 255)
GDH = (255, 225, 100, 255)
GDW = (255, 248, 185, 255)

# Tela roja (mantel de altar)
TDK = ( 65,   8,   8, 255)
TDM = (120,  15,  15, 255)
TDL = (168,  26,  26, 255)
TDH = (208,  48,  48, 255)

# Vela / llama / cera
WAX = (255, 248, 228, 255)
WAD = (220, 208, 178, 255)
FDK = (185,  62,   5, 255)
FDM = (235, 128,  18, 255)
FDL = (255, 202,  45, 255)
FDH = (255, 240, 155, 255)

# Agua (pila)
WAT = ( 28,  88, 175, 255)
WAM = ( 55, 138, 215, 255)
WAL = (115, 185, 252, 255)
WAH = (198, 228, 255, 255)

# Tela morada (Cuaresma / Adviento)
PUK = ( 35,   8,  50, 255)
PUM = ( 70,  16,  95, 255)
PUL = (105,  28, 145, 255)
PUH = (145,  48, 195, 255)

# Marfil / crema
IVD = (215, 205, 188, 255)
IVM = (235, 226, 210, 255)
IVL = (248, 242, 228, 255)

# Humo / gris
SMK = ( 80,  78,  82, 180)
SML2= (140, 138, 145, 120)
SMH2= (195, 193, 200,  70)

# Aliases internos
IDM = IM; IML = IL; MAK = MDK; IVH = IVL; SMM = SML2


# ── Helpers (igual que generador.py) ─────────────────────────────────────────
def cv():
    img = Image.new('RGBA', (S, S), T)
    p   = img.load()
    dr  = ImageDraw.Draw(img)

    def px(x, y, c):
        if 0 <= x < S and 0 <= y < S: p[x, y] = c

    def hl(y, x1, x2, c):
        for x in range(x1, x2 + 1): px(x, y, c)

    def vl(x, y1, y2, c):
        for y in range(y1, y2 + 1): px(x, y, c)

    def rc(x1, y1, x2, y2, c):
        for yy in range(y1, y2 + 1):
            for xx in range(x1, x2 + 1): px(xx, yy, c)

    return img, dr, p, px, hl, vl, rc


# ── Utilidad: dibujar vela con llama ─────────────────────────────────────────
def draw_candle(px, cx, ytop, height=10):
    """Dibuja una vela centrada en cx desde ytop hacia abajo."""
    # Cuerpo de la vela
    for y in range(ytop + 2, ytop + height):
        px(cx - 1, y, WAD); px(cx, y, WAX); px(cx + 1, y, WAD)
    # Mecha
    px(cx, ytop + 1, WDK)
    # Llama (4px de alto encima)
    px(cx,     ytop - 2, FDH)
    px(cx,     ytop - 1, FDL); px(cx - 1, ytop - 1, FDH)
    px(cx,     ytop,     FDM); px(cx - 1, ytop, FDL); px(cx + 1, ytop, FDL)
    px(cx,     ytop + 1, FDK)


# =============================================================================
# 01  BANCA DE IGLESIA
# =============================================================================
def mk_banca_iglesia():
    img, dr, p, px, hl, vl, rc = cv()

    # Sombra
    for x in range(7, 42): px(x, 47, SHC)

    # ── Reclinatorio (arrodilladera) ─────────────────────────────────────────
    for x in range(6, 43): px(x, 43, WDH); px(x, 44, WDL); px(x, 45, WDD); px(x, 46, WDK)
    for y in range(43, 47): px(5, y, WDK); px(6, y, WDD); px(42, y, WDD); px(43, y, WDK)

    # ── Patas ────────────────────────────────────────────────────────────────
    for y in range(32, 44):
        px(9, y, WDK); px(10, y, WDD); px(11, y, WDM); px(12, y, WDL)
        px(35, y, WDL); px(36, y, WDM); px(37, y, WDD); px(38, y, WDK)
    # Travesano entre patas
    for x in range(10, 38): px(x, 38, WDK); px(x, 39, WDD); px(x, 40, WDM); px(x, 41, WDK)

    # ── Asiento — 3 tablones ─────────────────────────────────────────────────
    hl(22, 6, 42, WDK)
    for x in range(7, 42): px(x, 23, WDH); px(x, 24, WDL)
    hl(25, 6, 42, WDK)
    for x in range(7, 42): px(x, 26, WDH); px(x, 27, WDL)
    hl(28, 6, 42, WDK)
    for x in range(7, 42): px(x, 29, WDL); px(x, 30, WDM)
    hl(31, 6, 42, WDK)
    # Cara frontal del asiento
    for x in range(6, 43): px(x, 32, WDD); px(x, 33, WDK)
    # Laterales
    for y in range(22, 34):
        px(5, y, WDK); px(6, y, WDD); px(42, y, WDD); px(43, y, WDK)

    # ── Apoyabrazos ──────────────────────────────────────────────────────────
    for y in range(16, 34):
        px(4, y, WDK); px(5, y, WDD); px(43, y, WDD); px(44, y, WDK)
    for x in range(4, 11):
        px(x, 15, WDK); px(x, 16, WDM); px(x, 17, WDL); px(x, 18, WDH)
    for x in range(37, 45):
        px(x, 15, WDK); px(x, 16, WDM); px(x, 17, WDL); px(x, 18, WDH)

    # ── Respaldo ─────────────────────────────────────────────────────────────
    # Barra superior
    for x in range(5, 44):
        px(x,  5, WDK); px(x,  6, WDD); px(x,  7, WDM)
        px(x,  8, WDL); px(x,  9, WDH)
    # Barra inferior
    for x in range(5, 44):
        px(x, 19, WDH); px(x, 20, WDL); px(x, 21, WDM); px(x, 22, WDK)
    # Tres paneles verticales
    for y in range(8, 22):
        for xi, ci in [(6,WDK),(7,WDD),(8,WDM),(9,WDL),(10,WDH),(11,WDL),(12,WDM),(13,WDD),(14,WDK)]:
            px(xi, y, ci)
        for xi, ci in [(17,WDK),(18,WDD),(19,WDM),(20,WDL),(21,WDH),(22,WDL),(23,WDM),(24,WDD),(25,WDK)]:
            px(xi, y, ci)
        for xi, ci in [(29,WDK),(30,WDD),(31,WDM),(32,WDL),(33,WDH),(34,WDL),(35,WDM),(36,WDD),(37,WDK)]:
            px(xi, y, ci)
    # Laterales del respaldo
    for y in range(5, 23):
        px(4, y, WDK); px(5, y, WDK); px(43, y, WDK); px(44, y, WDK)

    # ── Cruz tallada dorada en panel central ──────────────────────────────────
    # Brazo vertical (x=20..22, y=9..21)
    for y in range(9, 21): px(20, y, GDK); px(21, y, GDM); px(22, y, GDD)
    # Brazo horizontal (x=18..24, y=12..14)
    for x in range(18, 25): px(x, 12, GDK); px(x, 13, GDM); px(x, 14, GDD)
    # Highlight intersección
    px(21, 13, GDH)

    return img


# =============================================================================
# 02  ALTAR MAYOR
# =============================================================================
def mk_altar_mayor():
    img, dr, p, px, hl, vl, rc = cv()

    # Sombra
    for x in range(4, 45): px(x, 47, SHC)

    # ── Escalones (2 peldaños de piedra) ─────────────────────────────────────
    # Escalón inferior
    rc(3, 43, 44, 46, SM)
    for x in range(3, 45): px(x, 43, SHH); px(x, 46, SD)
    for y in range(43, 47): px(3, y, SD); px(44, y, SD)
    # Escalón superior
    rc(6, 40, 41, 43, SL)
    for x in range(6, 42): px(x, 40, SHH); px(x, 43, SD)

    # ── Mantel frontal rojo ───────────────────────────────────────────────────
    # Franja horizontal superior
    rc(7, 23, 40, 25, TDH)
    rc(7, 25, 40, 38, TDM)
    rc(7, 38, 40, 40, TDK)
    # Borde dorado del mantel
    for y in range(23, 41): px(7, y, GDD); px(40, y, GDD)
    hl(23, 7, 40, GDD); hl(40, 7, 40, GDD)
    # Cruz dorada bordada en el centro del mantel
    for y in range(26, 38): px(22, y, GDM); px(23, y, GDL); px(24, y, GDM)
    for x in range(18, 29): px(x, 30, GDM); px(x, 31, GDL); px(x, 32, GDM)
    px(23, 31, GDH)
    # Pliegues del mantel
    for y in range(24, 40): px(13, y, TDL); px(20, y, TDK); px(27, y, TDL); px(34, y, TDK)

    # ── Superficie superior del altar (mármol) ────────────────────────────────
    rc(6, 17, 41, 23, MA)
    for x in range(6, 42): px(x, 17, IVL); px(x, 23, MC)
    for y in range(17, 24): px(6, y, IVM); px(41, y, MC)
    # Venas del mármol
    for x in range(10, 38): px(x, 19, MB); px(x, 21, MB)
    px(15, 18, MC); px(25, 20, MC); px(32, 19, MC)

    # ── Cruz grande dorada (sobre el altar) ───────────────────────────────────
    # Vertical: x=22..25, y=4..17
    for y in range(4, 17):
        px(22, y, GDK); px(23, y, GDM); px(24, y, GDL); px(25, y, GDD)
    # Horizontal: x=15..32, y=8..11
    for x in range(15, 33):
        px(x,  8, GDK); px(x,  9, GDM); px(x, 10, GDL); px(x, 11, GDD)
    # Highlights de la cruz
    for y in range(4, 17): px(24, y, GDH)
    for x in range(15, 33): px(x,  9, GDH)
    px(24, 9, GDW)
    # Base de la cruz (pequeño pedestal)
    rc(20, 16, 27, 18, GDD)
    for x in range(19, 29): px(x, 16, GDH)

    # ── Dos velas sobre el altar ──────────────────────────────────────────────
    draw_candle(px, 11, 12, height=6)
    draw_candle(px, 36, 12, height=6)

    return img


# =============================================================================
# 03  VELADORA (candelero votivo)
# =============================================================================
def mk_veladora():
    img, dr, p, px, hl, vl, rc = cv()

    dr.ellipse([14, 43, 34, 47], fill=(0, 0, 0, 38))

    # ── Base / pie de hierro ──────────────────────────────────────────────────
    dr.ellipse([14, 41, 34, 47], fill=IDM)
    for x in range(15, 34): px(x, 41, IH); px(x, 45, ID)

    # ── Poste central ────────────────────────────────────────────────────────
    for y in range(14, 42):
        px(22, y, BOM); px(23, y, IM); px(24, y, IL); px(25, y, BOM)

    # ── Bandeja superior (donde van las velas grandes) ────────────────────────
    rc(12, 12, 35, 14, IDM)
    for x in range(12, 36): px(x, 12, IH); px(x, 14, ID)
    for y in range(12, 15): px(12, y, IH); px(35, y, ID)

    # ── Bandeja intermedia ────────────────────────────────────────────────────
    rc(15, 24, 32, 26, IDM)
    for x in range(15, 33): px(x, 24, IH); px(x, 26, ID)

    # ── Velas — fila superior (5 velas pequeñas) ─────────────────────────────
    # Vasitos de vidrio rojo
    candle_xs_top = [14, 18, 22, 26, 30, 34]
    for cx in candle_xs_top:
        # Vasito rojo (4px alto)
        for y in range(9, 13):
            px(cx - 1, y, TDM); px(cx, y, TDL); px(cx + 1, y, TDM)
        px(cx - 1, 9, TDH); px(cx, 9, TDH); px(cx + 1, 9, TDH)
        # Llama
        px(cx,  6, FDH)
        px(cx,  7, FDL); px(cx - 1, 7, FDH)
        px(cx,  8, FDM); px(cx + 1, 8, FDL)
        # Cera
        px(cx, 8, WAX)

    # ── Velas fila intermedia (3 velas medianas) ──────────────────────────────
    for cx in [17, 24, 31]:
        for y in range(20, 25): px(cx - 1, y, WAD); px(cx, y, WAX); px(cx + 1, y, WAD)
        # Vasito ámbar
        for y in range(23, 25): px(cx - 1, y, TDL); px(cx, y, TDL); px(cx + 1, y, TDL)
        # Llama
        draw_candle(px, cx, 19, height=1)

    return img


# =============================================================================
# 04  ATRIL
# =============================================================================
def mk_atril():
    img, dr, p, px, hl, vl, rc = cv()

    dr.ellipse([14, 43, 34, 47], fill=(0, 0, 0, 35))

    # ── Base de tres pies ────────────────────────────────────────────────────
    for y in range(38, 44):
        px(20, y, WDK); px(21, y, WDD); px(22, y, WDM)  # pie izq
        px(26, y, WDM); px(27, y, WDD); px(28, y, WDK)  # pie der
    for y in range(38, 46):
        px(23, y, WDK); px(24, y, WDD); px(25, y, WDK)  # pie centro

    # ── Poste central ────────────────────────────────────────────────────────
    for y in range(20, 39):
        px(22, y, WDK); px(23, y, WDD); px(24, y, WDM); px(25, y, WDL); px(26, y, WDK)

    # ── Águila decorativa (simplificada) como base del atril ─────────────────
    # Alas abiertas en y=24..28
    for x in range(14, 22):
        py2 = 26 - (x - 14) // 3
        px(x, py2,     WDM); px(x, py2 + 1, WDD); px(x, py2 + 2, WDK)
    for x in range(27, 35):
        py2 = 26 - (34 - x) // 3
        px(x, py2,     WDM); px(x, py2 + 1, WDD); px(x, py2 + 2, WDK)
    # Cuerpo del águila
    rc(21, 24, 27, 30, WDD)
    for x in range(21, 28): px(x, 24, WDM)
    # Cabeza
    px(23, 22, WDD); px(24, 22, WDM); px(25, 22, WDD)
    px(23, 23, WDK); px(24, 23, WDD); px(25, 23, WDK)
    # Pico
    px(25, 23, GDM); px(26, 24, GDD)

    # ── Superficie inclinada del atril ────────────────────────────────────────
    # Forma trapezoidal ligeramente inclinada (simula perspectiva)
    pts_top = [(9, 20), (39, 20), (37, 10), (11, 10)]
    dr.polygon(pts_top, fill=WDL)
    # Borde superior
    for x in range(11, 38): px(x, 10, WDH)
    # Borde inferior
    for x in range(9,  40): px(x, 20, WDK)
    # Laterales
    for y in range(10, 21): px(9, y, WDK); px(39, y, WDK)
    # Veta de madera
    for x in range(12, 37): px(x, 13, WDM); px(x, 17, WDM)
    # Borde de apoyo del libro
    for x in range(10, 39): px(x, 19, WDD)

    # ── Libro abierto ────────────────────────────────────────────────────────
    # Hoja izquierda
    rc(11, 11, 23, 19, IVL)
    for x in range(11, 24): px(x, 11, IVM); px(x, 19, IVD)
    for y in range(11, 20): px(11, y, IVD)
    # Hoja derecha
    rc(25, 11, 37, 19, IVL)
    for x in range(25, 38): px(x, 11, IVM); px(x, 19, IVD)
    for y in range(11, 20): px(37, y, IVD)
    # Lomo central
    vl(24, 11, 19, WDK)
    # Líneas de texto (simuladas)
    for ly in range(13, 19, 2):
        for x in range(12, 23): px(x, ly, MC)
        for x in range(26, 37): px(x, ly, MC)
    # Letras grandes (iniciales iluminadas)
    px(12, 12, GDM); px(13, 12, GDM); px(12, 13, GDM)   # 'L' izquierda
    px(26, 12, GDM); px(27, 12, GDM); px(27, 13, GDM)   # inicio derecha

    return img


# =============================================================================
# 05  PILA DE AGUA BENDITA
# =============================================================================
def mk_pila_agua():
    img, dr, p, px, hl, vl, rc = cv()

    dr.ellipse([13, 43, 35, 47], fill=(0, 0, 0, 40))

    # ── Base / pedestal ────────────────────────────────────────────────────
    # Pie
    dr.ellipse([12, 42, 36, 47], fill=SM)
    rc(12, 43, 36, 46, SM)
    for x in range(12, 37): px(x, 42, SHH); px(x, 46, SD)
    # Columna
    for y in range(28, 43):
        px(19, y, SD); px(20, y, SM); px(21, y, SL); px(22, y, SHH)
        px(23, y, SHH); px(24, y, SL); px(25, y, SM); px(26, y, SD); px(27, y, SD)
    # Anillo decorativo en la columna
    for x in range(19, 28): px(x, 32, SHH); px(x, 36, SHH)

    # ── Pila (cuenco ancho, forma de concha/media esfera) ───────────────────
    # Cuenco exterior de mármol
    dr.ellipse([ 6, 18, 42, 32], fill=SM)
    dr.ellipse([ 7, 19, 41, 31], fill=SL)
    # Borde superior (highlight)
    for x in range(7, 42):
        if p[x, 19][3] > 100: px(x, 19, SHH)
    # Borde inferior
    for x in range(6, 43):
        if p[x, 31][3] > 100: px(x, 31, SD)
    for y in range(18, 32):
        if p[6,  y][3] > 100: px(6,  y, SD)
        if p[42, y][3] > 100: px(42, y, SD)
    # Interior de la pila — agua
    dr.ellipse([10, 21, 38, 29], fill=WAT)
    dr.ellipse([12, 22, 36, 28], fill=WAM)
    dr.ellipse([15, 23, 33, 27], fill=WAL)
    dr.ellipse([18, 24, 30, 26], fill=WAH)
    # Reflejo del agua
    for x in range(13, 22): px(x, 24, WAH)
    # Detalle de concha (nervaduras radiales)
    for xi, yi in [(8,28),(11,30),(14,31),(18,31),(22,31),(26,31),(30,31),(34,30),(37,29)]:
        px(xi, yi, SD); px(xi, yi - 1, SM)

    # ── Cruz en relieve sobre el cuenco ───────────────────────────────────
    px(23, 20, GDM); px(24, 20, GDL)
    px(21, 21, GDD); px(22, 21, GDM); px(23, 21, GDL); px(24, 21, GDL); px(25, 21, GDD)
    px(23, 22, GDM); px(24, 22, GDL)

    return img


# =============================================================================
# 06  RECLINATORIO
# =============================================================================
def mk_reclinatorio():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(5, 44): px(x, 47, SHC)

    # ── Panel frontal (apoyalibros) ───────────────────────────────────────────
    rc(7, 28, 40, 40, WDM)
    for x in range(7, 41): px(x, 28, WDH); px(x, 40, WDK)
    for y in range(28, 41): px(7, y, WDH); px(40, y, WDK)
    # Marco interior del panel
    rc(9, 30, 38, 38, WDL)
    for x in range(9, 39): px(x, 30, WDH); px(x, 38, WDD)
    for y in range(30, 39): px(9, y, WDH); px(38, y, WDD)
    # Cruz dorada en el panel
    vl(24, 31, 37, GDM); px(23, 31, GDD); px(25, 31, GDD)
    hl(34, 21, 27, GDM); px(20, 34, GDD); px(28, 34, GDD)
    for x in range(21, 28): px(x, 34, GDM)
    for y in range(31, 38): px(24, y, GDM)
    px(24, 34, GDH)
    # Pequeño libro en el panel
    rc(10, 31, 18, 37, IVL)
    for x in range(10, 19): px(x, 31, IVM)
    for ly in range(32, 37, 2):
        for x in range(11, 18): px(x, ly, MC)

    # ── Patas del panel ───────────────────────────────────────────────────────
    for y in range(40, 46):
        px( 9, y, WDK); px(10, y, WDD); px(11, y, WDM)
        px(37, y, WDM); px(38, y, WDD); px(39, y, WDK)

    # ── Superficie de arrodillarse (cojín acolchado) ──────────────────────────
    # La vemos desde arriba/frente en perspectiva 3/4
    rc(6, 20, 41, 27, TDM)
    for x in range(6, 42): px(x, 20, TDH); px(x, 27, TDK)
    for y in range(20, 28): px(6, y, TDH); px(41, y, TDK)
    # Acolchado: botones hundidos
    for bx, by in [(14, 23), (24, 23), (33, 23)]:
        px(bx, by, TDK); px(bx + 1, by, TDK)
        px(bx, by - 1, TDH); px(bx + 1, by - 1, TDH)
    # Ribete dorado del cojín
    for x in range(6, 42): px(x, 21, GDK)
    for x in range(6, 42): px(x, 26, GDK)

    # ── Marco del cojín (madera) ──────────────────────────────────────────────
    for y in range(18, 21):
        px(5, y, WDK); px(6, y, WDD); px(41, y, WDD); px(42, y, WDK)
    for x in range(5, 43): px(x, 17, WDK); px(x, 18, WDH)

    return img


# =============================================================================
# 07  CONFESIONARIO
# =============================================================================
def mk_confesionario():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(4, 44): px(x, 47, SHC)

    # ── Cuerpo principal (cabina grande a la derecha) ─────────────────────────
    # Parte del sacerdote (izq): x=4..22
    rc(5, 8, 22, 42, WDD)
    for x in range(5, 23): px(x, 8, WDH); px(x, 42, WDK)
    for y in range(8, 43): px(5, y, WDH); px(22, y, WDK)
    # Puerta de madera
    rc(6, 10, 21, 41, WDM)
    for x in range(7, 21): px(x, 10, WDL); px(x, 41, WDD)
    for y in range(10, 42): px(6, y, WDL); px(21, y, WDD)
    # Celosía / reja del sacerdote (ventanita con malla)
    rc(8, 15, 19, 26, IDM)
    # Malla: patrón de cuadros
    for y in range(15, 27, 2):
        for x in range(8, 20, 2): px(x, y, IML)
    for x in range(8, 20): px(x, 15, IH); px(x, 26, ID)
    for y in range(15, 27): px(8, y, IH); px(19, y, ID)
    # Manija
    px(20, 25, IH); px(20, 26, IH); px(20, 27, IH)

    # ── Parte del penitente (der): x=23..43 ──────────────────────────────────
    rc(23, 10, 42, 42, WDD)
    for x in range(23, 43): px(x, 10, WDH); px(x, 42, WDK)
    for y in range(10, 43): px(23, y, WDK); px(42, y, WDH)
    # Interior
    rc(24, 11, 41, 41, WDM)

    # ── Cortina morada del penitente ──────────────────────────────────────────
    rc(25, 12, 40, 40, PUM)
    # Pliegues de la cortina
    for y in range(12, 41):
        px(27, y, PUK); px(30, y, PUL); px(33, y, PUK); px(36, y, PUL); px(39, y, PUK)
    for x in range(25, 41): px(x, 12, PUH); px(x, 40, PUK)
    # Barra de la cortina (arriba)
    for x in range(24, 42): px(x, 11, IDM); px(x, 12, IH)

    # ── Tejado / remate superior ─────────────────────────────────────────────
    rc(4, 4, 43, 9, WDL)
    for x in range(4, 44): px(x, 4, WDH); px(x, 9, WDK)
    for y in range(4, 10): px(4, y, WDH); px(43, y, WDK)
    # Cruz en el centro del remate
    vl(23, 4, 8, GDK); vl(24, 4, 8, GDM); vl(25, 4, 8, GDD)
    hl(6, 21, 27, GDK); hl(7, 21, 27, GDM)
    px(24, 7, GDH)

    # ── Divisor central (marco entre las dos cabinas) ─────────────────────────
    for y in range(8, 43):
        px(22, y, WDK); px(23, y, WDK)

    # ── Peldaño inferior ─────────────────────────────────────────────────────
    rc(4, 42, 43, 45, SM)
    for x in range(4, 44): px(x, 42, SHH); px(x, 45, SD)

    return img


# =============================================================================
# 08  CRUZ DE ALTAR (crucifijo)
# =============================================================================
def mk_cruz_altar():
    img, dr, p, px, hl, vl, rc = cv()

    dr.ellipse([12, 43, 36, 47], fill=(0, 0, 0, 42))

    # ── Base escalonada de piedra ────────────────────────────────────────────
    # Escalón 1 (base grande)
    rc(10, 42, 38, 46, SM)
    for x in range(10, 39): px(x, 42, SHH); px(x, 46, SD)
    for y in range(42, 47): px(10, y, SD); px(38, y, SD)
    # Escalón 2
    rc(14, 38, 34, 42, SL)
    for x in range(14, 35): px(x, 38, SHH); px(x, 42, SD)
    for y in range(38, 43): px(14, y, SD); px(34, y, SD)
    # Peana (plataforma de la cruz)
    rc(17, 34, 31, 38, MA)
    for x in range(17, 32): px(x, 34, IVL); px(x, 38, MAK)
    for y in range(34, 39): px(17, y, IVL); px(31, y, MAK)

    # ── Cruz (dark metal con borde dorado) ────────────────────────────────────
    # Palo vertical: x=22..25, y=6..34
    for y in range(6, 34):
        px(22, y, GDK); px(23, y, GDD); px(24, y, GDL); px(25, y, GDD)
    # Brazo horizontal: x=13..34, y=14..18
    for x in range(13, 35):
        px(x, 14, GDK); px(x, 15, GDD); px(x, 16, GDL); px(x, 17, GDD)
    # Inscripción INRI (tira dorada en el tope)
    rc(19, 6, 28, 9, GDM)
    for x in range(19, 29): px(x, 6, GDH); px(x, 9, GDK)
    # Letras I N R I
    px(20, 7, WDK); px(20, 8, WDK)   # I
    px(22, 7, WDK); px(23, 7, WDK); px(22, 8, WDK)  # N
    px(25, 7, WDK); px(26, 7, WDK); px(25, 8, WDK)  # R
    px(27, 7, WDK); px(27, 8, WDK)   # I
    # Highlights de la cruz
    for y in range(6, 34): px(24, y, GDH)
    for x in range(13, 35): px(x, 16, GDH)
    px(24, 16, GDW)

    # ── Corpus (figura de Cristo, simplificada) ───────────────────────────────
    # Cabeza (aureola dorada + cabeza)
    px(23, 11, GDM); px(24, 11, GDH); px(25, 11, GDM)  # aureola
    px(22, 12, GDK); px(25, 12, GDK)
    px(23, 12, IVL); px(24, 12, IVL)   # cara
    px(23, 13, IVD); px(24, 13, IVD)
    # Torso (extendido sobre los brazos)
    for x in range(18, 30):
        if 15 <= x <= 21 or 26 <= x <= 29:
            px(x, 18, IVM); px(x, 19, IVD)   # brazos
    px(23, 18, IVL); px(24, 18, IVL)           # torso
    px(23, 19, IVL); px(24, 19, IVL)
    px(23, 20, IVD); px(24, 20, IVD)
    px(23, 21, IVL); px(24, 21, IVL)
    px(23, 22, IVD); px(24, 22, IVD)

    return img


# =============================================================================
# 09  INCENSARIO
# =============================================================================
def mk_incensario():
    img, dr, p, px, hl, vl, rc = cv()

    # ── Humo (volutas) ────────────────────────────────────────────────────────
    # Voluta izquierda
    for xi, yi in [(22,3),(21,4),(20,5),(20,6),(21,7),(22,8)]:
        px(xi, yi, SMH2); px(xi-1, yi, SMH2)
    # Voluta central
    for y in range(3, 14): px(24, y, SMK if y % 2 == 0 else SML2)
    # Voluta derecha
    for xi, yi in [(25,4),(26,5),(27,6),(27,7),(26,8),(25,9)]:
        px(xi, yi, SMH2); px(xi+1, yi, SMH2)

    # ── Anillas y cadenas ─────────────────────────────────────────────────────
    # Tres cadenas que convergen desde arriba
    for y in range(14, 22):
        f = (y - 14) / 8
        lx = int(14 - f * 4); rx = int(34 + f * 4)
        cx = 24
        px(lx, y, IH); px(lx+1, y, IM)   # cadena izq
        px(cx, y, IH); px(cx+1, y, IM)    # cadena centro
        px(rx, y, IM); px(rx+1, y, IH)    # cadena der
    # Anilla superior
    dr.ellipse([21, 13, 28, 17], outline=GDD, fill=None, width=2)
    px(24, 13, GDL); px(25, 13, GDL)

    # ── Cuerpo del incensario (esfera perforada) ─────────────────────────────
    dr.ellipse([13, 22, 35, 38], fill=GDM)
    dr.ellipse([14, 23, 34, 37], fill=GDL)
    dr.ellipse([16, 25, 32, 35], fill=GDD)
    # Tapa superior
    dr.ellipse([16, 20, 32, 26], fill=GDM)
    dr.ellipse([17, 21, 31, 25], fill=GDL)
    for x in range(16, 33): px(x, 20, GDH)
    # Perforaciones (hoyos decorativos)
    for px2, py2 in [(18,27),(22,26),(27,27),(31,28),(18,32),(22,33),(27,32),(30,31),(24,29)]:
        px(px2, py2, GDK)
    # Banda decorativa central
    for x in range(14, 35):
        if p[x, 30][3] > 100: px(x, 30, GDH)
    # Pie del incensario
    dr.ellipse([17, 36, 31, 42], fill=GDM)
    dr.ellipse([18, 37, 30, 41], fill=GDL)
    for x in range(17, 32): px(x, 36, GDH); px(x, 41, GDK)

    # Sombra
    dr.ellipse([14, 41, 34, 45], fill=(0, 0, 0, 35))

    return img


# =============================================================================
# 10  ÓRGANO DE TUBOS
# =============================================================================
def mk_organo():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(3, 45): px(x, 47, SHC)

    # ── Cuerpo principal de madera ────────────────────────────────────────────
    rc(4, 16, 43, 44, WDD)
    for x in range(4, 44): px(x, 16, WDH); px(x, 44, WDK)
    for y in range(16, 45): px(4, y, WDH); px(43, y, WDK)
    # Interior del cuerpo
    rc(5, 17, 42, 43, WDM)
    # Tallas decorativas (molduras)
    for x in range(5, 43): px(x, 18, WDL); px(x, 20, WDK)
    for x in range(5, 43): px(x, 38, WDK); px(x, 40, WDL)
    for y in range(17, 44): px(7, y, WDL); px(40, y, WDD)

    # ── Teclado (visible en la parte frontal) ─────────────────────────────────
    rc(8, 29, 39, 37, IVL)
    for x in range(8, 40): px(x, 29, IVM); px(x, 37, IVD)
    for y in range(29, 38): px(8, y, IVD); px(39, y, IVD)
    # Teclas blancas
    for x in range(9, 39, 3): vl(x, 30, 36, IVH)
    for x in range(10, 39, 3): vl(x, 30, 36, SMM)   # divisores
    # Teclas negras
    for x in range(11, 38, 3): rc(x, 30, x+1, 34, IDM)

    # ── Paneles laterales decorativos ─────────────────────────────────────────
    # Panel izq
    rc(6, 21, 9, 37, WDL)
    for y in range(21, 38): px(6, y, WDH)
    # Panel der
    rc(38, 21, 41, 37, WDL)
    for y in range(21, 38): px(41, y, WDK)
    # Cruz en panel izq
    vl(7, 23, 35, GDK); hl(29, 5, 9, GDK)
    # Cruz en panel der
    vl(39, 23, 35, GDK); hl(29, 38, 41, GDK)

    # ── Caja de los tubos (arriba) ────────────────────────────────────────────
    rc(3, 3, 44, 16, WDD)
    for x in range(3, 45): px(x, 3, WDH); px(x, 16, WDK)
    for y in range(3, 17): px(3, y, WDH); px(44, y, WDK)
    rc(4, 4, 43, 15, WDM)

    # ── Tubos dorados del órgano ──────────────────────────────────────────────
    # 9 tubos de diferentes alturas
    tube_data = [
        (6,  4, 14),   # muy alto
        (10, 6, 14),
        (14, 5, 14),
        (18, 4, 14),   # alto
        (22, 3, 14),   # el más alto (centro)
        (26, 4, 14),
        (30, 5, 14),
        (34, 6, 14),
        (38, 4, 14),
    ]
    for tx, ty_top, ty_bot in tube_data:
        # Cuerpo del tubo
        for y in range(ty_top, ty_bot + 1):
            px(tx,     y, GDK); px(tx + 1, y, GDD)
            px(tx + 2, y, GDL); px(tx + 3, y, GDM)
        # Boca del tubo (abertura)
        boca_y = (ty_top + ty_bot) // 2
        rc(tx, boca_y, tx + 3, boca_y + 1, IDM)
        # Tope del tubo
        for x in range(tx, tx + 4): px(x, ty_top, GDH)
        # Sombra inferior del tubo
        for x in range(tx, tx + 4): px(x, ty_bot, GDK)

    # ── Pie del órgano (escalones) ─────────────────────────────────────────
    rc(3, 44, 44, 46, SM)
    for x in range(3, 45): px(x, 44, SHH); px(x, 46, SD)

    return img


# =============================================================================
# 11  SAGRARIO (tabernáculo)
# =============================================================================
def mk_sagrario():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(12, 37): px(x, 47, SHC)

    # Pedestal de mármol
    rc(12, 39, 36, 44, MB)
    for x in range(12, 37): px(x, 39, MA); px(x, 44, MDK)
    for y in range(39, 45): px(12, y, IVL); px(36, y, MC)
    rc(10, 36, 38, 39, MA)
    for x in range(10, 39): px(x, 36, IVL)
    for y in range(36, 40): px(10, y, IVL); px(38, y, MC)

    # Cuerpo dorado
    rc(10, 13, 38, 36, GDD)
    rc(11, 14, 37, 35, GDM)
    for y in range(13, 36): px(10, y, GDK); px(38, y, GDK)
    rc( 9, 10, 39, 13, GDL)
    for x in range(9, 40): px(x, 10, GDH)
    rc(10,  8, 38, 10, GDH)
    for x in range(10, 39): px(x, 8, GDW)

    # Puerta con marco
    rc(15, 17, 33, 34, GDM)
    for x in range(15, 34): px(x, 17, GDL); px(x, 34, GDK)
    for y in range(17, 35): px(15, y, GDL); px(33, y, GDK)
    for x in range(16, 33): px(x, 18, GDH); px(x, 33, GDD)
    for y in range(18, 34): px(16, y, GDH); px(32, y, GDD)
    # Cruz en la puerta
    for y in range(20, 32): px(24, y, GDH); px(23, y, GDM); px(25, y, GDM)
    for x in range(18, 30): px(x, 25, GDH); px(x, 26, GDM)
    px(24, 25, GDW); px(24, 26, GDW)
    # Bisagras
    px(15, 21, GDK); px(15, 22, GDK)
    px(15, 29, GDK); px(15, 30, GDK)
    # Manija
    px(32, 25, GDW); px(32, 26, GDW)

    # Lampara del sagrario (luz perpetua)
    for y in range(4, 8): px(24, y, GDD)
    rc(22, 8, 26, 12, TDM)
    for x in range(22, 27): px(x, 8, TDL); px(x, 12, TDK)
    for y in range(8, 13): px(22, y, TDL); px(26, y, TDK)
    px(24, 5, FDH); px(24, 6, FDL); px(23, 7, FDM); px(24, 7, FDK)

    return img


# =============================================================================
# 12  CALIZ Y PATENA
# =============================================================================
def mk_caliz():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(10, 40): px(x, 47, SHC)

    # Patena (plato dorado a la derecha)
    rc(34, 36, 46, 38, GDM)
    for x in range(34, 47): px(x, 36, GDL); px(x, 38, GDK)
    rc(35, 33, 45, 36, GDL)
    for x in range(35, 46): px(x, 33, GDW)
    for y in range(33, 37): px(35, y, GDH); px(45, y, GDD)

    # Base del caliz
    rc(12, 41, 32, 44, GDD)
    for x in range(12, 33): px(x, 41, GDL); px(x, 44, GDK)
    for y in range(41, 45): px(12, y, GDL); px(32, y, GDK)
    rc(13, 38, 31, 41, GDM)
    for x in range(13, 32): px(x, 38, GDH)
    for y in range(38, 42): px(13, y, GDL); px(31, y, GDD)

    # Tallo
    for y in range(22, 38):
        px(20, y, GDL); px(21, y, GDH); px(22, y, GDM); px(23, y, GDD)

    # Nudo
    rc(18, 28, 26, 32, GDM)
    for x in range(18, 27): px(x, 28, GDL); px(x, 32, GDK)
    for y in range(28, 33): px(18, y, GDL); px(26, y, GDK)
    for x in range(18, 27): px(x, 29, GDH)

    # Copa
    rows = [
        (22,19,25),(21,18,26),(20,17,27),(19,16,28),
        (18,15,29),(17,14,30),(16,13,31),(15,12,32),
        (14,11,33),(13,11,33),(12,11,33),(11,11,33),
        (10,11,33),( 9,12,32),( 8,13,31),( 7,14,30),
        ( 6,15,29),( 5,16,28),
    ]
    for (y, xl, xr) in rows:
        for x in range(xl, xr+1):
            if   x == xl:   px(x, y, GDK)
            elif x == xl+1: px(x, y, GDL)
            elif x == xl+2: px(x, y, GDH)
            elif x == xr-1: px(x, y, GDD)
            elif x == xr:   px(x, y, GDK)
            else:           px(x, y, GDM)
    for x in range(15, 29): px(x, 5, GDW)
    for x in range(14, 30): px(x, 6, GDH)

    return img


# =============================================================================
# 13  CANDELABRO DE PIE
# =============================================================================
def mk_candelabro():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(10, 40): px(x, 47, SHC)

    # Patas
    for y in range(38, 46):
        t = (y - 38) / 7.0
        lx = int(22 - t * 9); rx = int(26 + t * 9)
        px(lx, y, GDK); px(lx+1, y, GDD); px(lx+2, y, GDM)
        px(rx-2, y, GDM); px(rx-1, y, GDD); px(rx, y, GDK)
        if y < 42:
            px(23, y, GDD); px(24, y, GDM)
    # Pies decorativos
    for dx in range(-1, 2):
        px(13+dx, 44, GDL); px(35+dx, 44, GDL); px(23+dx, 45, GDL)

    # Anillo unificador
    rc(17, 35, 31, 38, GDM)
    for x in range(17, 32): px(x, 35, GDL); px(x, 38, GDK)
    for y in range(35, 39): px(17, y, GDL); px(31, y, GDK)

    # Fuste
    for y in range(8, 35):
        px(20, y, GDL); px(21, y, GDH); px(22, y, GDM)
        px(23, y, GDM); px(24, y, GDD); px(25, y, GDK)

    # Nudo decorativo
    rc(18, 20, 26, 24, GDM)
    for x in range(18, 27): px(x, 20, GDL); px(x, 24, GDK)
    for y in range(20, 25): px(18, y, GDL); px(26, y, GDK)
    for x in range(18, 27): px(x, 21, GDH)

    # Platillo portavela
    rc(18, 5, 26, 8, GDM)
    for x in range(18, 27): px(x, 5, GDL); px(x, 8, GDK)
    for y in range(5, 9): px(18, y, GDL); px(26, y, GDK)

    draw_candle(px, 22, 1, height=6)

    return img


# =============================================================================
# 14  VIRGEN / ESTATUA
# =============================================================================
def mk_virgen():
    img, dr, p, px, hl, vl, rc = cv()

    SKN = (235, 195, 165, 255)
    SKD = (200, 155, 118, 255)
    BLU = ( 18,  52, 142, 255)
    BLM = ( 38,  88, 188, 255)
    BLL = ( 68, 135, 225, 255)
    WHT = (245, 243, 235, 255)
    WHS = (205, 202, 190, 255)
    CRN = (255, 218,  38, 255)
    HAL = (255, 238, 100, 180)

    for x in range(10, 38): px(x, 47, SHC)

    # Pedestal
    rc(10, 40, 38, 45, MB)
    for x in range(10, 39): px(x, 40, MA); px(x, 45, MDK)
    for y in range(40, 46): px(10, y, IVL); px(38, y, MC)
    rc( 9, 37, 39, 40, MA)
    for x in range(9, 40): px(x, 37, IVL)
    for y in range(37, 41): px(9, y, IVL); px(39, y, MC)

    # Halo
    for dx in range(-9, 10):
        for dy in range(-9, 10):
            d2 = dx*dx + dy*dy
            if 56 <= d2 <= 81:
                px(24+dx, 9+dy, HAL)

    # Corona de estrellas
    for i in range(12):
        a = math.radians(i*30 - 90)
        px(int(24 + 10.5*math.cos(a)), int(9 + 10.5*math.sin(a)), CRN)

    # Velo (fondo de cabeza)
    rc(18, 5, 30, 14, BLU)
    # Cara
    rc(20, 7, 28, 13, SKN)
    for x in range(20, 29): px(x, 7, BLM)
    px(22, 10, SKD); px(26, 10, SKD); px(24, 12, SKD)

    # Cuello
    for y in range(13, 16):
        for x in range(22, 27): px(x, y, SKN)

    # Tunica blanca
    rc(19, 15, 29, 37, WHT)
    for y in range(16, 37): px(19, y, WHS); px(29, y, WHS)
    for y in range(20, 36, 4): px(22, y, WHS); px(26, y, WHS)

    # Manto azul
    for y in range(15, 37):
        for x in range(12, 19): px(x, y, BLM if x > 14 else BLU)
        for x in range(29, 37): px(x, y, BLM if x < 34 else BLU)
    for y in range(18, 36, 4):
        px(13, y, BLL); px(35, y, BLL)
    for x in range(18, 30): px(x, 15, BLU)

    # Manos
    for y in range(24, 28):
        px(20, y, SKN); px(21, y, SKN)
        px(27, y, SKN); px(28, y, SKN)

    # Base tunica
    rc(13, 35, 35, 37, BLU)
    for x in range(13, 36): px(x, 35, BLM)

    return img


# =============================================================================
# 15  VITRAL (ventana gotica de colores)
# =============================================================================
def mk_vitral():
    img, dr, p, px, hl, vl, rc = cv()

    LEAD  = ( 18,  18,  22, 255)
    STONE = ( 95,  88,  80, 255)
    VB1   = ( 15,  55, 175, 235)
    VR1   = (188,  14,  14, 235)
    VY1   = (215, 182,  10, 235)
    VG1   = ( 12, 128,  28, 235)
    VP1   = ( 95,  14, 140, 235)
    VW1   = (240, 235, 215, 235)

    # Marco de piedra lateral y base
    for y in range(8, 48):
        for x in range(0, 3): px(x, y, STONE)
        for x in range(45, 48): px(x, y, STONE)
    rc(0, 44, 47, 47, STONE)

    # Arco apuntado (piedra)
    arch_cx = 24; arch_cy = 20; arch_r = 20
    for y in range(0, 20):
        hw = int(math.sqrt(max(0, arch_r**2 - (y-arch_cy)**2)))
        for x in range(0, max(0, arch_cx-hw-1)): px(x, y, STONE)
        for x in range(min(47, arch_cx+hw+2), 48): px(x, y, STONE)
        # Marco (2px)
        px(max(0,arch_cx-hw), y, STONE); px(max(0,arch_cx-hw+1), y, SM)
        px(min(47,arch_cx+hw), y, STONE); px(min(47,arch_cx+hw-1), y, SM)

    # Lineas de plomo
    for x in range(2, 46): px(x, 20, LEAD)
    for x in range(2, 46): px(x, 33, LEAD)
    for y in range(0, 44): px(24, y, LEAD)
    for y in range(20, 44): px(14, y, LEAD); px(34, y, LEAD)
    for x in range(2, 14): px(x, 27, LEAD)
    for x in range(34, 46): px(x, 27, LEAD)

    # Rosen superior (arco)
    for y in range(1, 20):
        hw = int(math.sqrt(max(0, arch_r**2 - (y-arch_cy)**2))) - 2
        xl = max(2, arch_cx-hw); xr = min(45, arch_cx+hw)
        for x in range(xl, xr+1):
            if x == 24: continue
            dist = math.sqrt((x-24)**2 + (y-10)**2)
            if   dist < 4: px(x, y, VW1)
            elif dist < 7: px(x, y, VY1)
            elif x < 24:   px(x, y, VB1)
            else:          px(x, y, VR1)

    # Paneles medios
    for y in range(21, 33):
        for x in range(2,  14): px(x, y, VB1 if y < 27 else VG1)
        for x in range(15, 24): px(x, y, VR1 if y < 27 else VP1)
        for x in range(25, 34): px(x, y, VY1 if y < 27 else VR1)
        for x in range(35, 46): px(x, y, VG1 if y < 27 else VB1)

    # Paneles inferiores
    for y in range(34, 44):
        for x in range(2,  14): px(x, y, VR1)
        for x in range(15, 24): px(x, y, VB1)
        for x in range(25, 34): px(x, y, VG1)
        for x in range(35, 46): px(x, y, VY1)

    # Highlights de vidrio
    for y in range(1, 44):
        for x in range(2, 46):
            c = img.getpixel((x, y))
            if c[3] > 50 and c not in (STONE, LEAD, SM):
                if (x+y) % 9 == 0:
                    px(x, y, (min(255,c[0]+45), min(255,c[1]+45), min(255,c[2]+45), c[3]))

    return img


# =============================================================================
# 16  CAMPANILLAS DE ALTAR
# =============================================================================
def mk_campanillas():
    img, dr, p, px, hl, vl, rc = cv()

    BEL  = (215, 180,  35, 255)
    BED  = (145, 110,  15, 255)
    BEL2 = (255, 228,  90, 255)
    HDL  = ( 88,  45,  12, 255)
    HDL2 = (125,  68,  22, 255)
    CLP  = (188, 150,  25, 255)
    RIB  = (165,  12,  12, 255)

    for x in range(6, 42): px(x, 47, SHC)

    # Mango de madera
    for y in range(28, 41):
        px(22, y, HDL); px(23, y, HDL2); px(24, y, HDL2); px(25, y, HDL)
    rc(21, 38, 26, 41, HDL)
    for x in range(21, 27): px(x, 38, HDL2)

    # Cinta roja
    for x in range(21, 27): px(x, 31, RIB); px(x, 32, RIB)

    # Varilla horizontal
    for x in range(8, 40):
        px(x, 20, BED if x%3==0 else BEL)
        px(x, 21, BED)

    # Union varilla-mango
    rc(20, 21, 27, 28, BED)
    for x in range(20, 28): px(x, 21, BEL)
    for y in range(21, 29): px(20, y, BEL); px(27, y, BED)

    # Campana izquierda
    bell_l = [(27,8,14),(26,7,15),(25,7,15),(24,6,16),(23,6,16),(22,7,15),(21,8,14)]
    for y, xl, xr in bell_l:
        for x in range(xl, xr+1):
            if x==xl or x==xr: px(x,y,BED)
            elif x==xl+1: px(x,y,BEL2)
            else: px(x,y,BEL)
    px(10, 20, BED); px(11, 20, BEL)  # argolla
    px(10, 24, CLP); px(11, 24, CLP)  # badajo

    # Campana central (mas grande)
    bell_c = [(27,18,28),(26,17,29),(25,16,30),(24,16,30),(23,15,31),(22,15,31),
              (21,16,30),(20,17,29),(19,18,28)]
    for y, xl, xr in bell_c:
        for x in range(xl, xr+1):
            if x==xl or x==xr: px(x,y,BED)
            elif x==xl+1: px(x,y,BEL2)
            else: px(x,y,BEL)
    px(23, 20, BED); px(24, 20, BEL)
    px(23, 25, CLP); px(24, 25, CLP); px(23, 26, CLP)

    # Campana derecha
    bell_r = [(27,33,39),(26,32,40),(25,32,40),(24,31,41),(23,31,41),(22,32,40),(21,33,39)]
    for y, xl, xr in bell_r:
        for x in range(xl, xr+1):
            if x==xl or x==xr: px(x,y,BED)
            elif x==xl+1: px(x,y,BEL2)
            else: px(x,y,BEL)
    px(36, 20, BED); px(37, 20, BEL)
    px(36, 24, CLP); px(37, 24, CLP)

    return img


# =============================================================================
# 17  CIRIO PASCUAL
# =============================================================================
def mk_cirio_pascual():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(10, 38): px(x, 47, SHC)

    # Tripie dorado
    for y in range(38, 46):
        t = (y-38)/8.0
        lx = int(22 - t*9); rx = int(26 + t*9)
        px(lx, y, GDK); px(lx+1, y, GDD); px(lx+2, y, GDM)
        px(rx-2, y, GDM); px(rx-1, y, GDD); px(rx, y, GDK)
    for dx in range(-1, 2):
        px(13+dx, 45, GDL); px(35+dx, 45, GDL)

    # Anillo
    rc(17, 35, 31, 38, GDM)
    for x in range(17, 32): px(x, 35, GDL); px(x, 38, GDK)
    for y in range(35, 39): px(17, y, GDL); px(31, y, GDK)

    # Fuste
    for y in range(28, 35):
        px(21, y, GDL); px(22, y, GDH); px(23, y, GDM)
        px(24, y, GDM); px(25, y, GDD); px(26, y, GDK)

    # Platillo
    rc(17, 25, 31, 28, GDD)
    for x in range(17, 32): px(x, 25, GDL); px(x, 28, GDK)
    for y in range(25, 29): px(17, y, GDL); px(31, y, GDK)

    # Cuerpo del cirio (blanco grande)
    for y in range(5, 25):
        px(19, y, IVD); px(20, y, IVL); px(21, y, IVL)
        px(22, y, IVL); px(23, y, IVL); px(24, y, IVM)
        px(25, y, IVD); px(26, y, WAD); px(27, y, WDK)
    for x in range(19, 28): px(x, 5, IVL)

    # Cruz roja decorativa
    for y in range(9, 22): px(22, y, TDM); px(23, y, TDL)
    for x in range(20, 27): px(x, 14, TDM); px(x, 15, TDL)
    # 5 granos de incienso (puntos dorados)
    px(23, 10, GDH); px(23, 13, GDH); px(23, 17, GDH)
    px(21, 13, GDH); px(25, 13, GDH)
    # Alpha / Omega
    px(21, 8, TDH); px(24, 8, TDH)
    px(21, 22, TDH); px(24, 22, TDH)

    # Llama
    px(23, 3, WDK)
    px(23, 1, FDH); px(22, 2, FDL); px(23, 2, FDL); px(24, 2, FDL)
    px(22, 3, FDM); px(23, 3, FDM); px(24, 3, FDK)
    px(23, 4, FDK)

    return img


# =============================================================================
# 18  CREDENCIA (mesa de servicio liturgico)
# =============================================================================
def mk_credencia():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(5, 44): px(x, 47, SHC)

    # Patas
    for y in range(37, 46):
        px(7, y, WDK); px(8, y, WDD); px(9, y, WDM)
        px(38, y, WDL); px(39, y, WDD); px(40, y, WDK)
    for x in range(8, 40): px(x, 42, WDK); px(x, 43, WDD)

    # Mantel blanco
    rc(5, 24, 42, 37, IVL)
    for x in range(5, 43): px(x, 24, IVL); px(x, 37, IVD)
    for y in range(24, 38): px(5, y, IVL); px(42, y, IVD)
    for y in range(26, 37, 4): px(10, y, IVD); px(20, y, IVD); px(30, y, IVD); px(40, y, IVD)
    # Borde dorado
    for x in range(5, 43): px(x, 25, GDD); px(x, 36, GDD)

    # Tablero superior (perspectiva 3/4)
    rc(4, 19, 43, 24, MA)
    for x in range(4, 44): px(x, 19, IVL); px(x, 24, MB)
    for y in range(19, 25): px(4, y, IVL); px(43, y, MC)

    # --- Objetos sobre la mesa ---

    # Jarra de agua (izquierda)
    rc(8, 11, 15, 19, IVL)
    for x in range(8, 16): px(x, 11, IVL); px(x, 19, IVM)
    for y in range(11, 20): px(8, y, IVL); px(15, y, IVD)
    # Asa
    px(16, 12, IVD); px(16, 13, IVD); px(16, 14, IVD); px(16, 15, IVD)
    px(15, 11, IVD); px(15, 16, IVD)
    # Tapa
    rc(7, 9, 16, 11, IVL)
    for x in range(7, 17): px(x, 9, IVL)
    # Agua
    for y in range(13, 17): px(10, y, WAL); px(11, y, WAM); px(12, y, WAL)

    # Purificador/toalla (centro)
    rc(19, 12, 30, 19, IVL)
    for x in range(19, 31): px(x, 12, IVL); px(x, 19, IVD)
    for y in range(12, 20): px(19, y, IVL); px(30, y, IVD)
    # Cruz bordada
    for y in range(13, 18): px(24, y, GDD)
    for x in range(21, 28): px(x, 15, GDD)

    # Platillo (derecha)
    rc(33, 13, 41, 16, MB)
    for x in range(33, 42): px(x, 13, MA); px(x, 16, MDK)
    for y in range(13, 17): px(33, y, MA); px(41, y, MC)
    rc(34, 14, 40, 15, GDM)
    for x in range(34, 41): px(x, 14, GDL)

    return img


# =============================================================================
# 19  AMBON (lugar de proclamacion)
# =============================================================================
def mk_ambon():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(4, 44): px(x, 47, SHC)

    # Escalon lateral
    rc(4, 40, 14, 45, SM)
    for x in range(4, 15): px(x, 40, SHH); px(x, 45, SD)
    for y in range(40, 46): px(4, y, SHH); px(14, y, SD)

    # Base
    rc(9, 34, 42, 40, WDM)
    for x in range(9, 43): px(x, 34, WDH); px(x, 40, WDK)
    for y in range(34, 41): px(9, y, WDH); px(42, y, WDK)

    # Panel frontal
    rc(11, 16, 40, 34, WDD)
    rc(12, 17, 39, 33, WDM)
    for x in range(11, 41): px(x, 16, WDH); px(x, 34, WDK)
    for y in range(16, 35): px(11, y, WDH); px(40, y, WDK)

    # Relieve central tallado
    rc(15, 19, 36, 31, WDD)
    for x in range(15, 37): px(x, 19, WDM); px(x, 31, WDK)
    for y in range(19, 32): px(15, y, WDM); px(36, y, WDK)
    # Cruz tallada
    for y in range(21, 30): px(26, y, WDH); px(25, y, WDL)
    for x in range(17, 34): px(x, 25, WDH); px(x, 24, WDL)
    px(26, 25, WDH); px(25, 24, WDH)

    # Superficie inclinada (atril superior)
    rc(10, 9, 41, 16, WDL)
    for x in range(10, 42): px(x, 9, WDH); px(x, 16, WDM)
    for y in range(9, 17): px(10, y, WDH); px(41, y, WDD)

    # Libro abierto
    rc(12, 10, 25, 15, IVL)
    for x in range(12, 26): px(x, 10, IVL); px(x, 15, IVD)
    for y in range(10, 16): px(12, y, IVL); px(25, y, IVD)
    rc(25, 10, 39, 15, IVL)
    for x in range(25, 40): px(x, 10, IVL); px(x, 15, IVD)
    for y in range(10, 16): px(25, y, IVL); px(39, y, IVD)
    # Texto
    for y in range(11, 15):
        for x in range(13, 25, 3): px(x, y, IVD)
        for x in range(26, 38, 3): px(x, y, IVD)
    # Lomo
    for y in range(10, 16): px(25, y, WDM)
    # Inicial iluminada
    rc(13, 11, 16, 13, GDM)
    for x in range(13, 17): px(x, 11, GDL)

    # Microfono
    for y in range(3, 8): px(36, y, IM); px(37, y, IL)
    rc(34, 1, 39, 4, IM)
    for x in range(34, 40): px(x, 1, IL)
    for y in range(1, 5): px(34, y, IL); px(39, y, ID)
    rc(35, 8, 38, 10, ID)
    for y in range(1, 4):
        for x in range(35, 39, 2): px(x, y, ID)

    return img


# =============================================================================
# 20  RETABLO (altarpiece)
# =============================================================================
def mk_retablo():
    img, dr, p, px, hl, vl, rc = cv()

    # Fondo de madera oscura
    rc(0, 0, 47, 47, WDK)
    rc(1, 1, 46, 46, WDD)

    # Marco exterior dorado
    for x in range(2, 46): px(x, 2, GDH); px(x, 46, GDK)
    for y in range(2, 47): px(2, y, GDL); px(46, y, GDK)
    for x in range(3, 45):
        px(x, 3, GDM); px(x, 4, GDH); px(x, 5, GDM)
        px(x, 43, GDD); px(x, 44, GDM); px(x, 45, GDK)
    for y in range(3, 46):
        px(3, y, GDL); px(4, y, GDH); px(5, y, GDM)
        px(43, y, GDD); px(44, y, GDM); px(45, y, GDK)
    px(4,4,GDW); px(44,4,GDH); px(4,44,GDH); px(44,44,GDD)

    # Columna izquierda
    rc(6, 6, 13, 42, GDD)
    for y in range(6, 43): px(6, y, GDL); px(7, y, GDH); px(12, y, GDD); px(13, y, GDK)
    for y in range(8, 42, 3): px(9, y, GDK); px(10, y, GDM)
    # Columna derecha
    rc(34, 6, 41, 42, GDD)
    for y in range(6, 43): px(34, y, GDL); px(35, y, GDH); px(40, y, GDD); px(41, y, GDK)
    for y in range(8, 42, 3): px(37, y, GDK); px(38, y, GDM)
    # Capiteles
    rc(5, 6, 14, 9, GDL)
    for x in range(5, 15): px(x, 6, GDW); px(x, 9, GDD)
    rc(33, 6, 42, 9, GDL)
    for x in range(33, 43): px(x, 6, GDW); px(x, 9, GDD)

    # Nicho central
    rc(14, 6, 33, 42, WDK)
    rc(15, 7, 32, 41, (22, 10, 4, 255))

    # Arco de medio punto sobre el nicho
    for dy in range(-8, 1):
        hw = int(math.sqrt(max(0, 64 - dy*dy)))
        xl = max(14, 24-hw-1); xr = min(33, 24+hw+1)
        for x in range(xl, xr+1): px(x, 14+dy, GDM)

    # Figura central (silueta de Cristo)
    rc(19, 18, 29, 38, IVM)
    for x in range(19, 30): px(x, 18, IVL); px(x, 38, IVD)
    for y in range(18, 39): px(19, y, IVL); px(29, y, IVD)
    # Manto rojo
    for y in range(20, 38):
        px(17, y, TDM); px(18, y, TDL)
        px(30, y, TDL); px(31, y, TDM)
    # Halo dorado
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            if 12 <= dx*dx+dy*dy <= 20:
                px(24+dx, 13+dy, GDL)
    # Cara
    rc(21, 11, 27, 17, (215, 175, 140, 255))
    # Mano de bendicion
    for yy in range(23, 26): px(30, yy, (215,175,140,255)); px(31, yy, (215,175,140,255))

    # Remate triangular (fronton dorado)
    for dy in range(3, 7):
        hw = (7-dy)
        for x in range(24-hw, 24+hw+1): px(x, dy, GDH if dy==4 else GDM)
    px(24, 3, GDW)

    # Velas flanqueando el retablo
    draw_candle(px, 10, 36, height=6)
    draw_candle(px, 38, 36, height=6)

    return img


# ── Generar todos los items ───────────────────────────────────────────────────
ITEMS = [
    ('banca_iglesia',  mk_banca_iglesia ),
    ('altar_mayor',    mk_altar_mayor   ),
    ('veladora',       mk_veladora      ),
    ('atril',          mk_atril         ),
    ('pila_agua',      mk_pila_agua     ),
    ('reclinatorio',   mk_reclinatorio  ),
    ('confesionario',  mk_confesionario ),
    ('cruz_altar',     mk_cruz_altar    ),
    ('incensario',     mk_incensario    ),
    ('organo',         mk_organo        ),
    ('sagrario',       mk_sagrario      ),
    ('caliz',          mk_caliz         ),
    ('candelabro',     mk_candelabro    ),
    ('virgen',         mk_virgen        ),
    ('vitral',         mk_vitral        ),
    ('campanillas',    mk_campanillas   ),
    ('cirio_pascual',  mk_cirio_pascual ),
    ('credencia',      mk_credencia     ),
    ('ambon',          mk_ambon         ),
    ('retablo',        mk_retablo       ),
]

for nombre, fn in ITEMS:
    img  = fn()
    local = os.path.join(OUT_DIR,  f'{nombre}.png')
    copia = os.path.join(PNGS_DIR, f'{nombre}.png')
    img.save(local)
    shutil.copy2(local, copia)
    print(f'OK  {nombre}.png')

print(f'\n{len(ITEMS)} muebles de iglesia -> MUEBLES/ y PNGS/')
