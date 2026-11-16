"""Check spectral location, sensitivity, and matching on small fixtures."""

from itertools import permutations

import numpy as np


def main():
    a = np.array([[-2.0, 4.0, 0.0], [0.0, -3.0, 0.0], [0.0, 0.0, -8.0]])
    e = np.zeros_like(a)
    e[1, 0] = 1.0
    t = 0.02
    perturbation = t * e
    changed = a + perturbation
    tol = 1e-12

    scaling = np.array([8.0, 1.0, 1.0])
    scaled = changed * scaling[None, :] / scaling[:, None]
    centers = np.diag(scaled)
    radii = np.sum(abs(scaled), axis=1) - abs(centers)
    np.testing.assert_allclose(radii, [0.5, 0.16, 0], atol=tol, rtol=0)
    distances = abs(centers[:, None] - centers[None, :])
    np.fill_diagonal(distances, np.inf)
    assert np.all(distances > radii[:, None] + radii[None, :])
    eigenvalues = np.linalg.eigvals(changed)
    membership = abs(centers[:, None] - eigenvalues) <= radii[:, None] + tol
    np.testing.assert_array_equal(membership.sum(axis=1), [1, 1, 1])
    assert np.max(centers + radii) < 0

    right = np.array([1.0, 0.0, 0.0])
    left = np.array([1.0, 4.0, 0.0])
    derivative = left @ e @ right / (left @ right)
    step = 1e-6
    numeric = (
        np.linalg.eigvals(a + step * e).max()
        - np.linalg.eigvals(a - step * e).max()
    ) / (2 * step)
    np.testing.assert_allclose(numeric, derivative, atol=1e-8, rtol=0)

    defective = a[:2, :2].copy()
    defective[1, 1] = defective[0, 0]
    split = np.linalg.eigvals(defective + step * e[:2, :2])
    expected = -2 + 2 * np.sqrt(step) * np.array([-1, 1])
    np.testing.assert_allclose(np.sort(split), expected, atol=tol, rtol=0)

    v = np.eye(3)
    v[0, 1] = -4
    np.testing.assert_allclose(a @ v, v * centers, atol=tol, rtol=0)
    radius = np.linalg.cond(v, np.inf) * np.linalg.norm(perturbation, np.inf)
    nearest = np.min(abs(centers[:, None] - eigenvalues), axis=0)
    np.testing.assert_allclose(radius, 0.5, atol=tol, rtol=0)
    assert nearest.max() <= radius + tol

    symmetric_error = t * (e + e.T)
    normal_eigenvalues = np.linalg.eigvalsh(np.diag(centers) + symmetric_error)
    cost = min(
        np.linalg.norm(centers - normal_eigenvalues[list(order)])
        for order in permutations(range(3))
    )
    bound = np.linalg.norm(symmetric_error, "fro")
    assert cost <= bound + tol

    print(f"Scaled disk radii: {radii}")
    print(f"Mode derivative: {derivative:.6f}")
    print(f"Maximum distance to nominal spectrum: {nearest.max():.6f}")
    print(f"Normal matching distance: {cost:.6f} (bound {bound:.6f})")


if __name__ == "__main__":
    main()
