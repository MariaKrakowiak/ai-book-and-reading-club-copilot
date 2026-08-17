# AI Book & Reading Club Copilot

An AI-powered reading club assistant built with Databricks.

## Overview

The application helps individuals and reading clubs discover books,
manage reading lists, track reading progress and record ratings.

The AI agent combines semantic search with structured reading-club
data to make personalized recommendations.

## Architecture

Open Library
     |
     v
Spark ingestion
     |
     v
Delta
     |
     v
Lakebase
     |
     +---- Books
     +---- Clubs
     +---- Ratings
     +---- Reading progress
     +---- Notes
     |
     v
Book embeddings
     |
     v
Vector similarity search
     |
     v
AI Agent
     |
     v
Databricks App

## External API

Open Library API.

No API key is required.

The API provides book titles, authors, publication information,
subjects, ISBNs and cover information.

## MCP / Agent tools

The agent can use the following tools:

### Read tools

- search_books
- get_club_ratings

### Write tools

- add_book_to_club
- rate_book
- update_reading_progress
- save_note

## Semantic search

Book descriptions are transformed into embeddings using:

sentence-transformers/all-MiniLM-L6-v2

Embeddings have 384 dimensions and are stored in Lakebase using
pgvector.

## Example questions

"Recommend a mystery book for our club."

"Find a funny science-fiction book under 400 pages."

"What books have our club members rated highly?"

"Add The Hobbit to our reading club."

"I finished 150 pages of this book."

"Rate this book 5 stars and save my review."

## Agent guardrails

The agent:

- does not invent book information;
- uses semantic search before making recommendations;
- considers club ratings when recommending books;
- does not claim that a write operation succeeded unless the
  corresponding tool confirms it;
- validates ratings;
- does not create duplicate club-book relationships.

## Deployment

1. Configure Databricks authentication.
2. Validate the bundle:

databricks bundle validate

3. Deploy:

databricks bundle deploy

4. Run the ingestion job.
5. Verify the Delta and Lakebase tables.
6. Generate book embeddings.
7. Deploy the Databricks App.
8. Configure the Agent Bricks agent with the application tools.

## Demo

The final submission should include screenshots or transcripts
showing at least:

1. Semantic book recommendation.
2. Recommendation using club ratings.
3. Adding a book to a club.
4. Rating a book.
5. Updating reading progress.

## Project requirements

This project demonstrates:

- Spark data pipeline
- Delta Lake
- Lakebase
- Third-party API integration
- Unstructured text processing
- Embeddings
- Vector search
- AI agent
- Read/write agent tools
- Databricks App