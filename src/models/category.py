"""Category entity and repository for the library management system."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

from models.exceptions import CategoryNotFoundError, InvalidCategoryError


@dataclass
class Category:
    """Represents a library category for organizing books.

    Args:
        name: The display name of the category.
        description: A short description of the category.
        category_id: Unique identifier assigned to the category.
        created_at: Timestamp when the category was created.
    """

    name: str
    description: str = ""
    category_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self) -> None:
        """Validate the category record after initialization.

        Returns:
            None: The object is ready for use once validation passes.
        """
        cleaned_name = (self.name or "").strip()
        if not cleaned_name:
            raise InvalidCategoryError("Category name cannot be blank.")

        self.name = cleaned_name
        self.description = (self.description or "").strip()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the category into a serializable dictionary.

        Returns:
            Dict[str, Any]: Serialized category fields.
        """
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
        }


class CategoryRepository:
    """In-memory repository for managing category records."""

    def __init__(self) -> None:
        """Initialize an empty repository and name lookup index.

        Returns:
            None: Creates the backing storage for categories.
        """
        self._categories: Dict[str, Category] = {}
        self._name_index: Dict[str, str] = {}

    def create(self, category_payload: Dict[str, Any]) -> Category:
        """Create a new category from a dictionary payload.

        Args:
            category_payload: A dictionary containing the category name and description.

        Returns:
            Category: The newly created category object.
        """
        name = str(category_payload.get("name", "")).strip()
        description = str(category_payload.get("description", "") or "").strip()

        if not name:
            raise InvalidCategoryError("Category name cannot be blank.")

        normalized_name = name.casefold()
        if normalized_name in self._name_index:
            raise InvalidCategoryError(f"Category '{name}' already exists.")

        category = Category(name=name, description=description)
        self._categories[category.category_id] = category
        self._name_index[normalized_name] = category.category_id
        return category

    def get_by_id(self, category_id: str) -> Category:
        """Retrieve a category by its unique identifier.

        Args:
            category_id: The UUID value for the category.

        Returns:
            Category: The matching category.
        """
        category = self._categories.get(category_id)
        if category is None:
            raise CategoryNotFoundError(f"Category '{category_id}' was not found.")
        return category

    def list_categories(self) -> List[Category]:
        """Return all categories stored in the repository.

        Returns:
            List[Category]: A list of current category objects.
        """
        return list(self._categories.values())

    def update(self, category_id: str, category_payload: Dict[str, Any]) -> Category:
        """Update an existing category with a partial payload.

        Args:
            category_id: The category identifier to update.
            category_payload: A dictionary of new category fields.

        Returns:
            Category: The updated category object.
        """
        category = self.get_by_id(category_id)
        new_name = category_payload.get("name", category.name)
        new_description = category_payload.get("description", category.description)

        cleaned_name = str(new_name).strip()
        if not cleaned_name:
            raise InvalidCategoryError("Category name cannot be blank.")

        if cleaned_name.casefold() != category.name.casefold():
            normalized_name = cleaned_name.casefold()
            if normalized_name in self._name_index and self._name_index[normalized_name] != category_id:
                raise InvalidCategoryError(f"Category '{cleaned_name}' already exists.")
            self._name_index.pop(category.name.casefold(), None)
            self._name_index[normalized_name] = category_id

        category.name = cleaned_name
        category.description = str(new_description or "").strip()
        return category

    def delete(self, category_id: str) -> bool:
        """Delete a category from the repository.

        Args:
            category_id: The category identifier to delete.

        Returns:
            bool: True when the category was successfully removed.
        """
        category = self.get_by_id(category_id)
        self._categories.pop(category_id, None)
        self._name_index.pop(category.name.casefold(), None)
        return True
