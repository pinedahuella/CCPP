import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageOps

SRC_DIR = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PERSONAJES\MUJERES\MUJER1"
DST_DIR = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PERSONAJES\MUJERES\MUJER10"
os.makedirs(DST_DIR, exist_ok=True)

W, H = 18, 25

# ── Paleta monja ──────────────────────────────────────────────────────────────
VEL1 = (0x06, 0x04, 0x06, 255)   # velo: negro borde
VEL2 = (0x12, 0x10, 0x16, 255)   # velo: negro base
VEL3 = (0x1E, 0x1A, 0x22, 255)   # velo: reflejo interior (da volumen al oval)
TOC1 = (0xF0, 0xEC, 0xF4, 255)   # toca: blanca
TOC2 = (0xD0, 0xCC, 0xDC, 255)   # toca: sombra lateral
HAB1 = (0x0A, 0x0A, 0x14, 255)   # habito: borde/sombra
HAB2 = (0x14, 0x14, 0x22, 255)   # habito: azul marino oscuro base
HAB3 = (0x22, 0x22, 0x38, 255)   # habito: reflejo/pliegue
BIB1 = (0xF4, 0xF0, 0xFC, 255)   # pechera: blanca pura
BIB2 = (0xD4, 0xD0, 0xE4, 255)   # pechera: sombra
SKIN = (0xFE, 0xD9, 0x98, 255)
SKNS = (0xF5, 0xB9, 0x71, 255)
SKND = (0xD4, 0x94, 0x50, 255)
EYE  = (0x1C, 0x10, 0x10, 255)
SHO  = (0x10, 0x0E, 0x12, 255)
CRUZA = (0xD0, 0xA0, 0x18, 255)  # cruz dorada en pechera
# Fleco dorado (pelo que asoma del velo)
FLE1 = (0x90, 0x60, 0x08, 255)   # raiz del fleco (oscuro)
FLE2 = (0xC8, 0x90, 0x14, 255)   # cuerpo del fleco
FLE3 = (0xEC, 0xC0, 0x30, 255)   # punta del fleco (claro)
BOOK1 = (0x4C, 0x28, 0x08, 255)
BOOK2 = (0x78, 0x44, 0x14, 255)
BOOKP = (0xEC, 0xE8, 0xD8, 255)
BOOKX = (0xC0, 0x60, 0x08, 255)
ROS1  = (0x3C, 0x1C, 0x06, 255)
ROS2  = (0x6C, 0x3C, 0x10, 255)
ROSC  = (0xB8, 0x88, 0x20, 255)

# ── Zona de la cara POR FILA ──────────────────────────────────────────────────
# Ampliada para que los ojos siempre sean visibles
FACE = {
    8:  (5, 12),
    9:  (5, 11),   # x5-x11: incluye el ojo en x6
    10: (4, 12),
    11: (4, 12),
    12: (4, 13),
    13: (5, 12),
}

# ── Forma oval del velo (NO depende de MUJER1, se pinta incondicional) ────────
# Cada entrada: (x_izq, x_der) inclusive para ese dy relativo
VELO_SHAPE = [
    (7, 10),  # dy=0  cima: oval estrecho
    (5, 12),  # dy=1
    (4, 13),  # dy=2
    (3, 14),  # dy=3  punto mas ancho
    (3, 14),  # dy=4  fleco zone
    (3, 14),  # dy=5
    (3, 14),  # dy=6
    (3, 14),  # dy=7  toca zone
]

def vel_color(x, xl, xr):
    """Sombreado para dar volumen redondeado al velo."""
    if x == xl or x == xr:          return VEL1   # borde duro
    if x == xl+1 or x == xr-1:     return VEL2   # borde suave
    if abs(x - 8) <= 1:             return VEL3   # reflejo central minimo
    return VEL2

# Fleco: columnas con pelo dorado por fila (dy relativo)
# Las puntas del fleco bajan irregularmente para dar efecto natural
FLECO = {
    4: [(7,FLE2),(8,FLE3),(9,FLE3),(10,FLE2)],
    5: [(6,FLE1),(7,FLE2),(8,FLE3),(9,FLE3),(10,FLE2),(11,FLE1)],
    6: [(5,FLE1),(6,FLE2),(7,FLE3),(8,FLE3),(9,FLE3),(10,FLE2),(11,FLE1),(12,FLE1)],
}

def is_shifted(img):
    return all(img.getpixel((x,0))[3]==0 for x in range(W))

def px(img, x, y, c):
    if 0<=x<W and 0<=y<H: img.putpixel((x,y), c)

def hab(x):
    return HAB1 if (x<=5 or x>=13) else (HAB3 if x in (8,9) else HAB2)

def bib(x):
    """Pechera blanca en el centro del pecho."""
    if 6 <= x <= 11:
        return BIB1 if x in (7,8,9,10) else BIB2
    return hab(x)

