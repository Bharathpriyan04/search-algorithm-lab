# Ex. No. 3 — Kruskal's and Prim's Algorithms for Minimum Spanning Tree

**Course:** CS5303 – Design and Analysis of Algorithms Lab

## Aim
To implement Kruskal's and Prim's algorithms to find the Minimum Spanning Tree (MST) of a weighted, undirected graph.

## Description
- **Kruskal's Algorithm:** Sorts all edges by weight and greedily adds the smallest edge that doesn't form a cycle, using a Union-Find (Disjoint Set Union) structure with path compression and union by rank. Time complexity: O(E log E).
- **Prim's Algorithm:** Grows the MST one vertex at a time from a starting node, always picking the cheapest edge that connects a new vertex to the tree, using a min-heap (priority queue). Time complexity: O(E log V).

## Files
- `mst.py` — Python implementation of both algorithms with user input for the graph (vertices, edges, and weights).

## How to Run
```bash
python3 mst.py
```
You will be prompted to enter:
1. Number of vertices
2. Number of edges
3. Each edge in the format: `u v weight` (vertices are 0-indexed)

## Sample Input
```
Enter number of vertices: 7
Enter number of edges: 11
Edge 1: 0 1 7
Edge 2: 0 3 5
Edge 3: 1 2 8
Edge 4: 1 3 9
Edge 5: 1 4 7
Edge 6: 2 4 5
Edge 7: 3 4 15
Edge 8: 3 5 6
Edge 9: 4 5 8
Edge 10: 4 6 9
Edge 11: 5 6 11
```

## Sample Output
```
=== Kruskal's MST ===
  Edge (0 - 3) Weight: 5
  Edge (2 - 4) Weight: 5
  Edge (3 - 5) Weight: 6
  Edge (0 - 1) Weight: 7
  Edge (1 - 4) Weight: 7
  Edge (4 - 6) Weight: 9
  Total MST Cost: 39

=== Prim's MST ===
  Edge (0 - 3) Weight: 5
  Edge (3 - 5) Weight: 6
  Edge (0 - 1) Weight: 7
  Edge (1 - 4) Weight: 7
  Edge (4 - 2) Weight: 5
  Edge (4 - 6) Weight: 9
  Total MST Cost: 39
```

## Result
Both algorithms successfully computed the Minimum Spanning Tree with a total cost of 39, confirming that Kruskal's and Prim's algorithms yield the same MST weight regardless of the different edge selection order.
