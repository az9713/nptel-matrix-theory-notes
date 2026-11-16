"""Reproduce the device's composition and basis-change identities."""

import numpy as np


def main():
    device = np.array([[1, 1], [1, -1]])
    reporter = np.diag([2, 1])
    basis = np.array([[1, 1], [-1, 1]])
    basis_coordinates = np.array([1, 2])
    command = basis @ basis_coordinates
    assert np.array_equal(command, [3, 1])
    measurement = device @ command
    assert np.array_equal(measurement, (device @ basis) @ basis_coordinates)
    assert np.array_equal(measurement, [4, 2])
    assert np.array_equal(reporter @ measurement, [8, 2])
    assert np.array_equal(device @ (reporter @ command), [7, 5])
    assert np.trace(reporter @ device) == np.trace(device @ reporter) == 1

    changed_operator = np.linalg.solve(basis, device @ basis)
    assert np.allclose(basis @ changed_operator, device @ basis)
    assert np.isclose(np.trace(changed_operator), np.trace(device))
    print(f"Command {command.tolist()} produces {measurement.tolist()}.")
    print(f"Basis images: {(device @ basis).tolist()}.")


if __name__ == "__main__":
    main()
