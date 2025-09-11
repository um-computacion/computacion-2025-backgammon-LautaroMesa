import unittest
from unittest.mock import patch
from core.dice import Dado

class TestDado(unittest.TestCase):
    def setUp(self):
        self.dado = Dado()

    @patch('core.dice.random.randint')
    def test_tirar_valores_en_rango(self, mock_randint):
        #Verifica que tirar() use random.randint y devuelva los valores correctos.

        # Configurar el mock para que devuelva valores específicos
        mock_randint.side_effect = [3, 5]  # La primera llamada devuelve 3, segunda devuelve 5
        
        resultado = self.dado.tirar()
        
        # Verificar que se llamó random.randint dos veces con los parámetros correctos
        self.assertEqual(mock_randint.call_count, 2)
        mock_randint.assert_any_call(1, 6)
        
        # Verificar que devuelve los valores esperados
        self.assertEqual(resultado, (3, 5))
        self.assertEqual(self.dado.obtener_valores(), (3, 5))

    def test_tirar_valores_multiples(self):
        #Verifica que los valores estén en rango (sin mock, prueba real).

        for _ in range(100):
            d1, d2 = self.dado.tirar()
            self.assertIn(d1, range(1, 7))
            self.assertIn(d2, range(1, 7))

        # Verifica que es_doble detecta correctamente los dobles.
    def test_es_doble(self):              
       
        self.dado._Dado__dado1__ = 4
        self.dado._Dado__dado2__ = 4
        self.assertTrue(self.dado.es_doble())
        self.dado._Dado__dado1__ = 2
        self.dado._Dado__dado2__ = 5
        self.assertFalse(self.dado.es_doble())
        
        # Verifica que obtener_valores devuelve los valores actuales de los dados.
    def test_obtener_valores(self):         
                                        
        self.dado._Dado__dado1__ = 3
        self.dado._Dado__dado2__ = 6
        self.assertEqual(self.dado.obtener_valores(), (3, 6))

        # Verifica que reiniciar pone ambos dados en None.
    def test_reiniciar(self):             
        self.dado._Dado__dado1__ = 2
        self.dado._Dado__dado2__ = 5
        self.dado.reiniciar()
        self.assertIsNone(self.dado._Dado__dado1__)
        self.assertIsNone(self.dado._Dado__dado2__)

if __name__ == "__main__":
    unittest.main()