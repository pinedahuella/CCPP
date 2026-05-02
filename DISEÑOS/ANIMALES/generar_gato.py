import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

# ══════════════════════════════════════════════════════════════════════════════
# GATO CAMINANDO v3 — 32×32 px, 4 frames
# Dibujado píxel a píxel para un look limpio y reconocible
# ══════════════════════════════════════════════════════════════════════════════
W, H = 32, 32
BASE    = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS"
OUT_DIR = os.path.join(BASE, "ANIMALES", "GATO1")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Paleta ────────────────────────────────────────────────────────────────────
T   = (  0,   0,   0,   0)
O   = ( 25,  10,   2, 255)   # outline / contorno
F   = (212, 115,  35, 255)   # pelaje naranja base
FD  = (148,  55,   8, 255)   # pelaje oscuro (rayas tabby)
FS  = (238, 162,  65, 255)   # pelaje claro (lomo / brillo)
FL  = (250, 215, 155, 255)   # panza clara
FW  = (252, 245, 232, 255)   # blanco (patas, morro)
EG  = ( 72, 175,  55, 255)   # iris verde
EP  = ( 12,   5,   1, 255)   # pupila negra
EH  = (158, 228, 118, 255)   # brillo del ojo
NK  = (222, 105, 130, 255)   # nariz rosa
EI  = (238, 155, 162, 255)   # interior oreja claro
EID = (188, 105, 115, 255)   # interior oreja oscuro

def put(img, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), c)

def getc(img, x, y):
    if 0 <= x < W and 0 <= y < H: return img.getpixel((x, y))
    return T

def outline(img):
    edges = []
    for y in range(H):
        for x in range(W):
            if getc(img, x, y)[3] > 0:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x+dx, y+dy
                    if 0<=nx<W and 0<=ny<H and getc(img,nx,ny)[3]==0:
                        edges.append((nx,ny))
    for x, y in edges:
        put(img, x, y, O)

# ══════════════════════════════════════════════════════════════════════════════
# GRILLA DE PÍXELES — cada fila es una cadena de 32 chars
#
# Colores:
#  . transparente   O contorno   F naranja   D oscuro   S claro
#  L panza          W blanco     E ojo verde  P pupila   H brillo ojo
#  N nariz          I oreja int  i oreja int oscuro
#
# El gato mira a la IZQUIERDA (cabeza a la izq, cola a la der)
# ══════════════════════════════════════════════════════════════════════════════

# ── BASE del gato (cuerpo + cabeza + cola) — sin patas ───────────────────────
# Las patas se agregan encima según el frame
BASE_GRID = [
 #0         1         2         3
 #0123456789012345678901234567890 1
 "................................",  # 0
 "........OOO.....................",  # 1  — oreja punta
 ".......OIIO.....................",  # 2
 ".......OIIO.....................",  # 3
 "......OIIOO.....................",  # 4
 "......OFFOO.OOOOOOOOOOOOOOOO...",  # 5  — base oreja + lomo cuerpo
 ".....OFFFFFDDDDDDDDDDDDDDSFOO..",  # 6  — cabeza + cuerpo top + cola
 ".....OFFHPFDDDDDDDDDDDDDDOFSOO.",  # 7  — ojo H=brillo, P=pupila
 ".....OFFEPFDDDDDDDDDDDDDDO.FSOO",  # 8  — E=verde, P=pupila
 "....OFWNFFFDDDDDDDDDDDDDOO.OOOO",  # 9  — N=nariz, W=blanco morro
 "....OFWWFFFFFFFDDDDDDDDOO......",  # 10 — morro + panza comienza
 "....OFWWFFFFFFFLLLLLLOOO.......",  # 11
 ".....OFFFFFFFFFFLLLLLOO........",  # 12
 "......OOFFFFFFFFFFLOOO.........",  # 13
 ".......OOOOOOOOOOOOO...........",  # 14 — base del cuerpo
 "...............................",  # 15 — aquí van las patas
 "...............................",  # 16
 "...............................",  # 17
 "...............................",  # 18
 "...............................",  # 19
 "...............................",  # 20
 "...............................",  # 21
 "...............................",  # 22
 "...............................",  # 23
 "...............................",  # 24
 "...............................",  # 25
 "...............................",  # 26
 "...............................",  # 27
 "...............................",  # 28
 "...............................",  # 29
 "...............................",  # 30
 "...............................",  # 31
]

