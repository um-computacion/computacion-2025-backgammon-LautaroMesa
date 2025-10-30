import unittest
from core.board import Tablero
from core.checker import Ficha 
from unittest.mock import patch

class TestTablero(unittest.TestCase):
   
    def setUp(self):
        """Configura un tablero nuevo para cada test."""
        self.tablero = Tablero()

    def test_inicializacion_tablero(self):
        """Verifica que las fichas estén en sus posiciones iniciales correctas."""
        self.assertEqual(len(self.tablero.__puntos__), 24)
        estado = self.tablero.obtener_estado()
        
        self.assertEqual(estado[0], ['N', 'N'])
        self.assertEqual(estado[11], ['N'] * 5)
        self.assertEqual(estado[16], ['N'] * 3)
        self.assertEqual(estado[18], ['N'] * 5)
        
        self.assertEqual(estado[23], ['B', 'B'])
        self.assertEqual(estado[12], ['B'] * 5)
        self.assertEqual(estado[7], ['B'] * 3)
        self.assertEqual(estado[5], ['B'] * 5)

    def test_obtener_estado(self):
        """Verifica que obtener_estado() convierte objetos Ficha a strings ('B'/'N')."""
        estado = self.tablero.obtener_estado()
        self.assertIsInstance(self.tablero.__puntos__[0][0], Ficha)
        self.assertEqual(estado[0][0], 'N')
        self.assertEqual(estado[0], ['N', 'N'])

    def test_mover_ficha_valido(self):
        """Verifica un movimiento simple y válido de una ficha."""
        self.tablero.mover_ficha(0, 1, 'N')
        estado = self.tablero.obtener_estado()
        self.assertEqual(estado[0], ['N'])
        self.assertEqual(estado[1], ['N'])

    def test_mover_ficha_con_captura_automatica_blanca(self):
        """Verifica que mover_ficha captura un 'blot' 'B'."""
        self.tablero.__puntos__[5] = [Ficha('B')]
        self.tablero.mover_ficha(0, 5, 'N')
        estado = self.tablero.obtener_estado()
        self.assertEqual(estado[5], ['N'])
        self.assertEqual(len(self.tablero.__barra_blanco__), 1)

    def test_mover_ficha_con_captura_negra(self):
        """Verifica la captura de un 'blot' 'N' (cubre la rama 'else')."""
        self.tablero.__puntos__[20] = [Ficha('N')]
        self.tablero.mover_ficha(23, 20, 'B')
        estado = self.tablero.obtener_estado()
        self.assertEqual(estado[20], ['B'])
        self.assertEqual(len(self.tablero.__barra_negro__), 1)

    def test_mover_ficha_indices_invalidos(self):
        """Verifica error si el origen o destino están fuera de [0, 23]."""
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(-1, 5, 'N')
        self.assertEqual(str(context.exception), "Índices de puntos deben estar entre 0 y 23.")
        
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(0, 24, 'N')
        self.assertEqual(str(context.exception), "Índices de puntos deben estar entre 0 y 23.")

    def test_mover_ficha_sin_ficha_o_color_incorrecto(self):
        """Verifica error si el origen está vacío o la ficha es del oponente."""
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(1, 2, 'N')
        self.assertEqual(str(context.exception), "No hay ficha del color especificado en el punto de origen.")
        
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(0, 1, 'B')
        self.assertEqual(str(context.exception), "No hay ficha del color especificado en el punto de origen.")

    def test_mover_ficha_destino_bloqueado(self):
        """Verifica que mover a un punto bloqueado (2+ fichas op.) lanza un error."""
        self.tablero.__puntos__[1] = [Ficha('B'), Ficha('B')]
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(0, 1, 'N')
        self.assertEqual(str(context.exception), "Movimiento inválido: el punto de destino está bloqueado.")

    def test_reincorporar_ficha_indice_invalido(self):
        """Cubre el "Paso 1" de reincorporar_ficha."""
        self.tablero.__barra_blanco__.append(Ficha('B'))
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('B', 24)
        self.assertEqual(str(context.exception), "Índice de punto debe estar entre 0 y 23.")

    def test_reincorporar_ficha_color_invalido(self):
        """Cubre el "Paso 2" de reincorporar_ficha."""
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('X', 5)
        self.assertEqual(str(context.exception), "Color debe ser 'B' o 'N'.")

    def test_reincorporar_ficha_barra_vacia(self):
        """Cubre el "Paso 3" de reincorporar_ficha."""
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('B', 5)
        self.assertEqual(str(context.exception), "No hay fichas blancas en la barra para reincorporar.")
        
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('N', 5)
        self.assertEqual(str(context.exception), "No hay fichas negras en la barra para reincorporar.")

    def test_reincorporar_ficha_destino_bloqueado(self):
        """Cubre el "Paso 4" de reincorporar_ficha."""
        self.tablero.__barra_negro__.append(Ficha('N'))
        self.tablero.__puntos__[3] = [Ficha('B'), Ficha('B')]
        
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('N', 3)
        self.assertEqual(str(context.exception), "Movimiento inválido: el punto de destino está bloqueado.")

    def test_reincorporar_ficha_con_captura_blanca(self):
        """Cubre el "Paso 5" (rama 'if') de reincorporar_ficha."""
        self.tablero.__barra_blanco__.append(Ficha('B'))
        self.tablero.__puntos__[20] = [Ficha('N')]
        self.tablero.reincorporar_ficha('B', 20)
        self.assertEqual(self.tablero.__puntos__[20][0].obtener_color(), 'B')
        self.assertEqual(len(self.tablero.__barra_negro__), 1)

    def test_reincorporar_ficha_con_captura_negra(self):
        """Cubre el "Paso 5" (rama 'else') de reincorporar_ficha."""
        self.tablero.__barra_negro__.append(Ficha('N'))
        self.tablero.__puntos__[3] = [Ficha('B')]
        self.tablero.reincorporar_ficha('N', 3)
        self.assertEqual(len(self.tablero.__barra_blanco__), 1)

    def test_reincorporar_ficha_blanco_valido(self):
        """Cubre el "Paso 6" (if) de reincorporar_ficha."""
        self.tablero.__barra_blanco__.append(Ficha('B'))
        self.tablero.reincorporar_ficha('B', 5)
        self.assertEqual(self.tablero.__barra_blanco__, [])
        self.assertEqual(self.tablero.__puntos__[5][-1].obtener_color(), 'B')

    def test_reincorporar_ficha_negro_valido(self):
        """Cubre el "Paso 6" (else) de reincorporar_ficha."""
        self.tablero.__barra_negro__.append(Ficha('N'))
        self.tablero.reincorporar_ficha('N', 10)
        self.assertEqual(self.tablero.__barra_negro__, [])
        self.assertEqual(self.tablero.__puntos__[10][-1].obtener_color(), 'N')

    def test_sacar_ficha_valido_blanco(self):
        """Verifica que sacar_ficha mueve una ficha blanca a 'fuera'."""
        self.tablero.sacar_ficha(23, 'B')
        self.assertEqual(len(self.tablero.__puntos__[23]), 1)
        self.assertEqual(len(self.tablero.__fuera_blanco__), 1)
        self.assertEqual(self.tablero.__fuera_blanco__[0].obtener_color(), 'B')

    def test_sacar_ficha_valido_negro(self):
        """Verifica que sacar_ficha mueve una ficha negra a 'fuera' (cubre 'else')."""
        self.tablero.sacar_ficha(0, 'N')
        self.assertEqual(len(self.tablero.__puntos__[0]), 1)
        self.assertEqual(len(self.tablero.__fuera_negro__), 1)
        self.assertEqual(self.tablero.__fuera_negro__[0].obtener_color(), 'N')

    def test_sacar_ficha_error(self):
        """Verifica el 'else' de sacar_ficha (error)."""
        with self.assertRaises(ValueError) as context:
            self.tablero.sacar_ficha(1, 'B')
        self.assertEqual(str(context.exception), "No hay ficha de ese color para sacar.")
        
        with self.assertRaises(ValueError) as context:
            self.tablero.sacar_ficha(0, 'B')
        self.assertEqual(str(context.exception), "No hay ficha de ese color para sacar.")

    def test_hay_ganador_todos_los_casos(self):
        """Cubre todos los 4 casos de hay_ganador (Líneas 139-144)."""
        # --- Pruebas para 'B' (Cubre 139, 141, 142) ---
        
        # Caso 1: Blanco GANA
        self.tablero.__fuera_blanco__ = [Ficha('B') for _ in range(15)]
        self.assertTrue(self.tablero.hay_ganador('B'))
        
        # Caso 2: Blanco AÚN NO GANA
        self.tablero.__fuera_blanco__ = [Ficha('B') for _ in range(10)]
        self.assertFalse(self.tablero.hay_ganador('B'))
        
        # --- Pruebas para 'N' (Cubre 139, 141(F), 143, 144) ---
        
        # Caso 3: Negro GANA
        self.tablero.__fuera_negro__ = [Ficha('N') for _ in range(15)]
        self.assertTrue(self.tablero.hay_ganador('N'))
        
        # Caso 4: Negro AÚN NO GANA
        self.tablero.__fuera_negro__ = [Ficha('N') for _ in range(5)]
        self.assertFalse(self.tablero.hay_ganador('N'))

    def test_obtener_fichas_barra_ambos_casos(self):
        """Verifica los métodos de conteo de fichas en barra."""
        self.tablero.__barra_blanco__.append(Ficha('B'))
        self.assertEqual(self.tablero.obtener_fichas_barra('B'), 1)
        self.assertEqual(self.tablero.obtener_fichas_barra('N'), 0) # Cubre 'else'

    def test_obtener_fichas_fuera_ambos_casos(self):
        """Verifica los casos de obtener_fichas_fuera."""
        self.tablero.__fuera_blanco__ = [Ficha('B') for _ in range(3)]
        self.assertEqual(self.tablero.obtener_fichas_fuera('B'), 3)
        
        self.tablero.__fuera_negro__ = [Ficha('N') for _ in range(2)]
        self.assertEqual(self.tablero.obtener_fichas_fuera('N'), 2) # Cubre 'else'

    @patch('builtins.print')
    def test_mostrar_tablero(self, mock_print):
        """Cubre el método mostrar_tablero (Línea 79)."""
        self.tablero.mostrar_tablero()
        mock_print.assert_any_call("Punto 1: ['N', 'N']")

if __name__ == '__main__':
    unittest.main()