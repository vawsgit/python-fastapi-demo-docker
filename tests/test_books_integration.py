import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def test_post_books_stores_a_row(app_module):
    client = TestClient(app_module.app)
    client.post(
        "/books", data={"title": "Dune", "author": "Frank Herbert", "description": "x"}
    )
    assert "Dune" in client.get("/books").text
