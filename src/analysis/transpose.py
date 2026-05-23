"""
MODULO: transpose.py

DESCRIPCION:
Modulo encargado de calcular la matriz transpuesta. La transpuesta cambia filas
por columnas y permite revisar simetria de la matriz.

PROPOSITO:
Apoyar el analisis de matrices de rigidez, donde la simetria suele ser una
propiedad esperada en modelos estructurales idealizados.

ENTRADAS:
matrix -> Matriz de NumPy.

SALIDAS:
Matriz transpuesta A^T.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Transpuesta de matrices
- Simetria matricial
- Funciones con retorno
- Algebra lineal

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

import numpy as np


def calculate_transpose(matrix: np.ndarray) -> np.ndarray:
    """
    Calcula:
    A^T, donde las filas de A pasan a ser columnas.

    Entradas:
        matrix -> Matriz A.

    Salida:
        Matriz transpuesta A^T.

    Restricciones:
        No requiere que la matriz sea invertible; solo necesita valores
        numericos.
    """
    return matrix.T.copy()
