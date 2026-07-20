"""
N-Queens Problem — solved using Backtracking
----------------------------------------------
Place N queens on an N x N chessboard so that no two queens attack
each other (no shared row, column, or diagonal).

board[row] = col  ->  the column where the queen in that row is placed.
"""


def is_safe(board, row, col):
    """Check whether a queen can be placed at (row, col) safely."""
    for prev_row in range(row):
        placed = board[prev_row]
        if placed == col:  # Same column
            return False
        if abs(prev_row - row) == abs(placed - col):  # Same diagonal
            return False
    return True


def solve_n_queens(n):
    """
    Returns:
        solutions: list of boards (each board is a list where
                   board[row] = col of the queen in that row)
        backtrack_count: number of backtracking steps taken
    """
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1  # Undo
            else:
                backtrack_count[0] += 1

    backtrack(0)
    return solutions, backtrack_count[0]


def format_board(solution, n):
    """Returns a text rendering of a single board solution."""
    lines = []
    border = ' +' + '---+' * n
    lines.append(border)
    for row in range(n):
        line = ' |'
        for col in range(n):
            line += ' Q |' if solution[row] == col else ' . |'
        lines.append(line)
        lines.append(border)
    return '\n'.join(lines)


def solve(n, max_boards_to_render=20):
    """
    High level helper for the web/CLI front ends.
    Returns a dict with solution count, backtrack count, and
    formatted boards (capped at max_boards_to_render to avoid
    rendering huge output for large n).
    """
    if n < 1:
        raise ValueError('N must be a positive integer.')

    solutions, backtracks = solve_n_queens(n)

    boards = []
    for sol in solutions[:max_boards_to_render]:
        boards.append(format_board(sol, n))

    return {
        'n': n,
        'solution_count': len(solutions),
        'backtracks': backtracks,
        'solutions': solutions,
        'boards': boards,
        'boards_truncated': len(solutions) > max_boards_to_render,
        'boards_shown': len(boards),
    }


def _read_n_from_user():
    print('N-Queens Solver (Backtracking)')
    print('-------------------------------')
    while True:
        raw = input('Enter board size N: ').strip()
        try:
            n = int(raw)
            if n < 1:
                print('Please enter a positive integer.\n')
                continue
            return n
        except ValueError:
            print('Invalid input. Please enter an integer.\n')


def main():
    n = _read_n_from_user()
    result = solve(n, max_boards_to_render=20)

    print(f'\nN={result["n"]}: {result["solution_count"]} solutions, '
          f'{result["backtracks"]} backtracks')

    if result['solutions']:
        print(f'\nShowing {result["boards_shown"]} of {result["solution_count"]} solution(s):')
        for i, board_text in enumerate(result['boards'], 1):
            sol = result['solutions'][i - 1]
            print(f'\nSolution {i}: {sol}')
            print(board_text)
        if result['boards_truncated']:
            print(f'\n... {result["solution_count"] - result["boards_shown"]} more solution(s) not shown.')
    else:
        print('No solutions exist for this N.')


if __name__ == '__main__':
    main()
