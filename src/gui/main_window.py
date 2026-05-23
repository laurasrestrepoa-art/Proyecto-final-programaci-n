"""
=========================================================
MODULE: main_window.py

DESCRIPTION:
    Módulo que contiene la ventana principal de StructuraLab. Conecta el panel de
    entrada, el motor de analisis, las graficas, el panel de resultados y la
    exportación de reportes.

PURPOSE:
    Coordinar el flujo completo de la aplicación sin realizar cálculos matemáticos
    directamente dentro de la interfaz.

INPUT:
    - matrix -> Matriz enviada desde MatrixInputWidget.

OUTPUT:
    - Actualización visual de resultados, gráficas, historial y reportes PDF.

TOPICS RELATED TO THIS MODULE:
    - Interfaz gráfica
    - Programación modular
    - Señales y eventos
    - Integración de análisis y visualización

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

from datetime import datetime

import numpy as np
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from src.analysis.structural_solver import AnalysisResult, analyze_matrix
from src.config.settings import APP_NAME, APP_SUBTITLE, ensure_output_dirs
from src.gui.graph_view import GraphView
from src.gui.matrix_input import MatrixInputWidget
from src.gui.results_panel import ResultsPanel
from src.gui.styles import APP_STYLESHEET
from src.storage.export_pdf import export_analysis_report
from src.storage.save_results import append_history
from src.utils.formatter import format_number
from src.utils.validations import validate_matrix


class MainWindow(QMainWindow):
    """
    Represents:
    Ventana principal de la aplicación.

    Input:
        - No recibe parámetros directos al crearse.

    Output:
        Ventana gráfica con panel de entrada, gráficas y resultados.
    """

    def __init__(self) -> None:
        """
        Calculate:
        Inicialización completa de la ventana principal.

        Input:
            - No recibe parámetros.

        Output:
            - No retorna valores. Configura ventana, estilos y componentes.

        Restrictions:
            Debe ejecutarse después de crear QApplication.
        """
        super().__init__()
        ensure_output_dirs()
        self.current_result: AnalysisResult | None = None
        self.setWindowTitle(f"{APP_NAME} - {APP_SUBTITLE}")
        self.resize(1280, 760)
        self.setStyleSheet(APP_STYLESHEET)
        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        """
        Calculate:
        Construcción de la interfaz principal.

        Input:
            - No recibe parámetros.

        Output:
            - No retorna valores. Organiza titulo, paneles y separadores.

        Restrictions:
            Solo crea elementos visuales; no analiza matrices.
        """
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(18, 16, 18, 18)
        root_layout.setSpacing(12)

        title = QLabel(APP_NAME)
        title.setObjectName("TitleLabel")
        subtitle = QLabel(
            "Sistema visual para matrices 2x2 y 3x3, estabilidad, rigidez y modos."
        )
        subtitle.setObjectName("SubtitleLabel")
        root_layout.addWidget(title)
        root_layout.addWidget(subtitle)

        self.input_panel = MatrixInputWidget()
        self.graph_view = GraphView()
        self.results_panel = ResultsPanel()

        splitter = QSplitter()
        splitter.addWidget(self.input_panel)

        center_container = QWidget()
        center_layout = QHBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.addWidget(self.graph_view)
        splitter.addWidget(center_container)

        splitter.addWidget(self.results_panel)
        splitter.setSizes([280, 620, 380])
        root_layout.addWidget(splitter, stretch=1)

        self.setCentralWidget(root)

    def _connect_signals(self) -> None:
        """
        Calculate:
        Conexión entre acciones del usuario y funciones de la ventana.

        Input:
            - No recibe parámetros.

        Output:
            - No retorna valores. Conecta analizar y exportar.

        Restrictions:
            Las señales requieren que los widgets ya hayan sido creados.
        """
        self.input_panel.analyze_requested.connect(self.run_analysis)
        self.input_panel.export_requested.connect(self.export_report)

    def run_analysis(self, matrix: np.ndarray) -> None:
        """
        Calculate:
        Flujo completo de análisis de una matriz.

        Fórmula usada:
        Matriz valida -> analyze_matrix(A) -> gráficas + resultados + historial

        Input:
            - matrix -> Matriz 2x2 o 3x3 ingresada por el usuario.

        Output:
            - No retorna valores. Actualiza interfaz, graficas e historial.

        Restrictions:
            Si la matriz no cumple las validaciones, se muestra una advertencia
            y no se ejecuta el análisis.
        """
        valid, message = validate_matrix(matrix)
        if not valid:
            QMessageBox.warning(self, "Matriz invalida", message)
            return

        try:
            result = analyze_matrix(matrix)
        except Exception as exc:
            QMessageBox.critical(self, "Error de analisis", str(exc))
            return

        self.current_result = result
        self.graph_view.display_result(result)
        self.results_panel.display_result(result)

        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        label = (
            f"{stamp} | det={format_number(result.determinant, 2)} | "
            f"{result.stability.risk_level}"
        )
        self.input_panel.add_history_item(label)
        append_history(result)

    def export_report(self) -> None:
        """
        Calculate:
        Exportación del análisis actual como reporte PDF.

        Input:
            - No recibe parámetros. Usa self.current_result y las figuras actuales.

        Output:
            - No retorna valores. Genera un archivo en outputs/reports.

        Restrictions:
            Primero debe existir un análisis ejecutado; de lo contrario se
            muestra un mensaje informativo.
        """
        if self.current_result is None:
            QMessageBox.information(
                self,
                "Sin analisis",
                "Primero ejecuta un analisis para poder exportar el reporte.",
            )
            return

        try:
            path = export_analysis_report(self.current_result, self.graph_view.figures)
        except Exception as exc:
            QMessageBox.critical(self, "Error al exportar", str(exc))
            return

        QMessageBox.information(
            self,
            "Reporte exportado",
            f"Reporte guardado en:\n{path}",
        )
