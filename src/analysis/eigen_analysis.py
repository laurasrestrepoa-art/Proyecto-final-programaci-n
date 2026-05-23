"""
=========================================================
MODULE: eigen_analysis.py

DESCRIPTION:
    Este módulo contiene funciones para calcular valores propios, 
    vectores propios y una aproximación al análisis modal de una 
    matriz.


PURPOSE:
    Relacionar el álgebra lineal con el comportamiento físico de 
    una estructura. 
    
    A través de conceptos como valores propios, se interpreta
    la estabilidad de una estructura, ya que dichos valores se
    relacionan con frecuencias asociadas al sistema.
    
    Asimismo, los vectores propios representan modos básicos
    de deformación.


INPUT:
    - Matriz cuadrada de NumPy denominada matrix.
    - Matriz de vectores propios denominada eigenvectors.


OUTPUT:
    - Valores propios ordenados.
    - Vectores propios ordenados.
    - Porcentajes de participación modal.

TOPICS RELATED TO THIS MODULE:
    - Álgebra lineal
    - Valores propios
    - Vectores propios
    - Análisis modal
    - Ordenamiento de resultados

AUTHORS:
    Isabella Mejía Urueña
    Laura Sofía Restrepo Ardila
    
VERSION:
    3.0

CREATION DATE:
    2026-05-15

LAST UPDATE:
    2026-05-23
=========================================================
"""

from __future__ import annotations

# Se importa la librería NumPy.
import numpy as np


def calculate_eigen(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Esta función calcula los valores y
    vectores propios de una matriz usando
    la expresión matemática: 
    
    A * v =  λ * v

    Donde: 
        A es la matriz del sistema.
        v corresponde al vector propio.
        λ es el valor propio asociado.  
        
    Input:
        matrix -> Matriz cuadrada A.

    Output:
        eigenvalues -> Valores propios de λ ordenados por magnitud.
        eigenvectors -> Vectores propios v asociados a cada valor propio.

    Restricciones:
        - La matriz debe ser cuadrada de tamaño 2x2 o 3x3.
    """
    
    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    # Para organizar los valores propios de mayor a menor
    # según su magnitud
    order = np.argsort(np.abs(eigenvalues))[::-1]
    eigenvalues = np.real_if_close(eigenvalues[order], tol=1000)
    eigenvectors = np.real_if_close(eigenvectors[:, order], tol=1000)
    return eigenvalues, eigenvectors



def modal_participation(eigenvectors: np.ndarray) -> np.ndarray:
    """
    La función presentada calcula una participación
    relativa aproximada de cada modo de vibración.
    
    Es decir:
    
    participacion_i = suma(|v_i|) / suma_total_de_componentes

    Donde: 
        v_i corresponde a los componentes del vector propio
            asociado a cada modo. 

    Input:
        eigenvectors -> Matriz de vectores propios por columnas.

    Output:
        - Vector con la participación relativa de cada modo.

     Restrictions:
        - Si la suma total es cero, retorna un vector de ceros para evitar
          división entre cero.
    """
    # Suma de los valores absolutos de cada vector propio por columnas.
    weights = np.sum(np.abs(eigenvectors), axis=0)

    # Para calcular la suma total de participaciones.
    total = float(np.sum(weights))
    if total == 0:
        return np.zeros_like(weights, dtype=float)
    return weights / total
