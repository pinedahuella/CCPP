"""
generador.py  –  Muebles de parque  48x48 px  (perspectiva RPG 3/4)
Genera los PNGs en la misma carpeta y copia a PNGS/.

Itemes:
  01 banca_parque   - banca de madera con respaldo
  02 fuente_parque  - fuente circular de piedra con agua
  03 farol_parque   - farol de hierro forjado con glow
  04 mesa_parque    - mesa de picnic con dos bancas
  05 basurero       - papelera cilindrica verde
  06 macetero       - macetero de piedra con flores
  07 cartel_parque  - letrero informativo de madera
  08 estatua        - busto sobre pedestal de marmol
  09 bebedero       - bebedero de metal con cano
  10 arco_flores    - arco de madera con enredaderas y rosas
"""

from PIL import Image, ImageDraw
import os, shutil

OUT_DIR  = r'C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISENOS\MUEBLES'
PNGS_DIR = r'C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISENOS\PNGS'

# Deteccion automatica de la ruta real (manejo de la e con tilde en Windows)
import pathlib
_base = pathlib.Path(__file__).parent
OUT_DIR  = str(_base)
PNGS_DIR = str(_base.parent / 'PNGS')
os.makedirs(OUT_DIR,  exist_ok=True)
os.makedirs(PNGS_DIR, exist_ok=True)

S = 48  # tamano sprite

# -- Paleta global ------------------------------------------------------------
T   = (  0,   0,   0,   0)
BO  = ( 38,  16,   4, 255)   # borde madera
BOM = ( 15,  15,  18, 255)   # borde metal/hierro
# Madera
WD  = ( 92,  48,  12, 255);  WM  = (140,  86,  26, 255)
WL  = (185, 130,  55, 255);  WH  = (220, 175,  92, 255)
WBR = ( 65,  32,   5, 255)   # madera muy oscura (tornillos)
# Piedra
SD  = ( 88,  82,  76, 255);  SM  = (128, 122, 115, 255)
SL  = (172, 166, 158, 255);  SHH = (212, 207, 199, 255)
# Marmol
MA  = (230, 225, 218, 255);  MB  = (210, 205, 196, 255)
MC  = (185, 180, 170, 255);  MDK = (150, 144, 135, 255)
# Metal / hierro forjado
ID  = ( 35,  35,  40, 255);  IM  = ( 60,  60,  68, 255)
IL  = ( 92,  92, 102, 255);  IH  = (138, 138, 152, 255)
# Agua
WAD = ( 28,  88, 175, 255);  WAM = ( 55, 138, 215, 255)
WAL = (115, 185, 252, 255);  WAH = (198, 228, 255, 255)
# Verde plantas
GD  = ( 28,  78,  22, 255);  GM  = ( 52, 118,  38, 255)
GL  = ( 82, 162,  58, 255);  GH  = (128, 208,  96, 255)
# Flores
RM  = (228,  68,  48, 255)
YL  = (252, 218,  48, 255);  YD  = (195, 148,   0, 255)
PL  = (178,  98, 218, 255)
PKD = (195,  45, 100, 255);  PKL = (248, 140, 175, 255)
WW  = (240, 240, 248, 255)
# Glow
GLW = (255, 240, 120, 200)
# Sombra
SHC = (  0,   0,   0,  45)
# Tierra
SOD = ( 62,  36,  10, 255);  SOM = ( 90,  56,  20, 255)


# -- Canvas helper ------------------------------------------------------------
def cv():
    img = Image.new('RGBA', (S, S), T)
    p   = img.load()
    dr  = ImageDraw.Draw(img)

    def px(x, y, c):
        if 0 <= x < S and 0 <= y < S:
            p[x, y] = c

    def hl(y, x1, x2, c):
        for x in range(x1, x2 + 1): px(x, y, c)

    def vl(x, y1, y2, c):
        for y in range(y1, y2 + 1): px(x, y, c)

    def rc(x1, y1, x2, y2, c):
        for yy in range(y1, y2 + 1):
            for xx in range(x1, x2 + 1): px(xx, yy, c)

    return img, dr, p, px, hl, vl, rc


