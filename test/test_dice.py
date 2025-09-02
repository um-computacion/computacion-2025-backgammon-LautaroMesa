import unittest
from core.dice import Dado

class TestDado(unittest.TestCase):
    def setUp(self):
        self.dado = Dado()

    def test_tirar_valores_en_rango(self):
        """Verifica que los valores de los dados estén siempre entre 1 y 6."""
        for _ in range(100):
            d1, d2 = self.dado.tirar()
            self.assertIn(d1, range(1, 7))
            self.assertIn(d2, range(1, 7))

    def test_es_doble(self):
        """Verifica que es_doble detecta correctamente los dobles."""
        self.dado._Dado__dado1__ = 4
        self.dado._Dado__dado2__ = 4
        self.assertTrue(self.dado.es_doble())
        self.dado._Dado__dado1__ = 2
        self.dado._Dado__dado2__ = 5
        self.assertFalse(self.dado.es_doble())

    def test_obtener_valores(self):
        """Verifica que obtener_valores devuelve los valores actuales de los dados."""
        self.dado._Dado__dado1__ = 3
        self.dado._Dado__dado2__ = 6
        self.assertEqual(self.dado.obtener_valores(), (3, 6))

    def test_reiniciar(self):
        """Verifica que reiniciar pone ambos dados en None."""
        self.dado._Dado__dado1__ = 2
        self.dado._Dado__dado2__ = 5
        self.dado.reiniciar()
        self.assertIsNone(self.dado._Dado__dado1__)
        self.assertIsNone(self.dado._Dado__dado2__)

if __name__ == "__main__":
    unittest.main()