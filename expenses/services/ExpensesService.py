from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.db.models import QuerySet
from rest_framework.exceptions import NotFound

from expenses.models import Expense, Category


@transaction.atomic
def get_expenses_with_filters(
    user: AbstractUser, filters: dict[str, any] | None = None
) -> QuerySet[Expense]:
    """
    Get user's expenses with optional filtering

    Args:
        user: User object - the authenticated user
        filters: dict - optional filters including:
            - start_date: filter expenses from this date
            - end_date: filter expenses until this date
            - min_value: filter expenses with value >= this
            - max_value: filter expenses with value <= this
            - categories: list of category IDs to filter by

    Returns:
        QuerySet: Filtered expenses for the user
    """
    queryset = Expense.objects.filter(creator=user)
    if not filters:
        return queryset

    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    if start_date and end_date:
        queryset = queryset.filter(spent_at__range=[start_date, end_date])

    min_value = filters.get("min_value")
    max_value = filters.get("max_value")
    if min_value:
        queryset = queryset.filter(value__gte=min_value)
    if max_value:
        queryset = queryset.filter(value__lte=max_value)

    category_ids = filters.get("categories")
    if category_ids:
        if isinstance(category_ids, str):
            category_ids = category_ids.split(",")
        queryset = queryset.filter(categories__id__in=category_ids)

    return queryset.distinct()


@transaction.atomic
def get_expense_by_id(user: AbstractUser, expense_id: str) -> Expense:
    """
    Get specific expense by ID for the given user

    Args:
        user: User object - the authenticated user
        expense_id: UUID - ID of the expense to retrieve

    Returns:
        Expense: The requested expense object

    Raises:
        NotFound: If expense doesn't exist or doesn't belong to user
    """
    try:
        return Expense.objects.get(id=expense_id, creator=user)
    except Expense.DoesNotExist:
        raise NotFound(f"Expense with id {expense_id} not found")


@transaction.atomic
def create_expense(user: AbstractUser, validated_data: dict[str, any]) -> Expense:
    """
    Create a new expense for the user

    Args:
        user: User object - the authenticated user
        data: dict - expense data

    Returns:
        Expense: The created expense object
    """
    expense = Expense.objects.create(creator=user, **validated_data)
    category_ids = validated_data.get("categories", [])
    if category_ids:
        categories = Category.objects.filter(id__in=category_ids, creator=user)
        expense.categories.set(categories)

    return expense


@transaction.atomic
def update_expense(
    user: AbstractUser, expense_id: str, validated_data: dict[str, any]
) -> Expense:
    """
    Update an existing expense

    Args:
        user: User object - the authenticated user
        expense_id: UUID - ID of the expense to update
        data: dict - updated expense data

    Returns:
        Expense: The updated expense object

    Raises:
        NotFound: If expense doesn't exist or doesn't belong to user
    """
    expense = get_expense_by_id(user, expense_id)
    categories = validated_data.pop("categories", None)

    for attr, value in validated_data.items():
        setattr(expense, attr, value)
    expense.save()

    if categories is not None:
        expense.categories.set(categories)

    return expense


@transaction.atomic
def delete_expense(user: AbstractUser, expense_id: str) -> bool:
    """
    Delete an expense

    Args:
        user: User object - the authenticated user
        expense_id: UUID - ID of the expense to delete

    Returns:
        bool: True if deletion was successful

    Raises:
        NotFound: If expense doesn't exist or doesn't belong to user
    """
    expense = get_expense_by_id(user, expense_id)
    expense.delete()
    return True
