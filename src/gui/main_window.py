"""
MODULO: main_window.py

DESCRIPCION:
Modulo que contiene la ventana principal de StructuraLab. Conecta el panel de
entrada, el motor de analisis, las graficas, el panel de resultados y la
exportacion de reportes.

PROPOSITO:
Coordinar el flujo completo de la aplicacion sin realizar calculos matematicos
directamente dentro de la interfaz.

ENTRADAS:
matrix -> Matriz enviada desde MatrixInputWidget.

SALIDAS:
Actualizacion visual de resultados, graficas, historial y reportes PDF.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Interfaz grafica
- Programacion modular
- Senales y eventos
- Integracion de analisis y visualizacion

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
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
    Representa:
    ventana principal de la aplicacion.

    Entradas:
        No recibe parametros directos al crearse.

    Salida:
        Ventana grafica con panel de entrada, graficas y resultados.
    """

    def __init__(self) -> None:
        """
        Calcula:
        inicializacion completa de la ventana principal.

        Entradas:
            No recibe parametros.

        Salida:
            No retorna valores. Configura ventana, estilos y componentes.

        Restricciones:
            Debe ejecutarse despues de crear QApplication.
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
        Calcula:
        construccion de la interfaz principal.

        Entradas:
            No recibe parametros.

        Salida:
            No retorna valores. Organiza titulo, paneles y separadores.

        Restricciones:
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
        Calcula:
        conexion entre acciones del usuario y funciones de la ventana.

        Entradas:
            No recibe parametros.

        Salida:
            No retorna valores. Conecta analizar y exportar.

        Restricciones:
            Las senales requieren que los widgets ya hayan sido creados.
        """
        self.input_panel.analyze_requested.connect(self.run_analysis)
        self.input_panel.export_requested.connect(self.export_report)

    def run_analysis(self, matrix: np.ndarray) -> None:
        """
        Calcula:
        flujo completo de analisis de una matriz.

        Formula usada:
        matriz valida -> analyze_matrix(A) -> graficas + resultados + historial

        Entradas:
            matrix -> Matriz 2x2 o 3x3 ingresada por el usuario.

        Salida:
            No retorna valores. Actualiza interfaz, graficas e historial.

        Restricciones:
            Si la matriz no cumple las validaciones, se muestra una advertencia
            y no se ejecuta el analisis.
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
        Calcula:
        exportacion del analisis actual como reporte PDF.

        Entradas:
            No recibe parametros. Usa self.current_result y las figuras actuales.

        Salida:
            No retorna valores. Genera un archivo en outputs/reports.

        Restricciones:
            Primero debe existir un analisis ejecutado; de lo contrario se
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
