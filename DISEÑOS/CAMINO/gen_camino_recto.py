import sys, math, random
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

# ==============================================================================
# CONFIGURACION
# ==============================================================================
# TIPO:
#   "lodo"      — rectangulo solido de lodo, gradiente centro claro → bordes oscuros
#   "piedra"    — rectangulo solido de piedras con mortero gris
#   "madera"    — rectangulo solido con tablas horizontales de madera
#   "monte"     — rectangulo solido de pasto/grama, colores exactos de MONTE.png
#   "ladrillo"  — rectangulo solido de ladrillos rojos con mortero

TIPO = "procesion6"

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
# LADRILLO RECTO
# ==============================================================================
BRK_LIGHT  = (0xCC, 0x60, 0x38, 255)
BRK_MID    = (0xB0, 0x48, 0x24, 255)
BRK_DARK   = (0x88, 0x30, 0x14, 255)
BRK_MORTAR = (0xC8, 0xB8, 0x98, 255)

def ladrillo_pixel(x, y):
    row    = y // 4
    dy     = y % 4
    offset = 4 if (row % 2) else 0
    col    = ((x + offset) % 32) // 8
    dx     = ((x + offset) % 32) % 8
    if dy == 3 or dx == 7:
        return BRK_MORTAR
    tone = (row * 7 + col * 13 + row * col * 3) % 3
    base = BRK_LIGHT if dy == 0 else (BRK_DARK if dy == 2 else BRK_MID)
    r, g, b, a = base
    adj = (tone - 1) * 12
    return (max(0,min(255,r+adj)), max(0,min(255,g+adj)), max(0,min(255,b+adj)), 255)

# ==============================================================================
# ALFOMBRA ROJA RECTA
# ==============================================================================
# Diseno: borde oscuro + linea dorada + campo rojo con rombos y espina central
# Patron vertical repite cada 16px (tileable en 64)
ALP_BORDER = (0x48, 0x04, 0x04, 255)   # compartido: borde exterior muy oscuro
ALP_DEEP   = (0x72, 0x08, 0x08, 255)   # rojo profundo
ALP_MID    = (0x9C, 0x10, 0x10, 255)   # rojo principal
ALP_BRIGHT = (0xC0, 0x1C, 0x1C, 255)   # rojo brillante (centro)
ALP_GOLD   = (0xDC, 0xAC, 0x22, 255)   # oro claro
ALP_GOLD_DK= (0xA4, 0x78, 0x10, 255)   # oro oscuro

def procesion_pixel(x, y):
    # ── Divisores dorados entre carriles ─────────────────────────────────────
    # Layout: [carril1: x=0-9] [div: x=10] [carril2: x=11-20] [div: x=21] [carril3: x=22-31]
    GLD  = (0xDC, 0xAC, 0x22, 255)
    GLDK = (0xA4, 0x78, 0x10, 255)

    if x == 10 or x == 21:
        return GLD

    # ── CARRIL 1 — Morado (Penitencia / Cuaresma) ────────────────────────────
    # Cruz dorada sobre fondo violeta, repite cada 8px
    if x <= 9:
        lx = x
        PD = (0x26, 0x02, 0x3E, 255)   # morado oscuro
        PM = (0x52, 0x08, 0x82, 255)   # morado medio
        PL = (0x72, 0x14, 0xAC, 255)   # morado claro
        # Borde
        if lx == 0 or lx == 9: return PD
        if lx == 1 or lx == 8: return GLDK
        # Campo lx=2..7 (6px), eje=4
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 8; dy4 = abs(py - 4)
        if py == 0: return GLDK               # separador horizontal
        if dx < 0.6 and dy4 <= 2: return GLD  # barra vertical cruz
        if dy4 == 0 and dx <= 2.0: return GLD # barra horizontal cruz
        if dy4 == 1 and dx <= 1.0: return GLDK
        if dx >= 2.5: return PD
        return PM

    # ── CARRIL 2 — Rojo carmesi (Sangre de Cristo) ───────────────────────────
    # Medallon con rombo y cruz, repite cada 16px
    if x <= 20:
        lx = x - 11
        RD = (0x46, 0x04, 0x04, 255)
        RM = (0x8C, 0x08, 0x08, 255)
        RL = (0xBC, 0x18, 0x18, 255)
        if lx == 0 or lx == 9: return RD
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 16; dy8 = abs(py - 8)
        if py == 0: return GLDK
        dist = dx + dy8
        if dist == 6: return GLD              # contorno rombo
        if dist == 7: return GLDK
        if dist < 6:
            if dx < 0.6 and dy8 <= 3: return GLD   # cruz vertical
            if dy8 == 0 and dx <= 2.0: return GLD  # cruz horizontal
            if dist <= 2: return RL
            return RL
        if dx < 0.6: return RD
        if dx >= 2.5: return RD
        return RM

    # ── CARRIL 3 — Azul real (Virgen Maria / Esperanza) ─────────────────────
    # Estrella de 4 puntas con diagonal, repite cada 8px
    lx = x - 22
    BD = (0x04, 0x08, 0x52, 255)
    BM = (0x08, 0x16, 0x88, 255)
    BL = (0x12, 0x28, 0xB0, 255)
    if lx == 0 or lx == 9: return BD
    if lx == 1 or lx == 8: return GLDK
    ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
    py = y % 8; dy4 = abs(py - 4)
    if py == 0: return GLDK
    # Estrella: cruz + diagonales a 45°
    if dx < 0.6 and dy4 <= 2: return GLD     # vertical
    if dy4 == 0 and dx <= 2.0: return GLD    # horizontal
    if abs(dx - dy4) < 0.6 and dx <= 2.0: return GLDK  # diagonal
    if dx >= 2.5: return BD
    return BM

