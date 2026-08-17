from src.lakebase import run_query, run_write


def search_books(query_embedding, limit=10):
    """Find books using semantic similarity."""

    return run_query(
        """
        SELECT
            b.id,
            b.title,
            b.first_publish_year,
            b.number_of_pages,
            e.content,
            1 - (e.embedding <=> %s::vector) AS similarity
        FROM book_embeddings e
        JOIN books b ON b.id = e.book_id
        ORDER BY e.embedding <=> %s::vector
        LIMIT %s
        """,
        (
            query_embedding,
            query_embedding,
            limit
        )
    )


def get_club_ratings(club_id):
    """Retrieve ratings from members of a reading club."""

    return run_query(
        """
        SELECT
            b.title,
            r.rating,
            r.review,
            u.name
        FROM ratings r
        JOIN books b ON b.id = r.book_id
        JOIN users u ON u.id = r.user_id
        JOIN club_members cm ON cm.user_id = u.id
        WHERE cm.club_id = %s
        ORDER BY b.title
        """,
        (club_id,)
    )


def add_book_to_club(club_id, book_id):
    """Add a book to a club's reading list."""

    run_write(
        """
        INSERT INTO club_books (
            club_id,
            book_id
        )
        VALUES (%s, %s)
        ON CONFLICT (club_id, book_id)
        DO NOTHING
        """,
        (club_id, book_id)
    )

    return {
        "success": True,
        "club_id": club_id,
        "book_id": book_id
    }


def rate_book(user_id, book_id, rating, review=None):
    """Create or update a user's book rating."""

    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5.")

    run_write(
        """
        INSERT INTO ratings (
            user_id,
            book_id,
            rating,
            review
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (user_id, book_id)
        DO UPDATE SET
            rating = EXCLUDED.rating,
            review = EXCLUDED.review
        """,
        (
            user_id,
            book_id,
            rating,
            review
        )
    )

    return {
        "success": True
    }


def update_reading_progress(
    user_id,
    book_id,
    pages_read,
    status
):
    """Update a user's reading progress."""

    run_write(
        """
        INSERT INTO reading_progress (
            user_id,
            book_id,
            pages_read,
            status
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (user_id, book_id)
        DO UPDATE SET
            pages_read = EXCLUDED.pages_read,
            status = EXCLUDED.status,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            user_id,
            book_id,
            pages_read,
            status
        )
    )

    return {
        "success": True,
        "pages_read": pages_read,
        "status": status
    }


def save_note(user_id, book_id, note):
    """Save a reading note."""

    if not note or not note.strip():
        raise ValueError("Note cannot be empty.")

    run_write(
        """
        INSERT INTO notes (
            user_id,
            book_id,
            note
        )
        VALUES (%s, %s, %s)
        """,
        (
            user_id,
            book_id,
            note.strip()
        )
    )

    return {
        "success": True
    }