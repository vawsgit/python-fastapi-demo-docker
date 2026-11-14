# AGENTS.md

A FastAPI book catalogue with PostgreSQL, in three variants under `server/`.

## Commit convention

| Type | Bump | Example |
|---|---|---|
| `feat:` | minor | `feat(server): add GET /books/{book_id}/summary` |
| `fix:` | patch | `fix(server): return 404 when a book id does not exist` |
| `ci:`, `test:` | none | `ci: cache uv downloads` |

- A breaking change, such as a renamed environment variable, adds `!` and a `BREAKING CHANGE:` footer.
- The merge request title is the commit subject. Never use `--no-verify`.
