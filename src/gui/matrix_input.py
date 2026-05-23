"""
MODULO: matrix_input.py

DESCRIPCION:
Modulo que contiene el panel de entrada de datos. Permite seleccionar el tamano
de la matriz, escribir valores, cargar ejemplos, ejecutar analisis, exportar PDF
y mostrar historial.

PROPOSITO:
Separar la captura de datos de la ventana principal y del motor matematico.

ENTRADAS:
Valores escritos por el usuario en una tabla 2x2 o 3x3.
Ejemplos cargados desde data/matrix_examples.json.

SALIDAS:
Matriz de NumPy emitida hacia la ventana principal mediante una senal.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Entrada de datos
- Validacion previa
- Senales de PyQt6
- Matrices 2x2 y 3x3

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
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
    Representa:
    panel izquierdo donde el usuario ingresa la matriz y controla acciones.

    Entradas:
        parent -> Componente visual padre opcional.

    Salida:
        Componente visual que emite matrices y solicitudes de exportacion.
    """

    analyze_requested = pyqtSignal(object)
    export_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Calcula:
        inicializacion del panel de entrada y carga de ejemplos.

        Entradas:
            parent -> Componente visual padre opcional.

        Salida:
            No retorna valores. Construye el panel y deja una matriz 2x2 lista.

        Restricciones:
            Debe ejecutarse dentro de una aplicacion PyQt6.
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
        Calcula:
        construccion visual de tabla, botones, selector de ejemplos e historial.

        Entradas:
            No recibe parametros.

        Salida:
            No retorna valores. Agrega widgets al panel.

        Restricciones:
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
        Calcula:
        conexion entre botones, selectores y funciones internas.

        Entradas:
            No recibe parametros.

        Salida:
            No retorna valores. Activa eventos de la interfaz.

        Restricciones:
            Las senales solo funcionan mientras la aplicacion PyQt6 este activa.
        """
        self.size_combo.currentIndexChanged.connect(self._on_size_changed)
        self.example_combo.currentIndexChanged.connect(self._on_example_changed)
        self.analyze_button.clicked.connect(self._emit_analysis)
        self.clear_button.clicked.connect(self.clear_matrix)
        self.export_button.clicked.connect(self.export_requested.emit)

    def _load_examples(self) -> list[dict]:
        """
        Calcula:
        lectura de matrices de ejemplo desde un archivo JSON.

        Entradas:
            No recibe parametros. Usa data/matrix_examples.json.

        Salida:
            Lista de diccionarios con nombre, tamano y matriz.

        Restricciones:
            Si el archivo no existe, retorna una lista vacia.
        """
        path = Path(DATA_DIR) / "matrix_examples.json"
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _populate_examples(self) -> None:
        """
        Calcula:
        llenado del selector de ejemplos.

        Entradas:
            No recibe parametros. Usa self.examples.

        Salida:
            No retorna valores. Inserta opciones en el QComboBox.

        Restricciones:
            Debe llamarse despues de cargar los ejemplos.
        """
        self.example_combo.blockSignals(True)
        self.example_combo.clear()
        self.example_combo.addItem("Seleccionar ejemplo", None)
        for example in self.examples:
            self.example_combo.addItem(example["name"], example)
        self.example_combo.blockSignals(False)

    def _on_size_changed(self) -> None:
        """
        Calcula:
        cambio del tamano de la tabla segun seleccion del usuario.

        Entradas:
            No recibe parametros. Lee el indice del selector de tamano.

        Salida:
            No retorna valores. Ajusta la tabla a 2x2 o 3x3.

        Restricciones:
            Solo permite los tamanos definidos en el combo: 2x2 y 3x3.
        """
        self._resize_matrix(2 if self.size_combo.currentIndex() == 0 else 3)

    def _resize_matrix(self, size: int) -> None:
        """
        Calcula:
        redimensionamiento de la tabla de entrada.

        Entradas:
            size -> Tamano de la matriz, 2 o 3.

        Salida:
            No retorna valores. Ajusta filas, columnas y celdas.

        Restricciones:
            Esta funcion esta disenada para size = 2 o size = 3.
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
        Calcula:
        carga de un ejemplo seleccionado en la tabla.

        Entradas:
            No recibe parametros. Lee el ejemplo actual del QComboBox.

        Salida:
            No retorna valores. Escribe los valores del ejemplo en la tabla.

        Restricciones:
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
        Calcula:
        conversion de las celdas de la tabla en una matriz de NumPy.

        Formula usada:
        matrix[row][col] = float(texto_de_celda)

        Entradas:
            No recibe parametros. Lee los valores escritos en la tabla.

        Salida:
            Matriz de NumPy con valores decimales.

        Restricciones:
            Cada celda debe contener un numero valido. Se aceptan comas como
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
        Calcula:
        emision de la matriz capturada hacia la ventana principal.

        Entradas:
            No recibe parametros. Usa read_matrix().

        Salida:
            No retorna valores. Emite la senal analyze_requested.

        Restricciones:
            Si alguna celda no es numerica, Python genera error de conversion.
        """
        self.analyze_requested.emit(self.read_matrix())

    def clear_matrix(self) -> None:
        """
        Calcula:
        limpieza de la tabla de entrada.

        Formula usada:
        cada celda visible = 0

        Entradas:
            No recibe parametros.

        Salida:
            No retorna valores. Escribe cero en todas las celdas visibles.

        Restricciones:
            Solo modifica las celdas visibles segun el tamano actual.
        """
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                self.table.setItem(row, col, QTableWidgetItem("0"))

    def add_history_item(self, label: str) -> None:
        """
        Calcula:
        adicion visual de un registro al historial.

        Entradas:
            label -> Texto con fecha, determinante y riesgo.

        Salida:
            No retorna valores. Inserta el registro al inicio de la lista.

        Restricciones:
            El historial visual se reinicia al cerrar la aplicacion; el historial
            permanente se guarda en outputs/matrices/history.json.
        """
        self.history_list.insertItem(0, label)
