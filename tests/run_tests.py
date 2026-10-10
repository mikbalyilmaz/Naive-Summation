"""Unit tests. Run from the repository root:  python tests/run_tests.py

Each result is compared with an independent computation: exact rational arithmetic (fractions.Fraction),
a plain loop, or a published error bound.
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from naivesum import (EPS, condition_number, exact_error, exact_sum, gamma, kahan_prefix, kahan_sum,  # noqa: E402
                      l1_norm, naive_prefix, naive_sum, pairwise_sum)

failed = 0


def check(name, ok):
    global failed
    print(f"{'ok' if ok else 'FAIL':<5}{name}")
    if not ok:
        failed += 1


def exact_rational_sum(x):
    return sum((Fraction(float(v)) for v in x), Fraction(0))


rng = np.random.default_rng(20261010)
samples = [rng.uniform(-1, 1, n) for n in (1, 2, 3, 10, 100, 1000)] + \
          [rng.uniform(0, 1, n) for n in (5, 500)] + \
          [rng.normal(0, 1, 300) * 10.0 ** rng.integers(-8, 8, 300)]  # widely varying magnitudes

# Reference computations ------------------------------------------------------------------------------
check("exact_sum is the correctly rounded exact sum",
      all(exact_sum(x) == float(exact_rational_sum(x)) for x in samples))

check("exact_error equals the exactly computed error, rounded once",
      all(exact_error(naive_sum(x), x) == float(Fraction(naive_sum(x)) - exact_rational_sum(x)) for x in samples))

check("exact_error handles a low-order part",
      exact_error(1.0, [1.0, 2.0 ** -60], low=2.0 ** -60) == 0.0)

# Algorithms ------------------------------------------------------------------------------------------
check("np.cumsum reproduces the naive loop bit for bit",
      all(naive_prefix(x)[-1] == naive_sum(x) for x in samples))

check("kahan_prefix at the last count equals kahan_sum",
      all(kahan_prefix(x, [len(x)])[0] == kahan_sum(x) for x in samples))

check("all algorithms are exact on small integers",
      all(f(np.arange(1.0, 1001.0)) == 500500.0 for f in (naive_sum, pairwise_sum, kahan_sum, exact_sum)))

check("classic example: ten times 0.1",
      naive_sum([0.1] * 10) != 1.0 and exact_sum([0.1] * 10) == 1.0)

check("pairwise_sum of an odd-length array equals the exact sum of integers",
      pairwise_sum(np.arange(1.0, 1002.0)) == 1001 * 1002 / 2)

# Error bounds (Higham, 2002, ch. 4) ------------------------------------------------------------------
check("naive: |error| <= gamma_(n-1) * sum|x|",
      all(abs(exact_error(naive_sum(x), x)) <= gamma(len(x) - 1) * l1_norm(x) for x in samples))

check("pairwise: |error| <= gamma_ceil(log2 n) * sum|x|",
      all(abs(exact_error(pairwise_sum(x), x)) <= gamma(math.ceil(math.log2(max(len(x), 2)))) * l1_norm(x)
          for x in samples))

check("Kahan: |error| <= (2 eps + O(n eps^2)) * sum|x|, second-order term taken as 2 n eps^2",
      all(abs(exact_error(kahan_sum(x), x)) <= (2 * EPS + 2 * len(x) * EPS ** 2) * l1_norm(x) for x in samples))

check("condition number is at least 1",
      all(condition_number(x) >= 1.0 for x in samples))

# A case where naive summation loses everything and Kahan does not ----------------------------------------
x = [1.0] + [2.0 ** -53] * 1000
check("naive loses 1000 * 2^-53 entirely; Kahan and fsum keep it",
      naive_sum(x) == 1.0 and kahan_sum(x) == exact_sum(x) == float(exact_rational_sum(x)) != 1.0)

print(f"\n{failed} check(s) failed.")
sys.exit(1 if failed else 0)
