from fastapi.testclient import TestClient


def test_get_book_returns_404_for_a_missing_id(unit_app):
    client = TestClient(unit_app.app)
    assert client.get("/books/999").status_code == 404
