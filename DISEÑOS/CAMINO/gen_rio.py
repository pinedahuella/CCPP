import sys, math
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
import os

# ==============================================================================
# CONFIG
# ==============================================================================
W, H      = 32, 64
N_FRAMES  = 48          # 48 frames → saltos suaves de 8 pasos + loop perfecto

BASE    = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS"
OUT_DIR = os.path.join(BASE, "RIO")
os.makedirs(OUT_DIR, exist_ok=True)

# ==============================================================================
# PALETA — 8 niveles de profundidad
# ==============================================================================
W_ABYSS   = (0x03, 0x11, 0x44, 255)
W_DEEP    = (0x07, 0x26, 0x68, 255)
W_MID     = (0x0D, 0x42, 0x98, 255)
W_MID_L   = (0x17, 0x60, 0xBE, 255)
W_LIGHT   = (0x28, 0x84, 0xD8, 255)
W_FOAM    = (0x5C, 0xAE, 0xE6, 255)
W_CAUSTIC = (0x9C, 0xD6, 0xF6, 255)
W_BRIGHT  = (0xD4, 0xEE, 0xFF, 255)
W_EDGE    = (0x02, 0x0B, 0x2E, 255)
TRANSP    = (0, 0, 0, 0)

# ==============================================================================
# BORDES CURVOS
# ==============================================================================
K = 2 * math.pi / H

def left_edge(y):
    n = (5.0*math.sin(y*K*1+0.40)+3.2*math.sin(y*K*2+1.80)+2.0*math.sin(y*K*3+0.70)
        +1.3*math.sin(y*K*5+2.50)+0.8*math.sin(y*K*7+1.20)+0.5*math.sin(y*K*9+3.10)
        +0.3*math.sin(y*K*13+0.90))
    return 1.5 + (n + 13.1) / 26.2 * 9.5

def right_edge(y):
    n = (5.0*math.sin(y*K*1+3.80)+3.2*math.sin(y*K*2+5.20)+2.0*math.sin(y*K*3+2.10)
        +1.3*math.sin(y*K*5+4.70)+0.8*math.sin(y*K*7+0.30)+0.5*math.sin(y*K*9+5.80)
        +0.3*math.sin(y*K*13+2.70))
    return 21.5 + (n + 13.1) / 26.2 * 9.0

EDGES = [(left_edge(y), right_edge(y)) for y in range(H)]

def in_river(x, y):
    lx, rx = EDGES[y % H]
    return lx <= x <= rx

# ==============================================================================
# AGUA ANIMADA — 6 olas + caustica, loop perfecto via sin(2π*f/N)
# ==============================================================================
def water_color(x, y, frame):
    ph = 2 * math.pi * frame / N_FRAMES

    w1 = math.sin(y * 0.40 - ph * 2.30) * 0.30
    w2 = math.sin(y * 0.82 + x * 0.26 - ph * 1.70) * 0.19
    w3 = math.sin(x * 0.58 + y * 0.17 - ph * 0.95) * 0.13
    w4 = math.sin(y * 1.35 - ph * 3.20 + x * 0.11) * 0.09
    w5 = math.sin(x * 0.88 - ph * 0.65 + y * 0.06) * 0.06
    w6 = math.sin(y * 0.22 + x * 0.38 - ph * 0.45) * 0.04
    # caustica: interferencia de luz refractada
    c1 = math.sin(x * 1.90 + y * 0.85 - ph * 5.50) * 0.11
    c2 = math.sin(x * 0.72 - y * 1.60 + ph * 4.20) * 0.09
    c3 = math.sin((x + y) * 1.10 - ph * 3.80) * 0.06

    t = ((w1+w2+w3+w4+w5+w6+c1+c2+c3) + 1.07) / 2.14
    t = max(0.0, min(1.0, t))

    if   t > 0.935: return W_BRIGHT
    elif t > 0.840: return W_CAUSTIC
    elif t > 0.720: return W_FOAM
    elif t > 0.570: return W_LIGHT
    elif t > 0.410: return W_MID_L
    elif t > 0.260: return W_MID
    elif t > 0.110: return W_DEEP
    else:           return W_ABYSS

