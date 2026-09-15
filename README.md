# Astro Data Challenge

Build a tiny astronomy-image pipeline as a team.

## Mission

Turn five noisy exposures of the same star field into one clean composite
image, with a table showing the brightness of every detected source.

```text
load frames → stack/denoise → detect sources → measure photometry → composite
```

## Status

The core image pipeline is implemented.

The pipeline can:

1. Load five synthetic image frames.
2. Combine the frames using mean stacking.
3. Detect bright sources using thresholding and local maxima.
4. Measure source brightness using simple aperture photometry.
5. Create a display-ready image using contrast stretching.

The project also includes an optional real-sky bonus feature. This downloads
an image from the Digitized Sky Survey using `astroquery` and sends it through
the same source-detection, photometry, and image-composition steps.

## Installation

Use Python 3.10 or newer.

Install the required packages:

```sh
pip install numpy pandas matplotlib astroquery
```

## Quickstart

Run the normal synthetic pipeline:

```sh
python -m astrolab.pipeline
```

The synthetic pipeline automatically generates the sample frames if they are
missing. The generated data is deterministic and does not require internet
access.

The pipeline performs the following steps:

```text
Loading frames
    ↓
Stacking frames
    ↓
Detecting sources
    ↓
Measuring photometry
    ↓
Composing final image
```

## Real-sky bonus feature

Run the real-sky pipeline with:

```sh
python -m astrolab.pipeline --real
```

The real-sky pipeline fetches an image of M42, the Orion Nebula, from the
Digitized Sky Survey using `astroquery.skyview`.

The image is saved as a NumPy `.npy` file in:

```text
data/real/
```

If the cached file already exists, the pipeline loads it instead of making
another network request.

### Reproducibility and network trade-off

The normal synthetic pipeline is deterministic and works offline. It uses
generated sample frames with a fixed seed, so the same data can be recreated
consistently.

The real-sky pipeline depends on:

- An internet connection for the first download.
- The availability of the remote SkyView service.
- The selected target, survey, and image size.

After the first successful download, the image is cached locally. This makes
later runs faster and reduces dependence on the network.

The real-sky image is not guaranteed to be identical to every future remote
request unless the cached `.npy` file is preserved.

## Code layout

- `astrolab/synth.py` — deterministic synthetic star-field generator.
- `astrolab/io.py` — loading and saving NumPy frame files.
- `astrolab/pipeline.py` — orchestrates the full image-processing pipeline.
- `astrolab/realdata.py` — downloads and caches a real sky image using
  `astroquery.skyview`.
- `data/frames/*.npy` — generated synthetic image frames.
- `data/real/*.npy` — cached real-sky images.
- `notebooks/explore_frames.ipynb` — loads and plots the sample frames for
  exploration.

## Pipeline functions

The main functions in `astrolab.pipeline` are:

- `stack_frames(frames)` — combines multiple frames using mean stacking.
- `detect_sources(frame)` — finds bright sources using a threshold and local
  maximum detection.
- `measure_photometry(frame, sources)` — calculates the brightness of each
  detected source.
- `compose_image(frame)` — applies contrast stretching and returns a
  display-ready image.
- `run(real=False)` — runs the complete pipeline using either synthetic frames
  or a real sky image.

## Running the two pipeline modes

### Synthetic mode

```sh
python -m astrolab.pipeline
```

This mode uses the generated sample frames and does not require internet
access.

### Real-sky mode

```sh
python -m astrolab.pipeline --real
```

This mode uses the cached real image if available. If no cached image exists,
it downloads the image from SkyView and saves it under `data/real`.

## Development

Check the current Git status:

```sh
git status
```

View the changes made locally:

```sh
git diff
```

Run the available tests:

```sh
pytest
```

If pytest reports:

```text
collected 0 items
no tests ran
```

the repository currently contains no test files, so pytest has not executed
any tests.

## Team workflow

Each team works on its own Git branch. Changes to shared files such as
`astrolab/pipeline.py` and `README.md` may cause merge conflicts during
integration. These conflicts are expected because multiple tasks intentionally
modify the same files.

Before submitting the work:

```sh
git add astrolab/pipeline.py astrolab/realdata.py README.md
git commit -m "Implement real sky image pipeline"
git push -u origin task-3-real-pipeline
```

Then open a pull request on GitHub for the team’s branch.

## License

GPLv3 — see `LICENSE`.
