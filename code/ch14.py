"""Compare first-pivot choices and check two structured factorizations."""

import numpy as np
from scipy.linalg import lu, solve_triangular


def main():
    a = np.array([[1e-8, 1], [1, 1]], dtype=np.float32)
    b = a @ np.ones(2, dtype=a.dtype)
    multiplier = a[1, 0] / a[0, 0]
    second = (b[1] - multiplier * b[0]) / (
        a[1, 1] - multiplier * a[0, 1])
    first = (b[0] - a[0, 1] * second) / a[0, 0]
    unpivoted = np.array([first, second])
    inverse_permutation, lower, upper = lu(a)
    p = inverse_permutation.T
    np.testing.assert_allclose(p @ a, lower @ upper, atol=1e-7)
    intermediate = solve_triangular(lower, p @ b, lower=True)
    pivoted = solve_triangular(upper, intermediate)
    np.testing.assert_allclose(unpivoted, [0, 1])
    np.testing.assert_allclose(pivoted, [1, 1])
    h = np.array([[4.0, 2.0], [2.0, 3.0]])
    l = np.array([[1.0, 0.0], [0.5, 1.0]])
    d = np.diag([4.0, 2.0])
    np.testing.assert_allclose(l @ d @ l.T, h)
    cholesky = np.linalg.cholesky(h)
    np.testing.assert_allclose(cholesky, l @ np.sqrt(d))
    print(f"first multiplier without pivoting: {multiplier:.3g}")
    print(f"unpivoted: {unpivoted}, pivoted: {pivoted}")
    print(f"Cholesky diagonal: {cholesky.diagonal()}")


if __name__ == "__main__":
    main()
