# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Fail when the generated reference is older than the code it describes.

Regenerates the reference into a temporary directory and compares it with the
committed pages, so a route added without `make docs-openapi` fails the check.
"""

import filecmp
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ("openapi.json", "routes.md")


def main() -> int:
    committed = ROOT / "docs" / "reference"
    with tempfile.TemporaryDirectory() as tmp:
        keep = {name: (Path(tmp) / name) for name in PAGES}
        for name, path in keep.items():
            shutil.copyfile(committed / name, path)
        subprocess.run(
            ["uv", "run", str(ROOT / "scripts" / "docs_openapi_cli.py")],
            check=True,
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        stale = [name for name in PAGES if not filecmp.cmp(committed / name, keep[name], shallow=False)]
        for name, path in keep.items():
            shutil.copyfile(path, committed / name)
    if stale:
        print(f"docs/reference/{', '.join(stale)} is out of date. Run: make docs-openapi")
        return 1
    print("the generated reference matches the code")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
