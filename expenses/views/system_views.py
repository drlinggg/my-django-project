""" All system views are defined here """

from django.http import HttpRequest, HttpResponse


def hello_ping(request: HttpRequest) -> HttpResponse:
    """
    Simple ping endpoint for health checks

    Args:
        request: HttpRequest - the HTTP request object

    Returns:
        HttpResponse: HTML response with "Hello pong!" message

    Status Codes:
        200: Always returns successful response
    """
    return HttpResponse("<h1>Hello pong!</h1>")


def hello_world(request: HttpRequest) -> HttpResponse:
    """
    Simple hello world endpoint

    Args:
        request: HttpRequest - the HTTP request object

    Returns:
        HttpResponse: HTML response with "Hello world!" message

    Status Codes:
        200: Always returns successful response
    """
    return HttpResponse("<h1>Hello world!</h1>")
