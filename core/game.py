from core.player import Player
from core.board import Tablero
from core.dice import Dado 

class Game:

    # Representa el juego en si del backgammon.
    # (Versión refactorizada con validación de dados y dirección)
    # Es la clase principal que dirige el flujo del juego.
    
    
    def __init__(self, nombre_jugador1, nombre_jugador2):
        """
        Inicializa el juego con dos jugadores y un tablero.
        
        param nombre_jugador1: nombre del primer jugador (jugará con 'blanco')
        nombre_jugador2: nombre del segundo jugador (jugará con 'negro')
        """
        self.__jugador1__ = Player(nombre_jugador1, "blanco")
        self.__jugador2__ = Player(nombre_jugador2, "negro")
        self.__tablero__ = Tablero()
        self.__dados__ = Dado()
        self.__turno_actual__ = self.__jugador1__
        self.__juego_terminado__ = False
        self.__ganador__ = None
        
        self.__movimientos_disponibles__ = []

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
        
        self.__dados__.reiniciar()
        self.__movimientos_disponibles__.clear()
            
    def tirar_dados(self):
        """
        Tira los dados, los imprime y almacena los movimientos disponibles.
        return: Tupla con los valores de ambos dados.
        """
        (v1, v2) = self.__dados__.tirar()
        
        if self.__dados__.es_doble():
            self.__movimientos_disponibles__ = [v1, v1, v1, v1]
        else:
            self.__movimientos_disponibles__ = [v1, v2]
            
        return (v1, v2)

    def mover_ficha(self, origen, destino):
        """
        Mueve una ficha validando estado, dados y DIRECCIÓN.
        """
        if self.__juego_terminado__:
            raise ValueError("El juego ya ha terminado.")
            
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'

        # 1. Validación de Estado (Barra)
        if self.jugador_actual_tiene_fichas_en_barra():
            raise ValueError("Debe reincorporar todas las fichas desde la barra primero.")

        # --- VALIDACIÓN DE DIRECCIÓN ---
        if color == 'B' and destino >= origen:
            raise ValueError("Inválido: Fichas 'B' solo pueden moverse a puntos menores.")
        if color == 'N' and destino <= origen:
            raise ValueError("Inválido: Fichas 'N' solo pueden moverse a puntos mayores.")
        # --- FIN DE VALIDACIÓN DE DIRECCIÓN ---

        # 2. Validación de Dados
        distancia = abs(destino - origen)
        
        if distancia not in self.__movimientos_disponibles__:
            raise ValueError(f"Movimiento de {distancia} no está permitido por los dados: {self.__movimientos_disponibles__}")

        # Si todo es válido, mover
        self.__tablero__.mover_ficha(origen, destino, color)
        
        # "Gastar" el dado
        self.__movimientos_disponibles__.remove(distancia)

    def reincorporar_ficha_desde_barra(self, punto):
        """
        Reincorpora una ficha validando contra los dados.
        """
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'

        if not self.jugador_actual_tiene_fichas_en_barra():
            raise ValueError("No tiene fichas en la barra para reincorporar.")
            
        # Validación de Dados
        dado_necesario = 0
        
        # --- VALIDACIÓN DE DIRECCIÓN Y CUADRANTE ---
        if color == 'B':
            if not (0 <= punto <= 5):
                raise ValueError("Fichas 'B' solo pueden reincorporarse en puntos 0-5.")
            dado_necesario = punto + 1
        else: # color == 'N'
            if not (18 <= punto <= 23):
                raise ValueError("Fichas 'N' solo pueden reincorporarse en puntos 18-23.")
            dado_necesario = 24 - punto # pragma: no cover
        # --- FIN DE VALIDACIÓN DE DIRECCIÓN ---
            
        if dado_necesario not in self.__movimientos_disponibles__:
            raise ValueError(f"Reingreso al punto {punto} (necesita dado {dado_necesario}) no está permitido por los dados: {self.__movimientos_disponibles__}")

        self.__tablero__.reincorporar_ficha(color, punto)
        self.__movimientos_disponibles__.remove(dado_necesario)

    def sacar_ficha_del_tablero(self, origen):
        """
        Saca una ficha del tablero (cuando llega al final).
        """
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        
        if self.jugador_actual_tiene_fichas_en_barra():
            raise ValueError("Debe reincorporar todas las fichas desde la barra primero.")
            
        dado_necesario = 0
        if color == 'B':
            if not (18 <= origen <= 23):
                raise ValueError("Fichas 'B' solo pueden sacarse desde puntos 18-23.")
            dado_necesario = 24 - origen
        else:
            if not (0 <= origen <= 5):
                raise ValueError("Fichas 'N' solo pueden sacarse desde puntos 0-5.")
            dado_necesario = origen + 1

        if dado_necesario not in self.__movimientos_disponibles__:
            raise ValueError(f"Sacar del punto {origen} (necesita dado {dado_necesario}) no está permitido por los dados: {self.__movimientos_disponibles__}")

        self.__tablero__.sacar_ficha(origen, color)
        self.__movimientos_disponibles__.remove(dado_necesario)

    def verificar_victoria(self): 
        """
        Verifica si hay un ganador en el juego.
        Si hay ganador, actualiza el estado interno del juego.
        
        return: True si el juego terminó, False si continúa.
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
        return: Objeto Player del ganador, o None si hay.
        """
        return self.__ganador__

    def obtener_estado_tablero(self):
        """
        Obtiene el estado actual del tablero para visualización.
        Lo devuelve en formato de diccionario para la UI.
        
        return: Diccionario {indice_punto: [fichas]}
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
        
        return: True si tiene fichas, False si no.
        """
        color_jugador = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        # Delega la consulta al tablero
        return self.__tablero__.obtener_fichas_barra(color_jugador) > 0
     
    def obtener_movimientos_disponibles(self):
        """
        Devuelve la lista de dados/movimientos que quedan por usar.
        """
        return self.__movimientos_disponibles__