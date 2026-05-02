import sys
sys.stdout.reconfigure(encoding='utf-8')
"""
Generador HOMBRE10 — Padre / Sacerdote Catolico
================================================
18 x 25 px RGBA, 15 frames:
  F01-F08  — animacion de caminar (base HOMBRE1 recoloreada)
  F10      — Orante: ambas manos levantadas hacia arriba
  F11      — Manos juntas en oracion (rezando)
  F12      — Mano derecha levantada (bendicion)
  F13      — Mano en el pecho (gesto de devocion)
  F14      — Manos extendidas a los lados (bienvenida/abrazo)
  F15      — Sosteniendo el libro sagrado (Biblia/misal)
"""

from PIL import Image
import os

SRC_DIR = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PERSONAJES\HOMBRES\HOMBRE1"
DST_DIR = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PERSONAJES\HOMBRES\HOMBRE10"
os.makedirs(DST_DIR, exist_ok=True)

W, H = 18, 25

# ── Paleta del padre ────────────────────────────────────────────────────────
OUT   = (0x08, 0x06, 0x06, 255)   # contorno
SKIN  = (0xFE, 0xD9, 0x98, 255)   # piel clara (palmas, frente)
SKNS  = (0xF5, 0xB9, 0x71, 255)   # piel media (dorso mano, sombra)
SKND  = (0xD4, 0x94, 0x50, 255)   # piel oscura (sombra borde dedo)
EYE   = (0x1C, 0x10, 0x10, 255)
HAI1  = (0x14, 0x08, 0x04, 255)   # pelo sombra dura
HAI2  = (0x28, 0x10, 0x08, 255)   # pelo oscuro
HAI3  = (0x40, 0x1A, 0x10, 255)   # pelo reflejos
WHT   = (0xF2, 0xF2, 0xF4, 255)   # cuello blanco
WHTD  = (0xC4, 0xC0, 0xCC, 255)   # cuello sombra
SOT1  = (0x10, 0x10, 0x18, 255)   # sotana borde/sombra fuerte
SOT2  = (0x18, 0x18, 0x24, 255)   # sotana negro base
SOT3  = (0x26, 0x26, 0x36, 255)   # sotana pliegue / reflejo central
SHO   = (0x12, 0x10, 0x14, 255)   # zapato negro
BOOK1 = (0x4C, 0x28, 0x08, 255)   # libro: cubierta oscura
BOOK2 = (0x78, 0x44, 0x14, 255)   # libro: cubierta clara
BOOKP = (0xEC, 0xE8, 0xD8, 255)   # libro: paginas
BOOKX = (0xC0, 0x60, 0x08, 255)   # libro: cruz dorada

# ── Deteccion de colores de HOMBRE1 ──────────────────────────────────────────
def is_hair(r, g, b, a):
    return a > 0 and 0x1C <= r <= 0x50 and r > g * 1.5 and r > b * 1.8

def is_faja(r, g, b, a):
    return a > 0 and r > 140 and r > g * 3 and g > 20

def is_shoe(r, g, b, a):
    return a > 0 and r > 60 and r > g * 3 and g <= 20

def is_pants(r, g, b, a):
    return a > 0 and b > r and b > g and b > 30

def is_teal_body(r, g, b, a):
    # Color especial (12,DD,B0) de HOMBRE1 FRAME9 (brazos extendidos)
    return a > 0 and g > 0xC0 and b > 0x80 and r < 0x30

def is_skin(r, g, b, a):
    return a > 0 and r > 0xC0 and g > 0x70 and b > 0x30

def is_shifted(img):
    return all(img.getpixel((x, 0))[3] == 0 for x in range(W))

# ── Color del pelo por posicion ──────────────────────────────────────────────
def hair_color(x, dy):
    if x <= 1 or x >= 16 or dy >= 6: return HAI1
    if x <= 3 or x >= 14:            return HAI2
    if dy <= 1:                       return HAI3
    return HAI2

# ── Recolorear HOMBRE1 frame a sotana negra ──────────────────────────────────
def make_priest(src_img):
    img = src_img.copy()
    shifted = is_shifted(img)
    hy0 = 1 if shifted else 0

    for y in range(H):
        for x in range(W):
            r, g, b, a = img.getpixel((x, y))
            if a == 0: continue
            dy = y - hy0

            if 0 <= dy <= 9 and is_hair(r, g, b, a):
                if x != 0 and x != 17:  # pelo nunca toca el borde
                    img.putpixel((x, y), hair_color(x, dy) if dy <= 7 else HAI1)
                continue
            if is_faja(r, g, b, a):
                shade = SOT1 if (x <= 5 or x >= 13) else (SOT3 if x in (8,9) else SOT2)
                img.putpixel((x, y), shade); continue
            if is_pants(r, g, b, a) or is_teal_body(r, g, b, a):
                shade = SOT1 if (x <= 5 or x >= 13) else SOT2
                img.putpixel((x, y), shade); continue
            if is_shoe(r, g, b, a):
                img.putpixel((x, y), SHO); continue

    # Cuello romano blanco
    hy = hy0
    cy_chin = hy + 14
    cy_col  = hy + 15
    if cy_chin < H:
        for cx in range(7, 11):
            r, g, b, a = img.getpixel((cx, cy_chin))
            if a > 0: img.putpixel((cx, cy_chin), WHTD)
    if cy_col < H:
        for cx in range(7, 11):
            r, g, b, a = img.getpixel((cx, cy_col))
            if a > 0: img.putpixel((cx, cy_col), WHT)
    return img