def procesion5_pixel(x, y):
    GLD  = (0xDC, 0xAC, 0x22, 255)
    GLDK = (0xA4, 0x78, 0x10, 255)

    if x == 10 or x == 21:
        return GLD

    # ── CARRIL 1 — Azul marino (Bautismo / Agua viva) ────────────────────────
    # Ola continua: cresta dorada que sube y baja, repite cada 8px
    if x <= 9:
        lx = x
        AD = (0x04, 0x0C, 0x3C, 255)   # azul marino oscuro
        AM = (0x06, 0x18, 0x68, 255)   # azul marino medio
        AL = (0x0A, 0x28, 0x90, 255)   # azul marino claro
        if lx == 0 or lx == 9: return AD
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 8
        # Ola: seno simplificado sobre ix
        # En py=0..3 la cresta avanza de izq a der; py=4..7 vuelve
        crest = py if py <= 4 else (8 - py)   # 0..4..0
        crest_x = crest / 4.0 * 5.0           # 0..5
        dist_wave = abs(ix - crest_x)
        if dist_wave < 0.8:  return GLD
        if dist_wave < 1.5:  return GLDK
        # Espuma en pico (py=4) y valle (py=0)
        if (py == 0 or py == 4) and dx < 0.8: return GLDK
        if dx >= 2.5: return AD
        # Sombreado: mas oscuro en parte baja de la ola
        return AM if ix < crest_x else AL

    # ── CARRIL 2 — Verde esmeralda (Eucaristia / Santisimo Sacramento) ────────
    # Caliz simplificado + hostia, repite cada 16px
    if x <= 20:
        lx = x - 11
        ED = (0x02, 0x30, 0x18, 255)   # esmeralda oscuro
        EM = (0x04, 0x58, 0x2C, 255)   # esmeralda medio
        EL = (0x08, 0x80, 0x40, 255)   # esmeralda claro
        if lx == 0 or lx == 9: return ED
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 16; dy8 = abs(py - 8)
        if py == 0: return GLDK
        # Hostia (circulo dorado): centro en py=3, radio=2
        if dx*dx + (py-3)*(py-3) <= 3.8: return GLD   # disco hostia
        if dx*dx + (py-3)*(py-3) <= 5.5: return GLDK
        # Caliz: copa en py=5..10, pie en py=11..14
        # Copa: ancho crece con py (py=5 estrecho, py=9 ancho)
        if 5 <= py <= 9:
            copa_w = (py - 5) / 4.0 * 2.5   # 0..2.5
            if dx <= copa_w + 0.5: return GLD if dx <= copa_w else GLDK
        # Base del caliz (pie)
        if py == 10 and dx < 0.8: return GLD
        if 11 <= py <= 12 and dx <= 2.0: return GLDK   # plataforma
        if dx >= 2.5: return ED
        return EM

    # ── CARRIL 3 — Dorado puro (Cristo Rey / Santisima Trinidad) ─────────────
    # Cuadros concéntricos girados 45° (patron heraldico), repite cada 8px
    lx = x - 22
    DD = (0x4C, 0x2C, 0x02, 255)   # dorado muy oscuro
    DM = (0x90, 0x5C, 0x06, 255)   # dorado oscuro
    DL = (0xC8, 0x90, 0x0E, 255)   # dorado claro
    if lx == 0 or lx == 9: return DD
    if lx == 1 or lx == 8: return GLD
    ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
    py = y % 8; dy4 = abs(py - 4)
    if py == 0: return GLD
    # Rombo exterior (dist=4), medio (dist=2), punto central (dist=0)
    dist = dx + dy4
    if dist == 4: return (0xF0, 0xD0, 0x40, 255)   # borde exterior brillante
    if dist == 3: return GLD
    if dist == 2: return DL
    if dist == 1: return GLD
    if dist == 0: return (0xF8, 0xEC, 0x60, 255)   # centro: oro puro
    if dx >= 2.5: return DD
    return DM

