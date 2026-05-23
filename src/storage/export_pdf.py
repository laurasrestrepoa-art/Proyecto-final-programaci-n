"""
MODULE: export_pdf.py

DESCRIPTION:
    Este módulo contiene funciones encargadas de generar un reporte PDF 
    con el resumen matemático, la matriz analizada, los valores propios, 
    la interpretación estructural y las graficas correspondientes.

PURPOSE:
    Crear una evidencia formal del análisis para que el usario pueda 
    entregar o presentar.

INPUT:
    - Resultado del análisis denominado result.
    - Diccionario de gráficas denominado figures.

OUTPUT:
    - Archivo PDF generado dentro de la carpeta
      outputs/reports.

TOPICS RELATED TO THIS MODULE:
    - Generación de reportes
    - Exportación PDF
    - Tablas de resultados
    - Integración de gráficas

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


# Se importa importan datetime para generar nombres (según hora y fecha),
# Path para el manejo de rutas y carpetas, y también Figure para trabajar
# con las gráficas de Matplotlib.
from datetime import datetime
from pathlib import Path
from matplotlib.figure import Figure


# Resultado principal del análisis estructural.
from src.analysis.structural_solver import AnalysisResult


# Carpetas y funciones de configuración, para guardar imágenes
# y también, para formatear números y matrices.
from src.config.settings import REPORTS_DIR, ensure_output_dirs
from src.storage.export_images import save_figures
from src.utils.formatter import format_matrix, format_number


def export_analysis_report(result: AnalysisResult, figures: dict[str, Figure]) -> Path:
    """
    Esta función genera un reporte PDF
    con los resultados del análisis
    estructural.

    En el reporte se incluye:
        - Resumen matemático
        - Matriz analizada
        - Valores propios
        - Interpretación estructural
        - Gráficas generadas

    Input:
        result -> Resultado completo del analisis.
        figures -> Graficas asociadas al resultado.

     Output:
        - Ruta del PDF generado.

    Restrictions:
        - Requiere la librería ReportLab. Si no esta instalada, se crea un
          reporte TXT de respaldo y se informa el error.
    """
    
    # Creación de carpetas.
    ensure_output_dirs()
    
    # Generación de fecha y hora para el nombre automático del reporte.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"structural_analysis_{timestamp}.pdf"

    try:
        # Librerías usadas para el reporte PDF:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    except ImportError as exc:
        fallback_path = report_path.with_suffix(".txt")
        fallback_path.write_text(_build_text_report(result), encoding="utf-8")
        raise RuntimeError(
            "ReportLab no esta instalado. Se guardo un reporte TXT en "
            f"{fallback_path}. Instala dependencias con: pip install -r requirements.txt"
        ) from exc
    # Para guaradar las gráficas como imágenes:
    image_paths = save_figures(figures, prefix=f"analysis_{timestamp}")
    styles = getSampleStyleSheet()

    # Lista donde se agregarán los elementos del PDF:
    story = []

    story.append(Paragraph("StructuraLab - Reporte de analisis estructural", styles["Title"]))
    story.append(Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), styles["Normal"]))
    story.append(Spacer(1, 0.18 * inch))

    # Para crear la tabla de resumen:
    summary_data = [
        ["Indicador", "Valor"],
        ["Determinante", format_number(result.determinant)],
        ["Traza", format_number(result.trace)],
        ["Estado", result.stability.status],
        ["Riesgo", result.stability.risk_level],
        ["Condición numérica", format_number(result.stability.condition_number)],
        ["Simétrica", "Sí" if result.stability.is_symmetric else "No"],
        ["Dominancia diagonal", "Sí" if result.stability.is_diagonally_dominant else "No"],
    ]
    table = Table(summary_data, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.22 * inch))

    story.append(Paragraph("Matriz analizada", styles["Heading2"]))
    story.append(Paragraph(f"<pre>{format_matrix(result.matrix)}</pre>", styles["Code"]))

    story.append(Paragraph("Valores propios", styles["Heading2"]))
    eigen_text = "<br/>".join(
        f"lambda {index}: {format_number(value)}"
        for index, value in enumerate(result.eigenvalues, start=1)
    )
    story.append(Paragraph(eigen_text, styles["Normal"]))

    story.append(Paragraph("Interpretación estructural", styles["Heading2"]))
    for paragraph in result.interpretation.split("\n\n"):
        story.append(Paragraph(paragraph.replace("\n", "<br/>"), styles["Normal"]))
        story.append(Spacer(1, 0.08 * inch))

    story.append(Paragraph("Gráficas", styles["Heading2"]))
    for name, image_path in image_paths.items():
        story.append(Paragraph(name.replace("_", " ").title(), styles["Heading3"]))
        story.append(Image(str(image_path), width=5.8 * inch, height=4.2 * inch))
        story.append(Spacer(1, 0.15 * inch))

    document = SimpleDocTemplate(str(report_path), pagesize=letter)
    document.build(story)
    return report_path


def _build_text_report(result: AnalysisResult) -> str:
    """
    Esta función genera un reporte de respaldo 
    en formato TXT.

    Se utiliza cuando no es posible generar el
    archivo PDF.
    
    Input:
        result -> Resultado completo del análisis.

    Output:
        - Cadena de texto con resumen, matriz e interpretación.

    Restrictions:
        - Se usa solo como respaldo si ReportLab no esta disponible.
    """
    
    lines = [
        "StructuraLab - Reporte de análisis estructural",
        "",
        f"Determinante: {format_number(result.determinant)}",
        f"Traza: {format_number(result.trace)}",
        f"Estado: {result.stability.status}",
        f"Riesgo: {result.stability.risk_level}",
        "",
        "Matriz:",
        format_matrix(result.matrix),
        "",
        result.interpretation,
    ]
    return "\n".join(lines)
