import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageOps

HOMBRES_DIR = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PERSONAJES"
HOMBRE1_DIR = os.path.join(HOMBRES_DIR, "HOMBRE1")
W, H = 18, 25

# ── Paleta universal ──────────────────────────────────────────────────────────
SKIN  = (0xFE, 0xD9, 0x98, 255)
SKNS  = (0xF5, 0xB9, 0x71, 255)
SKND  = (0xD4, 0x94, 0x50, 255)
# Props (iguales al monaguillo)
BEL1  = (0x8C, 0x5C, 0x10, 255)
BEL2  = (0xD4, 0xA0, 0x20, 255)
BEL3  = (0xF0, 0xD0, 0x50, 255)
CND_W = (0xF8, 0xF4, 0xEC, 255)
CND_Y = (0xF0, 0xD0, 0x30, 255)
CND_O = (0xE8, 0x70, 0x10, 255)
THU1  = (0x6C, 0x40, 0x08, 255)
THU2  = (0xAC, 0x70, 0x14, 255)
CRS2  = (0x8C, 0x58, 0x18, 255)
CRSG  = (0xD4, 0xA0, 0x20, 255)

# ==============================================================================
# CONFIGURACION — editar aqui para regenerar F1-F8 de un personaje especifico
# ==============================================================================
NOMBRE_SALIDA = "HOMBRE9"

HAIR_SHADOW = (0x04, 0x28, 0x30, 255)
HAIR_BASE   = (0x08, 0x58, 0x68, 255)
HAIR_LIGHT  = (0x18, 0x9C, 0xB4, 255)

# Flat top — cambia este HAIR_MAP para cada personaje
HAIR_MAP = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # dy0
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy1: tope plano
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy2
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy3
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy4
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy5
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy6
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7 hairline (tapa en x=15)
]

def hair_color(x, dy):
    hard_edge = x <= 1 or x >= 16
    vert_side  = (x <= 2 or x >= 14) and dy >= 2
    soft_edge  = x <= 3 or x >= 14
    if dy >= 6:                    return HAIR_SHADOW
    if hard_edge:                  return HAIR_SHADOW
    if vert_side:                  return HAIR_SHADOW
    if dy >= 4 and soft_edge:      return HAIR_SHADOW
    if dy == 1:                    return HAIR_LIGHT   # tope plano = luz
    return HAIR_BASE

FAJA_MAP = {
    (0xF2,0x31,0x17,255): (0xE8,0x50,0x38,255),
    (0xF2,0x2B,0x13,255): (0xE0,0x48,0x30,255),
    (0xF1,0x32,0x13,255): (0xE4,0x4C,0x34,255),
    (0xD9,0x2B,0x14,255): (0xC4,0x3C,0x28,255),
    (0xAA,0x20,0x0F,255): (0x98,0x2C,0x1C,255),
    (0xC7,0x28,0x12,255): (0xB0,0x36,0x24,255),
    (0xF1,0x32,0x17,255): (0xE8,0x50,0x38,255),
    (0xF2,0x31,0x13,255): (0xE6,0x4E,0x36,255),
}

SHOE_MAP = {
    (0x9B,0x09,0x08,255): (0x60,0x0C,0x28,255),
    (0xF2,0x2B,0x13,255): (0xA8,0x18,0x44,255),
    (0x7B,0x07,0x05,255): (0x4A,0x08,0x1E,255),
    (0xB6,0x10,0x11,255): (0x7C,0x10,0x34,255),
    (0x72,0x07,0x05,255): (0x40,0x06,0x18,255),
    (0x61,0x06,0x04,255): (0x36,0x04,0x14,255),
    (0x70,0x07,0x05,255): (0x3E,0x06,0x1A,255),
    (0x81,0x07,0x05,255): (0x52,0x0A,0x22,255),
    (0x61,0x04,0x04,255): (0x36,0x04,0x14,255),
    (0xAA,0x20,0x0F,255): (0x6E,0x0E,0x2E,255),
}

# ==============================================================================
# DETECCION Y UTILIDADES
# ==============================================================================
def is_hair_src(r, g, b, a):
    """Detecta pelo cafe de HOMBRE1 fuente (para make_hombre)."""
    return a > 0 and 0x1C <= r <= 0x50 and r > g * 1.5 and r > b * 1.8

def is_eye(r, g, b, a):
    return a > 0 and r < 0x35 and g < 0x0C and b < 0x0C

def is_faja(r, g, b, a): return a > 0 and r > 140 and r > g * 3 and g > 20
def is_shoe(r, g, b, a): return a > 0 and r > 60  and r > g * 3 and g <= 20

def is_skin_warm(r, g, b, a):
    return a > 0 and r > 0xC0 and g > 0x70 and b > 0x30 and (r - b) > 40

def is_shifted(img):
    return all(img.getpixel((x, 0))[3] == 0 for x in range(W))

def px(img, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), color)

