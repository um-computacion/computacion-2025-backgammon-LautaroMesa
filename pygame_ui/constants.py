# pygame_ui/constants.py

import pygame

# --- TAMAÑOS ---
# Dimensiones de la ventana
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Dimensiones del tablero
MARGEN_TABLERO_X = 50
MARGEN_TABLERO_Y = 50
ANCHO_TABLERO = ANCHO_PANTALLA - (2 * MARGEN_TABLERO_X)
ALTO_TABLERO = ALTO_PANTALLA - (2 * MARGEN_TABLERO_Y)

# Dimensiones de los puntos (triángulos)
ANCHO_PUNTO = ANCHO_TABLERO / 13  # 12 puntos + 1 barra
ALTO_PUNTO = int(ALTO_TABLERO * 0.45)  # Alto de los triángulos
ANCHO_BARRA = ANCHO_PUNTO

# Dimensiones de las fichas
RADIO_FICHA = int(ANCHO_PUNTO * 0.45)
DIAMETRO_FICHA = RADIO_FICHA * 2

# Posiciones clave
CENTRO_X = ANCHO_PANTALLA / 2
CENTRO_Y = ALTO_PANTALLA / 2
BORDE_SUPERIOR_Y = MARGEN_TABLERO_Y
BORDE_INFERIOR_Y = ALTO_PANTALLA - MARGEN_TABLERO_Y
BARRA_Y_INICIO_ARRIBA = BORDE_SUPERIOR_Y
BARRA_Y_INICIO_ABAJO = BORDE_INFERIOR_Y - DIAMETRO_FICHA

# --- COLORES (RGB) ---
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_FONDO = (0, 50, 0)  # Verde oscuro
COLOR_TABLERO = (245, 222, 179)  # Color madera (Beige)
COLOR_PUNTO_A = (139, 69, 19)  # Marrón
COLOR_PUNTO_B = (210, 180, 140)  # Marrón claro
COLOR_BARRA = (100, 100, 100)  # Gris
COLOR_RESALTADO = (255, 255, 0, 100)  # Amarillo semitransparente
COLOR_MOVIMIENTO_POSIBLE = (0, 255, 0, 100)  # Verde semitransparente
COLOR_TEXTO = (230, 230, 230) # <--- ¡Este ya está corregido!

# --- FUENTES ---
pygame.font.init()
FUENTE_DEFAULT = pygame.font.SysFont("Arial", 18)
FUENTE_GRANDE = pygame.font.SysFont("Arial", 28)
FUENTE_GANADOR = pygame.font.SysFont("Impact", 60)

# --- ASSETS (IMÁGENES) ---
RUTA_ASSETS = "assets/"
RUTA_FONDO_TABLERO = RUTA_ASSETS + "board_texture.png"
RUTA_FICHA_BLANCA = RUTA_ASSETS + "checker_white.png"
RUTA_FICHA_NEGRA = RUTA_ASSETS + "checker_black.png"

# Diccionario para las caras de los dados
RUTA_IMAGENES_DADOS = {
    1: RUTA_ASSETS + "die_1.png",
    2: RUTA_ASSETS + "die_2.png",
    3: RUTA_ASSETS + "die_3.png",
    4: RUTA_ASSETS + "die_4.png",
    5: RUTA_ASSETS + "die_5.png",
    6: RUTA_ASSETS + "die_6.png",
}

# --- CONFIGURACIÓN DE PUNTOS (Se llenan dinámicamente) ---
COORDENADAS_PUNTOS = {}
HITBOXES_PUNTOS = {}
HITBOX_BARRA_J1 = None
HITBOX_BARRA_J2 = None
HITBOX_BOTON_LANZAR = None
HITBOX_FUERA_BLANCO = None  # Área clicable para sacar fichas de Blancas
HITBOX_FUERA_NEGRO = None   # Área clicable para sacar fichas de Negras
FPS = 180