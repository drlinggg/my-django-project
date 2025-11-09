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
    """
    API View for managing user categories

    Provides CRUD operations for categories:
    - List all categories (GET /)
    - Retrieve specific category (GET /{id})
    - Create new category (POST /)
    - Update existing category (PUT /{id})
    - Delete category (DELETE /{id})

    Requires authentication for all operations.
    """
    permission_classes: list = [IsAuthenticated]

    def get(self, request: Request, pk: str | None = None) -> Response:
        """
        Retrieve category/categories

        Args:
            request: Request - the HTTP request object
            pk: str | None - optional category ID for single category retrieval

        Returns:
            Response:
                - Single category details if pk provided
                - List of all categories if no pk provided

        Status Codes:
            200: Successfully retrieved data
            404: Category not found (when pk provided)
        """
        if pk:
            category = get_category_by_id(request.user, pk)
            serializer = CategoriesDetailReadSerializer(category)
            return Response(serializer.data)

        categories = get_categories(request.user)
        serializer = CategoriesReadSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Create a new category

        Args:
            request: Request - the HTTP request object with category data

        Returns:
            Response: Created category data

        Status Codes:
            201: Category successfully created
            400: Invalid input data
        """
        try:
            category = create_category(request.user, request.data)
            serializer = CategoriesReadSerializer(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, pk: str) -> Response:
        """
        Update an existing category

        Args:
            request: Request - the HTTP request object with updated category data
            pk: str - ID of the category to update

        Returns:
            Response: Updated category data

        Status Codes:
            200: Category successfully updated
            400: Invalid input data
            404: Category not found
        """
        try:
            category = update_category(request.user, pk, request.data)
            serializer = CategoriesReadSerializer(category)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: str) -> Response:
        """
        Delete a category

        Args:
            request: Request - the HTTP request object
            pk: str - ID of the category to delete

        Returns:
            Response: Empty response with appropriate status code

        Status Codes:
            204: Category successfully deleted
            400: Deletion failed
            404: Category not found
        """
        try:
            delete_category(request.user, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
