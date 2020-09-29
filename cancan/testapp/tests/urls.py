# handler404 and handler500 are needed for admin tests
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.views.generic import View
from cancan.testapp.views import ArticleListView

admin.autodiscover()


# class TestClassRedirectView(PermissionRequiredMixin, View):
#     permission_required = 'testapp.change_project'


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", LoginView.as_view(template_name="blank.html")),
    path("articles/", ArticleListView.as_view()),
]
