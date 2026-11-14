from fastapi.testclient import TestClient


def _client_with_two_authors(unit_app):
    client = TestClient(unit_app.app)
    for title, author in [("Emma", "Jane Austen"), ("1984", "George Orwell")]:
        client.post(
            "/books", data={"title": title, "author": author, "description": "-"}
        )
    return client


def test_author_filter_lists_only_that_authors_books(unit_app):
    page = (
        _client_with_two_authors(unit_app)
        .get("/books", params={"author": "Jane Austen"})
        .text
    )
    assert "Emma" in page and "1984" not in page


def test_blank_author_filter_lists_every_book(unit_app):
    page = _client_with_two_authors(unit_app).get("/books", params={"author": ""}).text
    assert "Emma" in page and "1984" in page
