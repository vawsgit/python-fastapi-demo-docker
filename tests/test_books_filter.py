import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def test_book_list_filters_by_author(app_module):
    client = TestClient(app_module.app)
    for title, author in [("Dune", "Frank Herbert"), ("Emma", "Jane Austen")]:
        client.post("/books", data={"title": title, "author": author, "description": "x"})
    page = client.get("/books", params={"author": "Jane Austen"}).text
    assert "Emma" in page
    assert "Dune" not in page


def test_book_list_without_author_lists_every_book(app_module):
    client = TestClient(app_module.app)
    for title, author in [("Dune", "Frank Herbert"), ("Emma", "Jane Austen")]:
        client.post("/books", data={"title": title, "author": author, "description": "x"})
    page = client.get("/books").text
    assert "Emma" in page
    assert "Dune" in page
