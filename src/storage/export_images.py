"""
MODULE: export_images.py

DESCRIPTION:
    Este módulo es el encargado de guardar las graficas 
    generadas por Matplotlib como imagenes PNG dentro de 
    la carpeta outputs/graphs.

PURPOSE:
    Permitir que las visualizaciones y gráficas del análisis
    estructural puedan utilizarse en reportes, evidencias o 
    presentaciones del proyecto.

INPUT:
    - Diccionario de figuras de Matplotlib
      denominado figures.
    - Texto opcional denominado prefix para
      nombrar los archivos exportados

OUTPUT:
    - Diccionario con las rutas de las imagenes guardadas.

TOPICS RELATED TO THIS MODULE:
    - Exportación de archivos
    - Gráficas en Matplotlib
    - Guardado de imágenes
    - Manejo de rutas

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


# Se importa datetime para generar nombres automáticos según la fecha y hora.
from datetime import datetime


# Importación de Path para manejar rutas y carpetas del proyecto.
from pathlib import Path


# Se importa Figure desde Matplotlib para trabajar con objetos gráficos.
from matplotlib.figure import Figure

# También se importan las carpetas de salida y la función
# encargada de crear directorios.
from src.config.settings import GRAPHS_DIR, ensure_output_dirs


def save_figures(figures: dict[str, Figure], prefix: str | None = None) -> dict[str, Path]:
    """
    Esta función guarda las gráficas
    generadas en formato PNG.

    Input:
        figures -> Diccionario con nombre de grafica y objeto Figure.
        prefix -> Prefijo opcional para los nombres de archivo.

    Output:
        - Diccionario con nombre de grafica y ruta del PNG generado.

    Restrictions:
        - Se requiere permiso de escritura en outputs/graphs.
    """
    # Creación de carpetas necesarias.
    ensure_output_dirs()
    if prefix is None:
        prefix = datetime.now().strftime("analysis_%Y%m%d_%H%M%S")

    paths: dict[str, Path] = {}

    # Se usa un ciclo for para "recorrer" cada gráfica del diccionario.
    for name, figure in figures.items():
        path = GRAPHS_DIR / f"{prefix}_{name}.png"
        figure.savefig(path, dpi=160, bbox_inches="tight")
        paths[name] = path
    return paths
