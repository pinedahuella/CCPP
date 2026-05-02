import sys, math, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

# ══════════════════════════════════════════════════════════════════════════════
# BICICLETA DE MONTAÑA — cuadro verde, neumáticos gruesos, manillar ancho,
#                        horquilla de suspensión doble
# ══════════════════════════════════════════════════════════════════════════════
W, H     = 48, 32
N_FRAMES = 8

BASE    = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS"
OUT_DIR = os.path.join(BASE, "ITEMS", "BICICLETA_MONTANA")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Paleta ────────────────────────────────────────────────────────────────────
T    = (  0,   0,   0,   0)

# Neumático knobby (grueso, con textura)
TIRE  = ( 18,  18,  22, 255)   # negro base
TIRH  = ( 55,  55,  62, 255)   # brillo
TIRNB = ( 10,  10,  14, 255)   # knob (protuberancia más oscura)
RIM   = (145, 150, 158, 255)   # llanta
SPK   = (205, 210, 218, 255)   # radio
SPKD  = (130, 135, 142, 255)
HUB   = (225, 228, 235, 255)
HUBD  = (160, 165, 172, 255)

# Cuadro verde + naranja accent
FRM  = ( 38, 130,  38, 255)   # verde medio
FRD  = ( 18,  70,  18, 255)   # verde oscuro (sombra)
FRL  = ( 88, 195,  88, 255)   # verde claro (brillo)
ACCN = (255, 138,   0, 255)   # naranja accent (detalles)

# Horquilla de suspensión
FSP  = ( 80,  80,  90, 255)   # gris suspensión
FSPL = (160, 165, 172, 255)   # gris claro suspensión
FSPC = (200, 205, 210, 255)   # crossbar gris muy claro

# Sillín deportivo
SED  = ( 28,  28,  38, 255)   # negro
SEDL = ( 65,  65,  80, 255)   # gris oscuro
SEDH = (110, 110, 130, 255)   # brillo sillín

# Manillar plano ancho
HBR  = ( 32,  32,  40, 255)
HBRL = ( 85,  88,  98, 255)
HBRG = (210, 140,  10, 255)   # grip naranja

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

# ── Rueda MTB: neumático 3px grueso con textura knobby ───────────────────────
def draw_wheel_mtb(img, cx, cy, angle):
    R = 7
    for dy in range(-R, R+1):
        for dx in range(-R, R+1):
            d = math.sqrt(dx*dx + dy*dy)
            x, y = cx+dx, cy+dy
            if d > R: continue

            if d >= R - 0.6:              # capa exterior
                a_px = math.atan2(dy, dx)
                put(img, x, y, TIRH if (-1.1 < a_px < 0.1) else TIRE)

            elif d >= R - 1.4:            # knobs (segunda capa)
                # Simula protuberancias cada ~45°
                a_knob = math.atan2(dy, dx)
                knob = int((a_knob + math.pi) / (math.pi / 4) + angle * 4 / math.pi) % 2
                put(img, x, y, TIRNB if knob == 0 else TIRE)

            elif d >= R - 3.2:            # capa interna del neumático
                put(img, x, y, TIRE)

            elif d >= R - 4.0:            # llanta (más delgada)
                put(img, x, y, RIM)

            elif d <= 1.5:
                put(img, x, y, HUBD if d > 0.8 else HUB)

    # Radios: 4 spokes
    for i in range(4):
        a = angle + i * (math.pi / 2)
        cos_a, sin_a = math.cos(a), math.sin(a)
        for step in range(14):
            t  = step / 13.0
            r  = 1.8 + t * 2.2
            put(img, int(round(cx + r*cos_a)), int(round(cy + r*sin_a)),
                SPK if t > 0.4 else SPKD)

