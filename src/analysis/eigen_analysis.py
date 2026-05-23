"""
MODULO: eigen_analysis.py

DESCRIPCION:
Modulo encargado de calcular valores propios, vectores propios y participacion
modal aproximada de la matriz analizada.

PROPOSITO:
Relacionar el algebra lineal con el comportamiento fisico de la estructura. Los
valores propios se usan para interpretar estabilidad y los vectores propios se
usan como modos simplificados de deformacion.

ENTRADAS:
matrix -> Matriz cuadrada de NumPy.
eigenvectors -> Matriz cuyas columnas representan vectores propios.

SALIDAS:
Valores propios ordenados, vectores propios ordenados y porcentajes de
participacion modal.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Valores propios
- Vectores propios
- Analisis modal
- Ordenamiento de resultados

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

import numpy as np


def calculate_eigen(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Calcula:
    A * v = lambda * v

    Entradas:
        matrix -> Matriz cuadrada A.

    Salida:
        eigenvalues -> Valores propios lambda ordenados por magnitud.
        eigenvectors -> Vectores propios v asociados a cada valor propio.

    Restricciones:
        La matriz debe ser cuadrada. En este proyecto se trabaja con matrices
        2x2 o 3x3.
    """
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    order = np.argsort(np.abs(eigenvalues))[::-1]
    eigenvalues = np.real_if_close(eigenvalues[order], tol=1000)
    eigenvectors = np.real_if_close(eigenvectors[:, order], tol=1000)
    return eigenvalues, eigenvectors


def modal_participation(eigenvectors: np.ndarray) -> np.ndarray:
    """
    Calcula:
    participacion_i = suma(|v_i|) / suma_total_de_componentes

    Entradas:
        eigenvectors -> Matriz de vectores propios por columnas.

    Salida:
        Vector con la participacion relativa de cada modo.

    Restricciones:
        Si la suma total es cero, retorna un vector de ceros para evitar
        division entre cero.
    """
    weights = np.sum(np.abs(eigenvectors), axis=0)
    total = float(np.sum(weights))
    if total == 0:
        return np.zeros_like(weights, dtype=float)
    return weights / total
