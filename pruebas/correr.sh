#!/bin/bash
# Corre pruebas de a una (con dos a la vez, las de posición y de foco fallan por tiempos; verif_consistencia
# llega a ~5,5 GB y va sola). Deja un log por prueba y _progreso.txt en salida/<carpeta>.
#   ./correr.sh                      todas las verif_*.py
#   ./correr.sh reg verif_a verif_b  solo esas, en salida/reg
# Con datos que no son los del repo: MFF_DATOS=/carpeta ./correr.sh (ver LEEME.md).
cd "$(dirname "$0")"
D=salida/${1:-reg}; shift || true
L=${*:-$(ls verif_*.py | sed 's/\.py$//')}
mkdir -p "$D"; : > "$D/_progreso.txt"
for t in $L; do
  timeout 1800 python3 "$t.py" > "$D/$t.log" 2>&1
  echo "$t salida $? $(grep -c '^FALLA ' "$D/$t.log") fallas" >> "$D/_progreso.txt"
done
echo FIN >> "$D/_progreso.txt"
