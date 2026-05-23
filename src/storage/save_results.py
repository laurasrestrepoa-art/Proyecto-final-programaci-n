"""
MODULO: save_results.py

DESCRIPCION:
Modulo encargado de guardar un historial resumido de los analisis realizados en
formato JSON.

PROPOSITO:
Permitir que el proyecto conserve evidencia de matrices analizadas, resultados
principales y niveles de riesgo.

ENTRADAS:
result -> Objeto AnalysisResult generado por el motor de analisis.

SALIDAS:
Ruta del archivo history.json actualizado.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Persistencia de datos
- Archivos JSON
- Historial de ejecucion
- Resultados de analisis

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from src.analysis.structural_solver import AnalysisResult
from src.config.settings import MATRICES_DIR, ensure_output_dirs


def append_history(result: AnalysisResult) -> Path:
    """
    Calcula:
    adicion de un nuevo registro al historial.

    Entradas:
        result -> Resultado completo del analisis actual.

    Salida:
        Ruta del archivo JSON donde se guardo el historial.

    Restricciones:
        Los valores propios se convierten a float para poder escribirse en JSON.
    """
    ensure_output_dirs()
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
