from django.http import HttpResponse, HttpRequest
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Category, Expense
from .serializers import (
    CategoriesWriteSerializer,
    CategoriesDetailReadSerializer,
    CategoriesReadSerializer,
    ExpensesWriteSerializer,
    ExpensesReadSerializer,
)

from .services import *

"""
REST API должен быть реализован с помощью Django REST Framework
Необходимо использовать разные сериализаторы для чтения и записи
Каждый эндпоинт должен аутентифицировать пользователя по jwt-токену

CRUD категорий - пользователь может взаимодействовать только со своими категориями:

GET /api/categories - список категорий пользователя
POST /api/categories - создать категорию
GET /api/categories/{id} - получить категорию
PUT /api/categories/{id} - обновить категорию
DELETE /api/categories/{id} - удалить категорию

CRUD расходов - пользователь может взаимодействовать только со своими расходами:
GET /api/expenses - список расходов пользователя поддерживает фильтрацию по диапазону дат, сумме и категориям (для реализации необходимо воспользоваться библиотекой django-filter)
POST /api/expenses - создать расход
GET /api/expenses/{id} - получить расход
PUT /api/expenses/{id} - обновить расход
DELETE /api/expenses/{id} - удалить расход
"""


def hello_ping(request: HttpRequest):
    """ hello pong html response """
    return HttpResponse("<h1>Hello pong!</h1>")


def hello_world(request: HttpRequest):
    """ hello world html response """
    return HttpResponse("<h1>Hello world!</h1>")


class ExpensesApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        # get via id
        if pk:
            expense = get_expense_by_id(request.user, pk)
            serializer = ExpensesReadSerializer(expense)
            return Response(serializer.data)

        # get all via filtering
        filters = request.query_params.dict()
        expenses = get_expenses_with_filters(request.user, filters)
        serializer = ExpensesReadSerializer(expenses, many=True)
        return Response(serializer.data)

        

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass


class CategoriesApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass
