"""Pruned Dynamic Programming algorithm for Group Steiner Tree."""

from collections import defaultdict
import heapq
from typing import Dict, Iterable, List, Set, Tuple

try:
    import networkx as nx  # type: ignore
    Graph = nx.Graph
except Exception:  # pragma: no cover - network access blocked
    class Graph:
        """Minimal undirected graph used if networkx is unavailable."""

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
    num_vertices: int = 20,
    edge_prob: float = 0.3,
    label_pool: Iterable[str] | None = None,
) -> Tuple[Graph, Dict[str, Set[str]]]:
    """Generate a random undirected graph with vertex labels."""
    import random

    if label_pool is None:
        label_pool = [chr(ord("a") + i) for i in range(20)]

    g = Graph()
    vertices = [f"v{i}" for i in range(num_vertices)]
    labels: Dict[str, Set[str]] = {}

    if hasattr(g, "add_nodes_from"):
        g.add_nodes_from(vertices)
    else:
        for v in vertices:
            g._adj.setdefault(v, {})  # type: ignore[attr-defined]

    for v in vertices:
        k = random.randint(1, max(1, 2))
        labels[v] = set(random.sample(list(label_pool), k=k))

    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < edge_prob:
                w = random.randint(1, 10)
                g.add_edge(vertices[i], vertices[j], weight=w)

    return g, labels


def pruned_dp(graph: Graph, P: Set[str], S: Dict[str, Set[str]]) -> Tuple[float, List[str]]:
    """Compute a minimal-cost tree covering ``P`` using pruning heuristics."""
    P = set(P)
    best_cost = float("inf")
    best_path: List[str] = []

    visited: Dict[Tuple[str, frozenset], float] = {}
    pq: List[Tuple[float, str, frozenset, List[str]]] = []

    # Initialize start states for each vertex and label
    for v in graph.nodes():
        for lbl in S.get(v, set()) & P:
            state = (v, frozenset({lbl}))
            if 0.0 >= visited.get(state, float("inf")):
                continue
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

        # prune if cost already too large compared to best
        if cost > best_cost * 2 / 3:
            continue

        # expand to neighbours
        for u in graph.neighbors(v):
            w = graph[v][u].get("weight", 1.0)
            new_cost = cost + w
            if new_cost >= best_cost:
                continue
            new_labels = labels | (S.get(u, set()) & P)
            new_state = (u, frozenset(new_labels))
            if new_cost < visited.get(new_state, float("inf")):
                visited[new_state] = new_cost
                heapq.heappush(pq, (new_cost, u, new_state[1], path + [u]))

        # try to combine with other partial solutions at the same vertex
        remaining = P - set(labels)
        for (vv, lbls), c in list(visited.items()):
            if vv != v:
                continue
            if not set(lbls).issubset(remaining) or not lbls:
                continue
            new_labels = labels | set(lbls)
            new_cost = cost + c
            key = (v, frozenset(new_labels))
            if new_cost <= best_cost * 2 / 3 and new_cost < visited.get(key, float("inf")):
                visited[key] = new_cost
                heapq.heappush(pq, (new_cost, v, key[1], path))

    return best_cost, best_path

if __name__ == "__main__":
    import random
    import argparse

    parser = argparse.ArgumentParser(description="Run PrunedDP on a random graph")
    parser.add_argument("--nodes", type=int, default=1000, help="number of vertices")
    parser.add_argument("--prob", type=float, default=0.3, help="edge probability")
    args = parser.parse_args()

    random.seed(42)
    G, labels = generate_graph(num_vertices=args.nodes, edge_prob=args.prob)
    all_labels = sorted({p for s in labels.values() for p in s})
    query = set(random.sample(all_labels, k=min(5, len(all_labels))))

    cost, path = pruned_dp(G, query, labels)
    print("Query labels:", query)
    print("Cost:", cost)
    print("Path:", " -> ".join(path))
