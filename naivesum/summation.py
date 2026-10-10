"""Summation algorithms and exact error measurement for double-precision numbers.

Notation follows Higham (2002, ch. 4): eps = 2**-53 is the unit roundoff of IEEE double precision, so that
fl(a + b) = (a + b)(1 + d) with |d| <= eps. (Trefethen and Bau, and the MIT 18.335 notes, call the same
quantity epsilon_machine.)

Author: Muhammed Ikbal Yilmaz
"""

import math

import numpy as np

EPS = 2.0 ** -53  # unit roundoff of float64


def _as_float_array(x):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 1:
        raise ValueError("x must be one-dimensional")
    return x


def naive_sum(x):
    """Recursive (naive) summation: s_k = s_{k-1} + x_k, one Python addition per element."""
    total = 0.0
    for value in _as_float_array(x).tolist():
        total += value
    return total


def naive_prefix(x):
    """All partial sums of naive summation, s_1, ..., s_n.

    np.cumsum accumulates sequentially, so its k-th element is exactly the naive sum of the first k
    values (unlike np.sum, which uses pairwise summation). The unit tests check this bit for bit.
    """
    return np.cumsum(_as_float_array(x))


def pairwise_sum(x):
    """Pairwise (cascade) summation: add neighbours level by level until one value is left.

    Padding with a zero when a level has odd length does not change any sum, because adding 0 is exact.
    """
    level = _as_float_array(x).copy()
    if level.size == 0:
        return 0.0
    while level.size > 1:
        if level.size % 2:
            level = np.append(level, 0.0)
        level = level[0::2] + level[1::2]
    return float(level[0])


def kahan_prefix(x, at):
    """Kahan's (1965) compensated summation, returning the running sum after each count listed in `at`.

    `at` must be increasing counts between 1 and len(x). The correction c carries the low-order part lost
    in each addition and subtracts it from the next term.
    """
    x = _as_float_array(x)
    at = list(at)
    if any(b <= a for a, b in zip(at, at[1:])) or (at and (at[0] < 1 or at[-1] > x.size)):
        raise ValueError("`at` must be increasing counts between 1 and len(x)")
    out = []
    total, c, j = 0.0, 0.0, 0
    for i, value in enumerate(x.tolist(), start=1):
        y = value - c
        t = total + y
        c = (t - total) - y
        total = t
        if j < len(at) and i == at[j]:
            out.append(total)
            j += 1
    return np.array(out)


def kahan_sum(x):
    """Kahan's compensated summation of all of x."""
    x = _as_float_array(x)
    return float(kahan_prefix(x, [x.size])[0]) if x.size else 0.0


def exact_sum(x):
    """The exact sum of x, correctly rounded to double precision (math.fsum)."""
    return math.fsum(_as_float_array(x).tolist())


def exact_error(s_hat, x, low=0.0):
    """Error (s_hat + low) - sum(x), computed exactly and rounded once at the end.

    fsum adds s_hat, low and -x_1, ..., -x_n without intermediate rounding. Comparing with a rounded
    reference sum instead would add up to half a unit in the last place of the sum to every measured
    error, which is as large as the error of the best algorithms. `low` holds the low-order part of a
    reference computed in a wider format (see the analysis of the version 1 reference).
    """
    x = _as_float_array(x)
    return math.fsum([float(s_hat), float(low)] + (-x).tolist())


def l1_norm(x):
    """sum(|x_i|), the scale of the worst-case error bounds."""
    return math.fsum(np.abs(_as_float_array(x)).tolist())


def condition_number(x):
    """Condition number of summation, sum(|x_i|) / |sum(x_i)| (infinite if the sum is zero)."""
    s = exact_sum(x)
    return math.inf if s == 0.0 else l1_norm(x) / abs(s)


def gamma(k):
    """Higham's gamma_k = k eps / (1 - k eps), the constant of the rigorous error bounds."""
    return k * EPS / (1.0 - k * EPS)
