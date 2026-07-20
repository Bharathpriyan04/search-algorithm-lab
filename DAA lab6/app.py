"""
Flask web app for Matrix Chain Multiplication (DP).
Deployable on Render as a web service.
"""
import os
from flask import Flask, render_template, request

from matrix_chain import solve

app = Flask(__name__)

DEFAULT_DIMS = "10,30,5,60,10"


@app.route('/', methods=['GET', 'POST'])
def index():
    dims_input = DEFAULT_DIMS
    result = None
    error = None

    if request.method == 'POST':
        dims_input = request.form.get('dims', '').strip()
        try:
            dims = [int(x.strip()) for x in dims_input.split(',') if x.strip() != '']
            if len(dims) < 2:
                error = 'Please enter at least two dimensions (e.g. 10,30,5).'
            else:
                result = solve(dims)
        except ValueError:
            error = 'Invalid input. Please enter integers separated by commas.'

    return render_template(
        'index.html',
        dims_input=dims_input,
        result=result,
        error=error,
    )


@app.route('/healthz')
def health_check():
    return {'status': 'ok'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
