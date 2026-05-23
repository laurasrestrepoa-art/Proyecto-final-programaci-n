"""
MODULO: validations.py

DESCRIPCION:
Modulo encargado de validar que la matriz ingresada por el usuario cumpla las
condiciones necesarias para ser analizada.

PROPOSITO:
Evitar errores matematicos y de interfaz antes de ejecutar el motor de analisis.

ENTRADAS:
matrix -> Matriz de NumPy capturada desde la interfaz.

SALIDAS:
Tupla con un valor booleano y un mensaje de error si aplica.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Validacion de datos
- Restricciones de dominio
- Matrices cuadradas
- Control de errores

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

import numpy as np


def validate_matrix(matrix: np.ndarray) -> tuple[bool, str]:
    """
    Calcula:
    verificacion de condiciones para analizar una matriz.

    Reglas usadas:
    - La matriz debe ser cuadrada.
    - Solo se aceptan tamanos 2x2 o 3x3.
    - Todos los valores deben ser finitos.
    - La matriz no puede ser completamente cero.

    Entradas:
        matrix -> Matriz ingresada por el usuario.

    Salida:
        (True, "") si es valida.
        (False, mensaje) si no cumple alguna regla.

    Restricciones:
        No realiza calculos estructurales; solo valida el dominio de entrada.
    """
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        return False, "La matriz debe ser cuadrada."

    if matrix.shape[0] not in (2, 3):
        return False, "Solo se aceptan matrices 2x2 o 3x3."

    if not np.all(np.isfinite(matrix)):
        return False, "Todos los valores deben ser numeros finitos."

    if np.allclose(matrix, 0):
        return False, "La matriz no puede estar compuesta solo por ceros."

    return True, ""
