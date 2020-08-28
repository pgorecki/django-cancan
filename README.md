# django-cancango

`django-cancango` is an authorization library for Django. It works on top of default Django permissions and allows to restrict the resources (models and objects) a given user can access.

This library is inspiered by `cancancan` for Ruby on Rails.

## Quick start

1. Add `cancango` to your `INSTALLED_APPS` setting like this:

```python
INSTALLED_APPS = [
    ...,
    'cancango',
]
```

2. Create a function that define user abilites. For example, in `abilities.py`:

```python
def declare_abilities(user, ability):
    if not user.is_authenticated:
        # Allow anonymous users to view published articles
        return ability.can('view', Article, published=True)

    if user.has_perm('article.view_own_article'):
        # Allow logged in user to change his articles
        return ability.can('change', Article, author=user)

    if user.is_superuser:
        # Allow superuser change all articles
        return ability.can('change', Article)
```

3. Configure `cancango` by adding `CANCANGO` section in `settings.py`:

```python
CANCANGO = {
    'ABILITIES': 'myapp.abilities.declare_abilities'
}
```

Next, add `cancango` middleware after `AuthenticationMiddleware`:

```python
MIDDLEWARE = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cancango.middleware.CanCanGoMiddleware',
    ...
]
```

Adding the middleware adds `request.user.can(...)` function that you can use
to check for model or object permissions.

4. Check abilities in a view:

```python
class ArticleDetailView(PermissionRequiredMixin, DetailView):
    queryset = TodoItem.objects.all()

    def has_permission(self):
        article = self.get_object()
        return self.request.user.can('view', article)
```

## Testing

Run `./manage.py test` to run all test for the `testapp`
