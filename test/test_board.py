import unittest
from core.board import Tablero
from core.checker import Ficha 
from unittest.mock import patch

class TestTablero(unittest.TestCase):
    """Pruebas unitarias para la clase Tablero (estable)."""
    
    def setUp(self):
        """Configura un tablero nuevo para cada test."""
        self.tablero = Tablero()

    def test_inicializacion_tablero(self):
        self.assertEqual(len(self.tablero.__puntos__), 24)
        estado = self.tablero.obtener_estado()
        self.assertEqual(estado[0], ['N', 'N'])
        self.assertEqual(estado[23], ['B', 'B'])

    def test_obtener_estado(self):
        estado = self.tablero.obtener_estado()
        self.assertIsInstance(self.tablero.__puntos__[0][0], Ficha)
        self.assertEqual(estado[0][0], 'N')

    def test_mover_ficha_valido(self):
        self.tablero.mover_ficha(0, 1, 'N')
        estado = self.tablero.obtener_estado()
        self.assertEqual(estado[0], ['N'])
        self.assertEqual(estado[1], ['N'])

    def test_mover_ficha_con_captura_automatica_blanca(self):
        self.tablero.__puntos__[5] = [Ficha('B')]
        self.tablero.mover_ficha(0, 5, 'N')
        self.assertEqual(len(self.tablero.__barra_blanco__), 1)

    def test_mover_ficha_con_captura_negra(self):
        self.tablero.__puntos__[20] = [Ficha('N')]
        self.tablero.mover_ficha(23, 20, 'B')
        self.assertEqual(len(self.tablero.__barra_negro__), 1)

    def test_mover_ficha_indices_invalidos(self):
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(-1, 5, 'N')
        self.assertEqual(str(context.exception), "Índices de puntos deben estar entre 0 y 23.")
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(0, 24, 'N')
        self.assertEqual(str(context.exception), "Índices de puntos deben estar entre 0 y 23.")

    def test_mover_ficha_sin_ficha_o_color_incorrecto(self):
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(1, 2, 'N')
        self.assertEqual(str(context.exception), "No hay ficha del color especificado en el punto de origen.")
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(0, 1, 'B')
        self.assertEqual(str(context.exception), "No hay ficha del color especificado en el punto de origen.")

    def test_mover_ficha_destino_bloqueado(self):
        self.tablero.__puntos__[1] = [Ficha('B'), Ficha('B')]
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(0, 1, 'N')
        self.assertEqual(str(context.exception), "Movimiento inválido: el punto de destino está bloqueado.")

    def test_reincorporar_ficha_indice_invalido(self):
        self.tablero.__barra_blanco__.append(Ficha('B'))
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('B', 24)
        self.assertEqual(str(context.exception), "Índice de punto debe estar entre 0 y 23.")

    def test_reincorporar_ficha_color_invalido(self):
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('X', 5)
        self.assertEqual(str(context.exception), "Color debe ser 'B' o 'N'.")

    def test_reincorporar_ficha_barra_vacia(self):
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('B', 5)
        self.assertEqual(str(context.exception), "No hay fichas blancas en la barra para reincorporar.")
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('N', 5)
        self.assertEqual(str(context.exception), "No hay fichas negras en la barra para reincorporar.")

    def test_reincorporar_ficha_destino_bloqueado(self):
        self.tablero.__barra_negro__.append(Ficha('N'))
        self.tablero.__puntos__[3] = [Ficha('B'), Ficha('B')]
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('N', 3)
        self.assertEqual(str(context.exception), "Movimiento inválido: el punto de destino está bloqueado.")

    def test_reincorporar_ficha_con_captura_blanca(self):
        self.tablero.__barra_blanco__.append(Ficha('B'))
        self.tablero.__puntos__[20] = [Ficha('N')]
        self.tablero.reincorporar_ficha('B', 20)
        self.assertEqual(len(self.tablero.__barra_negro__), 1)

    def test_reincorporar_ficha_con_captura_negra(self):
        self.tablero.__barra_negro__.append(Ficha('N'))
        self.tablero.__puntos__[3] = [Ficha('B')]
        self.tablero.reincorporar_ficha('N', 3)
        self.assertEqual(len(self.tablero.__barra_blanco__), 1)

    def test_reincorporar_ficha_blanco_valido(self):
        self.tablero.__barra_blanco__.append(Ficha('B'))
        self.tablero.reincorporar_ficha('B', 5)
        self.assertEqual(self.tablero.__barra_blanco__, [])

    def test_reincorporar_ficha_negro_valido(self):
        self.tablero.__barra_negro__.append(Ficha('N'))
        self.tablero.reincorporar_ficha('N', 10)
        self.assertEqual(self.tablero.__barra_negro__, [])

    def test_sacar_ficha_valido_blanco(self):
        self.tablero.sacar_ficha(23, 'B')
        self.assertEqual(len(self.tablero.__fuera_blanco__), 1)

    def test_sacar_ficha_valido_negro(self):
        self.tablero.sacar_ficha(0, 'N')
        self.assertEqual(len(self.tablero.__fuera_negro__), 1)

    def test_sacar_ficha_error(self):
        with self.assertRaises(ValueError) as context:
            self.tablero.sacar_ficha(1, 'B')
        self.assertEqual(str(context.exception), "No hay ficha de ese color para sacar.")
        with self.assertRaises(ValueError) as context:
            self.tablero.sacar_ficha(0, 'B')
        self.assertEqual(str(context.exception), "No hay ficha de ese color para sacar.")

    def test_hay_ganador_todos_los_casos(self):
        self.tablero.__fuera_blanco__ = [Ficha('B') for _ in range(15)]
        self.assertTrue(self.tablero.hay_ganador('B'))
        self.tablero.__fuera_blanco__ = [Ficha('B') for _ in range(10)]
        self.assertFalse(self.tablero.hay_ganador('B'))
        self.tablero.__fuera_negro__ = [Ficha('N') for _ in range(15)]
        self.assertTrue(self.tablero.hay_ganador('N'))
        self.tablero.__fuera_negro__ = [Ficha('N') for _ in range(5)]
        self.assertFalse(self.tablero.hay_ganador('N'))

    def test_obtener_fichas_barra_ambos_casos(self):
        self.tablero.__barra_blanco__.append(Ficha('B'))
        self.assertEqual(self.tablero.obtener_fichas_barra('B'), 1)
        self.assertEqual(self.tablero.obtener_fichas_barra('N'), 0)

    def test_obtener_fichas_fuera_ambos_casos(self):
        self.tablero.__fuera_blanco__ = [Ficha('B') for _ in range(3)]
        self.assertEqual(self.tablero.obtener_fichas_fuera('B'), 3)
        self.tablero.__fuera_negro__ = [Ficha('N') for _ in range(2)]
        self.assertEqual(self.tablero.obtener_fichas_fuera('N'), 2)

    @patch('builtins.print')
    def test_mostrar_tablero(self, mock_print):
        self.tablero.mostrar_tablero()
        mock_print.assert_any_call("Punto 1: ['N', 'N']")

    def test_todas_las_fichas_en_casa(self):
        self.assertFalse(self.tablero.todas_las_fichas_en_casa('B'))
        self.assertFalse(self.tablero.todas_las_fichas_en_casa('N'))
        self.tablero.__puntos__ = [[] for _ in range(24)]
        self.tablero.__puntos__[18] = [Ficha('B') for _ in range(15)]
        self.assertTrue(self.tablero.todas_las_fichas_en_casa('B'))
        self.tablero.__puntos__ = [[] for _ in range(24)]
        self.tablero.__puntos__[0] = [Ficha('N') for _ in range(15)]
        self.assertTrue(self.tablero.todas_las_fichas_en_casa('N'))
        self.tablero.__puntos__[18] = [Ficha('B') for _ in range(14)]
        self.tablero.__barra_blanco__ = [Ficha('B')]
        self.assertFalse(self.tablero.todas_las_fichas_en_casa('B'))
        self.tablero.__puntos__ = [[] for _ in range(24)]
        self.tablero.__puntos__[0] = [Ficha('N') for _ in range(14)]
        self.tablero.__barra_negro__ = [Ficha('N')]
        self.assertFalse(self.tablero.todas_las_fichas_en_casa('N'))

    def test_get_farthest_checker_in_home(self):
        self.tablero.__puntos__[18] = [Ficha('B')]
        self.tablero.__puntos__[20] = [Ficha('B')]
        self.assertEqual(self.tablero._get_farthest_checker_in_home('B'), 18)
        self.tablero.__puntos__ = [[] for _ in range(24)]
        self.tablero.__puntos__[19] = [Ficha('B')]
        self.assertEqual(self.tablero._get_farthest_checker_in_home('B'), 19)
        self.tablero.__puntos__ = [[] for _ in range(24)]
        self.tablero.__puntos__[5] = [Ficha('N')]
        self.tablero.__puntos__[3] = [Ficha('N')]
        self.assertEqual(self.tablero._get_farthest_checker_in_home('N'), 5)
        self.tablero.__puntos__ = [[] for _ in range(24)]
        self.tablero.__puntos__[4] = [Ficha('N')]
        self.assertEqual(self.tablero._get_farthest_checker_in_home('N'), 4)
        self.tablero.__puntos__ = [[] for _ in range(24)]
        self.assertIsNone(self.tablero._get_farthest_checker_in_home('B'))
        self.assertIsNone(self.tablero._get_farthest_checker_in_home('N'))
if __name__ == '__main__':
    unittest.main()