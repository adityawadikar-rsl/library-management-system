from typing import List, Optional, Tuple
from models.book import Book
from models.member import Member

ReportResult = Tuple[bool, str, Optional[str]]


def generate_inventory_report(books: List[Book]) -> ReportResult:
    try:
        lines = ["Library Inventory Report", "=" * 24]

        for book in books:
            status = "Borrowed" if book.is_borrowed else "Available"
            lines.append(f"[{status}] {book.title} by {book.author} ({book.year_published})")
            if book.is_borrowed:
                if not book.due_date:
                    return (False, "", "Borrowed books must have a due date")
                lines.append(f"    -> Due: {book.due_date[:10]}")

        return (True, "\n".join(lines), None)
    except Exception as error:
        return (False, "", f"Unable to generate inventory report: {error}")


def generate_financial_report(members: List[Member]) -> ReportResult:
    try:
        lines = ["Outstanding Fines Report", "=" * 24]
        total_fines = 0.0

        for member in members:
            if member.accumulated_fines > 0:
                lines.append(f"{member.name} ({member.email}): ₹{member.accumulated_fines:.2f}")
                total_fines += member.accumulated_fines

        lines.append("-" * 24)
        lines.append(f"Total Outstanding: ₹{total_fines:.2f}")
        return (True, "\n".join(lines), None)
    except Exception as error:
        return (False, "", f"Unable to generate financial report: {error}")
