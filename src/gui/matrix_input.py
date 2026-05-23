"""
=========================================================
MODULE: matrix_input.py

DESCRIPTION:
    El módulo que contiene el panel de entrada de datos. Permite seleccionar el tamano
    de la matriz, escribir valores, cargar ejemplos, ejecutar análisis, exportar PDF
    y mostrar historial.

PURPOSE:
    Separar la captura de datos de la ventana principal y del motor matemático.

INPUT:
    - Valores escritos por el usuario en una tabla 2x2 o 3x3.
    - Ejemplos cargados desde data/matrix_examples.json.

OUTPUT:
    - Matriz de NumPy emitida hacia la ventana principal mediante una señal.

TOPICS RELATED TO THIS MODULE:
    - Entrada de datos
    - Validación previa
    - Señales de PyQt6
    - Matrices 2x2 y 3x3

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

import json
from pathlib import Path

import numpy as np
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.config.settings import DATA_DIR


class MatrixInputWidget(QFrame):
    """
    Represents:
    Panel izquierdo donde el usuario ingresa la matriz y controla acciones.

    Input:
        - parent -> Componente visual padre opcional.

    Output:
        - Componente visual que emite matrices y solicitudes de exportación.
    """

    analyze_requested = pyqtSignal(object)
    export_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Calculate:
        Inicialización del panel de entrada y carga de ejemplos.

        Input:
            - parent -> Componente visual padre opcional.

        Output:
            No retorna valores. Construye el panel y deja una matriz 2x2 lista.

        Restrictions:
            Debe ejecutarse dentro de una aplicación PyQt6.
        """
        super().__init__(parent)
        self.setObjectName("SidePanel")
        self.examples = self._load_examples()
        self._build_ui()
        self._connect_signals()
        self._populate_examples()
        self._resize_matrix(2)

    def _build_ui(self) -> None:
        """
        Calculate:
        Construcción visual de tabla, botones, selector de ejemplos e historial.

        Input:
            - No recibe parámetros.

        Output:
            - No retorna valores. Agrega widgets al panel.

        Restrictions:
            Solo crea interfaz; no analiza la matriz.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("Entrada de matriz")
        title.setStyleSheet("font-size: 14pt; font-weight: 700;")
        layout.addWidget(title)

        size_row = QHBoxLayout()
        size_row.addWidget(QLabel("Tamano"))
        self.size_combo = QComboBox()
        self.size_combo.addItems(["2 x 2", "3 x 3"])
        size_row.addWidget(self.size_combo)
        layout.addLayout(size_row)

        self.table = QTableWidget(3, 3)
        self.table.setFixedHeight(150)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        self.example_combo = QComboBox()
        layout.addWidget(QLabel("Ejemplos"))
        layout.addWidget(self.example_combo)

        button_grid = QGridLayout()
        self.analyze_button = QPushButton("Analizar")
        self.clear_button = QPushButton("Limpiar")
        self.clear_button.setObjectName("SecondaryButton")
        self.export_button = QPushButton("Exportar PDF")
        self.export_button.setObjectName("SecondaryButton")
        button_grid.addWidget(self.analyze_button, 0, 0, 1, 2)
        button_grid.addWidget(self.clear_button, 1, 0)
        button_grid.addWidget(self.export_button, 1, 1)
        layout.addLayout(button_grid)

        layout.addWidget(QLabel("Historial"))
        self.history_list = QListWidget()
        self.history_list.setMinimumHeight(140)
        layout.addWidget(self.history_list, stretch=1)

    def _connect_signals(self) -> None:
        """
        Calculate:
        Conexion entre botones, selectores y funciones internas.

        Input:
            - No recibe parametros.

        Output:
            - No retorna valores. Activa eventos de la interfaz.

        Restrictions:
            Las señales solo funcionan mientras la aplicacion PyQt6 este activa.
        """
        self.size_combo.currentIndexChanged.connect(self._on_size_changed)
        self.example_combo.currentIndexChanged.connect(self._on_example_changed)
        self.analyze_button.clicked.connect(self._emit_analysis)
        self.clear_button.clicked.connect(self.clear_matrix)
        self.export_button.clicked.connect(self.export_requested.emit)

    def _load_examples(self) -> list[dict]:
        """
        Calculate:
        Lectura de matrices de ejemplo desde un archivo JSON.

        Input:
            - No recibe parámetros. Usa data/matrix_examples.json.

        Output:
            - Lista de diccionarios con nombre, tamano y matriz.

        Restrictions:
            Si el archivo no existe, retorna una lista vacia.
        """
        path = Path(DATA_DIR) / "matrix_examples.json"
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _populate_examples(self) -> None:
        """
        Calculate:
        Llenado del selector de ejemplos.

        Input:
            - No recibe parámetros. Usa self.examples.

        Output:
            No retorna valores. Inserta opciones en el QComboBox.

        Restrictions:
            Debe llamarse después de cargar los ejemplos.
        """
        self.example_combo.blockSignals(True)
        self.example_combo.clear()
        self.example_combo.addItem("Seleccionar ejemplo", None)
        for example in self.examples:
            self.example_combo.addItem(example["name"], example)
        self.example_combo.blockSignals(False)

    def _on_size_changed(self) -> None:
        """
        Calculate:
        Cambio del tamaño de la tabla según selección del usuario.

        Input:
            - No recibe parámetros. Lee el índice del selector de tamaño.

        Output:
            - No retorna valores. Ajusta la tabla a 2x2 o 3x3.

        Restrictions:
            Solo permite los tamaños definidos en el combo: 2x2 y 3x3.
        """
        self._resize_matrix(2 if self.size_combo.currentIndex() == 0 else 3)

    def _resize_matrix(self, size: int) -> None:
        """
        Calculate:
        Redimensionamiento de la tabla de entrada.

        Input:
            - size -> Tamaño de la matriz, 2 o 3.

        Output:
            - No retorna valores. Ajusta filas, columnas y celdas.

        Restrictions:
            Esta función esta diseñada para size = 2 o size = 3.
        """
        self.table.setRowCount(size)
        self.table.setColumnCount(size)
        for row in range(size):
            self.table.setRowHeight(row, 42)
            for col in range(size):
                if self.table.item(row, col) is None:
                    self.table.setItem(row, col, QTableWidgetItem("0"))
                self.table.setColumnWidth(col, 70)

    def _on_example_changed(self) -> None:
        """
        Calculate:
        Carga de un ejemplo seleccionado en la tabla.

        Input:
            - No recibe parámetros. Lee el ejemplo actual del QComboBox.

        Output:
            - No retorna valores. Escribe los valores del ejemplo en la tabla.

        Restrictions:
            El ejemplo debe contener claves name, size y matrix.
        """
        example = self.example_combo.currentData()
        if not example:
            return
        size = int(example["size"])
        self.size_combo.setCurrentIndex(0 if size == 2 else 1)
        self._resize_matrix(size)
        matrix = example["matrix"]
        for row in range(size):
            for col in range(size):
                self.table.setItem(row, col, QTableWidgetItem(str(matrix[row][col])))

    def read_matrix(self) -> np.ndarray:
        """
        Calculate:
        Conversión de las celdas de la tabla en una matriz de NumPy.

        Fórmula usada:
        matrix[row][col] = float(texto_de_celda)

        Input:
            - No recibe parámetros. Lee los valores escritos en la tabla.

        Output:
            Matriz de NumPy con valores decimales.

        Restrictions:
            Cada celda debe contener un número válido. Se aceptan comas como
            separador decimal y se convierten a punto.
        """
        size = self.table.rowCount()
        values: list[list[float]] = []
        for row in range(size):
            current_row: list[float] = []
            for col in range(size):
                item = self.table.item(row, col)
                text = item.text().strip() if item else "0"
                current_row.append(float(text.replace(",", ".")))
            values.append(current_row)
        return np.array(values, dtype=float)

    def _emit_analysis(self) -> None:
        """
        Calculate:
        Emisión de la matriz capturada hacia la ventana principal.

        Input:
            - No recibe parámetros. Usa read_matrix().

        Output:
            - No retorna valores. Emite la señal analyze_requested.

        Restrictions:
            Si alguna celda no es numérica, Python genera error de conversión.
        """
        self.analyze_requested.emit(self.read_matrix())

    def clear_matrix(self) -> None:
        """
        Calculate:
        Limpieza de la tabla de entrada.

        Fórmula usada:
        cada celda visible = 0

        Input:
            - No recibe parámetros.

        Output:
            - No retorna valores. Escribe cero en todas las celdas visibles.

        Restrictions:
            Solo modifica las celdas visibles según el tamaño actual.
        """
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                self.table.setItem(row, col, QTableWidgetItem("0"))

    def add_history_item(self, label: str) -> None:
        """
        Calculate:
        Adición visual de un registro al historial.

        Input:
            - label -> Texto con fecha, determinante y riesgo.

        Output:
            - No retorna valores. Inserta el registro al inicio de la lista.

        Restrictions:
            El historial visual se reinicia al cerrar la aplicacion; el historial
            permanente se guarda en outputs/matrices/history.json.
        """
        self.history_list.insertItem(0, label)
