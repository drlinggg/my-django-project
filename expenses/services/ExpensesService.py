from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from rest_framework.exceptions import NotFound, ValidationError

from expenses.models import Expense, Category
from expenses.serializers import ExpensesUpdateSerializer, ExpensesWriteSerializer


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


def create_expense(user: AbstractUser, data: dict[str, any]) -> Expense:
    """
    Create a new expense for the user

    Args:
        user: User object - the authenticated user
        data: dict - expense data including:
            - value: decimal - expense amount
            - spent_at: datetime - when expense occurred
            - description: str - optional description
            - categories: list - optional list of category IDs

    Returns:
        Expense: The created expense object

    Raises:
        ValidationError: If input data is invalid
    """
    serializer = ExpensesWriteSerializer(data=data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    expense = serializer.save(creator=user)
    category_ids = data.get("categories", [])
    if category_ids:
        categories = Category.objects.filter(id__in=category_ids, creator=user)
        expense.categories.set(categories)

    return expense


def update_expense(
    user: AbstractUser, expense_id: str, data: dict[str, any]
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
        ValidationError: If input data is invalid
    """
    expense = get_expense_by_id(user, expense_id)

    serializer = ExpensesUpdateSerializer(expense, data=data, partial=True)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    updated_expense = serializer.save()

    if "categories" in data:
        category_ids = data["categories"]
        categories = Category.objects.filter(id__in=category_ids, creator=user)
        updated_expense.categories.set(categories)

    return updated_expense


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
