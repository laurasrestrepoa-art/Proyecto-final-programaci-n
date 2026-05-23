"""
MODULO: test_analysis.py

DESCRIPCION:
Modulo de pruebas automaticas para comprobar que los calculos principales del
proyecto funcionan correctamente.

PROPOSITO:
Verificar determinante, analisis completo, validacion de dimensiones y deteccion
de matrices criticas antes de entregar el proyecto.

ENTRADAS:
Matrices de prueba creadas dentro de cada caso.

SALIDAS:
Resultados de unittest indicando si las pruebas pasan o fallan.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Pruebas unitarias
- Validacion de funciones
- Resultados esperados
- Calidad de software

AUTOR:
Laura y equipo de trabajo
"""

from __future__ import annotations

import unittest

import numpy as np

from src.analysis.determinant import calculate_determinant
from src.analysis.structural_solver import analyze_matrix
from src.utils.validations import validate_matrix


class AnalysisTests(unittest.TestCase):
    """
    Representa:
    conjunto de pruebas automaticas para el modulo de analisis.

    Entradas:
        Matrices definidas en cada metodo de prueba.

    Salida:
        Aserciones aprobadas o fallidas segun el resultado obtenido.
    """

    def test_determinant_for_stable_2x2_matrix(self) -> None:
        """
        Calcula:
        verificacion del determinante de una matriz estable 2x2.

        Formula usada:
        det([[4, -2], [-2, 4]]) = 4*4 - (-2*-2) = 12

        Entradas:
            Matriz [[4, -2], [-2, 4]].

        Salida:
            Prueba aprobada si el determinante es 12.
        """
        matrix = np.array([[4, -2], [-2, 4]], dtype=float)
        self.assertAlmostEqual(calculate_determinant(matrix), 12.0)

    def test_complete_analysis_detects_low_risk(self) -> None:
        """
        Calcula:
        verificacion de que el analisis completo clasifica una matriz estable
        como riesgo bajo.

        Entradas:
            Matriz simetrica y diagonal dominante [[4, -2], [-2, 4]].

        Salida:
            Prueba aprobada si el riesgo es Bajo y existen dos valores propios.

        Restricciones:
            Depende de las reglas definidas en stability_analysis.py.
        """
        matrix = np.array([[4, -2], [-2, 4]], dtype=float)
        result = analyze_matrix(matrix)
        self.assertEqual(result.stability.risk_level, "Bajo")
        self.assertTrue(result.stability.is_diagonally_dominant)
        self.assertEqual(len(result.eigenvalues), 2)

    def test_validation_rejects_4x4_matrix(self) -> None:
        """
        Calcula:
        verificacion de rechazo para matrices fuera del alcance del proyecto.

        Entradas:
            Matriz identidad 4x4.

        Salida:
            Prueba aprobada si validate_matrix retorna False.

        Restricciones:
            El proyecto solo acepta matrices 2x2 o 3x3.
        """
        valid, message = validate_matrix(np.eye(4))
        self.assertFalse(valid)
        self.assertIn("2x2 o 3x3", message)

    def test_critical_singular_matrix(self) -> None:
        """
        Calcula:
        verificacion de deteccion de matriz singular o critica.

        Formula usada:
        det([[2, 4], [1, 2]]) = 2*2 - 4*1 = 0

        Entradas:
            Matriz [[2, 4], [1, 2]].

        Salida:
            Prueba aprobada si el nivel de riesgo es Critico.
        """
        matrix = np.array([[2, 4], [1, 2]], dtype=float)
        result = analyze_matrix(matrix)
        self.assertEqual(result.stability.risk_level, "Critico")


if __name__ == "__main__":
    unittest.main()
