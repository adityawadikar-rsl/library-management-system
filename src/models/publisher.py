"""Publisher entity for the library management system."""

from dataclasses import dataclass


@dataclass
class Publisher:
    """Represent a publisher associated with library books.

    Args:
        publisher_id: The unique identifier for the publisher.
        name: The publisher's name.
        email: The publisher's contact email address.

    Returns:
        None: Dataclass instances are initialized with the supplied fields.
    """

    publisher_id: str
    name: str
    email: str