# ==============================================================================
# SPRITE DEL PEZ — 5×7 px
# '#'=cuerpo claro  'd'=lado oscuro  'o'=ojo
# ==============================================================================
FISH_BODY = [
    ".ddd.",   # 0 hocico
    "d###d",   # 1 cabeza
    "do##d",   # 2 ojo
    "d###d",   # 3 cuerpo
    ".d#d.",   # 4 estrecho
    "d...d",   # 5 cola
    "d...d",   # 6 cola
]
FISH_FLIP = list(reversed(FISH_BODY))   # cola arriba = subiendo
FISH_H_PX = len(FISH_BODY)   # 7
FISH_W_PX = 5

FISH_COLORS = [
    ((0xFF,0x90,0x18,255),(0xB8,0x3C,0x00,255),(0x14,0x0C,0x04,255)),  # 0 naranja
    ((0xFF,0xD8,0x28,255),(0xCC,0x88,0x00,255),(0x14,0x10,0x00,255)),  # 1 amarillo
    ((0xE8,0x28,0x28,255),(0x98,0x06,0x06,255),(0xFF,0xFF,0xFF,255)),  # 2 rojo
    ((0x30,0xD8,0x60,255),(0x0A,0x78,0x28,255),(0x14,0x0C,0x04,255)),  # 3 verde
    ((0xB0,0x40,0xF0,255),(0x58,0x0A,0x9E,255),(0xFF,0xFF,0xFF,255)),  # 4 morado
    ((0xFF,0xA4,0xCC,255),(0xD8,0x44,0x80,255),(0x14,0x0C,0x04,255)),  # 5 rosa
    ((0x20,0xE4,0xE4,255),(0x06,0x7C,0x7C,255),(0x14,0x0C,0x04,255)),  # 6 cyan
    ((0xF4,0x58,0xA4,255),(0x9C,0x0E,0x4C,255),(0xFF,0xFF,0xFF,255)),  # 7 magenta
]

def sprite_pixels(cx, fy, cidx, flipped=False):
    bl, bd, ey = FISH_COLORS[cidx]
    rows = FISH_FLIP if flipped else FISH_BODY
    out = []
    for row, pattern in enumerate(rows):
        py = fy + row
        for col, ch in enumerate(pattern):
            if ch == '.': continue
            px = cx - 2 + col
            c = ey if ch == 'o' else (bl if ch == '#' else bd)
            out.append((px, py, c))
    return out

# ==============================================================================
# DEFINICION DE PECES
#
# Cada pez tiene una VENTANA activa (f_on, f_off).
# Al inicio de la ventana el pez ENTRA desde arriba (fy = -FISH_H_PX).
# Al final de la ventana el pez SALE por abajo (fy ≈ H).
# Fuera de la ventana: NO se dibuja → periodo genuinamente vacio.
#
# Periodos SIN peces (curvo):
#   Frames  0-5  (6 frames) — inicio del ciclo
#   Frames 22-31 (10 frames) — pausa media larga
#   Frames 45-47 (3 frames) — final antes de reiniciar
#
# TEMPORADA 1 — frames  6-21 : naranja, amarillo(salta 8f), morado, rosa
# TEMPORADA 2 — frames 32-44 : rojo, verde(salta 8f), cyan(salta 8f), magenta
#
# Calidad del salto con 8 frames (t = 0/7 .. 7/7):
#   arc = sin(π*t) → posiciones x: 0%, 43%, 78%, 97%, 97%, 78%, 43%, 0%
#   El pez sale del agua, alcanza el pico, y regresa. Cada paso es visible.
# ==============================================================================

