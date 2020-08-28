from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TodoItem(models.Model):
    name = models.CharField(max_length=128)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'#{self.id} {self.name} (by {self.created_by.username})'
