"""
MODULO: formatter.py

DESCRIPCION:
Modulo con funciones auxiliares para convertir numeros, matrices y vectores en
texto legible dentro de la interfaz y los reportes.

PROPOSITO:
Mostrar resultados matematicos de forma clara, evitando que NumPy imprima datos
con formatos dificiles de leer para la sustentacion.

ENTRADAS:
Valores numericos, matrices o vectores de NumPy.

SALIDAS:
Cadenas de texto listas para mostrarse en pantalla o PDF.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Formato de salida
- Numeros reales y complejos
- Matrices
- Vectores

AUTOR:
Laura y equipo de trabajo
"""

from __future__ import annotations

import math

import numpy as np


def format_number(value: complex | float | int, decimals: int = 4) -> str:
    """
    Calcula:
    representacion textual de un numero real o complejo.

    Formula usada:
    valor_formateado = numero redondeado a una cantidad fija de decimales.

    Entradas:
        value -> Numero real, entero o complejo.
        decimals -> Cantidad de decimales a mostrar.

    Salida:
        Texto con el numero formateado.

    Restricciones:
        Si el numero complejo tiene partes cercanas a cero, se muestran como
        cero para mejorar la lectura.
    """
    value = np.real_if_close(value, tol=1000)
    if isinstance(value, np.ndarray):
        value = value.item()
    if isinstance(value, complex):
        real = 0.0 if math.isclose(value.real, 0.0, abs_tol=1e-10) else value.real
        imag = 0.0 if math.isclose(value.imag, 0.0, abs_tol=1e-10) else value.imag
        sign = "+" if imag >= 0 else "-"
        return f"{real:.{decimals}f} {sign} {abs(imag):.{decimals}f}i"
    return f"{float(value):.{decimals}f}"


def format_matrix(matrix: np.ndarray | None, decimals: int = 3) -> str:
    """
    Calcula:
    representacion de una matriz como texto por filas.

    Entradas:
        matrix -> Matriz de NumPy o None.
        decimals -> Cantidad de decimales por elemento.

    Salida:
        Texto con la matriz organizada por filas.

    Restricciones:
        Si matrix es None, retorna "No disponible".
    """
    if matrix is None:
        return "No disponible"
    rows = []
    for row in matrix:
        rows.append("  ".join(format_number(value, decimals) for value in row))
    return "\n".join(rows)


def format_vector(vector: np.ndarray, decimals: int = 4) -> str:
    """
    Calcula:
    representacion de un vector en una sola linea.

    Entradas:
        vector -> Vector de NumPy.
        decimals -> Cantidad de decimales por componente.

    Salida:
        Texto con formato [v1, v2, v3].

    Restricciones:
        El vector debe contener valores numericos.
    """
    return "[" + ", ".join(format_number(value, decimals) for value in vector) + "]"
