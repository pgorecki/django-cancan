from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

import core.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/profile/", RedirectView.as_view(url="/projects")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", core.views.HomeView.as_view(), name="home"),
    path("projects/", core.views.ProjectListView.as_view(), name="project_list"),
    path("projects/new/", core.views.ProjectCreateView.as_view(), name="project_new"),
    path(
        "projects/<pk>/", core.views.ProjectDetailView.as_view(), name="project_detail"
    ),
    path(
        "projects/<pk>/edit/",
        core.views.ProjectUpdateView.as_view(),
        name="project_edit",
    ),
]
