"""
MODULO: export_images.py

DESCRIPCION:
Modulo encargado de guardar las graficas generadas por Matplotlib como imagenes
PNG dentro de la carpeta outputs/graphs.

PROPOSITO:
Permitir que las visualizaciones del analisis se usen en reportes, evidencias e
infografias del proyecto.

ENTRADAS:
figures -> Diccionario de figuras de Matplotlib.
prefix -> Texto opcional para nombrar los archivos.

SALIDAS:
Diccionario con las rutas de las imagenes guardadas.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Exportacion de archivos
- Graficas Matplotlib
- Guardado de imagenes
- Manejo de rutas

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from matplotlib.figure import Figure

from src.config.settings import GRAPHS_DIR, ensure_output_dirs


def save_figures(figures: dict[str, Figure], prefix: str | None = None) -> dict[str, Path]:
    """
    Calcula:
    guardado de cada figura como archivo PNG.

    Entradas:
        figures -> Diccionario con nombre de grafica y objeto Figure.
        prefix -> Prefijo opcional para los nombres de archivo.

    Salida:
        Diccionario con nombre de grafica y ruta del PNG generado.

    Restricciones:
        Requiere permiso de escritura en outputs/graphs.
    """
    ensure_output_dirs()
    if prefix is None:
        prefix = datetime.now().strftime("analysis_%Y%m%d_%H%M%S")

    paths: dict[str, Path] = {}
    for name, figure in figures.items():
        path = GRAPHS_DIR / f"{prefix}_{name}.png"
        figure.savefig(path, dpi=160, bbox_inches="tight")
        paths[name] = path
    return paths
