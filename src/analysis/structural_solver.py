"""
========================================
SCRIPT: structural_solver.py

DESCRIPTION:
    Este es el módulo central del analisis. Une los calculos de determinante, traza, inversa,
    transpuesta, valores propios, intensidad nodal, estabilidad e interpretacion.

PURPOSE:
    Evitar que la interfaz grafica realice calculos directamente. Este modulo actua
    como el motor matematico del proyecto StructuraLab.

INPUT:
    - matrix -> Matriz cuadrada 2x2 o 3x3 ingresada por el usuario.

OUTPUT:
    - Objeto AnalysisResult con todos los resultados numericos, graficos e
      interpretativos requeridos por la interfaz y los reportes.

TOPICS RELATED TO THIS EXAMPLE:
    - Programacion modular
    - Integracion de funciones
    - Analisis matricial
    - Retorno de objetos estructurados

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

from src.analysis.determinant import calculate_determinant
from src.analysis.eigen_analysis import calculate_eigen, modal_participation
from src.analysis.inverse import calculate_inverse
from src.analysis.stability_analysis import StabilityResult, classify_stability
from src.analysis.structural_interpreter import interpret_structure
from src.analysis.trace import calculate_trace
from src.analysis.transpose import calculate_transpose


@dataclass(frozen=True)
class AnalysisResult:
    """
    Represents:
    paquete completo de resultados generados por el analisis.

    Input:
        matrix, determinant, trace, inverse, transpose, eigenvalues,
        eigenvectors, modal_participation, nodal_intensity, stability e
        interpretation.

    Output:
        Objeto organizado para que GUI, reportes y pruebas usen la misma
        informacion sin repetir calculos.
    """

    matrix: np.ndarray
    determinant: float
    trace: float
    inverse: np.ndarray | None
    transpose: np.ndarray
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray
    modal_participation: np.ndarray
    nodal_intensity: np.ndarray
    stability: StabilityResult
    interpretation: str


def calculate_nodal_intensity(matrix: np.ndarray) -> np.ndarray:
    """
    Calculate:
    intensidad_i = suma(|fila_i|) / maximo_de_intensidades

    Input:
        matrix -> Matriz A.

    Output:
        Vector normalizado de intensidad por nodo, con valores entre 0 y 1.

    Restrictions:
        Si todas las intensidades son cero, retorna el vector sin normalizar
        para evitar division entre cero.
    """
    intensity = np.sum(np.abs(matrix), axis=1)
    maximum = float(np.max(intensity)) if intensity.size else 0.0
    if maximum == 0:
        return intensity
    return intensity / maximum


def analyze_matrix(matrix: np.ndarray) -> AnalysisResult:
    """
    Calculate:
    analisis completo de una matriz estructural:
    det(A), traza(A), A^-1, A^T, valores propios, vectores propios,
    participacion modal, intensidad nodal, estabilidad e interpretacion.

    Input:
        matrix -> Matriz cuadrada 2x2 o 3x3.

    Output:
        AnalysisResult con todos los resultados del analisis.

    Restrictions:
        La matriz ya debe haber sido validada antes de llamar esta funcion.
    """
    determinant = calculate_determinant(matrix)
    trace = calculate_trace(matrix)
    inverse = calculate_inverse(matrix)
    transpose = calculate_transpose(matrix)
    eigenvalues, eigenvectors = calculate_eigen(matrix)
    participation = modal_participation(eigenvectors)
    nodal_intensity = calculate_nodal_intensity(matrix)
    stability = classify_stability(matrix, determinant, eigenvalues)
    interpretation = interpret_structure(
        matrix=matrix,
        determinant=determinant,
        eigenvalues=eigenvalues,
        eigenvectors=eigenvectors,
        stability=stability,
    )

    return AnalysisResult(
        matrix=matrix,
        determinant=determinant,
        trace=trace,
        inverse=inverse,
        transpose=transpose,
        eigenvalues=eigenvalues,
        eigenvectors=eigenvectors,
        modal_participation=participation,
        nodal_intensity=nodal_intensity,
        stability=stability,
        interpretation=interpretation,
    )
