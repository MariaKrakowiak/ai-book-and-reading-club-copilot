from pyspark.sql import SparkSession

from src.lakebase import run_write


spark = SparkSession.builder.getOrCreate()

df = spark.table("book_club.books_raw")

rows = df.collect()

for row in rows:

    run_write(
        """
        INSERT INTO books (
            open_library_key,
            title,
            first_publish_year,
            isbn,
            number_of_pages,
            cover_id,
            edition_count
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (open_library_key)
        DO UPDATE SET
            title = EXCLUDED.title,
            first_publish_year = EXCLUDED.first_publish_year,
            isbn = EXCLUDED.isbn,
            number_of_pages = EXCLUDED.number_of_pages,
            cover_id = EXCLUDED.cover_id,
            edition_count = EXCLUDED.edition_count
        """,
        (
            row.open_library_key,
            row.title,
            row.first_publish_year,
            row.isbn,
            row.number_of_pages,
            row.cover_id,
            row.edition_count
        )
    )

spark.stop()