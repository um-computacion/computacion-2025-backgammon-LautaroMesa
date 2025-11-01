import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.game import Game
from core.checker import Ficha

j = Game('A','B')
T = j.obtener_tablero()

# Limpiar tablero
T.__puntos__ = [[] for _ in range(24)]
T.__barra_blanco__ = []
T.__barra_negro__ = []

# Colocar 2 fichas blancas: una fuera de casa (idx 10) y una en idx 0
T.__puntos__[10] = [Ficha('B')]  # punto 11
T.__puntos__[0] = [Ficha('B')]   # punto 1

# Bloquear para blancas todos los posibles destinos desde idx 0 y 10 con d=1..6
# Para idx 0 -> bloquear 1..6 (idx 1..6)
for i in range(1, 7):
    T.__puntos__[i] = [Ficha('N'), Ficha('N')]
# Para idx 10 -> bloquear 11..16 (idx 11..16)
for i in range(11, 17):
    T.__puntos__[i] = [Ficha('N'), Ficha('N')]

print('Antes:', j.mostrar_jugador_actual().obtener_color(), j.obtener_movimientos_disponibles())
res = j.tirar_dados()
print('Dados:', res)
print('Despues:', j.mostrar_jugador_actual().obtener_color(), j.obtener_movimientos_disponibles())

# Consultar motivo del auto-pase
try:
    motivo = j.consumir_motivo_auto_pase()
except Exception:
    motivo = None
print('Motivo auto-pase:', motivo)
