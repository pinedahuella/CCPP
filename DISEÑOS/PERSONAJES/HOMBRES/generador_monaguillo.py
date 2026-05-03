import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageOps

SRC_DIR = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PERSONAJES\HOMBRES\HOMBRE1"
DST_DIR = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PERSONAJES\HOMBRES\HOMBRE11"
os.makedirs(DST_DIR, exist_ok=True)

W, H = 18, 25

# ── Paleta ─────────────────────────────────────────────────────────────────────
SKIN  = (0xFE, 0xD9, 0x98, 255)
SKNS  = (0xF5, 0xB9, 0x71, 255)
SKND  = (0xD4, 0x94, 0x50, 255)
EYE   = (0x1C, 0x10, 0x10, 255)
HAI1  = (0x28, 0x14, 0x08, 255)   # pelo: sombra
HAI2  = (0x4C, 0x2C, 0x10, 255)   # pelo: base castaño
HAI3  = (0x70, 0x48, 0x1C, 255)   # pelo: brillo (joven)
SOT1  = (0x5C, 0x08, 0x08, 255)   # sotana roja: borde/sombra fuerte
SOT2  = (0x8C, 0x14, 0x14, 255)   # sotana roja: base
SOT3  = (0xB0, 0x28, 0x28, 255)   # sotana roja: pliegue/reflejo
SUR1  = (0xD8, 0xD4, 0xE4, 255)   # sobrepelliz: sombra lateral
SUR2  = (0xF4, 0xF2, 0xFC, 255)   # sobrepelliz: blanco base
SHO   = (0x18, 0x10, 0x10, 255)   # zapatos negros
# Props
BEL1  = (0x8C, 0x5C, 0x10, 255)   # campana: borde oscuro
BEL2  = (0xD4, 0xA0, 0x20, 255)   # campana: cuerpo dorado
BEL3  = (0xF0, 0xD0, 0x50, 255)   # campana: brillo
CND_W = (0xF8, 0xF4, 0xEC, 255)   # vela: cera blanca
CND_Y = (0xF0, 0xD0, 0x30, 255)   # llama: amarillo
CND_O = (0xE8, 0x70, 0x10, 255)   # llama: naranja base
THU1  = (0x6C, 0x40, 0x08, 255)   # incensario: oscuro/borde
THU2  = (0xAC, 0x70, 0x14, 255)   # incensario: cuerpo
CRS2  = (0x8C, 0x58, 0x18, 255)   # baston: madera
CRSG  = (0xD4, 0xA0, 0x20, 255)   # cruz: dorada

# ── Deteccion de colores de HOMBRE1 ───────────────────────────────────────────
def is_hair(r, g, b, a):
    return a > 0 and 0x1C <= r <= 0x50 and r > g * 1.5 and r > b * 1.8

def is_eye(r, g, b, a):
    # Pixel oscuro de ojo/contorno facial en zona central (no borde del pelo)
    return a > 0 and r < 0x35 and g < 0x0C and b < 0x0C

def is_faja(r, g, b, a):
    return a > 0 and r > 140 and r > g * 3 and g > 20

def is_shoe(r, g, b, a):
    return a > 0 and r > 60 and r > g * 3 and g <= 20

def is_pants(r, g, b, a):
    return a > 0 and b > r and b > g and b > 30

def is_teal_body(r, g, b, a):
    return a > 0 and g > 0xC0 and b > 0x80 and r < 0x30

def is_skin(r, g, b, a):
    # Piel calida: r>192, g>112, b>48, Y mas calido que frio (r-b>40)
    # Esto excluye los blancos frios de la sobrepelliz (r-b cerca de 0)
    return a > 0 and r > 0xC0 and g > 0x70 and b > 0x30 and (r - b) > 40

def is_shifted(img):
    return all(img.getpixel((x, 0))[3] == 0 for x in range(W))

