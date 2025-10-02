import unittest
from unittest.mock import patch
from core.game import game

class TestGame(unittest.TestCase):
    
    def setUp(self):
        self.juego = game("Lautaro", "Eric")

    def test_inicializacion_completa(self):
        # Verificar TODOS los atributos iniciales (una sola vez)
        jugador1 = self.juego.mostrar_jugador1()
        jugador2 = self.juego.mostrar_jugador2()
        
        self.assertEqual(jugador1.obtener_nombre(), "Lautaro")
        self.assertEqual(jugador2.obtener_nombre(), "Eric")
        self.assertEqual(jugador1.obtener_color(), "blanco")
        self.assertEqual(jugador2.obtener_color(), "negro")
        self.assertEqual(self.juego.mostrar_jugador_actual(), jugador1)
        self.assertFalse(self.juego.__juego_terminado__)
        self.assertIsNone(self.juego.__ganador__)
        self.assertIsNotNone(self.juego.mostrar_dados())

    def test_cambiar_turno_ambas_direcciones(self):
        # Cubrir AMBAS ramas del if/else en cambiar_turno
        self.assertEqual(self.juego.__turno_actual__, self.juego.__jugador1__)
        
        # Cambio a jugador2
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.__turno_actual__, self.juego.__jugador2__)
        
        # Cambio a jugador1
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.__turno_actual__, self.juego.__jugador1__)

    def test_tirar_dados(self):
        # Ejecutar la línea de tirar_dados
        resultado = self.juego.tirar_dados()
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)

    def test_mover_ficha_ambos_colores_y_error(self):
        # Cubrir AMBAS ramas del if en mover_ficha + la excepción
        
        # Jugador blanco (turno inicial)
        with patch.object(self.juego.__tablero__, 'mover_ficha'):
            self.juego.mover_ficha(23, 20)  # Ejecuta línea del color 'B'
        
        # Jugador negro
        self.juego.cambiar_turno()
        with patch.object(self.juego.__tablero__, 'mover_ficha'):
            self.juego.mover_ficha(0, 3)  # Ejecuta línea del color 'N'
        
        # Juego terminado (excepción)
        self.juego.__juego_terminado__ = True
        with self.assertRaises(ValueError):
            self.juego.mover_ficha(0, 1)  # Ejecuta línea de la excepción

    @patch('builtins.print')
    def test_capturar_ficha_ambos_casos(self, mock_print):
        # Caso exitoso
        with patch.object(self.juego.__tablero__, 'capturar_ficha'):
            resultado = self.juego.capturar_ficha_enemiga(15)
            self.assertTrue(resultado)  # Ejecuta return True
        
        # Caso con error
        with patch.object(self.juego.__tablero__, 'capturar_ficha', 
                         side_effect=ValueError("Error")):
            resultado = self.juego.capturar_ficha_enemiga(5)
            self.assertFalse(resultado)  # Ejecuta return False

    @patch('builtins.print')
    def test_reincorporar_ficha_ambos_casos(self, mock_print):
        # Caso exitoso
        with patch.object(self.juego.__tablero__, 'reincorporar_ficha'):
            resultado = self.juego.reincorporar_ficha_desde_barra(8)
            self.assertTrue(resultado)
        
        # Caso con error
        with patch.object(self.juego.__tablero__, 'reincorporar_ficha', 
                         side_effect=ValueError("Error")):
            resultado = self.juego.reincorporar_ficha_desde_barra(10)
            self.assertFalse(resultado)

    @patch('builtins.print')
    def test_sacar_ficha_ambos_casos(self, mock_print):
        # Caso exitoso
        with patch.object(self.juego.__tablero__, 'sacar_ficha'):
            resultado = self.juego.sacar_ficha_del_tablero(0)
            self.assertTrue(resultado)
        
        # Caso con error
        with patch.object(self.juego.__tablero__, 'sacar_ficha', 
                         side_effect=ValueError("Error")):
            resultado = self.juego.sacar_ficha_del_tablero(23)
            self.assertFalse(resultado)

    def test_verificar_victoria_todos_casos(self):
        # TODOS los casos de victoria en un solo test
        
        # Caso 1: Sin ganador
        with patch.object(self.juego.__tablero__, 'hay_ganador', return_value=False):
            resultado = self.juego.verificar_victoria()
            self.assertFalse(resultado)
        
        # Caso 2: Jugador blanco gana
        with patch.object(self.juego.__tablero__, 'hay_ganador', 
                         side_effect=lambda color: color == 'B'):
            resultado = self.juego.verificar_victoria()
            self.assertTrue(resultado)
            self.assertEqual(self.juego.__ganador__, self.juego.__jugador1__)
        
        # Reset para caso 3
        self.juego.__juego_terminado__ = False
        self.juego.__ganador__ = None
        
        # Caso 3: Jugador negro gana
        with patch.object(self.juego.__tablero__, 'hay_ganador', 
                         side_effect=lambda color: color == 'N'):
            resultado = self.juego.verificar_victoria()
            self.assertTrue(resultado)
            self.assertEqual(self.juego.__ganador__, self.juego.__jugador2__)

    def test_obtener_ganador_ambos_casos(self):
        # Sin ganador
        self.assertIsNone(self.juego.obtener_ganador())
        
        # Con ganador
        self.juego.__ganador__ = self.juego.__jugador1__
        self.assertEqual(self.juego.obtener_ganador(), self.juego.__jugador1__)

if __name__ == '__main__':
    unittest.main()