from django.http import HttpRequest, HttpResponse


def hello_ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Hello pong!</h1>")


def hello_world(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Hello world!</h1>")
