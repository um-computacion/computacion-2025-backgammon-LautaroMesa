# pygame_ui/game_ui.py

import pygame
import sys
import math
from . import constants as const
# Importamos las clases del core
from core.game import Game
from core.board import Tablero 
from core.player import Player

class InterfazPygame:
    """
    Controla toda la interfaz gráfica de Pygame.
    Se comunica con la clase BackgammonGame de la lógica central.
    """

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.__pantalla__ = pygame.display.set_mode(
            (const.ANCHO_PANTALLA, const.ALTO_PANTALLA)
        )
        pygame.display.set_caption("Backgammon Computación 2025")
        self.__reloj__ = pygame.time.Clock()
        self.__assets__ = self.__cargar_assets__()

        # --- Obtener nombres de jugadores con interfaz gráfica ---
        nombre1, nombre2 = self.__pedir_nombres_jugadores__()

        # --- Instancia del Juego ---
        self.__juego__ = Game(nombre1, nombre2)

        # --- Estado de la UI ---
        self.__punto_seleccionado__ = None
        self.__movimientos_posibles__ = {}
        self.__boton_pasar_turno__ = None
        self.__mensaje_error__ = None
        self.__tiempo_error__ = 0

        self.__generar_coordenadas_layout__()

    def __pedir_nombres_jugadores__(self):
        """
        Muestra una pantalla elegante de sala de juegos para ingresar los nombres de los jugadores.
        """
        fuente_titulo = pygame.font.Font(None, 72)
        fuente_subtitulo = pygame.font.Font(None, 40)
        fuente_input = pygame.font.Font(None, 36)
        fuente_hint = pygame.font.Font(None, 24)
        
        nombre1 = ""
        nombre2 = ""
        input_activo = 1  # 1 para jugador 1, 2 para jugador 2
        
        reloj = pygame.time.Clock()
        
        while True:
            # Fondo elegante de madera oscura con textura
            self.__pantalla__.fill((40, 30, 20))  # Marrón oscuro profundo
            
            # Panel decorativo superior
            panel_superior = pygame.Rect(0, 0, const.ANCHO_PANTALLA, 180)
            # Gradiente simulado con múltiples rectángulos
            for i in range(180):
                color_gradiente = (30 + i // 6, 20 + i // 8, 10 + i // 12)
                pygame.draw.line(self.__pantalla__, color_gradiente, (0, i), (const.ANCHO_PANTALLA, i))
            
            # Marco dorado decorativo
            pygame.draw.rect(self.__pantalla__, (218, 165, 32), (20, 20, const.ANCHO_PANTALLA - 40, const.ALTO_PANTALLA - 40), 4, border_radius=15)
            pygame.draw.rect(self.__pantalla__, (139, 90, 43), (25, 25, const.ANCHO_PANTALLA - 50, const.ALTO_PANTALLA - 50), 2, border_radius=12)
            
            # Título principal con sombra
            titulo = fuente_titulo.render("BACKGAMMON", True, (218, 165, 32))
            sombra_titulo = fuente_titulo.render("BACKGAMMON", True, (20, 15, 10))
            self.__pantalla__.blit(sombra_titulo, (const.ANCHO_PANTALLA // 2 - titulo.get_width() // 2 + 3, 58))
            self.__pantalla__.blit(titulo, (const.ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 55))
            
            # Subtítulo elegante
            subtitulo = fuente_subtitulo.render("Sala de Juegos", True, (180, 140, 90))
            self.__pantalla__.blit(subtitulo, (const.ANCHO_PANTALLA // 2 - subtitulo.get_width() // 2, 130))
            
            # Línea decorativa
            pygame.draw.line(self.__pantalla__, (218, 165, 32), 
                           (const.ANCHO_PANTALLA // 2 - 200, 185), 
                           (const.ANCHO_PANTALLA // 2 + 200, 185), 3)
            
            # Instrucciones con estilo
            y_instruccion = 220
            if input_activo == 1:
                instruccion = fuente_input.render("Jugador Blanco", True, (240, 230, 200))
                icono = "♔"  # Rey blanco
            else:
                instruccion = fuente_input.render("Jugador Negro", True, (240, 230, 200))
                icono = "♚"  # Rey negro
            
            fuente_icono = pygame.font.Font(None, 50)
            texto_icono = fuente_icono.render(icono, True, (218, 165, 32))
            self.__pantalla__.blit(texto_icono, (const.ANCHO_PANTALLA // 2 - instruccion.get_width() // 2 - 50, y_instruccion - 5))
            self.__pantalla__.blit(instruccion, (const.ANCHO_PANTALLA // 2 - instruccion.get_width() // 2, y_instruccion))
            
            # Campo de entrada con estilo de madera tallada
            rect_input = pygame.Rect(const.ANCHO_PANTALLA // 2 - 250, 280, 500, 60)
            
            # Fondo del input con efecto hundido
            pygame.draw.rect(self.__pantalla__, (60, 45, 30), rect_input, border_radius=8)
            pygame.draw.rect(self.__pantalla__, (30, 22, 15), 
                           (rect_input.x + 3, rect_input.y + 3, rect_input.width - 6, rect_input.height - 6), 
                           border_radius=6)
            
            # Borde dorado brillante si está activo
            if input_activo:
                pygame.draw.rect(self.__pantalla__, (218, 165, 32), rect_input, 3, border_radius=8)
            else:
                pygame.draw.rect(self.__pantalla__, (100, 80, 60), rect_input, 2, border_radius=8)
            
            # Mostrar nombre actual
            if input_activo == 1:
                texto_nombre = fuente_input.render(nombre1 + "|", True, (255, 245, 220))
            else:
                texto_nombre = fuente_input.render(nombre2 + "|", True, (255, 245, 220))
            
            self.__pantalla__.blit(texto_nombre, (rect_input.x + 20, rect_input.y + 15))
            
            # Hint de texto si está vacío
            if (input_activo == 1 and not nombre1) or (input_activo == 2 and not nombre2):
                hint = fuente_hint.render("Ingrese su nombre...", True, (120, 100, 80))
                self.__pantalla__.blit(hint, (rect_input.x + 20, rect_input.y + 18))
            
            # Mostrar confirmación del primer jugador
            if nombre1:
                panel_confirmado = pygame.Rect(const.ANCHO_PANTALLA // 2 - 200, 370, 400, 50)
                pygame.draw.rect(self.__pantalla__, (50, 80, 50, 150), panel_confirmado, border_radius=10)
                pygame.draw.rect(self.__pantalla__, (100, 180, 100), panel_confirmado, 2, border_radius=10)
                
                confirmado1 = fuente_input.render(f"✓ Blanco: {nombre1}", True, (150, 255, 150))
                self.__pantalla__.blit(confirmado1, (const.ANCHO_PANTALLA // 2 - confirmado1.get_width() // 2, 380))
            
            # Instrucción final
            if nombre2 and input_activo == 2:
                info = fuente_input.render("Presiona ENTER para comenzar", True, (255, 220, 100))
                sombra_info = fuente_input.render("Presiona ENTER para comenzar", True, (100, 80, 40))
                y_info = 460
                # Efecto de parpadeo
                if (pygame.time.get_ticks() // 500) % 2 == 0:
                    self.__pantalla__.blit(sombra_info, (const.ANCHO_PANTALLA // 2 - info.get_width() // 2 + 2, y_info + 2))
                    self.__pantalla__.blit(info, (const.ANCHO_PANTALLA // 2 - info.get_width() // 2, y_info))
            
            # Decoración inferior
            pygame.draw.line(self.__pantalla__, (218, 165, 32), 
                           (50, const.ALTO_PANTALLA - 50), 
                           (const.ANCHO_PANTALLA - 50, const.ALTO_PANTALLA - 50), 2)
            
            pygame.display.flip()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        if input_activo == 1 and nombre1.strip():
                            input_activo = 2
                        elif input_activo == 2 and nombre2.strip():
                            return (nombre1 or "Jugador Blanco", nombre2 or "Jugador Negro")
                    elif evento.key == pygame.K_BACKSPACE:
                        if input_activo == 1:
                            nombre1 = nombre1[:-1]
                        else:
                            nombre2 = nombre2[:-1]
                    else:
                        if len(nombre1 if input_activo == 1 else nombre2) < 15:
                            if input_activo == 1:
                                nombre1 += evento.unicode
                            else:
                                nombre2 += evento.unicode
            
            reloj.tick(30)
    
    def __cargar_assets__(self):
        assets = {}
        try:
            assets["ficha_blanca"] = pygame.image.load(
                const.RUTA_FICHA_BLANCA
            ).convert_alpha()
            assets["ficha_blanca"] = pygame.transform.scale(
                assets["ficha_blanca"], (const.DIAMETRO_FICHA, const.DIAMETRO_FICHA)
            )
            assets["ficha_negra"] = pygame.image.load(
                const.RUTA_FICHA_NEGRA
            ).convert_alpha()
            assets["ficha_negra"] = pygame.transform.scale(
                assets["ficha_negra"], (const.DIAMETRO_FICHA, const.DIAMETRO_FICHA)
            )
            assets["dados"] = {}
            for i in range(1, 7):
                img_dado = pygame.image.load(const.RUTA_IMAGENES_DADOS[i]).convert_alpha()
                assets["dados"][i] = pygame.transform.scale(img_dado, (40, 40))
            try:
                assets["fondo_tablero"] = pygame.image.load(const.RUTA_FONDO_TABLERO).convert()
                assets["fondo_tablero"] = pygame.transform.scale(
                    assets["fondo_tablero"], (const.ANCHO_PANTALLA, const.ALTO_PANTALLA)
                )
            except pygame.error:
                assets["fondo_tablero"] = None
        except pygame.error as e:
            print(f"Error cargando assets: {e}")
            print("Asegúrate de tener la carpeta 'assets/' con las imágenes requeridas.")
            sys.exit()
        return assets

    def __generar_coordenadas_layout__(self):
        pos_x = const.MARGEN_TABLERO_X
        ancho_punto = const.ANCHO_PUNTO
        
        for i in range(12):
            if i == 6:
                pos_x += const.ANCHO_BARRA
            p1 = (pos_x, const.BORDE_INFERIOR_Y)
            p2 = (pos_x + ancho_punto, const.BORDE_INFERIOR_Y)
            p3 = (pos_x + ancho_punto / 2, const.BORDE_INFERIOR_Y - const.ALTO_PUNTO)
            const.COORDENADAS_PUNTOS[i] = [p1, p2, p3]
            const.HITBOXES_PUNTOS[i] = pygame.Rect(
                pos_x, const.BORDE_INFERIOR_Y - const.ALTO_PUNTO, ancho_punto, const.ALTO_PUNTO
            )
            pos_x += ancho_punto
            
        pos_x = const.MARGEN_TABLERO_X
        for i in range(23, 11, -1):
            if i == 17:
                pos_x += const.ANCHO_BARRA
            p1 = (pos_x, const.BORDE_SUPERIOR_Y)
            p2 = (pos_x + ancho_punto, const.BORDE_SUPERIOR_Y)
            p3 = (pos_x + ancho_punto / 2, const.BORDE_SUPERIOR_Y + const.ALTO_PUNTO)
            const.COORDENADAS_PUNTOS[i] = [p1, p2, p3]
            const.HITBOXES_PUNTOS[i] = pygame.Rect(
                pos_x, const.BORDE_SUPERIOR_Y, ancho_punto, const.ALTO_PUNTO
            )
            pos_x += ancho_punto

        barra_x = const.CENTRO_X - (const.ANCHO_BARRA / 2)
        const.HITBOX_BARRA_J1 = pygame.Rect(
            barra_x, const.CENTRO_Y, const.ANCHO_BARRA, const.ALTO_TABLERO / 2
        )
        const.HITBOX_BARRA_J2 = pygame.Rect(
            barra_x, const.MARGEN_TABLERO_Y, const.ANCHO_BARRA, const.ALTO_TABLERO / 2
        )
        const.HITBOX_BOTON_LANZAR = pygame.Rect(
            const.CENTRO_X - 50, const.CENTRO_Y - 20, 100, 40
        )

    # --- MÉTODOS DE DIBUJADO (DRAW) ---

    def __dibujar__(self):
        if self.__assets__["fondo_tablero"]:
            self.__pantalla__.blit(self.__assets__["fondo_tablero"], (0, 0))
        else:
            self.__pantalla__.fill(const.COLOR_FONDO)

        self.__dibujar_tablero__()
        self.__dibujar_todas_las_fichas__()
        self.__dibujar_elementos_ui__()
        self.__dibujar_resaltados__()
        self.__dibujar_mensaje_error__()
        self.__dibujar_mensaje_ganador__()

    def __dibujar_tablero__(self):
        # Fondo del tablero con borde
        rect_tablero = pygame.Rect(
            const.MARGEN_TABLERO_X, const.MARGEN_TABLERO_Y,
            const.ANCHO_TABLERO, const.ALTO_TABLERO
        )
        pygame.draw.rect(self.__pantalla__, const.COLOR_TABLERO, rect_tablero)
        
        # Borde del tablero para mayor definición
        pygame.draw.rect(self.__pantalla__, (101, 67, 33), rect_tablero, 4)
        
        # Barra central
        rect_barra = pygame.Rect(
            const.CENTRO_X - const.ANCHO_BARRA / 2, const.MARGEN_TABLERO_Y,
            const.ANCHO_BARRA, const.ALTO_TABLERO
        )
        pygame.draw.rect(self.__pantalla__, const.COLOR_BARRA, rect_barra)
        pygame.draw.rect(self.__pantalla__, (101, 67, 33), rect_barra, 2)
        
        # Dibujar los 24 puntos (triángulos)
        fuente_numeros = pygame.font.Font(None, 20)
        
        for i in range(24):
            # Alternar colores para los puntos
            color = const.COLOR_PUNTO_A if i % 2 == 0 else const.COLOR_PUNTO_B
            
            # Dibujar el triángulo
            pygame.draw.polygon(self.__pantalla__, color, const.COORDENADAS_PUNTOS[i])
            
            # Dibujar borde del triángulo para mayor nitidez
            pygame.draw.polygon(self.__pantalla__, (80, 60, 40), const.COORDENADAS_PUNTOS[i], 1)
            
            # Calcular posición del número
            hitbox = const.HITBOXES_PUNTOS[i]
            
            # Determinar si es fila superior o inferior
            es_fila_superior = i >= 12
            
            if es_fila_superior:
                # Números en la parte superior del triángulo
                pos_numero_x = hitbox.centerx
                pos_numero_y = const.BORDE_SUPERIOR_Y + 5
            else:
                # Números en la parte inferior del triángulo
                pos_numero_x = hitbox.centerx
                pos_numero_y = const.BORDE_INFERIOR_Y - 20
            
            # Calcular el número del punto según la lógica del backgammon
            # Fila inferior (índices 0-11): puntos 12, 11, 10, 9, 8, 7, | 6, 5, 4, 3, 2, 1
            # Fila superior (índices 12-23): puntos 13, 14, 15, 16, 17, 18 | 19, 20, 21, 22, 23, 24
            if es_fila_superior:
                # Fila superior: de 13 a 24
                numero_punto = i + 1  # índices 12-23 → puntos 13-24
            else:
                # Fila inferior: de 12 a 1 (invertido)
                numero_punto = 12 - i  # índices 0-11 → puntos 12-1
            
            # Dibujar el número del punto
            color_texto = (240, 230, 200) if i % 2 == 0 else (60, 40, 20)
            texto_numero = fuente_numeros.render(str(numero_punto), True, color_texto)
            
            # Centrar el número
            texto_rect = texto_numero.get_rect(center=(pos_numero_x, pos_numero_y))
            self.__pantalla__.blit(texto_numero, texto_rect)
        
        # Dibujar líneas divisorias entre cuadrantes para mayor claridad
        # Línea vertical izquierda (después del punto 6)
        x_linea_izq = const.MARGEN_TABLERO_X + (6 * const.ANCHO_PUNTO)
        pygame.draw.line(self.__pantalla__, (80, 60, 40), 
                        (x_linea_izq, const.MARGEN_TABLERO_Y), 
                        (x_linea_izq, const.MARGEN_TABLERO_Y + const.ALTO_TABLERO), 1)
        
        # Línea vertical derecha (después del punto 18)
        x_linea_der = const.MARGEN_TABLERO_X + (12 * const.ANCHO_PUNTO) + const.ANCHO_BARRA
        pygame.draw.line(self.__pantalla__, (80, 60, 40), 
                        (x_linea_der, const.MARGEN_TABLERO_Y), 
                        (x_linea_der, const.MARGEN_TABLERO_Y + const.ALTO_TABLERO), 1)

    def __dibujar_todas_las_fichas__(self):
        layout_tablero = self.__juego__.obtener_estado_tablero()

        # Fichas en los 24 puntos
        for indice_punto in range(24):
            if indice_punto not in layout_tablero:
                continue
            
            fichas = layout_tablero[indice_punto]
            if not fichas:
                continue
            
            # Determinar el color de la ficha basado en el primer carácter
            color_ficha = fichas[0]  # 'B' o 'N'
            img_ficha_original = self.__assets__["ficha_blanca"] if color_ficha == 'B' else self.__assets__["ficha_negra"]
            
            # Escalar la ficha a un tamaño compacto para no tapar números (75% del tamaño original)
            nuevo_diametro = int(const.DIAMETRO_FICHA * 0.75)
            img_ficha = pygame.transform.smoothscale(img_ficha_original, (nuevo_diametro, nuevo_diametro))
            
            base_x = const.HITBOXES_PUNTOS[indice_punto].left + (const.ANCHO_PUNTO - nuevo_diametro) // 2
            
            es_fila_superior = indice_punto >= 12
            pos_y = const.BORDE_SUPERIOR_Y + 8 if es_fila_superior else const.BORDE_INFERIOR_Y - nuevo_diametro - 8
            offset_y = nuevo_diametro - 8 if es_fila_superior else -(nuevo_diametro - 8)

            cantidad_fichas = len(fichas)
            for i in range(cantidad_fichas):
                if i >= 5: 
                    # Mostrar contador si hay más de 5 fichas
                    fuente = pygame.font.Font(None, 24)
                    texto = fuente.render(f"+{cantidad_fichas - 5}", True, (255, 255, 0))
                    self.__pantalla__.blit(texto, (base_x + nuevo_diametro // 2 - 10, pos_y + offset_y * 2))
                    break
                self.__pantalla__.blit(img_ficha, (base_x, pos_y))
                pos_y += offset_y

        # Fichas en la barra
        jugador1 = self.__juego__.mostrar_jugador1()
        jugador2 = self.__juego__.mostrar_jugador2()
        self.__dibujar_fichas_barra__(jugador1)
        self.__dibujar_fichas_barra__(jugador2)

        # Fichas en casa
        self.__dibujar_fichas_casa__(jugador1)
        self.__dibujar_fichas_casa__(jugador2)

    def __dibujar_fichas_barra__(self, jugador):
        color = 'B' if jugador.obtener_color() == 'blanco' else 'N'
        
        # Acceder al tablero a través del método público
        tablero = self.__juego__.obtener_tablero()
        contador = tablero.obtener_fichas_barra(color)
        
        if contador == 0:
            return

        img_ficha_original = self.__assets__["ficha_blanca"] if color == 'B' else self.__assets__["ficha_negra"]
        
        # Escalar la ficha a un tamaño compacto
        nuevo_diametro = int(const.DIAMETRO_FICHA * 0.75)
        img_ficha = pygame.transform.smoothscale(img_ficha_original, (nuevo_diametro, nuevo_diametro))
        
        pos_x = const.CENTRO_X - nuevo_diametro // 2
        
        if color == 'B': 
            pos_y = const.BARRA_Y_INICIO_ABAJO
            offset_y = -(nuevo_diametro - 8)
        else: 
            pos_y = const.BARRA_Y_INICIO_ARRIBA
            offset_y = nuevo_diametro - 8

        for i in range(contador):
            self.__pantalla__.blit(img_ficha, (pos_x, pos_y))
            pos_y += offset_y

    def __dibujar_fichas_casa__(self, jugador):
        color = 'B' if jugador.obtener_color() == 'blanco' else 'N'
        
        # Acceder al tablero a través del método público
        tablero = self.__juego__.obtener_tablero()
        
        # Obtener fichas fuera del tablero (en casa) usando el método público
        contador = tablero.obtener_fichas_fuera(color)
        
        if contador == 0:
            return

        img_ficha_original = self.__assets__["ficha_blanca"] if color == 'B' else self.__assets__["ficha_negra"]
        
        # Escalar la ficha a un tamaño compacto
        nuevo_diametro = int(const.DIAMETRO_FICHA * 0.75)
        img_ficha = pygame.transform.smoothscale(img_ficha_original, (nuevo_diametro, nuevo_diametro))
        
        pos_x = const.ANCHO_PANTALLA - const.MARGEN_TABLERO_X / 2

        if color == 'B':
            pos_y = const.ALTO_PANTALLA - const.MARGEN_TABLERO_Y - 30
        else: 
            pos_y = const.MARGEN_TABLERO_Y + 30
            
        self.__pantalla__.blit(img_ficha, (pos_x - nuevo_diametro // 2, pos_y - nuevo_diametro // 2))
        
        # Mostrar contador de fichas en casa
        fuente = pygame.font.Font(None, 28)
        texto = fuente.render(str(contador), True, (255, 255, 255))
        self.__pantalla__.blit(texto, (pos_x + const.RADIO_FICHA + 5, pos_y - 10))

    def __dibujar_elementos_ui__(self):
        # Obtener valores de los dados
        dados = self.__juego__.mostrar_dados()
        valores_dados_tupla = dados.obtener_valores()
        
        # Obtener movimientos disponibles para mostrar todos los dados correctamente
        movimientos_disponibles = self.__juego__.obtener_movimientos_disponibles()
        
        jugador_actual = self.__juego__.mostrar_jugador_actual()
        color_jugador = jugador_actual.obtener_color()
        
        # Crear panel compacto para el turno del jugador (arriba, sin tapar tablero)
        panel_y = 5
        panel_altura = 40
        panel_ancho = 350
        panel_x = const.CENTRO_X - panel_ancho // 2
        
        # Fondo del panel con efecto de madera
        panel_rect = pygame.Rect(panel_x, panel_y, panel_ancho, panel_altura)
        pygame.draw.rect(self.__pantalla__, (80, 60, 40), panel_rect, border_radius=8)
        pygame.draw.rect(self.__pantalla__, (218, 165, 32), panel_rect, 2, border_radius=8)
        
        # Imagen de la ficha del jugador (más pequeña)
        img_ficha = self.__assets__["ficha_blanca"] if color_jugador == 'blanco' else self.__assets__["ficha_negra"]
        # Escalar la ficha para que sea más pequeña
        ficha_pequena = pygame.transform.scale(img_ficha, (25, 25))
        ficha_x = panel_x + 10
        ficha_y = panel_y + panel_altura // 2 - 12
        self.__pantalla__.blit(ficha_pequena, (ficha_x, ficha_y))
        
        # Texto del turno con fuente elegante pero compacta
        fuente_nombre = pygame.font.SysFont('georgia', 22, bold=True)
        
        color_texto = (255, 255, 255) if color_jugador == 'blanco' else (50, 50, 50)
        
        # Nombre del jugador directamente
        texto_nombre = fuente_nombre.render(f"Turno: {jugador_actual.obtener_nombre()}", True, color_texto)
        texto_x = ficha_x + 35
        texto_y = panel_y + panel_altura // 2 - texto_nombre.get_height() // 2
        self.__pantalla__.blit(texto_nombre, (texto_x, texto_y))

        # Botón lanzar dados o mostrar dados
        if not valores_dados_tupla[0]:
            if not self.__juego__.verificar_victoria():
                # Color del botón según el jugador
                color_boton = (255, 255, 255) if color_jugador == 'blanco' else (50, 50, 50)
                pygame.draw.rect(
                    self.__pantalla__, color_boton, const.HITBOX_BOTON_LANZAR, border_radius=5
                )
                color_texto_boton = (0, 0, 0) if color_jugador == 'blanco' else (255, 255, 255)
                fuente = pygame.font.Font(None, 36)
                texto = fuente.render("Lanzar", True, color_texto_boton)
                self.__pantalla__.blit(texto, (const.HITBOX_BOTON_LANZAR.centerx - texto.get_width() // 2,
                                              const.HITBOX_BOTON_LANZAR.centery - texto.get_height() // 2))
        else:
            # Mostrar imágenes de dados basándose en movimientos disponibles
            # Si hay 4 movimientos, es doble (mostrar 4 dados)
            # Si hay 2 o menos, mostrar 2 dados normales
            dados_a_mostrar = []
            
            if len(movimientos_disponibles) == 4:
                # Dobles: mostrar 4 dados del mismo valor
                dados_a_mostrar = movimientos_disponibles
            elif len(movimientos_disponibles) > 0:
                # Mostrar los dados restantes
                dados_a_mostrar = movimientos_disponibles
            else:
                # No quedan movimientos pero mostrar los dados originales
                dados_a_mostrar = list(valores_dados_tupla)
            
            # Dibujar los dados
            total_dados = len(dados_a_mostrar)
            x_inicio = const.CENTRO_X - (total_dados * 25)
            for i, valor in enumerate(dados_a_mostrar):
                if valor and valor in self.__assets__["dados"]:
                    img_dado = self.__assets__["dados"][valor]
                    self.__pantalla__.blit(img_dado, (x_inicio + i * 50, const.CENTRO_Y - 20))
            
            # Mostrar botón "Pasar Turno" si no quedan movimientos
            if len(movimientos_disponibles) == 0:
                boton_pasar = pygame.Rect(const.CENTRO_X - 60, const.CENTRO_Y + 40, 120, 40)
                pygame.draw.rect(self.__pantalla__, (200, 100, 100), boton_pasar, border_radius=5)
                fuente = pygame.font.Font(None, 28)
                texto = fuente.render("Pasar Turno", True, (255, 255, 255))
                self.__pantalla__.blit(texto, (boton_pasar.centerx - texto.get_width() // 2,
                                              boton_pasar.centery - texto.get_height() // 2))
                # Guardar el botón para detectar clics
                self.__boton_pasar_turno__ = boton_pasar
            else:
                self.__boton_pasar_turno__ = None

    def __dibujar_resaltados__(self):
        s_seleccionar = pygame.Surface(
            (const.ANCHO_PUNTO, const.ALTO_PUNTO), pygame.SRCALPHA
        )
        s_seleccionar.fill((255, 255, 0, 100))  # Amarillo semi-transparente
        
        s_mover = pygame.Surface(
            (const.ANCHO_PUNTO, const.ALTO_PUNTO), pygame.SRCALPHA
        )
        s_mover.fill((0, 255, 0, 100))  # Verde semi-transparente

        if self.__punto_seleccionado__ is not None:
            if self.__punto_seleccionado__ == 24:  # Barra
                jugador = self.__juego__.mostrar_jugador_actual()
                color = jugador.obtener_color()
                if color == 'blanco':
                    hitbox = const.HITBOX_BARRA_J1
                else:
                    hitbox = const.HITBOX_BARRA_J2
                s_barra = pygame.Surface((hitbox.width, hitbox.height), pygame.SRCALPHA)
                s_barra.fill((255, 255, 0, 100))
                self.__pantalla__.blit(s_barra, hitbox.topleft)
            else:
                # Punto normal
                hitbox = const.HITBOXES_PUNTOS[self.__punto_seleccionado__]
                self.__pantalla__.blit(s_seleccionar, hitbox.topleft)

        for indice_punto in self.__movimientos_posibles__:
            if 0 <= indice_punto <= 23:
                hitbox = const.HITBOXES_PUNTOS[indice_punto]
                self.__pantalla__.blit(s_mover, hitbox.topleft)

    def __dibujar_mensaje_ganador__(self):
        if self.__juego__.verificar_victoria(): 
            ganador = self.__juego__.obtener_ganador() 
            texto = f"¡GANADOR: {ganador.obtener_nombre()}!"
            color = (255, 255, 255) if ganador.obtener_color() == 'blanco' else (50, 50, 50)
            
            overlay = pygame.Surface(
                (const.ANCHO_PANTALLA, const.ALTO_PANTALLA), pygame.SRCALPHA
            )
            overlay.fill((100, 100, 100, 180))
            self.__pantalla__.blit(overlay, (0, 0))
            
            # Dibujar texto de ganador
            fuente_ganador = pygame.font.Font(None, 72)
            texto_renderizado = fuente_ganador.render(texto, True, color)
            self.__pantalla__.blit(texto_renderizado, 
                                  (const.CENTRO_X - texto_renderizado.get_width() // 2,
                                   const.CENTRO_Y - texto_renderizado.get_height() // 2))

    def __dibujar_mensaje_error__(self):
        """
        Muestra un mensaje de error temporal en la parte inferior de la pantalla.
        """
        if self.__mensaje_error__ and pygame.time.get_ticks() - self.__tiempo_error__ < 3000:
            # Crear un recuadro semi-transparente para el mensaje
            ancho_mensaje = 500
            alto_mensaje = 60
            x_mensaje = const.CENTRO_X - ancho_mensaje // 2
            # Posicionar en la parte inferior para no obstruir el juego
            y_mensaje = const.ALTO_PANTALLA - 120
            
            # Fondo del mensaje - color tierra/marrón suave que combina con el tablero
            fondo_error = pygame.Surface((ancho_mensaje, alto_mensaje), pygame.SRCALPHA)
            fondo_error.fill((139, 90, 60, 200))  # Marrón tierra semi-transparente
            self.__pantalla__.blit(fondo_error, (x_mensaje, y_mensaje))
            
            # Borde dorado/amarillo suave para destacar sin ser agresivo
            pygame.draw.rect(self.__pantalla__, (218, 165, 32), 
                           (x_mensaje, y_mensaje, ancho_mensaje, alto_mensaje), 2, border_radius=8)
            
            # Texto del error
            fuente_error = pygame.font.Font(None, 24)
            
            # Dividir el mensaje en múltiples líneas si es muy largo
            palabras = self.__mensaje_error__.split(' ')
            lineas = []
            linea_actual = ""
            
            for palabra in palabras:
                test_linea = linea_actual + palabra + " "
                if fuente_error.size(test_linea)[0] < ancho_mensaje - 20:
                    linea_actual = test_linea
                else:
                    if linea_actual:
                        lineas.append(linea_actual)
                    linea_actual = palabra + " "
            
            if linea_actual:
                lineas.append(linea_actual)
            
            # Dibujar cada línea con color claro para buen contraste
            y_offset = y_mensaje + 12
            for linea in lineas[:2]:  # Máximo 2 líneas
                texto_renderizado = fuente_error.render(linea.strip(), True, (255, 255, 220))
                self.__pantalla__.blit(texto_renderizado, 
                                      (const.CENTRO_X - texto_renderizado.get_width() // 2, y_offset))
                y_offset += 26
        elif pygame.time.get_ticks() - self.__tiempo_error__ >= 3000:
            # Limpiar el mensaje después de 3 segundos
            self.__mensaje_error__ = None

    def __mostrar_error__(self, mensaje):
        """
        Establece un mensaje de error para mostrar en pantalla.
        """
        self.__mensaje_error__ = mensaje
        self.__tiempo_error__ = pygame.time.get_ticks()


    # --- MÉTODOS DE LÓGICA DE EVENTOS (HANDLE) ---

    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1: 
                        self.__manejar_clic__(evento.pos)

            self.__dibujar__()
            pygame.display.flip()
            self.__reloj__.tick(30) 

        pygame.quit()
        sys.exit()

    def __manejar_clic__(self, pos):
        if self.__juego__.verificar_victoria(): 
            return

        # Verificar si se hace clic en el botón de lanzar dados
        dados = self.__juego__.mostrar_dados()
        valores_dados_tupla = dados.obtener_valores()
        
        # Verificar clic en botón "Pasar Turno"
        if self.__boton_pasar_turno__ and self.__boton_pasar_turno__.collidepoint(pos):
            self.__juego__.cambiar_turno()
            self.__punto_seleccionado__ = None
            self.__movimientos_posibles__ = {}
            self.__boton_pasar_turno__ = None
            return
        
        if (not valores_dados_tupla[0]) and const.HITBOX_BOTON_LANZAR.collidepoint(pos):
            self.__juego__.tirar_dados()
            self.__punto_seleccionado__ = None
            self.__movimientos_posibles__ = {}
            return

        if not valores_dados_tupla[0]:
            return

        indice_punto_clic = self.__posicion_a_punto__(pos)
        
        if indice_punto_clic is None: 
            self.__punto_seleccionado__ = None
            self.__movimientos_posibles__ = {}
            return

        if self.__punto_seleccionado__ is not None:
            if indice_punto_clic in self.__movimientos_posibles__:
                # Realizar el movimiento
                try:
                    if self.__punto_seleccionado__ == 24:  # Desde la barra
                        self.__juego__.reincorporar_ficha_desde_barra(indice_punto_clic)
                    elif indice_punto_clic == -1:  # Sacar ficha
                        self.__juego__.sacar_ficha_del_tablero(self.__punto_seleccionado__)
                    else:  # Movimiento normal
                        self.__juego__.mover_ficha(self.__punto_seleccionado__, indice_punto_clic)
                    
                    # Verificar si hay victoria
                    self.__juego__.verificar_victoria()
                    
                    # Limpiar mensaje de error si el movimiento fue exitoso
                    self.__mensaje_error__ = None
                    
                except ValueError as e:
                    # Mostrar el error en pantalla
                    self.__mostrar_error__(str(e))
                except Exception as e:
                    # Otros errores
                    self.__mostrar_error__(f"Error: {str(e)}")
                
                self.__punto_seleccionado__ = None
                self.__movimientos_posibles__ = {}
            else:
                self.__punto_seleccionado__ = None
                self.__movimientos_posibles__ = {}
                self.__intentar_seleccionar_punto__(indice_punto_clic)
        else:
            self.__intentar_seleccionar_punto__(indice_punto_clic)

    def __intentar_seleccionar_punto__(self, indice_punto):
        jugador = self.__juego__.mostrar_jugador_actual()
        
        # Validar si hay fichas en la barra
        if self.__juego__.jugador_actual_tiene_fichas_en_barra():
            if indice_punto != 24:  # Si hay fichas en la barra, SÓLO se puede mover desde la barra
                self.__mostrar_error__("Debes reincorporar primero las fichas desde la barra")
                return 
        
        # Obtener el estado del tablero
        layout_tablero = self.__juego__.obtener_estado_tablero()
        
        # Verificar si el punto tiene fichas del jugador actual
        if indice_punto != 24:
            if indice_punto not in layout_tablero or not layout_tablero[indice_punto]:
                self.__mostrar_error__("No hay fichas en ese punto")
                return
            color_jugador = 'B' if jugador.obtener_color() == 'blanco' else 'N'
            if layout_tablero[indice_punto][0] != color_jugador:
                self.__mostrar_error__("Esa ficha no es tuya")
                return
        
        # Calcular movimientos posibles
        movimientos_posibles = {}
        movimientos_disponibles = self.__juego__.obtener_movimientos_disponibles()
        
        for valor_dado in set(movimientos_disponibles):
            try:
                if indice_punto == 24:  # Desde la barra
                    # Calcular punto de entrada según el color
                    if jugador.obtener_color() == 'blanco':
                        punto_destino = valor_dado - 1  # Puntos 0-5
                    else:
                        punto_destino = 24 - valor_dado  # Puntos 18-23
                    movimientos_posibles[punto_destino] = valor_dado
                else:
                    # Movimiento normal
                    # BLANCAS se mueven HACIA ABAJO (de 23 hacia 0)
                    # NEGRAS se mueven HACIA ARRIBA (de 0 hacia 23)
                    if jugador.obtener_color() == 'blanco':
                        punto_destino = indice_punto - valor_dado  # Blancas: restar
                    else:
                        punto_destino = indice_punto + valor_dado  # Negras: sumar
                    
                    if 0 <= punto_destino <= 23:
                        movimientos_posibles[punto_destino] = valor_dado
                    elif self.__juego__.jugador_puede_sacar_fichas():
                        # Puede sacar ficha
                        movimientos_posibles[-1] = valor_dado  # -1 indica "sacar ficha"
            except Exception as e:
                print(f"Error calculando movimiento: {e}")
        
        if movimientos_posibles:
            self.__punto_seleccionado__ = indice_punto
            self.__movimientos_posibles__ = movimientos_posibles
        else:
            self.__mostrar_error__("No hay movimientos válidos desde ese punto con los dados actuales")

    def __posicion_a_punto__(self, pos):
        jugador = self.__juego__.mostrar_jugador_actual()
        color = jugador.obtener_color()

        for i, hitbox in const.HITBOXES_PUNTOS.items():
            if hitbox.collidepoint(pos):
                return i
        
        if color == 'blanco' and const.HITBOX_BARRA_J1.collidepoint(pos):
            return 24  # 24 representa la barra
        if color == 'negro' and const.HITBOX_BARRA_J2.collidepoint(pos):
            return 24
            
        return None
