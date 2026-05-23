"""
========================================
MODULE: trace.py

DESCRIPTION:
    Este Módulo es el encargado de calcular la traza de una matriz cuadrada, es decir, la suma
    de los elementos ubicados en la diagonal principal.

PURPOSE:
    Complementar el análisis matricial mostrando una medida global de rigidez
    asociada a los términos diagonales de la matriz.

INPUT:
    - matrix -> Matriz cuadrada de NumPy.

OUTPUT:
    - Traza de la matriz como número decimal.

TOPICS RELATED TO THIS MODULE:
    - Funciones matemáticas
    - Diagonal principal
    - Retorno de valores
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


def calculate_trace(matrix: np.ndarray) -> float:
    """
    Calculate:
    Traza(A) = a11 + a22 + ... + ann

    Input:
        matrix -> Matriz cuadrada A.

    Output:
        Suma de los elementos de la diagonal principal.

    Restrictions:
        La matriz debe ser cuadrada para que la diagonal principal represente el
        sistema correctamente.
    """
    return float(np.trace(matrix))
