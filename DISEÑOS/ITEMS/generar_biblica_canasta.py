import sys, math, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════
W, H     = 48, 32
N_FRAMES = 8

BASE    = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS"
OUT_DIR = os.path.join(BASE, "ITEMS", "BICICLETA_CANASTA")
os.makedirs(OUT_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# PALETA
# ══════════════════════════════════════════════════════════════════════════════
T    = (  0,   0,   0,   0)   # transparente

# Rueda
TIRE = ( 22,  22,  26, 255)
TIRH = ( 68,  68,  76, 255)
RIM  = (155, 160, 168, 255)
SPK  = (210, 215, 222, 255)
SPKD = (140, 145, 152, 255)
HUB  = (230, 234, 240, 255)
HUBD = (170, 175, 182, 255)

# Cuadro rojo
FRM  = (210,  30,  30, 255)
FRD  = (138,  10,  10, 255)
FRL  = (246, 102,  90, 255)
FORK = (182,  24,  24, 255)

# Sillín
SED  = ( 88,  52,  16, 255)
SEDL = (150,  98,  44, 255)
SEDC = ( 60,  35,  10, 255)

# Manillar
HBR  = ( 34,  34,  42, 255)
HBRL = ( 88,  90, 100, 255)

# Pedalier
CHNC = ( 80,  65,  18, 255)

# ── Canasta de madera ─────────────────────────────────────────────────────────
BK_D = ( 90,  52,  12, 255)   # madera oscura  (bordes, ribs verticales)
BK_M = (155,  98,  34, 255)   # madera media   (cuerpo / latas horizontales)
BK_L = (210, 155,  70, 255)   # madera clara   (brillo horizontal)
BK_H = (235, 190, 110, 255)   # brillo superior (rim de la canasta)
BK_S = ( 55,  30,   6, 255)   # sombra muy oscura (borde inferior / sombra)
HND  = (125,  78,  22, 255)   # asa de la canasta (handle)
HNDD = ( 75,  44,  10, 255)   # asa oscura (sombra del asa)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def put(img, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), c)

def line(img, x0, y0, x1, y1, c):
    dx = abs(x1-x0); dy = abs(y1-y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        put(img, x0, y0, c)
        if x0 == x1 and y0 == y1: break
        e2 = 2*err
        if e2 > -dy: err -= dy; x0 += sx
        if e2 < dx:  err += dx; y0 += sy

# ══════════════════════════════════════════════════════════════════════════════
# RUEDA ANIMADA
# ══════════════════════════════════════════════════════════════════════════════
def draw_wheel(img, cx, cy, angle):
    R = 7
    for dy in range(-R, R+1):
        for dx in range(-R, R+1):
            d = math.sqrt(dx*dx + dy*dy)
            x, y = cx+dx, cy+dy
            if d > R: continue
            if d >= R - 0.6:
                ang_px = math.atan2(dy, dx)
                put(img, x, y, TIRH if (-1.1 < ang_px < 0.1) else TIRE)
            elif d >= R - 2.0:
                put(img, x, y, TIRE)
            elif d >= R - 3.0:
                put(img, x, y, RIM)
            elif d <= 1.5:
                put(img, x, y, HUBD if d > 0.8 else HUB)

    for i in range(4):
        a = angle + i * (math.pi / 2)
        cos_a, sin_a = math.cos(a), math.sin(a)
        for step in range(18):
            t  = step / 17.0
            r  = 1.8 + t * 2.8
            ix = int(round(cx + r * cos_a))
            iy = int(round(cy + r * sin_a))
            put(img, ix, iy, SPK if t > 0.4 else SPKD)

# ══════════════════════════════════════════════════════════════════════════════
# CUADRO DE LA BICICLETA
# ══════════════════════════════════════════════════════════════════════════════
def draw_frame(img):
    RWX, RWY = 10, 23
    FWX, FWY = 37, 23
    BBX, BBY = 23, 23
    STX, STY = 19, 12
    HTX, HTY = 35, 12
    HBX, HBY = 35, 20

    # Chain stay
    line(img, RWX, RWY,   BBX, BBY,   FRD)
    line(img, RWX, RWY-1, BBX, BBY-1, FRM)

    # Seat stay
    line(img, RWX,   RWY, STX,   STY, FRD)
    line(img, RWX+1, RWY, STX+1, STY, FRM)

    # Seat tube
    line(img, BBX,   BBY, STX,   STY, FRD)
    line(img, BBX-1, BBY, STX-1, STY, FRM)
    line(img, BBX-2, BBY, STX-2, STY, FRL)

    # Top tube
    line(img, STX, STY,   HTX, HTY,   FRM)
    line(img, STX, STY+1, HTX, HTY+1, FRD)
    for x_ in range(STX, HTX+1):
        put(img, x_, STY-1, FRL)

    # Down tube
    line(img, HTX,   HTY, BBX,   BBY, FRD)
    line(img, HTX-1, HTY, BBX-1, BBY, FRM)
    line(img, HTX-2, HTY, BBX-2, BBY, FRL)

    # Head tube
    line(img, HTX,   HTY, HBX,   HBY, FRM)
    line(img, HTX-1, HTY, HBX-1, HBY, FRL)

    # Horquilla
    line(img, HBX,   HBY, FWX,   FWY, FORK)
    line(img, HBX-1, HBY, FWX-1, FWY, FRM)

    # Pedalier
    for ox in [-1, 0, 1]:
        put(img, BBX+ox, BBY, CHNC)
    put(img, BBX, BBY-1, CHNC)

    # Sillín
    put(img, STX, STY-1, FRM)
    line(img, 15, STY-2, 21, STY-2, SEDC)
    for x_ in range(14, 23): put(img, x_, STY-3, SED)
    for x_ in range(15, 22): put(img, x_, STY-4, SEDL)
    put(img, 14, STY-3, SEDC)
    put(img, 22, STY-3, SEDC)
    put(img, 15, STY-5, SEDL)
    put(img, 16, STY-5, SED)

    # Manillar (más corto, la canasta va delante)
    put(img, HTX,   HTY-1, HBR)
    put(img, HTX,   HTY-2, HBR)
    put(img, HTX-1, HTY-2, HBR)
    # Barra horizontal (solo extremo izq — el der queda detrás de la canasta)
    for x_ in range(32, 37):
        put(img, x_, HTY-2, HBR)
    for x_ in range(33, 36):
        put(img, x_, HTY-3, HBRL)
    # Grip izquierdo
    for y_ in [HTY-2, HTY-1]:
        put(img, 32, y_, HBR)
    put(img, 32, HTY, HBR)
    put(img, 33, HTY-1, HBRL)

# ══════════════════════════════════════════════════════════════════════════════
# CANASTA DE MADERA
#   Montada en el manillar delantero, 12×8 px con asa de 6px
#   Posición: x=31..42, y=4..11  (asa en y=2..4)
# ══════════════════════════════════════════════════════════════════════════════
def draw_basket(img):
    # ── Geometría de la canasta ───────────────────────────────────────────────
    BX1, BX2 = 31, 42   # borde izquierdo / derecho
    BY1, BY2 = 5, 12    # borde superior / inferior

    # — Soporte que une manillar con canasta (pequeño poste) —
    put(img, 36, 10, HBR)
    put(img, 36, 11, HBR)
    put(img, 37, 10, HBR)

    # — Fondo de la canasta (sombra inferior) —
    for x_ in range(BX1, BX2+1):
        put(img, x_, BY2, BK_S)

    # — Cuerpo de la canasta: fila por fila con patrón de mimbre —
    #   Cada 2 filas alterna entre listón claro y rib oscura
    for y_ in range(BY1+1, BY2):
        for x_ in range(BX1+1, BX2):
            # Ribs verticales cada 2px
            is_rib = ((x_ - BX1) % 3 == 0)
            # Filas alternas (simulan el entrelazado del mimbre)
            is_dark_row = ((y_ - BY1) % 2 == 1)

            if is_rib:
                put(img, x_, y_, BK_D)          # rib vertical siempre oscuro
            elif is_dark_row:
                # Fila "debajo" del rib → madera media
                put(img, x_, y_, BK_M)
            else:
                # Fila "encima" del rib → madera clara (listón horizontal)
                put(img, x_, y_, BK_L)

    # — Borde izquierdo y derecho (oscuros) —
    for y_ in range(BY1, BY2+1):
        put(img, BX1, y_, BK_D)
        put(img, BX2, y_, BK_D)

    # — Rim superior (borde de la canasta, más brillante) —
    for x_ in range(BX1, BX2+1):
        put(img, x_, BY1, BK_H)
    # Sombra interna bajo el rim
    for x_ in range(BX1+1, BX2):
        put(img, x_, BY1+1, BK_D)

    # — Esquinas redondeadas (quitar las 4 esquinas extremas) —
    put(img, BX1,  BY1, BK_S)   # esquina sup-izq más oscura
    put(img, BX2,  BY1, BK_S)   # esquina sup-der más oscura

    # — Asa de la canasta (arco de madera sobre la canasta) —
    #   Arco: x=34..39, toca en y=BY1 en los extremos y baja a y=2 al centro
    asa = [
        (34, BY1-1, HNDD),
        (35, BY1-2, HND),
        (36, BY1-3, HND),
        (37, BY1-3, BK_H),   # brillo en el centro del asa
        (38, BY1-2, HND),
        (39, BY1-1, HNDD),
    ]
    for (ax, ay, ac) in asa:
        put(img, ax, ay, ac)
    # Sombra debajo del asa
    for ax in [35, 36, 37, 38]:
        put(img, ax, BY1, BK_D)

    # — Pequeños detalles: sombra lateral izquierda —
    for y_ in range(BY1+1, BY2):
        put(img, BX1+1, y_, BK_D)

# ══════════════════════════════════════════════════════════════════════════════
# GENERAR LOS 8 FRAMES
# ══════════════════════════════════════════════════════════════════════════════
for f in range(N_FRAMES):
    angle = (2 * math.pi * f) / N_FRAMES

    img = Image.new("RGBA", (W, H), T)

    draw_frame(img)                   # cuadro (atrás)
    draw_basket(img)                  # canasta (sobre el manillar)
    draw_wheel(img, 10, 23, angle)    # rueda trasera
    draw_wheel(img, 37, 23, angle)    # rueda delantera

    fname = f"FRAME{f+1}.png"
    img.save(os.path.join(OUT_DIR, fname))
    print(f"  [OK] {fname}")

print(f"\n=== BICICLETA CON CANASTA lista — {N_FRAMES} frames 48×32 en: {OUT_DIR} ===")
