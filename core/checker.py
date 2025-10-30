class Ficha:
    """
    Representa una ficha individual de Backgammon.
    (Versión refactorizada respetando name mangling)
    
    Una ficha solo necesita saber su color. Su posición
    es determinada por la lista del Tablero en la que se encuentra.
    """

    def __init__(self, color):
        """
        Inicializa una ficha con un color específico.
        :param color: Color de la ficha ('B' para blanco, 'N' para negro).
        """
        if color not in ['B', 'N']:
             raise ValueError("El color debe ser 'B' o 'N'.")
        self.__color__ = color 

    def obtener_color(self):
        """
        Devuelve el color de la ficha.
        :return: String con el color ('B' o 'N').
        """
        return self.__color__

    def __str__(self):
        """
        Representación en string de la ficha.
        :return: String que representa la ficha ('B' o 'N').
        """
        return self.__color__

    def __repr__(self):
        """
        Representación oficial del objeto, útil para depuración.
        """
        return f"Ficha('{self.__color__}')"