FISH_DEFS = [
    # ── TEMPORADA 1 (frames 6-21) ───────────────────────────────────────────
    # naranja: entra en f6, sale en f21
    {"cx_c":16,"cx_r": 8,"color":0,
     "vis_window":( 6,21),"jump_frames":None,      "jump_dir": 1,"jump_ext":5},

    # amarillo: entra f7, SALTA IZQUIERDA frames 10-17 (8 frames de arco)
    {"cx_c":17,"cx_r":16,"color":1,
     "vis_window":( 7,21),"jump_frames":(10,17),"jump_dir":-1,"jump_ext":5},

    # morado: entra f6, sale antes en f18 (transicion suave)
    {"cx_c":15,"cx_r":24,"color":4,
     "vis_window":( 6,18),"jump_frames":None,      "jump_dir":-1,"jump_ext":4},

    # rosa: entra f8, nada con el banco
    {"cx_c":14,"cx_r":20,"color":5,
     "vis_window":( 8,19),"jump_frames":None,      "jump_dir": 1,"jump_ext":4},

    # ── TEMPORADA 2 (frames 32-44) ──────────────────────────────────────────
    # rojo: ventana completa 32-44
    {"cx_c":14,"cx_r":12,"color":2,
     "vis_window":(32,44),"jump_frames":None,      "jump_dir":-1,"jump_ext":5},

    # verde: entra f33, SALTA DERECHA frames 36-43 (8 frames de arco)
    {"cx_c":17,"cx_r":20,"color":3,
     "vis_window":(33,44),"jump_frames":(36,43),"jump_dir": 1,"jump_ext":5},

    # cyan: entra f32, SALTA DERECHA justo al entrar frames 32-39 (8 frames)
    {"cx_c":16,"cx_r": 6,"color":6,
     "vis_window":(32,43),"jump_frames":(32,39),"jump_dir": 1,"jump_ext":6},

    # magenta: entra f35, pez solitario al final
    {"cx_c":15,"cx_r":26,"color":7,
     "vis_window":(35,44),"jump_frames":None,      "jump_dir":-1,"jump_ext":4},
]

# ==============================================================================
# CALCULAR POSICION Y SALTO DE UN PEZ EN UN FRAME
# ==============================================================================
def compute_fish_frame(fish, frame, variant):
    """
    Devuelve (swim_px, jump_px).
    swim_px: [(px,py,c)] dentro del agua
    jump_px: [(px,py,c)] fuera del agua (salto → visible en transparente)
    """
    f_on, f_off = fish["vis_window"]
    if not (f_on <= frame <= f_off):
        return [], []

    # Velocidad calculada para que el pez entre arriba y salga abajo exacto
    duration = max(1, f_off - f_on)
    speed    = (H + FISH_H_PX) / duration
    fy       = -FISH_H_PX + int((frame - f_on) * speed)

    cx = fish["cx_c"] if variant == "curvo" else fish["cx_r"]

    jf = fish["jump_frames"]
    in_jump = jf is not None and jf[0] <= frame <= jf[1]

    if not in_jump:
        raw  = sprite_pixels(cx, fy, fish["color"], flipped=False)
        swim = [(px,py,c) for px,py,c in raw if 0<=px<W and 0<=py<H]
        return swim, []

    # ── SALTO ────────────────────────────────────────────────────────────────
    jstart, jend = jf
    t    = (frame - jstart) / max(1, jend - jstart)   # 0.0 → 1.0
    arc  = math.sin(math.pi * t)                       # parábola suave
    rising = t < 0.5

    jdir = fish["jump_dir"]
    jext = fish["jump_ext"]

    if variant == "curvo":
        lx, rx = EDGES[max(0, min(H-1, fy))]
        edge_x = lx if jdir == -1 else rx
        x_peak = max(1, min(W-2, edge_x + jdir * jext))
        arc_x  = int(cx + (x_peak - cx) * arc)
    else:
        x_target = 2 if jdir == -1 else W - 3
        arc_x    = int(cx + (x_target - cx) * arc)

    raw = sprite_pixels(arc_x, fy, fish["color"], flipped=rising)

    swim_px, jump_px = [], []
    for px, py, c in raw:
        if not (0 <= px < W and 0 <= py < H): continue
        if variant == "curvo" and not in_river(px, py):
            jump_px.append((px, py, c))
        else:
            swim_px.append((px, py, c))
    return swim_px, jump_px

