# Exploration: book recommendations
Request: "Customers want book recommendations." From: product owner, 2026-11-14. Read at: 7153bf7.

## Facts found
- Book has id, title, author, description. No genre, tags or ratings. (server/general/app/models.py)
- The books table has the same four columns. (server/db/init.sh)
- GET /books/{book_id} renders one book's page. (server/general/app/main.py)
- The three variants each have their own copy of the routes. (server/general/, server/aws-secrets/, server/opentelemetry/)
- FEATURES.md lists no recommendation feature. (FEATURES.md)

## Decisions made
- Q1. Basis: (A) same author, as recommended. Product owner, 2026-11-14.
- Q2. Variants: (A) all three, as recommended. Product owner, 2026-11-14.
- Q3. Where shown: (B) on the book's own page, below its description. Product owner, 2026-11-14.

## Open questions
- Q4. Cache suggestions? Owner: product owner. Blocks spec: no.

## Notes
- Suggested in the interview: filter the books by author in read_book, and pass them to book_details.html.

## Ready for spec
- Yes, 2026-11-14. Blocking questions open: none.
