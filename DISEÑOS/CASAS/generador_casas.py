import sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
import os

BASE = r"C:\Users\memit\OneDrive - Universidad del Istmo\CCPP\DISEÑOS\CASAS"

# ==============================================================================
# CONFIGURACION — edita aqui para generar una casa
# ==============================================================================

NOMBRE_SALIDA = "CASA16"
W, H          = 48, 48
GABLE_BASE    = 17

# -- Estilo de pared -----------------------------------------------------------
# "candy"       franjas diagonales rojo/crema/azul (CASA16)
WALL_STYLE = "candy"

# -- Estilo de techo -----------------------------------------------------------
# "emerald"     tejas esmeralda brillante (CASA16)
ROOF_STYLE = "emerald"

# -- Colores de pared (madera) -------------------------------------------------
WOOD_LIGHT   = (0xDC, 0xB8, 0x80, 255)
WOOD_MID     = (0xC0, 0x98, 0x60, 255)
WOOD_DARK    = (0xA0, 0x7C, 0x48, 255)
WOOD_BATTEN  = (0x54, 0x30, 0x14, 255)
WOOD_SHADOW  = (0x68, 0x4C, 0x28, 255)
WOOD_OUTLINE = (0x28, 0x14, 0x06, 255)

# -- Colores de pared (piedra) -------------------------------------------------
STONE_LIGHT   = (0xE0, 0xCC, 0xA0, 255)
STONE_MID     = (0xC8, 0xB0, 0x84, 255)
STONE_DARK    = (0xA8, 0x90, 0x68, 255)
STONE_MORTAR  = (0x88, 0x74, 0x50, 255)
STONE_SHADOW  = (0x60, 0x50, 0x34, 255)
STONE_OUTLINE = (0x30, 0x24, 0x10, 255)

# -- Colores de pared (ladrillo rojo) ------------------------------------------
BRICK_LIGHT   = (0xCC, 0x60, 0x40, 255)  # cara superior iluminada
BRICK_MID     = (0xB0, 0x4C, 0x30, 255)  # cuerpo del ladrillo
BRICK_DARK    = (0x88, 0x38, 0x20, 255)  # sombra inferior/derecha
BRICK_MORTAR  = (0xD8, 0xC4, 0xA8, 255)  # junta beige clara
BRICK_SHADOW  = (0x60, 0x28, 0x14, 255)  # sombra profunda
BRICK_OUTLINE = (0x30, 0x14, 0x08, 255)

# -- Colores de techo (terracota) ----------------------------------------------
TILE_LIGHT   = (0xC4, 0x48, 0x24, 255)
TILE_MID     = (0xA0, 0x34, 0x18, 255)
TILE_BASE    = (0x80, 0x24, 0x10, 255)
TILE_SHADOW  = (0x50, 0x14, 0x08, 255)
TILE_EDGE    = (0x28, 0x0C, 0x04, 255)

# -- Colores de pared (lamina ondulada coral/salmon) — CASA7 ------------------
CORR_LIGHT   = (0xEC, 0xA0, 0x78, 255)  # cresta iluminada
CORR_MID     = (0xD0, 0x80, 0x58, 255)  # cuerpo
CORR_DARK    = (0xA8, 0x5C, 0x38, 255)  # valle/sombra
CORR_SEAM    = (0x80, 0x44, 0x28, 255)  # union horizontal entre paneles
CORR_OUTLINE = (0x48, 0x24, 0x10, 255)

# -- Colores de pared (bandas celeste + fucsia) — CASA10 ----------------------
CLST_LIGHT   = (0x90, 0xE0, 0xFF, 255)  # celeste iluminado
CLST_MID     = (0x50, 0xB8, 0xF0, 255)  # celeste medio
CLST_DARK    = (0x28, 0x88, 0xCC, 255)  # celeste sombra
FUCH_LIGHT   = (0xFF, 0x80, 0xD4, 255)  # fucsia iluminado
FUCH_MID     = (0xE0, 0x38, 0xA8, 255)  # fucsia medio
FUCH_DARK    = (0xB0, 0x14, 0x78, 255)  # fucsia sombra
BAND_SEP     = (0x18, 0x10, 0x40, 255)  # linea de separacion entre bandas
BAND_OUTLINE = (0x14, 0x08, 0x30, 255)  # contorno general

# -- Colores de techo fucsia brillante — CASA10 --------------------------------
FROOF_LIGHT  = (0xFF, 0x90, 0xDC, 255)
FROOF_MID    = (0xE8, 0x48, 0xBC, 255)
FROOF_DARK   = (0xC0, 0x20, 0x94, 255)
FROOF_SHADOW = (0x88, 0x08, 0x64, 255)
FROOF_EDGE   = (0x44, 0x04, 0x34, 255)

# -- Colores de pared (argyle diagonal: violeta + naranja) — CASA11 -----------
ARG_A_LIGHT  = (0xC0, 0x80, 0xFF, 255)  # violeta electrico luz
ARG_A_MID    = (0x90, 0x40, 0xE0, 255)  # violeta electrico medio
ARG_A_DARK   = (0x60, 0x18, 0xB0, 255)  # violeta electrico oscuro
ARG_B_LIGHT  = (0xFF, 0xA0, 0x40, 255)  # naranja neon luz
ARG_B_MID    = (0xF0, 0x68, 0x14, 255)  # naranja neon medio
ARG_B_DARK   = (0xC0, 0x40, 0x00, 255)  # naranja neon oscuro
ARG_SEP      = (0x14, 0x08, 0x24, 255)  # separador diagonal morado oscuro
ARG_OUTLINE  = (0x10, 0x06, 0x20, 255)  # contorno

# -- Colores de techo turquesa brillante — CASA11 ------------------------------
TURQ_LIGHT   = (0x40, 0xE4, 0xD4, 255)
TURQ_MID     = (0x18, 0xB4, 0xA0, 255)
TURQ_DARK    = (0x08, 0x80, 0x70, 255)
TURQ_SHADOW  = (0x04, 0x50, 0x44, 255)
TURQ_EDGE    = (0x02, 0x2C, 0x26, 255)

# -- Colores de pared (tartan neon: lima + magenta) — CASA12 ------------------
PLAID_A_LIGHT  = (0xA0, 0xFF, 0x20, 255)  # lima neon claro
PLAID_A_MID    = (0x70, 0xC0, 0x10, 255)  # lima neon medio
PLAID_B_LIGHT  = (0xFF, 0x20, 0x90, 255)  # magenta neon claro
PLAID_B_MID    = (0xC0, 0x10, 0x68, 255)  # magenta neon medio
PLAID_CROSS    = (0xFF, 0xFF, 0x60, 255)  # interseccion: amarillo brillante
PLAID_BG       = (0x08, 0x08, 0x28, 255)  # fondo navy oscuro
PLAID_OUTLINE  = (0x04, 0x04, 0x18, 255)  # contorno

# -- Colores de techo dorado brillante — CASA12 --------------------------------
GOLD_LIGHT   = (0xFF, 0xE0, 0x40, 255)
GOLD_MID     = (0xE8, 0xB8, 0x10, 255)
GOLD_DARK    = (0xB8, 0x88, 0x08, 255)
GOLD_SHADOW  = (0x80, 0x58, 0x04, 255)
GOLD_EDGE    = (0x40, 0x28, 0x02, 255)

# -- Colores de pared (mosaico 6 colores) — CASA13 ----------------------------
MOS_C1      = (0xFF, 0x50, 0x40, 255)  # coral
MOS_C2      = (0x20, 0x80, 0xFF, 255)  # azul electrico
MOS_C3      = (0x80, 0xFF, 0x20, 255)  # lima
MOS_C4      = (0x80, 0x20, 0xFF, 255)  # violeta
MOS_C5      = (0xFF, 0xC0, 0x10, 255)  # dorado
MOS_C6      = (0x10, 0xC0, 0xB0, 255)  # turquesa
MOS_GROUT   = (0x08, 0x08, 0x20, 255)  # junta navy oscura
MOS_OUTLINE = (0x04, 0x04, 0x10, 255)

# -- Colores de techo coral/salmon neon — CASA13 ------------------------------
CORAL_LIGHT  = (0xFF, 0x80, 0x60, 255)
CORAL_MID    = (0xFF, 0x50, 0x30, 255)
CORAL_DARK   = (0xD0, 0x30, 0x18, 255)
CORAL_SHADOW = (0x90, 0x18, 0x08, 255)
CORAL_EDGE   = (0x48, 0x0C, 0x04, 255)

# -- Colores de pared (panal hexagonal neon) — CASA14 -------------------------
HEX_C1      = (0x20, 0xFF, 0xF0, 255)  # cyan neon
HEX_C2      = (0xFF, 0xF0, 0x20, 255)  # amarillo neon
HEX_C3      = (0xFF, 0x28, 0xB8, 255)  # rosa neon
HEX_C4      = (0x40, 0xA0, 0xFF, 255)  # azul electrico
HEX_GROUT   = (0x10, 0x10, 0x18, 255)  # junta charcoal oscuro
HEX_OUTLINE = (0x08, 0x08, 0x10, 255)

# -- Colores de techo indigo profundo — CASA14 ---------------------------------
INDIGO_LIGHT  = (0x80, 0x60, 0xFF, 255)
INDIGO_MID    = (0x50, 0x30, 0xE0, 255)
INDIGO_DARK   = (0x30, 0x14, 0xA0, 255)
INDIGO_SHADOW = (0x18, 0x08, 0x60, 255)
INDIGO_EDGE   = (0x0C, 0x04, 0x30, 255)

# -- Colores de pared (circuito electronico) — CASA15 -------------------------
CIRC_BG      = (0x03, 0x10, 0x06, 255)  # fondo verde muy oscuro
CIRC_TRACE   = (0x18, 0xC0, 0x38, 255)  # traza verde neon
CIRC_PAD     = (0x70, 0xFF, 0x90, 255)  # pad brillante en interseccion
CIRC_GLOW    = (0x0A, 0x50, 0x18, 255)  # brillo tenue junto a trazas
CIRC_OUTLINE = (0x02, 0x08, 0x03, 255)

