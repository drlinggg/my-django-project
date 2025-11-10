""" All middlewares are defined here """

import typing as tp

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class MyExceptionMiddleware:

    def __init__(self, get_response: tp.Callable):
        self._get_response = get_response

    def __call__(self, request: Request) -> Response:
        try:
            response = self._get_response(request)
        except ValidationError as e:
            return Response({"exception": str(e)}, status=HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({"exception": str(e)}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"exception": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response
