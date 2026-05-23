"""
MODULO: plot_builders.py

DESCRIPCION:
Modulo encargado de construir las graficas del proyecto usando Matplotlib:
mapa de calor, estructura deformada, vectores propios 2D/3D y participacion
modal.

PROPOSITO:
Separar la visualizacion grafica de los calculos matematicos y de la interfaz.
Esto permite que las mismas graficas se usen en pantalla y en reportes PDF.

ENTRADAS:
result -> Objeto AnalysisResult con matriz, valores propios, vectores propios e
intensidad nodal.

SALIDAS:
Figuras de Matplotlib listas para mostrarse o exportarse.

TEMAS RELACIONADOS CON ESTE EJEMPLO:
- Visualizacion de datos
- Matplotlib
- Vectores propios en 2D y 3D
- Mapas de calor

AUTORES:
Isabella Mejía Urueña
Laura Sofía Restrepo Ardila
"""

from __future__ import annotations

import numpy as np
from matplotlib.figure import Figure

from src.analysis.structural_solver import AnalysisResult


TEXT_COLOR = "#f8fafc"
MUTED_COLOR = "#94a3b8"
GRID_COLOR = "#334155"
FIGURE_COLOR = "#050505"
AXIS_COLOR = "#0f172a"


def _apply_dark_theme(figure: Figure) -> None:
    """
    Calcula:
    aplicacion de colores oscuros a una figura.

    Entradas:
        figure -> Figura de Matplotlib.

    Salida:
        No retorna valores. Modifica la apariencia visual de la figura.

    Restricciones:
        Solo cambia estilo; no altera datos ni resultados matematicos.
    """
    figure.patch.set_facecolor(FIGURE_COLOR)
    for axis in figure.axes:
        axis.set_facecolor(AXIS_COLOR)
        axis.title.set_color(TEXT_COLOR)
        axis.xaxis.label.set_color(TEXT_COLOR)
        axis.yaxis.label.set_color(TEXT_COLOR)
        axis.tick_params(colors=MUTED_COLOR)
        if hasattr(axis, "zaxis"):
            axis.zaxis.label.set_color(TEXT_COLOR)
            axis.tick_params(axis="z", colors=MUTED_COLOR)
        for spine in axis.spines.values():
            spine.set_color(GRID_COLOR)


def _style_3d_axis(axis) -> None:
    """
    Calcula:
    estilo visual para ejes tridimensionales.

    Entradas:
        axis -> Eje 3D de Matplotlib.

    Salida:
        No retorna valores. Ajusta paneles, grilla y angulo de vista.

    Restricciones:
        Se usa solo en graficas 3D de matrices 3x3.
    """
    axis.xaxis.pane.set_facecolor(AXIS_COLOR)
    axis.yaxis.pane.set_facecolor(AXIS_COLOR)
    axis.zaxis.pane.set_facecolor(AXIS_COLOR)
    axis.xaxis.pane.set_edgecolor(GRID_COLOR)
    axis.yaxis.pane.set_edgecolor(GRID_COLOR)
    axis.zaxis.pane.set_edgecolor(GRID_COLOR)
    axis.xaxis._axinfo["grid"]["color"] = GRID_COLOR
    axis.yaxis._axinfo["grid"]["color"] = GRID_COLOR
    axis.zaxis._axinfo["grid"]["color"] = GRID_COLOR
    axis.view_init(elev=24, azim=38)
    try:
        axis.set_box_aspect((1, 1, 1))
    except AttributeError:
        pass


def _node_coordinates(size: int) -> np.ndarray:
    """
    Calcula:
    coordenadas base de nodos para representar la estructura.

    Formula usada:
    - Para 2 nodos: linea horizontal.
    - Para 3 nodos: triangulo simplificado.

    Entradas:
        size -> Cantidad de nodos o dimension de la matriz.

    Salida:
        Arreglo de coordenadas (x, y).

    Restricciones:
        Esta funcion esta disenada para tamanos 2 y 3.
    """
    if size == 2:
        return np.array([[0.0, 0.0], [1.8, 0.0]])
    return np.array([[0.0, 0.0], [1.8, 0.0], [0.9, 1.35]])


