"""Accuracy of naive summation: algorithms, exact error measurement and figure style."""

from .summation import (
    EPS,
    condition_number,
    exact_error,
    exact_sum,
    gamma,
    kahan_prefix,
    kahan_sum,
    l1_norm,
    naive_prefix,
    naive_sum,
    pairwise_sum,
)

__version__ = "2.0.0"
