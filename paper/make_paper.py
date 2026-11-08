"""Writes every number and table of the project notes from ../figures/*.csv, so that the text cannot drift
away from the analysis. Run from inside paper/:  python make_paper.py

Output (suffix _en, for naive_note.tex): numbers_en.tex (one macro per quoted number) and
tab_algorithms_en.tex (table body ending with its bottom rule, because a rule cannot follow
\\input directly inside a tabular).
"""

import csv
from pathlib import Path

FIG = Path(__file__).resolve().parents[1] / "figures"
OUT = Path(__file__).resolve().parent


def read(name):
    with open(FIG / f"{name}.csv", newline="") as f:
        return list(csv.DictReader(f))


growth = {(r["distribution"], r["method"]): r for r in read("table2_growth_slopes")}
cond = read("table4_conditioning_summary")[0]
algos = read("table5_algorithms")
plat = read("table6_platform")[0]
by_key = {r["key"]: r for r in algos}

TEXT = {
    "en": {
        "big": ",", "dec": ".",
        "methods": {
            "naive_python_loop": "Naive, Python loop (version 1)",
            "naive_cumsum": "Naive, \\texttt{np.cumsum}",
            "pairwise": "Pairwise",
            "numpy_sum": "\\texttt{np.sum} (NumPy, partial pairwise)",
            "kahan": "Kahan, Python loop",
            "fsum": "\\texttt{math.fsum} (correctly rounded)",
            "v1_reference": "\\texttt{np.sum}, \\texttt{longdouble} (version 1 reference)",
        },
        "ld_float64": ("On this machine \\texttt{longdouble} has the same precision as \\texttt{float64}, so the "
                       "version 1 reference is simply NumPy's pairwise sum in double precision; its error is "
                       "{ratio}\\% of the error of naive summation"),
        "ld_wider": ("On this machine \\texttt{longdouble} is wider than \\texttt{float64} (spacing of numbers at 1: "
                     "${eps}$ against $2{dec}2\\times 10^{{-16}}$), so the version 1 reference happens to be accurate "
                     "here; on platforms where \\texttt{longdouble} has the precision of \\texttt{float64} it reduces to "
                     "NumPy's pairwise sum"),
    },
}


def build(lang):
    t = TEXT[lang]

    def dec(x, d):
        return f"{float(x):.{d}f}".replace(".", t["dec"])

    def num(x):
        return f"{round(float(x)):,}".replace(",", t["big"])

    def sci(x, d=1):
        mant, exp = f"{float(x):.{d}e}".split("e")
        return f"{mant.replace('.', t['dec'])}\\times 10^{{{int(exp)}}}"

    m = {}
    m["SlopeNaivePos"] = dec(growth[("U(0,1)", "naive")]["slope_normalized"], 2)
    m["NormNaivePos"] = num(growth[("U(0,1)", "naive")]["normalized_at_max_n"])
    m["NormPairPos"] = dec(growth[("U(0,1)", "pairwise")]["normalized_at_max_n"], 2)
    m["NormKahanPos"] = dec(growth[("U(0,1)", "kahan")]["normalized_at_max_n"], 2)
    m["SlopeNaiveSym"] = dec(growth[("U(-1,1)", "naive")]["slope_normalized"], 2)
    m["NormNaiveSym"] = dec(growth[("U(-1,1)", "naive")]["normalized_at_max_n"], 2)
    m["NormPairSym"] = dec(growth[("U(-1,1)", "pairwise")]["normalized_at_max_n"], 4)
    m["NormKahanSym"] = dec(growth[("U(-1,1)", "kahan")]["normalized_at_max_n"], 4)

    m["CondTrials"] = num(cond["trials"])
    m["KappaMedian"] = num(cond["kappa_median"])
    m["KappaMax"] = num(cond["kappa_max"])
    m["CondSlope"] = dec(cond["slope_log_rel_error_on_log_kappa"], 2)
    m["RelMean"] = sci(cond["naive_rel_error_mean"])
    m["RelMedian"] = sci(cond["naive_rel_error_median"])
    m["MeanOverMedian"] = dec(float(cond["naive_rel_error_mean"]) / float(cond["naive_rel_error_median"]), 1)
    m["TopShare"] = num(100 * float(cond["share_of_mean_from_top_1pct"]))
    m["KahanMaxEps"] = dec(cond["kahan_rel_error_max_over_eps"], 2)
    m["BoundViolations"] = num(cond["naive_bound_violations"])

    ms = {k: 1000 * float(r["median_seconds"]) for k, r in by_key.items()}
    m["TimeLoop"] = dec(ms["naive_python_loop"], 1)
    m["TimeFsum"] = dec(ms["fsum"], 1)
    m["TimeNpSum"] = dec(ms["numpy_sum"], 2)
    m["TimeKahan"] = dec(ms["kahan"], 0)
    m["LoopOverFsum"] = dec(ms["naive_python_loop"] / ms["fsum"], 1)

    ratio = float(plat["v1_reference_error_over_naive_error"])
    m["RefRatioPct"] = dec(100 * ratio, 2)
    m["Machine"] = (f"{plat['system']} {plat['machine']}, Python {plat['python']}, NumPy {plat['numpy']}"
                    .replace("_", "\\_"))
    if plat["longdouble_is_float64"] == "True":
        m["LongdoubleSentence"] = t["ld_float64"].replace("{ratio}", dec(100 * ratio, 1))
    else:
        m["LongdoubleSentence"] = (t["ld_wider"].replace("{eps}", sci(plat["longdouble_eps"]))
                                   .replace("{dec}", t["dec"]).replace("{{-16}}", "{-16}"))

    # The text states that the version 1 loop is slower than fsum and that fsum is slower than np.sum; warn if
    # timings on this machine contradict that.
    if not ms["naive_python_loop"] > ms["fsum"] > ms["numpy_sum"]:
        print("WARNING: timings do not match the ordering described in the notes; check the text of analysis 3.")

    (OUT / f"numbers_{lang}.tex").write_text(
        "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in m.items()), encoding="utf-8")

    lines = []
    for r in algos:
        err = float(r["rms_error_over_eps_l1"])
        err_text = "0" if err == 0 else (f"${sci(err)}$" if err < 0.01 else dec(err, 3))
        lines.append(f"{t['methods'][r['key']]} & {err_text} & {dec(1000 * float(r['median_seconds']), 2)} \\\\")
    lines.append("\\bottomrule")
    (OUT / f"tab_algorithms_{lang}.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


for lang in ("en",):
    build(lang)
print("Wrote numbers_*.tex and tab_algorithms_*.tex (en).")