# =============================================================================
# MAKE_NUN — dos pasadas
#   PASADA 1 (incondicional): velo ovalado dy=0-7 segun VELO_SHAPE exacto
#   PASADA 2 (pixels fuente):  cara dy=8-13, collar/pechera/habito/zapatos
# =============================================================================
def make_nun(src_img):
    hy0 = 1 if is_shifted(src_img) else 0
    img  = Image.new("RGBA", (W, H), (0,0,0,0))
    FLECO_D = {dy: dict(pairs) for dy, pairs in FLECO.items()}

    # ── PASADA 1: velo ovalado (forma fija, independiente del pelo de MUJER1) ──
    for dy, (xl, xr) in enumerate(VELO_SHAPE):
        y = hy0 + dy
        if y >= H: break
        for x in range(xl, xr + 1):
            if dy in FLECO_D and x in FLECO_D[dy]:
                img.putpixel((x, y), FLECO_D[dy][x])
            elif dy == 7 and 5 <= x <= 12:
                img.putpixel((x, y), TOC2 if (x == 5 or x == 12) else TOC1)
            else:
                img.putpixel((x, y), vel_color(x, xl, xr))

    # ── PASADA 2: cara y cuerpo (siguen shape de la fuente) ───────────────────
    for y in range(H):
        for x in range(W):
            _, _, _, a = src_img.getpixel((x, y))
            if a == 0: continue
            dy = y - hy0
            if dy <= 7: continue   # velo ya pintado en pasada 1

            # Cara
            if 8 <= dy <= 13:
                fl, fr = FACE.get(dy, (5, 12))
                if fl <= x <= fr:
                    sr,sg,sb,_ = src_img.getpixel((x,y))
                    if sb > 150 and sr < 50:
                        img.putpixel((x,y), EYE)
                    else:
                        img.putpixel((x,y), (sr,sg,sb,255))
                elif x == fl-1:
                    img.putpixel((x,y), TOC1)
                elif x == fr+1:
                    img.putpixel((x,y), TOC1)
                else:
                    img.putpixel((x,y), VEL1 if (x<=1 or x>=16) else VEL2)

            # Collar blanco
            elif dy == 14:
                img.putpixel((x,y), TOC2 if 6<=x<=11 else hab(x))
            elif dy == 15:
                img.putpixel((x,y), TOC1 if 6<=x<=11 else hab(x))

            # Pechera blanca
            elif 16 <= dy <= 20:
                img.putpixel((x,y), bib(x))

            # Habito azul marino
            elif dy <= 22:
                img.putpixel((x,y), hab(x))

            # Zapatos
            else:
                img.putpixel((x,y), SHO)

    # Cruz dorada en pechera
    cy = hy0 + 17
    for dd in range(-1, 2):
        px(img, 8+dd, cy, CRUZA)
    px(img, 8, cy-1, CRUZA)
    px(img, 8, cy+1, CRUZA)

    return img

# =============================================================================
# FRAMES 1-8 — Caminar de frente
# =============================================================================
for i in range(1, 9):
    src = Image.open(os.path.join(SRC_DIR, f"FRAME{i}.png")).convert("RGBA")
    out = make_nun(src)
    hy0 = 1 if is_shifted(src) else 0
    # Munecas solo en frames de caminata (F1-F8); F9+ tienen manos propias
    px(out, 5, hy0+19, SKNS);  px(out, 4, hy0+19, SKND)
    px(out, 5, hy0+20, SKIN);  px(out, 4, hy0+20, SKNS)
    px(out, 12, hy0+19, SKNS); px(out, 13, hy0+19, SKND)
    px(out, 12, hy0+20, SKIN); px(out, 13, hy0+20, SKNS)
    out.save(os.path.join(DST_DIR, f"FRAME{i}.png"))
    print(f"FRAME{i} guardado")

BASE = make_nun(Image.open(os.path.join(SRC_DIR, "FRAME1.png")).convert("RGBA"))

for n in range(9, 50):
    p = os.path.join(DST_DIR, f"FRAME{n}.png")
    if os.path.exists(p): os.remove(p)

# =============================================================================
# F9 — Orante
# =============================================================================
f9 = BASE.copy()
px(f9,4,15,HAB2); px(f9,3,15,HAB1); px(f9,3,14,HAB2); px(f9,2,14,HAB1)
px(f9,2,13,HAB2); px(f9,1,13,HAB1); px(f9,1,12,HAB2); px(f9,0,12,HAB1)
px(f9,0,11,SKNS); px(f9,0,10,SKIN); px(f9,0,9,SKIN)
px(f9,13,15,HAB2); px(f9,14,15,HAB1); px(f9,14,14,HAB2); px(f9,15,14,HAB1)
px(f9,15,13,HAB2); px(f9,16,13,HAB1); px(f9,16,12,HAB2); px(f9,17,12,HAB1)
px(f9,17,11,SKNS); px(f9,17,10,SKIN); px(f9,17,9,SKIN)
f9.save(os.path.join(DST_DIR,"FRAME9.png")); print("FRAME9  — Orante")

# =============================================================================
# F10 — Manos juntas
# =============================================================================
f10 = BASE.copy()
px(f10,4,16,HAB3); px(f10,5,16,HAB3); px(f10,4,17,HAB3); px(f10,5,17,HAB2)
px(f10,13,16,HAB3); px(f10,12,16,HAB3); px(f10,13,17,HAB3); px(f10,12,17,HAB2)
for bx,c in [(7,SKNS),(8,SKIN),(9,SKIN),(10,SKIN),(11,SKNS)]: px(f10,bx,17,c)
for bx,c in [(7,SKND),(8,SKNS),(9,SKNS),(10,SKNS),(11,SKND)]: px(f10,bx,18,c)
px(f10,6,17,HAB1); px(f10,12,17,HAB1)
f10.save(os.path.join(DST_DIR,"FRAME10.png")); print("FRAME10 — Manos juntas")

# =============================================================================
# F11 — Mano al pecho
# =============================================================================
f11 = BASE.copy()
px(f11,13,15,HAB3); px(f11,13,16,HAB3); px(f11,12,16,HAB2); px(f11,12,17,HAB2)
px(f11,11,17,HAB1); px(f11,11,16,SKND); px(f11,10,15,SKNS); px(f11,11,15,SKND)
px(f11,9,16,SKIN); px(f11,10,16,SKIN); px(f11,9,17,SKNS); px(f11,10,17,SKND)
f11.save(os.path.join(DST_DIR,"FRAME11.png")); print("FRAME11 — Mano al pecho")

