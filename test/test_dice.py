import unittest
from unittest.mock import patch
from core.dice import Dado

class TestDado(unittest.TestCase):
    """Pruebas unitarias para la clase Dado."""

    def setUp(self):
        """Configura un objeto Dado nuevo para cada test."""
        self.dado = Dado()

    def test_inicializacion(self):
        """Verifica que los dados se inicializan en None."""
        self.assertIsNone(self.dado._Dado__dado1__)
        self.assertIsNone(self.dado._Dado__dado2__)

    @patch('core.dice.random.randint')
    def test_tirar_valores_en_rango(self, mock_randint):
        """Verifica que tirar() usa random.randint y devuelve los valores correctos."""
        mock_randint.side_effect = [3, 5] 
        
        resultado = self.dado.tirar()
        
        self.assertEqual(mock_randint.call_count, 2)
        mock_randint.assert_any_call(1, 6)
        self.assertEqual(resultado, (3, 5))
        self.assertEqual(self.dado.obtener_valores(), (3, 5))

    @patch('core.dice.random.randint')
    def test_tirar_dobles(self, mock_randint):
        """Verifica que es_doble() es True cuando los valores son iguales."""
        mock_randint.side_effect = [4, 4]
        
        resultado = self.dado.tirar()
        
        self.assertEqual(resultado, (4, 4))
        self.assertTrue(self.dado.es_doble())

    @patch('core.dice.random.randint')
    def test_tirar_diferentes_valores(self, mock_randint):
        """Verifica que es_doble() es False cuando los valores son diferentes."""
        mock_randint.side_effect = [1, 6]
        
        resultado = self.dado.tirar()
        
        self.assertEqual(resultado, (1, 6))
        self.assertFalse(self.dado.es_doble())

    def test_tirar_valores_multiples(self):
        """Verifica que los valores reales (sin mock) estén en el rango [1, 6]."""
        for _ in range(100):
            d1, d2 = self.dado.tirar()
            self.assertIn(d1, range(1, 7))
            self.assertIn(d2, range(1, 7))

    def test_es_doble_true(self):
        """Verifica que es_doble() funciona seteando valores manualmente."""
        self.dado._Dado__dado1__ = 4
        self.dado._Dado__dado2__ = 4
        self.assertTrue(self.dado.es_doble())

    def test_es_doble_false(self):
        """Verifica que es_doble() es False seteando valores manualmente."""
        self.dado._Dado__dado1__ = 2
        self.dado._Dado__dado2__ = 5
        self.assertFalse(self.dado.es_doble())

    def test_es_doble_con_none(self):
        """Verifica que es_doble() es False si los dados son None."""
        self.dado._Dado__dado1__ = None
        self.dado._Dado__dado2__ = None
        self.assertFalse(self.dado.es_doble())

    def test_es_doble_un_none(self):
        """Verifica que es_doble() es False si solo un dado es None."""
        self.dado._Dado__dado1__ = 3
        self.dado._Dado__dado2__ = None
        self.assertFalse(self.dado.es_doble())

    def test_obtener_valores_con_valores(self):
        """Verifica obtener_valores() después de setearlos manualmente."""
        self.dado._Dado__dado1__ = 3
        self.dado._Dado__dado2__ = 6
        self.assertEqual(self.dado.obtener_valores(), (3, 6))

    def test_obtener_valores_iniciales(self):
        """Verifica obtener_valores() antes de la primera tirada (devuelve Nones)."""
        self.assertEqual(self.dado.obtener_valores(), (None, None))

    def test_obtener_valores_despues_tirar(self):
        """Verifica que obtener_valores() coincide con el return de tirar()."""
        valores = self.dado.tirar()
        self.assertEqual(self.dado.obtener_valores(), valores)

    def test_reiniciar_con_valores(self):
        """Verifica que reiniciar() setea ambos dados a None."""
        self.dado._Dado__dado1__ = 2
        self.dado._Dado__dado2__ = 5
        self.dado.reiniciar()
        self.assertIsNone(self.dado._Dado__dado1__)
        self.assertIsNone(self.dado._Dado__dado2__)

    def test_reiniciar_ya_inicializado(self):
        """Verifica que reiniciar() funciona aunque los dados ya sean None."""
        self.dado.reiniciar()
        self.assertIsNone(self.dado._Dado__dado1__)
        self.assertIsNone(self.dado._Dado__dado2__)

    def test_flujo_completo(self):
        """Verifica un flujo de tirar() y luego reiniciar()."""
        valores = self.dado.tirar()
        self.assertEqual(self.dado.obtener_valores(), valores)
        
        self.dado.reiniciar()
        self.assertEqual(self.dado.obtener_valores(), (None, None))

    def test_multiples_tiradas(self):
        """Verifica que múltiples llamadas a tirar() siguen generando valores válidos."""
        valores1 = self.dado.tirar()
        valores2 = self.dado.tirar()
        
        for valor in valores1 + valores2:
            self.assertIn(valor, range(1, 7))

if __name__ == "__main__":
    unittest.main()