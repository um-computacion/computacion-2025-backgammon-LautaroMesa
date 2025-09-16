from core.player import Player
from core.board import Tablero
from core.dice import Dado 

class game:
    # En esta clase se representa el juego en si del backgammon 
    def __init__(self, __nombre__jugador1__, __nombre__jugador2__):
        # Inicializa el juego con dos jugadores y un tablero.
        # para __nombre__jugador1__: nombre del primer jugador
        # para __nombre__jugador2__: nombre del segundo jugador
    
        self.__jugador1__ = Player(__nombre__jugador1__, "blanco")
        self.__jugador2__ = Player(__nombre__jugador2__, "Negro")
        self.__tablero__ = Tablero()
        self.__dado1__ = Dado()
        self.__dado2__ = Dado() 
        self.__turno__ = self.__jugador1__  # Indica de que el jugador 1 empieza porque es la ficha blanca
        self.__turno__.establecer_turno(True)   # El jugador 1 (blanco) empieza
        self.__jugador2__.establecer_turno(False)  # El jugador 2

    