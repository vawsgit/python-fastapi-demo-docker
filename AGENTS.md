# AGENTS.md

A FastAPI book catalogue with PostgreSQL, in three variants under `server/`.

## Verification
- After each edit: `make lint` and `make test`.
- Before a commit, and before you say a task is done: `make check`. It needs Docker.
- If you changed a page, also run `make test-e2e` with the app running on 127.0.0.1:8000.
- Report the command, its exit status and the last 10 lines of output, from a run after your last edit.
- If a tier cannot run, say so. Do not report the task as done.

## Cloud

| Environment | AWS account | Region | Profile | Purpose | Agent may write |
|---|---|---|---|---|---|
| dev (read) | 111122223333 | us-west-2 | demo-read | Explore: list, describe, read logs | no |
| dev (deploy) | 111122223333 | us-west-2 | demo-deploy | Push images to ECR, apply `eks/` manifests, manage the test bucket `cloud-context-demo-bucket` | yes, after approval |
| any other account | — | — | none | Not a target for this repository | no |

- Pass `--profile` and `--region us-west-2` on every AWS command. Never rely on `AWS_PROFILE`, `AWS_REGION` or the default profile.
- Use the read profile unless the task says deploy.
- Read the current state and preview before a change.
- Before a delete, say what goes and whether it can be recovered. Then wait.
- If a target is not in the table, read only, and ask.
- Refer to credentials by profile name. Never read or print one. If credentials fail, stop and ask.
