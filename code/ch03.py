"""Check weighted and complex Gram–Schmidt, plus loss of orthogonality."""

import numpy as np


def gram_schmidt(matrix, weight, modified):
    """Return thin Q, R for independent columns in a positive metric."""
    rows, cols = matrix.shape
    dtype = np.result_type(matrix, weight, float)
    q = np.zeros((rows, cols), dtype=dtype)
    r = np.zeros((cols, cols), dtype=dtype)
    for j, column in enumerate(matrix.T):
        remainder = column.astype(dtype)
        for i in range(j):
            source = remainder if modified else column
            r[i, j] = np.vdot(q[:, i], weight @ source)
            remainder -= q[:, i] * r[i, j]
        magnitude = np.sqrt(np.vdot(remainder, weight @ remainder).real)
        if magnitude <= 0:
            raise ValueError("Cannot normalize a zero remainder.")
        r[j, j] = magnitude
        q[:, j] = remainder / magnitude
    return q, r


def main():
    calibration = np.array([[1, 0], [0, 1], [1, 1]])
    weight = np.diag([1, 1, 4])
    readings = np.array([2, 1, 4])
    q, r = gram_schmidt(calibration, weight, modified=True)
    np.testing.assert_allclose(q.T @ weight @ q, np.eye(2), atol=1e-14)
    np.testing.assert_allclose(q @ r, calibration, atol=1e-14)
    fitted = q @ (q.T @ weight @ readings)
    np.testing.assert_allclose(fitted, np.array([22, 13, 35]) / 9)
    np.testing.assert_allclose(
        calibration.T @ weight @ (readings - fitted), 0, atol=1e-14
    )

    complex_matrix = np.array([[1, 1j], [1j, 2], [-1, 1 + 1j]])
    q, r = gram_schmidt(complex_matrix, np.eye(3), modified=True)
    np.testing.assert_allclose(q.conj().T @ q, np.eye(2), atol=1e-14)
    np.testing.assert_allclose(q @ r, complex_matrix, atol=1e-14)

    sensitive = np.vstack((np.ones((1, 4)), 1e-8 * np.eye(4)))
    defects = []
    print("Weighted projection:", fitted)
    for modified in (False, True):
        q, r = gram_schmidt(sensitive, np.eye(5), modified)
        reconstruction = np.linalg.norm(q @ r - sensitive)
        orthogonality = np.linalg.norm(q.T @ q - np.eye(4))
        defects.append(orthogonality)
        assert reconstruction < 1e-14
        label = "Modified" if modified else "Classical"
        print(f"{label}: reconstruction {reconstruction:.3e}, "
              f"orthogonality defect {orthogonality:.3e}")
    assert defects[1] < 1e-6
    assert defects[0] > 1e6 * defects[1]


if __name__ == "__main__":
    main()
