"""
screens.py
----------
Pantallas (frames) de la aplicación. Cada clase representa una pantalla
completa que se monta dentro del contenedor de main.py.

Etapa 3 (este archivo, por ahora):
    - SetupScreen: pantalla inicial donde el usuario define n (5-10)
      y elige el modo de generación del grafo (manual o aleatorio).
    - ResumenTemporalScreen: pantalla puente temporal que solo confirma
      la configuración elegida. Se reemplazará en las Etapas 4 y 5 por
      las pantallas reales de construcción manual / generación aleatoria.
"""

import random
import tkinter as tk
from theme import COLORS, FONTS, SPACING, style_button
from graph_model import Graph, node_label
from graph_view import GraphCanvas


class Header(tk.Frame):
    """Encabezado reutilizable: título + subtítulo + indicador de paso."""

    def __init__(self, parent, step_text, title_text, subtitle_text):
        super().__init__(parent, bg=COLORS["bg_darkest"])

        tk.Label(
            self, text=step_text, font=FONTS["small"],
            bg=COLORS["bg_darkest"], fg=COLORS["accent"],
        ).pack(anchor="w")

        tk.Label(
            self, text=title_text, font=FONTS["title"],
            bg=COLORS["bg_darkest"], fg=COLORS["text_primary"],
        ).pack(anchor="w", pady=(2, 4))

        tk.Label(
            self, text=subtitle_text, font=FONTS["subtitle"],
            bg=COLORS["bg_darkest"], fg=COLORS["text_secondary"],
        ).pack(anchor="w")


