"""In-memory repository for publisher records."""

from typing import Any, Dict, List

from models.exceptions import InvalidPublisherError, PublisherNotFoundError
from models.publisher import Publisher


class PublisherRepository:
    """Store and manage publishers in memory."""

    def __init__(self) -> None:
        """Initialize an empty publisher store.

        Args:
            None: This repository does not require initial data.

        Returns:
            None: Creates the in-memory publisher storage.
        """
        self._publishers: Dict[str, Publisher] = {}

    def create(self, publisher_payload: Dict[str, Any]) -> Publisher:
        """Create and store a publisher from a dictionary payload.

        Args:
            publisher_payload: A dictionary containing publisher_id, name, and email.

        Returns:
            Publisher: The newly created publisher.
        """
        required_fields = ("publisher_id", "name", "email")
        if any(field not in publisher_payload for field in required_fields):
            raise InvalidPublisherError("Publisher payload must include all required fields.")

        publisher = Publisher(
            publisher_id=str(publisher_payload["publisher_id"]),
            name=str(publisher_payload["name"]),
            email=str(publisher_payload["email"]),
        )
        self._publishers[publisher.publisher_id] = publisher
        return publisher

    def get_by_id(self, publisher_id: str) -> Publisher:
        """Retrieve a publisher by its identifier.

        Args:
            publisher_id: The identifier of the publisher to retrieve.

        Returns:
            Publisher: The matching publisher.

        Raises:
            PublisherNotFoundError: If no publisher has the requested identifier.
        """
        publisher = self._publishers.get(publisher_id)
        if publisher is None:
            raise PublisherNotFoundError(f"Publisher '{publisher_id}' was not found.")
        return publisher

    def list_publishers(self) -> List[Publisher]:
        """List every publisher currently in the repository.

        Args:
            None: This method does not require filtering parameters.

        Returns:
            List[Publisher]: The publishers in insertion order.
        """
        return list(self._publishers.values())

    def update(self, publisher_id: str, publisher_payload: Dict[str, Any]) -> Publisher:
        """Update an existing publisher with supplied fields.

        Args:
            publisher_id: The identifier of the publisher to update.
            publisher_payload: A dictionary containing fields to update.

        Returns:
            Publisher: The updated publisher.

        Raises:
            PublisherNotFoundError: If no publisher has the requested identifier.
        """
        publisher = self.get_by_id(publisher_id)
        if "name" in publisher_payload:
            publisher.name = str(publisher_payload["name"])
        if "email" in publisher_payload:
            publisher.email = str(publisher_payload["email"])
        return publisher

    def delete(self, publisher_id: str) -> bool:
        """Delete a publisher by its identifier.

        Args:
            publisher_id: The identifier of the publisher to delete.

        Returns:
            bool: True when the publisher is removed.

        Raises:
            PublisherNotFoundError: If no publisher has the requested identifier.
        """
        self.get_by_id(publisher_id)
        del self._publishers[publisher_id]
        return True