# Astro Data Challenge

Build a tiny astro-image pipeline, together, as a team, over one evening
and one morning.

**Mission**: turn 5 noisy exposures of the same star field into one clean,
nice-looking composite image, with a table of the brightness of every
star found along the way.

```
load frames → stack/denoise → detect sources → measure photometry → composite
```

## Status: foundation layer only, on purpose

This repo currently contains just enough to load the sample frames and
watch the pipeline stop at the first unimplemented step. That's
intentional: there's no environment spec, no CI, no docs, no tests, and
most of the actual pipeline is missing. Those gaps are the workshop
backlog — see the course repo's `5-data-challenge/README.md` for the full
task list, team workflow, and schedule.

## Quickstart

Use the Conda/Miniforge environment spec to create an isolated Python
3.10+ environment with the core workshop dependencies:

```sh
conda env create -f environment.yml
conda activate astro-data-challenge
python -m astrolab.pipeline
```

If you want to try the optional live-sky bonus in `astrolab.realdata`,
install `astroquery` separately so the core offline pipeline stays lean:

```sh
conda install -n astro-data-challenge -c conda-forge 'astroquery>=0.4,<1'
```

You should see it load the 5 sample frames and then stop with:

```
NotImplementedError: stack_frames: implement frame stacking
```

That's expected — you've just reached backlog item #1.

## Code layout

- `astrolab/synth.py` — deterministic synthetic star-field generator
  (no download needed; same seed always produces the same data).
- `astrolab/io.py` — loading/saving frames (`.npy` files, numpy arrays).
- `astrolab/pipeline.py` — orchestrates the processing steps. Most of
  them (`stack_frames`, `detect_sources`, `measure_photometry`,
  `compose_image`) are stubs — this file is the shared entry point every
  team's work plugs into, so expect it to be a frequent source of merge
  conflicts during integration. That's by design.
- `data/frames/*.npy` — 5 synthetic, noisy exposures of the same field
  (128×128 pixels, 25 stars), generated with `astrolab.synth`, seed 42.
  Regenerate anytime with `python -m astrolab.synth` — output is
  byte-identical, so there's normally no need to.
- `astrolab/realdata.py` — **bonus feature, stubbed**: fetch a real
  telescope image (e.g. the Orion Nebula) live from a public sky-survey
  archive via `astroquery`, instead of a synthetic frame, for a genuine
  "real astro image" payoff. Not required for the core pipeline — the
  rest of the pipeline stays deterministic and offline by design.

## License

GPLv3 — see `LICENSE`.
