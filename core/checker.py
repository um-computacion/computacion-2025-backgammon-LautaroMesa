class Ficha:
    
    # Representa una ficha individual de Backgammon.
    # Cada ficha tiene un color y puede estar en diferentes estados.
    

    def __init__(self, __color__):
        
        #Inicializa una ficha con un color específico.
        #param __color__: Color de la ficha ('B' para blanco, 'N' para negro).
        
        self.__color__ = __color__
        self.__posicion__ = None

    def obtener_color(self):
        
        #Devuelve el color de la ficha.
        #return: String con el color ('B' o 'N').
        
        return self.__color__

    def obtener_posicion(self):
        
        #Devuelve la posición actual de la ficha.
        #return: Índice del punto (0-23) o None si no está en el tablero.
        
        return self.__posicion__

    def establecer_posicion(self, __posicion__):
        
        # Establece la posición de la ficha en el tablero.
        # para__posicion__: Índice del punto (0-23) o None.
        
        self.__posicion__ = __posicion__

    def __str__(self):
        
        #Representación en string de la ficha.
        #return: String que representa la ficha.
        
        color_nombre = "Blanca" if self.__color__ == 'B' else "Negra"
        if self.__posicion__ is None:
            return f"Ficha {color_nombre}"
        else:
            return f"Ficha {color_nombre} en punto {self.__posicion__ + 1}"
        