"""
=========================================================
SCRIPT: determinant.py

DESCRIPTION:
    Este módulo es el encargado de calcular el determinante de matrices 
    cuadradas 2x2 y 3x3 ingresadas por el usuario.

PURPOSE:
    Determinar si el sistema matricial tiene solución estable o si 
    puede presentar singularidad estructural, a partir del determinante
    calculado.

INPUT:
    - Matriz cuadrada de NumPy con valores numéricos.

OUTPUT:
    - Valor del determinante de la matriz como número decimal.

TOPICS RELATED TO THIS SCRIPT:
    - Definición de funciones
    - Retorno de valores
    - Determinante de matrices

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

import numpy as np


def calculate_determinant(matrix: np.ndarray) -> float:
    """
    Esta función permite calcular el
    determinante de una matriz.

    Input:
      - Matriz A de tamaño 2x2 o 3x3.

    Output:
      - Determinante de la matriz.

    Restrictions:
      - La matriz debe ser cuadrada.
    """
    return float(np.linalg.det(matrix))
