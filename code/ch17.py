"""Construct arrowhead extensions of small diagonal stiffness matrices."""

import numpy as np


def extension(old, target):
    """Return a real symmetric border for descending, interlaced lists."""
    old, target = np.asarray(old, float), np.asarray(target, float)
    n = old.size
    assert target.size == n + 1
    assert np.all(target[:-1] >= old) and np.all(old >= target[1:])
    repeated = old[:-1] == old[1:]
    active_indices = np.flatnonzero(np.r_[True, ~repeated])
    active_old = old[active_indices]
    active_target = target[np.r_[True, ~repeated, True]]
    coupling = np.zeros(n)

    for j, value in enumerate(active_old):
        numerator = np.prod(value - active_target)
        derivative = np.prod(value - np.delete(active_old, j))
        squared = -numerator / derivative
        assert squared >= 0
        active_index = active_indices[j]
        coupling[active_index] = np.sqrt(squared)

    matrix = np.zeros((n + 1, n + 1))
    matrix[:n, :n] = np.diag(old)
    matrix[:n, n] = matrix[n, :n] = coupling
    matrix[n, n] = np.sum(target) - np.sum(old)
    return matrix


def main():
    matrix = extension([6, 2], [8, 4, 1])
    tol = 1e-12
    np.testing.assert_allclose(
        np.linalg.eigvalsh(matrix), [1, 4, 8], atol=tol, rtol=0
    )
    np.testing.assert_allclose(
        np.linalg.eigvalsh(matrix[:2, :2]), [2, 6], atol=tol, rtol=0
    )
    np.testing.assert_allclose(matrix[:2, 2] ** 2, [5, 3], atol=tol, rtol=0)

    diagonal = np.sort(np.diag(matrix))[::-1]
    values = np.linalg.eigvalsh(matrix)[::-1]
    assert np.all(np.cumsum(diagonal) <= np.cumsum(values) + tol)
    assert abs(sum(diagonal) - sum(values)) <= tol

    repeated = extension([6, 6, 2], [8, 6, 4, 1])
    np.testing.assert_allclose(
        np.linalg.eigvalsh(repeated), [1, 4, 6, 8], atol=tol, rtol=0
    )
    assert repeated[1, -1] == 0

    print(f"Extended spectrum: {values}")
    print(f"Sorted diagonal: {diagonal}")
    print(f"Border couplings: {matrix[:2, 2]}")


if __name__ == "__main__":
    main()
