"""
Flask web app for the Travelling Salesman Problem (brute force).
Deployable on Render as a web service.
"""
import os
from flask import Flask, render_template, request

from tsp import solve, INF

app = Flask(__name__)

MAX_N = 9  # brute force is O((n-1)!) -> keep this small on a free dyno

DEFAULT_MATRIX_TEXT = (
    "INF,10,8,9,7\n"
    "10,INF,10,5,6\n"
    "8,10,INF,8,9\n"
    "9,5,8,INF,6\n"
    "7,6,9,6,INF"
)


def parse_matrix(text):
    """Parse a textarea of comma-separated rows into a cost matrix."""
    rows = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not rows:
        raise ValueError('Please enter a cost matrix.')

    matrix = []
    for row_text in rows:
        parts = [p.strip() for p in row_text.split(',') if p.strip() != '']
        parsed_row = []
        for p in parts:
            if p.upper() == 'INF':
                parsed_row.append(INF)
            else:
                parsed_row.append(float(p))
        matrix.append(parsed_row)

    n = len(matrix)
    if n < 2:
        raise ValueError('Need at least 2 cities (2 rows).')
    for row in matrix:
        if len(row) != n:
            raise ValueError(
                f'Matrix must be square: found {n} rows but a row with {len(row)} values.'
            )
    if n > MAX_N:
        raise ValueError(f'For performance, this demo caps N at {MAX_N} cities.')

    return matrix, n


@app.route('/', methods=['GET', 'POST'])
def index():
    matrix_text = DEFAULT_MATRIX_TEXT
    result = None
    error = None

    if request.method == 'POST':
        matrix_text = request.form.get('matrix', '').strip()
        try:
            matrix, n = parse_matrix(matrix_text)
            city_names = [chr(ord('A') + i) for i in range(n)]
            result = solve(matrix, city_names)
        except ValueError as e:
            error = str(e)
        except Exception:
            error = 'Could not parse the matrix. Check the format and try again.'

    return render_template(
        'index.html',
        matrix_text=matrix_text,
        result=result,
        error=error,
        max_n=MAX_N,
    )


@app.route('/healthz')
def health_check():
    return {'status': 'ok'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
