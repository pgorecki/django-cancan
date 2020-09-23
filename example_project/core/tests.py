from django.contrib.auth.models import AnonymousUser, User
from cancan.middleware import CanCanMiddleware
from core.views import ProjectListView
from core.models import Project


def test_login_required_for_projects_page(rf):
    request = rf.get("/projects/")
    request.user = AnonymousUser()
    CanCanMiddleware().process_request(request)
    response = ProjectListView.as_view()(request)
    assert response.status_code == 302


def test_user_can_see_his_own_projects(rf):
    alice = User.objects.create(username="alice")
    bob = User.objects.create(username="bob")

    project1 = Project.objects.create(name="Project 1", created_by=alice)
    project2 = Project.objects.create(name="Project 2", created_by=bob)

    request = rf.get("/projects/")
    request.user = alice
    CanCanMiddleware().process_request(request)
    response = ProjectListView.as_view()(request)
    assert response.status_code == 200
    assert response.context_data["object_list"].count() == 1


def test_admin_can_see_his_own_projects(rf):
    alice = User.objects.create(username="alice", is_superuser=True)
    bob = User.objects.create(username="bob")

    project1 = Project.objects.create(name="Project 1", created_by=alice)
    project2 = Project.objects.create(name="Project 2", created_by=bob)

    request = rf.get("/projects/")
    request.user = alice
    CanCanMiddleware().process_request(request)
    response = ProjectListView.as_view()(request)
    assert response.status_code == 200
    assert response.context_data["object_list"].count() == 2