# ── Peinado monaguillo: corto peinado a la derecha (distinto al padre) ────────
# El padre sigue la silueta irregular de HOMBRE1 (pico en x0 izquierda).
# El monaguillo tiene forma simetrica y corta, peinado hacia la derecha.
HAIR_MAP = [
    #x: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17
       [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # dy0: 6px top centrado
       [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],  # dy1: se abre
       [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # dy2
       [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # dy3
       [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # dy4: laterales planos
       [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # dy5
       [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # dy6
       [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # dy7 hairline (tapa en x=15)
]

def hair_color(x, dy):
    """Monaguillo: brillo en el tope central, sombra en bordes y base."""
    if x <= 1 or x >= 16 or dy >= 6: return HAI1   # borde duro
    if x <= 3 or x >= 14:            return HAI2   # laterales
    if dy <= 1 and 6 <= x <= 11:     return HAI3   # brillo en la corona central
    return HAI2

def sot_shade(x):
    return SOT1 if (x <= 5 or x >= 13) else (SOT3 if x in (8, 9) else SOT2)

def sur_shade(x):
    return SUR1 if (x <= 5 or x >= 12) else SUR2

# =============================================================================
# MAKE_ACOLYTE — recolorea HOMBRE1 a sotana roja + sobrepelliz blanca
# =============================================================================
def make_acolyte(src_img):
    img = src_img.copy()
    hy0 = 1 if is_shifted(src_img) else 0

    # 1. Recolorear cuerpo (faja, pantalon, zapatos)
    for y in range(H):
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if a == 0: continue
            if is_faja(r, g, b, a):
                img.putpixel((x, y), sot_shade(x)); continue
            if is_pants(r, g, b, a) or is_teal_body(r, g, b, a):
                img.putpixel((x, y), sot_shade(x)); continue
            if is_shoe(r, g, b, a):
                img.putpixel((x, y), SHO); continue

    # 2. Borrar todo el pelo original de HOMBRE1 (dy 0-9)
    # Guardar pixeles de ojo (dy=8-9, zona central x4-x13) para restaurarlos despues
    eye_pixels = {}
    for dy in range(10):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if is_hair(r, g, b, a):
                # Solo en dy=8-9 (zona de ojos) y centro de la cara
                if dy >= 8 and 4 <= x <= 13 and is_eye(r, g, b, a):
                    eye_pixels[(x, y)] = (r, g, b, a)
                img.putpixel((x, y), (0, 0, 0, 0))

    # 3. Pintar nuevo peinado segun HAIR_MAP
    for dy in range(8):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            if HAIR_MAP[dy][x] == 1:
                img.putpixel((x, y), hair_color(x, dy))

    # 4. Patillas (dy 8-9): borde exterior solamente
    for dy in range(8, 10):
        y = hy0 + dy
        if y >= H: break
        for x in range(W):
            r, g, b, a = src_img.getpixel((x, y))
            if is_hair(r, g, b, a) and (x <= 3 or x >= 14) and x != 0 and x != 17:
                img.putpixel((x, y), HAI1)

    # 5. Restaurar pixeles de ojo guardados
    for (x, y), c in eye_pixels.items():
        img.putpixel((x, y), c)

    # Sobrepelliz blanca encima de la sotana (hy0+14 a hy0+20, x5-x12)
    # Respeta piel original (cuello) y pelo
    for cy in range(hy0 + 14, min(hy0 + 21, H)):
        for cx in range(5, 13):
            ro, go, bo, ao = src_img.getpixel((cx, cy))
            if ao == 0: continue
            if is_skin(ro, go, bo, ao): continue   # no tapar cuello/barbilla
            if is_hair(ro, go, bo, ao): continue
            img.putpixel((cx, cy), sur_shade(cx))

    return img

def clean_hands(img):
    """Elimina pixels de piel en zona cuerpo (y15+). Respeta sobrepelliz (blanco frio)."""
    out = img.copy()
    for y in range(15, H):
        for x in range(W):
            r, g, b, a = out.getpixel((x, y))
            if a == 0: continue
            if is_skin(r, g, b, a):
                out.putpixel((x, y), sot_shade(x))
    return out

def px(img, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), color)

# ── Frames 1-8: caminata de frente ────────────────────────────────────────────
for i in range(1, 9):
    src = Image.open(os.path.join(SRC_DIR, f"FRAME{i}.png")).convert("RGBA")
    out = make_acolyte(src)
    out.save(os.path.join(DST_DIR, f"FRAME{i}.png"))
    print(f"FRAME{i} guardado")

# Limpiar frames anteriores
for _n in range(9, 50):
    _p = os.path.join(DST_DIR, f"FRAME{_n}.png")
    if os.path.exists(_p): os.remove(_p)

# BASE limpia para gestos (FRAME1 sin manos laterales)
BASE = clean_hands(make_acolyte(
    Image.open(os.path.join(SRC_DIR, "FRAME1.png")).convert("RGBA")
))

# =============================================================================
# F9 — Orante: ambos brazos levantados (alabanza)
# =============================================================================
f9 = BASE.copy()
px(f9, 4, 15, SOT2); px(f9, 3, 15, SOT1)
px(f9, 3, 14, SOT2); px(f9, 2, 14, SOT1)
px(f9, 2, 13, SOT2); px(f9, 1, 13, SOT1)
px(f9, 1, 12, SOT2); px(f9, 0, 12, SOT1)
px(f9, 0, 11, SKNS); px(f9, 0, 10, SKIN); px(f9, 0, 9, SKIN)
px(f9, 13, 15, SOT2); px(f9, 14, 15, SOT1)
px(f9, 14, 14, SOT2); px(f9, 15, 14, SOT1)
px(f9, 15, 13, SOT2); px(f9, 16, 13, SOT1)
px(f9, 16, 12, SOT2); px(f9, 17, 12, SOT1)
px(f9, 17, 11, SKNS); px(f9, 17, 10, SKIN); px(f9, 17, 9, SKIN)
f9.save(os.path.join(DST_DIR, "FRAME9.png"))
print("FRAME9  — Orante")

# =============================================================================
# F10 — Manos juntas en oracion
# =============================================================================
f10 = BASE.copy()
px(f10, 4, 16, SOT3); px(f10, 5, 16, SOT3)
px(f10, 4, 17, SOT3); px(f10, 5, 17, SOT2)
px(f10, 13, 16, SOT3); px(f10, 12, 16, SOT3)
px(f10, 13, 17, SOT3); px(f10, 12, 17, SOT2)
px(f10,  7, 17, SKNS); px(f10,  8, 17, SKIN); px(f10,  9, 17, SKIN)
px(f10, 10, 17, SKIN); px(f10, 11, 17, SKNS)
px(f10,  7, 18, SKND); px(f10,  8, 18, SKNS); px(f10,  9, 18, SKNS)
px(f10, 10, 18, SKNS); px(f10, 11, 18, SKND)
px(f10,  8, 19, SKND); px(f10,  9, 19, SKND); px(f10, 10, 19, SKND)
px(f10,  6, 17, SOT1); px(f10, 12, 17, SOT1)
f10.save(os.path.join(DST_DIR, "FRAME10.png"))
print("FRAME10 — Manos juntas")

# =============================================================================
# F11 — Campana (campanilla, brazo derecho levantado con campana)
# =============================================================================
f11 = BASE.copy()
# Brazo derecho sube
px(f11, 13, 15, SOT2); px(f11, 14, 15, SOT1)
px(f11, 14, 14, SOT2); px(f11, 14, 13, SOT1)
px(f11, 15, 13, SOT2); px(f11, 15, 12, SOT1)
px(f11, 15, 11, SOT2); px(f11, 16, 11, SOT1)
# Muneca/mano
px(f11, 15, 10, SKNS); px(f11, 16, 10, SKIN)
px(f11, 15,  9, SKND); px(f11, 16,  9, SKNS)
# Campana: mango, cuerpo, boca
px(f11, 15, 8, BEL2); px(f11, 16, 8, BEL1)                              # mango
px(f11, 14, 7, BEL1); px(f11, 15, 7, BEL3); px(f11, 16, 7, BEL2)       # cuerpo
px(f11, 13, 6, BEL1); px(f11, 14, 6, BEL2); px(f11, 15, 6, BEL3)       # boca izq
px(f11, 16, 6, BEL2); px(f11, 17, 6, BEL1)                              # boca der
f11.save(os.path.join(DST_DIR, "FRAME11.png"))
print("FRAME11 — Campana")

# =============================================================================
# F12 — Vela (candle sostenida con ambas manos al pecho)
# =============================================================================
f12 = BASE.copy()
# Llama
px(f12, 8, 7, CND_O)
px(f12, 7, 8, CND_Y); px(f12, 8, 8, CND_O); px(f12, 9, 8, CND_Y)
# Cera (wax)
for cy in range(9, 15):
    px(f12, 8, cy, CND_W)
# Manga + mano izquierda
px(f12, 5, 14, SOT2); px(f12, 4, 14, SOT1)
px(f12, 6, 14, SKNS); px(f12, 7, 14, SKIN)
px(f12, 6, 15, SKND); px(f12, 7, 15, SKNS)
# Manga + mano derecha
px(f12, 12, 14, SOT2); px(f12, 13, 14, SOT1)
px(f12, 11, 14, SKNS); px(f12, 10, 14, SKIN)
px(f12, 11, 15, SKND); px(f12, 10, 15, SKNS)
f12.save(os.path.join(DST_DIR, "FRAME12.png"))
print("FRAME12 — Vela")

# =============================================================================
# F13 — Incensario (thurible, brazo derecho bajando con cadena)
# =============================================================================
f13 = BASE.copy()
# Brazo derecho hacia abajo-derecha
px(f13, 13, 15, SOT2); px(f13, 14, 15, SOT1)
px(f13, 14, 16, SOT2); px(f13, 15, 16, SOT1)
px(f13, 15, 17, SOT2); px(f13, 16, 17, SOT1)
# Mano/muneca
px(f13, 15, 18, SKNS); px(f13, 16, 18, SKIN)
px(f13, 15, 19, SKND); px(f13, 16, 19, SKNS)
# Cadena corta
px(f13, 15, 20, THU1); px(f13, 16, 20, THU1)
# Incensario: 3 filas x 3 cols
px(f13, 14, 21, THU1); px(f13, 15, 21, THU2); px(f13, 16, 21, THU1)
px(f13, 14, 22, THU1); px(f13, 15, 22, THU2); px(f13, 16, 22, THU1)
px(f13, 14, 23, THU1); px(f13, 15, 23, THU1); px(f13, 16, 23, THU1)
f13.save(os.path.join(DST_DIR, "FRAME13.png"))
print("FRAME13 — Incensario")

# =============================================================================
# F14 — Manos extendidas (procesion / bienvenida)
# =============================================================================
f14 = BASE.copy()
px(f14, 3, 16, SOT2); px(f14, 2, 16, SOT1)
px(f14, 3, 17, SOT1); px(f14, 2, 17, SOT2)
px(f14, 1, 16, SKNS); px(f14, 0, 16, SKIN)
px(f14, 1, 17, SKND); px(f14, 0, 17, SKNS)
px(f14, 14, 16, SOT2); px(f14, 15, 16, SOT1)
px(f14, 14, 17, SOT1); px(f14, 15, 17, SOT2)
px(f14, 16, 16, SKNS); px(f14, 17, 16, SKIN)
px(f14, 16, 17, SKND); px(f14, 17, 17, SKNS)
f14.save(os.path.join(DST_DIR, "FRAME14.png"))
print("FRAME14 — Manos extendidas")

# =============================================================================
# F15 — Cruz procesional (sostenida al frente con ambas manos)
# Baston vertical x8, brazo horizontal dorado y9-y10, manos y15-y16
# =============================================================================
f15 = BASE.copy()
# Baston madera
for cy in range(9, 22):
    px(f15, 8, cy, CRS2)
# Cruz dorada: brazo vertical top
px(f15, 8, 9, CRSG); px(f15, 8, 10, CRSG); px(f15, 8, 11, CRSG)
# Brazo horizontal
for cx in range(5, 12):
    px(f15, cx, 10, CRSG)
# Manos sosteniendo el baston
px(f15, 5, 15, SOT2); px(f15, 4, 15, SOT1)
px(f15, 6, 15, SKNS); px(f15, 7, 15, SKIN)
px(f15, 6, 16, SKND); px(f15, 7, 16, SKNS)
px(f15, 12, 15, SOT2); px(f15, 13, 15, SOT1)
px(f15, 11, 15, SKNS); px(f15, 10, 15, SKIN)
px(f15, 11, 16, SKND); px(f15, 10, 16, SKNS)
f15.save(os.path.join(DST_DIR, "FRAME15.png"))
print("FRAME15 — Cruz procesional")

# =============================================================================
# F16-F27 — Señal de la Cruz (12 frames, misma logica que padre)
# =============================================================================
f16 = BASE.copy()
px(f16, 13, 15, SOT3); px(f16, 14, 15, SOT1); px(f16, 14, 14, SOT2); px(f16, 14, 13, SOT1)
px(f16, 14, 12, SKNS); px(f16, 15, 12, SKIN)
f16.save(os.path.join(DST_DIR, "FRAME16.png")); print("FRAME16 — Cruz 1: subiendo")

f17 = BASE.copy()
px(f17, 13, 15, SOT3); px(f17, 14, 15, SOT1); px(f17, 14, 14, SOT2)
px(f17, 15, 13, SOT1); px(f17, 15, 12, SOT2); px(f17, 15, 11, SOT1)
px(f17, 15, 10, SKNS); px(f17, 16, 10, SKIN)
f17.save(os.path.join(DST_DIR, "FRAME17.png")); print("FRAME17 — Cruz 2: subiendo")

f18 = BASE.copy()
px(f18, 13, 15, SOT3); px(f18, 14, 15, SOT1); px(f18, 14, 14, SOT2); px(f18, 14, 13, SOT1)
px(f18, 15, 12, SOT2); px(f18, 15, 11, SOT1); px(f18, 16, 10, SOT2)
px(f18, 15,  9, SKNS); px(f18, 16,  9, SKIN)
px(f18, 15,  8, SKND); px(f18, 16,  8, SKNS)
f18.save(os.path.join(DST_DIR, "FRAME18.png")); print("FRAME18 — Cruz 3: frente KEY")

f19 = BASE.copy()
px(f19, 13, 15, SOT3); px(f19, 14, 15, SOT1); px(f19, 14, 14, SOT2)
px(f19, 14, 13, SOT1); px(f19, 14, 12, SOT2)
px(f19, 14, 11, SKNS); px(f19, 15, 11, SKIN); px(f19, 15, 10, SKND)
f19.save(os.path.join(DST_DIR, "FRAME19.png")); print("FRAME19 — Cruz 4: bajando")

f20 = BASE.copy()
px(f20, 13, 15, SOT3); px(f20, 13, 16, SOT2); px(f20, 12, 16, SOT1)
px(f20, 11, 16, SOT2); px(f20, 10, 16, SOT1)
px(f20,  9, 15, SKNS); px(f20, 10, 15, SKIN)
px(f20,  8, 16, SKND); px(f20,  9, 16, SKNS); px(f20, 10, 16, SKIN); px(f20,  8, 17, SOT1)
f20.save(os.path.join(DST_DIR, "FRAME20.png")); print("FRAME20 — Cruz 5: pecho KEY")

f21 = BASE.copy()
px(f21, 13, 15, SOT2); px(f21, 12, 16, SOT1); px(f21, 11, 16, SOT2)
px(f21, 10, 16, SOT1); px(f21,  9, 16, SOT2)
px(f21,  8, 16, SKNS); px(f21,  7, 16, SKIN)
px(f21,  8, 15, SKND); px(f21,  7, 15, SKNS)
f21.save(os.path.join(DST_DIR, "FRAME21.png")); print("FRAME21 — Cruz 6: hacia hombro izq")

f22 = BASE.copy()
px(f22, 13, 16, SOT2); px(f22, 12, 16, SOT1); px(f22, 11, 16, SOT2)
px(f22, 10, 16, SOT1); px(f22,  9, 16, SOT2)
px(f22,  8, 16, SOT1); px(f22,  7, 16, SOT2); px(f22,  6, 16, SOT1)
px(f22,  5, 15, SKNS); px(f22,  4, 15, SKIN)
px(f22,  5, 16, SKND); px(f22,  4, 16, SKNS)
f22.save(os.path.join(DST_DIR, "FRAME22.png")); print("FRAME22 — Cruz 7: hombro izq KEY")

f23 = BASE.copy()
px(f23, 13, 15, SOT2); px(f23, 12, 15, SOT1); px(f23, 11, 15, SOT2)
px(f23, 10, 15, SOT1); px(f23,  9, 15, SOT2)
px(f23,  8, 15, SKNS); px(f23,  7, 15, SKIN); px(f23,  7, 14, SKND)
f23.save(os.path.join(DST_DIR, "FRAME23.png")); print("FRAME23 — Cruz 8: cruzando 1/3")

f24 = BASE.copy()
px(f24, 13, 15, SOT2); px(f24, 12, 15, SOT1); px(f24, 11, 15, SOT2)
px(f24, 11, 14, SKNS); px(f24, 10, 14, SKIN); px(f24, 11, 13, SKND)
f24.save(os.path.join(DST_DIR, "FRAME24.png")); print("FRAME24 — Cruz 9: cruzando 2/3")

f25 = BASE.copy()
px(f25, 13, 15, SOT3); px(f25, 14, 15, SOT2); px(f25, 14, 14, SOT1); px(f25, 13, 14, SOT2)
px(f25, 14, 13, SKNS); px(f25, 15, 13, SKIN)
px(f25, 13, 13, SKND); px(f25, 15, 14, SKNS)
f25.save(os.path.join(DST_DIR, "FRAME25.png")); print("FRAME25 — Cruz 10: hombro der KEY")

f26 = BASE.copy()
px(f26, 13, 15, SOT3); px(f26, 13, 14, SOT2); px(f26, 12, 14, SOT1); px(f26, 12, 13, SOT2)
px(f26, 11, 13, SKIN); px(f26, 12, 13, SKNS); px(f26, 11, 12, SKND)
f26.save(os.path.join(DST_DIR, "FRAME26.png")); print("FRAME26 — Cruz 11: hacia labios")

f27 = BASE.copy()
px(f27, 13, 15, SOT3); px(f27, 12, 15, SOT2); px(f27, 12, 14, SOT1)
px(f27, 11, 14, SOT2); px(f27, 11, 13, SOT1); px(f27, 10, 13, SOT2)
px(f27, 10, 12, SKNS); px(f27,  9, 12, SKIN); px(f27, 11, 12, SKND)
px(f27,  9, 11, SKNS); px(f27, 10, 11, SKIN)
f27.save(os.path.join(DST_DIR, "FRAME27.png")); print("FRAME27 — Cruz 12: beso KEY")

# =============================================================================
# ESPALDAS
# =============================================================================
def make_back_view(front_img):
    img = ImageOps.mirror(front_img).copy()
    head_px = set()
    for y in range(18):          # capturar hasta y17 inclusive
        for x in range(W):
            if img.getpixel((x, y))[3] > 0:
                head_px.add((x, y))
    for y in range(18):          # limpiar hasta y17 inclusive
        for x in range(W):
            img.putpixel((x, y), (0, 0, 0, 0))
    for (x, y) in head_px:
        if y <= 7:
            if x == 0 or x >= 16: continue  # copa max x=15
            # Copa: borde muy oscuro, interior medio, centro brillo
            if x <= 1 or x >= 15:    c = HAI1
            elif x <= 3 or x >= 14:  c = HAI2
            else:                    c = HAI3 if y <= 2 else HAI2
            img.putpixel((x, y), c)
        elif y <= 11:
            if x == 0 or x >= 16: continue  # nuca nunca toca el borde (max x=15)
            # Nuca: pelo corto cubre parte trasera de la cabeza
            img.putpixel((x, y), HAI1 if (x <= 2 or x >= 15) else HAI2)
        elif y <= 14:
            # Cuello visible desde atras (mismas filas que barbilla al frente)
            if x <= 3 or x >= 14:
                img.putpixel((x, y), SKND)   # borde oscuro cuello
            else:
                img.putpixel((x, y), SKNS if y == 12 else SKIN)
        else:
            # y15+: cuello/hombros de la sotana roja (alineado con inicio cuerpo frente)
            if x == 0 or x == 17: continue
            img.putpixel((x, y), SOT1 if (x <= 4 or x >= 13) else SOT2)
    return img

# F28-F32: caminata espaldas (flip F1-F5)
for i in range(1, 6):
    src = Image.open(os.path.join(DST_DIR, f"FRAME{i}.png")).convert("RGBA")
    back = make_back_view(src)
    back.save(os.path.join(DST_DIR, f"FRAME{27+i}.png"))
    print(f"FRAME{27+i} — Espaldas caminando (flip F{i})")

# F33: parado espaldas
f33 = make_back_view(Image.open(os.path.join(DST_DIR, "FRAME1.png")).convert("RGBA"))
f33.save(os.path.join(DST_DIR, "FRAME33.png"))
print("FRAME33 — Espaldas: parado")

# F34: sentado espaldas (sin piernas)
f34 = make_back_view(Image.open(os.path.join(DST_DIR, "FRAME1.png")).convert("RGBA"))
for x in range(W):
    for y in range(19, H):
        f34.putpixel((x, y), (0, 0, 0, 0))
f34.save(os.path.join(DST_DIR, "FRAME34.png"))
print("FRAME34 — Espaldas: sentado")

# =============================================================================
# FRAMES 36-39 — Caminando con Biblia (basados en F1-F4)
# =============================================================================
BK1  = (0x4C, 0x28, 0x08, 255)
BK2  = (0x78, 0x44, 0x14, 255)
BKP  = (0xEC, 0xE8, 0xD8, 255)
BKX  = (0xC0, 0x60, 0x08, 255)

def _draw_bible_mon(out):
    px(out,  4,15,SOT2); px(out,  5,15,SOT1)
    px(out,  4,16,SOT2); px(out,  5,16,SOT1)
    px(out, 13,15,SOT2); px(out, 12,15,SOT1)
    px(out, 13,16,SOT2); px(out, 12,16,SOT1)
    px(out,  4,17,SKNS); px(out,  4,18,SKND)
    px(out, 13,17,SKNS); px(out, 13,18,SKND)
    # Brazo derecho extendido al lado del libro
    px(out, 14,16,SOT1); px(out, 14,17,SOT1)
    px(out, 14,18,SOT1); px(out, 14,19,SOT1)
    # Zapato visible a la derecha del libro
    px(out, 13,20,SHO); px(out, 13,21,SHO)
    for _bx in range(5, 13):
        for _by in range(17, 22):
            if   _bx in (5,12):   _c = BK1
            elif _by in (17,21):  _c = BK1
            elif _bx in (6,11):   _c = BK2
            else:                 _c = BKP
            px(out, _bx, _by, _c)
    px(out, 8,18,BKX); px(out, 8,19,BKX); px(out, 8,20,BKX)
    px(out, 7,19,BKX); px(out, 9,19,BKX)

for _i in range(1, 2):
    _p = os.path.join(DST_DIR, f"FRAME{_i}.png")
    if not os.path.exists(_p): continue
    _src = Image.open(_p).convert("RGBA")
    _frm = _src.copy()
    for _y in range(15, H):
        for _x in range(W):
            _r, _g, _b, _a = _src.getpixel((_x, _y))
            if _a == 0 or not is_skin(_r, _g, _b, _a): continue
            _frm.putpixel((_x, _y), sot_shade(_x))
    _draw_bible_mon(_frm)
    _frm.save(os.path.join(DST_DIR, f"FRAME{35+_i}.png"))
    print(f"FRAME{35+_i} — Caminando con Biblia (base F{_i})")
for _fn in [37, 38, 39]:
    _fp = os.path.join(DST_DIR, f"FRAME{_fn}.png")
    if os.path.exists(_fp): os.remove(_fp)

# =============================================================================
# FRAMES 44-45 — Cantando (levanta/agacha + boca)
# =============================================================================
def _shift_up_m(src):
    out = Image.new("RGBA", (W, H), (0,0,0,0))
    for _y in range(1, H):
        for _x in range(W):
            out.putpixel((_x, _y-1), src.getpixel((_x, _y)))
    return out

_f1_mon = Image.open(os.path.join(DST_DIR, "FRAME1.png")).convert("RGBA")
MOT = (0x28, 0x10, 0x08, 255)
_ym = 11  # F1 no esta desplazado (hy0=0)

f45 = _shift_up_m(_f1_mon)
px(f45, 8, _ym,   MOT)
px(f45, 8, _ym-1, MOT)
f45.save(os.path.join(DST_DIR, "FRAME45.png"))
print("FRAME45 — Cantando: boca abierta 2px")

f44 = f45.copy()
for _cy in range(14, H):
    for _cx in range(4):      f44.putpixel((_cx,_cy),(0,0,0,0))
    for _cx in range(14, W): f44.putpixel((_cx,_cy),(0,0,0,0))
for _cy in range(16, H):
    for _cx in range(4, 14):
        _r,_g,_b,_a = f44.getpixel((_cx,_cy))
        if _a > 0 and is_skin(_r,_g,_b,_a): f44.putpixel((_cx,_cy),(0,0,0,0))
px(f44, 3,14,SOT1); px(f44, 2,13,SOT1)
px(f44, 1,12,SOT2); px(f44, 0,11,SKNS); px(f44, 0,10,SKIN)
px(f44,14,14,SOT1); px(f44,15,13,SOT1)
px(f44,16,12,SOT2); px(f44,17,11,SKNS); px(f44,17,10,SKIN)
f44.save(os.path.join(DST_DIR, "FRAME44.png"))
print("FRAME44 — Cantando: boca 2px + brazos levantados")

_f1_mon_back = Image.open(os.path.join(DST_DIR, "FRAME1.png")).convert("RGBA")

def _limpiar_brazos_m(img, y0=15, y1=22):
    for _cy in range(y0, y1):
        for _cx in range(4):      img.putpixel((_cx,_cy),(0,0,0,0))
        for _cx in range(14, W): img.putpixel((_cx,_cy),(0,0,0,0))
    for _cy in range(max(y0, 18), y1):
        for _cx in range(4, 14):
            _r,_g,_b,_a = img.getpixel((_cx,_cy))
            if _a > 0 and is_skin(_r,_g,_b,_a):
                img.putpixel((_cx,_cy),(0,0,0,0))

def _hombros_m(img):
    for _cy in range(15, 18):
        px(img, 4,_cy,SOT1); px(img,13,_cy,SOT1)

_msh = [(_r,_g,_b,255) for _sy in range(21,H) for _sx in range(W)
        for _r,_g,_b,_a in [_f1_mon_back.getpixel((_sx,_sy))]
        if _a>0 and _r<0xC0]
_msh_s = sorted(set(_msh), key=lambda c:c[0]+c[1]+c[2]) if _msh else []
MSHD = _msh_s[0] if _msh_s else SOT1
MSHM = _msh_s[min(len(_msh_s)//3,len(_msh_s)-1)] if _msh_s else SOT2

# F46: Incarse (arrodillado de espaldas)
f46 = make_back_view(_f1_mon_back)
for _cx in range(W):
    for _cy in range(15, H): f46.putpixel((_cx,_cy),(0,0,0,0))
for _cy in range(15, 18):
    for _cx in range(4, 14): f46.putpixel((_cx,_cy), SOT1 if (_cx<=5 or _cx>=12) else SOT2)
for _cx in range(4, 14): f46.putpixel((_cx,18), SOT1 if (_cx<=5 or _cx>=12) else SOT2)
for _cy in range(19, 21):
    px(f46,3,_cy,SOT1); px(f46,4,_cy,SOT2); px(f46,5,_cy,SOT2); px(f46,6,_cy,SOT1)
    px(f46,11,_cy,SOT1); px(f46,12,_cy,SOT2); px(f46,13,_cy,SOT2); px(f46,14,_cy,SOT1)
for _cx in range(4, 8):  f46.putpixel((_cx,21), MSHD if (_cx==4 or _cx==7) else MSHM)
for _cx in range(10,14): f46.putpixel((_cx,21), MSHD if (_cx==10 or _cx==13) else MSHM)
f46.save(os.path.join(DST_DIR, "FRAME46.png"))
print("FRAME46 — Incarse de espaldas")

# F47: Padre Nuestro de espaldas (brazos horizontales)
f47 = make_back_view(_f1_mon_back)
_limpiar_brazos_m(f47); _hombros_m(f47)
px(f47,3,15,SOT1); px(f47,2,15,SOT1); px(f47,1,15,SKNS); px(f47,0,15,SKIN)
px(f47,3,16,SOT1); px(f47,2,16,SOT1); px(f47,1,16,SKNS); px(f47,0,16,SKND)
px(f47,14,15,SOT1); px(f47,15,15,SOT1); px(f47,16,15,SKNS); px(f47,17,15,SKIN)
px(f47,14,16,SOT1); px(f47,15,16,SOT1); px(f47,16,16,SKNS); px(f47,17,16,SKND)
f47.save(os.path.join(DST_DIR, "FRAME47.png"))
print("FRAME47 — Padre Nuestro de espaldas")

# F48: Dar la paz de espaldas (brazo derecho extendido)
f48 = make_back_view(_f1_mon_back)
_limpiar_brazos_m(f48); _hombros_m(f48)
px(f48,14,15,SOT1); px(f48,15,15,SOT1)
px(f48,14,16,SOT1); px(f48,15,16,SOT2); px(f48,16,16,SKNS)
px(f48,16,17,SKNS); px(f48,17,17,SKIN)
px(f48,17,18,SKIN)
f48.save(os.path.join(DST_DIR, "FRAME48.png"))
print("FRAME48 — Dar la paz de espaldas")

# F49: Levantar manos de espaldas (ambos brazos completamente arriba)
f49 = make_back_view(_f1_mon_back)
_limpiar_brazos_m(f49, 9, 22); _hombros_m(f49)
px(f49, 3,15,SOT1); px(f49,2,15,SOT1)
px(f49, 3,14,SOT1); px(f49,2,14,SOT1)
px(f49, 2,13,SOT1); px(f49,1,13,SOT2)
px(f49, 2,12,SOT1); px(f49,1,12,SOT2)
px(f49, 1,11,SOT2); px(f49,0,11,SKNS)
px(f49, 0,10,SKNS); px(f49,0,9,SKIN)
px(f49,14,15,SOT1); px(f49,15,15,SOT1)
px(f49,14,14,SOT1); px(f49,15,14,SOT1)
px(f49,15,13,SOT1); px(f49,16,13,SOT2)
px(f49,15,12,SOT1); px(f49,16,12,SOT2)
px(f49,16,11,SOT2); px(f49,17,11,SKNS)
px(f49,17,10,SKNS); px(f49,17,9,SKIN)
# Restaurar nuca borrada por _limpiar donde el brazo no cubre (y=9-11)
px(f49, 1,9,HAI1);  px(f49,2,9,HAI1);  px(f49,3,9,HAI2)
px(f49, 1,10,HAI1); px(f49,2,10,HAI1); px(f49,3,10,HAI2)
px(f49, 2,11,HAI1); px(f49,3,11,HAI2)
px(f49,14,9,HAI2);  px(f49,15,9,HAI1)
px(f49,14,10,HAI2); px(f49,15,10,HAI1)
px(f49,14,11,HAI2); px(f49,15,11,HAI1)
f49.save(os.path.join(DST_DIR, "FRAME49.png"))
print("FRAME49 — Levantar manos de espaldas")

print(f"""
HOMBRE11 (Monaguillo) — 49 frames
  Sotana roja + sobrepelliz blanca
  F1-F8   caminata frente
  F9      orante
  F10     manos juntas
  F11     campana
  F12     vela
  F13     incensario
  F14     manos extendidas
  F15     cruz procesional
  F16-F27 señal de la cruz (12 frames)
  F28-F32 espaldas caminando
  F33     espaldas parado
  F34     espaldas sentado
  F36-F39 caminando con Biblia (F1-F4)
  F44     cantando: levanta, 1px boca
  F45     cantando: boca abierta, 2px vertical
  {DST_DIR}""")
