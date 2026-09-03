"""Custom exceptions for the Library Management System."""


class LibraryError(Exception):
    """Base exception for all library-related errors."""
    pass


class FineCalculationError(LibraryError):
    """Raised when fine calculation fails or invalid parameters are provided."""
    pass


class InvalidMemberError(LibraryError):
    """Raised when member-related operations fail."""
    pass


class InvalidBookError(LibraryError):
    """Raised when book-related operations fail."""
    pass


class BorrowingLimitError(LibraryError):
    """Raised when a member cannot borrow because of outstanding fines."""
    pass


class InvalidCategoryError(LibraryError):
    """Raised when category validation fails."""
    pass


class CategoryNotFoundError(LibraryError):
    """Raised when a category cannot be located in the repository."""
    pass


class PublisherNotFoundError(LibraryError):
    """Raised when a publisher cannot be located in the repository."""
    pass


class InvalidPublisherError(LibraryError):
    """Raised when publisher data is invalid."""
    pass