def build_heatmap_figure(result: AnalysisResult) -> Figure:
    """
    Calcula:
    mapa de calor de la matriz A.

    Formula usada:
    color_ij = intensidad visual segun el valor de aij.

    Entradas:
        result -> Resultado del analisis que contiene result.matrix.

    Salida:
        Figura de Matplotlib con el mapa de calor.

    Restricciones:
        La matriz debe ser 2x2 o 3x3 para coincidir con el alcance del proyecto.
    """
    matrix = result.matrix
    figure = Figure(figsize=(5.2, 4.0), tight_layout=True)
    axis = figure.add_subplot(111)
    image = axis.imshow(matrix, cmap="coolwarm")
    axis.set_title("Mapa de intensidad matricial")
    axis.set_xlabel("Nodo / grado de libertad")
    axis.set_ylabel("Nodo / grado de libertad")
    axis.set_xticks(range(matrix.shape[1]))
    axis.set_yticks(range(matrix.shape[0]))
    axis.set_xticklabels([f"N{i + 1}" for i in range(matrix.shape[1])])
    axis.set_yticklabels([f"N{i + 1}" for i in range(matrix.shape[0])])

    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            axis.text(
                col,
                row,
                f"{matrix[row, col]:.2f}",
                ha="center",
                va="center",
                color="#ffffff" if abs(matrix[row, col]) > np.max(np.abs(matrix)) / 2 else "#0f172a",
                fontsize=9,
                weight="bold",
            )

    colorbar = figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
    colorbar.ax.yaxis.set_tick_params(color=MUTED_COLOR)
    colorbar.outline.set_edgecolor(GRID_COLOR)
    for label in colorbar.ax.get_yticklabels():
        label.set_color(MUTED_COLOR)
    _apply_dark_theme(figure)
    return figure


def build_structure_figure(result: AnalysisResult) -> Figure:
    """
    Calcula:
    comparacion entre estructura original y estructura deformada.

    Formula usada:
    coordenada_deformada = coordenada_original + vector_modo_1 * escala

    Entradas:
        result -> Resultado con matriz, vectores propios e intensidad nodal.

    Salida:
        Figura con barras, nodos, colores de intensidad y deformacion simulada.

    Restricciones:
        La deformacion es una simulacion academica basada en el primer modo
        propio, no un desplazamiento real de obra.
    """
    matrix = result.matrix
    size = matrix.shape[0]
    coords = _node_coordinates(size)
    deformation_vector = np.real_if_close(result.eigenvectors[:, 0], tol=1000).astype(float)
    deformation = np.zeros_like(coords)
    deformation[:, 0] = deformation_vector
    if size >= 2:
        deformation[:, 1] = np.roll(deformation_vector, -1)
    deformation_scale = 0.22
    deformed = coords + deformation * deformation_scale

    figure = Figure(figsize=(5.2, 4.0), tight_layout=True)
    axis = figure.add_subplot(111)
    axis.set_title("Estructura original vs deformada")

    max_weight = float(np.max(np.abs(matrix))) or 1.0
    for i in range(size):
        for j in range(i + 1, size):
            weight = abs(matrix[i, j])
            if weight > 1e-9:
                width = 1.0 + 4.0 * weight / max_weight
                axis.plot(
                    [coords[i, 0], coords[j, 0]],
                    [coords[i, 1], coords[j, 1]],
                    color="#64748b",
                    linewidth=width,
                    linestyle="--",
                    alpha=0.7,
                )
                axis.plot(
                    [deformed[i, 0], deformed[j, 0]],
                    [deformed[i, 1], deformed[j, 1]],
                    color="#2563eb",
                    linewidth=width,
                    alpha=0.95,
                )

    scatter = axis.scatter(
        deformed[:, 0],
        deformed[:, 1],
        c=result.nodal_intensity,
        cmap="RdYlGn_r",
        s=260,
        edgecolors="#f8fafc",
        linewidths=1.2,
        zorder=4,
    )
    axis.scatter(coords[:, 0], coords[:, 1], c="#475569", s=140, zorder=3)

    for index, (x_value, y_value) in enumerate(deformed, start=1):
        axis.text(
            x_value,
            y_value,
            f"N{index}",
            ha="center",
            va="center",
            fontsize=9,
            weight="bold",
            color="#020617",
            zorder=5,
        )

    axis.set_aspect("equal", adjustable="datalim")
    axis.grid(True, color=GRID_COLOR, linewidth=0.8)
    axis.set_xlabel("Eje X")
    axis.set_ylabel("Eje Y")
    colorbar = figure.colorbar(scatter, ax=axis, fraction=0.046, pad=0.04, label="Intensidad nodal")
    colorbar.ax.yaxis.label.set_color(TEXT_COLOR)
    colorbar.ax.yaxis.set_tick_params(color=MUTED_COLOR)
    colorbar.outline.set_edgecolor(GRID_COLOR)
    for label in colorbar.ax.get_yticklabels():
        label.set_color(MUTED_COLOR)
    _apply_dark_theme(figure)
    return figure