def procesion4_pixel(x, y):
    GLD  = (0xDC, 0xAC, 0x22, 255)
    GLDK = (0xA4, 0x78, 0x10, 255)

    if x == 10 or x == 21:
        return GLD

    # ── CARRIL 1 — Marfil/Blanco (Navidad / Pascua / Matrimonio) ─────────────
    # Cruz grande solemne centrada, repite cada 16px
    if x <= 9:
        lx = x
        ID = (0x88, 0x78, 0x48, 255)   # marfil oscuro
        IM = (0xC8, 0xB8, 0x80, 255)   # marfil medio
        IL = (0xEC, 0xE0, 0xB4, 255)   # marfil claro
        if lx == 0 or lx == 9: return ID
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 16; dy8 = abs(py - 8)
        if py == 0: return GLDK
        # Cruz grande: brazo vertical todo el segmento, horizontal en centro
        if dx < 0.6:                   return GLD    # barra vertical
        if dy8 <= 1 and dx <= 2.0:    return GLD    # barra horizontal
        if dy8 == 2 and dx <= 1.5:    return GLDK   # ensanche horizontal
        # Puntos ornamentales en las 4 puntas de la cruz
        if dy8 <= 1 and dx >= 2.0:    return ID
        if dx >= 2.5:                  return ID
        return IM

    # ── CARRIL 2 — Cobre/Terracota (festivo / cosecha / agradecimiento) ───────
    # Reticulado diagonal de rombos (lattice), repite cada 4px
    if x <= 20:
        lx = x - 11
        CD = (0x4C, 0x1C, 0x04, 255)   # cobre oscuro
        CM = (0x88, 0x38, 0x08, 255)   # cobre medio
        CL = (0xC0, 0x60, 0x14, 255)   # cobre claro
        if lx == 0 or lx == 9: return CD
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 4
        # Diagonal lattice: lineas donde (ix+py)%4==0 o (ix-py+64)%4==0
        d1 = (int(ix*2) + py) % 4
        d2 = (int(ix*2) - py + 256) % 4
        if d1 == 0 and d2 == 0: return GLD    # interseccion = nudo
        if d1 == 0 or d2 == 0: return GLDK    # linea diagonal
        if dx >= 2.5: return CD
        # Interior del rombo: claro en centro, oscuro en borde
        if dx < 1.0: return CL
        return CM

    # ── CARRIL 3 — Plateado/Gris perla (angeles / gloria celestial) ──────────
    # Zigzag dorado continuo (onda), repite cada 8px
    lx = x - 22
    SD = (0x28, 0x30, 0x44, 255)   # gris azulado oscuro
    SM = (0x48, 0x54, 0x70, 255)   # gris medio
    SL = (0x78, 0x88, 0xA8, 255)   # gris perla claro
    if lx == 0 or lx == 9: return SD
    if lx == 1 or lx == 8: return GLDK
    ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
    py = y % 8
    # Zigzag: la "cresta" de la onda sube y baja
    # En py=0..3 la cresta va de izq a der; en py=4..7 vuelve
    wave_x = py if py <= 4 else (8 - py)   # 0..4..0
    wave_pos = wave_x / 4.0 * 5.0          # 0..5 → posicion en ix
    on_wave  = abs(ix - wave_pos) < 0.8
    on_trail = abs(ix - wave_pos) < 1.5
    if py == 0 or py == 4: return GLDK      # separadores en picos/valles
    if on_wave:  return GLD
    if on_trail: return GLDK
    if dx >= 2.5: return SD
    return SM

