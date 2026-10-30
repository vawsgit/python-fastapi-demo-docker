import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.connect import engine
from app.main import app, get_db
from app.models import Book


@pytest.fixture
def db():
    # Each test runs in a transaction that is rolled back afterwards; the
    # handlers' commits only release savepoints inside it.
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()


def add_book(db, title):
    book = Book(title=title, author="Frank Herbert", description="Sci-fi")
    db.add(book)
    db.commit()
    return book


def form(title):
    return {"title": title, "author": "Frank Herbert", "description": "Sci-fi"}


def test_create_rejects_whitespace_only_title(client, db):
    count = db.query(Book).count()

    response = client.post("/books", data=form("   "), follow_redirects=False)

    assert response.status_code == 422
    assert "Title is required." in response.text
    assert db.query(Book).count() == count


def test_create_strips_title(client, db):
    response = client.post("/books", data=form("  Dune  "), follow_redirects=False)

    assert response.status_code == 303
    book = db.query(Book).order_by(Book.id.desc()).first()
    assert book.title == "Dune"


def test_update_rejects_whitespace_only_title(client, db):
    book = add_book(db, "Dune")

    response = client.post(
        f"/books/{book.id}/update", data=form("   "), follow_redirects=False
    )

    assert response.status_code == 422
    assert "Title is required." in response.text
    db.refresh(book)
    assert book.title == "Dune"


def test_update_strips_title(client, db):
    book = add_book(db, "Dune")

    response = client.post(
        f"/books/{book.id}/update",
        data=form("  Children of Dune  "),
        follow_redirects=False,
    )

    assert response.status_code == 303
    db.refresh(book)
    assert book.title == "Children of Dune"
