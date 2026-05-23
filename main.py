"""
MODULO: main.py

DESCRIPCION:
Archivo principal del proyecto StructuraLab. Contiene la funcion que inicia la
aplicacion de escritorio y carga la ventana principal desarrollada con PyQt6.

PROPOSITO:
Servir como punto de entrada del taller. Desde este archivo se ejecuta el
programa completo sin mezclar la interfaz con los calculos matematicos.

ENTRADAS:
No recibe datos matematicos directos. Usa los argumentos del sistema operativo
para iniciar la aplicacion grafica.

SALIDAS:
Retorna un codigo entero de finalizacion. Si la aplicacion abre correctamente,
devuelve el codigo generado por PyQt6; si faltan dependencias, devuelve 1.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Creacion de modulo principal
- Importacion de modulos externos
- Inicializacion de interfaz grafica
- Manejo basico de errores

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

import sys


def main() -> int:
    """
    Calcula:
    inicio del ciclo grafico de la aplicacion.

    Formula usada:
    app = QApplication(sys.argv)
    ventana = MainWindow()
    salida = app.exec()

    Entradas:
        sys.argv -> argumentos del sistema usados por PyQt6.

    Salida:
        Codigo entero de finalizacion de la aplicacion.

    Restricciones:
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
