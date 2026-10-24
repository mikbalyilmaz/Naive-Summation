"""Analysis 1: how the error of naive summation grows with n, compared with its worst-case bound and with
pairwise and Kahan summation.

Why: the error bound |E| <= (n - 1) eps sum|x_i| grows linearly in n, but it is a worst case. The question
is how the error grows in practice, and how that depends on the data.

Design: for each distribution, 30 arrays of 10^6 values; for 26 log-spaced lengths n the error of each
algorithm on the first n values is computed exactly. Errors are reported as the root mean square over the
30 arrays, divided by eps * sum|x_i|; in these units the worst-case bound for naive summation is n - 1.
"""

import numpy as np

from common import DISTRIBUTIONS, SEED, save_table
from naivesum import EPS, exact_error, kahan_prefix, l1_norm, naive_prefix, pairwise_sum
from naivesum.style import BLUE, INK, MUTED, L, fit_log_axis, save_figure, use_style

N_MAX = 10 ** 6
TRIALS = 30
GRID = np.unique(np.round(np.logspace(1, 6, 26)).astype(int))
METHODS = ("naive", "pairwise", "kahan")

rows = []
for d_index, (dist, (low, high)) in enumerate(DISTRIBUTIONS.items()):
    rng = np.random.default_rng(SEED + d_index)
    errors = {m: np.zeros((TRIALS, GRID.size)) for m in METHODS}
    norms = np.zeros((TRIALS, GRID.size))
    for t in range(TRIALS):
        x = rng.uniform(low, high, N_MAX)
        naive = naive_prefix(x)
        kahan = kahan_prefix(x, GRID)
        for k, n in enumerate(GRID):
            head = x[:n]
            norms[t, k] = l1_norm(head)
            errors["naive"][t, k] = exact_error(naive[n - 1], head)
            errors["pairwise"][t, k] = exact_error(pairwise_sum(head), head)
            errors["kahan"][t, k] = exact_error(kahan[k], head)
    for m in METHODS:
        normalized = np.sqrt(np.mean((errors[m] / (EPS * norms)) ** 2, axis=0))
        rms_abs = np.sqrt(np.mean(errors[m] ** 2, axis=0))
        for k, n in enumerate(GRID):
            rows.append({"distribution": dist, "n": int(n), "method": m, "rms_error": rms_abs[k],
                         "rms_error_over_eps_l1": normalized[k], "mean_l1": norms[:, k].mean()})
    print(dist, "done")

save_table(rows, "table1_error_growth")

# Order of growth: least-squares slope of log(normalised error) on log(n) for n >= 1000. A slope of 1 means
# the error grows like the bound, 1/2 like sqrt(n) relative to the bound's scale, 0 like the scale itself.
slopes = []
for dist in DISTRIBUTIONS:
    for m in METHODS:
        sel = [r for r in rows if r["distribution"] == dist and r["method"] == m and r["n"] >= 1000]
        n = np.array([r["n"] for r in sel], dtype=float)
        y = np.array([r["rms_error_over_eps_l1"] for r in sel])
        slopes.append({"distribution": dist, "method": m,
                       "slope_normalized": np.polyfit(np.log(n), np.log(y), 1)[0],
                       "slope_absolute": np.polyfit(np.log(n), np.log([r["rms_error"] for r in sel]), 1)[0],
                       "normalized_at_max_n": y[-1]})
save_table(slopes, "table2_growth_slopes")
for s in slopes:
    print(s)

use_style()
COLORS = {"naive": BLUE, "pairwise": MUTED, "kahan": INK}


def draw():
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(4.75, 2.6), constrained_layout=True)
    names = {"naive": L("Naive", "Naive"), "pairwise": L("Pairwise", "İkili"), "kahan": "Kahan"}
    n = GRID.astype(float)
    for k, (ax, dist) in enumerate(zip(axes, DISTRIBUTIONS)):
        ax.plot(n, n - 1, color=INK, ls=(0, (3, 2)), lw=0.9,
                label=L("Worst-case bound, $n-1$", "En kötü durum sınırı, $n-1$"))
        for m in METHODS:
            y = [r["rms_error_over_eps_l1"] for r in rows if r["distribution"] == dist and r["method"] == m]
            ax.plot(n, y, color=COLORS[m], lw=1.3, marker="o", ms=2, label=names[m])
        fit_log_axis(ax, "x", n)
        fit_log_axis(ax, "y", [1e-4, 1e6], every=2)
        ax.set_xlabel("n")
        ax.set_title(f"({'ab'[k]}) " + dist.replace("-", "−"))
    axes[0].set_ylabel(L("RMS error / ($\\varepsilon\\,\\sum|x_i|$)", "KOH hata / ($\\varepsilon\\,\\sum|x_i|$)"))
    axes[0].legend(loc="lower right", fontsize=6.3, handlelength=2.2)
    return fig


save_figure("fig1_error_growth", draw,
            heading=lambda: L("Figure 1. Error of three summation algorithms against the worst-case bound",
                              "Şekil 1. Üç toplama yönteminin hatası ve en kötü durum sınırı"))
