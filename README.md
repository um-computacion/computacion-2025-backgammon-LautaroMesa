# Backgammon (Computación 2025)

Alumno: Lautaro Mesa

Este proyecto implementa el juego de Backgammon con dos interfaces:
- CLI (consola interactiva por menús)
- Pygame (interfaz gráfica con mouse)

El motor del juego (core) incluye reglas de orientación correctas, reintegro desde barra, "dado mayor" para sacar fichas y auto-pase de turno cuando no hay movimientos.

---

## Prerrequisitos

- Python 3.11+
- (Opcional pero recomendado) Entorno virtual de Python

Pasos sugeridos (Windows PowerShell):

```powershell
# Crear entorno virtual
python -m venv .venv

# Activar el entorno
.venv\Scripts\Activate.ps1 o .venv\Scripts\Activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## Cómo ejecutar

### Opción 1: CLI (texto)

Ejecuta la interfaz de consola (pedirá los nombres y guiará turno a turno):

```powershell
python -m cli.cli
```

Características del CLI:
- Presiona Enter cuando se te indique para tirar los dados.
- Verás el tablero en ASCII y los dados restantes del turno.
- Menú por turno basado en el estado:
  - Si hay fichas en la barra:
    1. Reincorporar ficha desde la barra
    2. Ver tablero
    3. Salir (abandonar la partida)
  - Si NO hay fichas en la barra:
    1. Mover ficha
    2. (Si corresponde) Sacar ficha del tablero
    3. Ver tablero
    4. Pasar turno (finalizar)
    5. Salir (abandonar la partida)
- Auto-pase: si el reingreso desde la barra está bloqueado para todos los dados, o si no existen movimientos posibles, el turno se pasa automáticamente y se informa el motivo.

Notas:
- La numeración visible del tablero va de 1 a 24, alineada con la interfaz.
- Las blancas avanzan hacia índices menores en el motor; las opciones del menú convierten puntos 1..24 a los índices internos por ti.

### Opción 2: Pygame (gráfica)

Ejecuta la interfaz visual con mouse:

```powershell
python .\main_pygame.py
```

Flujo básico en Pygame:
- Al inicio, ingresá los nombres de los jugadores en la pantalla de bienvenida (Enter para confirmar cada uno).
- Hacé clic en el botón "Lanzar" para tirar los dados cuando corresponda.
- Seleccioná un punto del tablero y luego un destino válido. Si estás habilitado para sacar, podés hacer clic en el área "Fuera" para borne-off.
- Si no querés (o no podés) continuar, usá el botón "Pasar turno".
- Los mensajes de error/ayuda aparecen superpuestos en pantalla.
- La UI muestra contador de fichas en la barra y un panel lateral con progreso de fichas fuera (borne-off) para ambos jugadores.

Controles (resumen):
- Mouse click: seleccionar fichas, destinos, botón de lanzar y pasar turno.
- Cerrar ventana: salir del juego.

---

## Reglas implementadas (resumen)

- Reincorporación desde barra:
  - Blancas: puntos 1..6 (índices 0..5)
  - Negras: puntos 19..24 (índices 18..23)
  - No se puede reingresar a puntos bloqueados (2+ del rival).
- Movimiento y dirección:
  - Blancas se mueven hacia índices menores; Negras hacia mayores (en el motor).
- Sacar fichas (borne-off):
  - Solo cuando todas tus fichas están en tu casa.
  - Dado exacto, o "dado mayor" únicamente para la ficha más alejada en casa.
- Auto-pase de turno:
  - Barra bloqueada para todos los dados.
  - Sin movimientos legales en el tablero.

---

## Tests y Cobertura (opcional)

Ejecutar tests:
```powershell
python -m unittest -q
```

Medir coverage:
```powershell
coverage run -m unittest -q
coverage report -m
```

Notas para desarrollo:
- Los tests no abren el CLI gracias a una guarda por variable de entorno en `cli/cli.py`.
- Para ejecutar manualmente el CLI, usá `python -m cli.cli` (sin la variable `BACKGAMMON_SKIP_MAIN=1`).

---

## Estructura del proyecto (resumen)

- `core/`: motor del juego (tablero, dados, jugadores y reglas)
- `cli/cli.py`: interfaz de línea de comandos
- `pygame_ui/`: interfaz gráfica en Pygame
- `main_pygame.py`: punto de entrada de Pygame
- `test/`: suite de unit tests

---

## Solución de problemas

- Si Pygame no está instalado: `pip install pygame`
- Si no abre la ventana en Windows, verificá que el entorno virtual esté activo y que los assets estén en `assets/`.
- En PowerShell, si algún comando falla por permisos, probá ejecutar la consola "Como administrador" o ajustá el ExecutionPolicy.

-