# ── Base limpia para gestos: sin manos laterales ─────────────────────────────
# En HOMBRE1 y18-y19: x4-x5 y x13-x14 son piel (manos a los lados de la cintura)
# Para los gestos se eliminan esas manos y se cierran con sotana.
def clean_hands(img):
    """Elimina pixeles de piel residuales en zona del cuerpo (y15-y24)."""
    out = img.copy()
    for y in range(15, H):
        for x in range(W):
            r, g, b, a = out.getpixel((x, y))
            if a == 0: continue
            # Saltar cuello blanco (y15, x7-x10)
            if y == 15 and 7 <= x <= 10:
                continue
            # Piel en zona del cuerpo → sotana
            if is_skin(r, g, b, a):
                shade = SOT1 if (x <= 5 or x >= 13) else (SOT3 if x in (8,9) else SOT2)
                out.putpixel((x, y), shade)
    return out

# ── Pintar pixel seguro ───────────────────────────────────────────────────────
def px(img, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), color)

# ── Frames 1-8: animacion de caminar ─────────────────────────────────────────
for i in range(1, 9):
    src = Image.open(os.path.join(SRC_DIR, f"FRAME{i}.png")).convert("RGBA")
    out = make_priest(src)
    out.save(os.path.join(DST_DIR, f"FRAME{i}.png"))
    print(f"FRAME{i} guardado")

# Eliminar FRAME9 si existe (ya no es necesario)
f9 = os.path.join(DST_DIR, "FRAME9.png")
if os.path.exists(f9):
    os.remove(f9)
    print("FRAME9 eliminado")

# ── Base de gestos: Frame1 recoloreado SIN manos laterales ───────────────────
BASE = clean_hands(make_priest(
    Image.open(os.path.join(SRC_DIR, "FRAME1.png")).convert("RGBA")
))

# =============================================================================
# FRAME 10 — Orante: ambas manos levantadas (alabanza / oracion de alabanza)
# Brazos suben diagonalmente hacia arriba-afuera desde los hombros.
# La manga de la sotana (SOT) sube por FUERA del cuerpo (columnas x2-x3 izq
# y x14-x15 der, que estan transparentes en esa zona) → visible contra fondo.
# La mano (piel) aparece al nivel del ojo exterior.
# =============================================================================
f10 = BASE.copy()

# ── Brazo IZQUIERDO — diagonal hacia arriba-izquierda hasta borde del canvas ──
# La cara ocupa hasta x1 en y9-y10, así que la mano va a x=0 (extremo).
# Manga sotana (2px ancho diagonal): cada 2 filas avanza 1px a la izq.
px(f10, 4, 15, SOT2)   # salida del hombro
px(f10, 3, 15, SOT1)
px(f10, 3, 14, SOT2)   # y14: diagonal izq
px(f10, 2, 14, SOT1)
px(f10, 2, 13, SOT2)   # y13: x2 libre (cara termina ~x5)
px(f10, 1, 13, SOT1)
px(f10, 1, 12, SOT2)   # y12: x1 libre (cara termina ~x4)
px(f10, 0, 12, SOT1)   # borde exterior de la manga (cuff)
# Mano izquierda — x=0 está FUERA de la cara en y9-y11
px(f10, 0, 11, SKNS)   # muneca
px(f10, 0, 10, SKIN)   # palma
px(f10, 0,  9, SKIN)   # punta dedos

# ── Brazo DERECHO — espejo hacia arriba-derecha hasta x=17 ───────────────────
px(f10, 13, 15, SOT2)
px(f10, 14, 15, SOT1)
px(f10, 14, 14, SOT2)
px(f10, 15, 14, SOT1)
px(f10, 15, 13, SOT2)
px(f10, 16, 13, SOT1)
px(f10, 16, 12, SOT2)
px(f10, 17, 12, SOT1)   # borde exterior manga (cuff)
# Mano derecha — x=17 fuera de la cara
px(f10, 17, 11, SKNS)
px(f10, 17, 10, SKIN)
px(f10, 17,  9, SKIN)

f10.save(os.path.join(DST_DIR, "FRAME10.png"))
print("FRAME10 guardado — Orante (ambas manos arriba)")

# =============================================================================
# FRAME 11 — Manos juntas en oracion
# Los dos antebrazos convergen al centro del pecho.
# Se ven mangas desde cada lado, y las manos unidas en el centro con sombras.
# =============================================================================
f11 = BASE.copy()

# ── Mangas convergiendo al centro desde cada hombro ──────────────────────────
# Manga izquierda: se recoge hacia el centro con pliegue mas claro (SOT3)
px(f11, 4, 16, SOT3)   # pliegue manga izq
px(f11, 5, 16, SOT3)
px(f11, 4, 17, SOT3)
px(f11, 5, 17, SOT2)
# Manga derecha
px(f11, 13, 16, SOT3)
px(f11, 12, 16, SOT3)
px(f11, 13, 17, SOT3)
px(f11, 12, 17, SOT2)

