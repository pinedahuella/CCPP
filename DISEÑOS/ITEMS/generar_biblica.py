import sys, math, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════
W, H     = 48, 32
N_FRAMES = 8

BASE    = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS"
OUT_DIR = os.path.join(BASE, "ITEMS", "BICICLETA")
os.makedirs(OUT_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# PALETA
# ══════════════════════════════════════════════════════════════════════════════
T    = (  0,   0,   0,   0)   # transparente

# Rueda
TIRE = ( 22,  22,  26, 255)   # neumático negro
TIRH = ( 68,  68,  76, 255)   # brillo neumático (cuadrante sup-der)
RIM  = (155, 160, 168, 255)   # llanta plateada
SPK  = (210, 215, 222, 255)   # radio plateado
SPKD = (140, 145, 152, 255)   # radio sombra
HUB  = (230, 234, 240, 255)   # cubo plateado claro
HUBD = (170, 175, 182, 255)   # cubo borde

# Cuadro
FRM  = (210,  30,  30, 255)   # rojo brillante
FRD  = (138,  10,  10, 255)   # rojo oscuro (sombra)
FRL  = (246, 102,  90, 255)   # rojo claro  (brillo)
FORK = (182,  24,  24, 255)   # horquilla

# Sillín
SED  = ( 88,  52,  16, 255)   # marrón oscuro
SEDL = (150,  98,  44, 255)   # marrón claro
SEDC = ( 60,  35,  10, 255)   # marrón muy oscuro (borde)

# Manillar
HBR  = ( 34,  34,  42, 255)   # gris oscuro
HBRL = ( 88,  90, 100, 255)   # gris claro

# Cadena / BB
CHNC = ( 80,  65,  18, 255)   # dorado oscuro

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def put(img, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), c)