# ── Detectar 3 tonos de pelo de un frame ya procesado (para back view) ────────
def detect_hair_shades(f1_img):
    hy0 = 1 if is_shifted(f1_img) else 0
    pixels = []
    for dy in range(6):
        y = hy0 + dy
        for x in range(W):
            r, g, b, a = f1_img.getpixel((x, y))
            if a > 0 and not is_skin_warm(r, g, b, a):
                pixels.append((r, g, b, 255))
    if not pixels:
        return (0x28,0x14,0x08,255), (0x4C,0x2C,0x10,255), (0x70,0x48,0x1C,255)
    unique = sorted(set(pixels), key=lambda c: c[0]+c[1]+c[2])
    n = len(unique)
    h1 = unique[max(0, n//10)]
    h2 = unique[n//2]
    h3 = unique[min(n-1, 9*n//10)]
    return h1, h2, h3

# ── Detectar 3 tonos del cuerpo/manga de un frame ya procesado ───────────────
def detect_body_shades(f1_img):
    hy0 = 1 if is_shifted(f1_img) else 0
    samples = []
    for y in range(hy0+15, min(hy0+18, H)):
        for x in range(4, 14):
            r, g, b, a = f1_img.getpixel((x, y))
            if a > 0 and not is_skin_warm(r, g, b, a):
                samples.append((r, g, b, 255))
    if not samples:
        return (0x30,0x30,0x40,255), (0x50,0x50,0x68,255), (0x70,0x70,0x88,255)
    unique = sorted(set(samples), key=lambda c: c[0]+c[1]+c[2])
    n = len(unique)
    s1 = unique[max(0, n//10)]
    s2 = unique[n//2]
    s3 = unique[min(n-1, 9*n//10)]
    return s1, s2, s3

# ==============================================================================
# MAKE_HOMBRE — recolorea HOMBRE1 fuente al NOMBRE_SALIDA configurado
# ==============================================================================
def make_hombre(src_img):
    img = src_img.copy()
    hy0 = 1 if is_shifted(src_img) else 0

    # Guardar ojos antes de borrar pelo
    eye_pixels = {}
    for dy in range(10):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if is_hair_src(r, g, b, a):
                if dy >= 8 and 4 <= x <= 13 and is_eye(r, g, b, a):
                    eye_pixels[(x, y)] = (r, g, b, a)
                img.putpixel((x, y), (0, 0, 0, 0))

    # Nuevo peinado segun HAIR_MAP
    for dy in range(8):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            if HAIR_MAP[dy][x] == 1:
                img.putpixel((x, y), hair_color(x, dy))

    # Patillas
    for dy in range(8, 10):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if is_hair_src(r, g, b, a) and (x <= 3 or x >= 14) and x != 0 and x != 17:
                img.putpixel((x, y), HAIR_SHADOW)

    # Restaurar ojos
    for (x, y), c in eye_pixels.items():
        img.putpixel((x, y), c)

    # Faja y zapatos
    for y in range(H):
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if x == 0 or x == 17: continue  # no recolorear bordes
            if is_shoe(r, g, b, a):
                img.putpixel((x, y), SHOE_MAP.get((r,g,b,a), (0x18,0x10,0x10,255)))
            elif is_faja(r, g, b, a):
                img.putpixel((x, y), FAJA_MAP.get((r,g,b,a), (0xC0,0x58,0x08,255)))

    return img

# ==============================================================================
# GENERADOR DE ANIMACIONES F9-F34 (universal para cualquier personaje)
# ==============================================================================
def gen_animations(dst_dir, f1_img, h1, h2, h3, s1, s2, s3):
    """
    Genera F9-F34 para cualquier hombre.
    f1_img : frame 1 ya procesado (con colores correctos)
    h1/h2/h3: tonos pelo (shadow/base/light)  para back view
    s1/s2/s3: tonos cuerpo/manga (dark/base/light) para gestos
    """

    def slv(x):
        return s1 if (x <= 5 or x >= 12) else (s3 if x in (8, 9) else s2)

    # ── BASE: F1 con brazos limpios ────────────────────────────────────────────
    BASE = f1_img.copy()
    for y in range(15, H):
        for x in range(W):
            r, g, b, a = BASE.getpixel((x, y))
            if a > 0 and is_skin_warm(r, g, b, a):
                BASE.putpixel((x, y), slv(x))

    # ── F9: Orante ─────────────────────────────────────────────────────────────
    f9 = BASE.copy()
    px(f9, 4,15,s2); px(f9, 3,15,s1)
    px(f9, 3,14,s2); px(f9, 2,14,s1)
    px(f9, 2,13,s2); px(f9, 1,13,s1)
    px(f9, 1,12,s2); px(f9, 0,12,s1)
    px(f9, 0,11,SKNS); px(f9, 0,10,SKIN); px(f9, 0,9,SKIN)
    px(f9,13,15,s2); px(f9,14,15,s1)
    px(f9,14,14,s2); px(f9,15,14,s1)
    px(f9,15,13,s2); px(f9,16,13,s1)
    px(f9,16,12,s2); px(f9,17,12,s1)
    px(f9,17,11,SKNS); px(f9,17,10,SKIN); px(f9,17,9,SKIN)
    f9.save(os.path.join(dst_dir,"FRAME9.png"))

    # ── F10: Manos juntas en oracion ───────────────────────────────────────────
    f10 = BASE.copy()
    px(f10, 4,16,s3); px(f10, 5,16,s3)
    px(f10, 4,17,s3); px(f10, 5,17,s2)
    px(f10,13,16,s3); px(f10,12,16,s3)
    px(f10,13,17,s3); px(f10,12,17,s2)
    px(f10, 7,17,SKNS); px(f10, 8,17,SKIN); px(f10, 9,17,SKIN)
    px(f10,10,17,SKIN); px(f10,11,17,SKNS)
    px(f10, 7,18,SKND); px(f10, 8,18,SKNS); px(f10, 9,18,SKNS)
    px(f10,10,18,SKNS); px(f10,11,18,SKND)
    px(f10, 8,19,SKND); px(f10, 9,19,SKND); px(f10,10,19,SKND)
    px(f10, 6,17,s1);   px(f10,12,17,s1)
    f10.save(os.path.join(dst_dir,"FRAME10.png"))

    # ── F11: Campana ───────────────────────────────────────────────────────────
    f11 = BASE.copy()
    px(f11,13,15,s2); px(f11,14,15,s1)
    px(f11,14,14,s2); px(f11,14,13,s1)
    px(f11,15,13,s2); px(f11,15,12,s1)
    px(f11,15,11,s2); px(f11,16,11,s1)
    px(f11,15,10,SKNS); px(f11,16,10,SKIN)
    px(f11,15, 9,SKND); px(f11,16, 9,SKNS)
    px(f11,15, 8,BEL2); px(f11,16, 8,BEL1)
    px(f11,14, 7,BEL1); px(f11,15, 7,BEL3); px(f11,16, 7,BEL2)
    px(f11,13, 6,BEL1); px(f11,14, 6,BEL2); px(f11,15, 6,BEL3)
    px(f11,16, 6,BEL2); px(f11,17, 6,BEL1)
    f11.save(os.path.join(dst_dir,"FRAME11.png"))

    # ── F12: Vela ──────────────────────────────────────────────────────────────
    f12 = BASE.copy()
    px(f12, 8, 7,CND_O)
    px(f12, 7, 8,CND_Y); px(f12, 8, 8,CND_O); px(f12, 9, 8,CND_Y)
    for cy in range(9, 15):
        px(f12, 8, cy, CND_W)
    px(f12, 5,14,s2); px(f12, 4,14,s1)
    px(f12, 6,14,SKNS); px(f12, 7,14,SKIN)
    px(f12, 6,15,SKND); px(f12, 7,15,SKNS)
    px(f12,12,14,s2); px(f12,13,14,s1)
    px(f12,11,14,SKNS); px(f12,10,14,SKIN)
    px(f12,11,15,SKND); px(f12,10,15,SKNS)
    f12.save(os.path.join(dst_dir,"FRAME12.png"))

    # ── F13: Incensario ────────────────────────────────────────────────────────
    f13 = BASE.copy()
    px(f13,13,15,s2); px(f13,14,15,s1)
    px(f13,14,16,s2); px(f13,15,16,s1)
    px(f13,15,17,s2); px(f13,16,17,s1)
    px(f13,15,18,SKNS); px(f13,16,18,SKIN)
    px(f13,15,19,SKND); px(f13,16,19,SKNS)
    px(f13,15,20,THU1); px(f13,16,20,THU1)
    px(f13,14,21,THU1); px(f13,15,21,THU2); px(f13,16,21,THU1)
    px(f13,14,22,THU1); px(f13,15,22,THU2); px(f13,16,22,THU1)
    px(f13,14,23,THU1); px(f13,15,23,THU1); px(f13,16,23,THU1)
    f13.save(os.path.join(dst_dir,"FRAME13.png"))

    # ── F14: Manos extendidas ──────────────────────────────────────────────────
    f14 = BASE.copy()
    px(f14, 3,16,s2); px(f14, 2,16,s1)
    px(f14, 3,17,s1); px(f14, 2,17,s2)
    px(f14, 1,16,SKNS); px(f14, 0,16,SKIN)
    px(f14, 1,17,SKND); px(f14, 0,17,SKNS)
    px(f14,14,16,s2); px(f14,15,16,s1)
    px(f14,14,17,s1); px(f14,15,17,s2)
    px(f14,16,16,SKNS); px(f14,17,16,SKIN)
    px(f14,16,17,SKND); px(f14,17,17,SKNS)
    f14.save(os.path.join(dst_dir,"FRAME14.png"))

    # ── F15: Cruz procesional ──────────────────────────────────────────────────
    f15 = BASE.copy()
    for cy in range(9, 22):
        px(f15, 8, cy, CRS2)
    px(f15, 8, 9,CRSG); px(f15, 8,10,CRSG); px(f15, 8,11,CRSG)
    for cx in range(5, 12):
        px(f15, cx, 10, CRSG)
    px(f15, 5,15,s2); px(f15, 4,15,s1)
    px(f15, 6,15,SKNS); px(f15, 7,15,SKIN)
    px(f15, 6,16,SKND); px(f15, 7,16,SKNS)
    px(f15,12,15,s2); px(f15,13,15,s1)
    px(f15,11,15,SKNS); px(f15,10,15,SKIN)
    px(f15,11,16,SKND); px(f15,10,16,SKNS)
    f15.save(os.path.join(dst_dir,"FRAME15.png"))

    # ── F16-F27: Senal de la Cruz ──────────────────────────────────────────────
    f16 = BASE.copy()
    px(f16,13,15,s3); px(f16,14,15,s1); px(f16,14,14,s2); px(f16,14,13,s1)
    px(f16,14,12,SKNS); px(f16,15,12,SKIN)
    f16.save(os.path.join(dst_dir,"FRAME16.png"))

    f17 = BASE.copy()
    px(f17,13,15,s3); px(f17,14,15,s1); px(f17,14,14,s2)
    px(f17,15,13,s1); px(f17,15,12,s2); px(f17,15,11,s1)
    px(f17,15,10,SKNS); px(f17,16,10,SKIN)
    f17.save(os.path.join(dst_dir,"FRAME17.png"))

    f18 = BASE.copy()
    px(f18,13,15,s3); px(f18,14,15,s1); px(f18,14,14,s2); px(f18,14,13,s1)
    px(f18,15,12,s2); px(f18,15,11,s1); px(f18,16,10,s2)
    px(f18,15, 9,SKNS); px(f18,16, 9,SKIN)
    px(f18,15, 8,SKND); px(f18,16, 8,SKNS)
    f18.save(os.path.join(dst_dir,"FRAME18.png"))

    f19 = BASE.copy()
    px(f19,13,15,s3); px(f19,14,15,s1); px(f19,14,14,s2)
    px(f19,14,13,s1); px(f19,14,12,s2)
    px(f19,14,11,SKNS); px(f19,15,11,SKIN); px(f19,15,10,SKND)
    f19.save(os.path.join(dst_dir,"FRAME19.png"))

    f20 = BASE.copy()
    px(f20,13,15,s3); px(f20,13,16,s2); px(f20,12,16,s1)
    px(f20,11,16,s2);  px(f20,10,16,s1)
    px(f20, 9,15,SKNS); px(f20,10,15,SKIN)
    px(f20, 8,16,SKND); px(f20, 9,16,SKNS); px(f20,10,16,SKIN); px(f20,8,17,s1)
    f20.save(os.path.join(dst_dir,"FRAME20.png"))

    f21 = BASE.copy()
    px(f21,13,15,s2); px(f21,12,16,s1); px(f21,11,16,s2)
    px(f21,10,16,s1);  px(f21, 9,16,s2)
    px(f21, 8,16,SKNS); px(f21, 7,16,SKIN)
    px(f21, 8,15,SKND); px(f21, 7,15,SKNS)
    f21.save(os.path.join(dst_dir,"FRAME21.png"))

    f22 = BASE.copy()
    px(f22,13,16,s2); px(f22,12,16,s1); px(f22,11,16,s2)
    px(f22,10,16,s1); px(f22, 9,16,s2)
    px(f22, 8,16,s1); px(f22, 7,16,s2); px(f22, 6,16,s1)
    px(f22, 5,15,SKNS); px(f22, 4,15,SKIN)
    px(f22, 5,16,SKND); px(f22, 4,16,SKNS)
    f22.save(os.path.join(dst_dir,"FRAME22.png"))

    f23 = BASE.copy()
    px(f23,13,15,s2); px(f23,12,15,s1); px(f23,11,15,s2)
    px(f23,10,15,s1); px(f23, 9,15,s2)
    px(f23, 8,15,SKNS); px(f23, 7,15,SKIN); px(f23, 7,14,SKND)
    f23.save(os.path.join(dst_dir,"FRAME23.png"))

    f24 = BASE.copy()
    px(f24,13,15,s2); px(f24,12,15,s1); px(f24,11,15,s2)
    px(f24,11,14,SKNS); px(f24,10,14,SKIN); px(f24,11,13,SKND)
    f24.save(os.path.join(dst_dir,"FRAME24.png"))

    f25 = BASE.copy()
    px(f25,13,15,s3); px(f25,14,15,s2); px(f25,14,14,s1); px(f25,13,14,s2)
    px(f25,14,13,SKNS); px(f25,15,13,SKIN)
    px(f25,13,13,SKND); px(f25,15,14,SKNS)
    f25.save(os.path.join(dst_dir,"FRAME25.png"))

    f26 = BASE.copy()
    px(f26,13,15,s3); px(f26,13,14,s2); px(f26,12,14,s1); px(f26,12,13,s2)
    px(f26,11,13,SKIN); px(f26,12,13,SKNS); px(f26,11,12,SKND)
    f26.save(os.path.join(dst_dir,"FRAME26.png"))

    f27 = BASE.copy()
    px(f27,13,15,s3); px(f27,12,15,s2); px(f27,12,14,s1)
    px(f27,11,14,s2);  px(f27,11,13,s1); px(f27,10,13,s2)
    px(f27,10,12,SKNS); px(f27, 9,12,SKIN); px(f27,11,12,SKND)
    px(f27, 9,11,SKNS); px(f27,10,11,SKIN)
    f27.save(os.path.join(dst_dir,"FRAME27.png"))

    # ── Back view helper ───────────────────────────────────────────────────────
    hy0 = 1 if is_shifted(f1_img) else 0  # necesario para make_back y cantando
    def make_back(src_img):
        img = ImageOps.mirror(src_img).copy()
        head_px = set()
        for y in range(18):
            for x in range(W):
                if img.getpixel((x, y))[3] > 0:
                    head_px.add((x, y))
        for y in range(18):
            for x in range(W):
                img.putpixel((x, y), (0, 0, 0, 0))
        for (x, y) in head_px:
            if y <= 7:
                if x == 0 or x == 17: continue  # borde extremo transparente
                if x <= 1 or x >= 16:    c = h1
                elif x <= 3 or x >= 14:  c = h2
                else:                    c = h3 if y <= 2 else h2
                img.putpixel((x, y), c)
            elif y <= 11 + hy0:  # nuca: +hy0 cubre fila extra en frames desplazados
                if x == 0 or x == 17: continue  # borde extremo transparente
                img.putpixel((x, y), h1 if (x <= 2 or x >= 15) else h2)
            elif y <= 14:
                if x <= 3 or x >= 14:    c = SKND
                else:                    c = SKNS if y == 12 else SKIN
                img.putpixel((x, y), c)
            else:
                # y15-y17: hombros/cuerpo
                if x == 0 or x == 17: continue
                img.putpixel((x, y), s1 if (x <= 4 or x >= 13) else s2)
        return img

    # F28-F32: caminata espaldas (flip F1-F5)
    for i in range(1, 6):
        p = os.path.join(dst_dir, f"FRAME{i}.png")
        if not os.path.exists(p): continue
        src = Image.open(p).convert("RGBA")
        make_back(src).save(os.path.join(dst_dir, f"FRAME{27+i}.png"))

    # F33: parado espaldas
    make_back(f1_img).save(os.path.join(dst_dir, "FRAME33.png"))

    # F34: sentado espaldas (sin piernas)
    f34 = make_back(f1_img)
    for x in range(W):
        for y in range(19, H):
            f34.putpixel((x, y), (0, 0, 0, 0))
    f34.save(os.path.join(dst_dir, "FRAME34.png"))

    # ── F35: Acostado en cama ──────────────────────────────────────────────────
    CAMA_TPL = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\FRAME9.png"
    if os.path.exists(CAMA_TPL):
        tmpl = Image.open(CAMA_TPL).convert("RGBA")
        f35 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for y in range(H):
            for x in range(W):
                r, g, b, a = tmpl.getpixel((x, y))
                if a == 0:
                    pass  # transparente
                elif is_hair_src(r, g, b, a):
                    if x != 0 and x != 17:  # pelo nunca toca el borde
                        lum = r + g + b
                        c = h1 if lum < 55 else (h3 if lum > 90 else h2)
                        f35.putpixel((x, y), c)
                elif is_faja(r, g, b, a):
                    lum = r + g + b
                    c = s1 if lum < 250 else (s3 if lum > 295 else s2)
                    f35.putpixel((x, y), c)
                else:
                    f35.putpixel((x, y), (r, g, b, a))  # piel y sabana sin cambio
        f35.save(os.path.join(dst_dir, "FRAME35.png"))

    # ── F36-F39: Caminando con Biblia (basados en F1-F4) ─────────────────────
    BK1 = (0x4C, 0x28, 0x08, 255)   # cubierta: lomo oscuro
    BK2 = (0x78, 0x44, 0x14, 255)   # cubierta: borde claro
    BKP = (0xEC, 0xE8, 0xD8, 255)   # paginas
    BKX = (0xC0, 0x60, 0x08, 255)   # cruz dorada
    # Detectar color del zapato del personaje
    _shoe_pix = []
    for _sy in range(21, H):
        for _sx in range(W):
            _r,_g,_b,_a = f1_img.getpixel((_sx, _sy))
            if _a > 0 and not is_skin_warm(_r,_g,_b,_a):
                _shoe_pix.append((_r,_g,_b,255))
    if _shoe_pix:
        _shoe_srt = sorted(set(_shoe_pix), key=lambda c: c[0]+c[1]+c[2])
        SHD = _shoe_srt[0]
        SHM = _shoe_srt[min(len(_shoe_srt)//3, len(_shoe_srt)-1)]
    else:
        SHD, SHM = s1, s2
    def _draw_bible(out):
        px(out,  4,15,s2); px(out,  5,15,s1)
        px(out,  4,16,s2); px(out,  5,16,s1)
        px(out, 13,15,s2); px(out, 12,15,s1)
        px(out, 13,16,s2); px(out, 12,16,s1)
        px(out,  4,17,SKNS); px(out,  4,18,SKND)
        px(out, 13,17,SKNS); px(out, 13,18,SKND)
        # Brazo derecho extendido al lado del libro (igual que HOMBRE1 pintado a mano)
        px(out, 14,16,s1); px(out, 14,17,s1)
        px(out, 14,18,s1); px(out, 14,19,s1)
        # Zapato visible a la derecha del libro
        px(out, 13,20,SHD); px(out, 13,21,SHD)
        for _bx in range(5, 13):
            for _by in range(17, 22):
                if   _bx in (5,12):   _c = BK1
                elif _by in (17,21):  _c = BK1
                elif _bx in (6,11):   _c = BK2
                else:                 _c = BKP
                px(out, _bx, _by, _c)
        px(out, 8,18,BKX); px(out, 8,19,BKX); px(out, 8,20,BKX)
        px(out, 7,19,BKX); px(out, 9,19,BKX)

    # Walk cycle con biblia: F36 (solo F1)
    for _i in range(1, 2):
        _p = os.path.join(dst_dir, f"FRAME{_i}.png")
        if not os.path.exists(_p): continue
        _src = Image.open(_p).convert("RGBA")
        _frm = _src.copy()
        # Borrar brazos oscilantes (piel) → camisa
        for _y in range(15, H):
            for _x in range(W):
                _r, _g, _b, _a = _src.getpixel((_x, _y))
                if _a == 0 or not is_skin_warm(_r, _g, _b, _a): continue
                _frm.putpixel((_x, _y), slv(_x))
        _draw_bible(_frm)
        _frm.save(os.path.join(dst_dir, f"FRAME{35+_i}.png"))
    for _fn in [37, 38, 39]:
        _fp = os.path.join(dst_dir, f"FRAME{_fn}.png")
        if os.path.exists(_fp): os.remove(_fp)

    # ── F44-F45: Cantando (levanta / agacha + boca) ───────────────────────────
    hy0 = 1 if is_shifted(f1_img) else 0
    ym  = hy0 + 11
    MOT = (0x28, 0x10, 0x08, 255)

    def _shift_up(src):
        """Desplaza todo el sprite 1px hacia arriba (simula que se levanta)."""
        out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for _y in range(1, H):
            for _x in range(W):
                out.putpixel((_x, _y - 1), src.getpixel((_x, _y)))
        return out

    def _shift_down(src):
        """Desplaza todo el sprite 1px hacia abajo (simula que se agacha)."""
        out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for _y in range(0, H - 1):
            for _x in range(W):
                out.putpixel((_x, _y + 1), src.getpixel((_x, _y)))
        return out

    # F45: shift up 1px + boca abierta 2px
    f45 = _shift_up(f1_img)
    px(f45, 8, ym,   MOT)
    px(f45, 8, ym-1, MOT)
    f45.save(os.path.join(dst_dir, "FRAME45.png"))

    # F44: igual que F45 + ambos brazos levantados ~45°
    f44 = f45.copy()
    _shy = 14 + hy0  # y del hombro tras shift_up
    for _cy in range(14, H):
        for _cx in range(4):      f44.putpixel((_cx,_cy),(0,0,0,0))
        for _cx in range(14, W): f44.putpixel((_cx,_cy),(0,0,0,0))
    for _cy in range(_shy+2, H):
        for _cx in range(4, 14):
            _r,_g,_b,_a = f44.getpixel((_cx,_cy))
            if _a > 0 and is_skin_warm(_r,_g,_b,_a): f44.putpixel((_cx,_cy),(0,0,0,0))
    # Brazo izquierdo: diagonal limpia x=3→0, y=shy→shy-4
    px(f44, 3,_shy,    s1); px(f44, 2,_shy-1,  s1)
    px(f44, 1,_shy-2,  s2); px(f44, 0,_shy-3,SKNS); px(f44, 0,_shy-4,SKIN)
    # Brazo derecho: diagonal limpia x=14→17, y=shy→shy-4
    px(f44,14,_shy,    s1); px(f44,15,_shy-1,  s1)
    px(f44,16,_shy-2,  s2); px(f44,17,_shy-3,SKNS); px(f44,17,_shy-4,SKIN)
    f44.save(os.path.join(dst_dir, "FRAME44.png"))

    # ── F46-F49: Frames de espaldas adicionales ───────────────────────────────

    # Limpia zonas laterales (artefactos de brazos walk a y=15-21, x=0-3 y x=14-17)
    # y también los artefactos de piel cálida del brazo oscilante en x=4-13, y=18+
    def _limpiar_brazos(img, y0=15, y1=22):
        for _cy in range(y0, y1):
            for _cx in range(4):      img.putpixel((_cx, _cy), (0,0,0,0))
            for _cx in range(14, W): img.putpixel((_cx, _cy), (0,0,0,0))
        for _cy in range(max(y0, 18), y1):
            for _cx in range(4, 14):
                _r,_g,_b,_a = img.getpixel((_cx, _cy))
                if _a > 0 and is_skin_warm(_r,_g,_b,_a):
                    img.putpixel((_cx, _cy), (0,0,0,0))

    # Restaura borde de hombro tras limpiar (x=4 izq, x=13 der)
    def _hombros(img, c1=None, c2=None):
        c1 = c1 or s1; c2 = c2 or s1
        for _cy in range(15, 18):
            px(img,  4, _cy, c1)
            px(img, 13, _cy, c2)

    # F37: Brazos extendidos hacia arriba-afuera (nivel cara) — frente
    f37 = f1_img.copy()
    _limpiar_brazos(f37)
    # Crear hueco visual entre brazo y cara (limpiar x=0-2 y x=15-17 en y=11-14)
    for _cy37 in range(11, 15):
        for _cx37 in range(3):      f37.putpixel((_cx37,_cy37),(0,0,0,0))
        for _cx37 in range(15, W): f37.putpixel((_cx37,_cy37),(0,0,0,0))
    _hombros(f37)
    px(f37, 3,15,s1); px(f37,2,15,s1)
    px(f37, 2,14,s1); px(f37,1,14,s1)
    px(f37, 1,13,s2); px(f37,0,13,s1)
    px(f37, 0,12,SKNS); px(f37,0,11,SKIN)
    px(f37,14,15,s1); px(f37,15,15,s1)
    px(f37,15,14,s1); px(f37,16,14,s1)
    px(f37,16,13,s2); px(f37,17,13,s1)
    px(f37,17,12,SKNS); px(f37,17,11,SKIN)
    f37.save(os.path.join(dst_dir,"FRAME37.png"))

    # F46: eliminado — borrar si existe
    _f46p = os.path.join(dst_dir, "FRAME46.png")
    if os.path.exists(_f46p): os.remove(_f46p)

    # F47: Padre Nuestro de espaldas (brazos horizontales, 2px de ancho)
    f47 = make_back(f1_img)
    _limpiar_brazos(f47)
    _hombros(f47)
    # Brazo izquierdo horizontal — 2 filas de grosor
    px(f47, 3,15,s1); px(f47,2,15,s1); px(f47,1,15,SKNS); px(f47,0,15,SKIN)
    px(f47, 3,16,s1); px(f47,2,16,s1); px(f47,1,16,SKNS); px(f47,0,16,SKND)
    # Brazo derecho horizontal — 2 filas de grosor
    px(f47,14,15,s1); px(f47,15,15,s1); px(f47,16,15,SKNS); px(f47,17,15,SKIN)
    px(f47,14,16,s1); px(f47,15,16,s1); px(f47,16,16,SKNS); px(f47,17,16,SKND)
    f47.save(os.path.join(dst_dir, "FRAME47.png"))

    # F48: Dar la paz de espaldas (brazo derecho diagonal baja, 2px de ancho)
    f48 = make_back(f1_img)
    _limpiar_brazos(f48)
    _hombros(f48)
    # Brazo derecho en diagonal baja — cada paso con 2px de ancho
    px(f48,14,15,s1);  px(f48,15,15,s1)
    px(f48,14,16,s2);  px(f48,15,16,s2);  px(f48,16,16,SKNS)
    px(f48,15,17,s2);  px(f48,16,17,SKNS); px(f48,17,17,SKIN)
    px(f48,16,18,SKNS); px(f48,17,18,SKIN)
    f48.save(os.path.join(dst_dir, "FRAME48.png"))

    # F49: Levantar manos de espaldas (brazos arriba diagonal, 2px de ancho)
    f49 = make_back(f1_img)
    _limpiar_brazos(f49, 9, 22)
    _hombros(f49)
    # Brazo izquierdo diagonal arriba-izquierda — 2px de ancho por paso
    px(f49, 3,15,s1);  px(f49,2,15,s1)
    px(f49, 3,14,s1);  px(f49,2,14,s1)
    px(f49, 2,13,s1);  px(f49,1,13,s2)
    px(f49, 2,12,s1);  px(f49,1,12,s2)
    px(f49, 1,11,s2);  px(f49,0,11,SKNS)
    px(f49, 0,10,SKNS); px(f49,0,9,SKIN)
    # Brazo derecho diagonal arriba-derecha — 2px de ancho por paso
    px(f49,14,15,s1);  px(f49,15,15,s1)
    px(f49,14,14,s1);  px(f49,15,14,s1)
    px(f49,15,13,s1);  px(f49,16,13,s2)
    px(f49,15,12,s1);  px(f49,16,12,s2)
    px(f49,16,11,s2);  px(f49,17,11,SKNS)
    px(f49,17,10,SKNS); px(f49,17,9,SKIN)
    # Restaurar nuca borrada por _limpiar donde el brazo no cubre (y=9-11)
    px(f49, 1,9,h1);  px(f49,2,9,h1);  px(f49,3,9,h2)
    px(f49, 1,10,h1); px(f49,2,10,h1); px(f49,3,10,h2)
    px(f49, 2,11,h1); px(f49,3,11,h2)
    px(f49,14,9,h2);  px(f49,15,9,h1)
    px(f49,14,10,h2); px(f49,15,10,h1)
    px(f49,14,11,h2); px(f49,15,11,h1)
    f49.save(os.path.join(dst_dir, "FRAME49.png"))

# ==============================================================================
# GENERAR NOMBRE_SALIDA desde cero (F1-F8 con make_hombre + F9-F36)
# ==============================================================================
DST = os.path.join(HOMBRES_DIR, NOMBRE_SALIDA)
os.makedirs(DST, exist_ok=True)

print(f"\n=== {NOMBRE_SALIDA} (desde HOMBRE1 fuente) ===")
for i in range(1, 9):
    src = Image.open(os.path.join(HOMBRE1_DIR, f"FRAME{i}.png")).convert("RGBA")
    make_hombre(src).save(os.path.join(DST, f"FRAME{i}.png"))
    print(f"  F{i} walk")

f1_dst = Image.open(os.path.join(DST, "FRAME1.png")).convert("RGBA")
h1, h2, h3 = HAIR_SHADOW, HAIR_BASE, HAIR_LIGHT
s1, s2, s3 = detect_body_shades(f1_dst)
gen_animations(DST, f1_dst, h1, h2, h3, s1, s2, s3)
print(f"  F9-F34 animaciones")
print(f"  Cuerpo detectado: s1={s1[:3]} s2={s2[:3]}")

# ==============================================================================
# BATCH — agregar F9-F34 a todos los demas HOMBRE1-HOMBRE9
# ==============================================================================
TODOS = ["HOMBRE1","HOMBRE2","HOMBRE3","HOMBRE4",
         "HOMBRE5","HOMBRE6","HOMBRE7","HOMBRE8","HOMBRE9"]

for nombre in TODOS:
    if nombre == NOMBRE_SALIDA:
        continue   # ya se genero arriba
    d = os.path.join(HOMBRES_DIR, nombre)
    f1_path = os.path.join(d, "FRAME1.png")
    if not os.path.exists(f1_path):
        print(f"\n{nombre}: sin FRAME1, omitido")
        continue

    print(f"\n=== {nombre} (F9-F34 sobre frames existentes) ===")
    f1 = Image.open(f1_path).convert("RGBA")
    h1b, h2b, h3b = detect_hair_shades(f1)
    s1b, s2b, s3b = detect_body_shades(f1)
    gen_animations(d, f1, h1b, h2b, h3b, s1b, s2b, s3b)
    print(f"  Pelo:  h1={h1b[:3]} h2={h2b[:3]} h3={h3b[:3]}")
    print(f"  Cuerpo: s1={s1b[:3]} s2={s2b[:3]}")
    print(f"  F9-F34 generados")

print(f"""
===============================================================
Generacion completa — 49 frames por personaje
  F1-F8   caminata frente
  F9      orante
  F10     manos juntas
  F11     campana
  F12     vela
  F13     incensario
  F14     manos extendidas
  F15     cruz procesional
  F16-F27 senal de la cruz (12 frames)
  F28-F32 espaldas caminando
  F33     espaldas parado
  F34     espaldas sentado
  F35     acostado en cama
  F36-F39 caminando con Biblia (ciclo walk 4 frames, F1-F4)
  F44     cantando: levanta, 1px boca
  F45     cantando: boca abierta, 2px vertical
  F47     Padre Nuestro de espaldas (brazos horizontales)
  F48     dar la paz de espaldas (brazo derecho)
  F49     levantar manos de espaldas
Personajes procesados: HOMBRE1-HOMBRE9
===============================================================""")

# ==============================================================================
# MUJER1 — mismo generador que HOMBRES, pelo largo y colores femeninos
# ==============================================================================
PERSONAJES_DIR  = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PERSONAJES"
HOMBRE1_SRC_DIR = os.path.join(PERSONAJES_DIR, "HOMBRE1")
MUJER1_DIR      = os.path.join(PERSONAJES_DIR, "MUJER1")
os.makedirs(MUJER1_DIR, exist_ok=True)

# ── Pelo largo mujer: rubio dorado con ondas ─────────────────────────────────
MH1 = (38,  22,  2,   255)   # sombra ámbar oscuro
MH2 = (148, 96,  6,   255)   # dorado cálido
MH3 = (232, 186, 38,  255)   # brillo dorado brillante

# Top dy0-dy7 + bob recto 3px uniforme (corte a la quijada, sin ondas)
HAIR_MAP_MUJER = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # dy0
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy1: tope
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy2
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy3
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy4
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy5
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy6
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7 hairline
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy8:  3px recto
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy9:  3px recto
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy10: 3px recto
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy11: 3px corte nivel (bob)
]

def hair_color_mujer(x, dy):
    # Sin bordes oscuros: solo base (MH2) y brillo (MH3)
    if dy >= 8:                         return MH2   # lados: base dorada uniforme
    if dy <= 2:                         return MH3   # tope: brillo
    if dy <= 5 and 3 <= x <= 14:        return MH3   # copa: brillo
    return MH2

# ── Vestido lavanda — dorado + lavanda es combo clásico femenino ──────────────
FAJA_MAP_M = {
    (0xF2,0x31,0x17,255): (0xA0,0x78,0xC8,255),   # → lila claro
    (0xF2,0x2B,0x13,255): (0x98,0x70,0xC0,255),
    (0xF1,0x32,0x13,255): (0x9C,0x74,0xC4,255),
    (0xD9,0x2B,0x14,255): (0x80,0x58,0xA8,255),   # → lila medio
    (0xAA,0x20,0x0F,255): (0x60,0x40,0x88,255),   # → lila oscuro
    (0xC7,0x28,0x12,255): (0x70,0x4C,0x98,255),
    (0xF1,0x32,0x17,255): (0xA0,0x78,0xC8,255),
    (0xF2,0x31,0x13,255): (0x9E,0x76,0xC6,255),
}

# ── Zapatos violeta oscuro (combina con lavanda) ──────────────────────────────
SHOE_MAP_M = {
    (0x9B,0x09,0x08,255): (0x38,0x10,0x60,255),
    (0xF2,0x2B,0x13,255): (0x5C,0x1A,0x90,255),
    (0x7B,0x07,0x05,255): (0x28,0x0C,0x48,255),
    (0xB6,0x10,0x11,255): (0x48,0x14,0x70,255),
    (0x72,0x07,0x05,255): (0x24,0x0A,0x40,255),
    (0x61,0x06,0x04,255): (0x1C,0x08,0x34,255),
    (0x70,0x07,0x05,255): (0x22,0x0A,0x3E,255),
    (0x81,0x07,0x05,255): (0x2C,0x0E,0x50,255),
    (0x61,0x04,0x04,255): (0x1C,0x08,0x34,255),
    (0xAA,0x20,0x0F,255): (0x44,0x16,0x78,255),
}

def make_mujer(src_img):
    """Recolorea un frame de HOMBRE1 fuente para MUJER1."""
    img = src_img.copy()
    hy0 = 1 if is_shifted(src_img) else 0

    # Guardar ojos SOLO en el centro de la cara (dy=8-12, x=4-13).
    # Los bordes laterales x=0-3 y x=14-17 en dy=8-12 son contorno del pelo,
    # no ojos — tienen colores identicos a is_eye y causaban falsos positivos.
    eye_pixels = {}
    for dy in range(8, 13):
        y = hy0 + dy
        if y >= H: break
        for x in range(4, 14):   # solo interior de la cara
            r, g, b, a = src_img.getpixel((x, y))
            if is_eye(r, g, b, a):
                eye_pixels[(x, y)] = (r, g, b, a)

    # Borrar dy0-15 sin excepciones is_eye — los falsos positivos laterales
    # ya no estan en eye_pixels, se borraran y se redibujara pelo encima.
    for dy in range(16):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if is_skin_warm(r, g, b, a): continue
            img.putpixel((x, y), (0, 0, 0, 0))

    # Dibujar pelo largo segun HAIR_MAP_MUJER
    for dy in range(len(HAIR_MAP_MUJER)):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            if HAIR_MAP_MUJER[dy][x] == 1:
                img.putpixel((x, y), hair_color_mujer(x, dy))

    # Restaurar ojos
    for (x, y), c in eye_pixels.items():
        img.putpixel((x, y), c)

    # Camisa rosa y zapatos vino
    for y in range(H):
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if x == 0 or x == 17: continue
            if is_shoe(r, g, b, a):
                img.putpixel((x, y), SHOE_MAP_M.get((r,g,b,a), (0x40,0x14,0x30,255)))
            elif is_faja(r, g, b, a):
                img.putpixel((x, y), FAJA_MAP_M.get((r,g,b,a), (0xD0,0x60,0x88,255)))

    return img

def make_back_mujer(src_img, s1m, s2m):
    """Vista espaldas MUJER1: bob dorado dibujado con mapa explicito (sin head_px)."""
    img = ImageOps.mirror(src_img).copy()
    hy0 = 1 if is_shifted(src_img) else 0

    # Conservar cuerpo (y >= hy0+13) del frame mirrored para ciclo de caminata
    body_px = {}
    for y in range(hy0 + 13, H):
        for x in range(W):
            c = img.getpixel((x, y))
            if c[3] > 0:
                body_px[(x, y)] = c

    # Limpiar todo y=0..(hy0+13)
    for y in range(hy0 + 14):
        for x in range(W):
            img.putpixel((x, y), (0, 0, 0, 0))

    # Copa (dy0-7): pelo completo en la parte superior de la cabeza
    _BTOP = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # dy0
        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy1
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy2
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy3
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy4
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy5
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy6
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7
    ]
    for dy, row in enumerate(_BTOP):
        y = hy0 + dy
        if y >= H: break
        for x, v in enumerate(row):
            if v:
                c = MH3 if (dy <= 2 and 3 <= x <= 14) else MH2
                img.putpixel((x, y), c)

    # Nuca (dy8-11): pelo cubre toda la nuca del bob
    for dy in range(8, 12):
        y = hy0 + dy
        if y >= H: break
        for x in range(2, 16):
            img.putpixel((x, y), MH2)

    # Linea final del bob (dy12): pelo completo
    y12 = hy0 + 12
    if y12 < H:
        for x in range(2, 16):
            img.putpixel((x, y12), MH2)

    # Restaurar cuerpo con ciclo correcto de caminata
    for (x, y), c in body_px.items():
        img.putpixel((x, y), c)

    return img

# ── Generar F1-F8 MUJER1 ──────────────────────────────────────────────────────
# Limpiar MUJER1_DIR antes de generar
import re as _re
for _f in os.listdir(MUJER1_DIR):
    if _re.match(r'FRAME\d+\.png', _f):
        os.remove(os.path.join(MUJER1_DIR, _f))
print("\n=== MUJER1 (rubio dorado ondulado, vestido lavanda, zapatos violeta) ===")
for i in range(1, 9):
    src = Image.open(os.path.join(HOMBRE1_SRC_DIR, f"FRAME{i}.png")).convert("RGBA")
    make_mujer(src).save(os.path.join(MUJER1_DIR, f"FRAME{i}.png"))
    print(f"  F{i} walk")

f1m = Image.open(os.path.join(MUJER1_DIR, "FRAME1.png")).convert("RGBA")
s1m, s2m, s3m = detect_body_shades(f1m)
gen_animations(MUJER1_DIR, f1m, MH1, MH2, MH3, s1m, s2m, s3m)
print("  F9-F49 animaciones")

# ── Regenerar vistas de espaldas con pelo largo ───────────────────────────────
for i in range(1, 6):
    p = os.path.join(MUJER1_DIR, f"FRAME{i}.png")
    if not os.path.exists(p): continue
    src = Image.open(p).convert("RGBA")
    make_back_mujer(src, s1m, s2m).save(os.path.join(MUJER1_DIR, f"FRAME{27+i}.png"))

make_back_mujer(f1m, s1m, s2m).save(os.path.join(MUJER1_DIR, "FRAME33.png"))

f34m = make_back_mujer(f1m, s1m, s2m)
for x in range(W):
    for y in range(19, H):
        f34m.putpixel((x, y), (0, 0, 0, 0))
f34m.save(os.path.join(MUJER1_DIR, "FRAME34.png"))

print("  F28-F34 espaldas con pelo largo regenerados")

# ── Parche camisa: gen_animations borra pixeles rosa porque is_skin_warm       ──
# ── los detecta como piel (r=240>192, g=120>112, r-b=80>40). Se restauran     ──
# ── los pixeles del torso (x=4-13, y=15-22) desde una BASE sin brazos.        ──
def _slv_m(x):
    return s1m if (x <= 5 or x >= 12) else (s3m if x in (8, 9) else s2m)

# Colores de camisa conocidos — NO borrar aunque pasen is_skin_warm
_SHIRT_RGB = {
    s1m[:3], s2m[:3], s3m[:3],
    (168,60,100),(188,76,116),(206,88,128),
    (240,120,160),(232,108,148),(224,96,136),
    (240,120,160),(236,116,156),(200,80,120),
}

# BASE_MUJER: F1 con brazos convertidos a camisa, respetando colores rosa
_BASE_M = f1m.copy()
for _y in range(15, H):
    for _x in range(W):
        _r,_g,_b,_a = _BASE_M.getpixel((_x,_y))
        if _a > 0 and (_r,_g,_b) not in _SHIRT_RGB and is_skin_warm(_r,_g,_b,_a):
            _BASE_M.putpixel((_x,_y), _slv_m(_x))

def _parchar_camisa(frame_img):
    """Restaura pixeles de camisa faltantes (x=4-13, y=15-22) desde _BASE_M."""
    out = frame_img.copy()
    for _y in range(15, 23):
        for _x in range(4, 14):
            _r,_g,_b,_a = out.getpixel((_x,_y))
            if _a == 0:
                _br,_bg,_bb,_ba = _BASE_M.getpixel((_x,_y))
                if _ba > 0:
                    out.putpixel((_x,_y), (_br,_bg,_bb,_ba))
    return out

for _fn in [37, 44, 45, 47, 48, 49]:
    _fp = os.path.join(MUJER1_DIR, f"FRAME{_fn}.png")
    if not os.path.exists(_fp): continue
    _img = Image.open(_fp).convert("RGBA")
    _parchar_camisa(_img).save(_fp)

print("  F37/44/45/47/48/49 camisa parcheada")

# ── Parche pelo lateral cantando (F44/F45): _shift_up mueve el pelo 1px arriba ──
# Al desplazar, la fila inferior del bob lateral queda transparente. Se rellena ──
# con MH2 solo donde haya transparente, para no tapar la cara/cuerpo.          ──
for _fn_cant in ('FRAME44.png', 'FRAME45.png'):
    _p_cant = os.path.join(MUJER1_DIR, _fn_cant)
    if not os.path.exists(_p_cant): continue
    _img_cant = Image.open(_p_cant).convert('RGBA')
    _hy_cant = 1 if is_shifted(_img_cant) else 0
    # Restaurar lados del bob en dy=8-12 (lado izquierdo x=1,2,3 y derecho x=13,14,15)
    # Reemplaza tanto transparente como piel-artefacto del shift_up
    for _dy_c in range(8, 13):
        _y_c = _hy_cant + _dy_c
        if _y_c >= H: break
        for _xc in (1, 2, 3, 13, 14, 15):
            _cc = _img_cant.getpixel((_xc, _y_c))
            if _cc[3] == 0 or is_skin_warm(_cc[0], _cc[1], _cc[2], _cc[3]):
                _img_cant.putpixel((_xc, _y_c), MH2)
    _img_cant.save(_p_cant)
print("  F44/F45 pelo lateral bob restaurado")

# ── Parche nuca inferior en back-pose frames (F47/F48/F49) ───────────────────
# _limpiar_brazos borra x=0-3 y x=14-17 en y=9-21, destruyendo la fila hy0+11
# que make_back acaba de dibujar. Se restaura con MH2 donde haya transparente.
for _fn_bpose in ('FRAME47.png', 'FRAME48.png', 'FRAME49.png'):
    _p_bpose = os.path.join(MUJER1_DIR, _fn_bpose)
    if not os.path.exists(_p_bpose): continue
    _img_bpose = Image.open(_p_bpose).convert('RGBA')
    _hy_bp = 1 if is_shifted(_img_bpose) else 0
    # Restaurar bordes del pelo en dy=11-13 (nuca última fila + cuello lateral)
    # Reemplaza transparente o piel-artefacto (make_back pinta SKND/SKIN ahí)
    for _dy_bp in (11, 12, 13):
        _y_bp = _hy_bp + _dy_bp
        if _y_bp >= H: break
        for _xb in (2, 3, 14, 15, 16):
            _cb = _img_bpose.getpixel((_xb, _y_bp))
            if _cb[3] == 0 or is_skin_warm(_cb[0], _cb[1], _cb[2], _cb[3]):
                _img_bpose.putpixel((_xb, _y_bp), MH2)
    _img_bpose.save(_p_bpose)
print("  F47/F48/F49 nuca inferior restaurada")

# ── Eliminar TODO rastro de café en zona de pelo (MUJER1) ────────────────────
# Barre y=0-16 de cada frame. Borra cualquier pixel que:
#   - no sea ojo, piel cálida, ni los colores dorados propios de MUJER1
#   - tenga tono rojizo-café (r domina sobre g y b, rango HOMBRE1 original)
# Esto captura MH1, colores originales de HOMBRE1, y cualquier otro café residual.
_cnt_m1_brown = 0
_M1_KEEP = {MH2, MH3}   # colores dorados permitidos (RGBA exacto)
for _fp_m1 in os.listdir(MUJER1_DIR):
    if not _re.match(r'FRAME\d+\.png', _fp_m1): continue
    _fp_full = os.path.join(MUJER1_DIR, _fp_m1)
    _img_b = Image.open(_fp_full).convert("RGBA")
    _changed_b = False
    for _py in range(min(17, H)):
        for _px in range(W):
            _br,_bg,_bb,_ba = _img_b.getpixel((_px, _py))
            if _ba == 0: continue
            if is_skin_warm(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) in _M1_KEEP: continue
            # Conservar ojos solo en zona de cara (y=8-13 aprox)
            if _py >= 8 and _py <= 13 and is_eye(_br,_bg,_bb,_ba): continue
            # Proteger pixel de boca (cantando) — pasa el filtro café pero es intencional
            if (_br,_bg,_bb,_ba) == (0x28, 0x10, 0x08, 255): continue
            # Café oscuro: r domina, g y b bajos
            if 8 <= _br <= 130 and _bg < 65 and _bb < 65 and _br > _bg*1.3 and _br > _bb*1.8:
                # MH1 (sombra ámbar borde de pelo) → reemplazar con MH2 en vez de borrar
                _rep = MH2 if (_br,_bg,_bb,_ba) == MH1 else (0,0,0,0)
                _img_b.putpixel((_px, _py), _rep)
                _cnt_m1_brown += 1
                _changed_b = True
    if _changed_b:
        _img_b.save(_fp_full)
print(f"  Café residual MUJER1 eliminado: {_cnt_m1_brown} pixeles borrados")

# Renombrar secuencialmente (elimina huecos)
_m1files = sorted([_f for _f in os.listdir(MUJER1_DIR) if _re.match(r'FRAME\d+\.png',_f)],
                  key=lambda _f: int(_re.search(r'(\d+)',_f).group(1)))
for _i,_f in enumerate(_m1files):
    os.rename(os.path.join(MUJER1_DIR,_f), os.path.join(MUJER1_DIR,f'_TM1_{_i+1}.png'))
for _i in range(len(_m1files)):
    os.rename(os.path.join(MUJER1_DIR,f'_TM1_{_i+1}.png'), os.path.join(MUJER1_DIR,f'FRAME{_i+1}.png'))

print(f"  Pelo: h1={MH1[:3]} h2={MH2[:3]} h3={MH3[:3]}")
print(f"  Cuerpo: s1={s1m[:3]} s2={s2m[:3]}")
print(f"""
===============================================================
MUJER1 completa — {len(_m1files)} frames secuenciales (FRAME1..FRAME{len(_m1files)})
  Pelo: rubio dorado ondulado (3→2→3→2→1→1 por lado)
  Vestido: lavanda
  Zapatos: violeta oscuro
===============================================================""")

# ==============================================================================
# MUJER2 — pelo loco cobre/cobrizo, vestido magenta brillante
# ==============================================================================
MUJER2_DIR = os.path.join(PERSONAJES_DIR, "MUJER2")
os.makedirs(MUJER2_DIR, exist_ok=True)

# ── Pelo verde esmeralda / teal brillante ────────────────────────────────────
M2H1 = (4,  26,  16,  255)   # sombra verde botella oscuro
M2H2 = (12, 92,  60,  255)   # esmeralda base
M2H3 = (22, 182, 106, 255)   # teal brillante

# Melena larga con capas: copa normal, lados alternan 3px/2px (efecto capas)
# Llega más abajo que MUJER1 — estilo más largo y diferente
HAIR_MAP_MUJER2 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # dy0: limpio
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy1: tope centrado
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy2
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy3
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy4
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy5
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy6
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7 hairline
    # Capas alternadas: 3px (capa exterior) / 2px (capa interior)
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy8:  3px capa exterior
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy9:  2px capa interior
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy10: 3px capa exterior
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy11: 2px capa interior
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy12: 3px capa exterior
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy13: 2px capa interior
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],  # dy14: 1px punta final
]

def hair_color_mujer2(x, dy):
    # Sin bordes oscuros: solo base (M2H2) y brillo (M2H3)
    if dy >= 8:                        return M2H2   # lados: esmeralda base uniforme
    if dy <= 2:                        return M2H3   # tope: teal brillante
    if dy <= 5 and 3 <= x <= 14:       return M2H3   # copa: brillo
    return M2H2

# ── Vestido azul cobalto (contrasta con verde esmeralda) ─────────────────────
FAJA_MAP_M2 = {
    (0xF2,0x31,0x17,255): (0x28,0x88,0xD8,255),  # → azul cobalto brillante
    (0xF2,0x2B,0x13,255): (0x20,0x80,0xD0,255),
    (0xF1,0x32,0x13,255): (0x24,0x84,0xD4,255),
    (0xD9,0x2B,0x14,255): (0x18,0x68,0xB8,255),  # → azul medio
    (0xAA,0x20,0x0F,255): (0x10,0x48,0x90,255),  # → azul oscuro
    (0xC7,0x28,0x12,255): (0x14,0x58,0xA4,255),
    (0xF1,0x32,0x17,255): (0x28,0x88,0xD8,255),
    (0xF2,0x31,0x13,255): (0x26,0x86,0xD6,255),
}

# ── Zapatos azul marino oscuro (combina con cobalto) ─────────────────────────
SHOE_MAP_M2 = {
    (0x9B,0x09,0x08,255): (0x08,0x18,0x48,255),
    (0xF2,0x2B,0x13,255): (0x14,0x30,0x78,255),
    (0x7B,0x07,0x05,255): (0x06,0x10,0x34,255),
    (0xB6,0x10,0x11,255): (0x0C,0x22,0x5C,255),
    (0x72,0x07,0x05,255): (0x06,0x0E,0x30,255),
    (0x61,0x06,0x04,255): (0x04,0x0C,0x28,255),
    (0x70,0x07,0x05,255): (0x06,0x0E,0x2E,255),
    (0x81,0x07,0x05,255): (0x08,0x12,0x3C,255),
    (0x61,0x04,0x04,255): (0x04,0x0C,0x28,255),
    (0xAA,0x20,0x0F,255): (0x10,0x24,0x60,255),
}

def make_mujer2(src_img):
    """Recolorea HOMBRE1 fuente para MUJER2."""
    img = src_img.copy()
    hy0 = 1 if is_shifted(src_img) else 0

    # Guardar ojos SOLO en el centro de la cara (dy=8-12, x=4-13). Mismo razonamiento que make_mujer.
    eye_pixels = {}
    for dy in range(8, 13):
        y = hy0 + dy
        if y >= H: break
        for x in range(4, 14):
            r, g, b, a = src_img.getpixel((x, y))
            if is_eye(r, g, b, a):
                eye_pixels[(x, y)] = (r, g, b, a)

    # Borrar dy0-15 sin excepciones is_eye.
    for dy in range(16):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if is_skin_warm(r, g, b, a): continue
            img.putpixel((x, y), (0, 0, 0, 0))

    # Dibujar pelo loco
    for dy in range(len(HAIR_MAP_MUJER2)):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            if HAIR_MAP_MUJER2[dy][x] == 1:
                img.putpixel((x, y), hair_color_mujer2(x, dy))

    # Restaurar ojos
    for (x, y), c in eye_pixels.items():
        img.putpixel((x, y), c)

    # Vestido magenta y zapatos borgoña
    for y in range(H):
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if x == 0 or x == 17: continue
            if is_shoe(r, g, b, a):
                img.putpixel((x, y), SHOE_MAP_M2.get((r,g,b,a), (0x38,0x08,0x1C,255)))
            elif is_faja(r, g, b, a):
                img.putpixel((x, y), FAJA_MAP_M2.get((r,g,b,a), (0xCC,0x38,0x58,255)))

    return img

def make_back_mujer2(src_img, s1v, s2v):
    """Vista espaldas MUJER2: melena esmeralda larga, mapa explícito sin head_px."""
    img = ImageOps.mirror(src_img).copy()
    hy0 = 1 if is_shifted(src_img) else 0

    # Conservar cuerpo (y >= hy0+12) del frame mirrored para ciclo de caminata
    body_px = {}
    for y in range(hy0 + 12, H):
        for x in range(W):
            c = img.getpixel((x, y))
            if c[3] > 0:
                body_px[(x, y)] = c

    # Limpiar cabeza (y=0..hy0+11)
    for y in range(hy0 + 12):
        for x in range(W):
            img.putpixel((x, y), (0, 0, 0, 0))

    # Copa (dy0-7): pelo completo en parte superior de la cabeza
    _BTOP2 = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # dy0
        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy1
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy2
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy3
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy4
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy5
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy6
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7
    ]
    for dy, row in enumerate(_BTOP2):
        y = hy0 + dy
        if y >= H: break
        for x, v in enumerate(row):
            if v:
                c = M2H3 if (dy <= 2 and 3 <= x <= 14) else M2H2
                img.putpixel((x, y), c)

    # Nuca (dy8-11): pelo cubre toda la nuca — capas alternas dan textura de profundidad
    for dy in range(8, 12):
        y = hy0 + dy
        if y >= H: break
        # Filas pares: borde externo M2H1 (sombra), resto M2H2
        # Filas impares: todo M2H2 (pelo base) — efecto cascada
        for x in range(1, 17):
            if (dy % 2 == 0) and (x <= 1 or x >= 16):
                img.putpixel((x, y), M2H1)  # sombra exterior en filas pares
            else:
                img.putpixel((x, y), M2H2)

    # Restaurar cuerpo con ciclo correcto de caminata
    for (x, y), c in body_px.items():
        img.putpixel((x, y), c)

    # Superponer melena cayendo sobre bordes de la espalda (dy12-17)
    _MELEN_XS = {
        12: list(range(1, 5)) + list(range(13, 17)),
        13: list(range(1, 5)) + list(range(13, 17)),
        14: list(range(1, 4)) + list(range(14, 17)),
        15: list(range(1, 4)) + list(range(14, 17)),
        16: [1, 2, 15, 16],
        17: [1, 2, 15, 16],
    }
    for dy, xs in _MELEN_XS.items():
        y = hy0 + dy
        if y >= H: break
        for x in xs:
            img.putpixel((x, y), M2H2)

    return img

# ── Generar F1-F8 MUJER2 ──────────────────────────────────────────────────────
# Limpiar MUJER2_DIR antes de generar
for _f in os.listdir(MUJER2_DIR):
    if _re.match(r'FRAME\d+\.png', _f):
        os.remove(os.path.join(MUJER2_DIR, _f))
print("\n=== MUJER2 (esmeralda mechones puntiagudos, vestido cobalto) ===")
for i in range(1, 9):
    src = Image.open(os.path.join(HOMBRE1_SRC_DIR, f"FRAME{i}.png")).convert("RGBA")
    make_mujer2(src).save(os.path.join(MUJER2_DIR, f"FRAME{i}.png"))
    print(f"  F{i} walk")

f1m2 = Image.open(os.path.join(MUJER2_DIR, "FRAME1.png")).convert("RGBA")
s1m2, s2m2, s3m2 = detect_body_shades(f1m2)
gen_animations(MUJER2_DIR, f1m2, M2H1, M2H2, M2H3, s1m2, s2m2, s3m2)
print("  F9-F49 animaciones")

# ── Espaldas con pelo largo ancho ─────────────────────────────────────────────
for i in range(1, 6):
    p = os.path.join(MUJER2_DIR, f"FRAME{i}.png")
    if not os.path.exists(p): continue
    src = Image.open(p).convert("RGBA")
    make_back_mujer2(src, s1m2, s2m2).save(os.path.join(MUJER2_DIR, f"FRAME{27+i}.png"))

make_back_mujer2(f1m2, s1m2, s2m2).save(os.path.join(MUJER2_DIR, "FRAME33.png"))

f34m2 = make_back_mujer2(f1m2, s1m2, s2m2)
for x in range(W):
    for y in range(19, H):
        f34m2.putpixel((x, y), (0, 0, 0, 0))
f34m2.save(os.path.join(MUJER2_DIR, "FRAME34.png"))

print("  F28-F34 espaldas regeneradas")

# ── Verificar si el magenta pasa is_skin_warm (si no, no necesita parche) ────
_check = s3m2
_need_patch = is_skin_warm(_check[0], _check[1], _check[2], 255)
if _need_patch:
    _SHIRT2_RGB = {s1m2[:3], s2m2[:3], s3m2[:3]}
    def _slv_m2(x): return s1m2 if (x<=5 or x>=12) else (s3m2 if x in (8,9) else s2m2)
    _BASE_M2 = f1m2.copy()
    for _y in range(15, H):
        for _x in range(W):
            _r,_g,_b,_a = _BASE_M2.getpixel((_x,_y))
            if _a>0 and (_r,_g,_b) not in _SHIRT2_RGB and is_skin_warm(_r,_g,_b,_a):
                _BASE_M2.putpixel((_x,_y), _slv_m2(_x))
    for _fn in [37,44,45,47,48,49]:
        _fp = os.path.join(MUJER2_DIR, f"FRAME{_fn}.png")
        if not os.path.exists(_fp): continue
        _img = Image.open(_fp).convert("RGBA")
        _out = _img.copy()
        for _y in range(15,23):
            for _x in range(4,14):
                if _out.getpixel((_x,_y))[3]==0:
                    _br,_bg,_bb,_ba = _BASE_M2.getpixel((_x,_y))
                    if _ba>0: _out.putpixel((_x,_y),(_br,_bg,_bb,_ba))
        _out.save(_fp)
    print("  Parche camisa aplicado")
else:
    print("  Magenta no interfiere con skin_warm — sin parche necesario")

# ── Parche pelo lateral cantando MUJER2 (F44/F45): mismo problema que MUJER1 ──
for _fn_cant2 in ('FRAME44.png', 'FRAME45.png'):
    _p_cant2 = os.path.join(MUJER2_DIR, _fn_cant2)
    if not os.path.exists(_p_cant2): continue
    _img_cant2 = Image.open(_p_cant2).convert('RGBA')
    _hy_cant2 = 1 if is_shifted(_img_cant2) else 0
    for _dy_c2 in range(8, 13):
        _y_c2 = _hy_cant2 + _dy_c2
        if _y_c2 >= H: break
        for _xc2 in (1, 2, 3, 13, 14, 15):
            _cc2 = _img_cant2.getpixel((_xc2, _y_c2))
            if _cc2[3] == 0 or is_skin_warm(_cc2[0], _cc2[1], _cc2[2], _cc2[3]):
                _img_cant2.putpixel((_xc2, _y_c2), M2H2)
    _img_cant2.save(_p_cant2)
print("  F44/F45 pelo lateral melena restaurado")

# ── Parche nuca inferior back-pose MUJER2 (F47/F48/F49) ──────────────────────
for _fn_bpose2 in ('FRAME47.png', 'FRAME48.png', 'FRAME49.png'):
    _p_bpose2 = os.path.join(MUJER2_DIR, _fn_bpose2)
    if not os.path.exists(_p_bpose2): continue
    _img_bpose2 = Image.open(_p_bpose2).convert('RGBA')
    _hy_bp2 = 1 if is_shifted(_img_bpose2) else 0
    for _dy_bp2 in (11, 12, 13):
        _y_bp2 = _hy_bp2 + _dy_bp2
        if _y_bp2 >= H: break
        for _xb2 in (2, 3, 14, 15, 16):
            _cb2 = _img_bpose2.getpixel((_xb2, _y_bp2))
            if _cb2[3] == 0 or is_skin_warm(_cb2[0], _cb2[1], _cb2[2], _cb2[3]):
                _img_bpose2.putpixel((_xb2, _y_bp2), M2H2)
    _img_bpose2.save(_p_bpose2)
print("  F47/F48/F49 nuca inferior MUJER2 restaurada")

# ── Eliminar TODO rastro de café en zona de pelo (MUJER2) ────────────────────
# Mismo barrido que MUJER1 — protege colores esmeralda propios de MUJER2.
_cnt_m2_brown = 0
_M2_KEEP = {M2H2, M2H3}
for _fp_m2 in os.listdir(MUJER2_DIR):
    if not _re.match(r'FRAME\d+\.png', _fp_m2): continue
    _fp_full2 = os.path.join(MUJER2_DIR, _fp_m2)
    _img_b2 = Image.open(_fp_full2).convert("RGBA")
    _changed_b2 = False
    for _py in range(min(17, H)):
        for _px in range(W):
            _br,_bg,_bb,_ba = _img_b2.getpixel((_px, _py))
            if _ba == 0: continue
            if is_skin_warm(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) in _M2_KEEP: continue
            if _py >= 8 and _py <= 13 and is_eye(_br,_bg,_bb,_ba): continue
            # Proteger pixel de boca (cantando)
            if (_br,_bg,_bb,_ba) == (0x28, 0x10, 0x08, 255): continue
            if 8 <= _br <= 130 and _bg < 65 and _bb < 65 and _br > _bg*1.3 and _br > _bb*1.8:
                _img_b2.putpixel((_px, _py), (0,0,0,0))
                _cnt_m2_brown += 1
                _changed_b2 = True
    if _changed_b2:
        _img_b2.save(_fp_full2)
print(f"  Café residual MUJER2 eliminado: {_cnt_m2_brown} pixeles borrados")

# Renombrar secuencialmente (elimina huecos)
_m2files = sorted([_f for _f in os.listdir(MUJER2_DIR) if _re.match(r'FRAME\d+\.png',_f)],
                  key=lambda _f: int(_re.search(r'(\d+)',_f).group(1)))
for _i,_f in enumerate(_m2files):
    os.rename(os.path.join(MUJER2_DIR,_f), os.path.join(MUJER2_DIR,f'_TM2_{_i+1}.png'))
for _i in range(len(_m2files)):
    os.rename(os.path.join(MUJER2_DIR,f'_TM2_{_i+1}.png'), os.path.join(MUJER2_DIR,f'FRAME{_i+1}.png'))

print(f"  Pelo: h1={M2H1[:3]} h2={M2H2[:3]} h3={M2H3[:3]}")
print(f"  Cuerpo: s1={s1m2[:3]} s2={s2m2[:3]}")
print(f"""
===============================================================
MUJER2 completa — {len(_m2files)} frames secuenciales (FRAME1..FRAME{len(_m2files)})
  Pelo: verde esmeralda/teal mechones puntiagudos (3px→1px→mecha extra)
  Vestido: azul cobalto
  Zapatos: azul marino oscuro
===============================================================""")

# ==============================================================================
# MUJER3 — HOMBRE3 con extension de pelo largo femenino (sin cambiar colores)
# ==============================================================================
HOMBRE3_SRC_DIR = os.path.join(PERSONAJES_DIR, "HOMBRE3")
MUJER3_DIR      = os.path.join(PERSONAJES_DIR, "MUJER3")
os.makedirs(MUJER3_DIR, exist_ok=True)

# Extension lateral frente: solo en pixels transparentes a los lados
HAIR_EXT_MAP = [
    #  x: 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy8: 3px cada lado
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy9
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy10
    [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy11: 2px
    [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy12
    [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy13
    [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy14
    [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy15
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],  # dy16: 1px
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],  # dy17
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # dy18: punta izquierda
]

def make_mujer3(src_img, h1, h2):
    """MUJER3: copia HOMBRE3 + extiende pelo en pixels transparentes laterales."""
    img = src_img.copy()
    hy0 = 1 if is_shifted(src_img) else 0
    for i, row in enumerate(HAIR_EXT_MAP):
        y = hy0 + 8 + i
        if y >= H: break
        for x in range(W):
            if row[x] == 1 and img.getpixel((x, y))[3] == 0:
                c = h1 if (x <= 2 or x >= 14) else h2
                img.putpixel((x, y), c)
    return img

def add_back_hair_ext(back_img, h1, h2):
    """Superpone franja de pelo largo en bordes del back frame generado por gen_animations.
    Se pinta incondicionalmente (overlay) — el pelo cae sobre la ropa desde la espalda.

    make_back() dibuja SKND en bordes de y=12-14 en coordenadas ABSOLUTAS.
    Para frames desplazados (hy0=1) tambien parchamos las posiciones relativas (hy0+12..17).
    """
    img = back_img.copy()
    hy0 = 1 if is_shifted(img) else 0

    # Pelo cubre la cabeza y cae sobre la camisa:
    #   y=12 → todo cubierto (sin piel)
    #   y=13 → piel solo en x=8 (1px centro)
    #   y=14 → piel en x=7-9 (3px centro)
    #   y=15-17 (camisa) → pelo invade el centro en forma de V invertida
    #     para que se vea que el pelo cae sobre la ropa
    ROW_XS = {
        12: list(range(1, 17)),                            # todo cubierto
        13: [1,2,3,4,5,6,7,9,10,11,12,13,14,15,16],       # deja x=8
        14: [1,2,3,4,5,6,10,11,12,13,14,15,16],            # deja x=7-9
        15: [1,2,3,4, 5,11, 12,13,14,15,16],               # +x=5,11 sobre camisa
        16: [1,2,3,4, 5,6,10,11, 12,13,14,15,16],          # +x=5-6,10-11
        17: [1,2,3,4, 5,6,7,9,10,11, 12,13,14,15,16],      # +x=5-7,9-11
        18: [1],
    }

    # Paso 1: parche absoluto (make_back dibuja en coordenadas absolutas)
    for ay, xs in ROW_XS.items():
        if ay >= H: break
        for x in xs:
            img.putpixel((x, ay), h1)

    # Paso 2: parche relativo (frames desplazados hy0=1 → aplica un row mas abajo)
    for dy, xs in ROW_XS.items():
        y = hy0 + dy
        if y >= H: break
        for x in xs:
            img.putpixel((x, y), h1)
    return img

# ── Generar MUJER3 ────────────────────────────────────────────────────────────
print("\n=== MUJER3 (HOMBRE3 + extension pelo largo femenino) ===")

# Limpiar directorio para evitar residuos de runs anteriores
import re as _re
for _f in os.listdir(MUJER3_DIR):
    if _re.match(r'FRAME\d+\.png', _f):
        os.remove(os.path.join(MUJER3_DIR, _f))

# Detectar colores de pelo de HOMBRE3 FRAME1
_h3src = Image.open(os.path.join(HOMBRE3_SRC_DIR, "FRAME1.png")).convert("RGBA")
h3m1, h3m2, h3m3 = detect_hair_shades(_h3src)

for i in range(1, 9):
    src = Image.open(os.path.join(HOMBRE3_SRC_DIR, f"FRAME{i}.png")).convert("RGBA")
    make_mujer3(src, h3m1, h3m2).save(os.path.join(MUJER3_DIR, f"FRAME{i}.png"))
    print(f"  F{i} walk")

f1m3 = Image.open(os.path.join(MUJER3_DIR, "FRAME1.png")).convert("RGBA")
s1m3, s2m3, s3m3 = detect_body_shades(f1m3)
gen_animations(MUJER3_DIR, f1m3, h3m1, h3m2, h3m3, s1m3, s2m3, s3m3)
print("  F9-F49 animaciones")

# Agregar extension de pelo a TODOS los back frames (F28-34 walk + F47-49 poses)
for fn in [28, 29, 30, 31, 32, 33, 34, 47, 48, 49]:
    p = os.path.join(MUJER3_DIR, f"FRAME{fn}.png")
    if not os.path.exists(p): continue
    src = Image.open(p).convert("RGBA")
    add_back_hair_ext(src, h3m1, h3m2).save(p)
print("  F28-F34 + F47-F49 extension pelo espalda aplicada")

# Parche F37 (manos extendidas): limpiar pelo x=3 y x=13 en y=8-14 que confunde brazos
_p37 = os.path.join(MUJER3_DIR, "FRAME37.png")
if os.path.exists(_p37):
    _f37 = Image.open(_p37).convert("RGBA")
    _hy37 = 1 if is_shifted(_f37) else 0
    for _cy in range(_hy37 + 8, _hy37 + 15):
        for _cx in [3, 13]:
            _cr,_cg,_cb,_ca = _f37.getpixel((_cx, _cy))
            # Solo limpiar pelo — NO limpiar piel (cara) ni transparente
            if _ca > 0 and not is_skin_warm(_cr,_cg,_cb,_ca):
                _f37.putpixel((_cx, _cy), (0,0,0,0))
    _f37.save(_p37)
    print("  F37 pelo interferente en x=3/x=13 limpiado")

# Parche F44 (cantando-raise): brazo derecho 2px de ancho en vez de 1px
_p44 = os.path.join(MUJER3_DIR, "FRAME44.png")
if os.path.exists(_p44):
    _f44 = Image.open(_p44).convert("RGBA")
    _hy = 1 if is_shifted(_f44) else 0
    def _px44(x, y, c): _f44.putpixel((x, _hy+y), c)
    _px44(13, 14, s1m3); _px44(14, 13, s1m3); _px44(15, 12, s2m3)
    _f44.save(_p44)
    print("  F44 brazo derecho ensanchado a 2px")

# Renombrar secuencialmente (elimina huecos F36,F37,F44... → F35,F36,F37...)
_m3files = sorted([_f for _f in os.listdir(MUJER3_DIR) if _re.match(r'FRAME\d+\.png',_f)],
                  key=lambda _f: int(_re.search(r'(\d+)',_f).group(1)))
for _i,_f in enumerate(_m3files):
    os.rename(os.path.join(MUJER3_DIR,_f), os.path.join(MUJER3_DIR,f'_TM3_{_i+1}.png'))
for _i in range(len(_m3files)):
    os.rename(os.path.join(MUJER3_DIR,f'_TM3_{_i+1}.png'), os.path.join(MUJER3_DIR,f'FRAME{_i+1}.png'))

print(f"  Pelo: h1={h3m1[:3]} h2={h3m2[:3]} h3={h3m3[:3]}")
print(f"  Cuerpo: s1={s1m3[:3]} s2={s2m3[:3]}")
print(f"""
===============================================================
MUJER3 completa — {len(_m3files)} frames secuenciales (FRAME1..FRAME{len(_m3files)})
  Base: HOMBRE3 (pelo, camisa y zapatos originales sin cambios)
  Extension pelo: 3px(dy8-10) → 2px(dy11-15) → 1px(dy16-18)
  Back: stub piel x=13-16 cubierto por pelo (y=12-14)
===============================================================""")

# ==============================================================================
# MUJER4 — Trenzas dobles rojo carmesí, vestido turquesa, zapatos jade oscuro
# ==============================================================================
MUJER4_DIR = os.path.join(PERSONAJES_DIR, "MUJER4")
os.makedirs(MUJER4_DIR, exist_ok=True)

# ── Pelo rojo carmesí — todos con r>130, fuera del rango del barrido café ────
M4H1 = (150,  20,  10, 255)   # sombra rojo oscuro
M4H2 = (215,  50,  25, 255)   # rojo carmesí base
M4H3 = (255, 128,  72, 255)   # coral brillante (highlight)

# Copa dy0-7: cobertura completa de la cabeza
# Lados dy8-14: trenzas dobles — alternan 3px/2px por lado
HAIR_MAP_MUJER4 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # dy0
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy1: tope
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy2
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy3
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy4
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy5
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy6
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7 hairline
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy8:  3px trenza gruesa
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy9:  2px trenza delgada
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy10: 3px trenza gruesa
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy11: 2px trenza delgada
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy12: 3px trenza gruesa
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy13: tapeando 2px
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],  # dy14: punta 1px
]

def hair_color_mujer4(x, dy):
    if dy >= 8:                        return M4H2   # trenzas: carmesí base
    if dy <= 2:                        return M4H3   # tope: coral brillante
    if dy <= 5 and 3 <= x <= 14:       return M4H3   # copa: brillo
    return M4H2

# ── Vestido turquesa (contrasta con rojo carmesí) ─────────────────────────────
FAJA_MAP_M4 = {
    (0xF2,0x31,0x17,255): (0x10,0xC0,0x98,255),   # → turquesa brillante
    (0xF2,0x2B,0x13,255): (0x0C,0xB8,0x90,255),
    (0xF1,0x32,0x13,255): (0x0E,0xBC,0x94,255),
    (0xD9,0x2B,0x14,255): (0x08,0x98,0x78,255),   # → turquesa medio
    (0xAA,0x20,0x0F,255): (0x04,0x68,0x50,255),   # → turquesa oscuro
    (0xC7,0x28,0x12,255): (0x06,0x80,0x64,255),
    (0xF1,0x32,0x17,255): (0x10,0xC0,0x98,255),
    (0xF2,0x31,0x13,255): (0x0F,0xBE,0x96,255),
}

# ── Zapatos jade oscuro (combina con turquesa) ────────────────────────────────
SHOE_MAP_M4 = {
    (0x9B,0x09,0x08,255): (0x04,0x38,0x28,255),
    (0xF2,0x2B,0x13,255): (0x08,0x58,0x40,255),
    (0x7B,0x07,0x05,255): (0x04,0x28,0x1C,255),
    (0xB6,0x10,0x11,255): (0x06,0x48,0x34,255),
    (0x72,0x07,0x05,255): (0x04,0x24,0x18,255),
    (0x61,0x06,0x04,255): (0x02,0x1C,0x14,255),
    (0x70,0x07,0x05,255): (0x04,0x22,0x18,255),
    (0x81,0x07,0x05,255): (0x04,0x2C,0x20,255),
    (0x61,0x04,0x04,255): (0x02,0x1C,0x14,255),
    (0xAA,0x20,0x0F,255): (0x06,0x44,0x30,255),
}

def make_mujer4(src_img):
    """Recolorea HOMBRE1 fuente para MUJER4 (trenzas dobles carmesí)."""
    img = src_img.copy()
    hy0 = 1 if is_shifted(src_img) else 0

    # Guardar ojos SOLO en centro de la cara (dy=8-12, x=4-13)
    eye_pixels = {}
    for dy in range(8, 13):
        y = hy0 + dy
        if y >= H: break
        for x in range(4, 14):
            r, g, b, a = src_img.getpixel((x, y))
            if is_eye(r, g, b, a):
                eye_pixels[(x, y)] = (r, g, b, a)

    # Borrar dy0-15 (pelo original y otros no-piel)
    for dy in range(16):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if is_skin_warm(r, g, b, a): continue
            img.putpixel((x, y), (0, 0, 0, 0))

    # Dibujar trenzas dobles según HAIR_MAP_MUJER4
    for dy in range(len(HAIR_MAP_MUJER4)):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            if HAIR_MAP_MUJER4[dy][x] == 1:
                img.putpixel((x, y), hair_color_mujer4(x, dy))

    # Restaurar ojos
    for (x, y), c in eye_pixels.items():
        img.putpixel((x, y), c)

    # Vestido turquesa y zapatos jade
    for y in range(H):
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if x == 0 or x == 17: continue
            if is_shoe(r, g, b, a):
                img.putpixel((x, y), SHOE_MAP_M4.get((r,g,b,a), (0x04,0x50,0x3C,255)))
            elif is_faja(r, g, b, a):
                img.putpixel((x, y), FAJA_MAP_M4.get((r,g,b,a), (0x10,0xC0,0x98,255)))

    return img

def make_back_mujer4(src_img, s1v, s2v):
    """Vista espaldas MUJER4: trenzas carmesí, mapa explícito sin head_px."""
    img = ImageOps.mirror(src_img).copy()
    hy0 = 1 if is_shifted(src_img) else 0

    # Conservar cuerpo (y >= hy0+12) del frame mirrored
    body_px = {}
    for y in range(hy0 + 12, H):
        for x in range(W):
            c = img.getpixel((x, y))
            if c[3] > 0:
                body_px[(x, y)] = c

    # Limpiar cabeza (y=0..hy0+11)
    for y in range(hy0 + 12):
        for x in range(W):
            img.putpixel((x, y), (0, 0, 0, 0))

    # Copa (dy0-7): pelo completo parte superior
    _BTOP4 = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # dy0
        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy1
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy2
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy3
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy4
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy5
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy6
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7
    ]
    for dy, row in enumerate(_BTOP4):
        y = hy0 + dy
        if y >= H: break
        for x, v in enumerate(row):
            if v:
                c = M4H3 if (dy <= 2 and 3 <= x <= 14) else M4H2
                img.putpixel((x, y), c)

    # Nuca (dy8-11): pelo cubre toda la nuca — fila par borde M4H1, resto M4H2
    for dy in range(8, 12):
        y = hy0 + dy
        if y >= H: break
        for x in range(1, 17):
            if (dy % 2 == 0) and (x <= 1 or x >= 16):
                img.putpixel((x, y), M4H1)
            else:
                img.putpixel((x, y), M4H2)

    # Restaurar cuerpo
    for (x, y), c in body_px.items():
        img.putpixel((x, y), c)

    # Trenzas cayendo (dy12-17): dos tiras estrechas a cada lado
    _TRENZA_XS = {
        12: list(range(1, 4)) + list(range(13, 16)),   # 3px cada lado
        13: list(range(1, 4)) + list(range(13, 16)),
        14: list(range(1, 3)) + list(range(14, 16)),   # 2px
        15: list(range(1, 3)) + list(range(14, 16)),
        16: [1, 15],                                    # 1px punta
        17: [1, 15],
    }
    for dy, xs in _TRENZA_XS.items():
        y = hy0 + dy
        if y >= H: break
        for x in xs:
            img.putpixel((x, y), M4H2)

    return img

# ── Generar F1-F8 MUJER4 ──────────────────────────────────────────────────────
for _f in os.listdir(MUJER4_DIR):
    if _re.match(r'FRAME\d+\.png', _f):
        os.remove(os.path.join(MUJER4_DIR, _f))
print("\n=== MUJER4 (trenzas dobles carmesí, vestido turquesa, zapatos jade) ===")
for i in range(1, 9):
    src = Image.open(os.path.join(HOMBRE1_SRC_DIR, f"FRAME{i}.png")).convert("RGBA")
    make_mujer4(src).save(os.path.join(MUJER4_DIR, f"FRAME{i}.png"))
    print(f"  F{i} walk")

f1m4 = Image.open(os.path.join(MUJER4_DIR, "FRAME1.png")).convert("RGBA")
s1m4, s2m4, s3m4 = detect_body_shades(f1m4)
gen_animations(MUJER4_DIR, f1m4, M4H1, M4H2, M4H3, s1m4, s2m4, s3m4)
print("  F9-F49 animaciones")

# ── Regenerar vistas de espaldas con trenzas dobles ──────────────────────────
for i in range(1, 6):
    p = os.path.join(MUJER4_DIR, f"FRAME{i}.png")
    if not os.path.exists(p): continue
    src = Image.open(p).convert("RGBA")
    make_back_mujer4(src, s1m4, s2m4).save(os.path.join(MUJER4_DIR, f"FRAME{27+i}.png"))

make_back_mujer4(f1m4, s1m4, s2m4).save(os.path.join(MUJER4_DIR, "FRAME33.png"))

f34m4 = make_back_mujer4(f1m4, s1m4, s2m4)
for x in range(W):
    for y in range(19, H):
        f34m4.putpixel((x, y), (0, 0, 0, 0))
f34m4.save(os.path.join(MUJER4_DIR, "FRAME34.png"))

print("  F28-F34 espaldas con trenzas regeneradas")

# ── Parche pelo lateral cantando (F44/F45): trenzas laterales después del shift ──
for _fn_cant4 in ('FRAME44.png', 'FRAME45.png'):
    _p_cant4 = os.path.join(MUJER4_DIR, _fn_cant4)
    if not os.path.exists(_p_cant4): continue
    _img_cant4 = Image.open(_p_cant4).convert('RGBA')
    _hy_cant4 = 1 if is_shifted(_img_cant4) else 0
    for _dy_c4 in range(8, 13):
        _y_c4 = _hy_cant4 + _dy_c4
        if _y_c4 >= H: break
        for _xc4 in (1, 2, 3, 13, 14, 15):
            _cc4 = _img_cant4.getpixel((_xc4, _y_c4))
            if _cc4[3] == 0 or is_skin_warm(_cc4[0], _cc4[1], _cc4[2], _cc4[3]):
                _img_cant4.putpixel((_xc4, _y_c4), M4H2)
    _img_cant4.save(_p_cant4)
print("  F44/F45 pelo lateral trenzas restaurado")

# ── Parche nuca inferior back-pose (F47/F48/F49) ─────────────────────────────
for _fn_bpose4 in ('FRAME47.png', 'FRAME48.png', 'FRAME49.png'):
    _p_bpose4 = os.path.join(MUJER4_DIR, _fn_bpose4)
    if not os.path.exists(_p_bpose4): continue
    _img_bpose4 = Image.open(_p_bpose4).convert('RGBA')
    _hy_bp4 = 1 if is_shifted(_img_bpose4) else 0
    for _dy_bp4 in (11, 12, 13):
        _y_bp4 = _hy_bp4 + _dy_bp4
        if _y_bp4 >= H: break
        for _xb4 in (2, 3, 14, 15, 16):
            _cb4 = _img_bpose4.getpixel((_xb4, _y_bp4))
            if _cb4[3] == 0 or is_skin_warm(_cb4[0], _cb4[1], _cb4[2], _cb4[3]):
                _img_bpose4.putpixel((_xb4, _y_bp4), M4H2)
    _img_bpose4.save(_p_bpose4)
print("  F47/F48/F49 nuca inferior MUJER4 restaurada")

# ── Eliminar rastro de café en zona de pelo (MUJER4) ─────────────────────────
# M4H1/M4H2/M4H3 tienen r>130, fuera del rango brownish (8-130). Son seguros.
# El barrido borra solo residuos del pelo original de HOMBRE1.
_cnt_m4_brown = 0
_M4_KEEP = {M4H1, M4H2, M4H3}
for _fp_m4 in os.listdir(MUJER4_DIR):
    if not _re.match(r'FRAME\d+\.png', _fp_m4): continue
    _fp_full4 = os.path.join(MUJER4_DIR, _fp_m4)
    _img_b4 = Image.open(_fp_full4).convert("RGBA")
    _changed_b4 = False
    for _py in range(min(17, H)):
        for _px in range(W):
            _br,_bg,_bb,_ba = _img_b4.getpixel((_px, _py))
            if _ba == 0: continue
            if is_skin_warm(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) in _M4_KEEP: continue
            if _py >= 8 and _py <= 13 and is_eye(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) == (0x28, 0x10, 0x08, 255): continue
            if 8 <= _br <= 130 and _bg < 65 and _bb < 65 and _br > _bg*1.3 and _br > _bb*1.8:
                _img_b4.putpixel((_px, _py), (0,0,0,0))
                _cnt_m4_brown += 1
                _changed_b4 = True
    if _changed_b4:
        _img_b4.save(_fp_full4)
print(f"  Café residual MUJER4 eliminado: {_cnt_m4_brown} pixeles borrados")

# Renombrar secuencialmente (elimina huecos)
_m4files = sorted([_f for _f in os.listdir(MUJER4_DIR) if _re.match(r'FRAME\d+\.png',_f)],
                  key=lambda _f: int(_re.search(r'(\d+)',_f).group(1)))
for _i,_f in enumerate(_m4files):
    os.rename(os.path.join(MUJER4_DIR,_f), os.path.join(MUJER4_DIR,f'_TM4_{_i+1}.png'))
for _i in range(len(_m4files)):
    os.rename(os.path.join(MUJER4_DIR,f'_TM4_{_i+1}.png'), os.path.join(MUJER4_DIR,f'FRAME{_i+1}.png'))

print(f"  Pelo: h1={M4H1[:3]} h2={M4H2[:3]} h3={M4H3[:3]}")
print(f"  Cuerpo: s1={s1m4[:3]} s2={s2m4[:3]}")
print(f"""
===============================================================
MUJER4 completa — {len(_m4files)} frames secuenciales (FRAME1..FRAME{len(_m4files)})
  Pelo: trenzas dobles rojo carmesí (3px→2px alternado, punta 1px)
  Vestido: turquesa brillante
  Zapatos: jade oscuro
===============================================================""")

# ==============================================================================
# MUJER5 — Ondas largas azul zafiro, copa voluminosa, vestido dorado, zapatos café
# ==============================================================================
MUJER5_DIR = os.path.join(PERSONAJES_DIR, "MUJER5")
os.makedirs(MUJER5_DIR, exist_ok=True)

# ── Pelo azul zafiro — todos fuera del rango brownish (r<8 o g>65 o b>65) ────
M5H1 = (  5,  10,  55, 255)   # índigo muy oscuro  (r=5 < 8 → fuera del rango)
M5H2 = ( 35,  70, 175, 255)   # azul zafiro base   (g=70 > 65 → no atrapado)
M5H3 = ( 90, 150, 245, 255)   # azul cielo highlight (g=150 → no atrapado)

# Copa dy0-7: más estrecha en el tope (silueta recogida / media cola)
#             se ensancha en dy4-5 dando volumen lateral extra (incluye x=16)
# Lados dy8-15: ondas alternas 3px/4px → más anchas que MUJER2 (3px/2px)
HAIR_MAP_MUJER5 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # dy0
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy1: tope estrecho (media cola)
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy2
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy3
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy4: ancho máximo (volumen)
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy5: ancho máximo
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy6
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7 hairline
    # Ondas alternas 3px / 4px — más anchas que MUJER2
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy8:  3px por lado
    [0,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0],  # dy9:  4px onda exterior
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy10: 3px
    [0,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0],  # dy11: 4px onda
    [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # dy12: 3px
    [0,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0],  # dy13: 4px onda
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0],  # dy14: 2px taper
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],  # dy15: 1px punta
]

def hair_color_mujer5(x, dy):
    if dy >= 8:                        return M5H2   # ondas: zafiro base
    if dy <= 1:                        return M5H3   # tope estrecho: highlight
    if dy <= 5 and 2 <= x <= 15:       return M5H3   # copa ancha: brillo
    return M5H2

# ── Vestido dorado ámbar (contrasta con azul zafiro) ─────────────────────────
FAJA_MAP_M5 = {
    (0xF2,0x31,0x17,255): (0xE8,0xA0,0x10,255),   # → dorado brillante
    (0xF2,0x2B,0x13,255): (0xE0,0x98,0x0C,255),
    (0xF1,0x32,0x13,255): (0xE4,0x9C,0x0E,255),
    (0xD9,0x2B,0x14,255): (0xC8,0x84,0x08,255),   # → ámbar medio
    (0xAA,0x20,0x0F,255): (0xA0,0x68,0x06,255),   # → ámbar oscuro
    (0xC7,0x28,0x12,255): (0xB4,0x76,0x07,255),
    (0xF1,0x32,0x17,255): (0xE8,0xA0,0x10,255),
    (0xF2,0x31,0x13,255): (0xE6,0x9E,0x0F,255),
}

# ── Zapatos marrón chocolate oscuro ──────────────────────────────────────────
SHOE_MAP_M5 = {
    (0x9B,0x09,0x08,255): (0x48,0x22,0x08,255),
    (0xF2,0x2B,0x13,255): (0x78,0x3C,0x10,255),
    (0x7B,0x07,0x05,255): (0x38,0x1A,0x06,255),
    (0xB6,0x10,0x11,255): (0x5C,0x2C,0x0C,255),
    (0x72,0x07,0x05,255): (0x34,0x18,0x06,255),
    (0x61,0x06,0x04,255): (0x2C,0x14,0x04,255),
    (0x70,0x07,0x05,255): (0x32,0x18,0x06,255),
    (0x81,0x07,0x05,255): (0x3C,0x1C,0x08,255),
    (0x61,0x04,0x04,255): (0x2C,0x14,0x04,255),
    (0xAA,0x20,0x0F,255): (0x54,0x28,0x0A,255),
}

def make_mujer5(src_img):
    """Recolorea HOMBRE1 fuente para MUJER5 (ondas azul zafiro, copa voluminosa)."""
    img = src_img.copy()
    hy0 = 1 if is_shifted(src_img) else 0

    eye_pixels = {}
    for dy in range(8, 13):
        y = hy0 + dy
        if y >= H: break
        for x in range(4, 14):
            r, g, b, a = src_img.getpixel((x, y))
            if is_eye(r, g, b, a):
                eye_pixels[(x, y)] = (r, g, b, a)

    for dy in range(16):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if is_skin_warm(r, g, b, a): continue
            img.putpixel((x, y), (0, 0, 0, 0))

    for dy in range(len(HAIR_MAP_MUJER5)):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            if HAIR_MAP_MUJER5[dy][x] == 1:
                img.putpixel((x, y), hair_color_mujer5(x, dy))

    for (x, y), c in eye_pixels.items():
        img.putpixel((x, y), c)

    for y in range(H):
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if x == 0 or x == 17: continue
            if is_shoe(r, g, b, a):
                img.putpixel((x, y), SHOE_MAP_M5.get((r,g,b,a), (0x44,0x20,0x08,255)))
            elif is_faja(r, g, b, a):
                img.putpixel((x, y), FAJA_MAP_M5.get((r,g,b,a), (0xD8,0x90,0x08,255)))

    return img

def make_back_mujer5(src_img, s1v, s2v):
    """Vista espaldas MUJER5: ondas zafiro anchas, mapa explícito."""
    img = ImageOps.mirror(src_img).copy()
    hy0 = 1 if is_shifted(src_img) else 0

    body_px = {}
    for y in range(hy0 + 12, H):
        for x in range(W):
            c = img.getpixel((x, y))
            if c[3] > 0:
                body_px[(x, y)] = c

    for y in range(hy0 + 12):
        for x in range(W):
            img.putpixel((x, y), (0, 0, 0, 0))

    # Copa (dy0-7): incluye ancho extra en dy4-5 (x=1 y x=16 de la copa)
    _BTOP5 = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # dy0
        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy1
        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy2
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy3
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy4: ancho máximo
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy5: ancho máximo
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy6
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7
    ]
    for dy, row in enumerate(_BTOP5):
        y = hy0 + dy
        if y >= H: break
        for x, v in enumerate(row):
            if v:
                c = M5H3 if (dy <= 1 or (dy <= 5 and 2 <= x <= 15)) else M5H2
                img.putpixel((x, y), c)

    # Nuca (dy8-11): cobertura completa de pelo
    for dy in range(8, 12):
        y = hy0 + dy
        if y >= H: break
        for x in range(1, 17):
            if (dy % 2 == 0) and (x <= 1 or x >= 16):
                img.putpixel((x, y), M5H1)
            else:
                img.putpixel((x, y), M5H2)

    # Restaurar cuerpo
    for (x, y), c in body_px.items():
        img.putpixel((x, y), c)

    # Ondas colgantes: alternan 4px / 3px por lado (mismo patrón que el frente)
    _ONDA_XS = {
        12: list(range(1, 5)) + list(range(12, 16)),   # 4px onda
        13: list(range(1, 4)) + list(range(13, 16)),   # 3px
        14: list(range(1, 5)) + list(range(12, 16)),   # 4px onda
        15: list(range(1, 3)) + list(range(14, 16)),   # 2px taper
        16: [1, 15],                                    # 1px punta
    }
    for dy, xs in _ONDA_XS.items():
        y = hy0 + dy
        if y >= H: break
        for x in xs:
            img.putpixel((x, y), M5H2)

    return img

# ── Generar F1-F8 MUJER5 ──────────────────────────────────────────────────────
for _f in os.listdir(MUJER5_DIR):
    if _re.match(r'FRAME\d+\.png', _f):
        os.remove(os.path.join(MUJER5_DIR, _f))
print("\n=== MUJER5 (ondas largas azul zafiro, copa voluminosa, vestido dorado) ===")
for i in range(1, 9):
    src = Image.open(os.path.join(HOMBRE1_SRC_DIR, f"FRAME{i}.png")).convert("RGBA")
    make_mujer5(src).save(os.path.join(MUJER5_DIR, f"FRAME{i}.png"))
    print(f"  F{i} walk")

f1m5 = Image.open(os.path.join(MUJER5_DIR, "FRAME1.png")).convert("RGBA")
s1m5, s2m5, s3m5 = detect_body_shades(f1m5)
gen_animations(MUJER5_DIR, f1m5, M5H1, M5H2, M5H3, s1m5, s2m5, s3m5)
print("  F9-F49 animaciones")

# ── Regenerar vistas de espaldas con ondas ────────────────────────────────────
for i in range(1, 6):
    p = os.path.join(MUJER5_DIR, f"FRAME{i}.png")
    if not os.path.exists(p): continue
    src = Image.open(p).convert("RGBA")
    make_back_mujer5(src, s1m5, s2m5).save(os.path.join(MUJER5_DIR, f"FRAME{27+i}.png"))

make_back_mujer5(f1m5, s1m5, s2m5).save(os.path.join(MUJER5_DIR, "FRAME33.png"))

f34m5 = make_back_mujer5(f1m5, s1m5, s2m5)
for x in range(W):
    for y in range(19, H):
        f34m5.putpixel((x, y), (0, 0, 0, 0))
f34m5.save(os.path.join(MUJER5_DIR, "FRAME34.png"))

print("  F28-F34 espaldas con ondas regeneradas")

# ── Parche pelo lateral cantando (F44/F45) ────────────────────────────────────
# Las ondas en dy9/dy11/dy13 llegan a x=4 y x=12 — cubrir también esos puntos
for _fn_cant5 in ('FRAME44.png', 'FRAME45.png'):
    _p_cant5 = os.path.join(MUJER5_DIR, _fn_cant5)
    if not os.path.exists(_p_cant5): continue
    _img_cant5 = Image.open(_p_cant5).convert('RGBA')
    _hy_cant5 = 1 if is_shifted(_img_cant5) else 0
    for _dy_c5 in range(8, 14):
        _y_c5 = _hy_cant5 + _dy_c5
        if _y_c5 >= H: break
        # Filas 3px: x=1,2,3 y x=13,14,15
        # Filas 4px (impares respecto a dy8): x=1,2,3,4 y x=12,13,14,15
        if _dy_c5 % 2 == 1:   # dy9,11,13 → 4px
            _xs5 = (1, 2, 3, 4, 12, 13, 14, 15)
        else:                  # dy8,10,12 → 3px
            _xs5 = (1, 2, 3, 13, 14, 15)
        for _xc5 in _xs5:
            _cc5 = _img_cant5.getpixel((_xc5, _y_c5))
            if _cc5[3] == 0 or is_skin_warm(_cc5[0], _cc5[1], _cc5[2], _cc5[3]):
                _img_cant5.putpixel((_xc5, _y_c5), M5H2)
    _img_cant5.save(_p_cant5)
print("  F44/F45 pelo lateral ondas restaurado")

# ── Parche nuca inferior back-pose (F47/F48/F49) ─────────────────────────────
for _fn_bpose5 in ('FRAME47.png', 'FRAME48.png', 'FRAME49.png'):
    _p_bpose5 = os.path.join(MUJER5_DIR, _fn_bpose5)
    if not os.path.exists(_p_bpose5): continue
    _img_bpose5 = Image.open(_p_bpose5).convert('RGBA')
    _hy_bp5 = 1 if is_shifted(_img_bpose5) else 0
    for _dy_bp5 in (11, 12, 13):
        _y_bp5 = _hy_bp5 + _dy_bp5
        if _y_bp5 >= H: break
        for _xb5 in (2, 3, 14, 15, 16):
            _cb5 = _img_bpose5.getpixel((_xb5, _y_bp5))
            if _cb5[3] == 0 or is_skin_warm(_cb5[0], _cb5[1], _cb5[2], _cb5[3]):
                _img_bpose5.putpixel((_xb5, _y_bp5), M5H2)
    _img_bpose5.save(_p_bpose5)
print("  F47/F48/F49 nuca inferior MUJER5 restaurada")

# ── Eliminar rastro de café (MUJER5) ─────────────────────────────────────────
# M5H1 r=5<8, M5H2 g=70>65, M5H3 g=150>65 — ninguno pasa el filtro brownish
_cnt_m5_brown = 0
_M5_KEEP = {M5H1, M5H2, M5H3}
for _fp_m5 in os.listdir(MUJER5_DIR):
    if not _re.match(r'FRAME\d+\.png', _fp_m5): continue
    _fp_full5 = os.path.join(MUJER5_DIR, _fp_m5)
    _img_b5 = Image.open(_fp_full5).convert("RGBA")
    _changed_b5 = False
    for _py in range(min(17, H)):
        for _px in range(W):
            _br,_bg,_bb,_ba = _img_b5.getpixel((_px, _py))
            if _ba == 0: continue
            if is_skin_warm(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) in _M5_KEEP: continue
            if _py >= 8 and _py <= 13 and is_eye(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) == (0x28, 0x10, 0x08, 255): continue
            if 8 <= _br <= 130 and _bg < 65 and _bb < 65 and _br > _bg*1.3 and _br > _bb*1.8:
                _img_b5.putpixel((_px, _py), (0,0,0,0))
                _cnt_m5_brown += 1
                _changed_b5 = True
    if _changed_b5:
        _img_b5.save(_fp_full5)
print(f"  Café residual MUJER5 eliminado: {_cnt_m5_brown} pixeles borrados")

# Renombrar secuencialmente
_m5files = sorted([_f for _f in os.listdir(MUJER5_DIR) if _re.match(r'FRAME\d+\.png',_f)],
                  key=lambda _f: int(_re.search(r'(\d+)',_f).group(1)))
for _i,_f in enumerate(_m5files):
    os.rename(os.path.join(MUJER5_DIR,_f), os.path.join(MUJER5_DIR,f'_TM5_{_i+1}.png'))
for _i in range(len(_m5files)):
    os.rename(os.path.join(MUJER5_DIR,f'_TM5_{_i+1}.png'), os.path.join(MUJER5_DIR,f'FRAME{_i+1}.png'))

print(f"  Pelo: h1={M5H1[:3]} h2={M5H2[:3]} h3={M5H3[:3]}")
print(f"  Cuerpo: s1={s1m5[:3]} s2={s2m5[:3]}")
print(f"""
===============================================================
MUJER5 completa — {len(_m5files)} frames secuenciales (FRAME1..FRAME{len(_m5files)})
  Pelo: ondas largas azul zafiro, copa extra ancha (x=1→16 en dy4-5)
        ondas 3px/4px alternas por lado, punta 1px en dy15
  Vestido: dorado ámbar
  Zapatos: marrón chocolate oscuro
===============================================================""")

# ==============================================================================
# MUJER6 — Pelo punk explosivo fucsia, copa 18px completa, mechones locos
# ==============================================================================
MUJER6_DIR = os.path.join(PERSONAJES_DIR, "MUJER6")
os.makedirs(MUJER6_DIR, exist_ok=True)

# ── Pelo fucsia/magenta — todos fuera del rango brownish ─────────────────────
M6H1 = ( 80,   0, 100, 255)   # morado sombra   (b=100>65 → no atrapado)
M6H2 = (200,  20, 150, 255)   # fucsia base      (r=200>130 → no atrapado)
M6H3 = (255, 120, 220, 255)   # rosa neón highlight (r=255>130 → no atrapado)

# Silueta LOCA:
#  dy0   — 4 picos sueltos en el tope del canvas (¡punk!)
#  dy3   — incluye x=0 (rompe borde izquierdo)
#  dy4   — ancho TOTAL 18px (incluye x=0 y x=17)
#  dy5   — incluye x=17 (rompe borde derecho)
#  dy6   — incluye x=0 de nuevo (zigzag en los bordes)
#  dy8   — 5px izq + x=0, 6px der + x=17 (asimétrico)
#  dy9   — 1 pixel suelto punk en cada lado
#  dy11  — mechones en los extremos absolutos (x=0-1 y x=14-16)
#  dy12  — 2px descentrado (x=3-4 y x=12-13, no en el borde)
#  dy14-15 — puntas muy separadas (x=2 y x=15, ó x=1 y x=16)
HAIR_MAP_MUJER6 = [
    [0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0],  # dy0:  4 picos dispersos ↑
    [0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0],  # dy1:  bases de picos
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy2
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy3:  x=0 incluido ←
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy4:  ¡18px COMPLETO!
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy5:  x=17 incluido →
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy6:  x=0 de nuevo
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7:  hairline
    # ── Mechones irregulares / punk ─────────────────────────────────────────
    [1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1],  # dy8:  5px+x0 izq | 6px+x17 der
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],  # dy9:  pixel suelto (¡punk!)
    [0,1,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0],  # dy10: 4px izq | 4px der
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0],  # dy11: extremos x=0-1 | x=14-16
    [0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0],  # dy12: 2px descentrado
    [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],  # dy13: 2px | 1px
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],  # dy14: 1px separados
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],  # dy15: puntas extremas punk
]

