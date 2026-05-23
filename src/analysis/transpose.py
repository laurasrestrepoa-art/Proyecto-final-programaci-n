"""
========================================
MODULO: transpose.py

DESCRIPTION:
    Este Módulo es el encargado de calcular la matriz transpuesta. La transpuesta cambia filas
    por columnas y permite revisar simétria de la matriz.

PURPOSE:
    Apoyar el análisis de matrices de rigidez, donde la simétria suele ser una
    propiedad esperada en modelos estructurales idealizados.

INPUT:
    - matrix -> Matriz de NumPy.

OUTPUT:
    - Matriz transpuesta A^T.

TOPICS RELATED TO THIS EXAMPLE:
    - Transpuesta de matrices
    - Simétria matricial
    - Funciones con retorno
    - Álgebra lineal

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

import numpy as np


def calculate_transpose(matrix: np.ndarray) -> np.ndarray:
    """
    Calculate:
    A^T, donde las filas de A pasan a ser columnas.

    Input:
        matrix -> Matriz A.

    Output:
        Matriz transpuesta A^T.

    Restrictions:
        No requiere que la matriz sea invertible; solo necesita valores
        numéricos.
    """
    return matrix.T.copy()
