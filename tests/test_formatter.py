from models.book import Book
from models.member import Member
from reports.formatter import generate_financial_report, generate_inventory_report
from reports.utils import sanitize_report_input


def test_inventory_report_returns_success_tuple() -> None:
    book = Book("Dune", "Frank Herbert", 1965)

    success, output, error = generate_inventory_report([book])

    assert success is True
    assert "[Available] Dune" in output
    assert error is None


def test_inventory_report_returns_failure_tuple_for_malformed_input() -> None:
    success, output, error = generate_inventory_report([object()])  # type: ignore[list-item]

    assert success is False
    assert output == ""
    assert error is not None


def test_financial_report_returns_success_tuple() -> None:
    member = Member("Ada Lovelace", "ada@example.com")
    member.add_fine(75.0)

    success, output, error = generate_financial_report([member])

    assert success is True
    assert "Ada Lovelace (ada@example.com): ₹75.00" in output
    assert error is None


def test_financial_report_returns_failure_tuple_for_malformed_input() -> None:
    success, output, error = generate_financial_report([object()])  # type: ignore[list-item]

    assert success is False
    assert output == ""
    assert error is not None


def test_sanitizer_normalizes_string_input() -> None:
    assert sanitize_report_input("  title  ") == "title"