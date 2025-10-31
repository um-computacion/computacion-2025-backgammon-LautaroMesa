# main_pygame.py

import sys
# Añadir el directorio raíz al path para que Python
# pueda encontrar los módulos 'core' y 'pygame_ui'
sys.path.append('.')

from pygame_ui.ui import InterfazPygame

if __name__ == "__main__":
    """
    Punto de entrada para la versión Pygame del juego.
    """
    
    # Validar que Pygame esté instalado
    try:
        import pygame
    except ImportError:
        print("Error: El módulo 'pygame' no está instalado.")
        print("Por favor, instálalo ejecutando: pip install pygame")
        sys.exit(1)
    
    # Crear y ejecutar la interfaz de usuario
    # Los nombres se pedirán mediante la interfaz gráfica
    ui_juego = InterfazPygame()
    ui_juego.ejecutar()