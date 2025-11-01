import unittest
from unittest.mock import patch, MagicMock

from cli.cli import CLI


class TestCLI(unittest.TestCase):
    def setUp(self):
        # Parcheo global de print para que los tests de CLI no "abran" ni ensucien salida
        self.print_patcher = patch('builtins.print')
        self.mock_print_global = self.print_patcher.start()
        self.cli = CLI()

    def tearDown(self):
        try:
            self.print_patcher.stop()
        except Exception:
            pass

    # --- ejecutar() ---
    @patch('builtins.print')
    def test_ejecutar_termina_sin_bucle_y_anuncia_ganador(self, mock_print):
        # Parchar configuración de jugadores para evitar input
        with patch.object(self.cli, '__configurar_jugadores__', return_value=("A", "B")):
            # Parchar Game dentro del módulo cli.cli
            with patch('cli.cli.Game') as MockGame:
                game = MagicMock()
                game.verificar_victoria.return_value = True  # no entra al bucle principal
                ganador = MagicMock()
                ganador.obtener_nombre.return_value = "A"
                game.obtener_ganador.return_value = ganador
                # Para __mostrar_tablero__
                game.obtener_estado_tablero.return_value = {}
                MockGame.return_value = game

                self.cli.ejecutar()

                # Se crea el juego y se llama mostrar_tablero + mensaje de ganador
                MockGame.assert_called_once_with("A", "B")
                self.assertTrue(any("El juego ha finalizado." in str(call) for call in sum((c.args for c in mock_print.call_args_list), ())))

    # --- __menu_turno__ con barra ---
    def test_menu_turno_barra_ver_tablero(self):
        self.cli.__juego__ = MagicMock()
        with patch.object(self.cli, '__leer_entero_en_rango__', return_value=2), \
             patch.object(self.cli, '__mostrar_tablero__') as mock_tab:
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=True)
            self.assertTrue(seguir)
            mock_tab.assert_called_once()

    def test_menu_turno_barra_reincorporar_ok(self):
        self.cli.__juego__ = MagicMock()
        # Opción 1 y luego punto 6
        with patch.object(self.cli, '__leer_entero_en_rango__', side_effect=[1, 6]):
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=True)
            self.assertTrue(seguir)
            self.cli.__juego__.reincorporar_ficha_desde_barra.assert_called_once_with(5)

    def test_menu_turno_barra_reincorporar_error(self):
        self.cli.__juego__ = MagicMock()
        self.cli.__juego__.reincorporar_ficha_desde_barra.side_effect = Exception('fallo')
        with patch.object(self.cli, '__leer_entero_en_rango__', side_effect=[1, 6]), \
             patch('builtins.print') as mock_print:
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=True)
            self.assertTrue(seguir)
            self.assertTrue(any('Error:' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))

    def test_menu_turno_barra_salir_confirmado(self):
        self.cli.__juego__ = MagicMock()
        with patch.object(self.cli, '__leer_entero_en_rango__', return_value=3), \
             patch.object(self.cli, '__leer_linea__', return_value='s'):
            with self.assertRaises(SystemExit):
                self.cli.__menu_turno__(tiene_fichas_en_barra=True)

    def test_leer_entero_en_rango_invalido_y_fuera_de_rango(self):
        # invalido no entero
        with patch.object(self.cli, '__leer_linea__', return_value='abc'), \
             patch('builtins.print') as mock_print:
            res = self.cli.__leer_entero_en_rango__('Opción', 1, 3)
            self.assertIsNone(res)
            self.assertTrue(any('Entrada inválida' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))
        # fuera de rango
        with patch.object(self.cli, '__leer_linea__', return_value='9'), \
             patch('builtins.print') as mock_print:
            res = self.cli.__leer_entero_en_rango__('Opción', 1, 3)
            self.assertIsNone(res)
            self.assertTrue(any('El número debe estar entre 1 y 3' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))

    @patch('builtins.print')
    def test_encabezado_turno_sin_dados_y_con_error(self, mock_print):
        j = MagicMock()
        self.cli.__juego__ = j
        # sin dados restantes
        j.mostrar_jugador1.return_value.obtener_nombre.return_value = 'A'
        j.mostrar_jugador1.return_value.obtener_color.return_value = 'blanco'
        j.mostrar_jugador2.return_value.obtener_nombre.return_value = 'B'
        j.mostrar_jugador2.return_value.obtener_color.return_value = 'negro'
        j.mostrar_jugador_actual.return_value.obtener_nombre.return_value = 'A'
        j.mostrar_jugador_actual.return_value.obtener_color.return_value = 'blanco'
        j.obtener_movimientos_disponibles.return_value = []
        self.cli.__encabezado_turno__()
        texts = [" ".join(map(str, c.args)) for c in mock_print.call_args_list]
        self.assertFalse(any('Dados restantes:' in t for t in texts))
        # forzar excepción
        mock_print.reset_mock()
        self.cli.__juego__.mostrar_jugador1.side_effect = Exception('fallo')
        self.cli.__encabezado_turno__()
        self.assertTrue(any('Error al obtener jugadores' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))

    @patch('builtins.print')
    def test_mostrar_tablero_guardas(self, mock_print):
        # sin partida
        self.cli.__juego__ = None
        self.cli.__mostrar_tablero__()
        self.assertTrue(any('No hay partida iniciada.' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))
        # error al obtener estado
        mock_print.reset_mock()
        self.cli.__juego__ = MagicMock()
        self.cli.__juego__.obtener_estado_tablero.side_effect = Exception('x')
        self.cli.__mostrar_tablero__()
        self.assertTrue(any('Error al obtener estado del tablero:' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))

    @patch('builtins.print')
    def test_mostrar_tablero_conteo_superior(self, mock_print):
        # Estado con más fichas que ALTURA para activar rama de conteo (B7)
        self.cli.__juego__ = MagicMock()
        self.cli.__juego__.obtener_estado_tablero.return_value = {0: ['B'] * 7}
        self.cli.__mostrar_tablero__()
        texts = [" ".join(map(str, c.args)) for c in mock_print.call_args_list]
        self.assertTrue(any('B7' in t for t in texts))

    @patch('builtins.print')
    def test_mostrar_estado_variantes(self, mock_print):
        # sin partida
        self.cli.__juego__ = None
        self.cli.__mostrar_estado__()
        self.assertTrue(any('No hay partida iniciada.' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))
        # con ganador
        mock_print.reset_mock()
        j = MagicMock()
        self.cli.__juego__ = j
        j.mostrar_jugador1.return_value.obtener_nombre.return_value = 'A'
        j.mostrar_jugador1.return_value.obtener_color.return_value = 'blanco'
        j.mostrar_jugador2.return_value.obtener_nombre.return_value = 'B'
        j.mostrar_jugador2.return_value.obtener_color.return_value = 'negro'
        j.mostrar_jugador_actual.return_value.obtener_nombre.return_value = 'A'
        j.mostrar_jugador_actual.return_value.obtener_color.return_value = 'blanco'
        j.verificar_victoria.return_value = True
        ganador = MagicMock()
        ganador.obtener_nombre.return_value = 'A'
        j.obtener_ganador.return_value = ganador
        self.cli.__mostrar_estado__()
        self.assertTrue(any('Ganador: A' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))
        # excepción
        mock_print.reset_mock()
        self.cli.__juego__.mostrar_jugador1.side_effect = Exception('fallo')
        self.cli.__mostrar_estado__()
        self.assertTrue(any('Error al mostrar estado' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))

    # --- __menu_turno__ sin barra ---
    def test_menu_turno_normal_pasar_turno(self):
        j = MagicMock()
        j.jugador_puede_sacar_fichas.return_value = False
        self.cli.__juego__ = j
        # opción 3 = pasar turno
        with patch.object(self.cli, '__leer_entero_en_rango__', return_value=3):
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=False)
            self.assertFalse(seguir)

    def test_menu_turno_normal_opcion_none(self):
        j = MagicMock()
        j.jugador_puede_sacar_fichas.return_value = False
        self.cli.__juego__ = j
        with patch.object(self.cli, '__leer_entero_en_rango__', return_value=None):
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=False)
            self.assertTrue(seguir)

    def test_menu_turno_barra_opcion_none(self):
        self.cli.__juego__ = MagicMock()
        with patch.object(self.cli, '__leer_entero_en_rango__', return_value=None):
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=True)
            self.assertTrue(seguir)

    def test_menu_turno_normal_salir_no_confirmado(self):
        j = MagicMock()
        j.jugador_puede_sacar_fichas.return_value = False
        self.cli.__juego__ = j
        with patch.object(self.cli, '__leer_entero_en_rango__', return_value=4), \
             patch.object(self.cli, '__leer_linea__', return_value='n'):
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=False)
            self.assertTrue(seguir)

    def test_menu_turno_normal_ver_tablero(self):
        j = MagicMock()
        j.jugador_puede_sacar_fichas.return_value = False
        self.cli.__juego__ = j
        with patch.object(self.cli, '__leer_entero_en_rango__', return_value=2), \
             patch.object(self.cli, '__mostrar_tablero__') as mock_tab:
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=False)
            self.assertTrue(seguir)
            mock_tab.assert_called_once()

    def test_menu_turno_normal_mover_ok(self):
        j = MagicMock()
        j.jugador_puede_sacar_fichas.return_value = False
        self.cli.__juego__ = j
        # Opción 1 (mover), origen=5, destino=3
        with patch.object(self.cli, '__leer_entero_en_rango__', side_effect=[1, 5, 3]):
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=False)
            self.assertTrue(seguir)
            j.mover_ficha.assert_called_once_with(4, 2)

    def test_menu_turno_normal_mover_error(self):
        j = MagicMock()
        j.jugador_puede_sacar_fichas.return_value = False
        self.cli.__juego__ = j
        j.mover_ficha.side_effect = Exception('x')
        with patch.object(self.cli, '__leer_entero_en_rango__', side_effect=[1, 5, 3]), \
             patch('builtins.print') as mock_print:
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=False)
            self.assertTrue(seguir)
            self.assertTrue(any('No se pudo mover la ficha' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))

    def test_menu_turno_normal_sacar_ok(self):
        j = MagicMock()
        j.jugador_puede_sacar_fichas.return_value = True
        self.cli.__juego__ = j
        # Opción 2 (sacar) y origen=18
        with patch.object(self.cli, '__leer_entero_en_rango__', side_effect=[2, 18]):
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=False)
            self.assertTrue(seguir)
            j.sacar_ficha_del_tablero.assert_called_once_with(17)

    def test_menu_turno_normal_sacar_error(self):
        j = MagicMock()
        j.jugador_puede_sacar_fichas.return_value = True
        j.sacar_ficha_del_tablero.side_effect = Exception('fallo')
        self.cli.__juego__ = j
        with patch.object(self.cli, '__leer_entero_en_rango__', side_effect=[2, 18]), \
             patch('builtins.print') as mock_print:
            seguir = self.cli.__menu_turno__(tiene_fichas_en_barra=False)
            self.assertTrue(seguir)
            self.assertTrue(any('Error:' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))

    # --- __encabezado_turno__ ---
    @patch('builtins.print')
    def test_encabezado_turno_muestra_dados_restantes(self, mock_print):
        j = MagicMock()
        self.cli.__juego__ = j
        # configurar jugadores y dados restantes
        j.mostrar_jugador1.return_value.obtener_nombre.return_value = 'A'
        j.mostrar_jugador1.return_value.obtener_color.return_value = 'blanco'
        j.mostrar_jugador2.return_value.obtener_nombre.return_value = 'B'
        j.mostrar_jugador2.return_value.obtener_color.return_value = 'negro'
        j.mostrar_jugador_actual.return_value.obtener_nombre.return_value = 'A'
        j.mostrar_jugador_actual.return_value.obtener_color.return_value = 'blanco'
        j.obtener_movimientos_disponibles.return_value = [3, 5]
        self.cli.__encabezado_turno__()
        # Buscar la línea con los dados restantes
        impresiones = [str(a) for call in mock_print.call_args_list for a in call.args]
        self.assertTrue(any('Dados restantes: [3, 5]' in s for s in impresiones))

    # --- __manejar_turno__ ---
    def test_manejar_turno_autopase(self):
        j = MagicMock()
        self.cli.__juego__ = j
        j.tirar_dados.return_value = (1, 2)
        j.consumir_motivo_auto_pase.return_value = 'sin-movimientos'
        with patch.object(self.cli, '__leer_linea__', return_value=''):
            # Debe devolver False porque el core ya cambió el turno
            self.assertFalse(self.cli.__manejar_turno__())

    def test_manejar_turno_autopase_barra_bloqueada(self):
        j = MagicMock()
        self.cli.__juego__ = j
        j.tirar_dados.return_value = (1, 2)
        j.consumir_motivo_auto_pase.return_value = 'barra-bloqueada'
        with patch.object(self.cli, '__leer_linea__', return_value=''), \
             patch('builtins.print') as mock_print:
            res = self.cli.__manejar_turno__()
            self.assertFalse(res)
            self.assertTrue(any('Sin reingresos posibles' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))

    def test_manejar_turno_sin_movimientos_finaliza(self):
        j = MagicMock()
        self.cli.__juego__ = j
        j.tirar_dados.return_value = (1, 2)
        j.consumir_motivo_auto_pase.return_value = None
        j.obtener_movimientos_disponibles.return_value = []
        with patch.object(self.cli, '__leer_linea__', return_value=''):
            # Debe devolver True para que el bucle principal cambie el turno
            self.assertTrue(self.cli.__manejar_turno__())

    def test_manejar_turno_excepcion_tirar_dados(self):
        j = MagicMock()
        self.cli.__juego__ = j
        j.tirar_dados.side_effect = Exception('boom')
        with patch.object(self.cli, '__leer_linea__', return_value=''), \
             patch('builtins.print') as mock_print:
            res = self.cli.__manejar_turno__()
            self.assertTrue(res)
            self.assertTrue(any('Error al tirar los dados' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))

    def test_manejar_turno_loop_con_movimientos(self):
        j = MagicMock()
        self.cli.__juego__ = j
        j.tirar_dados.return_value = (3, 4)
        j.consumir_motivo_auto_pase.return_value = None
        # hay movimientos
        j.obtener_movimientos_disponibles.return_value = [3]
        j.jugador_actual_tiene_fichas_en_barra.return_value = False
        with patch.object(self.cli, '__leer_linea__', return_value=''), \
             patch.object(self.cli, '__menu_turno__', return_value=False):
            res = self.cli.__manejar_turno__()
            self.assertTrue(res)

    def test_configurar_jugadores_valida_vacios(self):
        with patch.object(self.cli, '__leer_linea__', side_effect=['', 'A', '', 'B']), \
             patch('builtins.print') as mock_print:
            n1, n2 = self.cli.__configurar_jugadores__()
            self.assertEqual((n1, n2), ('A', 'B'))
            texts = [" ".join(map(str, c.args)) for c in mock_print.call_args_list]
            self.assertTrue(any('El nombre no puede estar vacío.' in t for t in texts))

    @patch('builtins.print')
    def test_ejecutar_keyboardinterrupt_en_constructor(self, mock_print):
        with patch.object(self.cli, '__configurar_jugadores__', return_value=("A", "B")):
            with patch('cli.cli.Game', side_effect=KeyboardInterrupt):
                self.cli.ejecutar()
                self.assertTrue(any('Interrupción por teclado' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))

    @patch('builtins.print')
    def test_ejecutar_excepcion_general(self, mock_print):
        with patch.object(self.cli, '__configurar_jugadores__', return_value=("A", "B")):
            with patch('cli.cli.Game', side_effect=Exception('X')):
                self.cli.ejecutar()
                self.assertTrue(any('Error durante la ejecución' in ' '.join(map(str, c.args)) for c in mock_print.call_args_list))

    def test_main_guard_covered(self):
        import runpy, os
        # Evitar que se ejecute el CLI al importar como __main__
        with patch.dict('os.environ', {'BACKGAMMON_SKIP_MAIN': '1'}):
            runpy.run_module('cli.cli', run_name='__main__')
if __name__ == '__main__':
    unittest.main()
