"""Pipeline orchestration - the shared entry point everyone's work plugs into.

This file is intentionally incomplete: most steps below are stubs. Each
stub is a task in the Session 5 backlog (see 5-data-challenge/README.md
in the course repo). Expect this file to be a frequent source of merge
conflicts during the Day 2 integration session - that's by design, not a
bug: it's the one place every team's PR touches.
"""

from astrolab.io import load_frame_set


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


def measure_photometry(frame, sources):
    """Measure the brightness of each detected source.

    TODO(backlog): implement simple aperture photometry, returning a
    table (e.g. a pandas DataFrame) of source -> flux.
    """
    raise NotImplementedError("measure_photometry: implement aperture photometry")


def compose_image(frame):
    """Turn a raw frame into a nice display image.

    TODO(backlog): implement contrast stretching / a false-color
    composite for the final "hero image".
    """
    raise NotImplementedError("compose_image: implement display composition")


def run():
    """Run the full pipeline end to end, printing progress as it goes."""
    print("Loading frames...")
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
