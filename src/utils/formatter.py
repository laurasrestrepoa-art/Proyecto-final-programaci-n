"""
========================================
MODULE: formatter.py

DESCRIPTION:
    Módulo con funciones auxiliares para convertir números, matrices y vectores en
    texto legible dentro de la interfaz y los reportes.

PURPOSE:
    Mostrar resultados matemáticos de forma clara, evitando que NumPy imprima datos
    con formatos dificiles de leer para la sustentacion.

INPUT:
    - Valores numéricos, matrices o vectores de NumPy.

OUTPUT:
    - Cadenas de texto listas para mostrarse en pantalla o PDF.

TOPICS RELATED TO THIS MODULE:
    - Formato de salida
    - Números reales y complejos
    - Matrices
    - Vectores

AUTHORS:
    Isabella Mejía Urueña
    Laura Sofía Restrepo Ardila

VERSION:
    3.O

CREATION DATE:
    2026-05-15

LAST UPDATE:
    2026-05-23
========================================
"""

from __future__ import annotations

import math

import numpy as np


def format_number(value: complex | float | int, decimals: int = 4) -> str:
    """
    Calculate:
    Representación textual de un número real o complejo.

    Fórmula usada:
    valor_formateado = número redondeado a una cantidad fija de decimales.

    Input:
        - value -> Número real, entero o complejo.
        - decimals -> Cantidad de decimales a mostrar.

    Output:
        - Texto con el número formateado.

    Restrictions:
        Si el número complejo tiene partes cercanas a cero, se muestran como
        cero para mejorar la lectura.
    """
    value = np.real_if_close(value, tol=1000)
    if isinstance(value, np.ndarray):
        value = value.item()
    if isinstance(value, complex):
        real = 0.0 if math.isclose(value.real, 0.0, abs_tol=1e-10) else value.real
        imag = 0.0 if math.isclose(value.imag, 0.0, abs_tol=1e-10) else value.imag
        sign = "+" if imag >= 0 else "-"
        return f"{real:.{decimals}f} {sign} {abs(imag):.{decimals}f}i"
    return f"{float(value):.{decimals}f}"


def format_matrix(matrix: np.ndarray | None, decimals: int = 3) -> str:
    """
    Calculate:
    Representación de una matriz como texto por filas.

    Input:
        - matrix -> Matriz de NumPy o None.
        - decimals -> Cantidad de decimales por elemento.

    Output:
        - Texto con la matriz organizada por filas.

    Restrictions:
        Si matrix es None, retorna "No disponible".
    """
    if matrix is None:
        return "No disponible"
    rows = []
    for row in matrix:
        rows.append("  ".join(format_number(value, decimals) for value in row))
    return "\n".join(rows)


def format_vector(vector: np.ndarray, decimals: int = 4) -> str:
    """
    Calculate:
    Representación de un vector en una sola linea.

    Input:
        - vector -> Vector de NumPy.
        - decimals -> Cantidad de decimales por componente.

    Output:
        - Texto con formato [v1, v2, v3].

    Restrictions:
        El vector debe contener valores numéricos.
    """
    return "[" + ", ".join(format_number(value, decimals) for value in vector) + "]"
