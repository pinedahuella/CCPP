import sys, math, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

# ══════════════════════════════════════════════════════════════════════════════
# BICICLETA VINTAGE / CRUISER — cuadro paso-through turquesa,
#                               guardabarros crema, manillar curvado,
#                               sillín ancho, rueda con más radios
# ══════════════════════════════════════════════════════════════════════════════
W, H     = 48, 32
N_FRAMES = 8

BASE    = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS"
OUT_DIR = os.path.join(BASE, "ITEMS", "BICICLETA_VINTAGE")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Paleta ────────────────────────────────────────────────────────────────────
T    = (  0,   0,   0,   0)

# Rueda (llanta dorada vintage)
TIRE  = ( 22,  22,  26, 255)
TIRH  = ( 62,  62,  70, 255)
RIM   = (185, 158,  55, 255)   # llanta dorada (vintage)
RIML  = (220, 198, 100, 255)   # llanta dorada clara
SPK   = (215, 185,  70, 255)   # radio dorado
SPKD  = (150, 120,  35, 255)
HUB   = (235, 210, 110, 255)
HUBD  = (170, 140,  50, 255)

# Cuadro turquesa
FRM  = ( 22, 160, 160, 255)   # turquesa medio
FRD  = (  8,  95,  95, 255)   # turquesa oscuro
FRL  = ( 80, 210, 210, 255)   # turquesa claro (brillo)
FORK = ( 18, 130, 130, 255)   # horquilla

# Guardabarros (crema / beige)
FND  = (210, 195, 148, 255)   # fender base crema
FNDL = (238, 226, 188, 255)   # fender claro
FNDD = (168, 148, 100, 255)   # fender oscuro (borde)

# Sillín ancho vintage (marrón cuero)
SED  = (128,  72,  20, 255)   # cuero oscuro
SEDL = (185, 118,  52, 255)   # cuero claro
SEDH = (225, 170,  90, 255)   # brillo cuero
SEDC = ( 80,  42,  10, 255)   # cuero borde

# Manillar curvado (cromo)
HBR  = (140, 145, 152, 255)   # cromo base
HBRL = (220, 225, 232, 255)   # cromo brillo
HBRD = ( 80,  85,  92, 255)   # cromo sombra

# Pedalier
CHNC = ( 78,  62,  16, 255)

# ── Helpers ───────────────────────────────────────────────────────────────────
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

# ── Rueda vintage: llanta dorada + 8 radios finos ────────────────────────────
def draw_wheel_vintage(img, cx, cy, angle):
    R = 7
    for dy in range(-R, R+1):
        for dx in range(-R, R+1):
            d = math.sqrt(dx*dx + dy*dy)
            x, y = cx+dx, cy+dy
            if d > R: continue
            if d >= R - 0.6:
                a_px = math.atan2(dy, dx)
                put(img, x, y, TIRH if (-1.1 < a_px < 0.1) else TIRE)
            elif d >= R - 2.0:
                put(img, x, y, TIRE)
            elif d >= R - 3.0:
                # Llanta dorada con brillo
                a_px = math.atan2(dy, dx)
                put(img, x, y, RIML if (-1.3 < a_px < 0.3) else RIM)
            elif d <= 1.5:
                put(img, x, y, HUBD if d > 0.8 else HUB)

    # 4 radios dorados finos intercalados (visualmente más ricos con llanta dorada)
    # Se usan 4 spokes en vez de 8 para que la rotación sea visible frame a frame
    for i in range(4):
        a = angle + i * (math.pi / 2)
        cos_a, sin_a = math.cos(a), math.sin(a)
        for step in range(18):
            t = step / 17.0
            r = 1.8 + t * 2.8
            put(img, int(round(cx + r*cos_a)), int(round(cy + r*sin_a)),
                SPK if t > 0.3 else SPKD)

