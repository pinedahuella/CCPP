"""
gen_dialogos.py  —  Cuadros de diálogo y cramapera (barra de carga)
=====================================================================
Genera:
  · 9 cuadros de texto rectangulares (192×48 px), sin texto, estilos variados
  · Cramapera (barra de carga) 160×32 px, 13 frames:
      f01–f10: relleno  10 % → 100 %
      f11–f13: desvanecimiento final

Todos se guardan en DIALOGOS/ y se copian a PNGS/.
"""

from PIL import Image, ImageDraw
import os, shutil, pathlib, math

_base    = pathlib.Path(__file__).parent
OUT_DIR  = str(_base)
PNGS_DIR = str(_base.parent / 'PNGS')
os.makedirs(OUT_DIR,  exist_ok=True)
os.makedirs(PNGS_DIR, exist_ok=True)

T = (0, 0, 0, 0)   # transparente

# ─────────────────────────────────────────────────────────────────────────────
# Helper de canvas
# ─────────────────────────────────────────────────────────────────────────────
def cv(w, h):
    img = Image.new('RGBA', (w, h), T)
    p   = img.load()
    dr  = ImageDraw.Draw(img)

    def px(x, y, c):
        if 0 <= x < w and 0 <= y < h:
            p[x, y] = c

    def hl(y, x1, x2, c):
        for x in range(x1, x2 + 1):
            px(x, y, c)

    def vl(x, y1, y2, c):
        for y in range(y1, y2 + 1):
            px(x, y, c)

    def rc(x1, y1, x2, y2, c):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                px(x, y, c)

    return img, dr, p, px, hl, vl, rc


# ─────────────────────────────────────────────────────────────────────────────
# Función auxiliar: aplica alpha a un color
# ─────────────────────────────────────────────────────────────────────────────
def fade(c, a):
    return (c[0], c[1], c[2], a)


# =============================================================================
# ESTILOS DE CUADRO DE DIÁLOGO  (192 × 48)
# =============================================================================
W, H = 192, 48

# ── 1 · Fantasía oscura (borde dorado, fondo negro-azulado) ──────────────────
def dialogo_1():
    img, dr, p, px, hl, vl, rc = cv(W, H)
    BG  = ( 12,  14,  30, 240)
    BO  = ( 20,  22,  48, 255)
    GO  = (180, 140,  40, 255)
    GL  = (240, 200,  80, 255)
    GH  = (255, 230, 120, 255)

    rc(0, 0, W-1, H-1, BO)
    rc(3, 3, W-4, H-4, BG)

    # Borde dorado exterior
    hl(0, 0, W-1, GO);  hl(H-1, 0, W-1, GO)
    vl(0, 0, H-1, GO);  vl(W-1, 0, H-1, GO)
    # Línea interior dorada
    hl(2, 2, W-3, GL);  hl(H-3, 2, W-3, GL)
    vl(2, 2, H-3, GL);  vl(W-3, 2, H-3, GL)

    # Esquinas ornamentadas
    for d in range(6):
        px(d, d,          GH); px(W-1-d, d,        GH)
        px(d, H-1-d,      GH); px(W-1-d, H-1-d,    GH)

    # Remaches dorados en esquinas
    for ox, oy in [(4,4),(W-5,4),(4,H-5),(W-5,H-5)]:
        rc(ox-1, oy-1, ox+1, oy+1, GO)
        px(ox, oy, GH)

    # Separador inferior (línea de subtítulo)
    hl(H-10, 6, W-7, (80, 60, 20, 180))
    hl(H-11, 6, W-7, (120, 90, 30, 100))

    return img

