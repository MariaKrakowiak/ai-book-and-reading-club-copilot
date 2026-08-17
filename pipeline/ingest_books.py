from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, array_distinct

from src.book_client import OpenLibraryClient


spark = SparkSession.builder.appName(
    "ai-book-reading-club-ingestion"
).getOrCreate()


client = OpenLibraryClient()

queries = [
    "science fiction",
    "mystery",
    "fantasy",
    "historical fiction",
    "romance",
    "nonfiction",
    "psychology",
    "business"
]


records = []

for query in queries:
    books = client.search_books(query, limit=50)

    for book in books:
        records.append(book)


df = spark.createDataFrame(records)

# Remove duplicate books.
df = df.dropDuplicates(["open_library_key"])

# Normalize author and subject arrays.
df = df.withColumn(
    "authors",
    array_distinct(col("authors"))
)

df = df.withColumn(
    "subjects",
    array_distinct(col("subjects"))
)

(
    df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("book_club.books_raw")
)

print(f"Ingested {df.count()} books.")

spark.stop()