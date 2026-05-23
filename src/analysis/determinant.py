"""
MÓDULO: determinant.py

DESCRIPCIÓN:
  Este módulo encargado de calcular el determinante de una matriz cuadrada. En el
  proyecto se usa para matrices 2x2 y 3x3 ingresadas por el usuario.

PROPOSITO:
   Determinar si el sistema matricial tiene solución estable o si 
   puede presentar singularidad () estructural.

ENTRADAS:
   - Matriz cuadrada con valores numéricos.

SALIDAS:
   - Valor del determinante de la matriz como número decimal.

TEMAS RELACIONADOS CON ESTE MÓDULO:
  - Definición de funciones
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

    Restricción:
      - La matriz debe ser cuadrada.

    Input:
      - Matriz 2x2 o 3x3.

    Output:
      - Determinante de la matriz.
    """
    return float(np.linalg.det(matrix))