# ── 2 · Limpio / moderno (blanco con borde azul) ─────────────────────────────
def dialogo_2():
    img, dr, p, px, hl, vl, rc = cv(W, H)
    BG  = (250, 252, 255, 245)
    B1  = ( 60, 120, 210, 255)
    B2  = (100, 160, 240, 255)
    SH  = (  0,   0,   0,  30)

    # Sombra
    rc(3, 3, W-1, H-1, SH)
    rc(0, 0, W-4, H-4, BG)

    # Borde azul doble
    hl(0, 0, W-4, B1);  hl(H-4, 0, W-4, B1)
    vl(0, 0, H-4, B1);  vl(W-4, 0, H-4, B1)
    hl(2, 2, W-6, B2);  hl(H-6, 2, W-6, B2)
    vl(2, 2, H-6, B2);  vl(W-6, 2, H-6, B2)

    # Punto de acento en esquinas
    for ox, oy in [(0,0),(W-4,0),(0,H-4),(W-4,H-4)]:
        rc(ox, oy, ox+3, oy+3, B1)

    # Línea decorativa en la parte superior interna
    hl(5, 5, W-9, (60, 120, 210, 60))

    return img

# ── 3 · Madera rústica ────────────────────────────────────────────────────────
def dialogo_3():
    img, dr, p, px, hl, vl, rc = cv(W, H)
    WD  = ( 92,  58,  20, 255)
    WM  = (130,  85,  35, 255)
    WL  = (172, 120,  60, 255)
    WH  = (210, 160, 100, 255)
    BG  = (245, 220, 170, 220)
    GR  = ( 60,  35,   8, 255)

    # Fondo pergamino
    rc(4, 4, W-5, H-5, BG)

    # Marco de madera (6 px grosor)
    for y in range(H):
        for x in range(W):
            in_frame = x < 5 or x >= W-5 or y < 5 or y >= H-5
            if not in_frame:
                continue
            # variación de veta según posición
            import random
            random.seed(x * 97 + y * 13)
            r = random.random()
            if x < 5 or x >= W-5:      # marcos laterales
                if r < 0.6:  c = WM
                elif r < 0.85: c = WL
                else: c = WD
            else:                        # marcos arriba/abajo
                if r < 0.6:  c = WM
                elif r < 0.85: c = WH
                else: c = WD
            px(x, y, c)

    # Bordes exteriores oscuros
    hl(0, 0, W-1, GR);  hl(H-1, 0, W-1, GR)
    vl(0, 0, H-1, GR);  vl(W-1, 0, H-1, GR)

    # Clavos en las esquinas
    for ox, oy in [(2,2),(W-3,2),(2,H-3),(W-3,H-3)]:
        px(ox, oy, GR); px(ox+1, oy, (90,60,20,255)); px(ox, oy+1, (90,60,20,255))

    # Línea de texto
    hl(H-10, 8, W-9, (140, 95, 40, 120))

    return img

# ── 4 · Piedra antigua (gris, runas) ─────────────────────────────────────────
def dialogo_4():
    img, dr, p, px, hl, vl, rc = cv(W, H)
    BG  = ( 52,  50,  48, 235)
    S1  = ( 85,  82,  78, 255)
    S2  = (115, 112, 108, 255)
    SL  = (155, 150, 145, 255)
    SH  = (185, 180, 175, 255)
    EM  = ( 90, 180, 120, 200)    # brillo esmeralda (runa)

    rc(0, 0, W-1, H-1, S1)
    rc(3, 3, W-4, H-4, BG)

    # Relieve de piedra (borde biselado)
    hl(1, 1, W-2, SH);  vl(1, 1, H-2, SH)    # claro (luz)
    hl(H-2, 1, W-2, S1); vl(W-2, 1, H-2, S1)  # oscuro (sombra)
    hl(2, 2, W-3, S2);  vl(2, 2, H-3, S2)
    hl(H-3, 2, W-3, S1); vl(W-3, 2, H-3, S1)

    # Runas decorativas en los bordes
    rune_pts = [
        # izquierda centro
        [(1,18),(1,20),(1,22),(2,19),(2,21)],
        # derecha centro
        [(W-2,18),(W-2,20),(W-2,22),(W-3,19),(W-3,21)],
        # arriba centro
        [(94,1),(96,1),(98,1),(95,2),(97,2)],
        # abajo centro
        [(94,H-2),(96,H-2),(98,H-2),(95,H-3),(97,H-3)],
    ]
    for grp in rune_pts:
        for (rx, ry) in grp:
            px(rx, ry, EM)

    # Separador de línea de texto
    hl(H-11, 5, W-6, S2)
    hl(H-10, 5, W-6, (30, 28, 26, 200))

    return img

