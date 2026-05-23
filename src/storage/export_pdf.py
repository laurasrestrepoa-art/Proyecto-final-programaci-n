"""
MODULO: export_pdf.py

DESCRIPCION:
Modulo encargado de generar un reporte PDF con el resumen matematico, la matriz
analizada, los valores propios, la interpretacion estructural y las graficas.

PROPOSITO:
Crear una evidencia formal del analisis para entregar o presentar en clase.

ENTRADAS:
result -> Objeto AnalysisResult con los resultados del analisis.
figures -> Diccionario de graficas generadas por Matplotlib.

SALIDAS:
Ruta del archivo PDF generado en outputs/reports.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Generacion de reportes
- Exportacion PDF
- Tablas de resultados
- Integracion de graficas

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from matplotlib.figure import Figure

from src.analysis.structural_solver import AnalysisResult
from src.config.settings import REPORTS_DIR, ensure_output_dirs
from src.storage.export_images import save_figures
from src.utils.formatter import format_matrix, format_number


def export_analysis_report(result: AnalysisResult, figures: dict[str, Figure]) -> Path:
    """
    Calcula:
    construccion de un reporte PDF con datos numericos y graficos.

    Entradas:
        result -> Resultado completo del analisis.
        figures -> Graficas asociadas al resultado.

    Salida:
        Ruta del PDF generado.

    Restricciones:
        Requiere la libreria ReportLab. Si no esta instalada, se crea un
        reporte TXT de respaldo y se informa el error.
    """
    ensure_output_dirs()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"structural_analysis_{timestamp}.pdf"

    try:
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

    image_paths = save_figures(figures, prefix=f"analysis_{timestamp}")
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("StructuraLab - Reporte de analisis estructural", styles["Title"]))
    story.append(Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), styles["Normal"]))
    story.append(Spacer(1, 0.18 * inch))

    summary_data = [
        ["Indicador", "Valor"],
        ["Determinante", format_number(result.determinant)],
        ["Traza", format_number(result.trace)],
        ["Estado", result.stability.status],
        ["Riesgo", result.stability.risk_level],
        ["Condicion numerica", format_number(result.stability.condition_number)],
        ["Simetrica", "Si" if result.stability.is_symmetric else "No"],
        ["Dominancia diagonal", "Si" if result.stability.is_diagonally_dominant else "No"],
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

    story.append(Paragraph("Interpretacion estructural", styles["Heading2"]))
    for paragraph in result.interpretation.split("\n\n"):
        story.append(Paragraph(paragraph.replace("\n", "<br/>"), styles["Normal"]))
        story.append(Spacer(1, 0.08 * inch))

    story.append(Paragraph("Graficas", styles["Heading2"]))
    for name, image_path in image_paths.items():
        story.append(Paragraph(name.replace("_", " ").title(), styles["Heading3"]))
        story.append(Image(str(image_path), width=5.8 * inch, height=4.2 * inch))
        story.append(Spacer(1, 0.15 * inch))

    document = SimpleDocTemplate(str(report_path), pagesize=letter)
    document.build(story)
    return report_path


def _build_text_report(result: AnalysisResult) -> str:
    """
    Calcula:
    reporte de respaldo en texto plano cuando no se puede generar PDF.

    Entradas:
        result -> Resultado completo del analisis.

    Salida:
        Cadena de texto con resumen, matriz e interpretacion.

    Restricciones:
        Se usa solo como respaldo si ReportLab no esta disponible.
    """
    lines = [
        "StructuraLab - Reporte de analisis estructural",
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
