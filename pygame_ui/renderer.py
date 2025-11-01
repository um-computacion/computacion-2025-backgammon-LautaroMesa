# pygame_ui/render.py
"""
Responsable de toda la lógica de dibujado (la 'Vista').
No debe contener ninguna lógica de juego.
"""

import pygame
from pygame_ui import constants as C 

def draw_board(screen):
    """
    Dibuja el tablero de Backgammon estático (triángulos, barra, etc.).
    """
    screen.fill(C.COLOR_BACKGROUND)

    for i in range(12):
        color = C.COLOR_BOARD_LIGHT if i % 2 == 0 else C.COLOR_BOARD_DARK

        # --- Mitad Superior (Puntos 13-24) ---
        point_x = C.BOARD_MARGIN + (C.POINT_WIDTH * i) + (C.POINT_WIDTH / 2)
        if i >= 6: 
            point_x += C.BAR_WIDTH
            
        base_y = C.BOARD_MARGIN
        base_left_x = point_x - (C.POINT_WIDTH / 2)
        base_right_x = point_x + (C.POINT_WIDTH / 2)
        
        vertices_top = [
            (point_x, C.BOARD_MARGIN + C.POINT_HEIGHT),
            (base_left_x, base_y),
            (base_right_x, base_y)
        ]
        pygame.draw.polygon(screen, color, vertices_top)

        # --- Mitad Inferior (Puntos 1-12) ---
        point_x_bottom = C.WINDOW_WIDTH - point_x
        
        base_y_bottom = C.WINDOW_HEIGHT - C.BOARD_MARGIN
        base_left_x_bottom = point_x_bottom - (C.POINT_WIDTH / 2)
        base_right_x_bottom = point_x_bottom + (C.POINT_WIDTH / 2)

        vertices_bottom = [
            (point_x_bottom, C.WINDOW_HEIGHT - C.BOARD_MARGIN - C.POINT_HEIGHT),
            (base_left_x_bottom, base_y_bottom),
            (base_right_x_bottom, base_y_bottom)
        ]
        pygame.draw.polygon(screen, color, vertices_bottom)

    bar_x = (C.WINDOW_WIDTH - C.BAR_WIDTH) / 2
    bar_rect = (bar_x, C.BOARD_MARGIN, C.BAR_WIDTH, C.WINDOW_HEIGHT - (2 * C.BOARD_MARGIN))
    pygame.draw.rect(screen, C.COLOR_BORDER, bar_rect)

def _get_checker_pos(point_index: int, checker_index: int) -> tuple[int, int]:
    """
    Calcula la coordenada (x, y) exacta para una ficha en un punto.
    :param point_index: Índice del core (0-23)
    :param checker_index: Índice de la ficha en esa pila (0, 1, 2...)
    """
    # Calcula la posición Y (vertical)
    # Si hay más de 5 fichas, se apilan
    stack_index = checker_index
    if checker_index >= 5:
        stack_index = 4 # Apilar a partir de la 5ta ficha
    
    y_pos = 0
    
    if 0 <= point_index <= 11:
        # --- Mitad Inferior (Puntos 1-12 del usuario) ---
        # (Los índices 0-11 del core se dibujan en la fila inferior)
        y_pos = C.WINDOW_HEIGHT - C.BOARD_MARGIN - C.CHECKER_RADIUS - (stack_index * (C.CHECKER_RADIUS * 2 + C.CHECKER_SPACING))
    else:
        # --- Mitad Superior (Puntos 13-24 del usuario) ---
        # (Los índices 12-23 del core se dibujan en la fila superior)
        y_pos = C.BOARD_MARGIN + C.CHECKER_RADIUS + (stack_index * (C.CHECKER_RADIUS * 2 + C.CHECKER_SPACING))

    # Calcula la posición X (horizontal)
    # Esta lógica mapea los índices 0-23 a la posición visual correcta
    x_pos = 0
    if 0 <= point_index <= 5:
        # Puntos 1-6 (inferior derecha)
        i = 11 - point_index
        x_pos = C.BOARD_MARGIN + (C.POINT_WIDTH * i) + (C.POINT_WIDTH / 2) + C.BAR_WIDTH
    elif 6 <= point_index <= 11:
        # Puntos 7-12 (inferior izquierda)
        i = 11 - point_index
        x_pos = C.BOARD_MARGIN + (C.POINT_WIDTH * i) + (C.POINT_WIDTH / 2)
    elif 12 <= point_index <= 17:
        # Puntos 13-18 (superior izquierda)
        i = point_index - 12
        x_pos = C.BOARD_MARGIN + (C.POINT_WIDTH * i) + (C.POINT_WIDTH / 2)
    else: 
        # Puntos 19-24 (superior derecha)
        i = point_index - 12
        x_pos = C.BOARD_MARGIN + (C.POINT_WIDTH * i) + (C.POINT_WIDTH / 2) + C.BAR_WIDTH
        
    return (int(x_pos), int(y_pos))

def draw_checkers(screen, board_state: dict):
    """
    Dibuja todas las fichas en el tablero según el estado del juego.
    para board_state: El diccionario {indice: ['B', 'B']} del core.Game
    """
    for point_index, checkers_list in board_state.items():
        if not checkers_list:
            continue
            
        # Determina el color de la ficha
        checker_color_str = checkers_list[0]
        color = C.COLOR_WHITE_CHECKER if checker_color_str == 'B' else C.COLOR_BLACK_CHECKER
        
        # Dibuja cada ficha en la pila
        for i, checker in enumerate(checkers_list):
            (x, y) = _get_checker_pos(point_index, i)
            
            # Dibuja la ficha
            pygame.draw.circle(screen, color, (x, y), C.CHECKER_RADIUS)
            # Dibuja el borde de la ficha
            pygame.draw.circle(screen, C.COLOR_BORDER, (x, y), C.CHECKER_RADIUS, 2)