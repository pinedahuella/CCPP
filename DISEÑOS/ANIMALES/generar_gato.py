import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

# ══════════════════════════════════════════════════════════════════════════════
# GATO v2 — 32×32 px, gato naranja tabby
#   FRAME 01–06  →  IDLE   (parado, cola oscilando, leve bob)
#   FRAME 07–14  →  RUN    (galope de 8 fases)
#   FRAME 15–20  →  BLINK  (parpadeo completo)
# ══════════════════════════════════════════════════════════════════════════════
W, H = 32, 32
BASE    = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS"
OUT_DIR = os.path.join(BASE, "ANIMALES", "GATO1")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Paleta ────────────────────────────────────────────────────────────────────
T   = (  0,   0,   0,   0)
O   = ( 28,  12,   4, 255)   # outline
F   = (210, 112,  32, 255)   # pelaje naranja
FD  = (150,  58,  10, 255)   # oscuro (rayas tabby)
FS  = (235, 158,  62, 255)   # claro (lomo / brillo)
FL  = (248, 212, 152, 255)   # panza
FW  = (252, 244, 230, 255)   # blanco patas y morro
EG  = ( 78, 170,  58, 255)   # ojo verde
EP  = ( 14,   6,   2, 255)   # pupila
EH  = (148, 218, 115, 255)   # brillo ojo
NK  = (220, 108, 130, 255)   # nariz rosa
EI  = (235, 152, 158, 255)   # interior oreja
EID = (190, 108, 116, 255)   # interior oreja oscuro

# ── Helpers ───────────────────────────────────────────────────────────────────
def put(img, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), c)

def getc(img, x, y):
    if 0 <= x < W and 0 <= y < H:
        return img.getpixel((x, y))
    return T

def outline(img):
    """Agrega borde O de 1px alrededor de todos los píxeles visibles."""
    edges = []
    for y in range(H):
        for x in range(W):
            if getc(img, x, y)[3] > 0:
                for dx, dy_ in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x+dx, y+dy_
                    if 0 <= nx < W and 0 <= ny < H and getc(img,nx,ny)[3] == 0:
                        edges.append((nx, ny))
    for x, y in edges:
        put(img, x, y, O)

# ══════════════════════════════════════════════════════════════════════════════
# CUERPO — filas explícitas con rayas tabby y panza clara
# ══════════════════════════════════════════════════════════════════════════════
# (y_row, x_left, x_right) — sin offset; dy se aplica al dibujar
BODY_ROWS = [
    (12, 12, 25),
    (13, 11, 26),
    (14, 10, 27),
    (15, 10, 27),
    (16, 10, 26),
    (17, 11, 25),
    (18, 12, 24),
    (19, 13, 23),
]

def draw_body(img, dy=0, sx=0):
    """sx = píxeles extra a la derecha para estirar en el galope."""
    for (y, xl, xr) in BODY_ROWS:
        ay = y + dy
        for x in range(xl, xr + sx + 1):
            # Rayas tabby en la parte superior del lomo
            if y <= 15:
                seg = (x - xl) // 3
                c = FD if seg % 2 == 0 else (FS if seg % 2 == 1 else F)
            # Panza clara en parte inferior
            elif y >= 17:
                margin = (xr + sx - xl) * 0.18
                c = FL if (xl + margin) < x < (xr + sx - margin) else F
            else:
                c = F
            put(img, x, ay, c)

# ══════════════════════════════════════════════════════════════════════════════
# CABEZA — incluye orejas, ojos, nariz, bigotes
# ══════════════════════════════════════════════════════════════════════════════
HEAD_ROWS = [
    ( 6,  7, 11),   # corona estrecha
    ( 7,  5, 12),
    ( 8,  4, 12),
    ( 9,  4, 12),
    (10,  4, 12),
    (11,  5, 12),
    (12,  6, 12),
    (13,  7, 12),   # cuello / conexión con cuerpo
]

