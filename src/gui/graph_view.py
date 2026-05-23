"""
=========================================================
MODULO: graph_view.py

DESCRIPTION:
    Este módulo crea el panel gráfico de la interfaz. Muestra las gráficas del
    análisis en pestañas: estructura, mapa de calor, vectores y modos.

PURPOSE:
    Integrar las figuras de Matplotlib dentro de la ventana PyQt6 sin mezclar el
    codigo visual con los calculos matematicos.

INPUT:
    - result -> Objeto AnalysisResult generado por el análisis.
    - widget -> Elemento gráfico que se desea ubicar dentro de una pestaña.

OUTPUT:
    - Panel QTabWidget con gráficas actualizadas.

TOPICS RELATED TO THIS MODULE:
    - Interfaz gráfica
    - Pestañas
    - Integración Matplotlib y PyQt6
    - Visualización de resultados

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

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QLabel, QTabWidget, QVBoxLayout, QWidget

from src.analysis.structural_solver import AnalysisResult
from src.visualization.plot_builders import build_all_figures


class GraphView(QTabWidget):
    """
    Represents:
    área de gráficas organizada en pestañas.

    Input:
        - parent -> Componente visual padre opcional de PyQt6.

    Output:
        - Objeto visual que se inserta en la ventana principal.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Calculate:
        inicialización del panel de gráficas con una pestaña de bienvenida.

        Input:
            - parent -> Componente visual padre opcional.

        Output:
            - No retorna valores. Configura el estado inicial del panel.

        Restrictions:
            Debe ejecutarse dentro de una aplicación PyQt6 activa.
        """
        super().__init__(parent)
        self.figures: dict[str, Figure] = {}
        self._placeholder = QLabel("Ingresa una matriz y presiona Analizar.")
        self._placeholder.setStyleSheet("font-size: 13pt; color: #cbd5e1; padding: 24px;")
        self.addTab(self._wrap_widget(self._placeholder), "Inicio")

    def _wrap_widget(self, widget: QWidget) -> QWidget:
        """
        Calculate:
        contenedor gráfico para insertar un widget dentro de una pestaña.

        Input:
            widget -> Elemento visual que se desea mostrar.

        Output:
            Componente visual contenedor con margenes internos.

        Restrictions:
            El parámetro debe ser un componente visual válido de PyQt6.
        """
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(widget)
        return container

    def display_result(self, result: AnalysisResult) -> None:
        """
        Calculate:
        actualización de todas las gráficas a partir de un nuevo análisis.

        Input:
            - result -> Resultado completo de analyze_matrix.

        Output:
            - No retorna valores. Reemplaza las pestañas por gráficas nuevas.

        Restrictions:
            El resultado debe contener matriz, valores propios e intensidad
            nodal calculados correctamente.
        """
        self.clear()
        self.figures = build_all_figures(result)
        labels = {
            "estructura": "Estructura",
            "mapa_calor": "Mapa de calor",
            "vectores": "Vectores",
            "modos": "Modos",
        }

        for key, figure in self.figures.items():
            canvas = FigureCanvas(figure)
            canvas.draw()
            self.addTab(self._wrap_widget(canvas), labels[key])