# ── 5 · Real / púrpura con ornamentos ────────────────────────────────────────
def dialogo_5():
    img, dr, p, px, hl, vl, rc = cv(W, H)
    BG  = ( 28,  10,  45, 245)
    P1  = ( 80,  20, 120, 255)
    P2  = (130,  50, 180, 255)
    PL  = (190, 110, 230, 255)
    PH  = (220, 170, 255, 255)
    GO  = (200, 165,  50, 255)

    rc(0, 0, W-1, H-1, P1)
    rc(3, 3, W-4, H-4, BG)

    # Marco doble
    hl(1, 1, W-2, P2);  hl(H-2, 1, W-2, P2)
    vl(1, 1, H-2, P2);  vl(W-2, 1, H-2, P2)
    hl(3, 3, W-4, PL);  hl(H-4, 3, W-4, PL)
    vl(3, 3, H-4, PL);  vl(W-4, 3, H-4, PL)

    # Ornamento central superior (corona simple)
    for i, (ox, c) in enumerate([(-2,P2),(-1,PL),(0,PH),(1,PL),(2,P2)]):
        px(W//2 + ox, 0, c)
        px(W//2 + ox, 1, PL)
    # Puntas de corona
    px(W//2 - 2, 0, GO); px(W//2, 0, GO); px(W//2 + 2, 0, GO)

    # Esquinas florales
    floral = [(0,0),(1,0),(0,1),(2,0),(0,2)]
    for ox, oy in [(0,0),(W-3,0),(0,H-3),(W-3,H-3)]:
        sx = 1 if ox == 0 else -1
        sy = 1 if oy == 0 else -1
        for dx, dy in floral:
            px(ox + dx*sx, oy + dy*sy, GO)

    # Línea degradada interna
    hl(H-10, 5, W-6, (100, 40, 140, 150))

    return img

# ── 6 · Naturaleza / verde con enredaderas ───────────────────────────────────
def dialogo_6():
    img, dr, p, px, hl, vl, rc = cv(W, H)
    BG  = ( 20,  38,  18, 235)
    G1  = ( 30,  80,  28, 255)
    G2  = ( 55, 120,  45, 255)
    GL  = ( 90, 165,  70, 255)
    GH  = (140, 210, 110, 255)
    BR  = ( 65,  38,  12, 255)   # ramita marrón

    rc(0, 0, W-1, H-1, G1)
    rc(3, 3, W-4, H-4, BG)

    # Marco de enredadera
    hl(0, 0, W-1, G1);  hl(1, 0, W-1, G2);  hl(2, 0, W-1, GL)
    hl(H-1, 0, W-1, G1); hl(H-2, 0, W-1, G2); hl(H-3, 0, W-1, GL)
    vl(0, 0, H-1, G1);  vl(1, 0, H-1, G2);  vl(2, 0, H-1, GL)
    vl(W-1, 0, H-1, G1); vl(W-2, 0, H-1, G2); vl(W-3, 0, H-1, GL)

    # Hojas en esquinas
    leaf = [(0,0),(1,0),(2,0),(0,1),(1,1),(0,2)]
    for ox, oy in [(3,3),(W-4,3),(3,H-4),(W-4,H-4)]:
        sx = 1 if ox < W//2 else -1
        sy = 1 if oy < H//2 else -1
        for dx, dy in leaf:
            px(ox + dx*sx, oy + dy*sy, GH if dx+dy < 2 else GL)

    # Ramitas a lo largo del borde
    for x in range(8, W-8, 12):
        px(x, 1, BR); px(x+1, 1, BR)
        px(x, H-2, BR); px(x+1, H-2, BR)

    # Brotes pequeños
    for x in range(14, W-14, 24):
        px(x, 0, GH); px(x, H-1, GH)

    hl(H-10, 5, W-6, (40, 80, 30, 130))

    return img

# ── 7 · Fuego / cálido (rojo-naranja) ────────────────────────────────────────
def dialogo_7():
    img, dr, p, px, hl, vl, rc = cv(W, H)
    BG  = ( 35,  12,   5, 245)
    F1  = (160,  50,  10, 255)
    F2  = (210,  90,  20, 255)
    FL  = (245, 145,  40, 255)
    FH  = (255, 200,  80, 255)
    YL  = (255, 240, 100, 255)

    rc(0, 0, W-1, H-1, F1)
    rc(3, 3, W-4, H-4, BG)

    # Borde de llama (degradado)
    for i in range(3):
        c = [F1, F2, FL][i]
        hl(i,   i, W-1-i, c); hl(H-1-i, i, W-1-i, c)
        vl(i,   i, H-1-i, c); vl(W-1-i, i, H-1-i, c)

    # Llamas superiores decorativas
    flame_x = list(range(6, W-6, 10))
    for fx in flame_x:
        px(fx,   0, FH)
        px(fx-1, 1, FL); px(fx+1, 1, FL)
        px(fx,   2, F2)

    # Brillo de ascua en esquinas
    for ox, oy in [(1,1),(W-2,1),(1,H-2),(W-2,H-2)]:
        px(ox, oy, YL)

    # Línea interna
    hl(H-10, 5, W-6, (180, 70, 15, 160))
    hl(H-11, 5, W-6, (120, 40, 8, 80))

    return img

# ── 8 · Hielo / cristal (azul pálido) ────────────────────────────────────────
def dialogo_8():
    img, dr, p, px, hl, vl, rc = cv(W, H)
    BG  = (220, 240, 255, 230)
    IC  = (140, 190, 240, 255)
    ID  = ( 90, 140, 200, 255)
    IH  = (240, 250, 255, 255)
    IS  = (180, 220, 255, 180)

    rc(0, 0, W-1, H-1, IC)
    rc(3, 3, W-4, H-4, BG)

    # Marco biselado helado
    hl(0, 0, W-1, IH); vl(0, 0, H-1, IH)
    hl(H-1, 0, W-1, ID); vl(W-1, 0, H-1, ID)
    hl(2, 2, W-3, IS); vl(2, 2, H-3, IS)
    hl(H-3, 2, W-3, ID); vl(W-3, 2, H-3, ID)

    # Cristales de hielo en esquinas
    for ox, oy, sx, sy in [(3,3,1,1),(W-4,3,-1,1),(3,H-4,1,-1),(W-4,H-4,-1,-1)]:
        px(ox, oy, IH)
        px(ox+sx, oy, IC); px(ox, oy+sy, IC)
        px(ox+2*sx, oy, ID); px(ox, oy+2*sy, ID)
        px(ox+sx, oy+sy, IH)

    # Puntos de brillo dispersos en el fondo
    import random
    random.seed(42)
    for _ in range(8):
        gx = random.randint(6, W-7); gy = random.randint(6, H-7)
        px(gx, gy, IH)

    hl(H-10, 5, W-6, (120, 170, 220, 140))

    return img

# ── 9 · Mínimal elegante (negro con acento plateado) ─────────────────────────
def dialogo_9():
    img, dr, p, px, hl, vl, rc = cv(W, H)
    BG  = ( 18,  18,  18, 252)
    EX  = (  8,   8,   8, 255)
    SL  = (180, 180, 185, 255)
    SM  = (130, 130, 135, 255)
    SH  = (220, 220, 225, 255)
    AC  = (100, 200, 255, 255)    # acento cian

    rc(0, 0, W-1, H-1, EX)
    rc(1, 1, W-2, H-2, BG)

    # Borde plateado de 1 px
    hl(1, 1, W-2, SL); hl(H-2, 1, W-2, SL)
    vl(1, 1, H-2, SL); vl(W-2, 1, H-2, SL)

    # Líneas de acento (esquinas)
    acent_len = 12
    for ox, oy, sx, sy in [(1,1,1,0),(1,1,0,1),(W-2,1,-1,0),(W-2,1,0,1),
                            (1,H-2,1,0),(1,H-2,0,-1),(W-2,H-2,-1,0),(W-2,H-2,0,-1)]:
        for k in range(acent_len):
            px(ox + sx*k, oy + sy*k, AC)

    # Separador inferior
    hl(H-10, 4, W-5, SM)
    # Puntos de acento en separador
    px(4, H-10, AC); px(W-5, H-10, AC)

    return img


# =============================================================================
# CRAMAPERA — Barra de carga  (160 × 32 px)
# =============================================================================
BW, BH = 160, 32

def mk_cargando(pct, alpha_mult=1.0):
    """
    Dibuja una barra de carga al pct% (0–100).
    alpha_mult < 1 para el desvanecimiento final.
    """
    img, dr, p, px, hl, vl, rc = cv(BW, BH)

    def ac(c):   # aplica alpha_mult
        a = int(c[3] * alpha_mult)
        return (c[0], c[1], c[2], a)

    # Colores
    BG  = ac(( 15,  15,  25, 240))
    FR  = ac(( 45,  45,  70, 255))   # fondo del riel
    B1  = ac(( 30,  90, 200, 255))   # barra base
    B2  = ac(( 60, 140, 255, 255))   # barra media
    BLT = ac(( 40, 200, 255, 255))   # brillo de barra
    BO  = ac(( 80,  80, 120, 255))   # borde
    BH_ = ac((200, 230, 255, 255))   # brillo superior
    TR_ = ac(( 20,  20,  35, 230))   # track borde exterior
    PC  = ac((220, 220, 255, 255))   # texto %  (decorativo: puntitos)
    GR  = ac(( 20, 220, 100, 255))   # verde al completarse

    # Fondo
    rc(0, 0, BW-1, BH-1, BG)

    # Marco exterior
    hl(0, 0, BW-1, TR_); hl(BH-1, 0, BW-1, TR_)
    vl(0, 0, BH-1, TR_); vl(BW-1, 0, BH-1, TR_)
    hl(1, 1, BW-2, BO);  hl(BH-2, 1, BW-2, BO)
    vl(1, 1, BH-2, BO);  vl(BW-2, 1, BH-2, BO)

    # Riel interior (donde corre la barra)
    rail_x1, rail_y1 = 6, 10
    rail_x2, rail_y2 = BW-7, BH-11
    rc(rail_x1, rail_y1, rail_x2, rail_y2, FR)
    # Borde del riel
    hl(rail_y1, rail_x1, rail_x2, BO)
    hl(rail_y2, rail_x1, rail_x2, ac((80, 80, 80, 180)))
    vl(rail_x1, rail_y1, rail_y2, BO)
    vl(rail_x2, rail_y1, rail_y2, ac((80, 80, 80, 180)))

    # Barra de progreso
    rail_w = rail_x2 - rail_x1 - 1
    fill_w = int(rail_w * pct / 100)

    if fill_w > 0:
        use_B1  = B1  if pct < 100 else ac((20, 190, 80, 255))
        use_B2  = B2  if pct < 100 else ac((50, 230, 120, 255))
        use_BLT = BLT if pct < 100 else GR

        bx1 = rail_x1 + 1
        bx2 = bx1 + fill_w - 1
        by1 = rail_y1 + 1
        by2 = rail_y2 - 1

        # Fondo de la barra (gradiente vertical)
        for y in range(by1, by2 + 1):
            t = (y - by1) / max(1, by2 - by1)
            r = int(use_B1[0] + (use_B2[0]-use_B1[0]) * t)
            g = int(use_B1[1] + (use_B2[1]-use_B1[1]) * t)
            b = int(use_B1[2] + (use_B2[2]-use_B1[2]) * t)
            a = int(use_B1[3] * alpha_mult)
            hl(y, bx1, bx2, (r, g, b, a))

        # Brillo superior de la barra
        hl(by1,   bx1, bx2, BLT)
        hl(by1+1, bx1, bx2, use_BLT)

        # Segmentos visuales (ranuras cada 14 px)
        for sx in range(bx1 + 14, bx2, 14):
            for y in range(by1, by2+1):
                vl(sx, by1, by2, ac((0, 0, 0, 60)))

        # Brillo en el frente de la barra (borde derecho)
        vl(bx2, by1, by2, BLT)

    # Puntos de progreso decorativos (10 nodos en la línea inferior)
    dot_y = BH - 6
    for i in range(10):
        dot_x = 8 + i * 14
        filled = (i + 1) * 10 <= pct
        dc = ac((60, 140, 255, 255)) if filled else ac((40, 40, 65, 255))
        px(dot_x,   dot_y,   dc)
        px(dot_x+1, dot_y,   dc)
        px(dot_x,   dot_y-1, dc)
        px(dot_x+1, dot_y-1, dc)

    # Estrellita/destello cuando llega a 100%
    if pct == 100:
        cx, cy = BW//2, BH//2
        for d in range(-3, 4):
            px(cx+d, cy, ac((255, 255, 200, 255)))
            px(cx, cy+d, ac((255, 255, 200, 255)))
        px(cx, cy, ac((255, 255, 255, 255)))

    return img


# =============================================================================
# GENERAR TODOS LOS ARCHIVOS
# =============================================================================

# ── 9 cuadros de diálogo ─────────────────────────────────────────────────────
dialogos = [
    ('dialogo_1_fantasía_oscura',   dialogo_1()),
    ('dialogo_2_limpio_moderno',    dialogo_2()),
    ('dialogo_3_madera_rustica',    dialogo_3()),
    ('dialogo_4_piedra_antigua',    dialogo_4()),
    ('dialogo_5_real_purpura',      dialogo_5()),
    ('dialogo_6_naturaleza',        dialogo_6()),
    ('dialogo_7_fuego',             dialogo_7()),
    ('dialogo_8_hielo_cristal',     dialogo_8()),
    ('dialogo_9_minimal',           dialogo_9()),
]

print('Generando cuadros de diálogo...')
for name, img in dialogos:
    local = os.path.join(OUT_DIR,  f'{name}.png')
    copia = os.path.join(PNGS_DIR, f'{name}.png')
    img.save(local)
    shutil.copy2(local, copia)
    print(f'  {name}.png  ({W}×{H} px)')

# ── Cramapera — 13 frames ─────────────────────────────────────────────────────
print('\nGenerando cramapera (barra de carga)...')

# Frames 01–10: 10% → 100%
for i in range(1, 11):
    pct  = i * 10
    img  = mk_cargando(pct, alpha_mult=1.0)
    fname = f'cargando_f{i:02d}_{pct:03d}pct'
    local = os.path.join(OUT_DIR,  f'{fname}.png')
    copia = os.path.join(PNGS_DIR, f'{fname}.png')
    img.save(local)
    shutil.copy2(local, copia)
    print(f'  {fname}.png')

# Frames 11–13: desvanecimiento 66% → 33% → 0%
for j, alpha in enumerate([0.66, 0.33, 0.05], start=11):
    img  = mk_cargando(100, alpha_mult=alpha)
    fname = f'cargando_f{j:02d}_fade'
    local = os.path.join(OUT_DIR,  f'{fname}.png')
    copia = os.path.join(PNGS_DIR, f'{fname}.png')
    img.save(local)
    shutil.copy2(local, copia)
    print(f'  {fname}.png  (alpha={alpha:.0%})')

print(f'\nOK -- 9 dialogos + 13 frames cramapera  ->  DIALOGOS/  y  PNGS/')