def draw_head(img, dy=0, eye_state='open'):
    # ── Oreja delantera (derecha del canvas) — triangular ────────────────────
    for (x, y) in [(9,3),(8,4),(9,4),(10,4),(8,5),(9,5),(10,5)]:
        put(img, x, y+dy, F)
    # Interior rosa
    put(img, 9, 3+dy, EI)
    put(img, 8, 4+dy, EI);  put(img, 9, 4+dy, EI)
    put(img, 8, 5+dy, EID); put(img, 9, 5+dy, EID)
    # Outline oreja
    for (x,y) in [(8,2),(9,2),(10,2),(7,3),(11,3),(7,4),(11,4),(7,5),(11,5)]:
        if getc(img, x, y+dy)[3] == 0:
            put(img, x, y+dy, O)

    # ── Oreja trasera (izquierda del canvas) — parcialmente visible ───────────
    for (x, y) in [(5,5),(6,5),(5,6),(6,6)]:
        if getc(img, x, y+dy)[3] == 0:
            put(img, x, y+dy, F)
    put(img, 5, 5+dy, EI); put(img, 6, 5+dy, EI)
    for (x,y) in [(4,5),(7,6),(4,6),(4,7)]:
        if getc(img, x, y+dy)[3] == 0:
            put(img, x, y+dy, O)

    # ── Forma de la cabeza (row by row) ──────────────────────────────────────
    for (y, xl, xr) in HEAD_ROWS:
        ay = y + dy
        for x in range(xl, xr+1):
            # Morro/mejilla blanca (lado izquierdo, filas bajas)
            if y >= 9 and x <= 6:
                c = FW
            # Rayas en la frente
            elif y <= 8 and x >= 9:
                seg = (x - 9) // 2
                c = FD if seg % 2 == 0 else F
            else:
                c = F
            put(img, x, ay, c)

    # Brillo dorsal de la cabeza
    for (x,y) in [(7,7),(8,7),(9,7),(8,6)]:
        put(img, x, y+dy, FS)

    # ── Ojo ──────────────────────────────────────────────────────────────────
    ex, ey = 7, 8
    if eye_state == 'open':
        put(img, ex,   ey+dy,   EG); put(img, ex+1, ey+dy,   EG)
        put(img, ex,   ey-1+dy, EG); put(img, ex+1, ey-1+dy, EP)  # pupila arriba-der
        put(img, ex,   ey+1+dy, EP); put(img, ex+1, ey+1+dy, EG)  # pupila abajo-izq
        put(img, ex-1, ey-1+dy, EH)                                 # brillo
    elif eye_state == 'squint':
        put(img, ex,   ey+dy,   EG); put(img, ex+1, ey+dy,   EP)
        put(img, ex,   ey+1+dy, EG); put(img, ex+1, ey+1+dy, EG)
        put(img, ex,   ey-1+dy, O);  put(img, ex+1, ey-1+dy, O)   # párpado
    elif eye_state == 'half':
        put(img, ex,   ey+dy,   EG); put(img, ex+1, ey+dy,   EP)
        put(img, ex,   ey-1+dy, O);  put(img, ex+1, ey-1+dy, O)
    elif eye_state == 'closed':
        put(img, ex-1, ey+dy, O); put(img, ex, ey+dy, O)
        put(img, ex+1, ey+dy, O); put(img, ex+2, ey+dy, O)

    # ── Nariz ────────────────────────────────────────────────────────────────
    put(img, 4, 10+dy, NK); put(img, 5, 10+dy, NK)
    put(img, 4, 11+dy, NK)
    # Línea de la boca
    put(img, 5, 12+dy, O); put(img, 6, 12+dy, O)

    # ── Bigotes (3 líneas blancas hacia la izquierda del morro) ──────────────
    for i in range(3):
        put(img, 3-i, 10+dy, FW)   # bigote superior
        put(img, 3-i, 11+dy, FW)   # bigote inferior

# ══════════════════════════════════════════════════════════════════════════════
# COLA
# ══════════════════════════════════════════════════════════════════════════════
def draw_tail(img, dy=0, swing=0, running=False):
    if running:
        # Cola extendida hacia atrás, casi horizontal
        pts = [(26,18+dy,2),(27,18+dy,2),(28,17+dy,2),
               (29,16+dy,1),(30,16+dy,1)]
    else:
        # Cola arqueada hacia arriba con oscilación
        pts = [
            (26, 19+dy, 2),
            (27, 17+dy, 2),
            (28, 15+dy, 2),
            (28+swing, 13+dy, 2),
            (28+swing, 11+dy, 1),
            (27+swing,  9+dy, 1),
            (26+swing,  8+dy, 1),
            (25+swing,  7+dy, 1),
        ]
    for i, (tx, ty, tw) in enumerate(pts):
        t = i / max(len(pts)-1, 1)
        c = FS if t > 0.5 else F
        for ox in range(tw):
            put(img, tx+ox, ty, c)

# ══════════════════════════════════════════════════════════════════════════════
# PATAS — 4 patas, 2px ancho × 7px largo; blanco en la punta
# ══════════════════════════════════════════════════════════════════════════════
FL_X, FR_X, BL_X, BR_X = 13, 16, 21, 24
LEG_LEN = 7

