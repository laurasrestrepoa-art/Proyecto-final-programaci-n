"""
=========================================================
MODULE: test_analysis.py

DESCRIPTION:
    Este módulo contiene pruebas automáticas para verificar 
    que los cálculos y funciones principales del proyecto 
    funcionen de manera correcta.

PURPOSE:
    Comprobar el cálculo del determinante, el análisis 
    estructural, la validación de matrices y la detección
    de matrices críticas antes de entregar el proyecto.

INPUT:
    - Matrices de prueba creadas dentro de cada función.

OUTPUT:
    - Resultados de unittest indicando si las pruebas fueron 
      aprobadas o fallidas.

TOPICS RELATED TO THIS MODULE:
    - Pruebas unitarias
    - Validación de funciones
    - Resultados esperados
    - Calidad de software

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

# Se importa unittest para realizar
# pruebas automáticas del programa.
import unittest

import numpy as np

from src.analysis.determinant import calculate_determinant
from src.analysis.structural_solver import analyze_matrix
from src.utils.validations import validate_matrix


class AnalysisTests(unittest.TestCase):
    """
    Esta clase contiene diferentes pruebas
    automáticas para comprobar el correcto
    funcionamiento del módulo de análisis.

    Input:
        - Matrices de prueba.

    Output:
        - Verificación de resultados esperados.

    Restricctions: 
        - Ninguna.
    """

    
    def test_determinant_for_stable_2x2_matrix(self) -> None:
        """
        Esta prueba verifica el cálculo del
        determinante de una matriz estable 2x2.

        Fórmula utilizada:
        det([[4, -2], [-2, 4]]) = 4*4 - (-2*-2) = 12

        Input:
            - Matriz [[4, -2], [-2, 4]].

        Output:
            - Prueba aprobada si el determinante es 12.
        """
        
        matrix = np.array([[4, -2], [-2, 4]], dtype=float)
        self.assertAlmostEqual(calculate_determinant(matrix), 12.0)
        

    def test_complete_analysis_detects_low_risk(self) -> None:
        """
        La prueba presentada verifica que una matriz estable 
        sea clasificada como riesgo bajo.

        Input:
            - Matriz simetrica y diagonal dominante [[4, -2], [-2, 4]].

        Output:
            - Prueba aprobada si el riesgo es Bajo y existen dos valores propios.

        Restrictions:
            - Depende de las reglas definidas en stability_analysis.py.
        """
        matrix = np.array([[4, -2], [-2, 4]], dtype=float)
        result = analyze_matrix(matrix)
        self.assertEqual(result.stability.risk_level, "Bajo")
        self.assertTrue(result.stability.is_diagonally_dominant)
        self.assertEqual(len(result.eigenvalues), 2)

    
    def test_validation_rejects_4x4_matrix(self) -> None:
        """
        Esta prueba verifica que el programa
        rechace matrices fuera del tamaño
        permitido.

        Input:
            - Matriz identidad 4x4.

        Output:
            - Prueba aprobada si validate_matrix retorna False.

        Restrictions:
            - El proyecto solo acepta matrices 2x2 o 3x3.
        """
        valid, message = validate_matrix(np.eye(4))
        self.assertFalse(valid)
        self.assertIn("2x2 o 3x3", message)
        

    def test_critical_singular_matrix(self) -> None:
        """
        Esta prueba verifica la detección
        de matrices singulares o críticas.

        Fórmula utilizada:
        det([[2, 4], [1, 2]]) = 2*2 - 4*1 = 0

        Input:
            - Matriz [[2, 4], [1, 2]].

        Output:
            - Prueba aprobada si el nivel de riesgo es Critico.
        """
        matrix = np.array([[2, 4], [1, 2]], dtype=float)
        result = analyze_matrix(matrix)
        self.assertEqual(result.stability.risk_level, "Critico")


if __name__ == "__main__":
    unittest.main()
