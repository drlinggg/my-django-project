import uuid

from django.db import models
from django.contrib.auth import get_user_model


"""
User - стандартная модель пользователя Django

BaseModel
id
created_at
updated_at

Category
id - идентификатор (uuid)  -> Basemodel.id
name - название категории
creator - создатель
created_at - дата и время создания (устанавливается автоматически) -> BaseModel.created_at
updated_at - дата и время обновления (устанавливается автоматически) -> BaseModel.updated_at

Expense
id - идентификатор (uuid) -> Basemodel.id
value - сумма траты
spent_at - дата и время траты
description - описание (может быть null)
creator - создатель
categories - категории траты (может быть несколько)
created_at - дата и время создания (устанавливается автоматически) -> BaseModel.created_at
updated_at - дата и время обновления (устанавливается автоматически) -> BaseModel.updated_at
"""

User = get_user_model()

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Expense(BaseModel):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    spent_at = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category) # TODO: fix here?

    def __str__(self):
        return f"{self.value} - {self.spent_at}"
