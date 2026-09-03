import pytest

from models.book import Book
from models.exceptions import BorrowingLimitError, InvalidMemberError
from models.member import Member
from services.library_manager import LibraryManager


def build_manager() -> tuple[LibraryManager, Member, Book]:
    manager = LibraryManager()
    member = Member("Ada Lovelace", "ada@example.com")
    book = Book("Computing", "Ada Lovelace", 1843)
    manager.register_member(member)
    manager.add_book(book)
    return manager, member, book


def test_add_and_register_store_entities() -> None:
    manager, member, book = build_manager()

    assert manager.books[book.book_id] is book
    assert manager.members[member.member_id] is member


def test_checkout_and_return_book() -> None:
    manager, member, book = build_manager()

    manager.checkout_book(member.member_id, book.book_id)
    assert book.is_borrowed is True
    assert member.borrowed_book_ids == [book.book_id]

    manager.process_return(member.member_id, book.book_id)
    assert book.is_borrowed is False
    assert member.borrowed_book_ids == []


def test_checkout_rejects_unknown_member_or_book() -> None:
    manager, member, book = build_manager()

    with pytest.raises(InvalidMemberError):
        manager.checkout_book("missing", book.book_id)
    with pytest.raises(InvalidMemberError):
        manager.process_return(member.member_id, "missing")


def test_checkout_rejects_member_over_fine_limit() -> None:
    manager, member, book = build_manager()
    member.accumulated_fines = 251.0

    with pytest.raises(BorrowingLimitError):
        manager.checkout_book(member.member_id, book.book_id)


def test_process_return_adds_overdue_fine() -> None:
    manager, member, book = build_manager()
    manager.checkout_book(member.member_id, book.book_id)
    book.due_date = "2020-01-01T00:00:00"

    manager.process_return(member.member_id, book.book_id)

    assert member.accumulated_fines == 250.0


def test_search_books_by_author_is_case_insensitive_and_partial() -> None:
    manager, _, book = build_manager()
    other = Book("Another", "Grace Hopper", 1952)
    manager.add_book(other)

    assert manager.search_books_by_author("lovelace") == [book]
    assert manager.search_books_by_author("HOP") == [other]