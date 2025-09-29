import unittest
from unittest.mock import patch
from core.game import game

class TestGame(unittest.TestCase):
    
    def setUp(self):
        # Configuración común para todos los tests
        self.juego = game("Lautaro", "Eric")

    def test_creacion_juego_basico(self):
        # Verifico que el juego se cree correctamente
        jugador1 = self.juego.mostrar_jugador1()
        jugador2 = self.juego.mostrar_jugador2()
        
        self.assertEqual(jugador1.obtener_nombre(), "Lautaro")
        self.assertEqual(jugador2.obtener_nombre(), "Eric")
        self.assertEqual(jugador1.obtener_color(), "blanco")
        self.assertEqual(jugador2.obtener_color(), "negro")
        
        # Por defecto debe empezar el jugador 1
        self.assertEqual(self.juego.mostrar_jugador_actual(), jugador1)

    def test_alternar_turnos(self):
        # Verifico que los turnos cambien correctamente
        primer_jugador = self.juego.mostrar_jugador_actual()
        
        self.juego.cambiar_turno()
        segundo_jugador = self.juego.mostrar_jugador_actual()
        
        # Deben ser diferentes
        self.assertNotEqual(primer_jugador, segundo_jugador)
        
        # Al cambiar de nuevo, vuelve al primero
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.mostrar_jugador_actual(), primer_jugador)

    def test_tirada_dados_valida(self):
        # Los dados deben devolver valores entre 1 y 6
        resultado = self.juego.tirar_dados()
        
        # Debe ser una tupla de 2 elementos
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)
        
        # Cada dado debe estar entre 1 y 6
        for dado in resultado:
            self.assertGreaterEqual(dado, 1)
            self.assertLessEqual(dado, 6)

if __name__ == '__main__':
    unittest.main()