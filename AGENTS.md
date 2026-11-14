# AGENTS.md

A FastAPI book catalogue with PostgreSQL, in three variants under `server/`: `general`, `aws-secrets`
and `opentelemetry`. Each variant has its own Dockerfile and Compose file.

## Run
- First: `cp .env.example .env`. Every variant reads `.env`. Never commit `.env`; it holds the database passwords.
- General variant (`server/general/`), from the repository root: `docker compose up --build`.
- OpenTelemetry variant: see `server/opentelemetry/AGENTS.md`.
- The database schema and seed rows are in `server/db/init.sh`. Compose mounts it into PostgreSQL at first start.

## Checks
- There are no tests yet. Do not search for a test command.
- Format: `pre-commit run --all-files` (runs black 23.7.0). Run it before every commit.
