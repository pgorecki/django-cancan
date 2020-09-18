from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Article


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        # this is how you can retrieve all objects a user can access
        qs = self.request.ability.queryset_for("view", Article)
        return qs


class ArticleDetailView(PermissionRequiredMixin, DetailView):
    queryset = Article.objects.all()

    def has_permission(self):
        article = self.get_object()
        # this is how you can check if user can access an object
        return self.request.ability.can("view", article)
