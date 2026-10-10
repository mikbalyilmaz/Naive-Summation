# Accuracy of Naive Summation: Error Growth, Conditioning and Better Algorithms

[![tests](https://github.com/mikbalyilmaz/Naive-Summation/actions/workflows/tests.yml/badge.svg)](https://github.com/mikbalyilmaz/Naive-Summation/actions/workflows/tests.yml)

Version 2 of a small study of the rounding error of naive (recursive) summation,

$$s_0 = 0, \qquad s_k = s_{k-1} + x_k, \qquad \hat S = s_n,$$

in double-precision arithmetic. Every error is computed exactly, compared with its theoretical bound, and explained
through the condition number of the sum. Pairwise summation, Kahan's compensated summation, `np.sum` and `math.fsum`
are compared for accuracy and speed. A short project note (English and Turkish) explains why each analysis was done
and what it shows.

## Contents

| Path | What it is |
|---|---|
| `naivesum/summation.py` | Naive, pairwise and Kahan summation; exact errors with `math.fsum`; condition number; Higham's $\gamma_k$ |
| `naivesum/style.py` | Shared figure style (Latin Modern Roman, colours, English and Turkish versions of each figure) |
| `tests/run_tests.py` | Unit tests against exact rational arithmetic and published error bounds |
| `analysis/01_error_growth.py` | How the error grows with $n$, against the worst-case bound (Figure 1) |
| `analysis/02_conditioning.py` | Relative error against the condition number (Figure 2) |
| `analysis/03_algorithms.py` | Accuracy and running time of six methods; accuracy of the version 1 reference |
| `analysis/run_all.py` | Runs the three analyses in order |
| `figures/` | Figures as PNG (300 dpi) and PDF, every reported table as CSV; `figures/tr/` holds the Turkish figures |
| `paper/naive_note.pdf`, `paper/naive_notu.pdf` | Project note in English and in Turkish; `make_paper.py` writes all their numbers from `figures/*.csv` |
| `legacy/naive_summation_v1.ipynb` | Version 1, unchanged |
| `fonts/` | Latin Modern Roman (GUST Font License) |

## How to run

```
pip install -r requirements.txt
python tests/run_tests.py
cd analysis
python run_all.py                    # about one minute
cd ../paper
python make_paper.py
xelatex naive_note.tex && xelatex naive_note.tex     # English; needs XeLaTeX
xelatex naive_notu.tex && xelatex naive_notu.tex     # Turkish
```

Seeds are fixed, so every number except the running times is the same on every machine.

## Usage

```python
import numpy as np
from naivesum import naive_sum, kahan_sum, exact_error, condition_number

x = np.random.default_rng(1).uniform(-1, 1, 10**6)
exact_error(naive_sum(x), x)     # exact error of naive summation
exact_error(kahan_sum(x), x)     # exact error of Kahan summation
condition_number(x)              # sum|x_i| / |sum x_i|
```

## Main results

With $\varepsilon = 2^{-53}$ the unit roundoff, the worst-case bound for naive summation is
$|E| \le (n-1)\,\varepsilon \sum|x_i|$ to first order (Higham, 2002).

- **The error is far below the bound.** In units of $\varepsilon\sum|x_i|$ the bound is $n - 1$. For positive terms,
  U(0,1), the RMS error grows like $\sqrt{n}$ (slope 0.50) and is 237 units at $n = 10^6$. For terms of both signs,
  U(−1,1), as in version 1, it hardly grows (slope 0.06) and stays below one unit.
- **The relative error is governed by the condition number** $\kappa = \sum|x_i| / |\sum x_i|$. Over 2,000 sums of
  $10^4$ values it rises with $\kappa$, while Kahan's relative error never exceeds $\varepsilon$. The mean relative
  error is 2.8 times its median, because 1% of the sums account for 37% of the mean.
- **Naive summation is backward stable, not unstable.** Large relative errors come from ill-conditioned sums.
- **Better methods are cheap.** For $n = 10^6$, `np.sum` is about 190 times more accurate than naive summation, and
  `math.fsum` returns the correctly rounded sum while running faster than the Python loop of version 1.

All numbers are in `figures/*.csv` and in the project note.

## Changes from version 1

See [`NEWS.md`](NEWS.md). In short: version 1 used `np.sum(x, dtype=np.longdouble)` as the exact sum, although
`longdouble` has the precision of `float64` on some platforms; it described the worst-case bound as the observed growth,
called a backward stable algorithm unstable, and averaged relative errors that are dominated by a few near-zero sums.
Its README pointed to a missing figure and to placeholder links.

## Limitations

Only uniformly distributed data, double precision and sizes up to $10^6$ are studied. Running times come from one
machine. Kahan's method is written in Python here and is therefore slow; its cost is small only in compiled code.

## References

- Higham, N. J. (1993). The accuracy of floating point summation. *SIAM Journal on Scientific Computing*, 14(4), 783–799.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM.
- Johnson, S. G. (2019). Notes on the accuracy of naive summation; Backwards stability of recursive summation. MIT 18.335J, *Introduction to Numerical Methods*, Lecture 3. [Course page](https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/pages/week-2)
- Kahan, W. (1965). Further remarks on reducing truncation errors. *Communications of the ACM*, 8(1), 40.

## Citation

Citation metadata are in [`CITATION.cff`](CITATION.cff); GitHub shows them under "Cite this repository".

## Licence

MIT; see [`LICENSE`](LICENSE). The fonts in `fonts/` are distributed under the GUST Font License.
