# AGENTS.md: server/opentelemetry

- Run this variant from the repository root: `docker compose -f docker-compose-opentelemetry.yml up --build`.
- It also starts the trace collector, configured by `server/opentelemetry/adot-collector-config/adot-config.yaml`.
- The collector mounts `~/.aws`, so it needs AWS credentials.