def hair_color_mujer6(x, dy):
    if dy <= 1:                             return M6H3   # picos: rosa neón puro
    if dy <= 5 and 1 <= x <= 16:            return M6H3   # copa full: neón
    if dy >= 8 and (x <= 1 or x >= 15):    return M6H1   # mechones borde: sombra
    return M6H2

# ── Vestido verde lima brillante (contrasta explosivo con fucsia) ─────────────
FAJA_MAP_M6 = {
    (0xF2,0x31,0x17,255): (0x88,0xCC,0x10,255),   # → verde lima brillante
    (0xF2,0x2B,0x13,255): (0x80,0xC4,0x0C,255),
    (0xF1,0x32,0x13,255): (0x84,0xC8,0x0E,255),
    (0xD9,0x2B,0x14,255): (0x68,0xA8,0x08,255),   # → verde medio
    (0xAA,0x20,0x0F,255): (0x48,0x80,0x06,255),   # → verde oscuro
    (0xC7,0x28,0x12,255): (0x58,0x94,0x07,255),
    (0xF1,0x32,0x17,255): (0x88,0xCC,0x10,255),
    (0xF2,0x31,0x13,255): (0x86,0xCA,0x0F,255),
}

# ── Zapatos morado oscuro (coordina con M6H1) ─────────────────────────────────
SHOE_MAP_M6 = {
    (0x9B,0x09,0x08,255): (0x3C,0x08,0x50,255),
    (0xF2,0x2B,0x13,255): (0x60,0x0C,0x80,255),
    (0x7B,0x07,0x05,255): (0x2C,0x06,0x3C,255),
    (0xB6,0x10,0x11,255): (0x4C,0x0A,0x64,255),
    (0x72,0x07,0x05,255): (0x28,0x04,0x38,255),
    (0x61,0x06,0x04,255): (0x20,0x04,0x2C,255),
    (0x70,0x07,0x05,255): (0x26,0x04,0x36,255),
    (0x81,0x07,0x05,255): (0x30,0x06,0x42,255),
    (0x61,0x04,0x04,255): (0x20,0x04,0x2C,255),
    (0xAA,0x20,0x0F,255): (0x48,0x0A,0x60,255),
}