# -- Colores de techo lava glowing — CASA15 ------------------------------------
LAVA_LIGHT   = (0xFF, 0xB0, 0x20, 255)  # naranja brillante
LAVA_MID     = (0xFF, 0x58, 0x08, 255)  # naranja-rojo
LAVA_DARK    = (0xC0, 0x20, 0x04, 255)  # rojo profundo
LAVA_SHADOW  = (0x60, 0x08, 0x02, 255)  # casi negro-rojo
LAVA_EDGE    = (0x30, 0x04, 0x01, 255)

# -- Colores de pared (franjas diagonales candy) — CASA16 ----------------------
CANDY_A       = (0xFF, 0x20, 0x30, 255)  # rojo circense
CANDY_B       = (0xFF, 0xF8, 0xE0, 255)  # crema/blanco
CANDY_C       = (0x20, 0x50, 0xE8, 255)  # azul royal
CANDY_SEP     = (0x18, 0x10, 0x20, 255)  # separador oscuro
CANDY_OUTLINE = (0x10, 0x08, 0x18, 255)

# -- Colores de techo esmeralda brillante — CASA16 ----------------------------
EMLD_LIGHT   = (0x40, 0xFF, 0x80, 255)
EMLD_MID     = (0x18, 0xD0, 0x50, 255)
EMLD_DARK    = (0x08, 0x98, 0x30, 255)
EMLD_SHADOW  = (0x04, 0x58, 0x18, 255)
EMLD_EDGE    = (0x02, 0x28, 0x0C, 255)

# -- Colores de pared (escamas ambar/miel) — CASA9 ----------------------------
SCALE_LIGHT   = (0xEC, 0xC8, 0x70, 255)  # zona iluminada superior de escama
SCALE_MID     = (0xCC, 0xA0, 0x48, 255)  # cuerpo de escama
SCALE_DARK    = (0x98, 0x70, 0x28, 255)  # fondo inferior (sombra)
SCALE_SHADOW  = (0x74, 0x50, 0x18, 255)  # sombra de solapado
SCALE_OUTLINE = (0x50, 0x34, 0x0C, 255)  # borde entre escamas

# -- Colores de techo verde bosque — CASA9 ------------------------------------
FOREST_LIGHT  = (0x50, 0x84, 0x4C, 255)
FOREST_MID    = (0x38, 0x60, 0x34, 255)
FOREST_DARK   = (0x24, 0x44, 0x20, 255)
FOREST_SHADOW = (0x14, 0x2C, 0x10, 255)
FOREST_EDGE   = (0x08, 0x18, 0x08, 255)

# -- Colores de pared (madera oscura, tablones verticales) — CASA8 ------------
DWOOD_LIGHT   = (0x58, 0x40, 0x2C, 255)  # resalte de canto
DWOOD_MID     = (0x38, 0x26, 0x18, 255)  # cuerpo del tablon
DWOOD_DARK    = (0x24, 0x16, 0x0C, 255)  # sombra lateral
DWOOD_GROOVE  = (0x10, 0x08, 0x04, 255)  # ranura entre tablones
DWOOD_GRAIN   = (0x46, 0x30, 0x20, 255)  # veta de madera
DWOOD_OUTLINE = (0x0C, 0x06, 0x02, 255)

# -- Colores residuales (cblock/flat — ya no en uso activo) -------------------
CBLOCK_LIGHT   = (0xC0, 0xD8, 0xCC, 255)
CBLOCK_MID     = (0xA4, 0xBC, 0xB0, 255)
CBLOCK_DARK    = (0x84, 0x9C, 0x90, 255)
CBLOCK_MORTAR  = (0x68, 0x80, 0x74, 255)
CBLOCK_OUTLINE = (0x34, 0x48, 0x40, 255)
CBLOCK_CAP     = (0xC8, 0x64, 0x28, 255)
FLAT_LIGHT  = (0x78, 0x80, 0x74, 255)
FLAT_MID    = (0x58, 0x60, 0x58, 255)
FLAT_DARK   = (0x3C, 0x44, 0x3C, 255)
FLAT_EDGE   = (0x24, 0x2C, 0x24, 255)

# -- Colores de pared (adobe/estuco calido) — CASA5 original ------------------
ADOBE_LIGHT   = (0xD8, 0xB8, 0x88, 255)
ADOBE_MID     = (0xC0, 0xA0, 0x70, 255)
ADOBE_DARK    = (0xA0, 0x84, 0x54, 255)
ADOBE_BAND    = (0xB4, 0x94, 0x64, 255)
ADOBE_OUTLINE = (0x50, 0x38, 0x1C, 255)

# -- Colores de pared (estuco oscuro azul-gris) — CASA6 -----------------------
DSTUC_LIGHT   = (0x3C, 0x5C, 0x70, 255)  # estuco teal iluminado
DSTUC_MID     = (0x26, 0x3E, 0x50, 255)  # estuco teal base
DSTUC_DARK    = (0x18, 0x2C, 0x3A, 255)  # estuco teal sombra
DSTUC_BAND    = (0x20, 0x34, 0x44, 255)  # banda de capa
DSTUC_OUTLINE = (0x0C, 0x18, 0x24, 255)

# -- Colores de ventana postigo (shutter) --------------------------------------
SHUT_OUTLINE = (0x18, 0x0C, 0x04, 255)
SHUT_DARK    = (0x2C, 0x50, 0x24, 255)   # verde oscuro
SHUT_MID     = (0x3C, 0x68, 0x30, 255)
SHUT_LIGHT   = (0x50, 0x80, 0x40, 255)
SHUT_SLAT    = (0x24, 0x40, 0x1C, 255)   # linea de tablilla

# -- Colores de techo (teja madera shingle) ------------------------------------
SHING_LIGHT   = (0x68, 0x40, 0x1C, 255)
SHING_MID     = (0x4C, 0x2C, 0x14, 255)
SHING_DARK    = (0x34, 0x1C, 0x0C, 255)
SHING_SHADOW  = (0x20, 0x10, 0x06, 255)
SHING_EDGE    = (0x10, 0x08, 0x02, 255)

# -- Colores de pared (entramado Tudor) ----------------------------------------
PLASTER_LIGHT  = (0xF0, 0xE8, 0xD4, 255)  # revoque iluminado
PLASTER_MID    = (0xDC, 0xD0, 0xB8, 255)  # revoque base
PLASTER_DARK   = (0xC4, 0xB4, 0x98, 255)  # revoque sombra
BEAM_LIGHT     = (0x54, 0x30, 0x10, 255)  # viga iluminada
BEAM_MID       = (0x38, 0x1C, 0x08, 255)  # viga base
BEAM_DARK      = (0x20, 0x10, 0x04, 255)  # viga sombra
BEAM_OUTLINE   = (0x10, 0x06, 0x02, 255)  # contorno

# -- Colores de techo (pizarra azul-gris) --------------------------------------
SLATE_LIGHT  = (0x88, 0x9C, 0xB4, 255)  # borde superior de cada pizarra
SLATE_MID    = (0x5C, 0x74, 0x8C, 255)  # cuerpo
SLATE_DARK   = (0x3C, 0x54, 0x6C, 255)  # sombra inferior
SLATE_SHADOW = (0x28, 0x3C, 0x50, 255)  # junta entre pizarras
SLATE_EDGE   = (0x14, 0x24, 0x34, 255)  # contorno

# -- Colores de techo (cobre patinado) -----------------------------------------
COPPER_LIGHT  = (0x68, 0xB4, 0x7C, 255)  # patina verde clara
COPPER_MID    = (0x48, 0x8C, 0x5C, 255)  # cuerpo verde
COPPER_DARK   = (0x30, 0x64, 0x40, 255)  # sombra verde oscura
COPPER_SHADOW = (0x1C, 0x44, 0x2C, 255)  # junta profunda
COPPER_EDGE   = (0x10, 0x28, 0x18, 255)  # contorno

# -- Colores de puerta ---------------------------------------------------------
DOOR_OUTLINE = (0x20, 0x10, 0x04, 255)
DOOR_DARK    = (0x3C, 0x1C, 0x08, 255)
DOOR_BASE    = (0x5C, 0x30, 0x14, 255)
DOOR_MID     = (0x78, 0x46, 0x20, 255)
DOOR_LIGHT   = (0x94, 0x5C, 0x2C, 255)
DOOR_HANDLE  = (0xD0, 0xA8, 0x30, 255)

# -- Colores de ventana --------------------------------------------------------
WIN_OUTLINE  = (0x14, 0x0A, 0x02, 255)   # negro profundo
WIN_MOLDING  = (0xE0, 0xCC, 0xA0, 255)   # crema claro — contrasta bien con ladrillo
WIN_MOLDING2 = (0xB8, 0xA0, 0x70, 255)   # crema medio
WIN_LINTEL   = (0xF0, 0xDC, 0xB0, 255)   # banda superior mas clara
WIN_FRAME    = (0x5C, 0x38, 0x14, 255)   # armazon interior oscuro
WIN_SILL_L   = (0xE8, 0xD0, 0xA0, 255)   # cara superior del alfeizar (clara)
WIN_SILL_D   = (0xA8, 0x88, 0x50, 255)   # frente del alfeizar (oscura)
WIN_GLASS1   = (0xB0, 0xE0, 0xF4, 255)
WIN_GLASS2   = (0x84, 0xC4, 0xE4, 255)
WIN_GLASS3   = (0x50, 0x98, 0xC4, 255)
WIN_REFL     = (0xDC, 0xF4, 0xFF, 255)


# ==============================================================================
# LOGICA DE PARED
# ==============================================================================

def wood_h(x, y, wy0):
    row = y - wy0; board = row // 6; local = row % 6
    if local == 0: return WOOD_SHADOW
    if local == 1: return WOOD_DARK
    if local == 5: return WOOD_LIGHT
    g = (x + board) % 10
    if g == 0: return WOOD_DARK
    if g == 5: return (0xCC, 0xA8, 0x6C, 255)
    return WOOD_MID

def wood_v(x, y, wx0):
    col = x - wx0; unit = col % 6; board = col // 6
    if unit == 0: return WOOD_SHADOW
    if unit == 1: return WOOD_BATTEN
    if unit == 2: return WOOD_LIGHT
    if unit == 5: return WOOD_DARK
    g = (y + board * 4) % 13
    if g in (0,1): return WOOD_DARK
    if g in (6,7): return WOOD_LIGHT
    return WOOD_MID

