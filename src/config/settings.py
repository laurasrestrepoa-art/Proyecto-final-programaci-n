"""
=========================================================
MODULE: settings.py

DESCRIPTION:
    Este es el módulo de configuración general del proyecto. 
    Define rutas principales, carpetas de salida y constantes 
    usadas por el programa.

PURPOSE:
    Guardar y organizar las rutas principales utilizadas por los
    diferentes módulos del proyecto. 

INPUTS:
    - No recibe datos del usuario. 
    - Calcula rutas a partir de la ubicación del archivo.

OUTPUTS:
    - Constantes de ruta 
    - Creación de carpetas para guardar los resultados.

TOPICS RELATED TO THIS MODULE:
    - Configuración de proyecto
    - Manejo de rutas
    - Carpetas de salida
    - Reutilización de constantes

AUTHORS:
    Isabella Mejía Urueña
    Laura Sofía Restrepo Ardila

VERSION:
    3.0

CREATION DATE:
    2026-05-15

LAST UPDATE: 
    2026-05-23
=========================================================
"""

from __future__ import annotations

# Se importa la librería utilizada para manejar rutas y carpetas 
from pathlib import Path

# Ruta principal del proyecto
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Carpetas donde se guardarán los resultados y reportes
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
GRAPHS_DIR = OUTPUTS_DIR / "graphs"
MATRICES_DIR = OUTPUTS_DIR / "matrices"

APP_NAME = "StructuraLab"
APP_SUBTITLE = "Análisis estructural matricial"


def ensure_output_dirs() -> None:
    """
    Esta función crea las carpetas necesarias 
    para guardar los resultados.

    Input:
        - No recibe parámetros.

    Output:
        - No retorna valores, solo crea carpetas si no existen.

    Restrictions:
        - Se requiere permiso de escritura en la carpeta del proyecto.
    """
    
    for path in (OUTPUTS_DIR, REPORTS_DIR, GRAPHS_DIR, MATRICES_DIR):
        path.mkdir(parents=True, exist_ok=True)