# =============================================================================
# F12 — Brazos extendidos
# =============================================================================
f12 = BASE.copy()
px(f12,3,16,HAB2); px(f12,2,16,HAB1); px(f12,3,17,HAB1); px(f12,2,17,HAB2)
px(f12,1,16,SKNS); px(f12,0,16,SKIN); px(f12,1,17,SKND); px(f12,0,17,SKNS)
px(f12,14,16,HAB2); px(f12,15,16,HAB1); px(f12,14,17,HAB1); px(f12,15,17,HAB2)
px(f12,16,16,SKNS); px(f12,17,16,SKIN); px(f12,16,17,SKND); px(f12,17,17,SKNS)
f12.save(os.path.join(DST_DIR,"FRAME12.png")); print("FRAME12 — Brazos extendidos")

# =============================================================================
# F13 — Libro sagrado
# =============================================================================
f13 = BASE.copy()
for bx in range(6,12):
    for by in range(15,20):
        if bx==6 or bx==11:        c=BOOK1
        elif by==15 or by==19:     c=BOOK1
        elif bx==7 or bx==10:      c=BOOK2
        else:                       c=BOOKP
        px(f13,bx,by,c)
px(f13,8,16,BOOKX); px(f13,8,17,BOOKX); px(f13,8,18,BOOKX)
px(f13,7,17,BOOKX); px(f13,9,17,BOOKX)
px(f13,5,17,SKNS); px(f13,5,18,SKIN); px(f13,4,18,SKNS); px(f13,5,19,SKND)
px(f13,12,17,SKNS); px(f13,12,18,SKIN); px(f13,13,18,SKNS); px(f13,12,19,SKND)
px(f13,4,16,HAB3); px(f13,4,17,HAB2); px(f13,13,16,HAB3); px(f13,13,17,HAB2)
f13.save(os.path.join(DST_DIR,"FRAME13.png")); print("FRAME13 — Libro sagrado")

# =============================================================================
# F14 — Rosario
# =============================================================================
f14 = BASE.copy()
for ry in range(17,23):
    px(f14,8,ry, ROS1 if ry%2==0 else ROS2)
    px(f14,9,ry, ROS2 if ry%2==0 else ROS1)
px(f14,8,23,ROSC); px(f14,9,23,ROSC); px(f14,10,23,ROSC)
px(f14,9,22,ROSC); px(f14,9,24,ROSC)
px(f14,7,17,SKNS); px(f14,7,18,SKIN)
px(f14,10,17,SKNS); px(f14,10,18,SKIN)
px(f14,5,16,HAB3); px(f14,6,16,HAB2); px(f14,11,16,HAB3); px(f14,12,16,HAB2)
f14.save(os.path.join(DST_DIR,"FRAME14.png")); print("FRAME14 — Rosario")

# =============================================================================
# F15-F26 — Señal de la Cruz
# =============================================================================
f15=BASE.copy()
px(f15,13,15,HAB3); px(f15,14,15,HAB1); px(f15,14,14,HAB2); px(f15,14,13,HAB1)
px(f15,14,12,SKNS); px(f15,15,12,SKIN)
f15.save(os.path.join(DST_DIR,"FRAME15.png")); print("FRAME15 — Cruz 1/3")

f16=BASE.copy()
px(f16,13,15,HAB3); px(f16,14,15,HAB1); px(f16,14,14,HAB2)
px(f16,15,13,HAB1); px(f16,15,12,HAB2); px(f16,15,11,HAB1)
px(f16,15,10,SKNS); px(f16,16,10,SKIN)
f16.save(os.path.join(DST_DIR,"FRAME16.png")); print("FRAME16 — Cruz 2/3")

f17=BASE.copy()
px(f17,13,15,HAB3); px(f17,14,15,HAB1); px(f17,14,14,HAB2); px(f17,14,13,HAB1)
px(f17,15,12,HAB2); px(f17,15,11,HAB1); px(f17,16,10,HAB2)
px(f17,15,9,SKNS); px(f17,16,9,SKIN); px(f17,15,8,SKND); px(f17,16,8,SKNS)
f17.save(os.path.join(DST_DIR,"FRAME17.png")); print("FRAME17 — Cruz: frente KEY")

f18=BASE.copy()
px(f18,13,15,HAB3); px(f18,14,15,HAB1); px(f18,14,14,HAB2); px(f18,14,13,HAB1); px(f18,14,12,HAB2)
px(f18,14,11,SKNS); px(f18,15,11,SKIN); px(f18,15,10,SKND)
f18.save(os.path.join(DST_DIR,"FRAME18.png")); print("FRAME18 — Cruz: bajando")

f19=BASE.copy()
px(f19,13,15,HAB3); px(f19,13,16,HAB2); px(f19,12,16,HAB1)
px(f19,11,16,HAB2); px(f19,10,16,HAB1)
px(f19,9,15,SKNS); px(f19,10,15,SKIN)
px(f19,8,16,SKND); px(f19,9,16,SKNS); px(f19,10,16,SKIN); px(f19,8,17,HAB1)
f19.save(os.path.join(DST_DIR,"FRAME19.png")); print("FRAME19 — Cruz: pecho KEY")

