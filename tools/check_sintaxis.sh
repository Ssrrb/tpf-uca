#!/usr/bin/env bash
# Valida la sintaxis de cada .puml con plantuml -checkonly.
# Si la pasada en lote falla, revisa archivo por archivo para nombrar los rotos.
# Uso: tools/check_sintaxis.sh [directorio]   (necesita el comando plantuml)
set -uo pipefail
DIR="${1:-diagramas}"; DIR="${DIR%/}"
if plantuml -checkonly "$DIR"/*.puml; then
  echo "Sintaxis: OK ($(ls "$DIR"/*.puml | wc -l) diagramas)."
  exit 0
fi
rotos=0
for f in "$DIR"/*.puml; do
  if ! salida=$(plantuml -checkonly -stdrpt:1 -pipe < "$f" 2>&1 >/dev/null); then
    echo "::error file=$f::sintaxis inválida: $(echo "$salida" | grep -v JAVA_TOOL | tr '\n' ' ')"
    rotos=$((rotos + 1))
  fi
done
echo "Sintaxis: ${rotos} archivos con errores."
exit 1
