#!/usr/bin/env bash
set -o errexit

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-.venv/bin/python}"
if [[ "$PYTHON_BIN" != /* && -x "$ROOT_DIR/$PYTHON_BIN" ]]; then
  PYTHON_BIN="$ROOT_DIR/$PYTHON_BIN"
fi
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python || command -v python3)"
fi

"$PYTHON_BIN" -m pip install --upgrade "pip>=26.0"
"$PYTHON_BIN" -m pip install -r backend/requirements.txt
cd "$ROOT_DIR/backend"
"$PYTHON_BIN" manage.py collectstatic --noinput
