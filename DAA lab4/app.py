"""
Ex. No. 4 | Implementation of Dijkstra's Algorithm for
             Single Source Shortest Path - Web Version
CS5303 - DAA Lab

A small Flask web app so this lab experiment can be deployed on Render
(or any similar host) and run in a browser instead of a terminal.
"""

import heapq
from flask import Flask, render_template_string, request

app = Flask(__name__)


def dijkstra(graph, source):
    """
    Dijkstra's Algorithm using Min-Heap
    Time: O((V + E) log V), Space: O(V)
    graph: dict {u: [(v, weight), ...]}, 0-indexed
    """
    n = len(graph)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[source] = 0
    pq = [(0, source)]
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def reconstruct_path(prev, source, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    if path[0] == source:
        return path
    return []


PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Dijkstra's Shortest Path - CS5303 DAA Lab</title>
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
  .checkbox-row { display: flex; align-items: center; gap: .5rem; margin-top: .8rem; }
  .checkbox-row input { width: auto; }
  .checkbox-row label { margin: 0; }
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
  td.inf { color: #ff9aa6; }
  footer { color: #666c78; font-size: .8rem; margin-top: 2rem; text-align: center; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Dijkstra's Shortest Path</h1>
  <div class="sub">CS5303 - DAA Lab, Ex. No. 4</div>

  {% if error %}
    <div class="error">{{ error }}</div>
  {% endif %}

  <form method="POST">
    <label for="n">Number of vertices</label>
    <input type="number" id="n" name="n" min="1" value="{{ n or 6 }}" required>

    <label for="edges">Edges (one per line: <code>u v weight</code>)</label>
    <textarea id="edges" name="edges" placeholder="0 1 4&#10;0 2 1&#10;1 3 1">{{ edges_text or default_edges }}</textarea>
    <small>Vertices are numbered 0 to n-1.</small>

    <div class="checkbox-row">
      <input type="checkbox" id="directed" name="directed" {% if directed %}checked{% endif %}>
      <label for="directed">Directed graph</label>
    </div>

    <label for="source">Source vertex</label>
    <input type="number" id="source" name="src" min="0" value="{{ src or 0 }}">

    <button type="submit">Compute Shortest Paths</button>
  </form>

  {% if dist is not none %}
  <div class="result">
    <h2>Shortest paths from vertex {{ src }}</h2>
    <table>
      <tr><th>Vertex</th><th>Distance</th><th>Path</th></tr>
      {% for v in range(n) %}
      <tr>
        <td>{{ v }}</td>
        {% if dist[v] == inf %}
          <td class="inf">INF</td>
          <td>No path</td>
        {% else %}
          <td>{{ dist[v] }}</td>
          <td>{{ paths[v] }}</td>
        {% endif %}
      </tr>
      {% endfor %}
    </table>
  </div>
  {% endif %}

  <footer>Deployed with Flask + Render</footer>
</div>
</body>
</html>
"""

DEFAULT_EDGES = """0 1 4
0 2 1
1 3 1
2 1 2
2 3 5
3 4 3
4 5 2"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template_string(PAGE, n=6, edges_text=None, default_edges=DEFAULT_EDGES,
                                       directed=True, src=0, dist=None, paths=None,
                                       inf=float('inf'), error=None)

    n_raw = request.form.get("n", "").strip()
    edges_text = request.form.get("edges", "").strip()
    directed = request.form.get("directed") == "on"
    source_raw = request.form.get("src", "0").strip()

    try:
        n = int(n_raw)
        source = int(source_raw) if source_raw else 0
        if n <= 0:
            raise ValueError("Number of vertices must be positive.")
        if not (0 <= source < n):
            raise ValueError("Source vertex must be between 0 and n-1.")

        graph = {i: [] for i in range(n)}
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
            if w < 0:
                raise ValueError(f"Edge '{line}' has a negative weight; Dijkstra requires non-negative weights.")
            graph[u].append((v, w))
            if not directed:
                graph[v].append((u, w))

        dist, prev = dijkstra(graph, source)
        paths = []
        for v in range(n):
            path = reconstruct_path(prev, source, v)
            paths.append(' -> '.join(map(str, path)) if path else 'No path')

        return render_template_string(PAGE, n=n, edges_text=edges_text, default_edges=DEFAULT_EDGES,
                                       directed=directed, src=source, dist=dist, paths=paths,
                                       inf=float('inf'), error=None)

    except ValueError as e:
        return render_template_string(PAGE, n=n_raw, edges_text=edges_text, default_edges=DEFAULT_EDGES,
                                       directed=directed, src=source_raw, dist=None, paths=None,
                                       inf=float('inf'), error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