# ── Manos juntas al centro del pecho (y17-y18, x7-x11) ──────────────────────
# Capa superior: manos con luz
px(f11,  7, 17, SKNS)
px(f11,  8, 17, SKIN)
px(f11,  9, 17, SKIN)
px(f11, 10, 17, SKIN)
px(f11, 11, 17, SKNS)
# Capa media: dedos con sombra
px(f11,  7, 18, SKND)
px(f11,  8, 18, SKNS)
px(f11,  9, 18, SKNS)
px(f11, 10, 18, SKNS)
px(f11, 11, 18, SKND)
# Sombra inferior (donde las manos se unen a la sotana)
px(f11,  8, 19, SKND)
px(f11,  9, 19, SKND)
px(f11, 10, 19, SKND)
# Contorno exterior de las manos (outline tenue)
px(f11,  6, 17, SOT1)
px(f11, 12, 17, SOT1)
px(f11,  7, 19, SOT1)
px(f11, 11, 19, SOT1)

f11.save(os.path.join(DST_DIR, "FRAME11.png"))
print("FRAME11 guardado — Manos juntas en oracion")

# =============================================================================
# FRAME 12 — Mano derecha levantada (bendicion sacerdotal)
# Solo brazo derecho sube. Brazo izquierdo: sotana limpia.
# =============================================================================
f12 = BASE.copy()

# ── Brazo derecho arriba (mismo que F10 lado derecho) ────────────────────────
px(f12, 13, 15, SOT2)
px(f12, 14, 15, SOT1)
px(f12, 14, 14, SOT2)
px(f12, 14, 13, SOT1)
px(f12, 15, 13, SOT2)
px(f12, 15, 12, SOT1)
px(f12, 15, 11, SOT2)
px(f12, 16, 11, SOT1)
# Mano de bendicion: 2 dedos levantados (index + medio)
px(f12, 15, 10, SKNS)
px(f12, 16, 10, SKIN)
px(f12, 15,  9, SKNS)  # dedo indice
px(f12, 16,  9, SKIN)
px(f12, 16,  8, SKIN)  # punta dedo
px(f12, 15,  8, SKND)  # sombra entre dedos

f12.save(os.path.join(DST_DIR, "FRAME12.png"))
print("FRAME12 guardado — Mano derecha en bendicion")

# =============================================================================
# FRAME 13 — Mano en el pecho (gesto de devocion / fe)
# Antebrazo derecho doblado horizontalmente, mano sobre el corazon.
# =============================================================================
f13 = BASE.copy()

# ── Manga derecha se dobla hacia el centro ────────────────────────────────────
# Codo visible como pliegue de manga
px(f13, 13, 15, SOT3)  # hombro der ligeramente mas claro
px(f13, 13, 16, SOT3)
px(f13, 13, 17, SOT1)  # codo (linea de pliegue oscura)
px(f13, 12, 16, SOT3)
px(f13, 12, 17, SOT2)  # antebrazo va hacia centro
px(f13, 11, 17, SOT2)
# Muneca + transicion a piel
px(f13, 11, 16, SKND)  # muneca sombra
# Mano sobre el pecho (centro-derecha del torso)
px(f13, 10, 15, SKNS)  # dorso de mano
px(f13, 11, 15, SKND)
px(f13,  9, 16, SKIN)  # palma
px(f13, 10, 16, SKIN)
px(f13,  9, 17, SKNS)  # sombra palma
px(f13, 10, 17, SKND)

f13.save(os.path.join(DST_DIR, "FRAME13.png"))
print("FRAME13 guardado — Mano en el pecho")

# =============================================================================
# FRAME 14 — Manos extendidas a los lados (gesto de bienvenida / abrazo)
# Ambos brazos salen horizontalmente por fuera del cuerpo.
# Al igual que F10, la manga va por columnas transparentes adyacentes.
# =============================================================================
f14 = BASE.copy()

# ── Brazo IZQUIERDO horizontal (nivel y16-y17, hacia x0) ─────────────────────
px(f14, 3, 16, SOT2)   # extension izq del hombro
px(f14, 2, 16, SOT1)
px(f14, 3, 17, SOT1)   # sombra inferior manga
px(f14, 2, 17, SOT2)
# Mano izquierda al final del brazo
px(f14, 1, 16, SKNS)   # dorso mano
px(f14, 0, 16, SKIN)   # palma hacia afuera
px(f14, 1, 17, SKND)   # sombra debajo
px(f14, 0, 17, SKNS)

# ── Brazo DERECHO horizontal (nivel y16-y17, hacia x17) ──────────────────────
px(f14, 14, 16, SOT2)
px(f14, 15, 16, SOT1)
px(f14, 14, 17, SOT1)
px(f14, 15, 17, SOT2)
# Mano derecha
px(f14, 16, 16, SKNS)
px(f14, 17, 16, SKIN)
px(f14, 16, 17, SKND)
px(f14, 17, 17, SKNS)

f14.save(os.path.join(DST_DIR, "FRAME14.png"))
print("FRAME14 guardado — Manos extendidas (bienvenida)")

# =============================================================================
# FRAME 15 — Sosteniendo el libro sagrado (Biblia / Misal)
# El libro cubre el torso central; ambas manos lo sujetan por los lados.
# =============================================================================
f15 = BASE.copy()

# ── Libro (x6-x11, y15-y19) ──────────────────────────────────────────────────
for bx in range(6, 12):
    for by in range(15, 20):
        if bx == 6 or bx == 11:             c = BOOK1          # lomo / canto
        elif by == 15 or by == 19:          c = BOOK1          # tapa arr/abj
        elif bx == 7 or bx == 10:           c = BOOK2          # borde cubierta
        else:                               c = BOOKP          # paginas interior
        px(f15, bx, by, c)

