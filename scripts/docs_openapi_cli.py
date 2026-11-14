# /// script
# requires-python = ">=3.12"
# dependencies = ["fastapi==0.135.3", "jinja2", "sqlalchemy", "python-multipart"]
# ///
"""Write docs/reference/openapi.json and docs/reference/routes.md from the app's own routes.

The app reads its database URL at import time, so this script registers an in-memory
stand-in for app.connect before importing app.main. No database and no running app.
"""

import json
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANT = ROOT / "server" / "general"
REFERENCE = ROOT / "docs" / "reference"


def stub_connect() -> None:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    engine = create_engine("sqlite://")
    module = types.ModuleType("app.connect")
    module.engine = engine
    module.db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    sys.modules["app.connect"] = module


def routes_table(document: dict) -> str:
    rows = []
    for path, methods in sorted(document["paths"].items()):
        for method, operation in sorted(methods.items()):
            summary = operation.get("summary", "")
            parameters = [
                p["name"] for p in operation.get("parameters", []) if p.get("in") == "query"
            ]
            rows.append(
                f"| `{method.upper()} {path}` | {summary} | "
                f"{', '.join(f'`{p}`' for p in parameters) or 'none'} |"
            )
    return "\n".join(rows)


def main() -> int:
    sys.path.insert(0, str(VARIANT))
    stub_connect()
    from app.main import app

    document = app.openapi()
    REFERENCE.mkdir(parents=True, exist_ok=True)
    (REFERENCE / "openapi.json").write_text(json.dumps(document, indent=2) + "\n")
    (REFERENCE / "routes.md").write_text(
        "---\n"
        "type: reference\n"
        "title: Routes\n"
        "---\n\n"
        "# Routes\n\n"
        "Every route the app serves, generated from the code by `make docs-openapi`.\n"
        "Never edit this page by hand.\n\n"
        "| Route | Summary | Query parameters |\n"
        "|---|---|---|\n" + routes_table(document) + "\n"
    )
    print(f"wrote {len(document['paths'])} paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
