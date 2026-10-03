"""
graph_model.py
--------------
Lógica matemática pura del grafo no dirigido y ponderado usado en el
Problema del Agente Viajero. Sin dependencias de interfaz gráfica, para
poder probarla de forma aislada (ver bloque de pruebas al final del
archivo).

Responsabilidades de este módulo:
    1. Representar nodos y aristas con peso (distancia/costo/tiempo).
    2. Construir la matriz de costos (adyacencia).
    3. Verificar si el grafo permite al menos un ciclo hamiltoniano.
    4. Si no lo permite, determinar qué aristas mínimas faltan para
       completar al menos un ciclo hamiltoniano válido.

La búsqueda de "todos" los ciclos hamiltonianos y el cálculo de fuerza
bruta del costo total de cada uno se implementará en tsp_solver.py
(entrega final), ya que corresponde a la etapa de resolución, no de
modelado del grafo.
"""

from itertools import permutations
import math
import string


def node_label(index):
    """Convierte un índice 0,1,2,... en una etiqueta A,B,C,...
    (más amigable para el usuario que mostrar números crudos)."""
    return string.ascii_uppercase[index]


class Graph:
    """Grafo no dirigido y ponderado con n nodos (5 <= n <= 10)."""

    def __init__(self, n):
        if not (5 <= n <= 10):
            raise ValueError("n debe estar en el rango [5, 10].")
        self.n = n
        self.labels = [node_label(i) for i in range(n)]
        # Las aristas se guardan como diccionario:
        #   clave   -> frozenset({i, j})  (no dirigido, sin duplicados)
        #   valor   -> peso (float)
        self.edges = {}

    # -----------------------------------------------------------------
    # Construcción del grafo
    # -----------------------------------------------------------------
    def add_edge(self, i, j, weight):
        """Agrega (o actualiza) la arista no dirigida entre los nodos i, j."""
        if i == j:
            raise ValueError("No se permiten bucles (arista de un nodo a sí mismo).")
        if weight <= 0:
            raise ValueError("El peso de la arista debe ser un número positivo.")
        self.edges[frozenset((i, j))] = float(weight)

    def remove_edge(self, i, j):
        self.edges.pop(frozenset((i, j)), None)

    def has_edge(self, i, j):
        return frozenset((i, j)) in self.edges

    def get_weight(self, i, j):
        return self.edges.get(frozenset((i, j)))

    def edge_list(self):
        """Devuelve la lista de aristas como tuplas (i, j, peso)."""
        return [(min(e), max(e), w) for e, w in self.edges.items()
                for e in [tuple(e)]]

    def degree(self, node):
        return sum(1 for e in self.edges if node in e)

    def is_complete(self):
        """True si el grafo tiene todas las aristas posibles (K_n)."""
        max_edges = self.n * (self.n - 1) // 2
        return len(self.edges) == max_edges

    # -----------------------------------------------------------------
    # Matriz de costos
    # -----------------------------------------------------------------
    def cost_matrix(self):
        """Matriz n x n. Usa math.inf donde no existe arista (o 0 en la
        diagonal). Índices y filas/columnas corresponden a self.labels."""
        matrix = [[0.0 if i == j else math.inf for j in range(self.n)]
                  for i in range(self.n)]
        for edge, w in self.edges.items():
            i, j = tuple(edge)
            matrix[i][j] = w
            matrix[j][i] = w
        return matrix

    # -----------------------------------------------------------------
    # Factibilidad hamiltoniana
    # -----------------------------------------------------------------
    def find_hamiltonian_cycle(self):
        """
        Busca UN ciclo hamiltoniano válido usando solo las aristas
        existentes (para verificar factibilidad). Fija el nodo 0 como
        inicio (un ciclo no tiene inicio real, así que esto no pierde
        generalidad) y recorre permutaciones de los nodos restantes.

        Retorna la lista de nodos del ciclo (ej. [0, 2, 1, 3, 4]) si
        existe, o None si el grafo no admite ningún ciclo hamiltoniano.
        """
        nodes = list(range(self.n))
        first = nodes[0]
        rest = nodes[1:]

        for perm in permutations(rest):
            cycle = [first] + list(perm)
            if self._is_valid_cycle(cycle):
                return cycle
        return None

    def _is_valid_cycle(self, cycle):
        """Verifica que todas las aristas consecutivas del ciclo (incluyendo
        el cierre del último nodo al primero) existan en el grafo."""
        n = len(cycle)
        for k in range(n):
            a, b = cycle[k], cycle[(k + 1) % n]
            if not self.has_edge(a, b):
                return False
        return True

    def is_hamiltonian_feasible(self):
        """True si existe al menos un ciclo hamiltoniano con las aristas
        actuales del grafo."""
        return self.find_hamiltonian_cycle() is not None

    def suggest_missing_edges_for_cycle(self):
        """
        Si el grafo YA es factible, retorna (cycle, []) con un ciclo
        hamiltoniano existente y ninguna arista faltante.

        Si NO es factible, busca —entre todas las ordenaciones posibles
        de los nodos— la que requiere agregar la MENOR cantidad de
        aristas nuevas para convertirse en un ciclo hamiltoniano válido,
        y retorna (cycle, missing_edges) donde missing_edges es la lista
        de tuplas (i, j) que el usuario debería incorporar.

        Nota de complejidad: se evalúan (n-1)!/2 ordenaciones distintas
        (fijando el primer nodo y sin contar el mismo ciclo en sentido
        inverso dos veces). Para n <= 10 esto es como máximo 181 440
        combinaciones, perfectamente manejable.
        """
        nodes = list(range(self.n))
        first = nodes[0]
        rest = nodes[1:]

        best_cycle = None
        best_missing = None

        seen_reversed = set()

        for perm in permutations(rest):
            cycle = [first] + list(perm)

            # Evitar procesar dos veces el mismo ciclo en sentido inverso
            key = tuple(cycle)
            rev_key = tuple([cycle[0]] + cycle[1:][::-1])
            if rev_key in seen_reversed:
                continue
            seen_reversed.add(key)

            missing = self._missing_edges_of_cycle(cycle)

            if best_missing is None or len(missing) < len(best_missing):
                best_cycle, best_missing = cycle, missing
                if len(missing) == 0:
                    break  # ya es factible, no se puede mejorar más

        return best_cycle, best_missing

    def _missing_edges_of_cycle(self, cycle):
        """Lista de aristas (i, j) del ciclo dado que NO existen todavía
        en el grafo."""
        n = len(cycle)
        missing = []
        for k in range(n):
            a, b = cycle[k], cycle[(k + 1) % n]
            if not self.has_edge(a, b):
                missing.append((a, b))
        return missing

    def labeled_cycle(self, cycle):
        """Convierte un ciclo de índices [0, 2, 1, ...] en etiquetas
        legibles 'A -> C -> B -> ... -> A'."""
        labels = [self.labels[i] for i in cycle] + [self.labels[cycle[0]]]
        return " → ".join(labels)

    def labeled_missing_edges(self, missing):
        """Convierte [(0,2), (1,3)] en ['A - C', 'B - D']."""
        return [f"{self.labels[i]} - {self.labels[j]}" for i, j in missing]