# ==============================================================================
# SALPICADURAS — sincronizadas con inicio/fin de cada salto
# (cx, cy, f_inicio, duracion)
# ==============================================================================
SPLASH_DEFS = [
    # Amarillo sale del agua (frame 10) y regresa (frame 17)
    (17, 30, 10, 3),
    (17, 30, 17, 2),
    # Verde sale (frame 36) y regresa (frame 43)
    (17, 38, 36, 3),
    (17, 38, 43, 2),
    # Cyan sale al entrar (frame 32) y regresa (frame 39)
    (16, 46, 32, 3),
    (16, 46, 39, 2),
    # Entrada de grupos
    (16,  4,  6, 2),   # naranja entra temporada 1
    (14, 10, 32, 2),   # rojo entra temporada 2
]

SPLASH_RING  = ["..X..", ".X.X.", "X...X", ".X.X.", "..X.."]
SPLASH_SMALL = [".X.", "X.X", ".X."]

def get_splash_pixels(frame):
    out = {}
    for sx, sy, f0, dur in SPLASH_DEFS:
        delta = (frame - f0) % N_FRAMES
        if delta >= dur: continue

        fade   = delta / max(1, dur - 1)
        c_out  = W_BRIGHT  if fade < 0.4 else W_FOAM
        c_mid  = W_CAUSTIC if fade < 0.4 else W_LIGHT

        for row, pat in enumerate(SPLASH_RING):
            for col, ch in enumerate(pat):
                if ch != 'X': continue
                px, py = sx - 2 + col, sy - 2 + row
                if 0 <= px < W and 0 <= py < H:
                    out[(px,py)] = c_out if (row in (0,4) or col in (0,4)) else c_mid

        if fade < 0.5:
            for row, pat in enumerate(SPLASH_SMALL):
                for col, ch in enumerate(pat):
                    if ch != 'X': continue
                    px, py = sx - 1 + col, sy - 1 + row
                    if 0 <= px < W and 0 <= py < H:
                        out[(px,py)] = c_mid

        if 0 <= sx < W and 0 <= sy < H:
            out[(sx,sy)] = W_BRIGHT
    return out

# ==============================================================================
# RENDER
# ==============================================================================
for variant in ("curvo", "recto"):
    for f in range(N_FRAMES):
        bg  = TRANSP if variant == "curvo" else W_DEEP
        img = Image.new("RGBA", (W, H), bg)

        all_swim: dict = {}
        all_jump: dict = {}
        for fish in FISH_DEFS:
            sw, jm = compute_fish_frame(fish, f, variant)
            for px,py,c in sw:
                if 0<=px<W and 0<=py<H: all_swim[(px,py)] = c
            for px,py,c in jm:
                if 0<=px<W and 0<=py<H: all_jump[(px,py)] = c

        splash = get_splash_pixels(f)

        for y in range(H):
            lx, rx     = EDGES[y]
            lx_u, rx_u = EDGES[(y-1) % H]
            lx_d, rx_d = EDGES[(y+1) % H]

            for x in range(W):
                if variant == "curvo":
                    in_wat = lx <= x <= rx
                    if not in_wat:
                        if (x,y) in all_jump:
                            img.putpixel((x,y), all_jump[(x,y)])
                        continue
                    on_edg = (x < lx+1 or x > rx-1 or
                              not (lx_u<=x<=rx_u) or not (lx_d<=x<=rx_d))
                    if on_edg:
                        img.putpixel((x,y), W_EDGE)
                        continue
                else:
                    if x <= 1 or x >= W-2:
                        img.putpixel((x,y), W_EDGE)
                        continue

                if   (x,y) in splash:    img.putpixel((x,y), splash[(x,y)])
                elif (x,y) in all_jump:  img.putpixel((x,y), all_jump[(x,y)])
                elif (x,y) in all_swim:  img.putpixel((x,y), all_swim[(x,y)])
                else:                    img.putpixel((x,y), water_color(x,y,f))

        fname = f"rio_{variant}_f{f+1:02d}.png"
        img.save(os.path.join(OUT_DIR, fname))

    print(f"[{variant.upper()}] {N_FRAMES} frames OK")

print(f"\n=== {N_FRAMES*2} PNGs → {OUT_DIR} ===")
