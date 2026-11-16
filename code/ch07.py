"""Check transient growth, a series tail bound, and Jacobi convergence."""

import numpy as np


def main():
    identity = np.eye(2)
    update = np.array([[0.8, 4], [0, 0.8]])
    nilpotent = update - 0.8 * identity
    values = []
    for k in range(1, 25):
        power = np.linalg.matrix_power(update, k)
        expected = 0.8**k * identity + k * 0.8**(k - 1) * nilpotent
        np.testing.assert_allclose(power, expected)
        values.append(power[0, 1])
    assert np.isclose(np.max(values), 8.192)
    assert np.allclose(values[3:5], [8.192, 8.192])
    print(f"Peak in the first coordinate: {np.max(values):.3f}")

    scale = np.diag([1, 0.02])
    adapted = np.linalg.solve(scale, update @ scale)
    ratio = np.linalg.norm(adapted, np.inf)
    assert np.isclose(ratio, 0.88)
    m = 24
    partial = sum(np.linalg.matrix_power(adapted, k) for k in range(m + 1))
    inverse = np.linalg.inv(identity - adapted)
    tail = np.linalg.norm(inverse - partial, np.inf)
    bound = ratio ** (m + 1) / (1 - ratio)
    assert tail <= bound
    np.testing.assert_allclose(
        np.linalg.solve(identity - update, [0, 1]), [100, 5]
    )
    print(f"Adapted inverse tail at m={m}: {tail:.6f} <= {bound:.6f}")

    system = np.array([[4, -1], [-2, 5]])
    diagonal = np.diag(system)
    jacobi = identity - system / diagonal[:, None]
    assert np.isclose(np.linalg.norm(jacobi, np.inf), 0.4)
    target = np.array([1, 3])
    exact = np.linalg.solve(system, target)
    np.testing.assert_allclose(exact, [4 / 9, 7 / 9])
    estimate = np.zeros(2)
    for _ in range(12):
        estimate = jacobi @ estimate + target / diagonal
    error = np.linalg.norm(estimate - exact, np.inf)
    assert error <= 0.4**12 * np.linalg.norm(exact, np.inf)
    print(f"Jacobi maximum error after 12 steps: {error:.6e}")


if __name__ == "__main__":
    main()
