# AGENTS.md

A FastAPI book catalogue with PostgreSQL, in three variants under `server/`.

## Verification
- After each edit: `make lint` and `make test`.
- Before a commit, and before you say a task is done: `make check`. It needs Docker.
- If you changed a page, also run `make test-e2e` with the app running on 127.0.0.1:8000.
- Report the command, its exit status and the last 10 lines of output, from a run after your last edit.
- If a tier cannot run, say so. Do not report the task as done.
