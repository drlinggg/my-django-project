""" All serializers are defined here """

from rest_framework import serializers

from .models import Expense, Category


class CategoriesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class CategoriesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["id", "created_at", "updated_at", "creator"]


class CategoriesReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoriesDetailReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ExpensesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        exclude = ["id"]


class ExpensesReadSerializer(serializers.ModelSerializer):
    categories = CategoriesReadSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = "__all__"


class ExpensesUpdateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), required=False
    )

    class Meta:
        model = Expense
        exclude = ["id", "created_at", "updated_at", "creator"]
