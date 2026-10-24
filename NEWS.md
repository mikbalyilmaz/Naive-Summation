# Changes

## Version 2.1.0

No result changed: every table and every number in the notes is the same as in version 2.0.0.

- Figures redrawn in the style of the charts on muhammedikbalyilmaz.com: series in black and deep blue (#0033a0),
  red dotted lines for dates and reference values, labels at the end of the lines where possible, bold panel titles,
  Latin Modern Roman. Every figure is 4.75 inches wide, the width of the text in the notes.
- Every figure is drawn in English and in Turkish (decimal comma), as before.
- Axis rule: every value axis starts and ends at a labelled tick, and there are no minor ticks. Before a figure is
  saved, `naivesum/style.py` checks it and stops with an error if an axis limit is not a labelled tick, if two pieces of
  text overlap, if a note or a legend lies on a data line, or if a note leaves its panel.
- The project notes now use the note template: 11 pt, A4, 4.5 cm side margins, a header with the short name and
  the compilation date, and the page count. Wide equations and tables were split or set in a smaller size to fit the
  narrower text block.
- References: one paragraph per entry with a 1.27 cm hanging indent, the full journal name of *SIAM Journal on
  Scientific Computing* and the edition in parentheses.

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
