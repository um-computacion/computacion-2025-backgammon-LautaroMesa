class Player:      # Caracteristicas de un jugador de Backgammon.

    def __init__(self, __nombre__, __color__):
        
        #Inicializa un jugador de Backgammon.
        #para__nombre__: Nombre del jugador.
        #para__color__: Color de las fichas del jugador ('blanco' o 'negro').
        
        self.__nombre__ =__nombre__ 
        self.__color__ = __color__

    def __str__(self):
       
        #Devuelve una representación en texto del jugador.
        #return: Cadena con nombre y color.
        
        return f"{self.__nombre__} ({self.__color__})"       
       