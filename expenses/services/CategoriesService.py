from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from rest_framework.exceptions import NotFound, ValidationError

from expenses.models import Category
from expenses.serializers import CategoriesUpdateSerializer, CategoriesWriteSerializer


def get_categories(user: AbstractUser) -> QuerySet[Category]:
    return Category.objects.filter(creator=user).distinct()


def get_category_by_id(user: AbstractUser, category_id: str) -> Category:
    try:
        return Category.objects.get(id=category_id, creator=user)
    except Category.DoesNotExist:
        raise NotFound(f"Category with id {category_id} not found")


def create_category(user: AbstractUser, data: dict) -> Category:
    serializer = CategoriesWriteSerializer(data=data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)
    category = serializer.save(creator=user)
    return category


def update_category(user: AbstractUser, category_id: str, data: dict) -> Category:
    category = get_category_by_id(user, category_id)

    serializer = CategoriesUpdateSerializer(category, data=data, partial=True)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    return serializer.save()


def delete_category(user: AbstractUser, category_id: str) -> bool:
    category = get_category_by_id(user, category_id)
    category.delete()
    return True
