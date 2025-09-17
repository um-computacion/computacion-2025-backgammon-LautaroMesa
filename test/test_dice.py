import unittest
from unittest.mock import patch
from core.dice import Dado

class TestDado(unittest.TestCase):
    def setUp(self):
        self.dado = Dado()

    def test_inicializacion(self):
        # Verifica que los dados se inicializan en None correctamente
        self.assertIsNone(self.dado._Dado__dado1__)
        self.assertIsNone(self.dado._Dado__dado2__)

    @patch('core.dice.random.randint')
    def test_tirar_valores_en_rango(self, mock_randint):
        # Verifica que tirar() use random.randint y devuelva los valores correctos
        # Configurar el mock para que devuelva valores específicos
        mock_randint.side_effect = [3, 5]  # La primera llamada devuelve 3, segunda devuelve 5
        
        resultado = self.dado.tirar()
        
        # Verificar que se llamó random.randint dos veces con los parámetros correctos
        self.assertEqual(mock_randint.call_count, 2)
        mock_randint.assert_any_call(1, 6)
        
        # Verificar que devuelve los valores esperados
        self.assertEqual(resultado, (3, 5))
        self.assertEqual(self.dado.obtener_valores(), (3, 5))

    @patch('core.dice.random.randint')
    def test_tirar_dobles(self, mock_randint):
        # Verifica el comportamiento cuando salen dados dobles
        mock_randint.side_effect = [4, 4]  # Ambos dados devuelven 4
        
        resultado = self.dado.tirar()
        
        self.assertEqual(resultado, (4, 4))
        self.assertTrue(self.dado.es_doble())

    @patch('core.dice.random.randint')
    def test_tirar_diferentes_valores(self, mock_randint):
        # Verifica el comportamiento cuando salen valores diferentes en los dados
        mock_randint.side_effect = [1, 6]  # Valores extremos
        
        resultado = self.dado.tirar()
        
        self.assertEqual(resultado, (1, 6))
        self.assertFalse(self.dado.es_doble())

    def test_tirar_valores_multiples(self):
        # Verifica que los valores estén en rango (sin mock, prueba real)
        for _ in range(100):
            d1, d2 = self.dado.tirar()
            self.assertIn(d1, range(1, 7))
            self.assertIn(d2, range(1, 7))

    def test_es_doble_true(self):
        # Verifica que es_doble detecta correctamente los dobles
        self.dado._Dado__dado1__ = 4
        self.dado._Dado__dado2__ = 4
        self.assertTrue(self.dado.es_doble())

    def test_es_doble_false(self):
        # Verifica que es_doble detecta correctamente cuando no son dobles
        self.dado._Dado__dado1__ = 2
        self.dado._Dado__dado2__ = 5
        self.assertFalse(self.dado.es_doble())

    def test_es_doble_con_none(self):
        # Verifica comportamiento de es_doble cuando los dados son None
        # Si los dados no se han tirado (None), no debería ser doble
        self.dado._Dado__dado1__ = None
        self.dado._Dado__dado2__ = None
        self.assertFalse(self.dado.es_doble())

    def test_es_doble_un_none(self):
        """Verifica comportamiento cuando solo un dado es None."""
        self.dado._Dado__dado1__ = 3
        self.dado._Dado__dado2__ = None
        self.assertFalse(self.dado.es_doble())

    def test_obtener_valores_con_valores(self):
        # Verifica que obtener_valores devuelve los valores actuales de los dados
        self.dado._Dado__dado1__ = 3
        self.dado._Dado__dado2__ = 6
        self.assertEqual(self.dado.obtener_valores(), (3, 6))

    def test_obtener_valores_iniciales(self):
        # Verifica obtener_valores cuando los dados no se han tirado
        self.assertEqual(self.dado.obtener_valores(), (None, None))

    def test_obtener_valores_despues_tirar(self):
        #Verifica que obtener_valores funciona después de tirar
        valores = self.dado.tirar()
        self.assertEqual(self.dado.obtener_valores(), valores)

    def test_reiniciar_con_valores(self):
        # Verifica que reiniciar pone ambos dados en None
        self.dado._Dado__dado1__ = 2
        self.dado._Dado__dado2__ = 5
        self.dado.reiniciar()
        self.assertIsNone(self.dado._Dado__dado1__)
        self.assertIsNone(self.dado._Dado__dado2__)

    def test_reiniciar_ya_inicializado(self):
        # Verifica reiniciar cuando ya está en None
        self.dado.reiniciar()
        self.assertIsNone(self.dado._Dado__dado1__)
        self.assertIsNone(self.dado._Dado__dado2__)

    def test_flujo_completo(self):
        # Verifica un flujo completo de uso del dado
        # Tirar dados
        valores = self.dado.tirar()
        
        # Verificar que se obtienen los mismos valores
        self.assertEqual(self.dado.obtener_valores(), valores)
        
        # Verificar que ambos valores están en rango
        self.assertIn(valores[0], range(1, 7))
        self.assertIn(valores[1], range(1, 7))
        
        # Reiniciar
        self.dado.reiniciar()
        self.assertEqual(self.dado.obtener_valores(), (None, None))

    def test_multiples_tiradas(self):
        # Verifica que se pueden hacer múltiples tiradas
        valores1 = self.dado.tirar()
        valores2 = self.dado.tirar()
        
        # Los valores pueden cambiar entre tiradas
        # Solo verificamos que están en rango
        for valor in valores1 + valores2:
            self.assertIn(valor, range(1, 7))

if __name__ == "__main__":
    unittest.main()