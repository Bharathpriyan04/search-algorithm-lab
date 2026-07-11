"""
Ex. No. 3 | Implementation of Kruskal's and Prim's Algorithms
             for Minimum Spanning Tree - Web Version
CS5303 - DAA Lab

A small Flask web app so this lab experiment can be deployed on Render
(or any similar host) and run in a browser instead of a terminal.
"""

import heapq
from flask import Flask, render_template_string, request

app = Flask(__name__)


# --- Union-Find for Kruskal ---
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
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
    edges = sorted(edges)
    uf = UnionFind(n)
    mst, cost = [], 0
    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            if len(mst) == n - 1:
                break
    return mst, cost


def prim(n, adj, start=0):
    INF = float('inf')
    key = [INF] * n
    parent = [-1] * n
    inMST = [False] * n
    key[start] = 0
    pq = [(0, start)]
    mst, cost = [], 0
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


PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Kruskal's &amp; Prim's MST - CS5303 DAA Lab</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root { color-scheme: dark; }
  body {
    font-family: -apple-system, Segoe UI, Roboto, sans-serif;
    background: #0f1117; color: #e6e6e6; margin: 0; padding: 2rem 1rem;
  }
  .wrap { max-width: 720px; margin: 0 auto; }
  h1 { font-size: 1.4rem; margin-bottom: .2rem; }
  .sub { color: #9aa0ac; margin-bottom: 1.5rem; font-size: .9rem; }
  form {
    background: #171a23; border: 1px solid #2a2e3a; border-radius: 10px;
    padding: 1.25rem; margin-bottom: 1.5rem;
  }
  label { display: block; margin: .6rem 0 .25rem; font-size: .9rem; color: #c7ccd6; }
  input[type=number], textarea {
    width: 100%; box-sizing: border-box; background: #0f1117; color: #e6e6e6;
    border: 1px solid #2a2e3a; border-radius: 6px; padding: .55rem .7rem; font-size: .95rem;
  }
  textarea { min-height: 140px; font-family: ui-monospace, monospace; resize: vertical; }
  small { color: #7d8390; }
  button {
    margin-top: 1rem; background: #4f7cff; color: white; border: none;
    padding: .6rem 1.1rem; border-radius: 6px; font-size: .95rem; cursor: pointer;
  }
  button:hover { background: #3d68e6; }
  .error { background: #3a1c22; border: 1px solid #7a2b36; color: #ff9aa6;
    padding: .8rem 1rem; border-radius: 8px; margin-bottom: 1.5rem; }
  .result { background: #171a23; border: 1px solid #2a2e3a; border-radius: 10px;
    padding: 1.25rem; margin-bottom: 1.25rem; }
  .result h2 { margin-top: 0; font-size: 1.1rem; color: #8fb3ff; }
  table { width: 100%; border-collapse: collapse; margin-top: .5rem; }
  th, td { text-align: left; padding: .35rem .5rem; border-bottom: 1px solid #2a2e3a; font-size: .9rem; }
  .cost { margin-top: .6rem; font-weight: 600; color: #7ee0a4; }
  footer { color: #666c78; font-size: .8rem; margin-top: 2rem; text-align: center; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Kruskal's &amp; Prim's MST</h1>
  <div class="sub">CS5303 - DAA Lab, Ex. No. 3</div>

  {% if error %}
    <div class="error">{{ error }}</div>
  {% endif %}

  <form method="POST">
    <label for="n">Number of vertices</label>
    <input type="number" id="n" name="n" min="1" value="{{ n or 7 }}" required>

    <label for="edges">Edges (one per line: <code>u v weight</code>)</label>
    <textarea id="edges" name="edges" placeholder="0 1 7&#10;0 3 5&#10;1 2 8">{{ edges_text or default_edges }}</textarea>
    <small>Vertices are numbered 0 to n-1.</small>

    <label for="start">Start vertex for Prim's algorithm</label>
    <input type="number" id="start" name="start" min="0" value="{{ start or 0 }}">

    <button type="submit">Compute MST</button>
  </form>

  {% if k_mst is not none %}
  <div class="result">
    <h2>Kruskal's MST</h2>
    <table>
      <tr><th>Edge</th><th>Weight</th></tr>
      {% for u, v, w in k_mst %}
      <tr><td>{{ u }} - {{ v }}</td><td>{{ w }}</td></tr>
      {% endfor %}
    </table>
    <div class="cost">Total MST Cost: {{ k_cost }}</div>
  </div>

  <div class="result">
    <h2>Prim's MST</h2>
    <table>
      <tr><th>Edge</th><th>Weight</th></tr>
      {% for u, v, w in p_mst %}
      <tr><td>{{ u }} - {{ v }}</td><td>{{ w }}</td></tr>
      {% endfor %}
    </table>
    <div class="cost">Total MST Cost: {{ p_cost }}</div>
  </div>
  {% endif %}

  <footer>Deployed with Flask + Render</footer>
</div>
</body>
</html>
"""

DEFAULT_EDGES = """0 1 7
0 3 5
1 2 8
1 3 9
1 4 7
2 4 5
3 4 15
3 5 6
4 5 8
4 6 9
5 6 11"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template_string(PAGE, n=7, edges_text=None, default_edges=DEFAULT_EDGES,
                                       start=0, k_mst=None, p_mst=None, error=None)

    n_raw = request.form.get("n", "").strip()
    edges_text = request.form.get("edges", "").strip()
    start_raw = request.form.get("start", "0").strip()

    try:
        n = int(n_raw)
        start = int(start_raw) if start_raw else 0
        if n <= 0:
            raise ValueError("Number of vertices must be positive.")
        if not (0 <= start < n):
            raise ValueError("Start vertex must be between 0 and n-1.")

        edges = []
        adj = {}
        for line in edges_text.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(f"Invalid edge line: '{line}'. Use 'u v weight'.")
            u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
            if not (0 <= u < n and 0 <= v < n):
                raise ValueError(f"Edge '{line}' references a vertex outside 0..{n-1}.")
            edges.append((w, u, v))
            adj.setdefault(u, []).append((v, w))
            adj.setdefault(v, []).append((u, w))

        if not edges:
            raise ValueError("Please enter at least one edge.")

        k_mst, k_cost = kruskal(n, edges[:])
        p_mst, p_cost = prim(n, adj, start)

        return render_template_string(PAGE, n=n, edges_text=edges_text, default_edges=DEFAULT_EDGES,
                                       start=start, k_mst=k_mst, k_cost=k_cost,
                                       p_mst=p_mst, p_cost=p_cost, error=None)

    except ValueError as e:
        return render_template_string(PAGE, n=n_raw, edges_text=edges_text, default_edges=DEFAULT_EDGES,
                                       start=start_raw, k_mst=None, p_mst=None, error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
