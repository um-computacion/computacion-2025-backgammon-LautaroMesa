class Player:      # Caracteristicas de un jugador de Backgammon.

    def __init__(self, __nombre__, __color__):
        
        #Inicializa un jugador de Backgammon.
        #para__nombre__: Nombre del jugador.
        #para__color__: Color de las fichas del jugador ('blanco' o 'negro').

        if __color__ not in ['blanco', 'negro']:
            raise ValueError("El color debe ser 'blanco' o 'negro'.")
        self.__nombre__ =__nombre__ 
        self.__color__ = __color__
        self.__fichas_en_barra__ = 0
        self.__fichas_fuera__ = 0
        self.__es_turno__ = False

    def obtener_nombre(self):
        #Devuelve el nombre del jugador.
        #return: Nombre del jugador.
        
        return self.__nombre__
    
    def obtener_color(self):
        #Devuelve el color de las fichas del jugador.
        #return: Color del jugador ('blanco' o 'negro').
        return self.__color__
     
    