from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.middleware import AuthenticationMiddleware
from .models import Project


class HomeView(TemplateView):
    template_name = "home.html"


class ProjectListView(UserPassesTestMixin, ListView):
    model = Project

    def get_queryset(self):
        return self.request.ability.queryset_for("view", self.model)

    def test_func(self):
        return self.request.ability.can("view", self.model)


class ProjectDetailView(DetailView):
    model = Project

    def get_queryset(self):
        return self.request.ability.queryset_for("view", self.model)

    def test_func(self):
        return self.request.ability.can("view", self.model)


class ProjectCreateView(UserPassesTestMixin, CreateView):
    model = Project
    fields = ["name", "description"]

    def test_func(self):
        return self.request.ability.can("add", self.model)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project-detail", args=(self.object.id,))
