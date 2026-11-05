#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
export PYTHONPATH="$ROOT${TIP_OPENPI_SRC:+:$TIP_OPENPI_SRC}${TIP_OPENPI_CLIENT_SRC:+:$TIP_OPENPI_CLIENT_SRC}${PYTHONPATH:+:$PYTHONPATH}"
export XLA_PYTHON_CLIENT_PREALLOCATE=false
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-4}"
exec "${TIP_MODEL_PYTHON:-python3}" -u -m tip_bridge.server "$@"
