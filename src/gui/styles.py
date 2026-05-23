"""
=========================================================
SCRIPT: styles.py

DESCRIPTION:
    Este Script contiene la hoja de estilos visuales de la interfaz gráfica en PyQt6.
    Define colores, bordes, botones, tablas, pestañas y cuadros de texto.

PURPOSE:
    Mantener el diseno visual separado de la lógica del programa. Esto permite
    cambiar la apariencia sin modificar cálculos ni funciones principales.

INPUT:
    - No recibe parámetros. Contiene una cadena de texto con reglas QSS.

OUTPUT:
    - APP_STYLESHEET -> Estilos aplicados a la ventaña principal.

TOPICS RELATED TO THIS SCRIPT:
    - Interfaz gráfica
    - Estilos QSS
    - Modo oscuro
    - Separación de responsabilidades

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

APP_STYLESHEET = """
QMainWindow {
    background: #050505;
}
QWidget {
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 10pt;
    color: #f8fafc;
}
QFrame#SidePanel, QFrame#ResultsPanel {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 8px;
}
QLabel#TitleLabel {
    font-size: 20pt;
    font-weight: 700;
    color: #f8fafc;
}
QLabel#SubtitleLabel {
    color: #cbd5e1;
}
QPushButton {
    background: #2563eb;
    color: white;
    border: 0;
    border-radius: 6px;
    padding: 8px 12px;
    font-weight: 600;
}
QPushButton:hover {
    background: #1d4ed8;
}
QPushButton:disabled {
    background: #475569;
}
QPushButton#SecondaryButton {
    background: #1f2937;
    color: #e5e7eb;
    border: 1px solid #334155;
}
QPushButton#SecondaryButton:hover {
    background: #374151;
}
QComboBox, QTableWidget, QListWidget, QTextEdit {
    background: #020617;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #f8fafc;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
}
QComboBox QAbstractItemView {
    background: #020617;
    color: #f8fafc;
    selection-background-color: #2563eb;
}
QHeaderView::section {
    background: #111827;
    color: #f8fafc;
    border: 1px solid #334155;
}
QTableCornerButton::section {
    background: #111827;
    border: 1px solid #334155;
}
QTabWidget::pane {
    border: 1px solid #334155;
    background: #050505;
    border-radius: 8px;
}
QTabBar::tab {
    background: #111827;
    color: #cbd5e1;
    padding: 8px 14px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background: #020617;
    color: #60a5fa;
    font-weight: 700;
}
QMessageBox {
    background: #111827;
}
"""
