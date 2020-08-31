from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from .models import TodoItem

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.middleware import AuthenticationMiddleware


class TodoIndexView(ListView):
    model = TodoItem

    def get_query_set():
        qs = self.request.user.accessible_query_set(TodoItem)
        return qs


class TodoDetailView(PermissionRequiredMixin, DetailView):
    queryset = TodoItem.objects.all()

    def has_permission(self):
        obj = self.get_object()
        return self.request.user.can('view', obj)
