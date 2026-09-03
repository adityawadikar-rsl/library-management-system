"""Tests for the category model and repository."""

import pytest

from models.category import Category, CategoryRepository
from models.exceptions import InvalidCategoryError, CategoryNotFoundError


class TestCategory:
    """Validate category entity behavior."""

    def test_category_creation(self) -> None:
        """A valid category should create a clean entity."""
        category = Category(name="Fiction", description="Novels and stories")

        assert category.name == "Fiction"
        assert category.description == "Novels and stories"
        assert category.category_id

    def test_category_creation_rejects_blank_name(self) -> None:
        """Blank category names are invalid."""
        with pytest.raises(InvalidCategoryError):
            Category(name="   ", description="Invalid name")


class TestCategoryRepository:
    """Validate repository CRUD behavior."""

    def test_repository_create_and_list(self) -> None:
        """Create a category and retrieve it from the repository."""
        repository = CategoryRepository()
        category = repository.create({"name": "Science", "description": "Science books"})

        assert category.name == "Science"
        assert repository.get_by_id(category.category_id).name == "Science"
        assert len(repository.list_categories()) == 1

    def test_repository_rejects_duplicate_names(self) -> None:
        """Duplicate category names should not exist in the repository."""
        repository = CategoryRepository()
        repository.create({"name": "History", "description": "World history"})

        with pytest.raises(InvalidCategoryError):
            repository.create({"name": "history", "description": "duplicate"})

    def test_repository_update_and_delete(self) -> None:
        """Update a category and then delete it."""
        repository = CategoryRepository()
        category = repository.create({"name": "Technology", "description": "Old description"})

        updated = repository.update(category.category_id, {"name": "Technology", "description": "Updated description"})
        assert updated.description == "Updated description"

        assert repository.delete(category.category_id) is True

        with pytest.raises(CategoryNotFoundError):
            repository.get_by_id(category.category_id)


if __name__ == "__main__":
    pytest.main(["-q", __file__])
