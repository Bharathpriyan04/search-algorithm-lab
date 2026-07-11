"""
Ex. No. 3 | Implementation of Kruskal's and Prim's Algorithms
             for Minimum Spanning Tree
CS5303 - DAA Lab

This version reads the graph (number of vertices, edges and weights)
from the user at runtime instead of using a hard-coded graph.
"""

import heapq


# --- Union-Find for Kruskal ---
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal(n, edges):
    """edges: list of (weight, u, v)"""
    edges = sorted(edges)  # O(E log E)
    uf = UnionFind(n)
    mst = []
    cost = 0
    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            if len(mst) == n - 1:
                break
    return mst, cost


def prim(n, adj, start=0):
    """adj: adjacency list {u: [(v, w), ...]}"""
    INF = float('inf')
    key = [INF] * n
    parent = [-1] * n
    inMST = [False] * n
    key[start] = 0
    pq = [(0, start)]
    mst = []
    cost = 0
    while pq:
        w, u = heapq.heappop(pq)
        if inMST[u]:
            continue
        inMST[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w
        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))
    return mst, cost


def read_graph_from_user():
    """Prompts the user for the number of vertices/edges and builds
    the edge list and adjacency list from their input."""
    print("=== Enter Graph Details ===")
    n = int(input("Enter number of vertices: ").strip())
    e = int(input("Enter number of edges: ").strip())

    print(f"Enter each edge as: u v weight  (vertices are 0 to {n - 1})")
    edges = []
    adj = {}
    for i in range(e):
        while True:
            try:
                u, v, w = input(f"  Edge {i + 1}: ").split()
                u, v, w = int(u), int(v), int(w)
                break
            except ValueError:
                print("  Invalid input. Please enter as: u v weight (e.g. 0 1 7)")

        edges.append((w, u, v))
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))

    start = input(f"Enter start vertex for Prim's algorithm (default 0): ").strip()
    start = int(start) if start else 0

    return n, edges, adj, start


def main():
    n, edges, adj, start = read_graph_from_user()

    k_mst, k_cost = kruskal(n, edges[:])
    p_mst, p_cost = prim(n, adj, start)

    print("\n=== Kruskal's MST ===")
    for u, v, w in k_mst:
        print(f' Edge ({u} - {v}) Weight: {w}')
    print(f' Total MST Cost: {k_cost}')

    print("\n=== Prim's MST ===")
    for u, v, w in p_mst:
        print(f' Edge ({u} - {v}) Weight: {w}')
    print(f' Total MST Cost: {p_cost}')


if __name__ == "__main__":
    main()
