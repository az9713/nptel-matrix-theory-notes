"""Verify unconstrained and constrained inference in the sensor model."""

import numpy as np


def main():
    epsilon = 0.02
    a = np.array([[1, 1, 0], [1, 1, 0], [0, 0, epsilon], [0, 0, 0]])
    b = np.array([2, 2, 1, 1])
    b_matrix = np.array([[0, 0, 1]])
    inverse = np.linalg.pinv(a)
    observation_projector = a @ inverse
    command_projector = inverse @ a
    assert np.allclose(observation_projector @ a, a)
    assert np.allclose(command_projector @ inverse, inverse)
    assert np.allclose(observation_projector, observation_projector.T)
    assert np.allclose(command_projector, command_projector.T)

    unbounded = inverse @ b
    residual = a @ unbounded - b
    assert np.allclose(unbounded, [1, 1, 50])
    assert np.allclose(a.T @ residual, 0)

    multiplier = epsilon / 2 - epsilon**2
    penalized = np.vstack([a, np.sqrt(multiplier) * b_matrix])
    bounded = np.linalg.lstsq(penalized, np.append(b, 0), rcond=None)[0]
    bounded_residual = a @ bounded - b
    assert np.allclose(bounded, [1, 1, 2])
    assert np.isclose(np.linalg.norm(b_matrix @ bounded), 2)
    assert np.isclose(residual @ residual, 1)
    assert np.isclose(bounded_residual @ bounded_residual, 1.9216)
    assert np.allclose(
        a.T @ bounded_residual + multiplier * b_matrix.T @ b_matrix @ bounded,
        0,
    )
    print(f"Unconstrained x3 = {unbounded[2]:g}, bounded x3 = {bounded[2]:g}.")
    print(f"Squared residuals: {residual @ residual:g}, "
          f"{bounded_residual @ bounded_residual:g}.")


if __name__ == "__main__":
    main()
