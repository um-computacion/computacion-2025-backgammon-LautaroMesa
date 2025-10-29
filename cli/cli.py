# cli/main.py
"""
CLI interactivo para Backgammon - Computación 2025

- Interfaz por menú (sin comandos libres).
- Tablero ASCII: 24 puntos en cuatro cuadrantes de 6.
  * Fila superior (izq→der): 13..24   (24 arriba a la derecha)
  * Fila inferior (izq→der): 12..1    (1  abajo a la derecha)
- Cambia de turno automáticamente tras mover/capturar/reincorporar/sacar.
- Usa solo la API pública de Game (SRP/SOLID).
"""

from typing import Optional
from core.game import Game


class CLI:
    def __init__(self):
        self.__juego__: Optional[Game] = None

    # ---------- utilidades ----------

    def __leer_linea__(self, prompt: str) -> str:
        return input(prompt)

    def __leer_entero_en_rango__(self, prompt: str, minimo: int, maximo: int) -> Optional[int]:
        txt = self.__leer_linea__(f"{prompt} [{minimo}-{maximo}]: ").strip()
        try:
            n = int(txt)
        except ValueError:
            print("Entrada inválida. Ingrese un número entero.")
            return None
        if not (minimo <= n <= maximo):
            print(f"El número debe estar entre {minimo} y {maximo}.")
            return None
        return n

    # ---------- presentación ----------

    def __encabezado_turno__(self) -> None:
        try:
            j1 = self.__juego__.mostrar_jugador1()
            j2 = self.__juego__.mostrar_jugador2()
            ja = self.__juego__.mostrar_jugador_actual()
            print("\n===========================================")
            print("             BACKGAMMON CLI")
            print("===========================================")
            print(f"Jugador 1: {j1.obtener_nombre()} ({j1.obtener_color()})")
            print(f"Jugador 2: {j2.obtener_nombre()} ({j2.obtener_color()})")
            print(f"Turno actual: {ja.obtener_nombre()} ({ja.obtener_color()})")
        except Exception as e:
            print(f"Error al obtener jugadores: {e}")

    def __mostrar_tablero__(self) -> None:
        """
        Tablero ASCII con 24 puntos:
          - Fila superior (izq→der): 13..24   (24 arriba a la derecha)
          - Fila inferior (izq→der): 12..1    (1  abajo a la derecha)

        Solo usa Game.obtener_estado_tablero() y, si existe, ficha.obtener_color_letra().
        """
        if not self.__juego__:
            print("No hay partida iniciada.")
            return

        try:
            estado = self.__juego__.obtener_estado_tablero()  # dict[int, list[fichas]]
        except Exception as e:
            print(f"Error al obtener estado del tablero: {e}")
            return

        # Parámetros visuales
        ALTURA = 5          # filas visibles por punto
        ANCHO  = 3          # ancho fijo por columna
        SEP    = " "        # separador entre puntos
        QSEP   = " | "      # separador vertical entre cuadrantes (6 y 6)
        HSEP   = "-"        # carácter separador horizontal entre mitades

        # Mapeo punto-usuario (1..24) -> índice del core (0..23).
        # Si tu core usa otro orden, ajustá esta lista.
        core_idx_for_user_point = list(range(24))

        def fichas_en_punto(punto_usuario: int):
            idx = core_idx_for_user_point[punto_usuario - 1]
            fichas = estado.get(idx, [])
            if not fichas:
                return " ", 0
            f0 = fichas[0]
            if hasattr(f0, "obtener_color_letra"):
                letra = f0.obtener_color_letra() or " "
            else:
                s = str(f0) if f0 is not None else ""
                letra = s[0] if s else " "
            return letra[0], len(fichas)

        def celda(letra: str, cant: int, fila: int) -> str:
            if cant == 0:
                return " " * ANCHO
            if cant > ALTURA and fila == ALTURA - 1:
                return f"{letra}{cant}".ljust(ANCHO)[:ANCHO]
            if cant >= (fila + 1):
                return f" {letra} ".ljust(ANCHO)[:ANCHO]
            return " " * ANCHO

        def columnas_para(puntos: list[int]) -> list[list[str]]:
            cols = []
            for p in puntos:
                letra, cant = fichas_en_punto(p)
                cols.append([celda(letra, cant, f) for f in range(ALTURA)])
            return cols

        def unir_cuadrantes(items: list[str]) -> str:
            # items tiene 12 elementos (6 y 6)
            return SEP.join(items[:6]) + QSEP + SEP.join(items[6:])

        # Orden visual exacto que pediste
        top_points    = list(range(13, 25))       # 13..24 (izq→der)
        bottom_points = list(range(12, 0, -1))    # 12..1  (izq→der)

        top_cols    = columnas_para(top_points)
        bottom_cols = columnas_para(bottom_points)

        rotulos_top    = unir_cuadrantes([str(p).rjust(ANCHO) for p in top_points])
        rotulos_bottom = unir_cuadrantes([str(p).rjust(ANCHO) for p in bottom_points])

        print()
        print("TABLERO")

        # ----- SOLO rótulos superiores -----
        print(rotulos_top)

        # ----- Mitad superior: 13..24 -----
        for fila in range(ALTURA - 1, -1, -1):
            linea = unir_cuadrantes([col[fila] for col in top_cols])
            print(linea)

        # ----- Separador horizontal entre mitades -----
        print(HSEP * len(rotulos_top))

        # ----- Mitad inferior: 12..1 -----
        for fila in range(ALTURA):
            linea = unir_cuadrantes([col[fila] for col in bottom_cols])
            print(linea)

        # ----- SOLO rótulos inferiores -----
        print(rotulos_bottom)
        print()

    def __mostrar_estado__(self) -> None:
        if not self.__juego__:
            print("No hay partida iniciada.")
            return
        try:
            j1 = self.__juego__.mostrar_jugador1()
            j2 = self.__juego__.mostrar_jugador2()
            ja = self.__juego__.mostrar_jugador_actual()
            print("Estado del juego")
            print(f"Jugador 1: {j1.obtener_nombre()} ({j1.obtener_color()})")
            print(f"Jugador 2: {j2.obtener_nombre()} ({j2.obtener_color()})")
            print(f"Turno actual: {ja.obtener_nombre()} ({ja.obtener_color()})")
            if self.__juego__.verificar_victoria():
                ganador = self.__juego__.obtener_ganador()
                if ganador:
                    print(f"Ganador: {ganador.obtener_nombre()}")
        except Exception as e:
            print(f"Error al mostrar estado: {e}")

    # ---------- menú y flujo ----------

    def __menu_turno__(self) -> bool:
        print("\nSeleccione una opción:")
        print("1. Mover ficha")
        print("2. Capturar ficha enemiga")
        print("3. Reincorporar ficha desde la barra")
        print("4. Sacar ficha del tablero")
        print("5. Ver estado del juego")
        print("6. Ver tablero")
        print("7. Pasar turno")
        print("8. Salir")

        opcion = self.__leer_entero_en_rango__("Opción", 1, 8)
        if opcion is None:
            return True

        if opcion == 1:
            origen = self.__leer_entero_en_rango__("Punto origen", 0, 23)
            if origen is None:
                return True
            destino = self.__leer_entero_en_rango__("Punto destino", 0, 23)
            if destino is None:
                return True
            try:
                self.__juego__.mover_ficha(origen, destino)
                print("Movimiento realizado.")
                return False  # cierra turno automático
            except Exception as e:
                print(f"No se pudo mover la ficha: {e}")
            return True

        if opcion == 2:
            punto = self.__leer_entero_en_rango__("Punto para capturar", 0, 23)
            if punto is None:
                return True
            try:
                if self.__juego__.capturar_ficha_enemiga(punto):
                    print("Ficha enemiga capturada.")
                    return False
                else:
                    print("No se pudo capturar.")
            except Exception as e:
                print(f"Error en captura: {e}")
            return True

        if opcion == 3:
            punto = self.__leer_entero_en_rango__("Punto para reincorporar", 0, 23)
            if punto is None:
                return True
            try:
                if self.__juego__.reincorporar_ficha_desde_barra(punto):
                    print("Ficha reincorporada.")
                    return False
                else:
                    print("No se pudo reincorporar.")
            except Exception as e:
                print(f"Error: {e}")
            return True

        if opcion == 4:
            origen = self.__leer_entero_en_rango__("Punto de origen para sacar", 0, 23)
            if origen is None:
                return True
            try:
                if self.__juego__.sacar_ficha_del_tablero(origen):
                    print("Ficha sacada del tablero.")
                    return False
                else:
                    print("No se pudo sacar.")
            except Exception as e:
                print(f"Error: {e}")
            return True

        if opcion == 5:
            self.__mostrar_estado__()
            return True

        if opcion == 6:
            self.__mostrar_tablero__()
            return True

        if opcion == 7:
            print("Turno finalizado.")
            return False

        if opcion == 8:
            c = self.__leer_linea__("¿Seguro que desea salir? (s/n): ").strip().lower()
            if c in ("s", "si"):
                print("Fin del juego por decisión del usuario.")
                raise SystemExit(0)
            return True

        return True
if __name__ == "__main__":
    CLI().ejecutar()
