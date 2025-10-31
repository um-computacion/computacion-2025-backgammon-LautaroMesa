#CLI DE BACKGAMMON
from typing import Optional
from core.game import Game


class CLI:
    def __init__(self):
        self.__juego__: Optional[Game] = None

    # UTILIDADES

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

    # PRESENTACION 

    def __encabezado_turno__(self) -> None:
        """Muestra el encabezado, incluyendo dados restantes."""
        try:
            j1 = self.__juego__.mostrar_jugador1()
            j2 = self.__juego__.mostrar_jugador2()
            ja = self.__juego__.mostrar_jugador_actual()
            print("\n===========================================")
            print("           BACKGAMMON CLI")
            print("===========================================")
            print(f"Jugador 1: {j1.obtener_nombre()} ({j1.obtener_color()})")
            print(f"Jugador 2: {j2.obtener_nombre()} ({j2.obtener_color()})")
            print("-------------------------------------------")
            print(f"Turno actual: {ja.obtener_nombre()} ({ja.obtener_color()})")
            
            dados_restantes = self.__juego__.obtener_movimientos_disponibles()
            if dados_restantes:
                print(f"Dados restantes: {dados_restantes}")
            
        except Exception as e:
            print(f"Error al obtener jugadores: {e}")

    def __mostrar_tablero__(self) -> None:
        """
        Muestra el tablero ASCII con puntos 1-24.
        """
        if not self.__juego__:
            print("No hay partida iniciada.")
            return

        try:
            estado = self.__juego__.obtener_estado_tablero()
        except Exception as e:
            print(f"Error al obtener estado del tablero: {e}")
            return

        ALTURA = 5
        ANCHO  = 3
        SEP    = " "
        QSEP   = " | "
        HSEP   = "-"

        core_idx_for_user_point = list(range(24))

        def fichas_en_punto(punto_usuario: int):
            idx = core_idx_for_user_point[punto_usuario - 1]
            fichas = estado.get(idx, [])
            if not fichas:
                return " ", 0
            letra = fichas[0] 
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
            return SEP.join(items[:6]) + QSEP + SEP.join(items[6:])

        top_points    = list(range(13, 25))
        bottom_points = list(range(12, 0, -1))

        top_cols    = columnas_para(top_points)
        bottom_cols = columnas_para(bottom_points)

        rotulos_top    = unir_cuadrantes([str(p).rjust(ANCHO) for p in top_points])
        rotulos_bottom = unir_cuadrantes([str(p).rjust(ANCHO) for p in bottom_points])

        print()
        print("TABLERO")
        print(rotulos_top)
        for fila in range(ALTURA - 1, -1, -1):
            linea = unir_cuadrantes([col[fila] for col in top_cols])
            print(linea)
        print(HSEP * len(rotulos_top))
        for fila in range(ALTURA):
            linea = unir_cuadrantes([col[fila] for col in bottom_cols])
            print(linea)
        print(rotulos_bottom)
        print()

    def __mostrar_estado__(self) -> None:
        """Muestra el estado del juego (jugadores, turno, ganador)."""
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

    # EL MENU Y FLUJO DE EL JUEGO

    def __menu_turno__(self, *, tiene_fichas_en_barra: bool) -> bool:
        """
        (ACTUALIZADO)
        Muestra un menú contextual basado en el estado del juego.
        """
        print("\nSeleccione una opción:")
        
        if tiene_fichas_en_barra:
            # --- MENÚ DE BARRA ---
            print("1. Reincorporar ficha desde la barra")
            print("2. Ver tablero")
            print("3. Salir (abandonar partida)")
            
            opcion = self.__leer_entero_en_rango__("Opción", 1, 3)
            if opcion is None: return True

            if opcion == 1:
                punto = self.__leer_entero_en_rango__("Punto para reincorporar", 1, 24)
                if punto is None: return True
                try:
                    self.__juego__.reincorporar_ficha_desde_barra(punto - 1)
                    print("Ficha reincorporada.")
                except Exception as e:
                    print(f"Error: {e}")
                return True

            if opcion == 2:
                self.__mostrar_tablero__()
                return True

            if opcion == 3:
                c = self.__leer_linea__("¿Seguro que desea salir? (s/n): ").strip().lower()
                if c in ("s", "si"):
                    print("Fin del juego por decisión del usuario.")
                    raise SystemExit(0)
                return True

        else:
            # --- MENÚ NORMAL (ACTUALIZADO) ---
            
            # 1. Preguntamos al 'core' si sacar fichas es legal
            puede_sacar = self.__juego__.jugador_puede_sacar_fichas()
            
            # 2. Mostramos las opciones dinámicamente
            print("1. Mover ficha")
            op_sacar = 0
            
            if puede_sacar:
                print("2. Sacar ficha del tablero")
                op_sacar = 1 # Creamos un "offset"
            
            print(f"{2 + op_sacar}. Ver tablero")
            print(f"{3 + op_sacar}. Pasar turno (finalizar)")
            print(f"{4 + op_sacar}. Salir (abandonar partida)")

            max_opcion = 4 + op_sacar
            opcion = self.__leer_entero_en_rango__("Opción", 1, max_opcion)
            if opcion is None: return True

            # 3. Mapeamos la opción a la acción correcta
            
            if opcion == 1:
                # --- Acción: Mover ficha ---
                origen = self.__leer_entero_en_rango__("Punto origen", 1, 24)
                if origen is None: return True
                destino = self.__leer_entero_en_rango__("Punto destino", 1, 24)
                if destino is None: return True
                try:
                    self.__juego__.mover_ficha(origen - 1, destino - 1)
                    print("Movimiento realizado.")
                except Exception as e:
                    print(f"No se pudo mover la ficha: {e}")
                return True

            if puede_sacar and opcion == 2:
                # --- Acción: Sacar ficha ---
                origen = self.__leer_entero_en_rango__("Punto de origen para sacar", 1, 24)
                if origen is None: return True
                try:
                    self.__juego__.sacar_ficha_del_tablero(origen - 1)
                    print("Ficha sacada del tablero.")
                except Exception as e:
                    print(f"Error: {e}")
                return True
            
            # --- Acciones restantes (se ajustan con el 'offset') ---
            if opcion == (2 + op_sacar):
                self.__mostrar_tablero__()
                return True

            if opcion == (3 + op_sacar):
                print("Turno finalizado.")
                return False # TERMINA el turno

            if opcion == (4 + op_sacar):
                c = self.__leer_linea__("¿Seguro que desea salir? (s/n): ").strip().lower()
                if c in ("s", "si"):
                    print("Fin del juego por decisión del usuario.")
                    raise SystemExit(0)
                return True
        
        return True

    def __manejar_turno__(self) -> None:
        """
        Maneja el flujo completo de un solo turno.
        """
        self.__encabezado_turno__()
        self.__leer_linea__("Presione Enter para tirar los dados... ")
        try:
            resultado = self.__juego__.tirar_dados()
            print(f"Resultado de los dados: {resultado}")
        except Exception as e:
            print(f"Error al tirar los dados: {e}")
            return

        while True:
            self.__mostrar_tablero__()
            self.__encabezado_turno__()

            if not self.__juego__.obtener_movimientos_disponibles():
                print("No quedan más movimientos.")
                break 
            
            debe_reincorporar = self.__juego__.jugador_actual_tiene_fichas_en_barra()
            
            continuar = self.__menu_turno__(tiene_fichas_en_barra=debe_reincorporar)
            if not continuar:
                break 

    def __configurar_jugadores__(self) -> tuple[str, str]:
        """Pide los nombres de los jugadores."""
        print("\nConfiguración de jugadores")
        while True:
            j1 = self.__leer_linea__("Jugador 1 (fichas blancas): ").strip()
            if j1:
                break
            print("El nombre no puede estar vacío.")
        while True:
            j2 = self.__leer_linea__("Jugador 2 (fichas negras): ").strip()
            if j2:
                break
            print("El nombre no puede estar vacío.")
        return j1, j2

    def ejecutar(self) -> None:
        """Bucle principal del juego."""
        print("===========================================")
        print("       BACKGAMMON - INTERFAZ CLI")
        print("===========================================")
        n1, n2 = self.__configurar_jugadores__()

        try:
            self.__juego__ = Game(n1, n2)
            print(f"Partida iniciada entre {n1} y {n2}.")

            while not self.__juego__.verificar_victoria():
                self.__manejar_turno__()
                self.__juego__.cambiar_turno()

            self.__mostrar_tablero__()
            ganador = self.__juego__.obtener_ganador()
            if ganador:
                print(f"El juego ha finalizado. Ganador: {ganador.obtener_nombre()}")
            else:
                print("El juego terminó sin ganador definido.")
        except SystemExit:
            pass
        except KeyboardInterrupt:
            print("\nInterrupción por teclado. Fin del juego.")
        except Exception as e:
            print(f"\nError durante la ejecución: {e}")
            print("Verifique la implementación del core y vuelva a intentar.")
            
if __name__ == "__main__":
    CLI().ejecutar()