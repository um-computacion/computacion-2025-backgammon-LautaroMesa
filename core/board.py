class Tablero:
    #Representa el tablero de Backgammon con 24 puntos.
    #Gestiona la ubicación de las fichas de ambos jugadores.
  

    def __init__(self):
       
    #Inicializa el tablero con 24 puntos y las posiciones estándar de las fichas.
       
        self.__puntos__ = [[] for _ in range(24)]  # Cada punto es una lista de fichas ('B' o 'N')
        self.__barra_blanco__ = []  # Fichas blancas en la barra
        self.__barra_negro__ = []   # Fichas negras en la barra
        self.__fuera_blanco__ = []  # Fichas blancas fuera (ganadas)
        self.__fuera_negro__ = []   # Fichas negras fuera (ganadas)
        self.__inicializar_fichas__()

    def __inicializar_fichas__(self):       #Inicializa con la posicion de las fichas
        
    #Coloca las fichas en las posiciones iniciales estándar de Backgammon.
        
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
    
    def mostrar_tablero(self):
        
        #Imprime el estado actual del tablero en consola (modo texto).
        
        for i, punto in enumerate(self.__puntos__):
            print(f"Punto {i+1}: {punto}")
    def mover_ficha(self, origen, destino, color):
        #Mueve una ficha de un punto a otro si el movimiento es válido.
        #origen: Índice del punto de origen (0-23).
        #destino: Índice del punto de destino (0-23).
        #color: Color de la ficha que se mueve ('B' o 'N').
        
        if origen < 0 or origen > 23 or destino < 0 or destino > 23:
            raise ValueError("Índices de puntos deben estar entre 0 y 23.")
        
        if not self.__puntos__[origen] or self.__puntos__[origen][-1] != color:
            raise ValueError("No hay ficha del color especificado en el punto de origen.")
        
        if len(self.__puntos__[destino]) >= 2 and self.__puntos__[destino][-1] != color:
            raise ValueError("Movimiento inválido: el punto de destino está bloqueado por fichas del oponente.")
        
        # Mover la ficha
        ficha = self.__puntos__[origen].pop()
        self.__puntos__[destino].append(ficha)
    def capturar_ficha(self, punto, color):
        #Este metodo es para captura una ficha del oponente y la coloca en la barra.
        #punto: Índice del punto donde se captura la ficha (0-23).
        #color: Color de la ficha que captura ('B' o 'N').
        
        if punto < 0 or punto > 23:
            raise ValueError("Índice de punto debe estar entre 0 y 23.")
        
        if not self.__puntos__[punto] or self.__puntos__[punto][-1] == color:
            raise ValueError("No hay ficha del oponente en el punto especificado.")
        
        if len(self.__puntos__[punto]) > 1:
            raise ValueError("No se puede capturar: más de una ficha del oponente en el punto.")
        
        # Capturar la ficha
        ficha_capturada = self.__puntos__[punto].pop()
        if color == 'B':
            self
    def reincorporar_ficha(self, color, punto):
        #Reincorpora una ficha desde la barra al tablero.
        #color: Color de la ficha que se reincorpora ('B= Blanco' o 'N=Negro').
        #punto: Índice del punto donde se reincorpora la ficha (0-23).
        
        if punto < 0 or punto > 23:
            raise ValueError("Índice de punto debe estar entre 0 y 23.")
        
        if color == 'B':
            if not self.__barra_blanco__:
                raise ValueError("No hay fichas blancas en la barra para reincorporar.")
            self.__barra_blanco__.pop()
        elif color == 'N':
            if not self.__barra_negro__:
                raise ValueError("No hay fichas negras en la barra para reincorporar.") 