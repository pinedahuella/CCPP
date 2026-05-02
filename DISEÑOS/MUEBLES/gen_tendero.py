"""
gen_tendero.py  -  Tendero de ropa  48x48 px  (ANIMACION MEJORADA)
12 frames de ciclo completo con movimiento organico:

  * Oscilacion sinusoidal suave (no steps cuadrados)
  * Efecto billow: la parte MEDIA de cada prenda se abomba
    hacia adelante como bandera — seno de arco encima del pendulo
  * Cada prenda tiene amplitud y fase distintas:
      camisa   amp=2.5 px  fase=0
      pantalon amp=2.0 px  fase=+18 grados (mas pesado, algo retrasado)
      toalla   amp=3.2 px  fase=+30 grados (mas ligera, mas adelantada)
"""

from PIL import Image
import os, shutil, pathlib, math

_base    = pathlib.Path(__file__).parent
OUT_DIR  = str(_base)
PNGS_DIR = str(_base.parent / 'PNGS')
os.makedirs(OUT_DIR,  exist_ok=True)
os.makedirs(PNGS_DIR, exist_ok=True)

S = 48

# ── Paleta ────────────────────────────────────────────────────────────────────
T   = (  0,   0,   0,   0)
BO  = ( 38,  16,   4, 255)
WD  = ( 92,  48,  12, 255);  WM  = (140,  86,  26, 255)
WL  = (185, 130,  55, 255);  WH  = (220, 175,  92, 255)
SHC = (  0,   0,   0,  45)
# Cuerda
RC  = (152, 118,  72, 255);  RD  = (108,  78,  34, 255)
# Gancho de ropa
GK  = ( 75,  36,   5, 255);  GL2 = (108,  60,  12, 255)
# Camisa celeste
CL  = (218, 232, 252, 255);  CM  = (182, 202, 238, 255)
CD  = (145, 168, 218, 255);  CS  = (112, 138, 198, 255)
# Pantalon jean
PL  = ( 88, 118, 175, 255);  PM  = ( 58,  88, 148, 255)
PD  = ( 38,  60, 118, 255)
# Toalla
TR  = (212,  48,  38, 255);  TRD = (168,  28,  20, 255)
TW  = (245, 240, 228, 255);  TWD = (220, 214, 200, 255)

# ── Parametros de animacion ───────────────────────────────────────────────────
N_FRAMES = 12

AMP_C  = 2.5;  PH_C  = 0.0                    # camisa
AMP_P  = 2.0;  PH_P  = math.pi / 10           # pantalon  (~18 deg retardo)
AMP_T  = 3.2;  PH_T  = math.pi / 6            # toalla    (~30 deg adelanto)


def get_sw(amp, phase, frame):
    """Valor de swing (float px) para este frame."""
    return amp * math.sin(2 * math.pi * frame / N_FRAMES + phase)


# ── Helpers de dibujo ─────────────────────────────────────────────────────────
def canvas():
    img = Image.new('RGBA', (S, S), T)
    p   = img.load()
    def px(x, y, c):
        if 0 <= x < S and 0 <= y < S:
            p[x, y] = c
    return img, px


def ry(x):
    """Y de la cuerda: parabola suave, sag maximo ~2 px en el centro."""
    return 9 + int(round((x - 23) ** 2 / 115))


def boff(y, y0, h, sw):
    """
    Offset horizontal con billow.
    Pendulo lineal + arco de seno en la misma direccion:
      - tope  (t=0): offset = 0
      - medio (t=0.5): pendulo + ~38% de sw extra (abombado hacia fuera)
      - base  (t=1):   solo el pendulo = sw
    Resultado: la tela se curva como una bandera ondeando.
    """
    if h == 0:
        return 0
    t        = (y - y0) / h
    pendulum = sw * t
    billow   = sw * 0.38 * math.sin(math.pi * t)
    return int(round(pendulum + billow))


