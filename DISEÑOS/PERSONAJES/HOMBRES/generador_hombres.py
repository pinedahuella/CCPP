import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
Generador de personajes HOMBRE para CCPP
=========================================
Edita la seccion CONFIGURACION para crear un nuevo personaje.
"""

from PIL import Image
import os

BASE    = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PERSONAJES\HOMBRES"
HOMBRE1 = os.path.join(BASE, "HOMBRE1")

# ==============================================================================
# CONFIGURACION
# ==============================================================================

NOMBRE_SALIDA = "HOMBRE9"

# -- Pelo: 3 tonos (sombra, base, luz) -----------------------------------------
# HOMBRE9: teal oscuro / cian profundo
HAIR_SHADOW = (0x04, 0x28, 0x30, 255)
HAIR_BASE   = (0x08, 0x58, 0x68, 255)
HAIR_LIGHT  = (0x18, 0x9C, 0xB4, 255)

# -- Pelo: forma / silueta ------------------------------------------------------
# Estilo FLAT TOP: tope plano horizontal, corte cuadrado — muy diferente a picos/curvas
HAIR_MAP = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # dy0: vacio — el flat top empieza en dy1
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],  # dy1: borde plano superior (flat top)
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],  # dy2: lados verticales
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy3
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],  # dy4
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],  # dy5
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy6
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # dy7 hairline
]

def hair_color(x, dy):
    """
    3 tonos jugando: BASE es el color dominante (mayoria del pelo),
    SHADOW solo en bordes reales y hairline,
    LIGHT solo en la zona de brillo superior.
    """
    hard_edge = x <= 1 or x >= 16
    soft_edge = x <= 3 or x >= 14
    # Picos del pelo salvaje: luz en las puntas de cada mechon
    # Flat top: borde superior plano = luz, lados verticales = sombra, interior = base
    flat_top   = dy == 1                     # fila del tope plano = luz
    vert_side  = (x <= 2 or x >= 14) and dy >= 2   # lados verticales = sombra

    if dy >= 6:
        return HAIR_SHADOW
    if hard_edge:
        return HAIR_SHADOW
    if vert_side:
        return HAIR_SHADOW
    if dy >= 4 and soft_edge:
        return HAIR_SHADOW
    if flat_top:
        return HAIR_LIGHT                    # superficie plana del top = luz
    return HAIR_BASE

# -- Faja: rojo -> coral/salmon -----------------------------------------------
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

# -- Zapatos: rojo oscuro -> vino/borgoña oscuro ------------------------------
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
# LOGICA
# ==============================================================================

def is_hair(r, g, b, a):
    return a > 0 and 0x1C <= r <= 0x50 and r > g * 1.5 and r > b * 1.8

def is_faja(r, g, b, a): return a > 0 and r > 140 and r > g * 3 and g > 20
def is_shoe(r, g, b, a): return a > 0 and r > 60  and r > g * 3 and g <= 20

def detect_shifted(frame):
    for x in range(18):
        if frame.getpixel((x, 0))[3] > 0:
            return False
    return True

# ==============================================================================
# GENERAR
# ==============================================================================

DST = os.path.join(BASE, NOMBRE_SALIDA)
os.makedirs(DST, exist_ok=True)

for i in range(1, 10):
    img = Image.open(os.path.join(HOMBRE1, f"FRAME{i}.png")).convert("RGBA")
    out = img.copy()

    shifted = detect_shifted(img)
    hair_y0 = 1 if shifted else 0

    # 1. Borrar todo el pelo cafe de HOMBRE1 en la zona del pelo
    for dy in range(8):
        y = hair_y0 + dy
        if y >= 25: break
        for x in range(18):
            r, g, b, a = img.getpixel((x, y))
            if is_hair(r, g, b, a):
                out.putpixel((x, y), (0, 0, 0, 0))

    # 2. Pintar el nuevo disenio de pelo segun HAIR_MAP
    for dy in range(8):
        y = hair_y0 + dy
        if y >= 25: break
        for x in range(18):
            if HAIR_MAP[dy][x] == 1:
                out.putpixel((x, y), hair_color(x, dy))

    # 3. Patillas (y08-y09): columnas exteriores
    for dy in range(8, 10):
        y = hair_y0 + dy
        if y >= 25: break
        for x in range(18):
            if 3 < x < 14: continue
            r, g, b, a = img.getpixel((x, y))
            if is_hair(r, g, b, a):
                out.putpixel((x, y), HAIR_SHADOW)

    # 4. Faja y zapatos
    for y in range(25):
        for x in range(18):
            r, g, b, a = img.getpixel((x, y))
            if a == 0: continue

            if is_shoe(r, g, b, a):
                out.putpixel((x, y), SHOE_MAP.get((r, g, b, a), (0x18, 0x54, 0x20, a)))
            elif y >= 20 and (r, g, b, a) in SHOE_MAP:
                out.putpixel((x, y), SHOE_MAP[(r, g, b, a)])
            elif is_faja(r, g, b, a):
                out.putpixel((x, y), FAJA_MAP.get((r, g, b, a), (0xC0, 0x58, 0x08, a)))

    out.save(os.path.join(DST, f"FRAME{i}.png"))
    print(f"FRAME{i}: shifted={shifted}")

print(f"\n{NOMBRE_SALIDA} listo en: {DST}")
