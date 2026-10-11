CREATE EXTENSION IF NOT EXISTS vector;


CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(320),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS reading_clubs (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    created_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS club_members (
    club_id BIGINT REFERENCES reading_clubs(id),
    user_id BIGINT REFERENCES users(id),
    role VARCHAR(50) DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (club_id, user_id)
);


CREATE TABLE IF NOT EXISTS books (
    id BIGSERIAL PRIMARY KEY,
    open_library_key VARCHAR(200) UNIQUE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    first_publish_year INTEGER,
    isbn VARCHAR(50),
    number_of_pages INTEGER,
    cover_id BIGINT,
    edition_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS book_authors (
    book_id BIGINT REFERENCES books(id),
    author_name VARCHAR(300) NOT NULL,
    PRIMARY KEY (book_id, author_name)
);


CREATE TABLE IF NOT EXISTS club_books (
    club_id BIGINT REFERENCES reading_clubs(id),
    book_id BIGINT REFERENCES books(id),
    status VARCHAR(50) DEFAULT 'candidate',
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (club_id, book_id)
);


CREATE TABLE IF NOT EXISTS ratings (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    book_id BIGINT REFERENCES books(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, book_id)
);


CREATE TABLE IF NOT EXISTS reading_progress (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    book_id BIGINT REFERENCES books(id),
    pages_read INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'not_started',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, book_id)
);


CREATE TABLE IF NOT EXISTS notes (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    book_id BIGINT REFERENCES books(id),
    note TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS recommendations (
    id BIGSERIAL PRIMARY KEY,
    club_id BIGINT REFERENCES reading_clubs(id),
    book_id BIGINT REFERENCES books(id),
    reason TEXT,
    score DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS book_embeddings (
    id BIGSERIAL PRIMARY KEY,
    book_id BIGINT REFERENCES books(id),
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(book_id, chunk_index)
);


CREATE INDEX IF NOT EXISTS book_embeddings_vector_idx
ON book_embeddings
USING ivfflat (embedding vector_cosine_ops);