# Mapa de caracteres a colores
CMAP = {
    '.': T, 'O': O, 'F': F, 'D': FD, 'S': FS,
    'L': FL, 'W': FW, 'E': EG, 'P': EP, 'H': EH,
    'N': NK, 'I': EI, 'i': EID,
}

def draw_grid(img, grid, dy=0):
    for row_i, row in enumerate(grid):
        y = row_i + dy
        for x, ch in enumerate(row):
            if ch in CMAP and CMAP[ch] != T:
                put(img, x, y, CMAP[ch])

# ── Segunda oreja (pequeña, detrás) ──────────────────────────────────────────
def draw_back_ear(img, dy=0):
    for (x, y, c) in [
        (5, 4+dy, F), (6, 4+dy, F),
        (5, 5+dy, EI),(6, 5+dy, EI),
        (5, 6+dy, F), (6, 6+dy, F),
    ]:
        if getc(img, x, y)[3] == 0:
            put(img, x, y, c)

# ── Bigotes ───────────────────────────────────────────────────────────────────
def draw_whiskers(img, dy=0):
    # 3 bigotes arriba del morro (x<4, y=9-10)
    for (x, y) in [(3,9+dy),(2,9+dy),(1,9+dy),
                   (3,10+dy),(2,10+dy),(1,10+dy),
                   (3,11+dy),(2,11+dy)]:
        if getc(img, x, y)[3] == 0:
            put(img, x, y, FW)

# ── Ojo (superpone sobre la grilla base) ─────────────────────────────────────
def draw_eye(img, dy=0, state='open'):
    ex, ey = 7, 7   # esquina sup-izq del ojo
    if state == 'open':
        put(img, ex,   ey+dy,   EG); put(img, ex+1, ey+dy,   EG)
        put(img, ex,   ey+1+dy, EG); put(img, ex+1, ey+1+dy, EP)
        put(img, ex,   ey+2+dy, EP); put(img, ex+1, ey+2+dy, EG)
        put(img, ex-1, ey+dy,   EH)                               # brillo
    elif state == 'blink':
        put(img, ex-1, ey+1+dy, O)
        put(img, ex,   ey+1+dy, O)
        put(img, ex+1, ey+1+dy, O)
        put(img, ex+2, ey+1+dy, O)

# ── Cola — curva que cambia entre frames ──────────────────────────────────────
TAIL_PIXELS = {
    #  swing -1 (cola izq)
    -1: [(26,6),(25,7),(24,8),(24,9),(25,10)],
    #  swing 0 (cola centro, recta)
     0: [(27,6),(27,7),(27,8),(26,9),(25,10)],
    #  swing +1 (cola der)
     1: [(28,6),(28,7),(27,8),(26,9),(25,10)],
}

def draw_tail_extra(img, swing=0, dy=0):
    """La cola base ya está en BASE_GRID; aquí añadimos la punta variable."""
    for (x, y) in TAIL_PIXELS.get(swing, TAIL_PIXELS[0]):
        put(img, x, y+dy, FS)

# ══════════════════════════════════════════════════════════════════════════════
# PATAS — definidas explícitamente por frame
#
# Tipo de pata:
#   'down'   = pata recta, en el suelo (7px)
#   'lifted' = pata levantada y doblada (4px + pie doblado)
#   'mid'    = en transición (5px, pie casi recto)
#
# Posiciones x de las 4 patas:
#   FL=10  FR=14  BL=20  BR=24
#   (FL = delantera izquierda = más cerca de la cabeza)
# ══════════════════════════════════════════════════════════════════════════════
LEG_Y_TOP  = 14   # fila donde empiezan las patas (justo bajo el cuerpo)
LEG_FULL   = 8    # largo de pata en el suelo
LEG_SHORT  = 4    # largo de pata levantada

