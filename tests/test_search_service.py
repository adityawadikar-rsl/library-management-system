"""Tests for the book title search service."""

import pytest

from models.book import Book
from models.exceptions import InvalidBookError
from services.search_service import SearchService, search_books_by_title


class TestSearchService:
    """Search service behavior for locating books by title."""

    def test_search_books_by_title_returns_case_insensitive_partial_matches(self) -> None:
        """The service should find partial, case-insensitive matches."""
        book_a = Book("Python Programming", "John Doe", 2020)
        book_b = Book("Advanced Python", "Jane Smith", 2021)
        book_c = Book("JavaScript Guide", "Bob Wilson", 2022)
        payload = {book_a.book_id: book_a, book_b.book_id: book_b, book_c.book_id: book_c}

        service = SearchService(payload)
        results = service.search_books_by_title("python")

        assert [book.title for book in results] == ["Python Programming", "Advanced Python"]

    def test_search_books_by_title_rejects_blank_query(self) -> None:
        """Blank queries are invalid and should raise a library domain exception."""
        service = SearchService({})

        with pytest.raises(InvalidBookError, match="title query"):
            service.search_books_by_title("   ")

    def test_module_level_search_helper_matches_title(self) -> None:
        """The helper function should support direct searches on a payload dictionary."""
        book = Book("Data Structures and Algorithms", "Alice Brown", 2019)
        payload = {book.book_id: book}

        results = search_books_by_title(payload, "structures")

        assert len(results) == 1
        assert results[0].title == "Data Structures and Algorithms"
