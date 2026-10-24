"""Analysis 2: what drives the relative error.

Why: version 1 found that the relative error |E| / |S| "fluctuates". For summation the relative error is
bounded by (n - 1) eps * kappa, where kappa = sum|x_i| / |sum x_i| is the condition number of the problem.
With terms of both signs the sum is often close to zero, kappa is large, and the relative error is large,
even though the absolute error is small. This analysis measures that relation.

Design: 2,000 arrays of 10^4 values from U(-1,1); for each, kappa and the relative error of naive and
Kahan summation, both computed exactly.
"""

import math

import numpy as np

from common import SEED, save_table
from naivesum import EPS, condition_number, exact_error, exact_sum, kahan_sum, naive_prefix
from naivesum.style import BLUE, INK, MUTED, RED, L, fit_log_axis, may_touch, save_figure, use_style

N = 10 ** 4
TRIALS = 2000

rng = np.random.default_rng(SEED + 10)
rows = []
for t in range(TRIALS):
    x = rng.uniform(-1.0, 1.0, N)
    s = exact_sum(x)
    rows.append({"trial": t, "kappa": condition_number(x),
                 "rel_error_naive": abs(exact_error(naive_prefix(x)[-1], x)) / abs(s),
                 "rel_error_kahan": abs(exact_error(kahan_sum(x), x)) / abs(s)})
save_table(rows, "table3_conditioning")

kappa = np.array([r["kappa"] for r in rows])
rel_naive = np.array([r["rel_error_naive"] for r in rows])
rel_kahan = np.array([r["rel_error_kahan"] for r in rows])
positive = rel_naive > 0
slope = np.polyfit(np.log(kappa[positive]), np.log(rel_naive[positive]), 1)[0]
top = np.sort(rel_naive)[::-1]
summary = [{
    "n": N, "trials": TRIALS,
    "kappa_median": float(np.median(kappa)), "kappa_max": float(kappa.max()),
    "slope_log_rel_error_on_log_kappa": float(slope),
    "naive_rel_error_mean": float(rel_naive.mean()), "naive_rel_error_median": float(np.median(rel_naive)),
    "share_of_mean_from_top_1pct": float(top[: TRIALS // 100].sum() / top.sum()),
    "kahan_rel_error_max_over_eps": float(rel_kahan.max() / EPS),
    "naive_bound_violations": int(np.sum(rel_naive > (N - 1) * EPS * kappa / (1 - (N - 1) * EPS))),
}]
save_table(summary, "table4_conditioning_summary")
print(summary)

use_style()


def draw():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(4.75, 2.7), constrained_layout=True)
    k = np.logspace(math.log10(kappa.min()) - 0.1, math.log10(kappa.max()) + 0.1, 50)
    ax.plot(k, (N - 1) * EPS * k, color=INK, ls=(0, (3, 2)), lw=0.9,
            label=L("Bound for naive summation, $(n-1)\\,\\varepsilon\\,\\kappa$",
                    "Naive toplama sınırı, $(n-1)\\,\\varepsilon\\,\\kappa$"))
    ax.scatter(kappa[positive], rel_naive[positive], s=3, color=BLUE, lw=0, label="Naive")
    keep = rel_kahan > 0
    ax.scatter(kappa[keep], rel_kahan[keep], s=3, color=MUTED, lw=0, label="Kahan")
    may_touch(ax.axhline(EPS, color=RED, lw=0.8, ls=(0, (1, 1.4))))
    ax.annotate("$\\varepsilon = 2^{-53}$", xy=(1, EPS), xycoords=("axes fraction", "data"), xytext=(-2, 2),
                textcoords="offset points", color=RED, fontsize=7, ha="right", va="bottom")
    fit_log_axis(ax, "x", k)
    # 1e-4 leaves room for the legend
    values = np.concatenate([rel_naive[positive], rel_kahan[keep], (N - 1) * EPS * k, [1e-4]])
    fit_log_axis(ax, "y", values, every=2)
    ax.set_xlabel(L("Condition number $\\kappa = \\sum|x_i|\\,/\\,|\\sum x_i|$",
                    "Koşul sayısı $\\kappa = \\sum|x_i|\\,/\\,|\\sum x_i|$"))
    ax.set_title(L(f"Relative error $|E|\\,/\\,|S|$, {TRIALS:,} arrays of $n = 10^4$ values from U(−1,1)",
                   "Göreli hata $|E|\\,/\\,|S|$, "
                   + f"U(−1,1) dağılımından {TRIALS:,} dizi".replace(",", ".") + ", $n = 10^4$"))
    ax.legend(loc="upper left", markerscale=2.5, fontsize=6.3)
    return fig


save_figure("fig2_conditioning", draw,
            heading=lambda: L("Figure 2. Relative error against the condition number of the sum",
                              "Şekil 2. Göreli hata ve toplamın koşul sayısı"))
