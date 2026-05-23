"""
MODULO: settings.py

DESCRIPCION:
Modulo de configuracion general del proyecto. Define rutas principales,
carpetas de salida y constantes usadas por la aplicacion.

PROPOSITO:
Centralizar las rutas para que los demas modulos no escriban direcciones de
carpetas manualmente.

ENTRADAS:
No recibe datos del usuario. Calcula rutas a partir de la ubicacion del archivo.

SALIDAS:
Constantes de ruta y funcion para crear carpetas de salida.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Configuracion de proyecto
- Manejo de rutas
- Carpetas de salida
- Reutilizacion de constantes

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
GRAPHS_DIR = OUTPUTS_DIR / "graphs"
MATRICES_DIR = OUTPUTS_DIR / "matrices"

APP_NAME = "StructuraLab"
APP_SUBTITLE = "Analisis estructural matricial"


def ensure_output_dirs() -> None:
    """
    Calcula:
    creacion de carpetas necesarias para guardar resultados.

    Entradas:
        No recibe parametros.

    Salida:
        No retorna valores. Crea carpetas si no existen.

    Restricciones:
        Requiere permiso de escritura en la carpeta del proyecto.
    """
    for path in (OUTPUTS_DIR, REPORTS_DIR, GRAPHS_DIR, MATRICES_DIR):
        path.mkdir(parents=True, exist_ok=True)
