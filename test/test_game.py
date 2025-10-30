from core.game import Game
import unittest
from unittest.mock import patch

class TestGame(unittest.TestCase):
    """Pruebas unitarias para la clase Game (cobertura 100%)."""
    
    def setUp(self):
        """Configura una instancia de Game nueva para cada test."""
        self.juego = Game("Lautaro", "Eric")

    def test_inicializacion_completa(self):
        """Verifica todos los atributos iniciales de Game."""
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
        """Verifica que cambiar_turno() alterna entre jugador1 y jugador2."""
        self.assertEqual(self.juego.__turno_actual__, self.juego.__jugador1__)
        
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.__turno_actual__, self.juego.__jugador2__)
        
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.__turno_actual__, self.juego.__jugador1__)

    def test_tirar_dados(self):
        """Verifica que tirar_dados() devuelve una tupla de 2 valores."""
        resultado = self.juego.tirar_dados()
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)

    def test_mover_ficha_ambos_colores_y_error(self):
        """Verifica que mover_ficha() pasa el color correcto ('B'/'N') al tablero."""
        
        # Jugador blanco (turno inicial)
        with patch.object(self.juego.__tablero__, 'mover_ficha') as mock_mover:
            self.juego.mover_ficha(23, 20)
            mock_mover.assert_called_with(23, 20, 'B') # Verifica que se llamó con 'B'
        
        # Jugador negro
        self.juego.cambiar_turno()
        with patch.object(self.juego.__tablero__, 'mover_ficha') as mock_mover:
            self.juego.mover_ficha(0, 3)
            mock_mover.assert_called_with(0, 3, 'N') # Verifica que se llamó con 'N'
        
        # Juego terminado (excepción)
        self.juego.__juego_terminado__ = True
        with self.assertRaises(ValueError):
            self.juego.mover_ficha(0, 1) 

    @patch('builtins.print')
    def test_reincorporar_ficha_todos_casos(self, mock_print):
        """Verifica reincorporar_ficha para ambos jugadores (éxito y error)."""
        # --- Jugador 1 (Blanco) ---
        with patch.object(self.juego.__tablero__, 'reincorporar_ficha') as mock_reincorporar:
            resultado = self.juego.reincorporar_ficha_desde_barra(8)
            self.assertTrue(resultado)
            mock_reincorporar.assert_called_with('B', 8)
        
        with patch.object(self.juego.__tablero__, 'reincorporar_ficha', 
                          side_effect=ValueError("Error")):
            resultado = self.juego.reincorporar_ficha_desde_barra(10)
            self.assertFalse(resultado)
            
        # --- Jugador 2 (Negro) ---
        self.juego.cambiar_turno()
        with patch.object(self.juego.__tablero__, 'reincorporar_ficha') as mock_reincorporar:
            resultado = self.juego.reincorporar_ficha_desde_barra(3)
            self.assertTrue(resultado)
            mock_reincorporar.assert_called_with('N', 3) # Verifica color 'N'

    @patch('builtins.print')
    def test_sacar_ficha_todos_casos(self, mock_print):
        """Verifica sacar_ficha para ambos jugadores (éxito y error)."""
        # --- Jugador 1 (Blanco) ---
        with patch.object(self.juego.__tablero__, 'sacar_ficha'):
            resultado = self.juego.sacar_ficha_del_tablero(20)
            self.assertTrue(resultado)
        
        with patch.object(self.juego.__tablero__, 'sacar_ficha', 
                          side_effect=ValueError("Error")):
            resultado = self.juego.sacar_ficha_del_tablero(23)
            self.assertFalse(resultado)

        # --- Jugador 2 (Negro) ---
        self.juego.cambiar_turno()
        with patch.object(self.juego.__tablero__, 'sacar_ficha') as mock_sacar:
            resultado = self.juego.sacar_ficha_del_tablero(3)
            self.assertTrue(resultado)
            mock_sacar.assert_called_with(3, 'N') # Verifica color 'N'

    def test_verificar_victoria_todos_casos(self):
        """Verifica los 3 escenarios de victoria: sin ganador, gana B, gana N."""
        
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
        
        self.juego = Game("L", "E") # Reset
        
        # Caso 3: Jugador negro gana
        with patch.object(self.juego.__tablero__, 'hay_ganador', 
                          side_effect=lambda color: color == 'N'):
            resultado = self.juego.verificar_victoria()
            self.assertTrue(resultado)
            self.assertEqual(self.juego.__ganador__, self.juego.__jugador2__)

    def test_obtener_ganador(self):
        """Cubre obtener_ganador() cuando no hay ganador y cuando sí hay."""
        # Sin ganador
        self.assertIsNone(self.juego.obtener_ganador())
        
        # Con ganador
        self.juego.__ganador__ = self.juego.__jugador1__
        self.assertEqual(self.juego.obtener_ganador(), self.juego.__jugador1__)

    def test_obtener_estado_tablero(self):
        """Cubre obtener_estado_tablero()."""
        estado_crudo = [
            ['N', 'N'], # Punto 0
            [],           # Punto 1
            ['B']         # Punto 2
        ]
        estado_crudo.extend([[] for _ in range(21)])
        
        with patch.object(self.juego.__tablero__, 'obtener_estado', return_value=estado_crudo):
            estado_dict = self.juego.obtener_estado_tablero()
            
            estado_esperado = {
                0: ['N', 'N'],
                2: ['B']
            }
            self.assertEqual(estado_dict, estado_esperado)
            self.assertNotIn(1, estado_dict)

    @patch('builtins.print')
    def test_mostrar_tablero_consola(self, mock_print):
        """Cubre mostrar_tablero_consola()."""
        with patch.object(self.juego.__tablero__, 'mostrar_tablero') as mock_mostrar:
            self.juego.mostrar_tablero_consola()
            mock_mostrar.assert_called_once()

    def test_jugador_actual_tiene_fichas_en_barra(self):
        """Cubre jugador_actual_tiene_fichas_en_barra()."""
        # Turno del Jugador 1 ('B')
        with patch.object(self.juego.__tablero__, 'obtener_fichas_barra', return_value=2) as mock_barra:
            self.assertTrue(self.juego.jugador_actual_tiene_fichas_en_barra())
            mock_barra.assert_called_with('B')

        # Turno del Jugador 2 ('N')
        self.juego.cambiar_turno()
        with patch.object(self.juego.__tablero__, 'obtener_fichas_barra', return_value=0) as mock_barra:
            self.assertFalse(self.juego.jugador_actual_tiene_fichas_en_barra())
            mock_barra.assert_called_with('N')

if __name__ == '__main__':
    unittest.main()