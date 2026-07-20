"""
Matrix Chain Multiplication using Dynamic Programming
------------------------------------------------------
Given a chain of matrices A1, A2, ..., An where matrix i has
dimensions dims[i-1] x dims[i], find the most efficient way
(minimum number of scalar multiplications) to multiply them.

Time complexity:  O(n^3)
Space complexity: O(n^2)
"""


def matrix_chain_order(dims):
    """
    dims: list of dimensions, matrix i has dims[i-1] x dims[i]
    Returns:
        m: m[i][j] = minimum multiplications for matrices i..j
        s: s[i][j] = optimal split point k for matrices i..j
    """
    n = len(dims) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # l is the chain length
    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    return m, s


def print_optimal_parens(s, i, j):
    if i == j:
        return f'A{i}'
    k = s[i][j]
    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)
    return f'({left} x {right})'


def format_dp_table(m, n):
    """Returns the DP cost table m[i][j] as a formatted string."""
    lines = []
    lines.append('DP Cost Table m[i][j]:')
    header = f'{"":>6}'
    for j in range(1, n + 1):
        header += f'A{j:>8}'
    lines.append(header)

    for i in range(1, n + 1):
        row = f'A{i:<5}'
        for j in range(1, n + 1):
            if j < i:
                row += f'{"---":>9}'
            else:
                row += f'{m[i][j]:>9}'
        lines.append(row)
    return '\n'.join(lines)


def solve(dims):
    """
    High level helper: given a dims list, returns a dict with
    the minimum cost, optimal parenthesization, and formatted table.
    """
    n = len(dims) - 1
    if n < 1:
        raise ValueError('Need at least one matrix (2 dimensions).')

    m, s = matrix_chain_order(dims)

    matrices = [f'A{i + 1}: {dims[i]} x {dims[i + 1]}' for i in range(n)]

    result = {
        'n': n,
        'dims': dims,
        'matrices': matrices,
        'min_multiplications': m[1][n] if n > 1 else 0,
        'optimal_parenthesization': print_optimal_parens(s, 1, n) if n > 1 else 'A1',
        'dp_table': format_dp_table(m, n) if n > 1 else None,
        'm': m,
        's': s,
    }
    return result


def _read_dims_from_user():
    """Prompt the user for matrix dimensions on the command line."""
    print('Matrix Chain Multiplication (Dynamic Programming)')
    print('----------------------------------------------------')
    print('Enter the dimensions as a single comma-separated list.')
    print('Example: for A1(10x30), A2(30x5), A3(5x60), A4(60x10)')
    print('enter: 10,30,5,60,10\n')

    while True:
        raw = input('Dimensions: ').strip()
        try:
            dims = [int(x.strip()) for x in raw.split(',') if x.strip() != '']
            if len(dims) < 2:
                print('Please enter at least two numbers.\n')
                continue
            return dims
        except ValueError:
            print('Invalid input. Please enter integers separated by commas.\n')


def main():
    dims = _read_dims_from_user()
    result = solve(dims)

    print('\nMatrix Dimensions:')
    for line in result['matrices']:
        print(f'  {line}')

    print(f'\nMinimum scalar multiplications: {result["min_multiplications"]}')
    print(f'Optimal parenthesization: {result["optimal_parenthesization"]}')

    if result['dp_table']:
        print('\n' + result['dp_table'])


if __name__ == '__main__':
    main()
