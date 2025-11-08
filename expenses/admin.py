from django.contrib import admin
from .models import Expense, Category

# Register your models here.


class CategoryInline(admin.TabularInline):
    model = Expense.categories.through
    extra = 1
    verbose_name = "Категория"
    verbose_name_plural = "Категории"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "creator", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name"]


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["value", "spent_at", "creator", "created_at"]
    list_filter = ["spent_at", "created_at"]
    search_fields = ["description"]

    exclude = ("categories",)
    inlines = [CategoryInline]


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category, CategoryAdmin)
