from sentence_transformers import SentenceTransformer

from src.lakebase import run_query, run_write


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


books = run_query(
    """
    SELECT
        id,
        title,
        description
    FROM books
    WHERE title IS NOT NULL
    """
)


for book in books:

    content = f"""
    Title: {book['title']}

    Description:
    {book.get('description') or 'No description available.'}
    """

    embedding = model.encode(
        content,
        normalize_embeddings=True
    ).tolist()

    run_write(
        """
        INSERT INTO book_embeddings (
            book_id,
            chunk_index,
            content,
            embedding
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (book_id, chunk_index)
        DO UPDATE SET
            content = EXCLUDED.content,
            embedding = EXCLUDED.embedding
        """,
        (
            book["id"],
            0,
            content,
            embedding
        )
    )