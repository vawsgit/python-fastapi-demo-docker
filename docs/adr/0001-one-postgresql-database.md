# 0001. One PostgreSQL database for all application data

Date: 2026-11-10

## Status

Accepted

## Context

The book catalogue keeps its books in PostgreSQL 15 locally and in Aurora PostgreSQL on EKS. All three server
variants (`server/general/`, `server/aws-secrets/`, `server/opentelemetry/`) read and write the same `books` table.
This record binds every variant and every deployment of the app.

Options considered:
- PostgreSQL only: one datastore to back up, secure and run. Pages already load fast enough.
- PostgreSQL plus Redis as a cache: lost. All three variants would change, Redis would add its own backups and
  credentials, and no page is slow enough to need it.

## Decision

We will keep PostgreSQL as the only datastore for application data, in every variant.

## Consequences

- One set of backups, credentials and connection settings.
- A future cache needs a new record that supersedes this one.
