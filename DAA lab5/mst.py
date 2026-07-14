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


def get_graph_from_user():
    """Reads number of vertices and edges from the user."""
    print("=== Minimum Spanning Tree (Kruskal's & Prim's) ===")
    n = int(input("Enter number of vertices: ").strip())
    e = int(input("Enter number of edges: ").strip())

    print(f"\nEnter each edge as: u v weight  (vertices 0 to {n - 1})")
    edges = []
    for i in range(e):
        while True:
            try:
                parts = input(f"Edge {i + 1}: ").strip().split()
                u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
                if not (0 <= u < n and 0 <= v < n):
                    print(f"  Vertices must be between 0 and {n - 1}. Try again.")
                    continue
                edges.append((w, u, v))
                break
            except (ValueError, IndexError):
                print("  Invalid input. Format must be: u v weight (e.g. 0 1 7). Try again.")

    return n, edges


def build_adjacency_list(edges):
    adj = {}
    for w, u, v in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    return adj


def main():
    n, edges = get_graph_from_user()
    adj = build_adjacency_list(edges)

    k_mst, k_cost = kruskal(n, edges[:])
    p_mst, p_cost = prim(n, adj)

    print("\n=== Kruskal's MST ===")
    for u, v, w in k_mst:
        print(f"  Edge ({u} - {v}) Weight: {w}")
    print(f"  Total MST Cost: {k_cost}")

    print("\n=== Prim's MST ===")
    for u, v, w in p_mst:
        print(f"  Edge ({u} - {v}) Weight: {w}")
    print(f"  Total MST Cost: {p_cost}")


if __name__ == "__main__":
    main()
