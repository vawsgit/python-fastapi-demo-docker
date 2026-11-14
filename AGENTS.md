# AGENTS.md

A FastAPI book catalogue with PostgreSQL, in three variants under `server/`.

## Development context
- Forge: GitLab at <forge-host>. CLI: glab.
- Project: <group>/python-fastapi-demo-docker.
- Base branch: main. Every merge request targets main.
- Git route: a branch per change, then a draft merge request. A person approves and merges.
- Credential: project access token, role Developer, scope api, expires <date>. Never print it.
- Closing keywords: `Closes #<n>` in the merge request description only. `Related to #<n>` for partial work.
- Templates: issues use the feature template; merge requests fill a copy of the default template.
- A person keeps: merge, approve, mark ready, auto-merge, closing issues by hand.
