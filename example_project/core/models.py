from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(default="", blank=True)
    members = models.ManyToManyField(User, through="Membership")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Issue(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(default="", blank=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues_assigned",
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="issues_created"
    )
