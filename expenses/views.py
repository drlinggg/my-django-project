from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.

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
    return HttpResponse("<h1>Hello pong!</h1>")

def hello_world(request: HttpRequest):
    return HttpResponse("<h1>Hello world!</h1>")
