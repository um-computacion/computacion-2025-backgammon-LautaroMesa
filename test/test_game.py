from core.game import Game
import unittest
from unittest.mock import patch, MagicMock
from core.checker import Ficha # <--- ¡ESTA LÍNEA ES CRUCIAL!

class TestGame(unittest.TestCase):
    """Pruebas unitarias para la clase Game (estable)."""
    
    def setUp(self):
        """Configura una instancia de Game nueva para cada test."""
        self.juego = Game("Lautaro", "Eric")

    def test_inicializacion_completa(self):
        jugador1 = self.juego.mostrar_jugador1()
        jugador2 = self.juego.mostrar_jugador2()
        self.assertEqual(jugador1.obtener_nombre(), "Lautaro")
        self.assertEqual(jugador2.obtener_nombre(), "Eric")
        self.assertEqual(self.juego.mostrar_jugador_actual(), jugador1)

    def test_cambiar_turno_ambas_direcciones(self):
        self.assertEqual(self.juego.__turno_actual__, self.juego.__jugador1__)
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.__turno_actual__, self.juego.__jugador2__)
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.__turno_actual__, self.juego.__jugador1__)

    def test_tirar_dados_normal(self):
        with patch('core.dice.random.randint', side_effect=[3, 5]):
            resultado = self.juego.tirar_dados()
            self.assertEqual(resultado, (3, 5))
            self.assertEqual(self.juego.__movimientos_disponibles__, [3, 5])

    def test_tirar_dados_dobles(self):
        with patch('core.dice.random.randint', side_effect=[4, 4]):
            resultado = self.juego.tirar_dados()
            self.assertEqual(resultado, (4, 4))
            self.assertEqual(self.juego.__movimientos_disponibles__, [4, 4, 4, 4])

    def test_mover_ficha_valido_con_dados(self):
        self.juego.__movimientos_disponibles__ = [5]
        # Ponemos una ficha 'B' en el origen para que sea válido
        self.juego.__tablero__.__puntos__[18] = [Ficha('B')]
        with patch.object(self.juego.__tablero__, 'mover_ficha') as mock_mover:
            self.juego.mover_ficha(18, 13)
            mock_mover.assert_called_with(18, 13, 'B')
        self.assertEqual(self.juego.__movimientos_disponibles__, [])

    def test_mover_ficha_juego_terminado(self):
        self.juego.__juego_terminado__ = True
        with self.assertRaises(ValueError):
            self.juego.mover_ficha(0, 1)

    def test_mover_ficha_con_ficha_en_barra(self):
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=True):
            with self.assertRaises(ValueError) as context:
                self.juego.mover_ficha(18, 13)
            self.assertIn("Debe reincorporar", str(context.exception))

    def test_mover_ficha_direccion_incorrecta(self):
        self.juego.__movimientos_disponibles__ = [5, 6]
        # Ponemos una ficha 'B' en el origen
        self.juego.__tablero__.__puntos__[18] = [Ficha('B')]
        with self.assertRaises(ValueError) as context:
            self.juego.mover_ficha(18, 23) 
        self.assertIn("solo pueden moverse a puntos menores", str(context.exception))
        
        self.juego.cambiar_turno()
        self.juego.__movimientos_disponibles__ = [5, 6]
        # (El punto 5 ya tiene fichas 'N' por defecto, así que no hace falta setup)
        with self.assertRaises(ValueError) as context:
            self.juego.mover_ficha(5, 0)
        self.assertIn("solo pueden moverse a puntos mayores", str(context.exception))

    def test_mover_ficha_dado_incorrecto(self):
        self.juego.__movimientos_disponibles__ = [3, 5]
        self.juego.__tablero__.__puntos__[18] = [Ficha('B')] # Setup de origen
        with self.assertRaises(ValueError) as context:
            self.juego.mover_ficha(18, 17) # Necesita dado 1
        self.assertIn("no está permitido por los dados", str(context.exception))

    # --- TEST CORREGIDO ---
    def test_mover_ficha_destino_bloqueado_desde_game(self):
        self.juego.__movimientos_disponibles__ = [1]
        # 1. Pone la ficha 'B' correcta en el origen
        self.juego.__tablero__.__puntos__[18] = [Ficha('B')]
        # 2. Bloquea el destino
        self.juego.__tablero__.__puntos__[17] = [Ficha('N'), Ficha('N')]
        
        with self.assertRaises(ValueError) as context:
            self.juego.mover_ficha(18, 17)
        # 3. Ahora SÍ debe fallar por el bloqueo
        self.assertIn("punto de destino está bloqueado", str(context.exception))

    @patch('builtins.print')
    def test_reincorporar_ficha_todos_casos(self, mock_print):
        self.juego.__movimientos_disponibles__ = [1, 3]
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=True):
            with patch.object(self.juego.__tablero__, 'reincorporar_ficha') as mock_reincorporar:
                self.juego.reincorporar_ficha_desde_barra(0)
                mock_reincorporar.assert_called_with('B', 0)
                self.assertEqual(self.juego.__movimientos_disponibles__, [3])
            
            with self.assertRaises(ValueError) as context:
                self.juego.reincorporar_ficha_desde_barra(1)
            self.assertIn("no está permitido por los dados", str(context.exception))
        
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=False):
            with self.assertRaises(ValueError) as context:
                self.juego.reincorporar_ficha_desde_barra(0)
            self.assertIn("No tiene fichas en la barra", str(context.exception))
            
    def test_reincorporar_ficha_destino_bloqueado_desde_game(self):
        self.juego.__movimientos_disponibles__ = [1]
        self.juego.__tablero__.__barra_blanco__ = [Ficha('B')]
        self.juego.__tablero__.__puntos__[0] = [Ficha('N'), Ficha('N')]
        
        with self.assertRaises(ValueError) as context:
            self.juego.reincorporar_ficha_desde_barra(0)
        self.assertIn("punto de destino está bloqueado", str(context.exception))

    def test_reincorporar_ficha_cuadrante_incorrecto(self):
        self.juego.__movimientos_disponibles__ = [1, 2]
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=True):
            with self.assertRaises(ValueError) as context:
                self.juego.reincorporar_ficha_desde_barra(10)
            self.assertIn("solo pueden reincorporarse en puntos 0-5", str(context.exception))
        self.juego.cambiar_turno()
        self.juego.__movimientos_disponibles__ = [1, 2]
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=True):
            with self.assertRaises(ValueError) as context:
                self.juego.reincorporar_ficha_desde_barra(10)
            self.assertIn("solo pueden reincorporarse en puntos 18-23", str(context.exception))

    def test_sacar_ficha_dado_exacto(self):
        self.juego.__movimientos_disponibles__ = [1, 3]
        with patch.object(self.juego.__tablero__, 'todas_las_fichas_en_casa', return_value=True):
            # Setup: Poner ficha 'B' en el origen
            self.juego.__tablero__.__puntos__[23] = [Ficha('B')]
            with patch.object(self.juego.__tablero__, 'sacar_ficha') as mock_sacar:
                self.juego.sacar_ficha_del_tablero(23)
                mock_sacar.assert_called_with(23, 'B')
                self.assertEqual(self.juego.__movimientos_disponibles__, [3])

    def test_sacar_ficha_dado_mayor(self):
        self.juego.__movimientos_disponibles__ = [6]
        with patch.object(self.juego.__tablero__, 'todas_las_fichas_en_casa', return_value=True):
            with patch.object(self.juego.__tablero__, '_get_farthest_checker_in_home', return_value=20):
                # Setup: Poner ficha 'B' en el origen
                self.juego.__tablero__.__puntos__[20] = [Ficha('B')]
                with patch.object(self.juego.__tablero__, 'sacar_ficha') as mock_sacar:
                    self.juego.sacar_ficha_del_tablero(20)
                    mock_sacar.assert_called_with(20, 'B')
                    self.assertEqual(self.juego.__movimientos_disponibles__, [])

    def test_sacar_ficha_dado_mayor_falla_si_no_es_la_mas_lejana(self):
        self.juego.__movimientos_disponibles__ = [6]
        with patch.object(self.juego.__tablero__, 'todas_las_fichas_en_casa', return_value=True):
            with patch.object(self.juego.__tablero__, '_get_farthest_checker_in_home', return_value=19):
                # Setup: Poner ficha 'B' en el origen
                self.juego.__tablero__.__puntos__[21] = [Ficha('B')]
                with self.assertRaises(ValueError) as context:
                    self.juego.sacar_ficha_del_tablero(21)
                self.assertIn("hay fichas más lejanas", str(context.exception))

    def test_sacar_ficha_dado_insuficiente(self):
        self.juego.__movimientos_disponibles__ = [4]
        with patch.object(self.juego.__tablero__, 'todas_las_fichas_en_casa', return_value=True):
            # Setup: Poner ficha 'B' en el origen
            self.juego.__tablero__.__puntos__[19] = [Ficha('B')]
            with self.assertRaises(ValueError) as context:
                self.juego.sacar_ficha_del_tablero(19)
            self.assertIn("no está permitido por los dados", str(context.exception))
            
    def test_sacar_ficha_casa_vacia_error(self):
        self.juego.__movimientos_disponibles__ = [6]
        with patch.object(self.juego.__tablero__, 'todas_las_fichas_en_casa', return_value=True):
            with patch.object(self.juego.__tablero__, '_get_farthest_checker_in_home', return_value=None):
                with self.assertRaises(ValueError) as context:
                    self.juego.sacar_ficha_del_tablero(20)
                self.assertIn("La casa está vacía", str(context.exception))

    def test_sacar_ficha_dado_exacto_negro(self):
        self.juego.cambiar_turno()
        self.juego.__movimientos_disponibles__ = [5, 6]
        with patch.object(self.juego.__tablero__, 'todas_las_fichas_en_casa', return_value=True):
            # Setup: Poner ficha 'N' en el origen
            self.juego.__tablero__.__puntos__[5] = [Ficha('N')]
            with patch.object(self.juego.__tablero__, 'sacar_ficha') as mock_sacar:
                self.juego.sacar_ficha_del_tablero(5)
                mock_sacar.assert_called_with(5, 'N')
                self.assertEqual(self.juego.__movimientos_disponibles__, [5])

    def test_sacar_ficha_cuadrante_incorrecto(self):
        self.juego.__movimientos_disponibles__ = [1, 2] 
        with patch.object(self.juego.__tablero__, 'todas_las_fichas_en_casa', return_value=True):
            with self.assertRaises(ValueError) as context:
                self.juego.sacar_ficha_del_tablero(10)
            self.assertIn("solo pueden sacarse desde puntos 18-23", str(context.exception))
        self.juego.cambiar_turno()
        self.juego.__movimientos_disponibles__ = [1, 2]
        with patch.object(self.juego.__tablero__, 'todas_las_fichas_en_casa', return_value=True):
            with self.assertRaises(ValueError) as context:
                self.juego.sacar_ficha_del_tablero(10)
            self.assertIn("solo pueden sacarse desde puntos 0-5", str(context.exception))

    def test_sacar_ficha_con_ficha_en_barra(self):
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=True):
            with self.assertRaises(ValueError) as context:
                self.juego.sacar_ficha_del_tablero(23)
            self.assertIn("Debe reincorporar", str(context.exception))

    def test_sacar_ficha_falla_si_no_estan_todas_en_casa(self):
        self.juego.__movimientos_disponibles__ = [1, 2]
        with patch.object(self.juego.__tablero__, 'todas_las_fichas_en_casa', return_value=False):
            with self.assertRaises(ValueError) as context:
                self.juego.sacar_ficha_del_tablero(23)
            self.assertIn("No se pueden sacar fichas", str(context.exception))

    def test_verificar_victoria_todos_casos(self):
        with patch.object(self.juego.__tablero__, 'hay_ganador', return_value=False):
            resultado = self.juego.verificar_victoria()
            self.assertFalse(resultado)
        with patch.object(self.juego.__tablero__, 'hay_ganador', 
                          side_effect=lambda color: color == 'B'):
            resultado = self.juego.verificar_victoria()
            self.assertTrue(resultado)
            self.assertEqual(self.juego.__ganador__, self.juego.__jugador1__)
        self.juego = Game("L", "E")
        with patch.object(self.juego.__tablero__, 'hay_ganador', 
                          side_effect=lambda color: color == 'N'):
            resultado = self.juego.verificar_victoria()
            self.assertTrue(resultado)
            self.assertEqual(self.juego.__ganador__, self.juego.__jugador2__)

    def test_obtener_ganador(self):
        self.assertIsNone(self.juego.obtener_ganador())
        self.juego.__ganador__ = self.juego.__jugador1__
        self.assertEqual(self.juego.obtener_ganador(), self.juego.__jugador1__)

    def test_obtener_estado_tablero(self):
        estado_crudo = [['N', 'N'], [], ['B']]
        estado_crudo.extend([[] for _ in range(21)])
        with patch.object(self.juego.__tablero__, 'obtener_estado', return_value=estado_crudo):
            estado_dict = self.juego.obtener_estado_tablero()
            estado_esperado = {0: ['N', 'N'], 2: ['B']}
            self.assertEqual(estado_dict, estado_esperado)
            self.assertNotIn(1, estado_dict)

    @patch('builtins.print')
    def test_mostrar_tablero_consola(self, mock_print):
        with patch.object(self.juego.__tablero__, 'mostrar_tablero') as mock_mostrar:
            self.juego.mostrar_tablero_consola()
            mock_mostrar.assert_called_once()

    def test_jugador_actual_tiene_fichas_en_barra(self):
        with patch.object(self.juego.__tablero__, 'obtener_fichas_barra', return_value=2) as mock_barra:
            self.assertTrue(self.juego.jugador_actual_tiene_fichas_en_barra())
            mock_barra.assert_called_with('B')
        self.juego.cambiar_turno()
        with patch.object(self.juego.__tablero__, 'obtener_fichas_barra', return_value=0) as mock_barra:
            self.assertFalse(self.juego.jugador_actual_tiene_fichas_en_barra())
            mock_barra.assert_called_with('N')

    def test_obtener_movimientos_disponibles(self):
        self.assertEqual(self.juego.obtener_movimientos_disponibles(), [])
        self.juego.__movimientos_disponibles__ = [5, 5]
        self.assertEqual(self.juego.obtener_movimientos_disponibles(), [5, 5])

    def test_jugador_puede_sacar_fichas(self):
        with patch.object(self.juego.__tablero__, 'todas_las_fichas_en_casa', return_value=False):
            self.assertFalse(self.juego.jugador_puede_sacar_fichas())
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=True):
            self.assertFalse(self.juego.jugador_puede_sacar_fichas())
        with patch.object(self.juego.__tablero__, 'todas_las_fichas_en_casa', return_value=True):
            with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=False):
                self.assertTrue(self.juego.jugador_puede_sacar_fichas())

if __name__ == '__main__':
    unittest.main()