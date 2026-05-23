"""
MODULO: graph_view.py

DESCRIPCION:
Modulo que crea el panel grafico de la interfaz. Muestra las graficas del
analisis en pestanas: estructura, mapa de calor, vectores y modos.

PROPOSITO:
Integrar las figuras de Matplotlib dentro de la ventana PyQt6 sin mezclar el
codigo visual con los calculos matematicos.

ENTRADAS:
result -> Objeto AnalysisResult generado por el analisis.
widget -> Elemento grafico que se desea ubicar dentro de una pestana.

SALIDAS:
Panel QTabWidget con graficas actualizadas.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Interfaz grafica
- Pestanas
- Integracion Matplotlib y PyQt6
- Visualizacion de resultados

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QLabel, QTabWidget, QVBoxLayout, QWidget

from src.analysis.structural_solver import AnalysisResult
from src.visualization.plot_builders import build_all_figures


class GraphView(QTabWidget):
    """
    Representa:
    area de graficas organizada en pestanas.

    Entradas:
        parent -> Componente visual padre opcional de PyQt6.

    Salida:
        Objeto visual que se inserta en la ventana principal.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Calcula:
        inicializacion del panel de graficas con una pestana de bienvenida.

        Entradas:
            parent -> Componente visual padre opcional.

        Salida:
            No retorna valores. Configura el estado inicial del panel.

        Restricciones:
            Debe ejecutarse dentro de una aplicacion PyQt6 activa.
        """
        super().__init__(parent)
        self.figures: dict[str, Figure] = {}
        self._placeholder = QLabel("Ingresa una matriz y presiona Analizar.")
        self._placeholder.setStyleSheet("font-size: 13pt; color: #cbd5e1; padding: 24px;")
        self.addTab(self._wrap_widget(self._placeholder), "Inicio")

    def _wrap_widget(self, widget: QWidget) -> QWidget:
        """
        Calcula:
        contenedor grafico para insertar un widget dentro de una pestana.

        Entradas:
            widget -> Elemento visual que se desea mostrar.

        Salida:
            Componente visual contenedor con margenes internos.

        Restricciones:
            El parametro debe ser un componente visual valido de PyQt6.
        """
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(widget)
        return container

    def display_result(self, result: AnalysisResult) -> None:
        """
        Calcula:
        actualizacion de todas las graficas a partir de un nuevo analisis.

        Entradas:
            result -> Resultado completo de analyze_matrix.

        Salida:
            No retorna valores. Reemplaza las pestanas por graficas nuevas.

        Restricciones:
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
