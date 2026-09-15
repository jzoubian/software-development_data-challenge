"""Pipeline orchestration - the shared entry point everyone's work plugs into."""

import numpy as np
import pandas as pd

from astrolab.io import load_frame_set
from astrolab.realdata import fetch_sky_image
from astrolab.synth import SAMPLE_FRAMES_DIR, regenerate_sample_data


def _ensure_sample_frames():
    """Generate the sample frames if missing."""
    if not SAMPLE_FRAMES_DIR.is_dir() or not any(SAMPLE_FRAMES_DIR.glob("*.npy")):
        regenerate_sample_data()


def stack_frames(frames):
    """Combine several noisy frames using mean stacking."""
    if not frames:
        raise ValueError("frames must not be empty")

    return np.mean(np.stack(frames), axis=0)


def detect_sources(frame):
    """Find bright point sources using thresholding and local maxima."""
    frame = np.asarray(frame)

    background = np.median(frame)
    noise = np.std(frame)
    threshold = background + 5 * noise

    candidates = frame > threshold

    padded = np.pad(frame, 1, mode="edge")
    local_maximum = np.ones_like(frame, dtype=bool)

    for dy in range(3):
        for dx in range(3):
            if dx == 1 and dy == 1:
                continue

            neighbour = padded[dy:dy + frame.shape[0], dx:dx + frame.shape[1]]
            local_maximum &= frame >= neighbour

    ys, xs = np.where(candidates & local_maximum)

    return list(zip(xs.tolist(), ys.tolist()))


def measure_photometry(frame, sources):
    """Measure source brightness using simple aperture photometry."""
    frame = np.asarray(frame)
    background = np.median(frame)

    rows = []

    for source_id, (x, y) in enumerate(sources):
        y_min = max(0, y - 2)
        y_max = min(frame.shape[0], y + 3)
        x_min = max(0, x - 2)
        x_max = min(frame.shape[1], x + 3)

        aperture = frame[y_min:y_max, x_min:x_max]
        flux = float(np.sum(aperture - background))

        rows.append(
            {
                "source": source_id,
                "x": x,
                "y": y,
                "flux": flux,
            }
        )

    return pd.DataFrame(rows, columns=["source", "x", "y", "flux"])


def compose_image(frame):
    """Apply contrast stretching and return a display-ready image."""
    frame = np.asarray(frame, dtype=float)

    low = np.percentile(frame, 1)
    high = np.percentile(frame, 99)

    if high <= low:
        return np.zeros_like(frame, dtype=np.uint8)

    image = np.clip((frame - low) / (high - low), 0, 1)
    return (image * 255).astype(np.uint8)


def run(real=False):
    """Run the full pipeline using synthetic or real sky data."""
    if real:
        print("Loading real sky image...")
        frame = fetch_sky_image()
        print(f"  loaded real image of shape {frame.shape}")
    else:
        print("Loading frames...")
        _ensure_sample_frames()
        frames = load_frame_set()
        print(f"  loaded {len(frames)} frames of shape {frames[0].shape}")

        print("Stacking frames...")
        frame = stack_frames(frames)

    print("Detecting sources...")
    sources = detect_sources(frame)
    print(f"  found {len(sources)} sources")

    print("Measuring photometry...")
    table = measure_photometry(frame, sources)
    print(table)

    print("Composing final image...")
    return compose_image(frame)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--real",
        action="store_true",
        help="Use the cached or downloaded real sky image",
    )
    args = parser.parse_args()

    run(real=args.real)
