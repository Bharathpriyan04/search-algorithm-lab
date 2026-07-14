import os
from flask import Flask, render_template, request

from min_max import run_min_max

app = Flask(__name__)


def parse_numbers(raw_text):
    """Turn user input text into a list of ints. Raises ValueError on bad input."""
    if not raw_text or not raw_text.strip():
        raise ValueError("Please enter at least one number.")
    cleaned = raw_text.replace(",", " ")
    numbers = [int(x) for x in cleaned.split()]
    if not numbers:
        raise ValueError("Please enter at least one number.")
    return numbers


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    raw_input_value = ""

    if request.method == "POST":
        raw_input_value = request.form.get("numbers", "")
        try:
            arr = parse_numbers(raw_input_value)
            result = run_min_max(arr)
        except ValueError as e:
            error = str(e)

    return render_template(
        "index.html",
        result=result,
        error=error,
        raw_input_value=raw_input_value,
    )


if __name__ == "__main__":
    # Render provides the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
