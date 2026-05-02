import sys, math, random
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

# ==============================================================================
# CONFIGURACION
# ==============================================================================
# TIPO:
#   "lodo"    — rectangulo solido de lodo, gradiente centro claro → bordes oscuros
#   "piedra"  — rectangulo solido de piedras con mortero gris
#   "madera"  — rectangulo solido con tablas horizontales de madera
#   "monte"   — rectangulo solido de pasto/grama, colores exactos de MONTE.png

TIPO = "monte"

# ==============================================================================
# COMUN
# ==============================================================================
W, H = 32, 64   # rectangulo perfecto, sin curvas, sin transparencia

# ==============================================================================
# LODO RECTO
# ==============================================================================
MUD_HIGH  = (0x8A, 0x62, 0x2C, 255)
MUD_LIGHT = (0x72, 0x4E, 0x20, 255)
MUD_BASE  = (0x58, 0x3C, 0x16, 255)
MUD_DARK  = (0x3E, 0x28, 0x0C, 255)
MUD_EDGE  = (0x2A, 0x18, 0x08, 255)

def lodo_pixel(x, y):
    hw = W / 2.0
    t  = abs(x - hw) / hw           # 0=centro, 1=borde
    t  = t * t * (3.0 - 2.0 * t)   # smoothstep
    # ruido sutil horizontal para que no sea liso
    noise = math.sin(x * 1.40 + 0.5) * 0.06 + math.sin(x * 3.10 + 1.8) * 0.03
    t = max(0.0, min(1.0, t + noise))
    if   t < 0.22: return MUD_HIGH
    elif t < 0.48: return MUD_LIGHT
    elif t < 0.72: return MUD_BASE
    elif t < 0.88: return MUD_DARK
    else:          return MUD_EDGE

# ==============================================================================
# PIEDRA RECTA
# ==============================================================================
STONE_BASE = [
    (0xC2, 0xBE, 0xBA),
    (0xB4, 0xB0, 0xAC),
    (0xAA, 0xAA, 0xAE),
    (0x9A, 0x98, 0x94),
    (0x90, 0x92, 0x96),
    (0x82, 0x80, 0x7C),
    (0x7A, 0x7C, 0x82),
    (0x6A, 0x68, 0x64),
]
GROUT      = (0x3C, 0x38, 0x34, 255)
STONE_EDGE = (0x22, 0x1E, 0x1A, 255)

rng = random.Random(17)
big = [
    (8,  8,  0.60, 5.0, 3.5),
    (23, 6,  1.20, 4.5, 3.0),
    (14, 18, 0.30, 6.0, 4.0),
    (6,  30, 0.80, 5.5, 3.8),
    (25, 26, 0.10, 4.8, 3.2),
    (11, 42, 1.50, 5.2, 3.6),
    (26, 46, 0.70, 4.2, 3.0),
    (7,  56, 1.10, 5.8, 3.4),
    (20, 58, 0.40, 4.6, 3.1),
]
small = []
for gy in range(12):
    for gx in range(6):
        cx = gx * 5.5 + 0.5 + rng.uniform(-1.8, 1.8)
        cy = gy * 5.5 + 0.5 + rng.uniform(-2.0, 2.0)
        angle = rng.uniform(0, math.pi)
        sx = rng.uniform(1.4, 2.8); sy = rng.uniform(1.1, 2.2)
        small.append((cx, cy, angle, sx, sy, rng.randint(0, 7)))

raw = []
for (cx, cy, angle, sx, sy) in big:
    raw.append((cx, cy, math.cos(-angle), math.sin(-angle), sx, sy, rng.randint(0, 7)))
for (cx, cy, angle, sx, sy, cidx) in small:
    raw.append((cx, cy, math.cos(-angle), math.sin(-angle), sx, sy, cidx))

all_stones = []
for s in raw:
    cx, cy, ca, sa, sx, sy, cidx = s
    for ddx in (-W, 0, W):
        for ddy in (-H, 0, H):
            all_stones.append((cx+ddx, cy+ddy, ca, sa, sx, sy, cidx))

def sdist(px, py, s):
    cx, cy, ca, sa, sx, sy, _ = s
    dx = px - cx; dy = py - cy
    rx = dx*ca - dy*sa; ry = dx*sa + dy*ca
    return math.sqrt((rx/sx)**2 + (ry/sy)**2)

