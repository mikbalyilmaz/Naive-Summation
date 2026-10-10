# Changes

## Version 2.0.0

### New

- `naivesum/` holds the algorithms; the analyses and the tests are separate from it.
- Exact error measurement: the computed sum and the negated terms are added with `math.fsum` and rounded once.
- Pairwise and Kahan summation, the condition number of the sum, and Higham's error bounds.
- Unit tests (`tests/run_tests.py`) against exact rational arithmetic (`fractions.Fraction`) and the published bounds.
- Three analyses with fixed seeds, two figures (English and Turkish), CSV tables, and a project note in English and
  Turkish whose numbers are written from the tables.
- `CITATION.cff`, `requirements.txt`.

### Corrections to version 1

| # | Version 1 | Version 2 |
|---|---|---|
| 1 | The "true sum" was `np.sum(x, dtype=np.longdouble)`. The precision of `longdouble` depends on the platform; where it equals `float64`, the reference is just NumPy's pairwise sum and has its own rounding error. | Errors are computed exactly with `math.fsum`, independent of the platform. The accuracy of the old reference is measured in analysis 3. |
| 2 | "The absolute error grows linearly with n" was presented as the result. Linear growth is the worst-case bound. | Observed growth is compared with the bound: about $\sqrt{n}$ on the bound's scale for positive terms, almost none for U(−1,1). |
| 3 | Naive summation was called "numerically unstable and unreliable". | It is backward stable (Higham, 2002; Johnson, 2019); large relative errors come from ill-conditioned sums. |
| 4 | Relative errors were averaged; the mean is dominated by a few sums close to zero, and `1e-20` was added to the denominator. | Relative error is analysed against the condition number; mean and median are both reported. |
| 5 | No random seed; results changed at every run. | Fixed seeds. |
| 6 | A comment said 30 points while the code used 20. | Code and text agree. |
| 7 | The README showed `example_plot.png`, which is not in the repository, linked to `yourusername/naive_summation_error_analysis`, and contained a leftover citation marker `【Naive Summation.pdf】`. | Rewritten README; citation metadata in `CITATION.cff`. |
| 8 | File names contained spaces; an HTML and a PDF export duplicated the notebook. | Version 1 notebook kept as `legacy/naive_summation_v1.ipynb`; the exports remain in the `v1.0.0` release. |

## Version 1.0.0

First version: a notebook that sums random numbers in [−1, 1] and plots the mean absolute and relative error.
