"""Compare short matrix recurrences and orthogonal factorizations."""

import numpy as np


def main():
    a = np.array([[0.8, 3.0], [0.0, 0.5]])
    identity = np.eye(2)
    np.testing.assert_allclose(a @ a - 1.3 * a + 0.4 * identity, 0,
                               atol=1e-14)
    shift = 1.0
    inverse = ((shift - 1.3) * identity + a)
    inverse /= (shift - 0.8) * (shift - 0.5)
    np.testing.assert_allclose((shift * identity - a) @ inverse, identity,
                               atol=1e-14)
    commutator = a.T @ a - a @ a.T
    rotation = np.array([[3.0, -4.0], [4.0, 3.0]]) / 5
    rotated = rotation @ a @ rotation.T
    q, r = np.linalg.qr(rotated)
    np.testing.assert_allclose(q @ r, rotated)
    np.testing.assert_allclose(q.T @ q, identity, atol=1e-14)
    np.testing.assert_allclose(r @ q, q.T @ rotated @ q, atol=1e-14)
    eigenvector = np.array([1.0, 0.0])
    assert not np.allclose(a.T @ eigenvector, 0.8 * eigenvector)
    assert np.isclose(np.linalg.norm(inverse @ [0, 1]), np.sqrt(904))
    print(f"resolvent response norm: {np.linalg.norm(inverse @ [0, 1]):.6f}")
    print(f"normality defect (Frobenius): {np.linalg.norm(commutator):.6f}")


if __name__ == "__main__":
    main()
