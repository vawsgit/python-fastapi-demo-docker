---
type: how-to
title: How to find books by author
---

# How to find books by author

This guide explains how to list only the books by one author in the book-catalogue app.

## Before you start

- The app runs with `docker compose up`.

## Steps

1. Open `http://localhost:8000/books?author=<name>`. Replace `<name>` with part of the author's name.

## Check the result

The list shows only the books whose author contains `<name>`. Case does not matter.

## Related

- [Routes](../reference/routes.md)
