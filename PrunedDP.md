# PrunedDP

This project implements the **Pruned Dynamic Programming (PrunedDP)** algorithm for solving the Group Steiner Tree (GST) problem in labeled graphs. It is an improved version of the `Basic(G, P, S)` algorithm, with additional pruning strategies to reduce redundant computation and improve performance.

## Goals

- **Input**:  
  - Graph `G = (V, E)` with non-negative edge weights  
  - Label set mapping `S`, where `S_v` is the set of labels assigned to vertex `v`  
  - Query label set `P ⊆ Σ`

- **Output**:  
  - The minimum weight of a tree in `G` whose nodes collectively cover all labels in `P`

## Key Improvements Over Basic Algorithm

- Adds pruning based on:
  - Cost comparison with current `best` solution
  - Avoidance of unnecessary expansion beyond a threshold (1/2 or 2/3 × best)
  - Early stopping via direct completion detection using memoized sub-solutions

---

## Core Algorithm Steps

1. **Initialization**:
   - Create a min-priority queue `Q` for states `(v, X)`
   - Maintain a dictionary `D` recording the best-known cost to `(v, X)`
   - Set `best` to ∞ (best feasible solution so far)

2. **Start States**:
   - For each node `v` and each label `p ∈ S_v`, initialize `(v, {p})` in `Q` with cost 0

3. **Main Loop**:
   - While `Q` is not empty:
     - Pop `(v, X)` with minimal `cost` from `Q`
     - If `X` covers `P`, return `cost`
     - Save current state in `D`, compute remaining labels `X̄ = P \ X`
     - For each `p ∈ X̄`, connect `v` to `v̄_p` using `Shortest-Path(v, v̄_p)`
     - Construct tree `T̃(v, P)` via MST on merged partial trees
     - Update `best` solution if `T̃(v, P)` is better

4. **Pruning & Updates**:
   - If `(v, X̄)` ∈ `D`, consider completing the solution directly with stored cost
   - Skip updates if current `cost` exceeds `best / 2`
   - For each edge `(v, u)`, expand to `(u, X)` with additional cost `w(v, u)`
   - For memoized subsets `(v, X′)` ⊆ `X̄`, try combining `X ∪ X′` with cost pruning:
     - Only update if `cost + cost′ ≤ (2/3) * best`

5. **Termination**:
   - If `Q` is exhausted and no full solution is found, return ∞

---

## To Do

- [ ] Implement shortest path logic between nodes and virtual label terminals
- [ ] Implement MST construction on trees `T′(v, X̄)` and `T(v, X)`
- [ ] Add pruning logic based on best solution thresholds (`1/2`, `2/3`)
- [ ] Efficiently memoize and lookup state costs with dictionary `D`
- [ ] Integrate update conditions as specified in lines 16–25

---

## Notes for Codex

- States are tuples `(v, X)` where `v` is the current node and `X` is the set of covered labels
- `Q` is a priority queue sorted by `cost`
- Use dictionaries for:
  - `D[(v, X)]`: memoized cost to `(v, X)`
  - `Q.cost((v, X))`: current queue cost (if exists)
- The pruning conditions at lines 16–25 are essential for performance and correctness
- Make sure to check subset conditions and cost thresholds accurately

