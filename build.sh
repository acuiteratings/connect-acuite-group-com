#!/usr/bin/env bash
set -o errexit

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
BUILD_BASE_COMMIT_COUNT="${APP_BUILD_BASE_COMMIT_COUNT:-3}"
if [[ "$PYTHON_BIN" != /* && -x "$ROOT_DIR/$PYTHON_BIN" ]]; then
  PYTHON_BIN="$ROOT_DIR/$PYTHON_BIN"
fi
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python || command -v python3)"
fi

BUILD_NUMBER="${APP_BUILD_NUMBER:-}"
if [[ -z "$BUILD_NUMBER" ]] && command -v git >/dev/null 2>&1; then
  COMMIT_COUNT="$(git -C "$ROOT_DIR" rev-list --count HEAD 2>/dev/null || true)"
  if [[ "$COMMIT_COUNT" =~ ^[0-9]+$ ]]; then
    BUILD_SUFFIX=$(( COMMIT_COUNT - BUILD_BASE_COMMIT_COUNT ))
    if (( BUILD_SUFFIX < 1 )); then
      BUILD_SUFFIX=1
    fi
    BUILD_NUMBER="1.000000${BUILD_SUFFIX}"
  fi
fi
if [[ -z "$BUILD_NUMBER" ]]; then
  BUILD_NUMBER="1.0000001"
fi

printf '%s\n' "$BUILD_NUMBER" > "$ROOT_DIR/.build-number"

"$PYTHON_BIN" -m pip install -r backend/requirements.txt
cd "$ROOT_DIR/backend"
"$PYTHON_BIN" manage.py collectstatic --noinput
