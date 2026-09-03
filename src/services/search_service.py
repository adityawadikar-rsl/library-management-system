"""Service for searching library books by title."""

from __future__ import annotations

from typing import Dict, List, Optional

from models.book import Book
from models.exceptions import InvalidBookError


class SearchService:
    """Search and filter books stored in memory by title."""

    def __init__(self, books_payload: Optional[Dict[str, Book]] = None) -> None:
        """Initialize the service with a dictionary of books keyed by book_id."""
        if books_payload is None:
            books_payload = {}
        if not isinstance(books_payload, dict):
            raise InvalidBookError("books_payload must be a dictionary of Book objects")
        self.books: Dict[str, Book] = books_payload

    def search_books_by_title(self, title_query: str) -> List[Book]:
        """Return books whose titles contain the query, ignoring case."""
        if not isinstance(title_query, str) or not title_query.strip():
            raise InvalidBookError("title query cannot be empty or whitespace")

        normalized_query = title_query.strip().lower()
        matches: List[Book] = []

        for book in self.books.values():
            if not isinstance(book, Book):
                raise InvalidBookError("books_payload must contain only Book instances")
            if normalized_query in book.title.lower():
                matches.append(book)

        return matches


def search_books_by_title(books_payload: Optional[Dict[str, Book]], title_query: str) -> List[Book]:
    """Convenience helper to search books by title directly from a payload."""
    service = SearchService(books_payload)
    return service.search_books_by_title(title_query)
