"""
Ex. No. 5 | Find Min-Max Value by Applying Divide and Conquer Technique
CS5303 - DAA Lab

This version takes the array from USER INPUT instead of random.randint().
It can be run directly (python min_max.py) for a command-line demo,
or imported by app.py for the web version.
"""

comparison_count = 0  # Global counter, reset before every run


def min_max_dc(arr, low, high):
    """Divide and conquer min-max."""
    global comparison_count

    # Base case: single element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        comparison_count += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2
    lmin, lmax = min_max_dc(arr, low, mid)
    rmin, rmax = min_max_dc(arr, mid + 1, high)

    # Conquer: combine with 2 comparisons
    comparison_count += 1
    overall_min = lmin if lmin < rmin else rmin
    comparison_count += 1
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


def min_max_naive(arr):
    """Straightforward linear scan, for comparison purposes."""
    mn, mx = arr[0], arr[0]
    comps = 0
    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x
        comps += 1
        if x > mx:
            mx = x
    return mn, mx, comps


def run_min_max(arr):
    """
    Convenience wrapper used by the web app.
    Resets the global counter, runs both algorithms, and returns a dict of results.
    """
    global comparison_count
    comparison_count = 0

    mn, mx = min_max_dc(arr, 0, len(arr) - 1)
    dc_comps = comparison_count

    _, _, naive_comps = min_max_naive(arr)

    n = len(arr)
    formula = (3 * n) // 2 - 2 if n >= 2 else 0

    return {
        "array": arr,
        "min": mn,
        "max": mx,
        "dc_comparisons": dc_comps,
        "naive_comparisons": naive_comps,
        "formula_3n_2_minus_2": formula,
    }


def get_user_array():
    """
    Reads a list of numbers from the user (command line).
    Accepts comma or space separated integers, e.g.:
        3, 1, 7, 4, 9
    or
        3 1 7 4 9
    """
    raw = input("Enter the numbers separated by spaces or commas: ")
    raw = raw.replace(",", " ")
    numbers = [int(x) for x in raw.split()]
    if not numbers:
        raise ValueError("You must enter at least one number.")
    return numbers


if __name__ == "__main__":
    print("Ex. No. 5 | Min-Max using Divide and Conquer")
    print("-" * 50)

    arr = get_user_array()
    result = run_min_max(arr)

    print(f"\nArray             : {result['array']}")
    print(f"Min                : {result['min']}")
    print(f"Max                : {result['max']}")
    print(f"D&C Comparisons    : {result['dc_comparisons']}")
    print(f"Naive Comparisons  : {result['naive_comparisons']}")
    print(f"Formula (3n/2 - 2) : {result['formula_3n_2_minus_2']}")