def make_mujer6(src_img):
    """Recolorea HOMBRE1 fuente para MUJER6 (pelo punk fucsia explosivo)."""
    img = src_img.copy()
    hy0 = 1 if is_shifted(src_img) else 0

    eye_pixels = {}
    for dy in range(8, 13):
        y = hy0 + dy
        if y >= H: break
        for x in range(4, 14):
            r, g, b, a = src_img.getpixel((x, y))
            if is_eye(r, g, b, a):
                eye_pixels[(x, y)] = (r, g, b, a)

    # Borrar dy0-15 (todo menos piel)
    for dy in range(16):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if is_skin_warm(r, g, b, a): continue
            img.putpixel((x, y), (0, 0, 0, 0))

    # Dibujar pelo punk
    for dy in range(len(HAIR_MAP_MUJER6)):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            if HAIR_MAP_MUJER6[dy][x] == 1:
                img.putpixel((x, y), hair_color_mujer6(x, dy))

    for (x, y), c in eye_pixels.items():
        img.putpixel((x, y), c)

    for y in range(H):
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if x == 0 or x == 17: continue
            if is_shoe(r, g, b, a):
                img.putpixel((x, y), SHOE_MAP_M6.get((r,g,b,a), (0x38,0x08,0x4C,255)))
            elif is_faja(r, g, b, a):
                img.putpixel((x, y), FAJA_MAP_M6.get((r,g,b,a), (0x80,0xC0,0x10,255)))

    return img

