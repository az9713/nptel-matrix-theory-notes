"""Check the actuator stiffness model and its complex phase transform."""

import numpy as np


def main():
    h = np.array([[3.0, -1.0], [-1.0, 5.0]])
    expected = 4 + np.sqrt(2) * np.array([-1.0, 1.0])
    values = np.linalg.eigvalsh(h)
    np.testing.assert_allclose(values, expected, atol=1e-12, rtol=0)

    trial = np.array([2.0, 1.0])
    quotient = np.vdot(trial, h @ trial) / np.vdot(trial, trial)
    residual = np.linalg.norm(h @ trial - quotient * trial)
    relative_residual = residual / np.linalg.norm(trial)
    np.testing.assert_allclose(quotient, 2.6, atol=1e-12, rtol=0)
    np.testing.assert_allclose(relative_residual, 0.2, atol=1e-12, rtol=0)
    assert min(abs(values - quotient)) <= relative_residual

    phase = np.diag([1, 1j])
    g = phase @ h @ phase.conj().T
    np.testing.assert_allclose(g, g.conj().T, atol=1e-12, rtol=0)
    new_values, modes = np.linalg.eigh(g)
    np.testing.assert_allclose(new_values, expected, atol=1e-12, rtol=0)
    np.testing.assert_allclose(
        g @ modes, modes * new_values, atol=1e-12, rtol=0
    )

    print(f"Stiffness spectrum (ascending): {values}")
    print(f"Trial quotient: {quotient:.3f}; residual: {relative_residual:.3f}")


if __name__ == "__main__":
    main()