def draw_leg(img, x, y_top, raised=False, fwd=True):
    """raised=True → pata levantada (solo mitad superior + pie doblado)."""
    if raised:
        n = LEG_LEN // 2
        for i in range(n):
            c = FW if i >= n-1 else F
            put(img, x,   y_top+i, c)
            put(img, x+1, y_top+i, c)
        # Pie doblado hacia adelante o atrás
        bx = x - 2 if fwd else x + 2
        put(img, bx,   y_top+n-1, FW)
        put(img, bx+1, y_top+n-1, FW)
    else:
        for i in range(LEG_LEN):
            c = FW if i >= LEG_LEN-2 else F
            put(img, x,   y_top+i, c)
            put(img, x+1, y_top+i, c)

def draw_legs(img, dy=0, fl=False, fr=False, bl=False, br=False):
    leg_top = BODY_ROWS[-1][0] + dy + 1   # justo bajo el cuerpo
    draw_leg(img, FL_X, leg_top, raised=fl, fwd=True)
    draw_leg(img, FR_X, leg_top, raised=fr, fwd=True)
    draw_leg(img, BL_X, leg_top, raised=bl, fwd=False)
    draw_leg(img, BR_X, leg_top, raised=br, fwd=False)

# ══════════════════════════════════════════════════════════════════════════════
# MAKE_FRAME — ensambla un frame completo
# ══════════════════════════════════════════════════════════════════════════════
def make_frame(dy=0, sx=0, swing=0, eye='open', running=False,
               fl=False, fr=False, bl=False, br=False):
    img = Image.new("RGBA", (W, H), T)
    # La cabeza se mueve la mitad que el cuerpo (más estable en carrera)
    hdy = dy // 2 if running else dy

    draw_tail(img, dy=dy, swing=swing, running=running)
    draw_body(img, dy=dy, sx=sx)
    draw_legs(img, dy=dy, fl=fl, fr=fr, bl=bl, br=br)
    draw_head(img, dy=hdy, eye_state=eye)
    outline(img)
    return img

# ══════════════════════════════════════════════════════════════════════════════
# DEFINICIÓN DE FRAMES
# ══════════════════════════════════════════════════════════════════════════════

# ── IDLE (6 frames): bob -1/0 alterno, cola oscila de -2 a +2 ────────────────
# (dy, swing)
IDLE = [(0,-2),(-1,-1),(0,0),(-1,1),(0,2),(-1,1)]

# ── RUN (8 frames): galope de 8 fases ────────────────────────────────────────
# (dy, sx, fl, fr, bl, br)
RUN = [
    ( 0, 0, False,True, True, False),   # 07 contacto A: FL/BR abajo
    (-2, 1, False,True, True, False),   # 08 despegue
    (-4, 2, True, True, True, True ),   # 09 vuelo pico (todos recogidos)
    (-2, 2, True, False,False,True ),   # 10 extensión B
    ( 0, 0, True, False,False,True ),   # 11 contacto B: FR/BL abajo
    (-2, 1, True, False,False,True ),   # 12 despegue B
    (-4, 2, True, True, True, True ),   # 13 vuelo pico B
    (-2, 2, False,True, True, False),   # 14 extensión A
]

# ── BLINK (6 frames): open→squint→half→closed→half→open ─────────────────────
BLINK = ['open','squint','half','closed','half','open']

# ══════════════════════════════════════════════════════════════════════════════
# GENERAR
# ══════════════════════════════════════════════════════════════════════════════
n = 1

for (dy, swing) in IDLE:
    img = make_frame(dy=dy, swing=swing)
    img.save(os.path.join(OUT_DIR, f"FRAME{n:02d}.png"))
    print(f"  [IDLE  {n}/6]  FRAME{n:02d}.png"); n += 1

for (dy, sx, fl, fr, bl, br) in RUN:
    img = make_frame(dy=dy, sx=sx, eye='squint', running=True,
                     fl=fl, fr=fr, bl=bl, br=br)
    img.save(os.path.join(OUT_DIR, f"FRAME{n:02d}.png"))
    print(f"  [RUN   {n-6}/8]  FRAME{n:02d}.png"); n += 1

for eye in BLINK:
    img = make_frame(eye=eye)
    img.save(os.path.join(OUT_DIR, f"FRAME{n:02d}.png"))
    print(f"  [BLINK {n-14}/6]  FRAME{n:02d}.png"); n += 1

print(f"""
=== GATO v2 — {n-1} frames 32×32 en: {OUT_DIR}
    FRAME01-06  → IDLE  (parado, cola oscila)
    FRAME07-14  → RUN   (galope 8 fases)
    FRAME15-20  → BLINK (parpadeo)
""")
