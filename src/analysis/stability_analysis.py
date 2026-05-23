"""
========================================
MODULO: stability_analysis.py

DESCRIPTION:
   El módulo clasifica la estabilidad estructural de la matriz mediante reglas
   basadas en el determinante, los valores propios, la simetría, la dominancia 
   diagonal y la condición numérica.

PURPOSE:
    Transformar resultados matemáticos en una evaluación comprensible para el
    usuario, indicando si la matriz representa un sistema estable, crítico o con
    revisión recomendada.

INPUT:
    - matrix -> Matriz cuadrada analizada.
    - determinant -> Determinante calculado de la matriz.
    - eigenvalues -> Valores propios de la matriz.
    - tolerance -> Tolerancia numérica para comparar valores cercanos a cero.

OUTPUT:
    - Objeto StabilityResult con estado, riesgo e indicadores estructurales.

TOPICS RELATED TO THIS MODULO:
    - ClasificaciÓn de estabilidad
    - Dominancia diagonal
    - Valores propios
    - Estructuras de datos

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

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class StabilityResult:
    """
    Represents:
    resumen de indicadores usados para interpretar la estabilidad.

    Input:
        - status -> Texto con el estado general.
        - risk_level -> Nivel de riesgo calculado.
        - is_symmetric -> Indica si A = A^T.
        - is_diagonally_dominant -> Indica si la diagonal domina cada fila.
        - condition_number -> Número de condición de la matriz.
        - positive_eigenvalues -> Cantidad de valores propios positivos.
        - negative_eigenvalues -> Cantidad de valores propios negativos.
        - near_zero_eigenvalues -> Cantidad de valores propios cercanos a cero.

    Output:
        - Objeto de datos usado por la interfaz, reportes e interpretación.
    """

    status: str
    risk_level: str
    is_symmetric: bool
    is_diagonally_dominant: bool
    condition_number: float
    positive_eigenvalues: int
    negative_eigenvalues: int
    near_zero_eigenvalues: int


def is_diagonally_dominant(matrix: np.ndarray, tolerance: float = 1e-9) -> bool:
    """
    Calculate:
    |aii| >= suma(|aij|) para j diferente de i

    Input:
        matrix -> Matriz cuadrada A.
        tolerance -> Margen numérico para evitar errores por decimales.

    Output:
        True si cada fila cumple dominancia diagonal; False en caso contrario.

    Restricciones:
        La matriz debe ser cuadrada para comparar diagonal y acoplamientos.
    """
    diagonal = np.abs(np.diag(matrix))
    off_diagonal_sum = np.sum(np.abs(matrix), axis=1) - diagonal
    return bool(np.all(diagonal + tolerance >= off_diagonal_sum))


def classify_stability(
    matrix: np.ndarray,
    determinant: float,
    eigenvalues: np.ndarray,
    tolerance: float = 1e-7,
) -> StabilityResult:
    """
    Calculate:
    clasificación estructural segun reglas:
    - det(A) cercano a 0 -> sistema crítico o singular.
    - valores propios negativos -> posible modo inestable.
    - valores propios positivos + simetria + dominancia -> estable y rigido.

    Input:
        - matrix -> Matriz A.
        - determinant -> Determinante de A.
        - eigenvalues -> Valores propios de A.
        - tolerance -> Valor mínimo para considerar cero numérico.

    Salida:
        - StabilityResult con estado, nivel de riesgo e indicadores.

    Restricciones:
        El análisis es académico y simplificado; no reemplaza un cálculo
        estructural profesional.
    """
    real_values = np.real_if_close(eigenvalues, tol=1000).astype(float)
    positive = int(np.sum(real_values > tolerance))
    negative = int(np.sum(real_values < -tolerance))
    near_zero = int(len(real_values) - positive - negative)
    symmetric = bool(np.allclose(matrix, matrix.T, atol=tolerance))
    diagonal = is_diagonally_dominant(matrix, tolerance)

    if abs(determinant) <= tolerance or near_zero > 0:
        status = "Sistema singular o cercano a singular"
        risk = "Crítico"
    elif negative > 0:
        status = "Posible modo inestable"
        risk = "Alto"
    elif positive == len(real_values) and symmetric and diagonal:
        status = "Estable y rigido"
        risk = "Bajo"
    elif positive == len(real_values):
        status = "Estable con revisión recomendada"
        risk = "Medio"
    else:
        status = "Comportamiento mixto"
        risk = "Medio"

    try:
        condition = float(np.linalg.cond(matrix))
    except np.linalg.LinAlgError:
        condition = float("inf")

    return StabilityResult(
        status=status,
        risk_level=risk,
        is_symmetric=symmetric,
        is_diagonally_dominant=diagonal,
        condition_number=condition,
        positive_eigenvalues=positive,
        negative_eigenvalues=negative,
        near_zero_eigenvalues=near_zero,
    )
