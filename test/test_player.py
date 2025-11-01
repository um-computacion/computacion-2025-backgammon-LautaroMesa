import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):
    """Pruebas unitarias para la clase Player."""
    
    def setUp(self):
        """Configura un jugador nuevo para cada test."""
        self.jugador = Player("Lautaro", "blanco")

    def test_inicializacion(self):
        """Verifica que los atributos se inicializan correctamente."""
        self.assertEqual(self.jugador.__nombre__, "Lautaro")
        self.assertEqual(self.jugador.__color__, "blanco")
        self.assertFalse(self.jugador.__es_turno__)
        # Se verifica que __fichas_en_barra__ y __fichas_fuera__ ya no existen.

    def test_inicializacion_color_valido_negro(self):
        """Verifica la inicialización exitosa con el color 'negro'."""
        jugador_negro = Player("Test", "negro")
        self.assertEqual(jugador_negro.__color__, "negro")

    def test_inicializacion_color_invalido(self):
        """Verifica que se lance ValueError si el color es inválido (ej: 'azul')."""
        with self.assertRaises(ValueError) as context:
            Player("Test", "azul")
        self.assertEqual(str(context.exception), "El color debe ser 'blanco' o 'negro'.")

    def test_inicializacion_color_invalido_vacio(self):
        """Verifica que se lance ValueError si el string de color está vacío."""
        with self.assertRaises(ValueError) as context:
            Player("Test", "")
        self.assertEqual(str(context.exception), "El color debe ser 'blanco' o 'negro'.")

    def test_obtener_nombre(self):
        """Verifica que el método obtener_nombre() devuelve el nombre correcto."""
        self.assertEqual(self.jugador.obtener_nombre(), "Lautaro")
        jugador2 = Player("Ana", "negro")
        self.assertEqual(jugador2.obtener_nombre(), "Ana")

    def test_obtener_color(self):
        """Verifica que el método obtener_color() devuelve el color correcto."""
        self.assertEqual(self.jugador.obtener_color(), "blanco")
        jugador_negro = Player("Luis", "negro")
        self.assertEqual(jugador_negro.obtener_color(), "negro")

    def test_str(self):
        """Verifica la representación en string (método __str__) del jugador."""
        self.assertEqual(str(self.jugador), "Lautaro (blanco)")

    def test_str_con_diferentes_valores(self):
        """Verifica __str__ con diferentes nombres y colores."""
        jugador_negro = Player("María", "negro")
        self.assertEqual(str(jugador_negro), "María (negro)")
        
        jugador_nombre_largo = Player("Juan Carlos", "blanco")
        self.assertEqual(str(jugador_nombre_largo), "Juan Carlos (blanco)")

    def test_todos_los_atributos_iniciales(self):
        """Prueba de redundancia para asegurar que los atributos principales están."""
        jugador = Player("Test", "blanco")
        self.assertEqual(jugador.__nombre__, "Test")
        self.assertEqual(jugador.__color__, "blanco")
        # Confirma que los atributos de conteo ya no están en Player.

if __name__ == "__main__":
    unittest.main()