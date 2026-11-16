"""Check singular gains, null spaces, and truncation for a four-channel model."""

import numpy as np


def main():
    epsilon = 0.02
    a = np.array([[1, 1, 0], [1, 1, 0], [0, 0, epsilon], [0, 0, 0]])
    u, singular, vh = np.linalg.svd(a, full_matrices=True)
    v = vh.T
    rank = 2
    reconstruction = (u[:, :rank] * singular[:rank]) @ vh[:rank]
    truncated = singular[0] * np.outer(u[:, 0], vh[0])
    invisible = np.array([1, -1, 0]) / np.sqrt(2)
    null_projector = v[:, rank:] @ v[:, rank:].T
    assert np.allclose(singular, [2, epsilon, 0])
    assert np.allclose(a, reconstruction)
    assert np.allclose(a @ v[:, rank:], 0)
    assert np.allclose(u[:, rank:].T @ a, 0)
    assert np.allclose(null_projector, np.outer(invisible, invisible))
    error = np.linalg.norm(a - truncated, ord=2)
    ratio = singular[0] / singular[1]
    assert np.isclose(error, epsilon)
    assert np.isclose(ratio, 100)
    print(f"Nonzero gains: {singular[0]:g}, {singular[1]:g}")
    print(f"Rank-one error: {error:g}. Observable gain ratio: {ratio:g}.")


if __name__ == "__main__":
    main()
