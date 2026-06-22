#!/usr/bin/env python3
"""Valida el puente entre secuencias PlantUML y métodos canónicos Overarch."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
DIAGRAM_DIR = ROOT.parent
MODEL_TEXT = "\n".join(
    path.read_text(encoding="utf-8") for path in sorted((ROOT / "models").glob("*.edn"))
)
OP_REF = re.compile(r"^\s*'\s*op:\s*(:\S+)\s*$")
MESSAGE_NAME = re.compile(r":\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(")


def canonical_name(ref: str) -> str:
    matches = list(re.finditer(rf":id\s+{re.escape(ref)}(?=\s|\}})", MODEL_TEXT))
    if len(matches) != 1:
        raise ValueError(
            f"{ref}: se esperaban 1 definición canónica y se encontraron {len(matches)}"
        )
    fragment = MODEL_TEXT[matches[0].end() : matches[0].end() + 300]
    name = re.search(r':name\s+"([^"]+)"', fragment)
    if not name:
        raise ValueError(f"{ref}: la definición no tiene :name cercano al :id")
    return name.group(1)


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    refs = 0
    for index, line in enumerate(lines):
        match = OP_REF.match(line)
        if not match:
            continue
        refs += 1
        ref = match.group(1)
        previous = index - 1
        while previous >= 0 and (not lines[previous].strip() or lines[previous].lstrip().startswith("'")):
            previous -= 1
        message = MESSAGE_NAME.search(lines[previous]) if previous >= 0 else None
        if not message:
            errors.append(f"{path.name}:{index + 1}: falta un mensaje con operación antes de {ref}")
            continue
        try:
            expected = canonical_name(ref)
        except ValueError as exc:
            errors.append(f"{path.name}:{index + 1}: {exc}")
            continue
        actual = message.group(1)
        if actual != expected:
            errors.append(
                f"{path.name}:{index + 1}: mensaje {actual}() no coincide con {ref} ({expected}())"
            )
    if refs == 0:
        errors.append(f"{path.name}: no contiene referencias ' op:")
    return errors


def main() -> int:
    files = sorted(DIAGRAM_DIR.glob("*secuencia*.puml"))
    errors = [error for path in files for error in validate_file(path)]
    if errors:
        print("Errores de consistencia en secuencias:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Referencias de secuencia válidas: {len(files)} archivo(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
