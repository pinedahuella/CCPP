import sys, math, random
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

# ==============================================================================
# CONFIGURACION
# ==============================================================================
# TIPO:
#   "lodo"           — camino de lodo con curvas organicas
#   "piedra"         — piedras con curvas + mortero gris
#   "piedra_relleno" — piedras con curvas, huecos transparentes
#   "monte"          — camino de pasto/grama, patron de cuadros verdes
#   "ladrillo"       — camino de ladrillos rojos con mortero

TIPO = "ladrillo"

# ==============================================================================
# COMUN — bordes curvos (tileable)
# ==============================================================================
W, H = 32, 64
K = 2 * math.pi / 64

def left_edge(y):
    n = (5.0*math.sin(y*K*1+0.40)+3.2*math.sin(y*K*2+1.80)+2.0*math.sin(y*K*3+0.70)
        +1.3*math.sin(y*K*5+2.50)+0.8*math.sin(y*K*7+1.20)+0.5*math.sin(y*K*9+3.10)
        +0.3*math.sin(y*K*13+0.90))
    return 1.5 + (n + 13.1) / 26.2 * 9.5

def right_edge(y):
    n = (5.0*math.sin(y*K*1+3.80)+3.2*math.sin(y*K*2+5.20)+2.0*math.sin(y*K*3+2.10)
        +1.3*math.sin(y*K*5+4.70)+0.8*math.sin(y*K*7+0.30)+0.5*math.sin(y*K*9+5.80)
        +0.3*math.sin(y*K*13+2.70))
    return 21.5 + (n + 13.1) / 26.2 * 9.0

# ==============================================================================
# LODO
# ==============================================================================
MUD_HIGH  = (0x8A, 0x62, 0x2C, 255)
MUD_LIGHT = (0x72, 0x4E, 0x20, 255)
MUD_BASE  = (0x58, 0x3C, 0x16, 255)
MUD_DARK  = (0x3E, 0x28, 0x0C, 255)
MUD_EDGE  = (0x20, 0x14, 0x05, 255)

def mud_color(x, lx, rx):
    hw = max(1.0, (rx - lx) * 0.5)
    t  = abs(x - (lx + rx) * 0.5) / hw
    t  = t * t * (3.0 - 2.0 * t)
    if   t < 0.25: return MUD_HIGH
    elif t < 0.50: return MUD_LIGHT
    elif t < 0.75: return MUD_BASE
    else:          return MUD_DARK

# ==============================================================================
# LADRILLO — patron clasico de ladrillos offset fila a fila, tileable
# ==============================================================================
# Brick: 7px ancho x 3px alto + 1px mortero = celda 8x4 tileable en 32x64
BRK_LIGHT  = (0xCC, 0x60, 0x38, 255)   # cara iluminada
BRK_MID    = (0xB0, 0x48, 0x24, 255)   # cuerpo
BRK_DARK   = (0x88, 0x30, 0x14, 255)   # sombra inferior/derecha
BRK_MORTAR = (0xC8, 0xB8, 0x98, 255)   # junta beige
BRK_EDGE   = (0x48, 0x18, 0x08, 255)   # contorno del camino

def brick_pixel(x, y):
    # Fila: cada 4px. Columna: offset de 4px en filas impares
    row    = (y % 64) // 4
    dy     = (y % 64) % 4          # 0-3 dentro de la fila
    offset = 4 if (row % 2) else 0
    col    = ((x + offset) % 32) // 8
    dx     = ((x + offset) % 32) % 8  # 0-7 dentro del ladrillo

    # Mortero horizontal (dy==3) y vertical (dx==7)
    if dy == 3 or dx == 7:
        return BRK_MORTAR

    # Variacion de tono por ladrillo (hash simple)
    tone = (row * 7 + col * 13 + row * col * 3) % 3

    # Gradiente: fila superior luz, inferior sombra, laterales
    if dy == 0:
        base = BRK_LIGHT
    elif dy == 2:
        base = BRK_DARK
    else:
        base = BRK_MID

    # Ajuste sutil por tono de ladrillo
    r, g, b, a = base
    adj = (tone - 1) * 12   # -12, 0, +12
    return (max(0,min(255,r+adj)), max(0,min(255,g+adj)), max(0,min(255,b+adj)), 255)

# ==============================================================================
# MONTE (pasto/grama) — patron de cuadros verdes como referencia
# ==============================================================================
# Colores exactos muestreados de MONTE.png (los mas frecuentes)
GRASS = [
    (0x0B, 0xA3, 0x03, 255),   # 0  muy oscuro
    (0x24, 0xAC, 0x17, 255),   # 1  oscuro
    (0x31, 0xAF, 0x20, 255),   # 2  oscuro medio
    (0x35, 0xB3, 0x1F, 255),   # 3  medio oscuro
    (0x41, 0xB6, 0x29, 255),   # 4  medio
    (0x4B, 0xBD, 0x34, 255),   # 5  medio claro
    (0x51, 0xC2, 0x34, 255),   # 6  claro
    (0x54, 0xC2, 0x34, 255),   # 7  claro calido
    (0x5B, 0xC1, 0x36, 255),   # 8  claro frio
    (0x63, 0xC8, 0x3A, 255),   # 9  brillante
    (0x64, 0xC4, 0x3D, 255),   # 10 muy brillante
    (0x76, 0xD4, 0x48, 255),   # 11 highlight
]
GRASS_EDGE = (0x07, 0x80, 0x01, 255)   # contorno del camino

