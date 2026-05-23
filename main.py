"""
========================================
MODULO: main.py

DESCRIPTION:
    Archivo principal del proyecto StructuraLab. Contiene la función que inicia la
    aplicación de escritorio y carga la ventana principal desarrollada con PyQt6.

PURPOSE:
    Servir como punto de entrada del taller. Desde este archivo se ejecuta el
    programa completo sin mezclar la interfaz con los cálculos matemáticos.

INPUT:
    - No recibe datos matematicos directos. Usa los argumentos del sistema operativo
    para iniciar la aplicación gráfica.

OUTPUT:
    - Retorna un codigo entero de finalizacion. Si la aplicación abre correctamente,
    devuelve el codigo generado por PyQt6; si faltan dependencias, devuelve 1.

TOPICS RELATED TO THIS MODULO
    - Creación de módulo principal
    - Importación de módulos externos
    - Inicialización de interfaz gráfica
    - Manejo básico de errores

AUTHORS:
    Isabella Mejía Urueña
    Laura Sofía Restrepo Ardila

VERSION:
    3.O

CREATION DATE:
    2026-05-15

LAST UPDATE:
    2026-05-23
========================================
"""

from __future__ import annotations

import sys


def main() -> int:
    """
    Calculate:
    inicio del ciclo gráfico de la aplicación.

    Fórmula usada:
    app = QApplication(sys.argv)
    ventana = MainWindow()
    salida = app.exec()

    Input:
        sys.argv -> argumentos del sistema usados por PyQt6.

    Output:
        Codigo entero de finalización de la aplicación.

    Restrictions:
        Requiere tener instaladas las librerias indicadas en requirements.txt.
    """
    try:
        from PyQt6.QtWidgets import QApplication

        from src.gui.main_window import MainWindow
    except ImportError as exc:
        print("No se pudo iniciar StructuraLab.")
        print("Instala las dependencias con: pip install -r requirements.txt")
        print(f"Detalle tecnico: {exc}")
        return 1

    app = QApplication(sys.argv)
    app.setApplicationName("StructuraLab")
    app.setOrganizationName("Proyecto Final Programacion")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
