"""
SCRIPT: trace.py

DESCRIPTION:
Modulo encargado de calcular la traza de una matriz cuadrada, es decir, la suma
de los elementos ubicados en la diagonal principal.

PURPOSE:
Complementar el analisis matricial mostrando una medida global de rigidez
asociada a los terminos diagonales de la matriz.

INPUT:
matrix -> Matriz cuadrada de NumPy.

OUTPUT:
Traza de la matriz como numero decimal.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Funciones matematicas
- Diagonal principal
- Retorno de valores
- Algebra lineal

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

import numpy as np


def calculate_trace(matrix: np.ndarray) -> float:
    """
    Calcula:
    traza(A) = a11 + a22 + ... + ann

    Entradas:
        matrix -> Matriz cuadrada A.

    Salida:
        Suma de los elementos de la diagonal principal.

    Restricciones:
        La matriz debe ser cuadrada para que la diagonal principal represente el
        sistema correctamente.
    """
    return float(np.trace(matrix))