# Cruz dorada en la cubierta
px(f15,  8, 16, BOOKX)
px(f15,  8, 17, BOOKX)
px(f15,  8, 18, BOOKX)   # brazo vertical
px(f15,  7, 17, BOOKX)
px(f15,  9, 17, BOOKX)   # brazo horizontal

# ── Manos sosteniendo el libro (ambos lados) ──────────────────────────────────
# Mano izquierda: asoma por debajo del libro por la izquierda
px(f15,  5, 17, SKNS)   # dorso
px(f15,  5, 18, SKIN)   # palma
px(f15,  4, 18, SKNS)   # dedo pulgar
px(f15,  5, 19, SKND)   # sombra

# Mano derecha: asoma por debajo del libro por la derecha
px(f15, 12, 17, SKNS)
px(f15, 12, 18, SKIN)
px(f15, 13, 18, SKNS)
px(f15, 12, 19, SKND)

# ── Mangas (sotana) detras del libro ─────────────────────────────────────────
px(f15, 4, 16, SOT3)
px(f15, 4, 17, SOT2)
px(f15, 13, 16, SOT3)
px(f15, 13, 17, SOT2)

f15.save(os.path.join(DST_DIR, "FRAME15.png"))
print("FRAME15 guardado — Sosteniendo el libro sagrado")

# Limpiar solo los frames que genera el script (NO tocar F28-F35: hechos a mano)
for _n in list(range(16, 28)) + list(range(36, 50)):
    _p = os.path.join(DST_DIR, f"FRAME{_n}.png")
    if os.path.exists(_p): os.remove(_p)
for _pn in ["PREVIEW_PADRE.png", "preview_v3.png"]:
    _p = os.path.join(DST_DIR, _pn)
    if os.path.exists(_p): os.remove(_p)

# =============================================================================
# FRAMES 16-27 — Señal de la Cruz (12 frames suaves)
# El brazo derecho se mueve ~2-3px por frame para no saltar de golpe.
# F16-F18: brazo sube a la frente   (3 frames)
# F19-F20: baja al pecho            (2 frames)
# F21-F22: cruza al hombro izq      (2 frames)
# F23-F25: cruza al hombro der      (3 frames — trayecto mas largo)
# F26-F27: sube a los labios/beso   (2 frames)
# =============================================================================

# ── F16 — Brazo empezando a subir (1/3 hacia la frente) ──────────────────────
f16 = BASE.copy()
px(f16, 13, 15, SOT3)
px(f16, 14, 15, SOT1); px(f16, 14, 14, SOT2); px(f16, 14, 13, SOT1)
px(f16, 14, 12, SKNS); px(f16, 15, 12, SKIN)   # mano baja-derecha
f16.save(os.path.join(DST_DIR, "FRAME16.png"))
print("FRAME16 — Cruz: brazo subiendo (1/3)")

# ── F17 — Brazo 2/3 hacia la frente ──────────────────────────────────────────
f17 = BASE.copy()
px(f17, 13, 15, SOT3)
px(f17, 14, 15, SOT1); px(f17, 14, 14, SOT2)
px(f17, 15, 13, SOT1); px(f17, 15, 12, SOT2); px(f17, 15, 11, SOT1)
px(f17, 15, 10, SKNS); px(f17, 16, 10, SKIN)   # mano media-derecha
f17.save(os.path.join(DST_DIR, "FRAME17.png"))
print("FRAME17 — Cruz: brazo subiendo (2/3)")

# ── F18 — Mano en la frente (KEY: Padre) ─────────────────────────────────────
f18 = BASE.copy()
px(f18, 13, 15, SOT3)
px(f18, 14, 15, SOT1); px(f18, 14, 14, SOT2); px(f18, 14, 13, SOT1)
px(f18, 15, 12, SOT2); px(f18, 15, 11, SOT1); px(f18, 16, 10, SOT2)
px(f18, 15,  9, SKNS); px(f18, 16,  9, SKIN)
px(f18, 15,  8, SKND); px(f18, 16,  8, SKNS)   # mano toca frente
f18.save(os.path.join(DST_DIR, "FRAME18.png"))
print("FRAME18 — Cruz: frente (Padre) KEY")

# ── F19 — Bajando desde la frente (1/2 de camino al pecho) ───────────────────
f19 = BASE.copy()
px(f19, 13, 15, SOT3)
px(f19, 14, 15, SOT1); px(f19, 14, 14, SOT2); px(f19, 14, 13, SOT1)
px(f19, 14, 12, SOT2)
px(f19, 14, 11, SKNS); px(f19, 15, 11, SKIN); px(f19, 15, 10, SKND)
f19.save(os.path.join(DST_DIR, "FRAME19.png"))
print("FRAME19 — Cruz: bajando (frente→pecho)")

# ── F20 — Mano en el pecho (KEY: Hijo) ───────────────────────────────────────
f20 = BASE.copy()
px(f20, 13, 15, SOT3)
px(f20, 13, 16, SOT2); px(f20, 12, 16, SOT1)
px(f20, 11, 16, SOT2); px(f20, 10, 16, SOT1)
px(f20,  9, 15, SKNS); px(f20, 10, 15, SKIN)
px(f20,  8, 16, SKND); px(f20,  9, 16, SKNS); px(f20, 10, 16, SKIN)
px(f20,  8, 17, SOT1)
f20.save(os.path.join(DST_DIR, "FRAME20.png"))
print("FRAME20 — Cruz: pecho (Hijo) KEY")

