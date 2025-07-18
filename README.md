# Basic(G, P, S) Algorithm

## Overview
The `Basic(G, P, S)` algorithm computes the **minimum weight tree** in a labeled undirected graph that **covers a given set of labels `P`** using a label-aware variant of shortest path and minimum spanning tree computations. It is a fundamental approach for solving problems like **Group Steiner Tree** in label-based graphs.

---

## Input
- **G = (V, E)**: An undirected graph with vertices `V` and edges `E`. Each edge `(u, v)` has a non-negative weight `w(u, v)`.
- **S**: A mapping from vertices to their label sets, i.e., `S_v` denotes the set of labels assigned to vertex `v`.
- **P**: A set of labels (query set) that the output tree must cover.

---

## Output
- The minimum weight of a tree in `G` whose vertices collectively cover all labels in `P`.

---

## Algorithm Steps

### Initialization
1. Initialize a priority queue `Q` and a visited dictionary `D`.
2. Set `best ← ∞` to store the weight of the best feasible solution found.
3. For every vertex `v ∈ V`, and every label `p ∈ S_v`, initialize the queue with node `(v, {p})` and cost 0.

### Main Loop
4. While the priority queue `Q` is not empty:
   - Pop the state `((v, X), cost)` with the smallest cost.
   - If `X` covers all query labels `P`, return `cost` as the result.
   - Record that `(v, X)` has been visited with cost.
   - Let `X̄ = P \ X` be the remaining uncovered labels.
   - For each label `p ∈ X̄`, construct:
     - A temporary tree `T'` by connecting `v` to a node `v̄_p` that contains label `p` using the shortest path.
   - Merge `T'` with existing tree `T(v, X)` and construct the MST `T̃(v, P)`.
   - Update the best solution with the cost of `T̃(v, P)`.

### Expansion
5. For each edge `(v, u) ∈ E`, attempt to move to `(u, X)` with updated cost.
6. For each visited `(v, X') ∈ D`, combine label sets to `X' ∪ X`, and attempt to update cost and push into `Q`.

### Termination
7. If no tree covers `P` after full expansion, return `+∞`.

---

## Update Procedure
A helper function that:
- Prunes states that are already visited or more costly than current `best`.
- Updates `best` if a complete label set is found.
- Pushes or updates the queue with better cost paths to `(v, X)`.

---

## Remarks
- This algorithm is label-aware and explores paths and combinations of vertex-label pairs efficiently.
- The use of MSTs and Shortest-Path ensures connection cost is minimized when completing label coverage.
- Performance can vary with graph size and label distribution, but it guarantees correctness through exhaustive label set exploration.

---

## Complexity
- Worst-case exponential in label size `|P|` due to label subset combinations.
- Practical performance often improved with pruning (`D`) and cost bounding (`best`).

