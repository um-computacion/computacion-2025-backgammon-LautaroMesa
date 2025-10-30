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

    def test_tirar_dados_normal(self):
        """Verifica que una tirada normal almacena 2 movimientos."""
        # Mockeamos randint para que devuelva 3 y 5
        with patch('core.dice.random.randint', side_effect=[3, 5]):
            resultado = self.juego.tirar_dados()
            self.assertEqual(resultado, (3, 5))
            # Verifica que los movimientos disponibles se almacenaron
            self.assertEqual(self.juego.__movimientos_disponibles__, [3, 5])

    def test_tirar_dados_dobles(self):
        """Verifica que una tirada doble almacena 4 movimientos."""
        # Mockeamos randint para que devuelva 4 y 4
        with patch('core.dice.random.randint', side_effect=[4, 4]):
            resultado = self.juego.tirar_dados()
            self.assertEqual(resultado, (4, 4))
            # Verifica que los 4 movimientos se almacenaron
            self.assertEqual(self.juego.__movimientos_disponibles__, [4, 4, 4, 4])

    def test_mover_ficha_valido_con_dados(self):
        """Verifica un movimiento válido que consume un dado."""
        # Damos manualmente los dados
        self.juego.__movimientos_disponibles__ = [5]
        # Mockeamos el tablero para que no falle
        with patch.object(self.juego.__tablero__, 'mover_ficha') as mock_mover:
            self.juego.mover_ficha(18, 13) # Movimiento 'B' de 5
            mock_mover.assert_called_with(18, 13, 'B')
        # Verifica que el dado fue consumido
        self.assertEqual(self.juego.__movimientos_disponibles__, [])

    def test_mover_ficha_juego_terminado(self):
        """Verifica que no se puede mover si el juego terminó."""
        self.juego.__juego_terminado__ = True
        with self.assertRaises(ValueError):
            self.juego.mover_ficha(0, 1)

    def test_mover_ficha_con_ficha_en_barra(self):
        """Verifica que no se puede mover si hay fichas en la barra."""
        # Mockeamos la función para que devuelva True
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=True):
            with self.assertRaises(ValueError) as context:
                self.juego.mover_ficha(18, 13)
            self.assertIn("Debe reincorporar", str(context.exception))

    def test_mover_ficha_direccion_incorrecta(self):
        """
        Verifica que el movimiento falla si va en la dirección incorrecta.
        (Cubre la nueva lógica de dirección en mover_ficha).
        """
        self.juego.__movimientos_disponibles__ = [5, 6] 
        
        # Caso 1: Blanco ('B') intentando moverse "hacia arriba" (ilegal)
        with self.assertRaises(ValueError) as context:
            self.juego.mover_ficha(18, 23) 
        self.assertIn("solo pueden moverse a puntos menores", str(context.exception))

        self.juego.cambiar_turno()
        self.juego.__movimientos_disponibles__ = [5, 6]
        
        # Caso 2: Negro ('N') intentando moverse "hacia abajo" (ilegal)
        with self.assertRaises(ValueError) as context:
            self.juego.mover_ficha(5, 0)
        self.assertIn("solo pueden moverse a puntos mayores", str(context.exception))

    def test_mover_ficha_dado_incorrecto(self):
        """Verifica que el movimiento falla si el dado no está disponible."""
        self.juego.__movimientos_disponibles__ = [3, 5]
        with self.assertRaises(ValueError) as context:
            self.juego.mover_ficha(18, 17) # Movimiento de 1, pero solo tiene [3, 5]
        self.assertIn("no está permitido por los dados", str(context.exception))

    @patch('builtins.print')
    def test_reincorporar_ficha_todos_casos(self, mock_print):
        """Verifica reincorporar_ficha para ambos jugadores (éxito y error)."""
        self.juego.__movimientos_disponibles__ = [1, 3]
        
        # --- Jugador 1 (Blanco) ---
        # Mockeamos que SÍ tiene fichas en la barra
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=True):
            # Caso Éxito (Punto 0 -> necesita dado 1)
            with patch.object(self.juego.__tablero__, 'reincorporar_ficha') as mock_reincorporar:
                self.juego.reincorporar_ficha_desde_barra(0)
                mock_reincorporar.assert_called_with('B', 0)
                self.assertEqual(self.juego.__movimientos_disponibles__, [3]) # Dado 1 consumido
            
            # Caso Error (Dado no disponible)
            with self.assertRaises(ValueError) as context:
                self.juego.reincorporar_ficha_desde_barra(1) # Necesita dado 2, solo tiene [3]
            self.assertIn("no está permitido por los dados", str(context.exception))
        
        # Caso Error (No tiene fichas en la barra)
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=False):
            with self.assertRaises(ValueError) as context:
                self.juego.reincorporar_ficha_desde_barra(0)
            self.assertIn("No tiene fichas en la barra", str(context.exception))

    def test_reincorporar_ficha_cuadrante_incorrecto(self):
        """
        Verifica que reincorporar falla si el punto no es el cuadrante de entrada.
        """
        self.juego.__movimientos_disponibles__ = [1, 2]
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=True):
        
            # Caso 1: Blanco ('B') intentando reincorporarse fuera de 0-5
            with self.assertRaises(ValueError) as context:
                self.juego.reincorporar_ficha_desde_barra(10)
            self.assertIn("solo pueden reincorporarse en puntos 0-5", str(context.exception))
        
        self.juego.cambiar_turno()
        self.juego.__movimientos_disponibles__ = [1, 2]
        
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=True):
            # Caso 2: Negro ('N') intentando reincorporarse fuera de 18-23
            with self.assertRaises(ValueError) as context:
                self.juego.reincorporar_ficha_desde_barra(10)
            self.assertIn("solo pueden reincorporarse en puntos 18-23", str(context.exception))

    @patch('builtins.print')
    def test_sacar_ficha_todos_casos(self, mock_print):
        """Verifica sacar_ficha para ambos jugadores (éxito y error)."""
        # --- Jugador 1 (Blanco) ---
        self.juego.__movimientos_disponibles__ = [1, 3] # Dado 1 para punto 23
        
        # Caso Éxito
        with patch.object(self.juego.__tablero__, 'sacar_ficha') as mock_sacar:
            self.juego.sacar_ficha_del_tablero(23) # Necesita dado 1 (24-23)
            mock_sacar.assert_called_with(23, 'B')
            self.assertEqual(self.juego.__movimientos_disponibles__, [3]) # Dado 1 consumido

        # Caso Error (Dado no disponible)
        with self.assertRaises(ValueError) as context:
            self.juego.sacar_ficha_del_tablero(20) # Necesita dado 4, solo tiene [3]
        self.assertIn("no está permitido por los dados", str(context.exception))

        # --- Jugador 2 (Negro) ---
        self.juego.cambiar_turno()
        self.juego.__movimientos_disponibles__ = [5, 6] # Dado 6 para punto 5
        
        with patch.object(self.juego.__tablero__, 'sacar_ficha') as mock_sacar:
            self.juego.sacar_ficha_del_tablero(5) # Necesita dado 6 (5+1)
            mock_sacar.assert_called_with(5, 'N')
            self.assertEqual(self.juego.__movimientos_disponibles__, [5]) # Dado 6 consumido

    def test_sacar_ficha_cuadrante_incorrecto(self):
        """
        Verifica que sacar ficha falla si no es desde el cuadrante de salida.
        """
        self.juego.__movimientos_disponibles__ = [1, 2] 
        
        with self.assertRaises(ValueError) as context:
            self.juego.sacar_ficha_del_tablero(10)
        self.assertIn("solo pueden sacarse desde puntos 18-23", str(context.exception))

        self.juego.cambiar_turno()
        self.juego.__movimientos_disponibles__ = [1, 2]
        
        with self.assertRaises(ValueError) as context:
            self.juego.sacar_ficha_del_tablero(10)
        self.assertIn("solo pueden sacarse desde puntos 0-5", str(context.exception))

    def test_sacar_ficha_con_ficha_en_barra(self):
        """Verifica que no se puede sacar ficha si hay fichas en la barra."""
        with patch.object(self.juego, 'jugador_actual_tiene_fichas_en_barra', return_value=True):
            with self.assertRaises(ValueError) as context:
                self.juego.sacar_ficha_del_tablero(23)
            self.assertIn("Debe reincorporar", str(context.exception))

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
        self.assertIsNone(self.juego.obtener_ganador())
        self.juego.__ganador__ = self.juego.__jugador1__
        self.assertEqual(self.juego.obtener_ganador(), self.juego.__jugador1__)

    def test_obtener_estado_tablero(self):
        """Cubre obtener_estado_tablero()."""
        estado_crudo = [['N', 'N'], [], ['B']]
        estado_crudo.extend([[] for _ in range(21)])
        
        with patch.object(self.juego.__tablero__, 'obtener_estado', return_value=estado_crudo):
            estado_dict = self.juego.obtener_estado_tablero()
            estado_esperado = {0: ['N', 'N'], 2: ['B']}
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
    def test_obtener_movimientos_disponibles(self):
        """Prueba el nuevo 'getter' para los movimientos."""
        # 1. Al inicio, la lista debe estar vacía
        self.assertEqual(self.juego.obtener_movimientos_disponibles(), [])
        
        # 2. Después de asignarlos, debe devolverlos
        self.juego.__movimientos_disponibles__ = [5, 5]
        self.assertEqual(self.juego.obtener_movimientos_disponibles(), [5, 5])
    

if __name__ == '__main__':
    unittest.main()