# ── F21 — Brazo cruzando a la mitad hacia hombro izquierdo ───────────────────
f21 = BASE.copy()
px(f21, 13, 15, SOT2)
px(f21, 12, 16, SOT1); px(f21, 11, 16, SOT2)
px(f21, 10, 16, SOT1); px(f21,  9, 16, SOT2)
px(f21,  8, 16, SKNS); px(f21,  7, 16, SKIN)
px(f21,  8, 15, SKND); px(f21,  7, 15, SKNS)   # mano a mitad del torso
f21.save(os.path.join(DST_DIR, "FRAME21.png"))
print("FRAME21 — Cruz: hacia hombro izq (mitad)")

# ── F22 — Mano en el hombro izquierdo (KEY: Espíritu) ────────────────────────
f22 = BASE.copy()
px(f22, 13, 16, SOT2)
px(f22, 12, 16, SOT1); px(f22, 11, 16, SOT2)
px(f22, 10, 16, SOT1); px(f22,  9, 16, SOT2)
px(f22,  8, 16, SOT1); px(f22,  7, 16, SOT2); px(f22,  6, 16, SOT1)
px(f22,  5, 15, SKNS); px(f22,  4, 15, SKIN)
px(f22,  5, 16, SKND); px(f22,  4, 16, SKNS)   # mano toca hombro izq
f22.save(os.path.join(DST_DIR, "FRAME22.png"))
print("FRAME22 — Cruz: hombro izq (Espíritu) KEY")

# ── F23 — Regresando: brazo en el centro-izquierda ───────────────────────────
f23 = BASE.copy()
px(f23, 13, 15, SOT2)
px(f23, 12, 15, SOT1); px(f23, 11, 15, SOT2)
px(f23, 10, 15, SOT1); px(f23,  9, 15, SOT2)
px(f23,  8, 15, SKNS); px(f23,  7, 15, SKIN); px(f23,  7, 14, SKND)
f23.save(os.path.join(DST_DIR, "FRAME23.png"))
print("FRAME23 — Cruz: cruzando izq→der (1/3)")

# ── F24 — Regresando: brazo en el centro-derecha ─────────────────────────────
f24 = BASE.copy()
px(f24, 13, 15, SOT2)
px(f24, 12, 15, SOT1); px(f24, 11, 15, SOT2)
px(f24, 11, 14, SKNS); px(f24, 10, 14, SKIN); px(f24, 11, 13, SKND)
f24.save(os.path.join(DST_DIR, "FRAME24.png"))
print("FRAME24 — Cruz: cruzando izq→der (2/3)")

# ── F25 — Mano en el hombro derecho (KEY: Santo) ─────────────────────────────
f25 = BASE.copy()
px(f25, 13, 15, SOT3)
px(f25, 14, 15, SOT2); px(f25, 14, 14, SOT1); px(f25, 13, 14, SOT2)
px(f25, 14, 13, SKNS); px(f25, 15, 13, SKIN)
px(f25, 13, 13, SKND); px(f25, 15, 14, SKNS)   # mano toca hombro der
f25.save(os.path.join(DST_DIR, "FRAME25.png"))
print("FRAME25 — Cruz: hombro der (Santo) KEY")

# ── F26 — Subiendo a los labios (mitad del camino) ───────────────────────────
f26 = BASE.copy()
px(f26, 13, 15, SOT3)
px(f26, 13, 14, SOT2); px(f26, 12, 14, SOT1)
px(f26, 12, 13, SOT2)
px(f26, 12, 13, SKNS); px(f26, 11, 13, SKIN); px(f26, 11, 12, SKND)
f26.save(os.path.join(DST_DIR, "FRAME26.png"))
print("FRAME26 — Cruz: subiendo a los labios")

# ── F27 — Beso de la mano (KEY: Amén) ────────────────────────────────────────
f27 = BASE.copy()
px(f27, 13, 15, SOT3)
px(f27, 12, 15, SOT2); px(f27, 12, 14, SOT1)
px(f27, 11, 14, SOT2); px(f27, 11, 13, SOT1); px(f27, 10, 13, SOT2)
px(f27, 10, 12, SKNS); px(f27,  9, 12, SKIN)
px(f27, 11, 12, SKND)
px(f27,  9, 11, SKNS); px(f27, 10, 11, SKIN)   # punta dedos en labios
f27.save(os.path.join(DST_DIR, "FRAME27.png"))
print("FRAME27 — Cruz: beso (Amén) KEY")

# =============================================================================
# PALETA ADICIONAL — Cáliz
# =============================================================================
CHAL_G = (0xDC, 0xAC, 0x22, 255)
CHAL_D = (0x8C, 0x5C, 0x08, 255)

def draw_chalice(img, cx, cy):
    px(img, cx-1, cy, CHAL_D); px(img, cx, cy, CHAL_G); px(img, cx+1, cy, CHAL_D)
    for dy in (1, 2):
        for dx in range(-2, 3):
            px(img, cx+dx, cy+dy, CHAL_D if abs(dx)==2 else CHAL_G)
    px(img, cx, cy+3, CHAL_G)
    for dx in range(-2, 3):
        px(img, cx+dx, cy+4, CHAL_D if abs(dx)==2 else CHAL_G)
    for dx in range(-3, 4):
        px(img, cx+dx, cy+5, CHAL_D if abs(dx)==3 else CHAL_G)

