"""Check index-by-index bounds and a robust stiffness certificate."""

import numpy as np


def descending(matrix):
    """Return the real eigenvalues of a Hermitian matrix, largest first."""
    return np.linalg.eigvalsh(matrix)[::-1]


def main():
    a = np.diag([8.0, 4.0, 2.0])
    z = np.array([0.0, 1.0, 1.0])
    b = np.outer(z, z)
    updated = a + b
    alpha, beta, gamma = map(descending, (a, b, updated))
    n = len(alpha)
    tol = 1e-12

    predicted = [8, 4 + np.sqrt(2), 4 - np.sqrt(2)]
    np.testing.assert_allclose(gamma, predicted, atol=tol, rtol=0)
    assert np.all(gamma >= alpha + beta[-1] - tol)
    assert np.all(gamma <= alpha + beta[0] + tol)
    for i in range(n):
        for j in range(n):
            if i + j < n:
                assert gamma[i + j] <= alpha[i] + beta[j] + tol
            if i + j >= n - 1:
                assert gamma[i + j - n + 1] >= alpha[i] + beta[j] - tol

    certificate = descending(updated[:2, :2])[-1]
    np.testing.assert_allclose(certificate, 5, atol=tol, rtol=0)
    assert certificate <= gamma[1] + tol
    assert np.all(gamma[1:] <= alpha[:-1] + tol)

    error = -0.4 * np.eye(n)
    perturbed = descending(updated + error)
    np.testing.assert_allclose(
        gamma - perturbed, np.linalg.norm(error, 2), atol=tol, rtol=0
    )
    assert perturbed[1] >= 5

    print(f"Updated spectrum: {gamma}")
    print(f"Plane certificate: {certificate:.3f}")
    print(f"Worst permitted second stiffness: {perturbed[1]:.6f}")


if __name__ == "__main__":
    main()