def build_vectors_figure(result: AnalysisResult) -> Figure:
    """
    Calcula:
    grafica de vectores propios.

    Formula usada:
    A * v = lambda * v

    Entradas:
        result -> Resultado con valores propios y vectores propios.

    Salida:
        Figura 2D si la matriz es 2x2.
        Figura 3D si la matriz es 3x3.

    Restricciones:
        Para matrices 3x3 se usan componentes X, Y y Z. Para matrices 2x2 se
        usan componentes X e Y.
    """
    eigenvectors = np.real_if_close(result.eigenvectors, tol=1000).astype(float)
    eigenvalues = np.real_if_close(result.eigenvalues, tol=1000).astype(float)
    size = eigenvectors.shape[0]
    colors = ["#2563eb", "#dc2626", "#16a34a"]

    figure = Figure(figsize=(5.2, 4.0), tight_layout=True)

    if size == 3:
        axis = figure.add_subplot(111, projection="3d")
        axis.set_title("Vectores propios en 3D")
        axis.set_xlabel("Componente X")
        axis.set_ylabel("Componente Y")
        axis.set_zlabel("Componente Z")

        for index in range(size):
            vector = eigenvectors[:, index]
            x_value = vector[0]
            y_value = vector[1]
            z_value = vector[2]
            color = colors[index % len(colors)]

            axis.quiver(
                0,
                0,
                0,
                x_value,
                y_value,
                z_value,
                color=color,
                linewidth=2.5,
                arrow_length_ratio=0.16,
            )
            axis.scatter(
                [x_value],
                [y_value],
                [z_value],
                color=color,
                s=38,
                depthshade=False,
            )
            axis.text(
                x_value * 1.12,
                y_value * 1.12,
                z_value * 1.12,
                f"Modo {index + 1}\nlambda={eigenvalues[index]:.2f}",
                fontsize=8,
                color=color,
                weight="bold",
            )

        axis.set_xlim(-1.15, 1.15)
        axis.set_ylim(-1.15, 1.15)
        axis.set_zlim(-1.15, 1.15)
        axis.scatter([0], [0], [0], color=TEXT_COLOR, s=18, depthshade=False)
        _style_3d_axis(axis)
        _apply_dark_theme(figure)
        return figure

    axis = figure.add_subplot(111)
    axis.set_title("Vectores propios y modos de deformacion")
    axis.axhline(0, color=MUTED_COLOR, linewidth=0.8)
    axis.axvline(0, color=MUTED_COLOR, linewidth=0.8)
    axis.grid(True, color=GRID_COLOR, linewidth=0.8)

    for index in range(size):
        vector = eigenvectors[:, index]
        x_value = vector[0]
        y_value = vector[1] if len(vector) > 1 else 0.0
        axis.quiver(
            0,
            0,
            x_value,
            y_value,
            angles="xy",
            scale_units="xy",
            scale=1,
            color=colors[index % len(colors)],
            width=0.012,
        )
        axis.text(
            x_value * 1.10,
            y_value * 1.10,
            f"Modo {index + 1}\nlambda={eigenvalues[index]:.2f}",
            fontsize=8,
            color=colors[index % len(colors)],
            weight="bold",
        )

    axis.set_xlim(-1.25, 1.25)
    axis.set_ylim(-1.25, 1.25)
    axis.set_xlabel("Componente X")
    axis.set_ylabel("Componente Y")
    _apply_dark_theme(figure)
    return figure


def build_modal_participation_figure(result: AnalysisResult) -> Figure:
    """
    Calcula:
    grafica de barras de participacion modal.

    Formula usada:
    porcentaje_i = participacion_i * 100

    Entradas:
        result -> Resultado con result.modal_participation.

    Salida:
        Figura con porcentaje estimado de participacion de cada modo.

    Restricciones:
        La participacion modal es una aproximacion educativa basada en magnitud
        de vectores propios.
    """
    participation = result.modal_participation
    figure = Figure(figsize=(5.2, 4.0), tight_layout=True)
    axis = figure.add_subplot(111)
    labels = [f"Modo {index + 1}" for index in range(len(participation))]
    axis.bar(labels, participation * 100, color=["#2563eb", "#dc2626", "#16a34a"][: len(labels)])
    axis.set_title("Participacion modal estimada")
    axis.set_ylabel("Participacion (%)")
    axis.set_ylim(0, max(100, float(np.max(participation * 100)) + 10))
    axis.grid(True, axis="y", color=GRID_COLOR)
    _apply_dark_theme(figure)
    return figure


def build_all_figures(result: AnalysisResult) -> dict[str, Figure]:
    """
    Calcula:
    conjunto completo de graficas del analisis.

    Entradas:
        result -> Resultado completo del motor de analisis.

    Salida:
        Diccionario con figuras: estructura, mapa de calor, vectores y modos.

    Restricciones:
        Se debe llamar despues de ejecutar analyze_matrix.
    """
    return {
        "estructura": build_structure_figure(result),
        "mapa_calor": build_heatmap_figure(result),
        "vectores": build_vectors_figure(result),
        "modos": build_modal_participation_figure(result),
    }
