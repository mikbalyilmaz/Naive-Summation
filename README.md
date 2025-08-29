# Naive Summation Error Analysis  

This project demonstrates the **numerical errors** that occur in the naive summation algorithm (sequential accumulation).  
By summing random values in the interval [-1, 1] with different list sizes, we compare the results with a high-precision reference and measure the **absolute** and **relative** errors.  
The aim of this project is to **show that computers, unlike humans, are not error-free**: due to floating-point arithmetic, even a simple addition may accumulate noticeable errors as the data size grows.  

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

## Purpose and Message  

The purpose of this project is not only to illustrate a numerical phenomenon, but also to **highlight a philosophical point**:  
> Even though machines are often seen as exact and flawless, they are bound by the limitations of floating-point arithmetic.  
> Humans make mistakes in logic or reasoning; computers make mistakes in **representation and precision**.  
This project shows that machines, too, are far from “error-free beings.”  

---

## Reference  

Inspired by the lecture notes:  
*“Accuracy of Naive Summation”*, MIT 18.335J *Introduction to Numerical Methods*,  
by S. G. Johnson (2019)【Naive Summation.pdf】.  

---

## License  

This project is licensed under the **MIT License** – feel free to use, modify, and share.  
