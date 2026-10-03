"""
main.py
-------
Punto de entrada de la aplicación. Contiene el motor de navegación
(App) que administra el cambio entre pantallas (frames) sin abrir
ventanas nuevas, manteniendo una sola ventana fluida.

La pantalla inicial es SetupScreen (screens.py), donde el usuario
define n y el modo de generación del grafo.
"""

import tkinter as tk
from theme import COLORS, WINDOW
from screens import SetupScreen


class App(tk.Tk):
    """Ventana principal y controlador de navegación entre pantallas."""

    def __init__(self):
        super().__init__()
        self.title(WINDOW["title"])
        self.geometry(f'{WINDOW["width"]}x{WINDOW["height"]}')
        self.minsize(WINDOW["min_width"], WINDOW["min_height"])
        self.configure(bg=COLORS["bg_darkest"])

        # Estado compartido de la aplicación (se irá llenando en las
        # siguientes etapas: número de nodos, modo de generación,
        # objeto Graph, etc.)
        self.state_data = {
            "n": None,
            "mode": None,   # "manual" | "aleatorio"
            "graph": None,
        }

        # Contenedor donde se apilan las pantallas
        container = tk.Frame(self, bg=COLORS["bg_darkest"])
        container.pack(fill="both", expand=True)
        self.container = container

        self.frames = {}
        self.show_frame(SetupScreen)

    def show_frame(self, screen_class):
        """Destruye la pantalla actual y monta una nueva. Navegación simple
        por reemplazo, adecuada para un flujo lineal paso a paso."""
        for widget in self.container.winfo_children():
            widget.destroy()

        frame = screen_class(self.container, self)
        frame.pack(fill="both", expand=True)
        self.frames[screen_class] = frame
        return frame


if __name__ == "__main__":
    app = App()
    app.mainloop()

    