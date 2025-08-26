# Naive Summation Error Analysis

This application analyzes the numerical errors of the **naive summation** (sequential accumulation) algorithm.  
Random values in [-1, 1] are summed in lists of different sizes, and the results are compared with a high-precision reference.  
Absolute and relative errors are measured and visualized on log–log scales.  

---

## Mathematical Background

The naive summation algorithm performs sequential accumulation:

$$
s_0 = 0, \quad s_k = s_{k-1} + x_k \quad (1 \leq k \leq n)
$$

So the final result is:

$$
\tilde{S} = \sum_{i=1}^{n} x_i
$$

In floating-point arithmetic, each addition introduces a small rounding error $\varepsilon_k$:

$$
fl(a + b) = (a + b)(1 + \varepsilon_k), \quad |\varepsilon_k| \leq \varepsilon_{machine}
$$

Thus, the computed result can be expressed as:

$$
\tilde{S} = \sum_{i=1}^n x_i \prod_{k=i}^n (1 + \varepsilon_k)
$$

The forward error bound is approximately:

$$
| \tilde{S} - S | \leq n \cdot \varepsilon_{machine} \cdot \sum_{i=1}^n |x_i| + O(\varepsilon_{machine}^2)
$$

This shows that the absolute error can grow **linearly with n**.

---

## How It Works

1. Generate random numbers in the interval [-1, 1].  
2. Compute the **true sum** using high precision (`longdouble`).  
3. Compute the **naive sum** by sequential accumulation.  
4. Measure both:
   - **Absolute error:** $| \tilde{S} - S |$
   - **Relative error:** $\frac{| \tilde{S} - S |}{| S |}$  
5. Plot the results on log–log scales for problem sizes $10^2$ up to $10^5$.  

---

## Example Output

- **Absolute Error (left):** grows steadily with $n$.  
- **Relative Error (right):** fluctuates due to cancellation between positive and negative numbers.  

<p align="center">
  <img src="example_plot.png" width="700">
</p>

---

## Reference

This application is inspired by the lecture notes:  
*“Accuracy of Naive Summation”*, MIT 18.335J *Introduction to Numerical Methods*,  
by S. G. Johnson (2019)【Naive Summation.pdf】.

---

## License

This project is licensed under the **MIT License** – feel free to use, modify, and share.  