def procesion3_pixel(x, y):
    # Mismos divisores → conecta con procesion1 y procesion2
    GLD  = (0xDC, 0xAC, 0x22, 255)
    GLDK = (0xA4, 0x78, 0x10, 255)

    if x == 10 or x == 21:
        return GLD

    # ── CARRIL 1 — Rosa (Gaudete / Laetare — alegria en penitencia) ──────────
    # Cadena de pequenos rombos conectados, repite cada 8px
    if x <= 9:
        lx = x
        PD = (0x5C, 0x06, 0x2C, 255)   # rosa oscuro
        PM = (0x98, 0x0E, 0x50, 255)   # rosa medio
        PL = (0xC4, 0x1A, 0x6C, 255)   # rosa claro
        if lx == 0 or lx == 9: return PD
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 8; dy2a = abs(py - 2); dy2b = abs(py - 6)
        if py == 0: return GLDK
        # Rombo superior (centro en py=2)
        if dx + dy2a <= 1: return GLD
        if dx + dy2a == 2: return GLDK
        # Rombo inferior (centro en py=6)
        if dx + dy2b <= 1: return GLD
        if dx + dy2b == 2: return GLDK
        # Hilo conector vertical entre rombos (py=3..5, dx<0.5)
        if 3 <= py <= 5 and dx < 0.6: return GLDK
        if dx >= 2.5: return PD
        return PM

    # ── CARRIL 2 — Negro/Gris (Viernes Santo — solemnidad) ───────────────────
    # Arco gotico apuntado, repite cada 16px
    if x <= 20:
        lx = x - 11
        ND = (0x0C, 0x08, 0x0C, 255)   # negro azulado
        NM = (0x28, 0x20, 0x28, 255)   # gris oscuro
        NL = (0x44, 0x38, 0x44, 255)   # gris medio
        if lx == 0 or lx == 9: return ND
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 16; dy0 = py; dy16 = 16 - py
        if py == 0: return GLD          # base dorada
        # Arco apuntado: dos lados que suben hacia el centro en py=8
        # lado izquierdo sube: x decrece con py  → oro en dx == (8-dy0)/3.5
        apex = py <= 8
        dy_arch = py if apex else (16 - py)   # 0=base, 8=punta
        # Ancho del arco: en base(dy=0) cubre todo; en punta(dy=8) un pixel
        arch_w = (8 - dy_arch) / 8.0 * 2.5   # 2.5 en base, 0 en punta
        on_left  = abs(dx - arch_w) < 0.7
        on_right = on_left                     # simetrico
        if dy_arch == 8 and dx < 0.6: return GLD   # punta del arco
        if on_left and dy_arch > 0: return GLD if dy_arch >= 7 else GLDK
        if dx < 0.6 and dy_arch <= 2: return GLDK  # espina superior
        if dx >= 2.5: return ND
        return NM

    # ── CARRIL 3 — Celeste (Inmaculada Concepcion) ───────────────────────────
    # Estrella de 8 puntas (+ y x combinadas), repite cada 8px
    lx = x - 22
    CD = (0x04, 0x30, 0x70, 255)   # celeste oscuro
    CM = (0x08, 0x58, 0xB0, 255)   # celeste medio
    CL = (0x14, 0x80, 0xD8, 255)   # celeste claro
    if lx == 0 or lx == 9: return CD
    if lx == 1 or lx == 8: return GLDK
    ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
    py = y % 8; dy4 = abs(py - 4)
    if py == 0: return GLDK
    # Estrella 8 puntas: brazos rectos (+) + brazos diagonales (x)
    on_plus  = (dx < 0.6 and dy4 <= 2) or (dy4 == 0 and dx <= 2.0)
    on_diag  = abs(dx - dy4) < 0.6 and dx <= 2.0
    if on_plus and on_diag: return GLD    # interseccion = centro
    if on_plus: return GLD
    if on_diag: return GLDK
    if dx >= 2.5: return CD
    return CM