# ---------------------------------------------------------------------
# Bloque de pruebas manuales (se ejecuta solo si corres este archivo
# directamente: `python graph_model.py`). Sirve para validar la lógica
# sin necesidad de la interfaz gráfica.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Prueba 1: grafo completo K5 (siempre factible) ===")
    g = Graph(5)
    for i in range(5):
        for j in range(i + 1, 5):
            g.add_edge(i, j, weight=(i + 1) * (j + 1))
    print("¿Factible?", g.is_hamiltonian_feasible())
    cycle = g.find_hamiltonian_cycle()
    print("Ciclo encontrado:", g.labeled_cycle(cycle))
    print()

    print("=== Prueba 2: grafo incompleto NO factible ===")
    g2 = Graph(5)
    # Solo un camino, sin cerrar el ciclo: A-B-C-D-E (falta E-A y más)
    g2.add_edge(0, 1, 10)
    g2.add_edge(1, 2, 10)
    g2.add_edge(2, 3, 10)
    g2.add_edge(3, 4, 10)
    print("¿Factible?", g2.is_hamiltonian_feasible())
    best_cycle, missing = g2.suggest_missing_edges_for_cycle()
    print("Mejor ciclo candidato:", g2.labeled_cycle(best_cycle))
    print("Aristas faltantes sugeridas:", g2.labeled_missing_edges(missing))
    print()

    print("=== Matriz de costos (Prueba 1) ===")
    for row in g.cost_matrix():
        print(row)