def make_back_mujer6(src_img, s1v, s2v):
    """Vista espaldas MUJER6: pelo punk ancho, mechones locos colgando."""
    img = ImageOps.mirror(src_img).copy()
    hy0 = 1 if is_shifted(src_img) else 0

    body_px = {}
    for y in range(hy0 + 12, H):
        for x in range(W):
            c = img.getpixel((x, y))
            if c[3] > 0:
                body_px[(x, y)] = c

    for y in range(hy0 + 12):
        for x in range(W):
            img.putpixel((x, y), (0, 0, 0, 0))

    # Copa explosiva — incluye x=0 y x=17 en filas alternas
    _BTOP6 = [
        [0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0],  # dy0: picos
        [0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0],  # dy1
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy2
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy3: x=0
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy4: 18px full
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy5: x=17
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy6: x=0
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7
    ]
    for dy, row in enumerate(_BTOP6):
        y = hy0 + dy
        if y >= H: break
        for x, v in enumerate(row):
            if v:
                c = M6H3 if (dy <= 1 or (dy <= 5 and 1 <= x <= 16)) else M6H2
                img.putpixel((x, y), c)

    # Nuca (dy8-11): cobertura completa con textura alternada
    for dy in range(8, 12):
        y = hy0 + dy
        if y >= H: break
        for x in range(0, 18):
            if x == 0 or x == 17:
                img.putpixel((x, y), M6H1 if dy % 2 == 0 else (0,0,0,0))
            elif x <= 1 or x >= 16:
                img.putpixel((x, y), M6H1)
            else:
                img.putpixel((x, y), M6H2)

    # Restaurar cuerpo
    for (x, y), c in body_px.items():
        img.putpixel((x, y), c)

    # Mechones locos colgando — mismo patrón asimétrico que el frente
    _PUNK_XS = {
        12: [0,1,2,3,4,   12,13,14,15,16,17],  # muy ancho
        13: [1,2,          14,15],
        14: [1,2,3,4,      11,12,13,14],
        15: [0,1,          15,16],
        16: [2,3,          12,13],
        17: [1,            15],
    }
    for dy, xs in _PUNK_XS.items():
        y = hy0 + dy
        if y >= H: break
        for x in xs:
            if 0 <= x < W:
                img.putpixel((x, y), M6H2)

    return img

