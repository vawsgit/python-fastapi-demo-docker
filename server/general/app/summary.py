from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.connect import db_session
from app.models import Book

MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
REGION = "us-west-2"

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
    client = boto3.client("bedrock-runtime", region_name=REGION)
    response = client.converse(
        modelId=MODEL_ID,
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