# =============================================================================
# FRAMES 28-35 — Hechos a mano por el usuario. El script NO los toca.
# F28-F29: Cáliz (inicio y fin de la elevación)
# F30-F34: Caminata de espaldas
# F35:     Sentado de espaldas
# =============================================================================

from PIL import ImageOps

def make_back_view(front_img):
    """
    Vista trasera: mirror + limpiar cabeza/cuello completo + repintar.
    Se guardan las posiciones exactas del sprite antes de limpiar,
    asi la silueta de cada frame de caminar queda correcta.
    Proporciones alineadas con el frente:
      y0-y7   copa del pelo
      y8-y11  nuca (pelo corto)
      y12-y14 cuello visible desde atras (piel)
      y15+    sotana negra (alineado con inicio del cuerpo al frente)
    """
    img = ImageOps.mirror(front_img).copy()

    # Guardar pixels en y0-y17 (silueta real del frame incluyendo cuello/hombros)
    head_px = set()
    for y in range(18):
        for x in range(W):
            if img.getpixel((x, y))[3] > 0:
                head_px.add((x, y))

    # Limpiar toda la zona cabeza+cuello+hombros
    for y in range(18):
        for x in range(W):
            img.putpixel((x, y), (0, 0, 0, 0))

    # Repintar con proporciones correctas
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
            # Nuca: pelo corto cubre toda la parte trasera
            img.putpixel((x, y), HAI1 if (x <= 2 or x >= 15) else HAI2)
        elif y <= 14:
            # Cuello visible desde atras (mismas filas que barbilla al frente)
            if x <= 3 or x >= 14:
                img.putpixel((x, y), SKND)
            else:
                img.putpixel((x, y), SKNS if y == 12 else SKIN)
        else:
            # y15+: sotana negra (alineado con inicio del cuerpo al frente)
            if x == 0 or x == 17: continue
            img.putpixel((x, y), SOT1 if (x <= 4 or x >= 13) else SOT2)

    return img

# =============================================================================
# FRAMES 36-37 — Elevacion del Caliz: frames intermedios
# F28 = caliz al pecho (rim y14, hecho a mano)
# F36 = caliz subiendo 1/3 (rim y10)
# F37 = caliz subiendo 2/3 (rim y06)
# F29 = caliz completamente elevado (rim y02, hecho a mano)
# Orden de animacion: F28 -> F36 -> F37 -> F29
# =============================================================================

# F36: Caliz subiendo, rim en y10 — brazos desde los hombros hacia y15
f36 = BASE.copy()
# Brazo izquierdo del hombro hacia la base del caliz
px(f36, 5, 15, SOT2); px(f36, 4, 15, SOT1)
px(f36, 5, 16, SOT2); px(f36, 4, 16, SOT1)
# Mano izquierda sosteniendo el pie del caliz (y15)
px(f36, 3, 15, SKIN);  px(f36, 4, 15, SKNS)
px(f36, 3, 16, SKNS);  px(f36, 4, 16, SKND)
# Brazo derecho simetrico
px(f36, 12, 15, SOT2); px(f36, 13, 15, SOT1)
px(f36, 12, 16, SOT2); px(f36, 13, 16, SOT1)
# Mano derecha
px(f36, 14, 15, SKIN);  px(f36, 13, 15, SKNS)
px(f36, 14, 16, SKNS);  px(f36, 13, 16, SKND)
draw_chalice(f36, 8, 10)   # rim y10, pie y15
f36.save(os.path.join(DST_DIR, "FRAME36.png"))
print("FRAME36 — Caliz subiendo 1/3 (rim y10)")

# F37: Caliz casi elevado, rim en y06 — brazos van hacia arriba
f37 = BASE.copy()
# Brazo izquierdo: del hombro (y15) sube hasta y11
for ys in range(11, 16):
    px(f37, 5, ys, SOT2); px(f37, 4, ys, SOT1)
# Mano izquierda en el pie del caliz (y11)
px(f37, 3, 11, SKIN);  px(f37, 4, 11, SKNS)
px(f37, 3, 10, SKNS)
# Brazo derecho simetrico
for ys in range(11, 16):
    px(f37, 12, ys, SOT2); px(f37, 13, ys, SOT1)
# Mano derecha
px(f37, 14, 11, SKIN);  px(f37, 13, 11, SKNS)
px(f37, 14, 10, SKNS)
draw_chalice(f37, 8, 6)    # rim y06, pie y11
f37.save(os.path.join(DST_DIR, "FRAME37.png"))
print("FRAME37 — Caliz subiendo 2/3 (rim y06)")

# =============================================================================
# FRAMES 39-40 — Alzar el Caliz (Elevacion en la Consagracion)
# Las manos sostienen la BASE del caliz. El caliz tiene forma reconocible.
# =============================================================================

# Caliz: rim 3px, copa 5px×2, tallo 1px, base 5px, pie 7px = 6 filas
def draw_chalice(img, cx, cy):
    """Caliz pixel art claro: copa, tallo y base distinguibles."""
    # Rim / boca
    for dx in range(-1, 2):
        px(img, cx+dx, cy,   CHAL_D if abs(dx)==1 else CHAL_G)
    # Copa (2 filas)
    for dy in (1, 2):
        for dx in range(-2, 3):
            px(img, cx+dx, cy+dy, CHAL_D if abs(dx)==2 else CHAL_G)
    # Tallo
    px(img, cx, cy+3, CHAL_G)
    # Base superior
    for dx in range(-2, 3):
        px(img, cx+dx, cy+4, CHAL_D if abs(dx)==2 else CHAL_G)
    # Pie (mas ancho)
    for dx in range(-3, 4):
        px(img, cx+dx, cy+5, CHAL_D if abs(dx)==3 else CHAL_G)