def grass_pixel(x, y):
    # Hash 1x1 por pixel, tileable, 12 colores exactos de MONTE.png
    px = x % W;  py = y % H
    v = (px * 1619 + py * 31337 + (px ^ py) * 6791 + px * py * 97) & 0xFFFF
    return GRASS[v % 12]

# ==============================================================================
# PIEDRA
# ==============================================================================
STONE_BASE = [
    (0xC2, 0xBE, 0xBA), (0xB4, 0xB0, 0xAC), (0xAA, 0xAA, 0xAE), (0x9A, 0x98, 0x94),
    (0x90, 0x92, 0x96), (0x82, 0x80, 0x7C), (0x7A, 0x7C, 0x82), (0x6A, 0x68, 0x64),
]
GROUT      = (0x3C, 0x38, 0x34, 255)
STONE_EDGE = (0x22, 0x1E, 0x1A, 255)

rng = random.Random(17)
big = [
    (8,8,0.60,5.0,3.5),(23,6,1.20,4.5,3.0),(14,18,0.30,6.0,4.0),
    (6,30,0.80,5.5,3.8),(25,26,0.10,4.8,3.2),(11,42,1.50,5.2,3.6),
    (26,46,0.70,4.2,3.0),(7,56,1.10,5.8,3.4),(20,58,0.40,4.6,3.1),
]
small = []
for gy in range(12):
    for gx in range(6):
        cx = gx*5.5+0.5+rng.uniform(-1.8,1.8); cy = gy*5.5+0.5+rng.uniform(-2.0,2.0)
        angle = rng.uniform(0,math.pi); sx = rng.uniform(1.4,2.8); sy = rng.uniform(1.1,2.2)
        small.append((cx,cy,angle,sx,sy,rng.randint(0,7)))
raw = []
for (cx,cy,angle,sx,sy) in big:
    raw.append((cx,cy,math.cos(-angle),math.sin(-angle),sx,sy,rng.randint(0,7)))
for (cx,cy,angle,sx,sy,cidx) in small:
    raw.append((cx,cy,math.cos(-angle),math.sin(-angle),sx,sy,cidx))
all_stones = []
for s in raw:
    cx,cy,ca,sa,sx,sy,cidx = s
    for ddx in (-W,0,W):
        for ddy in (-H,0,H):
            all_stones.append((cx+ddx,cy+ddy,ca,sa,sx,sy,cidx))

def sdist(px,py,s):
    cx,cy,ca,sa,sx,sy,_ = s
    dx=px-cx; dy=py-cy; rx=dx*ca-dy*sa; ry=dx*sa+dy*ca
    return math.sqrt((rx/sx)**2+(ry/sy)**2)

# ==============================================================================
# RENDER
# ==============================================================================
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

for y in range(H):
    lx = left_edge(y);  rx = right_edge(y)
    lx_u = left_edge((y-1)%H); rx_u = right_edge((y-1)%H)
    lx_d = left_edge((y+1)%H); rx_d = right_edge((y+1)%H)

    for x in range(W):
        if not (lx <= x <= rx):
            continue
        on_edge = (x < lx+1 or x > rx-1 or
                   not (lx_u <= x <= rx_u) or not (lx_d <= x <= rx_d))

        if TIPO == "ladrillo":
            img.putpixel((x,y), BRK_EDGE if on_edge else brick_pixel(x,y))

        elif TIPO == "monte":
            img.putpixel((x,y), GRASS_EDGE if on_edge else grass_pixel(x,y))

        elif TIPO == "lodo":
            img.putpixel((x,y), MUD_EDGE if on_edge else mud_color(x,lx,rx))

        else:  # piedra / piedra_relleno
            if on_edge:
                if TIPO == "piedra": img.putpixel((x,y), STONE_EDGE)
                continue
            d1=d2=1e9; s1=None
            for s in all_stones:
                d=sdist(x,y,s)
                if d<d1: d2=d1; d1,s1=d,s
                elif d<d2: d2=d
            if d2-d1 < 0.30:
                if TIPO == "piedra": img.putpixel((x,y), GROUT)
            else:
                cx,cy,ca,sa,sx,sy,cidx = s1
                r,g,b = STONE_BASE[cidx]
                lum_n = ((x-cx)*(-0.55)+(y-cy)*(-0.82)) / max((sx+sy)*0.5,1)
                adj = int(lum_n*28)
                img.putpixel((x,y),(max(0,min(255,r+adj)),max(0,min(255,g+adj)),max(0,min(255,b+adj)),255))

# ==============================================================================
# GUARDAR
# ==============================================================================
nombres = {
    "lodo":           "camino_lodo.png",
    "piedra":         "camino_piedra.png",
    "piedra_relleno": "camino_piedra_relleno.png",
    "monte":          "camino_monte.png",
    "ladrillo":       "camino_ladrillo.png",
}
nombre = nombres[TIPO]
dst1 = rf"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\CAMINO\{nombre}"
dst2 = rf"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PNGS\{nombre}"
img.save(dst1)
img.save(dst2)
print(f"[{TIPO} curvo] Guardado:\n  {dst1}\n  {dst2}")
