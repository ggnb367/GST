## 🧠 Basic Progressive GST Algorithm

This implementation is based on the Basic algorithm proposed in the paper *"Finding Top-k Min-Cost Connected Trees in Databases"*. It follows a progressive search framework to solve the Group Steiner Tree (GST) problem with increasing approximation quality over rounds.

### 🔍 Problem Overview

Given:
- A labeled graph \( G = (V, E) \)
- A query keyword set \( P \), where each \( p \in P \) corresponds to a group of vertices \( S_p \subseteq V \)

Goal:
- Find a minimum-cost connected tree \( T \subseteq G \) that includes at least one node from each group \( S_p \)
- Optionally find top-k such trees (this version only targets the 1-best solution)

---

### 🚀 Algorithm Summary: Basic (Progressive GST)

The **Basic** algorithm is a progressive, best-first search that maintains:
- A priority queue \( Q \) of states \( (v, X) \) where:
  - \( v \): current root node
  - \( X \subseteq P \): subset of keywords already covered
- A dictionary \( \mathcal{D} \) to store the best cost found so far for each state

Each state \( (v, X) \) represents a partial solution tree rooted at \( v \), covering keyword set \( X \). The algorithm expands states using dynamic programming transition rules and computes an **upper-bound feasible tree** \( \tilde{T}(v, P) \) using:
1. A precomputed shortest path from any node to virtual nodes \( \tilde{v}_p \) for each \( p \in P \)
2. Merging the tree for state \( (v, X) \) and the tree formed by shortest paths to \( \tilde{v}_p \) for \( p \in P \setminus X \)
3. Taking the MST of this union

---

### 💡 Key Properties

- **Progressive**: In every round, a feasible solution and its upper bound are provided
- **Monotonic**: The reported error bound (w.r.t. optimal) is non-increasing over rounds
- **Pruning**: Uses the current best cost to prune unpromising states

---

### 📦 Algorithm Pseudocode (Simplified Overview)

```python
Q ← ∅          # Priority queue for states (v, X)
D ← ∅          # Dictionary to store best cost per state
best ← +∞      # Best feasible solution cost so far

# Initialization: add all single-label states
for v in V:
    for p in Sv:
        Q.push((v, {p}), cost=0)

while Q not empty:
    (v, X), cost ← Q.pop()
    if X == P:
        return cost

    D[(v, X)] ← cost
    X̄ ← P \ X

    # Construct feasible solution by union of T(v, X) and shortest paths to virtual nodes
    T̃(v, P) ← MST(T(v, X) ∪ ShortestPaths(v, X̄))
    best ← min(best, weight(T̃(v, P)))
    report_approximation_ratio(best)

    # DP state transitions
    for each neighbor u of v:
        update(Q, D, (u, X), cost + w(v, u))
    for each X′ ⊆ X̄ and (v, X′) ∈ D:
        update(Q, D, (v, X ∪ X′), cost + D[(v, X′)])
```

---

### ⚙️ Preprocessing: Virtual Node Trick

Before main execution:
- For each label \( p \in P \), add a virtual node \( \tilde{v}_p \)
- Connect it to all \( v \in V \) with label \( p \) via zero-weight edges
- Precompute shortest paths from \( \tilde{v}_p \) to all \( v \in V \) using Dijkstra

---

### 📝 Complexity

- Preprocessing: \( O(k(m + n \log n)) \)
- Search: exponential in worst case, mitigated by pruning

---

### 📈 Approximation Guarantee

At any point, Basic can return:
- Feasible solution \( \tilde{T}(v, P) \)
- Approximation ratio \( f_{\tilde{T}}(v, P) / f^*_{\mathcal{T}}(v, X) \)

---
