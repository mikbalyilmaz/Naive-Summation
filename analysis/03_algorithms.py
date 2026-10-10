"""Analysis 3: accuracy and running time of six ways to sum 10^6 numbers, and the reference used in
version 1.

Why: a better algorithm is only worth using if its cost is acceptable, so accuracy and time are measured
together. Version 1 took np.sum(x, dtype=np.longdouble) as the exact sum. The precision of longdouble
depends on the platform (NumPy documentation), so the accuracy of that reference is measured here too, on
the machine that runs the script.

Design: 10 arrays of 10^6 values from U(-1,1), as in version 1. Errors are computed exactly and reported
as the RMS of |E| / (eps * sum|x_i|), as in analysis 1. Times are the median of five calls.
"""

import math
import platform
import time

import numpy as np

from common import SEED, save_table
from naivesum import EPS, exact_error, kahan_sum, l1_norm, naive_sum, pairwise_sum

N = 10 ** 6
TRIALS = 10


def v1_reference(x):
    """The 'true sum' of version 1, split into a double and its low-order remainder."""
    ref = np.sum(x, dtype=np.longdouble)
    high = float(ref)
    low = float(ref - np.longdouble(high))
    return high, low


METHODS = [
    ("naive_python_loop", "Naive, Python loop (version 1)", lambda x: (naive_sum(x), 0.0)),
    ("naive_cumsum", "Naive, np.cumsum", lambda x: (float(np.cumsum(x)[-1]), 0.0)),
    ("pairwise", "Pairwise", lambda x: (pairwise_sum(x), 0.0)),
    ("numpy_sum", "np.sum (NumPy partial pairwise)", lambda x: (float(np.sum(x)), 0.0)),
    ("kahan", "Kahan, Python loop", lambda x: (kahan_sum(x), 0.0)),
    ("fsum", "math.fsum (correctly rounded)", lambda x: (math.fsum(x.tolist()), 0.0)),
    ("v1_reference", "np.sum, dtype=longdouble (version 1 reference)", v1_reference),
]

rng = np.random.default_rng(SEED + 20)
arrays = [rng.uniform(-1.0, 1.0, N) for _ in range(TRIALS)]
norms = [l1_norm(x) for x in arrays]

rows = []
for key, label, method in METHODS:
    normalized = []
    for x, norm in zip(arrays, norms):
        high, low = method(x)
        normalized.append(exact_error(high, x, low=low) / (EPS * norm))
    times = []
    for _ in range(5):
        start = time.perf_counter()
        method(arrays[0])
        times.append(time.perf_counter() - start)
    rows.append({"key": key, "method": label, "n": N,
                 "rms_error_over_eps_l1": float(np.sqrt(np.mean(np.square(normalized)))),
                 "median_seconds": float(np.median(times))})
    print(rows[-1])
save_table(rows, "table5_algorithms")

info = np.finfo(np.longdouble)
by_key = {r["key"]: r for r in rows}
platform_rows = [{
    "machine": platform.machine(), "system": platform.system(),
    "python": platform.python_version(), "numpy": np.__version__,
    "longdouble_bits": int(info.bits), "longdouble_eps": float(info.eps),
    "longdouble_is_float64": bool(info.eps == np.finfo(np.float64).eps),
    "v1_reference_error_over_naive_error":
        by_key["v1_reference"]["rms_error_over_eps_l1"] / by_key["naive_cumsum"]["rms_error_over_eps_l1"],
}]
save_table(platform_rows, "table6_platform")
print(platform_rows)