# ── Guardabarros sobre una rueda ──────────────────────────────────────────────
def draw_fender(img, cx, cy):
    """Guardabarros: arco crema que cubre la parte superior de la rueda."""
    R_in  = 8    # radio interior del guardabarros (pegado al neumático)
    R_out = 9    # radio exterior

    for dy in range(-R_out, R_out+1):
        for dx in range(-R_out, R_out+1):
            d   = math.sqrt(dx*dx + dy*dy)
            x, y = cx+dx, cy+dy
            # Solo la mitad superior + un poco lateral (dy <= 2)
            if dy > 2: continue
            if R_in <= d <= R_out:
                # Brillo en el cuadrante superior
                put(img, x, y, FNDL if dy < -1 else FND)
    # Borde exterior del guardabarros (línea oscura)
    for dy in range(-R_out, 3):
        for dx in range(-R_out, R_out+1):
            d = math.sqrt(dx*dx + dy*dy)
            x, y = cx+dx, cy+dy
            if abs(d - R_out) < 0.7 and dy <= 2:
                put(img, x, y, FNDD)
    # Extremos del guardabarros (patitas de sujeción)
    # Izquierda
    lx = cx + int(round(-R_out * math.cos(math.radians(30))))
    ly = cy + int(round(R_out * math.sin(math.radians(30)))) - R_out + 1
    # Derecha
    rx = cx + int(round( R_out * math.cos(math.radians(30))))
    ry = ly
    for ox in [-1, 0]:
        put(img, cx + int(round(-8.2*math.cos(math.radians(20)))),
               cy + int(round( 8.2*math.sin(math.radians(20)))), FNDD)
        put(img, cx + int(round( 8.2*math.cos(math.radians(20)))),
               cy + int(round( 8.2*math.sin(math.radians(20)))), FNDD)

