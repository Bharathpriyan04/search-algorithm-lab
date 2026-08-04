from flask import Flask, render_template, request

app = Flask(__name__)


# ---------- Bin packing algorithms ----------

def first_fit(items, capacity=1.0):
    bins = []          # remaining space in each bin
    bin_contents = []
    for item in items:
        placed = False
        for i, space in enumerate(bins):
            if space >= item:
                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break
        if not placed:
            bins.append(capacity - item)
            bin_contents.append([item])
    return bin_contents


def first_fit_decreasing(items, capacity=1.0):
    return first_fit(sorted(items, reverse=True), capacity)


def best_fit_decreasing(items, capacity=1.0):
    sorted_items = sorted(items, reverse=True)
    bins = []
    bin_contents = []
    for item in sorted_items:
        best_idx = -1
        best_space = float('inf')
        for i, space in enumerate(bins):
            if space >= item and space - item < best_space:
                best_space = space - item
                best_idx = i
        if best_idx >= 0:
            bins[best_idx] -= item
            bin_contents[best_idx].append(item)
        else:
            bins.append(capacity - item)
            bin_contents.append([item])
    return bin_contents


def summarize(bin_contents, capacity):
    """Turn a list of bins (each a list of item sizes) into display-ready rows."""
    rows = []
    for i, b in enumerate(bin_contents, 1):
        used = sum(b)
        pct = used / capacity if capacity else 0
        rows.append({
            'index': i,
            'items': [round(x, 3) for x in b],
            'used': round(used, 3),
            'capacity': capacity,
            'percent': round(pct * 100, 1),
        })
    return rows


# ---------- Routes ----------

@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'items_raw': '0.5, 0.7, 0.3, 0.9, 0.2, 0.6, 0.8, 0.4, 0.1, 0.5',
        'capacity': 1.0,
        'error': None,
        'results': None,
    }

    if request.method == 'POST':
        items_raw = request.form.get('items', '').strip()
        capacity_raw = request.form.get('capacity', '1.0').strip()
        context['items_raw'] = items_raw
        context['capacity'] = capacity_raw

        try:
            capacity = float(capacity_raw)
            if capacity <= 0:
                raise ValueError('Capacity must be positive.')

            items = [float(x.strip()) for x in items_raw.split(',') if x.strip() != '']
            if not items:
                raise ValueError('Enter at least one item size.')
            if any(x <= 0 for x in items):
                raise ValueError('Item sizes must be positive numbers.')
            if any(x > capacity for x in items):
                raise ValueError('An item is larger than the bin capacity.')

            lower_bound = -(-sum(items) // capacity)  # ceiling division

            ff_bins = first_fit(items, capacity)
            ffd_bins = first_fit_decreasing(items, capacity)
            bfd_bins = best_fit_decreasing(items, capacity)

            context['results'] = {
                'item_list': items,
                'capacity': capacity,
                'total': round(sum(items), 3),
                'lower_bound': int(lower_bound),
                'algorithms': [
                    {
                        'name': 'First Fit (FF)',
                        'bin_count': len(ff_bins),
                        'bins': summarize(ff_bins, capacity),
                    },
                    {
                        'name': 'First Fit Decreasing (FFD)',
                        'bin_count': len(ffd_bins),
                        'bins': summarize(ffd_bins, capacity),
                    },
                    {
                        'name': 'Best Fit Decreasing (BFD)',
                        'bin_count': len(bfd_bins),
                        'bins': summarize(bfd_bins, capacity),
                    },
                ],
            }
        except ValueError as e:
            context['error'] = str(e)

    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
