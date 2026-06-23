from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)


def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1
        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons
        pos = low + int(((target - arr[low]) * (high - low)) / (arr[high] - arr[low]))
        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1, comparisons


def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons


def performance_analysis():
    sizes = [1000, 5000, 10000, 50000, 100000]
    results = []
    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]

        start = time.perf_counter()
        for _ in range(100):
            idx_is, comp_is = interpolation_search(arr, target)
        is_time = (time.perf_counter() - start) / 100 * 1000

        start = time.perf_counter()
        for _ in range(100):
            idx_bs, comp_bs = binary_search(arr, target)
        bs_time = (time.perf_counter() - start) / 100 * 1000

        results.append({
            "size": size,
            "is_time": round(is_time, 4),
            "bs_time": round(bs_time, 4),
            "is_comparisons": comp_is,
            "bs_comparisons": comp_bs,
        })
    return results


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    raw = data.get("array", "")
    target_raw = data.get("target", "")

    try:
        arr = [int(x.strip()) for x in raw.split(",") if x.strip()]
        target = int(target_raw)
    except ValueError:
        return jsonify({"error": "Invalid input. Please enter integers only."}), 400

    if not arr:
        return jsonify({"error": "Array cannot be empty."}), 400

    arr = sorted(arr)

    idx_is, comp_is = interpolation_search(arr, target)
    idx_bs, comp_bs = binary_search(arr, target)

    return jsonify({
        "array": arr,
        "target": target,
        "interpolation": {"index": idx_is, "comparisons": comp_is},
        "binary": {"index": idx_bs, "comparisons": comp_bs},
    })


@app.route("/performance", methods=["POST"])
def performance():
    results = performance_analysis()
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