# ── Cuadro vintage paso-through ───────────────────────────────────────────────
def draw_frame_vintage(img):
    RWX, RWY = 10, 23
    FWX, FWY = 37, 23
    BBX, BBY = 23, 23
    STX, STY = 20, 13   # seatpost top
    HTX, HTY = 35, 12   # head tube top
    HBX, HBY = 35, 20   # head tube bottom

    # ── Chain stay ────────────────────────────────────────────────────────────
    line(img, RWX, RWY,   BBX, BBY,   FRD)
    line(img, RWX, RWY-1, BBX, BBY-1, FRM)

    # ── Seat stay ─────────────────────────────────────────────────────────────
    line(img, RWX,   RWY, STX,   STY, FRD)
    line(img, RWX+1, RWY, STX+1, STY, FRM)

    # ── Seat tube ─────────────────────────────────────────────────────────────
    line(img, BBX,   BBY, STX,   STY, FRD)
    line(img, BBX-1, BBY, STX-1, STY, FRM)
    line(img, BBX-2, BBY, STX-2, STY, FRL)

    # ── CUADRO PASO-THROUGH: tubo bajo curvo (reemplaza top tube recto) ───────
    #   Va desde STX,STY → curva descendiendo → HTX,HTY+2
    #   Simulamos la curva con 3 segmentos suaves
    curve_pts = [
        (STX,   STY),
        (24,    STY+1),
        (28,    STY+1),
        (32,    STY),
        (HTX,   HTY+2),
    ]
    for i in range(len(curve_pts)-1):
        x0,y0 = curve_pts[i]
        x1,y1 = curve_pts[i+1]
        line(img, x0,   y0,   x1,   y1,   FRM)
        line(img, x0,   y0+1, x1,   y1+1, FRD)
        for x_ in range(min(x0,x1), max(x0,x1)+1):
            t = (x_ - x0) / max(x1 - x0, 1)
            y_ = int(y0 + t*(y1-y0))
            put(img, x_, y_-1, FRL)   # brillo superior de tubo

    # ── Down tube (desde head tube top a BB) ─────────────────────────────────
    line(img, HTX,   HTY, BBX,   BBY, FRD)
    line(img, HTX-1, HTY, BBX-1, BBY, FRM)
    line(img, HTX-2, HTY, BBX-2, BBY, FRL)

    # ── Head tube ─────────────────────────────────────────────────────────────
    line(img, HTX,   HTY, HBX,   HBY, FRM)
    line(img, HTX-1, HTY, HBX-1, HBY, FRL)

    # ── Horquilla ─────────────────────────────────────────────────────────────
    line(img, HBX,   HBY, FWX,   FWY, FORK)
    line(img, HBX-1, HBY, FWX-1, FWY, FRM)

    # Pedalier
    for ox in [-1, 0, 1]:
        put(img, BBX+ox, BBY, CHNC)
    put(img, BBX, BBY-1, CHNC)

    # ── Sillín ancho de cuero ─────────────────────────────────────────────────
    put(img, STX, STY-1, FRM)
    # Riel
    line(img, 14, STY-2, 22, STY-2, SEDC)
    # Superficie ancha y ligeramente abombada
    for x_ in range(13, 24):  put(img, x_, STY-3, SED)
    for x_ in range(14, 23):  put(img, x_, STY-4, SEDL)
    for x_ in range(15, 22):  put(img, x_, STY-5, SEDL)
    for x_ in range(16, 21):  put(img, x_, STY-5, SEDH)   # brillo
    # Bordes redondeados
    put(img, 13, STY-3, SEDC)
    put(img, 23, STY-3, SEDC)
    put(img, 14, STY-4, SEDC)
    put(img, 22, STY-4, SEDC)
    put(img, 15, STY-6, SEDL)   # abultamiento central
    put(img, 16, STY-6, SEDH)
    put(img, 17, STY-6, SEDH)
    put(img, 18, STY-6, SEDL)

    # ── Manillar curvado (swept-back / cuerno de vaca) ────────────────────────
    # Stem cromo sube desde head tube
    put(img, HTX,   HTY-1, HBR)
    put(img, HTX,   HTY-2, HBRL)
    put(img, HTX-1, HTY-2, HBR)
    # Curva central del manillar
    for x_ in range(32, 39):
        put(img, x_, HTY-2, HBR)
    for x_ in range(33, 38):
        put(img, x_, HTY-3, HBRL)
    # Brazos curvados hacia atrás (swept back)
    # Brazo derecho: sube y vuelve hacia la derecha
    for x_ in range(38, 42):
        put(img, x_, HTY-2, HBR)
        put(img, x_, HTY-1, HBRD)
    put(img, 41, HTY-2, HBR)
    put(img, 42, HTY-1, HBR)
    # Brazo izquierdo: sube y vuelve hacia la izquierda
    for x_ in range(29, 33):
        put(img, x_, HTY-2, HBR)
        put(img, x_, HTY-1, HBRD)
    put(img, 29, HTY-2, HBR)
    put(img, 28, HTY-1, HBR)
    # Brillo cromo
    put(img, 42, HTY-2, HBRL)
    put(img, 28, HTY-2, HBRL)

# ── Generar frames ────────────────────────────────────────────────────────────
for f in range(N_FRAMES):
    angle = (2 * math.pi * f) / N_FRAMES
    img = Image.new("RGBA", (W, H), T)

    draw_frame_vintage(img)                 # cuadro (atrás)
    draw_fender(img, 10, 23)               # guardabarros trasero
    draw_fender(img, 37, 23)               # guardabarros delantero
    draw_wheel_vintage(img, 10, 23, angle) # rueda trasera
    draw_wheel_vintage(img, 37, 23, angle) # rueda delantera

    fname = f"FRAME{f+1}.png"
    img.save(os.path.join(OUT_DIR, fname))
    print(f"  [OK] {fname}")

print(f"\n=== VINTAGE lista — {N_FRAMES} frames 48×32 en: {OUT_DIR} ===")
