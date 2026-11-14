# AGENTS.md

A FastAPI book catalogue with PostgreSQL, in three variants under `server/`.

## Verification
- After each edit: `make lint` and `make test`.
- Before a commit, and before you say a task is done: `make check`. It needs Docker.
- If you changed a page, also run `make test-e2e` with the app running on 127.0.0.1:8000.
- Report the command, its exit status and the last 10 lines of output, from a run after your last edit.
- If a tier cannot run, say so. Do not report the task as done.

## Git route
1. For each new branch, create a worktree from the primary checkout:
   `git fetch origin && git worktree add --no-track -b <branch> ../python-fastapi-demo-docker-<branch> origin/working/sample`
2. Copy `.env` into it. Set its own `COMPOSE_PROJECT_NAME` and `WEB_PORT`.
3. Before you edit, run `pwd` and `git worktree list`.
4. Never switch the primary checkout's branch. Other sessions and the dev server use it.
5. Save work as commits, not with `git stash`. All worktrees share one stash.
6. Push with `git push -u origin <branch>`. A person merges.
