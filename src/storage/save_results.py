"""
=========================================================
MODULE: save_results.py

DESCRIPTION:
    Este es el módulo encargado de guardar un historial resumido 
    de los análisis realizados por el programa.

    La información se almacena en un archivo JSON, el cual permite
    organizar datos estructurados de manera más sencilla.

PURPOSE:
    Permitir que el proyecto conserve evidencia de matrices analizadas, 
    junto con sus resultados principales y niveles de riesgo obtenidos.

INPUT:
    - Resultado del análisis denominado result.

OUTPUT:
    - Ruta del archivo history.json actualizado.

TOPICS RELATED TO THIS MODULE:
    - Persistencia de datos
    - Archivos JSON
    - Historial de ejecución
    - Resultados de análisis

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

# Se importa la librería json para guardar información
# en archivos JSON
import json

# Se importan datetime para registar fecha y hora de cada análisis
# y tmabién Path para el manejo de rutas y carpetas del proyecto.
from datetime import datetime
from pathlib import Path

# Resultado principal del análisis estructural
# y carpetas y funciones de configuración
from src.analysis.structural_solver import AnalysisResult
from src.config.settings import MATRICES_DIR, ensure_output_dirs


def append_history(result: AnalysisResult) -> Path:
    """
    Esta función agrega un nuevo análisis
    al historial del proyecto.

    La información se almacena dentro
    del archivo history.json.

    Input:
        result -> Resultado completo del analisis actual.

    Output:
        - Ruta del archivo JSON donde se guardó el historial.

    Restrictions:
        - Los valores propios se convierten a float para poder escribirse en JSON.
    """
        # Creación de carpetas.
    ensure_output_dirs()

    # Ruta del archivo hiatorial.
    path = MATRICES_DIR / "history.json"
    if path.exists():
        entries = json.loads(path.read_text(encoding="utf-8"))
    else:
        entries = []

    entries.append(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "matrix": result.matrix.tolist(),
            "determinant": result.determinant,
            "trace": result.trace,
            "eigenvalues": [float(value) for value in result.eigenvalues],
            "risk_level": result.stability.risk_level,
            "status": result.stability.status,
        }
    )
    path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    return path
