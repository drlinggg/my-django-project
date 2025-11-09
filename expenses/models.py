""" All models are defined here """

import uuid

from django.db import models
from django.contrib.auth import get_user_model


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
    categories = models.ManyToManyField(Category)  # TODO: fix here?

    def __str__(self):
        return f"{self.value} - {self.spent_at}"
