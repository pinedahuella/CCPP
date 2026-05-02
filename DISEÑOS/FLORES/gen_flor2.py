from PIL import Image
import os

out = r'C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\FLORES\FLOR2'
os.makedirs(out, exist_ok=True)

# ── Paleta ──────────────────────────────────────────────────────────────────
T  = (  0,  0,  0,  0)   # transparente
SG = ( 56,142, 60,255)   # tallo verde medio
SD = ( 27, 94, 32,255)   # tallo oscuro (bordes)
LG = ( 82,168, 58,255)   # hoja verde claro
LD = ( 46,110, 30,255)   # hoja verde oscuro

PO = ( 74, 20,140,255)   # contorno pétalo (violeta muy oscuro)
PD = (123, 31,162,255)   # pétalo oscuro
PM = (171, 71,188,255)   # pétalo medio
PL = (206,147,216,255)   # pétalo claro
PH = (230,200,240,255)   # brillo central


def draw_tulip(d, top_y):
    """
    Dibuja la copa del tulipán con la punta en top_y.
    Centrado en x=15-16. Altura total de la copa: 16 px.
    """
    # (y_relativa, xl, xr) respecto a top_y
    shape = [
        ( 0, 15, 16),   # punta
        ( 1, 14, 17),
        ( 2, 13, 18),
        ( 3, 12, 19),
        ( 4, 11, 20),
        ( 5, 10, 21),
        ( 6, 10, 21),
        ( 7, 10, 21),
        ( 8,  9, 22),   # más ancho
        ( 9,  9, 22),
        (10, 10, 21),
        (11, 11, 20),
        (12, 12, 19),
        (13, 13, 18),
        (14, 14, 17),
        (15, 15, 16),   # base – empalme con tallo
    ]
    for dy, xl, xr in shape:
        y   = top_y + dy
        w   = xr - xl
        mid = (xl + xr) / 2.0
        for x in range(xl, xr + 1):
            if x == xl or x == xr:
                c = PO
            elif x == xl+1 or x == xr-1:
                c = PD
            elif abs(x - mid) < 1.2:
                c = PH
            else:
                c = PM
            d(x, y, c)
        if w > 5:
            d(xl + w//3,   y, PD)
            d(xl + 2*w//3, y, PD)


def mk(mode):
    """
    mode 1 → flor arriba + tallo completo  (igual que FLOR1 frame 1)
    mode 2 → flor a media altura + tallo corto (igual que FLOR1 frame 2)
    mode 3 → solo flor, sin tallo            (igual que FLOR1 frame 3)
    """
    img = Image.new('RGBA', (32,32), T)
    p   = img.load()

    def d(x, y, c):
        if 0 <= x < 32 and 0 <= y < 32:
            p[x, y] = c

    if mode == 1:
        # ── Tallo completo ───────────────────────────────────────────────────
        for y in range(18, 31):
            d(14,y,SD); d(15,y,SG); d(16,y,SG); d(17,y,SD)
        # Hoja izquierda
        for x,y in [(14,23),(13,23),(12,22),(11,22),(10,21),(10,20)]:
            d(x,y,LG)
        for x,y in [(13,24),(12,23),(11,23)]:
            d(x,y,LD)
        # Hoja derecha
        for x,y in [(17,26),(18,26),(19,25),(20,25),(21,24),(21,23)]:
            d(x,y,LG)
        for x,y in [(18,27),(19,26),(20,26)]:
            d(x,y,LD)
        # Flor arriba (punta en y=2)
        draw_tulip(d, top_y=2)

    elif mode == 2:
        # ── Tallo corto ──────────────────────────────────────────────────────
        for y in range(26, 31):
            d(14,y,SD); d(15,y,SG); d(16,y,SG); d(17,y,SD)
        # Solo hoja derecha (la izquierda ya no alcanza a verse)
        for x,y in [(17,28),(18,28),(19,27),(20,27),(21,26)]:
            d(x,y,LG)
        for x,y in [(18,29),(19,28)]:
            d(x,y,LD)
        # Flor a media altura (punta en y=10)
        draw_tulip(d, top_y=10)

    elif mode == 3:
        # ── Solo flor, sin tallo ─────────────────────────────────────────────
        # Flor abajo (punta en y=16)
        draw_tulip(d, top_y=16)

    return img


# ── Guardar los 3 frames ─────────────────────────────────────────────────────
for i, mode in enumerate([1, 2, 3], start=1):
    img = mk(mode)
    img.save(os.path.join(out, f'FRAME{i}.png'))
    print(f'OK  FRAME{i}.png')

print('\nFLOR2 lista – tulipán morado 32×32 px, 3 frames de balanceo.')