def procesion2_pixel(x, y):
    # Mismos divisores y posiciones de carriles que procesion1 → conectan
    GLD  = (0xDC, 0xAC, 0x22, 255)
    GLDK = (0xA4, 0x78, 0x10, 255)

    if x == 10 or x == 21:
        return GLD

    # ── CARRIL 1 — Dorado/Amarillo (Gloria / Tiempo Pascual) ─────────────────
    # Rombo dorado sobre fondo ambar, repite cada 12px (12x4=48... no tile)
    # uso 8px para tileable en 64
    if x <= 9:
        lx = x
        AD = (0x6C, 0x44, 0x02, 255)   # ambar oscuro
        AM = (0xA8, 0x6C, 0x04, 255)   # ambar medio
        AL = (0xD4, 0x98, 0x08, 255)   # ambar claro
        if lx == 0 or lx == 9: return AD
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 8; dy4 = abs(py - 4)
        if py == 0: return AD                   # separador oscuro
        # Rombo puro (sin cruz)
        dist = dx + dy4
        if dist == 3: return GLD               # contorno rombo
        if dist == 4: return GLDK
        if dist < 3:
            return AL                           # interior brillante
        if dx >= 2.5: return AD
        return AM

    # ── CARRIL 2 — Verde (Esperanza / Tiempo Ordinario) ──────────────────────
    # Flor de 4 petalos dorada, repite cada 8px
    if x <= 20:
        lx = x - 11
        VD = (0x04, 0x30, 0x06, 255)   # verde muy oscuro
        VM = (0x08, 0x58, 0x0C, 255)   # verde medio
        VL = (0x0C, 0x7C, 0x10, 255)   # verde claro
        if lx == 0 or lx == 9: return VD
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 8; dy4 = abs(py - 4)
        if py == 0: return GLDK
        # Flor: 4 petalos en diagonal — puntos donde dx≈dy4 y pequeños
        on_diag = abs(dx - dy4) < 0.7 and dx <= 2.0
        on_cross_v = dx < 0.6 and dy4 <= 1
        on_cross_h = dy4 == 0 and dx <= 1.0
        if on_cross_v or on_cross_h: return GLD   # centro de la flor
        if on_diag: return GLDK                    # petalos diagonales
        if dx >= 2.5: return VD
        return VM

    # ── CARRIL 3 — Vino/Borgona (Martires / Adviento) ────────────────────────
    # X dorada (cruz en diagonal) sobre fondo vino, repite cada 8px
    lx = x - 22
    WD = (0x28, 0x02, 0x10, 255)   # vino oscuro
    WM = (0x58, 0x06, 0x22, 255)   # vino medio
    WL = (0x80, 0x0C, 0x34, 255)   # vino claro
    if lx == 0 or lx == 9: return WD
    if lx == 1 or lx == 8: return GLDK
    ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
    py = y % 8; dy4 = abs(py - 4)
    if py == 0: return GLDK
    # Cruz diagonal (X): donde |dx - dy4| < 0.7
    on_x1 = abs(dx - dy4) < 0.7 and dx <= 2.5
    # Centro de la X
    if on_x1:
        if dx < 0.6: return GLD
        return GLDK
    if dx >= 2.5: return WD
    return WM

def iglesia_pixel(x, y):
    # ── Borde triple: oscuro | oro | oscuro | oro fino | oscuro ──────────────
    if x == 0  or x == 31: return ALP_BORDER
    if x == 1  or x == 30: return ALP_GOLD_DK
    if x == 2  or x == 29: return ALP_BORDER
    if x == 3  or x == 28: return ALP_GOLD
    if x == 4  or x == 27: return ALP_DEEP

    # ── Campo interior x=5..26, ancho=22 ────────────────────────────────────
    ix  = x - 5            # 0..21
    iw  = 22
    mid = iw / 2 - 0.5    # 10.5 — eje central

    # Patron repite cada 16px (tileable en 64)
    py  = y % 16
    dy8 = abs(py - 8)      # distancia al centro vertical del segmento
    dx  = abs(ix - mid)    # distancia al eje central

    # ── Separador horizontal dorado en py==0 ────────────────────────────────
    if py == 0:
        if dx <= 10: return ALP_GOLD_DK
        return ALP_DEEP

    # ── Rombo exterior (marco del medallon) ─────────────────────────────────
    dist = dx + dy8
    if dist == 7: return ALP_GOLD
    if dist == 8: return ALP_GOLD_DK

    # ── Cruz dentro del medallon (solo si dist < 7) ─────────────────────────
    if dist < 7:
        # Brazo vertical de la cruz
        if dx < 1.0 and dy8 <= 4:
            return ALP_GOLD if dy8 == 0 else ALP_GOLD_DK
        # Brazo horizontal de la cruz
        if dy8 == 0 and dx <= 3.5:
            return ALP_GOLD_DK
        # Punta superior/inferior del rombo interior
        if dy8 >= 6 and dx < 1.5:
            return ALP_GOLD_DK
        # Interior del medallon: rojo brillante
        return ALP_BRIGHT

    # ── Espina central fuera del medallon ───────────────────────────────────
    if dx < 1.0: return ALP_DEEP

    # ── Puntos de esquina ornamentales ──────────────────────────────────────
    # Pequeno rombo en cada esquina del campo (cerca de bordes en py~0 o ~16)
    corner_py = min(py, 16 - py)   # 0=borde, 8=centro
    if corner_py <= 2 and dx >= 8:
        if dx + corner_py <= 10: return ALP_GOLD_DK

    # ── Fondo: oscuro en bordes, medio en centro ─────────────────────────────
    if dx >= 9: return ALP_DEEP
    return ALP_MID

