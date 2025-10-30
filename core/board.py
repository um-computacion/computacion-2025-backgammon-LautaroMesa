from core.checker import Ficha 

class Tablero:
    """
    Representa el tablero de Backgammon con 24 puntos.
    (Versión refactorizada respetando name mangling)
    Gestiona la ubicación de los *objetos* Ficha de ambos jugadores.
    """

    def __init__(self):
        """
        Inicializa el tablero con 24 puntos y las posiciones estándar de las fichas.
        """
        self.__puntos__ = [[] for _ in range(24)] 
        self.__barra_blanco__ = []  
        self.__barra_negro__ = []   
        self.__fuera_blanco__ = []  
        self.__fuera_negro__ = []   
        self.__inicializar_fichas__()

    def __inicializar_fichas__(self):
        """
        Coloca las fichas (objetos Ficha) en las posiciones iniciales.
        Es un método privado llamado solo por __init__.
        """
        self.__puntos__ = [[] for _ in range(24)]
        
        self.__puntos__[0]  = [Ficha('N') for _ in range(2)]
        self.__puntos__[11] = [Ficha('N') for _ in range(5)]
        self.__puntos__[16] = [Ficha('N') for _ in range(3)]
        self.__puntos__[18] = [Ficha('N') for _ in range(5)]

        self.__puntos__[23] = [Ficha('B') for _ in range(2)]
        self.__puntos__[12] = [Ficha('B') for _ in range(5)]
        self.__puntos__[7]  = [Ficha('B') for _ in range(3)]
        self.__puntos__[5]  = [Ficha('B') for _ in range(5)]

    def obtener_estado(self):
        """
        Devuelve una representación del estado actual del tablero.
        Convierte los objetos Ficha a strings ('B'/'N') para la UI.
        :return: Lista de listas con los *colores* de las fichas ('B' o 'N').
        """
        estado_como_strings = []
        for punto in self.__puntos__:
            estado_como_strings.append([ficha.obtener_color() for ficha in punto])
        return estado_como_strings

    def mostrar_tablero(self):
        """
        Imprime el estado actual del tablero en consola (modo texto).
        Útil para depuración rápida.
        """
        for i, punto in enumerate(self.obtener_estado()):
            print(f"Punto {i+1}: {punto}")

    def mover_ficha(self, origen, destino, color):
        """
        Mueve una ficha de un punto a otro.
        La lógica de CAPTURA está integrada aquí.
        
        :param origen: Índice del punto de origen (0-23).
        :param destino: Índice del punto de destino (0-23).
        :param color: Color de la ficha que se mueve ('B' o 'N').
        """
        if origen < 0 or origen > 23 or destino < 0 or destino > 23:
            raise ValueError("Índices de puntos deben estar entre 0 y 23.")
        
        if not self.__puntos__[origen] or self.__puntos__[origen][-1].obtener_color() != color:
            raise ValueError("No hay ficha del color especificado en el punto de origen.")
        
        if len(self.__puntos__[destino]) >= 2 and self.__puntos__[destino][-1].obtener_color() != color:
            raise ValueError("Movimiento inválido: el punto de destino está bloqueado.")
        
        # Lógica de captura automática
        if len(self.__puntos__[destino]) == 1 and self.__puntos__[destino][0].obtener_color() != color:
            ficha_capturada = self.__puntos__[destino].pop()
            if ficha_capturada.obtener_color() == 'B':
                self.__barra_blanco__.append(ficha_capturada)
            else:
                self.__barra_negro__.append(ficha_capturada)
        
        # Mover la ficha
        ficha = self.__puntos__[origen].pop()
        self.__puntos__[destino].append(ficha)

    def reincorporar_ficha(self, color, punto):
        """
        Reincorpora una ficha desde la barra al tablero.
        También maneja la captura de "blots" al reincorporar.
        
        :param color: Color de la ficha a reincorporar ('B' o 'N').
        :param punto: Índice del punto donde se reincorpora (0-23).
        """
        # 1. Validar índice
        if punto < 0 or punto > 23:
            raise ValueError("Índice de punto debe estar entre 0 y 23.")
        
        # 2. Validar color
        if color not in ('B', 'N'):
            raise ValueError("Color debe ser 'B' o 'N'.")
        
        # 3. Validar que haya fichas en la barra
        if color == 'B':
            if not self.__barra_blanco__:
                raise ValueError("No hay fichas blancas en la barra para reincorporar.")
        else:  # color == 'N'
            if not self.__barra_negro__:
                raise ValueError("No hay fichas negras en la barra para reincorporar.")
        
        # 4. Validar que el destino no esté bloqueado
        if len(self.__puntos__[punto]) >= 2 and self.__puntos__[punto][-1].obtener_color() != color:
            raise ValueError("Movimiento inválido: el punto de destino está bloqueado.")
        
        # 5. Lógica de captura (si hay un blot)
        if len(self.__puntos__[punto]) == 1 and self.__puntos__[punto][0].obtener_color() != color:
            ficha_capturada = self.__puntos__[punto].pop()
            if ficha_capturada.obtener_color() == 'B':
                self.__barra_blanco__.append(ficha_capturada)
            else:
                self.__barra_negro__.append(ficha_capturada)
        
        # 6. Reincorporar la ficha
        if color == 'B':
            ficha = self.__barra_blanco__.pop()
            self.__puntos__[punto].append(ficha)
        else:  # color == 'N'
            ficha = self.__barra_negro__.pop()
            self.__puntos__[punto].append(ficha)

    def sacar_ficha(self, origen, color):
        """
        Saca una ficha del tablero (cuando llega al final).
        
        :param origen: Índice del punto de origen (0-23).
        :param color: Color de la ficha a sacar ('B' o 'N').
        """
        if self.__puntos__[origen] and self.__puntos__[origen][-1].obtener_color() == color:
            ficha = self.__puntos__[origen].pop()
            if color == 'B':
                self.__fuera_blanco__.append(ficha)
            else:
                self.__fuera_negro__.append(ficha)
        else:
            raise ValueError("No hay ficha de ese color para sacar.")
    
    def hay_ganador(self, color):
        """
        Verifica si el jugador ha ganado (todas sus fichas fuera).
        
        :param color: Color del jugador a verificar ('B' o 'N').
        :return: True si ganó, False si no.
        """
        if color == 'B':
            return len(self.__fuera_blanco__) == 15
        else:
            return len(self.__fuera_negro__) == 15

    def obtener_fichas_barra(self, color):
        """
        Devuelve el número de fichas que un color tiene en la barra.
        
        :param color: Color a consultar ('B' o 'N').
        :return: Entero con la cantidad de fichas.
        """
        if color == 'B':
            return len(self.__barra_blanco__)
        else:
            return len(self.__barra_negro__)

    def obtener_fichas_fuera(self, color):
        """
        Devuelve el número de fichas que un color tiene fuera del tablero.
        
        :param color: Color a consultar ('B' o 'N').
        :return: Entero con la cantidad de fichas.
        """
        if color == 'B':
            return len(self.__fuera_blanco__)
        else:
            return len(self.__fuera_negro__)