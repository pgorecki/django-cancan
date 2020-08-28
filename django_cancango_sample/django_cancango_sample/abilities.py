from sample.models import TodoItem


def declare_abilities(user, ability):
    if not user.is_authenticated:
        return False

    # TODO:
    # multiple can will be OR'ed
    # after can, you can put cannot which will be overriden by following can

    # Logged in user can view his own todos
    ability.can('view', TodoItem, created_by=user.id)

    if user.has_perm('sample.view_todo'):
        # OR condition - allow to view all todo items
        ability.can('view', TodoItem)