# -----------------------------------------------------------------------------
# 01  BANCA DE PARQUE
# -----------------------------------------------------------------------------
def mk_banca_parque():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(9, 40): px(x, 43, SHC)

    # Patas traseras
    for y in range(25, 34):
        px(10,y,BO); px(11,y,WD); px(36,y,WD); px(37,y,BO)

    # Patas delanteras
    for y in range(33, 42):
        for xi, ci in [(9,BO),(10,WD),(11,WM),(12,WL)]: px(xi, y, ci)
        for xi, ci in [(35,WL),(36,WM),(37,WD),(38,BO)]: px(xi, y, ci)

    # Travesano
    for x in range(10, 38):
        px(x,38,BO); px(x,39,WD); px(x,40,WM); px(x,41,BO)

    # Asiento  3 tablones
    hl(24, 8, 39, BO)
    for x in range(8, 40): px(x,25, WH if x%7==2 else WL); px(x,26, WM)
    hl(27, 8, 39, BO)
    for x in range(8, 40): px(x,28, WH if x%7==2 else WL); px(x,29, WM)
    hl(30, 8, 39, BO)
    for x in range(8, 40): px(x,31, WH if x%7==2 else WL); px(x,32, WM)
    hl(33, 8, 39, BO)
    for x in range(8, 40): px(x,34, BO)
    for y in range(24, 35): px(8,y,BO); px(9,y,WD); px(38,y,WD); px(39,y,BO)

    # Apoyabrazos
    for y in range(18, 35): px(7,y,BO); px(8,y,WD); px(39,y,WD); px(40,y,BO)
    for x in range(7, 13):  px(x,17,BO); px(x,18,WM); px(x,19,WL); px(x,20,WH)
    for x in range(36, 41): px(x,17,BO); px(x,18,WM); px(x,19,WL); px(x,20,WH)

    # Respaldo - barra superior
    for x in range(8, 40):
        px(x,12,BO); px(x,13,WD); px(x,14,WM); px(x,15,WL); px(x,16,WH)

    # Respaldo - barra inferior
    for x in range(8, 40): px(x,22,WL); px(x,23,WM); px(x,24,WD)

    # Tres tablones verticales del respaldo
    for y in range(14, 24):
        for xi,ci in [( 9,BO),(10,WD),(11,WM),(12,WL),(13,WH),(14,WL),(15,WM),(16,WD),(17,BO)]: px(xi,y,ci)
        for xi,ci in [(19,BO),(20,WD),(21,WM),(22,WL),(23,WH),(24,WL),(25,WM),(26,WD),(27,BO)]: px(xi,y,ci)
        for xi,ci in [(30,BO),(31,WD),(32,WM),(33,WL),(34,WH),(35,WL),(36,WM),(37,WD),(38,BO)]: px(xi,y,ci)

    for y in range(12, 25): px(8,y,BO); px(39,y,BO)

    # Tornillos
    for tx, ty in [(10,14),(16,14),(10,22),(16,22),(20,14),(26,14),(20,22),(26,22),(31,14),(37,14),(31,22),(37,22)]:
        px(tx, ty, WBR)

    return img


