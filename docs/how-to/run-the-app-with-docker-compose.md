---
type: how-to
title: How to run the app with Docker Compose
---

# How to run the app with Docker Compose

This guide explains how to run the book-catalogue app and its database on your own machine.

## Before you start

- Docker Desktop runs.
- You copied `.env.example` to `.env`.

## Steps

1. Build the images.

   ```bash
   docker compose build
   ```

2. Start the app and the database.

   ```bash
   docker compose up -d
   ```

3. Read the app's logs until it reports that it serves on port 8000.

   ```bash
   docker compose logs -f web
   ```

## Check the result

Open `http://localhost:8000/books`. The list page opens.

## Related

- [Routes](../reference/routes.md)
