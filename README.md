# GST
# DPBF-k: Top-k Group Steiner Tree Search in Graph Databases

本项目实现了论文《Finding Top-k Min-Cost Connected Trees in Databases》中提出的 DPBF-k 算法，用于在大规模加权图中寻找包含所有关键词组的前 k 个最小代价连通树（Group Steiner Tree）。

---

## 📌 项目目标

- 输入：
  - 加权图 G = (V, E)，每个节点与边带有非负权重；
  - 关键词集合 P = {p₁, p₂, ..., pₗ}，每个关键词 pᵢ 对应一个候选节点组 Vᵢ；
  - 整体目标：从图中找出包含每组至少一个节点、且总代价最小的前 k 棵连通子图（树）。

- 输出：
  - GST-1 到 GST-k：每棵树覆盖所有关键词组、内部连通、总代价最小。

---

## 🧠 算法简介：DPBF-k

DPBF-k（Dynamic Programming with Best-First Search）是一种参数化动态规划算法，适用于关键词数量较小但图规模较大的情形。它通过组合两类递推操作：

- **Tree Grow**：将当前树从根节点向邻接节点扩展；
- **Tree Merge**：在同一根节点下合并两个 disjoint 关键词子集树；

每次从优先队列中取出代价最小的树状态，逐步扩展直到找到覆盖所有关键词的 top-k 棵最优子图。

---

## 🗂️ 模块结构建议

