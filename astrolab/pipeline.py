"""Pipeline orchestration - the shared entry point everyone's work plugs into.

This file is intentionally incomplete: most steps below are stubs. Each
stub is a task in the Session 5 backlog (see 5-data-challenge/README.md
in the course repo). Expect this file to be a frequent source of merge
conflicts during the Day 2 integration session - that's by design, not a
bug: it's the one place every team's PR touches.
"""

import numpy as np

from astrolab.io import load_frame_set
from astrolab.synth import SAMPLE_FRAMES_DIR, regenerate_sample_data


def _ensure_sample_frames():
    """Generate the sample frames if missing.

    data/frames/ is gitignored (generated, not source) - a fresh clone or
    fork starts without it, so regenerate deterministically from the same
    seed rather than requiring a manual step.
    """
    if not SAMPLE_FRAMES_DIR.is_dir() or not any(SAMPLE_FRAMES_DIR.glob("*.npy")):
        regenerate_sample_data()


def stack_frames(frames):
    """Combine several noisy frames of the same field into one.

    TODO(backlog): implement mean or median stacking to reduce noise.
    """
    raise NotImplementedError("stack_frames: implement frame stacking")


def detect_sources(frame):
    """Find point sources (stars) in a frame.

    TODO(backlog): implement threshold + local-maxima detection,
    returning a list of (x, y) pixel coordinates.
    """
    raise NotImplementedError("detect_sources: implement source detection")


def _aperture_sum(frame, x, y, radius=2):
    """Sum pixels in a circular aperture centered at ``(x, y)``."""
    if radius < 0:
        raise ValueError("radius must be non-negative")

    height, width = frame.shape
    x = int(round(x))
    y = int(round(y))
    x_start = max(0, x - radius)
    x_stop = min(width, x + radius + 1)
    y_start = max(0, y - radius)
    y_stop = min(height, y + radius + 1)

    aperture_y, aperture_x = np.mgrid[y_start:y_stop, x_start:x_stop]
    aperture_x -= x
    aperture_y -= y
    mask = aperture_x**2 + aperture_y**2 <= radius**2
    return frame[y_start:y_stop, x_start:x_stop][mask].sum()


def measure_photometry(frame, sources):
    """Measure the brightness of each detected source.

    Return ``(x, y, flux)`` records for each source. Table construction can
    be layered on top of these measurements by the pipeline integration step.
    """
    return [(x, y, _aperture_sum(frame, x, y)) for x, y in sources]


def compose_image(frame):
    """Turn a raw frame into a nice display image.

    TODO(backlog): implement contrast stretching / a false-color
    composite for the final "hero image".
    """
    raise NotImplementedError("compose_image: implement display composition")


def run():
    """Run the full pipeline end to end, printing progress as it goes."""
    print("Loading frames...")
    _ensure_sample_frames()
    frames = load_frame_set()
    print(f"  loaded {len(frames)} frames of shape {frames[0].shape}")

    print("Stacking frames...")
    stacked = stack_frames(frames)

    print("Detecting sources...")
    sources = detect_sources(stacked)
    print(f"  found {len(sources)} sources")

    print("Measuring photometry...")
    table = measure_photometry(stacked, sources)
    print(table)

    print("Composing final image...")
    return compose_image(stacked)


if __name__ == "__main__":
    run()
