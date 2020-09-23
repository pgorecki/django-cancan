from core.models import Project, Membership, Issue


def declare_abilities(user, rules):
    if not user.is_authenticated or not user.is_active:
        # anonymous/inactive users can do nothing
        return False

    # logged in can view own content
    rules.allow("add", Project)
    rules.allow("view", Project, created_by=user)

    if user.is_superuser:
        rules.allow("view", Project)
