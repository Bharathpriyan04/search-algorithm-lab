# Lab 3 – Kruskal's and Prim's Algorithms for Minimum Spanning Tree

**CS5303 – Design and Analysis of Algorithms Lab**

## Description
This program implements both **Kruskal's** and **Prim's** algorithms to find the
Minimum Spanning Tree (MST) of a weighted, undirected, connected graph.
Unlike a hard-coded version, this script takes the **graph as input from the
user** at runtime (number of vertices, number of edges, and each edge's
endpoints + weight).

## Files
- `mst_kruskal_prim.py` – main program (user-input driven)

## How to Run
```bash
python3 mst_kruskal_prim.py
```

You will be prompted for:
1. Number of vertices
2. Number of edges
3. Each edge in the format: `u v weight` (e.g. `0 1 7`)
4. (Optional) start vertex for Prim's algorithm — defaults to `0`

### Example Input
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
Enter start vertex for Prim's algorithm (default 0): 0
```

### Example Output
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

## Algorithms
- **Kruskal's Algorithm** – sorts all edges by weight and greedily adds an
  edge to the MST if it does not form a cycle, using a Union-Find
  (Disjoint Set) data structure with path compression and union by rank.
  Time Complexity: `O(E log E)`
- **Prim's Algorithm** – grows the MST from a start vertex, always adding
  the cheapest edge connecting a tree vertex to a non-tree vertex, using a
  min-heap (priority queue). Time Complexity: `O(E log V)`