# -----------------------------------------------------------------------------
# 02  FUENTE DE PARQUE
# -----------------------------------------------------------------------------
def mk_fuente_parque():
    img, dr, p, px, hl, vl, rc = cv()

    # Sombra
    dr.ellipse([10, 42, 38, 47], fill=(0, 0, 0, 35))

    # Cuenco exterior de piedra (eje Y comprimido = perspectiva 3/4)
    dr.ellipse([ 4, 27, 44, 43], fill=SM)
    dr.ellipse([ 5, 27, 43, 42], fill=SM)
    # Borde superior del cuenco (highlight)
    for x in range(5, 44):
        if 0 <= x < S and p[x, 27][3] > 100: px(x, 27, SHH)
    # Borde inferior (sombra)
    for x in range(5, 44):
        if 0 <= x < S and p[x, 42][3] > 100: px(x, 42, SD)
    for y in range(27, 43):
        if p[4, y][3]  > 100: px(4,  y, SD)
        if p[43,y][3]  > 100: px(43, y, SD)

    # Agua dentro del cuenco
    dr.ellipse([ 7, 29, 41, 41], fill=WAM)
    # Ripples
    dr.ellipse([10, 31, 22, 37], fill=WAL)
    dr.ellipse([25, 32, 39, 38], fill=WAH)
    dr.ellipse([15, 33, 32, 37], fill=WAL)

    # Columna central de piedra
    for y in range(11, 34):
        for xi, ci in [(21,SD),(22,SM),(23,SL),(24,SHH),(25,SL),(26,SM),(27,SD)]:
            px(xi, y, ci)

    # Cuenco superior (pequeno)
    dr.ellipse([16,  9, 32, 17], fill=SM)
    dr.ellipse([17,  9, 31, 16], fill=SL)
    dr.ellipse([18, 10, 30, 15], fill=SHH)
    dr.ellipse([19, 11, 29, 14], fill=WAL)
    for x in range(16, 33):
        if p[x,  9][3] > 100: px(x,  9, SD)
        if p[x, 17][3] > 100: px(x, 17, SD)

    # Chorros de agua arqueados
    for i in range(7):
        px(21 - i, 11 + i, WAL); px(20 - i, 10 + i, WAH)
    for i in range(7):
        px(27 + i, 11 + i, WAL); px(28 + i, 10 + i, WAH)
    # Gotas cayendo
    for dx, dy in [(-9,2),(-6,4),(-3,5),(3,5),(6,4),(9,2),(0,3),(-12,1),(12,1)]:
        px(24+dx, 28+dy, WAL); px(24+dx, 29+dy, WAM)

    return img


# -----------------------------------------------------------------------------
# 03  FAROL DE PARQUE
# -----------------------------------------------------------------------------
def mk_farol_parque():
    img, dr, p, px, hl, vl, rc = cv()

    # Sombra
    dr.ellipse([17, 43, 31, 47], fill=(0, 0, 0, 45))

    # Base de piedra
    dr.polygon([(13,44),(35,44),(33,39),(15,39)], fill=SM)
    for x in range(13, 36): px(x, 39, SHH); px(x, 44, SD)
    for y in range(39, 45): px(13,y,SD); px(35,y,SD)

    # Poste de hierro (5 px)
    for y in range(14, 40):
        px(22,y,BOM); px(23,y,IM); px(24,y,IL); px(25,y,IM); px(26,y,BOM)

    # Volutas decorativas
    for xi, yi in [(20,35),(19,34),(18,33),(18,32),(19,31),(20,30),(21,29)]:
        px(xi, yi, IM); px(xi-1, yi, BOM)
    for xi, yi in [(28,35),(29,34),(30,33),(30,32),(29,31),(28,30),(27,29)]:
        px(xi, yi, IM); px(xi+1, yi, BOM)

    # Cuerpo de la linterna
    rc(15, 12, 33, 27, IM)
    for x in range(15, 34): px(x,12,BOM); px(x,27,BOM)
    for y in range(12, 28): px(15,y,BOM); px(33,y,BOM)

    # Cristales con luz calida
    rc(16, 13, 23, 26, (255, 235,  88, 215))
    rc(25, 13, 32, 26, (255, 235,  88, 215))
    # Divisor central
    for y in range(12, 28): px(24, y, BOM)
    # Puntos brillantes
    px(20, 19, (255, 255, 200, 255)); px(28, 19, (255, 255, 200, 255))

    # Tejado de la linterna
    dr.polygon([(13,12),(35,12),(31, 7),(17, 7)], fill=IM)
    for x in range(13, 36): px(x,12,BOM)
    for x in range(17, 32): px(x, 7,BOM)
    # Punta del tejado
    for xi in [23,24,25]: px(xi, 4, BOM); px(xi, 5, BOM)
    px(24, 4, IH); px(23, 5, IM); px(25, 5, IM)

    # Halo de luz alrededor de la linterna
    for xi, yi in [(14,11),(14,28),(34,11),(34,28),(13,14),(13,25),(35,14),(35,25)]:
        px(xi, yi, (255, 240, 100, 80))

    return img