# ── Generar F1-F8 MUJER6 ──────────────────────────────────────────────────────
for _f in os.listdir(MUJER6_DIR):
    if _re.match(r'FRAME\d+\.png', _f):
        os.remove(os.path.join(MUJER6_DIR, _f))
print("\n=== MUJER6 (punk explosivo fucsia, copa 18px, mechones locos) ===")
for i in range(1, 9):
    src = Image.open(os.path.join(HOMBRE1_SRC_DIR, f"FRAME{i}.png")).convert("RGBA")
    make_mujer6(src).save(os.path.join(MUJER6_DIR, f"FRAME{i}.png"))
    print(f"  F{i} walk")

f1m6 = Image.open(os.path.join(MUJER6_DIR, "FRAME1.png")).convert("RGBA")
s1m6, s2m6, s3m6 = detect_body_shades(f1m6)
gen_animations(MUJER6_DIR, f1m6, M6H1, M6H2, M6H3, s1m6, s2m6, s3m6)
print("  F9-F49 animaciones")

# ── Regenerar espaldas con mechones punk ─────────────────────────────────────
for i in range(1, 6):
    p = os.path.join(MUJER6_DIR, f"FRAME{i}.png")
    if not os.path.exists(p): continue
    src = Image.open(p).convert("RGBA")
    make_back_mujer6(src, s1m6, s2m6).save(os.path.join(MUJER6_DIR, f"FRAME{27+i}.png"))

make_back_mujer6(f1m6, s1m6, s2m6).save(os.path.join(MUJER6_DIR, "FRAME33.png"))

