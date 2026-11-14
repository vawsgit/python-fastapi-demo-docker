# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""Smoke test for an installed book app: four critical paths, PASS or FAIL each.

Usage: uv run scripts/smoke_test_cli.py --base-url http://127.0.0.1:8000
Exits non-zero when any check fails.
"""

import argparse
import re
import sys
import uuid

import httpx


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base-url", required=True)
    base = parser.parse_args().base_url.rstrip("/")
    title = f"smoke-test-{uuid.uuid4().hex[:8]}"
    failed = 0

    def check(name: str, ok: bool) -> None:
        nonlocal failed
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
        failed += not ok

    with httpx.Client(base_url=base, timeout=10) as client:
        try:
            check("home page returns 200", client.get("/").status_code == 200)
            created = client.post(
                "/books",
                data={"title": title, "author": "Smoke Test", "description": "-"},
            )
            check("create a test book", created.status_code in (200, 303))
            listing = client.get("/books").text
            match = re.search(rf'href="/books/(\d+)">{title}<', listing)
            check("book list shows the test book", match is not None)
            deleted = match and client.get(f"/books/{match.group(1)}/delete")
            check("delete the test book", bool(deleted) and deleted.status_code == 200)
        except httpx.HTTPError as error:
            check(f"reach {base} ({type(error).__name__})", False)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
