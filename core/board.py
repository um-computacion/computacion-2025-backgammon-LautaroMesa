class Tablero:
    """
    Representa el tablero de Backgammon con 24 puntos.
    Gestiona la ubicación de las fichas de ambos jugadores.
    """

    def __init__(self):
        """
        Inicializa el tablero con 24 puntos y las posiciones estándar de las fichas.
        """
        self.__puntos__ = [[] for _ in range(24)]  # Cada punto es una lista de fichas ('B' o 'N')
        self.__barra_blanco__ = []  # Fichas blancas en la barra
        self.__barra_negro__ = []   # Fichas negras en la barra
        self.__fuera_blanco__ = []  # Fichas blancas fuera (ganadas)
        self.__fuera_negro__ = []   # Fichas negras fuera (ganadas)
        self.__inicializar_fichas__()

    def __inicializar_fichas__(self):       #Inicializa con la posicion de las fichas
        """
        Coloca las fichas en las posiciones iniciales estándar de Backgammon.
        """
        self.__puntos__ = [[] for _ in range(24)]
        self.__puntos__[0]  = ['N'] * 2
        self.__puntos__[11] = ['N'] * 5
        self.__puntos__[16] = ['N'] * 3
        self.__puntos__[18] = ['N'] * 5

        self.__puntos__[23] = ['B'] * 2
        self.__puntos__[12] = ['B'] * 5
        self.__puntos__[7]  = ['B'] * 3
        self.__puntos__[5]  = ['B'] * 5

    def obtener_estado(self):
        
        #Devuelve una representación del estado actual del tablero.
        #return: Lista de listas con las fichas en cada punto.
        
        return self.__puntos__

    