# 0002. Redis caches book lookups

Date: 2026-11-14

## Status

Accepted

## Context

Book lookups now dominate database load. Record 0001 kept PostgreSQL as the only datastore, and named a cache as
the change that would need a new record. This record binds all three server variants.

Options considered:
- Keep 0001 and tune PostgreSQL: lost, because the lookups repeat the same few rows.
- Redis as a read-through cache for book lookups: won. PostgreSQL stays the source of truth.

## Decision

We will cache book lookups in Redis, in every variant, and keep PostgreSQL as the only store of record.

## Consequences

- Redis adds its own credentials and a container in each Compose file.
- A write must clear the cached book, or a reader sees stale data.