# F38 — Caliz sostenido a la altura del pecho
# Manos agarran la BASE del caliz (y19-y20). Brazos van del hombro a la base.
f38 = BASE.copy()
px(f38, 5, 16, SOT2); px(f38, 4, 16, SOT1)
px(f38, 5, 17, SOT2); px(f38, 4, 17, SOT1)
px(f38, 5, 18, SOT2); px(f38, 4, 18, SOT1)
px(f38, 4, 19, SKNS); px(f38, 3, 19, SKIN)
px(f38, 4, 20, SKND); px(f38, 3, 20, SKNS)
px(f38, 12, 16, SOT2); px(f38, 13, 16, SOT1)
px(f38, 12, 17, SOT2); px(f38, 13, 17, SOT1)
px(f38, 12, 18, SOT2); px(f38, 13, 18, SOT1)
px(f38, 13, 19, SKNS); px(f38, 14, 19, SKIN)
px(f38, 13, 20, SKND); px(f38, 14, 20, SKNS)
draw_chalice(f38, 8, 14)
f38.save(os.path.join(DST_DIR, "FRAME38.png"))
print("FRAME38 — Caliz sostenido al pecho (manos en base)")

# F39 — Elevacion completa: brazos rectos arriba, manos en la base del caliz
f39 = BASE.copy()
for ys in range(8, 16):
    px(f39, 4, ys, SOT2); px(f39, 5, ys, SOT1)
px(f39, 4, 8, SKNS); px(f39, 3, 8, SKIN); px(f39, 3, 7, SKNS)
for ys in range(8, 16):
    px(f39, 13, ys, SOT2); px(f39, 12, ys, SOT1)
px(f39, 13, 8, SKNS); px(f39, 14, 8, SKIN); px(f39, 14, 7, SKNS)
draw_chalice(f39, 8, 2)
f39.save(os.path.join(DST_DIR, "FRAME39.png"))
print("FRAME39 — Elevacion completa (manos sostienen base del caliz)")

# =============================================================================
# FRAMES 40-43 — Caminando con Biblia (basados en F1-F4)
# =============================================================================
def _sot(x):
    return SOT1 if (x <= 5 or x >= 13) else (SOT3 if x in (8,9) else SOT2)

def _draw_bible_padre(out):
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
            if   _bx in (5,12):   _c = BOOK1
            elif _by in (17,21):  _c = BOOK1
            elif _bx in (6,11):   _c = BOOK2
            else:                 _c = BOOKP
            px(out, _bx, _by, _c)
    px(out, 8,18,BOOKX); px(out, 8,19,BOOKX); px(out, 8,20,BOOKX)
    px(out, 7,19,BOOKX); px(out, 9,19,BOOKX)

for _i in range(1, 2):   # solo F40 (F41/F42 eliminados, F43 = Padre Nuestro paso 1)
    _p = os.path.join(DST_DIR, f"FRAME{_i}.png")
    if not os.path.exists(_p): continue
    _src = Image.open(_p).convert("RGBA")
    _frm = _src.copy()
    for _y in range(15, H):
        for _x in range(W):
            _r, _g, _b, _a = _src.getpixel((_x, _y))
            if _a == 0 or not is_skin(_r, _g, _b, _a): continue
            _frm.putpixel((_x, _y), _sot(_x))
    _draw_bible_padre(_frm)
    _frm.save(os.path.join(DST_DIR, f"FRAME{39+_i}.png"))
    print(f"FRAME{39+_i} — Caminando con Biblia (base F{_i})")
for _fn in [41, 42]:
    _fp = os.path.join(DST_DIR, f"FRAME{_fn}.png")
    if os.path.exists(_fp): os.remove(_fp)

# =============================================================================
# FRAMES 44-45 — Cantando (levanta/agacha + boca)
# =============================================================================
def _shift_up_p(src):
    out = Image.new("RGBA", (W, H), (0,0,0,0))
    for _y in range(1, H):
        for _x in range(W):
            out.putpixel((_x, _y-1), src.getpixel((_x, _y)))
    return out

_f1_priest = Image.open(os.path.join(DST_DIR, "FRAME1.png")).convert("RGBA")
MOT = (0x28, 0x10, 0x08, 255)
_ym = 11  # F1 no esta desplazado (hy0=0)

f45 = _shift_up_p(_f1_priest)
px(f45, 8, _ym,   MOT)
px(f45, 8, _ym-1, MOT)
f45.save(os.path.join(DST_DIR, "FRAME45.png"))
print("FRAME45 — Cantando: boca abierta 2px")

f44 = f45.copy()
for _cy in range(9, H):
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

# ── helpers limpieza para poses F43/F46-F49 ──────────────────────────────────
def _limpiar_brazos_p(img, y0=15, y1=22):
    for _cy in range(y0, y1):
        for _cx in range(4):      img.putpixel((_cx,_cy),(0,0,0,0))
        for _cx in range(14, W): img.putpixel((_cx,_cy),(0,0,0,0))
    for _cy in range(max(y0, 18), y1):
        for _cx in range(4, 14):
            _r,_g,_b,_a = img.getpixel((_cx,_cy))
            if _a > 0 and is_skin(_r,_g,_b,_a):
                img.putpixel((_cx,_cy),(0,0,0,0))

