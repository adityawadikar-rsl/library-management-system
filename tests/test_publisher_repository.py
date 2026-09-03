"""Tests for the publisher entity and repository."""

import pytest

from models.exceptions import PublisherNotFoundError
from models.publisher import Publisher
from services.publisher_repository import PublisherRepository


def publisher_payload(publisher_id: str = "pub-1") -> dict[str, str]:
    """Build a valid publisher payload for tests."""
    return {
        "publisher_id": publisher_id,
        "name": "Acme Publishing",
        "email": "contact@acme.example",
    }


def test_create_and_retrieve_publisher() -> None:
    """A created publisher can be retrieved by ID."""
    repository = PublisherRepository()

    publisher = repository.create(publisher_payload())

    assert isinstance(publisher, Publisher)
    assert repository.get_by_id("pub-1") == publisher


def test_list_publishers() -> None:
    """The repository lists all created publishers."""
    repository = PublisherRepository()
    repository.create(publisher_payload("pub-1"))
    repository.create(publisher_payload("pub-2"))

    assert repository.list_publishers() == [
        repository.get_by_id("pub-1"),
        repository.get_by_id("pub-2"),
    ]


def test_update_publisher() -> None:
    """An existing publisher can be updated."""
    repository = PublisherRepository()
    repository.create(publisher_payload())

    updated = repository.update(
        "pub-1",
        {"name": "New Name", "email": "new@example.com"},
    )

    assert updated.name == "New Name"
    assert updated.email == "new@example.com"


def test_delete_publisher() -> None:
    """An existing publisher can be deleted."""
    repository = PublisherRepository()
    repository.create(publisher_payload())

    assert repository.delete("pub-1") is True
    assert repository.list_publishers() == []


def test_unknown_publisher_id_raises_custom_exception() -> None:
    """Unknown IDs raise the repository's domain exception."""
    repository = PublisherRepository()

    with pytest.raises(PublisherNotFoundError):
        repository.get_by_id("missing")

    with pytest.raises(PublisherNotFoundError):
        repository.update("missing", {"name": "Unknown"})

    with pytest.raises(PublisherNotFoundError):
        repository.delete("missing")


if __name__ == "__main__":
    pytest.main(["-q", __file__])