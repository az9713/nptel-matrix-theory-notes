"""Check spectral transfers and a simple eigenvalue derivative."""

import numpy as np


def main():
    a = np.array([[1.0, -4.0], [0.0, 1.0], [0.0, 0.0]])
    b = np.array([[0.8, 3.2, 0.0], [0.0, 0.5, 0.0]])
    m = a @ b
    reduced = b @ a
    assert np.allclose(np.sort(np.linalg.eigvals(m)), [0, 0.5, 0.8])
    assert np.allclose(np.sort(np.linalg.eigvals(reduced)), [0.5, 0.8])
    right = np.eye(2)
    assert np.allclose(reduced @ right, right @ np.diag([0.8, 0.5]))
    v = np.column_stack((a @ right, [0.0, 0.0, 1.0]))
    rows = np.linalg.solve(v, np.eye(3))
    eigenvalues = np.diag([0.8, 0.5, 0.0])
    assert np.allclose(m @ v, v @ eigenvalues)
    assert np.allclose(rows @ m, eigenvalues @ rows)
    assert np.allclose(rows @ v, np.eye(3))
    perturbation = np.zeros_like(m)
    perturbation[1, 0] = 1.0
    h = 1e-7
    shifted = max(np.linalg.eigvals(m + h * perturbation))
    derivative = rows[0] @ perturbation @ v[:, 0]
    assert np.isclose((shifted - 0.8) / h, derivative)
    norm_product = np.linalg.norm(rows[0]) * np.linalg.norm(v[:, 0])
    print(f"eigenvalue derivative: {derivative:.6f}")
    print(f"first spectral projector norm: {norm_product:.6f}")


if __name__ == "__main__":
    main()
