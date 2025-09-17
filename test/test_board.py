import unittest
from core.board import Tablero

class TestTablero(unittest.TestCase):
    
    def setUp(self):
        # Configura un tablero nuevo para cada test
        self.tablero = Tablero()

    def test_inicializacion_tablero(self):
        # Verifica inicialización correcta del tablero
        # Verificar 24 puntos
        self.assertEqual(len(self.tablero.__puntos__), 24)
        
        # Verificar fichas negras en posiciones iniciales
        self.assertEqual(self.tablero.__puntos__[0], ['N', 'N'])
        self.assertEqual(self.tablero.__puntos__[11], ['N'] * 5)
        self.assertEqual(self.tablero.__puntos__[16], ['N'] * 3)
        self.assertEqual(self.tablero.__puntos__[18], ['N'] * 5)
        
        # Verificar fichas blancas en posiciones iniciales
        self.assertEqual(self.tablero.__puntos__[23], ['B', 'B'])
        self.assertEqual(self.tablero.__puntos__[12], ['B'] * 5)
        self.assertEqual(self.tablero.__puntos__[7], ['B'] * 3)
        self.assertEqual(self.tablero.__puntos__[5], ['B'] * 5)

    def test_obtener_estado(self):
        # Verifica que obtener_estado devuelve los puntos
        estado = self.tablero.obtener_estado()
        self.assertEqual(estado, self.tablero.__puntos__)

    def test_mostrar_tablero(self):
        # Verifica que mostrar_tablero no lance errores
        # Solo verificar que no falle
        self.tablero.mostrar_tablero()

    def test_mover_ficha_valido(self):
        # Verifica movimiento válido
        self.tablero.mover_ficha(0, 1, 'N')
        self.assertEqual(self.tablero.__puntos__[0], ['N'])  # Queda una
        self.assertEqual(self.tablero.__puntos__[1], ['N'])  # Se movió una

    def test_mover_ficha_indices_invalidos(self):
        # Verifica validación de índices
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(-1, 5, 'N')
        self.assertEqual(str(context.exception), "Índices de puntos deben estar entre 0 y 23.")

    def test_mover_ficha_sin_ficha(self):
        # Verifica error cuando no hay ficha del color
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(1, 2, 'N')  # Punto 1 vacío
        self.assertEqual(str(context.exception), "No hay ficha del color especificado en el punto de origen.")

    def test_mover_ficha_destino_bloqueado(self):
        # Verifica bloqueo por fichas del oponente
        self.tablero.__puntos__[1] = ['B', 'B']  # Bloquear punto 1
        
        with self.assertRaises(ValueError) as context:
            self.tablero.mover_ficha(0, 1, 'N')
        self.assertEqual(str(context.exception), "Movimiento inválido: el punto de destino está bloqueado por fichas del oponente.")

    def test_capturar_ficha_valido(self):
        # Verifica captura válida
        self.tablero.__puntos__[1] = ['N']  # Una ficha negra sola
        self.tablero.capturar_ficha(1, 'B')
        
        self.assertEqual(self.tablero.__puntos__[1], [])
        self.assertEqual(self.tablero.__barra_negro__, ['N'])

    def test_capturar_ficha_indice_invalido(self):
        # Verifica validación de índice en captura
        with self.assertRaises(ValueError) as context:
            self.tablero.capturar_ficha(-1, 'B')
        self.assertEqual(str(context.exception), "Índice de punto debe estar entre 0 y 23.")

    def test_capturar_ficha_sin_oponente(self):
        # Verifica error sin ficha del oponente
        with self.assertRaises(ValueError) as context:
            self.tablero.capturar_ficha(1, 'B')  # Punto vacío
        self.assertEqual(str(context.exception), "No hay ficha del oponente en el punto especificado.")

    def test_capturar_ficha_multiples(self):
        # Verifica error con múltiples fichas
        with self.assertRaises(ValueError) as context:
            self.tablero.capturar_ficha(0, 'B')  # Punto 0 tiene 2 fichas negras
        self.assertEqual(str(context.exception), "No se puede capturar: más de una ficha del oponente en el punto.")

    def test_reincorporar_ficha_blanco(self):
        # Verifica reincorporación ficha blanca
        self.tablero.__barra_blanco__.append('B')
        self.tablero.reincorporar_ficha('B', 5)
        
        self.assertEqual(self.tablero.__barra_blanco__, [])
        self.assertEqual(self.tablero.__puntos__[5][-1], 'B')

    def test_reincorporar_ficha_negro(self):
        # Verifica reincorporación ficha negra
        self.tablero.__barra_negro__.append('N')
        self.tablero.reincorporar_ficha('N', 10)
        
        self.assertEqual(self.tablero.__barra_negro__, [])
        self.assertEqual(self.tablero.__puntos__[10][-1], 'N')

    def test_reincorporar_ficha_indice_invalido(self):
        # Verifica validación de índice en reincorporación
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('B', -1)
        self.assertEqual(str(context.exception), "Índice de punto debe estar entre 0 y 23.")

    def test_reincorporar_ficha_barra_vacia_blanco(self):
        # Verifica error con barra blanca vacía
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('B', 5)
        self.assertEqual(str(context.exception), "No hay fichas blancas en la barra para reincorporar.")

    def test_reincorporar_ficha_barra_vacia_negro(self):
        # Verifica error con barra negra vacía
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('N', 5)
        self.assertEqual(str(context.exception), "No hay fichas negras en la barra para reincorporar.")

    def test_reincorporar_ficha_color_invalido(self):
        # Verifica error con color inválido
        with self.assertRaises(ValueError) as context:
            self.tablero.reincorporar_ficha('X', 5)
        self.assertEqual(str(context.exception), "Color debe ser 'B' o 'N'.")

    def test_sacar_ficha_blanco(self):
        # Verifica sacar ficha blanca
        self.tablero.sacar_ficha(23, 'B')
        
        self.assertEqual(self.tablero.__puntos__[23], ['B'])  # Queda una
        self.assertEqual(self.tablero.__fuera_blanco__, ['B'])

    def test_sacar_ficha_negro(self):
        # Verifica sacar ficha negra
        self.tablero.sacar_ficha(0, 'N')
        
        self.assertEqual(self.tablero.__puntos__[0], ['N'])  # Queda una
        self.assertEqual(self.tablero.__fuera_negro__, ['N'])

    def test_sacar_ficha_sin_color(self):
        # Verifica error al sacar sin ficha del color
        with self.assertRaises(ValueError) as context:
            self.tablero.sacar_ficha(1, 'B')  # Punto vacío
        self.assertEqual(str(context.exception), "No hay ficha de ese color para sacar.")

    def test_hay_ganador_blanco_false(self):
        # Verifica que blanco no ha ganado inicialmente
        self.assertFalse(self.tablero.hay_ganador('B'))

    def test_hay_ganador_blanco_true(self):
        # Verifica victoria de blanco con 15 fichas fuera
        self.tablero.__fuera_blanco__ = ['B'] * 15
        self.assertTrue(self.tablero.hay_ganador('B'))

    def test_hay_ganador_negro_false(self):
        # Verifica que negro no ha ganado inicialmente
        self.assertFalse(self.tablero.hay_ganador('N'))

    def test_hay_ganador_negro_true(self):
        # Verifica victoria de negro con 15 fichas fuera
        self.tablero.__fuera_negro__ = ['N'] * 15
        self.assertTrue(self.tablero.hay_ganador('N'))

if __name__ == '__main__':
    unittest.main()