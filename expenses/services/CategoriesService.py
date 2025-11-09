from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.db.models import QuerySet
from rest_framework.exceptions import NotFound

from expenses.models import Category


@transaction.atomic
def get_categories(user: AbstractUser) -> QuerySet[Category]:
    """
    Get all categories for the user

    Args:
        user: User object - the authenticated user

    Returns:
        QuerySet: All categories belonging to the user
    """
    return Category.objects.filter(creator=user).distinct()


@transaction.atomic
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


@transaction.atomic
def create_category(user: AbstractUser, validated_data: dict) -> Category:
    """
    Create a new category for the user

    Args:
        user: User object - the authenticated user
        validated_data: dict - category data

    Returns:
        Category: The created category object
    """

    category = Category.objects.create(creator=user, **validated_data)
    return category


@transaction.atomic
def update_category(
    user: AbstractUser, category_id: str, validated_data: dict
) -> Category:
    """
    Update an existing category

    Args:
        user: User object - the authenticated user
        category_id: UUID - ID of the category to update
        validated_data: dict - updated category data

    Returns:
        Category: The updated category object

    Raises:
        NotFound: If category doesn't exist or doesn't belong to user
    """
    category = get_category_by_id(user, category_id)
    for attr, value in validated_data.items():
        setattr(category, attr, value)

    category.save()
    return category


@transaction.atomic
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
