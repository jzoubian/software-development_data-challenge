FROM python:3.11-slim

WORKDIR /app

# --- Dependencies -----------------------------------------------------
# No pyproject.toml / requirements.txt / pixi.toml was found in the repo
# at the time this Dockerfile was created. This project appears to use
# pixi (see pixi.nix) or Nix (see shell.nix) for local dev environments,
# neither of which is wired up here yet.
#
# Once dependencies are finalized, add ONE of the following blocks:
#
#   # pip:
#   COPY requirements.txt .
#   RUN pip install --no-cache-dir -r requirements.txt
#
#   # pixi:
#   COPY pixi.toml pixi.lock* .
#   RUN pip install pixi && pixi install
# ------------------------------------------------------------------------

# Copy the application code
COPY astrolab/ ./astrolab/

# data/ doesn't exist in the repo yet (likely gitignored / generated).
# Create an empty dir so the image has a stable mount point;
# swap this for `COPY data/ ./data/` once the folder exists.
RUN mkdir -p data

CMD ["python", "-m", "astrolab"]
