"""Search formatter for generating formatted search results for books."""

from typing import List, Tuple, Optional, Dict
from models.book import Book
from services.search_service import SearchService
from reports.utils import sanitize_report_input


def search_books_by_title(
    title_query: str, 
    books_payload: Optional[Dict[str, Book]] = None
) -> Tuple[bool, str, Optional[str]]:
    """
    Search for books by title and return formatted search results.
    
    This function searches for books matching the given title query
    and returns results as a formatted report tuple. No exceptions are raised;
    errors are returned in the error_message field.
    
    Args:
        title_query: The title or partial title to search for
        books_payload: Optional dictionary of Book objects keyed by book_id
    
    Returns:
        Tuple of (success_status, report_output, error_message):
        - success_status (bool): True if search completed successfully, False otherwise
        - report_output (str): Formatted search results or empty string on failure
        - error_message (Optional[str]): Error description if search failed, None if successful
    
    Example:
        >>> success, output, error = search_books_by_title("Python")
        >>> if success:
        ...     print(output)
    """
    try:
        # Sanitize the input
        sanitized_query: str = sanitize_report_input(title_query)
        
        # Validate sanitized input
        if not sanitized_query:
            return (False, "", "Title query cannot be empty or whitespace")
        
        # Initialize search service with books
        try:
            search_service: SearchService = SearchService(books_payload)
        except Exception as e:
            return (False, "", f"Failed to initialize search service: {str(e)}")
        
        # Perform the search
        try:
            results: List[Book] = search_service.search_books_by_title(sanitized_query)
        except Exception as e:
            return (False, "", f"Search failed: {str(e)}")
        
        # Format the results
        if not results:
            return (
                True, 
                f"No books found matching '{sanitized_query}'",
                None
            )
        
        # Build formatted output
        formatted_lines: List[str] = [
            f"Search Results for '{sanitized_query}' ({len(results)} book(s) found):",
            "-" * 60
        ]
        
        for idx, book in enumerate(results, 1):
            book_info: str = (
                f"{idx}. Title: {book.title}\n"
                f"   Author: {book.author}\n"
                f"   Year: {book.year_published}\n"
                f"   Book ID: {book.book_id}\n"
                f"   Status: {'Borrowed' if book.is_borrowed else 'Available'}"
            )
            formatted_lines.append(book_info)
        
        report_output: str = "\n".join(formatted_lines)
        
        return (True, report_output, None)
    
    except Exception as e:
        # Catch any unexpected errors
        return (False, "", f"Unexpected error during search: {str(e)}")