def carpet_pixel(x, y):
    # --- Borde L/R: 2px muy oscuro + 1px oro + 1px rojo profundo ---
    if x == 0 or x == 31:  return ALP_BORDER
    if x == 1 or x == 30:  return ALP_BORDER
    if x == 2 or x == 29:  return ALP_GOLD_DK
    if x == 3 or x == 28:  return ALP_DEEP

    # --- Campo interior x=4..27, ancho=24 ---
    ix  = x - 4          # 0..23
    iw  = 24
    mid = iw / 2 - 0.5   # 11.5 — eje central

    # patron que repite cada 16px en Y (tileable en 64)
    py  = y % 16          # 0..15
    dy8 = abs(py - 8)     # distancia a py==8 (centro del rombo)
    dx  = abs(ix - mid)   # distancia al eje central

    # Linea horizontal dorada en py==0 (limite de cada segmento)
    if py == 0:
        if dx <= 9:   return ALP_GOLD_DK
        return ALP_DEEP

    # Rombo dorado: contorno en |dx| + dy8 == 7
    dist = dx + dy8
    if dist == 7:          return ALP_GOLD
    if dist == 8:          return ALP_GOLD_DK

    # Interior del rombo: dist < 7
    if dist < 7:
        # Espina central dentro del rombo
        if dx < 1.0:       return ALP_GOLD_DK
        if dy8 == 0 and dx < 2.0: return ALP_GOLD_DK
        # Punta superior e inferior del rombo
        if dy8 >= 6:       return ALP_BRIGHT
        return ALP_BRIGHT

    # Exterior del rombo
    # Espina central fuera del rombo
    if dx < 1.0:           return ALP_DEEP
    # Esquinas (lejos del rombo)
    if dx >= 9:            return ALP_DEEP
    return ALP_MID

def procesion6_pixel(x, y):
    GLD  = (0xDC, 0xAC, 0x22, 255)
    GLDK = (0xA4, 0x78, 0x10, 255)

    if x == 10 or x == 21:
        return GLD

    # ── CARRIL 1 — TURQUESA (Espiritu Santo / Paloma de la Paz) ────────────────
    # Chevron dorado (Lambda): punta arriba, brazos se abren hacia abajo, cada 8px
    if x <= 9:
        lx = x
        TD = (0x0A, 0x38, 0x44, 255)   # turquesa oscuro
        TM = (0x10, 0x68, 0x7C, 255)   # turquesa medio
        if lx == 0 or lx == 9: return TD
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 8
        if py == 0: return GLDK
        t = (py - 1) / 6.0
        arm_spread = t * 2.5
        left_pos  = mid - arm_spread
        right_pos = mid + arm_spread
        on_gold  = ((abs(ix - left_pos)  < 0.7 and ix <= mid)
                 or (abs(ix - right_pos) < 0.7 and ix >= mid))
        on_shade = ((abs(ix - left_pos)  < 1.3 and ix <= mid)
                 or (abs(ix - right_pos) < 1.3 and ix >= mid))
        if on_gold:  return GLD
        if on_shade: return GLDK
        if dx >= 2.5: return TD
        return TM

    # ── CARRIL 2 — NARANJA QUEMADO (Pentecostes / Fuego del Espiritu Santo) ────
    # Llama dorada ascendente: punta estrecha arriba, base ancha abajo, cada 16px
    if x <= 20:
        lx = x - 11
        OD = (0x5C, 0x24, 0x02, 255)   # naranja oscuro
        OM = (0x9C, 0x48, 0x08, 255)   # naranja medio
        if lx == 0 or lx == 9: return OD
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 16
        if py == 0: return GLDK
        if 2 <= py <= 13:
            t       = (py - 2) / 11.0
            flame_w = t * 2.2
            wobble  = math.sin(py * 0.7) * 0.35
            eff_dx  = abs(ix - mid - wobble)
            if eff_dx <= max(0.1, flame_w * 0.35): return GLD
            if eff_dx <= max(0.3, flame_w):        return GLDK
        if dx >= 2.5: return OD
        return OM

    # ── CARRIL 3 — LAVANDA/LILA (Adviento / Santisima Trinidad) ────────────────
    # Trefoil dorado: 3 circulos que simbolizan la Trinidad, cada 16px
    lx = x - 22
    LD = (0x3C, 0x10, 0x60, 255)   # lavanda oscuro
    LM = (0x68, 0x20, 0xA0, 255)   # lavanda medio
    if lx == 0 or lx == 9: return LD
    if lx == 1 or lx == 8: return GLDK
    ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
    py = y % 16
    if py == 0: return GLDK
    c1 = (ix - mid)**2          + (py - 4)**2
    c2 = (ix - (mid - 1.5))**2 + (py - 11)**2
    c3 = (ix - (mid + 1.5))**2 + (py - 11)**2
    mn = min(c1, c2, c3)
    if mn <= 2.2: return GLD
    if mn <= 4.0: return GLDK
    if abs(ix - mid) < 0.7 and 4 <= py <= 11: return GLDK
    if dx >= 2.5: return LD
    return LM


