import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageOps

MUJERES_DIR = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PERSONAJES\MUJERES"
MUJER1_DIR  = os.path.join(MUJERES_DIR, "MUJER1")
W, H = 18, 25

# ── Paleta universal ──────────────────────────────────────────────────────────
SKIN  = (0xFE, 0xD9, 0x98, 255)
SKNS  = (0xF5, 0xB9, 0x71, 255)
SKND  = (0xD4, 0x94, 0x50, 255)
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
# CONFIGURACION — editar aqui para generar una variante nueva
# ==============================================================================
NOMBRE_SALIDA = "MUJER9"

# Pelo oscuro castano (para variante)
HAIR_SHADOW = (0x20, 0x10, 0x08, 255)
HAIR_BASE   = (0x44, 0x22, 0x0E, 255)
HAIR_LIGHT  = (0x68, 0x38, 0x18, 255)

# Peinado: mediano, sin tocar bordes del canvas (max x=2..x=14)
HAIR_MAP = [
    #x: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17
       [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # dy0 cima
       [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # dy1
       [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # dy2
       [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # dy3
       [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],  # dy4
       [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  # dy5 laterales
       [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  # dy6
       [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # dy7
]

def hair_color(x, dy):
    hard_edge = x <= 1 or x >= 16
    vert_side  = (x <= 2 or x >= 14) and dy >= 2
    soft_edge  = x <= 3 or x >= 14
    if dy >= 6:                   return HAIR_SHADOW
    if hard_edge:                 return HAIR_SHADOW
    if vert_side:                 return HAIR_SHADOW
    if dy >= 4 and soft_edge:     return HAIR_SHADOW
    if dy == 1:                   return HAIR_LIGHT
    return HAIR_BASE

# Blusa (para generar variante desde MUJER1 fuente — rosado → azul)
FAJA_MAP = {
    (250, 70,138,255): ( 70,130,220,255),
    (228,  0, 85,255): ( 40, 80,200,255),
    (255,  0, 96,255): ( 60,110,240,255),
    (205,  0, 77,255): ( 30, 60,170,255),
}

# Zapatos (rojo-naranja → negro)
SHOE_MAP = {
    (255, 39,  0,255): (0x22,0x18,0x18,255),
    (228, 35,  0,255): (0x18,0x10,0x10,255),
    (255, 84,  0,255): (0x2E,0x20,0x20,255),
    (207, 32,  0,255): (0x14,0x0C,0x0C,255),
}

# ==============================================================================
# DETECCION Y UTILIDADES
# ==============================================================================
def is_hair_src(r, g, b, a):
    """Detecta pelo cafe de HOMBRE1 (para F35 template acostado)."""
    return a > 0 and 0x1C <= r <= 0x50 and r > g * 1.5 and r > b * 1.8

def is_hair_mujer(r, g, b, a):
    """Detecta pelo amarillo/dorado de MUJER1 fuente (para make_mujer)."""
    return a > 0 and r > 200 and g > 170 and b < 100 and r > b * 3

def is_eye_mujer(r, g, b, a):
    """Detecta ojos de MUJER1 (azul y contorno oscuro)."""
    if a == 0: return False
    if b > 100 and b > r * 2 and b > g: return True   # ojo azul
    if r < 100 and g < 100 and b < 100 and r > 30: return True  # contorno oscuro
    return False

def is_blusa(r, g, b, a):
    """Detecta blusa rosada de MUJER1 (para make_mujer)."""
    return a > 0 and r > 150 and b > 50 and b > g and r > b

def is_zapato(r, g, b, a):
    """Detecta zapatos rojo-naranja de MUJER1 (para make_mujer)."""
    return a > 0 and r > 150 and g < 100 and b < 30

def is_faja(r, g, b, a):
    """Detecta faja/blusa en template de cama (HOMBRE1 rojo, para F35)."""
    return a > 0 and r > 140 and r > g * 3 and g > 20

def is_skin_warm(r, g, b, a):
    return a > 0 and r > 0xC0 and g > 0x70 and b > 0x30 and (r - b) > 40

def is_shifted(img):
    return all(img.getpixel((x, 0))[3] == 0 for x in range(W))

def px(img, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), color)

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
    return unique[max(0,n//10)], unique[n//2], unique[min(n-1,9*n//10)]

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
    return unique[max(0,n//10)], unique[n//2], unique[min(n-1,9*n//10)]

# ==============================================================================
# MAKE_MUJER — recolorea MUJER1 fuente al NOMBRE_SALIDA configurado
# ==============================================================================
def make_mujer(src_img):
    img = src_img.copy()
    hy0 = 1 if is_shifted(src_img) else 0

    # Guardar ojos antes de borrar pelo
    eye_pixels = {}
    for dy in range(12):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if is_hair_mujer(r, g, b, a):
                if dy >= 7 and 4 <= x <= 13 and is_eye_mujer(r, g, b, a):
                    eye_pixels[(x, y)] = (r, g, b, a)
                img.putpixel((x, y), (0, 0, 0, 0))

    # Nuevo peinado segun HAIR_MAP
    for dy in range(8):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            if HAIR_MAP[dy][x] == 1:
                img.putpixel((x, y), hair_color(x, dy))

    # Patillas laterales
    for dy in range(8, 12):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if is_hair_mujer(r, g, b, a) and (x <= 3 or x >= 14) and x != 0 and x != 17:
                img.putpixel((x, y), HAIR_SHADOW)

    # Restaurar ojos
    for (x, y), c in eye_pixels.items():
        img.putpixel((x, y), c)

    # Blusa y zapatos
    for y in range(H):
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if x == 0 or x == 17: continue
            if is_zapato(r, g, b, a):
                img.putpixel((x, y), SHOE_MAP.get((r,g,b,a), (0x18,0x10,0x10,255)))
            elif is_blusa(r, g, b, a):
                img.putpixel((x, y), FAJA_MAP.get((r,g,b,a), (0x40,0x80,0xC0,255)))

    return img

# ==============================================================================
# GENERADOR DE ANIMACIONES F9-F45 (universal para cualquier mujer)
# ==============================================================================
def gen_animations(dst_dir, f1_img, h1, h2, h3, s1, s2, s3):
    def slv(x):
        return s1 if (x <= 5 or x >= 12) else (s3 if x in (8,9) else s2)

    BASE = f1_img.copy()
    for y in range(15, H):
        for x in range(W):
            r, g, b, a = BASE.getpixel((x, y))
            if a > 0 and is_skin_warm(r, g, b, a):
                BASE.putpixel((x, y), slv(x))

    # ── F9: Orante ────────────────────────────────────────────────────────────
    f9 = BASE.copy()
    px(f9, 4,15,s2); px(f9, 3,15,s1); px(f9, 3,14,s2); px(f9, 2,14,s1)
    px(f9, 2,13,s2); px(f9, 1,13,s1); px(f9, 1,12,s2); px(f9, 0,12,s1)
    px(f9, 0,11,SKNS); px(f9, 0,10,SKIN); px(f9, 0,9,SKIN)
    px(f9,13,15,s2); px(f9,14,15,s1); px(f9,14,14,s2); px(f9,15,14,s1)
    px(f9,15,13,s2); px(f9,16,13,s1); px(f9,16,12,s2); px(f9,17,12,s1)
    px(f9,17,11,SKNS); px(f9,17,10,SKIN); px(f9,17,9,SKIN)
    f9.save(os.path.join(dst_dir,"FRAME9.png"))

    # ── F10: Manos juntas ─────────────────────────────────────────────────────
    f10 = BASE.copy()
    px(f10, 4,16,s3); px(f10, 5,16,s3); px(f10, 4,17,s3); px(f10, 5,17,s2)
    px(f10,13,16,s3); px(f10,12,16,s3); px(f10,13,17,s3); px(f10,12,17,s2)
    px(f10, 7,17,SKNS); px(f10, 8,17,SKIN); px(f10, 9,17,SKIN)
    px(f10,10,17,SKIN); px(f10,11,17,SKNS)
    px(f10, 7,18,SKND); px(f10, 8,18,SKNS); px(f10, 9,18,SKNS)
    px(f10,10,18,SKNS); px(f10,11,18,SKND)
    px(f10, 8,19,SKND); px(f10, 9,19,SKND); px(f10,10,19,SKND)
    px(f10, 6,17,s1); px(f10,12,17,s1)
    f10.save(os.path.join(dst_dir,"FRAME10.png"))

    # ── F11: Campana ──────────────────────────────────────────────────────────
    f11 = BASE.copy()
    px(f11,13,15,s2); px(f11,14,15,s1); px(f11,14,14,s2); px(f11,14,13,s1)
    px(f11,15,13,s2); px(f11,15,12,s1); px(f11,15,11,s2); px(f11,16,11,s1)
    px(f11,15,10,SKNS); px(f11,16,10,SKIN)
    px(f11,15, 9,SKND); px(f11,16, 9,SKNS)
    px(f11,15, 8,BEL2); px(f11,16, 8,BEL1)
    px(f11,14, 7,BEL1); px(f11,15, 7,BEL3); px(f11,16, 7,BEL2)
    px(f11,13, 6,BEL1); px(f11,14, 6,BEL2); px(f11,15, 6,BEL3)
    px(f11,16, 6,BEL2); px(f11,17, 6,BEL1)
    f11.save(os.path.join(dst_dir,"FRAME11.png"))

    # ── F12: Vela ─────────────────────────────────────────────────────────────
    f12 = BASE.copy()
    px(f12, 8, 7,CND_O)
    px(f12, 7, 8,CND_Y); px(f12, 8, 8,CND_O); px(f12, 9, 8,CND_Y)
    for cy in range(9, 15): px(f12, 8, cy, CND_W)
    px(f12, 5,14,s2); px(f12, 4,14,s1); px(f12, 6,14,SKNS); px(f12, 7,14,SKIN)
    px(f12, 6,15,SKND); px(f12, 7,15,SKNS)
    px(f12,12,14,s2); px(f12,13,14,s1); px(f12,11,14,SKNS); px(f12,10,14,SKIN)
    px(f12,11,15,SKND); px(f12,10,15,SKNS)
    f12.save(os.path.join(dst_dir,"FRAME12.png"))

    # ── F13: Incensario ───────────────────────────────────────────────────────
    f13 = BASE.copy()
    px(f13,13,15,s2); px(f13,14,15,s1); px(f13,14,16,s2); px(f13,15,16,s1)
    px(f13,15,17,s2); px(f13,16,17,s1)
    px(f13,15,18,SKNS); px(f13,16,18,SKIN)
    px(f13,15,19,SKND); px(f13,16,19,SKNS)
    px(f13,15,20,THU1); px(f13,16,20,THU1)
    px(f13,14,21,THU1); px(f13,15,21,THU2); px(f13,16,21,THU1)
    px(f13,14,22,THU1); px(f13,15,22,THU2); px(f13,16,22,THU1)
    px(f13,14,23,THU1); px(f13,15,23,THU1); px(f13,16,23,THU1)
    f13.save(os.path.join(dst_dir,"FRAME13.png"))

    # ── F14: Manos extendidas ─────────────────────────────────────────────────
    f14 = BASE.copy()
    px(f14, 3,16,s2); px(f14, 2,16,s1); px(f14, 3,17,s1); px(f14, 2,17,s2)
    px(f14, 1,16,SKNS); px(f14, 0,16,SKIN); px(f14, 1,17,SKND); px(f14, 0,17,SKNS)
    px(f14,14,16,s2); px(f14,15,16,s1); px(f14,14,17,s1); px(f14,15,17,s2)
    px(f14,16,16,SKNS); px(f14,17,16,SKIN); px(f14,16,17,SKND); px(f14,17,17,SKNS)
    f14.save(os.path.join(dst_dir,"FRAME14.png"))

    # ── F15: Cruz procesional ─────────────────────────────────────────────────
    f15 = BASE.copy()
    for cy in range(9, 22): px(f15, 8, cy, CRS2)
    px(f15, 8, 9,CRSG); px(f15, 8,10,CRSG); px(f15, 8,11,CRSG)
    for cx in range(5, 12): px(f15, cx, 10, CRSG)
    px(f15, 5,15,s2); px(f15, 4,15,s1); px(f15, 6,15,SKNS); px(f15, 7,15,SKIN)
    px(f15, 6,16,SKND); px(f15, 7,16,SKNS)
    px(f15,12,15,s2); px(f15,13,15,s1); px(f15,11,15,SKNS); px(f15,10,15,SKIN)
    px(f15,11,16,SKND); px(f15,10,16,SKNS)
    f15.save(os.path.join(dst_dir,"FRAME15.png"))

    # ── F16-F27: Senal de la Cruz ─────────────────────────────────────────────
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
    px(f19,13,15,s3); px(f19,14,15,s1); px(f19,14,14,s2); px(f19,14,13,s1); px(f19,14,12,s2)
    px(f19,14,11,SKNS); px(f19,15,11,SKIN); px(f19,15,10,SKND)
    f19.save(os.path.join(dst_dir,"FRAME19.png"))

    f20 = BASE.copy()
    px(f20,13,15,s3); px(f20,13,16,s2); px(f20,12,16,s1)
    px(f20,11,16,s2); px(f20,10,16,s1)
    px(f20, 9,15,SKNS); px(f20,10,15,SKIN)
    px(f20, 8,16,SKND); px(f20, 9,16,SKNS); px(f20,10,16,SKIN); px(f20,8,17,s1)
    f20.save(os.path.join(dst_dir,"FRAME20.png"))

    f21 = BASE.copy()
    px(f21,13,15,s2); px(f21,12,16,s1); px(f21,11,16,s2)
    px(f21,10,16,s1); px(f21, 9,16,s2)
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
    px(f27,11,14,s2); px(f27,11,13,s1); px(f27,10,13,s2)
    px(f27,10,12,SKNS); px(f27, 9,12,SKIN); px(f27,11,12,SKND)
    px(f27, 9,11,SKNS); px(f27,10,11,SKIN)
    f27.save(os.path.join(dst_dir,"FRAME27.png"))

    # ── Back view helper ──────────────────────────────────────────────────────
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
                if x == 0 or x >= 16: continue
                if x <= 1 or x >= 15:    c = h1
                elif x <= 3 or x >= 14:  c = h2
                else:                    c = h3 if y <= 2 else h2
                img.putpixel((x, y), c)
            elif y <= 11:
                if x == 0 or x >= 16: continue
                img.putpixel((x, y), h1 if (x <= 2 or x >= 15) else h2)
            elif y <= 14:
                if x <= 3 or x >= 14:    c = SKND
                else:                    c = SKNS if y == 12 else SKIN
                img.putpixel((x, y), c)
            else:
                if x == 0 or x == 17: continue
                img.putpixel((x, y), s1 if (x <= 4 or x >= 13) else s2)
        return img

    # F28-F32: caminata espaldas (flip F1-F5)
    for i in range(1, 6):
        p = os.path.join(dst_dir, f"FRAME{i}.png")
        if not os.path.exists(p): continue
        src = Image.open(p).convert("RGBA")
        make_back(src).save(os.path.join(dst_dir, f"FRAME{27+i}.png"))

    # F33: parada espaldas
    make_back(f1_img).save(os.path.join(dst_dir, "FRAME33.png"))

    # F34: sentada espaldas (sin piernas)
    f34 = make_back(f1_img)
    for x in range(W):
        for y in range(19, H):
            f34.putpixel((x, y), (0, 0, 0, 0))
    f34.save(os.path.join(dst_dir, "FRAME34.png"))

    # ── F35: Acostada en cama ─────────────────────────────────────────────────
    CAMA_TPL = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\FRAME9.png"
    if os.path.exists(CAMA_TPL):
        tmpl = Image.open(CAMA_TPL).convert("RGBA")
        f35 = Image.new("RGBA", (W, H), (0,0,0,0))
        for y in range(H):
            for x in range(W):
                r, g, b, a = tmpl.getpixel((x, y))
                if a == 0:
                    pass
                elif is_hair_src(r, g, b, a):
                    if x != 0 and x != 17:
                        lum = r + g + b
                        c = h1 if lum < 55 else (h3 if lum > 90 else h2)
                        f35.putpixel((x, y), c)
                elif is_faja(r, g, b, a):
                    lum = r + g + b
                    c = s1 if lum < 250 else (s3 if lum > 295 else s2)
                    f35.putpixel((x, y), c)
                else:
                    f35.putpixel((x, y), (r, g, b, a))
        f35.save(os.path.join(dst_dir, "FRAME35.png"))

    # ── F36-F39: Caminando con Biblia (F1-F4) ────────────────────────────────
    BK1 = (0x4C,0x28,0x08,255); BK2 = (0x78,0x44,0x14,255)
    BKP = (0xEC,0xE8,0xD8,255); BKX = (0xC0,0x60,0x08,255)
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
        px(out, 4,15,s2); px(out, 5,15,s1); px(out, 4,16,s2); px(out, 5,16,s1)
        px(out,13,15,s2); px(out,12,15,s1); px(out,13,16,s2); px(out,12,16,s1)
        px(out, 4,17,SKNS); px(out, 4,18,SKND)
        px(out,13,17,SKNS); px(out,13,18,SKND)
        # Brazo derecho extendido al lado del libro
        px(out, 14,16,s1); px(out, 14,17,s1)
        px(out, 14,18,s1); px(out, 14,19,s1)
        # Zapato visible a la derecha del libro
        px(out, 13,20,SHD); px(out, 13,21,SHD)
        for _bx in range(5,13):
            for _by in range(17,22):
                if   _bx in (5,12):  _c = BK1
                elif _by in (17,21): _c = BK1
                elif _bx in (6,11):  _c = BK2
                else:                _c = BKP
                px(out,_bx,_by,_c)
        px(out,8,18,BKX); px(out,8,19,BKX); px(out,8,20,BKX)
        px(out,7,19,BKX); px(out,9,19,BKX)

    for _i in range(1, 2):
        _p = os.path.join(dst_dir, f"FRAME{_i}.png")
        if not os.path.exists(_p): continue
        _src = Image.open(_p).convert("RGBA")
        _frm = _src.copy()
        for _y in range(15, H):
            for _x in range(W):
                _r,_g,_b,_a = _src.getpixel((_x,_y))
                if _a == 0 or not is_skin_warm(_r,_g,_b,_a): continue
                _frm.putpixel((_x,_y), slv(_x))
        _draw_bible(_frm)
        _frm.save(os.path.join(dst_dir, f"FRAME{35+_i}.png"))
    for _fn in [37, 38, 39]:
        _fp = os.path.join(dst_dir, f"FRAME{_fn}.png")
        if os.path.exists(_fp): os.remove(_fp)

    # ── F44-F45: Cantando (levanta/agacha + boca) ─────────────────────────────
    hy0 = 1 if is_shifted(f1_img) else 0
    ym  = hy0 + 11
    MOT = (0x28,0x10,0x08,255)

    def _shift_up(src):
        out = Image.new("RGBA",(W,H),(0,0,0,0))
        for _y in range(1,H):
            for _x in range(W):
                out.putpixel((_x,_y-1), src.getpixel((_x,_y)))
        return out

    f45 = _shift_up(f1_img)
    px(f45, 8, ym,   MOT)
    px(f45, 8, ym-1, MOT)
    f45.save(os.path.join(dst_dir,"FRAME45.png"))

    f44 = f45.copy()
    _shy = 14 + hy0
    for _cy in range(9, H):
        for _cx in range(4):      f44.putpixel((_cx,_cy),(0,0,0,0))
        for _cx in range(14, W): f44.putpixel((_cx,_cy),(0,0,0,0))
    for _cy in range(_shy+2, H):
        for _cx in range(4, 14):
            _r,_g,_b,_a = f44.getpixel((_cx,_cy))
            if _a > 0 and is_skin_warm(_r,_g,_b,_a): f44.putpixel((_cx,_cy),(0,0,0,0))
    px(f44, 3,_shy,    s1); px(f44, 2,_shy-1,  s1)
    px(f44, 1,_shy-2,  s2); px(f44, 0,_shy-3,SKNS); px(f44, 0,_shy-4,SKIN)
    px(f44,14,_shy,    s1); px(f44,15,_shy-1,  s1)
    px(f44,16,_shy-2,  s2); px(f44,17,_shy-3,SKNS); px(f44,17,_shy-4,SKIN)
    f44.save(os.path.join(dst_dir,"FRAME44.png"))

    # ── F46-F49: Frames de espaldas adicionales ───────────────────────────────

    def _limpiar_brazos(img, y0=15, y1=22):
        for _cy in range(y0, y1):
            for _cx in range(4):      img.putpixel((_cx,_cy),(0,0,0,0))
            for _cx in range(14, W): img.putpixel((_cx,_cy),(0,0,0,0))
        for _cy in range(max(y0, 18), y1):
            for _cx in range(4, 14):
                _r,_g,_b,_a = img.getpixel((_cx,_cy))
                if _a > 0 and is_skin_warm(_r,_g,_b,_a):
                    img.putpixel((_cx,_cy),(0,0,0,0))

    def _hombros(img):
        for _cy in range(15, 18):
            px(img, 4,_cy,s1); px(img,13,_cy,s1)

    # F46: Incarse (arrodillada de espaldas)
    f46 = make_back(f1_img)
    for _cx in range(W):
        for _cy in range(15, H): f46.putpixel((_cx,_cy),(0,0,0,0))
    for _cy in range(15, 18):
        for _cx in range(4, 14): f46.putpixel((_cx,_cy), s1 if (_cx<=5 or _cx>=12) else s2)
    for _cx in range(4, 14): f46.putpixel((_cx,18), s1 if (_cx<=5 or _cx>=12) else s2)
    for _cy in range(19, 21):
        px(f46, 3,_cy,s1); px(f46,4,_cy,s2); px(f46,5,_cy,s2); px(f46,6,_cy,s1)
        px(f46,11,_cy,s1); px(f46,12,_cy,s2); px(f46,13,_cy,s2); px(f46,14,_cy,s1)
    for _cx in range(4, 8):  f46.putpixel((_cx,21), SHD if (_cx==4 or _cx==7) else SHM)
    for _cx in range(10,14): f46.putpixel((_cx,21), SHD if (_cx==10 or _cx==13) else SHM)
    f46.save(os.path.join(dst_dir,"FRAME46.png"))

    # F47: Padre Nuestro de espaldas (brazos horizontales)
    f47 = make_back(f1_img)
    _limpiar_brazos(f47); _hombros(f47)
    px(f47,3,15,s1); px(f47,2,15,s1); px(f47,1,15,SKNS); px(f47,0,15,SKIN)
    px(f47,3,16,s1); px(f47,2,16,s1); px(f47,1,16,SKNS); px(f47,0,16,SKND)
    px(f47,14,15,s1); px(f47,15,15,s1); px(f47,16,15,SKNS); px(f47,17,15,SKIN)
    px(f47,14,16,s1); px(f47,15,16,s1); px(f47,16,16,SKNS); px(f47,17,16,SKND)
    f47.save(os.path.join(dst_dir,"FRAME47.png"))

    # F48: Dar la paz de espaldas (brazo derecho extendido)
    f48 = make_back(f1_img)
    _limpiar_brazos(f48); _hombros(f48)
    px(f48,14,15,s1); px(f48,15,15,s1)
    px(f48,14,16,s1); px(f48,15,16,s2); px(f48,16,16,SKNS)
    px(f48,16,17,SKNS); px(f48,17,17,SKIN)
    px(f48,17,18,SKIN)
    f48.save(os.path.join(dst_dir,"FRAME48.png"))

    # F49: Levantar manos de espaldas (ambos brazos completamente arriba)
    f49 = make_back(f1_img)
    _limpiar_brazos(f49, 9, 22); _hombros(f49)
    px(f49, 3,15,s1); px(f49,2,15,s1)
    px(f49, 3,14,s1); px(f49,2,14,s1)
    px(f49, 2,13,s1); px(f49,1,13,s2)
    px(f49, 2,12,s1); px(f49,1,12,s2)
    px(f49, 1,11,s2); px(f49,0,11,SKNS)
    px(f49, 0,10,SKNS); px(f49,0,9,SKIN)
    px(f49,14,15,s1); px(f49,15,15,s1)
    px(f49,14,14,s1); px(f49,15,14,s1)
    px(f49,15,13,s1); px(f49,16,13,s2)
    px(f49,15,12,s1); px(f49,16,12,s2)
    px(f49,16,11,s2); px(f49,17,11,SKNS)
    px(f49,17,10,SKNS); px(f49,17,9,SKIN)
    # Restaurar nuca borrada por _limpiar donde el brazo no cubre (y=9-11)
    px(f49, 1,9,h1);  px(f49,2,9,h1);  px(f49,3,9,h2)
    px(f49, 1,10,h1); px(f49,2,10,h1); px(f49,3,10,h2)
    px(f49, 2,11,h1); px(f49,3,11,h2)
    px(f49,14,9,h2);  px(f49,15,9,h1)
    px(f49,14,10,h2); px(f49,15,10,h1)
    px(f49,14,11,h2); px(f49,15,11,h1)
    f49.save(os.path.join(dst_dir,"FRAME49.png"))

# ==============================================================================
# GENERAR NOMBRE_SALIDA desde cero (F1-F8 con make_mujer + F9-F45)
# ==============================================================================
DST = os.path.join(MUJERES_DIR, NOMBRE_SALIDA)
os.makedirs(DST, exist_ok=True)

print(f"\n=== {NOMBRE_SALIDA} (desde MUJER1 fuente) ===")
for i in range(1, 9):
    src = Image.open(os.path.join(MUJER1_DIR, f"FRAME{i}.png")).convert("RGBA")
    make_mujer(src).save(os.path.join(DST, f"FRAME{i}.png"))
    print(f"  F{i} walk")

f1_dst = Image.open(os.path.join(DST,"FRAME1.png")).convert("RGBA")
h1,h2,h3 = HAIR_SHADOW, HAIR_BASE, HAIR_LIGHT
s1,s2,s3 = detect_body_shades(f1_dst)
gen_animations(DST, f1_dst, h1,h2,h3, s1,s2,s3)
print(f"  F9-F45 animaciones")
print(f"  Cuerpo detectado: s1={s1[:3]} s2={s2[:3]}")

# ==============================================================================
# BATCH — agregar F9-F45 a todas las demas MUJER1-MUJER9
# ==============================================================================
TODOS = ["MUJER1","MUJER2","MUJER3","MUJER4",
         "MUJER5","MUJER6","MUJER7","MUJER8","MUJER9"]

for nombre in TODOS:
    if nombre == NOMBRE_SALIDA:
        continue
    d = os.path.join(MUJERES_DIR, nombre)
    f1_path = os.path.join(d, "FRAME1.png")
    if not os.path.exists(f1_path):
        print(f"\n{nombre}: sin FRAME1, omitida")
        continue

    print(f"\n=== {nombre} (F9-F45 sobre frames existentes) ===")
    f1 = Image.open(f1_path).convert("RGBA")
    h1b,h2b,h3b = detect_hair_shades(f1)
    s1b,s2b,s3b = detect_body_shades(f1)
    gen_animations(d, f1, h1b,h2b,h3b, s1b,s2b,s3b)
    print(f"  Pelo:  h1={h1b[:3]} h2={h2b[:3]} h3={h3b[:3]}")
    print(f"  Cuerpo: s1={s1b[:3]} s2={s2b[:3]}")
    print(f"  F9-F45 generados")

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
  F33     espaldas parada
  F34     espaldas sentada
  F35     acostada en cama
  F36-F39 caminando con Biblia (F1-F4)
  F44     cantando: levanta, 1px boca
  F45     cantando: boca abierta, 2px vertical
  F46     incarse de espaldas
  F47     Padre Nuestro de espaldas (brazos horizontales)
  F48     dar la paz de espaldas (brazo derecho)
  F49     levantar manos de espaldas
Personajes procesados: MUJER1-MUJER9
===============================================================""")
