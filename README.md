# AI Book and Reading Club Copilot

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
Delta (book_club.books_raw)
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

## AI agent

The agent is implemented in Python (agent/agent.py) and calls a
Databricks Model Serving endpoint via the Databricks SDK
(default endpoint: databricks-meta-llama-3-3-70b-instruct).

## Agent tools

The following tools are implemented in agent/tools.py:

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

The agent's system prompt (agent/prompts.py) instructs the agent to:

- never invent book information;
- use semantic search before making recommendations;
- consider club ratings when recommending books;
- never claim that a write operation succeeded unless the
  corresponding tool confirms it.

Write tools enforce validation at the database level:

- ratings must be between 1 and 5;
- duplicate club-book relationships are prevented with an
  upsert (ON CONFLICT DO NOTHING);

## Deployment

1. Configure Databricks authentication.
2. Set the required bundle variables
   (lakebase_host, model_serving_endpoint) and make sure the
   configured Model Serving endpoint is available.
3. Validate the bundle:

 databricks bundle validate

4. Deploy:

 databricks bundle deploy

5. Run the ingestion job (ingest_books, sync_to_lakebase,
   embed_books).
6. Verify the Delta and Lakebase tables.
7. Deploy the Databricks App with the MODEL_SERVING_ENDPOINT
   environment variable configured.

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
- Model Serving endpoint integration
- Read/write agent tools
- Databricks App