f34m6 = make_back_mujer6(f1m6, s1m6, s2m6)
for x in range(W):
    for y in range(19, H):
        f34m6.putpixel((x, y), (0, 0, 0, 0))
f34m6.save(os.path.join(MUJER6_DIR, "FRAME34.png"))

print("  F28-F34 espaldas punk regeneradas")

# ── Parche cantando (F44/F45): pelos laterales anchos + extremos ─────────────
for _fn_cant6 in ('FRAME44.png', 'FRAME45.png'):
    _p_cant6 = os.path.join(MUJER6_DIR, _fn_cant6)
    if not os.path.exists(_p_cant6): continue
    _img_cant6 = Image.open(_p_cant6).convert('RGBA')
    _hy_cant6 = 1 if is_shifted(_img_cant6) else 0
    for _dy_c6 in range(8, 14):
        _y_c6 = _hy_cant6 + _dy_c6
        if _y_c6 >= H: break
        # Cubre todo el ancho posible del pelo punk en zona de cara-cuello
        if _dy_c6 in (8, 10):        _xs6 = (0, 1, 2, 3, 4, 12, 13, 14, 15, 16, 17)
        elif _dy_c6 == 9:            _xs6 = (2, 14)
        elif _dy_c6 == 11:           _xs6 = (0, 1, 14, 15, 16)
        elif _dy_c6 == 12:           _xs6 = (3, 4, 12, 13)
        else:                        _xs6 = (1, 2, 14)
        for _xc6 in _xs6:
            if not (0 <= _xc6 < W): continue
            _cc6 = _img_cant6.getpixel((_xc6, _y_c6))
            if _cc6[3] == 0 or is_skin_warm(_cc6[0], _cc6[1], _cc6[2], _cc6[3]):
                _img_cant6.putpixel((_xc6, _y_c6), M6H2)
    _img_cant6.save(_p_cant6)
print("  F44/F45 mechones laterales punk restaurados")

# ── Parche nuca inferior back-pose (F47/F48/F49) ─────────────────────────────
for _fn_bpose6 in ('FRAME47.png', 'FRAME48.png', 'FRAME49.png'):
    _p_bpose6 = os.path.join(MUJER6_DIR, _fn_bpose6)
    if not os.path.exists(_p_bpose6): continue
    _img_bpose6 = Image.open(_p_bpose6).convert('RGBA')
    _hy_bp6 = 1 if is_shifted(_img_bpose6) else 0
    for _dy_bp6 in (11, 12, 13):
        _y_bp6 = _hy_bp6 + _dy_bp6
        if _y_bp6 >= H: break
        for _xb6 in (1, 2, 3, 14, 15, 16):
            _cb6 = _img_bpose6.getpixel((_xb6, _y_bp6))
            if _cb6[3] == 0 or is_skin_warm(_cb6[0], _cb6[1], _cb6[2], _cb6[3]):
                _img_bpose6.putpixel((_xb6, _y_bp6), M6H2)
    _img_bpose6.save(_p_bpose6)
print("  F47/F48/F49 nuca punk restaurada")

# ── Eliminar rastro de café (MUJER6) ─────────────────────────────────────────
_cnt_m6_brown = 0
_M6_KEEP = {M6H1, M6H2, M6H3}
for _fp_m6 in os.listdir(MUJER6_DIR):
    if not _re.match(r'FRAME\d+\.png', _fp_m6): continue
    _fp_full6 = os.path.join(MUJER6_DIR, _fp_m6)
    _img_b6 = Image.open(_fp_full6).convert("RGBA")
    _changed_b6 = False
    for _py in range(min(17, H)):
        for _px in range(W):
            _br,_bg,_bb,_ba = _img_b6.getpixel((_px, _py))
            if _ba == 0: continue
            if is_skin_warm(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) in _M6_KEEP: continue
            if _py >= 8 and _py <= 13 and is_eye(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) == (0x28, 0x10, 0x08, 255): continue
            if 8 <= _br <= 130 and _bg < 65 and _bb < 65 and _br > _bg*1.3 and _br > _bb*1.8:
                _img_b6.putpixel((_px, _py), (0,0,0,0))
                _cnt_m6_brown += 1
                _changed_b6 = True
    if _changed_b6:
        _img_b6.save(_fp_full6)
print(f"  Café residual MUJER6 eliminado: {_cnt_m6_brown} pixeles borrados")

# Renombrar secuencialmente
_m6files = sorted([_f for _f in os.listdir(MUJER6_DIR) if _re.match(r'FRAME\d+\.png',_f)],
                  key=lambda _f: int(_re.search(r'(\d+)',_f).group(1)))
for _i,_f in enumerate(_m6files):
    os.rename(os.path.join(MUJER6_DIR,_f), os.path.join(MUJER6_DIR,f'_TM6_{_i+1}.png'))
for _i in range(len(_m6files)):
    os.rename(os.path.join(MUJER6_DIR,f'_TM6_{_i+1}.png'), os.path.join(MUJER6_DIR,f'FRAME{_i+1}.png'))

print(f"  Pelo: h1={M6H1[:3]} h2={M6H2[:3]} h3={M6H3[:3]}")
print(f"  Cuerpo: s1={s1m6[:3]} s2={s2m6[:3]}")
print(f"""
===============================================================
MUJER6 completa — {len(_m6files)} frames secuenciales (FRAME1..FRAME{len(_m6files)})
  Pelo: punk explosivo fucsia — 4 picos en dy0, copa 18px completa en dy4,
        mechones asimétricos locos (pixel suelto dy9, extremos dy11, etc.)
  Vestido: verde lima brillante
  Zapatos: morado oscuro
===============================================================""")

# ==============================================================================
# MUJER7 — Rastas de fuego naranja, 5 picos, copa doble-18px, dreads hasta dy19
# ==============================================================================
MUJER7_DIR = os.path.join(PERSONAJES_DIR, "MUJER7")
os.makedirs(MUJER7_DIR, exist_ok=True)

# ── Pelo naranja fuego — todos r>130, fuera del rango brownish ───────────────
M7H1 = (160,  50,   0, 255)   # naranja oscuro sombra  (r=160>130)
M7H2 = (255, 110,   0, 255)   # naranja fuego base     (r=255>130)
M7H3 = (255, 210,  60, 255)   # amarillo dorado brillo (r=255>130)

# LO QUE TIENE DE LOCO:
#  dy0  — 5 picos separados (vs 4 de MUJER6)
#  dy1  — bases con huecos (no bloque sólido)
#  dy3+dy4 — 18px FULL dos filas seguidas (vs 1 de MUJER6)
#  dy9  — patrón alternado pixel a pixel (efecto dread texturizado)
#  dy11 — pico en x=17 suelto al extremo derecho
#  dy15 — 3 puntas en posiciones no contiguas
#  dy16-dy19 — RASTAS LARGAS que cuelgan más abajo que cualquier otra mujer
HAIR_MAP_MUJER7 = [
    [0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0],  # dy0:  5 picos finos ↑
    [0,1,1,1,0,1,1,0,0,1,1,0,1,1,0,1,1,0],  # dy1:  bases separadas (huecos!)
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy2:  casi full
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy3:  18px FULL #1
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy4:  18px FULL #2 (dos seguidas!)
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy5:  x=17 incluido
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy6:  x=0 incluido
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7:  hairline
    # ── Rastas/dreads — irregulares, caóticas, más largas que cualquier mujer ─
    [1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0],  # dy8:  5px+x0 | 4px
    [0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0],  # dy9:  ALTERNADO pixel×pixel
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0],  # dy10: 3px | 3px+extremo
    [0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1],  # dy11: 2px | 2px + x=17 suelto!
    [1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,0,0],  # dy12: salpicado asimétrico
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],  # dy13: 1px izq | 2px der
    [0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0],  # dy14: 2px | 1px
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0],  # dy15: 3 puntas no contiguas
]

# Extensión rastas largas (dy16-19): se pinta sobre pixels transparentes
_DREAD7_EXT = [
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],  # dy16: rasta larga izq | der
    [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],  # dy17: desplazadas (movimiento)
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],  # dy18: vuelven a los bordes
    [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0],  # dy19: puntas finales internas
]

def hair_color_mujer7(x, dy):
    if dy <= 1:                              return M7H3   # picos: amarillo fuego
    if dy <= 5 and 1 <= x <= 16:             return M7H3   # copa ancha: dorado
    if dy >= 8 and (x <= 1 or x >= 15):     return M7H1   # rastas borde: sombra
    return M7H2

# ── Vestido borgoña/vino (contrasta con naranja fuego) ───────────────────────
FAJA_MAP_M7 = {
    (0xF2,0x31,0x17,255): (0xB0,0x14,0x30,255),   # → borgoña brillante
    (0xF2,0x2B,0x13,255): (0xA8,0x12,0x2C,255),
    (0xF1,0x32,0x13,255): (0xAC,0x13,0x2E,255),
    (0xD9,0x2B,0x14,255): (0x90,0x0E,0x24,255),   # → vino medio
    (0xAA,0x20,0x0F,255): (0x70,0x0A,0x1A,255),   # → vino oscuro
    (0xC7,0x28,0x12,255): (0x80,0x0C,0x20,255),
    (0xF1,0x32,0x17,255): (0xB0,0x14,0x30,255),
    (0xF2,0x31,0x13,255): (0xAE,0x13,0x2F,255),
}

# ── Zapatos negro/antracita ───────────────────────────────────────────────────
SHOE_MAP_M7 = {
    (0x9B,0x09,0x08,255): (0x1A,0x14,0x18,255),
    (0xF2,0x2B,0x13,255): (0x2C,0x22,0x28,255),
    (0x7B,0x07,0x05,255): (0x14,0x10,0x12,255),
    (0xB6,0x10,0x11,255): (0x22,0x1A,0x20,255),
    (0x72,0x07,0x05,255): (0x12,0x0E,0x10,255),
    (0x61,0x06,0x04,255): (0x10,0x0C,0x0E,255),
    (0x70,0x07,0x05,255): (0x11,0x0D,0x10,255),
    (0x81,0x07,0x05,255): (0x16,0x12,0x14,255),
    (0x61,0x04,0x04,255): (0x10,0x0C,0x0E,255),
    (0xAA,0x20,0x0F,255): (0x20,0x18,0x1C,255),
}

def make_mujer7(src_img):
    """Recolorea HOMBRE1 para MUJER7 (rastas naranja fuego, copa doble 18px)."""
    img = src_img.copy()
    hy0 = 1 if is_shifted(src_img) else 0

    eye_pixels = {}
    for dy in range(8, 13):
        y = hy0 + dy
        if y >= H: break
        for x in range(4, 14):
            r, g, b, a = src_img.getpixel((x, y))
            if is_eye(r, g, b, a):
                eye_pixels[(x, y)] = (r, g, b, a)

    for dy in range(16):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if is_skin_warm(r, g, b, a): continue
            img.putpixel((x, y), (0, 0, 0, 0))

    # Copa + mechones principales (dy0-15)
    for dy in range(len(HAIR_MAP_MUJER7)):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            if HAIR_MAP_MUJER7[dy][x] == 1:
                img.putpixel((x, y), hair_color_mujer7(x, dy))

    for (x, y), c in eye_pixels.items():
        img.putpixel((x, y), c)

    # Rastas largas (dy16-19): solo sobre pixels transparentes para no tapar cuerpo
    for di, row in enumerate(_DREAD7_EXT):
        y = hy0 + 16 + di
        if y >= H: break
        for x, v in enumerate(row):
            if v and img.getpixel((x, y))[3] == 0:
                img.putpixel((x, y), M7H2)

    # Vestido borgoña y zapatos negros
    for y in range(H):
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if x == 0 or x == 17: continue
            if is_shoe(r, g, b, a):
                img.putpixel((x, y), SHOE_MAP_M7.get((r,g,b,a), (0x18,0x12,0x16,255)))
            elif is_faja(r, g, b, a):
                img.putpixel((x, y), FAJA_MAP_M7.get((r,g,b,a), (0xA0,0x12,0x28,255)))

    return img

def make_back_mujer7(src_img, s1v, s2v):
    """Vista espaldas MUJER7: rastas naranja fuego, dreads colgando."""
    img = ImageOps.mirror(src_img).copy()
    hy0 = 1 if is_shifted(src_img) else 0

    body_px = {}
    for y in range(hy0 + 12, H):
        for x in range(W):
            c = img.getpixel((x, y))
            if c[3] > 0:
                body_px[(x, y)] = c

    for y in range(hy0 + 12):
        for x in range(W):
            img.putpixel((x, y), (0, 0, 0, 0))

    # Copa explosiva (misma que frente)
    _BTOP7 = [
        [0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0],  # dy0: picos
        [0,1,1,1,0,1,1,0,0,1,1,0,1,1,0,1,1,0],  # dy1
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy2
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy3: 18px
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy4: 18px
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy5
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy6
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy7
    ]
    for dy, row in enumerate(_BTOP7):
        y = hy0 + dy
        if y >= H: break
        for x, v in enumerate(row):
            if v:
                c = M7H3 if (dy <= 1 or (dy <= 5 and 1 <= x <= 16)) else M7H2
                img.putpixel((x, y), c)

    # Nuca (dy8-11): cobertura total con textura de rastas
    for dy in range(8, 12):
        y = hy0 + dy
        if y >= H: break
        for x in range(0, 18):
            if x <= 1 or x >= 15:
                img.putpixel((x, y), M7H1)
            else:
                img.putpixel((x, y), M7H2)

    # Restaurar cuerpo
    for (x, y), c in body_px.items():
        img.putpixel((x, y), c)

    # Dreads cayendo — patrón irregular igual que el frente
    _DREADS7_BACK = {
        12: [0,1,2,3,4,   12,13,14,15,16,17],
        13: [1,           15,16],
        14: [1,2,3,       11,12,13,14],
        15: [0,2,         14,16],
        16: [1,           15],
        17: [2,           13],
        18: [1,           14],
        19: [3,           12],
    }
    for dy, xs in _DREADS7_BACK.items():
        y = hy0 + dy
        if y >= H: break
        for x in xs:
            if 0 <= x < W:
                cur = img.getpixel((x, y))
                if cur[3] == 0:   # solo sobre transparente
                    img.putpixel((x, y), M7H2)

    return img

# ── Generar F1-F8 MUJER7 ──────────────────────────────────────────────────────
for _f in os.listdir(MUJER7_DIR):
    if _re.match(r'FRAME\d+\.png', _f):
        os.remove(os.path.join(MUJER7_DIR, _f))
print("\n=== MUJER7 (rastas fuego naranja, 5 picos, doble 18px, dreads dy16-19) ===")
for i in range(1, 9):
    src = Image.open(os.path.join(HOMBRE1_SRC_DIR, f"FRAME{i}.png")).convert("RGBA")
    make_mujer7(src).save(os.path.join(MUJER7_DIR, f"FRAME{i}.png"))
    print(f"  F{i} walk")

f1m7 = Image.open(os.path.join(MUJER7_DIR, "FRAME1.png")).convert("RGBA")
s1m7, s2m7, s3m7 = detect_body_shades(f1m7)
gen_animations(MUJER7_DIR, f1m7, M7H1, M7H2, M7H3, s1m7, s2m7, s3m7)
print("  F9-F49 animaciones")

# ── Regenerar espaldas con dreads largas ─────────────────────────────────────
for i in range(1, 6):
    p = os.path.join(MUJER7_DIR, f"FRAME{i}.png")
    if not os.path.exists(p): continue
    src = Image.open(p).convert("RGBA")
    make_back_mujer7(src, s1m7, s2m7).save(os.path.join(MUJER7_DIR, f"FRAME{27+i}.png"))

make_back_mujer7(f1m7, s1m7, s2m7).save(os.path.join(MUJER7_DIR, "FRAME33.png"))

f34m7 = make_back_mujer7(f1m7, s1m7, s2m7)
for x in range(W):
    for y in range(19, H):
        f34m7.putpixel((x, y), (0, 0, 0, 0))
f34m7.save(os.path.join(MUJER7_DIR, "FRAME34.png"))

print("  F28-F34 espaldas rastas regeneradas")

# ── Parche cantando (F44/F45): dreads anchos + alternado de dy9 ───────────────
for _fn_cant7 in ('FRAME44.png', 'FRAME45.png'):
    _p_cant7 = os.path.join(MUJER7_DIR, _fn_cant7)
    if not os.path.exists(_p_cant7): continue
    _img_cant7 = Image.open(_p_cant7).convert('RGBA')
    _hy_cant7 = 1 if is_shifted(_img_cant7) else 0
    for _dy_c7 in range(8, 14):
        _y_c7 = _hy_cant7 + _dy_c7
        if _y_c7 >= H: break
        if _dy_c7 == 8:      _xs7 = (0,1,2,3,4, 12,13,14,15,16)
        elif _dy_c7 == 9:    _xs7 = (1,3, 13,15)          # alternado
        elif _dy_c7 == 10:   _xs7 = (0,1,2, 14,15,16)
        elif _dy_c7 == 11:   _xs7 = (2,3, 13,14, 17)
        elif _dy_c7 == 12:   _xs7 = (0,1,3, 12,14,15)
        else:                _xs7 = (1, 15,16)
        for _xc7 in _xs7:
            if not (0 <= _xc7 < W): continue
            _cc7 = _img_cant7.getpixel((_xc7, _y_c7))
            if _cc7[3] == 0 or is_skin_warm(_cc7[0], _cc7[1], _cc7[2], _cc7[3]):
                _img_cant7.putpixel((_xc7, _y_c7), M7H2)
    _img_cant7.save(_p_cant7)
print("  F44/F45 rastas cantando restauradas")

# ── Parche nuca inferior back-pose (F47/F48/F49) ─────────────────────────────
for _fn_bpose7 in ('FRAME47.png', 'FRAME48.png', 'FRAME49.png'):
    _p_bpose7 = os.path.join(MUJER7_DIR, _fn_bpose7)
    if not os.path.exists(_p_bpose7): continue
    _img_bpose7 = Image.open(_p_bpose7).convert('RGBA')
    _hy_bp7 = 1 if is_shifted(_img_bpose7) else 0
    for _dy_bp7 in (11, 12, 13):
        _y_bp7 = _hy_bp7 + _dy_bp7
        if _y_bp7 >= H: break
        for _xb7 in (1, 2, 3, 14, 15, 16):
            _cb7 = _img_bpose7.getpixel((_xb7, _y_bp7))
            if _cb7[3] == 0 or is_skin_warm(_cb7[0], _cb7[1], _cb7[2], _cb7[3]):
                _img_bpose7.putpixel((_xb7, _y_bp7), M7H2)
    _img_bpose7.save(_p_bpose7)
print("  F47/F48/F49 nuca rastas restaurada")