f20=BASE.copy()
px(f20,13,15,HAB2); px(f20,12,16,HAB1); px(f20,11,16,HAB2)
px(f20,10,16,HAB1); px(f20,9,16,HAB2)
px(f20,8,16,SKNS); px(f20,7,16,SKIN); px(f20,8,15,SKND); px(f20,7,15,SKNS)
f20.save(os.path.join(DST_DIR,"FRAME20.png")); print("FRAME20 — Cruz: hombro izq medio")

f21=BASE.copy()
px(f21,13,16,HAB2); px(f21,12,16,HAB1); px(f21,11,16,HAB2); px(f21,10,16,HAB1)
px(f21,9,16,HAB2); px(f21,8,16,HAB1); px(f21,7,16,HAB2); px(f21,6,16,HAB1)
px(f21,5,15,SKNS); px(f21,4,15,SKIN); px(f21,5,16,SKND); px(f21,4,16,SKNS)
f21.save(os.path.join(DST_DIR,"FRAME21.png")); print("FRAME21 — Cruz: hombro izq KEY")

f22=BASE.copy()
px(f22,13,15,HAB2); px(f22,12,15,HAB1); px(f22,11,15,HAB2); px(f22,10,15,HAB1); px(f22,9,15,HAB2)
px(f22,8,15,SKNS); px(f22,7,15,SKIN); px(f22,7,14,SKND)
f22.save(os.path.join(DST_DIR,"FRAME22.png")); print("FRAME22 — Cruz: cruzando 1/3")

f23=BASE.copy()
px(f23,13,15,HAB2); px(f23,12,15,HAB1); px(f23,11,15,HAB2)
px(f23,11,14,SKNS); px(f23,10,14,SKIN); px(f23,11,13,SKND)
f23.save(os.path.join(DST_DIR,"FRAME23.png")); print("FRAME23 — Cruz: cruzando 2/3")

f24=BASE.copy()
px(f24,13,15,HAB3); px(f24,14,15,HAB2); px(f24,14,14,HAB1); px(f24,13,14,HAB2)
px(f24,14,13,SKNS); px(f24,15,13,SKIN); px(f24,13,13,SKND); px(f24,15,14,SKNS)
f24.save(os.path.join(DST_DIR,"FRAME24.png")); print("FRAME24 — Cruz: hombro der KEY")

f25=BASE.copy()
px(f25,13,15,HAB3); px(f25,13,14,HAB2); px(f25,12,14,HAB1); px(f25,12,13,HAB2)
px(f25,12,13,SKNS); px(f25,11,13,SKIN); px(f25,11,12,SKND)
f25.save(os.path.join(DST_DIR,"FRAME25.png")); print("FRAME25 — Cruz: hacia labios")

f26=BASE.copy()
px(f26,13,15,HAB3); px(f26,12,15,HAB2); px(f26,12,14,HAB1)
px(f26,11,14,HAB2); px(f26,11,13,HAB1); px(f26,10,13,HAB2)
px(f26,10,12,SKNS); px(f26,9,12,SKIN); px(f26,11,12,SKND)
px(f26,9,11,SKNS); px(f26,10,11,SKIN)
f26.save(os.path.join(DST_DIR,"FRAME26.png")); print("FRAME26 — Cruz: beso KEY")

# =============================================================================
# ESPALDAS
# =============================================================================
def make_back_view(front_img):
    img = ImageOps.mirror(front_img).copy()
    # Limpiar toda la zona de cabeza
    for y in range(14):
        for x in range(W): img.putpixel((x,y),(0,0,0,0))

    # Velo ovalado desde atras (misma forma VELO_SHAPE, sin fleco ni toca)
    for dy, (xl, xr) in enumerate(VELO_SHAPE):
        y = dy   # back frames usan FRAME1 (sin shift)
        if y >= 14: break
        for x in range(xl, xr + 1):
            img.putpixel((x, y), vel_color(x, xl, xr))

    # Nuca: piel en el centro (dy=8-13) dentro del contorno del velo
    xl_body, xr_body = VELO_SHAPE[-1]   # ancho del ultimo row del oval (3,14)
    for dy in range(8, 14):
        y = dy
        if y >= H: break
        for x in range(xl_body, xr_body + 1):
            if 5 <= x <= 12:
                img.putpixel((x, y), SKNS if x in (8,9) else SKND)
            else:
                img.putpixel((x, y), VEL1 if (x==xl_body or x==xr_body) else VEL2)
    return img

for i in range(1, 6):
    src = Image.open(os.path.join(DST_DIR, f"FRAME{i}.png")).convert("RGBA")
    back = make_back_view(src)
    back.save(os.path.join(DST_DIR, f"FRAME{26+i}.png"))
    print(f"FRAME{26+i} — Espaldas caminando (flip F{i})")

f32 = make_back_view(Image.open(os.path.join(DST_DIR,"FRAME1.png")).convert("RGBA"))
f32.save(os.path.join(DST_DIR,"FRAME32.png")); print("FRAME32 — Espaldas: parada")

f33 = make_back_view(Image.open(os.path.join(DST_DIR,"FRAME1.png")).convert("RGBA"))
for x in range(W):
    for y in range(19, H): f33.putpixel((x,y),(0,0,0,0))
f33.save(os.path.join(DST_DIR,"FRAME33.png")); print("FRAME33 — Espaldas: sentada")

def _is_skin_warm(r, g, b, a):
    return a > 0 and r > 0xC0 and g > 0x70 and b > 0x30 and (r - b) > 40

