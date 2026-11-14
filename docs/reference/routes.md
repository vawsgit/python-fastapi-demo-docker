---
type: reference
title: Routes
---

# Routes

Every route the app serves, generated from the code by `make docs-openapi`.
Never edit this page by hand.

| Route | Summary | Query parameters |
|---|---|---|
| `GET /` | Read Root | none |
| `GET /books` | List books | `author` |
| `POST /books` | Create Book Api | none |
| `GET /books/{book_id}` | Read Book | none |
| `GET /books/{book_id}/delete` | Delete Book | none |
| `GET /books/{book_id}/update` | Update Book Form | none |
| `POST /books/{book_id}/update` | Update Book | none |
| `GET /create_book` | Create Book Form | none |