# ── Parche camisa top MUJER7: algunos colores borgoña oscuros (r≤130) son ─────
# ── atrapados por el sweep brownish y borrados en y=13-16. Se re-pinta antes ─
# ── del sweep usando el color del vecino izquierdo/derecho más cercano.       ─
_m7_vest_c = FAJA_MAP_M7.get((0xD9,0x2B,0x14,255), s1m7)  # tono medio borgoña
for _fp_ct7 in os.listdir(MUJER7_DIR):
    if not _re.match(r'FRAME\d+\.png', _fp_ct7): continue
    _fpc7 = os.path.join(MUJER7_DIR, _fp_ct7)
    _ic7 = Image.open(_fpc7).convert('RGBA')
    _hy_ct7 = 1 if is_shifted(_ic7) else 0
    _ch_ct7 = False
    for _y_ct7 in range(_hy_ct7 + 13, _hy_ct7 + 17):
        if _y_ct7 >= H: break
        for _x_ct7 in range(4, 14):
            if _ic7.getpixel((_x_ct7, _y_ct7))[3] == 0:
                # buscar color vecino válido (no transparente, no pelo)
                _cv7 = None
                for _xn in [_x_ct7-1, _x_ct7+1, _x_ct7-2, _x_ct7+2]:
                    if not (0 <= _xn < W): continue
                    _cn = _ic7.getpixel((_xn, _y_ct7))
                    if _cn[3] > 0 and _cn[:3] not in (M7H1[:3], M7H2[:3], M7H3[:3]):
                        _cv7 = _cn; break
                _ic7.putpixel((_x_ct7, _y_ct7), _cv7 if _cv7 else _m7_vest_c)
                _ch_ct7 = True
    if _ch_ct7: _ic7.save(_fpc7)
print("  Camisa top MUJER7 parcheada (colores borgoña oscuro restaurados)")

# ── Parche brazo F40/F41 (FRAME48/49): _limpiar_brazos corta x=14-17 del ─────
# ── brazo extendido en espaldas. Se extiende color de x=12→13-16 donde TRANS ─
for _fn_arm7 in ('FRAME48.png', 'FRAME49.png'):
    _p_arm7 = os.path.join(MUJER7_DIR, _fn_arm7)
    if not os.path.exists(_p_arm7): continue
    _img_arm7 = Image.open(_p_arm7).convert('RGBA')
    _hy_arm7 = 1 if is_shifted(_img_arm7) else 0
    _ch_arm7 = False
    for _y_arm7 in range(_hy_arm7 + 14, _hy_arm7 + 20):
        if _y_arm7 >= H: break
        # referencia: primer pixel de cuerpo en x=9-12 (no pelo, no transparente)
        _refarm7 = None
        for _xr7 in range(12, 8, -1):
            _cr7 = _img_arm7.getpixel((_xr7, _y_arm7))
            if _cr7[3] > 0 and _cr7[:3] not in (M7H1[:3], M7H2[:3], M7H3[:3]):
                _refarm7 = _cr7; break
        if _refarm7 is None: continue
        # extender hacia la derecha hasta encontrar pixel no-transparente
        for _xa7 in range(13, 17):
            _ex7 = _img_arm7.getpixel((_xa7, _y_arm7))
            if _ex7[3] == 0:
                _img_arm7.putpixel((_xa7, _y_arm7), _refarm7)
                _ch_arm7 = True
            else:
                break
    if _ch_arm7: _img_arm7.save(_p_arm7)
print("  Brazo F48/F49 MUJER7 restaurado (extension x=13-16)")

# ── Eliminar rastro de café (MUJER7) ─────────────────────────────────────────
# Proteger TAMBIÉN los colores de vestido y zapatos que tengan r≤130 (borgoña)
_cnt_m7_brown = 0
_M7_KEEP = {M7H1, M7H2, M7H3} | set(FAJA_MAP_M7.values()) | set(SHOE_MAP_M7.values())
for _fp_m7 in os.listdir(MUJER7_DIR):
    if not _re.match(r'FRAME\d+\.png', _fp_m7): continue
    _fp_full7 = os.path.join(MUJER7_DIR, _fp_m7)
    _img_b7 = Image.open(_fp_full7).convert("RGBA")
    _changed_b7 = False
    for _py in range(min(17, H)):
        for _px in range(W):
            _br,_bg,_bb,_ba = _img_b7.getpixel((_px, _py))
            if _ba == 0: continue
            if is_skin_warm(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) in _M7_KEEP: continue
            if _py >= 8 and _py <= 13 and is_eye(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) == (0x28, 0x10, 0x08, 255): continue
            if 8 <= _br <= 130 and _bg < 65 and _bb < 65 and _br > _bg*1.3 and _br > _bb*1.8:
                _img_b7.putpixel((_px, _py), (0,0,0,0))
                _cnt_m7_brown += 1
                _changed_b7 = True
    if _changed_b7:
        _img_b7.save(_fp_full7)
print(f"  Café residual MUJER7 eliminado: {_cnt_m7_brown} pixeles borrados")

# Renombrar secuencialmente
_m7files = sorted([_f for _f in os.listdir(MUJER7_DIR) if _re.match(r'FRAME\d+\.png',_f)],
                  key=lambda _f: int(_re.search(r'(\d+)',_f).group(1)))
for _i,_f in enumerate(_m7files):
    os.rename(os.path.join(MUJER7_DIR,_f), os.path.join(MUJER7_DIR,f'_TM7_{_i+1}.png'))
for _i in range(len(_m7files)):
    os.rename(os.path.join(MUJER7_DIR,f'_TM7_{_i+1}.png'), os.path.join(MUJER7_DIR,f'FRAME{_i+1}.png'))

print(f"  Pelo: h1={M7H1[:3]} h2={M7H2[:3]} h3={M7H3[:3]}")
print(f"  Cuerpo: s1={s1m7[:3]} s2={s2m7[:3]}")
print(f"""
===============================================================
MUJER7 completa — {len(_m7files)} frames secuenciales (FRAME1..FRAME{len(_m7files)})
  Pelo: RASTAS FUEGO naranja — 5 picos dy0, bases con huecos dy1,
        doble 18px en dy3+dy4, alternado px×px en dy9, x=17 suelto dy11,
        DREADS LARGAS hasta dy19 (4 filas extra vs MUJER6)
  Vestido: borgoña/vino oscuro
  Zapatos: negro antracita
===============================================================""")

# ==============================================================================
# MUJER8 — Afro puff esférico violeta, silueta circular, SIN pelo bajo la cara
# ==============================================================================
# Concepto único: todas las demás mujeres tienen pelo ABAJO de la cara (lateral).
# MUJER8 tiene un afro puff que crece HACIA ARRIBA Y LOS LADOS como esfera:
#   - Sube de 8px (dy0) a 18px completos (dy4) — ancho máximo
#   - Luego BAJA a 11px (dy7) — hairline estrecho
#   - Solo 1px suelto a cada lado en dy8 (framing minimalista)
#   - NADA de pelo colgante — la esfera termina al nivel del rostro
# Esto crea una silueta completamente diferente a todas las demás.
MUJER8_DIR = os.path.join(PERSONAJES_DIR, "MUJER8")
os.makedirs(MUJER8_DIR, exist_ok=True)

# ── Pelo violeta vibrante — todos fuera del rango brownish ───────────────────
M8H1 = ( 15,   5,  80, 255)   # índigo oscuro sombra  (b=80>65 → no atrapado)
M8H2 = ( 80,  20, 180, 255)   # violeta vibrante base (b=180>65 → no atrapado)
M8H3 = (160,  80, 255, 255)   # lavanda neón highlight (r=160>130 → no atrapado)

# Silueta esférica: sube de estrecho→ancho→estrecho, SIN cola lateral
HAIR_MAP_MUJER8 = [
    [0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],  # dy0: tope estrecho  (8px centro)
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy1: 12px
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy2: 14px
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy3: 16px
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy4: ← 18px MÁXIMO (ecuador)
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy5: 16px (empieza a bajar)
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy6: 14px
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy7: 11px — hairline recto
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],  # dy8: 1px cada lado (solo framing)
    # ¡SIN NADA MÁS ABAJO! — la cara queda completamente expuesta
]

def hair_color_mujer8(x, dy):
    if dy <= 1:                              return M8H3   # tope: lavanda brillante
    if dy <= 4 and 2 <= x <= 15:            return M8H3   # esfera interior: highlight
    if dy >= 5 and (x <= 2 or x >= 15):     return M8H1   # parte baja: sombra profunda
    if dy == 8:                              return M8H1   # framing: sombra (1px)
    return M8H2

# ── Vestido coral/salmón vivo (contrasta con violeta) ────────────────────────
FAJA_MAP_M8 = {
    (0xF2,0x31,0x17,255): (0xE0,0x60,0x48,255),   # → coral brillante
    (0xF2,0x2B,0x13,255): (0xD8,0x58,0x40,255),
    (0xF1,0x32,0x13,255): (0xDC,0x5C,0x44,255),
    (0xD9,0x2B,0x14,255): (0xC0,0x48,0x34,255),   # → salmón medio
    (0xAA,0x20,0x0F,255): (0x98,0x34,0x24,255),   # → terracota oscuro
    (0xC7,0x28,0x12,255): (0xAC,0x3E,0x2C,255),
    (0xF1,0x32,0x17,255): (0xE0,0x60,0x48,255),
    (0xF2,0x31,0x13,255): (0xDE,0x5E,0x46,255),
}

# ── Zapatos dorado oscuro (complemento del violeta) ──────────────────────────
SHOE_MAP_M8 = {
    (0x9B,0x09,0x08,255): (0x60,0x46,0x00,255),
    (0xF2,0x2B,0x13,255): (0x90,0x6C,0x04,255),
    (0x7B,0x07,0x05,255): (0x4C,0x36,0x00,255),
    (0xB6,0x10,0x11,255): (0x78,0x58,0x02,255),
    (0x72,0x07,0x05,255): (0x46,0x32,0x00,255),
    (0x61,0x06,0x04,255): (0x3C,0x2A,0x00,255),
    (0x70,0x07,0x05,255): (0x44,0x32,0x00,255),
    (0x81,0x07,0x05,255): (0x52,0x3C,0x00,255),
    (0x61,0x04,0x04,255): (0x3C,0x2A,0x00,255),
    (0xAA,0x20,0x0F,255): (0x6C,0x50,0x02,255),
}

def make_mujer8(src_img):
    """Recolorea HOMBRE1 para MUJER8 (afro puff esférico violeta)."""
    img = src_img.copy()
    hy0 = 1 if is_shifted(src_img) else 0

    eye_pixels = {}
    for dy in range(8, 13):
        y = hy0 + dy
        if y >= H: break
        for x in range(4, 14):
            r, g, b, a = src_img.getpixel((x, y))
            if is_eye(r, g, b, a):
                eye_pixels[(x, y)] = (r, g, b, a)

    for dy in range(16):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if is_skin_warm(r, g, b, a): continue
            img.putpixel((x, y), (0, 0, 0, 0))

    for dy in range(len(HAIR_MAP_MUJER8)):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            if HAIR_MAP_MUJER8[dy][x] == 1:
                img.putpixel((x, y), hair_color_mujer8(x, dy))

    for (x, y), c in eye_pixels.items():
        img.putpixel((x, y), c)

    for y in range(H):
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if x == 0 or x == 17: continue
            if is_shoe(r, g, b, a):
                img.putpixel((x, y), SHOE_MAP_M8.get((r,g,b,a), (0x58,0x40,0x00,255)))
            elif is_faja(r, g, b, a):
                img.putpixel((x, y), FAJA_MAP_M8.get((r,g,b,a), (0xD0,0x54,0x3C,255)))

    return img

def make_back_mujer8(src_img, s1v, s2v):
    """Vista espaldas MUJER8: afro puff esférico desde atrás, nuca muy corta."""
    img = ImageOps.mirror(src_img).copy()
    hy0 = 1 if is_shifted(src_img) else 0

    body_px = {}
    for y in range(hy0 + 9, H):
        for x in range(W):
            c = img.getpixel((x, y))
            if c[3] > 0:
                body_px[(x, y)] = c

    for y in range(hy0 + 9):
        for x in range(W):
            img.putpixel((x, y), (0, 0, 0, 0))

    # Copa esférica — misma forma que el frente (simétrica)
    _BTOP8 = [
        [0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],  # dy0
        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy1
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy2
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy3
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy4: ecuador
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy5
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy6
        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy7
    ]
    for dy, row in enumerate(_BTOP8):
        y = hy0 + dy
        if y >= H: break
        for x, v in enumerate(row):
            if v:
                c = M8H3 if (dy <= 1 or (dy <= 4 and 2 <= x <= 15)) else (M8H1 if (dy >= 5 and (x <= 2 or x >= 15)) else M8H2)
                img.putpixel((x, y), c)

    # Nuca (dy8 solamente): muy corta — solo 1px al igual que el frente
    y8 = hy0 + 8
    if y8 < H:
        for x in range(2, 16):
            img.putpixel((x, y8), M8H2)

    # Restaurar cuerpo
    for (x, y), c in body_px.items():
        img.putpixel((x, y), c)

    # Sin melena colgante — el afro termina en dy8

    return img

# ── Generar F1-F8 MUJER8 ──────────────────────────────────────────────────────
for _f in os.listdir(MUJER8_DIR):
    if _re.match(r'FRAME\d+\.png', _f):
        os.remove(os.path.join(MUJER8_DIR, _f))
print("\n=== MUJER8 (afro puff esférico violeta, vestido coral, zapatos dorado) ===")
for i in range(1, 9):
    src = Image.open(os.path.join(HOMBRE1_SRC_DIR, f"FRAME{i}.png")).convert("RGBA")
    make_mujer8(src).save(os.path.join(MUJER8_DIR, f"FRAME{i}.png"))
    print(f"  F{i} walk")

f1m8 = Image.open(os.path.join(MUJER8_DIR, "FRAME1.png")).convert("RGBA")
s1m8, s2m8, s3m8 = detect_body_shades(f1m8)
gen_animations(MUJER8_DIR, f1m8, M8H1, M8H2, M8H3, s1m8, s2m8, s3m8)
print("  F9-F49 animaciones")

# ── Regenerar espaldas con afro esférico ─────────────────────────────────────
for i in range(1, 6):
    p = os.path.join(MUJER8_DIR, f"FRAME{i}.png")
    if not os.path.exists(p): continue
    src = Image.open(p).convert("RGBA")
    make_back_mujer8(src, s1m8, s2m8).save(os.path.join(MUJER8_DIR, f"FRAME{27+i}.png"))

make_back_mujer8(f1m8, s1m8, s2m8).save(os.path.join(MUJER8_DIR, "FRAME33.png"))

f34m8 = make_back_mujer8(f1m8, s1m8, s2m8)
for x in range(W):
    for y in range(19, H):
        f34m8.putpixel((x, y), (0, 0, 0, 0))
f34m8.save(os.path.join(MUJER8_DIR, "FRAME34.png"))

print("  F28-F34 espaldas afro regeneradas")

# ── Parche cantando (F44/F45): afro dy8 solo tiene 1px en x=2 y x=14 ─────────
for _fn_cant8 in ('FRAME44.png', 'FRAME45.png'):
    _p_cant8 = os.path.join(MUJER8_DIR, _fn_cant8)
    if not os.path.exists(_p_cant8): continue
    _img_cant8 = Image.open(_p_cant8).convert('RGBA')
    _hy_cant8 = 1 if is_shifted(_img_cant8) else 0
    # El afro solo tiene dy8 como framing — restaurar solo esos 2 pixels
    _y_c8 = _hy_cant8 + 8
    if _y_c8 < H:
        for _xc8 in (2, 14):
            _cc8 = _img_cant8.getpixel((_xc8, _y_c8))
            if _cc8[3] == 0 or is_skin_warm(_cc8[0], _cc8[1], _cc8[2], _cc8[3]):
                _img_cant8.putpixel((_xc8, _y_c8), M8H1)
    _img_cant8.save(_p_cant8)
print("  F44/F45 framing afro restaurado")

# ── Parche nuca back-pose (F47/F48/F49): nuca muy corta del afro ─────────────
for _fn_bpose8 in ('FRAME47.png', 'FRAME48.png', 'FRAME49.png'):
    _p_bpose8 = os.path.join(MUJER8_DIR, _fn_bpose8)
    if not os.path.exists(_p_bpose8): continue
    _img_bpose8 = Image.open(_p_bpose8).convert('RGBA')
    _hy_bp8 = 1 if is_shifted(_img_bpose8) else 0
    # Afro solo necesita restaurar dy8 (nuca 1 fila) en bordes
    _y_bp8 = _hy_bp8 + 8
    if _y_bp8 < H:
        for _xb8 in range(2, 16):
            _cb8 = _img_bpose8.getpixel((_xb8, _y_bp8))
            if _cb8[3] == 0 or is_skin_warm(_cb8[0], _cb8[1], _cb8[2], _cb8[3]):
                _img_bpose8.putpixel((_xb8, _y_bp8), M8H2)
    _img_bpose8.save(_p_bpose8)
print("  F47/F48/F49 nuca afro restaurada")

# ── Eliminar rastro de café (MUJER8) — afro violeta totalmente seguro ─────────
# M8H1 b=80>65, M8H2 b=180>65, M8H3 r=160>130 → ninguno pasa brownish sweep
_cnt_m8_brown = 0
_M8_KEEP = {M8H1, M8H2, M8H3} | set(FAJA_MAP_M8.values()) | set(SHOE_MAP_M8.values())
for _fp_m8 in os.listdir(MUJER8_DIR):
    if not _re.match(r'FRAME\d+\.png', _fp_m8): continue
    _fp_full8 = os.path.join(MUJER8_DIR, _fp_m8)
    _img_b8 = Image.open(_fp_full8).convert("RGBA")
    _changed_b8 = False
    for _py in range(min(17, H)):
        for _px in range(W):
            _br,_bg,_bb,_ba = _img_b8.getpixel((_px, _py))
            if _ba == 0: continue
            if is_skin_warm(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) in _M8_KEEP: continue
            if _py >= 8 and _py <= 13 and is_eye(_br,_bg,_bb,_ba): continue
            if (_br,_bg,_bb,_ba) == (0x28, 0x10, 0x08, 255): continue
            if 8 <= _br <= 130 and _bg < 65 and _bb < 65 and _br > _bg*1.3 and _br > _bb*1.8:
                _img_b8.putpixel((_px, _py), (0,0,0,0))
                _cnt_m8_brown += 1
                _changed_b8 = True
    if _changed_b8:
        _img_b8.save(_fp_full8)
print(f"  Café residual MUJER8 eliminado: {_cnt_m8_brown} pixeles borrados")

# Renombrar secuencialmente
_m8files = sorted([_f for _f in os.listdir(MUJER8_DIR) if _re.match(r'FRAME\d+\.png',_f)],
                  key=lambda _f: int(_re.search(r'(\d+)',_f).group(1)))
for _i,_f in enumerate(_m8files):
    os.rename(os.path.join(MUJER8_DIR,_f), os.path.join(MUJER8_DIR,f'_TM8_{_i+1}.png'))
for _i in range(len(_m8files)):
    os.rename(os.path.join(MUJER8_DIR,f'_TM8_{_i+1}.png'), os.path.join(MUJER8_DIR,f'FRAME{_i+1}.png'))

print(f"  Pelo: h1={M8H1[:3]} h2={M8H2[:3]} h3={M8H3[:3]}")
print(f"  Cuerpo: s1={s1m8[:3]} s2={s2m8[:3]}")
print(f"""
===============================================================
MUJER8 completa — {len(_m8files)} frames secuenciales (FRAME1..FRAME{len(_m8files)})
  Pelo: AFRO PUFF esférico violeta — sube de 8px a 18px (dy4 ecuador)
        luego baja a 11px hairline. CERO pelo lateral bajo la cara.
        Silueta circular única — ninguna otra mujer tiene esta forma.
  Vestido: coral/salmón vivo
  Zapatos: dorado oscuro
===============================================================""")
