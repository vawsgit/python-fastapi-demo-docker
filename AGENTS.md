# AGENTS.md

A FastAPI book catalogue with PostgreSQL, in three variants under `server/`.

## Documentation

- Update the docs in the same merge request as the code. A change is not done until its pages are.
- Docs are required when a change adds, changes or removes a route, query parameter, form field, page,
  environment variable, setup step or make target. Docs are not required for a refactor with no change
  in behaviour, a test-only change or a CI-only change. Then write "Docs: not needed, <reason>" in the
  merge request description.
- Choose the page type with two questions: does the page tell the reader what to do, or what is true?
  Is the reader learning, or working? Do and learn: `docs/tutorials/`. Do and work: `docs/how-to/`.
  Know and work: `docs/reference/`. Know and learn: `docs/explanation/`.
- Search `docs/` for an existing page before you create one. Extend it if it covers the subject.
- Start each new page from `docs/templates/<type>.md` and replace every `{placeholder}`.
- Never edit `docs/reference/openapi.json` or `docs/reference/routes.md` by hand. Run `make docs-openapi`.
- Before you report the change as done, run `make docs-check` and fix every error.
