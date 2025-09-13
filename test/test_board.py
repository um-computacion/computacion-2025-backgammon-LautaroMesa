import unittest
from core.board import Tablero

class TestTablero(unittest.TestCase):
    
    def setUp(self):
        #Configura un tablero nuevo para cada test
        self.tablero = Tablero()

    def test_inicializacion_tablero(self):
        # Verifica que el tablero se inicializa correctamente
        # Verificamos que hay 24 puntos
        self.assertEqual(len(self.tablero.__puntos__), 24)
        
        # Verificar posiciones iniciales de fichas negras
        self.assertEqual(self.tablero.__puntos__[0], ['N', 'N'])
        self.assertEqual(self.tablero.__puntos__[11], ['N'] * 5)
        self.assertEqual(self.tablero.__puntos__[16], ['N'] * 3)
        self.assertEqual(self.tablero.__puntos__[18], ['N'] * 5)
        
        # Verificar posiciones iniciales de fichas blancas
        self.assertEqual(self.tablero.__puntos__[23], ['B', 'B'])
        self.assertEqual(self.tablero.__puntos__[12], ['B'] * 5)
        self.assertEqual(self.tablero.__puntos__[7], ['B'] * 3)
        self.assertEqual(self.tablero.__puntos__[5], ['B'] * 5)
        
        # Verificar que las barras están vacías inicialmente
        self.assertEqual(self.tablero.__barra_blanco__, [])
        self.assertEqual(self.tablero.__barra_negro__, [])
        
        # Verificar que las áreas de fichas fuera están vacías
        self.assertEqual(self.tablero.__fuera_blanco__, [])
        self.assertEqual(self.tablero.__fuera_negro__, [])

    def test_obtener_estado(self):
        #Verifica que obtener_estado devuelve el estado correcto del tablero
        self.assertEqual(len(estado), 24)
        self.assertEqual(estado[0], ['N', 'N'])
        self.assertEqual(estado[23], ['B', 'B'])

    def test_mostrar_tablero(self):
        #Verifica que mostrar_tablero no genere errores
        # Solo verificamos que no lance excepciones
        try:
            self.tablero.mostrar_tablero()
        except Exception as e:
            self.fail(f"mostrar_tablero() lanzó una excepción: {e}")
if __name__ == '__main__':
    unittest.main()