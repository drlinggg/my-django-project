from rest_framework import serializers

from .models import Expense, Category


class CategoriesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class CategoriesReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoriesDetailReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ExpensesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class ExpensesReadSerializer(serializers.ModelSerializer):
    categories = CategoriesReadSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'
