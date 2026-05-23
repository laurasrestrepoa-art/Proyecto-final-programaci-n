"""
MODULO: structural_interpreter.py

DESCRIPCION:
Modulo que genera una interpretacion escrita del analisis estructural a partir
de determinante, valores propios, vectores propios y clasificacion de
estabilidad.

PROPOSITO:
Convertir resultados numericos en conclusiones comprensibles para el taller,
relacionando algebra lineal con estabilidad, rigidez, torsion y deformacion.

ENTRADAS:
matrix -> Matriz analizada.
determinant -> Determinante de la matriz.
eigenvalues -> Valores propios.
eigenvectors -> Vectores propios.
stability -> Resultado de clasificacion estructural.

SALIDAS:
Texto en espanol con interpretacion matematica e ingenieril.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Interpretacion de resultados
- Analisis estructural matricial
- Modos de deformacion
- Conclusiones automaticas

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
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
    Calcula:
    texto interpretativo a partir de reglas de analisis:
    - det(A) cercano a 0 indica posible singularidad.
    - lambda positivos sugieren estabilidad.
    - lambda negativos sugieren modo critico.
    - vectores propios indican direccion de deformacion.

    Entradas:
        matrix -> Matriz A.
        determinant -> Determinante det(A).
        eigenvalues -> Valores propios lambda.
        eigenvectors -> Vectores propios por columnas.
        stability -> Objeto con indicadores de riesgo.

    Salida:
        Cadena de texto con analisis estructural y conclusion global.

    Restricciones:
        La interpretacion es educativa y depende de reglas simplificadas.
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
            "Se detectaron valores propios negativos. En interpretacion "
            "estructural esto representa un posible modo critico o inestable."
        )

    if stability.near_zero_eigenvalues:
        lines.append(
            "Hay valores propios cercanos a cero. Esto puede indicar un modo de "
            "deformacion con muy baja resistencia."
        )

    if stability.is_diagonally_dominant:
        lines.append(
            "La matriz presenta dominancia diagonal. En terminos de rigidez, "
            "cada nodo resiste mas de lo que se acopla con los demas nodos."
        )
    else:
        lines.append(
            "La matriz no es claramente diagonal dominante. Las conexiones "
            "entre nodos tienen una influencia importante en la respuesta."
        )

    if stability.is_symmetric:
        lines.append(
            "La matriz es simetrica, una propiedad esperada en muchas matrices "
            "de rigidez estructural idealizadas."
        )
    else:
        lines.append(
            "La matriz no es simetrica. Esto puede representar direccionamiento "
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
                "rotacion, torsion o deformacion lateral."
            )
        else:
            lines.append(
                "- Las componentes principales son relativamente equilibradas, "
                "lo que sugiere deformacion mas uniforme."
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
            "rigidez dominante y respuesta matematica consistente."
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
