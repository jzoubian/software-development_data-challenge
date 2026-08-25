"""Synthetic star-field generation.

Frames are generated deterministically from a seed, so every team starts
from byte-identical data with no download required.
"""

from pathlib import Path

import numpy as np

FRAME_SHAPE = (128, 128)
DEFAULT_N_STARS = 25
DEFAULT_NOISE_SIGMA = 5.0
DEFAULT_BACKGROUND = 10.0

SAMPLE_SEED = 42
SAMPLE_N_FRAMES = 5
SAMPLE_FRAMES_DIR = Path(__file__).resolve().parent.parent / "data" / "frames"


def _generate_stars(shape, n_stars, rng):
    """Return (positions, amplitudes, sigmas) describing a field of stars."""
    height, width = shape
    positions = rng.uniform(low=[0, 0], high=[width, height], size=(n_stars, 2))
    amplitudes = rng.uniform(50.0, 255.0, size=n_stars)
    sigmas = rng.uniform(1.0, 2.5, size=n_stars)
    return positions, amplitudes, sigmas


def _render(shape, positions, amplitudes, sigmas, background, noise_sigma, rng):
    height, width = shape
    ys, xs = np.mgrid[0:height, 0:width]
    frame = np.full(shape, background, dtype=np.float64)
    for (cx, cy), amplitude, sigma in zip(positions, amplitudes, sigmas):
        frame += amplitude * np.exp(-(((xs - cx) ** 2 + (ys - cy) ** 2) / (2 * sigma**2)))
    frame += rng.normal(loc=0.0, scale=noise_sigma, size=shape)
    return frame


def generate_star_field(
    shape=FRAME_SHAPE,
    n_stars=DEFAULT_N_STARS,
    seed=0,
    noise_sigma=DEFAULT_NOISE_SIGMA,
    background=DEFAULT_BACKGROUND,
):
    """Generate a single synthetic noisy star-field frame.

    Deterministic: the same ``seed`` always produces the same frame.

    >>> frame = generate_star_field(shape=(32, 32), n_stars=3, seed=1)
    >>> frame.shape
    (32, 32)
    """
    rng = np.random.default_rng(seed)
    positions, amplitudes, sigmas = _generate_stars(shape, n_stars, rng)
    return _render(shape, positions, amplitudes, sigmas, background, noise_sigma, rng)


def generate_frame_set(
    n_frames=5,
    shape=FRAME_SHAPE,
    n_stars=DEFAULT_N_STARS,
    seed=0,
    noise_sigma=DEFAULT_NOISE_SIGMA,
    background=DEFAULT_BACKGROUND,
):
    """Generate several noisy exposures of the *same* field.

    Star positions/brightnesses are fixed once from ``seed``; each frame
    gets an independent noise draw. This is the input for the frame
    stacking task: averaging the frames should recover the field with a
    better signal-to-noise ratio than any single exposure.

    >>> frames = generate_frame_set(n_frames=3, shape=(32, 32), n_stars=3, seed=1)
    >>> len(frames)
    3
    >>> frames[0].shape
    (32, 32)
    """
    field_rng = np.random.default_rng(seed)
    positions, amplitudes, sigmas = _generate_stars(shape, n_stars, field_rng)

    frames = []
    for i in range(n_frames):
        noise_rng = np.random.default_rng(seed * 1000 + i + 1)
        frames.append(_render(shape, positions, amplitudes, sigmas, background, noise_sigma, noise_rng))
    return frames


def regenerate_sample_data():
    """Regenerate data/frames/*.npy - the committed sample dataset.

    Deterministic (SAMPLE_SEED): re-running this reproduces byte-identical
    files, so it's safe to re-run but nobody needs to.
    """
    from astrolab.io import save_frame

    frames = generate_frame_set(n_frames=SAMPLE_N_FRAMES, seed=SAMPLE_SEED)
    for i, frame in enumerate(frames):
        save_frame(SAMPLE_FRAMES_DIR / f"frame_{i:02d}.npy", frame)
    print(f"wrote {len(frames)} frames to {SAMPLE_FRAMES_DIR}")


if __name__ == "__main__":
    regenerate_sample_data()
