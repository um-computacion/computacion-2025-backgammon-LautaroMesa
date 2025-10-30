#CLI DE BACKGAMMON
from typing import Optional
from core.game import Game


class CLI:
    def __init__(self):
        self.__juego__: Optional[Game] = None

    # ... (UTILIDADES y PRESENTACION sin cambios) ...
    
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

    def __encabezado_turno__(self) -> None:
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
        # ... (Sin cambios. Tu código de __mostrar_tablero__ está perfecto) ...
        pass # (Solo para acortar esta respuesta)

    def __mostrar_estado__(self) -> None:
        # ... (Sin cambios. Tu código de __mostrar_estado__ está perfecto) ...
        pass # (Solo para acortar esta respuesta)


    # EL MENU Y FLUJO DE EL JUEGO

    def __menu_turno__(self, *, tiene_fichas_en_barra: bool) -> bool:
        """
        (VERSIÓN ACTUALIZADA)
        Muestra un menú contextual basado en el estado del juego.
        :param tiene_fichas_en_barra: True si el jugador debe reincorporar.
        """
        print("\nSeleccione una opción:")
        
        # --- NUEVA LÓGICA DE MENÚ CONTEXTUAL ---
        if tiene_fichas_en_barra:
            # Si está en la barra, SOLO puede reincorporar
            print("1. Reincorporar ficha desde la barra")
            print("2. Ver tablero")
            print("3. Salir (abandonar partida)")
            
            opcion = self.__leer_entero_en_rango__("Opción", 1, 3)
            if opcion is None: return True

            if opcion == 1:
                punto = self.__leer_entero_en_rango__("Punto para reincorporar", 0, 23)
                if punto is None: return True
                try:
                    self.__juego__.reincorporar_ficha_desde_barra(punto)
                    print("Ficha reincorporada.")
                except Exception as e:
                    print(f"Error: {e}")
                return True # Vuelve al bucle (para gastar más dados si es doble)

            if opcion == 2:
                self.__mostrar_tablero__()
                return True

            if opcion == 3:
                # (Mantenemos la misma lógica de salida)
                c = self.__leer_linea__("¿Seguro que desea salir? (s/n): ").strip().lower()
                if c in ("s", "si"):
                    print("Fin del juego por decisión del usuario.")
                    raise SystemExit(0)
                return True

        else:
            # Si está libre, puede moverse y sacar
            print("1. Mover ficha")
            print("2. Sacar ficha del tablero")
            print("3. Ver tablero")
            print("4. Pasar turno (finalizar)")
            print("5. Salir (abandonar partida)")

            opcion = self.__leer_entero_en_rango__("Opción", 1, 5)
            if opcion is None: return True

            if opcion == 1:
                origen = self.__leer_entero_en_rango__("Punto origen", 0, 23)
                if origen is None: return True
                destino = self.__leer_entero_en_rango__("Punto destino", 0, 23)
                if destino is None: return True
                try:
                    self.__juego__.mover_ficha(origen, destino)
                    print("Movimiento realizado.")
                except Exception as e:
                    print(f"No se pudo mover la ficha: {e}")
                return True

            if opcion == 2:
                origen = self.__leer_entero_en_rango__("Punto de origen para sacar", 0, 23)
                if origen is None: return True
                try:
                    self.__juego__.sacar_ficha_del_tablero(origen)
                    print("Ficha sacada del tablero.")
                except Exception as e:
                    print(f"Error: {e}")
                return True

            if opcion == 3:
                self.__mostrar_tablero__()
                return True

            if opcion == 4:
                print("Turno finalizado.")
                return False # TERMINA el turno

            if opcion == 5:
                c = self.__leer_linea__("¿Seguro que desea salir? (s/n): ").strip().lower()
                if c in ("s", "si"):
                    print("Fin del juego por decisión del usuario.")
                    raise SystemExit(0)
                return True
        
        return True

    def __manejar_turno__(self) -> None:
        """
        (ACTUALIZADO)
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
            
            # --- NUEVA COMPROBACIÓN DE ESTADO ---
            # Le preguntamos al 'core' el estado ANTES de mostrar el menú
            debe_reincorporar = self.__juego__.jugador_actual_tiene_fichas_en_barra()
            
            continuar = self.__menu_turno__(tiene_fichas_en_barra=debe_reincorporar)
            if not continuar:
                break 

    def __configurar_jugadores__(self) -> tuple[str, str]:
        # ... (sin cambios)
        pass # (Solo para acortar)

    def ejecutar(self) -> None:
        # ... (sin cambios)
        pass # (Solo para acortar)

if __name__ == "__main__":
    CLI().ejecutar()