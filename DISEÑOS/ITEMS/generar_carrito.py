import sys, math, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

# ══════════════════════════════════════════════════════════════════════════════
# CARRITO MEDIEVAL — carro de madera con ruedas de radios gruesos, tablones,
#                    herrajes de hierro y vara de tiro. 48×32 px, 8 frames.
# ══════════════════════════════════════════════════════════════════════════════
W, H     = 48, 32
N_FRAMES = 8

BASE    = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS"
OUT_DIR = os.path.join(BASE, "ITEMS", "CARRITO")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Paleta ────────────────────────────────────────────────────────────────────
T    = (  0,   0,   0,   0)

# Madera
WD_S = ( 50,  25,   5, 255)   # sombra madera (bordes)
WD_D = ( 90,  48,  12, 255)   # madera oscura
WD_M = (148,  88,  26, 255)   # madera media
WD_L = (198, 132,  50, 255)   # madera clara
WD_H = (230, 168,  78, 255)   # brillo madera
WD_G = ( 68,  36,   8, 255)   # veta de madera / junta entre tablones

# Hierro (herrajes, llantas de rueda)
IRN  = ( 38,  38,  44, 255)   # hierro oscuro
IRNM = ( 62,  62,  70, 255)   # hierro medio
IRNL = ( 92,  94, 104, 255)   # hierro claro (brillo)

# Cuerda / heno (detalle interior carro)
ROPE = (165, 130,  40, 255)
HAY  = (210, 175,  55, 255)
HAYD = (155, 118,  28, 255)

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

# ══════════════════════════════════════════════════════════════════════════════
# RUEDA MEDIEVAL — aro de hierro, llanta gruesa de madera, 6 radios robustos,
#                  cubo grande con herraje central
# ══════════════════════════════════════════════════════════════════════════════
def draw_wheel_medieval(img, cx, cy, angle):
    R = 8   # radio total

    for dy in range(-R, R+1):
        for dx in range(-R, R+1):
            d = math.sqrt(dx*dx + dy*dy)
            x, y = cx+dx, cy+dy
            if d > R: continue

            if d >= R - 0.7:              # llanta de hierro exterior
                a_px = math.atan2(dy, dx)
                put(img, x, y, IRNL if (-1.0 < a_px < 0.2) else IRN)

            elif d >= R - 1.8:            # llanta de hierro interior
                put(img, x, y, IRNM)

            elif d >= R - 3.2:            # aro de madera (felloe)
                a_px = math.atan2(dy, dx)
                put(img, x, y, WD_H if (-1.1 < a_px < 0.3) else WD_M)

            elif d <= 2.2:               # cubo central (hub)
                put(img, x, y, IRNM if d > 1.4 else IRN)

    # — 6 radios gruesos de madera (cada 60°) ─────────────────────────────────
    for i in range(6):
        a    = angle + i * (math.pi / 3)
        ca, sa = math.cos(a), math.sin(a)
        # Radio doble (2 líneas paralelas finas → radio grueso)
        for off in (-0.4, 0.0, 0.4):
            perp = a + math.pi/2
            ox = off * math.cos(perp)
            oy = off * math.sin(perp)
            for step in range(20):
                t = step / 19.0
                r = 2.5 + t * 3.5   # desde hub hasta aro de madera
                ix = int(round(cx + r*ca + ox))
                iy = int(round(cy + r*sa + oy))
                shade = WD_H if t > 0.6 else WD_D
                put(img, ix, iy, shade)

    # Herraje central (disco de hierro en el cubo)
    put(img, cx, cy, IRN)
    put(img, cx+1, cy, IRNM)
    put(img, cx-1, cy, IRNM)
    put(img, cx, cy+1, IRNM)
    put(img, cx, cy-1, IRNM)

