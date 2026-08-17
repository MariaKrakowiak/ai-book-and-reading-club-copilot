import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    """Create a connection to Lakebase."""

    database_url = os.environ.get("LAKEBASE_DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "LAKEBASE_DATABASE_URL environment variable is not configured."
        )

    return psycopg2.connect(database_url)


def run_query(query: str, params=None):
    """Execute a read query and return rows as dictionaries."""

    connection = get_connection()

    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
    finally:
        connection.close()


def run_write(query: str, params=None):
    """Execute an INSERT, UPDATE or DELETE statement."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()