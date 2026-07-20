"""
Flask web app for the N-Queens problem (Backtracking).
Deployable on Render as a web service.
"""
import os
from flask import Flask, render_template, request

from nqueens import solve

app = Flask(__name__)

DEFAULT_N = "8"
MAX_N = 12  # guard rail so the free web dyno doesn't hang on huge n
MAX_BOARDS = 20


@app.route('/', methods=['GET', 'POST'])
def index():
    n_input = DEFAULT_N
    result = None
    error = None

    if request.method == 'POST':
        n_input = request.form.get('n', '').strip()
        try:
            n = int(n_input)
            if n < 1:
                error = 'Please enter a positive integer.'
            elif n > MAX_N:
                error = f'For performance, N is capped at {MAX_N} on this demo.'
            else:
                result = solve(n, max_boards_to_render=MAX_BOARDS)
        except ValueError:
            error = 'Invalid input. Please enter a whole number.'

    return render_template(
        'index.html',
        n_input=n_input,
        result=result,
        error=error,
    )


@app.route('/healthz')
def health_check():
    return {'status': 'ok'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