# -----------------------------------------------------------------------------
# 04  MESA DE PICNIC
# -----------------------------------------------------------------------------
def mk_mesa_parque():
    img, dr, p, px, hl, vl, rc = cv()

    # Sombra
    dr.ellipse([3, 43, 44, 47], fill=(0, 0, 0, 28))

    # ── Patas traseras de la mesa (se ven detrás del tablero) ──
    # Estan en los EXTREMOS del tablero: izq x=10-11, der x=36-37
    for y in range(19, 25):
        px(10,y,BO); px(11,y,WD)
        px(36,y,WD); px(37,y,BO)

    # ── Patas delanteras de la mesa (extremo izq y extremo der) ──
    for y in range(22, 40):
        px( 9,y,BO); px(10,y,WD); px(11,y,WM); px(12,y,WL)
        px(35,y,WL); px(36,y,WM); px(37,y,WD); px(38,y,BO)

    # ── Travesano central entre patas de la mesa ──
    for x in range(11, 37):
        px(x,34,BO); px(x,35,WD); px(x,36,WM); px(x,37,BO)

    # ── Patas de la banca izquierda ──
    for y in range(31, 40):
        px(3,y,BO); px(4,y,WD); px(5,y,WM)

    # ── Patas de la banca derecha ──
    for y in range(31, 40):
        px(42,y,WM); px(43,y,WD); px(44,y,BO)

    # ── Banca izquierda  2 tablones ──
    hl(24, 1, 10, BO)
    for x in range(1, 11): px(x,25, WH if x%4==2 else WL); px(x,26,WM)
    hl(27, 1, 10, BO)
    for x in range(1, 11): px(x,28, WH if x%4==2 else WL); px(x,29,WM)
    hl(30, 1, 10, BO)
    # cara frontal banca izq
    for x in range(1, 11): px(x,30,WD); px(x,31,BO)
    for y in range(24, 31): px(1,y,BO); px(2,y,WD); px(9,y,WD); px(10,y,BO)

    # ── Banca derecha  2 tablones ──
    hl(24, 37, 46, BO)
    for x in range(37, 47): px(x,25, WH if x%4==2 else WL); px(x,26,WM)
    hl(27, 37, 46, BO)
    for x in range(37, 47): px(x,28, WH if x%4==2 else WL); px(x,29,WM)
    hl(30, 37, 46, BO)
    # cara frontal banca der
    for x in range(37, 47): px(x,30,WD); px(x,31,BO)
    for y in range(24, 31): px(37,y,BO); px(38,y,WD); px(45,y,WD); px(46,y,BO)

    # ── Tablero de la mesa  3 tablones ──
    hl(11, 8, 39, BO)
    for x in range(8, 40): px(x,12, WH if x%6==1 else WL); px(x,13,WM)
    hl(14, 8, 39, BO)
    for x in range(8, 40): px(x,15, WH if x%6==1 else WL); px(x,16,WM)
    hl(17, 8, 39, BO)
    for x in range(8, 40): px(x,18, WH if x%6==1 else WL); px(x,19,WM)
    hl(20, 8, 39, BO)
    # cara frontal tablero
    for x in range(8, 40): px(x,20,WD); px(x,21,BO)
    # laterales tablero
    for y in range(11, 21): px(8,y,BO); px(9,y,WD); px(38,y,WD); px(39,y,BO)

    return img