# =============================================================================
# FRAME 36 — Monja caminando con Biblia (basado en F1)
# =============================================================================
for _i in range(1, 2):
    _p = os.path.join(DST_DIR, f"FRAME{_i}.png")
    if not os.path.exists(_p): continue
    _src = Image.open(_p).convert("RGBA")
    _frm = _src.copy()
    for _y in range(15, 21):
        for _x in range(W):
            _r, _g, _b, _a = _src.getpixel((_x, _y))
            if _a == 0 or not _is_skin_warm(_r, _g, _b, _a): continue
            _frm.putpixel((_x, _y), hab(_x))
    px(_frm,  4,15,HAB2); px(_frm,  5,15,HAB1)
    px(_frm,  4,16,HAB2); px(_frm,  5,16,HAB1)
    px(_frm, 13,15,HAB2); px(_frm, 12,15,HAB1)
    px(_frm, 13,16,HAB2); px(_frm, 12,16,HAB1)
    px(_frm,  4,17,SKNS); px(_frm,  4,18,SKND)
    px(_frm, 13,17,SKNS); px(_frm, 13,18,SKND)
    # Brazo derecho extendido al lado del libro
    px(_frm, 14,16,HAB1); px(_frm, 14,17,HAB1)
    px(_frm, 14,18,HAB1); px(_frm, 14,19,HAB1)
    # Zapato visible a la derecha del libro
    px(_frm, 13,20,SHO); px(_frm, 13,21,SHO)
    for _bx in range(5, 13):
        for _by in range(17, 22):
            if   _bx in (5,12):   _c = BOOK1
            elif _by in (17,21):  _c = BOOK1
            elif _bx in (6,11):   _c = BOOK2
            else:                 _c = BOOKP
            px(_frm, _bx, _by, _c)
    px(_frm, 8,18,BOOKX); px(_frm, 8,19,BOOKX); px(_frm, 8,20,BOOKX)
    px(_frm, 7,19,BOOKX); px(_frm, 9,19,BOOKX)
    _frm.save(os.path.join(DST_DIR, f"FRAME{35+_i}.png"))
    print(f"FRAME{35+_i} — Monja con Biblia (base F{_i})")
for _fn in [37, 38, 39]:
    _fp = os.path.join(DST_DIR, f"FRAME{_fn}.png")
    if os.path.exists(_fp): os.remove(_fp)

# =============================================================================
# FRAMES 44-45 — Monja cantando
# =============================================================================
def _shift_up_n(src):
    out = Image.new("RGBA", (W, H), (0,0,0,0))
    for _y in range(1, H):
        for _x in range(W):
            out.putpixel((_x, _y-1), src.getpixel((_x, _y)))
    return out

_f1_nun = Image.open(os.path.join(DST_DIR, "FRAME1.png")).convert("RGBA")
MOT = (0x28, 0x10, 0x08, 255)
_ym = 11

f45 = _shift_up_n(_f1_nun)
px(f45, 8, _ym,   MOT)
px(f45, 8, _ym-1, MOT)
f45.save(os.path.join(DST_DIR, "FRAME45.png"))
print("FRAME45 — Monja cantando: boca abierta 2px")

f44 = f45.copy()
for _cy in range(9, H):
    for _cx in range(4):      f44.putpixel((_cx,_cy),(0,0,0,0))
    for _cx in range(14, W): f44.putpixel((_cx,_cy),(0,0,0,0))
for _cy in range(16, H):
    for _cx in range(4, 14):
        _r,_g,_b,_a = f44.getpixel((_cx,_cy))
        if _a > 0 and _is_skin_warm(_r,_g,_b,_a): f44.putpixel((_cx,_cy),(0,0,0,0))
px(f44, 3,14,HAB1); px(f44, 2,13,HAB1)
px(f44, 1,12,HAB2); px(f44, 0,11,SKNS); px(f44, 0,10,SKIN)
px(f44,14,14,HAB1); px(f44,15,13,HAB1)
px(f44,16,12,HAB2); px(f44,17,11,SKNS); px(f44,17,10,SKIN)
f44.save(os.path.join(DST_DIR, "FRAME44.png"))
print("FRAME44 — Monja cantando: boca 2px + brazos levantados")

# ── helpers limpieza para poses F46-F49 (monja) ──────────────────────────────
_f1_nun_bk = Image.open(os.path.join(DST_DIR, "FRAME1.png")).convert("RGBA")

def _limpiar_brazos_n(img, y0=15, y1=22):
    for _cy in range(y0, y1):
        for _cx in range(4):      img.putpixel((_cx,_cy),(0,0,0,0))
        for _cx in range(14, W): img.putpixel((_cx,_cy),(0,0,0,0))
    for _cy in range(max(y0, 18), y1):
        for _cx in range(4, 14):
            _r,_g,_b,_a = img.getpixel((_cx,_cy))
            if _a > 0 and _is_skin_warm(_r,_g,_b,_a):
                img.putpixel((_cx,_cy),(0,0,0,0))

def _hombros_n(img):
    for _cy in range(15, 18):
        px(img, 4,_cy,HAB1); px(img,13,_cy,HAB1)

_nsh = [(_r,_g,_b,255) for _sy in range(21,H) for _sx in range(W)
        for _r,_g,_b,_a in [_f1_nun_bk.getpixel((_sx,_sy))]
        if _a>0 and _r<0xC0]
