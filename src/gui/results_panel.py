"""
=========================================================
MODULE: results_panel.py

DESCRIPTION:
    Módulo que muestra los resultados numéricos e interpretativos del análisis
    estructural en la interfaz gráfica.

PURPOSE:
    Presentar al usuario el determinante, traza, inversa, transpuesta, valores
    propios, vectores propios, nivel de riesgo y conclusión estructural.

INPUT:
    - result -> Objeto AnalysisResult con los datos calculados.

OUTPUT:
    - Texto organizado dentro de un panel de resultados.

TOPICS RELATED TO THIS MODULE:
    - Visualización de resultados
    - Interfaz gráfica
    - Formato de matrices
    - Interpretación estructural

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

from PyQt6.QtWidgets import QFrame, QLabel, QTextEdit, QVBoxLayout, QWidget

from src.analysis.structural_solver import AnalysisResult
from src.utils.formatter import format_matrix, format_number, format_vector


class ResultsPanel(QFrame):
    """
    Represents:
    Panel lateral de resultados matemáticos y estructurales.

    Input:
        - parent -> Componente visual padre opcional.

    Output:
        - Componente visual listo para agregarse a la ventana principal.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Calculate:
        Inicialización del panel de resultados.

        Input:
            - parent -> Componente visual padre opcional.

        Output:
            - No retorna valores. Construye el panel visual.

        Restrictions:
            Debe usarse dentro de una aplicación PyQt6.
        """
        super().__init__(parent)
        self.setObjectName("ResultsPanel")
        self._build_ui()

    def _build_ui(self) -> None:
        """
        Calculate:
        Creación de etiquetas y caja de texto para resultados.

        Input:
            - No recibe parametros.

        Output:
            - No retorna valores. Agrega elementos al panel.

        Restrictions:
            Solo define interfaz; no realiza cálculos matemáticos.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel("Resultados")
        title.setStyleSheet("font-size: 14pt; font-weight: 700;")
        layout.addWidget(title)

        self.summary = QTextEdit()
        self.summary.setReadOnly(True)
        self.summary.setMinimumWidth(340)
        self.summary.setPlaceholderText("Ejecuta un analisis para ver resultados.")
        layout.addWidget(self.summary, stretch=1)

    def display_result(self, result: AnalysisResult) -> None:
        """
        Calculate:
        Conversión del resultado numérico en texto legible.

        Input:
            - result -> Resultado completo del análisis matricial.

        Salida:
            - No retorna valores. Escribe el resumen en el QTextEdit.

        Restrictions:
            Requiere que result haya sido generado por analyze_matrix.
        """
        lines: list[str] = []
        lines.append("RESUMEN MATEMATICO")
        lines.append("")
        lines.append(f"Determinante: {format_number(result.determinant)}")
        lines.append(f"Traza: {format_number(result.trace)}")
        lines.append(f"Estado: {result.stability.status}")
        lines.append(f"Nivel de riesgo: {result.stability.risk_level}")
        lines.append(f"Condicion numerica: {format_number(result.stability.condition_number)}")
        lines.append(f"Simetrica: {'Si' if result.stability.is_symmetric else 'No'}")
        lines.append(
            f"Dominancia diagonal: {'Si' if result.stability.is_diagonally_dominant else 'No'}"
        )
        lines.append("")
        lines.append("VALORES PROPIOS")
        for index, value in enumerate(result.eigenvalues, start=1):
            lines.append(f"lambda {index}: {format_number(value)}")

        lines.append("")
        lines.append("VECTORES PROPIOS")
        for index, vector in enumerate(result.eigenvectors.T, start=1):
            lines.append(f"Modo {index}: {format_vector(vector)}")

        lines.append("")
        lines.append("MATRIZ INVERSA")
        lines.append(format_matrix(result.inverse))

        lines.append("")
        lines.append("MATRIZ TRANSPUESTA")
        lines.append(format_matrix(result.transpose))

        lines.append("")
        lines.append(result.interpretation)

        self.summary.setPlainText("\n".join(lines))
