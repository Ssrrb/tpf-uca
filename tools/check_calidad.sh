#!/usr/bin/env bash
# Reglas de calidad en texto para diagramas/*.puml
#   1. Solo archivos .puml dentro de diagramas/ (ni .kuml.kts, ni PNG, ni nada más).
#   2. Nombres: CU-XX-<tipo>[-n-<detalle>].puml
#   3. Estilo: !theme plain y la paleta celeste del grupo.
#   4. Completitud: cada CU (salvo CU-00) tiene diagrama de clases y de secuencia.
# Uso: tools/check_calidad.sh [directorio]   (por defecto: diagramas)
set -uo pipefail
DIR="${1:-diagramas}"; DIR="${DIR%/}"
fallas=0
falla() { echo "::error file=$1::$2"; fallas=$((fallas + 1)); }

# Tipos de diagrama admitidos. CU-00 usa los dos tipos generales del sistema.
TIPOS='clases|secuencia|actividades|estados|paquetes|modelo-estructural|casos-de-uso-alto-nivel|generalizacion-actores'
DETALLE='[a-z0-9]+(-[a-z0-9]+)*'
NOMBRE_RE="^CU-[0-9]{2}-(${TIPOS})(-[0-9]+-${DETALLE})?\.puml$"

# Paleta del grupo (CU-01/02). Header solo aplica a diagramas con clases.
FONDO='#F5F8FA'; BORDE='#17324D'; HEADER='#EAF2F6'

echo "== 1. Solo .puml en ${DIR}/"
while IFS= read -r -d '' f; do
  case "$f" in *.puml) ;; *) falla "$f" "archivo que no es .puml dentro de ${DIR}/ (no forma parte de la entrega)";; esac
done < <(find "$DIR" -mindepth 1 \( -type f -o -type l \) -print0)
while IFS= read -r -d '' d; do falla "$d" "subcarpeta no permitida en ${DIR}/"; done \
  < <(find "$DIR" -mindepth 1 -type d -print0)

echo "== 2. Nombres CU-XX-<tipo>[-n-<detalle>].puml"
for f in "$DIR"/*.puml; do
  [[ "$(basename "$f")" =~ $NOMBRE_RE ]] || falla "$f" "nombre fuera de la convención CU-XX-<tipo>[-n-<detalle>].puml (tipos: ${TIPOS//|/, })"
done

echo "== 3. Estilo: !theme plain + paleta ${FONDO} / ${BORDE} / ${HEADER}"
for f in "$DIR"/*.puml; do
  grep -qE '^\s*!theme\s+plain\s*$' "$f" || falla "$f" "falta '!theme plain'"
  grep -qi "$FONDO" "$f" || falla "$f" "falta el color de fondo ${FONDO}"
  grep -qi "$BORDE" "$f" || falla "$f" "falta el color de borde ${BORDE}"
  case "$(basename "$f")" in
    *-clases*|*-modelo-estructural*) grep -qi "$HEADER" "$f" || falla "$f" "falta HeaderBackgroundColor ${HEADER}";;
  esac
  [ "$(grep -c '^\s*@startuml' "$f")" -eq 1 ] || falla "$f" "debe tener un solo @startuml (un diagrama por archivo)"
done

echo "== 4. Completitud: clases + secuencia por CU"
for cu in $(ls "$DIR" | grep -E '\.puml$' | grep -oE '^CU-[0-9]{2}' | sort -u); do
  [ "$cu" = "CU-00" ] && continue
  compgen -G "$DIR/$cu-clases*.puml" >/dev/null || compgen -G "$DIR/$cu-modelo-estructural*.puml" >/dev/null \
    || falla "$DIR/$cu" "$cu no tiene diagrama de clases"
  compgen -G "$DIR/$cu-secuencia*.puml" >/dev/null \
    || falla "$DIR/$cu" "$cu no tiene diagrama de secuencia"
done

echo
if [ "$fallas" -gt 0 ]; then echo "Calidad: ${fallas} fallas."; exit 1; fi
echo "Calidad: OK ($(ls "$DIR"/*.puml | wc -l) diagramas)."
