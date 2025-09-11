import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.jugador = Player("Lautaro", "blanco")

    def test_inicializacion(self):
        self.assertEqual(self.jugador.__nombre__, "Lautaro")
        self.assertEqual(self.jugador.__color__, "blanco")

    def test_str(self):
        self.assertEqual(str(self.jugador), "Lautaro (blanco)")

    def test_diferentes_colores(self):
        jugador2 = Player("Luis", "negro")
        self.assertEqual(jugador2.__color__, "negro")
        self.assertEqual(str(jugador2), "Luis (negro)")

    def test_casos_extremos(self):
        """Test adicional para cubrir casos borde."""
        jugador_vacio = Player("", "")
        self.assertEqual(str(jugador_vacio), " ()")
        
        jugador_largo = Player("NombreMuyLargo", "ColorEspecial")
        self.assertEqual(str(jugador_largo), "NombreMuyLargo (ColorEspecial)")

if __name__ == "__main__":
    unittest.main()