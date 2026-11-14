# Install the book app on AWS

This runbook installs the book app's database on Amazon RDS, then the app, and proves the install with a smoke test.

## Before you begin

| Prerequisite | Check | Ready output |
|---|---|---|
| AWS CLI v2 | `aws --version` | `aws-cli/2.` |
| Credentials for the target account | `aws sts get-caller-identity --query Account --output text` | The target account ID |
| Region set | `aws configure get region` | The target Region, such as `us-west-2` |
| Docker | `docker info --format '{{.ServerVersion}}'` | A version number |
| uv | `uv --version` | `uv 0.` |
| Database password in your secret store | `aws secretsmanager describe-secret --secret-id book-db-master` | The secret's ARN |

## Parameters

| Parameter | Description | Valid values |
|---|---|---|
| `ClusterType` | The kind of Amazon EKS cluster the database serves | `ManagedNodeGroup` (default), `AutoMode` |
| `DBMasterUsername` | Master user name for the database | 1 to 63 characters; default `bookdbadmin` |
| `DBMasterPassword` | Master password, passed from your secret store | 8 to 128 characters |

## Steps

1. Clone the repository. Expected result: a `python-fastapi-demo-docker` folder.
2. Copy `.env.example` to `.env`. Expected result: `.env` exists and git does not track it.
3. Set `DOCKER_DATABASE_URL` in `.env` for the target database. Expected result: `grep DOCKER_DATABASE_URL .env` prints one line.
4. Read the password into a shell variable: `DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id book-db-master --query SecretString --output text)`. Expected result: no output.
5. Validate the template: `aws cloudformation validate-template --template-body file://eks/rds-serverless-postgres.json`. Expected result: the three parameters are listed.
6. Deploy the database stack:
   `aws cloudformation deploy --template-file eks/rds-serverless-postgres.json --stack-name book-db --parameter-overrides ClusterType=ManagedNodeGroup DBMasterUsername=bookdbadmin DBMasterPassword="$DB_PASSWORD"`.
   Expected result: `Successfully created/updated stack - book-db`.
7. Start the app: `docker compose up -d --build`. Expected result: `docker compose ps` shows `web` as running.
8. Run the smoke test last: `uv run scripts/smoke_test_cli.py --base-url http://127.0.0.1:8000`. Expected result: four lines, each `PASS`.

## Open questions

- The README names no supported AWS Region.
- No file says who owns the database password secret, or how it is rotated.
