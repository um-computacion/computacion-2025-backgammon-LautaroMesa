from core.player import Player
from core.board import Tablero
from core.dice import Dado 

class Game:
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
    def capturar_ficha_enemiga(self, __punto__):
        # Captura una ficha enemiga en un punto especifico
        # __punto__: Punto donde capturar la ficha (0-23)
        # return: True si se capturó, False si no.   
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        
        try:
            # Usar el método capturar_ficha de Tablero
            self.__tablero__.capturar_ficha(__punto__, color)
            print(f"Ficha enemiga capturada en punto {__punto__}")
            return True
        except ValueError as e:
            print(f"No se pude capturar: {e}")
            return False

    def reincorporar_ficha_desde_barra(self, __punto__):
        # Reincorpora una ficha desde la barra al tablero
        # __punto__: es el punto donde se debe reincorporar la ficha (0-23)
        # return: True si se reincorporó, False si no
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        
        try:
            # Usar el método reincorporar_ficha de Tablero
            self.__tablero__.reincorporar_ficha(color, __punto__)
            print(f"Ficha reincorporada desde la barra al punto {__punto__}")
            return True
        except ValueError as e:
            print(f"No se pudo reincorporar: {e}")
            return False
    def sacar_ficha_del_tablero(self, __origen__):
        # Saca una ficha del tablero cuando llega al final
        # __origen__: Punto de origen (0-23)
        # return: True si se sacó, False si no
        
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        
        try:
            # Usar el método sacar_ficha de Tablero
            self.__tablero__.sacar_ficha(__origen__, color)
            print(f"Ficha sacada del tablero desde punto {__origen__}")
            return True
        except ValueError as e:
            print(f"No se pudo sacar la ficha: {e}")
            return False

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
    def obtener_estado_tablero(self):
        
        # Obtiene el estado actual del tablero para visualización.
        '''
        Este método expone el estado del tablero de forma controlada,
        permitiendo que las interfaces (CLI, Pygame) accedan a la información
        sin romper el encapsulamiento.
        '''        
        estado = self.__tablero__.obtener_estado()
        estado_dict = {}
        
        for i, punto in enumerate(estado):
            if punto:  # Solo incluir puntos que tienen fichas
                estado_dict[i] = punto
                
        return estado_dict

    def mostrar_tablero_consola(self):
        """
        Muestra el tablero en consola usando el método del tablero.
        """
        self.__tablero__.mostrar_tablero()