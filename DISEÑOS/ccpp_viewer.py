# -*- coding: utf-8 -*-
"""CCPP Live Viewer v8 — viewer más grande, iglesia completa, río asíncrono, árbol/persona Z-fix"""
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os, math, random

BASE = os.path.join('C:\\', 'Users', 'memit',
                    'OneDrive - Universidad del Istmo', 'CCPP', 'DISE\xd1OS')
PNGS = os.path.join(BASE, 'PNGS')

VW, VH  = 420, 196
SCALE   = 3
FPS     = 12
WORLD_W = 2400

HORIZON = 50
PLAY_Y0 = 62
PLAY_Y1 = 128
RIO_Y   = 133

KEY_SPD = 4.0   # solo flechas mueven la cámara

random.seed(55)

# ─── Utilidades ──────────────────────────────────────────────────
def load(path):
    return Image.open(path).convert('RGBA')

def load_seq(folder, prefix='FRAME', ext='.png'):
    try:
        files = sorted(
            [f for f in os.listdir(folder)
             if f.upper().startswith(prefix.upper()) and f.lower().endswith(ext)],
            key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
        return [load(os.path.join(folder, f)) for f in files]
    except Exception as e:
        print(f"WARN {folder}: {e}")
        return [Image.new('RGBA',(16,16),(200,0,200,255))]

def paste_at(canvas, sprite, x, y):
    cw, ch = canvas.size
    sw, sh = sprite.size
    sx0=max(0,-x); sy0=max(0,-y)
    dx0=max(0, x); dy0=max(0, y)
    sx1=sw-max(0,x+sw-cw); sy1=sh-max(0,y+sh-ch)
    if sx1<=sx0 or sy1<=sy0: return
    r=sprite.crop((sx0,sy0,sx1,sy1))
    canvas.paste(r,(dx0,dy0),r)

def scale_spr(spr, f):
    w,h = spr.size
    return spr.resize((max(1,int(w*f)), max(1,int(h*f))), Image.NEAREST)

def px_scale(spr, f):
    """Solo 0.5x o 1.0x — sin fracciones intermedias que distorsionan caras."""
    factor = 1.0 if f >= 0.72 else 0.5
    w,h = spr.size
    return spr.resize((max(1,int(w*factor)), max(1,int(h*factor))), Image.NEAREST)

def depth_s(y):
    t = max(0., min(1., (y-PLAY_Y0)/(PLAY_Y1-PLAY_Y0)))
    return 0.42 + 0.58*t

def w2s(world_x):
    raw = (world_x - camera_x) % WORLD_W
    if raw > WORLD_W*0.75: raw -= WORLD_W
    return int(raw)

# ─── Assets ──────────────────────────────────────────────────────
print("Cargando assets...")

P = os.path.join(BASE,'PERSONAJES')
hombres = [load_seq(os.path.join(P,f'HOMBRE{i}')) for i in range(1,12)]
mujeres = [load_seq(os.path.join(P,f'MUJER{i}'))  for i in range(1,9)]

C = os.path.join(BASE,'CASAS')
casas_f1 = []
for i in range(1,17):
    try: casas_f1.append(load(os.path.join(C,f'CASA{i}','FRAME1.png')))
    except: pass
try:    iglesia_f1 = load(os.path.join(C,'IGLESIA','FRAME1.png'))
except: iglesia_f1 = casas_f1[0]

flores_f1 = []
for i in range(1,10):
    try: flores_f1.append(load(os.path.join(BASE,'FLORES',f'FLOR{i}','FRAME1.png')))
    except: pass

rio_raw = load_seq(os.path.join(BASE,'RIO'),'rio_recto_f')
rio_h   = [f.rotate(-90, expand=True) for f in rio_raw]
# Fases aleatorias por posición de tile — evita que todos los peces salten juntos
random.seed(77)
RIO_PHASES = [random.randint(0, max(1, len(rio_raw)-1)) for _ in range(128)]
random.seed(55)

M = os.path.join(BASE,'MUEBLES')
mspr = {}
for k,v in {
    'banca_p':'banca_parque.png','banca_ig':'banca_iglesia.png',
    'farol':'farol_parque.png','fuente':'fuente_parque.png',
    'cartel':'cartel_parque.png','basurero':'basurero.png',
    'bebedero':'bebedero.png','mesa':'mesa_parque.png',
    'macetero':'macetero.png','virgen':'virgen.png','estatua':'estatua.png',
    # muebles iglesia
    'retablo':'retablo.png','sagrario':'sagrario.png',
    'pila_bautismal':'pila_bautismal.png','confesionario':'confesionario.png',
    'candelabro':'candelabro.png','imagen_santo':'imagen_santo.png',
    'reclinatorio':'reclinatorio.png','puerta_ig':'puerta_iglesia.png',
    'cirio':'cirio_pascual.png','altar':'altar_mayor.png',
}.items():
    try: mspr[k] = load(os.path.join(M,v))
    except: pass

canasta       = load(os.path.join(PNGS,'Canasta.png'))
alfombra_pic  = load(os.path.join(PNGS,'AlfombraPicnic.png'))

arbol    = load(os.path.join(PNGS,'Arbol.png'))
arbol_fr = load(os.path.join(PNGS,'ArbolFrondoso.png'))
pino     = load(os.path.join(PNGS,'Pino.png'))
roca     = load(os.path.join(PNGS,'Roca.png'))
roca_g   = load(os.path.join(PNGS,'RocaGrande.png'))
gato     = load(os.path.join(PNGS,'Gato.png'))
valla    = load(os.path.join(PNGS,'Valla.png'))
monte_spr  = load(os.path.join(PNGS,'Monte.png'))
fondo_mont = load(os.path.join(PNGS,'FondoMonte.png'))
try:    arbusto_spr = load(os.path.join(PNGS,'MonteCorto.png'))
except: arbusto_spr = Image.new('RGBA',(12,8),(40,140,30,255))

IP = os.path.join(BASE,'ITEMS')
bici_b    = load_seq(os.path.join(IP,'BICICLETA_BASICA'))
bici_v    = load_seq(os.path.join(IP,'BICICLETA_VINTAGE'))
bici_c_seq= load_seq(os.path.join(IP,'BICICLETA_CANASTA'))
carrito   = load_seq(os.path.join(IP,'CARRITO'))

CAM = os.path.join(BASE,'CAMINO')
def h_tile(name):
    return load(os.path.join(CAM,name)).rotate(90, expand=True)

def h_tile_s(name, s=0.55):
    raw = load(os.path.join(CAM,name)).rotate(90, expand=True)
    return scale_spr(raw, s)

def bg_road_tile(name, s=0.32):
    raw = load(os.path.join(CAM,name)).rotate(90, expand=True)
    return scale_spr(raw, s)

tile_lodo_bg   = bg_road_tile('camino_lodo_recto.png')
tile_piedra_bg = bg_road_tile('camino_piedra_recto.png')

tile_lodo_h    = h_tile_s('camino_lodo_recto.png')
tile_piedra_h  = h_tile_s('camino_piedra_recto.png')
tile_mont_h    = h_tile_s('camino_monte_recto.png')
tile_ladr_h    = h_tile_s('camino_ladrillo_recto.png')
tile_alfombra_h= h_tile('camino_alfombra_recto.png')
tile_iglesia_h = h_tile('camino_iglesia_recto.png')

_proc_names = [
    'camino_procesion_recto.png','camino_procesion2_recto.png',
    'camino_procesion3_recto.png','camino_procesion4_recto.png',
    'camino_procesion5_recto.png','camino_procesion6_recto.png',
    'camino_procesion7_recto.png','camino_procesion8_recto.png',
    'camino_alfombra_recto.png','camino_iglesia_recto.png',
]
proc_tiles_h = [load(os.path.join(CAM,n)).rotate(90,expand=True) for n in _proc_names]

tile_lodo_v    = load(os.path.join(CAM,'camino_lodo_recto.png'))
tile_piedra_v  = load(os.path.join(CAM,'camino_piedra_recto.png'))

print("Assets listos!")

# ─── Fondo: montañas pixel art (pre-render) ───────────────────────
def build_mountain_bg():
    w  = VW * 2
    h  = HORIZON + 34
    img= Image.new('RGBA',(w,h),(0,0,0,255))
    d  = ImageDraw.Draw(img)

    for y in range(h):
        f = y/h
        d.line([(0,y),(w,y)], fill=(int(48+70*f), int(72+88*f), int(155+28*f)))

    random.seed(7)
    y0 = HORIZON - 24
    for x in range(w):
        y0 += random.choice([-2,-1,-1,0,0,0,1,1,2])
        y0  = max(HORIZON-36, min(HORIZON-12, y0))
        d.line([(x,y0),(x,h)], fill=(55,60,115))

    random.seed(14)
    y0 = HORIZON - 14
    for x in range(w):
        y0 += random.choice([-1,-1,0,0,0,1,1])
        y0  = max(HORIZON-22, min(HORIZON-5, y0))
        d.line([(x,y0),(x,h)], fill=(68,82,90))

    random.seed(21)
    y0 = HORIZON - 6
    for x in range(w):
        y0 += random.choice([-1,0,0,0,1])
        y0  = max(HORIZON-10, min(HORIZON+1, y0))
        d.line([(x,y0),(x,h)], fill=(44,72,38))

    random.seed(55)
    return img

BG_MOUNT = build_mountain_bg()

GROUND = Image.new('RGBA',(VW,VH),(0,0,0,0))
gd = ImageDraw.Draw(GROUND)
random.seed(13)
for y in range(HORIZON-4, VH):
    f = (y-(HORIZON-4))/(VH-HORIZON+4)
    for x in range(VW):
        n = random.randint(-4,4)
        gd.point((x,y), fill=(max(0,int(22+14*f+n//3)),
                               max(0,int(75+24*f+n)),
                               max(0,int(12+6*f+n//4)),255))
random.seed(55)

# ─── Escalas ──────────────────────────────────────────────────────
TS = {
    'casa':1.25,'iglesia':1.55,
    'farol':1.10,'banca_p':1.00,'banca_ig':1.00,
    'fuente':0.78,'mesa':0.48,'macetero':0.55,
    'estatua':0.70,'virgen':0.70,'basurero':0.52,
    'bebedero':0.58,'cartel':0.60,'tendedero':0.75,
    'arbol':1.55,'arbol_fr':1.65,'pino':1.45,
    'bg_arbol':1.90,'bg_arbol_fr':2.00,'bg_pino':1.75,'bg_farol':0.38,
    'roca':0.38,'roca_g':0.46,
    'canasta':0.72,'alfombra_pic':2.20,
    'retablo':0.85,'sagrario':0.65,'pila_bautismal':0.65,
    'confesionario':0.75,'candelabro':0.55,'imagen_santo':0.60,
    'reclinatorio':0.50,'puerta_ig':0.90,'cirio':0.45,'altar':0.80,
    'gato':0.50,'valla':0.85,'arbusto':1.10,
}
FLOR_SCALE  = 0.32
BIKE_SCALE  = 0.48

spr_map = {
    'arbol':arbol,'arbol_fr':arbol_fr,'pino':pino,
    'bg_arbol':arbol,'bg_arbol_fr':arbol_fr,'bg_pino':pino,
    'roca':roca,'roca_g':roca_g,'gato':gato,'valla':valla,
    'canasta':canasta,'alfombra_pic':alfombra_pic,
    'arbusto':arbusto_spr,
}

path_tile_h = {'lodo': tile_lodo_h, 'piedra': tile_piedra_h}
path_tile_v = {'lodo': tile_lodo_v, 'piedra': tile_piedra_v}

# ─── MUNDO ────────────────────────────────────────────────────────
W = []
sitters = []   # (wx, wy, seq, fi) — se renderizan a 1x sin escalar
_SF = 6        # frame 7 (índice 6) = sentado

def add_obj(wx, wy, tp, data=None):
    W.append((wx, wy, tp, data))

def add_bench(wx, wy, btype='banca_p', c1=None, c2=None):
    """Agrega banca + par de personas sentadas (a escala 1x, sin reducir cara)."""
    add_obj(wx, wy, btype, None)
    if c1 is not None and c2 is not None:
        sitters.append((wx-5, wy+1, c1, _SF))
        sitters.append((wx+5, wy+1, c2, _SF))

# ══════════════════════════════════════════════════════════════
# FONDO LEJANO — casas bg + árboles + faroles bg
# ══════════════════════════════════════════════════════════════
BG_HOUSES = [(0,4),(200,9),(420,13),(640,1),(860,6),
             (1060,11),(1260,14),(1460,2),(1660,7),(1880,12)]
for idx,(wx,ci) in enumerate(BG_HOUSES):
    add_obj(wx,    68, 'casa', ci)
    add_obj(wx+105,70, 'bg_pino', None)
    add_obj(wx+155,70, 'bg_arbol', None)
    add_obj(wx+70, 69, 'bg_arbol_fr', None)
    add_obj(wx+10, 75, 'bg_farol', None)
    if idx % 2 == 1:
        add_obj(wx+195, 75, 'bg_farol', None)

# ── PICNICS — en huecos libres entre bg_farol y primer bg_arbol de cada casa ──
# Posiciones verificadas: sin tocar casa, árbol, ni piedra
for px, py, hi, mi in [
    ( 31, 75, 0,11), (233, 75, 1,12), (452, 75, 2,13),
    (672, 75, 3,11), (892, 75, 4,14), (1092,75, 5,15),
    (1292,75, 6,12), (1492,75, 7,16), (1692,75, 8,13),
    (1912,75, 9,11),
]:
    add_obj(px,   py,   'alfombra_pic', None)
    add_obj(px,   py,   'canasta',      None)
    add_obj(px-5, py,   'floor_sitter', hi)
    add_obj(px+5, py,   'floor_sitter', mi)

# ── Vallas al límite posterior del mapa verde — cadena horizontal pegada ──
for vx in range(0, WORLD_W, 5):
    add_obj(vx, 60, 'valla', None)

# ── Faroles en el camino de piedra — posiciones seguras (no tocan casas ni iglesia) ──
for fx in [45, 280, 525, 780, 1240, 1502, 1710, 1965, 2222]:
    add_obj(fx, 119, 'farol', None)

# ══════════════════════════════════════════════════════════════
# ZONA 0 — Entrada (x=0–480)
# ══════════════════════════════════════════════════════════════
add_obj(0,  94,'casa',0);  add_obj(155,90,'casa',3)
add_obj(310,96,'casa',7);  add_obj(460,92,'casa',10)
add_obj(80,118,'casa',1);  add_obj(260,115,'casa',5)
add_obj(420,120,'casa',8)

add_obj(40, 105,'farol',None);  add_obj(200,105,'farol',None)

add_obj(18, 98,'arbol',None);   add_obj(100,102,'arbol_fr',None)
add_obj(195,96,'pino',None);    add_obj(350,100,'arbol',None)
add_obj(440,104,'pino',None)

add_obj(30,115,'roca',None);    add_obj(170,118,'roca_g',None)
add_obj(340,112,'roca',None);   add_obj(430,116,'roca_g',None)

add_obj(20,110,'flor',0);  add_obj(90,106,'flor',5)
add_obj(110,109,'flor',1); add_obj(245,108,'flor',2)
add_obj(360,110,'flor',6)

add_obj(150,112,'gato',None); add_obj(380,119,'gato',None)
# Arbustos zona 0
add_obj(65,107,'arbusto',None); add_obj(220,109,'arbusto',None)
add_obj(320,106,'arbusto',None); add_obj(460,108,'arbusto',None)
# Basureros al costado de algunas casas
add_obj(118, 119,'basurero',None); add_obj(298, 116,'basurero',None)

# ══════════════════════════════════════════════════════════════
# ZONA 1 — Parque (x=500–1000)
# ══════════════════════════════════════════════════════════════
add_obj(520, 92,'casa',2);  add_obj(680,88,'casa',6)
add_obj(840, 94,'casa',11); add_obj(980,90,'casa',14)
add_obj(560,116,'casa',4);  add_obj(720,120,'casa',9)
add_obj(890,118,'casa',13)

add_obj(510, 73,'fuente',None)    # fuente en el monte de fondo
add_obj(630,110,'farol',None);   add_obj(660,112,'basurero',None)
add_obj(700,106,'estatua',None)
add_obj(775,110,'macetero',None);add_obj(810,105,'farol',None)
add_obj(850,108,'cartel',None);  add_obj(890,110,'bebedero',None)
add_obj(930,107,'macetero',None)

add_obj(505,98,'arbol_fr',None); add_obj(590,100,'pino',None)
add_obj(670,96,'arbol',None);    add_obj(760,100,'arbol_fr',None)
add_obj(870,98,'pino',None);     add_obj(955,102,'arbol',None)

add_obj(525,118,'roca',None);    add_obj(615,122,'roca_g',None)
add_obj(745,116,'roca',None);    add_obj(880,120,'roca_g',None)

for wx in [545,635,715,795,905,985]: add_obj(wx,103,'flor',4)

add_obj(570,115,'gato',None); add_obj(800,118,'gato',None)
# Arbustos zona 1
add_obj(515,108,'arbusto',None); add_obj(650,107,'arbusto',None)
add_obj(840,109,'arbusto',None); add_obj(970,107,'arbusto',None)
# Basureros al costado de casas
add_obj(598, 117,'basurero',None); add_obj(757, 121,'basurero',None)

# ══════════════════════════════════════════════════════════════
# ZONA 2 — Iglesia (x=1000–1500)
# ══════════════════════════════════════════════════════════════
add_obj(1080, 88, 'iglesia', None)

add_obj(1300, 94,'casa',7);  add_obj(1480,90,'casa',12)
add_obj(1280,115,'casa',15); add_obj(1430,120,'casa',2)

# Basurero al costado de casa de iglesia
add_obj(1318, 116,'basurero',None)

add_obj(1200,104,'virgen',None)
add_obj(1370,105,'virgen',None); add_obj(1450,110,'bebedero',None)

add_obj(940, 98,'pino',None);  add_obj(965,96,'arbol_fr',None)
add_obj(1300,98,'arbol_fr',None); add_obj(1340,96,'pino',None)
add_obj(1400,100,'arbol',None);   add_obj(1490,98,'pino',None)

add_obj(1290,116,'roca_g',None); add_obj(1420,118,'roca',None)

# Arbustos zona iglesia
add_obj(1015,108,'arbusto',None); add_obj(1160,110,'arbusto',None)
add_obj(1350,107,'arbusto',None); add_obj(1470,109,'arbusto',None)
# Sin flores en zona iglesia
add_obj(1380,115,'gato',None)

# Alfombras religiosas eliminadas

# ══════════════════════════════════════════════════════════════
# ZONA 3 — Residencial (x=1500–2000)
# ══════════════════════════════════════════════════════════════
add_obj(1520,92,'casa',6);  add_obj(1670,88,'casa',10)
add_obj(1820,94,'casa',1);  add_obj(1970,90,'casa',4)
add_obj(1580,118,'casa',8); add_obj(1740,115,'casa',3)
add_obj(1900,120,'casa',11)

add_obj(1548,108,'farol',None); add_obj(1712,105,'farol',None)
add_obj(1810,107,'basurero',None); add_obj(1860,105,'farol',None)
add_obj(1900,108,'cartel',None);   add_obj(1990,107,'macetero',None)

add_obj(1505,98,'arbol',None); add_obj(1600,96,'arbol_fr',None)
add_obj(1690,100,'pino',None); add_obj(1790,98,'arbol',None)
add_obj(1880,96,'arbol_fr',None); add_obj(1975,100,'pino',None)

add_obj(1530,116,'roca',None);  add_obj(1655,120,'roca_g',None)
add_obj(1765,118,'roca',None);  add_obj(1910,122,'roca_g',None)

for wx in [1570,1670,1770,1880,1990]: add_obj(wx,103,'flor',7)

add_obj(1625,115,'gato',None); add_obj(1870,118,'gato',None)
add_obj(1618,117,'basurero',None); add_obj(1878,119,'basurero',None)
# Arbustos zona 3
add_obj(1540,107,'arbusto',None); add_obj(1715,109,'arbusto',None)
add_obj(1840,106,'arbusto',None); add_obj(2000,108,'arbusto',None)

# ══════════════════════════════════════════════════════════════
# ZONA 4 — Salida (x=2000–2400)
# ══════════════════════════════════════════════════════════════
add_obj(2010,92,'casa',9);  add_obj(2160,88,'casa',13)
add_obj(2310,94,'casa',0);  add_obj(2080,118,'casa',7)
add_obj(2250,115,'casa',12)

add_obj(2050,105,'farol',None); add_obj(2150,105,'estatua',None)
add_obj(2220,108,'farol',None); add_obj(2340,105,'macetero',None)
add_obj(2380,108,'virgen',None)

add_obj(2030,98,'pino',None);  add_obj(2120,96,'arbol_fr',None)
add_obj(2210,100,'arbol',None);add_obj(2300,98,'pino',None)
add_obj(2380,96,'arbol_fr',None)

add_obj(2060,116,'roca_g',None); add_obj(2180,120,'roca',None)
add_obj(2310,118,'roca_g',None)

for wx in [2080,2175,2290,2390]: add_obj(wx,103,'flor',8)

add_obj(2140,116,'gato',None); add_obj(2360,118,'gato',None)
# Arbustos zona 4
add_obj(2070,107,'arbusto',None); add_obj(2230,109,'arbusto',None)
add_obj(2340,106,'arbusto',None)

# ══════════════════════════════════════════════════════════════
# SUB-RÍO — objetos debajo del río (se renderizan DESPUÉS del río)
# ══════════════════════════════════════════════════════════════
SUB_Y0 = RIO_Y + 10   # ≈143
SUB_Y1 = VH - 6       # ≈190

def depth_s_sub(y):
    t = max(0., min(1., (y - SUB_Y0) / max(1, SUB_Y1 - SUB_Y0)))
    return 0.55 + 0.45 * t

W_sub = []
def add_sub(wx, wy, tp, data=None):
    W_sub.append((wx, wy, tp, data))

# Arbustos
for ax,ay in [(60,170),(220,173),(400,171),(580,174),(760,172),(940,175),
              (1120,171),(1320,174),(1500,172),(1680,175),(1850,171),(2020,174),
              (2210,170),(2370,173)]:
    add_sub(ax, ay, 'arbusto', None)

# Árboles
for ax,ay in [(160,188),(450,185),(720,189),(980,186),(1250,188),
              (1510,185),(1780,189),(2040,186),(2300,188)]:
    add_sub(ax, ay, 'arbol', None)

for ax,ay in [(280,184),(560,187),(840,184),(1100,188),
              (1380,185),(1650,187),(1920,184),(2180,188)]:
    add_sub(ax, ay, 'arbol_fr', None)

# Flores — densas en toda la zona
for ax,ay in [(55,174),(130,177),(210,174),(310,178),(400,175),(490,178),
              (580,174),(670,177),(760,174),(850,178),(940,175),(1030,178),
              (1110,174),(1200,177),(1290,174),(1380,178),(1460,175),(1540,178),
              (1620,174),(1710,177),(1800,174),(1890,178),(1970,175),(2060,178),
              (2140,174),(2230,177),(2310,174),(2390,178)]:
    add_sub(ax, ay, 'flor', ax % 9)

# Arbustos extra
for ax,ay in [(160,169),(370,172),(620,169),(870,172),(1080,169),
              (1350,172),(1560,169),(1760,172),(2000,169),(2260,172)]:
    add_sub(ax, ay, 'arbusto', None)

# Personas caminando (frame de caminata fijo, dispersas)
for px,py,si in [
    (130,183,0),(350,186,2),(600,184,5),(820,187,8),(1050,183,1),
    (1280,186,3),(1510,184,6),(1740,187,10),(1980,183,4),(2220,186,7),(2390,184,9),
]:
    add_sub(px, py, 'sub_persona', si)

# Gatos
for gx,gy in [(250,182),(490,185),(750,182),(1010,185),(1170,182),
              (1440,185),(1640,182),(1900,185),(2150,182),(2350,185)]:
    add_sub(gx, gy, 'gato', None)

# ─── Personajes ──────────────────────────────────────────────────
class Walker:
    def __init__(self,wx,wy,seq,spd=0.45):
        self.wx=float(wx); self.wy=float(wy)
        self.seq=seq; self.fo=random.randint(0,4)
        self.spd=spd; self._new_dir()

    def _new_dir(self):
        ang=random.uniform(0,math.pi*2)
        s=self.spd*random.uniform(0.7,1.3)
        self.wdx=math.cos(ang)*s; self.wdy=math.sin(ang)*s*0.38
        self.timer=random.randint(90,240)

    def update(self):
        self.wx=(self.wx+self.wdx)%WORLD_W
        self.wy=max(95,min(PLAY_Y1-3,self.wy+self.wdy))
        self.timer-=1
        if self.timer<=0: self._new_dir()

    def get_frame(self,t):
        n = min(5, len(self.seq))   # máximo 5 frames de caminata
        return self.seq[(t+self.fo)%n]

all_seqs=[hombres[i] for i in range(11)]+[mujeres[i] for i in range(len(mujeres))]
# Walkers se inicializan en y≥PLAY_Y0+25 para no aparecer detrás de las casas del fondo
walkers=[Walker(random.randint(0,WORLD_W),
                random.uniform(95,PLAY_Y1-4),
                seq, spd=random.uniform(0.30,0.62))
         for seq in all_seqs]

class SeatedWalker(Walker):
    def update(self): pass   # completamente estático, no se mueve
    def get_frame(self, t):
        fi = min(6, len(self.seq)-1)
        return self.seq[fi]

walkers.append(SeatedWalker(
    random.randint(0, WORLD_W),
    random.uniform(PLAY_Y0+25, PLAY_Y1-10),
    hombres[3], spd=0.20))

# ─── Vehículos con jinete ─────────────────────────────────────────
BIKE_Y0=PLAY_Y0+18; BIKE_Y1=PLAY_Y1-5
SEATED_FRAME=6

class Rider:
    def __init__(self,wx,wy,veh_seq,char_seq,spd=1.1):
        self.wx=float(wx); self.wy=float(wy)
        self.veh_seq=veh_seq; self.char_seq=char_seq
        self.fo=random.randint(0,7); self.spd=spd
        self._new_dir()

    def _new_dir(self):
        ang=random.uniform(0,math.pi*2)
        s=self.spd*random.uniform(0.8,1.2)
        self.wdx=math.cos(ang)*s; self.wdy=math.sin(ang)*s*0.28
        self.timer=random.randint(80,200)

    def update(self):
        self.wx=(self.wx+self.wdx)%WORLD_W
        self.wy=max(BIKE_Y0,min(BIKE_Y1,self.wy+self.wdy))
        self.timer-=1
        if self.timer<=0: self._new_dir()

    def get_combo(self,t,ds):
        ds_e = max(ds, 0.54)
        veh  = scale_spr(self.veh_seq[(t+self.fo)%len(self.veh_seq)], ds_e*BIKE_SCALE)
        fi   = min(SEATED_FRAME, len(self.char_seq)-1)
        cha  = self.char_seq[fi]   # 1x — sin escalar la cara
        seat = int(veh.height * 0.42)
        char_top = veh.height - seat - cha.height
        total_h  = veh.height + max(0, -char_top)
        offset_v = max(0, -char_top)
        cw = max(veh.width, cha.width) + 2
        combo = Image.new('RGBA',(cw, total_h),(0,0,0,0))
        bx = (cw-veh.width)//2
        combo.paste(veh,(bx, offset_v), veh)
        cx = (cw-cha.width)//2
        cy = offset_v + char_top
        combo.paste(cha,(cx, max(0,cy)), cha)
        return combo

CART_Y0, CART_Y1 = 116, 127   # carritos solo en la carretera de cemento

class CartRider(Rider):
    """Carrito que circula exclusivamente por la carretera de piedra."""
    def update(self):
        self.wx=(self.wx+self.wdx)%WORLD_W
        self.wy=max(CART_Y0,min(CART_Y1,self.wy+self.wdy))
        self.timer-=1
        if self.timer<=0: self._new_dir()

# Bicis y bici-canastas
_bike_chars=[hombres[0],hombres[2],mujeres[0],
             hombres[5],hombres[7],mujeres[3],hombres[9],
             mujeres[1],mujeres[5],hombres[1]]
_bike_vehs =[bici_b,bici_v,bici_c_seq,bici_b,bici_v,bici_b,
             bici_v,bici_c_seq,bici_v,bici_b]
riders=[Rider(random.randint(0,WORLD_W),
              random.uniform(BIKE_Y0,BIKE_Y1),
              vs, cs, spd=random.uniform(0.9,1.5))
        for vs,cs in zip(_bike_vehs,_bike_chars)]

# Carritos: circulan por la carretera de cemento
_cart_chars=[hombres[3],mujeres[4],hombres[6],mujeres[2],
             hombres[8],mujeres[0],hombres[1],mujeres[6]]
riders += [CartRider(random.randint(0,WORLD_W),
                     random.uniform(CART_Y0,CART_Y1),
                     carrito, cs, spd=random.uniform(0.7,1.2))
           for cs in _cart_chars]

# Carrito visible al inicio — aparece justo al frente del jugador
riders.append(CartRider(160, 122, carrito, hombres[5], spd=0.85))

# ─── Caminadores sub-río ──────────────────────────────────────────
SUB_WALK_Y0 = 175
SUB_WALK_Y1 = 191

class SubWalker:
    """Persona que camina en la zona verde debajo del río."""
    def __init__(self, wx, wy, seq, spd=0.40):
        self.wx  = float(wx)
        self.wy  = float(wy)
        self.seq = seq
        self.fo  = random.randint(0, 4)
        self.spd = spd
        self._new_dir()

    def _new_dir(self):
        # Movimiento mayormente horizontal con poca variación vertical
        ang = random.uniform(-0.3, 0.3) if random.random() < 0.5 else random.uniform(math.pi-0.3, math.pi+0.3)
        s   = self.spd * random.uniform(0.8, 1.2)
        self.wdx   = math.cos(ang) * s
        self.wdy   = math.sin(ang) * s * 0.2
        self.timer = random.randint(120, 280)

    def update(self):
        self.wx = (self.wx + self.wdx) % WORLD_W
        self.wy = max(SUB_WALK_Y0, min(SUB_WALK_Y1, self.wy + self.wdy))
        self.timer -= 1
        if self.timer <= 0:
            self._new_dir()

    def get_frame(self, t):
        n = min(5, len(self.seq))
        return self.seq[(t + self.fo) % n]

# Solitarios
sub_walkers = []
_sw_solo = [
    (120, 180, hombres[0]),  (480, 183, mujeres[1]),
    (750, 181, hombres[4]),  (1020,184, mujeres[3]),
    (1300,180, hombres[7]),  (1550,183, mujeres[5]),
    (1820,181, hombres[2]),  (2080,184, mujeres[7]),
    (2300,180, hombres[9]),  (2400,183, mujeres[0]),
]
for wx,wy,seq in _sw_solo:
    sub_walkers.append(SubWalker(wx, wy, seq, spd=random.uniform(0.30,0.55)))

# Parejas — dos personas juntas con misma dirección
_sw_pairs = [
    (350, 182, hombres[1],  mujeres[2]),
    (680, 180, hombres[5],  mujeres[6]),
    (1150,183, hombres[8],  mujeres[4]),
    (1650,181, hombres[3],  mujeres[1]),
    (1980,184, hombres[10], mujeres[7]),
]
for wx,wy,s1,s2 in _sw_pairs:
    spd = random.uniform(0.28, 0.45)
    ang = random.uniform(-0.2, 0.2)
    w1  = SubWalker(wx,    wy,   s1, spd)
    w2  = SubWalker(wx+8,  wy+1, s2, spd)
    # Misma dirección inicial para que caminen juntos
    w1.wdx = w2.wdx = math.cos(ang) * spd
    w1.wdy = w2.wdy = 0.0
    sub_walkers.extend([w1, w2])

# ─── Estado cámara ────────────────────────────────────────────────
camera_x = 0.0
cam_vel  = 0.0

# ─── Render ───────────────────────────────────────────────────────
t = 0

def make_frame():
    global t, camera_x

    camera_x = (camera_x + cam_vel) % WORLD_W

    canvas = Image.new('RGBA',(VW,VH),(0,0,0,255))

    # 1. Montañas pixel art con parallax lento
    mw    = BG_MOUNT.width
    m_off = int(camera_x * 0.04) % mw
    for ox in range(-m_off, VW+mw, mw):
        paste_at(canvas, BG_MOUNT, ox, 0)

    # 2. Monte al horizonte (parallax 0.20)
    mo = int(camera_x*0.20) % monte_spr.width
    for mx in range(-mo, VW+monte_spr.width, monte_spr.width):
        paste_at(canvas, monte_spr,   mx, HORIZON-8)
        paste_at(canvas, fondo_mont,  mx, HORIZON-2)

    cam_off = int(camera_x)

    # 3. Pasto
    paste_at(canvas, GROUND, 0, 0)

    # 3b. Calle horizontal del fondo (lodo)
    bg_tw  = tile_lodo_bg.width
    bg_off = cam_off % bg_tw
    for gx in range(-bg_off, VW+bg_tw, bg_tw):
        paste_at(canvas, tile_lodo_bg, gx, 74)

    # 4. Caminos horizontales del frente
    def tile_h_strip(tile, y):
        tw  = tile.width
        off = cam_off % tw
        for gx in range(-off, VW+tw, tw):
            paste_at(canvas, tile, gx, y)

    tile_h_strip(tile_lodo_h,   100)
    tile_h_strip(tile_piedra_h, 114)   # camino piedra más ancho — arriba extra
    tile_h_strip(tile_piedra_h, 118)
    tile_h_strip(tile_piedra_h, 121)

    # 5. Camino de piedra fijo arriba del río
    tile_h_strip(tile_piedra_h, 128)

    # 6. Renderables
    items = []

    def add(ys, spr, cx, yf):
        items.append((ys, cx-spr.width//2, yf-spr.height, spr))

    for wx,wy,otype,data in W:
        sx = w2s(wx)
        if not(-65 < sx < VW+65): continue
        ds = depth_s(wy)

        if otype=='casa':
            ci  = data % len(casas_f1)
            spr = scale_spr(casas_f1[ci], ds*TS['casa'])
            add(wy, spr, sx, wy)

        elif otype=='iglesia':
            spr = scale_spr(iglesia_f1, TS['iglesia'])
            add(wy, spr, sx, wy)

        elif otype in mspr:
            spr = scale_spr(mspr[otype], ds*TS.get(otype,0.70))
            add(wy, spr, sx, wy)

        elif otype=='flor':
            fi  = data % len(flores_f1)
            spr = scale_spr(flores_f1[fi], ds*FLOR_SCALE)
            add(wy, spr, sx, wy)

        elif otype in spr_map:
            if otype == 'gato':
                add(wy, spr_map['gato'], sx, wy)
            elif otype in ('arbol','arbol_fr','pino','bg_arbol','bg_arbol_fr','bg_pino'):
                # Árboles siempre se renderizan ANTES que personas (sort key bajo)
                spr = scale_spr(spr_map[otype], ds*TS.get(otype,0.65))
                add(wy - 0.5, spr, sx, wy)
            else:
                spr = scale_spr(spr_map[otype], ds*TS.get(otype,0.65))
                add(wy, spr, sx, wy)

        elif otype=='path_bg_v':
            tile = path_tile_v.get(data, tile_lodo_v)
            spr  = scale_spr(tile, 0.30)
            add(wy, spr, sx, wy)

        elif otype=='bg_farol':
            if 'farol' in mspr:
                spr = scale_spr(mspr['farol'], 0.36)
                add(wy, spr, sx, wy)

        elif otype=='alfombra_rel':
            ti  = (data or 0) % len(proc_tiles_h)
            spr = scale_spr(proc_tiles_h[ti], ds*0.60)
            add(wy, spr, sx, wy)

        elif otype=='floor_sitter':
            idx = (data or 0) % len(all_seqs)
            seq = all_seqs[idx]
            fi2 = min(6, len(seq)-1)
            spr = seq[fi2]   # 1x siempre — sin reducir para preservar cara
            # sort DESPUÉS de la manta (wy+1) y pies sobre la manta
            add(wy+1, spr, sx, wy-1)

    # Sentados en bancas — a escala original, sin reducir cara
    for swx,swy,seq,fi in sitters:
        sx = w2s(swx)
        if -25 < sx < VW+25:
            fi2 = min(fi, len(seq)-1)
            spr = seq[fi2]   # 1x
            add(swy, spr, sx, swy)

    # Caminadores — depth sort natural para que casas los tapen correctamente
    for w in walkers:
        w.update()
        sx = w2s(w.wx)
        if -20 < sx < VW+20:
            add(int(w.wy), w.get_frame(t), sx, int(w.wy))

    # Jinetes (bici + persona sentada)
    for r in riders:
        r.update()
        sx = w2s(r.wx)
        if -55 < sx < VW+55:
            combo = r.get_combo(t, depth_s(r.wy))
            add(int(r.wy), combo, sx, int(r.wy))

    items.sort(key=lambda r: r[0])
    for _,px,py,spr in items:
        paste_at(canvas, spr, px, py)


    # 7. Río al frente — cada tile tiene fase aleatoria independiente
    rio_n   = len(rio_h)
    rw      = rio_h[0].width
    rio_off = cam_off % rw
    for gx in range(-rio_off, VW+rw, rw):
        tile_idx = ((gx + cam_off) // rw) % len(RIO_PHASES)
        phase    = RIO_PHASES[tile_idx]
        rio_fi   = ((t // 4) + phase) % rio_n
        paste_at(canvas, rio_h[rio_fi], gx, RIO_Y)

    # 8. Sub-río — renderizar en canvas separado y clipear al borde inferior del río
    rio_clip_y = RIO_Y + rio_h[0].height   # primer pixel visible debajo del río
    sub_canvas = Image.new('RGBA', (VW, VH), (0, 0, 0, 0))

    sub_items = []
    def add_s(ys, spr, cx, yf):
        sub_items.append((ys, cx - spr.width//2, yf - spr.height, spr))

    for wx, wy, otype, data in W_sub:
        sx = w2s(wx)
        if not(-65 < sx < VW+65): continue
        ds = depth_s_sub(wy)
        if otype in ('arbol','arbol_fr','pino'):
            spr2 = scale_spr(spr_map[otype], ds*TS.get(otype,1.0))
            add_s(wy - 0.5, spr2, sx, wy)
        elif otype == 'arbusto':
            spr2 = scale_spr(arbusto_spr, ds*TS['arbusto'])
            add_s(wy, spr2, sx, wy)
        elif otype == 'flor':
            if flores_f1:
                fi = (data or 0) % len(flores_f1)
                spr2 = scale_spr(flores_f1[fi], ds*FLOR_SCALE)
                add_s(wy, spr2, sx, wy)
        elif otype == 'alfombra_pic':
            spr2 = scale_spr(alfombra_pic, ds*TS['alfombra_pic'])
            add_s(wy, spr2, sx, wy)
        elif otype == 'canasta':
            spr2 = scale_spr(canasta, ds*TS['canasta'])
            add_s(wy, spr2, sx, wy)
        elif otype == 'floor_sitter':
            idx  = (data or 0) % len(all_seqs)
            seq2 = all_seqs[idx]
            fi2  = min(6, len(seq2)-1)
            spr2 = seq2[fi2]
            add_s(wy + 1, spr2, sx, wy - 1)
        elif otype == 'gato':
            add_s(wy, spr_map['gato'], sx, wy)
        elif otype == 'sub_persona':
            idx  = (data or 0) % len(all_seqs)
            seq2 = all_seqs[idx]
            fi2  = (t // 3) % min(5, len(seq2))
            spr2 = seq2[fi2]
            add_s(wy, spr2, sx, wy)

    # Sub-walkers animados
    for sw in sub_walkers:
        sw.update()
        sx = w2s(sw.wx)
        if -20 < sx < VW+20:
            add_s(int(sw.wy), sw.get_frame(t), sx, int(sw.wy))

    sub_items.sort(key=lambda r: r[0])
    for _,px,py,spr in sub_items:
        paste_at(sub_canvas, spr, px, py)

    # Pegar encima del canvas (los árboles quedan por encima del río)
    canvas.paste(sub_canvas, (0, 0), sub_canvas)

    t += 1
    return canvas

# ─── Tkinter ─────────────────────────────────────────────────────
root = tk.Tk()
root.title("CCPP v8  |  \u2190 \u2192 navegar   Q/ESC cerrar")
root.resizable(False,False)
root.configure(bg='#080808')

lbl = tk.Label(root, bg='#080808', bd=0)
lbl.pack(padx=0, pady=0)
bar = tk.Label(root, text="\u2190 \u2192 navegar   Q / ESC = cerrar",
               fg='#444', bg='#080808', font=('Consolas',8))
bar.pack(pady=2)

def on_press(e):
    global cam_vel
    if   e.keysym=='Right': cam_vel =  KEY_SPD
    elif e.keysym=='Left':  cam_vel = -KEY_SPD

def on_release(e):
    global cam_vel
    if e.keysym in ('Right','Left'): cam_vel = 0.0

root.bind('<KeyPress>',   on_press)
root.bind('<KeyRelease>', on_release)
root.bind('<Escape>', lambda e: root.destroy())
root.bind('<q>',      lambda e: root.destroy())
root.bind('<Q>',      lambda e: root.destroy())

tk_img = None
def update():
    global tk_img
    f   = make_frame()
    big = f.convert('RGB').resize((VW*SCALE, VH*SCALE), Image.NEAREST)
    tk_img = ImageTk.PhotoImage(big)
    lbl.config(image=tk_img)
    root.after(1000//FPS, update)

update()
root.mainloop()
