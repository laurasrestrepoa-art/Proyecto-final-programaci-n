"""
========================================
MODULO: structural_interpreter.py

DESCRIPTION:
   Este módulo genera una interpretación escrita del análisis estructural a partir del determinante, 
   los valores propios, los vectores propios y la clasificación de estabilidad.

PURPOSE:
    Convertir resultados numéricos en conclusiones comprensibles para el taller, relacionando 
    el álgebra lineal con la estabilidad, la rigidez, la torsión y la deformación.

INPUT:
    - matrix -> Matriz analizada.
    - determinant -> Determinante de la matriz.
    - eigenvalues -> Valores propios.
    - eigenvectors -> Vectores propios.
    - stability -> Resultado de clasificación estructural.

OUTPUT:
    - Texto en español con interpretación matemática e ingenieril.

TOPICS RELATED TO THIS EXAMPLE:
    - Interpretación de resultados
    - Análisis estructural matricial
    - Modos de deformación
    - Conclusiones automáticas

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

import numpy as np

from src.analysis.stability_analysis import StabilityResult


def interpret_structure(
    matrix: np.ndarray,
    determinant: float,
    eigenvalues: np.ndarray,
    eigenvectors: np.ndarray,
    stability: StabilityResult,
) -> str:
    """
    Calculate:
    texto interpretativo a partir de reglas de análisis:
    - det(A) cercano a 0 indica posible singularidad.
    - lambda positivos sugieren estabilidad.
    - lambda negativos sugieren modo critico.
    - vectores propios indican dirección de deformación.

    Input:
        - matrix -> Matriz A.
        - determinant -> Determinante det(A).
        - eigenvalues -> Valores propios lambda.
        - eigenvectors -> Vectores propios por columnas.
        - stability -> Objeto con indicadores de riesgo.

    Output:
        - Cadena de texto con análisis estructural y conclusión global.

    Restrictions:
        - La interpretación es educativa y depende de reglas simplificadas.
    """
    lines: list[str] = []

    lines.append("ANALISIS ESTRUCTURAL")
    lines.append("")

    if abs(determinant) < 1e-7:
        lines.append(
            "El determinante es cercano a cero. El sistema puede presentar "
            "singularidad, perdida de rigidez o dependencia entre ecuaciones."
        )
    else:
        lines.append(
            "El determinante es diferente de cero, por lo que el sistema tiene "
            "respuesta matematica definida para cargas compatibles."
        )

    if stability.positive_eigenvalues == len(eigenvalues):
        lines.append(
            "Todos los valores propios son positivos. Esto sugiere un "
            "comportamiento estable para la matriz de rigidez analizada."
        )

    if stability.negative_eigenvalues:
        lines.append(
            "Se detectaron valores propios negativos. En interpretación "
            "estructural esto representa un posible modo critico o inestable."
        )

    if stability.near_zero_eigenvalues:
        lines.append(
            "Hay valores propios cercanos a cero. Esto puede indicar un modo de "
            "deformación con muy baja resistencia."
        )

    if stability.is_diagonally_dominant:
        lines.append(
            "La matriz presenta dominancia diagonal. En términos de rigidez, "
            "cada nodo resiste más de lo que se acopla con los demás nodos."
        )
    else:
        lines.append(
            "La matriz no es claramente diagonal dominante. Las conexiones "
            "entre nodos tienen una influencia importante en la respuesta."
        )

    if stability.is_symmetric:
        lines.append(
            "La matriz es simétrica, una propiedad esperada en muchas matrices "
            "de rigidez estructural idealizadas."
        )
    else:
        lines.append(
            "La matriz no es simétrica. Esto puede representar direccionamiento "
            "de cargas, efectos no conservativos o datos que requieren revision."
        )

    lines.append("")
    lines.append("INTERPRETACION VECTORIAL Y MODAL")

    for index, vector in enumerate(eigenvectors.T, start=1):
        real_vector = np.real_if_close(vector, tol=1000).astype(float)
        dominant_axis = int(np.argmax(np.abs(real_vector)))
        axis_name = ["X", "Y", "Z"][dominant_axis]
        value = real_vector[dominant_axis]

        lines.append("")
        lines.append(f"Modo {index}:")
        lines.append(
            f"- Direccion dominante: eje {axis_name} con componente {value:.3f}."
        )

        if len(real_vector) >= 2 and abs(real_vector[0] - real_vector[1]) > 0.30:
            lines.append(
                "- Diferencia importante entre componentes X e Y: posible "
                "rotación, torsión o deformación lateral."
            )
        else:
            lines.append(
                "- Las componentes principales son relativamente equilibradas, "
                "lo que sugiere deformación más uniforme."
            )

        if len(real_vector) == 3 and abs(real_vector[2]) > 0.45:
            lines.append(
                "- La componente Z es relevante: puede interpretarse como "
                "desplazamiento vertical dentro del modelo simplificado."
            )

    lines.append("")
    lines.append("CONCLUSION GLOBAL")

    if stability.risk_level == "Bajo":
        lines.append(
            "La estructura matricial presenta condiciones favorables: estabilidad, "
            "rigidez dominante y respuesta matemática consistente."
        )
    elif stability.risk_level == "Critico":
        lines.append(
            "El sistema tiene condiciones criticas. Se recomienda revisar apoyos, "
            "conectividad, rigidez de elementos y datos de entrada."
        )
    else:
        lines.append(
            "El sistema es util para analisis, pero requiere revision ingenieril "
            "en los modos con mayor deformacion o acoplamiento."
        )

    return "\n".join(lines)