# -----------------------------------------------------------------------------
# 05  BASURERO / PAPELERA
# -----------------------------------------------------------------------------
def mk_basurero():
    img, dr, p, px, hl, vl, rc = cv()

    BD  = ( 20,  65,  20, 255)
    BM  = ( 38,  98,  36, 255)
    BL  = ( 60, 138,  55, 255)
    BH  = ( 98, 178,  90, 255)
    LID = ( 15,  52,  15, 255)
    LIM = ( 32,  85,  30, 255)

    dr.ellipse([11, 43, 37, 47], fill=(0, 0, 0, 40))

    # Fondo del cilindro
    dr.ellipse([11, 39, 37, 46], fill=BD)

    # Cuerpo vertical
    for y in range(17, 43):
        for x in range(11, 38): px(x, y, BM)
        px(11,y,BD); px(12,y,BH)
        px(36,y,BL); px(37,y,BD)

    # Lineas de relieve verticales
    for x in range(16, 37, 7):
        for y in range(18, 43): px(x, y, BD)

    # Highlight vertical
    for y in range(18, 42): px(13, y, BH); px(14, y, BL)

    # Tapa
    dr.ellipse([ 9,  9, 39, 20], fill=LID)
    dr.ellipse([10, 10, 38, 19], fill=LIM)
    dr.ellipse([12, 11, 36, 18], fill=LIM)
    dr.ellipse([14, 12, 34, 17], fill=(44, 100, 40, 255))
    dr.ellipse([15, 12, 26, 15], fill=(52, 115, 48, 255))

    # Borde tapa-cuerpo
    for x in range(10, 39):
        if 0 <= x < S:
            if p[x, 19][3] > 100: px(x, 19, BD)
            if p[x, 20][3] > 100: px(x, 20, BD)
    dr.ellipse([10, 15, 38, 22], outline=BD, fill=None)

    # Manija de la tapa
    dr.rounded_rectangle([19, 5, 29, 11], radius=2, fill=LID, outline=BD)
    dr.rounded_rectangle([20, 6, 28, 10], radius=2, fill=LIM)

    # Asa lateral
    dr.arc([6, 22, 13, 32], start=90, end=270, fill=BL, width=2)

    return img


# -----------------------------------------------------------------------------
# 06  MACETERO CON FLORES
# -----------------------------------------------------------------------------
def mk_macetero():
    img, dr, p, px, hl, vl, rc = cv()

    dr.ellipse([ 7, 43, 41, 47], fill=(0, 0, 0, 35))

    # Cuerpo de la maceta (forma trapezoidal)
    dr.polygon([(8,43),(40,43),(38,28),(10,28)], fill=SM)
    # Gradiente de iluminacion en el cuerpo
    for y in range(29, 43):
        t = (y - 29) / 14.0
        rv = int(SHH[0] * (1-t) + SD[0] * t)
        gv = int(SHH[1] * (1-t) + SD[1] * t)
        bv = int(SHH[2] * (1-t) + SD[2] * t)
        for x in range(9, 40):
            if p[x, y][3] > 100: px(x, y, (rv, gv, bv, 255))
    # Bordes
    for y in range(28, 44):
        if p[8,y][3]  > 100: px(8,  y, SD)
        if p[40,y][3] > 100: px(40, y, SD)
    hl(43, 8, 40, SD)

    # Rim superior de la maceta
    dr.ellipse([ 7, 23, 41, 32], fill=SL)
    dr.ellipse([ 8, 24, 40, 31], fill=SHH)
    dr.ellipse([ 9, 24, 39, 30], fill=SHH)
    for x in range(7, 42):
        if 0 <= x < S:
            if p[x, 23][3] > 100: px(x, 23, SD)
            if p[x, 31][3] > 100: px(x, 31, SD)

    # Tierra dentro
    dr.ellipse([10, 24, 38, 31], fill=SOD)
    dr.ellipse([12, 25, 36, 30], fill=SOM)

    # 3 plantas con flores distintas
    plants = [
        (17, 22, (RM,  YL,  RM )),
        (24, 19, (YL,  WW,  YD )),
        (31, 21, (PKL, PKD, PKL)),
    ]
    for sx, fy, (fc1, fc2, fc3) in plants:
        for y in range(fy + 6, 26): px(sx, y, GD); px(sx+1, y, GM)
        px(sx-1, fy+8, GL); px(sx-2, fy+7, GL)
        px(sx+2, fy+8, GL); px(sx+3, fy+7, GL)
        for dx, dy, fc in [
            ( 0, 0,fc2),( 1, 0,fc2),
            (-1, 1,fc1),( 0, 1,fc1),( 1, 1,fc1),( 2, 1,fc1),
            (-1, 2,fc1),( 0, 2,fc2),( 1, 2,fc2),( 2, 2,fc1),
            (-1, 3,fc1),( 0, 3,fc1),( 1, 3,fc1),( 2, 3,fc1),
            ( 0, 4,fc2),( 1, 4,fc2),
        ]:
            px(sx + dx, fy + dy, fc)
        px(sx,   fy+2, YL); px(sx+1, fy+2, YL)

    return img


