from django.http import HttpRequest, HttpResponse
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
    permission_classes: list = [IsAuthenticated]

    def get(self, request: Request, pk: str | None = None) -> Response:
        if pk:
            expense = get_expense_by_id(request.user, pk)
            serializer = ExpensesReadSerializer(expense)
            return Response(serializer.data)

        filters = request.query_params.dict()
        expenses = get_expenses_with_filters(request.user, filters)
        serializer = ExpensesReadSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        try:
            expense = create_expense(request.user, request.data)
            serializer = ExpensesReadSerializer(expense)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, pk: str) -> Response:
        try:
            expense = update_expense(request.user, pk, request.data)
            serializer = ExpensesReadSerializer(expense)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: str) -> Response:
        try:
            delete_expense(request.user, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