def draw_leg(img, x, leg_type='down', fwd=True):
    """Dibuja una pata de 2px de ancho."""
    y0 = LEG_Y_TOP
    if leg_type == 'down':
        for i in range(LEG_FULL):
            c = FW if i >= LEG_FULL-2 else F
            put(img, x, y0+i, c); put(img, x+1, y0+i, c)
    elif leg_type == 'lifted':
        for i in range(LEG_SHORT):
            c = FW if i >= LEG_SHORT-1 else F
            put(img, x, y0+i, c); put(img, x+1, y0+i, c)
        # Pie doblado (horizontal)
        dx = -2 if fwd else 2
        put(img, x+dx,   y0+LEG_SHORT-1, FW)
        put(img, x+dx+1, y0+LEG_SHORT-1, FW)
    elif leg_type == 'mid':
        for i in range(LEG_FULL-2):
            c = FW if i >= LEG_FULL-3 else F
            put(img, x, y0+i, c); put(img, x+1, y0+i, c)

# Definición de patas por frame: (FL_type, FR_type, BL_type, BR_type)
# fwd=True para patas delanteras, fwd=False para traseras
LEGS_DEF = [
    # Frame 1: FL/BR levantadas (diagonal par 1)
    ('lifted','down',  'down',  'lifted'),
    # Frame 2: transición — todas apoyadas
    ('down',  'down',  'down',  'down'),
    # Frame 3: FR/BL levantadas (diagonal par 2)
    ('down',  'lifted','lifted','down'),
    # Frame 4: transición — todas apoyadas
    ('down',  'down',  'down',  'down'),
]

LEG_X = {'FL': 10, 'FR': 14, 'BL': 20, 'BR': 24}
LEG_FWD = {'FL': True, 'FR': True, 'BL': False, 'BR': False}

def draw_all_legs(img, frame_idx):
    fl, fr, bl, br = LEGS_DEF[frame_idx]
    draw_leg(img, LEG_X['FL'], fl, LEG_FWD['FL'])
    draw_leg(img, LEG_X['FR'], fr, LEG_FWD['FR'])
    draw_leg(img, LEG_X['BL'], bl, LEG_FWD['BL'])
    draw_leg(img, LEG_X['BR'], br, LEG_FWD['BR'])

# ══════════════════════════════════════════════════════════════════════════════
# GENERACIÓN DE LOS 4 FRAMES
# ══════════════════════════════════════════════════════════════════════════════
# (tail_swing, eye_state)
FRAME_DEFS = [
    (-1, 'open'),   # Frame 1: cola a izquierda
    ( 0, 'open'),   # Frame 2: cola al centro
    ( 1, 'open'),   # Frame 3: cola a derecha
    ( 0, 'blink'),  # Frame 4: cola al centro, parpadeo
]

for i, (swing, eye) in enumerate(FRAME_DEFS):
    img = Image.new("RGBA", (W, H), T)

    # 1. Grilla base (cuerpo + cabeza + cola parcial)
    draw_grid(img, BASE_GRID, dy=0)
    draw_back_ear(img)
    draw_tail_extra(img, swing=swing)
    draw_whiskers(img)

    # 2. Patas según el frame
    draw_all_legs(img, i)

    # 3. Ojo encima (puede variar)
    draw_eye(img, state=eye)

    # 4. Contorno final
    outline(img)

    fname = f"FRAME{i+1}.png"
    img.save(os.path.join(OUT_DIR, fname))
    print(f"  [OK] {fname}")

print(f"\n=== GATO — 4 frames 32×32 en: {OUT_DIR} ===")
