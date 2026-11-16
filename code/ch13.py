"""Check Jordan chain sizes, powers and polynomial evaluation."""

from math import comb

import numpy as np


def main():
    nilpotent = np.diag(np.ones(2), 1)
    identity = np.eye(3)
    decay = 0.9
    block = decay * identity + nilpotent
    nullities = [3 - int(np.linalg.matrix_rank(
        np.linalg.matrix_power(nilpotent, k))) for k in range(4)]
    assert nullities == [0, 1, 2, 3]
    steps = 20
    analytic = sum(comb(steps, j) * decay**(steps - j)
                   * np.linalg.matrix_power(nilpotent, j)
                   for j in range(3))
    np.testing.assert_allclose(np.linalg.matrix_power(block, steps),
                               analytic)
    squared = decay**2 * identity + 2 * decay * nilpotent
    squared += nilpotent @ nilpotent
    np.testing.assert_allclose(block @ block, squared)
    perturbed = block.copy()
    perturbed[2, 0] = 1e-6
    shifts = np.linalg.eigvals(perturbed) - decay
    np.testing.assert_allclose(np.abs(shifts), 0.01)
    print(f"nullity profile: {nullities}")
    print(f"step-20 transfer: {analytic[0, 2]:.6f}")
    print(f"perturbation shift radius: {max(abs(shifts)):.6f}")


if __name__ == "__main__":
    main()
