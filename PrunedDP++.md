# PrunedDP++

This project implements the **PrunedDP++ algorithm**, an enhanced and tighter-bounded variant of the Group Steiner Tree solver in labeled graphs. It is built upon `PrunedDP` by introducing **lower bound estimation (lb)** for informed search and aggressive pruning.

## Goals

- **Input**:  
  - Graph `G = (V, E)` with edge weights  
  - Label mapping `S`: each vertex `v` has a label set `S_v`  
  - Query label set `P ⊆ Σ`

- **Output**:  
  - Minimum cost of a **connected tree** in `G` covering all labels in `P`

---

## Key Features & Improvements

- Adds **lower bound (`lb`) heuristic estimates** for each state in the search
- Uses `lb` as the **priority in the queue**, enabling more informed pruning
- Introduces `lb1`, `lb2`, and `dist`-based metrics to estimate future cost from uncovered labels
- Maintains tight control over expansion with early stopping and cost threshold checks

---

## Core Algorithm Steps

1. **Preprocessing**:
   - Compute `AllPaths(G, P)`: all-pairs shortest paths between relevant terminals
   - Initialize priority queue `Q` and cost dictionary `D`
   - Set `best ← ∞` to record the best feasible solution found

2. **Initialization**:
   - For each vertex `v` and label `p ∈ S_v`, push `(v, {p})` into `Q` with:
     - `cost = 0`
     - `lb = lb((v, {p}), 0, P)`

3. **Main Loop**:
   - While `Q` is not empty:
     - Pop state `(v, X)` with the **smallest `lb`**
     - If `X == P`, return `best - cost` (solution found)
     - Record cost in `D`, compute `X̄ = P \ X`
     - For all `p ∈ X̄`, connect `v` to `v̄_p` via `Shortest-Path`
     - Construct `T̃(v, P)` via MST from partial and new subtrees
     - Update `best ← min(best, f_T̃(v, P))`

4. **Search Expansion**:
   - If `(v, X̄)` exists in `D`, try finishing via that stored partial cost
   - If current cost < `best / 2`:
     - Expand to all neighbors `(u, X)` with edge cost
     - Merge with stored states `X′ ⊆ X̄` only if `cost + cost′ ≤ (2/3) * best`

5. **Update Function**:
   - Recomputes `lb` using new cost and `P`
   - If `lb >= best`, prune this path
   - If `X == P`, update best feasible cost
   - Insert into `Q` or update existing entry if this path is better

6. **Lower Bound Function `lb((v, X), cost, P)`**:
   - Compute `X̄ = P \ X`, return 0 if already complete
   - Compute:
     - `lb1`: best pairwise connection through current node
     - `lb2`: best forward and backward combinations
     - Also ensure coverage of all `p ∈ X̄` by checking `dist(v, v̄_p)`
   - Return `max(lb1, lb2, ..., lb_k) + cost`

---

## To Do

- [ ] Implement `AllPaths(G, P)` to precompute shortest path distances
- [ ] Implement lower bound function `lb((v, X), cost, P)` as specified
- [ ] Implement priority queue with `(v, X)` as key and `lb` as comparator
- [ ] Optimize MST construction and merging of partial solutions
- [ ] Ensure correctness of pruning thresholds and merging logic

---

## Notes for Codex

- Priority queue `Q` must support custom comparator on `lb`
- State format: `(v, X)` with associated `cost` and `lb`
- Use dictionaries for `D[(v, X)] = cost` and `Q.lb((v, X))`
- Make sure `lb` is computed **dynamically** based on `X`, `P`, and current `cost`
- For distances: assume `dist(u, v)` is precomputed and available via `AllPaths`

