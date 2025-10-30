import unittest
from core.checker import Ficha

class TestChecker(unittest.TestCase):
    """Pruebas unitarias para la clase Ficha (Checker)."""

    def test_inicializacion_color_invalido(self):
        """Verifica que Ficha() lanza un error si el color no es 'B' o 'N'."""
        with self.assertRaises(ValueError) as context:
            Ficha('Z') # 'Z' es un color inválido
        self.assertEqual(str(context.exception), "El color debe ser 'B' o 'N'.")

    def test_str_repr(self):
        """Verifica los métodos __str__ y __repr__."""
        ficha_b = Ficha('B')
        ficha_n = Ficha('N')
        
        self.assertEqual(str(ficha_b), 'B')
        self.assertEqual(str(ficha_n), 'N')
        self.assertEqual(repr(ficha_b), "Ficha('B')")
        self.assertEqual(repr(ficha_n), "Ficha('N')")

if __name__ == '__main__':
    unittest.main()