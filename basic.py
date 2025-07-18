# Implementation of Basic(G, P, S) algorithm described in README

from collections import defaultdict
import heapq
import random
import argparse
from typing import Dict, Iterable, List, Set, Tuple

try:
    import networkx as nx  # type: ignore
    Graph = nx.Graph
except Exception:  # pragma: no cover - network access blocked
    class Graph:
        """Minimal NetworkX-like undirected graph used as fallback."""

        def __init__(self) -> None:
            self._adj: Dict[str, Dict[str, Dict[str, float]]] = defaultdict(dict)

        def add_edge(self, u: str, v: str, weight: float = 1.0) -> None:
            self._adj[u][v] = {"weight": weight}
            self._adj[v][u] = {"weight": weight}

        def neighbors(self, v: str):
            return self._adj.get(v, {}).keys()

        def __getitem__(self, item: str):
            return self._adj[item]

        def nodes(self):
            return self._adj.keys()

    class nx:  # type: ignore
        Graph = Graph


def generate_graph(
    num_vertices: int = 20, edge_prob: float = 0.3,
    label_pool: Iterable[str] | None = None
) -> Tuple[Graph, Dict[str, Set[str]]]:
    """Generate a random undirected graph with labels on vertices."""

    if label_pool is None:
        label_pool = [chr(ord("a") + i) for i in range(6)]

    g = Graph()
    vertices = [f"v{i}" for i in range(num_vertices)]
    labels: Dict[str, Set[str]] = {}

    if hasattr(g, "add_nodes_from"):
        g.add_nodes_from(vertices)
    else:  # fallback Graph
        for v in vertices:
            g._adj.setdefault(v, {})  # type: ignore[attr-defined]

    # Assign labels to vertices
    for v in vertices:
        k = random.randint(1, max(1, len(label_pool) // 2))
        labels[v] = set(random.sample(list(label_pool), k=k))

    # Create random edges with weights 1..10
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < edge_prob:
                w = random.randint(1, 10)
                g.add_edge(vertices[i], vertices[j], weight=w)

    return g, labels


def graph_size(graph: Graph) -> Tuple[int, int]:
    """Return the number of vertices and edges of ``graph``."""
    if hasattr(graph, "number_of_nodes"):
        return graph.number_of_nodes(), graph.number_of_edges()
    # fallback Graph
    num_nodes = len(list(graph.nodes()))
    num_edges = sum(len(graph[v]) for v in graph.nodes()) // 2
    return num_nodes, num_edges


def basic(graph: Graph, P: Set[str], S: Dict[str, Set[str]]) -> Tuple[float, List[str]]:
    """Compute a minimal-cost path that covers all labels in ``P``.

    The function explores vertex-label combinations using a priority
    queue similar to Dijkstra search. Each state tracks the current
    vertex, the set of collected labels and the path taken so far. The
    returned path is a list of vertices describing the order in which
    they are visited.

    Parameters
    ----------
    graph : Graph
        Undirected weighted graph.
    P : set
        Labels that must be covered.
    S : dict
        Mapping from vertex to set of labels.

    Returns
    -------
    Tuple[float, List[str]]
        The cost of the path and the sequence of vertices visited. If no path
        covers ``P`` the cost will be ``+inf`` and the path will be empty.
    """
    P = set(P)
    best_cost = float('inf')
    best_path: List[str] = []

    visited: Dict[Tuple[str, frozenset], float] = {}
    pq: List[Tuple[float, str, frozenset, List[str]]] = []

    for v in graph.nodes():
        start_labels = S.get(v, set()) & P
        state = (v, frozenset(start_labels))
        visited[state] = 0.0
        heapq.heappush(pq, (0.0, v, state[1], [v]))

    while pq:
        cost, v, labels, path = heapq.heappop(pq)
        if cost != visited.get((v, labels)):
            continue
        if cost >= best_cost:
            continue
        if P.issubset(labels):
            if cost < best_cost:
                best_cost = cost
                best_path = path
            continue

        for u in graph.neighbors(v):
            w = graph[v][u].get("weight", 1.0)
            new_labels = labels | (S.get(u, set()) & P)
            new_state = (u, frozenset(new_labels))
            new_cost = cost + w
            if new_cost < visited.get(new_state, float('inf')):
                visited[new_state] = new_cost
                heapq.heappush(pq, (new_cost, u, new_state[1], path + [u]))

    return best_cost, best_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Basic algorithm on a random graph")
    parser.add_argument("--nodes", type=int, default=100000, help="number of vertices in the random graph")
    parser.add_argument("--prob", type=float, default=0.2, help="edge probability for the random graph")
    args = parser.parse_args()

    random.seed(42)
    G, labels = generate_graph(num_vertices=args.nodes, edge_prob=args.prob)
    n, m = graph_size(G)

    all_labels = sorted({p for lbls in labels.values() for p in lbls})
    query = set(random.sample(all_labels, k=min(4, len(all_labels))))

    cost, path = basic(G, query, labels)
    print(f"Graph size: {n} vertices, {m} edges")
    print("Query labels:", query)
    print("Cost:", cost)
    print("Path:", " -> ".join(path))
