from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from expenses.serializers import (
    CategoriesDetailReadSerializer,
    CategoriesReadSerializer,
)
from expenses.services import (
    get_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
)


class CategoriesApiView(APIView):
    permission_classes: list = [IsAuthenticated]

    def get(self, request: Request, pk: str | None = None) -> Response:
        if pk:
            category = get_category_by_id(request.user, pk)
            serializer = CategoriesDetailReadSerializer(category)
            return Response(serializer.data)

        categories = get_categories(request.user)
        serializer = CategoriesReadSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        try:
            category = create_category(request.user, request.data)
            serializer = CategoriesReadSerializer(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, pk: str) -> Response:
        try:
            category = update_category(request.user, pk, request.data)
            serializer = CategoriesReadSerializer(category)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: str) -> Response:
        try:
            delete_category(request.user, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
