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
        self.__jugador2__ = Player(__nombre__jugador2__, "negro")
        self.__tablero__ = Tablero()
        self.__dados__ = Dado()  # Un solo objeto Dado que maneja ambos dados
        self.__turno_actual__ = self.__jugador1__  # El jugador 1 empieza el juego porque tiene las fichas blancas
        self.__juego_terminado__ = False
        self.__ganador__ = None

    def mostrar_jugador1(self):
        return self.__jugador1__
    
    def mostrar_jugador2(self):
        return self.__jugador2__ 
    
    def mostrar_jugador_actual(self):
        #Devuelve el jugador que tiene el turno actual
        
        return self.__turno_actual__
    def mostrar_dados(self):
        # Se devuelve el dado para empezar el juego 
        return self.__dados__
    
    def cambiar_turno(self):
       #Cambia el turno al siguiente jugador 
        if self.__turno_actual__ == self.__jugador1__:
            self.__turno_actual__ = self.__jugador2__
        else:
            self.__turno_actual__ = self.__jugador1__
    def tirar_dados(self):
        # Tira los dados para el turno actual
        
        
        return self.__dados__.tirar()   # return: Tupla con los valores de ambos dados
    def mover_ficha(self, __origen__, __destino__):
        # Mueve una ficha en el tablero para el jugador actual.
        #__origen__: Punto de origen (0-23).
        #__destino__: Punto de destino (0-23).

        if self.__juego_terminado__:
            raise ValueError("El juego ya ha terminado.")
        
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        self.__tablero__.mover_ficha(__origen__, __destino__, color)
    
    def verificar_victoria(self):
        
        # Verifica si hay un ganador en el juego
        # return: True si el juego terminó, False si continúa
        
        if self.__tablero__.hay_ganador('B'):
            self.__juego_terminado__ = True
            self.__ganador__ = self.__jugador1__
            return True
        elif self.__tablero__.hay_ganador('N'):
            self.__juego_terminado__ = True
            self.__ganador__ = self.__jugador2__
            return True
        
        return False
    def obtener_ganador(self):
        # Devuelve el jugador ganador si el juego ya se termino 
        return self.__ganador__