# ── Cuadro MTB ────────────────────────────────────────────────────────────────
def draw_frame_mtb(img):
    RWX, RWY = 10, 23
    FWX, FWY = 37, 23
    BBX, BBY = 23, 23
    STX, STY = 20, 11   # seatpost más corto y erguido
    HTX, HTY = 35, 11
    HBX, HBY = 35, 19

    # Chain stay (doble grosor, más robusto)
    line(img, RWX, RWY,   BBX, BBY,   FRD)
    line(img, RWX, RWY-1, BBX, BBY-1, FRM)
    line(img, RWX, RWY+1, BBX, BBY+1, FRD)   # tercera línea extra robustez

    # Seat stay
    line(img, RWX,   RWY, STX,   STY, FRD)
    line(img, RWX+1, RWY, STX+1, STY, FRM)

    # Seat tube
    line(img, BBX,   BBY, STX,   STY, FRD)
    line(img, BBX-1, BBY, STX-1, STY, FRM)
    line(img, BBX-2, BBY, STX-2, STY, FRL)

    # Top tube (ligeramente inclinado en MTB)
    line(img, STX, STY,   HTX, HTY,   FRM)
    line(img, STX, STY+1, HTX, HTY+1, FRD)
    for x_ in range(STX, HTX+1):
        put(img, x_, STY-1, FRL)

    # Down tube
    line(img, HTX,   HTY, BBX,   BBY, FRD)
    line(img, HTX-1, HTY, BBX-1, BBY, FRM)
    line(img, HTX-2, HTY, BBX-2, BBY, FRL)

    # Head tube (más largo → más suspensión visual)
    line(img, HTX,   HTY, HBX,   HBY, FRM)
    line(img, HTX-1, HTY, HBX-1, HBY, FRL)

    # Accent naranja en el head tube
    for y_ in range(HTY+1, HBY-1):
        put(img, HTX+1, y_, ACCN)

    # ── Horquilla doble de suspensión ────────────────────────────────────────
    # Tubo derecho (exterior)
    line(img, HBX,   HBY, FWX+1, FWY, FSP)
    # Tubo izquierdo (interior)
    line(img, HBX-2, HBY, FWX-1, FWY, FSPL)
    # Crossbars de suspensión (2 travesaños que unen los tubos)
    mid_y = (HBY + FWY) // 2
    for bx in range(FWX-1, HBX+1):
        put(img, bx, mid_y,   FSPC)
        put(img, bx, mid_y+1, FSP)
    # Parte superior de suspensión (bota)
    for y_ in range(HBY, HBY+4):
        put(img, HBX,   y_, FSP)
        put(img, HBX-1, y_, FSPL)
        put(img, HBX-2, y_, FSP)

    # Pedalier
    for ox in [-1, 0, 1]:
        put(img, BBX+ox, BBY, CHNC)
    put(img, BBX, BBY-1, CHNC)

    # ── Sillín deportivo (delgado y puntiagudo) ───────────────────────────────
    put(img, STX, STY-1, FRM)
    # Riel
    line(img, 17, STY-2, 22, STY-2, SED)
    # Superficie (angosta)
    for x_ in range(17, 23): put(img, x_, STY-3, SED)
    for x_ in range(18, 22): put(img, x_, STY-4, SEDL)
    put(img, 19, STY-4, SEDH)   # brillo central
    put(img, 20, STY-4, SEDH)
    # Bordes puntiagudos
    put(img, 17, STY-3, FRD)
    put(img, 22, STY-3, FRD)

    # ── Manillar plano y ancho (flat bar) ─────────────────────────────────────
    # Stem corto
    put(img, HTX,   HTY-1, HBR)
    put(img, HTX-1, HTY-1, HBR)
    # Barra horizontal extendida (más ancha que la normal)
    for x_ in range(28, 44):
        put(img, x_, HTY-1, HBR)
    for x_ in range(29, 43):
        put(img, x_, HTY-2, HBRL)
    # Grips naranjas en extremos
    for y_ in [HTY-1, HTY]:
        for x_ in [28, 29, 42, 43]:
            put(img, x_, y_, HBRG)

# ── Generar frames ────────────────────────────────────────────────────────────
for f in range(N_FRAMES):
    angle = (2 * math.pi * f) / N_FRAMES
    img = Image.new("RGBA", (W, H), T)
    draw_frame_mtb(img)
    draw_wheel_mtb(img, 10, 23, angle)
    draw_wheel_mtb(img, 37, 23, angle)
    fname = f"FRAME{f+1}.png"
    img.save(os.path.join(OUT_DIR, fname))
    print(f"  [OK] {fname}")

print(f"\n=== MTB lista — {N_FRAMES} frames 48×32 en: {OUT_DIR} ===")