def piedra_pixel(x, y):
    d1 = d2 = 1e9; s1 = None
    for s in all_stones:
        d = sdist(x, y, s)
        if d < d1:   d2 = d1; d1, s1 = d, s
        elif d < d2: d2 = d
    gap = d2 - d1
    if gap < 0.30:
        return GROUT
    cx, cy, ca, sa, sx, sy, cidx = s1
    r, g, b = STONE_BASE[cidx]
    dx = x - cx; dy = y - cy
    lum_n = (dx*(-0.55) + dy*(-0.82)) / max((sx+sy)*0.5, 1)
    adj = int(lum_n * 28)
    return (max(0,min(255,r+adj)), max(0,min(255,g+adj)), max(0,min(255,b+adj)), 255)

# ==============================================================================
# MADERA RECTA
# ==============================================================================
WD_GAP = (0x22, 0x10, 0x04, 255)

# Alturas de tablas. Suma 52 + 12 gaps = 64px
PLANK_HEIGHTS = [4, 3, 5, 4, 4, 3, 6, 4, 4, 5, 4, 6]

PLANK_BASES = [
    (0xAC, 0x72, 0x2C),
    (0x98, 0x62, 0x22),
    (0xB4, 0x78, 0x30),
    (0x9C, 0x66, 0x24),
    (0xA8, 0x6E, 0x2A),
    (0x94, 0x60, 0x20),
    (0xB8, 0x7A, 0x32),
    (0xA0, 0x68, 0x26),
    (0xAE, 0x72, 0x2C),
    (0x96, 0x62, 0x22),
    (0xB0, 0x76, 0x2E),
    (0x9A, 0x64, 0x22),
]

plank_map = []
for pidx, ph in enumerate(PLANK_HEIGHTS):
    for dy in range(ph):
        plank_map.append((pidx, dy, ph))
    plank_map.append(None)

def madera_pixel(x, y):
    if y >= len(plank_map) or plank_map[y] is None:
        return WD_GAP
    pidx, dy, ph = plank_map[y]
    r, g, b = PLANK_BASES[pidx]
    if dy == 0:
        r, g, b = min(255,r+30), min(255,g+30), min(255,b+30)
    elif dy == ph - 1:
        r, g, b = max(0,r-30), max(0,g-30), max(0,b-30)
    grain = (math.sin(x * 0.75 + pidx * 2.1) * 0.28
           + math.sin(x * 1.90 + pidx * 0.8) * 0.14
           + math.sin(x * 3.50 + pidx * 1.5) * 0.07)
    adj = int(grain * 14)
    return (max(0,min(255,r+adj)), max(0,min(255,g+adj)), max(0,min(255,b+adj)), 255)

# ==============================================================================
# MONTE RECTO — colores exactos de MONTE.png, 1x1 pixel
# ==============================================================================
GRASS = [
    (0x0B, 0xA3, 0x03, 255),
    (0x24, 0xAC, 0x17, 255),
    (0x31, 0xAF, 0x20, 255),
    (0x35, 0xB3, 0x1F, 255),
    (0x41, 0xB6, 0x29, 255),
    (0x4B, 0xBD, 0x34, 255),
    (0x51, 0xC2, 0x34, 255),
    (0x54, 0xC2, 0x34, 255),
    (0x5B, 0xC1, 0x36, 255),
    (0x63, 0xC8, 0x3A, 255),
    (0x64, 0xC4, 0x3D, 255),
    (0x76, 0xD4, 0x48, 255),
]

def monte_pixel(x, y):
    v = (x * 1619 + y * 31337 + (x ^ y) * 6791 + x * y * 97) & 0xFFFF
    return GRASS[v % 12]

# ==============================================================================
# RENDER — rectangulo perfecto, todos los pixeles opacos
# ==============================================================================
img = Image.new("RGBA", (W, H), (0, 0, 0, 255))

dispatch = {"lodo": lodo_pixel, "piedra": piedra_pixel, "madera": madera_pixel, "monte": monte_pixel}
pixel_fn = dispatch[TIPO]

for y in range(H):
    for x in range(W):
        img.putpixel((x, y), pixel_fn(x, y))

# ==============================================================================
# GUARDAR
# ==============================================================================
nombres = {
    "lodo":   "camino_lodo_recto.png",
    "piedra": "camino_piedra_recto.png",
    "madera": "camino_madera_recto.png",
    "monte":  "camino_monte_recto.png",
}
nombre = nombres[TIPO]
dst1 = rf"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\CAMINO\{nombre}"
dst2 = rf"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PNGS\{nombre}"
img.save(dst1)
img.save(dst2)
print(f"[{TIPO} recto] Guardado:\n  {dst1}\n  {dst2}")
