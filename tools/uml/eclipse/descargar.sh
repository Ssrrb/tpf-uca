#!/usr/bin/env bash
# Descarga Eclipse UML2 5.5.0 + EMF desde el repositorio p2 oficial de Eclipse
# (release train 2025-06) y verifica cada jar con el SHA-256 publicado en su
# artifacts.jar. Eclipse UML2 5.x implementa UML 2.5 (metamodelo
# http://www.eclipse.org/uml2/5.0.0/UML) y lee XMI de OMG (UML 2.5.1,
# http://www.omg.org/spec/UML/20161101) con org.eclipse.uml2.uml.resources.
# Uso: descargar.sh [directorio]   (por defecto: ~/.cache/tpf-uca/eclipse)
set -euo pipefail
DEST="${1:-$HOME/.cache/tpf-uca/eclipse}"
REPO="https://download.eclipse.org/releases/2025-06/202506111000/plugins"
mkdir -p "$DEST"
while read -r id version sha; do
  jar="$DEST/${id}_${version}.jar"
  if [ ! -f "$jar" ]; then
    curl -fsSL -o "$jar" "$REPO/${id}_${version}.jar"
  fi
  echo "$sha  $jar" | sha256sum -c --quiet - || { rm -f "$jar"; exit 1; }
done <<'JARS'
org.eclipse.emf.common 2.42.0.v20250401-0947 dfc7c263c1e06ecc32c00a355a6a7e41b32bb7d5198ac4d9fae0f1f1d580909f
org.eclipse.emf.ecore 2.39.0.v20250401-0947 0e2a28b6ef30fea664d24c770ffe48fc44f9c35c226b37fcbed1696395e264f0
org.eclipse.emf.ecore.xmi 2.39.0.v20250414-1351 f9340cbec677ea84b9dbb35717d62efc188bd8bc45eba11eaf2b7cc606ff413d
org.eclipse.emf.mapping.ecore2xml 2.13.0.v20240604-0832 79da8e7ef0df09675027288589ba2b4f4a1acacceb34600c0dc328d01bab1573
org.eclipse.uml2.common 2.5.0.v20221116-1811 f69dc6416c0bc9832291ad79d24aa35d209a8f1e203a9e3e863643c69810fe7e
org.eclipse.uml2.types 2.5.0.v20221116-1811 920f5b5d0370da5c633225baaae7fe34a5553d7e682d587966ab0da019be51dd
org.eclipse.uml2.uml 5.5.0.v20221116-1811 b570e1eddcd69f3bf3844f290e75cdabd6dc00c94de61ba9a323e14d36647065
org.eclipse.uml2.uml.resources 5.5.0.v20221116-1811 036a7d10a5fa2ed00fdda39f6be8ec6b412b264219521b50bc3555a769998bac
org.eclipse.uml2.uml.profile.standard 1.5.0.v20221116-1811 54a6b4b9664ceddb4114401a485287bdeb110ab66215f34a2e224b745f2f43d7
JARS
echo "$DEST"
