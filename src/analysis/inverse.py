"""
MODULO: inverse.py

DESCRIPCION:
Modulo encargado de calcular la matriz inversa cuando el determinante permite
realizar la operacion.

PROPOSITO:
Identificar si el sistema matricial puede invertirse. En analisis estructural,
una matriz no invertible puede indicar singularidad o falta de restricciones.

ENTRADAS:
matrix -> Matriz cuadrada de NumPy.

SALIDAS:
Matriz inversa A^-1 o None si la matriz es singular.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Inversa de matrices
- Manejo de excepciones
- Sistemas lineales
- Validacion matematica

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

import numpy as np


def calculate_inverse(matrix: np.ndarray) -> np.ndarray | None:
    """
    Calcula:
    A^-1, donde A * A^-1 = I

    Entradas:
        matrix -> Matriz cuadrada A.

    Salida:
        Matriz inversa si existe. Si A es singular, retorna None.

    Restricciones:
        La inversa solo existe cuando det(A) es diferente de cero.
    """
    try:
        return np.linalg.inv(matrix)
    except np.linalg.LinAlgError:
        return None
