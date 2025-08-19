#!/usr/bin/env bash
set -euo pipefail

# Creates a venv, installs deps and the package in editable mode, then runs edge-assistant --help
VENVDIR=".venv"
python3 -m venv "$VENVDIR"
# shellcheck disable=SC1091
source "$VENVDIR/bin/activate"
python -m pip install --upgrade pip
pip install -e .
edge-assistant --help
