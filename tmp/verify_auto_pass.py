import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.game import Game
from core.checker import Ficha

j = Game('A','B')
T = j.obtener_tablero()

# Vaciar tablero y bloquear puntos 0..5 con 2 negras
T.__puntos__ = [[] for _ in range(24)]
for i in range(6):
    T.__puntos__[i] = [Ficha('N'), Ficha('N')]

# Poner una blanca en barra
T.__barra_blanco__.append(Ficha('B'))

print('Antes:', j.mostrar_jugador_actual().obtener_color(), j.mostrar_dados().obtener_valores(), j.obtener_movimientos_disponibles())

j.tirar_dados()

print('Despues:', j.mostrar_jugador_actual().obtener_color(), j.mostrar_dados().obtener_valores(), j.obtener_movimientos_disponibles())
