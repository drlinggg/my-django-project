from django.urls import path
from .views import hello_ping, hello_world


urlpatterns = [
    path("hello_ping/", hello_ping),
    path('', hello_world),
]
