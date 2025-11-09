from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from expenses.serializers import ExpensesReadSerializer
from expenses.services import (
    get_expense_by_id,
    get_expenses_with_filters,
    create_expense,
    update_expense,
    delete_expense,
)


class ExpensesApiView(APIView):
    """
    API View for managing user expenses

    Provides CRUD operations for expenses with filtering support:
    - List all expenses with optional filters (GET /)
    - Retrieve specific expense (GET /{id})
    - Create new expense (POST /)
    - Update existing expense (PUT /{id})
    - Delete expense (DELETE /{id})

    Supports filtering by date range, value range, and categories for listing.
    Requires authentication for all operations.
    """
    permission_classes: list = [IsAuthenticated]

    def get(self, request: Request, pk: str | None = None) -> Response:
        """
        Retrieve expense/expenses

        Args:
            request: Request - the HTTP request object
            pk: str | None - optional expense ID for single expense retrieval

        Query Parameters (when no pk provided):
            - start_date: filter expenses from this date (YYYY-MM-DD)
            - end_date: filter expenses until this date (YYYY-MM-DD)
            - min_value: filter expenses with value >= this amount
            - max_value: filter expenses with value <= this amount
            - categories: comma-separated list of category IDs to filter by

        Returns:
            Response: 
                - Single expense details if pk provided
                - List of filtered expenses if no pk provided

        Status Codes:
            200: Successfully retrieved data
            404: Expense not found (when pk provided)
        """
        if pk:
            expense = get_expense_by_id(request.user, pk)
            serializer = ExpensesReadSerializer(expense)
            return Response(serializer.data)

        filters = request.query_params.dict()
        expenses = get_expenses_with_filters(request.user, filters)
        serializer = ExpensesReadSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Create a new expense

        Args:
            request: Request - the HTTP request object with expense data including:
                - value: decimal - expense amount (required)
                - spent_at: datetime - when expense occurred (required)
                - description: str - optional description
                - categories: list - optional list of category IDs

        Returns:
            Response: Created expense data

        Status Codes:
            201: Expense successfully created
            400: Invalid input data
        """
        try:
            expense = create_expense(request.user, request.data)
            serializer = ExpensesReadSerializer(expense)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, pk: str) -> Response:
        """
        Update an existing expense

        Args:
            request: Request - the HTTP request object with updated expense data
            pk: str - ID of the expense to update

        Returns:
            Response: Updated expense data

        Status Codes:
            200: Expense successfully updated
            400: Invalid input data
            404: Expense not found
        """
        try:
            expense = update_expense(request.user, pk, request.data)
            serializer = ExpensesReadSerializer(expense)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: str) -> Response:
        """
        Delete an expense

        Args:
            request: Request - the HTTP request object
            pk: str - ID of the expense to delete

        Returns:
            Response: Empty response with appropriate status code

        Status Codes:
            204: Expense successfully deleted
            400: Deletion failed
            404: Expense not found
        """
        try:
            delete_expense(request.user, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
