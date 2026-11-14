# #12 Filter books by author

Readers with a long book list want to see one author's books at a time.

## Acceptance criteria
- The book list page has an author box. Submitting it shows only that author's books.
- `GET /books?author=<name>` returns only the books whose author is `<name>`.
- `GET /books` with no author still lists every book.

## Out of scope
- The `server/aws-secrets/` and `server/opentelemetry/` variants.