# -----------------------------------------------------------------------------
# 07  CARTEL INFORMATIVO DE PARQUE
# -----------------------------------------------------------------------------
def mk_cartel_parque():
    img, dr, p, px, hl, vl, rc = cv()

    dr.ellipse([10, 43, 38, 47], fill=(0, 0, 0, 35))

    # Dos postes de madera
    for y in range(29, 44):
        px(14,y,BO); px(15,y,WD); px(16,y,WM); px(17,y,WL)
        px(30,y,WL); px(31,y,WM); px(32,y,WD); px(33,y,BO)
    # Puntas biseladas
    for xi,ci in [(14,BO),(15,WM),(16,WL),(17,WH)]: px(xi,27,ci); px(xi,28,WM)
    for xi,ci in [(30,WH),(31,WL),(32,WM),(33,BO)]: px(xi,27,ci); px(xi,28,WM)

    # Tablero del cartel
    rc( 8, 11, 40, 28, WL)
    for x in range(8, 41): px(x, 11, BO); px(x, 28, BO)
    for y in range(11, 29): px(8,y,BO); px(40,y,BO)
    rc( 9, 12, 39, 27, WH)
    for x in range(10, 39): px(x, 13, WM); px(x, 26, WM)
    for y in range(13, 27): px(10,y,WM); px(38,y,WM)

    # Simbolo central: arbol de parque
    dr.ellipse([16, 14, 32, 23], fill=GM)
    dr.ellipse([18, 15, 30, 22], fill=GL)
    dr.ellipse([20, 15, 27, 21], fill=GH)
    for x in range(16, 33):
        if 0 <= x < S and p[x, 14][3] > 100: px(x, 14, GD)
    for y in range(21, 27): px(22,y,WD); px(23,y,WM); px(24,y,WM); px(25,y,WD)

    # Tornillos en esquinas
    for tx, ty in [(10,13),(38,13),(10,26),(38,26)]: px(tx, ty, WBR)

    return img


