from core.game import game
class CLI:

    def __init__(self):
        
        #Inicializa la interfaz CLI.
        
        #No recibe parámetros y establece el juego como None hasta que se inicie una partida.
    
        self.__juego__ = None
    def __mostrar_tablero__(self):
                
       # Se obtiene el estado del tablero desde el objeto game y lo presenta de forma visual.
        
        if not self.__juego__:
            print("Error: No hay partida iniciada.")
            return
        try:
            # Solo usamos métodos públicos de game
            estado_tablero = self.__juego__.mostrar_tablero()
            
            print("\n" + "=" * 70)
            print("                    TABLERO DE BACKGAMMON")
            print("=" * 70)
            
            # Mostrar puntos 13-24 (parte superior)
            print("Puntos:", end="  ")
            for i in range(13, 25):
                print(f"{i:2d}", end="  ")
            print()
             
            print("Fichas:", end="  ")
            for i in range(13, 25):
                punto = estado_tablero.get(i, [])
                if punto:
                    color = punto[0]
                    cantidad = len(punto)
                    print(f"{color}{cantidad:1d}", end="  ")
                else:
                    print("  ", end="  ")
            print()
            
            print("-" * 70)
            print("BARRA")
            print("-" * 70)
            
            # Mostrar puntos 12-1 (parte inferior)
            print("Fichas:", end="  ")
            for i in range(12, 0, -1):
                punto = estado_tablero.get(i-1, [])
                if punto:
                    color = punto[0]
                    cantidad = len(punto)
                    print(f"{color}{cantidad:1d}", end="  ")
                else:
                    print("  ", end="  ")
            print()
            
            print("Puntos:", end="  ")
            for i in range(12, 0, -1):
                print(f"{i-1:2d}", end="  ")
            print()
            
            print("=" * 70)
            
        except Exception as e:
            print(f"Error al mostrar tablero: {e}")
    def __obtener_nombres_jugadores__(self):
        """
        Solicita y valida los nombres de los jugadores.
        
        Devuelve:
            tuple: Nombres del jugador 1 (blancas) y jugador 2 (negras).
        """
        print("\nConfiguracion de jugadores:")
        
        while True:
            nombre1 = input("Nombre del Jugador 1 (Fichas Blancas): ").strip()
            if nombre1:
                break
            print("El nombre no puede estar vacio.")
        
        while True:
            nombre2 = input("Nombre del Jugador 2 (Fichas Negras): ").strip()
            if nombre2:
                break
            print("El nombre no puede estar vacio.")
        
        return nombre1, nombre2
    def __mostrar_ayuda__(self):
        
        # muestra la lista de comandos disponibles y su descripción.
    
        print("\n" + "=" * 50)
        print("COMANDOS DISPONIBLES")
        print("=" * 50)
        print("tablero      - Mostrar el tablero actual")
        print("dados        - Mostrar resultado de los dados")
        print("mover        - Mover una ficha")
        print("capturar     - Capturar ficha enemiga")
        print("reincorporar - Reincorporar ficha desde barra")
        print("sacar        - Sacar ficha del tablero")
        print("estado       - Ver estado completo del juego")
        print("pasar        - Pasar turno")
        print("ayuda        - Mostrar esta ayuda")
        print("salir        - Salir del juego")
        print("=" * 50)
    def __manejar_turno__(self):
        
    #Se gestiona un turno completo de juego usando solo métodos de game.

        jugador_actual = self.__juego__.mostrar_jugador_actual()
        
        print(f"\n{'-'*60}")
        print(f"Turno de: {jugador_actual.obtener_nombre()} ({jugador_actual.obtener_color()})")
        print(f"{'-'*60}")
        
        # Tirar dados
        input("Presiona Enter para tirar los dados...")
        dados_resultado = self.__juego__.tirar_dados()
        print(f"Resultado de los dados: {dados_resultado}")
        
        # Mostrar tablero
        self.__mostrar_tablero__()
        
        # Procesar comandos
        print(f"\n{jugador_actual.obtener_nombre()}, ¿que deseas hacer?")
        print("Escribe 'ayuda' para ver todos los comandos disponibles.")
        
        while True:
            comando = input("\nComando: ")
            if not self.__procesar_comando__(comando):
                break
    