"""
theme.py
--------
Paleta de colores, fuentes y utilidades de estilo para toda la aplicación.
Tema: "Grafito & Ámbar" — fondo oscuro elegante con acentos cálidos de alto
contraste, pensado para que se lea bien en proyección/exposición.

Mantener TODOS los colores y fuentes centralizados aquí para que la app
sea visualmente consistente en cada pantalla.
"""

# ---------------------------------------------------------------------------
# PALETA DE COLORES
# ---------------------------------------------------------------------------
COLORS = {
    # Fondos (de más oscuro a más claro)
    "bg_darkest":   "#12141C",   # fondo general de la ventana
    "bg_dark":      "#1B1F2B",   # fondo de paneles/tarjetas
    "bg_medium":    "#242A3A",   # fondo de inputs, listas
    "bg_light":     "#2F3648",   # hover / bordes sutiles

    # Texto
    "text_primary":   "#F2F3F7",  # texto principal (casi blanco)
    "text_secondary": "#A9AFC3",  # texto secundario / descripciones
    "text_muted":      "#6B7280",  # texto deshabilitado / placeholders

    # Acento principal (ámbar) — botones primarios, resaltados
    "accent":         "#F2A93B",
    "accent_hover":   "#FFC266",
    "accent_dark":    "#C6811F",

    # Acento secundario (cian frío) — info, aristas normales del grafo
    "accent2":        "#4FD1C5",
    "accent2_dark":   "#2FA79C",

    # Estados semánticos
    "success":  "#4ADE80",   # ciclo válido / factible
    "danger":   "#F87171",   # error / falta de aristas / no factible
    "warning":  "#FBBF24",   # advertencia

    # Grafo
    "node_fill":       "#2F3648",
    "node_border":     "#F2A93B",
    "node_text":       "#F2F3F7",
    "edge_default":    "#4FD1C5",
    "edge_optimal":    "#F2A93B",
    "edge_missing":    "#F87171",
}

# ---------------------------------------------------------------------------
# FUENTES
# ---------------------------------------------------------------------------
FONTS = {
    "title":     ("Segoe UI", 22, "bold"),
    "subtitle":  ("Segoe UI", 13, "normal"),
    "heading":   ("Segoe UI", 15, "bold"),
    "body":      ("Segoe UI", 11, "normal"),
    "body_bold": ("Segoe UI", 11, "bold"),
    "small":     ("Segoe UI", 9, "normal"),
    "button":    ("Segoe UI", 11, "bold"),
    "mono":      ("Consolas", 10, "normal"),
}

# ---------------------------------------------------------------------------
# ESPACIADO / DIMENSIONES
# ---------------------------------------------------------------------------
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
}

WINDOW = {
    "width": 1180,
    "height": 760,
    "min_width": 980,
    "min_height": 640,
    "title": "Problema del Agente Viajero — Fuerza Bruta",
}


def style_button(button, kind="primary"):
    """
    Aplica un estilo consistente a un tk.Button según su rol.
    kind: 'primary' | 'secondary' | 'danger' | 'ghost'
    """
    base = {
        "font": FONTS["button"],
        "relief": "flat",
        "bd": 0,
        "cursor": "hand2",
        "activeforeground": COLORS["text_primary"],
        "padx": 18,
        "pady": 10,
    }

    if kind == "primary":
        base.update(
            bg=COLORS["accent"],
            fg=COLORS["bg_darkest"],
            activebackground=COLORS["accent_hover"],
        )
    elif kind == "secondary":
        base.update(
            bg=COLORS["bg_light"],
            fg=COLORS["text_primary"],
            activebackground=COLORS["bg_medium"],
        )
    elif kind == "danger":
        base.update(
            bg=COLORS["danger"],
            fg=COLORS["bg_darkest"],
            activebackground="#FCA5A5",
        )
    elif kind == "ghost":
        base.update(
            bg=COLORS["bg_dark"],
            fg=COLORS["text_secondary"],
            activebackground=COLORS["bg_medium"],
        )

    button.configure(**base)

    # Efecto hover manual (tk no lo trae nativo para bg)
    normal_bg = base["bg"]
    hover_bg = base["activebackground"]

    def on_enter(_e):
        button.configure(bg=hover_bg)

    def on_leave(_e):
        button.configure(bg=normal_bg)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)