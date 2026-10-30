import os
from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import Base, Book
from app.connect import db_session, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
)


def get_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})


@app.get("/create_book")
def create_book_form(request: Request):
    return templates.TemplateResponse(request, "create_book.html", {"request": request})


@app.post("/books")
def create_book_api(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
):
    title = title.strip()
    if not title:
        return templates.TemplateResponse(
            request,
            "create_book.html",
            {"request": request, "error": "Title is required."},
            status_code=422,
        )
    book = Book(title=title, author=author, description=description)
    db.add(book)
    db.commit()
    db.refresh(book)
    return RedirectResponse(url="/books", status_code=303)


@app.get("/books")
def list_books(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return templates.TemplateResponse(
        request, "list_books.html", {"request": request, "books": books}
    )


@app.get("/books/{book_id}")
def read_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id)
    return templates.TemplateResponse(
        request, "book_details.html", {"request": request, "book": book}
    )


@app.get("/books/{book_id}/update")
def update_book_form(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id)
    return templates.TemplateResponse(
        request, "update_book.html", {"request": request, "book": book}
    )


@app.post("/books/{book_id}/update")
def update_book(
    request: Request,
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
):
    book = get_book(db, book_id)
    title = title.strip()
    if not title:
        return templates.TemplateResponse(
            request,
            "update_book.html",
            {"request": request, "book": book, "error": "Title is required."},
            status_code=422,
        )
    book.title = title
    book.author = author
    book.description = description
    db.commit()
    return RedirectResponse(url=f"/books/{int(book_id)}", status_code=303)


@app.get("/books/{book_id}/delete")
def delete_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id)
    db.delete(book)
    db.commit()
    return templates.TemplateResponse(
        request, "delete_book.html", {"request": request, "book": book}
    )
