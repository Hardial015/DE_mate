"""
graph_view.py
-------------
Dibujo del grafo ponderado usando matplotlib, embebido dentro de una
ventana Tkinter mediante FigureCanvasTkAgg.

Se separa la lógica de dibujo pura (draw_graph_on_axes), que no depende
de Tkinter y puede probarse de forma aislada, de la clase GraphCanvas
que sí depende de Tkinter para insertarse en la interfaz.
"""

import math

import matplotlib
matplotlib.use("Agg")  # backend por defecto; GraphCanvas lo cambia a TkAgg
import matplotlib.pyplot as plt

from theme import COLORS


def circular_layout(n, radius=1.0):
    """Calcula posiciones (x, y) de n nodos distribuidos uniformemente
    en un círculo, empezando desde arriba (ángulo 90°) en sentido horario."""
    positions = []
    start_angle = math.pi / 2
    for i in range(n):
        angle = start_angle - (2 * math.pi * i / n)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        positions.append((x, y))
    return positions


def draw_graph_on_axes(ax, graph, highlight_cycle=None, highlight_missing=None):
    """
    Dibuja el grafo `graph` (instancia de graph_model.Graph) sobre los
    ejes de matplotlib `ax` ya existentes.

    highlight_cycle: lista opcional de índices de nodos (ej. [0,2,1,3,4])
        que representa un ciclo a resaltar en color de acento (grueso,
        por encima de las demás aristas). Se usará en la etapa final
        para marcar el ciclo óptimo.
    highlight_missing: lista opcional de tuplas (i, j) de aristas que
        aún NO existen mostradas como sugerencia punteada en rojo.
    """
    ax.clear()
    ax.set_facecolor(COLORS["bg_dark"])
    ax.set_aspect("equal")
    ax.axis("off")

    n = graph.n
    positions = circular_layout(n, radius=1.0)

    edge_list = graph.edge_list()

    # --- 1) Líneas de aristas existentes (por debajo de todo) ---
    for (i, j, w) in edge_list:
        x1, y1 = positions[i]
        x2, y2 = positions[j]
        ax.plot([x1, x2], [y1, y2], color=COLORS["edge_default"],
                linewidth=1.6, alpha=0.85, zorder=1)

    # --- 2) Aristas faltantes sugeridas (punteadas, rojas) ---
    if highlight_missing:
        for (i, j) in highlight_missing:
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            ax.plot([x1, x2], [y1, y2], color=COLORS["danger"],
                    linewidth=1.6, linestyle="--", alpha=0.9, zorder=2)

    # --- 3) Ciclo resaltado (grueso, color de acento) ---
    if highlight_cycle:
        m = len(highlight_cycle)
        for k in range(m):
            a = highlight_cycle[k]
            b = highlight_cycle[(k + 1) % m]
            x1, y1 = positions[a]
            x2, y2 = positions[b]
            ax.plot([x1, x2], [y1, y2], color=COLORS["edge_optimal"],
                    linewidth=3.6, alpha=0.95, zorder=3)

    # --- 4) Etiquetas de peso (siempre por encima de todas las líneas) ---
    for (i, j, w) in edge_list:
        x1, y1 = positions[i]
        x2, y2 = positions[j]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my, f"{w:g}", fontsize=9.5, color=COLORS["text_primary"],
                ha="center", va="center", zorder=4, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.22", facecolor=COLORS["bg_dark"],
                           edgecolor=COLORS["bg_light"], linewidth=0.8))

    # --- 5) Nodos (dibujados al final, por encima de todo) ---
    for i, (x, y) in enumerate(positions):
        circle = plt.Circle((x, y), 0.11, facecolor=COLORS["node_fill"],
                             edgecolor=COLORS["node_border"], linewidth=2.2,
                             zorder=5)
        ax.add_patch(circle)
        ax.text(x, y, graph.labels[i], fontsize=13, fontweight="bold",
                color=COLORS["node_text"], ha="center", va="center", zorder=6)

    margin = 0.35
    ax.set_xlim(-1 - margin, 1 + margin)
    ax.set_ylim(-1 - margin, 1 + margin)


# ---------------------------------------------------------------------
# Clase para embeber el dibujo en Tkinter (usada por screens.py)
# ---------------------------------------------------------------------
class GraphCanvas:
    """
    Envoltorio que crea una figura de matplotlib embebida en un widget
    Tkinter (usando FigureCanvasTkAgg) y expone un método `update()`
    para redibujar cuando el grafo o el ciclo resaltado cambian.

    Uso:
        canvas = GraphCanvas(parent_frame, graph)
        canvas.widget.pack(fill="both", expand=True)
        ...
        canvas.update(graph, highlight_cycle=[0, 2, 1, 3, 4])
    """

    def __init__(self, parent, graph, figsize=(5.6, 5.2)):
        # Import diferido de los módulos de Tkinter: así graph_view.py
        # puede importarse y probarse (draw_graph_on_axes) en entornos
        # sin Tkinter instalado.
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        self.figure = plt.Figure(figsize=figsize, dpi=100,
                                  facecolor=COLORS["bg_dark"])
        self.ax = self.figure.add_subplot(111)

        self.tk_canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.widget = self.tk_canvas.get_tk_widget()
        self.widget.configure(bg=COLORS["bg_dark"], highlightthickness=0)

        self.update(graph)

    def update(self, graph, highlight_cycle=None, highlight_missing=None):
        draw_graph_on_axes(self.ax, graph, highlight_cycle, highlight_missing)
        self.tk_canvas.draw()