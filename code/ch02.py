"""Verify four subspaces and rank changes in the calibration example."""

import numpy as np


def main():
    matrix = np.array([[1, 0, 1, 2], [0, 1, 1, -1], [1, 1, 2, 1]])
    image_basis = matrix[:, :2]
    row_basis = matrix[:2, :].T
    kernel_basis = np.array([[-1, -1, 1, 0], [-2, 1, 0, 1]]).T
    left_null = np.array([-1, -1, 1])

    np.testing.assert_array_equal(image_basis @ row_basis.T, matrix)
    np.testing.assert_array_equal(matrix @ kernel_basis, np.zeros((3, 2)))
    np.testing.assert_array_equal(matrix.T @ left_null, np.zeros(4))
    assert np.linalg.matrix_rank(image_basis) == 2
    assert np.linalg.matrix_rank(row_basis) == 2
    assert np.linalg.matrix_rank(kernel_basis) == 2
    assert np.linalg.matrix_rank(matrix) == 2

    target = np.array([2, 1, 3])
    observable = np.array([7, 8, 15, 6]) / 17
    np.testing.assert_allclose(matrix @ observable, target)
    np.testing.assert_allclose(kernel_basis.T @ observable, 0, atol=1e-14)
    assert left_null @ target == 0
    assert left_null @ np.array([2, 1, 4]) == 1

    command_basis = np.column_stack((np.eye(4)[:, 0], kernel_basis[:, 0]))
    assert np.linalg.matrix_rank(command_basis) == 2
    assert np.linalg.matrix_rank(matrix @ command_basis) == 1

    perturbed = matrix.astype(float)
    perturbed[2, 3] += 1e-8
    assert np.linalg.matrix_rank(perturbed, tol=1e-10) == 3
    assert np.linalg.matrix_rank(perturbed, tol=1e-6) == 2
    print("Compatible command numerator:", (17 * observable).round())
    print("Smallest perturbed singular value:", np.linalg.svd(
        perturbed, compute_uv=False
    )[-1])
    print("Perturbed rank: 3 at tolerance 1e-10, 2 at tolerance 1e-6.")


if __name__ == "__main__":
    main()
