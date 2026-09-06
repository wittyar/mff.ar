#!/bin/sh
# Equivalente del MFF.bat para Linux y macOS (se usa para probar el mismo flujo).
cd "$(dirname "$0")" || exit 1
exec python3 desktop/servidor.py "$@"
