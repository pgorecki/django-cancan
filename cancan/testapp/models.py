from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    name = models.CharField(max_length=255)
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="articles", null=True
    )

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})
