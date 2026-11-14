---
type: tutorial
title: Add your first book
---

# Add your first book

In this tutorial you add one book to the catalogue and see it in the list.

## What you need

- The app runs with `docker compose up`.

## Steps

1. Open `http://localhost:8000/books`. The list page opens, empty on a new database.

2. Select **Add a book**. A form with title, author and description opens.

3. Type a title, an author and a description, then select **Save**.

   The app returns to the list page, and your book is on it.

## What you did

You added one book through the form, and the catalogue stored it in PostgreSQL. To find a book by its
author, read [How to run the app with Docker Compose](../how-to/run-the-app-with-docker-compose.md).