def stone_pixel(x, y, x0, y0):
    row = (y-y0)//6; loc_y = (y-y0)%6
    offset = (row%2)*5; loc_x = (x-x0+offset)%10
    if loc_y == 0: return STONE_SHADOW
    if loc_x == 0: return STONE_MORTAR
    if loc_y == 1: return STONE_LIGHT
    if loc_y == 5: return STONE_DARK
    if loc_x == 1: return STONE_LIGHT
    if loc_x == 9: return STONE_DARK
    t = (x*5 + y*7 + row*11) % 19
    if t < 2: return STONE_DARK
    if t < 4: return STONE_LIGHT
    return STONE_MID

def brick_pixel(x, y, x0, y0):
    """
    Ladrillo rojo clasico: 9px ancho x 5px alto (8px ladrillo + 1px mortero).
    Hiladas alternas con offset de 4px.
    """
    row_h  = 5
    blk_w  = 9
    row    = (y - y0) // row_h
    loc_y  = (y - y0) % row_h
    offset = (row % 2) * 4
    loc_x  = (x - x0 + offset) % blk_w

    if loc_y == 0: return BRICK_MORTAR    # junta horizontal
    if loc_x == 0: return BRICK_SHADOW    # junta vertical (sombra)
    if loc_y == 1: return BRICK_LIGHT     # borde superior (iluminado)
    if loc_y == row_h-1: return BRICK_DARK  # borde inferior (sombra)
    if loc_x == 1: return BRICK_LIGHT
    if loc_x == blk_w-1: return BRICK_DARK
    # Veta sutil en el cuerpo
    t = (x*3 + y*5 + row*7) % 17
    if t < 2: return BRICK_DARK
    if t < 4: return BRICK_LIGHT
    return BRICK_MID

def adobe_pixel(x, y, x0, y0):
    ly = (y - y0) % 8
    if ly == 0: return ADOBE_BAND
    if ly == 1: return ADOBE_DARK
    t = (x * 13 + y * 7) % 29
    if t < 3:  return ADOBE_DARK
    if t < 7:  return ADOBE_LIGHT
    return ADOBE_MID

def colorband_pixel(x, y, x0, y0):
    """
    Bandas horizontales alternadas: 5px celeste + 5px fucsia (ciclo 10px).
    Cada banda tiene: linea de sombra en la parte alta, highlight, cuerpo.
    """
    row = (y - y0) % 10
    if row == 0:   return BAND_SEP      # linea separadora
    if row < 5:                          # banda CELESTE
        if row == 1: return CLST_LIGHT
        if row == 4: return CLST_DARK
        return CLST_MID
    if row == 5:   return BAND_SEP      # linea separadora
                                         # banda FUCSIA
    if row == 6: return FUCH_LIGHT
    if row == 9: return FUCH_DARK
    return FUCH_MID

def candy_pixel(x, y, x0, y0):
    """
    Franjas diagonales a 45° estilo circense: rojo / crema / azul.
    Cada franja mide 6px, ciclo de 18px total.
    Borde oscuro al inicio, highlight al inicio+1, sombra al final.
    """
    d   = (x - x0) + (y - y0)
    pos = d % 18

    def shade(base, hi=False, lo=False):
        r,g,b,a = base
        if hi: return (min(255,r+40), min(255,g+40), min(255,b+40), a)
        if lo: return (max(0,r-45),  max(0,g-45),  max(0,b-45),  a)
        return base

    if pos == 0 or pos == 6 or pos == 12:
        return CANDY_SEP
    if pos < 6:
        return shade(CANDY_A, hi=(pos==1), lo=(pos==5))
    if pos < 12:
        return shade(CANDY_B, hi=(pos==7), lo=(pos==11))
    return shade(CANDY_C, hi=(pos==13), lo=(pos==17))

def circuit_pixel(x, y, x0, y0):
    """
    Placa de circuito electronico: trazas horizontales (periodo 8px)
    y verticales (2 trazas por periodo 11px). Pads en intersecciones.
    """
    px = x - x0; py = y - y0
    hy = py % 8     # posicion dentro del periodo vertical
    vx = px % 11    # posicion dentro del periodo horizontal
    h_on = hy == 0                   # traza horizontal
    v_on = vx == 0 or vx == 6       # 2 trazas verticales por periodo
    if h_on and v_on: return CIRC_PAD
    if h_on:          return CIRC_TRACE
    if v_on:          return CIRC_TRACE
    # Brillo sutil junto a las trazas
    if hy in (1, 7) and (vx in (1, 7)): return CIRC_GLOW
    return CIRC_BG

def hex_pixel(x, y, x0, y0):
    """
    Panal hexagonal: celdas de 6×4px con esquinas cortadas.
    Filas alternas desplazadas 3px. 4 colores neon rotando por celda.
    Bordes sup/izq claros, inf/der oscuros.
    """
    px  = x - x0; py = y - y0
    row = py // 4; ly = py % 4
    off = (row % 2) * 3
    lx  = (px + off) % 6
    hx  = (px + off) // 6
    # Esquinas y bordes → junta
    if lx == 0 or lx == 5 or ly == 0 or ly == 3: return HEX_GROUT
    # Interior — color por posicion de celda
    idx  = (hx * 2 + row * 3 + hx * row) % 4
    base = (HEX_C1, HEX_C2, HEX_C3, HEX_C4)[idx]
    r, g, b, a = base
    if lx == 1 or ly == 1:  # borde superior/izq iluminado
        return (min(255,r+35), min(255,g+35), min(255,b+35), a)
    if lx == 4 or ly == 2:  # borde inferior/der en sombra
        return (max(0,r-50), max(0,g-50), max(0,b-50), a)
    return base

def mosaic_pixel(x, y, x0, y0):
    """
    Mosaico de teselas 5px (4px color + 1px junta).
    6 colores vividos asignados por posicion de tesela con variacion.
    Bordes superiores/izquierdos claros, inferiores/derechos oscuros.
    """
    tx = (x - x0) % 5
    ty = (y - y0) % 5
    if tx == 0 or ty == 0: return MOS_GROUT
    lx = tx - 1; ly = ty - 1       # 0..3 dentro de la tesela
    tile_x = (x - x0) // 5
    tile_y = (y - y0) // 5
    idx = (tile_x * 3 + tile_y * 7 + tile_x * tile_y * 2) % 6
    base = (MOS_C1, MOS_C2, MOS_C3, MOS_C4, MOS_C5, MOS_C6)[idx]
    r, g, b, a = base
    if lx == 0 or ly == 0:
        return (min(255,r+40), min(255,g+40), min(255,b+40), a)
    if lx == 3 or ly == 3:
        return (max(0,r-50), max(0,g-50), max(0,b-50), a)
    return base

def plaid_pixel(x, y, x0, y0):
    """
    Tartán neon: rayas verticales lima + rayas horizontales magenta
    sobre fondo navy. Intersecciones = amarillo brillante.
    Ciclo 6px: 2px de raya + 4px de fondo.
    """
    cx = (x - x0) % 6
    cy = (y - y0) % 6
    v = cx < 2    # vertical lima
    h = cy < 2    # horizontal magenta
    if v and h:   return PLAID_CROSS
    if v:         return PLAID_A_LIGHT if cx == 0 else PLAID_A_MID
    if h:         return PLAID_B_LIGHT if cy == 0 else PLAID_B_MID
    return PLAID_BG

def argyle_pixel(x, y, x0, y0):
    """
    Diagonales a 45° alternando violeta electrico y naranja neon.
    Ciclo de 8px: 4px violeta / 4px naranja con separador diagonal.
    """
    d = ((x - x0) + (y - y0)) % 8
    if d == 0: return ARG_SEP
    if d < 4:
        if d == 1: return ARG_A_LIGHT
        if d == 3: return ARG_A_DARK
        return ARG_A_MID
    if d == 4: return ARG_SEP
    if d == 5: return ARG_B_LIGHT
    if d == 7: return ARG_B_DARK
    return ARG_B_MID

