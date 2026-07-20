"""
Travelling Salesman Problem (TSP)
----------------------------------
Given a cost matrix between N cities, find the minimum-cost tour that
starts at city 0, visits every other city exactly once, and returns
to city 0.

Includes:
  - reduce_matrix(): row/column reduction cost, a building block used
    in Branch & Bound style TSP solvers.
  - tsp_brute_force(): exact solution by trying every permutation
    (only practical for small N, since it is O((n-1)!)).
"""

from itertools import permutations

INF = float('inf')


def reduce_matrix(mat):
    """Reduce a cost matrix and return (reduced_matrix, reduction_cost)."""
    m = [row[:] for row in mat]
    n = len(m)
    cost = 0

    # Row reduction
    for i in range(n):
        row_min = min(m[i])
        if row_min and row_min != INF:
            cost += row_min
            m[i] = [x - row_min if x != INF else INF for x in m[i]]

    # Column reduction
    for j in range(n):
        col_min = min(m[i][j] for i in range(n))
        if col_min and col_min != INF:
            cost += col_min
            for i in range(n):
                if m[i][j] != INF:
                    m[i][j] -= col_min

    return m, cost


def tsp_brute_force(cost, n):
    """Exact TSP solution via brute-force permutation search."""
    cities = list(range(1, n))
    best_cost = INF
    best_path = None

    for perm in permutations(cities):
        path = [0] + list(perm) + [0]
        c = sum(cost[path[i]][path[i + 1]] for i in range(n))
        if c < best_cost:
            best_cost = c
            best_path = path

    return best_path, best_cost


def solve(cost, city_names=None):
    """
    High level helper for the web/CLI front ends.
    cost: n x n matrix (INF on the diagonal, or wherever there's no edge)
    city_names: optional list of labels, defaults to A, B, C, ...
    """
    n = len(cost)
    if n < 2:
        raise ValueError('Need at least 2 cities.')
    for row in cost:
        if len(row) != n:
            raise ValueError('Cost matrix must be square (n x n).')

    if city_names is None:
        city_names = [chr(ord('A') + i) for i in range(n)]

    best_path, best_cost = tsp_brute_force(cost, n)

    def _clean(x):
        return int(x) if x != INF and float(x).is_integer() else x

    steps = []
    for i in range(n):
        u, v = best_path[i], best_path[i + 1]
        steps.append({
            'from': city_names[u],
            'to': city_names[v],
            'cost': _clean(cost[u][v]),
        })

    display_matrix = []
    for row in cost:
        display_matrix.append([
            'INF' if x == INF else (int(x) if float(x).is_integer() else x)
            for x in row
        ])

    return {
        'n': n,
        'cities': city_names,
        'cost_matrix': cost,
        'display_matrix': display_matrix,
        'optimal_tour': [city_names[i] for i in best_path],
        'min_cost': _clean(best_cost),
        'steps': steps,
    }


def _read_matrix_from_user():
    print('Travelling Salesman Problem — Brute Force Solver')
    print('---------------------------------------------------')
    print('Enter the number of cities, then the cost matrix row by row.')
    print('Use "INF" for no direct edge (e.g. the diagonal).\n')

    while True:
        try:
            n = int(input('Number of cities: ').strip())
            if n < 2:
                print('Please enter at least 2 cities.\n')
                continue
            break
        except ValueError:
            print('Invalid input. Please enter an integer.\n')

    print(f'\nEnter each row as {n} comma-separated values.')
    print('Example row for 5 cities: INF,10,8,9,7\n')

    matrix = []
    for i in range(n):
        while True:
            raw = input(f'Row {i + 1}: ').strip()
            parts = [p.strip() for p in raw.split(',') if p.strip() != '']
            if len(parts) != n:
                print(f'Expected {n} values, got {len(parts)}. Try again.')
                continue
            try:
                row = [INF if p.upper() == 'INF' else float(p) for p in parts]
                matrix.append(row)
                break
            except ValueError:
                print('Invalid number in row. Try again.')

    return matrix, n


def main():
    matrix, n = _read_matrix_from_user()
    city_names = [chr(ord('A') + i) for i in range(n)]
    result = solve(matrix, city_names)

    print(f'\n{n}-City TSP - Cost Matrix:')
    header = '    ' + ' '.join(f'{c:>5}' for c in city_names)
    print(header)
    for i, row in enumerate(matrix):
        r = ['INF' if x == INF else str(int(x) if x == int(x) else x) for x in row]
        print(f'{city_names[i]:>4}', ' '.join(f'{v:>5}' for v in r))

    print(f'\nOptimal Tour: {" -> ".join(result["optimal_tour"])}')
    print(f'Minimum Cost: {result["min_cost"]}')

    print('\nPath verification:')
    for step in result['steps']:
        print(f'  {step["from"]} -> {step["to"]}: cost = {step["cost"]}')


if __name__ == '__main__':
    main()
