"""
MODULO: results_panel.py

DESCRIPCION:
Modulo que muestra los resultados numericos e interpretativos del analisis
estructural en la interfaz grafica.

PROPOSITO:
Presentar al usuario el determinante, traza, inversa, transpuesta, valores
propios, vectores propios, nivel de riesgo y conclusion estructural.

ENTRADAS:
result -> Objeto AnalysisResult con los datos calculados.

SALIDAS:
Texto organizado dentro de un panel de resultados.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Visualizacion de resultados
- Interfaz grafica
- Formato de matrices
- Interpretacion estructural

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

from PyQt6.QtWidgets import QFrame, QLabel, QTextEdit, QVBoxLayout, QWidget

from src.analysis.structural_solver import AnalysisResult
from src.utils.formatter import format_matrix, format_number, format_vector


class ResultsPanel(QFrame):
    """
    Representa:
    panel lateral de resultados matematicos y estructurales.

    Entradas:
        parent -> Componente visual padre opcional.

    Salida:
        Componente visual listo para agregarse a la ventana principal.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Calcula:
        inicializacion del panel de resultados.

        Entradas:
            parent -> Componente visual padre opcional.

        Salida:
            No retorna valores. Construye el panel visual.

        Restricciones:
            Debe usarse dentro de una aplicacion PyQt6.
        """
        super().__init__(parent)
        self.setObjectName("ResultsPanel")
        self._build_ui()

    def _build_ui(self) -> None:
        """
        Calcula:
        creacion de etiquetas y caja de texto para resultados.

        Entradas:
            No recibe parametros.

        Salida:
            No retorna valores. Agrega elementos al panel.

        Restricciones:
            Solo define interfaz; no realiza calculos matematicos.
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
        Calcula:
        conversion del resultado numerico en texto legible.

        Entradas:
            result -> Resultado completo del analisis matricial.

        Salida:
            No retorna valores. Escribe el resumen en el QTextEdit.

        Restricciones:
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
