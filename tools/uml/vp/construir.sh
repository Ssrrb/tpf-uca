#!/usr/bin/env bash
# Compila el plugin de VP y arma el zip para Help > Install Plugin.
# Uso: tools/uml/vp/construir.sh /ruta/a/openapi.jar [build/vp-diagramas.json] [salida.zip]
# openapi.jar viene con VP (Visual Paradigm.app/Contents/Resources/app/lib/openapi.jar);
# es propietario, así que no se versiona.
set -euo pipefail
API=${1:?falta la ruta a openapi.jar}
DATOS=${2:-build/vp-diagramas.json}
SALIDA=${3:-build/tpfuca-vp-plugin.zip}
AQUI=$(cd "$(dirname "$0")" && pwd)
TMP=$(mktemp -d)
mkdir -p "$TMP/tpfuca.vp"
# VP 18.1 trae Java 11.
javac --release 11 -encoding UTF-8 -cp "$API" -d "$TMP/tpfuca.vp" "$AQUI"/src/tpfuca/vp/*.java
cp "$AQUI/plugin.xml" "$DATOS" "$TMP/tpfuca.vp/"
rm -f "$SALIDA"
SALIDA_ABS=$(cd "$(dirname "$SALIDA")" && pwd)/$(basename "$SALIDA")
(cd "$TMP" && zip -qr "$SALIDA_ABS" tpfuca.vp)
rm -rf "$TMP"
echo "$SALIDA"
