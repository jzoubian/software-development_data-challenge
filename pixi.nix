# Instructor-only dev shell for rehearsing/testing this course's pixi demo
# (module 4) and any pixi-based exercises on NixOS.
#
# pixi itself runs fine on NixOS (it's a self-contained Rust binary), but the
# conda-forge packages it installs (python, numpy, ...) are plain,
# dynamically-linked Linux ELF binaries that expect the generic
# /lib64/ld-linux-x86-64.so.2 loader, which NixOS doesn't provide. Running
# `pixi run ...` outside this shell fails with "Could not start dynamically
# linked executable" (https://nix.dev/permalink/stub-ld). buildFHSEnv gives
# pixi's own environments a normal FHS layout to run in — same fix as
# `.conda-shell.nix` uses for plain conda.
#
# Usage: nix-shell pixi.nix, then `pixi init`, `pixi add`, `pixi run ...` as
# in the module 4 README/slides.
{ pkgs ? import <nixpkgs> { } }:

(pkgs.buildFHSEnv {
  name = "pixi-fhs";
  targetPkgs = pkgs: [ pkgs.pixi ];
}).env
