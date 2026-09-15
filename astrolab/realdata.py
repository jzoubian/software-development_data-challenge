"""Fetch a real telescope image - the "hero image" bonus feature.

Unlike astrolab.synth (deterministic, no network), this queries a real
public sky-survey archive live via astroquery. That's a deliberate
contrast with the rest of the pipeline: it raises the reproducibility
question modules 2/3 talk about explicitly - pin the survey name,
target, and image size, and consider caching the result to disk, so a
network hiccup during the workshop doesn't block the demo.

Confirmed working during course prep:

    from astroquery.skyview import SkyView
    imgs = SkyView.get_images(position="M42", survey=["DSS"], pixels=200)
    imgs[0][0].data  # -> a 2D numpy array, dtype float32

TODO(backlog): implement fetch_sky_image below, returning a plain 2D
numpy array so it can flow through the same detect_sources /
measure_photometry / compose_image steps as a stacked synthetic frame.
"""

from pathlib import Path

import numpy as np


DEFAULT_TARGET = "M42"  # the Orion Nebula - bright, iconic, DSS-covered
DEFAULT_SURVEY = "DSS"
DEFAULT_PIXELS = 200

CACHE_DIR = Path("data/real")


def fetch_sky_image(position=DEFAULT_TARGET, survey=DEFAULT_SURVEY, pixels=DEFAULT_PIXELS):
    """Fetch a real image of the sky around ``position`` from a public
    archive (the Digitized Sky Survey, via astroquery's SkyView client).

    The downloaded image is cached as a .npy file so that subsequent
    calls do not need network access.
    """
    cache_file = CACHE_DIR / f"{position}_{survey}_{pixels}.npy"

    if cache_file.exists():
        return np.load(cache_file)

    from astroquery.skyview import SkyView

    imgs = SkyView.get_images(
        position=position,
        survey=[survey],
        pixels=pixels,
    )

    image = imgs[0][0].data

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    np.save(cache_file, image)

    return image