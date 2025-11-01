from core.player import Player
from core.board import Tablero
from core.dice import Dado 
from typing import Optional

class Game:
    """
    Representa el juego en si del backgammon.
    (Versión estable con reglas de 'Dado Mayor' y 'Todos en Casa')
    """
    
    def __init__(self, nombre_jugador1, nombre_jugador2):
        """
        Inicializa el juego con dos jugadores y un tablero.
        """
        self.__jugador1__ = Player(nombre_jugador1, "blanco")
        self.__jugador2__ = Player(nombre_jugador2, "negro")
        self.__tablero__ = Tablero()
        self.__dados__ = Dado()
        self.__turno_actual__ = self.__jugador1__
        self.__juego_terminado__ = False
        self.__ganador__ = None
        self.__movimientos_disponibles__ = []
        self.__ultimo_auto_pase__: Optional[str] = None  # 'barra-bloqueada' | 'sin-movimientos' | None

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
        Tira los dados y almacena los movimientos disponibles.
        """
        (v1, v2) = self.__dados__.tirar()
        
        if self.__dados__.es_doble():
            self.__movimientos_disponibles__ = [v1, v1, v1, v1]
        else:
            self.__movimientos_disponibles__ = [v1, v2]
            
        # 1) Si el jugador tiene fichas en barra y no puede reingresar con NINGUNO de los dados,
        #    se pasa automáticamente el turno (regla solicitada por UI).
        if self.__auto_pasar_si_barra_bloqueada__():
            return (v1, v2)

        # 2) Si no hay fichas en barra pero igualmente no existe NI UN movimiento legal
        #    (mover dentro del tablero o sacar en casa), pasar el turno.
        self.__auto_pasar_si_sin_movimientos__()

        return (v1, v2)

    def __auto_pasar_si_barra_bloqueada__(self) -> bool:
        """
        Si el jugador actual tiene fichas en la barra y todos los puntos de reingreso
        que marcan los dados están bloqueados (2+ fichas rivales), pasa el turno
        automáticamente. Devuelve True si se pasó el turno.
        """
        if not self.jugador_actual_tiene_fichas_en_barra():
            return False
        if not self.__movimientos_disponibles__:
            return False

        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        estado = self.__tablero__.obtener_estado()  # lista de listas de 'B'/'N'

        # Para cada valor de dado disponible, calcular punto de entrada
        # Blancas reingresan en 0..5 con punto = dado-1
        # Negras reingresan en 18..23 con punto = 24-dado
        def punto_entrada(dado: int) -> int:
            if color == 'B':
                return dado - 1
            else:
                return 24 - dado

        # ¿Existe al menos un reingreso legal?
        for d in set(self.__movimientos_disponibles__):
            p = punto_entrada(d)
            if p < 0 or p > 23:
                continue
            pila = estado[p]
            # Bloqueado sólo si hay 2+ del rival
            if len(pila) >= 2 and pila[-1] != color:
                # bloqueado para este dado
                continue
            # Si len==0, len==1 (blot rival) o hay propias, es legal
            return False

        # Si ningún dado permite reingresar, pasar turno automáticamente
        # Marcar motivo y pasar turno
        self.__ultimo_auto_pase__ = 'barra-bloqueada'
        self.cambiar_turno()
        return True

    # Método público por si se quiere invocar manualmente desde una UI/CLI
    def auto_pasar_si_barra_bloqueada(self) -> bool:
        """Wrapper público de __auto_pasar_si_barra_bloqueada__."""
        return self.__auto_pasar_si_barra_bloqueada__()

    def __auto_pasar_si_sin_movimientos__(self) -> bool:
        """
        Si no existe ningún movimiento legal con los dados actuales (sin depender de estar en barra),
        pasa el turno automáticamente. Devuelve True si se pasó el turno.
        """
        if not self.__movimientos_disponibles__:
            return False

        if self.__hay_movimiento_legal__():
            return False

        self.__ultimo_auto_pase__ = 'sin-movimientos'
        self.cambiar_turno()
        return True

    def __hay_movimiento_legal__(self) -> bool:
        """
        Verifica si existe al menos un movimiento legal con los dados actuales:
        - Reingreso desde barra si aplica
        - Movimiento normal respetando dirección y bloqueos
        - Sacar ficha (si todas en casa) con dado exacto o 'dado mayor' (solo si es la más alejada)
        """
        movs = set(self.__movimientos_disponibles__)
        if not movs:
            return False

        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        estado = self.__tablero__.obtener_estado()

        # 1) Si hay fichas en barra, basta con que exista un reingreso legal
        if self.jugador_actual_tiene_fichas_en_barra():
            def punto_entrada(dado: int) -> int:
                return (dado - 1) if color == 'B' else (24 - dado)
            for d in movs:
                p = punto_entrada(d)
                if 0 <= p <= 23:
                    pila = estado[p]
                    if not (len(pila) >= 2 and pila and pila[-1] != color):
                        return True
            return False
        puede_sacar = self.jugador_puede_sacar_fichas()
        farthest = None
        if puede_sacar:
            farthest = self.__tablero__._get_farthest_checker_in_home(color)

        for i in range(24):
            pila = estado[i]
            if not pila or pila[-1] != color:
                continue

            for d in movs:
                # Dirección correcta: Blancas hacia índices menores; Negras hacia mayores
                destino = (i - d) if color == 'B' else (i + d)

                # Movimiento dentro del tablero
                if 0 <= destino <= 23:
                    dest_pila = estado[destino]
                    if len(dest_pila) >= 2 and dest_pila and dest_pila[-1] != color:
                        continue
                    # No bloqueado -> es legal
                    return True

                # Intento de sacar ficha (fuera del 0..23)
                if not puede_sacar:
                    continue

                if color == 'B':
                    # Para blancas, sacar desde i requiere dado exacto 24 - i
                    dado_necesario = 24 - i
                else:
                    # Para negras, sacar desde i requiere dado exacto i + 1
                    dado_necesario = i + 1

                if d == dado_necesario:
                    return True
                if d > dado_necesario and farthest is not None and farthest == i:
                    return True

        return False

    def consumir_motivo_auto_pase(self) -> Optional[str]:
        """Devuelve y limpia el último motivo de auto-pase si existiera."""
        motivo = self.__ultimo_auto_pase__
        self.__ultimo_auto_pase__ = None
        return motivo

    def mover_ficha(self, origen, destino):
        """
        Mueve una ficha validando estado, dados y DIRECCIÓN.
        """
        if self.__juego_terminado__:
            raise ValueError("El juego ya ha terminado.")
            
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'

        if self.jugador_actual_tiene_fichas_en_barra():
            raise ValueError("Debe reincorporar todas las fichas desde la barra primero.")

        # --- DIRECCIÓN ESPERADA POR TESTS ---
        # Blancas ('B') deben moverse a puntos MENORES (23 -> 0)
        # Negras  ('N') deben moverse a puntos MAYORES (0  -> 23)
        if color == 'B' and destino >= origen:
            raise ValueError("Inválido: Fichas 'B' solo pueden moverse a puntos menores.")
        if color == 'N' and destino <= origen:
            raise ValueError("Inválido: Fichas 'N' solo pueden moverse a puntos mayores.")

        distancia = abs(destino - origen)
        
        if distancia not in self.__movimientos_disponibles__:
            raise ValueError(f"Movimiento de {distancia} no está permitido por los dados: {self.__movimientos_disponibles__}")

        self.__tablero__.mover_ficha(origen, destino, color)
        self.__movimientos_disponibles__.remove(distancia)

    def reincorporar_ficha_desde_barra(self, punto):
        """
        Reincorpora una ficha validando contra los dados.
        """
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'

        if not self.jugador_actual_tiene_fichas_en_barra():
            raise ValueError("No tiene fichas en la barra para reincorporar.")
            
        dado_necesario = 0
        
        # --- REINCORPORACIÓN (según tests) ---
        if color == 'B':
            # Blancas reingresan en 0-5 (puntos 1..6)
            if not (0 <= punto <= 5):
                raise ValueError("Fichas 'B' solo pueden reincorporarse en puntos 0-5.")
            dado_necesario = punto + 1
        else: 
            # Negras reingresan en 18-23 (puntos 19..24)
            if not (18 <= punto <= 23):
                raise ValueError("Fichas 'N' solo pueden reincorporarse en puntos 18-23.")
            dado_necesario = 24 - punto
            
        if dado_necesario not in self.__movimientos_disponibles__:
            raise ValueError(f"Reingreso al punto {punto} (necesita dado {dado_necesario}) no está permitido por los dados: {self.__movimientos_disponibles__}")

        self.__tablero__.reincorporar_ficha(color, punto)
        self.__movimientos_disponibles__.remove(dado_necesario)

    def sacar_ficha_del_tablero(self, origen):
        """
        Saca una ficha del tablero validando 'Todos en Casa' y 'Dado Mayor'.
        """
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        
        if self.jugador_actual_tiene_fichas_en_barra():
            raise ValueError("Debe reincorporar todas las fichas desde la barra primero.")
        
        if not self.__tablero__.todas_las_fichas_en_casa(color):
            raise ValueError("No se pueden sacar fichas hasta que todas estén en casa.")
            
        dado_necesario = 0
        
        # --- SACAR FICHA (según tests) ---
        if color == 'B':
            # Blancas (casa 18..23), salen hacia 24
            if not (18 <= origen <= 23):
                raise ValueError("Fichas 'B' solo pueden sacarse desde puntos 18-23.")
            dado_necesario = 24 - origen
        else:
            # Negras (casa 0..5), salen hacia 0
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
        """
        Verifica si hay un ganador en el juego.
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
        """
        return self.__ganador__

    def obtener_estado_tablero(self):
        """
        Obtiene el estado actual del tablero para visualización.
        """
        estado = self.__tablero__.obtener_estado() 
        estado_dict = {}
        
        for i, punto in enumerate(estado):
            if punto:
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
        """
        color_jugador = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        return self.__tablero__.obtener_fichas_barra(color_jugador) > 0
        
    def obtener_movimientos_disponibles(self):
        """
        Devuelve la lista de dados/movimientos que quedan por usar.
        """
        return self.__movimientos_disponibles__

    def jugador_puede_sacar_fichas(self) -> bool:
        """
        Verifica si el jugador actual cumple las condiciones para sacar fichas.
        """
        color = 'B' if self.__turno_actual__.obtener_color() == 'blanco' else 'N'
        
        if self.jugador_actual_tiene_fichas_en_barra():
            return False
        if not self.__tablero__.todas_las_fichas_en_casa(color):
            return False
            
        return True

    # --- MÉTODO AÑADIDO PARA ARREGLAR PYGAME ---
    def obtener_tablero(self):
        """
        Devuelve la instancia del tablero.
        Útil para la interfaz gráfica.
        """
        return self.__tablero__