def fishscale_pixel(x, y, x0, y0):
    """
    Escamas superpuestas (fish scale shingles): filas de 4px alto,
    escamas de 6px ancho, hiladas alternas con offset de 3px.
    ly=0: sombra de solapado, ly=1: luz, ly=2: medio, ly=3: oscuro/punta.
    """
    px  = x - x0
    py  = y - y0
    row = py // 4
    ly  = py % 4
    off = (row % 2) * 3          # offset alternado de media escama
    lx  = (px + off) % 6        # posicion dentro de la escama (0-5)

    # Ranura vertical entre escamas
    if lx == 0: return SCALE_OUTLINE

    # La punta inferior del arco se estrecha: solo lx 2-3 en ly=3
    if ly == 3 and lx in (1, 5): return SCALE_OUTLINE

    # Color segun posicion vertical dentro de la escama
    if ly == 0: return SCALE_SHADOW   # bajo el solapado de la escama superior
    if ly == 1:                        # zona iluminada
        return SCALE_LIGHT if lx in (2, 3) else SCALE_MID
    if ly == 2:                        # cuerpo
        if lx in (1, 5): return SCALE_SHADOW
        # Variacion sutil por numero de escama
        t = ((px + off) // 6 + row * 3) % 5
        return SCALE_LIGHT if t == 0 else SCALE_MID
    # ly == 3: punta del arco, color oscuro
    return SCALE_DARK

def darkwood_pixel(x, y, x0, y0):
    """
    Tablones verticales oscuros de calidad — 6px ancho.
    Cada tablon tiene: ranura, canto iluminado, veta horizontal
    desplazada por numero de tablon, sombra derecha.
    """
    col = (x - x0) % 6
    plk = (x - x0) // 6          # numero de tablon (veta desplazada)

    if col == 0: return DWOOD_GROOVE   # ranura profunda entre tablones
    if col == 1: return DWOOD_LIGHT    # canto izq iluminado
    if col == 5: return DWOOD_DARK     # canto der en sombra

    # Veta horizontal: patron de 11px desplazado por tablon
    gy = (y - y0 + plk * 3) % 11
    if gy == 0:            return DWOOD_GROOVE  # veta oscura intensa
    if gy in (1, 10):      return DWOOD_DARK    # borde de veta
    if gy in (5, 6):       return DWOOD_GRAIN   # reflejo claro de veta

    # Micro-textura de fondo
    t = (x * 5 + y * 3 + plk * 7) % 17
    if t < 2:  return DWOOD_DARK
    if t < 4:  return DWOOD_GRAIN
    return DWOOD_MID

def corrugated_pixel(x, y, x0, y0):
    """
    Lamina ondulada (corrugated metal): ondas verticales cada 4px
    + juntas horizontales cada 10px simulando paneles.
    """
    wave  = (x - x0) % 4      # 0=cresta, 1=bajada, 2=valle, 3=subida
    panel = (y - y0) % 10     # junta horizontal cada 10px
    if panel == 0: return CORR_SEAM
    if wave == 0:  return CORR_LIGHT
    if wave == 2:  return CORR_DARK
    return CORR_MID

def cblock_pixel(x, y, x0, y0):
    """
    Bloque de concreto: 12px ancho x 6px alto (5 cuerpo + 1 mortero).
    Hiladas alternas con offset de 6px. Color mint centroamericano.
    """
    row   = (y - y0) // 6
    loc_y = (y - y0) % 6
    offset = (row % 2) * 6
    loc_x  = (x - x0 + offset) % 12
    if loc_y == 0:   return CBLOCK_MORTAR   # junta horizontal
    if loc_x == 0:   return CBLOCK_MORTAR   # junta vertical
    if loc_y == 1:   return CBLOCK_LIGHT    # cara superior iluminada
    if loc_y == 5:   return CBLOCK_DARK     # sombra inferior
    if loc_x == 1:   return CBLOCK_LIGHT
    if loc_x == 11:  return CBLOCK_DARK
    t = (x * 7 + y * 11 + row * 5) % 19
    if t < 2: return CBLOCK_DARK
    if t < 4: return CBLOCK_LIGHT
    return CBLOCK_MID

def dark_stucco_pixel(x, y, x0, y0):
    """
    Estuco oscuro azul-gris: misma estructura de capas que adobe
    pero en paleta fria teal/navy.
    """
    ly = (y - y0) % 8
    if ly == 0: return DSTUC_BAND
    if ly == 1: return DSTUC_DARK
    t = (x * 13 + y * 7) % 29
    if t < 3:  return DSTUC_DARK
    if t < 7:  return DSTUC_LIGHT
    return DSTUC_MID

def timber_pixel(x, y, x0, y0):
    """
    Entramado Tudor: cuadricula de vigas oscuras (cada 12px) con
    revoque claro entre ellas. Viga de 2px ancho.
    """
    lx = (x - x0) % 12
    ly = (y - y0) % 12
    on_v = lx <= 1
    on_h = ly == 0
    if on_v or on_h:
        if lx == 0 or ly == 0: return BEAM_DARK
        if on_v:                return BEAM_MID
        return BEAM_LIGHT
    # Revoque con textura sutil
    t = (x * 7 + y * 11) % 23
    if t < 2:  return PLASTER_DARK
    if t < 5:  return PLASTER_LIGHT
    return PLASTER_MID

def wall_pixel(x, y, x0, y0):
    if WALL_STYLE == "vertical": return wood_v(x, y, x0+1)
    if WALL_STYLE == "stone":    return stone_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "brick":    return brick_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "timber":   return timber_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "adobe":        return adobe_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "dark_stucco":  return dark_stucco_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "cblock":       return cblock_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "corrugated":   return corrugated_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "darkwood":     return darkwood_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "fishscale":    return fishscale_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "colorband":    return colorband_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "argyle":       return argyle_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "plaid":        return plaid_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "mosaic":       return mosaic_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "hex":          return hex_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "circuit":      return circuit_pixel(x, y, x0+1, y0+1)
    if WALL_STYLE == "candy":        return candy_pixel(x, y, x0+1, y0+1)
    return wood_h(x, y, y0+1)

def _wall_outline():
    if WALL_STYLE == "stone":        return STONE_OUTLINE
    if WALL_STYLE == "brick":        return BRICK_OUTLINE
    if WALL_STYLE == "timber":       return BEAM_OUTLINE
    if WALL_STYLE == "adobe":        return ADOBE_OUTLINE
    if WALL_STYLE == "dark_stucco":  return DSTUC_OUTLINE
    if WALL_STYLE == "cblock":       return CBLOCK_OUTLINE
    if WALL_STYLE == "corrugated":   return CORR_OUTLINE
    if WALL_STYLE == "darkwood":     return DWOOD_OUTLINE
    if WALL_STYLE == "fishscale":    return SCALE_OUTLINE
    if WALL_STYLE == "colorband":    return BAND_OUTLINE
    if WALL_STYLE == "argyle":       return ARG_OUTLINE
    if WALL_STYLE == "plaid":        return PLAID_OUTLINE
    if WALL_STYLE == "mosaic":       return MOS_OUTLINE
    if WALL_STYLE == "hex":          return HEX_OUTLINE
    if WALL_STYLE == "circuit":      return CIRC_OUTLINE
    if WALL_STYLE == "candy":        return CANDY_OUTLINE
    return WOOD_OUTLINE

def draw_wall(img, x0, y0, x1, y1):
    outline = _wall_outline()
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            if x==x0 or x==x1 or y==y0 or y==y1:
                img.putpixel((x,y), outline)
            else:
                img.putpixel((x,y), wall_pixel(x,y,x0,y0))


# ==============================================================================
# TECHO
# ==============================================================================

def _roof_color(x, y):
    if ROOF_STYLE == "slate":
        row    = y // 4
        offset = (row % 2) * 3
        lx     = (x + offset) % 6
        ly     = y % 4
        if lx == 0:  return SLATE_EDGE
        if ly == 0:  return SLATE_SHADOW
        if ly == 1:  return SLATE_LIGHT
        if ly == 2:  return SLATE_MID
        return SLATE_DARK
    elif ROOF_STYLE == "shingle":
        # Tejas de madera: filas de 5px alto, cada teja 8px ancho, alternadas
        row    = y // 5
        offset = (row % 2) * 4
        lx     = (x + offset) % 8
        ly     = y % 5
        if lx == 0:  return SHING_SHADOW   # junta vertical entre tejas
        if ly == 0:  return SHING_SHADOW   # borde superior solapado
        if ly == 1:  return SHING_LIGHT    # borde superior iluminado
        if ly == 4:  return SHING_DARK     # borde inferior (sombra)
        if lx >= 6:  return SHING_DARK
        t = (row * 5 + (x // 8) * 3) % 9
        if t < 2:  return SHING_DARK
        if t < 4:  return SHING_LIGHT
        return SHING_MID
    elif ROOF_STYLE == "copper":
        # Paneles de cobre: 8px ancho x 5px alto, con nervios verticales
        row    = y // 5
        lx     = x % 8
        ly     = y % 5
        if lx == 0:                return COPPER_SHADOW  # nervio vertical
        if lx == 1:                return COPPER_DARK
        if ly == 0:                return COPPER_SHADOW  # nervio horizontal
        if ly == 1:                return COPPER_LIGHT
        if lx >= 6:                return COPPER_DARK
        # Variacion de patina por panel
        t = (row * 3 + (x // 8) * 5) % 7
        if t < 2:  return COPPER_LIGHT
        if t < 4:  return COPPER_MID
        return COPPER_DARK
    elif ROOF_STYLE == "fuchsia":
        row    = y // 4
        offset = (row % 2) * 3
        lx     = (x + offset) % 6
        ly     = y % 4
        if lx == 0:  return FROOF_EDGE
        if ly == 0:  return FROOF_SHADOW
        if ly == 1:  return FROOF_LIGHT
        if ly == 2:  return FROOF_MID
        return FROOF_DARK
    elif ROOF_STYLE == "forest":
        row    = y // 4
        offset = (row % 2) * 3
        lx     = (x + offset) % 6
        ly     = y % 4
        if lx == 0:  return FOREST_EDGE
        if ly == 0:  return FOREST_SHADOW
        if ly == 1:  return FOREST_LIGHT
        if ly == 2:  return FOREST_MID
        return FOREST_DARK
    elif ROOF_STYLE == "turquoise":
        row    = y // 4
        offset = (row % 2) * 3
        lx     = (x + offset) % 6
        ly     = y % 4
        if lx == 0:  return TURQ_EDGE
        if ly == 0:  return TURQ_SHADOW
        if ly == 1:  return TURQ_LIGHT
        if ly == 2:  return TURQ_MID
        return TURQ_DARK
    elif ROOF_STYLE == "gold":
        row    = y // 4
        offset = (row % 2) * 3
        lx     = (x + offset) % 6
        ly     = y % 4
        if lx == 0:  return GOLD_EDGE
        if ly == 0:  return GOLD_SHADOW
        if ly == 1:  return GOLD_LIGHT
        if ly == 2:  return GOLD_MID
        return GOLD_DARK
    elif ROOF_STYLE == "coral":
        row    = y // 4
        offset = (row % 2) * 3
        lx     = (x + offset) % 6
        ly     = y % 4
        if lx == 0:  return CORAL_EDGE
        if ly == 0:  return CORAL_SHADOW
        if ly == 1:  return CORAL_LIGHT
        if ly == 2:  return CORAL_MID
        return CORAL_DARK
    elif ROOF_STYLE == "indigo":
        row    = y // 4
        offset = (row % 2) * 3
        lx     = (x + offset) % 6
        ly     = y % 4
        if lx == 0:  return INDIGO_EDGE
        if ly == 0:  return INDIGO_SHADOW
        if ly == 1:  return INDIGO_LIGHT
        if ly == 2:  return INDIGO_MID
        return INDIGO_DARK
    elif ROOF_STYLE == "lava":
        row    = y // 4
        offset = (row % 2) * 3
        lx     = (x + offset) % 6
        ly     = y % 4
        if lx == 0:  return LAVA_EDGE
        if ly == 0:  return LAVA_SHADOW
        if ly == 1:  return LAVA_LIGHT
        if ly == 2:  return LAVA_MID
        return LAVA_DARK
    elif ROOF_STYLE == "emerald":
        row    = y // 4
        offset = (row % 2) * 3
        lx     = (x + offset) % 6
        ly     = y % 4
        if lx == 0:  return EMLD_EDGE
        if ly == 0:  return EMLD_SHADOW
        if ly == 1:  return EMLD_LIGHT
        if ly == 2:  return EMLD_MID
        return EMLD_DARK
    else:  # terracota
        row    = y // 4
        offset = (row % 2) * 3
        lx     = (x + offset) % 6
        ly     = y % 4
        if lx == 0:  return TILE_EDGE
        if ly == 0:  return TILE_SHADOW
        if ly == 1:  return TILE_LIGHT
        if ly == 2:  return TILE_MID
        return TILE_BASE

def _flat_roof_pixel(x, y):
    """Techo plano: textura de grava suelta (ruido controlado)."""
    t = (x * 13 + y * 7 + (x^y) * 3) % 31
    if t < 4:  return FLAT_LIGHT
    if t < 10: return FLAT_DARK
    return FLAT_MID

def draw_parapet(img, height=5):
    """
    Pretil (parapet) para techo plano: banda de bloques en la parte
    superior del frame con tira de acento de color.
    """
    # Tira de acento (cap) — 2px
    for x in range(W):
        img.putpixel((x, 0), CBLOCK_OUTLINE)
        img.putpixel((x, 1), CBLOCK_CAP)
    # Cuerpo del pretil — misma pared
    for y in range(2, height):
        for x in range(W):
            if x == 0 or x == W-1:
                img.putpixel((x, y), CBLOCK_OUTLINE)
            else:
                img.putpixel((x, y), cblock_pixel(x, y, 1, 2))

def _roof_edge():
    if ROOF_STYLE == "slate":   return SLATE_EDGE
    if ROOF_STYLE == "copper":  return COPPER_EDGE
    if ROOF_STYLE == "shingle": return SHING_EDGE
    if ROOF_STYLE == "flat":    return FLAT_EDGE
    if ROOF_STYLE == "forest":  return FOREST_EDGE
    if ROOF_STYLE == "fuchsia":    return FROOF_EDGE
    if ROOF_STYLE == "turquoise":  return TURQ_EDGE
    if ROOF_STYLE == "gold":       return GOLD_EDGE
    if ROOF_STYLE == "coral":      return CORAL_EDGE
    if ROOF_STYLE == "indigo":     return INDIGO_EDGE
    if ROOF_STYLE == "lava":       return LAVA_EDGE
    if ROOF_STYLE == "emerald":    return EMLD_EDGE
    return TILE_EDGE

def _roof_shadow():
    if ROOF_STYLE == "slate":   return SLATE_SHADOW
    if ROOF_STYLE == "copper":  return COPPER_SHADOW
    if ROOF_STYLE == "shingle": return SHING_SHADOW
    if ROOF_STYLE == "forest":  return FOREST_SHADOW
    if ROOF_STYLE == "fuchsia":    return FROOF_SHADOW
    if ROOF_STYLE == "turquoise":  return TURQ_SHADOW
    if ROOF_STYLE == "gold":       return GOLD_SHADOW
    if ROOF_STYLE == "coral":      return CORAL_SHADOW
    if ROOF_STYLE == "indigo":     return INDIGO_SHADOW
    if ROOF_STYLE == "lava":       return LAVA_SHADOW
    if ROOF_STYLE == "emerald":    return EMLD_SHADOW
    return TILE_SHADOW

def draw_gable(img, base_y):
    peak_y = 1; span = base_y - peak_y
    cx_l = W//2 - 2; cx_r = W//2 + 1
    for y in range(0, base_y+1):
        if y < peak_y: continue
        t  = (y-peak_y)/span
        lx = round(cx_l - t*cx_l)
        rx = round(cx_r + t*(W-1-cx_r))
        for x in range(W):
            if x < lx or x > rx:
                img.putpixel((x,y), (0,0,0,0)); continue
            # La fila base del gable usa el outline de la pared
            # para que el techo y la fachada compartan el mismo borde
            if y == base_y:
                img.putpixel((x,y), _wall_outline())
            elif x==lx or x==rx:
                img.putpixel((x,y), _roof_edge())
            elif x==lx+1 or x==rx-1:
                img.putpixel((x,y), _roof_shadow())
            else:
                img.putpixel((x,y), _roof_color(x,y))


# ==============================================================================
# RELOJ DE TORRE (para gable)
# ==============================================================================

def draw_clock(img, cx, cy, r):
    """Reloj de torre pixel art dentro del gable. Marca las 10:10 (clasico)."""
    import math
    FACE    = (0xF4, 0xEC, 0xD0, 255)   # esfera crema
    RIM     = (0xC4, 0x94, 0x3C, 255)   # aro dorado
    OUTLINE = (0x14, 0x08, 0x02, 255)   # contorno
    HAND    = (0x14, 0x08, 0x02, 255)   # manecillas
    MARK    = (0x40, 0x24, 0x0C, 255)   # marcas de hora

    # Circulo: esfera, aro, contorno
    for dy in range(-r-1, r+2):
        for dx in range(-r-1, r+2):
            d = (dx*dx + dy*dy) ** 0.5
            px, py = cx+dx, cy+dy
            if not (0 <= px < W and 0 <= py < H): continue
            if d <= r-2:   img.putpixel((px,py), FACE)
            elif d <= r:   img.putpixel((px,py), RIM)
            elif d <= r+0.6: img.putpixel((px,py), OUTLINE)

    # Marcas de hora en 12, 3, 6, 9
    for a in [0, 90, 180, 270]:
        rad = math.radians(a - 90)
        mx = cx + round(math.cos(rad) * (r-2))
        my = cy + round(math.sin(rad) * (r-2))
        if 0 <= mx < W and 0 <= my < H:
            img.putpixel((mx, my), MARK)

    # Manecilla de hora → 10 en punto (−60° desde arriba)
    h_ang = math.radians(-60 - 90)
    for t in range(1, r-2):
        hx = cx + round(math.cos(h_ang) * t)
        hy = cy + round(math.sin(h_ang) * t)
        if 0 <= hx < W and 0 <= hy < H:
            img.putpixel((hx, hy), HAND)

    # Manecilla de minutos → 2 en punto (+60° desde arriba)
    m_ang = math.radians(60 - 90)
    for t in range(1, r-1):
        mx = cx + round(math.cos(m_ang) * t)
        my = cy + round(math.sin(m_ang) * t)
        if 0 <= mx < W and 0 <= my < H:
            img.putpixel((mx, my), HAND)

    # Punto central
    img.putpixel((cx, cy), HAND)


# ==============================================================================
# VENTANAS
# ==============================================================================

def draw_window(img, x0, y0, x1, y1, style="4panes", header=False):
    """
    header=True → dibuja friso decorativo encima (lineas V+H),
                  moldura de 2 capas en la ventana (mas limpia).
    header=False → moldura de 3 capas + lintel clasico.
    """
    # ── Franja horizontal (moderna, sin moldura, solo outline fino) ───────────
    if style == "strip":
        for y in range(y0, y1+1):
            for x in range(x0, x1+1):
                on_edge = x==x0 or x==x1 or y==y0 or y==y1
                if on_edge:
                    img.putpixel((x,y), WIN_OUTLINE)
                else:
                    iw = x1-x0-1; ih = y1-y0-1
                    tx = (x-x0-1)/max(iw-1,1)
                    ty = (y-y0-1)/max(ih-1,1)
                    t  = tx*0.6 + ty*0.4
                    c  = WIN_REFL if t<0.15 else WIN_GLASS1 if t<0.4 else WIN_GLASS2 if t<0.7 else WIN_GLASS3
                    img.putpixel((x,y), c)
        return

    # ── Arco escalonado (pirámide arriba de la ventana, estilo CASA6) ─────────
    if style == "arch":
        steps = 4
        for s in range(steps):
            sy0 = max(0, y0 - (s+1)*2)
            sy1 = y0 - s*2 - 1
            sx0 = x0 + s*2
            sx1 = x1 - s*2
            if sx1 <= sx0 or sy1 < sy0: break
            for y in range(sy0, sy1+1):
                for x in range(sx0, sx1+1):
                    on_edge = x==sx0 or x==sx1 or y==sy0
                    if on_edge:
                        img.putpixel((x,y), WIN_OUTLINE)
                    elif s == steps-1:        # bloque clave (keystone) arriba
                        img.putpixel((x,y), WIN_LINTEL)
                    elif y == sy1:
                        img.putpixel((x,y), WIN_MOLDING2)
                    else:
                        img.putpixel((x,y), WIN_MOLDING)
        # Ventana: solo 1 capa outline + cristal simple
        for y in range(y0, y1+1):
            for x in range(x0, x1+1):
                d = min(x-x0, x1-x, y-y0, y1-y)
                if d == 0: img.putpixel((x,y), WIN_OUTLINE)
                elif d == 1: img.putpixel((x,y), WIN_MOLDING)
        ix0,iy0,ix1,iy1 = x0+2,y0+2,x1-2,y1-2
        if ix1 > ix0 and iy1 > iy0:
            iw=ix1-ix0+1; ih=iy1-iy0+1
            for y in range(iy0,iy1+1):
                for x in range(ix0,ix1+1):
                    if x in(ix0,ix1) or y in(iy0,iy1):
                        img.putpixel((x,y),WIN_FRAME); continue
                    dw=max(iw-1,1); dh=max(ih-1,1)
                    t=((x-ix0)/dw+(y-iy0)/dh)/2
                    c=WIN_REFL if t<0.2 else WIN_GLASS1 if t<0.5 else WIN_GLASS2 if t<0.75 else WIN_GLASS3
                    img.putpixel((x,y),c)
        return

    # ── Jalousie (persianas verticales — lamas cada 3px) ─────────────────────
    if style == "jalousie":
        if header:
            hh=6; hx0=max(0,x0-1); hx1=min(W-1,x1+1); hy0=max(0,y0-hh); hy1=y0-1
            if hy1 > hy0:
                for y in range(hy0, hy1+1):
                    for x in range(hx0, hx1+1):
                        on_edge = x==hx0 or x==hx1 or y==hy0 or y==hy1
                        if on_edge:                       img.putpixel((x,y), WIN_OUTLINE)
                        elif y == hy0+1 or y == hy1-1:   img.putpixel((x,y), WIN_MOLDING)
                        elif (x-hx0) % 3 == 1:           img.putpixel((x,y), WIN_MOLDING2)
                        else:                             img.putpixel((x,y), WIN_LINTEL)
        layers = 2 if header else 3
        for y in range(y0, y1+1):
            for x in range(x0, x1+1):
                d = min(x-x0, x1-x, y-y0, y1-y)
                if d == 0:               img.putpixel((x,y), WIN_OUTLINE)
                elif d == 1:             img.putpixel((x,y), WIN_MOLDING)
                elif d==2 and layers==3: img.putpixel((x,y), WIN_MOLDING2)
        if not header:
            for x in range(x0+2, x1-1): img.putpixel((x, y0+1), WIN_LINTEL)
        off = layers
        ix0, iy0, ix1, iy1 = x0+off, y0+off, x1-off, y1-off
        if ix1 > ix0 and iy1 > iy0:
            for y in range(iy0, iy1+1):
                for x in range(ix0, ix1+1):
                    on_b = x in (ix0, ix1) or y in (iy0, iy1)
                    if on_b:
                        img.putpixel((x,y), WIN_FRAME)
                    else:
                        sl = (x - ix0) % 3         # lamas VERTICALES
                        if sl == 0:   img.putpixel((x,y), WIN_FRAME)
                        elif sl == 1: img.putpixel((x,y), WIN_GLASS1)
                        else:         img.putpixel((x,y), WIN_GLASS3)
        if y1+6 <= H-1:
            sx0=max(0,x0-2); sx1=min(W-1,x1+2)
            for sy in range(y1+1, y1+6):
                for sx in range(sx0, sx1+1):
                    e = sx==sx0 or sx==sx1 or sy==y1+1 or sy==y1+5
                    img.putpixel((sx,sy), WIN_OUTLINE if e else WIN_SILL_L if sy in(y1+2,y1+3) else WIN_SILL_D)
        return

    # ── Triple (3 paneles verticales con separadores de 2px) ─────────────────
    if style == "triple":
        if header:
            hh=6; hx0=max(0,x0-1); hx1=min(W-1,x1+1); hy0=max(0,y0-hh); hy1=y0-1
            if hy1 > hy0:
                for y in range(hy0, hy1+1):
                    for x in range(hx0, hx1+1):
                        on_edge = x==hx0 or x==hx1 or y==hy0 or y==hy1
                        if on_edge:                       img.putpixel((x,y), WIN_OUTLINE)
                        elif y == hy0+1 or y == hy1-1:   img.putpixel((x,y), WIN_MOLDING)
                        elif (x-hx0) % 3 == 1:           img.putpixel((x,y), WIN_MOLDING2)
                        else:                             img.putpixel((x,y), WIN_LINTEL)
        layers = 2 if header else 3
        for y in range(y0, y1+1):
            for x in range(x0, x1+1):
                d = min(x-x0, x1-x, y-y0, y1-y)
                if d == 0:               img.putpixel((x,y), WIN_OUTLINE)
                elif d == 1:             img.putpixel((x,y), WIN_MOLDING)
                elif d==2 and layers==3: img.putpixel((x,y), WIN_MOLDING2)
        if not header:
            for x in range(x0+2, x1-1): img.putpixel((x, y0+1), WIN_LINTEL)
        off = layers
        ix0, iy0, ix1, iy1 = x0+off, y0+off, x1-off, y1-off
        if ix1 > ix0 and iy1 > iy0:
            iw = ix1 - ix0
            s1 = ix0 + iw//3;  s2 = ix0 + (iw*2)//3   # separadores
            for y in range(iy0, iy1+1):
                for x in range(ix0, ix1+1):
                    on_b = x in (ix0, ix1) or y in (iy0, iy1)
                    on_s = x in (s1, s1+1, s2, s2+1)   # 2px de grosor
                    if on_b or on_s:
                        img.putpixel((x,y), WIN_FRAME)
                    else:
                        t = (y-iy0) / max(iy1-iy0, 1)
                        if x < s1:         # panel izquierdo
                            c = WIN_GLASS1 if t<0.35 else WIN_GLASS2 if t<0.7 else WIN_GLASS3
                        elif x <= s2+1:    # panel central
                            c = WIN_REFL if t<0.15 else WIN_GLASS1 if t<0.45 else WIN_GLASS2
                        else:              # panel derecho
                            c = WIN_GLASS2 if t<0.5 else WIN_GLASS3
                        img.putpixel((x,y), c)
        if y1+6 <= H-1:
            sx0=max(0,x0-2); sx1=min(W-1,x1+2)
            for sy in range(y1+1, y1+6):
                for sx in range(sx0, sx1+1):
                    e = sx==sx0 or sx==sx1 or sy==y1+1 or sy==y1+5
                    img.putpixel((sx,sy), WIN_OUTLINE if e else WIN_SILL_L if sy in(y1+2,y1+3) else WIN_SILL_D)
        return

    # ── Louvre (persianas horizontales — lamas cada 3px) ─────────────────────
    if style == "louvre":
        if header:
            hh=6; hx0=max(0,x0-1); hx1=min(W-1,x1+1); hy0=max(0,y0-hh); hy1=y0-1
            if hy1 > hy0:
                for y in range(hy0, hy1+1):
                    for x in range(hx0, hx1+1):
                        on_edge = x==hx0 or x==hx1 or y==hy0 or y==hy1
                        if on_edge:                       img.putpixel((x,y), WIN_OUTLINE)
                        elif y == hy0+1 or y == hy1-1:   img.putpixel((x,y), WIN_MOLDING)
                        elif (x-hx0) % 3 == 1:           img.putpixel((x,y), WIN_MOLDING2)
                        else:                             img.putpixel((x,y), WIN_LINTEL)
        layers = 2 if header else 3
        for y in range(y0, y1+1):
            for x in range(x0, x1+1):
                d = min(x-x0, x1-x, y-y0, y1-y)
                if d == 0:               img.putpixel((x,y), WIN_OUTLINE)
                elif d == 1:             img.putpixel((x,y), WIN_MOLDING)
                elif d==2 and layers==3: img.putpixel((x,y), WIN_MOLDING2)
        if not header:
            for x in range(x0+2, x1-1): img.putpixel((x, y0+1), WIN_LINTEL)
        off = layers
        ix0, iy0, ix1, iy1 = x0+off, y0+off, x1-off, y1-off
        if ix1 > ix0 and iy1 > iy0:
            for y in range(iy0, iy1+1):
                for x in range(ix0, ix1+1):
                    on_b = x in (ix0, ix1) or y in (iy0, iy1)
                    if on_b:
                        img.putpixel((x,y), WIN_FRAME)
                    else:
                        sl = (y - iy0) % 3
                        if sl == 0:   img.putpixel((x,y), WIN_FRAME)    # barra de persiana
                        elif sl == 1: img.putpixel((x,y), WIN_GLASS1)   # cara iluminada
                        else:         img.putpixel((x,y), WIN_GLASS3)   # sombra debajo
        if y1+6 <= H-1:
            sx0=max(0,x0-2); sx1=min(W-1,x1+2)
            for sy in range(y1+1, y1+6):
                for sx in range(sx0, sx1+1):
                    e = sx==sx0 or sx==sx1 or sy==y1+1 or sy==y1+5
                    img.putpixel((sx,sy), WIN_OUTLINE if e else WIN_SILL_L if sy in(y1+2,y1+3) else WIN_SILL_D)
        return

    # ── Porthole (ventana ojo de buey — circular) ─────────────────────────────
    if style == "porthole":
        cx_w = (x0 + x1) // 2
        cy_w = (y0 + y1) // 2
        r_out = min(x1-x0, y1-y0) // 2
        r_in  = max(1, r_out - 3)   # marco de 3px
        for y in range(y0, y1+1):
            for x in range(x0, x1+1):
                if not (0 <= x < W and 0 <= y < H): continue
                dx = x - cx_w; dy = y - cy_w
                d = (dx*dx + dy*dy) ** 0.5
                if d > r_out + 0.5: continue        # fuera → transparente
                if d > r_in:                        # anillo del marco
                    if   d > r_out - 0.5: img.putpixel((x,y), WIN_OUTLINE)
                    elif d > r_out - 1.5: img.putpixel((x,y), WIN_MOLDING)
                    else:                 img.putpixel((x,y), WIN_MOLDING2)
                else:                               # vidrio
                    nx_n = (dx/max(r_in,1) + 1) / 2
                    ny_n = (dy/max(r_in,1) + 1) / 2
                    t = (nx_n + ny_n) / 2
                    c = WIN_REFL if t<0.2 else WIN_GLASS1 if t<0.45 else WIN_GLASS2 if t<0.7 else WIN_GLASS3
                    img.putpixel((x,y), c)
        return

    # ── Diamante (X interior — 4 paneles triangulares) ────────────────────────
    if style == "diamond":
        if header:
            hh=6; hx0=max(0,x0-1); hx1=min(W-1,x1+1); hy0=max(0,y0-hh); hy1=y0-1
            if hy1 > hy0:
                for y in range(hy0, hy1+1):
                    for x in range(hx0, hx1+1):
                        on_edge = x==hx0 or x==hx1 or y==hy0 or y==hy1
                        if on_edge:                         img.putpixel((x,y), WIN_OUTLINE)
                        elif y == hy0+1 or y == hy1-1:     img.putpixel((x,y), WIN_MOLDING)
                        elif (x-hx0) % 3 == 1:             img.putpixel((x,y), WIN_MOLDING2)
                        else:                               img.putpixel((x,y), WIN_LINTEL)
        layers = 2 if header else 3
        for y in range(y0, y1+1):
            for x in range(x0, x1+1):
                d = min(x-x0, x1-x, y-y0, y1-y)
                if d == 0:               img.putpixel((x,y), WIN_OUTLINE)
                elif d == 1:             img.putpixel((x,y), WIN_MOLDING)
                elif d==2 and layers==3: img.putpixel((x,y), WIN_MOLDING2)
        if not header:
            for x in range(x0+2, x1-1): img.putpixel((x, y0+1), WIN_LINTEL)
        off = layers
        ix0, iy0, ix1, iy1 = x0+off, y0+off, x1-off, y1-off
        if ix1 > ix0 and iy1 > iy0:
            iw = ix1-ix0; ih = iy1-iy0
            for y in range(iy0, iy1+1):
                for x in range(ix0, ix1+1):
                    dx = x-ix0; dy = y-iy0
                    nx = dx/max(iw,1); ny = dy/max(ih,1)
                    d1 = abs(ny - nx)
                    d2 = abs(ny - (1.0 - nx))
                    on_b = x in (ix0,ix1) or y in (iy0,iy1)
                    if on_b or d1 < 0.14 or d2 < 0.14:
                        img.putpixel((x,y), WIN_FRAME)
                    else:
                        if   ny < nx  and ny < 1-nx:  c = WIN_GLASS1
                        elif ny > nx  and ny > 1-nx:  c = WIN_GLASS3
                        else:                         c = WIN_GLASS2
                        img.putpixel((x,y), c)
        if y1+6 <= H-1:
            sx0=max(0,x0-2); sx1=min(W-1,x1+2)
            for sy in range(y1+1, y1+6):
                for sx in range(sx0, sx1+1):
                    e = sx==sx0 or sx==sx1 or sy==y1+1 or sy==y1+5
                    img.putpixel((sx,sy), WIN_OUTLINE if e else WIN_SILL_L if sy in(y1+2,y1+3) else WIN_SILL_D)
        return

    # ── Header decorativo (friso con lineas verticales y horizontales) ─────────
    if header:
        hh  = 6                                # altura del friso
        hx0 = max(0,    x0 - 1)
        hx1 = min(W-1,  x1 + 1)
        hy0 = max(0,    y0 - hh)
        hy1 = y0 - 1
        if hy1 > hy0:
            for y in range(hy0, hy1 + 1):
                for x in range(hx0, hx1 + 1):
                    on_edge = x==hx0 or x==hx1 or y==hy0 or y==hy1
                    if on_edge:
                        img.putpixel((x, y), WIN_OUTLINE)
                    elif y == hy0 + 1:          # linea horizontal superior
                        img.putpixel((x, y), WIN_MOLDING)
                    elif y == hy1 - 1:          # linea horizontal inferior
                        img.putpixel((x, y), WIN_MOLDING)
                    elif (x - hx0) % 3 == 1:   # lineas verticales cada 3px
                        img.putpixel((x, y), WIN_MOLDING2)
                    else:
                        img.putpixel((x, y), WIN_LINTEL)

    # ── Moldura de la ventana (2 capas si hay header, 3 si no) ────────────────
    layers = 2 if header else 3
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d = min(x-x0, x1-x, y-y0, y1-y)
            if d == 0: img.putpixel((x, y), WIN_OUTLINE)
            elif d == 1: img.putpixel((x, y), WIN_MOLDING)
            elif d == 2 and layers == 3: img.putpixel((x, y), WIN_MOLDING2)

    # Lintel solo sin header
    if not header:
        for x in range(x0 + 2, x1 - 1):
            img.putpixel((x, y0 + 1), WIN_LINTEL)

    # ── Interior de vidrio ────────────────────────────────────────────────────
    off = layers
    ix0, iy0, ix1, iy1 = x0+off, y0+off, x1-off, y1-off
    if ix1 <= ix0 or iy1 <= iy0: return
    iw = ix1-ix0+1; ih = iy1-iy0+1
    cx = (ix0+ix1)//2; cy = (iy0+iy1)//2
    d1x = ix0+iw//3; d2x = ix0+(iw*2)//3; d1y = iy0+ih//2
    for y in range(iy0, iy1+1):
        for x in range(ix0, ix1+1):
            if style == "4panes":
                frm = x in (ix0,ix1,cx) or y in (iy0,iy1,cy)
            elif style == "2panes":
                frm = x in (ix0,ix1,cx) or y in (iy0,iy1)
            elif style == "grid":
                frm = x in (ix0,ix1,d1x,d2x) or y in (iy0,iy1,d1y)
            else:  # single
                frm = x in (ix0,ix1) or y in (iy0,iy1)
            if frm:
                img.putpixel((x, y), WIN_FRAME); continue
            left = x < cx; upper = y < cy
            if style == "grid":
                ci = 0 if x<d1x else (1 if x<d2x else 2)
                ri = 0 if y<d1y else 1
                pal = [WIN_REFL,WIN_GLASS1,WIN_GLASS2,WIN_GLASS1,WIN_GLASS2,WIN_GLASS3]
                c = pal[ri*3+ci]
                if ri==0 and ci==0 and x==ix0+1 and y==iy0+1: c = WIN_REFL
            elif style == "single":
                dw = max(iw-1,1); dh = max(ih-1,1)
                t = ((x-ix0)/dw + (y-iy0)/dh) / 2
                c = WIN_REFL if t<0.2 else WIN_GLASS1 if t<0.45 else WIN_GLASS2 if t<0.7 else WIN_GLASS3
            elif style == "2panes":
                c = (WIN_REFL if (x==ix0+1 and y==iy0+1) else WIN_GLASS1) if (left and upper) else \
                    WIN_GLASS2 if upper else WIN_GLASS2 if left else WIN_GLASS3
            else:  # 4panes
                if left and upper: c = WIN_REFL if (x==ix0+1 and y==iy0+1) else WIN_GLASS1
                elif not left and upper: c = WIN_GLASS2
                elif left: c = WIN_GLASS2
                else: c = WIN_GLASS3
            img.putpixel((x, y), c)

    # ── Alfeizar — solo si hay espacio suficiente ─────────────────────────────
    if y1 + 6 <= H - 1:
        sx0 = max(0, x0-2); sx1 = min(W-1, x1+2)
        for sy in range(y1+1, y1+6):
            for sx in range(sx0, sx1+1):
                e = sx==sx0 or sx==sx1 or sy==y1+1 or sy==y1+5
                img.putpixel((sx, sy), WIN_OUTLINE if e else WIN_SILL_L if sy in (y1+2,y1+3) else WIN_SILL_D)


# ==============================================================================
# PUERTA
# ==============================================================================

def draw_door(img, x0, y0, x1, y1):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            img.putpixel((x,y), DOOR_BASE)
    for y in range(y0,y1+1):
        img.putpixel((x0,y),DOOR_OUTLINE); img.putpixel((x1,y),DOOR_OUTLINE)
        img.putpixel((x0+1,y),DOOR_DARK);  img.putpixel((x1-1,y),DOOR_DARK)
    for x in range(x0, x1+1):
        img.putpixel((x, y0), DOOR_OUTLINE)
    for x in range(x0+1, x1):          # saltar columnas de outline para no pisarlas
        img.putpixel((x, y0+1), DOOR_DARK)
    px0,px1,py0,py1 = x0+3,x1-3,y0+3,y1-2
    if px1>px0 and py1>py0:
        for y in range(py0,py1+1):
            for x in range(px0,px1+1):
                e=x in(px0,px1) or y in(py0,py1)
                img.putpixel((x,y), DOOR_DARK if e else DOOR_LIGHT if (y==py0+1 or x==px0+1) else DOOR_MID)
    hx=x1-4; hy=(y0+y1)//2
    for dy in range(-1,3): img.putpixel((hx,hy+dy),DOOR_HANDLE)
    img.putpixel((hx-1,hy),DOOR_HANDLE); img.putpixel((hx-1,hy+1),DOOR_HANDLE)


# ==============================================================================
# HELPERS
# ==============================================================================

def new_frame(): return Image.new("RGBA",(W,H),(0,0,0,0))
def save(img, name):
    img.save(os.path.join(DST,name)); print(f"{name} guardado")

def draw_roof_frame(img):
    """Borde del FRAME5 con el outline de la pared — coincide con la fachada."""
    outline = _wall_outline()
    for x in range(W):
        img.putpixel((x, 0),   outline)
        img.putpixel((x, H-1), outline)
    for y in range(H):
        img.putpixel((0,   y), outline)
        img.putpixel((W-1, y), outline)


# ==============================================================================
# GENERACION — edita NOMBRE_SALIDA arriba para elegir que casa generar
# ==============================================================================

DST = os.path.join(BASE, NOMBRE_SALIDA)
os.makedirs(DST, exist_ok=True)

if NOMBRE_SALIDA == "CASA5":
    # ── FRAME 1: ventana 4panes con header izq + puerta der ──────────────────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_window(f1,  3, 23, 19, 38, style="4panes", header=True)
    draw_door(f1,   25, 30, 38, 47)
    save(f1, "FRAME1.png")

    # ── FRAME 2: ventana 2panes con header centrada ───────────────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2, 14, 23, 33, 37, style="2panes", header=True)
    save(f2, "FRAME2.png")

    # ── FRAME 3: ventana single con header — lado izquierdo ───────────────────
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    draw_window(f3,  8, 20, 22, 35, style="single", header=True)
    save(f3, "FRAME3.png")

    # ── FRAME 4: pared Tudor limpia (sin ventana) ─────────────────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo cobre ──────────────────────────────────────────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

elif NOMBRE_SALIDA == "CASA16":
    # ── FRAME 1: frente — jalousie + puerta ──────────────────────────────────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_window(f1,  2, 21, 20, 39, style="jalousie")
    draw_window(f1, 23, 21, 30, 30, style="jalousie")  # chica esquina
    draw_door(f1,   33, 31, 45, 47)
    save(f1, "FRAME1.png")

    # ── FRAME 2: atras — jalousie panoramica horizontal ───────────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2,  3, 22, 44, 37, style="jalousie")  # ancha — muchas lamas
    save(f2, "FRAME2.png")

    # ── FRAME 3: lado izquierdo — 2 jalousies asimetricos ────────────────────
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    draw_window(f3,  2, 5, 20, 42, style="jalousie")   # alto y estrecho
    draw_window(f3, 24, 12, 45, 36, style="jalousie")  # ancho y medio
    save(f3, "FRAME3.png")

    # ── FRAME 4: lado derecho — jalousie gigante centrada ────────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    draw_window(f4,  5, 6, 42, 42, style="jalousie")
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo esmeralda ──────────────────────────────────────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

elif NOMBRE_SALIDA == "CASA15":
    # ── FRAME 1: frente — triple ancha + puerta ───────────────────────────────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_window(f1,  2, 21, 29, 39, style="triple")
    draw_door(f1,   33, 31, 45, 47)
    save(f1, "FRAME1.png")

    # ── FRAME 2: atras — 2 triples lado a lado ────────────────────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2,  2, 22, 22, 38, style="triple")
    draw_window(f2, 25, 22, 45, 38, style="triple")
    save(f2, "FRAME2.png")

    # ── FRAME 3: lado izquierdo — triple muy alta (columna de vidrio) ─────────
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    draw_window(f3,  5, 4, 42, 42, style="triple")
    save(f3, "FRAME3.png")

    # ── FRAME 4: lado derecho — triple baja + louvre arriba ───────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    draw_window(f4,  4, 6, 43, 20, style="louvre")   # franja de persianas arriba
    draw_window(f4,  4, 24, 43, 42, style="triple")   # triple abajo
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo lava ───────────────────────────────────────────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

elif NOMBRE_SALIDA == "CASA14":
    # ── FRAME 1: frente — louvre grande + louvre chico + puerta ─────────────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_window(f1,  2, 22, 20, 40, style="louvre")   # ancho + alto, muchas lamas
    draw_window(f1, 23, 22, 31, 33, style="louvre")   # chico
    draw_door(f1,   33, 31, 45, 47)
    save(f1, "FRAME1.png")

    # ── FRAME 2: atras — louvre panoramico muy ancho y bajo ──────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2,  4, 22, 43, 34, style="louvre")   # casi toda la anchura
    save(f2, "FRAME2.png")

    # ── FRAME 3: lado izquierdo — 2 louvres offset diagonal ──────────────────
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    draw_window(f3,  2, 5, 22, 24, style="louvre")
    draw_window(f3, 23, 26, 45, 44, style="louvre")
    save(f3, "FRAME3.png")

    # ── FRAME 4: lado derecho — 2 louvres altos y estrechos ──────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    draw_window(f4,  3, 8, 20, 40, style="louvre")
    draw_window(f4, 24, 8, 44, 40, style="louvre")
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo indigo ─────────────────────────────────────────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

elif NOMBRE_SALIDA == "CASA13":
    # ── FRAME 1: frente — porthole grande izq + porthole chico + puerta ──────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_window(f1,  2, 20, 18, 36, style="porthole")   # r=8
    draw_window(f1, 21, 20, 30, 29, style="porthole")   # r=4 pequeño
    draw_door(f1,   33, 31, 45, 47)
    save(f1, "FRAME1.png")

    # ── FRAME 2: atras — 3 portholes en fila ─────────────────────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2,  2, 22, 14, 35, style="porthole")   # r=6
    draw_window(f2, 17, 22, 30, 35, style="porthole")   # r=6
    draw_window(f2, 33, 22, 45, 35, style="porthole")   # r=6
    save(f2, "FRAME2.png")

    # ── FRAME 3: lado izquierdo — 1 porthole gigante ──────────────────────────
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    draw_window(f3,  5, 6, 42, 42, style="porthole")    # r=18 enorme
    save(f3, "FRAME3.png")

    # ── FRAME 4: lado derecho — 2 portholes offset ───────────────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    draw_window(f4,  3, 4, 21, 22, style="porthole")    # r=9 arriba-izq
    draw_window(f4, 24, 22, 44, 44, style="porthole")   # r=10 abajo-der
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo coral ──────────────────────────────────────────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

elif NOMBRE_SALIDA == "CASA12":
    # ── FRAME 1: frente — 1 diamante grande izq + puerta der ─────────────────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_window(f1,  2, 22, 21, 38, style="diamond")
    draw_door(f1,   33, 31, 45, 47)
    save(f1, "FRAME1.png")

    # ── FRAME 2: atras — 2 diamantes lado a lado ──────────────────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2,  3, 22, 19, 38, style="diamond")
    draw_window(f2, 24, 22, 44, 38, style="diamond")
    save(f2, "FRAME2.png")

    # ── FRAME 3: lado izquierdo — diamante alto + franja strip baja ───────────
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    draw_window(f3,  4, 6, 22, 28, style="diamond")
    draw_window(f3, 26, 32, 44, 40, style="strip")
    save(f3, "FRAME3.png")

    # ── FRAME 4: lado derecho — diamante panoramico enorme ───────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    draw_window(f4,  4, 8, 43, 36, style="diamond")
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo dorado ─────────────────────────────────────────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

elif NOMBRE_SALIDA == "CASA11":
    # ── FRAME 1: frente — 2 arcos grandes + puerta esquina ───────────────────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_window(f1,  2, 26, 15, 40, style="arch")
    draw_window(f1, 18, 26, 31, 40, style="arch")
    draw_door(f1,   34, 31, 46, 47)
    save(f1, "FRAME1.png")

    # ── FRAME 2: atras — franja strip moderna + grid lateral ─────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2,  3, 22, 24, 29, style="strip")
    draw_window(f2, 27, 22, 44, 38, style="grid")
    save(f2, "FRAME2.png")

    # ── FRAME 3: lado izquierdo — dos ventanas offset (arriba izq + abajo der)
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    draw_window(f3,  3, 6, 19, 19, style="4panes")
    draw_window(f3, 22, 24, 44, 38, style="2panes")
    save(f3, "FRAME3.png")

    # ── FRAME 4: lado derecho — ventana unica panoramica ─────────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    draw_window(f4,  6, 12, 42, 34, style="single")
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo turquesa ───────────────────────────────────────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

elif NOMBRE_SALIDA == "CASA10":
    # ── FRAME 1: frente — 2 ventanas + puerta ────────────────────────────────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_window(f1,  2, 20, 14, 33, style="2panes")
    draw_window(f1, 18, 20, 30, 33, style="2panes")
    draw_door(f1,   33, 31, 45, 47)
    save(f1, "FRAME1.png")

    # ── FRAME 2: atras — ventana grid centrada ────────────────────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2, 14, 20, 33, 35, style="grid")
    save(f2, "FRAME2.png")

    # ── FRAME 3: lado izquierdo — ventana single ──────────────────────────────
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    draw_window(f3, 10, 14, 25, 28, style="single")
    save(f3, "FRAME3.png")

    # ── FRAME 4: pared limpia ─────────────────────────────────────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo fucsia ─────────────────────────────────────────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

elif NOMBRE_SALIDA == "CASA9":
    # ── FRAME 1: frente — arco izq + puerta der ───────────────────────────────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_window(f1,  3, 21, 17, 37, style="arch")
    draw_door(f1,   24, 31, 37, 47)
    save(f1, "FRAME1.png")

    # ── FRAME 2: atras — arco centrado ────────────────────────────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2, 15, 21, 32, 36, style="arch")
    save(f2, "FRAME2.png")

    # ── FRAME 3: lado izquierdo — 4panes clasico ──────────────────────────────
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    draw_window(f3,  9, 15, 24, 31, style="4panes")
    save(f3, "FRAME3.png")

    # ── FRAME 4: pared limpia ─────────────────────────────────────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo verde bosque ───────────────────────────────────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

elif NOMBRE_SALIDA == "CASA8":
    # ── FRAME 1: frente — reloj en el gable, sin ventanas, puerta centrada ────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_door(f1, 17, 31, 30, 47)           # puerta centrada
    save(f1, "FRAME1.png")

    # ── FRAME 2: atras — 1 ventana grid pequena ───────────────────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2, 15, 22, 32, 35, style="grid")
    save(f2, "FRAME2.png")

    # ── FRAME 3: lado izquierdo — pared limpia (madera oscura imponente) ──────
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    save(f3, "FRAME3.png")

    # ── FRAME 4: lado derecho — 1 ventana 4panes pequena alta ────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    draw_window(f4, 18, 12, 30, 24, style="4panes")
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo cobre patinado ─────────────────────────────────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

elif NOMBRE_SALIDA == "CASA7":
    # ── FRAME 1: frente — ventana 4panes con header + puerta ─────────────────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_window(f1,  3, 20, 18, 34, style="4panes")
    draw_door(f1,   24, 31, 35, 47)
    save(f1, "FRAME1.png")

    # ── FRAME 2: atras — ventana 2panes descentrada ───────────────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2,  8, 21, 26, 35, style="2panes")
    save(f2, "FRAME2.png")

    # ── FRAME 3: lado izquierdo — ventana single ──────────────────────────────
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    draw_window(f3, 10, 16, 24, 30, style="single")
    save(f3, "FRAME3.png")

    # ── FRAME 4: lado derecho — pared limpia ──────────────────────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo pizarra ────────────────────────────────────────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

elif NOMBRE_SALIDA == "CASA6":
    # ── FRAME 1: arco + puerta ────────────────────────────────────────────────
    f1 = new_frame()
    draw_wall(f1, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f1, GABLE_BASE)
    draw_window(f1,  4, 26, 20, 40, style="arch")
    draw_door(f1,   26, 30, 40, 47)
    save(f1, "FRAME1.png")

    # ── FRAME 2: dos arcos pequeños ───────────────────────────────────────────
    f2 = new_frame()
    draw_wall(f2, 0, GABLE_BASE, W-1, H-1)
    draw_gable(f2, GABLE_BASE)
    draw_window(f2,  5, 26, 17, 38, style="arch")
    draw_window(f2, 30, 26, 42, 38, style="arch")
    save(f2, "FRAME2.png")

    # ── FRAME 3: pared limpia ─────────────────────────────────────────────────
    f3 = new_frame()
    draw_wall(f3, 0, 0, W-1, H-1)
    save(f3, "FRAME3.png")

    # ── FRAME 4: arco centrado — lado derecho ─────────────────────────────────
    f4 = new_frame()
    draw_wall(f4, 0, 0, W-1, H-1)
    draw_window(f4, 13, 20, 34, 36, style="arch")
    save(f4, "FRAME4.png")

    # ── FRAME 5: techo terracota (contraste calido vs pared teal) ─────────────
    f5 = new_frame()
    for y in range(H):
        for x in range(W):
            f5.putpixel((x,y), _roof_color(x,y))
    draw_roof_frame(f5)
    save(f5, "FRAME5.png")

print(f"\n{NOMBRE_SALIDA} ({W}x{H}) lista en: {DST}")
