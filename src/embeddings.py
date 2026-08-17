"""
Book embedding pipeline.

Creates semantic embeddings for books and stores them in Lakebase
using pgvector.
"""

import os
import logging
from typing import Iterable, Dict, Any

import numpy as np
from sentence_transformers import SentenceTransformer

from lakebase import run_write

logger = logging.getLogger(__name__)

MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

EMBEDDING_DIMENSION = 384

_model = None


def get_model() -> SentenceTransformer:
    """Load the embedding model lazily."""

    global _model

    if _model is None:
        logger.info("Loading embedding model: %s", MODEL_NAME)
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def build_book_text(book: Dict[str, Any]) -> str:
    """
    Build the textual representation used for semantic embedding.

    Args:
        book: Dictionary containing book metadata.

    Returns:
        A normalized text representation of the book.
    """

    title = book.get("title") or ""
    author = book.get("author") or book.get("author_name") or ""

    description = (
        book.get("description")
        or book.get("summary")
        or ""
    )

    subjects = book.get("subjects") or []

    if isinstance(subjects, str):
        subjects_text = subjects
    else:
        subjects_text = ", ".join(str(value) for value in subjects)

    publication_year = (
        book.get("publication_year")
        or book.get("first_publish_year")
        or ""
    )

    parts = [
        f"Title: {title}",
        f"Author: {author}",
        f"Description: {description}",
        f"Subjects: {subjects_text}",
        f"Publication year: {publication_year}",
    ]

    return "\n".join(
        part for part in parts
        if part.split(":", 1)[1].strip()
    )


def create_embedding(text: str) -> list[float]:
    """
    Generate a normalized semantic embedding.

    Args:
        text: Text to embed.

    Returns:
        A list containing a 384-dimensional normalized vector.
    """

    if not text or not text.strip():
        raise ValueError("Cannot create an embedding from empty text.")

    model = get_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.astype(np.float32).tolist()


def embed_book(book: Dict[str, Any]) -> list[float]:
    """
    Create an embedding for a single book.

    Args:
        book: Book metadata.

    Returns:
        384-dimensional embedding vector.
    """

    text = build_book_text(book)

    if not text.strip():
        raise ValueError(
            f"Book {book.get('id')} does not contain enough text to embed."
        )

    return create_embedding(text)


def save_book_embedding(
    book_id: str,
    embedding: list[float],
    source_text: str
) -> None:
    """
    Store or update a book embedding in Lakebase.

    Args:
        book_id: Identifier of the book.
        embedding: 384-dimensional embedding.
        source_text: Text used to generate the embedding.
    """

    if len(embedding) != EMBEDDING_DIMENSION:
        raise ValueError(
            f"Expected {EMBEDDING_DIMENSION}-dimensional embedding, "
            f"got {len(embedding)}."
        )

    query = """
        INSERT INTO book_embeddings (
            book_id,
            embedding,
            source_text
        )
        VALUES (%s, %s::vector, %s)
        ON CONFLICT (book_id)
        DO UPDATE SET
            embedding = EXCLUDED.embedding,
            source_text = EXCLUDED.source_text,
            updated_at = CURRENT_TIMESTAMP
    """

    vector = "[" + ",".join(map(str, embedding)) + "]"

    run_write(
        query,
        (
            book_id,
            vector,
            source_text,
        )
    )


def process_book(book: Dict[str, Any]) -> None:
    """
    Generate and persist an embedding for a book.

    Args:
        book: Book metadata dictionary.
    """

    try:
        text = build_book_text(book)
        embedding = create_embedding(text)

        save_book_embedding(
            book_id=str(book["id"]),
            embedding=embedding,
            source_text=text,
        )

        logger.info(
            "Created embedding for book %s",
            book.get("id")
        )

    except Exception:
        logger.exception(
            "Failed to create embedding for book %s",
            book.get("id")
        )
        raise


def process_books(books: Iterable[Dict[str, Any]]) -> None:
    """
    Generate embeddings for multiple books.

    Args:
        books: Iterable containing book dictionaries.
    """

    processed = 0

    for book in books:
        process_book(book)
        processed += 1

    logger.info(
        "Finished embedding %s books",
        processed
    )


if __name__ == "__main__":
    logger.info(
        "embeddings.py is a library module. "
        "Use ingest_books.py to load and process books."
    )