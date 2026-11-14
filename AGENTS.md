# AGENTS.md

A FastAPI book catalogue with PostgreSQL, in three variants under `server/`.

## Architecture decisions

- Decision records live in `docs/adr/`. The index is `docs/adr/README.md`.
- Only records with the status Accepted bind, within the scope each record states.
- Before you change structure, add or remove a dependency or datastore, change an API route, or change security or
  performance behaviour, read the index and open the accepted records that apply.
- Name each record you follow, by number, in your plan and in the merge request description.
- If the task conflicts with an accepted record, stop before you edit. Name the record, say what conflicts, and ask
  whether to follow the record or to draft a new record that supersedes it.
- You may draft a record with the status Proposed. Only a person sets Accepted, Rejected, Superseded or Deprecated.