# ══════════════════════════════════════════════════════════════════════════════
# CARROCERÍA DEL CARRO MEDIEVAL
# ══════════════════════════════════════════════════════════════════════════════
def draw_cart(img):
    # ── Ejes del carro (vigas longitudinales bajo el piso) ────────────────────
    # Viga principal inferior (travesaño entre ruedas)
    for x in range(9, 38):
        put(img, x, 22, WD_D)
        put(img, x, 21, WD_M)
        put(img, x, 20, WD_S)

    # Travesaño diagonal de refuerzo
    line(img, 10, 21, 18, 18, WD_D)
    line(img, 37, 21, 29, 18, WD_D)

    # ── Plataforma / piso del carro (tablones horizontales) ───────────────────
    #   y=12 a y=19, x=6 a x=41
    for y in range(12, 20):
        for x in range(6, 42):
            # Junta vertical entre tablones cada 5px
            if (x - 6) % 5 == 0:
                put(img, x, y, WD_G)
                continue
            # Junta horizontal entre tablones cada 3px
            if (y - 12) % 3 == 0:
                put(img, x, y, WD_S if x in (6, 41) else WD_D)
                continue
            # Interior del tablón: brillo arriba, sombra abajo
            row_off = (y - 12) % 3
            if row_off == 1:
                c = WD_H if (7 < x < 40) else WD_M
            else:
                c = WD_M if (7 < x < 40) else WD_D
            # Borde lateral
            if x == 6 or x == 41:
                c = WD_S
            elif x == 7 or x == 40:
                c = WD_D
            put(img, x, y, c)

    # ── Tablón frontal del carro (derecha) ────────────────────────────────────
    for y in range(9, 20):
        put(img, 42, y, WD_S)
        put(img, 41, y, WD_D)
        put(img, 40, y, WD_M if y % 2 == 0 else WD_D)
        put(img, 39, y, WD_L if y % 3 != 0 else WD_M)

    # ── Tablón trasero del carro (izquierda) ──────────────────────────────────
    for y in range(9, 20):
        put(img, 5,  y, WD_S)
        put(img, 6,  y, WD_D)
        put(img, 7,  y, WD_M if y % 2 == 0 else WD_D)
        put(img, 8,  y, WD_L if y % 3 != 0 else WD_M)

    # ── Laterales del carro (barandas) — estacas verticales ──────────────────
    for stake_x in [9, 14, 20, 26, 32, 37]:
        for y in range(8, 13):
            put(img, stake_x,   y, WD_D)
            put(img, stake_x+1, y, WD_H if y < 11 else WD_M)
        put(img, stake_x, 7, WD_S)  # punta de estaca

    # Barra horizontal que une las estacas (barandal superior)
    for x in range(9, 39):
        put(img, x, 12, WD_M)
        put(img, x, 11, WD_H)
    for x in range(8, 40):
        put(img, x, 13, WD_D)

    # ── Herrajes de hierro en esquinas ────────────────────────────────────────
    # Esquina delantera
    for y in range(11, 20):
        put(img, 42, y, IRN)
        put(img, 43, y, IRNM)
    for x in range(39, 44):
        put(img, x, 11, IRN)
        put(img, x, 19, IRN)
    # Esquina trasera
    for y in range(11, 20):
        put(img, 5, y, IRN)
        put(img, 4, y, IRNM)
    for x in range(4, 9):
        put(img, x, 11, IRN)
        put(img, x, 19, IRN)

    # ── Vara de tiro (tirante que sale del frente) ────────────────────────────
    # Sale desde la parte delantera del carro hacia la derecha (donde iría el caballo)
    for x in range(42, 48):
        t = (x - 42) / 5.0
        y = int(21 - t * 3)   # sube ligeramente hacia el frente
        put(img, x, y,   WD_D)
        put(img, x, y-1, WD_M)
        if x < 46:
            put(img, x, y+1, WD_S)

    # Refuerzo de la vara (soporte diagonal)
    line(img, 42, 19, 45, 16, WD_S)
    line(img, 41, 19, 44, 16, WD_D)

    # ── Heno / carga dentro del carro ────────────────────────────────────────
    # Pequeños detalles de heno asomando por encima del barandal
    hay = [
        (11,10),(12,9),(13,10),(15,9),(16,10),(18,9),
        (21,10),(23,9),(25,10),(27,9),(28,10),(30,9),
        (33,10),(34,9),(35,10),
    ]
    for (hx, hy) in hay:
        put(img, hx, hy, HAY)
        put(img, hx, hy+1, HAYD)
        if hx % 3 == 0:
            put(img, hx+1, hy, HAYD)

# ══════════════════════════════════════════════════════════════════════════════
# GENERAR FRAMES
# ══════════════════════════════════════════════════════════════════════════════
for f in range(N_FRAMES):
    angle = (2 * math.pi * f) / N_FRAMES

    img = Image.new("RGBA", (W, H), T)

    draw_cart(img)                              # carrocería (debajo)
    draw_wheel_medieval(img,  9, 23, angle)     # rueda trasera
    draw_wheel_medieval(img, 37, 23, angle)     # rueda delantera

    fname = f"FRAME{f+1}.png"
    img.save(os.path.join(OUT_DIR, fname))
    print(f"  [OK] {fname}")

print(f"\n=== CARRITO MEDIEVAL listo — {N_FRAMES} frames 48×32 en: {OUT_DIR} ===")
