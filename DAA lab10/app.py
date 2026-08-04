import random
import sys
import time

from flask import Flask, render_template, request

sys.setrecursionlimit(20000)

app = Flask(__name__)

# Deterministic (last-element pivot) quicksort on large sorted/reverse arrays
# is O(n^2) and can be slow / hit recursion depth in a web request, so cap N.
MAX_N = 3000


# ---------- Sorting algorithms ----------

def partition(arr, low, high, counters):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        counters['comparisons'] += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def deterministic_quicksort(arr, low, high, counters):
    if low < high:
        pi = partition(arr, low, high, counters)
        deterministic_quicksort(arr, low, pi - 1, counters)
        deterministic_quicksort(arr, pi + 1, high, counters)


def randomized_quicksort(arr, low, high, counters):
    if low < high:
        rand_idx = random.randint(low, high)
        arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
        pi = partition(arr, low, high, counters)
        randomized_quicksort(arr, low, pi - 1, counters)
        randomized_quicksort(arr, pi + 1, high, counters)


def run_test(sort_fn, arr):
    a = arr[:]
    counters = {'comparisons': 0}
    start = time.perf_counter()
    sort_fn(a, 0, len(a) - 1, counters)
    elapsed = (time.perf_counter() - start) * 1000
    return counters['comparisons'], elapsed


def build_test_cases(n):
    random_arr = [random.randint(1, 100000) for _ in range(n)]
    sorted_arr = list(range(n))
    reverse_arr = list(range(n, 0, -1))

    nearly_sorted = list(range(n))
    for _ in range(max(n // 20, 1)):
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        nearly_sorted[i], nearly_sorted[j] = nearly_sorted[j], nearly_sorted[i]

    return {
        'Random': random_arr,
        'Sorted': sorted_arr,
        'Reverse': reverse_arr,
        'Nearly Sorted': nearly_sorted,
    }


# ---------- Routes ----------

@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'n': 500,
        'custom_array': '',
        'error': None,
        'results': None,
        'max_n': MAX_N,
    }

    if request.method == 'POST':
        n_raw = request.form.get('n', '').strip()
        custom_raw = request.form.get('custom_array', '').strip()
        context['n'] = n_raw
        context['custom_array'] = custom_raw

        try:
            test_cases = {}

            if custom_raw:
                custom_arr = [int(x.strip()) for x in custom_raw.split(',') if x.strip() != '']
                if not custom_arr:
                    raise ValueError('Enter at least one number in the custom array.')
                if len(custom_arr) > MAX_N:
                    raise ValueError(f'Custom array is limited to {MAX_N} numbers.')
                test_cases['Custom'] = custom_arr
            else:
                n = int(n_raw)
                if n <= 1:
                    raise ValueError('N must be greater than 1.')
                if n > MAX_N:
                    raise ValueError(f'N is limited to {MAX_N} for this demo (deterministic quicksort is O(n^2) on sorted/reverse input).')
                test_cases = build_test_cases(n)

            rows = []
            for case, arr in test_cases.items():
                d_comps, d_time = run_test(deterministic_quicksort, arr)
                r_comps, r_time = run_test(randomized_quicksort, arr)
                rows.append({
                    'case': case,
                    'size': len(arr),
                    'd_comps': d_comps,
                    'd_time': round(d_time, 3),
                    'r_comps': r_comps,
                    'r_time': round(r_time, 3),
                })

            context['results'] = rows
        except ValueError as e:
            context['error'] = str(e)

    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
