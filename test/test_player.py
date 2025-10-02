import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.jugador = Player("Lautaro", "blanco")

    def test_inicializacion(self):
        # Verifica que la inicialización funciona correctamente
        self.assertEqual(self.jugador.__nombre__, "Lautaro")
        self.assertEqual(self.jugador.__color__, "blanco")
        self.assertEqual(self.jugador.__fichas_en_barra__, 0)
        self.assertEqual(self.jugador.__fichas_fuera__, 0)
        self.assertFalse(self.jugador.__es_turno__)

    def test_inicializacion_color_valido_negro(self):
        # Verifica inicialización con color negro
        jugador_negro = Player("Test", "negro")
        self.assertEqual(jugador_negro.__color__, "negro")

    def test_inicializacion_color_invalido(self):
        # Verifica que se lance ValueError con color inválido
        try:
            Player("Test", "azul")
            self.fail("Debería haber lanzado ValueError")
        except ValueError as e:
            self.assertEqual(str(e), "El color debe ser 'blanco' o 'negro'.")

    def test_inicializacion_color_invalido_vacio(self):
        # Verifica que se lance ValueError con color vacío
        try:
            Player("Test", "")
            self.fail("Debería haber lanzado ValueError")
        except ValueError as e:
            self.assertEqual(str(e), "El color debe ser 'blanco' o 'negro'.")

    def test_obtener_nombre(self):
        # Verifica que obtener_nombre funciona correctamente
        self.assertEqual(self.jugador.obtener_nombre(), "Lautaro")
        
        # Test con nombre diferente
        jugador2 = Player("Ana", "negro")
        self.assertEqual(jugador2.obtener_nombre(), "Ana")

    def test_obtener_color(self):
        # Verifica que obtener_color funciona correctamente
        self.assertEqual(self.jugador.obtener_color(), "blanco")
        
        # Test con color negro
        jugador_negro = Player("Luis", "negro")
        self.assertEqual(jugador_negro.obtener_color(), "negro")

    def test_str(self):
        # Verifica la representación en string
        self.assertEqual(str(self.jugador), "Lautaro (blanco)")

    def test_str_con_diferentes_valores(self):
        # Verifica __str__ con diferentes combinaciones
        jugador_negro = Player("María", "negro")
        self.assertEqual(str(jugador_negro), "María (negro)")
        
        jugador_nombre_largo = Player("Juan Carlos", "blanco")
        self.assertEqual(str(jugador_nombre_largo), "Juan Carlos (blanco)")

    def test_todos_los_atributos_iniciales(self):
        # Se verifica que todos los atributos se inicialicen correctamente
        jugador = Player("Test", "blanco")
        self.assertEqual(jugador.__nombre__, "Test")
        self.assertEqual(jugador.__color__, "blanco")
        self.assertEqual(jugador.__fichas_en_barra__, 0)
        self.assertEqual(jugador.__fichas_fuera__, 0)

if __name__ == "__main__":
    unittest.main()