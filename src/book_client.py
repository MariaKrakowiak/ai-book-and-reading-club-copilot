import requests
from typing import Any, Dict, List, Optional


class OpenLibraryClient:
    """Client for the Open Library APIs."""

    BASE_URL = "https://openlibrary.org"

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "AI-Book-Reading-Club-Copilot/1.0"
        })

    def search_books(
        self,
        query: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search Open Library for books."""

        response = self.session.get(
            f"{self.BASE_URL}/search.json",
            params={
                "q": query,
                "limit": limit
            },
            timeout=self.timeout
        )

        response.raise_for_status()

        data = response.json()

        books = []

        for doc in data.get("docs", []):
            books.append(self._normalize_book(doc))

        return books

    def get_book(self, work_key: str) -> Optional[Dict[str, Any]]:
        """Retrieve detailed information about a book/work."""

        response = self.session.get(
            f"{self.BASE_URL}{work_key}.json",
            timeout=self.timeout
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()

        return response.json()

    def _normalize_book(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Open Library response into our application model."""

        authors = doc.get("author_name", [])

        return {
            "open_library_key": doc.get("key"),
            "title": doc.get("title"),
            "authors": authors,
            "first_publish_year": doc.get("first_publish_year"),
            "isbn": (doc.get("isbn") or [None])[0],
            "number_of_pages": doc.get("number_of_pages_median"),
            "subjects": doc.get("subject", [])[:20],
            "cover_id": doc.get("cover_i"),
            "edition_count": doc.get("edition_count"),
        }