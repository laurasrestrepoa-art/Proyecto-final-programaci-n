"""
MODULO: stability_analysis.py

DESCRIPCION:
Modulo que clasifica la estabilidad estructural de la matriz mediante reglas
basadas en determinante, valores propios, simetria, dominancia diagonal y
condicion numerica.

PROPOSITO:
Transformar resultados matematicos en una evaluacion comprensible para el
usuario, indicando si la matriz representa un sistema estable, critico o con
revision recomendada.

ENTRADAS:
matrix -> Matriz cuadrada analizada.
determinant -> Determinante calculado de la matriz.
eigenvalues -> Valores propios de la matriz.
tolerance -> Tolerancia numerica para comparar valores cercanos a cero.

SALIDAS:
Objeto StabilityResult con estado, riesgo e indicadores estructurales.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Clasificacion de estabilidad
- Dominancia diagonal
- Valores propios
- Estructuras de datos

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class StabilityResult:
    """
    Representa:
    resumen de indicadores usados para interpretar la estabilidad.

    Entradas:
        status -> Texto con el estado general.
        risk_level -> Nivel de riesgo calculado.
        is_symmetric -> Indica si A = A^T.
        is_diagonally_dominant -> Indica si la diagonal domina cada fila.
        condition_number -> Numero de condicion de la matriz.
        positive_eigenvalues -> Cantidad de valores propios positivos.
        negative_eigenvalues -> Cantidad de valores propios negativos.
        near_zero_eigenvalues -> Cantidad de valores propios cercanos a cero.

    Salida:
        Objeto de datos usado por la interfaz, reportes e interpretacion.
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
    Calcula:
    |aii| >= suma(|aij|) para j diferente de i

    Entradas:
        matrix -> Matriz cuadrada A.
        tolerance -> Margen numerico para evitar errores por decimales.

    Salida:
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
    Calcula:
    clasificacion estructural segun reglas:
    - det(A) cercano a 0 -> sistema critico o singular.
    - valores propios negativos -> posible modo inestable.
    - valores propios positivos + simetria + dominancia -> estable y rigido.

    Entradas:
        matrix -> Matriz A.
        determinant -> Determinante de A.
        eigenvalues -> Valores propios de A.
        tolerance -> Valor minimo para considerar cero numerico.

    Salida:
        StabilityResult con estado, nivel de riesgo e indicadores.

    Restricciones:
        El analisis es academico y simplificado; no reemplaza un calculo
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
        risk = "Critico"
    elif negative > 0:
        status = "Posible modo inestable"
        risk = "Alto"
    elif positive == len(real_values) and symmetric and diagonal:
        status = "Estable y rigido"
        risk = "Bajo"
    elif positive == len(real_values):
        status = "Estable con revision recomendada"
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
