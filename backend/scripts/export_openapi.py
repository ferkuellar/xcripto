from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.main import app  # noqa: E402


def export_openapi(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    schema = app.openapi()
    output.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Export XMIP Backend OpenAPI schema")
    parser.add_argument("--output", default="docs/openapi.json")
    args = parser.parse_args()

    output = export_openapi(Path(args.output))
    print(f"OpenAPI exported to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