def procesion7_pixel(x, y):
    GLD  = (0xDC, 0xAC, 0x22, 255)
    GLDK = (0xA4, 0x78, 0x10, 255)

    if x == 10 or x == 21:
        return GLD

    # ── CARRIL 1 — INDIGO PROFUNDO (Misterio Divino / Cielo Nocturno) ──────────
    # Rayos de sol: 8 rayos desde el centro del segmento, cada 16px
    if x <= 9:
        lx = x
        ID = (0x08, 0x06, 0x40, 255)   # indigo oscuro
        IM = (0x14, 0x10, 0x72, 255)   # indigo medio
        if lx == 0 or lx == 9: return ID
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 16
        if py == 0: return GLDK
        rx = ix - mid; ry = py - 8
        dist = math.sqrt(rx * rx + ry * ry)
        if dist < 0.8: return GLD
        angle  = math.atan2(ry, rx)
        sector = angle % (math.pi / 4)
        on_ray = sector < 0.22 or sector > (math.pi / 4 - 0.22)
        if on_ray and dist <= 3.5:
            return GLD if dist < 1.8 else GLDK
        if dx >= 2.5: return ID
        return IM

    # ── CARRIL 2 — BRONCE DORADO (Canonizacion / Corona de Gloria de los Santos)
    # Corona pixel art: 3 puntas + copa + base horizontal, cada 16px
    if x <= 20:
        lx = x - 11
        BD = (0x3C, 0x24, 0x08, 255)   # bronce oscuro
        BM = (0x6C, 0x48, 0x14, 255)   # bronce medio
        if lx == 0 or lx == 9: return BD
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 16
        if py == 0: return GLDK
        if py == 11 and dx <= 2.5: return GLD         # base solida
        if py == 12 and dx <= 2.4: return GLDK
        if 5 <= py <= 10 and dx >= 2.0: return GLDK   # paredes copa
        if dx < 0.7 and 1 <= py <= 4: return GLD      # punta central alta
        if dx < 1.3 and 2 <= py <= 4: return GLDK
        if abs(dx - 2.0) < 0.7 and 3 <= py <= 6: return GLD   # puntas laterales
        if abs(dx - 2.0) < 1.2 and 4 <= py <= 6: return GLDK
        if 5 <= py <= 10 and dx < 2.0: return BM      # interior copa
        if dx >= 2.5: return BD
        return BD

    # ── CARRIL 3 — ROJO PENTECOSTES (Fuego del Espiritu / Sangre de Martires) ──
    # Llama pequena ascendente (diferente de procesion6), cada 8px
    lx = x - 22
    RD = (0x58, 0x08, 0x08, 255)   # rojo oscuro pentecostes
    RM = (0xA0, 0x10, 0x10, 255)   # rojo brillante
    if lx == 0 or lx == 9: return RD
    if lx == 1 or lx == 8: return GLDK
    ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
    py = y % 8
    if py == 0: return GLDK
    if 1 <= py <= 6:
        t       = (py - 1) / 5.0
        flame_w = t * 2.0
        wobble  = math.sin(py * 1.2) * 0.25
        eff_dx  = abs(ix - mid - wobble)
        if eff_dx <= max(0.1, flame_w * 0.40): return GLD
        if eff_dx <= max(0.3, flame_w):        return GLDK
    if dx >= 2.5: return RD
    return RM