# -----------------------------------------------------------------------------
# 08  ESTATUA EN PEDESTAL DE MARMOL
# -----------------------------------------------------------------------------
def mk_estatua():
    img, dr, p, px, hl, vl, rc = cv()

    dr.ellipse([12, 43, 36, 47], fill=(0, 0, 0, 42))

    # Pedestal base (escalon inferior)
    dr.polygon([(10,44),(38,44),(36,40),(12,40)], fill=SM)
    rc(10, 40, 38, 44, SM)
    for x in range(10, 39): px(x, 40, SHH); px(x, 44, SD)
    for y in range(40, 45): px(10,y,SD); px(38,y,SD)

    # Cuerpo del pedestal
    rc(13, 34, 35, 41, SL)
    for x in range(13, 36): px(x, 34, SHH); px(x, 41, SD)
    for y in range(34, 42): px(13,y,SHH); px(35,y,SD)
    for x in range(13, 36): px(x, 36, SHH); px(x, 39, SD)

    # Plataforma de la figura
    dr.polygon([(11,34),(37,34),(35,30),(13,30)], fill=SL)
    for x in range(11, 38): px(x, 30, SHH); px(x, 34, SD)

    # Figura / tunica
    for y in range(15, 31):
        w = max(4, 7 - max(0, (y - 22)) // 2)
        for x in range(24 - w, 24 + w + 1):
            px(x, y, MA if y < 22 else MB)
        px(24 - w, y, MC); px(24 + w, y, MDK)

    # Cabeza / busto
    dr.ellipse([18,  7, 30, 17], fill=MA)
    dr.ellipse([19,  8, 29, 16], fill=MA)
    dr.ellipse([21, 10, 28, 15], fill=MB)
    px(21, 11, MC); px(26, 11, MC)    # ojos
    px(23, 13, MC); px(24, 13, MC)    # nariz
    dr.ellipse([20,  8, 24, 11], fill=(238, 234, 228, 180))
    for y in range(15, 18): px(22,y,MA); px(23,y,MB); px(24,y,MB); px(25,y,MA)

    return img


# -----------------------------------------------------------------------------
# 09  BEBEDERO DE METAL
# -----------------------------------------------------------------------------
def mk_bebedero():
    img, dr, p, px, hl, vl, rc = cv()

    dr.ellipse([16, 43, 32, 47], fill=(0, 0, 0, 42))

    # Base (pie ancho)
    dr.ellipse([14, 41, 34, 47], fill=IM)
    rc(14, 42, 34, 45, IM)
    for x in range(14, 35): px(x, 41, IH); px(x, 45, ID)
    for y in range(41, 46): px(14,y,IH); px(34,y,ID)

    # Poste central
    for y in range(22, 43):
        px(20,y,ID); px(21,y,IM); px(22,y,IL); px(23,y,IH)
        px(24,y,IH); px(25,y,IL); px(26,y,IM); px(27,y,ID)

    # Ensanchamiento hacia el tazon
    for y in range(18, 23):
        for x in range(18, 30): px(x, y, IM)
        px(18,y,IH); px(19,y,IH); px(28,y,ID); px(29,y,ID)

    # Tazon del bebedero
    dr.ellipse([13, 13, 35, 23], fill=IL)
    dr.ellipse([14, 14, 34, 22], fill=IH)
    dr.ellipse([16, 15, 32, 21], fill=WAM)
    dr.ellipse([18, 16, 30, 20], fill=WAL)
    for x in range(13, 36):
        if 0 <= x < S:
            if p[x, 13][3] > 100: px(x, 13, ID)
            if p[x, 22][3] > 100: px(x, 22, ID)

    # Cano (spout) curvo
    for y in range(9, 16): px(25,y,ID); px(26,y,IM); px(27,y,IL)
    px(28, 8, IM); px(29, 7, IM); px(30, 7, ID)
    px(28, 9, ID); px(29, 8, ID)
    # Gota de agua
    px(30, 9, WAL); px(31,10, WAM); px(30,10, WAL); px(31,11, WAD)

    # Palanca (handle izquierda)
    dr.ellipse([10, 14, 18, 20], fill=IM)
    dr.ellipse([11, 15, 17, 19], fill=IL)
    for x in range(10, 20): px(x, 16, ID); px(x, 17, IH); px(x, 18, ID)

    return img


# -----------------------------------------------------------------------------
# 10  ARCO DE FLORES
# -----------------------------------------------------------------------------
def mk_arco_flores():
    img, dr, p, px, hl, vl, rc = cv()

    for x in range(5, 43): px(x, 47, SHC)

    # Poste izquierdo
    for y in range(22, 45):
        px( 5,y,BO); px( 6,y,WD); px( 7,y,WM); px( 8,y,WL); px( 9,y,WD); px(10,y,BO)

    # Poste derecho
    for y in range(22, 45):
        px(37,y,BO); px(38,y,WD); px(39,y,WM); px(40,y,WL); px(41,y,WD); px(42,y,BO)

    # Arco de madera (4 pasadas = grosor)
    arco_colores = [BO, WD, WM, WL]
    for i, col in enumerate(arco_colores):
        dr.arc(
            [5 + i, 4 + i, 43 - i, 38 - i],
            start=180, end=360,
            fill=col,
            width=2
        )
    # Highlight del arco
    dr.arc([11, 10, 37, 32], start=200, end=340, fill=WH, width=1)

    # Enredaderas distribuidas sobre el arco
    vine_pts = [
        (10,21),(11,17),(13,13),(15, 9),(18, 6),(21, 4),(24, 3),
        (27, 4),(30, 6),(33, 9),(35,13),(37,17),(38,21),
    ]
    for vx, vy in vine_pts:
        px(vx,   vy,   GD); px(vx+1, vy,   GM)
        px(vx,   vy+1, GM); px(vx+1, vy+1, GL)
        px(vx-1, vy+1, GD); px(vx+2, vy+1, GD)
        px(vx,   vy+2, GD)

    # Flores sobre el arco (8 flores de colores variados)
    flowers = [
        (10, 19, RM,  YL ),
        (15,  7, PKL, PKD),
        (21,  2, WW,  YL ),
        (27,  2, RM,  YL ),
        (33,  7, PKL, PKD),
        (38, 19, YL,  YD ),
        (18,  4, WW,  PKL),
        (30,  4, YL,  WW ),
    ]
    for fx, fy, fc, fcc in flowers:
        px(fx,   fy,   fcc); px(fx+1, fy,   fcc)
        px(fx-1, fy+1, fc ); px(fx,   fy+1, fc ); px(fx+1, fy+1, fc ); px(fx+2, fy+1, fc )
        px(fx,   fy+2, YL ); px(fx+1, fy+2, YL )   # centro amarillo
        px(fx-1, fy+3, fc ); px(fx,   fy+3, fc ); px(fx+1, fy+3, fc ); px(fx+2, fy+3, fc )
        px(fx,   fy+4, fcc); px(fx+1, fy+4, fcc)

    # Hojas en los postes
    for y in range(26, 43, 5):
        px( 9, y, GL); px(10, y, GH); px(11, y, GL)
        px(37, y, GL); px(38, y, GH); px(39, y, GL)

    return img


# -- Generar todos los items --------------------------------------------------
ITEMS = [
    ('banca_parque',  mk_banca_parque ),
    ('fuente_parque', mk_fuente_parque),
    ('farol_parque',  mk_farol_parque ),
    ('mesa_parque',   mk_mesa_parque  ),
    ('basurero',      mk_basurero     ),
    ('macetero',      mk_macetero     ),
    ('cartel_parque', mk_cartel_parque),
    ('estatua',       mk_estatua      ),
    ('bebedero',      mk_bebedero     ),
    ('arco_flores',   mk_arco_flores  ),
]

for nombre, fn in ITEMS:
    img = fn()
    local = os.path.join(OUT_DIR,  f'{nombre}.png')
    copia = os.path.join(PNGS_DIR, f'{nombre}.png')
    img.save(local)
    shutil.copy2(local, copia)
    print(f'OK  {nombre}.png')

print(f'\n{len(ITEMS)} muebles de parque  ->  MUEBLES/  y  PNGS/')
