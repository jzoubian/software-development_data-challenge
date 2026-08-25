"""Loading and saving frames.

Frames are plain 2D numpy arrays stored as .npy files - no image-library
dependency required for the foundation layer.
"""

from pathlib import Path

import numpy as np

DEFAULT_FRAMES_DIR = Path(__file__).resolve().parent.parent / "data" / "frames"


def load_frame(path):
    """Load a single frame from a .npy file.

    >>> import numpy as np, tempfile
    >>> from pathlib import Path
    >>> with tempfile.TemporaryDirectory() as tmp:
    ...     p = Path(tmp) / "frame.npy"
    ...     np.save(p, np.ones((4, 4)))
    ...     load_frame(p).shape
    (4, 4)
    """
    return np.load(path)


def load_frame_set(directory=DEFAULT_FRAMES_DIR, pattern="*.npy"):
    """Load every frame in ``directory`` matching ``pattern``, sorted by filename."""
    directory = Path(directory)
    paths = sorted(directory.glob(pattern))
    if not paths:
        raise FileNotFoundError(f"no frames found in {directory} matching {pattern!r}")
    return [load_frame(p) for p in paths]


def save_frame(path, frame):
    """Save a single frame to a .npy file, creating parent directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(path, frame)
