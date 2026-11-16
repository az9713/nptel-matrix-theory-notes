"""Check a modal prediction and its repeated-root limit."""

import numpy as np


def main():
    a = np.array([[0.8, 0.3], [0.0, 0.5]])
    basis = np.array([[1.0, -1.0], [0.0, 1.0]])
    diagonal = np.diag([0.8, 0.5])
    assert np.allclose(a @ basis, basis @ diagonal)
    assert np.allclose(np.poly(a), [1.0, -1.3, 0.4])
    initial = np.array([0.0, 1.0])
    steps = 10
    weights = np.linalg.solve(basis, initial)
    prediction = basis @ (np.diag(diagonal)**steps * weights)
    assert np.allclose(np.linalg.matrix_power(a, steps) @ initial,
                       prediction)
    repeated = np.array([[0.8, 0.3], [0.0, 0.8]])
    transient = np.linalg.matrix_power(repeated, steps) @ initial
    assert np.isclose(transient[0], steps * 0.3 * 0.8**(steps - 1))
    assert np.linalg.matrix_rank(repeated - 0.8 * np.eye(2)) == 1
    print(f"distinct roots: {prediction[0]:.8f}, {prediction[1]:.8f}")
    print(f"repeated root:  {transient[0]:.8f}, {transient[1]:.8f}")


if __name__ == "__main__":
    main()
