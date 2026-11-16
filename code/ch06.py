"""Check complex dual attainment and induced matrix norms."""

import numpy as np


def main():
    y = np.array([2j, -1, 1 + 1j])
    p = 3
    q = p / (p - 1)
    y_q = np.linalg.norm(y, q)
    maximizer = (y / np.abs(y)) * (np.abs(y) / y_q) ** (q - 1)
    assert np.isclose(np.linalg.norm(maximizer, p), 1)
    assert np.isclose(np.vdot(y, maximizer), y_q)
    print(f"Complex dual norm at p={p}: {y_q:.6f}")

    calibration = np.array([[1, 0], [0, 1], [1, 1]])
    for order, witness, expected in (
        (1, [1, 0], 2), (2, [1, 1], np.sqrt(3)), (np.inf, [1, 1], 2)
    ):
        witness = np.array(witness)
        induced = np.linalg.norm(calibration, order)
        attained = np.linalg.norm(calibration @ witness, order)
        attained /= np.linalg.norm(witness, order)
        assert np.isclose(attained, induced)
        assert np.isclose(induced, expected)
        print(f"Induced p={order}: {induced:.6f}")

    ones = np.ones((3, 3))
    assert np.max(ones) == 1
    assert np.max(ones @ ones) == 3


if __name__ == "__main__":
    main()
