"""
MODULO: determinant.py

DESCRIPCION:
Modulo encargado de calcular el determinante de una matriz cuadrada. En el
proyecto se usa para matrices 2x2 y 3x3 ingresadas por el usuario.

PROPOSITO:
Determinar si el sistema matricial tiene solucion estable o si puede presentar
singularidad estructural.

ENTRADAS:
matrix -> Matriz cuadrada de NumPy con valores numericos.

SALIDAS:
Determinante de la matriz como numero decimal.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Creacion de modulos
- Definicion de funciones
- Retorno de valores
- Determinante de matrices

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

import numpy as np


def calculate_determinant(matrix: np.ndarray) -> float:
    """
    Calcula:
    determinante = det(A)

    Entradas:
        matrix -> Matriz cuadrada A de tamano 2x2 o 3x3.

    Salida:
        Valor numerico del determinante.

    Restricciones:
        La matriz debe ser cuadrada. En este proyecto se valida previamente que
        solo sea 2x2 o 3x3.
    """
    return float(np.linalg.det(matrix))
