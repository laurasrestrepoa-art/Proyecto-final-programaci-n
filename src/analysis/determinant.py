"""
MÓDULO: determinant.py

DESCRIPCIÓN:
  Este módulo encargado de calcular el determinante de una matriz cuadrada. En el
  proyecto se usa para matrices 2x2 y 3x3 ingresadas por el usuario.

PROPÓSITO:
   Determinar si el sistema matricial tiene solución estable o si 
   puede presentar singularidad estructural (cuando el determinate
   es igual a cero).

INPUT:
   - Matriz cuadrada de NumPy con valores numericos.

OUTPUT:
   - Valor del determinante de la matriz como número decimal.

TEMAS RELACIONADOS CON ESTE MODULO:
  - Definicion de funciones
  - Retorno de valores
  - Determinante de matrices

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
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