def procesion8_pixel(x, y):
    GLD  = (0xDC, 0xAC, 0x22, 255)
    GLDK = (0xA4, 0x78, 0x10, 255)

    if x == 10 or x == 21:
        return GLD

    # ── CARRIL 1 — BLANCO/PLATA (Resurreccion / Gloria Eterna) ────────────────
    # Cruz griega con nimbo (halo circular dorado), cada 16px
    if x <= 9:
        lx = x
        WD = (0x78, 0x78, 0x80, 255)   # gris plata oscuro
        WM = (0xB8, 0xB8, 0xC0, 255)   # plata medio
        WL = (0xE0, 0xE0, 0xE8, 255)   # blanco plateado
        if lx == 0 or lx == 9: return WD
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 16; dy8 = abs(py - 8)
        if py == 0: return GLDK
        dist_c  = math.sqrt(dx * dx + dy8 * dy8)
        on_v    = dx  < 0.7 and dy8 <= 3
        on_h    = dy8 <= 1  and dx  <= 2.5
        on_halo = abs(dist_c - 3.2) < 0.7
        if on_v or on_h: return GLD
        if on_halo:      return GLDK
        if dist_c < 3.2: return WL
        if dx >= 2.5:    return WD
        return WM

    # ── CARRIL 2 — NEGRO SAGRADO (Vigilia Pascual / Alfa y Omega) ─────────────
    # Letra A (comienzo) arriba y arco Omega (fin) abajo, cada 16px
    if x <= 20:
        lx = x - 11
        ND = (0x06, 0x06, 0x0A, 255)   # negro casi puro
        NM = (0x18, 0x16, 0x22, 255)   # negro muy oscuro
        if lx == 0 or lx == 9: return ND
        if lx == 1 or lx == 8: return GLDK
        ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
        py = y % 16
        if py == 0: return GLD          # separador dorado: maximo contraste
        if 1 <= py <= 7:                # ALFA (A): dos lados que convergen
            t_a = (7 - py) / 6.0       # 1=base(py=1), 0=punta(py=7)
            arm = t_a * 2.5
            on_l = abs(ix - (mid - arm)) < 0.7
            on_r = abs(ix - (mid + arm)) < 0.7
            on_b = (py == 4 and abs(ix - mid) <= 1.5)
            if on_l or on_r or on_b: return GLD
            if abs(ix-(mid-arm)) < 1.2 or abs(ix-(mid+arm)) < 1.2: return GLDK
        if 9 <= py <= 15:               # OMEGA: arco superior + base plana
            opy = py - 9
            if opy <= 4:
                dist_o = math.sqrt((ix - mid)**2 + opy**2)
                if abs(dist_o - 2.2) < 0.7: return GLD
                if abs(dist_o - 2.2) < 1.2: return GLDK
            if opy >= 5:
                if dx >= 1.5: return GLD
                if dx >= 0.8: return GLDK
        if dx >= 2.5: return ND
        return NM

    # ── CARRIL 3 — DORADO GLORIOSO (Parousia / Cristo Rey en Gloria) ──────────
    # Enrejado diagonal: barras cruzadas en X (heraldica real), cada 8px
    lx = x - 22
    G3D = (0x6C, 0x4C, 0x08, 255)   # dorado oscuro
    G3M = (0xB0, 0x7C, 0x10, 255)   # dorado medio
    G3L = (0xF0, 0xB8, 0x20, 255)   # dorado brillante
    if lx == 0 or lx == 9: return G3D
    if lx == 1 or lx == 8: return GLD
    ix = lx - 2; mid = 2.5; dx = abs(ix - mid)
    py = y % 8
    if py == 0: return GLD
    d1 = (ix + py) % 4
    d2 = (ix - py + 32) % 4
    if d1 == 0 and d2 == 0: return (0xFF, 0xF0, 0x70, 255)   # nudo: oro puro
    if d1 == 0: return G3L
    if d2 == 0: return GLD
    if dx >= 2.5: return G3D
    return G3M


# ==============================================================================
# RENDER — rectangulo perfecto, todos los pixeles opacos
# ==============================================================================
img = Image.new("RGBA", (W, H), (0, 0, 0, 255))

dispatch = {"lodo": lodo_pixel, "piedra": piedra_pixel, "madera": madera_pixel, "monte": monte_pixel, "ladrillo": ladrillo_pixel, "alfombra": carpet_pixel, "iglesia": iglesia_pixel, "procesion": procesion_pixel, "procesion2": procesion2_pixel, "procesion3": procesion3_pixel, "procesion4": procesion4_pixel, "procesion5": procesion5_pixel, "procesion6": procesion6_pixel, "procesion7": procesion7_pixel, "procesion8": procesion8_pixel}
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
    "monte":     "camino_monte_recto.png",
    "ladrillo":  "camino_ladrillo_recto.png",
    "alfombra":  "camino_alfombra_recto.png",
    "iglesia":   "camino_iglesia_recto.png",
    "procesion":  "camino_procesion_recto.png",
    "procesion2": "camino_procesion2_recto.png",
    "procesion3": "camino_procesion3_recto.png",
    "procesion4": "camino_procesion4_recto.png",
    "procesion5": "camino_procesion5_recto.png",
    "procesion6": "camino_procesion6_recto.png",
    "procesion7": "camino_procesion7_recto.png",
    "procesion8": "camino_procesion8_recto.png",
}
nombre = nombres[TIPO]
dst1 = rf"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\CAMINO\{nombre}"
dst2 = rf"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PNGS\{nombre}"
img.save(dst1)
img.save(dst2)
print(f"[{TIPO} recto] Guardado:\n  {dst1}\n  {dst2}")