class SetupScreen(tk.Frame):
    """Etapa 3: configuración inicial del problema (n y modo de generación)."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_darkest"])
        self.controller = controller
        self.selected_mode = tk.StringVar(value="")  # "manual" | "aleatorio"
        self.error_var = tk.StringVar(value="")

        outer = tk.Frame(self, bg=COLORS["bg_darkest"], padx=48, pady=36)
        outer.pack(fill="both", expand=True)

        Header(
            outer,
            step_text="PASO 1 DE 4",
            title_text="Configuración del grafo",
            subtitle_text=("Define cuántos nodos tendrá el grafo y cómo "
                            "quieres construirlo."),
        ).pack(anchor="w", fill="x")

        # ------------------------------------------------------------
        # Tarjeta: cantidad de nodos
        # ------------------------------------------------------------
        card_n = tk.Frame(outer, bg=COLORS["bg_dark"], padx=28, pady=22)
        card_n.pack(fill="x", pady=(28, 18))

        tk.Label(
            card_n, text="Cantidad de nodos (n)", font=FONTS["heading"],
            bg=COLORS["bg_dark"], fg=COLORS["text_primary"],
        ).pack(anchor="w")

        tk.Label(
            card_n, text="Debe estar entre 5 y 10.", font=FONTS["small"],
            bg=COLORS["bg_dark"], fg=COLORS["text_muted"],
        ).pack(anchor="w", pady=(0, 12))

        spin_row = tk.Frame(card_n, bg=COLORS["bg_dark"])
        spin_row.pack(anchor="w")

        self.n_var = tk.IntVar(value=5)
        self.spin_n = tk.Spinbox(
            spin_row, from_=5, to=10, textvariable=self.n_var,
            font=FONTS["heading"], width=4, justify="center",
            bg=COLORS["bg_medium"], fg=COLORS["text_primary"],
            buttonbackground=COLORS["bg_light"], relief="flat",
            insertbackground=COLORS["text_primary"],
        )
        self.spin_n.pack(side="left", ipady=6)

        # ------------------------------------------------------------
        # Tarjeta: modo de generación
        # ------------------------------------------------------------
        card_mode = tk.Frame(outer, bg=COLORS["bg_dark"], padx=28, pady=22)
        card_mode.pack(fill="x", pady=(0, 18))

        tk.Label(
            card_mode, text="Modo de generación del grafo",
            font=FONTS["heading"], bg=COLORS["bg_dark"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 14))

        options_row = tk.Frame(card_mode, bg=COLORS["bg_dark"])
        options_row.pack(fill="x")
        options_row.columnconfigure(0, weight=1)
        options_row.columnconfigure(1, weight=1)

        self.btn_manual = self._build_mode_option(
            options_row, "manual", "🖉  Manual",
            "Tú defines cada arista y su peso.", col=0,
        )
        self.btn_random = self._build_mode_option(
            options_row, "aleatorio", "🎲  Aleatorio",
            "El sistema genera el grafo por ti.", col=1,
        )

        # ------------------------------------------------------------
        # Error / validación
        # ------------------------------------------------------------
        tk.Label(
            outer, textvariable=self.error_var, font=FONTS["body"],
            bg=COLORS["bg_darkest"], fg=COLORS["danger"],
        ).pack(anchor="w", pady=(4, 8))

        # ------------------------------------------------------------
        # Botón continuar
        # ------------------------------------------------------------
        footer = tk.Frame(outer, bg=COLORS["bg_darkest"])
        footer.pack(fill="x", pady=(10, 0))

        btn_continue = tk.Button(footer, text="Continuar  →",
                                  command=self._on_continue)
        style_button(btn_continue, kind="primary")
        btn_continue.pack(side="right")

    # ---------------------------------------------------------------
    def _build_mode_option(self, parent, mode_key, title, description, col):
        """Crea una 'tarjeta' seleccionable para elegir el modo. Al hacer
        clic, se resalta visualmente y guarda la elección."""
        card = tk.Frame(parent, bg=COLORS["bg_medium"], padx=18, pady=16,
                         highlightthickness=2,
                         highlightbackground=COLORS["bg_light"],
                         highlightcolor=COLORS["bg_light"])
        card.grid(row=0, column=col, sticky="nsew",
                   padx=(0, 10) if col == 0 else (10, 0))

        title_lbl = tk.Label(card, text=title, font=FONTS["body_bold"],
                              bg=COLORS["bg_medium"], fg=COLORS["text_primary"])
        title_lbl.pack(anchor="w")

        desc_lbl = tk.Label(card, text=description, font=FONTS["small"],
                             bg=COLORS["bg_medium"], fg=COLORS["text_secondary"],
                             wraplength=220, justify="left")
        desc_lbl.pack(anchor="w", pady=(4, 0))

        widgets = [card, title_lbl, desc_lbl]

        def select(_event=None):
            self.selected_mode.set(mode_key)
            self._refresh_mode_cards()

        for w in widgets:
            w.bind("<Button-1>", select)
            w.configure(cursor="hand2")

        card.mode_key = mode_key
        return card

    def _refresh_mode_cards(self):
        """Actualiza el resaltado visual de las tarjetas manual/aleatorio
        según cuál esté seleccionada."""
        for card in (self.btn_manual, self.btn_random):
            is_selected = card.mode_key == self.selected_mode.get()
            border = COLORS["accent"] if is_selected else COLORS["bg_light"]
            bg = COLORS["bg_light"] if is_selected else COLORS["bg_medium"]
            card.configure(highlightbackground=border, highlightcolor=border,
                            bg=bg)
            for child in card.winfo_children():
                child.configure(bg=bg)

    # ---------------------------------------------------------------
    def _on_continue(self):
        self.error_var.set("")

        # Validar n
        try:
            n = int(self.n_var.get())
        except (tk.TclError, ValueError):
            self.error_var.set("Ingresa un número entero válido para n.")
            return

        if not (5 <= n <= 10):
            self.error_var.set("El número de nodos debe estar entre 5 y 10.")
            return

        # Validar modo
        mode = self.selected_mode.get()
        if mode == "":
            self.error_var.set("Selecciona un modo de generación (manual o aleatorio).")
            return

        # Guardar en el estado global y avanzar según el modo elegido
        self.controller.state_data["n"] = n
        self.controller.state_data["mode"] = mode

        if mode == "manual":
            self.controller.show_frame(ManualEdgesScreen)
        else:
            self.controller.show_frame(RandomGraphScreen)


class ResumenTemporalScreen(tk.Frame):
    """
    (En desuso) Se mantiene solo por si se necesita una pantalla puente
    genérica en el futuro. Tanto el modo manual como el aleatorio ya
    tienen sus propias pantallas dedicadas.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_darkest"])
        self.controller = controller
        data = controller.state_data

        outer = tk.Frame(self, bg=COLORS["bg_darkest"], padx=48, pady=36)
        outer.pack(fill="both", expand=True)

        Header(
            outer, step_text="CONFIGURACIÓN GUARDADA ✔",
            title_text="Resumen de configuración",
            subtitle_text="Esta pantalla es temporal (se reemplaza en las próximas etapas).",
        ).pack(anchor="w", fill="x")

        card = tk.Frame(outer, bg=COLORS["bg_dark"], padx=28, pady=22)
        card.pack(fill="x", pady=28)

        tk.Label(card, text=f"Número de nodos (n): {data['n']}",
                 font=FONTS["body_bold"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"]).pack(anchor="w", pady=4)

        modo_legible = "Manual" if data["mode"] == "manual" else "Aleatorio"
        tk.Label(card, text=f"Modo de generación: {modo_legible}",
                 font=FONTS["body_bold"], bg=COLORS["bg_dark"],
                 fg=COLORS["accent2"]).pack(anchor="w", pady=4)

        btn_back = tk.Button(outer, text="←  Volver",
                              command=lambda: controller.show_frame(SetupScreen))
        style_button(btn_back, kind="secondary")
        btn_back.pack(side="left")


class ManualEdgesScreen(tk.Frame):
    """
    Etapa 4: construcción manual del grafo mediante una matriz interactiva.

    Se muestra una cuadrícula (solo triángulo superior, ya que el grafo
    es no dirigido) con un campo de texto por cada posible arista. El
    usuario escribe el peso en las casillas de las aristas que quiere
    crear y deja vacías las que no existen.

    Al presionar "Verificar y continuar":
        - Si el grafo resultante permite un ciclo hamiltoniano, se guarda
          y se avanza a la siguiente pantalla.
        - Si no, se resaltan en rojo las casillas de las aristas mínimas
          que faltarían para completar al menos un ciclo válido, y se
          explica la sugerencia en texto.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_darkest"])
        self.controller = controller
        self.n = controller.state_data["n"]
        self.labels = [node_label(i) for i in range(self.n)]
        self.entries = {}       # (i, j) con i<j -> tk.Entry
        self.error_var = tk.StringVar(value="")
        self.suggestion_var = tk.StringVar(value="")

        outer = tk.Frame(self, bg=COLORS["bg_darkest"], padx=48, pady=30)
        outer.pack(fill="both", expand=True)

        Header(
            outer, step_text="PASO 2 DE 4",
            title_text="Construcción manual del grafo",
            subtitle_text=("Escribe el peso solo en las casillas de las aristas "
                            "que quieras crear. Deja vacío si no hay conexión."),
        ).pack(anchor="w", fill="x")

        # ------------------------------------------------------------
        # Cuadrícula de pesos
        # ------------------------------------------------------------
        grid_card = tk.Frame(outer, bg=COLORS["bg_dark"], padx=20, pady=20)
        grid_card.pack(pady=(22, 12))

        self._build_grid(grid_card)

        # ------------------------------------------------------------
        # Mensajes de error / sugerencia
        # ------------------------------------------------------------
        tk.Label(outer, textvariable=self.error_var, font=FONTS["body"],
                 bg=COLORS["bg_darkest"], fg=COLORS["danger"],
                 wraplength=900, justify="left").pack(anchor="w")

        tk.Label(outer, textvariable=self.suggestion_var, font=FONTS["body"],
                 bg=COLORS["bg_darkest"], fg=COLORS["warning"],
                 wraplength=900, justify="left").pack(anchor="w", pady=(2, 0))

        # ------------------------------------------------------------
        # Footer: navegación
        # ------------------------------------------------------------
        footer = tk.Frame(outer, bg=COLORS["bg_darkest"])
        footer.pack(fill="x", pady=(16, 0))

        btn_back = tk.Button(footer, text="←  Volver",
                              command=lambda: controller.show_frame(SetupScreen))
        style_button(btn_back, kind="secondary")
        btn_back.pack(side="left")

        btn_continue = tk.Button(footer, text="Verificar y continuar  →",
                                  command=self._on_verify)
        style_button(btn_continue, kind="primary")
        btn_continue.pack(side="right")

    # ---------------------------------------------------------------
    def _build_grid(self, parent):
        # Esquina superior izquierda vacía
        tk.Label(parent, text="", bg=COLORS["bg_dark"], width=4).grid(row=0, column=0)

        # Encabezados de columna
        for j in range(self.n):
            tk.Label(parent, text=self.labels[j], font=FONTS["body_bold"],
                     bg=COLORS["bg_dark"], fg=COLORS["accent2"],
                     width=5).grid(row=0, column=j + 1, pady=4)

        for i in range(self.n):
            # Encabezado de fila
            tk.Label(parent, text=self.labels[i], font=FONTS["body_bold"],
                     bg=COLORS["bg_dark"], fg=COLORS["accent2"],
                     width=4).grid(row=i + 1, column=0, padx=4)

            for j in range(self.n):
                if i == j:
                    tk.Label(parent, text="—", bg=COLORS["bg_medium"],
                             fg=COLORS["text_muted"], width=5, height=1,
                             relief="flat").grid(row=i + 1, column=j + 1,
                                                  padx=2, pady=2)
                elif i < j:
                    entry = tk.Entry(parent, width=5, font=FONTS["body"],
                                      justify="center", relief="flat",
                                      bg=COLORS["bg_medium"],
                                      fg=COLORS["text_primary"],
                                      insertbackground=COLORS["text_primary"],
                                      highlightthickness=2,
                                      highlightbackground=COLORS["bg_light"],
                                      highlightcolor=COLORS["accent"])
                    entry.grid(row=i + 1, column=j + 1, padx=2, pady=2, ipady=4)
                    self.entries[(i, j)] = entry
                else:
                    # Triángulo inferior: espejo visual del superior (no editable)
                    tk.Label(parent, text="↕", bg=COLORS["bg_medium"],
                             fg=COLORS["text_muted"], width=5,
                             relief="flat").grid(row=i + 1, column=j + 1,
                                                  padx=2, pady=2)

    # ---------------------------------------------------------------
    def _reset_highlights(self):
        for entry in self.entries.values():
            entry.configure(highlightbackground=COLORS["bg_light"])

    def _highlight_missing(self, missing_pairs):
        missing_set = {frozenset(p) for p in missing_pairs}
        for (i, j), entry in self.entries.items():
            if frozenset((i, j)) in missing_set:
                entry.configure(highlightbackground=COLORS["danger"])

    # ---------------------------------------------------------------
    def _on_verify(self):
        self.error_var.set("")
        self.suggestion_var.set("")
        self._reset_highlights()

        graph = Graph(self.n)

        # Parsear e validar cada casilla completada
        for (i, j), entry in self.entries.items():
            text = entry.get().strip()
            if text == "":
                continue
            try:
                weight = float(text)
            except ValueError:
                self.error_var.set(
                    f"El valor '{text}' en la arista {self.labels[i]}-{self.labels[j]} "
                    "no es un número válido."
                )
                entry.configure(highlightbackground=COLORS["danger"])
                return
            if weight <= 0:
                self.error_var.set(
                    f"El peso de la arista {self.labels[i]}-{self.labels[j]} debe ser positivo."
                )
                entry.configure(highlightbackground=COLORS["danger"])
                return
            graph.add_edge(i, j, weight)

        if len(graph.edges) < self.n:
            self.suggestion_var.set(
                "Aún no hay suficientes aristas para siquiera intentar un ciclo "
                "hamiltoniano (se necesitan al menos n aristas)."
            )

        if graph.is_hamiltonian_feasible():
            self.controller.state_data["graph"] = graph
            self.controller.show_frame(GraphVisualizationScreen)
            return

        # No factible: sugerir las aristas mínimas faltantes
        best_cycle, missing = graph.suggest_missing_edges_for_cycle()
        self._highlight_missing(missing)
        missing_labels = graph.labeled_missing_edges(missing)
        self.suggestion_var.set(
            "Con las aristas actuales todavía no se puede formar un ciclo "
            "hamiltoniano. Te sugerimos agregar el peso de estas aristas "
            "(resaltadas en rojo): " + ", ".join(missing_labels)
        )


class GraphVisualizationScreen(tk.Frame):
    """
    Etapa 6: visualización gráfica del grafo ya validado (matplotlib
    embebido en Tkinter), con sus etiquetas y pesos. Muestra además un
    ejemplo de ciclo hamiltoniano resaltado sobre el dibujo.

    Esta pantalla reemplaza a la anterior GraphReadyScreen (resumen
    textual). En la entrega final, aquí se agregará la exploración
    interactiva de todos los ciclos, la matriz de costos y el resaltado
    del ciclo óptimo (actualmente se muestra solo un ciclo de ejemplo).
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_darkest"])
        self.controller = controller
        graph = controller.state_data["graph"]

        outer = tk.Frame(self, bg=COLORS["bg_darkest"], padx=48, pady=24)
        outer.pack(fill="both", expand=True)

        Header(
            outer, step_text="PASO 3 DE 4 · GRAFO VÁLIDO ✔",
            title_text="Representación gráfica del grafo",
            subtitle_text=("Este es el grafo ponderado construido. El ciclo en ámbar "
                            "es un ejemplo de ciclo hamiltoniano válido encontrado."),
        ).pack(anchor="w", fill="x")

        body = tk.Frame(outer, bg=COLORS["bg_darkest"])
        body.pack(fill="both", expand=True, pady=(16, 8))
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)

        # ------------------------------------------------------------
        # Panel izquierdo: grafo dibujado
        # ------------------------------------------------------------
        canvas_card = tk.Frame(body, bg=COLORS["bg_dark"], padx=10, pady=10)
        canvas_card.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

        cycle = graph.find_hamiltonian_cycle()
        self.graph_canvas = GraphCanvas(canvas_card, graph)
        self.graph_canvas.widget.pack(fill="both", expand=True)
        self.graph_canvas.update(graph, highlight_cycle=cycle)

        # ------------------------------------------------------------
        # Panel derecho: información resumida
        # ------------------------------------------------------------
        info_card = tk.Frame(body, bg=COLORS["bg_dark"], padx=22, pady=20)
        info_card.grid(row=0, column=1, sticky="nsew")

        tk.Label(info_card, text="Resumen del grafo", font=FONTS["heading"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_primary"]
                 ).pack(anchor="w", pady=(0, 10))

        tk.Label(info_card, text=f"Nodos: {graph.n}  ({', '.join(graph.labels)})",
                 font=FONTS["body"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_secondary"], wraplength=320,
                 justify="left").pack(anchor="w", pady=3)

        tk.Label(info_card, text=f"Aristas: {len(graph.edges)} de "
                                  f"{graph.n * (graph.n - 1) // 2} posibles",
                 font=FONTS["body"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_secondary"], wraplength=320,
                 justify="left").pack(anchor="w", pady=3)

        modo_legible = "Manual" if controller.state_data["mode"] == "manual" else "Aleatorio"
        tk.Label(info_card, text=f"Modo de generación: {modo_legible}",
                 font=FONTS["body"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_secondary"]).pack(anchor="w", pady=3)

        tk.Label(info_card, text="Ejemplo de ciclo hamiltoniano:",
                 font=FONTS["body_bold"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"]).pack(anchor="w", pady=(16, 2))

        tk.Label(info_card, text=graph.labeled_cycle(cycle),
                 font=FONTS["body_bold"], bg=COLORS["bg_dark"],
                 fg=COLORS["accent"], wraplength=320,
                 justify="left").pack(anchor="w", pady=2)

        tk.Label(
            info_card,
            text=("Próximamente (entrega final): exploración paso a paso de "
                  "TODOS los ciclos hamiltonianos, matriz de costos completa, "
                  "y resaltado del ciclo óptimo mediante fuerza bruta."),
            font=FONTS["small"], bg=COLORS["bg_dark"], fg=COLORS["text_muted"],
            wraplength=320, justify="left",
        ).pack(anchor="w", pady=(20, 0))

        # ------------------------------------------------------------
        # Footer
        # ------------------------------------------------------------
        edit_target = (ManualEdgesScreen if controller.state_data["mode"] == "manual"
                       else RandomGraphScreen)
        footer = tk.Frame(outer, bg=COLORS["bg_darkest"])
        footer.pack(fill="x", pady=(10, 0))

        btn_back = tk.Button(outer, text="←  Editar grafo",
                              command=lambda: controller.show_frame(edit_target))
        style_button(btn_back, kind="secondary")
        btn_back.pack(in_=footer, side="left")


class RandomGraphScreen(tk.Frame):
    """
    Etapa 5: generación aleatoria del grafo.

    El usuario ajusta:
        - la densidad de conexiones (% de las aristas posibles a incluir),
        - el rango de pesos (mínimo y máximo).

    Al generar, el sistema arma un grafo aleatorio con esos parámetros.
    Si el resultado no permite un ciclo hamiltoniano, se completan
    automáticamente las aristas mínimas necesarias (con un peso también
    aleatorio dentro del rango elegido) y se informa cuáles se agregaron,
    para que el usuario entienda que el sistema garantizó la factibilidad.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_darkest"])
        self.controller = controller
        self.n = controller.state_data["n"]
        self.graph = None

        outer = tk.Frame(self, bg=COLORS["bg_darkest"], padx=48, pady=30)
        outer.pack(fill="both", expand=True)

        Header(
            outer, step_text="PASO 2 DE 4",
            title_text="Generación aleatoria del grafo",
            subtitle_text=("Ajusta los parámetros y genera el grafo. Si hace falta, "
                            "el sistema completará automáticamente las aristas "
                            "mínimas para garantizar un ciclo hamiltoniano."),
        ).pack(anchor="w", fill="x")

        # ------------------------------------------------------------
        # Tarjeta de parámetros
        # ------------------------------------------------------------
        params_card = tk.Frame(outer, bg=COLORS["bg_dark"], padx=28, pady=22)
        params_card.pack(fill="x", pady=(24, 14))

        # Densidad
        tk.Label(params_card, text="Densidad de conexiones (%)",
                 font=FONTS["body_bold"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"]).grid(row=0, column=0, sticky="w", pady=6)
        self.density_var = tk.IntVar(value=60)
        tk.Spinbox(params_card, from_=20, to=100, increment=5, width=5,
                   textvariable=self.density_var, font=FONTS["body"],
                   justify="center", bg=COLORS["bg_medium"],
                   fg=COLORS["text_primary"], buttonbackground=COLORS["bg_light"],
                   relief="flat").grid(row=0, column=1, sticky="w", padx=12)
        tk.Label(params_card, text="(mayor % = grafo más conectado)",
                 font=FONTS["small"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_muted"]).grid(row=0, column=2, sticky="w")

        # Rango de pesos
        tk.Label(params_card, text="Peso mínimo", font=FONTS["body_bold"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_primary"]
                 ).grid(row=1, column=0, sticky="w", pady=6)
        self.min_w_var = tk.IntVar(value=1)
        tk.Spinbox(params_card, from_=1, to=99, width=5,
                   textvariable=self.min_w_var, font=FONTS["body"],
                   justify="center", bg=COLORS["bg_medium"],
                   fg=COLORS["text_primary"], buttonbackground=COLORS["bg_light"],
                   relief="flat").grid(row=1, column=1, sticky="w", padx=12)

        tk.Label(params_card, text="Peso máximo", font=FONTS["body_bold"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_primary"]
                 ).grid(row=2, column=0, sticky="w", pady=6)
        self.max_w_var = tk.IntVar(value=20)
        tk.Spinbox(params_card, from_=2, to=100, width=5,
                   textvariable=self.max_w_var, font=FONTS["body"],
                   justify="center", bg=COLORS["bg_medium"],
                   fg=COLORS["text_primary"], buttonbackground=COLORS["bg_light"],
                   relief="flat").grid(row=2, column=1, sticky="w", padx=12)

        btn_generate = tk.Button(params_card, text="🎲  Generar grafo aleatorio",
                                  command=self._on_generate)
        style_button(btn_generate, kind="primary")
        btn_generate.grid(row=3, column=0, columnspan=3, sticky="w", pady=(16, 0))

        # ------------------------------------------------------------
        # Resultado
        # ------------------------------------------------------------
        self.error_var = tk.StringVar(value="")
        tk.Label(outer, textvariable=self.error_var, font=FONTS["body"],
                 bg=COLORS["bg_darkest"], fg=COLORS["danger"],
                 wraplength=900, justify="left").pack(anchor="w")

        self.result_card = tk.Frame(outer, bg=COLORS["bg_dark"], padx=28, pady=20)
        self.result_placeholder = tk.Label(
            self.result_card, text="Aún no se ha generado ningún grafo.",
            font=FONTS["body"], bg=COLORS["bg_dark"], fg=COLORS["text_muted"],
        )
        self.result_placeholder.pack(anchor="w")
        self.result_card.pack(fill="x", pady=(4, 14))

        # ------------------------------------------------------------
        # Footer
        # ------------------------------------------------------------
        footer = tk.Frame(outer, bg=COLORS["bg_darkest"])
        footer.pack(fill="x", pady=(6, 0))

        btn_back = tk.Button(footer, text="←  Volver",
                              command=lambda: controller.show_frame(SetupScreen))
        style_button(btn_back, kind="secondary")
        btn_back.pack(side="left")

        self.btn_continue = tk.Button(footer, text="Continuar  →",
                                       command=self._on_continue)
        style_button(self.btn_continue, kind="ghost")
        self.btn_continue.pack(side="right")

    # ---------------------------------------------------------------
    def _on_generate(self):
        self.error_var.set("")

        min_w = self.min_w_var.get()
        max_w = self.max_w_var.get()
        if min_w >= max_w:
            self.error_var.set("El peso mínimo debe ser menor que el peso máximo.")
            return

        density = self.density_var.get() / 100.0
        graph = Graph(self.n)

        # Generar aristas aleatorias según la densidad elegida
        possible_pairs = [(i, j) for i in range(self.n) for j in range(i + 1, self.n)]
        random.shuffle(possible_pairs)
        for (i, j) in possible_pairs:
            if random.random() < density:
                graph.add_edge(i, j, random.randint(min_w, max_w))

        auto_added = []
        if not graph.is_hamiltonian_feasible():
            _, missing = graph.suggest_missing_edges_for_cycle()
            for (i, j) in missing:
                w = random.randint(min_w, max_w)
                graph.add_edge(i, j, w)
                auto_added.append((i, j, w))

        self.graph = graph
        self._render_result(graph, auto_added)
        style_button(self.btn_continue, kind="primary")

    def _render_result(self, graph, auto_added):
        for widget in self.result_card.winfo_children():
            widget.destroy()

        tk.Label(self.result_card, text=f"Grafo generado: {len(graph.edges)} aristas",
                 font=FONTS["body_bold"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"]).pack(anchor="w", pady=2)

        edges_txt = ", ".join(
            f"{graph.labels[i]}-{graph.labels[j]} ({w:g})"
            for i, j, w in graph.edge_list()
        )
        tk.Label(self.result_card, text=edges_txt, font=FONTS["body"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_secondary"],
                 wraplength=900, justify="left").pack(anchor="w", pady=2)

        if auto_added:
            added_txt = ", ".join(
                f"{graph.labels[i]}-{graph.labels[j]} ({w:g})"
                for i, j, w in auto_added
            )
            tk.Label(
                self.result_card,
                text=("⚠ El grafo aleatorio no permitía un ciclo hamiltoniano, así "
                      f"que se agregaron automáticamente: {added_txt}"),
                font=FONTS["body"], bg=COLORS["bg_dark"], fg=COLORS["warning"],
                wraplength=900, justify="left",
            ).pack(anchor="w", pady=(8, 2))
        else:
            tk.Label(
                self.result_card,
                text="✔ El grafo generado ya permite un ciclo hamiltoniano por sí solo.",
                font=FONTS["body"], bg=COLORS["bg_dark"], fg=COLORS["success"],
            ).pack(anchor="w", pady=(8, 2))

    # ---------------------------------------------------------------
    def _on_continue(self):
        if self.graph is None:
            self.error_var.set("Primero genera un grafo aleatorio.")
            return
        self.controller.state_data["graph"] = self.graph
        self.controller.show_frame(GraphVisualizationScreen)