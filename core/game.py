
from core.player import Player
from core.board import Tablero
from core.dice import Dado 
from typing import Optional

class Game:
    """
    Representa el juego en si del backgammon.
    """
    
    def __init__(self, nombre_jugador1, nombre_jugador2):
        self.__jugador1__ = Player(nombre_jugador1, "blanco")
        self.__jugador2__ = Player(nombre_jugador2, "negro")
        self.__tablero__ = Tablero()
        self.__dados__ = Dado()
        self.__turno_actual__ = self.__jugador1__
        self.__juego_terminado__ = False
        self.__ganador__ = None
        self.__movimientos_disponibles__ = []

    def mostrar_jugador1(self):
        return self.__jugador1__
    
    def mostrar_jugador2(self):
        return self.__jugador2__ 
    
    def mostrar_jugador_actual(self):
        return self.__turno_actual__
    
    def mostrar_dados(self):
        return self.__dados__
     
    def cambiar_turno(self):
        if self.__turno_actual__ == self.__jugador1__:
            self.__turno_actual__ = self.__jugador2__
        else:
            self.__turno_actual__ = self.__jugador1__
        
        self.__dados__.reiniciar()
        self.__movimientos_disponibles__.clear()
            
    def tirar_dados(self):
        (v1, v2) = self.__dados__.tirar()
        
        if self.__dados__.es_doble():
            self.__movimientos_disponibles__ = [v1, v1, v1, v1]
        else:
            self.__movimientos_disponibles__ = [v1, v2]
   
        return (v1, v2)

    def mover_ficha(self, origen, destino):
        if self.__juego_terminado__:
            raise ValueError("El juego ya ha terminado.")
            
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'

        if self.jugador_actual_tiene_fichas_en_barra():
            raise ValueError("Debe reincorporar todas las fichas desde la barra primero.")

        if color == 'B' and destino >= origen:
            raise ValueError("Inválido: Fichas 'B' solo pueden moverse a puntos menores.")
        if color == 'N' and destino <= origen:
            raise ValueError("Inválido: Fichas 'N' solo pueden moverse a puntos mayores.")

        distancia = abs(destino - origen)
        
        if distancia not in self.__movimientos_disponibles__:
            raise ValueError(f"Movimiento de {distancia} no está permitido por los dados: {self.__movimientos_disponibles__}")

        # (El chequeo de bloqueo ahora lo hace 'mover_ficha' del tablero)
        
        self.__tablero__.mover_ficha(origen, destino, color)
        self.__movimientos_disponibles__.remove(distancia)

    def reincorporar_ficha_desde_barra(self, punto):
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'

        if not self.jugador_actual_tiene_fichas_en_barra():
            raise ValueError("No tiene fichas en la barra para reincorporar.")
            
        dado_necesario = 0
        
        if color == 'B':
            if not (0 <= punto <= 5):
                raise ValueError("Fichas 'B' solo pueden reincorporarse en puntos 0-5.")
            dado_necesario = punto + 1
        else: 
            if not (18 <= punto <= 23):
                raise ValueError("Fichas 'N' solo pueden reincorporarse en puntos 18-23.")
            dado_necesario = 24 - punto
            
        if dado_necesario not in self.__movimientos_disponibles__:
            raise ValueError(f"Reingreso al punto {punto} (necesita dado {dado_necesario}) no está permitido por los dados: {self.__movimientos_disponibles__}")
        # (El chequeo de bloqueo ahora lo hace 'reincorporar_ficha' del tablero)

        self.__tablero__.reincorporar_ficha(color, punto)
        self.__movimientos_disponibles__.remove(dado_necesario)

    def sacar_ficha_del_tablero(self, origen):
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        
        if self.jugador_actual_tiene_fichas_en_barra():
            raise ValueError("Debe reincorporar todas las fichas desde la barra primero.")
        
        if not self.__tablero__.todas_las_fichas_en_casa(color):
            raise ValueError("No se pueden sacar fichas hasta que todas estén en casa.")
            
        dado_necesario = 0
        if color == 'B':
            if not (18 <= origen <= 23):
                raise ValueError("Fichas 'B' solo pueden sacarse desde puntos 18-23.")
            dado_necesario = 24 - origen
        else:
            if not (0 <= origen <= 5):
                raise ValueError("Fichas 'N' solo pueden sacarse desde puntos 0-5.")
            dado_necesario = origen + 1

        dado_a_usar = None
        
        if dado_necesario in self.__movimientos_disponibles__:
            dado_a_usar = dado_necesario
        else:
            dados_mayores_validos = [d for d in self.__movimientos_disponibles__ if d > dado_necesario]
            
            if dados_mayores_validos:
                farthest_point_idx = self.__tablero__._get_farthest_checker_in_home(color)
                
                if farthest_point_idx is None:
                     raise ValueError("Error lógico: La casa está vacía pero se intenta sacar una ficha.")

                if farthest_point_idx == origen:
                    dado_a_usar = min(dados_mayores_validos)
                else:
                    raise ValueError(f"No se puede usar un dado mayor en el punto {origen+1} porque hay fichas más lejanas.")
            else:
                raise ValueError(f"Sacar del punto {origen} (necesita dado {dado_necesario}) no está permitido por los dados: {self.__movimientos_disponibles__}")

        self.__tablero__.sacar_ficha(origen, color)
        self.__movimientos_disponibles__.remove(dado_a_usar)

    def verificar_victoria(self):
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
        return self.__ganador__

    def obtener_estado_tablero(self):
        estado = self.__tablero__.obtener_estado() 
        estado_dict = {}
        
        for i, punto in enumerate(estado):
            if punto:
                estado_dict[i] = punto
                 
        return estado_dict

    def mostrar_tablero_consola(self):
        self.__tablero__.mostrar_tablero()

    def jugador_actual_tiene_fichas_en_barra(self):
        color_jugador = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        return self.__tablero__.obtener_fichas_barra(color_jugador) > 0
        
    def obtener_movimientos_disponibles(self):
        return self.__movimientos_disponibles__

    def jugador_puede_sacar_fichas(self) -> bool:
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        
        if self.jugador_actual_tiene_fichas_en_barra():
            return False
        if not self.__tablero__.todas_las_fichas_en_casa(color):
            return False
            
        return True

    def obtener_tablero(self):
        """
        Devuelve la instancia del tablero.
        Útil para la interfaz gráfica.
        """
        return self.__tablero__

    
    