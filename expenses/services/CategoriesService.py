from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from rest_framework.exceptions import NotFound, ValidationError

from expenses.models import Category
from expenses.serializers import CategoriesUpdateSerializer, CategoriesWriteSerializer


def get_categories(user: AbstractUser) -> QuerySet[Category]:
    """
    Get all categories for the user

    Args:
        user: User object - the authenticated user

    Returns:
        QuerySet: All categories belonging to the user
    """
    return Category.objects.filter(creator=user).distinct()


def get_category_by_id(user: AbstractUser, category_id: str) -> Category:
    """
    Get specific category by ID for the given user

    Args:
        user: User object - the authenticated user
        category_id: UUID - ID of the category to retrieve

    Returns:
        Category: The requested category object

    Raises:
        NotFound: If category doesn't exist or doesn't belong to user
    """
    try:
        return Category.objects.get(id=category_id, creator=user)
    except Category.DoesNotExist:
        raise NotFound(f"Category with id {category_id} not found")


def create_category(user: AbstractUser, data: dict) -> Category:
    """
    Create a new category for the user

    Args:
        user: User object - the authenticated user
        data: dict - category data including:
            - name: str - category name
            - description: str - optional description
            - color: str - optional color code

    Returns:
        Category: The created category object

    Raises:
        ValidationError: If input data is invalid
    """
    serializer = CategoriesWriteSerializer(data=data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)
    category = serializer.save(creator=user)
    return category


def update_category(user: AbstractUser, category_id: str, data: dict) -> Category:
    """
    Update an existing category

    Args:
        user: User object - the authenticated user
        category_id: UUID - ID of the category to update
        data: dict - updated category data

    Returns:
        Category: The updated category object

    Raises:
        NotFound: If category doesn't exist or doesn't belong to user
        ValidationError: If input data is invalid
    """
    category = get_category_by_id(user, category_id)

    serializer = CategoriesUpdateSerializer(category, data=data, partial=True)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    return serializer.save()


def delete_category(user: AbstractUser, category_id: str) -> bool:
    """
    Delete a category

    Args:
        user: User object - the authenticated user
        category_id: UUID - ID of the category to delete

    Returns:
        bool: True if deletion was successful

    Raises:
        NotFound: If category doesn't exist or doesn't belong to user
    """
    category = get_category_by_id(user, category_id)
    category.delete()
    return True
