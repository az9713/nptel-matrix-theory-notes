"""Compare calibration and residual error in a two-channel inverse model."""

import numpy as np


def main():
    norm = lambda value: np.linalg.norm(value, ord=np.inf)
    gap = 1e-4
    a = np.diag([1.0, gap])
    e = np.diag([0.0, -0.1 * gap])
    b = np.array([1.0, gap])
    x = np.linalg.solve(a, b)
    x_new = np.linalg.solve(a + e, b)
    q = norm(np.linalg.solve(a, e))
    relative_error = norm(x_new - x) / norm(x)
    bound = q / (1 - q)
    assert np.isclose(relative_error, bound)
    x_candidate = np.array([1.0, 0.0])
    residual = norm(b - a @ x_candidate)
    assert np.isclose(residual, gap)
    assert np.isclose(norm(x - x_candidate), 1.0)
    backward = residual / (norm(a) * norm(x_candidate) + norm(b))
    assert np.isclose(backward, gap / 2)
    print(f"calibration: q={q:.6g}, error={relative_error:.6g}, "
          f"bound={bound:.6g}")
    print(f"candidate: residual={residual:.6g}, "
          f"backward error={backward:.6g}, forward error=1")


if __name__ == "__main__":
    main()
