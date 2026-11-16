"""Check exact determinant identities and directional inverse sensitivity."""

from fractions import Fraction
from itertools import permutations
from math import prod

import numpy as np


def determinant(matrix):
    """Evaluate the signed permutation formula for small square matrices."""
    n = len(matrix)
    total = 0
    for perm in permutations(range(n)):
        inversions = sum(
            perm[i] > perm[j] for i in range(n) for j in range(i + 1, n)
        )
        total += (-1) ** inversions * prod(
            matrix[i][perm[i]] for i in range(n)
        )
    return total


def main():
    for eps in (Fraction(0), Fraction(1, 1000), Fraction(-3, 8)):
        matrix = [[1, 0, 1], [0, 1, 1], [1, 1, 2 + eps]]
        assert determinant(matrix) == eps
        swapped = [matrix[1], matrix[0], matrix[2]]
        assert determinant(swapped) == -eps

    eps, delta = 1e-3, 1e-4
    matrix = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 2 + eps]])
    offset = np.linalg.solve(matrix, [0, 0, delta])
    np.testing.assert_allclose(offset, [-0.1, -0.1, 0.1])
    np.testing.assert_allclose(
        np.linalg.solve(matrix, [delta, 0, delta]), [delta, 0, 0]
    )
    small = 1e-200 * np.diag([2, 1])
    assert np.isclose(np.linalg.cond(small), 2)
    assert np.linalg.det(small) == 0
    sign, log_magnitude = np.linalg.slogdet(small)
    assert sign == 1
    assert np.isclose(log_magnitude, np.log(2) + 2 * np.log(1e-200))
    print("Third-channel perturbation changes the solution by:", offset)
    print(f"Underflow example: determinant 0, log magnitude {log_magnitude:.3f}")


if __name__ == "__main__":
    main()
