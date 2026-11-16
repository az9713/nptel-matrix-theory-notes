"""Build the SVD geometry and constrained-fit figures."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
INK = "#e9edf3"
ACCENT = "#89d7f8"
PANEL = "#17202d"
EPSILON = 0.02


def figure():
    fig, ax = plt.subplots(figsize=(7.6, 3.8), layout="constrained")
    fig.patch.set_facecolor(PANEL)
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=INK)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)
    for spine in ax.spines.values():
        spine.set_color("#68798f")
    ax.grid(alpha=0.19)
    return fig, ax


def save(fig, stem):
    fig.savefig(ROOT / f"assets/{stem}.png", dpi=150, metadata={"Software": "Matplotlib"})
    plt.close(fig)


def main():
    cmap = np.diag([2.0, EPSILON])
    theta = np.linspace(0, 2 * np.pi, 361)
    directions = np.stack([np.cos(theta), np.sin(theta)])
    image = cmap @ directions
    assert np.allclose(np.sum((np.linalg.solve(cmap, image))**2, axis=0), 1)
    dpi_note = "Vertical range is 100× smaller"
    fig, ax = figure()
    ax.plot(*image, color=ACCENT, lw=2.6)
    ax.fill(*image, color=ACCENT, alpha=0.16)
    ax.set_xlabel("Output along the duplicate sum")
    ax.set_ylabel("Output along the weak channel")
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-0.0215, 0.0215)
    ax.set_title(dpi_note, color=INK)
    save(fig, "svd-ellipse")

    values = np.linspace(-5, 54, 591)
    residuals = 1 + (EPSILON * values - 1)**2
    assert np.isclose(1 + (EPSILON * 2 - 1)**2, 1.9216)
    fig, ax = figure()
    ax.axvspan(-2, 2, color=ACCENT, alpha=0.2, label="Allowed commands")
    ax.plot(values, residuals, color=ACCENT, lw=2.4)
    ax.scatter([2, 50], [1.9216, 1], s=42, color="#ffca9b", zorder=3)
    ax.annotate("Bounded fit (2, 1.9216)", (2, 1.9216), (7, 2.05), color=INK)
    ax.annotate("Unbounded fit (50, 1)", (50, 1), (28, 1.13), color=INK)
    ax.set_xlabel("Weak actuator command")
    ax.set_ylabel("Squared residual")
    ax.legend(labelcolor=INK, facecolor=PANEL, edgecolor="#68798f")
    save(fig, "constrained-fit")


if __name__ == "__main__":
    main()
