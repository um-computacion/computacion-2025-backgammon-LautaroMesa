class Player: 
    """
    Caracteristicas de un jugador de Backgammon.
    (Versión refactorizada)
    """

    def __init__(self, nombre, color):
        """
        Inicializa un jugador de Backgammon.
        :param nombre: Nombre del jugador.
        :param color: Color de las fichas del jugador ('blanco' o 'negro').
        """
        if color not in ['blanco', 'negro']:
            raise ValueError("El color debe ser 'blanco' o 'negro'.")
        
        self.__nombre__ = nombre 
        self.__color__ = color
        self.__es_turno__ = False
        # Se eliminaron __fichas_en_barra__ y __fichas_fuera__
        # para evitar duplicación de estado (ahora lo maneja Tablero).

    def obtener_nombre(self):
        """
        Devuelve el nombre del jugador.
        :return: Nombre del jugador.
        """
        return self.__nombre__
    
    def obtener_color(self):
        """
        Devuelve el color de las fichas del jugador.
        :return: Color del jugador ('blanco' o 'negro').
        """
        return self.__color__
     
    def __str__(self):
        """
        Devuelve una representación en texto del jugador.
        :return: Cadena con nombre y color.
        """
        return f"{self.__nombre__} ({self.__color__})"