# ── Constructor del frame ─────────────────────────────────────────────────────
def mk_frame(sw_c, sw_p, sw_t):

    img, px = canvas()

    # Sombra en el suelo
    for x in range(3, 45):
        px(x, 46, SHC)
        px(x, 47, (0, 0, 0, 22))

    # ── Poste izquierdo ───────────────────────────────────────────────────────
    for y in range(9, 46):
        px(2,y,BO); px(3,y,WD); px(4,y,WM); px(5,y,WL); px(6,y,WD); px(7,y,BO)
    for xi, ci in [(3,WD),(4,WM),(5,WL),(6,WD)]: px(xi, 8, ci)
    for xi, ci in [(4,WL),(5,WH)]: px(xi, 7, ci); px(xi, 6, ci)
    px(4,5,WM); px(5,5,WL)
    for y in range(5, 9): px(2,y,BO); px(7,y,BO)

    # ── Poste derecho ─────────────────────────────────────────────────────────
    for y in range(9, 46):
        px(40,y,BO); px(41,y,WD); px(42,y,WM); px(43,y,WL); px(44,y,WD); px(45,y,BO)
    for xi, ci in [(41,WD),(42,WM),(43,WL),(44,WD)]: px(xi, 8, ci)
    for xi, ci in [(42,WL),(43,WH)]: px(xi, 7, ci); px(xi, 6, ci)
    px(42,5,WM); px(43,5,WL)
    for y in range(5, 9): px(40,y,BO); px(45,y,BO)

    # ── Cuerda ────────────────────────────────────────────────────────────────
    for x in range(7, 41):
        r = ry(x)
        px(x, r,     RC)
        px(x, r + 1, RD)

    # ── Ganchos de ropa (3) ───────────────────────────────────────────────────
    for pcx in (13, 24, 35):
        r = ry(pcx)
        # Cuerpo superior (3 filas, sujeta la cuerda)
        for dy in range(3):
            px(pcx-1, r+dy, GK); px(pcx, r+dy, GL2); px(pcx+1, r+dy, GK)
        # Hendidura central
        px(pcx-1, r+3, GK); px(pcx+1, r+3, GK)
        # Dos patas inferiores del gancho
        for dy in range(3, 6):
            px(pcx-2, r+dy, GK);  px(pcx-1, r+dy, GL2)
            px(pcx+1, r+dy, GL2); px(pcx+2, r+dy, GK)

    # =========================================================================
    # CAMISA CELESTE
    # =========================================================================
    cx1 = 13;  r1 = ry(cx1);  ya1 = r1 + 7;  h1 = 14

    def b1(y): return boff(y, ya1, h1, sw_c)

    # Cuello (1 fila)
    px(cx1-1+b1(ya1), ya1, CM)
    px(cx1  +b1(ya1), ya1, CL)
    px(cx1+1+b1(ya1), ya1, CM)

    # Hombros + mangas (3 filas) — ancho 9 px
    for y in range(ya1+1, ya1+4):
        b = b1(y)
        px(cx1-4+b, y, CS); px(cx1-3+b, y, CD); px(cx1-2+b, y, CM)
        px(cx1-1+b, y, CL); px(cx1  +b, y, CL); px(cx1+1+b, y, CL)
        px(cx1+2+b, y, CM); px(cx1+3+b, y, CD); px(cx1+4+b, y, CS)

    # Cuerpo — ancho 7 px, arrugas cada 4 filas
    for y in range(ya1+4, ya1+h1+1):
        b = b1(y)
        px(cx1-3+b, y, CS)
        px(cx1-2+b, y, CD)
        px(cx1-1+b, y, CM)
        px(cx1  +b, y, CM if (y - ya1) % 4 == 0 else CL)   # arruga central
        px(cx1+1+b, y, CM)
        px(cx1+2+b, y, CD)
        px(cx1+3+b, y, CS)

    # Dobladillo
    b = b1(ya1 + h1)
    for dx in range(-3, 4): px(cx1+dx+b, ya1+h1, CD)

    # =========================================================================
    # PANTALON JEAN
    # =========================================================================
    cx2 = 24;  r2 = ry(cx2);  ya2 = r2 + 7;  h2 = 18

    def b2(y): return boff(y, ya2, h2, sw_p)

    # Cinturilla (2 filas oscuras)
    for y in range(ya2, ya2+2):
        b = b2(y)
        for dx in range(-4, 5):
            c = PD if abs(dx)==4 else (PM if abs(dx)==3 else PL)
            px(cx2+dx+b, y, c)

    # Cuerpo: unido hasta ya2+5, luego dos piernas
    div_y = ya2 + 6
    for y in range(ya2+2, ya2+h2+1):
        b = b2(y)
        if y < div_y:
            for dx in range(-4, 5):
                c = PD if abs(dx)==4 else (PM if abs(dx)==3 else PL)
                px(cx2+dx+b, y, c)
            px(cx2+b, y, PM)   # costura central visible
        else:
            # Pierna izquierda dx=-4..-1
            for dx in range(-4, 0):
                c = PD if dx==-4 else (PM if dx==-3 else PL)
                px(cx2+dx+b, y, c)
            # Pierna derecha dx=1..4
            for dx in range(1, 5):
                c = PL if dx<=2 else (PM if dx==3 else PD)
                px(cx2+dx+b, y, c)

    # Dobladillos de piernas
    b = b2(ya2 + h2)
    for dx in range(-4, 0): px(cx2+dx+b, ya2+h2, PD)
    for dx in range( 1, 5): px(cx2+dx+b, ya2+h2, PD)

    # =========================================================================
    # TOALLA A RAYAS ROJAS Y CREMA
    # =========================================================================
    cx3 = 35;  r3 = ry(cx3);  ya3 = r3 + 7;  h3 = 13

    def b3(y): return boff(y, ya3, h3, sw_t)

    for y in range(ya3, ya3+h3+1):
        b  = b3(y)
        n  = (y - ya3) // 2
        cf = TR  if n % 2 == 0 else TW
        ce = TRD if n % 2 == 0 else TWD
        for dx in range(-4, 5):
            px(cx3+dx+b, y, ce if abs(dx)==4 else cf)

    # Orilla superior e inferior
    for dx in range(-4, 5):
        px(cx3+dx+b3(ya3),    ya3,    TRD)
        px(cx3+dx+b3(ya3+h3), ya3+h3, TRD)

    return img


# ── Generar los 12 frames ─────────────────────────────────────────────────────
print(f'Generando {N_FRAMES} frames...\n')
for i in range(N_FRAMES):
    sc = get_sw(AMP_C, PH_C, i)
    sp = get_sw(AMP_P, PH_P, i)
    st = get_sw(AMP_T, PH_T, i)

    img   = mk_frame(sc, sp, st)
    fname = f'f{i+1:02d}'
    local = os.path.join(OUT_DIR,  f'tendero_{fname}.png')
    copia = os.path.join(PNGS_DIR, f'tendero_{fname}.png')
    img.save(local)
    shutil.copy2(local, copia)
    print(f'  tendero_{fname}.png   cam={sc:+5.2f}  pan={sp:+5.2f}  toa={st:+5.2f}')

print(f'\nOK — {N_FRAMES} frames  ->  MUEBLES/  y  PNGS/')
