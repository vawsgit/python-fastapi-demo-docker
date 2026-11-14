from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.connect import db_session
from app.models import Book
from app.settings import settings


router = APIRouter()


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


@router.get("/books/{book_id}/summary")
def summarize_book(book_id: int, db: Session = Depends(get_db)):
    import boto3

    book = db.query(Book).filter(Book.id == book_id).first()
    client = boto3.client("bedrock-runtime", region_name=settings.aws_region)
    response = client.converse(
        modelId=settings.bedrock_model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {"text": f"Summarize in two sentences: {book.description}"}
                ],
            }
        ],
    )
    text = response["output"]["message"]["content"][0]["text"]
    return {"book_id": book_id, "summary": text}
