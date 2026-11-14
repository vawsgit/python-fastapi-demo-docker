---
type: explanation
title: How the app is built
---

# How the app is built

This page explains why the book catalogue ships as three variants instead of one.

## Three variants, one catalogue

Each variant under `server/` serves the same routes and the same templates. They differ only in where
the database URL comes from: `server/general/` reads it from the environment, `server/aws-secrets/`
reads it from AWS Secrets Manager, and `server/opentelemetry/` adds tracing on top of the general
variant. Splitting them keeps each deployment's extra dependency out of the others.

## Server-rendered pages

The app returns HTML from Jinja templates rather than JSON for a browser to render. The catalogue is a
teaching app, so a reader can follow one request from the route to the page without a second codebase.

## Related

- [Routes](../reference/routes.md)
