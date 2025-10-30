from core.player import Player
from core.board import Tablero
from core.dice import Dado 

class Game:
    """
    Representa el juego en si del backgammon.
    (Versión refactorizada)
    Es la clase principal que dirige el flujo del juego.
    """
    
    def __init__(self, nombre_jugador1, nombre_jugador2):
        """
        Inicializa el juego con dos jugadores y un tablero.
        
        :param nombre_jugador1: nombre del primer jugador (jugará con 'blanco')
        :param nombre_jugador2: nombre del segundo jugador (jugará con 'negro')
        """
        self.__jugador1__ = Player(nombre_jugador1, "blanco")
        self.__jugador2__ = Player(nombre_jugador2, "negro")
        self.__tablero__ = Tablero() # Usa el Tablero refactorizado
        self.__dados__ = Dado()
        self.__turno_actual__ = self.__jugador1__
        self.__juego_terminado__ = False
        self.__ganador__ = None

    def mostrar_jugador1(self):
        """Devuelve el objeto Player del jugador 1."""
        return self.__jugador1__
    
    def mostrar_jugador2(self):
        """Devuelve el objeto Player del jugador 2."""
        return self.__jugador2__ 
    
    def mostrar_jugador_actual(self):
        """Devuelve el objeto Player que tiene el turno actual."""
        return self.__turno_actual__
    
    def mostrar_dados(self):
        """Devuelve el objeto Dado del juego."""
        return self.__dados__
     
    def cambiar_turno(self):
        """Cambia el turno al siguiente jugador."""
        if self.__turno_actual__ == self.__jugador1__:
            self.__turno_actual__ = self.__jugador2__
        else:
            self.__turno_actual__ = self.__jugador1__
            
    def tirar_dados(self):
        """
        Tira los dados para el turno actual.
        :return: Tupla con los valores de ambos dados.
        """
        return self.__dados__.tirar()

    def mover_ficha(self, origen, destino):
        """
        Mueve una ficha en el tablero para el jugador actual.
        Delega la lógica (incluida la captura) al Tablero.
        
        :param origen: Punto de origen (0-23).
        :param destino: Punto de destino (0-23).
        """
        if self.__juego_terminado__:
            raise ValueError("El juego ya ha terminado.")
        
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        self.__tablero__.mover_ficha(origen, destino, color)

    def reincorporar_ficha_desde_barra(self, punto):
        """
        Reincorpora una ficha desde la barra al tablero.
        
        :param punto: Punto donde se debe reincorporar la ficha (0-23).
        :return: True si se reincorporó, False si no.
        """
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        
        try:
            self.__tablero__.reincorporar_ficha(color, punto)
            print(f"Ficha reincorporada desde la barra al punto {punto}")
            return True
        except ValueError as e:
            print(f"No se pudo reincorporar: {e}")
            return False

    def sacar_ficha_del_tablero(self, origen):
        """
        Saca una ficha del tablero cuando llega al final.
        
        :param origen: Punto de origen (0-23).
        :return: True si se sacó, False si no.
        """
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        
        try:
            self.__tablero__.sacar_ficha(origen, color)
            print(f"Ficha sacada del tablero desde punto {origen}")
            return True
        except ValueError as e:
            print(f"No se pudo sacar la ficha: {e}")
            return False

    def verificar_victoria(self):
        """
        Verifica si hay un ganador en el juego.
        Si hay ganador, actualiza el estado interno del juego.
        
        :return: True si el juego terminó, False si continúa.
        """
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
        """
        Devuelve el jugador ganador si el juego ya se termino.
        :return: Objeto Player del ganador, o None si no hay.
        """
        return self.__ganador__

    def obtener_estado_tablero(self):
        """
        Obtiene el estado actual del tablero para visualización.
        Lo devuelve en formato de diccionario para la UI.
        
        :return: Diccionario {indice_punto: [fichas]}
        """
        estado = self.__tablero__.obtener_estado() 
        estado_dict = {}
        
        for i, punto in enumerate(estado):
            if punto: # Solo incluir puntos que tienen fichas
                estado_dict[i] = punto
                 
        return estado_dict

    def mostrar_tablero_consola(self):
        """
        Muestra el tablero en consola usando el método del tablero.
        """
        self.__tablero__.mostrar_tablero()

    def jugador_actual_tiene_fichas_en_barra(self):
        """
        Verifica si el jugador actual tiene fichas en la barra.
        Esencial para la lógica de turnos.
        
        :return: True si tiene fichas, False si no.
        """
        color_jugador = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        # Delega la consulta al tablero
        return self.__tablero__.obtener_fichas_barra(color_jugador) > 0