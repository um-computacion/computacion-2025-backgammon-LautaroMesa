import pygame
from pygame_ui import constants as const

def click_fuera_destino(pos, color_actual: str):
	"""
	Devuelve -1 si el clic cae en el área 'Fuera' del color actual, de lo contrario None.
	:param pos: (x, y) del clic del mouse
	:param color_actual: 'blanco' o 'negro'
	"""
	if color_actual == 'blanco':
		hit = const.HITBOX_FUERA_BLANCO
	else:
		hit = const.HITBOX_FUERA_NEGRO
	if isinstance(hit, pygame.Rect) and hit.collidepoint(pos):
		return -1
	return None

