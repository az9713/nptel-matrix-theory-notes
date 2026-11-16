"""Contrast unitary similarity with two-sided unitary equivalence."""

import numpy as np
from scipy.linalg import schur


def main():
    a = np.array([[0.8, 3.0], [0.0, 0.5]])
    q = np.array([[3.0, -4.0], [4.0, 3.0]]) / 5
    rotated = q @ a @ q.T
    triangular, z = schur(rotated, output="complex")
    np.testing.assert_allclose(z.conj().T @ z, np.eye(2), atol=1e-12)
    np.testing.assert_allclose(z @ triangular @ z.conj().T, rotated)
    np.testing.assert_allclose(np.sort(triangular.diagonal().real),
                               [0.5, 0.8])
    first = z[:, 0]
    np.testing.assert_allclose(rotated @ first, triangular[0, 0] * first)
    np.testing.assert_allclose(abs(triangular[0, 1]), 3.0)
    reversed_output = np.diag([-1.0, 1.0]) @ a
    np.testing.assert_allclose(reversed_output.T @ reversed_output, a.T @ a)
    np.testing.assert_allclose(np.linalg.eigvals(reversed_output),
                               [-0.8, 0.5])
    tracked = np.linalg.norm(rotated @ (q @ np.array([0.0, 1.0])))
    assert np.isclose(tracked, np.sqrt(9.25))
    print(f"one-step response: {tracked:.6f}")
    print(f"Schur coupling magnitude: {abs(triangular[0, 1]):.6f}")


if __name__ == "__main__":
    main()
