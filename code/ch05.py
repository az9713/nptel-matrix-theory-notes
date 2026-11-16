"""Check residual optimization and sharp vector norm comparisons."""

import numpy as np


def main():
    certificate = np.array([-2, -1, 1])
    l1_residual = np.array([-0.5, 0, 0])
    l2_residual = certificate / (certificate @ certificate)
    linf_residual = np.sign(certificate) / np.linalg.norm(certificate, 1)
    for order, candidate, dual_order in (
        (1, l1_residual, np.inf), (2, l2_residual, 2),
        (np.inf, linf_residual, 1)
    ):
        lower_bound = 1 / np.linalg.norm(certificate, dual_order)
        assert np.isclose(certificate @ candidate, 1)
        assert np.isclose(np.linalg.norm(candidate, order), lower_bound)
        print(f"p = {order}: residual {candidate}, optimum {lower_bound:.6f}")

    for vector in (np.eye(9)[0], np.ones(9), np.arange(1, 10)):
        l1 = np.linalg.norm(vector, 1)
        l2 = np.linalg.norm(vector, 2)
        assert l2 <= l1 <= 3 * l2

    flat = np.full(1024, 1 / 1024)
    assert np.linalg.norm(flat, 1) == 1
    assert np.linalg.norm(flat, np.inf) == 1 / 1024
    print("Flat vector in dimension 1024: norm ratio 1024.")


if __name__ == "__main__":
    main()
