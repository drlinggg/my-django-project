from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from expenses.views import (
    hello_ping,
    hello_world,
    CategoriesApiView,
    ExpensesApiView,
)


urlpatterns = [
    path("hello_ping/", hello_ping),
    path("", hello_world),
    path("expenses/", ExpensesApiView.as_view()),
    path("expenses/<uuid:pk>/", ExpensesApiView.as_view()),
    path("categories/", CategoriesApiView.as_view()),
    path("categories/<uuid:pk>/", CategoriesApiView.as_view()),
    # todo unite as token/
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]
