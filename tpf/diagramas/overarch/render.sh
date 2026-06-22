#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL_DIR="$ROOT/models"
RENDER_DIR="$ROOT/generated"

python3 "$ROOT/validate_sequence_refs.py"

if [[ -n "${OVERARCH_JAR:-}" ]]; then
  OVERARCH=(java -jar "$OVERARCH_JAR")
elif [[ -f "$ROOT/tools/overarch.jar" ]]; then
  OVERARCH=(java -jar "$ROOT/tools/overarch.jar")
elif command -v overarch >/dev/null 2>&1; then
  OVERARCH=(overarch)
else
  echo "No se encontró Overarch." >&2
  echo "Defina OVERARCH_JAR, copie overarch.jar en overarch/tools/ o instale el comando overarch." >&2
  exit 2
fi

mkdir -p "$RENDER_DIR"
"${OVERARCH[@]}" \
  --model-dir "$MODEL_DIR" \
  --render-format plantuml \
  --render-dir "$RENDER_DIR" \
  --no-render-format-subdirs \
  --model-warnings \
  --debug

if command -v plantuml >/dev/null 2>&1; then
  mapfile -d '' PUML_FILES < <(find "$RENDER_DIR" -type f -name '*.puml' -print0)
  if ((${#PUML_FILES[@]})); then
    JAVA_TOOL_OPTIONS="${JAVA_TOOL_OPTIONS:-} -Djava.awt.headless=true" \
      plantuml -tsvg "${PUML_FILES[@]}"
  fi
fi

echo "Vistas generadas en $RENDER_DIR"
