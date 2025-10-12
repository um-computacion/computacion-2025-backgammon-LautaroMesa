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
            print("                         BARRA")
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