def _hombros_p(img):
    for _cy in range(15, 18):
        px(img, 4,_cy,SOT1); px(img,13,_cy,SOT1)

# F43: Padre Nuestro paso 1 — brazos empezando a abrirse (45° hacia abajo-afuera)
f43 = make_back_view(_f1_priest)
_limpiar_brazos_p(f43); _hombros_p(f43)
# Brazo izquierdo: hombro → baja un paso → piel al final (inicio apertura)
px(f43, 3,15,SOT1); px(f43, 3,16,SOT1); px(f43, 2,17,SKNS); px(f43, 1,17,SKIN)
# Brazo derecho: simétrico
px(f43,14,15,SOT1); px(f43,14,16,SOT1); px(f43,15,17,SKNS); px(f43,16,17,SKIN)
f43.save(os.path.join(DST_DIR, "FRAME43.png"))
print("FRAME43 — Padre Nuestro paso 1 (brazos empezando a abrirse)")

# F46: Levantar manos paso 1 — brazos a mitad (~45° arriba)
f46 = make_back_view(_f1_priest)
_limpiar_brazos_p(f46, 9, 22); _hombros_p(f46)
# Brazo izquierdo sube en diagonal hasta y=11
px(f46, 3,15,SOT1); px(f46, 3,14,SOT1); px(f46, 2,13,SOT1)
px(f46, 1,12,SOT2); px(f46, 0,11,SKNS)
# Brazo derecho simétrico
px(f46,14,15,SOT1); px(f46,14,14,SOT1); px(f46,15,13,SOT1)
px(f46,16,12,SOT2); px(f46,17,11,SKNS)
f46.save(os.path.join(DST_DIR, "FRAME46.png"))
print("FRAME46 — Levantar manos paso 1 (brazos a 45° arriba)")

# F47: Padre Nuestro completo — brazos completamente horizontales
f47 = make_back_view(_f1_priest)
_limpiar_brazos_p(f47); _hombros_p(f47)
px(f47,3,15,SOT1); px(f47,2,15,SOT1); px(f47,1,15,SKNS); px(f47,0,15,SKIN)
px(f47,2,16,SOT1); px(f47,1,16,SKND)
px(f47,14,15,SOT1); px(f47,15,15,SOT1); px(f47,16,15,SKNS); px(f47,17,15,SKIN)
px(f47,15,16,SOT1); px(f47,16,16,SKND)
f47.save(os.path.join(DST_DIR, "FRAME47.png"))
print("FRAME47 — Padre Nuestro completo (brazos horizontales)")

# F48: Dar la paz iniciando — brazo apenas empezando a extenderse
f48 = make_back_view(_f1_priest)
_limpiar_brazos_p(f48); _hombros_p(f48)
# Brazo derecho: apenas sale del hombro, un paso hacia adelante-afuera
px(f48,14,15,SOT1); px(f48,15,15,SOT1)
px(f48,15,16,SOT1); px(f48,16,16,SKNS)
f48.save(os.path.join(DST_DIR, "FRAME48.png"))
print("FRAME48 — Dar la paz iniciando (brazo apenas saliendo)")

# F49: Levantar manos completo — ambos brazos completamente arriba
f49 = make_back_view(_f1_priest)
_limpiar_brazos_p(f49, 9, 22); _hombros_p(f49)
px(f49,3,15,SOT1); px(f49,3,14,SOT1); px(f49,2,13,SOT1)
px(f49,2,12,SOT1); px(f49,1,11,SOT2); px(f49,0,10,SKNS); px(f49,0,9,SKIN)
px(f49,14,15,SOT1); px(f49,14,14,SOT1); px(f49,15,13,SOT1)
px(f49,15,12,SOT1); px(f49,16,11,SOT2); px(f49,17,10,SKNS); px(f49,17,9,SKIN)
f49.save(os.path.join(DST_DIR, "FRAME49.png"))
print("FRAME49 — Levantar manos completo (brazos arriba)")

print(f"\nHOMBRE10 listo: 49 frames")
print(f"  F40-F42  Caminando con Biblia (3 pasos)")
print(f"  F43      Padre Nuestro paso 1 (brazos empezando a abrirse)")
print(f"  F46      Levantar manos paso 1 (brazos a 45° arriba)")
print(f"  F47      Padre Nuestro completo (brazos horizontales)")
print(f"  F48      Dar la paz iniciando")
print(f"  F49      Levantar manos completo")
print(f"  F01-F08  Caminar (frente)")
print(f"  F10-F15  Gestos liturgicos")
print(f"  F16-F27  Señal de la Cruz (12 frames suaves)")
print(f"  F28-F29  Caliz: inicio y fin [manuales]")
print(f"  F30-F34  Caminata de espaldas [manuales]")
print(f"  F35      Sentado de espaldas [manual]")
print(f"  F36-F37  Caliz: intermedios 1/3 y 2/3")
print(f"  F38-F39  Caliz: pecho y elevacion completa")
print(f"  F40-F43  Caminando con Biblia (F1-F4)")
print(f"  F44      Cantando: levanta, 1px boca")
print(f"  F45      Cantando: boca abierta, 2px vertical")
print(f"  Orden animacion caliz: F38 -> F36 -> F37 -> F29/F39")
print(f"  {DST_DIR}")
