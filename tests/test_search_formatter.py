from models.book import Book
from reports.search_formatter import search_books_by_title
from typing import Dict

# Unit tests
def test_search_books_by_title_empty_query() -> None:
    """Test that empty queries return an error."""
    success, output, error = search_books_by_title("")
    assert success is False
    assert error == "Title query cannot be empty or whitespace"
    assert output == ""

def test_search_books_by_title_whitespace_query() -> None:
    """Test that whitespace-only queries return an error."""
    success, output, error = search_books_by_title("   ")
    assert success is False
    assert error == "Title query cannot be empty or whitespace"
    assert output == ""

def test_search_books_by_title_no_results() -> None:
    """Test that searches with no results return success with appropriate message."""
    success, output, error = search_books_by_title("NonexistentBook")
    assert success is True
    assert "No books found" in output
    assert error is None

def test_search_books_by_title_with_results() -> None:
    """Test search with actual book results."""
    # Create sample books
    book1: Book = Book("Python Programming", "John Doe", 2020)
    book2: Book = Book("Advanced Python", "Jane Smith", 2021)
    book3: Book = Book("JavaScript Guide", "Bob Wilson", 2022)
    
    books_payload: Dict[str, Book] = {
        book1.book_id: book1,
        book2.book_id: book2,
        book3.book_id: book3,
    }
    
    success, output, error = search_books_by_title("Python", books_payload)
    
    assert success is True
    assert error is None
    assert "2 book(s) found" in output
    assert "Python Programming" in output
    assert "Advanced Python" in output
    assert "JavaScript Guide" not in output

def test_search_books_by_title_case_insensitive() -> None:
    """Test that search is case-insensitive."""
    book: Book = Book("Python Programming", "John Doe", 2020)
    books_payload: Dict[str, Book] = {book.book_id: book}

    success_lower, output_lower, _ = search_books_by_title("python", books_payload)
    success_upper, output_upper, _ = search_books_by_title("PYTHON", books_payload)
    success_mixed, output_mixed, _ = search_books_by_title("PyThOn", books_payload)

    assert success_lower is True
    assert success_upper is True
    assert success_mixed is True
    assert "Python Programming" in output_lower
    assert "Python Programming" in output_upper
    assert "Python Programming" in output_mixed

def test_search_books_by_title_partial_match() -> None:
    """Test that partial title matches are returned."""
    book: Book = Book("Python Programming Guide", "John Doe", 2020)
    books_payload: Dict[str, Book] = {book.book_id: book}

    success, output, error = search_books_by_title("Programming", books_payload)
    
    assert success is True
    assert error is None
    assert "Python Programming Guide" in output

def test_search_books_by_title_none_books_payload() -> None:
    """Test that None books_payload is handled gracefully."""
    success, output, error = search_books_by_title("Python", None)

    assert success is True
    assert "No books found" in output
    assert error is None
