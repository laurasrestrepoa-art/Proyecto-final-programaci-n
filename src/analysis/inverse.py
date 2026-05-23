"""
=========================================================
MODULE: inverse.py

DESCRIPTION:
    Este módulo contiene la función encargada
    de calcular la matriz inversa de una matriz
    cuadrada.
    
PURPOSE:
    Determinar si una matriz puede invertirse
    a partir de su determinante.

    En análisis estructural, una matriz no
    invertible puede relacionarse con problemas
    de singularidad o falta de restricciones
    en el sistema.

INPUT:
    - Matriz cuadrada de NumPy denominada matrix.

OUTPUT:
    - Matriz inversa de A.
    - Valor None si la matriz es singular.

TOPICS RELATED TO THIS MODULE:
    - Inversa de matrices
    - Sistemas lineales
    - Manejo de excepciones
    - Validación matemática

AUTHORS:
    Isabella Mejía Urueña
    Laura Sofía Restrepo Ardila

VERSION:
    4.0

CREATION DATE:
    2026-05-15

LAST UPDATE:
    2026-05-23
=========================================================
"""

from __future__ import annotations

# Importación de la librería NumPy.
import numpy as np


def calculate_inverse(matrix: np.ndarray) -> np.ndarray | None:
    """
    Esta función calcula la matriz inversa
    de una matriz cuadrada.
    
    Es decir, se calcula
        A^-1
        
    Cumpliendo que: 
        A * A^-1 = I

    Donde: 
        A -> Matriz original.
        A^-1 -> Matriz inversa.
        I -> Matriz identidad.

    Input:
        matrix -> Matriz cuadrada A.

     Output:
        - Matriz inversa si existe.
        - Valor None si la matriz es singular.

    Restricciones:
        - La inversa solo existe cuando det(A) es diferente de cero.
    """
    try:
        return np.linalg.inv(matrix)
    except np.linalg.LinAlgError:
        return None