def line(img, x0, y0, x1, y1, c):
    """Línea de Bresenham."""
    dx = abs(x1-x0); dy = abs(y1-y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        put(img, x0, y0, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2*err
        if e2 > -dy: err -= dy; x0 += sx
        if e2 < dx:  err += dx; y0 += sy

# ══════════════════════════════════════════════════════════════════════════════
# RUEDA ANIMADA
# ══════════════════════════════════════════════════════════════════════════════
def draw_wheel(img, cx, cy, angle):
    """
    Dibuja la rueda completa:
      - Neumático 2px negro con brillo
      - Llanta 1px plateada
      - Interior transparente
      - 4 radios (rotados) + cubo
    """
    R = 7  # radio exterior (neumático)

    for dy in range(-R, R+1):
        for dx in range(-R, R+1):
            d = math.sqrt(dx*dx + dy*dy)
            x, y = cx+dx, cy+dy
            if d > R:
                continue

            if d >= R - 0.6:              # capa exterior del neumático
                ang_px = math.atan2(dy, dx)
                c = TIRH if (-1.1 < ang_px < 0.1) else TIRE
                put(img, x, y, c)

            elif d >= R - 2.0:            # capa interior del neumático
                put(img, x, y, TIRE)

            elif d >= R - 3.0:            # llanta
                put(img, x, y, RIM)

            elif d <= 1.5:                # cubo
                c = HUBD if (d > 0.8) else HUB
                put(img, x, y, c)

            # else: interior transparente — los radios se pisan encima

    # — Radios: 4 spokes a 90° entre sí, girados según el frame —
    for i in range(4):
        a = angle + i * (math.pi / 2)
        cos_a = math.cos(a)
        sin_a = math.sin(a)
        for step in range(18):
            t  = step / 17.0
            r  = 1.8 + t * 2.8   # desde hub (r≈2) hasta llanta interior (r≈4.6)
            px = cx + r * cos_a
            py = cy + r * sin_a
            ix, iy = int(round(px)), int(round(py))
            shade = SPK if t > 0.4 else SPKD
            put(img, ix, iy, shade)

# ══════════════════════════════════════════════════════════════════════════════
# CUADRO DE LA BICICLETA (estático)
# ══════════════════════════════════════════════════════════════════════════════
def draw_frame(img):
    """
    Marco diamante clásico:
      RWX,RWY  = eje trasero   (10, 23)
      FWX,FWY  = eje delantero (37, 23)
      BBX,BBY  = pedalier      (23, 23)
      STX,STY  = tope sillín   (19, 12)
      HTX,HTY  = tope dirección(35, 12)
      HBX,HBY  = base dirección(35, 20)
    """
    RWX, RWY = 10, 23
    FWX, FWY = 37, 23
    BBX, BBY = 23, 23
    STX, STY = 19, 12
    HTX, HTY = 35, 12
    HBX, HBY = 35, 20

    # ── Chain stay: eje trasero → pedalier ───────────────────────────────────
    line(img, RWX, RWY,   BBX, BBY,   FRD)   # sombra
    line(img, RWX, RWY-1, BBX, BBY-1, FRM)   # principal

    # ── Seat stay: eje trasero → tope sillín ─────────────────────────────────
    line(img, RWX,   RWY, STX,   STY, FRD)
    line(img, RWX+1, RWY, STX+1, STY, FRM)

    # ── Seat tube: pedalier → tope sillín ────────────────────────────────────
    line(img, BBX,   BBY, STX,   STY, FRD)
    line(img, BBX-1, BBY, STX-1, STY, FRM)
    line(img, BBX-2, BBY, STX-2, STY, FRL)   # brillo

    # ── Top tube: tope sillín → tope dirección (horizontal) ──────────────────
    line(img, STX, STY,   HTX, HTY,   FRM)
    line(img, STX, STY+1, HTX, HTY+1, FRD)
    for x_ in range(STX, HTX+1):
        put(img, x_, STY-1, FRL)             # brillo superior

    # ── Down tube: tope dirección → pedalier (diagonal) ──────────────────────
    line(img, HTX,   HTY, BBX,   BBY, FRD)
    line(img, HTX-1, HTY, BBX-1, BBY, FRM)
    line(img, HTX-2, HTY, BBX-2, BBY, FRL)   # brillo

    # ── Head tube: tope → base dirección (vertical) ──────────────────────────
    line(img, HTX,   HTY, HBX,   HBY, FRM)
    line(img, HTX-1, HTY, HBX-1, HBY, FRL)  # brillo

    # ── Horquilla: base dirección → eje delantero ────────────────────────────
    line(img, HBX,   HBY, FWX,   FWY, FORK)
    line(img, HBX-1, HBY, FWX-1, FWY, FRM)

    # ── Pedalier (small indicator) ────────────────────────────────────────────
    for ox in [-1, 0, 1]:
        put(img, BBX+ox, BBY, CHNC)
    put(img, BBX, BBY-1, CHNC)

    # ── Sillín ────────────────────────────────────────────────────────────────
    # Post tip
    put(img, STX, STY-1, FRM)
    # Base del sillín (riel)
    line(img, 15, STY-2, 21, STY-2, SEDC)
    # Superficie del sillín (suave curva simulada)
    for x_ in range(14, 23):
        put(img, x_, STY-3, SED)
    for x_ in range(15, 22):
        put(img, x_, STY-4, SEDL)
    # Bordes
    put(img, 14, STY-3, SEDC)
    put(img, 22, STY-3, SEDC)
    put(img, 15, STY-5, SEDL)   # pequeño abultamiento frontal
    put(img, 16, STY-5, SED)

    # ── Manillar ──────────────────────────────────────────────────────────────
    # Vástago (stem) sube desde head tube top
    put(img, HTX,   HTY-1, HBR)
    put(img, HTX,   HTY-2, HBR)
    put(img, HTX-1, HTY-2, HBR)
    # Barra horizontal
    for x_ in range(32, 41):
        put(img, x_, HTY-2, HBR)
    # Brillo en barra
    for x_ in range(33, 40):
        put(img, x_, HTY-3, HBRL)
    # Grips (extremos caídos)
    for y_ in [HTY-2, HTY-1]:
        put(img, 32, y_, HBR)
        put(img, 40, y_, HBR)
    put(img, 32, HTY,   HBR)
    put(img, 40, HTY,   HBR)
    # Brillo grips
    put(img, 33, HTY-1, HBRL)
    put(img, 39, HTY-1, HBRL)

# ══════════════════════════════════════════════════════════════════════════════
# GENERAR LOS 8 FRAMES
#   Cada frame rota las ruedas 45° (360°/8) → animación fluida de giro
# ══════════════════════════════════════════════════════════════════════════════
for f in range(N_FRAMES):
    angle = (2 * math.pi * f) / N_FRAMES   # 0 → 2π distribuido en 8 frames

    img = Image.new("RGBA", (W, H), T)

    draw_frame(img)                         # cuadro primero (atrás)
    draw_wheel(img, 10, 23, angle)          # rueda trasera
    draw_wheel(img, 37, 23, angle)          # rueda delantera

    fname = f"FRAME{f+1}.png"
    img.save(os.path.join(OUT_DIR, fname))
    print(f"  [OK] {fname}")

print(f"\n=== BICICLETA lista — {N_FRAMES} frames 48×32 en: {OUT_DIR} ===")