_nsh_s = sorted(set(_nsh), key=lambda c:c[0]+c[1]+c[2]) if _nsh else []
NSHD = _nsh_s[0] if _nsh_s else HAB1
NSHM = _nsh_s[min(len(_nsh_s)//3,len(_nsh_s)-1)] if _nsh_s else HAB2

# F46: Incarse (arrodillada de espaldas)
f46 = make_back_view(_f1_nun_bk)
for _cx in range(W):
    for _cy in range(15, H): f46.putpixel((_cx,_cy),(0,0,0,0))
for _cy in range(15, 18):
    for _cx in range(4, 14): f46.putpixel((_cx,_cy), HAB1 if (_cx<=5 or _cx>=12) else HAB2)
for _cx in range(4, 14): f46.putpixel((_cx,18), HAB1 if (_cx<=5 or _cx>=12) else HAB2)
for _cy in range(19, 21):
    px(f46,3,_cy,HAB1); px(f46,4,_cy,HAB2); px(f46,5,_cy,HAB2); px(f46,6,_cy,HAB1)
    px(f46,11,_cy,HAB1); px(f46,12,_cy,HAB2); px(f46,13,_cy,HAB2); px(f46,14,_cy,HAB1)
for _cx in range(4, 8):  f46.putpixel((_cx,21), NSHD if (_cx==4 or _cx==7) else NSHM)
for _cx in range(10,14): f46.putpixel((_cx,21), NSHD if (_cx==10 or _cx==13) else NSHM)
f46.save(os.path.join(DST_DIR, "FRAME46.png"))
print("FRAME46 — Monja incarse de espaldas")

# F47: Padre Nuestro de espaldas (brazos horizontales)
f47 = make_back_view(_f1_nun_bk)
_limpiar_brazos_n(f47); _hombros_n(f47)
px(f47,3,15,HAB1); px(f47,2,15,HAB1); px(f47,1,15,SKNS); px(f47,0,15,SKIN)
px(f47,3,16,HAB1); px(f47,2,16,HAB1); px(f47,1,16,SKNS); px(f47,0,16,SKND)
px(f47,14,15,HAB1); px(f47,15,15,HAB1); px(f47,16,15,SKNS); px(f47,17,15,SKIN)
px(f47,14,16,HAB1); px(f47,15,16,HAB1); px(f47,16,16,SKNS); px(f47,17,16,SKND)
f47.save(os.path.join(DST_DIR, "FRAME47.png"))
print("FRAME47 — Monja Padre Nuestro de espaldas")

# F48: Dar la paz de espaldas (brazo derecho extendido)
f48 = make_back_view(_f1_nun_bk)
_limpiar_brazos_n(f48); _hombros_n(f48)
px(f48,14,15,HAB1); px(f48,15,15,HAB1)
px(f48,14,16,HAB1); px(f48,15,16,HAB2); px(f48,16,16,SKNS)
px(f48,16,17,SKNS); px(f48,17,17,SKIN)
px(f48,17,18,SKIN)
f48.save(os.path.join(DST_DIR, "FRAME48.png"))
print("FRAME48 — Monja dar la paz de espaldas")

# F49: Levantar manos de espaldas (ambos brazos completamente arriba)
f49 = make_back_view(_f1_nun_bk)
_limpiar_brazos_n(f49, 9, 22); _hombros_n(f49)
px(f49, 3,15,HAB1); px(f49,2,15,HAB1)
px(f49, 3,14,HAB1); px(f49,2,14,HAB1)
px(f49, 2,13,HAB1); px(f49,1,13,HAB2)
px(f49, 2,12,HAB1); px(f49,1,12,HAB2)
px(f49, 1,11,HAB2); px(f49,0,11,SKNS)
px(f49, 0,10,SKNS); px(f49,0,9,SKIN)
px(f49,14,15,HAB1); px(f49,15,15,HAB1)
px(f49,14,14,HAB1); px(f49,15,14,HAB1)
px(f49,15,13,HAB1); px(f49,16,13,HAB2)
px(f49,15,12,HAB1); px(f49,16,12,HAB2)
px(f49,16,11,HAB2); px(f49,17,11,SKNS)
px(f49,17,10,SKNS); px(f49,17,9,SKIN)
# Restaurar borde del velo borrado por _limpiar (solo x=3 y x=14 en y=9-11)
px(f49, 3,9,VEL1);  px(f49,3,10,VEL1);  px(f49,3,11,VEL1)
px(f49,14,9,VEL1);  px(f49,14,10,VEL1); px(f49,14,11,VEL1)
f49.save(os.path.join(DST_DIR, "FRAME49.png"))
print("FRAME49 — Monja levantar manos de espaldas")

# =============================================================================
# MUJER1 — Agregar F36-F39 (biblia) y F44-F45 (canto)
# =============================================================================
MUJ1_DIR = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\PERSONAJES\MUJERES\MUJER1"

def _detect_body_m1(f1_img):
    samples = []
    for _y in range(15, 18):
        for _x in range(4, 14):
            _r, _g, _b, _a = f1_img.getpixel((_x, _y))
            if _a > 0 and not _is_skin_warm(_r, _g, _b, _a):
                samples.append((_r, _g, _b, 255))
    if not samples:
        return (0x30,0x30,0x40,255), (0x50,0x50,0x68,255), (0x70,0x70,0x88,255)
    unique = sorted(set(samples), key=lambda c: c[0]+c[1]+c[2])
    n = len(unique)
    return unique[max(0,n//10)], unique[n//2], unique[min(n-1,9*n//10)]

_m1f1 = Image.open(os.path.join(MUJ1_DIR, "FRAME1.png")).convert("RGBA")
_ms1, _ms2, _ms3 = _detect_body_m1(_m1f1)

def _mslv(x):
    return _ms1 if (x<=5 or x>=12) else (_ms3 if x in (8,9) else _ms2)

for _n in list(range(36, 40)) + list(range(44, 50)):
    _p = os.path.join(MUJ1_DIR, f"FRAME{_n}.png")
    if os.path.exists(_p): os.remove(_p)

for _i in range(1, 2):
    _p = os.path.join(MUJ1_DIR, f"FRAME{_i}.png")
    if not os.path.exists(_p): continue
    _src = Image.open(_p).convert("RGBA")
    _frm = _src.copy()
    for _y in range(15, H):
        for _x in range(W):
            _r, _g, _b, _a = _src.getpixel((_x, _y))
            if _a == 0 or not _is_skin_warm(_r, _g, _b, _a): continue
            _frm.putpixel((_x, _y), _mslv(_x))
    px(_frm,  4,15,_ms2); px(_frm,  5,15,_ms1)
    px(_frm,  4,16,_ms2); px(_frm,  5,16,_ms1)
    px(_frm, 13,15,_ms2); px(_frm, 12,15,_ms1)
    px(_frm, 13,16,_ms2); px(_frm, 12,16,_ms1)
    px(_frm,  4,17,SKNS); px(_frm,  4,18,SKND)
    px(_frm, 13,17,SKNS); px(_frm, 13,18,SKND)
    # Brazo derecho extendido al lado del libro
    px(_frm, 14,16,_ms1); px(_frm, 14,17,_ms1)
    px(_frm, 14,18,_ms1); px(_frm, 14,19,_ms1)
    # Zapato visible a la derecha del libro
    px(_frm, 13,20,SHO); px(_frm, 13,21,SHO)
    for _bx in range(5, 13):
        for _by in range(17, 22):
            if   _bx in (5,12):   _c = BOOK1
            elif _by in (17,21):  _c = BOOK1
            elif _bx in (6,11):   _c = BOOK2
            else:                 _c = BOOKP
            px(_frm, _bx, _by, _c)
    px(_frm, 8,18,BOOKX); px(_frm, 8,19,BOOKX); px(_frm, 8,20,BOOKX)
    px(_frm, 7,19,BOOKX); px(_frm, 9,19,BOOKX)
    _frm.save(os.path.join(MUJ1_DIR, f"FRAME{35+_i}.png"))
    print(f"MUJER1 FRAME{35+_i} — Biblia (base F{_i})")

_m1f1_reload = Image.open(os.path.join(MUJ1_DIR, "FRAME1.png")).convert("RGBA")
_f45m1 = _shift_up_n(_m1f1_reload)
px(_f45m1, 8, 11, MOT)
px(_f45m1, 8, 10, MOT)
_f45m1.save(os.path.join(MUJ1_DIR, "FRAME45.png"))
print("MUJER1 FRAME45 — Cantando: boca abierta 2px")

_f44m1 = _f45m1.copy()
for _cy in range(9, H):
    for _cx in range(4):      _f44m1.putpixel((_cx,_cy),(0,0,0,0))
    for _cx in range(14, W): _f44m1.putpixel((_cx,_cy),(0,0,0,0))
for _cy in range(16, H):
    for _cx in range(4, 14):
        _r,_g,_b,_a = _f44m1.getpixel((_cx,_cy))
        if _a > 0 and _is_skin_warm(_r,_g,_b,_a): _f44m1.putpixel((_cx,_cy),(0,0,0,0))
px(_f44m1, 3,14,_ms1); px(_f44m1, 2,13,_ms1)
px(_f44m1, 1,12,_ms2); px(_f44m1, 0,11,SKNS); px(_f44m1, 0,10,SKIN)
px(_f44m1,14,14,_ms1); px(_f44m1,15,13,_ms1)
px(_f44m1,16,12,_ms2); px(_f44m1,17,11,SKNS); px(_f44m1,17,10,SKIN)
_f44m1.save(os.path.join(MUJ1_DIR, "FRAME44.png"))
print("MUJER1 FRAME44 — Cantando: boca 2px + brazos levantados")

# Helper vista trasera para MUJER1 (pelo amarillo, cuerpo detectado)
def _make_back_m1(src_img):
    img = ImageOps.mirror(src_img).copy()
    # Limpiar cabeza completa (y=0-13) y zona lateral brazos (y=14-21)
    for _y in range(14):
        for _x in range(W): img.putpixel((_x,_y),(0,0,0,0))
    for _y in range(14, 22):
        for _cx in range(4):      img.putpixel((_cx,_y),(0,0,0,0))
        for _cx in range(14, W): img.putpixel((_cx,_y),(0,0,0,0))
    # Pelo amarillo (nuca y corona)
    _H1=(180,135,0,255); _H2=(220,175,0,255); _H3=(255,219,0,255)
    for _y in range(8):
        for _x in range(2,15):
            img.putpixel((_x,_y), _H1 if (_x<=3 or _x>=13) else (_H3 if 7<=_x<=9 else _H2))
    for _y in range(8,12):
        for _x in range(2,15):
            img.putpixel((_x,_y), _H1 if (_x<=3 or _x>=13) else _H2)
    for _y in range(12,14):
        for _x in range(4,13): img.putpixel((_x,_y), SKNS if _x in (7,8,9) else SKND)
    # Hombros y torso limpio y=14-17
    for _y in range(14,18):
        for _cx in range(4,14): img.putpixel((_cx,_y), _ms1 if (_cx<=5 or _cx>=12) else _ms2)
    return img

_m1f1_bk = Image.open(os.path.join(MUJ1_DIR, "FRAME1.png")).convert("RGBA")

# Detectar color del zapato de MUJER1
_m1sh = [(_r,_g,_b,255) for _sy in range(21,H) for _sx in range(W)
         for _r,_g,_b,_a in [_m1f1_bk.getpixel((_sx,_sy))]
         if _a>0 and not _is_skin_warm(_r,_g,_b,_a)]
_m1sh_s = sorted(set(_m1sh), key=lambda c:c[0]+c[1]+c[2]) if _m1sh else []
M1SHD = _m1sh_s[0] if _m1sh_s else _ms1
M1SHM = _m1sh_s[min(len(_m1sh_s)//3,len(_m1sh_s)-1)] if _m1sh_s else _ms2

# F46: Incarse (arrodillada de espaldas)
_f46m1 = _make_back_m1(_m1f1_bk)
for _cx in range(W):
    for _cy in range(18, H): _f46m1.putpixel((_cx,_cy),(0,0,0,0))
for _cx in range(4,14): _f46m1.putpixel((_cx,18), _ms1 if (_cx<=5 or _cx>=12) else _ms2)
for _cy in range(19,21):
    px(_f46m1,3,_cy,_ms1); px(_f46m1,4,_cy,_ms2); px(_f46m1,5,_cy,_ms2); px(_f46m1,6,_cy,_ms1)
    px(_f46m1,11,_cy,_ms1); px(_f46m1,12,_cy,_ms2); px(_f46m1,13,_cy,_ms2); px(_f46m1,14,_cy,_ms1)
for _cx in range(4,8):  _f46m1.putpixel((_cx,21), M1SHD if (_cx==4 or _cx==7) else M1SHM)
for _cx in range(10,14): _f46m1.putpixel((_cx,21), M1SHD if (_cx==10 or _cx==13) else M1SHM)
_f46m1.save(os.path.join(MUJ1_DIR, "FRAME46.png"))
print("MUJER1 FRAME46 — Incarse de espaldas")

# F47: Padre Nuestro de espaldas (brazos horizontales)
_f47m1 = _make_back_m1(_m1f1_bk)
px(_f47m1,3,15,_ms1); px(_f47m1,2,15,_ms1); px(_f47m1,1,15,SKNS); px(_f47m1,0,15,SKIN)
px(_f47m1,3,16,_ms1); px(_f47m1,2,16,_ms1); px(_f47m1,1,16,SKNS); px(_f47m1,0,16,SKND)
px(_f47m1,14,15,_ms1); px(_f47m1,15,15,_ms1); px(_f47m1,16,15,SKNS); px(_f47m1,17,15,SKIN)
px(_f47m1,14,16,_ms1); px(_f47m1,15,16,_ms1); px(_f47m1,16,16,SKNS); px(_f47m1,17,16,SKND)
_f47m1.save(os.path.join(MUJ1_DIR, "FRAME47.png"))
print("MUJER1 FRAME47 — Padre Nuestro de espaldas")

# F48: Dar la paz de espaldas (brazo derecho extendido)
_f48m1 = _make_back_m1(_m1f1_bk)
px(_f48m1,14,15,_ms1); px(_f48m1,15,15,_ms1)
px(_f48m1,14,16,_ms1); px(_f48m1,15,16,_ms2); px(_f48m1,16,16,SKNS)
px(_f48m1,16,17,SKNS); px(_f48m1,17,17,SKIN)
px(_f48m1,17,18,SKIN)
_f48m1.save(os.path.join(MUJ1_DIR, "FRAME48.png"))
print("MUJER1 FRAME48 — Dar la paz de espaldas")

# F49: Levantar manos de espaldas (ambos brazos completamente arriba)
_f49m1 = _make_back_m1(_m1f1_bk)
px(_f49m1, 3,15,_ms1); px(_f49m1,2,15,_ms1)
px(_f49m1, 3,14,_ms1); px(_f49m1,2,14,_ms1)
px(_f49m1, 2,13,_ms1); px(_f49m1,1,13,_ms2)
px(_f49m1, 2,12,_ms1); px(_f49m1,1,12,_ms2)
px(_f49m1, 1,11,_ms2); px(_f49m1,0,11,SKNS)
px(_f49m1, 0,10,SKNS); px(_f49m1,0,9,SKIN)
px(_f49m1,14,15,_ms1); px(_f49m1,15,15,_ms1)
px(_f49m1,14,14,_ms1); px(_f49m1,15,14,_ms1)
px(_f49m1,15,13,_ms1); px(_f49m1,16,13,_ms2)
px(_f49m1,15,12,_ms1); px(_f49m1,16,12,_ms2)
px(_f49m1,16,11,_ms2); px(_f49m1,17,11,SKNS)
px(_f49m1,17,10,SKNS); px(_f49m1,17,9,SKIN)
_f49m1.save(os.path.join(MUJ1_DIR, "FRAME49.png"))
print("MUJER1 FRAME49 — Levantar manos de espaldas")

print(f"""
MUJER10 (Monja) — 49 frames
  Atuendo: habito azul marino, pechera blanca, cruz dorada, velo negro
  Fleco dorado asomando del velo en dy=4-6
  F1-F8   caminata frente
  F9-F14  gestos liturgicos
  F15-F26 señal de la cruz (12 frames)
  F27-F31 espaldas caminando
  F32     espaldas parada
  F33     espaldas sentada
  F36-F39 caminando con Biblia (F1-F4)
  F44     cantando: levanta, 1px boca
  F45     cantando: boca abierta, 2px vertical
  F46     incarse de espaldas
  F47     Padre Nuestro de espaldas (brazos horizontales)
  F48     dar la paz de espaldas (brazo derecho)
  F49     levantar manos de espaldas
MUJER1 — F36-F39 Biblia + F44-F49 agregados
  {DST_DIR}""")
